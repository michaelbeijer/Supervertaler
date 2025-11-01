# PDF Rescue - Multi-Provider AI Vision OCR & Text Extraction

## Overview

PDF Rescue is a dual-mode PDF text extraction tool that intelligently handles both image-based and text-based PDFs:

- **OCR Mode**: AI-powered vision OCR for scanned/image-based PDFs
- **Text Extraction Mode**: Fast, accurate direct text extraction from accessible PDFs

## Processing Modes

### 🤖 OCR Mode (Image-Based PDFs)

**When to use:**
- Scanned documents
- PDFs created from images
- Screenshots saved as PDF
- PDFs with no selectable text
- Poorly formatted PDFs where text extraction fails

**How it works:**
1. Converts PDF pages to 300 DPI images
2. Sends images to AI vision model (OpenAI/Claude/Gemini)
3. AI extracts and structures the text
4. Supports formatting preservation and multi-column layouts

**Pros:**
- Works on any PDF, even pure images
- Can handle complex layouts, tables, columns
- Preserves formatting (bold, italic, underline)
- Fixes poor formatting in original

**Cons:**
- Uses API credits (costs money)
- Slower than text extraction
- Can have occasional AI hallucinations
- Requires good image quality

### 📄 Text Extraction Mode (Accessible PDFs)

**When to use:**
- PDFs with selectable text
- Digital PDFs (not scanned)
- PDFs exported from Word, InDesign, etc.
- When you need 100% accuracy
- When you want instant results

**How it works:**
1. Opens PDF and reads embedded text directly
2. Extracts text from each page
3. No AI processing needed

**Pros:**
- ✅ **FREE** - no API costs
- ✅ **FAST** - instant extraction
- ✅ **ACCURATE** - no hallucinations, exact text
- ✅ **PRESERVES** - keeps original text exactly
- ✅ **SIMPLE** - one-click extraction

**Cons:**
- Only works if PDF has embedded text
- No formatting preservation
- No layout restructuring
- Won't work on scanned documents

## Usage

### Quick Start

1. **Select Mode**:
   - **OCR Mode**: For scanned/image PDFs
   - **Text Extraction**: For PDFs with selectable text (try selecting text in PDF viewer first)

2. **Import PDF**:
   - Click "📄 Import PDF"
   - In **OCR Mode**: Creates 300 DPI images for AI processing
   - In **Text Mode**: Extracts text directly

3. **Process**:
   - **OCR Mode**: Click "Process All" to send to AI (uses API credits)
   - **Text Mode**: Already extracted! Skip to export.

4. **Export**:
   - Click "💾 Export Markdown & Word"
   - Saves as .md and .docx files

### Choosing the Right Mode

**Not sure which mode? Try this:**

1. Open your PDF in a PDF viewer
2. Try to select some text with your mouse
3. **If you can select text** → Use **Text Extraction Mode** (faster, free, accurate)
4. **If you can't select text** → Use **OCR Mode** (image-based PDF)

## Supported Providers

### OpenAI (GPT-4 Vision)
- **Models**: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-5
- **Strengths**: 
  - Excellent instruction following
  - Strong at structured text extraction
  - Fast processing
- **Cost**: Moderate to high
- **Best for**: General-purpose OCR, mixed content

### Anthropic Claude (Vision)
- **Models**: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022, claude-3-opus-20240229
- **Strengths**:
  - **Lowest hallucination rate** - highly accurate
  - Excellent at complex layouts
  - Superior table/multi-column handling
  - Very precise instruction following
- **Cost**: Moderate
- **Best for**: Technical documentation, complex layouts, accuracy-critical work

### Google Gemini (Vision)
- **Models**: gemini-2.0-flash-exp, gemini-1.5-pro-002, gemini-1.5-flash-002
- **Strengths**:
  - Strong layout understanding
  - Competitive accuracy
  - Larger context windows
  - **Lower cost** than competitors
- **Cost**: Low to moderate
- **Best for**: Batch processing, budget-conscious projects, multi-page documents

## Setup

### 1. Install Required Packages

```powershell
# OpenAI (already installed)
pip install openai

# Anthropic Claude
pip install anthropic

# Google Gemini
pip install google-generativeai pillow
```

### 2. Add API Keys

Edit `user data_private/api_keys.txt` (or `api_keys.txt` in production):

```
# OpenAI
openai=sk-your-openai-key-here

# Anthropic Claude
claude=sk-ant-your-claude-key-here

# Google Gemini
gemini=your-gemini-key-here
```

Get keys from:
- **OpenAI**: https://platform.openai.com/api-keys
- **Claude**: https://console.anthropic.com/settings/keys
- **Gemini**: https://aistudio.google.com/app/apikey

### 3. Restart Supervertaler

The PDF Rescue tab will automatically detect available providers and show only the models for which you have API keys configured.

## Usage

1. **Select Model**: Choose from the dropdown (organized by provider)
2. **Import PDF or Images**: Use "📄 Import PDF" or "➕ Add Image Files"
   - **PDF Import**: Automatically converts pages to 300 DPI PNG images (professional quality)
   - **Image Import**: Use your own images (recommend 300+ DPI for best results)
3. **Process**: Click "Process Selected" or "Process All"
4. **Export**: Save to Word document with "Save DOCX"

## Image Quality

### PDF to Image Conversion

When you import a PDF, PDF Rescue extracts pages at **300 DPI (3x zoom)**:
- **Resolution**: Professional print quality
- **Format**: PNG (lossless compression)
- **Color**: RGB (no alpha channel for smaller files)
- **Optimized for**: AI vision models (OpenAI, Claude, Gemini)

**Why 300 DPI?**
- AI models perform best with clear, high-resolution text
- Reduces hallucinations and character substitution errors
- Professional quality suitable for client deliverables
- Balances quality vs. file size/processing time

### Recommended Image Quality

For best OCR results:
- **Minimum**: 150 DPI (1200px wide for letter-size page)
- **Recommended**: 300 DPI (2400px wide) - **default for PDF import**
- **Maximum benefit**: 400 DPI (3200px wide)
- **Diminishing returns**: Beyond 400 DPI adds file size but little accuracy gain

**Tips for better quality:**
- Use PDF import instead of screenshots when possible
- If scanning paper: 300 DPI, color or grayscale
- Ensure good contrast between text and background
- Avoid heavy JPEG compression artifacts

## Model Recommendations

### For Maximum Accuracy (Technical Manuals)
**Recommended**: Claude 3.5 Sonnet
- Lowest hallucination rate
- Best for multi-column layouts
- Superior table extraction
- Most accurate with complex formatting

### For Speed & Cost Balance
**Recommended**: Gemini 2.0 Flash or GPT-4o-mini
- Fast processing
- Lower API costs
- Good accuracy for most documents

### For Complex Document Understanding
**Recommended**: GPT-5 or Claude 3 Opus
- Advanced reasoning capabilities
- Best for documents with mixed content types
- Handles unusual layouts well

## Advanced Features

### Multi-Column Layout Detection

All providers support automatic column detection:

```markdown
[START COLUMN 1]
Left column text...
[END COLUMN 1]

[START COLUMN 2]
Right column text...
[END COLUMN 2]
```

The Word export automatically creates a table layout preserving side-by-side columns for CAT tool compatibility.

### Formatting Preservation

Enable "Preserve formatting (bold, italic, underline)" to maintain text styling:
- **Bold text**
- *Italic text*
- __Underlined text__

### Custom Instructions

Modify the extraction instructions for specific document types:
- Technical specifications
- Forms and tables
- Handwritten text
- Mixed language content

## Comparison Mode (Coming Soon)

Process the same document with multiple providers to:
- Compare accuracy
- Identify hallucinations
- Select best result
- Benchmark costs

## API Costs (Approximate)

| Provider | Model | Cost per 1K images* |
|----------|-------|---------------------|
| OpenAI | GPT-4o | $5-10 |
| OpenAI | GPT-4o-mini | $1-2 |
| Claude | 3.5 Sonnet | $4-8 |
| Claude | 3.5 Haiku | $1-3 |
| Gemini | 2.0 Flash | $0.50-1 |
| Gemini | 1.5 Pro | $2-4 |

*Estimates based on typical PDF pages (letter size, moderate content). Actual costs vary by image size and output length.

## Troubleshooting

### "Image quality" or "resolution" warnings
- **If using PDF import**: Images are already at 300 DPI (optimal quality)
- **If importing images**: Check source image resolution
  - Right-click image → Properties → Details → Dimensions
  - For letter-size page: aim for 2400x3000px or larger
  - Re-scan or re-export at higher DPI if needed

### "Client not initialized" Error
- Check that the API key is in `api_keys.txt`
- Verify the key format (claude keys start with `sk-ant-`, gemini keys are alphanumeric)
- Restart Supervertaler after adding keys

### Import Errors
```powershell
# If you see "anthropic library not installed"
pip install anthropic

# If you see "google-generativeai library not installed"
pip install google-generativeai pillow
```

### Poor Accuracy
1. Try Claude 3.5 Sonnet for best accuracy
2. Adjust extraction instructions for document type
3. Pre-process images (higher resolution, better contrast)
4. Use "Preserve formatting" for structured documents

## Development

### Adding New Providers

To add support for additional vision APIs:

1. Update `_initialize_clients()` - add client initialization
2. Add models to dropdown in `create_tab()`
3. Implement `_extract_with_<provider>()` method
4. Update `_get_provider_from_model()` for model detection

## License

Part of Supervertaler by Michael Beijer
https://supervertaler.com/
