"""
Unified Prompt Manager Module - Qt Edition
Simplified 2-Layer Architecture:

1. System Prompts (in Settings) - mode-specific, auto-selected based on document type
2. Prompt Library (main UI) - unified workspace with folders, favorites, multi-attach

This replaces the old 4-layer system (System/Domain/Project/Style Guides).
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QPlainTextEdit, QSplitter, QGroupBox, QMessageBox, QFileDialog,
    QInputDialog, QLineEdit, QFrame, QMenu, QCheckBox, QSizePolicy, QScrollArea, QTabWidget,
    QListWidget, QListWidgetItem, QStyledItemDelegate, QStyleOptionViewItem, QApplication, QDialog,
    QAbstractItemView, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QThread, QSize, QRect, QRectF
from PyQt6.QtGui import QFont, QColor, QAction, QIcon, QPainter, QPen, QBrush, QPainterPath, QLinearGradient

from modules.unified_prompt_library import UnifiedPromptLibrary
from modules.llm_clients import LLMClient, load_api_keys
from modules.prompt_library_migration import migrate_prompt_library
from modules.ai_attachment_manager import AttachmentManager
from modules.ai_file_viewer_dialog import FileViewerDialog, FileRemoveConfirmDialog
from modules.ai_actions import AIActionSystem


class CheckmarkCheckBox(QCheckBox):
    """Custom checkbox with green background and white checkmark when checked"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setEnabled(True)
        self.setStyleSheet("""
            QCheckBox {
                font-size: 9pt;
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
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
            from PyQt6.QtCore import QPointF
            
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
                pen_width = max(2.0, min(indicator_rect.width(), indicator_rect.height()) * 0.12)
                painter.setPen(QPen(QColor(255, 255, 255), pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
                painter.setBrush(QColor(255, 255, 255))
                
                # Draw checkmark (✓ shape) - coordinates relative to indicator
                x = indicator_rect.x()
                y = indicator_rect.y()
                w = indicator_rect.width()
                h = indicator_rect.height()
                
                # Add padding (15% on all sides)
                padding = min(w, h) * 0.15
                x += padding
                y += padding
                w -= padding * 2
                h -= padding * 2
                
                # Checkmark path
                check_x1 = x + w * 0.10
                check_y1 = y + h * 0.50
                check_x2 = x + w * 0.35
                check_y2 = y + h * 0.70
                check_x3 = x + w * 0.90
                check_y3 = y + h * 0.25
                
                # Draw two lines forming the checkmark
                painter.drawLine(QPointF(check_x2, check_y2), QPointF(check_x3, check_y3))
                painter.drawLine(QPointF(check_x1, check_y1), QPointF(check_x2, check_y2))


class PromptLibraryTreeWidget(QTreeWidget):
    """Tree widget that supports drag-and-drop moves for prompt files."""

    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self._manager = manager

        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)

    def dropEvent(self, event):
        """Handle prompt/folder moves via filesystem operations."""
        try:
            selected = self.selectedItems()
            if not selected:
                event.ignore()
                return

            source_item = selected[0]
            source_data = source_item.data(0, Qt.ItemDataRole.UserRole)
            if not source_data:
                event.ignore()
                return

            src_type = source_data.get('type')
            src_path = source_data.get('path')
            if src_type not in {'prompt', 'folder'} or not src_path:
                event.ignore()
                return

            pos = event.position().toPoint() if hasattr(event, 'position') else event.pos()
            target_item = self.itemAt(pos)
            target_data = target_item.data(0, Qt.ItemDataRole.UserRole) if target_item else None

            # Determine destination folder.
            dest_folder = ''
            if target_data:
                if target_data.get('type') == 'folder':
                    dest_folder = target_data.get('path', '')
                elif target_data.get('type') == 'prompt':
                    dest_folder = str(Path(target_data.get('path', '')).parent)
                    if dest_folder == '.':
                        dest_folder = ''
                else:
                    # Special nodes like Favorites / Quick Run: ignore.
                    event.ignore()
                    return

            moved = False
            if src_type == 'prompt' and self._manager and hasattr(self._manager, '_move_prompt_to_folder'):
                moved = self._manager._move_prompt_to_folder(src_path, dest_folder)

            if src_type == 'folder' and self._manager and hasattr(self._manager, '_move_folder_to_folder'):
                moved = self._manager._move_folder_to_folder(src_path, dest_folder)

            if moved:
                event.acceptProposedAction()
            else:
                event.ignore()

        except Exception:
            event.ignore()
            return


class ChatMessageDelegate(QStyledItemDelegate):
    """Custom delegate for rendering chat messages with proper bubble styling"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.padding = 16
        self.bubble_padding = 12
        self.avatar_size = 28
        self.avatar_margin = 8
        self.max_bubble_width_ratio = 0.7  # 70% of available width

    def _markdown_to_html(self, text: str, color: str = "#1a1a1a") -> str:
        """Convert simple markdown to HTML for rich text rendering"""
        import re

        # Escape HTML special characters first
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        # Convert markdown to HTML
        # Bold: **text** or __text__
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)

        # Italic: *text* or _text_
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)

        # Code: `code`
        text = re.sub(r'`(.+?)`', r'<code style="background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px; font-family: Consolas, monospace;">\1</code>', text)

        # Bullet points: lines starting with • or - or *
        lines = text.split('\n')
        html_lines = []
        in_list = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('•') or stripped.startswith('- ') or (stripped.startswith('* ') and len(stripped) > 2):
                if not in_list:
                    html_lines.append('<ul style="margin: 4px 0; padding-left: 20px;">')
                    in_list = True
                content = stripped[2:].strip() if stripped.startswith('- ') or stripped.startswith('* ') else stripped[1:].strip()
                html_lines.append(f'<li>{content}</li>')
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                if stripped:
                    html_lines.append(line)
                else:
                    html_lines.append('<br/>')

        if in_list:
            html_lines.append('</ul>')

        html_text = ''.join(html_lines)

        # Wrap in styled div
        return f'<div style="color: {color}; line-height: 1.4;">{html_text}</div>'

    def sizeHint(self, option: QStyleOptionViewItem, index):
        """Calculate size needed for this message"""
        from PyQt6.QtGui import QTextDocument

        message_data = index.data(Qt.ItemDataRole.UserRole)
        if not message_data:
            return QSize(0, 0)

        role = message_data.get('role', 'system')
        message = message_data.get('content', '')

        # Calculate text width
        width = option.rect.width() if option.rect.width() > 0 else 800
        max_bubble_width = int(width * self.max_bubble_width_ratio)

        font = QFont("Segoe UI", 10 if role != "system" else 9)

        if role == "system":
            # System messages are centered and smaller (with markdown formatting)
            text_width = int(width * 0.8) - (self.bubble_padding * 2)

            # Use QTextDocument to measure height with markdown
            doc = QTextDocument()
            doc.setDefaultFont(font)
            doc.setHtml(self._markdown_to_html(message, "#5f6368"))
            doc.setTextWidth(text_width)

            text_height = doc.size().height()
            height = text_height + self.bubble_padding + self.padding
        else:
            # User/assistant messages - use QTextDocument for accurate height with markdown
            text_width = max_bubble_width - (self.bubble_padding * 2) - self.avatar_size - self.avatar_margin - self.padding

            # Create text document to measure actual rendered height
            doc = QTextDocument()
            doc.setDefaultFont(font)
            doc.setHtml(self._markdown_to_html(message, "#1a1a1a"))
            doc.setTextWidth(text_width)

            # Get actual document height
            text_height = doc.size().height()
            bubble_height = text_height + self.bubble_padding * 2
            height = bubble_height + self.padding

        return QSize(width, int(height))

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        """Paint the chat message bubble"""
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        message_data = index.data(Qt.ItemDataRole.UserRole)
        if not message_data:
            painter.restore()
            return

        role = message_data.get('role', 'system')
        message = message_data.get('content', '')

        rect = option.rect

        if role == "user":
            self._paint_user_message(painter, rect, message)
        elif role == "assistant":
            self._paint_assistant_message(painter, rect, message)
        else:  # system
            self._paint_system_message(painter, rect, message)

        painter.restore()

    def _paint_user_message(self, painter: QPainter, rect: QRect, message: str):
        """Paint user message (right-aligned, blue gradient)"""
        from PyQt6.QtGui import QTextDocument

        # Calculate dimensions
        max_bubble_width = int(rect.width() * self.max_bubble_width_ratio)

        # Calculate text size using QTextDocument for accurate height
        font = QFont("Segoe UI", 10)
        painter.setFont(font)

        text_width = max_bubble_width - (self.bubble_padding * 2) - self.avatar_size - self.avatar_margin - self.padding

        # Create text document to measure actual rendered size
        doc = QTextDocument()
        doc.setDefaultFont(font)
        doc.setHtml(self._markdown_to_html(message, "white"))
        doc.setTextWidth(text_width)

        # Get actual document size
        doc_size = doc.size()
        bubble_width = min(doc_size.width() + self.bubble_padding * 2, max_bubble_width - self.avatar_size - self.avatar_margin)
        bubble_height = doc_size.height() + self.bubble_padding * 2

        # Position bubble on right side (leaving room for avatar)
        bubble_x = rect.right() - bubble_width - self.avatar_size - self.avatar_margin - self.padding
        bubble_y = rect.top() + self.padding // 2

        # Draw bubble with gradient
        bubble_rect = QRectF(bubble_x, bubble_y, bubble_width, bubble_height)
        path = QPainterPath()
        path.addRoundedRect(bubble_rect, 18, 18)

        # Supervertaler blue gradient
        gradient = QLinearGradient(bubble_rect.topLeft(), bubble_rect.bottomRight())
        gradient.setColorAt(0, QColor("#5D7BFF"))
        gradient.setColorAt(1, QColor("#4F6FFF"))

        painter.fillPath(path, QBrush(gradient))

        # Draw shadow
        painter.setPen(QPen(QColor(93, 123, 255, 76), 0))
        painter.drawRoundedRect(bubble_rect.adjusted(0, 2, 0, 2), 18, 18)

        # Draw text with markdown formatting (reuse doc from above)
        from PyQt6.QtGui import QAbstractTextDocumentLayout
        text_draw_rect = bubble_rect.adjusted(
            self.bubble_padding, self.bubble_padding,
            -self.bubble_padding, -self.bubble_padding
        )

        # Translate painter to text position and draw
        painter.save()
        painter.translate(text_draw_rect.topLeft())
        ctx = QAbstractTextDocumentLayout.PaintContext()
        doc.documentLayout().draw(painter, ctx)
        painter.restore()

        # Draw avatar (right side)
        avatar_x = rect.right() - self.avatar_size - self.padding
        avatar_y = bubble_y
        avatar_rect = QRectF(avatar_x, avatar_y, self.avatar_size, self.avatar_size)

        # Avatar gradient background
        avatar_gradient = QLinearGradient(avatar_rect.topLeft(), avatar_rect.bottomRight())
        avatar_gradient.setColorAt(0, QColor("#667eea"))
        avatar_gradient.setColorAt(1, QColor("#764ba2"))

        painter.setBrush(QBrush(avatar_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(avatar_rect)

        # Draw avatar emoji
        painter.setPen(QPen(QColor("white")))
        painter.setFont(QFont("Segoe UI Emoji", 13))
        painter.drawText(avatar_rect, Qt.AlignmentFlag.AlignCenter, "👤")

    def _paint_assistant_message(self, painter: QPainter, rect: QRect, message: str):
        """Paint assistant message (left-aligned, gray)"""
        from PyQt6.QtGui import QTextDocument

        # Calculate dimensions
        max_bubble_width = int(rect.width() * self.max_bubble_width_ratio)

        # Calculate text size using QTextDocument for accurate height
        font = QFont("Segoe UI", 10)
        painter.setFont(font)

        text_width = max_bubble_width - (self.bubble_padding * 2) - self.avatar_size - self.avatar_margin - self.padding

        # Create text document to measure actual rendered size
        doc = QTextDocument()
        doc.setDefaultFont(font)
        doc.setHtml(self._markdown_to_html(message, "#1a1a1a"))
        doc.setTextWidth(text_width)

        # Get actual document size
        doc_size = doc.size()
        bubble_width = min(doc_size.width() + self.bubble_padding * 2, max_bubble_width - self.avatar_size - self.avatar_margin)
        bubble_height = doc_size.height() + self.bubble_padding * 2

        # Position bubble on left side (leaving room for avatar)
        bubble_x = rect.left() + self.avatar_size + self.avatar_margin + self.padding
        bubble_y = rect.top() + self.padding // 2

        # Draw bubble
        bubble_rect = QRectF(bubble_x, bubble_y, bubble_width, bubble_height)
        path = QPainterPath()
        path.addRoundedRect(bubble_rect, 18, 18)

        painter.fillPath(path, QBrush(QColor("#F5F5F7")))

        # Draw border
        painter.setPen(QPen(QColor("#E8E8EA"), 1))
        painter.drawRoundedRect(bubble_rect, 18, 18)

        # Draw shadow
        painter.setPen(QPen(QColor(0, 0, 0, 20), 0))
        painter.drawRoundedRect(bubble_rect.adjusted(0, 2, 0, 2), 18, 18)

        # Draw text with markdown formatting (reuse doc from above)
        from PyQt6.QtGui import QAbstractTextDocumentLayout
        text_draw_rect = bubble_rect.adjusted(
            self.bubble_padding, self.bubble_padding,
            -self.bubble_padding, -self.bubble_padding
        )

        # Translate painter to text position and draw
        painter.save()
        painter.translate(text_draw_rect.topLeft())
        ctx = QAbstractTextDocumentLayout.PaintContext()
        doc.documentLayout().draw(painter, ctx)
        painter.restore()

        # Draw avatar (left side)
        avatar_x = rect.left() + self.padding
        avatar_y = bubble_y
        avatar_rect = QRectF(avatar_x, avatar_y, self.avatar_size, self.avatar_size)

        # Avatar gradient background
        avatar_gradient = QLinearGradient(avatar_rect.topLeft(), avatar_rect.bottomRight())
        avatar_gradient.setColorAt(0, QColor("#667eea"))
        avatar_gradient.setColorAt(1, QColor("#764ba2"))

        painter.setBrush(QBrush(avatar_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(avatar_rect)

        # Draw avatar emoji
        painter.setPen(QPen(QColor("white")))
        painter.setFont(QFont("Segoe UI Emoji", 15))
        painter.drawText(avatar_rect, Qt.AlignmentFlag.AlignCenter, "🤖")

    def _paint_system_message(self, painter: QPainter, rect: QRect, message: str):
        """Paint system message (centered, subtle, with markdown formatting)"""
        from PyQt6.QtGui import QTextDocument, QAbstractTextDocumentLayout

        # Create text document with markdown converted to HTML
        font = QFont("Segoe UI", 9)
        doc = QTextDocument()
        doc.setDefaultFont(font)
        doc.setHtml(self._markdown_to_html(message, "#5f6368"))

        # Set max width (80% of available width)
        max_width = int(rect.width() * 0.8) - (self.bubble_padding * 2)
        doc.setTextWidth(max_width)

        # Calculate bubble dimensions
        text_height = doc.size().height()
        bubble_width = max_width + self.bubble_padding * 2
        bubble_height = text_height + self.bubble_padding

        # Center horizontally
        bubble_x = (rect.width() - bubble_width) / 2
        bubble_y = rect.top() + self.padding // 2

        # Draw bubble
        bubble_rect = QRectF(bubble_x, bubble_y, bubble_width, bubble_height)
        path = QPainterPath()
        path.addRoundedRect(bubble_rect, 16, 16)

        painter.fillPath(path, QBrush(QColor("#F8F9FA")))

        # Draw border
        painter.setPen(QPen(QColor("#E8EAED"), 1))
        painter.drawRoundedRect(bubble_rect, 16, 16)

        # Draw text with markdown formatting
        text_draw_rect = bubble_rect.adjusted(
            self.bubble_padding, self.bubble_padding // 2,
            -self.bubble_padding, -self.bubble_padding // 2
        )

        # Translate painter to text position and draw
        painter.save()
        painter.translate(text_draw_rect.topLeft())
        ctx = QAbstractTextDocumentLayout.PaintContext()
        doc.documentLayout().draw(painter, ctx)
        painter.restore()


class UnifiedPromptManagerQt:
    """
    Unified Prompt Manager - Single-tab interface with:
    - Tree view with nested folders
    - Favorites and QuickMenu
    - Multi-attach capability
    - Active prompt configuration panel
    """
    
    def __init__(self, parent_app, standalone=False):
        """
        Initialize Unified Prompt Manager
        
        Args:
            parent_app: Reference to main application (needs .user_data_path, .log() method)
            standalone: If True, running standalone. If False, embedded in Supervertaler
        """
        self.parent_app = parent_app
        self.standalone = standalone
        
        # Get user_data path
        if hasattr(parent_app, 'user_data_path'):
            self.user_data_path = Path(parent_app.user_data_path)
        else:
            self.user_data_path = Path("user_data")
        
        # Initialize logging
        self.log = parent_app.log if hasattr(parent_app, 'log') else print
        
        # Paths
        self.prompt_library_dir = self.user_data_path / "prompt_library"
        # Use prompt_library directly, not prompt_library/Library
        self.unified_library_dir = self.prompt_library_dir

        # Run migration if needed
        self._check_and_migrate()

        # Initialize unified prompt library
        self.library = UnifiedPromptLibrary(
            library_dir=str(self.unified_library_dir),
            log_callback=self.log_message
        )
        
        # Load prompts
        self.library.load_all_prompts()
        
        # System Prompts (stored separately, loaded from settings/files)
        self.system_templates = {}
        self.current_mode = "single"  # single, batch_docx, batch_bilingual
        self._load_system_templates()
        
        # UI will be created by create_tab()
        self.main_widget = None
        self.tree_widget = None
        self.editor_content = None
        self.active_config_widget = None
        
        # AI Assistant state
        self.llm_client: Optional[LLMClient] = None
        self.attached_files: List[Dict] = []  # List of {path, name, content, type} - DEPRECATED, use attachment_manager
        self.chat_history: List[Dict] = []  # List of {role, content, timestamp}
        self.ai_conversation_file = self.user_data_path / "ai_assistant" / "conversation.json"
        self._cached_document_markdown: Optional[str] = None  # Cached markdown conversion of current document

        # Initialize Attachment Manager
        ai_assistant_dir = self.user_data_path / "ai_assistant"
        self.attachment_manager = AttachmentManager(
            base_dir=str(ai_assistant_dir),
            log_callback=self.log_message
        )
        # Set initial session based on current date/time
        session_id = datetime.now().strftime("%Y%m%d")
        self.attachment_manager.set_session(session_id)

        # Initialize AI Action System (Phase 2)
        self.ai_action_system = AIActionSystem(
            prompt_library=self.library,
            parent_app=self.parent_app,
            log_callback=self.log_message
        )

        self._init_llm_client()
        self._load_conversation_history()
        self._load_persisted_attachments()
    
    def _check_and_migrate(self):
        """Check if migration is needed and perform it"""
        try:
            needs_migration = migrate_prompt_library(
                str(self.prompt_library_dir),
                log_callback=self.log_message
            )
            
            if needs_migration:
                self.log_message("✓ Prompt library migration completed successfully")
            
        except Exception as e:
            self.log_message(f"⚠ Migration check failed: {e}")
    
    def log_message(self, message):
        """Log a message through parent app or print"""
        self.log(message)
    
    def create_tab(self, parent_widget):
        """
        Create the Prompt Manager tab UI with sub-tabs
        
        Args:
            parent_widget: Widget to add the tab to (will set its layout)
        """
        main_layout = QVBoxLayout(parent_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # Main header for Prompt Manager
        header = self._create_main_header()
        main_layout.addWidget(header, 0)
        
        # Sub-tabs: Prompt Library and AI Assistant
        self.sub_tabs = QTabWidget()
        self.sub_tabs.tabBar().setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sub_tabs.tabBar().setDrawBase(False)
        self.sub_tabs.setStyleSheet("QTabBar::tab { outline: 0; } QTabBar::tab:focus { outline: none; } QTabBar::tab:selected { border-bottom: 1px solid #2196F3; background-color: rgba(33, 150, 243, 0.08); }")

        # Tab 1: Prompt Library
        library_tab = self._create_prompt_library_tab()
        self.sub_tabs.addTab(library_tab, "📚 Library")

        # Tab 2: AI Assistant (placeholder for now)
        assistant_tab = self._create_ai_assistant_tab()
        self.sub_tabs.addTab(assistant_tab, "✨ AI Assistant")

        # Tab 3: Placeholders Reference
        placeholders_tab = self._create_placeholders_tab()
        self.sub_tabs.addTab(placeholders_tab, "📝 Placeholders")

        # Connect tab change signal to update context
        self.sub_tabs.currentChanged.connect(self._on_tab_changed)

        main_layout.addWidget(self.sub_tabs, 1)  # 1 = stretch

    def _on_tab_changed(self, index):
        """Handle tab change - update context when switching to AI Assistant"""
        if index == 1:  # AI Assistant tab
            self._update_context_sidebar()

    def refresh_context(self):
        """
        Public method to refresh AI Assistant context.
        Call this from the main app when document/project changes.
        """
        # Reload cached document markdown from disk
        if hasattr(self.parent_app, 'current_document_path') and self.parent_app.current_document_path:
            doc_path = Path(self.parent_app.current_document_path)
            # Try to load existing markdown
            markdown_dir = self.user_data_path / "ai_assistant" / "current_document"
            markdown_file = markdown_dir / f"{doc_path.stem}.md"
            if markdown_file.exists():
                try:
                    with open(markdown_file, 'r', encoding='utf-8') as f:
                        self._cached_document_markdown = f.read()
                    self.log_message(f"✓ Loaded cached markdown: {markdown_file.name}")
                except Exception as e:
                    self.log_message(f"⚠ Failed to load cached markdown: {e}")
                    self._cached_document_markdown = None
            else:
                self._cached_document_markdown = None
        else:
            self._cached_document_markdown = None

        self._update_context_sidebar()
    
    def _create_main_header(self) -> QWidget:
        """Create main Prompt Manager header"""
        header_container = QWidget()
        layout = QVBoxLayout(header_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Title
        title = QLabel("⚡ QuickMenu")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
        layout.addWidget(title, 0)
        
        # Description
        desc = QLabel(
            "Manage AI instructions and get AI assistance for your translation projects.\n"
            "Create custom prompts, organize them in folders, and use AI to analyze documents."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
        layout.addWidget(desc, 0)
        
        return header_container
    
    def _create_prompt_library_tab(self) -> QWidget:
        """Create the Prompt Library sub-tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 5, 0, 0)
        layout.setSpacing(5)
        
        # Main content: Horizontal splitter (left: config+buttons+tree | right: editor)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setHandleWidth(3)
        
        # Left panel container (not a splitter - fixed layout)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)
        
        # Active Configuration Panel (top of left)
        config_group = self._create_active_config_panel()
        config_group.setMinimumHeight(150)
        left_layout.addWidget(config_group)
        
        # Library Action Buttons (below Active Config, above tree)
        library_buttons = self._create_library_buttons()
        left_layout.addWidget(library_buttons)
        
        # Prompt Library Tree (bottom of left)
        tree_panel = self._create_library_tree_panel()
        tree_panel.setMinimumHeight(200)
        left_layout.addWidget(tree_panel, 1)  # stretch factor 1 - tree expands
        
        left_panel.setMinimumWidth(300)
        main_splitter.addWidget(left_panel)
        
        # Right: Editor only
        editor_group = self._create_editor_panel()
        editor_group.setMinimumWidth(400)
        editor_group.setMinimumHeight(300)
        main_splitter.addWidget(editor_group)
        
        # Set main splitter proportions (40% left, 60% editor)
        main_splitter.setSizes([400, 600])
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)
        
        layout.addWidget(main_splitter, 1)
        
        # Load initial tree content
        self._refresh_tree()
        
        return tab
    
    def _create_library_buttons(self) -> QWidget:
        """Create action buttons for Prompt Library (between Active Config and tree)"""
        container = QWidget()
        btn_layout = QHBoxLayout(container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(5)
        
        btn_new = QPushButton("+ New")
        btn_new.clicked.connect(self._new_prompt)
        btn_layout.addWidget(btn_new)
        
        btn_folder = QPushButton("📁 New Folder")
        btn_folder.clicked.connect(self._new_folder)
        btn_layout.addWidget(btn_folder)
        
        btn_settings = QPushButton("⚙️ System Prompts")
        btn_settings.clicked.connect(self._open_system_prompts_settings)
        btn_settings.setToolTip("Configure mode-specific system prompts (Settings)")
        btn_layout.addWidget(btn_settings)
        
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.clicked.connect(self._refresh_library)
        btn_layout.addWidget(btn_refresh)

        btn_collapse_all = QPushButton("▸ Collapse all")
        btn_collapse_all.setToolTip("Collapse all folders in the Prompt Library tree")
        btn_collapse_all.clicked.connect(self._collapse_prompt_library_tree)
        btn_layout.addWidget(btn_collapse_all)

        btn_expand_all = QPushButton("▾ Expand all")
        btn_expand_all.setToolTip("Expand all folders in the Prompt Library tree")
        btn_expand_all.clicked.connect(self._expand_prompt_library_tree)
        btn_layout.addWidget(btn_expand_all)
        
        btn_layout.addStretch()
        
        return container
    
    def _create_ai_assistant_tab(self) -> QWidget:
        """Create the AI Assistant sub-tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Quick Action Button at top
        # Note: && is needed to display a single & (Qt uses & for keyboard shortcuts)
        action_btn = QPushButton("🔍 Analyze Project && Generate Prompts")
        action_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                font-size: 11pt;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        action_btn.clicked.connect(self._analyze_and_generate)
        layout.addWidget(action_btn, 0)
        
        # Main content: Horizontal splitter (context sidebar | chat area)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setHandleWidth(3)
        
        # Left: Context Sidebar
        context_panel = self._create_context_sidebar()
        context_panel.setMinimumWidth(200)
        context_panel.setMaximumWidth(350)
        main_splitter.addWidget(context_panel)
        
        # Right: Chat Interface
        chat_panel = self._create_chat_interface()
        main_splitter.addWidget(chat_panel)
        
        # Set splitter proportions (25% context, 75% chat)
        main_splitter.setSizes([250, 750])
        main_splitter.setStretchFactor(0, 0)  # Context sidebar fixed-ish
        main_splitter.setStretchFactor(1, 1)  # Chat area expands
        
        layout.addWidget(main_splitter, 1)
        
        return tab
    
    def _create_placeholders_tab(self) -> QWidget:
        """Create the Placeholders Reference sub-tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Header (matches standard tool style: Superbench, AutoFingers, TMX Editor)
        header = QLabel("📝 Available Placeholders")
        header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
        layout.addWidget(header, 0)
        
        # Description box (matches standard tool style)
        description = QLabel(
            "Use these placeholders in your prompts. They will be replaced with actual values when the prompt runs."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
        layout.addWidget(description, 0)
        
        # Horizontal splitter for table and tips
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(3)
        
        # Left: Table with placeholders
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Placeholder", "Description", "Example"])
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        
        # Placeholder data
        placeholders = [
            (
                "{{SELECTION}}",
                "Currently selected text in the grid (source or target cell)",
                "If you select 'translation memory' in the grid, this will contain that text"
            ),
            (
                "{{SOURCE_TEXT}}",
                "Full text of the current source segment",
                "The complete source sentence/paragraph from the active segment"
            ),
            (
                "{{SOURCE_LANGUAGE}}",
                "Project's source language",
                "Dutch, English, German, French, etc."
            ),
            (
                "{{TARGET_LANGUAGE}}",
                "Project's target language",
                "English, Spanish, Portuguese, etc."
            ),
            (
                "{{SOURCE+TARGET_CONTEXT}}",
                "Project segments with BOTH source and target text. Use for proofreading prompts.",
                "[1] Source text\\n    → Target text\\n\\n[2] Source text\\n    → Target text\\n\\n..."
            ),
            (
                "{{SOURCE_CONTEXT}}",
                "Project segments with SOURCE ONLY. Use for translation/terminology questions.",
                "[1] Source text\\n\\n[2] Source text\\n\\n[3] Source text\\n\\n..."
            ),
            (
                "{{TARGET_CONTEXT}}",
                "Project segments with TARGET ONLY. Use for consistency/style analysis.",
                "[1] Target text\\n\\n[2] Target text\\n\\n[3] Target text\\n\\n..."
            )
        ]
        
        table.setRowCount(len(placeholders))
        for row, (placeholder, description, example) in enumerate(placeholders):
            # Placeholder column (monospace, bold)
            item_placeholder = QTableWidgetItem(placeholder)
            item_placeholder.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
            table.setItem(row, 0, item_placeholder)
            
            # Description column
            item_desc = QTableWidgetItem(description)
            item_desc.setToolTip(description)
            table.setItem(row, 1, item_desc)
            
            # Example column (monospace, italic)
            item_example = QTableWidgetItem(example)
            item_example.setFont(QFont("Courier New", 9))
            item_example.setToolTip(example)
            table.setItem(row, 2, item_example)
        
        # Set column widths
        table.setColumnWidth(0, 200)
        table.setColumnWidth(1, 300)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # Adjust row heights for readability
        for row in range(table.rowCount()):
            table.setRowHeight(row, 60)
        
        splitter.addWidget(table)
        
        # Right: Usage tips panel
        tips_panel = QWidget()
        tips_layout = QVBoxLayout(tips_panel)
        tips_layout.setContentsMargins(10, 0, 0, 0)
        
        tips_header = QLabel("💡 Usage Tips")
        tips_header.setStyleSheet("font-weight: bold; font-size: 11pt; color: #2196F3; margin-bottom: 8px;")
        tips_layout.addWidget(tips_header)
        
        tips_intro = QLabel(
            "Use these placeholders in your prompts. They will be replaced with actual values when the prompt runs."
        )
        tips_intro.setWordWrap(True)
        tips_intro.setStyleSheet("color: #666; margin-bottom: 15px; font-style: italic;")
        tips_layout.addWidget(tips_intro)
        
        tips_text = QLabel(
            "• Placeholders are case-sensitive (use UPPERCASE)\n\n"
            "• Surround placeholders with double curly braces: {{ }}\n\n"
            "• You can combine multiple placeholders in one prompt\n\n"
            "• Use {{DOCUMENT_CONTEXT}} for context-aware translations\n\n"
            "• Configure {{DOCUMENT_CONTEXT}} percentage in Settings → AI Settings"
        )
        tips_text.setWordWrap(True)
        tips_text.setStyleSheet("color: #666; line-height: 1.6;")
        tips_layout.addWidget(tips_text)
        
        tips_layout.addStretch()
        
        tips_panel.setMinimumWidth(280)
        tips_panel.setMaximumWidth(400)
        splitter.addWidget(tips_panel)
        
        # Set splitter proportions (75% table, 25% tips)
        splitter.setSizes([750, 250])
        splitter.setStretchFactor(0, 1)  # Table expands
        splitter.setStretchFactor(1, 0)  # Tips panel fixed-ish
        
        layout.addWidget(splitter, 1)  # 1 = stretch to fill all available space
        
        return tab
    
    def _create_context_sidebar(self) -> QWidget:
        """Create context sidebar showing available resources"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Title
        title = QLabel("📋 Available Context")
        title.setStyleSheet("font-weight: bold; font-size: 10pt; color: #1976D2;")
        layout.addWidget(title)
        
        # Scroll area for context items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)
        
        # Current Project Document
        self.context_current_doc = self._create_context_section(
            "📄 Current Document",
            "No document loaded"
        )
        content_layout.addWidget(self.context_current_doc)
        
        # Attached Files (expandable section)
        self.context_attached_files_frame = self._create_attached_files_section()
        content_layout.addWidget(self.context_attached_files_frame)
        
        # Prompts from Library
        prompt_count = len(self.library.prompts)
        self.context_prompts = self._create_context_section(
            f"💡 Prompt Library ({prompt_count})",
            f"{prompt_count} prompts available\nClick to select specific prompts"
        )
        self.context_prompts.setCursor(Qt.CursorShape.PointingHandCursor)
        content_layout.addWidget(self.context_prompts)
        
        # Translation Memories
        self.context_tms = self._create_context_section(
            "💾 Translation Memories",
            "Click to include TM data"
        )
        self.context_tms.setCursor(Qt.CursorShape.PointingHandCursor)
        content_layout.addWidget(self.context_tms)
        
        # Termbases
        self.context_termbases = self._create_context_section(
            "📚 Termbases",
            "Click to include termbase data"
        )
        self.context_termbases.setCursor(Qt.CursorShape.PointingHandCursor)
        content_layout.addWidget(self.context_termbases)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)
        
        return panel
    
    def _create_context_section(self, title: str, description: str) -> QFrame:
        """Create a context section widget"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                padding: 8px;
            }
            QFrame:hover {
                background-color: #EEEEEE;
                border: 1px solid #BDBDBD;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 9pt;")
        layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #666; font-size: 8pt;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        return frame

    def _create_attached_files_section(self) -> QFrame:
        """Create expandable attached files section with view/remove buttons"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                padding: 8px;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Header with expand/collapse button
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)

        self.attached_files_expand_btn = QPushButton("▼")
        self.attached_files_expand_btn.setFixedSize(20, 20)
        self.attached_files_expand_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        self.attached_files_expand_btn.clicked.connect(self._toggle_attached_files)
        header_layout.addWidget(self.attached_files_expand_btn)

        self.attached_files_title = QLabel("📎 Attached Files (0)")
        self.attached_files_title.setStyleSheet("font-weight: bold; font-size: 9pt;")
        header_layout.addWidget(self.attached_files_title, 1)

        # Attach button
        attach_btn = QPushButton("+")
        attach_btn.setFixedSize(20, 20)
        attach_btn.setToolTip("Attach file")
        attach_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        attach_btn.clicked.connect(self._attach_file)
        header_layout.addWidget(attach_btn)

        layout.addLayout(header_layout)

        # File list container (collapsible)
        self.attached_files_container = QWidget()
        self.attached_files_list_layout = QVBoxLayout(self.attached_files_container)
        self.attached_files_list_layout.setContentsMargins(5, 5, 5, 5)
        self.attached_files_list_layout.setSpacing(5)

        # Initially empty
        no_files_label = QLabel("No files attached")
        no_files_label.setStyleSheet("color: #999; font-size: 8pt; font-style: italic;")
        self.attached_files_list_layout.addWidget(no_files_label)

        layout.addWidget(self.attached_files_container)

        # Initially expanded
        self.attached_files_expanded = True

        return frame

    def _toggle_attached_files(self):
        """Toggle attached files section expansion"""
        self.attached_files_expanded = not self.attached_files_expanded
        self.attached_files_container.setVisible(self.attached_files_expanded)
        self.attached_files_expand_btn.setText("▼" if self.attached_files_expanded else "▶")

    def _refresh_attached_files_list(self):
        """Refresh the attached files list display"""
        # Clear current list
        while self.attached_files_list_layout.count():
            item = self.attached_files_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Update title count
        count = len(self.attached_files)
        self.attached_files_title.setText(f"📎 Attached Files ({count})")

        # If no files, show placeholder
        if count == 0:
            no_files_label = QLabel("No files attached")
            no_files_label.setStyleSheet("color: #999; font-size: 8pt; font-style: italic;")
            self.attached_files_list_layout.addWidget(no_files_label)
            return

        # Add each file
        for file_data in self.attached_files:
            file_widget = self._create_file_item_widget(file_data)
            self.attached_files_list_layout.addWidget(file_widget)

    def _create_file_item_widget(self, file_data: dict) -> QFrame:
        """Create widget for a single attached file"""
        item_frame = QFrame()
        item_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 3px;
                padding: 4px;
            }
            QFrame:hover {
                border: 1px solid #1976D2;
            }
        """)

        layout = QVBoxLayout(item_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)

        # Filename
        name_label = QLabel(file_data.get('name', 'Unknown'))
        name_label.setStyleSheet("font-weight: bold; font-size: 8pt;")
        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        # Size and type
        size = file_data.get('size', 0)
        size_kb = size / 1024 if size > 0 else 0
        file_type = file_data.get('type', '')
        info_label = QLabel(f"{file_type} • {size_kb:.1f} KB")
        info_label.setStyleSheet("color: #666; font-size: 7pt;")
        layout.addWidget(info_label)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(3)

        view_btn = QPushButton("👁 View")
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 2px;
                padding: 2px 6px;
                font-size: 7pt;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        view_btn.clicked.connect(lambda: self._view_file(file_data))
        btn_layout.addWidget(view_btn)

        remove_btn = QPushButton("❌")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                border-radius: 2px;
                padding: 2px 6px;
                font-size: 7pt;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        remove_btn.clicked.connect(lambda: self._remove_file(file_data))
        btn_layout.addWidget(remove_btn)

        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        return item_frame

    def _view_file(self, file_data: dict):
        """View an attached file"""
        try:
            file_id = file_data.get('file_id')
            if file_id:
                # Load from AttachmentManager
                full_data = self.attachment_manager.get_file(file_id)
                if full_data:
                    dialog = FileViewerDialog(full_data, self.main_widget)
                    dialog.exec()
                else:
                    QMessageBox.warning(
                        self.main_widget,
                        "File Not Found",
                        "File data not found in storage."
                    )
            else:
                # Fallback: use in-memory data
                dialog = FileViewerDialog(file_data, self.main_widget)
                dialog.exec()
        except Exception as e:
            QMessageBox.warning(
                self.main_widget,
                "View Error",
                f"Failed to view file:\n{e}"
            )

    def _remove_file(self, file_data: dict):
        """Remove an attached file"""
        try:
            filename = file_data.get('name', 'Unknown')

            # Confirm removal
            dialog = FileRemoveConfirmDialog(filename, self.main_widget)
            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            file_id = file_data.get('file_id')

            # Remove from AttachmentManager
            if file_id:
                self.attachment_manager.remove_file(file_id)

            # Remove from in-memory list
            if file_data in self.attached_files:
                self.attached_files.remove(file_data)

            # Update UI
            self._refresh_attached_files_list()
            self._save_conversation_history()

            # Add system message
            self._add_chat_message(
                "system",
                f"🗑️ Removed file: **{filename}**"
            )

        except Exception as e:
            QMessageBox.warning(
                self.main_widget,
                "Remove Error",
                f"Failed to remove file:\n{e}"
            )

    def _create_chat_interface(self) -> QWidget:
        """Create chat interface with messages and input"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Chat messages area (using QListWidget with custom delegate)
        self.chat_display = QListWidget()
        self.chat_display.setItemDelegate(ChatMessageDelegate())
        self.chat_display.setStyleSheet("""
            QListWidget {
                background-color: #FFFFFF;
                border: 1px solid #E8E8EA;
                border-radius: 8px;
                font-size: 10pt;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            QListWidget::item {
                border: none;
                background: transparent;
            }
            QListWidget::item:selected {
                background: transparent;
            }
            QListWidget::item:hover {
                background: transparent;
            }
        """)
        self.chat_display.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.chat_display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.chat_display.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chat_display.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.chat_display.setSpacing(0)
        # Enable context menu for copying messages
        self.chat_display.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.chat_display.customContextMenuRequested.connect(self._show_chat_context_menu)
        layout.addWidget(self.chat_display, 1)
        
        # Top toolbar with Clear button
        toolbar_frame = QFrame()
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(0, 0, 0, 5)
        toolbar_layout.setSpacing(5)
        
        clear_btn = QPushButton("🗑️ Clear Chat")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                border: none;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        """)
        clear_btn.clicked.connect(self._clear_chat)
        toolbar_layout.addWidget(clear_btn)
        toolbar_layout.addStretch()
        
        layout.addWidget(toolbar_frame, 0)
        
        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(5, 5, 5, 5)
        input_layout.setSpacing(5)
        
        self.chat_input = QPlainTextEdit()
        self.chat_input.setPlaceholderText("Type your message here... (Shift+Enter for new line)")
        self.chat_input.setMaximumHeight(80)
        self.chat_input.setStyleSheet("""
            QPlainTextEdit {
                border: none;
                font-size: 10pt;
                color: #1a1a1a;
                background-color: white;
                padding: 4px;
            }
        """)
        input_layout.addWidget(self.chat_input, 1)
        
        send_btn = QPushButton("Send")
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        send_btn.clicked.connect(self._send_chat_message)
        input_layout.addWidget(send_btn)
        
        layout.addWidget(input_frame, 0)
        
        return panel

    def _create_header(self) -> QWidget:
        """Create header - matches TMX Editor style exactly"""
        header_container = QWidget()
        layout = QVBoxLayout(header_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Reduced from 10 to 5 for tighter spacing
        
        # Header (matches TMX Editor style)
        title = QLabel("📚 Prompt Library")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
        layout.addWidget(title, 0)  # 0 = no stretch, stays compact
        
        # Description box (matches TMX Editor style)
        desc_text = QLabel(
            f"Custom instructions for AI translation.\n"
            f"• Mode: {self._get_mode_display_name()}"
        )
        desc_text.setWordWrap(True)
        desc_text.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
        layout.addWidget(desc_text, 0)  # 0 = no stretch, stays compact
        self.mode_label = desc_text  # Store reference for updates
        
        # Toolbar buttons row
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 5, 0, 0)
        toolbar_layout.setSpacing(5)
        
        btn_new = QPushButton("+ New")
        btn_new.clicked.connect(self._new_prompt)
        toolbar_layout.addWidget(btn_new)
        
        btn_folder = QPushButton("📁 New Folder")
        btn_folder.clicked.connect(self._new_folder)
        toolbar_layout.addWidget(btn_folder)
        
        btn_settings = QPushButton("⚙️ System Prompts")
        btn_settings.clicked.connect(self._open_system_prompts_settings)
        btn_settings.setToolTip("Configure mode-specific system prompts (Settings)")
        toolbar_layout.addWidget(btn_settings)
        
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.clicked.connect(self._refresh_library)
        toolbar_layout.addWidget(btn_refresh)

        btn_collapse_all = QPushButton("▸ Collapse all")
        btn_collapse_all.setToolTip("Collapse all folders in the Prompt Library tree")
        btn_collapse_all.clicked.connect(self._collapse_prompt_library_tree)
        toolbar_layout.addWidget(btn_collapse_all)

        btn_expand_all = QPushButton("▾ Expand all")
        btn_expand_all.setToolTip("Expand all folders in the Prompt Library tree")
        btn_expand_all.clicked.connect(self._expand_prompt_library_tree)
        toolbar_layout.addWidget(btn_expand_all)
        
        toolbar_layout.addStretch()
        
        layout.addWidget(toolbar, 0)
        
        return header_container
    
    def _create_library_tree_panel(self) -> QWidget:
        """Create left panel with folder tree"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tree widget
        self.tree_widget = PromptLibraryTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Prompt Library"])
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.itemClicked.connect(self._on_tree_item_clicked)
        self.tree_widget.itemDoubleClicked.connect(self._on_tree_item_double_clicked)
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self._show_tree_context_menu)
        
        layout.addWidget(self.tree_widget)
        
        return panel
    
    def _create_active_config_panel(self) -> QGroupBox:
        """Create active prompt configuration panel"""
        group = QGroupBox("Active Prompt")
        layout = QVBoxLayout()
        
        # Mode info (read-only, auto-selected)
        mode_frame = QFrame()
        mode_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        mode_layout = QHBoxLayout(mode_frame)
        mode_layout.setContentsMargins(10, 5, 10, 5)
        
        mode_label = QLabel(f"🔧 Current Mode: {self._get_mode_display_name()}")
        mode_label.setFont(QFont("Segoe UI", 9))
        mode_layout.addWidget(mode_label)
        
        btn_view_template = QPushButton("View System Prompt")
        btn_view_template.clicked.connect(self._view_current_system_template)
        btn_view_template.setMaximumWidth(150)
        mode_layout.addWidget(btn_view_template)
        
        layout.addWidget(mode_frame)
        
        # Primary Prompt
        primary_layout = QHBoxLayout()
        primary_label = QLabel("Primary Prompt ⭐:")
        primary_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        primary_layout.addWidget(primary_label)
        
        self.primary_prompt_label = QLabel("[None selected]")
        self.primary_prompt_label.setStyleSheet("color: #999;")
        primary_layout.addWidget(self.primary_prompt_label, 1)
        
        btn_load_external = QPushButton("Load External...")
        btn_load_external.clicked.connect(self._load_external_primary_prompt)
        btn_load_external.setToolTip("Load a prompt file from anywhere on your computer")
        btn_load_external.setMaximumWidth(100)
        primary_layout.addWidget(btn_load_external)
        
        btn_clear_primary = QPushButton("Clear")
        btn_clear_primary.clicked.connect(self._clear_primary_prompt)
        btn_clear_primary.setMaximumWidth(60)
        primary_layout.addWidget(btn_clear_primary)
        
        layout.addLayout(primary_layout)
        
        # Attached Prompts
        attached_label = QLabel("Attached Prompts 📎:")
        attached_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(attached_label)
        
        # Scrollable list of attached prompts
        self.attached_list_widget = QTreeWidget()
        self.attached_list_widget.setHeaderLabels(["Name", ""])
        self.attached_list_widget.setMaximumHeight(100)
        self.attached_list_widget.setRootIsDecorated(False)
        self.attached_list_widget.setColumnWidth(0, 200)
        layout.addWidget(self.attached_list_widget)
        
        # Image Context (visual context for AI)
        image_layout = QHBoxLayout()
        image_label = QLabel("Image Context 🖼️:")
        image_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        image_layout.addWidget(image_label)
        
        self.image_context_label = QLabel("[None loaded]")
        self.image_context_label.setStyleSheet("color: #999;")
        self.image_context_label.setToolTip(
            "Images loaded via Project Resources → Image Context tab\n"
            "are sent as binary data alongside your prompt when\n"
            "figure references (Fig. 1, Figure 2A, etc.) are detected."
        )
        image_layout.addWidget(self.image_context_label, 1)
        
        layout.addLayout(image_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        btn_preview = QPushButton("Preview Combined")
        btn_preview.setToolTip("Preview the complete assembled prompt that will be sent to the AI\n(System Prompt + Project Instructions + Custom Prompts + your text)")
        btn_preview.clicked.connect(self._preview_combined_prompt)
        btn_layout.addWidget(btn_preview)
        
        btn_clear_all = QPushButton("Clear All Attachments")
        btn_clear_all.clicked.connect(self._clear_all_attachments)
        btn_layout.addWidget(btn_clear_all)
        
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        group.setMaximumHeight(280)
        
        return group
    
    def _create_editor_panel(self) -> QGroupBox:
        """Create prompt editor panel"""
        group = QGroupBox("Prompt Editor")
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.editor_name_label = QLabel("Select a prompt to edit")
        self.editor_name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        toolbar.addWidget(self.editor_name_label)
        
        toolbar.addStretch()
        
        self.btn_save_prompt = QPushButton("💾 Save")
        self.btn_save_prompt.clicked.connect(self._save_current_prompt)
        self.btn_save_prompt.setEnabled(False)
        toolbar.addWidget(self.btn_save_prompt)
        
        layout.addLayout(toolbar)
        
        # External file path display (hidden by default)
        self.external_path_frame = QFrame()
        external_path_layout = QHBoxLayout(self.external_path_frame)
        external_path_layout.setContentsMargins(0, 0, 0, 4)
        external_path_layout.addWidget(QLabel("📂 Location:"))
        self.external_path_label = QLabel()
        self.external_path_label.setStyleSheet("color: #0066cc; text-decoration: underline;")
        self.external_path_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.external_path_label.setToolTip("Click to open containing folder")
        self.external_path_label.mousePressEvent = self._open_external_prompt_folder
        external_path_layout.addWidget(self.external_path_label, 1)
        self.btn_open_folder = QPushButton("📁 Open Folder")
        self.btn_open_folder.setMaximumWidth(100)
        self.btn_open_folder.clicked.connect(lambda: self._open_external_prompt_folder(None))
        external_path_layout.addWidget(self.btn_open_folder)
        self.external_path_frame.setVisible(False)
        layout.addWidget(self.external_path_frame)
        
        # Metadata fields
        metadata_layout = QHBoxLayout()
        
        # Name
        metadata_layout.addWidget(QLabel("Name:"))
        self.editor_name_input = QLineEdit()
        self.editor_name_input.setPlaceholderText("Prompt name")
        metadata_layout.addWidget(self.editor_name_input, 2)
        
        # Description
        metadata_layout.addWidget(QLabel("Description:"))
        self.editor_desc_input = QLineEdit()
        self.editor_desc_input.setPlaceholderText("Brief description")
        metadata_layout.addWidget(self.editor_desc_input, 3)
        
        layout.addLayout(metadata_layout)

        # QuickMenu fields
        quickmenu_layout = QHBoxLayout()

        quickmenu_layout.addWidget(QLabel("QuickMenu label:"))
        self.editor_quickmenu_label_input = QLineEdit()
        self.editor_quickmenu_label_input.setPlaceholderText("Label shown in QuickMenu")
        quickmenu_layout.addWidget(self.editor_quickmenu_label_input, 2)

        self.editor_quickmenu_in_grid_cb = CheckmarkCheckBox("Show in QuickMenu (in-app)")
        quickmenu_layout.addWidget(self.editor_quickmenu_in_grid_cb, 2)

        self.editor_quickmenu_in_quickmenu_cb = CheckmarkCheckBox("Show in QuickMenu (global)")
        quickmenu_layout.addWidget(self.editor_quickmenu_in_quickmenu_cb, 1)

        layout.addLayout(quickmenu_layout)
        
        # Content editor
        self.editor_content = QPlainTextEdit()
        self.editor_content.setPlaceholderText("Enter prompt content here...")
        self.editor_content.setFont(QFont("Consolas", 10))
        layout.addWidget(self.editor_content)
        
        group.setLayout(layout)
        
        return group
    
    def _get_mode_display_name(self) -> str:
        """Get display name for current mode"""
        mode_names = {
            "single": "Single Segment",
            "batch_docx": "Batch DOCX",
            "batch_bilingual": "Batch Bilingual"
        }
        return mode_names.get(self.current_mode, "Single Segment")
    
    def _refresh_tree(self):
        """Refresh the library tree view"""
        tree_state = self._capture_prompt_tree_state()
        self.tree_widget.clear()
        
        # Debug: Show what we have
        self.log_message(f"🔍 DEBUG: Refreshing tree with {len(self.library.prompts)} prompts")
        self.log_message(f"🔍 DEBUG: Library dir: {self.unified_library_dir}")
        self.log_message(f"🔍 DEBUG: Library dir exists: {self.unified_library_dir.exists()}")
        
        # Favorites section
        favorites_root = QTreeWidgetItem(["⭐ Favorites"])
        # Special node: not draggable/droppable
        favorites_root.setData(0, Qt.ItemDataRole.UserRole, {'type': 'special', 'kind': 'favorites'})
        favorites_root.setExpanded(False)
        font = favorites_root.font(0)
        font.setBold(True)
        favorites_root.setFont(0, font)
        self.tree_widget.addTopLevelItem(favorites_root)
        
        favorites = self.library.get_favorites()
        self.log_message(f"🔍 DEBUG: Favorites count: {len(favorites)}")
        for path, name in favorites:
            item = QTreeWidgetItem([name])
            item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'prompt', 'path': path})
            # Favorites are shortcuts, but allow dragging to move the actual prompt file.
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsDragEnabled)
            favorites_root.addChild(item)
        
        # Library folders (QuickMenu parent folder removed - folder hierarchy now defines menu structure)
        self.log_message(f"🔍 DEBUG: Building tree from {self.unified_library_dir}")
        self._build_tree_recursive(None, self.unified_library_dir, "")
        
        # Debug: Check what's in the tree
        self.log_message(f"🔍 DEBUG: Tree has {self.tree_widget.topLevelItemCount()} top-level items")
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            text = item.text(0)
            child_count = item.childCount()
            self.log_message(f"🔍 DEBUG: Top-level item {i}: '{text}' with {child_count} children")
        
        # Preserve user's expansion state across refreshes.
        if tree_state is None and not getattr(self, "_prompt_tree_state_initialized", False):
            # First-ever refresh: default to collapsed ("popped in").
            self.tree_widget.collapseAll()
            self._prompt_tree_state_initialized = True
        else:
            self._restore_prompt_tree_state(tree_state)

        self.log_message("🔍 DEBUG: Tree refresh complete")

    def _capture_prompt_tree_state(self) -> Optional[Dict[str, object]]:
        """Capture expansion + selection state for the Prompt Library tree."""
        if not hasattr(self, 'tree_widget') or not self.tree_widget:
            return None

        try:
            expanded_folders = set()
            expanded_special = {}

            current = self.tree_widget.currentItem()
            current_sel = None
            if current is not None:
                data = current.data(0, Qt.ItemDataRole.UserRole)
                if data and data.get('type') in {'prompt', 'folder'}:
                    current_sel = (data.get('type'), data.get('path'))

            # Scroll position (best-effort)
            scroll_val = None
            try:
                sb = self.tree_widget.verticalScrollBar()
                scroll_val = sb.value() if sb is not None else None
            except Exception:
                scroll_val = None

            def iter_items(parent: QTreeWidgetItem):
                for i in range(parent.childCount()):
                    child = parent.child(i)
                    yield child
                    yield from iter_items(child)

            root = self.tree_widget.invisibleRootItem()
            for item in iter_items(root):
                data = item.data(0, Qt.ItemDataRole.UserRole)
                if not data:
                    continue

                if data.get('type') == 'folder' and item.isExpanded():
                    path = data.get('path')
                    if path:
                        expanded_folders.add(path)

                if data.get('type') == 'special':
                    kind = data.get('kind')
                    if kind:
                        expanded_special[kind] = item.isExpanded()

            return {
                'expanded_folders': expanded_folders,
                'expanded_special': expanded_special,
                'current_sel': current_sel,
                'scroll_val': scroll_val,
            }
        except Exception:
            return None

    def _restore_prompt_tree_state(self, state: Optional[Dict[str, object]]):
        """Restore expansion + selection state for the Prompt Library tree."""
        if not state or not hasattr(self, 'tree_widget') or not self.tree_widget:
            return

        expanded_folders = state.get('expanded_folders', set()) or set()
        expanded_special = state.get('expanded_special', {}) or {}
        current_sel = state.get('current_sel')
        scroll_val = state.get('scroll_val')

        def iter_items(parent: QTreeWidgetItem):
            for i in range(parent.childCount()):
                child = parent.child(i)
                yield child
                yield from iter_items(child)

        # Restore expansions
        root = self.tree_widget.invisibleRootItem()
        for item in iter_items(root):
            data = item.data(0, Qt.ItemDataRole.UserRole)
            if not data:
                continue

            if data.get('type') == 'folder':
                p = data.get('path')
                if p in expanded_folders:
                    item.setExpanded(True)

            if data.get('type') == 'special':
                kind = data.get('kind')
                if kind in expanded_special:
                    item.setExpanded(bool(expanded_special[kind]))

        # Restore selection (prefer the main library tree item over Favorites/Quick Run shortcuts)
        if current_sel and len(current_sel) == 2:
            sel_type, sel_path = current_sel
            if sel_type == 'prompt' and sel_path:
                self._select_and_reveal_prompt(sel_path, prefer_library_tree=True)
            elif sel_type == 'folder' and sel_path:
                self._select_and_reveal_folder(sel_path)

        # Restore scroll position (best-effort)
        if scroll_val is not None:
            try:
                sb = self.tree_widget.verticalScrollBar()
                if sb is not None:
                    sb.setValue(int(scroll_val))
            except Exception:
                pass

    def _get_selected_folder_for_new_prompt(self) -> str:
        """Return folder path where a new prompt should be created based on current selection."""
        try:
            item = self.tree_widget.currentItem() if hasattr(self, 'tree_widget') else None
            if not item:
                return "Project Prompts"

            data = item.data(0, Qt.ItemDataRole.UserRole)
            if not data:
                return "Project Prompts"

            if data.get('type') == 'folder':
                return data.get('path', 'Project Prompts') or 'Project Prompts'

            if data.get('type') == 'prompt':
                folder = str(Path(data.get('path', '')).parent)
                if folder and folder != '.':
                    return folder
                return "Project Prompts"

        except Exception:
            pass

        return "Project Prompts"

    def _select_and_reveal_prompt(self, relative_path: str, prefer_library_tree: bool = False):
        """Expand parent folders (if needed) and select the prompt item in the tree."""
        if not hasattr(self, 'tree_widget') or not self.tree_widget:
            return

        def iter_items(parent: QTreeWidgetItem):
            for i in range(parent.childCount()):
                child = parent.child(i)
                yield child
                yield from iter_items(child)

        def is_under_special(it: QTreeWidgetItem) -> bool:
            p = it.parent()
            while p is not None:
                d = p.data(0, Qt.ItemDataRole.UserRole)
                if d and d.get('type') == 'special':
                    return True
                p = p.parent()
            return False

        root = self.tree_widget.invisibleRootItem()
        best = None
        for item in iter_items(root):
            data = item.data(0, Qt.ItemDataRole.UserRole)
            if data and data.get('type') == 'prompt' and data.get('path') == relative_path:
                if prefer_library_tree and is_under_special(item):
                    continue
                best = item
                break

        if best is None and prefer_library_tree:
            # Fall back to any match
            for item in iter_items(root):
                data = item.data(0, Qt.ItemDataRole.UserRole)
                if data and data.get('type') == 'prompt' and data.get('path') == relative_path:
                    best = item
                    break

        if best is not None:
            p = best.parent()
            while p is not None:
                p.setExpanded(True)
                p = p.parent()
            self.tree_widget.setCurrentItem(best)
            self.tree_widget.scrollToItem(best)

    def _select_and_reveal_folder(self, folder_path: str):
        """Select a folder item in the tree and expand its ancestors."""
        if not hasattr(self, 'tree_widget') or not self.tree_widget:
            return

        def iter_items(parent: QTreeWidgetItem):
            for i in range(parent.childCount()):
                child = parent.child(i)
                yield child
                yield from iter_items(child)

        root = self.tree_widget.invisibleRootItem()
        for item in iter_items(root):
            data = item.data(0, Qt.ItemDataRole.UserRole)
            if data and data.get('type') == 'folder' and data.get('path') == folder_path:
                p = item.parent()
                while p is not None:
                    p.setExpanded(True)
                    p = p.parent()
                self.tree_widget.setCurrentItem(item)
                self.tree_widget.scrollToItem(item)
                return

    def _make_unique_filename(self, folder: str, filename: str) -> str:
        """Generate a unique filename in a folder by appending (copy N) to the stem."""
        folder = folder or ""
        base = Path(filename).stem
        suffix = Path(filename).suffix or ".md"

        def build(name_stem: str) -> str:
            return f"{folder}/{name_stem}{suffix}" if folder else f"{name_stem}{suffix}"

        candidate_stem = f"{base} (copy)"
        candidate = build(candidate_stem)
        if candidate not in self.library.prompts:
            return candidate

        n = 2
        while True:
            candidate_stem = f"{base} (copy {n})"
            candidate = build(candidate_stem)
            if candidate not in self.library.prompts:
                return candidate
            n += 1

    def _make_unique_folder_path(self, dest_folder: str, folder_name: str) -> str:
        """Generate a unique folder path under dest_folder by appending (moved N)."""
        dest_folder = dest_folder or ""

        def build(name: str) -> str:
            return f"{dest_folder}/{name}" if dest_folder else name

        candidate = build(folder_name)
        if not (self.library.library_dir / candidate).exists():
            return candidate

        n = 2
        while True:
            candidate = build(f"{folder_name} (moved {n})")
            if not (self.library.library_dir / candidate).exists():
                return candidate
            n += 1

    def _move_folder_to_folder(self, src_folder: str, dest_folder: str) -> bool:
        """Move a folder (directory) to another folder (drag-and-drop backend)."""
        if not src_folder:
            return False

        src_folder = src_folder.strip("/\\")
        dest_folder = (dest_folder or "").strip("/\\")

        src_name = Path(src_folder).name
        new_folder = f"{dest_folder}/{src_name}" if dest_folder else src_name

        # Prevent moving into itself/descendant
        if dest_folder and (dest_folder == src_folder or dest_folder.startswith(src_folder + "/")):
            QMessageBox.warning(self.main_widget, "Move not allowed", "You can't move a folder into itself.")
            return False

        if new_folder == src_folder:
            return False

        # Handle destination conflict
        if (self.library.library_dir / new_folder).exists():
            new_folder = self._make_unique_folder_path(dest_folder, src_name)

        if not self.library.move_folder(src_folder, new_folder):
            QMessageBox.warning(self.main_widget, "Move failed", "Could not move the folder.")
            return False

        # Reload prompts so keys/filepaths match new layout.
        self.library.load_all_prompts()

        # Ensure active prompt content is still valid after path rewrite
        if self.library.active_primary_prompt_path and self.library.active_primary_prompt_path in self.library.prompts:
            self.library.active_primary_prompt = self.library.prompts[self.library.active_primary_prompt_path].get('content')

        # Remove attachments that no longer exist (shouldn't happen, but safe)
        self.library.attached_prompt_paths = [p for p in self.library.attached_prompt_paths if p in self.library.prompts]

        self._refresh_tree()
        return True

    def _move_prompt_to_folder(self, src_path: str, dest_folder: str) -> bool:
        """Move a prompt file to another folder (drag-and-drop backend)."""
        if src_path not in self.library.prompts:
            return False

        filename = Path(src_path).name
        dest_folder = dest_folder or ""
        new_path = f"{dest_folder}/{filename}" if dest_folder else filename

        if new_path == src_path:
            return False

        # Handle name conflicts
        if new_path in self.library.prompts:
            new_path = self._make_unique_filename(dest_folder, filename)

        if not self.library.move_prompt(src_path, new_path):
            QMessageBox.warning(self.main_widget, "Move failed", "Could not move the prompt.")
            return False

        # Update folder metadata and rewrite frontmatter in the moved file.
        try:
            prompt_data = self.library.prompts.get(new_path, {}).copy()
            prompt_data['folder'] = dest_folder
            prompt_data['modified'] = datetime.now().strftime('%Y-%m-%d')
            self.library.save_prompt(new_path, prompt_data)
        except Exception:
            pass

        self.library.load_all_prompts()
        self._refresh_tree()
        self._select_and_reveal_prompt(new_path)
        return True

    def _collapse_prompt_library_tree(self):
        """Collapse all folders in the Prompt Library tree."""
        if hasattr(self, 'tree_widget') and self.tree_widget:
            self.tree_widget.collapseAll()

    def _expand_prompt_library_tree(self):
        """Expand all folders in the Prompt Library tree."""
        if hasattr(self, 'tree_widget') and self.tree_widget:
            self.tree_widget.expandAll()
    
    def _build_tree_recursive(self, parent_item, directory: Path, relative_path: str):
        """Recursively build tree structure"""
        if not directory.exists():
            self.log_message(f"🔍 DEBUG: Directory doesn't exist: {directory}")
            return
        
        # Get items sorted (folders first, then files)
        try:
            items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            self.log_message(f"🔍 DEBUG: Found {len(items)} items in {directory.name}")
        except Exception as e:
            self.log_message(f"❌ ERROR listing directory {directory}: {e}")
            return
        
        for item in items:
            if item.name.startswith('.') or item.name == '__pycache__':
                continue
            
            if item.is_dir():
                # Folder
                rel_path = str(Path(relative_path) / item.name) if relative_path else item.name
                folder_item = QTreeWidgetItem([f"📁 {item.name}"])
                folder_item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'folder', 'path': rel_path})
                folder_item.setFlags(folder_item.flags() | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled)
                
                if parent_item:
                    parent_item.addChild(folder_item)
                else:
                    self.tree_widget.addTopLevelItem(folder_item)
                
                self.log_message(f"🔍 DEBUG: Added folder: {item.name} (path: {rel_path})")
                
                # Recurse
                self._build_tree_recursive(folder_item, item, rel_path)
            
            elif item.suffix.lower() in ['.svprompt', '.md', '.txt']:
                # Prompt file (.svprompt is new format, .md/.txt legacy)
                rel_path = str(Path(relative_path) / item.name) if relative_path else item.name
                
                self.log_message(f"🔍 DEBUG: Checking prompt file: {rel_path}")
                self.log_message(f"🔍 DEBUG: In library.prompts? {rel_path in self.library.prompts}")
                
                # Show first few keys for comparison
                if len(self.library.prompts) > 0:
                    sample_keys = list(self.library.prompts.keys())[:3]
                    self.log_message(f"🔍 DEBUG: Sample keys: {sample_keys}")
                
                if rel_path in self.library.prompts:
                    prompt_data = self.library.prompts[rel_path]
                    # Show full filename with extension in tree
                    name = item.name  # e.g., "prompt.svprompt"
                    
                    prompt_item = QTreeWidgetItem([name])
                    prompt_item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'prompt', 'path': rel_path})
                    prompt_item.setFlags(prompt_item.flags() | Qt.ItemFlag.ItemIsDragEnabled)
                    
                    # Visual indicators
                    indicators = []
                    if prompt_data.get('favorite'):
                        indicators.append("⭐")
                    if prompt_data.get('sv_quickmenu', prompt_data.get('quick_run', False)):
                        indicators.append("⚡")
                    if prompt_data.get('quickmenu_grid', False):
                        indicators.append("🖱️")
                    if indicators:
                        prompt_item.setText(0, f"{' '.join(indicators)} {name}")
                    
                    if parent_item:
                        parent_item.addChild(prompt_item)
                    else:
                        self.tree_widget.addTopLevelItem(prompt_item)
                    
                    self.log_message(f"🔍 DEBUG: Added prompt: {name}")
                else:
                    self.log_message(f"⚠️ DEBUG: Prompt not in library.prompts: {rel_path}")
    
    def _on_tree_item_clicked(self, item, column):
        """Handle tree item click"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if data and data.get('type') == 'prompt':
            self._load_prompt_in_editor(data['path'])
    
    def _on_tree_item_double_clicked(self, item, column):
        """Handle tree item double-click - set as primary"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if data and data.get('type') == 'prompt':
            self._set_primary_prompt(data['path'])
    
    def _show_tree_context_menu(self, position):
        """Show context menu for tree items"""
        item = self.tree_widget.itemAt(position)
        if not item:
            return
        
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        menu = QMenu()
        
        if data['type'] == 'prompt':
            path = data['path']
            
            # Set as primary
            action_primary = menu.addAction("⭐ Set as Primary Prompt")
            action_primary.triggered.connect(lambda: self._set_primary_prompt(path))
            
            # Attach/detach
            if path in self.library.attached_prompt_paths:
                action_attach = menu.addAction("❌ Detach from Active")
                action_attach.triggered.connect(lambda: self._detach_prompt(path))
            else:
                action_attach = menu.addAction("📎 Attach to Active")
                action_attach.triggered.connect(lambda: self._attach_prompt(path))
            
            menu.addSeparator()
            
            # Toggle favorite
            prompt_data = self.library.prompts.get(path, {})
            if prompt_data.get('favorite'):
                action_fav = menu.addAction("★ Remove from Favorites")
            else:
                action_fav = menu.addAction("☆ Add to Favorites")
            action_fav.triggered.connect(lambda: self._toggle_favorite(path))
            
            # Toggle QuickMenu (legacy: quick_run)
            if prompt_data.get('sv_quickmenu', prompt_data.get('quick_run', False)):
                action_qr = menu.addAction("⚡ Remove from QuickMenu")
            else:
                action_qr = menu.addAction("⚡ Add to QuickMenu")
            action_qr.triggered.connect(lambda: self._toggle_quick_run(path))

            # Toggle Grid right-click QuickMenu
            if prompt_data.get('quickmenu_grid', False):
                action_grid = menu.addAction("🖱️ Remove from Grid QuickMenu")
            else:
                action_grid = menu.addAction("🖱️ Add to Grid QuickMenu")
            action_grid.triggered.connect(lambda: self._toggle_quickmenu_grid(path))
            
            menu.addSeparator()
            
            # Edit, duplicate, delete
            action_edit = menu.addAction("✏️ Edit")
            action_edit.triggered.connect(lambda: self._load_prompt_in_editor(path))
            
            action_dup = menu.addAction("📋 Duplicate")
            action_dup.triggered.connect(lambda: self._duplicate_prompt(path))
            
            action_del = menu.addAction("🗑️ Delete")
            action_del.triggered.connect(lambda: self._delete_prompt(path))
        
        elif data['type'] == 'folder':
            # Folder operations
            action_new_prompt = menu.addAction("+ New Prompt in Folder")
            action_new_prompt.triggered.connect(lambda: self._new_prompt_in_folder(data['path']))
            
            action_new_folder = menu.addAction("📁 New Subfolder")
            action_new_folder.triggered.connect(lambda: self._new_subfolder(data['path']))
        
        menu.exec(self.tree_widget.viewport().mapToGlobal(position))
    
    def _load_prompt_in_editor(self, relative_path: str):
        """Load prompt into editor for viewing/editing"""
        if relative_path not in self.library.prompts:
            return
        
        prompt_data = self.library.prompts[relative_path]
        
        # Show full filename with extension (e.g., "prompt.svprompt")
        filename = Path(relative_path).name
        self.editor_name_label.setText(f"Editing: {filename}")
        self.editor_name_input.setText(filename)
        self.editor_desc_input.setText(prompt_data.get('description', ''))
        if hasattr(self, 'editor_quickmenu_label_input'):
            self.editor_quickmenu_label_input.setText(prompt_data.get('quickmenu_label', '') or prompt_data.get('name', ''))
        if hasattr(self, 'editor_quickmenu_in_grid_cb'):
            self.editor_quickmenu_in_grid_cb.setChecked(bool(prompt_data.get('quickmenu_grid', False)))
        if hasattr(self, 'editor_quickmenu_in_quickmenu_cb'):
            self.editor_quickmenu_in_quickmenu_cb.setChecked(bool(prompt_data.get('sv_quickmenu', prompt_data.get('quick_run', False))))
        self.editor_content.setPlainText(prompt_data.get('content', ''))
        
        # Store current path for saving
        self.editor_current_path = relative_path
        self.btn_save_prompt.setEnabled(True)
        
        # Hide external path display (this is a library prompt, not external)
        self.external_path_frame.setVisible(False)
        self._current_external_file_path = None
    
    def _save_current_prompt(self):
        """Save currently edited prompt"""
        try:
            name = self.editor_name_input.text().strip()
            description = self.editor_desc_input.text().strip()
            content = self.editor_content.toPlainText().strip()
            
            # Name field now represents the complete filename with extension
            # No stripping needed - user sees and edits the full filename

            quickmenu_label = ''
            quickmenu_grid = False
            sv_quickmenu = False
            if hasattr(self, 'editor_quickmenu_label_input'):
                quickmenu_label = self.editor_quickmenu_label_input.text().strip()
            if hasattr(self, 'editor_quickmenu_in_grid_cb'):
                quickmenu_grid = bool(self.editor_quickmenu_in_grid_cb.isChecked())
            if hasattr(self, 'editor_quickmenu_in_quickmenu_cb'):
                sv_quickmenu = bool(self.editor_quickmenu_in_quickmenu_cb.isChecked())

            if not name or not content:
                QMessageBox.warning(self.main_widget, "Error", "Name and content are required")
                return

            # Check if this is a new prompt or editing existing
            if hasattr(self, 'editor_current_path') and self.editor_current_path:
                path = self.editor_current_path
                
                # Handle external prompts (save back to external file)
                if path.startswith("[EXTERNAL] "):
                    external_file_path = path[11:]  # Remove "[EXTERNAL] " prefix
                    self._save_external_prompt(external_file_path, name, description, content)
                    return
                
                # Editing existing library prompt
                if path not in self.library.prompts:
                    QMessageBox.warning(self.main_widget, "Error", "Prompt no longer exists")
                    return

                prompt_data = self.library.prompts[path].copy()
                old_filename = Path(path).name
                
                # Extract name without extension for metadata
                name_without_ext = Path(name).stem
                
                prompt_data['name'] = name_without_ext
                prompt_data['description'] = description
                prompt_data['content'] = content
                prompt_data['quickmenu_label'] = quickmenu_label or name_without_ext
                prompt_data['quickmenu_grid'] = quickmenu_grid
                prompt_data['sv_quickmenu'] = sv_quickmenu
                # Keep legacy field in sync
                prompt_data['quick_run'] = sv_quickmenu
                
                # Check if filename changed - need to rename file
                if old_filename != name:
                    old_path = Path(path)
                    folder = str(old_path.parent) if old_path.parent != Path('.') else ''
                    new_path = f"{folder}/{name}" if folder else name
                    
                    # Delete old file and save to new location
                    if self.library.delete_prompt(path):
                        if self.library.save_prompt(new_path, prompt_data):
                            self.library.load_all_prompts()
                            self._refresh_tree()
                            self._select_and_reveal_prompt(new_path)
                            self.editor_current_path = new_path  # Update to new path
                            QMessageBox.information(self.main_widget, "Saved", f"Prompt renamed to '{name}' successfully!")
                            self.log_message(f"✓ Renamed prompt: {old_filename} → {name}")
                        else:
                            QMessageBox.warning(self.main_widget, "Error", "Failed to rename prompt")
                    else:
                        QMessageBox.warning(self.main_widget, "Error", "Failed to delete old prompt file")
                else:
                    # Name unchanged, just update in place
                    if self.library.save_prompt(path, prompt_data):
                        QMessageBox.information(self.main_widget, "Saved", "Prompt updated successfully!")
                        self._refresh_tree()
                    else:
                        QMessageBox.warning(self.main_widget, "Error", "Failed to save prompt")
            else:
                # Creating new prompt
                folder = getattr(self, 'editor_target_folder', 'Project Prompts')

                # Create new prompt data
                from datetime import datetime
                prompt_data = {
                    'name': name,
                    'description': description,
                    'content': content,
                    'domain': '',
                    'version': '1.0',
                    'task_type': 'Translation',
                    'favorite': False,
                    # QuickMenu
                    'quickmenu_label': quickmenu_label or name,
                    'quickmenu_grid': quickmenu_grid,
                    'sv_quickmenu': sv_quickmenu,
                    # Legacy
                    'quick_run': sv_quickmenu,
                    'folder': folder,
                    'tags': [],
                    'created': datetime.now().strftime('%Y-%m-%d'),
                    'modified': datetime.now().strftime('%Y-%m-%d')
                }

                # Create the prompt file (save_prompt creates new file if it doesn't exist)
                relative_path = f"{folder}/{name}.svprompt"
                if self.library.save_prompt(relative_path, prompt_data):
                    QMessageBox.information(self.main_widget, "Created", f"Prompt '{name}' created successfully!")
                    self.library.load_all_prompts()  # Reload to get new prompt in memory
                    self._refresh_tree()
                    self.editor_current_path = relative_path  # Now editing this prompt
                else:
                    QMessageBox.warning(self.main_widget, "Error", "Failed to create prompt")
        
        except Exception as e:
            import traceback
            error_msg = f"Prompt save error: {str(e)}\n{traceback.format_exc()}"
            print(f"[ERROR] {error_msg}")
            self.log_message(f"❌ Prompt save error: {str(e)}")
            QMessageBox.critical(self.main_widget, "Save Error", f"Failed to save prompt:\n\n{str(e)}")
            return
    
    def _save_external_prompt(self, file_path: str, name: str, description: str, content: str):
        """Save changes to an external prompt file"""
        from pathlib import Path
        import json
        
        path = Path(file_path)
        
        try:
            if file_path.lower().endswith('.svprompt'):
                # Save as JSON format
                data = {
                    'name': name,
                    'description': description,
                    'content': content,
                    'version': '1.0'
                }
                path.write_text(json.dumps(data, indent=2), encoding='utf-8')
            else:
                # Save as plain text
                path.write_text(content, encoding='utf-8')
            
            # Update the library's active primary prompt content
            self.library.active_primary_prompt = content
            
            QMessageBox.information(self.main_widget, "Saved", f"External prompt '{name}' saved successfully!")
            self.log_message(f"✓ Saved external prompt: {name}")
            
        except Exception as e:
            QMessageBox.warning(self.main_widget, "Error", f"Failed to save external prompt: {e}")
    
    def _set_primary_prompt(self, relative_path: str):
        """Set prompt as primary"""
        if self.library.set_primary_prompt(relative_path):
            prompt_data = self.library.prompts[relative_path]
            self.primary_prompt_label.setText(prompt_data.get('name', 'Unnamed'))
            self.primary_prompt_label.setStyleSheet("color: #000; font-weight: bold;")
            self.log_message(f"✓ Set primary: {prompt_data.get('name')}")
            # Also display in the editor
            self._load_prompt_in_editor(relative_path)
    
    def _attach_prompt(self, relative_path: str):
        """Attach prompt to active configuration"""
        if self.library.attach_prompt(relative_path):
            self._update_attached_list()
            prompt_data = self.library.prompts[relative_path]
            self.log_message(f"✓ Attached: {prompt_data.get('name')}")
    
    def _detach_prompt(self, relative_path: str):
        """Detach prompt from active configuration"""
        if self.library.detach_prompt(relative_path):
            self._update_attached_list()
            self.log_message(f"✓ Detached prompt")
    
    def _update_attached_list(self):
        """Update the attached prompts list widget"""
        self.attached_list_widget.clear()
        
        for path in self.library.attached_prompt_paths:
            if path in self.library.prompts:
                prompt_data = self.library.prompts[path]
                name = prompt_data.get('name', 'Unnamed')
                
                item = QTreeWidgetItem([name, "×"])
                item.setData(0, Qt.ItemDataRole.UserRole, path)
                
                self.attached_list_widget.addTopLevelItem(item)
    
    def _clear_primary_prompt(self):
        """Clear primary prompt selection"""
        self.library.active_primary_prompt = None
        self.library.active_primary_prompt_path = None
        self.primary_prompt_label.setText("[None selected]")
        self.primary_prompt_label.setStyleSheet("color: #999;")
        self.log_message("✓ Cleared primary prompt")
    
    def _load_external_primary_prompt(self):
        """Load an external prompt file (not in library) as primary"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_widget,
            "Select External Prompt File",
            "",
            "Prompt Files (*.svprompt *.txt *.md);;Supervertaler Prompts (*.svprompt);;Text Files (*.txt);;Markdown Files (*.md);;All Files (*.*)"
        )
        
        if not file_path:
            return  # User cancelled
        
        success, result = self.library.set_external_primary_prompt(file_path)
        
        if success:
            # result is the display name
            self.primary_prompt_label.setText(f"📁 {result}")
            self.primary_prompt_label.setStyleSheet("color: #0066cc; font-weight: bold;")
            self.primary_prompt_label.setToolTip(f"External file: {file_path}")
            self.log_message(f"✓ Loaded external prompt: {result}")
            
            # Display the external prompt in the editor
            self._display_external_prompt_in_editor(file_path, result)
        else:
            # result is the error message
            QMessageBox.warning(self.main_widget, "Error", f"Could not load file: {result}")
    
    def _display_external_prompt_in_editor(self, file_path: str, display_name: str):
        """Display an external prompt file in the editor (read-only view)"""
        from pathlib import Path
        import json
        
        path = Path(file_path)
        
        try:
            content = path.read_text(encoding='utf-8')
            description = ""
            
            # Try to parse as JSON (.svprompt format)
            if file_path.lower().endswith('.svprompt'):
                try:
                    data = json.loads(content)
                    # Extract content and description from svprompt
                    content = data.get('content', content)
                    description = data.get('description', '')
                except json.JSONDecodeError:
                    pass  # Keep raw content
            
            # Update editor fields
            self.editor_name_label.setText(f"📁 External: {display_name}")
            self.editor_name_input.setText(display_name)
            self.editor_desc_input.setText(description)
            self.editor_content.setPlainText(content)
            
            # Store the external path for potential save operations
            self.editor_current_path = f"[EXTERNAL] {file_path}"
            self._current_external_file_path = file_path  # Store for folder opening
            self.btn_save_prompt.setEnabled(True)
            
            # Show the external path with clickable link
            self.external_path_label.setText(file_path)
            self.external_path_frame.setVisible(True)
            
        except Exception as e:
            self.log_message(f"⚠ Could not display prompt in editor: {e}")
    
    def _open_external_prompt_folder(self, event):
        """Open the folder containing the current external prompt file"""
        import subprocess
        import platform
        from pathlib import Path
        
        if not hasattr(self, '_current_external_file_path') or not self._current_external_file_path:
            return
        
        folder_path = Path(self._current_external_file_path).parent
        
        if not folder_path.exists():
            QMessageBox.warning(self.main_widget, "Folder Not Found", f"The folder no longer exists:\n{folder_path}")
            return
        
        try:
            if platform.system() == 'Windows':
                # Open folder and select the file
                subprocess.run(['explorer', '/select,', str(self._current_external_file_path)])
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', '-R', str(self._current_external_file_path)])
            else:  # Linux
                subprocess.run(['xdg-open', str(folder_path)])
        except Exception as e:
            QMessageBox.warning(self.main_widget, "Error", f"Could not open folder: {e}")

    def _clear_all_attachments(self):
        """Clear all attached prompts"""
        self.library.clear_attachments()
        self._update_attached_list()
        self.log_message("✓ Cleared all attachments")
    
    def _toggle_favorite(self, relative_path: str):
        """Toggle favorite status"""
        if self.library.toggle_favorite(relative_path):
            self._refresh_tree()
    
    def _toggle_quick_run(self, relative_path: str):
        """Toggle QuickMenu (future app menu) status (legacy name: quick_run)."""
        if self.library.toggle_quick_run(relative_path):
            self._refresh_tree()

    def _toggle_quickmenu_grid(self, relative_path: str):
        """Toggle whether this prompt appears in the Grid right-click QuickMenu."""
        if self.library.toggle_quickmenu_grid(relative_path):
            self._refresh_tree()
    
    def _new_prompt(self):
        """Create new prompt in the currently selected folder."""
        self._new_prompt_in_folder(self._get_selected_folder_for_new_prompt())
    
    def _new_folder(self):
        """Create new folder"""
        name, ok = QInputDialog.getText(self.main_widget, "New Folder", "Enter folder name:")
        if ok and name:
            if self.library.create_folder(name):
                self._refresh_tree()
    
    def _new_prompt_in_folder(self, folder_path: str):
        """Create new prompt in specific folder"""
        name, ok = QInputDialog.getText(self.main_widget, "New Prompt", "Enter prompt filename with extension (e.g., prompt.svprompt):")
        if not ok or not name:
            return
        
        # Ensure .svprompt extension
        if not name.endswith('.svprompt'):
            name = f"{name}.svprompt"
        
        # Extract name without extension for metadata
        name_without_ext = Path(name).stem
        
        # Create the prompt immediately
        from datetime import datetime
        prompt_data = {
            'name': name_without_ext,
            'description': '',
            'content': '# Your prompt content here\n\nProvide translation instructions...',
            'domain': '',
            'version': '1.0',
            'task_type': 'Translation',
            'favorite': False,
            'quickmenu_label': name_without_ext,
            'quickmenu_grid': False,
            'sv_quickmenu': False,
            'quick_run': False,
            'folder': folder_path,
            'tags': [],
            'created': datetime.now().strftime('%Y-%m-%d'),
            'modified': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Create .svprompt file (name already includes .svprompt extension)
        relative_path = f"{folder_path}/{name}" if folder_path else name
        
        if self.library.save_prompt(relative_path, prompt_data):
            self.library.load_all_prompts()  # Reload to get new prompt in memory
            self._refresh_tree()
            self._select_and_reveal_prompt(relative_path)
            self._load_prompt_in_editor(relative_path)
            self.btn_save_prompt.setEnabled(True)  # Ensure Save button is enabled for new prompt
            self.log_message(f"✓ Created new prompt '{name}' in folder: {folder_path}")
        else:
            QMessageBox.warning(self.main_widget, "Error", "Failed to create prompt")
    
    def _new_subfolder(self, parent_folder: str):
        """Create subfolder"""
        name, ok = QInputDialog.getText(self.main_widget, "New Subfolder", "Enter folder name:")
        if ok and name:
            full_path = str(Path(parent_folder) / name)
            if self.library.create_folder(full_path):
                self._refresh_tree()
    
    def _duplicate_prompt(self, relative_path: str):
        """Duplicate a prompt into the same folder with a unique filename."""
        if relative_path not in self.library.prompts:
            return

        src_data = self.library.prompts[relative_path].copy()
        src_name = src_data.get('name', Path(relative_path).stem)

        folder = str(Path(relative_path).parent)
        if folder == '.':
            folder = ''

        filename = Path(relative_path).name
        new_path = self._make_unique_filename(folder, filename)
        new_name = Path(new_path).stem

        src_data['name'] = new_name
        src_data['favorite'] = False
        src_data['quick_run'] = False
        src_data['quickmenu_grid'] = False
        src_data['sv_quickmenu'] = False
        src_data['folder'] = folder
        src_data['created'] = datetime.now().strftime('%Y-%m-%d')
        src_data['modified'] = datetime.now().strftime('%Y-%m-%d')

        if self.library.save_prompt(new_path, src_data):
            self.library.load_all_prompts()
            self._refresh_tree()
            self._select_and_reveal_prompt(new_path)
            self._load_prompt_in_editor(new_path)
            self.log_message(f"✓ Duplicated: {src_name} → {new_name} (saved as .svprompt)")
        else:
            QMessageBox.warning(self.main_widget, "Duplicate failed", "Failed to duplicate the prompt.")
    
    def _delete_prompt(self, relative_path: str):
        """Delete a prompt"""
        reply = QMessageBox.question(
            self.main_widget,
            "Delete Prompt",
            "Are you sure you want to delete this prompt?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.library.delete_prompt(relative_path):
                self._refresh_tree()
                self.log_message("✓ Prompt deleted")
    
    def _refresh_library(self):
        """Reload library and refresh UI"""
        self.library.load_all_prompts()
        self._refresh_tree()
        self._update_attached_list()
        self.log_message("✓ Library refreshed")
    
    def _preview_combined_prompt(self):
        """Preview the combined prompt with actual segment text"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QMessageBox
        
        # Get current segment from the app
        current_segment = None
        current_segment_id = "Preview"
        source_lang = "Source Language"
        target_lang = "Target Language"
        
        # Try to get segment from main app
        if hasattr(self, 'parent_app') and self.parent_app:
            # Get languages if project loaded
            if hasattr(self.parent_app, 'current_project') and self.parent_app.current_project:
                source_lang = getattr(self.parent_app.current_project, 'source_lang', 'Source Language')
                target_lang = getattr(self.parent_app.current_project, 'target_lang', 'Target Language')
                
                # Try to get selected segment
                if hasattr(self.parent_app, 'table') and self.parent_app.table:
                    current_row = self.parent_app.table.currentRow()
                    if current_row >= 0:
                        # Map display row to actual segment index
                        actual_index = current_row
                        if hasattr(self.parent_app, 'grid_row_to_segment_index') and self.parent_app.grid_row_to_segment_index:
                            if current_row in self.parent_app.grid_row_to_segment_index:
                                actual_index = self.parent_app.grid_row_to_segment_index[current_row]
                        
                        # Get segment
                        if actual_index < len(self.parent_app.current_project.segments):
                            current_segment = self.parent_app.current_project.segments[actual_index]
                            current_segment_id = f"Segment {current_segment.id}"
                
                # Fallback to first segment if none selected
                if not current_segment and len(self.parent_app.current_project.segments) > 0:
                    current_segment = self.parent_app.current_project.segments[0]
                    current_segment_id = f"Example: Segment {current_segment.id}"
        
        # Get source text
        if current_segment:
            source_text = current_segment.source
        else:
            source_text = "{{SOURCE_TEXT}}"
            QMessageBox.information(
                self.main_widget,
                "No Segment Selected",
                "No segment is currently selected. Showing template with placeholder text.\n\n"
                "To see the actual prompt with your text, please select a segment first."
            )
        
        # Build combined prompt
        combined = self.build_final_prompt(source_text, source_lang, target_lang)
        
        # Build composition info
        composition_parts = []
        composition_parts.append(f"📍 Segment: {current_segment_id}")
        composition_parts.append(f"🌐 Languages: {source_lang} → {target_lang}")
        composition_parts.append(f"📏 Total prompt length: {len(combined):,} characters")
        
        if self.library.active_primary_prompt:
            composition_parts.append(f"✓ Primary prompt attached")
        
        if self.library.attached_prompts:
            composition_parts.append(f"✓ {len(self.library.attached_prompts)} additional prompt(s) attached")
        
        composition_text = "\n".join(composition_parts)
        
        # Create custom dialog with proper text editor
        dialog = QDialog(self.main_widget)
        dialog.setWindowTitle("🧪 Combined Prompt Preview")
        dialog.resize(900, 700)  # Larger default size
        
        layout = QVBoxLayout(dialog)
        
        # Info label
        info_label = QLabel(
            "<b>Complete Assembled Prompt</b><br>"
            "This is what will be sent to the AI (System Prompt + Custom Prompts + your text)<br><br>" +
            composition_text.replace("\n", "<br>")
        )
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding: 10px; background-color: #e3f2fd; border-radius: 4px; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # Text editor for preview
        text_edit = QTextEdit()
        text_edit.setPlainText(combined)
        text_edit.setReadOnly(True)
        text_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        text_edit.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace; font-size: 9pt;")
        layout.addWidget(text_edit, 1)  # Stretch factor 1
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        close_btn.setStyleSheet("padding: 8px 20px; font-weight: bold;")
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        dialog.exec()
    
    def _view_current_system_template(self):
        """View the current system prompt"""
        template = self.get_system_template(self.current_mode)
        
        dialog = QMessageBox(self.main_widget)
        dialog.setWindowTitle(f"System Prompt: {self._get_mode_display_name()}")
        dialog.setText(f"Current system prompt for {self._get_mode_display_name()} mode:")
        dialog.setDetailedText(template)
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.exec()
    
    def _open_system_prompts_settings(self):
        """Open system prompts in settings"""
        try:
            # Navigate to Settings tab if main app has the method
            # Use parent_app (not app)
            if hasattr(self.parent_app, 'main_tabs') and hasattr(self.parent_app, 'settings_tabs'):
                # Navigate to Settings tab (index 3)
                self.parent_app.main_tabs.setCurrentIndex(3)
                # Navigate to System Prompts sub-tab (index 5 - after General, LLM, Language, MT, View)
                # Verify the index is valid before setting it
                if self.parent_app.settings_tabs.count() > 5:
                    self.parent_app.settings_tabs.setCurrentIndex(5)
                else:
                    # Log warning and fall back to first tab
                    print(f"[WARNING] settings_tabs only has {self.parent_app.settings_tabs.count()} tabs, cannot navigate to index 5")
                    self.parent_app.settings_tabs.setCurrentIndex(0)
                    QMessageBox.warning(
                        self.main_widget,
                        "Navigation Issue",
                        f"Could not navigate to System Prompts tab (expected at index 5, but only {self.parent_app.settings_tabs.count()} tabs exist).\n\n"
                        "Please manually navigate to Settings → System Prompts."
                    )
            else:
                # Fallback message
                QMessageBox.information(
                    self.main_widget,
                    "System Prompts",
                    "System Prompts (Layer 1) are configured in Settings → System Prompts tab.\n\n"
                    "They are automatically selected based on the document type you're processing."
                )
        except Exception as e:
            import traceback
            error_msg = f"Error opening System Prompts settings: {str(e)}"
            print(f"[ERROR] {error_msg}")
            print(traceback.format_exc())
            QMessageBox.critical(
                self.main_widget,
                "Error",
                f"Failed to open System Prompts settings:\n\n{str(e)}\n\n"
                "Please manually navigate to Settings → System Prompts tab."
            )
    
    # === System Prompts Management ===
    
    def _load_system_templates(self):
        """Load system prompts from files"""
        system_templates_dir = self.prompt_library_dir / "1_System_Prompts"
        
        if system_templates_dir.exists():
            # Load from old location if exists (migration support)
            file_map = {
                "Single Segment Translation (system prompt).md": "single",
                "Batch DOCX Translation (system prompt).md": "batch_docx",
                "Batch Bilingual Translation (system prompt).md": "batch_bilingual"
            }
            
            for filename, mode in file_map.items():
                filepath = system_templates_dir / filename
                if filepath.exists():
                    self.system_templates[mode] = filepath.read_text(encoding='utf-8')
        
        # Fill missing with defaults
        for mode in ["single", "batch_docx", "batch_bilingual"]:
            if mode not in self.system_templates:
                self.system_templates[mode] = self._get_default_system_template(mode)
    
    def _get_default_system_template(self, mode: str) -> str:
        """Get default system prompt for a mode"""
        # Comprehensive system prompt with detailed CAT tag instructions
        return """# SYSTEM PROMPT

⚠️ **PROFESSIONAL TRANSLATION CONTEXT:**
You are performing professional technical/medical translation as a licensed service for a commercial translation company. This is legitimate professional work. All medical, technical, or specialized terminology is for professional translation purposes only.

You are an expert {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}} translator with deep understanding of context and nuance.

**YOUR TASK**: Translate the text below.

**IMPORTANT INSTRUCTIONS**:
- Provide ONLY the translated text
- Do NOT include numbering, labels, or commentary
- Do NOT repeat the source text
- Maintain accuracy and natural fluency

**CRITICAL: INLINE FORMATTING TAG PRESERVATION**:
- Source text may contain simple HTML-style formatting tags: <b>bold</b>, <i>italic</i>, <u>underline</u>
- These tags represent text formatting that MUST be preserved in the translation
- Place the tags around the CORRESPONDING translated words, not necessarily in the same position
- Example: "Click the <b>Save</b> button" → "Klik op de knop <b>Opslaan</b>"
- Ensure every opening tag has a matching closing tag
- Never omit, add, or modify tags - preserve the exact same tags from source

**CRITICAL: CAT TOOL TAG PRESERVATION**:
- Source may contain CAT tool formatting tags in various formats:
  • memoQ: [1}, {2], [3}, {4] (asymmetric bracket-brace pairs)
  • Trados Studio: <410>text</410>, <434>text</434> (XML-style opening/closing tags)
  • CafeTran: |formatted text| (pipe symbols mark formatted text - bold, italic, underline, etc.)
  • Other CAT tools: various bracketed or special character sequences
- These are placeholder tags representing formatting (bold, italic, links, etc.)
- PRESERVE ALL tags - if source has N tags, target must have exactly N tags
- Keep tags with their content and adjust position for natural target language word order
- Never translate, omit, or modify the tags themselves - only reposition them
- Examples:
  • memoQ: '[1}De uitvoer{2]' → '[1}The exports{2]'
  • Trados: '<410>De uitvoer van machines</410>' → '<410>Exports of machinery</410>'
  • CafeTran: 'He debuted against |Juventus FC| in 2001' → 'Hij debuteerde tegen |Juventus FC| in 2001'
  • Multiple: '[1}De uitvoer{2] [3}stelt niets voor{4]' → '[1}Exports{2] [3}mean nothing{4]'

**LANGUAGE-SPECIFIC NUMBER FORMATTING**:
- If the target language is **Dutch**, **French**, **German**, **Italian**, **Spanish**, or another **continental European language**, use a **comma** as the decimal separator and a **space or non-breaking space** between the number and unit (e.g., 17,1 cm).
- If the target language is **English** or **Irish**, use a **full stop (period)** as the decimal separator and **no space** before the unit (e.g., 17.1 cm).
- Always follow the **number formatting conventions** of the target language.

If the text refers to figures (e.g., 'Figure 1A'), relevant images may be provided for visual context.

{{SOURCE_LANGUAGE}} text:
{{SOURCE_TEXT}}"""
    
    def get_system_template(self, mode: str) -> str:
        """Get system prompt for specified mode"""
        return self.system_templates.get(mode, self._get_default_system_template(mode))
    
    def set_mode(self, mode: str):
        """Set current translation mode (single, batch_docx, batch_bilingual)"""
        if mode in ["single", "batch_docx", "batch_bilingual"]:
            self.current_mode = mode
            if hasattr(self, 'mode_label'):
                self.mode_label.setText(f"Mode: {self._get_mode_display_name()}")
    
    def update_image_context_display(self):
        """Update the Image Context label in Active Configuration panel"""
        if not hasattr(self, 'image_context_label'):
            return
            
        # Check if parent app has figure_context
        if hasattr(self, 'parent_app') and self.parent_app:
            if hasattr(self.parent_app, 'figure_context') and self.parent_app.figure_context:
                fc = self.parent_app.figure_context
                if fc.has_images():
                    count = fc.get_image_count()
                    folder_name = fc.get_folder_name() or "folder"
                    self.image_context_label.setText(f"✅ {count} image{'s' if count != 1 else ''} from: {folder_name}")
                    self.image_context_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
                    return
        
        # No images loaded
        self.image_context_label.setText("[None loaded]")
        self.image_context_label.setStyleSheet("color: #999;")
    
    # === Prompt Composition (for translation) ===
    
    def build_final_prompt(self, source_text: str, source_lang: str, target_lang: str, mode: str = None) -> str:
        """
        Build final prompt for translation using 2-layer architecture:
        1. System Prompt (auto-selected by mode)
        2. Combined prompts from library (primary + attached)
        
        Args:
            source_text: Text to translate
            source_lang: Source language
            target_lang: Target language
            mode: Override mode (if None, uses self.current_mode)
        
        Returns:
            Complete prompt ready for LLM
        """
        if mode is None:
            mode = self.current_mode
        
        # Layer 1: System Prompt
        system_template = self.get_system_template(mode)
        
        # Replace placeholders in system prompt
        system_template = system_template.replace("{{SOURCE_LANGUAGE}}", source_lang)
        system_template = system_template.replace("{{TARGET_LANGUAGE}}", target_lang)
        system_template = system_template.replace("{{SOURCE_TEXT}}", source_text)
        
        # Layer 2: Library prompts (primary + attached)
        library_prompts = ""
        
        if self.library.active_primary_prompt:
            library_prompts += "\n\n# PRIMARY INSTRUCTIONS\n\n"
            library_prompts += self.library.active_primary_prompt
        
        for attached_content in self.library.attached_prompts:
            library_prompts += "\n\n# ADDITIONAL INSTRUCTIONS\n\n"
            library_prompts += attached_content
        
        # Combine
        final_prompt = system_template + library_prompts
        
        # Add translation delimiter
        final_prompt += "\n\n**YOUR TRANSLATION (provide ONLY the translated text, no numbering or labels):**\n"
        
        return final_prompt
    
    # ============================================================================
    # AI ASSISTANT METHODS
    # ============================================================================
    
    def _init_llm_client(self):
        """Initialize LLM client with available API keys"""
        try:
            # Use parent app's API key loading method (reads from user_data/api_keys.txt)
            if hasattr(self.parent_app, 'load_api_keys'):
                api_keys = self.parent_app.load_api_keys()
            else:
                # Fallback to module function (legacy path)
                api_keys = load_api_keys()
            
            # Debug: Log which keys were found (without exposing the actual keys)
            key_names = [k for k in api_keys.keys() if api_keys.get(k)]
            if key_names:
                self.log_message(f"🔑 Found API keys for: {', '.join(key_names)}")
            else:
                self.log_message("⚠ No API keys found in api_keys.txt")
            
            # Try to use the same provider as main app if available
            provider = None
            model = None
            
            # Check parent app settings
            if hasattr(self.parent_app, 'current_provider'):
                provider = self.parent_app.current_provider
                if hasattr(self.parent_app, 'current_model'):
                    model = self.parent_app.current_model
            
            # Fallback: use first available API key
            if not provider:
                if api_keys.get("openai"):
                    provider = "openai"
                elif api_keys.get("claude"):
                    provider = "claude"
                elif api_keys.get("google") or api_keys.get("gemini"):
                    provider = "gemini"
            
            if provider:
                # Map provider names to API key names (gemini uses 'google' key)
                key_name = "google" if provider == "gemini" else provider
                api_key = api_keys.get(key_name) or api_keys.get("gemini") or api_keys.get("openai") or api_keys.get("claude") or api_keys.get("google")
                if api_key:
                    self.llm_client = LLMClient(
                        api_key=api_key,
                        provider=provider,
                        model=model,
                        max_tokens=16384
                    )
                    self.log_message(f"✓ AI Assistant initialized with {provider}")
                else:
                    self.log_message("⚠ No API keys found for AI Assistant")
            else:
                self.log_message("⚠ No LLM provider configured")
                
        except Exception as e:
            self.log_message(f"⚠ Failed to initialize AI Assistant: {e}")
    
    def _load_conversation_history(self):
        """Load previous conversation from disk"""
        try:
            if self.ai_conversation_file.exists():
                with open(self.ai_conversation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.chat_history = data.get('history', [])
                    # Don't load files from JSON - they're loaded from AttachmentManager

                # Restore chat display
                if hasattr(self, 'chat_display'):
                    for msg in self.chat_history[-10:]:  # Show last 10 messages
                        self._add_chat_message(msg['role'], msg['content'], save=False)

                # Refresh attached files list after UI is created
                if hasattr(self, 'attached_files_list_layout'):
                    self._refresh_attached_files_list()

        except Exception as e:
            self.log_message(f"⚠ Failed to load conversation history: {e}")
    
    def _save_conversation_history(self):
        """Save conversation to disk"""
        try:
            self.ai_conversation_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ai_conversation_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'history': self.chat_history,
                    'files': self.attached_files,
                    'updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.log_message(f"⚠ Failed to save conversation: {e}")

    def _load_persisted_attachments(self):
        """Load attached files from AttachmentManager"""
        try:
            # Load files from current session
            files = self.attachment_manager.list_session_files()

            # Populate attached_files for backward compatibility
            for file_meta in files:
                # Get full file data including content
                file_data = self.attachment_manager.get_file(file_meta['file_id'])
                if file_data:
                    # Convert to old format for compatibility
                    self.attached_files.append({
                        'path': file_data.get('original_path', ''),
                        'name': file_data.get('original_name', ''),
                        'content': file_data.get('content', ''),
                        'type': file_data.get('file_type', ''),
                        'size': file_data.get('size_chars', 0),
                        'attached_at': file_data.get('attached_at', ''),
                        'file_id': file_data.get('file_id', '')  # Keep ID for reference
                    })

            if files:
                self.log_message(f"✓ Loaded {len(files)} attached files from session")

        except Exception as e:
            self.log_message(f"⚠ Failed to load persisted attachments: {e}")

    def _analyze_and_generate(self):
        """Analyze current project and generate prompts"""
        if not self.llm_client:
            self._add_chat_message(
                "system",
                "⚠ AI Assistant not available. Please configure API keys in Settings."
            )
            return
        
        self._add_chat_message(
            "system",
            "🔍 Analyzing project and generating prompts...\n\n"
            "Gathering context from:\n"
            "• Current document\n"
            "• Translation memories\n"
            "• Termbases\n"
            "• Existing prompts"
        )
        
        # Build context
        context = self._build_project_context()
        
        # Create analysis prompt
        analysis_prompt = f"""Create a comprehensive translation prompt for this project and save it using the ACTION system.

PROJECT CONTEXT:
{context}

Create a translation prompt. Output ONE complete ACTION block:

ACTION:create_prompt PARAMS:{{"name": "[Name]", "content": "[Prompt]", "folder": "Project Prompts", "description": "Auto-generated", "activate": true}}

Prompt must include:

# ROLE & EXPERTISE
You are an expert [domain] translator ([source] → [target]) with 10+ years experience.

# DOCUMENT CONTEXT
**Type:** [type]
**Domain:** [domain]
**Language pair:** [source] → [target]
**Content:** [brief description]
**Number of segments:** [count]

# KEY TERMINOLOGY
| [Source] | [Target] | Notes |
|----------|----------|-------|
[Extract 20+ key terms from termbases/document]

# TRANSLATION CONSTRAINTS
**MUST:**
- Preserve all tags, markers, and placeholders exactly as in the source
- Translate strictly one segment per line, preserving segmentation and order
- Follow the KEY TERMINOLOGY glossary exactly for all mapped terms
- If a segment is already in the target language, leave it unchanged

**MUST NOT:**
- Add explanations, comments, footnotes, or translator's notes
- Modify formatting, tags, numbering, brackets, or spacing
- Merge or split segments

**CRITICAL:** Based on the language pair, include appropriate format localization rules:

### NUMBERS, DATES & LOCALISATION
- If translating FROM Dutch/French/German/Spanish/Italian TO English: Include number format conversion (comma decimal → period decimal, e.g., 718.592,01 → 718,592.01)
- If translating FROM English TO Dutch/French/German/Spanish/Italian: Include number format conversion (period decimal → comma decimal)
- Include date localization rules if relevant (e.g., Dutch month names → English: juni → June)

### DOMAIN-SPECIFIC RULES
- For LEGAL domain (Belgian): Include "Preserve 'Meester' + surname format for Belgian notaries"
- For LEGAL domain: Include preservation of legal entity abbreviations (e.g., BV, NV, RPR)
- For MEDICAL domain: Include anatomical term consistency
- For TECHNICAL domain: Include measurement unit handling

# OUTPUT FORMAT
Provide ONLY the translation, one segment per line, aligned 1:1 with the source lines.

Output complete ACTION."""
        
        # Send to AI (in thread to avoid blocking UI)
        self._send_ai_request(analysis_prompt, is_analysis=True)
    
    def _build_project_context(self) -> str:
        """Build context from current project"""
        context_parts = []

        # Current document info
        if hasattr(self.parent_app, 'current_document_path'):
            doc_path = self.parent_app.current_document_path
            if doc_path:
                context_parts.append(f"**Document:** {Path(doc_path).name}")

        # Language pair
        if hasattr(self.parent_app, 'current_project') and self.parent_app.current_project:
            project = self.parent_app.current_project
            if hasattr(project, 'source_language') and hasattr(project, 'target_language'):
                context_parts.append(f"**Language Pair:** {project.source_language} → {project.target_language}")

        # Full document content
        if hasattr(self.parent_app, 'current_project') and self.parent_app.current_project:
            project = self.parent_app.current_project
            if hasattr(project, 'segments') and project.segments:
                total = len(project.segments)
                context_parts.append(f"\n**Project Size:** {total} segments")

                # Try to get full document markdown (up to 50,000 chars for analysis)
                if self._cached_document_markdown:
                    # Use cached markdown
                    doc_content = self._cached_document_markdown[:50000]
                    context_parts.append(f"\n**Full Document Content:**\n{doc_content}")
                else:
                    # Fallback: Construct from segments (first 100 segments)
                    context_parts.append(f"\n**Document Content (first 100 segments):**")
                    for i, seg in enumerate(project.segments[:100], 1):
                        context_parts.append(f"\n{i}. {seg.source}")
                        if seg.target:
                            context_parts.append(f"   → {seg.target}")

        # Attached files
        if self.attached_files:
            context_parts.append(f"\n**Attached Files ({len(self.attached_files)}):**")
            for file in self.attached_files:
                context_parts.append(f"- {file['name']}: {len(file.get('content', ''))} chars")
                # Show preview of file content
                if file.get('content'):
                    preview = file['content'][:200].replace('\n', ' ')
                    context_parts.append(f"  Preview: {preview}...")

        return "\n".join(context_parts) if context_parts else "No context available"
    
    def _list_available_prompts(self) -> str:
        """List all prompts in library"""
        if not self.library.prompts:
            return "No prompts in library"
        
        lines = []
        for path, data in list(self.library.prompts.items())[:20]:  # First 20
            name = data.get('name', Path(path).stem)
            folder = Path(path).parent.name
            lines.append(f"- {folder}/{name}")
        
        if len(self.library.prompts) > 20:
            lines.append(f"... and {len(self.library.prompts) - 20} more")
        
        return "\n".join(lines)
    
    def _attach_file(self):
        """Attach a file to the conversation"""
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Attach File",
            "",
            "Documents (*.pdf *.docx *.txt *.md);;All Files (*.*)"
        )
        if not file_path:
            return
        
        try:
            file_path_obj = Path(file_path)
            
            # Read file content based on type
            content = ""
            file_type = file_path_obj.suffix.lower()
            conversion_note = ""
            
            if file_type == '.txt' or file_type == '.md':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file_type in ['.pdf', '.docx', '.pptx', '.xlsx']:
                # Use markitdown for document conversion
                try:
                    from markitdown import MarkItDown
                    md = MarkItDown()
                    result = md.convert(file_path)
                    content = result.text_content
                    conversion_note = f" (converted to markdown: {len(content):,} chars)"
                except ImportError:
                    content = f"[{file_type.upper()} file: {file_path_obj.name}]\n(markitdown not installed - run: pip install markitdown)"
                    conversion_note = " (conversion unavailable)"
                except Exception as e:
                    content = f"[{file_type.upper()} file: {file_path_obj.name}]\n(Conversion error: {e})"
                    conversion_note = f" (conversion failed: {e})"
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    content = f"[Binary file: {file_path_obj.name}]"
            
            # Save to AttachmentManager (persistent storage)
            file_id = self.attachment_manager.attach_file(
                original_path=str(file_path),
                markdown_content=content,
                original_name=file_path_obj.name,
                conversation_id=None  # Optional conversation tracking
            )

            if file_id:
                # Add to attached files for backward compatibility
                file_data = {
                    'path': str(file_path),
                    'name': file_path_obj.name,
                    'content': content,
                    'type': file_type,
                    'size': len(content),
                    'attached_at': datetime.now().isoformat(),
                    'file_id': file_id  # Store ID for later reference
                }
                self.attached_files.append(file_data)

                # Update UI
                self._update_context_sidebar()

                # Add message
                self._add_chat_message(
                    "system",
                    f"📎 File attached: **{file_path_obj.name}**\n"
                    f"Type: {file_type}, Size: {len(content):,} chars{conversion_note}\n\n"
                    f"You can now ask questions about this file."
                )

                self._save_conversation_history()
            else:
                QMessageBox.warning(None, "Attachment Error", "Failed to save attachment to disk.")
            
        except Exception as e:
            QMessageBox.warning(None, "Attachment Error", f"Failed to attach file:\n{e}")
    
    def _update_context_sidebar(self):
        """Update the context sidebar with current state"""
        # Update current document display
        self._update_current_document_display()

        # Update attached files list
        if hasattr(self, 'attached_files_list_layout'):
            self._refresh_attached_files_list()

    def _update_current_document_display(self):
        """Update the current document section in the sidebar"""
        if not hasattr(self, 'context_current_doc'):
            return

        # Get document info from parent app
        doc_info = "No document loaded"

        if hasattr(self.parent_app, 'current_project') and self.parent_app.current_project:
            project = self.parent_app.current_project
            # Get project name
            project_name = getattr(project, 'name', 'Unnamed Project')

            # Get document info
            if hasattr(self.parent_app, 'current_document_path') and self.parent_app.current_document_path:
                doc_path = Path(self.parent_app.current_document_path)
                doc_info = f"{project_name}\n{doc_path.name}"
            elif hasattr(project, 'source_file') and project.source_file:
                doc_path = Path(project.source_file)
                doc_info = f"{project_name}\n{doc_path.name}"
            else:
                doc_info = f"{project_name}\nNo document"

        # Update the label (find the description label in the section)
        # The section has a QVBoxLayout with [title_label, desc_label]
        layout = self.context_current_doc.layout()
        if layout and layout.count() >= 2:
            desc_label = layout.itemAt(1).widget()
            if isinstance(desc_label, QLabel):
                desc_label.setText(doc_info)

    def _get_document_content_preview(self, max_chars=3000):
        """
        Get a preview of the current document content.

        Tries multiple methods to access document content:
        1. From parent_app segments (if available)
        2. From project source_segments or target_segments
        3. Direct file read if needed

        Returns:
            String with document preview (first max_chars characters) or None
        """
        try:
            # Method 1: Try to get segments from parent app
            if hasattr(self.parent_app, 'segments') and self.parent_app.segments:
                segments = self.parent_app.segments
                # Combine segment source text
                lines = []
                for seg in segments[:50]:  # First 50 segments
                    if hasattr(seg, 'source'):
                        lines.append(seg.source)
                    elif isinstance(seg, dict) and 'source' in seg:
                        lines.append(seg['source'])

                if lines:
                    content = '\n'.join(lines)
                    return content[:max_chars]

            # Method 2: Try to get from current project's segments
            if hasattr(self.parent_app, 'current_project') and self.parent_app.current_project:
                project = self.parent_app.current_project

                # Check for source_segments attribute
                if hasattr(project, 'source_segments') and project.source_segments:
                    lines = []
                    for seg in project.source_segments[:50]:
                        if isinstance(seg, str):
                            lines.append(seg)
                        elif hasattr(seg, 'text'):
                            lines.append(seg.text)
                        elif isinstance(seg, dict) and 'text' in seg:
                            lines.append(seg['text'])

                    if lines:
                        content = '\n'.join(lines)
                        return content[:max_chars]

            # Method 3: Check if we have a cached markdown conversion
            if hasattr(self, '_cached_document_markdown') and self._cached_document_markdown:
                return self._cached_document_markdown[:max_chars]

            # Method 4: Try converting the source document file with markitdown
            if hasattr(self.parent_app, 'current_document_path') and self.parent_app.current_document_path:
                doc_path = Path(self.parent_app.current_document_path)
                if doc_path.exists():
                    # Try to convert with markitdown
                    converted = self._convert_document_to_markdown(doc_path)
                    if converted:
                        # Cache for future use
                        self._cached_document_markdown = converted
                        # Also save to disk for user access
                        self._save_document_markdown(doc_path, converted)
                        return converted[:max_chars]

            return None

        except Exception as e:
            self.log_message(f"⚠ Error getting document content preview: {e}")
            return None

    def _convert_document_to_markdown(self, file_path: Path) -> str:
        """
        Convert a document to markdown using markitdown.

        Args:
            file_path: Path to the document file

        Returns:
            Markdown content or None if conversion fails
        """
        try:
            from markitdown import MarkItDown

            md = MarkItDown()
            result = md.convert(str(file_path))

            if result and hasattr(result, 'text_content'):
                return result.text_content
            elif isinstance(result, str):
                return result

            return None

        except Exception as e:
            self.log_message(f"⚠ Error converting document to markdown: {e}")
            return None

    def _save_document_markdown(self, original_path: Path, markdown_content: str):
        """
        Save the markdown conversion of the current document.

        Saves to: user_data_private/ai_assistant/current_document/

        Args:
            original_path: Original document file path
            markdown_content: Converted markdown content
        """
        try:
            # Create directory for current document markdown
            doc_dir = self.user_data_path / "ai_assistant" / "current_document"
            doc_dir.mkdir(parents=True, exist_ok=True)

            # Create filename based on original
            md_filename = original_path.stem + ".md"
            md_path = doc_dir / md_filename

            # Save markdown content
            md_path.write_text(markdown_content, encoding='utf-8')

            # Save metadata
            metadata = {
                "original_file": str(original_path),
                "original_name": original_path.name,
                "converted_at": datetime.now().isoformat(),
                "markdown_file": str(md_path),
                "size_chars": len(markdown_content)
            }

            meta_path = doc_dir / (original_path.stem + ".meta.json")
            meta_path.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

            self.log_message(f"✓ Saved document markdown: {md_filename}")

        except Exception as e:
            self.log_message(f"⚠ Error saving document markdown: {e}")

    def generate_markdown_for_current_document(self) -> bool:
        """
        Public method to generate markdown for the current document.
        Called by main app when auto-markdown is enabled.

        Returns:
            True if markdown was generated successfully, False otherwise
        """
        try:
            # Check if we have a current document
            if not hasattr(self.parent_app, 'current_document_path') or not self.parent_app.current_document_path:
                return False

            doc_path = Path(self.parent_app.current_document_path)
            if not doc_path.exists():
                return False

            # Convert to markdown
            markdown_content = self._convert_document_to_markdown(doc_path)
            if not markdown_content:
                return False

            # Save markdown and metadata
            self._save_document_markdown(doc_path, markdown_content)

            # Cache for session
            self._cached_document_markdown = markdown_content

            self.log_message(f"✓ Generated markdown for {doc_path.name}")
            return True

        except Exception as e:
            self.log_message(f"⚠ Error generating markdown: {e}")
            return False

    def _get_segment_info(self) -> str:
        """
        Get structured segment information for AI context.

        Returns:
            Formatted string with segment count and ALL segments, or None if no segments available
        """
        try:
            segments = None

            # Try to get segments from parent app (preferred - most current)
            if hasattr(self.parent_app, 'current_project') and self.parent_app.current_project:
                project = self.parent_app.current_project
                if hasattr(project, 'segments') and project.segments:
                    segments = project.segments

            if not segments:
                return None

            total_count = len(segments)

            # Build segment overview
            lines = []
            lines.append(f"- Total segments: {total_count}")

            # Add statistics
            translated_count = sum(1 for seg in segments if seg.target and seg.target.strip())
            lines.append(f"- Translated: {translated_count}/{total_count}")

            # Include ALL segments (up to 500 to stay within token limits)
            # This allows the AI to search and answer questions about the full document
            max_segments = min(500, total_count)
            lines.append(f"\nDocument segments ({max_segments} of {total_count}):")

            for seg in segments[:max_segments]:
                # Use full source text (not truncated) so AI can search for terms
                source_text = seg.source.replace('\n', ' ')  # Normalize newlines
                target_text = ""
                if seg.target:
                    target_text = seg.target.replace('\n', ' ')

                lines.append(f"\nSegment {seg.id}: Source:{source_text}; Target:{target_text}; Status:{seg.status}")

            if total_count > max_segments:
                lines.append(f"\n... and {total_count - max_segments} more segments (not shown)")

            return "\n".join(lines)

        except Exception as e:
            self.log_message(f"⚠ Error getting segment info: {e}")
            return None

    def _send_chat_message(self):
        """Send a chat message to AI"""
        message = self.chat_input.toPlainText().strip()
        if not message:
            return
        
        if not self.llm_client:
            self._add_chat_message(
                "system",
                "⚠ AI Assistant not available. Please configure API keys in Settings."
            )
            return
        
        # Add user message
        self._add_chat_message("user", message)
        self.chat_input.clear()
        
        # Build context for AI
        context = self._build_ai_context(message)
        
        # Send to AI
        self._send_ai_request(context)
    
    def _build_ai_context(self, user_message: str) -> str:
        """Build full context for AI request"""
        parts = []

        # System context
        parts.append("You are an AI assistant for Supervertaler, a professional translation tool.")
        parts.append("\nAVAILABLE RESOURCES:")

        # Current document/project info
        if hasattr(self.parent_app, 'current_project') and self.parent_app.current_project:
            project = self.parent_app.current_project
            project_name = getattr(project, 'name', 'Unnamed Project')
            parts.append(f"- Current Project: {project_name}")

            if hasattr(self.parent_app, 'current_document_path') and self.parent_app.current_document_path:
                doc_path = Path(self.parent_app.current_document_path)
                parts.append(f"- Current Document: {doc_path.name}")
            elif hasattr(project, 'source_file') and project.source_file:
                doc_path = Path(project.source_file)
                parts.append(f"- Current Document: {doc_path.name}")

            # Add language pair info if available
            if hasattr(project, 'source_lang') and hasattr(project, 'target_lang'):
                parts.append(f"- Language Pair: {project.source_lang} → {project.target_lang}")

            # Add segment information if available
            segment_info = self._get_segment_info()
            if segment_info:
                parts.append(f"\nDOCUMENT SEGMENTS:")
                parts.append(segment_info)

            # Add document content preview if available (only if no segments)
            elif not segment_info:
                doc_content = self._get_document_content_preview()
                if doc_content:
                    parts.append(f"\nCURRENT DOCUMENT CONTENT (first 3000 characters):")
                    parts.append(doc_content)

        parts.append(f"- Prompt Library: {len(self.library.prompts)} prompts")
        parts.append(f"- Attached Files: {len(self.attached_files)} files")

        # Add action system instructions (Phase 2)
        parts.append(self.ai_action_system.get_system_prompt_addition())
        
        # Recent conversation (last 5 messages)
        if len(self.chat_history) > 1:
            parts.append("\nRECENT CONVERSATION:")
            for msg in self.chat_history[-5:]:
                if msg['role'] in ['user', 'assistant']:
                    parts.append(f"{msg['role'].upper()}: {msg['content'][:200]}")
        
        # Attached files content
        if self.attached_files:
            parts.append("\nATTACHED FILES CONTENT:")
            for file in self.attached_files[-3:]:  # Last 3 files
                parts.append(f"\n--- {file['name']} ---")
                parts.append(file['content'][:2000])  # First 2000 chars
        
        # User's current message
        parts.append(f"\nUSER QUESTION:\n{user_message}")
        
        return "\n".join(parts)
    
    def refresh_llm_client(self):
        """Refresh LLM client when settings change"""
        self._init_llm_client()

    def _send_ai_request(self, prompt: str, is_analysis: bool = False):
        """Send request to AI and handle response"""
        # Refresh LLM client to get latest provider settings
        self._init_llm_client()

        if not self.llm_client:
            self._add_chat_message(
                "system",
                "⚠ AI Assistant not available. Please configure API keys in Settings."
            )
            return
            
        try:
            # Log the request
            self.log_message(f"[AI Assistant] Sending request to {self.llm_client.provider} ({self.llm_client.model})")
            self.log_message(f"[AI Assistant] Prompt length: {len(prompt)} characters")

            # Show thinking message (don't save to history)
            self._add_chat_message("system", "🤔 Thinking...", save=False)

            # Force UI update
            if hasattr(self, 'chat_display'):
                from PyQt6.QtWidgets import QApplication
                QApplication.processEvents()

            # Call LLM using translate method with custom prompt
            # The translate method accepts a custom_prompt parameter that we can use for any text generation
            self.log_message("[AI Assistant] Calling LLM translate method...")
            response = self.llm_client.translate(
                text="",  # Empty text since we're using custom_prompt
                source_lang="en",
                target_lang="en",
                custom_prompt=prompt
            )

            # Log the response
            self.log_message(f"[AI Assistant] Received response: {len(response) if response else 0} characters")
            if response:
                self.log_message(f"[AI Assistant] Response preview: {response[:200]}...")

            # Clear the thinking message by clearing and reloading history
            self._reload_chat_display()

            # Check if we got a valid response
            if response and response.strip():
                self.log_message("[AI Assistant] Processing response with action system...")
                # Parse and execute actions (Phase 2)
                cleaned_response, action_results = self.ai_action_system.parse_and_execute(response)

                self.log_message(f"[AI Assistant] Cleaned response: {len(cleaned_response)} characters")
                self.log_message(f"[AI Assistant] Actions executed: {len(action_results)}")

                # Add the cleaned response (without ACTION blocks) - only if non-empty
                if cleaned_response and cleaned_response.strip():
                    self._add_chat_message("assistant", cleaned_response)

                # If actions were executed, show results
                if action_results:
                    formatted_results = self.ai_action_system.format_action_results(action_results)
                    self._add_chat_message("system", formatted_results)
                else:
                    # No actions found - show warning with first 500 chars of response for debugging
                    if not (cleaned_response and cleaned_response.strip()):
                        self.log_message(f"[AI Assistant] ⚠ No actions found in response. First 500 chars: {response[:500]}")
                        self._add_chat_message("system", "⚠ AI responded but no actions were found. Check logs for details.")

                # Reload prompt library if any prompts were modified
                if action_results and any(r['action'] in ['create_prompt', 'update_prompt', 'delete_prompt', 'activate_prompt']
                           for r in action_results if r['success']):
                        self.log_message("[AI Assistant] Reloading prompt library due to prompt modifications...")
                        self.library.load_all_prompts()
                        # Refresh tree widget if it exists
                        if hasattr(self, 'tree_widget') and self.tree_widget:
                            self._refresh_tree()
                        # Refresh active prompt display
                        if hasattr(self, '_update_active_prompt_display'):
                            self._update_active_prompt_display()

                self.log_message("[AI Assistant] ✓ Request completed successfully")
            else:
                self.log_message("[AI Assistant] ⚠ Received empty response from AI")
                self._add_chat_message(
                    "system",
                    "⚠ Received empty response from AI. Please try again."
                )

        except Exception as e:
            # Clear the thinking message
            self._reload_chat_display()

            # Log the full error
            import traceback
            error_details = traceback.format_exc()
            self.log_message(f"[AI Assistant] ❌ ERROR: {error_details}")
            print(f"AI Assistant Error:\n{error_details}")  # Also print to console

            self._add_chat_message(
                "system",
                f"⚠ Error communicating with AI: {str(e)}\n\nCheck the log for details."
            )
    
    def _reload_chat_display(self):
        """Reload chat display from history"""
        if not hasattr(self, 'chat_display'):
            return

        # Clear display
        self.chat_display.clear()

        # Reload all messages from history
        for msg in self.chat_history:
            self._add_chat_message(msg['role'], msg['content'], save=False)
    
    def _clear_chat(self):
        """Clear chat history and display"""
        reply = QMessageBox.question(
            None,
            "Clear Chat History",
            "Are you sure you want to clear the entire conversation history?\n\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear history
            self.chat_history = []
            self.attached_files = []
            
            # Save empty history
            self._save_conversation_history()
            
            # Clear display
            if hasattr(self, 'chat_display'):
                self.chat_display.clear()
            
            # Update context sidebar
            self._update_context_sidebar()
            
            # Show confirmation
            self._add_chat_message(
                "system",
                "✨ Chat cleared! Start a new conversation.",
                save=False
            )

    def _show_chat_context_menu(self, position):
        """Show context menu for chat messages to allow copying"""
        item = self.chat_display.itemAt(position)
        if item is None:
            return

        # Get message data
        message_data = item.data(Qt.ItemDataRole.UserRole)
        if not message_data:
            return

        message_text = message_data.get('content', '')

        # Create context menu
        menu = QMenu()

        copy_action = menu.addAction("📋 Copy Message")
        copy_action.triggered.connect(lambda: self._copy_message_to_clipboard(message_text))

        # Show menu at cursor position
        menu.exec(self.chat_display.mapToGlobal(position))

    def _copy_message_to_clipboard(self, text: str):
        """Copy message text to clipboard"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

        # Show brief confirmation
        self._add_chat_message(
            "system",
            "✓ Message copied to clipboard",
            save=False
        )

    def _add_chat_message(self, role: str, message: str, save: bool = True):
        """Add a message to the chat display"""
        # Save to history
        if save:
            self.chat_history.append({
                'role': role,
                'content': message,
                'timestamp': datetime.now().isoformat()
            })
            self._save_conversation_history()

        # Update UI
        if not hasattr(self, 'chat_display'):
            return

        # Create list item with message data
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, {
            'role': role,
            'content': message,
            'timestamp': datetime.now().isoformat()
        })

        # Add to list
        self.chat_display.addItem(item)

        # Scroll to bottom
        self.chat_display.scrollToBottom()
