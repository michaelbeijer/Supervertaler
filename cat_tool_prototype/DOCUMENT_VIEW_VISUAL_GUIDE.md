# Document View - Visual Guide

**Version**: v0.4.0  
**Date**: October 3, 2025

---

## Overview

This guide provides a visual reference for the Document View feature, showing how it transforms the translation workflow.

---

## The Four View Modes

### Grid View (Ctrl+1)
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📊 Grid View - Excel-like Table                                             │
├────┬──────┬──────────┬─────────────┬──────────────────────┬─────────────────┤
│ ID │ Type │ Style    │ Status      │ Source               │ Target          │
├────┼──────┼──────────┼─────────────┼──────────────────────┼─────────────────┤
│ 1  │ Para │ Heading 1│ Translated  │ Introduction         │ Inleiding       │
│ 2  │ Para │ Normal   │ Draft       │ This is a sentence.  │ Dit is een...   │
│ 3  │ T1R1C1│ Normal  │ Untranslated│ Cell content         │                 │
└────┴──────┴──────────┴─────────────┴──────────────────────┴─────────────────┘

Best for: Bulk editing, overview, status management
```

### Split View (Ctrl+2)
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📋 Split View - Traditional CAT Layout                                      │
├───────────────────────────┬─────────────────────────────────────────────────┤
│ Segment List (Left 40%)   │ Editor Panel (Right 60%)                        │
│                           │                                                 │
│ ┌───────────────────────┐ │ ┌─────────────────────────────────────────────┐│
│ │ 1. Introduction       │ │ │ Segment #2 │ Para │ Normal                  ││
│ │ 2. This is a sent...  │◄┼─┤ Status: [Draft ▼]                           ││
│ │ 3. Cell content       │ │ │                                             ││
│ │                       │ │ │ Source:                                     ││
│ └───────────────────────┘ │ │ This is a sentence about the topic.         ││
│                           │ │                                             ││
│                           │ │ Target:                                     ││
│                           │ │ ┌─────────────────────────────────────────┐ ││
│                           │ │ │Dit is een zin over het onderwerp.       │ ││
│                           │ │ └─────────────────────────────────────────┘ ││
│                           │ │                                             ││
│                           │ │ [Copy Source] [Clear] [Save & Next]         ││
│                           │ └─────────────────────────────────────────────┘│
└───────────────────────────┴─────────────────────────────────────────────────┘

Best for: Focused translation, sequential work
```

### Document View (Ctrl+4) ⭐ NEW
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📖 Document View - Natural Flow                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ Document (Top 60% - Scrollable)                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │   Introduction                                    <- Heading 1 (16pt)   │ │
│ │                                                                          │ │
│ │   This is a sentence about the topic. This is another sentence that     │ │
│ │   flows naturally. The text wraps properly and maintains readability.   │ │
│ │                                                                          │ │
│ │   Summary Table                                   <- Heading 2 (14pt)   │ │
│ │                                                                          │ │
│ │   ┌──────────────────────┬──────────────────────┬──────────────────┐   │ │
│ │   │ Header 1             │ Header 2             │ Header 3         │   │ │
│ │   ├──────────────────────┼──────────────────────┼──────────────────┤   │ │
│ │   │ Cell content here    │ More content         │ Final column     │   │ │
│ │   └──────────────────────┴──────────────────────┴──────────────────┘   │ │
│ │                                                                          │ │
│ │   Additional paragraph text continues after the table.                  │ │
│ │                                                                          │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ Editor Panel (Bottom 40%)                                                   │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Segment #2 │ Para │ Normal                        Status: [Draft ▼]    │ │
│ │                                                                          │ │
│ │ Source:                                                                  │ │
│ │ This is a sentence about the topic.                                      │ │
│ │                                                                          │ │
│ │ Target:                                                                  │ │
│ │ ┌──────────────────────────────────────────────────────────────────────┐│ │
│ │ │Dit is een zin over het onderwerp.                                    ││ │
│ │ └──────────────────────────────────────────────────────────────────────┘│ │
│ │                                                                          │ │
│ │ [Copy Source → Target] [Clear] [Save]                                   │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

Best for: Context, review, natural reading, table structure
```

---

## Document View Features

### 1. Status Color Coding

```
┌─────────────────────────────────────────────────────────────────┐
│  Introduction                                                    │
│                                                                  │
│  This is untranslated.    <- Red tint (#ffe6e6)                 │
│                                                                  │
│  This is a draft.         <- Yellow tint (#fff9e6)              │
│                                                                  │
│  This is translated.      <- Green tint (#e6ffe6)               │
│                                                                  │
│  This is approved.        <- Blue tint (#e6f3ff)                │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Smart Placeholders

**Scenario A: Untranslated (shows source for context)**
```
┌─────────────────────────────────────────────────────────────────┐
│  The quick brown fox jumps over the lazy dog.                   │
│  ^                                                               │
│  └─ Source text shown because no translation yet                │
└─────────────────────────────────────────────────────────────────┘
Status: Untranslated
Display: Source text (red tint)
```

**Scenario B: Translated (shows target)**
```
┌─────────────────────────────────────────────────────────────────┐
│  De snelle bruine vos springt over de luie hond.                │
│  ^                                                               │
│  └─ Target translation shown                                    │
└─────────────────────────────────────────────────────────────────┘
Status: Translated
Display: Target text (green tint)
```

**Scenario C: Cleared (shows placeholder)**
```
┌─────────────────────────────────────────────────────────────────┐
│  [empty - click to edit]                                        │
│  ^                                                               │
│  └─ Placeholder because user cleared the translation            │
└─────────────────────────────────────────────────────────────────┘
Status: Draft
Display: Placeholder (yellow tint)
```

### 3. Table Rendering

**Before v0.4.0 (Tables at end)**
```
┌─────────────────────────────────────────────────────────────────┐
│  Introduction paragraph.                                         │
│  More content here.                                              │
│  Conclusion paragraph.                                           │
│                                                                  │
│  [All tables appear here at the end, out of order]              │
│  Table Cell 1,1                                                  │
│  Table Cell 1,2                                                  │
│  Table Cell 2,1                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**After v0.4.0 (Tables in correct position)**
```
┌─────────────────────────────────────────────────────────────────┐
│  Introduction paragraph.                                         │
│                                                                  │
│  ┌──────────────────────┬──────────────────────┐                │
│  │ Cell 1,1             │ Cell 1,2             │ <- Table here  │
│  ├──────────────────────┼──────────────────────┤                │
│  │ Cell 2,1             │ Cell 2,2             │                │
│  └──────────────────────┴──────────────────────┘                │
│                                                                  │
│  More content here.                                              │
│  Conclusion paragraph.                                           │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Clickable Segments

**Normal State**
```
┌─────────────────────────────────────────────────────────────────┐
│  This is a paragraph. Click any sentence to edit it. Each       │
│  sentence is a separate clickable segment.                      │
│                                                                  │
│  Hover effect brightens background ↑                            │
└─────────────────────────────────────────────────────────────────┘
```

**Clicked/Selected State**
```
┌─────────────────────────────────────────────────────────────────┐
│  This is a paragraph. ┌────────────────────────────────┐ Each   │
│  sentence is a       │Click any sentence to edit it.  │        │
│  separate clickable  └────────────────────────────────┘        │
│  segment.              ^                                         │
│                        └─ Selected segment with border          │
└─────────────────────────────────────────────────────────────────┘
```

### 5. Style Formatting

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   Main Title                    <- Title (16pt, bold, #003366)  │
│                                                                  │
│   Document Subtitle             <- Subtitle (12pt, italic,      │
│                                                        #663399)  │
│                                                                  │
│   Chapter 1: Introduction       <- Heading 1 (16pt, bold,       │
│                                                        #003366)  │
│                                                                  │
│   Section A                     <- Heading 2 (14pt, bold,       │
│                                                        #0066cc)  │
│                                                                  │
│   Subsection 1                  <- Heading 3 (12pt, bold,       │
│                                                        #3399ff)  │
│                                                                  │
│   Regular paragraph text here.  <- Normal (11pt, #000000)       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Workflow Examples

### Example 1: Translating a Document with Tables

**Step 1: Start in Grid View**
- Import DOCX
- See all segments at once
- Mark some as "Translated"

**Step 2: Switch to Split View for focused work**
- Press `Ctrl+2`
- Translate segments sequentially
- See source and target side-by-side

**Step 3: Review in Document View**
- Press `Ctrl+4`
- See document flow
- Check table structure
- Verify headings appear correctly
- Click any segment to edit

**Step 4: Final polish**
- Press `Ctrl+1` for Grid View
- Mark all as "Approved"
- Export DOCX

### Example 2: Table Cell Translation

**Grid View:**
```
Row 45: T1R1C1 | Header 1
Row 46: T1R1C2 | Header 2
Row 47: T1R2C1 | Cell content
Row 48: T1R2C2 | More content
```
*Can't see table structure*

**Document View:**
```
┌──────────────────────┬──────────────────────┐
│ Header 1             │ Header 2             │
├──────────────────────┼──────────────────────┤
│ Cell content         │ More content         │
└──────────────────────┴──────────────────────┘
```
*Clear table structure, better context*

---

## Keyboard Shortcuts Quick Reference

```
┌────────────────┬─────────────────────────────────────────────┐
│ Shortcut       │ Action                                      │
├────────────────┼─────────────────────────────────────────────┤
│ Ctrl+1         │ Switch to Grid View                         │
│ Ctrl+2         │ Switch to Split View                        │
│ Ctrl+3         │ Switch to Compact View                      │
│ Ctrl+4         │ Switch to Document View ⭐ NEW             │
│                │                                             │
│ Ctrl+O         │ Import DOCX                                 │
│ Ctrl+S         │ Save Project                                │
│ Ctrl+D         │ Copy Source to Target                       │
│ Ctrl+Enter     │ Save & Move to Next                         │
│ ↑ ↓            │ Navigate Segments                           │
└────────────────┴─────────────────────────────────────────────┘
```

---

## Color Coding Reference

### Status Colors (Document View)

| Status       | Background Color | Hex Code  | Use Case                    |
|--------------|------------------|-----------|----------------------------|
| Untranslated | Light red        | #ffe6e6   | Not yet translated         |
| Draft        | Light yellow     | #fff9e6   | Work in progress           |
| Translated   | Light green      | #e6ffe6   | Translation complete       |
| Approved     | Light blue       | #e6f3ff   | Reviewed and approved      |

### Hover Colors

| Status       | Hover Color      | Hex Code  |
|--------------|------------------|-----------|
| Untranslated | Medium red       | #ffcccc   |
| Draft        | Medium yellow    | #ffe6b3   |
| Translated   | Medium green     | #ccffcc   |
| Approved     | Medium blue      | #cce6ff   |

### Style Colors

| Style        | Color            | Hex Code  | Font Size | Weight |
|--------------|------------------|-----------|-----------|--------|
| Heading 1    | Dark blue        | #003366   | 16pt      | Bold   |
| Heading 2    | Medium blue      | #0066cc   | 14pt      | Bold   |
| Heading 3    | Light blue       | #3399ff   | 12pt      | Bold   |
| Title        | Dark blue        | #003366   | 16pt      | Bold   |
| Subtitle     | Purple           | #663399   | 12pt      | Italic |
| Normal       | Black            | #000000   | 11pt      | Normal |

---

## Tips and Tricks

### 💡 Tip 1: Use the Right View for the Task

- **Bulk changes** → Grid View
- **Quality translation** → Split View
- **Review and context** → Document View

### 💡 Tip 2: Jump Between Views

Working on a tricky table?
1. Start in Grid View to see all cells
2. Switch to Document View (Ctrl+4) to see structure
3. Click the problem cell
4. Edit right there!
5. Switch back to Grid (Ctrl+1) to continue

### 💡 Tip 3: Color Coding Tells a Story

In Document View, scan for:
- 🔴 **Red patches** - Areas needing translation
- 🟡 **Yellow patches** - Drafts to review
- 🟢 **Green patches** - Done sections
- 🔵 **Blue patches** - Approved content

### 💡 Tip 4: Tables in Context

Always review tables in Document View to:
- Ensure column headers make sense
- Check that related cells are consistent
- Verify table appears in correct location
- See how table relates to surrounding text

---

## Conclusion

Document View brings the best of both worlds:
- Professional CAT tool functionality
- Word-like document reading experience

Perfect for translators who want both **precision** and **context**.

**Happy Translating!** 🌍📝
