"""Test the XML declaration fix"""
import sys
sys.path.insert(0, 'C:/Dev/Supervertaler')

from modules.trados_docx_handler import TradosDOCXHandler
import zipfile

# Test file
test_file = r'C:\Dev\Supervertaler\user data_private\test_xml_declaration_fix.docx'
original_file = r'C:\Dev\Supervertaler\user data_private\Projects\trados test\trados-test\External Review\en-US\trados-test.docx.review.docx'

# Copy original and update it
import shutil
shutil.copy(original_file, test_file)

# Update with test segments
test_segments = [
    {
        'id': '1bf904784-eef6-4de3-9c30-4d82f7e35eaa',
        'status': 'Translated (100%)',
        'target': 'Test translation with <13>tags</13>'
    }
]

print("Updating test file...")
TradosDOCXHandler.update_bilingual_docx(original_file, test_segments, test_file)

print("\nChecking XML declarations...")
with zipfile.ZipFile(test_file, 'r') as z:
    # Check document.xml
    doc_xml = z.read('word/document.xml').decode('utf-8')
    first_line = doc_xml.split('\n')[0][:100]
    print(f"\ndocument.xml declaration:")
    print(f"  {first_line}")
    
    if 'version="1.0"' in first_line and 'encoding="utf-8"' in first_line:
        print("  ✅ CORRECT - matches Trados format!")
    else:
        print("  ❌ WRONG - does not match Trados format")
    
    if "standalone=" in first_line:
        print("  ⚠️  WARNING: standalone attribute present (should be absent)")
    
    # Check styles.xml
    styles_xml = z.read('word/styles.xml').decode('utf-8')
    styles_first_line = styles_xml.split('\n')[0][:100]
    print(f"\nstyles.xml declaration:")
    print(f"  {styles_first_line}")

print("\n✅ Test complete!")
print(f"Test file saved to: {test_file}")
