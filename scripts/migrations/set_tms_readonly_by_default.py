"""
One-time script to set all existing TMs to read_only=1 by default.
This ensures all TMs start with Write unchecked.
Run this once after updating to the new Read/Write checkbox system.
"""

import sqlite3
from pathlib import Path

# Update both databases
for db_path in ['user_data/resources/supervertaler.db',
                'user_data_private/resources/supervertaler.db']:
    if not Path(db_path).exists():
        print(f"❌ {db_path} does not exist - skipping")
        continue
    
    print(f"\nUpdating: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if translation_memories table exists
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='translation_memories'").fetchall()
    if not tables:
        print(f"  ⚠️ translation_memories table does not exist - skipping")
        conn.close()
        continue
    
    # Set all TMs to read_only=1 (Write unchecked by default)
    cursor.execute("UPDATE translation_memories SET read_only = 1")
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"  ✓ Set {rows_affected} TMs to read_only (Write unchecked by default)")

print("\n✓ Migration complete - all TMs now default to Write unchecked")
print("Users can check the Write box for TMs they want to update with new translations.")
