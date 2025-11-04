# Supervertaler Project Context

**Last Updated:** November 1, 2025  
**Repository:** https://github.com/michaelbeijer/Supervertaler  
**Maintainer:** Michael Beijer

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

