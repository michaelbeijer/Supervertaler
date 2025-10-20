# GitHub Release v3.7.1 - READY TO COPY/PASTE

## 🎯 WHAT TO DO

1. Go to: https://github.com/michaelbeijer/Supervertaler/releases/new
2. Fill in the fields below with the copy/paste content provided
3. Click "Publish release"
4. Done! ✅

---

## 📋 FIELD 1: Release Tag

**Paste this into the "Choose a tag" field:**

```
v3.7.1
```

(Click "Create a new tag" and type exactly: `v3.7.1`)

---

## 📝 FIELD 2: Release Title

**Paste this into the "Release title" field:**

```
v3.7.1 - Security & Configuration Update
```

---

## 📄 FIELD 3: Release Description (MAIN CONTENT)

**Paste ALL of the following into the "Describe this release" textarea:**

```markdown
## 🔐 Security & Configuration Update

**v3.7.1 is a critical security patch and major UX improvement for Supervertaler.**

### 🚨 Important Security Updates

#### What Changed
- **Removed v3.7.0 from all distribution channels** (yanked from PyPI, deleted GitHub release)
- **Removed confidential client data from git history** (364 commits cleaned via git filter-branch)
- **API keys now stored securely** in user-chosen data folder, never in installation
- **Complete reorganization** of user data handling for better security and portability

#### Why
v3.7.0 had an unintended exposure of client project names in git history. This release completely resolves that issue and implements a secure, user-friendly data folder system.

#### What You Should Do
- **Upgrade to v3.7.1** (from v3.7.0 or earlier)
- **Consider API key rotation** (keys were visible in exposed file)
- That's it! First launch will guide you through setup

---

### ✨ What's New in v3.7.1

#### 🔧 User-Configurable Data Folder
- **First Launch**: SetupWizard guides you to choose where your data lives
- **Choose Anywhere**: Documents, Desktop, USB stick, cloud-synced folder - your choice
- **Settings Menu**: New "Change Data Folder" option to move data anytime
- **Benefits**: Data is portable, easy to backup, shareable across devices (if desired)

#### 📁 Improved Folder Structure
```
Your_Chosen_Location/
├── api_keys.txt                    ← Your API credentials (NEVER in git!)
├── Prompt_Library/
│   ├── System_prompts/             ← 19 domain-specific specialist prompts
│   └── Custom_instructions/        ← Your personal translation preferences
├── Translation_Resources/
│   ├── Glossaries/                 ← Your terminology
│   ├── TMs/                        ← Your translation memories
│   ├── Non-translatables/
│   └── Segmentation_rules/
└── Projects/                       ← Your translation projects
```

#### ⚡ Automatic Setup
- `api_keys.txt` created from template automatically
- Existing users: Your old keys migrated automatically
- No manual copying or configuration needed
- Just add your API keys and you're ready

#### 🐛 Bug Fixes
- Fixed Tkinter error when switching Prompt Library tabs
- Improved error handling throughout
- Better user feedback and status messages

---

### 📖 Documentation

**New Guides**:
- [USER_DATA_FOLDER_SETUP.md](https://github.com/michaelbeijer/Supervertaler/blob/main/docs/guides/USER_DATA_FOLDER_SETUP.md) - Complete setup guide for all platforms
- [RELEASE_v3.7.1.md](https://github.com/michaelbeijer/Supervertaler/blob/main/docs/RELEASE_v3.7.1.md) - Full release notes and technical details

**Updated**:
- [README.md](https://github.com/michaelbeijer/Supervertaler/blob/main/README.md) - Version updated, new features documented
- [CHANGELOG.md](https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md) - Comprehensive change log

---

### 📦 Installation

Choose your preferred method:

#### **Option 1: From Source (Recommended)**
```bash
# Clone or pull the latest code
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# Install dependencies
pip install -r requirements.txt

# Run it
python Supervertaler_v3.7.1.py
```

#### **Option 2: Python Package (via pip)**
```bash
# Coming soon to PyPI
# For now, use Option 1
```

#### **Option 3: Windows Executable (Coming Soon)**
- Pre-built executable will be released shortly
- No Python installation required

---

### 🔄 Upgrading from v3.7.0

**It's seamless:**
1. Download/pull v3.7.1
2. First launch shows SetupWizard
3. Select your data folder location
4. SetupWizard automatically migrates your old api_keys.txt
5. You're done! Everything continues working

---

### 🎯 Key Features (All Versions)

- 🤖 **Multiple AI Providers**: OpenAI GPT-4, Anthropic Claude, Google Gemini
- 🧠 **Context-Aware Translation**: Full document understanding
- 📚 **Prompt Library**: 19 System Prompts + Custom Instructions + Prompt Assistant
- 📊 **Translation Memory**: Fuzzy matching, segment history
- 🖼️ **Multimodal Support**: GPT-4 Vision for figure context
- ✏️ **Professional CAT Editor**: Grid view, pagination, dual selection
- 🔗 **CAT Tool Integration**: memoQ, CafeTran, Trados Studio
- 📥 **Smart Import/Export**: DOCX, TSV, JSON, XLIFF, TMX, Excel
- 🔐 **Privacy First**: No data collection, local processing only

---

### 🔐 Security Highlights

✅ **API Keys Protected**
- Stored in user data folder
- Never committed to git
- Never in installation directory

✅ **Client Data Safe**
- Removed from git history completely (verified 404)
- No confidential information in repository
- Development work separated from production

✅ **Open Source**
- Full audit trail visible
- No hidden code or behavior
- MIT licensed - use freely

---

### 📞 Support & Community

- 💬 **GitHub Discussions**: [Ask questions, share ideas](https://github.com/michaelbeijer/Supervertaler/discussions)
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/michaelbeijer/Supervertaler/issues)
- 📖 **Documentation**: [User Guides](https://github.com/michaelbeijer/Supervertaler/tree/main/docs/guides)
- 🌐 **Website**: [supervertaler.com](https://supervertaler.com)

---

### 💡 What's Next?

v3.8.0 is in planning phase with:
- Enhanced Prompt Assistant with auto-refinement
- Advanced TM features (penalty weights, leverage scoring)
- Glossary management UI improvements
- Additional CAT tool integrations

Community contributions welcome!

---

**Release Date**: October 20, 2025  
**Version**: v3.7.1  
**Status**: ✅ Ready for use  
**License**: MIT (Open Source and Free)

---

> **Supervertaler**: Empowering professional translators with intelligent, context-aware AI tools. Built by translators, for translators.
```

---

## 🎬 FINAL STEPS

### Option A: Upload from GitHub.com (Easiest)

1. **Go to**: https://github.com/michaelbeijer/Supervertaler/releases/new
2. **Tag version**: Type `v3.7.1`
3. **Release title**: Copy from "FIELD 2" above
4. **Description**: Copy from "FIELD 3" above (the big markdown block)
5. **Assets** (optional): Drag & drop `Supervertaler-v3.7.1-source.zip` from your computer
6. **Publish**: Click "Publish release"

### Option B: Using GitHub CLI

```bash
gh release create v3.7.1 \
  --title "v3.7.1 - Security & Configuration Update" \
  --draft=false \
  path/to/Supervertaler-v3.7.1-source.zip
```

(Then paste description in the web interface)

---

## ✅ VERIFICATION CHECKLIST

After publishing, verify:

- [ ] Release appears at: https://github.com/michaelbeijer/Supervertaler/releases/tag/v3.7.1
- [ ] Title displays correctly
- [ ] Description markdown renders properly
- [ ] All links in description work
- [ ] Source ZIP is attached (if uploading)
- [ ] Tag shows in "Releases" tab

---

## 📢 OPTIONAL: SHARE RELEASE

After publishing, you can share:

**On Twitter/X:**
```
🎉 Supervertaler v3.7.1 is here! 

🔐 Security & Configuration Update:
- Completely resolved security incident 
- Secure user data folder system
- API keys now protected
- First-launch SetupWizard
- Choose where your data lives

Download: https://github.com/michaelbeijer/Supervertaler/releases/tag/v3.7.1

Upgrading from v3.7.0? Seamless migration!

#Translation #AI #OpenSource #CAT
```

**On GitHub Discussions:**
- Post a link to the release
- Ask for feedback
- Announce new features

---

## 🎉 THAT'S IT!

Your v3.7.1 release is ready! All the copy/paste content is above.

**Questions?** Check `GITHUB_RELEASE_INSTRUCTIONS.md` for detailed step-by-step guide.

---

Generated: October 20, 2025
Version: v3.7.1
Status: Ready to Release ✅
