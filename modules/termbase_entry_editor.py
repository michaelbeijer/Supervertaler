"""
Glossary Entry Editor Dialog

Dialog for editing individual glossary entries with all metadata fields.
Can be opened from translation results panel (edit button or right-click menu).
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QSpinBox, QCheckBox, QPushButton, QGroupBox,
    QMessageBox, QListWidget, QListWidgetItem, QMenu, QScrollArea,
    QWidget, QToolButton, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from typing import Optional

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
            from PyQt6.QtWidgets import QStyleOptionButton
            from PyQt6.QtGui import QPainter, QPen, QColor
            from PyQt6.QtCore import QPointF, Qt

            opt = QStyleOptionButton()
            self.initStyleOption(opt)
            indicator_rect = self.style().subElementRect(
                self.style().SubElement.SE_CheckBoxIndicator,
                opt,
                self
            )

            if indicator_rect.isValid():
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                pen_width = max(2.0, min(indicator_rect.width(), indicator_rect.height()) * 0.12)
                painter.setPen(QPen(QColor(255, 255, 255), pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
                painter.setBrush(QColor(255, 255, 255))

                x = indicator_rect.x()
                y = indicator_rect.y()
                w = indicator_rect.width()
                h = indicator_rect.height()

                padding = min(w, h) * 0.15
                x += padding
                y += padding
                w -= padding * 2
                h -= padding * 2

                check_x1 = x + w * 0.10
                check_y1 = y + h * 0.50
                check_x2 = x + w * 0.35
                check_y2 = y + h * 0.70
                check_x3 = x + w * 0.90
                check_y3 = y + h * 0.25

                painter.drawLine(QPointF(check_x2, check_y2), QPointF(check_x3, check_y3))
                painter.drawLine(QPointF(check_x1, check_y1), QPointF(check_x2, check_y2))

                painter.end()



class TermbaseEntryEditor(QDialog):
    """Dialog for editing a termbase entry"""
    
    def __init__(self, parent=None, db_manager=None, termbase_id: Optional[int] = None, term_id: Optional[int] = None):
        """
        Initialize termbase entry editor
        
        Args:
            parent: Parent widget
            db_manager: DatabaseManager instance
            termbase_id: Termbase ID
            term_id: Term ID to edit (if None, creates new term)
        """
        super().__init__(parent)
        self.db_manager = db_manager
        self.termbase_id = termbase_id
        self.term_id = term_id
        self.term_data = None
        
        self.setWindowTitle("Edit Glossary Entry" if term_id else "New Glossary Entry")
        self.setModal(True)
        self.setMinimumWidth(550)

        # Auto-resize to fit screen (max 85% of screen height)
        screen = QApplication.primaryScreen().availableGeometry()
        max_height = int(screen.height() * 0.85)
        self.setMaximumHeight(max_height)

        # Start with very compact size for laptops
        self.resize(600, min(550, max_height))

        self.setup_ui()
        
        # Load existing term data if editing
        if term_id and db_manager:
            self.load_term_data()
    
    def setup_ui(self):
        """Setup the user interface"""
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
        header = QLabel("📖 Glossary Entry Editor")
        header.setStyleSheet("font-size: 12px; font-weight: bold; color: #333; padding: 4px;")
        layout.addWidget(header)
        
        # Terms group
        terms_group = QGroupBox("Terms")
        terms_layout = QVBoxLayout()
        terms_layout.setSpacing(4)
        
        # Source term
        source_label = QLabel("Source Term:")
        source_label.setStyleSheet("font-weight: bold;")
        terms_layout.addWidget(source_label)
        
        self.source_edit = QLineEdit()
        self.source_edit.setPlaceholderText("Enter source language term...")
        self.source_edit.setStyleSheet("padding: 6px; font-size: 11px;")
        terms_layout.addWidget(self.source_edit)
        
        # Target term
        target_label = QLabel("Target Term:")
        target_label.setStyleSheet("font-weight: bold;")
        terms_layout.addWidget(target_label)
        
        self.target_edit = QLineEdit()
        self.target_edit.setPlaceholderText("Enter target language term...")
        self.target_edit.setStyleSheet("padding: 6px; font-size: 11px;")
        terms_layout.addWidget(self.target_edit)
        
        terms_group.setLayout(terms_layout)
        layout.addWidget(terms_group)
        
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
        
        source_syn_info = QLabel("Alternative source terms. First item = preferred:")
        source_syn_info.setStyleSheet("color: #666; font-size: 10px;")
        source_syn_layout.addWidget(source_syn_info)
        
        source_add_layout = QHBoxLayout()
        self.source_synonym_edit = QLineEdit()
        self.source_synonym_edit.setPlaceholderText("Enter source synonym...")
        self.source_synonym_edit.setStyleSheet("padding: 4px; font-size: 10px;")
        source_add_layout.addWidget(self.source_synonym_edit)
        
        self.source_synonym_forbidden_check = CheckmarkCheckBox("Forbidden")
        self.source_synonym_forbidden_check.setStyleSheet("font-size: 10px;")
        source_add_layout.addWidget(self.source_synonym_forbidden_check)
        
        source_add_btn = QPushButton("Add")
        source_add_btn.setMaximumWidth(50)
        source_add_btn.setStyleSheet("padding: 4px; font-size: 10px;")
        source_add_btn.clicked.connect(self.add_source_synonym)
        source_add_layout.addWidget(source_add_btn)
        source_syn_layout.addLayout(source_add_layout)
        
        self.source_synonym_edit.returnPressed.connect(self.add_source_synonym)
        
        source_list_layout = QHBoxLayout()
        self.source_synonym_list = QListWidget()
        self.source_synonym_list.setMaximumHeight(80)
        self.source_synonym_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.source_synonym_list.customContextMenuRequested.connect(self.show_source_synonym_context_menu)
        source_list_layout.addWidget(self.source_synonym_list)
        
        source_btn_col = QVBoxLayout()
        source_up_btn = QPushButton("▲")
        source_up_btn.setMaximumWidth(25)
        source_up_btn.setToolTip("Move up")
        source_up_btn.clicked.connect(lambda: self.move_synonym(self.source_synonym_list, -1))
        source_btn_col.addWidget(source_up_btn)
        
        source_down_btn = QPushButton("▼")
        source_down_btn.setMaximumWidth(25)
        source_down_btn.setToolTip("Move down")
        source_down_btn.clicked.connect(lambda: self.move_synonym(self.source_synonym_list, 1))
        source_btn_col.addWidget(source_down_btn)
        source_btn_col.addStretch()
        
        source_del_btn = QPushButton("✗")
        source_del_btn.setMaximumWidth(25)
        source_del_btn.setToolTip("Delete")
        source_del_btn.clicked.connect(lambda: self.delete_synonym(self.source_synonym_list))
        source_btn_col.addWidget(source_del_btn)
        
        source_list_layout.addLayout(source_btn_col)
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
        
        target_syn_info = QLabel("Alternative target terms. First item = preferred:")
        target_syn_info.setStyleSheet("color: #666; font-size: 10px;")
        target_syn_layout.addWidget(target_syn_info)
        
        target_add_layout = QHBoxLayout()
        self.target_synonym_edit = QLineEdit()
        self.target_synonym_edit.setPlaceholderText("Enter target synonym...")
        self.target_synonym_edit.setStyleSheet("padding: 4px; font-size: 10px;")
        target_add_layout.addWidget(self.target_synonym_edit)
        
        self.target_synonym_forbidden_check = CheckmarkCheckBox("Forbidden")
        self.target_synonym_forbidden_check.setStyleSheet("font-size: 10px;")
        target_add_layout.addWidget(self.target_synonym_forbidden_check)
        
        target_add_btn = QPushButton("Add")
        target_add_btn.setMaximumWidth(50)
        target_add_btn.setStyleSheet("padding: 4px; font-size: 10px;")
        target_add_btn.clicked.connect(self.add_target_synonym)
        target_add_layout.addWidget(target_add_btn)
        target_syn_layout.addLayout(target_add_layout)
        
        self.target_synonym_edit.returnPressed.connect(self.add_target_synonym)
        
        target_list_layout = QHBoxLayout()
        self.target_synonym_list = QListWidget()
        self.target_synonym_list.setMaximumHeight(80)
        self.target_synonym_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.target_synonym_list.customContextMenuRequested.connect(self.show_target_synonym_context_menu)
        target_list_layout.addWidget(self.target_synonym_list)
        
        target_btn_col = QVBoxLayout()
        target_up_btn = QPushButton("▲")
        target_up_btn.setMaximumWidth(25)
        target_up_btn.setToolTip("Move up")
        target_up_btn.clicked.connect(lambda: self.move_synonym(self.target_synonym_list, -1))
        target_btn_col.addWidget(target_up_btn)
        
        target_down_btn = QPushButton("▼")
        target_down_btn.setMaximumWidth(25)
        target_down_btn.setToolTip("Move down")
        target_down_btn.clicked.connect(lambda: self.move_synonym(self.target_synonym_list, 1))
        target_btn_col.addWidget(target_down_btn)
        target_btn_col.addStretch()
        
        target_del_btn = QPushButton("✗")
        target_del_btn.setMaximumWidth(25)
        target_del_btn.setToolTip("Delete")
        target_del_btn.clicked.connect(lambda: self.delete_synonym(self.target_synonym_list))
        target_btn_col.addWidget(target_del_btn)
        
        target_list_layout.addLayout(target_btn_col)
        target_syn_layout.addLayout(target_list_layout)

        # Add collapsible content to main layout
        target_syn_main_layout.addWidget(self.target_syn_content)
        target_syn_group.setLayout(target_syn_main_layout)

        # Connect toggle button
        self.target_syn_toggle.clicked.connect(lambda: self.toggle_section(self.target_syn_toggle, self.target_syn_content))

        layout.addWidget(target_syn_group)
        
        # Metadata group
        metadata_group = QGroupBox("Metadata")
        metadata_layout = QVBoxLayout()
        metadata_layout.setSpacing(4)
        
        # Priority
        priority_layout = QHBoxLayout()
        priority_label = QLabel("Priority (1=highest, 99=lowest):")
        priority_label.setStyleSheet("font-weight: bold;")
        priority_layout.addWidget(priority_label)
        
        self.priority_spin = QSpinBox()
        self.priority_spin.setMinimum(1)
        self.priority_spin.setMaximum(99)
        self.priority_spin.setValue(50)
        self.priority_spin.setToolTip("Lower numbers = higher priority")
        self.priority_spin.setStyleSheet("padding: 4px; font-size: 11px;")
        priority_layout.addWidget(self.priority_spin)
        priority_layout.addStretch()
        
        metadata_layout.addLayout(priority_layout)
        
        # Domain
        domain_label = QLabel("Domain:")
        domain_label.setStyleSheet("font-weight: bold;")
        metadata_layout.addWidget(domain_label)
        
        self.domain_edit = QLineEdit()
        self.domain_edit.setPlaceholderText("e.g., Patents, Legal, Medical, IT...")
        self.domain_edit.setStyleSheet("padding: 6px; font-size: 11px;")
        metadata_layout.addWidget(self.domain_edit)
        
        # Note
        note_label = QLabel("Note:")
        note_label.setStyleSheet("font-weight: bold;")
        metadata_layout.addWidget(note_label)
        
        self.note_edit = QTextEdit()
        self.note_edit.setPlaceholderText("Usage notes, context, definition, URLs...")
        self.note_edit.setMaximumHeight(45)
        self.note_edit.setStyleSheet("padding: 3px; font-size: 10px;")
        metadata_layout.addWidget(self.note_edit)
        
        # Project
        project_label = QLabel("Project:")
        project_label.setStyleSheet("font-weight: bold;")
        metadata_layout.addWidget(project_label)
        
        self.project_edit = QLineEdit()
        self.project_edit.setPlaceholderText("Optional project name...")
        self.project_edit.setStyleSheet("padding: 6px; font-size: 11px;")
        metadata_layout.addWidget(self.project_edit)
        
        # Client
        client_label = QLabel("Client:")
        client_label.setStyleSheet("font-weight: bold;")
        metadata_layout.addWidget(client_label)
        
        self.client_edit = QLineEdit()
        self.client_edit.setPlaceholderText("Optional client name...")
        self.client_edit.setStyleSheet("padding: 6px; font-size: 11px;")
        metadata_layout.addWidget(self.client_edit)
        
        # Forbidden checkbox
        self.forbidden_check = CheckmarkCheckBox("⚠️ Mark as FORBIDDEN term (do not use)")
        self.forbidden_check.setStyleSheet("font-weight: bold; color: #d32f2f;")
        metadata_layout.addWidget(self.forbidden_check)
        
        metadata_group.setLayout(metadata_layout)
        layout.addWidget(metadata_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        # Delete button (only show when editing existing term)
        if self.term_id:
            self.delete_btn = QPushButton("🗑️ Delete")
            self.delete_btn.setStyleSheet("""
                QPushButton {
                    padding: 8px 20px;
                    font-size: 11px;
                    font-weight: bold;
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """)
            self.delete_btn.clicked.connect(self.delete_term)
            buttons_layout.addWidget(self.delete_btn)
        
        buttons_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                font-size: 11px;
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                font-size: 11px;
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.save_btn.clicked.connect(self.save_term)
        buttons_layout.addWidget(self.save_btn)
        
        layout.addLayout(buttons_layout)
        
        # Set the scroll area content
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def toggle_section(self, toggle_btn, content_widget):
        """Toggle visibility of a collapsible section"""
        is_visible = content_widget.isVisible()
        content_widget.setVisible(not is_visible)
        toggle_btn.setText("▼" if is_visible else "▲")

    def add_source_synonym(self):
        """Add source synonym to list"""
        text = self.source_synonym_edit.text().strip()
        if text:
            for i in range(self.source_synonym_list.count()):
                if self.source_synonym_list.item(i).data(Qt.ItemDataRole.UserRole)['text'] == text:
                    QMessageBox.warning(self, "Duplicate", "Synonym already added")
                    return
            
            forbidden = self.source_synonym_forbidden_check.isChecked()
            display = f"{'🚫 ' if forbidden else ''}{text}"
            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, {'text': text, 'forbidden': forbidden})
            if forbidden:
                item.setForeground(QColor('#d32f2f'))
            self.source_synonym_list.addItem(item)
            self.source_synonym_edit.clear()
            self.source_synonym_forbidden_check.setChecked(False)
    
    def add_target_synonym(self):
        """Add target synonym to list"""
        text = self.target_synonym_edit.text().strip()
        if text:
            for i in range(self.target_synonym_list.count()):
                if self.target_synonym_list.item(i).data(Qt.ItemDataRole.UserRole)['text'] == text:
                    QMessageBox.warning(self, "Duplicate", "Synonym already added")
                    return
            
            forbidden = self.target_synonym_forbidden_check.isChecked()
            display = f"{'🚫 ' if forbidden else ''}{text}"
            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, {'text': text, 'forbidden': forbidden})
            if forbidden:
                item.setForeground(QColor('#d32f2f'))
            self.target_synonym_list.addItem(item)
            self.target_synonym_edit.clear()
            self.target_synonym_forbidden_check.setChecked(False)
    
    def move_synonym(self, list_widget, direction):
        """Move synonym up (-1) or down (1)"""
        row = list_widget.currentRow()
        if row < 0:
            return
        new_row = row + direction
        if 0 <= new_row < list_widget.count():
            item = list_widget.takeItem(row)
            list_widget.insertItem(new_row, item)
            list_widget.setCurrentRow(new_row)
    
    def delete_synonym(self, list_widget):
        """Delete selected synonym"""
        row = list_widget.currentRow()
        if row >= 0:
            list_widget.takeItem(row)
    
    def show_source_synonym_context_menu(self, position):
        """Show context menu for source synonyms"""
        self._show_synonym_context_menu(self.source_synonym_list, position)
    
    def show_target_synonym_context_menu(self, position):
        """Show context menu for target synonyms"""
        self._show_synonym_context_menu(self.target_synonym_list, position)
    
    def _show_synonym_context_menu(self, list_widget, position):
        """Show context menu for synonym list"""
        if list_widget.count() == 0:
            return
        
        item = list_widget.currentItem()
        if not item:
            return
        
        menu = QMenu()
        data = item.data(Qt.ItemDataRole.UserRole)
        is_forbidden = data.get('forbidden', False)
        
        toggle_action = menu.addAction("Mark as Allowed" if is_forbidden else "Mark as Forbidden")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")
        
        action = menu.exec(list_widget.mapToGlobal(position))
        
        if action == toggle_action:
            data['forbidden'] = not is_forbidden
            text = data['text']
            display = f"{'🚫 ' if data['forbidden'] else ''}{text}"
            item.setText(display)
            item.setData(Qt.ItemDataRole.UserRole, data)
            item.setForeground(QColor('#d32f2f') if data['forbidden'] else QColor('#000000'))
        elif action == delete_action:
            list_widget.takeItem(list_widget.row(item))
    
    def load_term_data(self):
        """Load existing term data from database"""
        if not self.db_manager or not self.term_id:
            return
        
        try:
            cursor = self.db_manager.cursor
            cursor.execute("""
                SELECT source_term, target_term, priority, domain, definition, forbidden,
                       notes, project, client
                FROM termbase_terms
                WHERE id = ?
            """, (self.term_id,))
            
            row = cursor.fetchone()
            if row:
                self.term_data = {
                    'source_term': row[0],
                    'target_term': row[1],
                    'priority': row[2] or 50,
                    'domain': row[3] or '',
                    'definition': row[4] or '',  # Legacy field
                    'forbidden': row[5] or False,
                    'note': row[6] or '',
                    'project': row[7] or '',
                    'client': row[8] or ''
                }
                
                # Populate fields
                self.source_edit.setText(self.term_data['source_term'])
                self.target_edit.setText(self.term_data['target_term'])
                self.priority_spin.setValue(self.term_data['priority'])
                self.domain_edit.setText(self.term_data['domain'])
                # Use note field if available, otherwise fall back to definition (legacy)
                note_text = self.term_data['note'] or self.term_data['definition']
                self.note_edit.setPlainText(note_text)
                self.project_edit.setText(self.term_data['project'])
                self.client_edit.setText(self.term_data['client'])
                self.forbidden_check.setChecked(self.term_data['forbidden'])
                
                # Load synonyms
                self.load_synonyms()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load term data: {e}")
    
    def load_synonyms(self):
        """Load synonyms for current term"""
        if not self.db_manager or not self.term_id:
            return
        
        try:
            cursor = self.db_manager.cursor
            
            # Check if forbidden column exists (backward compatibility)
            cursor.execute("PRAGMA table_info(termbase_synonyms)")
            columns = [row[1] for row in cursor.fetchall()]
            has_forbidden = 'forbidden' in columns
            has_display_order = 'display_order' in columns
            
            # Load source synonyms
            if has_forbidden and has_display_order:
                cursor.execute("""
                    SELECT synonym_text, forbidden FROM termbase_synonyms
                    WHERE term_id = ? AND language = 'source'
                    ORDER BY display_order ASC
                """, (self.term_id,))
            else:
                cursor.execute("""
                    SELECT synonym_text FROM termbase_synonyms
                    WHERE term_id = ? AND language = 'source'
                    ORDER BY created_date ASC
                """, (self.term_id,))
            
            for row in cursor.fetchall():
                text = row[0]
                forbidden = bool(row[1]) if has_forbidden and len(row) > 1 else False
                display = f"{'🚫 ' if forbidden else ''}{text}"
                item = QListWidgetItem(display)
                item.setData(Qt.ItemDataRole.UserRole, {'text': text, 'forbidden': forbidden})
                if forbidden:
                    item.setForeground(QColor('#d32f2f'))
                self.source_synonym_list.addItem(item)
            
            # Load target synonyms
            if has_forbidden and has_display_order:
                cursor.execute("""
                    SELECT synonym_text, forbidden FROM termbase_synonyms
                    WHERE term_id = ? AND language = 'target'
                    ORDER BY display_order ASC
                """, (self.term_id,))
            else:
                cursor.execute("""
                    SELECT synonym_text FROM termbase_synonyms
                    WHERE term_id = ? AND language = 'target'
                    ORDER BY created_date ASC
                """, (self.term_id,))
            
            for row in cursor.fetchall():
                text = row[0]
                forbidden = bool(row[1]) if has_forbidden and len(row) > 1 else False
                display = f"{'🚫 ' if forbidden else ''}{text}"
                item = QListWidgetItem(display)
                item.setData(Qt.ItemDataRole.UserRole, {'text': text, 'forbidden': forbidden})
                if forbidden:
                    item.setForeground(QColor('#d32f2f'))
                self.target_synonym_list.addItem(item)
                
        except Exception as e:
            # Silently fail for backward compatibility
            print(f"Warning: Could not load synonyms: {e}")
    
    def delete_term(self):
        """Delete this term from database"""
        if not self.db_manager or not self.term_id:
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Delete this glossary entry?\n\nSource: {self.source_edit.text()}\nTarget: {self.target_edit.text()}\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.db_manager.cursor
                cursor.execute("DELETE FROM termbase_terms WHERE id = ?", (self.term_id,))
                self.db_manager.connection.commit()
                QMessageBox.information(self, "Success", "Glossary entry deleted")
                self.accept()  # Close dialog with success
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete entry: {e}")
    
    def save_term(self):
        """Save term to database"""
        # Validate inputs
        source_term = self.source_edit.text().strip()
        target_term = self.target_edit.text().strip()
        
        if not source_term or not target_term:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Both source and target terms are required."
            )
            return
        
        if not self.db_manager:
            QMessageBox.critical(
                self,
                "Error",
                "No database connection available."
            )
            return
        
        try:
            cursor = self.db_manager.cursor
            
            # Gather data
            priority = self.priority_spin.value()
            domain = self.domain_edit.text().strip()
            note = self.note_edit.toPlainText().strip()
            project = self.project_edit.text().strip()
            client = self.client_edit.text().strip()
            forbidden = self.forbidden_check.isChecked()
            
            if self.term_id:
                # Update existing term
                cursor.execute("""
                    UPDATE termbase_terms
                    SET source_term = ?, target_term = ?, priority = ?,
                        domain = ?, notes = ?, project = ?, client = ?, forbidden = ?
                    WHERE id = ?
                """, (source_term, target_term, priority, domain, note, project, client, forbidden, self.term_id))
            else:
                # Insert new term
                cursor.execute("""
                    INSERT INTO termbase_terms
                    (termbase_id, source_term, target_term, priority, domain, notes, project, client, forbidden)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.termbase_id, source_term, target_term, priority, domain, note, project, client, forbidden))
            
            self.db_manager.connection.commit()
            
            # Save synonyms (get the term_id if this was a new term)
            if not self.term_id:
                self.term_id = cursor.lastrowid
            
            self.save_synonyms()
            
            # Success
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save term: {e}"
            )
    
    def save_synonyms(self):
        """Save synonyms to database"""
        if not self.db_manager or not self.term_id:
            return
        
        try:
            cursor = self.db_manager.cursor
            
            # Delete existing synonyms for this term
            cursor.execute("DELETE FROM termbase_synonyms WHERE term_id = ?", (self.term_id,))
            
            # Save source synonyms
            for i in range(self.source_synonym_list.count()):
                item = self.source_synonym_list.item(i)
                data = item.data(Qt.ItemDataRole.UserRole)
                cursor.execute("""
                    INSERT INTO termbase_synonyms (term_id, synonym_text, language, display_order, forbidden)
                    VALUES (?, ?, 'source', ?, ?)
                """, (self.term_id, data['text'], i, 1 if data['forbidden'] else 0))
            
            # Save target synonyms
            for i in range(self.target_synonym_list.count()):
                item = self.target_synonym_list.item(i)
                data = item.data(Qt.ItemDataRole.UserRole)
                cursor.execute("""
                    INSERT INTO termbase_synonyms (term_id, synonym_text, language, display_order, forbidden)
                    VALUES (?, ?, 'target', ?, ?)
                """, (self.term_id, data['text'], i, 1 if data['forbidden'] else 0))
            
            self.db_manager.connection.commit()
            
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to save synonyms: {e}")
    
    def get_term_data(self) -> Optional[dict]:
        """Get the current term data from the form fields"""
        return {
            'source_term': self.source_edit.text().strip(),
            'target_term': self.target_edit.text().strip(),
            'priority': self.priority_spin.value(),
            'domain': self.domain_edit.text().strip(),
            'note': self.note_edit.toPlainText().strip(),
            'project': self.project_edit.text().strip(),
            'client': self.client_edit.text().strip(),
            'forbidden': self.forbidden_check.isChecked()
        }
