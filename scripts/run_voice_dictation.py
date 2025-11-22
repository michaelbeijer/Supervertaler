"""
Standalone launcher for Voice Dictation module
Run this to test the voice dictation system
"""

import sys
from PyQt6.QtWidgets import QApplication
from modules.voice_dictation import VoiceDictationWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show window
    window = VoiceDictationWidget()
    window.setWindowTitle("Voice Dictation - Supervertaler")
    window.resize(650, 750)
    window.show()

    sys.exit(app.exec())
