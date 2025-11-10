"""
Test script for TMX Editor module

This script demonstrates the standalone TMX Editor.
Run with: python test_tmx_editor.py
"""

import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from modules.tmx_editor import TmxEditorUI

if __name__ == '__main__':
    print("=" * 60)
    print("TMX Editor - Standalone Test")
    print("Inspired by Heartsome TMX Editor 8")
    print("=" * 60)
    print("\nStarting TMX Editor...")
    print("Features:")
    print("  • Create/Open/Save TMX files")
    print("  • Dual-language grid editor")
    print("  • Fast filtering and pagination")
    print("  • TMX validation and header editing")
    print("  • Multi-language support")
    print("\n" + "=" * 60 + "\n")
    
    app = TmxEditorUI(standalone=True)
    app.run()
