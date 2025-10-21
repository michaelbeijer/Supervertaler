#!/usr/bin/env python3
"""
Test script for batch operations in Style Guides feature.
Tests "add to all" and "add to [Language]" commands.
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.style_guide_manager import StyleGuideLibrary

def test_batch_operations():
    """Test batch operations with temporary directory"""
    
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
                    print(f"✓ Copied {file}")
        else:
            print(f"❌ Source guides directory not found at {source_guides_dir}")
            return False
        
        # Initialize library
        library = StyleGuideLibrary(test_guides_dir)
        library.load_all_guides()
        
        print(f"\n📚 Loaded {len(library.guides)} guides")
        print(f"   Languages: {', '.join(library.get_all_languages())}")
        
        # TEST 1: Add to all languages
        print("\n" + "="*60)
        print("TEST 1: Add to all languages")
        print("="*60)
        
        test_text_1 = "- Test rule for all languages"
        try:
            library.append_to_all_guides(test_text_1)
            print(f"✓ Added to all languages: '{test_text_1}'")
            
            # Verify addition
            for lang in library.get_all_languages():
                guide_content = library.get_guide_content(lang)
                if guide_content and test_text_1 in guide_content:
                    print(f"  ✓ Verified in {lang}")
                else:
                    print(f"  ❌ NOT verified in {lang}")
                    return False
        except Exception as e:
            print(f"❌ Error adding to all: {e}")
            return False
        
        # TEST 2: Add to specific language
        print("\n" + "="*60)
        print("TEST 2: Add to specific language")
        print("="*60)
        
        test_text_2 = "- Dutch-specific number formatting rule"
        try:
            library.append_to_guide("Dutch", test_text_2)
            print(f"✓ Added to Dutch: '{test_text_2}'")
            
            # Verify Dutch has it
            dutch_guide = library.get_guide_content("Dutch")
            if dutch_guide and test_text_2 in dutch_guide:
                print(f"  ✓ Verified in Dutch")
            else:
                print(f"  ❌ NOT verified in Dutch")
                return False
            
            # Verify other languages don't have it
            for lang in ["English", "Spanish", "German", "French"]:
                guide = library.get_guide_content(lang)
                if guide and test_text_2 not in guide:
                    print(f"  ✓ Correctly NOT in {lang}")
                else:
                    print(f"  ❌ Incorrectly found in {lang}")
                    return False
        except Exception as e:
            print(f"❌ Error adding to Dutch: {e}")
            return False
        
        # TEST 3: Multiple additions
        print("\n" + "="*60)
        print("TEST 3: Multiple additions (stress test)")
        print("="*60)
        
        try:
            for i in range(1, 6):
                text = f"- Additional rule {i}"
                library.append_to_all_guides(text)
            print(f"✓ Added 5 additional rules to all languages")
            
            # Verify English has all 6 additions
            english_guide = library.get_guide_content("English")
            if english_guide:
                additions_count = sum(1 for i in range(1, 6) if f"- Additional rule {i}" in english_guide)
            else:
                additions_count = 0
            
            if additions_count == 5:
                print(f"  ✓ All 5 additional rules in English")
            else:
                print(f"  ❌ Expected 5 rules, found {additions_count}")
                return False
        except Exception as e:
            print(f"❌ Error in stress test: {e}")
            return False
        
        # TEST 4: File persistence
        print("\n" + "="*60)
        print("TEST 4: File persistence")
        print("="*60)
        
        try:
            # Get current content
            dutch_before = library.get_guide_content("Dutch")
            
            # Create new library instance and reload
            library2 = StyleGuideLibrary(test_guides_dir)
            library2.load_all_guides()
            
            dutch_after = library2.get_guide_content("Dutch")
            
            if dutch_before and dutch_after and dutch_before == dutch_after:
                print(f"✓ Content persisted correctly")
            else:
                print(f"❌ Content changed after reload")
                if dutch_before:
                    print(f"   Before: {len(dutch_before)} chars")
                if dutch_after:
                    print(f"   After: {len(dutch_after)} chars")
                return False
        except Exception as e:
            print(f"❌ Error in persistence test: {e}")
            return False
        
        # TEST 5: Invalid language handling
        print("\n" + "="*60)
        print("TEST 5: Error handling - invalid language")
        print("="*60)
        
        try:
            # This should return False for invalid language
            result = library.append_to_guide("Klingon", "- Test")
            if not result:
                print(f"✓ Correctly returned False for invalid language")
            else:
                print(f"❌ Should have returned False for invalid language")
                return False
        except Exception as e:
            print(f"✓ Raised error: {e}")
        
        # TEST 6: Empty text handling
        print("\n" + "="*60)
        print("TEST 6: Error handling - empty text")
        print("="*60)
        
        try:
            # This should raise an error or handle gracefully
            library.append_to_guide("English", "")
            print(f"⚠ Handled empty text (no error)")
        except Exception as e:
            print(f"✓ Correctly raised error for empty text: {e}")
        
        # Summary
        print("\n" + "="*60)
        print("✅ ALL BATCH OPERATION TESTS PASSED!")
        print("="*60)
        return True

if __name__ == "__main__":
    success = test_batch_operations()
    sys.exit(0 if success else 1)
