#!/usr/bin/env python3
"""compile-cfg.py — compiles canonical flatmap + windows bindings into twiddler.cfg (v5 binary)
Usage: python3 tools/compile-cfg.py maps/<flatmap> targets/windows/default.bindings <output.cfg>
"""

import sys, struct, re

# HID keycode table — semantic binding string -> (modifier_byte, keycode_byte)
# modifier: 0x00=none, 0x01=LCtrl, 0x02=LShift, 0x04=LAlt, 0x20=RShift
HID = {
    'Up':           (0x00, 0x52),
    'Down':         (0x00, 0x51),
    'Left':         (0x00, 0x50),
    'Right':        (0x00, 0x4f),
    'PageUp':       (0x00, 0x4b),
    'PageDown':     (0x00, 0x4e),
    'Home':         (0x00, 0x4a),
    'End':          (0x00, 0x4d),
    'Space':        (0x00, 0x2c),
    'Tab':          (0x00, 0x2b),
    'Shift+Tab':    (0x02, 0x2b),
    'Enter':        (0x00, 0x28),
    'Escape':       (0x00, 0x29),
    'Ctrl+C':       (0x01, 0x06),
    'Ctrl+V':       (0x01, 0x19),
    'Shift+VolumeDown': (0x02, 0x81),  # RAW_128 candidate — empirical TBD
    'ScrollLock':   (0x00, 0x47),
}

# Chord bitmask encoding for v5
# Button layout: rows 1-4, cols L/M/R
# Bitmask: 16 bits, row1=bits15-12, row2=bits11-8, row3=bits7-4, row4=bits3-0
# Within each nibble: bit3=L, bit2=M, bit1=R, bit0=unused
# Thumb buttons 1/2/3 map to modifier nibble bits
COL = {'L': 0b1000, 'M': 0b0100, 'R': 0b0010}
ROW_SHIFT = {1: 12, 2: 8, 3: 4, 4: 0}
THUMB = {'1': 0x01, '2': 0x02, '3': 0x04}

def parse_chord(token):
    """Parse flatmap chord token into (thumb_byte, chord_word)."""
    parts = token.split('+')
    thumb = 0x00
    chord = 0x0000
    for p in parts:
        p = p.strip()
        m = re.match(r'^(\d)([LMR])$', p)
        if m:
            row, col = int(m.group(1)), m.group(2)
            chord |= (COL[col] << ROW_SHIFT[row])
        elif p in THUMB:
            thumb |= THUMB[p]
        else:
            raise ValueError(f"Unknown chord token: {p!r}")
    return thumb, chord

def parse_flatmap(path):
    entries = {}
    for raw in open(path):
        line = raw.split('#')[0].strip()
        if not line or '=' not in line:
            continue
        chord_tok, action = line.split('=', 1)
        entries[chord_tok.strip()] = action.strip()
    return entries

def parse_bindings(path):
    bindings = {}
    for raw in open(path):
        line = raw.split('#')[0].strip()
        if not line or '=' not in line:
            continue
        action, binding = line.split('=', 1)
        bindings[action.strip()] = binding.strip()
    return bindings

def build_cfg(flatmap_path, bindings_path, out_path):
    flatmap = parse_flatmap(flatmap_path)
    bindings = parse_bindings(bindings_path)

    # v5 header — copied verbatim from device
    header = bytes([0x05, 0x15, 0x12, 0x00])

    chord_entries = []
    skipped = []

    for chord_tok, action in sorted(flatmap.items()):
        binding = bindings.get(action, 'UNRESOLVED')
        if binding == 'UNRESOLVED':
            skipped.append((chord_tok, action, 'UNRESOLVED'))
            continue
        if binding not in HID:
            skipped.append((chord_tok, action, f'NO_HID_FOR:{binding}'))
            continue
        modifier, keycode = HID[binding]
        try:
            thumb, chord_word = parse_chord(chord_tok)
        except ValueError as e:
            skipped.append((chord_tok, action, str(e)))
            continue
        # v5 chord entry: [chord_hi] [chord_lo] [thumb|modifier] [keycode]
        chord_hi = (chord_word >> 8) & 0xff
        chord_lo = chord_word & 0xff
        mod_byte = (thumb << 4) | modifier
        chord_entries.append(bytes([chord_hi, chord_lo, mod_byte, keycode]))
        print(f"  OK  {chord_tok:20s} -> {action:25s} -> {binding:20s} [{chord_hi:02x}{chord_lo:02x} {mod_byte:02x} {keycode:02x}]")

    for item in skipped:
        print(f"  SKIP {item[0]:20s} -> {item[1]:25s} ({item[2]})")

    # v5 footer — copied from device tail bytes
    footer = bytes([0x08, 0x00, 0x00, 0x1e, 0x00, 0x1f, 0x00, 0x25])

    out = header
    for entry in chord_entries:
        out += entry
    out += footer

    open(out_path, 'wb').write(out)
    print(f"\nWrote {out_path} ({len(out)} bytes, {len(chord_entries)} chords, {len(skipped)} skipped)")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <flatmap> <bindings> <output.cfg>")
        sys.exit(1)
    build_cfg(sys.argv[1], sys.argv[2], sys.argv[3])
