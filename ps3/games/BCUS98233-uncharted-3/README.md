# Uncharted 3: Drake's Deception (BCUS98233, USA)

**Status:** working in RPCS3 and on a real CFW PS3.

| Version | Where it comes from | PPU hash |
|---|---|---|
| 1.00 | disc / ISO | `PPU-49c96996b6f3c0b32422375978c41e0c7ed95183` |
| 1.19 | game update (latest) | `PPU-02a88c3c6cd415b0bb81f1606bc743835881a4ba` |

If update 1.19 is installed, the console and RPCS3 run its EBOOT, not the disc's. With no update
installed, the console runs the EBOOT inside the disc or ISO: build the patched EBOOT, then put it
back into a copy of your ISO with `tools/iso_put_eboot.py` (see the [PS3 README](../../README.md)).

## Parts

- **Part 1: Full-height 3D.** On a 4:3 TV the game squeezes the 3D picture into a 16:9 band during
  post-processing. This removes only that squeeze; menus and HUD keep the game's own 4:3 layout.
- **Part 2: 4:3 camera.** Every camera set up for 16:9 is switched to 4:3 where the game builds its
  projection. You see the same width as on a 16:9 TV, plus more above and below, with correct
  proportions.

Use both together.

## RPCS3 settings

Besides aspect 4:3 and 720x480, keep RPCS3's recommended settings for this game (Accurate RSX
reservation access, Multithreaded RSX, Write Color Buffers and so on, from its wiki page). Without
them the game can freeze shortly after loading.

## Known issues

- Pre-rendered videos still play squeezed.
- RPCS3 sometimes draws bright white blobs where light glows should be. This happens without the
  patch too.
