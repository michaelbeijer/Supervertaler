# Supervertaler - Complete Changelog

**Latest Version**: v3.7.0 (2025-10-19)  
**Product**: Unified Supervertaler (v3.x CAT Edition)  
**Status**: Active Development

> As of v3.7.0, Supervertaler is a unified product focusing exclusively on the CAT (Computer-Aided Translation) editor experience. The previous Classic Edition (v2.x) is archived for reference but no longer actively developed.

---

## [3.7.0] - 2025-10-19 🎯 STABLE RELEASE

### ✨ MAJOR RESTRUCTURING

**Product Unification**:
- **Deprecated**: v2.5.0-CLASSIC (archived to `.dev/previous_versions/`)
- **Focus**: All development now concentrated on v3.x CAT Edition
- **Branding**: Removed "CAT" suffix - Supervertaler IS the CAT editor
- **Messaging**: Single product line, clear value proposition to users

**Repository Cleanup**:
- Moved all v2.x and earlier v3.x versions to `.dev/previous_versions/` folder
- Unified changelog (consolidated CHANGELOG-CAT.md and CHANGELOG-CLASSIC.md)
- Removed confusing dual-version documentation
- Main executable: `Supervertaler_v3.7.0-beta.py`

**Folder Structure Reorganization** (v3.6.9 continued):
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
- ✨ **Professional Polish**: Well-organized data structure
- ✨ **Future-Ready**: Easy to add new resource types

### 📦 REPOSITORY CLEANUP

**Previous Versions Folder**:
- Moved to `.dev/previous_versions/` (centralized archive)
- Archived: v2.5.0-CLASSIC.py
- Archived: v3.6.6-beta_CAT.py
- Archived: v3.6.7-beta_CAT.py
- Root now contains only: v3.7.0.py

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

### v3.6.5-beta, v3.6.4-beta, v3.6.3-beta
See [.dev/previous_versions/](.dev/previous_versions/) folder

### v2.5.0-CLASSIC (Archived - No Longer Developed)
**Production-ready DOCX-based workflow** (last update: 2025-10-14):
- CAT tool integration (CafeTran, memoQ, Trados)
- Translation Memory with fuzzy matching
- Multiple AI providers
- Custom prompts with variable substitution
- Full document context awareness

**Note**: This version is archived but remains available at [GitHub Release v2.4.1](https://github.com/michaelbeijer/Supervertaler/releases/tag/v2.4.1) for users who prefer the simpler DOCX-based workflow.

---

## Release Strategy

**Current Focus**: v3.7.0+ (Unified CAT Edition)
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
