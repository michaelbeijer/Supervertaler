# Supervertaler CAT Edition - Changelog

**Version Line**: v3.x.x-beta (Segment-based CAT Editor Architecture)

---

## [3.1.1-beta] - 2025-10-11 🔧 INFRASTRUCTURE UPDATE & BUG FIXES

> **📌 Version Bump**: Infrastructure update for parallel folder structure and critical bug fixes

### 🗂️ INFRASTRUCTURE CHANGES

**Parallel Folder Structure** - Complete architectural change for dev mode

- **NEW: Dual Directory Trees**:
  ```
  user data/          (public, Git-tracked, for end users)
  user data_private/  (private, Git-ignored, for developers)
  ```
  
- **Feature Flag System**:
  - Presence of `.supervertaler.local` file enables dev mode
  - Auto-routing: All save/load operations automatically use correct tree
  - No UI clutter: Removed all public/private checkboxes and labels
  - Developers create `.supervertaler.local` manually (not synced to Git)

- **Path Resolution**:
  - `get_user_data_path(folder_name)` returns appropriate root based on dev mode
  - Dev mode: `user data_private/System_prompts/`
  - User mode: `user data/System_prompts/`
  - All folders auto-route: System_prompts, Custom_instructions, Projects, TMs, Glossaries, etc.

- **Git Safety**:
  - `.gitignore` simplified: Single line `user data_private/` excludes all private data
  - Developers can work freely without accidentally committing private content
  - Users never see private feature options

### 🐛 BUG FIXES

**CAT Version (v3.1.0-beta → v3.1.1-beta)**:

- **FIXED**: Prompt Library not loading prompts in dev mode
  - Root cause: `self.system_prompts_dir` was hardcoded instead of using `get_user_data_path()`
  - Impact: PromptLibrary was looking in wrong directory when dev mode active
  - Solution: Updated initialization to use path resolver
  
- **FIXED**: UI still showing "📁 Public 🔒 Private" labels
  - Removed from Prompt Library header
  - Cleaned up all `_is_private` metadata references
  - UI now shows only "System prompts" and "Custom instructions" (UK English style)

- **FIXED**: Emoji rendering corruption
  - Filter button: `�` → 🔍 (magnifying glass, `\U0001F50D`)
  - Load Example Template button: `�` → 📋 (clipboard, `\U0001F4CB`)
  - Prompt tree icons: `�` → 📝 (memo, `\U0001F4DD`)
  - Solution: Used Unicode escape codes for reliable cross-platform rendering

### 🎨 UI/UX IMPROVEMENTS

- **UK English Style**: Changed all UI labels to lowercase
  - "System Prompts" → "System prompts"
  - "Custom Instructions" → "Custom instructions"
  - Location column: "System" → "System prompts", "Custom" → "Custom instructions"
  
- **Cleaner Prompt Editor**:
  - Removed private checkbox (no longer needed with auto-routing)
  - Added dev mode banner: "🔒 DEV MODE: All prompts auto-save to private folders"
  - Type dropdown shows user-friendly names with emojis

- **Dev Mode Banner**:
  - Red "🔒 DEV MODE" indicator when `.supervertaler.local` present
  - Clear visual confirmation that private mode is active

### 📝 BACKEND CHANGES

- **Removed Legacy Code**:
  - Eliminated `is_private` parameters from all PromptLibrary methods
  - Removed `_is_private` metadata from prompt JSON files
  - Cleaned up `prompt_private_var` and `project_private_var` checkbox code
  
- **Simplified Git Ignore**:
  - Old: 7 individual patterns (System_prompts_private, Custom_instructions_private, etc.)
  - New: 1 pattern (`user data_private/`) covers all private data

### 🔧 COMPATIBILITY

- **Both Versions Updated**: v2.4.4-CLASSIC and v3.1.1-beta use identical folder structure
- **Backward Compatible**: Existing prompts/projects automatically work
- **Migration**: Old `*_private` folders can be manually moved to new structure

---

## [3.1.0-beta] - 2025-10-10 🎯 PROMPT LIBRARY UPDATE

> **📌 Version Bump**: Bumped from v3.0.0-beta to v3.1.0-beta to reflect significant new feature and architectural change in prompt management system.

### ✨ NEW FEATURES

#### Unified Prompt Library
**Comprehensive prompt management system with two distinct prompt types!**

- **NEW: Custom Instructions** - User preferences and behavioral guidelines
  - Define HOW the AI should translate (tone, style, formatting preferences)
  - Examples: "Professional Tone", "Preserve Formatting", "Prefer TM Matches"
  - Separate from System Prompts (which define WHO the AI is)
  
- **NEW: Dual Prompt Type System**:
  - **🎭 System Prompts**: Define AI role/expertise (e.g., "Legal Specialist")
  - **📝 Custom Instructions**: Define user preferences/context (e.g., "Formal Tone")
  - Can combine both types for powerful, personalized workflows

- **NEW: Type Filtering**:
  - Radio buttons: All / System Prompts / Custom Instructions
  - Quick filtering in tree view
  - Sortable Type column

- **NEW: Dedicated "Prompt Library" Menu**:
  - Menu → Prompt Library → Open Prompt Library (Ctrl+P)
  - Menu → Prompt Library → System Prompts (filtered view)
  - Menu → Prompt Library → Custom Instructions (filtered view)
  - Keyboard shortcut: **Ctrl+P** for quick access

### 🗂️ FOLDER STRUCTURE CHANGES

**BREAKING CHANGE**: Unified folder structure across v2 and v3

- **New Structure**:
  ```
  user data/
  ├── System_prompts/          (public, Git-tracked)
  ├── System_prompts_private/  (private, Git-ignored)
  ├── Custom_instructions/     (public, Git-tracked)
  └── Custom_instructions_private/ (private, Git-ignored)
  ```

- **OLD v3 Structure** (deprecated):
  - ~~`custom_prompts/`~~ → `user data/System_prompts/`
  - ~~`custom_prompts_private/`~~ → `user data/System_prompts_private/`

### 🎨 UI/UX IMPROVEMENTS

- **Renamed**: "System Prompt Library" → "Prompt Library"
- **Button labels**: "Browse Prompts" → "Prompt Library"
- **Dialog title**: "🎯 Prompt Library - System Prompts & Custom Instructions"
- **Added Type dropdown** in prompt editor (create/edit)
- **Dynamic privacy label** updates based on selected type
- **Tree view enhancements**: Added Type column with icons

### 📦 EXAMPLE FILES

**3 Example Custom Instructions included**:
1. **Professional Tone & Style** - Ensures formal business language
2. **Preserve Formatting & Layout** - Maintains document structure
3. **Prefer Translation Memory Matches** - Prioritizes TM consistency

---

## [3.0.0-beta] - 2025-10-09 🚀 MAJOR RELEASE (CAT Editor)

> **📌 Version Renumbering**: This version was previously numbered v2.5.2. The jump to v3.0 reflects a **major architectural change** - a complete rewrite from the original DOCX workflow (v2.x-CLASSIC) to a segment-based CAT editor.

### ⚡ PERFORMANCE IMPROVEMENTS

#### Grid View Pagination System
**Major performance boost for large documents!**

- **NEW: Smart pagination** - Load only 50-100 segments at a time instead of all
- **Page size options**: 25, 50, 100, 200, or "All" segments per page
- **Navigation controls**: ⏮ First / ◀ Prev / Next ▶ / Last ⏭ buttons
- **Performance gain**: Grid view loads in ~0.5 seconds instead of 6-7 seconds
- **Benefits**:
  - ✅ 10x faster grid view loading
  - ✅ Eliminates freezing on view switches
  - ✅ Professional CAT tool behavior (like memoQ, Trados)

#### Smart Paragraph Detection
**Intelligent document structure recognition!**

- **NEW: Paragraph grouping** - Automatically detects paragraph boundaries from imports
- **Smart heuristics**: Detects headings, groups related sentences, identifies natural breaks
- **Document view improvements**: Headings properly separated, sentences flow naturally

### 🛡️ STABILITY IMPROVEMENTS

- **Enhanced loading protection** - Full-screen blocker prevents interaction during grid loading
- **Visual feedback** - "Loading page... Please wait." overlay
- **Prevents crashes** - Eliminates window resize/freeze issues

---

For older versions and detailed technical history, see: `CHANGELOG_full_backup.md`

**Last updated**: October 11, 2025
