#!/usr/bin/env python3
"""Debug term count query"""

from modules.database_manager import DatabaseManager

db = DatabaseManager()
db.connect()

# Check termbases table
print("Termbases table:")
db.cursor.execute("SELECT id, name FROM termbases")
for row in db.cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Check termbase_terms table
print("\nTermbase_terms table:")
db.cursor.execute("SELECT COUNT(*) FROM termbase_terms")
count = db.cursor.fetchone()[0]
print(f"  Total terms: {count}")

# Check actual terms
print("\nSample terms:")
db.cursor.execute("SELECT id, source_term, target_term, termbase_id FROM termbase_terms LIMIT 5")
for row in db.cursor.fetchall():
    print(f"  ID {row[0]}: {row[1]} -> {row[2]} (termbase_id={row[3]})")

# Run the actual query
print("\nRunning the actual query:")
db.cursor.execute("""
    SELECT 
        t.id, t.name,
        COUNT(gt.id) as term_count
    FROM termbases t
    LEFT JOIN termbase_terms gt ON t.id = gt.termbase_id
    GROUP BY t.id
    ORDER BY t.name ASC
""")

for row in db.cursor.fetchall():
    print(f"  {row[1]}: {row[2]} terms")

print("\nDone!")
db.connection.close()
