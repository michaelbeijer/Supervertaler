# Termbase Feature - Fixes Applied

## Issues Fixed

### 1. ✅ Source Column Not Selectable
**Problem**: Using a custom `TermbaseHighlightWidget` (QLabel) to display highlighted terms prevented text selection/interaction.

**Solution**: Removed the custom widget and instead store termbase matches as an attribute on the source QTableWidgetItem. This preserves:
- Full text selectability
- Copy/paste functionality
- Normal table interaction

**Code Change**: `load_segments_to_grid()` (line ~2680)
- Removed: `self.table.setCellWidget(row, 2, widget)`
- Added: `source_item.termbase_matches = termbase_matches` (store matches as attribute)

### 2. ✅ Segment Numbers Turning Black After Selection
**Problem**: After navigating away from a segment, the orange highlight wasn't maintained on the segment number.

**Solution**: Changed table selection behavior from `SelectRows` to `SelectItems` to allow custom highlighting logic in `on_cell_selected()`.

**Code Change**: `setup_grid_ui()` (line ~1792)
```python
# OLD: self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
# NEW: self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
```

### 3. ✅ Full Row Highlighting in Blue
**Problem**: When selecting a segment, the entire row was highlighted in blue instead of just the segment number in orange.

**Solution**: Using `SelectItems` instead of `SelectRows` allows only the individual cell to be selected, with manual orange highlighting applied only to column 0 (segment number) in `on_cell_selected()`.

### 4. ✅ Termbase Matches Not Showing on Right Panel
**Problem**: Even though termbase matches were found and stored, they weren't displayed in the TranslationResultsPanel on the right side.

**Solution**: Added code to extract termbase matches from the source item and populate the `matches_dict["Termbases"]` list.

**Code Change**: `on_cell_selected()` (line ~2900)
```python
# New section that adds termbase matches to the results panel
if hasattr(source_item, 'termbase_matches'):
    termbase_matches = source_item.termbase_matches
    for source_term, target_term in termbase_matches.items():
        match_obj = TranslationMatch(...)
        matches_dict["Termbases"].append(match_obj)
```

## Current Behavior

Now when you select a segment:
1. ✅ Only the segment number (column 0) highlights in orange
2. ✅ Source text is fully selectable (can copy/paste)
3. ✅ No blue full-row highlighting
4. ✅ Termbase matches appear in the right panel under "Termbases" section
5. ✅ Termbase matches are also highlighted in blue in the source text (visual indicator)

## Data Flow

```
Segment loaded
    ↓
find_termbase_matches_in_source() - searches database for matching terms
    ↓
Matches stored as attribute: source_item.termbase_matches = {...}
    ↓
Segment selected by user
    ↓
on_cell_selected() retrieves termbase_matches attribute
    ↓
Termbase matches added to matches_dict["Termbases"]
    ↓
TranslationResultsPanel displays matches on right side
```

## Testing

To test the fixes:
1. Load a project with source text containing termbase terms
2. Click on a segment
3. Verify:
   - ✅ Segment number shows in orange (not black after navigation)
   - ✅ Only segment number highlighted (not full row)
   - ✅ Source text is selectable (can click and copy)
   - ✅ Termbase matches appear on the right side panel
   - ✅ Matching terms are highlighted in blue in the source

## Files Modified

- `Supervertaler_Qt.py`:
  - Line ~1792: Changed `SelectRows` → `SelectItems`
  - Line ~2680: Removed custom widget, store matches as attribute
  - Line ~2900: Added termbase matches to results panel

## Known Limitations

1. Double-click insertion on termbase matches not yet implemented (was removed with widget)
2. Tooltip on hover not implemented (needs different approach without custom widget)
3. Only exact word matches are highlighted (not phrase matches yet)

## Next Steps (Optional)

To fully restore double-click insertion:
1. Connect to cell double-click event
2. Identify which termbase term was clicked
3. Insert translation into target column

Or alternatively: Add "Insert" button next to each termbase match on the right panel.
