"""Test bidirectional TM writing and reading"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.database_manager import DatabaseManager

# Use a temp database for testing
db_path = os.path.join(tempfile.gettempdir(), 'test_bidirectional_tm.db')

# Clean start
if os.path.exists(db_path):
    os.remove(db_path)

db = DatabaseManager(db_path, log_callback=print)
db.connect()  # Must call connect() to initialize database

# Simulate TM with EN-NL direction
tm_id = 'test_tm_en_nl'

print('=' * 60)
print('TEST: Bidirectional TM Writing and Reading')
print('=' * 60)

# 1. Save segment from EN->NL project
print('\n1. Saving segment from EN->NL project:')
print('   Source: "Hello world" | Target: "Hallo wereld"')
db.add_translation_unit(
    source='Hello world',
    target='Hallo wereld', 
    source_lang='en',
    target_lang='nl',
    tm_id=tm_id
)
print('   ✓ Saved with source_lang=en, target_lang=nl')

# 2. Save segment from NL->EN project (reversed direction)
print('\n2. Saving segment from NL->EN project:')
print('   Source: "Goedemorgen" | Target: "Good morning"')
db.add_translation_unit(
    source='Goedemorgen',
    target='Good morning',
    source_lang='nl',  # Note: reversed!
    target_lang='en',
    tm_id=tm_id
)
print('   ✓ Saved with source_lang=nl, target_lang=en')

# 3. Search from EN->NL project perspective
print('\n3. Searching from EN->NL project perspective:')
print('   Looking for: "Hello world"')
result = db.get_exact_match('Hello world', tm_ids=[tm_id], source_lang='en', target_lang='nl', bidirectional=True)
if result:
    print(f'   ✓ Found: "{result["source_text"]}" -> "{result["target_text"]}"')
    print(f'     Reverse match: {result.get("reverse_match", False)}')
else:
    print('   ✗ No match found')

print('\n   Looking for: "Good morning"')
result = db.get_exact_match('Good morning', tm_ids=[tm_id], source_lang='en', target_lang='nl', bidirectional=True)
if result:
    print(f'   ✓ Found: "{result["source_text"]}" -> "{result["target_text"]}"')
    print(f'     Reverse match: {result.get("reverse_match", False)}')
else:
    print('   ✗ No match found')

# 4. Search from NL->EN project perspective  
print('\n4. Searching from NL->EN project perspective:')
print('   Looking for: "Goedemorgen"')
result = db.get_exact_match('Goedemorgen', tm_ids=[tm_id], source_lang='nl', target_lang='en', bidirectional=True)
if result:
    print(f'   ✓ Found: "{result["source_text"]}" -> "{result["target_text"]}"')
    print(f'     Reverse match: {result.get("reverse_match", False)}')
else:
    print('   ✗ No match found')

print('\n   Looking for: "Hallo wereld"')
result = db.get_exact_match('Hallo wereld', tm_ids=[tm_id], source_lang='nl', target_lang='en', bidirectional=True)
if result:
    print(f'   ✓ Found: "{result["source_text"]}" -> "{result["target_text"]}"')
    print(f'     Reverse match: {result.get("reverse_match", False)}')
else:
    print('   ✗ No match found')

# 5. Test fuzzy matching bidirectionally
print('\n5. Testing fuzzy match from EN->NL (searching "Hello there"):')
results = db.search_fuzzy_matches('Hello there', tm_ids=[tm_id], source_lang='en', target_lang='nl', threshold=0.5, bidirectional=True)
for r in results:
    print(f'   {r["match_pct"]}% "{r["source_text"]}" -> "{r["target_text"]}" (reverse: {r.get("reverse_match", False)})')

if not results:
    print('   (no fuzzy matches above 50% threshold)')

print('\n' + '=' * 60)
print('TEST COMPLETE')
print('=' * 60)

# Cleanup
db.connection.close()
os.remove(db_path)
