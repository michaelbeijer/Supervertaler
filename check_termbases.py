#!/usr/bin/env python3
"""Check what's in the termbases table"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.database_manager import DatabaseManager

db_path = Path(__file__).parent / "user data" / "Translation_Resources" / "supervertaler.db"
db = DatabaseManager(db_path=str(db_path))
db.connect()

# Check termbases
print("=== Termbases ===")
db.cursor.execute("SELECT * FROM termbases")
termbases = db.cursor.fetchall()
print(f"Total termbases: {len(termbases)}")
for tb in termbases:
    print(f"  {tb}")

# Check termbase_terms
print("\n=== Termbase Terms ===")
db.cursor.execute("SELECT COUNT(*) FROM termbase_terms")
count = db.cursor.fetchone()[0]
print(f"Total termbase terms: {count}")

# Check if any are marked for activation
print("\n=== Termbase Activation ===")
db.cursor.execute("SELECT * FROM termbase_activation")
activations = db.cursor.fetchall()
print(f"Activated termbases: {len(activations)}")
for act in activations:
    print(f"  {act}")

# Check projects to see what language pairs we have
print("\n=== Projects ===")
db.cursor.execute("SELECT id, name, source_lang, target_lang FROM projects")
projects = db.cursor.fetchall()
for proj in projects:
    print(f"  {proj}")

print("\n✓ Check complete!")
