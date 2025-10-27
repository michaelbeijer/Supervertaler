# Bug Fix: TMX Export in Grid View

**Date:** October 6, 2025  
**Issue:** `'Supervertaler' object has no attribute 'target_text'` when exporting TMX from Grid View

## Problem

When attempting to export TMX while in Grid View mode, the application crashed with:
```
✗ TMX export failed: 'Supervertaler' object has no attribute 'target_text'
```

**Root cause:**
- The `save_current_segment()` method was trying to access `self.target_text`
- This widget only exists in List/Split View (the bottom editor panel)
- In Grid View, there is no `target_text` widget - editing is done inline in the grid

## Solution

Updated `save_current_segment()` to check the current layout mode:

```python
def save_current_segment(self):
    """Save current segment from editor"""
    if not self.current_segment:
        return
    
    # Check layout mode and get values accordingly
    if self.layout_mode == LayoutMode.GRID:
        # In Grid mode, save from grid editor if active
        if hasattr(self, 'save_grid_editor_segment'):
            self.save_grid_editor_segment()
        return
    
    # List/Document mode - use target_text widget
    if not hasattr(self, 'target_text'):
        return
    
    # ... rest of the method
```

## Changes Made

**File:** `Supervertaler_v2.5.0 (experimental - CAT editor development).py`  
**Lines:** ~6584-6603  
**Method:** `save_current_segment()`

**Logic:**
1. Check if in Grid View mode
2. If yes, call `save_grid_editor_segment()` instead
3. If in List/Split mode, verify `target_text` exists before accessing it
4. Proceed with normal save logic

## Testing

✅ TMX export works in Grid View  
✅ TMX export works in List View  
✅ TMX export works in Document View  
✅ No crashes when switching between layouts

## Impact

**Before:**
- ❌ TMX export crashed in Grid View
- ✅ TMX export worked only in List/Split View

**After:**
- ✅ TMX export works in all layout modes
- ✅ Graceful handling of layout-specific widgets
- ✅ No attribute errors

This fix ensures that TMX export is available regardless of which layout mode the user is currently using.
