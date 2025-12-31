# Quick Start Guide

This guide will get you translating in under 5 minutes.

## Step 1: Start Supervertaler

Launch the application by running `Supervertaler.exe` (Windows) or `python Supervertaler.py` (from source).

## Step 2: Import a Document

1. Go to **File → Import**
2. Choose your file type:
   - **DOCX** - Standard Word documents
   - **Text File** - Plain text (one segment per line)
   - **memoQ Bilingual** - memoQ XLIFF or bilingual DOCX
   - **Trados Package** - SDLPPX files
   - **Phrase Bilingual** - Memsource bilingual DOCX
   - **CafeTran Bilingual** - CafeTran external view

3. Select source and target languages when prompted
4. Your document appears in the translation grid

## Step 3: Navigate the Grid

The translation grid has 4 columns:

| Column | Description |
|--------|-------------|
| **#** | Segment number |
| **Status** | Translation status indicator |
| **Source** | Original text (read-only) |
| **Target** | Your translation (editable) |

### Basic Navigation

| Action | Shortcut |
|--------|----------|
| Next segment | `Enter` or `↓` (at end of cell) |
| Previous segment | `↑` (at start of cell) |
| Go to segment | `Ctrl+G` |

## Step 4: Translate a Segment

### Manual Translation

1. Click in the **Target** cell
2. Type your translation
3. Press `Ctrl+Enter` to confirm

### AI Translation

1. Select a segment
2. Press `Ctrl+T` to translate with AI
3. Review and edit if needed
4. Press `Ctrl+Enter` to confirm

{% hint style="info" %}
**Tip:** Set up your [API keys](api-keys.md) first to use AI translation.
{% endhint %}

## Step 5: Save Your Project

1. Press `Ctrl+S` or go to **File → Save Project**
2. Choose a location and filename
3. Projects are saved as `.svproj` files

## Step 6: Export Your Translation

1. Go to **File → Export**
2. Choose the appropriate format:
   - **DOCX** - Translated Word document
   - **Bilingual Table** - Side-by-side source/target
   - **Return Package** - For CAT tool workflows

---

## What's Next?

<table data-view="cards">
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Set up AI Translation</strong></td>
<td><a href="api-keys.md">Configure API keys →</a></td>
</tr>
<tr>
<td><strong>Learn Keyboard Shortcuts</strong></td>
<td><a href="../editor/keyboard-shortcuts.md">View all shortcuts →</a></td>
</tr>
<tr>
<td><strong>Work with CAT Tools</strong></td>
<td><a href="../cat-tools/overview.md">CAT tool integration →</a></td>
</tr>
</tbody>
</table>
