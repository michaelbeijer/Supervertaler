# ribbon_widget

**File:** `modules/ribbon_widget.py`
**Lines:** 597
**Classes:** 6
**Functions:** 0

---

## Module Description

Ribbon Widget - Modern Office-style ribbon interface for Supervertaler Qt

Provides context-sensitive ribbon tabs with grouped tool buttons,
similar to memoQ, Trados Studio, and Microsoft Office applications.

Author: Michael Beijer
License: MIT

---

## Classes

### `RibbonButton`

**Line:** 19

A ribbon-style tool button with icon and text

#### Methods

##### `set_group_color()`

Set the group color for this button


---

### `RibbonGroup`

**Line:** 103

A group of related ribbon buttons with a title

#### Methods

##### `set_tab_color()`

Set the tab color for this group and update styling

##### `add_button()`

Add a button to this group and apply group color

##### `add_buttons()`

Add multiple buttons to this group


---

### `RibbonTab`

**Line:** 174

A single ribbon tab containing multiple groups

#### Methods

##### `set_tab_color()`

Set the color theme for this ribbon tab

##### `add_group()`

Add a group to this ribbon tab

##### `add_stretch()`

Add stretch to push groups to the left


---

### `ColoredTabBar`

**Line:** 220

Custom QTabBar that supports per-tab background colors

#### Methods

##### `set_tab_color()`

Set the background color for a specific tab

##### `paintEvent()`

Override paint event to draw custom tab colors


---

### `RibbonWidget`

**Line:** 284

Main ribbon widget with multiple context-sensitive tabs

#### Methods

##### `add_ribbon_tab()`

Add a ribbon tab with color coding

##### `apply_initial_colors()`

Apply colors to all tabs after they're all added

##### `get_tab()`

Get a ribbon tab by name

##### `create_collapse_button()`

Create a collapse/expand button - more visible and better positioned

##### `toggle_collapse()`

Toggle ribbon between expanded and collapsed states

##### `create_button()`

Helper to create a ribbon button with action connection


---

### `RibbonBuilder`

**Line:** 544

Helper class to build ribbon interfaces declaratively

#### Methods

##### `build_home_ribbon()`

Build the Home ribbon tab

##### `build_translation_ribbon()`

Build the Translation ribbon tab

##### `build_tools_ribbon()`

Build the Tools ribbon tab


---

