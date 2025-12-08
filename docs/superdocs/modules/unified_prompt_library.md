# unified_prompt_library

**File:** `modules/unified_prompt_library.py`
**Lines:** 543
**Classes:** 1
**Functions:** 0

---

## Module Description

Unified Prompt Library Module

Simplified 2-layer architecture:
1. System Templates (in Settings) - mode-specific, auto-selected
2. Prompt Library (main UI) - unified workspace with folders, favorites, multi-attach

Replaces the old 4-layer system (System/Domain/Project/Style Guides).

---

## Classes

### `UnifiedPromptLibrary`

**Line:** 19

Manages prompts in a unified library structure with:
- Nested folder support (unlimited depth)
- Favorites and Quick Run menu
- Multi-attach capability
- Markdown files with YAML frontmatter

#### Methods

##### `set_directory()`

Set the library directory after initialization

##### `load_all_prompts()`

Load all prompts from library directory (recursive)

##### `save_prompt()`

Save prompt as Markdown file with YAML frontmatter.

Args:
    relative_path: Relative path within library (e.g., "Domain Expertise/Medical.md")
    prompt_data: Dictionary with prompt info and content

Returns:
    True if successful

##### `get_folder_structure()`

Get hierarchical folder structure with prompts.

Returns:
    Nested dictionary representing folder tree

##### `set_primary_prompt()`

Set the primary (main) active prompt

##### `set_external_primary_prompt()`

Set an external file (not in library) as the primary prompt.

Args:
    file_path: Absolute path to the external prompt file

Returns:
    Tuple of (success, display_name or error_message)

##### `attach_prompt()`

Attach a prompt to the active configuration

##### `detach_prompt()`

Remove an attached prompt

##### `clear_attachments()`

Clear all attached prompts

##### `toggle_favorite()`

Toggle favorite status for a prompt

##### `toggle_quick_run()`

Toggle quick run status for a prompt

##### `get_favorites()`

Get list of favorite prompts (path, name)

##### `get_quick_run_prompts()`

Get list of quick run prompts (path, name)

##### `create_folder()`

Create a new folder in the library

##### `move_prompt()`

Move a prompt to a different folder

##### `delete_prompt()`

Delete a prompt


---

