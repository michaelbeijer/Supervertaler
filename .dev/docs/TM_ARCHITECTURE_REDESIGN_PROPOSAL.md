# TM Architecture Redesign Proposal - v3.0.0-beta

**Date:** October 10, 2025  
**Status:** 📋 PROPOSAL - Awaiting Approval

---

## Current Problems

### 1. **Language Code Mismatch**
**Issue:** TMX import uses GUI language names to guess codes:
```python
src_code = self.source_language[:2].lower()  # "English" -> "en"
tgt_code = self.target_language[:2].lower()  # "Dutch" -> "du" ❌
```

**Problem:** "Dutch"[:2] = "du", but TMX uses "nl"  
**Result:** All imports fail with 0 entries loaded

### 2. **No TM Management**
**Current Architecture:**
```python
self.tm_agent = TMAgent()
self.tm_agent.tm_data = {}  # Single flat dictionary
```

**Problems:**
- ✗ All TMX files merge into ONE tm_data dictionary
- ✗ Can't disable/enable specific TMs
- ✗ Can't see which TM a match came from
- ✗ No separation of Project vs Reference vs Custom TMs
- ✗ TM Manager just shows flat list of all entries mixed together

---

## Proposed Solution

### Architecture Overview

```python
class TMDatabase:
    def __init__(self):
        self.tms = {
            'project': TM(name='Project TM', enabled=True, read_only=False),
            'main': TM(name='Main TM', enabled=True, read_only=False),
            'reference': TM(name='Reference TM', enabled=False, read_only=True),
        }
        self.custom_tms = {}  # User-loaded TMX files
    
    def search(self, source_text, enabled_only=True):
        results = []
        for tm_id, tm in self.get_active_tms(enabled_only):
            matches = tm.fuzzy_search(source_text)
            for match in matches:
                match['tm_name'] = tm.name
                match['tm_id'] = tm_id
                results.append(match)
        return results

class TM:
    def __init__(self, name, enabled=True, read_only=False):
        self.name = name
        self.enabled = enabled
        self.read_only = read_only
        self.entries = {}  # source -> target
        self.metadata = {
            'source_lang': None,
            'target_lang': None,
            'file_path': None,
            'entry_count': 0,
            'created': None,
            'modified': None
        }
```

---

## Feature 1: Language Code Selector

### TMX Import Dialog Flow

**Step 1: Select File**
```
[File Browser] → Select "MyTM.tmx"
```

**Step 2: Language Code Dialog** (NEW)
```
┌─────────────────────────────────────────┐
│ Import TMX: MyTM.tmx                   │
├─────────────────────────────────────────┤
│                                         │
│ TMX Language Codes:                     │
│                                         │
│ Source Language Code: [en-US  ▼]        │
│   Common codes: en, en-US, en-GB        │
│                                         │
│ Target Language Code: [nl-NL  ▼]        │
│   Common codes: nl, nl-NL, nl-BE        │
│                                         │
│ ⓘ Check your TMX file to find the      │
│   exact language codes it uses          │
│                                         │
│ [Detect Automatically] [Cancel] [Import]│
└─────────────────────────────────────────┘
```

**Auto-Detect Feature:**
- Scans TMX file for all language codes
- Shows dropdown with detected codes
- User selects which pair to import

---

## Feature 2: Multi-TM Management

### TM Manager Redesign

**Current (Flat List):**
```
┌────────────────────────────────────────┐
│ Translation Memory: 5,234 entries      │
├────────────────────────────────────────┤
│ # │ Source          │ Target           │
│ 1 │ Hello           │ Hallo            │
│ 2 │ Goodbye         │ Tot ziens        │
│ 3 │ Thank you       │ Dank u           │
│   ...                                  │
└────────────────────────────────────────┘
```
❌ Can't tell which TM each entry belongs to

**Proposed (Multi-TM Manager):**
```
┌───────────────────────────────────────────────────────────┐
│ Translation Memory Manager                                │
├───────────────────────────────────────────────────────────┤
│ Connected TMs:                                            │
│                                                           │
│ ☑ Project TM            │ 145 entries │ en→nl │ [View]   │
│   └─ Current document translations                       │
│                                                           │
│ ☑ Main TM               │ 4,523 entries│ en→nl │ [View]   │
│   └─ C:\TMs\main_tm.tmx                                   │
│                                                           │
│ ☐ Reference TM          │ 25,641 entries│ en→nl │ [View] │
│   └─ C:\TMs\reference.tmx                                │
│                                                           │
│ ☑ KDE Glossary          │ 1,234 entries│ en→nl │ [View]  │
│   └─ C:\TMs\kde_v4.tmx                                    │
│                                                           │
│ [+ Add TM] [Remove Selected] [Import TMX] [Export TMX]    │
│                                                           │
│ Active TMs: 3 of 4 | Total Entries: 5,902                │
└───────────────────────────────────────────────────────────┘
```

✅ Clear TM organization  
✅ Enable/disable individual TMs  
✅ See entry counts  
✅ View individual TM contents  

---

## Feature 3: TM Search Updates

### Current TM Source Dropdown
```
TM Source: [Project TM  ▼]
           - Project TM
           - Main TM
           - Reference TM
           - All TMs
           - Custom TM
```

### Proposed Dynamic Dropdown
```
TM Source: [All Active TMs ▼]
           - All Active TMs (3)        ← Searches only enabled TMs
           - All TMs (4)               ← Searches all, even disabled
           ─────────────────
           - Project TM (145)          ← Individual TMs
           - Main TM (4,523)
           - KDE Glossary (1,234)
           ─────────────────
           - Reference TM (25,641) [DISABLED]
```

### Search Results Show TM Origin
```
┌──────────────────────────────────────────┐
│ TM Matches for Current Segment           │
├──────────────────────────────────────────┤
│ Match │ Translation    │ TM Source       │
├──────────────────────────────────────────┤
│ 100%  │ Exact match   │ Project TM      │
│  95%  │ Similar match │ Main TM         │
│  87%  │ Fuzzy match   │ KDE Glossary    │
└──────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Core Architecture (1-2 hours)
1. Create `TMDatabase` class
2. Create `TM` class with metadata
3. Migrate existing `TMAgent` to use new structure
4. Update save/load project format

### Phase 2: Language Code Selector (30 mins)
1. Create language code selection dialog
2. Add auto-detect feature (scan TMX for language codes)
3. Update TMX import to use selected codes

### Phase 3: TM Manager UI (1 hour)
1. Redesign TM Manager dialog
2. Show all TMs with checkboxes
3. Add/Remove TM functionality
4. View individual TM contents

### Phase 4: Search Integration (30 mins)
1. Update TM search to query selected TMs
2. Add TM source column to results
3. Dynamic dropdown population

### Total Estimated Time: **3-4 hours**

---

## Data Structures

### Project File Format (Updated)
```json
{
  "segments": [...],
  "tm_database": {
    "project_tm": {
      "name": "Project TM",
      "enabled": true,
      "read_only": false,
      "entries": {"Hello": "Hallo", ...},
      "metadata": {
        "source_lang": "en",
        "target_lang": "nl",
        "entry_count": 145
      }
    },
    "custom_tms": {
      "kde_glossary": {
        "name": "KDE Glossary",
        "enabled": true,
        "read_only": false,
        "file_path": "C:\\TMs\\kde_v4.tmx",
        "entries": {...},
        "metadata": {...}
      }
    }
  }
}
```

---

## User Workflows

### Import TMX File
1. Click "Add TM" or "Import TMX" in TM Manager
2. Select TMX file
3. **Language Code Dialog appears:**
   - Shows detected language codes in TMX
   - User selects source and target codes
   - Or clicks "Detect Automatically"
4. TMX loads into new custom TM
5. TM appears in TM Manager list (enabled by default)
6. Immediately available for searches

### Manage TMs
1. Open TM Manager
2. See all connected TMs with entry counts
3. Check/uncheck to enable/disable
4. Click "View" to see TM contents
5. Select and "Remove" to disconnect TM
6. Changes apply immediately to searches

### Search with Multiple TMs
1. Select segment
2. Auto-search queries all enabled TMs
3. Results show which TM each match came from
4. Can change TM Source dropdown to search specific TM
5. Disable TMs in manager to exclude from searches

---

## Backwards Compatibility

### Migrating Old Projects
```python
def migrate_old_tm_format(old_data):
    if 'tm_data' in old_data:  # Old format
        # Convert single tm_data dict to new multi-TM structure
        new_format = {
            'project_tm': {
                'name': 'Imported TM',
                'enabled': True,
                'entries': old_data['tm_data'],
                'metadata': {...}
            }
        }
        return new_format
    return old_data  # Already new format
```

---

## Benefits

### For Users
✅ **Clarity:** See exactly which TMs are connected  
✅ **Control:** Enable/disable TMs per project  
✅ **Transparency:** Know which TM provided each match  
✅ **Flexibility:** Mix project, reference, and custom TMs  

### For Translators
✅ **Professional:** Matches industry-standard CAT tools  
✅ **Organized:** Separate client TMs, reference TMs, personal TMs  
✅ **Efficient:** Disable irrelevant TMs for cleaner matches  

### For Power Users
✅ **Scalable:** Support unlimited custom TMs  
✅ **Portable:** TM files can be shared/moved  
✅ **Maintainable:** Each TM is independent  

---

## Questions for User

1. **Should Project TM auto-save with project?**  
   ✓ Yes (recommended)  
   ✗ No, manual save only

2. **Default TMs to create:**  
   ✓ Project TM (always)  
   ✓ Main TM (optional persistent TM across all projects)  
   ? Reference TM (read-only, optional)

3. **TM file storage:**  
   Option A: Store TM data in project JSON  
   Option B: Reference external TMX files  
   Option C: Both (embed small TMs, reference large ones)

4. **Import behavior:**  
   Option A: Always create new TM for each import  
   Option B: Offer to merge into existing TM  
   Option C: Ask user each time

---

## Next Steps

**If approved:**
1. Implement Phase 1 (Core Architecture)
2. Test with existing projects
3. Implement Phase 2 (Language Code Selector)
4. Test TMX import with various language codes
5. Implement Phase 3 (TM Manager UI)
6. Implement Phase 4 (Search Integration)
7. Full testing
8. Documentation update

**Estimated completion:** Same session (3-4 hours of work)

---

**Ready to proceed?** Let me know if you want me to implement this, or if you'd like any changes to the design first.
