# Match Display Improvements - Side-by-Side Source/Target

## Overview

The Translation Results Panel now displays matches in a professional side-by-side layout, mimicking memoQ's design. Each match shows both source and target text for easy comparison.

## Visual Layout

### Match Item Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  #1  TM  95%                                                    │
│                                                                  │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐ │
│  │ Source (Light Blue)      │  │ Target (Light Green)         │ │
│  │                          │  │                              │ │
│  │ "In order to protect     │  │ "Voor de bescherming         │ │
│  │  the system against      │  │  van het systeem tegen       │ │
│  │  viruses..."             │  │  virussen..."                │ │
│  └──────────────────────────┘  └──────────────────────────────┘ │
│                                                                  │
│ Context: Medical device documentation...                         │
└─────────────────────────────────────────────────────────────────┘
```

### Color Coding

- **Header Bar:**
  - Match number (#1, #2, etc.) - Blue
  - Match type badge (TM) - Blue
  - Relevance percentage (95%) - Gray

- **Source Panel:**
  - Background: Light blue (#f0f8ff)
  - Border: Light blue border
  - Provides context for understanding differences

- **Target Panel:**
  - Background: Light green (#f0fff0)
  - Border: Light green border
  - Shows the suggested translation

### Information Displayed

| Element | Display | Purpose |
|---------|---------|---------|
| Match Number | #1, #2, #3... | Quick reference for Ctrl+# shortcuts |
| Type | NT, MT, TM, Termbases | Source of the match |
| Relevance | 95%, 100%, etc. | Match quality indicator |
| Source Text | Left panel | Comparison with current segment |
| Target Text | Right panel | Actual translation to use |
| Context | Below panels | Additional metadata from TM |

## Benefits Over Previous Design

### ✅ Before (Target Only)
```
┌──────────────────────────┐
│ #1  TM  95%              │
│                          │
│ "For de bescherming      │
│  van het systeem tegen   │
│  virussen..."            │
│                          │
│ Context: Medical...      │
└──────────────────────────┘
```
**Issues:**
- Source text not visible - hard to verify match accuracy
- Can't compare differences between current and TM source
- Single-language view

### ✅ After (Source + Target Side-by-Side)
```
┌──────────────────────────────────────────────────────┐
│ #1  TM  95%                                          │
│                                                      │
│ ┌────────────────────┐  ┌──────────────────────────┐ │
│ │ Source             │  │ Target                   │ │
│ │                    │  │                          │ │
│ │ "In order to       │  │ "Voor de bescherming    │ │
│ │  protect the       │  │  van het systeem       │ │
│ │  system against    │  │  tegen virussen..."    │ │
│ │  viruses..."       │  │                          │ │
│ └────────────────────┘  └──────────────────────────┘ │
│                                                      │
│ Context: Medical device documentation...            │
└──────────────────────────────────────────────────────┘
```

**Improvements:**
- ✅ Can visually compare source differences
- ✅ Professional bilingual layout
- ✅ Easy to spot fuzzy match variations
- ✅ Better for quality assurance
- ✅ Matches memoQ's familiar design

## User Workflow Impact

### Scenario: Verifying a Fuzzy Match

**Before:**
1. See "95% match"
2. Can't see source text - have to trust match score
3. Must manually check current segment source in grid
4. Back-and-forth switching between panels

**After:**
1. See "95% match" with both source and target
2. Immediately compare both sides
3. Spot the differences in source
4. Understand why it's 95%, not 100%
5. Make informed decision to accept or skip

## Implementation Details

### CompactMatchItem Widget

Each match is rendered as a `CompactMatchItem` with:

1. **Header Row:**
   - Match number label
   - Type badge
   - Relevance percentage

2. **Content Row (Horizontal Layout):**
   - **Source Frame (50% width):**
     - Blue background
     - Source text with word wrapping
     - Max 30px height
   - **Target Frame (50% width):**
     - Green background
     - Target text with word wrapping
     - Max 30px height

3. **Metadata Row:**
   - Context information (if available)

### Styling Features

```python
# Source panel styling
background-color: #f0f8ff  # Alice blue
border: 1px solid #b0d4ff  # Powder blue
border-radius: 2px
padding: 4px

# Target panel styling
background-color: #f0fff0  # Honeydew
border: 1px solid #b0ffb0  # Pale green
border-radius: 2px
padding: 4px
```

### Responsive Text Wrapping

- Both source and target text wrap at word boundaries
- Maximum height of 30px ensures compact display
- Font size: 8pt for optimal readability
- Overflow hidden with ellipsis if needed

## Advantages Over Compact-Only View

| Aspect | Compact-Only | Side-by-Side |
|--------|--------------|-------------|
| **Visibility** | Target text only | Source + Target |
| **Comparison** | Manual lookup needed | Visual comparison |
| **Quality Check** | Requires switching | Immediate verification |
| **Professional** | Basic | memoQ-like |
| **Space Usage** | Very compact | Slightly larger |
| **Learning Curve** | Low | Very low (standard layout) |

## Match Selection and Insertion

When you click a match or navigate with arrow keys:

1. **Selected Match Highlighted:**
   - Blue background (#0066cc)
   - White text
   - Both source and target remain visible

2. **Compare Box Updates:**
   - Current Source → Left compare box
   - TM Source → Middle compare box
   - TM Target → Right compare box

3. **Ready for Insertion:**
   - Press Enter to insert target text
   - Or use Ctrl+# shortcut

## Accessibility Notes

- High contrast between panels (blue vs green)
- Clear text sizing
- Logical left-to-right layout
- Matches Western language conventions
- Works with screen readers (accessible labels)

## Future Enhancements

Possible improvements:
1. **Diff Highlighting:** Highlight differences between source and current
2. **Resizable Panels:** Drag divider to adjust source/target width
3. **Inline Edit:** Edit source/target inline before accepting
4. **Context Panel:** Toggle to show full context
5. **Visual Diff:** Color-coded changes (added, removed, modified)

## Configuration

The side-by-side layout is hardcoded but can be made configurable:

```python
# Potential future settings:
LAYOUT_MODE = "side-by-side"  # or "stacked", "compact"
SOURCE_WIDTH_RATIO = 50  # 50% width
TARGET_WIDTH_RATIO = 50  # 50% width
SHOW_CONTEXT = True
CONTEXT_LINES = 2
```

## Performance

- **Rendering:** No performance impact (same number of widgets)
- **Memory:** Minimal increase (same widget hierarchy)
- **Responsiveness:** Instant navigation with arrow keys
- **Scrolling:** Smooth even with many matches

## Browser/CAT Tool Compatibility

This design is compatible with:
- ✅ memoQ's match display
- ✅ SDL Trados Studio
- ✅ Memsource
- ✅ Across
- ✅ OmegaT
- ✅ CafeTran

Provides familiar workflow for translators switching from other tools.
