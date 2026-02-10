# Supervertaler - Changelog

All notable changes to Supervertaler are documented in this file.

**Current Version:** v1.9.253 (February 11, 2026)


## v1.9.253 - February 11, 2026

### Improvements

- **macOS global hotkeys: Ctrl+Cmd+L / Ctrl+Cmd+M** — Global hotkeys for Superlookup and QuickTrans now use ⌃⌘L and ⌃⌘M on macOS (previously tried to register Ctrl+Alt which didn't work). Uses pynput with the correct key mapping. The in-app Superlookup shortcut also updated to ⌃⌘L on Mac.
- **macOS Accessibility permission guidance** — When global hotkeys fail to register on macOS, Supervertaler now prints a clear message directing users to grant Accessibility permission in System Settings → Privacy & Security → Accessibility.
- **Fixed Meta symbol display on macOS** — The `Meta` modifier now correctly displays as ⌃ (Control) instead of ⌘ (Command) in shortcut labels.

---

## v1.9.252 - February 11, 2026

### New Features

- **QuickTrans (Ctrl+Alt+M) now pastes translation at cursor** — When invoking QuickTrans from an external app (browser, Trados, text editor, etc.) and selecting a translation (1-9 or Enter), the selected translation is now copied to the clipboard AND pasted at the cursor position in the original app, replacing the selected text. Works cross-platform: AHK/PowerShell on Windows, osascript on macOS, pynput on Linux.

### Bug Fixes

- **QuickTrans no longer flashes taskbar icon** — The QuickTrans popup now uses a Tool window type when invoked via the global hotkey, preventing the Supervertaler taskbar icon from flashing on Windows.
- **Trados bilingual review: self-closing tags now exported correctly** — Self-closing tags like `<255/>` (standalone elements such as page breaks) were written as plain text instead of with the Tag character style when exporting to Trados bilingual DOCX. Trados flagged these as tag errors on re-import. The tag regex now matches all three tag forms: opening (`<11>`), closing (`</11>`), and self-closing (`<255/>`).
- **Superlookup (Ctrl+Alt+L) now brings window to foreground** — When pressing Ctrl+Alt+L from another application (e.g. Trados Studio), the Supervertaler window now reliably comes to the foreground instead of just flashing in the taskbar. Uses platform-native window activation: `AttachThreadInput` + `SetForegroundWindow` on Windows, `osascript` on macOS, `wmctrl`/`xdotool` on Linux.

---

## v1.9.250 - February 10, 2026

### Bug Fixes

- **TM and Glossary preselection fixed for new projects** — When creating a new project (via any import method, including Trados bilingual DOCX), TMs and glossaries from the previous project were still shown as selected in the UI. The database was correctly deactivated but the TM/Glossary tab checkboxes were not refreshed. Now properly refreshes both panels after deactivation.

### Improvements

- **Trados Bilingual Review dialog updated** — Improved preparation instructions: replaced incorrect Ctrl+A shortcut (which doesn't work in Trados) with proper segment selection method (click first segment number, Shift+click last). Added new step explaining that Supervertaler's exported file must be renamed to match the original Trados export name for re-import.

---

## v1.9.249 - February 10, 2026

### Improvements

- **Trados return package now matches Studio output** — Compared against a genuine Trados Studio return package and aligned Supervertaler's output:
  - **Byte-perfect SDLXLIFF preservation** — Switched from ElementTree round-trip to text-based regex replacement. Preserves UTF-8 BOM, double-quote XML declaration, original namespace prefixes, and all whitespace exactly as in the original file. Only `<target>` content and `sdl:seg` attributes are modified.
  - **Source language SDLXLIFF included** — Return package now includes the `en-gb/` source SDLXLIFF (unchanged) alongside the translated `nl-nl/` target, matching Studio's structure.
  - **CreatedBy scoped correctly** — `PackageCreatedBy` is updated without clobbering `ManualTask.CreatedBy`, `FileVersion.CreatedBy`, and other unrelated `CreatedBy` attributes in the `.sdlproj`.
  - **AutomaticTask and TermbaseConfiguration stripped** — Removed from `.sdlproj` as Studio does, keeping return packages lean.

---

## v1.9.248 - February 10, 2026

### Bug Fixes

- **Trados return package (SDLRPX) overhaul** — Fixed four issues with return package generation:
  - **Inline tags corrupted on export** — `<g>` formatting tags (e.g. superscript ¹⁷⁷Lu) were escaped as literal text (`&lt;14&gt;177&lt;/14&gt;`) instead of proper XML elements. Tags are now correctly reconstructed, including alphanumeric IDs like `qSuperscript`.
  - **PackageType wrong** — `.sdlproj` was copied verbatim with `PackageType="ProjectPackage"` instead of `"ReturnPackage"`. Now correctly sets ReturnPackage, updates timestamps, CreatedBy, ConfirmationStatistics (Draft→Translated), and marks the ManualTask as Completed.
  - **Extra files in package** — Source language folder (`en-gb/`) and `Reports/` were included. Return packages now only contain `.sdlproj` + target language SDLXLIFF.
  - **Segment origin not updated** — Translated segments now get `origin="interactive"` with stale TM/MT attributes removed.

---

## v1.9.247 - February 10, 2026

### Bug Fixes

- **Trados/SDLXLIFF tag insertion (Ctrl+,) fixed** — The "Insert next tag" shortcut now recognizes Trados Studio numeric tags (`<92>`, `</92>`, etc.) from imported SDLXLIFF packages. Previously the tag extraction regexes only matched letter-starting tags (`<b>`, `</i>`) and silently ignored numeric tags. Wrapping selected text with Trados tag pairs also works now.

---

## v1.9.246 - February 9, 2026

### Bug Fixes

- **memoQ bilingual RTF: missing segments fixed** — Segments containing mqInternal inline tags (e.g. `[1]`, `[1}...{2]` paired tags) were silently dropped during import. The row-matching regex now uses brace-aware matching to handle nested RTF brace groups. Previously 11 of 155 segments were lost in affected files.
- **memoQ bilingual RTF: formatting preserved on export** — Bold, italic, and underline formatting is now correctly converted back to RTF control words (`\b`, `\i`, `\ul`) when exporting translations. Previously these appeared as literal `<b>`, `<i>`, `<u>` text when re-imported into memoQ.

---

## v1.9.245 - February 9, 2026

### New Features

- **Cross-platform support**: Added `modules/platform_helpers.py` with cross-platform utilities for file opening, subprocess flags, global hotkeys, and keystroke automation. Supervertaler now runs on macOS and Linux in addition to Windows.
- **Native global hotkey system**: Replaced the AutoHotkey-based hotkey system with a native implementation — Windows `RegisterHotKey` API with AHK-based keystroke injection for Ctrl+C, pynput `GlobalHotKeys` on macOS/Linux. No more signal file watcher or polling timer.
- **Global Hotkeys settings moved**: The Global Hotkeys (Superlookup & QuickTrans) settings section has moved from the General tab to the Keyboard Shortcuts tab.

### Improvements

- **Cross-platform file opening**: Replaced all unguarded `os.startfile()` calls with `platform_helpers.open_file()` (uses `open` on macOS, `xdg-open` on Linux).
- **Cross-platform subprocess flags**: Guarded all `subprocess.CREATE_NO_WINDOW` usage behind platform checks so voice commands and other subprocess calls work on macOS/Linux.
- **Renamed "Universal Lookup" to "Superlookup"** in the Keyboard Shortcuts action column, sidebar, and shortcut cheatsheet for consistency.

### Dependencies

- Added `pynput>=1.7.6` as a cross-platform dependency for global hotkeys and keystroke automation.

---

## v1.9.244 - February 9, 2026

### Bug Fixes

- **Add to Glossary defaults:** The "Save to Glossary(s)" checklist now defaults to active glossaries for the current project instead of stale previous selections.
- **Immediate Termview update after glossary add:** After Add/Quick Add, the in-memory termbase cache and index are rebuilt before refresh so newly added terms appear immediately in Termview.

---

## v1.9.243 - February 9, 2026

### Bug Fixes

- **Glossary Termview refresh (Match Panel):** Fixed a regression where adding terms via "Add to Glossary" or "Quick Add" saved correctly but did not immediately refresh Termview in the Match Panel. Refresh paths now update when either Termview widget is available.

---

## v1.9.242 - February 8, 2026

### UI Improvements

- **macOS shortcut labels**: Normalized user-facing shortcut text to native macOS symbols (⌘, ⌥, ⇧) across context menus, tooltips, insert hints, and shortcut settings displays.
- **Branding consistency**: Restored **QuickTrans** and **QuickMenu** capitalization across user-facing UI and documentation.

---
## v1.9.241 - February 8, 2026

### Bug Fixes

- **QuickTrans LLM API keys on macOS/custom data paths**: Fixed QuickTrans incorrectly reporting missing API keys for Claude, OpenAI, and Gemini when keys were present in the configured user data location. QuickTrans now uses the app's unified key loader (`parent_app.load_api_keys()`), supports Gemini `google`/`gemini` aliases consistently, and reuses shared LLM client wiring.
- **LLM key path resolution fallback**: Updated `modules/llm_clients.load_api_keys()` to read the cross-platform config pointer and resolve keys from the actual configured user data folder (`settings/settings.json`), with legacy fallbacks retained.

---

## v1.9.240 - February 8, 2026

### New Features

- **Unified settings system**: Merged `general_settings.json`, `ui_preferences.json`, `feature_settings.json`, and `api_keys.txt` into a single `settings/settings.json` file. All settings files (themes, shortcuts, find/replace history, etc.) are now organized in a `settings/` subfolder within the user data folder. Existing installations are automatically migrated on first launch — old files are renamed to `.migrated` as a safety net.
- **Inline API key editing**: API keys can now be entered directly in the Settings UI instead of editing a text file. AI provider keys (OpenAI, Claude, Google/Gemini, Ollama endpoint) are in the AI Settings tab; machine translation keys (Google Translate, DeepL, Microsoft, Amazon, ModernMT, MyMemory) are in the MT Settings tab. All key fields are password-masked with a show/hide toggle.

---

## v1.9.239 - February 8, 2026

### 🐛 Bug Fixes

- **macOS: tabs now left-aligned**: Fixed all tab bars (main tabs, settings sub-tabs, resource tabs, etc.) being centered/expanded on macOS. Qt's native `QMacStyle` ignores `setExpanding(False)`, so the app now uses the Fusion style on macOS which respects all Qt widget properties while keeping the app's custom stylesheets intact.
- **macOS: combo box dropdowns no longer blank**: Fixed a macOS Qt issue where QComboBox popup menus (pagination "Per page", language selectors, model dropdowns, etc.) rendered with blank/empty item text. The Fusion style renders combo items with Qt's own paint code instead of the native NSMenu.

---

## v1.9.237 - February 7, 2026

### ✨ New Features

- **Custom OpenAI-Compatible API profiles**: The custom provider now supports named profiles, allowing users to save multiple endpoint configurations (e.g., "Volcengine Doubao", "DeepSeek", "My Local vLLM") and switch between them from a dropdown in Settings > AI Settings. Each profile stores its own endpoint URL, model name, and API key (password-masked). Existing single-endpoint configurations are automatically migrated. The `api_keys.txt` `custom_openai` key still works as a fallback.

---

## v1.9.236 - February 7, 2026

### ✨ New Features

- **Custom OpenAI-Compatible API provider** ([#155](https://github.com/michaelbeijer/Supervertaler/issues/155)): Added support for any OpenAI-compatible API endpoint — Volcengine (Doubao), Alibaba Tongyi (Qwen), DeepSeek, Mistral, Groq, and more. Configure endpoint URL, model name, and API key in Settings > AI Settings. Works for single-segment translation, batch translation, and QuickTrans.

---

## v1.9.235 - February 7, 2026

### 🐛 Bug Fixes

- **Version display stuck at 1.9.227 for pip-installed users**: Fixed `_read_version()` to use `importlib.metadata` as a fallback when `pyproject.toml` is not present (pip wheels don't include it). Previously, all pip-installed users saw version 1.9.227 regardless of the actual installed version.

---

## v1.9.234 - February 7, 2026

### ✨ New Features

- **Multi-file export: "Original Format" option**: The multi-file export dialog now defaults to "Original Format", which exports each file back to its source format (`.txt`, `.md`, or `.docx`). This is especially useful for mixed-format projects where different files were imported with different types.

---

## v1.9.233 - February 7, 2026

### 🐛 Bug Fixes

- **Batch pre-translation: termbase glossary injection crashed with SQLite thread error**: Fixed "SQLite objects created in a thread can only be used in that same thread" error during batch translation. The worker thread was calling back to the main thread's SQLite connection to fetch AI-inject glossary terms. Terms are now pre-fetched on the main thread and passed to the worker.

---

## v1.9.232 - February 7, 2026

### ✨ New Features

- **Saved Views for multi-file projects**: Create named views that filter the translation grid to show only selected files. Views persist in the project file and are accessible from the file filter dropdown. Manage Views dialog allows creating and deleting views.
- **File boundary separators**: Multi-file projects now display a blue separator line between segments from different files, making it easy to see where one file ends and the next begins.
- **Markdown (.md) support in multi-file import/export**: Multi-file folder import now recognizes `.md` files alongside `.docx` and `.txt`. Multi-file export adds a Markdown format option that preserves syntax.

### 🔧 Improvements

- **Tabbed Project Info dialog**: The Project Info dialog now uses a tabbed layout with Overview and File Progress tabs. The standalone File Progress dialog has been merged in — click the file count in the status bar to jump directly to the File Progress tab.

---

## v1.9.231 - February 7, 2026

### 🐛 Bug Fixes

- **memoQ Bilingual RTF: Quotation marks, Unicode characters, and special characters lost during import**: Fixed a bug where Unicode escapes (`\uc0\u8220`, `\uc0\u8221`, etc.) and RTF character control words (`\ldblquote`, `\rdblquote`, etc.) were stripped by the generic control word cleanup regex, causing quotation marks to disappear and adjacent text to concatenate (e.g. `"de" en "het" refereren` became `deen hetrefereren`). All Unicode escapes, hex escapes, and named character control words are now decoded before the generic strip.
- **memoQ Bilingual RTF: Combined formatting (bold+underline) not extracted for headings**: The pair-matching regex `[^\\]+` could not match text containing other formatting control words, so segments with combined `\b \ul TEXT\b0 \ul0` (e.g. headings) lost all formatting. Replaced with direct marker-to-tag conversion that handles any combination of bold, italic, and underline.
- **memoQ Bilingual RTF: Missing formatting options dialog**: The RTF import was skipping the "memoQ Bilingual Import Options" dialog (Ignore inline formatting / Smart formatting transfer) that the DOCX import shows. The dialog is now shown for RTF imports as well, and the tag view is auto-enabled when smart formatting is selected.

---

## v1.9.228 - February 7, 2026

### 🐛 Bug Fixes

- **TM Read/Write settings now persist correctly across restarts** (#143): Fixed a bug where TM activation (Read checkbox) and write status (Write checkbox) could revert to wrong values after closing and reopening a project. The root cause was stale global TM activations overriding project-specific settings. Project-specific TM settings now always take priority over global defaults.

## v1.9.227 - February 7, 2026

### 🎨 UI Improvements

- **Settings Panel Reorganized** : The "AI Translation Preferences" settings section has been reorganized with clear sub-headings: *Single-Segment Translation*, *Batch Translation*, *Translation Memory*, and *Document Context*. Previously these were mixed together without clear grouping.
- **TM Check Label Corrected**: The "Check TM before AI translation" setting was incorrectly labeled as applying only to single-segment translation. It actually applies to both single-segment and batch translation, and the label now reflects this.

### 🔧 Internal

- **Version auto-read from pyproject.toml**: `__version__` in Supervertaler.py now reads automatically from `pyproject.toml`, eliminating a manual version sync step.

---

## v1.9.226 - February 6, 2026

### 🐛 Bug Fixes

- **Import Dialogs Ignore Saved Language Pair** ([#143](https://github.com/michaelbeijer/Supervertaler/issues/143)): Fixed the Text/Markdown import dialog and Folder/multi-file import dialog always defaulting to English → Dutch, ignoring any previously saved language pair. Both dialogs now read and save the last used language pair from `general_settings.json`, matching the existing DOCX import behavior. All three import dialogs now share the same language memory.

---

## v1.9.225 - February 6, 2026

### 🐛 Bug Fixes

- **WYSIWYG/Tags Toggle Corrupts Target Text** ([#142](https://github.com/michaelbeijer/Supervertaler/issues/142)): Fixed the WYSIWYG/Tags view mode toggle permanently destroying whitespace and indentation in target text. The root cause was that `get_formatted_html_display()` generated HTML without whitespace preservation, so Qt's HTML renderer collapsed spaces and indentation. Switching back to Tags mode then showed the corrupted text. Fix: added `white-space: pre-wrap` CSS to the HTML output, and added `_suppress_target_change_handlers` guard during display mode refresh to prevent any edge-case data corruption.

---

## v1.9.224 - February 6, 2026

### 🐛 Bug Fixes

- **Per Page Dropdown Empty on macOS** ([#136](https://github.com/michaelbeijer/Supervertaler/issues/136)): Fixed the "Per page" dropdown in the grid toolbar appearing empty on macOS. The dropdown popup (`QComboBox QAbstractItemView`) had no explicit styling, causing macOS to render text as invisible against the platform-default background. Added explicit background, text color, and selection styling for dropdown popups.

---

## v1.9.223 - February 6, 2026

### ✨ New Features

- **memoQ Bilingual RTF Support** ([#145](https://github.com/michaelbeijer/Supervertaler/issues/145)): Added full import/export support for memoQ bilingual RTF files. This enables users with older memoQ versions (or those who prefer RTF) to use the same bilingual table workflow as DOCX. The RTF format uses the identical 5-column structure (ID, Source, Target, Comment, Status) as DOCX.
  - New menu options: File → Import → memoQ Bilingual Table (RTF)
  - New menu options: File → Export → memoQ Bilingual Table - Translated (RTF)
  - Preserves formatting (bold, italic, underline) from source segments
  - Handles Unicode text and special characters correctly

---

## v1.9.222 - February 5, 2026

### 🐛 Bug Fixes

- **"Exact matches only" Not Finding 100% Matches** ([#140](https://github.com/michaelbeijer/Supervertaler/issues/140)): Fixed batch TM pre-translation with "Exact matches only" option not finding 100% matches even when they exist. The bug was caused by `TMDatabase.get_exact_match()` returning only the target text (string) while the batch translation code expected a dictionary. Now returns the full match dictionary, allowing exact match mode to work correctly.

---

## v1.9.221 - February 5, 2026

### 🐛 Bug Fixes

- **TM Not Working After Re-import** ([#140](https://github.com/michaelbeijer/Supervertaler/issues/140)): Fixed Translation Memory not working after re-importing the same document. The root cause was that re-importing created a new project with a new ID, orphaning the TM activation records from the previous project ID. Now when re-importing the same file, users are prompted with a dialog offering two options:
  - **"Re-import into Current Project"**: Preserves the project ID and TM/glossary settings, ensuring TM continues to work
  - **"Create New Project"**: Creates a fresh project with clean slate (no TMs/glossaries pre-selected)

### ✨ Enhancements

- **Re-import Confirmation Dialog**: Added user-friendly confirmation dialog when importing a file that's already loaded in the current project. Applies to all import handlers: DOCX, memoQ bilingual, memoQ XLIFF, CafeTran, Trados, and TXT/Markdown.

---

## v1.9.220 - February 5, 2026

### 🐛 Bug Fixes

- **Reverted Auto-Activation of TMs**: Reverted incorrect fix from v1.9.219 that auto-activated all TMs when importing documents. The intended design is that new projects start with a **clean slate** - no TMs or glossaries pre-selected. Users should explicitly choose which resources to use for each project.

---

## v1.9.219 - February 5, 2026

### 🐛 Bug Fixes

- **Status Tooltip Rendering**: Fixed status icon tooltips appearing as black rectangles. Qt's built-in tooltip system was being affected by transparent widget backgrounds and theme stylesheets. The fix uses a custom QLabel popup widget with explicit styling (#f5f5f5 background, #333333 text), completely bypassing Qt's QToolTip system.

---

## v1.9.217 - February 4, 2026

### 🐛 Bug Fixes

- **Status Tooltip Rendering (partial)**: Attempted fix for black tooltip issue using `QToolTip.showText()`. This approach was insufficient; see v1.9.218 for the complete fix.

---

## v1.9.216 - February 4, 2026

### ✨ Enhancements

- **Status Icon Tooltips**: Hovering over status icons in the grid now displays tooltips showing the status name (e.g., "Not started", "Translated", "Confirmed"). Match percentage badges also show tooltips with details like "Context match from memoQ (101% or better)" or "Exact match from memoQ (100%)".

- **Standardized "Not started" Terminology**: The Quick Filter menu now uses "Not started" instead of "Not translated" to match the terminology used elsewhere in the application (Grid, Advanced Filters, menus). This aligns with memoQ's terminology and provides consistency throughout the UI.

---

## v1.9.215 - February 4, 2026

### 🐛 Bug Fixes

- **Quick Filters Not Working on macOS** ([#137](https://github.com/michaelbeijer/Supervertaler/issues/137)): Fixed Quick Filters (Empty segments, Not translated, Confirmed, Locked, Not locked, Commented) not working properly on macOS. The issue was that quick filters weren't integrating with the pagination system, causing any UI refresh event to override the filter. Now quick filters use the same mechanism as text filters, ensuring they persist correctly across all platforms. Additionally, the segment count label now shows the filtered count (e.g., "Showing 42 of 430 segments") when a filter is active.

---

## v1.9.214 - February 3, 2026

### ✨ Enhancements

- **DOCX Export Language Setting**: Exported target DOCX documents now have the correct language setting based on the project's target language. Previously, exported documents defaulted to American English regardless of the translation language pair. Now, when exporting EN→NL translations, the document language is correctly set to Dutch (Netherlands), enabling proper spellcheck and proofing in Word and other applications.

---

## v1.9.213 - February 3, 2026

### 🐛 Bug Fixes

- **Wrapping Tags in TM and TMX Export**: Fixed structural wrapping tags (e.g., `<li-b>`, `<li-o>`, `<p>`, `<td>`) being saved to Translation Memory and exported TMX files even when "Hide outer wrapping tags" was enabled in settings. All TM save and TMX export functions now properly strip these tags when the setting is active, improving TM leverage and ensuring cleaner exports.

---

## v1.9.212 - February 3, 2026

### 🐛 Bug Fixes

- **QuickTrans Project Languages**: Fixed QuickTrans not using the current project's source/target languages for MT and LLM providers. Now directly reads from `current_project.source_lang` and `current_project.target_lang` when a project is open, ensuring the correct language pair is sent to all translation providers.

---

## v1.9.211 - February 3, 2026

### 🐛 Bug Fixes

- **Batch Translate: Exact Matches Only**: Fixed the "Exact matches only" option in Batch Translate not finding any TM matches. The issue was that exact matching used hash comparison, but the hash didn't account for HTML/XML tags that may differ between stored TM entries and the search text. Now the exact match function tries multiple hash variants (with/without tags, normalized) to reliably find matches.

---

## v1.9.210 - February 3, 2026

### 🐛 Bug Fixes

- **Alt+0 TM Insert Shortcut**: Fixed the Alt+0 shortcut not inserting the TM target from the Match Panel. The shortcut previously only worked when the Match Panel tab was selected. Now it works regardless of which right panel tab is active, as long as there's a valid TM match displayed.

---

## v1.9.209 - February 3, 2026

### 🐛 Bug Fixes

- **TM/Glossary Auto-Selection on Startup**: Fixed an issue where Translation Memories and Glossaries were being auto-selected (both Read and Write checkboxes) when starting the application without a project open. Now when no project is loaded, all TMs and glossaries remain unselected as expected.

---

## v1.9.208 - February 3, 2026

### 🐛 Bug Fixes

- **DOCX Import: Hyperlink Text Missing**: Fixed an issue where text inside hyperlinks was being stripped during DOCX import. The `paragraph.text` property in python-docx doesn't include text from `w:hyperlink` elements. Now both `TagManager.extract_runs()` and `DOCXHandler.import_docx()` properly extract text from hyperlink elements, ensuring URLs and linked text are preserved.

---

## v1.9.207 - February 3, 2026

### 🔧 Maintenance

- **Version Sync**: Synchronized version number across pyproject.toml, Supervertaler.py, and PyPI package.

---

## v1.9.206 - February 3, 2026

### 🐛 Bug Fixes

- **AI Assistant Prompt Generation**: Fixed "Analyze Project & Generate Prompts" outputting placeholder text like `[Source Language]` and `[Translation]` instead of actual values. The template now pre-fills the actual language pair and segment count from project settings, with explicit instructions to not use placeholders.

---

## v1.9.205 - February 3, 2026

### 🐛 Bug Fixes

- **CRITICAL: Project Segments Corruption Fixed**: Fixed a critical bug where importing a new document would save the OLD project's segments instead of the newly imported ones. This affected all import functions (DOCX, text, memoQ, Trados, SDL package, Phrase, CafeTran, Déjà Vu). The issue was that `_original_segment_order` wasn't being updated after imports, causing the save function to overwrite new segments with old ones.

- **QuickTrans Language Mapping**: Fixed QuickTrans not respecting project source/target language settings. Machine translation providers (MyMemory, DeepL, Microsoft, ModernMT) now correctly map language names like "English" and "Dutch" to ISO codes.

- **Focus Rectangles Removed**: Fixed dotted focus rectangles appearing on buttons throughout the application. Added global stylesheet rules in theme manager and individual button fixes where custom stylesheets were used.

### ✨ Improvements

- **AI Assistant TM/Termbase Integration**: The "Click to include TM data" and "Click to include termbase data" buttons in the AI Assistant are now functional. Clicking toggles inclusion of TM matches and termbase entries in AI context.

- **AI Actions Error Messages**: Enhanced error messages for AI action debugging, showing received parameters when prompt creation fails.

---

## v1.9.204 - February 3, 2026

### 🐛 Bug Fixes

- **DOCX Export: Font Preservation**: Fixed an issue where exported DOCX files would lose the original font name (e.g., Verdana) and font size (e.g., 10pt). The export now correctly preserves font properties from the original document.

- **DOCX Export: All Caps Preservation**: Fixed an issue where text with the "All Caps" font effect (like patent titles) would export in normal case instead of uppercase. The `all_caps` font property is now preserved.

- **DOCX Export: Subscript/Superscript Support**: Fixed an issue where `<sub>` and `<sup>` formatting tags were not being processed during export. Text like "CO₂" now correctly exports with subscript formatting.

- **DOCX Export: Partial Replacement Formatting**: Fixed an issue where paragraphs containing multiple segments would lose all inline formatting (bold, italic, subscript, superscript) during export. Partial replacements now properly apply formatting tags.

### ✨ Improvements

- **Export Menu Reorganization**: Moved monolingual export formats (Target Only DOCX, Simple Text, AI-Readable Markdown) to the top of the Export menu with a separator, making them easier to find.

---

## v1.9.203 - February 3, 2026

### 🐛 Bug Fixes

- **Grid Row Height Stability**: Fixed an issue where row heights would become inconsistent ("messed up") after various actions like Ctrl+Enter confirmation, Clear Filters, or page navigation. Row heights are now properly recalculated:
  - After status cell updates (Ctrl+Enter confirmation)
  - After pagination/filter changes (sync + deferred resize)
  - After initial grid load (deferred resize for proper column widths)
  - After column resize (debounced handler for text reflow)

### ⚡ Performance Improvements

- **Faster Ctrl+Enter Navigation**: Removed wasteful MT/LLM API calls that were happening on every segment navigation. Machine translation providers (Google Translate, DeepL, Amazon, etc.) and LLM providers were being called even when the Translation Results panel was hidden. Now MT/LLM is only available via QuickTrans (Ctrl+M).

- **Removed Translation Results Panel**: The deprecated Translation Results panel has been removed from the UI. This panel was hidden by default with no way to enable it, but was still consuming resources. TM matching continues to work via the Match Panel, and MT/LLM translations are available via QuickTrans (Ctrl+M).

---

## v1.9.202 - February 2, 2026

### ✨ New Features

- **Clean TM Storage**: When "Hide outer wrapping tags" is enabled, structural tags like `<li-o>`, `<p>`, etc. are now stripped when saving to TM and when searching TM. This ensures better matching leverage - a segment `<li-o>Hello world</li-o>` will match a TM entry `Hello world` at 100%.

### 🐛 Bug Fixes

- **Find-and-Replace Tag Display**: Fixed an issue where outer wrapping tags would reappear in the grid after find-and-replace operations. All cell update operations now respect the "Hide outer wrapping tags" setting.

- **Preview Panel List Numbering**: Fixed claims/numbered lists starting at wrong number (e.g., claim #1 showing as "2." instead of "1."). The list counter now properly resets when starting a new list.

- **Preview Panel Line Breaks**: Ordered list items (like patent claims) now have proper paragraph-like spacing instead of running together.

- **Preview Section Headings**: Bold-wrapped section headings (like "CLAIMS", "TECHNICAL FIELD", "PRIOR ART") are now properly detected as headings with double line breaks before/after and bold formatting.

---

## v1.9.198 - February 2, 2026

### ✨ New Features

- **Hide Outer Wrapping Tags - Complete Implementation**: The "Hide outer wrapping tags" feature now works on **both Source and Target columns**. Tags are automatically restored when saving, making the process completely transparent to the translator.

- **WYSIWYG List Numbering & Bullets**: When "Hide outer wrapping tags" is enabled, list items now display with visual prefixes:
  - Ordered lists (`<li-o>`) show: "1. ", "2. ", "3. ", etc.
  - Unordered lists (`<li-b>`, `<li>`) show: "• "
  - These prefixes are display-only and don't affect the saved data

---

## v1.9.197 - February 2, 2026

### ✨ New Features

- **Hide Outer Wrapping Tags in Grid**: Added new option in View Settings → Grid Display Options to hide structural tags that wrap entire segments (like `<li-o>`, `<p>`, `<td>`). Since the segment type is shown in the Type column, these outer tags are redundant and can now be hidden for a cleaner grid display. Inner formatting tags like `<b>bold</b>` are preserved.

### 🐛 Bug Fixes

- **View Settings Now Preserves All Settings**: Fixed a bug where saving View Settings would overwrite unrelated settings in `general_settings.json`. Settings are now properly merged instead of replaced.

### 🏗️ UI Improvements

- **Match Panel Section Rename**: Renamed "Translation Results Pane & Tag Colors" to "Match Panel & Tag Colors" in View Settings to reflect the current UI terminology.

---

## v1.9.196 - February 2, 2026

### 🐛 Bug Fixes

- **AI Assistant "Analyze Project" Fixed** ([#132](https://github.com/michaelbeijer/Supervertaler/issues/132)): Fixed a bug where clicking "Analyze Project & Generate Prompts" in the AI Assistant would fail with "AI responded but no actions were found". The issue was that the LLM wasn't receiving a system prompt explaining the ACTION format. Now all providers (OpenAI, Claude, Gemini, Ollama) receive proper instructions on how to format their responses.

### 🎨 UI Improvements

- **Supervoice Settings Two-Column Layout**: Reorganized the Supervoice settings tab into a two-column layout. Voice commands table now displays on the right side, allowing more commands to be visible at once. Settings (Always-On Listening, Speech Recognition Model, AutoHotkey) remain on the left.

- **Green Checkmark Checkbox**: The "Enable voice commands" checkbox in Supervoice settings now uses the standard green checkmark style (CheckmarkCheckBox) for visual consistency with the rest of the application.

### 🏗️ Code Architecture

- **LLM Client System Prompt Support**: Added `system_prompt` parameter to the LLM client's `translate()` method and all provider-specific methods. This enables passing behavioral instructions to AI models for features like the AI Assistant.

---

## v1.9.195 - February 2, 2026

### 🏗️ Code Architecture

- **Module Rename**: Renamed `mt_quick_popup.py` → `quicktrans.py` to align with the QuickTrans branding. This prepares the module for future standalone distribution as a separate Windows executable.

---

## v1.9.194 - February 1, 2026

### 🎨 Branding & Naming

- **Tool Suite Naming**: Established consistent naming for Supervertaler's modular tools:
  - **Supervertaler** - Main CAT tool / translation workbench
  - **Superlookup** - Comprehensive research tool (TM, TB, MT, web, dictionaries)
  - **QuickTrans** - Instant translation popup (MT + LLM, GT4T-style)
  - **QuickMenu** - Quick access menu with various tools

- **QuickTrans** (formerly "MT Quick Lookup"): Renamed to better reflect that it provides instant translations from both MT engines AND LLMs. The tool can work standalone or integrated with Supervertaler.

- **Superlookup** (formerly "Superlookup"): Updated to CamelCase for consistency and readability. Now clearly distinguished from QuickTrans - Superlookup is for deep research, QuickTrans is for instant translations.

---

## v1.9.193 - February 1, 2026

### ✨ New Features

- **QuickTrans - LLM Support**: Added Claude, OpenAI (GPT), and Gemini as translation providers in QuickTrans. Now you can get translations from both MT engines AND LLMs in a single popup. Configure which providers to use in the QuickTrans settings (click the ⚙️ button in the popup).

- **Global QuickTrans Hotkey (Ctrl+Alt+M)**: Use QuickTrans from ANY application (memoQ, Word, browser, etc.) via AutoHotkey. Select text anywhere, press **Ctrl+Alt+M**, and the QuickTrans popup appears as an overlay at your cursor position - without switching focus to Supervertaler. Perfect for quick translations while working in your CAT tool.

- **QuickTrans Settings**: Added dedicated settings tab (Settings → QuickTrans) to configure:
  - Which MT engines to include (Google, DeepL, Microsoft, Amazon, ModernMT, MyMemory)
  - Which LLMs to include (Claude, OpenAI, Gemini) with model selection
  - Access settings directly from the popup via the ⚙️ button

### 🐛 Bug Fixes

- **View Settings Freeze Fixed**: Fixed a freeze that occurred when changing View settings (like "Termview under grid") and clicking "Save View Settings". The freeze was caused by TM saves being triggered for all confirmed segments during the update.

- **Termview Under Grid Default**: Changed "Termview/Session Log tabs under grid" to be OFF by default for new users. Setting is now properly persisted when changed.

---

## v1.9.192 - February 1, 2026

### ✨ New Features

- **QuickTrans (GT4T-style)**: Added a new popup window for instant translation suggestions, inspired by GT4T. Press **Ctrl+M** (default) or use the **right-click context menu** to open a popup showing translations from all enabled MT engines (Google Translate, DeepL, Microsoft Translator, Amazon Translate, ModernMT, MyMemory). Features include:
  - Source text displayed at the top for context
  - Numbered list of translation suggestions with provider badges
  - Press **1-9** to quickly insert a translation
  - Arrow keys to navigate, **Enter** to insert selected
  - **Escape** to dismiss
  - Translations fetched in parallel for fast results
  - Color-coded provider badges for easy identification
  - **Smart text selection**: If you have text selected in source or target, only that selection gets translated; otherwise translates the full source segment
  - Available from both source and target cell context menus ("⚡ QuickTrans")
  - **Resizable and movable**: Popup window can be dragged and resized to your preference
  - **Customizable shortcut**: Change the keyboard shortcut in Settings → Keyboard Shortcuts

---

## v1.9.191 - February 1, 2026

### 🎨 UI Improvements

- **Status Icon Enhancement**: Confirmed status checkmarks now display in green (#2e7d32) for better visual distinction. Status icons in rows with capitalized text no longer clip vertically.

- **Button Padding Standardization**: Unified button padding across all toolbar buttons (Show Invisibles, Advanced Filters, Sort, Clear Filters, Quick Filters, Spellcheck, etc.) to 3px vertical and 5px horizontal for consistent appearance and better text spacing.

- **Font Size Optimization**: Increased font size for segment numbers and type column symbols (¶, •, #1, H1, etc.) from size 8 to size 9 for better readability and visual proportion relative to grid content.

- **Column Width Optimization**: Segment number column now uses optimized width with reduced padding (12px total) and 55px maximum cap, accommodating up to 4-digit segment numbers (1-1000) without excess horizontal space.

---

## v1.9.190 - February 1, 2026

### 🎨 UI Improvements

- **Scrollbar Refinement**: Made main grid scrollbar narrower (12px) for cleaner appearance. Added visible triangle arrow icons to scrollbar buttons for better visual clarity. Removed custom floating precision scroll buttons for simpler interface.

- **Column Optimization**: Reduced Status column width from 60px to 50px to save horizontal space while maintaining full functionality. Changed table header font from bold to normal weight for more consistent typography.

### 🐛 Bug Fixes

- **Document Order Sort Fixed**: Document Order sort now correctly restores segments to their original sequence (1, 2, 3...) by sorting by segment ID. Previously, if segments were saved while sorted, the sorted order would become the "original" order, making it impossible to restore true document order.

- **Save/Load Order Preservation**: Projects now always save segments in original document order, not sorted order. When loading a project, sort state is reset to document order (no sort applied). This ensures consistent behavior and prevents sorted order from being permanently baked into project files.

---

## v1.9.189 - February 1, 2026

### 🎨 UI Improvements

- **Sort Progress Feedback**: Added progress dialog during sorting operations showing "Sorting segments, please wait..." message. Dialog only appears for operations taking longer than 500ms, providing clear user feedback without interrupting quick sorts on small projects. Automatically closes when sorting completes.

---

## v1.9.188 - February 1, 2026

### 🎨 UI Improvements

- **Sort Menu Styling**: Fixed sort dropdown menu to use clean white background matching Quick Filters menu style. Previous version incorrectly inherited orange button styling in menu items.

### ✨ Enhancements

- **Auto-Pagination on Sort**: Sorting now automatically sets pagination to "All" to display the complete sorted list. This prevents the confusing behavior where only the first page of sorted results would be visible. When you sort alphabetically, by length, by match rate, or any other criterion, you'll now see all sorted segments immediately.

---

## v1.9.187 - February 1, 2026

### ✨ New Features

- **Segment Sorting**: Added comprehensive sort dropdown button (⇅ Sort) in the toolbar, positioned after Advanced Filters. Similar to memoQ's sorting functionality, you can now sort segments by:
  - **Alphabetical**: Source/Target text (A → Z or Z → A)
  - **Text Length**: Source/Target (longer or shorter first)
  - **Match Rate**: TM match percentage (higher or lower first)
  - **Frequency**: Source/Target text occurrence count (higher or lower first)
  - **Last Changed**: Modification timestamp (newest or older first)
  - **Row Status**: Grouped by translation status (not started → draft → translated → confirmed)
  - **Document Order**: Reset to original document structure

  Sorting is applied to the entire project and reloads the grid to reflect the new order. The orange sort button with dropdown menu makes it easy to organize segments for review, identify patterns, or work systematically through similar content.

---

## v1.9.186 - February 1, 2026

### 🐛 Bug Fixes

- **Exit Crash Fixed**: Resolved Python crash that occurred when closing the program via File > Exit. The crash was caused by manual WebEngine cleanup interfering with Qt's internal shutdown sequence. Now lets Qt handle WebEngine cleanup naturally, resulting in clean program exit without crashes.

- **Import Shadowing Fixed**: Fixed UnboundLocalError crashes on startup caused by local imports shadowing global imports (QWidget, QHBoxLayout). Only QButtonGroup is now imported locally where needed.

### 🎨 UI Improvements

- **View Toggle Clarity**: Replaced confusing single "Tags OFF" toggle button with clear segmented control showing both "WYSIWYG" and "Tags" options. One button is always highlighted to show the current view mode.

- **Default View Mode**: Changed default view from WYSIWYG to Tags mode for better alignment with actual initial state. Tags button is now highlighted by default on startup.

---

## v1.9.185 - February 1, 2026

### 🎨 UI Improvements

- **Grid Zoom Shortcut**: Changed Grid Zoom In keyboard shortcut from Ctrl++ to Ctrl+= for easier access (no need to hold Shift). The = and + keys are on the same physical key, making this more intuitive and faster to use.

---

## v1.9.184 - February 1, 2026

### 🎨 UI Improvements

- **Dark Mode Refinements**: Improved text visibility in TermView panels (both bottom and right panel source text now use #FFFFFF for better contrast). HTML formatting tags (`<b>`, `</b>`, etc.) now display in light pink (#FFB6C1) in dark mode for enhanced readability.

- **TM Navigation Arrows**: Fixed navigation arrows in Match Panel and Compare Panel that were invisible or incorrectly rendered in dark mode. Now using crisp Unicode triangle symbols (◀ ▶) with theme-aware colors (white in dark mode, dark gray in light mode).

- **Table Header Font Size**: Reduced column header font size to match grid content (only bold, not larger), resulting in better visual proportions.

### 🐛 Bug Fixes

- **Prompt Library Updates**: Fixed Issue #112 where edited prompts were not immediately reflected in the Prompt Library or Preview Combined sections. Changes now update both the active primary prompt and attached prompts immediately after saving.

### 🛠️ Developer Experience

- **Windows Start Menu Shortcuts**: Added PowerShell scripts to create Start Menu shortcuts for both end users (`Supervertaler.exe`) and developers (`run.cmd`). Scripts are automatically included in release packages.

---

## v1.9.183 - January 31, 2026

### ⚡ Performance: Instant Ctrl+Enter Navigation

Major performance overhaul for segment navigation. Ctrl+Enter is now **instant** instead of taking 10-50+ seconds.

**In-Memory Termbase Index**
- Built a pre-indexed, in-memory glossary lookup system that replaces per-segment database queries
- Glossary lookups now take **<1ms** instead of **52 seconds** per segment
- Index is built once when project loads (~0.15s for 1,400 terms) and updated instantly when terms are added

**Async Auto-Confirm**
- The "auto-confirm 100% TM matches" feature now runs asynchronously
- Navigation completes instantly; TM lookup happens in the background
- If a 100% match is found, the segment is auto-confirmed after you've already moved

**Cache System Enabled by Default**
- Prefetch cache is now **enabled by default** for new installations
- Background workers pre-cache termbase and TM matches for upcoming segments
- Cache hit rate typically 95%+ after initial segment visit

### 🐛 Bug Fixes

- **TermView Updates on Ctrl+Enter**: The glossary/terminology panel now updates immediately when navigating with Ctrl+Enter, not just on mouse click

- **TM Panel Updates on Ctrl+Enter**: Translation Memory matches now appear immediately when navigating with Ctrl+Enter

- **Source Text Always Visible**: TermView now displays the source text even when there are no glossary matches, with appropriate status messages ("No matches in X words", "No glossaries activated", etc.)

- **Row Selection on Ctrl+Enter**: The target row is now properly selected (blue highlight) after Ctrl+Enter navigation, not just the previous row

- **TM Results for Correct Segment**: Fixed race condition where fast navigation could show TM results for the wrong segment; added segment validation before and after TM lookup

- **TM Lookup on Cache Hit**: Fixed issue where TM matches weren't shown when termbase was cached (prefetch worker skips TM for thread safety)

---

## v1.9.181 - January 30, 2026

### ✨ New Features

- **Expanded Language Support in New Project**: The New Project dialog now includes 53 languages (up from 10), matching the full list available in Settings. Languages now include Czech, Slovak, Romanian, Hungarian, and many more.

- **Global Language Sync**: When importing projects (memoQ, Trados, Phrase, XLIFF, etc.), the global language settings are now automatically synchronized with the imported project's source and target languages.

### 🎨 UI Improvements

- **TM/Glossary Activation Guidance**: When no TMs or glossaries are activated for a project, or when activated resources don't match the project's language pair, helpful guidance messages now appear in the Match Panel and Termview. Messages guide users to the Resources tab to activate appropriate resources.

---

## v1.9.180 - January 30, 2026

### ✨ New Features

- **Global UI Font Scale**: New user-configurable setting (50%-200%) that scales the entire application UI. Particularly useful for Linux/macOS users where Qt applications may render with smaller fonts, or for high-DPI displays. Find it in Settings → View → Global UI Font Scale.

---

## v1.9.178-beta - January 28, 2026

### 🐛 Bug Fixes

- **Slovak Language in Import Dialogs**: Slovak and other languages were missing from the Trados and Phrase import language dropdowns. Both dialogs now use the full language list matching the main New Project dialog.

- **mqxliff Target Loading for Pretranslated Files**: When importing pretranslated mqxliff files, the target translations were not being loaded. Added new `extract_bilingual_segments()` method to properly extract both source and target text from memoQ XLIFF files.

- **TM Activation for Global TMs**: Fixed issue where TMs created when no project was loaded would not save segments later. The TM activation system now properly handles global activations (project_id=0), so TMs activated before loading a project continue to work after a project is opened.

- **TM Storage Consistency**: The `get_writable_tm_ids`, `get_active_tm_ids`, and `is_tm_active` functions now include globally-activated TMs in addition to project-specific activations.

---

## v1.9.177-beta - January 28, 2026

### ✨ New Features

- **Bidirectional Termbase Matching**: Glossaries now work like memoQ and Trados - a termbase created for NL→EN will also find matches when working on EN→NL projects (and vice versa). This "direction-insensitive" behavior means you no longer need separate termbases for different language directions. When a match is found on the target side, source and target are automatically swapped in the results.

---

## v1.9.176-beta - January 28, 2026

### ✨ New Features

- **Unified Setup Wizard**: Combined the first-run data folder selection and features introduction into a single, streamlined wizard. New users now see a clear 2-step wizard (data folder → features), while existing users see a 1-step version with their current data folder displayed. The wizard is also accessible anytime from **Help → Setup Wizard**.

### 🎨 UI Improvements

- **Clickable Data Folder Path**: In the Setup Wizard, the data folder path is now a clickable link that opens the folder in your system's file manager (Windows Explorer, Finder, etc.).

- **Help Menu Enhancement**: Added "🚀 Setup Wizard..." menu item to the Help menu, allowing users to re-run the setup wizard at any time.

---

## v1.9.175-beta - January 28, 2026

### ✨ New Features

- **Glossary AI Injection**: New "AI" column in Glossary Settings allows glossary terms to be automatically injected into LLM translation prompts. When enabled (orange checkmark), all terms from that glossary are sent to the AI with every translation request, helping the model use your preferred terminology. Recommended for small, curated glossaries (< 500 terms).

### 🎨 UI Improvements

- **Terminology Consistency**: Renamed "Primary Prompt" to "Custom Prompt" throughout the application for better alignment with the 2-Layer Prompt Architecture documentation.

- **Preview Prompt Enhancements**: The Preview Prompts dialog now highlights the "# GLOSSARY" section in orange when glossary terms are injected.

- **Glossary Legend Updated**: The glossary settings help text now explains all four columns: Read (green), Write (blue), Priority, and AI (orange).

---

## v1.9.174 - January 28, 2026

### ✨ New Features

- **Batch Status Change**: Change the status of multiple selected segments at once via right-click context menu or Edit → Bulk Operations → Change Status. Supports all status types (Not started, Pre-translated, Translated, Confirmed, etc.)

- **Ctrl+, Tag Wrapping for HTML**: When text is selected, Ctrl+, now wraps it with HTML tag pairs (e.g., `<b>selection</b>`) in addition to memoQ tags and CafeTran pipes.

- **Ctrl+, Tip in Grid**: Added a subtle tip label "💡 Tip: Ctrl+, inserts the next tag from source" in the pagination bar to help new users discover this powerful shortcut.

### 🐛 Bug Fixes

- **TM Overwrite Mode Fixed**: The "Save only latest translation (overwrite)" TM setting now actually overwrites existing entries with the same source text, instead of creating duplicate entries.

- **Shift+Click Multi-Select Fixed**: Fixed grid selection where Shift+click to select a range was selecting extra rows. Now properly respects Qt's native range selection.

- **Status Dropdown Width**: Widened the status dropdown to prevent text truncation (e.g., "Pre-translated", "TR confirmed" now fully visible).

### 🎨 UI Improvements

- **AI Settings Reorganized**: Moved "Model Version Checker" and "API Keys" sections higher in AI Settings, right after Model Selection for easier access.

---

## v1.9.173 - January 28, 2026

### ✨ Improvements

- **Smarter TM Exact Matching**: Exact matches now use text normalization before hashing, so matches are found even when source text differs only in whitespace or Unicode normalization (e.g., non-breaking spaces vs regular spaces).

- **Improved TM Pre-Translation Dialog**: The progress dialog now shows the current segment being processed, count of matches found so far, and elapsed time. A patience message appears after 10 seconds for large jobs.

- **Higher Fuzzy Match Threshold**: Raised the minimum fuzzy match threshold from 70% to 75% for better quality matches across all TM operations.

---

## v1.9.172 - January 28, 2026

### 🐛 Bug Fixes

- **Fresh Projects Start Clean**: Fixed bug where TMs and glossaries remained activated from previous sessions when loading/creating new projects. Now all TMs and glossaries are properly deactivated when loading a project, giving you a clean slate. Saved resource activations are then restored from the project file if available.

---

## v1.9.171 - January 28, 2026

### 🐛 Bug Fixes

- **TM Target & Alt+0 Badge Restored**: Fixed regression where the TM Target and its blue "0" badge (Alt+0 shortcut) were missing from the Match Panel, even when TM matches were found. TM matches are now displayed correctly, and the Alt+0 shortcut works as documented.

---

## v1.9.170 - January 27, 2026

### ✨ New Features

- **Scratchpad Tab in Right Panel**: The Scratchpad is now available as a permanent tab in the right panel for easier access.
  - **Location**: Right panel tabs → last tab after "Session Log"
  - **Auto-Update**: Content automatically syncs with project's scratchpad notes
  - **Dual Access**: Available both as popup dialog (`Ctrl+Shift+P`) and as permanent tab
  - **Project-Aware**: Tab clears when creating new project, populates when loading project

- **Settings Improvement**: "Disable ALL caches" was temporarily enabled by default *(reverted in v1.9.183 - caches are now enabled by default for performance)*.

- **TM Target Shortcut Badge**: Added a blue "0" badge next to the TM Target in the Match Panel, indicating the Alt+0 shortcut for instant TM match insertion. Shortcut is documented and works out of the box.

---

## v1.9.169 - January 27, 2026

### ✨ New Features

- **Scratchpad for Private Notes**: New pop-up scratchpad for translator's private notes during a job.
  - **Access**: `Tools → 📝 Scratchpad...` or keyboard shortcut `Ctrl+Shift+P`
  - **Private**: Notes are stored only in the `.svproj` file and are **never** exported to CAT tools or shared with clients
  - **Persistent**: Notes are saved with the project and restored when you reopen it
  - **Use Cases**:
    - Terminology decisions and rationale
    - Client preferences and style notes
    - Research findings and reference links
    - Questions to ask the project manager
    - Personal reminders and to-do items
  - **Design**: Clean dialog with monospace font, placeholder text with usage suggestions

---

## v1.9.168 - January 27, 2026

### ✨ New Features

- **Markdown File Import Support**: Added `.md` file support to the text file importer. ([#127](https://github.com/michaelbeijer/Supervertaler/issues/127))
  - **File Menu**: `Import → Text / Markdown File (TXT, MD)...`
  - **File Filter**: Now shows "Text Files (*.txt *.md)", "Markdown (*.md)", "Plain Text (*.txt)"
  - **Smart Dialog**: Detects Markdown files and shows Markdown-specific import instructions
  - **Syntax Highlighting**: Markdown elements are highlighted with distinctive colors:
    - **Headings** (`#`, `##`, etc.): Blue, bold
    - **Bold/Italic markers** (`**`, `*`, `__`, `_`): Violet, bold
    - **Code** (`` ` ``, `` ``` ``): Orange, bold
    - **Links/Images** (`[]()`, `![]()`): Purple
    - **Blockquotes** (`>`): Green, bold
    - **Lists** (`-`, `*`, `+`, `1.`): Orange, bold
  - **Round-trip Safe**: Markdown syntax is preserved as-is for clean export back to `.md`
  - **Use Case**: Translate documentation, README files, AI prompts, and other Markdown content

---

## v1.9.167 - January 27, 2026

### 🐛 Bug Fixes

- **Keyboard Shortcuts Panel Text Vanishing**: Fixed bug where UI text (Action, Shortcut, Status columns) would disappear after changing a shortcut. ([#125](https://github.com/michaelbeijer/Supervertaler/issues/125))
  - **Root Cause**: Qt's sorting feature was interfering with table row modifications during `load_shortcuts()`, causing items to become disassociated from their rows.
  - **Fix**: Disabled sorting during table modifications and re-enabled it after completion.

---

## v1.9.166 - January 27, 2026

### 🐛 Bug Fixes

- **CRITICAL: TM Write Checkbox Now Works**: Fixed confirmed translations going to "project" TM instead of user-designated TM. The Write checkbox (not Read) now determines where segments are saved. ([#126](https://github.com/michaelbeijer/Supervertaler/issues/126))
  - **Root Cause**: `save_segment_to_activated_tms()` was using `get_active_tm_ids()` which only returns TMs with the Read checkbox enabled, ignoring the Write setting entirely.
  - **Fix**: Added new `get_writable_tm_ids()` method that checks for TMs with Write enabled (`read_only = 0`), and updated save logic to use it.
  - **Now**: Enabling Write checkbox alone (without Read) will save confirmed segments to that TM.

---

## v1.9.165 - January 27, 2026

### ✨ New Features

- **Settings Panel Font Scaling**: Added UI Font Scale setting (80%-200%) in View Settings for better readability on high-DPI/4K displays. Especially useful for macOS users with Retina displays. Click "Apply" for instant preview or save to persist. ([#128](https://github.com/michaelbeijer/Supervertaler/issues/128))

---

## v1.9.164 - January 26, 2026

### 🐛 Bug Fixes

- **macOS/Linux Compatibility**: Fixed `ModuleNotFoundError: No module named 'keyboard'` on non-Windows platforms. The `keyboard` module is Windows-only and is now imported conditionally with graceful fallback. ([#124](https://github.com/michaelbeijer/Supervertaler/issues/124))

---

## v1.9.163 - January 26, 2026

### 🐛 Bug Fixes

- **DOCX Import**: Fixed paragraph style bold/italic not being captured. Headings using styles like "Title" or "Subtitle" now correctly export as bold. Previously only direct run-level formatting was detected.
- **Termview Font Settings**: Fixed spinbox up/down buttons not visible. Fixed font size changes only applying to bottom Termview, not Match Panel Termview.
- **View Settings Dialog**: Fixed "Settings Saved" dialog not closing when clicking OK.

---

## 🧪 Cache Kill Switch & Performance Improvements (v1.9.155-162) - January 26, 2026

**Experimental Cache Bypass for Faster Grid Navigation**

This release includes a series of performance optimizations and a new experimental feature for testing grid responsiveness.

### 🧪 NEW: Cache Kill Switch (v1.9.162)

Added experimental setting to bypass all caching systems:

- **Location**: Settings → General → 🧪 Experimental Performance
- **Option**: "Disable all caches (for testing responsiveness)"
- **What it does**: Bypasses translation_matches_cache, termbase_cache, prefetch workers
- **Result**: Direct SQLite lookups - may actually be faster due to no lock contention!

Use this setting to test whether caching is helping or hurting your workflow.

### ⚡ Performance Optimizations (v1.9.155-161)

**Ctrl+Enter Speed Improvements:**
- Reduced verbose logging overhead (15-20 fewer log calls per navigation)
- Preview tab now skips TM/glossary lookups entirely (faster reviewing)
- Idle prefetch system loads matches while you type (Ctrl+Enter feels instant)
- Direct termbase lookups in prefetch worker (no more race conditions)

**TM Matching Fixes:**
- Fixed missing fuzzy matches when using multiple TMs (increased FTS5 candidate pool)
- Fixed crashes when no TMs activated or only "Write" enabled
- Fixed wrong dictionary key in TM exact match lookups

**Proactive Grid Highlighting (v1.9.161):**
- Glossary terms now highlight in UPCOMING segments while you work on current one
- See terms in segments 255, 256, 257 while editing segment 254
- No more waiting for highlighting after navigation

### 🔧 Bug Fixes

- Fixed batch translation crashes with empty TM lists
- Fixed TM pre-translation SQLite threading errors (now runs on main thread)
- Fixed retry pass variable scope issues in batch translate
- Fixed various logging and debug output issues

---

## 🎯 Match Panel Consolidation (v1.9.154) - January 25, 2026

**Streamlined Right Panel UI**

Replaced the Compare Panel with a more focused Match Panel that combines glossary terms and TM matches in one convenient view.

**What Changed:**
- **Compare Panel removed**: Was redundant with Translation Results panel
- **Match Panel introduced**: Combines Termview (glossary) + TM Source/Target boxes
- **Green TM boxes**: TM matches display with green background (#d4edda) for easy identification
- **Zoom shortcuts work**: Ctrl+Alt+= and Ctrl+Alt+- now zoom the Match Panel TM boxes
- **Cleaner tab structure**: Fewer tabs = less switching during translation

**New Right Panel Tabs:**
1. Translation Results (TM/MT/Glossary matches in list view)
2. Match Panel (Termview + TM Source/Target side-by-side)
3. Preview (document preview)
4. Segment Note
5. Session Log

**Benefits:**
- ✅ Less tab clutter - removed redundant Compare Panel
- ✅ Glossary terms and TM matches visible together in Match Panel
- ✅ Green highlighting makes TM boxes easy to spot
- ✅ Keyboard zoom shortcuts work on TM boxes

---

## 📐 Tab Layout Reorganization (v1.9.153) - January 23, 2026

**Better Workflow Organization**

Redesigned the tab layout to consolidate resources and improve translation workflow:

**What Changed:**
- **Termview stays under grid**: Original position preserved for quick glossary access
- **Second Termview in right panel**: Duplicate instance so you can see terms while viewing other tabs
- **Segment Note moved**: Now in right panel alongside Compare Panel and Preview
- **Session Log moved**: Also in right panel for better organization
- **Simultaneous updates**: Both Termview instances update together automatically

**New Tab Structure:**
- **Left panel**: Grid + Termview (collapsible)
- **Right panel**: Translation Results, Compare Panel, Preview, Segment Note, Session Log, Termview (6 tabs)

**Benefits:**
- ✅ All reference materials (TM, glossary, notes) in one location
- ✅ Grid area cleaner - just grid + glossary
- ✅ Two Termview instances let you see terms while using other tabs
- ✅ Ctrl+N shortcut still works to jump to Segment Note tab

**Implementation:**
- New helper method: `_update_both_termviews()` - updates both instances simultaneously
- Updated 5 locations where Termview gets updated
- Modified tab creation code to reorganize layout
- Updated Ctrl+N shortcut to find tab by name (works regardless of tab visibility)

**Future Enhancement (Phase 2):**
User requested advanced docking: ability to drag tabs to dock them vertically in the right panel (like VS Code). This would require QDockWidget architecture - a significant refactor planned for future version.

---

## ⚡ Instant Glossary Updates (v1.9.152) - January 23, 2026

**Lightning-Fast Term Addition Performance**

Adding terms to glossaries is now instant! The 5-6 second delay when using Alt+Shift+Up/Down shortcuts has been eliminated.

**The Problem:**
- Users experienced 5-6 second delays after adding glossary terms during translation
- Long patent sentences with 50+ words required 50+ individual database searches
- The app was searching for ALL words again just to find the ONE term we just added

**The Solution:**
- **Direct cache update**: New term added directly to cache instead of full segment re-search
- **Immediate TermView update**: Display updates instantly using cached matches
- **Smart highlighting**: Source cell highlighting updated via direct function call
- **Zero database searches**: We already know what we added - no need to search for it!

**Result:**
- ✅ TermView shows new term instantly (< 0.1 seconds)
- ✅ Source highlighting updates instantly
- ✅ Smooth, responsive workflow for building glossaries
- ✅ Perfect for intensive patent translation workflows

**Technical Implementation:**
- Modified `_quick_add_term_with_priority()` to create match entry directly from added term
- Bypasses expensive `find_termbase_matches_in_source()` database search
- Calls `highlight_source_with_termbase()` directly with updated cache
- Maintains all existing functionality while eliminating performance bottleneck

**Files Modified:**
- `Supervertaler.py` - Optimized glossary quick-add workflow (~60 lines modified)

**🛡️ Exit Crash Fix:**
- Enhanced `_cleanup_web_views()` method to prevent Python crash on program exit
- Now properly stops all WebEngine page loading/rendering before cleanup
- Processes events multiple times and adds delay to ensure Qt finishes cleanup
- No more "Python has stopped working" dialog when using File → Exit

---

## 🔧 TM Pre-Translation Fixed (v1.9.151) - January 23, 2026

**Critical Fix:** "Pre-translate from TM" batch operation now correctly finds TM matches!

**What Was Broken:**
- Running Edit → Batch Operations → Pre-translate from TM found 0 matches
- Even when a 100% TM match was clearly visible in the Compare Panel
- Issue: SQLite databases cannot be shared across threads

**Root Cause:**
The `PreTranslationWorker` ran in a background thread, but SQLite connections created in the main thread cannot be used in other threads. This caused a `sqlite3.ProgrammingError`.

**The Fix:**
- TM pre-translation now runs **on the main thread** (same as the Compare Panel)
- Uses `QProgressDialog` to show progress and keep UI responsive
- Uses the **exact same database methods** that work for segment navigation
- No more SQLite threading errors!

**Before:** "Pre-translate from TM" → 0 matches found
**After:** "Pre-translate from TM" → Correctly finds all TM matches

## 🔍 Superlookup Language-Aware Search Enhancement (v1.9.149-beta) - January 22, 2026

**Major Enhancement:** Superlookup TM search now intelligently handles language filters!

**What Changed:**
- **Intuitive Language Filters**: "From: Dutch → To: English" now means "Search FOR Dutch text and show me English translations"
- **Smart Column Detection**: Searches ALL TMs regardless of their stored direction (NL→EN or EN→NL)
- **Automatic Swapping**: Finds text in either column and automatically presents results in the correct order
- **More Powerful Than Traditional CAT Tools**: Unlike memoQ/Trados that only search one TM direction, Supervertaler finds matches everywhere

**How It Works:**
1. Set "From: Dutch → To: English"
2. Search for Dutch text
3. System searches both NL→EN TMs (source column) AND EN→NL TMs (target column)
4. Results automatically shown with Dutch in source, English in target

**UI Simplification:**
- **Removed Direction radio buttons** (Both/Source/Target) - always searches both columns now
- Cleaner, faster interface for translators
- Language dropdowns are all you need

**UI Polish:**
- **Renamed "QuickMenu" tab to "Prompt Manager"** - Better clarity for new users looking for translation prompts
- **Sub-tab renamed**: "Library" → "Prompt Library"
- Resolves confusion about where to find prompts for single-segment and batch translation

**Technical Details:**
- Language filters no longer restrict which TMs are searched
- Post-processing validates search text is in the correct language column
- Smart swapping ensures results always match user's requested language direction

**Files Modified:**
- `modules/database_manager.py` - Smart language-aware concordance search
- `modules/superlookup.py` - Column name handling
- `Supervertaler.py` - Removed Direction controls, simplified UI, renamed QuickMenu to Prompt Manager
- `modules/unified_prompt_manager_qt.py` - Updated tab and header labels

---

## 📁 User-Choosable Data Folder Location (v1.9.148-beta) - January 21, 2026

**Major Enhancement:** Users now choose where to store their data on first run!

**What Changed (from v1.9.147):**
- v1.9.147 stored data in hidden AppData folders - users couldn't easily find/backup their data
- v1.9.148 uses visible, accessible locations that users control

**The New System:**

| Platform | Default Location |
|----------|------------------|
| **Windows** | `C:\Users\Username\Supervertaler\` |
| **macOS** | `~/Supervertaler/` |
| **Linux** | `~/Supervertaler/` |

**Key Features:**
- **First-run dialog** lets users choose their data folder location
- **Default is visible** in home folder - easy to find and backup
- **Settings → General** includes "Change..." button to relocate data anytime
- **Auto-recovery** if config pointer is deleted but data exists at default location
- **Unified system** - ALL users (pip, EXE, dev) use the same approach

**How It Works:**
1. On first run, a dialog asks where to store data
2. User choice is saved to a small config pointer file:
   - Windows: `%APPDATA%\Supervertaler\config.json`
   - macOS: `~/Library/Application Support/Supervertaler/config.json`
   - Linux: `~/.config/Supervertaler/config.json`
3. This pointer just contains: `{"user_data_path": "C:\\Users\\John\\Supervertaler"}`
4. If pointer is deleted, app auto-recovers by checking the default location

**Benefits:**
- ✅ Data is visible and easy to find
- ✅ Easy to backup (just copy the folder)
- ✅ User has full control over location
- ✅ Can use cloud folders (OneDrive, Dropbox, etc.)
- ✅ Survives pip upgrades
- ✅ Works identically for all installation types

---

## 📁 Persistent User Data Location (v1.9.147) - January 21, 2026

*Note: v1.9.148 improves on this by using visible locations and adding user choice.*

**Major Enhancement:** User data (API keys, TMs, glossaries, prompts, settings) now persists across pip upgrades!

**The Problem:**
- When users ran `pip install --upgrade supervertaler`, their data was wiped
- This happened because user_data/ was stored inside the pip package directory
- pip replaces the entire package directory on upgrade, deleting all user files

---

## 🔑 Gemini/Google API Key Alias Fix (v1.9.146) - January 21, 2026

**Bug Fix:** Fixed "Gemini API Key Missing" error when users had `google=...` instead of `gemini=...` in their api_keys.txt file.

**The Problem:**
- Users could use either `google=YOUR_KEY` or `gemini=YOUR_KEY` in api_keys.txt
- Some code paths only checked for `gemini`, others only for `google`
- This caused confusing "API Key Missing" dialogs even when keys were properly configured

**The Solution:**
- Added **automatic normalization** in `load_api_keys()` - if either `google` or `gemini` is set, both keys are now populated
- Users can use either name interchangeably
- Fixed 6+ locations where the alias wasn't being handled correctly:
  - Single segment translation (Ctrl+T)
  - Batch translation
  - QuickMenu prompts
  - Async LLM fetch for Translation Results panel
  - Proofreading (also fixed `anthropic` → `claude` provider name bug)

**For Users:**
- Both `google=YOUR_KEY` and `gemini=YOUR_KEY` now work identically
- No action needed - existing api_keys.txt files will continue to work

---

## ✨ memoQ-Style Track Changes in Compare Panel (v1.9.145) - January 20, 2026

**Improvement:** Changed Compare Panel diff highlighting to match memoQ's "Track changes view" style.

**New Styling (memoQ-style):**
- **Deletions**: Red text + strikethrough (~~deleted~~)
- **Insertions**: Red text + underline (<u>inserted</u>)
- **Unchanged**: Normal text

This is cleaner and more familiar to translators who use Word's track changes or memoQ.

**Example:**
```
Current: In een derde aspect betreft de huidige uitvinding het gebruik van een dichtingskit...
TM:      In een tweede aspect betreft de huidige uitvinding een dichtingskit...

Compare Panel shows:
In een ~~tweede~~ derde aspect betreft de huidige uitvinding het gebruik van een dichtingskit...
        ^^^^^^^^  ^^^^^^                                      ^^^^^^^^^^^^^^^^
        red+strike red+under                                  red+underline
```

---

## ✨ Enhanced Compare Panel Diff Highlighting (v1.9.144) - January 20, 2026

**Improvement:** The Compare Panel now shows a complete diff with additions, deletions, and changes - matching what professional CAT tools display.

**Before:**
- Only showed text that was **different** (in red)
- Didn't show what was **added** in the current segment
- Hard to understand what changed between TM source and current source

**After:**
- **Red with strikethrough**: Text in TM that was changed/deleted in current segment
- **Green background**: Text in current segment that was added (not in TM)
- **Normal text**: Identical text in both

**Example:**
```
Current: In een derde aspect betreft de huidige uitvinding het gebruik van een dichtingskit...
TM:      In een tweede aspect betreft de huidige uitvinding een dichtingskit...

Compare Panel now shows:
In een [tweede→derde] aspect betreft de huidige uitvinding [+het gebruik van] een dichtingskit...
```

**Technical:**
- Changed from character-level to word-level diffing for better readability
- Additions shown inline in green where they would appear
- Deletions shown with strikethrough so you can see what was removed

---

## 🐛 Fix: Deleting Glossary Entry from Termview (v1.9.143) - January 20, 2026

**Bug Fix:** Deleting glossary entries via right-click in Termview failed with an error.

**Error in Logs:**
```
✗ Error deleting glossary entry from database: 'DatabaseManager' object has no attribute 'get_connection'
```

**Root Cause:**
- The delete handler was trying to call `db_manager.get_connection()` which doesn't exist
- Was using raw SQL instead of the existing `termbase_mgr.delete_term()` method

**The Fix:**
- Changed to use `self.termbase_mgr.delete_term(term_id)` which already exists and works correctly

---

## 🐛 Fix: Error When Editing Glossary Entry from Termview (v1.9.142) - January 20, 2026

**Bug Fix:** After editing a glossary entry via right-click → Edit in Termview, an error would occur preventing proper refresh.

**Error in Logs:**
```
Error refreshing segment matches: SupervertalerQt.on_cell_selected() missing 2 required positional arguments: 'previous_row' and 'previous_col'
```

**Root Cause:**
- The `_refresh_current_segment_matches()` method was calling `on_cell_selected(current_row, 2)` with only 2 arguments
- But `on_cell_selected()` requires 4 arguments: `current_row`, `current_col`, `previous_row`, `previous_col`

**The Fix:**
- Simplified `_refresh_current_segment_matches()` to use the targeted `_refresh_termbase_display_for_current_segment()` method
- This method already handles termbase cache clearing and display refresh correctly

---

## 🐛 Fix: Termview Blank After Adding Glossary Term (v1.9.141) - January 20, 2026

**Bug Fix:** After adding a term to a glossary via Alt+Down (or similar shortcuts), the Termview pane would go blank and stay blank until navigating to another segment.

**Error in Logs:**
```
Error updating termview: list index out of range
```

**Root Cause:**
- The `_refresh_termbase_display_for_current_segment()` method (added in v1.9.140) was using incorrect dictionary keys
- `find_termbase_matches_in_source()` returns dict with keys `source` and `translation`
- But the refresh method was looking for keys `source_term` and `target_term`
- This resulted in empty strings being passed to the termview, causing the index error

**The Fix:**
- Changed `match.get('source_term', '')` → `match.get('source', '')`
- Changed `match.get('target_term', '')` → `match.get('translation', '')`
- Applied same fix to Translation Results panel update section

---

## 🐛 Fix: Adding Glossary Term No Longer Triggers TM Search (v1.9.140) - January 20, 2026

**Performance Fix ([#118](https://github.com/michaelbeijer/Supervertaler/issues/118)):** Adding a term to a glossary was unnecessarily triggering a full Translation Memory search, causing delays.

**The Problem:**
- When adding a term via Ctrl+E, Ctrl+Q, or Ctrl+Shift+1/2, the app cleared BOTH caches and called `on_cell_selected()`
- This triggered a complete TM search even though adding a glossary term doesn't change the source/target text

**The Fix:**
- Created new targeted method `_refresh_termbase_display_for_current_segment()`
- Only clears the termbase cache (not TM cache)
- Updates TermView widget with fresh glossary matches
- Updates Translation Results panel's Termbases section only
- Re-highlights termbase matches in source cell
- TM results remain untouched

**Also in this release:**
- 🎤 Renamed "Voice OFF/ON" button to "Voice Commands OFF/ON" for clarity
- 🎤 Renamed "Dictate" button to "Dictation"

---

## 📐 Auto-Sizing Segment Number Column (v1.9.138) - January 20, 2026

**Grid UX Improvement:** The segment number column (#) now automatically sizes itself based on:
- The current font size (scales when you zoom in/out)
- The number of segments in the project (fits 3-digit, 4-digit numbers, etc.)

Uses Qt font metrics to calculate the exact pixel width needed. No more truncated numbers or wasted space!

**Also in this release:**
- Status column made slightly narrower (70px → 60px)

---

## 🏷️ Termview Punctuated Terms Fix (v1.9.138) - January 20, 2026

**Fixed: Glossary terms with punctuation now appear in Termview**

Glossary entries like "ca." (with period) or "typisch" (when appearing in parentheses as "(typisch)") were found by the termbase search (grid showed green highlighting) but did NOT appear in the Termview pane.

**Root Cause - Key Mismatch:**
- `matches_dict` keys were built using the raw source term: `"ca."` (with period)
- But lookup stripped punctuation from tokens: `"ca."` → `"ca"`
- Result: `matches_dict.get("ca")` returned nothing because the key was `"ca."`

**The Fix:**
- When building `matches_dict`, keys are now normalized by stripping punctuation
- Both the dictionary keys and lookup keys now use the same normalization
- Added brackets `()[]` to punctuation chars so "(typisch)" matches "typisch"

**Files Modified:**
- `modules/termview_widget.py` - Normalize punctuation in `matches_dict` keys and lookup

---

## 🔧 Termview Race Condition Fix (v1.9.137) - January 20, 2026

**Fixed: Glossary terms now appear in Termview pane**

When navigating to a segment, the Termview pane showed "No glossary matches" even though:
- The grid highlighted terms in green (glossary highlighting worked)
- Force Refresh (F5) would then show the terms correctly

**Root Cause - Timing/Race Condition:**
- `update_tab_segment_editor()` was called EARLY in the cell selection process
- It tried to read from `termbase_cache[segment_id]` to update Termview
- But the termbase search (`find_termbase_matches_in_source()`) hadn't run yet!
- Result: Termview called with empty list before matches were found

**The Fix:**
1. Removed premature Termview update from `update_tab_segment_editor()` 
2. Termview is now updated ONLY after the termbase search completes in `_on_cell_selected_full()`
3. Also fixed: Termview now updates even when no matches found (shows "No matches" state)

**Files Modified:**
- `Supervertaler.py` - Removed premature Termview update, fixed condition to always update Termview
- `modules/termview_widget.py` - Removed debug logging

---

## 📚 Glossary Matching Fix for Punctuation (v1.9.136) - January 20, 2026

**Fixed: Glossary terms with trailing punctuation now match correctly**

Glossary entries like "ca." (with period), "psi", and "typisch" were not being found in the Termview window when they appeared in source text like "ca. 2,2 (270 psi)".

**Root Cause:**
- When tokenizing source text, punctuation was stripped from words ("ca." → "ca")
- The database search then looked for "ca" but the glossary had "ca." — no match
- Short terms in parentheses like "(psi)" were also affected

**The Fix:**
1. Now searches for BOTH the stripped word AND the original word with punctuation
2. Database query enhanced with reverse matching: finds glossary terms where the search word matches the term with trailing punctuation stripped
3. Handles entries like "ca.", "gew.%", "psi", etc.

**Files Modified:**
- `Supervertaler.py` - Enhanced `find_termbase_matches_in_source()` to search with original punctuation
- `modules/database_manager.py` - Enhanced `search_termbases()` with punctuation-tolerant matching

---

## 🔍 Filter Now Searches Entire Document (v1.9.135) - January 20, 2026

**Fixed: Filter Source/Target boxes now search across ALL pages**

Previously, the Filter Source and Filter Target boxes above the grid would only search within the currently visible page. If the text you were looking for was on a different page, it wouldn't be found.

Now, filtering searches through the **entire document** regardless of pagination. When a filter is active, ALL matching rows are displayed (pagination is temporarily ignored). When you clear the filter, normal pagination resumes.

**Files Modified:**
- `Supervertaler.py` - Fixed `_apply_pagination_to_grid()` to show all filter matches

---

## 🔊 Fuzzy TM Match Sound Effect (v1.9.134) - January 20, 2026

**New sound effect option: "Fuzzy TM match found"**

Plays when navigating to a segment and a fuzzy TM match (50-99%) is found, but NO 100% match exists.

**Access:** Settings → General → Sound Effects → "Fuzzy TM match found"

Disabled by default (set to "None"). Works with the same sound options as other effects.

---

## 🔊 New Sound Effects (v1.9.133) - January 20, 2026

**Two new sound effect options added:**

1. **Segment confirmed** - Plays when you confirm a segment with Ctrl+Enter
2. **100% TM match alert** - Plays when navigating to a segment and a 100% TM match is found and auto-inserted

**Access:** Settings → General → Sound Effects

Both sounds are disabled by default (set to "None"). Users can configure them to any of the available Windows system sounds:
- OK, Asterisk, Exclamation, Hand, Question
- Windows .wav files: Restore, Navigation Start, Speech Disambiguation, etc.

**Files Modified:**
- `Supervertaler.py` - Added sound effect options and trigger points

---

## 🐛 Ctrl+K Superlookup Shortcut Fix (v1.9.132) - January 20, 2026

**Fixed: Ctrl+K was not working**

The Ctrl+K shortcut to open Superlookup with selected text was broken due to a duplicate shortcut conflict:

**Root Cause:**
- A QShortcut (global) was registered for Ctrl+K → `show_concordance_search()` (correct)
- A QAction menu item ALSO had `setShortcut("Ctrl+K")` → `_go_to_superlookup()` (wrong handler)
- When both claimed the same key, Qt's behavior was unpredictable

**The Fix:**
- Removed duplicate shortcut from menu action
- Menu item still shows "(Ctrl+K)" in label for discoverability
- Now connects to `show_concordance_search()` for consistent behavior

**Files Modified:**
- `Supervertaler.py` - Removed duplicate Ctrl+K binding from Tools menu

---

## ⌨️ Alt+K QuickMenu Shortcut (v1.9.131) - January 20, 2026

**Direct QuickMenu Access via Keyboard**

Added Alt+K keyboard shortcut to open the QuickMenu popup directly without right-clicking:

**How It Works:**
1. Press Alt+K while in the grid (source or target cell)
2. QuickMenu popup appears at cursor position
3. Use Up/Down arrows to navigate prompts
4. Press Enter to expand a prompt's actions
5. Select "Run (show response)" or "Run and replace target"

**Benefits:**
- Faster workflow - no mouse needed
- Quick access to AI prompt actions
- Works from both source and target cells
- Menu appears at cursor position for easy navigation

**Files Modified:**
- `modules/shortcut_manager.py` - Added `editor_open_quickmenu` shortcut definition
- `Supervertaler.py` - Added `open_quickmenu()` method, registered Alt+K shortcut

---

## ✨ Context Placeholders & Auto-Center Fix (v1.9.130) - January 20, 2026

**Three Context Placeholders for QuickMenu Prompts**

Split the `{{DOCUMENT_CONTEXT}}` placeholder into three specialized variants for better AI prompt control:

| Placeholder | Purpose | Output |
|-------------|---------|--------|
| `{{SOURCE+TARGET_CONTEXT}}` | Proofreading prompts | Both source and target text |
| `{{SOURCE_CONTEXT}}` | Translation/terminology questions | Source text only |
| `{{TARGET_CONTEXT}}` | Consistency/style analysis | Target text only |

**Why Three Placeholders?**
- **Proofreading**: Needs both source and target to verify translations
- **Translation questions**: Only needs source (showing MT translations would mislead the AI)
- **Style analysis**: Only needs target text to analyze consistency

**🎯 Auto-Center Active Segment Fix**

Fixed "Keep Active Segment Centered" feature using Qt's built-in centering:
- **Previous issue**: Manual viewport calculations were unreliable across different screen sizes
- **Solution**: Use `table.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)`
- **Result**: Active segment now reliably centers in the viewport during navigation

**⌨️ Double-Tap Shift Context Menu**

New keyboard shortcut for faster right-click menu access (via AutoHotkey):
- **Double-tap Shift**: Opens context menu at cursor position
- **Works in Supervertaler only**: Won't interfere with other applications
- **Requires AutoHotkey**: Part of `supervertaler_hotkeys.ahk` script

**🔧 Script Rename**

Renamed AHK script for clarity:
- `superlookup_hotkey.ahk` → `supervertaler_hotkeys.ahk`
- Now handles multiple hotkeys: Ctrl+Alt+L (Superlookup) + Shift+Shift (context menu)

**Files Modified:**
- `Supervertaler.py` - Context placeholder handling, auto-center fix, AHK script references
- `modules/unified_prompt_manager_qt.py` - Updated Placeholders reference tab
- `modules/shortcut_manager.py` - Added double-shift shortcut documentation
- `supervertaler_hotkeys.ahk` - New combined hotkey script

---

## 🐛 QuickMenu Document Context Bug Fix (v1.9.129) - January 19, 2026

**Fixed Critical Bug: {{DOCUMENT_CONTEXT}} Placeholder Now Works**

Fixed a critical bug where the `{{DOCUMENT_CONTEXT}}` placeholder in QuickMenu prompts was completely broken due to a method name typo:

**The Problem:**
- QuickMenu prompts using `{{DOCUMENT_CONTEXT}}` would fail to load project segments
- Instead of receiving actual document context, the AI received an error message
- This made context-aware prompts ineffective (AI answered generic questions without project knowledge)

**Root Cause:**
- `_build_quickmenu_document_context()` called `self.load_general_settings_from_file()` which doesn't exist
- Should have been `self.load_general_settings()` (without "_from_file" suffix)
- Exception was caught but resulted in error text being sent to AI instead of segments

**The Fix:**
- Fixed method name: `load_general_settings_from_file()` → `load_general_settings()`
- Document context now builds correctly with configurable percentage (default 50%)
- Maximum 100 segments as safety limit to prevent token overflow

**User Impact:**
- ✅ QuickMenu prompts can now access full project context
- ✅ AI receives actual segments instead of error messages
- ✅ Context-aware translation suggestions now work as intended
- ✅ Better handling of domain-specific terminology with project knowledge

**Example Working Prompt:**
```
Suggest the best possible translation of "{{SELECTION}}" from {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}} within the context of the current patent application: {{DOCUMENT_CONTEXT}}
```

**Files Modified:**
- `Supervertaler.py` - Fixed method name in `_build_quickmenu_document_context()`

---

## 📐 Placeholders Tab Layout Optimization (v1.9.128) - January 19, 2026

**Vertical Space Optimization**

Redesigned the Placeholders reference tab to eliminate wasted vertical space and match the standard tool layout pattern used in AutoFingers, TMX Editor, and Supercleaner:

**Layout Changes:**
- **Tips Sidebar**: Moved "Usage Tips" section to a right sidebar panel (280-400px width)
- **Standard Header**: Changed header from 10pt to 16pt bold with #1976D2 color to match other tools
- **Description Box**: Added light blue (#E3F2FD) description box below header for consistency
- **Stretch Factor**: Added stretch factor to splitter layout (`layout.addWidget(splitter, 1)`) to fill all vertical space
- **QSplitter**: Implemented horizontal splitter with table (75%) and tips panel (25%)

**Result:**
- Table now fills entire vertical space without any wasted area
- Tips remain easily accessible in right sidebar
- Visual consistency with other tool tabs throughout the application

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Complete `_create_placeholders_tab()` redesign (~85 lines modified)

---

## 🔧 Prompt Manager UI Fixes (v1.9.127) - January 19, 2026

**Save Button Fix**

Fixed issue where Save button remained greyed out (disabled) after creating a new prompt:

**Problem:**
- User clicks "+ New" → enters prompt name → prompt loads in editor
- Save button remains disabled despite content being loaded
- Could not save edits to new prompts

**Fix:**
- Added explicit `btn_save_prompt.setEnabled(True)` call after `_load_prompt_in_editor()` in `_new_prompt_in_folder()` method
- Ensures Save button is always enabled after new prompt creation
- Prevents workflow interruption when creating and editing prompts

**Label Rename**

Renamed QuickMenu checkbox label for clarity:

**Before:** "Show in QuickMenu"  
**After:** "Show in Supervertaler QuickMenu"

**Reason:** Distinguishes the app-level QuickMenu from the Grid right-click QuickMenu for better user understanding.

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Save button enable call, checkbox label text

---

## 🔄 Prompt System Improvements (v1.9.126) - January 19, 2026

**Field Rename: `quickmenu_quickmenu` → `sv_quickmenu`**

Renamed the redundant `quickmenu_quickmenu` field to cleaner `sv_quickmenu` (Supervertaler QuickMenu) throughout the codebase:

**What Changed:**
- All internal code now uses `sv_quickmenu` instead of `quickmenu_quickmenu`
- Backward compatibility maintained: Old .svprompt files with `quickmenu_quickmenu` still load correctly
- Legacy `quick_run` field kept in sync for compatibility with older code
- Pattern: Read old field names if present, always write new field name

**Files Modified:**
- `modules/unified_prompt_library.py` - Updated parse, save, toggle methods (6 occurrences)
- `modules/unified_prompt_manager_qt.py` - Updated editor, creation, display code (12 occurrences)

**📝 Placeholders Reference Tab**

Added new "Placeholders" tab to Prompt Manager for easy reference when writing prompts:

**Features:**
- Complete list of all 5 available placeholders with descriptions and examples
- Table format: Placeholder | Description | Example
- Usage tips section with best practices
- Located in Prompt Manager after AI Assistant tab

**Available Placeholders:**
- `{{SELECTION}}` - Currently selected text in grid
- `{{SOURCE_TEXT}}` - Full source segment text
- `{{SOURCE_LANGUAGE}}` - Project source language (e.g., "Dutch")
- `{{TARGET_LANGUAGE}}` - Project target language (e.g., "English")
- `{{DOCUMENT_CONTEXT}}` - Formatted list of project segments (configurable %)

**Access:**
- Open Prompt Manager
- Click "📝 Placeholders" tab
- View table with all placeholders, descriptions, and examples

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Added `_create_placeholders_tab()` method, added tab to sub-tabs

---

## 🐛 Prompt Save Crash Fix (v1.9.125) - January 19, 2026

**Fixed Critical Crash When Saving Prompts**

Fixed unhandled exception that caused the application to crash silently when saving prompts:

**The Problem:**
- Changing text in a prompt and clicking save would crash the app
- No error message displayed - just "Unhandled Python exception"
- Users couldn't save their prompt changes

**The Fix:**
- Wrapped entire `_save_current_prompt()` method in comprehensive try/except block
- Added detailed error logging with full stack trace
- Now shows user-friendly error dialog with actual error message
- Logs error to console and session log for debugging

**Error Handling:**
```python
try:
    # All save logic...
except Exception as e:
    # Log full traceback
    # Show error dialog to user
    # Prevent silent crash
```

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Added comprehensive error handling to prompt save

---

## 📄 QuickMenu Document Context Support (v1.9.124) - January 19, 2026

**QuickMenu Prompts Can Now Access Full Document Context**

Major enhancement allowing QuickMenu prompts to access the entire project's source segments for context-aware AI suggestions:

**New Placeholder:**
- `{{DOCUMENT_CONTEXT}}` - Inserts formatted list of project segments (source + target)

**Configurable Context:**
- Slider in Settings → AI Settings → QuickMenu Document Context (0-100%)
- Default: 50% of project segments
- Safety limit: Maximum 100 segments to prevent token overload
- 0% disables document context

**Format:**
```
=== DOCUMENT CONTEXT ===
(Showing 250 of 500 segments - 50%)

[1] Technical defect
    → Technisch mankement

[2] Manufacturing process
    → Fabricageproces

...
```

**Example Use Case:**
```
{{DOCUMENT_CONTEXT}}

Suggest the best possible translation of "{{SELECTION}}" from {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}} within the context of the current project shown above.
```

**Benefits:**
- ✅ AI understands project domain and terminology
- ✅ Consistent translations across the document
- ✅ Better handling of ambiguous terms
- ✅ Context-aware suggestions for specialized fields

**Files Modified:**
- `Supervertaler.py` - Added `_build_quickmenu_document_context()`, enhanced `_quickmenu_build_custom_prompt()`, added UI settings

---

## 🤖 QuickMenu Generic AI Support (v1.9.123) - January 19, 2026

**QuickMenu Now Supports Any AI Task**

Fixed critical bug where QuickMenu prompts were being forced into translation mode, preventing generic AI tasks from working correctly:

**The Problem:**
- QuickMenu was calling `client.translate()` with the selected text as input
- This forced the LLM to interpret every prompt as a translation task
- Generic prompts like "Explain this", "Define the selection", "Suggest four translations" would fail
- The AI would try to translate the prompt itself instead of executing it

**The Fix:**
- Changed to use generic AI completion pattern (empty text + custom_prompt)
- Simplified prompt builder to not add translation-specific instructions
- QuickMenu prompts now work as intended for ANY task

**What You Can Do Now:**
- ✅ **Explain this** - Get explanations of technical terms
- ✅ **Define the selection** - Quick dictionary lookups
- ✅ **Suggest four translations** - Multiple translation options with context
- ✅ **Analyze tone** - Check if translation matches source tone
- ✅ **Search for examples** - Find usage examples
- ✅ **Any custom prompt** - QuickMenu works for any AI task

**Example QuickMenu Prompts:**
```
Explain {{SELECTION}} in simple terms.

Suggest four possible translations of "{{SELECTION}}" from {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}} within the context of patent law.

Define {{SELECTION}} and provide usage examples.
```

**Technical Changes:**
- `run_grid_quickmenu_prompt()`: Now uses empty text with custom_prompt for generic completion
- `_quickmenu_build_custom_prompt()`: Simplified to generic prompt builder (removed translation-specific wrappers)
- Supports placeholders: `{{SELECTION}}`, `{{SOURCE_TEXT}}`, `{{SOURCE_LANGUAGE}}`, `{{TARGET_LANGUAGE}}`

**Files Modified:**
- `Supervertaler.py` - Fixed QuickMenu AI execution to support generic tasks

---

## ⌨️ Ctrl+N Repurposed for Quick Notes (v1.9.122) - January 19, 2026

**Faster Note-Taking Workflow**

Repurposed Ctrl+N keyboard shortcut from "New Project" to "Focus Segment Note Tab" for a more useful translation workflow:

**What Changed:**
- **Ctrl+N**: Now switches to the Segment Note tab and focuses the editor
- **New Project**: No longer has a keyboard shortcut (create via File menu)

**Why This Change:**
- Users rarely create new projects via keyboard
- Quick note-taking is much more common during translation
- Faster workflow: Press Ctrl+N, start typing your note immediately

**How It Works:**
1. Press Ctrl+N while translating in the grid
2. The "📝 Segment note" tab (below the grid) is selected
3. Cursor automatically placed in the notes editor
4. Start typing your note right away

**Use Cases:**
- Add context about difficult terms
- Note translation concerns for later review
- Add research notes or URLs
- Document translator decisions

**Files Modified:**
- `modules/shortcut_manager.py` - Changed `file_new` default to empty, added `editor_focus_notes` with Ctrl+N
- `Supervertaler.py` - Added `focus_segment_notes()` handler method

---

## 🐛 Find & Replace Performance Fix (v1.9.121) - January 19, 2026

**Critical Fix: Actually Fast Now!**

Fixed v1.9.120 optimization that accidentally made Find & Replace slower by calling `load_segments_to_grid()` which recreates all widgets.

**The Problem in v1.9.120:**
- Replace All took 37-39 seconds for 12 replacements (worse than before!)
- Root cause: `load_segments_to_grid()` recreates all 755 QTextEdit widgets (23 seconds)
- My optimization batched UI updates but then destroyed the performance by rebuilding everything

**The Real Fix in v1.9.121:**
- Update only the affected cells in-place using `cellWidget().setPlainText()`
- No widget recreation - just update the text content
- Track which rows were modified and update only those
- Batch operations update all target cells efficiently

**Performance Results:**
- Replace operations should now be near-instant (<1 second)
- No more 20+ second widget recreation delays
- Same results, but actually fast this time

**Files Modified:**
- `Supervertaler.py` - Fixed `replace_all_matches()` and `_fr_run_set_batch()` to update cells in-place

---

## ⚡ Find & Replace Speed Optimization (v1.9.120) - January 19, 2026

**Note:** This version had a bug that made performance worse. Use v1.9.121 instead.

**Massive Performance Improvement for Find & Replace Operations**
- Track which rows were modified and update only those
- Batch operations update all target cells efficiently

**Performance Results:**
- Replace operations should now be near-instant (<1 second)
- No more 20+ second widget recreation delays
- Same results, but actually fast this time

**Files Modified:**
- `Supervertaler.py` - Fixed `replace_all_matches()` and `_fr_run_set_batch()` to update cells in-place

---

## ⚡ Find & Replace Speed Optimization (v1.9.120) - January 19, 2026

**Note:** This version had a bug that made performance worse. Use v1.9.121 instead.

**Massive Performance Improvement for Find & Replace Operations**

Optimized Find & Replace to be dramatically faster, especially when making many replacements:

**The Problem:**
- Replace All operations could take 5-10 seconds when making many replacements
- UI was updated for **every single replacement**, causing hundreds of redraws
- After all replacements, the entire grid was reloaded, recreating ALL widgets
- No pre-filtering - all segments were processed even if they didn't contain the search text

**Optimizations Implemented:**

1. **Batch UI Updates**: Wrap replacements in `setUpdatesEnabled(False)` to prevent redraws during processing
   - Before: Update grid after each replacement (hundreds of redraws)
   - After: Single grid reload at the end

2. **Pre-Filter Segments**: Quick text search to skip segments that don't contain the search text
   - Before: Process all 500+ segments with regex operations
   - After: Only process segments that might match (case-insensitive substring check)

3. **Removed Individual Item Updates**: No longer calls `item.setText()` for each replacement
   - Before: Update each cell individually, then reload entire grid
   - After: Just reload grid once at the end

**Performance Results:**
- Operations that took 5-10 seconds now complete in under 1 second
- Batch F&R operations also optimized with same improvements
- No functional changes - same results, just much faster

**Files Modified:**
- `Supervertaler.py` - Optimized `replace_all_matches()`, `_fr_run_set_batch()`, `_execute_single_fr_operation()`

---

## ⌨️ Alt+D Dictionary Shortcut (v1.9.119) - January 19, 2026

**Quick Dictionary Addition from Grid**

Added Alt+D keyboard shortcut for quickly adding words to the custom dictionary without using the right-click menu:

**How It Works:**
- Place cursor on any misspelled word in the target cell
- Press Alt+D
- Word is instantly added to custom dictionary
- Red underline removed and highlighting refreshed across all cells

**Benefits:**
- Faster workflow - no need to right-click and select from menu
- Particularly useful when translating technical documents with many specialized terms
- Works exactly like the context menu "Add to Dictionary" but with a single keystroke

**Files Modified:**
- `modules/shortcut_manager.py` - Added `editor_add_to_dictionary` shortcut definition
- `Supervertaler.py` - Added `add_word_to_dictionary_shortcut()` handler method
- `Supervertaler.py` - Registered Alt+D shortcut in `setup_global_shortcuts()`

**Usage:**
1. See a red underline on a word in the target cell
2. Click to place cursor on that word
3. Press Alt+D
4. Word added to dictionary, underline removed

---

## 🐛 Termview Glossary Punctuation Fix (v1.9.118) - January 19, 2026

**Fixed Glossary Punctuation Matching in Termview Widget**

Completed the glossary punctuation fix by applying it to the Termview widget:

**The Problem:**
- v1.9.117 fixed punctuation matching in the Translation Results panel
- But the Termview widget has its own separate matching logic that wasn't fixed
- Glossary entry: `"...problemen."` (with period) wouldn't show in Termview
- Same entry without period: `"...problemen"` worked correctly

**The Fix:**
- Applied the same punctuation normalization fix to `get_all_termbase_matches()` in `termview_widget.py`
- Now strips trailing/leading punctuation from glossary terms before pattern matching
- Both Translation Results panel AND Termview now handle punctuation correctly

**User Impact:**
- Users can add full sentences/phrases to glossaries with punctuation
- Termview now shows matches for entries with periods, quotes, etc.
- Consistent behavior between Translation Results and Termview

**Files Modified:**
- `modules/termview_widget.py` - Added punctuation stripping to `get_all_termbase_matches()` (line ~933-947)

---

## 🐛 Glossary Matching with Punctuation (v1.9.117) - January 19, 2026

**Fixed Critical Glossary Matching Bug**

Glossary entries with trailing punctuation (periods, quotes, etc.) now match correctly in source text:

**The Problem:**
- Glossary entry: "De huidige uitvinding beoogt een oplossing te vinden voor tenminste enkele van bovenvermelde problemen." (with period)
- Source text: "De huidige uitvinding beoogt een oplossing te vinden voor tenminste enkele van bovenvermelde problemen."
- **Result**: No match! ❌

**Root Cause:**
- Tokenization stripped punctuation from source text words: "problemen." → "problemen"
- But glossary matching used the original entry WITH punctuation: "...problemen."
- Match failed because "problemen" ≠ "...problemen."

**The Fix:**
- Now strips trailing/leading punctuation from **both** source text AND glossary entries before matching
- Normalized term: "...problemen." → "...problemen"
- Source text: "...problemen." → "...problemen"
- **Result**: Match succeeds! ✅

**User Impact:**
- Users can now add full sentences to glossaries without worrying about punctuation
- Entries work correctly whether they have periods, quotes, or other punctuation at the end
- More natural workflow - copy/paste sentences directly into glossaries

**Files Modified:**
- `Supervertaler.py` - Added punctuation stripping to `find_termbase_matches_in_source()` (line ~31029-31031)

---

## 🐛 Fixed ALL Tab Navigation + Startup Tab (v1.9.116) - January 19, 2026

**What Was Wrong:**
The v1.9.115 fix for the "API Keys Missing" dialog navigation was incomplete - it still went to AutoFingers! The root cause was that `_go_to_settings_tab()` was using the **wrong tab index**.

**The Real Problem:**
When the Prompt Manager tab was added to the main tab bar, it shifted ALL subsequent tab indices:
- **Before**: Grid=0, Resources=1, Tools=2, Settings=3
- **After**: Grid=0, Resources=1, **Prompt Manager=2**, Tools=3, Settings=4

But `_go_to_settings_tab()` was still using index 3 (which is now Tools, not Settings)!

**What Was Fixed:**
- ✅ `_go_to_settings_tab()` now uses correct index 4 (Settings)
- ✅ "API Keys Missing" dialog now correctly navigates to Settings → AI Settings
- ✅ Navigate To menu items updated (Prompt Manager, Tools, Settings)
- ✅ First-run welcome dialog navigation fixed
- ✅ AutoFingers navigation fixed
- ✅ Superlookup hotkey handler fixed
- ✅ **Startup tab now Grid** (index 0) instead of Tools/AutoFingers

**User-Facing Changes:**
1. When you start Supervertaler, it now opens to the **Grid tab** (empty or with your last project)
2. "API Keys Missing" dialog **actually works** now - takes you to Settings → AI Settings
3. All menu navigation items work correctly

**Files Modified:**
- `Supervertaler.py` - Fixed 8+ locations with incorrect tab indices, added startup tab initialization

---

## 🐛 API Keys Dialog Navigation Fix (v1.9.115) - January 19, 2026

**Fixed "API Keys Missing" Dialog Navigation**

When users start Supervertaler without configured API keys, they see a dialog asking "Would you like to configure them now?" Clicking "Yes" should take them to Settings → AI Settings where they can configure their keys.

**The Bug:**
- Dialog navigation went to **Tools → AutoFingers** instead of **Settings → AI Settings**
- Users couldn't find where to configure their API keys

**The Fix:**
- Updated `_go_to_settings_tab()` to accept optional `subtab_name` parameter
- Dialog now calls `_go_to_settings_tab("AI Settings")` to navigate directly to the AI Settings sub-tab
- Users are now taken to the correct location where API keys can be configured

**Files Modified:**
- `Supervertaler.py` - Updated `_go_to_settings_tab()` method and API Keys Missing dialog handler

---

## 🔍 AI Assistant Diagnostic Logging (v1.9.114) - January 19, 2026

**Improved AI Assistant Troubleshooting**

Added diagnostic logging to help users troubleshoot API key issues:

- **Key Discovery Logging**: When AI Assistant initializes, it now logs which API keys were found
  - Example: "🔑 Found API keys for: openai, google, deepl"
  - If no keys found: "⚠ No API keys found in api_keys.txt"
  
- **Helps Diagnose Issues**:
  - Users can verify their API keys are being loaded correctly
  - Makes it clear which providers are available
  - Doesn't expose actual key values (only key names)

**Why This Helps**:
- User reported AI Assistant showing "not available" despite having keys configured
- New logging will show exactly which keys are detected
- Makes troubleshooting much easier for both users and developers

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Added API key discovery logging to `_init_llm_client()`

---

## 🔑🔐 API Key Loading System Unified (v1.9.113) - January 19, 2026

**Unified API Key Loading with Dev-First Priority**

Consolidated the confusing multi-path API key loading system into a single, clear dual-path approach that fixes AI Assistant bug #107:

**The Problem:**
- Three different API key file locations existed (root, user_data, user_data_private)
- Two different loading mechanisms (`Supervertaler.load_api_keys()` vs `llm_clients.load_api_keys()`)
- Conflicting instructions in example files
- **AI Assistant bug (#107)**: Keys worked for translation but failed for AI Assistant with "Incorrect API key" error

**The Solution:**
- **Unified loading in main app**: `load_api_keys()` now checks TWO locations with clear priority
  1. `user_data_private/api_keys.txt` (Dev mode - gitignored, never uploaded to GitHub)
  2. `user_data/api_keys.txt` (User mode - ships with app)
- **AI Assistant fixed**: Now uses `parent_app.load_api_keys()` instead of module function
- **Example files updated**: Both example files now give consistent, clear instructions

**Developer Workflow:**
- Store keys in `user_data_private/api_keys.txt`
- Fully gitignored - safe from accidental commits
- All features find keys here (translation, AI Assistant, tests)

**User Workflow:**
- Keys go in `user_data/api_keys.txt`
- App auto-creates this location on first run
- Simple, single location

**Files Modified:**
- `Supervertaler.py` - `load_api_keys()` method now checks dev path first (line ~39407)
- `api_keys.example.txt` - Updated with dev/user instructions
- `user_data/api_keys.example.txt` - Updated with dev/user instructions
- `README.md` - Updated First Steps with API key setup
- `AGENTS.md` - Updated API Keys section with new dual-path documentation

**Result:**
- ✅ Developers: Keys safe in gitignored location
- ✅ Users: Simple single location
- ✅ AI Assistant: Now works with same keys as translation
- ✅ No more confusion about where to put keys

---

## 🐛 Bug Fixes (v1.9.112) - January 19, 2026

**Filter Pagination Bug Fixed**

Fixed critical bug where Filter Source/Target boxes only searched visible page instead of all segments:

- **The Problem**: When pagination was active, filtering only searched through currently visible rows
- **Root Cause**: Used `self.table.rowCount()` which could be limited by pagination state
- **The Fix**: Now uses `len(segments)` to always search ALL segments in project
- **Result**: Filtering finds matches across entire project regardless of pagination settings

**Bilingual Table Export - Notes Column**

Fixed segment notes not being exported to Supervertaler Bilingual Table DOCX files:

- **The Problem**: Notes column was hardcoded to empty string `cells[4].text = ''`
- **The Fix**: Now properly exports `seg.notes` from each segment
- **Formatting**: 8pt font to match Status column styling
- **Includes**: Proofreading notes (⚠️ PROOFREAD prefix), user notes, all segment annotations

**Grid Column Width Optimization**

Reduced segment ID column width for more compact display:

- **Before**: 55px (unnecessarily wide)
- **After**: 40px (fits up to 3 digits comfortably, readable for 4+ digits)
- **Result**: More horizontal space for Source/Target columns

**Files Modified:**
- `Supervertaler.py` - Fixed `apply_filters()` iteration, notes export, column width

---

## 🔒 Clean Slate Project Imports (v1.9.111) - January 18, 2026

**Automatic Resource Deactivation on New Project Import**

New projects now start with a clean slate - all TMs, glossaries, and Non-Translatable lists are automatically deactivated on import:

- **Auto-Deactivation**: When importing a new project (DOCX, TXT, memoQ, CafeTran, Trados), all existing resources are deactivated
- **Explicit Activation**: Users explicitly activate only the resources they need for each project
- **Prevents Pollution**: Stops unintended resource bleeding across unrelated projects
- **Applied to All Imports**: Works consistently across all 5 import handlers

**User Workflow:**
1. Import new project → All resources deactivated automatically
2. Go to Project Resources tab → Activate needed TMs/glossaries
3. Work on project with only relevant resources active
4. Import next project → Clean slate again

**Technical Implementation:**
- New `_deactivate_all_resources_for_new_project()` method
- Deactivates TMs via `tm_metadata_mgr.deactivate_tm()`
- Deactivates glossaries via `termbase_mgr.deactivate_termbase()`
- Deactivates NT lists via `nt_manager.set_list_active(False)`
- Logs: "📋 New project: All TMs, glossaries, and NT lists deactivated (start clean)"

**Files Modified:**
- `Supervertaler.py` - Added deactivation method, called in all import handlers

---

## 🔄 Superconverter - Format Conversion Hub (v1.9.110) - January 18, 2026

**New Superconverter Tool - Document & Format Conversion**

Introduced a comprehensive format conversion tool under **Tools → Superconverter** with three tabs:

**1. Bilingual Table (Markdown Export)**
- Export project segments as AI-optimized Markdown tables
- Perfect for ChatGPT, Claude, Gemini - renders as clean tables in chat interfaces
- Options: bilingual, source-only, or target-only
- Filters: all segments, untranslated only, or translated only
- Language-tagged rows (e.g., `Dutch:`, `English:`)

**2. Document → Markdown Converter**
- Convert DOCX and TXT documents to structured Markdown
- **Single file conversion**: Choose file, set output location, convert
- **Batch conversion**: Select multiple files, output folder, convert all at once
- **Auto-detects ALL CAPS headings** (e.g., "TECHNISCH DOMEIN" → "## Technisch Domein")
  - Especially useful for patent documents and technical reports
- Preserves Word document structure:
  - Headings (H1-H6) → Markdown headings
  - Bulleted lists → Unordered lists
  - Numbered lists → Ordered lists
  - Paragraphs with proper spacing
  - Bold/italic formatting

**3. TMX Tools (Placeholder)**
- Prepared for future TMX conversion workflows
- More conversion workflows coming soon

**UI/UX Improvements:**
- All 11 Tools tab items now accessible via **Tools menu** for quick navigation
- Removed focus rectangles from buttons for cleaner appearance
- File → Export menu updated: "AI-Readable Format (TXT)" → "AI-Readable Markdown (.md)"

**Technical Details:**
- `create_superconverter_tab()` - New 3-tab converter interface
- `export_bilingual_table_markdown()` - Markdown table export with filters
- `convert_document_to_markdown()` - Single DOCX/TXT conversion
- `batch_convert_documents_to_markdown()` - Batch processing
- `_convert_docx_to_markdown()` - DOCX structure preservation + ALL CAPS detection
- `_convert_txt_to_markdown()` - TXT conversion + ALL CAPS detection
- `_navigate_to_tool()` - Helper for Tools menu navigation

**Files Modified:**
- `Supervertaler.py` - Complete Superconverter implementation (911 line insertions)

---

## 🔧 TMX Language Pair Bug Fix (v1.9.109) - January 18, 2026

**Fixed Critical TMX Import Language Reversal Bug**

**Issue ([#105](https://github.com/michaelbeijer/Supervertaler/issues/105)):** When importing TMX files, the language pair was sometimes reversed (EN-GB → DE-DE imported as DE-DE → EN-GB). This made it impossible to find matches for translated segments.

**Root Cause:** The TMX import code was incorrectly assuming that the FIRST language in the TMX file was the source language and the SECOND was the target language. However, TMX files list languages in arbitrary order (often alphabetically), so this assumption was wrong.

**Fix Implemented:**
- Added language pair selection dialog when importing TMX files
- User now explicitly selects which detected language should be source and which should be target
- Prevents accidental language reversal
- Applies to both "Create new TM from TMX" and "Add to existing TM" workflows

**User Workflow:**
1. Import TMX file
2. Dialog shows all detected languages (e.g., "de-DE, en-GB")
3. User selects: Source = en-GB, Target = de-DE
4. Import proceeds with correct language pair
5. TM matches now work correctly

**Files Modified:**
- `Supervertaler.py` - Added language selection dialog in `_import_tmx_as_tm()` method (2 locations)

---

## 📥📤 memoQ XLIFF Import/Export Support (v1.9.108) - January 18, 2026

**Complete memoQ XLIFF (.mqxliff) Workflow**

Added full import/export support for memoQ XLIFF files - feature was implemented in module but never exposed in UI:

**Implementation:**

1. **Import Menu Item**: File → Import → memoQ XLIFF (.mqxliff)...
   - Opens file dialog for `.mqxliff` files
   - Automatically extracts source segments using `MQXLIFFHandler`
   - Converts ISO language codes to full names (`sk` → `Slovak`)
   - Stores handler and source path for round-trip export

2. **Export Menu Item**: File → Export → memoQ XLIFF - Translated (.mqxliff)...
   - Updates target segments in original XLIFF structure
   - Preserves formatting tags (bpt/ept pairs)
   - Saves translated file with proper namespace handling

3. **Language Code Normalization**:
   - New `_normalize_language_code()` method
   - Converts ISO 639-1/639-2 codes to full language names
   - Supports 30+ languages including Slovak (`sk`, `sk-SK`)

4. **memoQ Bilingual DOCX Language Detection**:
   - Expanded `lang_map` in `import_memoq_bilingual()` from 8 to 24 languages
   - Now includes Slovak, Czech, Hungarian, Romanian, Bulgarian, Greek, Russian, Ukrainian, Swedish, Danish, Finnish, Norwegian, Japanese, Chinese, Korean, Arabic, Turkish, Hebrew
   - Fixes bug where Slovak would default to EN→NL instead of being detected

5. **Project Persistence**:
   - Added `mqxliff_source_path` field to `Project` dataclass
   - Source path saved in `.svproj` files
   - Automatic handler restoration when loading projects

**Round-Trip Workflow:**
1. Export from memoQ as XLIFF
2. Import into Supervertaler
3. Translate segments
4. Export back to XLIFF
5. Import into memoQ

**Files Modified:**
- `Supervertaler.py` - Import/export menu items, methods, language normalization
- `Supervertaler.py` - Project dataclass: added `mqxliff_source_path` field
- `Supervertaler.py` - Project save/load: persist mqxliff_source_path

**GitHub Discussion:**
- https://github.com/michaelbeijer/Supervertaler/discussions/106

---

## ✅ Prompt Library & Superlookup Fixes (v1.9.107) - January 15, 2026

**Prompt Library Improvements**

- **Unified filename and Name field**: Tree and editor now show full `.svprompt` extension
- **File Operations**: Name field edits now rename files on disk (filename = what you see = what you edit)
- **New Prompt Dialog**: Now asks for "filename with extension" and auto-appends `.svprompt` if missing

**Superlookup Navigation Fixes**

- **Fixed Ctrl+K AttributeError**: Removed ~140 lines of orphaned Supermemory code that was causing errors
- **Fixed Ctrl+K Navigation**: Now correctly navigates to Tools tab (index 3) instead of Prompt Manager (index 2)
  - Tab indices shifted when Prompt Manager was added: Tools moved from 2→3

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Tree display, editor field, save logic
- `Supervertaler.py` - Removed orphaned Supermemory methods, fixed tab index

---

## 🗑️ Supermemory Removed (v1.9.105) - January 15, 2026

**Major Architectural Change**

- **Removed Supermemory** (vector-indexed semantic search) from the project entirely
- Supermemory did not work reliably in frozen PyInstaller builds due to complex PyTorch native dependencies
- **Recommendation:** Focus development effort on improving the SQLite-based Translation Memory system
  - Better TMX import performance for large files
  - Advanced fuzzy matching algorithms
  - More reliable and faster than vector-based approaches for professional translation workflows

**Removed:**
- `modules/supermemory.py` (2100+ lines)
- Supermemory tab from UI
- Auto-init and cleanup code
- Dependencies: sentence-transformers, chromadb, tokenizers
- ~600 MB from default installation footprint

**Files Modified:**
- `Supervertaler.py` - Removed UI tab, auto-init, cleanup methods
- `modules/feature_manager.py` - Removed supermemory feature definition
- `pyproject.toml` - Removed supermemory pip extra and dependencies
- Build specs updated (CORE/FULL now only differ in Local Whisper inclusion)

## 📦 Packaging: Lighter Default Install (v1.9.104) - January 14, 2026

- Made **Supermemory** an optional install extra again, so the default `pip install supervertaler` no longer pulls the heavy ML stack (PyTorch / sentence-transformers / ChromaDB). Install with `pip install supervertaler[supermemory]` when needed.

## ✅ Filtered Ctrl+Enter + Website Screenshots (v1.9.103) - January 14, 2026

**Bug Fix**

- Fixed Ctrl+Enter confirmation under active **Filter Source/Filter Target**: it now confirms and advances through the *filtered* segments without the grid reverting to an unfiltered view.

**Website**

- Added new screenshots demonstrating the **Compare Panel** (MT + TM) and **Termview**.
- Updated the Prompt Manager screenshot reference.

## ⚡ QuickMenu in the Grid (v1.9.102) - January 14, 2026

- New **⚡ QuickMenu** in the Grid right-click menu (Source + Target cells)
  - Run a prompt and preview the response
  - Run a prompt and replace the selected text / target
- Prompt system update: renamed “Quick Run menu” terminology to **QuickMenu**
- New prompt metadata fields (backward compatible with `quick_run`):
  - `quickmenu_label` (menu label)
  - `quickmenu_grid` (show in Grid right-click QuickMenu)
  - `quickmenu_quickmenu` (show in future app-level QuickMenu)
- UI rename: main tab “📝 Project editor” → “📝 Grid”
**Framework:** PyQt6
**Status:** Active Development

**Note:** For historical information about legacy versions (Tkinter Edition, Classic Edition), see [legacy_versions/LEGACY_VERSIONS.md](legacy_versions/LEGACY_VERSIONS.md).

---

## 🧰 Prompt Library UX + Update Check Reliability (v1.9.101) - January 13, 2026

**Prompt Library**

- Prompt Library folders default to collapsed on first load and preserve expand/collapse + selection across refreshes.
- Added toolbar buttons: **Collapse all** / **Expand all**.
- Fixed **Duplicate** (creates a real copy with a unique “(copy …)” name) and adjusted **New Prompt** to create inside the currently selected folder.
- Added drag-and-drop moves for prompt files and folders (also supports dragging Favorites/Quick Run entries as shortcuts to move the underlying prompt).

**Check for Updates**

- Update check now uses a longer timeout and falls back to the GitHub releases page when `api.github.com` is slow/blocked.
- Fixed the update progress dialog briefly flashing and disappearing on some systems.
- Fixed a rare crash/auto-close issue where the first (API) network reply could finish after the fallback started and prematurely close/delete the active fallback request.

**Website**

- Navbar now includes a GitHub icon link + version pill, with cache-busting query strings for CSS/JS.

---

## ⌨️ Ctrl+Return Works Everywhere (v1.9.100) - January 13, 2026

**Bug Fix: Ctrl+Enter/Ctrl+Return confirmation now reliable**

- Fixed a Windows/Qt routing quirk where `Ctrl+Return` (main keyboard Return) could be swallowed before it reached the grid editor widgets and/or the global `QShortcut`.
- Implemented an application-level event filter that intercepts `Ctrl+Return` and `Ctrl+Enter` and triggers `confirm_selected_or_next()` when focus is in the editor grid context.
- Expanded the same behavior to also work when focus is in the **Filter Source** / **Filter Target** boxes.

---

## 🔊 Compare Panel Shortcuts + Sound Effects (v1.9.99) - January 12, 2026

**Feature: Compare Panel-first quick insert workflow**

- **Alt+0 / Alt+0,0 insertion (Compare Panel)**: Single-tap `Alt+0` inserts the current MT result; double-tap `Alt+0,0` inserts the current TM Target.
- **Full-segment replacement + single undo step**: Insertions replace the entire current target segment, wrapped in a single undo edit block.
- **Compare Panel navigation shortcuts**:
  - MT prev/next: `Ctrl+Alt+Left` / `Ctrl+Alt+Right`
  - TM prev/next: `Ctrl+Alt+Up` / `Ctrl+Alt+Down`
- **Context-aware match shortcuts**: Match navigation/insertion shortcuts now act only on the active panel (Compare Panel vs Translation Results), avoiding hidden-panel side effects.

**Feature: Minimalist sound effects + status-bar feedback**

- Added per-event **Windows sound mapping** (beeps or selected Windows `.wav` files) with a global enable toggle.
- Added **status bar “information bar” messages** for glossary entry add outcomes (added / duplicate / error).
- Sound effects are now **OFF by default** on fresh installs.

**UX: Reduced log spam**

- Collapsed repeated “Saved segment to TM(s)” messages into a single debounced log line with an `(xN)` count.

---

## 📝 Glossary Notes in Tooltips (v1.9.98) - January 11, 2026

**Bug Fix: Glossary Entry Notes Now Display in Tooltips**

Fixed an issue where glossary entry notes were not appearing in tooltips, even though they were correctly saved to the database.

**The Problem:**
- Notes were being saved correctly to the `termbase_terms.notes` database column
- However, when converting termbase matches from dictionary format to list format for display, the `notes` field was being dropped in multiple places
- This meant TermView tooltips and source cell tooltips never received the notes data

**The Fix:**
Fixed 5 locations where glossary notes were being lost:
1. **Cached termbase matches conversion** (lines ~26753-26768): Added `'notes'` field
2. **Fresh termbase matches conversion** (lines ~26835-26850): Added `'notes'` field  
3. **Refresh current segment conversion** (lines ~30420-30438): Added `'notes'` field
4. **TranslationMatch metadata** (lines ~30469-30485): Added `'notes'`, `'term_id'`, `'termbase_id'` to metadata dict

**Result:**
- Glossary entry notes now appear in TermView tooltips when hovering over terms
- Notes also appear in source cell tooltips for highlighted glossary terms
- Full data flow now preserved: Database → TranslationMatch → dict → list → TermBlock → Tooltip

**Also in this release:**
- **WebEngineView cleanup**: Fixed "Release of profile requested but WebEnginePage still not deleted" terminal warnings by properly cleaning up Superlookup web views on app close
- **FAQ update**: Added documentation about embedded browser password/cookie security in Superdocs FAQ
- **Community docs**: Added `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1)

---

## 🌐 All MT Providers in Translation Results (v1.9.97) - January 11, 2026

**Feature: Multiple Machine Translation Providers Now Displayed**

The Translation Results panel now shows translations from **all configured MT providers**, not just Google Translate.

**Previously:**
- Only Google Translate was called when navigating to a segment
- DeepL, Amazon Translate, and MyMemory were only available in Batch Translate

**Now:**
- All enabled MT providers are called and displayed progressively
- Each provider's translation appears as it completes
- Provider codes shown: GT (Google), DL (DeepL), AT (Amazon), MM (MyMemory)

**Supported MT Providers:**
| Provider | API Key Required | Notes |
|----------|-----------------|-------|
| Google Translate | Yes | `google_translate` key |
| DeepL | Yes | `deepl` key |
| Amazon Translate | Yes | `amazon_translate` + `amazon_translate_secret` + region |
| MyMemory | Optional | Free tier works without key; email gets higher limits |

**Configuration Tip:**
For MyMemory, you can use your email address as the key to get 10,000 words/day instead of 1,000:
```
mymemory = your.email@example.com
```

**Technical Changes:**
- Expanded `_add_mt_and_llm_matches_progressive()` to call all configured MT providers
- Each provider respects its enabled/disabled state from Settings → MT Settings
- Results displayed immediately as each provider responds

---

## 🛡️ Thread-Safe Logging (v1.9.96) - January 11, 2026

**Bug Fix: Crash When Adding Terms via Alt+Down**

Fixed a critical crash that occurred when adding glossary terms using the Alt+Down quick-add shortcut.

**The Problem:**
- The `log()` method was being called from background worker threads (e.g., termbase batch processor)
- Qt widgets like `status_bar` and `session_log_text` were being accessed from non-main threads
- This violates Qt's threading model and caused: `QObject::killTimer: Timers cannot be stopped from another thread`

**The Fix:**
- Made `log()` method thread-safe using PyQt signals
- Added `_log_signal = pyqtSignal(str)` to `SupervertalerQt` class
- Background threads now emit the signal instead of directly updating UI
- Signal automatically queues to main thread's event loop
- Console logging (`print()`) still works from any thread

**Technical Details:**
- New `_log_to_ui()` internal method handles actual widget updates
- Thread detection via `threading.current_thread() == threading.main_thread()`
- Signal connected with default `AutoConnection` which queues cross-thread calls

**Result:**
- No more crashes when background workers log messages
- Alt+Down quick-add works reliably
- All UI updates properly marshalled to main thread

---

## 🔍 TM Fuzzy Matching Fix (v1.9.95) - January 11, 2026

**Bug Fix: Improved Translation Memory Fuzzy Matching for Long Segments**

Fixed a critical issue where highly similar TM entries were not being found for long segments (especially in patent/technical documents).

**The Problem:**
- FTS5 full-text search uses BM25 ranking which prioritizes entries matching more search terms
- For long segments with many technical compound words, BM25 pushed truly similar entries below the candidate limit
- Example: Two sentences that were 92% similar weren't matching because other entries matched more individual words

**The Fix:**
- Increased the FTS5 candidate pool from 100 to 500 entries
- This ensures similar entries make it into the candidate pool before SequenceMatcher calculates actual similarity
- More candidates = better chance of finding the truly similar matches

**Technical Details:**
- Changed `max(50, max_results * 10)` to `max(500, max_results * 50)` in `search_fuzzy_matches()`
- FTS5 BM25 is great for keyword relevance but needs a larger pool for similarity-based reranking
- The SequenceMatcher then correctly scores the candidates by actual text similarity

**Result:**
- TM fuzzy matches now reliably appear for long technical segments
- 90%+ similar entries are no longer missed due to BM25 ranking artifacts

---

## 🎯 TermView Quick-Insert Shortcuts (v1.9.94) - January 11, 2026

**New Feature: TermView Quick-Insert Shortcuts**

**Note (v1.9.99+):** `Alt+0` / `Alt+0,0` are now reserved for the Compare Panel insertion workflow. TermView shortcuts start at `Alt+1`.

Insert glossary terms directly from TermView using keyboard shortcuts — a novel feature not found in other CAT tools!

- **Alt+1 through Alt+9** — Insert terms 1-9 (displayed as badges 1-9)
- **Double-tap Alt+N,N** — Insert terms 10-18 (displayed as badges 11, 22, ..., 99)
- **18 terms accessible** via quick keyboard shortcuts
- **Visual badges** show shortcut numbers on each term in TermView
- **Smart double-tap detection** — first tap inserts immediately, double-tap within 300ms replaces with the 11-20 term

**Visual Improvements:**
- 🎨 **Unified term styling** — Background color now extends across both translation text and shortcut badge
- 🔵 **Blue number badges** — Clear visual indicators (14px for single digit, 20px for double)
- 💡 **Hover effects** — Entire term block highlights on hover
- 🏷️ **Tooltips** — Show exact shortcut (e.g., "Press Alt+3 to insert" or "Press Alt+3,3 to insert")

**How It Works:**
| Badge | Shortcut | Term # |
|-------|----------|--------|
| 1-9 | Alt+1-9 | 1st-9th terms |
| 11-99 | Alt+1,1 - Alt+9,9 | 10th-18th terms |

---

## ⌨️ Keyboard Shortcuts & Quick Glossary Add (v1.9.93) - January 11, 2026

**New Features:**
- ⚡ **Quick Add to Priority Glossary** — Add terms directly to glossaries by their priority ranking
  - Alt+Up: Add selected term pair to glossary with Priority #1
  - Alt+Down: Add selected term pair to glossary with Priority #2
  - Works with any glossary that has Read enabled and a priority set
  - No dialog required — instant term addition

- 🔧 **Shortcut Enable/Disable** — Disable shortcuts from Settings → Keyboard Shortcuts
  - New "Enabled" checkbox column in shortcuts table
  - Disabled shortcuts fully release their key combinations
  - Released keys can be reassigned to other shortcuts
  - Settings persist between sessions

**Improvements:**
- ✓ **Button Renamed** — "Save & Next" button renamed to "Confirm & Next" to accurately reflect its function
- ⌨️ **Ctrl+Enter Fix** — Ctrl+Enter now correctly handled in target editor cells
- ↵ **Enter Key Behavior** — Plain Enter no longer inserts newlines; use Shift+Enter for line breaks

**Bug Fixes:**
- 🔧 Fixed Ctrl+Enter not working when focus is in target cell
- 🔧 Fixed "Save & Next" button not confirming segments (was only moving to next)
- 🔧 Fixed custom shortcut key bindings not loading at startup

---

## 🔄 F5 Force Refresh & Curly Quote Matching (v1.9.92) - January 10, 2026

**New Feature:**
- ⌨️ **F5 Force Refresh** — Press F5 to force refresh all glossary and TM matches for the current segment
  - Clears all caches (termbase cache, translation matches cache)
  - Re-searches all connected glossaries and translation memories
  - Updates TermView, Translation Results panel, and grid highlighting with fresh results
  - Useful when glossary changes aren't immediately reflected

**Bug Fixes:**
- 🔤 **Curly Quote Matching Fix** — Single-word glossary terms now correctly match when surrounded by curly quotes
  - Terms like `"omvatten",` or `„word"` now match their glossary entries
  - Comprehensive Unicode quote handling: `"`, `"`, `„`, `«`, `»`, `'`, `'`, `‚`, `‹`, `›`
  - Text normalized by replacing all quote variants with spaces before regex matching

**Improvements:**
- 🏷️ **TermView Tag Stripping** — CAT tool tags now stripped from TermView display for cleaner appearance
  - Handles `<b>`, `<i>`, memoQ `{1}`, `[2}`, Trados `<1>`, Déjà Vu `{00001}`
- 📝 **Find/Replace Field Behavior** — Selected text now always goes to Find field, never to Replace field
- 🔄 **TermView Cache Updates** — TermView now updates from cache when navigating segments (not just TM/MT results)

---

## 🎯 Déjà Vu X3 Bilingual RTF Support (v1.9.91) - January 10, 2026

**New CAT Tool Integration:**
- 📄 **Déjà Vu X3 RTF Import** — Import bilingual RTF files exported from Déjà Vu X3
  - Parses 4-column table format (ID | Source | Target | Comments)
  - Automatic language detection from RTF language codes (60+ languages supported)
  - Segment IDs preserved for round-trip workflow
- 📤 **Déjà Vu X3 RTF Export** — Export translations back to RTF format
  - Translations inserted with proper RTF formatting
  - Unicode characters properly encoded (`\uNNNN?` format)
  - Target language codes applied automatically
  - Balanced RTF brace structure maintained
- 🏷️ **Déjà Vu Tag Support** — Inline tags `{00108}` highlighted in pink
  - Pattern: `{NNNNN}` (5-digit numbers)
  - Tags preserved through translation workflow
- 🔄 **Full Round-Trip Workflow**:
  1. Export bilingual RTF from Déjà Vu X3
  2. Import into Supervertaler (File → Import → Déjà Vu Bilingual RTF)
  3. Translate using AI, TM, or manual editing
  4. Export back to RTF (File → Export → Déjà Vu Bilingual RTF)
  5. Reimport into Déjà Vu X3

**New Module:**
- `modules/dejavurtf_handler.py` — Complete Déjà Vu X3 RTF parser (~800 lines)
  - `DejaVuSegment` dataclass for segment data
  - `DejaVuRTFHandler` class with load/save methods
  - RTF text encoding/decoding utilities
  - Language code mapping for 60+ languages

**Technical Implementation:**
- RTF parsing uses regex patterns for `\cell` markers and segment IDs
- Segment IDs extracted via pattern `insrsid\d+\s+(\d{7})\}`
- Language detection uses `Counter` to find most common `\lang` codes
- Export inserts formatted RTF groups with proper brace balancing
- Project persistence: `dejavu_source_path`, `dejavu_segment_id`, `dejavu_row_index`

**Files Modified:**
- `Supervertaler.py` — Menu items, import/export methods, TagHighlighter pattern
- `modules/dejavurtf_handler.py` — NEW handler module

---

## 🐛 Bug Fixes (v1.9.89) - January 9, 2026

**Critical Bug Fixes:**
- 🔧 **Translation Results Zoom Persistence** — Fixed font size settings not being restored when loading projects (typo: `set_compare_font_size` → `set_compare_box_font_size`)
- 🎨 **Border Thickness Spinbox** — Fixed arrows not appearing in Target Cell Focus Border thickness control
  - Removed problematic stylesheet that was hiding buttons
  - Increased maximum thickness from 5px to 10px
  - Made spinbox wider (90px) to accommodate larger values
- 🌍 **Language Pair Memory** — Fixed DOCX import defaulting to EN→NL instead of remembering last used language pair
  - Now remembers last imported language pair across sessions
  - Falls back to current project languages if available
  - User report: "Whatever I do... the language is detected always as EN-NL!" → FIXED

**Files Modified:**
- `Supervertaler.py` — All bug fixes implemented

---

## 🔍 Context Menu Enhancement (v1.9.88) - January 9, 2026

**Superlookup Integration in Context Menus (NEW):**
- 🔍 **Quick Concordance Search** — Right-click selected text in source or target cells to instantly search in Superlookup
- 📋 **Context Menu Item** — New "🔍 Search in Superlookup (Ctrl+K)" option appears when text is selected
- 🎯 **Smart Navigation** — Automatically opens Superlookup tab and triggers search
- 🌍 **Language-Aware** — Passes project language pair to Superlookup for filtered results
- 📊 **Vertical View** — Uses traditional concordance list layout for search results
- ⚡ **Unified Search** — Searches TM, glossaries, Supermemory, MT, and web resources simultaneously
- 🔄 **Works Everywhere** — Available in both source (read-only) and target (editable) cells

**Workflow Benefits:**
- Select any term → Right-click → Instant concordance search (no need to open Superlookup first)
- Perfect for terminology research while translating
- Complements existing Ctrl+K keyboard shortcut

---

## ⚡ Workflow Enhancements & UI Polish (v1.9.87) - January 9, 2026

**Auto-Confirm 100% TM Matches (NEW):**
- 🎯 **Intelligent Auto-Confirmation** — When pressing Ctrl+Enter, automatically inserts, confirms, and skips segments with perfect TM matches
- 🔄 **Recursive Processing** — Continues through multiple 100% matches until finding a segment requiring manual work
- 🛡️ **Safety Check** — Only auto-confirms segments with empty targets (won't overwrite existing translations)
- ⚡ **Hash-Based Lookup** — Uses instant MD5 hash matching for O(1) performance
- 📊 **TM Integration** — Auto-confirmed segments automatically saved to active Translation Memories
- ⚙️ **Optional Setting** — Enable/disable in General Settings → TM/Glossary section
- 📝 **Session Logging** — Clear logs show: Found match → Auto-confirmed → Skipped to next

**Tab Layout Customization (NEW):**
- 📐 **Flexible Tab Position** — Move Termview and Session Log tabs above or below the grid
- ⚙️ **View Settings Toggle** — New "📐 Tab Layout" section with checkbox: "Show Termview/Session Log tabs above grid"
- 💾 **Persistent Setting** — Preference saved and restored between sessions
- 🔄 **Easy Switching** — Close and reopen project tab to apply layout change

**Grid & UI Improvements:**
- 📏 **Wider Segment Column** — Segment # column increased from 35px to 55px (fits 4-digit segment numbers up to 9999)
- 🎯 **Auto-Center Fix** — "Keep Active Segment Centered" setting now persists between restarts
- 🎨 **Badge Text Color** — Changed from black to dark gray (#333333) for better appearance on bright match backgrounds
- 🎨 **Color Customization** — New badge text color picker with 8 preset colors and custom selection
- 🔍 **Settings Rename** — "View/Display" tab renamed to "View Settings" for clarity

**Technical Improvements:**
- Navigation logic now uses exact match lookup for 100% TM matches (not fuzzy search)
- Pagination handling in auto-confirm recursion (switches pages when needed)
- Status icon updates and project modification flag management
- Settings persistence through general_settings.json

---

## 🔧 Glossary Quality Improvements (v1.9.86) - January 9, 2026

**Enhanced Glossary Management:**
- 🚫 **Duplicate Prevention** — Cannot save duplicate source→target pairs to a glossary
- 🎯 **Priority-Based Filtering** — If identical match exists in multiple glossaries, only highest priority version shown
- ⚖️ **Font Normalization** — TermView source and target text now use same font size
- 🔍 **Smart Filtering** — Duplicate filtering applied throughout: grid highlighting, Translation Results, TermView, and Superlookup
- ⚠️ **User Feedback** — Clear warning dialog when attempting to add duplicate terms

**Technical Changes:**
- Added case-insensitive duplicate check in `termbase_manager.py` before inserting terms
- `add_term()` now returns `None` if duplicate detected (graceful handling)
- Duplicate filtering in `find_termbase_matches_in_source()` prevents multiple sources from showing duplicates
- TermView target font size matches source font size (was 2pt smaller)

---

## ✅ AI Proofreading System (v1.9.85) - January 7, 2026

**Intelligent Translation Quality Verification:**
- 🔍 **Batch Proofreading** — LLM analyzes translations for errors, inconsistencies, and quality issues
- 📝 **Issue Tracking** — Problems stored in Notes field with `⚠️ PROOFREAD:` prefix
- 📊 **Results Table** — View all segments with issues, double-click to navigate
- 🎯 **Advanced Filters** — New "Has proofreading issues" filter option
- 🟠 **Visual Indicators** — Orange highlight on status icons for segments with proofreading notes
- 🧹 **Clear Operations** — Bulk clear all proofreading notes or clear individual segments
- ⚡ **Batch Processing** — Efficient API calls (20 segments per request)
- 📈 **Progress Dialog** — Real-time stats during proofreading operation

**Access Points:**
- Edit → Batch Operations → ✅ Proofread Translation...
- View → ✅ Proofreading Results...
- Right-click → ✅ Clear Proofreading Notes

---

## 📐 Subscript & Superscript Support (v1.9.84) - January 7, 2026

**New Formatting Tags:**
- ⬇️ **Subscript** — `<sub>` tags for subscript text (e.g., P<sub>totaal</sub>)
- ⬆️ **Superscript** — `<sup>` tags for superscript text (e.g., m<sup>2</sup>)

**Full Pipeline Support:**
- 📥 **Import** — Subscript/superscript preserved from DOCX files as `<sub>`/`<sup>` tags
- 📤 **Export** — Tags converted back to real Word subscript/superscript formatting
- 🎨 **Preview** — Document Preview renders actual subscript/superscript positioning

**Technical Details:**
- Updated `modules/tag_manager.py` with sub/sup support in FormattingRun dataclass
- TAG_PATTERN regex extended to match `<sub>` and `<sup>` tags
- DOCX handler applies `run.font.subscript` and `run.font.superscript` on export

---

## 📝 Notes Tab & Status Indicator (v1.9.83) - January 6, 2026

**Notes Tab in Translation Results Panel:**
- 📝 **TM Info + Notes Tabs** — Translation Results panel now has tabbed interface
- 💾 **TM Info Tab** — Shows TM match details when a match is selected
- ✏️ **Notes Tab** — Add/edit notes for each segment
- 🔄 **Auto-Save** — Notes save automatically as you type
- 📂 **Persistence** — Notes saved to .svproj project file

**Notes Indicator on Status Icon:**
- 🟠 **Orange Highlight** — Status icon (✓/✗) gets orange background when segment has notes
- 🎯 **Compact Design** — No separate icon cluttering the status cell
- 💬 **Tooltip** — Hover over status cell to see notes preview
- 📏 **Narrower Status Column** — Reduced from 120px to 70px for cleaner look

**UI Cleanup:**
- 🗑️ **Removed Comments Tab** — Redundant tab under grid removed (Notes tab replaces it)
- 🧹 **Cleaner Layout** — Only Termview and Session Log tabs remain under grid

---

## 🤖 Export for AI (v1.9.82) - January 5, 2026

**New Export Format:**
- 🤖 **AI-Readable Format** — New export option in File → Export menu
- 📝 **[SEGMENT XXXX] Format** — Outputs clean numbered segments with language labels
- 🌐 **Language Codes** — Auto-detects project languages (NL, EN, DE, etc.)
- ⚙️ **Configurable** — Customizable language codes, start number, zero padding

**Export Options:**
- 🔄 **Content Modes** — Bilingual (source+target), Source only, Target only
- 📊 **Segment Filters** — All segments, Untranslated only, Translated only
- 👁️ **Live Preview** — See format preview before exporting

**Use Cases:**
- 🧠 **AI Translation** — Export source-only for ChatGPT/Claude translation
- 🔍 **AI Review** — Export bilingual for AI quality review
- 📎 **Easy Parsing** — Simple format for automated processing

---

## 🔍 Superlookup UX Improvements (v1.9.81) - January 4, 2026

**Search History Dropdown:**
- 📜 **History Dropdown** — Superlookup search box now shows last 20 searches in dropdown
- 💾 **Persistent History** — Saved to `user_data/superlookup_history.json`
- ⌨️ **Editable Combo** — Type to search, click dropdown for history

**Resizable Sidebar:**
- ↔️ **QSplitter** — Web Resources sidebar now resizable (120-250px range)
- 📏 **No Text Cutoff** — Resource buttons properly visible at all widths

**UI Polish:**
- 🎯 **Focus Rectangles Removed** — Global stylesheet removes ugly focus outlines from all buttons
- 🟢 **Styled Radio Buttons** — Replaced 5 plain QRadioButton instances with CheckmarkRadioButton
- 🐛 **External Mode Fix** — External browser mode now correctly triggers web search

---

## 💻 GitHub Code Search (Beijerterm) in Superlookup (v1.9.80) - January 4, 2026

**New Web Resource:**
- 💻 **GitHub Code (Beijerterm)** — Search Beijerterm terminology repo directly from Superlookup
- 🔗 **Search URL** — `https://github.com/search?q={query}+repo:michaelbeijer/beijerterm&type=code`
- 📚 **Source Files** — Search YAML glossary files, Markdown documentation
- ✨ **Renamed** — "GitHub Code" → "GitHub Code (all)" for clarity

---

## 📚 Beijerterm Integration in Superlookup (v1.9.79) - January 4, 2026

**New Web Resource:**
- 📚 **Beijerterm** — Added to Superlookup's Web Resources tab (replaces old michaelbeijer.co.uk wiki)
- 🔗 **Search URL** — `https://michaelbeijer.github.io/beijerterm/?q={query}`
- 📊 **500k+ Terms** — Dutch-English terminology database with 583,000+ term entries
- ⚡ **URL Search** — Beijerterm now supports `?q=searchterm` for programmatic search integration

---

## 🔍 Find & Replace History & Batch Sets (v1.9.78) - January 4, 2026

**F&R History Dropdowns:**
- 📜 **History Dropdowns** — Find and Replace fields now have dropdown arrows showing last 20 searches
- 💾 **Persistent History** — Search/replace terms saved to `user_data/find_replace_history.json`
- 🔽 **Quick Access** — Click dropdown arrow or type to filter previous search terms

**F&R Sets (Batch Operations):**
- 📁 **F&R Sets Panel** — Collapsible panel for creating and managing batch replace operations
- ▶️ **Batch Operations** — Run multiple find/replace operations with a single click
- ➕ **Add to Set** — Save current find/replace values to a named set
- 📥📤 **Import/Export** — Save F&R sets as `.svfr` files for sharing or backup
- 🖱️ **Double-click** — Double-click any operation in a set to load it into the dialog

**New Module (`modules/find_replace_qt.py`):**
- `FindReplaceHistory` — Manages and persists recent search/replace terms
- `FindReplaceOperation` — Dataclass for single F&R operation (find, replace, options)
- `FindReplaceSet` — Collection of operations that can be saved/loaded
- `FindReplaceSetsManager` — QWidget UI for managing F&R sets with tables
- `HistoryComboBox` — Editable combo box with history dropdown

---

## 💻 GitHub Code Search in Superlookup (v1.9.77) - January 4, 2026

**New Web Resource:**
- 💻 **GitHub Code Search** — Added to Superlookup's Web Resources tab
- 🔗 **Search URL** — `https://github.com/search?q={query}&type=code`
- 🎯 **Use Case** — Search for terms/code across all public GitHub repositories
- ✨ **Great for** — Finding how technical terms are used in real code, locating terminology in open-source projects

---

## 🎉 Onboarding, Spellcheck & Project Info (v1.9.76) - January 3, 2025

**First-Run Welcome for New Users:**
- 🎉 **Welcome Dialog** — Shows on first launch explaining modular pip extras
- 📦 **Auto-Navigate** — Opens Settings → Features tab automatically to show installed/missing features
- ✅ **Don't Show Again** — Checkbox uses standard green CheckmarkCheckBox style
- 🐛 **Bug Fix** — First-run flag now saves to correct file (ui_preferences.json)

**Free vs Paid LLM Pricing Info:**
- 💰 **Info Box in AI Settings** — Clear pricing information at top of Settings → AI Settings
- 🆓 **Google Gemini** — FREE tier (15 req/min, 1M tokens/day)
- 🖥️ **Ollama** — 100% FREE (runs locally on your computer)
- 💳 **OpenAI/Claude** — Paid API only (no free tier)
- ⚠️ **Important Note** — Clarifies that ChatGPT Plus and Claude Pro web subscriptions do NOT include API access

**Spellcheck System Overhaul:**
- 🔤 **Spylls Backend** — Replaced `cyhunspell` with `spylls` (pure Python Hunspell), fixing Windows/Python 3.12 compatibility
- 🌍 **Language Variants** — Dropdown now shows "English (US)", "English (GB)", "Portuguese (BR)" etc.
- 📁 **Subdirectory Search** — Finds dictionaries in subfolders like `dictionaries/en/en_GB.dic`
- ✅ **Regional Spelling Works** — "colour" correct in en_GB, incorrect in en_US (and vice versa)
- 📋 **Improved Spellcheck Info Dialog** — Three backends displayed separately, active one highlighted green, bundled dictionary info, project links section

**Project Info Dialog (NEW):**
- 📋 **File → Project Info...** — New menu item to view comprehensive project information
- 📊 **Statistics** — Segment counts, word counts, character counts, progress percentage
- 📁 **Source Files** — Shows original DOCX, memoQ, CafeTran, Trados paths
- 🔧 **Resources** — Active prompt, TMs, glossaries, spellcheck settings

---

## 📦 Modular Architecture (v1.9.75) - January 2, 2025

**Major new feature: Install only the features you need!**

- 📦 **Modular Installation System** — Users can now choose which features to install, reducing disk space from ~1.2 GB (full) to ~300 MB (core only). Heavy dependencies like sentence-transformers, chromadb, and PyQt6-WebEngine are now optional.
- ⚙️ **Settings → Features Tab** — New settings page showing which optional features are installed (✅) vs not installed (❌), with size estimates and pip install commands for each.
- 🔧 **Feature Manager Module** — New `modules/feature_manager.py` provides `FeatureManager` class, `FEATURE_MODULES` definitions, and lazy import helpers for conditional loading.
- 📋 **pip Extras Support** — Install specific features with `pip install supervertaler[supermemory,voice,web]` or everything with `pip install supervertaler[all]`.

**Installation Options:**
| Command | Size |
|---------|------|
| `pip install supervertaler` | ~300 MB (core) |
| `pip install supervertaler[supermemory]` | +600 MB |
| `pip install supervertaler[voice]` | +150 MB |
| `pip install supervertaler[web]` | +100 MB |
| `pip install supervertaler[all]` | ~1.2 GB |

---

## 🔁 Maintenance Update (v1.9.74) - December 31, 2025

- 🧹 **Removed in-app Superdocs viewer & generator** — The documentation generator and Qt viewer have been deprecated and removed from the application; official documentation is now hosted on GitBook: https://supervertaler.gitbook.io/superdocs/. The app now directs users to the online Superdocs. Packaging metadata and site links updated accordingly.
- 📚 **Superdocs tooling docs refreshed** — Expanded the Tools section documentation (TMX Editor, AutoFingers, Supervoice voice commands, Image Extractor) to match the current UI and workflows.
- 🔍 **Superdocs Superlookup docs refreshed** — Expanded the Superlookup docs (TM search, glossary search, MT, web resources) to match current UI behavior and shortcuts.
- 🧩 **Superlookup copy/insert fix** — TM/Glossary results now store plain text in table items (while still rendering highlighted rich text), so copy/insert actions work reliably.

---

## 🌟 Recent Highlights - What's New in Supervertaler

**Latest Major Features:**

- 📝 **External Prompt Editor Display (v1.9.73)** - External prompts (not in the library) now display in the Prompt Editor panel when loaded or restored from a project. Editor shows name, description, and content fields. Edits can be saved back to the original file (.svprompt files save as JSON, .txt/.md as plain text). Visual indicator shows "📁 External: {name}" to distinguish from library prompts. Projects now correctly display their stored prompts (both external and library) in the editor when loaded.
 - 🔎 **Find & Replace: History, Reusable Sets & Batch Projects (v1.9.73)** - Added a dropdown history to the Find & Replace dialog that stores the last X entries for quick reuse. Users can save a sequence of find/replace operations as a reusable F&R project file, export/import these files, and run them as a batch on future projects. New UI includes a history dropdown, `Save/Load F&R Project` actions, and a `Run F&R Project` batch dialog with preview/dry-run and progress reporting.
- ⌨️ **Go to Segment Dialog (v1.9.71)** - Improved Ctrl+G shortcut with a minimal, streamlined dialog. Just type the segment number and press Enter - no need to click buttons. Global shortcut now works from anywhere in the application. Input field validates segment numbers and shows current position as placeholder. **Pagination-aware**: automatically switches to the correct page when jumping to segments on other pages. Cursor is placed in the target cell ready to edit.
- 📄 **Page Up/Down Pagination Navigation (v1.9.69)** - Page Up and Page Down keys now navigate through pagination pages! Press Page Up to go to the previous page, Page Down to go to the next page. Shortcuts appear in Settings → Keyboard Shortcuts under "Grid Navigation" category.
- 🎨 **memoQ Tag Color as Default (v1.9.68)** - Changed default tag highlight color to memoQ's actual dark red (`#7f0001`), color-picked directly from memoQ. Updated everywhere: grid cells, Translation Results panel, Settings defaults. Added 8 preset colors to the color picker (memoQ red, memoQ orange, Trados blue/purple, etc.). Each CAT tool export preserves its native tag colors (memoQ, Trados, Phrase, CafeTran). Supervertaler's own Bilingual Table export now uses memoQ red. Reset button updated to restore memoQ red.
- ⚡ **Performance Boost & Cache Fix (v1.9.66)** - Significantly faster segment navigation! Fixed termbase cache not working - empty results were being re-searched on every visit instead of being cached. Reduced verbose logging overhead that was slowing down navigation. Cache now properly stores and respects empty results using membership check (`segment_id in cache`). Removed per-word termbase search logging, per-match logging, prefetch progress logging, and MT/TM debug logging. Navigation should feel much snappier now.
- 📄 **Working Grid Pagination (v1.9.64)** - Grid pagination now actually works! Previously pagination controls existed but didn't filter the displayed segments. Now when you select "50 per page", only 50 segments are shown at a time. Use First/Prev/Next/Last buttons or type a page number to navigate. Efficient show/hide approach without grid reload for fast page changes.
- 🔄 **Batch Translate Retry Until Complete (v1.9.64)** - New "🔄 Retry until all segments are translated" option in batch translate dialog (enabled by default). If some segments fail or return empty after the first pass, automatically retries just those segments. Continues until all segments have translations or max 5 retries reached. No more running batch translate 2-3 times manually!
- 🤖 **Prompt Manager Tab Rename (v1.9.64)** - "Prompts" tab renamed to "Prompt manager" in Project resources for clarity.
- 📁 **External Prompt Restoration (v1.9.64)** - Fixed external prompts (from outside the library folder) not being restored when loading a project. External prompts are now correctly saved with `[EXTERNAL]` prefix and restored on project load.
- 🐧 **Linux Stability Fix (v1.9.63)** - Fixed memory access violations (segfaults) that could occur on Linux when clicking in the grid after importing a Trados package. Native code libraries (Hunspell, ChromaDB) can crash on Linux with improper dictionaries. Added safer Hunspell initialization with test spell check, crash detection flag to auto-disable spellcheck if it fails, and protected spellcheck highlighting with try/except. AutoHotkey registration now skipped entirely on Linux/Mac (no more "AutoHotkey not found" warnings). Linux users: if crashes persist, disable spellcheck in Settings or install proper Hunspell dictionaries (`sudo apt install hunspell-pl` for Polish).
- 🧹 **Dead Code Cleanup (v1.9.62)** - Removed ~230+ lines of deprecated and unused code. Cleaned up: `toggle_sidebar`, `handle_ribbon_action`, `create_toolbar`, `_render_paragraph`, deprecated termview methods, and verbose debug logging. Added missing `spellcheck_settings` field to Project dataclass with proper initialization. Removed unnecessary `hasattr()` checks. AutoFingers UI simplified by removing single-tab QTabWidget wrapper.
- 🔍 **Tag-Aware TM Matching (v1.9.60)** - Translation Memory fuzzy matching now works regardless of whether segments contain formatting tags! Searches both with and without tags, so `<b>Hello</b>` matches `Hello` in your TM. Similarity calculation also strips tags before comparing, giving accurate match percentages. Added `<li-b>` and `<li-o>` list item tags to TMX Tag Cleaner. Removed unused TMX Manager tab from AutoFingers - Import from TM button now in Control Panel.
- 🧹 **TMX Tag Cleaner (v1.9.59)** - New tag cleaning function in TMX Editor and main application! Access via Edit → Bulk Operations → Clean Tags, or the 🧹 Clean Tags toolbar button in TMX Editor. Select which tags to clean (formatting, TMX/XLIFF inline, memoQ, Trados, generic XML), choose replacement (remove or replace with space), and scope (source, target, or both). Cleans ALL languages in TMX regardless of display, not just visible pair. Handles both literal `<b>` and XML-escaped `&lt;b&gt;` tags. TMX Editor language dropdowns now correctly default to different languages (source→target, not source→source). AutoHotkey setup dialog now has "Do not show again" checkbox.
- 🏠 **Flattened Tab Structure (v1.9.57)** - Simplified main navigation from nested tabs to flat structure. The old "Workspace → Editor / Resources" hierarchy is now: **Project editor** | **Project resources** | **Tools** | **Settings**. All four tabs are now at the top level for easier navigation. Capitalization follows lowercase style for subtabs (e.g., "Project editor" not "Project Editor").
- ✏️ **Glossary Renaming (v1.9.56)** - Right-click on any glossary in Project resources → Glossaries tab to rename it. Previously, editing the name in the UI appeared to work but didn't actually save to the database. Now uses proper rename dialog with database persistence. Name column is no longer misleadingly editable inline.
- ⚡ **Lightning-Fast Filtering (v1.9.55)** - Filter operations (Ctrl+Shift+F) now run instantly instead of taking ~12 seconds! Optimized to avoid grid reload - only shows/hides rows and applies yellow highlights. **Ctrl+Shift+F toggle**: press once to filter on selected text, press again to clear the filter. Clear filter also listed separately in keyboard shortcuts for discoverability.
- 📋 **Superlookup Termbase Enhancements (v1.9.53)** - Improved Glossaries tab with additional metadata columns: Glossary name, Domain, Notes. Full metadata in results including priority, project, client, forbidden status. Tooltips show full content on hover.
- 📥 **Glossary Import Progress Dialog (v1.9.53)** - Real-time progress dialog when importing glossaries from TSV files. Visual progress bar, live statistics (✅ imported, ⏭️ skipped, ❌ errors), scrolling log window with color-coded entries.
- 🌐 **Superlookup Web Resources (v1.9.52)** - Expanded web resources tab with 14 reference sites! New resources: Juremy, michaelbeijer.co.uk, AcronymFinder, BabelNet, Wiktionary (Source & Target). Persistent login sessions with cookies stored in `user_data/web_cache/`. Auto-select language pair from project on load. Compact single-line search layout. Settings checkboxes control sidebar button visibility.
- 🔍 **Superlookup MT Integration (v1.9.51)** - Complete Machine Translation integration in Superlookup! Search now returns results from Google Translate, Amazon Translate, DeepL, Microsoft Translator, ModernMT, and MyMemory. MT provider status display shows active/disabled/missing API key providers with "⚙️ Configure in Settings" link. Error messages now shown in red with details (no more silent failures). Fixed language name mapping: "Dutch" → "nl", "English" → "en" for all MT providers. Added boto3 and deepl to requirements.txt. Removed debug print spam. Termbases tab now has search filter and split-view with editable terms grid.
- 🎤 **Voice Commands System (v1.9.50)** - Complete hands-free translation with Talon-style voice commands! Say "next segment", "confirm", "source to target", "translate", and more. **Always-On Listening Mode** with VAD (Voice Activity Detection) - no need to press F9. Dual recognition engines: **OpenAI Whisper API** (recommended, fast & accurate) or local Whisper model. New grid toolbar button (🎧 Voice ON/OFF) for easy toggle. Status bar indicator shows listening/recording/processing state. AutoHotkey integration for controlling external apps (memoQ, Trados, Word) by voice. Custom voice commands with fuzzy matching. Configure in Tools → Supervoice tab.
- 🎤 **Always-On Listening (v1.9.49)** - VAD-based continuous listening eliminates pressing F9 twice. Automatically detects speech, records, transcribes, and processes as command or dictation. Configurable mic sensitivity (Low/Medium/High). Visual feedback: 🟢 Listening → 🔴 Recording → ⏳ Processing. F9 stops always-on mode if active.
- 🎤 **Talon-Style Voice Commands (v1.9.48)** - 3-tier voice command architecture: Internal commands (control Supervertaler), System commands (AutoHotkey for other apps), Dictation fallback. Built-in commands: navigation, editing, translation, lookup. Custom command editor with phrase, aliases, and action configuration.
-  🧹 **Code Cleanup (v1.9.47)** - Removed ~811 lines of dead Document View code. The Document View feature was never used in production - the Grid View (Editor) is the primary and only workflow. Cleanup includes: removed `LayoutMode` class, removed `create_editor_widget()`, `create_document_view_widget()`, `refresh_document_view()` and all related helper methods. File reduced from 35,249 to 34,438 lines. No functional changes.
- 🏠 **Workspace UI Redesign (v1.9.46)** - Cleaner tab hierarchy with renamed tabs: **Workspace** (main tab) containing **Editor** (the grid) and **Resources** (TM, Termbases, Prompts, etc.). Removed Document View (unused). Simplified navigation menu. Fixed critical bug where termbase matches showed terms from non-activated termbases.
- 🏷️ **Termbase Highlight Styles (v1.9.45)** - Three configurable styles for termbase matches in the translation grid: **Background** (default pastel green shades), **Dotted Underline** (priority-based colors: red for P1, grays for P2-3, customizable for P4+), and **Semibold** (bold weight with tinted foreground). Configure via Settings → View Settings. Auto-spellcheck for target language: spellcheck now automatically initializes to project target language on import/load. Fixed short language codes (nl, de, fr) not mapping to dictionaries.
- 📚 **UI Reorganization (v1.9.44)** - Prompt Manager moved under Project Resources tab (prompts are project resources). Superlookup hotkey script now shows Supervertaler icon in system tray. Fixed termbase import "Could not find termbase ID" error. Removed dotted focus outline from Superlookup Search button.
- 🔑 **Superlookup Hotkey Improvements (v1.9.43)** - Fixed Ctrl+Alt+L global hotkey not bringing Superlookup to foreground. Added AutoHotkey setup helper (Help → Setup AutoHotkey for Superlookup). New AutoHotkey path configuration in Settings → General Settings. Better error handling when AutoHotkey is not installed.
- 📁 **Multi-File Project Support (v1.9.42)** - Import entire folders of files as a single multi-file project! File → Import → Folder (Multiple Files) supports DOCX and TXT files. Per-file progress tracking in View → File Progress dialog (or click status bar). New file filter dropdown to show segments from specific files. Status bar shows completion progress across all files. Source files automatically backed up to `_source_files/` folder. Relocate Source Folder feature to fix broken paths. Export to folder with TXT, DOCX, or Bilingual Table formats (export in progress - basic functionality available).
- 🔍 **Superlookup Fixes (v1.9.42)** - Renamed `UniversalLookupTab` to `SuperlookupTab` for consistency. Fixed `theme_manager` attribute error when using Ctrl+Alt+L hotkey. Theme-aware search term highlighting now works properly.
- 📋 **Spellcheck Info Dialog Redesign (v1.9.42)** - Two-column horizontal layout fits on screen without scrolling. Clear explanation of auto-switching between built-in pyspellchecker and Hunspell backends. Compact diagnostics section.
- 🌙 **Dark Mode (v1.9.41)** - Complete dark theme implementation with proper styling across the entire application. Dark compare boxes in Translation Results panel, dark Termview with visible text for non-matched words, and consistent theming throughout all UI components. Switch themes via View → Theme Editor.
- 🔍 **Superlookup Unified Concordance System (v1.9.40)** - Major consolidation: Ctrl+K now opens Superlookup instead of a separate concordance dialog. All lookup resources in one place: TM concordance, Termbase matches, Supermemory semantic search, Machine Translation, and Web Resources. New dual-view toggle: Horizontal (table) or Vertical (list) layout. Tab reorganization: "Project Resources" now comes before "Prompt Manager". Removed redundant tabs from Translation Memories (Concordance and Import/Export - functionality already available in Superlookup and TM List). FTS5 full-text search now properly used for blazingly fast concordance on millions of segments.
- 🔍 **Superlookup Multilingual Search (v1.9.39)** - Complete overhaul of Superlookup with multilingual language filtering. New From/To language dropdowns filter TM and termbase searches by source/target language pair. Search direction radio buttons (Both/Source only/Target only) for precise concordance searches. Yellow highlighting of search terms in results. Compact results display with tooltips for full text. Languages auto-populate from your TMs and termbases, grouped alphabetically by language family. UI cleanup: removed Manual Capture button and Operating Modes selector.
- 📁 **Improved Project File Format (v1.9.38)** - `.svproj` files now have all metadata at the top (name, languages, dates, settings, paths) with segments at the end for easier inspection in text editors. Added helpful tip in batch translate warning about using Select All + Clear Target instead of re-importing.
- 🔤 **User-Configurable Grid Fonts (v1.9.37)** - Choose your preferred font family for the translation grid from 10 popular options. Live preview shows font changes in real-time with sample source/target text and tags. Font family now persists between sessions.
- 🎨 **Universal Tag Coloring (v1.9.36)** - All CAT tool tags now highlighted in pink: memoQ `{1}`, `[2}`, Trados `<1>`, `</1>`, Phrase `{1}`, and HTML `<b>`, `<i>`. CafeTran pipe symbols only red in CafeTran projects (bug fix).
- 🎨 **memoQ Red Tags Support (v1.9.35)** - Fixed memoQ bilingual export not preserving red tag color. Tags in the target column now correctly inherit the red/magenta color from the source column, ensuring perfect formatting for memoQ re-import.
- 🎨 **UI Fixes (v1.9.34)** - Replaced all standard radio buttons with green-themed CheckmarkRadioButton.
- 🐛 **Spellcheck Update Fix (v1.9.33)** - Fixed issue where adding/ignoring words only removed underline in the current cell. Now triggers instant global refresh of all highlighters across the entire grid. No more false positive red underlines after you've whitelisted a word

- 📦 **Trados SDLRPX Status Fix (v1.9.32)** - Fixed critical bug where exported SDLRPX return packages kept segments in "Draft" status instead of updating to "Translated". Trados Studio now correctly recognizes translated segments. Client deliverables no longer show as MT draft content

- 🔤 **Spellcheck Language Fix (v1.9.31)** - Spellcheck now correctly uses the project's target language instead of defaulting to English. Added language dropdown in Spellcheck Info dialog to manually change spellcheck language. Language changes take effect immediately with highlighting refresh
- 🐛 **Critical LLM Fix (v1.9.30)** - Fixed OpenAI/LLM translation failing with "No such file or directory" error. Removed hardcoded debug file path that prevented translation when running from non-development directories
- 📝 **Spellcheck Integration (v1.9.29)** - Built-in spellcheck for target language. Works out of the box with pyspellchecker (8 languages bundled). Optional Hunspell support for more languages. Red wavy underlines for misspelled words. Right-click for suggestions, Add to Dictionary, Ignore. Custom dictionary with persistent word list. Spellcheck state saved per-project in .svproj files. Button state persists across restarts
- 📄 **Phrase (Memsource) Bilingual DOCX Support (v1.9.28)** - Full round-trip support for Phrase TMS bilingual DOCX files. Import preserves inline tags like `{1}`, `{1>text<1}`. Export writes translations back to Column 5 for seamless return to Phrase workflow. File → Import → Phrase (Memsource) Bilingual (DOCX) and File → Export → Phrase (Memsource) Bilingual
- 👁️ **Show Invisibles Feature (v1.9.28)** - Display invisible characters in the translation grid: spaces (·), tabs (→), non-breaking spaces (°), and line breaks (¶). Dropdown menu with granular control for each character type. Toggle All option. Smart handling preserves copy/paste (Ctrl+C copies original characters), double-click word selection, and Ctrl+Arrow word navigation. Configurable symbol color in Settings → View Settings
- 📄 **Simple Text File Import/Export (v1.9.27)** - Import simple text files where each line becomes a source segment. Translate with AI, then export a matching file with translations. Perfect for line-by-line translation of plain text content. Language pair selection, encoding options (UTF-8, Latin-1, etc.), and empty line handling. File → Import → Simple Text File (TXT) and File → Export → Simple Text File - Translated (TXT)
- 📦 **SDLPPX Project Persistence (v1.9.20)** - SDLPPX package path now saved in .svproj files. Full round-trip workflow persists across sessions - import SDLPPX, translate, save project, close, reopen, continue translating, export SDLRPX. Fixed export bug that showed "0 translations updated". Handler automatically restored on project load
- 📦 **Trados Studio Package Support (v1.9.19)** - Import SDLPPX packages directly from Trados Studio project managers. New File → Import → Trados Studio submenu with Package (SDLPPX) option. Translates SDLXLIFF files within the package, preserves SDL-specific markup and segment IDs. Export as SDLRPX return package (File → Export → Trados Studio → Return Package) for seamless delivery back to Trados users. Full round-trip workflow for freelance translators receiving packages
- 🔍 **Supermemory Concordance Integration (v1.9.18)** - Concordance Search (Ctrl+K) now includes Supermemory semantic search with two-tab interface. TM Matches tab for exact text search, Supermemory tab for meaning-based search. Active checkbox column in Supermemory to control which TMs are searched. Fixed Trados bilingual DOCX round-trip issues (xml:space, language settings). Supermemory moved to Resources tab
- 🧠 **Supermemory Enhancements (v1.9.17)** - Complete domain management system for translation memories with domain categorization (Legal, Medical, Patents, etc.), multi-language filtering in search, integration with Superlookup for unified lookup, and TMX/CSV export. Color-coded domain tags, dynamic column headers showing actual languages, and professional search/filter interface
- 🖥️ **Local LLM Support - Ollama (v1.9.16)** - Run AI translation entirely on your computer with no API costs, complete privacy, and offline capability. New "Local LLM (Ollama)" provider option in Settings with automatic hardware detection and model recommendations. Supports qwen2.5 (3B/7B/14B), llama3.2, mistral, and gemma2 models. Built-in setup wizard guides installation and model downloads. See FAQ for setup instructions
- 📋 **Bilingual Table Export/Import (v1.9.15)** - New Supervertaler Bilingual Table format for review workflows. Export menu options: **"Bilingual Table - With Tags (DOCX)"** preserves Supervertaler formatting tags for re-import after review. **"Bilingual Table - Formatted (DOCX)"** applies formatting (bold/italic/underline, bullet markers) for client-ready output. Tables include segment number, source, target, status, and notes columns. **"Import Bilingual Table"** compares edited DOCX with current project, shows diff preview, and applies changes. Document title links to supervertaler.com
- 📤 **Improved DOCX Export & Keyboard Navigation (v1.9.14)** - Fixed DOCX export to properly handle formatting tags (`<b>`, `<i>`, `<u>`) and convert them to actual Word formatting. Export now handles multi-segment paragraphs with partial replacement. Added cleanup for Unicode replacement characters (U+FFFC). Ctrl+Home/End now properly navigate to first/last segment even when editing in grid cells
- 📄 **Document Preview & List Tags (v1.9.13)** - New Preview tab shows formatted document view with headings, paragraphs, and list formatting. Click any text to navigate to that segment. Distinct list tags: `<li-o>` for ordered/numbered lists (1. 2. 3.) and `<li-b>` for bullet points (•). DOCX import now properly detects bullet vs numbered lists from Word's numbering XML. Type column shows `¶` for continuation paragraphs instead of `#`
- 📊 **Progress Indicator Status Bar (v1.9.12)** - New permanent status bar showing real-time translation progress: Words translated (X/Y with percentage), Confirmed segments (X/Y with percentage), and Remaining segments count. Color-coded: red (<50%), orange (50-80%), green (>80%). Updates automatically as you work
- ⚡ **Navigation & Find/Replace Improvements (v1.9.11)** - Ctrl+Home/End to jump to first/last segment. Find/Replace dialog now pre-fills selected text from source or target grid. Ctrl+Q shortcut for instant term pair saving (remembers last-used termbase from Ctrl+E dialog)
- 🔧 **Non-Translatables: Case-Sensitive & Full-Word Matching (v1.9.11)** - Non-translatables matching is now case-sensitive by default and only matches full words (not partial words). Added LLM refusal detection with helpful error messages for batch translation. Fixed crash when closing project (missing stop_termbase_batch_worker). Fixed .svprompt files not showing in Prompt Library tree
- 🔧 **TM Search Fixes & Language Matching (v1.9.10)** - Fixed TM matches not appearing in Translation Results panel. Added flexible language matching ("Dutch", "nl", "nl-NL" all match). TM metadata manager now initializes with project load. Removed legacy Project TM/Big Mama hardcoding. Cleaned public database for new users. Non-Translatables: sortable columns, right-click delete, Delete key support
- 🎨 **memoQ-style Alternating Row Colors (v1.9.9)** - Grid now displays alternating row colors across all columns (ID, Type, Source, Target) like memoQ. User-configurable colors in Settings → View Settings with even/odd row color pickers. Colors are consistent across the entire row including QTextEdit widgets
- 🔄 **CafeTran Integration & Editor Shortcuts (v1.9.8)** - Full CafeTran bilingual DOCX support with pipe symbol formatting. New Ctrl+Shift+S copies source to target. Ctrl+, inserts pipe symbols for CafeTran. Pipes highlighted in red/bold. Sortable keyboard shortcuts table. Batch size default changed to 20
- 🔄 **CafeTran Bilingual DOCX Support (v1.9.7)** - Full import/export support for CafeTran bilingual DOCX files. Import preserves pipe symbol formatting markers. Export writes translations back with formatting preserved. Round-trip workflow for CafeTran users
- 📁 **Custom File Extensions & Monolingual Export (v1.9.6)** - New branded file extensions: `.svproj` (projects), `.svprompt` (prompts), `.svntl` (non-translatables). All formats maintain backward compatibility. Monolingual DOCX import now prompts for language pair. New "Target Only (DOCX)" export preserves original document structure (tables, formatting). Original DOCX path saved in project files for reliable exports
- 📤 **Send Segments to TM & memoQ Tag Shortcuts (v1.9.5)** - Bulk send translated segments to TMs via Edit > Bulk Operations. Filter by status (Translated, Reviewed, etc.) and scope. New Ctrl+, shortcut inserts memoQ tags pairs or wraps selection. Tab renamed to "Resources"
- 🏷️ **Tag-Based Formatting System (v1.9.4)** - Complete inline formatting support for memoQ bilingual files. Import preserves bold/italic/underline as `<b>`, `<i>`, `<u>` tags. Toggle between WYSIWYG and Tag view with Ctrl+Alt+T. Ctrl+B/I/U shortcuts to apply formatting. AI translation preserves tags. Export converts tags back to Word formatting
- 📋 **Session Log Tab & TM Defaults Fix (v1.9.3)** - Added Session Log tab to bottom panel for easy access to log messages. Fixed TM Read/Write checkbox defaults to respect project.json settings
- ⚙️ **Superlookup Settings UI (v1.9.2)** - Redesigned Settings tab with sub-tabs for TM/Termbase/MT/Web resources. Proper 18x18px checkboxes with green background and white checkmarks matching standard Supervertaler style. Each resource type has dedicated full-height space for easy selection
- ↩️ **Undo/Redo for Grid Edits (v1.9.1)** - Full undo/redo support for grid editing operations with Ctrl+Z/Ctrl+Y. Tracks target text changes, status changes, and find/replace operations with 100-level history
- 🔍 **Termview - Inline Terminology (v1.9.0)** - Visual inline terminology display showing source words with translations underneath, inspired by RYS Trados plugin. Supports multi-word terms, click-to-insert, hover tooltips, and terms with punctuation like "gew.%"
- 🎨 **UI Refinements - Tab Styling (v1.8.0)** - Refined selected tab appearance with subtle 1px blue underline and light background highlighting for cleaner visual design
- ✅ **Simplified TM/Termbase System (v1.6.6)** - Redesigned with Read/Write checkboxes, auto-priority system, removed complex Active/Project concepts for clearer workflow
- 🔍 **Find/Replace & TM Enhancements (v1.7.9)** - Fixed highlighting, disabled TM saves during navigation, added bidirectional TM search with language variant matching
- 🔍 **Filter Highlighting Fix (v1.7.8)** - Fixed search term highlighting in source/target filter boxes using widget-internal highlighting
- 🎯 **Termbase Display Customization (v1.7.7)** - User-configurable termbase match sorting and filtering for cleaner translation results
- 💾 **Auto Backup System (v1.7.6)** - Automatic project.json and TMX backups at configurable intervals to prevent data loss
- 🐛 **Critical TM Save Bug Fix (v1.7.5)** - Fixed massive unnecessary database writes during grid operations that caused 10+ second freezes
- 💾 **Project Persistence (v1.7.4)** - Projects now remember your primary prompt and image context folder
- 🧪 **Prompt Preview & System Template Editor (v1.7.3)** - Preview combined prompts with figure context detection and improved system template editor with better layout
- 🔧 **Termbase Critical Fixes (v1.7.2)** - Fixed term deduplication and termbase selection issues
- 🎨 **Termbase UI Polish (v1.7.1)** - Improved visual consistency with pink highlighting for project termbases and real-time term count updates
- 📚 **Project Termbases (v1.7.0)** - Dedicated project-specific terminology with automatic extraction and pink highlighting
- 📁 **File Dialog Memory (v1.6.5)** - File dialogs remember your last used directory for improved workflow
- 🌐 **Superbrowser (v1.6.4)** - Multi-chat AI browser with ChatGPT, Claude, and Gemini side-by-side in one window
- ⚡ **UI Responsiveness & Precision Scroll (v1.6.3)** - Debug settings, disabled LLM auto-matching, memoQ-style precision scroll buttons, auto-center active segment
- 🖼️ **Superimage (v1.6.2)** - Extract images from DOCX files with preview and auto-folder management
- 📚 **Enhanced Termbase System (v1.6.1)** - Extended metadata with notes, project, client fields and refresh functionality
- 📚 **Complete Termbase System (v1.6.0)** - Professional terminology management with interactive features
- 🎤 **Supervoice (v1.4.0)** - AI voice dictation with OpenAI Whisper, 100+ languages, F9 hotkey
- 📊 **Superbench (v1.4.1)** - Benchmark LLM translation quality on YOUR actual projects with chrF++ scoring
- 🤖 **AI Assistant (v1.3.4)** - ChatGPT-quality conversational prompt refinement built into the editor
- 📚 **Unified Prompt Library (v1.3.0)** - Unlimited folders, favorites, multi-attach, quick run
- 📝 **TMX Editor (v1.1.3)** - Database-backed editor handles massive 1GB+ TMX files
- ✋ **AutoFingers (v1.2.4)** - Automated TMX-to-memoQ pasting with fuzzy matching and tag cleaning
- 📄 **PDF Rescue** - AI OCR with GPT-4 Vision transforms locked PDFs into clean DOCX
- 🖼️ **Image Context** - Multimodal AI automatically includes images when translating technical documents
- 💾 **Translation Memory** - Fuzzy matching with TMX import/export, auto-propagation
- 🔄 **CAT Tool Integration** - memoQ, Trados, CafeTran bilingual table support

**See full version history below** ↓

---

## [1.9.41] - December 16, 2025

### 🌙 Dark Mode - Complete Theme Implementation

**Full dark theme support across the entire application:**
- 🎨 **Compare Boxes**: Translation Results panel now properly displays dark backgrounds for Current Source, TM Source, and TM Target boxes in dark mode
- 📝 **Termview Visibility**: All words in Termview pane now visible in dark mode - not just terms with matches. Non-matched words use light text color on dark background
- 🔄 **Theme Consistency**: Fixed Qt styling issues where hidden widgets weren't receiving theme updates. Theme colors now applied when widgets become visible
- ⚡ **Reliable Styling**: Uses both stylesheet and QPalette approaches for maximum compatibility across different Qt rendering scenarios

**Technical improvements:**
- Added `_apply_compare_box_theme()` method for reliable theme application on visibility
- Theme-aware `TermBlock` and `NTBlock` classes in Termview widget
- Proper color inheritance for all UI components in dark mode

**Access Dark Mode:** View → Theme Editor → Select "Dark" theme

---

## [1.9.40] - December 12, 2025

### 🔍 Superlookup Unified Concordance System

**Major consolidation - Ctrl+K now opens Superlookup instead of separate dialog:**
- 🔗 **Unified Lookup Hub**: All concordance searches now go through Superlookup - one place for TM, Termbase, Supermemory, MT, and Web Resources
- ⌨️ **Ctrl+K Integration**: Pressing Ctrl+K in Project Editor navigates to Tools → Superlookup and auto-searches selected text
- 📝 **Selected Text Auto-Fill**: Any text selected in source/target automatically populates the search field

**Dual-view toggle for TM Matches tab:**
- 📊 **Horizontal (Table)**: Source | Target columns side-by-side - compact and scannable
- 📜 **Vertical (List)**: Dutch: ... / English: ... stacked format - traditional concordance layout with more detail
- 🔄 **Radio Button Toggle**: Switch between views instantly, results update in both views

**UI/Tab reorganization:**
- 📚 **"Resources" → "Project Resources"**: Clearer naming for the resources tab
- 🔀 **Tab Reorder**: Project Resources now comes BEFORE Prompt Manager (more logical flow)
- 🧹 **Removed Redundant Tabs**: Translation Memories no longer has Concordance or Import/Export tabs (functionality in Superlookup and TM List)
- 📦 **Compact Source Text**: Superlookup source text box shrunk from 100px to 50px
- 📚 **"Termbase Terms" → "Termbase Matches"**: Consistent naming

**FTS5 Full-Text Search optimization:**
- ⚡ **Concordance now uses FTS5**: `concordance_search()` now uses SQLite FTS5 MATCH instead of slow LIKE queries
- 🚀 **100-1000x faster** on large databases with millions of segments
- 🔄 **Auto-sync**: FTS5 index automatically rebuilt if out of sync with main table
- 🔧 **Manual rebuild**: New `rebuild_fts_index()` method available for maintenance

**ChromaDB stability fix:**
- 🐛 **Fixed Rust backend crashes**: Removed all `collection.count()` calls that caused native crashes in ChromaDB 1.3.x
- 📊 **Uses metadata count**: Stats now derived from SQLite metadata instead of ChromaDB collection queries
- ✅ **ChromaDB 0.6.3**: Stable version with Python backend, compatible with tokenizers 0.22.0

---

## [1.9.39] - December 11, 2025

### 🔍 Superlookup Multilingual Search

**Multilingual language filtering for TM and termbase searches:**
- 🌍 **From/To Language Dropdowns**: New filter dropdowns in Superlookup search bar to filter by source/target language pair
- 🔄 **Swap Button**: Quick ↔ button to swap From and To language selections
- 📚 **Auto-Population**: Languages auto-populate from your TMs and termbases when tab is first viewed
- 🔤 **Smart Sorting**: Languages alphabetically sorted with family grouping (all Dutch variants together, all English variants together, etc.)
- 🏷️ **Clear Display**: Format shows "English (en)", "Dutch (nl-BE)" for clarity and uniqueness

**Search direction controls:**
- ↔️ **Both**: Bidirectional search (searches source and target columns)
- → **Source only**: Search only in source text
- ← **Target only**: Search only in target text

**UI improvements:**
- 🟡 **Yellow Highlighting**: Search terms now highlighted in yellow in TM and termbase results
- 📏 **Compact Display**: Results use word wrap with 60px max row height, tooltips show full text on hover
- 🔢 **Hidden Row Numbers**: Cleaner display without row number column
- 🧹 **Removed Manual Capture**: Button was redundant (just paste text manually)
- 🧹 **Removed Operating Modes**: Dropdown was pointless (only Universal mode was used)

---

## [1.9.38] - December 11, 2025

### 📁 Project File & UX Improvements

**Reorganized .svproj file structure for human readability:**
- 📄 **Metadata First**: Project name, languages, dates, ID now at the top of the file
- ⚙️ **Settings Next**: Prompt, TM, termbase, spellcheck settings follow metadata
- 📂 **Paths Then**: Source file paths (DOCX, memoQ, Trados, etc.) before segments
- 📝 **Segments Last**: Translation content at the end for easy scrolling in text editors

**Improved batch translate warning for memoQ files:**
- 💡 Added tip: "You can clear all targets without re-importing" with instructions to use Select All + Clear Target from right-click menu
- Saves users from having to go back to memoQ to clean the file

---

## [1.9.37] - December 11, 2025

### 🔤 User-Configurable Grid Fonts

**New font customization options in Settings → View Settings:**
- 🔤 **Font Family Dropdown**: Choose from 10 popular fonts: Calibri, Segoe UI, Arial, Consolas, Verdana, Times New Roman, Georgia, Courier New, Tahoma, Trebuchet MS
- 👁️ **Live Preview**: Real-time preview showing sample source/target text with tags, updates instantly as you change font settings
- 💾 **Font Persistence**: Font family now saved to preferences and restored on startup (previously only font size was saved)
- 🎯 **Improved Spinbox**: Fixed font size spinner up/down arrows with better click targets
- 📝 **Contact Note**: Info text now includes "If your favourite font is missing, contact the developer!"

---

## [1.9.36] - December 10, 2025

### 🎨 Universal Tag Coloring

**All CAT tool tags now highlighted in pink in the translation grid:**
- 🏷️ **memoQ Tags**: `{1}`, `[2}`, `{3]`, `[4]` - all variations now colored pink
- 🏷️ **Trados Tags**: `<1>`, `</1>` - numeric tags now colored pink
- 🏷️ **Phrase Tags**: `{1}`, `{2}` - same as memoQ, now colored pink
- 🏷️ **HTML Tags**: `<b>`, `<i>`, `<u>`, `<li-o>` - already worked, still works

**CafeTran Pipe Symbol Fix:**
- 🐛 **Bug Fix**: Pipe symbols (`|`) were incorrectly highlighted red in ALL project types
- ✅ **Fixed**: Pipes now only red in CafeTran projects (as intended)
- 🔧 **Implementation**: Added `TagHighlighter._is_cafetran_project` class flag

---

## [1.9.35] - December 10, 2025

### 🎨 formatting
- **memoQ Red Tags**: Fixed issue where red formatting tags (e.g. `{1}`) in memoQ bilingual files were being exported as black text.
- **Smart Color Transfer**: Export now dynamically reads the source column color and applies it to the corresponding text in the target column.

## [1.9.34] - December 10, 2025

### 🎨 UI Fixes

**Checkmark Radio Buttons:**
- 🎨 **Global Update**: Replaced all standard `QRadioButton` instances across the application with the custom green `CheckmarkRadioButton`.
- ✅ **Updated Areas**: Find & Replace, Advanced Filters, Row Locking, Termbase Import, AutoFingers, and TM Import dialogs.
- 💅 **Visual Consistency**: Ensures a uniform look and feel across all green-themed UI elements.

---

## [1.9.32] - December 10, 2025

### 📦 Trados SDLRPX Status Fix

**Critical Bug Fix for Trados Return Packages:**
- 🔧 **Status Update Fix**: SDLRPX export now correctly updates segment confirmation status from "Draft" to "Translated"
- ✅ **Proper Trados Recognition**: Trados Studio now recognizes segments as translated, not machine translation drafts
- 📤 **Client Deliverables**: Return packages display correctly in Trados when client opens them
- 🏷️ **conf Attribute**: Fixed missing update of `conf` attribute in SDLXLIFF `<sdl:seg>` elements

**Technical Details:**
- Added `_update_segment_status()` method to `sdlppx_handler.py`
- Updates `conf` attribute in `sdl:seg-defs` section during export
- Maps internal status ('translated', 'approved') to SDL status ('Translated', 'ApprovedTranslation')
- Proper namespace handling for SDL elements in ElementTree

---

---

## [1.9.33] - December 10, 2025

### 🐛 Spellcheck Update Fix

**Fixed Spellcheck Highlighting Update:**
- 🔧 **Global Refresh**: Adding a word to custom dictionary or ignoring it now immediately updates all occurrences in the grid
- ✅ **No More False Positives**: Red wavy underlines vanish instantly across the entire document when you whitelist a word
- 🖱️ **Context Menu Fix**: Right-click "Add to Dictionary" and "Ignore Word" actions now trigger full grid refresh

---

## [1.9.31] - December 10, 2025

### 🔤 Spellcheck Language Fix

**Spellcheck Now Uses Project Target Language:**
- 🎯 **Automatic Language Detection**: Spellcheck initializes with project's target language instead of defaulting to English
- 🌐 **Language Dropdown**: Added language selector in Spellcheck Info dialog
- 🔄 **Immediate Effect**: Language changes take effect immediately with highlighting refresh
- 📝 **Fixed Initialization**: `_toggle_spellcheck()` now uses `self.current_project.target_lang`

---

## [1.9.30] - December 10, 2025

### 🐛 Critical LLM Fix

**Fixed OpenAI/LLM Translation Error:**
- 🔧 **File Path Error**: Fixed "No such file or directory: 'openai_debug.txt'" error that broke all LLM translations
- 📁 **Debug Path**: Removed hardcoded debug file path that only worked in development directory
- ✅ **Production Ready**: Translations now work when running from any directory

---

## [1.9.29] - December 10, 2025

### 📝 Spellcheck Integration

**Built-in Spellchecking for Target Language:**
- 📝 **Spellcheck Button**: Toggle in filter bar enables/disables spellchecking
- 〰️ **Red Wavy Underlines**: Misspelled words highlighted with red wavy underline
- 💬 **Right-Click Suggestions**: Click misspelled word for spelling suggestions
- ➕ **Add to Dictionary**: Add words to custom dictionary (persistent)
- 🔇 **Ignore Word**: Ignore word for current session only
- 📖 **Custom Dictionary**: Manage custom words from dropdown menu
- ℹ️ **Spellcheck Info**: View backend, language, and dictionary status

**Language Support:**
- 🇬🇧 English, 🇳🇱 Dutch, 🇩🇪 German, 🇫🇷 French, 🇪🇸 Spanish, 🇵🇹 Portuguese, 🇮🇹 Italian, 🇷🇺 Russian
- 🐍 **Built-in Backend**: Uses pyspellchecker with bundled dictionaries - works out of the box!
- 📚 **Hunspell Backend**: Optional .dic/.aff files for additional languages or improved accuracy
- Auto-matches project target language

**Settings & Persistence:**
- 💾 **Project-Level Settings**: Spellcheck state saved in .svproj files
- 🔄 **Session Persistence**: Button state remembered across restarts
- ℹ️ **Info Dialog**: Explains dual-backend system with dictionary download links

**Technical Details:**
- New module: `modules/spellcheck_manager.py` - Complete spellcheck handling
- Custom dictionary stored in `user_data/dictionaries/custom_words.txt`
- TagHighlighter extended for spell underline formatting
- Spellcheck only applied to target column (not source)
- Settings persisted in `ui_preferences.json` and `.svproj` files

---

## [1.9.28] - December 9, 2025

### 📄 Phrase (Memsource) Bilingual DOCX Support

**Full Round-Trip Workflow:**
- 📥 **Import Phrase Bilingual DOCX**: File → Import → Phrase (Memsource) Bilingual (DOCX)
- 📤 **Export Back to Phrase**: File → Export → Phrase (Memsource) Bilingual - Translated (DOCX)
- 🏷️ **Inline Tag Preservation**: Tags like `{1}`, `{1>text<1}` preserved for round-trip
- 🔍 **Auto-Detection**: Detects Phrase format (7-column tables, segment IDs with `:`)
- 💾 **Project Persistence**: Phrase source path saved in .svproj for future sessions

**Implementation:**
- New module: `modules/phrase_docx_handler.py` - Complete Phrase DOCX handling
- Language pair selection dialog for imported files
- Segment ID and status preserved in notes field
- Export updates only Column 5 (target text) as Phrase expects

### 👁️ Show Invisibles Feature

**Display Invisible Characters:**
- 🔘 **Dropdown Menu**: Show Invisibles button with granular control
- ·  **Spaces**: Displayed as middle dot (·)
- →  **Tabs**: Displayed as right arrow (→)
- °  **Non-Breaking Spaces**: Displayed as degree symbol (°)
- ¶  **Line Breaks**: Displayed as pilcrow (¶)
- 🎯 **Toggle All**: Quick on/off for all invisible types

**Smart Handling:**
- 📋 **Clipboard Safety**: Ctrl+C copies original characters, not symbols
- 🖱️ **Double-Click Selection**: Properly selects words when invisibles shown
- ⌨️ **Ctrl+Arrow Navigation**: Word-by-word navigation works correctly
- 🎨 **Configurable Color**: Symbol color in Settings → View Settings (default: light gray)
- ✅ **Zero-Width Space Technique**: Uses U+200B for line-break opportunities without breaking word boundaries

**Technical Details:**
- Replacements applied only at display time (segment data never modified)
- Automatic reversal when text is saved or edited
- TagHighlighter extended to color invisible symbols

### 🔧 TM Pre-Translation Fix

**Batch Translate with TM:**
- 🐛 **Fixed TM-Only Mode**: Batch Translate dialog now properly handles TM as a translation provider
- 📖 **TM Provider Support**: Select "Translation Memory" in provider dropdown for TM-only batch translation
- 🎯 **Respects Activated TMs**: Uses project's activated TMs for matching
- 📊 **Match Threshold**: Accepts matches 70% and above for pre-translation

---

## [1.9.26] - December 8, 2025

### 🔄 Automatic Model Version Checker

**Smart Model Updates:**
- 🆕 **Auto-detect New LLM Models**: Automatically checks for new models from OpenAI, Anthropic, and Google
- 📅 **Daily Checks**: Runs once per 24 hours on startup (configurable)
- 🔔 **Smart Notifications**: Popup dialog only when new models are detected
- ✅ **Easy Selection**: Click to select which models to add to Supervertaler
- 💾 **Intelligent Caching**: Remembers last check to avoid unnecessary API calls
- ⚙️ **Fully Configurable**: Enable/disable auto-check in Settings → AI Settings
- 🔍 **Manual Check**: "Check for New Models Now" button for on-demand checking

**Implementation:**
- New module: `modules/model_version_checker.py` - Core checking logic with 24-hour throttling
- New module: `modules/model_update_dialog.py` - User-friendly PyQt6 dialogs
- Settings integration: New "Model Version Checker" section in AI Settings
- Cache system: Stores results in `user_data/model_version_cache.json`
- Provider support: OpenAI (models.list API), Claude (pattern testing), Gemini (models API)

**User Experience:**
- Silent operation: No interruption if no new models found
- Error handling: Graceful degradation if APIs unavailable
- Documentation: Complete UI standards guide to maintain consistency

### 🎨 UI Polish & Standardization

**Checkbox Consistency:**
- ✅ **Standardized All Checkboxes**: Replaced 3 blue QCheckBox instances with green CheckmarkCheckBox
- 📏 **Refined Size**: Reduced checkbox size from 18x18px to 16x16px for cleaner appearance
- 📚 **Documentation**: Created UI_STANDARDS.md to prevent future inconsistencies
- 🎯 **Visual Consistency**: All checkboxes now use custom green style with white checkmarks

**Fixed Checkboxes:**
- "Enable LLM (AI) matching on segment selection"
- "Auto-generate markdown for imported documents"
- "Enable automatic model checking (once per day on startup)"

---

## [1.9.25] - December 8, 2025

### 🐧 Linux Compatibility Release

**Platform Support:**
- ✅ **Full Linux Compatibility**: Supervertaler now runs perfectly on Ubuntu and other Linux distributions
- ✅ **Removed Legacy Dependencies**: Eliminated tkinter imports from TMX editor module
- ✅ **Complete requirements.txt**: All dependencies now properly documented and installable
- ✅ **Graceful Platform Detection**: AutoFingers shows helpful message on Linux (Windows/memoQ-specific feature)

**Installation Improvements:**
- 📦 **One-Command Setup**: `pip install -r requirements.txt` installs all dependencies
- 📝 **Added Missing Dependencies**:
  - `pyyaml` - YAML support for Non-Translatables manager
  - `PyMuPDF` - PDF processing for PDF Rescue module
  - `sentence-transformers` - Semantic search for Supermemory
  - `keyboard` - Keyboard control for AutoFingers
  - `lxml` - XML processing for Trados DOCX handler
- 🛠️ **Platform-Specific Notes**: Clear documentation for Linux, Windows, and macOS compatibility
- 🔧 **Optional Dependencies**: Voice dictation and automation features clearly marked as optional

**Bug Fixes:**
- 🐛 **Fixed AutoFingers Import**: Made `pyautogui` import optional with graceful fallback for Linux
- 🐛 **Fixed TMX Editor**: Removed unnecessary tkinter dependency from core module
- 🐛 **Fixed Import Errors**: Proper error handling for platform-specific features

**Technical Changes:**
- 🔄 **AutoFingers Engine**: Added `HAS_PYAUTOGUI` flag for cross-platform compatibility
- 🔄 **Import Guards**: Platform-specific features now detect availability at runtime
- 📚 **Documentation**: Enhanced requirements.txt with feature descriptions and platform notes

**For Users:**
- 🎯 **Fresh Installation**: Works out-of-the-box on fresh Ubuntu installations
- 🎯 **Virtual Environment**: Full support for Python venv isolated installations
- 🎯 **Cross-Platform**: Same codebase works on Windows, Linux, and macOS

---

## [1.9.24] - December 7, 2025

### ✨ Smart Word Selection
- **Intelligent Text Selection**: Selecting part of a word automatically expands to the full word
  - Makes word selection faster and less stressful during translation
  - Works in both source (read-only) and target (editable) columns
  - Supports compound words with hyphens (e.g., "self-contained")
  - Supports contractions with apostrophes (e.g., "don't", "l'homme")
  - Threshold-based: Only expands selections under 50 characters (prevents interference with multi-word selections)
- **Settings Toggle**: New "Enable smart word selection" checkbox in Settings → General → Editor Settings
  - Enabled by default
  - Helpful tooltip explains the feature with examples
  - Can be disabled if user prefers traditional selection behavior
- **Implementation**:
  - Added `mouseReleaseEvent()` to both `ReadOnlyGridTextEditor` and `EditableGridTextEditor`
  - Word character detection includes alphanumeric, underscore, hyphen, and apostrophe
  - Boundary detection ensures expansion only occurs when selection is partial
  - Respects settings toggle across the application
- **Documentation**: Complete feature documentation in `SMART_WORD_SELECTION.md`
  - Implementation details, testing checklist, known limitations, future enhancements

### 🛡️ Supermemory Error Handling Improvements
- **Better DLL Error Messages**: Enhanced PyTorch DLL loading failure handling
  - `modules/supermemory.py` now catches `OSError` and `Exception` (not just `ImportError`)
  - Windows-specific DLL errors are properly caught and handled
  - Stores error message in `SENTENCE_TRANSFORMERS_ERROR` for debugging
- **Helpful Instructions**: Auto-detects DLL errors and provides actionable solutions
  - Detects "DLL", "c10.dll", or "torch" in error messages
  - Provides 3 specific fixes with direct links and exact commands:
    1. Install Visual C++ Redistributables (https://aka.ms/vs/17/release/vc_redist.x64.exe)
    2. Reinstall PyTorch with exact pip commands
    3. Disable Supermemory auto-init in Settings as fallback
  - Instructions appear automatically in the log when error occurs
- **Technical Details**:
  - Modified `Supervertaler.py`: Lines 4116-4126 (error handler in `_auto_init_supermemory()`)
  - Modified `modules/supermemory.py`: Lines 45-51 (exception catching)

---

## [1.9.23] - December 7, 2025

### 📄 Bilingual Table Landscape Orientation
- **Improved Visualization**: Supervertaler Bilingual Table exports now use landscape orientation
  - Better visualization of long segments (source and target columns have more horizontal space)
  - Applies to both "With Tags" and "Formatted" export options
  - Page dimensions automatically swapped for landscape layout
  - Maintains 0.5-inch margins on all sides
- **Technical Details**:
  - Added `WD_ORIENT.LANDSCAPE` to document sections
  - Swapped page width/height for proper landscape rendering
  - Modified `Supervertaler.py`: Lines 7820-7832 (document setup)

---

## [1.9.22] - December 7, 2025

### 🤖 Gemini 3 Pro Preview Support
- **Latest Google AI Model**: Added support for Gemini 3 Pro Preview (November 2025 release)
  - New model option in Settings → LLM Settings → Gemini Models dropdown
  - Listed as "gemini-3-pro-preview (Latest - Superior Performance)"
  - Works in both single segment translation (Ctrl+T) and batch translation
  - Performance: 10-20% improvement on average, 6-20x better on reasoning/math tasks
  - Pricing: $2/$12 per million tokens (vs $1.25/$10 for Gemini 2.5 Pro)
- **LLM Client Update**: Added all current Gemini models to supported list
  - `gemini-2.5-flash-lite` (Fastest & Most Economical)
  - `gemini-2.5-pro` (Premium - Complex Reasoning)
  - `gemini-3-pro-preview` (Latest - Superior Performance)
  - Updated module documentation to reflect Gemini 3 support
- **Files Modified**:
  - `Supervertaler.py`: Lines 10889-10902 (model dropdown and tooltip)
  - `modules/llm_clients.py`: Lines 8-11 (docs), 220-229 (supported models)

---

## [1.9.21] - December 6, 2025

### 🐛 Critical SDLPPX Handler Bug Fix
- **Fixed SDLRPX Export Failure After Project Reload**: Fixed "'str' object is not callable" error when exporting SDLRPX return packages after reopening a saved project
  - Root cause: Handler was initialized with path string instead of log_callback parameter
  - The path was incorrectly assigned to `self.log`, causing export to fail when trying to call log function
  - Now correctly initializes handler with `TradosPackageHandler(log_callback=self.log)` and calls `load_package(path)` separately
  - Also fixed missing `self.sdlppx_source_file` assignment during handler restoration
  - Full SDLPPX workflow now works correctly: import package → translate → save project → close → reopen → export SDLRPX ✓
- **Impact**: This bug prevented translators from exporting return packages after reopening saved SDLPPX projects, breaking the workflow for Trados Studio package handling

---

## [1.9.20] - December 5, 2025

### 📦 SDLPPX Project Persistence
- **Project Save/Restore**: SDLPPX package path now saved in .svproj files
  - Added `sdlppx_source_path` field to Project dataclass
  - Serialized in `to_dict()`, deserialized in `from_dict()`
  - Full round-trip workflow now persists across sessions
- **Handler Restoration**: SDLPPX handler automatically restored on project load
  - When opening a .svproj from an SDLPPX import, handler is recreated
  - SDLRPX export available immediately without reimporting
  - Log message confirms: "✓ Restored Trados package handler"
- **Export Bug Fix**: Fixed SDLRPX export showing "0 translations updated"
  - Export now reads from segment objects instead of table widget items
  - Notes column was never populated as QTableWidgetItem - data is in segment.notes
  - Verified translations correctly written to return package

---

## [1.9.19] - December 4, 2025

### 📦 Trados Studio Package Support
- **SDLPPX Import**: Import Trados Studio project packages directly
  - File → Import → Trados Studio → Package (SDLPPX)
  - Parses SDLXLIFF files within the package
  - Shows package info dialog with file list and segment counts
  - Preserves SDL-specific markup and segment IDs
  - Automatic language detection from package metadata
- **SDLRPX Export**: Create return packages for delivery
  - File → Export → Trados Studio → Return Package (SDLRPX)
  - Writes translations back to SDLXLIFF files
  - Creates properly formatted return package
  - Round-trip workflow for freelance translators
- **Menu Reorganization**: Grouped all Trados import/export options
  - New "Trados Studio" submenu under Import and Export
  - Contains both bilingual review DOCX and package options
- **New Module**: `modules/sdlppx_handler.py` (767 lines)
  - `TradosPackageHandler` class for package management
  - `SDLXLIFFParser` for parsing SDL-extended XLIFF files
  - Handles `<g>`, `<x/>`, `<mrk mtype="seg">` tags
  - Preserves SDL namespaces and attributes

---

## [1.9.18] - December 4, 2025

### 🔍 Supermemory Concordance Integration
- Concordance Search (Ctrl+K) now includes Supermemory semantic search
- Two-tab interface: TM Matches tab for exact text, Supermemory tab for meaning
- Active checkbox column in Supermemory to control which TMs are searched
- Fixed Trados bilingual DOCX round-trip issues (xml:space, language settings)
- Supermemory moved from Tools tab to Resources tab

---

## [1.9.17] - December 3, 2025

### 🧠 Supermemory Enhancements - Domain Management & Superlookup Integration

**Major upgrade to the vector-indexed translation memory system:**

**Domain Management System:**
- Added **Domain dataclass** with name, description, color, and active status
- New database schema: `domains` table and `domain` column in `indexed_tms`
- **8 default domains:** General, Patents, Medical, Legal, Technical, Marketing, Financial, Software
- **DomainManagerDialog:** Full CRUD interface with color pickers and active toggles
- Assign domains during TMX import with intuitive dropdown selector
- Color-coded domain tags in search results for visual categorization

**Enhanced Search & Filtering:**
- **Language pair filter:** Dropdown to filter by source-target language combination
- **Multi-domain filter:** Select multiple active domains to search within
- **Dynamic column headers:** Results table shows actual language codes (e.g., "Source (EN)", "Target (NL)")
- Search respects both language pair and domain filters simultaneously

**Superlookup Integration:**
- **New "Supermemory" tab** in Superlookup for unified terminology/TM lookup
- Semantic search results appear alongside TM, termbase, and MT matches
- Click to insert matches directly into target segment
- Seamless integration with existing Superlookup workflow

**Export Functionality:**
- **Export to TMX:** Full TMX export with language headers and segment metadata
- **Export to CSV:** Simple source-target pairs for spreadsheet workflows
- Export dialog lets you choose format before exporting

### Consolidated AI Settings

- Merged Gemini and Mistral settings into unified **"AI Settings"** tab
- Cleaner Settings panel with fewer tabs
- All API keys and model selections in one place

---

## [1.9.18] - December 4, 2025

### 🔍 Supermemory Concordance Integration & Trados Fixes

**Concordance Search now includes Supermemory semantic search:**

**Concordance Search Enhancements:**
- **Two-tab interface:** "TM Matches" (exact text) and "Supermemory" (semantic/meaning-based)
- Semantic search finds translations by meaning, not just exact words
- Tab headers show result counts (e.g., "📋 TM Matches (9)" and "🧠 Supermemory (25)")
- Results display similarity scores with color-coded High/Medium/Low indicators
- Window remembers position and size across sessions (saved to project)

**Supermemory UI Improvements:**
- **Moved to Resources tab** - now under Resources → Supermemory (was Tools)
- **Active checkbox column** in TM table - toggle which TMs are searched
- Only active TMs are included in Concordance semantic search
- Checkbox state persists in database

**Trados Bilingual DOCX Fixes:**
- Fixed `xml:space="preserve"` attribute on text elements for proper whitespace handling
- Fixed target language settings - runs now inherit from paragraph (was incorrectly setting nl-NL)
- Added language selection dialog on import (Trados files don't specify languages)
- Source file path now persisted in project for reliable re-export
- "Source File Not Found" now offers to browse for file in new location

**Other Improvements:**
- Renamed export menu items to "Supervertaler Bilingual Table" for clarity
- memoQ and CafeTran source paths also persisted in project
- Fixed Concordance accessing Supermemory engine (was checking wrong attribute)

---

## [1.9.16] - December 1, 2025

### 🖥️ Local LLM Support - Ollama Integration

**Run AI translation entirely on your computer with no API costs, complete privacy, and offline capability:**

**New Provider Option:**
- Added **"Local LLM (Ollama)"** as new provider in Settings → LLM Provider tab
- Appears alongside OpenAI, Anthropic, Google, etc. with familiar radio button selection
- Works with single translation, batch translation, and AI Assistant chat

**Intelligent Hardware Detection:**
- Automatically detects system RAM and GPU capabilities
- Recommends optimal model based on your hardware:
  - **4GB RAM:** qwen2.5:3b (2.5GB download) - Basic functionality
  - **8GB RAM:** qwen2.5:7b (5.5GB download) - Recommended default
  - **16GB+ RAM:** qwen2.5:14b (10GB download) - Premium quality
- GPU detection for NVIDIA, AMD, and Apple Silicon

**Built-in Setup Wizard:**
- One-click access via "Setup Local LLM..." button in Settings
- Guides users through complete Ollama installation
- Platform-specific instructions (Windows, macOS, Linux)
- Real-time connection testing to verify Ollama is running
- Model download with progress tracking and cancellation

**Recommended Models for Translation:**
- **qwen2.5** (3B/7B/14B) - Excellent multilingual capabilities, recommended for translation
- **llama3.2** (3B/7B) - Strong general purpose, good European languages
- **mistral:7b** - Fast inference, good quality/speed balance
- **gemma2:9b** - Google's efficient model, good multilingual

**Status Widget in Settings:**
- Shows real-time Ollama connection status
- Displays currently selected model
- Quick-access button to Setup dialog
- Hardware specification summary

**Technical Implementation:**
- `modules/local_llm_setup.py` (NEW) - Complete setup module with:
  - `LocalLLMSetupDialog` - Full wizard UI with model recommendations
  - `LocalLLMStatusWidget` - Compact status widget for Settings panel
  - `detect_system_specs()` - RAM and GPU detection
  - `get_model_recommendations()` - Hardware-based model suggestions
  - `ModelDownloadWorker` - Background download with progress
  - `ConnectionTestWorker` - Async connection verification
- `modules/llm_clients.py` - Extended with Ollama support:
  - `OLLAMA_MODELS` dict with 7 supported models
  - `check_ollama_status()` - Connection and model detection
  - `_call_ollama()` - REST API integration (OpenAI-compatible)
  - `translate()` routes to Ollama when selected

**Privacy & Cost Benefits:**
- All translation processing stays on your computer
- No data sent to external servers
- No API key required
- No per-token costs - unlimited translations
- Works completely offline after model download

---

## [1.9.15] - November 30, 2025

### 📋 Supervertaler Bilingual Table Export/Import

**New bilingual table format for proofreading and review workflows:**

**Export Options (File → Export):**
- **"Bilingual Table - With Tags (DOCX)"**: Exports 5-column table (Segment #, Source, Target, Status, Notes) with raw Supervertaler tags preserved. Intended for proofreaders to review and edit - can be re-imported after editing
- **"Bilingual Table - Formatted (DOCX)"**: Same structure but applies formatting: `<b>` becomes actual bold, `<i>` becomes italic, `<u>` becomes underline, list tags become visible markers (• for bullets, ◦ for nested). For client delivery or archiving - cannot be re-imported

**Import Option (File → Import):**
- **"Bilingual Table (DOCX) - Update Project"**: Re-imports edited bilingual table, compares with current project by segment number, shows preview of all changes (old vs new target), applies approved changes with status reset to "Not Started"

**Document Format:**
- Header with "Supervertaler Bilingual Table" title linking to Supervertaler.com
- Language names in column headers (e.g., "English", "Dutch" instead of "Source", "Target")
- Pink highlighting for tags in the With Tags version
- Footer with Supervertaler.com branding
- Decorative underlines for professional appearance

**Technical Implementation:**
- `export_review_table_with_tags()` - Wrapper for tag-visible export
- `export_review_table_formatted()` - Wrapper for formatted export with warning dialog
- `_export_review_table(apply_formatting)` - Core export logic with python-docx
- `_add_hyperlink_to_paragraph()` - Helper for Word hyperlinks via XML manipulation
- `import_review_table()` - Import logic with change detection and diff preview

---

## [1.9.14] - November 30, 2025

### 📤 Improved DOCX Export & Keyboard Navigation

**DOCX Export Improvements:**
- **Formatting Preservation:** Export now properly converts `<b>`, `<i>`, `<u>`, `<bi>` tags to actual Word formatting (bold, italic, underline)
- **Multi-Segment Paragraphs:** Export handles paragraphs containing multiple segments with partial replacement
- **Unicode Cleanup:** Removes problematic characters like U+FFFC (Object Replacement Character)
- **Tag Stripping:** Properly strips all list tags (`<li-o>`, `<li-b>`, `<li>`) while preserving formatting tags

**Keyboard Navigation Fix:**
- Ctrl+Home now properly navigates to first segment even when editing inside a grid cell
- Ctrl+End now properly navigates to last segment even when editing inside a grid cell
- Added `_get_main_window()` helper to both `EditableGridTextEditor` and `ReadOnlyGridTextEditor`

**Technical Changes:**
- `export_target_only_docx()`: Added `apply_formatted_text_to_paragraph()` for parsing tags into Word runs
- `export_target_only_docx()`: Added `replace_segments_in_text()` for partial segment replacement
- `export_target_only_docx()`: Added `clean_special_chars()` to remove Unicode replacement characters
- `EditableGridTextEditor.keyPressEvent()`: Added Ctrl+Home/End handlers
- `ReadOnlyGridTextEditor.event()`: Added Ctrl+Home/End handlers

---

## [1.9.13] - November 30, 2025

### 📄 Document Preview & List Formatting Tags

**New Preview tab shows formatted document view:**

**Preview Tab Features:**
- New "Preview" tab alongside Source/Target views in the main panel
- Shows formatted document with headings (H1-H6 with proper sizing), paragraphs, and lists
- List items display with correct prefix: numbers (1. 2. 3.) for ordered lists, bullets (•) for bullet points
- Click any text in preview to instantly navigate to that segment in the grid
- Read-only view for document context during translation

**List Type Detection from DOCX:**
- New `_get_list_type()` method in docx_handler.py examines Word's numPr XML structure
- Properly distinguishes numbered lists from bullet points by analyzing abstractNum definitions
- Looks for "bullet" in numFmt value or bullet characters (•, ○, ●, ■) in lvlText
- Caches list type lookups for performance

**New List Tags:**
- `<li-o>` - Ordered list items (numbered: 1. 2. 3.)
- `<li-b>` - Bullet list items (•)
- Both tags are colored with the tag highlighter
- Both work with Ctrl+, shortcut for quick insertion

**Type Column Improvements:**
- Type column now shows `#1`, `#2`, `#3` for ordered list items (numbered)
- Shows `•` for bullet list items
- Shows `¶` (paragraph mark) for continuation paragraphs instead of `#`
- Provides clearer visual distinction between list types

**Technical Implementation:**
- Added `_setup_preview_tab()` for Preview tab creation
- Added `_render_preview()` method with formatted text rendering
- Added `_render_formatted_text()` helper for styled QTextEdit output
- Updated tag regex pattern to support hyphenated tags: `[a-zA-Z][a-zA-Z0-9-]*`
- Preview connects to `_preview_navigation_requested()` for click-to-navigate

---

## [1.9.12] - November 28, 2025

### 📊 Progress Indicator Status Bar

**New permanent status bar showing real-time translation progress:**

**Progress Display:**
- **Words translated**: Shows X/Y words with percentage (counts words in segments that have translations)
- **Confirmed segments**: Shows X/Y segments with percentage (confirmed, tr_confirmed, proofread, approved statuses)
- **Remaining segments**: Count of segments still needing work (not_started, pretranslated, rejected statuses)

**Color Coding:**
- **Red** (<50%): Low progress - needs attention
- **Orange** (50-80%): Making progress - keep going
- **Green** (>80%): Almost done - near completion

**Auto-Updates:**
- Updates when project is loaded
- Updates when segment is confirmed (Ctrl+Enter)
- Updates after AI translation completes
- Updates after user finishes typing (debounced)
- Resets to "--" when project is closed

**Technical Implementation:**
- Added `_setup_progress_indicators()` method for status bar widget setup
- Added `update_progress_stats()` method for calculating and updating progress
- Added `_get_progress_color()` helper for color-based progress feedback
- Progress widgets are permanent status bar items (right-aligned)

---

## [1.9.11] - November 28, 2025

### 🔧 Non-Translatables: Case-Sensitive & Full-Word Matching

**Improved non-translatables matching to prevent false positives:**

**Matching Improvements:**
- Non-translatables matching is now **case-sensitive by default**
- Only matches **full words** (not partial words like "Product" inside "ProductName")
- Uses word boundary detection (`\b`) for accurate term matching
- Smart fallback for special characters like ® and ™ that don't work with word boundaries
- Prevents unwanted replacements in the middle of compound terms

**Bug Fixes:**
- Fixed crash when closing project: added missing `stop_termbase_batch_worker()` method
- Fixed `.svprompt` files not showing in Prompt Library tree (added extension to both library and manager)
- Added LLM refusal detection for batch translation with helpful error messages when AI refuses content

**Technical Details:**
- Changed `case_sensitive` default to `True` in `NonTranslatablesManager.matches()`
- Rewrote matching logic to use regex word boundaries for full-word matching
- Added proper error handling for OpenAI content policy refusals during batch translation

---

## [1.9.10] - November 28, 2025

### 🔧 TM Search Fixes & Flexible Language Matching

**Fixed TM matches not appearing in Translation Results panel:**

**Root Cause Analysis:**
- `tm_metadata_mgr` was only initialized when user opened TM List tab, but TM search runs immediately on segment navigation
- Database had mixed language formats ("Dutch", "nl", "nl-NL") but search only looked for ISO codes
- Legacy hardcoded `enabled_only=True` filter would search only 'project' and 'big_mama' TMs that don't exist

**Fixes Applied:**
- **Early initialization:** `tm_metadata_mgr` now initializes in `initialize_tm_database()` when project loads
- **Flexible language matching:** New `get_lang_match_variants()` function returns both ISO codes and full language names
- **Bypass legacy filter:** Added `enabled_only=False` to all `search_all()` calls
- **Fallback search:** When no TMs are explicitly activated, search now falls back to all TMs

**Database Improvements:**
- Cleaned public database (`user_data/Translation_Resources/supervertaler.db`) for new GitHub users
- Removed sample data that had orphaned TM entries without proper metadata
- Schema preserved - new users start with empty, properly structured database

**Code Cleanup:**
- Removed legacy `project` and `big_mama` TM hardcoding from `TMDatabase` class
- These were from the previous Supervertaler architecture and are no longer used
- All TMs now managed through `TMMetadataManager` with proper database storage

**Files Modified:**
- `Supervertaler.py` - TM metadata manager early init, enabled_only=False for searches
- `modules/translation_memory.py` - Removed legacy tm_metadata dict
- `modules/database_manager.py` - Flexible language matching in get_exact_match() and search_fuzzy_matches()
- `modules/tmx_generator.py` - Added get_lang_match_variants() and updated get_base_lang_code()

### 📊 Non-Translatables Entry Table Enhancements

**Sortable Columns:**
- Columns in the Non-Translatables entry table are now sortable by clicking on column headers
- Click on Pattern, Type, or other columns to sort alphabetically ascending/descending
- Default sort by Pattern column (ascending)
- Sorting is temporarily disabled during table refresh to prevent UI issues

**Delete Entries:**
- Right-click on selected entries to access context menu with delete option
- Press Delete key to remove selected entries
- Menu dynamically shows "Delete 1 entry" or "Delete N entries" based on selection
- Existing "🗑️ Remove Selected" button also still available

---

## [1.9.9] - November 27, 2025

### 🎨 memoQ-style Alternating Row Colors

**CafeTran Formatting Support:**
- Pipe symbols (|) now highlighted in red/bold in grid editor (like CafeTran)
- Ctrl+, inserts pipe symbols for CafeTran formatting (or wraps selection)
- Ctrl+Shift+S copies source text to target cell

**Keyboard Shortcuts Improvements:**
- Keyboard shortcuts table now sortable by clicking column headers
- Removed "Save Project As" shortcut (Ctrl+Shift+S now dedicated to copy source)

**Settings Changes:**
- Batch size default changed from 100 to 20 segments per API call

---

## [1.9.7] - November 27, 2025

### 🔄 CafeTran Bilingual DOCX Support

**Full import/export support for CafeTran bilingual table format:**

**CafeTran Import:**
- New **Import > CafeTran Bilingual Table (DOCX)...** menu option
- Validates CafeTran bilingual format (ID | Source | Target | Notes table)
- Extracts segments with pipe symbol formatting markers preserved
- Converts to internal segment format for translation
- Stores handler for round-trip export

**CafeTran Export:**
- New **Export > CafeTran Bilingual Table - Translated (DOCX)...** menu option
- Writes translations back to Target column
- Preserves pipe symbol formatting (bold/underline markers)
- Maintains original table structure
- File can be imported back into CafeTran

**Technical Implementation:**
- Uses `modules/cafetran_docx_handler.py` module
- `CafeTranDOCXHandler` class handles file I/O
- `FormattedSegment` class preserves pipe symbol markers
- Red/bold formatting for pipe symbols in export

---

## [1.9.4] - November 26, 2025

### 🏷️ Tag-Based Formatting System for memoQ Bilingual Files

**Complete inline formatting support for professional translation workflows with memoQ bilingual DOCX files.**

**Phase 1 - Import & Display:**
- Import memoQ bilingual DOCX preserves bold, italic, underline as `<b>`, `<i>`, `<u>` HTML-style tags
- New "🏷️ Tags ON/OFF" toggle button in grid toolbar
- WYSIWYG mode: Shows formatted text (bold appears bold)
- Tag mode: Shows raw tags like `<b>bold</b>` for precise editing
- Keyboard shortcut: **Ctrl+Alt+T** to toggle between modes
- Tags auto-enabled after import when formatting detected
- TagHighlighter colorizes tags with pink background for visibility

**Phase 2 - Export with Formatting:**
- Export converts `<b>`, `<i>`, `<u>` tags back to actual Word formatting
- New `tagged_text_to_runs()` function parses tags into Word runs
- Round-trip fidelity: Import → Edit → Export preserves formatting
- Handles nested tags correctly (e.g., `<b><i>bold italic</i></b>`)

**Phase 3 - AI Translation with Tags:**
- Updated default system prompt with inline formatting tag instructions
- AI translates text while preserving and repositioning tags intelligently
- Example: "Click the `<b>`Save`</b>` button" → "Klik op de knop `<b>`Opslaan`</b>`"
- Tags placed around corresponding translated words, not just same position

**Formatting Shortcuts in Target Editor:**
- **Ctrl+B** - Apply/toggle bold tags on selected text
- **Ctrl+I** - Apply/toggle italic tags on selected text
- **Ctrl+U** - Apply/toggle underline tags on selected text

**Helper Functions Added:**
- `runs_to_tagged_text()` - Convert Word runs to tagged text on import
- `tagged_text_to_runs()` - Parse tags back to Word runs on export
- `strip_formatting_tags()` - Remove tags for plain text
- `has_formatting_tags()` - Check if text contains formatting tags
- `get_formatted_html_display()` - Convert tags to HTML for WYSIWYG display

---

## [1.9.6] - November 27, 2025

### 📁 Custom File Extensions & Monolingual Export

**New Branded File Extensions:**
- **Projects:** `.svproj` (was `.json`) - Supervertaler Project files
- **Prompts:** `.svprompt` (was `.md`/`.json`) - Supervertaler Prompt files  
- **Non-Translatables:** `.svntl` (was `.ntl`) - Supervertaler Non-Translatable lists
- All formats maintain full backward compatibility - opens legacy files seamlessly
- New files created with branded extensions for professional consistency
- Industry standards retained: `.tmx` for TM exports, `.srx` planned for segmentation

**Monolingual DOCX Import Improvements:**
- Language pair selection dialog when importing monolingual DOCX files
- Dropdown selectors for source and target language (12 languages supported)
- Prevents language detection issues - user explicitly sets translation direction
- Removed unreliable auto-detect language feature

**Target-Only DOCX Export:**
- New **Export > Target Only (DOCX)...** menu option for monolingual exports
- Preserves original document structure (tables, formatting, styles, headers)
- Copies original DOCX as template before replacing text
- Replaces text in both paragraphs and table cells
- Falls back gracefully if original document unavailable

**Project Persistence:**
- Original DOCX path now saved in project files (`original_docx_path`)
- Path restored when reopening projects for reliable exports
- Enables structure-preserving exports even after closing and reopening

**Documentation Updates:**
- New modular documentation: QUICK_START.md, KEYBOARD_SHORTCUTS.md, CAT_WORKFLOW.md
- Archived legacy USER_GUIDE.md and INSTALLATION.md
- FAQ.md copied to repository root (fixes dead link)

---

## [1.9.5] - November 27, 2025

### 📤 Send Segments to TM & memoQ Tag Shortcuts

**Send Segments to TM (Bulk Operation):**
- New dialog under **Edit > Bulk Operations > Send Segments to TM**
- Send translated segments directly to selected Translation Memories
- **Scope filters:** All segments, Current selection, or specific row range
- **Status filters:** Filter by Translated, Reviewed, Approved, Needs Review, or Final status
- Select multiple TMs to write to simultaneously
- Shows count of segments that will be sent before execution
- Progress feedback with success/failure counts

**memoQ Tag Insertion Shortcut:**
- **Ctrl+,** (Ctrl+Comma) - Insert next memoQ tag pair or wrap selection
- Smart tag insertion: Analyzes source segment for memoQ tags (`[1}`, `{1]`, `[3]`, etc.)
- With selection: Wraps selected text with next unused tag pair
- Without selection: Inserts next available tag pair at cursor
- Works with paired tags (`[1}...{1]`) and standalone tags (`[3]`)
- Respects tag order from source segment for consistency

**UI Improvements:**
- Renamed "Translation Resources" tab to "Resources" for cleaner UI
- Resources tab contains TM, Termbase, and MT/Web resources sub-tabs

---

## [1.9.3] - November 26, 2025

### 📋 Session Log Tab & TM/Termbase Defaults Fix

**Session Log Tab:**
- Added Session Log tab to bottom panel alongside Comments and Termview
- Real-time log display with timestamps in monospace font
- Easy access to log messages without detaching window
- Read-only display with automatic scrolling to latest entries

**TM/Termbase Checkbox Defaults Fixed:**
- Read checkboxes now default to unchecked (inactive) when no project loaded
- Read checkboxes default to unchecked when no activation record exists
- Write checkboxes default to unchecked (read-only) by default
- All settings properly restored from project.json when project is loaded
- Fixed `is_tm_active()` in tm_metadata_manager.py to return False by default

**Quick Actions for Bulk Selection:**
- Added "Select All Read" and "Select All Write" checkboxes above TM table
- Added "Select All Read" and "Select All Write" checkboxes above Termbase table
- Green checkbox for Read, blue checkbox for Write matching table style
- Quickly activate/deactivate all resources with single click

---

## [1.9.2] - November 25, 2025

### ⚙️ Superlookup Settings UI Redesign

**Improved Resource Selection Interface:**
- Redesigned Settings tab with sub-tabs for TM, Termbase, MT, and Web Resources
- Each resource type now has dedicated full-height space in its own sub-tab
- Replaced cramped single-page layout with spacious tabbed interface

**Proper Checkbox Styling:**
- Replaced tiny multi-selection indicators with standard Supervertaler checkboxes
- 18x18px checkbox size with green (#4CAF50) background when checked
- White checkmark (✓) drawn on checked items matching AutoFingers style
- QScrollArea + CheckmarkCheckBox widgets instead of QListWidget
- Hover effects and proper visual feedback

**Technical Implementation:**
- `create_settings_tab()`: Creates QTabWidget with 4 sub-tabs
- `create_tm_settings_subtab()`: Full-height TM selection with checkboxes
- `create_termbase_settings_subtab()`: Full-height termbase selection
- `create_mt_settings_subtab()`: Placeholder for future MT integration
- `create_web_settings_subtab()`: Placeholder for future web resources
- CheckmarkCheckBox widgets in QScrollArea provide proper green checkboxes
- Fixed `cursor()` → `cursor` property access for database queries

**Bug Fixes:**
- Fixed Translation Memories list loading (was showing empty due to cursor() call error)
- Fixed termbase loading timing (lazy loading when Settings tab viewed)
- Proper checkbox state tracking with `setProperty()` and `property()` methods
- Select All/Clear All buttons now work with checkbox widgets instead of selection

**User Experience:**
- Much more spacious and easier to read
- Clear visual separation between resource types
- Checkboxes are now clearly visible and clickable
- Consistent styling across entire application

---

## [1.9.1] - November 24, 2025

### ↩️ Undo/Redo for Grid Edits

**New Feature: Complete Undo/Redo System**
- Full undo/redo support for all grid editing operations
- Keyboard shortcuts: Ctrl+Z (Undo), Ctrl+Y/Ctrl+Shift+Z (Redo)
- Edit menu actions with dynamic enabled/disabled states
- 100-level undo history to prevent memory issues

**What's Tracked:**
- Target text changes as you type
- Status changes (Not Started → Translated → Confirmed)
- Ctrl+Enter confirmations
- Find/Replace batch operations
- Document view edits

**Technical Implementation:**
- Dual stack system (undo_stack + redo_stack) tracks segment changes
- Records: segment_id, old_target, new_target, old_status, new_status
- Smart recording: Only captures actual changes, ignores no-ops
- Automatic redo stack clearing on new edits (standard undo behavior)
- Stack trimming to max 100 levels for memory efficiency
- Updates both segment data and grid display simultaneously

**Integration Points:**
- `on_target_text_changed()`: Text editing in grid cells
- `update_status_icon()`: Status changes via toolbar/ribbon
- `on_doc_status_change()`: Document view status changes
- `replace_all_matches()`: Batch find/replace operations
- Ctrl+Enter confirmation handler

**User Experience:**
- Menu actions show enabled/disabled state based on stack contents
- Seamless integration with existing editing workflow
- No performance impact on grid operations
- Professional CAT tool behavior (like memoQ/Trados)

---

## [1.9.0] - November 24, 2025

### 🔍 Termview - RYS-Style Inline Terminology Display

**New Feature: Visual Inline Terminology**
- Added "🔍 Termview" tab in bottom panel showing inline terminology like RYS Trados plugin
- Source text displayed as flowing words with translations appearing underneath matched terms
- Compact 8pt font with colored 2px top borders (pink for project termbase, blue for background)
- Text wrapping with FlowLayout to adapt to window width
- Click any translation to insert it into target segment
- Hover tooltips show full term details and metadata

**Technical Implementation:**
- `modules/termview_widget.py`: New widget with FlowLayout, TermBlock classes for visual display
- RYS-style tokenization preserves multi-word terms (e.g., "De uitvinding heeft betrekking op een werkwijze")
- Direct integration with Translation Results termbase cache for instant updates
- Smart refresh: Updates immediately after termbase search completes

**Termbase Search Enhancements:**
- Fixed punctuation handling: Terms like "gew.%" now matched correctly
- Changed from `strip()` to `rstrip()/lstrip()` to preserve internal punctuation
- Use lookaround word boundaries `(?<!\w)(?!\w)` for terms with punctuation
- Standard `\b` boundaries for regular words

**Bug Fixes:**
- Fixed data format mismatch between termbase cache dict and Termview list format
- Fixed timing issue where Termview updated before termbase search completed
- Fixed tokenization regex to capture terms with special characters
- Removed debug logging after successful implementation

### 🎯 Priority & Visual Improvements
- Project termbases (#1 priority) display with pink border for instant recognition
- Background termbases display with blue border
- Clean, minimal design with 1px padding and compact spacing

---

## [1.8.0] - November 23, 2025

### UI/UX Improvements
- **Tab Styling Refinement**: Reduced selected tab border-bottom from 3px to 1px for a more subtle, professional appearance
- **Visual Consistency**: Maintained light blue background highlighting (rgba(33, 150, 243, 0.08)) with thinner accent line
- **Applied Across Application**: Updated styling for all tab widgets including Resources, Modules, TM, Settings, Domain, Import, Results, and Prompt Manager tabs
- **Theme Manager Update**: Global tab styling now uses refined 1px border-bottom for consistent appearance

### Technical Changes
- Updated border-bottom styling in 12 locations across main application and modules
- Modified theme_manager.py for global tab appearance consistency
- Maintained focus removal and outline suppression for cleaner tab interactions

---

## [1.6.6] - November 23, 2025

### ✅ Simplified TM/Termbase Management System

**Major Redesign:**

- 🎯 **Simple Read/Write Checkbox System**
  - Removed confusing "Active" checkbox and "Project TM/Termbase" concepts
  - **Translation Memories:** Simple Read (green ✓) and Write (blue ✓) checkboxes
  - **Termbases:** Simple Read (green ✓) and Write (blue ✓) checkboxes  
  - All TMs and termbases start completely unchecked by default
  - Users explicitly check Read to use for matching, Write to allow updates
  
- 📊 **Auto-Priority System for Termbases**
  - Priorities 1-N automatically assigned to Read-enabled termbases
  - Priority #1 = Project Termbase (pink highlighting, highest priority)
  - Priority #2, #3, etc. = Background termbases (lower priorities)
  - No manual project termbase designation needed - just check Read boxes
  - Priority based on activation order (ranking in database)

- 🎨 **Cleaner Column Layout**
  - **TMs:** `TM Name | Languages | Entries | Read | Write | Last Modified | Description`
  - **Termbases:** `Type | Name | Languages | Terms | Read | Write | Priority`
  - Removed redundant columns and confusing labels
  - Type auto-shows "📌 Project" for priority #1, "Background" for others

- 🔒 **Read-Only Database Defaults**
  - New TMs created with `read_only=1` (Write unchecked by default)
  - New termbases created with `read_only=1` (Write unchecked by default)
  - Prevents accidental updates to reference memories
  - User must explicitly enable Write for TMs/termbases they want to update

**Benefits:**
- Much simpler mental model: Read = use for matching, Write = allow updates
- No more confusion about "Active" vs "Project" vs "Background"
- Project termbase is simply the highest priority (first activated)
- Clear visual feedback with color-coded checkboxes (green Read, blue Write)
- Safer defaults prevent accidental corruption of reference resources

---

## [1.7.9] - November 22, 2025

### 🔍 Find/Replace & TM Enhancements

**Fixed:**

- ✨ **Find/Replace Highlighting System** - Complete rewrite using consistent QTextCursor approach
  - "Find Next" now correctly highlights matches with yellow background
  - "Highlight All" button now actually highlights all matches in the grid
  - Font size no longer changes during navigation (previously shrunk with each find)
  - Switched from QLabel+HTML (which replaced widgets) to QTextCursor+QTextCharFormat (preserves existing widgets)
  - Matches same highlighting system used by filter boxes
  - Supports case-sensitive/insensitive, whole words, and entire segment modes

- ✨ **No More TM Saves During Find/Replace** - Eliminated slowdowns during search navigation
  - Added `find_replace_active` flag to disable background TM saves
  - Prevents segments from being saved to TM on every "Find Next" click
  - Re-enables TM saves when dialog closes
  - Also disables expensive TM/MT/LLM lookups during find/replace operations
  - Results in much faster navigation through search results

**Added:**

- 🌍 **Bidirectional TM Search** - TMs now search in both directions automatically
  - When translating nl→en, also searches en→nl TMs for reverse matches
  - Example: English source text can match Dutch source in reverse TM
  - Reverse matches clearly marked with "Reverse" indicator
  - Improves TM utilization by ~2x without any user action required

- 🌍 **Language Variant Matching** - Base language codes match all regional variants
  - "en" matches "en-US", "en-GB", "en-AU" automatically
  - "nl" matches "nl-NL", "nl-BE" automatically  
  - TMX import now handles language variants gracefully
  - User can choose to strip variants or preserve them during import
  - Supports bidirectional matching with variants (e.g., nl-BE → en-US works both ways)

- 💾 **Activated TM Persistence** - Projects remember which TMs are active
  - Activated TMs saved to `project.json` in `tm_settings.activated_tm_ids`
  - Automatically restored when project is reopened
  - No more manually re-activating TMs for each project session
  - Works per-project (different projects can have different active TMs)

- 📝 **TM Pre-Check in Batch Translation** - Saves API costs by checking TM first
  - Before making expensive API calls, checks if 100% TM matches exist
  - Auto-inserts TM matches and skips API translation for those segments
  - Shows clear log of how many API calls were saved
  - Can save significant costs on projects with high TM leverage
  - Controlled by "Check TM before API call" setting (enabled by default)

- 🎨 **Language Display Normalization** - Consistent language variant format
  - All language variants displayed as lowercase-UPPERCASE (e.g., nl-NL, en-US)
  - Previously: inconsistent formats like "nl-nl", "EN-us", "NL-BE"
  - Now: standardized as "nl-NL", "en-US", "nl-BE"
  - Applied in TM manager UI, TMX import dialogs, and all TM displays

**Technical Details:**

- **Find/Replace Highlighting:**
  - `highlight_search_term()` rewritten to use `QTextCursor` and `QTextCharFormat`
  - `highlight_all_matches()` rewritten to actually highlight instead of just filtering
  - Added `processEvents()` after grid load to ensure widgets exist before highlighting
  - Files: `Supervertaler.py` lines 15726-15792, 15982-16008

- **TM Save Prevention:**
  - Added `find_replace_active` flag check in `_handle_target_text_debounced_by_id()` (line 13660)
  - Added same check in `update_status_icon()` (line 13703)
  - Added check in `on_cell_selected()` to skip TM/MT/LLM lookups (line 14050)
  - Files: `Supervertaler.py` lines 13657-13664, 13699-13709, 14044-14051

- **Bidirectional Search:**
  - `get_exact_match()` now searches reverse direction if no forward match found
  - `search_fuzzy_matches()` includes reverse direction results
  - Results marked with `reverse_match: True` metadata
  - Files: `modules/database_manager.py` lines 635-732, 744-810

- **Language Variant Matching:**
  - Added `get_base_lang_code()` to extract base from variants (en-US → en)
  - Added `normalize_lang_variant()` for consistent display formatting
  - Added `languages_are_compatible()` for base code comparison
  - Database queries use LIKE pattern: `(source_lang = 'en' OR source_lang LIKE 'en-%')`
  - Files: `modules/tmx_generator.py` lines 119-156, `modules/database_manager.py` lines 652-676

- **TMX Import with Variants:**
  - `detect_tmx_languages()` reads all language codes from TMX
  - `check_language_compatibility()` analyzes variant mismatches
  - `_load_tmx_into_db()` accepts `strip_variants` parameter
  - User dialog offers "Import with variant stripping" vs "Create new TM"
  - Files: `modules/translation_memory.py` lines 408-557, `Supervertaler.py` lines 4807-4903

- **TM Persistence:**
  - Added `tm_settings` field to `Project` class (line 223)
  - `save_project_to_file()` saves activated TM IDs (lines 11442-11449)
  - `load_project()` restores activated TMs (lines 10797-10816)
  - Files: `Supervertaler.py` lines 220-285, 10794-10816, 11439-11449

**User Experience:**

- Find/Replace dialog now fast and responsive with proper highlighting
- "Highlight All" button finally works as expected
- No font size changes during search navigation
- TMs work across language variants automatically (no manual configuration)
- Projects remember your TM activation choices
- Batch translation saves money by checking TM first
- Clear visual feedback for all TM operations

---

## [1.7.8] - November 22, 2025

### 🔍 Filter Highlighting Fix

**Fixed:**

- ✨ **Filter Search Term Highlighting** - Fixed highlighting of search terms in filtered segments
  - Source and target filter boxes now correctly highlight matching terms in yellow
  - Previously used delegate-based highlighting which was bypassed by cell widgets
  - New implementation uses widget-internal highlighting with QTextCursor + QTextCharFormat
  - Case-insensitive matching: "test", "TEST", "TeSt" all match "test"
  - Multiple matches per cell are highlighted correctly
  - Highlights automatically clear when filters are removed

**Technical Details:**

- **Root Cause:** Source/target cells use `setCellWidget()` with QTextEdit widgets, which completely bypass `QStyledItemDelegate.paint()` method
- **Solution:** Created `_highlight_text_in_widget()` method that applies highlighting directly within QTextEdit widgets
- **Implementation:**
  - Uses `QTextCursor` to find all occurrences of search term in widget's document
  - Applies `QTextCharFormat` with yellow background (#FFFF00) to each match
  - Clears previous highlights before applying new ones
  - Modified `apply_filters()` to call widget highlighting instead of delegate approach
  - `clear_filters()` automatically clears highlights by reloading grid
- **Files Modified:**
  - `Supervertaler.py` (lines ~15765-15810): New `_highlight_text_in_widget()` method
  - `Supervertaler.py` (lines ~15779-15860): Modified `apply_filters()` to use widget highlighting
- **Documentation Added:**
  - `docs/FILTER_HIGHLIGHTING_FIX.md` - Complete technical explanation of the fix

**User Experience:**

- Filter boxes now work as expected with visible yellow highlighting
- Improves searchability and visual feedback when filtering segments
- No performance impact with large segment counts (tested with 219 segments)

---

## [1.7.7] - November 21, 2025

### 🎯 Termbase Display Customization

**Added:**

- ✨ **User-Configurable Termbase Sorting** - Control how termbase matches are displayed
  - Three sorting options available in Settings → General:
    - **Order of appearance in source text** (default) - Matches appear as they occur in the segment
    - **Alphabetical (A-Z)** - Matches sorted by source term alphabetically
    - **By length (longest first)** - Longer multi-word terms prioritized over shorter ones
  - Sorting preference persists across sessions
  - Only affects termbase matches; TM, MT, and LLM results maintain their existing order

- ✨ **Smart Substring Filtering** - Reduces termbase match clutter
  - Optional "Hide shorter termbase matches" checkbox in Settings → General
  - Automatically filters out shorter terms that are fully contained within longer matched terms
  - Example: If both "cooling" and "cooling system" match, only "cooling system" is shown
  - Helps focus on the most relevant multi-word terminology
  - Can be toggled on/off without restarting the application

**Enhanced:**

- 🔧 **Bold Font for Project Resources** - Project termbases and TMs now display with bold provider codes (TB, TM) instead of asterisks for cleaner visual distinction
- 🎨 **Translation Results Panel** - Added parent app reference for accessing user settings dynamically

**Technical Details:**

- Settings stored in `ui_preferences.json` under `general_settings`
- `TranslationResultsPanel` now accepts `parent_app` parameter for settings access
- New methods: `_sort_termbase_matches()` and `_filter_shorter_matches()` in `translation_results_panel.py`
- Sorting uses case-insensitive comparison for alphabetical mode
- Filtering uses substring detection with length comparison
- Files Modified:
  - `Supervertaler.py` (lines 2391-2393, 7377-7406, 8316-8360, 8930, 9548, 12604-12606)
  - `modules/translation_results_panel.py` (lines 626-628, 1201-1276, 1324-1329)

**User Experience:**

- Settings are immediately accessible via Settings → General → TM/Termbase Options
- Tooltips explain each option clearly
- Changes apply to all subsequent segment matches
- No performance impact on match retrieval

---

## [1.7.6] - November 20, 2025

### 💾 Auto Backup System

**Added:**

- ✨ **Automatic Backup System** - Prevents data loss during translation work
  - Auto-saves project.json at configurable intervals (1-60 minutes, default: 5 minutes)
  - Auto-exports TMX backup file in same folder as project.json
  - TMX backup includes all segments for maximum recovery capability
  - Settings UI in Settings → General tab with enable/disable toggle
  - Non-intrusive background operation with timestamp logging
  - Settings persist across sessions in ui_preferences.json
  - Timer automatically restarts when settings are changed

**Technical Details:**

- QTimer-based system with millisecond precision
- Uses existing `save_project_to_file()` and `TMXGenerator` methods
- Graceful error handling without interrupting workflow
- Only runs when project is open and has a file path
- TMX file named `{project_name}_backup.tmx` for easy identification

---

## [1.7.5] - November 20, 2025

### 🐛 Critical Bug Fix - Translation Memory Save Flood

**Fixed:**

- ✅ **TM Save Flood During Grid Operations** - CRITICAL FIX
  - **Issue:** Every time `load_segments_to_grid()` was called (startup, filtering, clear filters), all segments with status "translated"/"confirmed"/"approved" would trigger false TM database saves 1-2 seconds after grid load
  - **Symptoms:**
    - 10+ second UI freeze on projects with 200+ segments
    - Massive unnecessary database writes (219 saves on a 219-segment project)
    - Made filtering operations completely unusable
    - Could potentially corrupt data or cause performance issues on large projects
  - **Root Cause:** Qt internally queues document change events when `setPlainText()` is called on QTextEdit widgets, even when signals are blocked. When `blockSignals(False)` was called after grid loading, Qt delivered all these queued events, triggering `textChanged` for every segment. By that time, the suppression flag had already been restored, so the suppression check failed.
  - **Solution:**
    - Added `_initial_load_complete` flag to `EditableGridTextEditor` class
    - Signal handler now ignores the first spurious `textChanged` event after widget creation
    - All subsequent real user edits are processed normally
    - Clean, minimal fix that doesn't interfere with Qt's event system
  - **Testing:** Verified on BRANTS project (219 segments) - zero false TM saves during startup, filtering, and filter clearing
  - **Files Modified:** Supervertaler.py (lines 835, 11647-11651)

**Impact:**
- **Performance:** Grid loading is now instant with no post-load freeze
- **Database:** Eliminates 200+ unnecessary database writes per grid operation
- **User Experience:** Filtering and grid operations are now fast and responsive
- **Data Integrity:** Prevents potential database corruption from excessive writes

---

## [1.7.4] - November 20, 2025

### 💾 Project Persistence Improvements

**Enhanced:**

- ✅ **Primary Prompt Persistence** - Projects now remember your selected primary prompt
  - Automatically restores primary prompt when reopening project
  - Updates UI label to show active prompt name
  - Works with Unified Prompt Library system
  
- ✅ **Image Context Folder Persistence** - Projects remember loaded image folders
  - Image context folder path saved to project.json
  - Automatically reloads all images from saved folder on project open
  - Updates UI status label showing image count and folder name
  - Logs success/warnings if folder path has changed
  
- ✅ **Attached Prompts Persistence** - All attached prompts are restored
  - Maintains complete prompt configuration across sessions
  - Updates attached prompts list UI on restore

**Technical:**
- Changed from `library.set_primary_prompt()` to `_set_primary_prompt()` for UI updates
- Changed from `library.attach_prompt()` to `_attach_prompt()` for UI updates
- Added `image_context_folder` to `prompt_settings` in project.json
- Proper UI synchronization on project load for all prompt settings

**User Experience:**
Now when you save a project, it remembers:
- ✓ Which primary prompt you selected
- ✓ Which prompts you attached
- ✓ Which image folder you loaded
- ✓ All settings restore automatically on project open

---

## [1.7.3] - November 20, 2025

### 🧪 Prompt Preview & System Template Improvements

**New Features:**

**Added:**
- ✅ **Preview Combined Prompts Button** - New "🧪 Preview Prompts" button in Project Editor segment action bar
  - Shows complete assembled prompt that will be sent to AI
  - Displays System Template + Custom Prompts + current segment text
  - Real-time composition info (segment ID, languages, character count, attached prompts)
  - Visual context indicator showing which images will be sent alongside text
  - Clear tooltip explaining functionality

**Enhanced:**
- ✅ **System Template Editor** - Improved layout and usability in Settings → System Prompts
  - Increased text editor height from 400px to 500px
  - Added stretch factors for proper expansion to fill available space
  - Enabled word wrap at widget width for easier reading
  - Set plain text mode to prevent formatting issues
  
- ✅ **Figure Context Detection** - Fixed regex pattern for accurate figure reference detection
  - Now correctly matches "Figuur 3" → "3" instead of "3toont"
  - Properly handles subfigures (e.g., Figure 1A, 2B)
  - Requires space between "figuur/figure/fig" and number

**Improved:**
- ✅ **Image Context Preview** - Preview dialog now shows detailed image information
  - 🖼️ Displays which images will be sent with prompt (e.g., "Figure 3")
  - ⚠️ Warns if references detected but images not found
  - ℹ️ Shows info when images loaded but not referenced in segment
  - Yellow banner highlights when images are being sent as binary data

**Technical:**
- Updated `UnifiedPromptManagerQt._preview_combined_prompt()` to access actual segment data
- Added `_preview_combined_prompt_from_grid()` method in main app
- Fixed attribute reference from `self.unified_prompt_manager` to `self.prompt_manager_qt`
- Improved figure reference regex from `[\w\d]+(?:[\s\.\-]*[\w\d]+)?` to `\d+[a-zA-Z]?`

---

## [1.7.2] - November 19, 2025

### 🔧 Termbase Critical Fixes - Term Deduplication & Selection

**Major Bug Fixes:**

**Fixed:**
- ✅ **Multiple Translations Display** - Fixed critical deduplication bug where only one translation was kept for terms with same source text
  - Example: "inrichting → device" AND "inrichting → apparatus" now both display correctly
  - Root cause: Used `source_term` as dict key, now uses `term_id` to allow multiple translations
- ✅ **Termbase Selection** - Terms now save only to selected termbases (previously saved to all active termbases)
  - Filter logic working correctly with INTEGER termbase IDs
  - Debug logging confirmed type matching works as expected
- ✅ **Segment Highlighting Consistency** - Termbase highlighting now works consistently across all segments
  - Fixed cache iteration to handle new dict structure with `term_id` keys
  - Updated all code paths that consume termbase matches

**Technical Changes:**
- **Dictionary Structure Change:**
  - Changed from: `matches[source_term] = {...}` (only one translation per source)
  - Changed to: `matches[term_id] = {'source': source_term, 'translation': target_term, ...}` (multiple translations allowed)
- **Code Locations Updated:**
  - `find_termbase_matches_in_source()` - Changed dict key from source_term to term_id
  - `highlight_termbase_matches()` - Updated to extract source term from match_info
  - `DocumentView._create_highlighted_html()` - Updated iteration logic
  - `_get_cached_matches()` - Fixed to extract source term from dict values (2 locations)
  - All hover tooltip and double-click handlers updated

**Impact:**
- 🎯 **Better Term Disambiguation** - Users can now add multiple translations for same source term
- 🎨 **Accurate Highlighting** - All matching terms highlighted correctly in grid
- ✅ **Correct Termbase Selection** - Terms added only to user-selected termbases

---

## [1.7.1] - November 19, 2025

### 🎨 Termbase UI Polish - Visual Consistency Improvements

**Bug Fixes & UI Improvements:**

**Fixed:**
- ✅ **Deleted Term Highlighting** - Fixed issue where deleted termbase terms remained highlighted after deletion and navigation
- ✅ **Termbase Name Display** - Termbase names now correctly shown in Term Info metadata area
- ✅ **Term Count Updates** - Term counts in termbase list now update immediately after adding terms
- ✅ **Project Termbase Colors** - Fixed project termbases showing blue instead of pink in translation results
- ✅ **Ranking Metadata** - Added missing `ranking` field to TranslationMatch metadata in all code paths

**Improved:**
- 🎨 **Visual Consistency** - Project termbase matches now display with same style as background termbases (colored number badge only)
- 🎯 **Effective Project Detection** - Uses `ranking == 1` as fallback when `is_project_termbase` flag is false
- 🔄 **Real-time Refresh** - Termbase list UI refreshes immediately via callback after term addition
- 📊 **Database Query Fix** - Fixed TEXT/INTEGER comparison with CAST for accurate term counts

**Technical:**
- Modified `highlight_termbase_matches()` to clear formatting before early return
- Added `termbase_name` extraction and display in translation results panel
- Implemented `refresh_termbase_list()` callback storage and invocation
- Added explicit boolean conversion for `is_project_termbase` from SQLite
- Updated `CompactMatchItem.update_styling()` to use consistent badge-only coloring
- Fixed two locations where `ranking` was missing from TranslationMatch metadata

---

## [1.7.0] - November 18, 2025

### 📚 Project Termbases - Dedicated Project Terminology

**Project-Specific Terminology Management** - A powerful new termbase system that distinguishes between project-specific terminology (one per project) and background termbases (multiple allowed), with automatic term extraction from project source text.

### Added

**Project Termbase System:**
- 📌 **Project Termbase Designation** - Mark one termbase per project as the official project termbase
- 🎨 **Pink Highlighting** - Project termbase matches highlighted in light pink (RGB 255, 182, 193) in both grid and results panel
- 🔵 **Background Termbases** - Regular termbases use priority-based blue shading as before
- 🔍 **Term Extraction** - Automatically extract terminology from project source segments
- 🧠 **Smart Algorithm** - Frequency analysis, n-gram extraction, scoring based on capitalization and special characters
- 🌐 **Multi-Language Support** - Stop words for English, Dutch, German, French, Spanish
- 📊 **Preview & Select** - Review extracted terms with scores before adding to termbase
- 🎯 **Configurable Parameters** - Adjust min frequency, max n-gram size, language, term count
- ⚙️ **Standalone Module** - Term extractor designed as independent module (`modules/term_extractor.py`) for future CLI tool

**Termbases Tab Enhancements:**
- 📋 **Type Column** - Shows "📌 Project" in pink or "Background" for each termbase
- 🔘 **Set/Unset Buttons** - Easy designation of project termbases
- 🔍 **Extract Terms Button** - Launch term extraction dialog (only enabled with project loaded)
- 🎨 **Visual Distinction** - Project termbase names shown in pink
- 🔒 **Validation** - System enforces "only one project termbase per project" rule

**Database Schema:**
- 🗄️ **is_project_termbase Column** - Added to termbases table with migration
- ✅ **Backward Compatible** - Existing databases upgraded automatically

**Termbase Manager Extensions:**
- `set_as_project_termbase(termbase_id, project_id)` - Designate project termbase
- `unset_project_termbase(termbase_id)` - Remove designation
- `get_project_termbase(project_id)` - Retrieve project termbase
- Enhanced `create_termbase()` with `is_project_termbase` parameter and validation
- Enhanced `get_all_termbases()` to sort project termbase first

**Match Pipeline Integration:**
- 🔗 **Metadata Tracking** - `is_project_termbase` flag passed through entire match pipeline
- 🎨 **Grid Highlighting** - Light pink backgrounds for project termbase matches in source column
- 📋 **Results Panel** - Light pink number badges for project termbase matches

### Changed
- Updated termbase search to include `is_project_termbase` field
- Modified `highlight_termbase_matches()` to use pink for project termbases
- Enhanced `TranslationMatch` metadata to capture project termbase status
- Updated `CompactMatchItem` styling to handle three-way color logic (forbidden=black, project=pink, background=blue)

### Technical Details
- **Term Extraction Algorithm:**
  - N-gram extraction (unigrams, bigrams, trigrams)
  - Frequency-based scoring with logarithmic scaling
  - Bonuses for capitalization (+3), special characters (+2), n-gram size (+1.5 per word)
  - Term classification: proper_noun, technical, phrase, word
  - Configurable filtering by frequency, type, score
- **Color Scheme:**
  - Project Termbase: `#FFB6C1` (light pink)
  - Forbidden Terms: `#000000` (black)
  - Background Termbases: `#4d94ff` (blue with priority-based darkening)

### Use Cases
- **Starting New Projects** - Extract project-specific terminology automatically
- **Consistency** - Ensure project terminology has visual precedence
- **Background Knowledge** - Maintain general termbases alongside project-specific ones
- **Source-Only Termbases** - Perfect for extracting terms before translation begins

---

## [1.6.5] - November 18, 2025

### 📁 File Dialog Memory - Smart Directory Navigation

**File Dialogs Remember Your Last Location** - A quality-of-life improvement that significantly streamlines workflow by automatically remembering the last directory you navigated to across all file dialogs throughout the application.

### Added

**File Dialog Helper System:**
- 📁 **Last Directory Memory** - File dialogs automatically open in the last used directory
- 💾 **Persistent Storage** - Last directory saved to config file between sessions
- 🔄 **Universal Coverage** - Works for all dialog types (open file, save file, select folder, multiple files)
- 🎯 **Automatic Detection** - Extracts directory from file paths automatically
- 🛠️ **Helper Module** - Created `modules/file_dialog_helper.py` with wrapper functions

**Config Manager Enhancements:**
- Added `get_last_directory()` - Retrieve the last used directory
- Added `set_last_directory()` - Save a directory as the last used location
- Added `update_last_directory_from_file()` - Extract and save directory from file path

**Integration Points:**
- Image Extractor (add DOCX files, select folder, output directory)
- TMX import/export dialogs
- Project open/save dialogs
- Export dialogs (JSON, TMX, etc.)

**Benefits:**
- No more navigating from program root every time
- Improved workflow when working with files in the same folder
- Transparent operation - works automatically without configuration
- Persists between application sessions

### Technical Implementation
- Created `modules/file_dialog_helper.py` with `get_open_file_name()`, `get_save_file_name()`, `get_existing_directory()`, `get_open_file_names()` wrappers
- Extended `config_manager.py` with directory tracking methods
- Updated key file dialog calls in `Supervertaler.py` to use helper functions
- Last directory stored in `~/.supervertaler_config.json` (or dev mode equivalent)

---

## [1.6.4] - November 18, 2025

### 🌐 Superbrowser - Multi-Chat AI Browser

**Work with Multiple AI Chats Simultaneously** - A revolutionary new tab that displays ChatGPT, Claude, and Gemini side-by-side in resizable columns with persistent login sessions, perfect for comparing AI responses or maintaining multiple conversation threads.

### Added

**Superbrowser Tab:**
- 🌐 **Three-Column Layout** - ChatGPT, Claude, and Gemini displayed simultaneously in resizable columns
- 🔐 **Persistent Sessions** - Login credentials saved between sessions (no need to log in every time)
- 🔧 **Collapsible Configuration** - Hide/show URL configuration panel to maximize screen space
- 🎨 **Color-Coded Columns** - Each AI provider has distinct color (green, copper, blue)
- 🏠 **Navigation Controls** - URL bar, reload, and home buttons for each column
- 💾 **Profile Storage** - Separate persistent storage for each AI provider (cookies, cache, sessions)
- 📱 **Minimal Headers** - Tiny 10px headers maximize space for chat windows
- 🎯 **Dev Mode Support** - Uses `user_data_private/` for dev mode, `user_data/` for production

**Technical Implementation:**
- Created `modules/superbrowser.py` - Standalone module with `SuperbrowserWidget`
- Integrated QtWebEngine with OpenGL context sharing for proper rendering
- Added persistent profile management using `QWebEngineProfile`
- Implemented `ChatColumn` class for individual browser columns
- Added to Specialised Tools as "🌐 Superbrowser" tab

**Use Cases:**
- Compare how different AI models respond to the same prompt
- Maintain separate conversation threads for different projects
- Quick access to all major AI assistants without switching browser tabs
- Research and development with multiple AI perspectives

### Fixed
- QtWebEngine DLL compatibility issues resolved (version matching)
- OpenGL context sharing properly initialized before QApplication creation
- Profile storage paths follow application's dev mode patterns

### Dependencies
- Added `PyQt6-WebEngine>=6.8.0,<6.9.0` requirement (version matched to PyQt6 6.8.1)

---

## [1.6.3] - November 18, 2025

### ⚡ UI Responsiveness & Precision Scroll Enhancements

**Major Performance Improvements & memoQ-Style Navigation** - Comprehensive UI responsiveness optimizations including debug settings system, disabled LLM auto-matching by default, precision scroll buttons, and auto-center active segment feature.

### Added

**Debug Settings System:**
- 🐛 **Debug Settings Tab** - New dedicated tab in Settings dialog for debugging and performance tuning
- 📝 **Verbose Logging Toggle** - Enable/disable detailed debug logs (textChanged events, update cycles, cell selection)
- 📤 **Debug Log Export** - Export debug logs to timestamped files (`supervertaler_debug_log_YYYYMMDD_HHMMSS.txt`)
- 🔄 **Auto-export Option** - Automatically export debug logs on application exit
- 🗑️ **Clear Log Buffer** - Manual clear button for debug log buffer (10,000 entry limit)
- ⏱️ **Debounce Delay Control** - Spinbox to adjust target text debounce delay (100-5000ms range, default 1000ms)
- ⚠️ **Performance Warnings** - Clear warnings about performance impact of verbose logging

**Precision Scroll Controls:**
- ⬆️⬇️ **Precision Scroll Buttons** - memoQ-style ▲▼ buttons for fine-grained grid scrolling
- 🎯 **Fixed Pixel Scrolling** - Uses fixed pixel amounts (5-50px) instead of variable row heights for predictable movement
- 🎚️ **Adjustable Precision** - Spinbox setting (1-10 divisor) to control scroll increment size:
  - Divisor 1 = 50 pixels (coarse)
  - Divisor 3 = 40 pixels (default)
  - Divisor 5 = 30 pixels (fine)
  - Divisor 10 = 5 pixels (very fine)
- 📊 **Live Preview** - Setting shows "Coarse/Medium/Fine/Very fine" label based on divisor value
- 📍 **Smart Positioning** - Buttons positioned to left of scrollbar, never cut off or overlapping
- 🎨 **Hover Effects** - Blue highlight on hover, visual feedback on click
- 🔄 **Auto-repositioning** - Buttons reposition on window resize and table changes

**Auto-Center Active Segment:**
- 🎯 **Keep Active Segment Centered** - Optional toggle to auto-scroll and center selected segment in viewport
- 🔄 **CAT Tool Behavior** - Matches memoQ, Trados, and other professional CAT tools
- ✅ **Settings Persistence** - Auto-center preference saved to `ui_preferences.json`
- 🖱️ **Smooth Navigation** - Active segment always visible and centered when navigating

**Performance Optimizations:**
- 🚫 **LLM Auto-matching Disabled by Default** - Changed `enable_llm_matching` from `True` to `False` to prevent 10-20 second UI freezes
- ⚡ **Conditional Debug Logging** - All verbose logs wrapped in `if self.debug_mode_enabled:` checks
- ⏱️ **Increased Debounce Delay** - Target text change debounce increased from 500ms to 1000ms
- 🎛️ **LLM Matching Toggle** - Added checkbox in General Settings with warning tooltip
- 💾 **Settings Persistence** - Debug mode, LLM matching, precision scroll, and auto-center settings saved/loaded

**UI/UX Improvements:**
- 📑 **Precision Scroll Settings Section** - New section in General Settings with all scroll-related controls
- ℹ️ **Helpful Tooltips** - Detailed explanations for all new settings
- ⚠️ **Warning Messages** - Clear warnings about LLM performance impact (10-20 sec per segment)
- 🎨 **Consistent Styling** - Settings UI follows existing design patterns

### Changed

- 🔧 **Default LLM Behavior** - LLM translations no longer trigger automatically on segment selection (use "Translate with AI" button instead)
- ⏱️ **Debounce Timing** - Target text debounce delay increased from 500ms to 1000ms for better stability
- 📊 **Debug Logging** - Performance-heavy debug logs now conditional (only when debug mode enabled)
- 🎯 **Scroll Algorithm** - Precision scroll now uses fixed pixel amounts instead of row-height-based calculations

### Fixed

- 🐛 **UI Freezing on Segment Selection** - Eliminated 10-20 second freezes caused by automatic LLM API calls
- 🐛 **Unpredictable Scroll Jumping** - Fixed precision scroll skipping segments due to variable row heights
- 🐛 **Button Positioning** - Fixed scroll buttons being cut off by scrollbar
- 🐛 **Method Name Mismatch** - Fixed `create_tabbed_assistance_panel` vs `create_assistance_panel` naming error
- 🐛 **Duplicate Method Definition** - Removed duplicate `position_precision_scroll_buttons` method
- 🐛 **TranslationResultsPanel Initialization** - Fixed incorrect `main_window` and `match_limits` parameters

### Technical Details

**Files Modified:**
- `Supervertaler.py` - Core application with all new features
- `ui_preferences.json` - Stores debug_mode_enabled, debug_auto_export, enable_llm_matching, precision_scroll_divisor, auto_center_active_segment

**Performance Impact:**
- MT engines (1-2 sec) remain enabled for auto-matching ✅
- LLM translations (10-20 sec) now on-demand only (via button) ✅
- Debug logging overhead eliminated in production use ✅
- Smoother segment navigation with predictable scroll behavior ✅

**Location:**
- Settings → 🐛 Debug (Debug settings tab)
- Settings → General Settings (LLM matching toggle, precision scroll settings)
- Grid → Right edge (Precision scroll buttons ▲▼)

---

## [1.6.2] - November 17, 2025

### 🖼️ Image Extractor (Superimage)

**Extract Images from DOCX Files** - New tool for extracting all images from DOCX files with preview and batch processing capabilities.

### Added

**Image Extraction:**
- 📄 **DOCX Image Extractor** - Extract all images from DOCX files (located in word/media/ folder)
- 🖼️ **PNG Output** - Convert all image formats to PNG with sequential naming (Fig. 1.png, Fig. 2.png, etc.)
- 📁 **Auto-folder Mode** - Option to automatically create "Images" subfolder next to source DOCX
- 📚 **Batch Processing** - Add multiple DOCX files or entire folders for bulk extraction
- 🎯 **Custom Prefix** - Configurable filename prefix (default: "Fig.")

**Image Preview:**
- 👁️ **Click-to-Preview** - Click any extracted file in list to view in preview panel
- 🖼️ **Resizable Preview** - Horizontal splitter between results and preview (60% preview area)
- ⬅️➡️ **Navigation Buttons** - Previous/Next buttons synced with file list
- 🔍 **Auto-scaling** - Images automatically scaled to fit viewport while maintaining aspect ratio

**UI/UX:**
- 🎨 **Compact Layout** - Optimized vertical space with single-row controls
- 📝 **Resizable Status Log** - Extraction progress log with minimum 50px height
- 📋 **File List Management** - Add files, add folder, clear list functionality
- 🛠️ **Tools Menu Integration** - Quick access via Tools → Image Extractor (Superimage)

**Technical:**
- 🔧 **New Module** - `modules/image_extractor.py` with `ImageExtractor` class
- 📖 **Documentation** - Complete user guide in `modules/IMAGE_EXTRACTOR_README.md`
- 🧪 **Test Script** - `tests/test_image_extractor.py` for validation
- 🎨 **PIL/Pillow** - Image format conversion (RGBA→RGB with white background)

**Location:**
- Translation Resources → Reference Images tab
- Tools → Image Extractor (Superimage)...

---

## [1.6.1] - November 17, 2025

### 📚 Enhanced Termbase Metadata System

**Extended Metadata & Improved UX** - Comprehensive termbase metadata with notes, project, and client fields, plus instant refresh functionality.

### Added

**Enhanced Metadata Fields:**
- 📝 **Notes Field** - Multi-line notes field replacing old definition field for context, usage notes, and URLs
- 🔗 **Clickable URLs** - URLs in notes automatically become clickable links (opens in external browser)
- 📁 **Project Field** - Track which project a term belongs to
- 👤 **Client Field** - Associate terms with specific clients
- 🏷️ **Domain Field** - Already existed, now fully integrated throughout system

**Termbase Viewer Enhancements:**
- 📖 **Dedicated Termbase Viewer** - New panel at bottom of Translation Results showing selected termbase entry
- 🔄 **Refresh Data Button** - Manual refresh button to reload latest data from database
- ✏️ **Edit Button** - Direct access to edit dialog from termbase viewer
- 🖱️ **Right-Click Edit** - Context menu on termbase matches for quick editing
- ♻️ **Auto-Refresh on Edit** - Termbase viewer automatically updates after editing entry

**Improved Table Views:**
- 📊 **Extended Columns** - Edit Terms dialog now shows: Source, Target, Domain, Priority, Notes (truncated), Project, Client, Forbidden
- 📏 **Smart Column Widths** - Optimized column sizing for better visibility
- ✂️ **Notes Truncation** - Long notes truncated to 50 characters with "..." in table view

**Database Enhancements:**
- 🗄️ **Database Migration System** - Automated schema updates for backward compatibility
- ➕ **New Columns** - Added `notes`, `project`, `client` columns to `termbase_terms` table
- 🔗 **Synonyms Table** - Created `termbase_synonyms` table structure (foundation for future feature)
- 🔄 **Legacy Support** - Old `definition` column preserved for backward compatibility

### Fixed

**Metadata Flow Issues:**
- ✅ **Complete Metadata Chain** - All termbase metadata now flows correctly: Dialog → Database → Search → Display
- ✅ **Edit Button Caching** - Fixed issue where edit buttons didn't work until adding first new term
- ✅ **Thread-Safe Queries** - Background termbase worker now includes all metadata fields (term_id, termbase_id, etc.)
- ✅ **Initial Load** - Termbase matches loaded at startup now include full metadata for immediate editing
- ✅ **Field Consistency** - Standardized on "notes" (plural) throughout codebase

**UI/UX Improvements:**
- ✅ **Visible Refresh Button** - Changed from just "🔄" to "🔄 Refresh data" for better visibility
- ✅ **Metadata Display** - Termbase viewer shows all fields with proper formatting
- ✅ **URL Rendering** - QTextBrowser with `setOpenExternalLinks(True)` for clickable links
- ✅ **Edit Dialog Fields** - Updated TermMetadataDialog to show notes, project, client (removed old definition field)

### Changed

**API Updates:**
- 🔄 **termbase_manager.add_term()** - Updated signature to accept `notes`, `project`, `client` instead of `definition`
- 🔄 **termbase_manager.get_terms()** - Now returns all new fields in term dictionaries
- 🔄 **termbase_manager.update_term()** - Updated to handle new field structure
- 🔄 **database_manager.search_termbases()** - SELECT query includes all new columns
- 🔄 **TranslationMatch metadata** - All creation points include complete metadata with IDs

**Code Quality:**
- 📦 **Modular Migrations** - `database_migrations.py` handles all schema updates
- 🔒 **Type Safety** - Proper Optional types for new fields throughout
- 🧹 **Cleanup** - Removed all references to old "definition" field (except database column for compatibility)

### Technical Details

**Database Migration:**
```sql
-- Migration adds new columns to termbase_terms
ALTER TABLE termbase_terms ADD COLUMN notes TEXT;
ALTER TABLE termbase_terms ADD COLUMN project TEXT;
ALTER TABLE termbase_terms ADD COLUMN client TEXT;

-- New synonyms table (foundation for future feature)
CREATE TABLE IF NOT EXISTS termbase_synonyms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term_id INTEGER NOT NULL,
    synonym_text TEXT NOT NULL,
    language TEXT NOT NULL,
    created_date TEXT,
    FOREIGN KEY (term_id) REFERENCES termbase_terms(id) ON DELETE CASCADE
);
```

**Metadata Flow:**
1. **Add Term**: TermMetadataDialog → get_metadata() → add_term_pair_to_termbase() → termbase_mgr.add_term() → Database INSERT
2. **Load Terms**: Database SELECT → search_termbases() → TranslationMatch metadata → Termbase viewer display
3. **Edit Term**: Edit button → TermbaseEntryEditor → update_term() → Database UPDATE → Refresh viewer
4. **Cache Population**: Background worker → _search_termbases_thread_safe() → Complete metadata → termbase_cache

---

## [1.6.0] - November 16, 2025

### 📚 Complete Termbase System with Interactive Features

**The Ultimate Terminology Management** - Full-featured termbase system rivaling commercial CAT tools with memoQ-inspired interactive features.

### Added

**Core Termbase Features:**
- 📊 **SQLite-Based Storage** - Robust database backend for termbases and terms
- 🔍 **Real-Time Term Matching** - Automatic detection of termbase matches in source segments
- 🎨 **Priority-Based Highlighting** - Terms highlighted in source cells with color intensity matching priority (1-99)
- 🎯 **Visual Match Display** - All termbase matches shown in Translation Results panel with metadata
- ⚫ **Forbidden Term Marking** - Forbidden terms highlighted in black (source cells and translation results)
- 🗂️ **Multi-Termbase Support** - Create and manage multiple termbases per project
- ✅ **Termbase Activation** - Enable/disable specific termbases for each project

**Interactive Features (memoQ-Inspired):**
- 💡 **Hover Tooltips** - Mouse over highlighted terms to see translation, priority, and forbidden status
- 🖱️ **Double-Click Insertion** - Double-click any highlighted term to insert translation at cursor
- 📝 **Dual Selection Workflow** - Select source term → Tab → select target translation → Ctrl+E to add
- 🎹 **Keyboard Shortcuts** - Ctrl+E to add term pair, right-click context menu alternative

**Termbase Management UI:**
- 📋 **Termbase List** - View all termbases with term counts and activation toggles
- ➕ **Create/Delete** - Full CRUD operations with confirmation dialogs
- ✏️ **Edit Terms Dialog** - Modify source/target terms, priority (1-99), and forbidden flag
- 🔢 **Priority Editing** - Click priority cells to edit directly in table
- 🚫 **Forbidden Toggle** - Checkbox for marking terms as forbidden (do-not-use)
- 📊 **Metadata Entry** - Add definition, domain, priority, and forbidden status when creating terms

**Technical Implementation:**
- 🗄️ **Three-Table Schema** - `termbases`, `termbase_terms`, `termbase_activation` for flexible management
- 🔍 **FTS5 Full-Text Search** - Fast term matching even with large termbases
- 💾 **Smart Caching** - Term matches cached per segment for performance
- 🔄 **Automatic Refresh** - Adding/editing terms immediately updates highlighting and results
- 🎨 **QTextCharFormat Highlighting** - Non-intrusive background color without replacing widgets
- 🖱️ **Mouse Tracking** - Enable hover detection with `setMouseTracking(True)`
- 📍 **Position Detection** - `cursorForPosition()` for finding text under mouse cursor

**Color System:**
- 🔵 **Priority Colors** - Higher priority (lower number) = darker blue, lower priority = lighter blue
- ⚫ **Forbidden Terms** - Black background (#000000) with white text for maximum visibility
- 🎨 **Consistent Rendering** - Same color scheme in source highlights and translation results

**Workflow Integration:**
- ⚡ **Fast Term Entry** - Select in source → Tab → select in target → Ctrl+E → done
- 🔄 **Immediate Visibility** - New terms appear instantly in highlights and results
- 📊 **Project-Based Activation** - Each project remembers which termbases are active
- 🎯 **Settings Toggle** - Enable/disable grid highlighting in Settings → General

### Fixed
- ✅ Language code handling - Proper conversion from language names (Dutch → nl, English → en)
- ✅ Term search issues - Fixed "unknown" language codes preventing matches
- ✅ Activation persistence - Termbase toggles now save correctly across sessions
- ✅ Priority editing - Term priority changes now persist to database
- ✅ Delete functionality - Delete button now works with confirmation dialog
- ✅ Project ID tracking - Hash-based project ID for termbase activation
- ✅ Highlight consistency - Clear formatting before re-applying to prevent accumulation
- ✅ Cache clearing - Both termbase_cache and translation_matches_cache cleared after changes

### Technical Details
**Database Schema:**
```sql
-- Termbases table
CREATE TABLE termbases (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_date TEXT,
    modified_date TEXT
)

-- Termbase terms with FTS5 search
CREATE VIRTUAL TABLE termbase_terms USING fts5(
    termbase_id UNINDEXED,
    source_term,
    target_term,
    source_lang,
    target_lang,
    definition,
    domain,
    priority UNINDEXED,
    forbidden UNINDEXED,
    created_date UNINDEXED,
    modified_date UNINDEXED
)

-- Project-specific termbase activation
CREATE TABLE termbase_activation (
    project_id TEXT NOT NULL,
    termbase_id INTEGER NOT NULL,
    is_active INTEGER DEFAULT 1,
    PRIMARY KEY (project_id, termbase_id)
)
```

**Key Classes:**
- `TermbaseManager` - Database operations and term search
- `ReadOnlyGridTextEditor` - Source cell with highlighting, tooltip, and double-click
- `TermMetadataDialog` - Modal dialog for entering term metadata
- `find_termbase_matches_in_source()` - Search engine returning match dict
- `highlight_termbase_matches()` - Visual highlighting with priority/forbidden colors

### Documentation
- Added comprehensive termbase workflow documentation
- Updated keyboard shortcuts reference
- Documented color system and priority levels
- Added tooltip and double-click feature guides

---

## [1.5.1] - November 16, 2025

### ⌨️ Source/Target Tab Cycling for Termbase Workflow

**New Feature:**
- 🔄 **Tab Key Cycling** - Press `Tab` in target cell to jump to source cell, then `Tab` again to return to target
  - Enables fast termbase workflow: select term in source, Tab to target, select translation
  - Works bidirectionally: Target → Source → Target
  - Both source and target cells support text selection with keyboard and mouse
  - Arrow keys work in both cells for cursor movement
- 🔠 **Ctrl+Tab** - Insert actual tab character when needed (in both source and target)

**Technical Implementation:**
- Source cells (`ReadOnlyGridTextEditor`) now intercept Tab at the `event()` level for reliable cycling
- Target cells (`EditableGridTextEditor`) handle Tab in `keyPressEvent()`
- Text selection enabled in source cells via `TextSelectableByKeyboard | TextSelectableByMouse` flags
- Focus policy set to `StrongFocus` on both cell types

**Workflow Benefits:**
- Facilitates termbase entry: select source term → Tab → select target translation → add to termbase
- Maintains active text selections in both cells simultaneously for termbase operations
- No need to click between cells, keyboard-only navigation

---

## [1.5.0] - November 15, 2025

### 🔍 Translation Results Enhancement + Match Insertion Shortcuts

**Major Features:**
- 🎯 **Progressive Match Loading** - Termbase, TM, MT, and LLM results now accumulate instead of replacing each other
- ⌨️ **Match Navigation Shortcuts** - `Ctrl+Up/Down` to cycle through translation matches from the grid
- 🚀 **Quick Insert Shortcuts** - `Ctrl+1-9` to instantly insert specific matches at cursor position
- ⏎ **Smart Match Insertion** - `Ctrl+Space`, `Space`, or `Enter` in results panel to insert selected match
- 🏷️ **Tag Display Control** - Optional setting to show/hide HTML/XML tags in translation results (Settings → View Settings)
- 📊 **Status Management** - Manual edits now reset segment status to "Not started" requiring explicit confirmation

**Bug Fixes:**
- ✅ Fixed translation results panel showing only the last match type (now accumulates all: termbase → TM → MT → LLM)
- ✅ Fixed `add_matches()` method not found error (implemented progressive match accumulation)
- ✅ Fixed `save_mode` parameter errors in TM saving (removed deprecated parameter)
- ✅ Fixed match insertion not working (now correctly inserts at cursor position in target cell)
- ✅ Fixed `scroll_area` AttributeError (corrected to `matches_scroll`)

**Keyboard Shortcuts Added:**
- `Ctrl+Up` - Navigate to previous match in results panel
- `Ctrl+Down` - Navigate to next match in results panel
- `Ctrl+1` through `Ctrl+9` - Insert match #1-9 at cursor position
- `Ctrl+Space` - Insert currently selected match
- `Space` or `Enter` - Insert selected match (when focused on results panel)

**Documentation:**
- Updated shortcut manager with complete match navigation and insertion shortcuts
- Added comprehensive shortcut documentation in Settings → Shortcuts section

**Technical Improvements:**
- Implemented `add_matches()` method for progressive match accumulation
- Added `insert_match_by_number()` for direct match insertion by number
- Added `insert_selected_match()` for keyboard-driven match insertion
- Improved `on_match_inserted()` to insert at cursor position using `textCursor().insertText()`
- Added tag formatting control with `show_tags` class variable and `_format_text()` method

---

## [1.4.0] - November 12, 2025

### 🎤 Major Feature: Supervoice Voice Dictation + Detachable Log Window

**AI-Powered Hands-Free Translation Input** - OpenAI Whisper voice dictation with 100+ language support, plus multi-monitor log window capability.

### Added
- **🎤 Supervoice Voice Dictation Module**
  - AI-powered speech recognition using OpenAI Whisper
  - Support for 100+ languages (as many as Whisper can handle)
  - Press-to-start, press-to-stop recording with F9 global hotkey
  - 5 model sizes: tiny, base, small, medium, large (balance speed vs accuracy)
  - Configurable in Settings → 🎤 Supervoice
  - Automatic FFmpeg detection and bundling support
  - User-friendly error messages with installation instructions
  - Visual feedback: button color changes during recording
  - Seamless integration with segment editor and grid cells
  - Language auto-detection from project settings
  - Manual stop functionality (press F9 again to stop recording)
  - Future: Planned parallel dictation system for voice commands (confirm segment, go to top, filtering, workflow automation)

- **🪟 Detachable Log Window**
  - Log window can be detached into separate floating window
  - Perfect for multi-monitor setups
  - Synchronized auto-scroll between main and detached logs
  - "Detach Log" / "Attach Log" button in Settings
  - Remembers detached state across sessions
  - Independent positioning and sizing

- **📚 Comprehensive Documentation**
  - [VOICE_DICTATION_GUIDE.md](docs/VOICE_DICTATION_GUIDE.md) - Complete user guide
  - [VOICE_DICTATION_DEPLOYMENT.md](docs/VOICE_DICTATION_DEPLOYMENT.md) - Deployment options
  - [SUPERVOICE_TROUBLESHOOTING.md](docs/SUPERVOICE_TROUBLESHOOTING.md) - Troubleshooting guide
  - FFmpeg licensing information
  - Model selection recommendations
  - Corrupt model file recovery instructions

### Fixed
- **🐛 Voice Dictation Bug Fixes**
  - Fixed critical UnboundLocalError in `voice_dictation_lite.py:118` (duplicate `import os` statement)
  - Fixed language detection from project settings
  - Fixed button color restoration after recording
  - Fixed auto-scroll synchronization between log windows

### Changed
- **🔧 Version Update**
  - Updated version from 1.3.4 to 1.4.0
  - Updated all version strings in code and documentation
  - Updated window titles and welcome messages
  - Updated website (docs/index.html) with Supervoice module card
  - Updated hero badge to "v1.4.0 - Supervoice Voice Dictation"

### Technical
- New module: `modules/voice_dictation_lite.py` - Core dictation engine
- Enhanced `Supervertaler_Qt.py` - Integrated voice dictation and detachable log
- Updated `docs/index.html` - Added Supervoice feature highlight and module card
- Created FFmpeg detection and bundling infrastructure
- Whisper model caching in `%USERPROFILE%\.cache\whisper\`

---

## [1.3.3] - November 10, 2025

### 🏆 Major Feature: LLM Leaderboard + UI Standardization

**Translation Quality Benchmarking System** - Compare translation quality, speed, and cost across multiple LLM providers in a professional, standardized interface.

### Added
- **🏆 LLM Leaderboard Module** (Complete Implementation)
  - Benchmark translation quality across OpenAI, Claude, and Gemini models
  - chrF++ quality scoring for objective translation assessment
  - Speed and cost tracking for each translation
  - Multiple test datasets: Technical, Legal, Medical, Marketing (EN→NL, NL→EN)
  - Comprehensive Excel export with:
    - About sheet with clickable Supervertaler.com link
    - Summary sheet with rankings and statistics
    - Detailed results with all metrics
    - Dataset info in filename (e.g., `LLM_Leaderboard_Technical_EN-NL_20251110.xlsx`)
  - Auto-scrolling log for real-time progress monitoring
  - Standalone usage support with api_keys.example.txt template
  - Professional documentation in `modules/LLM_LEADERBOARD_STANDALONE.md`

- **🎨 Standardized Module Headers**
  - Consistent professional styling across all modules
  - Blue header color (#1976D2) matching Supervertaler branding
  - Light blue description boxes (#E3F2FD) with rounded corners
  - Trophy emoji 🏆 for LLM Leaderboard identity
  - Applied to: LLM Leaderboard, TMX Editor, AutoFingers, PDF Rescue

- **📊 Model Selection Enhancements**
  - Friendly model names in dropdowns (e.g., "GPT-5 (Reasoning)", "Claude Opus 4.1")
  - Support for latest models:
    - OpenAI: GPT-4o, GPT-4o Mini, GPT-5
    - Claude: Sonnet 4.5, Haiku 4.5, Opus 4.1
    - Gemini: 2.5 Flash, 2.5 Flash Lite, 2.5 Pro, 2.0 Flash (Exp)

### Fixed
- **🐛 LLM Leaderboard Bug Fixes**
  - Fixed Claude API call parameters (text vs custom_prompt)
  - Fixed Gemini API key mapping ("gemini" provider → "google" API key)
  - Fixed model dropdown display names (was showing generic names instead of selected models)
  - Fixed API key auto-creation from template file

### Changed
- **🔧 Excel Export Branding**
  - Title sheet matches UI header style with trophy emoji
  - Blue title color (#1976D2) for brand consistency
  - Clickable hyperlink to https://supervertaler.com/
  - Professional subtitle formatting

- **🔧 API Key Management**
  - Auto-creates `api_keys.txt` from `api_keys.example.txt` on first run
  - Supports standalone LLM Leaderboard usage outside Supervertaler

### Technical
- Enhanced `modules/llm_leaderboard.py` - Core benchmarking engine
- Enhanced `modules/superbench_ui.py` - Qt UI with standardized header
- Updated `modules/llm_clients.py` - Auto-create API keys functionality
- Updated `Supervertaler_Qt.py` - Gemini API key mapping fix
- Created `api_keys.example.txt` - Template for standalone usage
- Created `modules/LLM_LEADERBOARD_STANDALONE.md` - Complete documentation

---

## [1.3.2] - November 9, 2025

### 🎯 Major Feature: Segment-Level AI Access + Critical Bug Fix

**AI Assistant can now access and query individual segments from your translation project**

### Added
- **🔢 Segment-Level AI Actions** (Phase 2 Enhancement)
  - `get_segment_count` - Get total segments and translation progress
  - `get_segment_info` - Query specific segments by ID, multiple IDs, or range
  - AI can answer "How many segments?" and "What is segment 5?"
  - First 10 segments automatically included in AI context
  - Full segment properties: id, source, target, status, type, notes, match_percent, etc.

- **📊 Segment Information Display**
  - AI Assistant shows segment details in formatted chat bubbles
  - HTML entity escaping for CAT tool tags (`<tag>`, `&nbsp;`, etc.)
  - Proper handling of Trados, memoQ, Wordfast, CafeTran tags
  - Segments displayed in code blocks for readability

- **⚙️ Auto-Markdown Generation Setting**
  - Optional setting in Settings → General → AI Assistant Settings
  - "Auto-generate markdown for imported documents" checkbox
  - Automatically converts DOCX/PDF to markdown on import
  - Markdown saved to `user_data_private/AI_Assistant/current_document/`
  - Includes metadata JSON with conversion info

### Fixed
- **🐛 CRITICAL: Current Document Not Showing After Import**
  - Fixed attribute name mismatch: `self.prompt_manager` → `self.prompt_manager_qt`
  - Current document now appears in AI Assistant sidebar after import
  - Auto-markdown generation now triggers correctly
  - Context refresh now works properly

### Changed
- **🔧 AI Assistant Context Building** (`modules/unified_prompt_manager_qt.py`)
  - Added `_get_segment_info()` method for structured segment data
  - Added `generate_markdown_for_current_document()` public method
  - Modified context building to prioritize segment-level access
  - Document content fallback when segments unavailable

- **🔧 AI Actions System** (`modules/ai_actions.py`)
  - Added `parent_app` parameter to constructor
  - Added segment action handlers with full validation
  - Enhanced `format_action_results()` with segment display logic
  - Comprehensive HTML entity escaping (order-aware to prevent double-escaping)

- **🔧 Main Application** (`Supervertaler_Qt.py`)
  - Added auto-markdown setting to Settings UI
  - Setting persists in `ui_preferences.json`
  - Document import triggers markdown generation when enabled
  - Context refresh called after document import

### Technical
- **Segment Access Order:**
  1. `project.segments` - Full segment objects (PREFERRED)
  2. `parent_app.segments` - Currently loaded segments
  3. `project.source_segments` - Project source text
  4. Cached markdown conversion
  5. On-demand file conversion with markitdown

- **HTML Escaping Order:** `&` → `<` → `>` → `"` (prevents double-escaping)
- **Segment Data Structure:** Full dataclass with 12 properties per segment

### Testing
- ✅ Updated test suite (`test_ai_actions.py`)
- ✅ Added Test 9: get_segment_count action
- ✅ Added Test 10: get_segment_info action (single, multiple, range)
- ✅ All 10 tests passing

### Documentation
- Updated `docs/AI_ASSISTANT_INTEGRATION.md` with segment access details
- Added segment action examples and use cases
- Updated troubleshooting section

### Benefits
- ✅ **Segment-specific queries** - AI can find and analyze specific segments
- ✅ **Translation progress tracking** - AI reports completion status
- ✅ **CAT tool tag handling** - All tag types properly escaped and displayed
- ✅ **Auto-markdown option** - Users control document conversion
- ✅ **Fixed critical bug** - Current document now shows correctly

---

## [1.3.1] - November 9, 2025

### ✨ Major Feature: AI Assistant File Attachment Persistence (Phase 1)

**Complete persistent storage system for AI Assistant file attachments with view/manage UI**

### Added
- **📎 AttachmentManager Module** (`modules/ai_attachment_manager.py` - 390 lines)
  - Complete persistent storage system for attached files
  - Session-based organization (files grouped by date)
  - Master index tracking all attachments across sessions
  - Metadata storage with JSON (original name, path, type, size, date)
  - Full CRUD operations: attach, get, list, remove files
  - Statistics tracking (total files, size, sessions)

- **👁️ File Viewer Dialogs** (`modules/ai_file_viewer_dialog.py` - 160 lines)
  - FileViewerDialog - displays file content with metadata
  - Read-only markdown preview with monospace font
  - Copy to clipboard functionality
  - FileRemoveConfirmDialog - confirmation before deletion

- **🎨 Expandable Attached Files Panel** (AI Assistant context sidebar)
  - Collapsible "📎 Attached Files" section with expand/collapse button (▼/▶)
  - Dynamic file list showing name, type, size for each file
  - View button (👁) - opens file viewer dialog
  - Remove button (❌) - deletes from disk with confirmation
  - + button to attach new files
  - Auto-refresh on file operations

### Changed
- **🔧 AI Assistant Integration** (`modules/unified_prompt_manager_qt.py`)
  - Initialized AttachmentManager in `__init__`
  - Modified `_attach_file()` to save files to persistent storage
  - Added `_load_persisted_attachments()` method - loads files on startup
  - Created `_create_attached_files_section()` - expandable panel UI
  - Added `_refresh_attached_files_list()` - dynamic file list updates
  - Added `_create_file_item_widget()` - individual file items with buttons
  - Added `_view_file()` - opens FileViewerDialog
  - Added `_remove_file()` - removes from disk and memory
  - Added `_toggle_attached_files()` - expand/collapse functionality
  - Updated `_update_context_sidebar()` to refresh file list
  - Updated `_load_conversation_history()` to refresh UI after load

### Technical
- **Storage Structure:**
  - Base: `user_data_private/AI_Assistant/`
  - Attachments: `attachments/{session_id}/{file_hash}.md`
  - Metadata: `attachments/{session_id}/{file_hash}.meta.json`
  - Master index: `index.json`
- **Session Management:** Date-based sessions (YYYYMMDD format)
- **File Hashing:** SHA256-based unique IDs (path_hash + content_hash)
- **Backward Compatibility:** Old `self.attached_files` list still maintained

### Testing
- ✅ Created comprehensive test suite (`test_attachment_manager.py`)
- ✅ All 8 tests passing (imports, init, session, attach, list, get, stats, remove)
- ✅ UTF-8 console output handling for Windows

### Benefits
- ✅ **Files no longer lost** when application closes
- ✅ **Users can view** attached files anytime via viewer dialog
- ✅ **Users can remove** unwanted files with confirmation
- ✅ **Session organization** keeps files organized by date
- ✅ **Persistent across app restarts** - automatic reload on startup

### Documentation
- Updated `docs/PROJECT_CONTEXT.md` with Phase 1 implementation details
- Created `docs/AI_ASSISTANT_ENHANCEMENT_PLAN.md` with full specification
- Updated website (`docs/index.html`) to reflect new features

### Next
- Phase 2: AI Actions System (allow AI to create/modify prompts in library)

---

## [1.2.2] - November 6, 2025

### 🎨 Major Enhancement: Translation Results, Document Formatting & Tag System

**Fixed translation results display, enhanced document view with formatting, and activated the tag system!**

### Fixed
- **🐛 Translation Results Panels Not Working** - CRITICAL FIX
  - Removed lingering `assistance_widget` references that blocked match processing
  - Fixed termbase, TM, MT, and LLM matches not displaying in panels
  - Updated all 6 locations where matches were being set to use `results_panels`
  - All three views (Grid, List, Document) now show matches correctly

- **🐛 Menu Bar Blocked by Error Indicator** 
  - Removed 15+ obsolete `assistance_widget` references causing Qt errors
  - Fixed red error triangle that blocked File and Edit menus
  - Updated zoom functions, font settings, and close project cleanup

### Added
- **✅ Document View Formatting**
  - Renders inline formatting tags: `<b>bold</b>`, `<i>italic</i>`, `<u>underline</u>`, `<bi>bold+italic</bi>`
  - New list item tag: `<li>content</li>` renders with orange bullet (•)
  - Proper QTextCharFormat application for bold, italic, underline
  - Tag parsing with formatting stack for nested tags

- **✅ Enhanced Type Column**
  - Shows **H1, H2, H3, H4** for heading levels (blue background)
  - Shows **Title** for document titles
  - Shows **Sub** for subtitles
  - Shows **li** for list items (green background)
  - Shows **¶** for regular paragraphs
  - Color-coded for easy document structure visualization

- **✅ List Item Tag System**
  - DOCX import detects bullets and numbered lists
  - Automatically wraps list items in `<li>` tags
  - Detection works on Word numbering format, bullet characters, and numbered prefixes
  - Tags preserved through translation and export workflow

### Technical
- Updated `tag_manager.py` to support `<li>` tag (TAG_PATTERN regex)
- Enhanced `docx_handler.py` to detect and tag list items during import
- Document view parses tags and renders with proper formatting
- Type column detects `<li>` tags, heading styles, and text patterns
- Tag colors: Bold=#CC0000, Italic=#0066CC, Underline=#009900, BoldItalic=#CC00CC, ListItem=#FF6600

---

## [1.2.1] - November 6, 2025

### 🎨 UI Enhancement: Unified Tabbed Interface

**Added consistent tabbed panel structure to both Grid and List views for improved workflow!**

### Added
- **✅ Tabbed Panel in Grid View**
  - Tab 1: Translation Results (TM, MT, LLM, Termbase matches)
  - Tab 2: Segment Editor (source/target editing, status selector)
  - Tab 3: Notes (segment notes with save functionality)
  - Enables segment editing directly in Grid View (like Tkinter edition)

- **✅ Tabbed Panel in List View**
  - Same 3-tab structure as Grid View for consistency
  - Translation Results | Segment Editor | Notes
  - Replaces single-panel layout with flexible tabbed interface

- **✅ Synchronized Panel Updates**
  - Clicking segment in any view updates ALL tabs in ALL views
  - Editing in any panel automatically syncs to other panels
  - Prevents infinite loops with signal blocking
  - Multiple independent widget instances for Grid/List views

### Fixed
- **🐛 Widget Parenting Issues** - Fixed Qt single-parent constraint violations
  - Created separate TranslationResultsPanel instances for each view
  - Stored widget references on panel objects for flexible access
  - Maintains `results_panels` and `tabbed_panels` lists for batch updates

- **🐛 Signal Handler Crashes** - Fixed AttributeError when editing segments
  - Updated `on_tab_target_change()`, `on_tab_segment_status_change()`, `on_tab_notes_change()`
  - Handlers now iterate all panels instead of accessing non-existent attributes
  - Proper error handling per panel to prevent cascade failures

### Technical
- Unified panel creation via `create_tabbed_assistance_panel()`
- Widget reference storage pattern: `panel.editor_widget.source_editor`
- Centralized update function: `update_tab_segment_editor()` iterates all panels
- Signal blocking prevents infinite update loops during synchronization

---

## [1.2.0] - November 6, 2025 🎉

### 🎯 MAJOR RELEASE: Complete Translation Matching System

**The Supervertaler CAT tool now provides comprehensive translation assistance with all match types working together!**

### Added
- **✅ Google Cloud Translation API Integration**
  - Machine translation matches displayed alongside TM and LLM results
  - Uses Google Translate REST API v2 for direct API key authentication
  - Automatic language detection support
  - High-quality neural machine translation
  - Provider badge: "MT" in match display

- **✅ Multi-LLM Support (OpenAI, Claude, Gemini)**
  - **OpenAI GPT** integration (GPT-4o, GPT-5, o1, o3)
  - **Claude 3.5 Sonnet** integration (Anthropic)
  - **Google Gemini** integration (Gemini 2.0 Flash, 1.5 Pro)
  - All three LLM providers work simultaneously
  - Each provides translations with confidence scores
  - Provider badges: "OA" (OpenAI), "CL" (Claude), "GM" (Gemini)

- **✅ Complete Match Chaining System**
  - **Termbase matches** → Displayed immediately (yellow highlight)
  - **TM matches** → Displayed after 1.5s delay (prevents excessive API calls)
  - **MT matches** → Google Translate integrated in delayed search
  - **LLM matches** → All enabled LLMs called in parallel
  - All match types preserved and displayed together in Translation Results Panel

- **✅ Flexible API Key Management**
  - Supports both `google` and `google_translate` key names for Google Cloud Translation
  - Supports both `gemini` and `google` key names for Gemini API
  - Backward compatibility with existing configurations
  - Standalone `load_api_keys()` function in `modules/llm_clients.py`

### Fixed
- **🐛 Termbase Match Preservation** - Termbase matches no longer disappear when TM/MT/LLM results load
  - Root cause: Delayed search wasn't receiving termbase matches parameter
  - Solution: Pass `current_termbase_matches` to `_add_mt_and_llm_matches()`
  - Termbase matches now persist throughout the entire search process

- **🐛 Google Translate Authentication** - Fixed "Client.__init__() got an unexpected keyword argument 'api_key'"
  - Switched from google-cloud-translate SDK to direct REST API calls
  - Simpler authentication using API key in URL parameters
  - More reliable and easier to configure

- **🐛 Gemini Integration** - Gemini now properly called when using `google` API key
  - Added fallback to check both `gemini` and `google` key names
  - Fixed LLM wrapper to support Google's API key for Gemini

### Technical Implementation
- **File: `modules/llm_clients.py`**
  - Added standalone `load_api_keys()` function (lines 27-76)
  - Fixed `get_google_translation()` to use REST API instead of SDK
  - Backward compatible API key naming (checks multiple key names)
  - Module can now operate independently without main application

- **File: `Supervertaler_Qt.py`**
  - Enhanced `_add_mt_and_llm_matches()` with comprehensive logging
  - Fixed Gemini integration to check both key naming conventions
  - Improved match chaining with proper termbase preservation
  - Debounced search (1.5s delay) prevents excessive API calls

### Performance Optimizations
- **Debounced Search** - 1.5-second delay before calling TM/MT/LLM APIs
- **Timer Cancellation** - Previous searches cancelled when user moves to new segment
- **Immediate Termbase Display** - Termbase matches shown instantly (no delay)
- **Parallel LLM Calls** - All LLM providers called simultaneously for faster results

### Dependencies
- `requests` - For Google Translate REST API calls (standard library)
- `openai` - OpenAI GPT integration
- `anthropic` - Claude integration
- `google-generativeai` - Gemini integration
- `httpx==0.28.1` - HTTP client (version locked for LLM compatibility)

### Documentation
- Updated `docs/PROJECT_CONTEXT.md` with November 6, 2025 development activity
- Documented all LLM & MT integration details
- Listed resolved issues and technical decisions

### Match Display
All match types now display in the Translation Results Panel:
- **Termbases** (Yellow section) - Term matches from termbase databases
- **Translation Memory** (Blue section) - Fuzzy matches from TM database
- **Machine Translation** (Orange section) - Google Cloud Translation
- **LLM** (Purple section) - OpenAI GPT, Claude, and/or Gemini translations

Each match shows:
- Provider badge (NT/TM/MT/OA/CL/GM)
- Relevance percentage (0-100%)
- Target translation text
- Source context (when available)

---

## [1.1.9] - November 6, 2025

### Added
- **⌨️ Keyboard Shortcuts Manager** - Comprehensive keyboard shortcuts management system
  - New Settings tab: "⌨️ Keyboard Shortcuts"
  - View all 40+ keyboard shortcuts organized by category (File, Edit, Translation, View, Resources, Match Insertion, etc.)
  - Search/filter shortcuts by action, category, or key combination
  - Edit shortcuts with custom key capture widget
  - Conflict detection with warnings
  - Reset individual shortcuts or all shortcuts to defaults
  - Export shortcuts to JSON (share with team)
  - Import shortcuts from JSON
  - **Export HTML Cheatsheet** - Beautiful, printable keyboard reference with professional styling
  - Modular architecture: `modules/shortcut_manager.py` and `modules/keyboard_shortcuts_widget.py`

### Technical Details
- **ShortcutManager** class - Backend logic for managing shortcuts
- **KeyboardShortcutsWidget** - Full-featured UI for Settings tab
- **KeySequenceEdit** - Custom widget for capturing key presses
- **Conflict detection** - Real-time warnings for duplicate shortcuts
- **Context-aware shortcuts** - Different contexts (editor, grid, match panel) to prevent conflicts
- Data stored in `user_data/shortcuts.json`

### Documentation
- Added `Keyboard_Shortcuts_Implementation.md` in development docs
- Added `Competitive_Analysis_CotranslatorAI.md` in development docs

### Improved
- **Repository Philosophy** - Continued modular architecture to keep main file maintainable
- **AI-Friendly Codebase** - Complex features extracted to focused modules (easier for AI agents to understand)

---

## [1.1.8] - November 5, 2025

### Fixed
- **🎯 Prompt Generation (CRITICAL FIX):** Fixed incomplete prompt generation in Prompt Assistant
  - **Root Cause:** Using `client.translate()` for text generation instead of proper chat completion API
  - **Solution:** Switched to direct LLM API calls (OpenAI/Claude/Gemini) with proper message structure
  - Domain Prompts now generate complete 3-5 paragraph prompts (was 2 sentences)
  - Project Prompts now include full termbase tables + intro/closing paragraphs (was partial/truncated)
  - Added truncation detection and warnings for all providers
  - Temperature set to 0.4 for creative generation (was 0.3)
  - Max tokens set to 8000 (with full flexibility, not constrained by translation wrapper)
- **Documentation:** Added complete debugging session documentation (docs/2025-11-05.md)

### Technical Details
- Removed hybrid approach (programmatic termbase extraction + AI generation)
- Reverted to pure AI-only approach matching working tkinter version
- Direct API calls now match tkinter implementation exactly:
  - OpenAI: `chat.completions.create()` with system/user messages
  - Claude: `messages.create()` with proper system parameter
  - Gemini: `generate_content()` with combined prompt
- All providers now check `finish_reason`/`stop_reason` for truncation

### Impact
- **Generate Prompts** feature now works perfectly, producing complete professional prompts
- Critical feature that was broken is now fully functional
- Matches quality and completeness of tkinter version

---

## [1.1.7] - November 4, 2025

### Major Changes
- **🏠 Home Screen Redesign:** Complete restructuring of the primary workspace
  - Editor (Grid/List/Document views) on the left with Prompt Manager on the right
  - Resizable horizontal splitter between editor and prompt manager
  - Translation results panel moved to bottom of grid in compact form
  - Real-time prompt tweaking while viewing changes in the grid
  - Removed separate Editor and Prompt Manager tabs (integrated into Home)

### Strategic Refocus
- **🎯 Companion Tool Philosophy:** Pivoted from full CAT tool to companion tool
  - Grid simplified for viewing/reviewing (minor edits only)
  - Focus on AI-powered features and specialized modules
  - Documentation updated to reflect companion tool approach

### Added
- **Custom Styled Widgets:** Beautiful checkboxes and radio buttons with white checkmarks
  - `CheckmarkCheckBox` class for all checkboxes
  - `CustomRadioButton` class for LLM Provider selection
  - Square indicators with green background when checked, white checkmark overlay
- **Prompt Manager Enhancements:**
  - Preview Combined Prompt button shows exact prompt sent to AI
  - Deactivate buttons for Domain and Project prompts
  - Prompt Assistant tab moved to first position

### Improved
- **Grid Simplification:**
  - Double-click only editing (removed F2 key) - companion tool philosophy
  - Simplified styling with subtle colors for review-focused interface
  - Light blue selection highlight instead of bright blue
- **Segment Number Styling:**
  - All segment numbers start with black foreground
  - Only selected segment number highlighted in orange (like memoQ)
  - Fixed black numbers issue after navigation

### Fixed
- **Filter Crash:** Added safety checks for table and filter widgets
- **removeWidget Error:** Fixed QSplitter widget removal (use setParent instead)
- **Project Loading:** Fixed doc_segment_widgets AttributeError
- **Translation Results Panel:** Now properly visible at bottom of grid

### Technical
- Improved widget reparenting logic for splitter management
- Enhanced error handling in filter operations
- Better initialization of view state variables

---

## [1.1.6] - November 3, 2025

### Added
- **🔍 Detachable Superlookup:** Multi-screen support for Superlookup module
  - Detach button on Home tab to open Superlookup in separate window
  - Perfect for multi-monitor workflows - move lookup to second screen while translating
  - Proper window positioning and multi-monitor detection
  - Reattach functionality to return to embedded mode

### Improved
- **🏠 Home Tab Enhancements:**
  - Integrated About section directly into header with improved visibility
  - Better text styling with purple gradient for subtitle and version (larger, bold)
  - Reorganized layout: About in header, Resources & Support next, Projects at bottom
  - Projects section with distinct background color for visual separation
  - Superlookup prominently featured on right side of Home tab

### Fixed
- **Multi-Monitor Support:** Fixed window positioning for detached Superlookup
  - Correct screen detection using `QApplication.screenAt()` API
  - Proper window activation and focus handling
  - Window flags configured for proper minimize/maximize behavior
  - Improved error handling for window detachment process

### Technical
- Updated window positioning logic for Qt6 compatibility
- Enhanced screen detection for multi-monitor setups
- Improved window activation using QTimer for reliable focus management

---

## [1.1.5] - November 2, 2025

### Added
- **🏠 New Home Tab:** Brand new first-screen experience
  - Integrated About section with version info and purple gradient header
  - Quick access to resources (Website, GitHub, Discussions, Documentation)
  - Project management panel for recent projects
  - Embedded Superlookup for instant translations
  - Clean, modern design with proper visual hierarchy
  
- **Major UI Reorganization:** Complete restructuring of main interface
  - **Tab Order Redesigned:** 
    1. 🏠 Home (NEW - welcome screen)
    2. 💡 Prompt Manager (moved up from #5)
    3. 📝 Editor (renamed from "Project Editor")
    4. 🗂️ Resources (organized nested tabs)
    5. 🧩 Modules (renamed from "Specialised Modules")
    6. ⚙️ Settings (moved from Tools menu, includes Log)
  - **Navigation Menu:** Added "Go to Home" action (🏠 Home menu item)
  - **Removed Quick Access Sidebar:** Functionality integrated into Home tab
  - Cleaner, more intuitive workflow with logical feature grouping

- **Multiple View Modes:** Three different ways to view and edit your translation project
  - **Grid View (Ctrl+1):** Spreadsheet-like table view - perfect for quick segment-by-segment editing
  - **List View (Ctrl+2):** Segment list on left, editor panel on right - ideal for focused translation work
  - **Document View (Ctrl+3):** Natural document flow with clickable segments - great for review and context
  - View switcher toolbar with quick access buttons
  - All views share the same translation results pane (TM, LLM, MT, Termbase matches)
  - All views stay synchronized - changes in one view instantly reflected in others
  - Keyboard shortcuts (Ctrl+1/2/3) for rapid view switching

### Improved
- **Translation Results Pane:** Now visible and functional in all three view modes
  - Properly integrated into Grid, List, and Document views
  - Dynamic reparenting when switching between views
  - Consistent assistance panel across all view modes

### Technical
- **View Management:** Implemented QStackedWidget architecture for seamless view switching
  - Each view maintains its own splitter layout
  - Shared assistance widget dynamically moved between views
  - Clean separation of view-specific logic

---

## [1.1.4] - November 2, 2025

### Added
- **Encoding Repair Tool:** Full port from tkinter edition with standalone capability
  - Detect and fix text encoding corruption (mojibake) in translation files
  - Scan single files or entire folders recursively
  - Automatic backup creation (.backup files) before repair
  - Supports common corruption patterns (en/em dashes, quotes, ellipsis, bullets, etc.)
  - Clean Qt interface matching other modules (PDF Rescue, TMX Editor style)
  - **Standalone Mode:** Run independently with `python modules/encoding_repair_Qt.py`
  - **Embedded Mode:** Integrated as a tab in Supervertaler Qt
  - Test file available at `docs/tests/test_encoding_corruption.txt` for user testing

### Improved
- **Prompt Manager:** Fixed System Prompts tab to show list widget (matching Domain Prompts layout)
  - Added proper list/editor splitter layout for consistency
  - System Prompts now use shared editor panel with metadata fields hidden
  - Better visual consistency across all prompt tabs

### Fixed
- **About Dialog:** Updated with clickable website link (https://supervertaler.com/)
  - Changed description from "Professional Translation Memory & CAT Tool" to "AI-powered tool for translators & writers"
  - Improved dialog layout with better formatting

### Technical
- **Module Architecture:** Created `encoding_repair_Qt.py` as standalone, reusable module
  - Uses existing `encoding_repair.py` backend (shared with tkinter version)
  - Proper path handling for standalone execution
  - Consistent with other Qt modules (PDF Rescue, TMX Editor patterns)

---

## [1.1.3] - November 2, 2025

### Added
- **Prompt Manager:** Complete 4-Layer Prompt Architecture system integrated into Qt Edition
  - **Layer 1 - System Prompts:** Editable infrastructure prompts (CAT tags, formatting rules, language conventions)
  - **Layer 2 - Domain Prompts:** Domain-specific translation expertise (Legal, Medical, Technical, Financial, etc.)
  - **Layer 3 - Project Prompts:** Client and project-specific instructions and rules
  - **Layer 4 - Style Guides:** Language-specific formatting guidelines (numbers, dates, typography)
  - **Prompt Assistant:** AI-powered prompt refinement using natural language (unique to Supervertaler!)
  - **Full UI Integration:** Beautiful tab interface with activation system and preview
  - **Standardized Headers:** Consistent UI/UX matching other modules (TMX Editor, PDF Rescue, AutoFingers)
  - **Import/Export:** Save, reset, import, and export prompts for sharing and backup

### Website
- **4-Layer Architecture Documentation:** Comprehensive new section on website explaining the unique approach
- **Visual Design:** Color-coded layer cards with detailed explanations
- **Navigation:** Added dedicated navigation link for Architecture section
- **Hero Section:** Updated badges and feature highlights to showcase new architecture
- **Footer Links:** Integrated architecture documentation into site navigation

### Technical
- **Terminology Standardization:** Renamed all infrastructure/Custom Instructions references to System/Project Prompts
- **Code Quality:** Systematic refactoring with consistent naming conventions throughout
- **Module Architecture:** `prompt_manager_qt.py` created as standalone, reusable module
- **Backward Compatibility:** Maintained compatibility with existing prompt library files

---

## [1.1.2] - November 1, 2025

### Improved
- **PDF Rescue:** Simplified to OCR-only mode (removed dual-mode complexity)
  - Removed text extraction mode and 504 lines of complex layout detection code
  - Reverted to simple, reliable image-based OCR workflow
  - Updated UI description to clarify OCR-only purpose
  - Better results with simpler approach

### Fixed
- **PDF Rescue Prompt:** Restored original concise prompt that produced better OCR results
  - Removed verbose "CRITICAL ACCURACY RULES" that degraded performance
  - Simplified instructions for clearer AI guidance
  - Improved OCR accuracy with focused prompts

- **PDF Rescue DOCX Export:** Fixed excessive line breaks in Word documents
  - Changed paragraph detection from single newlines to double newlines
  - Single newlines now treated as spaces within paragraphs
  - Reduced paragraph spacing from 12pt to 6pt for tighter layout
  - Applied fix to both formatted and non-formatted export modes

### Added
- **PDF Rescue Branding:** Added clickable hyperlink in DOCX exports
  - "Supervertaler" text now links to https://supervertaler.com/
  - Professional branding with working hyperlinks in Word documents

- **Website Navigation:** Added "Modules" link to header navigation
  - Appears after "Features" in main menu
  - Provides direct access to modules documentation

### Removed
- **Website:** Removed "AI-First Philosophy" section (93 lines)
  - Streamlined website content
  - Removed from navigation menu
  - Content deemed redundant with other sections

---

## [1.1.1] - November 1, 2025

### Improved
- **AutoFingers Settings:** Simplified behavior settings by removing redundant "Use Alt+N" checkbox
  - Now uses single "Confirm segments" checkbox: checked = Ctrl+Enter (confirm), unchecked = Alt+N (skip confirmation)
  - More intuitive UI with clearer label and comprehensive tooltip
  - Maintains backward compatibility with existing settings files

---

## [1.1.0] - November 1, 2025

### Added
- **TMX Editor:** Professional translation memory editor integrated into Qt Edition
  - **Database-Backed TMX System:** Handle massive TMX files (1GB+) with SQLite backend
  - **Dual Loading Modes:** Choose RAM mode (fast for small files) or Database mode (handles any size)
  - **Smart Mode Selection:** Auto mode intelligently selects best loading method based on file size
  - **Inline Editing:** Edit source and target text directly in the grid (no popup dialogs)
  - **Real-time Highlighting:** Search terms highlighted with green background (Heartsome-style)
  - **Heartsome-Inspired UI:** Three-panel layout with top header (language selectors + filters), center grid, and right attributes panel
  - **Filtering:** Advanced search with case-insensitive matching and tag filtering
  - **Pagination:** Efficient 50 TUs per page for smooth performance
  - **Export/Import:** Save edited TMX files and export to new files
  - **Progress Indicators:** Clear progress bars with batch operations for fast loading
  - **Custom Checkboxes:** Consistent green checkmark style matching AutoFingers design

### Improved
- **Database Integration:** New TMX database tables (`tmx_files`, `tmx_translation_units`, `tmx_segments`) with foreign keys and indexes
- **Batch Operations:** Database commits every 100 TUs for 10-50x faster loading performance
- **UI Consistency:** Mode selection dialog uses custom CheckmarkCheckBox style throughout
- **Progress Feedback:** Immediate progress bar display with clearer blue styling

### Technical
- **Database Schema:** Added three new tables for TMX storage with proper indexing
- **Mode Detection:** Automatic recommendation based on file size thresholds (50MB, 100MB)
- **Transaction Management:** Optimized database operations with batch commits
- **Memory Efficiency:** Database mode frees RAM immediately after loading

---

## [1.0.2] - October 31, 2025

### Fixed
- **Broken Emoji Icons:** Fixed broken emoji characters in tab labels for Termbases (🏷️), Prompt Manager (💡), Encoding Repair (🔧), and Tracked Changes (🔄)
- **Checkbox Rendering:** Improved checkmark visibility on small displays with better padding and scaling

### Added
- **Startup Settings:** Added option to automatically restore last opened project on startup (Tools → Options → General → Startup Settings)
- **Font Size Persistence:** Added font size settings panel (Tools → Options → View/Display Settings) to save and restore:
  - Grid font size (7-72 pt)
  - Match list font size (7-16 pt)
  - Compare boxes font size (7-14 pt)
- **Auto-Save Font Sizes:** Font sizes are automatically saved when adjusted via zoom controls (Ctrl++/Ctrl+- for grid, Ctrl+Shift++/Ctrl+Shift+- for results pane)

### Improved
- **Checkbox Styling:** Implemented custom green checkboxes with white checkmarks (Option 1 style) for AutoFingers Behavior section - more intuitive than previous blue/white design
- **AutoFingers Layout:** Reorganized Settings section into 2-column grid layout (Languages/Timing on left, Behavior/Save on right) for better organization
- **Small Screen Support:** Moved Activity Log to right side of Settings for improved space utilization on laptop displays

---

## [1.0.1] - October 29, 2025

### Fixed
- **Terminology Standardization:** Replaced all "glossary" references with "termbase" throughout codebase
- **Database Schema:** Fixed NOT NULL constraint errors on `termbase_terms.source_lang` and `termbase_terms.target_lang` (changed to `DEFAULT 'unknown'`)
- **Method Naming:** Renamed `create_glossary_results_tab()` → `create_termbase_results_tab()`
- **Project Object Access:** Fixed Project attribute access patterns (changed from dict `.get()` to object attribute `.id`)
- **Tab Label:** Updated from "Term Bases" → "Termbases" (single word)

### Changed
- **Database Tables:** Renamed `glossary_terms` → `termbase_terms`, `glossary_id` → `termbase_id`
- **SQL Queries:** Updated all queries to use new table/column names

### Added
- **Sample Data:** Created 3 test termbases (Medical, Legal, Technical) with 48 total terms for testing

---

## [1.0.0] - October 28, 2025

### Added
- **Qt Edition Launch:** Initial release of PyQt6-based modern CAT interface
- **Translation Memory:** Full-text search with fuzzy matching and relevance scoring
- **Termbases:** Multiple termbase support with global and project-specific scopes
- **CAT Editor:** Segment-based translation editing interface
- **Project Management:** Create, manage, and switch between translation projects
- **Auto-fingers:** Smart terminology suggestions based on context
- **AI Integration:** OpenAI GPT and Claude support with configurable API keys
- **Database Backend:** SQLite persistent storage with 7 core tables

---

## Versioning Strategy

- **Major.Minor.Patch** (e.g., 1.0.1)
  - **Major:** Significant architecture changes or breaking changes
  - **Minor:** New features or substantial improvements
  - **Patch:** Bug fixes and minor adjustments

---

## Future Roadmap

### Planned for v1.1.0
- Terminology Search (Ctrl+P)
- Concordance Search (Ctrl+K)
- Create/Edit termbase dialogs

### Planned for v1.2.0
- TMX Editor with visual highlighting
- Advanced filtering options
- Custom keyboard shortcuts

### Planned for v2.0.0
- Full feature parity with Tkinter edition
- Deprecation of Tkinter edition

---

**Note:** This changelog focuses exclusively on the Qt Edition. See [CHANGELOG_Tkinter.md](CHANGELOG_Tkinter.md) for Classic edition history.

**Last Updated:** October 30, 2025
- ✅ Fixed Project object access pattern (changed from dict `.get()` to object attributes)
- ✅ Fixed database schema issues in private database folder

### 📋 Terminology Standardization
- Replaced all "glossary" references with "termbase" throughout codebase
- Updated database table: `glossary_terms` → `termbase_terms`
- Updated column: `glossary_id` → `termbase_id`
- Unified UI labels to use "Termbases" (one word, consistent)
- **Files Updated**: 5+ Python files, database schema, UI labels

### 🎯 Known Issues
- Terminology Search (Ctrl+P) - Planned for next release
- Concordance Search (Ctrl+K) - Planned for next release

---

## [v1.0.0] - 2025-10-29 🎯 Phase 5.3 - Advanced Ribbon Features Complete

### 🎨 Major UX Enhancements - ALL 5 FEATURES IMPLEMENTED

**1. ✅ Context-Sensitive Ribbon**
- Ribbon automatically switches based on active tab
- Superlookup tab → Shows Translation ribbon
- Project Editor tab → Shows Home ribbon
- Intelligent tab selection for better workflow

**2. ✅ Quick Access Toolbar (QAT)**
- Mini toolbar above ribbon with most-used commands
- **Actions**: New 📄, Open 📂, Save 💾, Superlookup 🔍, Translate 🤖
- **Minimize Ribbon toggle** ⌃ - Collapse ribbon to tabs-only
- Always visible for quick access to favorites
- Icon-only buttons for compact display

**3. ✅ Quick Access Sidebar** (NEW)
- memoQ-style left navigation panel
- **Collapsible sections**:
  - **Quick Actions**: New, Open, Save
  - **Translation Tools**: Superlookup, AutoFingers, TM Manager
  - **Recent Files**: Double-click to open
- Resizable via splitter
- Toggle on/off via View menu

**4. ✅ Ribbon Minimization**
- Minimize ribbon to tabs-only mode (saves vertical space)
- Click tabs to show ribbon temporarily
- Toggle via ⌃ button in QAT

**5. ✅ Ribbon Customization Foundation**
- Signal-based architecture for easy customization
- Action mapping system for flexibility
- Extensible group/button structure

### 📦 New Modules
- `modules/quick_access_sidebar.py` - Reusable sidebar components
- `modules/project_home_panel.py` - Project-specific home panel

### 🔧 Technical Improvements
- Renamed splitters for clarity (sidebar_splitter, editor_splitter)
- Connected sidebar actions to ribbon action handler
- Automatic recent files update
- Context-sensitive ribbon switching
- Professional multi-panel layout

---

## [v1.0.0 - Phase 5.2] - 2025-10-29 🎨 Ribbon Interface - Modern CAT UI

### ✨ Major Features
- ✅ **Modern Ribbon Interface** - Similar to memoQ, Trados Studio, Microsoft Office
- ✅ **Four Ribbon Tabs**:
  - **Home**: New, Open, Save, Copy, Paste, Find, Replace, Go To
  - **Translation**: Translate, Batch Translate, TM Manager, Superlookup
  - **View**: Zoom In/Out, Auto-Resize Rows, Themes
  - **Tools**: AutoFingers, Options
- ✅ **Grouped Buttons** - Related functions organized into visual groups
- ✅ **Emoji Icons** - Clear, colorful visual indicators
- ✅ **Hover Effects** - Modern button styling with transparency and borders
- ✅ **Full Integration** - All actions connected to existing functionality

### 🎯 Architecture
- Created `modules/ribbon_widget.py` - Reusable ribbon components
- Tab-based ribbon system with dynamic button groups
- Action signals connected to main window handlers
- Professional styling matching modern CAT tools

---

## [v1.0.0 - Phase 5.1] - 2025-10-28 📊 Translation Results Panel Complete

### ✨ Features Implemented
- ✅ **Compact Stacked Layout** - Collapsible match sections (NT, MT, TM, Termbases)
- ✅ **Relevance Display** - Shows match percentages and confidence levels
- ✅ **Metadata Display** - Domain, context, date information
- ✅ **Drag/Drop Support** - Insert matches into translation field
- ✅ **Compare Boxes** - Side-by-side comparison (Source | TM Source | TM Target)
- ✅ **Diff Highlighting** - Red/green styling for visual comparison
- ✅ **Segment Info** - Metadata and notes display
- ✅ **Integration** - Fully integrated into Project Editor tab

### 📦 New Module
- `modules/translation_results_panel.py` - Compact, production-ready results display

### 🎯 Layout
- Stacked match sections with collapsible headers
- Compact match items for efficient use of space
- Relevance percentage display
- Metadata columns (domain, context, source)
- Notes and segment information panel

---

## [v1.0.0 - Phase 5.0] - 2025-10-27 🚀 Qt Edition Launch

### ✨ Core Features
- ✅ **PyQt6 Framework** - Modern, cross-platform UI
- ✅ **Dual-Tab Interface**:
  - Project Editor - Main translation workspace
  - Superlookup - Dictionary/search tool
- ✅ **Project Management** - Load/save translation projects
- ✅ **Translation Memory** - Full TMX support
- ✅ **Segment Grid** - Professional translation grid view
- ✅ **AI Integration** - Multiple LLM provider support (OpenAI, Anthropic, etc.)
- ✅ **Keyboard Shortcuts** - Comprehensive hotkey system
- ✅ **AutoHotkey Integration** - System-wide lookup support

### 🎯 Application Structure
- Professional CAT tool architecture
- Modular design for extensibility
- Clean separation of concerns
- Database-backed translation memory
- Responsive UI with drag/drop support

---

## Release History - Previous Phases

For Qt development history before Phase 5.0, see `docs/RELEASE_Qt_v1.0.0_Phase5.md`

---

## Version Numbering

Supervertaler Qt uses semantic versioning:
- **MAJOR** - Major feature additions or breaking changes
- **MINOR** - New features, backward compatible
- **PATCH** - Bug fixes and improvements
- **PHASE** - Development phase tracking (Phase 5+)

**Current**: v1.0.2 (Phase 5.4)
