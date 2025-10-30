"""
Project Home Panel - Collapsible sidebar like memoQ's Project Home
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QListWidget, QListWidgetItem, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QColor, QFont, QIcon


class ProjectHomeItem(QWidget):
    """Individual item in the Project Home panel"""
    
    clicked = pyqtSignal(str)
    
    def __init__(self, icon: str, text: str, item_id: str, parent=None):
        super().__init__(parent)
        self.item_id = item_id
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)
        
        # Icon/emoji
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 18px; background: transparent;")
        icon_label.setMaximumWidth(30)
        layout.addWidget(icon_label)
        
        # Text
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background: transparent;
                font-size: 11px;
                font-weight: 500;
            }
        """)
        layout.addWidget(text_label, stretch=1)
        
        # Make the whole widget clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            ProjectHomeItem {
                background: transparent;
                border-radius: 4px;
            }
            ProjectHomeItem:hover {
                background: rgba(0, 0, 0, 0.05);
            }
        """)
    
    def mousePressEvent(self, event):
        """Emit signal when clicked"""
        self.clicked.emit(self.item_id)


class ProjectHomePanel(QWidget):
    """Collapsible Project Home panel similar to memoQ"""
    
    # Signals
    item_selected = pyqtSignal(str)  # Emits item ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_expanded = False
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header with tab
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: #f0f0f0;
                border-right: 1px solid #cccccc;
            }
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        # Tab button (left edge)
        tab_btn = QPushButton("PROJECT\nHOME")
        tab_btn.setMaximumWidth(60)
        tab_btn.setMinimumHeight(80)
        tab_btn.setStyleSheet("""
            QPushButton {
                background: #e8e8e8;
                border: 1px solid #cccccc;
                border-right: none;
                color: #333333;
                font-size: 9px;
                font-weight: bold;
                padding: 8px 4px;
            }
            QPushButton:hover {
                background: #f5f5f5;
            }
            QPushButton:pressed {
                background: #e0e0e0;
            }
        """)
        tab_btn.clicked.connect(self.toggle_panel)
        header_layout.addWidget(tab_btn)
        header_layout.addStretch()
        
        main_layout.addWidget(header)
        
        # Panel content (initially hidden)
        content = QFrame()
        content.setMaximumWidth(0)  # Start collapsed
        content.setStyleSheet("""
            QFrame {
                background: white;
                border-right: 1px solid #cccccc;
            }
        """)
        self.content = content
        
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Scroll area for items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background: white;
                border: none;
            }
            QScrollBar:vertical {
                background: white;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #cccccc;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #999999;
            }
        """)
        
        # Container for items
        items_container = QWidget()
        items_layout = QVBoxLayout(items_container)
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(1)
        
        # Add menu items
        menu_items = [
            ("📋", "Overview", "overview"),
            ("📁", "Translations", "translations"),
            ("📚", "Live Docs", "live_docs"),
            ("🔄", "Translation Memories", "memories"),
            ("🏷️", "Termbases", "termbases"),
            ("🤖", "Muses", "muses"),
            ("⚙️", "Settings", "settings"),
        ]
        
        self.items_map = {}
        for icon, text, item_id in menu_items:
            item = ProjectHomeItem(icon, text, item_id)
            item.clicked.connect(self.on_item_clicked)
            self.items_map[item_id] = item
            items_layout.addWidget(item)
        
        items_layout.addStretch()
        scroll.setWidget(items_container)
        content_layout.addWidget(scroll)
        
        main_layout.addWidget(content)
        
        # Animation for expand/collapse
        self.animation = QPropertyAnimation(self.content, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    
    def toggle_panel(self):
        """Toggle panel expanded/collapsed"""
        self.is_expanded = not self.is_expanded
        
        if self.is_expanded:
            # Expand
            self.animation.setEndValue(250)  # Width when expanded
        else:
            # Collapse
            self.animation.setEndValue(0)  # Width when collapsed
        
        self.animation.start()
    
    def on_item_clicked(self, item_id: str):
        """Handle item click"""
        self.item_selected.emit(item_id)
    
    def setMaximumWidth(self, width: int):
        """Override to allow animation"""
        super().setMaximumWidth(width)
        self.content.setMaximumWidth(width - 60)  # Account for tab width
