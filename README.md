# Supervertaler

AI‑powered Translator & Proofreader app, supporting multiple sources of context, with:
- Translation & proofreading modes
- Tracked changes ingestion (DOCX revisions + TSV)
- Figure / image contextualization (multimodal)
- Exact-match Translation Memory (TMX / TXT)
- Automatic TMX export (Translate mode)
- Chunked processing for large corpora
- Multiple LLMs supported (Claude / Gemini / OpenAI)
- GUI-based operation (Tkinter)

Current version: **2.0.1**

---

## 1. Features Overview

| Capability | Translate Mode | Proofread Mode |
|------------|----------------|----------------|
| Source ingestion (.txt) | 1 column (source) | source{TAB}target[{TAB}comment] |
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
   python Supervertaler_v2.0.0.py
   ```

> Pillow is optional (only needed for image / multimodal figure context).  
> If a provider library or API key is missing, related functionality is skipped gracefully.

---

## 3. API Keys

Create `api_keys.txt` next to the script (auto-template generated if absent):

```
#google = YOUR_GOOGLE_API_KEY_HERE
#claude = YOUR_CLAUDE_API_KEY_HERE
#openai = YOUR_OPENAI_API_KEY_HERE
```

Uncomment and fill lines. Multiple providers can coexist.

---

## 4. Input Formats

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

## 5. Output Formats

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

## 6. Tracked Changes

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

## 7. Images / Figures

Place figure image files in a chosen “Document Images Folder”.

Normalization examples (all map to `fig1a`):
```
Figure 1A.png
fig_1-a.JPG
Figuur 1-A.webp
```

On a line referencing “Figure 1A” / “Fig. 1A” the corresponding image is inserted into the model prompt before that line.

---

## 8. Translation Memory (Translate Mode)

Supported:
- **TMX 1.4** (`<tu><tuv xml:lang=".."><seg>...`)
- **Plain TXT**: `source{TAB}target`

Process:
1. Normalize GUI language codes (e.g., “English”→“en”).
2. Apply exact matches first (fills target, skips LLM call).
3. Remaining segments go to model.

No fuzzy matching yet (planned).

---

## 9. Custom Instructions

Free‑text field appended verbatim near the system directive.  
Use for:
- Terminology constraints
- Style (e.g., “Use formal patent phrasing”)
- Locale notes

---

## 10. Chunking & Performance

- Chunk Size = number of lines per model request.
- TM filtering reduces model cost where matches exist.
- Each batch includes: needed source lines, optional images, tracked-change subset, and instructions.

---

## 11. Error Handling & Logging

- Real‑time log pane (queue-driven).
- Graceful degradation when:
  - Missing provider lib
  - Missing API key
  - Pillow absent (image context disabled)
- Placeholder inserted if model omits a numbered output line.

---

## 12. Roadmap (See CHANGELOG.md)

Planned (Unreleased):
- Fuzzy TM matches
- Glossary enforcement
- JSON run metadata
- Token-based tracked-change scoring
- Enhanced provider capability introspection

---

## 13. Contributing

1. Fork / feature branch.
2. Add or update tests (if you introduce logic units).
3. Update CHANGELOG.md (Unreleased section).
4. Submit PR with concise summary.

---

## 14. License

(Choose or add a LICENSE file: MIT / Apache-2.0 / Proprietary – not specified yet.)

---

## 15. Quick Start Checklist

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

## 16. Support

Open an issue with:
- Version (shown at startup)
- Mode (Translate / Proofread)
- Provider + model
- Minimal repro input snippet
- Stack trace (if any)

---

Happy translating & proofreading!
