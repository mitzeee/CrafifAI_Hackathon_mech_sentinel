"""
Auto-rickshaw -- the light courier. Three wheels, no armour, no gun, and the
only thing in the fleet that can thread a reed pass a truck cannot.

Runs small, urgent loads: medicine, orders, a single passenger who matters.
Provenance: bottle-cap canopy, spool wheels, wire frame, a foil windscreen.
"""
import math
import kit
import palette


def build():
    kit.reset()
    C = palette.combine()
    N = palette.neutral()
    parts = []
    RF, RR = 0.44, 0.50

    # ---- single front wheel on a forked leg --------------------------------
    parts.append(kit.cyl('fw', RF, 0.34, sides=10, loc=(0, 2.05, RF),
                         rot=(0, math.pi / 2, 0), material=C['rubber']))
    for sx in (-0.26, 0.26):
        parts.append(kit.tube(f'fork_{sx}', [(sx, 2.05, RF), (sx, 1.72, 1.66)],
                              0.075, sides=5, material=C['steel']))
    parts.append(kit.tube('bars', [(-0.5, 1.6, 1.62), (0, 1.74, 1.70),
                                   (0.5, 1.6, 1.62)], 0.06, sides=6,
                          material=C['steel_dark']))

    # ---- rear axle ----------------------------------------------------------
    for sx in (-1.05, 1.05):
        parts.append(kit.cyl(f'rw_{sx}', RR, 0.36, sides=10, loc=(sx, -1.1, RR),
                             rot=(0, math.pi / 2, 0), material=C['rubber']))
    parts.append(kit.cyl('axle', 0.10, 2.1, sides=6, loc=(0, -1.1, RR),
                         rot=(0, math.pi / 2, 0), material=C['steel']))

    # ---- tub ----------------------------------------------------------------
    parts.append(kit.loft('tub', [
        (-1.85, [(0.86, 0.50), (0.90, 1.34), (0, 1.52), (-0.90, 1.34),
                 (-0.86, 0.50)]),
        (-0.2, [(0.98, 0.42), (1.02, 1.42), (0, 1.62), (-1.02, 1.42),
                (-0.98, 0.42)]),
        (1.15, [(0.74, 0.48), (0.78, 1.34), (0, 1.50), (-0.78, 1.34),
                (-0.74, 0.48)]),
    ], material=C['can_red']))
    parts.append(kit.box('floor', (1.85, 3.0, 0.16), loc=(0, -0.5, 0.52),
                         material=N['match_wood']))
    parts.append(kit.box('bench', (1.7, 0.85, 0.52), loc=(0, -1.35, 0.92),
                         material=C['rubber']))
    parts.append(kit.box('screen', (1.35, 0.14, 0.58), loc=(0, 1.16, 1.50),
                         material=C['glass']))

    # ---- crown-cap canopy ---------------------------------------------------
    # A full-size crown cap here reads as a mushroom; the canopy wants to be
    # a small lid over the tub, not wider than the vehicle.
    canopy = kit.crimped_disc('canopy', 1.05, 0.30, flutes=13, flute_depth=0.11,
                              loc=(0, -0.30, 2.24), material=C['foil'])
    canopy.scale = (1.0, 1.42, 1.0)
    kit.apply_transform(canopy)
    parts.append(canopy)
    for sx, sy in ((-0.88, 0.80), (0.88, 0.80), (-0.88, -1.5), (0.88, -1.5)):
        parts.append(kit.tube(f'post_{sx}_{sy}', [(sx, sy, 1.4), (sx, sy, 2.20)],
                              0.065, sides=5, material=C['steel']))

    # ---- small cargo + lamp --------------------------------------------------
    for i in range(3):
        parts.append(kit.rock(f'parcel_{i}', 0.38, seed=70 + i, squash=0.8,
                              subdiv=1, loc=(-0.45 + i * 0.45, -0.35, 0.86),
                              material=N['filter_paper']))
    parts.append(kit.cyl('lamp', 0.20, 0.18, sides=8, loc=(0, 1.55, 1.05),
                         rot=(math.pi / 2, 0, 0), material=C['lamp']))

    body = kit.join('rickshaw_combine_body', parts)
    kit.flat(body)
    root = kit.marker('rickshaw_combine', (0, 0, 0), size=0.9)
    body.parent = root
    kit.marker('mount_cargo', (0, -0.4, 0.9), root, kind='ARROWS')
    kit.marker('cam_driver', (0, 0.9, 1.5), root, kind='ARROWS')
    kit.marker('wheel_front', (0, 2.05, RF), root, size=0.3)
    kit.marker('wheel_rear_l', (-1.05, -1.1, RR), root, size=0.3)
    kit.marker('wheel_rear_r', (1.05, -1.1, RR), root, size=0.3)
    return root
