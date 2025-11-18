# UI Responsiveness Optimization Plan

## Problem Statement

Users experience "Not Responding" freezes when:
- Typing in target cells
- Clicking to select different segments
- Scrolling through the grid
- Clicking in filter boxes

**Root Cause:** CPU/database-heavy lookups block the UI thread during user interaction.

---

## Current Optimization Systems

### 1. **Debouncing (Partial)**
- Target text changes debounced with 500ms delay
- Only applies to TM saving, not to lookups
- Cell selection lookups are NOT debounced

### 2. **Caching**
- Termbase matches cached per segment
- Prefetch worker thread for upcoming segments
- TM database uses FTS5 full-text search

### 3. **Row Guards**
- `_last_selected_row` prevents re-running lookups on same row
- Helps when editing text within a cell

---

## Proposed: User Activity Detection System

### **Core Concept**

**Pause ALL expensive operations when user touches keyboard/mouse.**

Resume operations only when:
1. User stops interacting for X ms (configurable, default 300ms)
2. Operation is critical (e.g., saving data)
3. User explicitly requests it (e.g., clicking "Search TM")

---

## Implementation Design

### **Phase 1: Activity Monitor**

```python
class UserActivityMonitor(QObject):
    """Detects user activity and signals when it's safe to run expensive operations"""
    
    activity_started = pyqtSignal()  # User started interacting
    activity_settled = pyqtSignal()  # User stopped for X ms
    
    def __init__(self, settle_delay_ms=300):
        super().__init__()
        self.settle_delay_ms = settle_delay_ms
        self.settle_timer = QTimer()
        self.settle_timer.setSingleShot(True)
        self.settle_timer.timeout.connect(self.activity_settled.emit)
        self.is_active = False
    
    def register_activity(self):
        """Called whenever user touches keyboard/mouse"""
        if not self.is_active:
            self.is_active = True
            self.activity_started.emit()
        
        # Reset settle timer
        self.settle_timer.stop()
        self.settle_timer.start(self.settle_delay_ms)
    
    def on_settled(self):
        """Called when activity timer expires"""
        self.is_active = False
```

### **Phase 2: Operation Queue with Priorities**

```python
class OperationQueue:
    """Manages expensive operations with priorities"""
    
    CRITICAL = 0    # Must run (e.g., saving user data)
    HIGH = 1        # Important (e.g., status updates)
    NORMAL = 2      # Standard (e.g., TM lookups on cell selection)
    LOW = 3         # Background (e.g., prefetch next segments)
    
    def __init__(self, activity_monitor):
        self.monitor = activity_monitor
        self.pending_operations = []
        self.paused = False
        
        # Connect to activity signals
        self.monitor.activity_started.connect(self.pause)
        self.monitor.activity_settled.connect(self.resume)
    
    def queue_operation(self, func, args, priority=NORMAL, cancelable=True):
        """Queue an operation with priority"""
        op = {
            'func': func,
            'args': args,
            'priority': priority,
            'cancelable': cancelable,
            'id': uuid.uuid4()
        }
        
        # CRITICAL operations run immediately even during activity
        if priority == self.CRITICAL:
            func(*args)
            return
        
        # Add to queue
        self.pending_operations.append(op)
        self.pending_operations.sort(key=lambda x: x['priority'])
        
        # Try to execute if not paused
        if not self.paused:
            self._execute_next()
    
    def pause(self):
        """Pause non-critical operations"""
        self.paused = True
        # Cancel any running cancelable operations
        # (This would need worker thread cooperation)
    
    def resume(self):
        """Resume operations after user settles"""
        self.paused = False
        self._execute_next()
    
    def _execute_next(self):
        """Execute next operation in queue"""
        if self.paused or not self.pending_operations:
            return
        
        op = self.pending_operations.pop(0)
        
        # Run in QTimer to avoid blocking
        QTimer.singleShot(0, lambda: op['func'](*op['args']))
        
        # Chain to next operation
        if self.pending_operations and not self.paused:
            QTimer.singleShot(10, self._execute_next)  # Small delay between ops
```

### **Phase 3: Install Event Filter**

```python
def install_activity_monitor(self):
    """Install global event filter to detect user activity"""
    self.activity_monitor = UserActivityMonitor(settle_delay_ms=300)
    self.operation_queue = OperationQueue(self.activity_monitor)
    
    # Install event filter on application
    app = QApplication.instance()
    app.installEventFilter(self)
    
def eventFilter(self, watched, event):
    """Global event filter to detect user activity"""
    # Detect keyboard/mouse activity
    if event.type() in [
        QEvent.Type.KeyPress,
        QEvent.Type.KeyRelease,
        QEvent.Type.MouseButtonPress,
        QEvent.Type.MouseButtonRelease,
        QEvent.Type.MouseMove,
        QEvent.Type.Wheel,
        QEvent.Type.TouchBegin,
        QEvent.Type.TouchUpdate
    ]:
        self.activity_monitor.register_activity()
    
    return super().eventFilter(watched, event)
```

### **Phase 4: Convert Expensive Operations**

```python
# OLD: Immediate execution
def on_cell_selected(self, current_row, current_col, previous_row, previous_col):
    segment = self.current_project.segments[current_row]
    self.highlight_source_with_termbase(current_row, segment.source, matches)
    self.update_translation_results(segment)
    self.prefetch_next_segments()

# NEW: Queued with priorities
def on_cell_selected(self, current_row, current_col, previous_row, previous_col):
    # Critical: Update UI immediately
    segment = self.current_project.segments[current_row]
    self.update_segment_info_toolbar(segment)  # Instant, lightweight
    
    # Normal priority: Lookup operations
    self.operation_queue.queue_operation(
        self.load_termbase_matches,
        args=(current_row, segment.source),
        priority=OperationQueue.NORMAL,
        cancelable=True
    )
    
    self.operation_queue.queue_operation(
        self.load_tm_matches,
        args=(current_row, segment.source),
        priority=OperationQueue.NORMAL,
        cancelable=True
    )
    
    # Low priority: Prefetch
    self.operation_queue.queue_operation(
        self.prefetch_next_segments,
        args=(current_row,),
        priority=OperationQueue.LOW,
        cancelable=True
    )
```

---

## Additional Optimizations

### **1. Reduce Database Writes**

**Problem:** Every keystroke writes to database (BEFORE/AFTER update logs)

**Solution:**
```python
# Only update segment object in memory, don't commit to DB
def on_target_text_changed():
    # Update in-memory segment
    segment.target = new_text
    self.project_modified = True  # Mark as dirty
    
    # Debounce database write (2 seconds)
    self.queue_db_save(segment, delay=2000)

def queue_db_save(self, segment, delay=2000):
    """Queue segment for DB save after delay"""
    if segment.id in self.pending_saves:
        self.pending_saves[segment.id].stop()
    
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(lambda: self.save_segment_to_db(segment))
    timer.start(delay)
    self.pending_saves[segment.id] = timer
```

### **2. Lazy Panel Updates**

**Problem:** Translation Results panel updates on every cell selection

**Solution:**
```python
# Only update if panel is visible
def update_translation_results(self, segment):
    if not self.results_panel.isVisible():
        self.pending_panel_update = segment
        return
    
    # Queue with normal priority
    self.operation_queue.queue_operation(
        self._do_update_translation_results,
        args=(segment,),
        priority=OperationQueue.NORMAL
    )
```

### **3. Incremental Highlighting**

**Problem:** Highlighting entire source cell with termbase matches is slow

**Solution:**
```python
# Break highlighting into chunks
def highlight_source_with_termbase_incremental(self, row, source, matches):
    """Highlight matches incrementally to avoid blocking"""
    chunks = self._split_highlighting_into_chunks(matches, chunk_size=5)
    
    for i, chunk in enumerate(chunks):
        delay = i * 50  # 50ms between chunks
        self.operation_queue.queue_operation(
            self._highlight_chunk,
            args=(row, source, chunk),
            priority=OperationQueue.LOW,
            cancelable=True
        )
```

### **4. Skip Same-Row Lookups (Already Implemented)**

✅ Already have `_last_selected_row` guard - good!

---

## Configuration Options

Add to Settings dialog:

```python
# Performance tab
responsiveness_group = QGroupBox("Responsiveness")

self.settle_delay_spin = QSpinBox()
self.settle_delay_spin.setRange(100, 1000)
self.settle_delay_spin.setValue(300)
self.settle_delay_spin.setSuffix(" ms")
QLabel("Pause expensive operations for:")
# When user types/clicks, wait this long before resuming lookups

self.enable_operation_queue = QCheckBox("Enable smart operation queuing")
self.enable_operation_queue.setChecked(True)
self.enable_operation_queue.setToolTip(
    "Automatically pause TM/termbase lookups when you're typing or clicking.\n"
    "Reduces 'Not Responding' freezes."
)

self.db_save_delay_spin = QSpinBox()
self.db_save_delay_spin.setRange(500, 5000)
self.db_save_delay_spin.setValue(2000)
self.db_save_delay_spin.setSuffix(" ms")
QLabel("Save to database after:")
# Debounce DB writes to reduce overhead
```

---

## Implementation Phases

### **Phase 1: Quick Wins (30 minutes)**
1. Increase debounce delay from 500ms to 1000ms for DB saves
2. Remove debug logging (`BEFORE update`, `AFTER update`, `textChanged FIRED`)
3. Add `isVisible()` check before updating Translation Results panel

### **Phase 2: Activity Monitor (2 hours)**
1. Implement `UserActivityMonitor` class
2. Install global event filter
3. Test with simple pause/resume of termbase lookups

### **Phase 3: Operation Queue (3 hours)**
1. Implement `OperationQueue` with priorities
2. Convert `on_cell_selected()` to use queue
3. Convert text change handlers to use queue

### **Phase 4: Advanced (4 hours)**
1. Worker thread cooperation for cancelable operations
2. Incremental highlighting
3. Settings UI for configuration

---

## Expected Results

| Scenario | Before | After |
|----------|--------|-------|
| Typing in target cell | Frequent freezes (200-500ms) | Smooth, no freezes |
| Clicking between cells | 1-2 second delay | Instant UI response, lookups delayed |
| Scrolling through grid | Stuttering | Smooth scrolling |
| Clicking filter box | Must wait for lookup | Instant focus |

---

## Risks & Mitigation

**Risk:** User closes file before DB saves complete  
**Mitigation:** Flush all pending saves on file close (CRITICAL priority)

**Risk:** Delayed lookups confuse user  
**Mitigation:** Show subtle loading indicator in Translation Results panel

**Risk:** Complexity increase  
**Mitigation:** Make it opt-in via settings, keep old behavior as fallback

---

## Testing Checklist

- [ ] Type rapidly in target cell - no freezes
- [ ] Click multiple cells quickly - UI stays responsive
- [ ] Close file immediately after editing - all changes saved
- [ ] Disable feature - reverts to old behavior
- [ ] Large files (5000+ segments) - still responsive
- [ ] TM/termbase lookups still work - just delayed

---

## Alternative: Simpler Approach

If full operation queue is too complex, start with:

1. **Increase all debounce delays** (500ms → 1500ms)
2. **Disable lookups during rapid clicking** (detect if cell changed in last 500ms)
3. **Move ALL lookups to worker threads** with result callbacks
4. **Remove debug logging** in production

This gives 70% of benefits with 20% of complexity.

---

## What the Log Shows

Your log excerpt shows:

```
[23:05:29] 🔔 textChanged FIRED: segment_id=265, new_text='a drawing of a machi...'
[23:05:29] 📝 BEFORE update: seg 263 target='collecting a sample...', status=translated
[23:05:29] 📝 AFTER update: seg 263 target='collecting a sample...', status=translated
```

This means:
- ✅ Text change handler is firing (good)
- ❌ It's logging on EVERY keystroke (bad for performance)
- ❌ Database operations happening on every change (should be debounced)
- ✅ Segment ID system working correctly

**Quick fix:** Remove these debug logs - they're slowing things down!

---

*Would you like me to implement Phase 1 (Quick Wins) right now?*
