# Supervertaler Qt Migration Plan
## From tkinter v3.7.x to PyQt6 v1.x

**Document Version:** 1.0  
**Created:** October 26, 2025  
**Status:** Active Development

---

## Executive Summary

This document outlines the complete migration plan for Supervertaler from tkinter (v3.7.x) to PyQt6 (v1.x). This is a **long-term quality investment** to create a professional-grade CAT tool with industry-standard UI/UX.

### Why Qt?

The Qt demo (`qt_grid_demo.py`) proved that Qt offers:

✅ **Perfect auto-sizing** - One line: `table.resizeRowsToContents()`  
✅ **Sharp, crisp fonts** - Native rendering at all sizes  
✅ **Zero wasted space** - Professional grid layout like memoQ  
✅ **Industry standard** - Used by commercial CAT tools  
✅ **Superior widgets** - Better components than tkinter can offer  

**User verdict:** "ok, this is MUCH better"

---

## Versioning Strategy

### Dual-Track Development

We will maintain **two separate programs** during migration:

#### **Supervertaler_v3.7.x.py** (tkinter - Maintenance Mode)
- **Purpose:** Stable production version
- **Changes:** Bug fixes only, no new features
- **Versioning:** Continue 3.7.x numbering (3.7.7, 3.7.8, etc.)
- **Timeline:** Maintained until Qt version reaches feature parity
- **Status:** Current working version with all features

#### **Supervertaler_Qt_v1.x.py** (PyQt6 - Active Development)
- **Purpose:** Future production version
- **Changes:** New features, progressive migration
- **Versioning:** Start from v1.0.0, increment as features are added
- **Timeline:** Progressive development, no rush
- **Status:** Clean slate, professional foundation

### Version Numbering

**Qt Version Format:** `Supervertaler_Qt_v1.MINOR.PATCH.py`

- **v1.0.0** - Phase 1: Core infrastructure
- **v1.1.0** - Phase 2: Project management
- **v1.2.0** - Phase 3: File import/export
- **v1.3.0** - Phase 4: Translation Memory
- **v1.4.0** - Phase 5: Advanced features
- **v2.0.0** - Full feature parity + new Qt-exclusive features

---

## Migration Phases

### Phase 1: Core Infrastructure ✅ **COMPLETE (v1.0.0)**

**Status:** Implemented in `Supervertaler_Qt_v1.0.0.py`

**Features:**
- ✅ Main window with menu system
- ✅ Professional toolbar with font controls
- ✅ Translation grid (QTableWidget)
- ✅ Perfect auto-resize functionality
- ✅ Segment display and editing
- ✅ Project loading (JSON format)
- ✅ Status bar and logging
- ✅ Assistance panel structure (TM, Notes)
- ✅ Recent projects menu framework

**Deliverables:**
- Working Qt application
- Load existing project files
- Edit translations in grid
- Auto-resize rows to content
- Save projects

**Estimated Time:** ✅ Complete

---

### Phase 2: Project Management (v1.1.0 - v1.2.0)

**Target:** v1.1.0 for basic, v1.2.0 for advanced

#### v1.1.0 - Basic Project Features

**Features to Migrate:**
- ✅ New project dialog (language selection, metadata)
- ✅ Project properties editor
- ✅ Recent projects tracking (fully functional)
- ✅ Project statistics (word count, segment count, completion %)
- ✅ Segment status management (untranslated → draft → translated → approved)

**From tkinter code:**
- `new_project()` - Project creation
- `load_project()` - Enhanced with metadata
- Recent projects JSON handling
- Project statistics calculations

**Estimated Time:** 2-3 days

#### v1.2.0 - Import/Export

**Features to Migrate:**
- Import DOCX (plain, memoQ-preprocessed, Trados-tagged)
- Import MQXLIFF
- Export to DOCX (translated)
- Export to TMX
- Export to Excel (bilingual review)

**From tkinter code:**
- `modules/docx_handler.py` - DOCX import/export
- `modules/cafetran_docx_handler.py` - CafeTran format
- `modules/trados_docx_handler.py` - Trados format
- `modules/mqxliff_handler.py` - memoQ XLIFF
- `modules/tmx_generator.py` - TMX export

**Estimated Time:** 3-5 days

---

### Phase 3: Translation Memory (v1.3.0)

**Features to Migrate:**
- TM storage (JSON-based database)
- TM search (fuzzy matching)
- TM matches display in assistance panel
- Insert TM match into target
- TM management (import, export, clean)
- Auto-propagation of exact matches

**From tkinter code:**
- `modules/translation_memory.py` - Core TM engine
- TM search algorithms
- Match scoring (100%, 95%, 90%, etc.)
- TM panel in assistance area

**Qt Improvements:**
- Better TM panel with clickable matches
- Visual similarity highlighting
- TM statistics visualization
- Faster search with better UI feedback

**Estimated Time:** 4-6 days

---

### Phase 4: Advanced Translation Features (v1.4.0 - v1.6.0)

#### v1.4.0 - AI & Prompt Assistant

**Features to Migrate:**
- AI Prompt Assistant (ChatGPT/Claude integration)
- Prompt library management
- Context-aware AI suggestions
- API key management

**From tkinter code:**
- `modules/prompt_assistant.py` - AI integration
- `modules/prompt_library.py` - Prompt management
- API configuration

**Qt Improvements:**
- Better prompt editor with syntax highlighting
- Drag-and-drop prompt organization
- AI response preview panel

**Estimated Time:** 3-4 days

#### v1.5.0 - Document Analysis & Tools

**Features to Migrate:**
- Document analyzer (structure detection)
- Find & Replace (with regex)
- Tag manager (XML/HTML tags)
- Figure context manager
- Tracked changes handler

**From tkinter code:**
- `modules/document_analyzer.py`
- `modules/find_replace.py`
- `modules/tag_manager.py`
- `modules/figure_context_manager.py`
- `modules/tracked_changes.py`

**Qt Improvements:**
- Better Find & Replace dialog with live preview
- Visual tag highlighting in grid
- Document structure tree view

**Estimated Time:** 4-5 days

#### v1.6.0 - Specialized Tools

**Features to Migrate:**
- PDF Rescue (extract text from PDFs)
- Encoding repair tool
- Simple segmenter
- Setup wizard for first run

**From tkinter code:**
- `modules/pdf_rescue.py`
- `modules/encoding_repair.py`
- `modules/simple_segmenter.py`
- `modules/setup_wizard.py`

**Estimated Time:** 3-4 days

---

### Phase 5: View Modes & Workflow (v1.7.0 - v1.8.0)

#### v1.7.0 - Multiple View Modes

**Current tkinter has 3 view modes:**
1. **Grid View** - memoQ-style grid (like our Qt v1.0.0)
2. **List View** - Treeview list with editor panel below
3. **Document View** - Continuous flow document

**Qt Implementation:**
- Grid View (already done in v1.0.0)
- List View - QTreeWidget with QTextEdit panel
- Document View - QTextEdit with segment markers
- Quick view switching (Ctrl+1, Ctrl+2, Ctrl+3)

**Qt Improvements:**
- Smoother view transitions
- Remember view preferences per project
- Better document flow rendering

**Estimated Time:** 5-7 days

#### v1.8.0 - Advanced Workflow

**Features to Migrate:**
- Filtering (by status, content, date)
- Sorting (by ID, length, status)
- Batch operations (mark all as translated, etc.)
- Segment splitting/merging
- Comments and notes system
- Style guide integration

**From tkinter code:**
- Filter/sort logic from all views
- `modules/style_guide_manager.py`
- Batch operation handlers

**Qt Improvements:**
- Advanced filter builder UI
- Visual batch operation preview
- Better style guide panel with live search

**Estimated Time:** 4-6 days

---

### Phase 6: Configuration & Polish (v1.9.0 - v2.0.0)

#### v1.9.0 - Settings & Preferences

**Features:**
- Comprehensive settings dialog
- Keyboard shortcuts customization
- Theme/appearance customization (Qt stylesheets!)
- Plugin architecture foundation
- Auto-save and backup configuration

**Qt Improvements:**
- Professional multi-page settings dialog
- Dark mode support
- Custom color schemes
- Keyboard shortcut conflict detection

**Estimated Time:** 3-5 days

#### v2.0.0 - Feature Parity + Qt Exclusives

**Feature Parity:**
- All tkinter v3.7.x features migrated
- All modules functional
- Comprehensive testing
- User documentation

**Qt-Exclusive Enhancements:**
- **Tabbed projects** - Work on multiple projects simultaneously
- **Split screen** - Compare two documents side-by-side
- **Advanced TM visualization** - Charts, graphs, statistics
- **Better PDF handling** - Native PDF preview
- **Improved AI panel** - Streaming responses, better formatting
- **Cloud integration** - Optional cloud TM/project storage
- **Plugin system** - Community-developed extensions

**Estimated Time:** 2-3 weeks (includes testing)

---

## Feature Comparison Matrix

| Feature | tkinter v3.7.x | Qt v1.0.0 | Qt v2.0.0 (Planned) |
|---------|---------------|-----------|---------------------|
| **Grid Display** | ⚠️ Acceptable | ✅ Excellent | ✅ Perfect |
| **Auto-sizing** | ⚠️ Approximation | ✅ Perfect | ✅ Perfect |
| **Font Rendering** | ⚠️ Fuzzy | ✅ Sharp | ✅ Sharp |
| **Speed (1000 segments)** | ⚠️ Slow | ✅ Fast | ✅ Blazing |
| **Memory Usage** | ⚠️ High | ✅ Lower | ✅ Optimized |
| **UI Customization** | ❌ Limited | ✅ Good | ✅ Extensive |
| **Native Look** | ❌ No | ✅ Yes | ✅ Yes |
| **Tabbed Projects** | ❌ No | ❌ Not yet | ✅ Yes |
| **Dark Mode** | ❌ No | ❌ Not yet | ✅ Yes |
| **Plugins** | ❌ No | ❌ Not yet | ✅ Yes |

---

## Code Reuse Strategy

### What Stays the Same (70% of codebase)

**Business Logic Modules** (no changes needed):
- ✅ `modules/translation_memory.py` - TM engine
- ✅ `modules/docx_handler.py` - DOCX processing
- ✅ `modules/mqxliff_handler.py` - XLIFF processing
- ✅ `modules/tmx_generator.py` - TMX generation
- ✅ `modules/prompt_assistant.py` - AI logic
- ✅ `modules/config_manager.py` - Configuration
- ✅ Data models (`Segment`, `Project` classes)

**What Changes:** Only the UI calls these modules instead of tkinter

### What Needs Rewriting (30% of codebase)

**UI Layer Only:**
- tkinter widgets → PyQt6 widgets
- Grid/List/Document views → Qt equivalents
- Dialogs → Qt dialogs
- Event handlers → Qt signals/slots

**No logic duplication** - Just new UI connecting to same modules

---

## Development Workflow

### Recommended Approach

1. **Start with Qt v1.0.0** (already done! ✅)
2. **Test with real projects** - Load your actual translation projects
3. **Identify next priority feature** - What do you miss most from tkinter?
4. **Migrate that feature** - Implement in Qt
5. **Increment version** - v1.0.0 → v1.1.0 → v1.2.0...
6. **Repeat** until feature parity
7. **Add Qt-exclusive features** for v2.0.0

### No Rush Philosophy

> "I don't mind working on this for a very long time. I just want the app to eventually be as good as it possibly can be."

**This means:**
- ✅ Quality over speed
- ✅ One feature at a time
- ✅ Test thoroughly before moving on
- ✅ Keep tkinter version as fallback
- ✅ No pressure, no deadlines
- ✅ Enjoy the process

---

## Risk Mitigation

### Challenges & Solutions

| Challenge | Risk Level | Mitigation |
|-----------|-----------|------------|
| **Time investment** | 🟡 Medium | No deadline, work at your pace |
| **Learning Qt** | 🟢 Low | Similar to tkinter, good docs |
| **Missing tkinter features** | 🟢 Low | Keep tkinter v3.7.x as fallback |
| **Project file compatibility** | 🟢 Low | Same JSON format |
| **User confusion** | 🟢 Low | Clear naming (v3.7.x vs Qt v1.x) |
| **Module integration** | 🟢 Low | Modules already decoupled |

**Overall Risk:** 🟢 **LOW** - Very safe migration path

---

## Success Criteria

### Phase 1 Success (v1.0.0) ✅
- ✅ Qt app runs and loads projects
- ✅ Grid displays with perfect auto-sizing
- ✅ Fonts are sharp and crisp
- ✅ Can edit and save translations
- ✅ User prefers Qt grid over tkinter

**Status:** ✅ **ACHIEVED** - "ok, this is MUCH better"

### Phase 2 Success (v1.1-1.2)
- Can create new projects from scratch
- All import formats work (DOCX, MQXLIFF)
- All export formats work (DOCX, TMX, Excel)
- Recent projects fully functional

### Final Success (v2.0.0)
- All tkinter features migrated
- Qt performs better in every way
- Users prefer Qt version exclusively
- tkinter version deprecated

---

## Effort Estimation

### Total Development Time

**Conservative Estimate:**
- Phase 1: ✅ 1 day (complete)
- Phase 2: 1 week
- Phase 3: 1 week
- Phase 4: 2 weeks
- Phase 5: 2 weeks
- Phase 6: 3 weeks

**Total: 8-10 weeks full-time**

**But since you're working at your own pace:**
- **Part-time (2-3 hours/day):** 4-6 months
- **Weekend project:** 6-12 months
- **Whenever you feel like it:** 1-2 years

**And that's perfectly fine!** The tkinter version works meanwhile.

---

## Next Steps

### Immediate Actions (This Week)

1. ✅ **Remove Grid2 from tkinter version** - Done!
2. ✅ **Create Supervertaler_Qt_v1.0.0.py** - Done!
3. ✅ **Write migration plan** - You're reading it!
4. ⏳ **Test Qt v1.0.0 with real projects** - Next!
5. ⏳ **Identify Phase 2 priority** - What feature do you need most?

### Recommended Next Feature

**Option A: Recent Projects (Quick Win)**
- Fully implement recent projects tracking
- Makes Qt immediately more useful
- ~2 hours of work

**Option B: Project Creation (Core Feature)**
- New project dialog
- Language pair selection
- Makes Qt self-sufficient
- ~4-6 hours of work

**Option C: DOCX Import (High Value)**
- Import your actual translation files
- Makes Qt production-ready for basic work
- ~1-2 days of work

**Your choice!** What would make Qt most useful to you right now?

---

## Conclusion

This migration is:

✅ **Technically sound** - Qt is proven better  
✅ **Low risk** - Keep tkinter as fallback  
✅ **Incremental** - One feature at a time  
✅ **High reward** - Professional-grade final product  
✅ **Your pace** - No deadlines, no pressure  

**You're not rewriting everything** - Just the UI layer (30% of code)  
**You're building something better** - Industry-standard CAT tool  
**You have time** - No rush, quality first  

The Qt v1.0.0 foundation is **solid**. Every feature you add from here makes it more powerful. By the time you reach v2.0.0, you'll have a CAT tool that rivals commercial products.

**Welcome to the Qt journey!** 🚀

---

## Questions & Decisions

### For You to Decide

1. **What's your next priority feature?**
   - Recent projects tracking?
   - Project creation dialog?
   - DOCX import?
   - Something else?

2. **How much time per week?**
   - Helps estimate realistic timeline
   - No pressure, just planning

3. **What features from tkinter do you use most?**
   - Helps prioritize migration order

4. **Any Qt-exclusive features you'd love?**
   - Dark mode?
   - Tabbed projects?
   - Better AI panel?
   - PDF preview?

---

**Document End** - Ready to build the future! 🎯
