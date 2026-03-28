---
title: Colours
nav_order: 4
---

# Colours

lomsh uses a fixed true-colour ANSI palette. All colours are defined in `lomsh/colours.py` and applied consistently across the interface.

## Palette

| Slot | Hex | Name | Used for |
|------|-----|------|----------|
| 1 | `#fb8500` | Orange | Prompt, command stdout |
| 2 | `#219ebc` | Teal | Agent response text |
| 3 | `#023047` | Midnight Navy | Agent response background |
| 4 | `#8ecae6` | Sky Blue | Token stats |
| 5 | `#ee6c4d` | Burnt Orange | Errors, stderr |

## Source palettes

The palette draws from two complementary sets:

**Set 1**

| Hex | Name |
|-----|------|
| `#3d5a80` | Steel Blue |
| `#98c1d9` | Light Steel Blue |
| `#e0fbfc` | Ice White |
| `#ee6c4d` | Burnt Orange |
| `#293241` | Dark Navy |

**Set 2**

| Hex | Name |
|-----|------|
| `#8ecae6` | Sky Blue |
| `#219ebc` | Teal |
| `#023047` | Midnight Navy |
| `#ffb703` | Amber |
| `#fb8500` | Orange |

## Changing the palette

Edit the constants at the top of `lomsh/colours.py`:

```python
C_PROMPT  = _fg("#fb8500")   # 1 — prompt and stdout
C_OUTPUT  = _fg("#fb8500")   # 2 — command stdout
C_AGENT   = _fg("#219ebc")   # 3 — agent response text
C_AGENTBG = _bg("#023047")   # 4 — agent response background
C_STATS   = _fg("#8ecae6")   # 5 — token stats
C_ERROR   = _fg("#ee6c4d")   # 6 — errors
```

`_fg()` sets the foreground (text) colour. `_bg()` sets the background. Both accept any 6-digit hex colour.

## Terminal background

The terminal window background is not controlled by lomsh — set it in your terminal emulator (iTerm2, Terminal.app, etc.) to complement the palette. Midnight Navy `#023047` works well as a window background.
