# keyboard_shortcuts_widget

**File:** `modules/keyboard_shortcuts_widget.py`
**Lines:** 514
**Classes:** 3
**Functions:** 0

---

## Module Description

Keyboard Shortcuts Settings Widget
Provides UI for viewing, editing, and managing keyboard shortcuts

---

## Classes

### `KeySequenceEdit`

**Line:** 18

Custom widget for capturing keyboard shortcuts

#### Methods

##### `keyPressEvent()`

Capture key press and convert to shortcut string

##### `focusInEvent()`

Clear on focus for new input


---

### `ShortcutEditDialog`

**Line:** 67

Dialog for editing a keyboard shortcut

#### Methods

##### `reset_to_default()`

Reset to default shortcut

##### `check_conflicts()`

Check for conflicting shortcuts

##### `accept_shortcut()`

Accept the new shortcut


---

### `KeyboardShortcutsWidget`

**Line:** 182

Main widget for keyboard shortcuts settings

#### Methods

##### `init_ui()`

Initialize the user interface

##### `load_shortcuts()`

Load shortcuts into the table

##### `filter_shortcuts()`

Filter shortcuts based on search text

##### `edit_selected_shortcut()`

Edit the selected shortcut

##### `reset_selected()`

Reset selected shortcut to default

##### `reset_all()`

Reset all shortcuts to defaults

##### `export_shortcuts()`

Export shortcuts to JSON file

##### `import_shortcuts()`

Import shortcuts from JSON file

##### `export_html_cheatsheet()`

Export shortcuts as HTML cheatsheet


---

