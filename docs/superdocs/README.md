# Supervertaler Help

Welcome to the official help center for **Supervertaler** — professional translation tools built by translators, for translators.

## Two Tools, One Ecosystem

Supervertaler comes in two versions. Choose the one that matches your workflow:

<table data-view="cards">
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Supervertaler (Desktop)</strong></td>
<td>A standalone translation workbench for Windows, macOS, and Linux. Open source and free forever. Works with files from memoQ, Trados, Phrase, and CafeTran.<br><br><a href="get-started/quick-start.md">Get started →</a></td>
</tr>
<tr>
<td><strong>Supervertaler for Trados</strong></td>
<td>A plugin that runs inside Trados Studio 2024+. Adds TermLens inline terminology, an AI assistant, and batch translation — without leaving the Trados editor.<br><br><a href="supervertaler-for-trados/">Get started →</a></td>
</tr>
</tbody>
</table>

{% hint style="info" %}
**Not sure which one you need?** If you use Trados Studio as your primary CAT tool, the plugin gives you terminology and AI features directly inside the editor. If you work with multiple CAT tools or want a standalone translation environment, the desktop app is for you. You can use both — they share the same termbase format.
{% endhint %}

---

## Supervertaler (Desktop)

**Supervertaler** is a free, open-source desktop translation application that integrates AI-powered translation with traditional CAT tool workflows. It runs on Windows, macOS, and Linux.

- 🤖 **Translate with AI** — GPT-4, Claude, Gemini, or local models via Ollama
- 🔗 **Work with CAT tools** — import/export files from memoQ, Trados, Phrase, CafeTran
- 📚 **Translation Memory** — fuzzy matching, TMX import, Supermemory semantic search
- 📖 **Terminology** — glossaries, automatic term highlighting, TermLens
- 🔍 **Superlookup** — system-wide translation lookup (TM, glossary, MT, web)
- ✅ **Quality Assurance** — spellcheck, tag validation, non-translatables

| Requirement | Details |
|-------------|---------|
| **OS** | Windows 10/11, macOS, Linux |
| **Python** | 3.10 or higher |
| **License** | Free and open source (MIT) |
| **Source** | [github.com/michaelbeijer/Supervertaler](https://github.com/michaelbeijer/Supervertaler) |

📖 Start here: [Quick Start Guide](get-started/quick-start.md)

---

## Supervertaler for Trados

**Supervertaler for Trados** is a plugin for **Trados Studio 2024+** that brings Supervertaler's terminology and AI features directly into the Trados editor as dockable panels.

- 🔤 **TermLens** — live inline terminology with color-coded matches and keyboard insertion
- 💬 **Supervertaler Assistant** — context-aware AI chat with access to your segment, TM, and terminology
- ⚡ **Batch Translate** — translate multiple segments at once with domain-specific prompts
- 📋 **Prompt Library** — 14 built-in domain prompts plus custom prompt support

| Requirement | Details |
|-------------|---------|
| **Trados Studio** | 2024 (v18) or later |
| **OS** | Windows 10 or 11 |
| **License** | Paid plugin |
| **Source** | [github.com/michaelbeijer/Supervertaler-for-Trados](https://github.com/michaelbeijer/Supervertaler-for-Trados) |

📖 Start here: [Supervertaler for Trados Overview](supervertaler-for-trados/)

---

## Shared Termbase Format

Both tools use the same SQLite-based termbase format (`.db`). Termbases created in one tool work in the other — you can share terminology between the desktop app and the Trados plugin.

## Getting Help

- 📖 Browse this help center using the sidebar
- 🐛 Report issues on [GitHub](https://github.com/michaelbeijer/Supervertaler/issues)
- 💬 Join [GitHub Discussions](https://github.com/michaelbeijer/Supervertaler/discussions)
- 🌐 Visit [supervertaler.com](https://supervertaler.com)
