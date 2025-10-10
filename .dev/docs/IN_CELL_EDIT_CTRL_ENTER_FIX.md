# In-Cell Edit Mode Ctrl+Enter Fix

**Date:** October 10, 2025  
**Version:** v3.0.0-beta  
**Issue:** Segment #1 stuck on draft status when using in-cell editing

## Problem Description

When editing segments directly in the grid cells (in-cell edit mode), the Ctrl+Enter shortcut was using the old behavior:
- Only set status to "translated" **if** segment was "untranslated"
- Moved to **any** next segment, not specifically untranslated ones
- Did **not** add segments to Project TM

This meant:
1. If a segment had any status other than "untranslated" (e.g., was loaded from a saved project with "draft" status), pressing Ctrl+Enter would NOT change it to "translated"
2. User would have to manually change status for every segment
3. Segments were not being added to Project TM

## Root Cause

There are **TWO** different save functions in Grid mode:

### 1. Grid Editor Panel Save (`save_grid_editor_and_next()`)
- **Location:** Line ~2127
- **Triggered by:** Ctrl+Enter in the right-side editor panel
- **Status:** ✅ Already fixed in previous update
- Sets status to "translated"
- Moves to next untranslated segment
- Adds to Project TM

### 2. In-Cell Edit Save (`save_grid_edit()`)
- **Location:** Line ~6078
- **Triggered by:** Ctrl+Enter when editing directly in a grid cell
- **Status:** ❌ Was still using old logic (NOW FIXED)
- Previously only changed status if untranslated
- Previously moved to any next segment
- Previously did NOT add to Project TM

## Solution Implemented

Updated `save_grid_edit()` function to match the behavior of `save_grid_editor_and_next()`:

### Code Changes

**Before:**
```python
def save_grid_edit(self, go_next=False):
    # ... validation ...
    
    segment.target = new_text
    if new_text and segment.status == 'untranslated':  # ❌ Only if untranslated
        segment.status = 'translated'
    
    # ❌ No TM addition
    
    if go_next:
        # Navigate to next segment (any status) ❌
        if self.current_row_index < len(self.grid_rows) - 1:
            self.select_grid_row(self.current_row_index + 1)
```

**After:**
```python
def save_grid_edit(self, go_next=False):
    # ... validation ...
    
    segment.target = new_text
    
    # Set status based on go_next flag
    if go_next:
        # Ctrl+Enter was pressed - always set to translated ✅
        segment.status = 'translated'
    else:
        # Regular save - only auto-set if untranslated
        if new_text and segment.status == 'untranslated':
            segment.status = 'translated'
    
    # Add to Project TM if translated or approved ✅
    if segment.status in ['translated', 'approved'] and new_text:
        self.tm_database.add_to_project_tm(segment.source, new_text)
        self.log(f"✓ Added to Project TM: {segment.source[:50]}...")
    
    if go_next:
        # Find next untranslated segment ✅
        current_id = segment.id
        next_untranslated_index = None
        
        for i in range(self.current_row_index + 1, len(self.grid_rows)):
            if self.grid_rows[i]['segment'].status == 'untranslated':
                next_untranslated_index = i
                break
        
        if next_untranslated_index is not None:
            # Navigate to next untranslated segment
            self.select_grid_row(next_untranslated_index)
            self.root.after(50, self.enter_edit_mode)
        else:
            self.log("No more untranslated segments")
```

## New Behavior

### When Pressing Ctrl+Enter in In-Cell Edit Mode:

1. ✅ **Always** sets status to "translated" (regardless of previous status)
2. ✅ Adds segment to Project TM (if target not empty)
3. ✅ Moves to next **untranslated** segment
4. ✅ Automatically enters edit mode on the next segment
5. ✅ Shows "No more untranslated segments" when done

### When Pressing Escape (Regular Save):

1. Saves the segment
2. Only changes status to "translated" if was "untranslated"
3. Does NOT move to next segment
4. Returns focus to grid

## Auto-Search Issue Analysis

From the user's log, auto-search IS working correctly:

```
[17:34:39] ⏱ Auto-search scheduled (2 seconds)...
[17:34:41] 🔍 Auto-search executing...
[17:34:41] 🔍 Auto-search found 1 raw matches (before threshold filter)
[17:34:41] ✓ Auto-search: 1 matches above 75% threshold
[17:34:41] ✓ Auto-search: Populated TM tree with 1 matches
```

**However**, when navigating rapidly between segments:
```
[17:35:02] Segment #2 (Subtitle)
[17:35:02] ⏱ Auto-search scheduled (2 seconds)...
[17:35:02] Segment #3 (Heading 1)
[17:35:03] ⏱ Auto-search scheduled (2 seconds)...
[17:35:03] Segment #4 (Para)
[17:35:03] ⏱ Auto-search scheduled (2 seconds)...
```

The timer gets **cancelled and rescheduled** each time you navigate, which is **correct behavior**. The 2-second delay prevents unnecessary searches when quickly browsing.

**Conclusion:** Auto-search is working as designed. You only see matches after staying on a segment for 2 seconds.

## Testing Checklist

- [x] In-cell Ctrl+Enter sets status to "translated"
- [x] In-cell Ctrl+Enter adds to Project TM
- [x] In-cell Ctrl+Enter moves to next untranslated segment
- [x] Regular save (Escape) only changes status if untranslated
- [x] Auto-search triggers after 2-second delay
- [x] Auto-search cancelled when navigating quickly
- [x] TM matches display correctly when staying on a segment

## Impact

This fix ensures that **both** editing modes in Grid layout behave identically:
1. **Right-panel editor** (Ctrl+Enter)
2. **In-cell editing** (Ctrl+Enter)

Both now:
- Force status to "translated"
- Add to Project TM
- Jump to next untranslated segment

## Files Modified

- `Supervertaler_v3.0.0-beta_CAT.py`
  - Function: `save_grid_edit()` (line ~6078)
  - Added Project TM population logic
  - Added forced "translated" status when go_next=True
  - Added next-untranslated-segment navigation

---

**Status:** ✅ FIXED  
**Related Issue:** Segment #1 stuck on draft status  
**Root Cause:** In-cell edit mode using old save logic  
**Solution:** Updated `save_grid_edit()` to match `save_grid_editor_and_next()` behavior
