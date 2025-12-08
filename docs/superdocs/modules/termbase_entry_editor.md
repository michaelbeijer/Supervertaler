# termbase_entry_editor

**File:** `modules/termbase_entry_editor.py`
**Lines:** 842
**Classes:** 2
**Functions:** 0

---

## Module Description

Termbase Entry Editor Dialog

Dialog for editing individual termbase entries with all metadata fields.
Can be opened from translation results panel (edit button or right-click menu).

---

## Classes

### `CheckmarkCheckBox`

**Line:** 18

Custom checkbox with green background and white checkmark when checked

#### Methods

##### `paintEvent()`

Override paint event to draw white checkmark when checked


---

### `TermbaseEntryEditor`

**Line:** 99

Dialog for editing a termbase entry

#### Methods

##### `setup_ui()`

Setup the user interface

##### `toggle_section()`

Toggle visibility of a collapsible section

##### `add_source_synonym()`

Add source synonym to list

##### `add_target_synonym()`

Add target synonym to list

##### `move_synonym()`

Move synonym up (-1) or down (1)

##### `delete_synonym()`

Delete selected synonym

##### `show_source_synonym_context_menu()`

Show context menu for source synonyms

##### `show_target_synonym_context_menu()`

Show context menu for target synonyms

##### `load_term_data()`

Load existing term data from database

##### `load_synonyms()`

Load synonyms for current term

##### `delete_term()`

Delete this term from database

##### `save_term()`

Save term to database

##### `save_synonyms()`

Save synonyms to database

##### `get_term_data()`

Get the current term data from the form fields


---

