# THE DRYING — procedural asset pipeline

Every model is generated from Python. There are no hand-sculpted binaries in
the source of truth: change a number, run `build.py`, get the whole fleet back.
That matters for a game whose silhouettes are still moving.

```bash
pip install bpy                 # Blender 5.0 as a Python module, needs py3.11
python3 build.py                # all assets -> assets/glb + assets/blend
python3 build.py tank_combine   # just one
python3 contact.py /tmp/sheet   # turntable renders for review
```

## Layout

```
blender/
├── lib/kit.py        loft, tube, plate, crimped_disc, rock, rivets, markers, export
├── lib/palette.py    faction materials (art bible section 5) -- final, not placeholder
├── lib/render.py     Cycles CPU review renders, lighting matched to the reference
├── assets/*.py       one module per asset, each exposing build()
├── build.py          builds + exports everything
└── contact.py        renders every asset from a matched 3/4 angle
assets/glb/           Godot imports these
assets/blend/         open in the Blender GUI to hand-edit
assets/reference/     contact sheet
```

## Contracts

**Axes** — `+Y` forward (bow / nose / muzzle), `+Z` up, `+X` starboard. glTF
exports with `export_yup=True`, so this lands correctly in Godot.

**Scale** — game scale, never miniature scale (design doc 7.3). A hauler is 30
units long, not 4 centimetres. Modelling at true miniature size makes Godot's
default gravity and collision margins produce jitter and broken buoyancy;
miniature-ness is sold by the renderer, not the transform.

**Origin** — at the *waterline* for anything that floats, on the *ground plane*
for anything that drives. Buoyancy probes sample in object space.

**Markers** — empties export as plain glTF nodes, so they arrive in Godot as
`Node3D` children you can look up by name:

| Prefix | Meaning |
|---|---|
| `mount_*` | hardpoints, turret rings, deck bays, launch rails |
| `fx_*` | VFX emitters — wake, bow wave, funnel smoke, muzzle, spray |
| `probe_*` | buoyancy sample points (design doc 8.1.4) |
| `cam_*` | camera anchors for the possession system |
| `wheel_*` | wheel/roadwheel positions for suspension |

Parts that must animate independently are **separate objects**, never joined:
`tank_combine_turret` rotates about Z, `fighter_combine_prop` spins about Y.

## Style

Faceted low-poly, flat shading, flat-colour untextured materials, muted dusty
palette — locked against the reference frame (art bible section 2). `kit.flat()`
is applied to every asset; `kit.smooth()` exists but is deliberately unused.
Low segment counts (6–14) are a style choice, not a budget compromise.

## Current pass

| Asset | Tris | Notes |
|---|---:|---|
| `hauler_combine` | 3108 | Hero unit. Crushed-can hull, crown-cap tower, razor ram |
| `hauler_reedfolk` | 1424 | Faction mirror. Pod hull, leaf deck, silk rigging, glow seam |
| `tank_combine` | 2084 | Bottle-cap hull, watch-gear road wheels, nail gun. Separate turret |
| `props_kit` | 2036 | 9 found objects: cap, staple, match, filter, screw, clip, 3 pebbles |
| `bike_combine` | 1378 | Spool wheels, spring spine, matchstick forks |
| `fighter_combine` | 496 | Membrane wing, paperclip frame, separate prop |

**Total ~10.5k tris for the fleet** — comfortably inside the Steam Deck budget
in the design doc's 8.3, with headroom for crews and damage states.

## Known nits for the next pass

- Bike fairing reads as a flat slab from above; wants a curve or a cut-down.
- Rivets are real geometry. Fine for blockout and concept renders, but bake
  them to a normal map before shipping.
- No UVs yet. Flat-colour materials don't need them, but wear/decal passes will.
- No LODs, no collision meshes, no damage states.
- Combine bomber, submarine, engineer and artillery are still unbuilt
  (design doc section 6).
