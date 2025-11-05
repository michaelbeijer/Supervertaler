"""Test FTS5 query with special characters"""
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from database_manager import DatabaseManager

# Connect to the database
db_path = r"user_data_private\Translation_Resources\supervertaler.db"
db = DatabaseManager(db_path=db_path)

print("=" * 60)
print("Testing FTS5 Query with Special Characters")
print("=" * 60)

if db.connect():
    print("\n✓ Database connected")
    
    # Test queries with special characters that were causing errors
    test_queries = [
        "De uitvinding heeft betrekking op een voegplaat, voorzien van een wapening.",
        "voorzien van een wapening, die",
        "test, with, commas",
        "(parentheses) and punctuation!",
        "quotes: 'single' and \"double\"",
    ]
    
    print("\nTesting problematic queries:")
    print("-" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        try:
            matches = db.search_fuzzy_matches(query, threshold=0.5, max_results=3)
            print(f"   ✓ Success! Found {len(matches)} matches")
            for match in matches[:2]:  # Show first 2
                print(f"     • {match['match_pct']}%: {match['source_text'][:40]}...")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    db.close()
    print("\n" + "=" * 60)
    print("✓ Test complete!")
    print("=" * 60)
else:
    print("✗ Failed to connect to database")
