# Bilingual File Import - Analysis & Implementation Plan

**Date**: October 7, 2025  
**Feature**: Direct CAT Tool Bilingual Import  
**Status**: 📋 Planning Phase  
**Priority**: HIGH - Game-changing feature

---

## Executive Summary

Currently, Supervertaler requires users to manually copy the source column from bilingual exports into a TXT file. This feature will enable **direct import** of bilingual files from major CAT tools, eliminating manual steps and preserving all metadata.

**Current Workflow** (Manual):
```
CAT Tool → Export bilingual → User copies source to TXT → Import to Supervertaler
```

**Proposed Workflow** (Automated):
```
CAT Tool → Export bilingual → Import to Supervertaler (one click!)
```

---

## memoQ Bilingual Format Analysis

### File Structure

**Analyzed File**: `projects/memoQ bilingual.docx`

**Format**: Microsoft Word DOCX with single table

**Table Structure**:
- **Row 0**: Header with project metadata (merged cells)
  - Project name: "Test document (with formatting, styles and a table).docx"
  - Warning: "Important! Don't change segment ID or source text."
  - Version: "V12.0.10"
  - Project GUID: "9b98c768-c257-47d1-adce-7b19e2aa0789"

- **Row 1**: Column headers
  - Column 0: `ID`
  - Column 1: `Dutch (Netherlands)` (source language)
  - Column 2: `English (United Kingdom)` (target language)
  - Column 3: `Comment`
  - Column 4: `Status`

- **Rows 2+**: Segment data (27 segments in example)

**Column Details**:

| Col | Name | Content | Example |
|-----|------|---------|---------|
| 0 | ID | Segment number + GUID | `1\n5aa117a5-8634-46ae-8b76-f8d035c6ba47` |
| 1 | Source | Source text (Dutch) | `Biagio Pagano` |
| 2 | Target | Target text (English) | *(empty if untranslated)* |
| 3 | Comment | Translator comments | *(usually empty)* |
| 4 | Status | Translation status | `Not started` / `Confirmed` / etc. |

### Key Observations

1. **Segment ID Format**: Two-line format
   - Line 1: Sequential number (1, 2, 3...)
   - Line 2: UUID (unique identifier)

2. **Status Values** (observed):
   - `Not started` - No translation yet
   - *(Other statuses: TBD from more examples)*

3. **Empty Target Cells**: Represent untranslated segments

4. **No Tags**: This example doesn't contain formatting tags
   - Need additional example with tags to analyze tag formatting

5. **Metadata Preservation**: Critical fields
   - ✅ Segment IDs (number + GUID)
   - ✅ Source language name
   - ✅ Target language name
   - ✅ Status field
   - ⚠️ Comments (preserve if present)

---

## Implementation Strategy

### Phase 1: memoQ Bilingual Import (Week 1)

**Goal**: Import memoQ bilingual DOCX, extract source segments

**Features**:
1. **Format Detection**
   - Detect memoQ bilingual format by:
     - Single table with 5 columns
     - Header row with "ID", language names, "Comment", "Status"
     - Metadata header with "Important! Don't change segment ID"

2. **Segment Extraction**
   ```python
   def parse_memoq_bilingual(docx_path):
       """Parse memoQ bilingual DOCX and extract segments"""
       doc = Document(docx_path)
       table = doc.tables[0]
       
       # Extract metadata from row 0
       project_name = extract_project_name(table.rows[0])
       
       # Extract column headers from row 1
       source_lang = table.rows[1].cells[1].text.strip()
       target_lang = table.rows[1].cells[2].text.strip()
       
       # Extract segments from rows 2+
       segments = []
       for row in table.rows[2:]:
           seg_id = row.cells[0].text.strip()  # Number + GUID
           source = row.cells[1].text.strip()
           target = row.cells[2].text.strip()
           comment = row.cells[3].text.strip()
           status = row.cells[4].text.strip()
           
           segments.append({
               'id': seg_id,
               'source': source,
               'target': target,
               'comment': comment,
               'status': status
           })
       
       return {
           'format': 'memoq_bilingual',
           'project_name': project_name,
           'source_lang': source_lang,
           'target_lang': target_lang,
           'segments': segments
       }
   ```

3. **Integration with Existing Import**
   - Add "Import Bilingual DOCX" button
   - Auto-detect memoQ format
   - Extract source column → load as current TXT workflow
   - Preserve metadata for export

4. **UI Changes**
   ```
   Import Options:
   ┌─────────────────────────────┐
   │ ○ Import TXT (source only)  │  ← Current
   │ ● Import Bilingual DOCX     │  ← NEW
   │   (memoQ/Trados/Wordfast)   │
   └─────────────────────────────┘
   ```

### Phase 2: Bilingual Export (Week 2)

**Goal**: Export translations back to bilingual DOCX

**Features**:
1. **Preserve Original Structure**
   - Maintain exact table format
   - Preserve metadata header
   - Keep segment IDs unchanged
   - Update target column only

2. **Update Status Field**
   - "Not started" → "Confirmed" (or appropriate status)
   - User-configurable status mapping

3. **Export Function**
   ```python
   def export_memoq_bilingual(original_docx, translations, output_path):
       """Export translations to memoQ bilingual format"""
       doc = Document(original_docx)
       table = doc.tables[0]
       
       # Update target column (column 2) for each segment
       for i, translation in enumerate(translations, start=2):
           table.rows[i].cells[2].text = translation['target']
           table.rows[i].cells[4].text = 'Confirmed'  # Update status
       
       doc.save(output_path)
   ```

4. **Validation**
   - Ensure all segment IDs match
   - Verify no source text changed
   - Check tag preservation

### Phase 3: Tag Formatting Support (Week 3)

**Goal**: Properly format memoQ tags for reimport

**Requirements** (need example with tags):
- Font color for tags
- Character style
- Tag structure preservation
- Paired tag validation

**Analysis Needed**:
- [ ] Get memoQ bilingual file WITH tags
- [ ] Examine XML structure of tagged cells
- [ ] Identify formatting properties
- [ ] Test reimport requirements

### Phase 4: Multi-Format Support (Week 4+)

**Trados Studio** (DOCX review format):
- Different table structure (TBD - need example)
- XML-style tags `<410>...</410>`
- Specific tag formatting requirements
- Character styles and colors

**CafeTran** (TXT/TMX):
- Text-based formats
- Simpler parsing
- Tag format: `|1|...|2|`

**Wordfast** (DOCX/TXLF):
- Similar to Trados
- TBD - need examples

---

## Data Structures

### Enhanced Segment Object

```python
class BilingualSegment:
    """Enhanced segment with bilingual metadata"""
    def __init__(self, seg_id, source, target='', comment='', status='Not started',
                 guid=None, source_lang=None, target_lang=None):
        self.seg_id = seg_id         # Sequential number
        self.guid = guid             # UUID from memoQ
        self.source = source         # Source text
        self.target = target         # Target text (empty if untranslated)
        self.comment = comment       # Translator comment
        self.status = status         # Translation status
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        # For round-trip preservation
        self.original_format = None  # 'memoq', 'trados', etc.
        self.metadata = {}           # Additional format-specific data
```

### Project Metadata

```python
class BilingualProject:
    """Bilingual project with full metadata"""
    def __init__(self):
        self.format = None           # 'memoq_bilingual', 'trados_review', etc.
        self.project_name = None
        self.version = None
        self.project_guid = None
        self.source_lang = None
        self.target_lang = None
        self.segments = []           # List of BilingualSegment
        self.original_file = None    # Path to original bilingual file
```

---

## UI/UX Design

### Import Dialog

```
┌───────────────────────────────────────────┐
│  Import Document                          │
├───────────────────────────────────────────┤
│                                           │
│  Select Import Type:                      │
│  ○ Source Text Only (TXT)                 │
│  ● Bilingual Document (DOCX/TMX)          │
│                                           │
│  File: [Browse...] memoQ bilingual.docx   │
│                                           │
│  ┌─── Detected Format ────────────────┐  │
│  │ ✓ memoQ Bilingual Export            │  │
│  │   Version: 12.0.10                  │  │
│  │   Source: Dutch (Netherlands)       │  │
│  │   Target: English (United Kingdom)  │  │
│  │   Segments: 27                      │  │
│  │   Status: 0 translated, 27 pending  │  │
│  └─────────────────────────────────────┘  │
│                                           │
│  Import Options:                          │
│  ☑ Preserve original file for export     │
│  ☑ Auto-detect language pair             │
│  ☐ Import existing translations          │
│                                           │
│         [Cancel]  [Import]                │
└───────────────────────────────────────────┘
```

### Export Dialog

```
┌───────────────────────────────────────────┐
│  Export Bilingual Document                │
├───────────────────────────────────────────┤
│                                           │
│  Export Format:                           │
│  ● memoQ Bilingual (reimportable)         │
│  ○ Trados Review (if implemented)         │
│  ○ Generic DOCX Table                     │
│                                           │
│  Update Status To:                        │
│  ○ Confirmed                              │
│  ○ Reviewed                               │
│  ● Custom: [Translated]                   │
│                                           │
│  Validation:                              │
│  ✓ All segment IDs preserved              │
│  ✓ Source text unchanged                  │
│  ✓ 27/27 segments translated              │
│  ⚠ 3 segments contain tags - verify       │
│                                           │
│  Save As: [Browse...] output_bilingual.docx│
│                                           │
│         [Cancel]  [Export]                │
└───────────────────────────────────────────┘
```

---

## Testing Strategy

### Test Cases

**TC1: Import memoQ Bilingual**
- [x] Load `memoQ bilingual.docx`
- [ ] Verify 27 segments extracted
- [ ] Check source language detected: Dutch
- [ ] Check target language detected: English
- [ ] Verify segment IDs preserved
- [ ] Confirm GUIDs extracted

**TC2: Translate and Export**
- [ ] Import memoQ bilingual
- [ ] Translate all 27 segments
- [ ] Export to new bilingual DOCX
- [ ] Verify target column populated
- [ ] Check status updated
- [ ] Validate segment IDs unchanged

**TC3: Reimport to memoQ**
- [ ] Export bilingual DOCX from Supervertaler
- [ ] Import into memoQ project
- [ ] Verify all translations accepted
- [ ] Check no validation errors
- [ ] Confirm formatting preserved

**TC4: Tag Preservation** (pending tag examples)
- [ ] Import bilingual with memoQ tags
- [ ] Translate maintaining tags
- [ ] Export with tags
- [ ] Verify tag formatting correct
- [ ] Test reimport success

---

## Dependencies

### Current
- ✅ `python-docx` (already installed)
- ✅ DOCX parsing capabilities (already implemented)

### Additional (for future formats)
- ⏳ `lxml` (for XLIFF parsing)
- ⏳ TMX parser library (or custom implementation)

---

## Benefits

### For Users
- ✅ **Eliminate manual copying** - no more copy-paste from bilingual exports
- ✅ **Preserve metadata** - segment IDs, comments, status all maintained
- ✅ **Professional workflow** - seamless integration with CAT tools
- ✅ **Faster setup** - one-click import instead of multiple steps
- ✅ **Reimport capability** - export directly back to CAT tool
- ✅ **Error reduction** - automated extraction prevents copy-paste mistakes

### For Development
- ✅ **Competitive advantage** - unique feature in translation tools
- ✅ **Professional credibility** - proper CAT tool integration
- ✅ **User feedback** - easier testing with real projects
- ✅ **Future-proof** - foundation for more CAT formats

---

## Risks & Mitigation

### Risks

1. **Format Variations**
   - Risk: Different memoQ versions may have slightly different formats
   - Mitigation: Make parser flexible, test with multiple memoQ versions

2. **Tag Formatting**
   - Risk: Tag styling requirements unknown without examples
   - Mitigation: Request example files with tags from user

3. **Reimport Failures**
   - Risk: Exported file rejected by CAT tool
   - Mitigation: Rigorous validation, preserve original file structure exactly

4. **Large Files**
   - Risk: Performance issues with thousands of segments
   - Mitigation: Implement progress bar, optimize table parsing

### Mitigation Strategy

- Start with memoQ (most commonly requested)
- Get comprehensive examples (with and without tags)
- Test reimport thoroughly before release
- Provide clear documentation and validation

---

## Next Steps

### Immediate (This Week)

1. **Get Additional Examples**
   - [ ] memoQ bilingual WITH formatting tags
   - [ ] Trados Studio review DOCX
   - [ ] CafeTran bilingual export
   - [ ] Wordfast TXLF/DOCX

2. **Prototype Import Function**
   - [ ] Implement `parse_memoq_bilingual()`
   - [ ] Add "Import Bilingual" button to UI
   - [ ] Test with provided example file
   - [ ] Validate segment extraction

3. **Design Full Workflow**
   - [ ] Create detailed UI mockups
   - [ ] Plan data structure modifications
   - [ ] Document export requirements

### Short Term (Next 2 Weeks)

1. **Implement memoQ Import/Export**
   - [ ] Full bilingual import
   - [ ] Translation workflow
   - [ ] Bilingual export
   - [ ] Reimport testing

2. **Tag Formatting Analysis**
   - [ ] Analyze tagged examples
   - [ ] Identify formatting requirements
   - [ ] Implement tag styling

3. **User Testing**
   - [ ] Test with real projects
   - [ ] Validate reimport success
   - [ ] Gather feedback

### Medium Term (Next Month)

1. **Multi-Format Support**
   - [ ] Trados Studio review files
   - [ ] CafeTran exports
   - [ ] Generic XLIFF
   - [ ] TMX import/export

---

## Questions for User

1. **Tag Examples**: Can you provide a memoQ bilingual file that contains formatting tags `[1}...{2]`?

2. **Trados Files**: Do you have Trados Studio review DOCX examples to analyze?

3. **Reimport Testing**: Can you test reimporting exported files back into memoQ to verify success?

4. **Priority**: Which format is most important to implement first?
   - memoQ bilingual
   - Trados Studio review
   - CafeTran
   - Other?

5. **Status Values**: What status values does memoQ use besides "Not started"?
   - Confirmed?
   - Reviewed?
   - Proofread?
   - Others?

---

## Conclusion

This feature will **transform Supervertaler** from a TXT-based tool to a **professional CAT tool integration**. The memoQ bilingual format is well-structured and parseable. With proper implementation, this will:

- Eliminate manual workflow steps
- Preserve all project metadata
- Enable seamless round-trip translation
- Position Supervertaler as a professional translation tool

**Estimated Development Time**: 2-4 weeks for full memoQ support  
**Impact Level**: 🚀 **GAME-CHANGING**

---

*Analysis Document v1.0*  
*Date: October 7, 2025*  
*Analyst: GitHub Copilot*
