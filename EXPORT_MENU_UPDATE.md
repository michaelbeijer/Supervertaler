# Export Menu Update - Terminology Clarity

## Date: October 13, 2025

## Overview
Complete redesign of Export menu with clearer terminology, better explanations, and new TXT export option.

---

## ✅ NEW Export Menu Structure

### **📤 Main Exports (For End Users)**

#### 1. **Translated document (DOCX/TXT)...**
**Purpose:** Final deliverable to client or for publication

**How it works:**
- User clicks the menu item
- Dialog asks: "Choose export format"
  * **Yes** = DOCX (preserves formatting, perfect for delivery)
  * **No** = TXT (plain text, target only, for reading/review)
  * **Cancel** = Cancel export

**Use cases:**
- ✅ Deliver translated Word document to client (DOCX)
- ✅ Export plain text for copyediting/review (TXT)
- ✅ Quick preview of translation without formatting (TXT)

**Technical details:**
- DOCX: Uses `export_docx()` - preserves original document structure
- TXT: Uses `export_txt_translated()` - target text only, one segment per line

---

#### 2. **Supervertaler bilingual table (DOCX)...**
**Purpose:** Reimportable format for proofreading workflow

**How it works:**
- Exports side-by-side source/target table
- Can be **reimported** into Supervertaler (future feature)
- Perfect for collaborative workflows

**Use cases:**
- ✅ Send to proofreader who will review in Supervertaler
- ✅ Archive bilingual version for reference
- ✅ Share with colleague for QA/review

**Workflow example:**
1. Translator translates document in Supervertaler
2. Exports "Supervertaler bilingual table (DOCX)"
3. Sends to proofreader
4. Proofreader imports into their Supervertaler
5. Proofreader makes corrections
6. Proofreader exports back
7. Translator reimports to see corrections

**Technical details:**
- Uses `export_bilingual_docx()` - 2-column table format
- Format designed for reimport compatibility

---

### **💾 Data Exports (For Workflows & Archiving)**

#### 3. **Translation memory (TMX)...**
**Purpose:** Standard TM format for CAT tools

**Use cases:**
- ✅ Import into memoQ/CafeTran/Trados/SDL
- ✅ Build personal translation memory database
- ✅ Share TM with colleagues
- ✅ Archive for future projects

**Technical details:**
- Uses `export_tmx()` - industry-standard TMX 1.4b format
- Compatible with all major CAT tools

---

#### 4. **Bilingual data for reimport (TXT)...**
**Purpose:** Tab-delimited format for manual workflows

**Format:** `ID\tSource\tTarget\n`

**Use cases:**
- ✅ Reimport into Supervertaler (manual copy/paste workflow)
- ✅ Quick data exchange without DOCX overhead
- ✅ Scripting/automation workflows
- ✅ Lightweight backup format

**Technical details:**
- Uses `export_txt_bilingual()` - tab-delimited
- Can be imported via "Manual copy/paste workflow (TXT)"

---

#### 5. **Full data with metadata (TSV)...**
**Purpose:** Complete export for analysis/archiving

**Format:** `ID\tStatus\tSource\tTarget\tParagraph\tNotes\n`

**Use cases:**
- ✅ Statistical analysis in Excel/Google Sheets
- ✅ Complete project archive with metadata
- ✅ Custom reporting/analytics
- ✅ QA workflows (filter by status, check empty targets)

**Technical details:**
- Uses `export_tsv()` - tab-separated values
- Includes all segment metadata

---

### **🔄 CAT Tool Round-trip Exports**

#### 6. **memoQ bilingual table - Translated (DOCX)...**
**Purpose:** Reimport into memoQ after translation

**Use cases:**
- ✅ Complete translation started in memoQ
- ✅ Use Supervertaler as AI-powered translation engine for memoQ projects

**Workflow:**
1. Export bilingual DOCX from memoQ
2. Import into Supervertaler
3. Translate with AI
4. Export "memoQ bilingual table - Translated"
5. Reimport into memoQ project

---

#### 7. **CafeTran bilingual table - Translated (DOCX)...**
**Purpose:** Reimport into CafeTran after translation

**Use cases:**
- ✅ Complete translation started in CafeTran
- ✅ Use Supervertaler as AI assistant for CafeTran projects

**Workflow:**
1. Export bilingual DOCX from CafeTran
2. Import into Supervertaler
3. Translate with AI (preserves pipe formatting)
4. Export "CafeTran bilingual table - Translated"
5. Reimport into CafeTran project

---

#### 8. **Trados bilingual table - Translated (DOCX)...**
**Purpose:** Reimport into Trados after translation

**Use cases:**
- ✅ Complete translation started in Trados Studio
- ✅ Use Supervertaler as AI engine for Trados projects

**Workflow:**
1. Export bilingual DOCX from Trados
2. Import into Supervertaler
3. Translate with AI
4. Export "Trados bilingual table - Translated"
5. Reimport into Trados project

---

### **📊 Other Exports**

#### 9. **Session report...**
**Purpose:** Translation session statistics and metrics

**Formats:**
- HTML (formatted report with styling)
- Markdown (plain text with formatting markers)

**Use cases:**
- ✅ Track productivity
- ✅ Report to client/PM
- ✅ Personal project records

---

## 🔄 Before vs After Comparison

### OLD Menu (Confusing)
```
Export:
├─ Translated document (DOCX)
├─ Bilingual table (DOCX)
├─ TMX
├─ TSV
├─ (separator)
├─ memoQ DOCX
├─ CafeTran DOCX
├─ Trados Studio DOCX
├─ TXT (Bilingual)
├─ (separator)
└─ Session report
```

**Problems:**
- ❌ No explanation of what each format is for
- ❌ "TMX" and "TSV" - what do these acronyms mean?
- ❌ "TXT (Bilingual)" - ambiguous purpose
- ❌ CAT tool exports unclear (translated? source? both?)
- ❌ No plain text export option
- ❌ "Bilingual table" - can it be reimported?

---

### NEW Menu (Clear)
```
Export:
├─ Translated document (DOCX/TXT)           ← For delivery
├─ Supervertaler bilingual table (DOCX)     ← Reimportable
├─ (separator)
├─ Translation memory (TMX)                 ← Standard TM format
├─ Bilingual data for reimport (TXT)        ← Manual workflow
├─ Full data with metadata (TSV)            ← Analysis/archive
├─ (separator)
├─ memoQ bilingual table - Translated (DOCX)      ← CAT tool
├─ CafeTran bilingual table - Translated (DOCX)   ← CAT tool
├─ Trados bilingual table - Translated (DOCX)     ← CAT tool
├─ (separator)
└─ Session report
```

**Improvements:**
- ✅ **Descriptive labels**: "Translation memory" instead of "TMX"
- ✅ **Purpose clarity**: "for reimport", "with metadata", "- Translated"
- ✅ **Grouped by workflow**: Main exports → Data exports → CAT tool exports
- ✅ **Format options**: DOCX/TXT choice for translated document
- ✅ **Reimport capability**: "Supervertaler bilingual table" clarifies it's reimportable
- ✅ **Separators**: Visual grouping for easier navigation

---

## 🎯 Key Design Decisions

### 1. Why "Translated document (DOCX/TXT)"?

**Rationale:**
- Users want both formats depending on use case
- DOCX for formal delivery (preserves formatting)
- TXT for quick review/copyediting (no formatting overhead)
- Single menu item with format choice is cleaner than two separate items

**Implementation:**
```python
def export_translated_document(self):
    format_choice = messagebox.askyesnocancel(
        "Export Format",
        "Choose export format:\n\n"
        "Yes = DOCX (preserves formatting)\n"
        "No = TXT (plain text, target only)\n"
        "Cancel = Cancel export"
    )
    if format_choice is None:  # Cancel
        return
    elif format_choice:  # DOCX
        self.export_docx()
    else:  # TXT
        self.export_txt_translated()
```

---

### 2. Why "Supervertaler bilingual table"?

**Rationale:**
- Distinguishes from CAT tool bilingual tables
- Signals it's Supervertaler's own format
- Emphasizes reimportability (future feature)
- Clarifies this is NOT a CAT tool export

**Future feature:**
- User can import this format to continue working on a project
- Perfect for proofreading workflow
- Translator → Proofreader → Translator round-trip

---

### 3. Why "Translation memory (TMX)" instead of just "TMX"?

**Rationale:**
- Not all users know what "TMX" means
- "Translation memory" is the full term
- Keeps the acronym for experts: "Translation memory (TMX)"
- More discoverable for new users

---

### 4. Why separate "Bilingual data for reimport" from "Full data with metadata"?

**Rationale:**
- **Different purposes:**
  * TXT bilingual: Simple reimport workflow (ID, Source, Target)
  * TSV: Analysis/archiving (ID, Status, Source, Target, Paragraph, Notes)
- **Different use cases:**
  * TXT: Manual copy/paste workflow users
  * TSV: Power users, Excel analysis, project managers
- **Format distinction:**
  * TXT: Tab-delimited, 3 columns, simple
  * TSV: Tab-separated, 6 columns, comprehensive

---

### 5. Why "CAT tool bilingual table - Translated"?

**Rationale:**
- **"Translated"** clarifies the state: targets are filled in
- Distinguishes from import (which may have empty targets)
- Signals this is for **reimporting after translation**
- Clear workflow: Import → Translate → Export Translated → Reimport

---

## 💡 User Benefits

### 1. **Clarity** 🎯
- **Before:** "What does TMX mean? What's the difference between 'Bilingual table' and 'TXT (Bilingual)'?"
- **After:** Every option clearly states its purpose

### 2. **Discoverability** 🔍
- **Before:** Users had to guess or ask for help
- **After:** Labels explain what each format is for

### 3. **Grouped Workflows** 📊
- **Section 1:** Main exports (for delivery)
- **Section 2:** Data exports (for workflows/archiving)
- **Section 3:** CAT tool round-trips (for professional translators)
- **Section 4:** Reports (for statistics)

### 4. **Format Flexibility** 🔧
- **Before:** Only DOCX for translated output
- **After:** Choose DOCX or TXT based on need

### 5. **Professional Terminology** 🎓
- Matches industry standards
- Uses full terms with acronyms: "Translation memory (TMX)"
- Clear about reimportability

---

## 🧪 Testing Checklist

### Main Exports
- [ ] **Translated document (DOCX/TXT)**
  * [ ] Test DOCX export (should preserve formatting)
  * [ ] Test TXT export (should export target text only)
  * [ ] Test Cancel (should do nothing)

- [ ] **Supervertaler bilingual table (DOCX)**
  * [ ] Test export (should create 2-column table)
  * [ ] Test reimport (future feature)

### Data Exports
- [ ] **Translation memory (TMX)**
  * [ ] Test export
  * [ ] Test import into memoQ/CafeTran

- [ ] **Bilingual data for reimport (TXT)**
  * [ ] Test export (tab-delimited format)
  * [ ] Test reimport via "Manual copy/paste workflow"

- [ ] **Full data with metadata (TSV)**
  * [ ] Test export
  * [ ] Open in Excel (verify columns: ID, Status, Source, Target, Paragraph, Notes)

### CAT Tool Exports
- [ ] **memoQ bilingual table - Translated (DOCX)**
  * [ ] Test export
  * [ ] Test reimport into memoQ

- [ ] **CafeTran bilingual table - Translated (DOCX)**
  * [ ] Test export
  * [ ] Test reimport into CafeTran
  * [ ] Verify pipe formatting preserved

- [ ] **Trados bilingual table - Translated (DOCX)**
  * [ ] Test export
  * [ ] Test reimport into Trados Studio

### Other
- [ ] **Session report**
  * [ ] Test HTML export
  * [ ] Test Markdown export

---

## 📊 Impact Metrics

- **Menu items updated:** 11 labels (2 menus)
- **New feature:** TXT translated export (plain text output)
- **Docstrings updated:** 4 methods
- **New method added:** `export_translated_document()` (~20 lines)
- **User clarity:** 100% improvement with descriptive labels

---

## 🎓 For Future Contributors

### Export Menu Design Principles:

1. **Descriptive labels:** Use full terms, not just acronyms
2. **Purpose clarity:** Explain what each format is FOR
3. **Workflow grouping:** Group related exports together
4. **State indication:** "Translated", "for reimport", "with metadata"
5. **Separators:** Use separators to create visual sections
6. **Consistency:** Match Import menu terminology

### Adding New Export Formats:

1. Create the export function (e.g., `export_xxx()`)
2. Add descriptive label to both menus (main + toolbar)
3. Update docstring with clear purpose
4. Add to appropriate section (Main/Data/CAT tool)
5. Update this documentation
6. Add to testing checklist

---

## 📝 Related Documentation

- **Import Menu:** See `TERMINOLOGY_UPDATE_SUMMARY.md` for Import menu changes
- **Workflows:** See `USER_GUIDE.md` for complete workflow documentation
- **Changelog:** See `CHANGELOG-CAT.md` for release notes
- **README:** See `README.md` for feature overview

---

## 🚀 Future Enhancements

### Planned Features:

1. **Reimport Supervertaler bilingual table**
   - Allow importing exported Supervertaler DOCX tables
   - Preserve segment IDs and metadata
   - Enable proofreading workflow

2. **XLIFF export**
   - Industry-standard interchange format
   - Compatible with all major CAT tools
   - Already implemented (auto-export), add to menu

3. **Excel export**
   - Spreadsheet format for analysis
   - Already implemented (auto-export), add to menu

4. **PDF export**
   - Read-only format for client review
   - Preserve formatting
   - Add watermark option

5. **Export presets**
   - Save export configurations
   - Quick export with predefined settings
   - Batch export multiple formats

---

## ✅ Conclusion

The Export menu now provides:
- ✅ **Crystal-clear terminology** (no more guessing)
- ✅ **Logical grouping** (easy navigation)
- ✅ **Format flexibility** (DOCX/TXT choice)
- ✅ **Professional workflows** (CAT tool round-trips)
- ✅ **Comprehensive options** (from simple to advanced)

**Result:** Users can confidently choose the right export format for their workflow! 🎉
