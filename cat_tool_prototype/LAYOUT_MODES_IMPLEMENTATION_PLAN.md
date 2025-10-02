# Layout Modes Implementation Plan

**Feature**: Multiple UI layouts for CAT Editor (memoQ-style and alternatives)  
**Target Version**: v0.4.0  
**Date**: October 2, 2025  
**Status**: Planning

---

## Overview

Implement three distinct layout modes that users can switch between:
1. **Grid View** (memoQ-style) - Inline editing, wide columns, no editor panel
2. **Split View** (Current) - Grid + separate editor panel below
3. **Compact View** - Maximum density, minimal columns

---

## Phase 1: Layout Switching Framework

### 1.1 Add Layout Mode Enum
```python
class LayoutMode:
    GRID = "grid"      # memoQ-style inline editing
    SPLIT = "split"    # Current style with editor panel
    COMPACT = "compact" # Maximum density view
```

### 1.2 Add Layout Selection Buttons
**Location**: Toolbar, between Import/Export and Find/Replace

**UI**:
```
[📊 Grid View] [📋 Split View] [📄 Compact View]
```

**Behavior**:
- Radio button style (only one active)
- Active button highlighted
- Click switches layout immediately
- Preference saved to settings

### 1.3 Settings Storage
```python
# Add to settings/config
{
    "layout_mode": "grid",  # default to memoQ-style
    "column_widths": {
        "grid": {...},
        "split": {...},
        "compact": {...}
    }
}
```

---

## Phase 2: Grid View (memoQ-Style) Implementation

### 2.1 UI Changes

**Remove**:
- ❌ Segment editor panel below grid
- ❌ Copy Source, Clear, Save & Next buttons (move to context menu)
- ❌ Tag insertion buttons in separate panel

**Add**:
- ✅ Wider Source/Target columns (400-500px each)
- ✅ Direct cell editing (double-click or F2)
- ✅ Inline tag validation
- ✅ Context menu for common actions
- ✅ Optional translation results panel (right side)

### 2.2 Column Configuration

```python
# Grid View columns
columns = [
    ("id", 40, False),           # ID - narrow, fixed
    ("type", 65, False),         # Type - fixed
    ("status", 95, False),       # Status - fixed
    ("source", 500, True),       # Source - wide, stretchable
    ("target", 500, True)        # Target - wide, stretchable, EDITABLE
]
```

**Note**: Remove "Style" column in Grid View for cleaner appearance (still track internally)

### 2.3 Editable Target Column

**Implementation**:
```python
def make_target_editable(self):
    """Enable direct editing in target column"""
    # Bind double-click to enter edit mode
    self.tree.bind('<Double-1>', self.on_cell_double_click)
    # Bind F2 to enter edit mode
    self.tree.bind('<F2>', self.enter_edit_mode)
    # Bind Ctrl+Enter to save and next
    self.tree.bind('<Control-Return>', self.save_and_next_inline)
```

**Edit Mode**:
1. Double-click target cell → Show Entry widget overlay
2. Entry widget positioned exactly over cell
3. Pre-filled with current target text
4. Real-time tag validation below
5. Ctrl+Enter saves and moves to next
6. Escape cancels edit
7. Click outside saves

### 2.4 Inline Tag Validation

**Location**: Small label below edited cell or in status bar

**Display**:
```
Target: [Tweede <b>zin</b> hier]    Tags: ✓ Valid
```

**Features**:
- Real-time validation as user types
- Color-coded (green ✓, red ✗, yellow ⚠)
- Show error message if invalid
- Tag insertion via context menu or shortcuts

### 2.5 Context Menu

**Right-click on target cell**:
```
Copy Source to Target     Ctrl+D
─────────────────────────
Insert Bold Tag           Ctrl+B
Insert Italic Tag         Ctrl+I
Insert Underline Tag      Ctrl+U
Copy Source Tags          Ctrl+Shift+T
Strip Tags                Ctrl+Shift+X
─────────────────────────
Clear Target              Delete
─────────────────────────
Mark as Translated        Ctrl+T
Mark as Approved          Ctrl+Shift+A
Mark as Draft             Ctrl+Shift+D
```

---

## Phase 3: Split View (Current, Enhanced)

### 3.1 Keep Current Functionality

**Maintain**:
- ✅ Grid showing all columns
- ✅ Separate editor panel below
- ✅ All tag buttons
- ✅ Copy Source, Clear, Save & Next buttons
- ✅ Status dropdown

**Enhance**:
- Better panel sizing (grid takes more vertical space)
- Resizable splitter between grid and editor
- Remember splitter position

### 3.2 Column Configuration

```python
# Split View columns (current)
columns = [
    ("id", 40, False),
    ("type", 65, False),
    ("style", 80, False),
    ("status", 95, False),
    ("source", 400, True),
    ("target", 400, True)
]
```

---

## Phase 4: Compact View Implementation

### 4.1 Minimal Column Set

```python
# Compact View columns
columns = [
    ("id", 50, False),           # ID with status indicator
    ("source", 600, True),       # Wide source
    ("target", 600, True)        # Wide target
]
```

### 4.2 Status Indicators

**Inline in ID column**:
- `1✓` - Translated
- `2✗` - Untranslated
- `3⚠` - Draft
- `4✔` - Approved

### 4.3 Type Indicators

**Shown in source/target text**:
- `[T1R2C3] Cell content` - Table cells prefixed
- Regular paragraphs have no prefix

### 4.4 Style Indicators

**Color-coded rows**:
- Heading 1 rows: Dark blue background
- Heading 2 rows: Medium blue background
- Heading 3 rows: Light blue background
- Normal rows: White background

---

## Technical Implementation

### Code Structure Changes

```python
class CATEditor:
    def __init__(self):
        self.layout_mode = LayoutMode.GRID  # Default
        self.current_edit_widget = None      # For inline editing
        
    def create_ui(self):
        """Build UI based on layout_mode"""
        if self.layout_mode == LayoutMode.GRID:
            self.create_grid_layout()
        elif self.layout_mode == LayoutMode.SPLIT:
            self.create_split_layout()
        elif self.layout_mode == LayoutMode.COMPACT:
            self.create_compact_layout()
    
    def switch_layout(self, new_mode):
        """Switch between layout modes"""
        # Save current state
        self.save_current_segment()
        current_selection = self.get_selected_segment_id()
        
        # Change mode
        self.layout_mode = new_mode
        
        # Rebuild UI
        self.destroy_current_layout()
        self.create_ui()
        self.load_segments_to_grid()
        
        # Restore selection
        self.select_segment(current_selection)
        
        # Save preference
        self.save_layout_preference()
```

### Inline Editing Implementation

```python
def enter_edit_mode(self, event=None):
    """Enter inline edit mode for target cell"""
    selection = self.tree.selection()
    if not selection:
        return
    
    item = selection[0]
    
    # Get cell bounds
    bbox = self.tree.bbox(item, column="target")
    if not bbox:
        return
    
    # Create Entry widget overlay
    self.current_edit_widget = tk.Entry(
        self.tree,
        font=('Segoe UI', 10),
        relief='solid',
        borderwidth=1
    )
    
    # Position over cell
    x, y, width, height = bbox
    self.current_edit_widget.place(
        x=x, y=y, width=width, height=height
    )
    
    # Get current target text
    segment = self.get_segment_by_item(item)
    self.current_edit_widget.insert(0, segment.target)
    self.current_edit_widget.select_range(0, tk.END)
    self.current_edit_widget.focus()
    
    # Bind keys
    self.current_edit_widget.bind('<Return>', 
        lambda e: self.save_inline_edit(go_next=False))
    self.current_edit_widget.bind('<Control-Return>', 
        lambda e: self.save_inline_edit(go_next=True))
    self.current_edit_widget.bind('<Escape>', 
        lambda e: self.cancel_inline_edit())
    self.current_edit_widget.bind('<FocusOut>', 
        lambda e: self.save_inline_edit(go_next=False))
    
    # Real-time tag validation
    self.current_edit_widget.bind('<KeyRelease>', 
        self.validate_tags_inline)

def save_inline_edit(self, go_next=False):
    """Save inline edit and optionally move to next"""
    if not self.current_edit_widget:
        return
    
    # Get edited text
    new_text = self.current_edit_widget.get()
    
    # Validate tags
    if self.tag_manager:
        is_valid, error = self.tag_manager.validate_tags(new_text)
        if not is_valid:
            messagebox.showerror("Tag Error", error)
            return
    
    # Save to segment
    segment = self.get_current_segment()
    segment.target = new_text
    segment.status = 'translated'
    
    # Update grid
    self.update_segment_in_grid(segment)
    
    # Destroy edit widget
    self.current_edit_widget.destroy()
    self.current_edit_widget = None
    
    # Move to next if requested
    if go_next:
        self.next_segment()
    
    # Mark as modified
    self.modified = True
    self.update_progress()
```

### Translation Results Panel (Optional)

```python
def create_translation_results_panel(self):
    """Create right-side panel for TM/glossary results"""
    panel = ttk.Frame(self.main_frame)
    panel.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
    
    # Title
    ttk.Label(panel, text="📊 Translation Results", 
              font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=5)
    
    # Results area (scrollable)
    results_frame = ttk.Frame(panel)
    results_frame.pack(fill='both', expand=True)
    
    # TM matches section
    ttk.Label(results_frame, text="Translation Memory:",
              font=('Segoe UI', 10, 'bold')).pack(anchor='w')
    
    self.tm_results = tk.Text(results_frame, height=10, width=40,
                              wrap='word', font=('Segoe UI', 9))
    self.tm_results.pack(fill='both', expand=True, pady=5)
    
    # Glossary section
    ttk.Label(results_frame, text="Glossary:",
              font=('Segoe UI', 10, 'bold')).pack(anchor='w')
    
    self.glossary_results = tk.Text(results_frame, height=6, width=40,
                                    wrap='word', font=('Segoe UI', 9))
    self.glossary_results.pack(fill='both', expand=True, pady=5)
    
    # Toggle button
    self.toggle_results_btn = ttk.Button(
        self.toolbar,
        text="◀ Hide Results",
        command=self.toggle_results_panel
    )
```

---

## Implementation Steps

### Step 1: Add Layout Mode Framework (1 hour)
1. Add LayoutMode enum
2. Add layout_mode property to CATEditor
3. Add layout switching buttons to toolbar
4. Implement switch_layout() method
5. Save/load layout preference

### Step 2: Refactor UI Creation (2 hours)
1. Extract current UI to create_split_layout()
2. Create modular layout creation methods
3. Test switching between modes (all show current layout initially)

### Step 3: Implement Grid View (4 hours)
1. Create create_grid_layout() method
2. Wider columns, no editor panel
3. Implement editable target column
4. Add inline editing with Entry overlay
5. Implement save_inline_edit()
6. Add context menu for actions
7. Inline tag validation indicator

### Step 4: Implement Compact View (2 hours)
1. Create create_compact_layout() method
2. Minimal columns
3. Inline status indicators
4. Color-coded rows for styles
5. Type prefixes in text

### Step 5: Polish & Testing (2 hours)
1. Keyboard shortcuts for layout switching
2. Remember column widths per layout
3. Smooth transitions between layouts
4. Test all features in each layout
5. Documentation

**Total Estimated Time**: ~11 hours

---

## Testing Plan

### Test Cases

1. **Layout Switching**
   - ✅ Switch from Grid → Split → Compact → Grid
   - ✅ Current segment selection preserved
   - ✅ Current work saved
   - ✅ Preference saved and restored on restart

2. **Grid View Inline Editing**
   - ✅ Double-click enters edit mode
   - ✅ F2 enters edit mode
   - ✅ Ctrl+Enter saves and moves to next
   - ✅ Escape cancels edit
   - ✅ Click outside saves
   - ✅ Tag validation works inline
   - ✅ Context menu accessible

3. **All Layouts**
   - ✅ Import DOCX works
   - ✅ Export DOCX works
   - ✅ Status changes work
   - ✅ Find/Replace works
   - ✅ Project save/load works
   - ✅ Tag features work

4. **Edge Cases**
   - ✅ Empty target cells
   - ✅ Long text in cells
   - ✅ Table cells vs paragraphs
   - ✅ Different styles
   - ✅ Large documents (100+ segments)

---

## UI Mockups

### Grid View (memoQ-style)
```
┌──────────────────────────────────────────────────────────────────────────┐
│ File  Edit  View  Tools                                    Progress: 45% │
├──────────────────────────────────────────────────────────────────────────┤
│ [Import] [Export] [Save] │ [📊 Grid] [Split] [Compact] │ [Find]         │
├──────────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────────────────────┐ │
│ │ #  │ Type │ Status    │ Source              │ Target               │ │
│ ├────┼──────┼───────────┼─────────────────────┼──────────────────────┤ │
│ │ 1  │ Para │ Translated│ First sentence.     │ Eerste zin.          │ │
│ │ 2  │ Para │ Draft     │ Second sentence.    │ [Editing here...]    │ │← Active edit
│ │ 3  │T1R1C1│ -         │ Table cell.         │                      │ │
│ │ 4  │ Para │ Translated│ Another sentence.   │ Nog een zin.         │ │
│ │ 5  │ Para │ -         │ More content.       │                      │ │
│ │ 6  │ Para │ Approved  │ Final sentence.     │ Laatste zin.         │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│                                             Tags: ✓ Valid                 │
├──────────────────────────────────────────────────────────────────────────┤
│ Log: Segment #2 modified                                                 │
└──────────────────────────────────────────────────────────────────────────┘
```

### Split View (Current Enhanced)
```
┌──────────────────────────────────────────────────────────────────────────┐
│ File  Edit  View  Tools                                    Progress: 45% │
├──────────────────────────────────────────────────────────────────────────┤
│ [Import] [Export] [Save] │ [Grid] [📋 Split] [Compact] │ [Find]         │
├──────────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────────────────────┐ │
│ │ #│Type│Style │Status│Source         │Target                         │ │
│ ├──┼────┼──────┼──────┼───────────────┼───────────────────────────────┤ │
│ │1 │Para│Normal│✓     │First...       │Eerste...                      │ │
│ │2 │Para│H 1   │Draft │Second...      │Tweede...                      │ │← Selected
│ │3 │T1R1│Normal│-     │Table...       │                               │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│ ┌─ Segment Editor #2 ────────────────────────────────────────────────┐   │
│ │ Source: Second sentence from heading one.                          │   │
│ │ ┌────────────────────────────────────────────────────────────────┐ │   │
│ │ │ Tweede zin uit kop één.                                        │ │   │
│ │ └────────────────────────────────────────────────────────────────┘ │   │
│ │ [Copy] [Clear] [B][I][U] [Tags▼]      Status:[Draft▼] [Save&Next] │   │
│ └────────────────────────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────────────────┤
│ Log: Segment loaded                                                      │
└──────────────────────────────────────────────────────────────────────────┘
```

### Compact View
```
┌──────────────────────────────────────────────────────────────────────────┐
│ File  Edit  View  Tools                                    Progress: 45% │
├──────────────────────────────────────────────────────────────────────────┤
│ [Import] [Export] [Save] │ [Grid] [Split] [📄 Compact] │ [Find]         │
├──────────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────────────────────┐ │
│ │ #  │ Source                           │ Target                      │ │
│ ├────┼──────────────────────────────────┼─────────────────────────────┤ │
│ │ 1✓ │ First sentence here.             │ Eerste zin hier.            │ │
│ │ 2⚠ │ Second sentence from heading.    │ Tweede zin uit kop.         │ │
│ │ 3- │ [T1R1C1] Table cell content.     │                             │ │
│ │ 4✓ │ Another normal sentence.         │ Nog een normale zin.        │ │
│ │ 5- │ More content to translate.       │                             │ │
│ │ 6✔ │ Final approved sentence.         │ Laatste goedgekeurde zin.   │ │
│ │ 7✓ │ And one more for good measure.   │ En nog één voor de zekerheid│ │
│ └──────────────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────┤
│ Log: 7 segments loaded                                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Benefits

### Grid View (memoQ-style)
- ✅ **Familiar** to memoQ users
- ✅ **Efficient** - No mouse movement between grid and editor
- ✅ **More segments visible** - No editor panel
- ✅ **Faster** - Inline editing is quicker
- ✅ **Clean** - Less UI clutter

### Split View
- ✅ **Feature-rich** - All tools easily accessible
- ✅ **Beginner-friendly** - Clear editing area
- ✅ **Better for complex edits** - More space for tags
- ✅ **Training mode** - Good for learning

### Compact View
- ✅ **Maximum visibility** - See 2x more segments
- ✅ **Review mode** - Quick QA checks
- ✅ **Overview** - See document structure
- ✅ **Speed** - Fast navigation through many segments

---

## Keyboard Shortcuts

### Layout Switching
- `Ctrl+1` - Grid View
- `Ctrl+2` - Split View
- `Ctrl+3` - Compact View

### Grid View Editing
- `F2` - Enter edit mode
- `Ctrl+Enter` - Save and next
- `Escape` - Cancel edit
- `Ctrl+D` - Copy source to target
- `Ctrl+B` - Insert bold tags
- `Ctrl+I` - Insert italic tags
- `Ctrl+U` - Insert underline tags

### Navigation (All Views)
- `↑` `↓` - Move between segments
- `Page Up` `Page Down` - Scroll grid
- `Home` - First segment
- `End` - Last segment
- `Ctrl+F` - Find/Replace
- `Ctrl+G` - Go to segment

---

## Configuration File

```json
{
    "layout": {
        "mode": "grid",
        "grid": {
            "column_widths": {
                "id": 40,
                "type": 65,
                "status": 95,
                "source": 500,
                "target": 500
            },
            "show_results_panel": false
        },
        "split": {
            "column_widths": {
                "id": 40,
                "type": 65,
                "style": 80,
                "status": 95,
                "source": 400,
                "target": 400
            },
            "splitter_position": 0.7
        },
        "compact": {
            "column_widths": {
                "id": 50,
                "source": 600,
                "target": 600
            }
        }
    },
    "keyboard_shortcuts": {
        "layout_grid": "Control-1",
        "layout_split": "Control-2",
        "layout_compact": "Control-3",
        "edit_mode": "F2",
        "save_and_next": "Control-Return"
    }
}
```

---

## Documentation Updates Needed

1. Update README.md with layout modes
2. Add keyboard shortcuts reference
3. Create LAYOUT_MODES_GUIDE.md
4. Update screenshots
5. Add layout switching to quick start guide

---

## Version Planning

**v0.4.0**: Layout Modes Update
- Multiple UI layouts
- memoQ-style grid editing
- Inline editing features
- Context menus
- Layout preferences

**Future** (v0.5.0+):
- Translation results panel
- TM integration
- Glossary integration
- Concordance search

---

## Success Criteria

- ✅ Users can switch between 3 layouts seamlessly
- ✅ Grid View provides memoQ-like experience
- ✅ All existing features work in all layouts
- ✅ Layout preference persists across sessions
- ✅ Performance remains good with all layouts
- ✅ Keyboard shortcuts work consistently
- ✅ No data loss when switching layouts

---

**Status**: Ready to implement  
**Priority**: High (major UX improvement)  
**Target**: v0.4.0  
**Estimated Time**: ~11 hours development + testing
