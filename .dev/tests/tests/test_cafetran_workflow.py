"""
Test script for CafeTran bilingual DOCX import/export workflow.

This script tests:
1. Loading a CafeTran bilingual DOCX
2. Extracting source segments with pipe symbols
3. Simulating translation
4. Applying pipe formatting to translations
5. Saving the updated bilingual DOCX
"""

import sys
import os

# Add modules directory to path
modules_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'modules')
if modules_dir not in sys.path:
    sys.path.insert(0, modules_dir)

from cafetran_docx_handler import CafeTranDOCXHandler


def test_cafetran_workflow():
    """Test the complete CafeTran workflow."""
    
    # Test file path
    test_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'projects',
        'test_document (CafeTran bilingual docx).docx'
    )
    
    print(f"\n{'='*70}")
    print(f"CafeTran Bilingual DOCX Workflow Test")
    print(f"{'='*70}\n")
    
    # Step 1: Check if file is CafeTran format
    print("Step 1: Checking file format...")
    is_cafetran = CafeTranDOCXHandler.is_cafetran_bilingual_docx(test_file)
    print(f"✓ File is CafeTran bilingual DOCX: {is_cafetran}\n")
    
    if not is_cafetran:
        print("ERROR: File is not a CafeTran bilingual DOCX")
        return False
    
    # Step 2: Load the file
    print("Step 2: Loading file...")
    handler = CafeTranDOCXHandler()
    if not handler.load(test_file):
        print("ERROR: Failed to load file")
        return False
    print(f"✓ File loaded successfully\n")
    
    # Step 3: Extract source segments
    print("Step 3: Extracting source segments...")
    segments = handler.extract_source_segments()
    print(f"✓ Extracted {len(segments)} segments\n")
    
    # Display first few segments with pipe symbols
    print("First 5 segments with pipe symbols:")
    for i, seg in enumerate(segments[:5]):
        print(f"\n  Segment {i+1} (ID: {seg.segment_id}):")
        print(f"    Source with pipes: {seg.source_with_pipes}")
        print(f"    Plain text: {seg.plain_text}")
        has_pipes = '|' in seg.source_with_pipes
        print(f"    Has formatting: {'✓ Yes' if has_pipes else '✗ No'}")
    
    # Step 4: Simulate translations
    print("\n\nStep 4: Simulating translations...")
    # For testing, we'll use fake Dutch translations
    test_translations = [
        "Biagio Pagano",  # No formatting
        "Van Wikipedia, de vrije encyclopedie",  # No formatting
        "Over",  # No formatting
        "Biagio Pagano (geboren 29 januari 1983) is een Italiaanse voetballer die momenteel speelt als middenvelder voor Ghivizzano Borgoamozzano.",  # Bold at start
        "Pagano had 250 wedstrijden gespeeld in de Italiaanse Serie B, inclusief 2 in de play-offs in 2008-09 Serie B.",  # No formatting
    ]
    
    # Only use first 5 for testing
    limited_translations = test_translations + ["Translation " + str(i) for i in range(6, len(segments) + 1)]
    
    print(f"✓ Created {len(limited_translations)} test translations\n")
    
    # Step 5: Update target segments with formatting
    print("Step 5: Applying pipe formatting to translations...")
    if not handler.update_target_segments(limited_translations[:len(segments)]):
        print("ERROR: Failed to update target segments")
        return False
    print(f"✓ Target segments updated\n")
    
    # Display first few updated segments
    print("First 5 segments after formatting applied:")
    for i, seg in enumerate(segments[:5]):
        print(f"\n  Segment {i+1} (ID: {seg.segment_id}):")
        print(f"    Source: {seg.source_with_pipes}")
        print(f"    Target: {seg.target_with_pipes}")
        pipes_preserved = seg.source_with_pipes.count('|') == seg.target_with_pipes.count('|')
        print(f"    Pipe count match: {'✓ Yes' if pipes_preserved else '⚠ No (heuristic applied)'}")
    
    # Step 6: Save the updated file
    print("\n\nStep 6: Saving updated bilingual DOCX...")
    output_path = test_file.replace('.docx', '_TEST_OUTPUT.docx')
    
    if not handler.save(output_path):
        print("ERROR: Failed to save file")
        return False
    
    print(f"✓ File saved to: {output_path}\n")
    
    # Step 7: Verify the saved file
    print("Step 7: Verifying saved file...")
    verify_handler = CafeTranDOCXHandler()
    if not verify_handler.load(output_path):
        print("ERROR: Failed to load saved file")
        return False
    
    verify_segments = verify_handler.extract_source_segments()
    print(f"✓ Verified file has {len(verify_segments)} segments")
    
    # Check that targets are populated
    targets_filled = sum(1 for seg in verify_segments if seg.target_with_pipes)
    print(f"✓ Targets filled: {targets_filled}/{len(verify_segments)}\n")
    
    print(f"{'='*70}")
    print(f"✓ All tests passed!")
    print(f"{'='*70}\n")
    print(f"Test output saved to: {output_path}")
    print(f"You can open this file in CafeTran to verify the formatting.\n")
    
    return True


if __name__ == "__main__":
    try:
        success = test_cafetran_workflow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
