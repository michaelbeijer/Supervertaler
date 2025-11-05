"""Test the new TM methods"""
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from database_manager import DatabaseManager

# Connect to the database
db_path = r"user_data_private\Translation_Resources\supervertaler.db"
db = DatabaseManager(db_path=db_path)

print("=" * 60)
print("Testing TM Database Methods")
print("=" * 60)

if db.connect():
    print("\n✓ Database connected")
    
    # Test get_all_tms()
    print("\n1. Testing get_all_tms():")
    print("-" * 40)
    all_tms = db.get_all_tms(enabled_only=False)
    for tm in all_tms:
        print(f"  • {tm['name']}: {tm['entry_count']} entries")
    
    # Test get_tm_list() (alias)
    print("\n2. Testing get_tm_list():")
    print("-" * 40)
    tm_list = db.get_tm_list(enabled_only=False)
    print(f"  Found {len(tm_list)} TMs")
    
    # Test get_entry_count()
    print("\n3. Testing get_entry_count():")
    print("-" * 40)
    total = db.get_entry_count()
    print(f"  Total entries: {total}")
    
    # Test search_all()
    print("\n4. Testing search_all():")
    print("-" * 40)
    test_text = "De uitvinding heeft betrekking op"
    matches = db.search_all(test_text, threshold=0.5, max_results=10)
    print(f"  Searching for: '{test_text}'")
    print(f"  Found {len(matches)} matches:")
    for match in matches:
        print(f"    • {match['match_pct']}% - {match['tm_name']}")
        print(f"      Source: {match['source'][:50]}...")
        print(f"      Target: {match['target'][:50]}...")
    
    db.close()
    print("\n" + "=" * 60)
    print("✓ All tests complete!")
    print("=" * 60)
else:
    print("✗ Failed to connect to database")
