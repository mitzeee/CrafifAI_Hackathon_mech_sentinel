"""
Scene kit for mock-ups: basin terrain, faceted water, time-of-day light.

The important trick here is that the SHORELINE IS COMPUTED, not painted. Bands
are assigned per face from each face's height relative to `water_level`, so
dropping the level genuinely moves the waterline, exposes the tide marks and
surfaces the shoals -- the design doc's core mechanic (section 4), visible in
a still frame.
"""
import bpy
import bmesh
import math
import random
from mathutils import Vector, Matrix
import kit
import palette


def _basin_z(x, y, radius, depth, rng_seed=3):
    """Shallow bowl + ridges + grit. A puddle, not a crater."""
    r = math.hypot(x, y) / radius
    bowl = -depth * max(0.0, 1.0 - r * r) ** 1.35
    n = (math.sin(x * 0.083 + rng_seed) * math.cos(y * 0.071 - rng_seed) * 0.55
         + math.sin(x * 0.031 - y * 0.027) * 0.9
         + math.sin(x * 0.21 + y * 0.18) * 0.16)
    # No raised rim: a parking-lot puddle is a shallow depression in FLAT
    # tarmac. A lip turns the horizon into a crater wall and eats the sky.
    return bowl + n


def basin(size=300, cell=2.8, radius=98, depth=6.0, water_level=0.0, seed=3):
    """
    Terrain with waterline-relative material bands:
      0 silt (submerged)  1 wet  2 damp  3 tide grit  4 dry tarmac
    """
    # Dedicated low-contrast shore ramp. Reusing the prop palette put a bright
    # pebble tone against dark tarmac and the tide line read as a zigzag ribbon.
    mats = [kit.mat('_sh_silt', '#443F33', roughness=0.95),
            kit.mat('_sh_wet', '#32342E', roughness=0.62),
            kit.mat('_sh_damp', '#42433B', roughness=0.86),
            kit.mat('_sh_tide1', '#565549', roughness=0.93),
            kit.mat('_sh_tide2', '#68655A', roughness=0.94),
            kit.mat('_sh_dry', '#55564F', roughness=0.95)]
    n = int(size / cell)
    bm = bmesh.new()
    grid = {}
    for i in range(n + 1):
        for j in range(n + 1):
            x = -size / 2 + i * cell
            y = -size / 2 + j * cell
            grid[(i, j)] = bm.verts.new((x, y, _basin_z(x, y, radius, depth, seed)))
    faces = []
    for i in range(n):
        for j in range(n):
            faces.append(bm.faces.new((grid[(i, j)], grid[(i + 1, j)],
                                       grid[(i + 1, j + 1)], grid[(i, j + 1)])))
    ob = kit._finish('terrain', bm, None, weld=0)
    for m in mats:
        ob.data.materials.append(m)
    for f in ob.data.polygons:
        z = sum(ob.data.vertices[v].co.z for v in f.vertices) / len(f.vertices)
        d = z - water_level
        f.material_index = (0 if d < -0.25 else 1 if d < 0.30 else
                            2 if d < 0.85 else 3 if d < 1.45 else
                            4 if d < 2.10 else 5)
    kit.flat(ob)
    return ob


def water(size=320, cell=2.4, level=0.0, amp=0.22, choppy=1.0, seed=1):
    """
    Faceted Gerstner-ish surface. Small amplitude, high frequency -- miniature
    water moves fast and small (art bible 3.3); slow ocean swell instantly
    reads as full scale and kills the illusion.
    """
    N = palette.neutral()
    m = kit.mat('_water_surface', '#38463F', metallic=0.0, roughness=0.09)
    n = int(size / cell)
    bm = bmesh.new()
    grid = {}
    for i in range(n + 1):
        for j in range(n + 1):
            x = -size / 2 + i * cell
            y = -size / 2 + j * cell
            h = (math.sin(x * 0.31 + y * 0.19) * 0.42
                 + math.sin(x * 0.13 - y * 0.37) * 0.30
                 + math.sin(x * 0.67 + y * 0.58 + seed) * 0.22
                 + math.sin(x * 1.05 - y * 0.91 + seed * 2) * 0.12)
            grid[(i, j)] = bm.verts.new((x, y, level + h * amp * choppy))
    for i in range(n):
        for j in range(n):
            bm.faces.new((grid[(i, j)], grid[(i + 1, j)],
                          grid[(i + 1, j + 1)], grid[(i, j + 1)]))
    ob = kit._finish('water', bm, m, weld=0)
    kit.flat(ob)
    return ob


def wake(origin, rot_z, length=52, spread=0.30, level=0.0, width=2.0):
    """
    A V wake as flat ribbons ON the surface. Tubes stick up and read as
    floating planks; the wake has to lie in the water, not on it. Asset +Y is
    forward, so the wake trails opposite the heading.
    """
    m = kit.mat('_foam', '#B6BCB2', roughness=0.74, alpha=0.17)
    back = (rot_z + math.pi / 2) + math.pi
    out = []
    for side in (-1, 1):
        a = back + side * spread
        ex, ey = math.cos(a), math.sin(a)
        px, py = -ey, ex
        w0, w1 = width * 0.22, width * 1.05
        ox, oy = origin[0], origin[1]
        quad = [(ox + px * w0, oy + py * w0),
                (ox + ex * length + px * w1, oy + ey * length + py * w1),
                (ox + ex * length - px * w1, oy + ey * length - py * w1),
                (ox - px * w0, oy - py * w0)]
        out.append(kit.plate(f'wake_{side}', quad, 0.05,
                             loc=(0, 0, level + 0.07), material=m))
    return kit.join('wake', out)


def macro_backdrop(kind='tyre', dist=330, size=170, color='#2B2A28'):
    """
    The human world looming past the far shore -- rendered huge, dark and
    cropped, never fully in frame (art bible 4.4). A car is terrifying because
    you cannot see all of it.
    """
    m = kit.mat(f'_macro_{kind}', color, roughness=0.95)
    if kind == 'tyre':
        ob = kit.cyl('macro_tyre', size, size * 0.72, sides=22,
                     loc=(60, dist, size * 0.30), rot=(0, math.pi / 2, 0),
                     material=m)
    elif kind == 'curb':
        ob = kit.box('macro_curb', (900, 120, size * 0.9),
                     loc=(0, dist, size * 0.30), material=m)
    else:
        ob = kit.box('macro_slab', (700, 200, size * 1.4),
                     loc=(-120, dist, size * 0.4), material=m)
    return kit.flat(ob)


def scatter(objs_fn, count, radius_in, radius_out, level, above=True, seed=7):
    """Drop debris in a ring band, on the shore or in the shallows."""
    rng = random.Random(seed)
    out = []
    for i in range(count):
        a = rng.uniform(0, math.tau)
        r = rng.uniform(radius_in, radius_out)
        x, y = math.cos(a) * r, math.sin(a) * r
        z = _basin_z(x, y, 98, 6.0, 3)
        if above and z < level:
            continue
        o = objs_fn(i, rng)
        if o is None:
            continue
        o.location = (x, y, z + 0.05)
        o.rotation_euler = (0, 0, rng.uniform(0, math.tau))
        o.scale = (1, 1, 1)
        out.append(o)
    return out


def rocks(count, radius_in, radius_out, level, seed=11, smin=1.2, smax=7.0):
    N = palette.neutral()
    mats = [N['pebble'], N['pebble_pale'], N['grit']]

    def mk(i, rng):
        return kit.rock(f'rk_{i}', rng.uniform(smin, smax), seed=seed * 100 + i,
                        squash=rng.uniform(0.45, 0.72), subdiv=1,
                        material=mats[i % 3])
    return scatter(mk, count, radius_in, radius_out, level, seed=seed)


# --------------------------------------------------------------------------
# light
# --------------------------------------------------------------------------

ACTS = {
    # act        sun colour  energy  sun elev/azim   world colour  strength
    # Key-to-ambient RATIO decides whether a frame reads flat. A big soft
    # world light with a weak sun is exactly what "washed out" looks like,
    # so these run a strong sun against a restrained sky.
    'dawn':     ('#FFC98C', 7.5, (19, 118), '#6E8090', 1.30),
    'noon':     ('#FFF0D2', 11.0, (54, 44), '#8496A4', 1.45),
    'drying':   ('#FFD89A', 11.5, (36, -36), '#A89878', 1.55),
    'dusk':     ('#FF9A54', 12.0, (11, -128), '#5A6478', 1.85),
    'rain':     ('#B9C4CC', 4.6, (34, -70), '#65737C', 2.30),
    'storm':    ('#C6C2D2', 3.6, (22, -80), '#454954', 0.80),
    'grate':    ('#C9D6E0', 7.0, (70, 10), '#49525E', 0.85),
}


def light(act='dawn', target=(0, 0, 0)):
    c, e, (elev, azim), wc, ws = ACTS[act]
    w = bpy.context.scene.world or bpy.data.worlds.new('w')
    bpy.context.scene.world = w
    if not w.node_tree:
        w.use_nodes = True
    bg = w.node_tree.nodes.get('Background')
    bg.inputs[0].default_value = kit.srgb(wc)
    bg.inputs[1].default_value = ws

    d = bpy.data.lights.new('sun', 'SUN')
    d.energy = e
    d.color = kit.srgb(c)[:3]
    d.angle = math.radians(3.5 if act in ('noon', 'drying') else 9.0)
    o = bpy.data.objects.new('sun', d)
    bpy.context.collection.objects.link(o)
    a, el = math.radians(azim), math.radians(elev)
    loc = Vector((math.sin(a) * 200 * math.cos(el), -math.cos(a) * 200 * math.cos(el),
                  math.sin(el) * 200))
    o.location = loc
    o.rotation_euler = (Vector(target) - loc).to_track_quat('-Z', 'Y').to_euler()

    # cool bounce off the sky into the shadows
    f = bpy.data.lights.new('fill', 'AREA')
    f.energy = 70000 if act != 'grate' else 26000
    f.size = 180
    f.color = kit.srgb('#A8BCCC')[:3]
    fo = bpy.data.objects.new('fill', f)
    fo.location = (-140, -110, 90)
    bpy.context.collection.objects.link(fo)
    fo.rotation_euler = (Vector(target) - fo.location).to_track_quat('-Z', 'Y').to_euler()
    return o


def haze(density=0.0006, color='#B9B0A0', size=520):
    """Atmospheric perspective. Cheap at low density, and the depth cue that
    makes a 300-unit puddle read as a sea."""
    m = bpy.data.materials.new('_haze')
    if not m.node_tree:
        m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL':
            nt.nodes.remove(n)
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = kit.srgb(color)
    vol.inputs['Density'].default_value = density
    nt.links.new(vol.outputs[0], nt.nodes['Material Output'].inputs['Volume'])
    cube = kit.box('_haze_vol', (size, size, 150), loc=(0, 0, 40), material=m)
    return cube


def place(name, loc=(0, 0, 0), rot_z=0.0, pitch=0.0, roll=0.0, scale=1.0):
    """
    Drop a SHIPPED asset into the scene by importing its exported .glb, so the
    mock-ups are dressed with the same files Godot will load -- not a separate
    art path that can quietly drift from the real thing.
    """
    import os
    path = os.path.join(kit.GLB_DIR, f'{name}.glb')
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    roots = [o for o in new if o.parent not in new]
    holder = bpy.data.objects.new(f'{name}_at', None)
    bpy.context.collection.objects.link(holder)
    for r in roots:
        r.parent = holder
    holder.location = loc
    holder.rotation_euler = (pitch, roll, rot_z)
    holder.scale = (scale, scale, scale)
    return holder


# ==========================================================================
# WETLAND  -- the real setting: a big, deep pool in marsh, not a car park
# ==========================================================================

def wetland_z(x, y, radius=112, depth=17.0, seed=3):
    """
    Organic outline, not a circle. The pool is deep in the middle and shelves
    out through a reed margin, so the bank reads as marsh rather than kerb.
    """
    a = math.atan2(y, x)
    rmod = radius * (1.0 + 0.19 * math.sin(a * 3 + seed)
                     + 0.12 * math.sin(a * 5 - seed * 2)
                     + 0.07 * math.sin(a * 7 + 1.4))
    r = math.hypot(x, y) / rmod
    bowl = -depth * max(0.0, 1.0 - r * r) ** 1.22
    n = (math.sin(x * 0.041 + seed) * math.cos(y * 0.037 - seed) * 1.5
         + math.sin(x * 0.019 - y * 0.023) * 2.1
         + math.sin(x * 0.11 + y * 0.09) * 0.45)
    hump = 2.6 * max(0.0, r - 1.05)      # ground keeps rising past the margin
    return bowl + n + hump


def wetland(size=420, cell=3.4, radius=112, depth=17.0, water_level=0.0,
            seed=3, autumn=0.0, plants=380, flora_mod=None, avoid=None,
            corridor=None):
    """Terrain + dressed banks. Returns (terrain, plant_objects)."""
    mats = [kit.mat('_wl_deep', '#33372A', roughness=0.95),
            kit.mat('_wl_silt', '#434429', roughness=0.94),
            kit.mat('_wl_mud', '#4A4231', roughness=0.93),
            kit.mat('_wl_peat', '#4E4A34', roughness=0.92),
            kit.mat('_wl_damp', '#5B5540', roughness=0.91),
            kit.mat('_wl_bank', '#6A6146' if autumn < 0.5 else '#6E6142',
                    roughness=0.92)]
    n = int(size / cell)
    bm = bmesh.new()
    grid = {}
    for i in range(n + 1):
        for j in range(n + 1):
            x = -size / 2 + i * cell
            y = -size / 2 + j * cell
            grid[(i, j)] = bm.verts.new((x, y, wetland_z(x, y, radius, depth, seed)))
    for i in range(n):
        for j in range(n):
            bm.faces.new((grid[(i, j)], grid[(i + 1, j)],
                          grid[(i + 1, j + 1)], grid[(i, j + 1)]))
    ob = kit._finish('wetland', bm, None, weld=0)
    for m in mats:
        ob.data.materials.append(m)
    for f in ob.data.polygons:
        z = sum(ob.data.vertices[v].co.z for v in f.vertices) / len(f.vertices)
        d = z - water_level
        f.material_index = (0 if d < -6.0 else 1 if d < -1.8 else
                            2 if d < -0.2 else 3 if d < 0.9 else
                            4 if d < 2.2 else 5)
    kit.flat(ob)

    fl = flora_mod
    ps = []
    if fl:
        ps = fl.bank(lambda x, y: wetland_z(x, y, radius, depth, seed),
                     water_level, count=plants, r_in=radius * 0.36,
                     r_out=radius * 1.55, seed=seed * 7, autumn=autumn,
                     avoid=avoid, corridor=corridor)
    return ob, ps


def marsh_water(size=460, cell=2.6, level=0.0, amp=0.16, seed=1,
                color='#22332A'):
    """
    Deep tannin-stained marsh water: darker and far less transmissive than a
    rain puddle, so the surface carries the sky and the depth reads as depth.
    """
    m = kit.mat('_marsh_water', color, metallic=0.0, roughness=0.07)
    n = int(size / cell)
    bm = bmesh.new()
    grid = {}
    for i in range(n + 1):
        for j in range(n + 1):
            x = -size / 2 + i * cell
            y = -size / 2 + j * cell
            h = (math.sin(x * 0.26 + y * 0.17) * 0.40
                 + math.sin(x * 0.11 - y * 0.31) * 0.32
                 + math.sin(x * 0.58 + y * 0.49 + seed) * 0.18)
            grid[(i, j)] = bm.verts.new((x, y, level + h * amp))
    for i in range(n):
        for j in range(n):
            bm.faces.new((grid[(i, j)], grid[(i + 1, j)],
                          grid[(i + 1, j + 1)], grid[(i, j + 1)]))
    ob = kit._finish('marsh_water', bm, m, weld=0)
    return kit.flat(ob)


def floaters(fl, P, level, count=26, r_in=30, r_out=100, seed=9):
    """Lily pads and algae mats on the open water."""
    import random
    rng = random.Random(seed)
    pads = [fl.lily_pad(f'_pp{i}', P, 9 + i * 7, seed=i) for i in range(3)]
    mats_ = [fl.algae_mat(f'_pa{i}', P, 16 + i * 11, seed=20 + i) for i in range(2)]
    for o in pads + mats_:
        o.hide_render = True
        o.location = (0, 0, -900)
    out = []
    for i in range(count):
        a = rng.uniform(0, math.tau)
        rr = rng.uniform(r_in, r_out)
        proto = rng.choice(pads if rng.random() < 0.7 else mats_)
        ob = bpy.data.objects.new(f'float_{i}', proto.data)
        bpy.context.collection.objects.link(ob)
        ob.location = (math.cos(a) * rr, math.sin(a) * rr, level + 0.07)
        ob.rotation_euler = (0, 0, rng.uniform(0, math.tau))
        s = rng.uniform(0.7, 1.5)
        ob.scale = (s, s, s)
        out.append(ob)
    return out


def mud_track(a, b, width=9.0, terrain_z=None, seed=2):
    """A worn supply route: bare mud with two wheel ruts, laid on the bank."""
    import random
    rng = random.Random(seed)
    tz = terrain_z or (lambda x, y: wetland_z(x, y))
    ax, ay = a
    bx, by = b
    vx, vy = bx - ax, by - ay
    L = math.hypot(vx, vy)
    ux, uy = vx / L, vy / L
    px, py = -uy, ux
    mud = kit.mat('_track_mud', '#584C36', roughness=0.95)
    rut = kit.mat('_track_rut', '#463C2A', roughness=0.94)
    out = []
    steps = max(4, int(L / 12))
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        x0, y0 = ax + vx * t0, ay + vy * t0
        x1, y1 = ax + vx * t1, ay + vy * t1
        w0 = width * rng.uniform(0.85, 1.15)
        w1 = width * rng.uniform(0.85, 1.15)
        z = (tz(x0, y0) + tz(x1, y1)) / 2 + 0.16
        out.append(kit.plate(f'track_{i}', [
            (x0 + px * w0, y0 + py * w0), (x1 + px * w1, y1 + py * w1),
            (x1 - px * w1, y1 - py * w1), (x0 - px * w0, y0 - py * w0)],
            0.22, loc=(0, 0, z), material=mud))
        for side in (-1, 1):
            r = width * 0.34 * side
            out.append(kit.plate(f'rut_{i}_{side}', [
                (x0 + px * (r + 0.9), y0 + py * (r + 0.9)),
                (x1 + px * (r + 0.9), y1 + py * (r + 0.9)),
                (x1 + px * (r - 0.9), y1 + py * (r - 0.9)),
                (x0 + px * (r - 0.9), y0 + py * (r - 0.9))],
                0.10, loc=(0, 0, z + 0.14), material=rut))
    return out


def rain(count=1100, bounds=230, top=150, level=0.0, seed=4, length=7.0,
         rings=40):
    """
    Falling rain as thin streaks plus impact rings on the water.

    Seasons are flavour and complexity, not a doomsday clock: rain cuts
    visibility, grounds aircraft and makes the water dangerous, but the pool
    does not dry up.
    """
    import random
    rng = random.Random(seed)
    m = kit.mat('_rain', '#C6D2D6', roughness=0.25, alpha=0.40)
    bm = bmesh.new()
    for _ in range(count):
        x = rng.uniform(-bounds, bounds)
        y = rng.uniform(-bounds, bounds)
        z = rng.uniform(level, top)
        w = rng.uniform(0.09, 0.20)
        L = length * rng.uniform(0.6, 1.5)
        lean = rng.uniform(-0.9, 0.9)
        vs = [bm.verts.new((x - w, y, z)), bm.verts.new((x + w, y, z)),
              bm.verts.new((x + w + lean, y + lean * 0.4, z - L)),
              bm.verts.new((x - w + lean, y + lean * 0.4, z - L))]
        bm.faces.new(vs)
    streaks = kit._finish('rain', bm, m, weld=0)
    kit.flat(streaks)
    rm = kit.mat('_rain_ring', '#BFC9C6', roughness=0.4, alpha=0.30)
    for i in range(rings):
        rr = rng.uniform(0.9, 3.2)
        kit.tube(f"rring_{i}", kit.arc((rng.uniform(-bounds * 0.6, bounds * 0.6),
                                   rng.uniform(-bounds * 0.6, bounds * 0.6), 0),
                                  rr, 0, math.tau, steps=10, z=level + 0.12),
                 0.22, sides=4, material=rm)
    return streaks
