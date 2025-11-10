# Supervertaler Project Context

**Last Updated:** November 10, 2025
**Repository:** https://github.com/michaelbeijer/Supervertaler
**Maintainer:** Michael Beijer

---

## 📅 Recent Development Activity

### November 10, 2025 (Later) - AI Assistant Enhanced Prompt Generation

**🎯 ChatGPT-Quality Automatic Prompt Generation**

Redesigned the AI Assistant's "Analyze Project & Generate Prompts" feature to create comprehensive, professional translation prompts matching the quality of ChatGPT/Claude web interfaces.

**✅ Enhanced Prompt Generation:**

1. **Comprehensive High-Level Summaries**
   - AI now generates 3-4 paragraph detailed document analysis
   - Paragraph 1: Document purpose and main topic
   - Paragraph 2: Key technical details and innovations
   - Paragraph 3: Scope, structure, and special considerations
   - Paragraph 4: Translation challenges and style requirements
   - Previously: Only brief metadata (Type, Domain, Language pair)

2. **Extensive Glossaries**
   - Template now requires 30-40 key terms (up from 10-15)
   - Each term includes context notes
   - Covers all technical terminology, domain-specific terms, frequently occurring terms
   - Includes challenging or ambiguous terms with usage guidance

3. **Domain-Specific Constraints**
   - **Patents:** Claim structure, legal precision, figure references
   - **Technical:** Measurement units, technical accuracy
   - **Medical:** Clinical terminology, regulatory compliance
   - **Legal:** Legal terms of art, formal language
   - AI identifies document type and applies appropriate constraints

4. **Full Document Analysis**
   - AI now receives up to 50,000 characters of document content
   - Previously: Only 5 sample segments (500 chars total)
   - Fallback: First 100 complete segments if markdown not cached
   - Dramatic improvement in prompt quality and accuracy

5. **One-Click Workflow**
   - Generated prompts automatically created in Project Prompts folder
   - Automatically activated as primary prompt
   - Ready for immediate use in translation
   - No manual prompt engineering needed

**🐛 Bug Fixes:**

1. **Empty Chat Bubble Fix**
   - Problem: Empty assistant messages appeared when AI generated only ACTION blocks
   - Root cause: `cleaned_response` was empty string after removing ACTION blocks
   - Fix: Only add assistant message if `cleaned_response.strip()` is non-empty
   - File: `modules/unified_prompt_manager_qt.py` lines 2576-2578

2. **Full Document Content Sending**
   - Problem: Only 5 segments sent to AI (100 chars each = 500 chars total)
   - User expectation: Full document analysis
   - Fix: Send cached markdown (50,000 chars) or first 100 complete segments
   - File: `modules/unified_prompt_manager_qt.py` lines 2019-2030

3. **ACTION Block Parsing**
   - Problem: Regex required newline but AI outputted single-line format
   - Fix: Changed pattern from `r'ACTION:(\w+)\s*\n\s*PARAMS:\s*'` to `r'ACTION:(\w+)\s+PARAMS:\s*'`
   - File: `modules/ai_actions.py` line 85

**Files Modified:**

- [modules/unified_prompt_manager_qt.py](../modules/unified_prompt_manager_qt.py)
  - Lines 1966-2022: Enhanced prompt generation template with comprehensive instructions
  - Lines 2576-2578: Empty bubble fix (only add assistant message if non-empty)
  - Lines 2019-2030: Full document sending (50,000 chars vs 500 chars)
- [modules/ai_actions.py](../modules/ai_actions.py)
  - Line 85: ACTION parsing fix (accept single-line format)

**Example Generated Prompt Quality:**

Before:
- 10-15 terms in glossary
- No high-level summary
- Generic constraints
- Based on 5 sample segments (500 chars)

After:
- 30-40 terms in glossary with context notes
- 3-4 paragraph comprehensive high-level summary
- Domain-specific constraints (patents, technical, medical, legal)
- Based on full document (50,000 chars)
- Professional formatting matching user's example prompts

**Technical Implementation:**

Enhanced template structure:
```
YOUR TASK:
1. **ANALYZE THE FULL DOCUMENT** - Read through all content
2. **WRITE A COMPREHENSIVE HIGH-LEVEL SUMMARY** (3-4 paragraphs)
3. **EXTRACT 30-40 KEY TERMS** for glossary
4. **IDENTIFY DOMAIN-SPECIFIC CONSTRAINTS**
5. **CREATE THE ACTION BLOCK** with all content
```

**Benefits:**
- Professional-quality prompts matching ChatGPT/Claude web quality
- Save significant time - no manual prompt engineering needed
- Comprehensive coverage - extensive glossaries and detailed summaries
- Domain awareness - AI recognizes and adapts to document type
- Immediate use - prompts activated automatically

**Status:** ✅ Complete - v1.3.4 release ready

---

### November 10, 2025 (Earlier) - LLM Leaderboard UI Standardization

**🎯 Complete UI Header Standardization Across Modules**

Standardized the visual branding across all Supervertaler modules (LLM Leaderboard, TMX Editor, AutoFingers) with consistent header styling and extended this branding to Excel exports.

**✅ Completed Features:**

1. **Standardized Module Headers**
   - Applied consistent header style across all modules:
     - LLM Leaderboard: "🏆 LLM Leaderboard"
     - TMX Editor: Similar professional styling
     - AutoFingers: Similar professional styling
   - Header styling:
     - Blue title color (#1976D2) - matches Supervertaler branding
     - 16pt bold font for visibility
     - Compact spacing (no stretch)
   - Description box styling:
     - Light blue background (#E3F2FD)
     - Gray text color (#666)
     - Rounded corners (3px border-radius)
     - 5px padding
     - Word wrap enabled
   - Subtitle format: "Translation Quality Benchmarking System - A Supervertaler Module"

2. **Excel Export Branding Consistency**
   - Updated Excel export title sheet to match UI header style:
     - Title: "🏆 LLM Leaderboard" (with trophy emoji)
     - 24pt bold title in blue (#1976D2)
     - Subtitle: "Translation Quality Benchmarking System"
     - 12pt italic subtitle in gray (#666666)
     - Module branding: "A Supervertaler Module"
     - Clickable hyperlink to https://supervertaler.com/
   - Complete visual consistency between UI and exported files

3. **Previous Session Fixes Completed**
   - ✅ Claude model crash fix - Updated to Claude 4 series model IDs
   - ✅ Gemini API key mapping - Maps "gemini" provider to "google" API key name
   - ✅ Model dropdown selection - Shows correct friendly names (e.g., "GPT-5 (Reasoning)", "Claude Opus 4.1")
   - ✅ Excel export with dataset info in filename - Format: `LLM_Leaderboard_{dataset_name}_{timestamp}.xlsx`
   - ✅ Auto-create API keys file - Copies api_keys.example.txt to api_keys.txt on first run
   - ✅ Auto-scroll log - Always shows latest benchmark messages
   - ✅ Comprehensive Excel export - Three sheets (About, Summary, Results) with professional formatting

**Files Modified:**
- [modules/llm_leaderboard_ui.py](../modules/llm_leaderboard_ui.py)
  - Lines 90-111: Standardized header with emoji and professional styling
  - Lines 547-565: Excel export title sheet with matching branding
  - Lines 782-825: Model name mapping for correct dropdown display
  - Lines 827-832: Auto-scrolling log implementation
  - Lines 479-776: Comprehensive Excel export system

**Technical Details:**

**UI Header Implementation:**
```python
# Header (matches TMX Editor / AutoFingers style)
header = QLabel("🏆 LLM Leaderboard")
header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
layout.addWidget(header, 0)

# Description box
description = QLabel(
    "Translation Quality Benchmarking System - A Supervertaler Module.\n"
    "Compare translation quality, speed, and cost across multiple LLM providers."
)
description.setWordWrap(True)
description.setStyleSheet(
    "color: #666; padding: 5px; "
    "background-color: #E3F2FD; border-radius: 3px;"
)
layout.addWidget(description, 0)
```

**Excel Export Title Sheet:**
```python
# Title with emoji (matches UI header style)
ws_info['A1'] = "🏆 LLM Leaderboard"
ws_info['A1'].font = Font(size=24, bold=True, color="1976D2")
ws_info.merge_cells('A1:D1')

# Subtitle
ws_info['A2'] = "Translation Quality Benchmarking System"
ws_info['A2'].font = Font(size=12, italic=True, color="666666")
ws_info.merge_cells('A2:D2')

# Branding with hyperlink
ws_info['A3'] = "A Supervertaler Module"
ws_info['A3'].font = Font(size=11, color="0066CC", underline="single")
ws_info['A3'].hyperlink = "https://supervertaler.com/"
ws_info.merge_cells('A3:D3')
```

**Benefits:**
- Professional, consistent branding across all modules
- Clear visual identity reinforcing Supervertaler ecosystem
- Excel exports maintain same professional appearance as UI
- User experience enhanced through visual consistency
- Easier module recognition and navigation

**Status:** ✅ Complete - All standardization tasks finished

---

### November 9, 2025 (Later) - Segment-Level AI Access + Critical Bug Fix

**🎯 Phase 2 Enhancement Complete: Segment-Level AI Actions**

Implemented segment-level access for AI Assistant allowing querying of specific segments and translation progress tracking.

**✅ Segment-Level AI Actions Implemented:**
- Added two new AI actions:
  - `get_segment_count` - Returns total segments, translated, and untranslated counts
  - `get_segment_info` - Retrieves specific segment(s) by ID, multiple IDs, or range
- AI Assistant can now answer:
  - "How many segments are in this document?"
  - "What is segment 5?"
  - "Show me segments 10 through 15"
- First 10 segments automatically included in AI context for quick reference
- Full segment properties available: id, source, target, status, type, notes, match_percent, etc.

**✅ CAT Tool Tag Handling:**
- Implemented comprehensive HTML entity escaping for segment display
- Proper escaping order: `&` → `<` → `>` → `"` (prevents double-escaping)
- Supports all CAT tool tags: Trados Studio, memoQ, Wordfast, CafeTran
- Segments displayed in code blocks with monospace font for readability

**✅ Auto-Markdown Generation Feature:**
- Added optional setting: Settings → General → AI Assistant Settings
- Checkbox: "Auto-generate markdown for imported documents"
- When enabled, automatically converts DOCX/PDF to markdown on import
- Markdown saved to `user_data_private/AI_Assistant/current_document/`
- Includes metadata JSON with conversion timestamp and file info
- Setting persists in `ui_preferences.json`

**🐛 CRITICAL BUG FIX:**
- Fixed attribute name mismatch: `self.prompt_manager` → `self.prompt_manager_qt`
- This was preventing:
  - Current document from showing in AI Assistant sidebar after import
  - Auto-markdown generation from triggering
  - Context refresh from working properly
- All document context integration now working correctly

**Files Modified:**
- [Supervertaler_Qt.py](../Supervertaler_Qt.py) - Fixed attribute names, added auto-markdown setting UI
- [modules/unified_prompt_manager_qt.py](../modules/unified_prompt_manager_qt.py) - Added segment info method and auto-markdown generation
- [modules/ai_actions.py](../modules/ai_actions.py) - Added segment actions and HTML escaping
- [test_ai_actions.py](../test_ai_actions.py) - Added tests 9 and 10 for segment actions
- [docs/AI_ASSISTANT_INTEGRATION.md](AI_ASSISTANT_INTEGRATION.md) - Updated with segment access documentation

**Testing:**
- ✅ All 10 tests passing
- ✅ Test 9: get_segment_count action
- ✅ Test 10: get_segment_info action (single, multiple, range)

**Benefits:**
- AI can answer segment-specific questions
- Translation progress tracking via AI
- Direct segment content access by number
- CAT tool tags handled properly in display
- Optional markdown conversion for document analysis
- Fixed critical bug preventing document context integration

**Version:** Released as v1.3.2

---

### November 9, 2025 (Earlier) - System Prompts Tab + AI Assistant Enhancement Plan

**🎯 Complete System Prompts UI + Phase 1 Enhancement Plan**

Major additions to the System Prompts accessibility and planning for file attachment and AI action integration.

**✅ System Prompts Settings Tab Implemented:**
- Added dedicated "📝 System Prompts" settings tab in Settings
- Mode selector dropdown for three translation modes:
  - Single Segment Translation
  - Batch DOCX Translation
  - Batch Bilingual Translation
- Rich text editor with monospace font for editing prompts
- Save functionality (to both memory and JSON)
- Reset to default with confirmation dialog
- Navigation from Prompt Library tab to Settings → System Prompts
- Stored in `user_data_private/Prompt_Library/system_prompts_layer1.json`

**Files Modified:**
- [Supervertaler_Qt.py](../Supervertaler_Qt.py) - Added System Prompts tab (lines 2965-3846)
- [modules/unified_prompt_manager_qt.py](../modules/unified_prompt_manager_qt.py) - Updated navigation (lines 1424-1439)

**🔄 PLANNED: AI Assistant Enhancement (November 9, 2025)**

Created comprehensive enhancement plan for fixing three critical issues with AI Assistant:

**Issue 1: File Attachments Not Persistent**
- Current: Files only stored in memory (`self.attached_files` list)
- Current: Files lost when application closes
- Current: No UI to view/manage attached files after uploading
- **Planned Solution (Phase 1 - HIGH PRIORITY):**
  - Create persistent storage: `user_data_private/AI_Assistant/attachments/`
  - Save markdown files with metadata (JSON)
  - Implement file viewer dialog with markdown preview
  - Add expandable attached files panel in context sidebar
  - Add view/remove functionality

**Issue 2: AI Cannot Act on Prompt Library**
- Current: AI context only mentions prompts exist
- Current: AI cannot list, create, or modify prompts
- Current: No structured action interface
- **Planned Solution (Phase 2 - MEDIUM PRIORITY):**
  - Implement function calling/action parsing system
  - Add tools: `list_prompts()`, `create_prompt()`, `update_prompt()`, etc.
  - Parse AI responses for ACTION markers
  - Execute actions and update prompt library in real-time

**Storage Structure (Phase 1):**
```
user_data_private/
  AI_Assistant/
    attachments/
      {session_id}/
        {file_hash}.md        # Converted markdown content
        {file_hash}.meta.json # Metadata (original name, type, date)
    index.json               # Master index of all attachments
    conversations/
      {conversation_id}.json # Conversation history with references
```

**Metadata Format:**
```json
{
  "file_id": "abc123...",
  "original_name": "project_brief.pdf",
  "original_path": "/path/to/original.pdf",
  "file_type": ".pdf",
  "size_bytes": 123456,
  "size_chars": 45678,
  "attached_at": "2025-11-09T10:30:00",
  "conversation_id": "conv_xyz",
  "markdown_path": "attachments/conv_xyz/abc123.md"
}
```

**UI Enhancements (Phase 1):**
- Expandable "📎 Attached Files" section in context sidebar
- File list showing: name, size, date
- View button → opens dialog with markdown preview
- Remove button → confirmation + delete from disk
- Files persist across sessions

**AI Actions System (Phase 2):**
- Structured response parsing (ACTION format)
- Available tools:
  - `list_prompts()` - List all prompts in library
  - `get_prompt(path)` - Get content of specific prompt
  - `create_prompt(name, content, folder)` - Create new prompt
  - `update_prompt(path, content)` - Update existing prompt
  - `search_prompts(query)` - Search prompts by content/name
- System prompt enhancement with action instructions

**Implementation Timeline:**
- Phase 1 (File Persistence & Viewing): 2-3 hours
- Phase 2 (AI Actions System): 3-4 hours
- Testing & Refinement: 1-2 hours
- **Total:** 6-9 hours development time

**Files to Create:**
- `modules/ai_attachment_manager.py` - File attachment persistence
- `modules/ai_actions.py` - AI action system and handlers
- `modules/ai_file_viewer_dialog.py` - File viewing dialog

**Documentation:**
- [docs/AI_ASSISTANT_ENHANCEMENT_PLAN.md](AI_ASSISTANT_ENHANCEMENT_PLAN.md) - Full technical specification

**Status:** ✅ Phase 1 COMPLETE, ✅ Phase 2 COMPLETE

**Phase 1 Implementation Complete (November 9, 2025):**

✅ **Files Created:**
- `modules/ai_attachment_manager.py` (390 lines) - Complete persistence system
- `modules/ai_file_viewer_dialog.py` (160 lines) - File viewer and removal dialogs
- `test_attachment_manager.py` - Comprehensive test suite (all tests passing)

✅ **Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Full integration completed
  - Imported AttachmentManager and dialogs
  - Initialized AttachmentManager in `__init__`
  - Added `_load_persisted_attachments()` method
  - Modified `_attach_file()` to save to disk
  - Created `_create_attached_files_section()` - expandable panel
  - Added `_refresh_attached_files_list()` - dynamic file list
  - Added `_create_file_item_widget()` - file item with view/remove buttons
  - Added `_view_file()` - opens FileViewerDialog
  - Added `_remove_file()` - removes from disk and memory
  - Added `_toggle_attached_files()` - expand/collapse functionality
  - Updated `_update_context_sidebar()` to refresh file list
  - Updated `_load_conversation_history()` to refresh UI

✅ **Features Implemented:**
- **Persistent Storage:** Files saved to `user_data_private/AI_Assistant/attachments/`
- **Metadata Tracking:** JSON files with original name, path, type, size, date
- **Session Management:** Files organized by date-based sessions
- **Master Index:** `index.json` tracks all attachments across sessions
- **Expandable UI:** Collapsible attached files section in context sidebar
- **File List:** Shows name, type, size for each file
- **View Dialog:** Read-only markdown preview with copy to clipboard
- **Remove Function:** Confirmation dialog + disk deletion
- **Auto-Load:** Files persist and reload across app restarts

✅ **Testing Results:**
All 8 tests passed:
1. ✓ Module imports successful
2. ✓ AttachmentManager initialization
3. ✓ Session management
4. ✓ File attachment with metadata
5. ✓ File listing
6. ✓ File retrieval with content
7. ✓ Statistics tracking
8. ✓ File removal (tested separately)

**Phase 2 Implementation Complete (November 9, 2025):**

✅ **Files Created:**
- `modules/ai_actions.py` (665 lines) - Complete AI Actions system
  - AIActionSystem class with 12 action handlers
  - Smart JSON parser for ACTION blocks with proper brace matching
  - Action execution and result formatting
  - System prompt addition for AI instruction
- `test_ai_actions.py` (457 lines) - Comprehensive test suite (8/8 tests passing)

✅ **Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Full AI Actions integration
  - Imported AIActionSystem (line 30)
  - Initialized AI Actions in `__init__` (lines 432-436)
  - Modified `_send_ai_request()` to parse and execute actions (lines 2176-2193)
  - Updated `_build_ai_context()` to include action instructions (line 2126)
  - Auto-reload prompt library after create/update/delete actions
  - Refresh tree widget UI when prompts are modified

✅ **Features Implemented:**
- **12 Available Actions:**
  1. `list_prompts` - List all prompts with optional folder filter
  2. `get_prompt` - Get full details of specific prompt
  3. `create_prompt` - Create new prompt with metadata
  4. `update_prompt` - Update existing prompt content/metadata
  5. `delete_prompt` - Delete prompt from library
  6. `search_prompts` - Search by name, content, tags, or all
  7. `create_folder` - Create new folder in library
  8. `toggle_favorite` - Toggle favorite status
  9. `toggle_quick_run` - Toggle Quick Run menu status
  10. `get_favorites` - List all favorite prompts
  11. `get_quick_run` - List all Quick Run prompts
  12. `get_folder_structure` - Get complete folder hierarchy

- **Smart ACTION Parser:**
  - Proper JSON extraction with brace matching
  - Handles nested JSON objects
  - Handles strings with escaped characters
  - Extracts multiple ACTION blocks from single response
  - Removes ACTION blocks from displayed response

- **Result Display:**
  - Formatted action results in chat
  - Success/failure indicators
  - Detailed result information
  - Error messages for failed actions

- **UI Integration:**
  - Actions executed automatically when AI includes them
  - Prompt Library UI refreshes after modifications
  - System messages show action results
  - Seamless conversational interface

✅ **Testing Results:**
All 8 tests passed:
1. ✓ AIActionSystem initialization
2. ✓ list_prompts action (all + folder filter)
3. ✓ create_prompt action
4. ✓ search_prompts action (by name, tags, all)
5. ✓ Parse and execute ACTION blocks from AI response
6. ✓ update_prompt and delete_prompt actions
7. ✓ toggle_favorite and toggle_quick_run actions
8. ✓ Format action results for display

**Example Usage:**
```
User: "Create a medical translation prompt for cardiology"

AI: I'll create that prompt for you.

ACTION:create_prompt
PARAMS:{"name": "Cardiology Translation Expert", "content": "You are an expert cardiology translator...", "folder": "Medical", "tags": ["medical", "cardiology", "heart"]}

The prompt has been created and is ready to use!

[System automatically executes action and shows:]
✓ **create_prompt**: Created prompt: Cardiology Translation Expert
  Path: Medical/Cardiology Translation Expert.md
```

**Benefits:**
- AI can now actively manage the Prompt Library
- No manual prompt creation needed
- Conversational prompt management
- Intelligent prompt suggestions
- Automated library organization

---

### November 8-9, 2025 - MAJOR: Unified Prompt System + AI Assistant

**🎯 Complete UI Reorganization + AI Assistant Implementation**

Major refactoring of the entire prompt management system from 4-layer to 2-layer architecture, PLUS integration of a full AI Assistant for conversational prompt generation and document analysis.

---

## ✅ FIXED: Chat UI Rendering (November 9, 2025)

**Status:** RESOLVED - Chat interface now renders perfectly with custom Qt delegates

**Solution Implemented:**
Replaced the problematic QTextEdit+HTML approach with a **QListWidget + Custom QStyledItemDelegate** solution. This provides full control over rendering using Qt's native painting system.

**Implementation Details:**

1. **New ChatMessageDelegate Class** ([unified_prompt_manager_qt.py:30-286](modules/unified_prompt_manager_qt.py#L30-L286))
   - Custom `QStyledItemDelegate` that paints chat bubbles using `QPainter`
   - Supports three message types: user, assistant, system
   - Proper text wrapping with `QFontMetrics.boundingRect()`
   - Dynamic height calculation in `sizeHint()`
   - Professional styling:
     - User messages: Right-aligned, Supervertaler blue gradient (#5D7BFF → #4F6FFF)
     - AI messages: Left-aligned, light gray (#F5F5F7)
     - System messages: Centered, subtle notification style
   - Avatar circles with gradient backgrounds (👤 user, 🤖 AI)
   - Proper shadows, rounded corners (18px radius), smooth antialiasing

2. **Updated Chat Display** ([unified_prompt_manager_qt.py:643-677](modules/unified_prompt_manager_qt.py#L643-L677))
   - Replaced `QTextEdit` with `QListWidget`
   - Applied `ChatMessageDelegate` as item delegate
   - Disabled selection/focus for clean appearance
   - Smooth pixel-based scrolling

3. **Simplified Message Adding** ([unified_prompt_manager_qt.py:1932-1959](modules/unified_prompt_manager_qt.py#L1932-L1959))
   - `_add_chat_message()` now creates `QListWidgetItem` with data
   - No more HTML/CSS - just data stored in `UserRole`
   - Auto-scroll to bottom on new messages

**What Now Works:**
- ✅ Perfect chat bubble rendering with gradients and shadows
- ✅ User text fully visible (white on blue gradient)
- ✅ AI text fully visible (dark on light gray)
- ✅ Avatars properly positioned and styled
- ✅ Text wraps correctly within 70% max width
- ✅ Professional appearance matching Supervertaler branding
- ✅ No truncation or formatting glitches
- ✅ Smooth scrolling and responsive layout

**Testing:**
- Created [test_chat_ui.py](test_chat_ui.py) - standalone test window
- Tests all three message types (user, assistant, system)
- Tests long messages for proper wrapping
- All visual issues resolved

**Files Modified:**
- [modules/unified_prompt_manager_qt.py](modules/unified_prompt_manager_qt.py)
  - Added `ChatMessageDelegate` class (lines 30-286)
  - Updated imports for Qt painting classes
  - Modified `_create_chat_interface()` to use QListWidget
  - Simplified `_add_chat_message()` method
  - Removed old HTML-based stub methods

---

### November 8, 2025 - MAJOR: Unified Prompt Library System

**🎯 Complete Refactoring: 4-Layer → 2-Layer Prompt Architecture**

Radically simplified the prompt system from a confusing 4-layer architecture to an intuitive 2-layer system inspired by CoTranslatorAI. This is a MAJOR refactoring affecting the entire prompt management system.

**🔄 Architecture Change:**

**OLD (Confusing):**
```
System Prompts tab      → CAT tool tags, formatting
Domain Prompts tab      → Industry/domain expertise
Project Prompts tab     → Project-specific rules
Style Guides tab        → Language formatting rules
```

**NEW (Simple):**
```
System Templates        → In Settings, auto-selected by mode
Prompt Library          → Unified workspace with folders, multi-attach
```

**✅ Completed Implementation:**

1. **Core Library Module** (`modules/unified_prompt_library.py` - 700+ lines)
   - ✅ Nested folder support (unlimited depth like CoTranslator)
   - ✅ Favorites system (stored in YAML frontmatter)
   - ✅ Quick Run menu for one-click prompts
   - ✅ Multi-attach capability (primary + multiple attached prompts)
   - ✅ Markdown files with YAML frontmatter
   - ✅ Full CRUD operations
   - ✅ Recursive folder loading
   - ✅ Path-based organization

2. **Migration System** (`modules/prompt_library_migration.py` - 500+ lines)
   - ✅ Automatic migration from 4-layer to unified structure
   - ✅ Backs up old folders with `.old` extension
   - ✅ Converts JSON prompts to Markdown
   - ✅ Adds metadata (favorite, quick_run, tags, folder)
   - ✅ Creates new Library/ folder structure
   - ✅ Preserves all existing prompts
   - ✅ One-time migration on first launch
   - ✅ **TESTED & WORKING** - All 5 tests passing

3. **New UI** (`modules/unified_prompt_manager_qt.py` - 900+ lines)
   - ✅ Single-tab interface replacing 4 separate tabs
   - ✅ Tree view with nested folders
   - ✅ Favorites section at top
   - ✅ Quick Run menu section
   - ✅ Active configuration panel showing:
     - Current mode (Single Segment, Batch DOCX, Batch Bilingual)
     - Primary prompt (main instructions)
     - Attached prompts (additional rules)
   - ✅ Right-click context menus:
     - Set as Primary / Attach to Active
     - Add to Favorites / Quick Run
     - Edit / Duplicate / Delete
     - Create folders and subfolders
   - ✅ Prompt editor with metadata fields
   - ✅ Preview combined prompt
   - ✅ System Templates access from main UI

4. **Test Suite** (`tests/test_unified_prompt_library.py`)
   - ✅ Test 1: Migration (PASSED)
   - ✅ Test 2: Library Loading (PASSED - 16 prompts)
   - ✅ Test 3: Favorites & Quick Run (PASSED)
   - ✅ Test 4: Multi-Attach (PASSED)
   - ✅ Test 5: Prompt Composition (PASSED)
   - **Result: 5/5 tests passed** ✅

5. **Demo Application** (`tests/demo_unified_prompt_ui.py`)
   - ✅ Standalone UI demo
   - ✅ Shows complete new interface
   - ✅ Run with: `python tests/demo_unified_prompt_ui.py`

6. **User Documentation** (`docs/UNIFIED_PROMPT_LIBRARY_GUIDE.md`)
   - ✅ Complete user guide
   - ✅ Migration explanation
   - ✅ Usage examples
   - ✅ FAQ and troubleshooting
   - ✅ Tips and best practices

**📁 New File Structure:**

```
user_data/Prompt_Library/
├── 1_System_Prompts.old          (backed up - old system prompts)
├── 2_Domain_Prompts.old          (backed up - old domain prompts)
├── 3_Project_Prompts.old         (backed up - old project prompts)
├── 4_Style_Guides.old            (backed up - old style guides)
├── .migration_completed          (migration flag file)
└── Library/                      (NEW unified structure)
    ├── Style Guides/
    │   ├── Dutch.md
    │   ├── English.md
    │   ├── French.md
    │   ├── German.md
    │   └── Spanish.md
    ├── Domain Expertise/         (migrated from 2_Domain_Prompts)
    │   ├── Medical Translation Specialist.md
    │   ├── Legal Translation Specialist.md
    │   ├── Financial Translation Specialist.md
    │   └── ... (8 prompts total)
    ├── Project Prompts/           (migrated from 3_Project_Prompts)
    │   ├── Professional Tone & Style.md
    │   ├── Preserve Formatting & Layout.md
    │   └── Prefer Translation Memory Matches.md
    └── Active Projects/           (user creates own subfolders)
        └── (empty - ready for user organization)
```

**🔧 Technical Details:**

**Terminology Decision:**
- **"System Templates"** (not "Base Templates" or "Tag Processing Rules")
- Hidden in Settings > Translation (not in main UI)
- Auto-selected based on document type

**Metadata Format (YAML Frontmatter):**
```yaml
---
name: "Medical Translation Specialist"
description: "Expert medical device translation"
domain: "Medical"
version: "1.0"
task_type: "Translation"
favorite: false
quick_run: false
folder: "Domain Expertise"
tags: ["medical", "technical", "regulatory"]
created: "2025-10-19"
modified: "2025-11-08"
---

# Prompt content here...
```

**Multi-Attach System:**
```python
# User Configuration:
Primary Prompt:  Medical Translation Specialist
Attached:        Dutch Style Guide
Attached:        Professional Tone & Style

# System automatically combines:
final_prompt = system_template + primary + attached[0] + attached[1]
```

**Prompt Composition Logic:**
```python
def build_final_prompt(source_text, source_lang, target_lang, mode):
    # Layer 1: System Template (auto-selected)
    system = get_system_template(mode)  # single, batch_docx, batch_bilingual
    
    # Layer 2: Library Prompts
    library = ""
    if active_primary_prompt:
        library += primary_prompt
    for attached in attached_prompts:
        library += "\n\n" + attached
    
    # Combine
    final = system + library
    
    # Replace placeholders
    final = final.replace("{{SOURCE_LANGUAGE}}", source_lang)
    final = final.replace("{{TARGET_LANGUAGE}}", target_lang)
    final = final.replace("{{SOURCE_TEXT}}", source_text)
    
    return final
```

---

## ✨ AI ASSISTANT IMPLEMENTATION (November 8-9, 2025)

**Complete AI-Powered Conversational Interface**

After completing the unified prompt system, we restructured the Prompt Manager interface to include an AI Assistant for conversational prompt generation and document analysis.

### UI Structure Change

```
OLD: Single "📚 Prompt Library" tab

NEW: "🤖 Prompt Manager" with two sub-tabs:
     ├── 📚 Prompt Library (original functionality)
     └── ✨ AI Assistant (NEW conversational AI)
```

### AI Assistant Features Implemented

**1. Core Functionality** ✅
- LLM Integration: OpenAI, Claude, Gemini
- Auto-detects LLM provider from main app settings
- Conversation persistence (JSON storage)
- Message history (last 10 on load, full history saved)
- Clear chat functionality with confirmation

**2. Context Awareness** ✅
- Access to all 38+ prompts in unified library
- Current document tracking
- Recent conversation memory (last 5 messages in context)
- Attached files content included in AI requests

**3. File Attachments** ✅
- PDF/DOCX/PPTX/XLSX auto-conversion using `markitdown`
- TXT/MD direct import
- Multiple file support
- Content included in AI context (first 2000 chars per file)
- Persistent across sessions

**4. Project Analysis** ✅
- "🔍 Analyze Project & Generate Prompts" button
- Analyzes current project context
- Suggests relevant existing prompts
- Generates new custom prompts with complete text
- Lists available resources (prompts, TMs, termbases)

**5. UI Components** ⚠️ (FUNCTIONAL BUT STYLING BROKEN)

Context sidebar (left):
- 📄 Current Document
- 📎 Attached Files (with count)
- 💡 Prompt Library (38 prompts)
- 💾 Translation Memories (placeholder)
- 📚 Termbases (placeholder)

Chat area (right):
- Message display with chat bubbles
- Multi-line input (Shift+Enter for new lines)
- 🗑️ Clear Chat button
- Send button

### Technical Implementation

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` (1,600+ lines)
  - `_init_llm_client()` - Initialize AI with API keys
  - `_load_conversation_history()` - Restore previous chats
  - `_save_conversation_history()` - Persist to JSON
  - `_create_ai_assistant_tab()` - Build UI
  - `_create_context_sidebar()` - Resource panel
  - `_create_chat_interface()` - Chat display + input
  - `_send_chat_message()` - Handle user input
  - `_send_ai_request()` - Call LLM API
  - `_add_chat_message()` - Render chat bubbles
  - `_attach_file()` - File attachment + conversion
  - `_analyze_and_generate()` - Project analysis
  - `_clear_chat()` - Clear conversation

**Dependencies Added:**
```python
# pyproject.toml
dependencies = [
    ...
    "markitdown>=0.0.1",  # Document conversion
]
```

**Data Storage:**
```
user_data/ai_assistant/
└── conversation.json
    {
      "history": [
        {
          "role": "user|assistant|system",
          "content": "message text",
          "timestamp": "2025-11-08T..."
        }
      ],
      "files": [
        {
          "path": "full/path/to/file",
          "name": "filename.pdf",
          "content": "converted markdown...",
          "type": ".pdf",
          "size": 12345,
          "attached_at": "2025-11-08T..."
        }
      ],
      "updated": "2025-11-08T..."
    }
```

**Integration Points:**
- Uses `modules/llm_clients.py` for provider-agnostic API calls
- Uses `UnifiedPromptLibrary` to access prompt data
- Connects to parent app for settings and current document
- Same LLM provider/model as main translation engine

### 🚨 CURRENT PROBLEM: Chat UI Rendering

**Status:** BROKEN - Functional but visually unusable

**Issues:**
1. User input text appears invisible (white on white background)
2. Chat bubbles oddly formatted and truncated
3. HTML/CSS styling not rendering correctly in QTextEdit
4. Avatar positioning incorrect (bottom instead of top)
5. Message wrapping issues

**What's Been Tried:**
- ✅ Table-based layout → messages truncated
- ✅ Div-based with inline-block → formatting weird  
- ✅ Solid colors vs gradients → still issues
- ✅ Various text color combinations → input still invisible
- ✅ Vertical-align: top/bottom → avatars misaligned

**Root Cause:**
QTextEdit has limited HTML/CSS support. Advanced styling (flexbox, proper inline-block, gradients) doesn't work well.

**Recommendations for Fixing:**

**Option 1: QListWidget with Custom Delegates** (RECOMMENDED)
```python
class ChatMessageDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Custom painting of chat bubbles
        # Full control over rendering
        pass
```

**Option 2: QScrollArea + Custom Widgets**
```python
chat_container = QVBoxLayout()
for message in messages:
    bubble = ChatBubbleWidget(message)
    chat_container.addWidget(bubble)
```

**Option 3: QWebEngineView**
```python
# Use HTML/CSS/JS in web view
# Best styling control, but heavier
```

**What Works:**
- ✅ AI communication (all providers)
- ✅ Message sending and receiving
- ✅ Conversation persistence
- ✅ File attachments with markitdown conversion
- ✅ Context building and prompt analysis
- ✅ Error handling and logging

**What's Broken:**
- ❌ Chat bubble visual styling
- ❌ User input text visibility
- ❌ Avatar positioning
- ❌ Message truncation

**Goal:**
Professional chat interface matching Supervertaler website colors (#5D7BFF blue gradient), with:
- Clean chat bubbles (user right in blue, AI left in gray)
- Avatar icons (👤 for user, 🤖 for AI)
- Proper text visibility and wrapping
- Elegant spacing and shadows
- Similar to iMessage/Slack/modern chat UIs

**Files to Fix:**
- `modules/unified_prompt_manager_qt.py`
  - Lines ~1540-1650: `_add_chat_message()` method
  - Lines ~350-450: `_create_chat_interface()` method

**Documentation Created:**
- `docs/AI_ASSISTANT_GUIDE.md` - Complete user guide
- `docs/AI_ASSISTANT_IMPLEMENTATION.md` - Technical details
- `docs/AI_ASSISTANT_QUICK_REFERENCE.md` - Quick reference card

---

**📊 Migration Results:**

Actual migration output from test run:
```
============================================================
🔄 Starting Prompt Library Migration
============================================================

📚 Migrating Domain Prompts...
   ✓ Migrated 8 domain prompts

📋 Migrating Project Prompts...
   ✓ Migrated 3 project prompts

🎨 Migrating Style Guides...
   ✓ Migrated 5 style guides

💾 Creating backups of old folders...
   ✓ Backed up: 1_System_Prompts → 1_System_Prompts.old
   ✓ Backed up: 2_Domain_Prompts → 2_Domain_Prompts.old
   ✓ Backed up: 3_Project_Prompts → 3_Project_Prompts.old
   ✓ Backed up: 4_Style_Guides → 4_Style_Guides.old

============================================================
✅ Migration Complete! Migrated 16 prompts
============================================================
```

**🎯 Key Design Decisions:**

1. **No Legacy Mode** - Clean break, simpler codebase
2. **Favorites in YAML** - No separate favorites.json file
3. **Unlimited Nesting** - Like CoTranslator's folder structure
4. **System Templates Hidden** - In Settings, not fighting for attention
5. **Multi-Attach** - More flexible than old single-active system

**🚧 Remaining Integration Work:**

**Status: Ready for main app integration**

Files created and tested:
- ✅ `modules/unified_prompt_library.py`
- ✅ `modules/unified_prompt_manager_qt.py`
- ✅ `modules/prompt_library_migration.py`
- ✅ `tests/test_unified_prompt_library.py`
- ✅ `tests/demo_unified_prompt_ui.py`
- ✅ `docs/UNIFIED_PROMPT_LIBRARY_GUIDE.md`

Next steps to complete:
1. **Integrate into Supervertaler_Qt.py:**
   - Replace `from modules.prompt_manager_qt import PromptManagerQt`
   - With `from modules.unified_prompt_manager_qt import UnifiedPromptManagerQt`
   - Update all calls to `build_final_prompt()`
   - Update state tracking for active prompts

2. **Add System Templates to Settings:**
   - Create Settings > Translation > System Templates section
   - Allow viewing/editing mode-specific templates
   - Show warning about modifying CAT tool formats

3. **Final Testing:**
   - Test in actual translation workflow
   - Test mode switching (single → batch_docx → batch_bilingual)
   - Test with real documents
   - Verify tag preservation still works
   - Test with various LLM providers

**💡 User-Facing Benefits:**

- **Simpler:** One workspace instead of 4 tabs
- **Flexible:** Organize prompts however you want
- **Powerful:** Multi-attach for combining instructions
- **Familiar:** Like CoTranslatorAI's prompt library
- **Visual:** See folder structure, favorites, quick run
- **Safe:** Automatic migration with backups

**🔍 Files Modified/Created:**

**New Files:**
- `modules/unified_prompt_library.py` (700+ lines)
- `modules/unified_prompt_manager_qt.py` (900+ lines)
- `modules/prompt_library_migration.py` (500+ lines)
- `tests/test_unified_prompt_library.py` (200+ lines)
- `tests/demo_unified_prompt_ui.py` (60 lines)
- `docs/UNIFIED_PROMPT_LIBRARY_GUIDE.md` (comprehensive guide)

**Files to be Modified:**
- `Supervertaler_Qt.py` (replace prompt manager integration)
- Settings dialog (add System Templates section)

**Old Files (to be deprecated):**
- `modules/prompt_manager_qt.py` (4000+ lines - will be replaced)
- `modules/prompt_library.py` (680 lines - no longer needed)
- `modules/style_guide_manager.py` (316 lines - no longer needed)

**🎓 Learning Notes for Future AI:**

This refactoring demonstrates:
1. **User-centric design:** Simplify confusing architectures
2. **Inspiration from competitors:** CoTranslatorAI's approach was better
3. **Safe migration:** Always backup, provide rollback
4. **Modular design:** Each component testable independently
5. **Documentation:** User guide written before integration
6. **Test-driven:** Verify functionality before touching main app

**⚠️ Important Context:**

- This ONLY affects Supervertaler_Qt.py (Qt version)
- Supervertaler_tkinter.py is separate and unchanged
- Old prompt manager kept in codebase temporarily for reference
- Migration runs automatically on first launch of new version
- User can manually rollback by renaming .old folders

---

## 📅 Previous Development Activity

### November 7, 2025 - TagCleaner Module & AutoFingers Enhancement

**🎯 New Module: TagCleaner - CAT Tool Tag Removal System**

Implemented a standalone, modular tag cleaning system that removes CAT tool tags from translation text. Follows Supervertaler's modular architecture philosophy - can be used independently or integrated with other modules.

**✅ Completed Features:**

1. **Standalone TagCleaner Module** ([modules/tag_cleaner.py](../modules/tag_cleaner.py))
   - ✅ Fully independent module with no core dependencies
   - ✅ Granular control per CAT tool and tag type
   - ✅ Settings export/import via `to_dict()` / `from_dict()`
   - ✅ Extensible architecture for adding new tag patterns
   - ✅ Can be launched standalone or used programmatically

2. **memoQ Index Tag Support** (Initial Implementation)
   - ✅ Regex pattern: `(?:\[\d+\}|\{\d+\])`
   - ✅ Removes tags like `[1}`, `{2]`, `[7}`, `{8]`, `[99}`, `{100]`, etc.
   - ✅ Supports unlimited digit range (not limited to specific numbers)
   - ✅ Tested with real-world translation projects

3. **AutoFingers Integration**
   - ✅ TagCleaner instance automatically available: `engine.tag_cleaner`
   - ✅ Tags cleaned before pasting translation (line 290 in autofingers_engine.py)
   - ✅ Clean separation of concerns - modular design
   - ✅ Optional on-the-fly tag cleaning when pasting from TMX to memoQ

4. **User Interface Controls** (Supervertaler_Qt.py:12777-12843)
   - ✅ Master switch: "Enable tag cleaning" checkbox
   - ✅ Granular tag type selection (indented hierarchy):
     - ✅ memoQ index tags ([1} {2]) - **Active and functional**
     - ⏸️ Trados Studio tags - Framework ready (coming soon)
     - ⏸️ CafeTran tags - Framework ready (coming soon)
     - ⏸️ Wordfast tags - Framework ready (coming soon)
   - ✅ Scrollable settings panel for smaller screens

5. **Settings Persistence**
   - ✅ Structured JSON format in autofingers_settings.json
   - ✅ Nested structure matching modular architecture
   - ✅ Backward compatible with existing AutoFingers settings
   - ✅ Auto-save and auto-load on startup

**🔧 Technical Implementation:**

**Files Created:**
- `modules/tag_cleaner.py` - Standalone TagCleaner module (273 lines)
- `test_tag_cleaner_integration.py` - Comprehensive test suite

**Files Modified:**
- `modules/autofingers_engine.py` - Integrated TagCleaner (line 15, 87, 290)
- `Supervertaler_Qt.py` - Added UI controls and settings management
- `user_data_private/autofingers_settings.json` - Extended structure

**Architecture Highlights:**
```python
# Standalone usage
from modules.tag_cleaner import TagCleaner

cleaner = TagCleaner()
cleaner.enable()
cleaner.enable_memoq_index_tags()
cleaned = cleaner.clean("Text [1}with{2] tags")
# Result: "Text with tags"

# Integration with AutoFingers
engine.tag_cleaner.enable()
# Tags automatically cleaned during translation paste
```

**Test Results:**
- ✅ All 3 test suites passing
- ✅ Standalone module test
- ✅ AutoFingers integration test
- ✅ Settings export/import test
- ✅ Real-world project validation

**📦 Future Extensibility:**

The TagCleaner module is designed for easy expansion:

1. **Additional CAT Tools** (Ready to implement):
   - Trados Studio tag patterns
   - CafeTran Espresso tags
   - Wordfast tags
   - SDL Passolo tags
   - Others as requested by users

2. **Standalone Features** (Planned):
   - Dedicated TagCleaner tab in Supervertaler
   - Menu integration (Tools → Clean Tags)
   - Batch tag cleaning for TMX files
   - CLI mode for automation scripts
   - Drag-and-drop file cleaning

3. **Advanced Patterns** (Extensible):
   - Custom regex patterns via UI
   - Tag pattern libraries
   - Import/export tag pattern sets
   - Community-contributed patterns

**💡 Design Philosophy:**

TagCleaner embodies Supervertaler's modular architecture:
- **Independent**: Can run without Supervertaler core
- **Reusable**: Other modules can import and use it
- **Configurable**: Granular control, not all-or-nothing
- **Extensible**: New tag types = add pattern, no refactoring
- **User-Requested**: Future features driven by community needs

**🎯 User Impact:**

- Translators using AutoFingers with tagged TMX files can now clean tags automatically
- No manual tag removal needed after pasting from TMX
- Supports mixed CAT tool workflows (e.g., Trados TMX → memoQ target)
- Foundation for future standalone tag cleaning workflows

**📝 Version:** 1.2.4 (2025-11-07)

---

### November 6, 2025 - LLM & MT Integration Complete

**🎯 Major Achievement: Complete Translation Matching System**

Successfully integrated all translation sources (Termbase, TM, MT, LLM) with proper chaining and display:

**✅ Completed Features:**
1. **Multi-LLM Support Fully Operational**
   - ✅ OpenAI GPT integration working (GPT-4o, GPT-5, etc.)
   - ✅ Claude 3.5 Sonnet integration (API key issue - user needs credits)
   - ✅ Google Gemini integration working (Gemini 2.0 Flash)
   - ✅ Flexible API key naming: supports both `google` and `google_translate` keys
   - ✅ Flexible Gemini key naming: supports both `gemini` and `google` keys

2. **Google Cloud Translation API Integration**
   - ✅ Proper implementation using `google-cloud-translate` library
   - ✅ Added `load_api_keys()` function to `modules/llm_clients.py` for standalone operation
   - ✅ Backward compatible key naming (checks both `google_translate` and `google`)
   - ✅ Uses Translation API v2 with direct API key authentication
   - ✅ Returns structured response with translation, confidence, and metadata

3. **Termbase Match Preservation**
   - ✅ Fixed issue where termbase matches disappeared when TM/MT/LLM appeared
   - ✅ Root cause: delayed search wasn't receiving termbase matches parameter
   - ✅ Solution: Pass `current_termbase_matches` to `_add_mt_and_llm_matches()`
   - ✅ Termbase matches now display consistently across all scenarios

4. **Performance Optimization**
   - ✅ Debounced search with 1.5-second delay prevents excessive API calls
   - ✅ Timer-based cancellation when user moves between segments
   - ✅ Immediate termbase display, deferred TM/MT/LLM loading

**🔧 Technical Implementation:**

**File: `modules/llm_clients.py`**
- Added standalone `load_api_keys()` function (lines 27-76)
- Fixed Google Translate to use loaded API keys instead of undefined function
- Supports multiple API key locations (user_data_private/, root)
- Handles both key naming conventions for backward compatibility

**File: `Supervertaler_Qt.py`**
- Fixed Gemini integration to check for both `gemini` and `google` API keys (line ~10620)
- Enhanced Google Translate integration with comprehensive logging
- Termbase match preservation through delayed search parameter passing
- Structured match chaining: Termbase → TM → MT → LLM

**🐛 Resolved Issues:**
1. ✅ Google Translate error: `name 'load_api_keys' is not defined` 
   - Fixed by adding function to llm_clients.py module
2. ✅ Gemini not being called despite API key present
   - Fixed by checking both `gemini` and `google` key names
3. ✅ Termbase matches disappearing when TM/MT/LLM loaded
   - Fixed by passing termbase matches to delayed search function

**📦 Dependencies:**
- `google-cloud-translate` - Google Cloud Translation API library
- `openai` - OpenAI API client  
- `anthropic` - Anthropic Claude API client
- `google-generativeai` - Google Gemini API client
- `httpx==0.28.1` - HTTP client (version locked for LLM compatibility)

**💡 Key Design Decisions:**

1. **API Key Flexibility:**
   - Support both `google_translate` and `google` for Google Cloud Translation
   - Support both `gemini` and `google` for Gemini API
   - Provides backward compatibility and user flexibility

2. **Standalone Module Design:**
   - `llm_clients.py` can function independently with its own `load_api_keys()`
   - No dependency on main application for API key loading
   - Enables reuse in other projects

3. **Match Preservation Architecture:**
   - Termbase matches stored in panel's `_current_matches` dictionary
   - Passed explicitly to delayed search functions
   - Never overwritten, only appended to by TM/MT/LLM results

**🎯 Next Steps:**
- [ ] Test all LLM providers with real API keys
- [ ] Add user feedback for API errors (better than console logs)
- [ ] Consider adding DeepL integration
- [ ] Implement match insertion keyboard shortcuts

---

## 🎯 Project Overview

**Supervertaler** is a dual-platform AI-powered translation tool for professional translators. Currently maintaining two active versions during transition to Qt as primary platform.

### Two Active Versions

| Aspect | Qt Edition | Tkinter Edition (Classic) |
|--------|-----------|---------------------------|
| **File** | `Supervertaler_Qt.py` | `Supervertaler_tkinter.py` |
| **Version** | v1.0.1+ (Active Development) | v2.5.0+ (Maintenance) |
| **Framework** | PyQt6 | Tkinter |
| **Status** | Primary (new features) | Legacy (feature parity) |
| **UI** | Modern ribbon + compact panels | Tabbed interface |
| **Database** | SQLite (shared schema) | SQLite (shared schema) |
| **Changelog** | `CHANGELOG_Qt.md` | `CHANGELOG_Tkinter.md` |

**Migration Strategy:** Move all tkinter functionality to Qt version, then deprecate tkinter in v2.0.0

---

## 📁 Repository Structure (Lean)

```
/
├── Supervertaler_Qt.py              # Qt Edition (PRIMARY)
├── Supervertaler_tkinter.py         # Tkinter Edition (legacy)
├── README.md                         # Repository overview
├── CHANGELOG_Qt.md                   # Qt version history
├── CHANGELOG_Tkinter.md              # Tkinter version history
├── RELEASE_NOTES.md                  # Current release info
│
├── modules/                          # Shared modules
│   ├── database_manager.py           # SQLite backend
│   ├── termbase_manager.py           # Termbases CRUD
│   ├── project_home_panel.py         # Project home UI (Qt)
│   ├── translation_results_panel.py  # Results UI (Qt)
│   ├── autofingers_engine.py         # Auto-fingers feature
│   ├── config_manager.py             # Settings/config
│   └── [other modules]
│
├── docs/
│   ├── PROJECT_CONTEXT.md            # ← THIS FILE (Single source of truth)
│   ├── QUICK_START.md                # Getting started
│   ├── ARCHITECTURE.md               # System design
│   ├── DATABASE.md                   # Database schema
│   ├── sessions/                     # Archived session summaries
│   ├── guides/                       # How-to guides
│   └── archive/                      # Old documentation (reference)
│
├── user_data/                        # User projects & database
├── user_data_private/                # Dev database (gitignored)
├── tests/                            # Unit tests
└── assets/                           # Icons, images
```

---

## 🔑 Key Features (Both Versions)

### Translation Memory (TM)
- SQLite-based persistent storage
- Full-text search with fuzzy matching
- TM matches with relevance scores
- Context-aware suggestions
- Import/export (TMX format)

### Termbases
- Multiple termbases per project
- Global and project-specific scopes
- Term search with filtering
- Priority-based matching
- Sample data: 3 termbases (Medical, Legal, Technical) with 48 terms

### CAT Functionality
- Segment-based translation editing
- Translation memory integration
- Match insertion (keyboard shortcuts)
- Project management
- Auto-fingers support

### AI Integration
- OpenAI GPT support
- Claude support (configurable)
- API key management

---

## 🗄️ Database Schema (SQLite)

### Core Tables
- **translation_units** - TM entries (source_text, target_text, language pairs)
- **termbases** - Termbase definitions (name, source_lang, target_lang, project_id)
- **termbase_terms** - Individual terms (source_term, target_term, domain, priority)
- **termbase_activation** - Project termbase activation tracking
- **non_translatables** - Locked terms
- **projects** - Translation projects

### Important Constraints
- `termbase_terms.source_lang` DEFAULT 'unknown' (NOT NULL removed)
- `termbase_terms.target_lang` DEFAULT 'unknown' (NOT NULL removed)
- Never use `glossary_terms` table (renamed to `termbase_terms`)
- Never use `glossary_id` column (renamed to `termbase_id`)

---

## ⚙️ Current Status (v1.1.1-Qt)

**Completed (Nov 1, 2025):**
✅ AutoFingers UI simplification - removed redundant "Use Alt+N" setting  
✅ Single "Confirm segments" checkbox now controls behavior (checked = Ctrl+Enter, unchecked = Alt+N)  
✅ Backward compatibility maintained for existing settings files  
✅ Version bumped to 1.1.1  

**Completed (Oct 29-30, 2025):**
✅ Termbases feature complete  
✅ Terminology standardized ("termbase" everywhere)  
✅ Database schema fixed (NOT NULL constraints)  
✅ Bug fixes: method names, Project object access  
✅ Sample data: 3 termbases with 48 terms  

**In Progress:**
- [ ] Terminology Search (Ctrl+P)
- [ ] Concordance Search (Ctrl+K)
- [ ] Test create/edit dialogs

**Known Issues:** None

---

## 📝 Naming Conventions

**ALWAYS USE:**
- ✅ "Termbase" (one word, lowercase)
- ✅ "Qt Edition" / "Tkinter Edition"
- ✅ "Translation Memory" or "TM"

**NEVER USE:**
- ❌ "Glossary" (replaced with "Termbase")
- ❌ "Term Base" (two words - always one word)
- ❌ `glossary_terms` or `glossary_id` (renamed to termbase_*)

---

## 🚀 Running Applications

### Qt Edition
```bash
python Supervertaler_Qt.py
```

### Tkinter Edition
```bash
python Supervertaler_tkinter.py
```

---

## 📚 Key Reference Files

| File | Purpose |
|------|---------|
| `docs/PROJECT_CONTEXT.md` | This file - source of truth |
| `CHANGELOG_Qt.md` | Qt version history |
| `CHANGELOG_Tkinter.md` | Tkinter version history |
| `RELEASE_NOTES.md` | Current release |
| `modules/database_manager.py` | Database layer |
| `modules/termbase_manager.py` | Termbase operations |

---

## 🔍 Before Starting Work

1. **Consult this document first** - It's your source of truth
2. Understand which version you're working on (Qt vs Tkinter)
3. Check naming conventions (Termbase, never Glossary)
4. Review current focus items above
5. Verify database table/column names are correct

---

## 💡 Repository Philosophy

**Lean = Efficient:**
- ✅ Only essential source code
- ✅ Current documentation in `docs/`
- ✅ Old docs archived, summarized in PROJECT_CONTEXT.md
- ✅ Smaller repo = faster AI operations = lower costs

---

**Last Updated:** November 1, 2025
**Next Review:** Start of development sprint

**Hidden folders** (.gitignored):
- `.dev/` - Tests, scripts, backup files, documentation tools
- `.supervertaler.local` - Dev mode feature flag

---

## ✨ Key Features

### v1.0.0-Qt (Modern CAT Interface)

1. **Modern Ribbon Interface**
   - 4 context-sensitive ribbon tabs (Home, Translation, Tools, Settings)
   - Minimalist design, non-intrusive controls
   - Proper CAT workflow integration

2. **Professional Tab Organization**
   - **Project Group:** Project Manager, Project Editor
   - **Resources Group:** Translation Memories, Glossaries, Non-Translatables, Prompts
   - **Modules Group:** TMX Editor, Reference Images, PDF Rescue, Encoding Repair, AutoFingers, Tracked Changes
   - **Settings Group:** Settings, Log
   - **Utilities:** Universal Lookup (Ctrl+Alt+L)

3. **Translation Results Panel (NEW - PRODUCTION READY) ✨**
   - **Compact memoQ-style design** - Minimal wasted space, maximum info density
   - **Stacked match sections:** NT, Machine Translation, Translation Memory, Termbases
   - **Collapsible headers** - Toggle sections to see only what matters
   - **Match items display:**
     * Type badge (NT/MT/TM/Termbase)
     * Relevance percentage (0-100%)
     * Target text (main content, line-wrapped)
     * Source context when available
   - **Drag/drop support** - Drag matches directly into target field
   - **Compare boxes** - Shows Current Source | TM Source | TM Target side-by-side
   - **Diff highlighting** - Color-coded differences (ready to integrate)
   - **Segment info** - Shows current segment number and source preview
   - **Notes section** - For translator annotations (compact, below matches)

4. **AutoFingers Automation**
   - Replicates memoQ AutoFingers functionality
   - TMX-based translation automation
   - Hotkey-driven (Ctrl+Alt+P for single, Ctrl+Shift+L for loop)
   - Thread-safe match pane display
   - Simplified UI: Single "Confirm segments" checkbox controls behavior
     * Checked: Uses Ctrl+Enter to confirm segment before moving to next
     * Unchecked: Uses Alt+N to move to next without confirming

5. **Universal Lookup (Ctrl+Alt+L)**
   - Global hotkey search across all resources
   - Real-time results display
   - Integration with all translation memory sources

### v2.5.0-CLASSIC

1. **Multi-LLM Support**
   - Gemini, Claude, OpenAI/GPT
   - API key management in settings
   - Model selection per project

2. **DOCX Import/Export Workflow**
   - Load bilingual DOCX files
   - Extract/manage segments
   - AI translation with custom prompts
   - Export results to DOCX format

3. **Custom Prompts System**
   - System prompts (define AI role/expertise)
   - Custom instructions (user preferences/context)
   - Public and private storage
   - Reusable across projects

4. **Post-Translation Analysis (NEW - v2.5.0)**
   - **Tracked Changes Review**: Analyze editing patterns from memoQ/CafeTran
   - Load bilingual DOCX with tracked changes
   - Browse and filter changes
   - **Export to Markdown Report** with:
     - 3-column table (Source, Original, Revised)
     - AI-powered change summaries (4th column, optional)
     - Configurable batch processing (1-100 segments)
     - Precise change detection (quotes, punctuation, terminology)
   - **Export to TSV** for analysis/sharing

5. **Session Management**
   - Session reports in markdown
   - Statistics and summaries
   - Translation history

### v3.1.1-beta

- Segment-based CAT editor interface
- **Prompt Library** with tree-based organization
- Filter and search capabilities
- UK English lowercase UI style ("System prompts" not "System Prompts")
- Same AI backend as CLASSIC but with different workflow

---

## 📊 Tracked Changes Feature Details

**Purpose:** Help translators review how much they edited AI-generated translations

**Workflow:**
1. Translate project in CAT tool (memoQ, CafeTran, etc.) with tracked changes enabled
2. Export bilingual document with tracked changes
3. Load in Supervertaler
4. Browse changes (with optional search/filter)
5. Export analysis report (Markdown with optional AI summaries)

**AI Analysis (Optional):**
- Asks currently selected AI to provide precise change summaries
- Uses batch processing (default 25 segments/API call)
- Configurable batch size via slider (1-100)
- Examples:
  - ✅ `"pre-cut" → "incision"`
  - ✅ `Curly quotes → straight quotes: "roll" → "roll"`
  - ✅ `"package" → "packaging"`
  - ❌ "Fixed grammar" (too vague - not used)

**Report Format:** Paragraph-based Markdown
```markdown
### Segment 1

**Target (Original):**  
[AI-generated text]

**Target (Revised):**  
[Your edited text]

**Change Summary:**  
[AI analysis of what changed]
```

---

## 🔧 Technical Details

### File Naming Conventions

- Main executables: `Supervertaler_vX.X.X-[CLASSIC|CAT].py`
- Version bumps affect:
  - File name itself
  - First line comment in file
  - README.md references
  - CHANGELOG entries

### Code Organization

**CLASSIC version:**
- `TrackedChangesAgent` - Core logic for tracked changes parsing
- `TrackedChangesBrowser` - UI dialog for browsing changes
- `export_to_tsv()` / `export_to_md()` - Export functionality
- AI analysis with batch processing

**CAT version:**
- `PromptLibrary` - Manages system prompts and custom instructions
- Tree-based UI for organization
- Same TrackedChangesAgent (shared logic)
- Separate UI browser (to be ported)

### AI Integration

**Supported Providers:**
- Gemini (`google-generativeai`)
- Claude (`anthropic`)
- OpenAI (`openai`)

**Current Prompts (Batch Processing):**
```
You are a precision editor analyzing tracked changes...
Compare original and revised text and identify EXACTLY what changed.
- Be extremely specific and precise
- Quote exact words/phrases that changed
- Use format: "X" changed to "Y"
- PAY SPECIAL ATTENTION to quotes/punctuation
- Do NOT use vague terms
- DO quote actual changed text
```

**Token Limits:**
- Batch: 2000 tokens (for 25 segments)
- Single: 100 tokens (fallback)
- Response max: 10 words per change (enforced in parsing)

---

## 📝 Version History

### v2.5.0-CLASSIC (Current)
- ✨ **NEW:** Tracked Changes Review feature
- ✨ **NEW:** AI-powered change summaries
- ✨ **NEW:** Batch processing for faster analysis
- ✨ **NEW:** Configurable batch size slider
- 🐛 Infrastructure updates for parallel folder structure
- 🎨 UK English lowercase style throughout

### v3.1.1-beta (Current)
- 🐛 Fixed system_prompts_dir initialization
- 🐛 Fixed prompt loading in dev mode
- 🐛 Fixed emoji rendering issues
- 🎨 Applied UK English lowercase style
- 📝 Removed private UI elements
- 🔧 Parallel folder structure implementation

---

## 🎯 Development Strategy

### Chat History Management
- **Daily exports:** `docs/chat-logs/copilot_chat_history_YYYY-MM-DD (MB).txt`
- **Purpose:** Full context preservation between sessions
- **Benefit:** Faster issue resolution, historical context
- **Maintenance:** Automated via GitHub Copilot Chat Exporter

### Documentation
- **README.md** - User-facing overview
- **CHANGELOG.md** - Main navigation (links to split logs)
- **CHANGELOG-CLASSIC.md** - v2.x.x history
- **CHANGELOG-CAT.md** - v3.x.x-beta history
- **.dev/** folder - Development tools, scripts, tests

### Quality Assurance
- Both programs compile without syntax errors
- UK English lowercase style enforced
- Emoji rendering tested (Unicode escape codes)
- Cross-version consistency maintained

---

## 🎯 Strategic Refocus: Companion Tool Philosophy (November 2025)

### Vision Shift

**Original Goal:** Build a full-featured CAT tool with grid editing, TM/termbase matching, and comprehensive translation workflows.

**New Focus:** **Companion Tool** - Work alongside existing CAT tools (memoQ, Trados, CafeTran, Wordfast, etc.) rather than replacing them.

### Rationale

1. **Complexity Management:** Building a fully functional CAT tool grid, TM matching, and termbase integration is beyond scope and duplicates existing professional tools.
2. **Play to Strengths:** Supervertaler excels at AI-powered features and specialized modules that CAT tools don't offer.
3. **User Value:** Translators can continue using their trusted CAT tools while leveraging Supervertaler's unique capabilities.

### Core Strengths to Preserve

✅ **AI-Powered Translation/Proofreading/Localization**
- Comprehensive prompt management system
- Multi-layer prompts (System, Domain, Project, Style Guide)
- Multiple LLM providers (OpenAI, Claude, Gemini)

✅ **Specialized Modules**
- **AutoFingers** - Get translations back into CAT tools via TMX
- **PDF Rescue** - Extract text from images using AI OCR
- **Omni-Lookup** - Universal search across all resources
- **Text Encoding Repair** - Fix encoding issues
- **Tracked Changes Review** - Analyze editing patterns

✅ **CAT Tool Integration**
- TMX export/import for seamless workflow
- Compatible with memoQ, Trados, CafeTran, Wordfast formats

### Simplification Strategy

#### Grid View - Simplified to Review Tool

**Keep:**
- ✅ View-only with minor editing capability (quick fixes allowed)
- ✅ All filtering capabilities (essential for quality review)
- ✅ Comprehensive find & replace system
- ✅ Multiple views (Grid/List/Document) + extensibility for future views
- ✅ Translation quality review tools

**Simplify/Remove:**
- ❌ Full editing capabilities (reduce to minor edits only)
- ❌ Complex segment editing workflows
- ❌ Advanced CAT features that duplicate CAT tool functionality

#### TM/Termbase Matching - Optional Feature

**Implementation:**
- ✅ Add **toggle switch** to enable/disable TM/termbase matching
- ✅ When disabled: Hide assistance panel or show only AI translations
- ✅ When enabled: Show matches as read-only reference (no insertion workflows)

**What "Complex Lookup/Insert Workflows" Means:**
- Automatic TM/termbase search when selecting segments
- Click-to-insert matches from assistance panel
- Keyboard shortcuts (Ctrl+1-9) to insert matches by number
- Drag-and-drop match insertion
- Auto-population of target fields from matches

**Simplified Approach:**
- Keep matching as **optional read-only reference**
- Remove insertion workflows (let CAT tool handle that)
- Focus on **quality review** rather than active editing

#### AutoFingers - Keep As-Is

- ✅ Leave AutoFingers functionality unchanged
- ✅ Continue TMX-based translation automation
- ✅ Maintain hotkey-driven workflow (Ctrl+Alt+P, Ctrl+Shift+L)

### Updated Feature Priorities

**High Priority (Core Companion Features):**
1. AI translation/proofreading with prompt management
2. Grid view for quality review (simplified)
3. All specialized modules (AutoFingers, PDF Rescue, etc.)
4. TMX export/import

**Medium Priority (Quality of Life):**
1. Optional TM/termbase matching (toggle)
2. Find & replace
3. Multiple view modes

**Low Priority (Future):**
1. Advanced grid editing features
2. Full CAT tool duplication features

### Migration Path

**Phase 1: Add Toggle for TM/Termbase Matching**
- Add settings option to enable/disable matching
- Update assistance panel to respect toggle
- Keep code but make it optional

**Phase 2: Simplify Grid Editing**
- Reduce editing capabilities to "minor edits only"
- Remove complex insertion workflows
- Keep view and filtering intact

**Phase 3: Documentation Update**
- Update user guides to reflect companion tool philosophy
- Emphasize integration with CAT tools
- Highlight unique AI-powered features

---

## 🚀 Next Steps / Roadmap

### Immediate (Refocus Implementation)
- [ ] Add toggle switch for TM/termbase matching (Settings → View/Display)
- [ ] Simplify grid editing to allow only minor edits
- [ ] Remove complex match insertion workflows (keep as read-only reference)
- [ ] Update documentation to reflect companion tool philosophy

### Short-term
- [ ] User manual updates (companion tool workflow)
- [ ] Integration guides for memoQ/Trados/CafeTran
- [ ] API key security improvements
- [ ] Performance optimization for large files

### Future Considerations
- [ ] Multi-language UI support
- [ ] Custom model parameter tuning
- [ ] Export to additional formats (Excel, PDF)
- [ ] Enhanced CAT tool integration features

---

## �️ Qt Edition Architecture (v1.0.0)

### Implementation Details

**Main Application File:** `Supervertaler_Qt.py` (5,800+ lines)
- Modern PyQt6 application with professional CAT interface
- 14-tab main interface organized into 4 functional groups
- Context-sensitive ribbon with 4 ribbon tabs
- Horizontal splitter layout: Grid (left) | TranslationResultsPanel (right)
- Universal Lookup integration with global hotkey (Ctrl+Alt+L)
- AutoFingers CAT automation with TMX support

**Translation Results Panel:** `modules/translation_results_panel.py` (345 lines)
- **TranslationResultsPanel** - Main widget class
  - Manages stacked match sections
  - Handles match selection and compare box display
  - Compact, memoQ-inspired design
  - Integration point for all match types

- **MatchSection** - Collapsible section for each match type
  - Header with toggle button and match count
  - Scrollable container for multiple matches
  - Emits signals when matches selected

- **CompactMatchItem** - Individual match display
  - Type badge + relevance percentage
  - Target text preview (line-wrapped)
  - Metadata/context display
  - Drag/drop support
  - Click-to-select functionality

- **Supporting Classes:**
  - `TranslationMatch` - Data class for matches
  - Helper methods for compare boxes and diff display

**Integration with Editor Tab:**
- `create_editor_tab()` - Creates horizontal splitter with grid and panel
- `create_assistance_panel()` - Instantiates TranslationResultsPanel
- `on_cell_selected()` - Populates panel when segment selected
- `search_and_display_tm_matches()` - Queries TM and generates matches

### Compact Design Philosophy

The TranslationResultsPanel was designed to minimize wasted space while maximizing usability, following memoQ's principles:

1. **Collapsible Sections** - Hide/show match types as needed
2. **Compact Match Items** - Essential info only (type, %, text preview)
3. **Stacked Layout** - Multiple matches visible without excessive scrolling
4. **Minimal Padding** - 2-4px margins between elements
5. **Smart Typography** - Varied font sizes (8-10pt) for hierarchy
6. **Visual Hierarchy** - Color coding (badges) for quick scanning
7. **Integrated Notes** - No separate panel needed, built into bottom of results

### Database Integration

- **TM Database:** `modules/database_manager.py` (SQLite with FTS5 search)
  - `search_all(source_text, max_matches)` - Returns list of TM matches
  - Each match includes: source, target, match_pct, metadata
  
- **Match Loading:**
  - `on_cell_selected()` calls `tm_database.search_all()`
  - Results transformed to `TranslationMatch` objects
  - Sorted by relevance (100% exact matches first)
  - Limited to 10 matches per type for performance

### Performance Optimizations

- **Lazy Loading:** Matches loaded only when segment selected
- **Scrollable Sections:** Large match sets handled with QScrollArea
- **Signal/Slot:** Minimal UI updates via Qt signals
- **Compact HTML:** Previous diff display also works (fallback)
- **Metadata Trimming:** Context limited to first 40 characters

### Diff Highlighting System

Already implemented in `search_and_display_tm_matches()`:
```python
from difflib import SequenceMatcher

# Green: added text (underline + bold)
# Red: deleted text (strikethrough)
# Handles insertions, deletions, and replacements
```

Ready to integrate into TranslationResultsPanel's compare boxes.

---

## 🔗 Related Files

### Qt Edition (v1.0.0)
- **Main Application:** `Supervertaler_Qt.py` (Primary CAT interface, 5800+ lines)
- **UI Components:**
  - `modules/translation_results_panel.py` - Match display panel (345 lines, NEW)
  - `modules/ribbon_widget.py` - Modern ribbon UI
  - `modules/universal_lookup.py` - Global hotkey search
  - `modules/autofingers_engine.py` - CAT automation
- **Core Functionality:**
  - `modules/database_manager.py` - TM database (SQLite + FTS5)
  - `modules/simple_segmenter.py` - Text segmentation
  - `modules/config_manager.py` - Settings management

### Classic & CAT Editions
- **Main programs:** `Supervertaler_v2.5.0-CLASSIC.py`, `Supervertaler_v3.1.1-beta_CAT.py`
- **Documentation:** `/docs/` folder
- **Chat logs:** `/docs/chat-logs/` folder
- **Development tools:** `/.dev/` folder
- **Core modules:** `/modules/` folder
- **User data:** `/user_data/` (public), `/user_data_private/` (dev only)

---

## 💡 Key Decisions & Rationale

1. **Parallel folder structure over suffix pattern**
   - Cleaner separation of public/private
   - Simpler .gitignore (1 line vs 7)
   - Future-proof for new data types

2. **Batch processing for AI analysis**
   - ~90% faster than segment-by-segment
   - Better consistency (AI sees context)
   - Reduced API costs
   - Configurable via slider for flexibility

3. **Markdown over table format for tracked changes**
   - More readable for translators
   - Handles long text better
   - Better for mobile viewing
   - Easier to share/print

4. **Tracked changes as post-translation tool, not context**
   - Avoids circular context (translator reviewing own changes)
   - Makes purpose clearer (analysis, not translation context)
   - Proper workflow: translate → review changes → iterate

5. **UK English lowercase style**
   - "System prompts" not "System Prompts"
   - Cleaner, more professional appearance
   - Consistent across both versions
   - User preference from initial discussions

---

## 📞 Contact / Maintenance

**Active Development By:** Michael Beijer
**Project Started:** October 2025
**Last Major Update:** November 7, 2025

**Development Workflow:**
1. Develop in workspace folder
2. Export daily chat history
3. Update PROJECT_CONTEXT.md periodically
4. Commit changes to GitHub
5. Reference previous chats as needed for continuity

---

## Recent Updates (November 7, 2025) - v1.2.3

### Status Column UI Improvements
Fixed and enhanced the status column display in Grid view:

**Visual Fixes:**
- Fixed status column background stretching issues when using auto-resize rows
- Removed fixed minimum height from status widgets - now adapts to row height
- Increased minimum row height from 20px to 32px to prevent icon cutoff
- Status widgets now properly center vertically regardless of row height
- Match percentage label only shows when match data exists (eliminates empty gaps)

**Icon Improvements:**
- **Not started**: ❌ (red X, 11px) - matches memoQ style
- **Pre-translated**: 🤖 (robot) - clearer indication of automatic translation
- **Translated**: ✏️ (pencil) - matches Trados style for manual work
- **Confirmed**: ✔ (green checkmark via CSS) - clean, consistent with ❌
- Swapped Translated and Confirmed icons for better semantic meaning
- Improved comment icon: 🗨️ with text-shadow for better visibility

**Interaction Changes:**
- Disabled click-to-change-status on status column (prevents visual glitches)
- Status changes now only via Segment Editor (more intentional workflow)

**Technical Changes:**
- Background color now on table item, widget is transparent (prevents rendering issues)
- Status icon size varies by status: 11px for ❌, 14px for others
- Green color (#2e7d32) applied via CSS to confirmed checkmark
- All changes in `Supervertaler_Qt.py` and `modules/statuses.py`

