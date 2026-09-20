# THE DRYING — mock-ups

## Pass 2 — the wetland  (`assets/mockups_wetland/`)

The real setting: a big, deep pool sunk in marsh, walled by a standing forest of sedge and
cattail, skinned with lily pads and algae. Eight views.

| Shot | What it shows |
|---|---|
| `reed_channel` | **The signature image.** The Ark threading a pass between two reed stands — a green canyon with cattails overhead. This is the game |
| `wetland_dawn` | The open pool at first light, lily pads, reed wall as coastline |
| `through_the_reeds` | Hidden in the margin, watching a hull cross the water through a screen of blades. Foreground goes soft |
| `marsh_standoff` | Both haulers, one light. The Reedfolk pod looks like it *grew here*; the Combine can looks like it washed in |
| `bank_assault` | Armour working a mossy bank under the reed line — the Act III shore war |
| `the_heron` | The Grey Judge wades in. Legs like towers, a shadow across the pool. Cannot be fought |
| `autumn_drying` | Late season. Ochre reeds, water pulled back, the Ark aground in silt |
| `bridge_through_reeds` | From the Ark's bridge, reed wall to starboard, contact fine on the bow |

### On the foliage clock
`autumn_drying` and the green shots are the same scene at different points on the clock. The reed
wall goes green → gold → ochre → dead straw as the water falls, so the act structure is legible
from any camera angle without a single UI element. This is the strongest thing the wetland
setting bought us, and it is already implemented (`autumn` parameter in `scene.wetland`).

---

## Pass 1 — the parking lot  (`assets/mockups/`)  — superseded

Kept for the record. Thirteen views of the earlier tarmac setting, including the four-panel
`clockstrip` that demonstrates waterline retreat and tide-mark banding. **The clock strip's
mechanic still holds** — only its dressing changed — and it remains the clearest single
demonstration of the core idea. Worth re-shooting in the marsh.

---

## What is real here, and what is faked

**Real:**
- Every vehicle is the shipped glTF asset at true game scale.
- Shoreline banding and plant placement are both computed from `water_level`: plants root only
  where the water is shallower than ~5 units, so the reed belt genuinely advances as the pool
  retreats.
- Foliage colour is driven by one `autumn` parameter, matching the act structure.

**Faked — do not read these as solved:**
- **Water is a stand-in.** A faceted sum-of-sines surface, not the Gerstner + interactive
  ripple-buffer system in design doc §8.1. Wakes are placed geometry. **The hero water feature is
  not in these pictures because it is not built.** Treat M1 as unproven.
- **No crews.** No finger-tall men anywhere. This is still the biggest gap — crews would change
  the sense of scale in every frame.
- **No VFX** (spray, smoke, muzzle flash, silt) and **no UI**, including on the bridge view.
- The heron is two legs and a shadow. There is no bird.
- Renders are Blender Cycles, not Godot. Colour will shift on the way across.

## Note on method
There is **no image-generation model available in this environment** — these are rendered in
Blender from the actual game assets. That has an upside (what you see is the real build, and it
cannot drift from it) and a real limit: these are previews, not painted concept art. If you want
diffusion-style key art, the art bible §11 shot list doubles as a prompt list to take elsewhere.

## Next
1. Crews.
2. Re-shoot the four-panel clock strip in the marsh, with the foliage turning.
3. Bomber and submarine (design doc §6) — the two biggest unbuilt roles.
4. Underwater: drowned leaf forest, silt, larvae. The submarine has no picture yet.
5. Act IV — the Return. The best moment in the game has no image.
