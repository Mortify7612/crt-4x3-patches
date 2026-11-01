# Killzone 2 (BCUS98116, USA)

**Status:** working in RPCS3 and on a real CFW PS3.

| Version | Where it comes from | PPU hash |
|---|---|---|
| 1.29 | game update (latest) | `PPU-3a4e272eff128f7fa40bf722961a0c6de81bfc5a` |

Only update 1.29 is supported. Install it through the console's own update prompt; the console and
RPCS3 then run the update's EBOOT (`/dev_hdd0/game/BCUS98116/USRDIR/EBOOT.BIN`), not the disc's.

## Parts

- **Part 1: Full-screen picture.** On a 4:3 TV the game letterboxes the whole frame, menus and HUD
  included. This makes its video setup take the 16:9-TV path instead, so the frame fills the screen.
- **Part 2: 4:3 aspect.** Sets the game's 16:9 aspect values to 4:3, so the 3D isn't stretched by
  Part 1 and shapes are correct.

Use both together.

## Tips

- The heavy aiming the game is known for can be eased in **Options → Controls → High Precision**
  (added by a game update), with the look sensitivity raised a little.

## Known issues

- Menus and HUD use the game's 16:9 layout squeezed to 4:3, so they may look a little narrow.
- Pre-rendered videos haven't been checked.
