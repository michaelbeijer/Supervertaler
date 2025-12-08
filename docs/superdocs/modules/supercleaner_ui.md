# supercleaner_ui

**File:** `modules/supercleaner_ui.py`
**Lines:** 444
**Classes:** 2
**Functions:** 0

---

## Module Description

Supercleaner UI Module for Supervertaler
========================================

Interactive UI for document cleaning with selectable operations.
Inspired by TransTools Document Cleaner, Unbreaker, and CodeZapper.

Author: Michael Beijer / Supervertaler

---

## Classes

### `SupercleanerUI`

**Line:** 21

Interactive UI for document cleaning with selectable operations

#### Methods

##### `init_ui()`

Initialize the user interface

##### `browse_file()`

Open file browser to select DOCX file

##### `apply_quick_clean_preset()`

Apply recommended quick clean settings

##### `apply_aggressive_preset()`

Apply aggressive cleaning settings

##### `clear_all_options()`

Clear all cleaning options

##### `get_selected_operations()`

Get dictionary of selected cleaning operations

##### `clean_document()`

Perform document cleaning with selected operations

##### `log()`

Add message to log


---

### `CheckmarkCheckBox`

**Line:** 354

Custom checkbox with green background and white checkmark when checked

#### Methods

##### `paintEvent()`

Override paint event to draw white checkmark when checked


---

