# Termbase Ranking System - Bug Fixes

## Date: November 19, 2025

## Issues Reported by User

1. ❌ **Rankings not showing in termbase table** - Only dashes visible in Ranking column
2. ❌ **No way to change termbase type or ranking** - Missing UI controls  
3. ❌ **Activate/deactivate checkboxes not working** - No visible effect when toggling
4. ❌ **Project termbase terms not showing uniform light pink** - Inconsistent colors
5. ❌ **Confusing blue shades** - Unknown what different blues mean

## Root Causes Identified

### 1. **Critical Bug: Using OLD priority system instead of NEW ranking system**

The highlighting code was using the `priority` field (1-99, stored in individual terms) instead of the `ranking` field (1, 2, 3..., stored in termbases table). This caused:
- Inconsistent colors (multiple terms from same termbase showing different shades)
- Confusing blue variations
- Project termbases not showing uniform pink

### 2. **Missing debug logging**

No visibility into whether:
- Rankings were being assigned in database
- Checkboxes were triggering activate/deactivate
- Database queries were returning correct data

## Fixes Applied

### Fix #1: Use Ranking Instead of Priority for Highlighting

**File: `Supervertaler.py`**

Changed `highlight_termbase_matches()` (line ~465-490) to:
1. Extract `ranking` from match_info instead of `priority`
2. Use distinct blue shades based on ranking:
   - **Ranking #1**: Dark blue `RGB(0, 100, 255)`
   - **Ranking #2**: Medium blue `RGB(0, 150, 255)` 
   - **Ranking #3**: Light blue `RGB(0, 200, 255)`
   - **Ranking #4+**: Very light blue `RGB(100, 220, 255)`
3. Project termbases always use: Light pink `RGB(255, 182, 193)` = `#FFB6C1`

### Fix #2: Pass Ranking Through Data Flow

**File: `Supervertaler.py`**

Modified `find_termbase_matches_in_source()` (line ~13460-13510) to:
1. Extract `ranking` from database results: `ranking = result.get('ranking', None)`
2. Include ranking in matches dict: `'ranking': ranking`
3. Add ranking to debug logs: `ranking_info = f" ranking=#{ranking}"`

### Fix #3: Comprehensive Debug Logging

**File: `modules/termbase_manager.py`**

Added debug logging to:

**`activate_termbase()`**:
```python
self.log(f"🔵 ACTIVATE: termbase_id={termbase_id}, project_id={project_id}")
self.log(f"  ✓ Inserted activation record")
# ... after reassign_rankings ...
self.log(f"  ✓ Termbase {termbase_id} now has ranking: {ranking}")
```

**`deactivate_termbase()`**:
```python
self.log(f"🔴 DEACTIVATE: termbase_id={termbase_id}, project_id={project_id}")
self.log(f"  ✓ Inserted deactivation record")
self.log(f"  ✓ Cleared ranking for termbase {termbase_id}")
```

**File: `Supervertaler.py`**

Added debug logging to `refresh_termbase_list()` (line ~4750-4770):
```python
self.log(f"  Termbase '{tb['name']}' (ID {tb['id']}): Project termbase (no ranking)")
self.log(f"  Termbase '{tb['name']}' (ID {tb['id']}): Ranking #{ranking}")
self.log(f"  Termbase '{tb['name']}' (ID {tb['id']}): No ranking (inactive or not assigned)")
```

## Testing Instructions

### Test 1: Verify Rankings are Assigned

1. Open your project
2. Go to **Termbases** tab
3. **Check/uncheck** several termbases
4. **Watch the Session Log** for these messages:
   ```
   🔵 ACTIVATE: termbase_id=X, project_id=Y
     ✓ Inserted activation record
     ✓ Assigned ranking #1 to termbase ID X
     ✓ Termbase X now has ranking: 1
   ```
5. Look at the **Ranking column** in table - should show:
   - First activated termbase: `#1`
   - Second activated termbase: `#2`
   - Third activated termbase: `#3`
   - Deactivated termbases: `—` (dash)
   - Project termbases: `—` (dash with tooltip "Project termbases don't use ranking")

### Test 2: Verify Highlighting Colors

1. Open a segment with termbase matches
2. Check **Source column** for highlighted terms:
   - **Project termbase** terms → **Light pink** `#FFB6C1` (uniform across all terms)
   - **Ranking #1** terms → **Dark blue** `RGB(0,100,255)`
   - **Ranking #2** terms → **Medium blue** `RGB(0,150,255)`
   - **Ranking #3** terms → **Light blue** `RGB(0,200,255)`
   - **Ranking #4+** terms → **Very light blue** `RGB(100,220,255)`

3. Check Session Log for:
   ```
   🔍 Searching termbases for: 'your text'
     → term = translation (priority: 50 ranking=#1)
     → term2 = translation2 (priority: 30 ranking=#2)
   ```

### Test 3: Verify Checkbox Behavior

1. **Uncheck** an active termbase
2. Session Log should show:
   ```
   🔴 DEACTIVATE: termbase_id=X, project_id=Y
     ✓ Inserted deactivation record
     ✓ Cleared ranking for termbase X
     ✓ Assigned ranking #1 to termbase ID ...
   ✓ Deactivated termbase X for project Y
   ```
3. Table should **refresh automatically**
4. Rankings should **shift down** (e.g., #2 becomes #1)

### Test 4: Verify Type Changing

The UI already has **Set/Unset buttons** for changing termbase type:
- For **project termbases**: `✕` button to remove designation
- For **background termbases** (that belong to current project): `Set` button to make it project termbase

1. Find a termbase that shows **"Background"** with a **Set** button
2. Click **Set**
3. It should change to **"📌 Project"** (pink text) with `✕` button
4. Ranking should disappear (project termbases don't use ranking)

## Expected Behavior After Fixes

### Ranking Column Display

| Termbase Type | Active? | Ranking Column Shows | Color in Grid |
|--------------|---------|---------------------|---------------|
| Project TB | ✓ | `—` (dash) | Light pink #FFB6C1 |
| Background TB | ✓ (1st) | `#1` | Dark blue |
| Background TB | ✓ (2nd) | `#2` | Medium blue |
| Background TB | ✓ (3rd) | `#3` | Light blue |
| Background TB | ✓ (4th+) | `#4`, `#5`... | Very light blue |
| Any TB | ✗ (inactive) | `—` (dash) | No highlighting |

### Tooltips

- **Project termbase ranking dash**: "Project termbases don't use ranking (always highlighted pink)"
- **Inactive termbase ranking dash**: "No ranking - termbase not activated for current project"
- **Ranking #1, #2, #3...**: "Priority ranking #X (lower = higher priority)"

## What to Look For

### ✅ **Success indicators:**
1. Rankings appear in table when termbases are activated
2. Rankings update automatically when you check/uncheck
3. All project termbase terms show **uniform light pink**
4. Different rankings show **distinct blue shades**
5. Session Log shows detailed activation/deactivation messages

### ❌ **Problem indicators:**
1. Ranking column still shows only dashes
2. Checkboxes don't trigger any log messages
3. Colors are still inconsistent or wrong
4. No debug messages appear in Session Log

## Troubleshooting

If rankings still don't appear:

1. **Check Session Log** - Do you see:
   - `🔵 ACTIVATE:` messages when checking boxes?
   - `✓ Assigned ranking #X to termbase ID Y` messages?
   - Any error messages with red ✗?

2. **Check project_id** - Session Log should show:
   ```
   ✓ Current project: Your Project Name
   ```
   If project_id is missing/None, rankings won't be assigned.

3. **Database schema** - Verify `termbases` table has `ranking` column:
   ```sql
   SELECT id, name, ranking FROM termbases;
   ```

4. **Clear cache** - Close and reopen project to force fresh data load

## Known Limitations

1. **Rankings are project-specific** - Different projects can have different rankings for the same termbases
2. **Rankings auto-assign sequentially** - You cannot manually set ranking numbers (they're assigned based on activation order)
3. **Project termbases don't use ranking** - They always show pink, regardless of other termbases
4. **Only activated termbases get colors** - Inactive termbases don't highlight terms

## Summary

The core issue was that highlighting was using the OLD `priority` field (per-term, 1-99) instead of the NEW `ranking` field (per-termbase, 1, 2, 3...). This caused:
- Multiple shades for same termbase
- No uniform pink for project termbases
- Confusing color meanings

**Now fixed:** Each termbase gets ONE color based on its ranking, all terms from that termbase show the same color.
