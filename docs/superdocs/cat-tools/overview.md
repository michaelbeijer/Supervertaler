# CAT Tool Integration Overview

Supervertaler is designed to work alongside professional CAT (Computer-Assisted Translation) tools, not replace them. Use it as a **companion tool** for AI-powered translation within your existing workflow.

## Supported CAT Tools

| CAT Tool | Import Format | Export Format |
|----------|--------------|---------------|
| **memoQ** | Bilingual DOCX, XLIFF | Bilingual DOCX |
| **Trados Studio** | SDLPPX packages | SDLRPX return packages |
| **Phrase (Memsource)** | Bilingual DOCX | Bilingual DOCX |
| **CafeTran Espresso** | Bilingual table DOCX | Bilingual table DOCX |

## Why Use Supervertaler with CAT Tools?

### AI Translation Power

CAT tools have limited AI integration. Supervertaler lets you:
- Use multiple LLM providers (GPT-4, Claude, Gemini)
- Create custom translation prompts
- Batch translate with context awareness
- Leverage semantic TM search (Supermemory)

### Workflow Flexibility

- Translate offline with Ollama
- Work on files while others are locked in the CAT tool
- Quick review and post-editing without heavy software

## Typical Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR CAT TOOL                            │
│  (memoQ, Trados, Phrase, CafeTran)                         │
│                                                             │
│  1. Receive project from client                            │
│  2. Set up TM, termbases in CAT tool                       │
│  3. Export bilingual file or package                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    SUPERVERTALER                            │
│                                                             │
│  4. Import bilingual file                                  │
│  5. AI translate + post-edit                               │
│  6. Use Superlookup for research                           │
│  7. Export bilingual file                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    YOUR CAT TOOL                            │
│                                                             │
│  8. Import translations back                               │
│  9. Run QA checks                                          │
│  10. Deliver to client                                     │
└─────────────────────────────────────────────────────────────┘
```

## Key Concepts

### Preserving Formatting

Supervertaler preserves CAT tool formatting tags:
- memoQ: `{1}`, `[2}`, `{MQ}` inline tags
- Trados: `<1>`, `</1>` numbered tags
- Tags are highlighted in the grid for visibility

### Segment Status

Segment statuses map between tools:
- **Not Started** → Draft/Not Translated
- **Translated** → Translated
- **Confirmed** → Confirmed/Approved

### Round-Trip Compatibility

Files exported from Supervertaler can be imported back into the CAT tool with:
- All translations preserved
- Status information maintained
- Formatting intact

## Choosing the Right Workflow

| Scenario | Recommended Workflow |
|----------|---------------------|
| **Full project in memoQ** | [memoQ Bilingual DOCX](memoq.md) |
| **Trados Studio package** | [SDLPPX/SDLRPX](trados.md) |
| **Phrase/Memsource project** | [Phrase Bilingual DOCX](phrase.md) |
| **CafeTran external view** | [CafeTran DOCX](cafetran.md) |
| **Standalone DOCX** | Direct import, no CAT tool needed |

---

## Tool-Specific Guides

<table data-view="cards">
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>memoQ</strong></td>
<td><a href="memoq.md">memoQ workflow guide →</a></td>
</tr>
<tr>
<td><strong>Trados Studio</strong></td>
<td><a href="trados.md">Trados workflow guide →</a></td>
</tr>
<tr>
<td><strong>Phrase</strong></td>
<td><a href="phrase.md">Phrase workflow guide →</a></td>
</tr>
<tr>
<td><strong>CafeTran</strong></td>
<td><a href="cafetran.md">CafeTran workflow guide →</a></td>
</tr>
</tbody>
</table>
