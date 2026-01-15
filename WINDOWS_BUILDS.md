# Windows EXE Builds

## Two Build Flavors

Supervertaler Windows releases are published as **two separate ZIP assets**:

### 1. CORE (Recommended)
- **File:** `Supervertaler-v1.9.107-Windows-CORE.zip`
- **Size:** ~300 MB
- **Contents:** Full application without heavy ML stack
- **Excludes:** Supermemory, offline Local Whisper (PyTorch)
- **Recommended for:** Most users
- **Features:** All core CAT tool features, LLM translation, TM/glossaries, voice dictation via OpenAI API

### 2. FULL (Complete)
- **File:** `Supervertaler-v1.9.107-Windows-FULL.zip`
- **Size:** ~900 MB
- **Contents:** Full application with all optional components
- **Includes:** Everything in CORE + offline Local Whisper support
- **Note:** Supermemory has been removed as of v1.9.105

## Critical Installation Note

⚠️ **The EXE must be run from the extracted distribution folder.**

Do **NOT** separate `Supervertaler.exe` from the `_internal/` directory.

If users see an error like missing `python312.dll`, they are:
- Running the wrong EXE (from an intermediate build folder), or
- Moving the EXE away from `_internal/`

## Building

### Build Both (Recommended)
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_windows_release.ps1
```

### Build CORE Only
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_windows_release.ps1 -CoreOnly
```

### Build FULL Only
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_windows_release.ps1 -FullOnly
```

### Clean Build (Remove Build Venvs)
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_windows_release.ps1 -Clean
```

## Output Files

After successful build:
- `dist\Supervertaler-v1.9.107-Windows-CORE.zip`
- `dist\Supervertaler-v1.9.107-Windows-FULL.zip`

Each ZIP contains:
- `Supervertaler.exe`
- `_internal\` directory with all dependencies
- `README_FIRST.txt` with installation instructions

## Posting to GitHub

1. Create a new release on GitHub with tag `v1.9.107`
2. Attach **both** ZIP files to the same release
3. Users can choose which build suits their needs

## Build Environments

The build script uses isolated Python environments:
- `.venv-build-core` - For CORE build
- `.venv-build-full` - For FULL build

These are automatically created and managed by the build script.

## Version Update Checklist

Before building, ensure version is updated in:
- [x] `Supervertaler.py` (`__version__`)
- [x] `pyproject.toml` (`version`)
- [x] `README.md` (heading and current version)
- [x] `docs/index.html` (3 locations)
- [x] `CHANGELOG.md` (new entry)

## Current Version

**v1.9.107** - January 15, 2026
