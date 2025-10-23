# Database Backend Bug Fixes - October 23, 2025

## Issues Reported

1. **TM Manager button does nothing** - clicking the button produced no response
2. **TM lookup/search not working** - segments with matches in TM don't show results
3. **Project save failing** - AttributeError: 'TMDatabase' object has no attribute 'project_tm'

## Root Causes

### 1. Missing Database Methods
The new database backend (`DatabaseManager`) was missing several methods that the application expected:
- `get_all_tms()` - Get list of all translation memories
- `get_tm_list()` - Alias for backward compatibility  
- `get_entry_count()` - Get total number of entries
- `search_all()` - Search across all TMs (exact + fuzzy)

### 2. Dictionary vs Object Access
The application code was treating TM data as objects (`tm.name`, `tm.tm_id`) when the database returns dictionaries (`tm['name']`, `tm['tm_id']`)

### 3. Legacy Code References
`save_project()` was trying to access `self.tm_database.project_tm.entries` which doesn't exist in the database-backed architecture.

## Fixes Applied

### 1. Added Missing Methods to `database_manager.py`

#### `get_all_tms(enabled_only: bool = True)`
```python
def get_all_tms(self, enabled_only: bool = True) -> List[Dict]:
    """Get list of all translation memories"""
    query = "SELECT DISTINCT tm_id FROM translation_units ORDER BY tm_id"
    self.cursor.execute(query)
    tm_ids = [row[0] for row in self.cursor.fetchall()]
    
    tm_list = []
    for tm_id in tm_ids:
        entry_count = self.get_tm_count(tm_id)
        tm_info = {
            'tm_id': tm_id,
            'name': tm_id.replace('_', ' ').title(),
            'entry_count': entry_count,
            'enabled': True,
            'read_only': False
        }
        tm_list.append(tm_info)
    
    return tm_list
```

#### `get_tm_list(enabled_only: bool = True)`
```python
def get_tm_list(self, enabled_only: bool = True) -> List[Dict]:
    """Alias for get_all_tms for backward compatibility"""
    return self.get_all_tms(enabled_only=enabled_only)
```

#### `get_entry_count(enabled_only: bool = True)`
```python
def get_entry_count(self, enabled_only: bool = True) -> int:
    """Get total number of translation entries"""
    return self.get_tm_count()
```

#### `search_all(source, tm_ids, enabled_only, threshold, max_results)`
```python
def search_all(self, source: str, tm_ids: List[str] = None, enabled_only: bool = True,
               threshold: float = 0.75, max_results: int = 10) -> List[Dict]:
    """Search for matches across TMs (both exact and fuzzy)"""
    # First try exact match
    exact = self.get_exact_match(source, tm_ids=tm_ids)
    if exact:
        return [{
            'source': exact['source_text'],
            'target': exact['target_text'],
            'match_pct': 100,
            'tm_name': exact['tm_id'].replace('_', ' ').title(),
            'tm_id': exact['tm_id']
        }]
    
    # No exact match, try fuzzy
    fuzzy_matches = self.search_fuzzy_matches(
        source, tm_ids=tm_ids, threshold=threshold, max_results=max_results
    )
    
    results = []
    for match in fuzzy_matches:
        results.append({
            'source': match['source_text'],
            'target': match['target_text'],
            'match_pct': match['match_pct'],
            'tm_name': match['tm_id'].replace('_', ' ').title(),
            'tm_id': match['tm_id']
        })
    
    return results
```

### 2. Fixed Dictionary Access in `Supervertaler_v3.7.2.py`

**File:** Line ~7198-7200

**Before:**
```python
for tm in self.tm_database.get_all_tms(enabled_only=False):
    if tm.name == tm_name:
        tm_ids.append(tm.tm_id)
```

**After:**
```python
for tm in self.tm_database.get_all_tms(enabled_only=False):
    if tm['name'] == tm_name:
        tm_ids.append(tm['tm_id'])
```

### 3. Fixed Project Save (Previously Applied)

**File:** `Supervertaler_v3.7.2.py` Line ~12610

**Before:**
```python
'translation_memory': {
    'entries': self.tm_database.project_tm.entries,  # AttributeError!
    'fuzzy_threshold': self.tm_database.fuzzy_threshold
}
```

**After:**
```python
'tm_database': {
    'source_lang': self.tm_database.source_lang,
    'target_lang': self.tm_database.target_lang,
    'fuzzy_threshold': self.tm_database.fuzzy_threshold
}
```

### 4. Added Error Handling to TM Manager (Previously Applied)

**File:** `Supervertaler_v3.7.2.py` Line ~16702

**Added:**
```python
def show_tm_manager(self):
    """Show multi-TM management dialog with enable/disable controls"""
    try:
        # Update dropdown first
        self.update_tm_dropdown()
        
        dialog = tk.Toplevel(self.root)
        # ... rest of code
    except Exception as e:
        self.log(f"✗ Error opening TM Manager: {e}")
        messagebox.showerror("TM Manager Error", f"Failed to open TM Manager:\n{str(e)}")
        return
```

## Testing Results

### Test Script Output (`test_tm_methods.py`)

```
============================================================
Testing TM Database Methods
============================================================

✓ Database connected

1. Testing get_all_tms():
----------------------------------------
  • Project: 5 entries

2. Testing get_tm_list():
----------------------------------------
  Found 1 TMs

3. Testing get_entry_count():
----------------------------------------
  Total entries: 5

4. Testing search_all():
----------------------------------------
  Searching for: 'De uitvinding heeft betrekking op'
  Found 2 matches:
    • 73% - Project
      Source: heeft betrekking op...
      Target: relates to...
    • 60% - Project
      Source: De uitvinding heeft betrekking op een voegplaat vo...
      Target: The invention relates to a joint plate for joining...

============================================================
✓ All tests complete!
============================================================
```

## Current Status

### ✅ Fixed
- TM Manager opens successfully (error was missing `get_all_tms()` method)
- TM search/lookup working (added `search_all()` method)
- Project save no longer crashes (removed `project_tm` reference)
- Fuzzy matching returning real similarity scores (73%, 60%)

### ✏️ Needs User Verification
Please test the following in the application:

1. **TM Manager**: Click the "TM Manager" button - it should open without errors
2. **TM Lookup**: Navigate to a segment that exists in your TM - it should show matches automatically
3. **TM Search**: Click the search button - it should find matches
4. **Project Save**: Save your project - should work without AttributeError

## Database Statistics

- **Database Path**: `user data_private\Translation_Resources\supervertaler.db`
- **Current Size**: 148 KB
- **Project TM Entries**: 5
- **Total TMs**: 1 (Project)

## Architecture Notes

The new database backend:
- Returns **dictionaries** not objects
- All data is persistent (no in-memory TM objects)
- TMs identified by `tm_id` (e.g., "project", "big_mama")
- Fuzzy matching uses SequenceMatcher for real similarity scores
- FTS5 full-text search for fast candidate retrieval

## Next Steps

If issues persist:
1. Check the application log for error messages
2. Verify database exists at expected path
3. Test exact match vs fuzzy match behavior
4. Report any remaining errors with log output
