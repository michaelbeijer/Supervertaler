# Dual-Selection System - Implementation Guide

## What is Dual-Selection?

The dual-selection system allows users to:
1. Click on a segment in the grid
2. Use Tab to switch focus between source and target Text widgets
3. Use **Ctrl+Shift+Arrow keys** to select individual words/phrases in either source OR target
4. Once selections are made in both, press:
   - **Ctrl+G**: Add selected term pair to termbase
   - **Ctrl+Shift+T**: Add selected term pair to TM only

## Visual Feedback

- **Source focused**: Blue border (#2196F3) on source widget, dim target
- **Target focused**: Green border (#4CAF50) on target widget, dim source
- **Selected text**: Highlighted in light color while maintaining selection
- **Cursor position**: Remembered separately for source and target (Tab switches between them)

## Keyboard Bindings

| Key | Action |
|-----|--------|
| **Tab** | Switch focus between source and target |
| **Ctrl+Shift+Right** | Extend selection right by word |
| **Ctrl+Shift+Left** | Extend selection left by word |
| **Ctrl+Shift+Ctrl+Right** | Extend selection right by character |
| **Ctrl+Shift+Ctrl+Left** | Extend selection left by character |
| **Escape** | Clear all selections and exit selection mode |
| **Ctrl+G** | Add selected term pair to termbase |
| **Ctrl+Shift+T** | Add selected term pair to TM only |

## State Variables

```python
self.dual_selection_row = None                    # Currently active row
self.dual_selection_source = None                 # Source Text widget
self.dual_selection_target = None                 # Target Text widget
self.dual_selection_focused_widget = None         # 'source' or 'target'
self.dual_selection_source_cursor = None          # Cursor position in source
self.dual_selection_target_cursor = None          # Cursor position in target
```

## Flow Diagram

```
User clicks on segment
  ↓
Click handlers focus source/target
  ↓
User presses Tab to switch focus
  ↓
Source/target widgets enabled, cursor positioned, border shown
  ↓
User holds Ctrl+Shift and presses arrow keys
  ↓
Text selection grows/shrinks (word by word)
  ↓
User presses Ctrl+G or Ctrl+Shift+T
  ↓
Selected text extracted from both widgets
  ↓
Term pair added to termbase or TM
  ↓
Selection cleared
```

## Implementation Steps

1. Add state variables for dual-selection tracking
2. Add focus handlers on source/target widgets (click to enter selection mode)
3. Add keyboard bindings for Tab and arrow keys
4. Implement extend_selection_keyboard() for Ctrl+Shift+Arrow
5. Implement add_term_from_dual_selection() to extract and save term pairs
6. Implement clear_dual_selection() to reset state

## Qt Adaptation Notes

In PyQt6, the equivalent would be:
- Tkinter `Text` widget → PyQt6 `QPlainTextEdit`
- `tag_add()` / `tag_remove()` → `QTextCursor.setPosition()` and `QTextCharFormat`
- Tkinter keyboard bindings → `keyPressEvent()` override
- `mark_set()` / `index()` → `QTextCursor` operations
