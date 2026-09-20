"""
Combine bomber -- the strategic strike mission (design doc section 6).

Slow, heavy, two-seat. Goes deep across the water to hit what the enemy
cannot move: pump works, slipways, granaries, the far hauler at anchor. Needs
the fighter to survive the trip.

Provenance: matchbox fuselage, foil slab wing, twin rubber-band motors, and a
single precious ball bearing slung under the belly.
"""
import math
import kit
import palette

TAU = math.pi * 2


def ring(r, n=8):
    return [(math.cos(TAU * i / n + 0.39) * r,
             math.sin(TAU * i / n + 0.39) * r) for i in range(n)]


def build():
    kit.reset()
    C = palette.combine()
    N = palette.neutral()
    parts = []

    # ---- matchbox fuselage -------------------------------------------------
    parts.append(kit.loft('fuselage', [
        (-4.6, ring(0.22)), (-4.0, ring(0.50)), (-2.4, ring(0.72)),
        (0.0, ring(0.86)), (2.2, ring(0.82)), (3.6, ring(0.60)),
        (4.5, ring(0.34)), (4.9, ring(0.15)),
    ], material=C['steel']))
    parts.append(kit.box('box_sides', (1.55, 5.2, 1.30), loc=(0, 0.2, 0),
                         material=C['can_red']))
    parts.append(kit.loft('canopy', [
        (2.5, ring(0.16)), (1.9, ring(0.44)), (0.5, ring(0.48)),
        (-0.5, ring(0.22)),
    ], loc=(0, 0, 0.62), material=C['glass']))

    # ---- foil slab wing ----------------------------------------------------
    wing = [(-6.2, -0.55), (-6.2, -1.45), (-1.3, -2.05), (0, -1.9),
            (1.3, -2.05), (6.2, -1.45), (6.2, -0.55), (0, 1.35)]
    parts.append(kit.plate('wing', wing, 0.16, loc=(0, 0.35, 0.30),
                           material=C['foil']))
    parts.append(kit.tube('wing_le', [(-6.2, -0.15, 0.30), (0, 1.75, 0.30),
                                      (6.2, -0.15, 0.30)], 0.10, sides=6,
                          material=C['steel']))

    # ---- twin rubber-band motors -------------------------------------------
    for sx in (-2.8, 2.8):
        parts.append(kit.loft(f'nacelle_{sx}', [
            (-1.5, ring(0.20)), (-1.0, ring(0.42)), (0.8, ring(0.46)),
            (1.6, ring(0.26)),
        ], loc=(sx, 0.7, 0.34), material=C['steel_dark']))
        parts.append(kit.cyl(f'spinner_{sx}', 0.18, 0.28, sides=8,
                             loc=(sx, 2.42, 0.34), rot=(math.pi / 2, 0, 0),
                             material=C['rust']))
        parts.append(kit.plate(f'prop_{sx}', [(-0.09, -1.15), (0.13, -0.98),
                                              (0.13, 0.98), (-0.09, 1.15)],
                               0.05, loc=(sx, 2.56, 0.34),
                               rot=(math.pi / 2, 0, 0), material=C['bone']))

    # ---- twin tail ----------------------------------------------------------
    parts.append(kit.plate('stab', [(-2.2, -0.75), (-2.2, -0.15),
                                    (2.2, -0.15), (2.2, -0.75)], 0.12,
                           loc=(0, -4.0, 0.25), material=C['foil']))
    # plate() extrudes its XY outline along Z, so a vertical fin needs the
    # outline as (chord, height) and rot (90,0,90) -- rotating a thin slab
    # about Y instead just turns the THICKNESS into the chord and gives a box.
    for sx in (-2.05, 2.05):
        parts.append(kit.plate(f'fin_{sx}', [(-0.72, 0.0), (0.72, 0.0),
                                             (0.46, 1.30), (-0.42, 1.30)],
                               0.10, loc=(sx, -4.05, 0.30),
                               rot=(math.pi / 2, 0, math.pi / 2),
                               material=C['foil']))

    # ---- open bomb bay, one precious ball bearing ---------------------------
    parts.append(kit.box('bay', (1.15, 2.3, 0.22), loc=(0, 0.1, -0.72),
                         material=C['steel_dark']))
    for sx in (-0.62, 0.62):
        parts.append(kit.plate(f'baydoor_{sx}', [(0, -1.1), (0, 1.1),
                                                 (sx * 0.62, 1.0),
                                                 (sx * 0.62, -1.0)], 0.07,
                               loc=(sx, 0.1, -0.95), rot=(sx * 0.9, 0, 0),
                               material=C['foil']))
    parts.append(kit.rock('bearing', 0.52, seed=3, roughness=0.02, subdiv=2,
                          squash=1.0, loc=(0, 0.1, -1.05),
                          material=N['steel_bright']))
    for sx in (-1.8, 1.8):                  # matchhead incendiaries on rails
        parts.append(kit.cyl(f'incend_{sx}', 0.17, 1.5, sides=7,
                             loc=(sx, -0.3, -0.62), rot=(math.pi / 2, 0, 0),
                             material=N['match_wood']))
        parts.append(kit.cyl(f'incend_h_{sx}', 0.25, 0.42, sides=7,
                             loc=(sx, 0.55, -0.62), rot=(-math.pi / 2, 0, 0),
                             material=N['match_head']))
    parts.append(kit.cyl('turret', 0.42, 0.34, sides=9, loc=(0, -2.5, 0.78),
                         material=C['steel_dark']))
    parts.append(kit.cyl('tailgun', 0.06, 1.1, sides=5, loc=(0, -2.95, 0.86),
                         rot=(math.pi / 2, 0, 0), material=C['steel_dark']))

    body = kit.join('bomber_combine_body', parts)
    kit.flat(body)
    root = kit.marker('bomber_combine', (0, 0, 0), size=1.8)
    body.parent = root
    kit.marker('mount_bombbay', (0, 0.1, -1.0), root, kind='ARROWS')
    kit.marker('cam_pilot', (0, 1.2, 0.95), root, kind='ARROWS')
    kit.marker('cam_bombardier', (0, 1.9, -0.3), root, kind='ARROWS')
    kit.marker('fx_engine_l', (-2.8, 2.6, 0.34), root, kind='CONE')
    kit.marker('fx_engine_r', (2.8, 2.6, 0.34), root, kind='CONE')
    kit.marker('fx_tailgun', (0, -3.4, 0.86), root, kind='CONE')
    return root
