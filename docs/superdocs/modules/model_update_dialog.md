# model_update_dialog

**File:** `modules/model_update_dialog.py`
**Lines:** 381
**Classes:** 3
**Functions:** 0

---

## Module Description

Model Update Dialog for Supervertaler
======================================

Dialog window that displays new LLM models detected by the version checker.
Allows users to easily add new models to their configuration.

Features:
- Shows new models grouped by provider
- Click to select models to add
- One-click "Add Selected" button
- Shows model details when available

---

## Classes

### `ModelUpdateDialog`

**Line:** 24

Dialog for showing and adding new models

#### Methods

##### `init_ui()`

Initialize the user interface

##### `get_selected_models()`

Get the selected models


---

### `NoNewModelsDialog`

**Line:** 244

Simple dialog shown when no new models are found

#### Methods

##### `init_ui()`

Initialize UI


---

### `CheckmarkCheckBox`

**Line:** 304

Custom checkbox with green background and white checkmark when checked

#### Methods

##### `paintEvent()`

Override paint event to draw white checkmark when checked


---

