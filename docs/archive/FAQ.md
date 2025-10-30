# Supervertaler - Frequently Asked Questions

**Last Updated**: October 19, 2025  
**Version**: 3.7.0 (Latest Stable Release) / 2.5.0-CLASSIC

---

## 📑 Table of Contents

1. [About Supervertaler](#about-supervertaler)
2. [Getting Started](#getting-started)
3. [Supervertaler Features](#supervertaler-features)
4. [Technical Questions](#technical-questions)
5. [Workflow & Integration](#workflow--integration)
6. [Data Privacy & Confidentiality](#data-privacy--confidentiality)
7. [Troubleshooting](#troubleshooting)
8. [Development & History](#development--history)
9. [Miscellaneous](#miscellaneous)

---

## About Supervertaler

### What is Supervertaler?

Supervertaler is a context-aware, LLM-powered translation and proofreading tool designed specifically for professional translators. It leverages multiple AI providers (OpenAI GPT-4, Anthropic Claude, Google Gemini) and multiple context sources (translation memory, tracked changes, custom instructions, full document context) to deliver highly accurate translations that maintain consistency and domain expertise.

### What does "Supervertaler" mean?

**Supervertaler** is Dutch for "super translator" (*super* = super, *vertaler* = translator). 

The name reflects the creator's Dutch-American heritage and adds a bit of international flair to a tool designed for translators worldwide. It's also delightfully straightforward – no clever acronyms, no marketing gymnastics, just a Dutch word that does exactly what it says on the tin: translates, superbly.

Plus, it's fun to say. Try it: *"Soo-per-ver-TAH-ler"*. See? You're smiling already. 😊

### Who created Supervertaler?

Supervertaler was created by **Michael Beijer**, a professional translator and language technology enthusiast, with assistance from AI coding assistants. The project represents a collaboration between human expertise in translation workflows and AI capabilities in software development.

**Website**: [michaelbeijer.co.uk](https://michaelbeijer.co.uk/)  
**GitHub**: [github.com/michaelbeijer/Supervertaler](https://github.com/michaelbeijer/Supervertaler)

### How was Supervertaler created?

Supervertaler was developed using:
- **IDE**: Visual Studio Code (VS Code)
- **Primary AI Assistant**: Claude Sonnet 3.5 (later Sonnet 4.5) in Agent mode
- **Programming Language**: Python 3.12
- **GUI Framework**: tkinter (Python's standard GUI library)
- **Development Method**: Human-AI collaborative coding
  - Michael provided translation expertise, workflow requirements, and design decisions
  - Claude handled implementation, debugging, and technical architecture
  - Iterative development with extensive testing on real translation projects

The development process showcases the potential of AI-assisted software development when combined with domain expertise from a professional user.

### Who is Supervertaler for? (Target Audience)

**Primary Users**:
- **Professional translators** working with CAT tools (memoQ, CafeTran, Trados Studio, Wordfast)
- **Technical translators** handling patents, legal documents, medical texts, and specialized content
- **Freelance translators** seeking to enhance productivity with AI-powered assistance
- **Translation agencies** looking for quality assurance and consistency tools

**Ideal For**:
- Translators who want **AI assistance without losing control**
- Users who need **multiple context sources** (TM, glossaries, tracked changes, document context)
- Professionals requiring **flexible AI provider choice** (OpenAI, Claude, Gemini)
- CAT tool users wanting **seamless workflow integration**

**Not Ideal For**:
- Casual users needing simple text translation (use Google Translate, DeepL instead)
- Users without API keys for AI providers (requires paid API access)
- Projects requiring machine translation alone (Supervertaler adds context layers and control)

### How does Supervertaler compare to other translation tools?

**vs. Machine Translation (Google Translate, DeepL)**:
- ✅ **Context-aware**: Uses full document context, not just individual sentences
- ✅ **Customizable**: Custom instructions, system prompts, terminology management
- ✅ **TM integration**: Leverages translation memory for consistency
- ✅ **Professional control**: Inline editing, status tracking, project management

**vs. Traditional CAT Tools (memoQ, Trados)**:
- ✅ **AI-powered**: LLM translation with contextual understanding
- ✅ **Flexible AI**: Choose between OpenAI, Claude, Gemini
- ✅ **Modern UI**: Clean, responsive interface with multiple view modes
- ⚠️ **Complementary tool**: Works *with* CAT tools via bilingual DOCX, not as replacement

### What makes Supervertaler different? (The AI-First Philosophy)

**Traditional CAT tools** rely heavily on rule-based systems:
- Complex regex patterns for text processing
- Rigid QA rules that must be manually configured
- Fixed workflows that require technical knowledge to customize
- Limited by what developers anticipated users would need

**Supervertaler's AI-First Approach**:
Instead of writing countless rules, we simply ask the AI in natural language:

- **QA Example**: Instead of configuring dozens of QA rules, just ask: *"Run QA on my translation. Check for consistency, terminology accuracy, and formatting issues."*
  
- **Text Processing Example**: Instead of writing complex regex patterns, describe what you want: *"Extract all figure references and create a numbered list"* or *"Convert all product codes to uppercase and add hyphens every 4 characters"*

- **Custom Workflows Example**: Instead of being limited to predefined features, describe your need: *"Flag all segments containing measurements and suggest metric conversions"* or *"Identify segments with legal terminology and mark them for expert review"*

**The Power of Natural Language Control**:
- 🎯 **Intuitive**: Describe tasks in plain English instead of learning rule syntax
- 🚀 **Flexible**: Adapt workflows on-the-fly without software updates
- 🧠 **Contextual**: AI understands nuance and context that rigid rules miss
- ⚡ **Efficient**: Accomplish complex tasks with simple instructions

**Example - Traditional vs AI-First**:

*Traditional CAT Tool QA*:
```
✗ Configure: Number consistency check
✗ Configure: Terminology variance check  
✗ Configure: Tag presence validation
✗ Configure: Punctuation matching
✗ Configure: Length ratio limits
... (dozens more rules)
```

*Supervertaler AI-First QA*:
```
✓ "Run comprehensive QA on this translation. Focus on:
   - Consistency with translation memory
   - Proper use of client terminology
   - Tag preservation and formatting
   - Natural flow in target language
   - Technical accuracy for patent content"
```

The AI understands the intent, applies contextual judgment, and adapts to your specific project needs—all without rigid rule configuration.

This philosophy extends beyond QA to every aspect of translation work: prompt engineering replaces rule configuration, natural language replaces regex, and AI reasoning replaces rigid algorithms.

---

**vs. AI Translation Plugins**:
- ✅ **Standalone**: No subscription to specific CAT tool required
- ✅ **Multi-provider**: Not locked into one AI service
- ✅ **Full control**: Direct access to AI parameters, prompts, and context
- ✅ **Advanced features**: Tracked changes analysis, custom prompt library, auto-export options

**Unique Advantages**:
- **Multiple context sources**: TM + tracked changes + glossaries + document context + custom instructions
- **Dual architecture**: CLASSIC edition (DOCX workflow) + CAT edition (segment editor)
- **Developer-friendly**: Open source, Python-based, extensible
- **Bilingual format support**: CafeTran and memoQ bilingual DOCX with formatting preservation

---

## Getting Started

### Which version should I use?

**v2.5.0-CLASSIC (Recommended for Production)**:
- ✅ Fully tested and stable
- ✅ Original DOCX-based workflow
- ✅ Perfect for CAT tool integration (CafeTran, memoQ)
- ✅ Image/drawings context support for technical documents
- ✅ Proofreading mode with tracked changes analysis
- 📖 See: `USER_GUIDE.md`

**v3.7.0 (Latest - Stable Release)**:
- 🎯 Segment-based CAT editor architecture
- 🎨 Professional UI with Grid, List, and Document views
- 🎯 Multi-selection system (Ctrl/Shift/Ctrl+A)
- ⚡ Grid pagination (10x faster loading)
- ✅ Production-ready with all major features
- 📖 See: `CHANGELOG.md`

**Rule of Thumb**:
- **Production work** → Use v3.7.0 (Latest) or v2.5.0-CLASSIC
- **Legacy workflows** → Stick with v2.5.0-CLASSIC

### What do I need to run Supervertaler?

**Required**:
- Python 3.12 or higher
- Windows OS (tested on Windows 10/11)
- API keys for at least one AI provider:
  - OpenAI API key (for GPT-4, GPT-4o, GPT-4 Turbo)
  - Anthropic API key (for Claude Sonnet, Claude Opus)
  - Google API key (for Gemini Pro, Gemini Flash)

**Optional but Recommended**:
- PIL/Pillow library (for image context support in v2.5.0-CLASSIC)
- python-docx library (for DOCX handling)
- openpyxl library (for Excel export in v3.x)

**Setup Steps**:
1. Install Python 3.12+ from [python.org](https://python.org)
2. Clone or download Supervertaler from GitHub
3. Create `api_keys.txt` in root directory (see `api_keys.example.txt`)
4. Add your API keys to `api_keys.txt`
5. Run `python Supervertaler_v3.7.0.py` or `python Supervertaler_v2.5.0-CLASSIC.py`

### How do I get API keys?

**OpenAI** (GPT-4):
1. Visit [platform.openai.com](https://platform.openai.com)
2. Create account or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy key to `api_keys.txt` as `OPENAI_API_KEY=sk-...`

**Anthropic** (Claude):
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create account or log in
3. Navigate to API Keys
4. Generate new key
5. Copy key to `api_keys.txt` as `ANTHROPIC_API_KEY=sk-ant-...`

**Google** (Gemini):
1. Visit [aistudio.google.com](https://aistudio.google.com)
2. Create account or log in
3. Click "Get API key"
4. Generate key
5. Copy key to `api_keys.txt` as `GOOGLE_API_KEY=...`

**Cost Considerations**:
- All providers charge per token (input + output)
- Typical translation: $0.01 - $0.10 per page (varies by model and context)
- Claude and GPT-4 are more expensive but often higher quality
- Gemini Flash is most cost-effective for high-volume work

---

## Supervertaler Features

### Three CAT Editor Views (v3.x only)

Supervertaler v3.7.0 offers three professional view modes, each optimized for different tasks:

**1. Grid View** (Default - Professional Editing)
- **Best for**: Segment-by-segment editing, detailed work
- **Layout**: Spreadsheet-like grid with columns: #, Type, Style, Source, Target, Status
- **Features**:
  - Multi-selection (Ctrl/Shift/Ctrl+A)
  - Inline editing (double-click cells)
  - Status icons (✗/~/✓/✓✓/🔒) with color coding
  - Column resizing (drag borders)
  - Pagination (50 segments per page for fast loading)
- **Shortcuts**: Ctrl+1, View menu → Grid View

**2. List View** (Vertical Reading)
- **Best for**: Reading flow, reviewing translations, quick context checking
- **Layout**: Vertical stack of segment cards
- **Features**:
  - Source and target text displayed vertically
  - Segment metadata (ID, status, type, style)
  - Full text visible without column constraints
  - Easy scrolling through document
- **Shortcuts**: Ctrl+2, View menu → List View

**3. Document View** (Natural Reading)
- **Best for**: Final review, readability check, contextual proofreading
- **Layout**: Document-like presentation with paragraphs
- **Features**:
  - Source and target side-by-side
  - Smart paragraph detection (groups sentences intelligently)
  - Natural reading experience
  - Closest to final document appearance
- **Shortcuts**: Ctrl+3, View menu → Document View

**Switching Views**:
- Views are persistent - data is preserved when switching
- All views show the same segments, just different presentations
- Edit in any view, changes reflect everywhere
- Choose view based on current task (editing → Grid, reviewing → Document)

### Dual Text Selection (Grid View)

**What is it?**  
A memoQ-style feature that allows you to select corresponding pieces of source and target text simultaneously in the Grid View. This makes it easy to compare parallel text segments.

**How it works**:
1. Select text in Source column → corresponding text in Target column is auto-selected
2. Select text in Target column → corresponding text in Source column is auto-selected
3. Visual highlighting shows both selections in blue
4. Perfect for reviewing terminology consistency and parallel structure

**Use cases**:
- Verifying that technical terms are translated consistently
- Checking that formatting markers appear in corresponding positions
- Reviewing parallel sentence structure
- Quality assurance and proofreading

**Note**: This feature is specific to Grid View and works with individual segment text selection.

### Multi-Selection System (v3.x only)

**What is it?**  
Select multiple segments simultaneously for bulk operations - inspired by professional CAT tools like memoQ.

**How to use**:
- **Ctrl+Click**: Toggle individual segments (add/remove from selection)
- **Shift+Click**: Select range from last selected segment to clicked segment
- **Ctrl+A**: Select all visible segments on current page

**Visual feedback**:
- Selected rows highlighted with blue background (#CCE5FF)
- Selection counter in status bar: "X segment(s) selected"
- ID column clickable for easy selection

**Bulk operations**:
- Change Status (Ctrl+T): Change status of all selected segments
- Lock/Unlock (Ctrl+L): Lock or unlock selected segments
- Clear Selection: Remove all selections

**Workflow example**:
1. Select multiple untranslated segments with Ctrl+Click
2. Press Ctrl+T to translate them in batch
3. AI processes all selected segments with shared context
4. Review and edit results
5. Select translated segments and press Ctrl+L to lock them

### Figure Context / Visual Context Support (v2.5.0-CLASSIC, v3.7.0)

**What is it?**  
Load technical drawings, diagrams, and figures to provide visual context to AI during translation. Essential for patent documents, technical manuals, and scientific papers where text references visual elements.

**How it works**:
1. Prepare a folder with your figure images (PNG, JPG, JPEG, WEBP, GIF, BMP, TIFF)
2. Name files to match figure references: "Figure 1.png", "Figure 2A.jpg", "fig-3b.png"
3. In Supervertaler: `Resources > 🖼️ Load Figure Context...`
4. Select your figures folder
5. During translation, when Supervertaler detects a figure reference in text, it automatically includes the corresponding image in the AI prompt

**Example**:
- **File**: `Figure 1A.png` in figures folder
- **Text**: "As shown in Figure 1A, the motor housing (12) connects to shaft (14)..."
- **Result**: AI receives both text AND image, understands spatial relationships, part labels, and technical details
- **Translation**: More accurate because AI can "see" what's being described

**Figure reference patterns detected**:
- "Figure 1", "Figure 2A", "Figure 3-B"
- "Figuur 1" (Dutch), "fig. 2", "Fig 3"
- Case-insensitive, flexible formatting

**Benefits**:
- ✅ Accurate translation of technical descriptions
- ✅ Correct identification of parts and components
- ✅ Understanding of spatial relationships
- ✅ Proper translation of figure labels and annotations
- ✅ Essential for patent claims and technical specifications

**Supported in**: v2.5.0-CLASSIC (full support), v3.7.0 (full support with multimodal API)  
**UI indicators**: Context status shows "🖼️ X figures" when loaded

### Bilingual CAT Tool File Import/Translation/Export

**What is it?**  
Direct support for bilingual DOCX files from professional CAT tools (CafeTran, memoQ), allowing seamless integration into existing translation workflows.

**CafeTran Bilingual DOCX (AI-Based)**:
- **Format**: Source | Target pairs separated by tab
- **Formatting**: Pipe symbols `|text|` mark formatted text
- **Import**: Click "☕ Import CafeTran DOCX" (green button)
- **AI Processing**: Claude/GPT intelligently preserves pipe positions even with word reordering
- **Export**: Click "☕ Export to CafeTran DOCX" - pipes displayed as BOLD + RED
- **Reimport**: Import back to CafeTran with perfect formatting preservation

**memoQ Bilingual DOCX (Programmatic)**:
- **Format**: Source and target in table structure
- **Formatting**: Bold, italic, underline tracked algorithmically
- **Import**: Click "📊 Import memoQ DOCX" (green button)
- **Processing**: Formatting extracted, preserved, and reapplied programmatically
- **Export**: Click "📊 Export to memoQ DOCX" - all formatting intact
- **Reimport**: Import back to memoQ with 100% formatting accuracy

**Benefits**:
- ✅ No manual copy-paste between tools
- ✅ Formatting preservation (bold, italic, underline)
- ✅ Complete round-trip workflow verified
- ✅ Works with existing CAT tool projects
- ✅ AI-powered translation with professional CAT tool features

**Workflow**:
1. **In CAT tool**: Export bilingual DOCX
2. **In Supervertaler**: Import → Configure → Translate → Export
3. **In CAT tool**: Reimport translated DOCX
4. **Result**: Translated segments with formatting preserved, ready for review

### PDF Rescue - AI-Powered OCR Tool (v3.5.0-beta+)

**What is it?**  
PDF Rescue is a specialized AI-powered OCR tool built into Supervertaler. It extracts clean, editable text from badly formatted, scanned, or damaged PDFs using GPT-4 Vision—perfect for those "impossible" translation jobs.

**The Problem It Solves**:
Have you ever received a PDF where:
- Text won't copy-paste cleanly (broken line breaks)
- Traditional OCR produces gibberish
- Formatting is completely destroyed
- Redacted sections show as black boxes
- Stamps and signatures clutter the text
- Manual retyping would take hours

**PDF Rescue fixes all of this.**

**How it works**:
1. **Import PDF**: Click "📄 PDF" button → select badly-formatted PDF
2. **Automatic extraction**: PyMuPDF extracts each page as high-quality PNG (2x resolution)
3. **AI OCR**: GPT-4 Vision processes images and extracts clean text
4. **Smart handling**: Detects redactions, stamps, signatures → inserts descriptive placeholders
5. **Export DOCX**: Clean, formatted Word document ready for translation

**Key Features**:
- ✅ **One-click PDF import** - No external tools needed
- ✅ **GPT-4 Vision OCR** - Industry-leading accuracy
- ✅ **Smart redaction handling** - Inserts language-aware placeholders (`[naam]`, `[bedrag]`, `[datum]`)
- ✅ **Formatting preservation** - Optional markdown-based bold/italic/underline
- ✅ **Batch processing** - Process entire documents at once
- ✅ **Professional exports** - DOCX, session reports (MD), clipboard copy
- ✅ **Full transparency** - "Show Prompt" button reveals exact AI instructions
- ✅ **Persistent storage** - Images saved next to source PDF (client-deliverable!)

**Real-World Success Story**:
> *"Client reached out for rush job—4-page legal document scanned badly. Traditional OCR couldn't handle it. PDF Rescue's one-click import + AI OCR produced flawless Word doc. Multi-day nightmare became straightforward job delivered on time. Literally saved a client relationship."*  
> — Michael Beijer, Professional Translator

**Smart Features Explained**:

**Language-Aware Redaction Handling**:
- Dutch document: `De heer [naam] heeft €[bedrag] betaald op [datum]`
- English document: `Mr. [name] paid $[amount] on [date]`
- No manual language specification needed!

**Stamp & Signature Detection**:
- Identifies stamps: `[stempel]` (Dutch) or `[stamp]` (English)
- Identifies signatures: `[handtekening]` (Dutch) or `[signature]` (English)
- Contextual descriptions in square brackets

**Optional Formatting**:
- AI outputs markdown: `**bold**`, `*italic*`, `__underline__`
- Preview shows markdown (temporary)
- DOCX export has proper Word formatting (no visible markers)
- Toggle on/off via checkbox

**When to use PDF Rescue**:
- ✅ Badly formatted scanned PDFs
- ✅ Documents that won't copy-paste
- ✅ Files with redactions/stamps/signatures
- ✅ Traditional OCR fails
- ✅ Client needs editable version
- ✅ Legal documents with redactions
- ✅ Government forms with stamps

**Session Reports**:
PDF Rescue generates professional markdown reports with:
- Complete configuration record
- Processing summary table (all images + status)
- Full extracted text with page separators
- Statistics (character/word counts)
- Supervertaler branding (client-ready deliverable)

**Standalone Mode**:
Can run independently outside Supervertaler:
```bash
python modules/pdf_rescue.py
```

**Full Documentation**: See [`docs/guides/PDF_RESCUE.md`](docs/guides/PDF_RESCUE.md) for complete guide

### Translation Memory (TM) Integration

**What is it?**  
Load TMX translation memory files to provide AI with terminology consistency, previous translations, and domain-specific context.

**How to use**:
1. Click "📂 Load TM" in Assistant panel (TM tab)
2. Select TMX file(s) (standard TMX 1.4b format)
3. TM loads and indexes all translation units
4. During translation, Supervertaler searches TM for similar segments
5. Fuzzy matches above threshold are provided to AI as context

**Fuzzy Matching**:
- Configurable similarity threshold (default: 70%)
- Matches found using text similarity algorithms
- AI receives: "Similar translation from your TM: SOURCE → TARGET"
- AI uses matches for consistency and terminology

**Benefits**:
- ✅ Terminology consistency across projects
- ✅ Reduced translation cost (reuse existing translations)
- ✅ Domain-specific vocabulary reinforcement
- ✅ Client-specific style and terminology
- ✅ Quality through consistency

**Advanced features**:
- Multiple TM files supported simultaneously
- Auto-save translated segments to TM (optional)
- TMX export of completed translations
- TM statistics in Assistant panel

### Custom Instructions

**What is it?**  
Project-specific translation guidelines that you can save and reuse. Tell the AI exactly how you want translations handled.

**Examples**:
- "Prefer formal tone and use 'u' instead of 'je' in Dutch"
- "Preserve all technical acronyms untranslated"
- "Use British English spelling (colour, not color)"
- "Maintain consistency with client's brand terminology"
- "Translate measurements to metric system"

**How to use**:
1. Open Unified Prompt Library (Ctrl+P)
2. Navigate to Custom Instructions tab
3. Create new instruction file or edit existing
4. Write your guidelines in plain English
5. Save to `user data/Custom_instructions/`
6. Select instruction before translating

**Format (JSON)**:
```json
{
  "name": "Formal Dutch Translation",
  "instructions": "Use formal tone. Prefer 'u' over 'je'. Use complete sentences."
}
```

**Benefits**:
- ✅ Reusable across projects
- ✅ Consistent translation style
- ✅ Client-specific guidelines
- ✅ Domain-specific instructions
- ✅ Share instructions with team members

### System Prompts (Role-Based Translation)

**What is it?**  
Pre-configured AI roles that specialize the translation for specific domains and content types.

**Built-in Roles**:
- Medical Translation Specialist
- Legal Translation Specialist
- Patent Translation Specialist
- Financial Translation Specialist
- Gaming & Entertainment Specialist
- Marketing & Creative Translation
- Cryptocurrency & Blockchain Specialist

**How it works**:
1. Open Unified Prompt Library (Ctrl+P)
2. Browse System Prompts tab
3. Select a specialist role
4. AI adopts that expertise during translation

**Example - Medical Specialist**:
- Understands medical terminology
- Preserves Latin terms correctly
- Uses appropriate clinical language
- Follows medical translation conventions
- Recognises drug names and procedures

**Custom System Prompts**:
- Create your own specialist roles
- Save to `user data/System_prompts/`
- Use template variables: `{source_lang}`, `{target_lang}`
- Combine with Custom Instructions for maximum control

### Tracked Changes Analysis (v2.5.0-CLASSIC)

**What is it?**  
Load DOCX files containing Microsoft Word tracked changes to extract editing patterns and provide AI with your editing style preferences.

**How it works**:
1. Load DOCX file(s) with tracked changes: `Resources > Load Tracked Changes`
2. Supervertaler extracts before→after pairs
3. Analyzes editing patterns (corrections, style changes, terminology preferences)
4. Provides relevant patterns to AI during translation
5. AI learns your editing style and applies it proactively

**Example patterns**:
- "utilize" → "use" (prefer simple words)
- "in order to" → "to" (conciseness)
- "grey" → "gray" (spelling preference)
- Technical term corrections
- Style and tone adjustments

**Reports**:
- HTML and Markdown reports generated
- Shows all extracted change pairs
- Statistics on editing patterns
- Saved to `user data/` folder

**Benefits**:
- ✅ AI learns your editing style
- ✅ Fewer corrections needed
- ✅ Consistent application of preferences
- ✅ Saves time on post-editing
- ✅ Perfect for repeat clients

### Auto-Export Options (v3.x only)

**What is it?**  
Automatically export translation results in multiple formats after translation completes.

**Available formats**:
- **Session Reports** (MD/HTML): Translation statistics, timing, cost estimates
- **TMX**: Translation memory exchange format
- **TSV**: Tab-separated values (spreadsheet-compatible)
- **XLIFF**: XML Localization Interchange File Format
- **Excel**: XLSX spreadsheet with source/target columns

**How to configure**:
1. Open Project Settings (Ctrl+,)
2. Navigate to Export Settings tab
3. Check formats you want auto-exported
4. Set export options (include metadata, statistics, etc.)
5. Exports happen automatically after each translation

**Benefits**:
- ✅ No manual export steps
- ✅ Multiple formats for different uses
- ✅ Automatic backup in various formats
- ✅ Ready for different CAT tools and systems
- ✅ Compliance with client delivery requirements

### Status Tracking

**What is it?**  
Track the translation progress of each segment with visual indicators.

**Status levels**:
- **✗ Untranslated** (Red): Segment not yet translated
- **~ Draft** (Orange): Machine-translated or initial draft
- **✓ Translated** (Green): Human-reviewed and approved
- **✓✓ Approved** (Dark Blue): Final approved, ready for delivery
- **🔒 Locked** (Blue): Locked, cannot be edited (protected segments)

**How to use**:
- Change status: Right-click segment → Change Status
- Keyboard shortcut: Ctrl+T (cycles through statuses)
- Bulk status change: Select multiple segments → Ctrl+T
- Visual overview: Status column shows colored icons

**Workflow example**:
1. Import document → All segments "Untranslated" (✗)
2. Translate with AI → Status changes to "Draft" (~)
3. Review and edit → Change to "Translated" (✓)
4. Final QA → Change to "Approved" (✓✓)
5. Protect segments → Lock them (🔒)

### Find & Replace

**What is it?**  
Search through source and target segments, with regex support and scope filtering.

**Features**:
- Text search in source or target
- Regular expression (regex) support
- Case-sensitive option
- Whole word matching
- Replace single or Replace All
- Scope: Current page, All pages, Selected segments only

**Use cases**:
- Find terminology to check consistency
- Replace client name throughout document
- Find formatting markers
- Search for specific patterns (dates, numbers, codes)
- Quality assurance checks

**Keyboard shortcut**: Ctrl+F

### Grid Pagination (v3.x only)

**What is it?**  
Display segments in pages of 50 (configurable) instead of loading entire document at once.

**Benefits**:
- ⚡ **10x faster loading**: Large documents (1000+ segments) load instantly
- 💾 **Memory efficient**: Only current page in memory
- 🎯 **Better focus**: Work on manageable chunks
- ⚙️ **Configurable**: Adjust page size in settings

**Navigation**:
- Previous/Next page buttons
- Jump to page number
- Page indicator: "Page 3 of 20 (101-150 of 1000 segments)"
- Keyboard shortcuts: Alt+Left (previous), Alt+Right (next)

**Smart features**:
- Multi-selection works across current page
- Search works across all pages
- Statistics calculated for full document
- Export includes all pages

---

## Technical Questions

### What AI models are supported?

**OpenAI**:
- GPT-4 (0613, latest)
- GPT-4 Turbo (0125-preview, latest)
- GPT-4o (newest flagship model)

**Anthropic Claude**:
- Claude 3.5 Sonnet (most popular)
- Claude 3 Opus (highest capability)
- Claude 3 Sonnet
- Claude 3 Haiku (fastest, most economical)

**Google Gemini**:
- Gemini 1.5 Pro (latest)
- Gemini 1.5 Flash (cost-effective)
- Gemini Pro

**Recommendations**:
- **Best Quality**: Claude 3.5 Sonnet, GPT-4o, Claude 3 Opus
- **Best Value**: Gemini Flash, Claude 3 Haiku
- **Best Context**: Gemini 1.5 Pro (2M token context window)

### How does context provision work?

Supervertaler provides AI with **multiple layers of context**:

1. **Full Document Context**: Entire source document text (not just current sentence)
2. **Translation Memory**: Fuzzy matches from TMX files
3. **Custom Instructions**: Project-specific guidelines
4. **System Prompt**: Domain specialist role (medical, legal, patent, etc.)
5. **Tracked Changes**: Editing patterns from previous work
6. **Image Context** (v2.5.0-CLASSIC): Technical drawings and figures
7. **Segment Metadata**: Type, style, neighboring segments

**Why this matters**:
- AI understands document flow and terminology
- Maintains consistency throughout translation
- Adapts to your specific style and preferences
- Reduces ambiguity and improves accuracy
- Specialized domain knowledge applied

### What file formats are supported?

**Import formats**:
- **DOCX**: Microsoft Word documents
- **Bilingual DOCX**: CafeTran and memoQ formats
- **TXT**: Plain text (paragraph-based or line-based)
- **TMX**: Translation memory exchange format
- **TSV**: Tab-separated values
- **JSON**: Project files with segment data

**Export formats**:
- **DOCX**: Microsoft Word documents (with formatting)
- **Bilingual DOCX**: CafeTran (pipes as BOLD+RED), memoQ (formatted tables)
- **TMX**: Translation memory export
- **TSV**: Spreadsheet-compatible export
- **XLIFF**: XML localization format
- **Excel** (XLSX): Spreadsheet with metadata (v3.x only)
- **MD/HTML**: Session reports with statistics

### How is formatting preserved?

**CafeTran (AI-Based)**:
- Pipe symbols `|text|` mark formatted sections
- AI contextually places pipes in translation
- Handles word reordering intelligently
- Exported with pipes as BOLD + RED for visibility
- Reimport to CafeTran preserves formatting

**memoQ (Programmatic)**:
- Bold, italic, underline tracked algorithmically
- Character-level formatting extracted before translation
- Translation occurs on clean text
- Formatting reapplied to translation using alignment
- 100% accuracy on bold/italic/underline preservation

**Standard DOCX**:
- Paragraph styles preserved
- Basic formatting (bold, italic) maintained where possible
- Complex formatting may require manual review

### Can I use Supervertaler offline?

**No** - Supervertaler requires:
- Internet connection for AI API calls (OpenAI, Claude, Gemini)
- Active API keys with credit/subscription

**Why online-only**:
- AI models run on provider servers (OpenAI, Anthropic, Google)
- No local AI models supported currently
- Context and processing require cloud AI infrastructure

**Future consideration**:
- Local model support (Ollama, LM Studio) possible in future versions
- Would enable offline usage with reduced capability
- Not currently implemented

---

## Workflow & Integration

### How do I integrate Supervertaler with my CAT tool?

**Method 1: Bilingual DOCX (Recommended)**
1. **In your CAT tool** (memoQ, CafeTran): Export bilingual DOCX
2. **In Supervertaler**: Import bilingual DOCX → Translate → Export bilingual DOCX
3. **In your CAT tool**: Reimport translated DOCX
4. **Result**: Segments populated with translations, formatting preserved

**Method 2: TMX Exchange**
1. **In your CAT tool**: Export source segments as TMX
2. **In Supervertaler**: Import TMX → Translate → Export TMX
3. **In your CAT tool**: Import translated TMX
4. **Result**: Target segments loaded into CAT tool project

**Method 3: Copy-Paste**
1. **In your CAT tool**: Copy source segments
2. **In Supervertaler**: Paste into TXT file → Import → Translate → Export
3. **In your CAT tool**: Copy translated segments back
4. **Result**: Translations in CAT tool (manual process)

**Best practice**: Use Method 1 (Bilingual DOCX) for seamless workflow

### What's the typical translation workflow?

**Standard Workflow (v2.5.0-CLASSIC)**:
1. **Prepare**: Gather source document, TM files, drawings (if technical)
2. **Load Resources**: 
   - Load TM files
   - Load drawing images (if applicable)
   - Load tracked changes (if available)
3. **Configure**:
   - Select AI provider and model
   - Choose system prompt (domain specialist)
   - Add custom instructions
4. **Import**: Load source DOCX or bilingual file
5. **Translate**: Click "Translate" → AI processes with all context
6. **Review**: Check translations, make edits
7. **Proofread** (optional): Run proofreading mode for QA
8. **Export**: Export to target format (DOCX, TMX, etc.)
9. **Deliver**: Send to client or reimport to CAT tool

**CAT Editor Workflow (v3.7.0)**:
1. **Start**: Launch → Start Screen → Choose action
2. **Import**: Import bilingual or DOCX file
3. **Configure**: AI settings, prompts, TM
4. **Translate**: Select segments → Translate (Ctrl+T)
5. **Edit**: Inline editing in Grid View
6. **Review**: Switch to Document View for readability check
7. **QA**: Use Find & Replace, check consistency
8. **Approve**: Change status to "Approved" (✓✓)
9. **Export**: Auto-export enabled formats generated
10. **Save Project**: Project saved with all context and progress

### How do I handle large documents?

**v2.5.0-CLASSIC**:
- Chunk size setting (default: 20 segments per API call)
- Reduce chunk size for very large documents
- Use batch processing with progress monitoring
- Save progress periodically (automatic)

**v3.7.0**:
- Grid pagination: 50 segments per page
- Translate page-by-page for control
- Or translate all with progress tracking
- Memory efficient: Only current page loaded
- Save project to preserve progress

**Best practices**:
- Split very large documents (>5000 segments) into sections
- Use pagination to focus on manageable chunks
- Save project frequently
- Consider API rate limits and costs for huge documents
- Process overnight for very large projects

### Can I customize the AI prompts?

**Yes!** Multiple customization levels:

**Level 1: Custom Instructions** (Simplest)
- Plain English guidelines
- Project-specific rules
- No technical knowledge needed
- Example: "Use formal tone and British spelling"

**Level 2: System Prompts** (Advanced)
- Define AI role and expertise
- Use template variables (`{source_lang}`, `{target_lang}`)
- Create domain specialists
- Example: "You are a medical translator specialized in {source_lang} to {target_lang} clinical trials"

**Level 3: Edit Source Code** (Expert)
- Modify agent prompt templates in Python code
- Change context structure
- Add custom processing logic
- Requires Python programming knowledge

**Unified Prompt Library (Ctrl+P)**:
- Browse and edit all prompts in one interface
- System Prompts + Custom Instructions tabs
- Create new prompts with visual editor
- Test different prompts on same content

---

## Data Privacy & Confidentiality

**IMPORTANT**: This section addresses the critical concern many professional translators have about using any online translation tool, especially when handling confidential client documents.

### Is my data safe when using Supervertaler?

**Short Answer**: It depends on what you mean by "safe":

**✅ Supervertaler itself**:
- Runs entirely on YOUR computer (no Supervertaler company server)
- No data collection, telemetry, or analytics
- Fully open source (code is auditable)
- API keys never stored or transmitted by Supervertaler
- Translation memory, glossaries, custom instructions stay 100% local

**⚠️ When using external LLM APIs**:
- Your text MUST reach the LLM provider's servers (that's how AI translation works)
- This is unavoidable if you want to use GPT-4, Claude, or Gemini
- You're trusting the LLM provider's data handling practices
- This is different from offline/local translation tools

### When I click "Translate," what exactly happens to my data?

**Step-by-step process**:

1. **You select text** in Supervertaler
2. **Context is gathered** locally:
   - The text you selected
   - Relevant TM matches (from YOUR local TM file)
   - Custom instructions and prompts
   - Document context if enabled
3. **Formatted request is created** locally
4. **Request sent to LLM provider** via HTTPS (encrypted)
   - OpenAI servers receive: `{source_text, system_prompt, instructions, optional_context}`
   - Anthropic servers receive: `{source_text, system_prompt, instructions, optional_context}`
   - Google servers receive: `{source_text, system_prompt, instructions, optional_context}`
5. **AI generates translation** on provider's infrastructure
6. **Response returned** to your computer via HTTPS
7. **Translation stored locally** (NOT on Supervertaler's server)

**Critical Point**: Steps 4-6 mean your content briefly exists on the provider's systems. This is the tradeoff for using powerful cloud-based AI.

### What do the LLM providers do with my data?

**OpenAI (GPT-4, GPT-4o)**:
- **Default**: API data NOT used for training or model improvement
- **Enterprise plans**: Explicit zero-retention guarantees available
- **Data Processing Agreement**: Available for business customers
- **Compliance**: SOC 2 Type II, GDPR compliant
- **Your responsibility**: Review their terms, ensure enterprise plan if needed

**Anthropic (Claude)**:
- **Default**: API data NOT used for training
- **Policy**: Explicit "no data retention for training" commitment
- **Compliance**: SOC 2 Type II compliant
- **Enterprise**: Data processing agreements available
- **Best for confidentiality**: Generally considered most privacy-friendly

**Google Generative AI**:
- **Default**: Privacy practices vary by product
- **Enterprise plans**: Enhanced data protection available
- **Compliance**: SOC 2, GDPR options available
- **Your responsibility**: Verify your chosen Google product's specific terms

**All providers**:
- Comply with data residency requirements (GDPR, regional laws)
- Offer data processing agreements (DPAs) for business users
- Have documented security practices (HTTPS encryption, data centers)
- Support SOC 2 Type II or equivalent compliance

### What should I do for NDA/Confidential Work?

**If you're translating under NDA or with strictly confidential documents:**

**Recommended approach** (Required by most translation agencies for AI):

1. **Use Enterprise/Business Plans**
   - Most AI providers have specific enterprise products
   - Much stricter data protection than consumer/developer API
   - Often include zero-retention guarantees

2. **Get a Data Processing Agreement (DPA)**
   - Signed agreement with the LLM provider
   - Specifies data handling, retention, usage
   - Usually available through enterprise accounts
   - Shows your client you took data protection seriously

3. **Verify Key Guarantees**:
   - ✓ Zero data retention (data deleted after processing)
   - ✓ No use for training or model improvement
   - ✓ No use for other purposes
   - ✓ Data not shared with third parties
   - ✓ Secure transmission (HTTPS)
   - ✓ Encryption at rest (if applicable)

4. **Document Your Setup**
   - Keep copy of DPA with your records
   - Document which AI provider you're using
   - Note: You can use different providers for different projects
   - Share relevant parts with your client (privacy-focused ones appreciate this)

5. **Alternative for Maximum Confidentiality**:
   - Use only local/offline translation components
   - This means NOT using AI translation (since all major AI requires cloud transmission)
   - Use Supervertaler for TM, glossary, and CAT tool integration only
   - Do translation with your own local translation engine (if available)

### Are there any tools that keep data completely local?

**For AI Translation**: 
- ❌ **No major LLM platform keeps AI models running locally** (as of October 2025)
- Even "local" AI applications typically need cloud connectivity for actual translation
- This is because GPT-4, Claude, Gemini are only available on providers' servers
- Running large language models locally requires significant hardware and is impractical for most users

**Partial solutions**:
- **Local TM + Manual Translation**: Use Supervertaler's local TM with your own translations (no AI)
- **Offline TM Tools**: Many traditional CAT tools have fully local operation
- **Future**: Open-source local LLMs may improve, but current ones are significantly weaker than GPT-4/Claude

**For Most Professional Translators**:
- Accept that modern AI translation requires cloud transmission
- Get proper data processing agreements in place
- Use enterprise/business API plans for confidential work
- This is industry standard now (not specific to Supervertaler)

### How do I protect my data when using Supervertaler with AI?

**Best Practices**:

1. **API Key Security**:
   - ✓ Keep `api_keys.txt` secure (don't share, not in version control)
   - ✓ Regenerate keys if accidentally exposed
   - ✓ Use separate API keys for different projects (if needed)
   - ✓ Monitor API key usage/costs regularly

2. **Document Handling**:
   - ✓ Don't store confidential originals in Supervertaler projects
   - ✓ Delete projects/documents after delivery
   - ✓ Keep `user data/` folder secure (local disk encryption recommended)
   - ✓ Separate projects: One folder per client for organization

3. **Translation Memory**:
   - ✓ TM files stay 100% local
   - ✓ Don't share TM files with cloud services
   - ✓ Back up TM securely (encrypted if on cloud storage)
   - ✓ Treat TM as confidential (it contains all your work)

4. **Provider Selection**:
   - ✓ Choose Anthropic or OpenAI for strongest privacy defaults
   - ✓ Use enterprise plans for confidential work
   - ✓ Get written DPA from provider
   - ✓ Review provider's security practices

5. **Organizational Level**:
   - ✓ Document your data protection process
   - ✓ Communicate with clients about your AI usage and safeguards
   - ✓ Keep copies of relevant DPAs
   - ✓ Update privacy policies if you're an agency

### Can I tell my clients I use Supervertaler?

**Yes, and here's how to present it professionally**:

**What to say**:
- "I use professional AI-powered translation assistance (GPT-4 / Claude / Gemini) as part of my quality assurance and productivity process"
- "All AI translations are reviewed by me before delivery"
- "AI is used within secure enterprise data processing agreements"
- "Your data is protected by [Provider Name] enterprise data processing agreement"
- "No data is retained or used for training by the AI provider"

**What NOT to say**:
- ❌ "I use free/online translation tools" (implies lower quality, risky data handling)
- ❌ "I use Supervertaler" (clients don't know what it is, creates uncertainty)
- ❌ "My data might be used for AI training" (scary, inaccurate)

**Practical tip**:
- Many modern translation clients actually WANT you using AI (when properly secured)
- Demonstrates productivity and modern workflow
- Shows quality assurance capability
- Clients appreciate transparency + proper safeguards

### What about GDPR and other regulations?

**GDPR Compliance (EU)**:
- If translating EU personal data, GDPR applies
- LLM providers must have GDPR-compliant Data Processing Agreements
- Both OpenAI, Anthropic, Google offer GDPR-compliant enterprise plans
- You need a DPA signed before processing personal data

**Other Regulations**:
- **HIPAA** (US healthcare): Must use HIPAA-compliant AI provider plan
- **PCI-DSS** (payment data): Use PCI-compliant provider plans
- **CCPA** (California privacy): Similar to GDPR, need proper agreements

**What to do**:
1. Identify applicable regulations for your work
2. Verify LLM provider supports that regulation
3. Get proper enterprise plan + DPA
4. Document your compliance process
5. Keep records for audit purposes

### This seems complicated. What's the real bottom line?

**For translators**:

**If working with general/public-domain content**:
- Standard OpenAI/Anthropic API + default terms = fine
- No special precautions needed beyond basic API key security
- Cost-effective solution

**If working with client confidential content**:
- Must use enterprise API plan + Data Processing Agreement
- Takes 15-30 minutes to set up
- Protects you AND your client
- Allows you to use AI professionally without legal risk

**If working with heavily regulated content** (healthcare, legal, finance):
- Need regulation-specific enterprise plan (HIPAA, legal compliance, etc.)
- Longer setup (provider verification, agreement review)
- Worth it for client relationships and legal protection

**If working with highly secret/military/government classified**:
- ❌ Cannot use cloud AI at all
- Use only offline/local tools
- This is extremely rare in translation work

**For 95% of freelance translators**:
- Set up enterprise plan with Anthropic or OpenAI (15 min)
- Get DPA (if working with client confidential data)
- Use confidently = better workflow, faster delivery, competitive advantage

---

## Troubleshooting

### Why is translation slow?

**Common causes**:
1. **Large chunk size**: Reduce chunk size in settings (default: 20 → try 10)
2. **Provider rate limits**: Some providers throttle requests
3. **Model choice**: Slower models (GPT-4, Claude Opus) take longer
4. **Large context**: Full document + TM + images = more tokens = slower
5. **Internet speed**: Slow connection affects API response time

**Solutions**:
- Use faster models (Gemini Flash, Claude Haiku)
- Reduce chunk size
- Disable unnecessary context sources
- Switch to better internet connection
- Consider batch processing overnight

### API errors - what do they mean?

**"Invalid API Key"**:
- Check `api_keys.txt` for typos
- Ensure key format is correct (starts with `sk-` for OpenAI/Claude)
- Verify key is active on provider dashboard
- Check key has not expired

**"Rate Limit Exceeded"**:
- Too many requests in short time
- Wait a few minutes before retrying
- Reduce chunk size to make fewer requests
- Upgrade API plan for higher limits

**"Context Length Exceeded"**:
- Document + context too large for model
- Reduce chunk size
- Disable image context if not needed
- Use model with larger context window (Gemini 1.5 Pro: 2M tokens)

**"Insufficient Credits"**:
- API account out of credits
- Add funds to provider account
- Check billing settings on provider dashboard

### Formatting is lost in export

**CafeTran**:
- Ensure pipe symbols `|text|` are preserved in target
- Check export uses "☕ Export to CafeTran DOCX" button (not generic export)
- Verify pipes appear as BOLD + RED in exported file
- If pipes missing, AI may have removed them - edit manually

**memoQ**:
- Use "📊 Export to memoQ DOCX" button (not generic export)
- Check source DOCX had formatting to begin with
- Formatting only preserved if present in original
- Manual formatting may be needed for complex styles

**General**:
- Some formatting may not survive translation (by design)
- Review exported file before reimporting to CAT tool
- Keep backup of original source file
- Report formatting issues on GitHub for investigation

### Program crashes or freezes

**Immediate solutions**:
- Force quit and restart program
- Check for unsaved work (projects auto-save periodically)
- Review log panel for error messages before crash

**Preventing future crashes**:
- Update Python to latest version
- Update libraries: `pip install --upgrade openai anthropic google-generativeai pillow python-docx openpyxl`
- Reduce chunk size for large documents
- Close other programs to free memory
- Check for antivirus interference
- Report crash with error message on GitHub Issues

**Data recovery**:
- Check `user data/Projects/` for auto-saved project
- Check `user data/` for exported files (TMX, session reports)
- Source files are never modified (always safe)

### How do I report a bug?

1. **Gather information**:
   - Supervertaler version (v2.5.0-CLASSIC or v3.7.0)
   - Python version (`python --version`)
   - Operating system and version
   - Error message (from log panel or console)
   - Steps to reproduce the bug

2. **GitHub Issues**:
   - Visit [github.com/michaelbeijer/Supervertaler/issues](https://github.com/michaelbeijer/Supervertaler/issues)
   - Click "New Issue"
   - Provide detailed description with info from step 1
   - Attach relevant files if possible (sanitize sensitive content)

3. **Expected behavior**:
   - Describe what you expected to happen
   - Describe what actually happened
   - Include screenshots if UI-related

**Response time**: Typically 1-3 days, depending on complexity

---

## Development & History

### Why was Supervertaler created?

**Origins**:
- Michael Beijer needed better AI integration for professional translation work
- Existing CAT tools had limited or expensive AI plugins
- Wanted flexible multi-provider AI access (OpenAI, Claude, Gemini)
- Needed custom prompt control and multiple context sources
- Desired seamless workflow with existing CAT tools (memoQ, CafeTran)

**Goals**:
- **Context-aware translation**: Not just sentence-by-sentence machine translation
- **Professional control**: Inline editing, status tracking, project management
- **Flexibility**: Multiple AI providers, customizable prompts
- **Integration**: Work with existing CAT tools, not replace them
- **Open source**: Share with translation community
- **AI-assisted development**: Demonstrate human-AI collaboration potential

### What's the development history?

**Phase 1: Prototype (v1.0.0 - Early 2025)**:
- Basic DOCX import/export
- OpenAI GPT-4 translation
- Simple GUI with tkinter
- Proof of concept for context-aware translation

**Phase 2: Production (v1.x - v2.x, Jan-Aug 2025)**:
- Multi-provider support (OpenAI, Claude, Gemini)
- Translation memory integration
- CafeTran bilingual DOCX support (v2.4.3)
- memoQ bilingual DOCX support (v2.4.3)
- Tracked changes analysis
- Image context for technical documents
- Proofreading mode
- Stable production-ready releases

**Phase 3: CAT Editor Release (v3.x, Sep-Oct 2025)**:
- Complete architectural rewrite as segment-based CAT editor
- Professional UI with Grid, List, Document views
- Grid pagination for large documents
- Multi-selection system
- Status icons and tracking
- Auto-export options
- Unified prompt library
- Start Screen with project management
- v3.7.0 released as stable production version

**Current Status** (October 2025):
- v2.5.0-CLASSIC: Stable, production-ready, recommended for legacy workflows
- v3.7.0: Stable production release with latest features and CAT editor

**Future Plans**:
- Quality assurance tools
- Advanced statistics and reporting
- Potential local AI model support
- More CAT tool integrations

### Why is it open source?

**Reasons**:
1. **Community benefit**: Share with professional translators worldwide
2. **Transparency**: Open development process, no hidden functionality
3. **Collaboration**: Contributions from developers and translators welcome
4. **Learning**: Demonstrate AI-assisted software development
5. **Flexibility**: Users can modify and adapt to their needs
6. **Trust**: Code is inspectable, no data collection concerns

**License**: [Check LICENSE file in repository]

**Contributions welcome**:
- Bug reports and feature requests (GitHub Issues)
- Code contributions (Pull Requests)
- Documentation improvements
- Translation of UI to other languages
- Testing and feedback

### Why the name "Supervertaler"?

**Etymology**:
- Dutch language play on words
- "Vertaler" = "translator" in Dutch
- "Super" = "super/excellent" (English prefix)
- "Supervertaler" ≈ "Super Translator"

**Pronunciation**:
- Dutch: "SOO-per-fer-TAH-ler"
- English speakers: "SUPER-ver-TAY-ler" (close enough!)

**Branding**:
- Memorable and unique
- Reflects Dutch origin (Michael is based in Netherlands)
- International appeal (mix of English + Dutch)
- Tech-savvy without being too serious

---

## Miscellaneous

### Is my translation data private?

**Data flow**:
- Source text sent to AI provider (OpenAI, Anthropic, Google) for translation
- Translations received from AI provider
- No data sent to Supervertaler developers or third parties

**Privacy considerations**:
- **API providers**: Check their data retention policies
  - OpenAI: Does not train on API data (per policy as of 2025)
  - Anthropic: Does not train on API data (per policy)
  - Google: Check current Gemini API terms
- **Local storage**: All projects, TMs, and data stored locally on your computer
- **No telemetry**: Supervertaler does not collect usage data or analytics
- **Open source**: Code is public, verify no hidden data collection

**Best practices for sensitive content**:
- Review AI provider terms of service
- Use providers with strong privacy commitments
- Consider anonymizing sensitive client names, personal data
- For highly confidential work, consult with legal/compliance
- Keep local backups of all source and translated files

### Can I use Supervertaler commercially?

**Yes!** Supervertaler is designed for professional commercial translation work.

**Requirements**:
- Own valid API keys for AI providers (personal or business account)
- Comply with AI provider terms of service
- Respect open source license terms

**Recommended for**:
- Freelance translators
- Translation agencies
- Corporate translation departments
- Language service providers

**Not allowed** (per open source license):
- Reselling Supervertaler as your own product
- Removing author attribution
- [Check specific license terms in LICENSE file]

### How can I support the project?

**Ways to contribute**:

1. **Use it and provide feedback**: Test features, report bugs, suggest improvements
2. **Star the GitHub repository**: Increases visibility
3. **Share with colleagues**: Help other translators discover Supervertaler
4. **Contribute code**: Submit Pull Requests with new features or fixes
5. **Improve documentation**: Fix typos, add examples, translate docs
6. **Report bugs**: Detailed bug reports help improve quality
7. **Donate** (if Michael sets up donations): Support continued development

**Best contribution**: Use Supervertaler professionally and report your experience!

### Where can I learn more?

**Documentation**:
- `README.md`: Overview and feature list
- `USER_GUIDE.md`: Step-by-step usage guide for v2.5.0-CLASSIC
- `CHANGELOG.md`: Version history overview
- `CHANGELOG-CLASSIC.md`: v2.x detailed changelog
- `INSTALLATION.md`: Setup instructions
- `.dev/docs/`: Technical documentation and feature guides

**Online**:
- **GitHub**: [github.com/michaelbeijer/Supervertaler](https://github.com/michaelbeijer/Supervertaler)
- **Website**: [michaelbeijer.co.uk](https://michaelbeijer.co.uk/)
- **Blog post**: [michaelbeijer.co.uk/what_i_look_for_in_a_cat_tool](https://michaelbeijer.co.uk/what_i_look_for_in_a_cat_tool)

**Community**:
- GitHub Issues: Questions, bug reports, feature requests
- GitHub Discussions: General discussion, tips, workflows
- [Add other community channels if/when they exist]

### What's next for Supervertaler?

**Short-term (v3.8.0+)**:
- Enhanced quality assurance tools
- More auto-export formats
- Performance optimizations
- Bug fixes and improvements

**Medium-term (v4.0+)**:
- Terminology management (glossaries)
- Advanced statistics and reporting
- Better TMX management (search, filter, edit)
- More CAT tool integrations (Trados, Wordfast)
- Collaboration features (team projects)

**Long-term (v5.0+)**:
- Local AI model support (Ollama, LM Studio)
- Cloud sync for projects and TMs
- Mobile companion app
- Plugin system for extensions
- Translation memory suggestion ranking

**Experimental ideas**:
- Voice input for segment editing
- Real-time collaboration
- Automated quality checks
- MT post-editing workflows
- Integration with translation marketplaces

**Community-driven**: Feature prioritization based on user feedback and requests!

---

## Need More Help?

**Still have questions?**

1. **Check documentation**: README, USER_GUIDE, changelogs
2. **Search GitHub Issues**: Someone may have asked before
3. **Open new GitHub Issue**: Detailed questions get detailed answers
4. **GitHub Discussions**: General questions and community help

**Found a bug or want a feature?**  
→ [Open an issue on GitHub](https://github.com/michaelbeijer/Supervertaler/issues)

**Want to contribute?**  
→ [Check CONTRIBUTING.md](https://github.com/michaelbeijer/Supervertaler/CONTRIBUTING.md) (if exists)

---

*Last updated: October 19, 2025*  
*Supervertaler v3.7.0 (Latest Stable Release) / v2.5.0-CLASSIC*  
*Created by Michael Beijer with AI assistance*
