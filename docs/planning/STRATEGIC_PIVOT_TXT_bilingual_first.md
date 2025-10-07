# TXT Bilingual Translation Implementation Plan

**Date**: October 6, 2025  
**Priority**: HIGH  
**Rationale**: Simpler, more reliable than DOCX workflow

---

## Why TXT Bilingual First?

### Advantages Over DOCX
1. **No formatting complexity** - Plain text only
2. **Clear segment boundaries** - Numbered segments
3. **Industry standard** - memoQ, Trados, etc. all support this
4. **Easy validation** - Simple to verify correctness
5. **No alignment issues** - Segments are explicitly numbered
6. **Proven workflow** - Already used by professional translators

### memoQ Bilingual TXT Format

**Standard Format:**
```
1	Source text for first segment	Target text for first segment
2	Source text for second segment	Target text for second segment
3	Another source segment	Another target segment
```

**Features:**
- Tab-delimited columns
- Segment number, source, target
- One segment per line
- UTF-8 encoding
- Optional header row

**Alternative Format (TSV with status):**
```
ID	Source	Target	Status
1	Hello world	Hallo wereld	Translated
2	Second segment		Untranslated
3	Third segment	Derde segment	Translated
```

---

## Implementation Tasks

### Phase 1: Import TXT Bilingual Files ✅ (Already Done!)

**Current Status**: We already have TSV import in the codebase!

Check existing code:
- `import_tsv()` method
- `export_tsv()` method

**What we have:**
```python
def import_tsv(self):
    """Import TSV file (segment ID, source, target)"""
    # Already implemented!
```

**Test this:**
1. Export current project to TSV
2. Open in Excel/text editor
3. Verify format
4. Re-import
5. Check if it works

---

### Phase 2: Batch Translation for TXT Files

**Goal**: Translate all untranslated segments in a bilingual file

**Features Needed:**
1. ✅ Import TXT/TSV bilingual file
2. ✅ Show segments in grid
3. ✅ Batch translate untranslated segments
4. ✅ Export back to TXT/TSV

**Already Implemented:**
- ✅ TSV import/export
- ✅ Batch translation (`translate_all_untranslated`)
- ✅ Grid view with status
- ✅ Context-aware prompts (batch_bilingual_prompt ready!)

**What's Missing:**
- ⏳ Better memoQ TXT format support (tab-delimited)
- ⏳ Format detection (TSV vs TXT)
- ⏳ Preserve original file format on export

---

### Phase 3: Enhanced Bilingual Features

**Nice-to-Have Features:**

1. **Format Variants:**
   - Standard tab-delimited (num, source, target)
   - TSV with headers
   - CSV support
   - memoQ-specific formats

2. **Validation:**
   - Check segment count matches
   - Verify no missing translations
   - Flag mismatched segment numbers

3. **Metadata Preservation:**
   - Keep header rows
   - Preserve segment IDs
   - Maintain status flags

4. **Export Options:**
   - Export all segments
   - Export only translated
   - Export only changed segments
   - Maintain original format

---

## Quick Implementation Guide

### Step 1: Test Current TSV Functionality

**Try this NOW:**
1. Open Supervertaler
2. Import a DOCX (if you want)
3. File → Export → Export to TSV
4. Open the TSV in text editor
5. Close Supervertaler
6. Reopen Supervertaler  
7. File → Import TSV
8. Verify segments loaded correctly

**If this works**, you already have 90% of what you need!

---

### Step 2: Add memoQ TXT Import

**Simple implementation** (if TSV doesn't already work):

```python
def import_memoq_txt(self):
    """Import memoQ bilingual TXT file"""
    file_path = filedialog.askopenfilename(
        title="Select memoQ TXT file",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if not file_path:
        return
    
    try:
        self.segments = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                # Tab-delimited: ID, Source, Target
                parts = line.split('\t')
                
                if len(parts) < 2:
                    continue  # Skip malformed lines
                
                seg_id = int(parts[0]) if parts[0].isdigit() else line_num
                source = parts[1]
                target = parts[2] if len(parts) > 2 else ""
                
                segment = Segment(seg_id, source)
                segment.target = target
                segment.status = "translated" if target else "untranslated"
                self.segments.append(segment)
        
        self.load_segments_to_grid()
        self.log(f"✓ Loaded {len(self.segments)} segments from TXT")
        
    except Exception as e:
        messagebox.showerror("Import Error", f"Failed to import TXT: {e}")
```

---

### Step 3: Add memoQ TXT Export

```python
def export_memoq_txt(self):
    """Export to memoQ bilingual TXT file"""
    file_path = filedialog.asksaveasfilename(
        title="Save as memoQ TXT",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if not file_path:
        return
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for seg in self.segments:
                # Tab-delimited: ID, Source, Target
                f.write(f"{seg.id}\t{seg.source}\t{seg.target}\n")
        
        self.log(f"✓ Exported {len(self.segments)} segments to TXT")
        messagebox.showinfo("Success", f"Exported to:\n{file_path}")
        
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export TXT: {e}")
```

---

## Recommended Workflow

### For Professional Translators

**Step 1: Prepare in memoQ/Trados**
1. Import source document into memoQ
2. Pre-translate with TM
3. Export bilingual TXT (source + target columns)
4. Note: Untranslated segments have empty target column

**Step 2: AI Translation in Supervertaler**
1. Import bilingual TXT
2. Review pre-translated segments (from TM)
3. Use "Translate All Untranslated" for remaining segments
4. Review and edit AI translations
5. Export back to TXT

**Step 3: Finalize in memoQ**
1. Import updated bilingual TXT
2. Review translations
3. Export final deliverable (DOCX, PDF, etc.)
4. Update TM with confirmed translations

**Benefits:**
- ✅ memoQ handles all formatting
- ✅ Supervertaler focuses on translation quality
- ✅ Clear separation of concerns
- ✅ Reliable workflow
- ✅ No formatting corruption

---

## Testing Checklist

### Test Case 1: Basic TXT Import/Export
- [ ] Create simple TXT with 3 segments
- [ ] Import into Supervertaler
- [ ] Verify segments appear correctly
- [ ] Export back to TXT
- [ ] Verify format matches original

### Test Case 2: Translation Workflow
- [ ] Import TXT with 10 segments
- [ ] Leave some with target text (pre-translated)
- [ ] Leave some without target (untranslated)
- [ ] Run "Translate All Untranslated"
- [ ] Verify only untranslated segments are translated
- [ ] Export and verify format

### Test Case 3: memoQ Format
- [ ] Export bilingual file from memoQ
- [ ] Import into Supervertaler
- [ ] Translate
- [ ] Export
- [ ] Re-import into memoQ
- [ ] Verify no data loss

---

## Current Implementation Status

### Already Working ✅
1. ✅ TSV import/export (File menu)
2. ✅ Grid view with source/target
3. ✅ Batch translation
4. ✅ Status tracking
5. ✅ Translation memory
6. ✅ Context-aware prompts (batch_bilingual_prompt ready!)

### Quick Wins (Easy to Add) ⚡
1. ⚡ memoQ TXT format support (~50 lines)
2. ⚡ Format auto-detection (~20 lines)
3. ⚡ Better export options (~30 lines)

### Future Enhancements 🔮
1. 🔮 Multiple format support
2. 🔮 Validation and error checking
3. 🔮 Metadata preservation
4. 🔮 Diff view (show changes)

---

## Why This Is Smart

### Technical Benefits
- **Simple parsing**: Split on tabs/commas
- **Clear structure**: No ambiguity
- **Easy validation**: Check line count
- **No dependencies**: Works with any CAT tool

### Workflow Benefits
- **Proven process**: Industry standard
- **Tool integration**: Works with existing CAT tools
- **Quality control**: Multiple review stages
- **TM leverage**: Pre-translate with existing TM

### Business Benefits
- **Faster development**: Less complexity
- **Higher reliability**: Fewer edge cases
- **Better UX**: Predictable behavior
- **Professional workflow**: Matches translator expectations

---

## Next Session Plan

### Immediate Tasks (30 minutes)
1. Test current TSV import/export
2. Verify it works with bilingual files
3. Document any issues

### If TSV Works
1. Add menu item: "Import Bilingual TXT"
2. Add menu item: "Export Bilingual TXT"
3. Test with sample files
4. Done! ✅

### If TSV Needs Work
1. Review current TSV implementation
2. Fix any format issues
3. Add tab-delimited support
4. Test thoroughly

---

## Long-Term Vision

### Phase 1: TXT Bilingual (Priority 1) 🎯
- Get rock-solid TXT import/export
- Integrate with translation workflow
- Support memoQ/Trados formats
- Professional translator feedback

### Phase 2: DOCX Polish (Priority 2)
- Return to DOCX with lessons learned
- Focus on simple formatting only
- Use TXT experience to improve reliability
- Add comprehensive testing

### Phase 3: Advanced Features (Priority 3)
- XLIFF support
- TMX import/export (already have export!)
- Bilingual DOCX
- Custom format plugins

---

## Conclusion

**Excellent call to pivot to TXT bilingual!** This will:
1. ✅ Get you a working professional workflow faster
2. ✅ Build confidence with simpler format
3. ✅ Learn what features translators actually need
4. ✅ Provide foundation for DOCX improvements later

**Good news**: You probably already have 90% of this working via the TSV functionality!

**Tomorrow's goal**: Test TSV, confirm it works, add memoQ TXT variant if needed. Should be quick!

Have a great evening! 🌙
