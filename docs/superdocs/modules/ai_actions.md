# ai_actions

**File:** `modules/ai_actions.py`
**Lines:** 964
**Classes:** 1
**Functions:** 0

---

## Module Description

AI Actions Module

Provides structured action interface for AI Assistant to interact with Supervertaler
resources (Prompt Library, Translation Memories, Termbases).

Phase 2 of AI Assistant Enhancement Plan:
- Parses ACTION markers from AI responses
- Executes actions on prompt library
- Returns structured results for display

Action Format:
ACTION:function_name
PARAMS:{"param1": "value1", "param2": "value2"}

Example:
ACTION:list_prompts
PARAMS:{"folder": "Domain Expertise"}

ACTION:create_prompt
PARAMS:{"name": "Medical Translator", "content": "...", "folder": "Domain Expertise"}

---

## Classes

### `AIActionSystem`

**Line:** 30

Handles parsing and execution of AI actions on Supervertaler resources.

#### Methods

##### `parse_and_execute()`

Parse AI response for ACTION markers and execute actions.

Args:
    ai_response: Full response text from AI

Returns:
    Tuple of (cleaned_response, list of action results)
    cleaned_response: AI response with ACTION blocks removed
    action_results: List of {action, params, success, result/error}

##### `execute_action()`

Execute a single action with given parameters.

Args:
    action_name: Name of the action
    params: Dictionary of parameters

Returns:
    Dictionary with action result: {action, params, success, result/error}

##### `get_system_prompt_addition()`

Get text to add to AI system prompt to enable action usage.

Returns:
    String to append to AI system prompt

##### `format_action_results()`

Format action results for display in chat.

Args:
    action_results: List of action result dictionaries

Returns:
    Formatted string for display


---

