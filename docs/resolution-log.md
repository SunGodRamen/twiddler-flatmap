# Resolution Log

## RAW_128
- vendor string: `128`
- chord: `1+2M`
- status: wontfix-candidate
- hypothesis: raw HID keycode 0x80 — no standard USB HID Keyboard page usage at this value; likely vendor macro slot or dead mapping in Tuner
- evidence: none (not empirically tested on device)
- action: mark wontfix pending one live keystroke test; if device emits no output, confirm wontfix
