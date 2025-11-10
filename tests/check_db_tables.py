#!/usr/bin/env python3
"""Check database tables to see if old glossary_terms exists"""

import sqlite3
import os

db_paths = [
    'user_data_private/supervertaler.db',
    'user_data/supervertaler.db',
    'supervertaler.db'
]

for db_path in db_paths:
    if not os.path.exists(db_path):
        continue
    
    print(f"\n{db_path}:")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    for table in tables:
        name = table[0]
        if 'glossary' in name.lower() or 'termbase' in name.lower():
            print(f"  ✓ {name}")
    
    conn.close()

print("\nDone!")
