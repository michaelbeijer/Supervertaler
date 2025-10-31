#!/usr/bin/env python3
"""Create test termbase data for testing the highlighting feature"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.database_manager import DatabaseManager
from modules.termbase_manager import TermbaseManager

db_path = Path(__file__).parent / "user data" / "Translation_Resources" / "supervertaler.db"
print(f"Using database: {db_path}")

db = DatabaseManager(db_path=str(db_path))
db.connect()

tb_mgr = TermbaseManager(db, print)

# Create a test termbase
print("\n1. Creating test termbase...")
tb_id = tb_mgr.create_termbase(
    name="Test Termbase",
    source_lang="en",
    target_lang="nl",
    is_global=True,
    description="Test termbase for highlighting feature"
)

if not tb_id:
    print("Failed to create termbase!")
    sys.exit(1)

# Add some test terms
test_terms = [
    ("error message", "foutmelding"),
    ("error", "fout"),
    ("message", "bericht"),
    ("contact", "neem contact op"),
    ("unauthorized", "ongeautoriseerd"),
    ("permission", "toestemming"),
]

print("\n2. Adding test terms...")
for source, target in test_terms:
    tb_mgr.add_term(
        termbase_id=tb_id,
        source_term=source,
        target_term=target,
        source_lang="en",
        target_lang="nl"
    )

# Verify
print("\n3. Verifying data...")
db.cursor.execute("SELECT COUNT(*) FROM termbase_terms")
count = db.cursor.fetchone()[0]
print(f"Total termbase terms now: {count}")

db.cursor.execute("SELECT source_term, target_term FROM termbase_terms ORDER BY source_term")
print("\nTerms in database:")
for row in db.cursor.fetchall():
    print(f"  {row[0]} → {row[1]}")

# Test search
print("\n4. Testing search...")
results = db.search_termbases("error", source_lang="en", target_lang="nl")
print(f"Search for 'error': found {len(results)} results")
for r in results:
    print(f"  {r.get('source_term')} → {r.get('target_term')}")

db.connection.close()
print("\n✓ Test termbase data created!")
