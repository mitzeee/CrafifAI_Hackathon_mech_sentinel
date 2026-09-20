"""
Turntable / beauty renders for asset review. Cycles on CPU (headless bpy has
no GPU), low samples, small frames -- these are for checking silhouette and
value, not for marketing.

Lighting matches the reference frame: soft warm key, cool sky fill, gentle
ground bounce, mild haze. Low contrast, muted.
"""
import bpy
import math
import os
from mathutils import Vector
import kit


def world(bg='#8A8D86', strength=1.1):
    w = bpy.data.worlds.new('w') if not bpy.context.scene.world else bpy.context.scene.world
    bpy.context.scene.world = w
    if not w.node_tree:
        w.use_nodes = True
    bg_node = w.node_tree.nodes.get('Background')
    bg_node.inputs[0].default_value = kit.srgb(bg)
    bg_node.inputs[1].default_value = strength


def three_point(target=(0, 0, 0), scale=20.0):
    """Soft overcast-warm key + cool fill. No hard rim; the reference is gentle."""
    def lamp(name, kind, loc, energy, color, size=None, angle=None):
        d = bpy.data.lights.new(name, kind)
        d.energy = energy
        d.color = kit.srgb(color)[:3]
        if size is not None:
            d.size = size
        if angle is not None:
            d.angle = angle
        o = bpy.data.objects.new(name, d)
        o.location = loc
        bpy.context.collection.objects.link(o)
        direction = Vector(target) - Vector(loc)
        o.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        return o

    lamp('key', 'SUN', (scale * 0.9, -scale * 1.1, scale * 1.2), 3.2,
         '#FFE9CC', angle=math.radians(9))
    lamp('fill', 'AREA', (-scale * 1.3, -scale * 0.6, scale * 0.7), scale * 260,
         '#BFD2E0', size=scale * 1.6)
    lamp('bounce', 'AREA', (0, scale * 1.4, -scale * 0.25), scale * 120,
         '#B0A891', size=scale * 2.0)


def ground(z=-0.02, size=400, color='#6B5B49'):
    m = kit.mat('_ground', color, roughness=0.95)
    return kit.plate('_ground_plate', [(-size, -size), (size, -size),
                                       (size, size), (-size, size)], 0.4,
                     loc=(0, 0, z - 0.2), material=m)


def camera(target=(0, 0, 0), dist=42, azim=38, elev=26, lens=75):
    a, e = math.radians(azim), math.radians(elev)
    loc = (math.sin(a) * dist * math.cos(e),
           -math.cos(a) * dist * math.cos(e),
           math.sin(e) * dist)
    cd = bpy.data.cameras.new('cam')
    cd.lens = lens
    co = bpy.data.objects.new('cam', cd)
    co.location = loc
    bpy.context.collection.objects.link(co)
    d = Vector(target) - Vector(loc)
    co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = co
    return co


def camera_at(loc, look_at, lens=32, roll=0.0):
    """Camera placed in the world (cockpit / bridge views), not orbiting."""
    cd = bpy.data.cameras.new('cam')
    cd.lens = lens
    co = bpy.data.objects.new('cam', cd)
    co.location = loc
    bpy.context.collection.objects.link(co)
    q = (Vector(look_at) - Vector(loc)).to_track_quat('-Z', 'Y')
    e = q.to_euler()
    e.rotate_axis('Z', roll)
    co.rotation_euler = e
    bpy.context.scene.camera = co
    return co


def shot(path, res=(900, 600), samples=24):
    scn = bpy.context.scene
    scn.render.engine = 'CYCLES'
    scn.cycles.device = 'CPU'
    scn.cycles.samples = samples
    scn.cycles.use_denoising = True
    scn.render.resolution_x, scn.render.resolution_y = res
    scn.render.film_transparent = False
    scn.view_settings.view_transform = 'Filmic' if 'Filmic' in [
        v.name for v in scn.view_settings.bl_rna.properties['view_transform'].enum_items
    ] else 'AgX'
    scn.view_settings.look = 'None'
    scn.render.filepath = path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.render.render(write_still=True)
    return path
