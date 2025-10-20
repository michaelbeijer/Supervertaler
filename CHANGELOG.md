# Supervertaler - Complete Changelog

**Latest Version**: v3.7.1 (2025-10-20)  
**Product**: Unified Supervertaler (v3.x CAT Edition)  
**Status**: Active Development

> As of v3.7.1, Supervertaler is a unified product focusing exclusively on the CAT (Computer-Aided Translation) editor experience. The previous Classic Edition (v2.x) is archived for reference but no longer actively developed.

---

## [3.7.1] - 2025-10-20 🔐 SECURITY & CONFIGURATION UPDATE

### 🔐 CRITICAL SECURITY UPDATES

**Data Privacy & API Keys Security**:
- **🛡️ Removed sensitive data from git history** - `recent_projects.json` containing client project names completely removed from all 364 commits using git filter-branch
- **🔑 API Keys Protection** - Moved `api_keys.txt` to user data folder, never committed to git
- **v3.7.1 Yanked** - Removed from PyPI and GitHub releases due to security review (users should upgrade to v3.7.1)
- **Dev/User Mode Separation** - Separate configuration paths for development vs. user environments

**User Data Folder System** (NEW):
- **First-Launch SetupWizard**: Users select where to store their data (Windows: `Documents/Supervertaler_Data/`, etc.)
- **Configurable Location**: New "Change Data Folder" option in Settings menu
- **Automatic Setup**: `api_keys.txt` created from template on first launch
- **Migration Support**: Existing users' keys automatically migrated to new location
- **Configuration Stored**: User path saved to `~/.supervertaler_config.json`

**Code Quality**:
- 🐛 **Fixed Tkinter Error** - Corrected paned window widget management in Prompt Library tab switching
- ✅ **Enhanced Error Handling** - Try-catch blocks for TclError in tab switching
- ✅ **Improved UX** - SetupWizard now shows confirmation dialog with exact folder structure before creation

**Files Modified**:
- `Supervertaler_v3.7.1.py` - Updated tab switching logic, user data folder routing
- `modules/config_manager.py` - Dev/user mode detection, api_keys handling
- `modules/setup_wizard.py` - Enhanced first-launch experience
- Documentation - Updated README with new user data folder structure

**Migration Guide**:
- **Existing Users (v3.7.1)**: Simply upgrade - SetupWizard will guide you on first launch
- **New Users (v3.7.1)**: SetupWizard appears on first launch, guide you through setup
- **API Keys**: Will be copied to your chosen data folder automatically
- **Custom Prompts**: Already in `user data/Prompt_Library/` - can be moved to new location via Settings

### ✨ USER EXPERIENCE IMPROVEMENTS

**First-Launch Flow**:
1. App detects missing user data folder configuration
2. Welcome dialog explains what will be created
3. Folder selection dialog with clear examples
4. Confirmation dialog shows exact folder structure
5. Success message lists all created files/folders
6. Application launches with full functionality

**Settings Menu Enhancement**:
- New "Data Folder" section showing current path
- "Change Data Folder" button for mid-session changes
- Optional data migration when changing paths
- Clear feedback on what was moved

---

## [3.7.0] - 2025-10-19 🎯 STABLE RELEASE

### ✨ MAJOR RESTRUCTURING

**Product Unification**:
- **Deprecated**: v3.7.1-CLASSIC (archived to `.dev/previous_versions/`)
- **Focus**: All development now concentrated on v3.x CAT Edition
- **Branding**: Removed "CAT" suffix - Supervertaler IS the CAT editor
- **Messaging**: Single product line, clear value proposition to users

**Repository Cleanup**:
- Moved all v2.x and earlier v3.x versions to `.dev/previous_versions/` folder
- Unified changelog (consolidated CHANGELOG-CAT.md and CHANGELOG-CLASSIC.md)
- Removed confusing dual-version documentation
- Main executable: `Supervertaler_v3.7.1-beta.py`

**Folder Structure Reorganization** (v3.7.1 continued):
```
user data/
├── Prompt_Library/
│   ├── System_prompts/        (19 Markdown files)
│   └── Custom_instructions/   (8 Markdown files)
├── Translation_Resources/
│   ├── Glossaries/
│   ├── TMs/
│   ├── Non-translatables/
│   └── Segmentation_rules/
└── Projects/
```

**Benefits**:
- ✅ Clearer product identity
- ✅ Reduced user confusion
- ✅ Simplified documentation
- ✅ Better focus for development
- ✅ Easier to present to LSPs (single unified tool)

---

## [3.6.9-beta] - 2025-10-19 📁 FOLDER STRUCTURE REORGANIZATION

### 🗂️ MAJOR RESTRUCTURING

**Hierarchical Folder Organization**:
- Created `Prompt_Library/` to group all prompt-related resources:
  - `System_prompts/` - Domain-specific system prompts (19 files)
  - `Custom_instructions/` - User custom instructions (8 files)
- Created `Translation_Resources/` to centralize translation assets:
  - `Glossaries/` - Terminology databases
  - `TMs/` - Translation Memory files
  - `Non-translatables/` - Non-translatable terms lists
  - `Segmentation_rules/` - Segmentation rule files

**Migration Details**:
- Successfully migrated all 27 prompt files
- Full dev mode support (both `user data/` and `user data_private/`)
- Backward compatibility with auto-migration function
- Old folders automatically cleaned up

**Code Updates**:
- Updated `get_user_data_path()` function calls throughout
- Added `migrate_old_folder_structure()` for automatic migration
- Updated folder link operations
- Enhanced documentation examples

**Benefits**:
- ✨ **Better Scalability**: Clear hierarchy for future features
- ✨ **Improved Navigation**: Logical grouping of resources
- ✨ **Professional Polish**: Well-organised data structure
- ✨ **Future-Ready**: Easy to add new resource types

### 📦 REPOSITORY CLEANUP

**Previous Versions Folder**:
- Moved to `.dev/previous_versions/` (centralized archive)
- Archived: v3.7.1-CLASSIC.py
- Archived: v3.7.1-beta_CAT.py
- Archived: v3.7.1-beta_CAT.py
- Root now contains only: v3.7.1.py

---

## [3.6.8-beta] - 2025-10-19 📝 MARKDOWN PROMPT FORMAT

### ✨ MAJOR ENHANCEMENT

**Complete Markdown Format Migration for Prompts**:
- **NEW**: All prompts (System Prompts + Custom Instructions) now use Markdown with YAML frontmatter
- **NEW**: Save dialogs default to `.md` format instead of `.json`
- **NEW**: Beautiful native Markdown tables for glossaries and structured data
- **NEW**: YAML frontmatter provides clean, human-readable metadata
- **NEW**: Mixed format support - loads both `.json` and `.md` files automatically
- **MIGRATION**: All 27 existing prompts converted from JSON to Markdown

**User Experience**:
- ✅ Double-click prompts to open in any text editor
- ✅ Read and edit prompts naturally with section headers
- ✅ No escaped quotes or verbose JSON syntax
- ✅ Glossaries display as beautiful Markdown tables
- ✅ Human-friendly editing experience

**Format Example**:
```markdown
---
name: "Patent Translation Specialist"
description: "Expert patent translator"
domain: "Intellectual Property"
version: "2.2.0"
task_type: "Translation"
created: "2025-10-19"
---

# Patent Translation Guide

You are an expert translator with deep expertise in intellectual property...

## Key Principles

- Maintain technical precision
- Preserve claim structure
- Use consistent terminology
```

**Technical Implementation**:
- `parse_markdown()` - Parse Markdown with YAML frontmatter
- `dict_to_markdown()` - Save prompt data as formatted Markdown
- `_parse_yaml()` - Simple YAML parser for frontmatter
- `_load_from_directory()` - Enhanced for `.json` and `.md` files
- `convert_json_to_markdown()` - Convert JSON to Markdown
- `convert_all_prompts_to_markdown()` - Batch conversion

**Migration Summary**:
- ✅ 19 System Prompts converted
- ✅ 8 Custom Instructions converted
- ⚠️ 3 empty corrupted files skipped
- **Total**: 27 prompts successfully migrated

---

## [3.6.7-beta] - 2025-10-18 ✨ POLISH & FIXES

### ✨ ENHANCEMENTS

**UI Polish & Usability**:
- **Reduced Tab Height**: Lowered vertical padding for better screen density
- **Removed Maximize View**: Eliminated obsolete maximize functionality (~725 lines cleaned)
- **Better Button Names**: "📝 View/Edit Analysis Prompts" for clarity
- **Clickable Folder Links**: System_prompts and Custom_instructions folders now clickable
  - Opens Windows Explorer / macOS Finder / Linux file manager

**Website Enhancements**:
- **NEW About Section**: Beautiful gradient design telling Supervertaler's story
- Three story cards showing evolution from manual workflow to full CAT features
- Vision dialogue for future AI interaction
- Responsive design with modern effects

### 🐛 BUG FIXES

**Translation Error with Prompt Manager**:
- Fixed: `'Supervertaler' object has no attribute 'custom_instructions_text'`
- Root cause: Functions looking for old text widget
- Solution: Check `self.active_custom_instruction` first with fallback

**System Prompts Not Appearing**:
- Fixed: Saved prompts not showing in Prompt Manager
- Root cause: JSON using wrong name field
- Solution: Use `user_entered_name` for metadata

---

## [3.6.6-beta] - 2025-10-18 🤖 PROMPT ASSISTANT UX OVERHAUL

### 🎯 MAJOR UX IMPROVEMENTS

**Renamed "AI Assistant" to "Prompt Assistant"**:
- Better describes its purpose (analyzing documents and generating prompts)
- More professional terminology

**Moved to Prompt Library as Third Tab**:
- Consolidates all prompt-related features in one place
- Natural workflow: Analyze → Generate → Browse/Edit → Apply
- Auto-hides editor panel when active to maximize workspace
- Auto-shows editor when switching to other prompt tabs

**Smart Editor Panel Visibility**:
- Context-aware UI adapts based on current task
- Full width workspace for document analysis
- Better screen real estate utilization

### 🔄 TECHNICAL CHANGES

- Renamed UI components
- Updated event handlers for tab switching
- Preserved all functionality
- Enhanced documentation

---

## Previous Versions (Archived)

### v3.7.1-beta, v3.7.1-beta, v3.7.1-beta
See [.dev/previous_versions/](.dev/previous_versions/) folder

### v3.7.1-CLASSIC (Archived - No Longer Developed)
**Production-ready DOCX-based workflow** (last update: 2025-10-14):
- CAT tool integration (CafeTran, memoQ, Trados)
- Translation Memory with fuzzy matching
- Multiple AI providers
- Custom prompts with variable substitution
- Full document context awareness

**Note**: This version is archived but remains available at [GitHub Release v3.7.1](https://github.com/michaelbeijer/Supervertaler/releases/tag/v3.7.1) for users who prefer the simpler DOCX-based workflow.

---

## Release Strategy

**Current Focus**: v3.7.1+ (Unified CAT Edition)
- Weekly incremental improvements
- User feedback integration
- LSP consulting feedback incorporation
- Feature expansion based on professional translator needs

**Version Numbering**:
- **v3.x-beta**: Active development (current)
- **.dev/previous_versions/**: Archived but working versions

---

## Notable Features Across All Versions

### Core Translation Engine
- ✅ Multiple AI providers (OpenAI, Claude, Gemini)
- ✅ Custom prompts with variable substitution
- ✅ Translation Memory with fuzzy matching
- ✅ Full document context awareness
- ✅ Tracked changes learning

### Professional CAT Features
- ✅ Segment-based editing (CAT Editor)
- ✅ Grid pagination system (50 segments/page)
- ✅ Dual selection support (memoQ-style)
- ✅ CAT tool integration (memoQ, CafeTran, Trados)
- ✅ Figure context support (multimodal AI)

### Data Management
- ✅ Import/Export: DOCX, TSV, JSON, XLIFF, TMX
- ✅ Session reports in HTML and Markdown
- ✅ Project save/load with context preservation
- ✅ Automatic backups

### Prompt Management
- ✅ System Prompts (domain-specific)
- ✅ Custom Instructions (user-defined)
- ✅ Prompt Assistant (AI-powered generation)
- ✅ Markdown + YAML frontmatter format
- ✅ Mixed format support

---

## For Questions or Issues

- **GitHub Issues**: [michaelbeijer/Supervertaler](https://github.com/michaelbeijer/Supervertaler/issues)
- **Website**: [supervertaler.com](https://supervertaler.com)
- **Documentation**: See `/docs` folder and README.md

---

**Last Updated**: October 19, 2025  
**Maintainer**: Michael Beijer  
**License**: Open Source (MIT)
