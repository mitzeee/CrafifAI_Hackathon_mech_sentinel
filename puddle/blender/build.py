#!/usr/bin/env python3
"""
Build the whole fleet: every asset -> assets/glb/<name>.glb + assets/blend/.

    python3 build.py            # everything
    python3 build.py tank_combine

Each asset is built in a fresh subprocess because bpy holds one global scene
and asset modules call reset().
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = ['hauler_combine', 'hauler_reedfolk', 'sub_combine', 'bomber_combine',
          'fighter_combine', 'tank_combine', 'truck_combine',
          'rickshaw_combine', 'bike_combine', 'props_kit']


def build_one(name):
    code = (f'import sys; sys.path.insert(0,"lib"); sys.path.insert(0,"assets")\n'
            f'import kit, {name} as A\n'
            f'A.build()\n'
            f'g, b = kit.export("{name}")\n'
            f'print("OK", "{name}", kit.tris(), g)\n')
    r = subprocess.run([sys.executable, '-c', code], cwd=HERE,
                       capture_output=True, text=True)
    ok = [l for l in r.stdout.splitlines() if l.startswith('OK')]
    if ok:
        _, n, tris, path = ok[0].split(None, 3)
        print(f'  {n:<20} {tris:>6} tris   {os.path.basename(path)}')
        return int(tris)
    print(f'  {name:<20} FAILED')
    print('   ', '\n    '.join(r.stderr.strip().splitlines()[-6:]))
    return None


if __name__ == '__main__':
    targets = sys.argv[1:] or ASSETS
    print(f'building {len(targets)} assets -> assets/glb, assets/blend\n')
    total = 0
    failed = []
    for a in targets:
        t = build_one(a)
        if t is None:
            failed.append(a)
        else:
            total += t
    print(f'\ntotal {total} tris across {len(targets) - len(failed)} assets')
    if failed:
        print('FAILED:', ', '.join(failed))
        sys.exit(1)
