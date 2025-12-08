# unified_prompt_manager_qt

**File:** `modules/unified_prompt_manager_qt.py`
**Lines:** 2,952
**Classes:** 2
**Functions:** 0

---

## Module Description

Unified Prompt Manager Module - Qt Edition
Simplified 2-Layer Architecture:

1. System Templates (in Settings) - mode-specific, auto-selected based on document type
2. Prompt Library (main UI) - unified workspace with folders, favorites, multi-attach

This replaces the old 4-layer system (System/Domain/Project/Style Guides).

---

## Classes

### `ChatMessageDelegate`

**Line:** 33

Custom delegate for rendering chat messages with proper bubble styling

#### Methods

##### `sizeHint()`

Calculate size needed for this message

##### `paint()`

Paint the chat message bubble


---

### `UnifiedPromptManagerQt`

**Line:** 364

Unified Prompt Manager - Single-tab interface with:
- Tree view with nested folders
- Favorites and Quick Run menu
- Multi-attach capability
- Active prompt configuration panel

#### Methods

##### `log_message()`

Log a message through parent app or print

##### `create_tab()`

Create the Prompt Manager tab UI with sub-tabs

Args:
    parent_widget: Widget to add the tab to (will set its layout)

##### `refresh_context()`

Public method to refresh AI Assistant context.
Call this from the main app when document/project changes.

##### `get_system_template()`

Get system template for specified mode

##### `set_mode()`

Set current translation mode (single, batch_docx, batch_bilingual)

##### `build_final_prompt()`

Build final prompt for translation using 2-layer architecture:
1. System Template (auto-selected by mode)
2. Combined prompts from library (primary + attached)

Args:
    source_text: Text to translate
    source_lang: Source language
    target_lang: Target language
    mode: Override mode (if None, uses self.current_mode)

Returns:
    Complete prompt ready for LLM

##### `generate_markdown_for_current_document()`

Public method to generate markdown for the current document.
Called by main app when auto-markdown is enabled.

Returns:
    True if markdown was generated successfully, False otherwise

##### `refresh_llm_client()`

Refresh LLM client when settings change


---

