"""
Ribbon Widget - Modern Office-style ribbon interface for Supervertaler Qt

Provides context-sensitive ribbon tabs with grouped tool buttons,
similar to memoQ, Trados Studio, and Microsoft Office applications.

Author: Michael Beijer
License: MIT
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QToolButton, QLabel,
    QFrame, QSizePolicy, QTabWidget
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont


class RibbonButton(QToolButton):
    """A ribbon-style tool button with icon and text"""
    
    def __init__(self, text: str, icon_text: str = "", parent=None):
        super().__init__(parent)
        
        # Store emoji for display
        self.emoji = icon_text
        self.button_text = text
        
        # Set button style
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        # Create display text with emoji
        if icon_text:
            display_text = f"{icon_text} {text}"
        else:
            display_text = text
        
        self.setText(display_text)
        self.setToolTip(text)
        
        # Styling
        self.setMinimumSize(QSize(90, 50))
        self.setMaximumHeight(55)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        # Font for emoji + text
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        
        # Make button look modern
        self.setAutoRaise(True)
        self.setStyleSheet("""
            QToolButton {
                border: 1px solid transparent;
                border-radius: 3px;
                padding: 4px 8px;
                background: transparent;
            }
            QToolButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            QToolButton:pressed {
                background: rgba(0, 0, 0, 0.1);
            }
        """)


class RibbonGroup(QFrame):
    """A group of related ribbon buttons with a title"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        
        self.title = title
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        
        # Styling
        self.setStyleSheet("""
            RibbonGroup {
                border: 1px solid rgba(200, 200, 200, 0.3);
                border-radius: 4px;
                margin: 2px;
                padding: 4px;
            }
        """)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setSpacing(3)
        layout.setContentsMargins(6, 6, 6, 4)
        
        # Buttons area
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(3)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.buttons_layout)
        
        # Group title at bottom
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(7)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); margin-top: 2px;")
        layout.addWidget(title_label)
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    
    def add_button(self, button: RibbonButton):
        """Add a button to this group"""
        self.buttons_layout.addWidget(button)
    
    def add_buttons(self, buttons: list):
        """Add multiple buttons to this group"""
        for button in buttons:
            self.add_button(button)


class RibbonTab(QWidget):
    """A single ribbon tab containing multiple groups"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.groups = []
    
    def add_group(self, group: RibbonGroup):
        """Add a group to this ribbon tab"""
        self.groups.append(group)
        self.layout().addWidget(group)
    
    def add_stretch(self):
        """Add stretch to push groups to the left"""
        self.layout().addStretch()


class RibbonWidget(QTabWidget):
    """Main ribbon widget with multiple context-sensitive tabs"""
    
    # Signals for button actions
    action_triggered = pyqtSignal(str)  # Emits action name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Styling
        self.setDocumentMode(True)
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMaximumHeight(120)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Store tabs by name for easy access
        self.ribbon_tabs = {}
        
    def add_ribbon_tab(self, name: str, tab: RibbonTab):
        """Add a ribbon tab"""
        self.ribbon_tabs[name] = tab
        self.addTab(tab, name)
    
    def get_tab(self, name: str) -> RibbonTab:
        """Get a ribbon tab by name"""
        return self.ribbon_tabs.get(name)
    
    def create_button(self, text: str, emoji: str, action_name: str, tooltip: str = "") -> RibbonButton:
        """Helper to create a ribbon button with action connection"""
        # Create button with emoji as large icon text
        btn = RibbonButton(text, emoji)
        
        if tooltip:
            btn.setToolTip(tooltip)
        else:
            btn.setToolTip(text)
        
        # Connect to action signal
        btn.clicked.connect(lambda: self.action_triggered.emit(action_name))
        
        return btn


class RibbonBuilder:
    """Helper class to build ribbon interfaces declaratively"""
    
    @staticmethod
    def build_home_ribbon() -> RibbonTab:
        """Build the Home ribbon tab"""
        tab = RibbonTab()
        
        # File group
        file_group = RibbonGroup("File")
        tab.add_group(file_group)
        
        # Edit group
        edit_group = RibbonGroup("Edit")
        tab.add_group(edit_group)
        
        # View group
        view_group = RibbonGroup("View")
        tab.add_group(view_group)
        
        tab.add_stretch()
        return tab
    
    @staticmethod
    def build_translation_ribbon() -> RibbonTab:
        """Build the Translation ribbon tab"""
        tab = RibbonTab()
        
        # Translate group
        translate_group = RibbonGroup("Translate")
        tab.add_group(translate_group)
        
        # Memory group
        memory_group = RibbonGroup("Translation Memory")
        tab.add_group(memory_group)
        
        tab.add_stretch()
        return tab
    
    @staticmethod
    def build_tools_ribbon() -> RibbonTab:
        """Build the Tools ribbon tab"""
        tab = RibbonTab()
        
        # Automation group
        automation_group = RibbonGroup("Automation")
        tab.add_group(automation_group)
        
        # Settings group
        settings_group = RibbonGroup("Settings")
        tab.add_group(settings_group)
        
        tab.add_stretch()
        return tab
