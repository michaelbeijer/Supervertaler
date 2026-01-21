"""
Add read_only field to termbases table and set all existing termbases to read_only=1 by default.
This ensures all termbases start with Write unchecked.
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
    
    # Check if termbases table exists
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='termbases'").fetchall()
    if not tables:
        print(f"  ⚠️ termbases table does not exist - skipping")
        conn.close()
        continue
    
    # Check if read_only column already exists
    cursor.execute("PRAGMA table_info(termbases)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'read_only' not in columns:
        # Add read_only column with default value 1 (read-only by default)
        cursor.execute("ALTER TABLE termbases ADD COLUMN read_only BOOLEAN DEFAULT 1")
        print(f"  ✓ Added read_only column to termbases")
        
        # Set all existing termbases to read_only=1
        cursor.execute("UPDATE termbases SET read_only = 1")
        rows_affected = cursor.rowcount
        print(f"  ✓ Set {rows_affected} termbases to read_only (Write unchecked by default)")
    else:
        # Column already exists, just update all to read_only=1
        cursor.execute("UPDATE termbases SET read_only = 1")
        rows_affected = cursor.rowcount
        print(f"  ✓ Column exists - set {rows_affected} termbases to read_only")
    
    conn.commit()
    conn.close()

print("\n✓ Migration complete - all termbases now default to Write unchecked")
print("Users can check the Write box for termbases they want to update with new terms.")
