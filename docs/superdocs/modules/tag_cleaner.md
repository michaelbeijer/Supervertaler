# tag_cleaner

**File:** `modules/tag_cleaner.py`
**Lines:** 260
**Classes:** 2
**Functions:** 0

---

## Module Description

TagCleaner Module for Supervertaler
Removes CAT tool tags from translation text

Supports tags from:
- memoQ
- Trados Studio
- CafeTran
- Wordfast

Can be used standalone or integrated with other modules like AutoFingers.

---

## Classes

### `TagPattern`

**Line:** 20

Definition of a tag pattern to clean

---

### `TagCleaner`

**Line:** 28

Removes CAT tool tags from translation text.

Usage:
    cleaner = TagCleaner()
    cleaner.enable_memoq_index_tags()
    cleaned = cleaner.clean("Text with [1}tags{2] here")

#### Methods

##### `enable()`

Enable tag cleaning (master switch).

##### `disable()`

Disable tag cleaning (master switch).

##### `is_enabled()`

Check if tag cleaning is enabled.

##### `enable_memoq_index_tags()`

Enable cleaning of memoQ index tags ([1} {2] etc.).

##### `disable_memoq_index_tags()`

Disable cleaning of memoQ index tags.

##### `is_memoq_index_tags_enabled()`

Check if memoQ index tag cleaning is enabled.

##### `add_custom_pattern()`

Add a custom tag pattern.

Args:
    category: Category name ("memoq", "trados", "cafetran", "wordfast")
    key: Unique identifier for this pattern
    pattern: TagPattern to add

##### `remove_pattern()`

Remove a tag pattern.

##### `get_all_patterns()`

Get all tag patterns from all categories.

##### `get_enabled_patterns()`

Get only enabled tag patterns.

##### `clean()`

Remove tags from text based on enabled patterns.

Args:
    text: Text potentially containing CAT tool tags

Returns:
    Text with enabled tags removed

##### `preview_cleaning()`

Preview what text would look like with each pattern applied.

Args:
    text: Text to preview cleaning on

Returns:
    Dictionary mapping pattern names to cleaned text

##### `to_dict()`

Export settings to dictionary (for JSON serialization).

Returns:
    Dictionary with all tag cleaner settings

##### `from_dict()`

Import settings from dictionary.

Args:
    settings: Dictionary with tag cleaner settings


---

