"""
Termbase Entry Editor Dialog

Dialog for editing individual termbase entries with all metadata fields.
Can be opened from translation results panel (edit button or right-click menu).
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QSpinBox, QCheckBox, QPushButton, QGroupBox,
    QMessageBox
)
from PyQt6.QtCore import Qt
from typing import Optional


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
        
        self.setWindowTitle("Edit Termbase Entry" if term_id else "New Termbase Entry")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(450)
        
        self.setup_ui()
        
        # Load existing term data if editing
        if term_id and db_manager:
            self.load_term_data()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Header
        header = QLabel("📖 Termbase Entry Editor")
        header.setStyleSheet("font-size: 14px; font-weight: bold; color: #333; padding: 8px;")
        layout.addWidget(header)
        
        # Terms group
        terms_group = QGroupBox("Terms")
        terms_layout = QVBoxLayout()
        terms_layout.setSpacing(6)
        
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
        
        # Metadata group
        metadata_group = QGroupBox("Metadata")
        metadata_layout = QVBoxLayout()
        metadata_layout.setSpacing(6)
        
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
        self.note_edit.setMaximumHeight(80)
        self.note_edit.setStyleSheet("padding: 6px; font-size: 11px;")
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
        self.forbidden_check = QCheckBox("⚠️ Mark as FORBIDDEN term (do not use)")
        self.forbidden_check.setStyleSheet("font-weight: bold; color: #d32f2f;")
        metadata_layout.addWidget(self.forbidden_check)
        
        metadata_group.setLayout(metadata_layout)
        layout.addWidget(metadata_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
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
    
    def load_term_data(self):
        """Load existing term data from database"""
        if not self.db_manager or not self.term_id:
            return
        
        try:
            cursor = self.db_manager.cursor
            cursor.execute("""
                SELECT source_term, target_term, priority, domain, definition, forbidden,
                       note, project, client
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
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load term data: {e}")
    
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
                        domain = ?, note = ?, project = ?, client = ?, forbidden = ?
                    WHERE id = ?
                """, (source_term, target_term, priority, domain, note, project, client, forbidden, self.term_id))
            else:
                # Insert new term
                cursor.execute("""
                    INSERT INTO termbase_terms
                    (termbase_id, source_term, target_term, priority, domain, note, project, client, forbidden)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.termbase_id, source_term, target_term, priority, domain, note, project, client, forbidden))
            
            self.db_manager.connection.commit()
            
            # Success
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save term: {e}"
            )
    
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
