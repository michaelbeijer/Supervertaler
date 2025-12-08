# termbase_manager

**File:** `modules/termbase_manager.py`
**Lines:** 1,014
**Classes:** 1
**Functions:** 0

---

## Module Description

Termbase Manager Module

Handles all termbase operations: creation, activation, term management, searching.
Uses 'termbase' terminology throughout (never 'glossary').

Termbases can be:
- Global (available to all projects)
- Project-specific (linked to particular project)

Activation system: termbases can be activated/deactivated per project.

---

## Classes

### `TermbaseManager`

**Line:** 20

Manages termbase operations and term storage

#### Methods

##### `create_termbase()`

Create a new termbase

Args:
    name: Termbase name
    source_lang: Source language code (e.g., 'en', 'nl')
    target_lang: Target language code
    project_id: If set, termbase is project-specific; if None, it's global
    description: Optional description
    is_global: Whether this is a global termbase (available to all projects)
    is_project_termbase: Whether this is the special project termbase (only one allowed per project)
    
Returns:
    Termbase ID or None if failed

##### `get_all_termbases()`

Get all termbases (global and project-specific)

Returns:
    List of termbase dictionaries with fields: id, name, source_lang, target_lang, 
    project_id, description, is_global, is_active, term_count, created_date, modified_date

##### `get_termbase()`

Get single termbase by ID

##### `delete_termbase()`

Delete termbase and all its terms

Args:
    termbase_id: Termbase ID
    
Returns:
    True if successful

##### `get_active_termbases_for_project()`

Get all active termbases for a specific project

Args:
    project_id: Project ID
    
Returns:
    List of active termbase dictionaries

##### `is_termbase_active()`

Check if termbase is active for a project

##### `activate_termbase()`

Activate termbase for project and assign ranking

##### `deactivate_termbase()`

Deactivate termbase for project and reassign rankings

##### `set_termbase_read_only()`

Set termbase read-only status (True = read-only, False = writable)

##### `set_termbase_priority()`

Set manual priority for a termbase in a specific project.
Multiple termbases can have the same priority.

Args:
    termbase_id: Termbase ID
    project_id: Project ID
    priority: Priority level (1=highest, 2=second, etc.)

Returns:
    True if successful

##### `get_termbase_priority()`

Get priority for a termbase in a specific project

##### `set_as_project_termbase()`

Set a termbase as the project termbase for a project.
Only one project termbase allowed per project - this will unset any existing one.

##### `get_active_termbase_ids()`

Get list of active termbase IDs for a project (for saving to project file)

Returns:
    List of termbase IDs (not database IDs)

##### `unset_project_termbase()`

Remove project termbase designation from a termbase

##### `get_project_termbase()`

Get the project termbase for a specific project

##### `add_term()`

Add a term to termbase

Args:
    termbase_id: Termbase ID
    source_term: Source language term
    target_term: Target language term
    priority: Priority (1=highest, 99=default)
    domain: Domain/category
    notes: Optional notes/definition
    project: Optional project name
    client: Optional client name
    forbidden: Whether this is a forbidden term
    source_lang: Source language code
    target_lang: Target language code
    term_uuid: Optional UUID for tracking term across imports/exports
    
Returns:
    Term ID or None if failed

##### `get_terms()`

Get all terms in a termbase

##### `update_term()`

Update a term

##### `delete_term()`

Delete a term

##### `search_termbase()`

Search within a termbase (searches main terms AND synonyms)

Args:
    termbase_id: Termbase ID to search in
    search_term: Term to search for
    search_source: Search in source terms and source synonyms
    search_target: Search in target terms and target synonyms
    
Returns:
    List of matching terms (includes main term + synonyms as separate entries)

##### `add_synonym()`

Add a synonym to a term

Args:
    term_id: Term ID to add synonym to
    synonym_text: The synonym text
    language: 'source' or 'target' (default: 'target')
    display_order: Position in list (0 = main/top, higher = lower priority)
    forbidden: Whether this synonym is forbidden
    
Returns:
    True if successful, False otherwise

##### `get_synonyms()`

Get synonyms for a term, ordered by display_order (position)

Args:
    term_id: Term ID to get synonyms for
    language: Optional filter - 'source', 'target', or None for both
    
Returns:
    List of synonym dictionaries with fields: id, synonym_text, language, display_order, forbidden

##### `update_synonym_order()`

Update the display order of a synonym

Args:
    synonym_id: Synonym ID to update
    new_order: New display order (0 = top/main)
    
Returns:
    True if successful, False otherwise

##### `update_synonym_forbidden()`

Update the forbidden flag of a synonym

Args:
    synonym_id: Synonym ID to update
    forbidden: New forbidden status
    
Returns:
    True if successful, False otherwise

##### `reorder_synonyms()`

Reorder synonyms for a term

Args:
    term_id: Term ID
    language: 'source' or 'target'
    synonym_ids_in_order: List of synonym IDs in desired order
    
Returns:
    True if successful, False otherwise

##### `delete_synonym()`

Delete a synonym

Args:
    synonym_id: Synonym ID to delete
    
Returns:
    True if successful, False otherwise


---

