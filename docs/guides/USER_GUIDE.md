# Supervertaler User Guide
## Comprehensive Documentation for All Versions

> **📌 Version Note**: As of October 10, 2025, version numbering has changed. v2.4.1 is now **v2.4.1-CLASSIC** and v2.5.x has been renumbered to **v3.0.0-beta** to reflect the major architectural change. Where this guide mentions `Supervertaler_v2.4.1.py`, the current filename is `Supervertaler_v2.4.1-CLASSIC.py`. See [docs/VERSION_RENUMBERING_v3.0.0.md](docs/VERSION_RENUMBERING_v3.0.0.md) for details.

**Last Updated**: October 10, 2025  
**Covers**: v2.4.1-CLASSIC (Production - Stable) | v3.0.0-beta (Beta - CAT Editor)

---

## 📖 Quick Navigation

### For New Users
- **[Installation Guide](#installation--setup)** - Get started on Windows, macOS, or Linux
- **[API Keys Setup](#api-keys-setup)** - Configure your AI provider keys
- **[Quick Start](#quick-start-guide)** - First translation in 5 minutes

### For Professional Translators
- **[CAT Tool Integration](#cat-tool-integration)** - Essential workflow for professional translators
- **[Bilingual DOCX Workflow](#bilingual-docx-workflow-v241)** - v2.4.1-CLASSIC: Direct bilingual file handling
- **[Translation Workspace (v3.0.0-beta)](#translation-workspace-v250)** - Interactive CAT editor (beta)

### Feature Guides
- **[Translation Mode](#translation-mode)** - Full document translation
- **[Proofreading Mode](#proofreading-mode)** - Review and improve translations
- **[Project Library](#project-library)** - Workspace management
- **[Prompt Library](#prompt-library)** - Domain-specific prompts
- **[Translation Memory](#translation-memory)** - TM integration
- **[Troubleshooting](#troubleshooting)** - Common issues and solutions

---

## Version Guide

### v2.4.1-CLASSIC (Production - Stable) ✅ **RECOMMENDED**
**Filename**: `Supervertaler_v2.4.1-CLASSIC.py`  
**Status**: Production-ready, fully tested  
**Best For**: Professional translation projects requiring stability

**Key Features**:
- ✅ Bilingual DOCX import/export with formatting preservation
- ✅ GPT-5 full support with automatic parameter handling
- ✅ Switch Languages button for efficient workflow
- ✅ Multiple AI providers (OpenAI, Claude, Gemini)
- ✅ Project Library with workspace management
- ✅ Domain-specific prompt collections
- ✅ Translation Memory integration (TMX/TXT)
- ✅ Multimodal image processing for figures
- ✅ Session reporting and comprehensive logging

### v2.5.0 (Experimental - CAT Editor Development) 🧪
**Filename**: `Supervertaler_v2.5.0 (experimental - CAT editor development).py`  
**Status**: Under active development  
**Best For**: Testing new features, providing feedback

**New Experimental Features**:
- 🧪 Interactive Translation Workspace (grid interface)
- 🧪 Dual selection mode (memoQ-style)
- 🧪 Inline editing capabilities
- 🧪 Find/Replace functionality
- 🧪 Real-time status tracking
- 🧪 Enhanced project save/load

**Note**: Documentation for v2.5.0 features is in progress. See `docs/implementation/` for technical details.

---

## Table of Contents

1. [Installation & Setup](#installation--setup)
   - [Windows Installation](#windows-installation)
   - [macOS Installation](#macos-installation)
   - [Linux Installation](#linux-installation)
2. [API Keys Setup](#api-keys-setup)
3. [CAT Tool Integration](#cat-tool-integration)
4. [Bilingual DOCX Workflow (v2.4.1)](#bilingual-docx-workflow-v241)
5. [Translation Workspace (v2.5.0)](#translation-workspace-v250)
6. [Quick Start Guide](#quick-start-guide)
7. [Prompt Library](#prompt-library)
8. [Custom Prompt Library](#custom-prompt-library)
9. [Project Library](#project-library)
10. [Translation Mode](#translation-mode)
11. [Proofreading Mode](#proofreading-mode)
12. [Context Sources](#context-sources)
13. [Translation Memory](#translation-memory)
14. [AI Provider Settings](#ai-provider-settings)
15. [Troubleshooting](#troubleshooting)
16. [Advanced Tips](#advanced-tips)

---

## Installation & Setup

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.13+, or Linux (any modern distribution)
- **Python**: 3.8 or higher (3.12 recommended)
- **Disk Space**: ~50 MB for Supervertaler + dependencies
- **Internet**: Required for AI API calls
- **RAM**: 4GB minimum, 8GB recommended for large documents
- **API Keys**: At least one of:
  - OpenAI (GPT-4, GPT-5, etc.)
  - Anthropic (Claude 3.5 Sonnet, etc.)
  - Google (Gemini 2.5 Pro, etc.)

---

### Windows Installation

#### Step 1: Check Python Installation

Open PowerShell or Command Prompt and run:
```powershell
python --version
```

**Expected output**: `Python 3.8.0` or higher

**If Python is missing or outdated**:
1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
4. Restart your computer

#### Step 2: Download Supervertaler

**Option A - Git** (recommended):
```powershell
# Install git from https://git-scm.com/download/win if needed
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler
```

**Option B - Direct Download**:
1. Go to https://github.com/michaelbeijer/Supervertaler
2. Click green "Code" button → "Download ZIP"
3. Extract to your desired location (e.g., `C:\Users\YourName\Supervertaler`)
4. Navigate to folder in PowerShell

#### Step 3: Install Dependencies

```powershell
pip install anthropic openai google-generativeai python-docx pillow lxml
```

**Expected output**:
```
Successfully installed anthropic-0.x.x openai-1.x.x google-generativeai-0.x.x python-docx-1.x.x pillow-10.x.x lxml-5.x.x
```

**If pip command not found**:
```powershell
python -m pip install anthropic openai google-generativeai python-docx pillow lxml
```

#### Step 4: Set Up API Keys

See [API Keys Setup](#api-keys-setup) section below.

#### Step 5: Launch Application

```powershell
python Supervertaler_v2.4.1.py
```

---

### macOS Installation

#### Step 1: Check Python Installation

Most Macs come with Python pre-installed. Check your version:

```bash
python3 --version
```

**Expected output**: `Python 3.8.0` or higher

**If Python is missing or outdated**:

**Option A - Homebrew** (recommended):
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Option B - Official Installer**:
1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer
3. Check "Add Python to PATH" during installation

#### Step 2: Download Supervertaler

**Option A - Git** (recommended):
```bash
# Install git if needed
brew install git

# Clone repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler
```

**Option B - Direct Download**:
1. Go to https://github.com/michaelbeijer/Supervertaler
2. Click green "Code" button → "Download ZIP"
3. Extract to your desired location
4. Open Terminal and navigate:
   ```bash
   cd ~/Downloads/Supervertaler-main
   ```

#### Step 3: Install Dependencies

```bash
pip3 install anthropic openai google-generativeai python-docx pillow lxml
```

**Expected output**:
```
Successfully installed anthropic-0.x.x openai-1.x.x google-generativeai-0.x.x python-docx-1.x.x pillow-10.x.x lxml-5.x.x
```

**If pip3 command not found**:
```bash
python3 -m pip install anthropic openai google-generativeai python-docx pillow lxml
```

#### Step 4: Set Up API Keys

See [API Keys Setup](#api-keys-setup) section below.

#### Step 5: Launch Application

```bash
python3 Supervertaler_v2.4.1.py
```

---

### Linux Installation

#### Step 1: Check Python Installation

```bash
python3 --version
```

**Expected output**: `Python 3.8.0` or higher

**If Python is missing or outdated**:

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

**Fedora/RHEL**:
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

**Arch Linux**:
```bash
sudo pacman -S python python-pip tk
```

#### Step 2: Download Supervertaler

**Option A - Git** (recommended):
```bash
# Install git if needed
sudo apt install git  # Ubuntu/Debian
sudo dnf install git  # Fedora
sudo pacman -S git    # Arch

# Clone repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler
```

**Option B - Direct Download**:
1. Download ZIP from https://github.com/michaelbeijer/Supervertaler
2. Extract: `unzip Supervertaler-main.zip`
3. Navigate: `cd Supervertaler-main`

#### Step 3: Install Dependencies

```bash
pip3 install anthropic openai google-generativeai python-docx pillow lxml
```

**If permission error**:
```bash
pip3 install --user anthropic openai google-generativeai python-docx pillow lxml
```

#### Step 4: Set Up API Keys

See [API Keys Setup](#api-keys-setup) section below.

#### Step 5: Launch Application

```bash
python3 Supervertaler_v2.4.1.py
```

---

## API Keys Setup

### 🔒 Security First

**CRITICAL**: Your API keys are like passwords - they give access to your paid AI services. Supervertaler is designed to keep your keys 100% secure and local to your computer.

#### What's Protected ✅

- **`api_keys.txt`** - Your actual API keys (NEVER uploaded to GitHub)
- **`user data/System_prompts_private/`** - Your private system prompts
- **`user data/Projects_private/`** - Your private translation projects

These are all listed in `.gitignore` and will never be synced to version control.

#### What's Shared ✅

- **`api_keys.example.txt`** - Template file with instructions (safe to share)
- **`user data/System_prompts/`** - Public example prompts
- **`user data/Projects/`** - Public example projects

---

### Quick Setup (3 Steps)

#### Step 1: Copy the Example File

**Windows (PowerShell)**:
```powershell
Copy-Item "api_keys.example.txt" -Destination "api_keys.txt"
```

**macOS/Linux**:
```bash
cp api_keys.example.txt api_keys.txt
```

**Manual**: Right-click `api_keys.example.txt` → Copy → Paste → Rename to `api_keys.txt`

#### Step 2: Get Your API Keys

You only need keys for the AI providers you want to use. You don't need all three.

##### OpenAI (GPT-4, GPT-5, GPT-4o)
1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Name it (e.g., "Supervertaler")
5. Copy the key (starts with `sk-proj-` or `sk-`)
6. **Save it immediately** - you can't see it again!

**Pricing**: Pay-per-use, ~$0.01-0.15 per 1000 words depending on model

##### Anthropic Claude (Claude 3.5 Sonnet, Claude 3 Opus)
1. Go to: https://console.anthropic.com/settings/keys
2. Sign in or create account
3. Click "Create Key"
4. Name it (e.g., "Supervertaler")
5. Copy the key (starts with `sk-ant-`)
6. **Save it immediately** - you can't see it again!

**Pricing**: Pay-per-use, ~$0.015-0.075 per 1000 words depending on model

##### Google Gemini (Gemini 2.5 Pro, Gemini 1.5 Flash)
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API key"
4. Select or create a Google Cloud project
5. Copy the key (starts with `AIzaSy`)
6. **Save it immediately**

**Pricing**: Free tier available (60 requests/minute), then pay-per-use

#### Step 3: Edit api_keys.txt

Open `api_keys.txt` in a text editor (Notepad, VS Code, TextEdit, nano, etc.) and:

1. **Remove the `#` symbol** from the lines you want to use
2. **Replace the placeholder** with your actual key
3. **Save the file**

**Before**:
```
#openai = YOUR_OPENAI_KEY_HERE
#claude = YOUR_CLAUDE_KEY_HERE
#google = YOUR_GOOGLE_KEY_HERE
```

**After** (example with OpenAI and Claude keys):
```
openai = sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
claude = sk-ant-xyz789abc456def123ghi890jkl567mno234pqr901stu678vwx345
#google = YOUR_GOOGLE_KEY_HERE
```

**Important**: 
- No spaces around the `=` sign (or one space on each side is fine)
- No quotes around the key
- One key per line
- Lines starting with `#` are ignored (comments)

---

### Verification

After setting up API keys, launch Supervertaler and click **"List Models"** button to verify connectivity:

**Successful connection shows**:
```
--- Listing Models for OpenAI ---
Available OpenAI models:
1. gpt-5
2. gpt-4o
3. gpt-4
...
```

**If you see errors**:
- Check that API key is copied correctly (no extra spaces)
- Verify key is active in provider dashboard
- Ensure you have credits/quota available
- Check internet connection

---

## CAT Tool Integration

**Supervertaler is designed for professional translators using CAT tools** and integrates seamlessly into existing translation workflows. Understanding this integration is essential for getting the most out of Supervertaler.

### 🎯 Why CAT Tool Integration?

Supervertaler doesn't directly translate .docx, .xlsx, .pptx files because:
1. **Complexity**: Creating and maintaining support for all file formats would be extremely complex
2. **Efficiency**: CAT tools already excel at this with decades of development
3. **Quality**: Segmentation is crucial for consistent, high-quality translations
4. **Integration**: Professional translators already have established CAT tool workflows

### 🔄 Translation Workflow

#### Traditional Workflow (v2.4.1 and earlier):

**Input Process**:
1. **Import into CAT Tool**: Open source file in your CAT tool (memoQ, Trados, etc.)
2. **Pre-translate if needed**: Apply existing TM/terminology
3. **Export bilingual table**: Generate bilingual .docx or .rtf
4. **Extract source column**: Copy all source text rows
5. **Create .txt file**: Paste into plain text file, one segment per line

**Supervertaler Processing**:
- **Input**: Plain text file with source segments
- **Processing**: AI translation with full document context and multimodal intelligence
- **Output**: Tab-separated .txt file + TMX translation memory

**CAT Tool Re-integration**:
1. **Import TMX**: Add generated TMX file to your CAT tool project
2. **Apply translations**: Use exact matches from TMX or copy target column
3. **Continue workflow**: Review, edit, and deliver using your CAT tool

#### New Bilingual Workflow (v2.4.1+):

See [Bilingual DOCX Workflow](#bilingual-docx-workflow-v241) for streamlined import/export process.

### 🎯 Why This Approach Works

- **CAT Tools**: Excel at file format handling, project management, and client delivery
- **Supervertaler**: Provides superior AI translation with multicontextual intelligence
- **Combined**: Professional translation workflow with enhanced quality and efficiency

---

## Bilingual DOCX Workflow (v2.4.1)

🎉 **NEW in v2.4.1**: Direct import/export of bilingual DOCX files with formatting preservation!

### Quick Start (5 Steps)

#### Step 1: Export from Your CAT Tool
- Open your project in memoQ (or Trados Studio, CafeTran, etc.)
- Export bilingual DOCX file (File → Export → Bilingual DOCX)
- Save to your working folder

#### Step 2: Import to Supervertaler
- Launch `Supervertaler_v2.4.1.py`
- Click green **"📄 Import memoQ Bilingual DOCX"** button
- Select your exported bilingual DOCX file
- ✅ Supervertaler extracts source segments and formatting automatically

#### Step 3: Configure Translation
- **Source Language**: Auto-detected from bilingual file
- **Target Language**: Auto-detected from bilingual file
- **AI Provider**: Choose your preferred service (OpenAI, Anthropic, Google, etc.)
- **Model**: Select appropriate model for your content
- **Custom Prompt** (optional): Choose specialized prompt if needed

#### Step 4: Translate
- Click **"Translate"** button
- Supervertaler processes all segments with AI
- Progress bar shows translation status
- Success message shows statistics (e.g., "15 formatting preserved")

#### Step 5: Export Back to Bilingual DOCX
- Click blue **"💾 Export to Bilingual DOCX"** button
- File is saved with `_translated` suffix
- ✅ Formatting preserved (bold, italic, underline)
- ✅ CAT tool tags preserved
- ✅ Segment IDs maintained
- **Reimport to your CAT tool** - Ready to use!

---

### What's Preserved

#### ✅ Formatting
- **Bold text** - Full segments or partial (e.g., names at beginning)
- *Italic text* - Full segments
- <u>Underline</u> - Including on CAT tags and URLs
- **Success rate**: 100% in testing

#### ✅ CAT Tool Tags
- **memoQ**: `{1}example{2}` → Asymmetric bracket-brace pairs
- **Trados**: `<410>example</410>` → XML-style tags
- **CafeTran**: `|1|example|2|` → Pipe-delimited tags
- All tag formats preserved perfectly

#### ✅ Metadata
- Segment IDs (numbers + UUIDs)
- Project information
- Table structure
- Status updates (set to "Confirmed" after translation)

---

### Behind the Scenes

**What Supervertaler Does**:

1. **Import Phase**:
   - Reads bilingual DOCX table structure
   - Extracts source text from column 1 (Source Language)
   - Detects bold, italic, underline formatting in each run
   - Stores formatting map for each segment
   - Creates temporary .txt file with source text
   - Auto-configures input/output file paths

2. **Translation Phase**:
   - Uses standard Supervertaler translation workflow
   - AI processes source segments → target translations
   - Preserves all context and custom prompts
   - Creates tab-delimited output (source\ttarget)

3. **Export Phase**:
   - Opens original bilingual DOCX file
   - Writes translations to column 2 (Target Language)
   - Applies formatting based on source formatting map:
     - Full segment formatting (>60% threshold)
     - Partial formatting (beginning detection)
     - CAT tag formatting preservation
   - Updates status column to "Confirmed"
   - Saves file ready for CAT tool reimport

---

### Pro Tips

#### Tip 1: Test with Small File First
- Try with 10-20 segments initially
- Verify reimport works in your CAT tool
- Check formatting preservation
- Then scale up to full projects

#### Tip 2: Formatting Preservation Best Practices
- Keep formatting consistent in source text
- Use CAT tool's formatting preservation features
- Review formatting in bilingual export before translation
- Spot-check formatting in translated output

#### Tip 3: CAT Tool Tag Compatibility
- **memoQ**: Full support for all tag types
- **Trados Studio**: XML-style tags fully preserved
- **CafeTran**: Pipe-delimited tags maintained
- **Other tools**: Test with sample file first

#### Tip 4: Quality Assurance Workflow
1. Import TMX from previous translations for consistency
2. Use custom prompts for domain-specific guidance
3. Review translated bilingual DOCX before final reimport
4. Run CAT tool QA checks after reimport

---

### Trados Studio Re-Import: Critical Information ⚠️

**Important Discovery (October 2025)**: Trados Studio has specific behavior for bilingual review file re-import that differs from other CAT tools.

#### ✅ The Rule
> **Trados Studio only imports changes to segments that were translated BEFORE the export.**
>
> Empty/untranslated segments at export time → Changes are **ignored** during re-import

**Source**: [RWS Official Documentation](https://docs.rws.com/en-US/trados-studio-2022-980998/reviewing-bilingual-files-with-word-514802)

#### 📋 Workflow for Trados Studio

**Correct Workflow** (Changes will be imported):
1. In Trados: Pre-translate document (MT, TM, or manual)
2. Export bilingual review file (`yourfile.docx.review.docx`)
3. In Supervertaler: Import → Edit/Translate → Export
4. In Trados: Re-import bilingual file
5. ✅ **Changes are applied to pre-translated segments**

**Incorrect Workflow** (Changes will be ignored):
1. In Trados: Export with empty/untranslated segments
2. In Supervertaler: Add translations
3. In Trados: Re-import
4. ❌ **Changes are silently ignored** (segments remain empty)

#### 💡 Best Practice

**Pre-translate in Trados first**, then use Supervertaler for:
- Post-editing MT output
- Improving TM fuzzy matches
- Refining translations
- Consistency improvements

#### ✅ What Works

- ✅ Editing segments that had MT translation
- ✅ Improving segments with TM matches (100%, fuzzy)
- ✅ Refining manually translated segments
- ✅ Post-editing after Trados pre-translation
- ✅ Tag styling (properly preserved - italic, pink color)
- ✅ XML declaration (matches Trados format exactly)

#### ❌ What Doesn't Work

- ❌ Adding translations to completely empty segments
- ❌ First-pass translation of untranslated content

#### 🎯 Recommended Trados Workflow

1. **Prepare in Trados:**
   ```
   - Create project with source files
   - Pre-translate with MT (DeepL, Google, etc.)
   - OR apply TM matches
   - Export bilingual review file
   ```

2. **Process in Supervertaler:**
   ```
   - Import bilingual DOCX
   - Review/edit/improve translations
   - Export back to bilingual DOCX
   ```

3. **Finalize in Trados:**
   ```
   - Re-import bilingual file
   - Run QA checks
   - Deliver project
   ```

#### 📝 Note for v3.0.0-beta Users

The v3.0.0-beta CAT editor version handles Trados files with:
- Automatic tag style preservation
- XML declaration format matching
- Segment UUID preservation
- Full metadata compatibility

**All fixes are now integrated and working!** ✅

---

### 💰 Cost-Saving Alternative: Copy Source to Target

**Problem**: Pre-translating in Trados/memoQ/CafeTran with MT costs money and consumes API credits.

**Solution**: Use Supervertaler's "Copy Source to Target" feature to prepare files for re-import **without** paying for MT.

#### How It Works (v3.0.0-beta)

Instead of pre-translating with expensive MT in your CAT tool, you can:

1. **Export** bilingual file with **empty targets** from Trados/memoQ/CafeTran
2. **Import** into Supervertaler v3.0.0-beta
3. **Copy Source to Target (All)** from Edit menu
4. **Translate** with Supervertaler's AI (uses your own API keys)
5. **Export** back to bilingual format
6. **Re-import** into Trados/memoQ/CafeTran

#### Why This Works

- **Trados/memoQ/CafeTran** only accept changes to segments with existing targets
- **Copying source to target** gives each segment a "placeholder" translation
- **Your CAT tool** now sees them as "translated" segments (even though they're just source text)
- **On re-import**, your CAT tool accepts the AI translations ✅

#### Cost Comparison

| Method | Cost | Notes |
|--------|------|-------|
| **Trados MT Pre-translate** | ~€20-40 per 1M characters | Uses Trados credits |
| **memoQ MT Pre-translate** | Varies by MT engine | Separate MT subscription |
| **DeepL/Google MT** | ~€20 per 1M characters | API costs |
| **Copy Source → AI Translate** | ~€2-5 per 1M chars | Your own OpenAI/Claude/Gemini keys |

**Savings**: 80-90% compared to commercial MT! 💰

#### Step-by-Step (v3.0.0-beta)

1. **In Trados/memoQ/CafeTran:**
   - Export bilingual file (empty targets = OK!)

2. **In Supervertaler:**
   ```
   File → Import → [Trados/memoQ/CafeTran] Bilingual DOCX
   [All segments load with empty targets]
   
   Edit → Copy Source to Target (All Segments)
   [Confirmation dialog appears - click Yes]
   [Now all targets contain source text]
   
   Translate → Translate All Untranslated
   [AI translates all segments using YOUR API keys]
   
   File → Export → Export to [Trados/memoQ/CafeTran]
   ```

3. **Back in Trados/memoQ/CafeTran:**
   - Re-import bilingual file
   - ✅ All translations are accepted!

#### ⚠️ Important Notes

- **Source text in target**: Before translating, your targets will contain source language text. This is intentional and temporary.
- **Translate immediately**: After copying, translate with AI before exporting (don't export with source=target).
- **QA checks**: Your CAT tool may flag these as "identical source/target" until you translate.
- **Version requirement**: "Copy Source to Target" feature requires v3.0.0-beta or later.

#### When to Use This Workflow

✅ **Use Copy Source to Target when:**
- You want to save money on MT costs
- You have your own OpenAI/Claude/Gemini API keys
- You're working with large volumes
- MT quality isn't critical (you'll review anyway)

❌ **Pre-translate in CAT tool when:**
- Client requires specific MT engine (DeepL Pro, etc.)
- You need MT match % in analysis reports
- Project includes MT QA requirements
- Working with very specialized MT models

---

## Translation Workspace (v2.5.0)

🧪 **EXPERIMENTAL FEATURE** - Under active development

**Note**: v2.5.0 introduces an interactive Translation Workspace with grid-based editing. This is an experimental feature under active development. Documentation is being updated as features stabilize.

### Key Features (Experimental)

- **Interactive Grid Interface**: Edit translations directly in spreadsheet-like view
- **Dual Selection Mode**: memoQ-style selection of source and target segments
- **Inline Editing**: Click to edit any segment immediately
- **Find/Replace**: Search and replace across all segments
- **Status Tracking**: Monitor translation progress visually
- **Project Save/Load**: Complete workspace state preservation

### Current Status

This feature is under active development. For the latest technical details, see:
- `docs/implementation/TRANSLATION_WORKSPACE_REDESIGN.md`
- `docs/user_guides/WORKSPACE_VISUAL_GUIDE.md`

### Feedback Welcome

If you're testing v2.5.0, please provide feedback on:
- User interface clarity and usability
- Performance with large files
- Feature requests and suggestions
- Bug reports and issues

---

## Quick Start Guide

### Your First Translation (5 Minutes)

#### Step 1: Prepare Your Input

Create a simple text file with one segment per line:

**Example** (`test_translation.txt`):
```
Hello, world!
This is a test translation.
AI-powered translation is amazing.
```

#### Step 2: Launch Supervertaler

```bash
python Supervertaler_v2.4.1.py
```

#### Step 3: Configure Basic Settings

1. **Input File**: Click "Browse" → Select your `test_translation.txt`
2. **Source Language**: Type "English"
3. **Target Language**: Type "Dutch" (or your preferred language)
4. **Provider**: Select "Claude" (or your configured provider)
5. **Model**: Select "claude-3-5-sonnet-20241022"

#### Step 4: Run Translation

Click **"Start Process"** button

Watch the processing log for progress:
```
Processing chunk 1 of 1...
Successfully processed chunk 1 of 1
Translation complete!
```

#### Step 5: Review Output

Find two new files in your input file's directory:
- **`test_translation_translated.txt`**: Tab-separated source and target
- **`test_translation_translated.tmx`**: Translation memory file

**Example output** (`test_translation_translated.txt`):
```
Hello, world!	Hallo, wereld!
This is a test translation.	Dit is een testvertaling.
AI-powered translation is amazing.	AI-aangedreven vertaling is geweldig.
```

### Next Steps

Now that you've completed your first translation:

1. **Explore Context Sources**: Add Translation Memory for consistency
2. **Try Domain Prompts**: Select a specialized prompt from Prompt Library
3. **Test Proofreading**: Use proofreading mode to improve existing translations
4. **Create a Project**: Save your configuration in Project Library
5. **Advanced Features**: Explore tracked changes and multimodal image processing

---

## Prompt Library

The Prompt Library provides access to 8 professionally crafted domain-specific prompt collections, each optimised for different types of content.

### Available Prompt Collections

#### 🧬 Medical Translation Specialist
- **Focus**: Patient safety and regulatory accuracy
- **Strengths**: Medical terminology, pharmaceutical precision, clinical trial documentation
- **Use Cases**: Medical device manuals, pharmaceutical documentation, clinical reports
- **Key Features**:
  - Emphasis on patient safety and regulatory compliance
  - Preservation of medical terminology and drug names
  - Attention to dosage information and warnings
  - Formal, professional medical register

#### ⚖️ Legal Translation Specialist
- **Focus**: Juridical precision and formal register
- **Strengths**: Contract language, legal terminology, regulatory compliance
- **Use Cases**: Contracts, legal agreements, regulatory filings, court documents
- **Key Features**:
  - Juridical precision and formal legal register
  - Preservation of legal terms and Latin phrases
  - Attention to contractual obligations and rights
  - Compliance with legal translation standards

#### 🏭 Patent Translation Specialist
- **Focus**: Technical precision and legal compliance
- **Strengths**: Patent claims, technical descriptions, invention disclosure
- **Use Cases**: Patent applications, technical specifications, invention descriptions
- **Key Features**:
  - Technical and legal precision combined
  - Preservation of patent claim structure
  - Attention to technical terminology
  - Compliance with patent office requirements

#### 💰 Financial Translation Specialist
- **Focus**: Banking terminology and market conventions
- **Strengths**: Financial instruments, regulatory compliance, market analysis
- **Use Cases**: Financial reports, banking documents, investment materials
- **Key Features**:
  - Banking and financial terminology expertise
  - Attention to numerical accuracy and currency
  - Formal business register
  - Regulatory compliance awareness

#### ⚙️ Technical Translation Specialist
- **Focus**: Engineering accuracy and safety warnings
- **Strengths**: Technical manuals, safety procedures, industrial processes
- **Use Cases**: User manuals, technical specifications, safety documentation
- **Key Features**:
  - Engineering terminology precision
  - Safety warning preservation and emphasis
  - Technical accuracy in procedures
  - Clear, unambiguous language

#### 🎨 Marketing & Creative Translation
- **Focus**: Cultural adaptation and brand consistency
- **Strengths**: Transcreation, cultural nuance, brand voice maintenance
- **Use Cases**: Marketing materials, advertising copy, brand communications
- **Key Features**:
  - Transcreation over literal translation
  - Cultural adaptation and localization
  - Brand voice consistency
  - Persuasive, engaging language

#### ₿ Cryptocurrency & Blockchain Specialist
- **Focus**: DeFi protocols and Web3 terminology
- **Strengths**: Blockchain technology, smart contracts, crypto trading
- **Use Cases**: Crypto exchanges, DeFi platforms, blockchain documentation
- **Key Features**:
  - Blockchain and crypto terminology
  - DeFi protocol accuracy
  - Technical precision with emerging technology
  - Security and safety emphasis

#### 🎮 Gaming & Entertainment Specialist
- **Focus**: Cultural localization and user experience
- **Strengths**: Game mechanics, cultural adaptation, user interface
- **Use Cases**: Video games, entertainment software, mobile apps
- **Key Features**:
  - Game terminology and mechanics
  - Cultural localization (not just translation)
  - Player experience optimization
  - Fun, engaging tone appropriate to genre

### Using Domain Prompts

1. **Selection**: Click "Prompt Library" to see available collections
2. **Activation**: Click desired prompt - ⚡ symbol indicates active selection
3. **Review**: Hover over prompt to see description
4. **Deactivation**: Click active prompt again to deselect
5. **Edit**: Use "Edit Active Prompt" for project-specific adjustments

**Pro Tip**: Domain prompts work best when combined with relevant context sources (TM, tracked changes, custom instructions).

---

## Custom Prompt Library

Create, save, and manage your own specialized system prompts for recurring project types or specific client requirements.

### Creating Custom Prompts

#### Step 1: Open Editor
Click "Custom Prompt Library" → "Create New Prompt"

#### Step 2: Design Your Prompt

Write your system prompt with template variables:

```
You are a specialist in {source_lang} to {target_lang} translation
for [specific domain/client].

Focus on:
- [Specific requirements]
- [Terminology preferences]
- [Style guidelines]

CRITICAL FOCUS:
- [Key challenge 1]
- [Key challenge 2]
```

#### Step 3: Use Template Variables

- `{source_lang}` - Automatically replaced with source language
- `{target_lang}` - Automatically replaced with target language

**Example**:
```
You are an expert {source_lang} to {target_lang} translator
specializing in automotive technical documentation.
```

Becomes (when translating English to Dutch):
```
You are an expert English to Dutch translator
specializing in automotive technical documentation.
```

#### Step 4: Save Prompt

Give it a descriptive name and save to your library:
- Clear, descriptive names (e.g., "Client_XYZ_Technical_Manual")
- Include domain and client information
- Save to `user data/System_prompts_private/` for privacy

### Managing Your Library

**Organization Tips**:
- Use clear, descriptive names
- Include domain and client information in names
- Regular cleanup of outdated prompts
- Export important prompts for backup

**File Structure**:
```
user data/System_prompts_private/
├── Client_ABC_Legal_Contracts.json
├── Technical_Manual_Safety_Focus.json
├── Marketing_Creative_Transcreation.json
└── README.md
```

### Best Practices

#### Effective Prompt Design

1. **Clear Role Definition**: Specify translator expertise level
   ```
   You are an expert medical translator with 10+ years experience...
   ```

2. **Domain Context**: Include relevant industry knowledge
   ```
   You specialize in pharmaceutical regulatory documentation...
   ```

3. **Style Guidelines**: Define tone, formality, terminology preferences
   ```
   Use formal medical register. Preserve drug names. Emphasize safety.
   ```

4. **Template Variables**: Use for reusability
   ```
   Translating from {source_lang} to {target_lang}...
   ```

5. **Specific Instructions**: Address common challenges
   ```
   CRITICAL:
   - Never translate drug names
   - Preserve all dosage information exactly
   - Emphasize safety warnings in target language
   ```

#### Example Structure

```
You are an expert {source_lang} to {target_lang} translator specializing in [domain].

REQUIREMENTS:
- Maintain [specific style/tone]
- Use [terminology preferences]
- Follow [specific guidelines]

CRITICAL FOCUS:
- [Key challenge 1]
- [Key challenge 2]
- [Key challenge 3]

EXAMPLES:
- [Term 1]: [Translation preference]
- [Term 2]: [Translation preference]
```

---

## Project Library

The Project Library enables complete workspace management, allowing you to save and restore entire application configurations for different clients, projects, or content types.

### Creating Projects

#### Step 1: Configure Your Workspace

Set up all your settings:
- **File Paths**: Input file, TM, tracked changes, images
- **Language Pair**: Source and target languages
- **AI Provider and Model**: Selected AI service
- **Custom Instructions**: Project-specific guidance
- **Active Prompts**: Domain-specific prompts

#### Step 2: Save Project

1. Click **"Project Library"** button
2. Click **"Save Current Configuration"**
3. Enter a descriptive name

**Naming Convention Examples**:
- `Client_ProjectName_ContentType`
- `ABC_Corp_TechnicalManuals`
- `XYZ_Legal_Contracts_2024`
- `Medical_Device_Manual_ClientABC`

#### Step 3: Verify Save

Project saved to `user data/Projects/` or `user data/Projects_private/` folder as JSON file

### Loading Projects

#### Step 1: Browse Library

Click **"Project Library"** to view saved configurations

#### Step 2: Select Project

Click desired project from the list

#### Step 3: Automatic Loading

All settings restored instantly:
- ✅ File paths updated to saved locations
- ✅ Language pair set
- ✅ AI provider and model selected
- ✅ Custom instructions loaded
- ✅ Active prompts restored

### Project Management

**Organization Strategy**:
- **Client-Based**: Separate projects per client
- **Content-Based**: Group by content type (legal, technical, marketing)
- **Time-Based**: Include dates for version control

**File Management**:
- Projects stored as JSON files in `user data/Projects/` folder
- Private projects in `user data/Projects_private/` (excluded from git)
- Include timestamps for version tracking
- Export important projects for backup
- Cross-platform path compatibility (Windows, macOS, Linux)

### Advanced Features

**Cross-Platform Support**:
- File paths automatically adjust between operating systems
- Clickable folder paths work on Windows, macOS, and Linux
- Seamless collaboration across different platforms

**Version Control**:
- Projects include creation timestamps
- Easy to track configuration evolution
- Backup and restore capabilities

---

## Translation Mode

Translation mode is designed for translating source text into target language with maximum accuracy and context awareness.

### Input Requirements

**File Format**: Plain text file (.txt)  
**Content Structure**: One segment per line

**Example**:
```
CLAIMS
A vehicle control method, comprising:
obtaining sensor information of different modalities...
sending the short-cycle message information to a first data model...
```

### Configuration Options

#### Basic Settings
- **Input File**: Source text file path (Browse button)
- **Source Language**: Source language (e.g., "English", "German")
- **Target Language**: Target language (e.g., "Dutch", "French")
- **Switch Languages**: ⇄ button to quickly swap source/target
- **Chunk Size**: Number of lines processed per AI request (default: 50)

#### AI Provider Selection

**OpenAI Models**:
- **GPT-5**: Latest reasoning model - excellent for complex content
- **GPT-4o**: Multimodal capabilities with strong general performance
- **GPT-4**: Reliable baseline performance
- **GPT-4-turbo**: Enhanced context window

**Claude Models**:
- **Claude-3.5-Sonnet**: Excellent creative and nuanced content
- **Claude-3-Haiku**: Fast processing for simpler content

**Gemini Models**:
- **Gemini-2.5-Pro**: Strong technical performance
- **Gemini-1.5-Flash**: Fast processing option

### Context Sources

#### Translation Memory (TM)
**Supported Formats**: TMX, TXT (tab-separated)  
**Benefits**: 
- Exact matches provide instant consistency
- Fuzzy matches guide similar content
- Builds institutional knowledge

#### Custom Instructions
**Purpose**: Project-specific guidance

**Examples**:
```
This is a technical manual for automotive engineers.
Maintain formal tone and use metric measurements.
Preserve all part numbers exactly as written.
```

#### Tracked Changes
**Input**: DOCX files with revision tracking or TSV editing patterns  
**Function**: AI learns from human editing patterns  
**Benefits**: Adapts to preferred terminology and style choices

#### Document Images
**Format**: PNG, JPG, GIF supported  
**Function**: Visual context for figure references  
**Usage**: AI automatically detects figure mentions and provides relevant images

### Domain-Specific Prompts

Choose from 8 professional prompt collections:
- Medical, Legal, Patent, Financial
- Technical, Marketing, Crypto, Gaming

Active prompts shown with ⚡ symbol.

### Output Files

#### Primary Output: `filename_translated.txt`
Tab-separated source and target:
```
Source Text[TAB]Translated Text
CLAIMS[TAB]CONCLUSIES
A vehicle control method[TAB]Een voertuigbesturingsmethode
```

#### Translation Memory: `filename_translated.tmx`
Standard TMX format compatible with:
- memoQ
- Trados Studio
- CafeTran Espresso
- Wordfast Pro
- OmegaT

#### Session Report: `filename_translated_report.md`
Comprehensive documentation including:
- Complete AI prompts used
- Session settings and configuration
- Processing statistics
- Context sources utilized
- Timestamp and version information

### Best Practices

**File Preparation**:
1. Extract clean source text from CAT tool bilingual export
2. One segment per line, no empty lines
3. Preserve original segmentation from CAT tool
4. Save as UTF-8 encoded text file

**Context Optimization**:
1. Load relevant Translation Memory for consistency
2. Add project-specific custom instructions
3. Include tracked changes from similar previous work
4. Provide document images for visual context

**Quality Assurance**:
1. Review session report for prompt transparency
2. Import generated TMX into CAT tool for exact matches
3. Spot-check translations against original document context
4. Use proofreading mode for revision and refinement

---

## Proofreading Mode

Proofreading mode is designed for revising and improving existing translations, providing detailed change tracking and explanatory comments.

### Input Requirements

**File Format**: Tab-separated text file (.txt)  
**Structure**: Source{TAB}Target format

**Example**:
```
Source Text[TAB]Existing Translation
CLAIMS[TAB]BEWERINGEN
A vehicle control method[TAB]Een werkwijze voor voertuigbesturing
```

### Configuration

#### Basic Settings
- **Input File**: Bilingual tab-separated file
- **Source/Target Languages**: Language pair for the content
- **Provider/Model**: AI selection for proofreading analysis

#### Context Sources (Same as Translation Mode)
- Translation Memory for consistency checking
- Custom instructions for revision guidelines
- Tracked changes for learning preferred revision patterns
- Document images for visual context verification

### Proofreading Process

#### Analysis Approach

The AI performs comprehensive revision focusing on:

**Accuracy Assessment**:
- Terminology consistency
- Technical precision
- Cultural appropriateness
- Completeness verification

**Quality Enhancement**:
- Grammar and syntax improvement
- Style and tone optimization
- Readability enhancement
- Professional register maintenance

**Consistency Checking**:
- Cross-reference with Translation Memory
- Terminology standardization
- Style guide compliance
- Figure reference accuracy

### Output Format

#### Revised Translation: `filename_proofread.txt`

Three-column format with explanations:
```
Source[TAB]Revised_Translation[TAB]Change_Comments
CLAIMS[TAB]CONCLUSIES[TAB]Changed from "BEWERINGEN" to standard patent terminology
A vehicle control method[TAB]Een voertuigbesturingsmethode[TAB]Simplified compound structure for clarity
```

#### Column Structure:
1. **Source**: Original source text
2. **Revised_Translation**: AI-improved translation
3. **Change_Comments**: Explanation of revisions made

#### Session Report: `filename_proofread_report.md`
- Complete proofreading prompts
- Revision statistics and analysis
- Context sources used
- Session configuration details

### Integration Workflow

#### CAT Tool Re-integration:
1. **Import Revised File**: Load 3-column output into spreadsheet/CAT tool
2. **Review Changes**: Use comments column to understand revisions
3. **Selective Application**: Accept/reject changes based on professional judgment
4. **Update Translation Memory**: Add approved revisions to TM database

#### Quality Assurance:
1. **Change Tracking**: Comments explain every modification made
2. **Consistency Verification**: Cross-check with project terminology
3. **Client Review**: Use explanatory comments for client communication
4. **Learning Integration**: Feed back patterns into tracked changes

---

## Context Sources

Supervertaler's multicontextual approach leverages multiple information sources simultaneously to deliver superior translation accuracy.

### Translation Memory (TM)

#### Supported Formats

**TMX Files**: Standard translation memory exchange format
- Full compatibility with major CAT tools
- Preserves metadata and timestamps
- Language pair matching

**TXT Files**: Tab-separated format
```
Source Text[TAB]Translation
Hello world[TAB]Hallo wereld
```

#### Integration Benefits
- **Exact Matches**: Instant consistency for repeated content
- **Fuzzy Matches**: Guidance for similar segments
- **Terminology Consistency**: Standardized term translations
- **Quality Baseline**: Professional translation references

#### Best Practices
1. Use TM from same domain/client for consistency
2. Clean TM data before import (remove outdated entries)
3. Combine multiple relevant TM files
4. Regular TM maintenance and updates

### Custom Instructions

#### Purpose
Project-specific guidance that adapts AI behavior to your requirements.

#### Effective Instructions

**Domain Guidance**:
```
This is a technical manual for automotive engineers.
Use formal, professional language.
Preserve all part numbers and model codes exactly.
Convert imperial measurements to metric.
```

**Style Requirements**:
```
Target audience: General public
Use simple, accessible language
Avoid technical jargon
Maintain friendly, helpful tone
```

**Terminology Guidelines**:
```
Company name "TechCorp" should remain in English
"Software" translates to "Software" (not "Programmatuur")
Use "gebruiker" for "user" (not "afnemer")
```

#### Best Practices
1. Be specific and actionable
2. Include positive examples ("use X") and negative examples ("avoid Y")
3. Address known problem areas from previous work
4. Update instructions based on feedback and results

### Tracked Changes Integration

#### Input Sources

**DOCX Revision Tracking**: Import tracked changes from Word documents
- Captures human editing patterns
- Learns preferred terminology choices
- Understands style preferences

**TSV Editing Patterns**: Before/after comparison data
```
Original[TAB]Edited_Version
Old terminology[TAB]Preferred terminology
Awkward phrasing[TAB]Improved phrasing
```

#### Learning Mechanism

AI analyzes patterns in human edits to understand:
- Terminology preferences
- Style improvements
- Grammar corrections
- Cultural adaptations

#### Benefits
- **Personalized**: Adapts to your editing style
- **Consistent**: Applies learned patterns automatically
- **Improving**: Gets better with more data
- **Efficient**: Reduces post-editing time

### Document Images

#### Visual Context Integration

When source text references figures, charts, or diagrams, Supervertaler can automatically provide visual context to the AI.

#### Supported Formats
- PNG, JPG, JPEG, GIF
- High-resolution images preferred
- Multiple images per document supported

#### Automatic Detection

AI automatically detects figure references in text:
```
"As shown in Figure 1A..."
"See diagram below..."
"The flowchart illustrates..."
```

#### Benefits
- **Accuracy**: Visual context prevents misinterpretation
- **Completeness**: Ensures all visual elements are properly referenced
- **Technical Precision**: Critical for technical/scientific content
- **Cultural Adaptation**: Visual elements may need localization

---

## Translation Memory

Translation Memory (TM) integration provides consistency and efficiency by leveraging previously translated content and professional translation databases.

### Supported Formats

#### TMX (Translation Memory eXchange)

**Industry Standard**: Compatible with all major CAT tools

```xml
<?xml version="1.0" encoding="UTF-8"?>
<tmx version="1.4">
  <header>
    <prop type="x-filename">project.tmx</prop>
  </header>
  <body>
    <tu tuid="1">
      <tuv xml:lang="en">
        <seg>Hello world</seg>
      </tuv>
      <tuv xml:lang="nl">
        <seg>Hallo wereld</seg>
      </tuv>
    </tu>
  </body>
</tmx>
```

**Features**:
- Metadata preservation
- Multiple language pairs
- Timestamps and attributes
- Quality scoring

#### Tab-Separated TXT

**Simple Format**: Easy creation and editing

```
Source Text[TAB]Target Translation
Hello world[TAB]Hallo wereld
Good morning[TAB]Goedemorgen
```

**Use Cases**:
- Quick terminology lists
- Client-specific glossaries
- Manual TM creation
- Legacy data import

### TM Integration Process

#### Loading Translation Memory

1. **File Selection**: Browse and select TMX or TXT files
2. **Language Verification**: Confirm source/target language matching
3. **Import Process**: TM data loaded into memory for matching
4. **Status Confirmation**: Log shows successful import with entry count

#### Matching Algorithm

**Exact Matches**: 100% identical segments
- Instant application for consistency
- Highest confidence level
- Automatic terminology alignment

**Fuzzy Matches**: Similar but not identical segments
- Provides guidance for translation decisions
- Similarity scoring and ranking
- Context-aware matching

**Terminology Extraction**: Key term identification
- Domain-specific vocabulary recognition
- Consistent term translation
- Glossary integration

### Integration with CAT Tools

Generated TMX files integrate directly with:

**memoQ**:
- Import as translation memory
- Apply in real-time during translation
- Leverage for quality assurance

**Trados Studio**:
- Add to project TM
- Use for fuzzy matching
- Integration with terminology database

**CafeTran Espresso**:
- Load as project memory
- Auto-substitution features
- Terminology management

**OmegaT**:
- Import as project TM
- Real-time matching
- Open-source compatibility

---

## AI Provider Settings

Supervertaler supports multiple AI providers, each with different models and capabilities optimised for various translation scenarios.

### OpenAI Integration

#### Available Models

**GPT-5** 🔥 *Latest Reasoning Model*
- **Advanced Capabilities**: Logical analysis and reasoning
- **Token Limit**: Up to 50,000 tokens for large documents
- **Strengths**: Complex content, technical documentation, nuanced translation
- **Special Features**: Automatic reasoning effort optimization
- **Best For**: Patent documents, legal texts, complex technical content
- **v2.4.1+**: Full automatic parameter handling

**GPT-4o**
- **Multimodal**: Text and image processing
- **Token Limit**: 128,000 tokens
- **Strengths**: Visual context integration, balanced performance
- **Best For**: Documents with figures, charts, diagrams

**GPT-4**
- **Reliable**: Consistent baseline performance
- **Token Limit**: 32,000 tokens
- **Strengths**: General-purpose translation, stable output
- **Best For**: Standard translation work, consistent results

**GPT-4-turbo**
- **Enhanced**: Improved context handling
- **Token Limit**: 128,000 tokens
- **Strengths**: Large document processing, cost efficiency
- **Best For**: Long documents, batch processing

#### GPT-5 Special Considerations (v2.4.1+)

**Automatic Parameter Handling**:
- Uses `max_completion_tokens` instead of `max_tokens`
- Temperature parameter automatically handled
- Reasoning effort set to "low" for optimal output

**Token Management**:
- Dynamic allocation based on content size
- Accounts for reasoning token overhead
- Minimum 32,000 tokens, up to 50,000 for large jobs

**Output Processing**:
- Automatic cleanup of formatting quirks
- Removes double numbering artifacts
- Ensures clean, professional output

### Claude Integration

#### Available Models

**Claude-3.5-Sonnet**
- **Creative Excellence**: Superior cultural adaptation
- **Context**: 200,000 tokens
- **Strengths**: Literary translation, marketing content, cultural nuance
- **Best For**: Creative content, transcreation, cultural adaptation

**Claude-3-Haiku**
- **Speed**: Fast processing for simpler content
- **Context**: 200,000 tokens
- **Strengths**: Efficiency, cost-effective, quick turnaround
- **Best For**: Simple translations, batch processing, time-sensitive work

#### Claude Advantages
- **Cultural Sensitivity**: Excellent cross-cultural adaptation
- **Creative Content**: Superior for marketing and creative materials
- **Safety**: Built-in content filtering and ethical guidelines
- **Context Handling**: Excellent long-document processing

### Gemini Integration

#### Available Models

**Gemini-2.5-Pro**
- **Technical Excellence**: Strong analytical capabilities
- **Context**: 1,000,000+ tokens
- **Strengths**: Technical documentation, analytical content
- **Best For**: Technical manuals, scientific papers, data analysis

**Gemini-1.5-Flash**
- **Speed**: Rapid processing capabilities
- **Context**: 1,000,000+ tokens
- **Strengths**: Efficiency, cost-effective, high throughput
- **Best For**: Large volume processing, simple content

#### Gemini Advantages
- **Massive Context**: Exceptional long-document handling
- **Technical Accuracy**: Strong performance on technical content
- **Cost Efficiency**: Competitive pricing for large volumes
- **Speed**: Fast processing for time-sensitive projects

### Model Selection Guidelines

#### Content-Based Selection

**Complex Technical Content**:
- **First Choice**: GPT-5 (reasoning capabilities)
- **Alternative**: Gemini-2.5-Pro (technical accuracy)

**Creative/Marketing Content**:
- **First Choice**: Claude-3.5-Sonnet (cultural adaptation)
- **Alternative**: GPT-4o (balanced creativity)

**Legal/Patent Documents**:
- **First Choice**: GPT-5 (precision and reasoning)
- **Alternative**: Claude-3.5-Sonnet (formal register)

**Large Volume/Batch Work**:
- **First Choice**: Gemini-1.5-Flash (efficiency)
- **Alternative**: Claude-3-Haiku (speed)

**Visual Content (Figures/Charts)**:
- **First Choice**: GPT-4o (multimodal)
- **Alternative**: Gemini-2.5-Pro (analytical)

### Model Management Controls

#### 🔄 Refresh Models Button

**Primary Function**: Updates the model dropdown menu with current available models

**What It Does**:
- ✅ Updates model dropdown for selected provider
- ✅ Sets appropriate default model
- ✅ Quick operation with minimal logging
- ✅ Essential for UI maintenance

**When to Use**:
- Model dropdown appears empty or outdated
- After switching between AI providers
- When you want latest Gemini models
- UI appears unresponsive
- After updating API keys

#### 📋 List Models Button

**Primary Function**: Displays comprehensive model information in the log panel

**What It Does**:
- ✅ Shows detailed model information
- ✅ Provides model descriptions and capabilities
- ✅ Functions as diagnostic tool
- ✅ Verbose logging with details

**When to Use**:
- Research available models and capabilities
- Determine multimodal support
- Troubleshoot API connectivity
- Copy exact model names
- Evaluate models for specific use cases

---

## Troubleshooting

### Common Issues and Solutions

#### API and Connection Issues

**"API Key not found" or "Invalid API Key"**
- **Check**: `api_keys.txt` file exists and has correct format
- **Verify**: API key is valid and active
- **Test**: Use "List Models" button to verify connection
- **Solution**: Copy working API key from provider dashboard

**"Model not available" or "Model access denied"**
- **GPT-5 Access**: Ensure you have access through OpenAI
- **Claude Access**: Verify Anthropic API access level
- **Gemini Access**: Check Google AI Studio permissions
- **Solution**: Contact provider for model access or use alternative

**Connection timeout or network errors**
- **Network**: Verify internet connection stability
- **Firewall**: Check corporate firewall settings
- **VPN**: Try with/without VPN connection
- **Solution**: Use "Refresh Models" to test connection

#### File and Path Issues

**"File not found" or "Path does not exist"**
- **Absolute Paths**: Ensure file paths are complete and absolute
- **File Existence**: Verify all input files exist at specified locations
- **Permissions**: Check read permissions on input files
- **Solution**: Use "Browse" buttons to select files correctly

**"Unicode decode error" or "Encoding issues"**
- **File Encoding**: Save text files as UTF-8
- **Special Characters**: Ensure proper character encoding
- **BOM**: Remove Byte Order Mark if present
- **Solution**: Re-save files as UTF-8 without BOM

**Cross-platform path issues (Windows/Mac/Linux)**
- **Path Separators**: Use forward slashes (/) for compatibility
- **Drive Letters**: Windows drive letters may not work on other systems
- **Solution**: Use relative paths or Project Library for portability

#### Translation and Processing Issues

**GPT-5 returns empty translations**
- **Token Limit**: Automatic allocation should handle this (v2.4.1+)
- **Content Length**: Try reducing chunk size for very long segments
- **API Limits**: Check OpenAI usage limits and quotas
- **Solution**: Use smaller chunks or alternative model

**Double numbering in output (e.g., "1. 1. Text")**
- **GPT-5 Issue**: Fixed in v2.4.1 with automatic cleanup
- **Other Models**: Check system prompt configuration
- **Solution**: Update to v2.4.1 or manually clean output

**Inconsistent terminology across chunks**
- **Context**: Ensure Translation Memory is loaded
- **Instructions**: Add terminology guidelines to Custom Instructions
- **Chunk Size**: Reduce chunk size for better consistency
- **Solution**: Use tracked changes to learn terminology preferences

**AI refuses to translate certain content**
- **Content Policy**: Check for content that may violate AI policies
- **Language Support**: Verify source/target language combination
- **Model Limitations**: Try different AI provider/model
- **Solution**: Modify content or use alternative provider

#### Memory and Performance Issues

**"Out of memory" or application crashes**
- **Large Files**: Process in smaller chunks
- **System RAM**: Close other applications to free memory
- **Python Memory**: Restart application periodically for large jobs
- **Solution**: Increase chunk size or process files separately

**Slow processing speeds**
- **Network**: Check internet connection speed
- **API Limits**: Some providers have rate limits
- **Chunk Size**: Optimise chunk size for provider
- **Solution**: Adjust chunk size or use faster model variant

**GUI freezing or unresponsive**
- **Background Processing**: Translation runs in background thread
- **Large Jobs**: Very large files may take time
- **System Resources**: Check CPU and memory usage
- **Solution**: Wait for completion or restart if necessary

### Getting Help

**Information to Provide**:
1. Supervertaler version number (v2.4.1 or v2.5.0)
2. Operating system (Windows/Mac/Linux)
3. Python version
4. AI provider and model used
5. Error message from log
6. Session report (if generated)
7. Input file sample (if not confidential)

**Common Resolution Steps**:
1. Update to latest Supervertaler version
2. Verify API key validity
3. Test with different AI provider/model
4. Check file encoding and format
5. Try smaller chunk size
6. Review session report for details

---

## Advanced Tips

### Bulk Operations Guide (v3.3.0-beta)

**New in v3.3.0-beta**: Comprehensive bulk editing tools for managing large projects efficiently.

#### Accessing Bulk Operations

All bulk operations are in: **Edit → Bulk Operations**

#### Select All Segments (Ctrl+A)

- Selects all visible segments (respects current filter)
- Shows count and available operations
- Foundation for multi-selection features

**Use Cases**:
- Quick overview of project size
- Identify segments affected by bulk operations
- Combined with filters for targeted selection

#### Clear All Targets

**Purpose**: Remove all target translations at once

**Workflow**:
```
Edit → Bulk Operations → Clear All Targets...
[Confirmation dialog shows count]
Click "Yes" → All targets cleared
```

**When to Use**:
- Starting fresh translation after major source changes
- Clearing MT output before AI translation
- Resetting project for re-translation
- Testing workflows without losing source text

**⚠️ Warning**: This action cannot be undone! Save project first.

#### Change Status (All/Filtered)

**Two Options**:
1. **Change Status (All)** - Affects entire project
2. **Change Status (Filtered)** - Affects only visible segments

**Available Statuses**:
- Untranslated
- Translated
- Approved
- Draft

**Workflow Example** - Mark filtered segments as approved:
```
1. Set filter: Status = "Translated"
2. Edit → Bulk Operations → Change Status (Filtered)...
3. Select "Approved"
4. Click "Apply"
→ Only translated segments change to approved
```

**Use Cases**:
- Mark batch of AI translations as "Draft" for review
- Approve all segments after QA review
- Reset status after major revisions
- Mark filtered segments (e.g., all table cells) with specific status

#### Lock/Unlock Segments

**What is Locking?**
- **Locked segments** are marked as "final" and protected from accidental edits
- Lock status saved in project file
- Useful for reviewed/approved content

**Four Options**:
1. **Lock All Segments** - Lock entire project
2. **Unlock All Segments** - Unlock entire project
3. **Lock Filtered Segments** - Lock only visible segments
4. **Unlock Filtered Segments** - Unlock only visible segments

**Workflow Example** - Lock approved segments:
```
1. Set filter: Status = "Approved"
2. Edit → Bulk Operations → Lock Filtered Segments
→ Only approved segments are locked
```

**Lock Current Segment**:
- **Edit → Segment → Lock Current Segment**
- Quick way to lock single segment
- Useful during review workflow

**Use Cases**:
- Lock approved segments to prevent accidental changes
- Lock client-reviewed content
- Lock glossary entries or boilerplate text
- Unlock batch for revision after client feedback

**🔒 Pro Tip**: Combine filters with lock operations:
```
Filter: Source contains "Copyright"
→ Lock Filtered Segments
→ All copyright notices locked
```

#### Combining Filters with Bulk Operations

**Powerful Workflow**: Filter → Bulk Operation

**Example 1** - Clear targets in table cells:
```
1. Set filter: Source contains "Table"
2. Edit → Bulk Operations → Clear All Targets
→ Only table segments cleared
```

**Example 2** - Mark all headings as translated:
```
1. Set filter: Status = "Draft"
2. Set filter: Target contains text
3. Edit → Bulk Operations → Change Status (Filtered)
4. Select "Translated"
→ All drafted segments marked as translated
```

**Example 3** - Lock client-reviewed segments:
```
1. Set filter: Status = "Approved"
2. Edit → Bulk Operations → Lock Filtered Segments
→ Client-approved content protected
```

#### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Select All Segments | `Ctrl+A` |
| Find/Replace | `Ctrl+F` |
| Apply Filters | `Ctrl+Shift+A` |
| Toggle Filter Mode | `Ctrl+M` |

---

### Workflow Optimization

#### Project Setup Strategies

**Client-Specific Configurations**:
Create dedicated project configurations for each client with:
- Language pair and preferred models
- Client-specific Translation Memory
- Custom instructions with style guidelines
- Tracked changes from previous work
- Domain-specific prompts

**Content-Type Templates**:
- **Legal Documents**: Formal prompts, legal TM, conservative models
- **Marketing Materials**: Creative prompts, cultural adaptation focus
- **Technical Manuals**: Safety-focused prompts, technical terminology
- **Medical Content**: Regulatory compliance, medical terminology

#### Batch Processing Strategies

**Sequential Processing**:
For related documents:
1. Load comprehensive TM with all previous translations
2. Process documents in logical order
3. Add each output TMX to master TM database
4. Use accumulated knowledge for subsequent documents

**Parallel Processing**:
For independent documents:
- Process simultaneously using different AI providers
- Compare results for quality assurance
- Identify best-performing provider for content type

### Quality Assurance Techniques

#### Multi-Provider Validation

**Critical Content Double-Check**:
1. Primary translation: GPT-5 (reasoning capability)
2. Secondary validation: Claude-3.5-Sonnet (creative accuracy)
3. Compare outputs for consistency
4. Highlight discrepancies for human review

#### Context Optimization

**Layered Context Strategy**:
1. **Base Layer**: Domain-specific Translation Memory
2. **Enhancement Layer**: Project-specific Custom Instructions
3. **Learning Layer**: Tracked Changes from Previous Work
4. **Visual Layer**: Document Images and Figures
5. **Prompt Layer**: Domain-Specific System Prompts

### Professional Integration

#### CAT Tool Ecosystem

**memoQ Integration Workflow**:
1. **Pre-translation**: Export segments for Supervertaler processing
2. **AI Translation**: Process with optimal context and prompts
3. **TMX Integration**: Import generated TMX into project
4. **Quality Layer**: Use exact matches, review fuzzy matches
5. **Post-editing**: Refine with memoQ's built-in tools

**Trados Studio Integration**:
1. **Project Setup**: Configure with Supervertaler TMX
2. **Batch Processing**: Process multiple files with consistent settings
3. **Terminology Integration**: Combine with existing termbases
4. **Quality Assurance**: Leverage Trados QA with AI translations

---

*This comprehensive user guide covers all aspects of Supervertaler v2.4.1 and v2.5.0. For additional support or advanced enterprise features, please contact the development team or visit the GitHub repository.*

**Repository**: https://github.com/michaelbeijer/Supervertaler  
**Documentation**: See `docs/` folder for technical guides  
**Support**: GitHub Issues for bug reports and feature requests
