# translation_results_panel

**File:** `modules/translation_results_panel.py`
**Lines:** 1,638
**Classes:** 4
**Functions:** 0

---

## Module Description

Translation Results Panel
Compact memoQ-style right-side panel for displaying translation matches
Supports stacked match sections, drag/drop, and compare boxes with diff highlighting

Keyboard Shortcuts:
- ↑/↓ arrows: Navigate through matches (cycle through sections)
- Spacebar/Enter: Insert currently selected match into target cell
- Ctrl+1-9: Insert specific match directly (by number, global across all sections)
- Escape: Deselect match (when focus on panel)

Compare boxes: Vertical stacked with resizable splitter
Text display: Supports long segments with text wrapping

---

## Classes

### `TranslationMatch`

**Line:** 27

Represents a single translation match

---

### `CompactMatchItem`

**Line:** 38

Compact match display (like memoQ) with source and target in separate columns

#### Methods

##### `update_tag_color()`

Update tag highlight color for this item

##### `set_font_size()`

Set the font size for all match items

##### `update_font_size()`

Update font size for this item

##### `mousePressEvent()`

Emit signal when clicked

##### `select()`

Select this match

##### `deselect()`

Deselect this match

##### `update_styling()`

Update visual styling based on selection state and match type

##### `mouseMoveEvent()`

Support drag/drop


---

### `MatchSection`

**Line:** 492

Stacked section for a match type (NT/MT/TM/Termbases)

#### Methods

##### `select_by_number()`

Select match by number (1-based)

##### `navigate()`

Navigate matches: direction=1 for next, -1 for previous


---

### `TranslationResultsPanel`

**Line:** 609

Main translation results panel (right side of editor)
Compact memoQ-style design with stacked match sections

Features:
- Keyboard navigation: Up/Down arrows to cycle through matches
- Insert selected match: Press Enter
- Quick insert by number: Ctrl+1 through Ctrl+9 (1-based index)
- Vertical compare boxes with resizable splitter
- Match numbering display
- Zoom controls for both match list and compare boxes

#### Methods

##### `setup_ui()`

Setup the UI

##### `add_matches()`

Add new matches to existing matches (for progressive loading)
Merges new matches with existing ones and re-renders the display
Includes deduplication to prevent showing identical matches

Args:
    new_matches_dict: Dict with keys like "NT", "MT", "TM", "Termbases"

##### `set_matches()`

Set matches from different sources in unified flat list with GLOBAL consecutive numbering
(memoQ-style: single grid, color coding only identifies match type)

Args:
    matches_dict: Dict with keys like "NT", "MT", "TM", "Termbases"

##### `set_segment_info()`

Update segment info display

##### `clear()`

Clear all matches

##### `get_selected_match()`

Get currently selected match

##### `set_font_size()`

Set font size for all match items (for zoom control)

##### `set_compare_box_font_size()`

Set font size for compare boxes

##### `set_show_tags()`

Set whether to show HTML/XML tags in matches

##### `set_tag_color()`

Set tag highlight color for all match items

##### `zoom_in()`

Increase font size for both match list and compare boxes

##### `zoom_out()`

Decrease font size for both match list and compare boxes

##### `reset_zoom()`

Reset font size to defaults

##### `select_previous_match()`

Navigate to previous match (Ctrl+Up from main window)

##### `select_next_match()`

Navigate to next match (Ctrl+Down from main window)

##### `insert_match_by_number()`

Insert match by its number (1-based index) - for Ctrl+1-9 shortcuts

##### `insert_selected_match()`

Insert currently selected match (Ctrl+Space)

##### `keyPressEvent()`

Handle keyboard events for navigation and insertion

Shortcuts:
- Up/Down arrows: Navigate matches (plain arrows, no Ctrl)
- Spacebar: Insert selected match into target
- Return/Enter: Insert selected match into target
- Ctrl+Space: Insert selected match (alternative)
- Ctrl+1 to Ctrl+9: Insert specific match by number (global)

Note: Ctrl+Up/Down are handled at main window level for grid navigation


---

