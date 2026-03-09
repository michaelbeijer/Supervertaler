# Supervertaler Assistant

{% hint style="info" %}
This page is about **Supervertaler for Trados** — the Trados Studio plugin. The standalone desktop app has its own AI translation features — see [AI Translation Overview](../ai-translation/overview.md).
{% endhint %}

The Supervertaler Assistant is a conversational chat panel that runs inside Trados Studio as a separate dockable panel. It is context-aware: it automatically includes your current source and target text, matched terminology, and TM matches in every request, so the AI can give you informed answers about the segment you are working on.

## Opening the Panel

The Supervertaler Assistant lives in its own dockable panel. To open it, go to **View > Supervertaler Assistant**.

You can dock the panel on the right side, bottom, or as a floating window. Trados remembers the panel position between sessions.

## Chat Tab

The Chat tab is the main interface. Type a message in the input field at the bottom and press **Enter** to send.

### What You Can Ask

Because the assistant has access to your current segment context, you can ask things like:

- "Translate this segment"
- "What is the difference between these two translations?"
- "Is this terminology correct in a legal context?"
- "Suggest a more formal alternative"
- "Explain this source text"

The AI will consider your current source text, target text, matched terminology from your termbases, and TM fuzzy matches when responding.

### Sending Messages

| Action | How |
|--------|-----|
| Send a message | Press **Enter** |
| Insert a line break | Press **Shift+Enter** |
| Stop a response in progress | Click the **Stop** button |

## Context Awareness

The assistant automatically includes the following context with every message:

- **Current source segment** text
- **Current target segment** text (if any)
- **Matched terminology** from your active termbases
- **TM fuzzy matches** (if enabled in AI settings)

{% hint style="info" %}
You can control which termbases contribute terms to the AI context and whether TM matches are included. Configure this in the settings dialog on the **AI Settings** tab.
{% endhint %}

## Image Attachments

The Supervertaler Assistant supports multimodal input. You can attach images to your messages for visual context — for example, a screenshot of the source document layout, a reference image, or a table that is hard to describe in text.

| Method | How |
|--------|-----|
| Paste | Press **Ctrl+V** with an image on the clipboard |
| Drag and drop | Drag an image file into the chat input area |
| Browse | Click the **Browse** button to select an image file |

{% hint style="warning" %}
Image limits: up to **5 images** per message, **10 MB** maximum per image. Supported formats: PNG, JPEG, GIF, WebP.
{% endhint %}

## Apply to Target

To use an AI response as your translation:

1. **Right-click** any assistant response bubble
2. Select **Apply to target**
3. The response text is inserted into the active target segment in the Trados editor

This is useful when the assistant suggests a translation and you want to use it directly.

## Provider and Model

The current provider and model are shown in the status area of the chat panel. To change the provider or model, open the settings dialog (gear icon) and switch to the **AI Settings** tab.

### Supported Providers

| Provider | Models |
|----------|--------|
| **OpenAI** | GPT-4o, GPT-4o Mini, GPT-5, o1, o3 |
| **Anthropic** | Claude Sonnet 4.6, Claude Haiku 4.5, Claude Opus 4.6 |
| **Google** | Gemini 2.5 Flash, Gemini 2.5 Pro, Gemini 3 Pro Preview |
| **Ollama** | TranslateGemma, Qwen 3, Aya Expanse (local, no API key needed) |
| **Custom** | Any OpenAI-compatible API endpoint |

{% hint style="info" %}
You only need one provider to get started. If you want privacy or offline use, try [Ollama](../ai-translation/ollama.md) with a local model.
{% endhint %}

---

## See Also

- [Batch Translate](batch-translate.md)
- [Getting Started](getting-started.md)
- [Keyboard Shortcuts](keyboard-shortcuts.md)
