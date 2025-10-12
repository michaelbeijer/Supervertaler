"""Simple check of tag export"""
from docx import Document

output_file = r'C:\Dev\Supervertaler\user data_private\test_tag_fix_verification.docx'

try:
    doc = Document(output_file)
    table = doc.tables[0]
    
    print(f"Total rows: {len(table.rows)}")
    
    # Check each row
    for i, row in enumerate(table.rows):
        seg_id = row.cells[0].text
        target = row.cells[3].text
        
        if '<' in target and '>' in target:
            print(f"\nRow {i} - Segment: {seg_id[:20]}...")
            print(f"Target: {target[:100]}...")
            
            if '<14>14>' in target or '</14>14>' in target:
                print("❌ DUPLICATED TAGS FOUND!")
            elif '<14>Biagio' in target:
                print("✅ Tags look correct!")
                
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
