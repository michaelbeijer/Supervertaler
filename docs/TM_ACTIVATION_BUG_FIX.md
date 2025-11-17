# TM Activation Bug - Root Cause and Fix

## Problem Summary

Segments were not being saved to translation memories despite TMs being "activated" via the checkbox in the UI.

## Root Cause Analysis

### Investigation Timeline

1. **Initial Symptoms**: User reported segments not saving to activated TMs
2. **Added Debug Logging**: Confirmed all infrastructure working (project.id, TMMetadataManager, queries)
3. **Log Analysis Revealed**: `get_active_tm_ids(4063509871)` returned empty list `[]`
4. **Database Inspection**: `tm_activation` table had zero records for project 4063509871
5. **Code Review**: Found the bug in checkbox callback

### The Bug

**Location**: `Supervertaler.py`, line ~3075 (in `_create_tm_list_tab` method)

**Problem**: The checkbox callback was capturing `project_id` from a closure at UI creation time:

```python
# OLD BROKEN CODE:
# Get current project (ONCE at tab creation)
current_project = self.current_project if hasattr(self, 'current_project') else None
project_id = current_project.id if (current_project and hasattr(current_project, 'id')) else None

def refresh_tm_list():
    for row, tm in enumerate(tms):
        def on_toggle(checked, tm_id=tm['id']):
            if project_id:  # ← BUG: Uses captured value from closure!
                tm_metadata_mgr.activate_tm(tm_id, project_id)
```

**Why It Failed**:
1. `create_resources_tab()` is called during app initialization (line 2333)
2. At that time, NO project is loaded yet → `project_id = None`
3. The checkbox callback captures `project_id=None` in its closure
4. When user loads a project later, `self.current_project.id` is set to 4063509871
5. BUT the checkbox callback still uses the old captured value `None`
6. When checkbox is toggled: `if project_id:` evaluates to False, so nothing happens!

## The Fix

**File Modified**: `Supervertaler.py`, lines 3065-3091

**Solution**: Retrieve `project_id` dynamically instead of capturing it:

```python
# NEW FIXED CODE:
def refresh_tm_list():
    # Get current project dynamically (fresh on every refresh)
    current_project = self.current_project if hasattr(self, 'current_project') else None
    project_id = current_project.id if (current_project and hasattr(current_project, 'id')) else None
    
    for row, tm in enumerate(tms):
        def on_toggle(checked, tm_id=tm['id']):
            # Get current project ID dynamically (not from closure!)
            curr_proj = self.current_project if hasattr(self, 'current_project') else None
            curr_proj_id = curr_proj.id if (curr_proj and hasattr(curr_proj, 'id')) else None
            
            if curr_proj_id:
                if checked:
                    tm_metadata_mgr.activate_tm(tm_id, curr_proj_id)
                    self.log(f"✓ Activated TM {tm_id} for project {curr_proj_id}")
                else:
                    tm_metadata_mgr.deactivate_tm(tm_id, curr_proj_id)
                    self.log(f"✓ Deactivated TM {tm_id} for project {curr_proj_id}")
                refresh_tm_list()
            else:
                self.log(f"⚠️ Cannot toggle TM - no project loaded")
                checkbox.setChecked(not checked)  # Revert checkbox state
```

**Key Changes**:
1. Moved `project_id` retrieval INSIDE `refresh_tm_list()` function
2. Inside `on_toggle()`, get `project_id` dynamically from `self.current_project`
3. Added error handling if no project is loaded

## Verification

### Database State BEFORE Fix
```
tm_activation table: 0 records
Activations for project 4063509871: NONE
```

### Testing Steps
1. ✅ Applied fix to `Supervertaler.py`
2. ⏳ User needs to restart application
3. ⏳ Load project 'test7' (id=4063509871)
4. ⏳ Go to Translation Resources > Translation Memories > TM List
5. ⏳ Check 'Active' checkbox for 'BEIJER' TM
6. ⏳ Run `verify_tm_activation.py` to confirm database record created
7. ⏳ Confirm segment with Ctrl+Enter
8. ⏳ Check log - should show "✓ Saved to TM: BEIJER"

## Additional Files Created

1. **`verify_tm_activation.py`**: Script to inspect database state
   - Shows all TMs and their database IDs
   - Shows tm_activation table contents
   - Checks for activations for specific project

2. **`debug_and_clean_db.py`**: Already created earlier
   - Cleaned 7,142 legacy 'project' TM entries
   - Added debug logging to save functions

## Technical Notes

### Why This Closure Bug Is Common

Python closures capture variables by *reference*, not by value. When the outer function's variable changes later, the captured value doesn't update automatically. The fix is to either:
1. Pass value as default argument: `lambda x=value: func(x)` ← captures by value
2. Retrieve dynamically: `lambda: func(get_current_value())` ← no capture

In this case, we used option 2 because `project_id` can change during app lifetime.

### Database Schema (for reference)

```sql
-- Translation Memories metadata
CREATE TABLE translation_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    tm_id TEXT UNIQUE NOT NULL,  -- UUID for storage
    source_lang TEXT,
    target_lang TEXT,
    description TEXT,
    created_date TEXT,
    modified_date TEXT,
    last_used TEXT
);

-- Per-project TM activation
CREATE TABLE tm_activation (
    tm_id INTEGER NOT NULL,         -- FK to translation_memories.id
    project_id INTEGER NOT NULL,     -- FK to project ID
    is_active INTEGER DEFAULT 1,     -- 1=active, 0=inactive
    activated_date TEXT,
    PRIMARY KEY (tm_id, project_id),
    FOREIGN KEY (tm_id) REFERENCES translation_memories(id) ON DELETE CASCADE
);

-- Actual translation units
CREATE TABLE translation_units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tm_id TEXT NOT NULL,             -- FK to translation_memories.tm_id
    source_segment TEXT NOT NULL,
    target_segment TEXT NOT NULL,
    source_lang TEXT,
    target_lang TEXT,
    created_date TEXT,
    modified_date TEXT,
    created_by TEXT,
    modified_by TEXT,
    FOREIGN KEY (tm_id) REFERENCES translation_memories(tm_id) ON DELETE CASCADE
);
```

## Expected Behavior After Fix

1. User loads project → `self.current_project.id = 4063509871`
2. User opens TM List → checkboxes shown (unchecked)
3. User checks "BEIJER" TM checkbox → `on_toggle(True)` called
4. `on_toggle` gets fresh `project_id=4063509871` from `self.current_project`
5. Calls `tm_metadata_mgr.activate_tm(4, 4063509871)`
6. Database record created: `tm_activation (tm_id=4, project_id=4063509871, is_active=1)`
7. Next segment confirmation → `get_active_tm_ids(4063509871)` returns `[4]`
8. Segment saved to TM ID 4 (BEIJER)
9. Success! 🎉

## Conclusion

The entire TM infrastructure was working correctly:
- ✅ Project.id generation (MD5-based, stable)
- ✅ TMMetadataManager initialization
- ✅ Database schema and queries
- ✅ `get_active_tm_ids()` method
- ✅ `save_segment_to_activated_tms()` logic

Only the UI→Database connection was broken due to a closure variable capture bug in the checkbox callback. The fix ensures `project_id` is retrieved dynamically when the checkbox is toggled, not captured from tab creation time.
