"""
Supercleaner UI Module for Supervertaler
========================================

Interactive UI for document cleaning with selectable operations.
Inspired by TransTools Document Cleaner, Unbreaker, and CodeZapper.

Author: Michael Beijer / Supervertaler
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox,
    QPushButton, QLabel, QFileDialog, QMessageBox, QTextEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import os
from typing import Optional, Dict


class SupercleanerUI(QWidget):
    """Interactive UI for document cleaning with selectable operations"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # === FILE SELECTION ===
        file_group = QGroupBox("📄 Document Selection")
        file_layout = QVBoxLayout()

        # File path display and browse button
        file_row = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #666; padding: 5px; background-color: #f0f0f0; border-radius: 3px;")
        browse_btn = QPushButton("📂 Browse...")
        browse_btn.clicked.connect(self.browse_file)
        browse_btn.setMaximumWidth(150)
        
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(browse_btn, 0)
        file_layout.addLayout(file_row)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # === CLEANING OPTIONS ===
        # Create scrollable area for options
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        options_container = QWidget()
        options_layout = QVBoxLayout(options_container)
        
        # Document Cleaner Operations
        cleaner_group = QGroupBox("🧹 Document Cleaner Operations")
        cleaner_layout = QVBoxLayout()
        
        self.cb_remove_shading = CheckmarkCheckBox("Remove text shading")
        self.cb_remove_highlighting = CheckmarkCheckBox("Remove text highlighting")
        self.cb_font_color_automatic = CheckmarkCheckBox("Change font color from Black to Automatic")
        self.cb_normalize_font_color = CheckmarkCheckBox("Normalize font color in each paragraph")
        self.cb_normalize_font_size = CheckmarkCheckBox("Normalize font size in each paragraph")
        self.cb_normalize_font = CheckmarkCheckBox("Normalize font in each paragraph")
        self.cb_set_default_spacing = CheckmarkCheckBox("Set default text spacing")
        self.cb_remove_hyphens = CheckmarkCheckBox("Remove manual hyphens")
        self.cb_replace_symbols = CheckmarkCheckBox("Replace special symbols (non-breaking spaces, ellipsis)")
        self.cb_replace_symbols.setToolTip("Replaces non-breaking spaces and ellipsis characters that can cause TM matching issues")
        self.cb_simplify_quotes = CheckmarkCheckBox("Simplify quotes & dashes to ASCII (optional)")
        self.cb_simplify_quotes.setToolTip("Convert curly quotes ("")  and em-dashes (—) to straight quotes (\") and hyphens (-)")
        self.cb_remove_styles = CheckmarkCheckBox("Remove character styles (aggressive)")
        
        # Set defaults (checked)
        for cb in [self.cb_remove_shading, self.cb_remove_highlighting, 
                   self.cb_font_color_automatic, self.cb_normalize_font_color,
                   self.cb_normalize_font_size, self.cb_normalize_font,
                   self.cb_set_default_spacing, self.cb_remove_hyphens,
                   self.cb_replace_symbols]:
            cb.setChecked(True)
            cleaner_layout.addWidget(cb)
        
        # Optional operations unchecked by default
        cleaner_layout.addWidget(self.cb_simplify_quotes)  # New optional operation
        cleaner_layout.addWidget(self.cb_remove_styles)
        
        cleaner_group.setLayout(cleaner_layout)
        options_layout.addWidget(cleaner_group)

        # Unbreaker Operations
        unbreaker_group = QGroupBox("🔗 Unbreaker Operations")
        unbreaker_layout = QVBoxLayout()
        
        self.cb_fix_line_breaks = CheckmarkCheckBox("Fix incorrect line breaks (within paragraphs)")
        self.cb_join_sentences = CheckmarkCheckBox("Join broken sentences (across paragraphs) - EXPERIMENTAL")
        
        self.cb_fix_line_breaks.setChecked(True)
        # join_sentences disabled by default due to word spacing issues
        self.cb_join_sentences.setChecked(False)
        self.cb_join_sentences.setStyleSheet("color: #d32f2f;")
        self.cb_join_sentences.setToolTip(
            "⚠️ WARNING: This feature is experimental and may cause words to stick together.\n"
            "Only enable if you need to fix severely broken paragraph structure."
        )
        
        unbreaker_layout.addWidget(self.cb_fix_line_breaks)
        unbreaker_layout.addWidget(self.cb_join_sentences)
        
        unbreaker_group.setLayout(unbreaker_layout)
        options_layout.addWidget(unbreaker_group)

        # Space Removal Operations
        spaces_group = QGroupBox("␣ Remove Excessive Spaces")
        spaces_layout = QVBoxLayout()
        
        self.cb_remove_spaces = CheckmarkCheckBox("Remove excessive spaces (2+ spaces become 1)")
        self.cb_remove_spaces.setChecked(True)
        
        spaces_layout.addWidget(self.cb_remove_spaces)
        spaces_group.setLayout(spaces_layout)
        options_layout.addWidget(spaces_group)

        # Quick presets
        presets_layout = QHBoxLayout()
        quick_clean_btn = QPushButton("✨ Quick Clean (Recommended)")
        quick_clean_btn.clicked.connect(self.apply_quick_clean_preset)
        quick_clean_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px;")
        
        aggressive_btn = QPushButton("⚡ Aggressive Clean")
        aggressive_btn.clicked.connect(self.apply_aggressive_preset)
        aggressive_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 5px;")
        
        clear_all_btn = QPushButton("❌ Clear All")
        clear_all_btn.clicked.connect(self.clear_all_options)
        
        presets_layout.addWidget(quick_clean_btn)
        presets_layout.addWidget(aggressive_btn)
        presets_layout.addWidget(clear_all_btn)
        options_layout.addLayout(presets_layout)
        
        scroll_area.setWidget(options_container)
        main_layout.addWidget(scroll_area, 1)

        # === CLEAN BUTTON ===
        clean_btn = QPushButton("🧹 Clean Document")
        clean_btn.clicked.connect(self.clean_document)
        clean_btn.setStyleSheet(
            "background-color: #2196F3; color: white; font-weight: bold; "
            "font-size: 14pt; padding: 10px; border-radius: 5px;"
        )
        main_layout.addWidget(clean_btn)

        # === RESULTS LOG ===
        log_group = QGroupBox("📊 Cleaning Results")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("background-color: #f5f5f5; font-family: Consolas, monospace;")
        
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        # Initial message
        self.log("👋 Welcome to Supercleaner! Select a DOCX file and choose cleaning operations.")
        self.log("💡 Tip: Use 'Quick Clean' preset for most OCR/PDF documents.")

    def browse_file(self):
        """Open file browser to select DOCX file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select DOCX File to Clean",
            "",
            "Word Documents (*.docx);;All Files (*.*)"
        )
        
        if file_path:
            self.file_label.setText(file_path)
            self.log(f"📄 Selected: {os.path.basename(file_path)}")

    def apply_quick_clean_preset(self):
        """Apply recommended quick clean settings"""
        # Document Cleaner
        self.cb_remove_shading.setChecked(True)
        self.cb_remove_highlighting.setChecked(True)
        self.cb_font_color_automatic.setChecked(True)
        self.cb_normalize_font_color.setChecked(True)
        self.cb_normalize_font_size.setChecked(True)
        self.cb_normalize_font.setChecked(True)
        self.cb_set_default_spacing.setChecked(True)
        self.cb_remove_hyphens.setChecked(True)
        self.cb_replace_symbols.setChecked(True)
        self.cb_simplify_quotes.setChecked(False)  # Optional - preserves curly quotes by default
        self.cb_remove_styles.setChecked(False)
        
        # Unbreaker
        self.cb_fix_line_breaks.setChecked(True)
        self.cb_join_sentences.setChecked(False)  # Disabled due to spacing issues
        
        # Spaces
        self.cb_remove_spaces.setChecked(True)
        
        self.log("✨ Applied 'Quick Clean' preset (recommended for OCR/PDF documents)")

    def apply_aggressive_preset(self):
        """Apply aggressive cleaning settings"""
        # Check everything
        for cb in [self.cb_remove_shading, self.cb_remove_highlighting,
                   self.cb_font_color_automatic, self.cb_normalize_font_color,
                   self.cb_normalize_font_size, self.cb_normalize_font,
                   self.cb_set_default_spacing, self.cb_remove_hyphens,
                   self.cb_replace_symbols, self.cb_simplify_quotes,
                   self.cb_remove_styles, self.cb_fix_line_breaks,
                   self.cb_remove_spaces]:
            cb.setChecked(True)
        
        # Keep sentence joining disabled (known issues)
        self.cb_join_sentences.setChecked(False)
        
        self.log("⚡ Applied 'Aggressive Clean' preset")
        self.log("⚠️  Note: 'Join broken sentences' remains disabled due to known spacing issues")

    def clear_all_options(self):
        """Clear all cleaning options"""
        for cb in [self.cb_remove_shading, self.cb_remove_highlighting,
                   self.cb_font_color_automatic, self.cb_normalize_font_color,
                   self.cb_normalize_font_size, self.cb_normalize_font,
                   self.cb_set_default_spacing, self.cb_remove_hyphens,
                   self.cb_replace_symbols, self.cb_simplify_quotes,
                   self.cb_remove_styles, self.cb_fix_line_breaks,
                   self.cb_join_sentences, self.cb_remove_spaces]:
            cb.setChecked(False)
        
        self.log("❌ Cleared all cleaning options")

    def get_selected_operations(self) -> Dict[str, bool]:
        """Get dictionary of selected cleaning operations"""
        return {
            'remove_text_shading': self.cb_remove_shading.isChecked(),
            'remove_highlighting': self.cb_remove_highlighting.isChecked(),
            'font_color_to_automatic': self.cb_font_color_automatic.isChecked(),
            'normalize_font_color': self.cb_normalize_font_color.isChecked(),
            'normalize_font_size': self.cb_normalize_font_size.isChecked(),
            'normalize_font': self.cb_normalize_font.isChecked(),
            'set_default_spacing': self.cb_set_default_spacing.isChecked(),
            'remove_manual_hyphens': self.cb_remove_hyphens.isChecked(),
            'replace_special_symbols': self.cb_replace_symbols.isChecked(),
            'simplify_quotes_and_dashes': self.cb_simplify_quotes.isChecked(),
            'remove_character_styles': self.cb_remove_styles.isChecked(),
            'fix_line_breaks': self.cb_fix_line_breaks.isChecked(),
            'join_broken_sentences': self.cb_join_sentences.isChecked(),
            'remove_excessive_spaces': self.cb_remove_spaces.isChecked(),
            'accept_tracked_changes': False,  # Not yet implemented
        }

    def clean_document(self):
        """Perform document cleaning with selected operations"""
        # Validate file selection
        file_path = self.file_label.text()
        if file_path == "No file selected" or not os.path.exists(file_path):
            QMessageBox.warning(
                self,
                "No File Selected",
                "Please select a DOCX file to clean."
            )
            return

        # Get selected operations
        operations = self.get_selected_operations()
        
        # Check if any operations are selected
        if not any(operations.values()):
            QMessageBox.warning(
                self,
                "No Operations Selected",
                "Please select at least one cleaning operation."
            )
            return

        # Ask for output file
        default_output = file_path.replace('.docx', '_cleaned.docx')
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Cleaned Document As",
            default_output,
            "Word Documents (*.docx);;All Files (*.*)"
        )
        
        if not output_path:
            return

        # Perform cleaning
        self.log("━" * 60)
        self.log(f"🧹 Starting Supercleaner...")
        self.log(f"📄 Input: {os.path.basename(file_path)}")
        self.log(f"💾 Output: {os.path.basename(output_path)}")
        self.log("")

        try:
            from modules.supercleaner import DocumentCleaner
            
            cleaner = DocumentCleaner()
            stats = cleaner.clean_document(file_path, output_path, operations)

            self.log("✅ Cleaning Complete!")
            self.log(f"  📊 Paragraphs processed: {stats['paragraphs_processed']}")
            self.log(f"  🔧 Total changes made: {stats['changes_made']}")
            self.log("")
            
            if stats.get('operations'):
                self.log("  📝 Operations performed:")
                for op in stats['operations']:
                    self.log(f"     • {op}")
            
            self.log("")
            self.log(f"✅ Saved to: {output_path}")
            self.log("━" * 60)

            QMessageBox.information(
                self,
                "Success",
                f"Document cleaned successfully!\n\n"
                f"Paragraphs processed: {stats['paragraphs_processed']}\n"
                f"Changes made: {stats['changes_made']}\n\n"
                f"Saved to:\n{output_path}"
            )

        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            self.log("━" * 60)
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to clean document:\n\n{str(e)}"
            )

    def log(self, message: str):
        """Add message to log"""
        self.log_text.append(message)
        # Scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


if __name__ == "__main__":
    """Standalone mode for testing"""
    import sys
    from PyQt6.QtWidgets import QApplication

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

    
    app = QApplication(sys.argv)
    window = SupercleanerUI()
    window.setWindowTitle("Supercleaner - Document Cleaner")
    window.resize(800, 900)
    window.show()
    sys.exit(app.exec())
