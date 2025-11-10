"""
Unified Prompt Manager Module - Qt Edition
Simplified 2-Layer Architecture:

1. System Templates (in Settings) - mode-specific, auto-selected based on document type
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
    QListWidget, QListWidgetItem, QStyledItemDelegate, QStyleOptionViewItem, QApplication, QDialog
)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QThread, QSize, QRect, QRectF
from PyQt6.QtGui import QFont, QColor, QAction, QIcon, QPainter, QPen, QBrush, QPainterPath, QLinearGradient

from modules.unified_prompt_library import UnifiedPromptLibrary
from modules.llm_clients import LLMClient, load_api_keys
from modules.prompt_library_migration import migrate_prompt_library
from modules.ai_attachment_manager import AttachmentManager
from modules.ai_file_viewer_dialog import FileViewerDialog, FileRemoveConfirmDialog
from modules.ai_actions import AIActionSystem


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
    - Favorites and Quick Run menu
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
        self.prompt_library_dir = self.user_data_path / "Prompt_Library"
        # Use Prompt_Library directly, not Prompt_Library/Library
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
        
        # System Templates (stored separately, loaded from settings/files)
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
        ai_assistant_dir = self.user_data_path / "AI_Assistant"
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

        # Tab 1: Prompt Library
        library_tab = self._create_prompt_library_tab()
        self.sub_tabs.addTab(library_tab, "📚 Prompt Library")

        # Tab 2: AI Assistant (placeholder for now)
        assistant_tab = self._create_ai_assistant_tab()
        self.sub_tabs.addTab(assistant_tab, "✨ AI Assistant")

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
        title = QLabel("🤖 Prompt Manager")
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
        
        # Toolbar for Prompt Library
        toolbar = self._create_library_toolbar()
        layout.addWidget(toolbar, 0)
        
        # Main content: Horizontal splitter with tree view and editor/config
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(3)
        
        # Left: Prompt Library Tree
        left_panel = self._create_library_tree_panel()
        left_panel.setMinimumWidth(250)
        splitter.addWidget(left_panel)
        
        # Right: Active Config + Editor (with vertical splitter inside)
        right_panel = self._create_right_panel()
        right_panel.setMinimumWidth(300)
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (35% tree, 65% config+editor)
        splitter.setSizes([350, 650])
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter, 1)
        
        # Load initial tree content
        self._refresh_tree()
        
        return tab
    
    def _create_library_toolbar(self) -> QWidget:
        """Create toolbar for Prompt Library tab"""
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 5)
        toolbar_layout.setSpacing(5)
        
        # Mode indicator
        self.mode_label = QLabel(f"• Mode: {self._get_mode_display_name()}")
        self.mode_label.setStyleSheet("color: #666; font-size: 9pt;")
        toolbar_layout.addWidget(self.mode_label)
        
        toolbar_layout.addStretch()
        
        btn_new = QPushButton("+ New")
        btn_new.clicked.connect(self._new_prompt)
        toolbar_layout.addWidget(btn_new)
        
        btn_folder = QPushButton("📁 New Folder")
        btn_folder.clicked.connect(self._new_folder)
        toolbar_layout.addWidget(btn_folder)
        
        btn_settings = QPushButton("⚙️ System Templates")
        btn_settings.clicked.connect(self._open_system_templates_settings)
        btn_settings.setToolTip("Configure mode-specific templates (Settings)")
        toolbar_layout.addWidget(btn_settings)
        
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.clicked.connect(self._refresh_library)
        toolbar_layout.addWidget(btn_refresh)
        
        return toolbar
    
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
        
        btn_settings = QPushButton("⚙️ System Templates")
        btn_settings.clicked.connect(self._open_system_templates_settings)
        btn_settings.setToolTip("Configure mode-specific templates (Settings)")
        toolbar_layout.addWidget(btn_settings)
        
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.clicked.connect(self._refresh_library)
        toolbar_layout.addWidget(btn_refresh)
        
        toolbar_layout.addStretch()
        
        layout.addWidget(toolbar, 0)
        
        return header_container
    
    def _create_library_tree_panel(self) -> QWidget:
        """Create left panel with folder tree"""
        panel = QWidget()
        panel.setMinimumHeight(450)  # Ensure tree doesn't collapse on big screens
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tree widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Prompt Library"])
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.itemClicked.connect(self._on_tree_item_clicked)
        self.tree_widget.itemDoubleClicked.connect(self._on_tree_item_double_clicked)
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self._show_tree_context_menu)
        
        layout.addWidget(self.tree_widget)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Create right panel with active configuration and editor - vertically splittable"""
        # Use a vertical splitter so user can resize Active Config vs Editor
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Active Configuration Panel (top)
        config_group = self._create_active_config_panel()
        config_group.setMinimumHeight(200)  # Minimum height to prevent collapsing
        splitter.addWidget(config_group)
        
        # Editor (bottom - for viewing/editing selected prompt)
        editor_group = self._create_editor_panel()
        editor_group.setMinimumHeight(250)  # Minimum height for editor
        splitter.addWidget(editor_group)
        
        # Set initial sizes: 35% Active Config, 65% Editor
        splitter.setSizes([350, 650])
        
        return splitter
    
    def _create_active_config_panel(self) -> QGroupBox:
        """Create active prompt configuration panel"""
        group = QGroupBox("Active Configuration")
        layout = QVBoxLayout()
        
        # Mode info (read-only, auto-selected)
        mode_frame = QFrame()
        mode_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        mode_layout = QHBoxLayout(mode_frame)
        mode_layout.setContentsMargins(10, 5, 10, 5)
        
        mode_label = QLabel(f"🔧 Current Mode: {self._get_mode_display_name()}")
        mode_label.setFont(QFont("Segoe UI", 9))
        mode_layout.addWidget(mode_label)
        
        btn_view_template = QPushButton("View System Template")
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
        self.attached_list_widget.setMaximumHeight(120)
        self.attached_list_widget.setRootIsDecorated(False)
        self.attached_list_widget.setColumnWidth(0, 200)
        layout.addWidget(self.attached_list_widget)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        btn_preview = QPushButton("Preview Combined")
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
        self.tree_widget.clear()
        
        # Debug: Show what we have
        self.log_message(f"🔍 DEBUG: Refreshing tree with {len(self.library.prompts)} prompts")
        self.log_message(f"🔍 DEBUG: Library dir: {self.unified_library_dir}")
        self.log_message(f"🔍 DEBUG: Library dir exists: {self.unified_library_dir.exists()}")
        
        # Favorites section
        favorites_root = QTreeWidgetItem(["⭐ Favorites"])
        favorites_root.setExpanded(True)
        font = favorites_root.font(0)
        font.setBold(True)
        favorites_root.setFont(0, font)
        self.tree_widget.addTopLevelItem(favorites_root)
        
        favorites = self.library.get_favorites()
        self.log_message(f"🔍 DEBUG: Favorites count: {len(favorites)}")
        for path, name in favorites:
            item = QTreeWidgetItem([name])
            item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'prompt', 'path': path})
            favorites_root.addChild(item)
        
        # Quick Run section
        quick_run_root = QTreeWidgetItem(["🚀 Quick Run Menu"])
        quick_run_root.setExpanded(True)
        font = quick_run_root.font(0)
        font.setBold(True)
        quick_run_root.setFont(0, font)
        self.tree_widget.addTopLevelItem(quick_run_root)
        
        quick_run = self.library.get_quick_run_prompts()
        self.log_message(f"🔍 DEBUG: Quick Run count: {len(quick_run)}")
        for path, name in quick_run:
            item = QTreeWidgetItem([name])
            item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'prompt', 'path': path})
            quick_run_root.addChild(item)
        
        # Library folders
        self.log_message(f"🔍 DEBUG: Building tree from {self.unified_library_dir}")
        self._build_tree_recursive(None, self.unified_library_dir, "")
        
        # Debug: Check what's in the tree
        self.log_message(f"🔍 DEBUG: Tree has {self.tree_widget.topLevelItemCount()} top-level items")
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            text = item.text(0)
            child_count = item.childCount()
            self.log_message(f"🔍 DEBUG: Top-level item {i}: '{text}' with {child_count} children")
        
        # Expand all folders so prompts are visible
        self.tree_widget.expandAll()
        self.log_message(f"🔍 DEBUG: Called expandAll() on tree")
    
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
                
                if parent_item:
                    parent_item.addChild(folder_item)
                else:
                    self.tree_widget.addTopLevelItem(folder_item)
                
                self.log_message(f"🔍 DEBUG: Added folder: {item.name} (path: {rel_path})")
                
                # Recurse
                self._build_tree_recursive(folder_item, item, rel_path)
            
            elif item.suffix.lower() in ['.md', '.txt']:
                # Prompt file
                rel_path = str(Path(relative_path) / item.name) if relative_path else item.name
                
                self.log_message(f"🔍 DEBUG: Checking prompt file: {rel_path}")
                self.log_message(f"🔍 DEBUG: In library.prompts? {rel_path in self.library.prompts}")
                
                # Show first few keys for comparison
                if len(self.library.prompts) > 0:
                    sample_keys = list(self.library.prompts.keys())[:3]
                    self.log_message(f"🔍 DEBUG: Sample keys: {sample_keys}")
                
                if rel_path in self.library.prompts:
                    prompt_data = self.library.prompts[rel_path]
                    name = prompt_data.get('name', item.stem)
                    
                    prompt_item = QTreeWidgetItem([name])
                    prompt_item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'prompt', 'path': rel_path})
                    
                    # Visual indicators
                    if prompt_data.get('favorite'):
                        prompt_item.setText(0, f"⭐ {name}")
                    if prompt_data.get('quick_run'):
                        prompt_item.setText(0, f"🚀 {name}")
                    
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
            
            # Toggle quick run
            if prompt_data.get('quick_run'):
                action_qr = menu.addAction("Remove from Quick Run")
            else:
                action_qr = menu.addAction("Add to Quick Run")
            action_qr.triggered.connect(lambda: self._toggle_quick_run(path))
            
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
        
        self.editor_name_label.setText(f"Editing: {prompt_data.get('name', 'Unnamed')}")
        self.editor_name_input.setText(prompt_data.get('name', ''))
        self.editor_desc_input.setText(prompt_data.get('description', ''))
        self.editor_content.setPlainText(prompt_data.get('content', ''))
        
        # Store current path for saving
        self.editor_current_path = relative_path
        self.btn_save_prompt.setEnabled(True)
    
    def _save_current_prompt(self):
        """Save currently edited prompt"""
        if not hasattr(self, 'editor_current_path'):
            return
        
        path = self.editor_current_path
        if path not in self.library.prompts:
            return
        
        prompt_data = self.library.prompts[path].copy()
        prompt_data['name'] = self.editor_name_input.text()
        prompt_data['description'] = self.editor_desc_input.text()
        prompt_data['content'] = self.editor_content.toPlainText()
        prompt_data['modified'] = Path(prompt_data['_filepath']).stat().st_mtime
        
        if self.library.save_prompt(path, prompt_data):
            QMessageBox.information(self.main_widget, "Saved", "Prompt saved successfully!")
            self._refresh_library()
        else:
            QMessageBox.warning(self.main_widget, "Error", "Failed to save prompt")
    
    def _set_primary_prompt(self, relative_path: str):
        """Set prompt as primary"""
        if self.library.set_primary_prompt(relative_path):
            prompt_data = self.library.prompts[relative_path]
            self.primary_prompt_label.setText(prompt_data.get('name', 'Unnamed'))
            self.primary_prompt_label.setStyleSheet("color: #000; font-weight: bold;")
            self.log_message(f"✓ Set primary: {prompt_data.get('name')}")
    
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
        """Toggle quick run status"""
        if self.library.toggle_quick_run(relative_path):
            self._refresh_tree()
    
    def _new_prompt(self):
        """Create new prompt"""
        name, ok = QInputDialog.getText(self.main_widget, "New Prompt", "Enter prompt name:")
        if ok and name:
            # TODO: Implement new prompt creation
            self.log_message(f"TODO: Create new prompt: {name}")
    
    def _new_folder(self):
        """Create new folder"""
        name, ok = QInputDialog.getText(self.main_widget, "New Folder", "Enter folder name:")
        if ok and name:
            if self.library.create_folder(name):
                self._refresh_tree()
    
    def _new_prompt_in_folder(self, folder_path: str):
        """Create new prompt in specific folder"""
        # TODO: Implement
        self.log_message(f"TODO: Create prompt in {folder_path}")
    
    def _new_subfolder(self, parent_folder: str):
        """Create subfolder"""
        name, ok = QInputDialog.getText(self.main_widget, "New Subfolder", "Enter folder name:")
        if ok and name:
            full_path = str(Path(parent_folder) / name)
            if self.library.create_folder(full_path):
                self._refresh_tree()
    
    def _duplicate_prompt(self, relative_path: str):
        """Duplicate a prompt"""
        # TODO: Implement
        self.log_message(f"TODO: Duplicate {relative_path}")
    
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
        """Preview the combined prompt"""
        combined = self.build_final_prompt("{{SOURCE_TEXT}}", "Source Lang", "Target Lang")
        
        # Show in dialog
        dialog = QMessageBox(self.main_widget)
        dialog.setWindowTitle("Combined Prompt Preview")
        dialog.setText("This is how prompts will be combined:")
        dialog.setDetailedText(combined)
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.exec()
    
    def _view_current_system_template(self):
        """View the current system template"""
        template = self.get_system_template(self.current_mode)
        
        dialog = QMessageBox(self.main_widget)
        dialog.setWindowTitle(f"System Template: {self._get_mode_display_name()}")
        dialog.setText(f"Current system template for {self._get_mode_display_name()} mode:")
        dialog.setDetailedText(template)
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.exec()
    
    def _open_system_templates_settings(self):
        """Open system templates in settings"""
        # Navigate to Settings tab if main app has the method
        if hasattr(self.app, 'right_tabs') and hasattr(self.app, 'settings_tabs'):
            # Navigate to Settings tab (index 3)
            self.app.right_tabs.setCurrentIndex(3)
            # Navigate to System Prompts sub-tab (index 5 - after General, LLM, Language, MT, View)
            self.app.settings_tabs.setCurrentIndex(5)
        else:
            # Fallback message
            QMessageBox.information(
                self.main_widget,
                "System Templates",
                "System Templates (Layer 1) are configured in Settings → System Prompts tab.\n\n"
                "They are automatically selected based on the document type you're processing."
            )
    
    # === System Templates Management ===
    
    def _load_system_templates(self):
        """Load system templates from files"""
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
        """Get default system template for a mode"""
        # Use the same default as before
        return """# SYSTEM TEMPLATE

⚠️ **PROFESSIONAL TRANSLATION CONTEXT:**
You are performing professional technical/medical translation as a licensed service for a commercial translation company.

You are an expert {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}} translator.

**YOUR TASK**: Translate the text below.

**CRITICAL: CAT TOOL TAG PRESERVATION**:
- Preserve ALL formatting tags (memoQ: [1}, {2]; Trados: <410></410>; CafeTran: |text|)
- Never translate, omit, or modify tags - only reposition appropriately

{{SOURCE_LANGUAGE}} text:
{{SOURCE_TEXT}}"""
    
    def get_system_template(self, mode: str) -> str:
        """Get system template for specified mode"""
        return self.system_templates.get(mode, self._get_default_system_template(mode))
    
    def set_mode(self, mode: str):
        """Set current translation mode (single, batch_docx, batch_bilingual)"""
        if mode in ["single", "batch_docx", "batch_bilingual"]:
            self.current_mode = mode
            if hasattr(self, 'mode_label'):
                self.mode_label.setText(f"Mode: {self._get_mode_display_name()}")
    
    # === Prompt Composition (for translation) ===
    
    def build_final_prompt(self, source_text: str, source_lang: str, target_lang: str, mode: str = None) -> str:
        """
        Build final prompt for translation using 2-layer architecture:
        1. System Template (auto-selected by mode)
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
        
        # Layer 1: System Template
        system_template = self.get_system_template(mode)
        
        # Replace placeholders in system template
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
            api_keys = load_api_keys()
            
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
                elif api_keys.get("google"):
                    provider = "gemini"
            
            if provider:
                api_key = api_keys.get(provider) or api_keys.get("openai") or api_keys.get("claude") or api_keys.get("google")
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

Your task: Create a translation prompt for this project.

Output format - TWO complete ACTION blocks (no truncation):

ACTION:create_prompt PARAMS:{{"name": "[Name based on document]", "content": "[Full prompt with glossary]", "folder": "Project Prompts", "description": "Auto-generated"}}
ACTION:activate_prompt PARAMS:{{"path": "Project Prompts/[Name based on document].md", "mode": "primary"}}

Prompt structure to use:
# Translation Prompt: [Domain] [Languages]

## Document Summary
[2-3 paragraphs about the document]

## Key Terminology
| Source | Target | Notes |
|--------|--------|-------|
[20+ terms from document]

## Translation Guidelines
- Preserve all formatting
- Follow glossary exactly
- One segment per line

CRITICAL: Output BOTH actions complete. Do NOT truncate."""
        
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

        Saves to: user_data_private/AI_Assistant/current_document/

        Args:
            original_path: Original document file path
            markdown_content: Converted markdown content
        """
        try:
            # Create directory for current document markdown
            doc_dir = self.user_data_path / "AI_Assistant" / "current_document"
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
            Formatted string with segment count and sample segments, or None if no segments available
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

            # Add sample segments (first 10)
            sample_count = min(10, total_count)
            lines.append(f"\nFirst {sample_count} segments (use segment numbers to reference specific segments):")

            for i, seg in enumerate(segments[:sample_count], 1):
                source_preview = seg.source[:80] + "..." if len(seg.source) > 80 else seg.source
                target_preview = ""
                if seg.target:
                    target_preview = seg.target[:80] + "..." if len(seg.target) > 80 else seg.target

                lines.append(f"\n  Segment {seg.id}:")
                lines.append(f"    Source: {source_preview}")
                if target_preview:
                    lines.append(f"    Target: {target_preview}")
                lines.append(f"    Status: {seg.status}")

            if total_count > sample_count:
                lines.append(f"\n  ... and {total_count - sample_count} more segments")

            lines.append("\nNOTE: You can access individual segments by their segment number.")
            lines.append("Use get_segment_info action to retrieve details of specific segments.")

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

                    # Reload prompt library if any prompts were modified
                    if any(r['action'] in ['create_prompt', 'update_prompt', 'delete_prompt', 'activate_prompt']
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
