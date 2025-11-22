"""
Apply migration to the REAL database with actual terms
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.database_manager import DatabaseManager

print("="*60)
print("Migrating ACTUAL Database (user_data)")
print("="*60)

# Use the REAL database with your terms
db_path = "user_data/Translation_Resources/supervertaler.db"
print(f"\nDatabase: {db_path}")

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
    print(f"\n  Total terms preserved: {count}")
    
    # Check how many have UUIDs
    cursor.execute('SELECT COUNT(*) FROM termbase_terms WHERE term_uuid IS NOT NULL AND term_uuid != ""')
    uuid_count = cursor.fetchone()[0]
    print(f"  Terms with UUIDs: {uuid_count}")
    
    # Show sample
    if count > 0:
        print(f"\n  Sample terms:")
        cursor.execute('SELECT id, source_term, target_term, term_uuid FROM termbase_terms LIMIT 5')
        for row in cursor.fetchall():
            uuid_preview = row[3][:8] + "..." if row[3] else "None"
            print(f"    {row[0]}: {row[1]} → {row[2]} (UUID: {uuid_preview})")
    
    db.close()
else:
    print("\n❌ Migration failed!")

print("\n" + "="*60)
