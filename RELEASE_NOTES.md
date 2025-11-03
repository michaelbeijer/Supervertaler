# Supervertaler Release Notes

## Current Release: v1.1.6-Qt (November 3, 2025)

### What's New

**Detachable Universal Lookup** 🔍 (NEW!)
- **Multi-Screen Support:** Open Universal Lookup in a separate window for multi-monitor workflows
- **Flexible Workflow:** Keep your translation project on one screen while using Universal Lookup on another
- **Easy Detach/Reattach:** One-click detach button on Home tab, seamless reattach functionality
- **Smart Positioning:** Automatic window positioning that works correctly with multiple monitors
- **Improved Home Tab:** Universal Lookup prominently featured on Home screen for instant access

**Previous Release (v1.1.5): Multiple View Modes** 🎨

### What's New

**Multiple View Modes** 🎨
- **Three Ways to Work:** Choose the view that fits your workflow
  - **Grid View (Ctrl+1):** Spreadsheet-style table - perfect for fast segment-by-segment editing
  - **List View (Ctrl+2):** Segments list with dedicated editor panel - ideal for focused translation
  - **Document View (Ctrl+3):** Natural document flow with clickable segments - great for review
- **View Switcher Toolbar:** Quick buttons to switch between views instantly
- **Keyboard Shortcuts:** Ctrl+1, Ctrl+2, Ctrl+3 for rapid view switching
- **Synchronized Views:** All three views share the same project data - changes in one view instantly appear in others
- **Translation Results Pane:** Now available in all views - TM, LLM, MT, and Termbase matches always accessible

**Previous Release (v1.1.4): Encoding Repair Tool** 🔧

### What's New

**Encoding Repair Tool** 🔧 (NEW!)
- **Full Port from Tkinter:** Complete encoding corruption detection and repair functionality
- **Detect & Fix Mojibake:** Automatically repairs UTF-8 text incorrectly decoded as Latin-1/Windows-1252
- **File & Folder Support:** Scan single files or entire folders recursively
- **Automatic Backups:** Creates `.backup` files before repair to ensure safety
- **Standalone Mode:** Run independently with `python modules/encoding_repair_Qt.py`
- **Embedded Mode:** Integrated as a tab in Supervertaler Qt
- **Test File Available:** `docs/tests/test_encoding_corruption.txt` for user testing
- **Clean Qt Interface:** Matches PDF Rescue and TMX Editor design patterns

**4-Layer Prompt Architecture** 🎯 (Previous Release - v1.1.3)
- **Revolutionary Prompt Management:** Unique layered approach for maximum translation precision
- **Layer 1 - System Prompts:** Editable infrastructure (CAT tags, formatting rules, language conventions)
- **Layer 2 - Domain Prompts:** Domain-specific expertise (Legal, Medical, Technical, Financial, etc.)
- **Layer 3 - Project Prompts:** Client and project-specific instructions
- **Layer 4 - Style Guides:** Language-specific formatting guidelines
- **Prompt Assistant:** AI-powered prompt refinement using natural language (unique to Supervertaler!)
- **Beautiful UI:** Color-coded layer interface with activation system and preview
- **Full Integration:** Standardized headers matching other modules (TMX Editor, PDF Rescue)

**Previous Release (v1.1.0): TMX Editor - Professional Translation Memory Editor** 🎉
- **Database-Backed Large File Support:** Handle massive TMX files (1GB+) efficiently with SQLite backend
- **Dual Loading Modes:** Choose RAM mode (fast for small files) or Database mode (handles any size)
- **Smart Auto Mode:** Intelligently selects best loading method based on file size thresholds
- **Heartsome-Inspired UI:** Three-panel layout with top header (language selectors + filters), center grid, and right attributes panel
- **Inline Editing:** Edit source and target text directly in the grid - no popup dialogs needed
- **Real-time Highlighting:** Search terms highlighted with green background (Heartsome-style)
- **Advanced Filtering:** Case-insensitive search with tag filtering support
- **Efficient Pagination:** 50 TUs per page for smooth performance
- **Batch Operations:** Database commits every 100 TUs for 10-50x faster loading
- **Progress Indicators:** Clear progress bars with immediate display
- **Custom UI:** Consistent green checkmark style matching AutoFingers design

**Technical Improvements** ⚡
- New database tables: `tmx_files`, `tmx_translation_units`, `tmx_segments` with proper indexing
- Optimized transaction management for batch database operations
- Memory-efficient: Database mode frees RAM immediately after loading
- Automatic mode detection based on file size (50MB/100MB thresholds)

**Previous Release (v1.0.2): UI Improvements & Bug Fixes** ✅

### What's New

**UI Improvements & Bug Fixes** ✅
- Fixed broken emoji icons in tab labels (Termbases 🏷️, Prompt Manager 💡, Encoding Repair 🔧, Tracked Changes 🔄)
- Improved checkbox styling with custom green checkboxes and white checkmarks
- Better small-screen support with reorganized AutoFingers layout
- Activity Log moved to right side for improved space utilization

**New Features** ✨
- **Startup Settings:** Option to automatically restore last opened project on startup (Tools → Options → General)
- **Font Size Persistence:** New settings panel to save and restore all font sizes:
  - Grid font size (source/target columns)
  - Translation results match list font size
  - Translation results compare boxes font size
- **Auto-Save:** Font sizes automatically saved when adjusted via zoom keyboard shortcuts

**Previous Release (v1.0.1): Termbases Feature Complete** ✅
- Full termbase CRUD operations (Create, Read, Update, Delete)
- Multiple termbases per project with independent term sets
- Global and project-specific termbase scopes
- Sample data with 3 test termbases (48 terms total)

**Terminology Standardization**
- All references standardized to "Termbase" (single word)
- Consistent terminology throughout UI and codebase
- Eliminated ambiguity between "glossary" vs "termbase"

### Key Improvements

- **User Preferences:** Font sizes and startup behavior now persist across sessions
- **Startup Experience:** Option to automatically reopen your last project on launch
- **UI Polish:** Custom checkbox styling for better visual feedback
- **Layout:** 2-column grid layout for AutoFingers Settings section
- **Responsive Design:** Improved rendering on smaller laptop displays
- **Database:** Fixed NOT NULL constraint errors on language fields (v1.0.1)
- **Code Quality:** Fixed method naming and Project object access patterns

### System Requirements

- **Python:** 3.8+
- **OS:** Windows, macOS, Linux
- **GUI Framework:** PyQt6
- **Database:** SQLite (built-in)

---

## Known Issues

- None reported for v1.0.2

---

## Deprecated Features

- **Tkinter Edition:** Now in maintenance mode. Features being ported to Qt Edition.

---

## Breaking Changes

None in this release.

---

## Upgrading

### From v1.0.1 to v1.0.2

No database migration required. Simply install the new version:

### From v1.0.0 to v1.0.1

No database migration required. Simply install the new version:

```bash
python Supervertaler_Qt.py
```

---

## Support

For questions or bug reports, see [PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) for development team information.

---

## Future Releases

### v1.1.0 (Planned)
- Terminology Search (Ctrl+P)
- Concordance Search (Ctrl+K)
- Enhanced create/edit dialogs

### v1.2.0 (Planned)
- TMX Editor with visual highlighting
- Advanced filtering
- Custom keyboard shortcuts

### v2.0.0 (Future)
- Full feature parity with Tkinter edition
- Tkinter deprecation

---

**Documentation:** See [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) for complete project information.

**Last Updated:** November 2, 2025
