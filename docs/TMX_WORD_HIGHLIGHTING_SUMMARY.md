# TMX Editor - Word-Level Highlighting Summary

## What Changed

**Before**: When searching for "surface", the entire row was highlighted yellow.

**After**: When searching for "surface", only the word "surface" is highlighted yellow (and "oppervlak" in Dutch if searching target).

## Example

### Search: "surface"

**Before (Row Highlighting)**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID  Source                              Target
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
█ 1 █ The surface is smooth            █ Het oppervlak is glad    █
█████████████████████████████████████████████████████████████████
     ↑ Entire row highlighted in yellow
```

**After (Word Highlighting)**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID  Source                              Target
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1   The █surface█ is smooth             Het oppervlak is glad
         ↑ Only the search term highlighted in yellow
```

## How It Works

1. **Filter by source**: Type "surface" in the Source filter box
2. **Press Enter**: Apply filter
3. **View results**: Only segments containing "surface" are shown
4. **See highlighting**: The word "surface" appears with yellow background
5. **Multiple matches**: If "surface" appears multiple times in one segment, all are highlighted

## Features

✅ **Case-insensitive**: Finds "Surface", "surface", "SURFACE"  
✅ **Multiple occurrences**: All instances highlighted  
✅ **Source and target**: Filter and highlight each independently  
✅ **Professional UX**: Matches concordance search behavior  

## Technical Implementation

- **Widget**: Changed from Treeview to Text widget
- **Method**: `_insert_with_highlight()` finds all occurrences
- **Color**: `#ffff00` background (yellow), `#000000` text (black)
- **Display**: Monospaced font (Consolas) for clean table layout

## User Benefits

1. **Faster scanning**: Eye immediately drawn to search terms
2. **Better context**: See surrounding words clearly
3. **Professional**: Industry-standard highlighting approach
4. **Consistent**: Matches concordance search behavior

---

**Module**: `modules/tmx_editor.py`  
**Version**: 3.7.5  
**Updated**: October 25, 2025
