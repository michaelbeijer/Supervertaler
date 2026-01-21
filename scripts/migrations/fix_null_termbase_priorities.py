"""
Migration script: Set default priorities for termbase_activation records with NULL priority.

This ensures all active termbases have a priority value (1, 2, 3, etc.) so the spinbox works.
"""

import sqlite3
import sys

def fix_null_priorities(db_path='user_data_private/resources/supervertaler.db'):
    """Set default priorities for termbase activations that have NULL priority"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all active termbase activations grouped by project
        cursor.execute("""
            SELECT DISTINCT project_id 
            FROM termbase_activation 
            WHERE is_active = 1
        """)
        projects = [row[0] for row in cursor.fetchall()]
        
        print(f"Found {len(projects)} project(s) with active termbases")
        
        total_fixed = 0
        for project_id in projects:
            # Get active termbases for this project with NULL priority
            cursor.execute("""
                SELECT termbase_id, activated_date 
                FROM termbase_activation 
                WHERE project_id = ? AND is_active = 1 AND priority IS NULL
                ORDER BY activated_date ASC
            """, (project_id,))
            
            null_priority_termbases = cursor.fetchall()
            
            if null_priority_termbases:
                # Get current max priority for this project
                cursor.execute("""
                    SELECT COALESCE(MAX(priority), 0) 
                    FROM termbase_activation 
                    WHERE project_id = ? AND is_active = 1
                """, (project_id,))
                max_priority = cursor.fetchone()[0]
                
                # Assign priorities sequentially starting from max+1
                print(f"\n  Project {project_id}: Found {len(null_priority_termbases)} termbases with NULL priority")
                print(f"  Starting priority assignment from #{max_priority + 1}")
                
                for idx, (termbase_id, activated_date) in enumerate(null_priority_termbases, start=1):
                    new_priority = max_priority + idx
                    cursor.execute("""
                        UPDATE termbase_activation 
                        SET priority = ? 
                        WHERE termbase_id = ? AND project_id = ?
                    """, (new_priority, termbase_id, project_id))
                    print(f"    ✓ Set termbase {termbase_id} to priority #{new_priority}")
                    total_fixed += 1
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ Migration complete: Set priorities for {total_fixed} termbase activation(s)")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    db_path = 'user_data_private/resources/supervertaler.db'
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    print(f"Fixing NULL priorities in: {db_path}\n")
    success = fix_null_priorities(db_path)
    sys.exit(0 if success else 1)
