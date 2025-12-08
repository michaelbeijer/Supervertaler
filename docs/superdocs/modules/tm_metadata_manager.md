# tm_metadata_manager

**File:** `modules/tm_metadata_manager.py`
**Lines:** 505
**Classes:** 1
**Functions:** 0

---

## Module Description

Translation Memory Metadata Manager Module

Handles TM metadata operations: creation, activation, TM management.
Works alongside the existing translation_memory.py module which handles TM matching/searching.

TMs can be activated/deactivated per project (similar to termbases).

---

## Classes

### `TMMetadataManager`

**Line:** 15

Manages translation memory metadata and activation

#### Methods

##### `create_tm()`

Create a new TM metadata entry

Args:
    name: Display name for the TM (e.g., "ClientX_Medical_2024")
    tm_id: Unique identifier used in translation_units.tm_id field
    source_lang: Source language code (e.g., 'en', 'nl')
    target_lang: Target language code
    description: Optional description
    is_project_tm: Whether this is the special project TM (only one per project)
    read_only: Whether this TM should not be updated
    project_id: Which project this TM belongs to (NULL = global)
    
Returns:
    TM database ID or None if failed

##### `get_all_tms()`

Get all TMs with metadata

Returns:
    List of TM dictionaries with fields: id, name, tm_id, source_lang, target_lang,
    description, entry_count, created_date, modified_date, last_used,
    is_project_tm, read_only, project_id

##### `get_tm()`

Get single TM by database ID

##### `update_tm()`

Update TM metadata

##### `delete_tm()`

Delete TM metadata (and optionally its translation units)

Args:
    tm_db_id: Database ID of the TM
    delete_entries: If True, also delete all translation_units with this tm_id

##### `update_entry_count()`

Update cached entry count for a TM

##### `activate_tm()`

Activate a TM for a specific project

##### `deactivate_tm()`

Deactivate a TM for a specific project

##### `is_tm_active()`

Check if a TM is active for a project

##### `get_active_tm_ids()`

Get list of active tm_id strings for a project

Returns:
    List of tm_id strings that are active for the project

##### `set_as_project_tm()`

Set a TM as the project TM for a specific project.
Only one TM can be the project TM per project (automatically unsets others).

##### `unset_project_tm()`

Unset a TM as project TM

##### `get_project_tm()`

Get the project TM for a specific project

##### `get_tm_by_tm_id()`

Get TM by its tm_id string

##### `set_read_only()`

Set whether a TM is read-only (cannot be updated)


---

