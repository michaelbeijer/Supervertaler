# encoding_repair_Qt

**File:** `modules/encoding_repair_Qt.py`
**Lines:** 393
**Classes:** 2
**Functions:** 0

---

## Module Description

Encoding Repair Module - Qt Edition
Embeddable version of the text encoding repair tool for detecting and fixing mojibake/encoding corruption

This module can be embedded in the main Supervertaler Qt application as a tab.
Can also be run independently as a standalone application.

---

## Classes

### `EncodingRepairQt`

**Line:** 28

Encoding Repair feature - detect and fix text encoding corruption (mojibake)
Can be embedded in any PyQt6 application as a tab or panel

#### Methods

##### `log_message()`

Log a message to the parent app's log if available

##### `create_tab()`

Create the Encoding Repair tab UI

Args:
    parent: The QWidget container for the tab


---

### `StandaloneApp`

**Line:** 369

Minimal parent app for standalone mode

#### Methods

##### `log()`

Simple log method for standalone mode


---

