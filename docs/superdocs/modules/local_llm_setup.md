# local_llm_setup

**File:** `modules/local_llm_setup.py`
**Lines:** 1,104
**Classes:** 5
**Functions:** 4

---

## Module Description

Local LLM Setup Module for Supervertaler
=========================================

Provides setup wizard, status checking, and model management for local LLM
integration via Ollama.

Features:
- Ollama installation detection and guidance
- Hardware detection (RAM, GPU) for model recommendations
- Model download and management
- Connection testing

Usage:
    from modules.local_llm_setup import LocalLLMSetupDialog, check_ollama_status
    
    # Check if Ollama is running
    status = check_ollama_status()
    if status['running']:
        print(f"Ollama running with models: {status['models']}")
    
    # Show setup wizard
    dialog = LocalLLMSetupDialog(parent)
    dialog.exec()

Author: Supervertaler Team
Date: December 2025

---

## Classes

### `ModelDownloadWorker`

**Line:** 424

Background worker for downloading Ollama models.

#### Methods

##### `cancel()`

No docstring

##### `run()`

Download model using Ollama API.


---

### `ConnectionTestWorker`

**Line:** 490

Background worker for testing Ollama connection with a simple prompt.

#### Methods

##### `run()`

Test model with a simple translation prompt.


---

### `LocalLLMSetupDialog`

**Line:** 542

Setup wizard for local LLM configuration.

Guides users through:
1. Checking if Ollama is installed and running
2. Detecting hardware specs
3. Recommending and downloading a model
4. Testing the connection

#### Methods

##### `init_ui()`

Initialize the UI.

##### `refresh_status()`

Refresh Ollama status and hardware specs.

##### `on_model_selected()`

Update model info when selection changes.

##### `open_ollama_download()`

Open Ollama download page.

##### `start_ollama()`

Start the Ollama service.

##### `download_model()`

Start downloading the selected model.

##### `cancel_download()`

Cancel ongoing download.

##### `on_download_progress()`

Update download progress.

##### `on_download_finished()`

Handle download completion.

##### `test_connection()`

Test the selected model with a simple translation.

##### `on_test_finished()`

Handle test completion.

##### `closeEvent()`

Handle dialog close - cancel any running workers.


---

### `LocalLLMStatusWidget`

**Line:** 959

Compact status widget for embedding in settings panel.
Shows Ollama status and provides quick access to setup.

#### Methods

##### `init_ui()`

Initialize the compact UI.

##### `refresh_status()`

Refresh Ollama status.

##### `on_model_changed()`

Emit signal when model selection changes.

##### `show_setup_dialog()`

Show the full setup dialog.

##### `get_selected_model()`

Get currently selected model ID.

##### `set_selected_model()`

Set the selected model.


---

### `MEMORYSTATUSEX`

**Line:** 329

No docstring

---

## Functions

### `get_ollama_endpoint()`

**Line:** 214

Get Ollama endpoint from environment or return default.

---

### `check_ollama_status()`

**Line:** 219

Check if Ollama is running and get available models.

Args:
    endpoint: Ollama API endpoint (default: http://localhost:11434)
    
Returns:
    Dict with:
        - running: bool - whether Ollama is running
        - models: list - available model names  
        - version: str - Ollama version if available
        - error: str - error message if not running

---

### `detect_system_specs()`

**Line:** 295

Detect system hardware specifications.

Returns:
    Dict with:
        - ram_gb: Total RAM in GB
        - gpu_name: GPU name if detected
        - gpu_vram_gb: GPU VRAM in GB if detected
        - os_name: Operating system name
        - recommended_model: Suggested model based on specs

---

### `get_model_recommendations()`

**Line:** 386

Get model recommendations based on available RAM.

Args:
    ram_gb: Available RAM in gigabytes
    
Returns:
    List of model dicts sorted by recommendation priority

---

