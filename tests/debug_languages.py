#!/usr/bin/env python3
"""
Debug termbase matching and language settings
"""
import sqlite3
import os

db_path = "user_data_private/Translation_Resources/supervertaler.db"
if not os.path.exists(db_path):
    db_path = "user_data/Translation_Resources/supervertaler.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== TERMBASE DEBUG ===")
    
    # Check termbase languages
    cursor.execute("SELECT id, name, source_lang, target_lang FROM termbases")
    termbases = cursor.fetchall()
    print("Termbases:")
    for tb_id, name, src_lang, tgt_lang in termbases:
        print(f"  {tb_id}: {name} ({src_lang} -> {tgt_lang})")
    
    # Check termbase terms
    cursor.execute("SELECT source_term, target_term, termbase_id FROM termbase_terms ORDER BY termbase_id")
    terms = cursor.fetchall()
    print(f"\nTermbase terms ({len(terms)} total):")
    for src, tgt, tb_id in terms:
        print(f"  '{src}' -> '{tgt}' (TB: {tb_id})")
    
    # Check projects and their languages
    cursor.execute("SELECT name, source_lang, target_lang FROM projects")
    projects = cursor.fetchall()
    print(f"\nProjects ({len(projects)} total):")
    for name, src_lang, tgt_lang in projects:
        print(f"  {name}: {src_lang} -> {tgt_lang}")
    
    conn.close()
else:
    print(f"Database not found: {db_path}")