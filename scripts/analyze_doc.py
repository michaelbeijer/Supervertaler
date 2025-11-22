from docx import Document
import re

doc_path = r"C:\Dev\Supervertaler\user_data_private\Prompt_Library\Project Prompts\20250926 STEIN-002-BE-EP Application to file.docx_eng-US_translated.docx"
doc = Document(doc_path)

print("="*80)
print("DOCUMENT SYNCHRONIZATION ANALYSIS")
print("="*80)
print()

table = doc.tables[0]
total_rows = len(table.rows)
print(f"Total rows in table: {total_rows}")
print(f"Total columns: {len(table.columns)}")
print()

# Sample beginning, middle, and end
sample_indices = [
    ("BEGINNING", list(range(10, min(30, total_rows)))),
    ("MIDDLE", list(range(total_rows//2 - 10, total_rows//2 + 10))),
    ("END", list(range(max(total_rows - 30, 0), total_rows)))
]

issues_found = []

for section_name, indices in sample_indices:
    print(f"\n{'='*80}")
    print(f"ANALYZING: {section_name} (rows {indices[0]}-{indices[-1]})")
    print(f"{'='*80}\n")
    
    for i in indices[:15]:  # Show first 15 of each section
        if i >= total_rows:
            break
            
        row = table.rows[i]
        cells_text = [cell.text.strip() for cell in row.cells]
        
        # Check each cell
        for col_idx, text in enumerate(cells_text):
            if not text:
                continue
                
            # Check for multiple sentences/segments in one cell
            sentence_count = len([s for s in re.split(r"[.!?]+", text) if s.strip()])
            
            # Check for numbering patterns
            has_multiple_numbers = len(re.findall(r"^\d+\.", text, re.MULTILINE)) > 1
            
            # Check for concatenated translations (multiple uppercase starts)
            lines = text.split("\n")
            uppercase_starts = sum(1 for line in lines if line and line[0].isupper() and len(line) > 20)
            
            if sentence_count > 3 or has_multiple_numbers or uppercase_starts > 2:
                issues_found.append({
                    "row": i,
                    "col": col_idx,
                    "section": section_name,
                    "sentence_count": sentence_count,
                    "multiple_numbers": has_multiple_numbers,
                    "uppercase_starts": uppercase_starts,
                    "text_preview": text[:200] + "..." if len(text) > 200 else text
                })
                
        # Display sample
        print(f"Row {i}:")
        for col_idx, text in enumerate(cells_text):
            if text:
                preview = text[:150].replace("\n", " ") + ("..." if len(text) > 150 else "")
                print(f"  Col {col_idx}: {preview}")
        print()

print(f"\n{'='*80}")
print(f"ISSUES SUMMARY")
print(f"{'='*80}\n")
print(f"Total potential issues found: {len(issues_found)}")

if issues_found:
    print("\nDETAILED ISSUE BREAKDOWN:\n")
    for idx, issue in enumerate(issues_found[:20], 1):  # Show first 20 issues
        print(f"{idx}. Row {issue['row']}, Column {issue['col']} ({issue['section']})")
        print(f"   - Sentences: {issue['sentence_count']}")
        print(f"   - Multiple numbering: {issue['multiple_numbers']}")
        print(f"   - Multiple uppercase starts: {issue['uppercase_starts']}")
        print(f"   - Preview: {issue['text_preview']}")
        print()
