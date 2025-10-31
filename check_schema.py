#!/usr/bin/env python3
import sqlite3

# Check dev database schema
print("DEV DATABASE SCHEMA")
print("="*70)

conn = sqlite3.connect('user data_private/Translation_Resources/supervertaler.db')
cursor = conn.cursor()

# Check if termbases table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='termbases'")
if cursor.fetchone():
    print("\nTERMBASES table columns:")
    cursor.execute("PRAGMA table_info(termbases)")
    for col in cursor.fetchall():
        print(f"  {col}")
else:
    print("\nTERMBASES table: NOT FOUND")

# Check if termbase_terms table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='termbase_terms'")
if cursor.fetchone():
    print("\nTERMBASE_TERMS table columns:")
    cursor.execute("PRAGMA table_info(termbase_terms)")
    for col in cursor.fetchall():
        print(f"  {col}")
else:
    print("\nTERMBASE_TERMS table: NOT FOUND")

# List all tables
print("\nAll tables in dev database:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
for table in cursor.fetchall():
    print(f"  - {table[0]}")

conn.close()

print("\n" + "="*70)
print("NORMAL DATABASE SCHEMA")
print("="*70)

conn = sqlite3.connect('user data/Translation_Resources/supervertaler.db')
cursor = conn.cursor()

print("\nTERMBASES table columns:")
cursor.execute("PRAGMA table_info(termbases)")
for col in cursor.fetchall():
    print(f"  {col}")

print("\nTERMBASE_TERMS table columns:")
cursor.execute("PRAGMA table_info(termbase_terms)")
for col in cursor.fetchall():
    print(f"  {col}")

conn.close()
