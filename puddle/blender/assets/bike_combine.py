"""
Combine motorcycle -- recon, courier, sabotage (design doc section 6). Rides
the meniscus itself above a threshold speed; lose speed over deep water and
you sink. The trailer role.

Provenance: thread-spool wheels, spring-coil backbone, matchstick forks,
foil fairing.
"""
import math
import kit
import palette


def spool(name, sx, sy, r, mats):
    """A cotton reel: narrow hub, wide flanges. Reads instantly at any size."""
    # The spool reads as a WHEEL only if the dark tyre dominates and the
    # flanges are thin rims. Pale full-radius flanges read as loose discs.
    out = [kit.cyl(f'{name}_tyre', r * 0.94, 0.52, sides=12, loc=(sx, sy, r),
                   rot=(0, math.pi / 2, 0), material=mats['rubber'])]
    for dx in (-0.29, 0.29):
        out.append(kit.cyl(f'{name}_flange', r, 0.09, sides=12,
                           loc=(sx + dx, sy, r), rot=(0, math.pi / 2, 0),
                           material=mats['steel_dark']))
    out.append(kit.cyl(f'{name}_hub', r * 0.34, 0.66, sides=8, loc=(sx, sy, r),
                       rot=(0, math.pi / 2, 0), material=mats['brass']))
    return out


def build():
    kit.reset()
    C = palette.combine()
    N = palette.neutral()
    M = dict(C)
    M['match_wood'] = N['match_wood']
    parts = []

    R_REAR, R_FRONT = 0.54, 0.50
    parts += spool('rear', 0.0, -1.35, R_REAR, M)
    parts += spool('front', 0.0, 1.35, R_FRONT, M)

    # ---- spring-coil backbone ---------------------------------------------
    parts.append(kit.tube('spring', kit.helix((0, -1.25, 0.66), 2.10, 0.19,
                                              turns=6.5, steps=84, axis='Y'),
                          0.075, sides=5, material=C['steel']))
    parts.append(kit.tube('spine', [(0, -1.35, 0.68), (0, 1.15, 0.62)],
                          0.075, sides=6, material=C['steel_dark']))

    # ---- matchstick forks ---------------------------------------------------
    # forks must actually reach the front axle, or the wheel reads as loose
    for sx in (-0.22, 0.22):
        parts.append(kit.tube(f'fork_{sx}', [(sx, 1.35, R_FRONT),
                                             (sx, 1.10, 1.32)],
                              0.075, sides=6, material=N['match_wood']))
        parts.append(kit.cyl(f'fork_head_{sx}', 0.115, 0.22, sides=6,
                             loc=(sx, 1.06, 1.42), rot=(0.55, 0, 0),
                             material=N['match_head']))
    parts.append(kit.tube('steer', [(0, 1.12, 1.26), (0, 0.55, 0.90)],
                          0.07, sides=6, material=C['steel']))
    parts.append(kit.tube('bars', [(-0.48, 1.02, 1.30), (0, 1.12, 1.34),
                                   (0.48, 1.02, 1.30)], 0.055, sides=6,
                          material=C['steel']))

    # ---- foil fairing + seat -------------------------------------------------
    parts.append(kit.plate('fairing', [(-0.46, -0.35), (-0.30, 0.72),
                                       (0.30, 0.72), (0.46, -0.35)], 0.06,
                           loc=(0, 0.50, 0.98), rot=(0.30, 0, 0),
                           material=C['foil']))
    parts.append(kit.box('seat', (0.40, 0.95, 0.18), loc=(0, -0.60, 0.86),
                         material=C['rubber']))
    parts.append(kit.box('tail_box', (0.38, 0.50, 0.34), loc=(0, -1.15, 0.92),
                         material=C['rust']))
    # spray deflectors -- this bike lives on the meniscus
    for sx in (-1, 1):
        parts.append(kit.plate(f'skirt_{sx}', [(0, -0.5), (0, 0.5),
                                               (sx * 0.30, 0.42),
                                               (sx * 0.30, -0.42)], 0.05,
                               loc=(sx * 0.38, -1.35, 0.26), material=C['foil']))

    body = kit.join('bike_combine_body', parts)
    kit.flat(body)

    root = kit.marker('bike_combine', (0, 0, 0), size=0.8)
    body.parent = root
    kit.marker('mount_rider', (0, -0.50, 1.05), root, kind='ARROWS')
    kit.marker('wheel_front', (0, 1.35, R_FRONT), root, size=0.4)
    kit.marker('wheel_rear', (0, -1.35, R_REAR), root, size=0.4)
    kit.marker('fx_spray_front', (0, 1.35, 0.06), root, kind='CONE')
    kit.marker('fx_spray_rear', (0, -1.35, 0.06), root, kind='CONE')
    kit.marker('cam_chase', (0, -3.2, 1.6), root, kind='ARROWS')
    return root
