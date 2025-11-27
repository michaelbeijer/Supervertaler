#!/usr/bin/env python
"""Check and fix is_project_termbase flags in database"""

import sqlite3

conn = sqlite3.connect(r'C:\Dev\Supervertaler\user_data_private\Translation_Resources\supervertaler.db')
c = conn.cursor()

print("\n=== Current Termbase Status ===\n")
rows = c.execute('''
    SELECT id, name, project_id, is_project_termbase, ranking 
    FROM termbases 
    ORDER BY id
''').fetchall()

for row in rows:
    tb_id, name, project_id, is_project, ranking = row
    print(f"ID {tb_id}: {name}")
    print(f"  project_id: {project_id}")
    print(f"  is_project_termbase: {is_project}")
    print(f"  ranking: {ranking}")
    print()

# Fix: Set is_project_termbase=1 for termbases with project_id
print("\n=== Fixing project termbase flags ===\n")
c.execute('''
    UPDATE termbases
    SET is_project_termbase = 1
    WHERE project_id IS NOT NULL
    AND (is_project_termbase IS NULL OR is_project_termbase = 0)
''')
updated = c.rowcount
conn.commit()

if updated > 0:
    print(f"✓ Updated {updated} termbase(s) to have is_project_termbase=1")
    
    print("\n=== Updated Termbase Status ===\n")
    rows = c.execute('''
        SELECT id, name, project_id, is_project_termbase, ranking 
        FROM termbases 
        WHERE project_id IS NOT NULL
        ORDER BY id
    ''').fetchall()
    
    for row in rows:
        tb_id, name, project_id, is_project, ranking = row
        print(f"ID {tb_id}: {name}")
        print(f"  project_id: {project_id}")
        print(f"  is_project_termbase: {is_project}")
        print(f"  ranking: {ranking}")
        print()
else:
    print("No termbases needed updating")

conn.close()
