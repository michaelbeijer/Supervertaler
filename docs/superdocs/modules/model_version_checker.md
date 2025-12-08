# model_version_checker

**File:** `modules/model_version_checker.py`
**Lines:** 373
**Classes:** 1
**Functions:** 0

---

## Module Description

Model Version Checker for Supervertaler
========================================

Automatically checks for new LLM models from OpenAI, Anthropic, and Google.
Notifies users when new models are available and provides easy addition interface.

Features:
- Once-per-day automatic checking (configurable)
- Manual check button
- Popup dialog showing new models
- Easy click-to-add interface
- Caches results to avoid unnecessary API calls

Usage:
    from modules.model_version_checker import ModelVersionChecker

    checker = ModelVersionChecker(cache_path="user_data/model_cache.json")
    new_models = checker.check_for_new_models(
        openai_key="...",
        anthropic_key="...",
        google_key="..."
    )

---

## Classes

### `ModelVersionChecker`

**Line:** 33

Check for new models from LLM providers

#### Methods

##### `should_check()`

Check if we should run the version check

Returns:
    True if more than 24 hours since last check, or never checked

##### `check_openai_models()`

Check for new OpenAI models

Args:
    api_key: OpenAI API key

Returns:
    (list of new model IDs, error message if any)

##### `check_claude_models()`

Check for new Claude models

Note: Anthropic doesn't provide a models.list() endpoint, so we try
to call the API with common model naming patterns and see what works.

Args:
    api_key: Anthropic API key

Returns:
    (list of new model IDs, error message if any)

##### `check_gemini_models()`

Check for new Gemini models

Args:
    api_key: Google AI API key

Returns:
    (list of new model IDs, error message if any)

##### `check_all_providers()`

Check all providers for new models

Args:
    openai_key: OpenAI API key
    anthropic_key: Anthropic API key
    google_key: Google AI API key
    force: Force check even if checked recently

Returns:
    Dictionary with results per provider:
    {
        "openai": {"new_models": [...], "error": None},
        "claude": {"new_models": [...], "error": None},
        "gemini": {"new_models": [...], "error": None},
        "checked": True
    }

##### `has_new_models()`

Check if any new models were found

Args:
    results: Results from check_all_providers()

Returns:
    True if any new models found

##### `get_cache_info()`

Get information about the cache


---

