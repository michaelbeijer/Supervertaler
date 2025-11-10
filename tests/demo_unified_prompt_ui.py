"""
Standalone Demo: Unified Prompt Library UI

Run this to see the new prompt library interface in action.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import Qt

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.unified_prompt_manager_qt import UnifiedPromptManagerQt


class DemoApp(QMainWindow):
    """Demo application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unified Prompt Library - Demo")
        self.setGeometry(100, 100, 1200, 800)
        
        # Mock parent app interface
        self.user_data_path = "user_data"
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create prompt manager
        self.prompt_manager = UnifiedPromptManagerQt(self, standalone=True)
        
        # Create the prompt library tab
        prompt_tab = self.prompt_manager.create_tab(self.tabs)
        self.tabs.addTab(prompt_tab, "📚 Prompt Library")
    
    def log(self, message):
        """Log callback for prompt manager"""
        print(f"[LOG] {message}")


def main():
    """Run the demo application"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = DemoApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
