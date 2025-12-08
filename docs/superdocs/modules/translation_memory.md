# translation_memory

**File:** `modules/translation_memory.py`
**Lines:** 651
**Classes:** 3
**Functions:** 0

---

## Module Description

Translation Memory Module - SQLite Database Backend

Manages translation memory with fuzzy matching capabilities using SQLite.
Supports multiple TMs: Project TM, Big Mama TM, and custom TMX files.

Migrated from in-memory dictionaries to SQLite for scalability.

---

## Classes

### `TM`

**Line:** 18

Individual Translation Memory with metadata

#### Methods

##### `add_entry()`

Add translation pair to this TM

##### `get_exact_match()`

Get exact match from this TM

##### `calculate_similarity()`

Calculate similarity ratio between two texts

##### `get_fuzzy_matches()`

Get fuzzy matches from this TM

##### `get_entry_count()`

Get number of entries in this TM

##### `to_dict()`

Serialize TM to dictionary for JSON storage

##### `from_dict()`

Deserialize TM from dictionary


---

### `TMDatabase`

**Line:** 101

Manages multiple Translation Memories using SQLite backend

#### Methods

##### `set_tm_languages()`

Set language pair for TMs

##### `add_entry()`

Add translation pair to TM

Args:
    source: Source text
    target: Target text
    tm_id: TM identifier ('project', 'big_mama', or custom)
    context_before: Previous segment for context
    context_after: Next segment for context
    notes: Optional notes

##### `add_to_project_tm()`

Add entry to Project TM (convenience method)

##### `get_exact_match()`

Get exact match from TM(s)

Args:
    source: Source text to match
    tm_ids: List of TM IDs to search (None = all enabled)

Returns: Target text or None

##### `search_all()`

Search across multiple TMs for fuzzy matches

Args:
    source: Source text to search for
    tm_ids: Specific TM IDs to search (None = search all)
    enabled_only: Only search enabled TMs
    max_matches: Maximum number of results

Returns:
    List of match dictionaries sorted by similarity

##### `concordance_search()`

Search for text in both source and target

Args:
    query: Search query
    tm_ids: TM IDs to search (None = all)

Returns: List of matching entries

##### `get_tm_entries()`

Get all entries from a specific TM

Args:
    tm_id: TM identifier
    limit: Maximum number of entries (None = all)

Returns: List of entry dictionaries

##### `get_entry_count()`

Get entry count for TM(s)

Args:
    tm_id: Specific TM ID (None = all)
    enabled_only: Only count enabled TMs

Returns: Total entry count

##### `clear_tm()`

Clear all entries from a TM

##### `delete_entry()`

Delete a specific entry from a TM

##### `add_custom_tm()`

Register a custom TM

##### `remove_custom_tm()`

Remove a custom TM and its entries

##### `get_tm_list()`

Get list of all TMs with metadata

Returns: List of TM info dictionaries

##### `get_all_tms()`

Alias for get_tm_list() for backward compatibility

##### `load_tmx_file()`

Load TMX file into a new custom TM

Args:
    filepath: Path to TMX file
    src_lang: Source language code
    tgt_lang: Target language code
    tm_name: Custom name for TM (default: filename)
    read_only: Make TM read-only
    strip_variants: Match base languages ignoring regional variants (default: True)

Returns: (tm_id, entry_count)

##### `detect_tmx_languages()`

Detect all language codes present in a TMX file

##### `check_language_compatibility()`

Analyze if TMX languages match target TM languages, handling variants.
Returns dict with compatibility info and suggestions.

##### `close()`

Close database connection

##### `to_dict()`

Export to legacy dictionary format (for JSON serialization)

##### `from_dict()`

Import from legacy dictionary format (for JSON deserialization)


---

### `TMAgent`

**Line:** 596

Legacy wrapper for backwards compatibility - delegates to TMDatabase

#### Methods

##### `tm_data()`

Legacy property - returns Project TM entries as dictionary

##### `tm_data()`

Legacy property setter - loads entries into Project TM

##### `add_entry()`

Add to Project TM

##### `get_exact_match()`

Search all enabled TMs for exact match

##### `get_fuzzy_matches()`

Legacy format - returns tuples

##### `get_best_match()`

Get best match in legacy format

##### `load_from_tmx()`

Legacy TMX load - loads into a new custom TM

##### `get_entry_count()`

Get total entry count

##### `clear()`

Clear Project TM only

##### `delete_entry()`

Delete a specific entry from a TM


---

