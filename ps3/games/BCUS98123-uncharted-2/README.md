# Uncharted 2: Among Thieves (BCUS98123, USA)

**Status:** working in RPCS3 and on a real CFW PS3.

| Version | Where it comes from | PPU hash |
|---|---|---|
| 1.00 | disc / ISO | `PPU-9fe364d48b610e4b0a1c41d526bec9b1b2039c07` |
| 1.02 | game update | `PPU-c319a223b0d8d1fb319b87db2308e61d35e9cd33` |
| 1.09 | game update (latest) | `PPU-a3a5789c12711291dfe16a7d5d81c906d2b4c0c2` |

If an update is installed, the console and RPCS3 run its EBOOT, not the disc's.

## Parts

- **Part 1: Full-height 3D.** The game normally squeezes the 3D picture into a 16:9 letterbox when
  the display is 4:3. This removes only the 3D squeeze; menus and HUD keep the game's own 4:3 layout.
- **Part 2: 4:3 camera.** Rebuilds the gameplay camera for a 4:3 view, so shapes are correct
  instead of stretched. It changes the camera where its field of view and aspect are set, not the
  shared projection code, so shadow and light cameras stay untouched.

Use both together.

## Known issues

- Pre-rendered videos still play squeezed sideways.
- Cutscenes haven't been checked closely.
- The HUD sits slightly in from the screen edges, where the game places it on a 4:3 TV.
