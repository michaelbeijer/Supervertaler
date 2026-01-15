# Supervertaler v1.9.104 - January 2026 Release (incl. Windows .exe)

This file is a step-by-step guide for posting the **v1.9.104** release on GitHub (and optionally PyPI), and includes a **copy-pasteable GitHub Release description** that matches the structure and language of the v1.9.76 release.

---

## ✅ 1) Pre-Release Checklist

Before tagging/publishing, verify these are already updated to `v1.9.104`:

- `Supervertaler.py` (`__version__`)
- `pyproject.toml` (project version)
- `README.md` (header + “Current Version”)
- `CHANGELOG.md` (“Current Version” + v1.9.104 entry)
- `docs/index.html` (version pill / cache-busting if applicable)

Optional sanity checks:

- Launch from source once: `python Supervertaler.py`
- Confirm `Help → About` shows `v1.9.104`

---

## 🧱 2) Build the Windows Executable (.exe) + ZIP Asset

From the repo root:

```powershell
# (Optional) activate venv
.\.venv\Scripts\Activate.ps1

# Clean old build outputs
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path dist)  { Remove-Item -Recurse -Force dist }

# Build one-folder EXE
python -m PyInstaller --noconfirm --clean Supervertaler.spec

# Create the versioned ZIP asset (includes the folder build)
python .\create_release_zip.py
```

Expected artifact:

- `dist\Supervertaler-v1.9.104-Windows.zip`

Quick manual check:

- Extract the ZIP
- Run `Supervertaler.exe` from inside the extracted folder
- Ensure `_internal\` exists next to the EXE (required for `python312.dll`)

---

## 🏷️ 3) Create the Git Tag

```powershell
git status
# Ensure working tree is clean

git pull

git tag v1.9.104

git push origin v1.9.104
```

---

## 🧾 4) Create the GitHub Release

1. Go to the GitHub Releases page:
   - https://github.com/michaelbeijer/Supervertaler/releases
2. Click **Draft a new release**.
3. Choose tag: `v1.9.104`.
4. Release title: `Supervertaler v1.9.104`.
5. Upload the Windows asset:
   - `Supervertaler-v1.9.104-Windows.zip`
6. Paste the **copy-pasteable description** from the next section.
7. Tick **Set as the latest release**.
8. Publish.

---

## 📋 5) Copy-Pasteable GitHub Release Description

Paste everything below into the GitHub Release description field:

---

# Supervertaler v1.9.104 - January 2026 Release (incl. Windows .exe)

Release Date: January 14, 2026

## 📦 Installation

### Recommended: Install from PyPI

```bash
pip install supervertaler   # Install the package
supervertaler               # Launch the app
```

### Alternative: Windows Executable

Download `Supervertaler-v1.9.104-Windows.zip`, extract, and run `Supervertaler.exe`.

**Important:** The EXE must be run from the extracted folder with the `_internal` directory next to it.

**Optional features note (Supermemory / Local Whisper):** pip “extras” are for the Python install only — you can’t install them *into* the portable Windows EXE after the fact. If you need those heavy optional features, use the Python/pip install (and install extras there), or download a separate EXE build that already includes them.

## ✨ What’s New in v1.9.104

### 📦 Packaging: Lighter Default Install

Made **Supermemory** an optional install extra again, so the default `pip install supervertaler` no longer pulls the heavy ML stack (PyTorch / sentence-transformers / ChromaDB).

- Default install stays “batteries included” for the major workflows, while keeping the heavyweight ML dependencies out of the default path.
- Install Supermemory on demand:

```bash
pip install supervertaler[supermemory]
```

## 📋 Full Changelog

See [CHANGELOG.md](https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md) for complete version history.

## 🔗 Links

- PyPI Package: https://pypi.org/project/Supervertaler/
- Project website: https://supervertaler.com/
- Supervertaler Help: https://supervertaler.gitbook.io/superdocs/
- GitHub: https://github.com/michaelbeijer/Supervertaler

---

## 📦 6) (Optional) Publish to PyPI

Only do this if you’re releasing the Python package version at the same time and the version isn’t already on PyPI.

```powershell
# Clean build artifacts
Remove-Item -Recurse -Force .\dist -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .\build -ErrorAction SilentlyContinue

# Build wheel + sdist
python -m build

# Upload (requires twine + credentials)
python -m twine upload dist\*
```

---

## ✅ 7) Post-Release Quick Checks

- GitHub “Latest” release points to `v1.9.104`
- Asset downloads and extracts correctly
- Windows EXE launches from the extracted folder
- `pip install supervertaler` does **not** pull the Supermemory heavy stack by default
