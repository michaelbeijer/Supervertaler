# tag_manager

**File:** `modules/tag_manager.py`
**Lines:** 299
**Classes:** 2
**Functions:** 0

---

## Module Description

Tag Manager
Handle inline formatting tags (bold, italic, underline)

This module converts formatting runs into XML-like tags for editing,
validates tag integrity, and reconstructs formatting on export.

Example:
    "This is **bold** text" → "This is <b>bold</b> text"

---

## Classes

### `FormattingRun`

**Line:** 18

Represents a formatting run in text

#### Methods

##### `has_formatting()`

Check if this run has any formatting

##### `get_tag_name()`

Get the tag name for this formatting


---

### `TagManager`

**Line:** 44

Manage inline formatting tags

#### Methods

##### `extract_runs()`

Extract formatting runs from a python-docx paragraph

Args:
    paragraph: python-docx paragraph object
    
Returns:
    List of FormattingRun objects with position information

##### `runs_to_tagged_text()`

Convert formatting runs to tagged text

Example:
    [Run("Hello ", bold=False), Run("world", bold=True), Run("!", bold=False)]
    → "Hello <b>world</b>!"

Args:
    runs: List of FormattingRun objects
    
Returns:
    Text with inline tags

##### `tagged_text_to_runs()`

Convert tagged text back to run specifications

Example:
    "Hello <b>world</b>!" →
    [{'text': 'Hello ', 'bold': False},
     {'text': 'world', 'bold': True},
     {'text': '!', 'bold': False}]

Args:
    text: Text with inline tags
    
Returns:
    List of run specifications (dicts with text and formatting)

##### `validate_tags()`

Validate that all tags are properly paired and nested

Args:
    text: Text with inline tags
    
Returns:
    (is_valid, error_message)

##### `count_tags()`

Count tags in text

Returns:
    Dictionary with tag counts (e.g., {'b': 2, 'i': 1})

##### `strip_tags()`

Remove all tags from text

##### `get_tag_color()`

Get color for tag name

##### `format_for_display()`

Format tagged text for display (simplified version)
This could be enhanced with colored markers in a rich text widget

For now, just show tags as-is


---

