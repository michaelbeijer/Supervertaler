# Batch Translation

Translate multiple segments at once with AI.

## Starting Batch Translation

1. **Select segments** to translate:
   - Click first segment, Shift+click last for a range
   - Or use **Edit → Select All** (`Ctrl+A`)
   
2. **Start batch**:
   - Press `Ctrl+Shift+T`
   - Or go to **Edit → Batch Translate**

## Batch Dialog Options

### Provider Selection

Choose your LLM provider:
- OpenAI (GPT-4o, GPT-4-turbo)
- Anthropic (Claude 3.5, Claude 3)
- Google (Gemini Pro)
- Ollama (local models)

### Translation Mode

| Mode | Description |
|------|-------------|
| **LLM Only** | Use AI for all segments |
| **TM First** | Use TM matches above threshold, AI for rest |
| **TM + Context** | Include TM matches as context for AI |

### Options

- **Skip confirmed segments**: Don't re-translate ✅ segments
- **Include context**: Send surrounding segments for better quality
- **Retry until complete**: Auto-retry segments that return empty

## Progress Tracking

During translation:
- Progress bar shows completion
- Per-segment status updates
- Can cancel anytime

## Retry Feature

Enable **"🔄 Retry until all segments are translated"** to:
- Automatically detect empty translations
- Retry failed segments (up to 5 passes)
- Ensure all segments get translated

## Tips

### Optimal Batch Size

- 50-100 segments per batch works well
- Very large batches may timeout
- Split by page if needed

### Quality vs Speed

- GPT-4o: Good balance of speed and quality
- Claude 3 Opus: Highest quality, slower
- GPT-3.5/Gemini: Fastest, lower cost

### Post-Edit Strategy

After batch translation:
1. Review each segment
2. Fix any obvious errors
3. Confirm with `Ctrl+Enter`

---

## See Also

- [AI Translation Overview](overview.md)
- [Creating Prompts](prompts.md)
- [Single Segment Translation](single-segment.md)
