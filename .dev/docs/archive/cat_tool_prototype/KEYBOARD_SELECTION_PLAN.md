# Keyboard-Based Dual Selection - Enhancement Plan

**Date**: October 4, 2025  
**Enhancement**: Keyboard shortcuts for dual text selection  
**Reference**: memoQ-style Ctrl+Shift+Arrow key selection

---

## 🎯 Feature Overview

### Current Implementation
- ✅ Mouse-based dual selection (click and drag)
- ✅ Works well but requires mouse

### Enhancement Goal
Add **keyboard-based selection** using Ctrl+Shift+Arrow keys, matching memoQ's behavior:

- `Ctrl+Shift+Left` - Extend selection left by one character
- `Ctrl+Shift+Right` - Extend selection right by one character
- `Ctrl+Shift+Ctrl+Left` - Extend selection left by one word
- `Ctrl+Shift+Ctrl+Right` - Extend selection right by one word
- `Tab` - Switch focus between source and target widgets
- `Escape` - Clear current selections

---

## 🎨 User Experience Design

### Workflow Example

**Scenario**: Translating a long legal segment

```
1. Select row in Grid View
2. Press Tab to focus source widget
3. Use Ctrl+Shift+Right to select "transfer pricing arrangements"
4. Press Tab to switch to target widget
5. Use Ctrl+Shift+Right to select "Verrechnungspreisvereinbarungen"
6. Both selections visible with color coding
```

### Benefits
- ✅ Hands stay on keyboard (faster workflow)
- ✅ Precise character-by-character control
- ✅ Word-by-word selection for speed
- ✅ Professional translator workflow
- ✅ Matches memoQ behavior

---

## 🔧 Implementation Strategy

### Phase 1: Focus Management

**Add focus tracking:**
```python
self.dual_selection_focused_widget = None  # 'source' or 'target'
```

**Tab key switches focus:**
- Tab when in source → Focus target
- Tab when in target → Focus source
- Visual indicator (subtle border or highlight)

### Phase 2: Keyboard Selection

**Key bindings needed:**
```python
# Character-by-character selection
widget.bind('<Control-Shift-Left>', lambda e: self.extend_selection_left(widget, 'char'))
widget.bind('<Control-Shift-Right>', lambda e: self.extend_selection_right(widget, 'char'))

# Word-by-word selection
widget.bind('<Control-Shift-Control-Left>', lambda e: self.extend_selection_left(widget, 'word'))
widget.bind('<Control-Shift-Control-Right>', lambda e: self.extend_selection_right(widget, 'word'))

# Clear selections
widget.bind('<Escape>', lambda e: self.clear_dual_selection())

# Tab to switch focus
widget.bind('<Tab>', lambda e: self.switch_dual_selection_focus())
```

### Phase 3: Selection Extension Logic

**Method: `extend_selection_left(widget, unit)`**
```python
1. Get current cursor position
2. Move cursor left by unit (char or word)
3. Update selection range
4. Apply colored tag
5. Prevent default Tab behavior (return 'break')
```

**Method: `extend_selection_right(widget, unit)`**
```python
1. Get current cursor position
2. Move cursor right by unit (char or word)
3. Update selection range
4. Apply colored tag
5. Prevent default Tab behavior (return 'break')
```

### Phase 4: Visual Focus Indicator

**When source is focused:**
```python
source_widget.config(relief='solid', highlightthickness=2, highlightcolor='#2196F3')
target_widget.config(relief='flat', highlightthickness=0)
```

**When target is focused:**
```python
target_widget.config(relief='solid', highlightthickness=2, highlightcolor='#4CAF50')
source_widget.config(relief='flat', highlightthickness=0)
```

---

## 📝 Detailed Implementation

### Step 1: Add Focus State Variable

```python
# In __init__ method
self.dual_selection_focused_widget = None  # 'source', 'target', or None
self.dual_selection_focus_visual = {}  # Store visual state
```

### Step 2: Create Focus Management Methods

```python
def focus_source_for_selection(self, row_index):
    """Focus source widget for keyboard selection"""
    if row_index < 0 or row_index >= len(self.grid_rows):
        return
    
    row_data = self.grid_rows[row_index]
    source_widget = row_data['widgets']['source']
    
    # Enable the widget temporarily for keyboard input
    source_widget.config(state='normal')
    source_widget.focus_set()
    
    # Visual indicator
    source_widget.config(relief='solid', highlightthickness=2, 
                        highlightbackground='#2196F3', highlightcolor='#2196F3')
    
    # Clear target focus indicator
    if 'target' in row_data['widgets']:
        target_widget = row_data['widgets']['target']
        target_widget.config(relief='flat', highlightthickness=0)
    
    self.dual_selection_focused_widget = 'source'
    self.dual_selection_row = row_index

def focus_target_for_selection(self, row_index):
    """Focus target widget for keyboard selection"""
    if row_index < 0 or row_index >= len(self.grid_rows):
        return
    
    row_data = self.grid_rows[row_index]
    target_widget = row_data['widgets']['target']
    
    # Target should already be enabled for editing
    target_widget.focus_set()
    
    # Visual indicator
    target_widget.config(relief='solid', highlightthickness=2,
                        highlightbackground='#4CAF50', highlightcolor='#4CAF50')
    
    # Clear source focus indicator
    if 'source' in row_data['widgets']:
        source_widget = row_data['widgets']['source']
        source_widget.config(relief='flat', highlightthickness=0)
    
    self.dual_selection_focused_widget = 'target'
    self.dual_selection_row = row_index

def switch_dual_selection_focus(self):
    """Switch focus between source and target (Tab key)"""
    if self.current_row_index < 0 or self.current_row_index >= len(self.grid_rows):
        return 'break'
    
    if self.dual_selection_focused_widget == 'source':
        self.focus_target_for_selection(self.current_row_index)
    elif self.dual_selection_focused_widget == 'target':
        self.focus_source_for_selection(self.current_row_index)
    else:
        # Start with source
        self.focus_source_for_selection(self.current_row_index)
    
    return 'break'  # Prevent default Tab behavior
```

### Step 3: Create Selection Extension Methods

```python
def extend_selection_keyboard(self, widget, direction, unit, widget_type):
    """Extend selection using keyboard (Ctrl+Shift+Arrow)
    
    Args:
        widget: The Text widget (source or target)
        direction: 'left' or 'right'
        unit: 'char' or 'word'
        widget_type: 'source' or 'target'
    """
    try:
        # Get current insert position
        current_pos = widget.index(tk.INSERT)
        
        # Check if we already have a selection
        try:
            sel_start = widget.index(tk.SEL_FIRST)
            sel_end = widget.index(tk.SEL_LAST)
            has_selection = True
        except tk.TclError:
            # No existing selection, start from cursor
            sel_start = current_pos
            sel_end = current_pos
            has_selection = False
        
        # Calculate new position based on direction and unit
        if direction == 'right':
            if unit == 'char':
                new_pos = widget.index(f"{sel_end} + 1 char")
            else:  # word
                new_pos = widget.index(f"{sel_end} + 1 word")
            # Extend from start to new position
            new_start = sel_start
            new_end = new_pos
        else:  # left
            if unit == 'char':
                new_pos = widget.index(f"{sel_start} - 1 char")
            else:  # word
                new_pos = widget.index(f"{sel_start} - 1 word wordstart")
            # Extend from new position to end
            new_start = new_pos
            new_end = sel_end if has_selection else current_pos
        
        # Don't go beyond text boundaries
        text_start = widget.index("1.0")
        text_end = widget.index("end-1c")
        
        # Clamp to boundaries
        if widget.compare(new_start, "<", text_start):
            new_start = text_start
        if widget.compare(new_end, ">", text_end):
            new_end = text_end
        
        # Apply the selection
        widget.tag_remove('sel', '1.0', tk.END)  # Clear default selection
        
        # Remove existing colored tag
        tag_name = f'dual_sel_{widget_type}'
        widget.tag_remove(tag_name, '1.0', tk.END)
        
        # Add new colored selection
        if widget.compare(new_start, "!=", new_end):
            widget.tag_add(tag_name, new_start, new_end)
            
            # Configure tag colors
            if widget_type == 'source':
                widget.tag_config(tag_name,
                                background='#B3E5FC',  # Light blue
                                foreground='#01579B')  # Dark blue
            else:  # target
                widget.tag_config(tag_name,
                                background='#C8E6C9',  # Light green
                                foreground='#1B5E20')  # Dark green
            
            widget.tag_raise(tag_name)
            
            # Update cursor position to end of selection
            widget.mark_set(tk.INSERT, new_end)
            
            # Show selection in status bar
            selected_text = widget.get(new_start, new_end)
            self.log(f"{widget_type.capitalize()} selection: '{selected_text}' ({len(selected_text)} chars)")
    
    except tk.TclError as e:
        # Handle edge cases silently
        pass
    
    return 'break'  # Prevent default behavior
```

### Step 4: Add Keyboard Bindings to Text Widgets

**Modify `create_grid_row` to add keyboard bindings:**

```python
# After creating source_text widget:

# Keyboard selection bindings for source
source_text.bind('<Control-Shift-Left>', 
                lambda e, w=source_text: self.extend_selection_keyboard(w, 'left', 'char', 'source'))
source_text.bind('<Control-Shift-Right>', 
                lambda e, w=source_text: self.extend_selection_keyboard(w, 'right', 'char', 'source'))
source_text.bind('<Control-Shift-Control-Left>', 
                lambda e, w=source_text: self.extend_selection_keyboard(w, 'left', 'word', 'source'))
source_text.bind('<Control-Shift-Control-Right>', 
                lambda e, w=source_text: self.extend_selection_keyboard(w, 'right', 'word', 'source'))
source_text.bind('<Tab>', lambda e: self.switch_dual_selection_focus())
source_text.bind('<Escape>', lambda e: self.clear_dual_selection())

# Similar bindings for target_text widget:

target_text.bind('<Control-Shift-Left>', 
                lambda e, w=target_text: self.extend_selection_keyboard(w, 'left', 'char', 'target'))
target_text.bind('<Control-Shift-Right>', 
                lambda e, w=target_text: self.extend_selection_keyboard(w, 'right', 'char', 'target'))
target_text.bind('<Control-Shift-Control-Left>', 
                lambda e, w=target_text: self.extend_selection_keyboard(w, 'left', 'word', 'target'))
target_text.bind('<Control-Shift-Control-Right>', 
                lambda e, w=target_text: self.extend_selection_keyboard(w, 'right', 'word', 'target'))
target_text.bind('<Tab>', lambda e: self.switch_dual_selection_focus())
target_text.bind('<Escape>', lambda e: self.clear_dual_selection())
```

---

## 🎹 Keyboard Shortcuts Summary

| Shortcut | Action |
|----------|--------|
| `Tab` | Switch focus between source and target |
| `Ctrl+Shift+→` | Extend selection right by 1 character |
| `Ctrl+Shift+←` | Extend selection left by 1 character |
| `Ctrl+Shift+Ctrl+→` | Extend selection right by 1 word |
| `Ctrl+Shift+Ctrl+←` | Extend selection left by 1 word |
| `Escape` | Clear all selections |

---

## ✅ Benefits

### For Power Users
- ✅ Hands stay on keyboard
- ✅ Faster than mouse
- ✅ Precise control
- ✅ Professional workflow

### Matches memoQ
- ✅ Same keyboard shortcuts
- ✅ Same behavior
- ✅ Familiar to memoQ users
- ✅ Professional standard

### Flexibility
- ✅ Mouse selection still works
- ✅ Keyboard selection works
- ✅ Choose your preferred method
- ✅ Best of both worlds

---

## 🧪 Testing Checklist

### Basic Keyboard Selection
- [ ] Tab switches focus between source/target
- [ ] Ctrl+Shift+Right extends selection right
- [ ] Ctrl+Shift+Left extends selection left
- [ ] Visual focus indicator appears
- [ ] Selection colors correct (blue/green)

### Word-Level Selection
- [ ] Ctrl+Shift+Ctrl+Right selects by word
- [ ] Ctrl+Shift+Ctrl+Left selects by word
- [ ] Word boundaries detected correctly

### Integration
- [ ] Mouse selection still works
- [ ] Keyboard and mouse work together
- [ ] Escape clears selections
- [ ] Tab doesn't interfere with editing

### Edge Cases
- [ ] Selection at start of text
- [ ] Selection at end of text
- [ ] Empty widgets
- [ ] Very long selections

---

**Status**: Ready to implement  
**Estimated Time**: 1-2 hours  
**Complexity**: Medium (keyboard event handling)
