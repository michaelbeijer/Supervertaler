"""
Quick Access Sidebar - memoQ-style left navigation panel

Provides quick access to common actions, recent files, and project navigation.

Author: Michael Beijer
License: MIT
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFrame,
    QScrollArea, QSizePolicy, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont


class QuickActionButton(QPushButton):
    """A button for quick actions in the sidebar"""
    
    def __init__(self, icon: str, text: str, parent=None):
        super().__init__(parent)
        
        self.setText(f"{icon}  {text}")
        self.setMinimumHeight(36)
        self.setMaximumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Styling
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 8px 12px;
                border: none;
                border-radius: 4px;
                background: transparent;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background: rgba(0, 0, 0, 0.1);
            }
        """)


class SidebarSection(QFrame):
    """A collapsible section in the sidebar"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        
        self.title = title
        self.is_collapsed = False
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 4, 8, 8)
        
        # Section header (clickable to collapse/expand)
        self.header = QPushButton(f"▼ {title}")
        self.header.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 6px 8px;
                border: none;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 3px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        self.header.setCursor(Qt.CursorShape.PointingHandCursor)
        self.header.clicked.connect(self.toggle_collapsed)
        layout.addWidget(self.header)
        
        # Content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(2)
        self.content_layout.setContentsMargins(4, 4, 4, 4)
        layout.addWidget(self.content_widget)
        
        # Styling
        self.setStyleSheet("""
            SidebarSection {
                background: transparent;
                border: 1px solid rgba(200, 200, 200, 0.2);
                border-radius: 4px;
                margin: 2px;
            }
        """)
    
    def add_button(self, button: QuickActionButton):
        """Add a quick action button to this section"""
        self.content_layout.addWidget(button)
    
    def toggle_collapsed(self):
        """Toggle section collapsed state"""
        self.is_collapsed = not self.is_collapsed
        self.content_widget.setVisible(not self.is_collapsed)
        arrow = "▶" if self.is_collapsed else "▼"
        self.header.setText(f"{arrow} {self.title}")


class QuickAccessSidebar(QWidget):
    """Left sidebar with quick access to common functions"""
    
    # Signals
    action_triggered = pyqtSignal(str)  # Emits action name
    file_selected = pyqtSignal(str)  # Emits file path
    project_home_clicked = pyqtSignal()  # Emits when Project Home button clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setMinimumWidth(200)
        self.setMaximumWidth(250)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # Title
        title = QLabel("Quick Access")
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Scroll area for sections
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        self.sections_layout = QVBoxLayout(scroll_content)
        self.sections_layout.setSpacing(6)
        self.sections_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Styling
        self.setStyleSheet("""
            QuickAccessSidebar {
                background: rgba(0, 0, 0, 0.1);
                border-right: 1px solid rgba(200, 200, 200, 0.3);
            }
        """)
        
        # Build default sections
        self.build_default_sections()
    
    def build_default_sections(self):
        """Build default sidebar sections"""
        # Project Home button (top, always visible)
        project_home_btn = QuickActionButton("🏠", "Project Home")
        project_home_btn.clicked.connect(self.project_home_clicked.emit)
        project_home_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 8px 12px;
                border: none;
                border-radius: 4px;
                background: rgba(59, 130, 246, 0.15);
                font-size: 11pt;
                font-weight: bold;
                border-left: 3px solid #3B82F6;
            }
            QPushButton:hover {
                background: rgba(59, 130, 246, 0.25);
            }
            QPushButton:pressed {
                background: rgba(59, 130, 246, 0.35);
            }
        """)
        
        # Get the main layout and add Project Home button at top
        main_layout = self.layout()
        # Find where to insert (after title)
        main_layout.insertWidget(1, project_home_btn)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.insertWidget(2, separator)
        
        # Quick Actions section
        quick_actions = SidebarSection("Quick Actions")
        
        new_btn = QuickActionButton("📄", "New Project")
        new_btn.clicked.connect(lambda: self.action_triggered.emit("new"))
        quick_actions.add_button(new_btn)
        
        open_btn = QuickActionButton("📂", "Open Project")
        open_btn.clicked.connect(lambda: self.action_triggered.emit("open"))
        quick_actions.add_button(open_btn)
        
        save_btn = QuickActionButton("💾", "Save Project")
        save_btn.clicked.connect(lambda: self.action_triggered.emit("save"))
        quick_actions.add_button(save_btn)
        
        self.add_section(quick_actions)
        
        # Translation Tools section
        tools_section = SidebarSection("Translation Tools")
        
        lookup_btn = QuickActionButton("🔍", "Universal Lookup")
        lookup_btn.clicked.connect(lambda: self.action_triggered.emit("universal_lookup"))
        tools_section.add_button(lookup_btn)
        
        autofingers_btn = QuickActionButton("✋", "AutoFingers")
        autofingers_btn.clicked.connect(lambda: self.action_triggered.emit("autofingers"))
        tools_section.add_button(autofingers_btn)
        
        tm_btn = QuickActionButton("🗂️", "TM Manager")
        tm_btn.clicked.connect(lambda: self.action_triggered.emit("tm_manager"))
        tools_section.add_button(tm_btn)
        
        self.add_section(tools_section)
        
        # Recent Files section
        self.recent_section = SidebarSection("Recent Files")
        self.recent_list = QListWidget()
        self.recent_list.setMaximumHeight(150)
        self.recent_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                font-size: 9pt;
            }
            QListWidget::item {
                padding: 4px;
                border-radius: 2px;
            }
            QListWidget::item:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QListWidget::item:selected {
                background: rgba(100, 150, 255, 0.3);
            }
        """)
        self.recent_list.itemDoubleClicked.connect(self.on_recent_file_clicked)
        self.recent_section.content_layout.addWidget(self.recent_list)
        self.add_section(self.recent_section)
        
        # Add stretch at bottom
        self.sections_layout.addStretch()
    
    def add_section(self, section: SidebarSection):
        """Add a section to the sidebar"""
        self.sections_layout.addWidget(section)
    
    def update_recent_files(self, file_paths: list):
        """Update recent files list"""
        self.recent_list.clear()
        for path in file_paths:
            # Show only filename, store full path
            import os
            filename = os.path.basename(path)
            item = QListWidgetItem(filename)
            item.setData(Qt.ItemDataRole.UserRole, path)
            item.setToolTip(path)
            self.recent_list.addItem(item)
    
    def on_recent_file_clicked(self, item: QListWidgetItem):
        """Handle recent file double-click"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        if file_path:
            self.file_selected.emit(file_path)
