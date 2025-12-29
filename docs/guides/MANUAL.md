# Supervertaler Manual

**Version:** v1.9.64 | **Last Updated:** December 29, 2025

The complete guide to using Supervertaler for AI-powered translation.

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [API Keys Setup](#api-keys-setup)
3. [CAT Tool Workflows](#cat-tool-workflows)
   - [memoQ](#memoq)
   - [Trados Studio](#trados-studio)
   - [CafeTran Espresso](#cafetran-espresso)
   - [Phrase (Memsource)](#phrase-memsource)
4. [Working in Supervertaler](#working-in-supervertaler)
   - [The Grid View](#the-grid-view)
   - [Translation Options](#translation-options)
   - [Translation Memory](#translation-memory)
   - [Termbases (Glossaries)](#termbases-glossaries)
   - [Segment Status](#segment-status)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Formatting & Tags](#formatting--tags)
7. [Reimporting to CAT Tools](#reimporting-to-cat-tools)
8. [Advanced Features](#advanced-features)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Installation

### Option A: Install from PyPI (Recommended) ⭐

```bash
pip install supervertaler
supervertaler
```

To update:
```bash
pip install --upgrade supervertaler
```

**PyPI Package:** https://pypi.org/project/Supervertaler/

### Option B: Run from Source

```powershell
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler
pip install -r requirements.txt
python Supervertaler.py
```

### Option C: Windows Executable

Download from [GitHub Releases](https://github.com/michaelbeijer/Supervertaler/releases) and run `Supervertaler.exe`.

---

## API Keys Setup

Supervertaler needs at least one AI provider API key. The Setup Wizard guides you through this on first launch.

### Supported Providers

| Provider | Models | Get API Key |
|----------|--------|-------------|
| **OpenAI** | GPT-4o, GPT-4o-mini, o1, o3-mini | [platform.openai.com](https://platform.openai.com/api-keys) |
| **Anthropic** | Claude 4 Sonnet, Claude 4 Opus | [console.anthropic.com](https://console.anthropic.com/) |
| **Google** | Gemini 2.0 Flash, Gemini 2.5 Pro | [aistudio.google.com](https://aistudio.google.com/apikey) |

### Adding API Keys

1. Go to **Settings** → **API Keys** tab
2. Paste your key(s) and click **Save**

> **Tip:** You only need ONE provider to start. OpenAI GPT-4o-mini is the most cost-effective for testing.

---

## CAT Tool Workflows

Supervertaler is a **companion tool** that works alongside your CAT tool:

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   memoQ     │────▶│   Supervertaler  │────▶│   memoQ     │
│   Trados    │     │                  │     │   Trados    │
│   CafeTran  │     │  • AI Translation│     │   CafeTran  │
│   Phrase    │     │  • TM/Glossary   │     │   Phrase    │
│             │     │  • Review/Edit   │     │             │
│  Export     │     │  • Tag Handling  │     │  Reimport   │
│  Bilingual  │     │                  │     │  Bilingual  │
└─────────────┘     └──────────────────┘     └─────────────┘
```

---

### memoQ

**Export from memoQ:**
1. Open your project in memoQ
2. **Document → Export Bilingual** (Ctrl+Shift+E)
3. Select **Two-column RTF/DOC** format
4. Save as **.docx** (not .rtf)

**Import to Supervertaler:**
1. **File → Open** and select your DOCX
2. Translate with AI assistance
3. **File → Export → memoQ Bilingual DOCX**

**Reimport to memoQ:**
1. In memoQ: **Document → Import Bilingual**
2. Select your exported DOCX
3. Segments update in your project

---

### Trados Studio

Supervertaler supports two Trados exchange formats:

#### Option 1: SDLPPX/SDLRPX Packages (Recommended)

The native Trados package format with full metadata preservation.

**Workflow:**
1. Agency sends you an `.sdlppx` package
2. In Supervertaler: **File → Open** and select the `.sdlppx` file
3. Translate in Supervertaler
4. **File → Export → Trados Package (SDLRPX)**
5. Send the `.sdlrpx` back to the agency

**Benefits:**
- Full status synchronization (Draft → Translated)
- All segment metadata preserved
- Agency can reimport directly into Trados Studio

#### Option 2: Bilingual Review DOCX (Workaround)

> ⚠️ **IMPORTANT**: The Bilingual Review format is designed for **review only**, not for translation from scratch. It does NOT export empty target segments!
> 
> See: [RWS Community Discussion](https://community.rws.com/product-groups/trados-portfolio/trados-studio/f/studio/34874/export-for-bilingual-review-exports-only-source-text)

If you need to use bilingual DOCX instead of packages:

**Complete Workflow:**

1. **In Trados Studio (before export):**
   - Select all segments (Ctrl+A)
   - **Edit → Copy Source to Target** (fills empty targets)
   - Save the project

2. **Export from Trados:**
   - **File → Save Target As → Export for External Review**
   - Select **Bilingual Review (Word)**
   - Save as `.docx`

3. **In Microsoft Word:**
   - Open the exported DOCX
   - Select all text in the TARGET column (right column)
   - Delete it (cells are empty but exist)
   - Save the DOCX

4. **In Supervertaler:**
   - **File → Open** and select the prepared DOCX
   - Translate your segments
   - **File → Export → Trados Bilingual DOCX**

5. **Back in Trados Studio:**
   - **File → Open → Import Bilingual Document**
   - Select your translated DOCX

---

### CafeTran Espresso

**Export from CafeTran:**
1. Open project in CafeTran
2. **Project → Export → Bilingual Table**
3. Choose DOCX format

**Import to Supervertaler:**
1. **File → Open** and select the DOCX
2. Translate with AI assistance
3. **File → Export → CafeTran Bilingual DOCX**

**Reimport to CafeTran:**
1. **Project → Import** and select bilingual table
2. Choose merge options

---

### Phrase (Memsource)

**Export from Phrase:**
1. In Phrase Editor, go to **Document → Export → Bilingual DOCX**
2. Save the file

**Import to Supervertaler:**
1. **File → Open** and select the DOCX
2. Translate with AI assistance
3. **File → Export → Phrase Bilingual DOCX**

---

## Working in Supervertaler

### The Grid View

| Column | Content |
|--------|---------|
| **#** | Segment number |
| **Source** | Original text (read-only) |
| **Target** | Translation (editable) |
| **Status** | Segment status dropdown |

**Navigation:**
- **↑/↓** arrows move between segments (when at top/bottom line of cell)
- **Alt+↑/↓** always moves to previous/next segment
- **Ctrl+G** to go to a specific segment number
- **Page Up/Down** to scroll through segments

---

### Translation Options

**Single Segment (F5):**
1. Select a segment
2. Press **F5** or click Translate
3. AI translation appears in response panel
4. Press **Enter** to accept

**Selected Segments:**
1. Ctrl+Click to select multiple segments
2. Click **Translate Selected** in toolbar

**Batch Translation:**
1. **Edit → AI Actions → Translate All Segments**
2. Configure options (skip translated, batch size)
3. Enable "Retry until all segments translated" (recommended)
4. Click **Start Translation**

---

### Translation Memory

1. Go to **Project resources → Translation Memories**
2. Click **Add TM** and select TMX files
3. Check **Read** to use for lookups
4. Check **Write** to save new translations

**TM Matches:**
- Appear automatically in the TM Matches panel
- Color-coded by match percentage
- **Ctrl+1-9** to insert matches

---

### Termbases (Glossaries)

1. Go to **Project resources → Termbases**
2. Add termbase files (TBX, CSV, TSV)
3. Terms highlight in source text automatically

**Project Glossary:**
- Each project can have a dedicated glossary
- Use **Extract Terms** to auto-extract terminology
- Pink highlighting = project terms

---

### Segment Status

| Status | Meaning |
|--------|---------|
| Draft | Not translated |
| Translated | Has translation |
| Reviewed | Checked by translator |
| Approved | Ready for delivery |
| Needs Review | Flagged for attention |
| Final | Locked, don't edit |

---

## Keyboard Shortcuts

### Navigation
| Shortcut | Action |
|----------|--------|
| **↑/↓** | Move between segments (at edge of cell) |
| **Alt+↑/↓** | Always move to prev/next segment |
| **Page Up/Down** | Scroll through segments |
| **Ctrl+G** | Go to segment number |
| **Ctrl+Home/End** | First/last segment |

### Translation
| Shortcut | Action |
|----------|--------|
| **F5** | Translate current segment |
| **Enter** | Accept AI response |
| **Ctrl+1-9** | Insert TM match |
| **Ctrl+K** | Open Superlookup |

### Editing
| Shortcut | Action |
|----------|--------|
| **Ctrl+Z** | Undo |
| **Ctrl+Y** | Redo |
| **Ctrl+F** | Find & Replace |
| **Ctrl+S** | Save project |
| **Ctrl+Shift+F** | Filter on selection |

### Formatting
| Shortcut | Action |
|----------|--------|
| **Ctrl+B** | Bold `<b>...</b>` |
| **Ctrl+I** | Italic `<i>...</i>` |
| **Ctrl+U** | Underline `<u>...</u>` |
| **Ctrl+Alt+T** | Toggle Tag view |
| **Ctrl+,** | Insert memoQ tag pair |

### Voice & Lookup
| Shortcut | Action |
|----------|--------|
| **F9** | Start/stop voice dictation |
| **Ctrl+Alt+L** | System-wide TM lookup |

---

## Formatting & Tags

### Tag Display Modes

- **WYSIWYG Mode**: See **bold**, *italic*, underlined
- **Tag View**: See raw `<b>tags</b>`
- Toggle with **Ctrl+Alt+T**

### Supported Tags

| Tag | Meaning |
|-----|---------|
| `<b>...</b>` | Bold |
| `<i>...</i>` | Italic |
| `<u>...</u>` | Underline |
| `<bi>...</bi>` | Bold + Italic |
| `<sub>...</sub>` | Subscript |
| `<sup>...</sup>` | Superscript |

### CAT Tool Placeholder Tags

| CAT Tool | Tag Format |
|----------|------------|
| memoQ | `[1}text{1]`, `{2}` |
| Trados | `<1>`, `</1>` |
| Phrase | `{1}`, `{2}` |

---

## Reimporting to CAT Tools

### Export from Supervertaler

1. **File → Export** (Ctrl+E)
2. Choose your CAT tool format:
   - memoQ Bilingual DOCX
   - Trados Package (SDLRPX)
   - Trados Bilingual DOCX
   - CafeTran Bilingual DOCX
   - Phrase Bilingual DOCX

### Important Notes

- **Segment count must match** - Don't merge or split segments
- **Keep tags balanced** - `<b>text</b>` not `<b>text`
- **Run CAT tool QA** after reimport

---

## Advanced Features

### Superlookup (Ctrl+K)

Unified concordance search across all resources:
- Translation Memory
- Termbases
- Supermemory (semantic search)
- Machine Translation
- Web Resources (ProZ, Linguee, IATE, etc.)

### Supermemory

Vector-indexed semantic search across all your TMs:
1. **Settings → Supermemory** to enable
2. Indexes TM content with AI embeddings
3. Finds conceptually similar translations

### Supervoice (F9)

Voice dictation in 100+ languages:
- Press F9 to start/stop recording
- Enable "Always-On Listening" for hands-free
- Supports voice commands ("next segment", "confirm", etc.)

### PDF Rescue

Extract text from scanned/locked PDFs:
1. **Tools → PDF Rescue**
2. Select PDF file
3. AI OCR extracts text to editable DOCX

### Superbench

Benchmark AI models on your translation projects:
1. **Tools → Superbench**
2. Run same segments through multiple models
3. Compare quality scores

---

## Best Practices

### Before Starting
- ✅ Create a backup of your CAT project
- ✅ Export a test segment first to verify format
- ✅ Set up TMs and glossaries before translating
- ✅ Choose appropriate AI model for your language pair

### During Translation
- ✅ Use AI for first draft, then review
- ✅ Check terminology consistency with glossaries
- ✅ Update segment status as you work
- ✅ Save frequently (Ctrl+S)

### After Translation
- ✅ Run spell check in CAT tool after reimport
- ✅ Run QA checks in CAT tool
- ✅ Verify segment count matches
- ✅ Spot-check formatting

### Recommended Workflow

```
Day 1: Setup
├── Export from CAT tool
├── Import to Supervertaler
├── Set up TM/Glossaries
└── Configure prompts

Day 1-N: Translation
├── AI translate in batches
├── Review and edit
├── Mark segments as Reviewed
└── Save regularly

Final Day: Delivery
├── Final review pass
├── Export bilingual
├── Reimport to CAT tool
├── Run CAT tool QA
└── Deliver
```

---

## Troubleshooting

### Segments Don't Match on Reimport

**Cause:** Segment structure changed.

**Solution:**
- Don't merge or split segments in Supervertaler
- Export with same settings as import
- Check for empty segments

### Formatting Lost on Reimport

**Cause:** Tags not preserved correctly.

**Solution:**
- Use Tag view (Ctrl+Alt+T) to verify tags
- Ensure tags are balanced
- Check export settings include formatting

### TM Matches Not Appearing

**Cause:** TM not loaded or language mismatch.

**Solution:**
- Check TM is added in Project resources tab
- Verify "Read" checkbox is enabled
- Check source/target language matches

### Spellcheck Not Working

**Cause:** Wrong language or missing dictionary.

**Solution:**
- Check spellcheck language in Settings → View Settings
- Ensure Hunspell dictionary installed for target language
- Linux: `sudo apt install hunspell-XX` (language code)

---

## Getting Help

- **[FAQ](../FAQ.md)** - Common questions answered
- **[CHANGELOG](../../CHANGELOG.md)** - Latest features and fixes
- **[GitHub Discussions](https://github.com/michaelbeijer/Supervertaler/discussions)** - Community support
- **Website:** [supervertaler.com](https://supervertaler.com)

---

*Happy translating! 🌐*
