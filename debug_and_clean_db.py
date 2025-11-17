"""
Debug script - shows which database is being used and cleans it
"""
import sqlite3
import os
from pathlib import Path

# Check which mode we're in
ENABLE_PRIVATE_FEATURES = os.path.exists(".supervertaler.local")

if ENABLE_PRIVATE_FEATURES:
    user_data_path = Path("user_data_private")
    print("[DEV MODE] Using user_data_private/")
else:
    user_data_path = Path("user_data")
    print("[USER MODE] Using user_data/")

db_path = user_data_path / "Translation_Resources" / "supervertaler.db"

print(f"\n📂 Database path: {db_path.absolute()}")
print(f"📂 Exists: {db_path.exists()}")

if not db_path.exists():
    print("\n❌ Database file doesn't exist!")
    print(f"\nCreating directory: {db_path.parent}")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    print("✅ Directory created")
    exit()

print(f"📂 Size: {db_path.stat().st_size:,} bytes\n")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("  CURRENT DATABASE CONTENTS")
print("=" * 70)

# Show all TMs
cursor.execute("""
    SELECT tm_id, COUNT(*) as count 
    FROM translation_units 
    GROUP BY tm_id 
    ORDER BY count DESC
""")
tms = cursor.fetchall()

if not tms:
    print("\n✅ No TM entries in database")
else:
    print("\n📊 Translation units by TM:")
    for tm_id, count in tms:
        print(f"   {tm_id:20s} {count:8,} entries")
        
        # Show samples from 'project' TM
        if tm_id == 'project':
            cursor.execute("""
                SELECT source_text, target_text 
                FROM translation_units 
                WHERE tm_id = 'project' 
                LIMIT 3
            """)
            samples = cursor.fetchall()
            print(f"\n   Sample entries from '{tm_id}':")
            for source, target in samples:
                print(f"     • {source[:40]}... → {target[:40]}...")
            print()

# Count project entries
cursor.execute("SELECT COUNT(*) FROM translation_units WHERE tm_id = 'project'")
project_count = cursor.fetchone()[0]

if project_count > 0:
    print("\n" + "=" * 70)
    print(f"  DELETING {project_count} 'project' TM ENTRIES")
    print("=" * 70)
    
    cursor.execute("DELETE FROM translation_units WHERE tm_id = 'project'")
    conn.commit()
    
    print(f"\n✅ Deleted {project_count} entries from 'project' TM")
    
    # Show what's left
    cursor.execute("""
        SELECT tm_id, COUNT(*) as count 
        FROM translation_units 
        GROUP BY tm_id 
        ORDER BY count DESC
    """)
    remaining = cursor.fetchall()
    
    if not remaining:
        print("\n✅ Database is now clean - no TM entries remaining")
    else:
        print("\n📊 Remaining TMs:")
        for tm_id, count in remaining:
            print(f"   {tm_id:20s} {count:8,} entries")

conn.close()

print("\n" + "=" * 70)
print("✅ Done!")
print("=" * 70)
