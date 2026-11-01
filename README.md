# crt-4x3-patches

Patches that make 16:9-era console games render **true full-screen 4:3**, for playing on a CRT:
no letterbox, no stretching, correct proportions, with the 3D camera rebuilt for a 4:3 view.

Each patch is made per game and per version, and tested on an emulator and, where possible,
on real hardware.

**This repo contains no game code, no executables and no keys.** It only has the patches (the
changed instructions) and tools that apply them to a copy of the game you dump yourself.

## Games

| Platform | Game | ID | Versions | Emulator | Real hardware |
|---|---|---|---|---|---|
| PS3 | [Uncharted 2: Among Thieves](ps3/games/BCUS98123-uncharted-2/) | BCUS98123 | 1.00, 1.02, 1.09 | RPCS3 ✔ | CFW PS3 ✔ |
| PS3 | [Uncharted 3: Drake's Deception](ps3/games/BCUS98233-uncharted-3/) | BCUS98233 | 1.00, 1.19 | RPCS3 ✔ | CFW PS3 ✔ |
| PS3 | [God of War III](ps3/games/BCUS98111-god-of-war-3/) | BCUS98111 | 1.03 | RPCS3 ✔ | CFW PS3 ✔ |

## Platforms

- **[PS3](ps3/)**: RPCS3 patches, plus `patch_eboot.py` to build a patched `EBOOT.BIN` for a CFW PS3.
- **Xbox 360**: planned (Xenia patches, and patched XEX files for modded consoles).

## Layout

```
<platform>/
  README.md          how to use patches on that platform
  tools/             tools that apply patches to your own game files
  games/<ID>-<name>/
    README.md        status, supported versions, what changes, known issues
    patch.*          the patch, in the emulator's own format
```

## Licence

MIT, see [LICENSE](LICENSE). Game names and trademarks belong to their owners.
