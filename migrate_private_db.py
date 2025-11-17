"""
Apply migration to the PRIVATE database (dev mode)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.database_manager import DatabaseManager

print("="*60)
print("Migrating PRIVATE Database (dev mode)")
print("="*60)

# Use the private database
db_path = "user_data_private/Translation_Resources/supervertaler.db"
print(f"\nDatabase: {db_path}")

# Check if file exists
if os.path.exists(db_path):
    size = os.path.getsize(db_path)
    print(f"Current size: {size} bytes")
    if size == 0:
        print("⚠️  Database file is empty (0 bytes) - will recreate")

db = DatabaseManager(db_path=db_path)

# Connect (this will run migrations)
print("\nConnecting and migrating...")
success = db.connect()

if success:
    print("\n✅ Migration successful!")
    
    # Verify the columns
    cursor = db.cursor
    cursor.execute('PRAGMA table_info(termbase_terms)')
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print(f"\nColumn verification:")
    print(f"  ✓ term_uuid: {'term_uuid' in column_names}")
    print(f"  ✓ project: {'project' in column_names}")
    print(f"  ✓ client: {'client' in column_names}")
    print(f"  ✓ notes: {'notes' in column_names}")
    
    # Check term count
    cursor.execute('SELECT COUNT(*) FROM termbase_terms')
    count = cursor.fetchone()[0]
    print(f"\n  Total terms: {count}")
    
    if count > 0:
        cursor.execute('SELECT COUNT(*) FROM termbase_terms WHERE term_uuid IS NOT NULL AND term_uuid != ""')
        uuid_count = cursor.fetchone()[0]
        print(f"  Terms with UUIDs: {uuid_count}")
    
    db.close()
    
    # Check final file size
    size = os.path.getsize(db_path)
    print(f"\n  Final database size: {size:,} bytes")
else:
    print("\n❌ Migration failed!")

print("\n" + "="*60)
