#!/usr/bin/env python3
"""
Database consolidation script

Removes duplicate database files from root folders, keeping only the 
Translation_Resources folder versions which are the canonical locations.
"""

import sys
from pathlib import Path
import shutil

print("="*70)
print("DATABASE CONSOLIDATION")
print("="*70)

# Files to remove (old locations)
old_db_files = [
    Path("user data") / "supervertaler.db",
    Path("user data_private") / "supervertaler.db",
]

print("\nRemoving old database files from root folders...")
for old_db in old_db_files:
    full_path = Path(__file__).parent / old_db
    if full_path.exists():
        try:
            # Create backup first
            backup_path = full_path.parent / f"{full_path.name}.backup"
            shutil.copy2(full_path, backup_path)
            print(f"  Backed up: {backup_path}")
            
            # Remove old file
            full_path.unlink()
            print(f"  ✓ Removed: {full_path}")
        except Exception as e:
            print(f"  ✗ Error removing {full_path}: {e}")
    else:
        print(f"  - Not found: {old_db}")

print("\n" + "="*70)
print("FINAL DATABASE LOCATIONS")
print("="*70)

# List final locations
final_locations = [
    ("Normal mode", Path("user data") / "Translation_Resources" / "supervertaler.db"),
    ("Dev mode", Path("user data_private") / "Translation_Resources" / "supervertaler.db"),
]

for mode, db_path in final_locations:
    full_path = Path(__file__).parent / db_path
    exists = "✓" if full_path.exists() else "✗"
    print(f"\n{exists} {mode}")
    print(f"   {full_path}")

print("\n" + "="*70)
print("✓ Database consolidation complete!")
print("="*70)
