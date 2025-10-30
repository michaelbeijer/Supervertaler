# Keyboard Shortcuts for Match Selection & Insertion

## Overview
The translation match panel now supports multiple ways to navigate and insert matches, following memoQ's professional workflow.

## Navigation Shortcuts

### Arrow Keys (Simple Navigation)
| Shortcut | Action |
|----------|--------|
| **↑** (Up arrow) | Navigate to previous match |
| **↓** (Down arrow) | Navigate to next match |

**Note:** These navigate sequentially through all matches across all sections (NT, MT, TM, Termbase)

**Context:** These work when focus is in the match panel. When editing in grid cells:
- Press **Escape** to exit edit mode
- Then use **↑/↓** to navigate matches

---

## Match Insertion Shortcuts

### Method 1: Select & Insert with Spacebar
1. Use **↑/↓** arrow keys to cycle through matches
2. Selected match highlights in blue
3. Press **Spacebar** (or **Enter**) to insert into target cell

### Method 2: Direct Insert by Number (Ctrl+1-9)
Press **Ctrl+1** through **Ctrl+9** to directly insert the Nth match without navigating:

| Shortcut | Action |
|----------|--------|
| **Ctrl+1** | Insert match #1 directly |
| **Ctrl+2** | Insert match #2 directly |
| **Ctrl+3** | Insert match #3 directly |
| **Ctrl+4** | Insert match #4 directly |
| **Ctrl+5** | Insert match #5 directly |
| **Ctrl+6** | Insert match #6 directly |
| **Ctrl+7** | Insert match #7 directly |
| **Ctrl+8** | Insert match #8 directly |
| **Ctrl+9** | Insert match #9 directly |

**Behavior:** 
- Match number refers to global match number across all sections
- Match highlights blue as it's selected
- Text is inserted into target cell immediately
- Grid auto-advances to next segment

---

## Grid Navigation (Reserved Shortcuts)

These shortcuts are **NOT** for match navigation - they're for grid cell navigation:

| Shortcut | Action |
|----------|--------|
| **Ctrl+↑** | Jump to first cell in grid |
| **Ctrl+↓** | Jump to last cell in grid |
| **Escape** | Exit cell edit mode → use arrows to navigate cells |

---

## Practical Workflow Example

```
1. Translate segment #5
2. TM returns 3 matches
3. User sees:
   #1 95% (TM match - red)
   #2 87% (TM match - red)
   #3 52% (Fuzzy - yellow)

Option A (Navigate & Select):
   Press ↓ → Select match #2 (87%)
   Press Spacebar → Insert into target cell
   Grid auto-advances to segment #6

Option B (Direct Insert):
   Press Ctrl+2 → Insert match #2 immediately
   Grid auto-advances to segment #6
```

---

## Visual Feedback

### Match Highlighting
- **Unselected**: Gray background
- **Hovering**: Light blue background
- **Selected**: Dark blue background with white text

### Match Type Indicators
- **Red border**: Translation Memory (TM) match
- **Blue border**: Termbase match
- **Yellow border**: Other matches

---

## Important Notes

### Text Wrapping
Long segments are fully supported:
- Text wraps to multiple lines
- Source and target display is dynamic (expands/contracts as needed)
- Compare box grows vertically to accommodate text
- Fully resizable with splitter handles

### Match Panel Focus
The match panel must have focus for keyboard shortcuts to work:
- Click on any match to give it focus
- Press **Tab** to cycle focus between panels

### Escape Key Behavior
- If editing in grid cell: **Escape** exits edit mode
- Then **↑/↓** navigate grid cells
- To navigate matches, click on match panel first to give it focus

---

## Comparison with memoQ

| Feature | memoQ | Supervertaler |
|---------|-------|---------------|
| Arrow navigation | ✓ | ✓ |
| Spacebar insert | ✓ | ✓ |
| Ctrl+1-9 insert | ✓ | ✓ |
| Long text wrapping | ✓ | ✓ |
| Color-coded matches | ✓ | ✓ |
| Compact layout | ✓ | ✓ |
| Source+Target display | ✓ | ✓ |

---

## Troubleshooting

### Shortcuts not working?
1. **Click on match panel** to ensure it has focus
2. **Not in edit mode**: If a grid cell is in edit mode, press **Escape** first
3. **Verify match exists**: For Ctrl+1-9, ensure that match number exists

### Text not displaying?
- Long segments now expand dynamically
- If text still truncated, use splitter handles to resize compare boxes
- Drag splitter to make more vertical space

---

## Future Enhancements

Potential additions (not yet implemented):
- Ctrl+Shift+Up/Down for match jump in grid
- Custom keyboard shortcuts configuration
- Match context preview on hover
- Diff highlighting in compare boxes
