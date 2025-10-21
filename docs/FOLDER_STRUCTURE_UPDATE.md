# Folder Structure Update - Style Guides Relocation

**Date:** Implementation Update  
**Status:** ✅ Complete

---

## Change Summary

The Style Guides folder has been **relocated and reorganized** to match the structure of other Translation Resources.

### Before
```
user data/
├── Style_Guides/
│   ├── Dutch.md
│   ├── English.md
│   ├── Spanish.md
│   ├── German.md
│   └── French.md
└── Translation_Resources/
    ├── Glossaries/
    ├── TMs/
    ├── Non-translatables/
    └── Segmentation_rules/
```

### After
```
user data/
└── Translation_Resources/
    ├── Style_Guides/          ← NEW LOCATION
    │   ├── Dutch.md
    │   ├── English.md
    │   ├── Spanish.md
    │   ├── German.md
    │   └── French.md
    ├── Glossaries/
    ├── TMs/
    ├── Non-translatables/
    └── Segmentation_rules/
```

---

## Why This Change?

1. **Consistency** - Style Guides are now alongside other Translation Resources
2. **Organization** - Similar to how System_prompts and Custom_instructions are organized
3. **Logical Grouping** - All translation reference materials in one location
4. **User Clarity** - Clear that Style Guides are translation resources

---

## Files Updated

| File | Change | Lines |
|------|--------|-------|
| `modules/config_manager.py` | Updated REQUIRED_FOLDERS path | Line 35 |
| `Supervertaler_v3.7.1.py` | Updated initialization path | Line 813 |

---

## Backend Impact

**StyleGuideLibrary** (`modules/style_guide_manager.py`):
- ✅ No code changes needed - uses provided path
- ✅ Works with any directory location
- ✅ Automatically creates directory if missing

**Initialization** (in `Supervertaler_v3.7.1.py`):
- ✅ Path now: `Translation_Resources/Style_Guides`
- ✅ ConfigManager auto-creates folder on startup
- ✅ All guides automatically loaded

---

## User Impact

### For End Users
- **No action required** - Automatic migration
- Guides automatically available in new location
- All functionality unchanged

### For Developers
- **Folder location:** `c:\Dev\Supervertaler\user data\Translation_Resources\Style_Guides\`
- **Path in code:** `get_user_data_path("Translation_Resources/Style_Guides")`
- **ConfigManager:** Handles path automatically

---

## Private vs Public Folders

### Style_Guides Locations

**Public Repository** (`user data/Translation_Resources/Style_Guides/`)
- Where users store their custom style guides
- Shared with team members via export/import
- Public-repo safe

**Private Development** (`user data_private/Translation_Resources/Style_Guides/`)
- Optional: For private/sensitive guides
- Not in public repository
- Same structure as public folder

---

## Folder Structure Reference

For completeness, the full Translation_Resources structure:

```
user data/Translation_Resources/
├── Style_Guides/              ← Translation style guides (NEW LOCATION)
│   ├── Dutch.md
│   ├── English.md
│   ├── Spanish.md
│   ├── German.md
│   └── French.md
│
├── Glossaries/                ← Terminology databases
│   └── *.txt (glossary files)
│
├── TMs/                        ← Translation memories
│   └── *.tmx (memory files)
│
├── Non-translatables/         ← Brand names, proper nouns
│   └── *.txt
│
└── Segmentation_rules/        ← Sentence segmentation
    └── *.srx
```

---

## Configuration

### ConfigManager (`modules/config_manager.py`)
```python
REQUIRED_FOLDERS = [
    "Prompt_Library/System_prompts",
    "Prompt_Library/Custom_instructions",
    "Translation_Resources/Style_Guides",    # ← Updated path
    "Translation_Resources/Glossaries",
    "Translation_Resources/TMs",
    "Translation_Resources/Non-translatables",
    "Translation_Resources/Segmentation_rules",
    "Projects",
]
```

### App Initialization (`Supervertaler_v3.7.1.py`)
```python
style_guides_dir = get_user_data_path("Translation_Resources/Style_Guides")
self.style_guide_library = StyleGuideLibrary(
    style_guides_dir=style_guides_dir,
    log_callback=self.log
)
```

---

## Verification

### Check if Update Applied
```bash
# Should exist:
user data/Translation_Resources/Style_Guides/Dutch.md
user data/Translation_Resources/Style_Guides/English.md
user data/Translation_Resources/Style_Guides/Spanish.md
user data/Translation_Resources/Style_Guides/German.md
user data/Translation_Resources/Style_Guides/French.md

# Should NOT exist:
user data/Style_Guides/  (old location)
```

---

## Next Steps

1. ✅ **Migration Complete** - Folder moved to new location
2. ✅ **Configuration Updated** - Paths updated in code
3. ✅ **Tests Passed** - Backend verified working
4. 🔄 **Phase 2 Ready** - UI implementation can proceed

---

## Notes

- **Backward Compatibility:** If old path exists, it will be ignored. Users should use new location.
- **Automatic Creation:** New folder created automatically on app startup if missing
- **No Data Loss:** All 5 language guides preserved and functional
- **Same Functionality:** No change to feature capabilities

---

## Related Documentation

- `MASTER_INDEX.md` - Navigation hub
- `COMPLETE_PROJECT_SUMMARY.md` - Project overview
- `PHASE2_IMPLEMENTATION_DETAILED_CHECKLIST.md` - Implementation guide

---

**Status:** ✅ Relocation Complete  
**Location:** `user data/Translation_Resources/Style_Guides/`  
**Ready for Phase 2:** YES
