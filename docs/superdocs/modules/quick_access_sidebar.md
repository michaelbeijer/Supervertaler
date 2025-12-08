# quick_access_sidebar

**File:** `modules/quick_access_sidebar.py`
**Lines:** 282
**Classes:** 3
**Functions:** 0

---

## Module Description

Quick Access Sidebar - memoQ-style left navigation panel

Provides quick access to common actions, recent files, and project navigation.

Author: Michael Beijer
License: MIT

---

## Classes

### `QuickActionButton`

**Line:** 18

A button for quick actions in the sidebar

#### Methods


---

### `SidebarSection`

**Line:** 48

A collapsible section in the sidebar

#### Methods

##### `add_button()`

Add a quick action button to this section

##### `toggle_collapsed()`

Toggle section collapsed state


---

### `QuickAccessSidebar`

**Line:** 111

Left sidebar with quick access to common functions

#### Methods

##### `build_default_sections()`

Build default sidebar sections

##### `add_section()`

Add a section to the sidebar

##### `update_recent_files()`

Update recent files list

##### `on_recent_file_clicked()`

Handle recent file double-click


---

