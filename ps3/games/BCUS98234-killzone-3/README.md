# Killzone 3 (BCUS98234, USA)

**Status:** working in RPCS3 and on a real CFW PS3.

| Version | Where it comes from | PPU hash |
|---|---|---|
| 1.14 | game update (latest) | `PPU-4836b8e74c47919f50b030ee6b47d96bc7305387` |

Only update 1.14 is supported. Install it through the console's own update prompt; the console and
RPCS3 then run the update's EBOOT (`/dev_hdd0/game/BCUS98234/USRDIR/EBOOT.BIN`), not the disc's.

## Parts

- **Part 1: Full-screen picture.** On a 4:3 TV the game letterboxes the whole frame, menus and HUD
  included. This makes its video setup take the 16:9-TV path instead, so the frame fills the screen.
- **Part 2: 4:3 aspect.** Sets the game's 16:9 display aspect to 4:3, so the 3D isn't stretched by
  Part 1 and shapes are correct.
- **Part 3: First-person layer.** The game keeps the vertical field of view and widens the
  horizontal one, so at 4:3 the first-person layer is drawn for a taller view than the screen and
  the red Helghast goggles overlay stops short of the top and bottom. This draws that layer (arms,
  weapon, goggles) 15% bigger, so the goggles reach the edges. Optional.

Use Parts 1 and 2 together; add Part 3 for the goggles. The tested PS3 EBOOT has all three.

## Known issues

- Menus and HUD use the game's 16:9 layout squeezed to 4:3, so they may look a little narrow.
- With Part 3, arms and weapon are 15% bigger all the time, not only while the goggles are on.
- Pre-rendered videos haven't been checked.
