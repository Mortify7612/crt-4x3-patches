#!/usr/bin/env python3
"""Decrypt a retail disc SELF (APP) or free-license NPDRM SELF into a plain ELF, following RPCS3's unself.cpp.

usage: unself.py KEYS EBOOT.BIN OUT.elf
KEYS is RPCS3's rpcs3/Crypto directory (key_vault.cpp + key_vault.h); see keys.py.
Prints the RPCS3 patch hash (PPU-...) of the result.
"""
import hashlib, os, re, struct, sys, zlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def aes_cbc_dec(key, iv, data):
    d = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    return d.update(data) + d.finalize()


def aes_ctr(key, iv, data):
    d = Cipher(algorithms.AES(key), modes.CTR(iv)).decryptor()
    return d.update(data) + d.finalize()


def vault_keys(vault_src, arr='sk_APP_arr', kt='KEY_APP'):
    keys = {}
    pat = re.compile(arr + r'\.emplace_back\([^,]+,[^,]+,\s*(0x[0-9A-Fa-f]+),\s*' + kt + r',\s*"([0-9A-F]+)",\s*"([0-9A-F]+)"')
    for rev, erk, riv in pat.findall(vault_src):
        keys.setdefault(int(rev, 16), (bytes.fromhex(erk), bytes.fromhex(riv)))
    return keys


def app_keys(vault_src):
    return vault_keys(vault_src)


def read_vault(path):
    """Text of key_vault.cpp + key_vault.h from RPCS3's Crypto directory (or a path to key_vault.cpp)."""
    d = path if os.path.isdir(path) else os.path.dirname(path)
    return ''.join(open(os.path.join(d, n)).read() for n in ('key_vault.cpp', 'key_vault.h'))


def vault_array(vault_src, name):
    """A constexpr u8 NAME[...] = { 0x.., ... }; array from key_vault.h."""
    m = re.search(name + r'\[[^\]]*\]\s*=\s*\{([^}]*)\}', vault_src)
    assert m, f'{name} not found in key_vault.h'
    return bytes(int(x, 16) for x in re.findall(r'0x([0-9A-Fa-f]{2})', m.group(1)))


def aes_ecb_dec(key, data):
    d = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    return d.update(data) + d.finalize()


def supplemental(f, ext):
    """Yield (type, offset, size) for each supplemental/control-info header."""
    a, end = ext[7], ext[7] + ext[8]
    while a < end:
        t, sz, nxt = struct.unpack_from('>IIQ', f, a)
        yield t, a, sz
        a += sz
        if not nxt:
            break


def decrypt_meta_info(vault_src, f):
    """Return the decrypted 0x40-byte metadata info for an APP (4) or free-license NPDRM (8) SELF."""
    _, _, flags, _, meta, _, _ = struct.unpack_from('>IIHHIQQ', f, 0)
    ext = struct.unpack_from('>10Q', f, 0x20)
    ptype = struct.unpack_from('>I', f, ext[1] + 12)[0]
    info = f[0x20 + meta:0x20 + meta + 0x40]
    if ptype == 4:
        erk, riv = vault_keys(vault_src)[flags]
    elif ptype == 8:
        erk, riv = vault_keys(vault_src, 'sk_NPDRM_arr', 'KEY_NPDRM')[flags]
        npd = [o for t, o, _ in supplemental(f, ext) if t == 3]
        if npd:
            license = struct.unpack_from('>i', f, npd[0] + 16 + 8)[0]
            assert license == 3, f'NPDRM license {license} needs a RAP file'
            npdrm_key = aes_ecb_dec(vault_array(vault_src, 'NP_KLIC_KEY'), vault_array(vault_src, 'NP_KLIC_FREE'))
            info = aes_cbc_dec(npdrm_key, b'\0' * 16, info)
    else:
        raise AssertionError(f'unsupported program type {ptype}')
    return aes_cbc_dec(erk, riv, info)


def main(vault_path, self_path, out_path):
    f = open(self_path, 'rb').read()

    magic, hver, flags, stype, meta, hsize, esize = struct.unpack_from('>IIHHIQQ', f, 0)
    assert magic == 0x53434500, 'not a SELF'
    ext = struct.unpack_from('>10Q', f, 0x20)
    pid_off, ehdr_off, phdr_off = ext[1], ext[2], ext[3]
    auth_id, vendor, ptype, sce_ver = struct.unpack_from('>QIIQ', f, pid_off)
    print(f'SELF rev=0x{flags:x} type={stype} program_type={ptype} auth=0x{auth_id:x} ver=0x{sce_ver:x}')

    ehdr = bytearray(f[ehdr_off:ehdr_off + 0x40])
    e_phoff, e_shoff = struct.unpack_from('>QQ', ehdr, 0x20)
    e_phentsize, e_phnum = struct.unpack_from('>HH', ehdr, 0x36)
    phdrs = [struct.unpack_from('>IIQQQQQQ', f, phdr_off + i * 0x38) for i in range(e_phnum)]

    info = decrypt_meta_info(read_vault(vault_path), f)
    mkey, mkey_pad, miv, miv_pad = info[0:16], info[16:32], info[32:48], info[48:64]
    assert mkey_pad[0] == 0 and miv_pad[0] == 0, 'metadata info did not decrypt (wrong key?)'

    hdr_start = 0x20 + meta + 0x40
    mh = aes_ctr(mkey, miv, f[hdr_start:hsize])
    _, _, sec_count, key_count, _, _, _ = struct.unpack_from('>QIIIIII', mh, 0)
    secs = [struct.unpack_from('>QQIIIIIIII', mh, 0x20 + i * 0x30) for i in range(sec_count)]
    dkeys = mh[0x20 + sec_count * 0x30:0x20 + sec_count * 0x30 + key_count * 0x10]
    dk = lambda i: dkeys[i * 16:(i + 1) * 16]

    size = max(p[2] + p[5] for p in phdrs)
    out = bytearray(max(size, e_phoff + e_phnum * e_phentsize))
    struct.pack_into('>Q', ehdr, 0x28, 0)  # drop section headers: e_shoff
    struct.pack_into('>HH', ehdr, 0x3c, 0, 0)  # e_shnum, e_shstrndx
    out[0:0x40] = ehdr
    out[e_phoff:e_phoff + e_phnum * 0x38] = f[phdr_off:phdr_off + e_phnum * 0x38]

    for off, dsize, typ, pidx, hashed, sha_idx, enc, kidx, ividx, comp in secs:
        if typ != 2:
            continue
        data = f[off:off + dsize]
        if enc == 3:
            data = aes_ctr(dk(kidx), dk(ividx), data)
        if comp == 2:
            data = zlib.decompress(data)
        p = phdrs[pidx]
        assert len(data) == p[5], f'segment {pidx}: size {len(data):#x} != filesz {p[5]:#x}'
        out[p[2]:p[2] + len(data)] = data

    open(out_path, 'wb').write(out)

    sha = hashlib.sha1()
    for p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align in phdrs:
        sha.update(struct.pack('>II', p_type, p_flags))
        if p_type == 1 and p_memsz:
            sha.update(struct.pack('>QQ', p_vaddr, p_memsz))
            sha.update(out[p_offset:p_offset + p_filesz])
        print(f'  phdr type=0x{p_type:08x} flags=0x{p_flags:x} off=0x{p_offset:x} vaddr=0x{p_vaddr:x} filesz=0x{p_filesz:x} memsz=0x{p_memsz:x}')
    print('PPU-' + sha.hexdigest())
    return 'PPU-' + sha.hexdigest()


if __name__ == '__main__':
    main(*sys.argv[1:4])
