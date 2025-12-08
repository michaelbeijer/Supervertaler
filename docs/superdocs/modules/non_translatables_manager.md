# non_translatables_manager

**File:** `modules/non_translatables_manager.py`
**Lines:** 743
**Classes:** 3
**Functions:** 1

---

## Module Description

Non-Translatables Manager Module

Manages non-translatable (NT) content - terms, phrases, and patterns that should 
not be translated. These include brand names, product names, technical identifiers,
codes, abbreviations, and other content that must remain in the original language.

File Format: .ntl (Non-Translatable List)
- YAML frontmatter with metadata
- Simple line-by-line entries (one NT per line)
- Comments start with #
- Blank lines are ignored

Import Support:
- Native .svntl format
- memoQ .mqres non-translatable lists (XML format)

Features:
- Multiple NT lists per project
- Case-sensitive/insensitive matching options
- Merge import with duplicate detection
- Export to native format

---

## Classes

### `NonTranslatable`

**Line:** 36

Single non-translatable entry

#### Methods

##### `matches()`

Find all occurrences of this NT in source text.

Matching is:
- Case-sensitive by default (case_sensitive=True)
- Full word only (uses word boundaries to avoid matching inside other words)
- Special characters (®, ™, etc.) are handled specially

Returns:
    List of (start_pos, end_pos) tuples for each match


---

### `NonTranslatableList`

**Line:** 109

A list of non-translatables with metadata

#### Methods

##### `entry_count()`

No docstring

##### `get_unique_texts()`

Get set of all NT texts (lowercase for comparison)

##### `find_matches()`

Find all NT matches in source text.

Returns:
    List of dicts with 'text', 'start', 'end', 'entry' keys


---

### `NonTranslatablesManager`

**Line:** 163

Manages non-translatable lists: loading, saving, searching, import/export

#### Methods

##### `save_list()`

Save a non-translatable list to .ntl format.

Format:
    ---
    name: List Name
    description: Optional description
    created_date: ISO date
    modified_date: ISO date
    source_language: en
    target_language: nl
    ---
    # Comments start with #
    Brand Name
    Product™
    Technical Term

Args:
    nt_list: The list to save
    filepath: Optional specific path (defaults to base_path/name.ntl)
    
Returns:
    True if successful

##### `load_list()`

Load a non-translatable list from .ntl format.

Args:
    filepath: Path to .ntl file
    
Returns:
    NonTranslatableList or None if failed

##### `load_from_plain_text()`

Load entries from a plain text file (one entry per line).

Args:
    filepath: Path to text file
    name: Optional name for the list (defaults to filename)
    
Returns:
    NonTranslatableList or None if failed

##### `import_memoq_mqres()`

Import non-translatables from memoQ .mqres format.

memoQ format:
    <MemoQResource ResourceType="NonTrans" Version="1.0">
      <Resource>
        <Guid>...</Guid>
        <FileName>...</FileName>
        <Name>...</Name>
        <Description />
      </Resource>
    </MemoQResource>
    <?xml version="1.0" encoding="utf-8"?>
    <nonTrans version="1.0">
      <nonTransRule>term1</nonTransRule>
      <nonTransRule>term2</nonTransRule>
    </nonTrans>

Args:
    filepath: Path to .mqres file
    name: Optional name override
    
Returns:
    NonTranslatableList or None if failed

##### `load_all_lists()`

Load all .svntl and legacy .ntl files from the base directory.

Returns:
    Number of lists loaded

##### `get_all_lists()`

Get all loaded lists

##### `get_active_lists()`

Get only active lists

##### `set_list_active()`

Set whether a list is active

##### `create_list()`

Create a new empty NT list

##### `delete_list()`

Delete a list (removes from memory and disk)

##### `merge_into_list()`

Merge entries from source list into target list.

Args:
    target_name: Name of target list (must exist)
    source_list: Source list to merge from
    ignore_duplicates: If True, skip entries that already exist
    
Returns:
    Tuple of (added_count, skipped_count)

##### `add_entry()`

Add a single entry to a list

##### `remove_entry()`

Remove an entry from a list by text

##### `find_all_matches()`

Find all NT matches in source text from all active lists.

Args:
    source_text: Text to search in
    
Returns:
    List of match dicts sorted by position

##### `get_unique_entries_from_active()`

Get all unique NT entries from active lists (lowercase)

##### `export_list()`

Export a list to .ntl format.

Args:
    name: Name of list to export
    filepath: Destination file path
    
Returns:
    True if successful

##### `export_to_plain_text()`

Export a list to plain text (one entry per line).

Args:
    name: Name of list to export
    filepath: Destination file path
    
Returns:
    True if successful


---

## Functions

### `convert_txt_to_ntl()`

**Line:** 719

Convert a plain text NT file to .ntl format.

Args:
    input_path: Path to input .txt file
    output_path: Path for output .ntl file (defaults to same dir with .ntl extension)
    name: Name for the list (defaults to filename)
    
Returns:
    True if successful

---

