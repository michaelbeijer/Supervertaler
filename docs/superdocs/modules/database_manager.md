# database_manager

**File:** `modules/database_manager.py`
**Lines:** 1,574
**Classes:** 1
**Functions:** 0

---

## Module Description

Database Manager Module

SQLite database backend for Translation Memories, Glossaries, and related resources.
Replaces in-memory JSON-based storage with efficient database storage.

Schema includes:
- Translation units (TM entries)
- Termbase terms
- Non-translatables
- Segmentation rules
- Project metadata
- Resource file references

---

## Classes

### `DatabaseManager`

**Line:** 26

Manages SQLite database for translation resources

#### Methods

##### `connect()`

Connect to database and create tables if needed

##### `close()`

Close database connection

##### `add_translation_unit()`

Add translation unit to database

Returns: ID of inserted/updated entry

##### `get_exact_match()`

Get exact match from TM

Args:
    source: Source text to match
    tm_ids: List of TM IDs to search (None = all)
    source_lang: Filter by source language (base code matching: 'en' matches 'en-US', 'en-GB', etc.)
    target_lang: Filter by target language (base code matching)
    bidirectional: If True, search both directions (nl→en AND en→nl)

Returns: Dictionary with match data or None

##### `calculate_similarity()`

Calculate similarity ratio between two texts using SequenceMatcher

Returns: Similarity score from 0.0 to 1.0

##### `search_fuzzy_matches()`

Search for fuzzy matches using FTS5 with proper similarity calculation

Args:
    bidirectional: If True, search both directions (nl→en AND en→nl)

Returns: List of matches with similarity scores

##### `search_all()`

Search for matches across TMs (both exact and fuzzy)

Args:
    source: Source text to search for
    tm_ids: List of TM IDs to search (None = all)
    enabled_only: Currently ignored (all TMs enabled)
    threshold: Minimum similarity threshold (0.0-1.0)
    max_results: Maximum number of results
    
Returns:
    List of matches with source, target, match_pct, tm_name

##### `get_tm_entries()`

Get all entries from a specific TM

##### `get_tm_count()`

Get entry count for TM(s)

##### `clear_tm()`

Clear all entries from a TM

##### `delete_entry()`

Delete a specific entry from a TM

##### `concordance_search()`

Search for text in both source and target (concordance search)

##### `add_termbase_term()`

Add term to termbase (Phase 3)

##### `search_termbases()`

Search termbases for matching source terms

Args:
    search_term: Source term to search for
    source_lang: Filter by source language (optional)
    target_lang: Filter by target language (optional)
    project_id: Filter by project (optional)
    min_length: Minimum term length to return
    
Returns:
    List of termbase hits, sorted by priority (lower = higher priority)

##### `get_all_tms()`

Get list of all translation memories

Args:
    enabled_only: If True, only return enabled TMs
    
Returns:
    List of TM info dictionaries with tm_id, name, entry_count, enabled

##### `get_tm_list()`

Alias for get_all_tms for backward compatibility

##### `get_entry_count()`

Get total number of translation entries

Args:
    enabled_only: Currently ignored (all TMs enabled)
    
Returns:
    Total number of translation units

##### `vacuum()`

Optimize database (VACUUM)

##### `tmx_store_file()`

Store TMX file metadata in database

Returns:
    tmx_file_id (int)

##### `tmx_store_translation_unit()`

Store a translation unit in database

Args:
    commit: If False, don't commit (for batch operations)

Returns:
    Internal TU ID (for referencing segments)

##### `tmx_store_segment()`

Store a segment (language variant) for a translation unit

Args:
    commit: If False, don't commit (for batch operations)

##### `tmx_get_file_id()`

Get TMX file ID by file path

##### `tmx_get_translation_units()`

Get translation units with pagination and filtering

Returns:
    List of dicts with TU data including segments

##### `tmx_count_translation_units()`

Count translation units matching filters

##### `tmx_update_segment()`

Update a segment text

##### `tmx_delete_file()`

Delete TMX file and all its data (CASCADE will handle TUs and segments)

##### `tmx_get_file_info()`

Get TMX file metadata

##### `get_database_info()`

Get database statistics


---

