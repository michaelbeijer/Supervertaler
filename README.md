# Supervertaler
# Supervertaler

**Version 2.5.0 (In Development)** - AI-Powered Translation Tool with Advanced CAT Features

> **Note**: Two versions are maintained:
> - `Supervertaler_v2.4.0 (stable - production ready).py` - Tested and stable for production use
> - `Supervertaler_v2.5.0 (experimental - CAT editor development).py` - Active development with new features

🎯 **Context-aware, LLM-powered translation & proofreading tool, leveraging multiple context sources for enhanced accuracy (built for translators)** - Revolutionary approach to document translation that leverages multiple context sources for unparalleled accuracy.

**Note**: A standalone CAT (Computer-Aided Translation) editor prototype is under active development in the *cat_tool_prototype/* folder. **Latest: v0.4.2** with dual text selection (memoQ-style), column management, formatting display, and three professional view modes (Grid, List, Document). We're implementing features from [michaelbeijer.co.uk/what_i_look_for_in_a_cat_tool](https://michaelbeijer.co.uk/what_i_look_for_in_a_cat_tool). See `cat_tool_prototype/README.md` for details.

## 🔧 CAT Tool Integration

**Supervertaler is designed for professional translators using CAT tools** (memoQ, Trados Studio, CafeTran, Wordfast, etc.). It integrates seamlessly into existing translation workflows:

### Input Workflow:
1. **Export from CAT tool**: Export bilingual table from your CAT tool (usually .docx or .rtf format)
2. **Extract source text**: Copy all rows from the source language column
3. **Create .txt input**: Paste into plain text file, one segment per line
4. **Process with Supervertaler**: Use Translation mode for AI-powered translation

### Output Integration:
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

**📋 Complete User Guide**: [`Supervertaler User Guide (v2.3.0).md`](Supervertaler%20User%20Guide%20(v2.3.0).md)
- **5-minute Quick Start**: Get up and running immediately
- **Complete Feature Documentation**: Comprehensive coverage of all capabilities
- **Domain-Specific Prompts**: Professional prompt collections for specialized fields
- **Project Library**: Revolutionary workspace management
- **Troubleshooting**: Common issues and solutions
- **Advanced Tips**: Professional workflow optimization

## 1. Features Overview

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

## 14. Roadmap (See CHANGELOG.md)

Planned (Unreleased):
- **Fuzzy TM matches**: Leverage partial matches intelligently  
- **Glossary enforcement**: Hard terminology constraints
- **JSON run metadata**: Detailed processing statistics
- **Token-based tracked-change scoring**: Smarter relevance filtering
- **Enhanced provider introspection**: Better model capability detection

---

## 15. Contributing

1. **Fork** / feature branch.
2. **Add or update** functionality (ideally in discrete logic units).
3. **Update CHANGELOG.md** (add entry in Unreleased section).
4. **Submit PR** with concise summary.

---

## 16. License

(Choose or add a LICENSE file: MIT / Apache-2.0 / Proprietary – not specified yet.)

---

## 17. Quick Start Checklist

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

## 18. Support

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
