# Build Requirements and Guidelines

## CRITICAL: Pre-Build Checklist

### 1. Clean Build Environment (ALWAYS DO THIS FIRST!)

**MANDATORY commands before EVERY build:**

```powershell
cd "c:\Users\mbeijer\My Drive\Software\Python\Supervertaler"
Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
```

**Why:** Ensures old build artifacts don't interfere with new build

### 2. Clean Old Release ZIPs (If version name unchanged)

**ALWAYS delete existing ZIP if creating a new one with the same name:**

```powershell
Remove-Item -Path "Supervertaler_v2.4.1_Windows.zip" -Force -ErrorAction SilentlyContinue
```

**Why:** Prevents confusion between old and new releases with same version number

---

## File Structure Requirements

### ⚠️ IMPORTANT: Files That MUST Be in ROOT (not _internal)

The following files/folders **MUST** be in the distribution root folder (alongside `Supervertaler.exe`), NOT in the `_internal` folder:

#### Folders (User-Accessible):
- ✅ `custom_prompts/` - User-accessible custom prompt templates
- ✅ `docs/` - User documentation and guides
- ✅ `projects/` - User project storage
- ✅ `projects_private/` - Private project storage

#### Files (User-Visible):
- ✅ `api_keys.example.txt` - Template for API keys
- ✅ `CHANGELOG.md` - Version history
- ✅ `README.md` - Main documentation
- ✅ `INSTALLATION_GUIDE.txt` - Installation instructions

### Files That Should Stay in _internal:

- `MB.ico` - Application icon (used by .exe)
- `modules/` - Python modules (internal dependencies)
- All Python libraries and DLLs
- All other runtime dependencies

---

## Correct Distribution Structure

After build completion, verify this structure:

```
Supervertaler_v2.4.1/
├── Supervertaler.exe               ← Main executable
├── custom_prompts/                 ← ROOT (user-accessible)
│   ├── Cryptocurrency & Blockchain Specialist.json
│   ├── Financial Translation Specialist.json
│   ├── Gaming & Entertainment Specialist.json
│   ├── Legal Translation Specialist.json
│   ├── Marketing & Creative Translation.json
│   ├── Medical Translation Specialist.json
│   ├── Netherlands - Russian Federation BIT.json
│   └── Patent Translation Specialist.json
├── docs/                           ← ROOT (user-accessible)
│   ├── features/
│   │   ├── CAFETRAN_SUPPORT.md
│   │   └── MEMOQ_SUPPORT.md
│   ├── user_guides/
│   ├── README.md
│   └── ...
├── projects/                       ← ROOT (empty, for user files)
├── projects_private/               ← ROOT (empty, for user files)
├── api_keys.example.txt            ← ROOT (user-visible)
├── CHANGELOG.md                    ← ROOT (user-visible)
├── README.md                       ← ROOT (user-visible)
├── INSTALLATION_GUIDE.txt          ← ROOT (user-visible)
└── _internal/                      ← Internal files (hidden from user)
    ├── MB.ico
    ├── modules/
    │   ├── cafetran_docx_handler.py
    │   ├── docx_handler.py
    │   ├── mqxliff_handler.py
    │   ├── simple_segmenter.py
    │   ├── tag_manager.py
    │   └── __init__.py
    ├── base_library.zip
    ├── python312.dll
    └── ... (all other dependencies)
```

---

## Complete Build Command Sequence

Use this exact sequence for every build:

```powershell
# 1. Navigate to project directory
cd "c:\Users\mbeijer\My Drive\Software\Python\Supervertaler"

# 2. Clean everything (dist, build, old ZIP)
Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "Supervertaler_v2.4.1_Windows.zip" -Force -ErrorAction SilentlyContinue

# 3. Build executable with PyInstaller
pyinstaller Supervertaler.spec --noconfirm

# 4. Wait for build to complete (watch for "Build complete!" message)
# This takes about 60-90 seconds

# 5. CRITICAL: Run post-build script to copy user files to root
python post_build.py

# Expected output:
# ✅ Copied file: api_keys.example.txt
# ✅ Copied file: README.md
# ✅ Copied file: CHANGELOG.md
# ✅ Copied file: INSTALLATION_GUIDE.txt
# ✅ Copied folder: custom_prompts/ (8 items)
# ✅ Copied folder: docs/ (119 items)
# ✅ Copied folder: projects/ (16 items)
# ✅ Copied folder: projects_private/ (3 items)

# 6. Verify ROOT folder structure
Get-ChildItem "dist\Supervertaler_v2.4.1" | Format-Table Name

# Expected output:
# custom_prompts         (DIRECTORY)
# docs                   (DIRECTORY)
# projects               (DIRECTORY)
# projects_private       (DIRECTORY)
# _internal              (DIRECTORY)
# api_keys.example.txt   (FILE)
# CHANGELOG.md           (FILE)
# INSTALLATION_GUIDE.txt (FILE)
# README.md              (FILE)
# Supervertaler.exe      (FILE)

# 7. Create release ZIP
Compress-Archive -Path "dist\Supervertaler_v2.4.1" -DestinationPath "Supervertaler_v2.4.1_Windows.zip" -Force

# 8. Check ZIP size (should be ~47-50 MB)
Get-Item "Supervertaler_v2.4.1_Windows.zip" | Select-Object Name, @{Name="Size (MB)";Expression={[math]::Round($_.Length / 1MB, 2)}}
```

### ⚠️ IMPORTANT: Post-Build Script

The `post_build.py` script is **MANDATORY** and must be run after every PyInstaller build. It copies user-facing files from `_internal` to the root folder where users can easily access them.

**Why is this needed?**
PyInstaller's one-folder mode puts all data files in `_internal` by default. The post-build script moves user-accessible files (docs, custom prompts, README, etc.) to the root folder for better user experience.

---

## Verification Checklist

After build, verify:

### ✅ Root Folder Checks:
- [ ] `custom_prompts/` folder exists in root (NOT _internal)
- [ ] `docs/` folder exists in root (NOT _internal)
- [ ] `projects/` folder exists in root (NOT _internal)
- [ ] `projects_private/` folder exists in root (NOT _internal)
- [ ] `api_keys.example.txt` exists in root (NOT _internal)
- [ ] `CHANGELOG.md` exists in root (NOT _internal)
- [ ] `README.md` exists in root (NOT _internal)
- [ ] `INSTALLATION_GUIDE.txt` exists in root (NOT _internal)
- [ ] `Supervertaler.exe` exists in root

### ✅ _internal Folder Checks:
- [ ] `modules/` folder exists in _internal (NOT root)
- [ ] `MB.ico` exists in _internal (NOT root)
- [ ] `base_library.zip` exists in _internal
- [ ] Python DLLs exist in _internal

### ✅ Size Checks:
- [ ] ZIP file size: ~47-50 MB (expected range)
- [ ] Executable size: ~12-13 MB (expected range)

### ✅ Post-Build Script:
- [ ] `post_build.py` executed successfully
- [ ] All 4 files copied to root (README, CHANGELOG, INSTALLATION_GUIDE, api_keys.example.txt)
- [ ] All 4 folders copied to root (custom_prompts, docs, projects, projects_private)

---

## Common Issues & Solutions

### Issue: Files in _internal instead of root
**Symptoms:** `custom_prompts/`, `docs/`, etc. are in `_internal` folder  
**Cause:** Spec file COLLECT section not configured correctly  
**Solution:** Check `Supervertaler.spec` lines 106-122 - root files should be added separately with Tree() for folders and tuples for files

### Issue: Files in root instead of _internal
**Symptoms:** `modules/` folder or `MB.ico` in root folder  
**Cause:** Files added to COLLECT instead of Analysis datas  
**Solution:** Check `Supervertaler.spec` - `modules/` and `MB.ico` should be in `internal_files` list (line 15), NOT in COLLECT section

### Issue: Old files in new build
**Cause:** Didn't clean dist/build folders first  
**Solution:** Always run clean commands before building

### Issue: ZIP contains old version
**Cause:** Didn't delete old ZIP before creating new one  
**Solution:** Delete old ZIP in pre-build cleanup

### Issue: "ValueError: too many values to unpack"
**Cause:** Incorrect tuple unpacking in COLLECT section  
**Solution:** Use `('source', 'dest', 'DATA')` format, NOT `*[(...)]` format

---

## Spec File Configuration Reference

### For _internal files (line 14-19):
```python
internal_files = [
    ('MB.ico', '.'),  # Icon file used by exe
]
if os.path.exists('modules'):
    internal_files.append(('modules/*', 'modules'))
```

### For ROOT files (line 106-122):
```python
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    # Root files (tuples):
    ('api_keys.example.txt', 'api_keys.example.txt', 'DATA'),
    ('README.md', 'README.md', 'DATA'),
    ('CHANGELOG.md', 'CHANGELOG.md', 'DATA'),
    ('INSTALLATION_GUIDE.txt', 'INSTALLATION_GUIDE.txt', 'DATA'),
    # Root folders (Tree objects):
    Tree('custom_prompts', prefix='custom_prompts', excludes=[]),
    Tree('docs', prefix='docs', excludes=[]),
    Tree('projects', prefix='projects', excludes=[]),
    Tree('projects_private', prefix='projects_private', excludes=[]),
    ...
)
```

---

## Version-Specific Notes

### v2.4.1
- Icon: MB.ico (changed from Supervertaler.ico)
- New folders: custom_prompts, docs, projects, projects_private
- New file: INSTALLATION_GUIDE.txt
- Build size: ~53 MB (ZIP)
- Python: 3.12.6
- PyInstaller: 6.16.0

---

**Last Updated:** October 9, 2025  
**Build Configuration:** Supervertaler.spec (one-folder mode)

