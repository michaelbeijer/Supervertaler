import sqlite3

conn = sqlite3.connect('user_data_private/supervertaler.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print(f'All tables in database ({len(tables)}):')
for table in tables:
    print(f'  - {table[0]}')

print('\n' + '='*60)

# Check for glossary_terms (old name)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='glossary_terms'")
if cursor.fetchone():
    print('\n✓ Found old table: glossary_terms')
    cursor.execute('PRAGMA table_info(glossary_terms)')
    columns = cursor.fetchall()
    print(f'  Columns ({len(columns)}):')
    for col in columns:
        print(f'    {col[1]}: {col[2]}')
    
    cursor.execute('SELECT COUNT(*) FROM glossary_terms')
    count = cursor.fetchone()[0]
    print(f'  Total terms: {count}')

# Check for termbase_terms (new name)  
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='termbase_terms'")
if cursor.fetchone():
    print('\n✓ Found new table: termbase_terms')
    cursor.execute('PRAGMA table_info(termbase_terms)')
    columns = cursor.fetchall()
    print(f'  Columns ({len(columns)}):')
    for col in columns:
        print(f'    {col[1]}: {col[2]}')
    
    cursor.execute('SELECT COUNT(*) FROM termbase_terms')
    count = cursor.fetchone()[0]
    print(f'  Total terms: {count}')
else:
    print('\n✗ Table termbase_terms does NOT exist')

conn.close()
