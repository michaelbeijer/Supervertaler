"""
Test database creation and migration
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.database_manager import DatabaseManager

print("="*60)
print("Testing Database Creation & Migration")
print("="*60)

# Create database manager
db_path = "user_data_private/supervertaler.db"
print(f"\nDatabase path: {db_path}")

db = DatabaseManager(db_path=db_path)

# Connect (this should create tables and run migrations)
print("\nConnecting to database...")
success = db.connect()

if success:
    print("\n✅ Connection successful!")
    
    # Check what was created
    cursor = db.cursor
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    print(f"\nTables created ({len(tables)}):")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check termbase_terms specifically
    print("\n" + "-"*60)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='termbase_terms'")
    if cursor.fetchone():
        cursor.execute('PRAGMA table_info(termbase_terms)')
        columns = cursor.fetchall()
        print(f"\ntermbase_terms columns ({len(columns)}):")
        for col in columns:
            print(f"  {col[1]}: {col[2]}")
        
        column_names = [col[1] for col in columns]
        print(f"\nRequired columns present:")
        print(f"  ✓ term_uuid: {'term_uuid' in column_names}")
        print(f"  ✓ project: {'project' in column_names}")
        print(f"  ✓ client: {'client' in column_names}")
        print(f"  ✓ notes: {'notes' in column_names}")
    else:
        print("\n❌ ERROR: termbase_terms table not found!")
    
    db.close()
else:
    print("\n❌ Connection failed!")

print("\n" + "="*60)
