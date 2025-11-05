#!/usr/bin/env python3
"""Add more test termbase data to cover both language directions"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.database_manager import DatabaseManager

db_path = Path(__file__).parent / "user_data" / "Translation_Resources" / "supervertaler.db"
db = DatabaseManager(db_path=str(db_path))
db.connect()

# Get existing termbases
db.cursor.execute("SELECT id, name, source_lang, target_lang FROM termbases")
termbases = db.cursor.fetchall()

print("Existing termbases:")
for tb in termbases:
    print(f"  ID {tb[0]}: {tb[1]} ({tb[2]} → {tb[3]})")

# Get current termbase term count
db.cursor.execute("SELECT COUNT(*) FROM termbase_terms")
total_terms = db.cursor.fetchone()[0]
print(f"\nTotal termbase terms: {total_terms}")

# Show all current terms
print("\nAll current terms:")
db.cursor.execute("""
    SELECT t.source_term, t.target_term, t.source_lang, t.target_lang, tb.name
    FROM termbase_terms t
    JOIN termbases tb ON t.termbase_id = tb.id
    ORDER BY tb.name, t.source_lang
""")
for row in db.cursor.fetchall():
    print(f"  {row[0]} → {row[1]} ({row[2]} → {row[3]}) in '{row[4]}'")

# Check if we can search by Dutch terms too
print("\n\nSearching for 'fout'...")
db.cursor.execute("""
    SELECT source_term, target_term, source_lang, target_lang
    FROM termbase_terms WHERE source_term LIKE '%fout%'
""")
results = db.cursor.fetchall()
print(f"Found {len(results)} results")
for r in results:
    print(f"  {r[0]} ({r[2]}) → {r[1]} ({r[3]})")

db.connection.close()
print("\n✓ Done!")
