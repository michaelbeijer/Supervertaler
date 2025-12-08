# shortcut_manager

**File:** `modules/shortcut_manager.py`
**Lines:** 677
**Classes:** 1
**Functions:** 0

---

## Module Description

Keyboard Shortcut Manager for Supervertaler Qt
Centralized management of all keyboard shortcuts

---

## Classes

### `ShortcutManager`

**Line:** 12

Manages all keyboard shortcuts for Supervertaler

#### Methods

##### `load_shortcuts()`

Load custom shortcuts from file

##### `save_shortcuts()`

Save custom shortcuts to file

##### `get_shortcut()`

Get the current shortcut for a given ID

Args:
    shortcut_id: The shortcut identifier
    
Returns:
    The key sequence string (e.g., "Ctrl+T")

##### `set_shortcut()`

Set a custom shortcut

Args:
    shortcut_id: The shortcut identifier
    key_sequence: The new key sequence string

##### `reset_shortcut()`

Reset a shortcut to its default value

##### `reset_all_shortcuts()`

Reset all shortcuts to defaults

##### `get_all_shortcuts()`

Get all shortcuts with their current values

Returns:
    Dictionary of all shortcuts with metadata

##### `get_shortcuts_by_category()`

Get shortcuts organized by category

Returns:
    Dictionary with categories as keys, list of (id, data) tuples as values

##### `find_conflicts()`

Find conflicts with a proposed shortcut

Args:
    shortcut_id: The shortcut being changed
    key_sequence: The proposed new key sequence
    
Returns:
    List of conflicting shortcut IDs

##### `export_shortcuts()`

Export shortcuts to a JSON file

Args:
    file_path: Path to export file

##### `import_shortcuts()`

Import shortcuts from a JSON file

Args:
    file_path: Path to import file
    
Returns:
    True if successful, False otherwise

##### `export_html_cheatsheet()`

Export shortcuts as an HTML cheatsheet

Args:
    file_path: Path to export HTML file


---

