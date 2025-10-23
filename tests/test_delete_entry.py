"""Test delete_entry method is accessible"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.translation_memory import TMDatabase

def test_delete_entry():
    """Test that delete_entry method exists and is callable"""
    
    # Create TMDatabase instance
    tm_db = TMDatabase(db_path=":memory:")  # Use in-memory database
    
    # Check that delete_entry method exists
    assert hasattr(tm_db, 'delete_entry'), "TMDatabase should have delete_entry method"
    assert callable(tm_db.delete_entry), "delete_entry should be callable"
    
    # Add an entry
    tm_db.add_entry("Test source", "Test target", tm_id='project')
    
    # Verify it was added
    entries = tm_db.get_tm_entries('project')
    assert len(entries) > 0, "Entry should be added"
    
    # Delete the entry
    tm_db.delete_entry(tm_id='project', source="Test source", target="Test target")
    
    # Verify it was deleted
    entries_after = tm_db.get_tm_entries('project')
    assert len(entries_after) == 0, "Entry should be deleted"
    
    print("✅ All tests passed!")
    print("  - delete_entry method exists")
    print("  - delete_entry is callable")
    print("  - delete_entry successfully removes entries")
    
    tm_db.close()

if __name__ == "__main__":
    test_delete_entry()
