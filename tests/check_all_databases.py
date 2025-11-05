#!/usr/bin/env python3
"""Check which database files exist and what data they contain"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Check all possible database locations
db_locations = [
    Path("user_data") / "supervertaler.db",
    Path("user_data") / "Translation_Resources" / "supervertaler.db",
    Path("user_data_private") / "supervertaler.db",
    Path("user_data_private") / "Translation_Resources" / "supervertaler.db",
]

print("="*70)
print("DATABASE FILE LOCATIONS")
print("="*70)

for db_path in db_locations:
    full_path = Path(__file__).parent / db_path
    exists = full_path.exists()
    size = f"{full_path.stat().st_size} bytes" if exists else "N/A"
    print(f"\n{'✓' if exists else '✗'} {db_path}")
    print(f"  Full path: {full_path}")
    print(f"  Size: {size}")
    
    if exists:
        try:
            from modules.database_manager import DatabaseManager
            db = DatabaseManager(db_path=str(full_path))
            db.connect()
            
            # Check what tables exist
            db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = db.cursor.fetchall()
            print(f"  Tables: {len(tables)}")
            
            # Count termbases
            if any(t[0] == 'termbases' for t in tables):
                db.cursor.execute("SELECT COUNT(*) FROM termbases")
                tb_count = db.cursor.fetchone()[0]
                print(f"    - Termbases: {tb_count}")
                
                db.cursor.execute("SELECT COUNT(*) FROM termbase_terms")
                term_count = db.cursor.fetchone()[0]
                print(f"    - Termbase terms: {term_count}")
            
            # Count TM entries
            if any(t[0] == 'translation_units' for t in tables):
                db.cursor.execute("SELECT COUNT(*) FROM translation_units")
                tm_count = db.cursor.fetchone()[0]
                print(f"    - Translation memory entries: {tm_count}")
            
            db.connection.close()
        except Exception as e:
            print(f"  Error reading: {e}")

print("\n" + "="*70)
print("RECOMMENDATION")
print("="*70)
print("""
The correct database file location should be:
  user_data/Translation_Resources/supervertaler.db (normal mode)
  user_data_private/Translation_Resources/supervertaler.db (dev mode)

This is because:
1. All translation resources (TMs, termbases, glossaries) go in Translation_Resources/
2. The database file should be in the same folder as other resources
3. This matches the existing structure with Glossaries/, Non-translatables/, etc.
""")
