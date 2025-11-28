#!/usr/bin/env python
"""Check and prepare the public database for new users"""
import sqlite3
import os

db_path = 'C:/Dev/Supervertaler/user_data/Translation_Resources/supervertaler.db'

print(f"Database exists: {os.path.exists(db_path)}")
print(f"Size: {os.path.getsize(db_path) / 1024:.1f} KB")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# List tables
c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in c.fetchall()]
print(f"\nTables: {tables}")

# Check counts
for table in tables:
    if not table.startswith('sqlite_') and not table.endswith('_fts'):
        try:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            count = c.fetchone()[0]
            print(f"  {table}: {count} rows")
        except:
            pass

# Check translation_memories
print("\n=== translation_memories ===")
c.execute("SELECT id, name, tm_id FROM translation_memories")
for r in c.fetchall():
    print(f"  {r['id']}: {r['name']} ({r['tm_id']})")

# Check translation_units
print("\n=== translation_units (sample) ===")
c.execute("SELECT source_text, target_text, tm_id FROM translation_units LIMIT 5")
for r in c.fetchall():
    print(f"  [{r['tm_id']}] {r['source_text'][:40]}...")

conn.close()
