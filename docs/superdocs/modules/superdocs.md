# superdocs

**File:** `modules/superdocs.py`
**Lines:** 543
**Classes:** 1
**Functions:** 1

---

## Module Description

Superdocs - Automated Documentation Generator for Supervertaler
================================================================

Automatically generates and maintains living documentation by:
- Scanning Python source files
- Extracting classes, functions, and docstrings
- Creating markdown documentation
- Mapping module dependencies
- Generating architecture overview

Usage:
    from modules.superdocs import Superdocs

    docs = Superdocs()
    docs.generate_all()  # Generate complete documentation

Output:
    docs/superdocs/
        index.md              # Overview and table of contents
        architecture.md       # System architecture
        modules/              # Per-module documentation
        dependencies.md       # Module dependency graph

---

## Classes

### `Superdocs`

**Line:** 34

Automated documentation generator for Supervertaler codebase

#### Methods

##### `generate_all()`

Generate complete documentation suite


---

## Functions

### `main()`

**Line:** 536

Command-line interface for Superdocs

---

