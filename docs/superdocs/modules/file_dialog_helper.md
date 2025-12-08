# file_dialog_helper

**File:** `modules/file_dialog_helper.py`
**Lines:** 148
**Classes:** 0
**Functions:** 4

---

## Module Description

File Dialog Helper for Supervertaler
Wraps PyQt6 QFileDialog to remember last used directory across all dialogs.

Author: Michael Beijer
License: MIT

---

## Functions

### `get_open_file_name()`

**Line:** 14

Show an open file dialog that remembers the last directory.

Args:
    parent: Parent widget
    caption: Dialog title
    filter: File type filters (e.g., "Text Files (*.txt);;All Files (*)")
    initial_filter: Initially selected filter
    
Returns:
    Tuple of (selected_file_path, selected_filter)

---

### `get_open_file_names()`

**Line:** 49

Show an open multiple files dialog that remembers the last directory.

Args:
    parent: Parent widget
    caption: Dialog title
    filter: File type filters
    initial_filter: Initially selected filter
    
Returns:
    Tuple of (list_of_selected_files, selected_filter)

---

### `get_save_file_name()`

**Line:** 84

Show a save file dialog that remembers the last directory.

Args:
    parent: Parent widget
    caption: Dialog title
    filter: File type filters
    initial_filter: Initially selected filter
    
Returns:
    Tuple of (selected_file_path, selected_filter)

---

### `get_existing_directory()`

**Line:** 119

Show a directory selection dialog that remembers the last directory.

Args:
    parent: Parent widget
    caption: Dialog title
    options: Dialog options
    
Returns:
    Selected directory path

---

