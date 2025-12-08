# superbench_ui

**File:** `modules/superbench_ui.py`
**Lines:** 1,319
**Classes:** 4
**Functions:** 0

---

## Module Description

Superbench - Qt UI Components
==============================

PyQt6 user interface for LLM translation benchmarking.

Features:
- Test dataset selection
- Model selection (checkboxes)
- Benchmark execution with progress
- Results table with comparison
- Summary statistics panel
- Export functionality

Author: Michael Beijer
License: MIT

---

## Classes

### `CheckmarkCheckBox`

**Line:** 44

Custom checkbox with green background and white checkmark when checked

#### Methods

##### `paintEvent()`

Override paint event to draw white checkmark when checked


---

### `CustomRadioButton`

**Line:** 126

Custom radio button with square indicator, green when checked, white checkmark

#### Methods

##### `paintEvent()`

Override paint event to draw white checkmark when checked


---

### `BenchmarkThread`

**Line:** 208

Background thread for running benchmarks without blocking UI

#### Methods

##### `run()`

Run benchmark in background thread


---

### `LLMLeaderboardUI`

**Line:** 247

Main UI widget for Superbench

#### Methods

##### `init_ui()`

Initialize the user interface

##### `log()`

Append message to log output and auto-scroll to bottom


---

