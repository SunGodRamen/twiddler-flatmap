#!/usr/bin/env python3
"""validate-flatmap.py — validates canonical flatmap and cross-checks target bindings."""

import sys
import re
from pathlib import Path

VALID_PREFIXES = {"NAV", "UI", "EDIT", "MEDIA", "SYS", "RAW", "APP", "WM"}
WARN_PREFIXES = {"RAW"}

CHORD_RE = re.compile(r'^(\d\+)?(\d[LMR])(\+(\d\+)?(\d[LMR]))*$')
META_RE = re.compile(r'#\s*(.+)')
KV_RE = re.compile(r'(\w+):(\S+)')

errors = []
warnings = []

def parse_flatmap(path):
    entries = {}
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
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
            errors.append(f"{path}:{lineno} — malformed line: {raw!r}")
            continue
        chord, action = code.strip().split('=', 1)
        chord, action = chord.strip(), action.strip()
        if not CHORD_RE.match(chord):
            errors.append(f"{path}:{lineno} — invalid chord token: {chord!r}")
        prefix = action.split('_')[0]
        if prefix not in VALID_PREFIXES:
            errors.append(f"{path}:{lineno} — unknown action prefix: {prefix!r} in {action!r}")
        if prefix in WARN_PREFIXES:
            status = meta.get('status', 'unresolved')
            hypothesis = meta.get('hypothesis', '')
            hyp_str = f" hypothesis:{hypothesis}" if hypothesis else ""
            warnings.append(f"{path}:{lineno} — [WARN:unresolved] {chord}={action} status:{status}{hyp_str}")
        if chord in entries:
            errors.append(f"{path}:{lineno} — duplicate chord: {chord!r}")
        entries[chord] = (action, meta)
    return entries

def parse_bindings(path):
    bindings = {}
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        code = line.split('#')[0].strip()
        if '=' not in code:
            continue
        action, binding = code.split('=', 1)
        bindings[action.strip()] = binding.strip()
    return bindings

def check_coverage(flatmap_entries, bindings, bindings_path):
    canonical_actions = {action for action, _ in flatmap_entries.values()}
    for action in canonical_actions:
        if action not in bindings:
            errors.append(f"{bindings_path} — missing binding for: {action!r}")

root = Path(__file__).parent.parent
flatmap_files = list((root / 'maps').glob('*.flatmap'))
target_dirs = list((root / 'targets').iterdir())

if not flatmap_files:
    errors.append("No .flatmap files found in maps/")
    sys.exit(1)

all_entries = {}
for fm in flatmap_files:
    all_entries.update(parse_flatmap(fm))

for td in target_dirs:
    if not td.is_dir():
        continue
    bindings_file = td / 'default.bindings'
    if bindings_file.exists():
        bindings = parse_bindings(bindings_file)
        check_coverage(all_entries, bindings, bindings_file)
    else:
        warnings.append(f"No default.bindings in target: {td.name}")

for w in warnings:
    print(f"WARN  {w}")
for e in errors:
    print(f"ERROR {e}")

if errors:
    print(f"\nFAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1)
else:
    print(f"\nOK — 0 errors, {len(warnings)} warning(s), {len(all_entries)} chords validated")
