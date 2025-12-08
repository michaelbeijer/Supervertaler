# prompt_assistant

**File:** `modules/prompt_assistant.py`
**Lines:** 357
**Classes:** 1
**Functions:** 0

---

## Module Description

AI Prompt Assistant Module

Provides AI-powered prompt modification through natural language conversation.
Part of Phase 1 implementation for v4.0.0-beta.

Features:
- Conversational prompt modification
- Visual diff generation
- Prompt versioning
- Chat history tracking

---

## Classes

### `PromptAssistant`

**Line:** 20

AI-powered prompt modification and learning system

#### Methods

##### `set_llm_client()`

Set or update the LLM client

##### `send_message()`

Send a message to the LLM and get a response (for Style Guides chat).

Args:
    system_prompt: System prompt to use for context
    user_message: User's message
    callback: Optional callback function to handle response (called with response text)

Returns:
    Response text or None if LLM not available

##### `suggest_modification()`

AI suggests changes to a prompt based on user request.

Args:
    prompt_name: Name of the prompt being modified
    current_prompt: Current content of the prompt
    user_request: User's natural language request for modification

Returns:
    Dictionary containing:
    - explanation: Why the changes were made
    - modified_prompt: New version of the prompt
    - changes_summary: List of key changes
    - diff: Unified diff showing changes
    - success: Boolean indicating if modification succeeded

##### `generate_diff()`

Generate unified diff between two prompts.

Args:
    original: Original prompt text
    modified: Modified prompt text

Returns:
    Unified diff string

##### `generate_diff_html()`

Generate line-by-line diff suitable for colored display.

Args:
    original: Original prompt text
    modified: Modified prompt text

Returns:
    List of tuples (change_type, line) where change_type is:
    - 'equal': unchanged line
    - 'delete': removed line
    - 'insert': added line
    - 'replace': modified line

##### `get_chat_history()`

Get the chat history

##### `clear_chat_history()`

Clear the chat history

##### `get_modification_history()`

Get the modification history

##### `undo_last_modification()`

Get the previous version of the prompt for undo functionality.

Returns:
    Dictionary with original prompt info, or None if no history

##### `export_chat_session()`

Export chat history and modifications to a file.

Args:
    filepath: Path to save the session data


---

