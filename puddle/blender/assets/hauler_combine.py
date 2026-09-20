"""
Combine hauler "Ark" -- the hub unit (design doc section 2).

Provenance: crushed aluminium drink can hull, crown-cap conning tower, foil
deck plating, razor-blade ram bow, paperclip masts.

Contract: +Y bow, +Z up, origin AT THE WATERLINE so Godot's buoyancy probes
(design doc 8.1.4) can sample the Gerstner heightfield in object space.
"""
import math
import kit
import palette

TAU = math.pi * 2

LEN_HALF = 15.0      # 30 m overall -- game scale, not miniature scale
AXIS_Z = -0.90       # can centreline sits below the waterline
DECK_Z = 1.60        # flat crushed top -> the cargo deck
# The flat deck is the CLAMPED top of the can, so its half-width is not a
# constant -- it falls out of the local hull radius. Solve it per station or
# the plating overhangs the bow as the can necks down.
#   (y, radius, crush)
STATIONS = [
    (-15.0, 2.10, 0.00), (-14.3, 3.70, 0.00), (-13.7, 4.22, 0.00),
    (-12.8, 4.05, 0.00), (-11.0, 4.35, 0.22), (-8.0, 4.35, 0.70),
    (-5.5, 4.35, 0.95), (-2.0, 4.30, 0.72), (1.0, 4.35, 0.98),
    (5.0, 4.35, 0.55), (9.0, 4.30, 0.15), (11.4, 3.55, 0.00),
    (12.9, 2.45, 0.00), (13.7, 2.25, 0.00), (14.2, 2.62, 0.00),
    (14.7, 2.40, 0.00),
]
RISE = 1.60 + 0.90          # DECK_Z - AXIS_Z


def hull_r(y):
    for (y0, r0, _), (y1, r1, _) in zip(STATIONS, STATIONS[1:]):
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            return r0 + (r1 - r0) * t
    return STATIONS[0][1] if y < STATIONS[0][0] else STATIONS[-1][1]


def deck_hw(y):
    r = hull_r(y)
    return math.sqrt(max(0.0, r * r - RISE * RISE))


DECK_HW = deck_hw(0.0)
R = 4.35


def can_ring(r, n=14, crush=0.0, deck=True):
    """
    One cross-section of the can. `crush` dents the upper-port quarter inward,
    which is what makes the hull read as *crushed* rather than as a clean
    cylinder -- the single most important silhouette cue on this asset.
    """
    pts = []
    for i in range(n):
        a = TAU * i / n + TAU / (2 * n)
        x = math.cos(a) * r
        z = math.sin(a) * r + AXIS_Z
        if crush > 0.0:
            d = max(0.0, math.cos(a - 2.25)) ** 1.4
            x -= d * crush * r * 0.55
            z -= d * crush * r * 0.34
            d2 = max(0.0, math.cos(a + 0.95)) ** 2.0
            x += d2 * crush * r * 0.20
            z -= d2 * crush * r * 0.16
        if deck and z > DECK_Z:
            z = DECK_Z
        pts.append((x, z))
    return pts


def blade(h, t, z0=0.0):
    return [(t / 2, h / 2 + z0), (-t / 2, h / 2 + z0),
            (-t / 2, -h / 2 + z0), (t / 2, -h / 2 + z0)]


def build():
    kit.reset()
    C = palette.combine()
    parts = []

    # ---- hull: the can -------------------------------------------------
    hull = kit.loft('hull', [
        (y, can_ring(r, crush=c, deck=(y > -14.0)))
        for (y, r, c) in STATIONS
    ], material=C['can_red'])
    parts.append(hull)

    # patch repairs over patch repairs -- the Combine never replaces a panel
    for idx, (py, pl, pm) in enumerate(((-6.4, 0.75, 'foil'), (2.4, 0.60, 'rust'),
                                        (-10.4, 0.70, 'steel_dark'),
                                        (6.6, 0.55, 'rust'))):
        parts.append(kit.loft(f'patch_{idx}', [
            (py - pl / 2, can_ring(R + 0.05, crush=0.60)),
            (py + pl / 2, can_ring(R + 0.05, crush=0.60)),
        ], cap_start=False, cap_end=False, material=C[pm]))

    # ---- deck plating: foil panels with gaps ---------------------------
    y = -12.6
    i = 0
    while y < 11.4:
        seg = 4.1 if i % 2 == 0 else 3.2
        # taper each plate to the hull it sits on: a trapezoid, not a rectangle
        y_end = min(y + seg, 11.4)
        hw0 = deck_hw(y) - 0.12
        hw1 = deck_hw(y_end) - 0.12
        if hw0 < 0.4 or y_end - y < 0.5:
            break
        parts.append(kit.loft(f'deck_{i}', [
            (y,     [(hw0, DECK_Z), (-hw0, DECK_Z),
                     (-hw0, DECK_Z + 0.22), (hw0, DECK_Z + 0.22)]),
            (y_end, [(hw1, DECK_Z), (-hw1, DECK_Z),
                     (-hw1, DECK_Z + 0.22), (hw1, DECK_Z + 0.22)]),
        ], material=C['bone']))
        y += seg + 0.28
        i += 1

    # deck stringers under the plating
    for sx in (-2.6, 0.0, 2.6):
        parts.append(kit.box(f'stringer_{sx}', (0.5, 23.0, 0.34),
                             loc=(sx, -1.0, DECK_Z - 0.12), material=C['steel_dark']))

    # ---- razor-blade ram bow -------------------------------------------
    RAM_Z = -1.05    # the blade cuts at the waterline, not along the deck
    parts.append(kit.loft('ram', [
        (11.0, blade(5.2, 1.40, RAM_Z)),
        (14.6, blade(4.6, 0.62, RAM_Z + 0.1)),
        (18.0, blade(3.1, 0.20, RAM_Z + 0.3)),
        (20.4, blade(1.5, 0.05, RAM_Z + 0.5)),
    ], material=C['foil']))
    # the blade's slot, framed rather than booleaned -- cheaper and reads fine
    for sz in (0.85, -0.85):
        parts.append(kit.box('slot_frame', (0.40, 2.6, 0.26),
                             loc=(0, 14.6, RAM_Z + sz), material=C['steel_dark']))
    # blade shoulder where it bolts to the neck
    parts.append(kit.box('ram_root', (1.7, 1.0, 4.2),
                         loc=(0, 11.4, RAM_Z + 0.1), material=C['steel_dark']))

    # ---- crown-cap conning tower ---------------------------------------
    tower = kit.crimped_disc('tower', 2.75, 2.60, flutes=17, flute_depth=0.10,
                             loc=(0, -7.4, DECK_Z + 1.30), material=C['bone'])
    parts.append(tower)
    parts.append(kit.crimped_disc('bridge', 1.70, 1.15, flutes=13, flute_depth=0.11,
                                  loc=(0, -7.4, DECK_Z + 3.15), material=C['rust']))
    # viewport slit
    parts.append(kit.box('viewport', (2.5, 0.30, 0.55),
                         loc=(0, -6.15, DECK_Z + 3.20), material=C['glass']))
    # tower lamps
    for sx in (-1.5, 1.5):
        parts.append(kit.cyl('lamp', 0.24, 0.30, sides=8, rot=(math.pi / 2, 0, 0),
                             loc=(sx, -6.1, DECK_Z + 2.05), material=C['lamp']))

    # ---- funnel ---------------------------------------------------------
    parts.append(kit.cyl('funnel', 1.15, 3.40, sides=10,
                         loc=(0, -11.2, DECK_Z + 1.70), material=C['steel_dark']))
    parts.append(kit.cyl('funnel_flare', 1.45, 0.60, sides=10, radius_top=1.15,
                         loc=(0, -11.2, DECK_Z + 3.10), material=C['rust']))

    # ---- rubber-band torsion launch rail (foredeck) ---------------------
    for sx in (-1.55, 1.55):
        parts.append(kit.box('rail', (0.34, 10.5, 0.30),
                             loc=(sx, 6.4, DECK_Z + 0.45), material=C['steel']))
    parts.append(kit.cyl('band_post_l', 0.30, 1.5, sides=8,
                         loc=(-1.55, 1.3, DECK_Z + 0.95), material=C['steel_dark']))
    parts.append(kit.cyl('band_post_r', 0.30, 1.5, sides=8,
                         loc=(1.55, 1.3, DECK_Z + 0.95), material=C['steel_dark']))
    parts.append(kit.tube('rubber_band',
                          [(-1.55, 1.3, DECK_Z + 1.3), (0, 2.6, DECK_Z + 1.3),
                           (1.55, 1.3, DECK_Z + 1.3)], 0.16, sides=6,
                          material=C['rubber']))

    # ---- deck bays (hangars for the fighter/bomber) ---------------------
    for idx, by in enumerate((-2.2, -5.6)):
        parts.append(kit.box(f'bay_{idx}', (5.1, 2.9, 0.30),
                             loc=(0, by, DECK_Z + 0.12), material=C['steel_dark']))
        parts.append(kit.box(f'bay_lip_{idx}', (5.5, 3.3, 0.14),
                             loc=(0, by, DECK_Z + 0.26), material=C['rust']))

    # ---- gunwale rails + stanchions -------------------------------------
    for side in (-1, 1):
        ys = [-12.6 + k * 1.6 for k in range(16)]
        ys = [yy for yy in ys if deck_hw(yy) > 0.9]
        path = [(side * (deck_hw(yy) - 0.28), yy, DECK_Z + 1.05) for yy in ys]
        parts.append(kit.tube(f'gunwale_{side}', path, 0.10, sides=6,
                              material=C['steel']))
        for yy in ys[::2]:
            parts.append(kit.cyl('stanchion', 0.09, 1.05, sides=6,
                                 loc=(side * (deck_hw(yy) - 0.28), yy, DECK_Z + 0.52),
                                 material=C['steel']))

    # ---- paperclip mast --------------------------------------------------
    parts.append(kit.tube('mast', [(0, -9.3, DECK_Z), (0, -9.3, DECK_Z + 6.4),
                                   (0.9, -9.9, DECK_Z + 7.1)],
                          0.11, sides=6, material=C['steel']))

    # ---- rivets along the sheer -------------------------------------------
    for sx in (-1, 1):
        pts = []
        for k in range(22):
            yy = -12.9 + (k / 21.0) * 23.0
            hw = deck_hw(yy)
            if hw < 0.9:
                continue
            pts.append((sx * (hw + 0.02), yy, DECK_Z - 0.30))
        parts.append(kit.rivets(f'rivets_{sx}', pts, radius=0.14,
                                material=C['steel_dark']))

    body = kit.join('hauler_combine_body', parts)
    kit.flat(body)

    # ---- gameplay markers -------------------------------------------------
    root = kit.marker('hauler_combine', (0, 0, 0), size=3.0)
    body.parent = root
    kit.marker('mount_launch_rail', (0, 11.2, DECK_Z + 0.6), root, kind='ARROWS')
    kit.marker('mount_bay_a', (0, -2.2, DECK_Z + 0.3), root)
    kit.marker('mount_bay_b', (0, -5.6, DECK_Z + 0.3), root)
    kit.marker('mount_turret_fwd', (0, 8.2, DECK_Z + 0.3), root)
    kit.marker('mount_turret_aft', (0, -13.0, DECK_Z + 0.3), root)
    kit.marker('mount_bridge_cam', (0, -6.6, DECK_Z + 4.1), root, kind='ARROWS')
    kit.marker('fx_funnel', (0, -11.2, DECK_Z + 3.5), root, kind='CONE')
    kit.marker('fx_bow_wave', (0, 13.8, 0.0), root, kind='CONE')
    kit.marker('fx_wake', (0, -14.6, 0.0), root, kind='CONE')
    kit.marker('waterline', (0, 0, 0), root, size=6.0, kind='CIRCLE')
    kit.buoyancy_probes(root, half_len=12.5, half_beam=3.2, z=0.0, n=4)
    return root


if __name__ == '__main__':
    build()
    print('tris:', kit.tris())
