#!/usr/bin/env python3
"""Test script to verify termbase search functionality"""

import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.database_manager import DatabaseManager

# Initialize database
db_path = Path(__file__).parent / "user_data" / "Translation_Resources" / "supervertaler.db"
print(f"Database path: {db_path}")
print(f"Database exists: {db_path.exists()}")

db = DatabaseManager(db_path=str(db_path))
db.connect()

# Test 1: Count total terms
print("\n=== TEST 1: Count total terms ===")
db.cursor.execute("SELECT COUNT(*) FROM termbase_terms")
total = db.cursor.fetchone()[0]
print(f"Total termbase terms: {total}")

# Test 2: List all tables
print("\n=== TEST 2: List all tables ===")
db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = db.cursor.fetchall()
for table in tables:
    print(f"  - {table[0]}")

# Test 3: Show sample terms
print("\n=== TEST 3: Sample termbase terms ===")
db.cursor.execute("SELECT source_term, target_term, source_lang, target_lang FROM termbase_terms LIMIT 10")
results = db.cursor.fetchall()
for row in results:
    print(f"  {row[0]} → {row[1]} ({row[2]} → {row[3]})")

# Test 4: Search for "foutmelding" (error message in Dutch)
print("\n=== TEST 4: Search for 'foutmelding' ===")
results = db.search_termbases("foutmelding", source_lang="nl", target_lang="en", min_length=2)
print(f"Found {len(results)} results:")
for result in results:
    print(f"  {result.get('source_term')} → {result.get('target_term')} (priority: {result.get('priority')})")

# Test 5: Search for "error" (English)
print("\n=== TEST 5: Search for 'error' ===")
results = db.search_termbases("error", source_lang="en", target_lang="nl", min_length=2)
print(f"Found {len(results)} results:")
for result in results:
    print(f"  {result.get('source_term')} → {result.get('target_term')} (priority: {result.get('priority')})")

print("\n✓ Tests complete!")
