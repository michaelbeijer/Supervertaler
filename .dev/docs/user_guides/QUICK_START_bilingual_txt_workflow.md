# Quick Start Guide - Bilingual TXT Workflow
## Professional CAT Tool Integration for Supervertaler

### 🎯 What is the Bilingual TXT Workflow?

A **simple, reliable translation workflow** compatible with professional CAT tools like memoQ and Trados. Perfect for:
- Large-scale translation projects
- Integration with existing CAT tool workflows
- Projects with partial pre-translations
- Simple source-only files needing translation

---

## 🚀 Quick Start (3 Simple Steps)

### Step 1: Import Your TXT File

**Click**: `📄 Import TXT` button (toolbar)  
**Or**: `File` → `Import Bilingual TXT...`

**Supported Formats**:
- ✅ Single-column (source only)
- ✅ Two-column bilingual (Source, Target)
- ✅ Three-column with IDs (ID, Source, Target)

The program **auto-detects** the format!

---

### Step 2: Translate

**Option A - Translate All Untranslated**:
- Click `Translate All Untranslated` button
- AI translates only empty target cells
- Pre-existing translations are preserved

**Option B - Translate Selected Segments**:
- Select segments in the grid
- Click `Translate Selected` button

**Option C - Manual Translation**:
- Double-click any segment
- Edit the target text
- Press Enter to save

---

### Step 3: Export

**Click**: `File` → `Export to Bilingual TXT...`

**Output Format**: Tab-delimited (ID, Source, Target)
```
1	Hello world	Hallo wereld
2	Welcome	Welkom
3	Thank you	Bedankt
```

**Re-import** into memoQ/Trados or back into Supervertaler!

---

## 📋 File Format Examples

### Format 1: Single-Column Source Only
```
Hello world
Welcome to our application
Thank you for using our service
Please enter your information below
Contact us for more information
```

**Import Result**: 5 untranslated segments ready to translate

---

### Format 2: Two-Column Bilingual (Tab-Delimited)
```
Hello world	Hallo wereld
Welcome to our application	
Thank you	Bedankt
Please enter your information	
Contact us	
```

**Import Result**: 5 segments (2 pre-translated, 3 untranslated)

---

### Format 3: Three-Column with IDs
```
1	Hello world	Hallo wereld
2	Welcome to our application	
3	Thank you	Bedankt
4	Please enter your information	
5	Contact us	
```

**Import Result**: Same as Format 2, but with custom segment IDs

---

### Format 4: CSV (Comma-Delimited)
```
Hello world,Hallo wereld
Welcome to our application,
Thank you,Bedankt
```

**Import Result**: Auto-detected as CSV format

---

## 🎨 Smart Format Detection

### How It Works:

**1. Delimiter Detection**:
- File has tabs → Tab-delimited
- No tabs, but 80%+ lines have commas → CSV
- Otherwise → Single-column (no splitting)

**2. Column Detection**:
- 1 column → Source only
- 2 columns (first is number) → ID + Source
- 2 columns (first is text) → Source + Target
- 3+ columns → ID + Source + Target

**3. Header Detection**:
- Auto-detects and skips header rows
- Looks for: "id", "source", "target", "segment"

**4. Status Assignment**:
- Has target text → "translated" (🟢)
- Empty target → "untranslated" (🔴)

---

## 💡 Common Workflows

### Workflow 1: memoQ Integration
```
1. Export bilingual TXT from memoQ
2. Import into Supervertaler
3. Use AI to translate untranslated segments
4. Review and edit translations
5. Export back to TXT
6. Re-import into memoQ
```

**Benefits**: AI-powered pre-translation + memoQ's powerful features

---

### Workflow 2: Pure Supervertaler
```
1. Create/import single-column source TXT
2. Translate all with AI
3. Review and edit in grid
4. Export to bilingual TXT
5. Archive for translation memory
```

**Benefits**: Simple, fast, no external tools needed

---

### Workflow 3: Partial Pre-Translation
```
1. Import TXT with some translations
2. AI translates only untranslated segments
3. Review both AI and existing translations
4. Export complete bilingual file
```

**Benefits**: Preserves existing work, fills gaps efficiently

---

## 🔧 Advanced Features

### Handling Commas in Source Text

**Problem**: Text like `"Hello, world"` might be split incorrectly.

**Solution**: Smart delimiter detection!
- Single-column files with commas → NOT split
- Only splits if 80%+ lines have commas (true CSV)

**Example**:
```
Hello, world and welcome
This is a test, with commas
Please contact us, thank you
```
✅ Imported as 3 single-column segments (NOT split)

---

### Custom Segment IDs

**Option 1**: Let Supervertaler assign IDs
```
Hello world
Welcome
```
→ IDs: 1, 2, 3...

**Option 2**: Specify your own IDs
```
100	Hello world
200	Welcome
```
→ IDs: 100, 200

**Benefit**: Maintain ID consistency across projects

---

### Header Row Support

**Your file**:
```
ID	Source	Target
1	Hello	Hallo
2	Welcome	Welkom
```

**Auto-detected**: Header row skipped automatically!

---

## 🎯 Best Practices

### ✅ DO:
- Use **tab-delimited** format for maximum compatibility
- Include **segment IDs** for large projects
- **Test round-trip** (import → export → re-import) before production
- **Review AI translations** before finalizing
- **Save projects** regularly during work

### ❌ DON'T:
- Mix tabs and commas in the same file
- Use special characters in segment IDs
- Forget to review AI-generated translations
- Export without verifying segment count

---

## 🐛 Troubleshooting

### Issue: "File imported with wrong column split"

**Cause**: Delimiter auto-detection may have failed

**Solutions**:
1. Ensure tab-delimited files use ACTUAL tabs (not spaces)
2. For CSV, ensure 80%+ lines have commas
3. Check for hidden characters in text editor
4. Try manually adding a tab to first line

---

### Issue: "Segments have wrong status (translated vs untranslated)"

**Cause**: Target column may have whitespace

**Solutions**:
1. Clean up target column (remove spaces from empty cells)
2. Re-import after cleaning
3. Manually mark segments in Supervertaler

---

### Issue: "Some segments missing after import"

**Cause**: Empty lines or header detection

**Check**:
1. Remove blank lines from file
2. Verify header row is correct format
3. Check file encoding (should be UTF-8)

---

## 📊 Format Comparison

| Feature | Single-Column | Two-Column | Three-Column | CSV |
|---------|---------------|------------|--------------|-----|
| Pre-translations | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| Custom IDs | ❌ No | ⚠️ Optional | ✅ Yes | ⚠️ Optional |
| memoQ Compatible | ❌ No | ✅ Yes | ✅ Yes | ⚠️ Maybe |
| Simplicity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Recommended | Starter | Yes | Large Projects | Avoid |

**Recommendation**: Use **two-column tab-delimited** format for best compatibility.

---

## 🎓 Examples

### Example 1: Complete Workflow

**1. Your source file** (`my_project.txt`):
```
Welcome to Supervertaler
This is an AI-powered translation tool
You can translate documents efficiently
Thank you for using our service
```

**2. Import**:
- Click `📄 Import TXT`
- Select `my_project.txt`
- See: "Loaded 4 segments (source-only format)"

**3. Translate**:
- Click `Translate All Untranslated`
- AI processes all 4 segments
- Review translations in grid

**4. Export**:
- `File` → `Export to Bilingual TXT...`
- Save as `my_project_NL.txt`

**5. Result**:
```
1	Welcome to Supervertaler	Welkom bij Supervertaler
2	This is an AI-powered translation tool	Dit is een AI-aangedreven vertaaltool
3	You can translate documents efficiently	U kunt documenten efficiënt vertalen
4	Thank you for using our service	Bedankt voor het gebruik van onze service
```

---

### Example 2: Partial Pre-Translation

**1. Your bilingual file** (`partial.txt`):
```
1	Hello world	Hallo wereld
2	Welcome to our application	
3	You can translate documents	
4	Thank you	Bedankt
5	Contact us for more information	
```

**2. Import**:
- See: "Loaded 5 segments (partially translated bilingual format)"
- "Pre-translated: 2, Untranslated: 3"

**3. Translate Only Untranslated**:
- Click `Translate All Untranslated`
- AI translates segments 2, 3, 5
- Segments 1, 4 unchanged (preserved!)

**4. Export**:
- All 5 segments now have translations
- Pre-existing translations preserved exactly

---

## 🚀 Power Tips

### Tip 1: Batch Processing
Import multiple files sequentially, translate each, export. Supervertaler handles each independently.

### Tip 2: Translation Memory
Export all projects to TXT. Use grep/search to find similar segments across projects for consistency.

### Tip 3: Custom Prompts
Set up domain-specific prompts (legal, medical, etc.) in Settings before batch translation.

### Tip 4: Keyboard Shortcuts
- **Ctrl+T**: Translate selected segment
- **Ctrl+S**: Save project
- **Enter**: Confirm segment edit
- **Escape**: Cancel segment edit

### Tip 5: Quality Assurance
After AI translation, sort by status to review all "Draft" segments systematically.

---

## 📞 Need Help?

**Check Documentation**:
- `FEATURE_bilingual_txt_import_export.md` - Complete technical reference
- `SESSION_SUMMARY_2025-10-06.md` - Implementation details
- `README.md` - General Supervertaler documentation

**Common Questions**:
- Q: Can I use Excel to create TXT files?
- A: Yes! Save as "Tab Delimited Text (.txt)"

- Q: What encoding should I use?
- A: Always UTF-8 for maximum compatibility

- Q: Can I edit TXT files in Notepad?
- A: Yes, but use Notepad++ or VS Code for better handling

---

## ✅ Checklist for Success

Before starting a project:
- [ ] Verify file is UTF-8 encoded
- [ ] Ensure columns are tab-delimited (not spaces)
- [ ] Remove any blank lines
- [ ] Check header row is formatted correctly
- [ ] Test with small sample first

During translation:
- [ ] Review AI-generated translations
- [ ] Check for terminology consistency
- [ ] Verify formatting preservation
- [ ] Save project regularly

Before export:
- [ ] Verify all segments translated
- [ ] Check segment count matches import
- [ ] Review any "Draft" status segments
- [ ] Test round-trip import

---

**Happy Translating! 🎉**
