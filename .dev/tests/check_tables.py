#!/usr/bin/env python3
"""List and migrate database tables from glossary to termbase"""

import sqlite3
import os

db_path = 'supervertaler.db'

if not os.path.exists(db_path):
    print(f"Database {db_path} not found")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
print("Current database tables:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()
for table in tables:
    print(f"  - {table[0]}")

# Check if old glossary_terms table exists with data
cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='glossary_terms';")
old_table_exists = cursor.fetchone()[0] > 0

if old_table_exists:
    cursor.execute("SELECT COUNT(*) FROM glossary_terms")
    count = cursor.fetchone()[0]
    print(f"\nFound glossary_terms table with {count} rows")
    
    # Show schema
    cursor.execute("PRAGMA table_info(glossary_terms)")
    print("\nglossary_terms schema:")
    for col in cursor.fetchall():
        print(f"  {col[1]:20} {col[2]}")

conn.close()
print("\nDone!")
