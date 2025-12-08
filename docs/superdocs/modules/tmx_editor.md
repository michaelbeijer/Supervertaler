# tmx_editor

**File:** `modules/tmx_editor.py`
**Lines:** 1,461
**Classes:** 6
**Functions:** 1

---

## Module Description

TMX Editor Module - Professional Translation Memory Editor

A standalone, nimble TMX editor inspired by Heartsome TMX Editor 8.
Can run independently or integrate with Supervertaler.

Key Features (inspired by Heartsome):
- Dual-language grid editor (source/target columns)
- Fast filtering by language, content, status
- In-place editing with validation
- TMX file validation and repair
- Header metadata editing
- Large file support with pagination
- Import/Export multiple formats
- Multi-language support (view any language pair)

Architecture:
- Standalone mode: Run this file directly
- Integrated mode: Called from Supervertaler as a module

Designer: Michael Beijer
Based on concepts from: Heartsome TMX Editor 8 (Java/Eclipse RCP)
License: MIT - Open Source and Free

---

## Classes

### `TmxSegment`

**Line:** 35

Translation unit variant (segment in one language)

---

### `TmxTranslationUnit`

**Line:** 46

Translation unit (TU) containing multiple language variants

#### Methods

##### `get_segment()`

Get segment for specific language

##### `set_segment()`

Set or update segment for specific language


---

### `TmxHeader`

**Line:** 71

TMX file header information

#### Methods


---

### `TmxFile`

**Line:** 90

TMX file data model

#### Methods

##### `add_translation_unit()`

Add a translation unit and update language list

##### `get_languages()`

Get list of all languages in the TMX file

##### `get_tu_by_id()`

Get translation unit by ID

##### `get_tu_count()`

Get total number of translation units


---

### `TmxParser`

**Line:** 125

TMX file parser and writer

#### Methods

##### `parse_file()`

Parse TMX file and return TmxFile object

##### `save_file()`

Save TMX file


---

### `TmxEditorUI`

**Line:** 320

TMX Editor user interface

#### Methods

##### `create_ui()`

Create the user interface

##### `create_menu_bar()`

Create menu bar for standalone mode

##### `create_toolbar()`

Create toolbar with common actions

##### `create_language_panel()`

Create language selection panel

##### `create_filter_panel()`

Create filter panel

##### `create_edit_panel()`

Create integrated edit panel above the grid

##### `create_grid_editor()`

Create grid editor for translation units using Treeview (supports selection & resizing)

##### `create_pagination_controls()`

Create pagination controls

##### `create_status_bar()`

Create status bar

##### `create_context_menu()`

Create right-click context menu

##### `show_context_menu()`

Show context menu on right-click

##### `new_tmx()`

Create new TMX file

##### `open_tmx()`

Open TMX file

##### `save_tmx()`

Save TMX file

##### `save_tmx_as()`

Save TMX file with new name

##### `add_translation_unit()`

Add new translation unit

##### `delete_selected_tu()`

Delete translation unit (placeholder)

##### `edit_selected_tu()`

Edit selected translation unit (placeholder)

##### `open_edit_dialog()`

Open dialog to edit translation unit

##### `copy_source_to_target()`

Copy source text to target (placeholder)

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

##### `highlight_search_term_in_text()`

Highlight search term in text using Unicode bold characters

Args:
    text: Text to search in
    search_term: Term to highlight

Returns:
    Text with search term converted to Unicode bold

##### `refresh_current_page()`

Refresh current page in Treeview grid

##### `on_tree_select()`

Handle tree selection - load into edit panel

##### `on_tree_double_click()`

Handle double-click on tree - load into edit panel and focus

##### `edit_selected_tu()`

Edit selected TU from context menu

##### `load_tu_into_edit_panel()`

Load a TU into the integrated edit panel

##### `save_integrated_edit()`

Save changes from integrated edit panel

##### `cancel_integrated_edit()`

Cancel editing and clear the integrated edit panel

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

##### `show_find_replace()`

Show find/replace dialog

##### `export_tmx()`

Export TMX to other formats

##### `refresh_ui()`

Refresh entire UI after loading file

##### `set_status()`

Set status bar message

##### `on_closing()`

Handle window closing

##### `run()`

Run the application (standalone mode only)


---

## Functions

### `main()`

**Line:** 1454

Main entry point for standalone execution

---

