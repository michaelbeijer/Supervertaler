# GitHub Releases Guide - Supervertaler v2.4.1

**Complete step-by-step guide to publishing your Windows executable on GitHub Releases**

---

## 📦 What You Have Ready

✅ **Distribution Package**: `Supervertaler_v2.4.1_Windows.zip` (52.9 MB)  
✅ **Location**: Project root directory  
✅ **Contents**: Complete executable package with all files  

---

## 🚀 Publishing to GitHub Releases - Step by Step

### Step 1: Navigate to Your GitHub Repository

1. Open your browser
2. Go to: **https://github.com/michaelbeijer/Supervertaler**
3. Make sure you're logged in

### Step 2: Access the Releases Section

1. Click on **"Releases"** in the right sidebar
   - If you don't see it, look for the version number (like "v2.4.0")
   - Or go directly to: **https://github.com/michaelbeijer/Supervertaler/releases**

2. Click **"Create a new release"** button (or "Draft a new release")

### Step 3: Create Release Tag

**Tag version**: `v2.4.1`
- ✅ Use semantic versioning (v + version number)
- ✅ Click "Create new tag: v2.4.1 on publish"
- ✅ Target: `main` branch

### Step 4: Fill in Release Information

**Release Title**: `Supervertaler v2.4.1 - Windows Executable with memoQ Integration`

**Description** (copy this template):

```markdown
## 🎉 Supervertaler v2.4.1 - Standalone Windows Executable

**Major Update**: Direct memoQ bilingual DOCX integration with formatting preservation!

### 🎁 Download for Windows

**No Python required!** Just download, extract, and run.

#### 📥 Installation (3 Easy Steps):

1. **Download** `Supervertaler_v2.4.1_Windows.zip` below
2. **Extract** to your desired location (e.g., `C:\Program Files\Supervertaler` or your Documents folder)
3. **Edit** `api_keys.txt` with your API keys (OpenAI, Anthropic, or Google)
4. **Double-click** `Supervertaler.exe` to launch

📖 **See `INSTALLATION_GUIDE.txt` inside the package for detailed instructions**

---

### ✨ What's New in v2.4.1

#### 🚀 NEW FEATURES

**📄 memoQ Bilingual DOCX Import/Export** (GAME-CHANGER)
- One-click import directly from memoQ
- One-click export back to memoQ
- Perfect for professional translators using CAT tools
- Seamless workflow integration

**🎨 Formatting Preservation** (100% Success Rate)
- **Bold**, *italic*, and <u>underline</u> formatting maintained
- Smart 3-strategy algorithm (threshold, beginning, CAT tag detection)
- Tested on 15/15 segments with perfect results

#### 🔧 Technical Details

- **Supported Format**: memoQ bilingual DOCX (5-column table)
- **Formatting Detection**: 60% threshold with beginning-of-segment detection
- **CAT Tags Preserved**: memoQ `[1}...{2]` format maintained
- **Segment IDs**: Maintained for perfect reimport compatibility

**Coming Soon**: Trados Studio and CafeTran bilingual support

---

### 💻 System Requirements

- **OS**: Windows 10 or Windows 11 (64-bit)
- **Disk Space**: ~200 MB
- **Internet**: Required for AI API calls
- **API Keys**: At least one of:
  - OpenAI (gpt-4o, gpt-4-turbo, etc.)
  - Anthropic Claude (claude-3.5-sonnet, etc.)
  - Google Gemini (gemini-1.5-pro, etc.)

---

### 📚 Getting Started

1. **Get API Keys**:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Google: https://makersuite.google.com/app/apikey

2. **Read Documentation**:
   - `README.md` - Complete feature overview
   - `docs/user_guides/Supervertaler User Guide (v2.4.0).md` - Detailed user guide
   - `docs/user_guides/BILINGUAL_WORKFLOW_QUICK_START.md` - memoQ workflow guide
   - `docs/user_guides/API_KEYS_SETUP_GUIDE.md` - API setup instructions

3. **Try the Bilingual Workflow**:
   - Export bilingual DOCX from memoQ
   - Import to Supervertaler (green button)
   - Configure and translate
   - Export back (blue button)
   - Reimport to memoQ

---

### 🔒 Security Notes

**Windows SmartScreen Warning**:
If Windows shows a security warning when running `Supervertaler.exe`:
1. Click **"More info"**
2. Click **"Run anyway"**

This is normal for new applications without an expensive code-signing certificate. The executable is safe - you can verify the source code in this repository.

**Your Data**:
- All processing happens locally on your computer
- Only API calls go to AI providers (OpenAI/Anthropic/Google)
- Your API keys stay on your machine
- No telemetry or data collection

---

### 📖 Full Documentation

- **CHANGELOG**: See below for complete version history
- **User Guides**: Included in `docs/user_guides/` folder
- **GitHub**: https://github.com/michaelbeijer/Supervertaler
- **Website**: https://michaelbeijer.co.uk

---

### 🐛 Known Issues

None currently! Report issues at: https://github.com/michaelbeijer/Supervertaler/issues

---

### ⬆️ Upgrading from v2.4.0

1. Download v2.4.1
2. Extract to a new folder
3. Copy your `api_keys.txt` from the old version
4. Copy your projects from `projects/` and `projects_private/`
5. Copy custom prompts from `custom_prompts_private/`

---

### 🙏 Support

- **Issues**: https://github.com/michaelbeijer/Supervertaler/issues
- **Email**: info@michaelbeijer.co.uk
- **Website**: https://michaelbeijer.co.uk

---

### 📊 Package Contents

```
Supervertaler_v2.4.1/
├── Supervertaler.exe (12.4 MB)
├── api_keys.txt (edit with your keys)
├── api_keys.example.txt
├── README.md
├── CHANGELOG.md
├── INSTALLATION_GUIDE.txt
├── custom_prompts/ (8 pre-made prompts)
├── custom_prompts_private/
├── docs/user_guides/
├── projects/
├── projects_private/
└── _internal/ (Python runtime - don't modify)
```

**Total Size**: 154 MB uncompressed, 53 MB ZIP

---

### 📝 CHANGELOG Extract (v2.4.1)

See full CHANGELOG.md in the package or repository.

**Major Features**:
- memoQ bilingual DOCX import/export
- Formatting preservation (bold/italic/underline)
- 100% production-tested

**Bug Fixes**:
- Tab-separated output parsing
- Formatting detection accuracy
- Output file path handling

---

**Thank you for using Supervertaler!** 🎉

If you find this tool useful, please ⭐ star the repository and share with other translators!
```

### Step 5: Upload the Distribution File

1. **Scroll down** to the **"Attach binaries"** section
2. **Drag and drop** or click to upload:
   - `Supervertaler_v2.4.1_Windows.zip`
3. Wait for upload to complete (may take 1-2 minutes for 53 MB)

### Step 6: Set Release Options

- ✅ **Check**: "Set as the latest release"
- ⬜ **Uncheck**: "Set as a pre-release" (this is stable!)
- ⬜ **Uncheck**: "Create a discussion for this release" (optional)

### Step 7: Publish!

1. Click **"Publish release"** button
2. Wait for processing (a few seconds)
3. Your release is now live! 🎉

---

## 🎯 After Publishing

### Immediate Actions

1. **Test the download link**:
   - Go to your Releases page
   - Download the ZIP
   - Extract and test `Supervertaler.exe`

2. **Update README.md** with download link:
   ```markdown
   ## 📥 Download
   
   ### Windows Executable (No Python Required)
   **[Download Supervertaler v2.4.1 for Windows](https://github.com/michaelbeijer/Supervertaler/releases/latest)**
   
   - Size: ~53 MB (compressed), ~154 MB (extracted)
   - System: Windows 10/11 64-bit
   - Just extract and run - no installation needed!
   ```

3. **Share the release**:
   - Twitter/X: "Just released Supervertaler v2.4.1 with memoQ integration! 🎉"
   - LinkedIn: Professional translation community
   - Email: Notify existing users

### Monitor & Respond

- **Check download stats**: GitHub shows download count on Releases page
- **Monitor Issues**: https://github.com/michaelbeijer/Supervertaler/issues
- **Respond to feedback**: Users may report bugs or request features

---

## 📊 Your Release Will Look Like This

**URL**: `https://github.com/michaelbeijer/Supervertaler/releases/tag/v2.4.1`

**What Users See**:
```
Supervertaler v2.4.1 - Windows Executable with memoQ Integration
Released on Oct 8, 2025

[Your description here]

Assets:
✅ Supervertaler_v2.4.1_Windows.zip (52.9 MB)
📦 Source code (zip) - auto-generated by GitHub
📦 Source code (tar.gz) - auto-generated by GitHub

Downloads: [counter will show here]
```

---

## 🔄 For Future Updates

When you release v2.4.2, v2.5.0, etc.:

1. **Build new version**: `python build_executable.py`
2. **Create ZIP**: `Compress-Archive -Path "dist\Supervertaler_vX.X.X" -DestinationPath "Supervertaler_vX.X.X_Windows.zip"`
3. **Create new release** on GitHub with new tag
4. **Upload new ZIP**
5. **Mark as latest release**

**Users automatically see new version** on your Releases page!

---

## 💡 Pro Tips

### Maximize Downloads

1. **Pin to repository top**: GitHub shows latest release prominently
2. **Add badge to README**:
   ```markdown
   ![GitHub release](https://img.shields.io/github/v/release/michaelbeijer/Supervertaler)
   ![Downloads](https://img.shields.io/github/downloads/michaelbeijer/Supervertaler/total)
   ```

3. **Create release notes template**: Save your description format for next release

### Track Success

- **Download stats**: Check Insights → Traffic → Popular content
- **Stars/Forks**: Indicates community interest
- **Issues**: User engagement and feedback

---

## ⚠️ Important Reminders

**Before Publishing**:
- ✅ Test the ZIP file yourself
- ✅ Make sure `api_keys.txt` is empty/example
- ✅ Verify version number in release matches executable
- ✅ Proofread the description
- ✅ Check for typos in download instructions

**After Publishing**:
- 🔒 Can't delete releases easily (can mark as pre-release)
- 📝 Can edit description anytime
- 🔄 Can add/remove files from release
- ⭐ Old downloads stay accessible

---

## 🆘 Troubleshooting

**Problem**: Upload fails
- **Solution**: Check file size (<2GB), try different browser

**Problem**: Can't create tag
- **Solution**: Make sure tag doesn't already exist, use unique version

**Problem**: Release not showing as "latest"
- **Solution**: Edit release, check "Set as latest release"

**Problem**: Download is slow
- **Solution**: Normal for 53MB, consider providing torrent for very large files

---

## ✅ Quick Checklist

Before clicking "Publish release":

- [ ] Tag: `v2.4.1`
- [ ] Title: Descriptive and includes version
- [ ] Description: Complete with download instructions
- [ ] File attached: `Supervertaler_v2.4.1_Windows.zip`
- [ ] Latest release: Checked
- [ ] Pre-release: Unchecked
- [ ] Tested ZIP file works

**Ready? Click "Publish release"!** 🚀

---

**Your users will love having an easy download option!** 

The GitHub Releases page provides:
- ✅ Professional appearance
- ✅ Version history
- ✅ Easy downloads
- ✅ Automatic changelog
- ✅ Download statistics

**Time to make Supervertaler accessible to everyone!** 🎉
