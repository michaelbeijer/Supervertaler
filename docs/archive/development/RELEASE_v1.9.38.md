# Supervertaler v1.9.38 Release Notes

**Release Date**: December 11, 2025  
**Type**: Quality of Life Improvements  
**Status**: Production Ready

---

## 🎯 Overview

Version 1.9.38 brings user experience improvements focused on project file readability and clearer guidance for batch translation workflows. This release also includes the font customization feature from v1.9.37.

---

## ✨ New Features

### **User-Configurable Grid Fonts** (v1.9.37)

Choose your preferred font for the translation grid from 10 popular options.

**Features**:
- ✅ Font family dropdown with 10 fonts: Calibri, Segoe UI, Arial, Consolas, Verdana, Times New Roman, Georgia, Courier New, Tahoma, Trebuchet MS
- ✅ Live preview panel showing source/target text with tag highlighting
- ✅ Font family now persists between sessions (previously only font size was saved)
- ✅ Fixed font size spinbox up/down arrows with improved styling and larger click targets

**Location**: Settings → View Settings → Grid Text Font

**Note**: If your favourite font is missing, contact the developer!

---

## 📁 Improvements

### **Reorganized .svproj File Structure**

Project files are now easier to inspect and edit in text editors.

**Before** (segments scattered throughout):
```
{
  "segments": [... huge array ...],
  "name": "My Project",
  "source_lang": "en",
  ...
}
```

**After** (logical ordering):
```
{
  "name": "My Project",
  "source_lang": "en",
  "target_lang": "nl",
  "created_date": "2025-12-11T10:30:00",
  "modified_date": "2025-12-11T14:45:00",
  "project_id": "abc123",
  
  "prompts": { ... },
  "prompt_folder": "...",
  "attached_tms": [ ... ],
  "attached_termbases": [ ... ],
  "spellcheck_enabled": true,
  
  "original_docx_path": "...",
  "memoq_source_path": "...",
  "sdlppx_source_path": "...",
  "phrase_source_path": "...",
  "cafetran_source_path": "...",
  
  "segments": [ ... now at the END ... ]
}
```

**Benefits**:
- All metadata visible at top of file without scrolling
- Project settings easy to review/edit
- Segments (bulk data) moved to end where it belongs
- Easier troubleshooting and manual inspection

---

### **Improved Batch Translate Warning**

Enhanced the warning dialog that appears when batch translating memoQ bilingual files with existing translations.

**Added Tip**:
> 💡 **Tip:** To clear all targets before batch translation, use the segment grid's right-click menu: Select All (Ctrl+A) → Clear Target. This avoids needing to re-import the file.

**Why This Helps**:
- Users previously thought they had to re-import the memoQ file to clear targets
- Now they know about the Select All + Clear Target shortcut
- Faster workflow for translators who need to redo translations

---

## 📋 Files Modified

| File | Changes |
|------|---------|
| `Supervertaler.py` | `Project.to_dict()` restructured, batch translate warning updated, font UI improvements |
| `CHANGELOG.md` | Added v1.9.37 and v1.9.38 entries |
| `README.md` | Updated version and feature highlights |
| `AGENTS.md` | Added development history entries |
| `docs/index.html` | Updated website version |

---

## 🔧 Technical Details

### Project.to_dict() Method

The serialization method now outputs keys in this order:
1. `name` - Project name
2. `source_lang`, `target_lang` - Language pair
3. `created_date`, `modified_date` - Timestamps
4. `project_id` - Unique identifier
5. All settings (prompts, TM, termbases, spellcheck)
6. All source paths (docx, memoq, trados, phrase, cafetran, txt)
7. `segments` - **Last** (the large array)

### Font Settings Storage

Settings stored in `user_data/ui_preferences.json`:
```json
{
  "grid_font_family": "Calibri",
  "grid_font_size": 11
}
```

---

## 🧪 Testing Checklist

- [x] Font family dropdown populates correctly
- [x] Font preview updates in real-time
- [x] Font settings persist after restart
- [x] .svproj files save with new key ordering
- [x] Existing .svproj files load correctly (backward compatible)
- [x] Batch translate warning shows new tip
- [x] Select All + Clear Target workflow works

---

## 📦 Build Information

**Build Date**: December 11, 2025  
**Build Tool**: PyInstaller  
**Executable Size**: ~84 MB  
**Output Location**: `dist/Supervertaler/Supervertaler.exe`

**Build Warnings** (expected, non-blocking):
- `tbb12.dll` - numba/threading dependency (Supermemory feature)
- torch DLL access violations - Whisper/voice dictation loading

---

## ⬆️ Upgrade Notes

**From v1.9.37 or earlier**:
- No breaking changes
- Existing projects load normally
- Font settings will default to "Segoe UI" on first load

**What Changes**:
- New .svproj files will have reorganized structure
- Existing .svproj files work as-is (no migration needed)

---

## 📌 Version History Context

| Version | Date | Focus |
|---------|------|-------|
| v1.9.38 | Dec 11, 2025 | Project file & UX improvements |
| v1.9.37 | Dec 11, 2025 | User-configurable grid fonts |
| v1.9.36 | Dec 10, 2025 | Universal tag coloring |
| v1.9.35 | Dec 10, 2025 | memoQ red tag color fix |
| v1.9.34 | Dec 10, 2025 | UI standardization |
| v1.9.33 | Dec 10, 2025 | Spellcheck update fix |
| v1.9.32 | Dec 10, 2025 | Trados SDLRPX status fix |

---

*Generated: December 11, 2025*
