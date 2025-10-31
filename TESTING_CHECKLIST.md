# Testing Checklist for Termbase & Match Display Improvements

## Pre-Test Setup
- [ ] Load a project with multiple segments
- [ ] Ensure termbase is loaded (should have test data: 6 terms)
- [ ] Ensure Translation Memory is loaded

## Test 1: Segment Number Highlighting
**Expected Behavior**:
- Current segment number shows in orange with white text
- Previous segment number shows in black text on white background

**Steps**:
1. Click on segment 1
2. Observe segment number shows orange
3. Click on segment 2
4. Verify segment 1 number is NOW black (not still orange)
5. Click on segment 3
6. Verify segment 2 number is NOW black

**Result**: ✅ Pass / ❌ Fail

---

## Test 2: Global Match Numbering
**Expected Behavior**:
- Translation Memory matches numbered 1, 2, 3, ...
- Termbase matches continue from where TM left off (e.g., 11, 12, 13 if TM had 10)

**Steps**:
1. Load a segment with text containing termbase matches
2. Look at right panel
3. Count TM matches
4. Look at Termbase section
5. Verify numbers start after TM (not restart at 1)

**Result**: ✅ Pass / ❌ Fail

---

## Test 3: Compact Match Display
**Expected Behavior**:
- Each match shows on ONE line
- Format: `[#] PercentageA Source → Target`
- Much less vertical space than before

**Steps**:
1. Look at a single match in the right panel
2. Verify all info (number, percentage, source, target) is on one line
3. Verify no match takes up 3+ rows

**Visual Check**: Estimate vertical space used
- Before: ~3 rows per match = ~90px
- After: ~1 row per match = ~30px

**Result**: ✅ Pass / ❌ Fail

---

## Test 4: Match Number Box Coloring
**Expected Behavior**:
- Unselected: Number box is colored (red for TM, blue for Termbase)
- Selected: Number box is darker color, row gets light background

**Steps**:
1. Look at an unselected match
2. Verify ONLY the number box is colored (red/blue)
3. Rest of row is white
4. Click on a match to select it
5. Verify: number box gets darker, row gets light background + border
6. Click another match
7. Verify: previous match returns to unselected state (white background)

**Result**: ✅ Pass / ❌ Fail

---

## Test 5: Ctrl+1-9 Insertion with Global Numbering
**Expected Behavior**:
- Ctrl+1 inserts match #1 (first TM match)
- Ctrl+2 inserts match #2 (second TM match)
- Ctrl+9 inserts match #9 (depending on how many matches)
- Numbers are global (not per-section)

**Steps**:
1. Select a segment
2. Click on target column to enter edit mode
3. Press Ctrl+1
4. Verify first match is inserted
5. Undo (Ctrl+Z)
6. Try Ctrl+2, Ctrl+3, etc.
7. Verify correct matches are inserted

**Result**: ✅ Pass / ❌ Fail

---

## Test 6: Source Text Selectability
**Expected Behavior**:
- Can click and drag to select individual words in source text
- Can double-click to select a word
- Can copy selected text (Ctrl+C)

**Current Status**: ❌ NOT YET IMPLEMENTED
- Source column is read-only
- Requires dual-selection system implementation

**Steps for Future**:
1. Click on source text and drag to select
2. Double-click a word
3. Press Ctrl+C to copy
4. Verify selection is highlighted

**Result**: ⏳ Pending Implementation

---

## Test 7: Termbase Highlighting in Source
**Expected Behavior**:
- Words that match termbase terms show in blue, bold, underlined in source text
- Hovering shows tooltip (or clicking shows match)

**Steps**:
1. Load a segment
2. Look at source text
3. If text contains termbase terms ("error", "message", "contact", etc.)
4. Verify they show in blue+bold+underline
5. Mouse over - should show tooltip with translation

**Result**: ✅ Pass / ❌ Fail / ⏳ Not Yet Tested

---

## Test 8: Keyboard Navigation (Pending)
**Expected Behavior**: NOT YET IMPLEMENTED
- Ctrl+Up/Down: Navigate through matches
- Plain Up/Down: Navigate through grid segments only

**Status**: ⏳ TO BE IMPLEMENTED

---

## Test 9: Dual-Selection System (Pending)
**Expected Behavior**: NOT YET IMPLEMENTED
- Tab: Switch focus between source and target
- Ctrl+Shift+Right/Left: Extend selection word by word
- Ctrl+G: Add selected term pair to termbase
- Ctrl+Shift+T: Add selected term pair to TM

**Status**: ⏳ TO BE IMPLEMENTED

---

## Summary

### Critical Tests (Must Pass)
- [ ] Test 1: Segment number highlighting
- [ ] Test 2: Global numbering
- [ ] Test 3: Compact display
- [ ] Test 4: Color coding

### Important Tests (Should Pass)
- [ ] Test 5: Ctrl+1-9 insertion
- [ ] Test 7: Termbase highlighting

### Future Tests
- [ ] Test 6: Source selectability
- [ ] Test 8: Keyboard navigation
- [ ] Test 9: Dual-selection

---

## Troubleshooting

### If Segment Numbers Stay Orange
- Restart the application
- Check that you're navigating between different segments (not clicking same segment)
- Verify on_cell_selected is being called (check console for logs)

### If Match Numbering Restarts
- Check TranslationResultsPanel.set_matches() is being called with updated logic
- Verify MatchSection receives global_number_start parameter
- Print debug info: Check what numbers are being assigned

### If Matches Still Take 3 Rows
- Check CompactMatchItem layout is horizontal (QHBoxLayout)
- Verify margins/padding are minimal
- Check stylesheet is not adding extra height

### If Only Number Box or Entire Row Gets Color
- Check update_styling() method in CompactMatchItem
- Verify only num_label_ref gets setStyleSheet() call
- Check if self.num_label_ref is being set correctly

---

## Notes for Developer

1. **Test with real project**, not just test data
2. **Test with many matches** to verify scrolling works
3. **Test keyboard shortcuts** - Ctrl+1-9 especially
4. **Check console output** for any error messages or warnings
5. **Monitor application performance** - should still be fast with compact display

---

**Last Updated**: October 30, 2025
**Testing Status**: Ready to begin
**App Status**: Running
