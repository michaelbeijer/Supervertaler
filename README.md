# Supervertaler

🎯 **Context-aware, LLM-powered translation & proofreading tool, leveraging multiple context sources for enhanced accuracy (built for translators)** - Revolutionary approach to document translation that leverages multiple context sources for unparalleled accuracy.

**Note**: A version of Supervertaler is being developed with many features commonly found in proper CAT tools (Computer-Aided Translation tools), which has reached **v3.4.0-beta** with professional UI enhancements! It features memoQ-style status icons (color-coded ✗/~/✓/✓✓/🔒), multi-selection system (Ctrl/Shift/Ctrl+A), responsive compact layout, column optimization (115px reclaimed), custom tab overflow, and comprehensive grid editor improvements. The v3.3.0-beta release added a cleaner toolbar (55% space reduction), reorganized menus, semantic color coding, unified prompt management, grid pagination (10x faster loading), smart paragraph detection, dual text selection, three professional view modes (Grid, List, Document), and comprehensive auto-export options. We're implementing features from [michaelbeijer.co.uk/what_i_look_for_in_a_cat_tool](https://michaelbeijer.co.uk/what_i_look_for_in_a_cat_tool).


## 📦 Available Versions

### v3.4.0-beta (Experimental - CAT Editor) 🎨
**File**: `Supervertaler_v3.4.0-beta_CAT.py`
- 🎨 **NEW**: memoQ-style status icons (✗/~/✓/✓✓/🔒) with color coding (red/orange/green/blue)
- ✅ **NEW**: Multi-selection system (Ctrl+Click, Shift+Click, Ctrl+A)
- 📊 **NEW**: Selection counter in status bar with visual feedback
- 🎯 **NEW**: Responsive compact layout (55% vertical space reduction in editor)
- 📏 **NEW**: Column optimization (115px total reclaimed: ID/Type/Style/Status optimized)
- 🔧 **NEW**: Column resize handles (drag borders, min 25px)
- 📑 **NEW**: Custom tab overflow with dropdown menu (full names, no truncation)
- 🔄 **NEW**: Refresh Tabs button (purple, fixes tab display issues)
- 🎨 **v3.3.0**: Professional Start Screen (project management interface when no document loaded)
  * Projects tab with recent projects list and quick actions
  * File Explorer tab with tree view for browsing/opening files
  * Settings tab with quick access to all configuration options
  * Automatic transition to Grid View when document is loaded
- 🎨 **v3.3.0**: Major UI/UX redesign - 55% cleaner toolbar with dropdown menus
- 🗂️ **v3.3.0**: Reorganized menu bar (File/Edit/View/Project/Resources/Help)
- 🎨 **v3.3.0**: Semantic color coding (green=import, orange=export, blue=save, gray=views)
- 📝 **v3.3.0**: "Assistant panel" terminology (was "Translation Workspace")
- ❓ **v3.3.0**: Help menu (User Guide, Changelog, About)
- 🔧 **v3.3.0**: Tracked Changes reports now include clickable GitHub links
- ✅ **v3.3.0**: Batch size dialog height (OK button fully visible)
- 🎯 Unified Prompt Library with System Prompts + Custom Instructions (Ctrl+P)
- ⚡ Grid pagination system (50 segments/page, 10x faster loading!)
- 🧠 Smart paragraph detection for document view
- ✅ Professional CAT editor with Grid, List, and Document views
- ✅ Auto-export options (session reports MD/HTML, TMX, TSV, XLIFF, Excel)
- ✅ CafeTran and memoQ bilingual DOCX support
- 📖 **Status**: UI-optimized, feature-complete, beta testing phase
- 💡 **Note**: v3.x signifies major architectural change from original DOCX workflow

### v2.5.0-CLASSIC (Production-ready) 🎉
**File**: `Supervertaler_v2.5.0-CLASSIC.py`
- 🔧 **NEW**: Parallel folder structure (`user data/` vs `user data_private/`) for dev mode
- 🔒 **NEW**: Private features auto-routing (`.supervertaler.local` feature flag)
- ✅ Unified folder structure with v3.x (all user data in `user data/`)
- ✅ Projects now saved to `user data/Projects/`
- ✅ CafeTran bilingual DOCX support - AI-based pipe formatting!
- ✅ memoQ bilingual DOCX support - Programmatic formatting preservation!
- ✅ Two complementary formatting approaches (AI-based & programmatic)
- ✅ 100% success rate in production testing (both formats)
- ✅ Fully tested and stable for professional use
- 📖 **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- 📖 **CafeTran Guide**: [`.dev/docs/features/CAFETRAN_SUPPORT.md`](.dev/docs/features/CAFETRAN_SUPPORT.md)
- 📖 **memoQ Guide**: [`.dev/docs/features/MEMOQ_SUPPORT.md`](.dev/docs/features/MEMOQ_SUPPORT.md)
- 🏷️ **Version Note**: "-CLASSIC" suffix denotes original DOCX workflow architecture

> **💡 Recommendation**: Use **v2.5.0-CLASSIC** for production translation work. Try **v3.4.0-beta** if you want to test the experimental CAT editor features with professional UI enhancements!
> 
> **🔢 Version Scheme**: The jump from v2.x to v3.x reflects a **major architectural change**. v2.5.0-CLASSIC uses the original DOCX-based workflow, while v3.2.0-beta is a complete rewrite as a segment-based CAT editor. The "-CLASSIC" and "-beta" suffixes help distinguish these fundamentally different architectures.

----

## 🔧 CAT Tool Integration

**Supervertaler is designed for professional translators using CAT tools** (memoQ, CafeTran, Trados Studio, Wordfast, etc.). It integrates seamlessly into existing translation workflows with **three workflow options**:

### 🆕 CafeTran Bilingual DOCX Workflow (v2.4.3 - ☕ AI-BASED) 🎉

**Intelligent AI-powered formatting marker preservation!**

> **📌 Why CafeTran?**: CafeTran uses simple pipe symbols `|text|` to mark formatted text. Supervertaler's AI understands these markers contextually and places them intelligently in translations, even when word order changes completely.

1. **Export bilingual DOCX** from CafeTran
2. **Click "☕ Import CafeTran DOCX"** in Supervertaler (green button)
3. **Configure translation settings** (language pair, AI provider, model)
4. **Click "Translate"** - AI processes segments and intelligently places pipes
5. **Click "☕ Export to CafeTran DOCX"** - Pipes displayed as BOLD + RED
6. **Reimport to CafeTran** - Formatting markers perfectly preserved!

**Benefits**:
- ✅ **AI-based intelligence** - Pipes placed contextually, not mechanically
- ✅ **Handles word reordering** - Works perfectly even with different sentence structures
- ✅ **Visual clarity** - All pipe symbols displayed as BOLD + RED in exported DOCX
- ✅ **Simple format** - `|formatted text|` is easy to understand
- ✅ **Complete round-trip** - Verified CafeTran reimport workflow
- ✅ **Native integration** - Direct CafeTran bilingual format support

**Example**:
- Source: `"He debuted against |Juventus FC| in 2001"`
- Translation: `"Hij debuteerde tegen |Juventus FC| in 2001"`
- AI correctly preserves the pipe position around the team name

📖 **Full Documentation**: See [`.dev/docs/features/CAFETRAN_SUPPORT.md`](.dev/docs/features/CAFETRAN_SUPPORT.md) for detailed guide

---

### 🆕 memoQ Bilingual DOCX Workflow (v2.4.3 - 📊 PROGRAMMATIC) 🎉

**Professional CAT tool integration with algorithmic formatting preservation!**

> **📌 Why memoQ?**: memoQ bilingual DOCX files include complex formatting at the character-run level. Supervertaler extracts this formatting and applies it programmatically to translations using smart threshold logic.

1. **Export bilingual DOCX** from memoQ
2. **Click "� Import memoQ DOCX"** in Supervertaler (green button)
3. **Configure translation settings** (language pair, AI provider, model)
4. **Click "Translate"** - AI translates segments
5. **Click "💾 Export to memoQ DOCX"** - Formatting applied programmatically
6. **Reimport to memoQ** - Formatting and tags preserved!

**Benefits**:
- ✅ **Programmatic precision** - Formatting applied algorithmically (>60% = whole segment)
- ✅ **Professional format** - Industry-standard memoQ bilingual DOCX
- ✅ **Complex formatting supported** - Bold, italic, underline at character level
- ✅ **CAT tag preservation** - `[1}...{2]` format maintained
- ✅ **Segment IDs maintained** - Perfect reimport compatibility
- ✅ **Status updates** - Automatically marked as "Confirmed"

**Smart Formatting Logic**:
- If source is >60% formatted → entire target gets formatting
- If source has partial formatting → first 1-2 words formatted
- Character-level precision when needed

📖 **Full Documentation**: See [`.dev/docs/features/MEMOQ_SUPPORT.md`](.dev/docs/features/MEMOQ_SUPPORT.md) for detailed guide

---

### Traditional Text Workflow (All versions)

**Manual extraction for maximum flexibility**:

1. **Export from CAT tool**: Export bilingual table from your CAT tool (usually .docx or .rtf format)
2. **Extract source text**: Copy all rows from the source language column
3. **Create .txt input**: Paste into plain text file, one segment per line
4. **Process with Supervertaler**: Use Translation mode for AI-powered translation

**Output Integration**:
Supervertaler provides two output formats for flexible CAT tool integration:

**📄 Tab-delimited .txt file**: 
- Source{TAB}Target format for easy reimport
- Copy target column back into your bilingual table
- Reimport into CAT tool to populate translations

**📚 TMX translation memory**:
- Add directly to your CAT tool project
- Instant exact matches as you translate
- Builds your translation memory assets

*Why this approach?* Leveraging CAT tools' existing segmentation capabilities is more efficient and maintainable than recreating complex file format support in Supervertaler.

## 🚀 What Makes Supervertaler Special

**Multicontextual Intelligence**: Unlike traditional sentence-by-sentence translators, Supervertaler considers multiple layers of context simultaneously:

### **Multiple context sources for enhanced translation/proofreading accuracy:**

- **Full document context** - Every sentence translated with awareness of the entire document
- **Tracked changes ingestion** - Learn from DOCX revisions (from memoQ/Trados-generated bilingual review files) and TSV editing patterns  
- **Translation memory matching** - Leverage exact matches from TMX/TXT for consistency
- **Multimodal figure context** - AI sees referenced images when translating figure captions
- **Custom instructions** - Domain-specific guidance tailored to your content
- **Advanced prompt management** - Specialized system prompt library for different document types

### **Professional workflow features:**

- **Project Library** ⚡ - Save/restore complete workspace configurations for different clients/projects
- **Domain-Specific Prompts** ⚡ - 8 professionally crafted prompt collections (medical, legal, technical, financial, etc.)
- **Custom Prompt Library** - Save/load specialized prompt sets for different use cases
- **Prompt Library** - Edit and customize active AI instructions in real-time
- **Advanced 3-panel GUI** - Resizable interface with professional font rendering
- **Switch Languages Button** - One-click swap between source and target languages
- **Cross-platform Support** - Clickable folder paths work on Windows, macOS, and Linux
- **Chunked processing** - Handle large documents with intelligent batching
- **Multiple LLM support** - Claude, Gemini, and OpenAI integration
- **Automatic TMX export** - Build translation memories from your work

---

![supervertaler_screenshot_v2 3 0](https://github.com/user-attachments/assets/22481fd0-fe7e-42c4-b037-b39ddb1eec7b)


## 📖 Documentation

### Quick Start
- **📋 Complete User Guide**: [USER_GUIDE.md](USER_GUIDE.md) - Comprehensive guide for all versions
- **⚡ Installation Guide**: [INSTALLATION.md](INSTALLATION.md) - Get started quickly

### Advanced Documentation (for developers/contributors)
- **System Prompts Guide**: [`.dev/docs/user_guides/SYSTEM_PROMPTS_GUIDE.md`](.dev/docs/user_guides/SYSTEM_PROMPTS_GUIDE.md)
- **Translation Memory Guide**: [`.dev/docs/user_guides/TM_USER_GUIDE.md`](.dev/docs/user_guides/TM_USER_GUIDE.md)
- **Translation Workspace**: [`.dev/docs/user_guides/TRANSLATION_WORKSPACE_REDESIGN.md`](.dev/docs/user_guides/TRANSLATION_WORKSPACE_REDESIGN.md)
- **Implementation Docs**: See `.dev/docs/implementation/` for technical details
- **Development History**: See `.dev/docs/` for session summaries, planning docs, and implementation notes

## 1. Features Overview

> **📌 Note**: The features below apply to **v2.4.0 (stable)**. For v2.5.1 experimental features, see the [v2.5.1 Features](#v251-experimental-features) section below.

### v2.4.0 Feature Matrix

| Capability | Translate Mode | Proofread Mode |
|------------|----------------|----------------|
| Source ingestion (.txt) | 1 column (source) | source{TAB}target{TAB}comment |
| TM (exact match) | Applied pre‑LLM | Not applied |
| Tracked changes context | Yes (relevant subset) | Yes (relevant subset) |
| Images (fig refs) | Injected before referenced lines | Same |
| Output TXT | source{TAB}translated | source{TAB}revised_target{TAB}comment |
| Output TMX | Yes | No |
| Custom instructions | Appended to prompt | Appended to prompt |
| Comments merging | N/A | Original + AI summary (conditional) |

### v2.5.1 Experimental Features

**🚧 Under Development** - The following features are available in v2.5.1 but may change:

- **✅ Translation Memory with Fuzzy Matching**: 75% threshold with difflib.SequenceMatcher
- **✅ Enhanced Translation Workspace**: 10 organized tabs (Projects, System Prompts, Custom Instructions, MT, LLM, TM, Glossary, Images, Non-trans, Settings)
- **✅ System Prompts Architecture**: Separate global AI behavior from project-specific instructions
- **✅ Custom Instructions**: Project-level guidance that extends system prompts
- **✅ Global Prompt Preview**: Test combined prompts with current segment
- **✅ TM Manager**: Import/export TMX, delete individual entries
- **✅ Auto-Export Options**: Session reports (MD/HTML), TMX, TSV, XLIFF, Excel bilingual
- **🚧 Context-Aware Translation**: In development
🚧 Under Development:

- ✅ Translation Memory with Fuzzy Matching
- ✅ Enhanced Translation Workspace (10 tabs)
- ✅ System Prompts Architecture
- ✅ Custom Instructions
- ✅ Global Prompt Preview
- ✅ TM Manager
- ✅ Auto-Export Options (7 formats)
- ✅ **Full Document Context** (v2.4.0 proven approach - **JUST COMPLETED!**)
- 🚧 Batch Translation with Progress (basic implementation complete, refinement in progress)
- 🚧 TrackedChangesAgent (port from v2.4.0)
- 🚧 Prompt Library Integration

**⚠️ Important**: v3.1.0-beta is experimental. Features may be incomplete, changed, or removed. Use v2.4.3-CLASSIC for production work.

---

## 2. 🧠 Multicontextual Intelligence Explained

### Why Context Matters
Traditional translation tools translate each sentence in isolation, missing crucial contextual cues that affect meaning, consistency, and quality. Supervertaler's **multicontextual approach** considers multiple information sources simultaneously:

#### 📖 Full Document Context
- **Complete awareness**: Every sentence is translated with knowledge of the entire document
- **Consistency**: Technical terms, proper nouns, and style remain consistent throughout
- **Coherence**: Maintains logical flow and references between sections
- **Disambiguation**: Resolves ambiguous terms using surrounding content

#### 🔄 Tracked Changes Context  
- **Learning from edits**: Analyzes track changes from memoQ/Trados-generated bilingual review files (DOCX) and TSV edit patterns
- **Style adaptation**: Understands preferred editing patterns and terminology choices
- **Quality improvement**: Learns from human corrections to avoid similar issues

#### 🎯 Translation Memory Integration
- **Exact matching**: Pre-populates identical segments from previous translations
- **Terminology consistency**: Ensures consistent translation of recurring phrases
- **Efficiency**: Reduces costs and time by reusing validated translations

#### 🖼️ Multimodal Figure Context
- **Visual understanding**: AI sees referenced images when translating figure captions
- **Accurate descriptions**: Better translation of visual elements and diagrams  
- **Technical precision**: Improved handling of charts, graphs, and technical illustrations

#### ⚙️ Advanced Custom Context
- **Domain expertise**: Custom instructions for specialized fields (legal, medical, technical)
- **Brand consistency**: Maintain corporate terminology and style guidelines
- **Flexible prompts**: Adapt translation approach based on document type and requirements

### The Supervertaler Advantage
This multicontextual approach delivers translation quality that approaches human-level understanding while maintaining the efficiency and consistency of AI processing.

---

## 3. Installation

1. **Python**: 3.10+ recommended.
2. Create / activate virtual environment (optional):
   ```
   python -m venv venv
   source venv/Scripts/activate  (Windows: venv\Scripts\activate)
   ```
3. Install dependencies (install only what you need):
   ```
   pip install google-generativeai anthropic openai pillow
   ```
4. Run:
   ```
   python Supervertaler_v2.3.0.py
   ```

### First Launch (Key Configuration)
On first run, Supervertaler creates an `api_keys.txt` template. Edit it:

```
#google = YOUR_GOOGLE_API_KEY_HERE
#claude = YOUR_CLAUDE_API_KEY_HERE  
#openai = YOUR_OPENAI_API_KEY_HERE
```

Uncomment and fill keys for desired providers. At least **one** valid key is required.

---

## 4. Quick API Key Setup

### Google Gemini (Recommended)
1. https://aistudio.google.com/
2. Create API key
3. Add to `api_keys.txt`: `google = YOUR_KEY_HERE`

### Anthropic Claude
1. https://console.anthropic.com/
2. Get API key + add billing credits
3. Add to `api_keys.txt`: `claude = YOUR_KEY_HERE`

### OpenAI
1. https://platform.openai.com/
2. Get API key + add billing  
3. Add to `api_keys.txt`: `openai = YOUR_KEY_HERE`

---

## 5. Basic Usage

### Translation Mode (most common)
1. **Prepare .txt input**: One source segment per line
2. **Select input/output files**
3. **Set languages** (source → target)  
4. **Choose AI provider/model**
5. **Add context sources** (optional): TM, tracked changes, images
6. **Hit "Start Process"**

### Proofreading Mode
1. **Prepare .txt input**: `source{TAB}target{TAB}optional_comment` per line
2. Same setup as Translation
3. Output: revised targets + merged comments

**⚠️ Provider Note**: For proofreading, Gemini works most reliably. OpenAI/Claude proofreading may have formatting quirks but remain functional. Translation works excellently with all providers.

---

## 6. Context Sources (Power Features)

### Translation Memory (TM)
- **TMX files**: Standard format from CAT tools
- **TXT files**: `source{TAB}target` format
- **Exact matches**: Applied before LLM (saves costs)
- **Fuzzy matches**: Provided as context to LLM

### Tracked Changes
- **DOCX files**: With track changes enabled
- **TSV files**: `original{TAB}revised` format  
- **Learning**: AI learns from human editing patterns

### Document Images  
- **Auto-detection**: Finds "Figure X" references in text
- **Multimodal**: AI sees the actual images when translating
- **File formats**: PNG, JPG, WebP, GIF
- **Naming**: `figure1a.png` matches "Figure 1A" in text

### Custom Instructions
- **Domain guidance**: "Use medical terminology..."
- **Style preferences**: "Maintain formal register..."
- **Client requirements**: Custom formatting/terminology

---

## 7. AI Provider Models

### Gemini (Google)
- **gemini-1.5-pro**: Best for complex documents
- **gemini-1.5-flash**: Fast, still high-quality  
- **Strong**: Technical content, structured output

### Claude (Anthropic)  
- **claude-3.5-sonnet**: Excellent creative/nuanced content
- **claude-3-haiku**: Fast for simpler tasks
- **Strong**: Creative writing, cultural adaptation

### OpenAI
- **gpt-5**: Latest reasoning model with advanced capabilities  
- **gpt-4o**: Excellent multimodal performance
- **gpt-4**: Reliable general-purpose
- **gpt-4-turbo**: Better context window
- **Strong**: Balanced performance across domains

---

## 8. Output Files

### Translation Mode
1. **TXT**: `source{TAB}translated` (tab-separated)
2. **TMX**: Translation memory format (import into CAT tools)

### Proofreading Mode  
1. **TXT**: `source{TAB}revised_target{TAB}comments` 

---

## 9. Advanced Features (v2.3.0)

### Project Library
- **Save complete workspace**: Languages, files, prompts, everything
- **Instant project switching**: Client A → Client B workflows
- **Cross-platform**: Clickable folder access on Windows/macOS/Linux

### Custom Prompt Library
- **Domain-specific prompts**: 8 professional collections included
- **Save custom prompts**: Create your own specialized sets
- **Quick switching**: Active prompts marked with ⚡

### System Prompt Editor
- **Full control**: Edit underlying AI instructions
- **Template variables**: `{source_lang}`, `{target_lang}` auto-replace
- **Preview**: See final prompt before processing

---

## 10. Professional Workflow Integration

### For CAT Tool Users
1. **Export bilingual**: From memoQ/Trados/CafeTran
2. **Extract source column**: Paste into .txt (one line per segment)
3. **Process with Supervertaler**: Get AI translations
4. **Import back**: Either tab-separated TXT or TMX memory

### For Translation Agencies
- **Project Library**: Client-specific configurations
- **Domain Prompts**: Medical, legal, technical specializations
- **Team Sharing**: Export/import prompt and project configurations
- **Quality Control**: Consistent settings across translators

### For Freelancers
- **Efficiency**: Faster than manual translation
- **Quality**: Better than basic AI tools via context
- **Memory Building**: TMX exports grow your translation assets
- **Specialization**: Domain-specific prompts for your expertise

---

## 11. File Format Requirements

### Translation Input (.txt)
```
First sentence to translate.
Second sentence here.
Reference to Figure 1A should trigger image.
```

### Proofreading Input (.txt)  
```
Hello world	Hola mundo
How are you?	¿Como estas?	Missing accents
Goodbye	Adiós
```

### Translation Memory (.tmx or .txt)
TMX: Standard XML format
TXT: `source{TAB}target` per line

### Tracked Changes (.docx or .tsv)
DOCX: Word file with track changes
TSV: `original{TAB}revised` per line

---

## 12. Chunking & Performance

### Chunk Size (default: 100)
- **Small docs**: 25-50 lines per batch
- **Large docs**: 150+ lines per batch  
- **Complex content**: Smaller chunks for better context
- **Simple content**: Larger chunks for efficiency

### Performance Tips
- **Larger chunks**: Fewer API calls, faster processing
- **Smaller chunks**: Better context awareness, higher quality
- **Chunk Size = lines per LLM request**: Balance speed vs. quality

### Context Management
- **TM filtering**: Only relevant matches sent to LLM
- **Tracked changes**: Only applicable examples included  
- **Each batch includes**: Current chunk + relevant context + custom instructions

---

## 13. Error Handling & Logging

### Robust Design
- **Network issues**: Auto-retry with backoff
- **API limits**: Graceful waiting and resume
- **Real‑time log pane** (queue-driven)

### Graceful degradation when:
- **Missing provider** lib: Others still work
- **Missing API key**: Other providers available  
- **Pillow absent**: Image context disabled
- **File errors**: Placeholder in output, processing continues

### Log Analysis
- **Processing steps**: See exactly what's happening
- **Error context**: Specific lines/chunks with issues
- **Performance stats**: Time per chunk, API response times
- **Placeholder in failed output line**

---

## 14. Roadmap

For detailed version history, see:
- **[CHANGELOG-CLASSIC.md](CHANGELOG-CLASSIC.md)** - v2.x.x-CLASSIC releases
- **[CHANGELOG-CAT.md](CHANGELOG-CAT.md)** - v3.x.x-beta releases
- **[CHANGELOG.md](CHANGELOG.md)** - Overview and navigation

Planned (Unreleased):
- **Fuzzy TM matches**: Leverage partial matches intelligently  
- **Glossary enforcement**: Hard terminology constraints
- **JSON run metadata**: Detailed processing statistics
- **Token-based tracked-change scoring**: Smarter relevance filtering
- **Enhanced provider introspection**: Better model capability detection

---

## 15. Similar Projects & Tools

Supervertaler is part of a growing ecosystem of AI-powered translation tools that bring LLM capabilities to professional translators. Here are other notable projects exploring similar approaches:

### Context-Aware Translation Tools
- **[aLLMende](https://www.proz.com/forum/cafetran_support/374570-allmende_automated_imitation.html)** by Hans Lenting - AI-powered translation assistant
- **[Bohemicus CAT editor](https://www.youtube.com/watch?si=X_6YsNfjn6Ib6Faq&v=HTIPNOltNbI&feature=youtu.be)** - CAT tool with AI integration
- **[CALT: Context-Aware LLM Translator](https://github.com/CyrusCKF/translator)** - Runs locally for privacy
- **[ConText - Local Secure Translation App](https://github.com/KazKozDev/ConText)** - Privacy-focused local translation
- **[CotranslatorAI](https://cotranslatorai.com/)** - AI translation platform
- **[DeepContextual-Translate](https://github.com/RUIJIESHI0917/DeepContextual-Translate/tree/main)** - Deep learning context translation
- **[toLLMatch🔪](https://github.com/RomanKoshkin/toLLMatch)** - Context-aware LLM-based simultaneous translation

### Automation & Integration Tools
- **[ChatGPT-AutoHotkey-Utility](https://github.com/kdalanon/ChatGPT-AutoHotkey-Utility)** - AutoHotkey integration for ChatGPT
- **[LLM-AutoHotkey-Assistant](https://github.com/kdalanon/LLM-AutoHotkey-Assistant)** - General LLM automation
- **[openai_translation](https://github.com/gasparl/openai_translation?utm_source=chatgpt.com)** - OpenAI translation utilities
- **[openai-translator](https://github.com/openai-translator/openai-translator)** - Cross-platform translation tool

### Why Supervertaler?
While many tools offer AI translation, Supervertaler's unique approach combines:
- **Multiple context sources** (document, TM, tracked changes, images, custom instructions)
- **Professional CAT tool integration** (memoQ & CafeTran bilingual DOCX workflows in v2.4.3-CLASSIC; expanded CAT support in v3.1.0-beta)
- **Specialized domain prompts** (legal, medical, technical, financial, etc.)
- **Project library system** (save/restore complete workspace configurations)
- **Multimodal support** (AI sees referenced images in context)

**Know of another tool?** Contact us at [info@michaelbeijer.co.uk](mailto:info@michaelbeijer.co.uk) to add it to this list!

---

## 16. Contributing

1. **Fork** / feature branch.
2. **Add or update** functionality (ideally in discrete logic units).
3. **Update appropriate CHANGELOG** (CHANGELOG-CLASSIC.md or CHANGELOG-CAT.md depending on version).
4. **Submit PR** with concise summary.

---

## 17. License

(Choose or add a LICENSE file: MIT / Apache-2.0 / Proprietary – not specified yet.)

---

## 18. Quick Start Checklist

| Task | Done |
|------|------|
| Install dependencies | ☐ |
| Add API keys | ☐ |
| Prepare input TXT | ☐ |
| (Optional) TMX/TXT TM | ☐ |
| (Optional) DOCX / TSV tracked changes | ☐ |
| (Optional) Images folder | ☐ |
| Run script & select mode | ☐ |
| Review log & outputs | ☐ |

---

## 19. Support

Open an issue with:
- Version (shown at startup)
- Mode (Translate / Proofread)
- Provider + model
- Minimal repro input snippet
- Stack trace (if any)

---

Happy translating & proofreading!

---

## Quick verification of image support
- Add a PNG named "Figure 1A.png" to your images folder.
- Include "Figure 1A" in a test segment.
- Run with Claude and OpenAI (e.g., claude-3-5-sonnet-20241022, gpt-4o).
- Check Log for "Added Image for Figure Ref …" messages.
