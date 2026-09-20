"""Render every asset from a matched 3/4 angle into one contact sheet."""
import sys, os, subprocess
sys.path.insert(0, 'lib'); sys.path.insert(0, 'assets')

SHOTS = [
    ('hauler_combine',  80, 58, 17, 68, (2, 0, 0.5), -5.4),
    ('fighter_combine', 13, 48, 20, 62, (0, 0, 0.1), -0.9),
    ('tank_combine',    22, 52, 22, 62, (0, 0, 1.2), -0.05),
    ('bike_combine',     9, 50, 26, 58, (0, 0, 0.7), -0.05),
    ('props_kit',       96, 40, 30, 55, (-6, 0, 1.0), -0.05),
    ('hauler_reedfolk', 80, 58, 17, 68, (2, 0, 0.5), -5.4),
]
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/sheet'
only = sys.argv[2:] if len(sys.argv) > 2 else None

for name, dist, az, el, lens, tgt, gz in SHOTS:
    if only and name not in only:
        continue
    if not os.path.exists(f'assets/{name}.py'):
        continue
    code = f'''
import sys; sys.path.insert(0,"lib"); sys.path.insert(0,"assets")
import kit, render, {name} as A
A.build()
render.world(); render.three_point(scale=max(6,{dist}*0.28)); render.ground(z={gz})
render.camera(target={tgt}, dist={dist}, azim={az}, elev={el}, lens={lens})
render.shot("{OUT}/{name}.png", res=(760,470), samples=18)
print("TRIS", "{name}", kit.tris())
'''
    r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True)
    line = [l for l in r.stdout.splitlines() if l.startswith('TRIS')]
    print(line[0] if line else f'FAIL {name}: {r.stderr.strip().splitlines()[-3:]}')
