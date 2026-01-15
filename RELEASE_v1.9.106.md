# Supervertaler v1.9.106 - January 2026 Release

**Release Date:** January 15, 2026

---

## 📦 Installation

### Recommended: Install from PyPI

```bash
pip install supervertaler   # Install the package
supervertaler               # Launch the app
```

### Alternative: Windows Executable (Two Builds Available)

**CORE (Recommended)** - `Supervertaler-v1.9.106-Windows-CORE.zip` (~300 MB)
- Full CAT tool functionality
- All LLM translation (GPT-4, Claude, Gemini, Ollama)
- Voice dictation via OpenAI Whisper API
- Excludes: Offline Local Whisper (PyTorch)

**FULL (Complete)** - `Supervertaler-v1.9.106-Windows-FULL.zip` (~900 MB)  
- Everything in CORE
- Plus: Offline Local Whisper support (no API required)
- For users who need offline voice dictation

**Important:** The EXE must be run from the extracted folder with the `_internal` directory next to it.

---

## ✨ What's New in v1.9.106

### 🗂️ Tab Reorganization
- **Segmentation Rules** moved from Resources → Settings (more logical placement for configuration)
- **Prompt Manager** elevated to top-level tab (now positioned between Resources and Tools)
- New tab structure: Grid → Resources → **Prompt Manager** → Tools → Settings

### 📝 Improved Descriptions
- Updated project description to emphasize "AI-enhanced" workflow (assists translators rather than replacing them)
- New GitHub About section highlighting Superlookup concordance system and CAT tool integrations
- Updated website and documentation with clearer messaging

### 🔧 Technical Improvements
- Fixed duplicate entry in `pyproject.toml` that was causing build errors
- All version references synchronized across codebase
- Documentation improvements in `WINDOWS_BUILDS.md`

---

## 🗑️ Note: Supermemory Removed (v1.9.105)

As of v1.9.105, Supermemory (vector-indexed semantic search) has been completely removed from the project. This decision was made after extensive Windows EXE packaging attempts revealed:
- Complex native dependencies (PyTorch, CUDA libs, Intel MKL)
- ~600 MB footprint for a feature that didn't work reliably in frozen builds
- 7+ packaging iterations without stable results

**The focus is now on the SQLite-based Translation Memory system**, which is:
- ✅ Faster and more reliable
- ✅ Works perfectly in frozen builds  
- ✅ Easier to maintain
- ✅ Better suited for large TMX imports

---

## 🔍 CORE vs FULL: What's the Difference?

Since Supermemory has been removed, the **only difference** between CORE and FULL is:

| Feature | CORE | FULL |
|---------|------|------|
| **Voice Dictation (OpenAI API)** | ✅ Included | ✅ Included |
| **Offline Local Whisper** | ❌ Not included | ✅ Included |
| **PyTorch Dependencies** | ❌ Not included | ✅ Included |
| **Download Size** | ~300 MB | ~900 MB |
| **Recommended For** | Most users | Offline voice users |

**Recommendation:** Use **CORE** unless you specifically need offline voice dictation without an OpenAI API key.

---

## 📋 Full Changelog

See [CHANGELOG.md](https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md) for complete version history.

---

## 🔗 Links

- **PyPI Package:** https://pypi.org/project/Supervertaler/
- **Project Website:** https://supervertaler.com/
- **Documentation:** https://supervertaler.gitbook.io/superdocs/
- **GitHub:** https://github.com/michaelbeijer/Supervertaler

---

## ✅ Post-Release Checklist

- [ ] GitHub "Latest" release points to v1.9.106
- [ ] Both ZIP assets (CORE + FULL) download and extract correctly
- [ ] Windows EXE launches from extracted folder
- [ ] `pip install supervertaler` installs v1.9.106
- [ ] Website shows v1.9.106
