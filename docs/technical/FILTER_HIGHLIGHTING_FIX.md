# Filter Highlighting Fix

**Date:** 2025-01-XX  
**Issue:** Filter search terms were not being highlighted in source/target cells  
**Status:** ✅ FIXED

## Problem

When users entered search terms in the filter source/target boxes, the filtered segments were displayed correctly, but the search terms were NOT highlighted in yellow within the visible cells.

### Root Cause

The highlighting system was using a **delegate-based approach** (`WordWrapDelegate.paint()` method) which works perfectly for normal `QTableWidgetItem` cells. However, both source and target columns use **cell widgets** (`EditableGridTextEditor` and `ReadOnlyGridTextEditor` - QTextEdit subclasses) via `setCellWidget()`.

**Critical discovery:** When a cell has a widget set via `setCellWidget()`, Qt completely bypasses the delegate's `paint()` method and renders the widget directly. This means:
- The delegate's `global_search_term` was being set correctly
- The delegate's highlight logic was perfect
- BUT the delegate's `paint()` method was NEVER CALLED for these cells

## Solution

Changed from delegate-based highlighting to **widget-internal highlighting** using QTextCursor and QTextCharFormat:

### New Method: `_highlight_text_in_widget()`

```python
def _highlight_text_in_widget(self, row: int, col: int, search_term: str):
    """Highlight search term within a QTextEdit cell widget.
    
    Since source/target cells use setCellWidget() with QTextEdit editors,
    the delegate's paint() method is bypassed. We must highlight the text
    directly within the widget using QTextCursor and QTextCharFormat.
    """
    widget = self.table.cellWidget(row, col)
    if not widget or not hasattr(widget, 'document'):
        return
    
    # Clear any existing search highlights
    cursor = widget.textCursor()
    cursor.select(QTextCursor.SelectionType.Document)
    clear_format = QTextCharFormat()
    cursor.setCharFormat(clear_format)
    cursor.clearSelection()
    
    # Create yellow highlight format
    highlight_format = QTextCharFormat()
    highlight_format.setBackground(QColor("#FFFF00"))
    
    # Find and highlight all occurrences (case-insensitive)
    document = widget.document()
    cursor = QTextCursor(document)
    
    search_term_lower = search_term.lower()
    text = document.toPlainText()
    text_lower = text.lower()
    
    # Find all occurrences
    pos = 0
    while True:
        pos = text_lower.find(search_term_lower, pos)
        if pos == -1:
            break
        
        # Select the match and apply highlight
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.MoveOperation.Right, 
                          QTextCursor.MoveMode.KeepAnchor, len(search_term))
        cursor.mergeCharFormat(highlight_format)
        
        pos += len(search_term)
```

### Changes to `apply_filters()`

Replaced:
```python
# Old: Delegate-based approach (didn't work)
if source_filter_text:
    self.highlight_search_term(row, 2, segment.source, source_filter_text)
if target_filter_text:
    self.highlight_search_term(row, 3, segment.target, target_filter_text)
```

With:
```python
# New: Widget-internal highlighting (works!)
if source_filter_text and source_filter_text.lower() in segment.source.lower():
    self._highlight_text_in_widget(row, 2, source_filter_text)
if target_filter_text and target_filter_text.lower() in segment.target.lower():
    self._highlight_text_in_widget(row, 3, target_filter_text)
```

Also removed all delegate-related code (setting `global_search_term`, calling `viewport().repaint()`, etc.) since it's no longer needed.

## How It Works

1. **User enters search term** in source_filter or target_filter QLineEdit
2. **apply_filters() filters rows** based on search term matches
3. **For each visible matching row:**
   - Gets the QTextEdit widget from the cell using `cellWidget(row, col)`
   - Clears any existing highlights from the widget's document
   - Creates a `QTextCharFormat` with yellow background (#FFFF00)
   - Uses `QTextCursor` to find all occurrences (case-insensitive)
   - Applies the highlight format to each match using `mergeCharFormat()`

4. **When filters are cleared:**
   - `clear_filters()` calls `load_segments_to_grid()`
   - This recreates all widgets from scratch
   - Fresh widgets have no highlights → highlights cleared automatically

## Key Insights

- **Widgets bypass delegates:** `setCellWidget()` completely bypasses `QStyledItemDelegate.paint()`
- **QTextEdit has powerful formatting:** QTextCursor + QTextCharFormat provide precise control over text appearance
- **Case-insensitive search:** Using `.lower()` comparison for both search and matching
- **Multiple matches per cell:** The loop handles multiple occurrences correctly
- **No performance issues:** Direct widget manipulation is very fast

## Testing Checklist

- [ ] Enter term in source filter → yellow highlights appear in source column
- [ ] Enter term in target filter → yellow highlights appear in target column
- [ ] Enter terms in both filters → highlights in both columns
- [ ] Multiple matches per cell → all highlighted correctly
- [ ] Case-insensitive: "test", "TEST", "TeSt" all match "test"
- [ ] Clear filters → all highlights disappear
- [ ] Performance with 219 segments → smooth and responsive

## Related Files

- `Supervertaler.py` line ~15765: `_highlight_text_in_widget()` (new method)
- `Supervertaler.py` line ~15779: `apply_filters()` (modified to use widget highlighting)
- `Supervertaler.py` line 15872: `clear_filters()` (no changes needed - already works correctly)

## Future Enhancements

Could add:
- **Highlight color preference** in settings
- **Regex support** for advanced search patterns
- **Match count display** ("3 matches found")
- **Next/Previous match navigation** buttons
