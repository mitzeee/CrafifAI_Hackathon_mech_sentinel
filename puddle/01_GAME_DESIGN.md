# THE DRYING
### *A war fought in a puddle, against a clock made of sunlight.*

> Working title. Alternates: **TARMAC SEA**, **BRACKWATER**, **A War Called Tuesday**.
> Engine: **Godot 4 (Forward+)**. Scope: medium, single-player first, co-op-ready architecture.

---

## 1. The One-Line Pitch

**Carrier Command in a puddle, on an evaporation clock.**

You are the captain of a scavenged cargo hauler — the *Ark* — crewed by finger-tall men, fighting
a total war across a chain of rain puddles in a supermarket parking lot. You don't watch the war
from a map. You *sit in every seat*: the bridge, the fighter cockpit, the bomb bay, the tank
turret, the motorcycle saddle. And the whole theater of war is evaporating under your feet.

---

## 2. Why This Shape (the "better operation" answer)

The original brief was an **anthology**: cargo captain, fighter, bomber, tank, motorcycle, "and
various other roles." Anthologies have a known failure mode — six shallow minigames stitched by a
mission-select menu, none of them deep, none of them connected, and the player never feels like a
*commander*, only a tourist.

**The fix: make the cargo ship the hub, not a level.**

The hauler is your mobile base. It carries the fighters in its deck bays, the bombers on its
spine, the tanks in its hold, the bikes on its gunwale rails. Every other role is *launched from
it*. That single change converts six disconnected missions into one continuous, escalating
operation:

| Anthology (original) | Carrier model (recommended) |
|---|---|
| Menu → pick role → play mission → menu | One unbroken world; you walk from the bridge to the flight deck |
| Roles are thematically related | Roles are **mechanically interdependent** — the bomber needs the fighter's escort, the fighter needs the ship's fuel, the ship needs the tank to take the shore battery that's shelling it |
| No strategic layer | The ship's position *is* the strategic layer |
| Nothing at stake between missions | Losses are permanent; a pilot who dies is gone, a hull that sinks stays sunk |
| Can't do co-op | Drop-in co-op falls out for free: one captain, one pilot, one gunner, same ship |

**The verb is possession, not selection.** Every vehicle you own is an AI-crewed unit running its
orders right now. At any moment you slam into any one of them and take the stick. The war does not
pause while you fly. That tension — *what is going wrong somewhere else while I'm doing this?* —
is the game.

**The second fix: give the roles a reason to exist in sequence.** See §4.

---

## 3. The World

### 3.1 Setting

**A wetland.** A big, deep pool sunk in marsh — ringed by sedge and cattail that stand over it
like a coastline of trees, floored with silt and drowned leaf-fall, skinned with lily pads and
algae, and walled in every direction by vibrant shrub, grass and mossy rock.

To the men who live in it this is an inland sea, and the reed beds around it are forest. The pool
connects to smaller pans and boggy channels through reed passes that open and close with the
water. Everything drains, eventually, toward the outflow at the low end of the marsh.

Nobody tiny knows what the marsh is. The tribes have cosmology for it. The reed wall is *the
Standing Forest*. The outflow is *the Throat*. A wading heron is *the Grey Judge*.

> **Setting note.** An earlier draft set this in a supermarket parking lot. The wetland is better
> on every axis: it justifies the Reedfolk's whole material language, it gives the Combine's
> scavenged human litter the weight of something *foreign* that washed in, and it turns the
> shoreline into a living wall instead of a kerb. The found-object rule survives intact — marsh
> litter is bottle caps, fishing line, shotgun wadding, a lost lure — but it now sits alongside
> seed pods, thorn, chitin and reed.

### 3.2 The Eight Theaters

Each puddle is a self-contained combat map, ~400 × 300 "game meters" (see §7.3 on scale).
They connect via rivulets that are navigable only at high water.

| # | Theater | Character | Signature hazard |
|---|---|---|---|
| 1 | **The Open Pool** | The deep centre. Wide, dark, lily-skinned. Home water. | None. Teaching water. |
| 2 | **The Reed Channel** | A pass between two reed stands — a green canyon. | Ambush topology; no room to manoeuvre aircraft |
| 3 | **Scum Bloom** | Decaying algae mat over black anoxic water. | Flammable marsh gas; nothing survives in the water |
| 4 | **The Braid** | A boggy delta of shifting channels in silt. | Channels close as the water drops — you strand |
| 5 | **The Snag Reef** | Fallen sticks, snail shells, a drowned lure. Shallow. | Cover-dense, tank country, terrible for aircraft |
| 6 | **The Lens** | A discarded bottle half-sunk at the margin, focusing sun. | A moving beam of lethal heat; burns hulls, boils water |
| 7 | **The Sluice** | The outflow creek. The current pulls, always. | Undertow; losing power means losing the ship |
| 8 | **The Throat** | The culvert the marsh drains into. Endgame. Dark, vertical. | Everything |

### 3.3 The Macro World as Weather

The human-scale world is not scenery, it's the **weather system** — acts of god neither tribe
controls, telegraphed with a few seconds of warning:

- **The Grey Judge** — a heron wades in. Legs like towers, a shadow that crosses the whole pool,
  and a strike that takes a ship and its crew out of the world. Cannot be fought. You get the
  shadow as warning, and a few seconds to scatter.
- **The Wading Beast** — a deer or boar crosses. Displaced water, a wall of silt, permanent new
  channels stamped into the bed.
- **Reed Wind** — the standing forest bends. Chop, driven spray, aircraft grounded, visibility gone.
- **The Lens Beam** — see Theater 6. Slow, inevitable, survivable if you read it.
- **Scum Bloom** — algae goes anoxic and spreads. Flammable, kills swimmers, blinds sonar.
- **The Rain Return** — see §4, Act IV. The apocalypse and the salvation.
- **Frog Fall** — a frog enters the water. A meteor strike, then a predator in your sea lane.
- **Dragonfly** — apex air predator. Eats both tribes' aircraft. The fighter's real job.
- **Strider Flock** — water striders skating the meniscus. Neutral until provoked. Beautiful.
- **Larvae Bloom** — mosquito larvae in the deep water. The submarine's problem.

---

## 4. The Clock: Evaporation as Core Mechanic

**Water level is the master variable of the entire game.** One float, `water_level`, drives
navigability, terrain, unit viability, faction strategy, and the campaign's act structure.

```
SPRING  ████████████████████  1.00   THE FLOOD      green, high, cold
EARLY   ██████████████        0.70   THE SHALLOWS   full growth, first margins
HIGH    ███████               0.35   THE DRYING     ochre, cracked silt, stranding
LATE    ██                    0.10   THE THROAT     dead reed, remnant pools
```

> **OPEN DECISION — the clock's timescale.** The original draft ran the whole war across one
> day, which works for a rain puddle on tarmac. A *big, deep* wetland pool does not evaporate in
> an afternoon, and a one-day clock now strains belief.
>
> **Recommendation: stretch the clock to a season** — spring melt through late-summer drought.
> Every mechanic below survives untouched; only the labels change. And it buys something the
> day-clock could never have: **the vegetation changes with the clock.** The reed wall goes green
> → gold → ochre → dead straw as the water falls. The act structure becomes visible in the
> foliage, not just the shoreline. The mock-ups already render this (`autumn_drying`), and it is
> the best-looking thing in the set.
>
> Cost: permadeath and fatigue read differently over months than over hours, and "one desperate
> day" is a cleaner pitch than "one long summer". **Your call before the full design doc.**

As the level falls:
- Navigable channels close. Your hauler gets **stranded** if you plan badly. This is the single
  most important strategic decision in the game: *where will my ship be when the water leaves?*
- Shoals surface and become land bridges. Tanks and bikes gain ground the navy loses.
- Sunken wrecks emerge — salvage, and cover.
- Deep water shrinks to a few basins. Submarines are lethal early, trapped late.

**This is why the roles exist in sequence.** It isn't a menu of six toys, it's a war whose
dominant arm *changes underneath you*:

| Act | Water | Foliage | Dominant arms | The feeling |
|---|---|---|---|---|
| **I — The Flood** | 1.00 → 0.70 | Deep green, rising | Hauler, submarine, torpedo boats | Naval. Open water. Grand. |
| **II — The Shallows** | 0.70 → 0.35 | Full growth, first gold | Aircraft, combined arms, first land bridges | Everything at once. Peak complexity. |
| **III — The Drying** | 0.35 → 0.10 | Ochre, cracking, dying | Tanks, bikes, artillery. The ship is beached and becomes a fortress. | Desperate, dusty, land war over a dying sea |
| **IV — The Return** *(conditional)* | 0.10 → 1.00 in 90 seconds | Flattened, drowned | Survival | A storm crest. Everything on the floor drowns. Everything that floats is saved. Your beached hauler either refloats or is crushed. |

Act IV triggers only if the player has completed the Reedfolk seeding objectives, or on a scripted
campaign beat. It is the game's best moment: total reversal, in ninety seconds, of everything you
spent three hours adapting to.

---

## 5. The Two Tribes

Not red vs blue. They disagree about *the puddle itself*, which is what makes the clock thematic.

### 5.1 The Windward Combine — "Tinmen"
**West shore. Industrial. Metal. They want the puddle gone.**

Scavengers of machine detritus — screws, foil, springs, circuit board, staples, razor blades.
Riveted plate hulls, coal-black smoke, sodium-orange running lights, gunmetal and rust. They
believe standing water is a disease; their great work is **the Drainage**, a pump-and-channel
project to empty the lot forever and inherit dry, defensible tarmac. They will win the war and
end the world, and they are entirely sincere about it.

- **Doctrine:** heavy, slow, armored, artillery-forward. Wins the late acts.
- **Signature unit:** *The Siphon* — a pump barge. A support unit that is also a weapon: parked in
  an enemy harbor it lowers local water level, beaching their fleet.
- **Palette:** gunmetal, oxide red, sodium orange, cold white sparks.

### 5.2 The Reedfolk — "Mirefolk"
**East shore. Organic. Grown. They want the puddle kept.**

Builders from seed pods, beeswax, chitin, resin, amber, waxed leaf, spider silk. Hulls are grown
and lacquered, not welded. They seed the water with algae mats to slow evaporation and cut the
sun. They believe the puddle is a living thing and the tribes are its passengers. They are also
willing to drown a thousand Tinmen to prove it.

- **Doctrine:** fast, light, amphibious, swarming. Wins the early acts.
- **Signature unit:** *The Bloom* — an algae seeder. Support that slows the global clock,
  contests the Combine's Drainage, and blinds air recon with green haze.
- **Palette:** amber, waxy green, bone-white chitin, resin gold, dark honey.

### 5.3 Why it works
The faction asymmetry maps directly onto the clock. The Combine is *trying to advance the act
structure*; the Reedfolk are *trying to hold it back*. Every skirmish is also a fight over what
time it is.

---

## 6. Roles — The Seats

All roles share one control philosophy: **full manual control, forgiving physics, arcade-sim.**
Not a study sim. You should be able to fly the fighter in ten seconds and still have a skill
ceiling in ten hours.

### Confirmed from brief

**1. Cargo Hauler Captain — *the Ark*** *(the hub role)*
Command the bridge of a scavenged bottle-cap-and-plate hauler. Helm, throttle, ballast, damage
control, launch/recovery ops, and the tactical table. Slow, huge, vulnerable, and carrying
everything you own. Ballast is a real verb — flooding tanks lets you cross under a low wire or
sit stable in a bow wave; pumping out lets you clear a shoal. Beaching is survivable but the
ship becomes a fixed fortress until Act IV.

**2. Fighter Pilot**
Rubber-band-and-stretched-membrane interceptor launched off the hauler's rail. Duties: air
superiority, strafing landing craft, escorting bombers, and **intercepting the neutral fauna**
(dragonflies are the apex air predator of this world and will eat both tribes' aircraft). Fast,
fragile, spectacular; a knife fight at three inches' altitude, with the water surface as a wall.

**3. Bomber Pilot**
Slow, heavy, two-seat. You fly it *or* you drop from it; in co-op, one player does each. Targets:
shore batteries, pump works, the enemy hauler, causeways. Ordnance is scavenged: matchhead
incendiaries, staple sticks, a single precious ball-bearing "bunker buster." Bombing a water
target produces a real, persistent ripple wave that shoves boats — **ordnance is a naval weapon.**

**4. Tank Operator**
Shore war. Treads on tarmac, grit, gravel, wet mud that behaves differently at different water
levels. Slow turret traverse, satisfying weight, hull-down play behind cigarette filters and
bottle caps. Wades to a fixed depth — and that depth is a live tactical question every act.

**5. Motorcycle Soldier**
The speed and spectacle role. Recon, courier, sabotage, harassment. A meniscus-skimming bike
that can **ride the surface tension itself** if you keep the throttle above a threshold — lose
speed over deep water and you sink. Wake spray, lean, drift, jumps off gravel ramps. This is the
role that goes in the trailer.

### Recommended additions

**6. Submarine Commander** *(strongest addition)*
The puddle has *depth*, and nobody expects it. A sealed pill-capsule hull below the silt line.
Down there: drowned leaf forests, a sunken bottle cap as a wreck to hide under, silt clouds,
algae kelp, mosquito larvae the size of submarines, and the pressure-dark of the deep basin.
Ties into the clock perfectly — dominant in Act I, hunted and trapped in Act III as the basin
shrinks around it.

**7. Combat Engineer / Salvage Crew**
Third-person, on foot. Pontoon causeways, field repairs, cutting an enemy channel, towing wrecks,
and operating the pumps. The role that *changes the map.* Also the tutorial for the economy.

**8. Artillery Spotter**
Two-part role — call from a high point (a curb, a cinderblock), or serve the gun. Arcing fire
across the whole theater. In co-op this is the best two-player role in the game.

**9. AA Gunner**
Short, tense, defensive turret sessions aboard the hauler under air attack. Not a campaign role —
an *interrupt*. You're on the bridge, klaxon sounds, you sprint to a gun.

**10. Rescue Coxswain**
A role with no gun. Pull survivors out of the water before the oil ignites or the larvae find
them. Recovered crew return as veterans — this is where the permanent-loss system gets teeth.

### Deliberately cut
Infantry FPS (dilutes the vehicle identity, triples the animation budget), and any role that
can't be launched from or supported by the hauler.

---

## 7. Systems

### 7.1 Possession & Command
- Every owned unit is an autonomous agent with an order queue. The AI is competent, not brilliant.
- **Tactical Table:** pause-light strategic view from the hauler's bridge. Issue orders, then
  *dive into* any unit. Transition is a continuous camera move, never a load screen.
- **Hot-seat urgency:** you cannot be everywhere. The AI will lose fights you should have flown.
  This is the intended pressure, not a flaw to patch out.
- **Ghost handoff:** when you leave a unit, the AI resumes from exactly your state and heading.

### 7.2 Economy — Salvage
No currency. You scavenge **Scrap** (Combine) / **Resin** (Reedfolk) from debris, wrecks, and
captured caches. Spend at the hauler's workshop on hull refits, ordnance, and replacement crew.
As the water falls, new wrecks surface — **the clock is also the economy's release schedule.**

### 7.3 Scale — the critical production note
**Do not build at true miniature scale.** A hauler 4 cm long with Godot's default gravity and
collision margins produces jittering physics, broken buoyancy, and unusable camera near-planes.

**Build everything at "game scale"** — treat a puddle as 400 m across and a hauler as a 30 m ship.
Sell the miniature-ness entirely through *presentation*:
- Aggressive tilt-shift depth of field with an oversized circle of confusion
- Dust motes and pollen as volumetric particles at all times
- Macro reference objects (a staple, a grain of sand) modeled at the scale they'd be
- Shallow, high-frequency surface detail on "huge" objects
- Fast, small-amplitude water — miniature water moves *quickly*, that's the tell

This one decision saves weeks of physics debugging.

### 7.4 Permanence
Crew are named and die permanently. Hulls that sink stay on the seabed for the whole campaign as
navigable wrecks. Terrain damage from the Rolling God persists. The parking lot at 18:00 is a
visibly different place from the parking lot at 06:00, and it's your fault.

---

## 8. Technical Plan — Godot 4

**Target:** Godot 4.4+, Forward+ renderer, GDScript core with C# or GDExtension only for measured
hot paths. Jolt physics (built-in from 4.4). PC first (Windows/Linux), Steam Deck as the perf bar.

### 8.1 Water — the signature tech
Not a fluid simulation. A layered fake that looks better than a sim at this scale:

1. **Heightfield surface** — summed Gerstner waves in a vertex shader on an LOD'd plane, driven
   by a single global `water_level` uniform. Small amplitude, high frequency (see §7.3).
2. **Interactive ripple buffer** — a `SubViewport` holding a 2-channel wave-propagation texture.
   Every hull, bomb, footfall, and raindrop writes an impulse into it; the shader reads it as a
   normal-map perturbation. *This is the feature that sells the whole game* — wakes that persist,
   interfere, reflect off shores, and shove other boats.
3. **Shore blending** — soft depth-fade, refraction via screen texture, wet-sand darkening band
   that recedes with the level and leaves a visible tide mark.
4. **Buoyancy** — probe-point buoyancy (4–8 probes per hull) sampling the same heightfield the
   shader uses. Cheap, stable, and correct-looking.
5. **Meniscus layer** — a thin separate surface tension shell at the shoreline and around striders
   and the motorcycle. Purely visual + one boolean physics state.

### 8.2 Scene architecture
```
World (Node3D)
├── Theater (one puddle, own scene, streamed)
│   ├── WaterVolume        # Gerstner + ripple SubViewport
│   ├── Terrain            # static mesh + tide-mark shader
│   ├── DebrisField        # MultiMeshInstance3D
│   └── MacroEventDirector # Rolling God, Boot, Lens, Rain
├── CampaignState (autoload Resource)  # water_level, roster, salvage, wrecks
├── UnitPool               # every owned/enemy unit, AI-controlled by default
└── PossessionManager      # swaps Controller nodes; owns camera transitions
```
Each unit = `Rig` (mesh/physics) + swappable `Controller` (`AIController` ⇄ `PlayerController`).
Possession never respawns the unit; it swaps one child node. That is the whole trick, and it's
what makes drop-in co-op a later config change rather than a rewrite.

### 8.3 Performance plan
- `MultiMeshInstance3D` for debris, crowds, and the infantry that never need individual logic
- Aggressive LOD + visibility ranges; theaters are small and bounded by design
- Ripple SubViewport at 256², updated at 30 Hz, not 60
- Tilt-shift DoF is a full-screen effect: budget for it early, it is non-negotiable to the look
- AI runs on a staggered tick (units update on rotating frames), not every frame

### 8.4 Risks
| Risk | Mitigation |
|---|---|
| Water shader eats the whole schedule | Timebox it. M1 ships an ugly-but-correct version; polish in M5 |
| Six roles = six control schemes to tune | Build the fighter and hauler first. If those two aren't fun, cut roles, don't add them |
| `water_level` touching everything = fragile | One autoload, one signal, every consumer reads — never writes — it |
| Scope | The theater list is ordered. Theaters 1, 3, 5 alone are a shippable game |

---

## 9. Milestones

| # | Name | Deliverable | Gate |
|---|---|---|---|
| **M0** | Grey Sea | Godot project, flat water plane, one box boat, buoyancy, camera | Does a box on water feel good? |
| **M1** | Wake | Interactive ripple buffer, wakes, shore fade, `water_level` as a live global | Does lowering one slider visibly change the world? |
| **M2** | Two Seats | Hauler + fighter, full manual control, launch and recovery, possession swap | **Hard gate — are these two fun?** |
| **M3** | War | AI units, orders, tactical table, combat, damage, salvage economy | Is it a game? |
| **M4** | The Clock | Full act structure, stranding, land bridges, tank + bike + bomber | Does the war change shape as it dries? |
| **M5** | The Look | Art bible applied, tilt-shift, VFX, audio, macro event director | Screenshot test |
| **M6** | The Lot | All 8 theaters, campaign, permanence, Act IV, submarine + engineer | Ship |

**Vertical slice = M0–M2 + Theater 1.** One puddle, hauler and fighter, one enemy hauler, one
dropping water level. If that is fun for ten minutes, the rest of this document is worth building.

---

## 10. Co-op (design for it now, ship it later)
2–4 players, drop-in, same hauler group. One captain, one pilot, one gunner, one engineer. The
possession architecture in §8.2 makes this a networking problem, not a design problem — but only
if `Controller` swapping is respected from M2 onward. **Do not let anything read player input
outside a Controller node.**

---

## 11. Open Questions
1. Player faction: fixed (Combine campaign only) or both? *Recommendation: Combine campaign ships
   first — the "win the war, kill the world" arc is stronger. Reedfolk in a second campaign.*
2. Does Act IV end the game or reset the clock? *Recommendation: reset once, then never again.*
3. Named-crew permadeath — full ironman or one resurrection? *Recommendation: Rescue Coxswain
   exists precisely so permadeath has a counterplay. Keep it brutal.*
4. Art render style — **pending reference screenshot.**

---

*Document status: design locked pending §11. Art bible: `02_ART_BIBLE.md`.*
