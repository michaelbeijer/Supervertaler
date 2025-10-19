# Building Supervertaler Executable (.exe)

This guide explains how to build a standalone Windows executable for Supervertaler using PyInstaller.

## Quick Start

```bash
# Navigate to project root
cd c:\Dev\Supervertaler

# Run the build script
python build_exe.py
```

**Output**: `dist/Supervertaler.exe` (~150-180 MB)

## What's Included in the .exe

- Python 3.12 runtime (embedded, not required on user system)
- All Python dependencies (PIL, docx, openpyxl, openai, anthropic, google-generativeai)
- tkinter GUI framework
- All documentation (README, FAQ, CHANGELOG, guides)
- Example configuration files
- All modules and helper scripts

## Users Don't Need

- Python installed
- pip or package manager
- Any dependencies configured
- Command line knowledge

**Users Just Need**: Windows 10/11 and an internet connection (for AI API calls)

## Detailed Build Process

### Prerequisites

```bash
# 1. Python 3.12 or higher
python --version

# 2. PyInstaller
pip install pyinstaller

# 3. (Optional) Build wheel/source distribution
pip install build twine
```

### Manual Build (if using build_exe.py fails)

```bash
# Navigate to project root
cd c:\Dev\Supervertaler

# Clean previous builds
Remove-Item -Path ".\dist", ".\build" -Recurse -Force -ErrorAction SilentlyContinue

# Run PyInstaller directly
pyinstaller `
  --onefile `
  --windowed `
  --name=Supervertaler `
  --distpath=".\dist" `
  --workpath=".\build" `
  --exclude-module=PyQt6 `
  --add-data="assets;assets" `
  --add-data="modules;modules" `
  --add-data="docs;docs" `
  --add-data="README.md;." `
  --add-data="CHANGELOG.md;." `
  --add-data="FAQ.md;." `
  --add-data="api_keys.example.txt;." `
  Supervertaler_v3.7.0.py
```

### Build Output

- **Location**: `dist/Supervertaler.exe`
- **Size**: 150-180 MB (includes Python runtime + all dependencies)
- **Time**: 3-5 minutes typical
- **Compatibility**: Windows 10 SP1+, Windows 11

## For CI/CD / Automation

### GitHub Actions Example

```yaml
name: Build Supervertaler Executable

on:
  release:
    types: [published]

jobs:
  build-exe:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: pip install pyinstaller
      
      - name: Build executable
        run: python build_exe.py
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: Supervertaler.exe
          path: dist/Supervertaler.exe
```

### AppVeyor / Azure Pipelines

Similar approach - install Python 3.12, run `pip install pyinstaller`, then `python build_exe.py`.

## Distribution

### Direct Download
1. Build the .exe locally
2. Upload to GitHub Releases
3. Users download and run directly
4. No Python knowledge required

### Optional: Code Signing
For professional distribution, consider signing the .exe:
```bash
# Requires certificate
signtool sign /f certificate.pfx /p password /t http://timestamp.authority Supervertaler.exe
```

## Troubleshooting

### Build fails with "PyQt6 conflict"
- **Cause**: Multiple Qt bindings installed
- **Solution**: Use `--exclude-module=PyQt6` (already in scripts)

### .exe is too large (>300 MB)
- **Cause**: Unnecessary packages included
- **Solution**: Reduce with `--exclude-module=numpy`, `--exclude-module=pandas`

### .exe won't start
- **Cause**: Missing dependencies or antivirus blocking
- **Solution**: Run from terminal to see error messages
- **Antivirus**: Add exception for Supervertaler.exe

### "Module not found" when running .exe
- **Cause**: Hidden imports not included
- **Solution**: Add to `hidden_imports` in build command
- **Example**: `--hidden-import=PIL --hidden-import=docx`

## Verification

After building, test the executable:

```bash
# Run from command line to see output
.\dist\Supervertaler.exe

# Check file properties
Get-Item .\dist\Supervertaler.exe | Select-Object Name, Length, LastWriteTime
```

## Release Checklist

- [ ] Python 3.12 installed and working
- [ ] PyInstaller installed (`pip install pyinstaller`)
- [ ] Repository in clean state (no unsaved changes)
- [ ] Version updated in Supervertaler_v3.7.0.py (`APP_VERSION = "3.7.0"`)
- [ ] Run `python build_exe.py`
- [ ] Test the resulting .exe
- [ ] No errors in build output
- [ ] .exe size reasonable (150-200 MB)
- [ ] Ready to upload to GitHub Releases

## Advanced Options

### Reduce File Size

```bash
pyinstaller --onefile --windowed --strip \
  --exclude-module=numpy \
  --exclude-module=pandas \
  Supervertaler_v3.7.0.py
```

### Add Custom Icon

1. Prepare icon: `assets/icon.ico` (256x256 or larger, .ico format)
2. Add flag: `--icon=assets/icon.ico`

### Use UPX Compression (Optional)

1. Install UPX: https://upx.github.io/
2. PyInstaller uses automatically if available
3. Can reduce size by 30-40%

### Debug Build (for troubleshooting)

```bash
pyinstaller --onefile --windowed --debug=all \
  Supervertaler_v3.7.0.py
```

## Support

- **PyInstaller Docs**: https://pyinstaller.org/
- **Issues**: Report via GitHub: https://github.com/michaelbeijer/Supervertaler/issues
- **Questions**: Open GitHub Discussion

## Next Steps

After building the .exe:

1. **Test thoroughly** on clean Windows 10/11 systems
2. **Upload to GitHub Releases** (attach .exe file)
3. **Create release announcement** with download link
4. **Update website** with download instructions
5. **Share on translation communities** (ProZ, TranslatorsCafe, etc.)

---

*For detailed info on distributing the executable, see: [Distribution Guide](DISTRIBUTION.md)*
