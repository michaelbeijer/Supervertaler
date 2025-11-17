"""
Verify TM Activation System
============================
This script checks the tm_activation table and verifies the fix.
"""

import sqlite3
import os

# Database path
db_path = os.path.join(
    os.path.dirname(__file__), 
    "user_data_private", 
    "Translation_Resources", 
    "supervertaler.db"
)

if not os.path.exists(db_path):
    print(f"❌ Database not found: {db_path}")
    exit(1)

print(f"📊 Opening database: {db_path}\n")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check translation_memories table
print("=" * 70)
print("TRANSLATION MEMORIES TABLE")
print("=" * 70)
cursor.execute("""
    SELECT id, name, tm_id, source_lang, target_lang, 
           (SELECT COUNT(*) FROM translation_units WHERE tm_id = tm.tm_id) as entry_count
    FROM translation_memories tm
    ORDER BY name
""")

tms = cursor.fetchall()
print(f"Total TMs: {len(tms)}\n")

if tms:
    print(f"{'ID':<5} {'Name':<30} {'TM_ID':<25} {'Langs':<15} {'Entries':<10}")
    print("-" * 90)
    for row in tms:
        db_id, name, tm_id, src, tgt, count = row
        langs = f"{src or '?'} → {tgt or '?'}"
        print(f"{db_id:<5} {name:<30} {tm_id:<25} {langs:<15} {count:<10}")
else:
    print("(No TMs found)")

# Check tm_activation table
print("\n" + "=" * 70)
print("TM ACTIVATION TABLE")
print("=" * 70)

cursor.execute("""
    SELECT ta.tm_id, tm.name, ta.project_id, ta.is_active, ta.activated_date
    FROM tm_activation ta
    LEFT JOIN translation_memories tm ON ta.tm_id = tm.id
    ORDER BY ta.project_id, tm.name
""")

activations = cursor.fetchall()
print(f"Total activation records: {len(activations)}\n")

if activations:
    print(f"{'TM_ID':<7} {'TM Name':<30} {'Project ID':<12} {'Active':<8} {'Activated Date':<20}")
    print("-" * 85)
    for row in activations:
        tm_id, tm_name, proj_id, is_active, date = row
        active_str = "✓ Yes" if is_active else "✗ No"
        print(f"{tm_id:<7} {tm_name:<30} {proj_id:<12} {active_str:<8} {date or 'N/A':<20}")
else:
    print("(No activation records found)")
    print("\n⚠️  This is the problem! When you check the 'Active' checkbox in the UI,")
    print("   records should be created in this table.")

# Check for project_id 4063509871 specifically
print("\n" + "=" * 70)
print("ACTIVATIONS FOR PROJECT 4063509871")
print("=" * 70)

cursor.execute("""
    SELECT ta.tm_id, tm.name, ta.is_active
    FROM tm_activation ta
    LEFT JOIN translation_memories tm ON ta.tm_id = tm.id
    WHERE ta.project_id = 4063509871
""")

proj_activations = cursor.fetchall()
if proj_activations:
    print(f"Found {len(proj_activations)} activated TMs for project 4063509871:")
    for tm_id, tm_name, is_active in proj_activations:
        status = "ACTIVE" if is_active else "INACTIVE"
        print(f"  • {tm_name} (ID {tm_id}): {status}")
else:
    print("❌ NO ACTIVATIONS FOUND for project 4063509871")
    print("\n💡 This confirms the bug: checkbox toggles are not writing to database")

conn.close()

print("\n" + "=" * 70)
print("NEXT STEPS")
print("=" * 70)
print("1. The fix has been applied to Supervertaler.py")
print("2. Restart the application")
print("3. Load the 'test7' project")
print("4. Go to Translation Resources > Translation Memories > TM List")
print("5. Check the 'Active' checkbox for a TM")
print("6. Run this script again to verify activation records were created")
print("=" * 70)
