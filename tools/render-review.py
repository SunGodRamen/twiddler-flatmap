#!/usr/bin/env python3
"""render-review.py — renders canonical flatmap + all target bindings into review.tsv."""

import re
from pathlib import Path
from datetime import datetime, timezone

KV_RE = re.compile(r'(\w+):(\S+)')

def parse_flatmap(path):
    entries = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        meta = {}
        if '#' in line:
            code, comment = line.split('#', 1)
            for k, v in KV_RE.findall(comment):
                meta[k] = v
        else:
            code = line
        if '=' not in code:
            continue
        chord, action = code.strip().split('=', 1)
        entries[chord.strip()] = (action.strip(), meta)
    return entries

def parse_bindings(path):
    bindings = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        code = line.split('#')[0].strip()
        if '=' not in code:
            continue
        action, binding = code.split('=', 1)
        bindings[action.strip()] = binding.strip()
    return bindings

root = Path(__file__).parent.parent
flatmap_files = list((root / 'maps').glob('*.flatmap'))
target_dirs = sorted(d for d in (root / 'targets').iterdir() if d.is_dir())

all_entries = {}
for fm in flatmap_files:
    all_entries.update(parse_flatmap(fm))

targets = {}
for td in target_dirs:
    bf = td / 'default.bindings'
    if bf.exists():
        targets[td.name] = parse_bindings(bf)

out = root / 'generated' / 'review.tsv'
out.parent.mkdir(exist_ok=True)

header_cols = ['CHORD', 'CANONICAL', 'STATUS'] + [t.upper() for t in targets]
lines = [
    f"# generated: {datetime.now(timezone.utc).isoformat()}",
    '\t'.join(header_cols)
]

for chord, (action, meta) in all_entries.items():
    status = meta.get('status', 'ok') if action.startswith('RAW_') else meta.get('status', 'ok')
    hypothesis = meta.get('hypothesis', '')
    status_cell = status + (f"({hypothesis})" if hypothesis else "")
    row = [chord, action, status_cell]
    for tname in targets:
        row.append(targets[tname].get(action, 'MISSING'))
    lines.append('\t'.join(row))

out.write_text('\n'.join(lines) + '\n')
print(f"Wrote {out} ({len(all_entries)} chords, {len(targets)} targets)")
