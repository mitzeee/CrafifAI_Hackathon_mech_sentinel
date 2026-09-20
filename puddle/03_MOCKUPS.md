# THE DRYING — mock-ups, pass 1

Thirteen framed views of the game. Every one is dressed with the **shipped
assets** (`assets/glb/`) in a scene built from the design doc's own numbers —
so these are previews of the actual build, not a parallel concept-art track
that can quietly drift from it.

Regenerate any shot with `cd blender && python3 mockups.py <outdir> <shot>`.

---

## The clock — `clockstrip.jpg`

**The most important image here.** One locked camera, one fixed scatter of
found objects, four water levels. The shoreline is *computed* from
`water_level`, not painted: every metre the puddle gives up exposes another
tide terrace and strands another prop.

| Panel | Water | Waterline radius | What changed |
|---|---|---|---|
| `clock_0600` | 1.00 | ~98 | Open sea. Debris floating at the margin |
| `clock_1000` | 0.70 | ~73 | First tide band. Shoals breaking surface |
| `clock_1400` | 0.30 | ~47 | Props fully beached. Terraces clearly stepped |
| `clock_1800` | 0.10 | ~27 | A dark remnant pool. Everything exposed |

If one image has to sell the pitch, it's this one.

---

## Acts

| Shot | What it shows |
|---|---|
| `act1_flood` | 06:00, water 1.00. The Ark stands out into open water. Naval, wide, cold dawn light. Found objects on the far shore carry the scale |
| `act2_shallows` | 10:00, water 0.55. Combined arms — hauler under way, fighter crossing as escort, tank working a shoal. Peak complexity |
| `act3_drying` | 14:00, water 0.18. The Ark **aground**, heeled, fortress-not-ship, ringed by the tide terraces it left coming down. Hot, bleached, dusty |

## Theaters

| Shot | What it shows |
|---|---|
| `theater5_reef` | Cigarette Reef. Cover-dense debris field, tank country, hopeless for aircraft |
| `theater6_lens` | The Lens. Sunlight focused through a discarded bottle into a moving column of lethal heat, scorching the water where it lands |
| `theater8_throat` | The Throat. The storm grate — dark, vertical, cathedral-scale, light falling in shafts between bars |

## Scenarios

| Shot | What it shows |
|---|---|
| `rolling_god` | A car crosses the lot. A wall of water on top of the hull, the Ark heeled and bow-on. Neither tribe controls this |
| `faction_standoff` | The design-language page: both haulers, one light. Combine = straight lines and smoke; Reedfolk = curves and glow |
| `bridge_view` | First person from the Ark's bridge over the cargo deck and launch rail, contact ahead. The hub seat you always return to |

---

## What is real here, and what is faked

Being explicit, because mock-ups that oversell cost you a schedule later.

**Real — these are load-bearing and already work:**
- All vehicles are the shipped glTF assets at true game scale.
- The shoreline banding is genuinely driven by `water_level`. Changing one
  float moves the waterline, the terraces and the beached props.
- The basin profile, theater sizes and unit sizes are the design doc's numbers.
- Lighting follows the four time-of-day presets in the art bible's §4.3.

**Faked — do not read these as solved:**
- **Water is a stand-in.** A faceted sum-of-sines surface, not the Gerstner +
  interactive ripple-buffer system in design doc §8.1. The V wakes are *placed
  geometry*, not simulation. The hero feature — wakes that persist, interfere,
  reflect off shores and shove other boats — is not shown here because it isn't
  built. Treat M1 as unproven.
- **No VFX**: no smoke, spray, muzzle flash, steam, fire, or silt.
- **No crews.** No finger-tall men anywhere. That's a whole animation budget.
- **No UI.** Even `bridge_view` has no diegetic instruments yet.
- Renders are Blender Cycles, not Godot. The target look is achievable in
  Forward+, but colour and post will shift on the way across.

## What the next pass needs

1. Crews — even low-detail silhouettes change every shot's sense of scale.
2. The bomber and submarine (design doc §6), the two biggest unbuilt roles.
3. An underwater view. The submarine is the best surprise in the design and
   has no picture yet.
4. Diegetic HUD pass over `bridge_view` and a fighter cockpit.
5. Act IV — the Return. The 90-second flash flood has no image, and it's the
   best moment in the game.
