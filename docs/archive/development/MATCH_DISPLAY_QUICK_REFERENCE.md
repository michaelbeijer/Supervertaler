# Match Display Quick Reference

## Understanding the Match Panel

### What Do the Colors Mean?

When you see matches in the right panel, the **border color** tells you the match type:

| Color | Type | Meaning |
|-------|------|---------|
| 🔴 **RED** | TM | Translation Memory (previously approved, most reliable) |
| 🔵 **BLUE** | Termbase | Glossary/approved terminology |
| 🟢 **GREEN** | MT | Machine Translation (auto-generated) |
| ⚫ **GRAY** | NT | New Translation (never used before) |

### Reading a Match

```
┌──────────────────────────┬──────────────────────────┐
│ #1 English text here...  │ Dutch translation...    │
├──────────────────────────┼──────────────────────────┤
│                                                100% │
└──────────────────────────┴──────────────────────────┘
 ▲                                                ▲
 Match number (use Ctrl+1 to insert)          Match quality %
 
Border = RED (TM match)
Left side = English source text
Right side = Dutch target translation
```

## Keyboard Shortcuts

### Navigation
- **↑** (Up arrow) - Previous match
- **↓** (Down arrow) - Next match

### Insertion
- **Enter** - Insert currently selected match
- **Ctrl+1** through **Ctrl+9** - Insert match #1 through #9 directly

### Example Workflow

1. View 3-4 matches at once (all visible on screen)
2. Press **↓** to navigate down, **↑** to go back
3. Selected match highlights in color
4. Press **Enter** to insert
5. Automatically moves to next segment

OR

1. See match #3 is perfect
2. Press **Ctrl+3** to insert directly
3. Done!

## Why No Labels?

Old version had "Source" and "Target" text labels - **wasted space**. 

Now it's **obvious:**
- **Left box** (light blue) = Source text
- **Right box** (light green) = Translation

This saves ~75% of space, so you can see **4-5 matches** instead of **1-2**.

## Color Psychology

- 🔴 **RED (TM)** = ⚡ Premium content (previously approved)
- 🔵 **BLUE (Termbase)** = 📚 Reference/terminology
- 🟢 **GREEN (MT)** = 🤖 Computer-generated (review needed)
- ⚫ **GRAY (NT)** = ❓ Unknown (new suggestion)

**Rule of Thumb:**
- Red matches usually need **no review** (already approved)
- Blue matches provide **terminology consistency**
- Green matches need **review/editing**
- Gray matches are **experimental**

## Example Panel

```
Panel: Translation Memory Matches

┌──────────────────────────┬──────────────────────────┐
│ #1 Network error         │ Netwerkfout              │ RED (TM)
├──────────────────────────┼──────────────────────────┤
│                                                100% │
└──────────────────────────┴──────────────────────────┘

┌──────────────────────────┬──────────────────────────┐
│ #2 Error handling system │ Foutbehandelingssysteem  │ BLUE (Termbase)
├──────────────────────────┼──────────────────────────┤
│                                                 95% │
└──────────────────────────┴──────────────────────────┘

┌──────────────────────────┬──────────────────────────┐
│ #3 System processing...  │ Systeemverwerking...    │ GREEN (MT)
├──────────────────────────┼──────────────────────────┤
│                                                 75% │
└──────────────────────────┴──────────────────────────┘
```

**Scenario:**
- Press **↓** to move to match #2 (blue becomes highlighted)
- That's terminology, so insert it
- Press **Enter** - inserted into target column
- Next segment loads automatically

## Matching Workflow

### Pro Tip: Color-Scan Strategy

1. **Scan for RED** → Usually copy directly (100% matches)
2. **Check BLUE** → Ensure terminology is consistent
3. **Review GREEN** → May need editing (machine translation)
4. **Ignore GRAY** → Experimental suggestions

### Statistics

If you can see 4 matches at once:
- ✅ Faster decision making
- ✅ Less scrolling
- ✅ Better overview
- ✅ More efficient workflow

## The Percentage

The number on the right (like "95%") is **match quality**:

- **100%** = Exact match (identical previous translation)
- **95-99%** = Fuzzy match (very similar, minor changes)
- **75-94%** = Context match (similar context, some differences)
- **50-75%** = Partial match (some relevant content)

**100% matches** usually need no editing.
**Lower % matches** need review/editing.

## Tips & Tricks

### Fast Insertion
Instead of navigating with arrows, use keyboard numbers:
- See match #2 is perfect → Press **Ctrl+2** instantly
- No navigation needed!

### Comparison
- Left box shows original source
- Right box shows translation
- Instantly compare them while deciding

### Keyboard-Only Workflow
1. **Ctrl+1** - Try first match
2. Doesn't fit? Press **Ctrl+Z** (undo)
3. **Ctrl+2** - Try second match
4. Perfect! Move to next segment automatically

### Multiple Language Pairs
Color coding is consistent across all language pairs:
- RED always = TM
- BLUE always = Termbase  
- GREEN always = MT
- GRAY always = NT

No relearning needed!

## Troubleshooting

### "I don't see any matches"
- Segment might be new or very different from TM
- Check search filters
- Try adjusting fuzzy match threshold

### "Match #3 won't insert"
- Make sure target column is active (highlighted blue in grid)
- Click on target cell first
- Then press Ctrl+3

### "Numbers aren't visible"
- Check monitor brightness/contrast
- All matches should show #1, #2, #3, etc. on the left
- If not visible, might be rendering issue

## Related Shortcuts

The match panel works with these main shortcuts:
- **Ctrl+1-9** = Insert match by number (global)
- **Enter** = Insert selected match (if panel focused)
- **↑↓** = Navigate matches (if panel focused)
- **Tab** = Switch focus to grid

## Professional Comparison

This layout matches **memoQ 9** and **Trados Studio**, industry-standard CAT tools. The color-coding system is:
- Intuitive for professionals
- Faster than text labels
- Consistent across tools
- Professional appearance

---

**Remember:** The colors + position make it obvious what's what. No need to read labels = faster workflow! 🚀
