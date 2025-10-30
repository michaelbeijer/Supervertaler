# TMX Editor - Dual Highlighting System

**Date**: October 25, 2025  
**Version**: v3.7.6  
**Status**: ✅ Implemented and Working

## Overview

The TMX Editor features a **dual highlighting system** that combines two complementary approaches to make search results highly visible while maintaining the professional Treeview grid interface.

## The Challenge

- **Treeview Widget Limitation**: Tkinter's Treeview widget cannot display rich text formatting (bold, colors) within cells
- **User Need**: Precise highlighting of search terms (not entire rows)
- **Grid Requirements**: Professional features (resizable columns, row selection, table layout)

## The Solution: Dual Highlighting

### 1. Row-Level Background Highlighting
- **Visual Cue**: Light yellow background (`#fffacd`)
- **Purpose**: Quickly identify which rows contain matches
- **Coverage**: Entire row is highlighted
- **Implementation**: Treeview tag configuration

### 2. Term-Level Text Markers
- **Visual Cue**: Unicode bold characters (𝐛𝐨𝐥𝐝 𝐭𝐞𝐱𝐭)
- **Purpose**: Pinpoint exact location of matches within text
- **Coverage**: Only the matched words
- **Implementation**: Unicode mathematical bold character conversion

## Example

### Search Query
```
Search Term: "concrete"
```

### Before Filtering
```
ID  | Source
----|-----------------------------------------------
001 | T-shaped concrete base (configuration 2)
002 | T-shaped concrete base
003 | T-shaped concrete base
004 | Cutaway view of the T-shaped concrete base
```

### After Filtering (With Dual Highlighting)
```
ID  | Source                                        | Background
----|-----------------------------------------------|------------
001 | T-shaped 𝐜𝐨𝐧𝐜𝐫𝐞𝐭𝐞 base (configuration 2)    | 💛 Yellow
002 | T-shaped 𝐜𝐨𝐧𝐜𝐫𝐞𝐭𝐞 base                      | 💛 Yellow
003 | T-shaped 𝐜𝐨𝐧𝐜𝐫𝐞𝐭𝐞 base                      | 💛 Yellow
004 | Cutaway view of the T-shaped 𝐜𝐨𝐧𝐜𝐫𝐞𝐭𝐞 base  | 💛 Yellow
```

## How It Works

### In the Code

```python
def highlight_search_term_in_text(self, text, search_term):
    """Highlight search term using Unicode bold characters"""
    # Case-insensitive search
    search_lower = search_term.lower()
    text_lower = text.lower()
    
    # Find all occurrences and convert to Unicode bold
    result = []
    last_pos = 0
    
    pos = text_lower.find(search_lower)
    while pos != -1:
        result.append(text[last_pos:pos])
        match_text = text[pos:pos + len(search_term)]
        bold_text = self._to_unicode_bold(match_text)  # Convert to bold!
        result.append(bold_text)
        last_pos = pos + len(search_term)
        pos = text_lower.find(search_lower, last_pos)
    
    result.append(text[last_pos:])
    return ''.join(result)

def _to_unicode_bold(self, text):
    """Convert text to Unicode bold characters"""
    bold_map = {
        **{chr(ord('A') + i): chr(0x1D400 + i) for i in range(26)},  # A-Z
        **{chr(ord('a') + i): chr(0x1D41A + i) for i in range(26)},  # a-z
        **{chr(ord('0') + i): chr(0x1D7CE + i) for i in range(10)},  # 0-9
    }
    return ''.join(bold_map.get(c, c) for c in text)
```

### In the Display

```python
def refresh_current_page(self):
    # ... for each TU ...
    
    # Highlight search terms with markers
    if self.filter_source:
        src_display = self.highlight_search_term_in_text(src_display, self.filter_source)
    if self.filter_target:
        tgt_display = self.highlight_search_term_in_text(tgt_display, self.filter_target)
    
    # Check if row matches (for background highlighting)
    tags = ()
    if self.filter_source and self.filter_source.lower() in src_text.lower():
        tags = ('match',)  # Light yellow background
```

## Why Unicode Bold?

### Advantages
1. **True Bold Text**: Actually renders as bold in the Treeview (no markers needed)
2. **No Special Characters**: Doesn't add « » or ** around text
3. **Clean Look**: Looks professional and native
4. **Universal Support**: Unicode mathematical bold characters (U+1D400-U+1D7D7)
5. **No Conflict**: Doesn't interfere with actual content
6. **Treeview Compatible**: Works where HTML/rich text doesn't

### How It Works
Unicode has a special range of "Mathematical Alphanumeric Symbols" that includes bold versions of:
- **Uppercase A-Z**: U+1D400 to U+1D419 (𝐀 𝐁 𝐂 ... 𝐙)
- **Lowercase a-z**: U+1D41A to U+1D433 (𝐚 𝐛 𝐜 ... 𝐳)
- **Digits 0-9**: U+1D7CE to U+1D7D7 (𝟎 𝟏 𝟐 ... 𝟗)

### Example Conversions
- `concrete` → `𝐜𝐨𝐧𝐜𝐫𝐞𝐭𝐞`
- `Base123` → `𝐁𝐚𝐬𝐞𝟏𝟐𝟑`
- `T-shaped` → `𝐓-𝐬𝐡𝐚𝐩𝐞𝐝` (hyphen stays normal)

### Limitations
- **Special Characters**: Punctuation (-, /, etc.) remains normal (no Unicode bold version)
- **Non-Latin Characters**: Only works for A-Z, a-z, 0-9
- **Font Support**: Requires font that supports Unicode mathematical symbols (most modern fonts do)

## User Experience

### Workflow
1. User enters search term in Source or Target filter box
2. Press Enter or click "Apply Filter"
3. Grid updates to show:
   - Only matching rows (filtered)
   - Light yellow background on all matching rows
   - **Search terms in Unicode bold** (𝐛𝐨𝐥𝐝 𝐭𝐞𝐱𝐭)
4. User can:
   - Quickly scan yellow rows to find matches
   - Precisely locate terms using bold text
   - Click row to load into edit panel
   - Resize columns to see full text

### Benefits
- **Fast Scanning**: Yellow background provides immediate visual feedback
- **Precise Location**: Bold text shows exact match positions
- **Professional Appearance**: True bold rendering (not markers)
- **Clean Display**: No extra characters added to text
- **Professional Grid**: Maintains all Treeview features (resizable, selectable)
- **No Trade-offs**: Best of both worlds (grid functionality + bold highlighting)

## Technical Details

### Character Encoding
- **Unicode Mathematical Bold**: U+1D400 to U+1D7D7
- **Encoding**: UTF-8 (standard in TMX files and Supervertaler)
- **Display**: Requires font with mathematical symbol support (e.g., Arial, Segoe UI, most modern fonts)

### Performance
- **Impact**: Minimal (string concatenation only)
- **Optimization**: Applied during display refresh, not during parsing
- **Scalability**: Works efficiently with pagination (50 TUs per page)

### Compatibility
- **Python**: 3.8+ (full Unicode support)
- **Tkinter**: All versions (plain text in Treeview cells)
- **TMX Files**: No modification (highlighting is display-only)
- **Platforms**: Windows, macOS, Linux

## Comparison with Other Solutions

| Approach | Grid Features | Term Highlighting | Trade-offs |
|----------|--------------|-------------------|------------|
| **Text Widget** | ❌ No resizing<br>❌ No selection | ✅ Bold/color tags<br>✅ Word-level | Shows XML content |
| **HTML Viewer** | ❌ No editing<br>❌ Complex | ✅ Full formatting | Read-only |
| **Custom Canvas** | ⚠️ Must implement<br>⚠️ Complex | ✅ Full control | Weeks of work |
| **Unicode Bold** | ✅ Full Treeview<br>✅ Resizable | ✅ **True bold text**<br>✅ Background | Perfect! ✅ |

## Future Enhancements (Optional)

### Potential Improvements
1. **Bold + Italic**: Use Unicode italic or bold-italic variants
2. **Color Options**: Allow customization of yellow background
3. **Multiple Terms**: Support highlighting multiple search terms with different styles
4. **Regex Support**: Highlight pattern matches
5. **Case Sensitivity Toggle**: Option to match case exactly
6. **Fallback Options**: Allow users to choose guillemets if their font doesn't support Unicode bold

### Why Not Implemented Yet
- Current solution works excellently
- Additional complexity may confuse users
- Waiting for user feedback and real-world usage

## Conclusion

The dual highlighting system successfully solves the Treeview limitation by combining:
- **Background highlighting** for quick visual scanning
- **Text markers** for precise term location
- **Professional grid** for full functionality

This approach maintains all the benefits of a proper TMX editor interface while providing the precise search term highlighting users need.

**Result**: A professional, functional TMX editor that doesn't compromise on features or usability.

---

*Part of Supervertaler v3.7.6 TMX Editor implementation*
