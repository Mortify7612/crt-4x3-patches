#!/usr/bin/env python3
"""Apply an RPCS3 patch file to your own EBOOT.BIN, producing a patched EBOOT.BIN for a CFW PS3.

usage: patch_eboot.py EBOOT.BIN PATCH.yml OUT_EBOOT.BIN [--skip PART ...] [--keys RPCS3_CRYPTO_DIR]

Decrypts the EBOOT, picks the patches in PATCH.yml whose PPU hash matches it, applies every
be32 write, re-encrypts with the original keys, then decrypts the result again to check it.
--skip leaves out every part whose name contains PART (case-insensitive); use it when a game
offers alternative parts. Parts that write the same address are refused unless one is skipped.
The header signature is left invalid, so the console needs a CFW that skips that check.
"""
import argparse, os, re, struct, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reself, unself
from keys import keys_dir


def patch_words(yml_text, ppu_hash):
    """(part name, [(addr, value)]) for every patch listed under ppu_hash."""
    block = re.search(r'^' + re.escape(ppu_hash) + r':\s*\n(.*?)(?=^\S|\Z)', yml_text, re.M | re.S)
    if not block:
        return []
    parts = []
    for name, body in re.findall(r'^  "([^"]+)":\s*\n(.*?)(?=^  "|\Z)', block.group(1), re.M | re.S):
        words = []
        for typ, addr, val in re.findall(r'-\s*\[\s*(\w+)\s*,\s*(0x[0-9A-Fa-f]+)\s*,\s*(0x[0-9A-Fa-f]+)\s*\]', body):
            assert typ == 'be32', f'{name}: patch type {typ} is not supported (be32 only)'
            words.append((int(addr, 16), int(val, 16)))
        parts.append((name, words))
    return parts


def file_offset(elf, addr):
    e_phoff, = struct.unpack_from('>Q', elf, 0x20)
    e_phnum, = struct.unpack_from('>H', elf, 0x38)
    for i in range(e_phnum):
        p_type, _, off, vaddr, _, filesz, _, _ = struct.unpack_from('>IIQQQQQQ', elf, e_phoff + i * 0x38)
        if p_type == 1 and vaddr <= addr and addr + 4 <= vaddr + filesz:
            return off + addr - vaddr
    raise AssertionError(f'address {addr:#x} is not in a loaded segment')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('eboot')
    ap.add_argument('patch_yml')
    ap.add_argument('out')
    ap.add_argument('--skip', action='append', default=[], metavar='PART',
                    help='leave out parts whose name contains PART (repeatable)')
    ap.add_argument('--keys', help="RPCS3's rpcs3/Crypto directory (default: download from RPCS3 GitHub)")
    a = ap.parse_args()
    keys = keys_dir(a.keys)

    with tempfile.TemporaryDirectory() as tmp:
        elf_path, patched_path, check_path = (os.path.join(tmp, n) for n in ('orig.elf', 'patched.elf', 'check.elf'))
        ppu_hash = unself.main(keys, a.eboot, elf_path)
        parts = patch_words(open(a.patch_yml).read(), ppu_hash)
        if not parts:
            sys.exit(f'{a.patch_yml} has no patches for {ppu_hash}: wrong game or version')
        for name, _ in parts:
            if any(s.lower() in name.lower() for s in a.skip):
                print(f'skipping "{name}"')
        parts = [(n, w) for n, w in parts if not any(s.lower() in n.lower() for s in a.skip)]
        owner = {}
        for name, words in parts:
            for addr, _ in words:
                if addr in owner and owner[addr] != name:
                    sys.exit(f'"{owner[addr]}" and "{name}" both change {addr:#x}: they are alternatives, '
                             f'leave one out with --skip')
                owner[addr] = name

        elf = bytearray(open(elf_path, 'rb').read())
        for name, words in parts:
            print(f'applying "{name}" ({len(words)} words)')
            for addr, val in words:
                struct.pack_into('>I', elf, file_offset(elf, addr), val)
        open(patched_path, 'wb').write(elf)

        reself.main(keys, a.eboot, patched_path, a.out)
        unself.main(keys, a.out, check_path)
        assert open(check_path, 'rb').read() == bytes(elf), 'patched EBOOT does not decrypt back to the patched code'
    print(f'OK: wrote {a.out} (verified by decrypting it again)')


if __name__ == '__main__':
    main()
