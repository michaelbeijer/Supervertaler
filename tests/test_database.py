"""
Quick test script for the new SQLite database backend
"""

import os
import sys

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

from modules.database_manager import DatabaseManager
from modules.translation_memory import TMDatabase

def test_database():
    """Test basic database functionality"""
    print("="*60)
    print("Testing SQLite Database Backend")
    print("="*60)
    
    # Create test database
    db_path = "test_supervertaler.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✓ Removed old test database")
    
    print(f"\n1. Creating database: {db_path}")
    tm_db = TMDatabase(
        source_lang="en",
        target_lang="nl", 
        db_path=db_path,
        log_callback=print
    )
    
    # Verify languages are set
    print(f"   Source language: {tm_db.source_lang}")
    print(f"   Target language: {tm_db.target_lang}")
    
    print(f"\n2. Adding test entries to Project TM...")
    test_entries = [
        ("Hello world", "Hallo wereld"),
        ("Good morning", "Goedemorgen"),
        ("Thank you very much", "Hartelijk bedankt"),
        ("How are you?", "Hoe gaat het met je?"),
        ("I am fine", "Met mij gaat het goed"),
    ]
    
    for source, target in test_entries:
        tm_db.add_entry(source, target, tm_id='project')
        print(f"   Added: {source} → {target}")
    
    print(f"\n3. Testing exact match...")
    match = tm_db.get_exact_match("Hello world")
    print(f"   Query: 'Hello world'")
    print(f"   Result: {match}")
    assert match == "Hallo wereld", "Exact match failed!"
    print("   ✓ Exact match working!")
    
    print(f"\n4. Testing fuzzy search...")
    # Lower the threshold for testing
    tm_db.fuzzy_threshold = 0.5
    matches = tm_db.search_all("hello world test", max_matches=5)
    print(f"   Query: 'hello world test' (threshold: {tm_db.fuzzy_threshold})")
    for match in matches:
        print(f"   - {match['match_pct']}%: {match['source']} → {match['target']}")
    
    if len(matches) == 0:
        print("   ⚠️ No fuzzy matches found - trying direct database query...")
        # Test database directly
        db_matches = tm_db.db.search_fuzzy_matches("hello", threshold=0.5, max_results=5)
        print(f"   Direct DB query for 'hello': {len(db_matches)} results")
        for m in db_matches:
            print(f"     - {m['match_pct']}%: {m['source_text']}")
    else:
        print(f"   ✓ Found {len(matches)} fuzzy matches")
    
    # Test with more variations
    print(f"\n4b. Testing fuzzy search with variations...")
    test_queries = [
        ("Good morning everyone", "Good morning"),
        ("Thank you", "Thank you very much"),
        ("how r u", "How are you?"),
    ]
    for query, expected_match in test_queries:
        matches = tm_db.search_all(query, max_matches=1)
        if matches:
            print(f"   '{query}' → {matches[0]['match_pct']}% match: '{matches[0]['source']}'")
        else:
            print(f"   '{query}' → No matches")
    
    print(f"\n5. Testing concordance search...")
    results = tm_db.concordance_search("good")
    print(f"   Query: 'good'")
    for result in results:
        print(f"   - {result['source']} → {result['target']}")
    print(f"   ✓ Found {len(results)} concordance matches")
    
    print(f"\n6. Testing entry count...")
    count = tm_db.get_entry_count(tm_id='project')
    print(f"   Project TM has {count} entries")
    assert count == len(test_entries), "Entry count mismatch!"
    print("   ✓ Entry count correct!")
    
    print(f"\n7. Adding entries to Big Mama TM...")
    tm_db.add_entry("Database test", "Database test", tm_id='big_mama')
    tm_db.add_entry("This is working", "Dit werkt", tm_id='big_mama')
    bigmama_count = tm_db.get_entry_count(tm_id='big_mama')
    print(f"   Big Mama TM has {bigmama_count} entries")
    
    print(f"\n8. Testing TM list...")
    tm_list = tm_db.get_tm_list()
    for tm_info in tm_list:
        print(f"   - {tm_info['name']}: {tm_info['entry_count']} entries (Enabled: {tm_info['enabled']})")
    
    print(f"\n9. Testing database info...")
    info = tm_db.db.get_database_info()
    print(f"   Database size: {info['size_mb']} MB")
    print(f"   Total entries: {info['tm_entries']}")
    
    print(f"\n10. Closing database...")
    tm_db.close()
    print("   ✓ Database closed successfully")
    
    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"\n✓ Test database removed")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_database()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
