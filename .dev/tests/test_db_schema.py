#!/usr/bin/env python3
"""Test database schema after terminology fixes"""

import sqlite3

conn = sqlite3.connect('supervertaler.db')
cursor = conn.cursor()

# Check what tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()
print("Database tables:")
for table in tables:
    print(f"  - {table[0]}")

# Check termbase_terms schema
print("\nChecking termbase_terms schema:")
cursor.execute("PRAGMA table_info(termbase_terms)")
columns = cursor.fetchall()

if columns:
    for col in columns:
        print(f"  {col[1]:20} {col[2]:15} NULL:{col[3]}")
    
    # Check source_lang and target_lang specifically
    for col in columns:
        if col[1] in ['source_lang', 'target_lang']:
            default = col[4]
            not_null = col[3]
            print(f"\n  {col[1]} - DEFAULT: {default}, NOT NULL: {not_null}")
else:
    print("  ERROR: Table does not exist!")

conn.close()
print("\nDone!")
