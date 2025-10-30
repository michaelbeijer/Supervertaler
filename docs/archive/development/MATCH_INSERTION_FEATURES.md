# Match Insertion Features - memoQ-Style Functionality

## Overview

Supervertaler Qt now supports professional match insertion workflows inspired by memoQ, enabling rapid segment translation through keyboard shortcuts and match selection.

## Key Features Implemented

### 1. Match Numbering Display
- Each match in the Translation Results Panel is numbered sequentially (#1, #2, #3, etc.)
- Number appears at the beginning of each match item
- Makes keyboard shortcuts intuitive and discoverable

### 2. Keyboard Navigation (Arrow Keys)
**Usage:**
- Press **Up Arrow** - Navigate to previous match
- Press **Down Arrow** - Navigate to next match

**Behavior:**
- Selection highlighted in blue with white text
- Automatically scrolls match list to keep selection visible
- Works within each match type section (NT, MT, TM, Termbases)
- Provides continuous workflow without mouse interaction

### 3. Insert with Enter Key
**Usage:**
- Select a match (click or arrow keys)
- Press **Enter** or **Return**

**Result:**
- Match text is inserted into the currently selected target cell
- Current segment's target is replaced with match text
- Application automatically advances to the next segment
- Green log message confirms insertion: "✓ Match inserted into segment N target"

### 4. Quick Insert by Number (Ctrl+1 through Ctrl+9)
**Usage:**
- Press **Ctrl+1** to insert match #1
- Press **Ctrl+2** to insert match #2
- ... up to **Ctrl+9** for match #9

**Behavior:**
- Works globally across all match sections (NT, MT, TM, Termbases)
- No need to select match first - goes directly to insertion
- Automatically selects and highlights the match being inserted
- Emits insertion signal, replacing target and advancing segment

**Example Workflow:**
```
User sees 4 matches in Translation Results Panel
Presses Ctrl+1 → First match inserted into target
Presses Ctrl+2 → Second match inserted (if user backs up)
Presses Ctrl+3 → Third match inserted
```

### 5. Compare Box (Vertical Stacked Layout)
**Changes from Previous Implementation:**
- Boxes now stack **vertically** instead of horizontally
- Much better for reading longer text content
- Three resizable sections:
  1. Current Source (blue background) - Source of current segment
  2. TM Source (yellow background) - Source from translation memory match
  3. TM Target (green background) - Target from translation memory match

**Resizing:**
- Drag divider between boxes to resize sections
- Default proportions: 33% each
- Hover over divider for blue highlight showing it's resizable
- Each box can be sized independently based on content

### 6. Match Selection UI Improvements
**Visual Feedback:**
- Unselected matches: Light gray background with dark border
- Hover state: Light blue background with blue border
- Selected matches: Dark blue background (#0066cc) with white text

**Match Information Displayed:**
- Match number (e.g., #1, #2, #3)
- Match type badge (NT, MT, TM, Termbases)
- Relevance percentage (e.g., 95%, 85%)
- Target text (line-wrapped for readability)
- Context information (if available from TM)

### 7. Notes Section Enhancement
**Purpose:**
The Notes area is for **segment-level annotations**, allowing translators to:
- Add translation concerns or special handling instructions
- Record terminology notes
- Document quality assurance comments
- Store context or reference information

**Features:**
- Compact 50-pixel height (expandable via splitter)
- Placeholder text guides user: "Add notes about this segment, context, or translation concerns..."
- Persisted with segment data
- Displayed when segment is selected

## Complete Match Insertion Workflow

### Scenario 1: Sequential Translation with Keyboard
```
1. Click segment in grid → Matches load in right panel
2. Press Down arrow → First match highlighted
3. Press Enter → Match inserted, move to next segment
4. Repeat with arrow navigation and Enter
```

### Scenario 2: Rapid Selection by Number
```
1. See 4 matches in panel
2. Ctrl+1 → Insert match 1 if good
3. Next segment loaded
4. Ctrl+3 → Insert match 3 for next segment
5. Continue rapidly through document
```

### Scenario 3: Mixed Navigation
```
1. Click match with mouse → Selected and highlighted
2. Down arrow twice → Move to different match
3. Enter → Insert that match
4. Compare different options before committing
```

### Scenario 4: Compare Before Insertion
```
1. Select a TM match → Compare box appears
2. Review Current Source vs TM Source vs TM Target
3. Resize compare boxes for better visibility
4. Press Enter when satisfied with choice
```

## Keyboard Shortcut Reference

| Shortcut | Action |
|----------|--------|
| **↑ (Up)** | Navigate to previous match |
| **↓ (Down)** | Navigate to next match |
| **Enter** | Insert selected match into target |
| **Ctrl+1** | Insert match #1 directly |
| **Ctrl+2** | Insert match #2 directly |
| **Ctrl+3** | Insert match #3 directly |
| **Ctrl+4** | Insert match #4 directly |
| **Ctrl+5** | Insert match #5 directly |
| **Ctrl+6** | Insert match #6 directly |
| **Ctrl+7** | Insert match #7 directly |
| **Ctrl+8** | Insert match #8 directly |
| **Ctrl+9** | Insert match #9 directly |

## Code Architecture

### TranslationResultsPanel Class
**Signals:**
- `match_selected(TranslationMatch)` - Emitted when match is selected (for highlighting, compare boxes)
- `match_inserted(str)` - Emitted when match should be inserted into target

**Key Methods:**
- `set_matches(matches_dict)` - Populate panel with matches
- `set_segment_info(segment_num, source_text)` - Update segment display
- `keyPressEvent(event)` - Handle all keyboard shortcuts
- `navigate(direction)` - Arrow key navigation
- `select_by_number(number)` - Direct number selection

### MatchSection Class
**Manages:**
- Individual match type sections (NT, MT, TM, Termbases)
- Collapsible headers with match count
- Selection tracking per section
- Navigation within section

### CompactMatchItem Class
**Features:**
- Compact memoQ-style display
- Match numbering
- Selection state styling
- Drag/drop support
- Click-to-select with signal emission

## Performance Considerations

1. **Keyboard Response:** Near-instant keyboard navigation (no network latency)
2. **Memory Efficient:** Selection state tracked per section
3. **Rendering:** Matches lazily scrolled in scroll area
4. **Focus Management:** Strong focus policy ensures keyboard events always captured

## Future Enhancements

Potential additions (not implemented yet):
1. **Concatenate Matches:** Ctrl+Shift+1+2 to combine multiple matches
2. **Fuzzy Match Auto-Accept:** Auto-insert 100% matches without user confirmation
3. **Context Menu:** Right-click for additional insertion options (append, prepend, replace)
4. **Diff Highlighting:** Visual diff between current source and TM source
5. **Custom Scoring:** User-adjustable relevance weighting
6. **Match Statistics:** Track which matches were inserted, ignore rate, etc.

## Integration Points

**Main Application (Supervertaler_Qt.py):**
- `on_match_inserted(match_text)` - Handles insertion into grid
- Updates segment target text
- Advances to next segment
- Logs insertion action

**Grid Integration:**
- Works with current cell selection
- Validates target column context
- Updates model and UI atomically

**Database Integration:**
- Matches loaded from TM database
- Segment notes persisted with segment
- Match metadata available in compare boxes

## User Experience Flow Diagram

```
┌─ Click Segment in Grid ─┐
│                          ↓
│               Load Matches in Panel
│               Show Match Numbers
│                          ↓
├─ Option 1: Arrow Keys + Enter
│  ↓ Press Down Arrow → Select Next Match
│  ↓ Press Enter → Insert Match
│  ↓ Move to Next Segment
│  └─ Repeat
│
├─ Option 2: Ctrl+Number
│  ↓ Press Ctrl+1 → Insert Match #1
│  ↓ Automatically Advance
│  └─ Repeat
│
├─ Option 3: Mouse + Keyboard
│  ↓ Click Match to Select
│  ↓ Review in Compare Box
│  ↓ Press Enter to Confirm
│  └─ Move to Next Segment
│
└─ All paths lead to: Segment target updated + Next segment loaded

```

## Notes for Translators

- **Speed:** Keyboard shortcuts are fastest (Ctrl+1, Ctrl+2, etc.)
- **Accuracy:** Use arrow keys to review multiple matches before pressing Enter
- **Context:** Check Compare Box before inserting to verify match quality
- **Notes:** Add annotations to segments for future reference or QA
- **Workflow:** Mix arrow navigation and number shortcuts for optimal speed
