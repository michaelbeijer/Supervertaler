"""
Settings Sidebar Widget - Vertical tab navigation for Settings panel

Replaces the horizontal QTabWidget with a QListWidget sidebar + QStackedWidget.
Exposes the same API as QTabWidget (setCurrentIndex, currentIndex, count, tabText)
so existing navigation code works unchanged.

Author: Michael Beijer
License: MIT
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QListWidget, QListWidgetItem,
    QStackedWidget, QSplitter, QAbstractItemView
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont


class SettingsSidebar(QWidget):
    """
    Vertical sidebar navigation that mimics QTabWidget API.

    Uses QListWidget (left) + QStackedWidget (right) in a QSplitter.
    Drop-in replacement: callers use setCurrentIndex(), tabText(), count()
    exactly as they did with QTabWidget.
    """

    # Emitted when the current page changes (same signature as QTabWidget.currentChanged)
    currentChanged = pyqtSignal(int)

    # Sidebar width constraints
    SIDEBAR_MIN_WIDTH = 170
    SIDEBAR_MAX_WIDTH = 220

    def __init__(self, parent=None):
        super().__init__(parent)

        self._tab_names = []  # Ordered list of tab labels (for tabText())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Splitter: sidebar | content ---
        self._splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self._splitter.setChildrenCollapsible(False)

        # --- Left: sidebar list ---
        self._list = QListWidget()
        self._list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._list.setMinimumWidth(self.SIDEBAR_MIN_WIDTH)
        self._list.setMaximumWidth(self.SIDEBAR_MAX_WIDTH)
        self._list.setIconSize(QSize(0, 0))  # We use emoji in text, no QIcon

        # --- Right: stacked content pages ---
        self._stack = QStackedWidget()

        # Assemble splitter
        self._splitter.addWidget(self._list)
        self._splitter.addWidget(self._stack)
        self._splitter.setStretchFactor(0, 0)  # Sidebar: fixed
        self._splitter.setStretchFactor(1, 1)  # Content: stretches

        layout.addWidget(self._splitter)

        # Wire selection → page switch
        self._list.currentRowChanged.connect(self._on_row_changed)

        # Apply default styling
        self._apply_style()

    # ------------------------------------------------------------------ #
    #  QTabWidget-compatible API                                          #
    # ------------------------------------------------------------------ #

    def addTab(self, widget: QWidget, label: str) -> int:
        """Add a page with the given label. Returns the new page index."""
        index = self._stack.count()

        # Add widget to stack
        self._stack.addWidget(widget)

        # Add item to sidebar list
        item = QListWidgetItem(label)
        item.setSizeHint(QSize(0, 38))  # Fixed row height for consistent look
        self._list.addItem(item)

        # Track the label
        self._tab_names.append(label)

        # Auto-select the first item
        if index == 0:
            self._list.setCurrentRow(0)

        return index

    def setCurrentIndex(self, index: int):
        """Switch to the page at the given index."""
        if 0 <= index < self._list.count():
            self._list.setCurrentRow(index)

    def currentIndex(self) -> int:
        """Return the index of the currently selected page."""
        return self._list.currentRow()

    def count(self) -> int:
        """Return the number of pages."""
        return self._stack.count()

    def tabText(self, index: int) -> str:
        """Return the label text for the page at the given index."""
        if 0 <= index < len(self._tab_names):
            return self._tab_names[index]
        return ""

    def widget(self, index: int) -> QWidget:
        """Return the widget at the given index."""
        return self._stack.widget(index)

    # ------------------------------------------------------------------ #
    #  Convenience: tabBar() stub for code that calls tabBar().setFont()  #
    # ------------------------------------------------------------------ #

    def tabBar(self):
        """Return the sidebar list (duck-typing for tabBar().setStyleSheet() calls)."""
        return self._list

    def set_font_size(self, pt_size: int):
        """Set the sidebar list font size (for global UI font scaling)."""
        font = self._list.font()
        font.setPointSize(pt_size)
        self._list.setFont(font)
        # Adjust row height proportionally
        row_height = max(32, int(pt_size * 3.8))
        for i in range(self._list.count()):
            self._list.item(i).setSizeHint(QSize(0, row_height))

    # ------------------------------------------------------------------ #
    #  Internal                                                           #
    # ------------------------------------------------------------------ #

    def _on_row_changed(self, row: int):
        """Handle sidebar selection change."""
        if 0 <= row < self._stack.count():
            self._stack.setCurrentIndex(row)
            self.currentChanged.emit(row)

    def _apply_style(self):
        """Apply the sidebar styling."""
        self._list.setStyleSheet("""
            QListWidget {
                border: none;
                border-right: 1px solid #D0D0D0;
                background-color: transparent;
                outline: none;
                padding: 6px 0px;
            }
            QListWidget::item {
                padding: 7px 14px;
                border-radius: 0px;
                border: none;
                margin: 1px 4px;
                border-radius: 6px;
            }
            QListWidget::item:selected {
                background-color: rgba(33, 150, 243, 0.12);
                color: #1976D2;
                font-weight: bold;
            }
            QListWidget::item:hover:!selected {
                background-color: rgba(0, 0, 0, 0.04);
            }
        """)

        self._stack.setStyleSheet("""
            QStackedWidget {
                border: none;
            }
        """)

    def apply_dark_style(self):
        """Switch to dark-mode sidebar styling."""
        self._list.setStyleSheet("""
            QListWidget {
                border: none;
                border-right: 1px solid #404040;
                background-color: transparent;
                outline: none;
                padding: 6px 0px;
            }
            QListWidget::item {
                padding: 7px 14px;
                border: none;
                margin: 1px 4px;
                border-radius: 6px;
            }
            QListWidget::item:selected {
                background-color: rgba(33, 150, 243, 0.20);
                color: #64B5F6;
                font-weight: bold;
            }
            QListWidget::item:hover:!selected {
                background-color: rgba(255, 255, 255, 0.06);
            }
        """)
