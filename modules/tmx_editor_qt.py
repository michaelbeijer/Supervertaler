"""
TMX Editor Module - PyQt6 Edition

Professional Translation Memory Editor for Qt version of Supervertaler.
Based on the tkinter version, converted to PyQt6.

Key Features:
- Dual-language grid editor (source/target columns)
- Fast filtering by language, content, status
- In-place editing with validation
- TMX file validation and repair
- Header metadata editing
- Large file support with pagination
- Import/Export multiple formats
- Multi-language support (view any language pair)

Reuses core logic from tmx_editor.py (TmxFile, TmxParser, data classes)
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QFileDialog,
    QMessageBox, QDialog, QDialogButtonBox, QFormLayout, QListWidget,
    QFrame, QMenu, QGroupBox, QHeaderView, QCheckBox, QStyledItemDelegate,
    QAbstractItemView, QStyleOptionViewItem, QStyle, QStyleOptionButton,
    QRadioButton, QProgressDialog, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPointF
from PyQt6.QtGui import QColor, QKeySequence, QShortcut, QContextMenuEvent, QPainter, QFontMetrics, QPen, QPolygonF
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

# Import core logic from tkinter version (framework-agnostic)
from modules.tmx_editor import (
    TmxFile, TmxParser, TmxTranslationUnit, TmxSegment, TmxHeader
)


class CheckmarkCheckBox(QCheckBox):
    """Custom checkbox with green background and white checkmark when checked - same as AutoFingers"""
    
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
                
                # Checkmark path: bottom-left to middle, then middle to top-right
                check_x1 = x + w * 0.10
                check_y1 = y + h * 0.50
                check_x2 = x + w * 0.35
                check_y2 = y + h * 0.70
                check_x3 = x + w * 0.90
                check_y3 = y + h * 0.25
                
                checkmark = QPolygonF([
                    QPointF(check_x1, check_y1),
                    QPointF(check_x2, check_y2),
                    QPointF(check_x3, check_y3)
                ])
                painter.drawPolyline(checkmark)
                painter.end()


class HighlightDelegate(QStyledItemDelegate):
    """Custom delegate to highlight filter text in table cells"""
    
    def __init__(self, parent=None, column: int = 1):
        super().__init__(parent)
        self.column = column  # Column index (1 = Source, 2 = Target)
        self.highlight_text = ""
        self.ignore_case = True
    
    def set_highlight(self, text: str, ignore_case: bool = True):
        """Set the text to highlight"""
        self.highlight_text = text
        self.ignore_case = ignore_case
    
    def paint(self, painter, option, index):
        """Paint the cell with highlighted text"""
        text = index.data(Qt.ItemDataRole.DisplayRole) or ""
        
        if not self.highlight_text or not text:
            # No highlighting needed, use default painting
            super().paint(painter, option, index)
            return
        
        # Get the rect and text
        rect = option.rect
        painter.save()
        
        # Draw background if selected (check if Selected flag is set)
        is_selected = bool(option.state & QStyle.StateFlag.State_Selected)
        if is_selected:
            painter.fillRect(rect, option.palette.highlight())
            painter.setPen(option.palette.highlightedText().color())
        else:
            painter.setPen(option.palette.text().color())
        
        # Find all occurrences of highlight text
        search_text = self.highlight_text
        display_text = text
        if self.ignore_case:
            search_text = search_text.lower()
            display_text = text.lower()
        
        # Draw text with highlighting
        fm = QFontMetrics(painter.font())
        x = rect.left() + 2
        y = rect.top() + fm.ascent() + 2
        
        # Find all match positions
        matches = []
        start = 0
        while True:
            pos = display_text.find(search_text, start)
            if pos == -1:
                break
            matches.append((pos, pos + len(search_text)))
            start = pos + 1
        
        # Draw text segments with highlighting
        last_pos = 0
        for start_pos, end_pos in matches:
            # Draw text before match
            if start_pos > last_pos:
                before_text = text[last_pos:start_pos]
                painter.drawText(x, y, before_text)
                x += fm.horizontalAdvance(before_text)
            
            # Draw highlighted match
            match_text = text[start_pos:end_pos]
            # Reduce highlight height to be more compact (just around the text baseline)
            text_height = fm.height()  # Full font height (ascent + descent)
            highlight_height = int(text_height * 0.7)  # Make it 70% of font height for tighter fit
            highlight_y = y - fm.ascent() + (fm.ascent() - highlight_height) // 2  # Center vertically on text
            highlight_rect = QRect(x, highlight_y, fm.horizontalAdvance(match_text), highlight_height)
            painter.fillRect(highlight_rect, QColor("#90EE90"))  # Light green like Heartsome
            painter.drawText(x, y, match_text)
            x += fm.horizontalAdvance(match_text)
            
            last_pos = end_pos
        
        # Draw remaining text
        if last_pos < len(text):
            remaining_text = text[last_pos:]
            painter.drawText(x, y, remaining_text)
        
        painter.restore()


class TmxEditorUIQt(QWidget):
    """TMX Editor user interface - PyQt6 version"""
    
    def __init__(self, parent=None, standalone=False, db_manager=None):
        """
        Initialize TMX Editor UI
        
        Args:
            parent: Parent widget (None for standalone window)
            standalone: If True, creates own window. If False, embeds in parent
            db_manager: DatabaseManager instance for database-backed TMX files (optional)
        """
        super().__init__(parent)
        self.db_manager = db_manager  # Database manager for database mode
        self.tmx_file: Optional[TmxFile] = None
        self.tmx_file_id: Optional[int] = None  # Database file ID when in database mode
        self.load_mode: str = "ram"  # "ram" or "database"
        self.current_page = 0
        self.items_per_page = 50
        self.filtered_tus: List[TmxTranslationUnit] = []
        self.src_lang = ""
        self.tgt_lang = ""
        self.filter_source = ""
        self.filter_target = ""
        self.standalone = standalone
        self.current_edit_tu: Optional[TmxTranslationUnit] = None
        self.tu_row_map: Dict[int, TmxTranslationUnit] = {}  # Maps table row to TU
        
        # Create highlight delegates for text highlighting (one per column)
        self.highlight_delegate_source = HighlightDelegate(self, column=1)
        self.highlight_delegate_target = HighlightDelegate(self, column=2)
        
        self.setup_ui()
        
        if standalone:
            self.setWindowTitle("TMX Editor - Supervertaler")
            self.resize(1200, 700)
    
    def setup_ui(self):
        """Create the user interface - Heartsome-style layout"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Toolbar
        self.create_toolbar(main_layout)
        
        # Top header panel: Language Pair and Search Filter (Heartsome style)
        self.create_top_header_panel(main_layout)
        
        # Main content area with splitter (grid center, attributes right)
        from PyQt6.QtWidgets import QSplitter
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Center panel: Grid editor
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        
        # Grid editor
        self.create_grid_editor(center_layout)
        
        # Pagination controls
        self.create_pagination_controls(center_layout)
        
        content_splitter.addWidget(center_panel)
        content_splitter.setStretchFactor(0, 1)
        
        # Right panel: Attributes Editor
        right_panel = self.create_attributes_editor()
        content_splitter.addWidget(right_panel)
        content_splitter.setStretchFactor(1, 0)
        content_splitter.setSizes([1000, 300])  # Initial widths
        
        main_layout.addWidget(content_splitter)
        
        # Status bar
        self.create_status_bar(main_layout)
    
    def create_toolbar(self, parent_layout):
        """Create toolbar with common actions"""
        toolbar = QFrame()
        toolbar.setFrameStyle(QFrame.Shape.Box)
        toolbar.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        
        # File operations
        btn_new = QPushButton("📁 New")
        btn_new.clicked.connect(self.new_tmx)
        toolbar_layout.addWidget(btn_new)
        
        btn_open = QPushButton("📂 Open")
        btn_open.clicked.connect(self.open_tmx)
        toolbar_layout.addWidget(btn_open)
        
        btn_save = QPushButton("💾 Save")
        btn_save.clicked.connect(self.save_tmx)
        toolbar_layout.addWidget(btn_save)
        
        btn_save_as = QPushButton("💾 Save As...")
        btn_save_as.clicked.connect(self.save_tmx_as)
        toolbar_layout.addWidget(btn_save_as)
        
        btn_close = QPushButton("❌ Close")
        btn_close.clicked.connect(self.close_tmx)
        toolbar_layout.addWidget(btn_close)
        
        toolbar_layout.addWidget(QFrame())  # Spacer
        
        # Edit operations
        btn_add = QPushButton("➕ Add TU")
        btn_add.clicked.connect(self.add_translation_unit)
        toolbar_layout.addWidget(btn_add)
        
        btn_delete = QPushButton("❌ Delete")
        btn_delete.clicked.connect(self.delete_selected_tu)
        toolbar_layout.addWidget(btn_delete)
        
        toolbar_layout.addWidget(QFrame())  # Spacer
        
        # View operations
        btn_header = QPushButton("ℹ️ Header")
        btn_header.clicked.connect(self.edit_header)
        toolbar_layout.addWidget(btn_header)
        
        btn_stats = QPushButton("📊 Stats")
        btn_stats.clicked.connect(self.show_statistics)
        toolbar_layout.addWidget(btn_stats)
        
        btn_validate = QPushButton("✓ Validate")
        btn_validate.clicked.connect(self.validate_tmx)
        toolbar_layout.addWidget(btn_validate)
        
        toolbar_layout.addStretch()
        parent_layout.addWidget(toolbar)
    
    def create_top_header_panel(self, parent_layout):
        """Create top header panel with Language Pair and Search Filter - Heartsome style"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.Box)
        header_frame.setStyleSheet("background-color: #fffacd; padding: 5px; border: 1px solid #d0d0d0;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 5, 10, 5)
        header_layout.setSpacing(15)
        
        # Language Pair section
        lang_label = QLabel("Source:")
        lang_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(lang_label)
        
        self.src_lang_combo = QComboBox()
        self.src_lang_combo.setMinimumWidth(100)
        self.src_lang_combo.currentTextChanged.connect(self.on_language_changed)
        header_layout.addWidget(self.src_lang_combo)
        
        lang_label2 = QLabel("Target:")
        lang_label2.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(lang_label2)
        
        self.tgt_lang_combo = QComboBox()
        self.tgt_lang_combo.setMinimumWidth(100)
        self.tgt_lang_combo.currentTextChanged.connect(self.on_language_changed)
        header_layout.addWidget(self.tgt_lang_combo)
        
        # Spacer
        header_layout.addSpacing(20)
        
        # Filter section
        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(filter_label)
        
        # Source search
        self.src_search_label = QLabel(f"Source: {self.src_lang if self.src_lang else 'en'}")
        header_layout.addWidget(self.src_search_label)
        self.filter_source_entry = QLineEdit()
        self.filter_source_entry.setPlaceholderText("Enter source text")
        self.filter_source_entry.setMinimumWidth(150)
        self.filter_source_entry.returnPressed.connect(self.apply_filters)
        header_layout.addWidget(self.filter_source_entry)
        
        # Target search
        self.tgt_search_label = QLabel(f"Target: {self.tgt_lang if self.tgt_lang else 'nl'}")
        header_layout.addWidget(self.tgt_search_label)
        self.filter_target_entry = QLineEdit()
        self.filter_target_entry.setPlaceholderText("Enter target text")
        self.filter_target_entry.setMinimumWidth(150)
        self.filter_target_entry.returnPressed.connect(self.apply_filters)
        header_layout.addWidget(self.filter_target_entry)
        
        # Filter dropdown
        self.filter_all_segments = QComboBox()
        self.filter_all_segments.addItems(["All Segments"])
        self.filter_all_segments.setMinimumWidth(120)
        header_layout.addWidget(self.filter_all_segments)
        
        # Search button
        btn_apply = QPushButton("Search")
        btn_apply.clicked.connect(self.apply_filters)
        btn_apply.setStyleSheet("background-color: #ff9800; color: white; padding: 4px 8px; font-size: 9pt;")
        header_layout.addWidget(btn_apply)
        
        # Checkboxes - use custom CheckmarkCheckBox style like AutoFingers
        self.filter_ignore_case = CheckmarkCheckBox("Ignore case")
        self.filter_ignore_case.setChecked(True)
        header_layout.addWidget(self.filter_ignore_case)
        
        self.filter_ignore_tags = CheckmarkCheckBox("Ignore tags")
        header_layout.addWidget(self.filter_ignore_tags)
        
        # Clear button
        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_filters)
        btn_clear.setStyleSheet("background-color: #9e9e9e; color: white; padding: 4px 8px; font-size: 9pt;")
        header_layout.addWidget(btn_clear)
        
        header_layout.addStretch()
        
        parent_layout.addWidget(header_frame)
    
    def create_language_panel(self, parent_layout):
        """Create language selection panel - compact version for sidebar"""
        lang_frame = QGroupBox("Language Pair")
        lang_frame.setStyleSheet("background-color: #e8f4f8; padding: 5px;")
        lang_layout = QVBoxLayout(lang_frame)
        lang_layout.setContentsMargins(5, 5, 5, 5)
        
        src_layout = QHBoxLayout()
        src_layout.addWidget(QLabel("Source:"))
        self.src_lang_combo = QComboBox()
        self.src_lang_combo.setMinimumWidth(120)
        self.src_lang_combo.currentTextChanged.connect(self.on_language_changed)
        src_layout.addWidget(self.src_lang_combo)
        lang_layout.addLayout(src_layout)
        
        tgt_layout = QHBoxLayout()
        tgt_layout.addWidget(QLabel("Target:"))
        self.tgt_lang_combo = QComboBox()
        self.tgt_lang_combo.setMinimumWidth(120)
        self.tgt_lang_combo.currentTextChanged.connect(self.on_language_changed)
        tgt_layout.addWidget(self.tgt_lang_combo)
        lang_layout.addLayout(tgt_layout)
        
        btn_all_langs = QPushButton("🌐 All Languages")
        btn_all_langs.clicked.connect(self.show_all_languages)
        btn_all_langs.setStyleSheet("background-color: #4CAF50; color: white; padding: 3px; font-size: 9pt;")
        lang_layout.addWidget(btn_all_langs)
        
        parent_layout.addWidget(lang_frame)
    
    def create_filter_panel(self, parent_layout):
        """Create filter panel - Heartsome style"""
        filter_frame = QGroupBox("🔍 Search & Filter")
        filter_frame.setStyleSheet("background-color: #fff3cd; padding: 5px;")
        filter_layout = QVBoxLayout(filter_frame)
        filter_layout.setContentsMargins(5, 5, 5, 5)
        
        # Search section
        search_layout = QVBoxLayout()
        
        src_search_layout = QHBoxLayout()
        src_search_layout.addWidget(QLabel(f"Source: {self.src_lang if self.src_lang else 'en'}"))
        self.filter_source_entry = QLineEdit()
        self.filter_source_entry.setPlaceholderText("Enter source for search")
        self.filter_source_entry.returnPressed.connect(self.apply_filters)
        src_search_layout.addWidget(self.filter_source_entry)
        search_layout.addLayout(src_search_layout)
        
        tgt_search_layout = QHBoxLayout()
        tgt_search_layout.addWidget(QLabel(f"Target: {self.tgt_lang if self.tgt_lang else 'nl'}"))
        self.filter_target_entry = QLineEdit()
        self.filter_target_entry.setPlaceholderText("Enter translation for search")
        self.filter_target_entry.returnPressed.connect(self.apply_filters)
        tgt_search_layout.addWidget(self.filter_target_entry)
        search_layout.addLayout(tgt_search_layout)
        
        btn_apply = QPushButton("Search")
        btn_apply.clicked.connect(self.apply_filters)
        btn_apply.setStyleSheet("background-color: #ff9800; color: white; padding: 3px; font-size: 9pt;")
        search_layout.addWidget(btn_apply)
        
        filter_layout.addLayout(search_layout)
        
        # Filter options
        filter_options_layout = QVBoxLayout()
        
        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet("font-weight: bold;")
        filter_options_layout.addWidget(filter_label)
        
        self.filter_all_segments = QComboBox()
        self.filter_all_segments.addItems(["All Segments"])
        filter_options_layout.addWidget(self.filter_all_segments)
        
        self.filter_ignore_case = QCheckBox("✔ Ignore case")
        self.filter_ignore_case.setChecked(True)
        filter_options_layout.addWidget(self.filter_ignore_case)
        
        self.filter_ignore_tags = QCheckBox("Ignore tags")
        filter_options_layout.addWidget(self.filter_ignore_tags)
        
        filter_layout.addLayout(filter_options_layout)
        
        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_filters)
        btn_clear.setStyleSheet("background-color: #9e9e9e; color: white; padding: 3px; font-size: 9pt;")
        filter_layout.addWidget(btn_clear)
        
        parent_layout.addWidget(filter_frame)
    
    def create_grid_editor(self, parent_layout):
        """Create grid editor for translation units using QTableWidget - Heartsome style"""
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # No., Source, Target, System Attributes
        self.table.setHorizontalHeaderLabels(['No.', 'Source', 'Target', 'System Attributes'])
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # No. column fixed
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Source stretch
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Target stretch
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Attributes fixed
        self.table.setColumnWidth(0, 50)  # No. column
        self.table.setColumnWidth(3, 120)  # System Attributes column
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
            }
            QTableWidget::item {
                padding: 2px;
            }
            QTableWidget::item:selected {
                background-color: #add8e6;  /* Light blue for selected row */
            }
        """)
        
        # Enable inline editing for Source and Target columns (columns 1 and 2)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked | 
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )
        
        # Set highlight delegates for Source and Target columns
        self.table.setItemDelegateForColumn(1, self.highlight_delegate_source)  # Source column
        self.table.setItemDelegateForColumn(2, self.highlight_delegate_target)  # Target column
        
        # Enable word wrap
        self.table.setWordWrap(True)
        
        # Connect signals
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)
        self.table.itemDoubleClicked.connect(self.on_table_double_clicked)
        self.table.itemChanged.connect(self.on_cell_edited)  # Handle cell edits
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        parent_layout.addWidget(self.table)
    
    def create_pagination_controls(self, parent_layout):
        """Create pagination controls"""
        page_frame = QFrame()
        page_frame.setFrameStyle(QFrame.Shape.Box)
        page_frame.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        page_layout = QHBoxLayout(page_frame)
        page_layout.setContentsMargins(10, 5, 10, 5)
        
        self.page_label = QLabel("Page 0 of 0 (0 TUs)")
        page_layout.addWidget(self.page_label)
        
        page_layout.addStretch()
        
        # Navigation buttons
        btn_first = QPushButton("⏮️ First")
        btn_first.clicked.connect(self.first_page)
        page_layout.addWidget(btn_first)
        
        btn_prev = QPushButton("◀️ Prev")
        btn_prev.clicked.connect(self.prev_page)
        page_layout.addWidget(btn_prev)
        
        btn_next = QPushButton("Next ▶️")
        btn_next.clicked.connect(self.next_page)
        page_layout.addWidget(btn_next)
        
        btn_last = QPushButton("Last ⏭️")
        btn_last.clicked.connect(self.last_page)
        page_layout.addWidget(btn_last)
        
        parent_layout.addWidget(page_frame)
    
    def create_attributes_editor(self) -> QWidget:
        """Create Attributes Editor panel (right side) - Heartsome style"""
        attributes_panel = QWidget()
        attributes_layout = QVBoxLayout(attributes_panel)
        attributes_layout.setContentsMargins(5, 5, 5, 5)
        attributes_layout.setSpacing(5)
        
        title = QLabel("Attributes Editor")
        title.setStyleSheet("font-size: 11pt; font-weight: bold; padding: 5px;")
        attributes_layout.addWidget(title)
        
        # System Attributes section
        sys_attr_group = QGroupBox("System Attributes")
        sys_attr_layout = QFormLayout(sys_attr_group)
        sys_attr_layout.setSpacing(5)
        
        # Create fields for system attributes
        self.attr_creation_date = QLineEdit()
        self.attr_creation_date.setReadOnly(True)
        self.attr_creation_date.setStyleSheet("background-color: #f5f5f5;")
        sys_attr_layout.addRow("Creation Date:", self.attr_creation_date)
        
        self.attr_creation_id = QLineEdit()
        self.attr_creation_id.setReadOnly(True)
        self.attr_creation_id.setStyleSheet("background-color: #f5f5f5;")
        sys_attr_layout.addRow("Creation ID:", self.attr_creation_id)
        
        self.attr_change_date = QLineEdit()
        self.attr_change_date.setReadOnly(True)
        self.attr_change_date.setStyleSheet("background-color: #f5f5f5;")
        sys_attr_layout.addRow("Change Date:", self.attr_change_date)
        
        self.attr_change_id = QLineEdit()
        self.attr_change_id.setReadOnly(True)
        self.attr_change_id.setStyleSheet("background-color: #f5f5f5;")
        sys_attr_layout.addRow("Change ID:", self.attr_change_id)
        
        attributes_layout.addWidget(sys_attr_group)
        
        # Custom Attributes section
        custom_attr_group = QGroupBox("Custom Attributes")
        custom_attr_layout = QVBoxLayout(custom_attr_group)
        self.custom_attributes_text = QTextEdit()
        self.custom_attributes_text.setReadOnly(True)
        self.custom_attributes_text.setMaximumHeight(100)
        self.custom_attributes_text.setPlaceholderText("No custom attributes")
        custom_attr_layout.addWidget(self.custom_attributes_text)
        attributes_layout.addWidget(custom_attr_group)
        
        # Language-specific Attributes section
        lang_attr_group = QGroupBox("Language-specific Attributes")
        lang_attr_layout = QFormLayout(lang_attr_group)
        
        self.lang_attr_creation_date = QLineEdit()
        self.lang_attr_creation_date.setReadOnly(True)
        self.lang_attr_creation_date.setStyleSheet("background-color: #f5f5f5;")
        lang_attr_layout.addRow("Creation Date:", self.lang_attr_creation_date)
        
        self.lang_attr_change_date = QLineEdit()
        self.lang_attr_change_date.setReadOnly(True)
        self.lang_attr_change_date.setStyleSheet("background-color: #f5f5f5;")
        lang_attr_layout.addRow("Change Date:", self.lang_attr_change_date)
        
        attributes_layout.addWidget(lang_attr_group)
        
        # Comments section
        comments_group = QGroupBox("Comments")
        comments_layout = QVBoxLayout(comments_group)
        self.comments_text = QTextEdit()
        self.comments_text.setReadOnly(True)
        self.comments_text.setPlaceholderText("No comments")
        comments_layout.addWidget(self.comments_text)
        attributes_layout.addWidget(comments_group)
        
        attributes_layout.addStretch()
        
        return attributes_panel
    
    def update_attributes_display(self, tu: TmxTranslationUnit):
        """Update the Attributes Editor panel with TU attributes"""
        # System Attributes
        self.attr_creation_date.setText(tu.creation_date if tu.creation_date else "")
        self.attr_creation_id.setText(tu.creation_id if tu.creation_id else "")
        self.attr_change_date.setText(tu.change_date if tu.change_date else "")
        self.attr_change_id.setText(tu.change_id if tu.change_id else "")
        
        # Language-specific attributes (from segments)
        src_seg = tu.get_segment(self.src_lang)
        if src_seg:
            self.lang_attr_creation_date.setText(src_seg.creation_date if src_seg.creation_date else "")
            self.lang_attr_change_date.setText(src_seg.change_date if src_seg.change_date else "")
        else:
            self.lang_attr_creation_date.setText("")
            self.lang_attr_change_date.setText("")
        
        # Custom attributes and comments - empty for now
        self.custom_attributes_text.clear()
        self.comments_text.clear()
    
    def clear_attributes_display(self):
        """Clear the Attributes Editor panel"""
        self.attr_creation_date.clear()
        self.attr_creation_id.clear()
        self.attr_change_date.clear()
        self.attr_change_id.clear()
        self.lang_attr_creation_date.clear()
        self.lang_attr_change_date.clear()
        self.custom_attributes_text.clear()
        self.comments_text.clear()
    
    def create_status_bar(self, parent_layout):
        """Create status bar"""
        self.status_bar = QLabel("Ready")
        self.status_bar.setStyleSheet("background-color: #e0e0e0; padding: 3px; border: 1px solid #ccc;")
        self.status_bar.setMinimumHeight(20)
        parent_layout.addWidget(self.status_bar)
    
    # ===== File Operations =====
    
    def new_tmx(self):
        """Create new TMX file"""
        if self.tmx_file and self.tmx_file.is_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "Current file has unsaved changes. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Prompt for languages
        dialog = QDialog(self)
        dialog.setWindowTitle("New TMX File")
        dialog.resize(400, 250)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("Create New TMX File")
        title.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(title)
        
        form = QFormLayout()
        
        src_entry = QLineEdit("en-US")
        form.addRow("Source Language:", src_entry)
        
        tgt_entry = QLineEdit("nl-NL")
        form.addRow("Target Language:", tgt_entry)
        
        creator_entry = QLineEdit(os.getlogin() if hasattr(os, 'getlogin') else "user")
        form.addRow("Creator ID:", creator_entry)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            src = src_entry.text().strip()
            tgt = tgt_entry.text().strip()
            creator = creator_entry.text().strip()
            
            if not src or not tgt:
                QMessageBox.warning(self, "Error", "Please enter both source and target languages")
                return
            
            self.tmx_file = TmxFile()
            self.tmx_file.header.srclang = src
            self.tmx_file.header.creation_id = creator
            self.tmx_file.header.change_id = creator
            self.tmx_file.languages = [src, tgt]
            
            # Add one empty translation unit
            tu = TmxTranslationUnit(tu_id=1, creation_id=creator)
            tu.set_segment(src, "")
            tu.set_segment(tgt, "")
            self.tmx_file.add_translation_unit(tu)
            
            self.src_lang = src
            self.tgt_lang = tgt
            
            self.refresh_ui()
            self.set_status(f"Created new TMX file: {src} → {tgt}")
    
    def open_tmx(self):
        """Open TMX file with RAM/DB/Auto mode selection"""
        if self.tmx_file and self.tmx_file.is_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "Current file has unsaved changes. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open TMX File", "", "TMX files (*.tmx);;All files (*.*)"
        )
        
        if not file_path:
            return
        
        # Get file size
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # Determine recommended mode
        if file_size_mb < 50:
            recommended_mode = "ram"
            recommended_text = "RAM mode"
        elif file_size_mb > 100:
            recommended_mode = "database"
            recommended_text = "Database mode"
        else:
            recommended_mode = "database"
            recommended_text = "Database mode"
        
        # Show mode selection dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Open TMX File")
        dialog.resize(500, 250)
        layout = QVBoxLayout(dialog)
        
        # File info
        info_label = QLabel(f"File: {os.path.basename(file_path)}\nSize: {file_size_mb:.2f} MB")
        info_label.setStyleSheet("font-weight: bold; font-size: 10pt; padding: 10px;")
        layout.addWidget(info_label)
        
        # Important note about what this dialog does
        explanation_label = QLabel(
            "Choose how to load this TMX file:\n"
            "• RAM Mode: Entire file loads into memory (fast, but limited by RAM)\n"
            "• Database Mode: File stored in database (slower load, but handles huge files)\n"
            "• Auto: Automatically selects the best mode for this file size"
        )
        explanation_label.setStyleSheet("background-color: #fff9e6; padding: 10px; border: 1px solid #ffd700; border-radius: 5px; font-size: 9pt;")
        layout.addWidget(explanation_label)
        
        # Mode selection with CheckmarkCheckBox style (mutually exclusive)
        mode_group = QGroupBox("Select Load Mode (click to choose)")
        mode_layout = QVBoxLayout(mode_group)
        mode_layout.setSpacing(8)
        
        # Auto mode - show what it will actually do
        auto_text = f"Auto → Current file will load in {recommended_text}"
        mode_auto = CheckmarkCheckBox(auto_text)
        mode_auto.setChecked(True)
        mode_layout.addWidget(mode_auto)
        
        # RAM mode
        mode_ram = CheckmarkCheckBox("RAM Mode → Loads entire file into RAM memory")
        mode_layout.addWidget(mode_ram)
        
        # Database mode
        mode_db = CheckmarkCheckBox("Database Mode → Stores file in SQLite database")
        mode_layout.addWidget(mode_db)
        
        # Make them mutually exclusive (like radio buttons)
        # Prevent unchecking - always keep one selected
        _updating_checks = False
        
        def handle_toggle(toggled_widget):
            """Handle toggle - make mutually exclusive and prevent unchecking"""
            nonlocal _updating_checks
            if _updating_checks:
                return
            
            if toggled_widget.isChecked():
                # Uncheck others
                _updating_checks = True
                for widget in [mode_auto, mode_ram, mode_db]:
                    if widget != toggled_widget:
                        widget.setChecked(False)
                _updating_checks = False
            else:
                # Prevent unchecking - re-check this one (like radio buttons)
                _updating_checks = True
                toggled_widget.setChecked(True)
                _updating_checks = False
        
        mode_auto.toggled.connect(lambda checked: handle_toggle(mode_auto))
        mode_ram.toggled.connect(lambda checked: handle_toggle(mode_ram))
        mode_db.toggled.connect(lambda checked: handle_toggle(mode_db))
        
        layout.addWidget(mode_group)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Open | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        # Determine selected mode (only one should be checked due to mutual exclusivity)
        if mode_auto.isChecked():
            selected_mode = recommended_mode
        elif mode_ram.isChecked():
            selected_mode = "ram"
        elif mode_db.isChecked():
            selected_mode = "database"
        else:
            # Fallback: if somehow none is checked, use auto
            selected_mode = recommended_mode
        
        # Load file
        try:
            if selected_mode == "database":
                self._open_tmx_database(file_path, file_size)
            else:
                self._open_tmx_ram(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open TMX file:\n{str(e)}")
    
    def _open_tmx_ram(self, file_path: str):
        """Open TMX file in RAM mode"""
        self.tmx_file = TmxParser.parse_file(file_path)
        self.tmx_file.file_path = file_path
        self.load_mode = "ram"
        self.tmx_file_id = None
        
        # Set default languages (first two in file)
        langs = self.tmx_file.get_languages()
        if len(langs) >= 2:
            self.src_lang = langs[0]
            self.tgt_lang = langs[1]
        elif len(langs) == 1:
            self.src_lang = langs[0]
            self.tgt_lang = langs[0]
        
        self.refresh_ui()
        self.set_status(f"Opened (RAM): {os.path.basename(file_path)} ({self.tmx_file.get_tu_count()} TUs)")
    
    def _open_tmx_database(self, file_path: str, file_size: int):
        """Open TMX file in Database mode"""
        if not self.db_manager:
            QMessageBox.warning(self, "Warning", "Database manager not available. Using RAM mode instead.")
            self._open_tmx_ram(file_path)
            return
        
        # Parse file first to get header and TU count
        temp_tmx = TmxParser.parse_file(file_path)
        tu_count = temp_tmx.get_tu_count()
        languages = temp_tmx.get_languages()
        
        # Prepare header data
        header_data = {
            'creation_tool': temp_tmx.header.creation_tool,
            'creation_tool_version': temp_tmx.header.creation_tool_version,
            'segtype': temp_tmx.header.segtype,
            'o_tmf': temp_tmx.header.o_tmf,
            'adminlang': temp_tmx.header.adminlang,
            'srclang': temp_tmx.header.srclang,
            'datatype': temp_tmx.header.datatype,
            'creation_date': temp_tmx.header.creation_date,
            'creation_id': temp_tmx.header.creation_id,
            'change_date': temp_tmx.header.change_date,
            'change_id': temp_tmx.header.change_id,
        }
        
        # Store file metadata
        file_name = os.path.basename(file_path)
        # Use a normalized path for database storage (to handle same file opened multiple times)
        db_file_path = f"tmx://{file_name}"
        
        self.tmx_file_id = self.db_manager.tmx_store_file(
            file_path=db_file_path,
            file_name=file_name,
            original_file_path=file_path,
            load_mode="database",
            file_size=file_size,
            header_data=header_data,
            tu_count=tu_count,
            languages=languages
        )
        
        # Store all translation units with batching for performance
        progress = QProgressDialog("Loading TMX into database...", "Cancel", 0, tu_count, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)  # Show immediately
        
        # Style the progress bar for better visibility - clearer blue
        progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #1976D2;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                background-color: #E3F2FD;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 3px;
            }
        """)
        
        progress.show()
        QApplication.processEvents()  # Force initial display
        
        # Batch size for database operations (commit every N TUs)
        BATCH_SIZE = 100
        
        try:
            # Start transaction for better performance
            self.db_manager.connection.execute("BEGIN TRANSACTION")
            
            for i, tu in enumerate(temp_tmx.translation_units):
                if progress.wasCanceled():
                    # Rollback transaction
                    self.db_manager.connection.rollback()
                    # Delete partial data
                    self.db_manager.tmx_delete_file(self.tmx_file_id)
                    return
                
                # Store TU (no commit - batch operation)
                tu_db_id = self.db_manager.tmx_store_translation_unit(
                    tmx_file_id=self.tmx_file_id,
                    tu_id=tu.tu_id,
                    creation_date=tu.creation_date,
                    creation_id=tu.creation_id,
                    change_date=tu.change_date,
                    change_id=tu.change_id,
                    srclang=tu.srclang,
                    custom_attributes=None,  # TODO: Extract custom attributes
                    comments=None,  # TODO: Extract comments
                    commit=False  # Batch commit
                )
                
                # Store segments (no commit - batch operation)
                for lang, segment in tu.segments.items():
                    self.db_manager.tmx_store_segment(
                        tu_db_id=tu_db_id,
                        lang=lang,
                        text=segment.text,
                        creation_date=segment.creation_date,
                        creation_id=segment.creation_id,
                        change_date=segment.change_date,
                        change_id=segment.change_id,
                        commit=False  # Batch commit
                    )
                
                # Commit batch and update progress every BATCH_SIZE items
                if (i + 1) % BATCH_SIZE == 0 or (i + 1) == tu_count:
                    self.db_manager.connection.commit()
                    if (i + 1) < tu_count:
                        # Start next transaction
                        self.db_manager.connection.execute("BEGIN TRANSACTION")
                    
                    # Update progress (less frequently for better performance)
                    progress.setValue(i + 1)
                    # Process events every batch, not every item
                    QApplication.processEvents()
        
        except Exception as e:
            # Rollback on error
            self.db_manager.connection.rollback()
            raise
        finally:
            # Ensure transaction is closed
            try:
                self.db_manager.connection.commit()
            except:
                pass
            progress.close()
        
        # Set mode and clear RAM file
        self.load_mode = "database"
        self.tmx_file = None  # No longer needed in RAM
        
        # Set default languages
        if len(languages) >= 2:
            self.src_lang = languages[0]
            self.tgt_lang = languages[1]
        elif len(languages) == 1:
            self.src_lang = languages[0]
            self.tgt_lang = languages[0]
        
        self.refresh_ui()
        self.set_status(f"Opened (Database): {file_name} ({tu_count} TUs)")
    
    def save_tmx(self):
        """Save TMX file"""
        if self.load_mode == "database":
            # Database mode - export to TMX file
            if not self.db_manager or not self.tmx_file_id:
                QMessageBox.warning(self, "Warning", "No file to save")
                return
            
            # Get file info to determine save path
            file_info = self.db_manager.tmx_get_file_info(self.tmx_file_id)
            if not file_info:
                QMessageBox.warning(self, "Warning", "File information not found")
                return
            
            original_path = file_info.get('original_file_path')
            if not original_path:
                # No original path, use Save As
                self.save_tmx_as()
                return
            
            # Export database to TMX file
            self._export_database_to_tmx(original_path)
            return
        
        # RAM mode
        if not self.tmx_file:
            QMessageBox.warning(self, "Warning", "No file to save")
            return
        
        if not self.tmx_file.file_path:
            self.save_tmx_as()
            return
        
        try:
            # Update change date
            self.tmx_file.header.change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            
            TmxParser.save_file(self.tmx_file, self.tmx_file.file_path)
            self.tmx_file.is_modified = False
            self.set_status(f"Saved: {os.path.basename(self.tmx_file.file_path)}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save TMX file:\n{str(e)}")
    
    def close_tmx(self):
        """Close current TMX file"""
        # Check for unsaved changes (only relevant for RAM mode)
        if self.load_mode == "ram" and self.tmx_file and self.tmx_file.is_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "Current file has unsaved changes. Close without saving?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.No:
                # User wants to save first
                self.save_tmx()
                if self.tmx_file and self.tmx_file.is_modified:
                    # Save was cancelled or failed
                    return
        
        # For database mode, optionally delete from database (or keep for future sessions)
        # For now, we'll keep it in database - user can reopen it
        
        # Clear the file
        self.tmx_file = None
        self.tmx_file_id = None
        self.load_mode = "ram"
        self.filtered_tus = []
        self.current_page = 0
        self.tu_row_map.clear()
        
        # Clear UI
        self.table.setRowCount(0)
        self.page_label.setText("No file open")
        self.clear_attributes_display()
        
        # Clear language combos
        self.src_lang_combo.clear()
        self.tgt_lang_combo.clear()
        
        # Clear filter fields
        self.filter_source_entry.clear()
        self.filter_target_entry.clear()
        
        # Clear header labels
        if hasattr(self, 'src_search_label'):
            self.src_search_label.setText("Source:")
        if hasattr(self, 'tgt_search_label'):
            self.tgt_search_label.setText("Target:")
        
        self.src_lang = ""
        self.tgt_lang = ""
        
        self.set_status("TMX file closed")
    
    def save_tmx_as(self):
        """Save TMX file with new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save TMX File", "", "TMX files (*.tmx);;All files (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            if self.load_mode == "database":
                # Export database to TMX file
                self._export_database_to_tmx(file_path)
            else:
                # RAM mode - save directly
                if not self.tmx_file:
                    QMessageBox.warning(self, "Warning", "No file to save")
                    return
                
                # Update change date
                self.tmx_file.header.change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
                
                TmxParser.save_file(self.tmx_file, file_path)
                self.tmx_file.file_path = file_path
                self.tmx_file.is_modified = False
                self.set_status(f"Saved as: {os.path.basename(file_path)}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save TMX file:\n{str(e)}")
    
    def _export_database_to_tmx(self, file_path: str):
        """Export database-backed TMX to TMX file"""
        if not self.db_manager or not self.tmx_file_id:
            raise ValueError("Database manager or file ID not available")
        
        # Get file info
        file_info = self.db_manager.tmx_get_file_info(self.tmx_file_id)
        if not file_info:
            raise ValueError("File information not found")
        
        # Create TmxFile object from database
        tmx_file = TmxFile()
        
        # Set header from database
        header_data = file_info['header_data']
        for key, value in header_data.items():
            if hasattr(tmx_file.header, key):
                setattr(tmx_file.header, key, value)
        
        # Get all translation units (without pagination for export)
        progress = QProgressDialog("Exporting TMX file...", "Cancel", 0, file_info['tu_count'], self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        
        # Style the progress bar for better visibility - clearer blue
        progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #1976D2;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                background-color: #E3F2FD;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 3px;
            }
        """)
        
        progress.show()
        
        try:
            offset = 0
            batch_size = 1000
            
            while True:
                db_tus = self.db_manager.tmx_get_translation_units(
                    tmx_file_id=self.tmx_file_id,
                    offset=offset,
                    limit=batch_size,
                    src_lang=None,  # Get all languages
                    tgt_lang=None,
                    src_filter=None,
                    tgt_filter=None,
                    ignore_case=True
                )
                
                if not db_tus:
                    break
                
                # Convert to TmxTranslationUnit objects
                for db_tu in db_tus:
                    tu = self._db_tu_to_tmx_tu(db_tu)
                    tmx_file.add_translation_unit(tu)
                    progress.setValue(len(tmx_file.translation_units))
                    QApplication.processEvents()
                    
                    if progress.wasCanceled():
                        raise Exception("Export cancelled")
                
                offset += batch_size
                if len(db_tus) < batch_size:
                    break
        
        finally:
            progress.close()
        
        # Save to file
        tmx_file.header.change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        TmxParser.save_file(tmx_file, file_path)
        
        # Update database file info
        self.db_manager.cursor.execute("""
            UPDATE tmx_files
            SET original_file_path = ?, last_modified = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (file_path, self.tmx_file_id))
        self.db_manager.connection.commit()
        
        self.set_status(f"Exported: {os.path.basename(file_path)} ({len(tmx_file.translation_units)} TUs)")
    
    # ===== Edit Operations =====
    
    def add_translation_unit(self):
        """Add new translation unit"""
        if not self.src_lang or not self.tgt_lang:
            QMessageBox.warning(self, "Warning", "Please select source and target languages")
            return
        
        if self.load_mode == "database":
            if not self.db_manager or not self.tmx_file_id:
                QMessageBox.warning(self, "Warning", "Please create or open a TMX file first")
                return
            
            # Get next TU ID (find max tu_id for this file)
            self.db_manager.cursor.execute("""
                SELECT MAX(tu_id) FROM tmx_translation_units
                WHERE tmx_file_id = ?
            """, (self.tmx_file_id,))
            result = self.db_manager.cursor.fetchone()
            new_id = (result[0] + 1) if result[0] else 1
            
            # Get creation_id from file info
            file_info = self.db_manager.tmx_get_file_info(self.tmx_file_id)
            creation_id = file_info.get('header_data', {}).get('creation_id', '') if file_info else ''
            
            # Create new TU in database
            tu_db_id = self.db_manager.tmx_store_translation_unit(
                tmx_file_id=self.tmx_file_id,
                tu_id=new_id,
                creation_id=creation_id,
                srclang=self.src_lang
            )
            
            # Add segments
            self.db_manager.tmx_store_segment(tu_db_id, self.src_lang, "")
            self.db_manager.tmx_store_segment(tu_db_id, self.tgt_lang, "")
            
            # Update file TU count
            self.db_manager.cursor.execute("""
                UPDATE tmx_files
                SET tu_count = tu_count + 1, last_modified = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (self.tmx_file_id,))
            self.db_manager.connection.commit()
            
            self.apply_filters()  # Refresh view
            self.set_status(f"Added TU #{new_id}")
            return
        
        # RAM mode
        if not self.tmx_file:
            QMessageBox.warning(self, "Warning", "Please create or open a TMX file first")
            return
        
        # Create new TU
        new_id = self.tmx_file.get_tu_count() + 1
        tu = TmxTranslationUnit(tu_id=new_id,
                               creation_id=self.tmx_file.header.creation_id)
        tu.set_segment(self.src_lang, "")
        tu.set_segment(self.tgt_lang, "")
        
        self.tmx_file.add_translation_unit(tu)
        self.apply_filters()  # Refresh view
        self.set_status(f"Added TU #{new_id}")
    
    def delete_selected_tu(self):
        """Delete selected translation unit"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "Info", "Please select a translation unit to delete")
            return
        
        if current_row not in self.tu_row_map:
            return
        
        tu = self.tu_row_map[current_row]
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete translation unit #{tu.tu_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.load_mode == "database":
                # Delete from database
                if self.db_manager and self.tmx_file_id:
                    # Delete TU (segments will be deleted via CASCADE)
                    self.db_manager.cursor.execute("""
                        DELETE FROM tmx_translation_units
                        WHERE tmx_file_id = ? AND tu_id = ?
                    """, (self.tmx_file_id, tu.tu_id))
                    self.db_manager.connection.commit()
                    
                    # Update file TU count
                    self.db_manager.cursor.execute("""
                        UPDATE tmx_files
                        SET tu_count = tu_count - 1, last_modified = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (self.tmx_file_id,))
                    self.db_manager.connection.commit()
            else:
                # Delete from RAM
                self.tmx_file.translation_units.remove(tu)
                self.tmx_file.is_modified = True
            
            self.apply_filters()
            self.set_status(f"Deleted TU #{tu.tu_id}")
    
    # ===== View Operations =====
    
    def on_language_changed(self):
        """Handle language selection change"""
        self.src_lang = self.src_lang_combo.currentText()
        self.tgt_lang = self.tgt_lang_combo.currentText()
        
        # Update filter labels to show current language codes
        if hasattr(self, 'src_search_label'):
            self.src_search_label.setText(f"Source: {self.src_lang}")
        if hasattr(self, 'tgt_search_label'):
            self.tgt_search_label.setText(f"Target: {self.tgt_lang}")
        
        self.apply_filters()
    
    def show_all_languages(self):
        """Show dialog with all languages in TMX"""
        languages = []
        
        if self.load_mode == "database":
            if self.db_manager and self.tmx_file_id:
                file_info = self.db_manager.tmx_get_file_info(self.tmx_file_id)
                if file_info:
                    languages = file_info.get('languages', [])
        else:
            if not self.tmx_file:
                return
            languages = self.tmx_file.get_languages()
        
        if not languages:
            QMessageBox.information(self, "Info", "No languages found")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("All Languages")
        dialog.resize(400, 400)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("Languages in this TMX file:")
        title.setStyleSheet("font-size: 11pt; font-weight: bold;")
        layout.addWidget(title)
        
        list_widget = QListWidget()
        for lang in languages:
            list_widget.addItem(lang)
        layout.addWidget(list_widget)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec()
    
    def edit_header(self):
        """Edit TMX header metadata"""
        # Get header data
        header_data = {}
        
        if self.load_mode == "database":
            if not self.db_manager or not self.tmx_file_id:
                QMessageBox.warning(self, "Warning", "Please create or open a TMX file first")
                return
            file_info = self.db_manager.tmx_get_file_info(self.tmx_file_id)
            if file_info:
                header_data = file_info.get('header_data', {})
        else:
            if not self.tmx_file:
                QMessageBox.warning(self, "Warning", "Please create or open a TMX file first")
                return
            # Get header from RAM file
            header_data = {
                'creation_tool': self.tmx_file.header.creation_tool,
                'creation_tool_version': self.tmx_file.header.creation_tool_version,
                'segtype': self.tmx_file.header.segtype,
                'o_tmf': self.tmx_file.header.o_tmf,
                'adminlang': self.tmx_file.header.adminlang,
                'srclang': self.tmx_file.header.srclang,
                'datatype': self.tmx_file.header.datatype,
                'creation_date': self.tmx_file.header.creation_date,
                'creation_id': self.tmx_file.header.creation_id,
                'change_date': self.tmx_file.header.change_date,
                'change_id': self.tmx_file.header.change_id,
            }
        
        dialog = QDialog(self)
        dialog.setWindowTitle("TMX Header Metadata")
        dialog.resize(500, 500)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("TMX Header Information")
        title.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(title)
        
        form = QFormLayout()
        fields = {}
        
        for field_name, field_label in [
            ('creation_tool', 'Creation Tool'),
            ('creation_tool_version', 'Tool Version'),
            ('segtype', 'Segment Type'),
            ('o_tmf', 'O-TMF'),
            ('adminlang', 'Admin Language'),
            ('srclang', 'Source Language'),
            ('datatype', 'Data Type'),
            ('creation_id', 'Creator ID'),
            ('change_id', 'Last Modified By')
        ]:
            entry = QLineEdit()
            entry.setText(str(header_data.get(field_name, '')))
            form.addRow(f"{field_label}:", entry)
            fields[field_name] = entry
        
        # Read-only dates
        form.addRow("Creation Date:", QLabel(header_data.get('creation_date', '')))
        form.addRow("Last Modified:", QLabel(header_data.get('change_date', '')))
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        
        def save_header():
            # Update header data
            updated_header = {}
            for field_name, entry in fields.items():
                updated_header[field_name] = entry.text()
            
            updated_header['change_date'] = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            
            if self.load_mode == "database":
                # Update database
                header_json = json.dumps(updated_header)
                self.db_manager.cursor.execute("""
                    UPDATE tmx_files
                    SET header_data = ?, last_modified = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (header_json, self.tmx_file_id))
                self.db_manager.connection.commit()
            else:
                # Update RAM file
                for field_name, value in updated_header.items():
                    if hasattr(self.tmx_file.header, field_name):
                        setattr(self.tmx_file.header, field_name, value)
                self.tmx_file.is_modified = True
            
            dialog.accept()
            self.set_status("Header updated")
        
        buttons.accepted.connect(save_header)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec()
    
    def show_statistics(self):
        """Show TMX file statistics"""
        if self.load_mode == "database":
            if not self.db_manager or not self.tmx_file_id:
                QMessageBox.warning(self, "Warning", "No file open")
                return
            
            file_info = self.db_manager.tmx_get_file_info(self.tmx_file_id)
            if not file_info:
                QMessageBox.warning(self, "Warning", "File information not found")
                return
            
            total_tus = file_info.get('tu_count', 0)
            languages = file_info.get('languages', [])
            
            # Count segments per language (would need separate query for accurate counts)
            # For now, show basic stats
            stats = f"TMX File Statistics\n\n"
            stats += f"Total Translation Units: {total_tus}\n"
            stats += f"Languages: {len(languages)}\n"
            stats += f"Load Mode: Database\n"
            stats += f"File Size: {file_info.get('file_size', 0) / (1024*1024):.2f} MB\n\n"
            stats += "Languages:\n"
            for lang in sorted(languages):
                stats += f"  - {lang}\n"
            
            QMessageBox.information(self, "Statistics", stats)
            return
        
        # RAM mode
        if not self.tmx_file:
            return
        
        total_tus = self.tmx_file.get_tu_count()
        languages = self.tmx_file.get_languages()
        
        # Count segments per language
        lang_counts = {lang: 0 for lang in languages}
        total_chars = {lang: 0 for lang in languages}
        
        for tu in self.tmx_file.translation_units:
            for lang, segment in tu.segments.items():
                lang_counts[lang] += 1
                total_chars[lang] += len(segment.text)
        
        # Build statistics message
        stats = f"TMX File Statistics\n\n"
        stats += f"Total Translation Units: {total_tus}\n"
        stats += f"Languages: {len(languages)}\n"
        stats += f"Load Mode: RAM\n\n"
        stats += "Segments per Language:\n"
        
        for lang in sorted(languages):
            avg_chars = total_chars[lang] / lang_counts[lang] if lang_counts[lang] > 0 else 0
            stats += f"  {lang}: {lang_counts[lang]} segments (avg {avg_chars:.1f} chars)\n"
        
        QMessageBox.information(self, "Statistics", stats)
    
    # ===== Filter Operations =====
    
    def apply_filters(self):
        """Apply filters and refresh grid"""
        if self.load_mode == "database":
            # Database mode - filters are applied in refresh_current_page via query
            self.current_page = 0
            self.refresh_current_page()
            return
        
        # RAM mode
        if not self.tmx_file:
            return
        
        ignore_case = self.filter_ignore_case.isChecked()
        
        # Get filter text (store original case for highlighting)
        source_filter_text = self.filter_source_entry.text()
        target_filter_text = self.filter_target_entry.text()
        
        # Store filters (lowercase for comparison if ignore_case)
        self.filter_source = source_filter_text.lower() if ignore_case else source_filter_text
        self.filter_target = target_filter_text.lower() if ignore_case else target_filter_text
        
        # Filter TUs
        self.filtered_tus = []
        for tu in self.tmx_file.translation_units:
            src_seg = tu.get_segment(self.src_lang)
            tgt_seg = tu.get_segment(self.tgt_lang)
            
            src_text = src_seg.text if src_seg else ""
            tgt_text = tgt_seg.text if tgt_seg else ""
            
            # Apply filters (case-insensitive if ignore_case is checked)
            if ignore_case:
                src_text = src_text.lower()
                tgt_text = tgt_text.lower()
            
            if self.filter_source and self.filter_source not in src_text:
                continue
            if self.filter_target and self.filter_target not in tgt_text:
                continue
            
            self.filtered_tus.append(tu)
        
        self.current_page = 0
        self.refresh_current_page()
    
    def clear_filters(self):
        """Clear all filters"""
        self.filter_source_entry.clear()
        self.filter_target_entry.clear()
        self.filter_source = ""
        self.filter_target = ""
        self.apply_filters()
    
    # ===== Pagination =====
    
    def _db_tu_to_tmx_tu(self, db_tu_data: Dict) -> TmxTranslationUnit:
        """Convert database TU data to TmxTranslationUnit object"""
        tu = TmxTranslationUnit(tu_id=db_tu_data['tu_id'])
        tu.creation_date = db_tu_data.get('creation_date', '')
        tu.creation_id = db_tu_data.get('creation_id', '')
        tu.change_date = db_tu_data.get('change_date', '')
        tu.change_id = db_tu_data.get('change_id', '')
        tu.srclang = db_tu_data.get('srclang', '')
        
        # Add segments
        for lang, seg_data in db_tu_data.get('segments', {}).items():
            seg = TmxSegment(
                lang=lang,
                text=seg_data.get('text', ''),
                creation_date=seg_data.get('creation_date', ''),
                creation_id=seg_data.get('creation_id', ''),
                change_date=seg_data.get('change_date', ''),
                change_id=seg_data.get('change_id', '')
            )
            tu.segments[lang] = seg
        
        return tu
    
    def refresh_current_page(self):
        """Refresh current page in table"""
        # Update column headers with language codes
        self.table.setHorizontalHeaderLabels([
            'No.',
            f'{self.src_lang}',
            f'{self.tgt_lang}',
            'System Attributes'
        ])
        
        if self.load_mode == "database":
            # Database mode - query database
            if not self.db_manager or not self.tmx_file_id:
                self.page_label.setText("No file open")
                self.table.setRowCount(0)
                self.tu_row_map.clear()
                self.clear_attributes_display()
                return
            
            # Get filters
            ignore_case = self.filter_ignore_case.isChecked()
            source_filter = self.filter_source_entry.text() if self.filter_source_entry else ""
            target_filter = self.filter_target_entry.text() if self.filter_target_entry else ""
            
            # Count total items
            total_items = self.db_manager.tmx_count_translation_units(
                tmx_file_id=self.tmx_file_id,
                src_lang=self.src_lang,
                tgt_lang=self.tgt_lang,
                src_filter=source_filter,
                tgt_filter=target_filter,
                ignore_case=ignore_case
            )
            
            total_pages = (total_items + self.items_per_page - 1) // self.items_per_page if total_items > 0 else 0
            
            if total_pages == 0:
                self.page_label.setText("No items")
                self.table.setRowCount(0)
                self.tu_row_map.clear()
                self.clear_attributes_display()
                return
            
            # Query current page
            offset = self.current_page * self.items_per_page
            db_tus = self.db_manager.tmx_get_translation_units(
                tmx_file_id=self.tmx_file_id,
                offset=offset,
                limit=self.items_per_page,
                src_lang=self.src_lang,
                tgt_lang=self.tgt_lang,
                src_filter=source_filter,
                tgt_filter=target_filter,
                ignore_case=ignore_case
            )
            
            # Convert to TmxTranslationUnit objects for display
            tus = [self._db_tu_to_tmx_tu(db_tu) for db_tu in db_tus]
            
        else:
            # RAM mode
            if not self.tmx_file:
                self.page_label.setText("No file open")
                self.table.setRowCount(0)
                self.tu_row_map.clear()
                self.clear_attributes_display()
                return
            
            # Calculate page range
            total_items = len(self.filtered_tus)
            total_pages = (total_items + self.items_per_page - 1) // self.items_per_page if total_items > 0 else 0
            
            if total_pages == 0:
                self.page_label.setText("No items")
                self.table.setRowCount(0)
                self.tu_row_map.clear()
                self.clear_attributes_display()
                return
            
            start_idx = self.current_page * self.items_per_page
            end_idx = min(start_idx + self.items_per_page, total_items)
            tus = self.filtered_tus[start_idx:end_idx]
        
        # Set row count
        self.table.setRowCount(len(tus))
        self.tu_row_map.clear()
        
        # Add items to table
        for i, tu in enumerate(tus):
            row = i
            src_seg = tu.get_segment(self.src_lang)
            tgt_seg = tu.get_segment(self.tgt_lang)
            
            src_text = src_seg.text if src_seg else ""
            tgt_text = tgt_seg.text if tgt_seg else ""
            
            # Clean up text for display (remove newlines)
            src_display = src_text.replace('\n', ' ').replace('\r', '')
            tgt_display = tgt_text.replace('\n', ' ').replace('\r', '')
            
            # Create items
            no_item = QTableWidgetItem(str(tu.tu_id))
            no_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            no_item.setFlags(no_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            # Source item - editable with original text stored
            src_item = QTableWidgetItem(src_display)
            src_item.setFlags(src_item.flags() | Qt.ItemFlag.ItemIsEditable)  # Make editable
            src_item.setData(Qt.ItemDataRole.UserRole, src_text)  # Store original text with newlines
            
            # Target item - editable with original text stored
            tgt_item = QTableWidgetItem(tgt_display)
            tgt_item.setFlags(tgt_item.flags() | Qt.ItemFlag.ItemIsEditable)  # Make editable
            tgt_item.setData(Qt.ItemDataRole.UserRole, tgt_text)  # Store original text with newlines
            
            # System Attributes column - show "N/A" for now
            attr_item = QTableWidgetItem("N/A")
            attr_item.setFlags(attr_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            attr_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.table.setItem(row, 0, no_item)
            self.table.setItem(row, 1, src_item)
            self.table.setItem(row, 2, tgt_item)
            self.table.setItem(row, 3, attr_item)
            
            # Store TU reference
            self.tu_row_map[row] = tu
        
        # Update highlight delegates with current filter text
        ignore_case = self.filter_ignore_case.isChecked()
        source_filter = self.filter_source_entry.text() if self.filter_source_entry else ""
        target_filter = self.filter_target_entry.text() if self.filter_target_entry else ""
        
        self.highlight_delegate_source.set_highlight(source_filter, ignore_case)
        self.highlight_delegate_target.set_highlight(target_filter, ignore_case)
        
        # Trigger repaint to show highlighting
        self.table.viewport().update()
        
        # Update page label
        self.page_label.setText(f"Page {self.current_page + 1} of {total_pages} ({total_items} TUs)")
    
    def create_status_bar(self, parent_layout):
        """Create status bar - Heartsome style"""
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Shape.Box)
        status_frame.setStyleSheet("background-color: #e0e0e0; padding: 3px; border-top: 1px solid #ccc;")
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(5, 2, 5, 2)
        
        self.status_bar = QLabel("Ready")
        self.status_bar.setStyleSheet("font-size: 9pt;")
        status_layout.addWidget(self.status_bar)
        
        status_layout.addStretch()
        
        # Right side could show memory usage, language, date/time like Heartsome
        # For now just keep it simple
        
        parent_layout.addWidget(status_frame)
    
    def on_table_selection_changed(self):
        """Handle table selection change - update attributes"""
        current_row = self.table.currentRow()
        if current_row >= 0 and current_row in self.tu_row_map:
            tu = self.tu_row_map[current_row]
            self.update_attributes_display(tu)
        else:
            self.clear_attributes_display()
    
    def on_table_double_clicked(self, item):
        """Handle double-click on table - edit inline"""
        # Inline editing is handled by QTableWidget edit triggers
        pass
    
    def on_cell_edited(self, item: QTableWidgetItem):
        """Handle cell edit - save changes directly to TMX data"""
        row = item.row()
        col = item.column()
        
        if row not in self.tu_row_map:
            return
        
        tu = self.tu_row_map[row]
        new_text = item.text()
        
        # Temporarily disconnect to avoid recursion
        self.table.itemChanged.disconnect(self.on_cell_edited)
        
        try:
            if col == 1:  # Source column
                if self.load_mode == "database":
                    # Update database
                    if self.db_manager and self.tmx_file_id:
                        self.db_manager.tmx_update_segment(
                            tmx_file_id=self.tmx_file_id,
                            tu_id=tu.tu_id,
                            lang=self.src_lang,
                            text=new_text
                        )
                else:
                    # Update RAM
                    tu.set_segment(self.src_lang, new_text)
                    self.tmx_file.is_modified = True
                
                # Update display (remove newlines for display)
                display_text = new_text.replace('\n', ' ').replace('\r', '')
                item.setText(display_text)
                # Store original text
                item.setData(Qt.ItemDataRole.UserRole, new_text)
                
            elif col == 2:  # Target column
                if self.load_mode == "database":
                    # Update database
                    if self.db_manager and self.tmx_file_id:
                        self.db_manager.tmx_update_segment(
                            tmx_file_id=self.tmx_file_id,
                            tu_id=tu.tu_id,
                            lang=self.tgt_lang,
                            text=new_text
                        )
                else:
                    # Update RAM
                    tu.set_segment(self.tgt_lang, new_text)
                    self.tmx_file.is_modified = True
                
                # Update display (remove newlines for display)
                display_text = new_text.replace('\n', ' ').replace('\r', '')
                item.setText(display_text)
                # Store original text
                item.setData(Qt.ItemDataRole.UserRole, new_text)
            
            # Update the TU object in memory for display
            tu.set_segment(self.src_lang if col == 1 else self.tgt_lang, new_text)
            
            # Update attributes display if this is the selected row
            if self.table.currentRow() == row:
                self.update_attributes_display(tu)
            
            self.set_status(f"Updated TU #{tu.tu_id}")
            
        finally:
            # Reconnect signal
            self.table.itemChanged.connect(self.on_cell_edited)
    
    def show_context_menu(self, position):
        """Show context menu on right-click"""
        menu = QMenu(self)
        
        edit_action = menu.addAction("Edit")
        edit_action.triggered.connect(self.edit_selected_tu)
        
        menu.addSeparator()
        
        refresh_action = menu.addAction("Refresh")
        refresh_action.triggered.connect(self.refresh_current_page)
        
        menu.exec(self.table.mapToGlobal(position))
    
    def edit_selected_tu(self):
        """Edit selected TU from context menu - just focus the cell for inline editing"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            # Select the target cell and start editing
            self.table.edit(self.table.item(current_row, 2))
    
    def first_page(self):
        """Go to first page"""
        self.current_page = 0
        self.refresh_current_page()
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh_current_page()
    
    def next_page(self):
        """Go to next page"""
        # Get total items count
        if self.load_mode == "database":
            if not self.db_manager or not self.tmx_file_id:
                return
            ignore_case = self.filter_ignore_case.isChecked()
            source_filter = self.filter_source_entry.text() if self.filter_source_entry else ""
            target_filter = self.filter_target_entry.text() if self.filter_target_entry else ""
            total_items = self.db_manager.tmx_count_translation_units(
                tmx_file_id=self.tmx_file_id,
                src_lang=self.src_lang,
                tgt_lang=self.tgt_lang,
                src_filter=source_filter,
                tgt_filter=target_filter,
                ignore_case=ignore_case
            )
        else:
            total_items = len(self.filtered_tus)
        
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page if total_items > 0 else 0
        
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.refresh_current_page()
    
    def last_page(self):
        """Go to last page"""
        # Get total items count
        if self.load_mode == "database":
            if not self.db_manager or not self.tmx_file_id:
                return
            ignore_case = self.filter_ignore_case.isChecked()
            source_filter = self.filter_source_entry.text() if self.filter_source_entry else ""
            target_filter = self.filter_target_entry.text() if self.filter_target_entry else ""
            total_items = self.db_manager.tmx_count_translation_units(
                tmx_file_id=self.tmx_file_id,
                src_lang=self.src_lang,
                tgt_lang=self.tgt_lang,
                src_filter=source_filter,
                tgt_filter=target_filter,
                ignore_case=ignore_case
            )
        else:
            total_items = len(self.filtered_tus)
        
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page if total_items > 0 else 0
        
        if total_pages > 0:
            self.current_page = total_pages - 1
            self.refresh_current_page()
    
    # ===== Tools =====
    
    def validate_tmx(self):
        """Validate TMX file structure"""
        if self.load_mode == "database":
            # For database mode, validation is less critical (data is already structured)
            QMessageBox.information(self, "Validation", 
                "Database-backed TMX files are automatically validated during import.\n"
                "✓ Structure is valid (stored in normalized database format)")
            return
        
        # RAM mode validation
        if not self.tmx_file:
            QMessageBox.warning(self, "Warning", "Please create or open a TMX file first")
            return
        
        issues = []
        
        # Check header
        if not self.tmx_file.header.srclang:
            issues.append("Missing source language in header")
        
        # Check translation units
        for tu in self.tmx_file.translation_units:
            if not tu.segments:
                issues.append(f"TU #{tu.tu_id}: No segments")
                continue
            
            # Check for empty segments
            for lang, seg in tu.segments.items():
                if not seg.text.strip():
                    issues.append(f"TU #{tu.tu_id}: Empty segment for {lang}")
        
        if issues:
            issues_text = "\n".join(issues[:20])  # Show first 20 issues
            if len(issues) > 20:
                issues_text += f"\n... and {len(issues) - 20} more issues"
            
            QMessageBox.warning(self, "Validation Issues", 
                              f"Found {len(issues)} issue(s):\n\n{issues_text}")
        else:
            QMessageBox.information(self, "Validation", "✓ No issues found. TMX file is valid!")
    
    # ===== UI Helpers =====
    
    def refresh_ui(self):
        """Refresh entire UI after loading file"""
        languages = []
        
        if self.load_mode == "database":
            # Database mode - get languages from database
            if self.db_manager and self.tmx_file_id:
                file_info = self.db_manager.tmx_get_file_info(self.tmx_file_id)
                if file_info:
                    languages = file_info.get('languages', [])
        else:
            # RAM mode
            if not self.tmx_file:
                return
            languages = self.tmx_file.get_languages()
        
        if not languages:
            return
        
        # Update language combos
        self.src_lang_combo.clear()
        self.src_lang_combo.addItems(languages)
        
        self.tgt_lang_combo.clear()
        self.tgt_lang_combo.addItems(languages)
        
        if self.src_lang in languages:
            self.src_lang_combo.setCurrentText(self.src_lang)
        elif languages:
            self.src_lang_combo.setCurrentIndex(0)
            self.src_lang = languages[0]
        
        if self.tgt_lang in languages:
            self.tgt_lang_combo.setCurrentText(self.tgt_lang)
        elif len(languages) > 1:
            self.tgt_lang_combo.setCurrentIndex(1)
            self.tgt_lang = languages[1]
        elif languages:
            self.tgt_lang_combo.setCurrentIndex(0)
            self.tgt_lang = languages[0]
        
        # Apply filters (will refresh grid)
        self.apply_filters()
    
    def set_status(self, message: str):
        """Set status bar message"""
        self.status_bar.setText(message)


# === Standalone Application ===

if __name__ == "__main__":
    """Run TMX Editor as a standalone application"""
    import sys
    from pathlib import Path
    
    # Determine database path (dev vs regular mode)
    import os
    ENABLE_PRIVATE_FEATURES = os.path.exists(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".supervertaler.local")
    )
    user_data_path = Path("user data_private" if ENABLE_PRIVATE_FEATURES else "user data")
    db_path = user_data_path / "Translation_Resources" / "supervertaler.db"
    
    # Ensure database directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("TMX Editor")
    app.setOrganizationName("Supervertaler")
    
    # Create database manager
    from modules.database_manager import DatabaseManager
    
    def log_callback(message: str):
        """Simple log callback for standalone mode"""
        print(f"[TMX Editor] {message}")
    
    db_manager = DatabaseManager(
        db_path=str(db_path),
        log_callback=log_callback
    )
    db_manager.connect()
    
    # Create main window
    from PyQt6.QtWidgets import QMainWindow
    
    class StandaloneWindow(QMainWindow):
        """Standalone window for TMX Editor"""
        def __init__(self):
            super().__init__()
            self.setWindowTitle("TMX Editor - Professional Translation Memory Editor")
            self.setGeometry(100, 100, 1400, 900)
            
            # Create TMX Editor widget with database manager
            self.tmx_editor = TmxEditorUIQt(parent=self, standalone=True, db_manager=db_manager)
            self.setCentralWidget(self.tmx_editor)
            
            # Create menu bar
            menubar = self.menuBar()
            
            # File menu
            file_menu = menubar.addMenu("File")
            open_action = file_menu.addAction("Open TMX...")
            open_action.setShortcut(QKeySequence.StandardKey.Open)
            open_action.triggered.connect(self.tmx_editor.open_tmx)
            
            save_action = file_menu.addAction("Save")
            save_action.setShortcut(QKeySequence.StandardKey.Save)
            save_action.triggered.connect(self.tmx_editor.save_tmx)
            
            save_as_action = file_menu.addAction("Save As...")
            save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
            save_as_action.triggered.connect(self.tmx_editor.save_tmx_as)
            
            file_menu.addSeparator()
            
            close_action = file_menu.addAction("Close")
            close_action.triggered.connect(self.tmx_editor.close_tmx)
            
            file_menu.addSeparator()
            
            exit_action = file_menu.addAction("Exit")
            exit_action.setShortcut(QKeySequence.StandardKey.Quit)
            exit_action.triggered.connect(self.close)
            
            # Edit menu
            edit_menu = menubar.addMenu("Edit")
            add_tu_action = edit_menu.addAction("Add Translation Unit")
            add_tu_action.triggered.connect(self.tmx_editor.add_translation_unit)
            
            delete_tu_action = edit_menu.addAction("Delete Selected TU")
            delete_tu_action.triggered.connect(self.tmx_editor.delete_selected_tu)
            
            # View menu
            view_menu = menubar.addMenu("View")
            stats_action = view_menu.addAction("Statistics")
            stats_action.triggered.connect(self.tmx_editor.show_statistics)
            langs_action = view_menu.addAction("All Languages")
            langs_action.triggered.connect(self.tmx_editor.show_all_languages)
            header_action = view_menu.addAction("Header Metadata")
            header_action.triggered.connect(self.tmx_editor.edit_header)
            
            # Tools menu
            tools_menu = menubar.addMenu("Tools")
            validate_action = tools_menu.addAction("Validate TMX")
            validate_action.triggered.connect(self.tmx_editor.validate_tmx)
        
        def closeEvent(self, event):
            """Handle window close - check for unsaved changes"""
            if self.tmx_editor.load_mode == "ram" and self.tmx_editor.tmx_file and self.tmx_editor.tmx_file.is_modified:
                reply = QMessageBox.question(
                    self, "Unsaved Changes",
                    "Current file has unsaved changes. Close without saving?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
                )
                if reply == QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
                elif reply == QMessageBox.StandardButton.No:
                    self.tmx_editor.save_tmx()
                    if self.tmx_editor.tmx_file and self.tmx_editor.tmx_file.is_modified:
                        event.ignore()
                        return
            
            # Close database connection
            if db_manager:
                db_manager.close()
            
            event.accept()
    
    # Create and show window
    window = StandaloneWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

