"""
Encoding Repair Module - Qt Edition
Embeddable version of the text encoding repair tool for detecting and fixing mojibake/encoding corruption

This module can be embedded in the main Supervertaler Qt application as a tab.
Can also be run independently as a standalone application.
"""

import os
import sys
from pathlib import Path

# Fix import path for standalone mode - must be done before any module imports
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QMessageBox, QPlainTextEdit, QGroupBox, QFrame, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextOption

from modules.encoding_repair import EncodingRepair


class EncodingRepairQt:
    """
    Encoding Repair feature - detect and fix text encoding corruption (mojibake)
    Can be embedded in any PyQt6 application as a tab or panel
    """
    
    def __init__(self, parent_app, standalone=False):
        """
        Initialize Encoding Repair module
        
        Args:
            parent_app: Reference to the main application (optional, for logging)
            standalone: If True, running as standalone app. If False, embedded in Supervertaler
        """
        self.parent_app = parent_app
        self.standalone = standalone
        
        # Initialize logging
        self.log = parent_app.log if hasattr(parent_app, 'log') else print
        
        # State
        self.selected_path = None
        self.is_folder = False
        
    def log_message(self, message: str):
        """Log a message to the parent app's log if available"""
        if hasattr(self.parent_app, 'log'):
            self.parent_app.log(f"[Encoding Repair] {message}")
        else:
            print(f"[Encoding Repair] {message}")
    
    def create_tab(self, parent: QWidget):
        """
        Create the Encoding Repair tab UI
        
        Args:
            parent: The QWidget container for the tab
        """
        # Main layout
        main_layout = QVBoxLayout(parent)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # ===== HEADER: Standard Template (matches PDF Rescue / TMX Editor style) =====
        header = QLabel("🔧 Encoding Repair")
        header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
        main_layout.addWidget(header, 0)  # 0 = no stretch, stays compact
        
        # Description box (matches Universal Lookup / PDF Rescue / TMX Editor style)
        description = QLabel(
            "Detect and fix text encoding corruption (mojibake) in translation files.\n"
            "Automatically repairs UTF-8 text incorrectly decoded as Latin-1 or Windows-1252."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
        main_layout.addWidget(description, 0)  # 0 = no stretch, stays compact
        
        # ===== FILE SELECTION SECTION =====
        file_group = QGroupBox("📁 Select File or Folder")
        file_layout = QVBoxLayout(file_group)
        file_layout.setSpacing(10)
        
        # Selected path display
        self.path_label = QLabel("No file or folder selected")
        self.path_label.setWordWrap(True)
        self.path_label.setStyleSheet("color: #666; padding: 5px; background-color: #F5F5F5; border-radius: 3px;")
        file_layout.addWidget(self.path_label)
        
        # Selection buttons
        select_layout = QHBoxLayout()
        select_layout.setSpacing(10)
        
        select_file_btn = QPushButton("📄 Select File")
        select_file_btn.clicked.connect(self._select_file)
        select_file_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 6px 12px;")
        select_layout.addWidget(select_file_btn)
        
        select_folder_btn = QPushButton("📁 Select Folder")
        select_folder_btn.clicked.connect(self._select_folder)
        select_folder_btn.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; padding: 6px 12px;")
        select_layout.addWidget(select_folder_btn)
        
        select_layout.addStretch()
        file_layout.addLayout(select_layout)
        
        main_layout.addWidget(file_group, 0)
        
        # ===== ACTIONS SECTION =====
        action_group = QGroupBox("🔍 Detect & Repair")
        action_layout = QVBoxLayout(action_group)
        action_layout.setSpacing(10)
        
        # Action buttons
        action_btn_layout = QHBoxLayout()
        action_btn_layout.setSpacing(10)
        
        scan_btn = QPushButton("🔍 Scan for Corruption")
        scan_btn.clicked.connect(self._scan_files)
        scan_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 6px 12px;")
        action_btn_layout.addWidget(scan_btn)
        
        repair_btn = QPushButton("✅ Repair Files")
        repair_btn.clicked.connect(self._repair_files)
        repair_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 6px 12px;")
        action_btn_layout.addWidget(repair_btn)
        
        clear_btn = QPushButton("❌ Clear")
        clear_btn.clicked.connect(self._clear_results)
        clear_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 6px 12px;")
        action_btn_layout.addWidget(clear_btn)
        
        action_btn_layout.addStretch()
        action_layout.addLayout(action_btn_layout)
        
        main_layout.addWidget(action_group, 0)
        
        # ===== RESULTS SECTION =====
        results_group = QGroupBox("📊 Results")
        results_layout = QVBoxLayout(results_group)
        results_layout.setContentsMargins(5, 5, 5, 5)
        
        self.results_text = QPlainTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Consolas", 9))
        self.results_text.setStyleSheet("""
            QPlainTextEdit {
                background-color: #F5F5F5;
                border: 1px solid #DDD;
                border-radius: 3px;
            }
        """)
        results_layout.addWidget(self.results_text, 1)  # 1 = stretch factor
        
        main_layout.addWidget(results_group, 1)  # 1 = stretch factor, expands to fill space
    
    def _select_file(self):
        """Select a single file for encoding repair"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select file to scan",
            "", "Text files (*.txt);;All files (*.*)"
        )
        if file_path:
            self.selected_path = file_path
            self.is_folder = False
            self.path_label.setText(f"File: {file_path}")
            self.log_message(f"Selected file: {file_path}")
    
    def _select_folder(self):
        """Select a folder for encoding repair"""
        folder_path = QFileDialog.getExistingDirectory(
            None, "Select folder to scan"
        )
        if folder_path:
            self.selected_path = folder_path
            self.is_folder = True
            self.path_label.setText(f"Folder: {folder_path}")
            self.log_message(f"Selected folder: {folder_path}")
    
    def _scan_files(self):
        """Scan selected file(s) for encoding corruption"""
        if not self.selected_path:
            QMessageBox.warning(None, "No Selection", "Please select a file or folder first.")
            return
        
        # Clear results
        self.results_text.clear()
        self.results_text.appendPlainText("Scanning for encoding corruption...\n")
        QApplication.processEvents()
        
        try:
            if self.is_folder:
                # Scan all text files in folder
                folder = Path(self.selected_path)
                text_files = list(folder.rglob('*.txt'))
                
                if not text_files:
                    self.results_text.appendPlainText("⚠️ No text files found in folder\n")
                    return
                
                self.results_text.appendPlainText(f"Scanning {len(text_files)} file(s)...\n\n")
                QApplication.processEvents()
                
                total_corruptions = 0
                files_with_corruption = 0
                
                for filepath in text_files:
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        has_corruption, corruption_count, patterns = EncodingRepair.detect_corruption(content)
                        
                        if has_corruption:
                            files_with_corruption += 1
                            total_corruptions += corruption_count
                            
                            self.results_text.appendPlainText(f"📄 {filepath.name}\n")
                            self.results_text.appendPlainText(f"  ✓ Found {corruption_count} corruption(s)\n")
                            for pattern in patterns:
                                self.results_text.appendPlainText(f"    • {pattern}\n")
                            self.results_text.appendPlainText("\n")
                    except Exception as e:
                        self.results_text.appendPlainText(f"❌ Error reading {filepath.name}: {str(e)}\n")
                    
                    QApplication.processEvents()
                
                self.results_text.appendPlainText("\n--- Summary ---\n")
                self.results_text.appendPlainText(f"Files with corruption: {files_with_corruption}\n")
                self.results_text.appendPlainText(f"Total corruptions found: {total_corruptions}\n")
                
            else:
                # Scan single file
                try:
                    with open(self.selected_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    has_corruption, corruption_count, patterns = EncodingRepair.detect_corruption(content)
                    
                    filename = Path(self.selected_path).name
                    
                    if has_corruption:
                        self.results_text.appendPlainText(f"📄 {filename}\n")
                        self.results_text.appendPlainText("✓ Encoding corruption detected!\n\n")
                        self.results_text.appendPlainText(f"Found {corruption_count} corruption pattern(s):\n\n")
                        for pattern in patterns:
                            self.results_text.appendPlainText(f"  • {pattern}\n")
                    else:
                        self.results_text.appendPlainText(f"📄 {filename}\n")
                        self.results_text.appendPlainText("✓ No encoding corruption found\n")
                        
                except Exception as e:
                    self.results_text.appendPlainText(f"❌ Error: {str(e)}\n")
            
            self.log_message("Scan completed")
            
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to scan files:\n\n{str(e)}")
            self.log_message(f"Scan error: {str(e)}")
    
    def _repair_files(self):
        """Fix encoding corruption in selected file(s)"""
        if not self.selected_path:
            QMessageBox.warning(None, "No Selection", "Please select a file or folder first.")
            return
        
        # Confirm before repair
        if self.is_folder:
            msg = f"Repair all text files in folder?\n\n{self.selected_path}\n\nA backup will be created for each file."
        else:
            msg = f"Repair file?\n\n{Path(self.selected_path).name}\n\nA backup will be created."
        
        reply = QMessageBox.question(
            None, "Confirm Repair", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Append to results
        self.results_text.appendPlainText("\n--- Repair Process ---\n")
        QApplication.processEvents()
        
        try:
            if self.is_folder:
                # Repair all text files in folder
                folder = Path(self.selected_path)
                text_files = list(folder.rglob('*.txt'))
                
                if not text_files:
                    self.results_text.appendPlainText("⚠️ No text files found\n")
                    return
                
                repaired_count = 0
                for filepath in text_files:
                    try:
                        # Create backup
                        backup_path = f"{filepath}.backup"
                        with open(filepath, 'rb') as f_src:
                            with open(backup_path, 'wb') as f_dst:
                                f_dst.write(f_src.read())
                        
                        # Repair
                        success, message, stats = EncodingRepair.repair_file(str(filepath))
                        
                        if success:
                            if stats.get('has_corruption', False):
                                repaired_count += 1
                                self.results_text.appendPlainText(f"✅ {filepath.name}\n")
                                self.results_text.appendPlainText(f"   Fixed {stats.get('corruption_count', 0)} corruption(s)\n")
                            else:
                                self.results_text.appendPlainText(f"ℹ️  {filepath.name} (no corruption found)\n")
                        else:
                            self.results_text.appendPlainText(f"❌ {filepath.name}: {message}\n")
                        
                        QApplication.processEvents()
                        
                    except Exception as e:
                        self.results_text.appendPlainText(f"❌ Error repairing {filepath.name}: {str(e)}\n")
                
                self.results_text.appendPlainText(f"\n✅ Repaired {repaired_count}/{len(text_files)} file(s)\n")
                QMessageBox.information(None, "Repair Complete", f"Repaired {repaired_count} file(s) in folder.")
                
            else:
                # Repair single file
                # Create backup
                backup_path = f"{self.selected_path}.backup"
                with open(self.selected_path, 'rb') as f_src:
                    with open(backup_path, 'wb') as f_dst:
                        f_dst.write(f_src.read())
                
                # Repair
                success, message, stats = EncodingRepair.repair_file(self.selected_path)
                
                if success:
                    self.results_text.appendPlainText(message + "\n")
                    if 'corruption_count' in stats and stats['corruption_count'] > 0:
                        self.results_text.appendPlainText(f"File size: {stats.get('original_size', 0)} → {stats.get('repaired_size', 0)} bytes\n")
                        self.results_text.appendPlainText(f"Backup created: {backup_path}\n")
                    QMessageBox.information(None, "Success", f"File repaired successfully!\n\nBackup saved as: {backup_path}")
                else:
                    self.results_text.appendPlainText(message + "\n")
                    QMessageBox.critical(None, "Error", f"Repair failed:\n\n{message}")
            
            self.log_message("Repair completed")
            
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to repair files:\n\n{str(e)}")
            self.log_message(f"Repair error: {str(e)}")
    
    def _clear_results(self):
        """Clear the results display"""
        self.results_text.clear()


# === Standalone Application ===

if __name__ == "__main__":
    """Run Encoding Repair as a standalone application"""
    from PyQt6.QtWidgets import QMainWindow
    
    class StandaloneApp(QMainWindow):
        """Minimal parent app for standalone mode"""
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Encoding Repair Tool - Text Encoding Corruption Fixer")
            self.setGeometry(100, 100, 900, 700)
            
            # Create central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Create Encoding Repair widget
            self.encoding_repair = EncodingRepairQt(self, standalone=True)
            self.encoding_repair.create_tab(central_widget)
        
        def log(self, message: str):
            """Simple log method for standalone mode"""
            print(message)
    
    # Create and run application
    app = QApplication(sys.argv)
    window = StandaloneApp()
    window.show()
    sys.exit(app.exec())

