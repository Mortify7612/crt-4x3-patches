#!/usr/bin/env python3
"""Rebuild a retail disc or free-license NPDRM SELF with patched code: same layout/keys, re-encrypted segment 0, fixed section HMAC.

usage: reself.py KEYS ORIG_EBOOT.BIN PATCHED.elf OUT_EBOOT.BIN
PATCHED.elf must be the unself.py output with patches applied (only PT_LOAD segment contents differ).
The ECDSA header signature is left as-is (invalid after the change) — needs a CFW that skips that check.
"""
import hashlib, hmac, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from selfinfo import parse
from unself import aes_ctr


def main(vault, orig_path, patched_elf, out_path):
    d = parse(vault, orig_path)
    f = bytearray(d['f'])
    elf = open(patched_elf, 'rb').read()
    e_phoff, = struct.unpack_from('>Q', elf, 0x20)
    phdrs = [struct.unpack_from('>IIQQQQQQ', elf, e_phoff + i * 0x38) for i in range(struct.unpack_from('>H', elf, 0x38)[0])]
    keys = bytearray(d['keys'])
    k = lambda i, n=1: bytes(keys[i * 16:(i + n) * 16])

    changed = []
    for n, (off, size, typ, pidx, hashed, sha_idx, enc, kidx, ividx, comp) in enumerate(d['secs']):
        if typ != 2 or size == 0:
            continue
        assert enc == 3 and comp == 1 and hashed == 2, f'sec{n}: unsupported enc={enc} comp={comp} hashed={hashed}'
        plain = aes_ctr(k(kidx), k(ividx), bytes(f[off:off + size]))
        hkey = k(sha_idx + 2, 4)
        stored = k(sha_idx, 2)[:20]
        assert hmac.new(hkey, plain, hashlib.sha1).digest() == stored, f'sec{n}: HMAC method mismatch on original'
        p = phdrs[pidx]
        new = elf[p[2]:p[2] + p[5]]
        assert len(new) == size
        if new == plain:
            continue
        diff = sum(1 for i in range(0, size, 4) if new[i:i + 4] != plain[i:i + 4])
        changed.append((n, diff))
        f[off:off + size] = aes_ctr(k(kidx), k(ividx), new)
        keys[sha_idx * 16:sha_idx * 16 + 20] = hmac.new(hkey, new, hashlib.sha1).digest()

    # Re-encrypt metadata section headers + keys (AES-CTR with the metadata key, which is unchanged).
    mh = bytearray(d['mh'])
    kstart = 0x20 + d['nsec'] * 0x30
    mh[kstart:kstart + len(keys)] = keys
    hdr_start = 0x20 + d['meta'] + 0x40
    f[hdr_start:d['hsize']] = aes_ctr(d['mkey'], d['miv'], bytes(mh))
    open(out_path, 'wb').write(f)
    print('sections re-encrypted (sec, changed words):', changed)


if __name__ == '__main__':
    main(*sys.argv[1:5])
