"""
Supervertaler Qt Edition
========================
The ultimate companion tool for translators and writers.
Modern PyQt6 interface with specialised modules to handle any problem.
Version: 1.8.0 (UI Refinements - Tab Styling)
Release Date: November 23, 2025
Framework: PyQt6

This is the modern edition of Supervertaler using PyQt6 framework.
For the classic tkinter edition, see Supervertaler_tkinter.py

Key Features:
- Complete Translation Matching: Termbase + TM + MT + Multi-LLM
- Project Termbases: Dedicated terminology per project with automatic extraction
- Supervoice: AI-powered voice dictation (100+ languages via OpenAI Whisper)
- Superimage: Extract images from DOCX files with preview
- Google Cloud Translation API integration
- Multi-LLM Support: OpenAI GPT, Claude, Google Gemini
- 2-Layer Prompt Architecture (System + Custom Prompts) with AI Assistant
- AI Assistant with conversational interface for document analysis
- Universal Lookup with global hotkey (Ctrl+Alt+L)
- Detachable Log window for multi-monitor setups
- Modern theme system (6 themes + custom editor)
- AutoFingers automation for memoQ with TagCleaner module
- memoQ bilingual DOCX import/export
- SQLite-based translation memory with FTS5 search
- Professional TMX editor

Author: Michael Beijer
License: MIT
"""

# Version Information.
__version__ = "1.8.0"
__phase__ = "0.8"
__release_date__ = "2025-11-23"
__edition__ = "Qt"

import sys
import json
import os
import subprocess
import atexit
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import threading
import time  # For delays in Universal Lookup
import re

# Fix encoding for Windows console (UTF-8 support)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# External dependencies
import pyperclip  # For clipboard operations in Universal Lookup
from modules.universal_lookup import UniversalLookupEngine  # Universal Lookup engine
from modules.voice_dictation_lite import QuickDictationThread  # Voice dictation
from modules.statuses import (
    STATUSES,
    DEFAULT_STATUS,
    StatusDefinition,
    get_status,
    match_memoq_status,
    compose_memoq_status,
)
from modules import file_dialog_helper as fdh  # File dialog helper with last directory memory


STATUS_ORDER = [
    "not_started",
    "pretranslated",
    "translated",
    "confirmed",
    "tr_confirmed",
    "proofread",
    "approved",
    "rejected",
]

STATUS_CYCLE = STATUS_ORDER

TRANSLATABLE_STATUSES = {"not_started", "pretranslated", "translated"}

# Check for PyQt6 and offer to install if missing
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTableWidget, QTableWidgetItem, QHeaderView, QMenuBar, QMenu,
        QFileDialog, QMessageBox, QToolBar, QLabel, QComboBox,
        QPushButton, QSpinBox, QSplitter, QTextEdit, QStatusBar,
        QStyledItemDelegate, QInputDialog, QDialog, QLineEdit, QRadioButton,
        QButtonGroup, QDialogButtonBox, QTabWidget, QGroupBox, QGridLayout, QCheckBox,
        QProgressBar, QFormLayout, QTabBar, QPlainTextEdit, QAbstractItemDelegate,
        QFrame, QListWidget, QListWidgetItem, QStackedWidget, QTreeWidget, QTreeWidgetItem,
        QScrollArea, QSizePolicy, QSlider, QToolButton
    )
    from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal, QObject, QUrl
    from PyQt6.QtGui import QFont, QAction, QKeySequence, QIcon, QTextOption, QColor, QDesktopServices, QTextCharFormat, QTextCursor, QBrush, QSyntaxHighlighter, QPalette
    from PyQt6.QtWidgets import QStyleOptionViewItem, QStyle
    from PyQt6.QtCore import QRectF
    from PyQt6 import sip
except ImportError:
    print("PyQt6 not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
    print("✓ PyQt6 installed. Please restart the application.")
    sys.exit(0)


# ============================================================================
# PRIVATE DATA PROTECTION SYSTEM
# ============================================================================

# Check for .supervertaler.local file to enable private features (for developers only)
# This ensures that private data (API keys, personal projects, etc.) stays in user_data_private/
# which is .gitignored, preventing accidental upload to GitHub
ENABLE_PRIVATE_FEATURES = os.path.exists(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".supervertaler.local")
)
if ENABLE_PRIVATE_FEATURES:
    print("[DEV MODE] Private features enabled (.supervertaler.local found)")
    print("[DEV MODE] Using 'user_data_private/' folder (git-ignored)")
else:
    print("[USER MODE] Using 'user_data/' folder")


# ============================================================================
# GLOBAL AHK PROCESS CLEANUP
# ============================================================================

# Global variable to track AHK process
_ahk_process = None

def cleanup_ahk_process():
    """Cleanup function to kill AHK process on exit"""
    global _ahk_process
    if _ahk_process:
        try:
            _ahk_process.terminate()
            _ahk_process.wait(timeout=1)
            print("[Universal Lookup] AHK process terminated on exit")
        except:
            try:
                _ahk_process.kill()
                print("[Universal Lookup] AHK process killed on exit")
            except:
                pass

# Register cleanup function to run on Python exit
atexit.register(cleanup_ahk_process)


# ============================================================================
# ENUMS
# ============================================================================

class LayoutMode:
    """Layout/view modes for the Project Editor"""
    GRID = "grid"       # Spreadsheet-like table (default)
    DOCUMENT = "document"  # Document flow view with clickable segments


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Segment:
    """Translation segment (matches tkinter version format)"""
    id: int
    source: str
    target: str = ""
    status: str = DEFAULT_STATUS.key
    type: str = "para"  # para, heading, list_item, table_cell
    notes: str = ""  # Stored as “Comments” in UI
    match_percent: Optional[int] = None  # memoQ match score if provided
    memoQ_status: str = ""  # Raw memoQ status text
    locked: bool = False  # For compatibility with tkinter version
    paragraph_id: int = 0  # Group segments by paragraph for document flow
    style: str = "Normal"  # Heading 1, Heading 2, Title, Subtitle, Normal, etc.
    document_position: int = 0  # Position in original document
    is_table_cell: bool = False  # Whether this segment is in a table
    table_info: Optional[tuple] = None  # (table_idx, row_idx, cell_idx) if is_table_cell
    modified: bool = False  # Track if segment has been edited
    created_at: str = ""  # Creation timestamp
    modified_at: str = ""  # Last modification timestamp
    
    def __post_init__(self):
        """Initialize timestamps if not provided"""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.modified_at:
            self.modified_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Segment':
        """Create Segment from dictionary, ignoring unknown fields"""
        # Only use fields that the dataclass knows about
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)


@dataclass
class Project:
    """Translation project"""
    name: str
    source_lang: str = "en"
    target_lang: str = "nl"
    segments: List[Segment] = None
    created: str = ""
    modified: str = ""
    prompt_settings: Dict[str, Any] = None  # Store active prompt settings
    tm_settings: Dict[str, Any] = None  # Store activated TM settings
    termbase_settings: Dict[str, Any] = None  # Store activated termbase settings
    id: int = None  # Unique project ID for TM activation tracking
    
    def __post_init__(self):
        if self.segments is None:
            self.segments = []
        if not self.created:
            self.created = datetime.now().isoformat()
        if not self.modified:
            self.modified = datetime.now().isoformat()
        if self.prompt_settings is None:
            self.prompt_settings = {}
        if self.tm_settings is None:
            self.tm_settings = {}
        if self.termbase_settings is None:
            self.termbase_settings = {}
        # Generate ID if not set (for backward compatibility with old projects)
        if self.id is None:
            import hashlib
            # Create stable ID from project name + created timestamp
            id_source = f"{self.name}_{self.created}"
            self.id = int(hashlib.md5(id_source.encode()).hexdigest()[:8], 16)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {
            'name': self.name,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
            'segments': [seg.to_dict() for seg in self.segments],
            'created': self.created,
            'modified': self.modified,
            'id': self.id  # Save project ID
        }
        # Add prompt settings if they exist
        if hasattr(self, 'prompt_settings'):
            result['prompt_settings'] = self.prompt_settings
        # Add TM settings if they exist
        if hasattr(self, 'tm_settings') and self.tm_settings:
            result['tm_settings'] = self.tm_settings
        # Add termbase settings if they exist
        if hasattr(self, 'termbase_settings') and self.termbase_settings:
            result['termbase_settings'] = self.termbase_settings
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create Project from dictionary"""
        segments = [Segment.from_dict(seg) for seg in data.get('segments', [])]
        
        # Handle missing name field (use filename or default)
        name = data.get('name', 'Untitled Project')
        
        project = cls(
            name=name,
            source_lang=data.get('source_lang', 'en'),
            target_lang=data.get('target_lang', 'nl'),
            segments=segments,
            created=data.get('created', ''),
            modified=data.get('modified', ''),
            id=data.get('id', None)  # Load project ID (will auto-generate if missing)
        )
        # Store prompt settings if they exist
        if 'prompt_settings' in data:
            project.prompt_settings = data['prompt_settings']
        # Store TM settings if they exist
        if 'tm_settings' in data:
            project.tm_settings = data['tm_settings']
        # Store termbase settings if they exist
        if 'termbase_settings' in data:
            project.termbase_settings = data['termbase_settings']
        return project


# ============================================================================
# CUSTOM DELEGATES AND EDITORS
# ============================================================================

class GridTableEventFilter:
    """Mixin to pass keyboard shortcuts from editor to table"""
    pass


class GridTextEditor(QTextEdit):
    """Custom QTextEdit for grid cells that passes special shortcuts to parent"""
    
    table_widget = None  # Will be set by delegate
    assistance_panel = None  # Will be set by delegate
    current_row = None  # Track which row this editor is in
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Prevent Tab from changing focus - we handle it manually
        self.setTabChangesFocus(False)
    
    def keyPressEvent(self, event):
        """Override keyPressEvent to handle Tab - this is called AFTER event()"""
        # Ctrl+Tab: Insert actual tab character
        if event.key() == Qt.Key.Key_Tab and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.insertPlainText('\t')
            event.accept()
            return
        
        # Tab (without Ctrl): Cycle to source cell
        if event.key() == Qt.Key.Key_Tab:
            if self.table_widget and self.current_row is not None:
                # Close current editor
                self.table_widget.closeEditor(self, QAbstractItemDelegate.EndEditHint.NoHint)
                # Open editor for source cell in same row (column 2)
                source_index = self.table_widget.model().index(self.current_row, 2)
                self.table_widget.setCurrentIndex(source_index)
                self.table_widget.edit(source_index)
                event.accept()
                return
        
        # Handle other Ctrl+ shortcuts
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Ctrl+1 through Ctrl+9: Insert match by number
            # TODO: Update to work with new results_panels system
            if event.key() >= Qt.Key.Key_1 and event.key() <= Qt.Key.Key_9:
                # Disabled for now - needs update to work with results_panels
                pass
            # Ctrl+Up/Down: Send to grid for grid navigation
            elif event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down):
                if self.table_widget:
                    self.table_widget.keyPressEvent(event)
                    event.accept()
                    return
            # Ctrl+Enter: Insert actual line break
            elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                super().keyPressEvent(event)
                event.accept()
                return
        
        # Shift+Enter: Insert line break (for multi-line content)
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                super().keyPressEvent(event)
                event.accept()
                return
        
        # Enter/Return: Don't insert, let delegate handle it (will close editor)
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            # Just ignore it - the table's default behavior will close the editor
            event.ignore()
            return
        
        # All other keys: Handle normally (including ESC for closing editor)
        print(f"🔑 GridTextEditor: Passing to super().keyPressEvent")
        super().keyPressEvent(event)


class ReadOnlyGridTextEditor(QTextEdit):
    """Read-only QTextEdit for source cells - allows easy text selection"""
    
    # Class variable for tag highlight color (shared across all instances)
    tag_highlight_color = '#FFB6C1'  # Default light pink
    
    table_widget = None  # Will be set by delegate
    current_row = None  # Track which row this editor is in
    allow_source_edit = False  # Will be set by delegate based on settings
    
    def __init__(self, text: str = "", parent=None, row: int = -1):
        super().__init__(parent)
        self.row = row  # Store row number for Tab cycling
        self.table_ref = parent  # Store table reference (parent is the table)
        self.setReadOnly(True)  # Prevent typing but allow selection
        self.setPlainText(text)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setAcceptRichText(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # CRITICAL: Enable keyboard focus and text selection
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # Enable text interaction: selection with keyboard and mouse
        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByKeyboard | 
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        
        # Make inactive selections stay visible with same color
        from PyQt6.QtGui import QPalette
        palette = self.palette()
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor("#D0E7FF"))
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, QColor("black"))
        palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor("#D0E7FF"))
        palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor("black"))
        self.setPalette(palette)
        
        # Style to look like a normal cell with subtle selection
        # IMPORTANT: Use light gray background instead of transparent to avoid text visibility issues
        self.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: #f5f5f5;
                padding: 0px;
                color: black;
            }
            QTextEdit:focus {
                border: 1px solid #2196F3;
                background-color: white;
                color: black;
            }
            QTextEdit::selection {
                background-color: #D0E7FF;
                color: black;
            }
        """)
        
        # Set document margins to 0 for compact display
        doc = self.document()
        doc.setDocumentMargin(0)
        
        # Configure text option for minimal line spacing
        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WrapMode.WordWrap)
        doc.setDefaultTextOption(text_option)
        
        # Set minimum height to 0 - let content determine size
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)  # Qt's max int
        
        # Store termbase matches for this cell (for tooltip and double-click)
        self.termbase_matches = {}
        
        # Enable mouse tracking for hover tooltips
        self.setMouseTracking(True)
        
        # Add syntax highlighter for tags
        self.highlighter = TagHighlighter(self.document(), self.tag_highlight_color)
    
    def highlight_termbase_matches(self, matches_dict: Dict):
        """
        Highlight termbase matches in the text using background colors based on priority.
        Does NOT change the widget - just adds background formatting to existing text.
        
        Args:
            matches_dict: Dictionary of {term: {'translation': str, 'priority': int}} or {term: str}
        """
        from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
        
        # Get the document and create a cursor
        doc = self.document()
        text = self.toPlainText()
        text_lower = text.lower()
        
        # IMPORTANT: Always clear all previous formatting first to prevent inconsistent highlighting
        cursor = QTextCursor(doc)
        cursor.select(QTextCursor.SelectionType.Document)
        default_fmt = QTextCharFormat()
        cursor.setCharFormat(default_fmt)
        
        # If no matches, we're done (highlighting has been cleared)
        if not matches_dict:
            return
        
        # Sort matches by source term length (longest first) to avoid partial matches
        # Since dict keys are now term_ids, we need to extract source terms first
        term_entries = []
        for term_id, match_info in matches_dict.items():
            if isinstance(match_info, dict):
                source_term = match_info.get('source', '')
                if source_term:
                    term_entries.append((source_term, term_id, match_info))
        
        # Sort by source term length (longest first)
        term_entries.sort(key=lambda x: len(x[0]), reverse=True)
        
        # Track positions we've already highlighted to avoid overlaps
        highlighted_ranges = []
        
        for term, term_id, match_info in term_entries:
            # Get ranking, forbidden status, and termbase type
            ranking = match_info.get('ranking', None)  # NEW: use ranking instead of priority
            forbidden = match_info.get('forbidden', False)
            is_project_termbase = match_info.get('is_project_termbase', False)
            
            # IMPORTANT: Treat ranking #1 as project termbase (even if flag not set)
            # This matches the logic in the termbase list UI
            is_effective_project = is_project_termbase or (ranking == 1)
            
            # Debug logging for color selection
            # (This will be printed once per term)
            if hasattr(self, 'parent') and hasattr(self.parent(), 'log'):
                parent = self.parent()
                while parent and not hasattr(parent, 'log'):
                    parent = parent.parent()
                if parent and hasattr(parent, 'log'):
                    parent.log(f"  🎨 Highlighting '{term}': is_project={is_project_termbase}, ranking={ranking}, effective_project={is_effective_project}, forbidden={forbidden}")
            
            # Color selection based on term status and ranking
            # All termbase matches use SOFT, PASTEL green shades (subtle background highlighting)
            # Lower ranking number = higher priority = slightly less pastel (but still soft)
            if forbidden:
                color = QColor(0, 0, 0)  # Black for forbidden terms
            else:
                # Use ranking to determine soft green shade
                # All shades are pastel/soft to stay in the background
                if ranking is not None:
                    # Map ranking to soft pastel green shades:
                    # Ranking #1: Soft medium green (still readable but subtle)
                    # Ranking #2: Soft light green
                    # Ranking #3: Very soft light green
                    # Ranking #4+: Extremely soft pastel green
                    if ranking == 1:
                        color = QColor(165, 214, 167)  # Soft medium green (Green 200)
                    elif ranking == 2:
                        color = QColor(200, 230, 201)  # Soft light green (Green 100)
                    elif ranking == 3:
                        color = QColor(220, 237, 200)  # Very soft light green (Light Green 100)
                    else:
                        color = QColor(232, 245, 233)  # Extremely soft pastel green (Green 50)
                else:
                    # No ranking (inactive termbase) - use soft light green
                    color = QColor(200, 230, 201)  # Green 100 (fallback)
            
            # Find all occurrences of this term (case-insensitive)
            term_lower = term.lower()
            start = 0
            while True:
                idx = text_lower.find(term_lower, start)
                if idx == -1:
                    break
                
                end_idx = idx + len(term)
                
                # Check if this range overlaps with already highlighted text
                overlaps = any(
                    (idx < h_end and end_idx > h_start)
                    for h_start, h_end in highlighted_ranges
                )
                
                if not overlaps:
                    # Create cursor for this position
                    cursor = QTextCursor(doc)
                    cursor.setPosition(idx)
                    cursor.setPosition(end_idx, QTextCursor.MoveMode.KeepAnchor)
                    
                    # Create format with background color
                    fmt = QTextCharFormat()
                    fmt.setBackground(color)
                    # Use black text for soft pastel backgrounds (better contrast and readability)
                    # Only use white text for dark forbidden terms
                    if forbidden:
                        fmt.setForeground(QColor("white"))
                    else:
                        fmt.setForeground(QColor("black"))
                    
                    # Apply format
                    cursor.setCharFormat(fmt)
                    
                    # Track this range as highlighted
                    highlighted_ranges.append((idx, end_idx))
                
                start = end_idx
    
    def event(self, event):
        """Override event() to catch Tab and Ctrl+T keys before Qt's default handling"""
        # Catch Tab key at event level (before keyPressEvent)
        if event.type() == event.Type.KeyPress:
            key_event = event
            
            # Ctrl+E: Add selected terms to termbase
            if key_event.key() == Qt.Key.Key_E and key_event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self._handle_add_to_termbase()
                return True  # Event handled
            
            if key_event.key() == Qt.Key.Key_Tab:
                # Ctrl+Tab: Insert actual tab character (if editing is allowed)
                if key_event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                    if self.allow_source_edit:
                        self.insertPlainText('\t')
                        return True  # Event handled
                
                # Tab alone: Cycle to target cell (column 3) in same row
                if key_event.modifiers() == Qt.KeyboardModifier.NoModifier:
                    if self.table_ref and self.row >= 0:
                        # Get target cell widget (column 3)
                        target_widget = self.table_ref.cellWidget(self.row, 3)
                        if target_widget:
                            target_widget.setFocus()
                            self.table_ref.setCurrentCell(self.row, 3)
                            return True  # Event handled, don't propagate
        
        # Let base class handle all other events
        return super().event(event)
    
    def keyPressEvent(self, event):
        """Override to handle other keys (Tab is handled in event())"""
        # All keys: Handle normally (Tab already handled in event())
        super().keyPressEvent(event)
    
    def sizeHint(self):
        """Return compact size based on content"""
        doc = self.document()
        ideal_width = self.width() if self.width() > 0 else 200
        doc.setTextWidth(ideal_width)
        height = int(doc.size().height())
        # Add minimal padding (2px total)
        height = max(height + 2, 1)
        current_width = self.width() if self.width() > 0 else 200
        return QSize(current_width, height)
    
    def _handle_add_to_termbase(self):
        """Handle Ctrl+T: Add selected source and target terms to termbase"""
        if not self.table_ref or self.row < 0:
            return
        
        # Get source selection (from this widget)
        source_text = self.textCursor().selectedText().strip()
        
        # Get target cell widget and its selection
        target_widget = self.table_ref.cellWidget(self.row, 3)
        target_text = ""
        if target_widget and hasattr(target_widget, 'textCursor'):
            target_text = target_widget.textCursor().selectedText().strip()
        
        # Validate we have both selections
        if not source_text or not target_text:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select text in both Source and Target cells before adding to termbase.\\n\\n"
                "Workflow:\\n"
                "1. Select term in source cell\\n"
                "2. Press Tab to cycle to target cell\\n"
                "3. Select corresponding translation\\n"
                "4. Press Ctrl+E (or right-click) to add to termbase"
            )
            return
        
        # Find main window and call add_to_termbase method
        main_window = self.table_ref.parent()
        while main_window and not hasattr(main_window, 'add_term_pair_to_termbase'):
            main_window = main_window.parent()
        
        if main_window and hasattr(main_window, 'add_term_pair_to_termbase'):
            main_window.add_term_pair_to_termbase(source_text, target_text)
    
    def mouseMoveEvent(self, event):
        """Show tooltip when hovering over highlighted termbase matches"""
        super().mouseMoveEvent(event)
        
        # Get cursor position
        cursor = self.cursorForPosition(event.pos())
        cursor_pos = cursor.position()
        
        # Check if cursor is over a termbase match
        for term_id, match_info in self.termbase_matches.items():
            # Extract source term from match_info
            term = match_info.get('source', '') if isinstance(match_info, dict) else str(term_id)
            # Find term position in text
            text = self.toPlainText()
            text_lower = text.lower()
            term_lower = term.lower()
            
            start = 0
            while True:
                idx = text_lower.find(term_lower, start)
                if idx == -1:
                    break
                
                end_idx = idx + len(term)
                
                # Check if cursor is within this term's range
                if idx <= cursor_pos <= end_idx:
                    # Get translation and other info
                    if isinstance(match_info, dict):
                        translation = match_info.get('translation', '')
                        priority = match_info.get('priority', 50)
                        forbidden = match_info.get('forbidden', False)
                        
                        # Build tooltip
                        tooltip = f"<b>{term}</b> → <b>{translation}</b>"
                        if forbidden:
                            tooltip += "<br><span style='color: red;'>⚠️ FORBIDDEN TERM</span>"
                        tooltip += f"<br><span style='color: #666;'>Priority: {priority}</span>"
                        tooltip += "<br><span style='color: #666;'><i>Double-click to insert</i></span>"
                    else:
                        tooltip = f"<b>{term}</b> → <b>{match_info}</b><br><span style='color: #666;'><i>Double-click to insert</i></span>"
                    
                    self.setToolTip(tooltip)
                    return
                
                start = end_idx
        
        # No match found at cursor position
        self.setToolTip("")
    
    def mouseDoubleClickEvent(self, event):
        """Insert termbase translation on double-click"""
        # Get cursor position
        cursor = self.cursorForPosition(event.pos())
        cursor_pos = cursor.position()
        
        # Check if double-clicked on a termbase match
        for term_id, match_info in self.termbase_matches.items():
            # Extract source term from match_info
            term = match_info.get('source', '') if isinstance(match_info, dict) else str(term_id)
            text = self.toPlainText()
            text_lower = text.lower()
            term_lower = term.lower()
            
            start = 0
            while True:
                idx = text_lower.find(term_lower, start)
                if idx == -1:
                    break
                
                end_idx = idx + len(term)
                
                # Check if cursor is within this term's range
                if idx <= cursor_pos <= end_idx:
                    # Get translation
                    if isinstance(match_info, dict):
                        translation = match_info.get('translation', '')
                    else:
                        translation = match_info
                    
                    # Insert translation into target cell at cursor position
                    if self.table_ref and self.row >= 0:
                        target_widget = self.table_ref.cellWidget(self.row, 3)
                        if target_widget and hasattr(target_widget, 'textCursor'):
                            # Insert at current cursor position in target
                            target_cursor = target_widget.textCursor()
                            target_cursor.insertText(translation)
                            target_widget.setFocus()
                    return
                
                start = end_idx
        
        # If not on a termbase match, allow normal double-click selection
        super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event):
        """Allow text selection on click and trigger row selection"""
        super().mousePressEvent(event)
        
        # Find the table and row number by checking which row this widget belongs to
        if self.parent():
            try:
                table = self.parent()
                # Find which row this widget is in
                for row in range(table.rowCount()):
                    if table.cellWidget(row, 2) == self:  # Source is column 2
                        table.selectRow(row)
                        table.setCurrentCell(row, 2)
                        
                        # CRITICAL: Manually trigger on_cell_selected since signals aren't firing
                        # Find the main window and call the method directly
                        main_window = table.parent()
                        while main_window and not hasattr(main_window, 'on_cell_selected'):
                            main_window = main_window.parent()
                        if main_window and hasattr(main_window, 'on_cell_selected'):
                            main_window.on_cell_selected(row, 2, -1, -1)
                        break
            except Exception as e:
                print(f"Error triggering manual cell selection: {e}")
    
    def focusInEvent(self, event):
        """Select text when focused for easy copying and trigger row selection"""
        super().focusInEvent(event)
        # Don't auto-select - let user select manually
        
        # Find the table and row number by checking which row this widget belongs to
        if self.parent():
            try:
                table = self.parent()
                # Find which row this widget is in
                for row in range(table.rowCount()):
                    if table.cellWidget(row, 2) == self:  # Source is column 2
                        table.selectRow(row)
                        table.setCurrentCell(row, 2)
                        
                        # CRITICAL: Manually trigger on_cell_selected since signals aren't firing
                        # Find the main window and call the method directly
                        main_window = table.parent()
                        while main_window and not hasattr(main_window, 'on_cell_selected'):
                            main_window = main_window.parent()
                        if main_window and hasattr(main_window, 'on_cell_selected'):
                            main_window.on_cell_selected(row, 2, -1, -1)
                        break
            except Exception as e:
                print(f"Error triggering manual cell selection: {e}")


class TagHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for HTML/XML tags in text editors"""
    
    def __init__(self, document, tag_color='#FFB6C1'):
        super().__init__(document)
        self.tag_color = tag_color
        self.update_tag_format()
    
    def update_tag_format(self):
        """Update the tag format with current color"""
        from PyQt6.QtGui import QTextCharFormat, QColor
        self.tag_format = QTextCharFormat()
        self.tag_format.setForeground(QColor(self.tag_color))
    
    def set_tag_color(self, color: str):
        """Update tag highlight color"""
        self.tag_color = color
        self.update_tag_format()
        self.rehighlight()
    
    def highlightBlock(self, text):
        """Highlight all tags in the text block"""
        import re
        # Match opening and closing tags: <tag>, </tag>, <tag/>
        tag_pattern = re.compile(r'</?[a-zA-Z][a-zA-Z0-9]*/?>')
        
        for match in tag_pattern.finditer(text):
            start = match.start()
            length = match.end() - start
            self.setFormat(start, length, self.tag_format)


class EditableGridTextEditor(QTextEdit):
    """Editable QTextEdit for target cells - allows text selection and editing"""
    
    # Class variable for tag highlight color (shared across all instances)
    tag_highlight_color = '#FFB6C1'  # Default light pink
    
    def __init__(self, text: str = "", parent=None, row: int = -1, table=None):
        super().__init__(parent)
        self.row = row  # Store row number for auto-selection
        self.table = table  # Store table reference
        self.setReadOnly(False)

        # CRITICAL: Track initial load state to ignore spurious textChanged events
        # Qt queues document change events during setPlainText() even with blockSignals(True).
        # When signals are unblocked later, Qt delivers these queued events, causing false
        # textChanged signals. This flag allows us to ignore the first event after unblocking.
        self._initial_load_complete = False

        # CRITICAL: Block ALL signals during initialization to prevent textChanged from firing
        # when setText is called. Signals will be unblocked AFTER signal handler is connected
        # in load_segments_to_grid. This prevents ANY textChanged events during grid loading.
        self.blockSignals(True)
        self.setPlainText(text)
        # DO NOT unblock signals here - they will be unblocked after handler connection
        
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setAcceptRichText(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # CRITICAL: Enable strong focus to receive Tab key events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Make inactive selections stay visible with same color
        from PyQt6.QtGui import QPalette
        palette = self.palette()
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor("#D0E7FF"))
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, QColor("black"))
        palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor("#D0E7FF"))
        palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor("black"))
        self.setPalette(palette)
        
        # Add syntax highlighter for tags
        self.highlighter = TagHighlighter(self.document(), self.tag_highlight_color)
        
        # Style to look like a normal cell with subtle selection
        # IMPORTANT: Use white background instead of transparent to avoid text visibility issues
        self.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: white;
                padding: 0px;
                color: black;
            }
            QTextEdit:focus {
                border: 1px solid #2196F3;
                background-color: white;
                color: black;
            }
            QTextEdit::selection {
                background-color: #D0E7FF;
                color: black;
            }
        """)
        
        # Set document margins to 0 for compact display
        doc = self.document()
        doc.setDocumentMargin(0)
        
        # Configure text option for minimal line spacing
        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WrapMode.WordWrap)
        doc.setDefaultTextOption(text_option)
        
        # Set minimum height to 0 - let content determine size
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)  # Qt's max int
    
    def _handle_add_to_termbase(self):
        """Handle Ctrl+T: Add selected source and target terms to termbase"""
        if not self.table or self.row < 0:
            return
        
        # Get target selection (from this widget)
        target_text = self.textCursor().selectedText().strip()
        
        # Get source cell widget and its selection
        source_widget = self.table.cellWidget(self.row, 2)
        source_text = ""
        if source_widget and hasattr(source_widget, 'textCursor'):
            source_text = source_widget.textCursor().selectedText().strip()
        
        # Validate we have both selections
        if not source_text or not target_text:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select text in both Source and Target cells before adding to termbase.\\n\\n"
                "Workflow:\\n"
                "1. Select term in source/target cell\\n"
                "2. Press Tab to cycle to other cell\\n"
                "3. Select corresponding term\\n"
                "4. Press Ctrl+E (or right-click) to add to termbase"
            )
            return
        
        # Find main window and call add_to_termbase method
        main_window = self.table.parent()
        while main_window and not hasattr(main_window, 'add_term_pair_to_termbase'):
            main_window = main_window.parent()
        
        if main_window and hasattr(main_window, 'add_term_pair_to_termbase'):
            main_window.add_term_pair_to_termbase(source_text, target_text)
    
    def contextMenuEvent(self, event):
        """Show context menu with Add to Termbase option"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction
        
        menu = QMenu(self)
        
        # Add standard edit actions
        if self.textCursor().hasSelection():
            copy_action = QAction("Copy", self)
            copy_action.triggered.connect(self.copy)
            menu.addAction(copy_action)
            
            cut_action = QAction("Cut", self)
            cut_action.triggered.connect(self.cut)
            menu.addAction(cut_action)
            menu.addSeparator()
        
        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.paste)
        menu.addAction(paste_action)
        menu.addSeparator()
        
        # Add to termbase action
        add_to_tb_action = QAction("Add to Termbase (Ctrl+E)", self)
        add_to_tb_action.triggered.connect(self._handle_add_to_termbase)
        menu.addAction(add_to_tb_action)
        
        menu.exec(event.globalPos())
    
    def sizeHint(self):
        """Return compact size based on content"""
        doc = self.document()
        ideal_width = self.width() if self.width() > 0 else 200
        doc.setTextWidth(ideal_width)
        height = int(doc.size().height())
        # Add minimal padding (2px total)
        height = max(height + 2, 1)
        current_width = self.width() if self.width() > 0 else 200
        return QSize(current_width, height)
    
    def mousePressEvent(self, event):
        """Allow text selection on click and auto-select row"""
        super().mousePressEvent(event)
        # Auto-select the row when clicking in the target cell
        if self.table and self.row >= 0:
            self.table.selectRow(self.row)
            self.table.setCurrentCell(self.row, 3)  # Column 3 is Target
            
            # CRITICAL: Manually trigger on_cell_selected since signals aren't firing
            # Find the main window and call the method directly
            try:
                main_window = self.table.parent()
                while main_window and not hasattr(main_window, 'on_cell_selected'):
                    main_window = main_window.parent()
                if main_window and hasattr(main_window, 'on_cell_selected'):
                    main_window.on_cell_selected(self.row, 3, -1, -1)
            except Exception as e:
                print(f"Error triggering manual cell selection: {e}")
    
    def focusInEvent(self, event):
        """Ensure text remains visible when focused and auto-select row"""
        super().focusInEvent(event)
        # Ensure the widget is properly visible
        self.setVisible(True)
        self.show()
        # Auto-select the row when focusing the target cell
        if self.table and self.row >= 0:
            self.table.selectRow(self.row)
            self.table.setCurrentCell(self.row, 3)  # Column 3 is Target
            
            # CRITICAL: Manually trigger on_cell_selected since signals aren't firing
            # Find the main window and call the method directly
            try:
                main_window = self.table.parent()
                while main_window and not hasattr(main_window, 'on_cell_selected'):
                    main_window = main_window.parent()
                if main_window and hasattr(main_window, 'on_cell_selected'):
                    main_window.on_cell_selected(self.row, 3, -1, -1)
            except Exception as e:
                print(f"Error triggering manual cell selection: {e}")
    
    def keyPressEvent(self, event):
        """Handle Tab and Ctrl+E keys to cycle between source and target cells"""
        # Ctrl+E: Add selected terms to termbase
        if event.key() == Qt.Key.Key_E and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._handle_add_to_termbase()
            event.accept()
            return
        
        # Ctrl+Tab: Insert actual tab character
        if event.key() == Qt.Key.Key_Tab and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.insertPlainText('\t')
            event.accept()
            return
        
        # Tab alone: Cycle to source cell (column 2) in same row
        if event.key() == Qt.Key.Key_Tab and event.modifiers() == Qt.KeyboardModifier.NoModifier:
            if self.table and self.row >= 0:
                # Get source cell widget (column 2)
                source_widget = self.table.cellWidget(self.row, 2)
                if source_widget:
                    source_widget.setFocus()
                    self.table.setCurrentCell(self.row, 2)
                    event.accept()
                    return
        
        # All other keys: Handle normally
        super().keyPressEvent(event)


class SearchHighlightDelegate(QStyledItemDelegate):
    """
    Custom delegate that highlights search terms in cells while preserving full editability.
    Uses custom painting to draw highlights underneath the text.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_terms = {}  # Dict of {(row, col): search_term}
        self.highlight_color = QColor(255, 255, 0, 180)  # Yellow with some transparency

    def set_highlight(self, row: int, col: int, search_term: str):
        """Set a search term to highlight for a specific cell"""
        self.search_terms[(row, col)] = search_term

    def clear_highlight(self, row: int, col: int):
        """Clear highlight for a specific cell"""
        if (row, col) in self.search_terms:
            del self.search_terms[(row, col)]

    def clear_all_highlights(self):
        """Clear all highlights"""
        self.search_terms.clear()

    def paint(self, painter, option, index):
        """Custom paint method that highlights search terms"""
        row = index.row()
        col = index.column()

        # Check if this cell has a search term to highlight
        if (row, col) in self.search_terms:
            search_term = self.search_terms[(row, col)]
            text = index.data(Qt.ItemDataRole.DisplayRole) or ""

            if text and search_term:
                # Save painter state
                painter.save()

                # Draw the background first (handles selection, etc.)
                option_copy = QStyleOptionViewItem(option)
                self.initStyleOption(option_copy, index)

                # Get the style
                style = option.widget.style() if option.widget else QApplication.style()

                # Draw background
                style.drawPrimitive(QStyle.PrimitiveElement.PE_PanelItemViewItem, option_copy, painter, option.widget)

                # Calculate text rect
                text_rect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, option_copy, option.widget)

                # Get font metrics
                fm = painter.fontMetrics()

                # Find and highlight all occurrences of the search term
                text_lower = text.lower()
                search_lower = search_term.lower()
                pos = 0

                while True:
                    found = text_lower.find(search_lower, pos)
                    if found == -1:
                        break

                    # Calculate the position of this occurrence
                    prefix = text[:found]
                    prefix_width = fm.horizontalAdvance(prefix)
                    term_width = fm.horizontalAdvance(text[found:found + len(search_term)])

                    # Draw highlight rectangle
                    highlight_rect = QRectF(
                        text_rect.left() + prefix_width,
                        text_rect.top(),
                        term_width,
                        text_rect.height()
                    )
                    painter.fillRect(highlight_rect, self.highlight_color)

                    pos = found + len(search_term)

                # Draw the text on top
                painter.setPen(option_copy.palette.color(QPalette.ColorRole.Text))
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)

                painter.restore()
                return

        # Default painting for non-highlighted cells
        super().paint(painter, option, index)


class ClickableHighlightLabel(QLabel):
    """
    Custom QLabel for highlighted search results that allows double-click to edit.
    When double-clicked, it removes itself from the table cell and triggers editing.

    Mouse events are transparent by default - the table's viewport handles them.
    We use installEventFilter on the table's viewport to catch double-clicks.
    """

    def __init__(self, table, row: int, col: int, plain_text: str, parent=None):
        super().__init__(parent)
        self.table = table
        self.row = row
        self.col = col
        self.plain_text = plain_text  # Store the original plain text for restoration
        # Make mouse events pass through to the table underneath
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)


class TermbaseHighlightWidget(QLabel):
    """Custom label widget that displays source text with termbase highlights and tooltips"""
    
    # Signal for term double-click
    term_double_clicked = None
    
    def __init__(self, source_text: str, termbase_matches: Optional[Dict[str, str]] = None, parent=None):
        """
        Args:
            source_text: The full source text to display
            termbase_matches: Dict of {term: translation} for highlighted terms
            parent: Parent widget
        """
        super().__init__(parent)
        self.source_text = source_text
        self.termbase_matches = termbase_matches if termbase_matches is not None else {}
        self.term_ranges = {}  # Store {term: (start_pos, end_pos)}
        self.setWordWrap(True)
        self.setup_display()
        self.setMouseTracking(True)
    
    def setup_display(self):
        """Create rich text display with highlighted terms"""
        html = self._create_highlighted_html()
        self.setText(html)
        self.setTextFormat(Qt.TextFormat.RichText)
    
    def _create_highlighted_html(self) -> str:
        """Create HTML with highlighted termbase matches using priority colors"""
        text = self.source_text
        
        # Sort matches by source term length (longest first) to avoid overlaps
        # Since dict keys are now term_ids, extract source terms first
        term_entries = []
        for term_id, match_info in self.termbase_matches.items():
            if isinstance(match_info, dict):
                source_term = match_info.get('source', '')
                if source_term:
                    term_entries.append((source_term, match_info))
        
        term_entries.sort(key=lambda x: len(x[0]), reverse=True)
        
        # Build HTML with highlights
        html = text
        offset = 0
        
        for term, match_info in term_entries:
            # Case-insensitive search
            search_term = term.lower()
            search_html = html.lower()
            
            # Get priority-based color (if termbase_matches contains priority info)
            if isinstance(match_info, dict) and 'priority' in match_info:
                priority = match_info.get('priority', 50)
                translation = match_info.get('translation', '')
            else:
                # Backward compatibility: if just string, use default priority
                priority = 50
                translation = match_info if isinstance(match_info, str) else ''
            
            # Calculate color based on priority (1-99, higher = darker blue)
            # Priority 99 = darkest (#0066CC), Priority 1 = lightest (#99CCFF)
            darkness = int(255 - (priority * 1.5))  # Higher priority = lower RGB value = darker
            darkness = max(0, min(darkness, 200))  # Clamp between 0-200
            color = f"rgb(0, {darkness}, 255)"
            
            # Find all occurrences
            start = 0
            while True:
                idx = search_html.find(search_term, start)
                if idx == -1:
                    break
                
                # Extract original casing
                original_term = html[idx:idx + len(term)]
                
                # Replace with highlighted version using priority color
                highlighted = f'<span style="background-color: {color}; color: white; padding: 1px 3px; border-radius: 2px; font-weight: bold; cursor: pointer;" class="termbase-match" data-term="{term}" title="{translation} (Priority: {priority})">{original_term}</span>'
                
                html = html[:idx] + highlighted + html[idx + len(term):]
                search_html = html.lower()
                
                start = idx + len(highlighted)
        
        return html
    
    def mouseMoveEvent(self, ev):
        """Show tooltip when hovering over highlighted terms"""
        # Find if cursor is over a highlighted term using text format
        # This is a simplified approach - shows generic tooltip
        super().mouseMoveEvent(ev)
    
    def mouseDoubleClickEvent(self, ev):
        """Handle double-click on highlighted terms"""
        # Find which term was clicked by getting the word at the position
        # Since QLabel doesn't provide cursor position easily, we look at the click
        # and try to extract the clicked word from the text
        
        # Get position in text (approximate)
        pos = ev.pos()
        
        # Try to find which term is near the click point
        # This is a simplified approach - in production would need better handling
        for term_id, match_info in self.termbase_matches.items():
            term = match_info.get('source', '') if isinstance(match_info, dict) else str(term_id)
            translation = match_info.get('translation', match_info) if isinstance(match_info, dict) else match_info
            # Check if this term contains the click area (very approximate)
            if self.term_double_clicked is not None and callable(self.term_double_clicked):
                # For now, if we get a double-click and there are matches,
                # this is a signal to insert the first/only match
                # Better implementation would need proper hit detection
                pass
        
        super().mouseDoubleClickEvent(ev)


class WordWrapDelegate(QStyledItemDelegate):
    """Custom delegate to enable word wrap when editing cells, with search term highlighting"""

    def __init__(self, assistance_panel=None, table_widget=None, allow_source_edit=False):
        super().__init__()
        self.assistance_panel = assistance_panel
        self.table_widget = table_widget
        self.allow_source_edit = allow_source_edit  # Controls whether source can be edited
        self.search_terms = {}  # Dict of {(row, col): search_term} for highlighting
        self.highlight_color = QColor(255, 255, 0, 180)  # Yellow with some transparency

    def set_highlight(self, row: int, col: int, search_term: str):
        """Set a search term to highlight for a specific cell"""
        self.search_terms[(row, col)] = search_term

    def clear_highlight(self, row: int, col: int):
        """Clear highlight for a specific cell"""
        if (row, col) in self.search_terms:
            del self.search_terms[(row, col)]

    def clear_all_highlights(self):
        """Clear all highlights"""
        self.search_terms.clear()

    def paint(self, painter, option, index):
        """Custom paint method that highlights search terms while keeping cells editable.

        Uses QTextDocument with HTML for reliable cross-line highlighting.
        Instead of storing per-cell terms, we store a global search term and check
        if the cell's text contains it.
        """
        row = index.row()
        col = index.column()

        # Check if this cell has a search term to highlight
        # Use global search term if set, otherwise check per-cell dict
        search_term = None
        if col == 3 and hasattr(self, 'global_search_term') and self.global_search_term:
            # For target column, use global search term
            search_term = self.global_search_term
        elif col == 2 and hasattr(self, 'global_source_search_term') and self.global_source_search_term:
            # For source column, use global source search term
            search_term = self.global_source_search_term
        elif (row, col) in self.search_terms:
            search_term = self.search_terms[(row, col)]

        # Debug: Log once per column 3 cell when global_search_term is set
        if col == 3 and hasattr(self, 'global_search_term') and self.global_search_term and row == 0:
            print(f"[PAINT DEBUG] Row 0, Col 3: global_search_term='{self.global_search_term}', search_term='{search_term}'")

        if search_term:
            text = index.data(Qt.ItemDataRole.DisplayRole) or ""

            # Only highlight if the search term is actually in the text
            if text and search_term.lower() in text.lower():
                from PyQt6.QtGui import QColor, QTextDocument, QAbstractTextDocumentLayout, QPalette
                from PyQt6.QtCore import QRectF, QSizeF
                import html as html_module

                # Get style and text rect
                option_copy = QStyleOptionViewItem(option)
                self.initStyleOption(option_copy, index)
                style = option.widget.style() if option.widget else QApplication.style()

                # Draw background first (handles selection state etc.)
                style.drawPrimitive(QStyle.PrimitiveElement.PE_PanelItemViewItem, option_copy, painter, option.widget)

                # Get the text rectangle
                text_rect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, option_copy, option.widget)

                # Add small padding like default delegate
                text_rect = text_rect.adjusted(3, 0, -3, 0)

                # Create HTML with highlighted search terms
                # Escape HTML special characters first
                escaped_text = html_module.escape(text)
                escaped_term = html_module.escape(search_term)

                # Case-insensitive replacement with highlighting
                import re
                pattern = re.compile(re.escape(escaped_term), re.IGNORECASE)

                def replace_with_highlight(match):
                    return f'<span style="background-color: #FFFF00;">{match.group(0)}</span>'

                html_text = pattern.sub(replace_with_highlight, escaped_text)

                # Create QTextDocument with the highlighted HTML
                doc = QTextDocument()
                doc.setDefaultFont(option.font)
                doc.setTextWidth(text_rect.width())
                doc.setHtml(html_text)

                painter.save()
                painter.translate(text_rect.topLeft())

                # Clip to text rect
                painter.setClipRect(QRectF(0, 0, text_rect.width(), text_rect.height()))

                # Draw the document
                doc.drawContents(painter)

                painter.restore()
                return

        # Default painting for non-highlighted cells
        super().paint(painter, option, index)
    
    def createEditor(self, parent, option, index):
        """Create a QTextEdit for multi-line editing with word wrap"""
        # Target column (column 3) - always editable
        if index.column() == 3:
            editor = GridTextEditor(parent)
            editor.assistance_panel = self.assistance_panel
            editor.table_widget = self.table_widget
            editor.current_row = index.row()
            editor.setWordWrapMode(QTextOption.WrapMode.WordWrap)
            editor.setAcceptRichText(False)  # Plain text only
            editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            
            # Ensure the row is tall enough for editing
            table = parent.parent()
            if hasattr(table, 'resizeRowToContents'):
                # Schedule row resize after editor is shown
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(0, lambda: table.resizeRowToContents(index.row()))
            
            return editor
        
        # Source column (column 2) - editable for selection/dual selection, optionally editable for content
        elif index.column() == 2:
            editor = ReadOnlyGridTextEditor("", parent)
            editor.table_widget = self.table_widget
            editor.current_row = index.row()
            editor.allow_source_edit = self.allow_source_edit
            
            # If allow_source_edit is True, make it actually editable (with warning color)
            if self.allow_source_edit:
                editor.setReadOnly(False)
                editor.setStyleSheet("""
                    QTextEdit {
                        border: none;
                        background-color: #FFF9E6;
                        padding: 0px;
                        color: black;
                    }
                    QTextEdit:focus {
                        border: 1px solid #FF9800;
                        background-color: #FFFACD;
                        color: black;
                    }
                    QTextEdit::selection {
                        background-color: #D0E7FF;
                        color: black;
                    }
                """)
            
            # Ensure the row is tall enough for editing
            table = parent.parent()
            if hasattr(table, 'resizeRowToContents'):
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(0, lambda: table.resizeRowToContents(index.row()))
            
            return editor
        else:
            return super().createEditor(parent, option, index)
    
    def setEditorData(self, editor, index):
        """Load data into the editor"""
        if isinstance(editor, (QTextEdit, ReadOnlyGridTextEditor)):
            text = index.model().data(index, Qt.ItemDataRole.EditRole)
            editor.setPlainText(text or "")
            # Ensure cursor is at start
            cursor = editor.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            editor.setTextCursor(cursor)
        else:
            super().setEditorData(editor, index)
    
    def setModelData(self, editor, model, index):
        """Save data from editor back to model"""
        if isinstance(editor, ReadOnlyGridTextEditor):
            # Only save if editing is allowed
            if editor.allow_source_edit:
                text = editor.toPlainText()
                model.setData(index, text, Qt.ItemDataRole.EditRole)
            # Otherwise, just close without saving (was for selection only)
        elif isinstance(editor, QTextEdit):
            text = editor.toPlainText()
            model.setData(index, text, Qt.ItemDataRole.EditRole)
        else:
            super().setModelData(editor, model, index)
    
    def updateEditorGeometry(self, editor, option, index):
        """Set the editor geometry to match the cell size"""
        if isinstance(editor, (QTextEdit, ReadOnlyGridTextEditor)):
            # Make the editor fill the cell properly with some padding
            rect = option.rect
            editor.setGeometry(rect)
        else:
            super().updateEditorGeometry(editor, option, index)


# ============================================================================
# THEME EDITOR DIALOG
# ============================================================================

class ThemeEditorDialog(QDialog):
    """Dialog for editing and managing themes"""
    
    def __init__(self, parent, theme_manager):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setWindowTitle("Theme Editor")
        self.setModal(True)
        self.resize(700, 600)
        
        self.setup_ui()
        self.load_themes()
    
    def setup_ui(self):
        """Create the UI"""
        layout = QVBoxLayout(self)
        
        # Theme selection
        theme_group = QGroupBox("Select Theme")
        theme_layout = QHBoxLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.currentTextChanged.connect(self.on_theme_selected)
        theme_layout.addWidget(QLabel("Theme:"))
        theme_layout.addWidget(self.theme_combo, 1)
        
        self.apply_btn = QPushButton("✓ Apply")
        self.apply_btn.clicked.connect(self.apply_theme)
        theme_layout.addWidget(self.apply_btn)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Color customization
        colors_group = QGroupBox("Customize Colors")
        colors_layout = QGridLayout()
        
        # Create color pickers for main colors
        self.color_buttons = {}
        color_configs = [
            ("window_bg", "Window Background", 0, 0),
            ("base", "Input Fields", 0, 1),
            ("button", "Buttons", 0, 2),
            ("text", "Text", 1, 0),
            ("highlight", "Highlight", 1, 1),
            ("border", "Borders", 1, 2),
            ("grid_header", "Table Headers", 2, 0),
            ("alternate_bg", "Alternate Rows", 2, 1),
            ("tm_exact", "100% TM Match", 3, 0),
            ("tm_high", "95-99% TM Match", 3, 1),
        ]
        
        for attr, label, row, col in color_configs:
            lbl = QLabel(label + ":")
            btn = QPushButton()
            btn.setMinimumHeight(30)
            btn.setProperty("color_attr", attr)
            btn.clicked.connect(lambda checked, a=attr: self.pick_color(a))
            self.color_buttons[attr] = btn
            
            colors_layout.addWidget(lbl, row * 2, col)
            colors_layout.addWidget(btn, row * 2 + 1, col)
        
        colors_group.setLayout(colors_layout)
        layout.addWidget(colors_group)
        
        # Custom theme actions
        custom_group = QGroupBox("Custom Themes")
        custom_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save as Custom Theme")
        save_btn.clicked.connect(self.save_custom_theme)
        custom_layout.addWidget(save_btn)
        
        delete_btn = QPushButton("🗑️ Delete Custom Theme")
        delete_btn.clicked.connect(self.delete_custom_theme)
        custom_layout.addWidget(delete_btn)
        
        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)
        
        # Preview area
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout()
        
        preview_text = QLabel("This is how text will look in the selected theme.")
        preview_layout.addWidget(preview_text)
        
        preview_table = QTableWidget(3, 2)
        preview_table.setHorizontalHeaderLabels(["Source", "Target"])
        preview_table.setItem(0, 0, QTableWidgetItem("Sample text"))
        preview_table.setItem(0, 1, QTableWidgetItem("Voorbeeldtekst"))
        preview_layout.addWidget(preview_table)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_themes(self):
        """Load available themes into combo box"""
        self.theme_combo.clear()
        themes = self.theme_manager.get_all_themes()
        for theme_name in themes.keys():
            self.theme_combo.addItem(theme_name)
        
        # Select current theme
        current_idx = self.theme_combo.findText(self.theme_manager.current_theme.name)
        if current_idx >= 0:
            self.theme_combo.setCurrentIndex(current_idx)
    
    def on_theme_selected(self, theme_name):
        """When theme is selected from combo box"""
        if not theme_name:
            return
        
        theme = self.theme_manager.get_theme(theme_name)
        if theme:
            self.update_color_buttons(theme)
    
    def update_color_buttons(self, theme):
        """Update color button backgrounds"""
        for attr, btn in self.color_buttons.items():
            color = getattr(theme, attr, "#FFFFFF")
            btn.setStyleSheet(f"background-color: {color}; border: 1px solid #999;")
            btn.setText(color)
    
    def pick_color(self, attr):
        """Open color picker for an attribute"""
        from PyQt6.QtWidgets import QColorDialog
        
        theme_name = self.theme_combo.currentText()
        theme = self.theme_manager.get_theme(theme_name)
        
        if not theme:
            return
        
        current_color = QColor(getattr(theme, attr))
        color = QColorDialog.getColor(current_color, self, f"Pick {attr}")
        
        if color.isValid():
            # Update button
            hex_color = color.name()
            self.color_buttons[attr].setStyleSheet(
                f"background-color: {hex_color}; border: 1px solid #999;"
            )
            self.color_buttons[attr].setText(hex_color)
            
            # Update theme
            setattr(theme, attr, hex_color)
    
    def apply_theme(self):
        """Apply the selected theme"""
        theme_name = self.theme_combo.currentText()
        if self.theme_manager.set_theme(theme_name):
            self.theme_manager.apply_theme(QApplication.instance())
            QMessageBox.information(self, "Theme Applied", 
                                   f"Theme '{theme_name}' has been applied.")
    
    def save_custom_theme(self):
        """Save current settings as a custom theme"""
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, "Save Theme", "Enter theme name:")
        if ok and name:
            # Create new theme from current settings
            theme_name = self.theme_combo.currentText()
            base_theme = self.theme_manager.get_theme(theme_name)
            
            if base_theme:
                # Create copy with new name
                from modules.theme_manager import Theme
                new_theme = Theme(
                    name=name,
                    **{k: v for k, v in base_theme.to_dict().items() if k != 'name'}
                )
                
                # Update with any modified colors
                for attr, btn in self.color_buttons.items():
                    color = btn.text()
                    if color.startswith('#'):
                        setattr(new_theme, attr, color)
                
                self.theme_manager.save_custom_theme(new_theme)
                self.load_themes()
                
                # Select the new theme
                idx = self.theme_combo.findText(name)
                if idx >= 0:
                    self.theme_combo.setCurrentIndex(idx)
                
                QMessageBox.information(self, "Theme Saved", 
                                       f"Custom theme '{name}' has been saved.")
    
    def delete_custom_theme(self):
        """Delete the selected custom theme"""
        theme_name = self.theme_combo.currentText()
        
        # Can't delete predefined themes
        from modules.theme_manager import ThemeManager
        if theme_name in ThemeManager.PREDEFINED_THEMES:
            QMessageBox.warning(self, "Cannot Delete", 
                               "Cannot delete predefined themes.")
            return
        
        reply = QMessageBox.question(self, "Delete Theme",
                                    f"Delete custom theme '{theme_name}'?",
                                    QMessageBox.StandardButton.Yes | 
                                    QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.theme_manager.delete_custom_theme(theme_name):
                self.load_themes()
                QMessageBox.information(self, "Theme Deleted", 
                                       f"Theme '{theme_name}' has been deleted.")


# ============================================================================
# DETACHED LOG WINDOW
# ============================================================================

class DetachedLogWindow(QWidget):
    """Detached log window that can be moved to another screen"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Supervertaler - Session Log")
        self.setWindowIcon(self.parent.windowIcon())
        self.resize(800, 600)

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Top toolbar
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)

        # Info label
        info_label = QLabel("📋 This is a detached log window. It will update in real-time.")
        info_label.setStyleSheet("color: #666; font-style: italic;")
        toolbar_layout.addWidget(info_label)

        toolbar_layout.addStretch()

        # Re-attach button
        reattach_btn = QPushButton("↩️ Close")
        reattach_btn.setToolTip("Close this detached window")
        reattach_btn.clicked.connect(self.close)
        toolbar_layout.addWidget(reattach_btn)

        layout.addWidget(toolbar)

        # Log display
        self.log_display = QPlainTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("""
            QPlainTextEdit {
                background-color: #ffffff;
                color: #000000;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10px;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.log_display)

        # Copy existing log content
        if hasattr(parent, 'session_log') and parent.session_log:
            self.log_display.setPlainText(parent.session_log.toPlainText())
            # Scroll to bottom
            scrollbar = self.log_display.verticalScrollBar()
            if scrollbar:
                scrollbar.setValue(scrollbar.maximum())

    def closeEvent(self, event):
        """Handle window close"""
        # Remove from parent's list
        try:
            if self in self.parent.detached_log_windows:
                self.parent.detached_log_windows.remove(self)
        except:
            pass
        event.accept()


# ============================================================================
# TERM METADATA DIALOG
# ============================================================================

class TermMetadataDialog(QDialog):
    """Dialog for adding/editing term metadata before saving to termbase"""
    
    def __init__(self, source_term: str, target_term: str, active_termbases: list, parent=None):
        super().__init__(parent)
        self.source_term = source_term
        self.target_term = target_term
        self.active_termbases = active_termbases
        self.termbase_checkboxes = {}  # Store checkbox references
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Add Term to Termbase")
        self.setMinimumWidth(550)
