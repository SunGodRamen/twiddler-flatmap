#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

MAP_RE = re.compile(r'^([A-Za-z0-9+]+)=([A-Z0-9_]+)$')
BIND_RE = re.compile(r'^([A-Z0-9_]+)=(.+)$')

def read_map(path: Path):
    out = {}
    for lineno, raw in enumerate(path.read_text().splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        m = MAP_RE.match(line)
        if not m:
            raise ValueError(f'{path}:{lineno}: invalid map line: {raw}')
        chord, action = m.groups()
        if chord in out:
            raise ValueError(f'{path}:{lineno}: duplicate chord: {chord}')
        out[chord] = action
    return out

def read_bindings(path: Path):
    out = {}
    for lineno, raw in enumerate(path.read_text().splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        m = BIND_RE.match(line)
        if not m:
            raise ValueError(f'{path}:{lineno}: invalid binding line: {raw}')
        action, binding = m.groups()
        out[action] = binding
    return out

def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print('usage: validate-flatmap.py <flatmap> <windows.bindings> <android.bindings>')
        return 2

    flatmap = read_map(Path(argv[1]))
    win = read_bindings(Path(argv[2]))
    android = read_bindings(Path(argv[3]))

    actions = sorted(set(flatmap.values()))
    rc = 0

    for action in actions:
        if action not in win:
            print(f'ERROR missing windows binding: {action}')
            rc = 1
        if action not in android:
            print(f'ERROR missing android binding: {action}')
            rc = 1
        if action.startswith('RAW_'):
            print(f'WARN unresolved raw action: {action}')

    if rc == 0:
        print('OK flatmap and bindings are internally consistent')
    return rc

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
