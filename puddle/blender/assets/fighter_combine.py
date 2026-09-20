"""
Combine fighter -- air superiority, bomber escort, and dragonfly interception
(design doc section 6). Launched off the hauler's rubber-band torsion rail.

Provenance: paperclip-wire frame, stretched membrane wing, matchbox nose,
rubber-band-driven prop. Fragile, fast, disposable.
"""
import math
import kit
import palette


def build():
    kit.reset()
    C = palette.combine()
    parts = []

    # ---- fuselage: a wire-frame spindle ---------------------------------
    def ring(r, n=8):
        return [(math.cos(math.tau * i / n + 0.39) * r,
                 math.sin(math.tau * i / n + 0.39) * r) for i in range(n)]

    parts.append(kit.loft('fuselage', [
        (-2.50, ring(0.10)), (-2.10, ring(0.26)), (-1.30, ring(0.36)),
        (-0.30, ring(0.48)), (0.60, ring(0.46)), (1.50, ring(0.34)),
        (2.25, ring(0.22)), (2.55, ring(0.13)),
    ], material=C['steel']))

    # ---- membrane wing ---------------------------------------------------
    wing = [(-3.05, -0.30), (-3.05, -0.86), (-0.55, -1.25), (0.00, -1.10),
            (0.55, -1.25), (3.05, -0.86), (3.05, -0.30), (0.00, 0.92)]
    parts.append(kit.plate('wing', wing, 0.07, loc=(0, 0.05, 0.16),
                           material=C['membrane']))
    # paperclip leading edge + spar
    parts.append(kit.tube('wing_le', [(-3.05, -0.25, 0.16), (0, 0.97, 0.16),
                                      (3.05, -0.25, 0.16)], 0.065, sides=6,
                          material=C['steel']))
    parts.append(kit.tube('wing_spar', [(-3.05, -0.75, 0.16), (0, -0.55, 0.16),
                                        (3.05, -0.75, 0.16)], 0.05, sides=6,
                          material=C['steel']))
    for sx in (-2.3, -1.4, -0.7, 0.7, 1.4, 2.3):
        t = abs(sx) / 3.05
        le = 0.92 - t * 1.22
        te = -1.15 + t * 0.30
        parts.append(kit.tube(f'rib_{sx}', [(sx, le, 0.16), (sx, te, 0.16)],
                              0.035, sides=4, material=C['steel']))

    # ---- V-tail ----------------------------------------------------------
    # V-tail: rotate about Y so each fin lifts outboard into the vee
    tail = [(0.0, -0.60), (0.0, 0.40), (1.15, 0.36), (1.15, -0.02)]
    for side in (-1, 1):
        parts.append(kit.plate(f'tail_{side}', [(x * side, y) for x, y in tail],
                               0.06, loc=(0, -2.10, 0.20),
                               rot=(0, -side * 0.95, 0), material=C['membrane']))
    parts.append(kit.tube('tail_boom', [(0, -1.6, 0.05), (0, -2.45, 0.18)],
                          0.07, sides=6, material=C['steel']))

    # ---- canopy, prop, launch lug ---------------------------------------
    parts.append(kit.loft('canopy', [
        (0.95, ring(0.10)), (0.65, ring(0.26)), (0.05, ring(0.28)),
        (-0.45, ring(0.13)),
    ], material=C['glass']))
    parts.append(kit.cyl('spinner', 0.16, 0.30, sides=8, loc=(0, 2.68, 0),
                         rot=(math.pi / 2, 0, 0), material=C['rust']))
    parts.append(kit.box('lug', (0.16, 0.9, 0.34), loc=(0, 0.1, -0.55),
                         material=C['steel_dark']))
    for sx in (-1.0, 1.0):
        parts.append(kit.cyl('gun', 0.05, 0.8, sides=6, loc=(sx, 0.35, 0.12),
                             rot=(math.pi / 2, 0, 0), material=C['steel_dark']))

    body = kit.join('fighter_combine_body', parts)
    kit.flat(body)

    # rubber-band prop stays separate so Godot can spin it
    blade_a = kit.plate('pb_a', [(-0.07, -0.92), (0.11, -0.78), (0.11, 0.78),
                                 (-0.07, 0.92)], 0.04, material=C['bone'])
    blade_b = kit.plate('pb_b', [(-0.05, -0.34), (0.05, -0.34), (0.05, 0.34),
                                 (-0.05, 0.34)], 0.10, material=C['rust'])
    prop = kit.join('fighter_combine_prop', [blade_a, blade_b])
    prop.rotation_euler = (math.pi / 2, 0, 0)
    kit.apply_transform(prop)
    prop.location = (0, 2.80, 0)
    kit.flat(prop)

    root = kit.marker('fighter_combine', (0, 0, 0), size=1.2)
    body.parent = root
    prop.parent = root
    kit.marker('mount_hardpoint_l', (-1.6, -0.2, 0.05), root)
    kit.marker('mount_hardpoint_r', (1.6, -0.2, 0.05), root)
    kit.marker('mount_launch_lug', (0, 0.1, -0.75), root, kind='ARROWS')
    kit.marker('cam_cockpit', (0, 0.35, 0.50), root, kind='ARROWS')
    kit.marker('fx_muzzle_l', (-1.0, 0.80, 0.12), root, kind='CONE')
    kit.marker('fx_muzzle_r', (1.0, 0.80, 0.12), root, kind='CONE')
    kit.marker('fx_wingtip_l', (-3.05, -0.55, 0.16), root, kind='CONE')
    kit.marker('fx_wingtip_r', (3.05, -0.55, 0.16), root, kind='CONE')
    return root
