# AI Translation Overview

Supervertaler integrates with leading AI language models for high-quality translation.

## Supported Providers

| Provider | Models | Speed | Quality | Cost |
|----------|--------|-------|---------|------|
| **OpenAI** | GPT-4o, GPT-4-turbo | ⚡ Fast | ⭐⭐⭐⭐⭐ | $$ |
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus | ⚡ Fast | ⭐⭐⭐⭐⭐ | $$ |
| **Google** | Gemini 1.5 Pro | ⚡ Fast | ⭐⭐⭐⭐ | $ |
| **Ollama** | Llama 3, Mistral, etc. | 🐢 Varies | ⭐⭐⭐-⭐⭐⭐⭐ | Free |

## Quick Start

1. [Set up API keys](../get-started/api-keys.md)
2. Open a project with segments to translate
3. Select a segment
4. Press `Ctrl+T` to translate

## Translation Methods

### Single Segment

Translate one segment at a time:
- Select a segment
- Press `Ctrl+T` or click **Translate** button
- AI translation appears in the target cell
- Review, edit, and confirm

### Batch Translation

Translate multiple segments at once:
- Select segments (Shift+click for range)
- Press `Ctrl+Shift+T` or use **Edit → Batch Translate**
- Configure options in the dialog
- All selected segments are translated

{% hint style="info" %}
Supervertaler has multiple batch scopes (selected / not-started / etc.). Start with **Edit → Batch Translate → Translate all not-started & pre-translated**.
{% endhint %}

### TM + AI Hybrid

Combine Translation Memory with AI:
1. TM matches are checked first
2. High matches (e.g., >90%) are used directly
3. Lower matches are AI-translated with TM context
4. No matches use pure AI translation

## Prompts

Prompts control how the AI translates. A good prompt includes:

- Translation direction (source → target language)
- Domain/subject matter
- Style guidelines
- Terminology rules
- Special instructions

### Example Prompt

```
You are a professional Dutch-to-English translator specializing 
in technical documentation. 

Maintain formal register. Use American English spelling. 
Keep all formatting tags like {1}, <b>, </b> in place.

Translate naturally while preserving the original meaning.
```

See [Creating Prompts](prompts.md) and [Prompt Library](prompt-library.md) for more.

## Provider Selection

### In Settings

1. Go to **Settings** tab
2. Find **LLM Settings**
3. Choose your preferred **Provider** and **Model**
4. Save settings

### Per-Translation

When batch translating, you can choose the provider in the dialog.

## Quality Tips

### Get Better Results

1. **Use specific prompts** - Include domain, style, and rules
2. **Provide context** - Enable "include context" for surrounding segments
3. **Add glossary terms** - Attach terminology for consistent translations
4. **Post-edit** - AI is great but not perfect; always review

### Common Issues

| Issue | Solution |
|-------|----------|
| Wrong terminology | Add terms to glossary, include in prompt |
| Inconsistent style | Be more specific in your prompt |
| Tags removed/moved | Explicitly tell AI to preserve tags |
| Too literal | Ask for "natural, fluent" translation |

## Cost Management

### API costs

Cloud providers typically charge by usage (tokens). Pricing and free tiers change over time, so treat each provider dashboard as the source of truth.

### Reducing Costs

1. **Use Ollama** (local) when appropriate
2. **Translate only what you need** (for example not-started segments)
3. **Pre-translate with TM** when you have good matches
4. **Use smaller/faster models** for drafts, larger models for final passes

---

## Learn More

<table data-view="cards">
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Single Segment</strong></td>
<td><a href="single-segment.md">Translate one at a time →</a></td>
</tr>
<tr>
<td><strong>Batch Translation</strong></td>
<td><a href="batch-translation.md">Translate in bulk →</a></td>
</tr>
<tr>
<td><strong>Creating Prompts</strong></td>
<td><a href="prompts.md">Write effective prompts →</a></td>
</tr>
<tr>
<td><strong>Local AI (Ollama)</strong></td>
<td><a href="ollama.md">Free, private AI →</a></td>
</tr>
</tbody>
</table>
