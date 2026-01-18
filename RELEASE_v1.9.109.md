# Supervertaler v1.9.109 - Windows Release

## 📦 What's in This Release

This folder contains the distribution packages for Supervertaler v1.9.109:

| File | Type | Size | Description |
|------|------|------|-------------|
| Supervertaler-v1.9.109-Windows-CORE.zip | Windows EXE | ~200 MB | Core Windows application (excludes heavy ML dependencies) |
| Supervertaler-v1.9.109-Windows-FULL.zip | Windows EXE | ~589 MB | Complete Windows application with all features including heavy ML dependencies (Supermemory, Local Whisper) |
| supervertaler-1.9.109-py3-none-any.whl | Python Wheel | ~1 MB | Pip installable package (wheel format) |
| supervertaler-1.9.109.tar.gz | Python Source | ~14 MB | Pip installable package (source distribution) |

---

## 🪟 Windows EXE Installation

### CRITICAL: One-Folder Build Rule

⚠️ **The EXE must be run from the extracted distribution folder!**

**Correct Setup:**
1. Extract `Supervertaler-v1.9.109-Windows-CORE.zip` (or FULL) to a folder (e.g., `C:\Supervertaler\`)
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
pip install supervertaler-1.9.109-py3-none-any.whl
```

### Option 3: Install from Source
```bash
pip install supervertaler-1.9.109.tar.gz
```

### Run After Installation
```bash
# Launch the application
supervertaler

# Or via Python module
python -m Supervertaler
```

---

## 🆕 What's New in v1.9.109

### TMX Import Language Pair Fix (Issue #105)

**🔧 Fixed Critical Bug:** TMX files were sometimes being imported with reversed language pairs

**The Problem:**
- User reported EN-GB → DE-DE TMX files being imported as DE-DE → EN-GB
- Made TM matches impossible to find
- Caused by incorrect assumption about TMX language order

**The Fix:**
- Added language pair selection dialog when importing TMX files
- User now explicitly chooses which language is source and which is target
- Prevents accidental language reversal regardless of TMX file structure
- Applied to both "Create new TM" and "Add to existing TM" workflows

**User Impact:**
- TMX imports now work correctly for all language pairs
- No more mysterious "no matches found" issues
- Clear, explicit language selection every time

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

Store in `api_keys.txt`:
```
openai_api_key=sk-...
anthropic_api_key=sk-ant-...
google_api_key=AI...
```

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

Built on January 18, 2026  
Version: 1.9.109
