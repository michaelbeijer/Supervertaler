# GitHub Release Instructions for Supervertaler v2.4.1

## Step-by-Step Release Process

### 1. Create Distribution Package

First, create a ZIP file of the built application:

```powershell
cd "c:\Users\mbeijer\My Drive\Software\Python\Supervertaler"
Compress-Archive -Path "dist\Supervertaler_v2.4.1" -DestinationPath "Supervertaler_v2.4.1_Windows.zip" -Force
```

This creates `Supervertaler_v2.4.1_Windows.zip` containing:
- `Supervertaler.exe` (main executable)
- `_internal/` folder (contains all dependencies, modules, docs, custom prompts, etc.)

### 2. Go to GitHub Releases

1. Navigate to: https://github.com/michaelbeijer/Supervertaler/releases
2. Click **"Draft a new release"** button

### 3. Configure Release Settings

**Tag version:** `v2.4.1`
- Click "Choose a tag" → Type `v2.4.1` → Click "Create new tag: v2.4.1 on publish"

**Release title:** `Supervertaler v2.4.1 - CafeTran & memoQ Support`

**Target:** `main` (or your current branch if merging PR first)

### 4. Release Description Template

Copy and paste the following into the description field:

---

## 🎉 Supervertaler v2.4.1 - CAT Tool Integration

This release adds comprehensive support for **CafeTran** and **memoQ** bilingual DOCX workflows, enabling professional translators to use AI-powered translation within their preferred CAT tools.

### ✨ New Features

#### CafeTran Bilingual DOCX Support
- **AI-powered formatting preservation** using intelligent pipe symbol placement (`|text|`)
- Seamless import/export workflow for CafeTran bilingual DOCX files
- Automatic detection and preservation of formatting markers
- Tested with 18/18 segments - 100% pipe preservation rate

#### memoQ Bilingual DOCX Support  
- **Programmatic formatting detection** with 60% threshold rule
- Smart preservation of bold, italic, underline, and combined formatting
- Automatic CAT tag preservation for untranslatable elements
- Tested with 27/27 segments - 15/15 formatted segments preserved correctly

#### Enhanced File Format Support
- Import/export for CafeTran bilingual DOCX (`.docx`)
- Import/export for memoQ bilingual DOCX (`.docx`)
- All existing formats remain fully supported (DOCX, XLIFF, TMX, TSV, TXT)

### 📚 Documentation

Comprehensive guides included in this release:

- **[CafeTran Support Guide](https://github.com/michaelbeijer/Supervertaler/blob/main/docs/features/CAFETRAN_SUPPORT.md)** - Complete workflow, formatting logic, troubleshooting
- **[memoQ Support Guide](https://github.com/michaelbeijer/Supervertaler/blob/main/docs/features/MEMOQ_SUPPORT.md)** - Programmatic approach, threshold rules, best practices
- **[Updated README](https://github.com/michaelbeijer/Supervertaler/blob/main/README.md)** - New workflow sections for both CAT tools
- **[CHANGELOG](https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md)** - Full v2.4.1 feature details

### 🔧 Technical Details

**CafeTran Implementation:**
- Uses AI models to intelligently place pipe symbols for formatting markers
- Preserves CafeTran's native bilingual format structure
- Module: `modules/cafetran_docx_handler.py`

**memoQ Implementation:**
- Programmatic analysis with 60% coverage threshold
- Automatic formatting application using python-docx
- Module: `modules/docx_handler.py` (enhanced)

**Supported AI Models:**
- Claude 3.5 Sonnet, Claude 3 Opus, Claude 3.5 Haiku
- GPT-4o, GPT-4o mini, GPT-4 Turbo, o1-preview, o1-mini
- Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash

### 📦 Installation

**Windows (64-bit):**

1. Download `Supervertaler_v2.4.1_Windows.zip` below
2. Extract to a folder of your choice
3. Run `Supervertaler.exe`
4. Enter your API keys on first launch (Claude, OpenAI, and/or Gemini)

**Important Notes:**
- Windows Defender may show a warning (click "More info" → "Run anyway")
- All data files are in the `_internal` folder alongside the executable
- Custom prompts can be added to `_internal/custom_prompts/`
- Documentation is available in `_internal/docs/`

### 🚀 Quick Start - CafeTran Workflow

1. Export bilingual DOCX from CafeTran
2. In Supervertaler: **File** → **Import** → **CafeTran Bilingual DOCX**
3. Translate using AI (segments processed individually)
4. **File** → **Export** → **CafeTran Bilingual DOCX**
5. Import back into CafeTran - formatting preserved automatically!

### 🚀 Quick Start - memoQ Workflow

1. Export bilingual DOCX from memoQ  
2. In Supervertaler: **File** → **Import** → **memoQ Bilingual DOCX**
3. Translate using AI
4. **File** → **Export** → **memoQ Bilingual DOCX**
5. Import back into memoQ with formatting intact!

### 🔄 Upgrade from v2.4.0

This is a feature release with no breaking changes. Simply download and replace your existing installation. Your API keys and custom prompts are stored separately and will be preserved.

### 🐛 Bug Fixes

- Fixed gray placeholder text issue in custom instructions field
- Improved error handling for malformed bilingual DOCX files
- Enhanced segment extraction for complex table structures

### 📝 Full Changelog

See [CHANGELOG.md](https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md) for complete version history.

### 💬 Feedback & Support

Found a bug or have a feature request? Please [open an issue](https://github.com/michaelbeijer/Supervertaler/issues)!

---

### 5. Upload Release Asset

1. Scroll down to **"Attach binaries by dropping them here or selecting them"**
2. Click and select (or drag & drop): `Supervertaler_v2.4.1_Windows.zip`
3. Wait for upload to complete (file size: ~35-40 MB)

### 6. Pre-release or Latest Release?

- **Uncheck** "Set as a pre-release" (this is a stable release)
- **Check** "Set as the latest release" (recommended)

### 7. Publish Release

1. Review all information is correct
2. Click **"Publish release"** button
3. Release is now live at: `https://github.com/michaelbeijer/Supervertaler/releases/tag/v2.4.1`

---

## Post-Release Checklist

After publishing:

- [ ] Verify download link works
- [ ] Test downloaded ZIP extracts properly
- [ ] Confirm executable runs on a clean Windows machine
- [ ] Update README.md if it references "latest version"
- [ ] Announce release (social media, user groups, etc.)
- [ ] Close or update related GitHub issues
- [ ] Merge the PR if release was from a feature branch
- [ ] Start planning v2.5.0 features! 🎉

---

## Troubleshooting

### "GitHub Release Not Showing Up"
- Ensure you clicked "Publish release" (not just "Save draft")
- Check you're viewing the correct repository
- Try refreshing the releases page

### "ZIP File Too Large"
- Current build should be ~35-40 MB
- If larger, you may have debug symbols enabled
- Verify PyInstaller used `strip=False, upx=True` settings

### "Users Report .exe Won't Run"
- Add note about Windows Defender warning (expected behavior)
- Include Visual C++ Redistributable requirement (usually auto-included)
- Recommend checking antivirus logs

---

## Optional Enhancements

### Add Screenshots
Upload screenshots to the release description showing:
- CafeTran workflow in action
- memoQ import/export dialogs
- Main application interface

### Create Release Video
Consider recording a 2-3 minute demo showing:
- CafeTran bilingual workflow
- memoQ bilingual workflow  
- Side-by-side formatting comparison

### Social Media Announcement Template
```
🚀 Supervertaler v2.4.1 is here!

New: CafeTran & memoQ bilingual DOCX support
✅ AI-powered formatting preservation
✅ Seamless CAT tool integration
✅ 100% tested & documented

Download: [GitHub Release Link]

#translation #CATtools #AI
```

---

## Version History

- **v2.4.1** - CafeTran & memoQ support (current release)
- **v2.4.0** - Enhanced XLIFF support
- **v2.3.0** - Multi-model support
- **v2.2.0** - Custom prompts
- **v2.1.0** - TMX import/export
- **v2.0.0** - Major UI overhaul

---

**Last Updated:** October 9, 2025  
**Build Date:** October 9, 2025  
**Python Version:** 3.12.6  
**PyInstaller Version:** 6.16.0
