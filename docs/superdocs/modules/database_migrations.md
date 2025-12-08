# database_migrations

**File:** `modules/database_migrations.py`
**Lines:** 413
**Classes:** 0
**Functions:** 7

---

## Module Description

Database Migration Functions

Handles schema updates and data migrations for the Supervertaler database.

---

## Functions

### `migrate_termbase_fields()`

**Line:** 11

Migrate termbase_terms table to add new fields:
- project (TEXT)
- client (TEXT)
- term_uuid (TEXT UNIQUE) - for tracking terms across import/export

Note: 'notes' field already exists in schema, 'definition' is legacy (no longer used)

Args:
    db_manager: DatabaseManager instance
    
Returns:
    True if migration successful

---

### `create_synonyms_table()`

**Line:** 84

Create termbase_synonyms table for storing term synonyms.

Schema:
- id: Primary key
- term_id: Foreign key to termbase_terms
- synonym_text: The synonym text
- language: 'source' or 'target'
- created_date: Timestamp

Args:
    db_manager: DatabaseManager instance
    
Returns:
    True if successful

---

### `run_all_migrations()`

**Line:** 158

Run all pending database migrations.

Args:
    db_manager: DatabaseManager instance
    
Returns:
    True if all migrations successful

---

### `check_and_migrate()`

**Line:** 191

Check if migrations are needed and run them if so.
This is safe to call on every app startup.

Args:
    db_manager: DatabaseManager instance
    
Returns:
    True if migrations successful or not needed

---

### `migrate_synonym_fields()`

**Line:** 254

Migrate termbase_synonyms table to add new fields:
- display_order (INTEGER) - position in synonym list (0 = main term)
- forbidden (INTEGER) - whether this synonym is forbidden (0/1)

Args:
    db_manager: DatabaseManager instance
    
Returns:
    True if migration successful

---

### `generate_missing_uuids()`

**Line:** 315

Generate UUIDs for any termbase terms that don't have them.
This ensures all existing terms get UUIDs after the term_uuid column is added.

Args:
    db_manager: DatabaseManager instance

Returns:
    True if successful

---

### `fix_project_termbase_flags()`

**Line:** 363

Fix is_project_termbase flags for termbases that have project_id but is_project_termbase=0.
This is a data repair function that should be called manually or in migrations.

Args:
    db_manager: DatabaseManager instance

Returns:
    Number of termbases fixed

---

