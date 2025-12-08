# theme_manager

**File:** `modules/theme_manager.py`
**Lines:** 454
**Classes:** 2
**Functions:** 0

---

## Module Description

Theme Manager
=============
Manages UI themes and color schemes for Supervertaler Qt.
Allows users to customize the appearance of the entire application.

Features:
- Predefined themes (Light, Dark, Sepia, High Contrast)
- Custom theme creation and editing
- Save/load user themes
- Apply themes to all UI elements

---

## Classes

### `Theme`

**Line:** 23

Theme definition with all UI colors

#### Methods

##### `to_dict()`

Convert theme to dictionary

##### `from_dict()`

Create theme from dictionary


---

### `ThemeManager`

**Line:** 79

Manages application themes

#### Methods

##### `get_all_themes()`

Get all available themes (predefined + custom)

##### `get_theme()`

Get theme by name

##### `set_theme()`

Set current theme

Args:
    name: Theme name
    
Returns:
    True if theme was found and applied

##### `save_custom_theme()`

Save a custom theme

##### `delete_custom_theme()`

Delete a custom theme

##### `load_custom_themes()`

Load custom themes from file

##### `apply_theme()`

Apply current theme to application

Args:
    app: QApplication instance


---

