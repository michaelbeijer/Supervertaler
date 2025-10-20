# GitHub Release v3.7.1 - Copy & Paste Ready

**Build Status**: ✅ COMPLETE  
**Build Date**: October 20, 2025  
**Executable**: Supervertaler-v3.7.1.zip (93.37 MB)  
**Location**: `/dist/Supervertaler-v3.7.1.zip`

---

## 📋 STEP 1: Copy Release Title

```
Supervertaler v3.7.1 - Security & Configuration Update
```

---

## 📝 STEP 2: Copy Release Description

```markdown
🔐 **Critical Security & Configuration Update**

This release resolves a critical security incident and implements a major configuration overhaul for better user experience and data protection.

## 🚨 SECURITY UPDATES

**What's Fixed**:
- ✅ Removed `recent_projects.json` from entire git history (364 commits cleaned)
- ✅ API keys now stored in user data folder (never in installation)
- ✅ v3.7.0 yanked from PyPI and GitHub releases
- ✅ Fixed Tkinter tab switching crash in Prompt Library

**What You Should Do**:
- Upgrade from v3.7.0 (yanked - no longer available)
- Consider rotating API keys if v3.7.0 was used with live keys
- Backup your current data before upgrading

## ✨ NEW FEATURES

**User-Configurable Data Folder**:
- First-launch SetupWizard guides you through setup
- Choose where to store your data (Documents, Desktop, custom path)
- All your data in one portable location
- Easy backups and cloud sync support

**Automatic Setup & Migration**:
- `api_keys.txt` created automatically on first launch
- Existing API keys from v3.7.0 auto-migrated
- Configuration saved securely
- Projects and resources preserved

**Settings Enhancement**:
- New "Data Folder" section in Settings
- "Change Data Folder" button to relocate data anytime
- Optional migration when changing paths

## 📁 WHAT'S INCLUDED

- ✅ Windows executable (`Supervertaler.exe`)
- ✅ Full folder structure with docs and modules
- ✅ All documentation and guides
- ✅ No external dependencies needed (everything bundled)

## 📚 DOCUMENTATION

- **[USER_DATA_FOLDER_SETUP.md](https://github.com/michaelbeijer/Supervertaler/blob/main/docs/guides/USER_DATA_FOLDER_SETUP.md)** - Complete setup guide for all platforms
- **[RELEASE_v3.7.1.md](https://github.com/michaelbeijer/Supervertaler/blob/main/docs/RELEASE_v3.7.1.md)** - Detailed release summary
- **[README.md](https://github.com/michaelbeijer/Supervertaler/blob/main/README.md)** - General overview
- **[CHANGELOG.md](https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md)** - Full version history

## 🚀 QUICK START

1. **Download** `Supervertaler-v3.7.1.zip`
2. **Extract** to any folder (e.g., `C:\Program Files\Supervertaler\`)
3. **Run** `Supervertaler/Supervertaler.exe`
4. **SetupWizard** guides you through first-time setup
5. **Add API keys** and start translating!

## 🔄 FOR v3.7.0 USERS

Upgrade is seamless:
1. Download and extract v3.7.1
2. Run the executable
3. SetupWizard appears on first launch
4. Choose your data folder location
5. Existing API keys automatically copied
6. Everything works as before (but more secure!)

## 🐛 BUG FIXES

- Fixed Tkinter crash when switching Prompt Library tabs
- Improved error handling in UI framework

## 📊 TECHNICAL DETAILS

**Version**: 3.7.1  
**Build Date**: October 20, 2025  
**Python**: 3.12  
**File Size**: 93.37 MB (zipped)  
**Windows**: 10, 11 (64-bit)  

**Dependencies Included**:
- OpenAI SDK (GPT-4 support)
- Anthropic Claude API
- Google Gemini API
- python-docx (DOCX support)
- PIL/Pillow (Image handling)
- All other required libraries

**No installation required** - just extract and run!

## 📞 SUPPORT

- 📖 [User Guide](https://github.com/michaelbeijer/Supervertaler/blob/main/docs/guides/USER_GUIDE.md)
- 🐛 [Report Issues](https://github.com/michaelbeijer/Supervertaler/issues)
- 💬 [GitHub Discussions](https://github.com/michaelbeijer/Supervertaler/discussions)
- 🌐 [Website](https://supervertaler.com)

## ✅ VERIFIED

- ✅ Executable tested and working
- ✅ All dependencies bundled
- ✅ Folder structure complete
- ✅ Documentation updated
- ✅ Security audited and cleared

---

**Release Notes**: This is a recommended upgrade from v3.7.0. See [RELEASE_v3.7.1.md](https://github.com/michaelbeijer/Supervertaler/blob/main/docs/RELEASE_v3.7.1.md) for comprehensive details.
```

---

## 🏷️ STEP 3: Add Release Tags

Choose these tags (comma-separated):
```
security,configuration,windows,cat-tool,translation,ai,llm,gpt-4,claude
```

---

## 📦 STEP 4: Upload Asset

**File to Upload**: `c:\Dev\Supervertaler\dist\Supervertaler-v3.7.1.zip`

**File Details**:
- Filename: `Supervertaler-v3.7.1.zip`
- Size: 93.37 MB
- Type: Windows executable + full folder structure
- Contains: `Supervertaler.exe` + docs + modules + all dependencies

**Upload Instructions**:
1. Go to: https://github.com/michaelbeijer/Supervertaler/releases/new
2. Paste Title from **STEP 1**
3. Paste Description from **STEP 2**
4. Add Tags from **STEP 3** (click "Add label")
5. Drag & drop `Supervertaler-v3.7.1.zip` to Assets section
6. OR click "Attach binaries" and browse to the file
7. Make sure "This is a pre-release" is **UNCHECKED** (this is a stable release)
8. Click "Publish release"

---

## 🎯 CHECKLIST BEFORE PUBLISHING

- [ ] Title copied correctly
- [ ] Description text pasted into description field
- [ ] ZIP file (93.37 MB) uploaded to assets
- [ ] Tags added
- [ ] "This is a pre-release" is UNCHECKED
- [ ] Release description mentions it's a security update
- [ ] All links work (can test after publishing)

---

## 🔗 DIRECT GITHUB LINK

Create release here:
https://github.com/michaelbeijer/Supervertaler/releases/new

---

## 📋 ALTERNATIVE: Using GitHub CLI

If you have GitHub CLI installed, run:

```bash
cd c:\Dev\Supervertaler
gh release create v3.7.1 `
  --title "Supervertaler v3.7.1 - Security & Configuration Update" `
  --body "$(Get-Content -Path 'docs/RELEASE_v3.7.1.md')" `
  dist/Supervertaler-v3.7.1.zip
```

---

## ✅ VERIFICATION

After publishing, verify:

1. **Check ZIP downloads**: https://github.com/michaelbeijer/Supervertaler/releases/v3.7.1
2. **Confirm file size**: Should show ~93 MB
3. **Verify description**: Should have security highlights
4. **Test link**: Download and extract locally to confirm

---

**Ready to release!** Just follow the 4 steps above. 🚀
```

