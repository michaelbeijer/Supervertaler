# Encoding Repair Tool - User Guide

## What is Text Encoding Corruption?

Text encoding corruption (also called **mojibake**) occurs when text that was originally encoded in one character set (like UTF-8) is incorrectly interpreted as another (like Latin-1 or Windows-1252).

### Common symptoms:
- Mysterious sequences like `\u00e2\u20ac\u201c` appearing in text
- Special characters displaying as garbage or placeholder symbols
- Accented characters becoming double-encoded (e.g., "é" becomes "Ã©")
- Em dashes appearing as `–` or similar patterns
- Curly quotes appearing as escape codes

### How it happens:
Text files get corrupted when they're:
1. Opened in an application using the wrong character encoding
2. Converted between systems with incompatible encoding assumptions
3. Processed by scripts that don't preserve the original encoding
4. Imported/exported from CAT tools without proper encoding handling

---

## Using the Encoding Repair Tool

The Encoding Repair Tool is built directly into Supervertaler and can be accessed from the **Tools** menu.

### Basic Operations

#### 1. **Scan a Single File**
- Click **Select File** and choose your text file
- Click **🔍 Scan File**
- The tool will analyze the file and report any encoding corruption found
- No changes are made - this is a read-only operation

#### 2. **Repair a Single File**
- Click **Select File** and choose your text file
- Click **Scan File** first to see what needs fixing (optional but recommended)
- Click **🔧 Repair File** to fix the corruption
- A backup will be created automatically (`.backup`)
- The file is saved as UTF-8

#### 3. **Scan a Folder**
- Click **Select Folder** and choose your folder
- Click **📂 Scan Folder**
- The tool will recursively scan all text files in the folder
- Results show which files have corruption and how many issues each has

#### 4. **Repair a Folder**
- Click **Select Folder** and choose your folder
- Click **📂 Scan Folder** first (recommended - see what will be fixed)
- Click **🔧 Repair Folder**
- All corrupted files in the folder will be fixed
- Backups are created for all files

---

## Understanding the Results

When corruption is detected, the tool shows:

```
⚠️  ENCODING CORRUPTION DETECTED
Total corruptions: 12

Patterns found:
  1. \u00e2\u20ac\u201c → – (5 occurrences)
  2. \u00e2\u20ac\u0090 → - (2 occurrences)
  3. \u00e2\u20ac\u2122 → ' (1 occurrences)
  ...
```

**What this means:**
- The escape sequence `\u00e2\u20ac\u201c` (UTF-8 for "–" misinterpreted as Latin-1) appears 5 times
- It will be replaced with the correct en dash character "–"
- Similar fixes apply to other detected patterns

---

## Common Patterns and Their Fixes

| Corrupted Pattern | Fixed Character | Meaning |
|---|---|---|
| `\u00e2\u20ac\u201c` | – | En dash |
| `\u00e2\u20ac\u201d` | — | Em dash |
| `\u00e2\u20ac\u0090` | - | Non-breaking hyphen |
| `\u00e2\u20ac\u0153` | " | Left double quote |
| `\u00e2\u20ac\u009d` | " | Right double quote |
| `\u00e2\u20ac\u2122` | ' | Apostrophe/right single quote |
| `\u00e2\u20ac\u00a6` | … | Ellipsis |
| `\u00c2\u00a0` | (space) | Non-breaking space |
| `\u00c2\u00b0` | ° | Degree symbol |

---

## Recovery Options

### If Something Goes Wrong

**Automatic Backup:** Every repair operation creates a `.backup` file in the same directory as the original. For example:

- Original: `glossary.txt`
- Backup: `glossary.txt.backup`

You can manually restore the backup if needed:
```
copy glossary.txt.backup glossary.txt
```

### Manual Recovery

If you need to undo repairs:

1. **Locate the backup file** (look for `.backup` extension)
2. **Delete the repaired file**
3. **Rename the backup** by removing `.backup` from the filename

---

## Technical Details

### What Encodings Does It Fix?

The tool specifically targets UTF-8 content that was misinterpreted as:
- **Latin-1 (ISO-8859-1)**
- **Windows-1252 (CP1252)**

These are the most common source of this type of corruption.

### Supported File Types

- Text files (`.txt`)
- CSV files (`.csv`)
- TSV files (`.tsv`)
- Markdown files (`.md`)
- Any text-based format

### How It Works

1. **Detection:** Scans for known mojibake patterns (corrupted character sequences)
2. **Validation:** Confirms the patterns match common encoding corruption
3. **Repair:** Replaces corrupted sequences with correct Unicode characters
4. **Output:** Saves the file as UTF-8 (the universal standard)

---

## Troubleshooting

### "No corruption detected" but I see garbled text

**Possible causes:**
- The corruption might be a different type than the tool currently handles
- The file might need to be opened with a specific encoding first
- The garbled text might be intentional special formatting

**Solution:** Try manually setting the file encoding in your text editor to UTF-8.

### File size changed significantly after repair

**This is normal!** Corrupted files often contain extra characters from the double-encoding. When fixed, the file becomes smaller.

Example:
- `é` (1 character when correct in UTF-8) 
- Becomes `Ã©` (2 characters when corrupted)
- After repair, it's back to 1 character

### Backup file is very large

Backups are saved in their raw form. They might appear larger than the text representation if the original file had encoding issues.

---

## FAQ

**Q: Will this fix ALL encoding issues?**
A: Not necessarily. It specifically fixes UTF-8→Latin-1 mojibake patterns, which are the most common. Other encoding issues might require different solutions.

**Q: Is it safe to use on important files?**
A: Yes, but always keep backups. The tool creates automatic backups before any repair, so you can always restore the original.

**Q: Can I use this on binary files?**
A: No. The tool is designed for text files only. Using it on binary files (images, PDFs, executables) will cause corruption.

**Q: How do I prevent this in the future?**
A: 
- Always explicitly set file encoding to UTF-8 in your text editor
- Use CAT tools that preserve encoding information
- When importing/exporting, check encoding settings
- Keep consistent encoding across your projects

**Q: Can I repair files in batch (many files at once)?**
A: Yes! Use the "Repair Folder" feature to fix all text files in a directory recursively.

---

## Example Use Case

### Scenario: You received a glossary file with corrupted text

```
❌ BEFORE:
aggregate \u00e2\u20ac\u201c chemical impurities
Poisson\u00e2\u20ac\u2122s ratio

✅ AFTER:
aggregate – chemical impurities  
Poisson's ratio
```

**Steps:**
1. Open Supervertaler → Tools → Encoding Repair
2. Click "Select File" and choose the glossary
3. Click "Scan File" to preview the issues
4. Click "Repair File" to fix it
5. The file is repaired and saved as UTF-8

Done! Your glossary is now properly encoded.

---

## Integration with Your Workflow

### In memoQ:
After repairing files, import them into memoQ as you normally would. The cleaned-up text will import correctly.

### In CafeTran:
Repair your source files before importing. This ensures CafeTran doesn't have to work with corrupted text.

### In Supervertaler:
When importing glossaries or translation resources, run this tool first to ensure clean data.

---

## Need More Help?

- **Report Issues:** [GitHub Issues](https://github.com/michaelbeijer/Supervertaler/issues)
- **Ask Questions:** [GitHub Discussions](https://github.com/michaelbeijer/Supervertaler/discussions)
- **View Source Code:** [Modules on GitHub](https://github.com/michaelbeijer/Supervertaler/tree/main/modules)

