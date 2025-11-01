"""
Supervertaler Qt Edition
========================
Professional Translation Memory & CAT Tool
Modern PyQt6 interface with Universal Lookup and advanced features

Version: 1.1.2 (Phase 5.5)
Release Date: November 1, 2025
Framework: PyQt6

This is the modern edition of Supervertaler using PyQt6 framework.
For the classic tkinter edition, see Supervertaler_tkinter.py

Key Features:
- Universal Lookup with global hotkey (Ctrl+Alt+L)
- Modern theme system (6 themes + custom editor)
- AutoFingers automation for memoQ
- memoQ bilingual DOCX import/export
- SQLite-based translation memory with FTS5 search
- Professional TMX editor

Author: Michael Beijer
License: MIT
"""

# Version Information
__version__ = "1.1.2"
__phase__ = "5.5"
__release_date__ = "2025-11-01"
__edition__ = "Qt"

import sys
import json
import os
import subprocess
import atexit
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import threading
import time  # For delays in Universal Lookup

# Fix encoding for Windows console (UTF-8 support)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# External dependencies
import pyperclip  # For clipboard operations in Universal Lookup
from modules.universal_lookup import UniversalLookupEngine  # Universal Lookup engine

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
        QFrame
    )
    from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal, QObject
    from PyQt6.QtGui import QFont, QAction, QKeySequence, QIcon, QTextOption, QColor
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
# This ensures that private data (API keys, personal projects, etc.) stays in user data_private/
# which is .gitignored, preventing accidental upload to GitHub
ENABLE_PRIVATE_FEATURES = os.path.exists(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".supervertaler.local")
)
if ENABLE_PRIVATE_FEATURES:
    print("[DEV MODE] Private features enabled (.supervertaler.local found)")
    print("[DEV MODE] Using 'user data_private/' folder (git-ignored)")
else:
    print("[USER MODE] Using 'user data/' folder")


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
# DATA MODELS
# ============================================================================

@dataclass
class Segment:
    """Translation segment (matches tkinter version format)"""
    id: int
    source: str
    target: str = ""
    status: str = "untranslated"  # untranslated, draft, translated, approved
    type: str = "para"  # para, heading, list_item, table_cell
    notes: str = ""
    locked: bool = False  # For compatibility with tkinter version
    
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
    
    def __post_init__(self):
        if self.segments is None:
            self.segments = []
        if not self.created:
            self.created = datetime.now().isoformat()
        if not self.modified:
            self.modified = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
            'segments': [seg.to_dict() for seg in self.segments],
            'created': self.created,
            'modified': self.modified
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create Project from dictionary"""
        segments = [Segment.from_dict(seg) for seg in data.get('segments', [])]
        
        # Handle missing name field (use filename or default)
        name = data.get('name', 'Untitled Project')
        
        return cls(
            name=name,
            source_lang=data.get('source_lang', 'en'),
            target_lang=data.get('target_lang', 'nl'),
            segments=segments,
            created=data.get('created', ''),
            modified=data.get('modified', '')
        )


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
    
    def keyPressEvent(self, event):
        """Override to handle Ctrl+1-9, Ctrl+Up/Down shortcuts"""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
        # Ctrl+1 through Ctrl+9: Insert match by number (global)
            if event.key() >= Qt.Key.Key_1 and event.key() <= Qt.Key.Key_9:
                match_num = event.key() - Qt.Key.Key_0  # Convert key to number
                if hasattr(self, 'assistance_widget') and hasattr(self.assistance_widget, 'all_matches'):
                    matches = self.assistance_widget.all_matches
                    if 0 < match_num <= len(matches):
                        match = matches[match_num - 1]
                        # Insert the match target into current cell
                        self.on_match_inserted(match.target)
                        event.accept()
                        return
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
        super().keyPressEvent(event)


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
        """Create HTML with highlighted termbase matches"""
        text = self.source_text
        
        # Sort terms by length (longest first) to avoid overlaps
        sorted_terms = sorted(self.termbase_matches.keys(), key=len, reverse=True)
        
        # Build HTML with highlights
        html = text
        offset = 0
        
        for term in sorted_terms:
            # Case-insensitive search
            search_term = term.lower()
            search_html = html.lower()
            
            # Find all occurrences
            start = 0
            while True:
                idx = search_html.find(search_term, start)
                if idx == -1:
                    break
                
                # Extract original casing
                original_term = html[idx:idx + len(term)]
                
                # Replace with highlighted version
                highlighted = f'<span style="color: blue; font-weight: bold; text-decoration: underline; cursor: pointer;" class="termbase-match" data-term="{term}">{original_term}</span>'
                
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
        for term, translation in self.termbase_matches.items():
            # Check if this term contains the click area (very approximate)
            if self.term_double_clicked is not None and callable(self.term_double_clicked):
                # For now, if we get a double-click and there are matches,
                # this is a signal to insert the first/only match
                # Better implementation would need proper hit detection
                pass
        
        super().mouseDoubleClickEvent(ev)


class WordWrapDelegate(QStyledItemDelegate):
    """Custom delegate to enable word wrap when editing cells"""
    
    def __init__(self, assistance_panel=None, table_widget=None):
        super().__init__()
        self.assistance_panel = assistance_panel
        self.table_widget = table_widget
    
    def createEditor(self, parent, option, index):
        """Create a QTextEdit for multi-line editing with word wrap"""
        # Only use QTextEdit for Target column (column 3)
        if index.column() == 3:
            editor = GridTextEditor(parent)
            editor.assistance_panel = self.assistance_panel
            editor.table_widget = self.table_widget
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
        else:
            return super().createEditor(parent, option, index)
    
    def setEditorData(self, editor, index):
        """Load data into the editor"""
        if isinstance(editor, QTextEdit):
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
        if isinstance(editor, QTextEdit):
            text = editor.toPlainText()
            model.setData(index, text, Qt.ItemDataRole.EditRole)
        else:
            super().setModelData(editor, model, index)
    
    def updateEditorGeometry(self, editor, option, index):
        """Set the editor geometry to match the cell size"""
        if isinstance(editor, QTextEdit):
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
# MAIN WINDOW
# ============================================================================

class SupervertalerQt(QMainWindow):
    """Main application window"""
    
    MAX_RECENT_PROJECTS = 10  # Maximum number of recent projects to track
    
    def __init__(self):
        super().__init__()
        
        # Application state
        self.current_project: Optional[Project] = None
        self.project_file_path: Optional[str] = None
        self.project_modified = False
        
        # UI Configuration
        self.default_font_family = "Calibri"
        self.default_font_size = 11
        
        # Application settings
        self.allow_replace_in_source = False  # Safety: don't allow replace in source by default
        
        # Translation Memory
        self.tm_database = None  # Will be initialized when project is loaded
        
        # Database Manager for Termbases
        from modules.database_manager import DatabaseManager
        self.user_data_path = Path("user data_private" if ENABLE_PRIVATE_FEATURES else "user data")
        self.db_manager = DatabaseManager(
            db_path=str(self.user_data_path / "Translation_Resources" / "supervertaler.db"),
            log_callback=self.log
        )
        self.db_manager.connect()
        
        # Theme Manager
        from modules.theme_manager import ThemeManager
        self.theme_manager = None  # Will be initialized after UI setup
        
        # User data path - uses safety system to prevent private data leaks
        # If .supervertaler.local exists: uses "user data_private" (git-ignored)
        # Otherwise: uses "user data" (safe to commit)
        base_folder = "user data_private" if ENABLE_PRIVATE_FEATURES else "user data"
        self.recent_projects_file = self.user_data_path / "recent_projects.json"
        
        # Initialize UI
        self.init_ui()
        
        # Initialize theme manager and apply theme
        self.theme_manager = ThemeManager(self.user_data_path)
        self.theme_manager.apply_theme(QApplication.instance())
        
        # Create example API keys file on first launch (after UI is ready)
        self.ensure_example_api_keys()
        
        self.log("Welcome to Supervertaler Qt v1.1.2")
        self.log("Professional Translation Memory & CAT Tool")
        
        # Restore last project if enabled in settings
        self.restore_last_project_if_enabled()
        
        # Load font sizes from preferences (after UI is fully initialized)
        QApplication.instance().processEvents()  # Allow UI to finish initializing
        self.load_font_sizes_from_preferences()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Build window title with dev mode indicator
        title = "Supervertaler Qt v1.1.2"
        if ENABLE_PRIVATE_FEATURES:
            title += " [🛠️ DEV MODE]"
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 1400, 800)
        
        # Create menu bar (ribbon removed - using traditional menus)
        self.create_menus()
        
        # Ribbon removed - all functionality moved to menu bar
        # self.create_ribbon()
        
        # Create main layout
        self.create_main_layout()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def create_menus(self):
        """Create application menus"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Project", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open Project...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        # Recent projects submenu
        self.recent_menu = file_menu.addMenu("Open &Recent")
        self.update_recent_menu()
        
        file_menu.addSeparator()
        
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        close_action = QAction("&Close Project", self)
        close_action.triggered.connect(self.close_project)
        file_menu.addAction(close_action)
        
        file_menu.addSeparator()
        
        # Import/Export submenu
        import_menu = file_menu.addMenu("&Import")
        
        import_memoq_action = QAction("memoQ &Bilingual Table (DOCX)...", self)
        import_memoq_action.triggered.connect(self.import_memoq_bilingual)
        import_menu.addAction(import_memoq_action)
        
        export_menu = file_menu.addMenu("&Export")
        
        export_memoq_action = QAction("memoQ &Bilingual Table - Translated (DOCX)...", self)
        export_memoq_action.triggered.connect(self.export_memoq_bilingual)
        export_menu.addAction(export_memoq_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction("&Find...", self)
        find_action.setShortcut(QKeySequence.StandardKey.Find)
        find_action.triggered.connect(self.show_find_replace_dialog)
        edit_menu.addAction(find_action)
        
        replace_action = QAction("&Replace...", self)
        replace_action.setShortcut(QKeySequence.StandardKey.Replace)
        replace_action.triggered.connect(self.show_find_replace_dialog)
        edit_menu.addAction(replace_action)
        
        edit_menu.addSeparator()
        
        goto_action = QAction("&Go to Segment...", self)
        goto_action.setShortcut("Ctrl+G")
        goto_action.triggered.connect(self.show_goto_dialog)
        edit_menu.addAction(goto_action)
        
        edit_menu.addSeparator()
        
        translate_action = QAction("&Translate Segment", self)
        translate_action.setShortcut("Ctrl+T")
        translate_action.triggered.connect(self.translate_current_segment)
        edit_menu.addAction(translate_action)
        
        batch_translate_action = QAction("Translate &Multiple Segments...", self)
        batch_translate_action.setShortcut("Ctrl+Shift+T")
        batch_translate_action.triggered.connect(self.translate_batch)
        edit_menu.addAction(batch_translate_action)
        
        edit_menu.addSeparator()
        
        # Universal Lookup
        universal_lookup_action = QAction("🔍 &Universal Lookup...", self)
        universal_lookup_action.setShortcut("Ctrl+Alt+L")
        universal_lookup_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(2) if hasattr(self, 'main_tabs') else None)
        edit_menu.addAction(universal_lookup_action)
        
        # View Menu
        view_menu = menubar.addMenu("&View")
        
        # Navigation submenu
        nav_menu = view_menu.addMenu("📑 &Navigate To")
        
        go_projects_action = QAction("📁 &Project Manager", self)
        go_projects_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(0) if hasattr(self, 'main_tabs') else None)
        nav_menu.addAction(go_projects_action)
        
        go_editor_action = QAction("📝 &Project Editor", self)
        go_editor_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(1) if hasattr(self, 'main_tabs') else None)
        nav_menu.addAction(go_editor_action)
        
        go_tm_action = QAction("📊 &Translation Memories", self)
        go_tm_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(2) if hasattr(self, 'main_tabs') else None)
        nav_menu.addAction(go_tm_action)
        
        go_termbases_action = QAction("🏷️ &Termbases", self)
        go_termbases_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(3) if hasattr(self, 'main_tabs') else None)
        nav_menu.addAction(go_termbases_action)
        
        view_menu.addSeparator()
        
        # Grid Text section
        grid_zoom_menu = view_menu.addMenu("📊 &Grid Text Zoom")
        
        grid_zoom_in = QAction("Grid Zoom &In", self)
        grid_zoom_in.setShortcut(QKeySequence.StandardKey.ZoomIn)
        grid_zoom_in.triggered.connect(self.zoom_in)
        grid_zoom_menu.addAction(grid_zoom_in)
        
        grid_zoom_out = QAction("Grid Zoom &Out", self)
        grid_zoom_out.setShortcut(QKeySequence.StandardKey.ZoomOut)
        grid_zoom_out.triggered.connect(self.zoom_out)
        grid_zoom_menu.addAction(grid_zoom_out)
        
        grid_zoom_menu.addSeparator()
        
        grid_increase_font = QAction("Grid &Increase Font Size", self)
        grid_increase_font.setShortcut("Ctrl++")
        grid_increase_font.triggered.connect(self.increase_font_size)
        grid_zoom_menu.addAction(grid_increase_font)
        
        grid_decrease_font = QAction("Grid &Decrease Font Size", self)
        grid_decrease_font.setShortcut("Ctrl+-")
        grid_decrease_font.triggered.connect(self.decrease_font_size)
        grid_zoom_menu.addAction(grid_decrease_font)
        
        grid_zoom_menu.addSeparator()
        
        grid_font_family_menu = grid_zoom_menu.addMenu("Grid Font &Family")
        font_families = ["Calibri", "Segoe UI", "Arial", "Consolas", "Verdana", 
                        "Times New Roman", "Georgia", "Courier New"]
        for font_name in font_families:
            font_action = QAction(font_name, self)
            font_action.triggered.connect(lambda checked, f=font_name: self.set_font_family(f))
            grid_font_family_menu.addAction(font_action)
        
        view_menu.addSeparator()
        
        # Translation Results Pane section
        results_zoom_menu = view_menu.addMenu("📋 Translation &Results Pane")
        
        results_zoom_in_action = QAction("Results Zoom &In", self)
        results_zoom_in_action.setShortcut("Ctrl+Shift+=")
        results_zoom_in_action.triggered.connect(self.results_pane_zoom_in)
        results_zoom_menu.addAction(results_zoom_in_action)
        
        results_zoom_out_action = QAction("Results Zoom &Out", self)
        results_zoom_out_action.setShortcut("Ctrl+Shift+-")
        results_zoom_out_action.triggered.connect(self.results_pane_zoom_out)
        results_zoom_menu.addAction(results_zoom_out_action)
        
        results_zoom_reset_action = QAction("Results Zoom &Reset", self)
        results_zoom_reset_action.triggered.connect(self.results_pane_zoom_reset)
        results_zoom_menu.addAction(results_zoom_reset_action)
        
        results_zoom_menu.addSeparator()
        
        results_note = QAction("(Includes match list + compare boxes)", self)
        results_note.setEnabled(False)
        results_zoom_menu.addAction(results_note)
        
        view_menu.addSeparator()
        
        auto_resize_action = QAction("📐 &Auto-Resize Rows", self)
        auto_resize_action.triggered.connect(self.auto_resize_rows)
        auto_resize_action.setToolTip("Automatically resize all rows to fit content")
        view_menu.addAction(auto_resize_action)
        
        # Tools Menu
        tools_menu = menubar.addMenu("&Tools")
        
        tm_manager_action = QAction("&Translation Memory Manager...", self)
        tm_manager_action.setShortcut("Ctrl+M")
        tm_manager_action.triggered.connect(self.show_tm_manager)
        tools_menu.addAction(tm_manager_action)
        
        autofingers_action = QAction("✋ &AutoFingers - CAT Tool Automation...", self)
        autofingers_action.setShortcut("Ctrl+Shift+A")
        autofingers_action.triggered.connect(self.show_autofingers)
        tools_menu.addAction(autofingers_action)
        
        tools_menu.addSeparator()
        
        theme_action = QAction("🎨 &Theme Editor...", self)
        theme_action.triggered.connect(self.show_theme_editor)
        tools_menu.addAction(theme_action)
        
        options_action = QAction("&Options...", self)
        options_action.triggered.connect(self.show_options_dialog)
        tools_menu.addAction(options_action)
        
        # Help Menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_quick_access_toolbar(self):
        """Create Quick Access Toolbar above ribbon"""
        from PyQt6.QtWidgets import QToolBar, QWidget, QHBoxLayout
        from PyQt6.QtCore import QSize
        
        qat = QToolBar("Quick Access")
        qat.setMovable(False)
        qat.setFloatable(False)
        qat.setIconSize(QSize(20, 20))
        qat.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        qat.setMaximumHeight(28)
        qat.setMinimumWidth(170)  # Fixed width to align ribbon tabs
        qat.setMaximumWidth(170)
        
        # Styling for compact appearance
        qat.setStyleSheet("""
            QToolBar {
                background: transparent;
                border: none;
                spacing: 2px;
                padding: 2px;
            }
            QToolButton {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 3px;
                padding: 2px;
                margin: 0px;
                font-size: 14pt;
            }
            QToolButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            QToolButton:pressed {
                background: rgba(0, 0, 0, 0.1);
            }
        """)
        
        # Empty toolbar - all buttons removed, minimize moved to ribbon
        # Add empty separator just to maintain spacing
        qat.addSeparator()
        
        return qat
    
    def create_ribbon(self):
        """
        Create modern ribbon interface - DISABLED
        Ribbon functionality has been moved to traditional menu bar.
        This code is kept for potential future use.
        """
        # Ribbon removed - all actions are now in the menu bar
        # Keeping this method for potential future re-enablement
        return
        
        # from modules.ribbon_widget import RibbonWidget, RibbonTab, RibbonGroup, RibbonButton
        # 
        # # Create ribbon widget
        # self.ribbon = RibbonWidget(self)
        # 
        # # Connect ribbon actions to methods
        # self.ribbon.action_triggered.connect(self.handle_ribbon_action)
        
        # Ribbon code commented out - all functionality moved to menu bar
        # HOME TAB - Project management and navigation
        # home_tab = RibbonTab()
        # project_group = RibbonGroup("Project")
        # project_group.add_button(self.ribbon.create_button("New", "📄", "new", "New project (Ctrl+N)"))
        # ... (all ribbon tab creation code commented out)
        # All actions are now available in the traditional menu bar
    
    def create_ribbon_toolbar(self):
        """Create a toolbar to hold the ribbon - DISABLED"""
        # Ribbon removed - using traditional menu bar instead
        # This method kept for potential future use
        return None
    
    def toggle_ribbon_minimized(self, minimized: bool):
        """Toggle ribbon between full and minimized (tabs-only) mode - DISABLED"""
        # Ribbon removed - no action needed
        self.ribbon_minimized = minimized  # Store state for backwards compatibility
        pass
    
    def show_ribbon_temporarily(self, index: int):
        """Show ribbon temporarily when tab clicked in minimized mode - DISABLED"""
        # Ribbon removed - no action needed
        pass
    
    def on_main_tab_changed(self, index: int):
        """Handle main tab change"""
        # Ribbon removed - menu bar remains constant across all tabs
        # No context switching needed
        pass
    
    def toggle_sidebar(self, visible: bool):
        """Toggle Quick Access Sidebar visibility - DEPRECATED (Quick Access removed)"""
        # The Quick Access sidebar has been removed in favor of Project Home collapsible panel
        pass
    
    def update_sidebar_recent_files(self):
        """Update sidebar recent files list - DEPRECATED (Quick Access removed)"""
        # The Quick Access sidebar has been removed in favor of Project Home collapsible panel
        pass
    
    def handle_ribbon_action(self, action_name: str):
        """
        Handle ribbon button clicks - DEPRECATED
        Ribbon has been removed in favor of traditional menu bar.
        All actions are now accessible through menus.
        This method is kept for backwards compatibility.
        """
        # All ribbon actions have been moved to menu bar
        # This method is kept in case any code still references it
        action_map = {
            # File actions
            "new": self.new_project,
            "open": self.open_project,
            "save": self.save_project,
            "close_project": self.close_project,
            
            # Navigation actions
            "go_to_projects": lambda: self.main_tabs.setCurrentIndex(0) if hasattr(self, 'main_tabs') else None,
            "go_to_editor": lambda: self.main_tabs.setCurrentIndex(1) if hasattr(self, 'main_tabs') else None,
            "go_to_tm": lambda: self.main_tabs.setCurrentIndex(2) if hasattr(self, 'main_tabs') else None,
            "go_to_termbases": lambda: self.main_tabs.setCurrentIndex(3) if hasattr(self, 'main_tabs') else None,
            
            # Translation actions
            "translate": self.translate_current_segment,
            "batch_translate": self.translate_batch,
            "tm_manager": self.show_tm_manager,
            "universal_lookup": lambda: self.main_tabs.setCurrentIndex(2) if hasattr(self, 'main_tabs') else None,
            
            # View actions
            "zoom_in": self.zoom_in,
            "zoom_out": self.zoom_out,
            "auto_resize": self.auto_resize_rows,
            "themes": self.show_theme_editor,
            
            # Tools actions
            "autofingers": self.show_autofingers,
            "options": self.show_options_dialog,
        }
        
        # Execute action if found (for backwards compatibility)
        action = action_map.get(action_name)
        if action:
            action()
    
    
    def create_toolbar(self):
        """Create main toolbar - REMOVED: Replaced by ribbon interface"""
        # Toolbar removed - replaced by modern ribbon interface
        # All functionality accessible via ribbon tabs and menus
        pass
    
    def create_main_layout(self):
        """Create main application layout with tabs"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with splitter for sidebar and main content
        from PyQt6.QtWidgets import QSplitter, QHBoxLayout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create tab widget for main interface with HORIZONTAL tabs
        self.main_tabs = QTabWidget()
        # self.main_tabs.setTabPosition(QTabWidget.TabPosition.West)  # Uncomment for vertical tabs
        
        # Connect tab change to ribbon update
        self.main_tabs.currentChanged.connect(self.on_main_tab_changed)
        
        # Style tabs with color coding by function group
        self.main_tabs.setStyleSheet("""
            QTabBar::tab { padding: 8px 15px; }
        """)
        
        # ===== GROUP 1: PROJECT MANAGEMENT (Orange) =====
        projects_tab = self.create_projects_manager_tab()
        self.main_tabs.addTab(projects_tab, "📁 Project Manager")
        
        editor_tab = self.create_editor_tab()
        self.main_tabs.addTab(editor_tab, "📝 Project Editor")
        
        # ===== GROUP 2: TRANSLATION RESOURCES (Purple) =====
        tm_tab = self.create_translation_memories_tab()
        self.main_tabs.addTab(tm_tab, "💾 Translation Memories")
        
        termbase_tab = self.create_termbases_tab()
        self.main_tabs.addTab(termbase_tab, "🏷️ Termbases")
        
        nt_tab = self.create_non_translatables_tab()
        self.main_tabs.addTab(nt_tab, "🚫 Non-Translatables")
        
        prompt_tab = self.create_prompt_manager_tab()
        self.main_tabs.addTab(prompt_tab, "💡 Prompt Manager")
        
        # ===== GROUP 3: SPECIALIZED MODULES (Green) =====
        tmx_tab = self.create_tmx_editor_tab()
        self.main_tabs.addTab(tmx_tab, "✏️ TMX Editor")
        
        ref_tab = self.create_reference_images_tab()
        self.main_tabs.addTab(ref_tab, "🖼️ Reference Images")
        
        pdf_tab = self.create_pdf_rescue_tab()
        self.main_tabs.addTab(pdf_tab, "📄 PDF Rescue")
        
        encoding_tab = self.create_encoding_repair_tab()
        self.main_tabs.addTab(encoding_tab, "🔧 Encoding Repair")
        
        self.autofingers_tab = AutoFingersWidget(self)
        self.main_tabs.addTab(self.autofingers_tab, "✋ AutoFingers")
        
        tracked_tab = self.create_tracked_changes_tab()
        self.main_tabs.addTab(tracked_tab, "🔄 Tracked Changes")
        
        # ===== GROUP 4: SETTINGS/LOG (Gray) =====
        settings_tab = self.create_settings_tab()
        self.main_tabs.addTab(settings_tab, "⚙️ Settings")
        
        log_tab = self.create_log_tab()
        self.main_tabs.addTab(log_tab, "📋 Log")
        
        # ===== UTILITIES =====
        self.lookup_tab = UniversalLookupTab(self)
        self.main_tabs.addTab(self.lookup_tab, "🔍 Universal Lookup")
        
        # Add tabs to content layout
        content_layout.addWidget(self.main_tabs)
        
        # Add content directly to main layout
        main_layout.addWidget(content_widget)
    
    def _create_placeholder_tab(self, title: str, description: str) -> QWidget:
        """Create a simple placeholder tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        header = QLabel(title)
        header.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)
        
        placeholder = QLabel(description)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(placeholder, stretch=1)
        
        return tab
    
    def create_non_translatables_tab(self) -> QWidget:
        """Create the Non-Translatables tab - NT management"""
        return self._create_placeholder_tab(
            "🚫 Non-Translatables",
            "Non-Translatables Manager - Coming Soon\n\nFeatures:\n• Manage non-translatable content\n• Define NT patterns\n• Exclude from translation"
        )
    
    def create_prompt_manager_tab(self) -> QWidget:
        """Create the Prompt Manager tab - System Prompts"""
        return self._create_placeholder_tab(
            "📚 Prompt Manager",
            "Prompt Manager - Coming Soon\n\nFeatures:\n• Manage system prompts\n• Domain-specific translations\n• Custom instructions"
        )
    
    def create_tmx_editor_tab(self) -> QWidget:
        """Create the TMX Editor tab - Edit TMs"""
        from modules.tmx_editor_qt import TmxEditorUIQt
        
        # Create container widget with Universal Lookup style header
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)  # Reduced from 10 to 5 for tighter spacing
        
        # Header (matches Universal Lookup / AutoFingers / PDF Rescue style)
        header = QLabel("📝 TMX Editor")
        header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
        layout.addWidget(header, 0)  # 0 = no stretch, stays compact
        
        # Description box (matches Universal Lookup / AutoFingers / PDF Rescue style)
        description = QLabel(
            "Edit translation memory files directly - inspired by Heartsome TMX Editor.\n"
            "Open, edit, filter, and manage your TMX translation memories."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
        layout.addWidget(description, 0)  # 0 = no stretch, stays compact
        
        # Create TMX Editor widget (embedded mode) - pass database manager
        tmx_editor = TmxEditorUIQt(parent=None, standalone=False, db_manager=self.db_manager)
        layout.addWidget(tmx_editor, 1)  # 1 = stretch factor, expands to fill space
        
        # Store reference for potential future use
        self.tmx_editor_embedded = tmx_editor
        
        return container
    
    def create_reference_images_tab(self) -> QWidget:
        """Create the Reference Images tab - Visual context"""
        return self._create_placeholder_tab(
            "🖼️ Reference Images",
            "Reference Images - Coming Soon\n\nFeatures:\n• Upload reference images\n• Visual context for translation\n• Screenshot annotation"
        )
    
    def create_pdf_rescue_tab(self) -> QWidget:
        """Create the PDF Rescue tab - AI OCR"""
        from modules.pdf_rescue_Qt import PDFRescueQt
        
        # Create PDF Rescue widget (embedded mode, not standalone)
        pdf_rescue_widget = QWidget()
        self.pdf_rescue_qt = PDFRescueQt(self, standalone=False)
        self.pdf_rescue_qt.create_tab(pdf_rescue_widget)
        
        return pdf_rescue_widget
    
    def create_encoding_repair_tab(self) -> QWidget:
        """Create the Encoding Repair tab - Text Encoding Tool"""
        return self._create_placeholder_tab(
            "🔧 Encoding Repair",
            "Encoding Repair - Coming Soon\n\nFeatures:\n• Fix mojibake/encoding issues\n• Auto-detect encoding\n• Batch repair"
        )
    
    def create_tracked_changes_tab(self) -> QWidget:
        """Create the Tracked Changes tab - Post-Translation Analysis"""
        return self._create_placeholder_tab(
            "📊 Tracked Changes",
            "Tracked Changes - Coming Soon\n\nFeatures:\n• Track translation changes\n• Version history\n• Comparison reports"
        )
    
    def create_log_tab(self) -> QWidget:
        """Create the Log tab - Session Log"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Log display area
        self.session_log = QPlainTextEdit()
        self.session_log.setReadOnly(True)
        self.session_log.setStyleSheet("""
            QPlainTextEdit {
                background: #1e1e1e;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        layout.addWidget(self.session_log)
        
        return tab
    
    def create_projects_manager_tab(self):
        """Create the Projects Manager tab - manage projects, attach TMs and glossaries"""
        from PyQt6.QtWidgets import QSplitter, QPushButton, QLabel, QFrame
        
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with controls
        header = QFrame()
        header.setStyleSheet("background: #f0f0f0; border-bottom: 1px solid #ddd;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 8, 10, 8)
        header_layout.setSpacing(8)
        
        header_layout.addWidget(QLabel("📁 Project Manager"))
        header_layout.addStretch()
        
        new_btn = QPushButton("➕ New Project")
        new_btn.setMaximumWidth(120)
        new_btn.clicked.connect(self.new_project)
        header_layout.addWidget(new_btn)
        
        open_btn = QPushButton("📂 Open Project")
        open_btn.setMaximumWidth(120)
        open_btn.clicked.connect(self.open_project)
        header_layout.addWidget(open_btn)
        
        layout.addWidget(header)
        
        # TODO: Add project list on left, project details on right
        placeholder = QLabel("Projects Manager - Coming Soon\n\nFeatures:\n• Create new projects\n• Browse past projects\n• Edit project settings\n• Attach TMs and glossaries")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(placeholder, stretch=1)
        
        return tab
    
    def create_translation_memories_tab(self):
        """Create the Translation Memories tab - manage all TMs (global)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = QLabel("💾 Translation Memories")
        header.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # TODO: Add TM list with activate/deactivate, properties, import/export
        placeholder = QLabel("Translation Memories Manager - Coming Soon\n\nFeatures:\n• View all available TMs\n• Activate/deactivate for current project\n• Import new TMs\n• Export TMs\n• Manage TM properties")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(placeholder, stretch=1)
        
        return tab
    
    def create_termbases_tab(self):
        """Create the Termbases tab - manage all termbases (global and project-specific)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = QLabel("📚 Termbases")
        header.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Description
        desc = QLabel("Manage termbases for terminology searching. Activate/deactivate for current project.")
        desc.setStyleSheet("color: #666; font-size: 11px; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Check if database is available
        if not (hasattr(self, 'db_manager') and self.db_manager):
            placeholder = QLabel("Termbases Manager\n\nDatabase not initialized.")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("color: #888; font-size: 12px;")
            layout.addWidget(placeholder, stretch=1)
            return tab
        
        # Import here to avoid issues if database not available
        from modules.termbase_manager import TermbaseManager
        termbase_mgr = TermbaseManager(self.db_manager, self.log)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search termbases...")
        search_box.setMaximumWidth(300)
        search_layout.addWidget(search_box)
        search_layout.addStretch()
        layout.addLayout(search_layout)
        
        # Termbase list with table
        termbase_table = QTableWidget()
        termbase_table.setColumnCount(5)
        termbase_table.setHorizontalHeaderLabels(["Active", "Name", "Languages", "Terms", "Scope"])
        termbase_table.horizontalHeader().setStretchLastSection(False)
        termbase_table.setColumnWidth(0, 60)
        termbase_table.setColumnWidth(1, 200)
        termbase_table.setColumnWidth(2, 150)
        termbase_table.setColumnWidth(3, 80)
        termbase_table.setColumnWidth(4, 100)
        
        # Get current project
        current_project = self.current_project if hasattr(self, 'current_project') else None
        # current_project is a Project object, not a dict
        project_id = current_project.id if (current_project and hasattr(current_project, 'id')) else None
        
        # Populate termbase list
        def refresh_termbase_list():
            termbases = termbase_mgr.get_all_termbases()
            termbase_table.setRowCount(len(termbases))
            
            for row, tb in enumerate(termbases):
                # Check if active for current project
                is_active = termbase_mgr.is_termbase_active(tb['id'], project_id) if project_id else True
                
                # Active checkbox
                checkbox = QCheckBox()
                checkbox.setChecked(is_active)
                checkbox.toggled.connect(lambda checked, tb_id=tb['id']: 
                    termbase_mgr.activate_termbase(tb_id, project_id) if checked and project_id else termbase_mgr.deactivate_termbase(tb_id, project_id) if project_id else None)
                termbase_table.setCellWidget(row, 0, checkbox)
                
                # Name (bold if active)
                name_item = QTableWidgetItem(tb['name'])
                if is_active:
                    font = name_item.font()
                    font.setBold(True)
                    name_item.setFont(font)
                termbase_table.setItem(row, 1, name_item)
                
                # Languages
                langs = f"{tb['source_lang'] or '?'} → {tb['target_lang'] or '?'}"
                termbase_table.setItem(row, 2, QTableWidgetItem(langs))
                
                # Term count
                termbase_table.setItem(row, 3, QTableWidgetItem(str(tb['term_count'])))
                
                # Scope
                scope = "Global" if tb['is_global'] else "Project"
                termbase_table.setItem(row, 4, QTableWidgetItem(scope))
        
        refresh_termbase_list()
        layout.addWidget(termbase_table, stretch=1)
        
        # Button bar
        button_layout = QHBoxLayout()
        
        create_btn = QPushButton("+ Create New")
        create_btn.clicked.connect(lambda: self._show_create_termbase_dialog(termbase_mgr, refresh_termbase_list, project_id))
        button_layout.addWidget(create_btn)
        
        import_btn = QPushButton("📥 Import")
        button_layout.addWidget(import_btn)
        
        export_btn = QPushButton("📤 Export")
        button_layout.addWidget(export_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        button_layout.addWidget(delete_btn)
        
        edit_btn = QPushButton("✏️ Edit Terms")
        edit_btn.clicked.connect(lambda: self._show_edit_terms_dialog(termbase_mgr, termbase_table, refresh_termbase_list))
        button_layout.addWidget(edit_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return tab
    
    def _show_create_termbase_dialog(self, termbase_mgr, refresh_callback, project_id):
        """Show dialog to create new termbase"""
        from modules.termbase_manager import TermbaseManager
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New Termbase")
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        # Name
        name_field = QLineEdit()
        layout.addRow("Termbase Name:", name_field)
        
        # Source language
        source_lang_field = QLineEdit()
        source_lang_field.setPlaceholderText("e.g., en, nl, de")
        layout.addRow("Source Language:", source_lang_field)
        
        # Target language
        target_lang_field = QLineEdit()
        target_lang_field.setPlaceholderText("e.g., en, nl, de")
        layout.addRow("Target Language:", target_lang_field)
        
        # Description
        desc_field = QTextEdit()
        desc_field.setMaximumHeight(80)
        layout.addRow("Description:", desc_field)
        
        # Scope
        scope_group = QButtonGroup()
        global_radio = QRadioButton("Global (all projects)")
        global_radio.setChecked(True)
        project_radio = QRadioButton("Project-specific")
        scope_group.addButton(global_radio, 0)
        scope_group.addButton(project_radio, 1)
        
        scope_layout = QHBoxLayout()
        scope_layout.addWidget(global_radio)
        scope_layout.addWidget(project_radio)
        layout.addRow("Scope:", scope_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        create_btn = QPushButton("Create")
        cancel_btn = QPushButton("Cancel")
        
        def create_termbase():
            name = name_field.text().strip()
            if not name:
                QMessageBox.warning(dialog, "Error", "Please enter a termbase name")
                return
            
            source_lang = source_lang_field.text().strip() or None
            target_lang = target_lang_field.text().strip() or None
            description = desc_field.toPlainText().strip()
            is_global = scope_group.checkedId() == 0
            
            tb_project_id = None if is_global else project_id
            
            tb_id = termbase_mgr.create_termbase(
                name=name,
                source_lang=source_lang,
                target_lang=target_lang,
                project_id=tb_project_id,
                description=description,
                is_global=is_global
            )
            
            if tb_id:
                QMessageBox.information(dialog, "Success", f"Termbase '{name}' created successfully!")
                refresh_callback()
                dialog.accept()
            else:
                QMessageBox.critical(dialog, "Error", "Failed to create termbase")
        
        create_btn.clicked.connect(create_termbase)
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(create_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow("", button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def _show_edit_terms_dialog(self, termbase_mgr, termbase_table, refresh_callback):
        """Show dialog to edit terms in selected termbase"""
        selected_row = termbase_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Please select a termbase first")
            return
        
        # Get termbase ID from table
        tb_name = termbase_table.item(selected_row, 1).text()
        
        # Find termbase ID
        termbases = termbase_mgr.get_all_termbases()
        termbase = next((tb for tb in termbases if tb['name'] == tb_name), None)
        if not termbase:
            QMessageBox.warning(self, "Error", "Could not find selected termbase")
            return
        
        termbase_id = termbase['id']
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Edit Terms - {tb_name}")
        dialog.setMinimumSize(700, 500)
        
        layout = QVBoxLayout()
        
        # Terms table
        terms_table = QTableWidget()
        terms_table.setColumnCount(5)
        terms_table.setHorizontalHeaderLabels(["Source", "Target", "Domain", "Priority", "Forbidden"])
        terms_table.horizontalHeader().setStretchLastSection(False)
        terms_table.setColumnWidth(0, 150)
        terms_table.setColumnWidth(1, 150)
        terms_table.setColumnWidth(2, 150)
        terms_table.setColumnWidth(3, 80)
        terms_table.setColumnWidth(4, 80)
        
        # Load terms
        def refresh_terms_table():
            terms = termbase_mgr.get_terms(termbase_id)
            terms_table.setRowCount(len(terms))
            
            for row, term in enumerate(terms):
                terms_table.setItem(row, 0, QTableWidgetItem(term['source_term']))
                terms_table.setItem(row, 1, QTableWidgetItem(term['target_term']))
                terms_table.setItem(row, 2, QTableWidgetItem(term['domain'] or ""))
                terms_table.setItem(row, 3, QTableWidgetItem(str(term['priority'])))
                
                forbidden_check = QCheckBox()
                forbidden_check.setChecked(term['forbidden'])
                terms_table.setCellWidget(row, 4, forbidden_check)
        
        refresh_terms_table()
        layout.addWidget(QLabel(f"Terms in '{tb_name}':"), 0)
        layout.addWidget(terms_table, 1)
        
        # Add term section
        add_layout = QHBoxLayout()
        
        source_field = QLineEdit()
        source_field.setPlaceholderText("Source term")
        add_layout.addWidget(source_field)
        
        target_field = QLineEdit()
        target_field.setPlaceholderText("Target term")
        add_layout.addWidget(target_field)
        
        priority_spin = QSpinBox()
        priority_spin.setMinimum(1)
        priority_spin.setMaximum(99)
        priority_spin.setValue(50)
        priority_spin.setMaximumWidth(60)
        add_layout.addWidget(QLabel("Priority:"))
        add_layout.addWidget(priority_spin)
        
        add_btn = QPushButton("+ Add")
        def add_term():
            source = source_field.text().strip()
            target = target_field.text().strip()
            if not source or not target:
                QMessageBox.warning(dialog, "Error", "Both source and target terms are required")
                return
            
            termbase_mgr.add_term(
                termbase_id=termbase_id,
                source_term=source,
                target_term=target,
                priority=priority_spin.value()
            )
            
            source_field.clear()
            target_field.clear()
            refresh_terms_table()
        
        add_btn.clicked.connect(add_term)
        add_layout.addWidget(add_btn)
        layout.addLayout(add_layout)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def create_settings_tab(self):
        """Create the Settings tab - general application settings"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = QLabel("⚙️ General Settings")
        header.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # TODO: Add general settings controls (same as Tools > Options)
        placeholder = QLabel("General Settings - Coming Soon\n\nFeatures:\n• AI Provider settings\n• Display settings\n• Keyboard shortcuts\n• Default languages\n• Export options")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(placeholder, stretch=1)
        
        return tab
    
    def create_editor_tab(self):
        """Create the project editor tab (existing grid view)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Splitter for grid and assistance panel
        self.editor_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Grid container with filter boxes
        grid_container = QWidget()
        grid_layout = QVBoxLayout(grid_container)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(5)
        
        # Warning banner for replace in source (hidden by default)
        self.warning_banner = QWidget()
        self.warning_banner.setStyleSheet(
            "background-color: #dc2626; color: white; padding: 8px; border-radius: 4px;"
        )
        warning_layout = QHBoxLayout(self.warning_banner)
        warning_layout.setContentsMargins(10, 5, 10, 5)
        
        warning_icon = QLabel("⚠️")
        warning_icon.setStyleSheet("font-size: 16px; background: transparent;")
        warning_layout.addWidget(warning_icon)
        
        warning_text = QLabel(
            "<b>WARNING:</b> Replace in Source Text is ENABLED. "
            "This allows modifying your original source segments. Use with extreme caution!"
        )
        warning_text.setStyleSheet("background: transparent; font-weight: bold;")
        warning_text.setWordWrap(True)
        warning_layout.addWidget(warning_text, stretch=1)
        
        settings_link = QPushButton("⚙️ Disable in Options")
        settings_link.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.2); color: white; "
            "border: 1px solid white; padding: 4px 12px; border-radius: 3px; font-weight: bold;"
        )
        settings_link.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_link.clicked.connect(self.show_options_dialog)
        warning_layout.addWidget(settings_link)
        
        grid_layout.addWidget(self.warning_banner)
        self.warning_banner.hide()  # Hidden by default
        
        # Filter panel (like memoQ)
        filter_panel = QWidget()
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(10)
        
        # Source filter
        source_filter_label = QLabel("Filter Source:")
        self.source_filter = QLineEdit()
        self.source_filter.setPlaceholderText("Type to filter source segments...")
        self.source_filter.textChanged.connect(self.apply_filters)
        self.source_filter.returnPressed.connect(self.apply_filters)
        
        # Target filter
        target_filter_label = QLabel("Filter Target:")
        self.target_filter = QLineEdit()
        self.target_filter.setPlaceholderText("Type to filter target segments...")
        self.target_filter.textChanged.connect(self.apply_filters)
        self.target_filter.returnPressed.connect(self.apply_filters)
        
        # Clear filters button
        clear_filters_btn = QPushButton("Clear Filters")
        clear_filters_btn.clicked.connect(self.clear_filters)
        clear_filters_btn.setMaximumWidth(100)
        
        filter_layout.addWidget(source_filter_label)
        filter_layout.addWidget(self.source_filter, stretch=1)
        filter_layout.addWidget(target_filter_label)
        filter_layout.addWidget(self.target_filter, stretch=1)
        filter_layout.addWidget(clear_filters_btn)
        
        grid_layout.addWidget(filter_panel)
        
        # Create assistance panel FIRST so it can be passed to grid editor
        self.create_assistance_panel()
        
        # Translation Grid
        self.create_translation_grid()
        grid_layout.addWidget(self.table)
        
        self.editor_splitter.addWidget(grid_container)
        self.editor_splitter.addWidget(self.assistance_widget)
        
        # Set splitter proportions (70% grid, 30% assistance)
        self.editor_splitter.setSizes([1000, 400])
        
        layout.addWidget(self.editor_splitter)
        
        return tab
    
    def create_translation_grid(self):
        """Create the translation grid (QTableWidget)"""
        self.table = QTableWidget()
        
        # Configure columns
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["#", "Type", "Source", "Target", "Status"])
        
        # Column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Source
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Target
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Status
        
        self.table.setColumnWidth(0, 50)   # ID
        self.table.setColumnWidth(1, 100)  # Type
        self.table.setColumnWidth(4, 80)   # Status
        
        # Enable word wrap in cells (both display and edit mode)
        self.table.setWordWrap(True)
        
        # Apply custom delegate for word wrap in edit mode
        # Pass assistance_panel and table so keyboard shortcuts can be forwarded
        self.table.setItemDelegate(WordWrapDelegate(self.assistance_widget, self.table))
        
        # Row behavior - Select items (not full rows) to allow custom highlighting of segment numbers only
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Alternating row colors
        self.table.setAlternatingRowColors(True)
        
        # Enable editing for Target column only
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked |
                                   QTableWidget.EditTrigger.EditKeyPressed)
        
        # Connect signals
        self.table.itemChanged.connect(self.on_cell_changed)
        self.table.currentCellChanged.connect(self.on_cell_selected)
        self.table.itemClicked.connect(self.on_cell_clicked)
    
    def create_assistance_panel(self):
        """Create right-side assistance panel with TranslationResultsPanel"""
        try:
            from modules.translation_results_panel import TranslationResultsPanel
            self.assistance_widget = TranslationResultsPanel(self)
            self.assistance_widget.match_selected.connect(self.on_match_selected)
            self.assistance_widget.match_inserted.connect(self.on_match_inserted)
        except ImportError as e:
            # Fallback to simple panel if import fails
            print(f"Warning: Could not import TranslationResultsPanel: {e}")
            self.assistance_widget = QWidget()
            layout = QVBoxLayout(self.assistance_widget)
            
            # Translation Memory section
            tm_label = QLabel("📚 Translation Memory")
            tm_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
            layout.addWidget(tm_label)
            
            self.tm_display = QTextEdit()
            self.tm_display.setReadOnly(True)
            self.tm_display.setPlaceholderText("Translation memory matches will appear here...")
            layout.addWidget(self.tm_display, stretch=2)
            
            # Notes section
            notes_label = QLabel("📝 Notes")
            notes_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
            layout.addWidget(notes_label)
            
            self.notes_edit = QTextEdit()
            self.notes_edit.setPlaceholderText("Segment notes...")
            layout.addWidget(self.notes_edit, stretch=1)
    
    def on_match_selected(self, match):
        """Handle match selection from TranslationResultsPanel"""
        # This will be called when user selects a match in the panel
        # Can be used for highlighting, compare boxes, etc.
        pass
    
    def on_match_inserted(self, match_text: str):
        """
        Handle match insertion (user pressed Ctrl+number or Spacebar in match pane)
        Insert the match text into the currently selected target cell
        WITHOUT confirming the segment or moving to next
        """
        try:
            if not self.current_project or not self.table:
                return
            
            # Get current cell from grid
            current_item = self.table.currentItem()
            if current_item:
                row = current_item.row()
                col = current_item.column()
                
                # Check if we're in a target column (column 3 for Target)
                if col == 3 and row < len(self.current_project.segments):
                    # Just insert the match text - don't confirm or move
                    segment = self.current_project.segments[row]
                    segment.target = match_text
                    
                    # Update the table view
                    self.table.item(row, col).setText(match_text)
                    self.log(f"✓ Match inserted into segment {row + 1}")
                    
                    # Stay in current segment - don't move or confirm
                    # User is still in edit mode and can continue editing
        except Exception as e:
            self.log(f"Error inserting match: {e}")
    
    # ========================================================================
    # PROJECT MANAGEMENT
    # ========================================================================
    
    def new_project(self):
        """Create a new project"""
        from PyQt6.QtWidgets import (
            QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, QTextEdit,
            QComboBox, QRadioButton, QButtonGroup, QPushButton, QTabWidget
        )
        from modules.simple_segmenter import SimpleSegmenter
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("New Translation Project")
        dialog.setMinimumWidth(700)
        dialog.setMinimumHeight(500)
        
        layout = QVBoxLayout(dialog)
        
        # Project Settings Group
        settings_group = QGroupBox("Project Settings")
        settings_layout = QFormLayout()
        
        # Project name
        name_input = QLineEdit()
        name_input.setText("Untitled Project")
        name_input.selectAll()
        settings_layout.addRow("Project Name:", name_input)
        
        # Source language
        source_lang_combo = QComboBox()
        common_langs = [
            ("English", "en"),
            ("Dutch", "nl"),
            ("German", "de"),
            ("French", "fr"),
            ("Spanish", "es"),
            ("Italian", "it"),
            ("Portuguese", "pt"),
            ("Russian", "ru"),
            ("Chinese", "zh"),
            ("Japanese", "ja"),
        ]
        for lang_name, lang_code in common_langs:
            source_lang_combo.addItem(lang_name, lang_code)
        settings_layout.addRow("Source Language:", source_lang_combo)
        
        # Target language
        target_lang_combo = QComboBox()
        for lang_name, lang_code in common_langs:
            target_lang_combo.addItem(lang_name, lang_code)
        target_lang_combo.setCurrentIndex(1)  # Default to Dutch
        settings_layout.addRow("Target Language:", target_lang_combo)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Import Options Group
        import_group = QGroupBox("Import Source Text")
        import_layout = QVBoxLayout()
        
        # Tab widget for different import methods
        import_tabs = QTabWidget()
        
        # Tab 1: Paste Text
        paste_tab = QWidget()
        paste_layout = QVBoxLayout(paste_tab)
        paste_layout.addWidget(QLabel("Paste or type your source text below:"))
        
        text_input = QTextEdit()
        text_input.setPlaceholderText(
            "Paste your text here...\n\n"
            "Text will be automatically segmented into sentences.\n"
            "Each sentence becomes a translatable segment."
        )
        paste_layout.addWidget(text_input)
        import_tabs.addTab(paste_tab, "📝 Paste Text")
        
        # Tab 2: Load from File
        file_tab = QWidget()
        file_layout = QVBoxLayout(file_tab)
        file_layout.addWidget(QLabel("Load text from a file:"))
        
        file_path_display = QLineEdit()
        file_path_display.setPlaceholderText("No file selected...")
        file_path_display.setReadOnly(True)
        
        browse_btn = QPushButton("📁 Browse...")
        
        def browse_file():
            file_path, _ = QFileDialog.getOpenFileName(
                dialog,
                "Select Text File",
                "",
                "Text Files (*.txt);;All Files (*.*)"
            )
            if file_path:
                file_path_display.setText(file_path)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_input.setText(f.read())
                    import_tabs.setCurrentIndex(0)  # Switch to paste tab to show loaded text
                except Exception as e:
                    QMessageBox.warning(dialog, "Error", f"Could not load file:\n{e}")
        
        browse_btn.clicked.connect(browse_file)
        
        file_btn_layout = QHBoxLayout()
        file_btn_layout.addWidget(file_path_display)
        file_btn_layout.addWidget(browse_btn)
        file_layout.addLayout(file_btn_layout)
        file_layout.addStretch()
        
        import_tabs.addTab(file_tab, "📄 Load File")
        
        # Tab 3: Start Empty
        empty_tab = QWidget()
        empty_layout = QVBoxLayout(empty_tab)
        empty_layout.addWidget(QLabel("Create an empty project:"))
        empty_layout.addWidget(QLabel("You can add segments manually after creation."))
        empty_layout.addStretch()
        import_tabs.addTab(empty_tab, "\u2b50 Start Empty")
        
        import_layout.addWidget(import_tabs)
        import_group.setLayout(import_layout)
        layout.addWidget(import_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        create_btn = QPushButton("Create Project")
        create_btn.setDefault(True)
        create_btn.setMinimumWidth(120)
        create_btn.clicked.connect(dialog.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(120)
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(create_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Show dialog
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        # Create project
        project_name = name_input.text().strip() or "Untitled Project"
        source_lang = source_lang_combo.currentData()
        target_lang = target_lang_combo.currentData()
        
        # Validate languages
        if source_lang == target_lang:
            QMessageBox.warning(
                self,
                "Invalid Languages",
                "Source and target languages must be different!"
            )
            return
        
        # Create project
        self.current_project = Project(
            name=project_name,
            source_lang=source_lang,
            target_lang=target_lang,
            segments=[]
        )
        
        # Process source text if provided
        source_text = text_input.toPlainText().strip()
        if source_text:
            try:
                segmenter = SimpleSegmenter()
                sentences = segmenter.segment_text(source_text)
                
                # Create segments
                for idx, sentence in enumerate(sentences, start=1):
                    if sentence.strip():
                        segment = Segment(
                            id=idx,
                            source=sentence.strip(),
                            target="",
                            status="untranslated"
                        )
                        self.current_project.segments.append(segment)
                
                self.log(f"Created {len(self.current_project.segments)} segments from source text")
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Segmentation Error",
                    f"Could not segment text:\n{e}\n\nProject created but no segments added."
                )
        
        # Update UI
        self.project_file_path = None
        self.project_modified = True  # Mark as modified since it hasn't been saved
        self.update_window_title()
        self.load_segments_to_grid()
        self.initialize_tm_database()  # Initialize TM for this project
        
        self.log(f"Created new project: {project_name} ({source_lang} → {target_lang})")
        
        # Prompt to save
        if self.current_project.segments:
            reply = QMessageBox.question(
                self,
                "Save Project",
                "Would you like to save your new project now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.save_project_as()
    
    def closeEvent(self, event):
        """Handle application close - cleanup AHK process"""
        try:
            # Terminate AutoHotkey process if running
            if hasattr(self.lookup_tab, 'ahk_process') and self.lookup_tab.ahk_process:
                try:
                    self.lookup_tab.ahk_process.terminate()
                    self.lookup_tab.ahk_process.wait(timeout=2)
                    print("[Universal Lookup] AHK process terminated")
                except:
                    # Force kill if terminate doesn't work
                    try:
                        self.lookup_tab.ahk_process.kill()
                    except:
                        pass
        except Exception as e:
            print(f"[Universal Lookup] Error terminating AHK: {e}")
        
        # Accept the close event
        event.accept()
    
    def open_project(self):
        """Open a project file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            str(self.user_data_path / "Projects"),
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            self.load_project(file_path)
    
    def load_project(self, file_path: str):
        """Load project from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # If no name in file, use filename
            if 'name' not in data:
                data['name'] = Path(file_path).stem
            
            self.current_project = Project.from_dict(data)
            self.project_file_path = file_path
            self.project_modified = False
            
            self.load_segments_to_grid()
            self.initialize_tm_database()  # Initialize TM for this project
            self.update_window_title()
            self.add_to_recent_projects(file_path)
            
            self.log(f"✓ Loaded project: {self.current_project.name} ({len(self.current_project.segments)} segments)")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load project:\n{str(e)}")
            self.log(f"✗ Error loading project: {e}")
    
    def save_project(self):
        """Save current project"""
        if not self.current_project:
            return
        
        if not self.project_file_path:
            self.save_project_as()
        else:
            self.save_project_to_file(self.project_file_path)
    
    def save_project_as(self):
        """Save project with new filename"""
        if not self.current_project:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project As",
            str(self.user_data_path / "Projects" / f"{self.current_project.name}.json"),
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            self.save_project_to_file(file_path)
            self.project_file_path = file_path
            self.add_to_recent_projects(file_path)
    
    def save_project_to_file(self, file_path: str):
        """Save project to specified file"""
        try:
            self.current_project.modified = datetime.now().isoformat()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_project.to_dict(), f, indent=2, ensure_ascii=False)
            
            self.project_modified = False
            self.update_window_title()
            self.log(f"✓ Saved project: {Path(file_path).name}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save project:\n{str(e)}")
            self.log(f"✗ Error saving project: {e}")
    
    def close_project(self):
        """Close current project"""
        if not self.current_project:
            QMessageBox.information(self, "No Project", "No project is currently open")
            return
        
        # Check for unsaved changes
        if self.project_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "Save current project before closing?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                self.save_project()
                # If save was cancelled or failed, project_modified will still be True
                if self.project_modified:
                    return
        
        # Clear project data
        self.current_project = None
        self.project_file_path = None
        self.project_modified = False
        
        # Clear the grid
        self.clear_grid()
        
        # Clear translation results if available
        if hasattr(self, 'assistance_widget'):
            if hasattr(self.assistance_widget, 'clear_results'):
                self.assistance_widget.clear_results()
            # Clear TM and termbase results tables
            if hasattr(self.assistance_widget, 'tm_results_table'):
                self.assistance_widget.tm_results_table.setRowCount(0)
            if hasattr(self.assistance_widget, 'termbase_results_table'):
                self.assistance_widget.termbase_results_table.setRowCount(0)
        
        # Update window title
        self.update_window_title()
        
        self.log("✓ Project closed")
    
    def update_recent_menu(self):
        """Update recent projects menu"""
        self.recent_menu.clear()
        
        recent_projects = self.load_recent_projects()
        
        if not recent_projects:
            no_recent = QAction("No recent projects", self)
            no_recent.setEnabled(False)
            self.recent_menu.addAction(no_recent)
            return
        
        # Add menu items for each recent project
        for i, project_info in enumerate(recent_projects[:self.MAX_RECENT_PROJECTS]):
            path = project_info['path']
            name = project_info['name']
            
            # Show relative path if in workspace, otherwise just filename
            try:
                rel_path = Path(path).relative_to(Path.cwd())
                display_name = f"{i+1}. {name} ({rel_path.parent})"
            except ValueError:
                display_name = f"{i+1}. {name}"
            
            action = QAction(display_name, self)
            action.setStatusTip(path)
            action.triggered.connect(lambda checked, p=path: self.load_project(p))
            self.recent_menu.addAction(action)
        
        # Add separator and "Clear Recent" option
        if recent_projects:
            self.recent_menu.addSeparator()
            clear_action = QAction("Clear Recent Projects", self)
            clear_action.triggered.connect(self.clear_recent_projects)
            self.recent_menu.addAction(clear_action)
    
    def add_to_recent_projects(self, file_path: str):
        """Add project to recent projects list"""
        if not file_path or not os.path.exists(file_path):
            return
        
        # Load existing recent projects
        recent_projects = self.load_recent_projects()
        
        # Create new entry
        new_entry = {
            'path': os.path.abspath(file_path),
            'name': self.current_project.name if self.current_project else Path(file_path).stem,
            'last_opened': datetime.now().isoformat()
        }
        
        # Remove if already exists (to move to top)
        recent_projects = [p for p in recent_projects if p['path'] != new_entry['path']]
        
        # Add to beginning
        recent_projects.insert(0, new_entry)
        
        # Keep only MAX_RECENT_PROJECTS
        recent_projects = recent_projects[:self.MAX_RECENT_PROJECTS]
        
        # Save back to file
        self.save_recent_projects(recent_projects)
        
        # Update menu
        self.update_recent_menu()
    
    def load_recent_projects(self) -> List[Dict[str, str]]:
        """Load recent projects from file"""
        if not self.recent_projects_file.exists():
            return []
        
        try:
            with open(self.recent_projects_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both old dict format and new list format
            if isinstance(data, dict):
                # Old format: convert to list
                recent = []
                for key, value in data.items():
                    if isinstance(value, list):
                        # Extract path and name from old list format
                        for item in value:
                            if isinstance(item, dict):
                                recent.append(item)
                            else:
                                # String path
                                recent.append({
                                    'path': str(item),
                                    'name': Path(str(item)).stem,
                                    'last_opened': datetime.now().isoformat()
                                })
                    elif isinstance(value, str):
                        recent.append({
                            'path': value,
                            'name': Path(value).stem,
                            'last_opened': datetime.now().isoformat()
                        })
                return recent
            elif isinstance(data, list):
                # New format: already a list
                # Ensure all entries have required fields
                normalized = []
                for item in data:
                    if isinstance(item, dict) and 'path' in item:
                        # Ensure all required fields exist
                        if 'name' not in item:
                            item['name'] = Path(item['path']).stem
                        if 'last_opened' not in item:
                            item['last_opened'] = datetime.now().isoformat()
                        # Only include if file still exists
                        if os.path.exists(item['path']):
                            normalized.append(item)
                return normalized
            
            return []
        
        except Exception as e:
            self.log(f"Error loading recent projects: {e}")
            return []
    
    def save_recent_projects(self, recent_projects: List[Dict[str, str]]):
        """Save recent projects to file"""
        try:
            # Ensure directory exists
            self.user_data_path.mkdir(parents=True, exist_ok=True)
            
            with open(self.recent_projects_file, 'w', encoding='utf-8') as f:
                json.dump(recent_projects, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            self.log(f"Error saving recent projects: {e}")
    
    def clear_recent_projects(self):
        """Clear all recent projects"""
        reply = QMessageBox.question(
            self,
            "Clear Recent Projects",
            "Are you sure you want to clear all recent projects?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.save_recent_projects([])
            self.update_recent_menu()
            self.log("Recent projects cleared")
    
    # ========================================================================
    # MEMOQ BILINGUAL DOCX IMPORT/EXPORT
    # ========================================================================
    
    def import_memoq_bilingual(self):
        """Import memoQ bilingual DOCX file (table format)"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select memoQ Bilingual DOCX File",
            "",
            "Word Documents (*.docx);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            from docx import Document
            
            # Load the bilingual DOCX
            doc = Document(file_path)
            
            if not doc.tables:
                QMessageBox.critical(
                    self, "Error",
                    "No table found in the DOCX file.\n\nExpected memoQ bilingual format with a table."
                )
                return
            
            table = doc.tables[0]
            
            # Validate table structure (should have at least 3 rows: header, column names, data)
            if len(table.rows) < 3:
                QMessageBox.critical(
                    self, "Error",
                    f"Invalid table structure.\n\nExpected at least 3 rows, found {len(table.rows)}."
                )
                return
            
            # Extract source and target segments from columns 1 and 2 (skipping header rows 0 and 1)
            # Also extract formatting information (bold, italic, underline)
            segments_data = []  # List of (source, target) tuples
            formatting_map = {}  # segment_index -> list of formatting info
            
            for row_idx in range(2, len(table.rows)):
                row = table.rows[row_idx]
                
                # Ensure we have at least 3 cells (0=segment#, 1=source, 2=target)
                if len(row.cells) >= 3:
                    source_cell = row.cells[1]
                    target_cell = row.cells[2]
                    
                    source_text = source_cell.text.strip()
                    target_text = target_cell.text.strip()
                    
                    # Always add the row to maintain alignment
                    segment_idx = len(segments_data)
                    segments_data.append((source_text, target_text))
                    
                    # Extract formatting from runs in source cell
                    formatting_info = []
                    for paragraph in source_cell.paragraphs:
                        for run in paragraph.runs:
                            run_text = run.text
                            if run_text:  # Only store runs with actual text
                                formatting_info.append({
                                    'text': run_text,
                                    'bold': run.bold == True,
                                    'italic': run.italic == True,
                                    'underline': run.underline == True
                                })
                    
                    # Store formatting for this segment
                    if formatting_info:
                        formatting_map[segment_idx] = formatting_info
            
            if not segments_data:
                QMessageBox.warning(self, "Warning", "No segments found in the bilingual file.")
                return
            
            # Create new project with the imported segments
            project_name = Path(file_path).stem
            
            # Detect languages from table header (row 1, columns 1 and 2)
            header_row = table.rows[1]
            source_lang = "en"  # Default
            target_lang = "nl"  # Default
            
            if len(header_row.cells) >= 3:
                source_header = header_row.cells[1].text.strip().lower()
                target_header = header_row.cells[2].text.strip().lower()
                
                # Try to detect language from header
                lang_map = {
                    'english': 'en', 'dutch': 'nl', 'german': 'de', 'french': 'fr',
                    'spanish': 'es', 'italian': 'it', 'portuguese': 'pt', 'polish': 'pl'
                }
                
                for lang_name, lang_code in lang_map.items():
                    if lang_name in source_header:
                        source_lang = lang_code
                    if lang_name in target_header:
                        target_lang = lang_code
            
            # Create project
            self.current_project = Project(
                name=project_name,
                source_lang=source_lang,
                target_lang=target_lang,
                segments=[]
            )
            
            # Create segments
            for idx, (source_text, target_text) in enumerate(segments_data):
                segment = Segment(
                    id=idx + 1,
                    source=source_text,
                    target=target_text,
                    status="translated" if target_text else "untranslated",
                    type="para"
                )
                self.current_project.segments.append(segment)
            
            # Store the original memoQ file info for export
            self.memoq_source_file = file_path
            self.memoq_formatting_map = formatting_map
            
            # Update UI
            self.project_file_path = None
            self.project_modified = True
            self.update_window_title()
            self.load_segments_to_grid()
            self.initialize_tm_database()
            
            self.log(f"✓ Imported memoQ bilingual DOCX: {len(segments_data)} segments from {Path(file_path).name}")
            
            QMessageBox.information(
                self, "Import Successful",
                f"Imported {len(segments_data)} segment(s) from memoQ bilingual DOCX.\n\n"
                f"File: {Path(file_path).name}\n"
                f"Languages: {source_lang} → {target_lang}"
            )
            
        except ImportError:
            QMessageBox.critical(
                self, "Missing Dependency",
                "The 'python-docx' library is required for memoQ bilingual DOCX import.\n\n"
                "Install it with: pip install python-docx"
            )
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import memoQ bilingual DOCX:\n\n{str(e)}")
            self.log(f"✗ memoQ import failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def export_memoq_bilingual(self):
        """Export to memoQ bilingual DOCX format with translations"""
        # Check if we have segments
        if not self.current_project or not self.current_project.segments:
            QMessageBox.warning(self, "No Data", "No segments to export")
            return
        
        # Check if a memoQ source file was imported
        if not hasattr(self, 'memoq_source_file'):
            QMessageBox.warning(
                self, "No memoQ Source",
                "No memoQ bilingual file was imported.\n\n"
                "This feature is only available after importing a memoQ bilingual DOCX file."
            )
            return
        
        try:
            from docx import Document
            from docx.shared import RGBColor
            
            # Collect translations
            translations = [seg.target for seg in self.current_project.segments]
            
            if not translations or all(not t.strip() for t in translations):
                QMessageBox.warning(self, "Warning", "No translations found to export.")
                return
            
            # Load the original bilingual DOCX
            doc = Document(self.memoq_source_file)
            table = doc.tables[0]
            
            # Write translations to target column (column 2) and update status
            segments_updated = 0
            segments_with_formatting = 0
            
            for i, translation in enumerate(translations):
                row_idx = i + 2  # Skip header rows (0 and 1)
                
                if row_idx < len(table.rows):
                    row = table.rows[row_idx]
                    
                    # Write translation to column 2 (target) with formatting
                    if len(row.cells) >= 3:
                        target_cell = row.cells[2]
                        
                        # Get formatting info for this segment (if available)
                        formatting_info = None
                        if hasattr(self, 'memoq_formatting_map') and i in self.memoq_formatting_map:
                            formatting_info = self.memoq_formatting_map[i]
                            if any(f['bold'] or f['italic'] or f['underline'] for f in formatting_info):
                                segments_with_formatting += 1
                        
                        # Apply formatting to the target cell
                        self._apply_formatting_to_cell(target_cell, translation, formatting_info)
                        segments_updated += 1
                    
                    # Update status to 'Confirmed' in column 4
                    if len(row.cells) >= 5:
                        row.cells[4].text = 'Confirmed'
            
            # Prompt user to save the updated bilingual file
            default_name = Path(self.memoq_source_file).stem + "_translated.docx"
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save memoQ Bilingual DOCX",
                default_name,
                "Word Documents (*.docx);;All Files (*.*)"
            )
            
            if save_path:
                doc.save(save_path)
                
                # Build success message
                success_msg = (
                    f"✓ Successfully exported {segments_updated} translation(s) to memoQ bilingual DOCX!\n\n"
                    f"File saved: {Path(save_path).name}\n\n"
                )
                
                if segments_with_formatting > 0:
                    success_msg += (
                        f"✓ Formatting preserved in {segments_with_formatting} segment(s)\n"
                        f"  (bold, italic, underline)\n\n"
                    )
                
                success_msg += (
                    f"✓ Status updated to 'Confirmed'\n"
                    f"✓ Table structure preserved\n\n"
                    f"You can now import this file back into memoQ."
                )
                
                self.log(f"✓ Exported {segments_updated} translations to memoQ bilingual DOCX: {Path(save_path).name}")
                
                QMessageBox.information(self, "Export Successful", success_msg)
        
        except ImportError:
            QMessageBox.critical(
                self, "Missing Dependency",
                "The 'python-docx' library is required for memoQ bilingual DOCX export.\n\n"
                "Install it with: pip install python-docx"
            )
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export memoQ bilingual DOCX:\n\n{str(e)}")
            self.log(f"✗ memoQ export failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _apply_formatting_to_cell(self, cell, text, formatting_info=None):
        """Apply formatting to a cell based on formatting info from source"""
        # Clear existing paragraphs
        cell._element.clear_content()
        
        # Add new paragraph
        paragraph = cell.add_paragraph()
        
        if not formatting_info or not text:
            # No formatting - just add plain text
            paragraph.add_run(text)
            return
        
        # Apply formatting based on source formatting
        # Match text pieces and apply corresponding formatting
        remaining_text = text
        used_chars = 0
        
        for fmt in formatting_info:
            source_text = fmt['text']
            source_len = len(source_text)
            
            # Find corresponding text in translation (same position ratio)
            ratio = used_chars / sum(len(f['text']) for f in formatting_info)
            target_start = int(ratio * len(text))
            target_len = min(source_len, len(text) - target_start)
            
            if target_len > 0:
                chunk = text[target_start:target_start + target_len]
                run = paragraph.add_run(chunk)
                
                if fmt['bold']:
                    run.bold = True
                if fmt['italic']:
                    run.italic = True
                if fmt['underline']:
                    run.underline = True
                
                used_chars += source_len
        
        # If we didn't format all the text, add the rest as plain text
        if used_chars < len(text):
            ratio = used_chars / len(text)
            if ratio < 0.9:  # If less than 90% formatted, just use plain text
                cell._element.clear_content()
                paragraph = cell.add_paragraph()
                paragraph.add_run(text)
    
    # ========================================================================
    # GRID MANAGEMENT
    # ========================================================================
    
    def load_segments_to_grid(self):
        """Load segments into the grid with termbase highlighting"""
        if not self.current_project or not self.current_project.segments:
            self.clear_grid()
            return
        
        self.table.setRowCount(len(self.current_project.segments))
        
        for row, segment in enumerate(self.current_project.segments):
            # Clear any previous cell widgets
            self.table.removeCellWidget(row, 2)  # Source
            self.table.removeCellWidget(row, 3)  # Target
            
            # ID
            id_item = QTableWidgetItem(str(segment.id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Highlight segment number in orange when selected (like memoQ)
            self.table.setItem(row, 0, id_item)
            
            # Type - show segment type or just #
            type_display = "#" if segment.type == "para" else segment.type.upper()
            type_item = QTableWidgetItem(type_display)
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, type_item)
            
            # Source - Display with termbase matches stored for later use
            source_item = QTableWidgetItem(segment.source)
            source_item.setFlags(source_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
            self.table.setItem(row, 2, source_item)
            
            # Find and store termbase matches (will be used when segment is selected)
            try:
                if hasattr(self, 'db_manager') and self.db_manager:
                    termbase_matches = self.find_termbase_matches_in_source(segment.source)
                    if termbase_matches:
                        self.log(f"📍 Row {row + 1}: Found {len(termbase_matches)} termbase matches")
                        # Store matches in a custom attribute for later use in on_cell_selected
                        source_item.termbase_matches = termbase_matches
                    else:
                        self.log(f"📍 Row {row + 1}: No termbase matches found")
                        source_item.termbase_matches = {}
                else:
                    self.log(f"📍 Row {row + 1}: db_manager not available")
                    source_item.termbase_matches = {}
            except Exception as e:
                self.log(f"❌ Error finding termbase matches for row {row + 1}: {e}")
                import traceback
                self.log(f"Traceback: {traceback.format_exc()}")
                source_item.termbase_matches = {}
            
            # Target (editable)
            target_item = QTableWidgetItem(segment.target)
            self.table.setItem(row, 3, target_item)
            
            # Status
            status_icon = self.get_status_icon(segment.status)
            status_item = QTableWidgetItem(status_icon)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, status_item)
        
        # Apply current font
        self.apply_font_to_grid()
        
        # Auto-resize rows
        self.auto_resize_rows()
        
        self.log(f"✓ Loaded {len(self.current_project.segments)} segments to grid")


    
    def clear_grid(self):
        """Clear all rows from grid"""
        self.table.setRowCount(0)
    
    def auto_resize_rows(self):
        """Auto-resize all rows to fit content - THE MAGIC LINE!"""
        self.table.resizeRowsToContents()
        self.log("✓ Auto-resized rows to fit content")
    
    def apply_font_to_grid(self):
        """Apply selected font to all grid cells"""
        font = QFont(self.default_font_family, self.default_font_size)
        
        self.table.setFont(font)
        
        # Also update header font
        header_font = QFont(self.default_font_family, self.default_font_size, QFont.Weight.Bold)
        self.table.horizontalHeader().setFont(header_font)
    
    def set_font_family(self, family_name: str):
        """Set font family from menu"""
        self.default_font_family = family_name
        self.apply_font_to_grid()
        self.auto_resize_rows()
        self.log(f"✓ Font changed to {family_name}")
    
    def increase_font_size(self):
        """Increase font size (Ctrl++)"""
        self.default_font_size = min(72, self.default_font_size + 1)
        self.apply_font_to_grid()
        self.auto_resize_rows()
        self.log(f"✓ Font size: {self.default_font_size}")
        # Save font size to preferences
        self.save_current_font_sizes()
    
    def decrease_font_size(self):
        """Decrease font size (Ctrl+-)"""
        self.default_font_size = max(7, self.default_font_size - 1)
        self.apply_font_to_grid()
        self.auto_resize_rows()
        self.log(f"✓ Font size: {self.default_font_size}")
        # Save font size to preferences
        self.save_current_font_sizes()
    
    def on_font_changed(self):
        """Handle font change - legacy method for compatibility"""
        self.apply_font_to_grid()
        self.auto_resize_rows()

    
    def zoom_in(self):
        """Increase font size (same as Ctrl++)"""
        self.increase_font_size()
    
    def zoom_out(self):
        """Decrease font size (same as Ctrl+-)"""
        self.decrease_font_size()
    
    def results_pane_zoom_in(self):
        """Increase font size in translation results pane"""
        if hasattr(self, 'assistance_widget') and hasattr(self.assistance_widget, 'zoom_in'):
            self.assistance_widget.zoom_in()
            # Save font sizes to preferences
            self.save_current_font_sizes()
    
    def results_pane_zoom_out(self):
        """Decrease font size in translation results pane"""
        if hasattr(self, 'assistance_widget') and hasattr(self.assistance_widget, 'zoom_out'):
            self.assistance_widget.zoom_out()
            # Save font sizes to preferences
            self.save_current_font_sizes()
    
    def results_pane_zoom_reset(self):
        """Reset font size in translation results pane to default"""
        if hasattr(self, 'assistance_widget') and hasattr(self.assistance_widget, 'reset_zoom'):
            self.assistance_widget.reset_zoom()
            # Save font sizes to preferences
            self.save_current_font_sizes()
    
    def save_current_font_sizes(self):
        """Save current font sizes to preferences"""
        try:
            from modules.translation_results_panel import CompactMatchItem, TranslationResultsPanel
            general_settings = self.load_general_settings()
            general_settings['grid_font_size'] = self.default_font_size
            if hasattr(CompactMatchItem, 'font_size_pt'):
                general_settings['results_match_font_size'] = CompactMatchItem.font_size_pt
            if hasattr(TranslationResultsPanel, 'compare_box_font_size'):
                general_settings['results_compare_font_size'] = TranslationResultsPanel.compare_box_font_size
            # Preserve other settings
            if 'restore_last_project' not in general_settings:
                general_settings['restore_last_project'] = False
            self.save_general_settings(general_settings)
        except Exception as e:
            # Silently fail - don't interrupt user workflow
            pass
    
    def load_general_settings(self) -> Dict[str, Any]:
        """Load general settings from user preferences"""
        prefs_file = self.user_data_path / "ui_preferences.json"
        
        defaults = {
            'restore_last_project': False,
            'grid_font_size': 11,
            'results_match_font_size': 9,
            'results_compare_font_size': 9
        }
        
        if not prefs_file.exists():
            return defaults
        
        try:
            with open(prefs_file, 'r') as f:
                prefs = json.load(f)
                general = prefs.get('general_settings', {})
                # Merge with defaults to ensure all keys exist
                result = defaults.copy()
                result.update(general)
                return result
        except:
            return defaults
    
    def save_general_settings(self, settings: Dict[str, Any]):
        """Save general settings to user preferences"""
        prefs_file = self.user_data_path / "ui_preferences.json"
        
        # Load existing preferences
        prefs = {}
        if prefs_file.exists():
            try:
                with open(prefs_file, 'r') as f:
                    prefs = json.load(f)
            except:
                pass
        
        # Update general settings
        prefs['general_settings'] = settings
        
        # Save back
        try:
            with open(prefs_file, 'w') as f:
                json.dump(prefs, f, indent=2)
        except Exception as e:
            self.log(f"⚠ Could not save general settings: {str(e)}")
    
    def load_font_sizes_from_preferences(self):
        """Load and apply font sizes from preferences on startup"""
        try:
            general_settings = self.load_general_settings()
            
            # Load grid font size
            grid_size = general_settings.get('grid_font_size', 11)
            if 7 <= grid_size <= 72:
                self.default_font_size = grid_size
                if hasattr(self, 'table') and self.table is not None:
                    self.apply_font_to_grid()
            
            # Load results pane font sizes
            match_size = general_settings.get('results_match_font_size', 9)
            compare_size = general_settings.get('results_compare_font_size', 9)
            
            if hasattr(self, 'assistance_widget') and hasattr(self.assistance_widget, 'set_font_size'):
                if 7 <= match_size <= 16:
                    from modules.translation_results_panel import CompactMatchItem
                    CompactMatchItem.set_font_size(match_size)
                    self.assistance_widget.set_font_size(match_size)
            
            if hasattr(self, 'assistance_widget') and hasattr(self.assistance_widget, 'set_compare_box_font_size'):
                if 7 <= compare_size <= 14:
                    from modules.translation_results_panel import TranslationResultsPanel
                    TranslationResultsPanel.compare_box_font_size = compare_size
                    self.assistance_widget.set_compare_box_font_size(compare_size)
                    
        except Exception as e:
            self.log(f"⚠ Could not load font sizes: {e}")
    
    def restore_last_project_if_enabled(self):
        """Restore the last opened project on startup if the setting is enabled"""
        try:
            # Check if setting is enabled
            general_settings = self.load_general_settings()
            if not general_settings.get('restore_last_project', False):
                return
            
            # Get recent projects
            recent_projects = self.load_recent_projects()
            if not recent_projects:
                return
            
            # Get the most recent project (first in the list)
            # Recent projects are sorted by most recent first
            last_project = recent_projects[0]
            project_path = last_project.get('path') if isinstance(last_project, dict) else last_project
            
            # Verify file exists
            if not project_path or not os.path.exists(project_path):
                self.log(f"⚠ Last project file not found: {project_path}")
                return
            
            # Load the project
            self.log(f"🔄 Restoring last project: {Path(project_path).name}")
            self.load_project(project_path)
            
        except Exception as e:
            # Silently fail - don't block startup if restoration fails
            self.log(f"⚠ Could not restore last project: {e}")
    
    
    def get_status_icon(self, status: str) -> str:
        """Get status icon for display"""
        icons = {
            'untranslated': '⚪',
            'draft': '📝',
            'translated': '✅',
            'approved': '⭐'
        }
        return icons.get(status, '⚪')
    
    def update_status_icon(self, row: int, status: str):
        """Update status icon for a specific row"""
        status_icon = self.get_status_icon(status)
        status_item = QTableWidgetItem(status_icon)
        status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, 4, status_item)
    
    def on_cell_changed(self, item: QTableWidgetItem):
        """Handle cell edit"""
        if not self.current_project:
            return
        
        row = item.row()
        col = item.column()
        
        # Only Target column (3) is editable
        if col == 3 and row < len(self.current_project.segments):
            segment = self.current_project.segments[row]
            segment.target = item.text()
            
            # Update status if translation was added
            if segment.target and segment.status == 'untranslated':
                segment.status = 'draft'
                status_item = self.table.item(row, 4)
                if status_item:
                    status_item.setText(self.get_status_icon('draft'))
            
            self.project_modified = True
            self.update_window_title()
            
            # Auto-resize the edited row
            self.table.resizeRowToContents(row)
    
    def on_cell_selected(self, current_row, current_col, previous_row, previous_col):
        """Handle cell selection change"""
        try:
            # Clear previous highlighting
            if previous_row >= 0 and previous_row < self.table.rowCount():
                prev_id_item = self.table.item(previous_row, 0)
                if prev_id_item:
                    prev_id_item.setBackground(QColor())  # Reset background to default
                    prev_id_item.setForeground(QColor("black"))  # Reset text color to black
            
            # Highlight current segment number in orange (like memoQ)
            if current_row >= 0 and current_row < self.table.rowCount():
                current_id_item = self.table.item(current_row, 0)
                if current_id_item:
                    current_id_item.setBackground(QColor("#FFA500"))  # Orange background
                    current_id_item.setForeground(QColor("white"))    # White text for contrast
            
            if not self.current_project or current_row < 0:
                return
            
            if current_row < len(self.current_project.segments):
                segment = self.current_project.segments[current_row]
                
                # Update notes - check if using TranslationResultsPanel or fallback
                if hasattr(self.assistance_widget, 'notes_edit'):
                    try:
                        self.assistance_widget.notes_edit.setText(segment.notes)
                    except Exception as e:
                        self.log(f"Error updating notes: {e}")
                
                # Update TM matches
                try:
                    self.search_and_display_tm_matches(segment.source)
                except Exception as e:
                    self.log(f"Error searching TM: {e}")
                
                # Update TranslationResultsPanel if available
                if hasattr(self, 'assistance_widget') and hasattr(self.assistance_widget, 'set_segment_info'):
                    try:
                        self.assistance_widget.set_segment_info(current_row + 1, segment.source)
                        
                        # Generate matches dictionary for the panel
                        from modules.translation_results_panel import TranslationMatch
                        
                        matches_dict = {
                            "NT": [],      # No Translation
                            "MT": [],      # Machine Translation
                            "TM": [],      # Translation Memory
                            "Termbases": [] # Terminology
                        }
                        
                        # Generate sample matches from database if available
                        if self.tm_database:
                            try:
                                tm_matches = self.tm_database.search_all(segment.source, max_matches=10)
                                for match in tm_matches:
                                    match_obj = TranslationMatch(
                                        source=match.get('source', ''),
                                        target=match.get('target', ''),
                                        relevance=match.get('match_pct', 0),
                                        metadata={
                                            'context': match.get('context', ''),
                                            'tm_name': match.get('tm_name', ''),
                                            'timestamp': match.get('created_at', '')
                                        },
                                        match_type='TM',
                                        compare_source=match.get('source', '')
                                    )
                                    matches_dict["TM"].append(match_obj)
                            except Exception as e:
                                self.log(f"Error loading TM matches: {e}")
                        
                        # Add termbase matches to the results panel
                        try:
                            if hasattr(self, 'db_manager') and self.db_manager:
                                # Get termbase matches from the source item if available
                                source_item = self.table.item(current_row, 2)
                                if source_item and hasattr(source_item, 'termbase_matches'):
                                    termbase_matches = source_item.termbase_matches
                                    if termbase_matches:
                                        self.log(f"Adding {len(termbase_matches)} termbase matches to panel")
                                        for source_term, target_term in termbase_matches.items():
                                            match_obj = TranslationMatch(
                                                source=source_term,
                                                target=target_term,
                                                relevance=100,  # Exact matches from termbase
                                                metadata={
                                                    'context': 'Termbase match',
                                                    'tm_name': 'Termbase',
                                                    'timestamp': ''
                                                },
                                                match_type='Termbase',
                                                compare_source=source_term
                                            )
                                            matches_dict["Termbases"].append(match_obj)
                        except Exception as e:
                            self.log(f"Error adding termbase matches: {e}")
                        
                        self.assistance_widget.set_matches(matches_dict)
                    except Exception as e:
                        self.log(f"Error updating TranslationResultsPanel: {e}")
        except Exception as e:
            self.log(f"Critical error in on_cell_selected: {e}")
    
    
    def on_cell_clicked(self, item: QTableWidgetItem):
        """Handle cell click - allows toggling status by clicking Status column"""
        if not self.current_project:
            return
        
        row = item.row()
        col = item.column()
        
        # Status column (4) - click to cycle through statuses
        if col == 4 and row < len(self.current_project.segments):
            segment = self.current_project.segments[row]
            
            # Cycle through statuses: untranslated → draft → translated → approved → untranslated
            status_cycle = ['untranslated', 'draft', 'translated', 'approved']
            current_index = status_cycle.index(segment.status) if segment.status in status_cycle else 0
            next_status = status_cycle[(current_index + 1) % len(status_cycle)]
            
            segment.status = next_status
            item.setText(self.get_status_icon(next_status))
            
            self.project_modified = True
            self.update_window_title()
            self.log(f"Segment {row + 1} status: {next_status}")
    
    # ========================================================================
    # TRANSLATION MEMORY
    # ========================================================================
    
    def initialize_tm_database(self):
        """Initialize TM database when project is loaded"""
        if not self.current_project:
            return
        
        try:
            from modules.translation_memory import TMDatabase
            
            # Get database path
            db_path = self.user_data_path / "Translation_Resources" / "supervertaler.db"
            
            # Initialize TM database
            self.tm_database = TMDatabase(
                source_lang=self.current_project.source_lang,
                target_lang=self.current_project.target_lang,
                db_path=str(db_path),
                log_callback=self.log
            )
            
            # Update Universal Lookup tab with TM database
            if hasattr(self, 'lookup_tab') and self.lookup_tab:
                self.lookup_tab.set_tm_database(self.tm_database)
            
            self.log(f"TM database initialized ({self.current_project.source_lang} → {self.current_project.target_lang})")
        except Exception as e:
            self.log(f"Warning: Could not initialize TM database: {e}")
            self.tm_database = None
    
    def search_and_display_tm_matches(self, source_text: str):
        """Search TM and Termbases and display matches with visual diff for fuzzy matches"""
        if not source_text or not source_text.strip():
            if hasattr(self, 'tm_display'):
                self.tm_display.clear()
            return
        
        # Initialize TM if not already done
        if not self.tm_database and self.current_project:
            self.initialize_tm_database()
        
        if not self.tm_database:
            if hasattr(self, 'tm_display'):
                self.tm_display.setHtml(
                    "<p style='color: #999;'><i>Translation Memory not available</i></p>"
                )
            return
        
        try:
            # Search for matches
            matches = self.tm_database.search_all(source_text, max_matches=5)
            
            if not matches:
                if hasattr(self, 'tm_display'):
                    self.tm_display.setHtml(
                        f"<p style='color: #666;'><b>Source:</b> {source_text}</p>"
                        f"<p style='color: #999;'><i>No translation memory matches found</i></p>"
                    )
                return
            
            # If using TranslationResultsPanel, populate it with TM and Termbase results
            if hasattr(self.assistance_widget, 'set_matches'):
                try:
                    from modules.translation_results_panel import TranslationMatch
                    
                    # Convert TM matches
                    tm_matches = []
                    for match in matches:
                        tm_match = TranslationMatch(
                            source=match.get('source', ''),
                            target=match.get('target', ''),
                            relevance=int(match.get('match_pct', 0)),
                            metadata={
                                'tm_name': match.get('tm_name', 'Unknown TM'),
                                'context': match.get('context', '')
                            },
                            match_type='TM',
                            compare_source=match.get('source', '')
                        )
                        tm_matches.append(tm_match)
                    
                    # Search for termbase matches
                    termbase_matches = []
                    try:
                        if hasattr(self, 'db_manager') and self.db_manager:
                            # Get current project language pair
                            source_lang = None
                            target_lang = None
                            project_id = None
                            
                            if self.current_project:
                                # current_project is a Project object, not a dict
                                project_id = self.current_project.id if hasattr(self.current_project, 'id') else None
                                source_lang = self.current_project.source_lang if hasattr(self.current_project, 'source_lang') else None
                                target_lang = self.current_project.target_lang if hasattr(self.current_project, 'target_lang') else None
                            
                            # Search for individual words in the source text
                            words = source_text.split()
                            searched_terms = set()  # Track what we've already searched
                            
                            for word in words:
                                # Remove punctuation
                                clean_word = word.strip('.,!?;:')
                                if len(clean_word) < 2 or clean_word in searched_terms:
                                    continue
                                
                                searched_terms.add(clean_word)
                                
                                # Search termbases for this word
                                tb_results = self.db_manager.search_termbases(
                                    clean_word,
                                    source_lang=source_lang,
                                    target_lang=target_lang,
                                    project_id=project_id,
                                    min_length=2
                                )
                                
                                # Convert termbase results to TranslationMatch objects
                                for tb_match in tb_results:
                                    termbase_match = TranslationMatch(
                                        source=tb_match.get('source_term', ''),
                                        target=tb_match.get('target_term', ''),
                                        relevance=100 - tb_match.get('priority', 99),  # Lower priority = higher relevance
                                        metadata={
                                            'termbase_id': tb_match.get('termbase_id'),
                                            'priority': tb_match.get('priority', 99),
                                            'definition': tb_match.get('definition', ''),
                                            'domain': tb_match.get('domain', ''),
                                            'forbidden': tb_match.get('forbidden', False)
                                        },
                                        match_type='Termbase',
                                        compare_source=tb_match.get('source_term', '')
                                    )
                                    termbase_matches.append(termbase_match)
                    except Exception as e:
                        self.log(f"Error searching termbases: {e}")

                    
                    # Update the panel with both TM and Termbase matches
                    matches_dict = {}
                    if tm_matches:
                        matches_dict['TM'] = tm_matches
                    if termbase_matches:
                        matches_dict['Termbases'] = termbase_matches
                    
                    if matches_dict:
                        self.assistance_widget.set_matches(matches_dict)
                    return
                except Exception as e:
                    self.log(f"Error populating TranslationResultsPanel: {e}")
            
            # Fallback: display in tm_display if it exists
            if not hasattr(self, 'tm_display'):
                return
            
            # Build HTML display with diff highlighting
            html = f"<div style='font-family: {self.default_font_family}; font-size: {self.default_font_size}pt;'>"
            html += f"<p style='color: #666; margin-bottom: 10px;'><b>🔍 Searching for:</b><br>{source_text}</p>"
            html += "<hr style='border: 1px solid #ddd;'>"
            
            for idx, match in enumerate(matches, start=1):
                match_pct = match.get('match_pct', 0)
                tm_name = match.get('tm_name', 'Unknown TM')
                source_match = match.get('source', '')
                target_match = match.get('target', '')
                
                # Color based on match percentage
                if match_pct == 100:
                    color = "#22c55e"  # Green for exact match
                    badge_style = "background-color: #22c55e; color: white;"
                elif match_pct >= 95:
                    color = "#3b82f6"  # Blue for high match
                    badge_style = "background-color: #3b82f6; color: white;"
                elif match_pct >= 85:
                    color = "#f59e0b"  # Orange for medium match
                    badge_style = "background-color: #f59e0b; color: white;"
                else:
                    color = "#ef4444"  # Red for low match
                    badge_style = "background-color: #ef4444; color: white;"
                
                html += f"<div style='margin: 10px 0; padding: 10px; background-color: #f9fafb; border-left: 4px solid {color}; border-radius: 4px;'>"
                html += f"<div style='margin-bottom: 5px;'>"
                html += f"<span style='padding: 2px 8px; border-radius: 3px; font-weight: bold; font-size: 10pt; {badge_style}'>{match_pct}%</span> "
                html += f"<span style='color: #666; font-size: 9pt;'>{tm_name}</span>"
                html += "</div>"
                
                # Display source with diff if not 100% match
                if match_pct < 100:
                    diff_html = self.create_diff_html(source_text, source_match)
                    html += f"<p style='margin: 5px 0; color: #444;'><b>TM Source:</b><br>{diff_html}</p>"
                else:
                    html += f"<p style='margin: 5px 0; color: #444;'><b>TM Source:</b><br>{source_match}</p>"
                
                # Display target (clickable to insert)
                html += f"<p style='margin: 5px 0; color: #059669; font-weight: bold;'><b>TM Target:</b><br>"
                html += f"<span style='cursor: pointer; text-decoration: underline;' "
                html += f"onclick='alert(\"{target_match}\")'>{target_match}</span></p>"
                html += "</div>"
            
            html += "</div>"
            self.tm_display.setHtml(html)
            
        except Exception as e:
            self.log(f"Error searching TM: {e}")
            if hasattr(self, 'tm_display'):
                self.tm_display.setHtml(
                    f"<p style='color: #ef4444;'><b>Error:</b> {e}</p>"
                )
    
    def create_diff_html(self, current_text: str, tm_text: str) -> str:
        """Create HTML with visual diff highlighting between current and TM source
        
        Shows changes inline like memoQ:
        - Red strikethrough for deleted text (in TM but not in current)
        - Green underline + bold for added text (in current but not in TM)
        - Sequential display: deletions then additions in order
        """
        from difflib import SequenceMatcher
        
        s = SequenceMatcher(None, tm_text, current_text)
        html_parts = []
        
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            tm_chunk = tm_text[i1:i2]
            current_chunk = current_text[j1:j2]
            
            if tag == 'equal':
                # Matching text - show normally
                html_parts.append(tm_chunk)
            elif tag == 'delete':
                # Text removed from TM - show with red strikethrough (like memoQ deletion)
                html_parts.append(f'<span style="color: #dc2626; text-decoration: line-through;">{tm_chunk}</span>')
            elif tag == 'insert':
                # Text added in current - show with green underline + bold (like memoQ insertion)
                html_parts.append(f'<span style="color: #22c55e; text-decoration: underline; font-weight: bold;">{current_chunk}</span>')
            elif tag == 'replace':
                # Text changed - show deletion (strikethrough) followed by insertion (underline)
                # This matches memoQ's behavior: old text strikethrough, new text underlined
                html_parts.append(f'<span style="color: #dc2626; text-decoration: line-through;">{tm_chunk}</span>')
                html_parts.append(' ')  # Add space between deletion and insertion
                html_parts.append(f'<span style="color: #22c55e; text-decoration: underline; font-weight: bold;">{current_chunk}</span>')
        
        return ''.join(html_parts)
    
    # ========================================================================
    # TERMBASE HIGHLIGHTING & MATCHING
    # ========================================================================
    
    def find_termbase_matches_in_source(self, source_text: str) -> Dict[str, str]:
        """
        Find all termbase matches in source text
        Returns dict of {term: translation} for all matches found
        """
        if not source_text or not hasattr(self, 'db_manager') or not self.db_manager:
            return {}
        
        try:
            source_lang = self.current_project.source_lang if self.current_project else None
            target_lang = self.current_project.target_lang if self.current_project else None
            
            # Debug logging
            self.log(f"🔍 Searching termbases for: '{source_text}' ({source_lang} → {target_lang})")
            
            # First, check if we have any termbases at all
            query = "SELECT COUNT(*) FROM termbase_terms"
            self.db_manager.cursor.execute(query)
            total_terms = self.db_manager.cursor.fetchone()[0]
            self.log(f"  Total terms in database: {total_terms}")
            
            if total_terms == 0:
                self.log(f"  ⚠️  No termbases loaded in database")
                return {}
            
            # Search termbases for all terms that appear in the source text
            # Split source text into words and search for each one
            words = source_text.split()
            matches = {}
            
            for word in words:
                # Remove punctuation and search
                clean_word = word.strip('.,!?;:')
                if len(clean_word) < 2:  # Skip short words
                    continue
                
                termbase_results = self.db_manager.search_termbases(
                    clean_word,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    min_length=2
                )
                
                if termbase_results:
                    self.log(f"  ✓ Found {len(termbase_results)} match(es) for '{clean_word}'")
                    for result in termbase_results:
                        source_term = result.get('source_term', '').strip()
                        target_term = result.get('target_term', '').strip()
                        if source_term and target_term:
                            matches[source_term] = target_term
                            self.log(f"    → {source_term} = {target_term}")
            
            self.log(f"🔍 Total unique matches: {len(matches)}")
            return matches
            
        except Exception as e:
            self.log(f"❌ Error finding termbase matches: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
            return {}
    
    def highlight_source_with_termbase(self, row: int, source_text: str):
        """
        Highlight termbase matches in the source column of the grid
        Creates a custom widget with clickable term highlights
        """
        if not self.table or row < 0:
            return
        
        try:
            # Find termbase matches
            termbase_matches = self.find_termbase_matches_in_source(source_text)
            
            if not termbase_matches:
                # No matches - display plain text
                return
            
            # Create highlighted widget
            widget = TermbaseHighlightWidget(source_text, termbase_matches, parent=self.table)
            
            # Store reference to insert translation on double-click
            def on_term_clicked(term, translation):
                self.insert_term_translation(row, translation)
            
            widget.term_double_clicked = on_term_clicked
            
            # Set the widget in the source column (column 2)
            self.table.setCellWidget(row, 2, widget)
            
        except Exception as e:
            self.log(f"Error highlighting termbase matches: {e}")
    
    def insert_term_translation(self, row: int, translation: str):
        """
        Double-click handler: insert termbase translation into target cell
        """
        if not self.table or row < 0 or row >= len(self.current_project.segments):
            return
        
        try:
            # Get the target cell
            target_item = self.table.item(row, 3)
            if not target_item:
                return
            
            # Insert translation
            segment = self.current_project.segments[row]
            segment.target = translation
            target_item.setText(translation)
            
            # Update status
            if segment.status == 'untranslated':
                segment.status = 'draft'
                self.update_status_icon(row, 'draft')
            
            self.project_modified = True
            self.update_window_title()
            self.log(f"✓ Term translation inserted in segment {row + 1}")
            
        except Exception as e:
            self.log(f"Error inserting term translation: {e}")
    
    # ========================================================================
    # NAVIGATION & SEARCH
    # ========================================================================
    
    def show_find_replace_dialog(self):
        """Show unified Find & Replace dialog (Ctrl+F and Ctrl+H both open same dialog)
        Filters grid to show only matching segments, like filter boxes.
        """
        if not self.current_project or not self.current_project.segments:
            QMessageBox.information(self, "No Project", "Please open a project first.")
            return
        
        from PyQt6.QtWidgets import QCheckBox, QGroupBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Find and Replace")
        dialog.setMinimumWidth(700)
        dialog.setMinimumHeight(450)
        
        # Main horizontal layout - left side (options) and right side (buttons)
        main_layout = QHBoxLayout(dialog)
        
        # Left side - all options
        left_layout = QVBoxLayout()
        
        # Left side - all options
        left_layout = QVBoxLayout()
        
        # Find what
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find what:"))
        self.find_input = QLineEdit()
        find_layout.addWidget(self.find_input, stretch=1)
        left_layout.addLayout(find_layout)
        
        # Replace with
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace with:"))
        self.replace_input = QLineEdit()
        replace_layout.addWidget(self.replace_input, stretch=1)
        left_layout.addLayout(replace_layout)
        
        # Search in options
        search_in_group = QGroupBox("Search in")
        search_in_layout = QVBoxLayout()
        
        self.search_source_cb = QCheckBox("Source text")
        self.search_target_cb = QCheckBox("Target text")
        self.search_target_cb.setChecked(True)  # Default to target
        
        search_in_layout.addWidget(self.search_source_cb)
        search_in_layout.addWidget(self.search_target_cb)
        search_in_group.setLayout(search_in_layout)
        left_layout.addWidget(search_in_group)
        
        # Match options
        match_group = QGroupBox("Match")
        match_layout = QVBoxLayout()
        
        self.match_group = QButtonGroup(dialog)
        match_anything = QRadioButton("Anything")
        match_anything.setChecked(True)
        match_whole_words = QRadioButton("Only whole words")
        match_entire = QRadioButton("Entire segment")
        
        self.match_group.addButton(match_anything, 0)
        self.match_group.addButton(match_whole_words, 1)
        self.match_group.addButton(match_entire, 2)
        
        match_layout.addWidget(match_anything)
        match_layout.addWidget(match_whole_words)
        match_layout.addWidget(match_entire)
        
        self.case_sensitive_cb = QCheckBox("Case sensitive")
        match_layout.addWidget(self.case_sensitive_cb)
        
        match_group.setLayout(match_layout)
        left_layout.addWidget(match_group)
        
        left_layout.addStretch()
        
        # Right side - buttons
        right_layout = QVBoxLayout()
        
        find_next_btn = QPushButton("Find next")
        find_next_btn.setMinimumWidth(150)
        find_next_btn.clicked.connect(lambda: self.find_next_match())
        right_layout.addWidget(find_next_btn)
        
        find_all_btn = QPushButton("Find all")
        find_all_btn.setMinimumWidth(150)
        find_all_btn.clicked.connect(lambda: self.find_all_matches())
        right_layout.addWidget(find_all_btn)
        
        # Replace buttons
        right_layout.addSpacing(10)
        
        replace_this_btn = QPushButton("Replace this")
        replace_this_btn.setMinimumWidth(150)
        replace_this_btn.clicked.connect(lambda: self.replace_current_match())
        right_layout.addWidget(replace_this_btn)
        
        replace_all_btn = QPushButton("Replace all")
        replace_all_btn.setMinimumWidth(150)
        replace_all_btn.clicked.connect(lambda: self.replace_all_matches())
        right_layout.addWidget(replace_all_btn)
        
        right_layout.addSpacing(10)
        
        highlight_all_btn = QPushButton("Highlight all")
        highlight_all_btn.setMinimumWidth(150)
        highlight_all_btn.clicked.connect(lambda: self.highlight_all_matches())
        right_layout.addWidget(highlight_all_btn)
        
        clear_highlight_btn = QPushButton("Clear highlighting")
        clear_highlight_btn.setMinimumWidth(150)
        clear_highlight_btn.clicked.connect(lambda: self.clear_search_highlights())
        right_layout.addWidget(clear_highlight_btn)
        
        right_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setMinimumWidth(150)
        close_btn.clicked.connect(dialog.close)
        right_layout.addWidget(close_btn)
        
        # Add left and right to main layout
        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addLayout(right_layout, stretch=1)
        
        # Store dialog reference and show
        self.find_replace_dialog = dialog
        self.current_match_index = -1
        self.find_matches = []
        
        dialog.show()
    
    def find_next_match(self):
        """Find next occurrence of search term, filtering grid to show only matching rows"""
        find_text = self.find_input.text()
        if not find_text:
            return
        
        search_source = self.search_source_cb.isChecked()
        search_target = self.search_target_cb.isChecked()
        case_sensitive = self.case_sensitive_cb.isChecked()
        match_mode = self.match_group.checkedId()
        
        # Find all matches if not already done
        if not self.find_matches:
            self.find_all_matches_internal(find_text, search_source, search_target, case_sensitive, match_mode)
            
            if self.find_matches:
                # First search - reload grid and filter rows
                self.load_segments_to_grid()
                
                # Get unique rows that have matches
                matching_rows = set(row for row, col in self.find_matches)
                
                # Hide all non-matching rows
                for row in range(len(self.current_project.segments)):
                    self.table.setRowHidden(row, row not in matching_rows)
        
        if not self.find_matches:
            QMessageBox.information(self.find_replace_dialog, "Find", "No matches found.")
            return
        
        # Move to next match
        self.current_match_index = (self.current_match_index + 1) % len(self.find_matches)
        row, col = self.find_matches[self.current_match_index]
        
        # Highlight the search term in the matched cell
        segment = self.current_project.segments[row]
        text = segment.source if col == 2 else segment.target
        self.highlight_search_term(row, col, text, find_text)
        
        self.table.setCurrentCell(row, col)
        self.table.scrollToItem(self.table.item(row, col))
        self.log(f"Match {self.current_match_index + 1} of {len(self.find_matches)}")
    
    def find_all_matches(self):
        """Find and highlight all matches, filtering grid to show only matching rows"""
        find_text = self.find_input.text()
        if not find_text:
            return
        
        search_source = self.search_source_cb.isChecked()
        search_target = self.search_target_cb.isChecked()
        case_sensitive = self.case_sensitive_cb.isChecked()
        match_mode = self.match_group.checkedId()
        
        self.find_all_matches_internal(find_text, search_source, search_target, case_sensitive, match_mode)
        
        if self.find_matches:
            # First, reload grid to clear previous highlights
            self.load_segments_to_grid()
            
            # Get unique rows that have matches
            matching_rows = set(row for row, col in self.find_matches)
            
            # Hide all non-matching rows (like filter boxes do)
            for row in range(len(self.current_project.segments)):
                self.table.setRowHidden(row, row not in matching_rows)
            
            # Highlight all matches with yellow
            for row, col in self.find_matches:
                segment = self.current_project.segments[row]
                text = segment.source if col == 2 else segment.target
                self.highlight_search_term(row, col, text, find_text)
            
            # Jump to first match
            first_row, first_col = self.find_matches[0]
            self.table.setCurrentCell(first_row, first_col)
            self.table.scrollToItem(self.table.item(first_row, first_col))
            self.current_match_index = 0
            
            self.log(f"Found {len(self.find_matches)} match(es) in {len(matching_rows)} segment(s)")
        else:
            QMessageBox.information(self.find_replace_dialog, "Find", "No matches found.")
    
    def find_all_matches_internal(self, find_text, search_source, search_target, case_sensitive, match_mode):
        """Internal method to find all matches"""
        import re
        
        self.find_matches = []
        
        for row, segment in enumerate(self.current_project.segments):
            texts_to_search = []
            if search_source:
                texts_to_search.append((segment.source, 2))
            if search_target:
                texts_to_search.append((segment.target, 3))
            
            for text, col in texts_to_search:
                if self.text_matches(text, find_text, case_sensitive, match_mode):
                    self.find_matches.append((row, col))
    
    def text_matches(self, text, find_text, case_sensitive, match_mode):
        """Check if text matches search criteria"""
        import re
        
        if match_mode == 2:  # Entire segment
            if case_sensitive:
                return text == find_text
            else:
                return text.lower() == find_text.lower()
        
        elif match_mode == 1:  # Whole words
            if case_sensitive:
                pattern = r'\b' + re.escape(find_text) + r'\b'
                return bool(re.search(pattern, text))
            else:
                pattern = r'\b' + re.escape(find_text) + r'\b'
                return bool(re.search(pattern, text, re.IGNORECASE))
        
        else:  # Anything (0)
            if case_sensitive:
                return find_text in text
            else:
                return find_text.lower() in text.lower()
    
    def replace_current_match(self):
        """Replace the currently selected match"""
        if self.current_match_index < 0 or self.current_match_index >= len(self.find_matches):
            QMessageBox.information(self.find_replace_dialog, "Replace", "No match selected. Use 'Find next' first.")
            return
        
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        row, col = self.find_matches[self.current_match_index]
        
        # Safety check: prevent replacing in source if disabled
        if col == 2 and not self.allow_replace_in_source:  # Source column
            QMessageBox.warning(
                self.find_replace_dialog,
                "Replace in Source Disabled",
                "Replacing in source text is disabled for safety.\n\n"
                "To enable this feature, go to Tools > Options and check 'Allow Replace in Source Text'."
            )
            return
        
        segment = self.current_project.segments[row]
        case_sensitive = self.case_sensitive_cb.isChecked()
        match_mode = self.match_group.checkedId()
        
        # Determine which field to update
        if col == 2:  # Source column
            field_text = segment.source
        else:  # col == 3, Target column
            field_text = segment.target
        
        if match_mode == 2:  # Entire segment
            new_text = replace_text
        else:
            # Replace using the appropriate method
            if case_sensitive:
                new_text = field_text.replace(find_text, replace_text, 1)
            else:
                import re
                pattern = re.escape(find_text)
                new_text = re.sub(pattern, replace_text, field_text, count=1, flags=re.IGNORECASE)
        
        # Update the appropriate field
        if col == 2:
            segment.source = new_text
        else:
            segment.target = new_text
        
        # Update table
        item = self.table.item(row, col)
        if item:
            item.setText(segment.target)
        
        self.project_modified = True
        self.update_window_title()
        
        # Refresh matches
        self.find_matches = []
        self.find_next_match()
    
    def replace_all_matches(self):
        """Replace all matches in target segments"""
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        
        if not find_text:
            return
        
        search_source = self.search_source_cb.isChecked()
        search_target = self.search_target_cb.isChecked()
        case_sensitive = self.case_sensitive_cb.isChecked()
        match_mode = self.match_group.checkedId()
        
        # Safety check: warn if trying to replace in source when disabled
        if search_source and not self.allow_replace_in_source:
            reply = QMessageBox.warning(
                self.find_replace_dialog,
                "Replace in Source Disabled",
                "Replacing in source text is disabled for safety.\n\n"
                "Only target text will be replaced.\n\n"
                "To enable replacing in source, go to Tools > Options and check 'Allow Replace in Source Text'.",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Cancel:
                return
            # Continue with target only
            search_source = False
            if not search_target:
                return
        
        # Find all matches
        self.find_all_matches_internal(find_text, search_source, search_target, case_sensitive, match_mode)
        
        if not self.find_matches:
            QMessageBox.information(self.find_replace_dialog, "Replace All", "No matches found.")
            return
        
        # Count matches by column
        source_count = sum(1 for _, col in self.find_matches if col == 2)
        target_count = sum(1 for _, col in self.find_matches if col == 3)
        
        # Filter out source matches if not allowed
        if not self.allow_replace_in_source:
            self.find_matches = [(row, col) for row, col in self.find_matches if col == 3]
            if not self.find_matches:
                QMessageBox.information(self.find_replace_dialog, "Replace All", "No matches found in Target column.")
                return
        
        # Build confirmation message
        msg_parts = []
        if source_count > 0 and self.allow_replace_in_source:
            msg_parts.append(f"{source_count} in source")
        if target_count > 0:
            msg_parts.append(f"{target_count} in target")
        
        confirmation_msg = f"Replace {len(self.find_matches)} occurrence(s) of '{find_text}' with '{replace_text}'?\n\n"
        if msg_parts:
            confirmation_msg += f"({', '.join(msg_parts)})"
        
        # Extra warning if replacing in source
        if source_count > 0 and self.allow_replace_in_source:
            confirmation_msg += "\n\n⚠️ WARNING: This will modify source text!"
        
        # Confirm
        reply = QMessageBox.question(
            self.find_replace_dialog,
            "Replace All",
            confirmation_msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Perform replacements
        import re
        replaced_count = 0
        
        for row, col in self.find_matches:
            segment = self.current_project.segments[row]
            
            # Get the appropriate field
            if col == 2:  # Source
                old_text = segment.source
            else:  # col == 3, Target
                old_text = segment.target
            
            # Perform replacement
            if match_mode == 2:  # Entire segment
                new_text = replace_text
            else:
                if case_sensitive:
                    new_text = old_text.replace(find_text, replace_text)
                else:
                    pattern = re.escape(find_text)
                    new_text = re.sub(pattern, replace_text, old_text, flags=re.IGNORECASE)
            
            if new_text != old_text:
                replaced_count += 1
                # Update the appropriate field
                if col == 2:
                    segment.source = new_text
                else:
                    segment.target = new_text
                
                # Update table
                item = self.table.item(row, col)
                if item:
                    item.setText(new_text)
        
        self.project_modified = True
        self.update_window_title()
        
        # Clear matches and reload
        self.find_matches = []
        self.load_segments_to_grid()
        
        QMessageBox.information(self.find_replace_dialog, "Replace All", f"Replaced {replaced_count} occurrence(s).")
        self.log(f"✓ Replaced {replaced_count} occurrence(s) of '{find_text}'")
    
    def highlight_all_matches(self):
        """Highlight all matches using the filter system"""
        find_text = self.find_input.text()
        if not find_text:
            return
        
        search_source = self.search_source_cb.isChecked()
        search_target = self.search_target_cb.isChecked()
        
        # Use filter boxes to highlight
        if search_source:
            self.source_filter.setText(find_text)
        else:
            self.source_filter.clear()
        
        if search_target:
            self.target_filter.setText(find_text)
        else:
            self.target_filter.clear()
    
    def clear_search_highlights(self):
        """Clear all search highlights and unhide all rows (for Find & Replace dialog)"""
        self.load_segments_to_grid()
        
        # Unhide all rows
        for row in range(self.table.rowCount()):
            self.table.setRowHidden(row, False)
        
        self.find_matches = []
        self.current_match_index = -1
        self.log("Search highlights cleared")
    
    def show_goto_dialog(self):
        """Show dialog to jump to a specific segment"""
        if not self.current_project or not self.current_project.segments:
            QMessageBox.information(self, "No Project", "Please open a project first.")
            return
        
        max_segment = len(self.current_project.segments)
        segment_num, ok = QInputDialog.getInt(
            self,
            "Go to Segment",
            f"Enter segment number (1-{max_segment}):",
            value=self.table.currentRow() + 1,
            min=1,
            max=max_segment
        )
        
        if ok:
            row = segment_num - 1
            self.table.setCurrentCell(row, 3)  # Jump to Target column
            self.table.scrollToItem(self.table.item(row, 3))
            self.log(f"Jumped to segment {segment_num}")
    
    def show_search_dialog(self):
        """Show enhanced search dialog with source/target options"""
        if not self.current_project or not self.current_project.segments:
            QMessageBox.information(self, "No Project", "Please open a project first.")
            return
        
        from PyQt6.QtWidgets import QDialog, QLineEdit, QRadioButton, QButtonGroup, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Find in Segments")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Search text input
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search for:"))
        search_input = QLineEdit()
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)
        
        # Search scope options
        scope_label = QLabel("Search in:")
        layout.addWidget(scope_label)
        
        radio_layout = QHBoxLayout()
        search_scope_group = QButtonGroup(dialog)
        
        both_radio = QRadioButton("Both Source and Target")
        both_radio.setChecked(True)
        source_radio = QRadioButton("Source only")
        target_radio = QRadioButton("Target only")
        
        search_scope_group.addButton(both_radio, 0)
        search_scope_group.addButton(source_radio, 1)
        search_scope_group.addButton(target_radio, 2)
        
        radio_layout.addWidget(both_radio)
        radio_layout.addWidget(source_radio)
        radio_layout.addWidget(target_radio)
        layout.addLayout(radio_layout)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        # Show dialog and process
        if dialog.exec() == QDialog.DialogCode.Accepted:
            search_text = search_input.text()
            if search_text:
                scope = search_scope_group.checkedId()
                self.search_segments(search_text, scope)
    
    def search_segments(self, search_text: str, scope: int = 0):
        """Search for text in segments and highlight ONLY the exact search term
        
        Args:
            search_text: Text to search for
            scope: 0=both, 1=source only, 2=target only
        """
        if not self.current_project:
            return
        
        # Populate filter boxes based on scope
        if scope == 0:  # Both
            self.source_filter.setText(search_text)
            self.target_filter.setText(search_text)
        elif scope == 1:  # Source only
            self.source_filter.setText(search_text)
            self.target_filter.clear()
        elif scope == 2:  # Target only
            self.source_filter.clear()
            self.target_filter.setText(search_text)
        
        # The filter boxes will trigger apply_filters() automatically
        # which handles highlighting and hiding
        
        # Find first match and jump to it
        search_lower = search_text.lower()
        for row, segment in enumerate(self.current_project.segments):
            source_match = scope != 2 and search_lower in segment.source.lower()
            target_match = scope != 1 and search_lower in segment.target.lower()
            
            if source_match or target_match:
                self.table.setCurrentCell(row, 3)
                self.table.scrollToItem(self.table.item(row, 3))
                break
    
    def highlight_search_term(self, row: int, col: int, text: str, search_term: str):
        """Highlight only the search term within the cell text using HTML"""
        # Create a custom widget with HTML formatting
        label = QLabel()
        label.setWordWrap(True)
        label.setTextFormat(Qt.TextFormat.RichText)
        
        # Build HTML with highlighted search term (case-insensitive)
        search_lower = search_term.lower()
        text_lower = text.lower()
        
        # Find all occurrences and build highlighted HTML
        html_text = ""
        last_pos = 0
        
        while True:
            pos = text_lower.find(search_lower, last_pos)
            if pos == -1:
                # Add remaining text
                html_text += text[last_pos:]
                break
            
            # Add text before match
            html_text += text[last_pos:pos]
            # Add highlighted match
            html_text += f'<span style="background-color: yellow;">{text[pos:pos+len(search_term)]}</span>'
            last_pos = pos + len(search_term)
        
        label.setText(html_text)
        self.table.setCellWidget(row, col, label)
    
    def apply_filters(self):
        """Apply source and target filters to show/hide rows and highlight matches"""
        if not self.current_project:
            return
        
        source_filter_text = self.source_filter.text().strip()
        target_filter_text = self.target_filter.text().strip()
        
        # If both empty, clear everything
        if not source_filter_text and not target_filter_text:
            self.clear_filters()
            return
        
        # Clear previous highlights by reloading
        self.load_segments_to_grid()
        
        visible_count = 0
        
        for row, segment in enumerate(self.current_project.segments):
            source_match = not source_filter_text or source_filter_text.lower() in segment.source.lower()
            target_match = not target_filter_text or target_filter_text.lower() in segment.target.lower()
            
            show_row = source_match and target_match
            
            # Hide/show row
            self.table.setRowHidden(row, not show_row)
            
            if show_row:
                visible_count += 1
                
                # Highlight matching terms
                if source_filter_text and source_filter_text.lower() in segment.source.lower():
                    self.highlight_search_term(row, 2, segment.source, source_filter_text)
                
                if target_filter_text and target_filter_text.lower() in segment.target.lower():
                    self.highlight_search_term(row, 3, segment.target, target_filter_text)
        
        # Update status
        if source_filter_text or target_filter_text:
            self.log(f"Filter applied: showing {visible_count} of {len(self.current_project.segments)} segments")
    
    def clear_filters(self):
        """Clear all filter boxes, highlighting, and show all rows"""
        # Block signals to prevent recursion
        self.source_filter.blockSignals(True)
        self.target_filter.blockSignals(True)
        
        self.source_filter.clear()
        self.target_filter.clear()
        
        # Re-enable signals
        self.source_filter.blockSignals(False)
        self.target_filter.blockSignals(False)
        
        # Reload grid to remove all highlighting
        if self.current_project:
            self.load_segments_to_grid()
            
            # Explicitly show all rows (unhide them)
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)
        
        self.log("Filters cleared")
    
    # ========================================================================
    # UTILITY
    # ========================================================================
    
    def update_window_title(self):
        """Update window title with project name and modified state"""
        title = "Supervertaler Qt v1.1.2"
        if ENABLE_PRIVATE_FEATURES:
            title += " [🛠️ DEV MODE]"
        if self.current_project:
            title += f" - {self.current_project.name}"
            if self.project_modified:
                title += " *"
        self.setWindowTitle(title)
    
    def log(self, message: str):
        """Log message to status bar"""
        if hasattr(self, 'status_bar'):
            self.status_bar.showMessage(message)
        print(f"[LOG] {message}")
    
    def show_options_dialog(self):
        """Show application options dialog with LLM settings"""
        from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setMinimumWidth(650)
        dialog.setMinimumHeight(500)
        
        layout = QVBoxLayout(dialog)
        
        # Create tabs for different settings categories
        tabs = QTabWidget()
        
        # ===== TAB 1: LLM Settings =====
        llm_tab = QWidget()
        llm_layout = QVBoxLayout(llm_tab)
        
        # LLM Provider Selection
        provider_group = QGroupBox("LLM Provider")
        provider_layout = QVBoxLayout()
        
        provider_label = QLabel("Select your preferred translation provider:")
        provider_layout.addWidget(provider_label)
        
        # Load current settings
        settings = self.load_llm_settings()
        
        # Provider radio buttons
        provider_button_group = QButtonGroup(dialog)
        
        openai_radio = QRadioButton("OpenAI (GPT-4o, GPT-5, o1, o3)")
        openai_radio.setChecked(settings.get('provider', 'openai') == 'openai')
        provider_button_group.addButton(openai_radio)
        provider_layout.addWidget(openai_radio)
        
        claude_radio = QRadioButton("Anthropic Claude (Claude 3.5 Sonnet)")
        claude_radio.setChecked(settings.get('provider', 'openai') == 'claude')
        provider_button_group.addButton(claude_radio)
        provider_layout.addWidget(claude_radio)
        
        gemini_radio = QRadioButton("Google Gemini (Gemini 2.0 Flash)")
        gemini_radio.setChecked(settings.get('provider', 'openai') == 'gemini')
        provider_button_group.addButton(gemini_radio)
        provider_layout.addWidget(gemini_radio)
        
        provider_group.setLayout(provider_layout)
        llm_layout.addWidget(provider_group)
        
        # Model Selection
        model_group = QGroupBox("Model Selection")
        model_layout = QVBoxLayout()
        
        model_label = QLabel("Choose the specific model to use:")
        model_layout.addWidget(model_label)
        
        # OpenAI models
        openai_model_label = QLabel("<b>OpenAI Models:</b>")
        model_layout.addWidget(openai_model_label)
        
        openai_combo = QComboBox()
        openai_combo.addItems([
            "gpt-4o (Recommended)",
            "gpt-4o-mini (Fast & Economical)",
            "gpt-5 (Reasoning, Temperature 1.0)",
            "o3-mini (Reasoning, Temperature 1.0)",
            "o1 (Reasoning, Temperature 1.0)",
            "gpt-4-turbo"
        ])
        # Set current selection
        current_openai_model = settings.get('openai_model', 'gpt-4o')
        for i in range(openai_combo.count()):
            if current_openai_model in openai_combo.itemText(i).lower():
                openai_combo.setCurrentIndex(i)
                break
        openai_combo.setEnabled(openai_radio.isChecked())
        model_layout.addWidget(openai_combo)
        
        model_layout.addSpacing(10)
        
        # Claude models
        claude_model_label = QLabel("<b>Claude Models:</b>")
        model_layout.addWidget(claude_model_label)
        
        claude_combo = QComboBox()
        claude_combo.addItems([
            "claude-3-5-sonnet-20241022 (Recommended)",
            "claude-3-5-haiku-20241022 (Fast)",
            "claude-3-opus-20240229 (Powerful)"
        ])
        current_claude_model = settings.get('claude_model', 'claude-3-5-sonnet-20241022')
        for i in range(claude_combo.count()):
            if current_claude_model in claude_combo.itemText(i):
                claude_combo.setCurrentIndex(i)
                break
        claude_combo.setEnabled(claude_radio.isChecked())
        model_layout.addWidget(claude_combo)
        
        model_layout.addSpacing(10)
        
        # Gemini models
        gemini_model_label = QLabel("<b>Gemini Models:</b>")
        model_layout.addWidget(gemini_model_label)
        
        gemini_combo = QComboBox()
        gemini_combo.addItems([
            "gemini-2.0-flash-exp (Recommended)",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ])
        current_gemini_model = settings.get('gemini_model', 'gemini-2.0-flash-exp')
        for i in range(gemini_combo.count()):
            if current_gemini_model in gemini_combo.itemText(i):
                gemini_combo.setCurrentIndex(i)
                break
        gemini_combo.setEnabled(gemini_radio.isChecked())
        model_layout.addWidget(gemini_combo)
        
        model_group.setLayout(model_layout)
        llm_layout.addWidget(model_group)
        
        # Connect radio buttons to enable/disable combos
        def update_combo_states():
            openai_combo.setEnabled(openai_radio.isChecked())
            claude_combo.setEnabled(claude_radio.isChecked())
            gemini_combo.setEnabled(gemini_radio.isChecked())
        
        openai_radio.toggled.connect(update_combo_states)
        claude_radio.toggled.connect(update_combo_states)
        gemini_radio.toggled.connect(update_combo_states)
        
        # API Keys info
        api_keys_group = QGroupBox("API Keys")
        api_keys_layout = QVBoxLayout()
        
        api_keys_info = QLabel(
            f"Configure your API keys in:<br>"
            f"<code>{self.user_data_path / 'api_keys.txt'}</code><br><br>"
            f"See example file for format:<br>"
            f"<code>{self.user_data_path / 'api_keys.example.txt'}</code>"
        )
        api_keys_info.setWordWrap(True)
        api_keys_layout.addWidget(api_keys_info)
        
        # Button to open API keys file
        open_keys_btn = QPushButton("📝 Open API Keys File")
        open_keys_btn.clicked.connect(lambda: self.open_api_keys_file())
        api_keys_layout.addWidget(open_keys_btn)
        
        api_keys_group.setLayout(api_keys_layout)
        llm_layout.addWidget(api_keys_group)
        
        llm_layout.addStretch()
        tabs.addTab(llm_tab, "🤖 LLM Settings")
        
        # ===== TAB 2: General Settings =====
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # Load current general settings
        general_settings = self.load_general_settings()
        
        # Startup Settings group
        startup_group = QGroupBox("Startup Settings")
        startup_layout = QVBoxLayout()
        
        # Restore last project checkbox
        restore_last_project_cb = QCheckBox("Restore last project on startup")
        restore_last_project_cb.setChecked(general_settings.get('restore_last_project', False))
        restore_last_project_cb.setToolTip(
            "When enabled, Supervertaler will automatically open the last project you were working on when the application starts."
        )
        startup_layout.addWidget(restore_last_project_cb)
        
        startup_group.setLayout(startup_layout)
        general_layout.addWidget(startup_group)
        
        # Find & Replace settings group
        find_replace_group = QGroupBox("Find && Replace Settings")
        find_replace_layout = QVBoxLayout()
        
        # Allow replace in source checkbox
        allow_replace_cb = QCheckBox("Allow Replace in Source Text")
        allow_replace_cb.setChecked(self.allow_replace_in_source)
        allow_replace_cb.setToolTip(
            "⚠️ WARNING: Enabling this allows replacing text in the source column.\n"
            "This can be dangerous as it modifies your original source text.\n"
            "Use with extreme caution!"
        )
        find_replace_layout.addWidget(allow_replace_cb)
        
        # Add warning label
        warning_label = QLabel(
            "⚠️ <b>Warning:</b> Replacing in source text modifies your original content.\n"
            "This feature is disabled by default for safety."
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: #d97706; padding: 10px; background-color: #fef3c7; border-radius: 3px;")
        find_replace_layout.addWidget(warning_label)
        
        find_replace_group.setLayout(find_replace_layout)
        general_layout.addWidget(find_replace_group)
        
        general_layout.addStretch()
        tabs.addTab(general_tab, "⚙️ General")
        
        # ===== TAB 3: View/Display Settings =====
        view_tab = QWidget()
        view_layout = QVBoxLayout(view_tab)
        
        # Load current font size settings
        font_settings = self.load_general_settings()
        
        # Grid Text Font Size section
        grid_group = QGroupBox("📊 Grid Text Font Size")
        grid_layout = QVBoxLayout()
        
        grid_size_info = QLabel(
            "Set the default font size for the grid (source and target columns).\n"
            "You can also adjust this using View menu → Grid Text Zoom."
        )
        grid_size_info.setStyleSheet("font-size: 8pt; color: #666; padding: 8px; background-color: #f3f4f6; border-radius: 2px;")
        grid_size_info.setWordWrap(True)
        grid_layout.addWidget(grid_size_info)
        
        grid_spin_layout = QHBoxLayout()
        grid_spin_layout.addWidget(QLabel("Font Size:"))
        grid_font_spin = QSpinBox()
        grid_font_spin.setMinimum(7)
        grid_font_spin.setMaximum(72)
        grid_font_spin.setValue(font_settings.get('grid_font_size', 11))
        grid_font_spin.setSuffix(" pt")
        grid_font_spin.setToolTip("Grid font size (7-72 pt)")
        grid_spin_layout.addWidget(grid_font_spin)
        grid_spin_layout.addStretch()
        grid_layout.addLayout(grid_spin_layout)
        
        grid_group.setLayout(grid_layout)
        view_layout.addWidget(grid_group)
        
        # Translation Results Pane Font Size section
        results_group = QGroupBox("📋 Translation Results Pane Font Size")
        results_layout = QVBoxLayout()
        
        results_size_info = QLabel(
            "Set the default font sizes for the translation results pane.\n"
            "You can also adjust these using View menu → Translation Results Pane."
        )
        results_size_info.setStyleSheet("font-size: 8pt; color: #666; padding: 8px; background-color: #f3f4f6; border-radius: 2px;")
        results_size_info.setWordWrap(True)
        results_layout.addWidget(results_size_info)
        
        # Match list font size
        match_spin_layout = QHBoxLayout()
        match_spin_layout.addWidget(QLabel("Match List Font Size:"))
        match_font_spin = QSpinBox()
        match_font_spin.setMinimum(7)
        match_font_spin.setMaximum(16)
        match_font_spin.setValue(font_settings.get('results_match_font_size', 9))
        match_font_spin.setSuffix(" pt")
        match_font_spin.setToolTip("Match list font size (7-16 pt)")
        match_spin_layout.addWidget(match_font_spin)
        match_spin_layout.addStretch()
        results_layout.addLayout(match_spin_layout)
        
        # Compare boxes font size
        compare_spin_layout = QHBoxLayout()
        compare_spin_layout.addWidget(QLabel("Compare Boxes Font Size:"))
        compare_font_spin = QSpinBox()
        compare_font_spin.setMinimum(7)
        compare_font_spin.setMaximum(14)
        compare_font_spin.setValue(font_settings.get('results_compare_font_size', 9))
        compare_font_spin.setSuffix(" pt")
        compare_font_spin.setToolTip("Compare boxes font size (7-14 pt)")
        compare_spin_layout.addWidget(compare_font_spin)
        compare_spin_layout.addStretch()
        results_layout.addLayout(compare_spin_layout)
        
        results_group.setLayout(results_layout)
        view_layout.addWidget(results_group)
        
        # Quick Reference section
        reference_group = QGroupBox("⌨️ Font Size Quick Reference")
        reference_layout = QVBoxLayout()
        
        reference_text = QLabel(
            "<b>All Zoom Controls:</b><br>"
            "View → Grid Text Zoom<br>"
            "• Ctrl++ (NumPad +) - Increase<br>"
            "• Ctrl+- (NumPad -) - Decrease<br><br>"
            "View → Translation Results Pane<br>"
            "• Ctrl+Shift++ (Ctrl+Shift+=) - Increase<br>"
            "• Ctrl+Shift+- - Decrease<br>"
            "• Results Zoom Reset - Back to default (9pt)<br>"
        )
        reference_text.setTextFormat(Qt.TextFormat.RichText)
        reference_text.setWordWrap(True)
        reference_layout.addWidget(reference_text)
        
        reference_group.setLayout(reference_layout)
        view_layout.addWidget(reference_group)
        
        view_layout.addStretch()
        tabs.addTab(view_tab, "🔍 View/Display")
        
        # Add tabs to main layout
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_button = QPushButton("OK")
        ok_button.setMinimumWidth(100)
        ok_button.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumWidth(100)
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        # Show dialog and save settings if accepted
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Save general settings
            self.allow_replace_in_source = allow_replace_cb.isChecked()
            self.update_warning_banner()
            
            # Save general settings (including restore_last_project and font sizes)
            general_settings = {
                'restore_last_project': restore_last_project_cb.isChecked(),
                'grid_font_size': grid_font_spin.value(),
                'results_match_font_size': match_font_spin.value(),
                'results_compare_font_size': compare_font_spin.value()
            }
            self.save_general_settings(general_settings)
            
            # Apply font sizes immediately
            if self.default_font_size != grid_font_spin.value():
                self.default_font_size = grid_font_spin.value()
                if hasattr(self, 'table') and self.table is not None:
                    self.apply_font_to_grid()
                    self.auto_resize_rows()
            
            # Apply results pane font sizes
            if hasattr(self, 'assistance_widget') and hasattr(self.assistance_widget, 'set_font_size'):
                from modules.translation_results_panel import CompactMatchItem
                if CompactMatchItem.font_size_pt != match_font_spin.value():
                    CompactMatchItem.set_font_size(match_font_spin.value())
                    self.assistance_widget.set_font_size(match_font_spin.value())
            
            if hasattr(self, 'assistance_widget') and hasattr(self.assistance_widget, 'set_compare_box_font_size'):
                from modules.translation_results_panel import TranslationResultsPanel
                if TranslationResultsPanel.compare_box_font_size != compare_font_spin.value():
                    TranslationResultsPanel.compare_box_font_size = compare_font_spin.value()
                    self.assistance_widget.set_compare_box_font_size(compare_font_spin.value())
            
            # Save LLM settings
            new_settings = {
                'provider': 'openai' if openai_radio.isChecked() else 
                           'claude' if claude_radio.isChecked() else 'gemini',
                'openai_model': openai_combo.currentText().split()[0],  # Extract model name
                'claude_model': claude_combo.currentText().split()[0],
                'gemini_model': gemini_combo.currentText().split()[0]
            }
            
            self.save_llm_settings(new_settings)
            self.log(f"✓ Settings saved: Provider={new_settings['provider']}")
    
    def open_api_keys_file(self):
        """Open API keys file in system text editor"""
        api_keys_file = self.user_data_path / "api_keys.txt"
        
        # Create file if it doesn't exist
        if not api_keys_file.exists():
            try:
                # Copy from example file
                example_file = self.user_data_path / "api_keys.example.txt"
                if example_file.exists():
                    import shutil
                    shutil.copy(example_file, api_keys_file)
                    self.log(f"✓ Created api_keys.txt from example")
                else:
                    # Create basic file
                    with open(api_keys_file, 'w') as f:
                        f.write("# Add your API keys here\n")
                        f.write("# openai=sk-your-key\n")
                        f.write("# claude=sk-ant-your-key\n")
                        f.write("# gemini=your-key\n")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not create api_keys.txt: {str(e)}")
                return
        
        # Open in system editor
        try:
            import subprocess
            import platform
            
            if platform.system() == 'Windows':
                os.startfile(api_keys_file)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', api_keys_file])
            else:  # Linux
                subprocess.call(['xdg-open', api_keys_file])
                
            self.log(f"✓ Opened {api_keys_file}")
        except Exception as e:
            QMessageBox.information(
                self, "API Keys File",
                f"Please edit this file manually:\n\n{api_keys_file}"
            )
    
    def load_llm_settings(self) -> Dict[str, str]:
        """Load LLM settings from user preferences"""
        prefs_file = self.user_data_path / "ui_preferences.json"
        
        if not prefs_file.exists():
            return {
                'provider': 'openai',
                'openai_model': 'gpt-4o',
                'claude_model': 'claude-3-5-sonnet-20241022',
                'gemini_model': 'gemini-2.0-flash-exp'
            }
        
        try:
            with open(prefs_file, 'r') as f:
                prefs = json.load(f)
                return prefs.get('llm_settings', {
                    'provider': 'openai',
                    'openai_model': 'gpt-4o',
                    'claude_model': 'claude-3-5-sonnet-20241022',
                    'gemini_model': 'gemini-2.0-flash-exp'
                })
        except:
            return {
                'provider': 'openai',
                'openai_model': 'gpt-4o',
                'claude_model': 'claude-3-5-sonnet-20241022',
                'gemini_model': 'gemini-2.0-flash-exp'
            }
    
    def save_llm_settings(self, settings: Dict[str, str]):
        """Save LLM settings to user preferences"""
        prefs_file = self.user_data_path / "ui_preferences.json"
        
        # Load existing preferences
        prefs = {}
        if prefs_file.exists():
            try:
                with open(prefs_file, 'r') as f:
                    prefs = json.load(f)
            except:
                pass
        
        # Update LLM settings
        prefs['llm_settings'] = settings
        
        # Save back
        try:
            with open(prefs_file, 'w') as f:
                json.dump(prefs, f, indent=2)
        except Exception as e:
            self.log(f"⚠ Could not save LLM settings: {str(e)}")
    
    def update_warning_banner(self):
        """Show/hide warning banner based on allow_replace_in_source setting"""
        if self.allow_replace_in_source:
            self.warning_banner.show()
        else:
            self.warning_banner.hide()
    
    def show_tm_manager(self):
        """Show Translation Memory Manager dialog"""
        from modules.translation_memory import TMDatabase
        
        if not self.current_project:
            QMessageBox.warning(
                self,
                "No Project Loaded",
                "Please load or create a project first."
            )
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Translation Memory Manager")
        dialog.setMinimumSize(900, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Header
        header_label = QLabel("<h2>📚 Translation Memory Manager</h2>")
        layout.addWidget(header_label)
        
        # Tab widget for different TM management tasks
        tabs = QTabWidget()
        
        # ===== Tab 1: TM Database Overview =====
        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)
        
        # Current project info
        info_group = QGroupBox("Current Project")
        info_layout = QGridLayout()
        info_layout.addWidget(QLabel("<b>Name:</b>"), 0, 0)
        info_layout.addWidget(QLabel(self.current_project.name), 0, 1)
        info_layout.addWidget(QLabel("<b>Language Pair:</b>"), 1, 0)
        info_layout.addWidget(QLabel(f"{self.current_project.source_lang} → {self.current_project.target_lang}"), 1, 1)
        info_group.setLayout(info_layout)
        overview_layout.addWidget(info_group)
        
        # TM Statistics
        stats_group = QGroupBox("Translation Memory Statistics")
        stats_layout = QVBoxLayout()
        
        if self.tm_database:
            # Get TM count from database
            try:
                # Query database for entry count
                cursor = self.tm_database.db.connection.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM translation_units WHERE source_lang=? AND target_lang=?",
                    (self.current_project.source_lang, self.current_project.target_lang)
                )
                entry_count = cursor.fetchone()[0]
                
                stats_text = f"""<ul>
                    <li><b>Total Entries:</b> {entry_count:,}</li>
                    <li><b>Database Path:</b> {self.tm_database.db.db_path}</li>
                    <li><b>Active Language Pair:</b> {self.current_project.source_lang} → {self.current_project.target_lang}</li>
                </ul>"""
                stats_label = QLabel(stats_text)
            except Exception as e:
                stats_label = QLabel(f"<span style='color: #ef4444;'>Error reading database: {e}</span>")
        else:
            stats_label = QLabel("<span style='color: #f59e0b;'>No TM database initialized</span>")
        
        stats_layout.addWidget(stats_label)
        stats_group.setLayout(stats_layout)
        overview_layout.addWidget(stats_group)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh Statistics")
        refresh_btn.clicked.connect(lambda: self.show_tm_manager())  # Reopen dialog
        overview_layout.addWidget(refresh_btn)
        
        overview_layout.addStretch()
        tabs.addTab(overview_tab, "📊 Overview")
        
        # ===== Tab 2: Add Entry Manually =====
        add_tab = QWidget()
        add_layout = QVBoxLayout(add_tab)
        
        add_label = QLabel("<h3>Add Translation Entry</h3>")
        add_layout.addWidget(add_label)
        
        form_layout = QGridLayout()
        
        form_layout.addWidget(QLabel(f"<b>Source ({self.current_project.source_lang}):</b>"), 0, 0)
        source_input = QTextEdit()
        source_input.setMaximumHeight(100)
        source_input.setPlaceholderText("Enter source text...")
        form_layout.addWidget(source_input, 1, 0)
        
        form_layout.addWidget(QLabel(f"<b>Target ({self.current_project.target_lang}):</b>"), 2, 0)
        target_input = QTextEdit()
        target_input.setMaximumHeight(100)
        target_input.setPlaceholderText("Enter target translation...")
        form_layout.addWidget(target_input, 3, 0)
        
        add_layout.addLayout(form_layout)
        
        # Add button
        def add_entry():
            source = source_input.toPlainText().strip()
            target = target_input.toPlainText().strip()
            
            if not source or not target:
                QMessageBox.warning(dialog, "Missing Data", "Please enter both source and target text.")
                return
            
            if self.tm_database:
                try:
                    self.tm_database.add_entry(source, target)
                    QMessageBox.information(dialog, "Success", "Translation entry added to TM database!")
                    source_input.clear()
                    target_input.clear()
                    self.log(f"Added TM entry: {source[:50]}... → {target[:50]}...")
                except Exception as e:
                    QMessageBox.critical(dialog, "Error", f"Failed to add entry: {e}")
            else:
                QMessageBox.warning(dialog, "No Database", "TM database not initialized.")
        
        add_btn = QPushButton("✅ Add to Translation Memory")
        add_btn.clicked.connect(add_entry)
        add_btn.setStyleSheet("background-color: #22c55e; color: white; padding: 10px; font-weight: bold;")
        add_layout.addWidget(add_btn)
        
        add_layout.addStretch()
        tabs.addTab(add_tab, "➕ Add Entry")
        
        # ===== Tab 3: Import TMX =====
        import_tab = QWidget()
        import_layout = QVBoxLayout(import_tab)
        
        import_label = QLabel("<h3>Import TMX File</h3>")
        import_layout.addWidget(import_label)
        
        import_info = QLabel(
            "Import translation memories from TMX files. "
            "Entries will be added to the database for the current language pair."
        )
        import_info.setWordWrap(True)
        import_layout.addWidget(import_info)
        
        # File selection
        file_group = QGroupBox("TMX File")
        file_layout = QHBoxLayout()
        
        file_path_label = QLabel("No file selected")
        file_path_label.setStyleSheet("color: #6b7280;")
        file_layout.addWidget(file_path_label, 1)
        
        selected_file = [None]  # Use list to make it mutable in nested function
        
        def browse_tmx():
            file_path, _ = QFileDialog.getOpenFileName(
                dialog,
                "Select TMX File",
                str(self.user_data_path / "Translation_Resources"),
                "TMX Files (*.tmx);;All Files (*.*)"
            )
            if file_path:
                selected_file[0] = file_path
                file_path_label.setText(file_path)
                file_path_label.setStyleSheet("color: #22c55e;")
        
        browse_btn = QPushButton("📁 Browse...")
        browse_btn.clicked.connect(browse_tmx)
        file_layout.addWidget(browse_btn)
        
        file_group.setLayout(file_layout)
        import_layout.addWidget(file_group)
        
        # Import button
        def import_tmx():
            if not selected_file[0]:
                QMessageBox.warning(dialog, "No File", "Please select a TMX file first.")
                return
            
            if not self.tm_database:
                QMessageBox.warning(dialog, "No Database", "TM database not initialized.")
                return
            
            try:
                # Import TMX file
                count = self.tm_database.import_tmx(
                    selected_file[0],
                    self.current_project.source_lang,
                    self.current_project.target_lang
                )
                
                QMessageBox.information(
                    dialog,
                    "Import Successful",
                    f"Imported {count} translation entries from TMX file!"
                )
                self.log(f"Imported {count} entries from {selected_file[0]}")
                
                # Clear selection
                selected_file[0] = None
                file_path_label.setText("No file selected")
                file_path_label.setStyleSheet("color: #6b7280;")
                
            except Exception as e:
                QMessageBox.critical(dialog, "Import Error", f"Failed to import TMX file:\n{e}")
        
        import_btn = QPushButton("📥 Import TMX File")
        import_btn.clicked.connect(import_tmx)
        import_btn.setStyleSheet("background-color: #3b82f6; color: white; padding: 10px; font-weight: bold;")
        import_layout.addWidget(import_btn)
        
        import_layout.addStretch()
        tabs.addTab(import_tab, "📥 Import TMX")
        
        # ===== Tab 4: Browse Entries =====
        browse_tab = QWidget()
        browse_layout = QVBoxLayout(browse_tab)
        
        browse_label = QLabel("<h3>Browse TM Entries</h3>")
        browse_layout.addWidget(browse_label)
        
        # Search box
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("🔍 Search:"))
        search_input = QLineEdit()
        search_input.setPlaceholderText("Enter search term...")
        search_layout.addWidget(search_input, 1)
        browse_layout.addLayout(search_layout)
        
        # Results table
        results_table = QTableWidget()
        results_table.setColumnCount(3)
        results_table.setHorizontalHeaderLabels(["Source", "Target", "Match %"])
        results_table.horizontalHeader().setStretchLastSection(False)
        results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        results_table.setColumnWidth(2, 80)
        results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        browse_layout.addWidget(results_table)
        
        def search_tm():
            search_term = search_input.text().strip()
            if not search_term or not self.tm_database:
                results_table.setRowCount(0)
                return
            
            try:
                matches = self.tm_database.search_all(search_term, max_matches=50)
                
                results_table.setRowCount(len(matches))
                for i, match in enumerate(matches):
                    source_item = QTableWidgetItem(match.get('source', ''))
                    target_item = QTableWidgetItem(match.get('target', ''))
                    match_pct_item = QTableWidgetItem(f"{match.get('match_pct', 0)}%")
                    
                    # Color code by match percentage
                    match_pct = match.get('match_pct', 0)
                    if match_pct == 100:
                        color = "#22c55e"
                    elif match_pct >= 95:
                        color = "#3b82f6"
                    elif match_pct >= 85:
                        color = "#f59e0b"
                    else:
                        color = "#ef4444"
                    
                    match_pct_item.setForeground(QColor(color))
                    match_pct_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    results_table.setItem(i, 0, source_item)
                    results_table.setItem(i, 1, target_item)
                    results_table.setItem(i, 2, match_pct_item)
                
            except Exception as e:
                QMessageBox.critical(dialog, "Search Error", f"Failed to search TM: {e}")
        
        search_input.returnPressed.connect(search_tm)
        search_btn = QPushButton("🔍 Search")
        search_btn.clicked.connect(search_tm)
        search_layout.addWidget(search_btn)
        
        browse_layout.addWidget(QLabel("<i>Tip: Press Enter to search</i>"))
        
        tabs.addTab(browse_tab, "🔍 Browse")
        
        # Add tabs to dialog
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.exec()
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Supervertaler Qt",
            "<h2>Supervertaler Qt v1.1.2</h2>"
            "<p>Professional Translation Memory & CAT Tool</p>"
            "<p>Rebuilt with PyQt6 for superior performance and UI quality.</p>"
            "<p><b>Author:</b> Michael Beijer</p>"
            "<p><b>License:</b> MIT</p>"
            "<hr>"
            "<p><i>v1.1.2 - PDF Rescue Refinements & Website Updates</i></p>"
            "<p>Features are being migrated progressively from Supervertaler v3.7.x (tkinter).</p>"
        )
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.project_modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_project()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    
    # =========================================================================
    # LLM TRANSLATION INTEGRATION
    # =========================================================================
    
    def translate_current_segment(self):
        """Translate currently selected segment using LLM (Ctrl+T)"""
        current_row = self.table.currentRow()
        if current_row < 0 or not self.current_project:
            QMessageBox.warning(self, "No Selection", "Please select a segment to translate.")
            return
        
        segment = self.current_project.segments[current_row]
        
        if not segment.source.strip():
            QMessageBox.warning(self, "Empty Source", "Cannot translate empty source text.")
            return
        
        # Load API keys
        api_keys = self.load_api_keys()
        if not api_keys:
            reply = QMessageBox.question(
                self, "API Keys Missing",
                "No API keys found. Would you like to configure them now?\n\n"
                f"Keys should be in: {self.user_data_path / 'api_keys.txt'}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.show_options_dialog()
            return
        
        # Load LLM settings
        settings = self.load_llm_settings()
        provider = settings.get('provider', 'openai')
        
        # Get model based on provider
        model_key = f'{provider}_model'
        model = settings.get(model_key, 'gpt-4o')
        
        # Check if API key exists for selected provider
        if provider not in api_keys:
            reply = QMessageBox.question(
                self, f"{provider.title()} API Key Missing",
                f"{provider.title()} API key not found in api_keys.txt\n\n"
                f"Would you like to configure it now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.show_options_dialog()
            return
        
        try:
            self.status_bar.showMessage(f"Translating segment #{segment.id} with {provider} ({model})...")
            QApplication.processEvents()  # Update UI
            
            # Use modular LLM client with user's settings
            from modules.llm_clients import LLMClient
            
            client = LLMClient(
                api_key=api_keys[provider],
                provider=provider,
                model=model
            )
            
            # Translate using the module
            translation = client.translate(
                text=segment.source,
                source_lang=self.current_project.source_lang,
                target_lang=self.current_project.target_lang
            )
            
            if translation:
                # Update segment
                segment.target = translation
                segment.status = "draft"
                
                # Update grid - Column 3 is Target
                self.table.setItem(current_row, 3, QTableWidgetItem(translation))
                self.update_status_icon(current_row, "draft")
                
                # Add to Translation Memory
                if self.tm_database:
                    try:
                        self.tm_database.add_to_project_tm(segment.source, translation)
                        self.log(f"✓ Added to TM: {segment.source[:30]}... → {translation[:30]}...")
                    except Exception as tm_error:
                        self.log(f"⚠ Could not add to TM: {str(tm_error)}")
                
                # Mark project as modified
                self.project_modified = True
                self.update_window_title()
                
                self.log(f"✓ Segment #{segment.id} translated with {provider}/{model}")
                self.status_bar.showMessage(f"✓ Segment #{segment.id} translated", 3000)
            else:
                self.log(f"✗ Translation failed for segment #{segment.id}")
                QMessageBox.warning(self, "Translation Failed", "No translation received from LLM.")
                
        except Exception as e:
            self.log(f"✗ Translation error: {str(e)}")
            QMessageBox.critical(self, "Translation Error", f"Failed to translate segment:\n\n{str(e)}")
            self.status_bar.showMessage("Translation failed", 3000)
    
    def translate_batch(self):
        """Translate multiple segments with progress dialog"""
        if not self.current_project:
            QMessageBox.warning(self, "No Project", "Please load or create a project first.")
            return
        
        # Get untranslated segments
        untranslated_segments = [
            (i, seg) for i, seg in enumerate(self.current_project.segments)
            if not seg.target or seg.target.strip() == ""
        ]
        
        if not untranslated_segments:
            QMessageBox.information(
                self, "All Translated",
                "All segments already have translations!"
            )
            return
        
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Batch Translation",
            f"Found {len(untranslated_segments)} untranslated segment(s).\n\n"
            f"Translate all using your configured LLM provider?\n\n"
            f"This may take several minutes and consume API credits.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Load API keys and settings
        api_keys = self.load_api_keys()
        if not api_keys:
            QMessageBox.critical(
                self, "API Keys Missing",
                "Please configure your API keys in Settings first."
            )
            return
        
        settings = self.load_llm_settings()
        provider = settings.get('provider', 'openai')
        model_key = f'{provider}_model'
        model = settings.get(model_key, 'gpt-4o')
        
        if provider not in api_keys:
            QMessageBox.critical(
                self, f"{provider.title()} API Key Missing",
                f"Please configure your {provider.title()} API key in Settings."
            )
            return
        
        # Create progress dialog
        progress = QDialog(self)
        progress.setWindowTitle("Batch Translation Progress")
        progress.setMinimumWidth(600)
        progress.setMinimumHeight(250)
        progress.setModal(True)
        
        layout = QVBoxLayout(progress)
        
        # Header
        header_label = QLabel(f"<h3>🚀 Translating {len(untranslated_segments)} segments</h3>")
        layout.addWidget(header_label)
        
        # Provider info
        info_label = QLabel(f"<b>Provider:</b> {provider.title()} | <b>Model:</b> {model}")
        layout.addWidget(info_label)
        
        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setMaximum(len(untranslated_segments))
        progress_bar.setValue(0)
        layout.addWidget(progress_bar)
        
        # Current segment label
        current_label = QLabel("Starting...")
        layout.addWidget(current_label)
        
        # Statistics
        stats_label = QLabel("Translated: 0 | Failed: 0 | Remaining: " + str(len(untranslated_segments)))
        layout.addWidget(stats_label)
        
        # Close button (initially disabled)
        close_btn = QPushButton("Close")
        close_btn.setEnabled(False)
        close_btn.clicked.connect(progress.accept)
        layout.addWidget(close_btn)
        
        # Show progress dialog
        progress.show()
        QApplication.processEvents()
        
        # Translation statistics
        translated_count = 0
        failed_count = 0
        
        try:
            # Import LLM client
            from modules.llm_clients import LLMClient
            
            client = LLMClient(
                api_key=api_keys[provider],
                provider=provider,
                model=model
            )
            
            # Get languages from project
            source_lang = getattr(self.current_project, 'source_lang', 'en')
            target_lang = getattr(self.current_project, 'target_lang', 'nl')
            
            self.log(f"Batch translation: {source_lang} → {target_lang}")
            
            # Translate each segment
            for idx, (row_index, segment) in enumerate(untranslated_segments):
                # Update progress
                current_label.setText(f"Translating segment #{segment.id}: {segment.source[:60]}...")
                progress_bar.setValue(idx)
                QApplication.processEvents()
                
                try:
                    # Translate
                    translation = client.translate(
                        text=segment.source,
                        source_lang=source_lang,
                        target_lang=target_lang
                    )
                    
                    if translation:
                        # Update segment
                        segment.target = translation
                        segment.status = "draft"
                        
                        # Update grid
                        self.table.setItem(row_index, 3, QTableWidgetItem(translation))
                        self.update_status_icon(row_index, "draft")
                        
                        # Add to TM
                        if self.tm_database:
                            try:
                                self.tm_database.add_to_project_tm(segment.source, translation)
                            except:
                                pass  # Don't fail batch on TM errors
                        
                        translated_count += 1
                        self.log(f"✓ Batch: Segment #{segment.id} translated")
                    else:
                        failed_count += 1
                        self.log(f"✗ Batch: Segment #{segment.id} - no translation received")
                
                except Exception as e:
                    failed_count += 1
                    self.log(f"✗ Batch: Segment #{segment.id} - {str(e)}")
                
                # Update statistics
                remaining = len(untranslated_segments) - (idx + 1)
                stats_label.setText(
                    f"Translated: {translated_count} | Failed: {failed_count} | Remaining: {remaining}"
                )
                QApplication.processEvents()
            
            # Mark project as modified
            if translated_count > 0:
                self.project_modified = True
                self.update_window_title()
            
            # Completion message
            progress_bar.setValue(len(untranslated_segments))
            current_label.setText(
                f"<b>✓ Batch translation complete!</b><br>"
                f"Successfully translated: {translated_count}<br>"
                f"Failed: {failed_count}"
            )
            
            # Enable close button
            close_btn.setEnabled(True)
            
            self.log(f"✓ Batch translation complete: {translated_count} translated, {failed_count} failed")
            
        except Exception as e:
            QMessageBox.critical(
                progress,
                "Batch Translation Error",
                f"Batch translation failed:\n\n{str(e)}"
            )
            self.log(f"✗ Batch translation error: {str(e)}")
            close_btn.setEnabled(True)
        
        # Wait for user to close
        progress.exec()
    
    def load_api_keys(self) -> Dict[str, str]:
        """Load API keys from user data folder"""
        api_keys = {}
        api_keys_file = self.user_data_path / "api_keys.txt"
        
        if not api_keys_file.exists():
            return api_keys
        
        try:
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        api_keys[key.strip().lower()] = value.strip()
        except Exception as e:
            self.log(f"⚠ Error loading API keys: {str(e)}")
        
        return api_keys
    
    def ensure_example_api_keys(self):
        """Create example API keys file on first launch for new users"""
        example_file = self.user_data_path / "api_keys.example.txt"
        
        # Only create if it doesn't exist
        if example_file.exists():
            return
        
        example_content = """# Supervertaler API Keys Configuration
# =======================================
# 
# Add your API keys below. Remove the # to activate a key.
# Never commit this file with real keys to version control!
#
# For actual use:
# 1. Copy this file to "api_keys.txt" in the same folder
# 2. Add your real API keys (remove the # from the lines you use)
# 3. Save the file
#
# Available providers:

# OpenAI (GPT-4, GPT-4o, GPT-5, o1, o3 models)
# Get your key at: https://platform.openai.com/api-keys
#openai=sk-your-openai-api-key-here

# Anthropic Claude (Claude 3.5 Sonnet, etc.)
# Get your key at: https://console.anthropic.com/
#claude=sk-ant-your-claude-api-key-here

# Google Gemini (Gemini 2.0 Flash, Pro models)
# Get your key at: https://makersuite.google.com/app/apikey
#gemini=your-gemini-api-key-here

# Temperature settings for reasoning models:
# - GPT-5, o1, o3: Use temperature=1.0 (automatically applied)
# - Standard models: Use temperature=0.3 (automatically applied)
"""
        
        try:
            with open(example_file, 'w', encoding='utf-8') as f:
                f.write(example_content)
            self.log(f"✓ Created example API keys file: {example_file}")
        except Exception as e:
            self.log(f"⚠ Could not create example API keys file: {str(e)}")
    
    def show_autofingers(self):
        """Show AutoFingers by switching to the AutoFingers tab"""
        # Find the AutoFingers tab index and activate it
        for i in range(self.main_tabs.count()):
            if self.main_tabs.tabText(i) == "✋ AutoFingers":
                self.main_tabs.setCurrentIndex(i)
                break
    
    def show_theme_editor(self):
        """Show Theme Editor dialog"""
        dialog = ThemeEditorDialog(self, self.theme_manager)
        if dialog.exec():
            # Theme may have been changed, reapply
            self.theme_manager.apply_theme(QApplication.instance())


# ============================================================================
# UNIVERSAL LOOKUP TAB
# ============================================================================

class UniversalLookupTab(QWidget):
    """
    Universal Lookup - System-wide translation lookup
    Works anywhere on your computer: in CAT tools, browsers, Word, any text box
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Import lookup engine
        try:
            from modules.universal_lookup import UniversalLookupEngine, LookupResult
            self.UniversalLookupEngine = UniversalLookupEngine
            self.LookupResult = LookupResult
        except ImportError:
            QMessageBox.critical(
                self,
                "Missing Module",
                "Could not import universal_lookup module.\nPlease ensure modules/universal_lookup.py exists."
            )
            self.UniversalLookupEngine = None
            self.LookupResult = None
            return
        
        # Initialize engine
        self.engine = None
        self.tm_database = None
        self.hotkey_registered = False
        
        # UI setup
        self.init_ui()
        
        # Register global hotkey
        self.register_global_hotkey()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)  # Reduced from 10 to 5 for consistency
        
        # Header
        header = QLabel("🔍 Universal Lookup")
        header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
        layout.addWidget(header, 0)  # 0 = no stretch, stays compact
        
        # Description
        if os.name == 'nt':
            # Windows - full functionality
            description_text = (
                "Look up translations anywhere on your computer.\n"
                "Press Ctrl+Alt+L or paste text manually to search your translation memory."
            )
        else:
            # Mac/Linux - manual mode only
            description_text = (
                "Look up translations in your translation memory.\n"
                "⚠️ Global hotkey not available on this platform. Paste text manually to search."
            )
        
        description = QLabel(description_text)
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
        layout.addWidget(description, 0)  # 0 = no stretch, stays compact
        
        # Mode selector (using label instead of group box)
        mode_label_header = QLabel("⚙️ Operating Mode")
        mode_label_header.setStyleSheet("font-weight: bold; font-size: 10pt; margin-top: 10px;")
        layout.addWidget(mode_label_header, 0)  # 0 = no stretch
        
        mode_layout = QHBoxLayout()
        
        mode_label = QLabel("Mode:")
        mode_layout.addWidget(mode_label)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Universal (Any Text Box)", "memoQ", "Trados", "CafeTran"])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo, stretch=1)
        
        layout.addLayout(mode_layout)
        
        # Source text area (using label instead of group box)
        source_label_header = QLabel("📝 Source Text")
        source_label_header.setStyleSheet("font-weight: bold; font-size: 10pt; margin-top: 10px;")
        layout.addWidget(source_label_header)
        
        self.source_text = QTextEdit()
        self.source_text.setPlaceholderText("Click 'Capture Text' or paste text here to search...")
        self.source_text.setMaximumHeight(100)
        layout.addWidget(self.source_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        if os.name == 'nt':
            # Windows - show capture button (though hotkey is preferred)
            capture_btn = QPushButton("📥 Manual Capture")
            capture_btn.setToolTip("Manually trigger text capture (Ctrl+Alt+L is recommended)")
            capture_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
            capture_btn.clicked.connect(self.capture_text)
            button_layout.addWidget(capture_btn)
        
        search_btn = QPushButton("🔍 Search")
        search_btn.setStyleSheet("font-weight: bold; background-color: #2196F3; color: white; padding: 8px;")
        search_btn.clicked.connect(self.perform_lookup)
        button_layout.addWidget(search_btn)
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        # Results area (with tabs for TM, termbase, MT)
        self.results_tabs = QTabWidget()
        
        # TM Results tab
        tm_tab = self.create_tm_results_tab()
        self.results_tabs.addTab(tm_tab, "📖 TM Matches")
        
        # Termbase Results tab
        termbase_tab = self.create_termbase_results_tab()
        self.results_tabs.addTab(termbase_tab, "📚 Termbase Terms")
        
        # MT Results tab
        mt_tab = self.create_mt_results_tab()
        self.results_tabs.addTab(mt_tab, "🤖 Machine Translation")
        
        layout.addWidget(self.results_tabs, stretch=1)
        
        # Status bar
        self.status_label = QLabel("Ready. Select a mode and capture text to begin.")
        self.status_label.setStyleSheet("padding: 5px; background-color: #f5f5f5; border-radius: 3px;")
        layout.addWidget(self.status_label, 0)  # 0 = no stretch, stays compact
    
    def create_tm_results_tab(self):
        """Create the TM results tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Results table
        self.tm_results_table = QTableWidget()
        self.tm_results_table.setColumnCount(4)
        self.tm_results_table.setHorizontalHeaderLabels(["Match %", "Source", "Target", "Type"])
        self.tm_results_table.horizontalHeader().setStretchLastSection(False)
        self.tm_results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tm_results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tm_results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tm_results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tm_results_table.doubleClicked.connect(self.on_tm_result_double_click)
        
        layout.addWidget(self.tm_results_table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        copy_btn = QPushButton("📋 Copy Target")
        copy_btn.clicked.connect(self.copy_selected_tm_target)
        button_layout.addWidget(copy_btn)
        
        insert_btn = QPushButton("📥 Insert Target")
        insert_btn.setToolTip("Insert selected translation (Ctrl+V)")
        insert_btn.clicked.connect(self.insert_selected_tm_target)
        button_layout.addWidget(insert_btn)
        
        layout.addLayout(button_layout)
        
        return tab
    
    def create_termbase_results_tab(self):
        """Create the termbase results tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Results table
        self.termbase_results_table = QTableWidget()
        self.termbase_results_table.setColumnCount(2)
        self.termbase_results_table.setHorizontalHeaderLabels(["Term (Source)", "Translation (Target)"])
        self.termbase_results_table.horizontalHeader().setStretchLastSection(True)
        self.termbase_results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.termbase_results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.termbase_results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(self.termbase_results_table)
        
        # Info label
        info = QLabel("💡 Tip: Double-click a term to copy it to clipboard")
        info.setStyleSheet("color: #666; font-size: 9pt; padding: 5px;")
        layout.addWidget(info)
        
        return tab
    
    def create_mt_results_tab(self):
        """Create the MT results tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Results list
        self.mt_results_layout = QVBoxLayout()
        
        # Placeholder
        placeholder = QLabel("🤖 Machine Translation\n\nComing soon: DeepL, OpenAI, Google Translate integration")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #999; padding: 40px;")
        self.mt_results_layout.addWidget(placeholder)
        
        layout.addLayout(self.mt_results_layout)
        layout.addStretch()
        
        return tab
    
    def on_mode_changed(self, mode_text):
        """Handle mode change"""
        mode_map = {
            "Universal (Any Text Box)": "universal",
            "memoQ": "memoq",
            "Trados": "trados",
            "CafeTran": "cafetran"
        }
        
        mode = mode_map.get(mode_text, "universal")
        
        if self.engine:
            self.engine.mode = mode
            self.status_label.setText(f"Mode changed to: {mode_text}")
    
    def __del__(self):
        """Destructor - cleanup AHK process when widget is destroyed"""
        try:
            self.unregister_global_hotkey()
        except:
            pass
    
    def capture_text(self, delay=True):
        """
        Capture text from the active application
        
        Args:
            delay: If True, wait 1.5 seconds before capturing (for manual button clicks)
                   If False, capture immediately (for global hotkey)
        """
        if not self.UniversalLookupEngine:
            return
        
        # Initialize engine if needed
        if not self.engine:
            mode_text = self.mode_combo.currentText()
            mode_map = {
                "Universal (Any Text Box)": "universal",
                "memoQ": "memoq",
                "Trados": "trados",
                "CafeTran": "cafetran"
            }
            mode = mode_map.get(mode_text, "universal")
            self.engine = self.UniversalLookupEngine(mode=mode)
            
            # Set TM database if available
            if self.tm_database:
                self.engine.set_tm_database(self.tm_database)
        
        if delay:
            # Manual button click - give time to switch windows
            self.status_label.setText("⏳ Capturing text... Switch to target application now!")
            QApplication.processEvents()
            time.sleep(1.5)
        else:
            # Global hotkey - capture immediately
            self.status_label.setText("⏳ Capturing text...")
            QApplication.processEvents()
        
        # Capture text
        text = self.engine.capture_text()
        
        if text:
            self.source_text.setPlainText(text)
            self.status_label.setText(f"✓ Captured {len(text)} characters. Searching...")
            # Auto-search after capture
            self.perform_lookup()
        else:
            self.status_label.setText("✗ No text captured. Try again.")
    
    def perform_lookup(self):
        """Perform lookup on the source text"""
        text = self.source_text.toPlainText().strip()
        
        if not text:
            self.status_label.setText("⚠️ No text to search. Enter or capture text first.")
            return
        
        if not self.engine:
            # Initialize engine
            mode_text = self.mode_combo.currentText()
            mode_map = {
                "Universal (Any Text Box)": "universal",
                "memoQ": "memoq",
                "Trados": "trados",
                "CafeTran": "cafetran"
            }
            mode = mode_map.get(mode_text, "universal")
            self.engine = UniversalLookupEngine(mode=mode)
            
            # Set TM database if available
            if self.tm_database:
                self.engine.set_tm_database(self.tm_database)
        
        self.status_label.setText("🔍 Searching...")
        QApplication.processEvents()
        
        # Perform lookups
        results = self.engine.lookup_all(text)
        
        # Display TM results
        self.display_tm_results(results.get('tm', []))
        
        # Display termbase results
        self.display_glossary_results(results.get('termbase', []))
        
        # Display MT results
        self.display_mt_results(results.get('mt', []))
        
        total_results = len(results.get('tm', [])) + len(results.get('termbase', [])) + len(results.get('mt', []))
        self.status_label.setText(f"✓ Found {total_results} results")
    
    def display_tm_results(self, results):
        """Display TM results in the table"""
        self.tm_results_table.setRowCount(0)
        
        for result in results:
            row = self.tm_results_table.rowCount()
            self.tm_results_table.insertRow(row)
            
            # Match percentage
            match_item = QTableWidgetItem(f"{result.match_percent}%")
            if result.match_percent == 100:
                match_item.setBackground(QColor("#C8E6C9"))  # Green for exact
            elif result.match_percent >= 95:
                match_item.setBackground(QColor("#FFF9C4"))  # Yellow for high
            self.tm_results_table.setItem(row, 0, match_item)
            
            # Source
            self.tm_results_table.setItem(row, 1, QTableWidgetItem(result.source))
            
            # Target
            self.tm_results_table.setItem(row, 2, QTableWidgetItem(result.target))
            
            # Type
            match_type = result.metadata.get('match_type', 'unknown')
            self.tm_results_table.setItem(row, 3, QTableWidgetItem(match_type))
        
        self.tm_results_table.resizeRowsToContents()
    
    def display_termbase_results(self, results):
        """Display termbase results"""
        self.termbase_results_table.setRowCount(0)
        
        for result in results:
            row = self.termbase_results_table.rowCount()
            self.termbase_results_table.insertRow(row)
            
            self.termbase_results_table.setItem(row, 0, QTableWidgetItem(result.source))
            self.termbase_results_table.setItem(row, 1, QTableWidgetItem(result.target))
        
        self.termbase_results_table.resizeRowsToContents()
    
    def display_mt_results(self, results):
        """Display MT results"""
        # Clear existing
        while self.mt_results_layout.count():
            item = self.mt_results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if results:
            for result in results:
                label = QLabel(f"{result.metadata.get('provider', 'MT')}: {result.target}")
                label.setWordWrap(True)
                self.mt_results_layout.addWidget(label)
        else:
            placeholder = QLabel("🤖 No MT results yet\n\n(MT integration coming soon)")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("color: #999; padding: 20px;")
            self.mt_results_layout.addWidget(placeholder)
    
    def on_tm_result_double_click(self, index):
        """Handle double-click on TM result"""
        self.copy_selected_tm_target()
    
    def copy_selected_tm_target(self):
        """Copy selected TM target to clipboard"""
        selected = self.tm_results_table.selectedItems()
        if selected:
            row = selected[0].row()
            target_item = self.tm_results_table.item(row, 2)
            if target_item:
                pyperclip.copy(target_item.text())
                self.status_label.setText(f"✓ Copied to clipboard: {target_item.text()[:50]}...")
    
    def insert_selected_tm_target(self):
        """Insert selected TM target into active application"""
        selected = self.tm_results_table.selectedItems()
        if selected:
            row = selected[0].row()
            target_item = self.tm_results_table.item(row, 2)
            if target_item:
                pyperclip.copy(target_item.text())
                self.status_label.setText("✓ Copied to clipboard. Press Ctrl+V to paste.")
                # Could auto-paste here if we wanted to be aggressive
                # pyautogui.hotkey('ctrl', 'v')
    
    def clear_all(self):
        """Clear all text and results"""
        self.source_text.clear()
        self.tm_results_table.setRowCount(0)
        self.termbase_results_table.setRowCount(0)
        self.status_label.setText("Cleared. Ready for new lookup.")
    
    def set_tm_database(self, tm_db):
        """Set TM database (called from main window)"""
        self.tm_database = tm_db
        if self.engine:
            self.engine.set_tm_database(tm_db)
    
    def register_global_hotkey(self):
        """Register global hotkey for Universal Lookup"""
        global _ahk_process
        try:
            # Kill any existing instances of the AHK script first
            if os.name == 'nt':
                try:
                    # Use multiple methods to ensure cleanup
                    # Method 1: Kill by window title
                    subprocess.run(['taskkill', '/F', '/FI', 'WINDOWTITLE eq universal_lookup_hotkey.ahk*'],
                                 capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    
                    # Method 2: Kill AutoHotkey processes more aggressively
                    subprocess.run(['taskkill', '/F', '/IM', 'AutoHotkey.exe'],
                                 capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    
                    # Method 3: Kill by process name pattern
                    import psutil
                    try:
                        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                            try:
                                if 'universal_lookup_hotkey' in ' '.join(proc.cmdline() or []):
                                    proc.kill()
                            except:
                                pass
                    except:
                        pass
                except:
                    pass
            
            # Find AutoHotkey executable
            username = os.environ.get('USERNAME', '')
            ahk_paths = [
                r"C:\Program Files\AutoHotkey\v2\AutoHotkey.exe",
                r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe",
                r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
                fr"C:\Users\{username}\AppData\Local\Programs\AutoHotkey\AutoHotkey.exe"
            ]
            
            ahk_exe = None
            for path in ahk_paths:
                if os.path.exists(path):
                    ahk_exe = path
                    break
            
            if not ahk_exe:
                print("[Universal Lookup] AutoHotkey not found. Please install from https://www.autohotkey.com/")
                print("[Universal Lookup] Searched paths:", ahk_paths)
                self.hotkey_registered = False
                return
            
            ahk_script = Path(__file__).parent / "universal_lookup_hotkey.ahk"
            if ahk_script.exists():
                # Start AHK script in background (hidden)
                self.ahk_process = subprocess.Popen([ahk_exe, str(ahk_script)],
                                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                # Store in global variable for atexit cleanup
                _ahk_process = self.ahk_process
                print(f"[Universal Lookup] AHK hotkey registered: Ctrl+Alt+L")
                
                # Start file watcher
                self.start_file_watcher()
                self.hotkey_registered = True
            else:
                print(f"[Universal Lookup] AHK script not found: {ahk_script}")
                self.hotkey_registered = False
        except Exception as e:
            print(f"[Universal Lookup] Could not start AHK hotkey: {e}")
            self.hotkey_registered = False
    
    def start_file_watcher(self):
        """Watch for signal file from AHK"""
        self.signal_file = Path(__file__).parent / "lookup_signal.txt"
        self.capture_file = Path(__file__).parent / "temp_capture.txt"
        
        # Create timer to check for signal file
        self.file_check_timer = QTimer()
        self.file_check_timer.timeout.connect(self.check_for_signal)
        self.file_check_timer.start(100)  # Check every 100ms
    
    def check_for_signal(self):
        """Check if AHK wrote a signal file"""
        if self.signal_file.exists():
            try:
                # Delete signal file
                self.signal_file.unlink()
                
                # Get text from clipboard (AHK already copied it)
                time.sleep(0.1)  # Give clipboard a moment
                text = pyperclip.paste()
                
                # Trigger lookup
                if text:
                    self.on_ahk_capture(text)
            except Exception as e:
                print(f"[Universal Lookup] Error reading capture: {e}")
    
    def on_ahk_capture(self, text):
        """Handle text captured by AHK"""
        try:
            # Bring Supervertaler to foreground
            main_window = self.window()
            if main_window:
                # Check if window was maximized before restoring
                was_maximized = main_window.isMaximized()
                
                # Restore if minimized or hidden
                if main_window.isMinimized():
                    main_window.showNormal()
                elif main_window.isHidden():
                    main_window.show()
                else:
                    # If already visible, just activate
                    main_window.show()
                
                # Restore maximized state if it was maximized
                if was_maximized:
                    main_window.showMaximized()
                
                # Aggressive activation without flag manipulation
                main_window.raise_()
                main_window.activateWindow()
                
                # Windows-specific: force to foreground (multi-monitor safe)
                if os.name == 'nt':
                    try:
                        import ctypes
                        hwnd = int(main_window.winId())
                        
                        # Get the foreground window's thread
                        foreground_hwnd = ctypes.windll.user32.GetForegroundWindow()
                        foreground_thread = ctypes.windll.user32.GetWindowThreadProcessId(foreground_hwnd, None)
                        current_thread = ctypes.windll.kernel32.GetCurrentThreadId()
                        
                        # Attach to foreground thread to bypass focus stealing prevention
                        if foreground_thread != current_thread:
                            ctypes.windll.user32.AttachThreadInput(foreground_thread, current_thread, True)
                        
                        # Now we can set foreground
                        ctypes.windll.user32.SetForegroundWindow(hwnd)
                        ctypes.windll.user32.BringWindowToTop(hwnd)
                        
                        # Detach thread input
                        if foreground_thread != current_thread:
                            ctypes.windll.user32.AttachThreadInput(foreground_thread, current_thread, False)
                    except Exception as e:
                        print(f"[Universal Lookup] Window activation error: {e}")
                
                if hasattr(main_window, 'main_tabs'):
                    main_window.main_tabs.setCurrentIndex(0)
            
            # Paste into search box
            if text:
                self.source_text.setPlainText(text)
                self.status_label.setText(f"✓ Captured {len(text)} characters. Searching...")
                QApplication.processEvents()
                self.perform_lookup()
            else:
                self.status_label.setText("✗ No text captured.")
        except Exception as e:
            print(f"[Universal Lookup] Error: {e}")
            self.status_label.setText(f"✗ Error: {e}")
    
    def unregister_global_hotkey(self):
        """Unregister global hotkey and terminate AHK process"""
        global _ahk_process
        if self.hotkey_registered:
            try:
                # Stop file watcher
                if hasattr(self, 'file_check_timer'):
                    self.file_check_timer.stop()
                
                # Terminate AHK process
                if hasattr(self, 'ahk_process') and self.ahk_process:
                    try:
                        self.ahk_process.terminate()
                        self.ahk_process.wait(timeout=2)
                        print("[Universal Lookup] AHK process terminated")
                    except Exception as e:
                        # Force kill if terminate doesn't work
                        try:
                            self.ahk_process.kill()
                            print("[Universal Lookup] AHK process killed")
                        except:
                            pass
                    finally:
                        _ahk_process = None  # Clear global reference
                
                self.hotkey_registered = False
                print("[Universal Lookup] AHK hotkey unregistered")
            except Exception as e:
                print(f"[Universal Lookup] Error unregistering: {e}")
                pass
    
    def restore_window_flags(self, window):
        """Restore normal window flags after showing on top"""
        try:
            window.setWindowFlags(window.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
            window.show()
        except:
            pass


# ============================================================================
# AUTOFINGERS DIALOG
# ============================================================================

class CheckmarkCheckBox(QCheckBox):
    """Custom checkbox with green background and white checkmark when checked"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                font-size: 9pt;
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #999;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
            }
            QCheckBox::indicator:hover {
                border-color: #666;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #45a049;
                border-color: #45a049;
            }
        """)
    
    def paintEvent(self, event):
        """Override paint event to draw white checkmark when checked"""
        super().paintEvent(event)
        
        if self.isChecked():
            # Get the indicator rectangle using QStyle
            from PyQt6.QtWidgets import QStyleOptionButton
            from PyQt6.QtGui import QPainter, QPen, QColor
            from PyQt6.QtCore import QPointF, QRect
            
            opt = QStyleOptionButton()
            self.initStyleOption(opt)
            indicator_rect = self.style().subElementRect(
                self.style().SubElement.SE_CheckBoxIndicator,
                opt,
                self
            )
            
            if indicator_rect.isValid():
                # Draw white checkmark
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                # Slightly thinner pen for better fit on smaller displays
                pen_width = max(2.0, min(indicator_rect.width(), indicator_rect.height()) * 0.12)
                painter.setPen(QPen(QColor(255, 255, 255), pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
                painter.setBrush(QColor(255, 255, 255))
                
                # Draw checkmark (✓ shape) - coordinates relative to indicator
                # Add padding to prevent clipping on smaller displays
                x = indicator_rect.x()
                y = indicator_rect.y()
                w = indicator_rect.width()
                h = indicator_rect.height()
                
                # Add padding (15% on all sides) to ensure checkmark doesn't get cut off on smaller displays
                padding = min(w, h) * 0.15
                x += padding
                y += padding
                w -= padding * 2
                h -= padding * 2
                
                # Checkmark path: bottom-left to middle, then middle to top-right
                # Using proportions that create a nice checkmark shape with proper padding
                check_x1 = x + w * 0.10  # Left point (more padding from left)
                check_y1 = y + h * 0.50  # Bottom point (centered vertically)
                check_x2 = x + w * 0.35  # Middle-bottom point
                check_y2 = y + h * 0.70  # Bottom point (with padding from bottom)
                check_x3 = x + w * 0.90  # Right point (more padding from right)
                check_y3 = y + h * 0.25  # Top point (with padding from top)
                
                # Draw two lines forming the checkmark
                painter.drawLine(QPointF(check_x2, check_y2), QPointF(check_x3, check_y3))
                painter.drawLine(QPointF(check_x1, check_y1), QPointF(check_x2, check_y2))
                
                painter.end()


class AutoFingersWidget(QWidget):
    """
    AutoFingers - CAT Tool Automation Widget
    Provides UI for translation automation in tools like memoQ
    Now integrated as a tab in the main Supervertaler window
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Import AutoFingers engine
        try:
            from modules.autofingers_engine import AutoFingersEngine
            self.AutoFingersEngine = AutoFingersEngine
        except ImportError:
            QMessageBox.critical(
                self,
                "Import Error",
                "Could not import AutoFingers engine.\n"
                "Make sure modules/autofingers_engine.py exists."
            )
            return
        
        # Initialize engine
        self.engine = None
        self.is_running = False
        
        # Get default TMX path from user data
        if ENABLE_PRIVATE_FEATURES:
            default_tmx = "user data_private/autofingers_tm.tmx"
        else:
            default_tmx = "user data/autofingers_tm.tmx"
        
        self.tmx_file = default_tmx
        
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Header (matches Universal Lookup / PDF Rescue / TMX Editor style)
        header = QLabel("🤖 AutoFingers")
        header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
        layout.addWidget(header, 0)  # 0 = no stretch, stays compact
        
        # Description box (matches Universal Lookup / PDF Rescue / TMX Editor style)
        info = QLabel(
            "Automated Translation Pasting for memoQ.\n"
            "AutoFingers reads from a TMX file and pastes translations automatically."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
        layout.addWidget(info, 0)  # 0 = no stretch, stays compact
        
        # Tabs
        tabs = QTabWidget()
        
        # TAB 1: Control Panel (with integrated settings)
        control_tab = self.create_control_tab()
        tabs.addTab(control_tab, "🎮 Control Panel")
        
        # TAB 2: TMX Manager
        tmx_tab = self.create_tmx_tab()
        tabs.addTab(tmx_tab, "📚 TMX Manager")
        
        layout.addWidget(tabs, 1)  # 1 = stretch to fill space
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout, 0)  # 0 = no stretch, stays compact
        
        # Setup global keyboard shortcuts (matching AutoHotkey version)
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """Setup GLOBAL keyboard shortcuts for AutoFingers actions"""
        import keyboard
        
        try:
            # Store hotkey references for later removal
            self.hotkeys = []
            
            # Register global hotkeys that work even when memoQ has focus
            # Ctrl+Alt+P - Process single segment
            self.hotkeys.append(keyboard.add_hotkey('ctrl+alt+p', self.process_single_safe))
            
            # Ctrl+Shift+L - Toggle loop mode
            self.hotkeys.append(keyboard.add_hotkey('ctrl+shift+l', self.toggle_loop_safe))
            
            # Ctrl+Alt+S - Stop loop
            self.hotkeys.append(keyboard.add_hotkey('ctrl+alt+s', self.stop_loop_safe))
            
            # Ctrl+Alt+R - Reload TMX
            self.hotkeys.append(keyboard.add_hotkey('ctrl+alt+r', self.reload_tmx_safe))
            
            self.log("✓ Global hotkeys registered: Ctrl+Alt+P (single), Ctrl+Shift+L (loop), Ctrl+Alt+S (stop), Ctrl+Alt+R (reload)")
            self.log("ℹ️ Hotkeys work globally - even when memoQ has focus!")
            
        except Exception as e:
            self.log(f"⚠️ Could not register global hotkeys: {str(e)}")
            self.log("ℹ️ You may need to run as Administrator for global hotkeys")
    
    def process_single_safe(self):
        """Safe wrapper for process_single (called from global hotkey - runs in hotkey thread)"""
        try:
            # Dispatch to main Qt thread to avoid threading issues
            QTimer.singleShot(0, self.process_single)
        except Exception as e:
            print(f"Error in process_single_safe: {e}")
    
    def toggle_loop_safe(self):
        """Safe wrapper for toggle_loop (called from global hotkey - runs in hotkey thread)"""
        try:
            # Dispatch to main Qt thread to avoid threading issues
            QTimer.singleShot(0, self.toggle_loop)
        except Exception as e:
            print(f"Error in toggle_loop_safe: {e}")
    
    def stop_loop_safe(self):
        """Safe wrapper for stop_loop (called from global hotkey)"""
        try:
            self.stop_loop()
        except Exception as e:
            print(f"Error in stop_loop: {e}")
    
    def reload_tmx_safe(self):
        """Safe wrapper for reload_tmx (called from global hotkey)"""
        try:
            self.reload_tmx()
        except Exception as e:
            print(f"Error in reload_tmx: {e}")
    
    def cleanup_hotkeys(self):
        """Cleanup AutoFingers hotkeys when widget is closed/hidden"""
        # Unregister ONLY AutoFingers hotkeys
        try:
            import keyboard
            if hasattr(self, 'hotkeys'):
                for hotkey in self.hotkeys:
                    try:
                        keyboard.remove_hotkey(hotkey)
                    except:
                        pass
                self.log("AutoFingers hotkeys unregistered")
        except Exception as e:
            print(f"Error unregistering hotkeys: {e}")
    
    def create_control_tab(self):
        """Create the main control panel with horizontal layout"""
        tab = QWidget()
        main_layout = QVBoxLayout(tab)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # TOP ROW: Actions and TMX File side by side
        top_row = QHBoxLayout()
        top_row.setSpacing(8)
        
        # === LEFT: ACTIONS GROUP ===
        actions_group = QGroupBox("🎯 Actions")
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        # Single button
        single_col = QVBoxLayout()
        single_btn = QPushButton("▶️ Single")
        single_btn.setMinimumHeight(40)
        single_btn.setMinimumWidth(100)
        single_btn.setStyleSheet("font-size: 10pt; font-weight: bold;")
        single_btn.clicked.connect(self.process_single)
        single_col.addWidget(single_btn)
        single_info = QLabel("(Ctrl+Alt+P)")
        single_info.setStyleSheet("color: #666; font-size: 8pt;")
        single_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        single_col.addWidget(single_info)
        actions_layout.addLayout(single_col)
        
        # Loop button
        loop_col = QVBoxLayout()
        self.loop_btn = QPushButton("▶ Loop Mode")
        self.loop_btn.setMinimumHeight(40)
        self.loop_btn.setMinimumWidth(110)
        self.loop_btn.setStyleSheet("font-size: 10pt; font-weight: bold; background-color: #4CAF50; color: white;")
        self.loop_btn.clicked.connect(self.toggle_loop)
        loop_col.addWidget(self.loop_btn)
        loop_info = QLabel("(Ctrl+Shift+L)")
        loop_info.setStyleSheet("color: #666; font-size: 8pt;")
        loop_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loop_col.addWidget(loop_info)
        actions_layout.addLayout(loop_col)
        
        # Segments spin
        segs_col = QVBoxLayout()
        segs_label = QLabel("Segments:")
        segs_label.setStyleSheet("font-size: 9pt; font-weight: bold;")
        segs_col.addWidget(segs_label)
        self.loop_segments_spin = QSpinBox()
        self.loop_segments_spin.setMinimum(0)
        self.loop_segments_spin.setMaximum(9999)
        self.loop_segments_spin.setValue(0)
        self.loop_segments_spin.setSuffix(" (0=∞)")
        self.loop_segments_spin.setMinimumHeight(28)
        self.loop_segments_spin.setStyleSheet("font-size: 9pt;")
        segs_col.addWidget(self.loop_segments_spin)
        actions_layout.addLayout(segs_col)
        
        # Progress
        progress_col = QVBoxLayout()
        self.progress_label = QLabel("Ready")
        self.progress_label.setStyleSheet("font-weight: bold; font-size: 9pt;")
        progress_col.addWidget(self.progress_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(28)
        progress_col.addWidget(self.progress_bar)
        actions_layout.addLayout(progress_col)
        
        actions_group.setLayout(actions_layout)
        top_row.addWidget(actions_group, 2)
        
        # === RIGHT: TMX FILE GROUP ===
        tmx_group = QGroupBox("📁 TMX File")
        tmx_layout = QVBoxLayout()
        tmx_layout.setSpacing(4)
        
        # File path row
        path_row = QHBoxLayout()
        self.tmx_path_label = QLabel(self.tmx_file)
        self.tmx_path_label.setStyleSheet("padding: 4px; background-color: #F5F5F5; font-size: 8pt;")
        path_row.addWidget(self.tmx_path_label, 1)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setMaximumWidth(70)
        browse_btn.clicked.connect(self.browse_tmx)
        path_row.addWidget(browse_btn)
        
        reload_btn = QPushButton("Reload")
        reload_btn.setMaximumWidth(70)
        reload_btn.clicked.connect(self.reload_tmx)
        path_row.addWidget(reload_btn)
        
        tmx_layout.addLayout(path_row)
        
        # Status
        self.tmx_status_label = QLabel("No TMX loaded")
        self.tmx_status_label.setStyleSheet("padding: 4px; font-weight: bold; font-size: 9pt;")
        tmx_layout.addWidget(self.tmx_status_label)
        
        tmx_group.setLayout(tmx_layout)
        top_row.addWidget(tmx_group, 1)
        
        main_layout.addLayout(top_row)
        
        # MIDDLE ROW: Settings in a 2-column grid layout for better organization
        settings_group = QGroupBox("⚙️ Settings")
        settings_layout = QGridLayout()
        settings_layout.setSpacing(15)
        settings_layout.setColumnStretch(0, 1)  # Left column flexible
        settings_layout.setColumnStretch(1, 1)  # Right column flexible
        
        # LEFT COLUMN: Languages and Timing (input fields grouped together)
        left_col = QVBoxLayout()
        left_col.setSpacing(12)
        
        # Languages section
        lang_group = QVBoxLayout()
        lang_label = QLabel("Languages:")
        lang_label.setStyleSheet("font-weight: bold; font-size: 9pt;")
        lang_group.addWidget(lang_label)
        lang_inputs = QHBoxLayout()
        lang_inputs.addWidget(QLabel("Source:"))
        self.source_lang_edit = QLineEdit("en")
        self.source_lang_edit.setMaximumWidth(50)
        lang_inputs.addWidget(self.source_lang_edit)
        lang_inputs.addSpacing(10)
        lang_inputs.addWidget(QLabel("Target:"))
        self.target_lang_edit = QLineEdit("nl")
        self.target_lang_edit.setMaximumWidth(50)
        lang_inputs.addWidget(self.target_lang_edit)
        lang_inputs.addStretch()
        lang_group.addLayout(lang_inputs)
        left_col.addLayout(lang_group)
        
        # Timing section
        timing_group = QVBoxLayout()
        timing_label = QLabel("Timing (ms):")
        timing_label.setStyleSheet("font-weight: bold; font-size: 9pt;")
        timing_group.addWidget(timing_label)
        timing_inputs = QHBoxLayout()
        timing_inputs.addWidget(QLabel("Loop:"))
        self.loop_delay_spin = QSpinBox()
        self.loop_delay_spin.setRange(500, 10000)
        self.loop_delay_spin.setValue(4000)
        self.loop_delay_spin.setSuffix(" ms")
        self.loop_delay_spin.setMaximumWidth(90)
        timing_inputs.addWidget(self.loop_delay_spin)
        timing_inputs.addSpacing(10)
        timing_inputs.addWidget(QLabel("Confirm:"))
        self.confirm_delay_spin = QSpinBox()
        self.confirm_delay_spin.setRange(100, 5000)
        self.confirm_delay_spin.setValue(900)
        self.confirm_delay_spin.setSuffix(" ms")
        self.confirm_delay_spin.setMaximumWidth(90)
        timing_inputs.addWidget(self.confirm_delay_spin)
        timing_inputs.addStretch()
        timing_group.addLayout(timing_inputs)
        left_col.addLayout(timing_group)
        
        left_col.addStretch()  # Push content to top
        
        # RIGHT COLUMN: Behavior checkboxes and Save button
        right_col = QVBoxLayout()
        right_col.setSpacing(12)
        
        # Behavior section
        behavior_group = QVBoxLayout()
        behavior_label = QLabel("Behavior:")
        behavior_label.setStyleSheet("font-weight: bold; font-size: 9pt;")
        behavior_group.addWidget(behavior_label)
        
        # Use custom checkboxes with green background and white checkmark when checked
        self.auto_confirm_check = CheckmarkCheckBox("Confirm segments")
        self.auto_confirm_check.setChecked(True)
        self.auto_confirm_check.setToolTip("When checked: Confirm segment with Ctrl+Enter before moving to next. When unchecked: Move to next with Alt+N without confirming")
        behavior_group.addWidget(self.auto_confirm_check)
        self.skip_no_match_check = CheckmarkCheckBox("Skip no match")
        self.skip_no_match_check.setChecked(True)
        behavior_group.addWidget(self.skip_no_match_check)
        right_col.addLayout(behavior_group)
        
        # Save button - centered at bottom of right column
        right_col.addStretch()
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setMinimumHeight(35)
        save_btn.setStyleSheet("font-size: 9pt; font-weight: bold;")
        save_btn.clicked.connect(self.save_settings)
        right_col.addWidget(save_btn)
        
        # Add columns to grid layout
        left_widget = QWidget()
        left_widget.setLayout(left_col)
        right_widget = QWidget()
        right_widget.setLayout(right_col)
        
        settings_layout.addWidget(left_widget, 0, 0)
        settings_layout.addWidget(right_widget, 0, 1)
        
        settings_group.setLayout(settings_layout)
        
        # Create horizontal container for Settings and Activity Log side-by-side
        settings_log_row = QHBoxLayout()
        settings_log_row.setSpacing(15)
        settings_log_row.addWidget(settings_group, 1)  # Settings takes flexible space
        
        # Activity Log on the right
        log_group = QGroupBox("📋 Activity Log")
        log_layout = QVBoxLayout()
        log_layout.setContentsMargins(5, 5, 5, 5)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(200)  # Give it a reasonable minimum height
        self.log_text.setStyleSheet("""
            font-family: 'Consolas', monospace;
            padding: 4px;
            line-height: 1.3;
            font-size: 8pt;
        """)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        settings_log_row.addWidget(log_group, 1)  # Activity Log takes equal flexible space
        
        main_layout.addLayout(settings_log_row)
        
        return tab
    
    def create_tmx_tab(self):
        """Create the TMX manager tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Info
        info = QLabel(
            "Manage your AutoFingers translation memory file.\n"
            "The TMX file stores source-target translation pairs."
        )
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Stats
        self.tmx_stats_label = QLabel("No TMX loaded")
        self.tmx_stats_label.setStyleSheet("padding: 10px; background-color: #F5F5F5; font-weight: bold;")
        layout.addWidget(self.tmx_stats_label)
        
        # Actions
        btn_layout = QVBoxLayout()
        
        create_btn = QPushButton("➕ Create New Empty TMX")
        create_btn.clicked.connect(self.create_empty_tmx)
        btn_layout.addWidget(create_btn)
        
        open_btn = QPushButton("📂 Open TMX in Editor")
        open_btn.clicked.connect(self.open_tmx_in_editor)
        btn_layout.addWidget(open_btn)
        
        import_btn = QPushButton("📥 Import from Supervertaler TM")
        import_btn.clicked.connect(self.import_from_tm)
        btn_layout.addWidget(import_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        return tab
    
    def log(self, message: str):
        """Add message to activity log (thread-safe)"""
        # Skip logging if not on main thread to prevent QTextDocument crashes
        from threading import current_thread, main_thread
        if current_thread() is main_thread():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self._append_log(f"[{timestamp}] {message}")
        else:
            # Queue for main thread
            timestamp = datetime.now().strftime("%H:%M:%S")
            QTimer.singleShot(0, lambda msg=f"[{timestamp}] {message}": self._append_log(msg))
    
    def _append_log(self, message: str):
        """Actually append to log (runs on main thread)"""
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.maximum())
    
    def update_progress_label(self, text: str):
        """Thread-safe progress label update"""
        QTimer.singleShot(0, lambda t=text: self.progress_label.setText(t))
    
    def update_progress_bar(self, value: int):
        """Thread-safe progress bar update"""
        QTimer.singleShot(0, lambda v=value: self.progress_bar.setValue(v))
    
    def browse_tmx(self):
        """Browse for TMX file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select TMX File",
            "",
            "TMX Files (*.tmx);;All Files (*.*)"
        )
        
        if file_path:
            self.tmx_file = file_path
            self.tmx_path_label.setText(file_path)
            self.reload_tmx()
    
    def reload_tmx(self):
        """Reload TMX file"""
        try:
            self.engine = self.AutoFingersEngine(
                tmx_file=self.tmx_file,
                source_lang=self.source_lang_edit.text(),
                target_lang=self.target_lang_edit.text()
            )
            
            # Apply settings
            self.engine.loop_delay = self.loop_delay_spin.value()
            self.engine.confirm_delay = self.confirm_delay_spin.value()
            self.engine.auto_confirm = self.auto_confirm_check.isChecked()
            self.engine.skip_no_match = self.skip_no_match_check.isChecked()
            
            success, message = self.engine.load_tmx()
            
            if success:
                self.log(f"✓ {message}")
                self.tmx_status_label.setText(f"✓ {message}")
                self.tmx_status_label.setStyleSheet("padding: 10px; font-weight: bold; color: green;")
                self.tmx_stats_label.setText(
                    f"📊 TMX Statistics:\n"
                    f"  • Translation Units: {self.engine.tm_count}\n"
                    f"  • Source Language: {self.engine.source_lang}\n"
                    f"  • Target Language: {self.engine.target_lang}"
                )
            else:
                self.log(f"✗ {message}")
                self.tmx_status_label.setText(f"✗ {message}")
                self.tmx_status_label.setStyleSheet("padding: 10px; font-weight: bold; color: red;")
                
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load TMX:\n{str(e)}")
    
    def sync_settings_to_engine(self):
        """Sync current UI settings to the engine"""
        if self.engine:
            self.engine.loop_delay = self.loop_delay_spin.value()
            self.engine.confirm_delay = self.confirm_delay_spin.value()
            self.engine.auto_confirm = self.auto_confirm_check.isChecked()
            self.engine.skip_no_match = self.skip_no_match_check.isChecked()
    
    def process_single(self):
        """Process a single segment"""
        if not self.engine:
            QMessageBox.warning(self, "No TMX", "Please load a TMX file first.")
            return
        
        # Sync current settings to engine before processing
        self.sync_settings_to_engine()
        
        self.log("▶️ Processing single segment...")
        self.progress_label.setText("Processing...")
        
        # Give user time to switch to memoQ
        QApplication.processEvents()
        import time
        time.sleep(1)
        
        try:
            success, message = self.engine.process_single_segment()
            
            # Log match result
            if self.engine.last_source and self.engine.last_match:
                self.log(f"✓ Match: {self.engine.last_match.match_type} ({self.engine.last_match.match_percent}%)")
            else:
                self.log(f"⚠️ No match found for segment")
            
            if success:
                self.log(f"✓ {message}")
                self.progress_label.setText("✓ Segment processed successfully")
            else:
                self.log(f"✗ {message}")
                self.progress_label.setText(f"✗ {message}")
        except Exception as e:
            self.log(f"❌ Error in process_single: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
    
    def toggle_loop(self):
        """Toggle loop mode on/off"""
        if self.is_running:
            # Stop loop
            self.engine.stop()
            self.is_running = False
            self.loop_btn.setText("▶ Loop Mode")
            self.loop_btn.setStyleSheet("font-size: 9pt; font-weight: bold; background-color: #4CAF50; color: white; padding: 2px;")
            self.progress_bar.setVisible(False)
            self.log("⏹️ Loop mode stopped")
        else:
            # Start loop
            if not self.engine:
                QMessageBox.warning(self, "No TMX", "Please load a TMX file first.")
                return
            
            # Sync current settings to engine before starting loop
            self.sync_settings_to_engine()
            
            max_segments = self.loop_segments_spin.value()
            self.is_running = True
            self.loop_btn.setText("⏹ Stop Loop")
            self.loop_btn.setStyleSheet("font-size: 9pt; font-weight: bold; background-color: #F44336; color: white; padding: 2px;")
            
            if max_segments > 0:
                self.progress_bar.setMaximum(max_segments)
                self.progress_bar.setValue(0)
                self.progress_bar.setVisible(True)
            else:
                self.progress_bar.setVisible(False)
            
            self.log(f"▶️ Starting loop mode ({max_segments if max_segments > 0 else '∞'} segments)...")
            
            # Start loop in background thread
            self.loop_thread = threading.Thread(target=self.run_loop, args=(max_segments,), daemon=True)
            self.loop_thread.start()
    
    def run_loop(self, max_segments):
        """Run the loop mode in background thread"""
        import time
        
        segment_count = 0
        
        while self.is_running:
            # Check if reached limit
            if max_segments > 0 and segment_count >= max_segments:
                self.is_running = False
                self.log(f"✓ Completed {segment_count} segments")
                self.update_progress_label(f"✓ Completed {segment_count} segments")
                QTimer.singleShot(0, self.reset_loop_ui)
                break
            
            # Process one segment
            try:
                success, message = self.engine.process_single_segment()
                
                if success:
                    segment_count += 1
                    self.log(f"✓ {message}")
                    self.update_progress_label(f"Processing... ({segment_count} completed)")
                    if max_segments > 0:
                        self.update_progress_bar(segment_count)
                else:
                    self.log(f"✗ {message}")
                    
                    # Stop if no match and not skipping
                    if not self.engine.skip_no_match:
                        self.is_running = False
                        self.update_progress_label(f"Stopped - no translation found")
                        QTimer.singleShot(0, self.reset_loop_ui)
                        break
                
                # Wait between segments
                if self.is_running:
                    time.sleep(self.engine.loop_delay / 1000)
                    
            except Exception as e:
                self.log(f"✗ Error: {str(e)}")
                self.is_running = False
                QTimer.singleShot(0, self.reset_loop_ui)
                break
    
    def reset_loop_ui(self):
        """Reset UI after loop stops"""
        self.loop_btn.setText("▶ Loop Mode")
        self.loop_btn.setStyleSheet("font-size: 9pt; font-weight: bold; background-color: #4CAF50; color: white; padding: 2px;")
        if self.progress_bar.maximum() > 0:
            self.progress_bar.setVisible(True)  # Keep visible to show final progress
        else:
            self.progress_bar.setVisible(False)
    
    def stop_loop(self):
        """Stop loop mode (separate method for keyboard shortcut)"""
        if self.is_running:
            self.toggle_loop()  # Reuse toggle logic when running
        else:
            self.log("Loop mode is not running")
    
    def create_empty_tmx(self):
        """Create a new empty TMX file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Create New TMX File",
            self.tmx_file,
            "TMX Files (*.tmx)"
        )
        
        if file_path:
            temp_engine = self.AutoFingersEngine(
                tmx_file=file_path,
                source_lang=self.source_lang_edit.text(),
                target_lang=self.target_lang_edit.text()
            )
            
            if temp_engine.create_empty_tmx():
                self.log(f"✓ Created empty TMX: {file_path}")
                self.tmx_file = file_path
                self.tmx_path_label.setText(file_path)
                self.reload_tmx()
            else:
                QMessageBox.critical(self, "Error", "Failed to create TMX file")
    
    def open_tmx_in_editor(self):
        """Open TMX file in external editor"""
        import subprocess
        try:
            if sys.platform == 'win32':
                os.startfile(self.tmx_file)
            elif sys.platform == 'darwin':
                subprocess.call(['open', self.tmx_file])
            else:
                subprocess.call(['xdg-open', self.tmx_file])
            self.log(f"📂 Opened TMX in editor: {self.tmx_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open TMX file:\n{str(e)}")
    
    def import_from_tm(self):
        """Import translations from Supervertaler TM database"""
        QMessageBox.information(
            self,
            "Feature Coming Soon",
            "TM import functionality will be added in the next update!\n\n"
            "For now, you can manually edit the TMX file or use the\n"
            "AutoHotkey version to populate your translation memory."
        )
    
    def load_settings(self):
        """Load saved settings from file"""
        try:
            settings_file = Path("user data_private" if ENABLE_PRIVATE_FEATURES else "user data") / "autofingers_settings.json"
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Apply settings to UI
                self.loop_delay_spin.setValue(settings.get('loop_delay', 4000))
                self.confirm_delay_spin.setValue(settings.get('confirm_delay', 900))
                self.auto_confirm_check.setChecked(settings.get('auto_confirm', True))
                self.skip_no_match_check.setChecked(settings.get('skip_no_match', True))
                # Backward compatibility: if old settings had use_down_arrow=True, set auto_confirm=False
                if settings.get('use_down_arrow', False):
                    self.auto_confirm_check.setChecked(False)
                
                self.log("✓ Settings loaded")
        except Exception as e:
            self.log(f"⚠️ Could not load settings: {e}")
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            settings = {
                'loop_delay': self.loop_delay_spin.value(),
                'confirm_delay': self.confirm_delay_spin.value(),
                'auto_confirm': self.auto_confirm_check.isChecked(),
                'skip_no_match': self.skip_no_match_check.isChecked()
            }
            
            settings_file = Path("user data_private" if ENABLE_PRIVATE_FEATURES else "user data") / "autofingers_settings.json"
            settings_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
            
            self.log("💾 Settings saved")
            QMessageBox.information(self, "Saved", "Settings saved successfully!")
        except Exception as e:
            self.log(f"⚠️ Could not save settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save settings:\n{str(e)}")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Supervertaler Qt")
    app.setOrganizationName("Supervertaler")
    
    window = SupervertalerQt()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
