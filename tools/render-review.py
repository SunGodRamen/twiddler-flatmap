#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

def read_pairs(path: Path):
    out = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        k, v = line.split('=', 1)
        out.append((k, v))
    return out

repo = Path(__file__).resolve().parent.parent
flatmap = read_pairs(repo / 'maps' / 'twiddler3-tabspace-v5-media.flatmap')
win = dict(read_pairs(repo / 'targets' / 'windows' / 'default.bindings'))
android = dict(read_pairs(repo / 'targets' / 'android' / 'default.bindings'))

out = repo / 'generated' / 'review.tsv'
out.parent.mkdir(parents=True, exist_ok=True)

with out.open('w', encoding='utf-8') as f:
    f.write('CHORD\tCANONICAL\tWINDOWS\tANDROID\n')
    for chord, action in flatmap:
        f.write(f'{chord}\t{action}\t{win.get(action, "")}\t{android.get(action, "")}\n')

print(out)
