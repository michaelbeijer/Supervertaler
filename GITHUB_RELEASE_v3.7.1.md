# GitHub Release v3.7.1 - Copy/Paste Content

## Release Title
```
v3.7.1 - Security & Configuration Update
```

## Release Tag
```
v3.7.1
```

## Release Description (Body)

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

#### **Option 1: From Source (Recommended for Now)**
```bash
# Clone or pull the latest code
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# Install dependencies
pip install -r requirements.txt

# Run it
python Supervertaler_v3.7.1.py
```

#### **Option 2: Python Package**
```bash
# Coming soon to PyPI - v3.7.1 will be uploaded shortly
# For now, use Option 1 (From Source)
```

#### **Option 3: Windows Executable**
- Coming soon - pre-built executable will be attached to this release

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

## Checklist for Creating Release on GitHub

1. Go to: https://github.com/michaelbeijer/Supervertaler/releases/new
2. Set **Tag version**: `v3.7.1`
3. Set **Release title**: `v3.7.1 - Security & Configuration Update`
4. Paste the above **Release Description** into the body
5. Options:
   - ☐ Check "This is a pre-release" if testing only
   - ☑ Leave unchecked for production release
6. (Optional) **Attach files**:
   - Source code ZIP (auto-generated by GitHub)
   - Once PyInstaller build completes, attach `dist/Supervertaler.zip`
7. Click **"Publish release"**

---

## Additional Details for Release

### Release Assets to Attach (When Ready)

If you want to add downloadable files:

```
Supervertaler-v3.7.1-source.zip          (Source code)
Supervertaler-v3.7.1-windows-portable.zip (Windows executable + full folder structure)
```

To create the Windows portable ZIP:
```powershell
# After PyInstaller build completes:
cd c:\Dev\Supervertaler\dist
Compress-Archive -Path Supervertaler -DestinationPath Supervertaler-v3.7.1-windows-portable.zip
```

---

## GitHub Web Release URL

After publishing, your release will be at:
```
https://github.com/michaelbeijer/Supervertaler/releases/tag/v3.7.1
```

---

## Optional: Release Announcement

Share on social media / forums:
```
🎉 Supervertaler v3.7.1 is here! 

🔐 Security & Configuration Update:
- Completely resolved security incident 
- Secure user data folder system
- API keys now protected
- First-launch SetupWizard
- Choose where your data lives

Download now: https://github.com/michaelbeijer/Supervertaler/releases/tag/v3.7.1

Upgrading from v3.7.0? Seamless migration - just launch and follow the wizard!

#Translation #AI #OpenSource #CAT
```
