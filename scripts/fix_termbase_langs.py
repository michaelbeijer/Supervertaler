import sqlite3

conn = sqlite3.connect('user_data_private/Translation_Resources/supervertaler.db')
c = conn.cursor()

# Update all terms with unknown language codes
c.execute("UPDATE termbase_terms SET source_lang='nl', target_lang='en' WHERE source_lang='unknown' OR target_lang='unknown'")
affected = c.rowcount
conn.commit()

print(f'✓ Updated {affected} terms to use nl->en language codes')

# Show recent terms
c.execute('SELECT id, source_term, target_term, source_lang, target_lang FROM termbase_terms ORDER BY id DESC LIMIT 10')
rows = c.fetchall()
print('\nRecent terms now:')
for row in rows:
    print(f'  ID {row[0]}: {row[1]} = {row[2]} | Lang: {row[3]} -> {row[4]}')

conn.close()
