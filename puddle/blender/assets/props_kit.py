"""
Theater 1 prop kit -- the found objects the tribes inherited but did not make.

At this scale a staple is a bridge, a bottle cap is a bunker and a cigarette
filter is a sandbag (art bible 6.3). Everything is modelled at the size it
would actually be relative to a 30 m hauler.

Exports as one kit; each prop is its own top-level object so Godot can split
them into separate scenes on import.
"""
import math
import kit
import palette


def bottlecap(x):
    N = palette.neutral()
    cap = kit.crimped_disc('prop_bottlecap', 3.6, 1.30, flutes=21,
                           flute_depth=0.11, loc=(x, 0, 0.65),
                           material=N['cap_paint'])
    inner = kit.crimped_disc('_ci', 3.15, 0.30, flutes=21, flute_depth=0.10,
                             loc=(x, 0, 1.24), material=N['filter_stain'])
    return kit.flat(kit.join('prop_bottlecap', [cap, inner]))


def staple(x):
    N = palette.neutral()
    p = [(x - 5.8, 0, 0.0), (x - 5.8, 0, 2.6), (x - 5.4, 0, 3.0),
         (x + 5.4, 0, 3.0), (x + 5.8, 0, 2.6), (x + 5.8, 0, 0.0)]
    return kit.flat(kit.tube('prop_staple', p, 0.55, sides=7, material=N['zinc']))


def matchstick(x):
    N = palette.neutral()
    stick = kit.cyl('_ms', 0.62, 18.0, sides=8, loc=(x, 0, 0.62),
                    rot=(math.pi / 2, 0, 0), material=N['match_wood'])
    head = kit.cyl('_mh', 0.95, 2.4, sides=8, radius_top=0.70,
                   loc=(x, 9.6, 0.62), rot=(-math.pi / 2, 0, 0),
                   material=N['match_head'])
    return kit.flat(kit.join('prop_matchstick', [stick, head]))


def cig_filter(x):
    N = palette.neutral()
    body = kit.cyl('_cf', 1.45, 7.6, sides=10, loc=(x, 0, 1.45),
                   rot=(math.pi / 2, 0, 0), material=N['filter_paper'])
    stain = kit.cyl('_cs', 1.50, 1.8, sides=10, loc=(x, -3.0, 1.45),
                    rot=(math.pi / 2, 0, 0), material=N['filter_stain'])
    burn = kit.cyl('_cb', 1.38, 0.5, sides=10, loc=(x, 3.7, 1.45),
                   rot=(math.pi / 2, 0, 0), material=N['grit'])
    return kit.flat(kit.join('prop_cig_filter', [body, stain, burn]))


def screw(x):
    N = palette.neutral()
    parts = [kit.cyl('_ss', 0.85, 9.0, sides=8, radius_top=0.45,
                     loc=(x, 0, 0.85), rot=(math.pi / 2, 0, 0),
                     material=N['steel_bright'])]
    parts.append(kit.cyl('_sh', 1.75, 0.9, sides=10, loc=(x, -4.9, 0.85),
                         rot=(math.pi / 2, 0, 0), material=N['steel_bright']))
    for r in (0, 1):
        parts.append(kit.box('_sl', (2.9, 0.34, 0.34) if r else (0.34, 0.34, 2.9),
                             loc=(x, -5.35, 0.85), material=N['grit']))
    thread = kit.helix((x, -4.2, 0.85), 8.0, 0.78, turns=7.0, steps=90, axis='Y')
    parts.append(kit.tube('_st', thread, 0.16, sides=4,
                          material=N['steel_bright']))
    return kit.flat(kit.join('prop_screw', parts))


def paperclip(x):
    N = palette.neutral()
    p = [(x + 3.4, -4.6, 0.4), (x + 3.4, 3.6, 0.4)]
    p += kit.arc((x, 3.6, 0.4), 3.4, 0.0, math.pi, steps=8)
    p += [(x - 3.4, -3.0, 0.4)]
    p += kit.arc((x, -3.0, 0.4), 2.1, math.pi, math.tau, steps=8)
    p += [(x + 2.1, 2.4, 0.4)]
    return kit.flat(kit.tube('prop_paperclip', p, 0.40, sides=6,
                             material=N['steel_bright']))


def pebbles(x):
    N = palette.neutral()
    out = []
    for i, (r, sd, mtl) in enumerate(((4.2, 11, 'pebble'), (2.4, 27, 'pebble_pale'),
                                      (1.3, 43, 'grit'))):
        out.append(kit.flat(kit.rock(f'prop_pebble_{"abc"[i]}', r, seed=sd,
                                     squash=0.62, subdiv=1,
                                     loc=(x + i * 9.0, 0, r * 0.55),
                                     material=N[mtl])))
    return out


def build():
    kit.reset()
    roots = [bottlecap(-46), staple(-34), matchstick(-18), cig_filter(-4),
             screw(8), paperclip(20)] + pebbles(30)
    root = kit.marker('props_kit', (0, 0, 0), size=2.0)
    for r in roots:
        r.parent = root
    return root
