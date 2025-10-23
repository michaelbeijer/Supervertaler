"""
Debug script to test FTS5 functionality
"""

import sqlite3
import os

# Create test database
db_path = "test_fts5.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create simple table and FTS5 index
cursor.execute("""
    CREATE TABLE test_data (
        id INTEGER PRIMARY KEY,
        text TEXT
    )
""")

cursor.execute("""
    CREATE VIRTUAL TABLE test_fts 
    USING fts5(text, content=test_data, content_rowid=id)
""")

# Trigger to keep FTS in sync
cursor.execute("""
    CREATE TRIGGER test_fts_insert AFTER INSERT ON test_data BEGIN
        INSERT INTO test_fts(rowid, text) VALUES (new.id, new.text);
    END
""")

# Insert test data
test_entries = [
    "Hello world",
    "Good morning",
    "Thank you very much",
    "How are you?",
    "I am fine"
]

for entry in test_entries:
    cursor.execute("INSERT INTO test_data (text) VALUES (?)", (entry,))

conn.commit()

print("=== Test Data ===")
cursor.execute("SELECT * FROM test_data")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n=== FTS5 Content ===")
cursor.execute("SELECT * FROM test_fts")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n=== FTS5 Queries ===")

# Test various query styles
queries = [
    ("hello", "Single word (lowercase)"),
    ("Hello", "Single word (capitalized)"),
    ("hello OR world", "OR query"),
    ("good OR morning", "OR query"),
    ("thank", "Partial word"),
]

for query, description in queries:
    cursor.execute("""
        SELECT d.text 
        FROM test_data d
        JOIN test_fts ON d.id = test_fts.rowid
        WHERE test_fts MATCH ?
    """, (query,))
    
    results = cursor.fetchall()
    print(f"\nQuery: '{query}' ({description})")
    if results:
        for row in results:
            print(f"  ✓ {row[0]}")
    else:
        print(f"  ✗ No matches")

conn.close()
os.remove(db_path)
print("\n✓ Test database removed")
