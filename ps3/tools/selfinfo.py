"""Dump SELF layout: segment ext headers, metadata sections and key usage (reuses unself.py helpers)."""
import struct, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unself import decrypt_meta_info, aes_ctr, read_vault

def parse(vault, path):
    f = open(path, 'rb').read()
    magic, hver, flags, stype, meta, hsize, esize = struct.unpack_from('>IIHHIQQ', f, 0)
    ext = struct.unpack_from('>10Q', f, 0x20)
    info = decrypt_meta_info(read_vault(vault), f)
    mkey, miv = info[0:16], info[32:48]
    mh = aes_ctr(mkey, miv, f[0x20 + meta + 0x40:hsize])
    sig_len, _, nsec, nkeys, opt, _, _ = struct.unpack_from('>QIIIIII', mh, 0)
    secs = [struct.unpack_from('>QQIIIIIIII', mh, 0x20 + i * 0x30) for i in range(nsec)]
    keys = mh[0x20 + nsec * 0x30:0x20 + nsec * 0x30 + nkeys * 0x10]
    return dict(f=f, flags=flags, meta=meta, hsize=hsize, esize=esize, ext=ext, mkey=mkey, miv=miv,
                info=info, mh=mh, sig_len=sig_len, nsec=nsec, nkeys=nkeys, opt=opt, secs=secs, keys=keys)

if __name__ == '__main__':
    d = parse(sys.argv[1], sys.argv[2])
    print(f"flags(rev)={d['flags']:#x} meta={d['meta']:#x} hsize={d['hsize']:#x} esize={d['esize']:#x} filesize={len(d['f']):#x}")
    names = 'ver prog_id ehdr phdr shdr seg_ext ver_hdr supp supp_size pad'.split()
    print(' '.join(f'{n}={v:#x}' for n, v in zip(names, d['ext'])))
    print(f"sig_input_len={d['sig_len']:#x} nsec={d['nsec']} nkeys={d['nkeys']} opt_hdr_size={d['opt']:#x}")
    for i, s in enumerate(d['secs']):
        print(f'  sec{i}: off={s[0]:#x} size={s[1]:#x} type={s[2]} idx={s[3]} hashed={s[4]} sha1_idx={s[5]} enc={s[6]} key={s[7]} iv={s[8]} comp={s[9]}')
    se = d['ext'][5]
    nph = struct.unpack_from('>H', d['f'], d['ext'][2] + 0x38)[0]
    for i in range(nph):
        print('  segext', i, ' '.join(f'{v:#x}' for v in struct.unpack_from('>QQIIII', d['f'], se + i * 0x20)))
    # supplemental / control info headers
    a, end = d['ext'][7], d['ext'][7] + d['ext'][8]
    while a < end:
        t, sz, nxt = struct.unpack_from('>IIQ', d['f'], a)
        print(f'  supp type={t} size={sz:#x} next={nxt}  {d["f"][a+16:a+min(sz,0x40)].hex()}')
        a += sz
        if not nxt: break
