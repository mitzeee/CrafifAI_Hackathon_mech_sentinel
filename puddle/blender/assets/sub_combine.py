"""
Combine submarine -- the reconnaissance mission (design doc section 6).

Goes under to watch and listen: count the enemy fleet, photograph the shore,
tap a cable, and come home without being seen. Carries torpedoes it would
rather not use, because firing them ends the mission.

Provenance: a sealed pill capsule, wire planes, a glass porthole, a drinking-
straw snorkel. Origin at the waterline so it can run surfaced or trimmed down.
"""
import math
import kit
import palette

TAU = math.pi * 2


def ring(r, n=12, cz=0.0):
    return [(math.cos(TAU * i / n + 0.26) * r,
             math.sin(TAU * i / n + 0.26) * r + cz) for i in range(n)]


def build():
    kit.reset()
    C = palette.combine()
    N = palette.neutral()
    parts = []
    CZ = -0.55

    # ---- capsule hull: two halves of a pill, with the joint ring showing ---
    parts.append(kit.loft('hull', [
        (-7.4, ring(0.34, cz=CZ)), (-7.0, ring(0.95, cz=CZ)),
        (-6.2, ring(1.45, cz=CZ)), (-4.6, ring(1.72, cz=CZ)),
        (-0.3, ring(1.80, cz=CZ)), (-0.1, ring(1.86, cz=CZ)),
        (0.1, ring(1.86, cz=CZ)), (0.3, ring(1.78, cz=CZ)),
        (4.4, ring(1.70, cz=CZ)), (6.1, ring(1.35, cz=CZ)),
        (7.0, ring(0.85, cz=CZ)), (7.45, ring(0.30, cz=CZ)),
    ], material=C['bone']))
    # the capsule's coloured half
    parts.append(kit.loft('cap_half', [
        (-7.05, ring(0.98, cz=CZ)), (-6.25, ring(1.48, cz=CZ)),
        (-4.6, ring(1.75, cz=CZ)), (-0.15, ring(1.84, cz=CZ)),
    ], cap_start=False, cap_end=False, material=C['can_red']))

    # ---- conning tower, porthole, snorkel, periscope -----------------------
    parts.append(kit.loft('sail', [
        (-1.3, [(0.52, 1.12), (0.44, 2.05), (-0.44, 2.05), (-0.52, 1.12)]),
        (1.5, [(0.52, 1.12), (0.44, 2.05), (-0.44, 2.05), (-0.52, 1.12)]),
        (2.1, [(0.40, 1.12), (0.32, 1.85), (-0.32, 1.85), (-0.40, 1.12)]),
    ], material=C['steel_dark']))
    parts.append(kit.cyl('porthole', 0.34, 0.16, sides=10, loc=(0, 2.9, 0.15),
                         rot=(math.pi / 2, 0, 0), material=C['glass']))
    parts.append(kit.cyl('porthole_rim', 0.42, 0.12, sides=10, loc=(0, 2.86, 0.15),
                         rot=(math.pi / 2, 0, 0), material=N['steel_bright']))
    parts.append(kit.tube('periscope', [(0.18, 0.4, 2.0), (0.18, 0.4, 3.5),
                                        (0.55, 0.75, 3.5)],
                          0.085, sides=6, material=C['steel']))
    parts.append(kit.tube('snorkel', [(-0.26, -0.5, 2.0), (-0.26, -0.5, 3.1)],
                          0.14, sides=6, material=N['filter_paper']))

    # ---- planes, screw, torpedo tubes --------------------------------------
    for sx in (-1, 1):
        parts.append(kit.plate(f'plane_{sx}', [(0, -0.55), (sx * 2.5, -0.35),
                                               (sx * 2.5, 0.35), (0, 0.55)],
                               0.12, loc=(0, -5.2, CZ + 0.1), material=C['foil']))
    parts.append(kit.plate('fin_top', [(-0.85, 0.0), (0.85, 0.0),
                                       (0.45, 1.55), (-0.55, 1.55)], 0.10,
                           loc=(0, -6.2, CZ + 0.4),
                           rot=(math.pi / 2, 0, math.pi / 2),
                           material=C['foil']))
    parts.append(kit.cyl('screw_hub', 0.22, 0.4, sides=8, loc=(0, -7.6, CZ),
                         rot=(math.pi / 2, 0, 0), material=C['brass']))
    for k in range(3):
        a = TAU * k / 3
        parts.append(kit.plate(f'blade_{k}', [(-0.16, 0), (0.16, 0.1),
                                              (0.12, 0.85), (-0.12, 0.85)],
                               0.06, loc=(math.cos(a) * 0.4, -7.75,
                                          CZ + math.sin(a) * 0.4),
                               rot=(math.pi / 2, 0, a), material=C['brass']))
    for sx in (-0.7, 0.7):
        parts.append(kit.cyl(f'tube_{sx}', 0.26, 0.3, sides=8,
                             loc=(sx, 7.25, CZ - 0.2), rot=(math.pi / 2, 0, 0),
                             material=C['steel_dark']))

    body = kit.join('sub_combine_body', parts)
    kit.flat(body)
    root = kit.marker('sub_combine', (0, 0, 0), size=1.6)
    body.parent = root
    kit.marker('mount_periscope', (0.55, 0.75, 3.5), root, kind='ARROWS')
    kit.marker('cam_periscope', (0.55, 0.75, 3.6), root, kind='ARROWS')
    kit.marker('fx_torpedo_l', (-0.7, 7.5, CZ - 0.2), root, kind='CONE')
    kit.marker('fx_torpedo_r', (0.7, 7.5, CZ - 0.2), root, kind='CONE')
    kit.marker('fx_screw', (0, -7.9, CZ), root, kind='CONE')
    kit.marker('waterline', (0, 0, 0), root, size=3.0, kind='CIRCLE')
    kit.buoyancy_probes(root, half_len=6.0, half_beam=1.4, z=0.0, n=3)
    return root
