# CAT Tool Workflow Guide

**Version:** v1.9.27 | **Last Updated:** December 9, 2025

How to use Supervertaler alongside your CAT tool (memoQ, Trados, CafeTran) for professional translation workflows.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [What's New in v1.9.27](#whats-new-in-v1927)
3. [Exporting from CAT Tools](#exporting-from-cat-tools)
4. [Working in Supervertaler](#working-in-supervertaler)
5. [Reimporting to CAT Tools](#reimporting-to-cat-tools)
6. [Formatting Preservation](#formatting-preservation-v194)
7. [Best Practices](#best-practices)

---

## Overview

Supervertaler is a **companion tool** that works alongside your CAT tool:

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   memoQ     │────▶│   Supervertaler  │────▶│   memoQ     │
│   Trados    │     │                  │     │   Trados    │
│   CafeTran  │     │  • AI Translation│     │   CafeTran  │
│             │     │  • TM/Termbase   │     │             │
│  Export     │     │  • Review/Edit   │     │  Reimport   │
│  Bilingual  │     │  • Tag Handling  │     │  Bilingual  │
└─────────────┘     └──────────────────┘     └─────────────┘
```

**Workflow Summary:**
1. Export bilingual DOCX from CAT tool
2. Open in Supervertaler
3. Translate/review with AI assistance
4. Export bilingual DOCX
5. Reimport to CAT tool

---

## What's New in v1.9.27

### 📄 Simple Text File Import/Export

For simple text files that don't need CAT tool processing:

- **Import**: File → Import → Simple Text File (TXT)
- Each line becomes one source segment
- **Export**: File → Export → Simple Text File - Translated (TXT)
- Output matches input structure exactly

**Ideal for:** Simple line-by-line text content, subtitle files, configuration files

### 🔄 Automatic Model Version Checker (v1.9.26)

Supervertaler automatically checks for new LLM models from OpenAI, Anthropic (Claude), and Google (Gemini):

- **Daily Checks**: Runs once per 24 hours on startup (configurable in Settings)
- **Smart Notifications**: Only shows popup when new models are detected
- **Easy Selection**: Check the models you want to add, click OK
- **Manual Check**: Use **Help → Settings → AI Settings** or the toolbar button

**Why this matters for translators:**
- Stay current with latest AI capabilities
- Get access to improved models automatically
- No need to manually track model releases

### 📚 Superdocs - Interactive Documentation

Access comprehensive, auto-generated documentation directly from within Supervertaler:

- **Location**: **Tools → Superdocs** or **Help → Superdocs (Interactive)**
- **Content**: Architecture overview, module documentation, dependency graphs
- **Features**: Tree navigation, rich markdown preview, one-click generation
- **Always Current**: Regenerate documentation anytime to reflect code changes

### 🎨 UI Improvements

- All 68 checkboxes standardized to green with white checkmarks
- Refined 16×16px size for modern, consistent appearance
- Improved visual consistency throughout the application

---

## Exporting from CAT Tools

### memoQ

**Two-Column Bilingual Export:**
1. Open your project in memoQ
2. Go to **Document → Export Bilingual** (Ctrl+Shift+E)
3. Select **Two-column RTF/DOC** format
4. Save as **.docx** (not .rtf)

**Settings to note:**
- Include segment status (optional)
- Include comments (optional)

### Trados Studio

When working with agencies that use Trados Studio, Supervertaler supports two exchange formats:

#### SDLPPX/SDLRPX Package Exchange

This is the native Trados package format used by agencies:

**Workflow:**
1. Agency sends you an `.sdlppx` package
2. In Supervertaler: **File → Open** and select the `.sdlppx` file
3. Translate in Supervertaler
4. **File → Export → Trados Package (SDLRPX)** to create return package
5. Send the `.sdlrpx` back to the agency

**Characteristics:**
- Full status synchronization (Draft → Translated)
- All segment metadata preserved
- Agency can reimport directly into Trados Studio

#### Bilingual Review DOCX

Some agencies may send bilingual DOCX files instead of packages.

> ⚠️ **IMPORTANT**: The Bilingual Review DOCX format is designed for **review only**, 
> not for translation from scratch. It does NOT export empty target segments!
> 
> See: [RWS Community Discussion](https://community.rws.com/product-groups/trados-portfolio/trados-studio/f/studio/34874/export-for-bilingual-review-exports-only-source-text)

If you receive a bilingual DOCX with empty targets, or need to create one yourself,
follow this **specific workflow**:

**Complete Workflow:**

1. **In Trados Studio (before export):**
   - Select all segments (Ctrl+A)
   - **Edit → Copy Source to Target** (fills empty targets with source text)
   - Save the project

2. **Export from Trados:**
   - **File → Save Target As → Export for External Review**
   - Select **Bilingual Review (Word)**
   - Save as `.docx`

3. **In Microsoft Word:**
   - Open the exported DOCX
   - The table now has source text in BOTH columns
   - Select all text in the TARGET column (right column)
   - Delete it (now target cells are empty but EXIST)
   - Save the DOCX

4. **In Supervertaler:**
   - **File → Open** and select the prepared DOCX
   - Translate your segments
   - **File → Export Trados Bilingual DOCX**

5. **Back in Trados Studio:**
   - **File → Open → Import Bilingual Document**
   - Select your translated DOCX
   - Translations will be imported with correct status

**Why this workaround?**
The Bilingual Review format only exports segments that have target text.
By copying source to target first, we ensure all segments are exported.
Then we delete the targets in Word so you have empty cells to translate.

### CafeTran Espresso

**Export Bilingual:**
1. Open project in CafeTran
2. Go to **Project → Export → Bilingual Table**
3. Choose DOCX format
4. Save file

### Other CAT Tools

Supervertaler works with any bilingual table format that has:
- Source text in one column
- Target text in adjacent column
- Consistent table structure

---

## Working in Supervertaler

### Opening Bilingual Files

1. **File → Open** (Ctrl+O)
2. Select your bilingual DOCX
3. Supervertaler auto-detects the format:
   - memoQ two-column
   - Trados bilingual review
   - Generic two-column table

### The Grid View

| Column | Content |
|--------|---------|
| **#** | Segment number |
| **Source** | Original text (read-only) |
| **Target** | Translation (editable) |
| **Status** | Segment status |

**Navigation:**
- Click any row to select
- Arrow keys to move up/down
- Double-click target to edit

### Translation Options

**Single Segment (F5):**
1. Select a segment
2. Press F5 or click Translate
3. AI translation appears in response panel
4. Press Enter to accept

**Selected Segments:**
1. Ctrl+Click to select multiple segments
2. Click "Translate Selected" in toolbar
3. Review each translation

**All Segments:**
1. **Edit → AI Actions → Translate All Segments**
2. Configure options:
   - Skip already translated
   - Skip locked segments
   - Batch size
3. Click Start

### Using Translation Memory

1. Go to **Resources → Translation Memories**
2. Click **Add TM** and select your TMX files
3. Check **Read** to use for lookups
4. Check **Write** to save new translations

**TM Matches appear automatically:**
- In the TM Matches panel (right side)
- Color-coded by match percentage
- Ctrl+1-9 to insert matches

### Using Termbases

1. Go to **Resources → Termbases**
2. Add your termbase files (TBX, CSV, Excel)
3. Terms highlight in source text
4. Hover or click to see translations

**Project Termbases:**
- Each project can have a dedicated termbase
- Use **Extract Terms** to auto-extract terminology
- Pink highlighting = project terms

### Status Tracking

| Status | Meaning | Use When |
|--------|---------|----------|
| Draft | Not translated | Initial state |
| Translated | Has translation | After AI/manual translation |
| Reviewed | Checked by translator | After review pass |
| Approved | Ready for delivery | Client/PM approved |
| Needs Review | Flagged for attention | Uncertain translations |
| Final | Locked | Complete, don't edit |

---

## Reimporting to CAT Tools

### Export from Supervertaler

1. **File → Export** (Ctrl+E)
2. Choose **Bilingual DOCX**
3. Save file (use descriptive name like `project_translated.docx`)

### memoQ Reimport

1. In memoQ, go to **Document → Import Bilingual**
2. Select your exported DOCX
3. Choose import options:
   - Update existing segments
   - Add to TM (optional)
4. Click Import

**Important:** Segment count must match original export.

### Trados Studio Reimport

1. In Trados, go to **File → Open**
2. Select the bilingual review file
3. Choose **Update from bilingual review**
4. Segments update in your project

### CafeTran Reimport

1. In CafeTran, go to **Project → Import**
2. Select bilingual table
3. Choose merge options

---

## Formatting Preservation (v1.9.4+)

### How It Works

When importing memoQ bilingual files with formatting:

1. **Import**: Bold, italic, underline preserved as tags
   - `<b>bold text</b>`
   - `<i>italic text</i>`
   - `<u>underlined text</u>`

2. **Display modes:**
   - **WYSIWYG**: See **bold**, *italic*, <u>underlined</u>
   - **Tag view**: See raw `<b>tags</b>`
   - Toggle with **Ctrl+Alt+T**

3. **Editing**: Apply formatting with shortcuts
   - **Ctrl+B** for bold
   - **Ctrl+I** for italic
   - **Ctrl+U** for underline

4. **Export**: Tags convert back to Word formatting
   - Round-trip fidelity preserved

### memoQ Placeholder Tags (v1.9.5+)

memoQ uses numbered tags for placeholders: `[1}text{1]`, `[2}`, `{3]`

**Inserting tags:**
1. Look at source segment for tag patterns
2. Press **Ctrl+,** to insert next tag pair
3. Or select text and press Ctrl+, to wrap with tags

**Tag detection:**
- Paired: `[1}...{1]` (opening + closing)
- Standalone: `[3]` (single tag)

---

## Best Practices

### Before Starting

1. ✅ Create a backup of your CAT project
2. ✅ Export a test segment first to verify format
3. ✅ Set up TMs and termbases before translating
4. ✅ Choose appropriate AI model for your language pair

### During Translation

1. ✅ Use AI for first draft, then review
2. ✅ Check terminology consistency with termbases
3. ✅ Update segment status as you work
4. ✅ Save frequently (Ctrl+S)

### After Translation

1. ✅ Run spell check in CAT tool after reimport
2. ✅ Run QA checks in CAT tool
3. ✅ Verify segment count matches
4. ✅ Spot-check formatting

### Recommended Workflow

```
Day 1: Setup
├── Export from CAT tool
├── Import to Supervertaler
├── Set up TM/Termbases
└── Configure prompts

Day 1-N: Translation
├── AI translate in batches
├── Review and edit
├── Mark segments as Reviewed
└── Save regularly

Final Day: Delivery
├── Final review pass
├── Export bilingual DOCX
├── Reimport to CAT tool
├── Run CAT tool QA
└── Deliver
```

---

## Troubleshooting

### Segments Don't Match on Reimport

**Cause:** Segment structure changed between export and reimport.

**Solution:**
- Don't merge or split segments in Supervertaler
- Export with same settings as import
- Check for empty segments

### Formatting Lost on Reimport

**Cause:** Tags not preserved correctly.

**Solution:**
- Use Tag view (Ctrl+Alt+T) to verify tags
- Ensure tags are balanced: `<b>text</b>` not `<b>text`
- Check memoQ export settings include formatting

### TM Matches Not Appearing

**Cause:** TM not loaded or language mismatch.

**Solution:**
- Check TM is added in Resources tab
- Verify "Read" checkbox is enabled
- Check source/target language matches project

---

*See also: [Quick Start Guide](QUICK_START.md) | [Keyboard Shortcuts](KEYBOARD_SHORTCUTS.md)*
