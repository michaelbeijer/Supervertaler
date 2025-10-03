# What's New in CAT Editor v0.4.1

## 🎯 Quick Summary

**Version 0.4.1** brings precise search highlighting and comprehensive filtering across all view modes. Search for specific terms and see them highlighted in bright yellow - not the entire sentence, just the words you're looking for!

---

## ✨ New Features

### 1. Precise Search Term Highlighting
**What Changed**: Instead of highlighting entire sentences, now only your search terms are highlighted.

**Before**:
```
[Entire sentence in yellow]
This contract establishes the terms and conditions.
```

**After**:
```
This contract establishes the terms and conditions.
     ^^^^^^^^ (only "contract" is bright yellow)
```

**Why It Matters**: 
- See exactly what matched your search
- Read the context around matches
- Spot multiple occurrences in the same sentence
- Much cleaner and more professional

---

### 2. Filter Panel in All Views
**What's New**: Document View now has the same filter panel as Grid View and List View.

**Features**:
- Filter by source text, target text, or status
- Two modes: Filter (show only matches) or Highlight (show all, highlight matches)
- Results counter shows how many segments match
- Click "🔍 Apply" or press Enter to filter

**Switch Views**:
- Grid View: `Ctrl+1` - Spreadsheet-like interface
- List View: `Ctrl+2` - Compact tree view
- Document View: `Ctrl+3` - Natural document flow

Filters work the same in all three views!

---

### 3. Keyboard Shortcuts for Speed
**New Shortcuts**:
- `Ctrl+M` - Toggle between Filter Mode (🔍) and Highlight Mode (💡)
- `Ctrl+Shift+A` - Apply your filters
- `Ctrl+Shift+F` - Jump to the source filter field
- `Enter` - Apply filters (while in a filter field)

**Example Workflow**:
1. Press `Ctrl+Shift+F` to jump to filter
2. Type "contract"
3. Press `Enter` to apply
4. Press `Ctrl+3` to see in Document View
5. See "contract" highlighted throughout document

---

### 4. Your Filters Are Saved
**What Happens**: When you save your project, your filter settings are saved too.

**What's Saved**:
- Your search terms (source and target)
- Selected status (untranslated, draft, etc.)
- Filter mode (Filter or Highlight)
- Whether filters were active

**Next Time**: Open your project and your filters are exactly as you left them. No need to re-enter your search terms!

---

### 5. Better Control Over Filtering
**What Changed**: Filters no longer apply automatically while you type.

**How It Works Now**:
1. Type your search terms
2. Click "🔍 Apply" or press Enter
3. Filters are applied

**Why**: Better performance and you control when filtering happens.

---

## 📖 How to Use

### Basic Filtering
1. Open a document (or load a project)
2. Look for the filter panel at the top
3. Type what you want to find in "Source" or "Target"
4. Click "🔍 Apply" (or press Enter)

### Two Filter Modes

**🔍 Filter Mode** (default):
- Shows only segments that match
- Example: Search for "contract" → See only 25 of 150 segments
- Perfect for focused work

**💡 Highlight Mode**:
- Shows all segments
- Highlights matching terms in bright yellow
- Example: Search for "contract" → See all 150 segments, "contract" highlighted
- Perfect for reviewing in context

**Switch with** `Ctrl+M`

---

## 🎨 What You'll See

### In Document View
Your document looks natural (like Word), with:
- Paragraphs in normal flow
- Tables rendered as actual tables
- Color-coded status (red=untranslated, yellow=draft, green=translated, blue=approved)
- **Search terms in bright yellow with bold font**

### In Grid View
Excel-like spreadsheet with:
- 6 columns: ID, Type, Style, Status, Source, Target
- Filtered rows based on your search
- Yellow highlighting in source/target cells

### In List View
Compact tree view with:
- Filtered list of segments
- Quick overview of structure
- Edit panel below

---

## 💡 Tips & Tricks

### Tip 1: Quick Context Check
Working in Filter Mode but need to see full context?
- Press `Ctrl+M` to switch to Highlight Mode
- See all segments with your search terms highlighted
- Press `Ctrl+M` again to go back

### Tip 2: Find All Untranslated Terms
1. Type "important" in source filter
2. Select "untranslated" in status dropdown
3. Press Enter
4. See only untranslated segments containing "important"

### Tip 3: Review Consistency
1. Press `Ctrl+M` for Highlight Mode
2. Type "patient" in source filter
3. Press Enter
4. Scroll through document
5. See all uses of "patient" highlighted
6. Check if translation is consistent

### Tip 4: Keyboard-Only Workflow
1. `Ctrl+Shift+F` - Jump to filter
2. Type your search
3. `Enter` - Apply
4. `Ctrl+3` - Document View
5. Click a segment to edit
6. `Ctrl+Enter` - Save and next

---

## 🆚 Filter Mode vs Highlight Mode

### When to Use Filter Mode
- Translating specific terms
- Working on untranslated segments only
- Focused, distraction-free work
- Smaller subset of segments

### When to Use Highlight Mode
- Reviewing document consistency
- Checking term usage
- Need to see full context
- Making global decisions

---

## 🚀 Getting Started

### First Time?
1. Import a document (`Ctrl+O`)
2. Try searching for a common word
3. Click "🔍 Apply"
4. See the results!
5. Try `Ctrl+M` to toggle modes
6. Switch views with `Ctrl+1`, `Ctrl+2`, `Ctrl+3`

### Already Have Projects?
- Your old projects work perfectly
- Load them as usual (`Ctrl+L`)
- Start using filters
- Filters will be saved when you save the project

---

## 📚 More Information

### Quick References
- **FILTER_QUICK_REFERENCE.md** - Detailed filter guide
- **README.md** - Full feature list
- **QUICK_START.md** - Getting started guide

### Keyboard Shortcuts
All shortcuts listed in README.md

### Support
Check the documentation files in the `cat_tool_prototype` folder.

---

## 🎉 Enjoy!

The new filtering features make it easier to:
- Find specific terms quickly
- Review translations in context
- Work efficiently with keyboard shortcuts
- Resume exactly where you left off

**Happy translating!** 🌍

---

**Version**: 0.4.1
**Release Date**: October 3, 2025
