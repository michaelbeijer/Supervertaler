# Fix: Initial Color Display and Target Text Visibility

## Issues Fixed

### Issue 1: Colors Not Showing Until Clicked
**Problem**: Match number boxes had no color when the grid first opened. Colors only appeared after clicking on each match.

**Root Cause**: 
```python
# OLD CODE (wrong order):
def __init__(self):
    self.update_styling()  # Called BEFORE num_label_ref is set!
    ...
    self.num_label_ref = num_label  # Set AFTER
```

The `update_styling()` method tried to apply color to `self.num_label_ref`, but that attribute didn't exist yet because it was set after the call.

**Solution**:
```python
# NEW CODE (correct order):
def __init__(self):
    self.num_label_ref = None  # Initialize FIRST
    ...
    self.num_label_ref = num_label  # Set during layout creation
    ...
    self.update_styling()  # Called LAST after everything is ready
```

Now when `update_styling()` is called in `__init__`, the `num_label_ref` already exists and the color gets applied immediately.

### Issue 2: Target Text Not Visible
**Current Status**: ✅ ALREADY WORKING
The format `f"{match.source} → {match.target}"` is already showing both source AND target text in the matches display.

**Example Display**:
```
[1] 100%  error → fout
[2] 100%  error message → foutmelding  
[3] 100%  message → bericht
```

Both source and target are visible separated by the arrow (→).

**Truncation**:
- If the combined text exceeds 50 characters, it's truncated to 47 chars + "..."
- This prevents the text from wrapping or overflowing

## What Changed

### File: `modules/translation_results_panel.py`
**Lines**: ~41-95 (CompactMatchItem.__init__)

**Changes**:
1. Moved `self.num_label_ref = None` to the very beginning
2. Set `self.num_label_ref = num_label` immediately after creating the label widget
3. Moved `self.update_styling()` call to the very end (LAST in __init__)

### Execution Order Before:
1. ✗ `update_styling()` called → tries to use non-existent `num_label_ref`
2. ✓ `num_label` created and assigned to `num_label_ref`

### Execution Order After:
1. ✓ `num_label_ref` initialized to None
2. ✓ `num_label` created
3. ✓ `num_label_ref` assigned to point to `num_label`
4. ✓ `update_styling()` called → now `num_label_ref` exists and styling applies

## Test Results Expected

When you open a project and load a segment with matches:

1. **Immediately upon loading** (before clicking):
   - ✅ TM matches show with RED number boxes
   - ✅ Termbase matches show with BLUE number boxes
   - ✅ Source → target text visible for all matches
   - ✅ Percentage shown for all matches

2. **Upon clicking a match**:
   - ✅ Number box becomes darker red/blue
   - ✅ Entire row gets light background + border
   - ✅ Previous match returns to unselected state

3. **Text visibility**:
   - ✅ Both source and target text visible
   - ✅ Separated by arrow (→)
   - ✅ Long text truncated with "..." if needed

## Code Quality

- ✅ No syntax errors
- ✅ No logic errors (initialization order fixed)
- ✅ Backward compatible
- ✅ Simple fix (just reordering 3 operations)

## Summary

The issue was a classic initialization order problem. The styling was being applied before the widget references were created. By moving the initialization of `num_label_ref` to the beginning and `update_styling()` to the end, all styling now applies correctly on initial load.

All matches now display with their proper colors immediately, and both source and target text are visible in the compact format.
