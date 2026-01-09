"""   
Supervertaler
=============
The Ultimate Translation Workbench.
Modern PyQt6 interface with specialised modules to handle any problem.
Version: 1.9.47 (Code Cleanup)
Release Date: December 18, 2025
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
- Superlookup with global hotkey (Ctrl+Alt+L)
- Detachable Log window for multi-monitor setups
- Modern theme system (6 themes + custom editor)
- AutoFingers automation for memoQ with TagCleaner module
- memoQ bilingual DOCX import/export
- Bilingual Table export/import for review workflow
- SQLite-based translation memory with FTS5 search
- Professional TMX editor
- Spellcheck integration with Hunspell and custom dictionary support

Author: Michael Beijer
License: MIT
"""

# Version Information.
__version__ = "1.9.87"
__phase__ = "0.9"
__release_date__ = "2026-01-07"
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


def get_resource_path(relative_path: str) -> Path:
    """Get absolute path to resource, works for dev and for PyInstaller bundled app."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running as compiled executable (PyInstaller)
        base_path = Path(sys._MEIPASS)
    else:
        # Running in development
        base_path = Path(__file__).parent
    return base_path / relative_path
import threading
import time  # For delays in Superlookup
import re

# Fix encoding for Windows console (UTF-8 support)
# Only set if stdout/stderr exist (they're None in PyInstaller --windowed mode)
if sys.platform == 'win32':
    import io
    if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if sys.stderr is not None and hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# External dependencies
import pyperclip  # For clipboard operations in Superlookup
from modules.superlookup import SuperlookupEngine  # Superlookup engine
from modules.voice_dictation_lite import QuickDictationThread  # Voice dictation
from modules.voice_commands import VoiceCommandManager, VoiceCommand, ContinuousVoiceListener  # Voice commands (Talon-style)
from modules.statuses import (
    STATUSES,
    DEFAULT_STATUS,
    StatusDefinition,
    get_status,
    match_memoq_status,
    compose_memoq_status,
)
from modules import file_dialog_helper as fdh  # File dialog helper with last directory memory
from modules.spellcheck_manager import SpellcheckManager, get_spellcheck_manager  # Spellcheck with Hunspell
from modules.find_replace_qt import (
    FindReplaceHistory,
    FindReplaceOperation,
    FindReplaceSet,
    FindReplaceSetsManager,
    HistoryComboBox,
)  # F&R History and Sets


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
        QProgressBar, QProgressDialog, QFormLayout, QTabBar, QPlainTextEdit, QAbstractItemDelegate,
        QFrame, QListWidget, QListWidgetItem, QStackedWidget, QTreeWidget, QTreeWidgetItem,
        QScrollArea, QSizePolicy, QSlider, QToolButton
    )
    from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal, QObject, QUrl
    from PyQt6.QtGui import QFont, QAction, QKeySequence, QIcon, QTextOption, QColor, QDesktopServices, QTextCharFormat, QTextCursor, QBrush, QSyntaxHighlighter, QPalette, QTextBlockFormat
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
            print("[Superlookup] AHK process terminated on exit")
        except:
            try:
                _ahk_process.kill()
                print("[Superlookup] AHK process killed on exit")
            except:
                pass

# Register cleanup function to run on Python exit
atexit.register(cleanup_ahk_process)


# ============================================================================
# ============================================================================
# DATA MODELS
# ============================================================================

# ============================================================================
# INLINE FORMATTING TAG UTILITIES
# ============================================================================

def runs_to_tagged_text(paragraphs) -> str:
    """
    Convert Word document paragraphs with run formatting to HTML-tagged text.
    
    Args:
        paragraphs: List of python-docx Paragraph objects
        
    Returns:
        String with HTML tags for formatting (e.g., "<b>bold</b> normal <i>italic</i>")
    """
    result_parts = []
    
    for paragraph in paragraphs:
        for run in paragraph.runs:
            text = run.text
            if not text:
                continue
            
            # Determine which tags to apply
            is_bold = run.bold == True
            is_italic = run.italic == True
            is_underline = run.underline == True
            
            # Build tagged text
            if is_bold or is_italic or is_underline:
                # Open tags (order: bold, italic, underline)
                if is_bold:
                    text = f"<b>{text}"
                if is_italic:
                    text = f"<i>{text}" if not is_bold else text.replace("<b>", "<b><i>", 1)
                if is_underline:
                    if is_bold and is_italic:
                        text = text.replace("<b><i>", "<b><i><u>", 1)
                    elif is_bold:
                        text = text.replace("<b>", "<b><u>", 1)
                    elif is_italic:
                        text = text.replace("<i>", "<i><u>", 1)
                    else:
                        text = f"<u>{text}"
                
                # Close tags (reverse order: underline, italic, bold)
                if is_underline:
                    text = f"{text}</u>"
                if is_italic:
                    text = f"{text}</i>"
                if is_bold:
                    text = f"{text}</b>"
            
            result_parts.append(text)
    
    return ''.join(result_parts)


def strip_formatting_tags(text: str) -> str:
    """
    Remove HTML formatting tags from text, leaving plain text.
    
    Args:
        text: Text with HTML tags like <b>, </b>, <i>, </i>, <u>, </u>
        
    Returns:
        Plain text without tags
    """
    import re
    # Remove <b>, </b>, <i>, </i>, <u>, </u> tags
    return re.sub(r'</?[biu]>', '', text)


def has_formatting_tags(text: str) -> bool:
    """
    Check if text contains any formatting tags.
    
    Args:
        text: Text to check
        
    Returns:
        True if text contains <b>, <i>, or <u> tags
    """
    import re
    return bool(re.search(r'</?[biu]>', text))


def apply_formatting_tags(text: str, tag: str) -> str:
    """
    Wrap text with the specified formatting tag.
    
    Args:
        text: Text to wrap
        tag: Tag name ('b', 'i', or 'u')
        
    Returns:
        Tagged text like "<b>text</b>"
    """
    if tag in ('b', 'i', 'u'):
        return f"<{tag}>{text}</{tag}>"
    return text


def get_formatted_html_display(text: str) -> str:
    """
    Convert our simple tags to HTML for rich text display.
    
    Args:
        text: Text with <b>, <i>, <u> tags
        
    Returns:
        HTML string suitable for QTextEdit.setHtml()
    """
    # Escape HTML entities first (except our tags)
    import html
    
    # Temporarily replace our tags with placeholders
    text = text.replace('<b>', '\x00B_OPEN\x00')
    text = text.replace('</b>', '\x00B_CLOSE\x00')
    text = text.replace('<i>', '\x00I_OPEN\x00')
    text = text.replace('</i>', '\x00I_CLOSE\x00')
    text = text.replace('<u>', '\x00U_OPEN\x00')
    text = text.replace('</u>', '\x00U_CLOSE\x00')
    
    # Escape other HTML
    text = html.escape(text)
    
    # Restore our tags as real HTML
    text = text.replace('\x00B_OPEN\x00', '<b>')
    text = text.replace('\x00B_CLOSE\x00', '</b>')
    text = text.replace('\x00I_OPEN\x00', '<i>')
    text = text.replace('\x00I_CLOSE\x00', '</i>')
    text = text.replace('\x00U_OPEN\x00', '<u>')
    text = text.replace('\x00U_CLOSE\x00', '</u>')
    
    return text


def tagged_text_to_runs(text: str) -> list:
    """
    Parse text with HTML formatting tags and return a list of runs with formatting info.
    
    Args:
        text: Text with <b>, <i>, <u> tags (can be nested)
        
    Returns:
        List of dicts: [{'text': str, 'bold': bool, 'italic': bool, 'underline': bool}, ...]
    
    Example:
        "Hello <b>bold</b> and <i>italic</i> world"
        -> [{'text': 'Hello ', 'bold': False, 'italic': False, 'underline': False},
            {'text': 'bold', 'bold': True, 'italic': False, 'underline': False},
            {'text': ' and ', 'bold': False, 'italic': False, 'underline': False},
            {'text': 'italic', 'bold': False, 'italic': True, 'underline': False},
            {'text': ' world', 'bold': False, 'italic': False, 'underline': False}]
    """
    import re
    
    runs = []
    
    # Track current formatting state
    is_bold = False
    is_italic = False
    is_underline = False
    
    # Pattern to match opening/closing tags
    tag_pattern = re.compile(r'(</?[biu]>)')
    
    # Split text by tags, keeping the tags as delimiters
    parts = tag_pattern.split(text)
    
    current_text = ""
    
    for part in parts:
        if part == '<b>':
            # Save any accumulated text before changing state
            if current_text:
                runs.append({
                    'text': current_text,
                    'bold': is_bold,
                    'italic': is_italic,
                    'underline': is_underline
                })
                current_text = ""
            is_bold = True
        elif part == '</b>':
            if current_text:
                runs.append({
                    'text': current_text,
                    'bold': is_bold,
                    'italic': is_italic,
                    'underline': is_underline
                })
                current_text = ""
            is_bold = False
        elif part == '<i>':
            if current_text:
                runs.append({
                    'text': current_text,
                    'bold': is_bold,
                    'italic': is_italic,
                    'underline': is_underline
                })
                current_text = ""
            is_italic = True
        elif part == '</i>':
            if current_text:
                runs.append({
                    'text': current_text,
                    'bold': is_bold,
                    'italic': is_italic,
                    'underline': is_underline
                })
                current_text = ""
            is_italic = False
        elif part == '<u>':
            if current_text:
                runs.append({
                    'text': current_text,
                    'bold': is_bold,
                    'italic': is_italic,
                    'underline': is_underline
                })
                current_text = ""
            is_underline = True
        elif part == '</u>':
            if current_text:
                runs.append({
                    'text': current_text,
                    'bold': is_bold,
                    'italic': is_italic,
                    'underline': is_underline
                })
                current_text = ""
            is_underline = False
        else:
            # Regular text - accumulate it
            current_text += part
    
    # Don't forget any remaining text
    if current_text:
        runs.append({
            'text': current_text,
            'bold': is_bold,
            'italic': is_italic,
            'underline': is_underline
        })
    
    return runs


# ============================================================================
# MEMOQ TAG UTILITIES (for tag insertion shortcuts)
# ============================================================================

def extract_memoq_tags(text: str) -> list:
    """
    Extract all memoQ-style tags from text in order of appearance.
    
    memoQ uses several tag types:
    - Paired opening tags: [1}, [2}, [3} etc.
    - Paired closing tags: {1], {2], {3] etc.
    - Standalone tags: [1], [2], [3] etc. (e.g., for tabs, special characters)
    
    Args:
        text: Source text containing tags
        
    Returns:
        List of tag strings in order of appearance: ['[1}', '{1]', '[2]', ...]
    """
    import re
    # Match:
    # - Opening paired tags: [N}
    # - Closing paired tags: {N]
    # - Standalone tags: [N]
    pattern = r'(\[\d+\}|\{\d+\]|\[\d+\])'
    return re.findall(pattern, text)


def extract_html_tags(text: str) -> list:
    """
    Extract all HTML/XML tags from text in order of appearance.
    
    Supports common formatting tags used in translation:
    - Opening tags: <b>, <i>, <u>, <li>, <p>, <span>, etc.
    - Closing tags: </b>, </i>, </u>, </li>, </p>, </span>, etc.
    - Self-closing tags: <br/>, <hr/>, etc.
    
    Args:
        text: Source text containing HTML tags
        
    Returns:
        List of tag strings in order of appearance: ['<li>', '</li>', '<b>', '</b>', ...]
    """
    import re
    # Match HTML/XML tags: <tagname>, </tagname>, <tagname/>, <tagname attr="value">
    pattern = r'(</?[a-zA-Z][a-zA-Z0-9]*(?:\s+[^>]*)?>)'
    return re.findall(pattern, text)


def extract_all_tags(text: str) -> list:
    """
    Extract all tags (memoQ and HTML) from text in order of appearance.
    
    Args:
        text: Source text containing tags
        
    Returns:
        List of all tag strings in order of appearance
    """
    import re
    # Combined pattern for both memoQ tags and HTML tags
    # memoQ: [N}, {N], [N]
    # HTML: <tag>, </tag>, <tag/>, <tag attr="value"> - includes hyphenated tags like li-o, li-b
    pattern = r'(\[\d+\}|\{\d+\]|\[\d+\]|</?[a-zA-Z][a-zA-Z0-9-]*(?:\s+[^>]*)?>)'
    return re.findall(pattern, text)


def count_pipe_symbols(text: str) -> int:
    """Count the number of CafeTran pipe symbols in text."""
    return text.count('|')


def get_next_pipe_count_needed(source_text: str, target_text: str) -> int:
    """
    Get how many more pipe symbols are needed in target to match source.
    
    Args:
        source_text: Source segment text with pipe symbols
        target_text: Current target text
        
    Returns:
        Number of additional pipe symbols needed (0 if target has enough or more)
    """
    source_pipes = count_pipe_symbols(source_text)
    target_pipes = count_pipe_symbols(target_text)
    return max(0, source_pipes - target_pipes)


def get_tag_pair(tag_number: int) -> tuple:
    """
    Get opening and closing tag pair for a given number.
    
    Args:
        tag_number: The tag number (1, 2, 3, etc.)
        
    Returns:
        Tuple of (opening_tag, closing_tag) e.g. ('[1}', '{1]')
    """
    return (f'[{tag_number}}}', f'{{{tag_number}]')


def find_next_unused_tag(source_text: str, target_text: str) -> str:
    """
    Find the next tag from source that hasn't been used in target yet.
    
    Supports both memoQ tags ([1}, {1], [1]) and HTML tags (<li>, </li>, <b>, etc.)
    
    Args:
        source_text: Source segment text with tags
        target_text: Current target text (may have some tags already)
        
    Returns:
        The next tag to insert, or empty string if all tags are used
    """
    # Use combined extraction for both memoQ and HTML 	
    source_tags = extract_all_tags(source_text)
    target_tags = extract_all_tags(target_text)
    
    # Count occurrences in target
    from collections import Counter
    target_tag_counts = Counter(target_tags)
    source_tag_counts = Counter(source_tags)
    
    # Find first tag that needs more occurrences in target
    for tag in source_tags:
        source_count = source_tag_counts[tag]
        target_count = target_tag_counts.get(tag, 0)
        if target_count < source_count:
            return tag
    
    return ""  # All tags already in target


def get_wrapping_tag_pair(source_text: str, target_text: str) -> tuple:
    """
    Get the next available tag pair for wrapping selected text.
    
    Finds the first tag number from source where either opening or closing
    tag is not yet in target.
    
    Args:
        source_text: Source segment text with tags
        target_text: Current target text
        
    Returns:
        Tuple of (opening_tag, closing_tag) or (None, None) if no pairs available
    """
    import re
    
    # Extract all tag numbers from source
    source_tags = extract_memoq_tags(source_text)
    if not source_tags:
        return (None, None)
    
    # Get unique tag numbers in order
    tag_numbers = []
    for tag in source_tags:
        match = re.search(r'\d+', tag)
        if match:
            num = int(match.group())
            if num not in tag_numbers:
                tag_numbers.append(num)
    
    target_tags = extract_memoq_tags(target_text)
    
    # Find first tag number where pair is not complete in target
    for num in tag_numbers:
        opening, closing = get_tag_pair(num)
        if opening not in target_tags or closing not in target_tags:
            return (opening, closing)
    
    return (None, None)


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
    list_number: Optional[int] = None  # For numbered lists: 1, 2, 3, etc. None for bullets or non-lists
    list_type: str = ""  # "numbered", "bullet", or "" for non-list items
    file_id: Optional[int] = None  # ID of the file this segment belongs to (for multi-file projects)
    file_name: str = ""  # Name of the file this segment belongs to (for multi-file projects)
    
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
    nt_settings: Dict[str, Any] = None  # Store activated non-translatables settings
    spellcheck_settings: Dict[str, Any] = None  # Store spellcheck settings {enabled, language}
    id: int = None  # Unique project ID for TM activation tracking
    original_docx_path: str = None  # Path to original DOCX for structure-preserving export
    trados_source_path: str = None  # Path to original Trados bilingual DOCX for round-trip export
    memoq_source_path: str = None  # Path to original memoQ bilingual DOCX for round-trip export
    cafetran_source_path: str = None  # Path to original CafeTran bilingual DOCX for round-trip export
    sdlppx_source_path: str = None  # Path to original Trados SDLPPX package for SDLRPX export
    original_txt_path: str = None  # Path to original simple text file for round-trip export
    concordance_geometry: Dict[str, int] = None  # Window geometry for Concordance Search {x, y, width, height}
    # Multi-file project support
    files: List[Dict[str, Any]] = None  # List of files in project: [{id, name, path, type, segment_count, ...}]
    is_multifile: bool = False  # True if this is a multi-file project
    
    def __post_init__(self):
        if self.segments is None:
            self.segments = []
        if self.files is None:
            self.files = []
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
        if self.nt_settings is None:
            self.nt_settings = {}
        if self.spellcheck_settings is None:
            self.spellcheck_settings = {}
        # Generate ID if not set (for backward compatibility with old projects)
        if self.id is None:
            import hashlib
            # Create stable ID from project name + created timestamp
            id_source = f"{self.name}_{self.created}"
            self.id = int(hashlib.md5(id_source.encode()).hexdigest()[:8], 16)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.
        
        Structure is organized for human readability when opened in a text editor:
        1. Project identification (name, languages, dates, id)
        2. Settings (prompts, TM, termbases, spellcheck, etc.)
        3. Source file paths
        4. UI state (concordance geometry)
        5. Segments (at the end - the actual translation content)
        """
        # Start with core project metadata
        result = {
            'name': self.name,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
            'created': self.created,
            'modified': self.modified,
            'id': self.id  # Save project ID
        }
        
        # Add settings (prompts, TM, termbases, etc.)
        if hasattr(self, 'prompt_settings'):
            result['prompt_settings'] = self.prompt_settings
        if self.tm_settings:
            result['tm_settings'] = self.tm_settings
        if self.termbase_settings:
            result['termbase_settings'] = self.termbase_settings
        if self.nt_settings:
            result['nt_settings'] = self.nt_settings
        if self.spellcheck_settings:
            result['spellcheck_settings'] = self.spellcheck_settings
        
        # Add source file paths
        if self.original_docx_path:
            result['original_docx_path'] = self.original_docx_path
        if self.trados_source_path:
            result['trados_source_path'] = self.trados_source_path
        if self.memoq_source_path:
            result['memoq_source_path'] = self.memoq_source_path
        if self.cafetran_source_path:
            result['cafetran_source_path'] = self.cafetran_source_path
        if self.sdlppx_source_path:
            result['sdlppx_source_path'] = self.sdlppx_source_path
        if self.original_txt_path:
            result['original_txt_path'] = self.original_txt_path
        
        # Add UI state
        if self.concordance_geometry:
            result['concordance_geometry'] = self.concordance_geometry
        
        # Add multi-file project data
        if self.is_multifile:
            result['is_multifile'] = self.is_multifile
        if self.files:
            result['files'] = self.files
        
        # Add segments LAST (so they appear at the end of the file)
        result['segments'] = [seg.to_dict() for seg in self.segments]
        
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
        # Store non-translatables settings if they exist
        if 'nt_settings' in data:
            project.nt_settings = data['nt_settings']
        # Store spellcheck settings if they exist
        if 'spellcheck_settings' in data:
            project.spellcheck_settings = data['spellcheck_settings']
        # Store original DOCX path if it exists
        if 'original_docx_path' in data:
            project.original_docx_path = data['original_docx_path']
        # Store Trados source path if it exists
        if 'trados_source_path' in data:
            project.trados_source_path = data['trados_source_path']
        # Store memoQ source path if it exists
        if 'memoq_source_path' in data:
            project.memoq_source_path = data['memoq_source_path']
        # Store CafeTran source path if it exists
        if 'cafetran_source_path' in data:
            project.cafetran_source_path = data['cafetran_source_path']
        # Store SDLPPX source path if it exists
        if 'sdlppx_source_path' in data:
            project.sdlppx_source_path = data['sdlppx_source_path']
        # Store original TXT path if it exists
        if 'original_txt_path' in data:
            project.original_txt_path = data['original_txt_path']
        # Store concordance window geometry if it exists
        if 'concordance_geometry' in data:
            project.concordance_geometry = data['concordance_geometry']
        # Store multi-file project data if it exists
        if 'is_multifile' in data:
            project.is_multifile = data['is_multifile']
        if 'files' in data:
            project.files = data['files']
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
            # Ctrl+, (comma): Insert next memoQ tag or wrap selection with tag pair
            elif event.key() == Qt.Key.Key_Comma:
                self._insert_next_tag_or_wrap_selection()
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
    
    def _insert_next_tag_or_wrap_selection(self):
        """
        Insert the next memoQ tag, HTML tag, or CafeTran pipe symbol from source, or wrap selection.
        
        Behavior:
        - If text is selected: Wrap it with the next available tag pair [N}selection{N] or |selection|
        - If no selection: Insert the next unused tag/pipe from source at cursor position
        
        Supports:
        - memoQ tags: [1}, {1], [2}, {2], etc.
        - HTML/XML tags: <li>, </li>, <b>, </b>, <i>, </i>, etc.
        - CafeTran pipe symbols: |
        
        Shortcut: Ctrl+, (comma)
        """
        # Get the main window and current segment
        if not self.table_widget or self.current_row is None:
            return
        
        # Navigate up to find main window
        main_window = self.table_widget.parent()
        while main_window and not hasattr(main_window, 'current_project'):
            main_window = main_window.parent()
        
        if not main_window or not hasattr(main_window, 'current_project'):
            return
        
        if not main_window.current_project or self.current_row >= len(main_window.current_project.segments):
            return
        
        segment = main_window.current_project.segments[self.current_row]
        source_text = segment.source
        current_target = self.toPlainText()
        
        # Check what type of tags are in the source
        has_memoq_tags = bool(extract_memoq_tags(source_text))
        has_html_tags = bool(extract_html_tags(source_text))
        has_any_tags = has_memoq_tags or has_html_tags
        has_pipe_symbols = '|' in source_text
        
        # Check if there's a selection
        cursor = self.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            
            # Try memoQ tag pair first
            if has_memoq_tags:
                opening_tag, closing_tag = get_wrapping_tag_pair(source_text, current_target)
                if opening_tag and closing_tag:
                    wrapped_text = f"{opening_tag}{selected_text}{closing_tag}"
                    cursor.insertText(wrapped_text)
                    if hasattr(main_window, 'log'):
                        main_window.log(f"🏷️ Wrapped selection with {opening_tag}...{closing_tag}")
                    return
            
            # Try CafeTran pipe symbols
            if has_pipe_symbols:
                pipes_needed = get_next_pipe_count_needed(source_text, current_target)
                if pipes_needed >= 2:
                    # Wrap with pipes
                    wrapped_text = f"|{selected_text}|"
                    cursor.insertText(wrapped_text)
                    if hasattr(main_window, 'log'):
                        main_window.log(f"🏷️ Wrapped selection with |...|")
                    return
            
            if hasattr(main_window, 'log'):
                main_window.log("⚠️ No tag pairs available from source")
        else:
            # No selection - insert next unused tag or pipe at cursor
            
            # Try memoQ tags and HTML tags (find_next_unused_tag handles both)
            if has_any_tags:
                next_tag = find_next_unused_tag(source_text, current_target)
                if next_tag:
                    cursor.insertText(next_tag)
                    if hasattr(main_window, 'log'):
                        main_window.log(f"🏷️ Inserted tag: {next_tag}")
                    return
            
            # Try CafeTran pipe symbols
            if has_pipe_symbols:
                pipes_needed = get_next_pipe_count_needed(source_text, current_target)
                if pipes_needed > 0:
                    cursor.insertText('|')
                    if hasattr(main_window, 'log'):
                        main_window.log(f"🏷️ Inserted pipe symbol (|)")
                    return
            
            if hasattr(main_window, 'log'):
                main_window.log("✓ All tags from source already in target")


class ReadOnlyGridTextEditor(QTextEdit):
    """Read-only QTextEdit for source cells - allows easy text selection"""
    
    # Class variable for tag highlight color (shared across all instances)
    tag_highlight_color = '#7f0001'  # Default memoQ dark red
    
    table_widget = None  # Will be set by delegate
    current_row = None  # Track which row this editor is in
    allow_source_edit = False  # Will be set by delegate based on settings
    
    def __init__(self, text: str = "", parent=None, row: int = -1):
        super().__init__(parent)
        self.row = row  # Store row number for Tab cycling
        self.table_ref = parent  # Store table reference (parent is the table)
        self.setReadOnly(True)  # Prevent typing but allow selection
        self.setPlainText(text)

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
        # Background and text colors now managed by theme system
        self.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 0px 4px 0px 0px;
            }
            QTextEdit:focus {
                border: 1px solid #2196F3;
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
        # With zero-width spaces inserted after invisible character markers,
        # normal WordWrap will work correctly
        wrap_mode = QTextOption.WrapMode.WordWrap

        self.setWordWrapMode(wrap_mode)
        self.setAcceptRichText(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        text_option = QTextOption()
        text_option.setWrapMode(wrap_mode)
        doc.setDefaultTextOption(text_option)
        
        # Set minimum height to 0 - let content determine size
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)  # Qt's max int
        
        # Store termbase matches for this cell (for tooltip and double-click)
        self.termbase_matches = {}
        
        # Enable mouse tracking for hover tooltips
        self.setMouseTracking(True)

        # Add syntax highlighter for tags (no spellcheck for source cells)
        # Get invisible char color from main window if available
        main_window = self._get_main_window()
        invisible_char_color = main_window.invisible_char_color if main_window and hasattr(main_window, 'invisible_char_color') else '#999999'
        self.highlighter = TagHighlighter(self.document(), self.tag_highlight_color, invisible_char_color, enable_spellcheck=False)

        # Store raw text (with tags) for mode switching
        self._raw_text = text
    
    def keyPressEvent(self, event):
        """Override to fix clipboard and word navigation when invisible characters shown"""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QTextCursor
        
        # Check for Ctrl+C (copy)
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_C:
            # Get selected text
            cursor = self.textCursor()
            if cursor.hasSelection():
                selected_text = cursor.selectedText()
                # Reverse invisible character replacements before copying
                main_window = self._get_main_window()
                if main_window and hasattr(main_window, 'reverse_invisible_replacements'):
                    clean_text = main_window.reverse_invisible_replacements(selected_text)
                    # Also replace paragraph separator with newline (Qt uses U+2029)
                    clean_text = clean_text.replace('\u2029', '\n')
                    # Set clipboard with clean text
                    clipboard = QApplication.clipboard()
                    clipboard.setText(clean_text)
                    return  # Don't call parent - we handled it
        
        # Handle Ctrl+Arrow word navigation when invisibles are shown
        main_window = self._get_main_window()
        if main_window and hasattr(main_window, 'invisible_display_settings'):
            if main_window.invisible_display_settings.get('spaces', False):
                ctrl_only = event.modifiers() == Qt.KeyboardModifier.ControlModifier
                ctrl_shift = event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier)
                
                if (ctrl_only or ctrl_shift) and event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right):
                    cursor = self.textCursor()
                    text = self.toPlainText()
                    pos = cursor.position()
                    word_chars = ('·', '\u200B', '\n', '\t', '→', '°', '¶', ' ')
                    
                    if event.key() == Qt.Key.Key_Right:
                        # Move to end of current word, then skip delimiters to start of next word
                        # First skip any delimiters we're on
                        while pos < len(text) and text[pos] in word_chars:
                            pos += 1
                        # Then skip to end of word (next delimiter)
                        while pos < len(text) and text[pos] not in word_chars:
                            pos += 1
                    else:  # Key_Left
                        # Move backwards: skip delimiters, then find start of word
                        if pos > 0:
                            pos -= 1
                        # Skip any delimiters
                        while pos > 0 and text[pos] in word_chars:
                            pos -= 1
                        # Find start of word
                        while pos > 0 and text[pos - 1] not in word_chars:
                            pos -= 1
                    
                    # Apply cursor movement
                    if ctrl_shift:
                        cursor.setPosition(pos, QTextCursor.MoveMode.KeepAnchor)
                    else:
                        cursor.setPosition(pos)
                    self.setTextCursor(cursor)
                    return
        
        # Arrow Up/Down: memoQ-style segment navigation at cell boundaries
        # When cursor is at top line and Up is pressed, go to previous segment
        # When cursor is at bottom line and Down is pressed, go to next segment
        if event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down) and event.modifiers() == Qt.KeyboardModifier.NoModifier:
            cursor = self.textCursor()
            
            # Get current cursor position info
            current_block = cursor.block()
            doc = self.document()
            first_block = doc.firstBlock()
            last_block = doc.lastBlock()
            
            # Get table reference
            table = self.table_ref if hasattr(self, 'table_ref') else self.parent()
            
            if event.key() == Qt.Key.Key_Up:
                # Check if we're on the first line
                if current_block == first_block:
                    # Navigate to previous segment
                    main_window = self._get_main_window()
                    if main_window and hasattr(main_window, 'go_to_previous_segment'):
                        # Get cursor column position for smart positioning
                        col_in_line = cursor.positionInBlock()
                        # Navigate and let go_to_previous_segment position cursor in target cell
                        main_window.go_to_previous_segment(target_column=col_in_line, to_last_line=True)
                        
                        # Now move focus from target to source cell, preserving column position
                        if table:
                            current_row = table.currentRow()
                            source_widget = table.cellWidget(current_row, 2)  # Column 2 is Source
                            if source_widget and hasattr(source_widget, 'textCursor'):
                                new_cursor = source_widget.textCursor()
                                src_doc = source_widget.document()
                                src_last_block = src_doc.lastBlock()
                                new_cursor.setPosition(src_last_block.position())
                                line_length = src_last_block.length() - 1
                                target_pos = min(col_in_line, max(0, line_length))
                                new_cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor, target_pos)
                                source_widget.setTextCursor(new_cursor)
                                source_widget.setFocus()
                        return
            
            elif event.key() == Qt.Key.Key_Down:
                # Check if we're on the last line
                if current_block == last_block:
                    # Navigate to next segment
                    main_window = self._get_main_window()
                    if main_window and hasattr(main_window, 'go_to_next_segment'):
                        # Get cursor column position for smart positioning
                        col_in_line = cursor.positionInBlock()
                        # Navigate and let go_to_next_segment position cursor in target cell
                        main_window.go_to_next_segment(target_column=col_in_line, to_first_line=True)
                        
                        # Now move focus from target to source cell, preserving column position
                        if table:
                            current_row = table.currentRow()
                            source_widget = table.cellWidget(current_row, 2)  # Column 2 is Source
                            if source_widget and hasattr(source_widget, 'textCursor'):
                                new_cursor = source_widget.textCursor()
                                src_doc = source_widget.document()
                                src_first_block = src_doc.firstBlock()
                                new_cursor.setPosition(src_first_block.position())
                                line_length = src_first_block.length() - 1
                                target_pos = min(col_in_line, max(0, line_length))
                                new_cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor, target_pos)
                                source_widget.setTextCursor(new_cursor)
                                source_widget.setFocus()
                        return
        
        # Tab key: Cycle to target cell (column 3) in same row
        if event.key() == Qt.Key.Key_Tab and event.modifiers() == Qt.KeyboardModifier.NoModifier:
            table = self.table_ref if hasattr(self, 'table_ref') else self.parent()
            if table and self.row >= 0:
                target_widget = table.cellWidget(self.row, 3)  # Column 3 is Target
                if target_widget:
                    target_widget.setFocus()
                    table.setCurrentCell(self.row, 3)
                    return
        
        super().keyPressEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """Handle double-click to select words properly when invisibles are shown"""
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QTextCursor
        
        main_window = self._get_main_window()
        # Check if invisible spaces are being shown
        if main_window and hasattr(main_window, 'invisible_display_settings'):
            if main_window.invisible_display_settings.get('spaces', False):
                # Get cursor position at click
                cursor = self.cursorForPosition(event.pos())
                pos = cursor.position()
                text = self.toPlainText()
                
                # Find word boundaries using middle dot (·) or zero-width space as delimiters
                # Find start of word (search backwards for · or start of text)
                start = pos
                while start > 0 and text[start - 1] not in ('·', '\u200B', '\n', '\t', '→', '°', '¶'):
                    start -= 1
                
                # Find end of word (search forwards for · or end of text)
                end = pos
                while end < len(text) and text[end] not in ('·', '\u200B', '\n', '\t', '→', '°', '¶'):
                    end += 1
                
                # Select the word
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
                self.setTextCursor(cursor)
                return
        
        # Default behavior
        super().mouseDoubleClickEvent(event)
    
    def _get_main_window(self):
        """Get the main application window by traversing the parent hierarchy"""
        table = self.table_ref if hasattr(self, 'table_ref') else self.parent()
        if not table:
            return None
        main_window = table.parent()
        while main_window and not hasattr(main_window, 'go_to_first_segment'):
            main_window = main_window.parent()
        return main_window
    
    def update_display_mode(self, text: str, show_tags: bool):
        """
        Update the display based on tag view mode.
        
        Args:
            text: The raw text (with HTML tags like <b>bold</b>)
            show_tags: If True, show raw tags. If False, show formatted WYSIWYG.
        """
        self._raw_text = text
        
        if show_tags:
            # Show raw tags as plain text
            self.setPlainText(text)
        else:
            # Show WYSIWYG - convert tags to actual formatting
            html = get_formatted_html_display(text)
            self.setHtml(html)
    
    def get_raw_text(self) -> str:
        """Get the raw text with tags, regardless of display mode."""
        return getattr(self, '_raw_text', self.toPlainText())

    def highlight_termbase_matches(self, matches_dict: Dict):
        """
        Highlight termbase matches in the text using the configured style.
        Does NOT change the widget - just adds formatting to existing text.
        
        Supported styles (configured in Settings > View Settings):
        - 'background': Pastel green background colors based on priority (default)
        - 'dotted': Subtle dotted underline (IDE/code editor style)
        - 'semibold': Slightly bolder text with tinted color (typographic)
        
        Args:
            matches_dict: Dictionary of {term: {'translation': str, 'priority': int}} or {term: str}
        """
        from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor, QFont
        
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
        
        # Get highlight style from main window settings
        highlight_style = 'background'  # default
        dotted_color = '#808080'  # default medium gray (more visible)
        parent = self.parent()
        while parent:
            if hasattr(parent, 'termbase_highlight_style'):
                highlight_style = getattr(parent, 'termbase_highlight_style', 'background')
                dotted_color = getattr(parent, 'termbase_dotted_color', '#808080')
                break
            elif hasattr(parent, 'load_general_settings'):
                settings = parent.load_general_settings()
                highlight_style = settings.get('termbase_highlight_style', 'semibold')
                dotted_color = settings.get('termbase_dotted_color', '#808080')
                break
            parent = parent.parent() if hasattr(parent, 'parent') else None
        
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
            ranking = match_info.get('ranking', None)
            forbidden = match_info.get('forbidden', False)
            is_project_termbase = match_info.get('is_project_termbase', False)
            translation = match_info.get('target', match_info.get('translation', ''))
            
            # IMPORTANT: Treat ranking #1 as project termbase (even if flag not set)
            is_effective_project = is_project_termbase or (ranking == 1)
            
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
                    
                    # Create format based on style
                    fmt = QTextCharFormat()
                    
                    if highlight_style == 'dotted':
                        # DOTTED UNDERLINE STYLE (IDE/code editor approach)
                        # Simple dotted line like the Gemini example - clean and unobtrusive
                        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.DotLine)
                        if forbidden:
                            fmt.setUnderlineColor(QColor(0, 0, 0))  # Black for forbidden
                        else:
                            # Higher priority = red (more attention), lower = gray (subtle)
                            if ranking == 1:
                                fmt.setUnderlineColor(QColor('#CC0000'))  # Red for priority 1 (project termbase)
                            elif ranking == 2:
                                fmt.setUnderlineColor(QColor('#505050'))  # Dark gray for priority 2
                            elif ranking == 3:
                                fmt.setUnderlineColor(QColor('#707070'))  # Medium gray
                            else:
                                fmt.setUnderlineColor(QColor(dotted_color))  # User-configured color
                        # Add tooltip with translation
                        if translation:
                            fmt.setToolTip(f"Glossary: {translation}")
                    
                    elif highlight_style == 'semibold':
                        # SEMIBOLD TEXT STYLE (typographic approach)
                        fmt.setFontWeight(QFont.Weight.DemiBold)
                        if forbidden:
                            fmt.setForeground(QColor(180, 0, 0))  # Dark red for forbidden
                        else:
                            # Tinted dark color based on ranking
                            if ranking == 1:
                                fmt.setForeground(QColor('#1B5E20'))  # Dark green for priority 1
                            elif ranking == 2:
                                fmt.setForeground(QColor('#2E7D32'))  # Medium dark green
                            elif ranking == 3:
                                fmt.setForeground(QColor('#388E3C'))  # Medium green
                            else:
                                fmt.setForeground(QColor('#43A047'))  # Lighter green
                        # Add tooltip with translation
                        if translation:
                            fmt.setToolTip(f"Glossary: {translation}")
                    
                    else:
                        # BACKGROUND COLOR STYLE (default - current behavior)
                        if forbidden:
                            color = QColor(0, 0, 0)  # Black for forbidden terms
                            fmt.setForeground(QColor("white"))
                        else:
                            # Use ranking to determine soft green shade
                            if ranking is not None:
                                if ranking == 1:
                                    color = QColor(165, 214, 167)  # Soft medium green (Green 200)
                                elif ranking == 2:
                                    color = QColor(200, 230, 201)  # Soft light green (Green 100)
                                elif ranking == 3:
                                    color = QColor(220, 237, 200)  # Very soft light green
                                else:
                                    color = QColor(232, 245, 233)  # Extremely soft pastel green
                            else:
                                color = QColor(200, 230, 201)  # Green 100 (fallback)
                            fmt.setForeground(QColor("black"))
                        fmt.setBackground(color)
                    
                    # Apply format
                    cursor.setCharFormat(fmt)
                    
                    # Track this range as highlighted
                    highlighted_ranges.append((idx, end_idx))
                
                start = end_idx
    
    def highlight_non_translatables(self, nt_matches: list, highlighted_ranges: list = None):
        """
        Highlight non-translatable matches in the text using pastel yellow background.
        
        Args:
            nt_matches: List of dicts with 'text', 'start', 'end' keys from NT manager
            highlighted_ranges: Optional list of already-highlighted ranges to avoid overlap
        """
        from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
        
        if not nt_matches:
            return
        
        doc = self.document()
        
        # Track ranges we've highlighted (to avoid overlap with termbase matches)
        if highlighted_ranges is None:
            highlighted_ranges = []
        
        # Pastel yellow for non-translatables
        nt_color = QColor(255, 253, 208)  # Pastel yellow (#FFFDD0)
        
        for match in nt_matches:
            start_pos = match.get('start', 0)
            end_pos = match.get('end', 0)
            
            if start_pos >= end_pos:
                continue
            
            # Check for overlap with existing highlights
            overlaps = any(
                (start_pos < h_end and end_pos > h_start)
                for h_start, h_end in highlighted_ranges
            )
            
            if overlaps:
                continue
            
            # Create cursor for this position
            cursor = QTextCursor(doc)
            cursor.setPosition(start_pos)
            cursor.setPosition(end_pos, QTextCursor.MoveMode.KeepAnchor)
            
            # Create format with pastel yellow background
            fmt = QTextCharFormat()
            fmt.setBackground(nt_color)
            fmt.setForeground(QColor("#5D4E37"))  # Dark brown text for contrast
            
            cursor.setCharFormat(fmt)
            highlighted_ranges.append((start_pos, end_pos))
    
    def event(self, event):
        """Override event() to catch Tab and Ctrl+T keys before Qt's default handling"""
        # Catch Tab key at event level (before keyPressEvent)
        if event.type() == event.Type.KeyPress:
            key_event = event
            
            # Ctrl+E: Add selected terms to termbase (with dialog)
            if key_event.key() == Qt.Key.Key_E and key_event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self._handle_add_to_termbase()
                return True  # Event handled
            
            # Alt+Left: Quick add selected terms to last-used termbase (no dialog)
            if key_event.key() == Qt.Key.Key_Left and key_event.modifiers() == Qt.KeyboardModifier.AltModifier:
                self._handle_quick_add_to_termbase()
                return True  # Event handled
            
            # Ctrl+Alt+N: Add selected text to non-translatables
            if key_event.key() == Qt.Key.Key_N and key_event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier):
                self._handle_add_to_nt()
                return True  # Event handled
            
            # Ctrl+Home: Navigate to first segment (pass to main window)
            if key_event.key() == Qt.Key.Key_Home and key_event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                main_window = self._get_main_window()
                if main_window and hasattr(main_window, 'go_to_first_segment'):
                    main_window.go_to_first_segment()
                return True  # Event handled
            
            # Ctrl+End: Navigate to last segment (pass to main window)
            if key_event.key() == Qt.Key.Key_End and key_event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                main_window = self._get_main_window()
                if main_window and hasattr(main_window, 'go_to_last_segment'):
                    main_window.go_to_last_segment()
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
                "Please select text in both Source and Target cells before adding to glossary.\\n\\n"
                "Workflow:\\n"
                "1. Select term in source cell\\n"
                "2. Press Tab to cycle to target cell\\n"
                "3. Select corresponding translation\\n"
                "4. Press Ctrl+E (or right-click) to add to glossary"
            )
            return
        
        # Find main window and call add_to_termbase method
        main_window = self.table_ref.parent()
        while main_window and not hasattr(main_window, 'add_term_pair_to_termbase'):
            main_window = main_window.parent()
        
        if main_window and hasattr(main_window, 'add_term_pair_to_termbase'):
            main_window.add_term_pair_to_termbase(source_text, target_text)
    
    def _handle_quick_add_to_termbase(self):
        """Handle Ctrl+R: Quick add selected source and target terms to termbase (no dialog)"""
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
                "Please select text in both Source and Target cells before quick-adding to termbase.\n\n"
                "Tip: Use Ctrl+E to add with a dialog where you can choose termbase and add metadata."
            )
            return
        
        # Find main window and call quick_add_to_termbase method
        main_window = self.table_ref.parent()
        while main_window and not hasattr(main_window, 'quick_add_term_pair_to_termbase'):
            main_window = main_window.parent()
        
        if main_window and hasattr(main_window, 'quick_add_term_pair_to_termbase'):
            main_window.quick_add_term_pair_to_termbase(source_text, target_text)
    
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

    def mouseReleaseEvent(self, event):
        """Smart word selection - expand partial selections to full words"""
        super().mouseReleaseEvent(event)

        # Check if smart selection is enabled
        main_window = self._get_main_window()
        if main_window and hasattr(main_window, 'enable_smart_word_selection'):
            if not main_window.enable_smart_word_selection:
                return  # Feature disabled

        # Get the current cursor
        cursor = self.textCursor()

        # Only expand if there's a selection
        if cursor.hasSelection():
            # Get selection boundaries
            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            # Get the full text
            text = self.toPlainText()

            # Helper function to check if character is part of a word
            # Includes alphanumeric, underscore, hyphen, and apostrophe
            def is_word_char(char):
                return char.isalnum() or char in "_-'"

            # Check if we're at word boundaries
            at_start_boundary = start == 0 or not is_word_char(text[start - 1])
            at_end_boundary = end == len(text) or not is_word_char(text[end])

            # If selection is partial (not at both boundaries) and reasonably small
            # (to avoid interfering with intentional multi-word selections)
            selection_length = end - start
            if (not at_start_boundary or not at_end_boundary) and selection_length < 50:
                # Expand to word boundaries
                # Move start backward to word boundary
                while start > 0 and is_word_char(text[start - 1]):
                    start -= 1

                # Move end forward to word boundary
                while end < len(text) and is_word_char(text[end]):
                    end += 1

                # Set the new selection
                cursor.setPosition(start)
                cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
                self.setTextCursor(cursor)

    def _get_main_window(self):
        """Get the main application window by traversing the parent hierarchy"""
        if not self.parent():
            return None
        main_window = self.parent()
        while main_window and not hasattr(main_window, 'go_to_first_segment'):
            main_window = main_window.parent()
        return main_window
    
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

    def contextMenuEvent(self, event):
        """Show context menu with Add to Glossary and Add to Non-Translatables options"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction
        
        menu = QMenu(self)
        
        # Add standard actions
        if self.textCursor().hasSelection():
            copy_action = QAction("Copy", self)
            copy_action.triggered.connect(self.copy)
            menu.addAction(copy_action)
            menu.addSeparator()
        
        # Add to glossary action (with dialog)
        add_to_tb_action = QAction("📖 Add to Glossary (Ctrl+E)", self)
        add_to_tb_action.triggered.connect(self._handle_add_to_termbase)
        menu.addAction(add_to_tb_action)
        
        # Quick add to glossary action (no dialog) - uses last-selected glossary from Ctrl+E
        quick_add_action = QAction("⚡ Quick Add to Glossary (Alt+Left)", self)
        quick_add_action.triggered.connect(self._handle_quick_add_to_termbase)
        menu.addAction(quick_add_action)
        
        # Add to non-translatables action
        add_to_nt_action = QAction("🚫 Add to Non-Translatables (Ctrl+Alt+N)", self)
        add_to_nt_action.triggered.connect(self._handle_add_to_nt)
        menu.addAction(add_to_nt_action)
        
        menu.exec(event.globalPos())
    
    def _handle_add_to_nt(self):
        """Handle Ctrl+Alt+N: Add selected text to active non-translatable list(s)"""
        # Get selected text
        selected_text = self.textCursor().selectedText().strip()
        
        if not selected_text:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select text in the Source cell before adding to non-translatables."
            )
            return
        
        # Find main window and call add_to_nt method
        table = self.table_ref if hasattr(self, 'table_ref') else self.parent()
        if table:
            main_window = table.parent()
            while main_window and not hasattr(main_window, 'add_text_to_non_translatables'):
                main_window = main_window.parent()
            
            if main_window and hasattr(main_window, 'add_text_to_non_translatables'):
                main_window.add_text_to_non_translatables(selected_text)
            else:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "Feature Not Available",
                    "Non-translatables functionality not available."
                )

    def set_background_color(self, color: str):
        """Set the background color for this text editor (for alternating row colors)"""
        self.setStyleSheet(f"""
            QTextEdit {{
                border: none;
                background-color: {color};
                padding: 0px;
            }}
            QTextEdit:focus {{
                border: 1px solid #2196F3;
            }}
            QTextEdit::selection {{
                background-color: #D0E7FF;
                color: black;
            }}
        """)


class TagHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for HTML/XML tags, CAT tool tags, CafeTran pipe symbols, and spell checking in text editors"""

    # Class-level reference to spellcheck manager (shared across all instances)
    _spellcheck_manager = None
    _spellcheck_enabled = False
    _is_cafetran_project = False  # Only highlight pipe symbols for CafeTran projects

    def __init__(self, document, tag_color='#7f0001', invisible_char_color='#999999', enable_spellcheck=False):
        super().__init__(document)
        self.tag_color = tag_color
        self.invisible_char_color = invisible_char_color
        self._local_spellcheck_enabled = enable_spellcheck
        self.update_tag_format()

    @classmethod
    def set_spellcheck_manager(cls, manager):
        """Set the shared spellcheck manager instance"""
        cls._spellcheck_manager = manager

    @classmethod
    def set_spellcheck_enabled(cls, enabled: bool):
        """Enable or disable spellchecking globally"""
        cls._spellcheck_enabled = enabled

    def update_tag_format(self):
        """Update the tag format with current color"""
        from PyQt6.QtGui import QTextCharFormat, QColor
        self.tag_format = QTextCharFormat()
        self.tag_format.setForeground(QColor(self.tag_color))

        # CafeTran pipe symbols - red and bold like in CafeTran
        self.pipe_format = QTextCharFormat()
        self.pipe_format.setForeground(QColor('#FF0000'))  # Red
        self.pipe_format.setFontWeight(700)  # Bold

        # Invisible character symbols - use configured color
        self.invisible_format = QTextCharFormat()
        self.invisible_format.setForeground(QColor(self.invisible_char_color))

        # Spellcheck format - red wavy underline
        self.spellcheck_format = QTextCharFormat()
        self.spellcheck_format.setUnderlineColor(QColor('#FF0000'))
        self.spellcheck_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)

    def set_tag_color(self, color: str):
        """Update tag highlight color"""
        self.tag_color = color
        self.update_tag_format()
        self.rehighlight()

    def set_invisible_char_color(self, color: str):
        """Update invisible character color"""
        self.invisible_char_color = color
        self.update_tag_format()
        self.rehighlight()

    def set_local_spellcheck(self, enabled: bool):
        """Enable or disable spellcheck for this specific highlighter"""
        self._local_spellcheck_enabled = enabled
        self.rehighlight()
    
    def highlightBlock(self, text):
        """Highlight all tags, pipe symbols, invisible chars, and misspelled words in the text block"""
        import re
        # Combined pattern for ALL CAT tool tag types:
        # 1. HTML/XML: <tag>, </tag>, <tag/>, <tag attr="val">
        # 2. Trados numeric: <1>, </1>
        # 3. memoQ numeric bracket tags:
        #    - Opening: [1}, [2} etc.
        #    - Closing: {1], {2] etc.
        #    - Standalone: [1], [2] etc.
        # 4. memoQ content tags with text/attributes (from bilingual DOCX):
        #    - [uicontrol id="GUID-..."], [image cid="..." href="..."], etc.
        #    - {uicontrol}, {image}, etc. (closing tags)
        #    NOTE: Opening [tag] MUST have attributes (space+content) to avoid matching
        #          placeholders like [Company] or [Bedrijf]. Closing {tag} doesn't need attrs.
        tag_patterns = [
            r'</?[a-zA-Z][a-zA-Z0-9-]*/?(?:\s[^>]*)?>',  # HTML/XML tags
            r'</?\d+>',                                   # Trados numeric: <1>, </1>
            r'\[\d+[}\]]',                                # memoQ numeric: [1}, [1]
            r'\{\d+[}\]]',                                # memoQ numeric: {1}, {1]
            r'\[[^}\]]+\}',                               # memoQ mixed: [anything} (exclude } and ])
            r'\{[^\[\]]+\]',                              # memoQ mixed: {anything] (exclude [ and ])
            r'\[[a-zA-Z][^}\]]*\s[^}\]]*\]',              # memoQ content: [tag attr...] (exclude } and ])
            r'\{[a-zA-Z][a-zA-Z0-9_-]*\}',                # memoQ closing: {uicontrol}, {MQ}
        ]
        combined_pattern = re.compile('|'.join(tag_patterns))

        matches_found = list(combined_pattern.finditer(text))

        for match in matches_found:
            start = match.start()
            length = match.end() - start
            self.setFormat(start, length, self.tag_format)

        # Match invisible character symbols (light blue)
        for i, char in enumerate(text):
            if char in '·→°¶':  # Invisible character replacement symbols
                self.setFormat(i, 1, self.invisible_format)
        
        # CafeTran pipe symbols (red and bold) - ONLY for CafeTran projects
        if TagHighlighter._is_cafetran_project:
            for i, char in enumerate(text):
                if char == '|':
                    self.setFormat(i, 1, self.pipe_format)

        # Spell checking - only for target editors when enabled
        if self._local_spellcheck_enabled and TagHighlighter._spellcheck_enabled and TagHighlighter._spellcheck_manager:
            self._highlight_misspelled_words(text)

    def _highlight_misspelled_words(self, text):
        """Highlight misspelled words with red wavy underline"""
        # Safety check - if spellcheck manager is not available or disabled, skip
        if not TagHighlighter._spellcheck_manager:
            return
        
        # Check if spellcheck manager detected a crash - if so, skip entirely
        if hasattr(TagHighlighter._spellcheck_manager, '_crash_detected') and TagHighlighter._spellcheck_manager._crash_detected:
            return
        
        import re
        # Find all words (letters only, including accented characters)
        # Skip words inside tags or that look like technical content
        word_pattern = re.compile(r'\b([a-zA-ZÀ-ÿ\']+)\b', re.UNICODE)
        
        try:
            for match in word_pattern.finditer(text):
                word = match.group(1)
                start = match.start(1)
                length = len(word)
                
                # Skip very short words and words with apostrophes at start/end
                if len(word) < 2:
                    continue
                
                # Check if this word is inside ANY type of tag:
                # - HTML/XML: < ... >
                # - memoQ/DITA: [ ... } or [ ... ] or { ... ]
                before_text = text[:start]
                
                # Check for HTML tags
                last_html_open = before_text.rfind('<')
                last_html_close = before_text.rfind('>')
                if last_html_open > last_html_close:
                    continue  # Inside HTML tag
                
                # Check for bracket tags: [ ... } or [ ... ]
                last_square_open = before_text.rfind('[')
                last_square_close = max(before_text.rfind('}'), before_text.rfind(']'))
                if last_square_open > last_square_close:
                    continue  # Inside [tag...} or [tag...]
                
                # Check for curly tags: { ... ] or { ... }
                last_curly_open = before_text.rfind('{')
                last_curly_close = max(before_text.rfind(']'), before_text.rfind('}'))
                if last_curly_open > last_curly_close:
                    continue  # Inside {tag...] or {tag...}
                
                # Check spelling
                if not TagHighlighter._spellcheck_manager.check_word(word):
                    self.setFormat(start, length, self.spellcheck_format)
        except Exception as e:
            # If anything goes wrong during spellcheck highlighting, disable it
            print(f"Spellcheck highlighting error: {e}")
            if TagHighlighter._spellcheck_manager:
                TagHighlighter._spellcheck_manager._crash_detected = True
                TagHighlighter._spellcheck_manager.enabled = False


class EditableGridTextEditor(QTextEdit):
    """Editable QTextEdit for target cells - allows text selection and editing"""
    
    # Class variable for tag highlight color (shared across all instances)
    tag_highlight_color = '#7f0001'  # Default memoQ dark red
    
    # Class variables for focus border customization
    focus_border_color = '#2196F3'  # Default blue
    focus_border_thickness = 2  # Default 2px (slightly thicker than before)
    
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

        # Add syntax highlighter for tags (with spellcheck enabled for target cells)
        # Get invisible char color from main window if available
        main_window = self._get_main_window()
        invisible_char_color = main_window.invisible_char_color if main_window and hasattr(main_window, 'invisible_char_color') else '#999999'
        self.highlighter = TagHighlighter(self.document(), self.tag_highlight_color, invisible_char_color, enable_spellcheck=True)

        # Style to look like a normal cell with subtle selection
        # Background and text colors now managed by theme system
        self.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 0px 4px 0px 0px;
            }
            QTextEdit:focus {
                border: 1px solid #2196F3;
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
        # With zero-width spaces inserted after invisible character markers,
        # normal WordWrap will work correctly
        wrap_mode = QTextOption.WrapMode.WordWrap

        self.setWordWrapMode(wrap_mode)
        self.setAcceptRichText(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        text_option = QTextOption()
        text_option.setWrapMode(wrap_mode)
        doc.setDefaultTextOption(text_option)
        
        # Set minimum height to 0 - let content determine size
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)  # Qt's max int
    
    def mouseDoubleClickEvent(self, event):
        """Handle double-click to select words properly when invisibles are shown"""
        from PyQt6.QtGui import QTextCursor
        
        main_window = self._get_main_window()
        # Check if invisible spaces are being shown
        if main_window and hasattr(main_window, 'invisible_display_settings'):
            if main_window.invisible_display_settings.get('spaces', False):
                # Get cursor position at click
                cursor = self.cursorForPosition(event.pos())
                pos = cursor.position()
                text = self.toPlainText()
                
                # Find word boundaries using middle dot (·) or zero-width space as delimiters
                # Find start of word (search backwards for · or start of text)
                start = pos
                while start > 0 and text[start - 1] not in ('·', '\u200B', '\n', '\t', '→', '°', '¶'):
                    start -= 1
                
                # Find end of word (search forwards for · or end of text)
                end = pos
                while end < len(text) and text[end] not in ('·', '\u200B', '\n', '\t', '→', '°', '¶'):
                    end += 1
                
                # Select the word
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
                self.setTextCursor(cursor)
                return
        
        # Default behavior
        super().mouseDoubleClickEvent(event)
    
    def _get_main_window(self):
        """Get the main application window by traversing the parent hierarchy"""
        if not self.table:
            return None
        main_window = self.table.parent()
        while main_window and not hasattr(main_window, 'go_to_first_segment'):
            main_window = main_window.parent()
        return main_window
    
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
                "Please select text in both Source and Target cells before adding to glossary.\\n\\n"
                "Workflow:\\n"
                "1. Select term in source/target cell\\n"
                "2. Press Tab to cycle to other cell\\n"
                "3. Select corresponding term\\n"
                "4. Press Ctrl+E (or right-click) to add to glossary"
            )
            return
        
        # Find main window and call add_to_termbase method
        main_window = self.table.parent()
        while main_window and not hasattr(main_window, 'add_term_pair_to_termbase'):
            main_window = main_window.parent()
        
        if main_window and hasattr(main_window, 'add_term_pair_to_termbase'):
            main_window.add_term_pair_to_termbase(source_text, target_text)
    
    def _handle_quick_add_to_termbase(self):
        """Handle Ctrl+R: Quick add selected source and target terms to glossary (no dialog)"""
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
                "Please select text in both Source and Target cells before quick-adding to glossary.\n\n"
                "Tip: Use Ctrl+E to add with a dialog where you can choose glossary and add metadata."
            )
            return
        
        # Find main window and call quick_add_to_termbase method
        main_window = self.table.parent()
        while main_window and not hasattr(main_window, 'quick_add_term_pair_to_termbase'):
            main_window = main_window.parent()
        
        if main_window and hasattr(main_window, 'quick_add_term_pair_to_termbase'):
            main_window.quick_add_term_pair_to_termbase(source_text, target_text)
    
    def contextMenuEvent(self, event):
        """Show context menu with Add to Glossary, Non-Translatables, and Spellcheck options"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction
        
        menu = QMenu(self)
        
        # Check if cursor is on a misspelled word for spellcheck suggestions
        cursor_pos = self.cursorForPosition(event.pos())
        misspelled_word, word_start, word_end = self._get_misspelled_word_at_cursor(cursor_pos)
        
        if misspelled_word:
            # Get spellcheck suggestions
            if TagHighlighter._spellcheck_manager:
                suggestions = TagHighlighter._spellcheck_manager.get_suggestions(misspelled_word)
                
                if suggestions:
                    # Add suggestions at the top
                    for suggestion in suggestions[:5]:  # Limit to 5 suggestions
                        suggestion_action = QAction(f"✓ {suggestion}", self)
                        # Use default argument to capture current value
                        suggestion_action.triggered.connect(
                            lambda checked, s=suggestion, start=word_start, end=word_end: 
                            self._replace_word(start, end, s)
                        )
                        suggestion_action.setFont(menu.font())
                        menu.addAction(suggestion_action)
                    menu.addSeparator()
                
                # Add to dictionary action
                add_to_dict_action = QAction(f"📖 Add '{misspelled_word}' to Dictionary", self)
                add_to_dict_action.triggered.connect(
                    lambda checked, w=misspelled_word: self._add_to_dictionary(w)
                )
                menu.addAction(add_to_dict_action)
                
                # Ignore this session action
                ignore_action = QAction(f"🔇 Ignore '{misspelled_word}' (this session)", self)
                ignore_action.triggered.connect(
                    lambda checked, w=misspelled_word: self._ignore_word(w)
                )
                menu.addAction(ignore_action)
                menu.addSeparator()
        
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
        
        # Add to termbase action (with dialog)
        add_to_tb_action = QAction("📖 Add to Glossary (Ctrl+E)", self)
        add_to_tb_action.triggered.connect(self._handle_add_to_termbase)
        menu.addAction(add_to_tb_action)
        
        # Quick add to termbase action (no dialog) - uses last-selected termbase from Ctrl+E
        quick_add_action = QAction("⚡ Quick Add to Glossary (Alt+Left)", self)
        quick_add_action.triggered.connect(self._handle_quick_add_to_termbase)
        menu.addAction(quick_add_action)
        
        # Add to non-translatables action
        add_to_nt_action = QAction("🚫 Add to Non-Translatables (Ctrl+Alt+N)", self)
        add_to_nt_action.triggered.connect(self._handle_add_to_nt)
        menu.addAction(add_to_nt_action)
        
        menu.exec(event.globalPos())

    def _get_misspelled_word_at_cursor(self, cursor):
        """Get the misspelled word at the cursor position, if any"""
        import re
        
        if not TagHighlighter._spellcheck_enabled or not TagHighlighter._spellcheck_manager:
            return None, 0, 0
        
        text = self.toPlainText()
        pos = cursor.position()
        
        # Find word boundaries around cursor position
        word_pattern = re.compile(r'\b([a-zA-ZÀ-ÿ\']+)\b', re.UNICODE)
        
        for match in word_pattern.finditer(text):
            start = match.start(1)
            end = match.end(1)
            
            if start <= pos <= end:
                word = match.group(1)
                # Check if this word is misspelled
                if not TagHighlighter._spellcheck_manager.check_word(word):
                    return word, start, end
                break
        
        return None, 0, 0

    def _replace_word(self, start: int, end: int, replacement: str):
        """Replace a word at the given position with the replacement"""
        cursor = self.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
        cursor.insertText(replacement)

    def _add_to_dictionary(self, word: str):
        """Add word to the custom dictionary"""
        if TagHighlighter._spellcheck_manager:
            TagHighlighter._spellcheck_manager.add_to_dictionary(word)
            
            # Show confirmation in main window log
            main_window = self._get_main_window()
            if main_window and hasattr(main_window, 'log'):
                main_window.log(f"✓ Added '{word}' to custom dictionary")

            # Refresh all highlighters to update other occurrences
            if main_window and hasattr(main_window, '_refresh_all_highlighters'):
                main_window._refresh_all_highlighters()
            else:
                # Fallback to local rehighlight
                self.highlighter.rehighlight()

    def _ignore_word(self, word: str):
        """Ignore word for this session"""
        if TagHighlighter._spellcheck_manager:
            TagHighlighter._spellcheck_manager.ignore_word(word)
            
            # Show confirmation in main window log
            main_window = self._get_main_window()
            if main_window and hasattr(main_window, 'log'):
                main_window.log(f"🔇 Ignoring '{word}' for this session")

            # Refresh all highlighters to update other occurrences
            if main_window and hasattr(main_window, '_refresh_all_highlighters'):
                main_window._refresh_all_highlighters()
            else:
                # Fallback to local rehighlight
                self.highlighter.rehighlight()
    
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

    def mouseReleaseEvent(self, event):
        """Smart word selection - expand partial selections to full words"""
        super().mouseReleaseEvent(event)

        # Check if smart selection is enabled
        main_window = self._get_main_window()
        if main_window and hasattr(main_window, 'enable_smart_word_selection'):
            if not main_window.enable_smart_word_selection:
                return  # Feature disabled

        # Get the current cursor
        cursor = self.textCursor()

        # Only expand if there's a selection
        if cursor.hasSelection():
            # Get selection boundaries
            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            # Get the full text
            text = self.toPlainText()

            # Helper function to check if character is part of a word
            # Includes alphanumeric, underscore, hyphen, and apostrophe
            def is_word_char(char):
                return char.isalnum() or char in "_-'"

            # Check if we're at word boundaries
            at_start_boundary = start == 0 or not is_word_char(text[start - 1])
            at_end_boundary = end == len(text) or not is_word_char(text[end])

            # If selection is partial (not at both boundaries) and reasonably small
            # (to avoid interfering with intentional multi-word selections)
            selection_length = end - start
            if (not at_start_boundary or not at_end_boundary) and selection_length < 50:
                # Expand to word boundaries
                # Move start backward to word boundary
                while start > 0 and is_word_char(text[start - 1]):
                    start -= 1

                # Move end forward to word boundary
                while end < len(text) and is_word_char(text[end]):
                    end += 1

                # Set the new selection
                cursor.setPosition(start)
                cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
                self.setTextCursor(cursor)

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
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QTextCursor
        
        # Ctrl+C: Fix clipboard when copying with invisible characters shown
        if event.key() == Qt.Key.Key_C and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            cursor = self.textCursor()
            if cursor.hasSelection():
                selected_text = cursor.selectedText()
                # Reverse invisible character replacements before copying
                main_window = self._get_main_window()
                if main_window and hasattr(main_window, 'reverse_invisible_replacements'):
                    clean_text = main_window.reverse_invisible_replacements(selected_text)
                    # Also replace paragraph separator with newline (Qt uses U+2029)
                    clean_text = clean_text.replace('\u2029', '\n')
                    # Set clipboard with clean text
                    clipboard = QApplication.clipboard()
                    clipboard.setText(clean_text)
                    event.accept()
                    return
        
        # Handle Ctrl+Arrow word navigation when invisibles are shown
        main_window = self._get_main_window()
        if main_window and hasattr(main_window, 'invisible_display_settings'):
            if main_window.invisible_display_settings.get('spaces', False):
                ctrl_only = event.modifiers() == Qt.KeyboardModifier.ControlModifier
                ctrl_shift = event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier)
                
                if (ctrl_only or ctrl_shift) and event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right):
                    cursor = self.textCursor()
                    text = self.toPlainText()
                    pos = cursor.position()
                    word_chars = ('·', '\u200B', '\n', '\t', '→', '°', '¶', ' ')
                    
                    if event.key() == Qt.Key.Key_Right:
                        # Move to end of current word, then skip delimiters to start of next word
                        # First skip any delimiters we're on
                        while pos < len(text) and text[pos] in word_chars:
                            pos += 1
                        # Then skip to end of word (next delimiter)
                        while pos < len(text) and text[pos] not in word_chars:
                            pos += 1
                    else:  # Key_Left
                        # Move backwards: skip delimiters, then find start of word
                        if pos > 0:
                            pos -= 1
                        # Skip any delimiters
                        while pos > 0 and text[pos] in word_chars:
                            pos -= 1
                        # Find start of word
                        while pos > 0 and text[pos - 1] not in word_chars:
                            pos -= 1
                    
                    # Apply cursor movement
                    if ctrl_shift:
                        cursor.setPosition(pos, QTextCursor.MoveMode.KeepAnchor)
                    else:
                        cursor.setPosition(pos)
                    self.setTextCursor(cursor)
                    event.accept()
                    return
        
        # Ctrl+E: Add selected terms to termbase (with dialog)
        if event.key() == Qt.Key.Key_E and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._handle_add_to_termbase()
            event.accept()
            return
        
        # Alt+Left: Quick add selected terms to last-used termbase (no dialog)
        if event.key() == Qt.Key.Key_Left and event.modifiers() == Qt.KeyboardModifier.AltModifier:
            self._handle_quick_add_to_termbase()
            event.accept()
            return
        
        # Ctrl+Alt+N: Add selected text to non-translatables
        if event.key() == Qt.Key.Key_N and event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier):
            self._handle_add_to_nt()
            event.accept()
            return
        
        # Ctrl+Home: Navigate to first segment (pass to main window)
        if event.key() == Qt.Key.Key_Home and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            main_window = self._get_main_window()
            if main_window and hasattr(main_window, 'go_to_first_segment'):
                main_window.go_to_first_segment()
            event.accept()
            return
        
        # Ctrl+End: Navigate to last segment (pass to main window)
        if event.key() == Qt.Key.Key_End and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            main_window = self._get_main_window()
            if main_window and hasattr(main_window, 'go_to_last_segment'):
                main_window.go_to_last_segment()
            event.accept()
            return
        
        # Ctrl+, (comma): Insert next memoQ tag or wrap selection with tag pair
        if event.key() == Qt.Key.Key_Comma and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._insert_next_tag_or_wrap_selection()
            event.accept()
            return
        
        # Ctrl+Shift+S: Copy source text to target
        if event.key() == Qt.Key.Key_S and event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier):
            self._copy_source_to_target()
            event.accept()
            return
        
        # Ctrl+B: Apply bold formatting to selection
        if event.key() == Qt.Key.Key_B and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._apply_formatting_tag('b')
            event.accept()
            return
        
        # Ctrl+I: Apply italic formatting to selection
        if event.key() == Qt.Key.Key_I and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._apply_formatting_tag('i')
            event.accept()
            return
        
        # Ctrl+U: Apply underline formatting to selection
        if event.key() == Qt.Key.Key_U and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._apply_formatting_tag('u')
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
        
        # Arrow Up/Down: memoQ-style segment navigation at cell boundaries
        # When cursor is at top VISUAL line and Up is pressed, go to previous segment
        # When cursor is at bottom VISUAL line and Down is pressed, go to next segment
        if event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down) and event.modifiers() == Qt.KeyboardModifier.NoModifier:
            cursor = self.textCursor()
            current_block = cursor.block()
            doc = self.document()
            first_block = doc.firstBlock()
            last_block = doc.lastBlock()
            
            # Get the visual line number within the current block
            layout = current_block.layout()
            if layout:
                pos_in_block = cursor.positionInBlock()
                current_visual_line = layout.lineForTextPosition(pos_in_block)
                current_line_num = current_visual_line.lineNumber() if current_visual_line.isValid() else 0
                total_lines_in_block = layout.lineCount()
            else:
                current_line_num = 0
                total_lines_in_block = 1
            
            if event.key() == Qt.Key.Key_Up:
                # Only navigate to previous segment if we're on the FIRST visual line of the FIRST block
                is_first_visual_line = (current_block == first_block and current_line_num == 0)
                if is_first_visual_line:
                    main_window = self._get_main_window()
                    if main_window and hasattr(main_window, 'go_to_previous_segment'):
                        # Get cursor column within current visual line
                        if layout and current_visual_line.isValid():
                            col_in_line = pos_in_block - int(current_visual_line.textStart())
                        else:
                            col_in_line = cursor.positionInBlock()
                        # Signal rapid navigation for performance optimization
                        main_window._arrow_key_navigation = True
                        main_window.go_to_previous_segment(target_column=col_in_line, to_last_line=True)
                        event.accept()
                        return
            
            elif event.key() == Qt.Key.Key_Down:
                # Only navigate to next segment if we're on the LAST visual line of the LAST block
                is_last_visual_line = (current_block == last_block and current_line_num >= total_lines_in_block - 1)
                if is_last_visual_line:
                    main_window = self._get_main_window()
                    if main_window and hasattr(main_window, 'go_to_next_segment'):
                        # Get cursor column within current visual line
                        if layout and current_visual_line.isValid():
                            col_in_line = pos_in_block - int(current_visual_line.textStart())
                        else:
                            col_in_line = cursor.positionInBlock()
                        # Signal rapid navigation for performance optimization
                        main_window._arrow_key_navigation = True
                        main_window.go_to_next_segment(target_column=col_in_line, to_first_line=True)
                        event.accept()
                        return
        
        # All other keys: Handle normally
        super().keyPressEvent(event)
    
    def _handle_add_to_nt(self):
        """Handle Ctrl+Alt+N: Add selected text to active non-translatable list(s)"""
        # Get selected text from source cell (for NT, we typically add from source)
        # But if this is target and source is available, use source
        selected_text = self.textCursor().selectedText().strip()
        
        # If no selection in target, try getting from source
        if not selected_text and self.table and self.row >= 0:
            source_widget = self.table.cellWidget(self.row, 2)
            if source_widget and hasattr(source_widget, 'textCursor'):
                selected_text = source_widget.textCursor().selectedText().strip()
        
        if not selected_text:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select text before adding to non-translatables."
            )
            return
        
        # Find main window and call add_to_nt method
        if self.table:
            main_window = self.table.parent()
            while main_window and not hasattr(main_window, 'add_text_to_non_translatables'):
                main_window = main_window.parent()
            
            if main_window and hasattr(main_window, 'add_text_to_non_translatables'):
                main_window.add_text_to_non_translatables(selected_text)
            else:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "Feature Not Available",
                    "Non-translatables functionality not available."
                )

    def _insert_next_tag_or_wrap_selection(self):
        """
        Insert the next memoQ tag, HTML tag, or CafeTran pipe symbol from source, or wrap selection.
        
        Behavior:
        - If text is selected: Wrap it with the next available tag pair [N}selection{N] or |selection|
        - If no selection: Insert the next unused tag/pipe from source at cursor position
        
        Supports:
        - memoQ tags: [1}, {1], [2}, {2], etc.
        - HTML/XML tags: <li>, </li>, <b>, </b>, <i>, </i>, etc.
        - CafeTran pipe symbols: |
        
        Shortcut: Ctrl+, (comma)
        """
        if not self.table or self.row < 0:
            return
        
        # Navigate up to find main window
        main_window = self.table.parent()
        while main_window and not hasattr(main_window, 'current_project'):
            main_window = main_window.parent()
        
        if not main_window or not hasattr(main_window, 'current_project'):
            return
        
        if not main_window.current_project or self.row >= len(main_window.current_project.segments):
            return
        
        segment = main_window.current_project.segments[self.row]
        source_text = segment.source
        current_target = self.toPlainText()
        
        # Check what type of tags are in the source
        has_memoq_tags = bool(extract_memoq_tags(source_text))
        has_html_tags = bool(extract_html_tags(source_text))
        has_any_tags = has_memoq_tags or has_html_tags
        has_pipe_symbols = '|' in source_text
        
        # Check if there's a selection
        cursor = self.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            
            # Try memoQ tag pair first
            if has_memoq_tags:
                opening_tag, closing_tag = get_wrapping_tag_pair(source_text, current_target)
                if opening_tag and closing_tag:
                    wrapped_text = f"{opening_tag}{selected_text}{closing_tag}"
                    cursor.insertText(wrapped_text)
                    if hasattr(main_window, 'log'):
                        main_window.log(f"🏷️ Wrapped selection with {opening_tag}...{closing_tag}")
                    return
            
            # Try CafeTran pipe symbols
            if has_pipe_symbols:
                pipes_needed = get_next_pipe_count_needed(source_text, current_target)
                if pipes_needed >= 2:
                    # Wrap with pipes
                    wrapped_text = f"|{selected_text}|"
                    cursor.insertText(wrapped_text)
                    if hasattr(main_window, 'log'):
                        main_window.log(f"🏷️ Wrapped selection with |...|")
                    return
            
            if hasattr(main_window, 'log'):
                main_window.log("⚠️ No tag pairs available from source")
        else:
            # No selection - insert next unused tag or pipe at cursor
            
            # Try memoQ tags and HTML tags (find_next_unused_tag handles both)
            if has_any_tags:
                next_tag = find_next_unused_tag(source_text, current_target)
                if next_tag:
                    cursor.insertText(next_tag)
                    if hasattr(main_window, 'log'):
                        main_window.log(f"🏷️ Inserted tag: {next_tag}")
                    return
            
            # Try CafeTran pipe symbols
            if has_pipe_symbols:
                pipes_needed = get_next_pipe_count_needed(source_text, current_target)
                if pipes_needed > 0:
                    cursor.insertText('|')
                    if hasattr(main_window, 'log'):
                        main_window.log(f"🏷️ Inserted pipe symbol (|)")
                    return
            
            if hasattr(main_window, 'log'):
                main_window.log("✓ All tags from source already in target")
    
    def _copy_source_to_target(self):
        """
        Copy source text to target cell.
        
        Shortcut: Ctrl+Shift+S
        """
        if not self.table or self.row < 0:
            return
        
        # Navigate up to find main window
        main_window = self.table.parent()
        while main_window and not hasattr(main_window, 'current_project'):
            main_window = main_window.parent()
        
        if not main_window or not hasattr(main_window, 'current_project'):
            return
        
        if not main_window.current_project or self.row >= len(main_window.current_project.segments):
            return
        
        segment = main_window.current_project.segments[self.row]
        source_text = segment.source
        
        # Set the target text
        self.setPlainText(source_text)
        
        if hasattr(main_window, 'log'):
            main_window.log(f"📋 Copied source to target (segment {self.row + 1})")

    def _apply_formatting_tag(self, tag: str):
        """
        Apply or toggle a formatting tag on the selected text.
        
        Args:
            tag: The tag to apply ('b', 'i', or 'u')
        """
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return
        
        selected_text = cursor.selectedText()
        
        # Check if the text is already wrapped with this tag
        open_tag = f"<{tag}>"
        close_tag = f"</{tag}>"
        
        # Get the full text and selection position
        full_text = self.toPlainText()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        
        # Check for existing tags just before/after selection
        prefix_has_tag = start >= len(open_tag) and full_text[start - len(open_tag):start] == open_tag
        suffix_has_tag = end + len(close_tag) <= len(full_text) and full_text[end:end + len(close_tag)] == close_tag
        
        if prefix_has_tag and suffix_has_tag:
            # Remove the tags (toggle off)
            new_text = full_text[:start - len(open_tag)] + selected_text + full_text[end + len(close_tag):]
            cursor.setPosition(start - len(open_tag))
            cursor.setPosition(end + len(close_tag), cursor.MoveMode.KeepAnchor)
            cursor.insertText(selected_text)
        else:
            # Add the tags (toggle on)
            wrapped_text = f"{open_tag}{selected_text}{close_tag}"
            cursor.insertText(wrapped_text)
            
            # Re-select the wrapped text (including tags)
            cursor.setPosition(start)
            cursor.setPosition(start + len(wrapped_text), cursor.MoveMode.KeepAnchor)
            self.setTextCursor(cursor)

    def update_display_mode(self, text: str, show_tags: bool):
        """
        Update the display based on tag view mode.
        
        Args:
            text: The raw text (with HTML tags like <b>bold</b>)
            show_tags: If True, show raw tags. If False, show formatted WYSIWYG.
        """
        # Store raw text as property for later retrieval
        self._raw_text = text
        
        self.blockSignals(True)
        if show_tags:
            # Tag view: Show plain text with visible tags
            # The TagHighlighter will colorize the tags
            self.setPlainText(text)
        else:
            # WYSIWYG view: Apply formatting
            if has_formatting_tags(text):
                html = get_formatted_html_display(text)
                self.setHtml(html)
            else:
                # No tags, just plain text
                self.setPlainText(text)
        self.blockSignals(False)
    
    def get_raw_text(self) -> str:
        """Get the raw text with tags, regardless of display mode."""
        return getattr(self, '_raw_text', self.toPlainText())

    def set_background_color(self, color: str):
        """Set the background color for this text editor (for alternating row colors)"""
        self.setStyleSheet(f"""
            QTextEdit {{
                border: none;
                background-color: {color};
                padding: 0px;
            }}
            QTextEdit:focus {{
                border: 1px solid #2196F3;
            }}
            QTextEdit::selection {{
                background-color: #D0E7FF;
                color: black;
            }}
        """)


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

            # Call the main app's refresh method to update all UI elements
            if hasattr(self.parent(), 'refresh_theme_colors'):
                self.parent().refresh_theme_colors()

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
    
    def __init__(self, source_term: str, target_term: str, active_termbases: list, parent=None, user_data_path=None):
        super().__init__(parent)
        self.source_term = source_term
        self.target_term = target_term
        self.active_termbases = active_termbases
        self.termbase_checkboxes = {}  # Store checkbox references
        self.user_data_path = user_data_path
        self.saved_selections = self._load_termbase_selections()
        self.setup_ui()
    
    def _load_termbase_selections(self):
        """Load saved termbase selections from preferences"""
        if not self.user_data_path:
            return None
        
        prefs_file = self.user_data_path / "ui_preferences.json"
        if not prefs_file.exists():
            return None
        
        try:
            with open(prefs_file, 'r') as f:
                prefs = json.load(f)
                return prefs.get('add_term_termbase_selections', None)
        except:
            return None
    
    def _save_termbase_selections(self):
        """Save current termbase selections to preferences"""
        if not self.user_data_path:
            return
        
        prefs_file = self.user_data_path / "ui_preferences.json"
        
        # Load existing preferences
        prefs = {}
        if prefs_file.exists():
            try:
                with open(prefs_file, 'r') as f:
                    prefs = json.load(f)
            except:
                pass
        
        # Save the selected termbase IDs
        selected_ids = [tb_id for tb_id, cb in self.termbase_checkboxes.items() if cb.isChecked()]
        prefs['add_term_termbase_selections'] = selected_ids
        
        try:
            with open(prefs_file, 'w') as f:
                json.dump(prefs, f, indent=2)
        except:
            pass
        
    def setup_ui(self):
        self.setWindowTitle("Add Term to Glossary")
        self.setMinimumWidth(550)

        # Auto-resize to fit screen (max 85% of screen height)
        screen = QApplication.primaryScreen().availableGeometry()
        max_height = int(screen.height() * 0.85)
        self.setMaximumHeight(max_height)

        # Start with very compact size for laptops
        self.resize(600, min(550, max_height))

        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create scroll area for all content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(4)
        layout.setContentsMargins(6, 6, 6, 6)
        
        # Header
        header = QLabel("Add term pair to glossary")
        header.setStyleSheet("font-size: 12px; font-weight: bold; margin-bottom: 5px; padding: 4px;")
        layout.addWidget(header)
        
        # Term pair display (read-only)
        term_group = QGroupBox("Term Pair")
        term_layout = QFormLayout()
        
        source_label = QLabel(self.source_term)
        source_label.setStyleSheet("padding: 5px; border-radius: 3px;")
        source_label.setWordWrap(True)
        term_layout.addRow("Source:", source_label)
        
        target_label = QLabel(self.target_term)
        target_label.setStyleSheet("padding: 5px; border-radius: 3px;")
        target_label.setWordWrap(True)
        term_layout.addRow("Target:", target_label)
        
        term_group.setLayout(term_layout)
        layout.addWidget(term_group)
        
        # Termbase selection
        tb_group = QGroupBox("Save to Glossary(s)")
        tb_layout = QVBoxLayout()
        
        if not self.active_termbases:
            no_tb_label = QLabel("⚠️ No active glossaries found. Please activate at least one glossary first.")
            no_tb_label.setStyleSheet("color: #d32f2f; padding: 10px;")
            no_tb_label.setWordWrap(True)
            tb_layout.addWidget(no_tb_label)
        else:
            # Header with select all/none buttons
            header_layout = QHBoxLayout()
            select_all_btn = QPushButton("Select All")
            select_all_btn.setMaximumWidth(100)
            select_none_btn = QPushButton("Select None")
            select_none_btn.setMaximumWidth(100)
            
            def select_all():
                for cb in self.termbase_checkboxes.values():
                    cb.setChecked(True)
            
            def select_none():
                for cb in self.termbase_checkboxes.values():
                    cb.setChecked(False)
            
            select_all_btn.clicked.connect(select_all)
            select_none_btn.clicked.connect(select_none)
            
            header_layout.addWidget(select_all_btn)
            header_layout.addWidget(select_none_btn)
            header_layout.addStretch()
            tb_layout.addLayout(header_layout)
            
            # Checkboxes for each active termbase
            for tb in self.active_termbases:
                is_project_tb = tb.get('is_project_termbase', False)
                
                # Use pink checkbox for project termbase, green for others
                if is_project_tb:
                    cb = PinkCheckmarkCheckBox(f"📌 {tb['name']} (Project)")
                else:
                    cb = CheckmarkCheckBox(tb['name'])
                
                # Use saved selection if available, otherwise default to all selected
                if self.saved_selections is not None:
                    cb.setChecked(tb['id'] in self.saved_selections)
                else:
                    cb.setChecked(True)  # Default: all selected
                cb.setToolTip(f"Languages: {tb.get('source_lang', '?')} → {tb.get('target_lang', '?')}")
                
                self.termbase_checkboxes[tb['id']] = cb
                tb_layout.addWidget(cb)
        
        tb_group.setLayout(tb_layout)
        layout.addWidget(tb_group)
        
        # Metadata fields
        meta_group = QGroupBox("Metadata (Optional)")
        meta_layout = QFormLayout()
        
        # Domain
        self.domain_edit = QLineEdit()
        self.domain_edit.setPlaceholderText("e.g., Patents, Legal, Medical, IT...")
        meta_layout.addRow("Domain:", self.domain_edit)
        
        # Notes
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(45)
        self.notes_edit.setPlaceholderText("Usage notes, context, definition, URLs...")
        self.notes_edit.setStyleSheet("padding: 3px; font-size: 10px;")
        meta_layout.addRow("Notes:", self.notes_edit)
        
        # Project
        self.project_edit = QLineEdit()
        self.project_edit.setPlaceholderText("Optional project name...")
        meta_layout.addRow("Project:", self.project_edit)
        
        # Client
        self.client_edit = QLineEdit()
        self.client_edit.setPlaceholderText("Optional client name...")
        meta_layout.addRow("Client:", self.client_edit)
        
        # Forbidden term checkbox
        self.forbidden_check = CheckmarkCheckBox("Mark as forbidden term")
        self.forbidden_check.setToolTip("Forbidden terms trigger warnings when used")
        meta_layout.addRow("", self.forbidden_check)
        
        meta_group.setLayout(meta_layout)
        layout.addWidget(meta_group)
        
        # Source Synonyms section (collapsible)
        source_syn_group = QGroupBox()
        source_syn_main_layout = QVBoxLayout()

        # Header with collapse button
        source_syn_header = QHBoxLayout()
        self.source_syn_toggle = QToolButton()
        self.source_syn_toggle.setText("▼")
        self.source_syn_toggle.setStyleSheet("QToolButton { border: none; font-weight: bold; }")
        self.source_syn_toggle.setFixedSize(20, 20)
        self.source_syn_toggle.setCheckable(True)
        self.source_syn_toggle.setChecked(False)
        source_syn_header.addWidget(self.source_syn_toggle)

        source_syn_label = QLabel("Source Synonyms (Optional)")
        source_syn_label.setStyleSheet("font-weight: bold;")
        source_syn_header.addWidget(source_syn_label)
        source_syn_header.addStretch()
        source_syn_main_layout.addLayout(source_syn_header)

        # Collapsible content
        self.source_syn_content = QWidget()
        source_syn_layout = QVBoxLayout(self.source_syn_content)
        source_syn_layout.setContentsMargins(0, 0, 0, 0)
        self.source_syn_content.setVisible(False)

        # Instructions
        source_syn_info = QLabel("Add alternative source terms. First item = preferred term:")
        source_syn_info.setStyleSheet("color: #666; font-size: 10px;")
        source_syn_layout.addWidget(source_syn_info)
        
        # Input field + Add button + Forbidden checkbox
        source_add_layout = QHBoxLayout()
        self.source_synonym_edit = QLineEdit()
        self.source_synonym_edit.setPlaceholderText("Enter source synonym and press Add or Enter...")
        source_add_layout.addWidget(self.source_synonym_edit)
        
        self.source_synonym_forbidden_check = CheckmarkCheckBox("Forbidden")
        self.source_synonym_forbidden_check.setToolTip("Mark this source synonym as forbidden")
        source_add_layout.addWidget(self.source_synonym_forbidden_check)
        
        source_add_syn_btn = QPushButton("Add")
        source_add_syn_btn.setMaximumWidth(60)
        source_add_syn_btn.clicked.connect(self.add_source_synonym)
        source_add_layout.addWidget(source_add_syn_btn)
        source_syn_layout.addLayout(source_add_layout)
        
        # Connect Enter key to add synonym
        self.source_synonym_edit.returnPressed.connect(self.add_source_synonym)
        
        # List of source synonyms with control buttons
        source_list_layout = QHBoxLayout()
        
        self.source_synonym_list = QListWidget()
        self.source_synonym_list.setMaximumHeight(100)
        self.source_synonym_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.source_synonym_list.customContextMenuRequested.connect(self.show_source_synonym_context_menu)
        source_list_layout.addWidget(self.source_synonym_list)
        
        # Up/Down buttons for source synonyms
        source_button_col = QVBoxLayout()
        source_move_up_btn = QPushButton("▲")
        source_move_up_btn.setToolTip("Move synonym up (higher priority)")
        source_move_up_btn.setMaximumWidth(30)
        source_move_up_btn.clicked.connect(self.move_source_synonym_up)
        source_button_col.addWidget(source_move_up_btn)
        
        source_move_down_btn = QPushButton("▼")
        source_move_down_btn.setToolTip("Move synonym down (lower priority)")
        source_move_down_btn.setMaximumWidth(30)
        source_move_down_btn.clicked.connect(self.move_source_synonym_down)
        source_button_col.addWidget(source_move_down_btn)
        
        source_button_col.addStretch()
        
        source_delete_btn = QPushButton("✗")
        source_delete_btn.setToolTip("Delete synonym")
        source_delete_btn.setMaximumWidth(30)
        source_delete_btn.clicked.connect(self.delete_selected_source_synonym)
        source_button_col.addWidget(source_delete_btn)
        
        source_list_layout.addLayout(source_button_col)
        source_syn_layout.addLayout(source_list_layout)

        # Add collapsible content to main layout
        source_syn_main_layout.addWidget(self.source_syn_content)
        source_syn_group.setLayout(source_syn_main_layout)

        # Connect toggle button
        self.source_syn_toggle.clicked.connect(lambda: self.toggle_section(self.source_syn_toggle, self.source_syn_content))

        layout.addWidget(source_syn_group)
        
        # Target Synonyms section (collapsible)
        target_syn_group = QGroupBox()
        target_syn_main_layout = QVBoxLayout()

        # Header with collapse button
        target_syn_header = QHBoxLayout()
        self.target_syn_toggle = QToolButton()
        self.target_syn_toggle.setText("▼")
        self.target_syn_toggle.setStyleSheet("QToolButton { border: none; font-weight: bold; }")
        self.target_syn_toggle.setFixedSize(20, 20)
        self.target_syn_toggle.setCheckable(True)
        self.target_syn_toggle.setChecked(False)
        target_syn_header.addWidget(self.target_syn_toggle)

        target_syn_label = QLabel("Target Synonyms (Optional)")
        target_syn_label.setStyleSheet("font-weight: bold;")
        target_syn_header.addWidget(target_syn_label)
        target_syn_header.addStretch()
        target_syn_main_layout.addLayout(target_syn_header)

        # Collapsible content
        self.target_syn_content = QWidget()
        target_syn_layout = QVBoxLayout(self.target_syn_content)
        target_syn_layout.setContentsMargins(0, 0, 0, 0)
        self.target_syn_content.setVisible(False)

        # Instructions
        target_syn_info = QLabel("Add alternative translations (synonyms). First item = preferred term:")
        target_syn_info.setStyleSheet("color: #666; font-size: 10px;")
        target_syn_layout.addWidget(target_syn_info)
        
        # Input field + Add button + Forbidden checkbox
        target_add_layout = QHBoxLayout()
        self.target_synonym_edit = QLineEdit()
        self.target_synonym_edit.setPlaceholderText("Enter synonym and press Add or Enter...")
        target_add_layout.addWidget(self.target_synonym_edit)
        
        self.target_synonym_forbidden_check = CheckmarkCheckBox("Forbidden")
        self.target_synonym_forbidden_check.setToolTip("Mark this synonym as forbidden (warning when used)")
        target_add_layout.addWidget(self.target_synonym_forbidden_check)
        
        target_add_syn_btn = QPushButton("Add")
        target_add_syn_btn.setMaximumWidth(60)
        target_add_syn_btn.clicked.connect(self.add_target_synonym)
        target_add_layout.addWidget(target_add_syn_btn)
        target_syn_layout.addLayout(target_add_layout)
        
        # Connect Enter key to add synonym
        self.target_synonym_edit.returnPressed.connect(self.add_target_synonym)
        
        # List of target synonyms with control buttons
        target_list_layout = QHBoxLayout()
        
        self.target_synonym_list = QListWidget()
        self.target_synonym_list.setMaximumHeight(100)
        self.target_synonym_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.target_synonym_list.customContextMenuRequested.connect(self.show_target_synonym_context_menu)
        target_list_layout.addWidget(self.target_synonym_list)
        
        # Up/Down buttons for target synonyms
        target_button_col = QVBoxLayout()
        target_move_up_btn = QPushButton("▲")
        target_move_up_btn.setToolTip("Move synonym up (higher priority)")
        target_move_up_btn.setMaximumWidth(30)
        target_move_up_btn.clicked.connect(self.move_target_synonym_up)
        target_button_col.addWidget(target_move_up_btn)
        
        target_move_down_btn = QPushButton("▼")
        target_move_down_btn.setToolTip("Move synonym down (lower priority)")
        target_move_down_btn.setMaximumWidth(30)
        target_move_down_btn.clicked.connect(self.move_target_synonym_down)
        target_button_col.addWidget(target_move_down_btn)
        
        target_button_col.addStretch()
        
        target_delete_btn = QPushButton("✗")
        target_delete_btn.setToolTip("Delete synonym")
        target_delete_btn.setMaximumWidth(30)
        target_delete_btn.clicked.connect(self.delete_selected_target_synonym)
        target_button_col.addWidget(target_delete_btn)
        
        target_list_layout.addLayout(target_button_col)
        target_syn_layout.addLayout(target_list_layout)

        # Add collapsible content to main layout
        target_syn_main_layout.addWidget(self.target_syn_content)
        target_syn_group.setLayout(target_syn_main_layout)

        # Connect toggle button
        self.target_syn_toggle.clicked.connect(lambda: self.toggle_section(self.target_syn_toggle, self.target_syn_content))

        layout.addWidget(target_syn_group)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Add to Glossary")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px 15px; border: none; outline: none;")
        save_btn.clicked.connect(self._accept_and_save)
        save_btn.setDefault(True)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

        # Set the scroll area content
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def toggle_section(self, toggle_btn, content_widget):
        """Toggle visibility of a collapsible section"""
        is_visible = content_widget.isVisible()
        content_widget.setVisible(not is_visible)
        toggle_btn.setText("▼" if is_visible else "▲")

    # ========================================================================
    # SOURCE SYNONYM METHODS
    # ========================================================================
    
    def add_source_synonym(self):
        """Add a source synonym to the list"""
        synonym = self.source_synonym_edit.text().strip()
        if synonym:
            # Check for duplicates
            for i in range(self.source_synonym_list.count()):
                item = self.source_synonym_list.item(i)
                item_text = item.data(Qt.ItemDataRole.UserRole).get('text', '')
                if item_text == synonym:
                    QMessageBox.warning(self, "Duplicate", f"Source synonym '{synonym}' already added.")
                    return
            
            # Don't allow the main source term as a synonym
            if synonym.lower() == self.source_term.lower():
                QMessageBox.warning(self, "Invalid Synonym", "Cannot add the main source term as a synonym.")
                return
            
            # Create list item with stored data
            is_forbidden = self.source_synonym_forbidden_check.isChecked()
            display_text = f"{'🚫 ' if is_forbidden else ''}{synonym}"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, {
                'text': synonym,
                'forbidden': is_forbidden
            })
            
            if is_forbidden:
                item.setForeground(QColor('#d32f2f'))
            
            self.source_synonym_list.addItem(item)
            self.source_synonym_edit.clear()
            self.source_synonym_forbidden_check.setChecked(False)
            self.source_synonym_edit.setFocus()
    
    def move_source_synonym_up(self):
        """Move selected source synonym up in the list"""
        current_row = self.source_synonym_list.currentRow()
        if current_row > 0:
            item = self.source_synonym_list.takeItem(current_row)
            self.source_synonym_list.insertItem(current_row - 1, item)
            self.source_synonym_list.setCurrentRow(current_row - 1)
    
    def move_source_synonym_down(self):
        """Move selected source synonym down in the list"""
        current_row = self.source_synonym_list.currentRow()
        if current_row < self.source_synonym_list.count() - 1 and current_row >= 0:
            item = self.source_synonym_list.takeItem(current_row)
            self.source_synonym_list.insertItem(current_row + 1, item)
            self.source_synonym_list.setCurrentRow(current_row + 1)
    
    def delete_selected_source_synonym(self):
        """Delete selected source synonym"""
        current_row = self.source_synonym_list.currentRow()
        if current_row >= 0:
            self.source_synonym_list.takeItem(current_row)
    
    def show_source_synonym_context_menu(self, position):
        """Show context menu for source synonym list"""
        if self.source_synonym_list.count() == 0:
            return
        
        current_item = self.source_synonym_list.currentItem()
        if not current_item:
            return
        
        menu = QMenu()
        
        # Toggle forbidden status
        data = current_item.data(Qt.ItemDataRole.UserRole)
        is_forbidden = data.get('forbidden', False)
        
        if is_forbidden:
            toggle_action = menu.addAction("Mark as Allowed")
        else:
            toggle_action = menu.addAction("Mark as Forbidden")
        
        menu.addSeparator()
        delete_action = menu.addAction("Delete")
        
        action = menu.exec(self.source_synonym_list.mapToGlobal(position))
        
        if action == toggle_action:
            # Toggle forbidden status
            data['forbidden'] = not is_forbidden
            text = data['text']
            display_text = f"{'🚫 ' if data['forbidden'] else ''}{text}"
            current_item.setText(display_text)
            current_item.setData(Qt.ItemDataRole.UserRole, data)
            
            if data['forbidden']:
                current_item.setForeground(QColor('#d32f2f'))
            else:
                current_item.setForeground(QColor('#000000'))
                
        elif action == delete_action:
            self.source_synonym_list.takeItem(self.source_synonym_list.row(current_item))
    
    def get_source_synonyms(self):
        """Return list of source synonym dictionaries with text, forbidden flag, and order"""
        synonyms = []
        for i in range(self.source_synonym_list.count()):
            item = self.source_synonym_list.item(i)
            data = item.data(Qt.ItemDataRole.UserRole)
            synonyms.append({
                'text': data['text'],
                'forbidden': data['forbidden'],
                'order': i
            })
        return synonyms
    
    # ========================================================================
    # TARGET SYNONYM METHODS
    # ========================================================================
    
    def add_target_synonym(self):
        """Add a target synonym to the list"""
        synonym = self.target_synonym_edit.text().strip()
        if synonym:
            # Check for duplicates
            for i in range(self.target_synonym_list.count()):
                item = self.target_synonym_list.item(i)
                item_text = item.data(Qt.ItemDataRole.UserRole).get('text', '')
                if item_text == synonym:
                    QMessageBox.warning(self, "Duplicate", f"Synonym '{synonym}' already added.")
                    return
            
            # Don't allow the main target term as a synonym
            if synonym.lower() == self.target_term.lower():
                QMessageBox.warning(self, "Invalid Synonym", "Cannot add the main target term as a synonym.")
                return
            
            # Create list item with stored data
            is_forbidden = self.target_synonym_forbidden_check.isChecked()
            display_text = f"{'🚫 ' if is_forbidden else ''}{synonym}"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, {
                'text': synonym,
                'forbidden': is_forbidden
            })
            
            if is_forbidden:
                item.setForeground(QColor('#d32f2f'))
            
            self.target_synonym_list.addItem(item)
            self.target_synonym_edit.clear()
            self.target_synonym_forbidden_check.setChecked(False)
            self.target_synonym_edit.setFocus()
    
    def move_target_synonym_up(self):
        """Move selected target synonym up in the list"""
        current_row = self.target_synonym_list.currentRow()
        if current_row > 0:
            item = self.target_synonym_list.takeItem(current_row)
            self.target_synonym_list.insertItem(current_row - 1, item)
            self.target_synonym_list.setCurrentRow(current_row - 1)
    
    def move_target_synonym_down(self):
        """Move selected target synonym down in the list"""
        current_row = self.target_synonym_list.currentRow()
        if current_row < self.target_synonym_list.count() - 1 and current_row >= 0:
            item = self.target_synonym_list.takeItem(current_row)
            self.target_synonym_list.insertItem(current_row + 1, item)
            self.target_synonym_list.setCurrentRow(current_row + 1)
    
    def delete_selected_target_synonym(self):
        """Delete selected target synonym"""
        current_row = self.target_synonym_list.currentRow()
        if current_row >= 0:
            self.target_synonym_list.takeItem(current_row)
    
    def show_target_synonym_context_menu(self, position):
        """Show context menu for target synonym list"""
        if self.target_synonym_list.count() == 0:
            return
        
        current_item = self.target_synonym_list.currentItem()
        if not current_item:
            return
        
        menu = QMenu()
        
        # Toggle forbidden status
        data = current_item.data(Qt.ItemDataRole.UserRole)
        is_forbidden = data.get('forbidden', False)
        
        if is_forbidden:
            toggle_action = menu.addAction("Mark as Allowed")
        else:
            toggle_action = menu.addAction("Mark as Forbidden")
        
        menu.addSeparator()
        delete_action = menu.addAction("Delete")
        
        action = menu.exec(self.target_synonym_list.mapToGlobal(position))
        
        if action == toggle_action:
            # Toggle forbidden status
            data['forbidden'] = not is_forbidden
            text = data['text']
            display_text = f"{'🚫 ' if data['forbidden'] else ''}{text}"
            current_item.setText(display_text)
            current_item.setData(Qt.ItemDataRole.UserRole, data)
            
            if data['forbidden']:
                current_item.setForeground(QColor('#d32f2f'))
            else:
                current_item.setForeground(QColor('#000000'))
                
        elif action == delete_action:
            self.target_synonym_list.takeItem(self.target_synonym_list.row(current_item))
    
    def get_target_synonyms(self):
        """Return list of target synonym dictionaries with text, forbidden flag, and order"""
        synonyms = []
        for i in range(self.target_synonym_list.count()):
            item = self.target_synonym_list.item(i)
            data = item.data(Qt.ItemDataRole.UserRole)
            synonyms.append({
                'text': data['text'],
                'forbidden': data['forbidden'],
                'order': i
            })
        return synonyms
    
    def get_metadata(self):
        """Return dictionary of metadata fields"""
        return {
            'domain': self.domain_edit.text().strip(),
            'notes': self.notes_edit.toPlainText().strip(),
            'project': self.project_edit.text().strip(),
            'client': self.client_edit.text().strip(),
            'forbidden': self.forbidden_check.isChecked()
        }
    
    def get_selected_termbases(self):
        """Return list of selected termbase IDs"""
        return [tb_id for tb_id, cb in self.termbase_checkboxes.items() if cb.isChecked()]
    
    def _accept_and_save(self):
        """Save termbase selections and accept the dialog"""
        self._save_termbase_selections()
        self.accept()


class VoiceCommandEditDialog(QDialog):
    """Dialog for adding/editing voice commands"""
    
    CATEGORIES = ["navigation", "editing", "translation", "lookup", "file", "view", "dictation", "memoq", "trados", "custom"]
    ACTION_TYPES = [
        ("internal", "Internal Action (Supervertaler)"),
        ("keystroke", "Keystroke (e.g., ctrl+s)"),
        ("ahk_inline", "AutoHotkey Code"),
        ("ahk_script", "AutoHotkey Script File"),
    ]
    
    def __init__(self, parent=None, command: VoiceCommand = None):
        super().__init__(parent)
        self.command = command
        self.setup_ui()
        
        if command:
            self.populate_from_command(command)
    
    def setup_ui(self):
        self.setWindowTitle("Edit Voice Command" if self.command else "Add Voice Command")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        # Phrase
        phrase_layout = QHBoxLayout()
        phrase_layout.addWidget(QLabel("Phrase:"))
        self.phrase_edit = QLineEdit()
        self.phrase_edit.setPlaceholderText("e.g., confirm segment")
        phrase_layout.addWidget(self.phrase_edit)
        layout.addLayout(phrase_layout)
        
        # Aliases
        aliases_layout = QHBoxLayout()
        aliases_layout.addWidget(QLabel("Aliases:"))
        self.aliases_edit = QLineEdit()
        self.aliases_edit.setPlaceholderText("e.g., confirm, done, okay (comma-separated)")
        aliases_layout.addWidget(self.aliases_edit)
        layout.addLayout(aliases_layout)
        
        # Action Type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        for value, label in self.ACTION_TYPES:
            self.type_combo.addItem(label, value)
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Action
        action_layout = QVBoxLayout()
        action_label = QLabel("Action:")
        action_layout.addWidget(action_label)
        self.action_edit = QTextEdit()
        self.action_edit.setMaximumHeight(100)
        self.action_edit.setPlaceholderText("For internal: action_name\nFor keystroke: ctrl+s\nFor AHK: Send, ^s")
        action_layout.addWidget(self.action_edit)
        layout.addLayout(action_layout)
        
        # Internal actions dropdown (for internal type)
        self.internal_actions_layout = QHBoxLayout()
        self.internal_actions_layout.addWidget(QLabel("Preset:"))
        self.internal_combo = QComboBox()
        self.internal_combo.addItems([
            "navigate_next", "navigate_previous", "navigate_first", "navigate_last",
            "confirm_segment", "copy_source_to_target", "clear_target",
            "translate_segment", "batch_translate",
            "open_superlookup", "concordance_search",
            "show_log", "show_editor",
            "start_dictation", "stop_listening"
        ])
        self.internal_combo.currentTextChanged.connect(lambda t: self.action_edit.setPlainText(t))
        self.internal_actions_layout.addWidget(self.internal_combo)
        self.internal_actions_layout.addStretch()
        layout.addLayout(self.internal_actions_layout)
        
        # Description
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("e.g., Confirm current segment")
        desc_layout.addWidget(self.desc_edit)
        layout.addLayout(desc_layout)
        
        # Category
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel("Category:"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(self.CATEGORIES)
        self.cat_combo.setEditable(True)
        cat_layout.addWidget(self.cat_combo)
        layout.addLayout(cat_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        save_btn.setDefault(True)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        # Initial type setup
        self._on_type_changed()
    
    def _on_type_changed(self):
        """Show/hide internal actions dropdown based on type"""
        is_internal = self.type_combo.currentData() == "internal"
        for i in range(self.internal_actions_layout.count()):
            widget = self.internal_actions_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(is_internal)
    
    def populate_from_command(self, cmd: VoiceCommand):
        """Populate dialog from existing command"""
        self.phrase_edit.setText(cmd.phrase)
        self.aliases_edit.setText(", ".join(cmd.aliases))
        
        # Find and set action type
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == cmd.action_type:
                self.type_combo.setCurrentIndex(i)
                break
        
        self.action_edit.setPlainText(cmd.action)
        self.desc_edit.setText(cmd.description)
        
        # Set category
        idx = self.cat_combo.findText(cmd.category)
        if idx >= 0:
            self.cat_combo.setCurrentIndex(idx)
        else:
            self.cat_combo.setCurrentText(cmd.category)
    
    def get_command(self) -> VoiceCommand:
        """Get the command from dialog inputs"""
        aliases_text = self.aliases_edit.text().strip()
        aliases = [a.strip() for a in aliases_text.split(",") if a.strip()] if aliases_text else []
        
        return VoiceCommand(
            phrase=self.phrase_edit.text().strip(),
            aliases=aliases,
            action_type=self.type_combo.currentData(),
            action=self.action_edit.toPlainText().strip(),
            description=self.desc_edit.text().strip(),
            category=self.cat_combo.currentText().strip(),
            enabled=True
        )


class AdvancedFiltersDialog(QDialog):
    """Dialog for advanced filtering options"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Advanced Filters")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        layout = QVBoxLayout(self)
        
        # Create scroll area for filters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(15)
        
        # Match Rate Filter
        match_group = QGroupBox("Match Rate (%)")
        match_layout = QHBoxLayout()
        
        self.match_rate_check = CheckmarkCheckBox("Enable")
        match_layout.addWidget(self.match_rate_check)
        
        match_layout.addWidget(QLabel("From:"))
        self.match_min_spin = QSpinBox()
        self.match_min_spin.setRange(0, 100)
        self.match_min_spin.setValue(0)
        self.match_min_spin.setSuffix("%")
        match_layout.addWidget(self.match_min_spin)
        
        match_layout.addWidget(QLabel("To:"))
        self.match_max_spin = QSpinBox()
        self.match_max_spin.setRange(0, 100)
        self.match_max_spin.setValue(100)
        self.match_max_spin.setSuffix("%")
        match_layout.addWidget(self.match_max_spin)
        match_layout.addStretch()
        
        match_group.setLayout(match_layout)
        content_layout.addWidget(match_group)
        
        # Row Status Filter
        status_group = QGroupBox("Row Status")
        status_layout = QVBoxLayout()
        
        self.status_not_started = CheckmarkCheckBox("Not started")
        self.status_edited = CheckmarkCheckBox("Edited")
        self.status_translated = CheckmarkCheckBox("Translated")
        self.status_confirmed = CheckmarkCheckBox("Confirmed")
        self.status_draft = CheckmarkCheckBox("Draft")
        
        status_layout.addWidget(self.status_not_started)
        status_layout.addWidget(self.status_edited)
        status_layout.addWidget(self.status_translated)
        status_layout.addWidget(self.status_confirmed)
        status_layout.addWidget(self.status_draft)
        
        status_group.setLayout(status_layout)
        content_layout.addWidget(status_group)
        
        # Locked/Unlocked Filter
        locked_group = QGroupBox("Locked Status")
        locked_layout = QVBoxLayout()
        
        self.locked_both = CheckmarkRadioButton("Both locked and unlocked rows")
        self.locked_only = CheckmarkRadioButton("Only locked rows")
        self.locked_unlocked_only = CheckmarkRadioButton("Only unlocked rows")
        self.locked_both.setChecked(True)
        
        locked_layout.addWidget(self.locked_both)
        locked_layout.addWidget(self.locked_only)
        locked_layout.addWidget(self.locked_unlocked_only)
        
        locked_group.setLayout(locked_layout)
        content_layout.addWidget(locked_group)
        
        # Other Properties
        other_group = QGroupBox("Other Properties")
        other_layout = QVBoxLayout()
        
        self.has_comments_check = CheckmarkCheckBox("Has comments/notes")
        self.has_proofreading_check = CheckmarkCheckBox("Has proofreading issues")
        self.repetitions_check = CheckmarkCheckBox("Repetitions only")
        self.auto_propagated_check = CheckmarkCheckBox("Auto-propagated")
        
        other_layout.addWidget(self.has_comments_check)
        other_layout.addWidget(self.has_proofreading_check)
        other_layout.addWidget(self.repetitions_check)
        other_layout.addWidget(self.auto_propagated_check)
        
        other_group.setLayout(other_layout)
        content_layout.addWidget(other_group)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        reset_btn = QPushButton("Reset All")
        reset_btn.clicked.connect(self.reset_filters)
        button_layout.addWidget(reset_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        apply_btn = QPushButton("Apply Filters")
        apply_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 5px 15px; border: none; outline: none;")
        apply_btn.clicked.connect(self.accept)
        apply_btn.setDefault(True)
        button_layout.addWidget(apply_btn)
        
        layout.addLayout(button_layout)
    
    def reset_filters(self):
        """Reset all filters to default"""
        self.match_rate_check.setChecked(False)
        self.match_min_spin.setValue(0)
        self.match_max_spin.setValue(100)
        
        self.status_not_started.setChecked(False)
        self.status_edited.setChecked(False)
        self.status_translated.setChecked(False)
        self.status_confirmed.setChecked(False)
        self.status_draft.setChecked(False)
        
        self.locked_both.setChecked(True)
        
        self.has_comments_check.setChecked(False)
        self.has_proofreading_check.setChecked(False)
        self.repetitions_check.setChecked(False)
        self.auto_propagated_check.setChecked(False)
    
    def get_filters(self):
        """Return dictionary of filter settings"""
        filters = {}
        
        # Match rate
        filters['match_rate_enabled'] = self.match_rate_check.isChecked()
        filters['match_rate_min'] = self.match_min_spin.value()
        filters['match_rate_max'] = self.match_max_spin.value()
        
        # Row status
        row_status = []
        if self.status_not_started.isChecked():
            row_status.append('not_started')
        if self.status_edited.isChecked():
            row_status.append('edited')
        if self.status_translated.isChecked():
            row_status.append('translated')
        if self.status_confirmed.isChecked():
            row_status.append('confirmed')
        if self.status_draft.isChecked():
            row_status.append('draft')
        filters['row_status'] = row_status
        
        # Locked filter
        if self.locked_only.isChecked():
            filters['locked_filter'] = 'locked'
        elif self.locked_unlocked_only.isChecked():
            filters['locked_filter'] = 'unlocked'
        else:
            filters['locked_filter'] = None
        
        # Other properties
        filters['has_comments'] = self.has_comments_check.isChecked()
        filters['has_proofreading'] = self.has_proofreading_check.isChecked()
        filters['repetitions_only'] = self.repetitions_check.isChecked()
        filters['auto_propagated'] = self.auto_propagated_check.isChecked()
        
        return filters


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
        
        # memoQ bilingual DOCX import tracking
        self.memoq_source_file = None
        
        # UI Configuration
        self.default_font_family = "Calibri"
        self.default_font_size = 11
        
        # Application settings
        self.allow_replace_in_source = False  # Safety: don't allow replace in source by default
        self.auto_propagate_exact_matches = True  # Auto-fill 100% TM matches for empty segments
        self.auto_insert_100_percent_matches = True  # Auto-insert 100% TM matches when segment selected
        self.auto_confirm_100_percent_matches = False  # Auto-confirm 100% matches when navigating with Ctrl+Enter
        self.tm_save_mode = 'latest'  # 'all' = keep all translations with timestamps, 'latest' = only keep most recent (DEFAULT)
        
        # Tab position setting
        self.tabs_above_grid = False  # Whether to show Termview/Session Log tabs above grid
        
        # TM and Termbase matching toggle (default: enabled)
        self.enable_tm_matching = True
        self.enable_termbase_matching = True
        self.enable_mt_matching = True  # Machine Translation enabled
        self.enable_llm_matching = False  # LLM Translation enabled (DISABLED by default - too slow for navigation!)
        self.enable_termbase_grid_highlighting = True  # Highlight termbase matches in source cells

        # Termbase display settings
        self.termbase_display_order = 'appearance'  # Options: 'alphabetical', 'appearance', 'length'
        self.termbase_hide_shorter_matches = False  # Hide shorter terms included in longer ones

        # Invisible character display settings
        self.showing_invisible_spaces = False  # Track whether spaces are shown as middle dots
        self.invisible_char_color = '#999999'  # Light gray color for invisible characters
        self.invisible_display_settings = {
            'spaces': False,
            'tabs': False,
            'nbsp': False,
            'linebreaks': False
        }

        # Grid row color settings (memoQ-style alternating row colors)
        self.enable_alternating_row_colors = True  # Enable alternating row colors by default
        self.even_row_color = '#FFFFFF'  # White for even rows
        self.odd_row_color = '#F0F0F0'  # Light gray for odd rows
        
        # Termbase highlight style settings
        self.termbase_highlight_style = 'semibold'  # 'background', 'dotted', or 'semibold'
        self.termbase_dotted_color = '#808080'  # Medium gray for dotted underline (more visible)
        
        # Focus border settings for target cells
        self.focus_border_color = '#2196F3'  # Blue
        self.focus_border_thickness = 2  # 2px

        # Debug mode settings (for troubleshooting performance issues)
        self.debug_mode_enabled = False  # Enables verbose debug logging
        self.debug_auto_export = False  # Auto-export debug logs to file
        self.debug_log_buffer = []  # Buffer for debug logs (for export)
        
        # Precision scroll settings (for fine-tuned grid navigation)
        self.precision_scroll_divisor = 3  # Divide row height by this (higher = finer increments)
        self.auto_center_active_segment = False  # Auto-scroll to keep active segment centered
        
        # Translation service availability flags (would be set from config/API keys)
        self.google_translate_enabled = True  # For demo purposes
        self.deepl_enabled = False  # Not implemented yet
        self.openai_enabled = True  # For demo purposes
        self.claude_enabled = True  # For demo purposes
        
        # Timer for delayed lookup (cancel if user moves to another segment)
        self.lookup_timer = None
        self.current_lookup_segment_id = None
        
        # Termbase cache for performance optimization
        # Maps segment ID → {term: translation} dictionary
        self.termbase_cache = {}
        self.termbase_cache_lock = threading.Lock()  # Thread-safe cache access
        self.termbase_batch_worker_thread = None  # Background worker thread
        self.termbase_batch_stop_event = threading.Event()  # Signal to stop background worker
        
        # TM/MT/LLM prefetch cache for instant segment switching (like memoQ)
        # Maps segment ID → {"TM": [...], "MT": [...], "LLM": [...]}
        self.translation_matches_cache = {}
        self.translation_matches_cache_lock = threading.Lock()
        self.prefetch_worker_thread = None
        self.prefetch_stop_event = threading.Event()
        self.prefetch_queue = []  # List of segment IDs to prefetch
        
        # Undo/Redo stack for grid edits
        self.undo_stack = []  # List of (segment_id, old_target, new_target, old_status, new_status)
        self.redo_stack = []  # List of undone actions that can be redone
        self.max_undo_levels = 100  # Maximum number of undo levels to keep
        
        # Global language settings (defaults)
        self.source_language = "English"
        self.target_language = "Dutch"

        # Supervoice model download tracking
        self.is_loading_model = False
        self.loading_model_name = None
        
        # Target editor signal suppression (prevents load-time churn)
        self._suppress_target_change_handlers = False
        self.warning_banners: Dict[str, QWidget] = {}
        
        # Superlookup detached window
        self.lookup_detached_window = None
        
        # Database Manager for Termbases
        from modules.database_manager import DatabaseManager
        self.user_data_path = Path("user_data_private" if ENABLE_PRIVATE_FEATURES else "user_data")
        self.db_manager = DatabaseManager(
            db_path=str(self.user_data_path / "Translation_Resources" / "supervertaler.db"),
            log_callback=self.log
        )
        self.db_manager.connect()
        
        # TM Database - Initialize early so Superlookup works without a project loaded
        from modules.translation_memory import TMDatabase
        self.tm_database = TMDatabase(
            source_lang=None,  # Will be set when project is loaded
            target_lang=None,  # Will be set when project is loaded
            db_path=str(self.user_data_path / "Translation_Resources" / "supervertaler.db"),
            log_callback=self.log
        )
        
        # TM Metadata Manager - needed for TM list in Superlookup
        from modules.tm_metadata_manager import TMMetadataManager
        self.tm_metadata_mgr = TMMetadataManager(self.db_manager, self.log)
        
        # Spellcheck Manager for target language spell checking
        self.spellcheck_manager = get_spellcheck_manager(str(self.user_data_path))
        # Note: spellcheck_enabled will be loaded from preferences later in _load_spellcheck_settings()
        # For now set to False, it gets updated when UI is created
        self.spellcheck_enabled = False
        # Set up the shared spellcheck manager for TagHighlighter instances
        TagHighlighter.set_spellcheck_manager(self.spellcheck_manager)
        TagHighlighter.set_spellcheck_enabled(self.spellcheck_enabled)
        
        # Find & Replace History Manager
        self.fr_history = FindReplaceHistory(str(self.user_data_path))
        
        # Voice Command Manager for Talon-style voice commands
        self.voice_command_manager = VoiceCommandManager(self.user_data_path, main_window=self)
        
        # Continuous Voice Listener (always-on mode) - initialized on demand
        self.voice_listener = None  # Will be ContinuousVoiceListener when enabled
        
        # Figure Context Manager for multimodal AI translation
        from modules.figure_context_manager import FigureContextManager
        self.figure_context = FigureContextManager(self)
        
        # Theme Manager
        from modules.theme_manager import ThemeManager
        self.theme_manager = None  # Will be initialized after UI setup
        
        # User data path - uses safety system to prevent private data leaks
        # If .supervertaler.local exists: uses "user_data_private" (git-ignored)
        # Otherwise: uses "user_data" (safe to commit)
        base_folder = "user_data_private" if ENABLE_PRIVATE_FEATURES else "user_data"
        self.recent_projects_file = self.user_data_path / "recent_projects.json"
        
        # Initialize UI
        self.init_ui()
        
        # Initialize theme manager and apply theme
        self.theme_manager = ThemeManager(self.user_data_path)
        self.theme_manager.apply_theme(QApplication.instance())
        
        # Update widgets that were created before theme_manager existed
        if hasattr(self, 'termview_widget') and self.termview_widget:
            self.termview_widget.theme_manager = self.theme_manager
            if hasattr(self.termview_widget, 'apply_theme'):
                self.termview_widget.apply_theme()
        
        if hasattr(self, 'translation_results_panel') and self.translation_results_panel:
            self.translation_results_panel.theme_manager = self.theme_manager
            # Also update class-level theme_manager for CompactMatchItem
            from modules.translation_results_panel import CompactMatchItem
            CompactMatchItem.theme_manager = self.theme_manager
            print(f"🎨 DEBUG: Calling apply_theme on translation_results_panel", flush=True)
            # Write to file for debugging
            with open("theme_debug.txt", "w") as f:
                f.write(f"apply_theme called, theme={self.theme_manager.current_theme.name}\n")
                f.write(f"compare_text_edits count: {len(self.translation_results_panel.compare_text_edits)}\n")
                f.flush()
            if hasattr(self.translation_results_panel, 'apply_theme'):
                self.translation_results_panel.apply_theme()
                print(f"🎨 DEBUG: apply_theme() called successfully", flush=True)
        else:
            print(f"🎨 DEBUG: translation_results_panel NOT FOUND!", flush=True)
            with open("theme_debug.txt", "w") as f:
                f.write("translation_results_panel NOT FOUND!\n")
                f.flush()
        
        # Schedule theme refresh after UI is fully initialized
        # This ensures all widgets are properly themed at startup
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, self.refresh_theme_colors)
        
        # Create example API keys file on first launch (after UI is ready)
        self.ensure_example_api_keys()
        
        self.log(f"Welcome to Supervertaler v{__version__}")
        self.log("Supervertaler: The Ultimate Translation Workbench.")
        
        # Load general settings (including auto-propagation)
        self.load_general_settings()
        
        # Load language settings
        self.load_language_settings()
        
        # Restore last project if enabled in settings
        self.restore_last_project_if_enabled()
        
        # Auto-open log window if enabled in settings
        general_settings = self.load_general_settings()
        if general_settings.get('auto_open_log', False):
            # Use QTimer to open log window after UI fully initializes
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(500, self.detach_log_window)  # 500ms delay to ensure UI is ready

        # Initialize auto backup timer
        self.auto_backup_timer = None
        self.last_backup_time = None
        self.restart_auto_backup_timer()

        # Load font sizes from preferences (after UI is fully initialized)
        QApplication.instance().processEvents()  # Allow UI to finish initializing
        self.load_font_sizes_from_preferences()
        
        # Auto-initialize Supermemory if enabled in settings
        if general_settings.get('supermemory_auto_init', False):
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(1000, self._auto_init_supermemory)  # 1 second delay to not block startup

        # Auto-check for new models if enabled in settings
        if general_settings.get('auto_check_models', True):
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, lambda: self._check_for_new_models(force=False))  # 2 second delay
        
        # First-run check - show Features tab to new users
        if not general_settings.get('first_run_completed', False):
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(500, self._show_first_run_welcome)
    
    def _show_first_run_welcome(self):
        """Show welcome message and Features tab on first run."""
        try:
            # Create a custom dialog with checkbox
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox, QDialogButtonBox
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Welcome to Supervertaler!")
            dialog.setMinimumWidth(450)
            
            layout = QVBoxLayout(dialog)
            layout.setSpacing(15)
            
            # Icon and title
            title_label = QLabel("<h2>Welcome to Supervertaler! 🎉</h2>")
            layout.addWidget(title_label)
            
            # Message
            msg_label = QLabel(
                "Supervertaler uses a <b>modular architecture</b> - you can install "
                "only the features you need to save disk space.<br><br>"
                "We'll now show you the <b>Features</b> tab where you can see which "
                "optional components are installed and how to add more.<br><br>"
                "💡 <b>Tip:</b> You can always access this from Settings → Features."
            )
            msg_label.setWordWrap(True)
            layout.addWidget(msg_label)
            
            # Checkbox - use our standard green checkmark style
            dont_show_checkbox = CheckmarkCheckBox("Don't show this again")
            dont_show_checkbox.setChecked(True)  # Default to not showing again
            layout.addWidget(dont_show_checkbox)
            
            # OK button
            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
            button_box.accepted.connect(dialog.accept)
            layout.addWidget(button_box)
            
            dialog.exec()
            
            # Navigate to Settings → Features tab
            self.main_tabs.setCurrentIndex(3)  # Settings tab
            if hasattr(self, 'settings_tabs'):
                # Find the Features tab index
                for i in range(self.settings_tabs.count()):
                    if "Features" in self.settings_tabs.tabText(i):
                        self.settings_tabs.setCurrentIndex(i)
                        break
            
            # Save the preference to ui_preferences.json (where load_general_settings reads from)
            if dont_show_checkbox.isChecked():
                prefs_file = self.user_data_path / "ui_preferences.json"
                prefs = {}
                if prefs_file.exists():
                    try:
                        with open(prefs_file, 'r') as f:
                            prefs = json.load(f)
                    except:
                        pass
                if 'general_settings' not in prefs:
                    prefs['general_settings'] = {}
                prefs['general_settings']['first_run_completed'] = True
                with open(prefs_file, 'w', encoding='utf-8') as f:
                    json.dump(prefs, f, indent=2)
                self.log("✅ First-run welcome completed (won't show again)")
            else:
                self.log("✅ First-run welcome shown (will show again next time)")
        except Exception as e:
            self.log(f"⚠️ First-run welcome error: {e}")
    
    def _auto_init_supermemory(self):
        """Auto-initialize Supermemory in the background at startup."""
        try:
            # Check if Supermemory widget exists (it's lazy-loaded)
            if not hasattr(self, 'supermemory_widget') or self.supermemory_widget is None:
                # Import and create the widget to trigger initialization
                try:
                    from modules.supermemory import SupermemoryWidget
                    self.supermemory_widget = SupermemoryWidget(self.user_data_path)
                    self.log("🧠 Supermemory auto-initialized at startup")
                    
                    # Check if engine initialized successfully
                    if self.supermemory_widget.engine and self.supermemory_widget.engine.is_initialized():
                        stats = self.supermemory_widget.engine.get_stats()
                        if stats.get('total_entries', 0) > 0:
                            self.log(f"  ✓ {stats['total_entries']:,} entries ready for semantic search")
                        else:
                            self.log("  ℹ No entries indexed yet. Go to Resources → Supermemory to index TMX files.")
                except ImportError as e:
                    self.log(f"  ⚠ Supermemory dependencies not installed: {e}")
                    self.log("  Run: pip install chromadb sentence-transformers")
            else:
                # Widget already exists, just ensure engine is initialized
                if self.supermemory_widget.engine and not self.supermemory_widget.engine.is_initialized():
                    self.supermemory_widget.engine.initialize()
                    self.log("🧠 Supermemory engine initialized")
        except Exception as e:
            error_msg = str(e)
            self.log(f"⚠ Supermemory auto-init failed: {error_msg}")

            # Provide helpful instructions for common Windows DLL errors
            if "DLL" in error_msg or "c10.dll" in error_msg or "torch" in error_msg.lower():
                self.log("  💡 PyTorch DLL loading failed. Try these fixes:")
                self.log("  1. Install Visual C++ Redistributables: https://aka.ms/vs/17/release/vc_redist.x64.exe")
                self.log("  2. Reinstall PyTorch: pip uninstall torch sentence-transformers")
                self.log("     Then: pip install torch sentence-transformers")
                self.log("  3. If still failing, disable Supermemory auto-init in Settings → AI Settings")

    def _check_for_new_models(self, force: bool = False):
        """
        Check for new LLM models from providers

        Args:
            force: Force check even if checked recently
        """
        try:
            from modules.model_version_checker import ModelVersionChecker
            from modules.model_update_dialog import ModelUpdateDialog, NoNewModelsDialog
            from modules.llm_clients import load_api_keys

            # Load API keys
            api_keys = load_api_keys()

            # Initialize checker with cache in user_data
            cache_path = self.user_data_path / "model_version_cache.json"
            checker = ModelVersionChecker(cache_path=str(cache_path))

            # Check if we should run (unless forced)
            if not force and not checker.should_check():
                # Already checked recently
                return

            self.log("🔍 Checking for new LLM models...")

            # Run the check
            results = checker.check_all_providers(
                openai_key=api_keys.get("OPENAI_API_KEY"),
                anthropic_key=api_keys.get("ANTHROPIC_API_KEY"),
                google_key=api_keys.get("GOOGLE_API_KEY"),
                force=force
            )

            # If this was a forced manual check, log the results
            if force:
                self.log(f"  OpenAI: {len(results.get('openai', {}).get('new_models', []))} new models")
                self.log(f"  Claude: {len(results.get('claude', {}).get('new_models', []))} new models")
                self.log(f"  Gemini: {len(results.get('gemini', {}).get('new_models', []))} new models")

            # Check if any new models found
            if checker.has_new_models(results):
                self.log(f"✨ New models detected! Opening dialog...")

                # Show dialog with new models
                dialog = ModelUpdateDialog(results, parent=self)
                dialog.models_selected.connect(self._on_new_models_selected)
                dialog.exec()

            else:
                # No new models
                if force:
                    # Only show "no new models" dialog for manual checks
                    cache_info = checker.get_cache_info()
                    dialog = NoNewModelsDialog(
                        last_check=cache_info.get('last_check'),
                        parent=self
                    )
                    dialog.exec()
                else:
                    # Silent for automatic checks
                    self.log("✓ No new models detected")

        except ImportError as e:
            self.log(f"⚠ Could not check for new models: Missing dependencies ({e})")
        except Exception as e:
            self.log(f"⚠ Error checking for new models: {e}")
            if force:
                # Show error dialog for manual checks
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "Model Check Error",
                    f"Failed to check for new models:\n\n{str(e)}"
                )

    def _on_new_models_selected(self, selected_models: dict):
        """
        Handle user selection of new models to add

        Args:
            selected_models: Dict of {provider: [model_ids]}
        """
        try:
            # Update the known models in llm_clients.py
            # For now, just log what would be added
            self.log("📦 Adding selected models to Supervertaler:")

            for provider, models in selected_models.items():
                if models:
                    self.log(f"  {provider.capitalize()}: {len(models)} model(s)")
                    for model in models:
                        self.log(f"    • {model}")

            # TODO: Actually add the models to the configuration
            # This would require modifying llm_clients.py or a separate config file
            # For now, just show a message
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "Models Added",
                f"Selected models have been noted:\n\n"
                f"{sum(len(m) for m in selected_models.values())} model(s) from "
                f"{len(selected_models)} provider(s)\n\n"
                f"These models will be available after restarting Supervertaler.\n\n"
                f"Note: You may need to manually add them to Settings → AI Settings for now."
            )

        except Exception as e:
            self.log(f"❌ Error adding models: {e}")

    def init_ui(self):
        """Initialize the user interface"""
        # Build window title with dev mode indicator
        title = f"Supervertaler v{__version__}"
        if ENABLE_PRIVATE_FEATURES:
            title += " [🛠️ DEV MODE]"
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 1400, 800)

        # Set application icon
        from PyQt6.QtGui import QIcon
        icon_path = get_resource_path("assets/icon.ico")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Ensure window can be resized (no minimum size constraint)
        self.setMinimumSize(400, 300)  # Very small minimum to allow resizing
        
        # Create menu bar (ribbon removed - using traditional menus)
        self.create_menus()
        
        # Ribbon removed - all functionality moved to menu bar
        # self.create_ribbon()
        
        # Create main layout
        self.create_main_layout()
        
        # Create status bar with progress indicators
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Add permanent progress widgets to status bar (right side)
        self._setup_progress_indicators()

        # Setup global shortcuts
        self.setup_global_shortcuts()

    def setup_global_shortcuts(self):
        """Setup application-wide keyboard shortcuts"""
        from PyQt6.QtGui import QShortcut

        # F9 - Voice dictation
        self.shortcut_dictate = QShortcut(QKeySequence("F9"), self)
        self.shortcut_dictate.activated.connect(self.start_voice_dictation)
        
        # Ctrl+Up/Down - Cycle through translation matches
        self.shortcut_match_up = QShortcut(QKeySequence("Ctrl+Up"), self)
        self.shortcut_match_up.activated.connect(self.select_previous_match)
        
        self.shortcut_match_down = QShortcut(QKeySequence("Ctrl+Down"), self)
        self.shortcut_match_down.activated.connect(self.select_next_match)
        
        # Ctrl+1 through Ctrl+9 - Insert match by number
        self.match_shortcuts = []
        for i in range(1, 10):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i}"), self)
            shortcut.activated.connect(lambda num=i: self.insert_match_by_number(num))
            self.match_shortcuts.append(shortcut)
        
        # Ctrl+Space - Insert currently selected match
        self.shortcut_insert_selected = QShortcut(QKeySequence("Ctrl+Space"), self)
        self.shortcut_insert_selected.activated.connect(self.insert_selected_match)
        
        # Alt+Up/Down - Navigate to previous/next segment
        self.shortcut_segment_up = QShortcut(QKeySequence("Alt+Up"), self)
        self.shortcut_segment_up.activated.connect(self.go_to_previous_segment)
        
        self.shortcut_segment_down = QShortcut(QKeySequence("Alt+Down"), self)
        self.shortcut_segment_down.activated.connect(self.go_to_next_segment)
        
        # Ctrl+Home/End - Navigate to first/last segment
        self.shortcut_go_to_top = QShortcut(QKeySequence("Ctrl+Home"), self)
        self.shortcut_go_to_top.activated.connect(self.go_to_first_segment)
        
        self.shortcut_go_to_bottom = QShortcut(QKeySequence("Ctrl+End"), self)
        self.shortcut_go_to_bottom.activated.connect(self.go_to_last_segment)
        
        # Ctrl+Enter - Confirm segment(s) and go to next unconfirmed
        # If multiple segments selected: confirm all selected
        # If single segment: confirm and go to next unconfirmed
        self.shortcut_confirm_next = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut_confirm_next.activated.connect(self.confirm_selected_or_next)
        
        # Ctrl+Shift+Enter - Always confirm all selected segments
        self.shortcut_confirm_selected = QShortcut(QKeySequence("Ctrl+Shift+Return"), self)
        self.shortcut_confirm_selected.activated.connect(self.confirm_selected_segments)
        
        # Note: Ctrl+Shift+S (Copy source to target) is handled in EditableGridTextEditor.keyPressEvent
        
        # Ctrl+K - Concordance Search
        self.shortcut_concordance = QShortcut(QKeySequence("Ctrl+K"), self)
        self.shortcut_concordance.activated.connect(self.show_concordance_search)
        
        # Ctrl+Shift+F - Filter on selected text / Clear filter (toggle)
        self.shortcut_filter_selected = QShortcut(QKeySequence("Ctrl+Shift+F"), self)
        self.shortcut_filter_selected.activated.connect(self.filter_on_selected_text)
        
        # Ctrl+Alt+T - Toggle Tag View
        self.shortcut_toggle_tags = QShortcut(QKeySequence("Ctrl+Alt+T"), self)
        self.shortcut_toggle_tags.activated.connect(self._toggle_tag_view_via_shortcut)
        
        # Page Up/Down - Navigate pagination pages
        self.shortcut_page_up = QShortcut(QKeySequence("PgUp"), self)
        self.shortcut_page_up.activated.connect(self.go_to_prev_page)
        
        self.shortcut_page_down = QShortcut(QKeySequence("PgDown"), self)
        self.shortcut_page_down.activated.connect(self.go_to_next_page)
        
        # Ctrl+G - Go to segment
        self.shortcut_goto = QShortcut(QKeySequence("Ctrl+G"), self)
        self.shortcut_goto.activated.connect(self.show_goto_dialog)

    def _setup_progress_indicators(self):
        """Setup permanent progress indicator widgets in the status bar"""
        from PyQt6.QtWidgets import QLabel, QFrame

        # Create a container frame for all progress info
        progress_frame = QFrame()
        progress_layout = QHBoxLayout(progress_frame)
        progress_layout.setContentsMargins(0, 0, 10, 0)
        progress_layout.setSpacing(20)

        # LLM Provider/Model indicator (leftmost in the permanent area)
        self.llm_indicator_label = QLabel("")
        self.llm_indicator_label.setStyleSheet("color: #888; font-size: 11px;")
        self.llm_indicator_label.setToolTip("Current LLM provider and model")
        progress_layout.addWidget(self.llm_indicator_label)
        
        # Update LLM indicator on startup
        self._update_llm_indicator()

        # Words translated label
        self.progress_words_label = QLabel("Words: --")
        self.progress_words_label.setStyleSheet("color: #555; font-size: 11px;")
        self.progress_words_label.setToolTip("Words with translation / Total words (percentage)")
        progress_layout.addWidget(self.progress_words_label)

        # Segments confirmed label
        self.progress_confirmed_label = QLabel("Confirmed: --")
        self.progress_confirmed_label.setStyleSheet("color: #555; font-size: 11px;")
        self.progress_confirmed_label.setToolTip("Confirmed segments / Total segments (percentage)")
        progress_layout.addWidget(self.progress_confirmed_label)

        # Remaining segments label
        self.progress_remaining_label = QLabel("Remaining: --")
        self.progress_remaining_label.setStyleSheet("color: #555; font-size: 11px;")
        self.progress_remaining_label.setToolTip("Segments still requiring work")
        progress_layout.addWidget(self.progress_remaining_label)
        
        # Files indicator (for multi-file projects)
        self.progress_files_label = QLabel("")
        self.progress_files_label.setStyleSheet("color: #2196F3; font-size: 11px;")
        self.progress_files_label.setToolTip("Files in multi-file project (click for details)")
        self.progress_files_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.progress_files_label.mousePressEvent = lambda e: self.show_file_progress_dialog()
        self.progress_files_label.hide()  # Hidden by default, shown for multi-file projects
        progress_layout.addWidget(self.progress_files_label)
        
        # Always-on voice indicator
        self.alwayson_indicator_label = QLabel("")
        self.alwayson_indicator_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        self.alwayson_indicator_label.setToolTip("Always-on voice listening status\nClick to toggle")
        self.alwayson_indicator_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.alwayson_indicator_label.mousePressEvent = lambda e: self._toggle_alwayson_from_statusbar()
        self.alwayson_indicator_label.hide()  # Hidden until enabled
        progress_layout.addWidget(self.alwayson_indicator_label)

        # Add as permanent widget (stays on right side)
        self.status_bar.addPermanentWidget(progress_frame)
        
        # Initialize Ollama keep-warm timer
        self.ollama_keepwarm_timer = None
        self._setup_ollama_keepwarm()
    
    def _update_llm_indicator(self):
        """Update the LLM provider/model indicator in the status bar"""
        try:
            settings = self.load_llm_settings()
            provider = settings.get('provider', 'openai')
            model_key = f'{provider}_model'
            model = settings.get(model_key, 'gpt-4o')
            
            # Format nicely
            if provider == 'ollama':
                icon = "🖥️"
                display = f"{icon} Local: {model}"
            elif provider == 'openai':
                icon = "🤖"
                display = f"{icon} {model}"
            elif provider == 'claude':
                icon = "🟣"
                display = f"{icon} {model}"
            elif provider == 'gemini':
                icon = "💎"
                display = f"{icon} {model}"
            else:
                display = f"{provider}: {model}"
            
            if hasattr(self, 'llm_indicator_label'):
                self.llm_indicator_label.setText(display)
                self.llm_indicator_label.setToolTip(f"LLM Provider: {provider.title()}\nModel: {model}")
        except Exception as e:
            if hasattr(self, 'llm_indicator_label'):
                self.llm_indicator_label.setText("")
    
    def _setup_ollama_keepwarm(self):
        """Setup timer to keep Ollama model warm (loaded in memory)"""
        from PyQt6.QtCore import QTimer
        
        # Check settings to see if keep-warm is enabled
        general_settings = self.load_general_settings()
        keepwarm_enabled = general_settings.get('ollama_keepwarm', False)
        
        if keepwarm_enabled:
            self._start_ollama_keepwarm_timer()
    
    def _start_ollama_keepwarm_timer(self):
        """Start the Ollama keep-warm timer (pings every 4 minutes)"""
        from PyQt6.QtCore import QTimer
        
        if self.ollama_keepwarm_timer is None:
            self.ollama_keepwarm_timer = QTimer(self)
            self.ollama_keepwarm_timer.timeout.connect(self._ping_ollama_keepwarm)
        
        # Ping every 4 minutes (Ollama unloads after 5 min of inactivity)
        self.ollama_keepwarm_timer.start(4 * 60 * 1000)  # 4 minutes in ms
        self.log("🔥 Ollama keep-warm enabled (pinging every 4 minutes)")
    
    def _stop_ollama_keepwarm_timer(self):
        """Stop the Ollama keep-warm timer"""
        if self.ollama_keepwarm_timer:
            self.ollama_keepwarm_timer.stop()
            self.log("❄️ Ollama keep-warm disabled")
    
    def _ping_ollama_keepwarm(self):
        """Send a minimal request to Ollama to keep the model loaded"""
        import threading
        
        def ping():
            try:
                import requests
                settings = self.load_llm_settings()
                if settings.get('provider') != 'ollama':
                    return
                
                model = settings.get('ollama_model', 'qwen2.5:7b')
                endpoint = "http://localhost:11434"
                
                # Send minimal request to keep model warm
                response = requests.post(
                    f"{endpoint}/api/generate",
                    json={
                        "model": model,
                        "prompt": "hi",
                        "options": {"num_predict": 1}  # Generate just 1 token
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    print(f"🔥 Ollama keep-warm ping successful ({model})")
            except Exception as e:
                print(f"⚠️ Ollama keep-warm ping failed: {e}")
        
        # Run in background thread to not block UI
        threading.Thread(target=ping, daemon=True).start()

    def update_progress_stats(self):
        """Update the progress indicator labels in the status bar"""
        try:
            if not self.current_project or not self.current_project.segments:
                self.progress_words_label.setText("Words: --")
                self.progress_confirmed_label.setText("Confirmed: --")
                self.progress_remaining_label.setText("Remaining: --")
                if hasattr(self, 'progress_files_label'):
                    self.progress_files_label.hide()
                return

            segments = self.current_project.segments
            total_segments = len(segments)

            # Count words in source text for each segment
            total_words = 0
            translated_words = 0
            confirmed_count = 0
            remaining_count = 0

            # Statuses that indicate "done" (confirmed or higher)
            confirmed_statuses = {'confirmed', 'tr_confirmed', 'proofread', 'approved'}
            # Statuses that need work
            unfinished_statuses = {'not_started', 'pretranslated', 'rejected'}

            for segment in segments:
                # Count words in source (simple split on whitespace)
                source_words = len(segment.source.split()) if segment.source else 0
                total_words += source_words

                # If segment has a non-empty translation, count those words as translated
                if segment.target and segment.target.strip():
                    translated_words += source_words

                # Count confirmed (or higher status)
                if segment.status in confirmed_statuses:
                    confirmed_count += 1

                # Count remaining (not_started, pretranslated, or rejected)
                if segment.status in unfinished_statuses:
                    remaining_count += 1

            # Calculate percentages
            word_percent = (translated_words / total_words * 100) if total_words > 0 else 0
            confirmed_percent = (confirmed_count / total_segments * 100) if total_segments > 0 else 0

            # Update labels with color-coding based on progress
            word_color = self._get_progress_color(word_percent)
            confirmed_color = self._get_progress_color(confirmed_percent)
            remaining_color = "#c00" if remaining_count > 0 else "#080"

            self.progress_words_label.setText(f"Words: {translated_words}/{total_words} ({word_percent:.0f}%)")
            self.progress_words_label.setStyleSheet(f"color: {word_color}; font-size: 11px;")

            self.progress_confirmed_label.setText(f"Confirmed: {confirmed_count}/{total_segments} ({confirmed_percent:.0f}%)")
            self.progress_confirmed_label.setStyleSheet(f"color: {confirmed_color}; font-size: 11px;")

            self.progress_remaining_label.setText(f"Remaining: {remaining_count}")
            self.progress_remaining_label.setStyleSheet(f"color: {remaining_color}; font-size: 11px;")
            
            # Multi-file project indicator
            if hasattr(self, 'progress_files_label'):
                is_multifile = getattr(self.current_project, 'is_multifile', False)
                files = getattr(self.current_project, 'files', [])
                
                if is_multifile and files:
                    # Count completed files
                    completed_files = 0
                    for file_info in files:
                        file_id = file_info['id']
                        file_segs = [s for s in segments if getattr(s, 'file_id', None) == file_id]
                        if file_segs:
                            conf_count = sum(1 for s in file_segs if s.status in confirmed_statuses)
                            if conf_count == len(file_segs):
                                completed_files += 1
                    
                    self.progress_files_label.setText(f"📁 Files: {completed_files}/{len(files)}")
                    self.progress_files_label.setToolTip(
                        f"Multi-file project: {len(files)} files\n"
                        f"Completed: {completed_files} files\n\n"
                        "Click for detailed file progress"
                    )
                    self.progress_files_label.show()
                else:
                    self.progress_files_label.hide()

        except Exception as e:
            self.log(f"⚠️ Error updating progress stats: {e}")

    def _get_progress_color(self, percent: float) -> str:
        """Get color for progress percentage: red < 50%, orange < 80%, green >= 80%"""
        if percent < 50:
            return "#c00"  # Red
        elif percent < 80:
            return "#c60"  # Orange
        else:
            return "#080"  # Green

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
        # No keyboard shortcut - Ctrl+Shift+S is used for Copy Source to Target in editor
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        close_action = QAction("&Close Project", self)
        close_action.triggered.connect(self.close_project)
        file_menu.addAction(close_action)
        
        file_menu.addSeparator()
        
        # Import/Export submenu
        import_menu = file_menu.addMenu("&Import")
        
        import_docx_action = QAction("&Monolingual Document (DOCX)...", self)
        import_docx_action.triggered.connect(self.import_docx)
        import_docx_action.setShortcut("Ctrl+O")
        import_menu.addAction(import_docx_action)
        
        import_txt_action = QAction("Simple &Text File (TXT)...", self)
        import_txt_action.triggered.connect(self.import_simple_txt)
        import_menu.addAction(import_txt_action)
        
        import_menu.addSeparator()
        
        # Multi-file folder import
        import_folder_action = QAction("📁 &Folder (Multiple Files)...", self)
        import_folder_action.triggered.connect(self.import_folder_multifile)
        import_menu.addAction(import_folder_action)
        
        import_menu.addSeparator()  # Separate monolingual from bilingual tools
        
        import_memoq_action = QAction("memoQ &Bilingual Table (DOCX)...", self)
        import_memoq_action.triggered.connect(self.import_memoq_bilingual)
        import_menu.addAction(import_memoq_action)
        
        import_cafetran_action = QAction("&CafeTran Bilingual Table (DOCX)...", self)
        import_cafetran_action.triggered.connect(self.import_cafetran_bilingual)
        import_menu.addAction(import_cafetran_action)
        
        # Trados submenu - group all Trados imports together
        trados_submenu = import_menu.addMenu("&Trados Studio")

        import_trados_bilingual_action = QAction("Bilingual &Review (DOCX)...", self)
        import_trados_bilingual_action.triggered.connect(self.import_trados_bilingual)
        trados_submenu.addAction(import_trados_bilingual_action)

        import_sdlppx_action = QAction("&Package (SDLPPX)...", self)
        import_sdlppx_action.triggered.connect(self.import_sdlppx_package)
        trados_submenu.addAction(import_sdlppx_action)

        # Phrase (Memsource) import
        import_phrase_bilingual_action = QAction("&Phrase (Memsource) Bilingual (DOCX)...", self)
        import_phrase_bilingual_action.triggered.connect(self.import_phrase_bilingual)
        import_menu.addAction(import_phrase_bilingual_action)

        import_menu.addSeparator()
        
        import_review_table_action = QAction("&Bilingual Table (DOCX) - Update Project...", self)
        import_review_table_action.triggered.connect(self.import_review_table)
        import_menu.addAction(import_review_table_action)
        
        export_menu = file_menu.addMenu("&Export")
        
        export_memoq_action = QAction("memoQ &Bilingual Table - Translated (DOCX)...", self)
        export_memoq_action.triggered.connect(self.export_memoq_bilingual)
        export_menu.addAction(export_memoq_action)
        
        export_cafetran_action = QAction("&CafeTran Bilingual Table - Translated (DOCX)...", self)
        export_cafetran_action.triggered.connect(self.export_cafetran_bilingual)
        export_menu.addAction(export_cafetran_action)
        
        # Trados submenu - group all Trados exports together
        trados_export_submenu = export_menu.addMenu("&Trados Studio")

        export_trados_bilingual_action = QAction("Bilingual &Review - Translated (DOCX)...", self)
        export_trados_bilingual_action.triggered.connect(self.export_trados_bilingual)
        trados_export_submenu.addAction(export_trados_bilingual_action)

        export_sdlrpx_action = QAction("Return &Package (SDLRPX)...", self)
        export_sdlrpx_action.triggered.connect(self.export_sdlrpx_package)
        trados_export_submenu.addAction(export_sdlrpx_action)

        # Phrase (Memsource) export
        export_phrase_bilingual_action = QAction("&Phrase (Memsource) Bilingual - Translated (DOCX)...", self)
        export_phrase_bilingual_action.triggered.connect(self.export_phrase_bilingual)
        export_menu.addAction(export_phrase_bilingual_action)
        
        export_target_docx_action = QAction("&Target Only (DOCX)...", self)
        export_target_docx_action.triggered.connect(self.export_target_only_docx)
        export_menu.addAction(export_target_docx_action)
        
        export_txt_action = QAction("Simple &Text File - Translated (TXT)...", self)
        export_txt_action.triggered.connect(self.export_simple_txt)
        export_menu.addAction(export_txt_action)
        
        export_ai_action = QAction("🤖 &AI-Readable Format (TXT)...", self)
        export_ai_action.triggered.connect(self.export_for_ai)
        export_ai_action.setToolTip("Export segments in [SEGMENT] format for AI translation/review")
        export_menu.addAction(export_ai_action)
        
        export_menu.addSeparator()
        
        # Multi-file folder export
        export_folder_action = QAction("📁 &Folder (Multiple Files)...", self)
        export_folder_action.triggered.connect(self.export_folder_multifile)
        export_folder_action.setToolTip("Export multi-file project to folder with separate files")
        export_menu.addAction(export_folder_action)
        
        export_menu.addSeparator()
        
        # Relocate source folder for multi-file projects
        relocate_source_action = QAction("🔗 &Relocate Source Folder...", self)
        relocate_source_action.triggered.connect(self.relocate_source_folder)
        relocate_source_action.setToolTip("Repoint to moved/renamed source folder for multi-file project")
        export_menu.addAction(relocate_source_action)
        
        export_menu.addSeparator()
        
        # Supervertaler Bilingual Table exports
        export_review_table_action = QAction("Supervertaler Bilingual Table - With &Tags (DOCX)...", self)
        export_review_table_action.triggered.connect(self.export_review_table_with_tags)
        export_menu.addAction(export_review_table_action)
        
        export_review_table_formatted_action = QAction("Supervertaler Bilingual Table - &Formatted (DOCX)...", self)
        export_review_table_formatted_action.triggered.connect(self.export_review_table_formatted)
        export_menu.addAction(export_review_table_formatted_action)
        
        export_menu.addSeparator()
        
        export_grid_action = QAction("TMX from &Grid (all segments)...", self)
        export_grid_action.triggered.connect(self.export_tmx_from_grid)
        export_menu.addAction(export_grid_action)
        
        export_selected_action = QAction("TMX from &Selected Segments...", self)
        export_selected_action.triggered.connect(self.export_tmx_from_selected)
        export_menu.addAction(export_selected_action)
        
        export_tm_action = QAction("TMX from &TM(s) for Current Project...", self)
        export_tm_action.triggered.connect(self.export_tmx_from_tm_database)
        export_menu.addAction(export_tm_action)
        
        file_menu.addSeparator()
        
        # Project Info
        project_info_action = QAction("📋 Project &Info...", self)
        project_info_action.triggered.connect(self.show_project_info_dialog)
        file_menu.addAction(project_info_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        
        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(self.undo_action_handler)
        self.undo_action.setEnabled(False)
        edit_menu.addAction(self.undo_action)
        
        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(self.redo_action_handler)
        self.redo_action.setEnabled(False)
        edit_menu.addAction(self.redo_action)
        
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
        
        goto_action = QAction("&Go to Segment...\tCtrl+G", self)
        goto_action.triggered.connect(self.show_goto_dialog)
        edit_menu.addAction(goto_action)
        
        edit_menu.addSeparator()
        
        translate_action = QAction("&Translate Segment", self)
        translate_action.setShortcut("Ctrl+T")
        translate_action.triggered.connect(self.translate_current_segment)
        edit_menu.addAction(translate_action)

        translate_menu = edit_menu.addMenu("Batch &Translate")

        translate_selected_not_started_action = QAction("Translate selected not-started segments", self)
        translate_selected_not_started_action.triggered.connect(
            lambda checked=False: self.translate_multiple_segments("selected_not_started")
        )
        translate_menu.addAction(translate_selected_not_started_action)

        translate_all_not_started_action = QAction("Translate all not-started segments", self)
        translate_all_not_started_action.triggered.connect(
            lambda checked=False: self.translate_multiple_segments("all_not_started")
        )
        translate_menu.addAction(translate_all_not_started_action)

        translate_all_pretranslated_action = QAction("Translate all pre-translated segments", self)
        translate_all_pretranslated_action.triggered.connect(
            lambda checked=False: self.translate_multiple_segments("all_pretranslated")
        )
        translate_menu.addAction(translate_all_pretranslated_action)

        translate_pending_action = QAction("Translate all not-started & pre-translated", self)
        translate_pending_action.setShortcut("Ctrl+Shift+T")
        translate_pending_action.triggered.connect(
            lambda checked=False: self.translate_multiple_segments("all_not_started_pretranslated")
        )
        translate_menu.addAction(translate_pending_action)

        translate_translatable_action = QAction("Translate all translatable segments", self)
        translate_translatable_action.triggered.connect(
            lambda checked=False: self.translate_multiple_segments("all_translatable")
        )
        translate_menu.addAction(translate_translatable_action)

        translate_all_segments_action = QAction("Translate all segments (all statuses)", self)
        translate_all_segments_action.triggered.connect(
            lambda checked=False: self.translate_multiple_segments("all_segments")
        )
        translate_menu.addAction(translate_all_segments_action)
        
        translate_menu.addSeparator()
        
        # NEW: Translate only empty segments (for re-running failed batches)
        translate_empty_action = QAction("Translate all empty segments", self)
        translate_empty_action.setToolTip("Translate segments with empty target (useful after partial batch translation)")
        translate_empty_action.triggered.connect(
            lambda checked=False: self.translate_multiple_segments("all_empty")
        )
        translate_menu.addAction(translate_empty_action)
        
        translate_filtered_action = QAction("Translate all filtered segments", self)
        translate_filtered_action.setToolTip("Translate only segments currently visible after filtering")
        translate_filtered_action.triggered.connect(
            lambda checked=False: self.translate_multiple_segments("filtered_segments")
        )
        translate_menu.addAction(translate_filtered_action)
        
        edit_menu.addSeparator()
        
        # Bulk Operations submenu
        bulk_menu = edit_menu.addMenu("Bulk &Operations")
        
        confirm_selected_action = QAction("✅ &Confirm Selected Segments", self)
        confirm_selected_action.setShortcut("Ctrl+Shift+Return")
        confirm_selected_action.setToolTip("Confirm all selected segments (Ctrl+Shift+Enter)")
        confirm_selected_action.triggered.connect(self.confirm_selected_segments_from_menu)
        bulk_menu.addAction(confirm_selected_action)
        
        clear_translations_action = QAction("🗑️ &Clear Translations", self)
        clear_translations_action.setToolTip("Clear translations for selected segments")
        clear_translations_action.triggered.connect(self.clear_selected_translations_from_menu)
        bulk_menu.addAction(clear_translations_action)
        
        copy_source_to_target_action = QAction("📋 Copy &Source to Target", self)
        copy_source_to_target_action.setToolTip("Copy source text to target for selected/filtered segments")
        copy_source_to_target_action.triggered.connect(self.copy_source_to_target_bulk)
        bulk_menu.addAction(copy_source_to_target_action)
        
        send_to_tm_action = QAction("💾 &Send Segments to TM...", self)
        send_to_tm_action.setToolTip("Send confirmed segments to a writable Translation Memory")
        send_to_tm_action.triggered.connect(self.send_segments_to_tm_dialog)
        bulk_menu.addAction(send_to_tm_action)
        
        bulk_menu.addSeparator()
        
        clean_tags_action = QAction("🧹 Clean &Tags...", self)
        clean_tags_action.setToolTip("Remove formatting tags from selected segments")
        clean_tags_action.triggered.connect(self.show_clean_tags_dialog)
        bulk_menu.addAction(clean_tags_action)
        
        proofread_action = QAction("✅ &Proofread Translation...", self)
        proofread_action.setToolTip("Use AI to proofread and verify translation quality")
        proofread_action.triggered.connect(self.show_proofread_dialog)
        bulk_menu.addAction(proofread_action)
        
        clear_proofread_notes_action = QAction("🗑️ Clear All &Proofreading Notes", self)
        clear_proofread_notes_action.setToolTip("Remove all AI proofreading notes from entire project (preserves your personal notes)")
        clear_proofread_notes_action.triggered.connect(self._bulk_clear_proofreading_notes)
        bulk_menu.addAction(clear_proofread_notes_action)
        
        edit_menu.addSeparator()
        
        # Superlookup
        superlookup_action = QAction("🔍 &Superlookup...", self)
        superlookup_action.setShortcut("Ctrl+Alt+L")
        # Tab indices: Project editor=0, Project resources=1, Tools=2, Settings=3
        superlookup_action.triggered.connect(lambda: self._go_to_superlookup() if hasattr(self, 'main_tabs') else None)  # Navigate to Superlookup
        edit_menu.addAction(superlookup_action)
        
        # View Menu
        view_menu = menubar.addMenu("&View")
        
        # Navigation submenu
        nav_menu = view_menu.addMenu("📑 &Navigate To")
        
        go_editor_action = QAction("📝 Project &editor", self)
        go_editor_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(0) if hasattr(self, 'main_tabs') else None)
        nav_menu.addAction(go_editor_action)
        
        go_resources_action = QAction("🗂️ Project &resources", self)
        go_resources_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(1) if hasattr(self, 'main_tabs') else None)
        nav_menu.addAction(go_resources_action)
        
        go_tools_action = QAction("🛠️ &Tools", self)
        go_tools_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(2) if hasattr(self, 'main_tabs') else None)
        nav_menu.addAction(go_tools_action)
        
        go_settings_action = QAction("⚙️ &Settings", self)
        go_settings_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(3) if hasattr(self, 'main_tabs') else None)
        nav_menu.addAction(go_settings_action)
        
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

        view_menu.addSeparator()
        
        # Multi-file project progress
        file_progress_action = QAction("📁 &File Progress...", self)
        file_progress_action.triggered.connect(self.show_file_progress_dialog)
        file_progress_action.setToolTip("View translation progress per file (multi-file projects)")
        view_menu.addAction(file_progress_action)
        
        # Proofreading results
        proofread_results_action = QAction("✅ &Proofreading Results...", self)
        proofread_results_action.triggered.connect(self.show_proofreading_results_dialog)
        proofread_results_action.setToolTip("View and manage proofreading issues")
        view_menu.addAction(proofread_results_action)

        view_menu.addSeparator()

        theme_action = QAction("🎨 &Theme Editor...", self)
        theme_action.triggered.connect(self.show_theme_editor)
        view_menu.addAction(theme_action)

        # Tools Menu
        tools_menu = menubar.addMenu("&Tools")
        
        autofingers_action = QAction("✋ &AutoFingers - CAT Tool Automation...", self)
        autofingers_action.setShortcut("Ctrl+Shift+A")
        autofingers_action.triggered.connect(self.show_autofingers)
        tools_menu.addAction(autofingers_action)
        
        tools_menu.addSeparator()
        
        image_extractor_action = QAction("🖼️ &Image Extractor (Superimage)...", self)
        image_extractor_action.triggered.connect(self.show_image_extractor_from_tools)
        image_extractor_action.setToolTip("Extract images from DOCX files")
        tools_menu.addAction(image_extractor_action)
        
        tools_menu.addSeparator()

        settings_action = QAction("&Settings...", self)
        settings_action.triggered.connect(lambda: self._go_to_settings_tab())
        tools_menu.addAction(settings_action)
        
        # Help Menu
        help_menu = menubar.addMenu("&Help")

        # Documentation links (GitHub URLs for universal access)
        # Removed internal manual link — documentation migrated to GitBook

        # Place Supervertaler Help at the top of the Help menu
        superdocs_action = QAction("Supervertaler Help", self)
        superdocs_action.setToolTip("Superdocs (GitBook)")
        superdocs_action.triggered.connect(lambda: self._open_url("https://supervertaler.gitbook.io/superdocs/"))
        help_menu.addAction(superdocs_action)

        help_menu.addSeparator()

        shortcuts_action = QAction("⌨️ Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(lambda: self._open_url("https://github.com/michaelbeijer/Supervertaler/blob/main/docs/guides/KEYBOARD_SHORTCUTS.md"))
        help_menu.addAction(shortcuts_action)

        changelog_action = QAction("📝 Changelog", self)
        changelog_action.triggered.connect(lambda: self._open_url("https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md"))
        help_menu.addAction(changelog_action)

        help_menu.addSeparator()

        github_action = QAction("🔗 GitHub Repository", self)
        github_action.triggered.connect(lambda: self._open_url("https://github.com/michaelbeijer/Supervertaler"))
        help_menu.addAction(github_action)

        help_menu.addSeparator()
        
        # AutoHotkey setup (Windows only)
        if os.name == 'nt':
            ahk_setup_action = QAction("⌨️ Setup AutoHotkey (Global Hotkey)", self)
            ahk_setup_action.setToolTip("Configure AutoHotkey for Superlookup global hotkey (Ctrl+Alt+L)")
            ahk_setup_action.triggered.connect(self._show_ahk_setup_from_menu)
            help_menu.addAction(ahk_setup_action)
            help_menu.addSeparator()

        about_action = QAction("ℹ️ About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def record_undo_state(self, segment_id, old_target, new_target, old_status, new_status):
        """Record an undo state when grid cells are edited"""
        # Don't record if nothing actually changed
        if old_target == new_target and old_status == new_status:
            return
        
        # Add to undo stack
        undo_entry = {
            "segment_id": segment_id,
            "old_target": old_target,
            "new_target": new_target,
            "old_status": old_status,
            "new_status": new_status
        }
        self.undo_stack.append(undo_entry)
        
        # Trim undo stack to max levels
        if len(self.undo_stack) > self.max_undo_levels:
            self.undo_stack.pop(0)
        
        # Clear redo stack (can't redo after new edit)
        self.redo_stack.clear()
        
        # Update menu actions
        self.update_undo_redo_actions()
    
    def undo_action_handler(self):
        """Handle Undo (Ctrl+Z) action"""
        if not self.undo_stack:
            return
        
        # Pop last action from undo stack
        action = self.undo_stack.pop()
        
        # Find the segment
        segment_id = action["segment_id"]
        segment = None
        for seg in self.current_project.segments:
            if seg.segment_id == segment_id:
                segment = seg
                break
        
        if not segment:
            return
        
        # Revert to old values
        segment.target_text = action["old_target"]
        segment.status = action["old_status"]
        
        # Update grid display
        row = self.find_grid_row_by_segment_id(segment_id)
        if row is not None:
            # Update target text cell
            target_item = self.grid.item(row, 2)
            if target_item:
                target_item.setText(action["old_target"])
            
            # Update status cell
            status_item = self.grid.item(row, 3)
            if status_item:
                status_item.setText(action["old_status"])
        
        # Move action to redo stack
        self.redo_stack.append(action)
        
        # Update menu actions
        self.update_undo_redo_actions()
    
    def redo_action_handler(self):
        """Handle Redo (Ctrl+Shift+Z / Ctrl+Y) action"""
        if not self.redo_stack:
            return
        
        # Pop last action from redo stack
        action = self.redo_stack.pop()
        
        # Find the segment
        segment_id = action["segment_id"]
        segment = None
        for seg in self.current_project.segments:
            if seg.segment_id == segment_id:
                segment = seg
                break
        
        if not segment:
            return
        
        # Reapply new values
        segment.target_text = action["new_target"]
        segment.status = action["new_status"]
        
        # Update grid display
        row = self.find_grid_row_by_segment_id(segment_id)
        if row is not None:
            # Update target text cell
            target_item = self.grid.item(row, 2)
            if target_item:
                target_item.setText(action["new_target"])
            
            # Update status cell
            status_item = self.grid.item(row, 3)
            if status_item:
                status_item.setText(action["new_status"])
        
        # Move action back to undo stack
        self.undo_stack.append(action)
        
        # Update menu actions
        self.update_undo_redo_actions()
    
    def update_undo_redo_actions(self):
        """Update enabled/disabled state of undo/redo menu actions"""
        self.undo_action.setEnabled(len(self.undo_stack) > 0)
        self.redo_action.setEnabled(len(self.redo_stack) > 0)
    
    def find_grid_row_by_segment_id(self, segment_id):
        """Find the grid row index for a given segment ID"""
        for row in range(self.grid.rowCount()):
            id_item = self.grid.item(row, 0)
            if id_item and id_item.text() == str(segment_id):
                return row
        return None
    
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
    
    def create_main_layout(self):
        """Create main application layout with all-tab interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # ===== SIMPLIFIED TAB-BASED UI =====
        # Single tab widget with all functionality
        from modules.unified_prompt_manager_qt import UnifiedPromptManagerQt
        
        # Create main tab widget
        self.main_tabs = QTabWidget()
        self.main_tabs.tabBar().setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.main_tabs.tabBar().setDrawBase(False)
        self.main_tabs.setStyleSheet("""
            QTabBar::tab { padding: 8px 15px; outline: 0; }
            QTabBar::tab:focus { outline: none; }
            QTabBar::tab:selected { 
                border-bottom: 1px solid #2196F3; 
                background-color: rgba(33, 150, 243, 0.08);
            }
        """)
        
        # ===== 1. PROJECT EDITOR TAB =====
        # Contains the translation grid
        grid_widget = self.create_grid_view_widget_for_home()
        self.main_tabs.addTab(grid_widget, "📝 Project editor")
        
        # ===== 2. PROJECT RESOURCES TAB =====
        # Contains TM, Termbases, Supermemory, Non-Translatables, Prompts
        resources_tab = self.create_resources_tab()
        self.main_tabs.addTab(resources_tab, "🗂️ Project resources")
        
        # Keep backward compatibility reference
        self.document_views_widget = self.main_tabs
        
        # 3. TOOLS
        tools_tab = self.create_specialised_tools_tab()
        self.main_tabs.addTab(tools_tab, "🛠️ Tools")

        # 4. SETTINGS
        settings_tab = self.create_settings_tab()
        self.main_tabs.addTab(settings_tab, "⚙️ Settings")
        
        main_layout.addWidget(self.main_tabs)
        
        # 