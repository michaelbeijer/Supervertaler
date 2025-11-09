"""
AI Assistant File Viewer Dialog

Dialog for viewing attached file content in markdown format.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QGroupBox, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime


class FileViewerDialog(QDialog):
    """
    Dialog for viewing attached file content.

    Shows:
    - Original filename
    - File type and size
    - Attached date
    - Converted markdown content (read-only)
    - Copy to clipboard button
    """

    def __init__(self, file_data: dict, parent=None):
        """
        Initialize the file viewer dialog.

        Args:
            file_data: Dictionary with file metadata and content
            parent: Parent widget
        """
        super().__init__(parent)

        self.file_data = file_data
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("View Attached File")
        self.setModal(True)
        self.resize(800, 600)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # File info group
        info_group = QGroupBox("File Information")
        info_layout = QVBoxLayout(info_group)

        # Original filename
        name_label = QLabel(f"<b>Filename:</b> {self.file_data.get('original_name', 'Unknown')}")
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)

        # File type and size
        file_type = self.file_data.get('file_type', 'Unknown')
        size_bytes = self.file_data.get('size_bytes', 0)
        size_kb = size_bytes / 1024

        if size_kb < 1024:
            size_str = f"{size_kb:.1f} KB"
        else:
            size_str = f"{size_kb / 1024:.1f} MB"

        type_size_label = QLabel(f"<b>Type:</b> {file_type} &nbsp;&nbsp; <b>Size:</b> {size_str}")
        info_layout.addWidget(type_size_label)

        # Attached date
        attached_at = self.file_data.get('attached_at', '')
        if attached_at:
            try:
                # Parse ISO format date
                dt = datetime.fromisoformat(attached_at)
                date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                date_str = attached_at
        else:
            date_str = "Unknown"

        date_label = QLabel(f"<b>Attached:</b> {date_str}")
        info_layout.addWidget(date_label)

        layout.addWidget(info_group)

        # Content group
        content_group = QGroupBox("Converted Content (Markdown)")
        content_layout = QVBoxLayout(content_group)

        # Content viewer (read-only text editor)
        self.content_viewer = QTextEdit()
        self.content_viewer.setReadOnly(True)
        self.content_viewer.setFont(QFont("Consolas", 9))

        # Set content
        content = self.file_data.get('content', '')
        if content:
            self.content_viewer.setPlainText(content)
        else:
            self.content_viewer.setPlainText("(No content available)")

        # Move cursor to top
        cursor = self.content_viewer.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.content_viewer.setTextCursor(cursor)

        content_layout.addWidget(self.content_viewer)

        layout.addWidget(content_group)

        # Button bar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        # Copy button
        copy_btn = QPushButton("📋 Copy to Clipboard")
        copy_btn.setToolTip("Copy content to clipboard")
        copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(copy_btn)

        button_layout.addStretch()

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setDefault(True)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def copy_to_clipboard(self):
        """Copy content to clipboard"""
        content = self.file_data.get('content', '')
        if content:
            clipboard = QApplication.clipboard()
            clipboard.setText(content)

            QMessageBox.information(
                self,
                "Copied",
                "Content copied to clipboard.",
                QMessageBox.StandardButton.Ok
            )
        else:
            QMessageBox.warning(
                self,
                "No Content",
                "No content available to copy.",
                QMessageBox.StandardButton.Ok
            )


class FileRemoveConfirmDialog(QDialog):
    """
    Confirmation dialog for removing attached files.
    """

    def __init__(self, filename: str, parent=None):
        """
        Initialize the confirmation dialog.

        Args:
            filename: Name of file to remove
            parent: Parent widget
        """
        super().__init__(parent)

        self.filename = filename
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Confirm Remove File")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Warning icon and message
        msg_label = QLabel(
            f"⚠️ Are you sure you want to remove this file?\n\n"
            f"<b>{self.filename}</b>\n\n"
            f"The file will be permanently deleted from disk."
        )
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg_label)

        # Button bar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setDefault(True)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        # Remove button
        remove_btn = QPushButton("Remove File")
        remove_btn.setStyleSheet("background-color: #d32f2f; color: white;")
        remove_btn.clicked.connect(self.accept)
        button_layout.addWidget(remove_btn)

        layout.addLayout(button_layout)
