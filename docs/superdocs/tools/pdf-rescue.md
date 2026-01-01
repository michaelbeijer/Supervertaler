# PDF Rescue (OCR)

This page is the GitBook version of the original PDF Rescue guide.

If you prefer the repository copy, see: https://github.com/michaelbeijer/Supervertaler/blob/main/docs/guides/PDF_RESCUE.md

---

# PDF Rescue - AI-Powered OCR Tool

**Part of [Supervertaler](https://supervertaler.com/) • by Michael Beijer**

---

## 📖 Overview

**PDF Rescue** is a specialised AI-powered OCR tool designed to extract clean, editable text from poorly formatted PDFs. Built into Supervertaler, it uses vision-capable LLM OCR to intelligently recognise text, formatting, redactions, stamps, and signatures—producing professional, translator-ready documents.

### 🎯 The Problem It Solves

Have you ever received a PDF translation job where:
- The text won't copy-paste cleanly?
- Line breaks are all over the place?
- Formatting is completely broken?
- Traditional OCR produces gibberish?
- Redacted sections show as black boxes?
- Stamps and signatures clutter the text?

**PDF Rescue fixes all of this.**

###  Real-World Success Story

> *"I had a client reach out for a rush job—a 4-page legal document that had clearly been scanned badly. Traditional OCR couldn't handle it, and manual retyping would have taken hours.*
> 
> *I used PDF Rescue's one-click PDF import, processed all 4 pages with AI OCR, and it produced a flawless Word document that I could immediately start working with. What would have been a multi-day nightmare became a straightforward job I could deliver on time.*
> 
> *I was able to tell my client that I could handle the job—and delivered professional quality. PDF Rescue literally saved a client relationship."*
> 
> — Michael Beijer, Professional Translator

---

## ✨ Key Features

### 1. 📄 **One-Click PDF Import**
- **No external tools needed** - Import PDFs directly
- **Automatic page extraction** - Each page saved as high-quality PNG (2x resolution)
- **Persistent storage** - Images saved next to source PDF in `{filename}_images/` folder
- **Client-ready** - Images can be delivered to end clients if needed

### 2. 🧠 **Smart AI-Powered OCR**
- **Vision-capable LLM OCR** - High accuracy OCR
- **Context-aware** - Understands document structure and formatting
- **Intelligent cleanup** - Fixes line breaks, spacing, and formatting issues
- **Redaction handling** - Inserts descriptive placeholders like `[naam]`, `[bedrag]` in document language
- **Stamps & signatures** - Detects and describes non-text elements: `[stempel]`, `[handtekening]`

### 3. 🎨 **Optional Formatting Preservation**
- **Markdown-based** - Uses `**bold**`, `*italic*`, `__underline__`
- **Toggle on/off** - User-controlled via checkbox
- **Clean output** - Markdown converted to proper formatting in DOCX export
- **Visual preview** - See formatting markers before export

### 4. 📊 **Batch Processing**
- **Process selected** - Work on individual images
- **Process all** - Batch process entire document
- **Progress tracking** - Visual progress bar and status updates
- **Skip processed** - Already-processed images are skipped (unless re-selected)

### 5. 📝 **Comprehensive Logging**
- **Activity log integration** - All operations logged with timestamps
- **PDF import progress** - Each page extraction logged
- **OCR processing** - Per-image processing logged
- **DOCX export** - Export operations tracked

### 6. 👁️ **Full Transparency**
- **"Show Prompt" button** - View exact instructions sent to AI
- **Configuration display** - See model, formatting settings, max tokens
- **No black boxes** - Complete visibility into AI processing

### 7. 📊 **Professional Session Reports**
- **Markdown format** - Clean, readable documentation
- **Complete configuration** - All settings recorded
- **Processing summary** - Table of all images and status
- **Full extracted text** - All OCR results included
- **Statistics** - Character/word counts and averages
- **Supervertaler branding** - Professional client-ready reports

### 8. 💾 **Flexible Export Options**
- **DOCX export** - Formatted Word documents with optional bold/italic/underline
- **Copy to clipboard** - Quick text extraction
- **Session reports** - Professional MD documentation

### 9. 🚀 **Standalone Mode**

Can run independently outside Supervertaler:

```bash
python modules/pdf_rescue.py
```

Full-featured standalone application with all capabilities.

---

## 🎯 Workflow

### Quick Start (5 Steps)

1. **Open PDF Rescue** - Navigate to Assistant panel → PDF Rescue tab
2. **Import PDF** - Click "📄 PDF" button, select your badly-formatted PDF
3. **Check formatting option** - Leave "Preserve formatting" checked (default)
4. **Process** - Click "⚡ Process ALL" to OCR all pages
5. **Export** - Click "💾 Save DOCX" to create Word document

**That's it!** You now have a clean, editable Word document ready for translation.

---

### Detailed Workflow

#### Step 1: Import Your PDF

**Method 1: Direct PDF Import** (Recommended)
```
Click: 📄 PDF button
→ Select PDF file
→ Automatic page extraction to {filename}_images/ folder
→ All pages added to processing queue
```

**Method 2: Manual Image Import**
```
Click: 📁 Add Files → Select individual images
OR
Click: 📂 Folder → Select folder with images
```

**Result**: All images listed in left panel with ✓ status indicators

---

#### Step 2: Configure Settings

**Model Selection**:
- `gpt-4o` (Recommended) - Latest, fastest, best quality
- `gpt-4o-mini` - Budget option, good quality
- `gpt-4-turbo` - Alternative, similar quality to gpt-4o

**Formatting Option**:
- ✓ **Preserve formatting (bold/italic/underline)** - Enabled by default
- Unchecked = Plain text output only

**Extraction Instructions**:
- Default instructions optimized for badly formatted PDFs
- Handles redactions, stamps, signatures automatically
- Can customize if needed (advanced)
- Click **"👁️ Show Prompt"** to see exact AI instructions

---

#### Step 3: Process Images

**Option A: Process Selected**
```
1. Select image(s) in list
2. Click: 🔍 Process Selected
3. View result in preview pane
```

**Option B: Process All** (Recommended)
```
1. Click: ⚡ Process ALL
2. Confirm batch processing dialog
3. Watch progress bar
4. All pages processed automatically
```

**Processing Details**:
- Each image sent to the OCR model
- Text extracted with context awareness
- Formatting detected (if enabled)
- Redactions/stamps/signatures handled
- Results stored in memory
- ✓ indicator appears when processed

---

#### Step 4: Review & Export

**Review Extracted Text**:
- Click any processed image in list
- Preview pane shows extracted text
- Formatting shown as markdown (`**bold**`, `*italic*`, etc.)
- Verify quality before export

**Export Options**:

1. **💾 Save DOCX** (Primary export)
   - Formatted Word document
   - Markdown converted to proper formatting
   - One page per document page
   - Page headers with filenames
   - Ready for translation work

2. **📋 Copy All**
   - All text to clipboard
   - Includes page separators
   - Quick paste into any application

3. **📊 Session Report**
   - Professional markdown documentation
   - Complete configuration record
   - All extracted text included
   - Statistics and metadata
   - Client-ready deliverable
