# Repository Cleanup Script
# Run this to organize documentation files into proper folders
# Date: October 7, 2025

import os
import shutil
from pathlib import Path

# Get the repository root (same directory as this script)
REPO_ROOT = Path(__file__).parent

print("=" * 60)
print("Supervertaler Repository Cleanup Script")
print("=" * 60)
print()

# Create the new folder structure
folders_to_create = [
    "docs/features",
    "docs/bugfixes",
    "docs/session_summaries",
    "docs/user_guides",
    "docs/planning",
    "docs/archive",
    "tests"
]

print("Creating folder structure...")
for folder in folders_to_create:
    folder_path = REPO_ROOT / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {folder}/")

print()

# Define file movements
file_movements = {
    # Feature documentation
    "docs/features/": [
        "FEATURES_dynamic_models_contextual_prompts.md",
        "FEATURE_bilingual_txt_import_export.md",
        "NUMBER_FORMATTING_FIX_2025-10-07.md",
        "SESSION_REPORT_FEATURE_2025-10-07.md",
        "TMX_AND_IMAGE_SUPPORT_ADDED.md"
    ],
    
    # Bugfix documentation
    "docs/bugfixes/": [
        "BUGFIX_CRITICAL_docx_table_alignment.md",
        "BUGFIX_model_selection_and_formatting_tags.md",
        "BUGFIX_tag_manager_import.md",
        "BUGFIX_tmx_export_grid_view.md",
        "BUGFIXES_translation_export_issues.md"
    ],
    
    # Session summaries
    "docs/session_summaries/": [
        "SESSION_SUMMARY_2025-10-06_bilingual_txt_dynamic_models.md",
        "SESSION_SUMMARY_dynamic_models_prompts_2025-10-06.md"
    ],
    
    # User guides
    "docs/user_guides/": [
        "QUICK_REFERENCE_dynamic_models_prompts.md",
        "QUICK_START_bilingual_txt_workflow.md"
    ],
    
    # Planning/Strategic docs
    "docs/planning/": [
        "STRATEGIC_PIVOT_TXT_bilingual_first.md"
    ],
    
    # Test files
    "tests/": [
        "test_bilingual.txt",
        "test_source_only.txt",
        "test_doc_structure.py",
        "test_tmx_export.py",
        "debug_export.py"
    ]
}

# Move files
print("Moving files...")
moved_count = 0
skipped_count = 0

for target_folder, files in file_movements.items():
    for filename in files:
        source = REPO_ROOT / filename
        destination = REPO_ROOT / target_folder / filename
        
        if source.exists():
            try:
                shutil.move(str(source), str(destination))
                print(f"  ✓ Moved: {filename} → {target_folder}")
                moved_count += 1
            except Exception as e:
                print(f"  ✗ Error moving {filename}: {e}")
        else:
            print(f"  ⊘ Skipped: {filename} (not found)")
            skipped_count += 1

print()

# Archive cat_tool_prototype
print("Archiving cat_tool_prototype...")
cat_prototype_source = REPO_ROOT / "cat_tool_prototype"
cat_prototype_dest = REPO_ROOT / "docs" / "archive" / "cat_tool_prototype"

if cat_prototype_source.exists() and cat_prototype_source.is_dir():
    try:
        if cat_prototype_dest.exists():
            print(f"  ⚠ Archive already exists: {cat_prototype_dest}")
            print(f"    Skipping archive (manual review needed)")
        else:
            shutil.move(str(cat_prototype_source), str(cat_prototype_dest))
            print(f"  ✓ Archived: cat_tool_prototype/ → docs/archive/")
            
            # Create README in archived folder
            archive_readme = cat_prototype_dest / "README_ARCHIVED.md"
            with open(archive_readme, 'w', encoding='utf-8') as f:
                f.write("""# CAT Tool Prototype (Archived)

**Archive Date**: October 7, 2025  
**Reason**: Fully integrated into Supervertaler v2.5.0

## About This Archive

This folder contains the original CAT Editor prototype that was developed separately
and then integrated into the main Supervertaler application (v2.5.0).

## Integration Status

✅ **COMPLETE** - All features from this prototype have been integrated into:
- `Supervertaler_v2.5.0 (experimental - CAT editor development).py`

## Files Preserved

All original files are preserved here for:
- Historical reference
- Code archaeology
- Feature verification
- Documentation purposes

## Do NOT Use

This code is **archived** and should not be used for active development.
Please use the main v2.5.0 application instead.

---
*For integration details, see: docs/planning/INTEGRATION_PLAN_v2.5.0.md*
""")
            print(f"  ✓ Created: README_ARCHIVED.md in archive")
            
    except Exception as e:
        print(f"  ✗ Error archiving cat_tool_prototype: {e}")
else:
    print(f"  ⊘ cat_tool_prototype not found (may already be archived)")

print()
print("=" * 60)
print("Cleanup Summary")
print("=" * 60)
print(f"Files moved: {moved_count}")
print(f"Files skipped: {skipped_count}")
print()
print("✓ Repository cleanup complete!")
print()
print("Next steps:")
print("  1. Review the new folder structure")
print("  2. Update any broken links in documentation")
print("  3. Commit changes to git")
print("  4. Continue with v2.5.0 development priorities")
print()
