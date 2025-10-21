# Style Guides Feature - Quick Reference Guide

## Overview

The Style Guides feature in Supervertaler allows you to manage professional formatting rules and style guidelines for any task: translation, proofreading, localization, copywriting, and more.

---

## Accessing Style Guides

1. Open Supervertaler v3.7.1+
2. Click the **"📖 Style Guides"** tab in the Assistant Panel (right side)
3. The tab has three sections:
   - **Left Panel:** List of available languages
   - **Middle Panel:** Style guide content editor
   - **Right Panel:** AI Chat assistant

---

## Quick Commands

### Add Rules to All Languages

```
add to all: - Your new formatting rule here
```

**Example:**
```
add to all: - Use en-dashes (–) for numeric ranges, not hyphens (-)
```

**Result:** Rule added to Dutch, English, Spanish, German, and French guides

---

### Add Rules to Specific Language

```
add to [Language]: - Your formatting rule here
```

**Examples:**
```
add to Dutch: - Dutch abbreviations should use periods (bijv. = bijvoorbeeld)
add to German: - Use guillemets (« ») for quotations, not quotes (" ")
add to French: - Always use non-breaking space before punctuation
```

**Result:** Rule added only to specified language

---

### List Available Languages

```
show
```
or
```
list
```
or
```
list languages
```

**Result:** Shows all available languages
- Dutch
- English
- Spanish
- German
- French

---

## Manual Editing

1. Select a language from the left panel
2. Click **Load** button
3. The guide content appears in the middle panel
4. Edit the text directly
5. Click **Save** button to persist changes

---

## Import & Export

### Export Guide to File
1. Select language
2. Click **Load**
3. Click **Export**
4. Choose save location

### Import Guide from File
1. Click **Import**
2. Select Markdown or TXT file
3. Confirm language assignment

---

## AI Assistant

### Ask Questions
Simply type a question in the chat:

```
Suggest numbering format conventions for German technical documents
```

The AI will provide suggestions based on style guide best practices.

### Get Suggestions
```
What are best practices for consistency in translated terminology?
```

### Note
- Requires OpenAI API key configured
- Works offline with command suggestions if no API key

---

## Supported Markdown Formatting

Style guides support standard Markdown:

```markdown
# Section Header

## Subsection

- Bullet point
- Another point
  - Nested point

1. Numbered list
2. Another item

**Bold** and *italic* text

`code` and ```code blocks```

> Quotes and blockquotes
```

---

## Use Cases

### Translation
```
add to all: - Preserve all hyperlinks in target document
add to Dutch: - Don't translate software menu items
add to German: - Use German spelling (ß) not ss
```

### Proofreading
```
add to all: - Check consistency of terminology across sections
add to English: - Use Oxford comma in lists
add to Spanish: - Maintain tú/usted consistency
```

### Localization
```
add to all: - Adapt dates to local format (DD.MM.YYYY)
add to French: - Maintain French legal terminology
add to German: - German TradMark symbol for ®
```

### Copywriting
```
add to all: - Maintain brand voice and tone
add to all: - Use active voice where possible
add to Dutch: - Follow Dutch marketing conventions
```

---

## Tips & Tricks

1. **Organize by Category**: Use headers to organize rules
   ```
   # Terminology
   # Numbers & Formatting
   # Punctuation
   # Brand Guidelines
   ```

2. **Include Examples**: Add examples for clarity
   ```
   - Currency: Use € (EUR) not € (Euro)
     Example: €100,00 not €100.00
   ```

3. **Cross-Reference**: Link related rules
   ```
   - See "Punctuation" section for dash usage
   ```

4. **Version Control**: Include dates for updates
   ```
   - Last updated: 2024-01-15
   - Previous version: 2023-12-01
   ```

---

## Troubleshooting

### "Language not found" error
- Check spelling: Dutch, English, Spanish, German, French
- Copy from the "show" command output

### Changes not saving
- Click **Save** button after edits
- Check that file permissions allow writing to `user data/Translation_Resources/Style_Guides/`

### AI not responding
- Verify OpenAI API key is configured in `api_keys.txt`
- Check internet connection
- Try again - sometimes OpenAI API is slow

### Chat not showing
- Make sure you're in the "📖 Style Guides" tab
- Clear chat history if needed

---

## File Locations

**Style Guides Storage:**
```
user data/Translation_Resources/Style_Guides/
├── Dutch.md
├── English.md
├── Spanish.md
├── German.md
└── French.md
```

**API Configuration:**
```
root/api_keys.txt
```

---

## Keyboard Shortcuts

- **Enter** in chat input: Send message
- **Ctrl+S** in editor: Save (standard save)
- **Tab** in editor: Indent (standard editor behavior)

---

## Getting Help

For each language, there are built-in examples. Check the loaded guides to see:
- Formatting conventions already documented
- Structure and organization
- Best practices by category

---

## Feature Capabilities Summary

| Feature | Status | Notes |
|---------|--------|-------|
| Batch add to all languages | ✅ | Supports all 5 languages |
| Batch add to specific language | ✅ | Language validation |
| Manual editing | ✅ | Full Markdown support |
| Save/Load | ✅ | Auto-persisted to disk |
| Import/Export | ✅ | Markdown or TXT files |
| AI suggestions | ✅ | Requires OpenAI API key |
| Chat history | ✅ | Saved in session |
| Error messages | ✅ | Clear and helpful |
| Offline mode | ✅ | Works with commands only |

---

## Best Practices

1. **Regular Updates**: Review and update guides quarterly
2. **Consistency**: Use same terminology across all languages
3. **Examples**: Include real examples from your projects
4. **Team Collaboration**: Share guides with your team
5. **Version Control**: Note when guides were last updated
6. **Testing**: Use guides during actual translation work to verify they're effective

---

**Version:** 3.7.1+  
**Last Updated:** 2024  
**Status:** Stable & Ready for Production
