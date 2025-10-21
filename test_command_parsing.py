#!/usr/bin/env python3
"""
Test script for command parsing in Style Guides AI chat handler.
Simulates user messages to verify parsing logic.
"""

import os
import sys
import tempfile
import shutil

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.style_guide_manager import StyleGuideLibrary

def simulate_parse_command(library, message):
    """Simulate the _parse_style_guide_command method"""
    msg_lower = message.lower()
    
    # Command: "add to all: text"
    if msg_lower.startswith("add to all:"):
        text_to_add = message[11:].strip()  # Remove "add to all:"
        if not text_to_add:
            return {'executed': False, 'response': "Please provide text after 'add to all:'"}
        
        try:
            library.append_to_all_guides(text_to_add)
            languages = ", ".join(library.get_all_languages())
            response = f"✅ Added to all 5 languages:\n{languages}\n\nText: {text_to_add[:50]}{'...' if len(text_to_add) > 50 else ''}"
            return {'executed': True, 'response': response}
        except Exception as e:
            return {'executed': False, 'response': f"❌ Error: {str(e)}"}
    
    # Command: "add to [Language]: text"
    elif msg_lower.startswith("add to ") and ":" in message:
        parts = message.split(":", 1)
        lang_part = parts[0].replace("add to", "").replace("Add to", "").strip()
        text_to_add = parts[1].strip()
        
        if not text_to_add:
            return {'executed': False, 'response': f"Please provide text after 'add to {lang_part}:'"}
        
        # Check if language is valid
        available_languages = library.get_all_languages()
        if lang_part not in available_languages:
            return {'executed': False, 
                   'response': f"Language '{lang_part}' not found.\nAvailable: {', '.join(available_languages)}"}
        
        try:
            library.append_to_guide(lang_part, text_to_add)
            response = f"✅ Added to {lang_part} guide\n\nText: {text_to_add[:50]}{'...' if len(text_to_add) > 50 else ''}"
            return {'executed': True, 'response': response}
        except Exception as e:
            return {'executed': False, 'response': f"❌ Error: {str(e)}"}
    
    # Command: "show" or "list languages"
    elif msg_lower in ["show", "show all", "list", "list languages"]:
        languages = library.get_all_languages()
        response = f"Available languages:\n• " + "\n• ".join(languages)
        return {'executed': True, 'response': response}
    
    # Not a batch operation command
    return None

def test_command_parsing():
    """Test command parsing with various user inputs"""
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        test_guides_dir = os.path.join(tmpdir, "Style_Guides")
        os.makedirs(test_guides_dir)
        
        # Copy default guides to test directory
        source_guides_dir = os.path.join(
            os.path.dirname(__file__), 
            "user data", 
            "Translation_Resources", 
            "Style_Guides"
        )
        
        if os.path.exists(source_guides_dir):
            for file in os.listdir(source_guides_dir):
                if file.endswith('.md'):
                    src = os.path.join(source_guides_dir, file)
                    dst = os.path.join(test_guides_dir, file)
                    shutil.copy(src, dst)
        
        # Initialize library
        library = StyleGuideLibrary(test_guides_dir)
        library.load_all_guides()
        
        print(f"📚 Loaded {len(library.guides)} guides")
        print(f"   Languages: {', '.join(library.get_all_languages())}\n")
        
        # Test cases
        test_cases = [
            # (message, expected_executed, test_name)
            ("add to all: - New rule for all languages", True, "Add to all"),
            ("Add to all: - Another rule for all", True, "Add to all (capitalized)"),
            ("ADD TO ALL: - Uppercase command", True, "Add to all (uppercase)"),
            ("add to Dutch: - Dutch-only number formatting", True, "Add to specific language"),
            ("add to English: - English-specific punctuation", True, "Add to English"),
            ("add to German: - German quotation marks", True, "Add to German"),
            ("show", True, "Show languages command"),
            ("Show", True, "Show command (capitalized)"),
            ("list", True, "List command"),
            ("list languages", True, "List languages command"),
            ("add to all: ", False, "Add to all with no text"),
            ("add to all:", False, "Add to all with no text (no space)"),
            ("add to NonExistent: - Some rule", False, "Invalid language"),
            ("add to Dutch: ", False, "Add to Dutch with no text"),
            ("Suggest a Dutch number formatting rule", None, "General query (not a command)"),
            ("How should I format dates in German?", None, "Question (not a command)"),
            ("Tell me about style guides", None, "General inquiry (not a command)"),
        ]
        
        print("=" * 70)
        print("TEST: Command Parsing")
        print("=" * 70)
        
        passed = 0
        failed = 0
        
        for message, expected_executed, test_name in test_cases:
            result = simulate_parse_command(library, message)
            
            if expected_executed is None:
                # Should return None (not a command)
                if result is None:
                    print(f"✓ {test_name}")
                    print(f"  Message: '{message}'")
                    print(f"  Result: Not a command (routed to AI) ✓\n")
                    passed += 1
                else:
                    print(f"❌ {test_name}")
                    print(f"  Message: '{message}'")
                    print(f"  Expected: None (route to AI)")
                    print(f"  Got: {result}\n")
                    failed += 1
            else:
                # Should return dict with executed status
                if result is not None and result.get('executed') == expected_executed:
                    status = "executed ✓" if expected_executed else "validation error ✓"
                    print(f"✓ {test_name}")
                    print(f"  Message: '{message}'")
                    print(f"  Status: {status}")
                    print(f"  Response: {result.get('response', 'N/A')[:60]}...\n")
                    passed += 1
                else:
                    print(f"❌ {test_name}")
                    print(f"  Message: '{message}'")
                    print(f"  Expected executed: {expected_executed}")
                    print(f"  Got: {result}\n")
                    failed += 1
        
        # Summary
        print("=" * 70)
        print(f"RESULTS: {passed} passed, {failed} failed")
        print("=" * 70)
        
        return failed == 0

if __name__ == "__main__":
    success = test_command_parsing()
    sys.exit(0 if success else 1)
