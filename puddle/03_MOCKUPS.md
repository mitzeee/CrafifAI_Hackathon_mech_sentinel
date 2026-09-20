# BRACKWATER — mock-ups

## Pass 3 — the missions  (`assets/mockups_missions/`)

One image per mission archetype, because each vehicle is its own mission with its own verb
(design doc §6). Dressed with the shipped glTF assets.

| Shot | Mission | The verb |
|---|---|---|
| `m_supply_land` | **Land logistics** — truck + rickshaw on the bank track at dusk | Route, timing, not being seen. No guns |
| `m_cargo_water` | **Water logistics** — hauler running a reed pass, loaded and slow | Same job, no cover, nowhere to run |
| `m_recon_sub` | **Reconnaissance** — half-surfaced off the enemy slipway | Watch, count, come home. Firing ends the mission |
| `m_strike_bomber` | **Strategic strike** — bomber over the far bank, bay open, escort high | Hit what the enemy cannot move |
| `m_intercept_fighter` | **Air intercept** — breaking up their flight over open water | Defend a truck that is somewhere else |
| `m_armour_push` | **Ground action** — tank and bike taking bank | Take and hold, so the convoys run |
| `m_rain_run` | **Weather** — a hull running in a downpour | Rain hides a convoy and grounds the aircraft |

**Half of these have no gun.** That is the design, not an omission — logistics and recon are
stealth problems, and the quiet/loud split in §6 is what keeps eight missions from collapsing
into one shooter with eight skins.

`m_rain_run` is the weather argument made visually: the pool does not dry up, so seasons and
weather are there for texture and tactics — rain collapses visibility, which is exactly what a
smuggler wants and exactly what grounds an air force.

---

## Pass 2 — the wetland  (`assets/mockups_wetland/`)

Eight views establishing the setting: the open pool, `reed_channel` (a hull threading a green
canyon — still the signature image), the marsh standoff, a bank assault, the heron macro event,
late-season colour, and a bridge view.

## Pass 1 — the parking lot  (`assets/mockups/`) — superseded
Kept for the record only. Wrong setting, and built around the retired evaporation clock.

---

## What is real here, and what is faked

**Real:** every vehicle is the shipped glTF at true game scale; flora places itself by height
above the waterline so the reed belt is computed, not painted; foliage colour runs off one
`autumn` parameter matching the seasonal reed cycle; the supply track is a real cleared corridor
through the reed belt.

**Faked — do not read these as solved:**
- **Water is a stand-in.** A faceted sum-of-sines surface, not the Gerstner + interactive
  ripple-buffer system in §8.1. Wakes are placed geometry. **The hero water feature is not in
  these pictures because it is not built.** Treat M1 as unproven.
- **No crews.** Still the biggest gap — finger-tall men would change the scale read in every frame.
- **No UI**, no muzzle flash, no smoke, no spray, no silt.
- The heron is two legs and a shadow. There is no bird.
- Stealth is not visualised at all. No detection cones, no patrol routes, no alert states — and
  since half the missions *are* stealth, that is the most important thing still missing.
- Renders are Blender Cycles, not Godot. Colour will shift on the way across.

## On the washed-out look (fixed in this pass)
The earlier sets were flat for three stacking reasons: a haze volume over the whole frame, a
strong ambient fill against a weak sun, and a high exposure on a Standard view transform. Fixed at
source — haze cut roughly 60%, sun energy raised and world strength cut so the key-to-ambient
ratio produces real shadows, palettes re-saturated, and a contrast S-curve with a true black point
added via `render.grade()`.

Worth recording: several earlier lighting edits were **silent no-ops** — a whitespace mismatch
meant the presets never actually changed, so every "brighter" render until now came only from
exposure and grade. The presets are live now.

## Next
1. Crews.
2. Stealth visualisation — detection, patrol lines, alert states.
3. The war map (§7.1) — the screen between missions, which has no picture at all.
4. Underwater for the recon mission: drowned leaf forest, silt, larvae.
