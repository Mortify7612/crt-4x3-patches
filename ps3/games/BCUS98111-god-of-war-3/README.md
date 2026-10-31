# God of War III (BCUS98111, USA)

**Status:** working in RPCS3 and on a real CFW PS3.

| Version | Where it comes from | PPU hash |
|---|---|---|
| 1.03 | game update | `PPU-19724fde16a5b111b7b4d2a065f5dccaf8e01962` |

Only update 1.03 is supported. The console and RPCS3 run the update's EBOOT
(`/dev_hdd0/game/BCUS98111/USRDIR/EBOOT.BIN`), not the disc's.

## Parts

- **Part 1: No letterbox.** On a 4:3 TV the game draws the whole frame, menus included, into a
  16:9 band. This leaves the letterbox off, so the frame fills the screen.
- **Part 2: 4:3 camera.** The game renders its 3D at 4:3 instead of 16:9, so shapes are correct.

Use both together. Each part changes one instruction.

## RPCS3 settings

Besides aspect 4:3 and 720x480, turn on **Stretch To Display Area** for this game. Without it RPCS3
shows the full 4:3 frame too narrow, with black bars at the sides. A real PS3 doesn't need this.

## Known issues

- Pre-rendered videos still play letterboxed.
