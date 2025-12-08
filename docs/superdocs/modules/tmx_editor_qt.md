# tmx_editor_qt

**File:** `modules/tmx_editor_qt.py`
**Lines:** 2,269
**Classes:** 4
**Functions:** 0

---

## Module Description

TMX Editor Module - PyQt6 Edition

Professional Translation Memory Editor for Qt version of Supervertaler.
Based on the tkinter version, converted to PyQt6.

Key Features:
- Dual-language grid editor (source/target columns)
- Fast filtering by language, content, status
- In-place editing with validation
- TMX file validation and repair
- Header metadata editing
- Large file support with pagination
- Import/Export multiple formats
- Multi-language support (view any language pair)

Reuses core logic from tmx_editor.py (TmxFile, TmxParser, data classes)

---

## Classes

### `CheckmarkCheckBox`

**Line:** 41

Custom checkbox with green background and white checkmark when checked - same as AutoFingers

#### Methods

##### `paintEvent()`

Override paint event to draw white checkmark when checked


---

### `HighlightDelegate`

**Line:** 123

Custom delegate to highlight filter text in table cells

#### Methods

##### `set_highlight()`

Set the text to highlight

##### `paint()`

Paint the cell with highlighted text


---

### `TmxEditorUIQt`

**Line:** 210

TMX Editor user interface - PyQt6 version

#### Methods

##### `setup_ui()`

Create the user interface - Heartsome-style layout

##### `create_toolbar()`

Create toolbar with common actions

##### `create_top_header_panel()`

Create top header panel with Language Pair and Search Filter - Heartsome style

##### `create_language_panel()`

Create language selection panel - compact version for sidebar

##### `create_filter_panel()`

Create filter panel - Heartsome style

##### `create_grid_editor()`

Create grid editor for translation units using QTableWidget - Heartsome style

##### `create_pagination_controls()`

Create pagination controls

##### `create_attributes_editor()`

Create Attributes Editor panel (right side) - Heartsome style

##### `update_attributes_display()`

Update the Attributes Editor panel with TU attributes

##### `clear_attributes_display()`

Clear the Attributes Editor panel

##### `create_status_bar()`

Create status bar

##### `new_tmx()`

Create new TMX file

##### `open_tmx()`

Open TMX file with RAM/DB/Auto mode selection

##### `save_tmx()`

Save TMX file

##### `close_tmx()`

Close current TMX file

##### `save_tmx_as()`

Save TMX file with new name

##### `add_translation_unit()`

Add new translation unit

##### `delete_selected_tu()`

Delete selected translation unit

##### `on_language_changed()`

Handle language selection change

##### `show_all_languages()`

Show dialog with all languages in TMX

##### `edit_header()`

Edit TMX header metadata

##### `show_statistics()`

Show TMX file statistics

##### `apply_filters()`

Apply filters and refresh grid

##### `clear_filters()`

Clear all filters

##### `refresh_current_page()`

Refresh current page in table

##### `create_status_bar()`

Create status bar - Heartsome style

##### `on_table_selection_changed()`

Handle table selection change - update attributes

##### `on_table_double_clicked()`

Handle double-click on table - edit inline

##### `on_cell_edited()`

Handle cell edit - save changes directly to TMX data

##### `show_context_menu()`

Show context menu on right-click

##### `edit_selected_tu()`

Edit selected TU from context menu - just focus the cell for inline editing

##### `first_page()`

Go to first page

##### `prev_page()`

Go to previous page

##### `next_page()`

Go to next page

##### `last_page()`

Go to last page

##### `validate_tmx()`

Validate TMX file structure

##### `refresh_ui()`

Refresh entire UI after loading file

##### `set_status()`

Set status bar message


---

### `StandaloneWindow`

**Line:** 2179

Standalone window for TMX Editor

#### Methods

##### `closeEvent()`

Handle window close - check for unsaved changes


---

