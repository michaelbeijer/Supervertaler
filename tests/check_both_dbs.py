#!/usr/bin/env python3
"""Check both databases for termbase content"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.database_manager import DatabaseManager

# Check both databases
db_paths = [
    Path(__file__).parent / "user data" / "Translation_Resources" / "supervertaler.db",
    Path(__file__).parent / "user data_private" / "Translation_Resources" / "supervertaler.db",
]

for db_path in db_paths:
    print(f"\n{'='*60}")
    print(f"Database: {db_path.name} in {db_path.parent.name}")
    print(f"Exists: {db_path.exists()}")
    print('='*60)
    
    if not db_path.exists():
        continue
    
    try:
        db = DatabaseManager(db_path=str(db_path))
        db.connect()
        
        # Count termbases
        db.cursor.execute("SELECT COUNT(*) FROM termbases")
        tb_count = db.cursor.fetchone()[0]
        print(f"\nTotal termbases: {tb_count}")
        
        # List all termbases
        if tb_count > 0:
            db.cursor.execute("SELECT id, name, source_lang, target_lang, is_global FROM termbases")
            for row in db.cursor.fetchall():
                print(f"  ID {row[0]}: {row[1]} ({row[2]} → {row[3]}) {'[GLOBAL]' if row[4] else '[PROJECT]'}")
        
        # Count termbase terms
        db.cursor.execute("SELECT COUNT(*) FROM termbase_terms")
        term_count = db.cursor.fetchone()[0]
        print(f"\nTotal termbase terms: {term_count}")
        
        # Show sample terms
        if term_count > 0:
            db.cursor.execute("""
                SELECT source_term, target_term, source_lang, target_lang 
                FROM termbase_terms LIMIT 5
            """)
            print("\nSample terms:")
            for row in db.cursor.fetchall():
                print(f"  {row[0]} → {row[1]} ({row[2]} → {row[3]})")
        
        db.connection.close()
    except Exception as e:
        print(f"Error: {e}")

print("\n✓ Check complete!")
