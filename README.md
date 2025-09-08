# Supervertaler

AI‑powered Translator & Proofreader app, leveraging multiple context sources for enhanced accuracy, with:
- Translation & proofreading modes with **custom prompt library**
- **Advanced system prompt management** with save/load functionality
- Tracked changes ingestion (DOCX revisions + TSV)
- Figure / image contextualization (multimodal)
- Exact-match Translation Memory (TMX / TXT)
- Automatic TMX export (Translate mode)
- Chunked processing for large corpora
- Multiple LLMs supported (Claude / Gemini / OpenAI)
- **Professional 3-panel resizable GUI** (Tkinter)
- **Custom prompt templates** organized in local library

Current version: **2.2.0**

---

![supervertaler_screenshot_v2 0 0_with_source code](https://github.com/user-attachments/assets/996e9098-163e-41b3-93a3-cbe110a769ec)

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

## 2. Installation

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
   python Supervertaler_v2.2.0.py
   ```

> Pillow is optional (only needed for image / multimodal figure context).  
> If a provider library or API key is missing, related functionality is skipped gracefully.

---

## 3. 🎯 NEW: Advanced System Prompts & Custom Prompt Library

**Supervertaler v2.2.0** introduces comprehensive prompt management capabilities:

### Advanced System Prompts
- **Expandable Section**: Click "⚙️ Advanced System Prompts" to reveal the prompt editor
- **Tabbed Interface**: Separate tabs for Translation and Proofreading prompts
- **Template Variables**: Use `{source_lang}` and `{target_lang}` in your prompts
- **Live Preview**: See how your prompts will look with current language settings
- **Reset Function**: Instantly restore default prompts with one click

### Custom Prompt Library
- **Save Custom Sets**: Create named collections of your specialized prompts
- **Organized Storage**: Automatic file management in `custom_prompts/` folder
- **Easy Switching**: Browse and load different prompt sets instantly
- **Professional Use Cases**: 
  - Legal document translation prompts
  - Medical/scientific terminology sets
  - Creative writing style variations
  - Industry-specific formatting requirements

### Usage Example
1. Open Advanced System Prompts → Edit translation/proofreading prompts
2. Switch to "📁 Prompt Library" tab → Enter name → Save
3. Later: Select saved set from list → Load instantly
4. Perfect for switching between document types or client requirements!

---

## 4. API Keys

Create `api_keys.txt` next to the script (auto-template generated if absent):

```
#google = YOUR_GOOGLE_API_KEY_HERE
#claude = YOUR_CLAUDE_API_KEY_HERE
#openai = YOUR_OPENAI_API_KEY_HERE
```

Uncomment and fill lines. Multiple providers can coexist.

---

## 5. Input Formats

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

## 6. Output Formats

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

## 7. Tracked Changes

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

## 8. Images / Figures

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

## 9. Translation Memory (Translate Mode)

Supported:
- **TMX 1.4** (`<tu><tuv xml:lang=".."><seg>...`)
- **Plain TXT**: `source{TAB}target`

Process:
1. Normalize GUI language codes (e.g., “English”→“en”).
2. Apply exact matches first (fills target, skips LLM call).
3. Remaining segments go to model.

No fuzzy matching yet (planned).

---

## 10. Custom Instructions

Free‑text field appended verbatim near the system directive.  
Use for:
- Terminology constraints
- Style (e.g., “Use formal patent phrasing”)
- Locale notes

---

## 11. Chunking & Performance

- Chunk Size = number of lines per model request.
- TM filtering reduces model cost where matches exist.
- Each batch includes: needed source lines, optional images, tracked-change subset, and instructions.

---

## 12. Error Handling & Logging

- Real‑time log pane (queue-driven).
- Graceful degradation when:
  - Missing provider lib
  - Missing API key
  - Pillow absent (image context disabled)
- Placeholder inserted if model omits a numbered output line.

---

## 13. Roadmap (See CHANGELOG.md)

Planned (Unreleased):
- Fuzzy TM matches
- Glossary enforcement
- JSON run metadata
- Token-based tracked-change scoring
- Enhanced provider capability introspection

---

## 14. Contributing

1. Fork / feature branch.
2. Add or update tests (if you introduce logic units).
3. Update CHANGELOG.md (Unreleased section).
4. Submit PR with concise summary.

---

## 15. License

(Choose or add a LICENSE file: MIT / Apache-2.0 / Proprietary – not specified yet.)

---

## 16. Quick Start Checklist

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

## 17. Support

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
