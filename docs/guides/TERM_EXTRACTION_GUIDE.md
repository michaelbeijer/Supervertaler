# Term Extraction from Dual Selection

## Overview

Supervertaler allows you to extract terminology directly from your translated segments using the **Dual Selection** feature. While translating, you can select a term in both the source and target segments, then add it to your Translation Memory or Glossary with a simple keyboard shortcut.

## How It Works

### Step-by-Step Guide

1. **Translate a segment** containing terminology you want to save
2. **Select the term in the SOURCE segment** (click and drag)
3. **Select the corresponding term in the TARGET segment** (click and drag)
4. **Press a keyboard shortcut**:
   - `Ctrl+G` → Add to Glossary (saved to Project TM for now, glossary support coming soon)
   - `Ctrl+Shift+T` → Add to Translation Memory only

### Visual Feedback

- **Source selection**: Highlighted in **light blue** with dark blue text
- **Target selection**: Highlighted in **light green** with dark green text
- **Confirmation popup**: Shows "✓ Term Added" with the term pair for 2 seconds

## Example Workflow

```
Source segment: "The stabilization rib tapers toward the end"
Target segment: "De stabilisatierib loopt taps toe naar het einde"

1. Select "stabilization rib" in source (highlighted blue)
2. Select "stabilisatierib" in target (highlighted green)
3. Press Ctrl+G
4. ✓ Term added: "stabilization rib → stabilisatierib"
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+G` | Add selected term pair to Glossary (TM for now) |
| `Ctrl+Shift+T` | Add selected term pair to TM only |
| `Tab` | Switch focus between source and target for keyboard selection |
| `Ctrl+Shift+Arrow` | Extend selection by character |
| `Ctrl+Shift+Ctrl+Arrow` | Extend selection by word |
| `Escape` | Clear dual selection |

## Context Menu (Right-Click)

Right-click on the target segment to access:
- **📚 Add Selection to Glossary (Ctrl+G)**
- **💾 Add Selection to TM (Ctrl+Shift+T)**

## Tips & Best Practices

### ✅ Good Term Extraction Practices

- **Extract single terms or short phrases**: "stabilization rib" ✓
- **Extract consistently**: Use the same terminology throughout your project
- **Extract domain-specific terms**: Technical terms, product names, etc.
- **Extract before moving to next segment**: Don't lose your selections!

### ❌ What NOT to Extract

- **Full sentences**: Use regular translation memory for sentences
- **Common words**: "the", "and", "is" don't need glossary entries
- **Inconsistent translations**: Make sure your translation is correct first!

## Future Features (Coming Soon)

When full glossary support is implemented, you'll be able to:

- **Add metadata** to terms (subject, client, project, notes)
- **Add synonyms** and forbidden terms
- **View terms in dedicated Glossary Manager**
- **Auto-recognition** of terms in new segments
- **Export glossaries** as TMX or tab-delimited files
- **Import existing glossaries** from other CAT tools

## Database Storage

Currently, extracted terms are saved to:
- **Project TM** (in SQLite database once implemented)
- **Big Mama TM** (optional, for reuse across projects)

When glossary support is added:
- Terms will be stored in a dedicated `glossary_terms` table
- Link to original TM entry will be maintained
- Full metadata support (subject, client, definition, etc.)

## Troubleshooting

### "No Selection" Warning

**Problem**: You pressed Ctrl+G but got a warning message.

**Solution**: Make sure you have:
1. Selected text in the **source** segment (blue highlight)
2. Selected text in the **target** segment (green highlight)
3. Both selections are in the **same row**

### Selection Disappeared

**Problem**: Your selection cleared when you switched rows.

**Solution**: Dual selections are row-specific. Stay in the same row or re-select.

### Can't Select Text

**Problem**: Text widget won't let you select.

**Solution**: 
- Make sure you're in **Grid View** (Ctrl+1)
- Click once to focus the widget
- Click and drag to select text

## Related Features

- **Translation Memory Search**: Automatic matching of segments
- **Fuzzy Matching**: Find similar translations (coming with database)
- **Big Mama TM**: Universal TM across all projects
- **TMX Export**: Export your TM with embedded glossary terms

---

**Note**: Full glossary functionality will be added in Phase 3 of the database implementation. For now, terms are saved to the Project TM and can be exported as standard TMX files.
