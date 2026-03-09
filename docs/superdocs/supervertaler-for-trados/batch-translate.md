# Batch Translate

{% hint style="info" %}
This page is about **Supervertaler for Trados** — the Trados Studio plugin. For batch translation in the standalone desktop app, see [Batch Translation (Desktop)](../ai-translation/batch-translation.md).
{% endhint %}

Batch Translate lets you translate multiple segments at once using AI. It is located in the **Supervertaler Assistant** panel, on the second tab.

## Starting a Batch Translation

1. Open the **Supervertaler Assistant** panel (View > Supervertaler Assistant)
2. Switch to the **Batch Translate** tab
3. Choose a **scope** from the dropdown
4. Choose a **prompt** from the prompt selector
5. Click **Translate**

## Scope

The scope dropdown controls which segments are translated:

| Scope | Description |
|-------|-------------|
| **Empty Segments Only** | Translates segments that have no target text |
| **All Segments** | Translates every segment in the file |
| **Filtered Segments** | Translates only the segments currently visible after applying a filter |
| **Filtered Empty Only** | Translates empty segments within the current filter |

## Prompt Selection

Choose a prompt to guide the AI translation style and domain. The prompt selector shows:

- **Built-in prompts** — 14 prompts covering medical, legal, patent, financial, technical, marketing, IT, style guides, and project prompts
- **Custom prompts** — your own prompts created in the Prompt Manager

{% hint style="info" %}
Domain-specific prompts (e.g., Medical Translation Specialist, Legal Translation Specialist) produce significantly better results for specialized content. Choose the prompt that matches your source material.
{% endhint %}

## Provider and Model

The current AI provider and model are displayed below the prompt selector. To change them, open the settings dialog (gear icon in the TermLens header) and go to the **AI Settings** tab.

## Progress and Logging

During translation:

- A **progress bar** shows overall completion
- A **real-time log** displays the status of each segment as it is translated
- The **Stop** button aborts the batch at any time — segments already translated are kept

## Single-Segment AI Translation

You do not need to open the Batch Translate tab to translate a single segment. Press **Ctrl+Alt+A** to translate just the active segment with AI. The translation is inserted directly into the target cell.

## Tips

### Translate Empty Segments First

Start by translating only the empty segments (scope: **Empty Segments Only**). Review the results, then fix any issues. This avoids overwriting segments you have already edited.

### Use Domain-Specific Prompts

The built-in domain prompts include detailed instructions for medical terminology, legal precision, patent claim structure, and other specialized fields. Selecting the right prompt is the single most effective way to improve translation quality.

### Combine with TM

If your project has a translation memory, TM matches are shown alongside AI translations. You can pre-translate with TM first (using Trados's built-in batch tasks), then use Batch Translate to fill in the remaining empty segments with AI.

### Review After Batch

AI translation is a first draft. After a batch run:

1. Review each translated segment
2. Fix any terminology or style issues
3. Confirm segments with **Ctrl+Enter** (Trados default)

---

## See Also

- [Supervertaler Assistant](ai-assistant.md)
- [TermLens](termlens.md)
- [Keyboard Shortcuts](keyboard-shortcuts.md)
