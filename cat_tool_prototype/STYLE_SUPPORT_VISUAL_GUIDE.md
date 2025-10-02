# Style Support - Visual Guide

## What's New in v0.3.1

### 📋 Style Column Added!

The segment grid now shows the Word style of each segment.

### Before (v0.3.0):
```
ID | Type   | Status        | Source                    | Target
---+--------+---------------+---------------------------+--------
1  | Para   | Untranslated  | Introduction              | 
2  | Para   | Untranslated  | This is body text...      | 
3  | Para   | Untranslated  | Background                | 
```
❌ **Problem**: Can't tell which are headings!

### After (v0.3.1):
```
ID | Type   | Style     | Status        | Source                    | Target
---+--------+-----------+---------------+---------------------------+--------
1  | Para   | H 1       | Untranslated  | Introduction              | 
2  | Para   | Normal    | Untranslated  | This is body text...      | 
3  | Para   | H 2       | Untranslated  | Background                | 
```
✅ **Solution**: Style column shows exactly what each segment is!

## Visual Style Indicators

### 🎨 Color & Font Coding

#### Heading 1
- **Display**: H 1
- **Appearance**: **Bold, Dark Blue** (#003366)
- **Example**: Main section titles

#### Heading 2  
- **Display**: H 2
- **Appearance**: **Bold, Medium Blue** (#0066cc)
- **Example**: Subsection titles

#### Heading 3
- **Display**: H 3
- **Appearance**: **Bold, Light Blue** (#3399ff)
- **Example**: Sub-subsection titles

#### Title
- **Display**: Title
- **Appearance**: **Bold, Larger, Purple** (#663399)
- **Example**: Document title

#### Subtitle
- **Display**: Subtitle
- **Appearance**: *Italic, Purple* (#663399)
- **Example**: Document subtitle

#### Normal
- **Display**: Normal
- **Appearance**: Regular text
- **Example**: Body paragraphs

#### Table Cells
- **Display**: Normal (in Style column)
- **Type**: T#R#C# (in Type column)
- **Appearance**: *Blue italic* (from v0.3.0)

## Real Document Example

### Software Development Agreement

```
ID | Type   | Style        | Status | Source
---+--------+--------------+--------+----------------------------------------
1  | Para   | Title        | Draft  | Software Development Agreement        [Bold Purple]
2  | Para   | Subtitle     | Draft  | Between Company A and Company B       [Italic Purple]
3  | Para   | H 1          | Draft  | 1. Introduction                       [Bold Dark Blue]
4  | Para   | Normal       | Draft  | This Software Development...          [Regular]
5  | Para   | Normal       | Draft  | The purpose of this Agreement...      [Regular]
6  | Para   | H 2          | Draft  | 1.1 Definitions                       [Bold Med Blue]
7  | Para   | Normal       | Draft  | For the purposes of this...           [Regular]
8  | Para   | H 3          | Draft  | 1.1.1 Software                        [Bold Light Blue]
9  | Para   | Normal       | Draft  | "Software" means the computer...      [Regular]
10 | Para   | H 3          | Draft  | 1.1.2 Services                        [Bold Light Blue]
11 | Para   | Normal       | Draft  | "Services" means the software...      [Regular]
12 | Para   | H 2          | Draft  | 1.2 Scope of Work                     [Bold Med Blue]
13 | Para   | Normal       | Draft  | The Developer agrees to develop...    [Regular]
14 | Para   | H 1          | Draft  | 2. Project Details                    [Bold Dark Blue]
15 | T1R1C1 | Normal       | Draft  | Project Name                          [Blue Italic]
16 | T1R1C2 | Normal       | Draft  | Enterprise Resource Planning...       [Blue Italic]
```

**Document Statistics:**
- Title: 1
- Subtitle: 1
- Heading 1: 5
- Heading 2: 5
- Heading 3: 2
- Normal: 31
- Table cells: 20

## Benefits for Translators

### 1. Instant Context Recognition
```
H 1  | Introduction           → Main heading, formal tone
Normal | This document...      → Body text, standard translation
H 2  | Definitions           → Subsection, clear/concise
Normal | "Software" means...   → Technical definition, precise
```

### 2. Appropriate Translation Style

**Heading Translation:**
- Shorter, punchier
- May use title case
- Formal terminology
- Parallel structure

**Body Text Translation:**
- Full sentences
- More explanation
- Standard terminology
- Natural flow

### 3. Document Hierarchy

```
H 1: 1. Introduction          → Top level
  H 2: 1.1 Definitions        → Second level
    H 3: 1.1.1 Software       → Third level
    Normal: Definition text   → Body content
```

**Result**: Maintain proper structure in translation!

## Style Name Abbreviations

### Short Display Names (for space):
- `Title` → Title
- `Subtitle` → Subtitle
- `Heading 1` → H 1
- `Heading 2` → H 2
- `Heading 3` → H 3
- `Heading 4` → H 4
- `Normal` → Normal
- `List Paragraph` → List Para
- `Intense Quote` → Intense Quote

## Combined Visual Features

### Status + Style
Segments show BOTH status color (background) AND style formatting (text):

```
[Red Background, Bold Dark Blue Text] = Untranslated Heading 1
[Yellow Background, Regular Text]     = Draft Normal paragraph
[Green Background, Bold Med Blue]     = Translated Heading 2
[Blue Background, Regular Text]       = Approved Normal paragraph
```

### Type + Style
```
Para + H 1     = Regular paragraph with Heading 1 style
Para + Normal  = Regular paragraph with Normal style
T1R2C3 + Normal = Table cell (always Normal style)
```

## Translation Workflow

### Step 1: Import Document
```
File → Import DOCX → Select document

Result: Style column populated automatically!
```

### Step 2: Review Structure
```
Scroll through segments, observe:
- Which are headings (H 1, H 2, H 3)
- Which are body text (Normal)
- Document organization
```

### Step 3: Translate with Context
```
Select H 1 segment → Translate as main heading (formal, concise)
Select Normal segment → Translate as body text (standard)
Select H 2 segment → Translate as subsection (clear)
```

### Step 4: Export
```
File → Export Translated DOCX

Note: In v0.3.1, style preservation is visual only.
Full export preservation coming in Phase B!
```

## Keyboard Navigation

### Standard Shortcuts Still Work:
- `↑↓` - Navigate segments
- `Enter` - Edit segment
- `Ctrl+Enter` - Save and next
- `Ctrl+S` - Save project

### Style-Aware Navigation (visual only):
- Headings **stand out visually** in bold blue
- Easy to jump to next section (look for bold)
- Quick identification of document structure

## Use Case Examples

### Legal Contract:
```
Title        | Software License Agreement
H 1          | Article 1: Definitions
H 2          | 1.1 Licensed Software
Normal       | "Licensed Software" means...
H 2          | 1.2 Territory
Normal       | "Territory" means...
H 1          | Article 2: Grant of License
Normal       | Licensor hereby grants...
```

### Technical Manual:
```
Title        | User Guide - Version 2.0
H 1          | Chapter 1: Getting Started
H 2          | 1.1 Installation
Normal       | To install the software...
H 3          | 1.1.1 System Requirements
Normal       | Minimum specifications...
H 2          | 1.2 Configuration
Normal       | After installation...
```

### Business Report:
```
Title        | Q4 2024 Financial Report
Subtitle     | Executive Summary
H 1          | Financial Overview
Normal       | Revenue increased by 15%...
H 2          | Revenue Analysis
Normal       | Key drivers of growth...
H 2          | Expense Management
Normal       | Operating expenses...
```

## Tips & Best Practices

### 1. Use Style for Context
- Always check style before translating
- Headings may need different terminology
- Adjust formality based on style

### 2. Maintain Hierarchy
- Keep heading structure parallel
- Don't make headings too long
- Preserve numbering systems

### 3. Check Document Flow
- Scroll through to see structure
- Headings should make sense in sequence
- Body text should support headings

### 4. Quality Control
- Review all H 1 segments together
- Check consistency in heading translation
- Verify parallel structure maintained

## Troubleshooting

### Q: Style shows "None" or blank?
**A**: Rare case where Word document has no style assigned. Treated as "Normal".

### Q: Custom style not color-coded?
**A**: Only common styles (H 1-3, Title) have special colors. Custom styles show in regular text but are labeled correctly.

### Q: Style column too narrow?
**A**: Column is auto-sized for most common styles. Can be adjusted by dragging column divider.

### Q: Want to filter by style?
**A**: Coming in Phase C (future release)! For now, use visual scanning - headings in bold blue stand out.

## What's Not Included (Yet)

### In v0.3.1:
- ✅ Style displayed
- ✅ Visual color coding
- ✅ Style saved with project
- ❌ Style preserved on export (coming in Phase B)
- ❌ Filter by style (coming in Phase C)
- ❌ Style-specific settings (coming in Phase C)

### Coming Soon:
**Phase B** (during integration): Export preserves original styles
**Phase C** (future): Advanced features (filtering, analytics, etc.)

---

## Quick Reference Card

| Style | Display | Color | Font | Use |
|-------|---------|-------|------|-----|
| Title | Title | Purple | Bold, Large | Document title |
| Subtitle | Subtitle | Purple | Italic | Document subtitle |
| Heading 1 | H 1 | Dark Blue | Bold | Main sections |
| Heading 2 | H 2 | Med Blue | Bold | Subsections |
| Heading 3 | H 3 | Light Blue | Bold | Sub-subsections |
| Normal | Normal | Black | Regular | Body text |
| Table | Normal | Blue | Italic | Table cells |

---

**Import the test document `test_document_with_styles.docx` to see style support in action!** 🎨
