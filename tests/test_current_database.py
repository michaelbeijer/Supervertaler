"""
Test script to verify database is accessible and working
"""

import os
import sys

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

def get_user_data_path(folder_name):
    """Get path to user_data folder"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Check for dev mode marker
    dev_marker = os.path.join(script_dir, ".supervertaler.local")
    if os.path.exists(dev_marker):
        return os.path.join(script_dir, "user_data_private", folder_name)
    else:
        return os.path.join(script_dir, "user_data", folder_name)

# Test database
db_path = os.path.join(get_user_data_path("Translation_Resources"), "supervertaler.db")
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    print(f"Database size: {os.path.getsize(db_path) / 1024:.2f} KB")
    
    # Try to connect
    from modules.translation_memory import TMDatabase
    
    print("\n=== Testing Database Connection ===")
    tm_db = TMDatabase(
        source_lang="en",
        target_lang="nl",
        db_path=db_path,
        log_callback=print
    )
    
    print(f"\n=== Database Stats ===")
    print(f"Total entries: {tm_db.get_entry_count()}")
    print(f"Project TM entries: {tm_db.get_entry_count(tm_id='project')}")
    print(f"Big Mama entries: {tm_db.get_entry_count(tm_id='big_mama')}")
    
    print(f"\n=== TM List ===")
    tm_list = tm_db.get_tm_list()
    for tm in tm_list:
        print(f"  {tm['name']}: {tm['entry_count']} entries (Enabled: {tm['enabled']})")
    
    print(f"\n=== Testing Search ===")
    # Try to search
    matches = tm_db.search_all("test", max_matches=5)
    print(f"Search for 'test': {len(matches)} matches")
    for match in matches:
        print(f"  {match['match_pct']}%: {match['source'][:50]}...")
    
    # Test exact match
    print(f"\n=== Testing Exact Match ===")
    entries = tm_db.get_tm_entries('project', limit=5)
    if entries:
        test_source = entries[0]['source']
        print(f"Testing exact match for: {test_source[:50]}...")
        exact = tm_db.get_exact_match(test_source)
        print(f"Result: {exact}")
    else:
        print("No entries in Project TM to test")
    
    tm_db.close()
    print("\n✓ Database test complete!")
else:
    print("Database does not exist yet - will be created on first launch")
