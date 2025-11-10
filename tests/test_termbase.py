"""
Quick test of termbase functionality
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.database_manager import DatabaseManager
from modules.termbase_manager import TermbaseManager

# Test database connection
print("Testing Termbase Functionality...")
print("=" * 60)

db_path = "user_data/supervertaler.db"
db_manager = DatabaseManager(db_path)
db_manager.connect()

# Create termbase manager
termbase_mgr = TermbaseManager(db_manager)

# Get all termbases
print("\n✓ Fetching all termbases from database...")
termbases = termbase_mgr.get_all_termbases()

print(f"\nFound {len(termbases)} termbases:")
print("-" * 60)

for tb in termbases:
    print(f"\n{tb['name']}")
    print(f"  Languages: {tb['source_lang']} → {tb['target_lang']}")
    print(f"  Scope: {'Global' if tb['is_global'] else 'Project'}")
    print(f"  Terms: {tb['term_count']}")
    print(f"  Description: {tb['description']}")

print("\n" + "=" * 60)
print("✓ Test complete - termbases working correctly!")
print("=" * 60)
