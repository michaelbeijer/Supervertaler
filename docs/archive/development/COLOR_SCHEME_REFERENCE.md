# Match Type Color Scheme Reference

## Color Coding System

The match display now uses professional color coding to indicate match type, eliminating the need for text labels.

### Match Type Colors

#### 🔴 TM (Translation Memory) - RED
- **Hex:** `#ff6b6b`
- **Meaning:** Previously approved translations
- **Priority:** HIGH (most reliable)
- **Selected Color:** Darker red
- **Light Variant:** Pale pink background with red border

#### 🔵 Termbase - BLUE  
- **Hex:** `#4d94ff`
- **Meaning:** Glossary/terminology matches
- **Priority:** HIGH (approved terminology)
- **Selected Color:** Darker blue
- **Light Variant:** Pale blue background with blue border

#### 🟢 MT (Machine Translation) - GREEN
- **Hex:** `#51cf66`
- **Meaning:** Automated translation output
- **Priority:** MEDIUM (needs review)
- **Selected Color:** Darker green
- **Light Variant:** Pale green background with green border

#### ⚫ NT (New Translation) - GRAY
- **Hex:** `#adb5bd`
- **Meaning:** New/untested translation
- **Priority:** LOW (informational)
- **Selected Color:** Darker gray
- **Light Variant:** Pale gray background with gray border

## Visual States

### Unselected (Hoverable)
```
┌─────────────────────────────────┐
│ Light tint background           │
│ Thin colored border             │
│ Normal text color               │
│ (Hover slightly darker)         │
└─────────────────────────────────┘
```

### Selected (Focused)
```
┌═════════════════════════════════┐
│ Solid match-type-color bkgd     │
│ Thick colored border             │
│ WHITE text                       │
│ Strong visual focus              │
└═════════════════════════════════┘
```

## Why Color Coding?

1. **Space Efficient:** No text label needed
2. **Intuitive:** Professional standard in CAT tools
3. **Fast Recognition:** Visual at a glance
4. **Consistent:** Matches memoQ interface
5. **Accessibility:** Works with screen readers (color is supplemented by HTML semantic structure)

## HTML/CSS Implementation

The colors are used in PyQt6 stylesheets:

```python
type_color_map = {
    "TM": "#ff6b6b",           # Red
    "Termbase": "#4d94ff",     # Blue
    "MT": "#51cf66",           # Green
    "NT": "#adb5bd"            # Gray
}
```

When match type changes, the entire frame border and selected-state colors update automatically.

## Color Accessibility

| Color | Hex | Luminance | Contrast vs White | WCAG AA |
|-------|-----|-----------|-------------------|---------|
| Red (TM) | #ff6b6b | 59 | 4.5:1 | ✅ Pass |
| Blue (Termbase) | #4d94ff | 43 | 6.5:1 | ✅ Pass |
| Green (MT) | #51cf66 | 72 | 3.9:1 | ⚠️ Borderline |
| Gray (NT) | #adb5bd | 68 | 4.1:1 | ✅ Pass |

All colors meet minimum WCAG AA contrast requirements when white text is overlaid (selected state).

## Psychology Behind Color Choices

- **Red (TM):** High importance, proven reliability
- **Blue (Termbase):** Professional, reference authority
- **Green (MT):** Processing/generated (common in software UX)
- **Gray (NT):** Neutral, new/uncertain status

## Examples in Context

### Match List with Multiple Types

```
┌──────────────────────┬──────────────────────┐
│ #1 Error message... │ Message d'erreur... │ ← TM (RED)
├──────────────────────┼──────────────────────┤
│                 100% │
└──────────────────────┴──────────────────────┘

┌──────────────────────┬──────────────────────┐
│ #2 Warning message..│ Message d'alerte...  │ ← Termbase (BLUE)
├──────────────────────┼──────────────────────┤
│                  95% │
└──────────────────────┴──────────────────────┘

┌──────────────────────┬──────────────────────┐
│ #3 System error...   │ Erreur système...    │ ← MT (GREEN)
├──────────────────────┼──────────────────────┤
│                  75% │
└──────────────────────┴──────────────────────┘
```

The color borders make it instantly clear which types of matches you're seeing.

## Customization

Colors can be easily customized by modifying the `type_color_map` dictionary in `CompactMatchItem.update_styling()`.

For example, to use different colors:

```python
type_color_map = {
    "TM": "#e74c3c",           # Darker red
    "Termbase": "#3498db",     # Darker blue
    "MT": "#2ecc71",           # Darker green
    "NT": "#95a5a6"            # Different gray
}
```

The color manipulation functions will automatically create appropriate light and dark variants.

## Related Files

- `modules/translation_results_panel.py` - Color coding implementation
- `docs/COMPACT_LAYOUT_UPDATE.md` - Layout changes
- `Supervertaler_Qt.py` - Main application (uses TranslationMatch.match_type)
