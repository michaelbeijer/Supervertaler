#!/usr/bin/env python3
"""
Multi-Chat Viewer - Display multiple AI chat pages side by side
Displays ChatGPT, Claude, and Gemini chats in a three-column layout
"""

import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QLabel, QSplitter
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QPalette, QColor


class ChatColumn(QWidget):
    """A column containing a chat interface"""

    def __init__(self, title, url, header_color):
        super().__init__()
        self.title = title
        self.url = url
        self.header_color = header_color
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header label
        header = QLabel(self.title)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"""
            QLabel {{
                background-color: {self.header_color};
                color: white;
                padding: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
        """)

        # Web view
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl(self.url))

        # Add to layout
        layout.addWidget(header)
        layout.addWidget(self.web_view)

        self.setLayout(layout)


class MultiChatViewer(QMainWindow):
    """Main window for the Multi-Chat Viewer"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Multi-Chat Viewer - ChatGPT | Claude | Gemini")
        self.setGeometry(100, 100, 1800, 1000)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title bar
        title_bar = QLabel("Multi-Chat Viewer - ChatGPT | Claude | Gemini")
        title_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_bar.setStyleSheet("""
            QLabel {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(title_bar)

        # Splitter for resizable columns
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Chat URLs
        chatgpt_url = "https://chatgpt.com/g/g-p-691b3c7d19b4819183e9a27cd0700bc7-brants-stein-002-be-ep/c/691c9614-b258-832c-8201-88e911ae26f9"
        claude_url = "https://claude.ai/chat/7e0f1651-33a5-43c0-bca6-be6f4977736b"
        gemini_url = "https://gemini.google.com/gem/839507734ccd/3ebe6cf9e3dafd58"

        # Create columns
        chatgpt_column = ChatColumn("ChatGPT", chatgpt_url, "#10a37f")
        claude_column = ChatColumn("Claude", claude_url, "#c17c4f")
        gemini_column = ChatColumn("Gemini", gemini_url, "#4285f4")

        # Add columns to splitter
        splitter.addWidget(chatgpt_column)
        splitter.addWidget(claude_column)
        splitter.addWidget(gemini_column)

        # Set equal sizes for all columns
        splitter.setSizes([600, 600, 600])

        # Add splitter to main layout
        main_layout.addWidget(splitter)

        central_widget.setLayout(main_layout)

        # Set dark theme
        self.set_dark_theme()

    def set_dark_theme(self):
        """Apply a dark theme to the application"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        self.setPalette(palette)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Multi-Chat Viewer")

    viewer = MultiChatViewer()
    viewer.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
