# Supervertaler for Trados

Supervertaler for Trados is a plugin for **Trados Studio 2024+** that brings Supervertaler's terminology and AI features directly into the Trados editor. It runs natively inside Trados Studio as a set of dockable panels, so you never have to leave the editor.

## Key Features

### TermLens (Inline Terminology)

Live terminology display that shows the source text word by word, with glossary translations underneath each matched term. Color-coded by termbase type:

- **Blue** for regular termbase matches
- **Pink** for project termbase matches (higher priority)
- **Yellow** for non-translatable terms

Numbered badges let you insert terms with **Alt+1** through **Alt+9**.

### Supervertaler Assistant

A conversational AI chat panel that is aware of your current segment, matched terminology, and TM matches. Ask questions about translation choices, get alternative phrasings, or request explanations — all without leaving Trados.

### Batch Translate

Translate multiple segments at once using AI. Choose a scope (empty segments, all segments, filtered segments), pick a prompt, and let the AI work through your file. Progress is shown in real time.

### Prompt Library

14 built-in domain prompts covering medical, legal, patent, financial, technical, marketing, and IT translation, plus style guides for Dutch, English, French, German, and Spanish. You can also create your own custom prompts.

### Termbase Management

Create, edit, and import termbases in Supervertaler's `.db` format. Quick-add terms with keyboard shortcuts, mark terms as non-translatable, and manage multiple termbases per project.

## System Requirements

| Requirement | Version |
|-------------|---------|
| Trados Studio | 2024 (v18) or later |
| Windows | 10 or 11 |
| .NET Framework | 4.8 |

## Shared Termbase Format

Supervertaler for Trados uses the same SQLite-based termbase format (`.db`) as the standalone [Supervertaler](../README.md) desktop application. Termbases created in either tool are fully compatible — you can open the same `.db` file in both applications.

{% hint style="info" %}
For the SDLPPX round-trip workflow (translating Trados packages in the standalone Supervertaler app), see [Trados Studio Workflow](../cat-tools/trados.md).
{% endhint %}

## Context-Sensitive Help

Press **F1** at any time to open context-sensitive help for the panel or dialog that currently has focus.

## Next Steps

<table data-view="cards">
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Installation</strong></td>
<td><a href="installation.md">Install the plugin →</a></td>
</tr>
<tr>
<td><strong>Getting Started</strong></td>
<td><a href="getting-started.md">Set up termbases and AI →</a></td>
</tr>
<tr>
<td><strong>TermLens</strong></td>
<td><a href="termlens.md">Inline terminology display →</a></td>
</tr>
<tr>
<td><strong>Supervertaler Assistant</strong></td>
<td><a href="ai-assistant.md">Chat with AI in Trados →</a></td>
</tr>
<tr>
<td><strong>Batch Translate</strong></td>
<td><a href="batch-translate.md">Translate segments in bulk →</a></td>
</tr>
<tr>
<td><strong>Keyboard Shortcuts</strong></td>
<td><a href="keyboard-shortcuts.md">All shortcuts at a glance →</a></td>
</tr>
</tbody>
</table>
