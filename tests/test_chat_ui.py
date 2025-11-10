"""
Test the new chat interface rendering
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from modules.unified_prompt_manager_qt import UnifiedPromptManagerQt


class MockApp:
    """Mock parent app for testing"""
    def __init__(self):
        self.user_data_path = Path("user_data_private")

    def log(self, message):
        # Handle Unicode in Windows console
        try:
            print(f"[LOG] {message}")
        except UnicodeEncodeError:
            print(f"[LOG] {message.encode('ascii', errors='replace').decode('ascii')}")


class TestWindow(QMainWindow):
    """Test window to display the AI Assistant tab"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat UI Test - Supervertaler AI Assistant")
        self.setGeometry(100, 100, 900, 700)

        # Create mock app
        self.mock_app = MockApp()

        # Create unified prompt manager
        self.prompt_manager = UnifiedPromptManagerQt(self.mock_app, standalone=True)

        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Create the AI Assistant tab directly
        assistant_tab = self.prompt_manager._create_ai_assistant_tab()
        layout.addWidget(assistant_tab)

        # Add test buttons
        test_buttons = QWidget()
        test_layout = QHBoxLayout(test_buttons)

        btn_user = QPushButton("Add User Message")
        btn_user.clicked.connect(self.add_user_message)
        test_layout.addWidget(btn_user)

        btn_ai = QPushButton("Add AI Message")
        btn_ai.clicked.connect(self.add_ai_message)
        test_layout.addWidget(btn_ai)

        btn_system = QPushButton("Add System Message")
        btn_system.clicked.connect(self.add_system_message)
        test_layout.addWidget(btn_system)

        btn_long = QPushButton("Add Long Message")
        btn_long.clicked.connect(self.add_long_message)
        test_layout.addWidget(btn_long)

        layout.addWidget(test_buttons)

        # Add initial test messages
        self.add_initial_messages()

    def add_initial_messages(self):
        """Add initial test messages"""
        self.prompt_manager._add_chat_message(
            "system",
            "✨ Chat interface initialized! Testing new rendering system."
        )

        self.prompt_manager._add_chat_message(
            "user",
            "Hello! Can you help me analyze my translation project?"
        )

        self.prompt_manager._add_chat_message(
            "assistant",
            "Of course! I'd be happy to help you analyze your translation project. I can:\n\n"
            "• Analyze your **source documents**\n"
            "• Generate *custom prompts* based on domain and style\n"
            "• Review translation memories and `termbases`\n"
            "• Suggest improvements to your **workflow**\n\n"
            "What would you like to start with?"
        )

    def add_user_message(self):
        """Add a test user message"""
        self.prompt_manager._add_chat_message(
            "user",
            "This is a test user message. Let me see how it renders with the new chat bubble design!"
        )

    def add_ai_message(self):
        """Add a test AI message"""
        self.prompt_manager._add_chat_message(
            "assistant",
            "This is a test AI response. The new rendering system uses QListWidget with a custom delegate instead of QTextEdit with HTML/CSS. This gives us full control over the visual appearance!"
        )

    def add_system_message(self):
        """Add a test system message"""
        self.prompt_manager._add_chat_message(
            "system",
            "📎 File attached: example_document.pdf (converted to markdown: 5,432 chars)"
        )

    def add_long_message(self):
        """Add a long message to test wrapping"""
        long_text = (
            "This is a very long message to test text wrapping in the chat bubbles. "
            "The delegate should properly calculate the height needed for multi-line text "
            "and wrap it nicely within the bubble constraints. The maximum bubble width is "
            "set to 70% of the available width, which should look good on various screen sizes. "
            "Let's add even more text to really test the wrapping behavior. "
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
            "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
            "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        )
        self.prompt_manager._add_chat_message("assistant", long_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
