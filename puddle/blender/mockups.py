"""
Mock-up shots. Each SHOT dresses a scene with SHIPPED assets and renders it,
so what you see is what the game would look like -- not a separate concept
art path that can drift from the build.

    python3 mockups.py /out            # all
    python3 mockups.py /out act3_drying
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


# ---------------------------------------------------------------- Act I ----
@shot
def act1_flood(s, kit, render):
    """06:00. Water at 1.00. Naval. The Ark stands out into open water."""
    s.basin(water_level=0.0)
    s.water(level=0.0, amp=0.22)
    s.rocks(34, 54, 145, 0.0, seed=5)
    yaw = R(-34)
    s.place('hauler_combine', loc=(-10, 6, 0), rot_z=yaw)
    s.wake((-10, 6), yaw, length=58)
    s.place('props_kit', loc=(56, -46, 0), rot_z=R(20))       # scale cues
    s.place('props_kit', loc=(-86, 40, 0), rot_z=R(-70))
    s.macro_backdrop('tyre', dist=300, size=150)
    s.light('dawn')
    s.haze(0.0012)
    render.camera(target=(-6, 4, 6), dist=92, azim=56, elev=13, lens=52)


# --------------------------------------------------------------- Act II ----
@shot
def act2_shallows(s, kit, render):
    """10:00. Water 0.55. Everything at once -- peak complexity."""
    s.basin(water_level=-2.4)
    s.water(level=-2.4, amp=0.16)
    s.rocks(46, 40, 150, -2.4, seed=9)
    yaw = R(-18)
    s.place('hauler_combine', loc=(-4, 2, -2.4), rot_z=yaw)
    s.wake((-4, 2), yaw, length=46, level=-2.4)
    # escort crossing the frame, close enough to read as a fighter not a gull
    s.place('fighter_combine', loc=(30, -26, 17), rot_z=R(-52), pitch=R(-6),
            roll=R(28), scale=1.5)
    s.place('tank_combine', loc=(-52, -30, -1.6), rot_z=R(116), scale=1.6)
    s.place('props_kit', loc=(58, 44, 0), rot_z=R(-15))
    s.macro_backdrop('curb', dist=330, size=140)
    s.light('noon')
    s.haze(0.0010)
    render.camera(target=(-4, -6, 5), dist=98, azim=30, elev=15, lens=52)


# -------------------------------------------------------------- Act III ----
@shot
def act3_drying(s, kit, render):
    """
    14:00. Water 0.18. The Ark is aground and has become a fortress; the
    tide marks it left on the way down are the whole game in one frame.
    """
    s.basin(water_level=-4.6)
    s.water(level=-4.6, amp=0.10)
    s.rocks(58, 26, 150, -4.6, seed=13)
    s.place('hauler_combine', loc=(-16, 4, -4.1), rot_z=R(-52), pitch=R(6),
            roll=R(-9))
    s.place('tank_combine', loc=(40, -40, -1.6), rot_z=R(-150))
    s.place('bike_combine', loc=(19, -44, -1.2), rot_z=R(152))
    s.place('props_kit', loc=(-58, -26, 0), rot_z=R(40))
    s.macro_backdrop('tyre', dist=310, size=160)
    s.light('drying')
    s.haze(0.0016, color='#C6B79C')
    render.camera(target=(0, -14, 1), dist=116, azim=44, elev=21, lens=54)


# ------------------------------------------------------------ factions -----
@shot
def faction_standoff(s, kit, render):
    """The design-language bible page: both haulers, one light."""
    s.basin(water_level=0.0)
    s.water(level=0.0, amp=0.18)
    s.rocks(22, 62, 150, 0.0, seed=21)
    # Stationary standoff: no wakes, and framed wide enough that neither
    # hull is cropped -- this page has to be readable as a comparison.
    s.place('hauler_combine', loc=(-34, -10, 0), rot_z=R(24))
    s.place('hauler_reedfolk', loc=(32, 16, 0), rot_z=R(206))
    s.place('props_kit', loc=(-6, 76, 0), rot_z=R(-40))
    s.macro_backdrop('curb', dist=330, size=140)
    s.light('noon')
    s.haze(0.0011)
    render.camera(target=(-2, 2, 2), dist=156, azim=36, elev=21, lens=58)


# ----------------------------------------------------------- the lens ------
@shot
def theater6_lens(s, kit, render):
    """
    Theater 6. Sunlight focused through a discarded bottle into a moving beam
    of lethal heat. Survivable if you read it.
    """
    import bpy
    s.basin(water_level=-1.0)
    s.water(level=-1.0, amp=0.14)
    s.rocks(30, 46, 150, -1.0, seed=31)
    glass = kit.mat('_bottle', '#8FA890', roughness=0.04, alpha=0.22)
    kit.cyl('bottle', 26, 130, sides=16, loc=(6, 54, 54),
            rot=(R(64), 0, R(14)), material=glass)
    kit.cyl('bottle_neck', 12, 34, sides=12, loc=(-16, 6, 22),
            rot=(R(64), 0, R(14)), material=glass)
    yaw = R(-66)
    s.place('hauler_combine', loc=(-30, -16, -1.0), rot_z=yaw)
    s.wake((-30, -16), yaw, length=48, level=-1.0)
    s.light('noon')
    d = bpy.data.lights.new('beam', 'SPOT')
    d.energy = 9.0e6
    d.spot_size = R(9)
    d.spot_blend = 0.06
    d.color = kit.srgb('#FFF4D2')[:3]
    o = bpy.data.objects.new('beam', d)
    o.location = (14, 22, 86)
    bpy.context.collection.objects.link(o)
    o.rotation_euler = (R(9), 0, 0)
    # scorched water where the beam lands, and steam standing off it
    kit.cyl('scorch', 11, 0.25, sides=18, loc=(14, 8, -0.85),
            material=kit.mat('_scorch', '#E8DCB4', roughness=0.30,
                             emission='#FFF0C0', emit_strength=1.4))
    # Steam as geometry read as floating boulders; the beam column through
    # light haze does the job on its own.
    s.haze(0.0020, color='#EFE3C6', size=380)
    render.camera(target=(6, 8, 14), dist=104, azim=26, elev=10, lens=46)


# ------------------------------------------------------ rolling god -------
@shot
def rolling_god(s, kit, render):
    """
    A car crosses the lot. Pressure wave, then a bow wave that capsizes
    anything not bow-on. Neither tribe controls it; you get a few seconds.
    """
    s.basin(water_level=0.0)
    s.water(level=0.0, amp=0.26, choppy=1.6)
    s.rocks(26, 58, 145, 0.0, seed=41)
    s.macro_backdrop('tyre', dist=280, size=175, color='#262523')
    crest = kit.mat('_crest', '#7F8A84', roughness=0.12)
    foam = kit.mat('_crestfoam', '#C4C9BF', roughness=0.7, alpha=0.55)
    # The wall of water has to be ON TOP of the hull, not parked on the far
    # shore -- at y=60 it just merged with the shoreline.
    kit.tube('wave', [(-190, 30, -2.0), (-40, 24, 0.4), (60, 26, 0.0),
                      (190, 32, -2.0)], 9.5, sides=12, material=crest)
    kit.plate('wave_foam', [(-190, 12), (190, 14), (190, 26), (-190, 24)],
              0.4, loc=(0, 0, 1.6), material=foam)
    yaw = R(4)
    s.place('hauler_combine', loc=(-14, -26, 0.8), rot_z=yaw, pitch=R(-13),
            roll=R(8))
    s.light('noon')
    s.haze(0.0018)
    render.camera(target=(-12, -4, 6), dist=92, azim=24, elev=12, lens=48)


# ------------------------------------------------------ the throat --------
@shot
def theater8_throat(s, kit, render):
    """Theater 8. The storm grate. Endgame: dark, echoing, vertical."""
    s.basin(water_level=-3.2, radius=70, depth=9.0)
    s.water(level=-3.2, amp=0.10)
    s.rocks(34, 30, 120, -3.2, seed=53)
    iron = kit.mat('_grate_iron', '#2A2C2B', metallic=0.4, roughness=0.75)
    for i in range(7):                       # grate bars overhead
        kit.box(f'bar_{i}', (13, 300, 11), loc=(-78 + i * 26, 20, 62),
                material=iron)
    kit.box('grate_frame_l', (16, 300, 40), loc=(-96, 20, 44), material=iron)
    kit.box('grate_frame_r', (16, 300, 40), loc=(92, 20, 44), material=iron)
    kit.box('throat_lip', (260, 26, 30), loc=(0, -66, -8), material=iron)
    yaw = R(186)
    s.place('hauler_combine', loc=(-8, 6, -3.2), rot_z=yaw)
    s.wake((-8, 6), yaw, length=40, level=-3.2)
    s.light('grate')
    s.haze(0.0030, color='#8FA0AE', size=420)
    render.camera(target=(0, 4, 14), dist=120, azim=10, elev=16, lens=44)


# -------------------------------------------------- cigarette reef --------
@shot
def theater5_reef(s, kit, render):
    """Theater 5. Cover-dense, tank country, terrible for aircraft."""
    s.basin(water_level=-3.0)
    s.water(level=-3.0, amp=0.12)
    s.rocks(44, 24, 140, -3.0, seed=67)
    for i, (x, y, rz, sc) in enumerate((
            (-30, 14, 40, 1.0), (-8, 30, 110, 0.9), (26, 10, 15, 1.1),
            (44, -28, 70, 0.85), (-46, -20, 140, 1.0), (8, -34, 95, 0.95))):
        s.place('props_kit', loc=(x * 1.6, y * 1.6, -2.0), rot_z=R(rz),
                scale=sc)
    s.place('tank_combine', loc=(-14, -30, -2.2), rot_z=R(24), scale=1.8)
    s.place('bike_combine', loc=(22, -40, -2.0), rot_z=R(-40), scale=1.8)
    s.macro_backdrop('slab', dist=300, size=120)
    s.light('noon')
    s.haze(0.0014)
    render.camera(target=(0, -16, 2), dist=88, azim=38, elev=15, lens=52)


# ------------------------------------------------------- bridge view ------
@shot
def bridge_view(s, kit, render):
    """
    From the Ark's bridge, looking forward over the cargo deck and the launch
    rail. This is the hub seat -- the one you always come back to.
    """
    s.basin(water_level=0.0)
    s.water(level=0.0, amp=0.20)
    s.rocks(40, 46, 150, 0.0, seed=71)
    s.place('hauler_combine', loc=(0, 0, 0))
    s.place('hauler_reedfolk', loc=(34, 78, 0), rot_z=R(206))
    s.place('props_kit', loc=(-52, 70, 0), rot_z=R(30))
    s.macro_backdrop('curb', dist=340, size=150)
    s.light('noon')
    s.haze(0.0011)
    render.camera_at((0, -7.2, 6.4), (0, 60, 2.0), lens=30)


# ------------------------------------------------------- the clock strip ---
def _clock_panel(s, kit, render, level, act):
    """
    Locked camera across all four panels so the waterline visibly retreats.
    The basin is a bowl, so the shore sits at radius ~98 / 73 / 47 / 27 as the
    level drops -- and every metre it gives up leaves a tide band behind.
    """
    s.basin(water_level=level)
    s.water(level=level, amp=0.16)
    s.rocks(52, 22, 132, level, seed=17)
    s.place('props_kit', loc=(52, -22, 0), rot_z=R(24))      # beaches by 14:00
    s.light(act)
    s.haze(0.0015 if act != 'drying' else 0.0022)
    render.camera(target=(0, 0, -3), dist=176, azim=34, elev=31, lens=44)


for _i, (_lv, _act, _nm) in enumerate([
        (0.0, 'dawn', 'clock_0600'), (-2.0, 'noon', 'clock_1000'),
        (-4.2, 'drying', 'clock_1400'), (-5.4, 'storm', 'clock_1800')]):
    def _mk(lv=_lv, act=_act):
        return lambda s, kit, render: _clock_panel(s, kit, render, lv, act)
    SHOTS[_nm] = _mk()


# ---------------------------------------------------------------------------
RES = (1280, 720)


def run(name, outdir, samples=28):
    code = f'''
import sys, math; sys.path.insert(0,"lib"); sys.path.insert(0,"assets")
sys.path.insert(0,".")
import kit, scene, render, mockups
kit.reset()
mockups.SHOTS["{name}"](scene, kit, render)
render.shot(r"{outdir}/{name}.png", res={RES}, samples={samples})
print("DONE", "{name}", kit.tris())
'''
    r = subprocess.run([sys.executable, '-c', code], cwd=HERE,
                       capture_output=True, text=True)
    ok = [l for l in r.stdout.splitlines() if l.startswith('DONE')]
    if ok:
        print('  ' + ok[0])
    else:
        print(f'  FAIL {name}')
        print('   ', '\n    '.join(r.stderr.strip().splitlines()[-5:]))


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    targets = sys.argv[2:] or list(SHOTS)
    for t in targets:
        run(t, out)
