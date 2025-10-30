"""
PyQt6 Grid Demo - Proof of Concept
Shows how Qt's QTableWidget provides superior grid display for translation tools
"""

import sys
import json
from pathlib import Path

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
        QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel,
        QComboBox, QHeaderView, QAbstractItemView
    )
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont, QColor
except ImportError:
    print("PyQt6 not installed. Installing now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
    print("Please run the script again.")
    sys.exit(1)


class QtGridDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.segments = []
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("PyQt6 Grid Demo - Professional Translation Grid")
        self.setGeometry(100, 100, 1400, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Toolbar
        toolbar = QHBoxLayout()
        layout.addLayout(toolbar)
        
        # Font controls
        toolbar.addWidget(QLabel("Font:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems(['Calibri', 'Segoe UI', 'Arial', 'Consolas', 'Verdana'])
        self.font_combo.currentTextChanged.connect(self.update_font)
        toolbar.addWidget(self.font_combo)
        
        toolbar.addWidget(QLabel("Size:"))
        self.size_combo = QComboBox()
        self.size_combo.addItems(['7', '8', '9', '10', '11', '12', '14', '16', '18'])
        self.size_combo.setCurrentText('10')
        self.size_combo.currentTextChanged.connect(self.update_font)
        toolbar.addWidget(self.size_combo)
        
        # Auto-resize button
        resize_btn = QPushButton("Auto-Resize Rows")
        resize_btn.clicked.connect(self.auto_resize_rows)
        toolbar.addWidget(resize_btn)
        
        # Load project button
        load_btn = QPushButton("Load Recent Project")
        load_btn.clicked.connect(self.load_recent_project)
        toolbar.addWidget(load_btn)
        
        toolbar.addStretch()
        
        # Info label
        self.info_label = QLabel("PyQt6 Demo - Click 'Load Recent Project' to see your translation")
        toolbar.addWidget(self.info_label)
        
        # Create table
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        # Configure table
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['#', 'Type', 'Source', 'Target', 'Status'])
        
        # Make columns resizable
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Source
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Target
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Status
        
        # Enable editing
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked | 
                                   QAbstractItemView.EditTrigger.SelectedClicked)
        
        # Alternating row colors
        self.table.setAlternatingRowColors(True)
        
        # Enable word wrap
        self.table.setWordWrap(True)
        
        # Set default font
        self.update_font()
        
        # Status bar
        self.statusBar().showMessage('Ready - Load a project to see the superior Qt grid rendering')
    
    def update_font(self):
        """Update table font"""
        family = self.font_combo.currentText()
        size = int(self.size_combo.currentText())
        
        font = QFont(family, size)
        self.table.setFont(font)
        
        # Auto-resize after font change
        self.auto_resize_rows()
    
    def auto_resize_rows(self):
        """Auto-resize rows to fit content - THE MAGIC OF QT!"""
        self.table.resizeRowsToContents()
        self.statusBar().showMessage('Rows auto-resized to perfectly fit content!')
    
    def load_recent_project(self):
        """Load most recent project from Supervertaler"""
        try:
            print("Looking for recent projects...")
            
            # Try private folder first
            recent_file = Path("user data_private/recent_projects.json")
            if not recent_file.exists():
                recent_file = Path("user data/recent_projects.json")
            
            print(f"Checking: {recent_file.absolute()}")
            
            if not recent_file.exists():
                msg = f"No recent projects found at {recent_file.absolute()}"
                print(msg)
                self.info_label.setText(msg)
                self.statusBar().showMessage(msg)
                return
            
            print(f"Loading recent projects from {recent_file}")
            with open(recent_file, 'r', encoding='utf-8') as f:
                recent = json.load(f)
            
            print(f"Recent projects structure: {type(recent)}")
            print(f"Content: {recent}")
            
            # Handle different formats
            if isinstance(recent, dict):
                # Get all values (should be lists of projects)
                all_projects = []
                for key, value in recent.items():
                    if isinstance(value, list):
                        all_projects.extend(value)
                    else:
                        all_projects.append(value)
                recent_list = all_projects
            elif isinstance(recent, list):
                recent_list = recent
            else:
                recent_list = [recent]
            
            print(f"Found {len(recent_list)} recent projects")
            
            if not recent_list:
                self.info_label.setText("No recent projects")
                self.statusBar().showMessage("No recent projects found")
                return
            
            # Get most recent project (first item)
            latest = recent_list[0]
            print(f"Latest project: {latest}")
            
            # Handle both dict and string path formats
            if isinstance(latest, dict):
                project_path = Path(latest.get('path', latest.get('file', '')))
            else:
                project_path = Path(latest)
            
            print(f"Loading project: {project_path}")
            
            if not project_path.exists():
                msg = f"Project not found: {project_path}"
                print(msg)
                self.info_label.setText(msg)
                self.statusBar().showMessage(msg)
                return
            
            # Load project
            print(f"Reading project file...")
            with open(project_path, 'r', encoding='utf-8') as f:
                project = json.load(f)
            
            segments = project.get('segments', [])
            print(f"Found {len(segments)} segments")
            
            self.load_segments(segments)
            
            msg = f"Loaded: {project_path.name} ({len(segments)} segments)"
            print(msg)
            self.info_label.setText(msg)
            self.statusBar().showMessage(f"Loaded {len(segments)} segments - Notice the perfect spacing!")
            
        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            self.info_label.setText(error_msg)
            self.statusBar().showMessage(error_msg)
    
    def load_segments(self, segments):
        """Load segments into table"""
        self.segments = segments
        self.table.setRowCount(len(segments))
        
        for i, seg in enumerate(segments):
            # ID
            id_item = QTableWidgetItem(str(seg.get('id', i+1)))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
            self.table.setItem(i, 0, id_item)
            
            # Type
            seg_type = seg.get('type', 'para')
            type_item = QTableWidgetItem(seg_type.capitalize() if seg_type else 'Para')
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i, 1, type_item)
            
            # Source (read-only, gray background)
            source_item = QTableWidgetItem(seg.get('source', ''))
            source_item.setFlags(source_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            source_item.setBackground(QColor(245, 245, 245))
            self.table.setItem(i, 2, source_item)
            
            # Target (editable)
            target_item = QTableWidgetItem(seg.get('target', ''))
            self.table.setItem(i, 3, target_item)
            
            # Status
            status = seg.get('status', 'untranslated')
            status_icons = {
                'untranslated': '⚪',
                'draft': '📝',
                'translated': '✅',
                'approved': '⭐'
            }
            status_item = QTableWidgetItem(status_icons.get(status, '⚪'))
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i, 4, status_item)
        
        # Auto-resize to fit content - ONE LINE!
        self.table.resizeRowsToContents()
        
        # Scroll to top
        self.table.scrollToTop()


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show window
    demo = QtGridDemo()
    demo.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
