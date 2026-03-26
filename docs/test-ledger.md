# Test ledger

## Purpose

Track empirical behavior of Twiddler chords on each target platform.

## Status keys

- untested
- confirmed
- mismatch
- ambiguous

## Windows

| Chord | Canonical | Expected | Observed | Status | Notes |
|---|---|---|---|---|---|
| 1R | NAV_UP | Up |  | untested |  |
| 1+1R | MEDIA_VOLUME_DOWN | Shift+VolumeDown or volume down behavior |  | untested | vendor encoding unusual |
| 1M | UI_SPACE | Space |  | untested |  |
| 1M+1R | EDIT_PASTE | Ctrl+V |  | untested |  |
| 1L+1M | EDIT_COPY | Ctrl+C |  | untested |  |
| 2R | NAV_RIGHT | Right |  | untested |  |
| 1R+2R | NAV_PAGEUP | PageUp |  | untested |  |
| 2M | UI_TAB | Tab |  | untested |  |
| 1+2M | RAW_128 | unknown |  | untested | identify real emitted behavior |
| 1M+2M | UI_ENTER | Enter |  | untested |  |
| 3R | NAV_LEFT | Left |  | untested |  |
| 3M | UI_BACKTAB | Shift+Tab |  | untested |  |
| 4R | NAV_DOWN | Down |  | untested |  |
| 1R+2R+4R | NAV_HOME | Home |  | untested |  |
| 3R+4R | NAV_PAGEDOWN | PageDown |  | untested |  |
| 1R+3R+4R | NAV_END | End |  | untested |  |
| 3+1R+2R+3R+4R | SYS_SCROLLLOCK | ScrollLock |  | untested |  |
| 4M | UI_ESCAPE | Escape |  | untested |  |

## Android

| Chord | Canonical | Expected | Observed | Status | Notes |
|---|---|---|---|---|---|
| 1+2M | RAW_128 | unknown |  | untested | especially important |
