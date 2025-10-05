# Translation Memory - Quick User Guide

## What is Translation Memory?

Translation Memory (TM) automatically remembers your translations and suggests them when you encounter similar text again. This saves time, ensures consistency, and reduces translation costs.

## Key Features

### 🎯 Exact Matches (100%)
When you translate a segment that's identical to something you've translated before, Supervertaler will:
- Show you the previous translation
- Ask if you want to use it
- Insert it immediately if you accept

### 🔍 Fuzzy Matches (75%+)
When similar (but not identical) text is found:
- Shows up to 3 best matches
- Displays similarity percentage (e.g., 85% match)
- Shows both source and target for context
- Lets you decide whether to use AI translation

### 📚 Automatic TM Building
Every time you translate a segment (manually or with AI):
- The translation is automatically added to TM
- No manual work required
- TM grows organically as you work

## How to Use

### Loading an Existing TM File

1. **From TMX File** (industry standard):
   ```
   Translate → Load TM File... → Select .tmx file
   ```

2. **From TXT File** (simple format):
   ```
   Translate → Load TM File... → Select .txt file
   ```
   TXT format: One translation per line, tab-separated:
   ```
   Hello World	Hallo Wereld
   Good morning	Goedemorgen
   ```

### Viewing Your TM

```
Translate → Translation Memory...
```

This opens a window showing:
- Total number of TM entries
- Current fuzzy match threshold (75%)
- Complete list of all source/target pairs

### Exporting Your TM

1. Open TM Manager: `Translate → Translation Memory...`
2. Click **Save TM...**
3. Choose location and filename
4. TM saved as tab-delimited TXT file

You can then:
- Share with other translators
- Use in other CAT tools (after converting to TMX)
- Keep as backup

### Managing TM Entries

**To clear all entries**:
1. `Translate → Translation Memory...`
2. Click **Clear All**
3. Confirm (warning: this cannot be undone!)

**To add more entries**:
- Just keep translating! Each translation is automatically added
- Or load additional TM files (they merge with existing entries)

## Translation Workflow with TM

### Step-by-step:

1. **Select a segment** (click in grid or use Ctrl+Down)

2. **Press Ctrl+T** to translate

3. **TM Check happens automatically**:
   
   **Scenario A - Exact Match Found**:
   ```
   ┌─────────────────────────────────────┐
   │ TM Match Found                      │
   ├─────────────────────────────────────┤
   │ Found exact translation in TM:      │
   │                                     │
   │ Goedemorgen                         │
   │                                     │
   │ Use this translation?               │
   │                                     │
   │        [Yes]        [No]            │
   └─────────────────────────────────────┘
   ```
   - Click **Yes**: Translation inserted instantly (no API cost!)
   - Click **No**: Continues with AI translation

   **Scenario B - Fuzzy Matches Found**:
   ```
   ┌─────────────────────────────────────┐
   │ Fuzzy TM Matches                    │
   ├─────────────────────────────────────┤
   │ Match 1 (92%)                       │
   │   Source: Good morning everyone     │
   │   Target: Goedemorgen allemaal      │
   │                                     │
   │ Match 2 (85%)                       │
   │   Source: Good evening              │
   │   Target: Goedenavond               │
   │                                     │
   │ Continue with AI translation?       │
   │                                     │
   │        [Yes]        [No]            │
   └─────────────────────────────────────┘
   ```
   - Click **Yes**: Uses AI to translate (but you've seen similar examples)
   - Click **No**: Cancel translation

   **Scenario C - No Matches**:
   - Proceeds directly to AI translation
   - No dialog shown

4. **Translation completed and added to TM**
   - Log shows: "✓ Segment #5 translated successfully (added to TM)"
   - Now available for future matches!

## Project Integration

### TM in Projects

When you save a project (Ctrl+S), your TM is automatically included:
- All source/target pairs saved
- Fuzzy match threshold saved
- Next time you open project, TM is restored

This means:
- ✅ TM persists across sessions
- ✅ No need to reload TM files each time
- ✅ Project is self-contained

### Sharing Projects with TM

When you send a project file (.json) to another translator:
- They receive your complete TM
- Can continue building on your work
- Maintains translation consistency

## Tips & Best Practices

### 📌 Tip 1: Start with an Existing TM
If you have previous translations:
- Export them to TXT format (source<TAB>target per line)
- Load at project start: `Translate → Load TM File...`
- Instant suggestions from the beginning!

### 📌 Tip 2: Use TM for Repetitive Content
TM shines with:
- User interface strings (buttons, labels)
- Legal/contract boilerplate
- Product descriptions with variations
- Technical documentation

### 📌 Tip 3: Don't Worry About Exact Duplicates
If you load a TM file that has overlapping entries:
- Newer entries overwrite older ones (latest wins)
- No duplicate storage
- TM stays efficient

### 📌 Tip 4: Export Regularly
Save your TM periodically:
1. `Translate → Translation Memory...`
2. `Save TM...`
3. Keep in backup folder

This gives you:
- Backup if project file corrupted
- Standalone TM for other projects
- Archive of your translation work

### 📌 Tip 5: Review Fuzzy Matches Carefully
A 75% match doesn't mean 75% correct!
- High match (90%+): Usually safe to use AI with confidence
- Medium match (75-85%): Review carefully, might need editing
- Always verify numbers, names, and technical terms

## Troubleshooting

### "No TM matches found" but I know I translated this before

**Possible causes**:
1. **Different punctuation**: "Hello." vs "Hello" are different
2. **Extra spaces**: "Hello  world" vs "Hello world"
3. **Different tags**: `<b>Hello</b>` vs `Hello`

**Solution**: TM matches exact text. Minor variations count as fuzzy matches.

### TMX file won't load

**Check**:
1. Language codes match: English=en, Dutch=nl, German=de, etc.
2. File is valid XML (open in text editor to verify)
3. TMX version supported (1.4 and 2.0 work best)

**Try**:
- Export TMX to TXT from original CAT tool
- Load TXT instead (simpler format)

### TM entries not showing up

**Verify**:
1. Check TM count: `Translate → Translation Memory...`
2. Check threshold: Default 75% (shown in TM Manager)
3. Try exact match first: Translate identical segment

### Clear TM doesn't clear

After clicking "Clear All":
- TM manager dialog doesn't auto-refresh
- Close and reopen to see change
- Or check entry count at top

## Advanced: Creating TM Files

### Creating TXT TM Files

Use Excel/LibreOffice:
1. Column A: Source text
2. Column B: Target text
3. Save As → Text (Tab delimited) (.txt)
4. Encoding: UTF-8

Or use a text editor:
```
Source text here<TAB>Target text here
Another source<TAB>Another target
```
(Replace `<TAB>` with actual Tab key press)

### Converting TM Formats

**From TMX to TXT**:
1. Load TMX: `Translate → Load TM File...`
2. Save TXT: `Translate → Translation Memory... → Save TM...`

**From TXT to TMX**:
- Not currently supported in Supervertaler
- Use external tools like Okapi Rainbow or OmegaT

## Summary

✅ **Automatic**: TM works in the background, no manual management needed
✅ **Intelligent**: Finds both exact and fuzzy matches
✅ **Integrated**: Part of your project, saves/loads automatically  
✅ **Compatible**: Supports industry-standard TMX and simple TXT formats
✅ **Cost-saving**: Exact matches = no API calls = free translations!

**Key Shortcut**: `Ctrl+T` to translate (TM check happens automatically)

---

**Need More Help?**
- See main Supervertaler User Guide for complete feature documentation
- Check TRANSLATION_MEMORY_IMPLEMENTATION.md for technical details
