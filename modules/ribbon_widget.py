"""
Ribbon Widget - Modern Office-style ribbon interface for Supervertaler Qt

Provides context-sensitive ribbon tabs with grouped tool buttons,
similar to memoQ, Trados Studio, and Microsoft Office applications.

Author: Michael Beijer
License: MIT
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QToolButton, QLabel,
    QFrame, QSizePolicy, QTabWidget, QTabBar, QPushButton
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPainter, QColor


class RibbonButton(QToolButton):
    """A ribbon-style tool button with icon and text"""
    
    def __init__(self, text: str, icon_text: str = "", parent=None):
        super().__init__(parent)
        
        # Store emoji for display
        self.emoji = icon_text
        self.button_text = text
        self.group_color = "#F5F5F5"  # Default
        
        # Set button style
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        # Create display text with emoji
        if icon_text:
            display_text = f"{icon_text} {text}"
        else:
            display_text = text
        
        self.setText(display_text)
        self.setToolTip(text)
        
        # Reduced sizing for more compact ribbon
        self.setMinimumSize(QSize(80, 40))
        self.setMaximumHeight(44)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        # Font for emoji + text
        font = QFont()
        font.setPointSize(9)
        self.setFont(font)
        
        # Make button look modern
        self.setAutoRaise(True)
        self._update_style()
    
    def set_group_color(self, color: str):
        """Set the group color for this button"""
        self.group_color = color
        self._update_style()
    
    def _update_style(self):
        """Update button styling with current group color"""
        # Convert color to RGB for calculations
        color_rgb = self.group_color.lstrip('#')
        r, g, b = tuple(int(color_rgb[i:i+2], 16) for i in (0, 2, 4))
        
        # Create hover color (slightly darker)
        hover_r = min(255, r + 20)
        hover_g = min(255, g + 20)
        hover_b = min(255, b + 20)
        hover_color = f"rgb({hover_r}, {hover_g}, {hover_b})"
        
        # Create pressed color (darker)
        pressed_r = max(0, r - 30)
        pressed_g = max(0, g - 30)
        pressed_b = max(0, b - 30)
        pressed_color = f"rgb({pressed_r}, {pressed_g}, {pressed_b})"
        
        # Border color (darker than background)
        border_r = max(0, r - 40)
        border_g = max(0, g - 40)
        border_b = max(0, b - 40)
        border_color = f"rgb({border_r}, {border_g}, {border_b})"
        
        self.setStyleSheet(f"""
            QToolButton {{
                border: 1px solid {border_color};
                border-radius: 3px;
                padding: 3px 6px;
                background-color: {self.group_color};
            }}
            QToolButton:hover {{
                background-color: {hover_color};
                border: 1px solid {border_color};
            }}
            QToolButton:pressed {{
                background-color: {pressed_color};
                border: 1px solid {border_color};
            }}
        """)


class RibbonGroup(QFrame):
    """A group of related ribbon buttons with a title"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        
        self.title = title
        self.tab_color = "#F5F5F5"  # Default
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        
        # Layout (must be created before styling)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Buttons area
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(3)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.buttons_layout)
        
        # Group title at bottom (hidden by default for cleaner look)
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(7)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: rgba(0, 0, 0, 0.7); margin-top: 2px;")
        self.title_label.hide()  # Hide group titles for cleaner appearance
        layout.addWidget(self.title_label)
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        
        # Initial styling (after layout is set up)
        self._update_style()
    
    def set_tab_color(self, color: str):
        """Set the tab color for this group and update styling"""
        self.tab_color = color
        self._update_style()
    
    def _update_style(self):
        """Update group styling with current tab color"""
        # Use tab color as subtle background, with very subtle or no border
        color_rgb = self.tab_color.lstrip('#')
        r, g, b = tuple(int(color_rgb[i:i+2], 16) for i in (0, 2, 4))
        border_color = f"rgb({max(0, r-30)}, {max(0, g-30)}, {max(0, b-30)})"
        
        self.setStyleSheet(f"""
            RibbonGroup {{
                border: none;
                border-radius: 0px;
                margin: 0px;
                padding: 2px 4px;
                background-color: transparent;
            }}
        """)
    
    def add_button(self, button: RibbonButton):
        """Add a button to this group and apply group color"""
        # Apply tab color to button
        button.set_group_color(self.tab_color)
        self.buttons_layout.addWidget(button)
    
    def add_buttons(self, buttons: list):
        """Add multiple buttons to this group"""
        for button in buttons:
            self.add_button(button)


class RibbonTab(QWidget):
    """A single ribbon tab containing multiple groups"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.tab_color = "#F5F5F5"  # Default light gray
        
        layout = QHBoxLayout(self)
        layout.setSpacing(2)  # Reduced spacing between groups for cleaner look
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.groups = []
    
    def set_tab_color(self, color: str):
        """Set the color theme for this ribbon tab"""
        self.tab_color = color
        self.setStyleSheet(f"background-color: {color};")
        # Update all groups and their buttons with the new color
        self._update_all_groups()
    
    def _update_all_groups(self):
        """Update all groups and buttons with the current tab color"""
        for group in self.groups:
            group.set_tab_color(self.tab_color)
            # Also update all buttons in the group
            for i in range(group.buttons_layout.count()):
                item = group.buttons_layout.itemAt(i)
                if item and item.widget():
                    button = item.widget()
                    if isinstance(button, RibbonButton):
                        button.set_group_color(self.tab_color)
    
    def add_group(self, group: RibbonGroup):
        """Add a group to this ribbon tab"""
        self.groups.append(group)
        # Apply tab color to group (will propagate to buttons)
        group.set_tab_color(self.tab_color)
        self.layout().addWidget(group)
    
    def add_stretch(self):
        """Add stretch to push groups to the left"""
        self.layout().addStretch()


class ColoredTabBar(QTabBar):
    """Custom QTabBar that supports per-tab background colors"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tab_colors = {}  # index -> color
    
    def set_tab_color(self, index: int, color: str):
        """Set the background color for a specific tab"""
        self.tab_colors[index] = color
        self.update()
    
    def paintEvent(self, event):
        """Override paint event to draw custom tab colors"""
        # Draw colored backgrounds first
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for i in range(self.count()):
            tab_rect = self.tabRect(i)
            color_str = self.tab_colors.get(i, "#E0E0E0")
            
            # Convert hex to QColor
            color = QColor(color_str)
            
            # If selected, use full color; otherwise use lighter version
            if i == self.currentIndex():
                painter.fillRect(tab_rect, color)
                # Draw border bottom (thicker line for selected)
                darker = QColor(color)
                darker.setRed(max(0, darker.red() - 50))
                darker.setGreen(max(0, darker.green() - 50))
                darker.setBlue(max(0, darker.blue() - 50))
                pen = painter.pen()
                pen.setColor(darker)
                pen.setWidth(3)
                painter.setPen(pen)
                painter.drawLine(tab_rect.left(), tab_rect.bottom() - 1, tab_rect.right(), tab_rect.bottom() - 1)
            else:
                # Lighter version for unselected tabs
                lighter = QColor(color)
                # Blend with gray (E0E0E0 = 224, 224, 224)
                lighter.setRed(int((lighter.red() + 224) / 2))
                lighter.setGreen(int((lighter.green() + 224) / 2))
                lighter.setBlue(int((lighter.blue() + 224) / 2))
                painter.fillRect(tab_rect, lighter)
        
        # Now draw text on top of colored backgrounds
        painter.setPen(QColor(Qt.GlobalColor.black))
        font = self.font()
        painter.setFont(font)
        
        for i in range(self.count()):
            tab_rect = self.tabRect(i)
            text = self.tabText(i)
            # Center text in tab
            painter.drawText(tab_rect, Qt.AlignmentFlag.AlignCenter, text)
        
        painter.end()
        
        # Don't call super().paintEvent() as it would redraw default backgrounds
        # We've already drawn everything we need


class RibbonWidget(QTabWidget):
    """Main ribbon widget with multiple context-sensitive tabs"""
    
    # Signals for button actions
    action_triggered = pyqtSignal(str)  # Emits action name
    
    # Color scheme for ribbon tabs
    TAB_COLORS = {
        "Home": "#E3F2FD",  # Light blue
        "Translation": "#FFF3E0",  # Light orange
        "View": "#E8F5E9",  # Light green
        "Tools": "#F3E5F5",  # Light purple
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Replace default tab bar with custom colored one
        custom_tab_bar = ColoredTabBar(self)
        self.setTabBar(custom_tab_bar)
        
        # Styling - compact ribbon with colored tabs
        self.setDocumentMode(True)
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMaximumHeight(90)  # Reduced from 120
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Store expanded/collapsed state
        self.is_collapsed = False
        self.expanded_height = 90
        self.collapsed_height = 30  # Just tabs, no content
        
        # Base styling - ribbon area has distinct background
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-top: none;
                background-color: #F5F5F5;
                margin: 0px;
                padding: 4px;
            }
            QTabBar {
                background-color: #E0E0E0;
                margin: 0px;
                padding: 0px;
            }
            QTabBar::tab {
                padding: 6px 12px;
                margin: 0px 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: none;
                background-color: transparent;
            }
            QTabBar::tab:selected {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Store tabs by name for easy access
        self.ribbon_tabs = {}
        
        # Connect to tab change to update colors
        self.currentChanged.connect(self._on_tab_changed)
        
        # Connect to tab click - if collapsed, temporarily expand
        tab_bar = self.tabBar()
        if tab_bar:
            try:
                tab_bar.tabBarClicked.connect(self._on_tab_clicked)
            except AttributeError:
                # Fallback if signal doesn't exist
                pass
        
        # Create collapse/expand button
        self.create_collapse_button()
        
    def add_ribbon_tab(self, name: str, tab: RibbonTab):
        """Add a ribbon tab with color coding"""
        self.ribbon_tabs[name] = tab
        
        # Apply color to the tab
        tab_color = self.TAB_COLORS.get(name, "#F5F5F5")
        tab.set_tab_color(tab_color)
        
        # Add tab
        index = self.addTab(tab, name)
        
        # Set color on custom tab bar
        tab_bar = self.tabBar()
        if isinstance(tab_bar, ColoredTabBar):
            tab_bar.set_tab_color(index, tab_color)
    
    def apply_initial_colors(self):
        """Apply colors to all tabs after they're all added"""
        # Trigger the tab change handler to apply colors to the first tab
        if self.count() > 0:
            self._on_tab_changed(0)
    
    def _on_tab_changed(self, index: int):
        """Update pane color when tab changes"""
        if index < 0 or index >= self.count():
            return
        
        # If ribbon is collapsed and user clicked a tab, expand it
        if self.is_collapsed:
            self.is_collapsed = False
            self.setMaximumHeight(self.expanded_height)
            self.setMinimumHeight(0)
            self.collapse_button.setText("▼ Hide")
            self.collapse_button.setToolTip("Hide Ribbon (Ctrl+F1)")
            
        tab_name = self.tabText(index)
        tab_color = self.TAB_COLORS.get(tab_name, "#F5F5F5")
        
        # Get the active tab widget
        active_tab = self.widget(index)
        if isinstance(active_tab, RibbonTab):
            # Ensure all buttons in the active tab have the correct color
            active_tab._update_all_groups()
            # Show the tab content
            active_tab.setVisible(True)
        
        # Update custom tab bar (it will repaint automatically)
        tab_bar = self.tabBar()
        if isinstance(tab_bar, ColoredTabBar):
            tab_bar.update()
        
        # Update pane background to match selected tab
        self.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #CCCCCC;
                border-top: none;
                background-color: {tab_color};
                margin: 0px;
                padding: 4px;
            }}
        """)
        
        # Force update to ensure visibility
        self.update()
        if active_tab:
            active_tab.update()
    
    def _darker_color(self, color: str) -> str:
        """Make a color darker for borders"""
        color_rgb = color.lstrip('#')
        r, g, b = tuple(int(color_rgb[i:i+2], 16) for i in (0, 2, 4))
        return f"rgb({max(0, r-50)}, {max(0, g-50)}, {max(0, b-50)})"
    
    def _lighter_color(self, color: str) -> str:
        """Make a color lighter for unselected tabs"""
        color_rgb = color.lstrip('#')
        r, g, b = tuple(int(color_rgb[i:i+2], 16) for i in (0, 2, 4))
        # Blend with gray background (E0E0E0 = 224, 224, 224)
        r = int((r + 224) / 2)
        g = int((g + 224) / 2)
        b = int((b + 224) / 2)
        return f"rgb({r}, {g}, {b})"
    
    def get_tab(self, name: str) -> RibbonTab:
        """Get a ribbon tab by name"""
        return self.ribbon_tabs.get(name)
    
    def create_collapse_button(self):
        """Create a collapse/expand button - more visible and better positioned"""
        # Create button widget - larger and more visible
        self.collapse_button = QPushButton("▼ Hide")
        self.collapse_button.setToolTip("Hide/Show Ribbon (Ctrl+F1)")
        self.collapse_button.setFixedSize(60, 26)  # Larger size with text
        self.collapse_button.setStyleSheet("""
            QPushButton {
                border: 1px solid #999;
                background-color: #E8E8E8;
                font-size: 11px;
                font-weight: normal;
                color: #333;
                border-radius: 3px;
                padding: 2px 4px;
            }
            QPushButton:hover {
                background-color: #D8D8D8;
                border: 1px solid #777;
            }
            QPushButton:pressed {
                background-color: #C8C8C8;
                border: 1px solid #555;
            }
        """)
        self.collapse_button.clicked.connect(self.toggle_collapse)
        
        # Position it as corner widget but it will be more visible now
        self.setCornerWidget(self.collapse_button, Qt.Corner.TopRightCorner)
    
    def toggle_collapse(self):
        """Toggle ribbon between expanded and collapsed states"""
        self.is_collapsed = not self.is_collapsed
        
        if self.is_collapsed:
            # Collapse: hide content pane, show only tabs
            self.setMaximumHeight(self.collapsed_height)
            self.setMinimumHeight(self.collapsed_height)
            # Hide the content area (pane)
            for i in range(self.count()):
                widget = self.widget(i)
                if widget:
                    widget.setVisible(False)
            self.collapse_button.setText("▲ Show")
            self.collapse_button.setToolTip("Show Ribbon (Ctrl+F1)")
        else:
            # Expand: show full ribbon with content
            self.setMaximumHeight(self.expanded_height)
            self.setMinimumHeight(0)
            # Show the content area for the current tab
            current_index = self.currentIndex()
            if current_index >= 0:
                widget = self.widget(current_index)
                if widget:
                    widget.setVisible(True)
            self.collapse_button.setText("▼ Hide")
            self.collapse_button.setToolTip("Hide Ribbon (Ctrl+F1)")
    
    def _on_tab_clicked(self, index: int):
        """Handle tab click - if collapsed, temporarily expand"""
        if self.is_collapsed:
            # Temporarily expand to show the selected tab's content
            self.is_collapsed = False  # Update state
            self.setMaximumHeight(self.expanded_height)
            self.setMinimumHeight(0)
            
            # Show the clicked tab's content
            widget = self.widget(index)
            if widget:
                widget.setVisible(True)
            
            # Update button text
            self.collapse_button.setText("▼ Hide")
            self.collapse_button.setToolTip("Hide Ribbon (Ctrl+F1)")
            
            # Update colors for the newly selected tab
            if index >= 0 and index < self.count():
                self._on_tab_changed(index)
    
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
