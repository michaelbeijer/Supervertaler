#!/usr/bin/env python3
"""
Migrate termbases from normal database to dev database
"""

import sqlite3
from pathlib import Path

# Database paths
NORMAL_DB = Path("user data/Translation_Resources/supervertaler.db")
DEV_DB = Path("user data_private/Translation_Resources/supervertaler.db")

def migrate_termbases():
    """Copy all termbases and termbase_terms from normal to dev database"""
    
    # Connect to both databases
    normal_conn = sqlite3.connect(str(NORMAL_DB))
    dev_conn = sqlite3.connect(str(DEV_DB))
    
    normal_cursor = normal_conn.cursor()
    dev_cursor = dev_conn.cursor()
    
    try:
        # Get all termbases from normal database
        normal_cursor.execute("SELECT * FROM termbases")
        termbases = normal_cursor.fetchall()
        
        print(f"Found {len(termbases)} termbase(s) in normal database")
        
        # Insert each termbase into dev database
        for termbase in termbases:
            try:
                dev_cursor.execute("""
                    INSERT OR REPLACE INTO termbases 
                    (id, name, description, source_lang, target_lang, project_id, is_global, created_date, modified_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, termbase)
                print(f"  ✓ Inserted termbase: {termbase[1]}")
            except Exception as e:
                print(f"  ✗ Error inserting termbase {termbase[1]}: {e}")
        
        # Get all termbase terms from normal database
        normal_cursor.execute("SELECT * FROM termbase_terms")
        terms = normal_cursor.fetchall()
        
        print(f"\nFound {len(terms)} termbase term(s) in normal database")
        
        # Insert each term into dev database
        for term in terms:
            try:
                dev_cursor.execute("""
                    INSERT OR REPLACE INTO termbase_terms
                    (id, source_term, target_term, source_lang, target_lang, termbase_id, priority, 
                     project_id, synonyms, forbidden_terms, definition, context, part_of_speech, 
                     domain, case_sensitive, forbidden, tm_source_id, created_date, modified_date, 
                     usage_count, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, term)
            except Exception as e:
                print(f"  ✗ Error inserting term: {e}")
        
        print(f"  ✓ Inserted {len(terms)} term(s)")
        
        # Commit changes
        dev_conn.commit()
        
        print("\n" + "="*70)
        print("MIGRATION COMPLETE")
        print("="*70)
        
        # Verify results
        dev_cursor.execute("SELECT COUNT(*) FROM termbases")
        tb_count = dev_cursor.fetchone()[0]
        dev_cursor.execute("SELECT COUNT(*) FROM termbase_terms")
        term_count = dev_cursor.fetchone()[0]
        
        print(f"\nDev database now has:")
        print(f"  - {tb_count} termbase(s)")
        print(f"  - {term_count} termbase term(s)")
        
    except Exception as e:
        print(f"Migration error: {e}")
        dev_conn.rollback()
    finally:
        normal_conn.close()
        dev_conn.close()

if __name__ == "__main__":
    migrate_termbases()
