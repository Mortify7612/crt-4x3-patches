#!/usr/bin/env python3
"""Write a patched EBOOT.BIN into a PS3 ISO in place, for games that have no update installed.

usage: iso_put_eboot.py GAME.iso EBOOT_4x3.BIN

Finds PS3_GAME/USRDIR/EBOOT.BIN in the ISO, checks the new file is the same size, and overwrites
only the bytes that differ. Work on a copy of your ISO. Run it again with the original EBOOT.BIN
to undo.
"""
import struct, sys

SECTOR = 2048


def records(data):
    """(name, extent, size) for each entry of an ISO9660 directory."""
    i = 0
    while i < len(data):
        ln = data[i]
        if ln == 0:
            i = (i // SECTOR + 1) * SECTOR  # records don't cross sectors
            continue
        ext, size = struct.unpack_from('<I', data, i + 2)[0], struct.unpack_from('<I', data, i + 10)[0]
        nlen = data[i + 32]
        yield data[i + 33:i + 33 + nlen].decode('latin-1').split(';')[0], ext, size
        i += ln


def find(iso, path):
    """(byte offset, size) of a file in the ISO."""
    iso.seek(16 * SECTOR)
    pvd = iso.read(SECTOR)
    assert pvd[1:6] == b'CD001', 'not an ISO9660 image'
    ext, size = struct.unpack_from('<I', pvd, 158)[0], struct.unpack_from('<I', pvd, 166)[0]
    for part in path.split('/'):
        iso.seek(ext * SECTOR)
        for name, e, s in records(iso.read(size)):
            if name.upper() == part.upper():
                ext, size = e, s
                break
        else:
            sys.exit(f'{path}: {part} not found in the ISO')
    return ext * SECTOR, size


def main(iso_path, eboot_path):
    new = open(eboot_path, 'rb').read()
    with open(iso_path, 'r+b') as iso:
        off, size = find(iso, 'PS3_GAME/USRDIR/EBOOT.BIN')
        if size != len(new):
            sys.exit(f'size mismatch: ISO EBOOT is {size} bytes, {eboot_path} is {len(new)}')
        iso.seek(off)
        old = iso.read(size)
        runs, i = 0, 0
        while i < size:
            if old[i] != new[i]:
                j = i
                while j < size and old[j] != new[j]:
                    j += 1
                iso.seek(off + i)
                iso.write(new[i:j])
                runs += 1
                i = j
            else:
                i += 1
        iso.seek(off)
        assert iso.read(size) == new, 'read-back mismatch'
    print(f'EBOOT at ISO byte {off}: {runs} changed runs written, verified')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:3])
