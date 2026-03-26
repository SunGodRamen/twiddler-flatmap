# Vendor observations

## Source layout

- Name: Twiddler3_TabSpace_V5_media
- Source: manual transcription from Tuner screenshot
- Status: partial baseline

## Raw observations

### 1R
- Tuner action: UpArrow
- Canonical action: NAV_UP
- Status: confirmed by label

### 1 + 1R
- Tuner action: R⇧,key-volumedown.R⇧
- Canonical action: MEDIA_VOLUME_DOWN
- Status: inferred
- Notes:
  - vendor encoding appears to wrap volume down with right shift
  - requires empirical behavior check on target devices

### 1M
- Tuner action: [space]
- Canonical action: UI_SPACE
- Status: confirmed by label

### 1M + 1R
- Tuner action: L⌃vL⌃
- Canonical action: EDIT_PASTE
- Status: inferred from key sequence

### 1L + 1M
- Tuner action: L⌃cL⌃
- Canonical action: EDIT_COPY
- Status: inferred from key sequence

### 2R
- Tuner action: RightArrow
- Canonical action: NAV_RIGHT
- Status: confirmed by label

### 1R + 2R
- Tuner action: PageUp
- Canonical action: NAV_PAGEUP
- Status: confirmed by label

### 2M
- Tuner action: Tab
- Canonical action: UI_TAB
- Status: confirmed by label

### 1 + 2M
- Tuner action: 128
- Canonical action: RAW_128
- Status: unresolved
- Notes:
  - requires empirical behavior test on Windows and mobile targets

### 1M + 2M
- Tuner action: Enter
- Canonical action: UI_ENTER
- Status: confirmed by label

### 3R
- Tuner action: LeftArrow
- Canonical action: NAV_LEFT
- Status: confirmed by label

### 3M
- Tuner action: L⇧TabL⇧
- Canonical action: UI_BACKTAB
- Status: inferred from key sequence

### 4R
- Tuner action: DownArrow
- Canonical action: NAV_DOWN
- Status: confirmed by label

### 1R + 2R + 4R
- Tuner action: Home
- Canonical action: NAV_HOME
- Status: confirmed by label

### 3R + 4R
- Tuner action: PageDown
- Canonical action: NAV_PAGEDOWN
- Status: confirmed by label

### 1R + 3R + 4R
- Tuner action: End
- Canonical action: NAV_END
- Status: confirmed by label

### 3 + 1R + 2R + 3R + 4R
- Tuner action: ScrollLock
- Canonical action: SYS_SCROLLLOCK
- Status: confirmed by label

### 4M
- Tuner action: Escape
- Canonical action: UI_ESCAPE
- Status: confirmed by label
