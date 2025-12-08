# Supervertaler Architecture

**Generated:** 2025-12-08 17:41:47

---

## System Overview

Supervertaler is a PyQt6-based desktop application for AI-powered translation with CAT tool integration.

### Core Components

#### 🎨 UI Components

- `ai_file_viewer_dialog` - AI Assistant File Viewer Dialog

Dialog for viewing attached file content in markdown format
- `encoding_repair_Qt` - Encoding Repair Module - Qt Edition
Embeddable version of the text encoding repair tool for detecting and fixing mojibake/encoding corruption

This module can be embedded in the main Supervertaler Qt application as a tab
- `encoding_repair_ui` - Encoding Repair Tool UI - Menu-based interface for the encoding repair module

Provides a user-friendly GUI for detecting and fixing text encoding corruption
- `file_dialog_helper` - File Dialog Helper for Supervertaler
Wraps PyQt6 QFileDialog to remember last used directory across all dialogs
- `llm_superbench_ui` - Superbench - Qt UI Components
==============================

PyQt6 user interface for LLM translation benchmarking
- `model_update_dialog` - Model Update Dialog for Supervertaler
======================================

Dialog window that displays new LLM models detected by the version checker
- `pdf_rescue_Qt` - PDF Rescue Module - Qt Edition
Embeddable version of the AI-powered OCR tool for extracting text from poorly formatted PDFs
Supports multiple AI providers: OpenAI GPT-4 Vision, Anthropic Claude Vision, Google Gemini Vision

This module can be embedded in the main Supervertaler Qt application as a tab
- `prompt_manager_qt` - Prompt Manager Module - Qt Edition
4-Layer Prompt Architecture for maximum translation/proofreading/copywriting precision

Layers:
1
- `quick_access_sidebar` - Quick Access Sidebar - memoQ-style left navigation panel

Provides quick access to common actions, recent files, and project navigation
- `style_guide_manager` - Style Guide Manager Module

Manages translation style guides for different languages
- `superbench_ui` - Superbench - Qt UI Components
==============================

PyQt6 user interface for LLM translation benchmarking
- `supercleaner_ui` - Supercleaner UI Module for Supervertaler
========================================

Interactive UI for document cleaning with selectable operations
- `tm_editor_dialog` - TM Editor Dialog - Edit a specific Translation Memory

This dialog provides comprehensive editing for a single TM:
- Browse entries
- Concordance search
- Statistics
- Import/Export (scoped to this TM)
- Maintenance

Similar to TMManagerDialog but scoped to a specific tm_id
- `tm_manager_qt` - Translation Memory Manager for Supervertaler Qt
Provides comprehensive TM management features:
- Browse all TM entries
- Concordance search
- Import/Export TMX files
- Delete entries
- View statistics
- `tmx_editor_qt` - TMX Editor Module - PyQt6 Edition

Professional Translation Memory Editor for Qt version of Supervertaler
- `unified_prompt_manager_qt` - Unified Prompt Manager Module - Qt Edition
Simplified 2-Layer Architecture:

1

#### 🚀 Feature Modules

- `llm_clients` - LLM Clients Module for Supervertaler
=====================================

Specialized independent module for interacting with various LLM providers
- `llm_leaderboard` - LLM Leaderboard - Core Benchmarking Module
===========================================

Comprehensive LLM translation benchmarking system for Supervertaler
- `local_llm_setup` - Local LLM Setup Module for Supervertaler
=========================================

Provides setup wizard, status checking, and model management for local LLM
integration via Ollama
- `superbrowser` - =============================================================================
MODULE: Superbrowser - Multi-Chat AI Browser
=============================================================================
Display multiple AI chat pages side by side in a single interface
- `supercleaner` - Supercleaner Module for Supervertaler
======================================

Cleans up DOCX documents before translation by removing formatting issues,
excessive tags, and OCR artifacts
- `superdocs` - Superdocs - Automated Documentation Generator for Supervertaler
================================================================

Automatically generates and maintains living documentation by:
- Scanning Python source files
- Extracting classes, functions, and docstrings
- Creating markdown documentation
- Mapping module dependencies
- Generating architecture overview

Usage:
    from modules
- `superlookup` - Superlookup Engine
==================
System-wide translation lookup that works anywhere on your computer
- `supermemory` - Supermemory - Vector-Indexed Translation Memory
================================================
Semantic search across translation memories using embeddings
- `termbase_entry_editor` - Termbase Entry Editor Dialog

Dialog for editing individual termbase entries with all metadata fields
- `termbase_import_export` - Termbase Import/Export Module

Handles importing and exporting termbases in TSV (Tab-Separated Values) format
- `termbase_manager` - Termbase Manager Module

Handles all termbase operations: creation, activation, term management, searching
- `tm_metadata_manager` - Translation Memory Metadata Manager Module

Handles TM metadata operations: creation, activation, TM management
- `tmx_editor` - TMX Editor Module - Professional Translation Memory Editor

A standalone, nimble TMX editor inspired by Heartsome TMX Editor 8
- `tmx_generator` - TMX Generator Module

Helper class for generating TMX (Translation Memory eXchange) files

#### 🔧 Utilities

- `ai_actions` - AI Actions Module

Provides structured action interface for AI Assistant to interact with Supervertaler
resources (Prompt Library, Translation Memories, Termbases)
- `ai_attachment_manager` - AI Assistant Attachment Manager

Manages persistent storage of attached files for the AI Assistant
- `autofingers_engine` - AutoFingers Translation Automation Engine
Replicates AutoHotkey AutoFingers functionality in Python
Automates translation pasting in memoQ from TMX translation memory
- `cafetran_docx_handler` - CafeTran Bilingual DOCX Handler

This module handles the import and export of CafeTran bilingual DOCX files
- `config_manager` - Configuration Manager for Supervertaler
Handles user_data folder location, first-time setup, and configuration persistence
- `database_manager` - Database Manager Module

SQLite database backend for Translation Memories, Glossaries, and related resources
- `database_migrations` - Database Migration Functions

Handles schema updates and data migrations for the Supervertaler database
- `document_analyzer` - Document Analyzer Module

Analyzes loaded document segments to provide context-aware insights and suggestions
- `docx_handler` - DOCX Handler
Import and export DOCX files with formatting preservation
- `encoding_repair` - Text Encoding Corruption Detection and Repair Module

Detects and fixes common text encoding issues (mojibake), particularly:
- UTF-8 text incorrectly decoded as Latin-1 (Windows-1252)
- Double-encoded Unicode escape sequences
- Common encoding corruption patterns
- `figure_context_manager` - Figure Context Manager
Handles loading, displaying, and providing visual context for technical translations
- `find_replace` - Find and Replace Dialog Module

This module provides find and replace functionality for the CAT editor
- `glossary_manager` - Termbase Manager Module

Handles termbase/termbase management for Supervertaler:
- Create/delete glossaries
- Add/edit/delete terms
- Activate/deactivate for projects
- Import/export glossaries
- Search across termbases

Unified management for both global and project-specific termbases
- `image_extractor` - ═══════════════════════════════════════════════════════════════════════════════
Image Extractor Module for Supervertaler
═══════════════════════════════════════════════════════════════════════════════

Purpose:
    Extract images from DOCX files and save them as sequentially numbered PNG files
- `keyboard_shortcuts_widget` - Keyboard Shortcuts Settings Widget
Provides UI for viewing, editing, and managing keyboard shortcuts
- `model_version_checker` - Model Version Checker for Supervertaler
========================================

Automatically checks for new LLM models from OpenAI, Anthropic, and Google
- `mqxliff_handler` - MQXLIFF Handler Module
======================
Handles import/export of memoQ XLIFF (
- `non_translatables_manager` - Non-Translatables Manager Module

Manages non-translatable (NT) content - terms, phrases, and patterns that should 
not be translated
- `pdf_rescue_tkinter` - PDF Rescue Module
Embeddable version of the AI-powered OCR tool for extracting text from poorly formatted PDFs
Uses OpenAI's GPT-4 Vision API

This module can be embedded in the main Supervertaler application as a tab
- `project_home_panel` - Project Home Panel - Collapsible sidebar like memoQ's Project Home
- `prompt_assistant` - AI Prompt Assistant Module

Provides AI-powered prompt modification through natural language conversation
- `prompt_library` - Prompt Library Manager Module

Manages translation prompts with domain-specific expertise
- `prompt_library_migration` - Migration Script: 4-Layer to Unified Prompt Library

Migrates from old structure:
    1_System_Prompts/
    2_Domain_Prompts/
    3_Project_Prompts/
    4_Style_Guides/

To new unified structure:
    Library/
        Style Guides/
        Domain Expertise/
        Project Prompts/
        Active Projects/

System Prompts are moved to settings storage (handled separately)
- `ribbon_widget` - Ribbon Widget - Modern Office-style ribbon interface for Supervertaler Qt

Provides context-sensitive ribbon tabs with grouped tool buttons,
similar to memoQ, Trados Studio, and Microsoft Office applications
- `sdlppx_handler` - Trados Studio Package Handler (SDLPPX/SDLRPX)

This module handles the import and export of Trados Studio project packages
- `setup_wizard` - Setup Wizard for Supervertaler First Launch
Guides new users to select their user_data folder location
- `shortcut_manager` - Keyboard Shortcut Manager for Supervertaler Qt
Centralized management of all keyboard shortcuts
- `simple_segmenter` - Simple Segmenter
Basic sentence segmentation using regex patterns
- `statuses` - Centralized status vocabulary for Supervertaler segments
- `tag_cleaner` - TagCleaner Module for Supervertaler
Removes CAT tool tags from translation text

Supports tags from:
- memoQ
- Trados Studio
- CafeTran
- Wordfast

Can be used standalone or integrated with other modules like AutoFingers
- `tag_manager` - Tag Manager
Handle inline formatting tags (bold, italic, underline)

This module converts formatting runs into XML-like tags for editing,
validates tag integrity, and reconstructs formatting on export
- `term_extractor` - Term Extractor Module

Extracts potential terminology from source text for project termbases
- `termview_widget` - Termview Widget - RYS-style Inline Terminology Display

Displays source text with termbase translations shown directly underneath each word/phrase
- `theme_manager` - Theme Manager
=============
Manages UI themes and color schemes for Supervertaler Qt
- `tracked_changes` - Tracked Changes Management Module

This module handles tracked changes from DOCX files or TSV files
- `trados_docx_handler` - Trados Bilingual DOCX Handler (Review Files)

This module handles the import and export of Trados Studio bilingual review DOCX files
- `translation_memory` - Translation Memory Module - SQLite Database Backend

Manages translation memory with fuzzy matching capabilities using SQLite
- `translation_results_panel` - Translation Results Panel
Compact memoQ-style right-side panel for displaying translation matches
Supports stacked match sections, drag/drop, and compare boxes with diff highlighting

Keyboard Shortcuts:
- ↑/↓ arrows: Navigate through matches (cycle through sections)
- Spacebar/Enter: Insert currently selected match into target cell
- Ctrl+1-9: Insert specific match directly (by number, global across all sections)
- Escape: Deselect match (when focus on panel)

Compare boxes: Vertical stacked with resizable splitter
Text display: Supports long segments with text wrapping
- `translation_services` - Translation Services Module
Handles Machine Translation (MT) and Large Language Model (LLM) integration
Keeps main application file clean and manageable

Author: Michael Beijer
License: MIT
- `unified_prompt_library` - Unified Prompt Library Module

Simplified 2-layer architecture:
1
- `voice_dictation` - Voice Dictation Module for Supervertaler
Uses OpenAI Whisper for multilingual speech recognition
Supports English, Dutch, and 90+ other languages
- `voice_dictation_lite` - Lightweight Voice Dictation for Supervertaler
Minimal version for integration into target editors


---

## 🏗️ Application Structure

```
Supervertaler.py (Main Application)
    └── SupervertalerQt (QMainWindow)
        ├── UI Tabs
        │   ├── Grid View (Segment Editor)
        │   ├── Document View (Preview)
        │   ├── List View (Compact)
        │   ├── TM Browser
        │   ├── Termbases
        │   └── Settings
        │
        ├── Feature Integration
        │   ├── AI Translation (LLM Clients)
        │   ├── Translation Memory
        │   ├── Termbase Management
        │   ├── Voice Dictation (Supervoice)
        │   └── Benchmarking (Superbench)
        │
        └── File Operations
            ├── DOCX Import/Export
            ├── TMX Import/Export
            ├── Bilingual Tables
            └── Project Management
```

---

## 📦 Module Categories

### UI Components

- Modules: 16
- Classes: 43
- Functions: 5
- Lines: 18,166

### Feature Modules

- Modules: 14
- Classes: 41
- Functions: 23
- Lines: 11,589

### Utilities

- Modules: 42
- Classes: 80
- Functions: 25
- Lines: 22,045

