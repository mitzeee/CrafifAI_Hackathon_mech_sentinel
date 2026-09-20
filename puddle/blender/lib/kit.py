"""
THE DRYING - procedural asset toolkit.

Small layer over bmesh for building found-object game assets. Everything is
built from code so silhouettes stay tweakable: change a number, rebuild the
whole fleet.

Scale contract (design doc 7.3): model at GAME scale, not miniature scale.
A hauler is ~30 units long, not 4 centimetres. Miniature-ness is sold by the
renderer (tilt-shift, dust, macro reference props), never by tiny transforms.

Axis contract, matching Godot's glTF import:
    +Y = forward (bow / nose / muzzle)
    +Z = up
    +X = starboard
Origin sits at the waterline for anything that floats, on the ground plane
for anything that drives.
"""

import bpy
import bmesh
import math
import os
import random
from mathutils import Vector, Matrix, Quaternion

TAU = math.pi * 2


# --------------------------------------------------------------------------
# scene
# --------------------------------------------------------------------------

def reset():
    """Empty scene, metric units, deterministic RNG."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scn = bpy.context.scene
    scn.unit_settings.system = 'METRIC'
    scn.unit_settings.scale_length = 1.0
    random.seed(20260920)


def srgb(hexstr):
    """'#4A5057' -> linear RGBA. Blender wants linear; the art bible is sRGB."""
    h = hexstr.lstrip('#')
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (out[0], out[1], out[2], 1.0)


def mat(name, color, metallic=0.0, roughness=0.6, emission=None, emit_strength=2.0,
        alpha=1.0):
    """Principled material, cached by name so the fleet shares one palette."""
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    m = bpy.data.materials.new(name)
    if not m.node_tree:
        m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = srgb(color)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Alpha'].default_value = alpha
    if alpha < 1.0:
        m.surface_render_method = 'BLENDED'
    if emission:
        bsdf.inputs['Emission Color'].default_value = srgb(emission)
        bsdf.inputs['Emission Strength'].default_value = emit_strength
    return m


# --------------------------------------------------------------------------
# mesh plumbing
# --------------------------------------------------------------------------

def _finish(name, bm, material, weld=1e-4):
    if weld:
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=weld)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    if material:
        ob.data.materials.append(material)
    return ob


def _xform(bm, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    m = (Matrix.Translation(Vector(loc))
         @ Quaternion(Vector((0, 0, 1)), rot[2]).to_matrix().to_4x4()
         @ Quaternion(Vector((0, 1, 0)), rot[1]).to_matrix().to_4x4()
         @ Quaternion(Vector((1, 0, 0)), rot[0]).to_matrix().to_4x4()
         @ Matrix.Diagonal(Vector(scale).to_4d()))
    bmesh.ops.transform(bm, matrix=m, verts=bm.verts[:])


def box(name, size, loc=(0, 0, 0), rot=(0, 0, 0), material=None):
    sx, sy, sz = (s / 2 for s in size)
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in (
        (-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
        (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz))]
    for f in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1),
              (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
        bm.faces.new([vs[i] for i in f])
    _xform(bm, loc, rot)
    return _finish(name, bm, material)


def cyl(name, radius, depth, sides=16, loc=(0, 0, 0), rot=(0, 0, 0),
        radius_top=None, material=None, caps=True):
    """Cylinder/cone along local +Z. radius_top=0 gives a cone."""
    rt = radius if radius_top is None else radius_top
    bm = bmesh.new()
    lo, hi = [], []
    for i in range(sides):
        a = TAU * i / sides
        lo.append(bm.verts.new((math.cos(a) * radius, math.sin(a) * radius, -depth / 2)))
        hi.append(bm.verts.new((math.cos(a) * rt, math.sin(a) * rt, depth / 2)))
    for i in range(sides):
        j = (i + 1) % sides
        bm.faces.new((lo[i], lo[j], hi[j], hi[i]))
    if caps:
        if radius > 1e-5:
            bm.faces.new(list(reversed(lo)))
        if rt > 1e-5:
            bm.faces.new(hi)
    _xform(bm, loc, rot)
    return _finish(name, bm, material)


def loft(name, sections, cap_start=True, cap_end=True, material=None,
         loc=(0, 0, 0), rot=(0, 0, 0)):
    """
    Skin a series of cross-sections into a hull.

    sections: [(y, [(x, z), ...]), ...] -- every ring needs the same point
    count, ordered consistently. This is how every hull in the game is
    built; box-assembly silhouettes read as programmer art.
    """
    bm = bmesh.new()
    rings = [[bm.verts.new((x, y, z)) for x, z in pts] for y, pts in sections]
    for a, b in zip(rings, rings[1:]):
        n = len(a)
        for i in range(n):
            j = (i + 1) % n
            try:
                bm.faces.new((a[i], a[j], b[j], b[i]))
            except ValueError:
                pass  # degenerate at a collapsed nose ring
    if cap_start:
        try:
            bm.faces.new(list(reversed(rings[0])))
        except ValueError:
            pass
    if cap_end:
        try:
            bm.faces.new(rings[-1])
        except ValueError:
            pass
    _xform(bm, loc, rot)
    return _finish(name, bm, material)


def plate(name, outline, thickness, loc=(0, 0, 0), rot=(0, 0, 0), material=None):
    """
    Extrude a 2D outline (XY) into a thin slab along Z. Wings, membrane panels,
    leaf decks, razor blades, fins -- most of this game's flat found-object
    parts are plates.
    """
    bm = bmesh.new()
    bot = [bm.verts.new((x, y, -thickness / 2)) for x, y in outline]
    top = [bm.verts.new((x, y, thickness / 2)) for x, y in outline]
    n = len(outline)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    bm.faces.new(list(reversed(bot)))
    bm.faces.new(top)
    _xform(bm, loc, rot)
    return _finish(name, bm, material)


def _frames(pts):
    """Parallel-transport frames so swept tubes don't corkscrew."""
    n = len(pts)
    tan = []
    for i in range(n):
        if i == 0:
            t = pts[1] - pts[0]
        elif i == n - 1:
            t = pts[-1] - pts[-2]
        else:
            t = pts[i + 1] - pts[i - 1]
        tan.append(t.normalized())
    ref = Vector((0, 0, 1))
    if abs(tan[0].dot(ref)) > 0.9:
        ref = Vector((1, 0, 0))
    nor = [(ref - tan[0] * ref.dot(tan[0])).normalized()]
    for i in range(1, n):
        axis = tan[i - 1].cross(tan[i])
        if axis.length < 1e-8:
            nor.append(nor[-1])
        else:
            q = Quaternion(axis.normalized(), tan[i - 1].angle(tan[i]))
            nor.append((q @ nor[-1]).normalized())
    return tan, nor


def tube(name, points, radius, sides=8, material=None, caps=True, taper=None):
    """
    Sweep a circle along a polyline. Wire, rails, rigging, springs, gun
    barrels -- the Combine is held together with bent wire, so this gets
    used constantly.

    taper: optional fn(t in 0..1) -> radius multiplier.
    """
    pts = [Vector(p) for p in points]
    tan, nor = _frames(pts)
    bm = bmesh.new()
    rings = []
    for i, p in enumerate(pts):
        t = i / max(1, len(pts) - 1)
        r = radius * (taper(t) if taper else 1.0)
        binor = tan[i].cross(nor[i])
        ring = []
        for k in range(sides):
            a = TAU * k / sides
            ring.append(bm.verts.new(p + nor[i] * (math.cos(a) * r)
                                     + binor * (math.sin(a) * r)))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for i in range(sides):
            j = (i + 1) % sides
            try:
                bm.faces.new((a[i], a[j], b[j], b[i]))
            except ValueError:
                pass
    if caps:
        try:
            bm.faces.new(list(reversed(rings[0])))
            bm.faces.new(rings[-1])
        except ValueError:
            pass
    return _finish(name, bm, material)


def arc(center, radius, a0, a1, steps=12, plane='XY', z=0.0):
    """Point list for feeding into tube()."""
    out = []
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        c, s = math.cos(a) * radius, math.sin(a) * radius
        if plane == 'XY':
            out.append((center[0] + c, center[1] + s, center[2] + z))
        elif plane == 'YZ':
            out.append((center[0] + z, center[1] + c, center[2] + s))
        else:
            out.append((center[0] + c, center[1] + z, center[2] + s))
    return out


def helix(start, axis_len, radius, turns, steps=64, axis='Y'):
    """Spring coils -- the Combine motorcycle frame."""
    out = []
    for i in range(steps + 1):
        t = i / steps
        a = TAU * turns * t
        c, s = math.cos(a) * radius, math.sin(a) * radius
        if axis == 'Y':
            out.append((start[0] + c, start[1] + axis_len * t, start[2] + s))
        else:
            out.append((start[0] + c, start[1] + s, start[2] + axis_len * t))
    return out


# --------------------------------------------------------------------------
# found-object detail
# --------------------------------------------------------------------------

def crimped_disc(name, radius, height, flutes=21, flute_depth=0.08,
                 skirt=0.0, loc=(0, 0, 0), rot=(0, 0, 0), material=None):
    """
    A crown bottle cap: fluted skirt, flat top. Provenance for the Combine
    conning tower, tank hull and turret, and the bunker prop. One of the most
    recognisable silhouettes in the whole found-object vocabulary.
    """
    sides = flutes * 2
    secs = []
    top = []
    mid = []
    bot = []
    for i in range(sides):
        a = TAU * i / sides
        r = radius * (1.0 - flute_depth * (i % 2))
        top.append((math.cos(a) * radius * 0.94, math.sin(a) * radius * 0.94))
        mid.append((math.cos(a) * r, math.sin(a) * r))
        bot.append((math.cos(a) * r * 0.97, math.sin(a) * r * 0.97))
    # loft along Z by reusing loft()'s (y, [(x,z)]) form then rotating upright
    secs.append((-height / 2, bot))
    secs.append((-height * 0.18, mid))
    secs.append((height / 2 - height * 0.12, mid))
    secs.append((height / 2, top))
    ob = loft(name, secs, material=material)
    # loft builds along +Y; stand it up on +Z
    ob.rotation_euler = (math.pi / 2, 0, 0)
    bpy.context.view_layer.update()
    apply_transform(ob)
    ob.location = loc
    ob.rotation_euler = rot
    return ob


def rivets(name, points, radius=0.09, material=None, sides=6):
    """Rivet heads as real geometry. Fine for blockout and concept renders;
    bake to a normal map before shipping."""
    bm = bmesh.new()
    for p in points:
        sub = bmesh.new()
        for i in range(sides):
            a = TAU * i / sides
            sub.verts.new((math.cos(a) * radius, math.sin(a) * radius, 0))
        sub.verts.ensure_lookup_table()
        sub.faces.new(sub.verts[:])
        bmesh.ops.extrude_face_region(sub, geom=sub.faces[:])
        top = [v for v in sub.verts if not v.link_faces or True][-sides:]
        for v in top:
            v.co.z += radius * 0.6
            v.co.x *= 0.6
            v.co.y *= 0.6
        _xform(sub, loc=p)
        me = bpy.data.meshes.new('_r')
        sub.to_mesh(me)
        sub.free()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    return _finish(name, bm, material, weld=0)


def rivet_line(a, b, count):
    a, b = Vector(a), Vector(b)
    return [tuple(a.lerp(b, i / max(1, count - 1))) for i in range(count)]


def rock(name, radius, seed=0, roughness=0.42, subdiv=2, squash=0.7,
         loc=(0, 0, 0), material=None):
    """Irregular pebble. At this scale a grain of grit is a boulder."""
    rng = random.Random(seed)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=radius)
    for v in bm.verts:
        v.co *= 1.0 + rng.uniform(-roughness, roughness)
        v.co.z *= squash
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(loc)), verts=bm.verts[:])
    return _finish(name, bm, material)


# --------------------------------------------------------------------------
# object ops
# --------------------------------------------------------------------------

def select(objs, active=None):
    bpy.ops.object.select_all(action='DESELECT')
    objs = objs if isinstance(objs, (list, tuple)) else [objs]
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = active or objs[0]


def apply_transform(ob):
    select(ob)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def join(name, objs, material=None):
    objs = [o for o in objs if o]
    select(objs, active=objs[0])
    if len(objs) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = name
    ob.data.name = name
    if material:
        ob.data.materials.clear()
        ob.data.materials.append(material)
    return ob


def bevel(ob, width=0.05, segments=2, angle=50):
    m = ob.modifiers.new('bevel', 'BEVEL')
    m.width = width
    m.segments = segments
    m.limit_method = 'ANGLE'
    m.angle_limit = math.radians(angle)
    m.harden_normals = False
    return ob


def mirror_x(ob):
    m = ob.modifiers.new('mirror', 'MIRROR')
    m.use_axis = (True, False, False)
    return ob


def flat(ob):
    """
    Hard-edge everything. The reference style is faceted low-poly: flat shading
    IS the look, so this is the default and smooth() is the exception (used
    only where a hull needs to read as a grown compound curve).
    """
    select(ob)
    bpy.ops.object.shade_flat()
    return ob


def smooth(ob, angle=38):
    select(ob)
    bpy.ops.object.shade_auto_smooth(angle=math.radians(angle))
    return ob


def apply_mods(ob):
    select(ob)
    for m in list(ob.modifiers):
        try:
            bpy.ops.object.modifier_apply(modifier=m.name)
        except RuntimeError:
            ob.modifiers.remove(m)
    return ob


def marker(name, loc, parent=None, size=0.6, kind='PLAIN_AXES'):
    """
    Gameplay attach point. glTF exports empties as plain nodes, so these land
    in Godot as Node3D children ready to be looked up by name -- launch rails,
    turret rings, buoyancy probes, VFX emitters.
    """
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = kind
    e.empty_display_size = size
    e.location = loc
    bpy.context.collection.objects.link(e)
    if parent:
        e.parent = parent
    return e


def buoyancy_probes(parent, half_len, half_beam, z=0.0, n=4):
    """
    Probe points for the design doc's 8.1.4 buoyancy: sample the same Gerstner
    heightfield the water shader uses, push up per probe. Laid out fore/aft
    along both sides so the hull pitches and rolls correctly.
    """
    out = []
    for i in range(n):
        t = -1.0 + 2.0 * i / (n - 1)
        for sx, tag in ((-1, 'P'), (1, 'S')):
            out.append(marker(f'probe_{tag}{i}', (half_beam * sx, half_len * t, z),
                              parent=parent, size=0.4, kind='SPHERE'))
    return out


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------

# Generated output lives OUTSIDE blender/, next to the design docs -- keeping
# it in blender/assets/ collides with the asset source modules of the same name.
BLENDER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BLENDER_DIR)
GLB_DIR = os.path.join(ROOT, 'assets', 'glb')
BLEND_DIR = os.path.join(ROOT, 'assets', 'blend')


def export(name, root=None):
    """Write .glb (for Godot) and .blend (for hand-editing) side by side."""
    os.makedirs(GLB_DIR, exist_ok=True)
    os.makedirs(BLEND_DIR, exist_ok=True)
    glb = os.path.join(GLB_DIR, f'{name}.glb')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=glb,
        export_format='GLB',
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
    )
    blend = os.path.join(BLEND_DIR, f'{name}.blend')
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    return glb, blend


def tris():
    n = 0
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            o.data.calc_loop_triangles()
            n += len(o.data.loop_triangles)
    return n
