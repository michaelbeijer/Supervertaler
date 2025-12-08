# llm_clients

**File:** `modules/llm_clients.py`
**Lines:** 1,242
**Classes:** 2
**Functions:** 7

---

## Module Description

LLM Clients Module for Supervertaler
=====================================

Specialized independent module for interacting with various LLM providers.
Can be used standalone or imported by other applications.

Supported Providers:
- OpenAI (GPT-4, GPT-4o, GPT-5, o1, o3)
- Anthropic (Claude Sonnet 4.5, Haiku 4.5, Opus 4.1)
- Google (Gemini 2.5 Flash, 2.5 Pro, 3 Pro Preview)

Claude 4 Models (Released 2025):
- Sonnet 4.5: Best balance - flagship model for general translation ($3/$15 per MTok)
- Haiku 4.5: Fast & affordable - 2x speed, 1/3 cost of Sonnet ($1/$5 per MTok)
- Opus 4.1: Premium quality - complex legal/technical translation ($15/$75 per MTok)

Temperature Handling:
- Reasoning models (GPT-5, o1, o3): temperature parameter OMITTED (not supported)
- Standard models: temperature=0.3

Usage:
    from modules.llm_clients import LLMClient

    # Use default (Sonnet 4.5)
    client = LLMClient(api_key="your-key", provider="claude")

    # Or specify model
    client = LLMClient(api_key="your-key", provider="claude", model="claude-haiku-4-5-20251001")

    response = client.translate("Hello world", source_lang="en", target_lang="nl")

---

## Classes

### `LLMConfig`

**Line:** 113

Configuration for LLM client

---

### `LLMClient`

**Line:** 122

Universal LLM client for translation tasks

#### Methods

##### `get_claude_model_info()`

Get information about available Claude models

Args:
    model_id: Specific model ID to get info for, or None for all models

Returns:
    Dict with model information

Example:
    # Get all models
    models = LLMClient.get_claude_model_info()
    for model_id, info in models.items():
        print(f"{info['name']}: {info['description']}")

    # Get specific model
    info = LLMClient.get_claude_model_info("claude-sonnet-4-5-20250929")
    print(info['use_case'])

##### `get_ollama_model_info()`

Get information about available Ollama models

Args:
    model_id: Specific model ID to get info for, or None for all models
    
Returns:
    Dict with model information

##### `check_ollama_status()`

Check if Ollama is running and get available models

Args:
    endpoint: Ollama API endpoint (default: http://localhost:11434)
    
Returns:
    Dict with:
        - running: bool - whether Ollama is running
        - models: list - available model names
        - error: str - error message if not running

##### `model_supports_vision()`

Check if a model supports vision (image) inputs

Args:
    provider: Provider name ("openai", "claude", "gemini")
    model_name: Model identifier
    
Returns:
    True if model supports vision, False otherwise

##### `translate()`

Translate text using configured LLM

Args:
    text: Text to translate
    source_lang: Source language code
    target_lang: Target language code
    context: Optional context for translation
    custom_prompt: Optional custom prompt (overrides default simple prompt)

Returns:
    Translated text


---

## Functions

### `load_api_keys()`

**Line:** 39

Load API keys from api_keys.txt file (supports both root and user_data_private locations)

---

### `main()`

**Line:** 992

Example standalone usage of LLM client

---

### `get_openai_translation()`

**Line:** 1017

Get OpenAI translation with metadata

Args:
    text: Text to translate
    source_lang: Source language name
    target_lang: Target language name
    context: Optional context for better translation

Returns:
    Dict with translation, model, and metadata

---

### `get_claude_translation()`

**Line:** 1067

Get Claude translation with metadata

Args:
    text: Text to translate
    source_lang: Source language name
    target_lang: Target language name
    context: Optional context for better translation

Returns:
    Dict with translation, model, and metadata

---

### `get_google_translation()`

**Line:** 1153

Get Google Cloud Translation API translation with metadata

Args:
    text: Text to translate
    source_lang: Source language code (e.g., 'en', 'nl', 'auto')
    target_lang: Target language code (e.g., 'en', 'nl')

Returns:
    Dict with translation, confidence, and metadata

---

