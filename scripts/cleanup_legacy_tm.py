"""
Clean up legacy 'project' TM entries from the database.
This removes all translation units with tm_id='project' to allow fresh start with new TM system.
"""
import sqlite3
import os

def cleanup_legacy_tm(db_path):
    """Remove all entries with tm_id='project'"""
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Count entries to be deleted
    cursor.execute("SELECT COUNT(*) FROM translation_units WHERE tm_id = 'project'")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print(f"✅ No legacy 'project' TM entries found in {db_path}")
    else:
        print(f"🗑️  Found {count} legacy 'project' TM entries in {db_path}")
        
        # Delete them
        cursor.execute("DELETE FROM translation_units WHERE tm_id = 'project'")
        conn.commit()
        
        print(f"✅ Deleted {count} entries from legacy 'project' TM")
    
    conn.close()

if __name__ == "__main__":
    # Clean both databases
    databases = [
        "user_data/supervertaler.db",
        "user_data_private/supervertaler.db"
    ]
    
    print("=" * 60)
    print("  CLEANING LEGACY 'project' TM ENTRIES")
    print("=" * 60)
    print()
    
    for db_path in databases:
        cleanup_legacy_tm(db_path)
        print()
    
    print("=" * 60)
    print("✅ Cleanup complete! You can now start fresh with the new TM system.")
    print("=" * 60)
