# Supervertaler v1.9.113 - Windows Release

## 📦 What's in This Release

This folder contains the distribution packages for Supervertaler v1.9.113:

| File | Type | Size | Description |
|------|------|------|-------------|
| Supervertaler-v1.9.113-Windows-CORE.zip | Windows EXE | ~341 MB | Core Windows application (excludes heavy ML dependencies) |
| Supervertaler-v1.9.113-Windows-FULL.zip | Windows EXE | ~589 MB | Complete Windows application with all features including heavy ML dependencies (Local Whisper offline voice) |
| supervertaler-1.9.113-py3-none-any.whl | Python Wheel | ~951 KB | Pip installable package (wheel format) |
| supervertaler-1.9.113.tar.gz | Python Source | ~14 MB | Pip installable package (source distribution) |

---

## 🪟 Windows EXE Installation

### CRITICAL: One-Folder Build Rule

⚠️ **The EXE must be run from the extracted distribution folder!**

**Correct Setup:**
1. Extract `Supervertaler-v1.9.113-Windows-CORE.zip` (or FULL) to a folder (e.g., `C:\Supervertaler\`)
2. Run `Supervertaler.exe` from that folder (next to the `_internal/` directory)
3. Never move the EXE away from `_internal/` - it won't work!

**File Structure After Extraction:**
```
Supervertaler-core/  (or Supervertaler-full/)
├── Supervertaler.exe          ← Run this
├── _internal/                 ← Required dependencies (thousands of files)
│   ├── python312.dll
│   ├── PyQt6/
│   ├── torch/              (FULL only)
│   └── ... (all dependencies)
└── README_FIRST.txt
```

### Common Mistakes

❌ Moving `Supervertaler.exe` to Desktop → Won't work  
❌ Running the EXE from a build folder → Wrong EXE  
❌ Missing `_internal/` directory → DLL errors  
✅ Extract ZIP, run EXE from extracted folder → Works!

---

## 🐍 Python Package Installation

### Option 1: Install from PyPI (Recommended)
```bash
pip install --upgrade supervertaler
```

### Option 2: Install from Wheel (Offline/Local)
```bash
pip install supervertaler-1.9.113-py3-none-any.whl
```

### Option 3: Install from Source
```bash
pip install supervertaler-1.9.113.tar.gz
```

### Run After Installation
```bash
# Launch the application
supervertaler

# Or via Python module
python -m Supervertaler
```

---

## 🆕 What's New in v1.9.113

### 🔐 Unified API Key Loading System

**Major improvement that fixes AI Assistant bug #107 and consolidates API key management:**

**The Problem:**
- Three different API key file locations existed (root, user_data, user_data_private)
- Two different loading mechanisms caused inconsistencies
- Conflicting instructions in example files
- **AI Assistant bug (#107)**: Keys worked for translation but failed for AI Assistant with "Incorrect API key provided" error

**The Solution:**
- **Unified loading in main app**: Single `load_api_keys()` method checks TWO locations with clear priority:
  1. `user_data_private/api_keys.txt` (Dev mode - gitignored, never uploaded to GitHub)
  2. `user_data/api_keys.txt` (User mode - ships with app)
- **AI Assistant fixed**: Now uses `parent_app.load_api_keys()` instead of separate module function
- **Example files updated**: Both example files now give consistent, clear instructions

**Developer Workflow:**
- Store keys in `user_data_private/api_keys.txt`
- Fully gitignored - safe from accidental commits
- All features find keys here (translation, AI Assistant, tests)

**User Workflow:**
- Keys go in `user_data/api_keys.txt`
- App auto-creates this location on first run
- Simple, single location

**Result:**
- ✅ Developers: Keys safe in gitignored location
- ✅ Users: Simple single location
- ✅ AI Assistant: Now works with same keys as translation
- ✅ No more confusion about where to put keys

---

## 📋 System Requirements

### Windows EXE (CORE/FULL)

- **OS:** Windows 10 or later (64-bit)
- **RAM:** 4 GB minimum, 8 GB recommended
- **Disk Space:** 1-2 GB free space (CORE) or 2-3 GB (FULL)
- **Display:** 1280x720 minimum resolution

### Python Package

- **Python:** 3.10 or later
- **OS:** Windows, Linux, macOS
- **RAM:** 2 GB minimum
- **Dependencies:** Installed automatically via pip

---

## 🔑 API Keys (Optional)

For AI translation features, you'll need API keys from:

- **OpenAI** (ChatGPT models)
- **Anthropic** (Claude models)
- **Google AI** (Gemini models - FREE tier available!)

### Where to Store API Keys

**End Users (Windows EXE or pip install):**

Create a file called `api_keys.txt` in your `user_data` folder:

```
openai=sk-...
claude=sk-ant-...
google=AI...
deepl=...
```

The app will automatically create this folder on first run. Look for it in:
- **Windows:** `C:\Users\YourName\AppData\Local\Supervertaler\user_data\`
- **Or:** Next to the `Supervertaler.exe` if running from extracted ZIP

**Developers (running from source):**

Create `user_data_private/api_keys.txt` (this location is gitignored):

```
openai=sk-...
claude=sk-ant-...
google=AI...
```

### MyMemory Translation Tip

MyMemory offers a free machine translation API. For better rate limits, use your email as the key:

```
mymemory=your.email@example.com
```

This increases your limit from 1,000 to 10,000 words/day!

---

## 🆘 Troubleshooting

### Windows EXE Issues

**"python312.dll not found"**
- ✅ Extract the full ZIP archive
- ✅ Run `Supervertaler.exe` from the extracted folder
- ❌ Don't move the EXE away from `_internal/`

**Application won't start**
- Check Windows Defender/antivirus isn't blocking it
- Right-click → Properties → Unblock
- Run as administrator if needed

### Python Package Issues

**Import errors**
```bash
# Reinstall with all dependencies
pip install --force-reinstall supervertaler
```

**Qt platform plugin errors**
```bash
# Install PyQt6 explicitly
pip install PyQt6>=6.6.0
```

**AI Assistant not finding API keys**
- Make sure you're using v1.9.113 or later
- Check `api_keys.txt` is in the correct location (see above)
- Verify the file format matches the examples (no extra spaces)

---

## 📚 Documentation

- **Website:** https://supervertaler.com
- **Online Help:** https://supervertaler.gitbook.io/superdocs/
- **GitHub:** https://github.com/michaelbeijer/Supervertaler
- **Support:** Open an issue on GitHub

---

## 📄 License

MIT License - Copyright (c) 2025-2026 Michael Beijer

---

## 🙏 Credits

**Author:** Michael Beijer  
**Translation:** Dutch ↔ English patent and technical translator  
**Website:** https://michaelbeijer.co.uk  
**Terminology:** https://beijerterm.com

Built on January 19, 2026  
Version: 1.9.113
