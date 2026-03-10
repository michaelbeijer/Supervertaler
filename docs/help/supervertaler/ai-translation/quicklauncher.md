# QuickLauncher

The **Supervertaler QuickLauncher** is a floating AI action menu that gives you instant access to translation tools, the Supervertaler Assistant, and your custom prompts — without leaving your current workflow.

## Opening QuickLauncher

There are several ways to open the QuickLauncher:

### Inside Supervertaler

| Method | How |
|--------|-----|
| **Right-click** a source or target cell | Select text → right-click → **⚡ QuickLauncher** |
| **Alt+K** keyboard shortcut | Place your cursor in a cell → press `Alt+K` |

The selected text in the cell is automatically used as input.

### From any external application

| Method | How |
|--------|-----|
| **Ctrl+Alt+K** global hotkey | Select text in any app (Word, memoQ, Trados, browser, etc.) → press `Ctrl+Alt+K` |

{% hint style="info" %}
The global hotkey requires AutoHotkey to be installed. Supervertaler captures the selected text from your clipboard and opens the QuickLauncher.
{% endhint %}

## Menu Items

When you open the QuickLauncher, you see a popup menu with the following items:

### QuickTrans

**⚡ QuickTrans** opens a compact popup window that instantly translates the selected text using your configured AI provider.

- Press `Ctrl+M` to open QuickTrans directly (without the menu)
- The translation appears in a floating popup
- Useful for quick lookups while working in the grid

See also: [Single Segment Translation](single-segment.md)

### Supervertaler Assistant

**💬 Supervertaler Assistant** opens a conversational AI chat inside the AI tab. Unlike one-shot translations, you can have a back-and-forth conversation:

- Ask follow-up questions ("Can you rephrase this more formally?")
- Get explanations ("What does this legal term mean?")
- Iterate on translations ("Now adapt it for patents")

The selected text is automatically inserted as your first message.

{% hint style="tip" %}
When launched from an external app via `Ctrl+Alt+K`, press **Escape** in the Assistant to return focus to the app you were working in.
{% endhint %}

### Custom Prompts

Below the built-in items, you'll see any prompts you've added to the QuickLauncher from the [Prompt Manager](prompt-library.md).

Each prompt offers two actions:

| Action | What it does |
|--------|-------------|
| **▶ Run (show response)…** | Runs the prompt and shows the result in a dialog |
| **↺ Run and replace target selection** | Runs the prompt and replaces the selected text with the result |

When using the QuickLauncher from an external app (`Ctrl+Alt+K`), the second action becomes **↺ Run and paste into app** — the result is copied to your clipboard and pasted back into the external application.

## Adding Prompts to QuickLauncher

1. Go to the **✨ AI** tab → **📋 Prompt Manager**
2. Create or select a prompt
3. Enable the **Show in QuickLauncher** option for that prompt

Your prompt will then appear in the QuickLauncher menu every time you open it.

## Context and Variables

When a prompt runs from the QuickLauncher, it has access to the following context variables:

| Variable | Description |
|----------|-------------|
| `{source_text}` | The selected / captured text |
| `{target_text}` | The current segment's target text (in-grid only) |
| `{source_lang}` | Project source language |
| `{target_lang}` | Project target language |

This means your prompts can be language-aware and context-sensitive. For example, a prompt like *"Explain {source_text} in simple {target_lang}"* will automatically use the correct languages.

See [Creating Prompts](prompts.md) and [Prompt Manager](prompt-library.md) for more on writing and managing prompts.

## Customizing Hotkeys

You can change the default keyboard shortcuts for the QuickLauncher and QuickTrans in **Settings → Keyboard Shortcuts**.

| Default shortcut | Action |
|------------------|--------|
| `Alt+K` | Open QuickLauncher (in-app) |
| `Ctrl+Alt+K` | Open QuickLauncher (global, from any app) |
| `Ctrl+M` | QuickTrans (direct, skip menu) |

## Tips

- **Start with QuickTrans** if you just need a quick translation — it's the fastest path.
- **Use the Supervertaler Assistant** when you need to discuss or iterate on a translation.
- **Create custom prompts** for repetitive tasks (e.g., "Simplify this", "Make formal", "Extract terminology").
- The QuickLauncher works without a project open — useful for general-purpose AI lookups.

---

## See Also

- [Single Segment Translation](single-segment.md)
- [Creating Prompts](prompts.md)
- [Prompt Manager](prompt-library.md)
- [Keyboard Shortcuts](../editor/keyboard-shortcuts.md)
