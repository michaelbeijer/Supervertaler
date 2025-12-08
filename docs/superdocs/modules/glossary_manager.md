# glossary_manager

**File:** `modules/glossary_manager.py`
**Lines:** 433
**Classes:** 3
**Functions:** 0

---

## Module Description

Termbase Manager Module

Handles termbase/termbase management for Supervertaler:
- Create/delete glossaries
- Add/edit/delete terms
- Activate/deactivate for projects
- Import/export glossaries
- Search across termbases

Unified management for both global and project-specific termbases.

---

## Classes

### `TermbaseInfo`

**Line:** 20

Information about a termbase/termbase

---

### `TermbaseEntry`

**Line:** 35

A single term entry in a termbase

---

### `TermbaseManager`

**Line:** 50

Manages glossaries and termbases

#### Methods

##### `create_termbase()`

Create a new termbase

Args:
    name: termbase name
    description: Optional description
    source_lang: Source language code (e.g., 'NL', 'EN')
    target_lang: Target language code
    project_id: Optional project ID (None = global termbase)

Returns:
    termbase ID

##### `get_all_termbases()`

Get all glossaries (global and project-specific)

##### `get_termbase_terms()`

Get all terms in a termbase

##### `add_term()`

Add a term to a termbase

Args:
    termbase_id: Target termbase ID
    source_term: Source language term
    target_term: Target language term
    priority: Priority ranking (1-99, lower = higher)
    domain: Domain/subject area
    definition: Definition or note
    forbidden: Whether term is forbidden for translation
    non_translatable: Whether term should not be translated

Returns:
    Term ID

##### `update_term()`

Update a term in a termbase

##### `delete_term()`

Delete a term from a termbase

##### `delete_termbase()`

Delete a termbase and all its terms

##### `activate_for_project()`

Mark a termbase as active for a specific project

##### `deactivate_for_project()`

Mark a termbase as inactive for a specific project

##### `is_active_for_project()`

Check if termbase is active for a project

##### `get_active_glossaries_for_project()`

Get all glossaries active for a specific project (global + project-specific)

##### `export_glossary_to_csv()`

Export termbase to CSV format

##### `import_glossary_from_csv()`

Import terms into termbase from CSV file


---

