# setup_wizard

**File:** `modules/setup_wizard.py`
**Lines:** 353
**Classes:** 2
**Functions:** 0

---

## Module Description

Setup Wizard for Supervertaler First Launch
Guides new users to select their user_data folder location.

Author: Michael Beijer
License: MIT

---

## Classes

### `SetupWizard`

**Line:** 17

First-launch setup wizard for Supervertaler.

Guides users through:
1. Welcome and explanation
2. Folder selection
3. Migration of existing data (if applicable)
4. Confirmation

#### Methods

##### `run()`

Run the full setup wizard.

Returns:
    Tuple of (success: bool, user_data_path: str)


---

### `SetupWizardWindow`

**Line:** 226

Alternative: Full window-based setup wizard (more elegant, optional).
Can be used instead of dialog-based approach.

#### Methods

##### `run()`

Run the window-based wizard.


---

