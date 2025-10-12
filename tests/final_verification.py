"""Final verification test - Full workflow"""
import sys
sys.path.insert(0, 'C:/Dev/Supervertaler')

from modules.trados_docx_handler import TradosDOCXHandler
import zipfile
import os

print("="*80)
print("TRADOS RE-IMPORT FIX - FINAL VERIFICATION")
print("="*80)

# Files
original_file = r'C:\Dev\Supervertaler\user data_private\Projects\trados test\trados-test\External Review\en-US\trados-test.docx.review.docx'
output_file = r'C:\Dev\Supervertaler\user data_private\Projects\trados test\trados-test\External Review\en-US\trados_bilingual_FIXED.review.docx'

# Create test segments with translations
test_segments = [
    {
        'id': '1bf904784-eef6-4de3-9c30-4d82f7e35eaa',
        'status': 'Translated (100%)',
        'target': 'Foldable frame for fold-up furniture'
    },
    {
        'id': '2237af40a-8bd1-48f3-a9c1-4e34850d6fa2',
        'status': 'Translated (100%)',
        'target': 'TECHNICAL FIELD'
    },
    {
        'id': '326ecfdf1-7ca6-4a56-b44d-f748a4dd2b0a',
        'status': 'Translated (100%)',
        'target': 'The invention relates to a foldable frame for a fold-up piece of furniture such as a sofa bed, as well as to an item of folding furniture comprising this framework.'
    }
]

print("\n1️⃣ Updating Trados bilingual file...")
try:
    TradosDOCXHandler.update_bilingual_docx(original_file, test_segments, output_file)
    print("   ✅ Export successful!")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n2️⃣ Verifying XML declarations...")
with zipfile.ZipFile(output_file, 'r') as z:
    xml_files = ['word/document.xml', 'word/styles.xml', 'word/settings.xml']
    
    all_correct = True
    for xml_file in xml_files:
        if xml_file not in z.namelist():
            print(f"   ⚠️  {xml_file} not found in package")
            continue
            
        content = z.read(xml_file).decode('utf-8')
        first_line = content.split('\n')[0]
        
        # Check for correct declaration
        is_correct = (
            'version="1.0"' in first_line and
            'encoding="utf-8"' in first_line and
            'standalone' not in first_line
        )
        
        status = "✅" if is_correct else "❌"
        print(f"   {status} {xml_file}: {first_line[:80]}...")
        
        if not is_correct:
            all_correct = False

if not all_correct:
    print("\n   ❌ XML declarations not correct!")
    sys.exit(1)

print("\n3️⃣ Verifying tag styling...")
from docx import Document
doc = Document(output_file)
table = doc.tables[0]

# Check if Tag style exists
try:
    tag_style = doc.styles['Tag']
    print(f"   ✅ 'Tag' style exists")
except KeyError:
    print(f"   ❌ 'Tag' style missing!")

print("\n4️⃣ Verifying translated content...")
row = table.rows[1]
target_text = row.cells[3].text
if 'Foldable frame' in target_text:
    print(f"   ✅ Translation present: {target_text[:50]}...")
else:
    print(f"   ❌ Translation missing!")

print("\n5️⃣ Verifying file size...")
file_size = os.path.getsize(output_file)
print(f"   File size: {file_size:,} bytes")
if file_size > 10000:
    print(f"   ✅ File size looks reasonable")
else:
    print(f"   ⚠️  File size seems small")

print("\n" + "="*80)
print("VERIFICATION COMPLETE!")
print("="*80)
print(f"\n✅ Fixed file ready for Trados re-import:")
print(f"   {output_file}")
print(f"\nNow try importing this file back into Trados Studio!")
print("\nIf Trados still rejects it, please provide the EXACT error message.")
