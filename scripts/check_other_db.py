import sqlite3

db_path = "user_data/Translation_Resources/supervertaler.db"
print(f"Checking: {db_path}\n")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if termbase_terms exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='termbase_terms'")
if cursor.fetchone():
    # Check columns
    cursor.execute('PRAGMA table_info(termbase_terms)')
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print(f"termbase_terms table found with {len(columns)} columns")
    print(f"  term_uuid exists: {'term_uuid' in column_names}")
    print(f"  project exists: {'project' in column_names}")
    print(f"  client exists: {'client' in column_names}")
    
    # Count terms
    cursor.execute('SELECT COUNT(*) FROM termbase_terms')
    count = cursor.fetchone()[0]
    print(f"\n  Total terms in database: {count}")
    
    if count > 0:
        print(f"\n  Sample terms:")
        cursor.execute('SELECT id, source_term, target_term FROM termbase_terms LIMIT 5')
        for row in cursor.fetchall():
            print(f"    {row[0]}: {row[1]} → {row[2]}")
else:
    print("termbase_terms table NOT found")

conn.close()
