# Quick Reference: Match Panel Keyboard Shortcuts

## 🎯 Navigation

```
    ↑ UP
    │
    ├─→ Previous Match (cycles through all sections)
    │
   START ← → Select Match Highlighted in BLUE
    │
    ├─→ Next Match (cycles through all sections)
    │
    ↓ DOWN
```

---

## 🔧 Insertion Methods

### Method 1: Arrow + Spacebar
```
┌─────────────────────────┐
│  ↑ ↓ to Navigate        │
│     ↓                   │
│  Spacebar to Insert     │
└─────────────────────────┘
```

**Steps:**
1. Press **↑** or **↓** until desired match highlights blue
2. Press **Spacebar** (or **Enter**)
3. Match inserts → Grid auto-advances

---

### Method 2: Ctrl+Number
```
Ctrl+1  →  Insert Match #1 (immediately, no navigation needed)
Ctrl+2  →  Insert Match #2
Ctrl+3  →  Insert Match #3
...
Ctrl+9  →  Insert Match #9
```

**Steps:**
1. Press **Ctrl+1** through **Ctrl+9**
2. Match inserts → Grid auto-advances

---

## 📍 Context Switching

```
GRID CELL (editing)
    ↓
Press Escape
    ↓
GRID CELL (not editing)
    ↓
Press ↑/↓ to navigate cells
    ↓
Click on Match Panel
    ↓
MATCH PANEL (focused)
    ↓
Press ↑/↓ to navigate matches
Press Spacebar to insert
```

---

## 🚀 Practical Examples

### Example 1: Select Middle Match
```
Matches shown:
#1 TM 95%
#2 TM 87%    ← Want this one
#3 Fuzzy 52%

Action:  ↓ (Down arrow once) → Spacebar
Result:  Match #2 inserts into target
```

### Example 2: Direct Insert by Number
```
Matches shown:
#1 TM 95%
#2 TM 87%
#3 Fuzzy 52%    ← Want this one

Action:  Ctrl+3
Result:  Match #3 inserts into target (no navigation needed)
```

### Example 3: Grid to Match Navigation
```
1. User editing cell in grid
2. Finds match, so presses Escape
3. Clicks on match panel
4. Presses ↓ to navigate matches
5. Finds good match, presses Spacebar
6. Match inserts into target
7. Grid auto-advances
```

---

## ⚠️ Important Reminders

| Scenario | Do This |
|----------|---------|
| In grid edit mode, want to navigate matches | Press **Escape** first to exit edit mode |
| Want Ctrl+Up/Down for grid | Click grid first to focus it |
| Spacebar not working | Click match panel to ensure focus |
| Text not fully visible | Drag splitter handles to resize boxes |

---

## 🎨 Visual Indicators

```
UNSELECTED MATCH:          SELECTED MATCH:
┌──────────────────┐      ┌──────────────────┐
│ #1 TM 95%        │      │ #1 TM 95%        │
│ Source text... ··│      │ Source text... ··│  ← BLUE BG
│ Target text... ··│      │ Target text... ··│  ← WHITE TEXT
└──────────────────┘      └──────────────────┘
```

---

## 📋 Keyboard Legend

| Key | Symbol | Used For |
|-----|--------|----------|
| Up Arrow | ↑ | Navigate to previous match |
| Down Arrow | ↓ | Navigate to next match |
| Spacebar | [Space] | Insert selected match |
| Enter | ⏎ | Insert selected match |
| Ctrl | Ctrl | Modifier for number shortcuts |
| Escape | Esc | Exit edit mode |

---

## 🔄 Supported Match Types

```
RED border    →  Translation Memory (TM) match
BLUE border   →  Termbase match
YELLOW border →  Other/Fuzzy matches
```

**Number** = Global match number across all sections

---

## ✅ Implemented

- ✅ Long segment text wrapping (expands dynamically)
- ✅ Arrow key navigation (↑/↓)
- ✅ Spacebar insertion
- ✅ Ctrl+1-9 direct insertion
- ✅ Reserved Ctrl+Up/Down for grid navigation
- ✅ Auto-advance to next segment after insertion
- ✅ Color-coded match types
- ✅ Compact inline match numbering
- ✅ Blue selection highlighting

---

## 🎓 Tips for Fast Translation

1. **Default method**: Arrow navigation is fastest for sequential matches
2. **Known match**: If you know match number, use Ctrl+1-9 for instant insertion
3. **Spacebar benefit**: Keeps your hands on the keyboard (no mouse needed)
4. **Ctrl+Up/Down**: Use grid navigation when in grid (not in match panel)
5. **Tab key**: Switch focus between panels quickly

---

**Version**: 1.0  
**Last Updated**: October 29, 2025  
**Status**: All shortcuts implemented ✅
