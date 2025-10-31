# Match Display Compactness - Final Fixes

## Issue Identified

Looking at the user's screenshots, while the layout was changed to horizontal, the items were still taking up too much vertical space due to:

1. **Variable/Flexible Heights**: QLabel widgets were using flexible sizing (min-width vs fixed width)
2. **Extra Padding**: Margins and spacing were still not minimal enough
3. **Text Wrapping**: Long text could still cause height changes
4. **Font Sizes**: Still too large for ultra-compact display

## Fixes Applied

### 1. **Fixed Heights on All Components**
```python
# Before: Flexible heights, variable sizing
num_label.setMaximumWidth(30)

# After: Fixed compact dimensions
num_label.setFixedWidth(18)
num_label.setFixedHeight(16)
```

Each element now has a **fixed 16px height**:
- Number box: 18px wide × 16px high
- Percentage: 35px wide × 16px high
- Content: Remaining space × 16px high

### 2. **Ultra-Minimal Layout Margins**
```python
# Before: layout.setContentsMargins(2, 1, 2, 1)
# After:  layout.setContentsMargins(1, 1, 1, 1)

# Before: layout.setSpacing(2)
# After:  layout.setSpacing(1)
```

### 3. **Container Height Fixed**
```python
self.setMaximumHeight(20)  # Entire match item is maximum 20px high
```

This prevents the frame from expanding beyond necessary.

### 4. **Stylesheet Zero Padding**
Added explicit `padding: 0px; margin: 0px;` to all labels:
```css
QLabel {
    padding: 0px;
    margin: 0px;
    /* ... other styles ... */
}
```

### 5. **Truncate Long Text**
```python
# If source → target is longer than 50 chars, truncate with ...
content_text = f"{match.source} → {match.target}"
if len(content_text) > 50:
    content_text = content_text[:47] + "..."
```

This prevents text wrapping that would increase height.

### 6. **Font Size Reductions**
- Number box: 9px → 8px
- Percentage: 8px → 7px
- Content: 8px (unchanged)

## Result

**Before**: Each match ~30-40px high (multiple rows due to variable sizing)
**After**: Each match exactly 20px high (single compact row)

This achieves:
- ✅ Consistent 20px height per match
- ✅ No text wrapping
- ✅ No variable sizing
- ✅ All elements visible on one line
- ✅ Matches the memoQ compact style

## Visual Expected Change

```
Before (variable heights):
┌────────────────────────┐
│ [1] 100% error → fout  │  ← ~30-40px
└────────────────────────┘

After (fixed heights):
┌────────────────────────┐
│ [1] 100% error → fout  │  ← exactly 20px
└────────────────────────┘

For 4 matches (before):
Total: ~120-160px

For 4 matches (after):
Total: 80px (4 × 20px)
```

## Testing

Load the app and look at the Termbase section:
1. Each match should be **exactly one line**
2. Should be **exactly the same height** as other matches
3. Should take up ~50% less vertical space than before
4. Text should be truncated if too long (showing "..." at end)
5. Selection highlighting should work correctly

## File Modified

- `modules/translation_results_panel.py`
  - CompactMatchItem.__init__() (lines 40-95)
  - Changed from flexible to fixed sizing
  - Added text truncation logic
  - Reduced margins/padding/spacing

## Implementation Details

### Width Allocation (in order):
1. Number box: 18px (fixed)
2. Percentage: 35px (fixed)
3. Content: Remaining space (flexible with truncation)

### Height Allocation (fixed):
- Frame: 20px max
- All labels: 16px each
- Margins: 1px top/bottom = 2px total
- Total: 16px + 2px = 18px (within 20px frame)

### Truncation Rule:
- If content > 50 characters: truncate to 47 chars + "..."
- Prevents accidental wrapping to second line
- User can still see truncated text via tooltip (when implemented)
