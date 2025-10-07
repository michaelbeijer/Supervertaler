# Dual Selection Implementation Plan

**Date**: October 4, 2025  
**Feature**: Dual text selection in Grid View  
**Reference**: https://michaelbeijer.co.uk/what_i_look_for_in_a_cat_tool

---

## 📋 Feature Overview

### What is Dual Selection?

The ability to make **two simultaneous independent text selections** - one in the source column and one in the target column of the same segment. This is essential for:

- Translating long segments methodically
- Checking corresponding pieces of text
- Ensuring nothing is missed
- Visual verification of translation completeness

**Reference**: memoQ has this feature and it's considered non-negotiable by professional translators.

---

## 🎯 User Experience Design

### Visual Behavior

**When dual selection is active:**
1. User can select text in the source Text widget (e.g., "transfer pricing arrangements")
2. User can then select text in the target Text widget (e.g., "verrechnungspreisvereinbarungen")
3. **Both selections remain visible simultaneously** with distinct colors
4. Clicking elsewhere or navigating away clears both selections

### Visual Design

**Source Selection**:
- Background: `#B3E5FC` (light blue)
- Foreground: `#01579B` (dark blue)
- Tag name: `source_selection`

**Target Selection**:
- Background: `#C8E6C9` (light green)
- Foreground: `#1B5E20` (dark green)
- Tag name: `target_selection`

**Purpose**: Different colors make it easy to see both selections at once

---

## 🏗️ Technical Architecture

### Current State Analysis

**Grid Row Structure** (Line 403):
```python
self.grid_rows = []  # List of row data: {'segment': seg, 'widgets': {...}, 'row_frame': frame}
```

**Each row contains** (Lines 2920-2990):
- `widgets['source']` - tk.Text widget (source column)
- `widgets['target']` - tk.Text widget (target column)
- `widgets['source_frame']`, `widgets['target_frame']` - container frames
- Various other widgets (ID, type, status labels)

**Current Click Handlers**:
- Line 2930: `source_text.bind('<Button-1>', lambda e, idx=row_index: self.on_text_widget_click(e, idx))`
- Line 2972: `target_text.bind('<Button-1>', lambda e, idx=row_index: self.on_target_click(e, idx))`

---

## 🔧 Implementation Strategy

### Phase 1: Data Structure (DONE - already exists)

The grid infrastructure is ready:
- ✅ Source and target are separate Text widgets
- ✅ Text widgets support tags and selections
- ✅ Row data structure is accessible

### Phase 2: Selection State Management (NEW)

**Add to `__init__` method** (around Line 170):
```python
# Dual selection state
self.dual_selection_active = False
self.dual_selection_row = None  # Which row has dual selection
self.dual_selection_source_range = None  # (start, end) positions
self.dual_selection_target_range = None  # (start, end) positions
```

### Phase 3: Selection Tracking (NEW METHODS)

**Method 1: `enable_dual_selection_mode(row_index)`**
- Activates dual selection for a specific row
- Configures Text widgets for selection tracking
- Sets up visual indicators

**Method 2: `on_source_text_select(event, row_index)`**
- Captures selection in source Text widget
- Stores selection range
- Applies source selection tag
- Prevents default row selection

**Method 3: `on_target_text_select(event, row_index)`**
- Captures selection in target Text widget
- Stores selection range
- Applies target selection tag
- Prevents default row selection

**Method 4: `clear_dual_selection()`**
- Removes selection tags from both widgets
- Resets dual selection state
- Returns widgets to normal state

**Method 5: `update_dual_selection_visual()`**
- Applies colored tags to selected text ranges
- Makes both selections visible simultaneously

### Phase 4: Event Binding Modifications

**Modify existing click handlers**:

**For Source Text** (Line 2930):
```python
# OLD:
source_text.bind('<Button-1>', lambda e, idx=row_index: self.on_text_widget_click(e, idx))

# NEW:
source_text.bind('<Button-1>', lambda e, idx=row_index: self.on_source_text_click(e, idx))
source_text.bind('<ButtonRelease-1>', lambda e, idx=row_index: self.on_source_selection_made(e, idx))
```

**For Target Text** (Line 2972):
```python
# OLD:
target_text.bind('<Button-1>', lambda e, idx=row_index: self.on_target_click(e, idx))

# NEW:
target_text.bind('<Button-1>', lambda e, idx=row_index: self.on_target_text_click(e, idx))
target_text.bind('<ButtonRelease-1>', lambda e, idx=row_index: self.on_target_selection_made(e, idx))
```

### Phase 5: Activation Logic

**Dual selection activates when**:
1. User clicks in source or target Text widget
2. User drags to select text (not just a single click)
3. Widget is in **read-only mode** (not edit mode)

**Dual selection deactivates when**:
1. User clicks outside the current row
2. User navigates to different segment
3. User enters edit mode (double-click or F2)
4. User presses Escape

---

## 📝 Detailed Implementation

### Step 1: Add Selection State Variables

**Location**: `__init__` method around Line 170

```python
# Dual text selection feature (for comparing source/target)
self.dual_selection_row = None  # Currently active row index
self.dual_selection_source = None  # Source Text widget with selection
self.dual_selection_target = None  # Target Text widget with selection
```

### Step 2: Create Selection Handler Methods

**Location**: After grid editing methods (around Line 3300)

```python
def on_source_text_click(self, event, row_index):
    """Handle click in source text - potential start of dual selection"""
    # First, handle row selection
    self.select_grid_row(row_index)
    
    # Check if this is a text selection (drag) or just a click
    # We'll detect selection in the ButtonRelease event
    
    # Clear any existing dual selection from other rows
    if self.dual_selection_row is not None and self.dual_selection_row != row_index:
        self.clear_dual_selection()
    
    self.dual_selection_row = row_index
    row_data = self.grid_rows[row_index]
    self.dual_selection_source = row_data['widgets']['source']

def on_source_selection_made(self, event, row_index):
    """Handle selection made in source text"""
    if row_index != self.dual_selection_row:
        return
    
    source_widget = self.grid_rows[row_index]['widgets']['source']
    
    # Check if there's a selection
    try:
        selection_start = source_widget.index(tk.SEL_FIRST)
        selection_end = source_widget.index(tk.SEL_LAST)
        
        # Store the selection and highlight it
        if selection_start != selection_end:
            # Remove existing source selection tag
            source_widget.tag_remove('dual_sel_source', '1.0', tk.END)
            
            # Add colored tag for source selection
            source_widget.tag_add('dual_sel_source', selection_start, selection_end)
            source_widget.tag_config('dual_sel_source',
                                    background='#B3E5FC',  # Light blue
                                    foreground='#01579B')  # Dark blue
            
            # Raise the tag above other tags
            source_widget.tag_raise('dual_sel_source')
            
            self.log(f"Source selection: {source_widget.get(selection_start, selection_end)}")
    except tk.TclError:
        # No selection made
        pass

def on_target_text_click(self, event, row_index):
    """Handle click in target text - potential start of dual selection"""
    # First, handle row selection
    self.select_grid_row(row_index)
    
    # Check if this is the same row
    if self.dual_selection_row is not None and self.dual_selection_row != row_index:
        self.clear_dual_selection()
    
    self.dual_selection_row = row_index
    row_data = self.grid_rows[row_index]
    self.dual_selection_target = row_data['widgets']['target']
    
    # Don't enter edit mode on single click - only on double-click
    # This allows for selection without editing

def on_target_selection_made(self, event, row_index):
    """Handle selection made in target text"""
    if row_index != self.dual_selection_row:
        return
    
    target_widget = self.grid_rows[row_index]['widgets']['target']
    
    # Check if there's a selection
    try:
        selection_start = target_widget.index(tk.SEL_FIRST)
        selection_end = target_widget.index(tk.SEL_LAST)
        
        # Store the selection and highlight it
        if selection_start != selection_end:
            # Remove existing target selection tag
            target_widget.tag_remove('dual_sel_target', '1.0', tk.END)
            
            # Add colored tag for target selection
            target_widget.tag_add('dual_sel_target', selection_start, selection_end)
            target_widget.tag_config('dual_sel_target',
                                    background='#C8E6C9',  # Light green
                                    foreground='#1B5E20')  # Dark green
            
            # Raise the tag above other tags
            target_widget.tag_raise('dual_sel_target')
            
            self.log(f"Target selection: {target_widget.get(selection_start, selection_end)}")
    except tk.TclError:
        # No selection made
        pass

def clear_dual_selection(self):
    """Clear dual text selection highlights"""
    if self.dual_selection_row is not None:
        row_data = self.grid_rows[self.dual_selection_row]
        
        # Clear source selection tag
        if 'source' in row_data['widgets']:
            source_widget = row_data['widgets']['source']
            source_widget.tag_remove('dual_sel_source', '1.0', tk.END)
        
        # Clear target selection tag
        if 'target' in row_data['widgets']:
            target_widget = row_data['widgets']['target']
            target_widget.tag_remove('dual_sel_target', '1.0', tk.END)
    
    self.dual_selection_row = None
    self.dual_selection_source = None
    self.dual_selection_target = None
```

### Step 3: Modify Existing Click Handlers

**Location**: In `create_grid_row` method (Lines 2930 and 2972)

**CHANGE 1** - Source text binding (around Line 2930):
```python
# OLD:
source_text.bind('<Button-1>', lambda e, idx=row_index: self.on_text_widget_click(e, idx))

# NEW:
source_text.bind('<Button-1>', lambda e, idx=row_index: self.on_source_text_click(e, idx))
source_text.bind('<ButtonRelease-1>', lambda e, idx=row_index: self.on_source_selection_made(e, idx))
```

**CHANGE 2** - Target text binding (around Line 2972):
```python
# OLD:
target_text.bind('<Button-1>', lambda e, idx=row_index: self.on_target_click(e, idx))

# NEW:
target_text.bind('<Button-1>', lambda e, idx=row_index: self.on_target_text_click(e, idx))
target_text.bind('<ButtonRelease-1>', lambda e, idx=row_index: self.on_target_selection_made(e, idx))
```

### Step 4: Clear Selection on Row Change

**Location**: In `select_grid_row` method (around Line 2716)

```python
def select_grid_row(self, row_index):
    """Select a row in the grid and update current segment"""
    if row_index < 0 or row_index >= len(self.grid_rows):
        return
    
    # Clear dual selection if changing rows
    if self.dual_selection_row is not None and self.dual_selection_row != row_index:
        self.clear_dual_selection()
    
    # ... rest of existing code
```

### Step 5: Clear Selection on Edit Mode Entry

**Location**: In `enter_edit_mode` method (around Line 3088)

Add at the beginning:
```python
def enter_edit_mode(self, event=None):
    """Enter inline edit mode for target cell"""
    # Clear dual selection when entering edit mode
    self.clear_dual_selection()
    
    # ... rest of existing code
```

---

## 🎨 User Interface Indicators

### Visual Feedback

**When dual selection is active**:
- Source selection: Light blue background (`#B3E5FC`)
- Target selection: Light green background (`#C8E6C9`)
- Both selections visible simultaneously
- Selection colors distinct from:
  - Edit mode yellow (`#ffffcc`)
  - Filter highlights (bright yellow `#FFFF00`)
  - Status colors (green, orange, pink, purple)

### Status Bar Feedback

**Optional enhancement**: Show selection info in status bar
```python
# In on_source_selection_made and on_target_selection_made:
selected_text = widget.get(selection_start, selection_end)
self.log(f"Selection: '{selected_text}' ({len(selected_text)} characters)")
```

---

## ⚙️ Configuration & Settings

### User Preferences (Future Enhancement)

Could add to filter preferences or separate section:
```python
'dual_selection_preferences': {
    'source_color': '#B3E5FC',
    'target_color': '#C8E6C9',
    'auto_clear_on_nav': True,
    'show_selection_stats': True
}
```

### Keyboard Shortcuts (Future Enhancement)

- `Ctrl+Shift+C` - Clear dual selections
- `Escape` - Clear dual selections (already clears on row change)

---

## 🧪 Testing Checklist

### Basic Functionality
- [ ] Can select text in source column
- [ ] Can select text in target column
- [ ] Both selections visible simultaneously
- [ ] Selections have distinct colors
- [ ] Selections clear when changing rows
- [ ] Selections clear when entering edit mode

### Edge Cases
- [ ] Multiple selections in same widget (only last should show)
- [ ] Clicking without dragging (no selection)
- [ ] Very long segments with scrolling
- [ ] Empty source or target
- [ ] Segments with inline tags

### Integration
- [ ] Doesn't interfere with normal row selection
- [ ] Doesn't interfere with edit mode
- [ ] Doesn't interfere with filter highlighting
- [ ] Doesn't interfere with status colors
- [ ] Works with keyboard navigation

### Performance
- [ ] Fast with 100+ segments
- [ ] No lag when selecting long text
- [ ] Smooth visual updates

---

## 📦 Deliverables

### Code Changes
1. ✅ State variables in `__init__`
2. ✅ 6 new methods for dual selection
3. ✅ 2 modified event bindings in `create_grid_row`
4. ✅ 1 modification in `select_grid_row`
5. ✅ 1 modification in `enter_edit_mode`

### Documentation
1. ✅ This implementation plan
2. ⏳ User guide update (QUICK_REFERENCE.md)
3. ⏳ WHATS_NEW update for next version
4. ⏳ CHANGELOG entry

### Version
- **Target Version**: v0.4.2 or v0.5.0
- **Feature Type**: Non-negotiable professional CAT tool feature
- **Priority**: High (requested by user, aligns with blog requirements)

---

## 🔄 Future Enhancements

### Phase 2 Features (Optional)
1. **Selection Statistics**: Show character/word count of selections
2. **Copy Both**: Keyboard shortcut to copy both selections
3. **Selection History**: Remember recent selections
4. **Highlight Matching**: Automatically highlight matching terms in other column
5. **Selection Presets**: Save common selection patterns
6. **Multi-row Selection**: Allow selections across multiple segments

### Integration with Other Views
- List View: Add dual selection to list view
- Document View: Visual indicators for selected ranges

---

## ✅ Success Criteria

**The feature is successful if**:
1. ✅ User can select text in source and target simultaneously
2. ✅ Both selections are clearly visible with distinct colors
3. ✅ Selections don't interfere with existing functionality
4. ✅ Performance is unaffected
5. ✅ User experience feels natural and intuitive
6. ✅ Aligns with professional CAT tool standards (memoQ reference)

---

**Status**: Ready for implementation  
**Estimated Time**: 2-3 hours (coding + testing)  
**Complexity**: Medium (requires event handling and visual state management)
