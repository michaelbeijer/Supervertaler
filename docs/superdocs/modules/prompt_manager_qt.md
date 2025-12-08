# prompt_manager_qt

**File:** `modules/prompt_manager_qt.py`
**Lines:** 4,370
**Classes:** 7
**Functions:** 0

---

## Module Description

Prompt Manager Module - Qt Edition
4-Layer Prompt Architecture for maximum translation/proofreading/copywriting precision

Layers:
1. System Prompts (hardcoded - always included: memoQ tags, formatting rules)
2. Domain Prompts (domain-specific translation prompts)
3. Project Prompts (project-specific rules)
4. Style Guides (language-specific formatting guidelines)
5. Prompt Assistant (AI-powered prompt refinement)

This module can be embedded in the main Supervertaler Qt application as a tab.

---

## Classes

### `AnalysisUpdateEvent`

**Line:** 30

Custom event for updating UI after analysis completes

#### Methods


---

### `PromptManagerQt`

**Line:** 42

Prompt Manager feature - manage System Prompts, Domain Prompts, Project Prompts, and Style Guides
Can be embedded in any PyQt6 application as a tab or panel

#### Methods

##### `log_message()`

Log a message to the parent app's log if available

##### `create_tab()`

Create the Prompt Manager tab UI

Args:
    parent: The QWidget container for the tab


---

### `CheckmarkCheckBox`

**Line:** 3597

Custom checkbox with green background and white checkmark when checked

#### Methods

##### `paintEvent()`

Override paint event to draw white checkmark when checked

##### `get_system_prompt()`

Get the System Prompt (Layer 1 - always included)
Contains memoQ tags, formatting rules, etc.

Args:
    mode: "single", "batch_docx", or "batch_bilingual"

Returns:
    System Prompt string (Layer 1)

##### `build_final_prompt()`

Build final prompt using 4-layer architecture

Args:
    source_text: Text to translate
    source_lang: Source language name
    target_lang: Target language name
    mode: Translation mode ("single", "batch_docx", "batch_bilingual")

Returns:
    Complete prompt string ready to send to LLM


---

### `AssistantTabWidget`

**Line:** 659

No docstring

#### Methods

##### `event()`

Handle custom events from background threads


---

### `DummySegment`

**Line:** 1457

No docstring

---

### `PromptGenCompleteEvent`

**Line:** 3418

No docstring

#### Methods


---

### `PromptGenErrorEvent`

**Line:** 3474

No docstring

#### Methods


---

