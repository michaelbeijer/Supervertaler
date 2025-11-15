# AI Agent Translation Workflow Concept

## Context: The Problem

While using Gemini API for batch translation (German → Dutch), encountered a **429 "Resource exhausted"** error during batch processing:

```
Batch 5/6 (100 segments)...
Translation error: 429 Resource exhausted. Please try again later.
```

### Root Cause
- **Rate limiting**: Too many API requests per minute (RPM) or tokens per minute (TPM)
- Batches 1-4 succeeded, but accumulated requests exceeded Google Cloud limits by batch 5
- Retry logic worked, but indicates systemic rate limit issue

### Traditional Solutions
1. Add delays between batches (2-5 seconds)
2. Reduce batch size (50 or 25 segments instead of 100)
3. Implement exponential backoff
4. Upgrade API tier for higher rate limits
5. Check/increase quotas in Google Cloud Console

---

## New Approach: Using Coding Assistants for Translation

### Core Idea
Instead of batch API calls, use **Cursor Desktop** or **GitHub Copilot in VS Code** as a CAT (Computer-Assisted Translation) tool replacement by:

1. Converting bilingual files into markdown tables
2. Using the AI agent's chat interface for translation
3. Leveraging workspace context for consistency and quality

---

## Why This Could Work

### Advantages of Coding Assistants

| Feature | Benefit for Translation |
|---------|------------------------|
| **Large context windows** | Sees entire project, maintains consistency across all segments |
| **Structured data expertise** | Handles markdown tables, TSV, CSV natively |
| **Workspace awareness** | Can reference glossaries, style guides, previous translations |
| **Iterative refinement** | Chat interface allows real-time feedback and adjustments |
| **No rate limits** | Avoids API 429 errors (mostly) |
| **Intelligent context** | Understands relationships between segments better than batch processing |

### What Coding Assistants Offer That CAT Tools Don't

- **Complex contextual instructions**: "Use informal 'je' for this marketing content, but 'u' for legal disclaimers"
- **Cross-segment understanding**: Sees surrounding context for disambiguation
- **On-the-fly adjustments**: Easy to refine tone, fix terminology, batch-update terms
- **No rigid segmentation**: Can handle context across sentence boundaries
- **Ad-hoc QA**: Just ask: "Check if all numbers are preserved" or "Find terminology inconsistencies"

---

## Proposed Workflow

### Step 1: Workspace Setup

```
translation-project/
├── source.md              # Markdown table with source segments
├── glossary.md            # Client-specific terminology
├── style-guide.md         # Translation guidelines & tone
├── previous-translations.md  # Similar past work for reference
└── output.md              # Translated segments (generated)
```

### Step 2: Format Source File

Convert your CAT tool export into a markdown table:

```markdown
| Segment ID | Source (German) | Target (Dutch) | Notes |
|------------|-----------------|----------------|-------|
| 001 | Willkommen | | |
| 002 | Einstellungen | | |
| 003 | Bitte wählen Sie eine Option | | |
```

### Step 3: Create Reference Files

**glossary.md:**
```markdown
# Translation Glossary - Client: Gigaset

| German | Dutch | Notes |
|--------|-------|-------|
| Einstellungen | Instellingen | Always use, not "configuratie" |
| Gerät | Apparaat | Hardware context |
| Anruf | Oproep | Noun form |
```

**style-guide.md:**
```markdown
# Style Guide: Gigaset (DE→NL)

- **Formality**: Use formal "u" form for UI
- **Brand names**: Keep untranslated (Gigaset, etc.)
- **Numbers**: Preserve exactly, including decimal separators
- **Tags**: Maintain all XML/HTML tags unchanged
```

### Step 4: Translation Prompt

In Cursor/Copilot chat:

```
Translate the German source text to Dutch in source.md:

- Use glossary.md for terminology
- Follow style-guide.md conventions
- Maintain formal tone (use "u")
- Preserve all formatting, numbers, and tags
- Fill in the "Target (Dutch)" column

Start with segments 001-050, then I'll review before continuing.
```

### Step 5: Iterative Refinement

```
"Change all instances of 'configuratie' to 'instellingen' to match glossary"

"In segment 023, use a more natural Dutch word order"

"Check all segments for consistency in how 'Anruf' is translated"
```

---

## Advanced Use Cases

### Consistency Checks
```
"Find all instances where I translated 'Gerät' and ensure consistency"

"List any segments where the translation is significantly longer/shorter than source"
```

### Quality Assurance
```
"Verify all numbers match between source and target"

"Check that all XML tags in source appear in target"

"Identify any untranslated segments"
```

### Batch Updates
```
"Update all instances of [old term] to [new term] throughout the file"

"Change tone from formal to informal for segments 100-150"
```

---

## Limitations vs. Traditional CAT Tools

| Missing Feature | Workaround |
|----------------|------------|
| ❌ Translation Memory (TM) database | Include previous-translations.md in workspace |
| ❌ Automatic repetition detection | Ask agent: "Find repeated segments" |
| ❌ Built-in QA checks | Request specific checks via chat |
| ❌ TM fuzzy matching | Provide similar past translations as context |
| ❌ Integrated term bases | Use glossary.md files |
| ❌ Native CAT file formats | Manual export/import needed |

---

## Potential Enhancements

### 1. Scripted Preprocessing
Create a Python script to convert CAT exports to markdown:

```python
# cat_to_markdown.py
# Convert bilingual TMX/XLSX to markdown table
# Include segment IDs, source, target, notes columns
```

### 2. Post-Processing
Script to convert completed markdown back to CAT format:

```python
# markdown_to_tmx.py
# Generate TMX file from completed markdown table
```

### 3. Workspace Templates
Standardized project structure for different language pairs/clients

### 4. Custom Instructions
Store client-specific prompts for consistency:

```markdown
# GIGASET-PROMPT.md
Always use when translating Gigaset materials:
- Formal "u" form
- Technical accuracy > naturalness
- Preserve all product names
```

---

## Next Steps: Implementation Plan

### Phase 1: Proof of Concept
1. [ ] Take a small bilingual file (50 segments)
2. [ ] Convert to markdown table
3. [ ] Create minimal glossary.md
4. [ ] Test translation in Cursor/Copilot
5. [ ] Evaluate quality vs. current workflow

### Phase 2: Refinement
1. [ ] Develop preprocessing script (CAT export → markdown)
2. [ ] Test with larger file (500+ segments)
3. [ ] Document optimal prompt patterns
4. [ ] Create client-specific templates

### Phase 3: Production Use
1. [ ] Develop post-processing script (markdown → TMX/CAT format)
2. [ ] Compare quality/speed with traditional CAT + Gemini API
3. [ ] Establish QA checklist specific to this workflow
4. [ ] Create reusable workspace templates

---

## Open Questions to Explore

1. **Segment limits**: What's the practical maximum for one file? (Test with 1000, 5000, 10000 segments)
2. **Context optimization**: Do smaller files with better context beat larger files? 
3. **Multi-file projects**: How to maintain consistency across multiple files?
4. **Revision tracking**: How to handle updates/revisions systematically?
5. **Collaboration**: Can multiple translators work in same workspace effectively?

---

## Resources

### Tools Referenced
- **Cursor Desktop**: AI-powered code editor (https://cursor.sh)
- **GitHub Copilot**: AI pair programmer for VS Code
- **Current workflow**: Gemini API batch translation

### Related Concepts
- CAT tools (Computer-Assisted Translation)
- Translation Memory (TM)
- TMX format (Translation Memory eXchange)

### Error Encountered
- Gemini API 429 error: https://cloud.google.com/vertex-ai/generative-ai/docs/error-code-429

---

## Conclusion

This approach leverages the strengths of coding assistants (context awareness, flexibility, iterative refinement) while working around their limitations (no TM database) through smart workspace organization. 

**Key insight**: Modern AI coding assistants are essentially "context-aware text processors" — which is exactly what translation requires.

The feasibility depends on:
- Project size (smaller projects may work better)
- Need for TM leverage (less critical if using AI)
- Workflow flexibility requirements (higher = better fit)

**Recommendation**: Start with a small pilot project to validate before committing to full production use.

---

*Document created: 2025-11-07*
*Context: Exploring alternatives to rate-limited API batch translation*
