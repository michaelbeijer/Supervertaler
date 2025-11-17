import sqlite3

db_path = "user_data_private/Translation_Resources/supervertaler.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if translation_memories table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='translation_memories'")
if cursor.fetchone():
    print("✅ translation_memories table exists!")
    
    cursor.execute('PRAGMA table_info(translation_memories)')
    columns = cursor.fetchall()
    print(f"\nColumns ({len(columns)}):")
    for col in columns:
        print(f"  {col[1]}: {col[2]}")
    
    cursor.execute('SELECT COUNT(*) FROM translation_memories')
    count = cursor.fetchone()[0]
    print(f"\nTotal TMs: {count}")
else:
    print("❌ translation_memories table NOT found")

# Check tm_activation table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tm_activation'")
if cursor.fetchone():
    print("\n✅ tm_activation table exists!")
else:
    print("\n❌ tm_activation table NOT found")

conn.close()
