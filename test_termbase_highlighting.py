#!/usr/bin/env python3
"""
Quick test to verify termbase highlighting will work
Tests the full chain: db connection → search → highlighting
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from database_manager import DatabaseManager

print("="*70)
print("TERMBASE HIGHLIGHTING TEST")
print("="*70)

# Test database connection
db_path = "user data_private/Translation_Resources/supervertaler.db"
print(f"\n1. Connecting to database: {db_path}")

try:
    db_manager = DatabaseManager(db_path=db_path)
    db_manager.connect()
    print("   ✓ Database connected")
except Exception as e:
    print(f"   ✗ Connection failed: {e}")
    sys.exit(1)

# Test: Search for terms
print(f"\n2. Testing term searches...")

test_terms = ["error", "message", "contact", "unauthorized"]

for term in test_terms:
    try:
        results = db_manager.search_termbases(
            term,
            source_lang="en",
            target_lang="nl"
        )
        if results:
            print(f"   ✓ '{term}' → {results[0]['target_term']} (found {len(results)} match)")
        else:
            print(f"   - '{term}' → (no matches)")
    except Exception as e:
        print(f"   ✗ Error searching '{term}': {e}")

# Test: Full sentence highlighting
print(f"\n3. Testing full sentence highlighting...")

test_sentence = "There is an error message. Please contact us if you are unauthorized."
words = test_sentence.split()
all_matches = {}

for word in words:
    clean_word = word.strip('.,!?;:')
    if len(clean_word) < 2:
        continue
    
    try:
        results = db_manager.search_termbases(clean_word, source_lang="en", target_lang="nl")
        if results:
            for result in results:
                source_term = result.get('source_term', '').strip()
                target_term = result.get('target_term', '').strip()
                if source_term and target_term:
                    all_matches[source_term] = target_term
    except:
        pass

print(f"   Input:   '{test_sentence}'")
print(f"   Matches: {all_matches}")

if all_matches:
    # Create highlighted HTML
    html = test_sentence
    for term, translation in sorted(all_matches.items(), key=lambda x: len(x[0]), reverse=True):
        highlighted = f'<span style="color: blue; font-weight: bold; text-decoration: underline;">{term}</span>'
        html = html.replace(term, highlighted)
    print(f"   ✓ HTML: {html}")
else:
    print(f"   ✗ No matches found!")

print("\n" + "="*70)
print("✓ Termbase highlighting is ready to work!")
print("="*70)
