#!/usr/bin/env python
"""
Clean the public database for GitHub release.
Removes all sample/test data while preserving the schema.
New users will start with a fresh, empty database.
"""
import sqlite3
import os
import shutil
from datetime import datetime

# Public database path
db_path = 'C:/Dev/Supervertaler/user_data/Translation_Resources/supervertaler.db'

print(f"=== Cleaning Public Database for Release ===")
print(f"Database: {db_path}")
print(f"Size before: {os.path.getsize(db_path) / 1024:.1f} KB")

# Create backup
backup_path = db_path.replace('.db', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
shutil.copy(db_path, backup_path)
print(f"Backup created: {backup_path}")

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Tables to clear (data tables, not FTS internal tables)
tables_to_clear = [
    'translation_units',
    'translation_memories', 
    'tm_activation',
    'termbase_terms',
    'termbase_synonyms',
    'termbases',
    'termbase_activation',
    'termbase_project_activation',
    'tmx_files',
    'tmx_segments',
    'tmx_translation_units',
    'projects',
    'glossaries',
    'non_translatables',
    'prompt_files',
    'style_guide_files',
    'segmentation_rules',
]

print("\nClearing tables...")
for table in tables_to_clear:
    try:
        c.execute(f"DELETE FROM {table}")
        deleted = c.rowcount
        if deleted > 0:
            print(f"  ✓ {table}: deleted {deleted} rows")
        else:
            print(f"  - {table}: already empty")
    except sqlite3.OperationalError as e:
        print(f"  ✗ {table}: {e}")

# Reset auto-increment counters
print("\nResetting auto-increment counters...")
c.execute("DELETE FROM sqlite_sequence")
conn.commit()

# Rebuild FTS indexes
print("\nRebuilding FTS indexes...")
try:
    c.execute("INSERT INTO translation_units_fts(translation_units_fts) VALUES('rebuild')")
    print("  ✓ translation_units_fts rebuilt")
except Exception as e:
    print(f"  - translation_units_fts: {e}")

try:
    c.execute("INSERT INTO termbase_terms_fts(termbase_terms_fts) VALUES('rebuild')")
    print("  ✓ termbase_terms_fts rebuilt")
except Exception as e:
    print(f"  - termbase_terms_fts: {e}")

conn.commit()

# Vacuum to reclaim space
print("\nVacuuming database...")
c.execute("VACUUM")
conn.commit()

conn.close()

print(f"\nSize after: {os.path.getsize(db_path) / 1024:.1f} KB")
print("\n✅ Public database cleaned and ready for release!")
print(f"   Backup saved at: {backup_path}")
