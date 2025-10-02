# Bug Fix: Column Misalignment After Translation Update

## Problem Identified 🐛

**Issue**: When saving a translation (Ctrl+Enter), the text would appear in the wrong columns in the grid display. Source and Target text would overflow into the Style and Status columns.

**Visual Symptom**: After translating a segment, the grid would show:
- ID column: ✅ Correct
- Type column: ✅ Correct  
- Style column: ❌ Shows source text
- Status column: ❌ Shows source text (continued)
- Source column: ❌ Shows target text
- Target column: ❌ Empty or wrong text

## Root Cause

When we added the **Type** and **Style** columns in v0.3.0 and v0.3.1, we updated:
- ✅ Initial grid loading (`load_segments_to_grid()`) - **6 values**
- ❌ Grid update after edit (`update_segment_in_grid()`) - **still 4 values!**

### The Buggy Code

```python
def update_segment_in_grid(self, segment: Segment):
    """Update segment display in grid"""
    for item in self.tree.get_children():
        values = self.tree.item(item, 'values')
        if int(values[0]) == segment.id:
            self.tree.item(item,
                         values=(segment.id, segment.status.capitalize(),
                                self._truncate(segment.source, 100),
                                self._truncate(segment.target, 100)),  # Only 4 values!
                         tags=(segment.status,))
            break
```

**Problem**: Passing only 4 values when the grid expects 6!

### Column Mapping Before Fix

Grid expects: `(id, type, style, status, source, target)` - 6 values
Update provides: `(id, status, source, target)` - 4 values

**Result**:
- Column 0 (ID): Gets `id` ✅
- Column 1 (Type): Gets `status` ❌
- Column 2 (Style): Gets `source` ❌
- Column 3 (Status): Gets `target` ❌
- Column 4 (Source): Gets nothing ❌
- Column 5 (Target): Gets nothing ❌

**Everything shifted two columns to the left!**

## The Fix

Updated `update_segment_in_grid()` to match the full column structure:

```python
def update_segment_in_grid(self, segment: Segment):
    """Update segment display in grid"""
    for item in self.tree.get_children():
        values = self.tree.item(item, 'values')
        if int(values[0]) == segment.id:
            # Determine type label
            if segment.is_table_cell and segment.table_info:
                type_label = f"T{segment.table_info[0]+1}R{segment.table_info[1]+1}C{segment.table_info[2]+1}"
            else:
                type_label = "Para"
            
            # Format style name
            style_display = self._format_style_name(segment.style)
            
            # Set tags for styling
            tags = [segment.status]
            if segment.is_table_cell:
                tags.append('table_cell')
            style_tag = self._get_style_tag(segment.style)
            if style_tag:
                tags.append(style_tag)
            
            self.tree.item(item,
                         values=(segment.id, type_label, style_display, 
                                segment.status.capitalize(),
                                self._truncate(segment.source, 75),
                                self._truncate(segment.target, 75)),  # All 6 values!
                         tags=tuple(tags))
            break
```

**Now provides**: `(id, type, style, status, source, target)` - 6 values ✅

## Additional Fix: Column Widths

Also adjusted column widths and added constraints to prevent overflow:

```python
self.tree.column('id', width=40, minwidth=40, anchor='center', stretch=False)
self.tree.column('type', width=65, minwidth=60, anchor='center', stretch=False)
self.tree.column('style', width=80, minwidth=70, anchor='w', stretch=False)
self.tree.column('status', width=95, minwidth=90, anchor='center', stretch=False)
self.tree.column('source', width=400, minwidth=200, anchor='w', stretch=True)
self.tree.column('target', width=400, minwidth=200, anchor='w', stretch=True)
```

**Key improvements:**
- Fixed columns (ID, Type, Style, Status) have `stretch=False` - won't expand
- Content columns (Source, Target) have `stretch=True` - can expand
- Added `minwidth` constraints to prevent columns getting too narrow
- Adjusted widths to better balance the display

## Testing

### Before Fix:
1. Import document
2. Translate segment #3
3. Press Ctrl+Enter
4. **Result**: Text appears in wrong columns ❌

### After Fix:
1. Import document
2. Translate segment #3
3. Press Ctrl+Enter
4. **Result**: Text appears in correct columns ✅

### Verification Points:
- ✅ ID stays in ID column
- ✅ Type stays in Type column (Para or T#R#C#)
- ✅ Style stays in Style column (H 1, Normal, etc.)
- ✅ Status stays in Status column (Draft, Translated, etc.)
- ✅ Source stays in Source column
- ✅ Target stays in Target column
- ✅ Visual styling preserved (colors, fonts)

## Impact

### Affected Operations:
- **Saving translation** (Ctrl+Enter or Save & Next button)
- **Changing status** (dropdown change)
- **Any segment update** that calls `update_segment_in_grid()`

### Severity:
- **High** - Makes the application unusable for translation
- **Cosmetic** - Doesn't corrupt data, but prevents proper workflow
- **User-visible** - Immediately apparent when translating

## Files Modified

**cat_editor_prototype.py**:
- Lines 198-203: Column width adjustments
- Lines 508-533: Complete rewrite of `update_segment_in_grid()`

## Prevention

This bug occurred because:
1. We added columns incrementally (Type in v0.3.0, Style in v0.3.1)
2. We updated `load_segments_to_grid()` each time
3. We **forgot** to update `update_segment_in_grid()` to match

**Lesson**: When changing grid structure, update **ALL** methods that interact with grid values:
- `load_segments_to_grid()` - Initial population ✅
- `update_segment_in_grid()` - Individual updates ✅ (now fixed)
- Any other methods using `tree.item(values=...)` ✅

## Version Update

This fix is included in:
- ✅ **CAT Editor v0.3.1** (patched)
- Part of column structure improvements
- Critical fix for usability

## User Action Required

**If you experienced this issue:**
1. Restart the CAT Editor (already done automatically)
2. Reload your document
3. Try translating again - columns should now align correctly!

## Related Issues

This fix also addresses:
- Column header misalignment
- Text overflow into adjacent columns
- Confusion about which text is source vs target

---

## Summary

**Bug**: Column misalignment when updating translations due to incorrect number of values (4 instead of 6)

**Fix**: Updated `update_segment_in_grid()` to provide all 6 column values with proper type and style labels

**Status**: ✅ **FIXED** and tested

**Impact**: Critical - affected all translation saves

**Complexity**: Medium - required matching load and update logic

---

**Fixed**: October 2, 2025
**File**: cat_editor_prototype.py  
**Function**: update_segment_in_grid()
**Lines**: 508-533 (method), 198-203 (column config)
