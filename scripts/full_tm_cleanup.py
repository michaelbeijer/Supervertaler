"""
Complete TM cleanup - removes ALL 'project' TM entries and shows current state
"""
import sqlite3
import os

def cleanup_database(db_path):
    """Clean up and show TM state"""
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"DATABASE: {db_path}")
    print(f"{'='*60}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Show ALL translation_units grouped by tm_id
    print("\n📊 Current TM entries:")
    cursor.execute("""
        SELECT tm_id, COUNT(*) as count 
        FROM translation_units 
        GROUP BY tm_id 
        ORDER BY count DESC
    """)
    all_tms = cursor.fetchall()
    if all_tms:
        for tm_id, count in all_tms:
            print(f"   • {tm_id}: {count} entries")
    else:
        print("   (no entries)")
    
    # Delete 'project' TM
    cursor.execute("SELECT COUNT(*) FROM translation_units WHERE tm_id = 'project'")
    project_count = cursor.fetchone()[0]
    
    if project_count > 0:
        print(f"\n🗑️  Deleting {project_count} 'project' TM entries...")
        cursor.execute("DELETE FROM translation_units WHERE tm_id = 'project'")
        conn.commit()
        print(f"✅ Deleted!")
    else:
        print(f"\n✅ No 'project' TM entries to delete")
    
    # Show translation_memories table
    print("\n📋 Registered TMs (translation_memories table):")
    try:
        cursor.execute("SELECT id, name, tm_id, entry_count FROM translation_memories")
        tms = cursor.fetchall()
        if tms:
            for db_id, name, tm_id, count in tms:
                print(f"   • {name} (tm_id={tm_id}, db_id={db_id}) - {count} entries")
        else:
            print("   (no registered TMs)")
    except Exception as e:
        print(f"   (translation_memories table doesn't exist: {e})")
    
    # Show tm_activation table
    print("\n🔘 TM Activations (tm_activation table):")
    try:
        cursor.execute("""
            SELECT ta.tm_id, ta.project_id, ta.is_active, tm.name
            FROM tm_activation ta
            LEFT JOIN translation_memories tm ON ta.tm_id = tm.id
        """)
        activations = cursor.fetchall()
        if activations:
            for tm_id, proj_id, is_active, name in activations:
                status = "✓ ACTIVE" if is_active else "✗ inactive"
                print(f"   • TM {tm_id} ('{name}') - Project {proj_id}: {status}")
        else:
            print("   (no activations)")
    except Exception as e:
        print(f"   (tm_activation table doesn't exist: {e})")
    
    conn.close()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  COMPLETE TM CLEANUP & STATUS")
    print("="*60)
    
    # Clean both databases
    databases = [
        "user_data/supervertaler.db",
        "user_data_private/supervertaler.db"
    ]
    
    for db_path in databases:
        cleanup_database(db_path)
    
    print("\n" + "="*60)
    print("✅ Cleanup complete!")
    print("="*60)
    print()
