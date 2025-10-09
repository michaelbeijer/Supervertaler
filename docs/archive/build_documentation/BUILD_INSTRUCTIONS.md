# Building Supervertaler Executable - Instructions

This guide explains how to build a distributable executable version of Supervertaler v2.4.1 that users can run without installing Python.

---

## 🎯 Overview

The build process creates a standalone package containing:
- `Supervertaler.exe` - Main executable (no Python required)
- All necessary files and folders
- User guides and documentation
- Installation instructions

**Result**: A folder users can extract and run immediately by double-clicking `Supervertaler.exe`

---

## 📋 Prerequisites

### 1. Install Python Dependencies

First, ensure you have all required packages installed:

```powershell
# Install PyInstaller (builds the executable)
pip install pyinstaller

# Install Pillow (for icon creation)
pip install Pillow

# Install Supervertaler dependencies (if not already installed)
pip install anthropic google-generativeai openai python-docx
```

### 2. Verify Installation

Check that PyInstaller is installed:

```powershell
pyinstaller --version
```

You should see something like: `6.x.x`

---

## 🚀 Quick Build (Automated)

### Option 1: Use the Build Script (RECOMMENDED)

The easiest way is to use the automated build script:

```powershell
# Navigate to the Supervertaler directory
cd "C:\Users\mbeijer\My Drive\Software\Python\Supervertaler"

# Run the build script
python build_executable.py
```

The script will:
1. ✅ Check all dependencies
2. ✅ Create the application icon
3. ✅ Clean previous builds
4. ✅ Build the executable
5. ✅ Set up user folders
6. ✅ Create installation guide

**Build time**: 3-5 minutes

**Output**: `dist/Supervertaler_v2.4.1/` folder ready for distribution

---

## 🔧 Manual Build (Step by Step)

If you prefer to build manually or troubleshoot issues:

### Step 1: Create Icon

```powershell
# Create icon from your character image
python create_icon.py
```

This creates `Supervertaler.ico` from `Screenshots/Supervertaler_character.JPG`

### Step 2: Build with PyInstaller

```powershell
# Build using the spec file
pyinstaller Supervertaler.spec --clean
```

### Step 3: Set Up User Folders

```powershell
# Navigate to the output directory
cd "dist/Supervertaler_v2.4.1"

# Create user data folders
New-Item -ItemType Directory -Path "custom_prompts_private", "projects", "projects_private"

# Copy api_keys example to create editable version
Copy-Item "api_keys.example.txt" "api_keys.txt"
```

---

## 📦 What Gets Built

### Output Structure

```
dist/Supervertaler_v2.4.1/
├── Supervertaler.exe                    ← Main executable
├── api_keys.txt                         ← User edits this
├── api_keys.example.txt
├── README.md
├── CHANGELOG.md
├── INSTALLATION_GUIDE.txt               ← For end users
├── custom_prompts/                      ← Pre-made prompts
├── custom_prompts_private/              ← User's private prompts
├── projects/                            ← User's projects
├── projects_private/                    ← User's private projects
├── docs/
│   └── user_guides/
│       ├── Supervertaler User Guide (v2.4.0).md
│       ├── BILINGUAL_WORKFLOW_QUICK_START.md
│       └── API_KEYS_SETUP_GUIDE.md
└── _internal/                           ← PyInstaller dependencies
    ├── python312.dll
    ├── (many other files)
    └── ...
```

### File Sizes (Approximate)

- **Supervertaler.exe**: ~2-5 MB
- **_internal/ folder**: ~100-150 MB (Python runtime + libraries)
- **Total package**: ~150-200 MB

---

## 🧪 Testing the Build

### 1. Test Locally

```powershell
# Navigate to the built package
cd "dist/Supervertaler_v2.4.1"

# Run the executable
.\Supervertaler.exe
```

**Checklist**:
- [ ] Application launches without errors
- [ ] GUI displays correctly
- [ ] Can load projects
- [ ] Can access custom prompts
- [ ] API keys can be edited in api_keys.txt
- [ ] Translation functions work (if API keys configured)

### 2. Test on Clean Machine (Recommended)

To ensure it works without Python installed:
1. Copy the `Supervertaler_v2.4.1` folder to a USB drive
2. Test on a computer without Python installed
3. Verify all functionality works

---

## 📤 Distribution

### Option 1: ZIP File (Simple)

```powershell
# Create a ZIP file for distribution
Compress-Archive -Path "dist/Supervertaler_v2.4.1" -DestinationPath "Supervertaler_v2.4.1_Windows.zip"
```

Users download, extract, and run.

### Option 2: Installer (Professional)

For a more professional installation experience, use **Inno Setup**:

1. Download Inno Setup: https://jwilder.github.io/innosetup/
2. Create an installer script (we can create this later)
3. Build a Setup.exe that installs Supervertaler

**Benefits**:
- Professional installation wizard
- Creates Start Menu shortcuts
- Adds to Programs and Features
- Includes uninstaller

### Option 3: GitHub Release

Upload to GitHub Releases:

```powershell
# Create release ZIP
Compress-Archive -Path "dist/Supervertaler_v2.4.1" -DestinationPath "Supervertaler_v2.4.1_Windows.zip"

# Then:
# 1. Go to GitHub > Releases > Create new release
# 2. Tag: v2.4.1
# 3. Title: Supervertaler v2.4.1 - Standalone Windows Executable
# 4. Upload the ZIP file
# 5. Publish release
```

---

## 🔍 Troubleshooting

### Problem: "Module not found" error

**Solution**: Add the missing module to `hiddenimports` in `Supervertaler.spec`:

```python
hiddenimports=[
    'tkinter',
    'missing_module_name',  # Add here
    ...
],
```

Then rebuild.

### Problem: Icon not showing

**Solution**: 
1. Verify `Supervertaler.ico` exists in the project root
2. Check the spec file has: `icon='Supervertaler.ico'`
3. Rebuild with `--clean` flag

### Problem: Large file size

**Solution**: The executable is large because it includes Python and all libraries. This is normal. To reduce size:

1. Remove unused packages from `hiddenimports`
2. Use UPX compression (enabled by default in spec file)
3. Exclude large packages you don't need (already done in spec)

### Problem: Slow startup

**Solution**: Use `--onedir` mode (already configured). One-file mode (`--onefile`) is slower because it extracts to temp every time.

### Problem: Antivirus blocking

**Solution**: This is common for PyInstaller executables:
1. Submit to antivirus vendor as false positive
2. Code-sign the executable (requires certificate)
3. Users can whitelist the application

---

## 🎨 Customizing the Icon

If you want to use a different image:

```powershell
# Run the icon creator interactively
python create_icon.py

# When prompted, enter the path to your image
# Example: Screenshots/my_custom_logo.png
```

Supported formats: JPG, PNG, BMP, GIF

---

## 📝 Build Checklist

Before distributing:

- [ ] All dependencies installed
- [ ] Icon created and looks good
- [ ] Build completes without errors
- [ ] Executable tested on development machine
- [ ] Executable tested on clean machine (no Python)
- [ ] api_keys.txt is present and editable
- [ ] All user guides included
- [ ] INSTALLATION_GUIDE.txt is clear
- [ ] Package zipped for distribution
- [ ] Version number is correct in all files

---

## 🔄 Rebuilding After Changes

If you modify `Supervertaler_v2.4.1.py`:

```powershell
# Quick rebuild
python build_executable.py

# Or manually
pyinstaller Supervertaler.spec --clean
```

---

## 📊 Build Script Options

The `build_executable.py` script accepts no arguments (fully automated), but you can modify it to:

- Skip icon creation (if icon exists)
- Keep previous builds
- Create different package names
- Add version info to executable

---

## 🆘 Getting Help

If you encounter issues:

1. Check the PyInstaller documentation: https://pyinstaller.org/
2. Review the build log for error messages
3. Test with a simple script first
4. Contact: info@michaelbeijer.co.uk

---

## 📄 Files Reference

| File | Purpose |
|------|---------|
| `build_executable.py` | Automated build script |
| `create_icon.py` | Convert image to .ico |
| `Supervertaler.spec` | PyInstaller configuration |
| `BUILD_INSTRUCTIONS.md` | This file |

---

**Next**: After successful build, see `DISTRIBUTION_GUIDE.md` for publishing instructions.
