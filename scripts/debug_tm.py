#!/usr/bin/env python
"""Debug script to check TM database contents"""
import sqlite3
import os

# DEV MODE uses user_data_private
db_path = r"C:\Dev\Supervertaler\user_data_private\Translation_Resources\supervertaler.db"
print(f"Checking database: {db_path}")
print(f"Exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Search for "rendering" in translation_units
    print("\n=== Searching for 'rendering' ===")
    cur.execute("SELECT tm_id, source_text, target_text FROM translation_units WHERE source_text LIKE '%rendering%' LIMIT 10")
    rows = cur.fetchall()
    print(f"Found {len(rows)} matches")
    for r in rows:
        print(f"\n  TM: {r[0]}")
        print(f"  Source: {r[1][:100]}...")
        print(f"  Target: {r[2][:100]}...")
    
    # Check what TM IDs exist in translation_units
    print("\n=== TM IDs in translation_units ===")
    cur.execute("SELECT DISTINCT tm_id, COUNT(*) as cnt FROM translation_units GROUP BY tm_id")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]} entries")
    
    # Check what's in translation_memories
    print("\n=== translation_memories entries ===")
    cur.execute("SELECT id, name, tm_id FROM translation_memories")
    for r in cur.fetchall():
        print(f"  DB ID: {r[0]}, Name: {r[1]}, tm_id: {r[2]}")
    
    conn.close()
