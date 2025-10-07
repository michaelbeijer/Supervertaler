# Dynamic Model Fetching & Context-Aware Prompts

**Date**: October 6, 2025
**Version**: v2.5.0

## Overview

Two major enhancements have been added to improve translation quality and user experience:

1. **Dynamic Model Fetching**: Automatically discover available AI models based on your API key
2. **Context-Aware Prompts**: Intelligent prompt selection based on translation mode

---

## 1. Dynamic Model Fetching

### What It Does

Instead of using a hardcoded list of models, Supervertaler now queries each AI provider's API to discover which models are actually available to you based on your API key and subscription tier.

### Benefits

- ✅ **No more 403 errors** from trying to use models you don't have access to
- ✅ **Always up-to-date** with the latest models from each provider
- ✅ **Automatic filtering** - only shows models you can actually use
- ✅ **Smart sorting** - models ordered by preference (e.g., gpt-4o first)

### How to Use

1. Open **Translate → API Settings**
2. Enter your API key for any provider (OpenAI, Claude, or Gemini)
3. Click the **🔄 Refresh Available Models** button
4. Wait a few seconds while models are fetched
5. The dropdown will update with only models available to your account

### Supported Providers

| Provider | Model Discovery | Notes |
|----------|----------------|-------|
| **OpenAI** | ✅ Full support | Queries `/v1/models` endpoint, filters for GPT models |
| **Gemini** | ✅ Full support | Queries `list_models()`, filters for content generation |
| **Claude** | ⚠️ Limited | Returns known models (Anthropic has no list endpoint) |

### Fallback Behavior

If model fetching fails (no internet, invalid API key, etc.), Supervertaler falls back to a curated list of common models:

**OpenAI Fallback**:
- gpt-4o
- gpt-4o-mini
- gpt-4-turbo
- gpt-4

**Claude Fallback**:
- claude-3-5-sonnet-20241022
- claude-3-5-haiku-20241022
- claude-3-opus-20240229

**Gemini Fallback**:
- gemini-2.5-pro-preview-05-06
- gemini-2.5-flash-preview-05-06
- gemini-1.5-pro-latest
- gemini-1.5-flash-latest

### Technical Details

The `fetch_available_models()` function handles model discovery:

```python
def fetch_available_models(provider: str, api_key: str) -> List[str]:
    """Fetch available models from API provider"""
    # OpenAI: Query models API, filter for GPT models, sort by preference
    # Gemini: Query list_models(), filter for content generation
    # Claude: Return known models (no API endpoint)
    # Returns fallback list if fetch fails
```

---

## 2. Context-Aware Prompts

### What It Does

Supervertaler now automatically selects the most appropriate translation prompt based on how you're translating:

- **Single Segment** (Ctrl+T): Focused, context-rich prompt for individual segments
- **Batch DOCX**: Document-oriented prompt emphasizing consistency
- **Batch Bilingual** (future): Prompt for numbered bilingual files (memoQ exports)

### Translation Modes

#### Mode 1: Single Segment Translation (Ctrl+T)

**When**: Translating one segment at a time with Ctrl+T

**Prompt Focus**:
- Deep context understanding
- Reference to full document
- Support for figure/image references
- Maximum translation quality

**Example Prompt**:
```
You are an expert English to Dutch translator with deep understanding of context and nuance.

**CONTEXT**: Full document context is provided for reference below.

**YOUR TASK**: Translate ONLY the text in the 'TEXT TO TRANSLATE' section.

**IMPORTANT INSTRUCTIONS**:
- Provide ONLY the translated text
- Do NOT include numbering, labels, or commentary
- Do NOT repeat the source text
- Maintain accuracy and natural fluency

If the text refers to figures (e.g., 'Figure 1A'), relevant images may be provided for visual context.
```

#### Mode 2: Batch DOCX Translation

**When**: Using "Translate All Untranslated" on a DOCX document

**Prompt Focus**:
- Document structure preservation
- Terminology consistency across segments
- Efficient batch processing
- Parallel segment handling

**Example Prompt**:
```
You are an expert English to Dutch translator specializing in document translation.

**YOUR TASK**: Translate ALL segments below while maintaining document structure and formatting.

**IMPORTANT INSTRUCTIONS**:
- Translate each segment completely and accurately
- Preserve paragraph breaks and structure
- Maintain consistent terminology throughout
- Consider document-wide context for accuracy
- Output translations in the same order as source segments
```

#### Mode 3: Batch Bilingual Translation (Future)

**When**: Translating bilingual TXT files (memoQ exports)

**Prompt Focus**:
- Segment number alignment
- Bilingual format awareness
- Special marker preservation
- Numbered output

**Example Prompt**:
```
You are an expert English to Dutch translator working with a bilingual translation file.

**YOUR TASK**: Translate each source segment below.

**FILE FORMAT**: This is a bilingual export (e.g., from memoQ) where each segment is numbered.

**IMPORTANT INSTRUCTIONS**:
- Translate each numbered segment
- Maintain segment numbering in your output
- Keep translations aligned with source segment numbers
- Preserve any special formatting markers
- Ensure consistency across all segments
```

### How It Works

The `get_context_aware_prompt()` method automatically selects the right prompt:

```python
def get_context_aware_prompt(self, mode: str = "single") -> str:
    """Get the appropriate translation prompt based on context.
    
    Args:
        mode: 'single', 'batch_docx', or 'batch_bilingual'
    
    Returns:
        The appropriate prompt template
    """
    # If user selected custom prompt, use that
    if self.current_translate_prompt != self.single_segment_prompt:
        return self.current_translate_prompt
    
    # Otherwise, select based on mode
    if mode == "single":
        return self.single_segment_prompt
    elif mode == "batch_docx":
        return self.batch_docx_prompt
    elif mode == "batch_bilingual":
        return self.batch_bilingual_prompt
    else:
        return self.single_segment_prompt  # Fallback
```

### Custom Prompts Still Work

If you load a custom prompt from **Translate → Custom Prompts**, that prompt takes precedence over the context-aware defaults. This allows domain specialists to use specialized prompts (legal, medical, technical, etc.) while still benefiting from the framework.

---

## Benefits

### Dynamic Model Fetching Benefits

1. **Avoid API Errors**: Never try to use models you don't have access to
2. **Stay Current**: Automatically see new models as they're released
3. **Account-Specific**: Only shows models available to YOUR subscription
4. **Time-Saving**: No manual model list updates needed

### Context-Aware Prompts Benefits

1. **Better Translation Quality**: Each mode gets optimized instructions
2. **Reduced Errors**: AI gets clear, mode-specific guidance
3. **Automatic Selection**: No manual prompt switching needed
4. **Consistency**: Batch translations maintain terminology across document
5. **Flexibility**: Custom prompts still work when needed

---

## Usage Examples

### Example 1: First-Time Setup

```
1. Open Translate → API Settings
2. Enter your OpenAI API key: sk-proj-...
3. Click "🔄 Refresh Available Models"
4. See available models:
   ✓ gpt-4o
   ✓ gpt-4o-mini
   ✗ gpt-4-turbo (not available on your plan)
5. Select gpt-4o
6. Click Save
```

### Example 2: Single Segment Translation

```
1. Import DOCX document
2. Click on segment #5 (a technical description)
3. Press Ctrl+T
4. Supervertaler uses single_segment_prompt:
   - Includes full document context
   - Optimized for individual segment quality
   - Supports figure references
5. High-quality translation appears
```

### Example 3: Batch Document Translation

```
1. Import 50-page technical manual
2. Click "Translate All Untranslated"
3. Supervertaler uses batch_docx_prompt:
   - Emphasizes terminology consistency
   - Maintains document structure
   - Efficient batch processing
4. All 200 segments translated with consistent terms
```

---

## API Provider Comparison

| Feature | OpenAI | Claude | Gemini |
|---------|--------|--------|--------|
| Dynamic model fetch | ✅ Full | ⚠️ Static list | ✅ Full |
| Multimodal support | ✅ GPT-4 models | ✅ All models | ✅ All models |
| Context-aware prompts | ✅ Yes | ✅ Yes | ✅ Yes |
| Fallback models | ✅ Yes | ✅ Yes | ✅ Yes |

---

## Troubleshooting

### "No models found" when refreshing

**Cause**: Invalid API key or no internet connection

**Solution**:
1. Check your API key is correct
2. Verify internet connection
3. The app will use fallback models automatically

### Model I need doesn't appear

**Cause**: Your API subscription doesn't include that model

**Solution**:
1. Check your API provider's dashboard
2. Upgrade your subscription if needed
3. Use an available model from the list

### Custom prompt not being used

**Cause**: Context-aware prompts only activate when using default prompts

**Solution**:
1. Load your custom prompt via Translate → Custom Prompts
2. It will automatically override context-aware selection
3. Click "Use Default Prompts" to re-enable context-aware behavior

---

## Implementation Notes

### Files Modified

- `Supervertaler_v2.5.0.py`:
  - Added `fetch_available_models()` function (lines ~960-1020)
  - Added context-aware prompt templates (lines ~1135-1180)
  - Added `get_context_aware_prompt()` method (lines ~1225-1250)
  - Updated `show_api_settings()` with refresh button (lines ~7295-7360)
  - Updated `translate_current_segment()` to use context-aware prompts
  - Updated `translate_all_untranslated()` to use batch prompt

### Code Size

- Dynamic model fetching: ~70 lines
- Context-aware prompts: ~80 lines
- API settings UI updates: ~50 lines
- **Total new code**: ~200 lines

### Backward Compatibility

✅ **Fully backward compatible**:
- Existing projects work unchanged
- Fallback models available if fetch fails
- Custom prompts still work
- Default prompt available for legacy behavior

---

## Future Enhancements

### Planned for v2.6.0

1. **Smart prompt caching**: Remember which prompts work best for each document type
2. **Bilingual file support**: Full implementation of batch_bilingual_prompt
3. **Model recommendations**: Suggest best model based on document type
4. **Usage statistics**: Track which models/prompts give best results

### Under Consideration

- **A/B testing**: Compare translation quality across prompts
- **Auto-optimization**: Learn from user edits to improve prompts
- **Cloud sync**: Share successful prompt configurations across devices

---

## Conclusion

These features make Supervertaler smarter and more adaptable:

- ✅ Always shows models you can actually use
- ✅ Automatically optimizes prompts for your workflow
- ✅ Maintains flexibility for custom domain-specific needs
- ✅ Reduces errors and improves translation quality

No configuration needed - just refresh your models and start translating!
