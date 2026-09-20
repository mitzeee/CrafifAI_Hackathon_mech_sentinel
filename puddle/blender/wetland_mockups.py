"""
Wetland mock-ups. The real setting: a big, deep pool in marsh -- vibrant
shrubs, sedge, grass and mossy rock, not a car park.

Scale note that drives everything here: the hauler is 30 units for a ~12 cm
can, so one unit is roughly 4 mm and real marsh growth is ENORMOUS. A sedge
blade is 40-120 units; a reed stand is a forest the ships sail through.

    python3 wetland_mockups.py /out [shot ...]
"""
import math
import os
import subprocess
import sys

R = math.radians
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = {}


def shot(fn):
    SHOTS[fn.__name__] = fn
    return fn


def _base(s, fl, level, autumn, plants=300, seed=3, water='#2B3A31',
          avoid=None, corridor=None):
    P = fl.pal()
    s.wetland(water_level=level, autumn=autumn, plants=plants, seed=seed,
              flora_mod=fl, avoid=avoid, corridor=corridor)
    s.marsh_water(level=level, color=water)
    return P


def _reed_screen(fl, P, pts, height=150, seed=0, autumn=0.0):
    """
    A curtain of sedge right in front of the lens.

    Cameras live in the DEEP CENTRE of the pool, radius < 45. Plants root
    wherever the water is shallower than ~5 units, which puts the reed belt
    at radius 60-175; a camera anywhere in that belt ends up inside a leaf.

    A foreground screen therefore has to be placed by hand, with a deliberate
    gap in the middle -- blades at the edges of frame, subject visible through
    the centre.
    """
    out = []
    for i, (x, y, sc) in enumerate(pts):
        c = fl.sedge(f'screen_{i}', P, height * sc, seed=seed + i * 5,
                     autumn=autumn)
        c.location = (x, y, -6)
        c.rotation_euler = (0, 0, (i * 1.7) % math.tau)
        out.append(c)
    return out


# ---------------------------------------------------------------- W1 ------
@shot
def wetland_dawn(s, kit, render, fl):
    """Open water at first light. The pool is big and deep; the reeds are a
    coastline."""
    P = _base(s, fl, 0.0, autumn=0.15, plants=340, avoid=(28, -44, 44))
    s.floaters(fl, P, 0.0, count=34, r_in=34, r_out=98)
    yaw = R(-38)
    s.place('hauler_combine', loc=(-16, 10, 0), rot_z=yaw)
    s.wake((-16, 10), yaw, length=58)
    s.light('dawn')
    s.haze(0.0011, color='#AEB8B4')
    render.camera_at((28, -44, 17), (-26, 28, 7), lens=42)


# ---------------------------------------------------------------- W2 ------
@shot
def through_the_reeds(s, kit, render, fl):
    """Low, hidden, watching from inside the reed bed. Foreground goes soft."""
    P = _base(s, fl, 0.0, autumn=0.2, plants=300, avoid=(6, -52, 44))
    s.floaters(fl, P, 0.0, count=26, r_in=30, r_out=90)
    yaw = R(66)
    s.place('hauler_combine', loc=(6, 34, 0), rot_z=yaw)
    s.wake((6, 34), yaw, length=50)
    # gap left in the middle so the subject reads through the screen
    _reed_screen(fl, P, [(-46, -26, 1.2), (-32, -22, 0.95), (-20, -28, 1.1),
                         (20, -27, 1.05), (32, -22, 1.25), (46, -29, 0.9)],
                 height=30, seed=11, autumn=0.2)
    s.light('dawn')
    s.haze(0.0012, color='#B4BCB6')
    cam = render.camera_at((6, -52, 10), (2, 44, 6), lens=50)
    render.dof(cam, distance=96, fstop=2.0)


# ---------------------------------------------------------------- W3 ------
@shot
def reed_channel(s, kit, render, fl):
    """Threading a channel between two reed stands -- a canyon of grass."""
    P = _base(s, fl, 0.0, autumn=0.1, plants=200, seed=5, avoid=(16, -196, 130))
    s.floaters(fl, P, 0.0, count=18, r_in=26, r_out=70)
    for side in (-1, 1):
        for i in range(9):
            c = fl.sedge(f'ch_{side}_{i}', P, 58 + (i % 3) * 28,
                         seed=200 + side * 13 + i)
            c.location = (side * (48 + (i % 2) * 14), -70 + i * 20, -3)
            c.rotation_euler = (0, 0, i * 0.9)
        for i in range(4):
            c = fl.cattail(f'cc_{side}_{i}', P, 92 + i * 20, seed=300 + i)
            c.location = (side * (62 + (i % 2) * 10), -50 + i * 38, -3)
    yaw = R(2)
    s.place('hauler_combine', loc=(-2, -14, 0), rot_z=yaw)
    s.wake((-2, -14), yaw, length=52)
    s.light('noon')
    s.haze(0.0014, color='#AFB9A8')
    render.camera_at((14, -124, 38), (0, 4, 13), lens=44)


# ---------------------------------------------------------------- W4 ------
@shot
def the_heron(s, kit, render, fl):
    """
    Macro event, wetland edition. A heron wades in. Neither tribe controls it,
    it cannot be fought, and you get a few seconds of shadow as warning.
    """
    P = _base(s, fl, 0.0, autumn=0.15, plants=260, avoid=(-38, -46, 44))
    s.floaters(fl, P, 0.0, count=22, r_in=30, r_out=92)
    leg = kit.mat('_heron_leg', '#9A8C5E', roughness=0.72)
    dark = kit.mat('_heron_dark', '#4A4638', roughness=0.80)
    for i, (x, y, r0, r1) in enumerate(((22, 40, 6.5, 4.2), (52, 66, 6.0, 3.9))):
        kit.cyl(f'leg_{i}', r0, 400, sides=9, radius_top=r1,
                loc=(x, y, 196), material=leg)
        for t in range(3):
            a = R(-40 + t * 40)
            kit.tube(f'toe_{i}_{t}', [(x, y, -2), (x + math.sin(a) * 16,
                                                   y + math.cos(a) * 16, -5)],
                     2.4, sides=5, material=dark)
    for k in range(4):                     # impact rings
        kit.tube(f"ring_{k}", kit.arc((28, 46, 0), 16 + k * 13, 0, math.tau,
                                    steps=26, z=0.25),
                 0.9 + k * 0.3, sides=4,
                 material=kit.mat('_ring', '#AEB6AC', roughness=0.6, alpha=0.30))
    kit.plate('heron_shadow', [(-70, -40), (150, -70), (170, 130), (-40, 150)],
              0.3, loc=(0, 0, 0.12),
              material=kit.mat('_hshadow', '#20241F', roughness=0.95, alpha=0.42))
    yaw = R(-128)
    s.place('hauler_combine', loc=(-18, -6, 0), rot_z=yaw, roll=R(6))
    s.wake((-18, -6), yaw, length=44)
    s.light('noon')
    s.haze(0.0011, color='#B2BAB2')
    render.camera_at((-38, -46, 20), (14, 30, 46), lens=38)


# ---------------------------------------------------------------- W5 ------
@shot
def autumn_drying(s, kit, render, fl):
    """Late season. The pool has pulled back, the marsh has gone to ochre,
    and the Ark is aground in its own tide marks."""
    P = _base(s, fl, -8.5, autumn=0.95, plants=380, water='#36402E',
              avoid=(26, -30, 40))
    s.floaters(fl, P, -8.5, count=10, r_in=20, r_out=46)
    s.place('hauler_combine', loc=(-18, 6, -7.6), rot_z=R(-54), pitch=R(7),
            roll=R(-10))
    s.place('tank_combine', loc=(44, -44, -2.0), rot_z=R(-150), scale=1.5)
    s.place('bike_combine', loc=(20, -56, -1.0), rot_z=R(150), scale=1.5)
    s.light('drying')
    s.haze(0.0016, color='#CCBB98')
    render.camera_at((26, -30, 13), (-12, -2, -5), lens=44)


# ---------------------------------------------------------------- W6 ------
@shot
def marsh_standoff(s, kit, render, fl):
    """Both haulers, one light. Combine = straight lines and smoke;
    Reedfolk = curves and glow, and they look like they belong here."""
    P = _base(s, fl, 0.0, autumn=0.2, plants=300, seed=9, avoid=(34, -48, 44))
    s.floaters(fl, P, 0.0, count=30, r_in=28, r_out=92)
    s.place('hauler_combine', loc=(-26, 8, 0), rot_z=R(38))
    s.place('hauler_reedfolk', loc=(20, 34, 0), rot_z=R(214))
    s.light('noon')
    s.haze(0.0013, color='#AFB9B2')
    render.camera_at((24, -34, 16), (-4, 20, 3), lens=42)


# ---------------------------------------------------------------- W7 ------
@shot
def bank_assault(s, kit, render, fl):
    """Act III shore war: armour working a mossy bank under the reed line."""
    P = _base(s, fl, -5.0, autumn=0.45, plants=340, seed=13,
              avoid=(16, -30, 42))
    s.floaters(fl, P, -5.0, count=14, r_in=24, r_out=62)
    s.place('tank_combine', loc=(-18, -62, 1.0), rot_z=R(16), scale=2.0)
    s.place('bike_combine', loc=(26, -74, 1.4), rot_z=R(-32), scale=2.0)
    yaw = R(104)
    s.place('hauler_combine', loc=(-58, -6, -5.0), rot_z=yaw)
    s.wake((-58, -6), yaw, length=44, level=-5.0)
    s.place('fighter_combine', loc=(34, -26, 34), rot_z=R(-64), pitch=R(-7),
            roll=R(26), scale=2.2)
    s.light('noon')
    s.haze(0.0015, color='#B3B9A6')
    render.camera_at((16, -30, 17), (-6, -56, 4), lens=46)


# ---------------------------------------------------------------- W8 ------
@shot
def bridge_through_reeds(s, kit, render, fl):
    """From the Ark's bridge, reed wall to starboard, contact fine on the bow."""
    P = _base(s, fl, 0.0, autumn=0.2, plants=320, seed=17, avoid=(0, 0, 70))
    s.floaters(fl, P, 0.0, count=28, r_in=32, r_out=96)
    s.place('hauler_combine', loc=(0, 0, 0))
    s.place('hauler_reedfolk', loc=(26, 96, 0), rot_z=R(204))
    for i in range(7):
        c = fl.sedge(f'sb_{i}', P, 58 + (i % 3) * 24, seed=400 + i, autumn=0.2)
        c.location = (40 + (i % 2) * 12, 6 + i * 20, -4)
    s.light('dawn')
    s.haze(0.0015, color='#AFB8B4')
    render.camera_at((0, -7.2, 6.6), (0, 70, 4), lens=30)


def enemy_base(kit, palette, x, y, z, rot=0.0, scale=1.0):
    """
    A strategic target on the far bank: fuel drums, a pump house, a slipway
    and a mast. This is what the bomber is for -- things the enemy cannot move.
    """
    C = palette.combine()
    N = palette.neutral()
    R2 = palette.reedfolk()
    out = []
    c, s2 = math.cos(rot), math.sin(rot)

    def at(lx, ly, lz):
        return (x + lx * c - ly * s2, y + lx * s2 + ly * c, z + lz)

    for i, (lx, ly, r) in enumerate(((-9, 4, 3.4), (-2, 7, 3.0), (5, 3, 3.6))):
        out.append(kit.crimped_disc(f'eb_tank{i}', r * scale, 4.2 * scale,
                                    flutes=15, flute_depth=0.09,
                                    loc=at(lx * scale, ly * scale, 2.1 * scale),
                                    material=R2['amber'] if i % 2 else C['rust']))
    out.append(kit.box('eb_shed', (14 * scale, 9 * scale, 5.5 * scale),
                       loc=at(8 * scale, -7 * scale, 2.7 * scale),
                       rot=(0, 0, rot), material=R2['honey']))
    out.append(kit.box('eb_roof', (15.5 * scale, 10 * scale, 0.9 * scale),
                       loc=at(8 * scale, -7 * scale, 5.8 * scale),
                       rot=(0, 0, rot), material=R2['wax_green']))
    out.append(kit.tube('eb_pipe', [at(-12 * scale, 2 * scale, 4.0 * scale),
                                    at(2 * scale, -4 * scale, 4.0 * scale),
                                    at(9 * scale, -6 * scale, 4.6 * scale)],
                        0.9 * scale, sides=6, material=N['zinc']))
    out.append(kit.tube('eb_mast', [at(-14 * scale, -9 * scale, 0),
                                    at(-14 * scale, -9 * scale, 22 * scale)],
                        0.6 * scale, sides=5, taper=lambda t: 1 - 0.5 * t,
                        material=R2['bark']))
    for i in range(3):                      # slipway planks down to the water
        out.append(kit.box(f'eb_slip{i}', (11 * scale, 2.2 * scale, 0.5 * scale),
                           loc=at(16 * scale, (2 + i * 3) * scale,
                                  (0.6 - i * 0.5) * scale),
                           rot=(0, 0, rot), material=N['match_wood']))
    return out


# ======================= MISSIONS ==========================================
# Each vehicle is its own mission type with its own verb (design doc S6).

@shot
def m_supply_land(s, kit, render, fl):
    """LAND LOGISTICS. Truck and rickshaw running rations and raw material up
    the bank track at dusk. No guns. The mission is route, timing and not
    being seen."""
    P = _base(s, fl, 0.0, autumn=0.35, plants=300, seed=21,
              avoid=(46, -164, 46), corridor=(-40, -158, 72, -66, 17))
    s.mud_track((-40, -158), (72, -66), width=12)
    s.place('truck_combine', loc=(16, -112, 2.6), rot_z=R(39), scale=2.4)
    s.place('rickshaw_combine', loc=(-10, -134, 2.4), rot_z=R(39), scale=2.4)
    s.light('dusk')
    s.haze(0.0005, color='#9E8A78')
    render.camera_at((42, -152, 15), (4, -116, 5), lens=46)


@shot
def m_cargo_water(s, kit, render, fl):
    """WATER LOGISTICS. The hauler running dark through a reed pass, loaded
    and slow. Same job as the truck, different medium and a worse escape."""
    P = _base(s, fl, 0.0, autumn=0.15, plants=210, seed=5,
              avoid=(14, -124, 70))
    s.floaters(fl, P, 0.0, count=20, r_in=26, r_out=72)
    for side in (-1, 1):
        for i in range(9):
            c = fl.sedge(f'ch_{side}_{i}', P, 58 + (i % 3) * 28,
                         seed=200 + side * 13 + i)
            c.location = (side * (48 + (i % 2) * 14), -70 + i * 20, -3)
            c.rotation_euler = (0, 0, i * 0.9)
        for i in range(4):
            c = fl.cattail(f'cc_{side}_{i}', P, 92 + i * 20, seed=300 + i)
            c.location = (side * (62 + (i % 2) * 10), -50 + i * 38, -3)
    yaw = R(2)
    s.place('hauler_combine', loc=(-2, -18, 0), rot_z=yaw)
    s.wake((-2, -18), yaw, length=46)
    s.light('dawn')
    s.haze(0.0010, color='#9FB0A8')
    render.camera_at((14, -124, 38), (0, 4, 13), lens=44)


@shot
def m_recon_sub(s, kit, render, fl):
    """RECONNAISSANCE. Periscope up off the enemy slipway, counting hulls.
    Firing ends the mission; the win condition is getting home unseen."""
    P = _base(s, fl, 0.0, autumn=0.2, plants=280, seed=33, avoid=(18, -40, 44))
    s.floaters(fl, P, 0.0, count=24, r_in=26, r_out=88)
    enemy_base(kit, __import__('palette'), 26, 104, 1.0, rot=R(-18), scale=1.5)
    s.place('hauler_reedfolk', loc=(-16, 78, 0), rot_z=R(196))
    # half-surfaced and close: a recon mission reads as sail-and-periscope,
    # but the hull has to be legible or the shot is just a post in the water
    s.place('sub_combine', loc=(8, 4, -0.7), rot_z=R(12), scale=2.3)
    s.light('noon')
    s.haze(0.0008, color='#A6B4B0')
    render.camera_at((15, -28, 6), (9, 54, 9), lens=48)


@shot
def m_strike_bomber(s, kit, render, fl):
    """STRATEGIC STRIKE. Over the far bank with the bay open. Slow, heavy,
    and dead without escort."""
    P = _base(s, fl, 0.0, autumn=0.25, plants=300, seed=41, avoid=(-6, -70, 46))
    s.floaters(fl, P, 0.0, count=18, r_in=30, r_out=86)
    enemy_base(kit, __import__('palette'), 4, 112, 1.0, rot=R(8), scale=1.9)
    s.place('bomber_combine', loc=(2, 26, 46), rot_z=R(4), pitch=R(-4),
            roll=R(9), scale=2.6)
    s.place('fighter_combine', loc=(-30, 52, 60), rot_z=R(-12), roll=R(22),
            scale=2.0)
    s.light('noon')
    s.haze(0.0010, color='#A8B4BA')
    render.camera_at((-26, -66, 60), (4, 66, 34), lens=46)


@shot
def m_intercept_fighter(s, kit, render, fl):
    """AIR INTERCEPT. Break up the enemy flight before it reaches the convoy.
    Fast, fragile, and fought a few inches above the water."""
    P = _base(s, fl, 0.0, autumn=0.15, plants=260, seed=47, avoid=(-20, -58, 46))
    s.floaters(fl, P, 0.0, count=22, r_in=28, r_out=90)
    s.place('fighter_combine', loc=(-8, 6, 26), rot_z=R(28), pitch=R(6),
            roll=R(-38), scale=2.6)
    s.place('fighter_combine', loc=(34, 46, 34), rot_z=R(-142), roll=R(30),
            scale=2.2)
    s.place('fighter_combine', loc=(52, 66, 44), rot_z=R(-150), roll=R(18),
            scale=2.0)
    s.place('hauler_reedfolk', loc=(22, 86, 0), rot_z=R(200))
    s.light('noon')
    s.haze(0.0009, color='#A8B6BC')
    render.camera_at((-20, -58, 30), (6, 40, 30), lens=44)


@shot
def m_armour_push(s, kit, render, fl):
    """ARMOUR. Taking and holding ground on the bank so the convoys can run."""
    P = _base(s, fl, -5.0, autumn=0.45, plants=320, seed=13,
              avoid=(16, -30, 42))
    s.floaters(fl, P, -5.0, count=14, r_in=24, r_out=62)
    s.place('tank_combine', loc=(-18, -58, 1.0), rot_z=R(14), scale=2.2)
    s.place('bike_combine', loc=(22, -70, 1.4), rot_z=R(-34), scale=2.2)
    yaw = R(104)
    s.place('hauler_combine', loc=(-58, -6, -5.0), rot_z=yaw)
    s.wake((-58, -6), yaw, length=44, level=-5.0)
    s.light('noon')
    s.haze(0.0010, color='#A6AE98')
    render.camera_at((16, -30, 17), (-6, -56, 4), lens=46)


@shot
def m_rain_run(s, kit, render, fl):
    """
    WEATHER. Rain does not drain the pool -- it cuts visibility, grounds the
    aircraft and hides a convoy. Season is flavour and complexity, not a clock.
    """
    P = _base(s, fl, 0.0, autumn=0.3, plants=280, seed=53, avoid=(24, -46, 44),
              water='#1E2A26')
    s.floaters(fl, P, 0.0, count=20, r_in=28, r_out=84)
    yaw = R(-24)
    s.place('hauler_combine', loc=(-14, 18, 0), rot_z=yaw)
    s.wake((-14, 18), yaw, length=44)
    s.rain(count=1500, bounds=150, top=120, rings=60)
    s.light('rain')
    s.haze(0.0030, color='#8E9AA0', size=300)
    render.camera_at((24, -46, 16), (-12, 22, 8), lens=48)


RES = (1280, 720)


def run(name, outdir, samples=30):
    code = f'''
import sys, math; sys.path.insert(0,"lib"); sys.path.insert(0,"assets"); sys.path.insert(0,".")
import kit, scene, render, flora, wetland_mockups as W
kit.reset()
W.SHOTS["{name}"](scene, kit, render, flora)
render.grade()
render.shot(r"{outdir}/{name}.png", res={RES}, samples={samples})
print("DONE", "{name}", kit.tris())
'''
    r = subprocess.run([sys.executable, '-c', code], cwd=HERE,
                       capture_output=True, text=True)
    ok = [l for l in r.stdout.splitlines() if l.startswith('DONE')]
    print('  ' + ok[0] if ok else f'  FAIL {name}\n    ' +
          '\n    '.join(r.stderr.strip().splitlines()[-5:]))


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for t in (sys.argv[2:] or list(SHOTS)):
        run(t, out)
