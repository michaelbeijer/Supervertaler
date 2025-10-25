# TMX Editor - Word-Level Highlighting Update

## Overview

The TMX Editor now implements **word-level search highlighting** instead of row-level highlighting. When you search for a term like "surface", only that specific word is highlighted in yellow throughout the results, not the entire row.

## Implementation

### Previous Approach (Row-Level)
- Used Tkinter Treeview widget
- Could only apply tags to entire rows
- Searching for "surface" highlighted the entire row yellow
- Less precise for spotting search terms in long segments

### New Approach (Word-Level)
- Uses Tkinter Text widget instead of Treeview
- Supports precise text-level highlighting
- Only the search term(s) are highlighted in yellow
- Matches concordance search behavior

## Technical Details

### Display Widget
```python
# Text widget with scrollbars
self.results_text = tk.Text(grid_container, wrap='none',
                            font=('Consolas', 9),
                            cursor='arrow',
                            state='disabled',
                            bg='white')

# Configure highlighting tag
self.results_text.tag_configure('highlight', background='#ffff00', foreground='#000000')
```

### Highlighting Logic
```python
def _insert_with_highlight(self, text, search_term, width, row_tag):
    """Insert text with highlighted search terms"""
    if search_term and search_term.strip():
        # Find all occurrences of search term (case-insensitive)
        search_lower = search_term.lower()
        text_lower = display_text.lower()
        
        last_pos = 0
        while True:
            pos = text_lower.find(search_lower, last_pos)
            if pos == -1:
                # Insert remaining text
                if last_pos < len(display_text):
                    self.results_text.insert('end', display_text[last_pos:], row_tag)
                break
            
            # Insert text before match
            if pos > last_pos:
                self.results_text.insert('end', display_text[last_pos:pos], row_tag)
            
            # Insert highlighted match
            match_end = pos + len(search_lower)
            self.results_text.insert('end', display_text[pos:match_end], ('highlight', row_tag))
            
            last_pos = match_end
```

## User Experience

### Before (Row Highlighting)
```
ID       Source                                          Target
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1        The surface is smooth                           Het oppervlak is glad
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ (entire row yellow)
```

### After (Word Highlighting)
```
ID       Source                                          Target
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1        The surface is smooth                           Het oppervlak is glad
             ^^^^^^^                                          ^^^^^^^^^^ (only search terms yellow)
```

## Features

### Search Highlighting
- **Case-insensitive**: "Surface", "surface", "SURFACE" all match
- **Multiple occurrences**: All instances in a segment are highlighted
- **Source and target**: Separate filters for each language
- **Real-time**: Highlighting updates when filters are applied

### Display Format
- **Table layout**: ID, Source, Target columns
- **Alternating rows**: Gray/white background for readability
- **Monospaced font**: Consolas for consistent alignment
- **Pagination**: 50 TUs per page for performance

### Interaction
- **Double-click**: Edit any TU
- **Right-click**: Context menu
- **Scrolling**: Both horizontal and vertical

## Color Scheme

Consistent with Supervertaler's concordance search:
- **Highlight background**: `#ffff00` (yellow)
- **Highlight foreground**: `#000000` (black)
- **Row even**: `#f9f9f9` (light gray)
- **Row odd**: `#ffffff` (white)
- **Header**: `#e8e8e8` (gray)

## Benefits

1. **Precision**: Immediately spot the search term in long segments
2. **Consistency**: Matches concordance search highlighting
3. **Readability**: Doesn't obscure surrounding text
4. **Performance**: Text widget is efficient for large TMX files
5. **Professional**: Industry-standard highlighting approach

## Notes

- Bulk selection/delete functionality temporarily simplified during transition
- Individual TU editing fully functional via double-click
- Future updates will restore multi-select with Text widget selection tracking

---

**Version**: 3.7.5  
**Date**: October 25, 2025  
**Module**: `modules/tmx_editor.py`
