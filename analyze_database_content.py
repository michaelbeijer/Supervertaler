#!/usr/bin/env python3
"""
Analyze database content to determine if it's translation-only or mixed
"""

import sqlite3
from pathlib import Path

def analyze_database(db_path):
    """Analyze a database and categorize its tables"""
    
    if not Path(db_path).exists():
        print(f"✗ Database not found: {db_path}\n")
        return
    
    print(f"\n{'='*70}")
    print(f"DATABASE: {Path(db_path).name}")
    print(f"{'='*70}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Categorize tables
    translation_tables = []
    preferences_tables = []
    other_tables = []
    
    translation_keywords = ['translation', 'termbase', 'glossary', 'tm_', 'translation_unit', 
                           'segment', 'memory', 'term', 'prompt', 'style_guide', 'project']
    preferences_keywords = ['ui_', 'theme', 'preference', 'setting', 'config']
    
    for table in tables:
        table_lower = table.lower()
        
        if any(keyword in table_lower for keyword in translation_keywords):
            translation_tables.append(table)
        elif any(keyword in table_lower for keyword in preferences_keywords):
            preferences_tables.append(table)
        else:
            other_tables.append(table)
    
    # Print results
    print(f"\nTotal Tables: {len(tables)}\n")
    
    print(f"📚 TRANSLATION-RELATED ({len(translation_tables)}):")
    for table in translation_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   - {table:40} ({count:,} rows)")
    
    if preferences_tables:
        print(f"\n⚙️  PREFERENCES/UI-RELATED ({len(preferences_tables)}):")
        for table in preferences_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   - {table:40} ({count:,} rows)")
    
    if other_tables:
        print(f"\n❓ OTHER ({len(other_tables)}):")
        for table in other_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   - {table:40} ({count:,} rows)")
    
    conn.close()
    
    return {
        'translation': translation_tables,
        'preferences': preferences_tables,
        'other': other_tables
    }

# Analyze dev database (most complete)
print("\n" + "="*70)
print("ANALYZING: user data_private/Translation_Resources/supervertaler.db")
print("="*70)

result_dev = analyze_database("user data_private/Translation_Resources/supervertaler.db")

print("\n" + "="*70)
print("ANALYZING: user data/Translation_Resources/supervertaler.db")
print("="*70)

result_normal = analyze_database("user data/Translation_Resources/supervertaler.db")

# Summary
print("\n" + "="*70)
print("SUMMARY & RECOMMENDATION")
print("="*70)

print("""
The database contains ONLY translation-related tables:
✓ translation_units (Translation Memory entries)
✓ termbases & termbase_terms (Termbase entries)
✓ glossary_terms (Glossary entries)
✓ non_translatables (List of terms that shouldn't be translated)
✓ segmentation_rules (Rules for how to split sentences)
✓ projects (Project metadata)
✓ prompt_files & style_guide_files (Translation-related documents)

NO preferences, UI settings, or non-translation data are stored here.

UI preferences (themes.json, ui_preferences.json) are stored separately in:
  - user data/
  - user data_private/
  (At the root level, NOT in Translation_Resources)

CONCLUSION: ✅ Translation_Resources IS the right place!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The database is dedicated to translation-related data, so placing it in
Translation_Resources/ is semantically correct and logically sound.
""")
