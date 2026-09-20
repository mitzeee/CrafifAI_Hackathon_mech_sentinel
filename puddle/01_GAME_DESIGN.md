# BRACKWATER
### *A war fought in a wetland, by men the size of a fingernail.*

> Working title — **"THE DRYING" is retired**, since the pool no longer dries. Alternates:
> **THE STANDING FOREST**, **MIREFRONT**, **REEDWAR**. Your call.
> Engine: **Godot 4 (Forward+)**. Scope: medium, single-player first, co-op-ready architecture.

---

## 1. The One-Line Pitch

**Eight missions, eight machines, one wetland — and half of them have no gun.**

Two tribes of finger-tall men hold opposite shores of a deep marsh pool. You are whoever the war
needs today: the driver running rations up a mud track at dusk, the submarine commander counting
hulls through a periscope, the bomber pilot with one precious ball bearing, the fighter pilot
whose job is not to survive but to make sure a truck somewhere else does.

The machines are built from what the marsh gave them and what washed into it — a crushed drink can
for a hull, a bottle cap for a turret, a matchstick for a fork leg, watch gears for road wheels.

---

## 2. Shape: a campaign of missions, one vehicle each

**Every vehicle is its own mission type, with its own verb.** You do not fly a generic war in a
generic machine; you are handed a job, and the job comes with the vehicle that does it.

| Mission | Vehicle | Verb | What failure costs |
|---|---|---|---|
| **Land logistics** | Supply truck | Sneak rations and raw material up the bank track | The front goes hungry |
| **Light courier** | Auto-rickshaw | Thread a reed pass a truck cannot | Orders arrive late, or never |
| **Water logistics** | Cargo hauler | Run supplies across the pool, loaded and slow | A season's materiel on the bottom |
| **Reconnaissance** | Submarine | Watch, count, listen, come home unseen | You bomb blind |
| **Strategic strike** | Bomber | Destroy what the enemy cannot move | Their war machine keeps running |
| **Air intercept** | Fighter | Break up their flight before it reaches your convoy | Your convoy dies, not you |
| **Ground action** | Tank | Take and hold the bank so convoys can run | The route closes |
| **Scout / harass** | Motorcycle | Find the patrol line, and be somewhere else | You drive into it next time |

**Half the missions have no guns.** That is the point. Logistics and recon are stealth problems —
route, timing, weather, and not being seen — not combat problems. A game where the truck run is as
tense as the bombing run is a more interesting game than one where it is a loading screen.

> **Design note, honestly flagged.** An earlier draft of this document argued *against* the
> mission anthology and proposed a carrier model instead — the hauler as a hub that launches every
> other vehicle. That was overridden, and correctly: it collapsed eight distinct jobs into one
> machine and lost exactly the variety that makes the premise work. What survives from it is the
> one idea worth keeping — **interdependence** — and §4 is how it is kept without a carrier.

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

## 4. The Spine: the supply line, not a clock

**The pool never dries up.** Earlier drafts made evaporation the master variable and the campaign
a doomsday clock. That is cut. A deep wetland pool is permanent, and a war fought around one needs
a spine made of something the players actually control.

**That spine is materiel.** Every mission feeds or starves another mission:

```
        RECON  ──reveals──►  STRIKE  ──destroys──►  enemy strategic assets
     (submarine)              (bomber)                      │
          ▲                      ▲                          │ weakens
          │                      │ needs escort             ▼
          │                  INTERCEPT                enemy raids on YOUR convoys
          │                   (fighter)                      │
          │                      ▲                           │ threatens
          │                      │ protects                   ▼
     GROUND ACTION ──opens──►  LOGISTICS  ──────supplies──► everything above
        (tank)                (truck · rickshaw · hauler)
```

Read it as a loop. Recon reveals targets; without it the bomber area-bombs and mostly misses.
Strikes wreck the enemy's pump house, granary and slipway, which cuts the raids they can mount
against your convoys. Fewer raids means your logistics get through. Supply that gets through buys
the armour that opens the next route. **And the enemy is running the same loop against you.**

### 4.1 Why this is better than the clock
- Every vehicle is load-bearing. Skip recon for three missions and the bombing goes blind — you
  feel the gap without being told.
- It creates real strategic choice without a strategy layer: *which* mission you fly personally.
- It gives failure a texture. A lost convoy is not a lost life bar, it is armour you don't have
  next week.
- It survives a permanent pool.

### 4.2 You cannot be everywhere
Each turn of the war offers several missions. **You fly one; the AI resolves the rest, worse than
you would.** That pressure — *what is going wrong somewhere else while I'm doing this?* — was the
single best thing about the discarded carrier model, and it transplants cleanly.

### 4.3 Seasons and weather: flavour and complexity, never a clock
Weather changes how a mission is fought, not how long the war lasts.

| Condition | Effect |
|---|---|
| **Rain** | Visibility collapses. The best smuggling window in the game, and aircraft are grounded |
| **Dawn mist** | Cover on the water, useless on land. Convoys move at first light for a reason |
| **Wind** | Chop on the pool, aircraft grounded, and the reed wall bends — sightlines open that were closed |
| **Night** | Cover for everyone, including the patrol you cannot see |
| **Algae bloom** | Chokes channels in high summer. Routes close; the hauler reroutes long |
| **Hard frost** | Margins freeze. New land routes open where boats used to run |

### 4.4 The reed cycle — the map's slow variable
What the water level used to do, **vegetation** now does better. The reed wall grows and dies back
across the year:

| Season | Reed state | What it means |
|---|---|---|
| **Spring** | New growth, low and sparse | Open sightlines. Everything is exposed. Armour's season |
| **Summer** | Dense, tall, green | Maximum cover. Passes close. Smuggling's season |
| **Autumn** | Gold, thinning | Cover degrading week by week. Routes reopen |
| **Winter** | Dead straw, flattened | The marsh is naked. Long sightlines, new routes, nowhere to hide |

Cover, routes and sightlines all change — but nothing is *dying*, so there is no doomsday pressure
and no forced ending. The art system for this already exists (one `autumn` parameter).

---

## 5. The Two Tribes

Not red vs blue. They disagree about *what the marsh is for*, and every supply route, pump
house and burned reed bed is an argument in that disagreement.

### 5.1 The Windward Combine — "Tinmen"
**West shore. Industrial. Metal. They want the marsh put to work.**

Scavengers of machine detritus — screws, foil, springs, circuit board, staples, razor blades.
Riveted plate hulls, coal-black smoke, sodium-orange running lights, gunmetal and rust. They
believe the marsh is raw material going to waste. Their great work is **the Reclamation**: pump
the margins, channel the flow, cut the reed, and turn shoreline into buildable, defensible,
*productive* ground. They are not trying to kill the pool — they are trying to industrialise
everything around it, and they are entirely sincere that this is progress.

- **Doctrine:** heavy, slow, armored, artillery-forward. Wins the late acts.
- **Signature unit:** *The Siphon* — a pump barge. A support unit that is also a weapon: parked in
  an enemy harbour it drops the local margin, beaching their fleet and killing the reed cover
  they were hiding in.
- **Palette:** gunmetal, oxide red, sodium orange, cold white sparks.

### 5.2 The Reedfolk — "Mirefolk"
**East shore. Organic. Grown. They want the marsh left as it is.**

Builders from seed pods, beeswax, chitin, resin, amber, waxed leaf, spider silk. Hulls are grown
and lacquered, not welded. They seed algae mats, plant reed, and cultivate the cover they
fight from. They believe the marsh is a living thing and the tribes are its passengers. They are
also willing to drown a thousand Tinmen to prove it.

- **Doctrine:** fast, light, amphibious, swarming. Wins the early acts.
- **Signature unit:** *The Bloom* — an algae seeder. Support that grows new cover where there was
  none, chokes channels the Combine depends on, and blinds air recon with green haze.
- **Palette:** amber, waxy green, bone-white chitin, resin gold, dark honey.

### 5.3 Why it works
The asymmetry maps onto the reed cycle (§4.4), which is the map's slow variable. The Combine wants
the marsh **cut and open** — clear fields of fire, hard routes, no cover for smugglers. The
Reedfolk want it **dense and grown** — cover everywhere, channels that only they can read. So
every burned reed bed and every seeded bloom is both tribes editing the battlefield toward the
shape that suits them. That is a live, two-sided terrain war, and it never has to end.

---

## 6. The Missions

One control philosophy across all of them: **full manual control, forgiving physics, arcade-sim.**
Learnable in ten seconds, a skill ceiling in ten hours. Not a study sim.

Missions split into two families that play nothing alike.

### 6.A Quiet missions — logistics and recon
No guns, or guns you should not fire. The verbs are **route, timing, concealment and load**. These
are tension games, and they are half the campaign.

**1. Supply truck — land logistics**
Rations and raw material up the bank track to the front. Slow, loud, loaded, defenceless. You
choose the route (the short exposed track or the long covered one), the hour (mist, rain, night)
and the load (heavy and slow, or light and twice as many runs). Getting seen is not instant death —
it starts a chase you are certain to lose unless you planned for it.

**2. Auto-rickshaw — light courier**
Three wheels, no armour, no gun, and the only thing in the fleet that threads a reed pass a truck
cannot. Small urgent loads: medicine, orders, a single passenger who matters. Fast and fragile —
this is the one you take when the truck route has already been cut.

**3. Cargo hauler — water logistics**
The same job across the pool, loaded and slow, with no cover but the reed line and nowhere to run.
Ballast is a real verb: trim down to pass under a fallen stem, pump out to clear a shoal. Beaching
is survivable and ruinous.

**4. Submarine — reconnaissance**
Go under to watch, count, listen and come home. The win condition is **information**, not kills —
and firing the torpedoes ends the mission. What recon reveals is what the bomber can aim at
(§4); skip it and the strike missions go blind.

**5. Motorcycle — scout and harass**
Find the patrol line, map it, and be somewhere else. The speed role, and the trailer role. Rides
the meniscus above a threshold speed; lose speed over deep water and you sink.

### 6.B Loud missions — combat
The verbs are **aim, manoeuvre and commit**.

**6. Bomber — strategic strike**
Slow, heavy, two-seat. Goes deep across the pool to hit what the enemy cannot move: pump works,
slipways, granaries, the far hauler at anchor. Ordnance is scavenged — matchhead incendiaries,
staple sticks, one precious ball-bearing. Dead without escort, and blind without recon.

**7. Fighter — air intercept**
Break up their flight before it reaches your convoy. Note the framing: **you are not defending
yourself, you are defending a truck somewhere else.** Also the only answer to the dragonflies,
which are the apex air predator here and eat both tribes' aircraft.

**8. Tank — ground action**
Take and hold bank so the convoys can run. Slow turret, satisfying weight, hull-down behind
mossy rock and fallen stems. Wades to a fixed depth, and the reed cycle (§4.4) decides every
season whether that ground is covered or naked.

### 6.C Supporting roles *(later, if the eight above land)*
Combat engineer (causeways, repairs, cutting a channel — the role that *changes the map*),
artillery spotter, AA gunner as an interrupt rather than a mission, rescue coxswain.

### Deliberately cut
Infantry FPS — it dilutes the vehicle identity and triples the animation budget.

### The mission-variety test
The eight above must feel like eight games, not one game with eight skins. If the truck run plays
like the tank run with less armour, **cut the truck** rather than ship a reskin. The quiet/loud
split in §6.A/§6.B is the safeguard: a mission with no gun cannot accidentally become a shooter.

---

## 7. Systems

### 7.1 The war map and mission select
- Between missions you sit over a **war map** of the marsh: your shore, theirs, the routes, the
  known strategic assets, the current reed state and the weather forecast.
- Each turn offers several missions. **You fly one. The AI resolves the rest, worse than you
  would** (§4.2). The map shows you exactly what you are choosing to let go badly.
- Recon progressively reveals the enemy half of the map. Unrevealed assets cannot be targeted.
- No unit possession-swapping mid-mission — that belonged to the discarded carrier model. One
  mission, one vehicle, start to finish.

### 7.2 Economy — Supply and Materiel
Two stocks, and the whole campaign runs on them.

- **Rations** keep units in the field. Run out and formations weaken, then desert.
- **Materiel** (Scrap for the Combine, Resin for the Reedfolk) buys hulls, ordnance and repairs.

Logistics missions *deliver* both; combat missions *consume* them; strike missions *deny* them to
the enemy. There is no currency and no shop — what you delivered last week is what you are flying
this week. A convoy lost is not an abstract penalty, it is the escort fighter you do not have.

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
Crew are named and die permanently. Hulls that sink stay on the bed for the whole campaign as
navigable wrecks. Burned reed beds stay burned until the next growing season; cut channels stay
cut; a wrecked pump house is rubble for months. The marsh at the end of a campaign is a visibly
different place from the marsh at the start, and it is your fault.

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
| **M2** | Two Missions | One quiet mission (supply truck) and one loud (fighter), full manual control, start to finish | **Hard gate — is the truck run as tense as the dogfight?** |
| **M3** | War | AI units, orders, tactical table, combat, damage, salvage economy | Is it a game? |
| **M4** | The Loop | War map, supply/materiel stocks, recon-reveals-strike chain, AI resolving the missions you skip | Does skipping recon visibly hurt the next bombing run? |
| **M5** | The Look | Art bible applied, tilt-shift, VFX, audio, macro event director | Screenshot test |
| **M6** | The Lot | All 8 theaters, campaign, permanence, Act IV, submarine + engineer | Ship |

**Vertical slice = M0–M2.** One stretch of marsh, one supply run and one intercept. If the *truck
mission* is fun for ten minutes with no gun on it, the rest of this document is worth building.
If it is not, the whole quiet/loud split is in question and better to know in week three.

---

## 10. Co-op (design for it now, ship it later)
2–4 players, drop-in, same hauler group. One captain, one pilot, one gunner, one engineer. The
possession architecture in §8.2 makes this a networking problem, not a design problem — but only
if `Controller` swapping is respected from M2 onward. **Do not let anything read player input
outside a Controller node.**

---

## 11. Open Questions
1. **Title.** "The Drying" is retired with the clock. **BRACKWATER** is the working replacement.
2. **Does the campaign end?** With no clock there is no forced ending. *Recommendation: a
   territorial win condition — hold every route on the pool for one full season — plus an
   open "endless marsh" mode. It needs to be winnable, not merely survivable.*
3. **Player faction:** Combine campaign first, Reedfolk second? *Recommendation: yes. The
   Reclamation arc is the stronger story and the Combine's scavenged kit is the better tutorial.*
4. **How punishing is a failed convoy?** *Recommendation: painful but never a dead end — the
   next mission gets harder, not impossible.*
5. **Named-crew permadeath** — full ironman, or the rescue coxswain as counterplay? *Recommendation:
   keep it brutal, keep the counterplay.*

---

*Document status: design locked pending §11. Art bible: `02_ART_BIBLE.md`.*
