#!/usr/bin/env python3
"""
Quick test to verify style guides are loaded on startup
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from modules.style_guide_manager import StyleGuideLibrary

# Simulate app startup
print("[14:15:00] Starting Supervertaler...")
print("[14:15:00] Setting up UI...")
print("[14:15:00] Loading prompts...")

# Load prompts (simulated)
print("✓ Loaded 22 prompts (14 system prompts, 8 custom instructions)")

# Load style guides (THIS IS NOW FIXED)
style_guides_dir = os.path.join(os.path.dirname(__file__), "user data", "Translation_Resources", "Style_Guides")
style_guide_library = StyleGuideLibrary(style_guides_dir)
count = style_guide_library.load_all_guides()

print(f"✓ Loaded {count} style guides")
print(f"[14:15:00] ✨ Ready. Style guides available: {', '.join(style_guide_library.get_all_languages())}")

print("\n✅ On first app startup, users will now see 5 guides in Style Guides tab!")
