# The Last of Us (BCUS98174, USA)

**Status:** working in RPCS3 and on a real CFW PS3.

| Version | Where it comes from | PPU hash |
|---|---|---|
| 1.11 | game update (latest) | `PPU-120fb71f7352d62521c639b0e99f960018c10a56` |

Only update 1.11 is supported. Install it through the console's own update prompt; the console and
RPCS3 then run the update's EBOOT (`/dev_hdd0/game/BCUS98174/USRDIR/EBOOT.BIN`), not the disc's.

Same engine as [Uncharted 3](../BCUS98233-uncharted-3/); the patch is ported from it.

## Parts

- **Part 1: Full-height 3D.** On a 4:3 TV the game squeezes the 3D picture into a 16:9 band during
  post-processing. This removes only that squeeze; menus and HUD keep the game's own 4:3 layout.
- **Part 2: 4:3 camera.** Every camera set up for 16:9 is switched to 4:3 where the game builds its
  projection, keeping the 16:9 view's height and trimming its sides, so proportions are correct.

Use both together.

Uncharted 3's camera keeps the 16:9 width and adds view above and below instead. In The Last of Us
that froze the game at the menu in RPCS3, so this version trims the sides.

## RPCS3 settings

Besides aspect 4:3 and 720x480 and RPCS3's recommended settings for the game, it froze on loading
screens here (with or without this patch) until these were on:

- RPCS3 patches: **Enable GPU Lighting**, **Disable in-built MLAA**, **Bug Fix: Infected Severed Head Crash**
- Strict Rendering Mode on, RSX FIFO accuracy "Ordered & Atomic", Driver Wake-Up Delay 600,
  Shader Mode "Legacy Recompiler" (from [RPCS3 issue #18828](https://github.com/RPCS3/rpcs3/issues/18828))

Not all of these may be needed. A real PS3 needs none of them.

## Known issues

- The pause menu darkens only a 16:9 band (the game's own 4:3 menu layout).
- Pre-rendered videos still play letterboxed.
