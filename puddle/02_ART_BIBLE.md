# THE DRYING — Art Bible

> **Status:** locked. §2 resolved against the reference frame. First procedural asset pass is
> built and exported — see `blender/README.md` and `assets/reference/fleet_sheet.png`.

---

## 1. The One Sentence

**A real wetland, photographed with a macro lens, where the marsh has been colonised and the
garbage has been conquered.**

Two material languages, and everything must belong to one of them. The **Reedfolk** build from
what grows here — seed pod, wax, chitin, resin, reed, thorn. The **Combine** build from what
*washed in* — tin, foil, staple, screw, bottle cap, razor blade. Human litter should always read
as foreign, older and harder than everything around it. If an asset can't be traced to either the
marsh or the litter in it, it doesn't belong in the game.

---

## 2. Render Style — LOCKED

**Faceted low-poly naturalism.** Cheap geometry, flat shading, flat colour; lighting and
composition carry the image.

| Variable | Decision |
|---|---|
| **Shading** | **Flat / hard-edged everywhere.** Faceting is the look, not a budget compromise. Smoothing groups are the exception, used only where a Reedfolk hull must read as a grown compound curve |
| **Geometry** | Low, chunky, readable. 6–14 segments on round forms. A pebble is 40–120 tris; a hero hull is ~3k |
| **Texture** | **None.** Flat per-material colour, one material per real-world substance. Wear and decals come later as a separate pass, never as a base requirement |
| **Metalness** | Deliberately restrained. High-spec metal reads as a different game — the Combine's "metal" sells through faceted silhouette and value contrast, not reflections |
| **Saturation** | Low. Muted, dusty, earthbound. Faded brick red, olive, ochre, bone grey. No pure hues |
| **Lighting** | Soft warm key (overcast-through-cloud), cool sky fill, warm ground bounce. Gentle shadows, strong AO, mild haze with distance |
| **Outlines** | None. Silhouette separation comes from value, not ink |
| **Post** | Slight vignette, filmic curve with lifted blacks, moderate DoF |
| **Camera** | High third-person, 20–30° elevation, 55–70 mm. Close to the reference framing |

### The tilt-shift revision
The original §3 called extreme tilt-shift non-negotiable. **That was wrong for this style.**
Faceted low-poly already reads as *constructed* — stacking aggressive miniature-faking on top
over-eggs it and makes the world read as a toy rather than a place. Use **moderate** depth of
field, and carry the sense of scale on macro reference props, particulate air and fast small
water instead. §3.1 below is amended accordingly.

---

## 3. The Non-Negotiables (whatever the style)

These four sell "miniature world" harder than any texture decision:

1. **Moderate depth of field** — amended, see §2. A soft falloff at the far edge of the theater,
   not an oversized circle of confusion. The faceted style is already doing the "this is a
   constructed miniature" work; let it.
2. **Atmosphere is always particulate.** Dust motes, pollen, spray, midges, steam. The air is
   never empty. Macro photography always has stuff floating in it.
3. **Water moves fast and small.** High-frequency, low-amplitude ripples. Slow rolling ocean
   swells instantly read as "full scale" and destroy the illusion.
4. **Macro reference objects in every shot.** A staple. A sand grain. A hair. A bottle cap. The
   player must never lose the sense of how small this is — you do that by keeping a *known object*
   in frame. With the tilt-shift dialled back this is now the **primary** scale cue, which is why
   the prop kit was built in the first asset pass rather than last.

---

## 4. World Look

### 4.1 The Marsh
A **standing forest of sedge and cattail** rings the pool — at this scale a blade of grass is a
tree and a reed stand is a coastline. Behind it: vibrant shrub in layered greens and ochres,
tussock grass, fern, and mossy rock the size of hills. Underfoot, peat and silt, drowned
leaf-fall, root tangle.

Foliage is the primary visual. It is not set dressing — it is the terrain, the cover, the
skyline and the clock. Build it chunky and angular: big flat leaf-blades fanned from a point, not
billboards. Silhouette over detail.

### 4.2 Water
- **Surface:** dark, tannin-stained and strongly reflective — this pool is *deep*. Sky, reed
  wall and lily pads mirrored in it. Far less transmissive than a rain puddle; depth must read
  as depth.
- **Skin:** lily pads and algae mats, which double as cover, landing platforms and map features.
- **Shoreline:** the most important surface in the game. A wet-dark band, then a drying band, then
  dry tarmac. **The wet band recedes all day and leaves visible tide marks** — concentric rings of
  grit and grime that are a permanent record of the act structure. Players should be able to read
  the time of day off the shore.
- **Underwater:** silt haze, god-rays, drowned leaf-forests, algae kelp, debris embedded in mud.
  Visibility falls with depth and rises as the water drops.

### 4.3 Sky and Light
Only one day. The lighting *is* the clock:

| Act | Time | Light |
|---|---|---|
| I | 06:00 | Blue-grey dawn, long shadows, wet everything, low contrast, mist over the water |
| II | 10:00 | Clean high sun, sharp shadows, water at its most beautiful, maximum saturation |
| III | 14:00 | Hot, bleached, heat shimmer, dust, high contrast, shadows short and hard |
| IV | 18:00 | Storm light — bruised sky, wind, first heavy drops, everything goes dark and violent |

### 4.4 The Macro Intrusions
Rendered *huge and cropped* — a heron is two tower-legs and a shadow that swallows the pool.
Never show the whole creature; always partial, always too big for the frame. The Grey Judge is
terrifying precisely because you cannot see all of it.

### 4.5 The Foliage Clock
The reed wall carries the act structure in its colour: deep green at the flood, full growth with
first gold in the shallows, ochre and cracking in the drying, dead straw at the end. This is the
single cheapest, strongest way to tell the player what time it is — cheaper than UI, and visible
from any camera angle.

---

## 5. Faction Design Language

### 5.1 The Windward Combine — "Tinmen"
**Verb: riveted. Everything is cut, bent, bolted and welded from human machine detritus.**

| | |
|---|---|
| **Source materials** | Sheet steel, tin can wall, aluminium foil, screws, springs, staples, razor blades, circuit board, wire, solder, bottle caps, paperclips |
| **Construction** | Overlapping riveted plate, visible weld beads, exposed fasteners, patch repairs over patch repairs |
| **Silhouette** | Boxy, top-heavy, asymmetric, bristling. Every unit looks *assembled*, never designed |
| **Surface** | Scratched paint over rust over bare metal. Three layers of history on every panel |
| **Palette** | Gunmetal `#4A5057` · oxide red `#8C3A21` · sodium orange `#F2801D` · bone grey `#B8B5AC` · spark white |
| **Light** | Warm orange running lights, welding-arc white, coal smoke |
| **Insignia** | A stencilled downward arrow — *the water goes down* |
| **Sound identity** | Diesel, clank, steam release, rivet-gun stutter |

**Signature: *The Siphon*** — a low pump barge. A corrugated drinking-straw intake trunk, a wet
sputtering pump-heart of springs and rubber, and a spreading dry circle around it where it has
drunk the water away.

### 5.2 The Reedfolk — "Mirefolk"
**Verb: grown. Everything is cultivated, waxed, lashed and lacquered from organic matter.**

| | |
|---|---|
| **Source materials** | Seed pods, beeswax, chitin shell, tree resin, amber, waxed leaf, spider silk, thorn, reed, bark, cicada wing — all of it harvested from the marsh they are standing in |
| **Construction** | Lashed and lacquered; compound-curve pod hulls; silk rigging; nothing bolted |
| **Silhouette** | Curved, streamlined, tapering, insectile. Bilaterally symmetric — they grew it |
| **Surface** | Translucent shell with light passing through it. Resin gloss. Waxy bloom |
| **Palette** | Amber `#D99A2B` · waxy green `#6E7F3A` · bone chitin `#E8DCC0` · honey dark `#4A2E14` · resin gold |
| **Light** | Bioluminescent green-blue, firefly lanterns, glowing resin seams |
| **Insignia** | A closed circle with a drop inside — *the water stays* |
| **Sound identity** | Creaking wood, wet organic, insect chitter, wind through reeds |

**Signature: *The Bloom*** — an algae seeder. A broad flat pod-barge trailing green mats that
spread visibly across the water behind it, dimming the surface and slowing the clock.

### 5.3 Reading the difference at 200 metres
Combine = **straight lines and smoke.** Reedfolk = **curves and glow.** A player must be able to
call the faction from the silhouette alone, in fog, at night, out of focus.

---

## 6. Asset Taxonomy — the found-object rule

Every asset gets a **provenance**: the human object it was made from. This is the discipline that
keeps the world coherent when the asset count gets large.

### 6.1 Vehicles

| Unit | Combine provenance | Reedfolk provenance |
|---|---|---|
| **Hauler (Ark)** | Crushed drink can hull, bottle-cap conning tower, foil deck plating, razor-blade ram bow | Great seed-pod hull, waxed-leaf deck, resin-lacquered shell, silk rigging |
| **Fighter** | Stretched-membrane wing on a paperclip frame, rubber-band torsion launch | Cicada-wing glider, chitin fuselage, living-thorn talons |
| **Bomber** | Matchbox fuselage, foil wings, a ball-bearing slung under the belly | Hollow pod bomber, wax-sealed spore bombs |
| **Tank** | Bottle-cap hull on watch-gear tracks, nail-barrel gun, staple-plate armour | Beetle-shell casemate, thorn cannon, resin-plate armour |
| **Motorcycle** | Spool-and-spring frame, matchstick forks, foil fairing | Water-strider legged frame, chitin body, spider-silk grips |
| **Submarine** | Sealed pill capsule, wire fins, a tiny glass porthole | Waxed pod, breathing reed snorkel, translucent amber hull |
| **Artillery** | Rubber-band torsion catapult throwing staples and ball bearings | Thorn-spring ballista throwing resin shot |

### 6.2 Ordnance
Matchhead incendiaries · staple flechettes · ball-bearing penetrators · glass-shard shrapnel ·
resin-glue foulant · spore gas · thumbtack mines · a single, precious, campaign-unique
**Battery Cell** — the nuclear option, leaking acid, and the Combine's endgame weapon.

### 6.3 Structures
Cigarette filters as sandbags · bottle caps as bunkers · matchstick palisades · a crushed can as
a fortress · chewing-gum foil as roofing · a drinking straw as a pipeline · the storm grate bars
as cathedral architecture.

### 6.4 The Men
Finger-tall. Deliberately **low-detail and silhouette-driven** — they are crew and crowd, not
the camera's subject. Combine: goggles, welding masks, oilskin, heavy boots. Reedfolk: wax cloaks,
chitin helms, bare feet, woven silk. Readable at a glance, cheap to produce, animated in bulk.

---

## 7. VFX Language

| Effect | Note |
|---|---|
| **Wakes** | The hero effect. Persistent, interfering, shore-reflecting. From §8.1 of the design doc |
| **Spray** | Every hull, constantly. Fine droplet mist off the motorcycle at speed |
| **Meniscus** | Visible surface-tension shell at shorelines and around the bike and striders |
| **Explosions** | *Wet* — a water column, then a ring wave that shoves boats, then rain-back |
| **Smoke** | Combine: black, oily, heavy, hugging the water. Reedfolk: pale green, rising, translucent |
| **Fire on oil** | Spreads across the surface as a living map feature, not a particle |
| **Heat shimmer** | Act III, everywhere, over tarmac. A time-of-day tell |
| **Silt** | Kicked up by anything touching the bottom. Persistent clouds. Concealment |
| **Sunbeams** | Through the water surface from below; through the bottle Lens from above |

---

## 8. UI & HUD

**Diegetic wherever possible.** Instruments are *objects in the cockpit*, built from the same
found-object language: a compass is a magnetised needle on a cork float; the fuel gauge is a
sight-glass; the tactical table is a scratched tarmac map with pebble tokens.

The only non-diegetic element is the **water-level gauge** — permanent, in the corner, a
falling column. The player should feel it in their peripheral vision all game.

Type: Combine = stencilled industrial, hand-painted over metal. Reedfolk = organic, incised,
almost runic. Never a clean modern UI font anywhere in the game.

---

## 9. Audio Direction *(one paragraph, because it's half the miniature illusion)*

**Record everything close-mic'd and small, then pitch it down.** Real miniature audio is the same
trick as miniature visuals — a matchstick snapping, pitched down two octaves, *is* a snapping mast.
Water is the constant bed: lapping, trickling, dripping. The clock is audible — the ambient
trickle of draining water never stops and slowly gets quieter across the campaign. Silence in
Act III should feel wrong.

---

## 10. Production Order for Art

1. **The shoreline shader + tide marks** — it carries the clock, the game's core idea
2. **Combine hauler + fighter** — the M2 gate units
3. **Theater 1 (The Shallows)** environment kit
4. **Reedfolk hauler + fighter** — proves the faction language reads
5. Tank, bike, bomber
6. Macro intrusion set (car, boot, lens)
7. Remaining theaters in the order listed in the design doc
8. Submarine + underwater kit

---

## 11. Concept Art Shot List

To be generated once §2 is locked. Each of these is a specific, framed image, not a study:

1. **Key art** — the Combine hauler under way at dawn, Theater 1, macro lens, a staple in the
   foreground for scale
2. **The two haulers, side by side, same lighting** — the faction language bible page
3. **Shoreline study, four panels** — the same 10 metres of shore at 06:00 / 10:00 / 14:00 / 18:00
4. **Cockpit interiors** — hauler bridge, fighter, tank. Diegetic UI in place
5. **The Rolling God** — a car's shadow crossing the lot, bow wave incoming, from deck level
6. **The Lens** — Theater 6, the beam cutting the water, steam wall
7. **Underwater** — the deep basin, drowned leaf forest, silt, a larva
8. **The Throat** — the storm grate, endgame, cathedral scale
9. **Vehicle orthographic sheets** — all seven unit classes × both factions
10. **Material studies** — riveted tin vs. lacquered chitin, close enough to see the surface story

---

## 12. Build status

First procedural pass is complete and exported to glTF: both faction haulers, the Combine
fighter, tank and motorcycle, and a nine-piece found-object prop kit — ~10.5k tris total. Every
model is generated from Python (`blender/`), so silhouettes stay editable by changing a number
rather than by re-sculpting.

Still unbuilt from §6: bomber, submarine, combat engineer, artillery, AA gunner, rescue coxswain,
and the crews. Still unbuilt from §4: the theater environment kits.
