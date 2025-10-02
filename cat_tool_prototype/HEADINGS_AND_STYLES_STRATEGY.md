# Headings and Word Styles - Analysis & Strategy

## Current State Analysis

### ✅ What We're Already Capturing

**Good news!** The CAT Editor is **already storing style information**:

```python
para_info = ParagraphInfo(
    text=text,
    style=para.style.name if para.style else None,  # ✅ Already captured!
    alignment=str(para.alignment) if para.alignment else None,
    paragraph_index=para_counter,
    is_table_cell=False
)
```

**Styles being captured include:**
- `Heading 1`, `Heading 2`, `Heading 3`, etc.
- `Title`, `Subtitle`
- `Normal` (body text)
- `List Paragraph`
- `Quote`, `Intense Quote`
- Custom styles
- Any other Word style

### ❌ What We're NOT Doing Yet

**The problem:** We capture the style but don't:
1. **Display it** to the translator (can't see if something is a heading)
2. **Preserve it** on export (everything becomes Normal paragraph)
3. **Filter by it** (can't isolate headings for review)
4. **Use it for context** (translators need to know heading vs body text)

## The Problem in Detail

### Issue #1: Invisible Headings

**What happens now:**
```
Original Document:
  Heading 1: "Introduction"
  Normal: "This is the first paragraph."
  Heading 2: "Background"
  Normal: "More details here."

CAT Editor Display:
  #1 | Para | Source: Introduction
  #2 | Para | Source: This is the first paragraph.
  #3 | Para | Source: Background
  #4 | Para | Source: More details here.
```

**The translator can't tell which are headings!** They all look the same.

### Issue #2: Lost Styles on Export

**What happens now:**
```python
# Export reconstructs document but loses styles
# Everything becomes "Normal" paragraph style
```

**Result:** Translated document has no headings, no structure!

### Issue #3: No Context for Translation

**Headings need different treatment:**
- Headings are often **shorter, punchier**
- Headings may use **title case** in English (all words capitalized)
- Headings may need **different terminology** (formal vs casual)
- Headings provide **context** for following paragraphs

## Proposed Solutions

### 🎯 Solution Strategy

I recommend a **phased approach**:

#### **Phase A: Visual Display (Easy, High Impact)** ⭐ **DO THIS FIRST**
- Add style information to segment grid
- Show heading level visually
- Color-code or icon-code different styles

#### **Phase B: Style Preservation (Medium, Critical)**
- Preserve original style on export
- Apply style to translated paragraph
- Maintain heading hierarchy

#### **Phase C: Advanced Features (Complex, Nice-to-Have)**
- Filter segments by style
- Style-specific translation settings
- Custom style mapping (Heading 1 EN → Heading 1 ES)

---

## Phase A: Visual Display (Recommended Next Step)

### Implementation Plan

#### 1. Add Style Column to Grid

**Before:**
```
ID | Type   | Status | Source              | Target
---+--------+--------+---------------------+--------
1  | Para   | ...    | Introduction        | ...
2  | Para   | ...    | This is the first...| ...
```

**After:**
```
ID | Type   | Style      | Status | Source              | Target
---+--------+------------+--------+---------------------+--------
1  | Para   | Heading 1  | ...    | Introduction        | ...
2  | Para   | Normal     | ...    | This is the first...| ...
3  | Para   | Heading 2  | ...    | Background          | ...
4  | T1R1C1 | Normal     | ...    | Party A             | ...
```

#### 2. Visual Styling by Type

**Color/Font Coding:**
- **Heading 1**: Bold, larger font, dark blue
- **Heading 2**: Bold, medium font, medium blue
- **Heading 3**: Bold, regular font, light blue
- **Title**: Bold, larger font, purple
- **Normal**: Regular (current display)
- **Quote**: Italic, gray

### Code Changes Required

#### Update Segment Class
```python
class Segment:
    def __init__(self, seg_id: int, source: str, paragraph_id: int = 0, 
                 is_table_cell: bool = False, table_info: tuple = None,
                 style: str = None):  # ✨ Add style parameter
        self.id = seg_id
        self.source = source
        self.target = ""
        self.status = "untranslated"
        self.paragraph_id = paragraph_id
        self.notes = ""
        self.modified = False
        self.created_at = datetime.now().isoformat()
        self.modified_at = datetime.now().isoformat()
        
        # Table information
        self.is_table_cell = is_table_cell
        self.table_info = table_info
        
        # Style information ✨ NEW
        self.style = style or "Normal"
```

#### Update Treeview
```python
# Add style column
self.tree = ttk.Treeview(grid_frame,
                        columns=('id', 'type', 'style', 'status', 'source', 'target'),
                        show='headings',
                        selectmode='browse')

# Define column
self.tree.heading('style', text='Style')
self.tree.column('style', width=100, anchor='w')

# Configure tags for different styles
self.tree.tag_configure('heading1', font=('TkDefaultFont', 10, 'bold'), 
                       foreground='#003366')
self.tree.tag_configure('heading2', font=('TkDefaultFont', 9, 'bold'), 
                       foreground='#0066cc')
self.tree.tag_configure('heading3', font=('TkDefaultFont', 9, 'bold'), 
                       foreground='#3399ff')
self.tree.tag_configure('title', font=('TkDefaultFont', 11, 'bold'), 
                       foreground='#663399')
```

#### Update Import Workflow
```python
# When creating segments
for seg_id, (para_id, text) in enumerate(segmented, 1):
    para_info = self.docx_handler._get_para_info(para_id)
    
    is_table = False
    table_info = None
    style = "Normal"  # Default
    
    if para_info:
        style = para_info.style or "Normal"  # ✨ Get style
        if para_info.is_table_cell:
            is_table = True
            table_info = (para_info.table_index, para_info.row_index, para_info.cell_index)
    
    segment = Segment(seg_id, text, para_id, is_table, table_info, style)  # ✨ Pass style
    self.segments.append(segment)
```

#### Update Display Logic
```python
def load_segments_to_grid(self):
    for seg in self.segments:
        # Determine type label
        if seg.is_table_cell and seg.table_info:
            type_label = f"T{seg.table_info[0]+1}R{seg.table_info[1]+1}C{seg.table_info[2]+1}"
        else:
            type_label = "Para"
        
        # Determine style display
        style_display = self._format_style_name(seg.style)  # ✨ Format style
        
        # Set tags for styling
        tags = [seg.status]
        if seg.is_table_cell:
            tags.append('table_cell')
        
        # Add style tag ✨ NEW
        style_tag = self._get_style_tag(seg.style)
        if style_tag:
            tags.append(style_tag)
        
        self.tree.insert('', 'end',
                       values=(seg.id, type_label, style_display, seg.status.capitalize(),
                              self._truncate(seg.source, 80),
                              self._truncate(seg.target, 80)),
                       tags=tuple(tags))

def _format_style_name(self, style: str) -> str:
    """Format style name for display"""
    if not style or style == "Normal":
        return "Normal"
    # Shorten common styles
    style = style.replace("Heading", "H")
    return style

def _get_style_tag(self, style: str) -> str:
    """Get treeview tag for style"""
    if not style:
        return None
    style_lower = style.lower()
    if 'heading 1' in style_lower:
        return 'heading1'
    elif 'heading 2' in style_lower:
        return 'heading2'
    elif 'heading 3' in style_lower:
        return 'heading3'
    elif 'title' in style_lower:
        return 'title'
    return None
```

### Estimated Time: 1-2 hours

### Benefits:
- ✅ **Immediate visual feedback** for translators
- ✅ **No breaking changes** to existing functionality
- ✅ **Easy to implement** (we already have the data!)
- ✅ **High value** for professional documents

---

## Phase B: Style Preservation

### Implementation Plan

#### 1. Preserve Style on Export

**Current export logic:**
```python
# Replaces text but doesn't restore style
self._replace_paragraph_text(para, new_text)
```

**Enhanced export logic:**
```python
def export_docx(self, segments: List[Dict[str, Any]], output_path: str, 
                preserve_formatting: bool = True):
    # ... existing code ...
    
    # When processing paragraph
    if para_info and not para_info.is_table_cell:
        translations = [s['target'] for s in para_segments[para_info.paragraph_index]]
        
        if translations:
            new_text = ' '.join(translations)
            self._replace_paragraph_text(para, new_text)
            
            # ✨ Restore original style
            if para_info.style:
                para.style = para_info.style  # Apply original style
```

#### 2. Handle Style Edge Cases

**Considerations:**
- What if translator adds multiple sentences to a heading?
- What if style doesn't exist in output document?
- What about custom styles?

**Solution: Style mapping with fallbacks**
```python
def _apply_style(self, paragraph, style_name: str):
    """Apply style with fallback handling"""
    try:
        paragraph.style = style_name
    except KeyError:
        # Style doesn't exist - try to map it
        mapped_style = self._map_style(style_name)
        if mapped_style:
            paragraph.style = mapped_style
        else:
            # Fallback to Normal
            paragraph.style = 'Normal'
            print(f"Warning: Style '{style_name}' not found, using 'Normal'")

def _map_style(self, style_name: str) -> str:
    """Map styles that might not exist"""
    # Common mappings
    mappings = {
        'Heading1': 'Heading 1',
        'Heading2': 'Heading 2',
        'Heading3': 'Heading 3',
        'Title': 'Title',
        # Add more as needed
    }
    return mappings.get(style_name)
```

### Estimated Time: 2-3 hours

### Benefits:
- ✅ **Professional output** - headings preserved
- ✅ **Structure maintained** - document hierarchy intact
- ✅ **Client-ready** - no manual reformatting needed

---

## Phase C: Advanced Features (Future)

### Potential Features

#### 1. Filter by Style
```python
# Filter dropdown
self.style_filter = ttk.Combobox(toolbar, 
                                 values=['All', 'Headings Only', 'Body Text', 'Tables'])
```

#### 2. Style-Specific Settings
```python
# Different prompts for headings vs body text
if segment.style.startswith('Heading'):
    prompt = "Translate this heading (keep it concise):"
else:
    prompt = "Translate this paragraph:"
```

#### 3. Style Analytics
```python
# Show statistics
stats = {
    'Heading 1': 5,
    'Heading 2': 12,
    'Normal': 150,
    'Table Cells': 24
}
```

#### 4. Custom Style Mapping
```python
# Allow user to map styles between languages
style_map = {
    'Heading 1': 'Título 1',  # Spanish
    'Quote': 'Cita'
}
```

### Estimated Time: 5-8 hours (all features)

---

## Recommendations

### 🚀 **Immediate Action (Phase A)**

**I recommend implementing Phase A now** (1-2 hours):
1. Add style column to grid
2. Add visual styling for headings
3. Update segment display logic

**Why now?**
- Easy to implement (data already captured)
- High impact (immediate translator feedback)
- No risk (backward compatible)
- Completes the "visual information" aspect of CAT editor

### ⏳ **Near-Term (Phase B)**

**Implement Phase B during integration** (Phase 1 or 2):
1. Style preservation on export
2. Style mapping with fallbacks
3. Testing with various document types

**Why then?**
- More complex (requires careful export testing)
- Critical for professional output
- Natural fit during Phase 4 (DOCX Export)

### 🔮 **Long-Term (Phase C)**

**Consider Phase C for v2.6.0 or later**:
- Filter by style
- Style-specific translation settings
- Advanced analytics

**Why later?**
- Nice-to-have, not essential
- Requires UI/UX design
- Better after gathering user feedback

---

## Implementation Priority

### High Priority ⭐⭐⭐
1. **Visual display of styles** (Phase A) - DO NOW
2. **Style preservation on export** (Phase B) - DO DURING INTEGRATION

### Medium Priority ⭐⭐
3. **Style mapping/fallbacks** (Phase B) - DO DURING INTEGRATION
4. **Filter by style** (Phase C) - AFTER INITIAL RELEASE

### Low Priority ⭐
5. **Style-specific settings** (Phase C) - BASED ON USER FEEDBACK
6. **Style analytics** (Phase C) - NICE TO HAVE

---

## Technical Considerations

### Style Names in Word

**Common Word styles:**
- `Normal` - Default paragraph
- `Heading 1`, `Heading 2`, `Heading 3`, `Heading 4`, etc.
- `Title`, `Subtitle`
- `List Paragraph`, `List`, `List 2`, `List 3`
- `Quote`, `Intense Quote`
- `Caption`
- `Header`, `Footer`
- Custom user-defined styles

### Style Objects in python-docx

```python
# Access style
para.style.name  # String: "Heading 1"
para.style.style_id  # String: "Heading1" (no space)

# Apply style
para.style = 'Heading 1'  # By name
para.style = document.styles['Heading1']  # By style object
```

### Potential Issues

1. **Localized style names**
   - German Word: "Überschrift 1" not "Heading 1"
   - Solution: Use style_id (language-independent)

2. **Custom styles**
   - May not exist in output document
   - Solution: Fallback mapping + warning

3. **Style changes**
   - What if translator splits heading into multiple sentences?
   - Solution: Keep first segment's style, subsequent become Normal

---

## Real-World Example

### Document with Headings

**Original:**
```
[Heading 1] Introduction
[Normal] This document outlines the terms...
[Heading 2] Definitions
[Normal] For purposes of this agreement...
[Heading 2] Obligations
[Normal] Party A shall...
[List Paragraph] • Provide services
[List Paragraph] • Maintain quality
```

### CAT Editor Display (Phase A)

```
ID | Type | Style     | Status | Source
---+------+-----------+--------+-------------------------
1  | Para | H 1       | Draft  | Introduction
2  | Para | Normal    | Draft  | This document outlines...
3  | Para | H 2       | Draft  | Definitions
4  | Para | Normal    | Draft  | For purposes of this...
5  | Para | H 2       | Draft  | Obligations
6  | Para | Normal    | Draft  | Party A shall...
7  | Para | List Para | Draft  | • Provide services
8  | Para | List Para | Draft  | • Maintain quality
```

**Visual effects:**
- Row 1: **Bold, dark blue** (Heading 1)
- Row 3, 5: **Bold, medium blue** (Heading 2)
- Row 7, 8: *Indented, bullet* (List)

### Exported Document (Phase B)

```
Translation completes, export clicked...

✅ Heading 1 style preserved
✅ Heading 2 styles preserved
✅ List formatting preserved
✅ Normal paragraphs preserved
✅ Document structure intact!
```

---

## Next Steps Decision

### Option 1: Implement Phase A Now (Recommended) ⭐
**Time**: 1-2 hours
**Value**: High immediate impact

**Action**: 
- Add style column
- Add visual styling
- Update display logic
- Test with heading-heavy document

### Option 2: Wait Until Integration
**Time**: Save for later
**Risk**: Translators won't see heading context

### Option 3: Implement A + B Together
**Time**: 3-4 hours
**Value**: Complete style support in one go

---

## My Recommendation 🎯

**Implement Phase A immediately** (add style column + visual display):

**Why:**
1. Quick win (1-2 hours)
2. We already have the data
3. Completes the "information display" for CAT editor
4. Makes Phase 0.2 testing more valuable (test with real documents that have headings)
5. Phase B (export) can wait until Phase 4 of integration

**Then:**
- Phase 0.2 testing will reveal if we need style filtering or other features
- Phase B (export preservation) fits naturally into Phase 4 (DOCX Export)
- Phase C (advanced features) can be based on real user feedback

---

**Would you like me to implement Phase A now?** It would take the CAT Editor from v0.3.0 to v0.3.1 with full heading visibility! 🚀
