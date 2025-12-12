# Supervertaler Quick Start Guide

**Version:** v1.9.6 | **Last Updated:** November 27, 2025

Get translating in 5 minutes. This guide covers the essentials to start using Supervertaler with your CAT tool workflow.

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [API Keys Setup](#api-keys-setup)
3. [Your First Translation](#your-first-translation)
4. [Essential Keyboard Shortcuts](#essential-keyboard-shortcuts)
5. [Next Steps](#next-steps)

---

## Installation

### Option A: Run from Source (Recommended)

```powershell
# 1. Clone the repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch
python Supervertaler.py
```

### Option B: Windows Executable

Download from [GitHub Releases](https://github.com/michaelbeijer/Supervertaler/releases) and run `Supervertaler.exe`.

---

## API Keys Setup

Supervertaler needs at least one AI provider API key. On first launch, the Setup Wizard guides you through this.

### Supported Providers

| Provider | Models | Get API Key |
|----------|--------|-------------|
| **OpenAI** | GPT-4o, GPT-4o-mini, o1, o3-mini | [platform.openai.com](https://platform.openai.com/api-keys) |
| **Anthropic** | Claude 4 Sonnet, Claude 4 Opus | [console.anthropic.com](https://console.anthropic.com/) |
| **Google** | Gemini 2.0 Flash, Gemini 2.5 Pro | [aistudio.google.com](https://aistudio.google.com/apikey) |

### Adding API Keys

1. Go to **Settings** (gear icon in toolbar)
2. Select **API Keys** tab
3. Paste your key(s) and click **Save**

> **Tip:** You only need ONE provider to start. OpenAI GPT-4o-mini is the most cost-effective for testing.

---

## Your First Translation

### Step 1: Import a Bilingual Document

Supervertaler works with bilingual DOCX files exported from CAT tools.

**From memoQ:**
1. In memoQ: **Document → Export Bilingual** (or Ctrl+Shift+E)
2. Choose "Two-column RTF/DOC" format
3. Save as DOCX

**From Trados (Package - Recommended):**
1. Open the `.sdlppx` package directly in Supervertaler
2. Translate and export as `.sdlrpx` return package

**From Trados (Bilingual DOCX - Workaround):**
> ⚠️ The Bilingual Review format is for review only, not translation.
> See the [CAT Workflow Guide](CAT_WORKFLOW.md#trados-studio) for the required preparation steps.

**In Supervertaler:**
1. Click **File → Open** (or Ctrl+O)
2. Select your bilingual DOCX or SDLPPX package
3. Segments appear in the grid with Source (left) and Target (right)

### Step 2: Configure Your Resources

Go to the **Resources** tab (bottom panel) to set up:

- **Translation Memories** - Add TMX files for consistency
- **Termbases** - Add terminology databases
- **Web Resources** - Configure MT engines (optional)

### Step 3: Translate with AI

**Single Segment:**
1. Click on a segment in the grid
2. Click **Translate** button (or press **F5**)
3. AI translation appears in the AI Response panel
4. Press **Enter** to accept into target cell

**Multiple Segments:**
1. Select segments (Ctrl+Click or Shift+Click)
2. Click **Translate Selected** in the toolbar
3. Review and accept translations

**Batch Translation:**
1. Go to **Edit → AI Actions → Translate All Segments**
2. Choose options (skip translated, etc.)
3. Click **Start**

### Step 4: Review and Edit

- **Double-click** any target cell to edit
- **Ctrl+Z** to undo changes
- Use status dropdown to mark segments (Translated, Reviewed, etc.)

### Step 5: Export

1. Click **File → Export** (or Ctrl+E)
2. Choose your format:
   - **Bilingual DOCX** - For reimport to CAT tool
   - **Target Only DOCX** - Final translated document
   - **TMX** - Export as translation memory

---

## Essential Keyboard Shortcuts

### Navigation
| Shortcut | Action |
|----------|--------|
| **↑/↓** | Move between segments |
| **Page Up/Down** | Scroll through segments |
| **Ctrl+G** | Go to segment number |

### Translation
| Shortcut | Action |
|----------|--------|
| **F5** | Translate current segment |
| **Enter** | Accept AI response to target |
| **Ctrl+1-9** | Insert TM match (1=best) |

### Editing
| Shortcut | Action |
|----------|--------|
| **Ctrl+Z** | Undo |
| **Ctrl+Y** | Redo |
| **Ctrl+F** | Find & Replace |
| **Ctrl+S** | Save project |

### Formatting (v1.9.4+)
| Shortcut | Action |
|----------|--------|
| **Ctrl+B** | Bold tags `<b>...</b>` |
| **Ctrl+I** | Italic tags `<i>...</i>` |
| **Ctrl+U** | Underline tags `<u>...</u>` |
| **Ctrl+Alt+T** | Toggle Tag view |
| **Ctrl+,** | Insert memoQ tag pair |

### Voice & Lookup
| Shortcut | Action |
|----------|--------|
| **F9** | Start/stop voice dictation |
| **Ctrl+Alt+L** | Universal TM lookup (system-wide) |

---

## Next Steps

### Customize Your Prompts

The **Prompts** tab lets you control how AI translates:

1. **System Prompts** - Core translation rules (select from dropdown)
2. **Custom Prompts** - Project-specific instructions
3. **AI Assistant** - Chat with AI to generate prompts from your document

### Set Up Project Termbases

1. Go to **Resources → Termbases**
2. Click **Extract Terms** to auto-extract terminology
3. Edit terms in the **Termbase Entry Editor**

### Try Advanced Features

- **Superbench** - Benchmark AI models on your projects
- **Supervoice** - Voice dictation in 100+ languages (F9)
- **Superlookup** - Universal TM search from any app (Ctrl+Alt+L)
- **PDF Rescue** - OCR locked PDFs to editable DOCX

---

## Getting Help

- **[FAQ](FAQ.md)** - Common questions answered
- **[Keyboard Shortcuts](KEYBOARD_SHORTCUTS.md)** - Complete shortcut reference
- **[CHANGELOG](../../CHANGELOG.md)** - Latest features and fixes
- **[GitHub Discussions](https://github.com/michaelbeijer/Supervertaler/discussions)** - Community support

---

*Happy translating! 🌐*
