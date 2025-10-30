#!/usr/bin/env python3
"""
Test the TMMatchPane UI integration
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

# Import the classes
from Supervertaler_Qt import TMMatchPane
from modules.autofingers_engine import TranslationMatch

def test_match_pane_ui():
    """Test the match pane UI rendering"""
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("TM Match Pane Test")
    window.setGeometry(100, 100, 800, 400)
    
    # Create central widget with match pane
    central = QWidget()
    layout = QVBoxLayout(central)
    
    # Add title
    title = QLabel("Testing TMMatchPane Integration")
    title.setStyleSheet("font-size: 14pt; font-weight: bold; padding: 10px;")
    layout.addWidget(title)
    
    # Create and add match pane
    match_pane = TMMatchPane()
    layout.addWidget(match_pane)
    
    window.setCentralWidget(central)
    
    # Test 1: Show "waiting" state
    print("Test 1: Showing waiting state...")
    match_pane.show_no_match()
    window.show()
    app.processEvents()
    
    # Test 2: Display exact match
    print("Test 2: Displaying exact match...")
    exact_match = TranslationMatch(
        translation="Dit is een test",
        match_type="exact",
        match_percent=100
    )
    match_pane.display_match("This is a test", exact_match)
    app.processEvents()
    
    # Test 3: Display fuzzy match
    print("Test 3: Displaying fuzzy match...")
    fuzzy_match = TranslationMatch(
        translation="Dit is een [1}test{2]",
        match_type="fuzzy",
        match_percent=97
    )
    match_pane.display_match("This is a <test>", fuzzy_match)
    app.processEvents()
    
    # Test 4: Clear
    print("Test 4: Clearing match pane...")
    match_pane.clear()
    app.processEvents()
    
    print("✓ All UI tests passed!")
    print("✓ TMMatchPane class instantiated successfully")
    print("✓ All methods callable (display_match, show_no_match, clear)")
    print("✓ Integration with TranslationMatch NamedTuple verified")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(test_match_pane_ui())
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
