# style_guide_manager

**File:** `modules/style_guide_manager.py`
**Lines:** 315
**Classes:** 1
**Functions:** 0

---

## Module Description

Style Guide Manager Module

Manages translation style guides for different languages.
Supports style guides as Markdown files with optional YAML frontmatter.

Extracted for modularity and reusability.
Supports both individual language-specific guides and optional user additions.

---

## Classes

### `StyleGuideLibrary`

**Line:** 19

Manages translation style guides for multiple languages.
Loads style guide files from appropriate folder based on dev mode.

#### Methods

##### `set_directory()`

Set the directory after initialization

##### `load_all_guides()`

Load all style guides from the style guides directory

##### `get_guide()`

Get a specific style guide by language.

Args:
    language: Language name (e.g., 'Dutch', 'English')

Returns:
    Dictionary with guide data or None if not found

##### `get_all_languages()`

Get list of all available style guide languages

##### `get_guide_content()`

Get the content of a specific style guide

##### `update_guide()`

Update a style guide with new content.

Args:
    language: Language name
    new_content: New content for the guide

Returns:
    True if successful, False otherwise

##### `append_to_guide()`

Append content to an existing style guide.

Args:
    language: Language name
    additional_content: Content to append

Returns:
    True if successful, False otherwise

##### `append_to_all_guides()`

Append content to all style guides.

Args:
    additional_content: Content to append to all guides

Returns:
    Tuple of (successful_count, failed_count)

##### `create_guide()`

Create a new style guide file.

Args:
    language: Language name
    content: Initial content (optional)

Returns:
    True if successful, False otherwise

##### `export_guide()`

Export a style guide to a file.

Args:
    language: Language name
    export_path: Path where to save the exported guide

Returns:
    True if successful, False otherwise

##### `import_guide()`

Import a style guide from a file.

Args:
    language: Language name to import as
    import_path: Path to the file to import
    append: If True, append to existing guide; if False, replace

Returns:
    True if successful, False otherwise


---

