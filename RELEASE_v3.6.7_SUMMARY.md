# Release v3.6.7-beta Summary
**Date**: October 18, 2025  
**Commit**: f702a95  
**Status**: ✅ Released and pushed to GitHub

---

## 🎯 What's New in v3.6.7

### ✨ UI Polish & Enhancements

1. **Reduced Tab Height**
   - Changed padding from [12, 8] → [12, 4]
   - Better screen density and cleaner look
   - More content visible without scrolling

2. **Removed Obsolete Maximize View**
   - Deleted maximize_prompt_library() function
   - Cleaned ~725 lines of orphaned code
   - Simplified codebase

3. **Better Button Naming**
   - "Show Prompt" → "📝 View/Edit Analysis Prompts"
   - Clearer purpose and functionality

4. **Clickable Folder Links**
   - System_prompts folder link opens File Explorer
   - Custom_instructions folder link opens File Explorer
   - Cross-platform support (Windows/macOS/Linux)
   - Translators can easily locate their prompt files

5. **Website Enhancements**
   - **NEW About Section**: Beautiful gradient purple design
   - Three story cards: Where It Started, Where It's Going, What Makes It Different
   - Vision dialogue showcasing future AI assistant
   - Responsive design with backdrop-filter blur effects

### 🐛 Bug Fixes

1. **Translation Error Fixed**
   - **Issue**: `'Supervertaler' object has no attribute 'custom_instructions_text'`
   - **Cause**: Translation code looking for old text widget instead of Prompt Manager
   - **Fix**: Updated batch_translate_all(), translate_segment(), preview_combined_prompt()
   - **Result**: Translations work perfectly with activated custom instructions

2. **System Prompts Display Fixed**
   - **Issue**: Saved prompts not appearing in Prompt Manager
   - **Cause**: JSON `name` field using `default_name` instead of user input
   - **Fix**: Store user_entered_name in JSON metadata
   - **Result**: All saved prompts appear immediately

---

## 📦 Files Updated

### Core Application
- ✅ `Supervertaler_v3.6.6-beta_CAT.py` → `Supervertaler_v3.6.7-beta_CAT.py` (renamed)
- ✅ Version references updated throughout (window title, log messages, splash screen)

### Documentation
- ✅ `README.md` - Updated version, features list, and recommendations
- ✅ `CHANGELOG.md` - Added v3.6.7 entry with full details
- ✅ `docs/guides/PROMPT_ASSISTANT_USER_GUIDE.md` - Updated version reference
- ✅ `docs/guides/AI_PROMPT_ASSISTANT_USER_GUIDE.md` - Updated version reference

### Website
- ✅ `docs/index.html` - Updated version badge, download link, feature badges
- ✅ About section already added (previous commits)

### Modules
- ✅ `modules/prompt_library.py` - Added `import re` for future Markdown support

---

## 🚀 What's Next (Planned for v3.6.8)

### Markdown Format Support (Saved for Tomorrow)
We've created comprehensive examples comparing three formats:

**Format Examples Created**:
- ✅ `user data_private/System_prompts/format_examples/STAR7_Ipsos.yaml`
- ✅ `user data_private/System_prompts/format_examples/STAR7_Ipsos.toml`
- ✅ `user data_private/System_prompts/format_examples/STAR7_Ipsos.md` ⭐ **USER CHOICE**
- ✅ `user data_private/Custom_instructions/format_examples/STAR7_Ipsos.yaml`
- ✅ `user data_private/Custom_instructions/format_examples/STAR7_Ipsos.toml`
- ✅ `user data_private/Custom_instructions/format_examples/STAR7_Ipsos.md` ⭐ **USER CHOICE**

**User Decision**: Markdown format chosen for best readability! ✨

**Implementation Plan** (Tomorrow):
1. Add Markdown parsing with YAML frontmatter to `prompt_library.py`
2. Update save functions to default to `.md` format
3. Update file dialogs to show both `.json` and `.md` files
4. No backward compatibility needed - convert all existing JSON to MD
5. Create conversion utility to migrate existing prompts

**Benefits**:
- Translators can double-click prompts and read them like documents
- Native Markdown tables for glossaries (beautiful formatting!)
- Section headers and structure
- Human-friendly editing
- No escaped quotes or verbose JSON syntax

---

## 📊 Statistics

- **Lines Changed**: 16,628 insertions, 16 deletions
- **Files Changed**: 8 files
- **Code Cleanup**: ~725 lines removed (maximize view)
- **Bug Fixes**: 2 critical issues resolved
- **UI Improvements**: 4 major enhancements
- **Website**: 1 new section added

---

## ✅ Verification

- ✅ Version bumped from 3.6.6 → 3.6.7
- ✅ All documentation updated
- ✅ Website updated with new download link
- ✅ Commit created with detailed message
- ✅ Pushed to GitHub successfully
- ✅ Branch: `main` - up to date with origin/main

---

## 🎉 Release Highlights

This release focuses on **polish and stability**:
- Cleaner UI with reduced tab height
- More intuitive button names
- Direct folder access for translators
- Fixed critical translation bugs
- Enhanced website storytelling
- Prepared groundwork for Markdown format migration

**User Impact**: Better usability, fewer errors, clearer workflows. The application is now more polished and professional, ready for the upcoming Markdown format feature.

---

**Next Session**: Implement Markdown format support based on user's chosen format! 🚀
