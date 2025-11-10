#!/usr/bin/env python3
"""Debug TM matching state and database"""

import sqlite3
import os

def check_tm_state():
    print("🔍 Checking TM (Translation Memory) state...")
    
    # Check if database exists
    db_path = "user_data/Translation_Resources/supervertaler.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    print(f"✓ Database found: {db_path}")
    
    # Connect and check TM data
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check translation_units table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='translation_units'")
        if cursor.fetchone():
            print("✓ translation_units table exists")
            
            # Count TM entries
            cursor.execute("SELECT COUNT(*) as count FROM translation_units")
            count = cursor.fetchone()['count']
            print(f"📊 TM entries in database: {count}")
            
            if count > 0:
                # Show sample entries
                cursor.execute("""
                    SELECT source_text, target_text, source_lang, target_lang, tm_id 
                    FROM translation_units 
                    LIMIT 5
                """)
                rows = cursor.fetchall()
                print("\n📋 Sample TM entries:")
                for i, row in enumerate(rows, 1):
                    print(f"  {i}. {row['source_lang']}→{row['target_lang']}: '{row['source_text'][:50]}...' → '{row['target_text'][:50]}...'")
                
                # Check language pairs
                cursor.execute("""
                    SELECT source_lang, target_lang, COUNT(*) as count 
                    FROM translation_units 
                    GROUP BY source_lang, target_lang
                """)
                pairs = cursor.fetchall()
                print("\n🌍 Language pairs in TM:")
                for pair in pairs:
                    print(f"  {pair['source_lang']} → {pair['target_lang']}: {pair['count']} entries")
            else:
                print("⚠️ No TM entries found in database")
        else:
            print("❌ translation_units table not found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_tm_state()