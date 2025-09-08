# Supervertaler

🎯 **Multicontextual AI Translation & Proofreading Suite** - Revolutionary approach to document translation that leverages multiple context sources for unparalleled accuracy.

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
- **Cross-platform Support** - Clickable folder paths work on Windows, macOS, and Linux
- **Chunked processing** - Handle large documents with intelligent batching
- **Multiple LLM support** - Claude, Gemini, and OpenAI integration
- **Automatic TMX export** - Build translation memories from your work

**Current version: 2.3.0**
---

![supervertaler_screenshot_v2 0 0](https://github.com/user-attachments/assets/39cc08ee-0709-4ebe-af23-d39eaa21abbb)

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

> Pillow is optional (only needed for image / multimodal figure context).  
> If a provider library or API key is missing, related functionality is skipped gracefully.

---

## 4. 🎯 NEW: Project Management & Library System

**Supervertaler v2.3.0** introduces a revolutionary triple-library system for complete workflow management:

### 💼 Project Library (NEW!)
- **Complete Workspace Saving**: Save entire application state in one click
- **Configuration Management**: Languages, providers, models, file paths, prompts - everything
- **Client/Project Switching**: Instant switching between different project configurations
- **Cross-platform Storage**: JSON-based projects work on Windows, macOS, Linux
- **Clickable Folder Access**: Direct access to project directory from the interface

### 📝 Prompt Library (Renamed from Advanced System Prompts)
- **Expandable Section**: Click "📝 Prompt Library" to reveal the prompt editor
- **Tabbed Interface**: Separate tabs for Translation and Proofreading prompts with ⚡ active indicators
- **Template Variables**: Use `{source_lang}` and `{target_lang}` in your prompts
- **Live Preview**: See how your prompts will look with current language settings
- **Reset Function**: Instantly restore default prompts with one click

### 📚 Custom Prompt Library
- **Save Custom Sets**: Create named collections of your specialized prompts
- **Organized Storage**: Automatic file management in `custom_prompts/` folder
- **Easy Switching**: Browse and load different prompt sets instantly
- **Pre-built Domain Collections** (NEW!):
  - **Medical Translation Specialist**: Patient safety, medical terminology, regulatory compliance
  - **Legal Translation Specialist**: Juridical precision, legal system differences, formal register
  - **Financial Translation Specialist**: Banking terminology, regulatory compliance, market conventions
  - **Technical Translation Specialist**: Engineering precision, safety warnings, technical documentation
  - **Cryptocurrency & Blockchain Specialist**: DeFi protocols, Web3 terminology, security considerations
  - **Gaming & Entertainment Specialist**: Cultural adaptation, character voice, user experience optimization

### Usage Example
1. Open Advanced System Prompts → Edit translation/proofreading prompts
2. Switch to "📁 Prompt Library" tab → Enter name → Save
3. Later: Select saved set from list → Load instantly
4. Perfect for switching between document types or client requirements!

---

## 5. API Keys

Create `api_keys.txt` next to the script (auto-template generated if absent):

```
#google = YOUR_GOOGLE_API_KEY_HERE
#claude = YOUR_CLAUDE_API_KEY_HERE
#openai = YOUR_OPENAI_API_KEY_HERE
```

Uncomment and fill lines. Multiple providers can coexist.

---

## 6. Input Formats

### Translate Mode
```
Source sentence 1
Source sentence 2
...
```
If you re‑feed a previously exported 2‑column file:
```
Source sentence 1{TAB}Old translation
```
Only the first column is read; the rest are ignored.

### Proofread Mode
```
Source{TAB}ExistingTarget
Source{TAB}ExistingTarget{TAB}Optional prior comment
```

---

## 7. Output Formats

### Translate Output
```
Source{TAB}NewTranslation
```
Plus: `*.tmx` (exact matches + generated translations, excludes error placeholders).

### Proofread Output
```
Source{TAB}RevisedTarget{TAB}MergedComment
```
MergedComment includes (if present):
- ORIGINAL COMMENT:
- PROOFREADER COMMENT (AI):

If no changes: AI may omit revisions or summarize “No changes”.

---

## 8. Tracked Changes

Load:
- **DOCX** with Word tracked revisions (insertions/deletions)
- **TSV**: `Original{TAB}Final`

Browser UI:
- Search (substring or exact)
- View full original / final pair
- Copy single or combined entries

Context Injection:
- Per batch: exact matches first, then partial word-overlap (≥2 meaningful tokens)
- Capped length to protect token budget

---

## 9. Images / Figures

Place figure image files in a chosen “Document Images Folder”.

Normalization examples (all map to `fig1a`):
```
Figure 1A.png
fig_1-a.JPG
Figuur 1-A.webp
```

On a line referencing “Figure 1A” / “Fig. 1A” the corresponding image is inserted into the model prompt before that line.

Supported providers:
- **Gemini**: PIL images embedded in prompt.
- **Claude**: base64 image blocks.
- **OpenAI**: data URL image_url blocks.

---

## 10. Translation Memory (Translate Mode)

Supported:
- **TMX 1.4** (`<tu><tuv xml:lang=".."><seg>...`)
- **Plain TXT**: `source{TAB}target`

Process:
1. Normalize GUI language codes (e.g., “English”→“en”).
2. Apply exact matches first (fills target, skips LLM call).
3. Remaining segments go to model.

No fuzzy matching yet (planned).

---

## 11. Custom Instructions

Free‑text field appended verbatim near the system directive.  
Use for:
- Terminology constraints
- Style (e.g., “Use formal patent phrasing”)
- Locale notes

---

## 12. Chunking & Performance

- Chunk Size = number of lines per model request.
- TM filtering reduces model cost where matches exist.
- Each batch includes: needed source lines, optional images, tracked-change subset, and instructions.

---

## 13. Error Handling & Logging

- Real‑time log pane (queue-driven).
- Graceful degradation when:
  - Missing provider lib
  - Missing API key
  - Pillow absent (image context disabled)
- Placeholder inserted if model omits a numbered output line.

---

## 14. Roadmap (See CHANGELOG.md)

Planned (Unreleased):
- Fuzzy TM matches
- Glossary enforcement
- JSON run metadata
- Token-based tracked-change scoring
- Enhanced provider capability introspection

---

## 15. Contributing

1. Fork / feature branch.
2. Add or update tests (if you introduce logic units).
3. Update CHANGELOG.md (Unreleased section).
4. Submit PR with concise summary.

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
- Add a PNG named “Figure 1A.png” to your images folder.
- Include “Figure 1A” in a test segment.
- Run with Claude and OpenAI (e.g., claude-3-5-sonnet-20241022, gpt-4o).
- Check Log for “Added Image for Figure Ref …” messages.
