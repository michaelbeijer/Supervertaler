# prompt_library

**File:** `modules/prompt_library.py`
**Lines:** 689
**Classes:** 1
**Functions:** 1

---

## Module Description

Prompt Library Manager Module

Manages translation prompts with domain-specific expertise.
Supports two types:
- System Prompts: Define AI role and expertise
- Custom Instructions: Additional context and preferences

Supports both JSON (legacy) and Markdown (recommended) formats.
Markdown files use YAML frontmatter for metadata.

Extracted from main Supervertaler file for better modularity.

---

## Classes

### `PromptLibrary`

**Line:** 33

Manages translation prompts with domain-specific expertise.
Supports two types:
- System Prompts: Define AI role and expertise
- Custom Instructions: Additional context and preferences

Loads prompt files from appropriate folders based on dev mode.

#### Methods

##### `set_directories()`

Set the directories after initialization

Args:
    domain_prompts_dir: Path to domain prompts directory (Layer 2 - preferred)
    project_prompts_dir: Path to project prompts directory (Layer 3 - preferred)
    system_prompts_dir: (Deprecated) Alias for domain_prompts_dir
    custom_instructions_dir: (Deprecated) Alias for project_prompts_dir

##### `load_all_prompts()`

Load all prompts (system prompts and custom instructions) from appropriate directories

##### `parse_markdown()`

Parse Markdown file with YAML frontmatter into prompt data.

Format:
---
name: "Prompt Name"
description: "Description"
domain: "Domain"
version: "1.0"
task_type: "Translation"
created: "2025-10-19"
---

# Content
Actual prompt content here...

##### `markdown_to_dict()`

Convert Markdown file to dictionary (alias for parse_markdown)

##### `dict_to_markdown()`

Save prompt data as Markdown file with YAML frontmatter.

Args:
    prompt_data: Dictionary with prompt info
    filepath: Where to save the .md file

##### `get_prompt_list()`

Get list of available prompts with metadata

##### `get_prompt()`

Get full prompt data by filename

##### `set_active_prompt()`

Set the active custom prompt

##### `clear_active_prompt()`

Clear active prompt (use default)

##### `get_translate_prompt()`

Get the translate_prompt from active prompt, or None if using default

##### `get_proofread_prompt()`

Get the proofread_prompt from active prompt, or None if using default

##### `search_prompts()`

Search prompts by name, description, or domain

##### `create_new_prompt()`

Create a new prompt and save as .svprompt

Args:
    prompt_type: Either 'system_prompt' or 'custom_instruction'
    task_type: Type of translation task

##### `update_prompt()`

Update an existing prompt

##### `delete_prompt()`

Delete a custom prompt

##### `export_prompt()`

Export a prompt to a specific location

##### `import_prompt()`

Import a prompt from an external file

Args:
    import_path: Path to JSON file to import
    prompt_type: Either 'system_prompt' or 'custom_instruction'

##### `convert_json_to_markdown()`

Convert all JSON files in directory to Markdown format.

Args:
    directory: Path to directory containing .json files
    prompt_type: Either 'system_prompt' or 'custom_instruction'
    
Returns:
    tuple: (converted_count, failed_count)

##### `convert_all_prompts_to_markdown()`

Convert all JSON prompts to Markdown format in both directories.

Returns:
    dict: {"system_prompts": (converted, failed), "custom_instructions": (converted, failed)}


---

## Functions

### `get_user_data_path()`

**Line:** 23

Get path to user_data folder, handling DEV_MODE.
This is imported from the main module's implementation.

---

