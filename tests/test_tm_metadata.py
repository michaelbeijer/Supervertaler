"""Test TM metadata structure"""
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from translation_memory import TMDatabase

# Create TM database
db_path = r"user_data_private\Translation_Resources\supervertaler.db"
tm_db = TMDatabase(source_lang="en", target_lang="nl", db_path=db_path)

print("=" * 60)
print("Testing TM Metadata Structure")
print("=" * 60)

print("\n1. tm_metadata structure:")
print(f"Type: {type(tm_db.tm_metadata)}")
print(f"Keys: {tm_db.tm_metadata.keys()}")

for tm_id, meta in tm_db.tm_metadata.items():
    print(f"\n  {tm_id}:")
    print(f"    Type: {type(meta)}")
    print(f"    Content: {meta}")
    print(f"    'enabled' key exists: {'enabled' in meta}")
    print(f"    'enabled' value: {meta.get('enabled', 'NOT FOUND')}")

print("\n2. get_tm_list() returns:")
tm_list = tm_db.get_tm_list(enabled_only=False)
print(f"Type: {type(tm_list)}")
print(f"Length: {len(tm_list)}")

for i, tm_info in enumerate(tm_list):
    print(f"\n  Item {i}:")
    print(f"    Type: {type(tm_info)}")
    print(f"    Content: {tm_info}")
    print(f"    'enabled' key exists: {'enabled' in tm_info}")
    if isinstance(tm_info, dict):
        print(f"    'enabled' value: {tm_info.get('enabled', 'NOT FOUND')}")

tm_db.close()
print("\n" + "=" * 60)
