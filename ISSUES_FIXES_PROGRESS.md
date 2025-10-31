# Outstanding Issues & Implementation Plan

## Issues Addressed So Far

### ✅ Issue 1: Black Segment Numbers After Navigation
**Status**: FIXED in Supervertaler_Qt.py line ~2825
- Added explicit reset of foreground color to black when clearing previous selection
- Now properly maintains white text on orange background for current segment

### ✅ Issue 2: Global Numbering for Matches
**Status**: FIXED in translation_results_panel.py
- Modified `MatchSection` to accept `global_number_start` parameter
- Updated `_populate_matches()` to use global numbering
- Updated `set_matches()` to assign consecutive numbers across TM and Termbases
- Now: TM matches 1-N, then Termbases matches continue N+1...

## Issues Still TODO

### 🔄 Issue 3: Reduce Spacing in Match Display
**What needs to change**:
- Match percentage should be on same line as target term (not below)
- memoQ-style: only the match number box gets color, not entire row
- Reduce padding/margins between matches

**Files to modify**: `modules/translation_results_panel.py`
- `CompactMatchItem` class - adjust layout and styling
- `MatchSection` - reduce spacing between items

**Approach**:
```
Old (current):
┌─────────────────┐
│ [1] error       │ ← Number in colored box
│ fout            │ ← Target below
│ 100%            │ ← Percentage below
└─────────────────┘

New (memoQ-style):
┌────────────────────────┐
│ [1] 100%  error → fout │ ← All on one line, only box gets color
└────────────────────────┘
```

**Keyboard**:  Ctrl+1 through Ctrl+9 should insert the match with that global number

### 🔄 Issue 4: Add Ctrl+Up/Down Navigation for Matches
**What needs to change**:
- Ctrl+Up/Down should navigate through matches (not grid)
- Plain Up/Down should only navigate grid
- Need to intercept Ctrl+Up/Down at grid level

**Files to modify**: `Supervertaler_Qt.py`
- Find where grid keyboard events are handled
- Add `keyPressEvent()` override to intercept Ctrl+Up/Down
- When Ctrl+Up/Down detected, forward to TranslationResultsPanel instead

### 🔄 Issue 5: Implement Dual-Selection System
**What needs to change**:
- Users should be able to select individual words in source (not just whole segments)
- Use Ctrl+Shift+Right/Left arrows to extend selection word by word
- Use Tab to switch focus between source and target
- Use Ctrl+G to add selected term to termbase
- Use Ctrl+Shift+T to add selected term to TM only

**Files to modify**: `Supervertaler_Qt.py`
- Make source column (QTableWidgetItem) actually editable/selectable OR
- Use custom text editor widgets that support selection and keyboard bindings

**Approach**:
Since source is currently read-only (marked with `ItemIsEditable` flag removed), we need to either:
1. Make source column temporarily editable when user clicks it (like focus mode)
2. Replace source display with actual text widgets that support selection
3. Create a custom widget that supports both display and selection modes

**Recommended**: Use custom text widgets per segment (similar to Tkinter version's dual-selection)

## Implementation Priority

1. **HIGH** - Issue 3: Reduce spacing (user complaint about wasted space)
2. **HIGH** - Issue 4: Ctrl+Up/Down navigation (keyboard shortcut expectation)
3. **MEDIUM** - Issue 5: Dual-selection (nice-to-have but important for term extraction)

## Code References

### Global Numbering (FIXED)
- `MatchSection.__init__()`: Added `global_number_start` parameter
- `MatchSection._populate_matches()`: Uses `global_number = self.global_number_start + local_idx`
- `TranslationResultsPanel.set_matches()`: Calculates and passes global_number_start to each section

### Segment Number Highlighting (FIXED)  
- `on_cell_selected()` line ~2825:
  ```python
  prev_id_item.setForeground(QColor("black"))  # Now explicitly resets color
  ```

## Testing Checklist

- [ ] Load project and verify segment numbers don't turn black after navigation
- [ ] Select multiple segments and verify numbering flows: TM 1-10, Termbases 11+
- [ ] Try Ctrl+1 through Ctrl+9 to insert matches (should work with global numbering)
- [ ] Try Ctrl+Up/Down and verify it doesn't affect grid (currently will, needs fix)
- [ ] Test mouse selection of words in source (currently not possible)
