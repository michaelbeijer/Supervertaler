# Pre-Translation Progress Dialog Enhancement

**Identified:** January 22, 2026  
**Status:** Ready for implementation  
**Complexity:** Medium (2-3 hours - threading + UI)  
**Priority:** HIGH (major UX improvement discovered during production use)

---

## 🐛 Current Problem: "Not Responding" Frozen Dialog

When running batch/pre-translation, the progress dialog:
- **Grays out** and shows "Not Responding"
- **Blocks all UI updates** (runs on main thread)
- **No visibility** into what's happening
- **Users can't tell** if it crashed or is working
- **Creates anxiety** during long translation jobs (200+ segments)

**Real-World Example:**
User translating 229-segment patent document, dialog frozen for ~5 minutes with no feedback.

---

## ✨ Proposed Solution: Live Console Output Dialog

Replace frozen progress bar with interactive console-style dialog showing real-time processing updates.

### Key Features

#### 1. Live Console Widget (QTextEdit, read-only, monospace)
- Real-time log of each segment as it processes
- Shows source text preview (first 50 chars)
- Shows provider, timing, success/error status
- Auto-scrolls to bottom
- Color-coded: ✓ Green for success, ✗ Red for errors

**Example Console Output:**
```
Starting batch translation: 229 segments
Provider: OpenAI GPT-4 Turbo | Model: gpt-4-turbo-preview
----------------------------------------
[1/229] Translating: "The present invention relates to a method for..." (0.8s) ✓
[2/229] Translating: "In the field of mechanical engineering, it is..." (0.9s) ✓
[3/229] Translating: "Prior art solutions have been unable to address..." (1.1s) ✓
[4/229] ERROR: Rate limit exceeded. Retrying in 20s... ⏳
[4/229] Translating: "Prior art solutions have been unable to address..." (1.0s) ✓
[5/229] Translating: "The inventive concept provides a novel approach..." (0.7s) ✓
...
```

#### 2. QThread Worker (non-blocking background processing)
- `PreTranslationWorker(QThread)` class
- Moves batch loop off main UI thread
- Emits signals for progress updates
- Dialog stays responsive throughout

#### 3. Detailed Progress Info
- Traditional progress bar (visual reference)
- Segment counter: "4/229 (2%)"
- Elapsed time timer (updates every second)
- Estimated time remaining (based on average speed)
- Current processing speed (segments/minute)

#### 4. User Control
- **Cancel** button (stops worker thread gracefully)
- **Minimize to Background** (optional feature)
- Dialog is draggable, resizable
- Can click elsewhere without interrupting

---

## 🏗️ Implementation Plan

### Step 1: Create PreTranslationWorker (QThread)

```python
from PyQt6.QtCore import QThread, pyqtSignal

class PreTranslationWorker(QThread):
    """Background worker thread for batch translation."""
    
    # Signals
    progress_update = pyqtSignal(int, int, str, bool)  # current, total, message, success
    translation_complete = pyqtSignal(int, int)  # success_count, error_count
    translation_error = pyqtSignal(str)  # error_message
    
    def __init__(self, parent_app, segments, provider_type, provider_name, model):
        super().__init__()
        self.parent_app = parent_app
        self.segments = segments
        self.provider_type = provider_type
        self.provider_name = provider_name
        self.model = model
        self._cancelled = False
    
    def run(self):
        """Main translation loop - runs in background thread."""
        success_count = 0
        error_count = 0
        
        for idx, segment in enumerate(self.segments):
            if self._cancelled:
                break
            
            try:
                # Get translation from provider
                start_time = time.time()
                translation = self._translate_segment(segment)
                elapsed = time.time() - start_time
                
                # Update segment in main data
                segment.target = translation
                segment.status = "Translated"
                
                # Emit progress (success)
                preview = segment.source[:50] + ("..." if len(segment.source) > 50 else "")
                message = f"[{idx+1}/{len(self.segments)}] Translating: \"{preview}\" ({elapsed:.1f}s) ✓"
                self.progress_update.emit(idx + 1, len(self.segments), message, True)
                
                success_count += 1
                
            except Exception as e:
                # Emit progress (error)
                message = f"[{idx+1}/{len(self.segments)}] ERROR: {str(e)} ✗"
                self.progress_update.emit(idx + 1, len(self.segments), message, False)
                error_count += 1
        
        # Emit completion
        self.translation_complete.emit(success_count, error_count)
    
    def cancel(self):
        """Request cancellation of translation job."""
        self._cancelled = True
    
    def _translate_segment(self, segment):
        """Translate a single segment using configured provider."""
        # Call existing translation logic from parent_app
        # This method will vary based on provider_type
        if self.provider_type == "LLM":
            client = self.parent_app._get_llm_client(self.provider_name)
            result = client.translate(
                text=segment.source,
                source_lang=self.parent_app.project.source_lang,
                target_lang=self.parent_app.project.target_lang,
                model=self.model
            )
            return result
        # ... similar for MT, TM providers
```

### Step 2: Create LiveProgressDialog

```python
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QProgressBar, QLabel, QTextEdit)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QTextCursor, QColor

class LiveProgressDialog(QDialog):
    """Progress dialog with live console output."""
    
    def __init__(self, parent, total_segments):
        super().__init__(parent)
        self.total_segments = total_segments
        self.start_time = time.time()
        self.segment_times = []  # Track processing times for estimation
        
        self.setWindowTitle("Batch Translation Progress")
        self.setMinimumSize(700, 500)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Progress info section
        info_layout = QHBoxLayout()
        self.progress_label = QLabel("0/0 (0%)")
        self.time_label = QLabel("Elapsed: 0:00 | Remaining: --:--")
        self.speed_label = QLabel("Speed: -- seg/min")
        info_layout.addWidget(self.progress_label)
        info_layout.addStretch()
        info_layout.addWidget(self.time_label)
        info_layout.addWidget(self.speed_label)
        layout.addLayout(info_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(total_segments)
        layout.addWidget(self.progress_bar)
        
        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 9))
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
            }
        """)
        layout.addWidget(self.console)
        
        # Button section
        button_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        # Timer for elapsed time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time_display)
        self.timer.start(1000)  # Update every second
    
    def add_console_line(self, message, is_success=True):
        """Add a line to the console with color coding."""
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Set text color
        fmt = cursor.charFormat()
        if is_success:
            fmt.setForeground(QColor("#4ec9b0"))  # Greenish (VS Code style)
        else:
            fmt.setForeground(QColor("#f48771"))  # Reddish (VS Code style)
        
        cursor.setCharFormat(fmt)
        cursor.insertText(message + "\n")
        
        # Auto-scroll to bottom
        self.console.setTextCursor(cursor)
        self.console.ensureCursorVisible()
    
    def update_progress(self, current, total, elapsed_seconds):
        """Update progress bar and labels."""
        self.progress_bar.setValue(current)
        
        # Update progress label
        percent = int((current / total) * 100)
        self.progress_label.setText(f"{current}/{total} ({percent}%)")
        
        # Track timing
        self.segment_times.append(elapsed_seconds)
        
        # Calculate speed and estimate remaining time
        if len(self.segment_times) > 0:
            avg_time = sum(self.segment_times) / len(self.segment_times)
            speed = 60 / avg_time if avg_time > 0 else 0
            remaining_segments = total - current
            remaining_seconds = remaining_segments * avg_time
            
            # Update labels
            self.speed_label.setText(f"Speed: {speed:.1f} seg/min")
            
            remaining_str = self._format_time(remaining_seconds)
            self.time_label.setText(
                f"Elapsed: {self._format_time(time.time() - self.start_time)} | "
                f"Remaining: {remaining_str}"
            )
    
    def _update_time_display(self):
        """Update elapsed time display (called every second)."""
        if self.progress_bar.value() < self.total_segments:
            elapsed = time.time() - self.start_time
            current_text = self.time_label.text()
            # Update only elapsed portion
            if " | " in current_text:
                remaining_part = current_text.split(" | ")[1]
                self.time_label.setText(
                    f"Elapsed: {self._format_time(elapsed)} | {remaining_part}"
                )
    
    @staticmethod
    def _format_time(seconds):
        """Format seconds as MM:SS."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def show_completion_message(self, success_count, error_count):
        """Show completion summary in console."""
        self.add_console_line("", True)  # Blank line
        self.add_console_line("=" * 50, True)
        self.add_console_line(f"Translation Complete!", True)
        self.add_console_line(f"✓ Success: {success_count}", True)
        if error_count > 0:
            self.add_console_line(f"✗ Errors: {error_count}", False)
        self.add_console_line("=" * 50, True)
        
        # Change button to "Close"
        self.cancel_btn.setText("Close")
```

### Step 3: Modify show_batch_translate_dialog()

In `Supervertaler.py`, update the batch translate method:

```python
def show_batch_translate_dialog(self):
    """Show batch translate dialog with live progress."""
    # ... existing dialog code to get settings ...
    
    # Create worker and dialog
    worker = PreTranslationWorker(
        self, segments_to_translate, 
        provider_type, provider_name, model
    )
    dialog = LiveProgressDialog(self, len(segments_to_translate))
    
    # Connect signals
    worker.progress_update.connect(
        lambda current, total, msg, success: self._handle_progress_update(
            dialog, current, total, msg, success
        )
    )
    worker.translation_complete.connect(
        lambda success, errors: self._handle_translation_complete(
            dialog, worker, success, errors
        )
    )
    
    # Connect cancel button
    dialog.rejected.connect(worker.cancel)
    
    # Add initial console messages
    dialog.add_console_line(f"Starting batch translation: {len(segments_to_translate)} segments")
    dialog.add_console_line(f"Provider: {provider_name} | Model: {model}")
    dialog.add_console_line("-" * 50)
    
    # Start worker and show dialog
    worker.start()
    dialog.exec()

def _handle_progress_update(self, dialog, current, total, message, success):
    """Handle progress update from worker thread."""
    dialog.add_console_line(message, success)
    # Extract elapsed time from message if needed, or track separately
    dialog.update_progress(current, total, 1.0)  # Use actual elapsed time

def _handle_translation_complete(self, dialog, worker, success_count, error_count):
    """Handle translation job completion."""
    dialog.show_completion_message(success_count, error_count)
    worker.wait()  # Wait for thread to fully terminate
    self.load_segments_to_grid()  # Refresh grid with new translations
```

---

## 📋 Testing Checklist

- [ ] Test with 5 segments (quick completion)
- [ ] Test with 50 segments (moderate duration)
- [ ] Test with 200+ segments (long duration - like user's 229-segment patent)
- [ ] Test cancel button (graceful shutdown)
- [ ] Test with API rate limit errors (should show retry in console)
- [ ] Test with network errors (should show red error messages)
- [ ] Test console auto-scroll (should stay at bottom)
- [ ] Test time estimation accuracy (should improve as job progresses)
- [ ] Test dialog resize (should maintain layout)
- [ ] Verify no UI freeze (dialog should remain responsive)
- [ ] Verify thread cleanup (no zombie threads after close)

---

## ✅ Benefits

- **Transparency** - See exactly which segment is processing
- **Confidence** - Know it's working, not frozen
- **Debugging** - See where and why failures occur
- **Professionalism** - Matches modern tools (VS Code extensions, npm install, pip install)
- **Responsiveness** - Can cancel or resize anytime
- **No anxiety** - Real-time feedback eliminates "is it crashed?" worry

---

## 📊 Estimated Implementation Time

**Total: 2-3 hours**
- PreTranslationWorker class: 45 min
- LiveProgressDialog class: 1 hour
- Integration in Supervertaler.py: 30 min
- Testing: 45 min

---

## 🎯 User Impact

**HIGH** - Eliminates major UX pain point discovered during production use. User reported frozen "Not Responding" dialog during 229-segment patent translation with no feedback for ~5 minutes.

---

## 🔗 Related Files

- `Supervertaler.py` - Main app, batch translate method
- `modules/llm_clients.py` - Translation providers
- No new dependencies required (uses PyQt6 QThread + QDialog)

---

**Implement tonight after user's patent translation job completes.**
