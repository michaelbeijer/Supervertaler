"""
Keyboard Shortcuts Settings Widget
Provides UI for viewing, editing, and managing keyboard shortcuts
"""

from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QDialog,
    QDialogButtonBox, QMessageBox, QFileDialog, QGroupBox, QCheckBox,
    QStyleOptionButton
)
from PyQt6.QtCore import Qt, QEvent, QPointF, QRect
from PyQt6.QtGui import QKeySequence, QKeyEvent, QFont, QPainter, QPen, QColor

from modules.shortcut_manager import ShortcutManager


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

                # Draw checkmark (✓ shape)
                x = indicator_rect.x()
                y = indicator_rect.y()
                w = indicator_rect.width()
                h = indicator_rect.height()

                # Checkmark coordinates (relative to indicator)
                p1 = QPointF(x + w * 0.20, y + h * 0.50)  # Start left
                p2 = QPointF(x + w * 0.40, y + h * 0.70)  # Bottom middle
                p3 = QPointF(x + w * 0.80, y + h * 0.30)  # End right-top

                painter.drawLine(p1, p2)
                painter.drawLine(p2, p3)
                painter.end()


class KeySequenceEdit(QLineEdit):
    """Custom widget for capturing keyboard shortcuts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Press keys or click to edit...")
        self.setReadOnly(False)
        self.current_sequence = ""
        
    def keyPressEvent(self, event: QKeyEvent):
        """Capture key press and convert to shortcut string"""
        # Ignore modifier-only presses
        if event.key() in (Qt.Key.Key_Control, Qt.Key.Key_Shift, 
                          Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            return
        
        # Build key sequence from modifiers + key
        modifiers = event.modifiers()
        key = event.key()
        
        parts = []
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            parts.append("Ctrl")
        if modifiers & Qt.KeyboardModifier.AltModifier:
            parts.append("Alt")
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            parts.append("Shift")
        if modifiers & Qt.KeyboardModifier.MetaModifier:
            parts.append("Meta")
        
        # Get key name
        key_name = QKeySequence(key).toString()
        if key_name:
            parts.append(key_name)
        
        # Create shortcut string
        if parts:
            sequence = "+".join(parts)
            self.setText(sequence)
            self.current_sequence = sequence
        
        event.accept()
    
    def focusInEvent(self, event):
        """Clear on focus for new input"""
        super().focusInEvent(event)
        self.selectAll()


class ShortcutEditDialog(QDialog):
    """Dialog for editing a keyboard shortcut"""
    
    def __init__(self, shortcut_id: str, data: dict, manager: ShortcutManager, parent=None):
        super().__init__(parent)
        self.shortcut_id = shortcut_id
        self.data = data
        self.manager = manager
        
        self.setWindowTitle(f"Edit Shortcut: {data['description']}")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        # Description
        desc_label = QLabel(f"<b>Action:</b> {data['description']}")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Category
        cat_label = QLabel(f"<b>Category:</b> {data['category']}")
        layout.addWidget(cat_label)
        
        # Default shortcut
        default_label = QLabel(f"<b>Default:</b> {data['default']}")
        layout.addWidget(default_label)
        
        layout.addSpacing(10)
        
        # Current shortcut input
        input_layout = QHBoxLayout()
        input_label = QLabel("New Shortcut:")
        self.shortcut_input = KeySequenceEdit()
        self.shortcut_input.setText(data['current'])
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.shortcut_input)
        layout.addLayout(input_layout)
        
        # Reset button
        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_to_default)
        layout.addWidget(reset_btn)
        
        # Conflict warning label
        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: #f44336; font-weight: bold;")
        self.warning_label.setWordWrap(True)
        layout.addWidget(self.warning_label)
        
        layout.addSpacing(10)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept_shortcut)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        # Check for conflicts when text changes
        self.shortcut_input.textChanged.connect(self.check_conflicts)
    
    def reset_to_default(self):
        """Reset to default shortcut"""
        self.shortcut_input.setText(self.data['default'])
    
    def check_conflicts(self):
        """Check for conflicting shortcuts"""
        new_sequence = self.shortcut_input.text()
        if not new_sequence:
            self.warning_label.setText("")
            return
        
        conflicts = self.manager.find_conflicts(self.shortcut_id, new_sequence)
        if conflicts:
            conflict_names = []
            all_shortcuts = self.manager.get_all_shortcuts()
            for conflict_id in conflicts:
                conflict_names.append(all_shortcuts[conflict_id]['description'])
            
            self.warning_label.setText(
                f"⚠️ Warning: This shortcut conflicts with:\n" + 
                "\n".join(f"  • {name}" for name in conflict_names)
            )
        else:
            self.warning_label.setText("")
    
    def accept_shortcut(self):
        """Accept the new shortcut"""
        new_sequence = self.shortcut_input.text()
        
        # Check conflicts one more time
        conflicts = self.manager.find_conflicts(self.shortcut_id, new_sequence)
        if conflicts:
            reply = QMessageBox.question(
                self,
                "Conflict Detected",
                "This shortcut is already in use. Do you want to override it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        # Set the new shortcut
        if new_sequence == self.data['default']:
            # Same as default, remove custom
            self.manager.reset_shortcut(self.shortcut_id)
        else:
            self.manager.set_shortcut(self.shortcut_id, new_sequence)
        
        self.manager.save_shortcuts()
        self.accept()


class KeyboardShortcutsWidget(QWidget):
    """Main widget for keyboard shortcuts settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Store reference to main window
        # Use main window's shortcut manager if available, otherwise create new one
        if hasattr(parent, 'shortcut_manager'):
            self.manager = parent.shortcut_manager
        else:
            self.manager = ShortcutManager()
        self.init_ui()
        self.load_shortcuts()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("<h2>⌨️ Keyboard Shortcuts</h2>")
        layout.addWidget(header)
        
        # Description
        desc = QLabel(
            "View and customize all keyboard shortcuts. Double-click a shortcut to edit it."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Search/Filter
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter by action or shortcut...")
        self.search_input.textChanged.connect(self.filter_shortcuts)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Shortcuts table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Enabled", "Category", "Action", "Shortcut", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)  # Enable column sorting
        self.table.doubleClicked.connect(self.edit_selected_shortcut)
        
        # Style the table
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #2196F3;
                color: white;
            }
        """)
        
        layout.addWidget(self.table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        edit_btn = QPushButton("✏️ Edit Selected")
        edit_btn.clicked.connect(self.edit_selected_shortcut)
        button_layout.addWidget(edit_btn)
        
        reset_btn = QPushButton("🔄 Reset Selected to Default")
        reset_btn.clicked.connect(self.reset_selected)
        button_layout.addWidget(reset_btn)
        
        reset_all_btn = QPushButton("🔄 Reset All to Defaults")
        reset_all_btn.clicked.connect(self.reset_all)
        button_layout.addWidget(reset_all_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Export/Import buttons
        io_group = QGroupBox("Import/Export")
        io_layout = QHBoxLayout(io_group)
        
        export_json_btn = QPushButton("📤 Export Shortcuts (JSON)")
        export_json_btn.clicked.connect(self.export_shortcuts)
        io_layout.addWidget(export_json_btn)
        
        import_json_btn = QPushButton("📥 Import Shortcuts (JSON)")
        import_json_btn.clicked.connect(self.import_shortcuts)
        io_layout.addWidget(import_json_btn)
        
        export_html_btn = QPushButton("📄 Export Cheatsheet (HTML)")
        export_html_btn.clicked.connect(self.export_html_cheatsheet)
        export_html_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        io_layout.addWidget(export_html_btn)
        
        layout.addWidget(io_group)
        
        # Info label
        info = QLabel(
            "💡 Tip: Exported HTML cheatsheets can be printed or saved as PDF for reference."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #666; font-style: italic; margin-top: 5px;")
        layout.addWidget(info)
    
    def load_shortcuts(self):
        """Load shortcuts into the table"""
        # CRITICAL: Disable sorting during table modifications to prevent
        # items from becoming disassociated from their rows (causes vanishing text bug)
        self.table.setSortingEnabled(False)
        
        self.table.setRowCount(0)
        
        all_shortcuts = self.manager.get_all_shortcuts()
        shortcuts_by_category = self.manager.get_shortcuts_by_category()
        
        row = 0
        for category in sorted(shortcuts_by_category.keys()):
            shortcuts = shortcuts_by_category[category]
            
            for shortcut_id, data in sorted(shortcuts, key=lambda x: x[1]["description"]):
                self.table.insertRow(row)
                
                # Enabled checkbox (column 0) - using green checkmark style
                checkbox = CheckmarkCheckBox()
                checkbox.setChecked(data.get("is_enabled", True))
                checkbox.setToolTip("Enable or disable this shortcut")
                # Store shortcut_id in checkbox for reference
                checkbox.setProperty("shortcut_id", shortcut_id)
                checkbox.stateChanged.connect(self._on_enabled_changed)
                # Create a widget container to center the checkbox
                checkbox_container = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_container)
                checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                checkbox_layout.addWidget(checkbox)
                self.table.setCellWidget(row, 0, checkbox_container)
                
                # Category (column 1)
                cat_item = QTableWidgetItem(data["category"])
                cat_item.setData(Qt.ItemDataRole.UserRole, shortcut_id)  # Store ID
                self.table.setItem(row, 1, cat_item)
                
                # Action (column 2)
                action_item = QTableWidgetItem(data["description"])
                self.table.setItem(row, 2, action_item)
                
                # Shortcut (column 3)
                shortcut_item = QTableWidgetItem(data["current"])
                shortcut_font = QFont()
                shortcut_font.setFamily("Courier New")
                shortcut_font.setBold(True)
                shortcut_item.setFont(shortcut_font)
                # Gray out if disabled
                if not data.get("is_enabled", True):
                    shortcut_item.setForeground(Qt.GlobalColor.gray)
                else:
                    shortcut_item.setForeground(Qt.GlobalColor.blue)
                self.table.setItem(row, 3, shortcut_item)
                
                # Status (column 4)
                status = "Custom" if data["is_custom"] else "Default"
                status_item = QTableWidgetItem(status)
                if data["is_custom"]:
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                    status_font = QFont()
                    status_font.setBold(True)
                    status_item.setFont(status_font)
                self.table.setItem(row, 4, status_item)
                
                row += 1
        
        # Re-enable sorting after all modifications are complete
        self.table.setSortingEnabled(True)
    
    def _on_enabled_changed(self, state):
        """Handle checkbox state change for enabling/disabling shortcuts"""
        checkbox = self.sender()
        if checkbox:
            shortcut_id = checkbox.property("shortcut_id")
            if shortcut_id:
                is_enabled = state == Qt.CheckState.Checked.value
                if is_enabled:
                    self.manager.enable_shortcut(shortcut_id)
                else:
                    self.manager.disable_shortcut(shortcut_id)
                self.manager.save_shortcuts()
                # Update the shortcut text color to indicate disabled state
                self._update_shortcut_text_color(shortcut_id, is_enabled)
                # Immediately refresh the actual shortcut enabled states in the main window
                if self.main_window and hasattr(self.main_window, 'refresh_shortcut_enabled_states'):
                    self.main_window.refresh_shortcut_enabled_states()
    
    def _update_shortcut_text_color(self, shortcut_id: str, is_enabled: bool):
        """Update the shortcut text color based on enabled state"""
        for row in range(self.table.rowCount()):
            cat_item = self.table.item(row, 1)
            if cat_item and cat_item.data(Qt.ItemDataRole.UserRole) == shortcut_id:
                shortcut_item = self.table.item(row, 3)
                if shortcut_item:
                    if is_enabled:
                        shortcut_item.setForeground(Qt.GlobalColor.blue)
                    else:
                        shortcut_item.setForeground(Qt.GlobalColor.gray)
                break
    
    def filter_shortcuts(self):
        """Filter shortcuts based on search text"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            action = self.table.item(row, 2).text().lower()
            shortcut = self.table.item(row, 3).text().lower()
            category = self.table.item(row, 1).text().lower()
            
            if search_text in action or search_text in shortcut or search_text in category:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)
    
    def edit_selected_shortcut(self):
        """Edit the selected shortcut"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "No Selection", "Please select a shortcut to edit.")
            return
        
        # Get shortcut ID from Category column (column 1)
        shortcut_id = self.table.item(current_row, 1).data(Qt.ItemDataRole.UserRole)
        all_shortcuts = self.manager.get_all_shortcuts()
        data = all_shortcuts[shortcut_id]
        
        # Open edit dialog
        dialog = ShortcutEditDialog(shortcut_id, data, self.manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_shortcuts()  # Reload to show changes
            QMessageBox.information(
                self, 
                "Shortcut Updated", 
                "The shortcut has been updated. Changes will take effect when you restart the application."
            )
    
    def reset_selected(self):
        """Reset selected shortcut to default"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "No Selection", "Please select a shortcut to reset.")
            return
        
        shortcut_id = self.table.item(current_row, 1).data(Qt.ItemDataRole.UserRole)
        all_shortcuts = self.manager.get_all_shortcuts()
        data = all_shortcuts[shortcut_id]
        
        if not data["is_custom"]:
            QMessageBox.information(self, "Already Default", "This shortcut is already using its default value.")
            return
        
        reply = QMessageBox.question(
            self,
            "Reset Shortcut",
            f"Reset '{data['description']}' to its default shortcut ({data['default']})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.manager.reset_shortcut(shortcut_id)
            self.manager.save_shortcuts()
            self.load_shortcuts()
            QMessageBox.information(self, "Reset Complete", "Shortcut has been reset to default.")
    
    def reset_all(self):
        """Reset all shortcuts to defaults"""
        reply = QMessageBox.question(
            self,
            "Reset All Shortcuts",
            "Are you sure you want to reset ALL shortcuts to their default values?\n\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.manager.reset_all_shortcuts()
            self.manager.save_shortcuts()
            self.load_shortcuts()
            QMessageBox.information(self, "Reset Complete", "All shortcuts have been reset to defaults.")
    
    def export_shortcuts(self):
        """Export shortcuts to JSON file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Shortcuts",
            "supervertaler_shortcuts.json",
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                self.manager.export_shortcuts(Path(file_path))
                QMessageBox.information(
                    self, 
                    "Export Successful", 
                    f"Shortcuts exported to:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Export Failed", 
                    f"Failed to export shortcuts:\n{str(e)}"
                )
    
    def import_shortcuts(self):
        """Import shortcuts from JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Shortcuts",
            "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self,
                "Import Shortcuts",
                "This will replace your current custom shortcuts. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    if self.manager.import_shortcuts(Path(file_path)):
                        self.manager.save_shortcuts()
                        self.load_shortcuts()
                        QMessageBox.information(
                            self, 
                            "Import Successful", 
                            "Shortcuts imported successfully.\n\nChanges will take effect when you restart the application."
                        )
                    else:
                        QMessageBox.critical(
                            self, 
                            "Import Failed", 
                            "Invalid shortcuts file format."
                        )
                except Exception as e:
                    QMessageBox.critical(
                        self, 
                        "Import Failed", 
                        f"Failed to import shortcuts:\n{str(e)}"
                    )
    
    def export_html_cheatsheet(self):
        """Export shortcuts as HTML cheatsheet"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export HTML Cheatsheet",
            "supervertaler_shortcuts.html",
            "HTML Files (*.html)"
        )
        
        if file_path:
            try:
                self.manager.export_html_cheatsheet(Path(file_path))
                
                reply = QMessageBox.question(
                    self,
                    "Export Successful",
                    f"HTML cheatsheet exported to:\n{file_path}\n\nWould you like to open it in your browser?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    import webbrowser
                    webbrowser.open(file_path)
                    
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Export Failed", 
                    f"Failed to export cheatsheet:\n{str(e)}"
                )

