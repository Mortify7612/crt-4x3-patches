# Asura's Wrath (BLUS30721, USA)

**Status:** working in RPCS3 and on a real CFW PS3.

| Version | Where it comes from | PPU hash |
|---|---|---|
| 1.02 | game update (latest) | `PPU-83096111daff850cc92b637aec1780c4079e1c58` |

Only update 1.02 is supported. Install it through the console's own update prompt; the console and
RPCS3 then run the update's EBOOT (`/dev_hdd0/game/BLUS30721/USRDIR/EBOOT.BIN`), not the disc's.

## Parts

On SD TVs the game renders at 1280x720 and lets Sony's cellResc library scale the picture down. On
a 4:3 TV it asks cellResc to letterbox.

- **Part 1: Full-screen output.** Asks cellResc to fill the screen instead, as the game already does
  on a 16:9 TV.
- **Part 2: 4:3 render size.** Renders at 960x720 instead of 1280x720 on SD TVs, so the engine sets
  up a 4:3 view itself and shapes are correct. Still more horizontal detail than a 480p TV shows.

Use both together. Each part changes one instruction. They only affect SD (480/576) output.

## Known issues

- Cutscenes keep the game's own thin cinematic bars.
