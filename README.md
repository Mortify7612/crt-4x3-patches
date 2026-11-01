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
| PS3 | [Dante's Inferno](ps3/games/BLUS30405-dantes-inferno/) | BLUS30405 | 1.04 | RPCS3 ✔ | CFW PS3 ✔ |
| PS3 | [Asura's Wrath](ps3/games/BLUS30721-asuras-wrath/) | BLUS30721 | 1.02 | RPCS3 ✔ | CFW PS3 ✔ |
| PS3 | [The Last of Us](ps3/games/BCUS98174-the-last-of-us/) | BCUS98174 | 1.11 | RPCS3 ✔ | CFW PS3 ✔ |
| PS3 | [Killzone 2](ps3/games/BCUS98116-killzone-2/) | BCUS98116 | 1.29 | RPCS3 ✔ | CFW PS3 ✔ |

### Already 4:3, no patch needed

These output true full-screen 4:3 on their own when the console (or RPCS3) is set to a 4:3 TV.
Checked on a CRT; cutscenes may keep the game's own cinematic bars.

| Platform | Game | ID |
|---|---|---|
| PS3 | inFamous | BCUS98119 |
| PS3 | inFamous 2 | BCUS98125 |
| PS3 | MotorStorm | BCUS98137 |
| PS3 | Ratchet & Clank Future: A Crack in Time | BCUS98124 |

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
