# Quick Reference: Filter Features

## Keyboard Shortcuts

### Filter Operations
- **Ctrl+M** - Toggle between Filter Mode and Highlight Mode
- **Ctrl+Shift+A** - Apply current filters
- **Ctrl+Shift+F** - Focus source filter field
- **Enter** (in filter fields) - Apply filters

### View Switching
- **Ctrl+1** - Grid View
- **Ctrl+2** - List View
- **Ctrl+3** - Document View

---

## Filter Modes Explained

### 🔍 Filter Mode (Default)
- Shows **only** segments that match your filters
- Example: Filter for "contract" → See only segments containing "contract"
- Results: "🔍 Showing 25 of 150 segments"

### 💡 Highlight Mode
- Shows **all** segments
- Highlights matching segments in bright yellow
- Example: Filter for "contract" → See all 150 segments, 25 highlighted
- Results: "💡 Highlighting 25 of 150 segments"

**Toggle with Ctrl+M**

---

## Filter Panel Locations

| View | Filter Panel Location |
|------|----------------------|
| **Grid View** | Top of screen, above grid |
| **List View** | Top of screen, above tree |
| **Document View** | Top of screen, above document |

All three views use the **same filters** - switching views keeps your filters active!

---

## How to Filter

### Basic Filtering
1. Type text in **Source** or **Target** fields
2. Select status from **Status** dropdown (optional)
3. Click **🔍 Apply** button (or press Enter in filter field)

### Quick Workflow
1. Type your search terms
2. Press **Enter** to apply
3. Press **Ctrl+M** to toggle mode if needed
4. Press **✕ Clear** to remove filters

---

## Document View Highlighting

In Document View, matching segments are highlighted with:
- **Bright yellow background** (#FFEB3B)
- **Solid 2px border** for visibility
- Works in both paragraphs and table cells

This makes it easy to:
- Spot matches in document flow
- See context around matches
- Verify translations in place

---

## Saved Filter Preferences

When you save a project, these are remembered:
- ✅ Filter Mode (Filter or Highlight)
- ✅ Source filter text
- ✅ Target filter text
- ✅ Status selection
- ✅ Whether filters were active

**Next time you open the project** → Filters automatically restored!

---

## Tips & Tricks

### Tip 1: Context Viewing
Working in Filter Mode but need to see context?
- Press **Ctrl+M** to switch to Highlight Mode
- See all segments with your matches highlighted
- Press **Ctrl+M** again to return to Filter Mode

### Tip 2: Fast Filtering
- Use **Ctrl+Shift+F** to jump to filter field
- Type your search
- Press **Enter** to apply
- No mouse needed!

### Tip 3: Status Filtering
- Set Status to "untranslated" to see what needs work
- Set Status to "draft" to review your progress
- Combine with text filters for precise results

### Tip 4: Keyboard Navigation
- Filter to specific segments
- Use **Ctrl+Down/Up** to navigate through them
- Edit inline with **F2**
- All without touching the mouse!

### Tip 5: Document View Review
- Switch to Document View (Ctrl+3)
- Apply your filters
- See matches highlighted in natural document flow
- Click any highlighted segment to edit

---

## Filter Combinations

### Find Untranslated Legal Terms
```
Source: "contract"
Target: (empty)
Status: untranslated
Mode: Filter
```
Result: Only untranslated segments containing "contract"

### Review All "Patient" Translations
```
Source: "patient"
Target: (empty)
Status: All
Mode: Highlight
```
Result: All segments shown, "patient" segments highlighted

### Check Specific Status
```
Source: (empty)
Target: (empty)
Status: draft
Mode: Filter
```
Result: Only draft segments shown

### Find Missing Translations
```
Source: "important"
Target: (empty - or specific term)
Status: untranslated
Mode: Filter
```
Result: Untranslated segments with "important" in source

---

## Menu Access

All filter functions available in **View** menu:
```
View → Toggle Filter Mode       (Ctrl+M)
View → Apply Filters            (Ctrl+Shift+A)
View → Clear Filters
View → Focus Filter             (Ctrl+Shift+F)
```

---

## Common Questions

**Q: Do filters work in all views?**
A: Yes! The same filters apply in Grid View, List View, and Document View.

**Q: Are my filters saved?**
A: Yes! When you save your project, filter settings are saved too.

**Q: What's the difference between Filter and Highlight modes?**
A: Filter shows only matches. Highlight shows everything and highlights matches.

**Q: Can I use Enter to apply filters?**
A: Yes! Press Enter in any filter field to apply filters.

**Q: How do I clear all filters?**
A: Click the "✕ Clear" button or use View → Clear Filters.

**Q: Can I filter by multiple criteria?**
A: Yes! All active filters must match (AND logic). Source + Target + Status all apply together.

---

## Version
CAT Editor Prototype v0.4.0 - October 3, 2025
