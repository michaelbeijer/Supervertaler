# TermLens Settings

Configure how TermLens loads and displays terminology in Trados Studio.

## Accessing TermLens settings

Click the **gear icon** in the TermLens panel, or open the plugin **Settings** dialog and switch to the **TermLens** tab.

## Database path

The path to your Supervertaler termbase `.db` file. Click **Browse** to select a database, or **Create New** to start with an empty one.

{% hint style="info" %}
**Auto-detect:** If Supervertaler Workbench is installed on the same machine, the plugin can automatically detect its default database location. Click **Auto-detect** to find and use it.
{% endhint %}

## Termbase toggles

Each Supervertaler termbase in the database has three toggles. See [Termbase Management](../termbase-management.md) for full details.

| Toggle | Purpose |
|--------|---------|
| **Read** | Load terms for matching –only termbases with Read enabled appear in TermLens |
| **Write** | Receive new terms added via the [quick-add shortcuts](../termlens/adding-terms.md) |
| **Project** | Mark as the project termbase (shown in pink, prioritised) |

## MultiTerm termbases

If your Trados project has MultiTerm termbases (`.sdltb` files) attached, they appear at the bottom of the termbase list with a **[MultiTerm]** label and a light green row background. The **Read** toggle controls visibility in TermLens; **Write** and **Project** are always disabled because MultiTerm termbases are read-only.

To add or remove MultiTerm termbases, use Trados Studio's **Project Settings > Language Pairs > Termbases**. See [MultiTerm Support](../multiterm-support.md) for full details.

## Auto-load on startup

When enabled, the plugin automatically loads the termbase database when Trados Studio opens. This means terms are available immediately when you start translating, without needing to open the settings first.

If disabled, the termbase loads the first time you open the TermLens settings or click the TermLens panel.

## Panel font size

Adjust the font size used in the TermLens display panel. Valid range: **7 pt** to **16 pt**.

Increase the font size if TermLens text is hard to read; decrease it to fit more terms on screen.

---

## See Also

- [Termbase Management](../termbase-management.md)
- [MultiTerm Support](../multiterm-support.md)
- [AI Settings](ai-settings.md)
- [TermLens (Workbench)](https://supervertaler.gitbook.io/supervertaler/glossaries/termlens)
