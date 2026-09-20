"""
Combine supply lorry -- the land logistics mission (design doc section 6).

Runs rations and raw materials up to the front under threat. Slow, loud,
loaded, and completely defenceless: this mission is about route, timing and
not being seen, not about fighting.

Provenance: matchbox body, button wheels, foil tilt over wire hoops,
bottle-cap fuel drum. Origin on the ground plane.
"""
import math
import kit
import palette


def button_wheel(name, sx, sy, r, C, N):
    out = [kit.cyl(f'{name}_t', r, 0.62, sides=11, loc=(sx, sy, r),
                   rot=(0, math.pi / 2, 0), material=C['rubber'])]
    for dx in (-0.34, 0.34):
        out.append(kit.cyl(f'{name}_f', r * 0.62, 0.10, sides=9,
                           loc=(sx + dx, sy, r), rot=(0, math.pi / 2, 0),
                           material=N['steel_bright']))
    return out


def build():
    kit.reset()
    C = palette.combine()
    N = palette.neutral()
    parts = []
    R = 0.72

    # ---- matchbox chassis + cab ------------------------------------------
    parts.append(kit.box('chassis', (2.9, 9.4, 0.5), loc=(0, 0, 0.92),
                         material=C['steel_dark']))
    parts.append(kit.box('cab', (2.7, 2.6, 1.9), loc=(0, 2.9, 2.15),
                         material=C['can_red']))
    parts.append(kit.box('screen', (2.3, 0.18, 0.9), loc=(0, 4.15, 2.55),
                         material=C['glass']))
    parts.append(kit.box('bonnet', (2.5, 1.5, 1.0), loc=(0, 4.9, 1.65),
                         material=C['can_red']))
    parts.append(kit.box('grille', (2.2, 0.20, 0.7), loc=(0, 5.62, 1.55),
                         material=N['steel_bright']))
    for sx in (-0.95, 0.95):
        parts.append(kit.cyl('lamp', 0.26, 0.22, sides=8, loc=(sx, 5.6, 2.05),
                             rot=(math.pi / 2, 0, 0), material=C['lamp']))

    # ---- cargo bed, loaded with sacks -------------------------------------
    parts.append(kit.box('bed', (2.9, 5.6, 0.22), loc=(0, -1.5, 1.24),
                         material=N['match_wood']))
    for sx in (-1.42, 1.42):
        parts.append(kit.box('bedside', (0.18, 5.6, 0.85), loc=(sx, -1.5, 1.68),
                             material=N['match_wood']))
    parts.append(kit.box('tailgate', (2.9, 0.18, 0.85), loc=(0, -4.25, 1.68),
                         material=N['match_wood']))
    for i in range(6):                      # ration sacks
        sx = -0.7 + (i % 2) * 1.4
        sy = -3.3 + (i // 2) * 1.7
        parts.append(kit.rock(f'sack_{i}', 0.62, seed=30 + i, squash=0.78,
                              subdiv=1, loc=(sx, sy, 1.85),
                              material=N['filter_paper']))

    # ---- foil tilt over wire hoops -----------------------------------------
    for i in range(4):
        sy = -3.9 + i * 1.6
        parts.append(kit.tube(f'hoop_{i}', kit.arc((0, sy, 1.6), 1.45,
                                                   0.0, math.pi, steps=8,
                                                   plane='XZ'),
                              0.07, sides=5, material=C['steel']))
    parts.append(kit.loft('tilt', [
        (-4.35, [(1.45, 1.62), (1.05, 2.78), (0, 3.06), (-1.05, 2.78),
                 (-1.45, 1.62)]),
        (1.45, [(1.45, 1.62), (1.05, 2.78), (0, 3.06), (-1.05, 2.78),
                (-1.45, 1.62)]),
    ], cap_start=False, cap_end=False, material=C['foil']))

    # ---- running gear, fuel drum, exhaust ----------------------------------
    for sy in (3.5, -0.9, -2.9):
        for sx in (-1.55, 1.55):
            parts += button_wheel(f'w{sy}{sx}', sx, sy, R, C, N)
    parts.append(kit.crimped_disc('drum', 0.70, 1.15, flutes=13,
                                  flute_depth=0.10, loc=(-1.75, 1.2, 1.55),
                                  rot=(0, math.pi / 2, 0),
                                  material=C['rust']))
    parts.append(kit.tube('exhaust', [(1.6, 1.4, 1.2), (1.6, 1.4, 3.3)],
                          0.14, sides=6, material=C['steel_dark']))

    body = kit.join('truck_combine_body', parts)
    kit.flat(body)
    root = kit.marker('truck_combine', (0, 0, 0), size=1.4)
    body.parent = root
    kit.marker('mount_cargo', (0, -1.5, 1.9), root, kind='ARROWS')
    kit.marker('cam_cab', (0, 3.2, 2.6), root, kind='ARROWS')
    kit.marker('fx_exhaust', (1.6, 1.4, 3.4), root, kind='CONE')
    for sy in (3.5, -0.9, -2.9):
        for sx in (-1.55, 1.55):
            kit.marker(f'wheel_{sy}_{sx}', (sx, sy, R), root, size=0.3)
    return root
