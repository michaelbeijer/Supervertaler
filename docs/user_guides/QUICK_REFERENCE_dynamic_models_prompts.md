# Quick Reference: Dynamic Models & Context-Aware Prompts

## 🔄 Refresh Available Models

**Location**: Translate → API Settings

1. Enter your API key (OpenAI, Claude, or Gemini)
2. Click **🔄 Refresh Available Models** button
3. Wait 2-3 seconds for model list to update
4. Select a model from the updated list
5. Click **Save**

**What it does**: Queries the API provider to show ONLY models available to your account

**Benefits**:
- ✅ No more "403 Access Denied" errors
- ✅ See latest models automatically
- ✅ Account-specific model list

---

## 🎯 Context-Aware Translation Prompts

Supervertaler automatically chooses the best prompt for your workflow:

### Ctrl+T (Single Segment)
**Optimized for**: Quality, context, figure references
```
"Deep understanding of context and nuance"
"Use full document context for reference"
"Support for figure/image references"
```

### Translate All Untranslated (Batch DOCX)
**Optimized for**: Consistency, structure, terminology
```
"Maintain document structure and formatting"
"Consistent terminology throughout"
"Consider document-wide context"
```

### Bilingual TXT Import (Future)
**Optimized for**: Segment alignment, numbered output
```
"Maintain segment numbering"
"Preserve formatting markers"
"Aligned translations"
```

---

## 🛠️ How It Works

1. **You translate**: Press Ctrl+T or click "Translate All Untranslated"
2. **App detects mode**: Single segment vs batch translation
3. **Selects prompt**: Uses optimized prompt for that mode
4. **AI translates**: Gets clear, mode-specific instructions
5. **Better results**: Higher quality, fewer errors

---

## 💡 Tips

- **Custom prompts still work**: Load a custom prompt to override auto-selection
- **Fallback models available**: If model refresh fails, common models are available
- **No configuration needed**: Just use the app normally, prompts auto-optimize

---

## 📊 Comparison

| Translation Method | Prompt Used | Focus |
|--------------------|-------------|-------|
| Ctrl+T on one segment | Single Segment | Quality, context |
| Translate All Untranslated | Batch DOCX | Consistency, structure |
| Bilingual TXT (future) | Batch Bilingual | Alignment, numbering |
| Custom prompt loaded | Your Custom | Your specifications |

---

## ⚙️ API Provider Support

| Provider | Model Fetching | Notes |
|----------|----------------|-------|
| OpenAI | ✅ Full dynamic fetch | Shows GPT models you have access to |
| Gemini | ✅ Full dynamic fetch | Shows Gemini models for your API key |
| Claude | ⚠️ Known models only | Anthropic has no model list endpoint |

---

## 🔧 Troubleshooting

**"No models found"**
- Check API key is correct
- Verify internet connection
- App will use fallback models automatically

**Model I want doesn't appear**
- Your API plan may not include that model
- Check provider dashboard
- Use an available model or upgrade plan

**Prompt seems wrong**
- Load a custom prompt if you need specific instructions
- Context-aware prompts optimize for common workflows
- Custom prompts always override auto-selection
