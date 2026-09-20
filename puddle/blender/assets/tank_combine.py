"""
Combine tank -- the shore war (design doc section 6). Wades to a fixed depth,
and that depth is a live tactical question every act.

Provenance: bottle-cap hull on watch-gear road wheels, nail-barrel gun,
bent-staple applique armour. Origin on the ground plane, not the waterline.
"""
import math
import kit
import palette


def build():
    kit.reset()
    C = palette.combine()
    parts = []

    # ---- bottle-cap hull, stretched fore-and-aft -------------------------
    hull = kit.crimped_disc('hull', 2.95, 1.55, flutes=19, flute_depth=0.09,
                            loc=(0, 0, 1.15), material=C['can_red'])
    hull.scale = (1.0, 1.38, 1.0)
    kit.apply_transform(hull)
    parts.append(hull)
    parts.append(kit.box('glacis', (3.4, 1.5, 0.55), loc=(0, 2.9, 1.15),
                         rot=(-0.5, 0, 0), material=C['steel']))

    # ---- watch-gear running gear ------------------------------------------
    for side in (-1, 1):
        sx = side * 2.62
        parts.append(kit.box(f'track_{side}', (0.90, 6.5, 1.10),
                             loc=(sx, 0, 0.60), material=C['rubber']))
        for sy in (-3.25, 3.25):
            parts.append(kit.cyl(f'idler_{side}_{sy}', 0.55, 0.90, sides=10,
                                 loc=(sx, sy, 0.60), rot=(0, math.pi / 2, 0),
                                 material=C['rubber']))
        # tread cleats
        for k in range(9):
            parts.append(kit.box('cleat', (1.02, 0.22, 1.16),
                                 loc=(sx, -3.2 + k * 0.80, 0.60),
                                 material=C['steel_dark']))
        # Watch-gear road wheels sit PROUD of the track on the outer face --
        # inboard they just punch through the tread and read as debris.
        gx = sx + side * 0.62
        for k in range(3):
            sy = -2.1 + k * 2.1
            parts.append(kit.cyl(f'wheel_{side}_{k}', 0.62, 0.26, sides=12,
                                 loc=(gx, sy, 0.60), rot=(0, math.pi / 2, 0),
                                 material=C['brass']))
            for tth in range(10):
                a = math.tau * tth / 10
                parts.append(kit.box('tooth', (0.24, 0.15, 0.15),
                                     loc=(gx, sy + math.cos(a) * 0.70,
                                          0.60 + math.sin(a) * 0.70),
                                     material=C['brass']))

    # ---- bent-staple applique armour ---------------------------------------
    for k, sy in enumerate((3.2, 2.5)):
        parts.append(kit.tube(f'staple_{k}',
                              [(-1.5, sy, 1.05), (-1.5, sy + 0.5, 1.55),
                               (1.5, sy + 0.5, 1.55), (1.5, sy, 1.05)],
                              0.12, sides=5, material=C['zinc'] if 'zinc' in C
                              else C['foil']))

    body = kit.join('tank_combine_body', parts)
    kit.flat(body)

    # ---- turret: separate object, Godot rotates it about Z ----------------
    tparts = [kit.crimped_disc('turret_cap', 1.85, 1.05, flutes=15,
                               flute_depth=0.10, material=C['steel'])]
    tparts.append(kit.box('mantlet', (1.0, 0.8, 0.8), loc=(0, 1.5, 0.05),
                          material=C['steel_dark']))
    # the gun is a nail: tapered shank, flat head at the breech
    tparts.append(kit.cyl('barrel', 0.24, 4.6, sides=8, radius_top=0.13,
                          loc=(0, 3.9, 0.05), rot=(-math.pi / 2, 0, 0),
                          material=C['steel_dark']))
    tparts.append(kit.cyl('nail_head', 0.52, 0.22, sides=8, loc=(0, 1.62, 0.05),
                          rot=(math.pi / 2, 0, 0), material=C['foil']))
    tparts.append(kit.cyl('cupola', 0.52, 0.42, sides=8, loc=(-0.55, -0.5, 0.72),
                          material=C['rust']))
    turret = kit.join('tank_combine_turret', tparts)
    turret.location = (0, -0.3, 2.45)
    kit.flat(turret)

    root = kit.marker('tank_combine', (0, 0, 0), size=1.5)
    body.parent = root
    turret.parent = root
    kit.marker('mount_turret_ring', (0, -0.3, 2.45), root, kind='CIRCLE', size=1.9)
    kit.marker('fx_muzzle', (0, 6.2, 2.50), turret, kind='CONE')
    kit.marker('fx_exhaust', (-1.9, -3.1, 1.6), root, kind='CONE')
    for side in (-1, 1):
        for k in range(3):
            kit.marker(f'wheel_{"L" if side < 0 else "R"}{k}',
                       (side * 2.62, -2.1 + k * 2.1, 0.60), root, size=0.4)
    return root
