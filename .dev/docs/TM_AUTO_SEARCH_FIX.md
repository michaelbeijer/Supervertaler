# TM Auto-Search Fix

**Date**: 2025-10-10  
**Issue**: TM search not triggering automatically after segment selection  
**Status**: ✅ FIXED

## Problem

User reported that when navigating to a new segment in CAT mode, the TM search was not being triggered automatically after 2 seconds as expected.

## Root Cause

The `tm_auto_search_timer` variable was **never initialized** in the `__init__` method, causing an `AttributeError` when `schedule_auto_tm_search()` tried to check if a timer was already running.

```python
def schedule_auto_tm_search(self):
    # This line would fail if self.tm_auto_search_timer didn't exist:
    if self.tm_auto_search_timer is not None:
        self.root.after_cancel(self.tm_auto_search_timer)
```

Additionally, the `auto_search_tm()` method had an unnecessary panel visibility check that could block searches.

## Solution

### Fix 1: Initialize Timer Variable

**File**: `Supervertaler_v3.0.0-beta_CAT.py`  
**Line**: ~1478

Added timer initialization in the `__init__` method:

```python
# Translation memory - new multi-TM architecture
self.tm_database = TMDatabase()
self.tm_agent = TMAgent()
self.tm_agent.tm_database = self.tm_database
self.translation_memory: List[Dict[str, str]] = []
self.tm_auto_search_timer = None  # Timer for automatic TM search ← ADDED
```

### Fix 2: Simplify Auto-Search Logic

**File**: `Supervertaler_v3.0.0-beta_CAT.py`  
**Line**: ~3700

Removed panel visibility check that could block searches:

**Before:**
```python
def auto_search_tm(self):
    self.tm_auto_search_timer = None
    
    if not hasattr(self, 'current_segment') or not self.current_segment:
        return
    
    # Only auto-search if TM panel is visible and enabled
    if hasattr(self, 'panel_visibility') and self.panel_visibility.get('tm_matches', True):
        self.search_tm(auto_triggered=True)  # Could be blocked!
```

**After:**
```python
def auto_search_tm(self):
    self.tm_auto_search_timer = None
    
    if not hasattr(self, 'current_segment') or not self.current_segment:
        return
    
    # Trigger the search (auto_triggered flag prevents logging)
    self.search_tm(auto_triggered=True)  # Always searches
```

**Rationale**: Even if the TM panel is collapsed, the search should still run in the background so results are ready when user expands the panel.

## How It Works Now

1. **User selects segment** → `on_segment_select()` called
2. **Schedule search** → `schedule_auto_tm_search()` sets 2-second timer
3. **User navigates quickly** → Timer cancelled and reset on each segment change
4. **User stays on segment** → After 2 seconds, `auto_search_tm()` triggered
5. **Search executes** → `search_tm(auto_triggered=True)` runs silently
6. **Results displayed** → TM matches tree populated

## Testing

**Before fix:**
- ❌ Auto-search never triggered
- ❌ User had to click "🔍 Search" button manually

**After fix:**
- ✅ Auto-search triggers 2 seconds after segment selection
- ✅ Timer resets if user navigates to another segment
- ✅ Silent search (no log spam)
- ✅ Manual search still works via button

## Files Modified

- `Supervertaler_v3.0.0-beta_CAT.py` (2 changes)
  - Line ~1478: Added `self.tm_auto_search_timer = None`
  - Line ~3700: Simplified `auto_search_tm()` method

## Related Features

This fix completes the auto-search feature implemented in the TM improvements:

- ✅ Auto-search after 2-second delay
- ✅ Timer cancellation on navigation
- ✅ Silent search (no log messages)
- ✅ Works with new multi-TM architecture
- ✅ Shows TM source in results
