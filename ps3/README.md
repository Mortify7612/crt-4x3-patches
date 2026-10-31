# PS3

Every game folder has a `patch.yml` in RPCS3's patch format. The same file drives both setups.

## RPCS3

1. RPCS3 → **Manage → Game Patches**, drag `patch.yml` into the window to import it.
2. Tick every part listed for the game. Parts are separate so you can switch one off to compare.
3. Game's custom configuration → GPU: **Aspect ratio 4:3** and **Resolution 720x480**.
   720p is 16:9-only in RPCS3, as on real hardware. 4:3 with 720p leaves the game no valid
   video mode, and some games crash at boot.

## Real PS3 (custom firmware)

Needs a PS3 on CFW that skips the EBOOT signature check (tested on Evilnat 4.93 Cobra).

1. **Find the EBOOT the console runs.** If a game update is installed, it's
   `/dev_hdd0/game/<ID>/USRDIR/EBOOT.BIN`, not the one on the disc or ISO. Check the game's
   README for supported versions; other versions are refused.
2. **Copy that EBOOT to your PC** (webMAN FTP works) and keep a backup.
3. **Build the patched EBOOT:**
   ```
   pip install cryptography
   python3 tools/patch_eboot.py EBOOT.BIN games/<game>/patch.yml EBOOT_4x3.BIN
   ```
   The first run downloads RPCS3's `key_vault.cpp`/`key_vault.h` from its GitHub. Pass
   `--keys path/to/rpcs3/rpcs3/Crypto` to use a local RPCS3 checkout instead.
   The tool decrypts the EBOOT, applies the patch, re-encrypts it with the original keys, then
   decrypts the result again to check it. The file stays the same size; about 100 bytes change.
4. **Install it:** rename the console's file to `EBOOT.BIN.orig` and upload yours as `EBOOT.BIN`.
   If there's no update and the game runs from an ISO, write the patched EBOOT into a copy of the
   ISO instead, then put that ISO on the console:
   ```
   python3 tools/iso_put_eboot.py GAME.iso EBOOT_4x3.BIN
   ```
   It only overwrites the bytes that differ and checks the result. Run it with the original
   `EBOOT.BIN` to undo.
5. **Set the PS3 to a 4:3 TV:** Settings → Display Settings → TV type **4:3**, **480p** or 480i.
   The patches assume the game sees a 4:3 display.

To undo, rename `EBOOT.BIN.orig` back to `EBOOT.BIN`.

## Tools

| Tool | What it does |
|---|---|
| `patch_eboot.py` | One step: EBOOT + patch.yml → patched EBOOT, verified |
| `iso_put_eboot.py` | Writes a patched EBOOT into an ISO in place (games without an update) |
| `unself.py` | Decrypt a disc or free-license NPDRM (update) EBOOT to an ELF; prints its RPCS3 `PPU-` hash |
| `reself.py` | Re-encrypt a patched ELF into the original EBOOT's layout |
| `selfinfo.py` | Dump a SELF's headers, sections and key usage |
| `keys.py` | Find or download RPCS3's key files |

`reself.py` handles EBOOTs whose code is stored uncompressed (most disc and update EBOOTs;
`selfinfo.py` shows `comp=1`). The header's ECDSA signature can't be redone, which is why CFW is needed.
