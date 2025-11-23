import sqlite3
from pathlib import Path

print("Verifying both databases have correct schema:\n")

for db_path in ['user_data/Translation_Resources/supervertaler.db',
                'user_data_private/Translation_Resources/supervertaler.db']:
    print(f"{'='*60}")
    print(f"{db_path}")
    print(f"{'='*60}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check for TM tables
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t[0] for t in tables]
    
    has_tm = 'translation_memories' in table_names
    has_tm_activation = 'tm_activation' in table_names
    
    print(f"translation_memories: {'✓' if has_tm else '❌'}")
    print(f"tm_activation: {'✓' if has_tm_activation else '❌'}")
    
    if has_tm:
        # Check columns
        columns_result = cursor.execute('PRAGMA table_info(translation_memories)').fetchall()
        columns = [col[1] for col in columns_result]
        
        print(f"is_project_tm column: {'✓' if 'is_project_tm' in columns else '❌'}")
        print(f"read_only column: {'✓' if 'read_only' in columns else '❌'}")
        print(f"project_id column: {'✓' if 'project_id' in columns else '❌'}")
        
        # Count TMs
        count = cursor.execute('SELECT COUNT(*) FROM translation_memories').fetchone()[0]
        print(f"Number of TMs: {count}")
    
    conn.close()
    print()
