"""Test the Trados DOCX handler"""
import sys
sys.path.insert(0, '.')

from modules.trados_docx_handler import TradosDOCXHandler, detect_bilingual_docx_type

# Detect file type
file_path = 'user_data_private/Projects/DAT FRANCE/SPV agreement NL_page3.docx.review.docx'
file_type = detect_bilingual_docx_type(file_path)
print(f"Detected file type: {file_type}")
print()

# Load the file
handler = TradosDOCXHandler()
if handler.load(file_path):
    # Extract segments
    segments = handler.extract_source_segments()
    
    print(f"\n=== FIRST 5 SEGMENTS ===")
    for seg in segments[:5]:
        print(f"Row {seg.row_index}: Status={seg.status}")
        print(f"  Source: {seg.source_text[:80]}...")
        print(f"  Tags: {seg.source_tags}")
        print(f"  Plain: {seg.plain_source[:80]}...")
        print()
    
    # Get segments for translation
    to_translate = handler.get_segments_for_translation()
    print(f"\nSegments needing translation: {len(to_translate)}")
    
    # Show segments with tags
    print("\n=== SEGMENTS WITH TAGS ===")
    for seg in segments:
        if seg.source_tags:
            print(f"Row {seg.row_index}: {seg.source_tags}")
            print(f"  Source: {seg.source_text[:100]}...")
            print()
