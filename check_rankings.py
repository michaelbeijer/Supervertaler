import sqlite3
import os

# Check both possible database locations
db_paths = [
    'user_data_private/supervertaler.db',
    'user_data/supervertaler.db'
]

for db_path in db_paths:
    if os.path.exists(db_path):
        print(f"\n=== Checking {db_path} ===")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # List tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in c.fetchall()]
        print(f"Tables: {', '.join(tables)}")
        
        # Check termbases if it exists
        if 'termbases' in tables:
            c.execute("PRAGMA table_info(termbases)")
            columns = [r[1] for r in c.fetchall()]
            print(f"Termbases columns: {', '.join(columns)}")
            
            c.execute("SELECT id, name, ranking, is_project_termbase FROM termbases")
            print("\nTermbases:")
            for row in c.fetchall():
                print(f"  ID: {row[0]}, Name: {row[1]}, Ranking: {row[2]}, IsProject: {row[3]}")
        
        conn.close()
        break
