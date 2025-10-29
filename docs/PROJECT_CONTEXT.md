# Supervertaler Project Context

**Last Updated:** October 29, 2025  
**Project Status:** Active Development (v1.0.0-Qt, v2.5.0-CLASSIC & v3.1.1-beta)  
**Current Version:** v1.0.1-Qt

---

## 📝 Current Focus: Termbases Feature - Terminology Standardization & Bug Fixes Complete ✅

**Status:** Termbases fully implemented with standardized terminology (v1.0.1-Qt)

**Session Summary (Oct 29, Afternoon):**
- ✅ **Terminology Standardization:** Replaced all "glossary" references with "termbase" throughout codebase
- ✅ **Database Schema Fixed:**
  - Table: `glossary_terms` → `termbase_terms`
  - Column: `glossary_id` → `termbase_id`  
  - Changed `source_lang` and `target_lang` from NOT NULL → DEFAULT 'unknown'
  - Fixed NOT NULL constraint errors preventing term creation
- ✅ **Code Updates:** 
  - Method: `create_glossaries_tab()` → `create_termbases_tab()`
  - Method: `create_glossary_results_tab()` → `create_termbase_results_tab()`
  - UI Label: "Term Bases" → "Termbases" (one word, consistent)
  - All Project object attribute access fixed (.id instead of .get('id'))
- ✅ **Bug Fixes:**
  - Fixed method call: `create_glossary_results_tab()` → `create_termbase_results_tab()`
  - Fixed Project object access pattern (was using dict .get() on object)
  - Database migration: Updated `user_data_private/supervertaler.db` with correct schema
- ✅ **Sample Data:** Created 3 test termbases with 48 terms (Medical, Legal, Technical)
- ✅ **Testing:** All syntax verified, application launches successfully

**Architecture Status:**
- **Tab Structure:** ✅ Complete - Termbases tab fully functional
- **Database:** ✅ Termbases tables (termbases, termbase_terms, termbase_activation)
- **UI Labels:** ✅ Consistent "Termbases" terminology throughout
- **Error Handling:** ✅ Fixed NOT NULL constraints, Project object access

**Next Phase:** 
- Implement Terminology Search (Ctrl+P)
- Implement Concordance Search (Ctrl+K)
- Test create/edit termbase dialogs in full app

---

## 🎯 Project Overview

**Supervertaler** is a multi-platform AI-powered translation tool for professional translators working with various LLM providers and CAT workflows.

### Three Active Versions

| Version | Name | Architecture | Status | Use Case |
|---------|------|--------------|--------|----------|
| **v1.0.1-Qt** | Qt Edition | Modern PyQt6 CAT interface | Active Development | Professional CAT workflow with advanced translation memory features |
| **v2.5.0-CLASSIC** | CLASSIC Edition | DOCX-based workflow | Production-ready | Professional translators using CAT tools (memoQ, CafeTran) |
| **v3.1.1-beta** | CAT Edition | Segment-based CAT editor | Beta/Experimental | Early adopters, new feature testing |

---

## 📝 Development Approach

- **Minimal Documentation During Development:** Extensive guides are created only when features stabilize. Active code changes are tested iteratively rather than documented extensively, as the codebase evolves frequently. This keeps workflow lean and documentation maintainable.

---

## 🏗️ Architecture & Infrastructure

### Private/Public Data System

**Implementation:** Parallel folder structure with `.supervertaler.local` feature flag

- **Development mode** (`.supervertaler.local` present):
  - All data auto-routes to `user data_private/` folder
  - Red "🔒 DEV MODE" banner visible in app
  - Complete isolation of private data
  
- **User mode** (no `.supervertaler.local`):
  - All data saved to public `user data/` folder
  - No UI clutter or private option visibility
  - Clean experience for end users

**Benefits:**
- ✅ Single codebase for both public and private use
- ✅ No confusing UI for users
- ✅ Simple `.gitignore` (one line: `user data_private/`)
- ✅ Easy mode switching for developers

**Migration:** Completed - uses parallel folder structure:
```
user data/              (public)
user data_private/      (dev only, gitignored)
```

### Repository Structure

**Root directory** (clean for users):
- `Supervertaler_v2.5.0-CLASSIC.py` - Main CLASSIC executable
- `Supervertaler_v3.1.1-beta_CAT.py` - Main CAT executable
- `modules/` - Core functionality (needed by v3.1.1)
- Documentation files (README, CHANGELOG, etc.)

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

## 🚀 Next Steps / Roadmap

### Immediate (Ready to implement)
- [ ] Port Tracked Changes feature to v3.1.1-beta
- [ ] Implement CAT-tool-specific tracked changes parsers
- [ ] Add batch size persistence (save user preference)

### Short-term
- [ ] User manual updates
- [ ] API key security improvements
- [ ] Performance optimization for large files

### Future Considerations
- [ ] Multi-language UI support
- [ ] Custom model parameter tuning
- [ ] Export to additional formats (Excel, PDF)
- [ ] Collaborative features (shared TMs, glossaries)

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
- **User data:** `/user data/` (public), `/user data_private/` (dev only)

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
**Last Major Update:** October 29, 2025  

**Development Workflow:**
1. Develop in workspace folder
2. Export daily chat history
3. Update PROJECT_CONTEXT.md periodically
4. Commit changes to GitHub
5. Reference previous chats as needed for continuity

