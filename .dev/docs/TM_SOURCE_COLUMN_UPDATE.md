# TM Source Column Update

**Date:** October 10, 2025  
**Version:** v3.0.0-beta  
**Feature:** Separate column for TM source in TM Matches pane

## Overview

Added a dedicated "TM Source" column to the TM matches tree view, replacing the previous format where the TM name was displayed in brackets after the translation.

## Changes Made

### Before:
```
Match %  | Translation
---------|----------------------------------------
100%     | Van Wikipedia, de vrije encyclopedie [Project TM]
95%      | Aus Wikipedia, der freien Enzyklopädie [Big Mama]
```

### After:
```
Match %  | Translation                              | TM Source
---------|------------------------------------------|------------
100%     | Van Wikipedia, de vrije encyclopedie     | Project TM
95%      | Aus Wikipedia, der freien Enzyklopädie   | Big Mama
```

## Technical Details

### Tree View Structure

**Updated Column Definition:**
```python
self.tm_tree = ttk.Treeview(tree_frame, columns=('match', 'text', 'source_tm'),
                           show='headings', yscrollcommand=scrollbar.set,
                           selectmode='browse', height=8)

# Column headings
self.tm_tree.heading('match', text='Match %')
self.tm_tree.heading('text', text='Translation')
self.tm_tree.heading('source_tm', text='TM Source')

# Column widths
self.tm_tree.column('match', width=70, minwidth=70, stretch=False)
self.tm_tree.column('text', width=250, minwidth=150, stretch=True)
self.tm_tree.column('source_tm', width=120, minwidth=100, stretch=False)
```

**Previous Structure:**
```python
self.tm_tree = ttk.Treeview(tree_frame, columns=('match', 'text'),
                           show='headings', ...)

self.tm_tree.heading('match', text='Match %')
self.tm_tree.heading('text', text='Translation')

self.tm_tree.column('match', width=70, minwidth=70, stretch=False)
self.tm_tree.column('text', width=250, minwidth=150, stretch=True)
```

### Data Population

**Updated Insert Logic:**
```python
for result in self.tm_results:
    match_pct = result['match']
    # ... tag logic ...
    
    # Use separate column for TM source
    self.tm_tree.insert('', 'end', 
                       values=(f"{match_pct}%", result['target'], result['tm']), 
                       tags=(tag,))
```

**Previous Insert Logic:**
```python
for result in self.tm_results:
    match_pct = result['match']
    # ... tag logic ...
    
    # TM source in brackets
    display_text = f"{result['target']} [{result['tm']}]"
    self.tm_tree.insert('', 'end', 
                       values=(f"{match_pct}%", display_text), 
                       tags=(tag,))
```

## Benefits

1. **Cleaner Display** - Translation text is not cluttered with TM source in brackets
2. **Better Readability** - Clear visual separation between translation and source
3. **Sortable** - Can potentially sort by TM source in the future
4. **Professional Look** - Matches industry-standard CAT tool interfaces
5. **Easier Scanning** - Quickly identify which TM provided each match

## Column Widths

- **Match %**: 70px (fixed) - Percentage display (e.g., "100%", "95%")
- **Translation**: 250px (expandable) - The actual translation text
- **TM Source**: 120px (fixed) - TM name (e.g., "Project TM", "Big Mama", "Custom TM 1")

The Translation column stretches to fill available space, while Match % and TM Source remain fixed width.

## Backwards Compatibility

✅ **Fully compatible** - No changes to data structures:
- `self.tm_results` structure unchanged
- Search functions unchanged
- TM database unchanged
- Only UI display modified

## Color Coding

Match quality color coding remains unchanged:
- **100% match**: Light green background (`#c8e6c9`)
- **90-99% match**: Light yellow background (`#fff9c4`)
- **<90% match**: Light orange background (`#ffecb3`)

## Related Functions

These functions remain compatible without modification:

### `on_tm_select(event)`
- Uses `self.tm_results[idx]` to get data
- Does not parse tree values
- ✅ No changes needed

### `copy_suggestion_to_target()`
- Copies from detail pane, not tree
- ✅ No changes needed

### `search_tm(auto_triggered=False)`
- Populates `self.tm_results` list
- Updated to insert 3 columns instead of 2
- ✅ Working correctly

## Files Modified

- `Supervertaler_v3.0.0-beta_CAT.py`
  - Line ~3548: Updated Treeview columns definition
  - Line ~3553-3559: Added heading and column for 'source_tm'
  - Line ~3816: Updated insert to use 3 values instead of formatted string

## Testing Checklist

- [x] TM tree displays 3 columns: Match %, Translation, TM Source
- [x] Match percentages display correctly
- [x] Translation text displays without brackets
- [x] TM source displays in separate column
- [x] Double-click to copy translation works
- [x] Selection and detail pane update works
- [x] Color coding for match quality works
- [x] Auto-search populates tree correctly
- [x] Manual search populates tree correctly
- [x] No syntax errors
- [x] No runtime errors

## Visual Impact

**Before:**
```
┌──────────┬────────────────────────────────────────────────┐
│ Match %  │ Translation                                    │
├──────────┼────────────────────────────────────────────────┤
│ 100%     │ Van Wikipedia [Project TM]                     │
│ 95%      │ Aus Wikipedia [Big Mama]                       │
└──────────┴────────────────────────────────────────────────┘
```

**After:**
```
┌──────────┬───────────────────────────────┬──────────────┐
│ Match %  │ Translation                   │ TM Source    │
├──────────┼───────────────────────────────┼──────────────┤
│ 100%     │ Van Wikipedia                 │ Project TM   │
│ 95%      │ Aus Wikipedia                 │ Big Mama     │
└──────────┴───────────────────────────────┴──────────────┘
```

## Future Enhancements (Optional)

- Add column header click to sort by TM source
- Add TM source filtering
- Show TM source icon/color instead of text
- Add tooltip showing full TM path for custom TMs
- Make column widths user-adjustable with persistence

---

**Status:** ✅ IMPLEMENTED  
**Impact:** Low (UI enhancement only)  
**Breaking Changes:** None  
**User Benefit:** Cleaner, more professional TM match display
