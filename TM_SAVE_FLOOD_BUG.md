# Critical Bug: TM Save Flood During Grid Loading

## Problem Summary
Every time `load_segments_to_grid()` is called (startup, filtering, clear filters), all 219 segments trigger false TM database saves 1-2 seconds after grid load completes. This causes:
- 10+ second UI freeze
- Massive unnecessary database writes
- Poor user experience during filtering operations

## Symptoms
```
[18:16:43] ✓ Loaded 219 segments to grid
[18:16:44] 💾 Saved segment to 1 TM(s)  ← Starts 1 second after load
[18:16:45] 💾 Saved segment to 1 TM(s)
[18:16:45] 💾 Saved segment to 1 TM(s)
... (219 total saves over ~15 seconds)
```

## Root Cause
The `textChanged` signal on `EditableGridTextEditor` widgets (QTextEdit) is firing for ALL 219 segments shortly after `load_segments_to_grid()` completes, even though:
1. No user is editing
2. Text is set during construction with `blockSignals(True)`
3. There is a suppression flag `_suppress_target_change_handlers` set during loading

## Technical Details

### Signal Flow
1. `EditableGridTextEditor.__init__()` (line ~826)
   - Calls `blockSignals(True)`
   - Calls `setPlainText(text)` with segment text
   - Signals remain blocked (no `blockSignals(False)` in constructor)

2. Widget placed in table: `self.table.setCellWidget(row, 3, target_editor)` (line ~11678)

3. Signal handler connected: `target_editor.textChanged.connect(make_target_changed_handler(...))` (line ~11687)

4. **Signals unblocked in finally block** (line ~11720):
   ```python
   for row in range(self.table.rowCount()):
       target_widget = self.table.cellWidget(row, 3)
       if target_widget:
           target_widget.blockSignals(False)
   ```

5. **PROBLEM**: 1000ms after signals are unblocked, `textChanged` fires for all 219 widgets

### Signal Handler
When `textChanged` fires, it calls `on_target_text_changed()` (line ~11631):
```python
def on_target_text_changed():
    nonlocal debounce_timer
    new_text = editor_widget.toPlainText()
    
    if self._suppress_target_change_handlers:  # This is FALSE by this point!
        if self.debug_mode_enabled:
            self.log(f"🔔 textChanged SUPPRESSED for segment {segment_id}")
        return
    
    # ... updates segment.target ...
    
    # Creates NEW QTimer for each widget
    debounce_timer = QTimer()
    debounce_timer.setSingleShot(True)
    debounce_timer.timeout.connect(lambda text=new_text: 
        self._handle_target_text_debounced_by_id(segment_id, text))
    debounce_timer.start(1000)  # Fires 1000ms later
```

After 1000ms, `_handle_target_text_debounced_by_id()` (line ~12605) saves to TM:
```python
def _handle_target_text_debounced_by_id(self, segment_id, new_text):
    # ... find segment ...
    
    # Save to TM if segment is translated/approved/confirmed
    if segment.status in ['translated', 'approved', 'confirmed'] and new_text.strip():
        try:
            self.save_segment_to_activated_tms(segment.source, new_text)
        except Exception as e:
            self.log(f"Warning: Could not save to TM: {e}")
```

## Failed Solutions Attempted

### Attempt 1: Move signal connection after widget placement
**Result**: Failed - signals still fired

### Attempt 2: Block signals during setPlainText in constructor
**Code**:
```python
self.blockSignals(True)
self.setPlainText(text)
self.blockSignals(False)
```
**Result**: Failed - unblocking immediately allowed events to queue

### Attempt 3: Keep signals blocked until after handler connection
**Code**: Removed `blockSignals(False)` from constructor, only unblock after `connect()`
**Result**: Failed - signals still fired after unblock

### Attempt 4: Unblock signals in finally block after suppression restored
**Current code** (line ~11720):
```python
finally:
    self._suppress_target_change_handlers = previous_suppression
    
    # NOW unblock all target editor signals
    for row in range(self.table.rowCount()):
        target_widget = self.table.cellWidget(row, 3)
        if target_widget:
            target_widget.blockSignals(False)
```
**Result**: STILL FAILING - `textChanged` fires for all widgets ~1 second after unblock

## Key Questions / Mysteries

1. **Why does `textChanged` fire when signals are unblocked?**
   - The text was set during construction with signals blocked
   - No code modifies the text after unblocking
   - Is Qt queuing document change events internally that fire on unblock?

2. **Why doesn't the suppression flag help?**
   - `_suppress_target_change_handlers = True` during loading (line 11537)
   - Set back to `False` in finally block (line 11718)
   - By the time textChanged fires (1 second later), suppression is already off

3. **What triggers textChanged when signals are unblocked?**
   - No `setPlainText()` calls after construction
   - No user input
   - No focus changes
   - Widget is just sitting in the table

## Relevant Code Locations

### Supervertaler.py
- **Line 826-840**: `EditableGridTextEditor.__init__()` - Constructor with blockSignals
- **Line 11536-11537**: Set `_suppress_target_change_handlers = True` at start of load
- **Line 11621**: Create `EditableGridTextEditor` with segment text
- **Line 11625-11676**: `make_target_changed_handler()` factory function
- **Line 11631-11675**: `on_target_text_changed()` handler - creates debounce timer
- **Line 11678**: Place widget in table with `setCellWidget()`
- **Line 11687**: Connect signal with `textChanged.connect()`
- **Line 11716-11727**: Finally block - restore suppression, unblock all signals
- **Line 12605-12640**: `_handle_target_text_debounced_by_id()` - performs TM save

## Debugging Suggestions

1. **Add extensive logging to track signal emission**:
   ```python
   def on_target_text_changed():
       import traceback
       self.log(f"🔔 textChanged FIRED for segment {segment_id}")
       self.log(f"🔔 Suppression flag: {self._suppress_target_change_handlers}")
       self.log(f"🔔 Call stack: {''.join(traceback.format_stack()[-5:])}")
   ```

2. **Check if QTextEdit has pending document changes**:
   - Qt's QTextDocument might have internal change tracking
   - Try calling `document().clearUndoRedoStacks()` or similar

3. **Test if issue is specific to QTextEdit vs QPlainTextEdit**:
   - Switch widget type temporarily to isolate Qt behavior

4. **Verify if table operations trigger textChanged**:
   - `resizeRowToContents()` at line 11703
   - `apply_font_to_grid()` at line 11701
   - Try commenting these out temporarily

5. **Check if finally block execution order matters**:
   - Try unblocking signals BEFORE restoring suppression flag
   - Or add a flag that stays True until user actually edits

## Potential Solutions to Try

### Solution A: Never unblock signals programmatically
Keep signals blocked until user actually clicks into a cell. Override `focusInEvent()` to unblock:
```python
def focusInEvent(self, event):
    self.blockSignals(False)  # Unblock only when user focuses
    super().focusInEvent(event)
```

### Solution B: Track "initial load" state per widget
Add instance variable to track if widget has been "activated":
```python
class EditableGridTextEditor(QTextEdit):
    def __init__(self, ...):
        self._initial_load = True
        self.blockSignals(True)
        self.setPlainText(text)
        # Never unblock here

def on_target_text_changed():
    if hasattr(editor_widget, '_initial_load') and editor_widget._initial_load:
        editor_widget._initial_load = False
        return  # Ignore first textChanged after unblock
```

### Solution C: Use document modification tracking
Instead of textChanged, track `document().contentsChanged` with a modification counter:
```python
def __init__(self, ...):
    self._mod_count = self.document().revision()
    
def on_target_text_changed():
    new_mod = self.document().revision()
    if new_mod == self._mod_count + 1:  # Only one change since init
        return  # Ignore initial "change"
```

### Solution D: Delay unblocking signals
Instead of unblocking in finally block, use QTimer to delay:
```python
finally:
    self._suppress_target_change_handlers = previous_suppression
    # Don't unblock immediately - give Qt event loop time to settle
    QTimer.singleShot(100, self._unblock_all_target_signals)

def _unblock_all_target_signals(self):
    self._suppress_target_change_handlers = True  # Re-enable suppression
    for row in range(self.table.rowCount()):
        target_widget = self.table.cellWidget(row, 3)
        if target_widget:
            target_widget.blockSignals(False)
    # Keep suppression True until user actually edits something
```

## Test Case
1. Start program with project that has ~200 segments with status "translated" or "confirmed"
2. Observe log for "💾 Saved segment to 1 TM(s)" messages
3. Apply filter
4. Observe log again
5. Clear filter
6. Observe log again

**Expected**: Zero TM saves during grid operations
**Actual**: 219 TM saves every time grid is loaded

## Environment
- PyQt6
- Windows (PowerShell)
- Python 3.12
- Project: BRANTS (PACC-001-BE-WO) with 219 segments

## Priority
**CRITICAL** - This bug makes filtering unusable and causes unnecessary database writes that could corrupt data or cause performance issues on large projects.
