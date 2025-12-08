# tracked_changes

**File:** `modules/tracked_changes.py`
**Lines:** 900
**Classes:** 2
**Functions:** 1

---

## Module Description

Tracked Changes Management Module

This module handles tracked changes from DOCX files or TSV files.
Provides AI with examples of preferred editing patterns to learn translator style.

Classes:
    - TrackedChangesAgent: Manages tracked changes data and provides search/filtering
    - TrackedChangesBrowser: UI window for browsing and analyzing tracked changes

---

## Classes

### `TrackedChangesAgent`

**Line:** 25

Manages tracked changes from DOCX files or TSV files.
Provides AI with examples of preferred editing patterns to learn translator style.

#### Methods

##### `log()`

Log a message

##### `load_docx_changes()`

Load tracked changes from a DOCX file

Args:
    docx_path: Path to DOCX file
    parse_docx_pairs_func: Function to parse DOCX and extract change pairs

##### `load_tsv_changes()`

Load tracked changes from a TSV file (original_text<tab>final_text format)

##### `clear_changes()`

Clear all loaded tracked changes

##### `search_changes()`

Search for changes containing the search text

##### `find_relevant_changes()`

Find tracked changes relevant to the current source segments being processed.
Uses two-pass algorithm: exact matches first, then partial word overlap.

##### `get_entry_count()`

Get number of loaded change pairs


---

### `TrackedChangesBrowser`

**Line:** 185

Browser UI for viewing and searching tracked changes

#### Methods

##### `show_browser()`

Show the tracked changes browser window

##### `create_window()`

Create the browser window

##### `on_selection_change()`

Handle selection change in the tree

##### `on_search()`

Handle search input

##### `clear_search()`

Clear search and show all results

##### `load_results()`

Load results into the treeview

##### `show_context_menu()`

Show context menu for copying

##### `get_selected_change()`

Get the currently selected change pair

##### `copy_original()`

Copy original text to clipboard

##### `copy_final()`

Copy final text to clipboard

##### `copy_both()`

Copy both texts to clipboard

##### `export_to_md_report()`

Export tracked changes to a Markdown report with AI-powered change analysis

##### `get_ai_change_summaries_batch()`

Get AI summaries for a batch of changes - much faster than one-by-one


---

## Functions

### `format_tracked_changes_context()`

**Line:** 883

Format tracked changes for AI context, keeping within token limits

---

