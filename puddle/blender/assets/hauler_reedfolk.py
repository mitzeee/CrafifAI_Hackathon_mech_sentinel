"""
Reedfolk hauler -- the mirror of the Combine Ark (design doc section 5.2).

Provenance: a great seed pod, waxed-leaf deck, resin-lacquered shell, spider-
silk rigging, bioluminescent resin seams. Where the Combine is straight lines
and smoke, this is curves and glow -- a player must call the faction from the
silhouette alone, out of focus.

Same marker contract as the Combine hauler so Godot can treat them alike.
"""
import math
import kit
import palette

LEN_HALF = 15.0
AXIS_Z = -1.05
# Low enough that the clamped top is a real deck: at DECK_Z 1.75 the waxed-leaf
# decking came out 3 m wide on an 8 m hull and vanished under its own midrib.
DECK_Z = 1.00

#   (y, half-beam, half-height)
STATIONS = [
    (-16.2, 0.30, 0.26), (-15.0, 1.15, 0.95), (-13.2, 2.15, 1.70),
    (-10.5, 3.10, 2.35), (-7.0, 3.80, 2.80), (-3.0, 4.15, 3.05),
    (1.0, 4.20, 3.05), (5.0, 3.85, 2.80), (9.0, 3.10, 2.30),
    (12.2, 2.20, 1.65), (14.6, 1.20, 0.95), (16.4, 0.28, 0.32),
]


def pod_ring(rx, rz, n=14, clamp=None):
    """Elliptical, bilaterally symmetric -- they grew it, they didn't weld it."""
    top = DECK_Z if clamp is None else clamp
    pts = []
    for i in range(n):
        a = math.tau * i / n + math.tau / (2 * n)
        z = math.sin(a) * rz + AXIS_Z
        pts.append((math.cos(a) * rx, min(z, top)))
    return pts


def beam_at(y):
    for (y0, b0, h0), (y1, b1, h1) in zip(STATIONS, STATIONS[1:]):
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            return b0 + (b1 - b0) * t, h0 + (h1 - h0) * t
    return 0.3, 0.3


def deck_hw(y):
    _, h = beam_at(y)
    b, _ = beam_at(y)
    rise = DECK_Z - AXIS_Z
    if h <= rise:
        return 0.0
    return b * math.sqrt(max(0.0, 1.0 - (rise / h) ** 2))


def build():
    kit.reset()
    R = palette.reedfolk()
    parts = []

    parts.append(kit.loft('pod', [(y, pod_ring(b, h)) for y, b, h in STATIONS],
                          material=R['chitin']))
    # lacquered underbody: the waterline band, darker honey resin
    # lacquered underbody only -- capping it at deck height buried the decking
    parts.append(kit.loft('lacquer', [
        (y, pod_ring(b + 0.05, h + 0.05, clamp=AXIS_Z + 0.35))
        for y, b, h in STATIONS if -13.5 < y < 13.5
    ], cap_start=False, cap_end=False, material=R['honey']))

    # ---- waxed-leaf deck with a central vein ------------------------------
    y = -12.5
    i = 0
    while y < 12.2:
        seg = 3.4
        y_end = min(y + seg, 12.2)
        hw0, hw1 = deck_hw(y) - 0.10, deck_hw(y_end) - 0.10
        if hw0 < 0.4 or y_end - y < 0.5:
            break
        parts.append(kit.loft(f'leaf_{i}', [
            (y,     [(hw0, DECK_Z), (-hw0, DECK_Z),
                     (-hw0, DECK_Z + 0.18), (hw0, DECK_Z + 0.18)]),
            (y_end, [(hw1, DECK_Z), (-hw1, DECK_Z),
                     (-hw1, DECK_Z + 0.18), (hw1, DECK_Z + 0.18)]),
        ], material=R['wax_green']))
        y = y_end + 0.22
        i += 1
    parts.append(kit.box('midrib', (0.70, 24.0, 0.30), loc=(0, -0.3, DECK_Z + 0.24),
                         material=R['bark']))
    for k in range(9):          # side veins
        sy = -11.0 + k * 2.7
        hw = deck_hw(sy)
        if hw < 0.8:
            continue
        for side in (-1, 1):
            parts.append(kit.tube(f'vein_{k}_{side}',
                                  [(0, sy, DECK_Z + 0.22),
                                   (side * hw * 0.92, sy + 1.5, DECK_Z + 0.20)],
                                  0.07, sides=4, material=R['bark']))

    # ---- curled horn tower -------------------------------------------------
    horn = [(0, -7.0 + math.sin(t * 1.5) * 0.9, DECK_Z + t * 4.4)
            for t in [i / 10 for i in range(11)]]
    horn += [(0, -5.6, DECK_Z + 5.0), (0.8, -4.9, DECK_Z + 5.3)]
    parts.append(kit.tube('horn', horn, 1.35, sides=10,
                          taper=lambda t: 1.0 - 0.72 * t, material=R['amber']))
    parts.append(kit.loft('gall', [
        (-9.6, pod_ring(1.1, 1.0)), (-8.4, pod_ring(2.3, 2.1)),
        (-6.6, pod_ring(2.4, 2.2)), (-5.4, pod_ring(1.3, 1.2)),
    ], loc=(0, 0, DECK_Z + 1.5), material=R['resin']))
    parts.append(kit.box('viewport', (2.2, 0.28, 0.5), loc=(0, -5.4, DECK_Z + 2.4),
                         material=R['amber_clear']))

    # ---- masts and spider-silk rigging -------------------------------------
    for my in (3.5, -11.0):
        parts.append(kit.tube(f'mast_{my}', [(0, my, DECK_Z), (0, my, DECK_Z + 7.0)],
                              0.20, sides=6, taper=lambda t: 1.0 - 0.45 * t,
                              material=R['bark']))
    for side in (-1, 1):
        parts.append(kit.tube(f'stay_{side}',
                              [(0, 3.5, DECK_Z + 6.9), (side * 2.6, -3.0, DECK_Z + 0.4)],
                              0.05, sides=4, material=R['silk']))
        parts.append(kit.tube(f'stay_b_{side}',
                              [(0, -11.0, DECK_Z + 6.9),
                               (side * 2.2, -5.0, DECK_Z + 0.4)],
                              0.05, sides=4, material=R['silk']))
    parts.append(kit.tube('forestay', [(0, 3.5, DECK_Z + 6.9), (0, 13.0, DECK_Z - 0.2)],
                          0.05, sides=4, material=R['silk']))

    # ---- bioluminescent resin seams ----------------------------------------
    for side in (-1, 1):
        pts = []
        for k in range(14):
            yy = -12.0 + k * 1.85
            b, h = beam_at(yy)
            pts.append((side * (b + 0.05), yy, AXIS_Z + h * 0.25))
        parts.append(kit.tube(f'seam_{side}', pts, 0.10, sides=4, material=R['glow']))

    body = kit.join('hauler_reedfolk_body', parts)
    kit.flat(body)

    root = kit.marker('hauler_reedfolk', (0, 0, 0), size=3.0)
    body.parent = root
    kit.marker('mount_launch_rail', (0, 10.5, DECK_Z + 0.4), root, kind='ARROWS')
    kit.marker('mount_bay_a', (0, -1.0, DECK_Z + 0.3), root)
    kit.marker('mount_bay_b', (0, -4.0, DECK_Z + 0.3), root)
    kit.marker('mount_turret_fwd', (0, 7.5, DECK_Z + 0.3), root)
    kit.marker('mount_turret_aft', (0, -13.0, DECK_Z + 0.3), root)
    kit.marker('mount_bridge_cam', (0, -5.0, DECK_Z + 3.0), root, kind='ARROWS')
    kit.marker('fx_bow_wave', (0, 14.0, 0.0), root, kind='CONE')
    kit.marker('fx_wake', (0, -15.0, 0.0), root, kind='CONE')
    kit.marker('fx_spore_vent', (0.8, -4.9, DECK_Z + 5.3), root, kind='CONE')
    kit.marker('waterline', (0, 0, 0), root, size=6.0, kind='CIRCLE')
    kit.buoyancy_probes(root, half_len=12.0, half_beam=3.2, z=0.0, n=4)
    return root
