# tm_manager_qt

**File:** `modules/tm_manager_qt.py`
**Lines:** 1,280
**Classes:** 4
**Functions:** 0

---

## Module Description

Translation Memory Manager for Supervertaler Qt
Provides comprehensive TM management features:
- Browse all TM entries
- Concordance search
- Import/Export TMX files
- Delete entries
- View statistics

---

## Classes

### `TMXImportThread`

**Line:** 24

Background thread for importing TMX files

#### Methods

##### `run()`

Import TMX file in background


---

### `HighlightDelegate`

**Line:** 99

Custom delegate to render HTML with highlighted text in table cells

#### Methods

##### `set_search_term()`

Set the term to highlight

##### `paint()`

Paint the cell with HTML rendering for highlighting

##### `sizeHint()`

Return size hint based on content


---

### `ConcordanceSearchDialog`

**Line:** 175

Lightweight Concordance Search dialog for Ctrl+K.
Focused on quick concordance search without other TM management features.
Features two view modes: List view and Table view (memoQ-style side-by-side).

#### Methods

##### `exec()`

Override exec to restore saved geometry or match parent window

##### `closeEvent()`

Save window geometry to project when closing

##### `setup_ui()`

Setup the UI with TM and Supermemory tabs

##### `do_search()`

Perform both TM concordance and Supermemory semantic search

##### `update_tm_view()`

Update the TM concordance view with current results

##### `update_supermemory_view()`

Update the Supermemory semantic search view


---

### `TMManagerDialog`

**Line:** 529

Translation Memory Manager dialog

#### Methods

##### `setup_ui()`

Setup the UI with tabs

##### `create_browser_tab()`

Create TM browser tab

##### `create_search_tab()`

Create concordance search tab

##### `create_import_export_tab()`

Create import/export tab

##### `create_stats_tab()`

Create statistics tab

##### `load_initial_data()`

Load initial data for all tabs

##### `refresh_browser()`

Refresh the TM browser table

##### `filter_browser_entries()`

Filter browser entries as user types

##### `delete_selected_entry()`

Delete the selected TM entry

##### `do_concordance_search()`

Perform concordance search

##### `import_tmx()`

Import a TMX file

##### `on_import_progress()`

Update import progress

##### `on_import_finished()`

Import finished

##### `export_tmx()`

Export TM to TMX file

##### `refresh_stats()`

Refresh TM statistics

##### `create_maintenance_tab()`

Create maintenance/cleaning tab

##### `clean_identical_source_target()`

Remove entries where source and target are identical

##### `clean_duplicate_sources()`

Remove duplicate sources, keeping only the newest translation


---

