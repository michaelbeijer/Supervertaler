# prompt_library_migration

**File:** `modules/prompt_library_migration.py`
**Lines:** 447
**Classes:** 1
**Functions:** 1

---

## Module Description

Migration Script: 4-Layer to Unified Prompt Library

Migrates from old structure:
    1_System_Prompts/
    2_Domain_Prompts/
    3_Project_Prompts/
    4_Style_Guides/

To new unified structure:
    Library/
        Style Guides/
        Domain Expertise/
        Project Prompts/
        Active Projects/

System Prompts are moved to settings storage (handled separately).

---

## Classes

### `PromptLibraryMigration`

**Line:** 26

Handles one-time migration from 4-layer to unified structure

#### Methods

##### `needs_migration()`

Check if migration is needed

##### `migrate()`

Perform migration from old to new structure.

Steps:
1. Create new Library/ structure
2. Copy Domain Prompts → Library/Domain Expertise/
3. Copy Project Prompts → Library/Project Prompts/
4. Copy Style Guides → Library/Style Guides/
5. Backup old folders with .old extension
6. Mark migration as completed

Note: System Prompts are NOT migrated here (moved to settings separately)

Returns:
    True if successful

##### `rollback()`

Rollback migration (restore from .old backups)


---

## Functions

### `migrate_prompt_library()`

**Line:** 429

Convenience function to perform migration.

Args:
    prompt_library_dir: Path to user_data/Prompt_Library
    log_callback: Function for logging

Returns:
    True if migration successful or not needed

---

