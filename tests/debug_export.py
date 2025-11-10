"""
Debug script to analyze DOCX export issue

This script will:
1. Load your project
2. Show which segments are translated
3. Show paragraph mapping
4. Help identify where export stops
"""

import json
import sys

# Get project file path from command line
if len(sys.argv) < 2:
    print("Usage: python debug_export.py <project_file.json>")
    sys.exit(1)

project_file = sys.argv[1]

# Load project
with open(project_file, 'r', encoding='utf-8') as f:
    project = json.load(f)

segments = project.get('segments', [])
print(f"\n{'='*80}")
print(f"PROJECT DEBUG INFO")
print(f"{'='*80}\n")

print(f"Total segments: {len(segments)}")

# Find "Career" segment
career_segments = []
for seg in segments:
    if 'career' in seg['source'].lower():
        career_segments.append(seg)

if career_segments:
    print(f"\nFound {len(career_segments)} segments containing 'Career':")
    for seg in career_segments:
        print(f"\n  Segment #{seg['id']}:")
        print(f"    Source: {seg['source']}")
        print(f"    Target: {seg.get('target', '(empty)')[:100]}")
        print(f"    Status: {seg.get('status', 'unknown')}")
        print(f"    Paragraph ID: {seg.get('paragraph_id', 'N/A')}")
        print(f"    Is table cell: {seg.get('is_table_cell', False)}")
        if seg.get('table_info'):
            print(f"    Table info: {seg['table_info']}")

# Show paragraph distribution
para_distribution = {}
for seg in segments:
    para_id = seg.get('paragraph_id', 0)
    if para_id not in para_distribution:
        para_distribution[para_id] = {'total': 0, 'translated': 0, 'segments': []}
    para_distribution[para_id]['total'] += 1
    if seg.get('target', '').strip():
        para_distribution[para_id]['translated'] += 1
    para_distribution[para_id]['segments'].append(seg['id'])

print(f"\n{'='*80}")
print(f"PARAGRAPH DISTRIBUTION")
print(f"{'='*80}\n")

# Find paragraph where Career appears
career_para_id = None
if career_segments:
    career_para_id = career_segments[0].get('paragraph_id')

for para_id in sorted(para_distribution.keys()):
    info = para_distribution[para_id]
    marker = " ← CAREER HERE" if para_id == career_para_id else ""
    print(f"Para {para_id}: {info['translated']}/{info['total']} translated, "
          f"segments {info['segments']}{marker}")

# Check for gaps
print(f"\n{'='*80}")
print(f"CHECKING FOR ISSUES")
print(f"{'='*80}\n")

# Check if all segments after Career are untranslated
if career_para_id is not None:
    after_career = [seg for seg in segments if seg.get('paragraph_id', 0) > career_para_id]
    untranslated_after = [seg for seg in after_career if not seg.get('target', '').strip()]
    
    if untranslated_after:
        print(f"⚠️  WARNING: {len(untranslated_after)}/{len(after_career)} segments after 'Career' are untranslated!")
        print(f"   This would explain why export stops at 'Career'")
    else:
        print(f"✓ All segments after 'Career' are translated")
        print(f"  Export issue may be with paragraph mapping, not translations")

# Check for table cells
table_cells = [seg for seg in segments if seg.get('is_table_cell', False)]
print(f"\nTable cells: {len(table_cells)}")
if table_cells:
    print(f"  First table cell: paragraph {table_cells[0].get('paragraph_id')}")
    print(f"  Last table cell: paragraph {table_cells[-1].get('paragraph_id')}")

print(f"\n{'='*80}\n")
