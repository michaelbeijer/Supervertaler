"""
Test script for Image Extractor module
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.image_extractor import ImageExtractor

def test_image_extractor():
    """Test the ImageExtractor class"""
    
    extractor = ImageExtractor()
    
    print("=" * 60)
    print("Image Extractor Test")
    print("=" * 60)
    
    print("\n✅ ImageExtractor initialized successfully")
    print(f"   Supported formats: {extractor.supported_formats}")
    
    # Test with a sample file if it exists
    sample_file = "test.docx"
    if os.path.exists(sample_file):
        print(f"\n🔍 Testing with: {sample_file}")
        
        output_dir = "test_extracted_images"
        
        try:
            count, files = extractor.extract_images_from_docx(sample_file, output_dir)
            print(f"✅ Extracted {count} images")
            
            for f in files:
                print(f"   • {f}")
        
        except Exception as e:
            print(f"⚠️  Error: {e}")
    
    else:
        print(f"\n⚠️  No test file found ({sample_file})")
        print("   Create a DOCX file with images to test extraction")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_image_extractor()
