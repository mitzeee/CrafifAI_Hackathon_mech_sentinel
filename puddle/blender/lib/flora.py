"""
Wetland flora kit -- low-poly, faceted, single-sided blades.

The reference frame's vegetation is big angular planes, not billboards: a
shrub is a dozen chunky leaf-blades fanned around a point, a tuft of grass is
six tapered triangles. Blades are single-sided faces (Cycles renders both
sides) which keeps a dense bank cheap.

Everything is built into ONE bmesh per clump rather than joining objects --
a bank with 400 plants is otherwise minutes of bpy.ops.
"""
import bmesh
import math
import random
import bpy
from mathutils import Vector, Matrix
import kit

TAU = math.pi * 2


def _blade(bm, M, length, width, droop=0.35, mi=0):
    """One leaf: 4 verts, 1 face, bent along its length."""
    pts = [(0, 0, 0),
           (width * 0.5, length * 0.34, -droop * 0.12 * length),
           (0, length, -droop * length),
           (-width * 0.5, length * 0.34, -droop * 0.12 * length)]
    vs = [bm.verts.new(M @ Vector(p)) for p in pts]
    f = bm.faces.new(vs)
    f.material_index = mi
    return f


def _clump(name, mats, count, height, width_ratio, tilt_lo, tilt_hi,
           droop, seed, radius=0.0, rise=0.0, hvar=0.42):
    rng = random.Random(seed)
    bm = bmesh.new()
    for i in range(count):
        a = rng.uniform(0, TAU)
        tilt = rng.uniform(tilt_lo, tilt_hi)
        L = height * rng.uniform(1.0 - hvar, 1.0)
        W = L * width_ratio * rng.uniform(0.75, 1.3)
        off = Vector((math.cos(a) * radius * rng.uniform(0, 1),
                      math.sin(a) * radius * rng.uniform(0, 1), rise))
        # +tilt, not -tilt: rotating a +Y blade by -tilt about X drives it
        # DOWN through the terrain, which is why clumps rendered as bare mud.
        M = (Matrix.Translation(off)
             @ Matrix.Rotation(a, 4, 'Z')
             @ Matrix.Rotation(tilt, 4, 'X'))
        _blade(bm, M, L, W, droop, mi=rng.randrange(len(mats)))
    ob = kit._finish(name, bm, None, weld=0)
    for m in mats:
        ob.data.materials.append(m)
    return kit.flat(ob)


# --------------------------------------------------------------- palette ---

def pal():
    return dict(
        olive=kit.mat('fl_olive', '#6C7E2E', roughness=0.82),
        olive_dk=kit.mat('fl_olive_dk', '#41551E', roughness=0.85),
        green=kit.mat('fl_green', '#55742C', roughness=0.80),
        green_dk=kit.mat('fl_green_dk', '#2E4419', roughness=0.86),
        ochre=kit.mat('fl_ochre', '#C5811A', roughness=0.84),
        ochre_dk=kit.mat('fl_ochre_dk', '#8E6526', roughness=0.86),
        gold=kit.mat('fl_gold', '#B39433', roughness=0.85),
        dry=kit.mat('fl_dry', '#8A7A46', roughness=0.88),
        rust=kit.mat('fl_rust', '#8C5A2A', roughness=0.86),
        moss=kit.mat('fl_moss', '#4F6B22', roughness=0.90),
        moss_lt=kit.mat('fl_moss_lt', '#74864A', roughness=0.90),
        bark=kit.mat('fl_bark', '#5A4A38', roughness=0.92),
        birch=kit.mat('fl_birch', '#C3C0B4', roughness=0.84),
        pad=kit.mat('fl_pad', '#456B26', roughness=0.62),
        cattail=kit.mat('fl_cattail', '#6B4A2E', roughness=0.84),
        algae=kit.mat('fl_algae', '#5E6B36', roughness=0.70),
    )


# ----------------------------------------------------------------- plants ---

def shrub(name, P, height=3.4, seed=0, autumn=0.0):
    """Big angular fronds fanned round a point -- the reference's signature."""
    greens = [P['olive'], P['green'], P['olive_dk'], P['green_dk']]
    autumns = [P['ochre'], P['gold'], P['rust'], P['ochre_dk']]
    n = max(1, int(4 * (1 - autumn)))
    mats = greens[:n] + autumns[:4 - n] if autumn > 0 else greens
    return _clump(name, mats, count=18, height=height, width_ratio=0.34,
                  tilt_lo=0.45, tilt_hi=1.35, droop=0.42, seed=seed,
                  radius=height * 0.16, rise=height * 0.10)


def grass(name, P, height=1.5, seed=0, autumn=0.0):
    mats = ([P['dry'], P['gold'], P['ochre']] if autumn > 0.5
            else [P['olive'], P['green'], P['gold']])
    return _clump(name, mats, count=11, height=height, width_ratio=0.21,
                  tilt_lo=0.95, tilt_hi=1.45, droop=0.34, seed=seed,
                  radius=height * 0.20)


def sedge(name, P, height=4.2, seed=0, autumn=0.0):
    """Tall marsh blades -- these stand IN the water at the margin."""
    mats = ([P['dry'], P['gold']] if autumn > 0.5
            else [P['green'], P['olive'], P['green_dk']])
    # Blades must be CHUNKY to read at distance; at 0.075 ratio a sedge was
    # 8 units wide for 46 tall and vanished into the bank.
    return _clump(name, mats, count=15, height=height, width_ratio=0.155,
                  tilt_lo=1.02, tilt_hi=1.46, droop=0.22, seed=seed,
                  radius=height * 0.15)


def cattail(name, P, height=6.0, seed=0):
    ob = sedge(name + '_blades', P, height=height, seed=seed)
    rng = random.Random(seed + 91)
    parts = [ob]
    for i in range(rng.randrange(2, 4)):
        a = rng.uniform(0, TAU)
        x, y = math.cos(a) * height * 0.06, math.sin(a) * height * 0.06
        h = height * rng.uniform(0.85, 1.05)
        # stem/head radii scale with height -- fixed 0.055 gave hairlines
        parts.append(kit.cyl(f'{name}_stem{i}', h * 0.011, h, sides=5,
                             loc=(x, y, h / 2), material=P['green_dk']))
        parts.append(kit.cyl(f'{name}_head{i}', h * 0.038, h * 0.17, sides=7,
                             loc=(x, y, h * 0.90), material=P['cattail']))
    return kit.flat(kit.join(name, parts))


def fern(name, P, height=2.0, seed=0):
    return _clump(name, [P['green_dk'], P['green'], P['moss']], count=12,
                  height=height, width_ratio=0.34, tilt_lo=0.62, tilt_hi=1.22,
                  droop=0.62, seed=seed, radius=height * 0.16)


def moss_rock(name, P, r=3.0, seed=0):
    N_pebble = kit.mat('fl_stone', '#8E8D85', roughness=0.92)
    rk = kit.rock(f'{name}_r', r, seed=seed, squash=0.62, subdiv=1,
                  material=N_pebble)
    cap = kit.rock(f'{name}_m', r * 0.82, seed=seed + 7, squash=0.30,
                   subdiv=1, loc=(0, 0, r * 0.30), material=P['moss'])
    return kit.flat(kit.join(name, [rk, cap]))


def lily_pad(name, P, r=1.6, seed=0):
    rng = random.Random(seed)
    pts = []
    n = 9
    for i in range(n):
        a = TAU * i / n
        rr = r * (1.0 if i else 0.35) * rng.uniform(0.85, 1.12)
        pts.append((math.cos(a) * rr, math.sin(a) * rr))
    return kit.flat(kit.plate(name, pts, 0.06, material=P['pad']))


def log(name, P, length=14.0, r=1.1, seed=0):
    parts = [kit.cyl(f'{name}_b', r, length, sides=9, rot=(math.pi / 2, 0, 0),
                     loc=(0, 0, r), material=P['bark'])]
    rng = random.Random(seed)
    for i in range(4):
        parts.append(kit.rock(f'{name}_m{i}', r * rng.uniform(0.4, 0.7),
                              seed=seed + i, squash=0.3, subdiv=1,
                              loc=(rng.uniform(-0.4, 0.4),
                                   rng.uniform(-length / 2.4, length / 2.4),
                                   r * 1.35), material=P['moss_lt']))
    return kit.flat(kit.join(name, parts))


def algae_mat(name, P, r=7.0, seed=0):
    rng = random.Random(seed)
    pts = []
    n = 12
    for i in range(n):
        a = TAU * i / n
        rr = r * rng.uniform(0.6, 1.15)
        pts.append((math.cos(a) * rr, math.sin(a) * rr))
    return kit.flat(kit.plate(name, pts, 0.05, material=P['algae']))


# -------------------------------------------------------------- scatter ----

def _seg_dist(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / L2))
    return math.hypot(px - (ax + vx * t), py - (ay + vy * t))


def bank(terrain_z, water_level, count=340, r_in=40, r_out=175, seed=5,
         autumn=0.0, P=None, avoid=None, corridor=None):
    """
    Dress the bank. Plants pick themselves by how far above the waterline they
    sit: sedge and cattail wade at the margin, grass and shrub hold the dry
    ground, ferns and moss take the damp band behind them.

    `avoid` is (x, y, radius): keep this disc clear of planting. Plants here
    are big, so a camera dropped in the bank ends up INSIDE a shrub and
    renders a black frame.

    `corridor` is (ax, ay, bx, by, width): keep a lane clear along a segment.
    This is how supply routes get cut through the reed belt -- the land
    missions need a track, and the track is the mission.

    Returns instanced copies -- linked duplicates share mesh data, so 340
    plants cost 8 meshes.
    """
    # SCALE: one unit is ~4 mm (the hauler is 30 units for a ~12 cm can), so
    # literal marsh growth would be 100-250 units and swallow every camera.
    # These are compressed for readability -- big enough that a reed stand is
    # a forest the ships sail through, small enough to frame a shot in.
    P = P or pal()
    rng = random.Random(seed)
    protos = {
        'sedge': [sedge(f'_p_sedge{i}', P, 30 + i * 20, seed=i * 3, autumn=autumn)
                  for i in range(3)],
        'cattail': [cattail(f'_p_cat{i}', P, 66 + i * 26, seed=40 + i)
                    for i in range(2)],
        'grass': [grass(f'_p_grass{i}', P, 12 + i * 8, seed=70 + i, autumn=autumn)
                  for i in range(3)],
        'shrub': [shrub(f'_p_shrub{i}', P, 34 + i * 20, seed=100 + i, autumn=autumn)
                  for i in range(3)],
        'fern': [fern(f'_p_fern{i}', P, 17 + i * 10, seed=130 + i)
                 for i in range(2)],
        'rock': [moss_rock(f'_p_rock{i}', P, 4 + i * 7, seed=160 + i)
                 for i in range(3)],
    }
    for group in protos.values():
        for o in group:
            o.hide_render = True
            o.location = (0, 0, -900)

    out = []
    for i in range(count):
        a = rng.uniform(0, TAU)
        rr = rng.uniform(r_in, r_out)
        x, y = math.cos(a) * rr, math.sin(a) * rr
        if avoid and math.hypot(x - avoid[0], y - avoid[1]) < avoid[2]:
            continue
        if corridor and _seg_dist(x, y, *corridor[:4]) < corridor[4]:
            continue
        z = terrain_z(x, y)
        d = z - water_level
        if d < -5.0:
            continue                                  # too deep to root
        if d < 1.2:
            kind = 'sedge' if rng.random() < 0.70 else 'cattail'
        elif d < 3.5:
            kind = rng.choice(['sedge', 'grass', 'fern', 'rock'])
        else:
            kind = rng.choice(['grass', 'shrub', 'shrub', 'grass', 'fern',
                               'rock'])
        proto = rng.choice(protos[kind])
        ob = bpy.data.objects.new(f'{kind}_{i}', proto.data)
        bpy.context.collection.objects.link(ob)
        ob.location = (x, y, z - 0.10)
        ob.rotation_euler = (rng.uniform(-0.05, 0.05), rng.uniform(-0.05, 0.05),
                             rng.uniform(0, TAU))
        s = rng.uniform(0.75, 1.35)
        ob.scale = (s, s, s)
        out.append(ob)
    return out
