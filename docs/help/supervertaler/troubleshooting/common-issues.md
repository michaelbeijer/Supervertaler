# Common Issues

Solutions to frequently encountered problems.

## Startup Issues

### Application won't start

**Symptoms:** Double-click does nothing, or window briefly appears then closes.

**Solutions:**

1. **Run from command line** to see error messages:
   ```bash
   python Supervertaler.py
   ```

2. **Reset UI preferences** (corrupted window state):
   - Delete `user_data/ui_preferences.json`
   - Restart the application

3. **Check dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Python version** (needs 3.10+):
   ```bash
   python --version
   ```

### "Module not found" error

Install the missing module:
```bash
pip install <module-name>
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

---

## Import Problems

### "Cannot read file" error

- Close the file in other programs (Word, Excel, etc.)
- Check if the file is read-only
- Try copying the file to a different location

### memoQ bilingual shows no segments

- Ensure you exported as **Bilingual DOCX** (table format)
- Check the file in Word to verify it has a source/target table

### Trados package fails to extract

- The SDLPPX might be corrupted
- Re-export from Trados Studio
- Check if the package includes all required files

### Encoding errors (garbled text)

- Try opening the source file in Notepad++ to check encoding
- Use **Tools → Encoding Repair** to fix common issues
- Export from source tool with UTF-8 encoding

---

## Translation Issues

### AI translation returns empty

1. Check your API key is valid
2. Verify you have credits with the provider
3. Check internet connection
4. Try a different model

### "Rate limit exceeded" error

- Wait 1-2 minutes and try again
- Reduce batch size
- Upgrade your API plan

### Wrong translation language

- Check your prompt specifies the correct language pair
- Verify source/target languages are set correctly in project settings

### Tags are removed or moved

Add explicit instructions to your prompt:
```
Keep all formatting tags like {1}, <b>, </b> in exactly 
the same positions in the translation.
```

---

## Reimporting Issues

### Segments don't match on reimport

**Cause:** Segment structure changed.

**Solution:**

- Don’t merge or split segments in Supervertaler.
- Export the matching format for your CAT tool/workflow.
- If you’re working from a bilingual table, don’t modify the table structure in Word.

### Formatting lost on reimport

**Cause:** Tags/placeholders weren’t preserved.

**Solution:**

- Verify tags in Tag view before exporting.
- Ensure tags are balanced and not renumbered.
- Run CAT tool QA after import to catch tag issues early.

### TM matches not appearing

**Cause:** TM not loaded, disabled, or language mismatch.

**Solution:**

- Open **Project resources → Translation Memories**.
- Ensure the TM is added and **Read** is enabled.
- Verify source/target language pair matches your project.

---

## Export Problems

### Exported DOCX has no translations

- Make sure you translated the segments (target column isn't empty)
- Check you're exporting the correct format
- Verify the segments are confirmed

### Trados SDLRPX shows "Draft" status

Update to v1.9.32 or later - this bug was fixed.

### "Source file not found" on export

The original imported file was moved or deleted.
- Use **File → Relocate Source Folder** to point to the new location
- Or re-import the source file

### Formatting lost after round-trip

- Keep all inline tags in your translations
- Don't modify the structure of bilingual tables
- Check CAT tool import settings

---

## Performance Issues

### Application is slow

1. **Reduce segments per page** in pagination settings (try 50)
2. **Disable spellcheck** if not needed (Settings → View)
3. **Close other heavy applications**
4. **Disable Supermemory** if not using it

### Navigation between segments is slow

Fixed in v1.9.66:
- Termbase cache now works correctly
- Verbose logging removed

Update to the latest version.

### Large files take forever to import

- Very large files (10,000+ segments) may take time
- Consider splitting into smaller files
- Use multi-file import for better organization

---

## Spellcheck Issues

### Spellcheck not working

1. Check spellcheck is enabled: **Settings → View Settings → Spellcheck**
2. Verify the correct language is selected
3. For Hunspell, ensure dictionaries are installed

### Wrong language being checked

Go to **Settings → View Settings → Spellcheck** and select the correct target language.

### Red underlines appear everywhere

The spellcheck language might not match your target language. Or you might need to add technical terms to your dictionary.

---

## UI Issues

### Dark mode colors look wrong

Some widgets apply styles when becoming visible. Try:
- Switch themes back and forth
- Restart the application

### Window opens off-screen

Delete `user_data/ui_preferences.json` to reset window position.

### Fonts look different/wrong

Go to **Settings → View Settings** and select your preferred font family.

---

## Still Having Issues?

1. Check the [GitHub Issues](https://github.com/michaelbeijer/Supervertaler/issues) for known bugs
2. Open a new issue with:
   - Your OS and Python version
   - Steps to reproduce the problem
   - Error messages (if any)
   - Screenshots (if helpful)
