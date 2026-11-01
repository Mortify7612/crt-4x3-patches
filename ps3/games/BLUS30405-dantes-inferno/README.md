# Dante's Inferno (BLUS30405, USA)

**Status:** working in RPCS3 and on a real CFW PS3.

| Version | Where it comes from | PPU hash |
|---|---|---|
| 1.04 | game update (latest) | `PPU-539a6d42763b06228b136fa70f42070b34d30529` |

Only update 1.04 is supported. Install it through the console's own update prompt; the console and
RPCS3 then run the update's EBOOT (`/dev_hdd0/game/BLUS30405/USRDIR/EBOOT.BIN`), not the disc's.

## Parts

- **Part 1: Full-screen picture.** On a 4:3 TV the game letterboxes the whole frame, menus and HUD
  included. This makes it use its 16:9-TV output path instead, so the frame fills the screen.
- **Part 2: 4:3 aspect.** Sets the game's three 16:9 aspect values to 4:3, so the 3D isn't
  stretched sideways by Part 1. The addresses come from boma's "Aspect Ratio" patch in RPCS3's
  patch database; that patch alone doesn't remove the letterbox.

Use both together. Don't enable boma's "Aspect Ratio" patch at the same time.

## Known issues

- Menus and HUD use the game's 16:9 layout squeezed to 4:3, so they may look a little narrow. Not
  checked closely, nor are pre-rendered videos.
