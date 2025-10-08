# Cross-Platform Distribution Guide

**How to support Windows, macOS, and Linux users**

---

## 🌍 Current Situation

✅ **Windows**: Standalone `.exe` available (v2.4.1)  
⚠️ **macOS**: Python script only (requires Python installation)  
⚠️ **Linux**: Python script only (requires Python installation)  

---

## 📊 Options for Mac & Linux Users

### Option 1: Python Script (Current - Recommended for Now)

**Best for**: Technical users, developers, power users

**Advantages**:
- ✅ Works on ALL platforms (Windows, macOS, Linux)
- ✅ Always up-to-date (no build delays)
- ✅ Smaller download (~1 MB vs 50+ MB)
- ✅ Easy to inspect/modify source code
- ✅ No PyInstaller platform-specific builds needed

**User Requirements**:
- Python 3.8+ installed
- pip for installing dependencies
- Basic command-line knowledge

**Installation Instructions** (include in README):

```markdown
## 📥 Installation for macOS & Linux

### Quick Start (5 minutes)

1. **Install Python** (if not already installed):
   - **macOS**: 
     ```bash
     brew install python3
     # or download from python.org
     ```
   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip python3-tk
     ```
   - **Linux (Fedora/RHEL)**:
     ```bash
     sudo dnf install python3 python3-pip python3-tkinter
     ```

2. **Download Supervertaler**:
   ```bash
   git clone https://github.com/michaelbeijer/Supervertaler.git
   cd Supervertaler
   ```
   *Or download ZIP from GitHub and extract*

3. **Install Dependencies**:
   ```bash
   pip3 install anthropic openai google-generativeai python-docx pillow
   ```

4. **Set Up API Keys**:
   ```bash
   cp api_keys.example.txt api_keys.txt
   nano api_keys.txt  # or use your preferred editor
   ```

5. **Run Supervertaler**:
   ```bash
   python3 Supervertaler_v2.4.1.py
   ```

### Create Desktop Shortcut (Optional)

**macOS**:
1. Open Automator → New Document → Application
2. Add "Run Shell Script"
3. Paste:
   ```bash
   cd /path/to/Supervertaler
   /usr/bin/python3 Supervertaler_v2.4.1.py
   ```
4. Save as "Supervertaler.app" in Applications
5. Right-click → Get Info → drag custom icon

**Linux**:
Create `~/.local/share/applications/supervertaler.desktop`:
```ini
[Desktop Entry]
Type=Application
Name=Supervertaler
Exec=/usr/bin/python3 /path/to/Supervertaler/Supervertaler_v2.4.1.py
Icon=/path/to/Supervertaler/Supervertaler.ico
Terminal=false
Categories=Office;Translation;
```
```

---

### Option 2: Build Platform-Specific Executables

**Best for**: Non-technical users on Mac/Linux

**Pros**:
- ✅ No Python installation needed
- ✅ Double-click to run
- ✅ Professional user experience

**Cons**:
- ❌ Requires Mac/Linux machine for building
- ❌ 3 separate builds to maintain (Windows/Mac/Linux)
- ❌ Large file sizes (50+ MB per platform)
- ❌ macOS notarization costs $99/year (Apple Developer account)
- ❌ Time-consuming (build + test on each platform)

**How to Create**:

#### macOS (.app bundle)

**Requirements**:
- macOS computer (or macOS VM)
- PyInstaller installed
- Apple Developer account ($99/year for code signing - optional but recommended)

**Build Process**:
```bash
# On macOS machine
pip3 install pyinstaller pillow

# Create macOS .app
pyinstaller --name=Supervertaler \
    --onedir \
    --windowed \
    --icon=Supervertaler.icns \
    --add-data "api_keys.example.txt:." \
    --add-data "custom_prompts:custom_prompts" \
    --add-data "docs/user_guides:docs/user_guides" \
    Supervertaler_v2.4.1.py

# Result: dist/Supervertaler.app
# Compress: zip -r Supervertaler_v2.4.1_macOS.zip dist/Supervertaler.app
```

**Note**: macOS may show "unidentified developer" warning unless you:
1. Pay $99/year for Apple Developer account
2. Code-sign the app
3. Notarize with Apple (automated via `xcrun notarytool`)

#### Linux (AppImage or standalone)

**Requirements**:
- Linux machine (or VM)
- PyInstaller installed

**Build Process**:
```bash
# On Linux machine
pip3 install pyinstaller pillow

# Create Linux executable
pyinstaller --name=Supervertaler \
    --onedir \
    --windowed \
    --icon=Supervertaler.ico \
    --add-data "api_keys.example.txt:." \
    --add-data "custom_prompts:custom_prompts" \
    --add-data "docs/user_guides:docs/user_guides" \
    Supervertaler_v2.4.1.py

# Result: dist/Supervertaler/Supervertaler
# Package: tar -czf Supervertaler_v2.4.1_Linux.tar.gz -C dist Supervertaler
```

**Distribution Options**:
- `.tar.gz` - traditional Unix format
- AppImage - single-file, no installation needed
- Snap/Flatpak - sandboxed, auto-updates

---

### Option 3: Docker Container

**Best for**: Consistent cross-platform experience

**Pros**:
- ✅ Works on Windows, Mac, Linux
- ✅ Isolated environment
- ✅ Reproducible builds
- ✅ Easy version management

**Cons**:
- ❌ Requires Docker installation
- ❌ More complex for non-technical users
- ❌ GUI apps need X11 forwarding (complex)
- ❌ Not ideal for desktop GUI apps

**Verdict**: Not recommended for Supervertaler (GUI-focused application)

---

### Option 4: Web-Based Version

**Best for**: Maximum accessibility

**Pros**:
- ✅ Works on ALL platforms (including mobile!)
- ✅ No installation whatsoever
- ✅ Always latest version
- ✅ Centralized updates

**Cons**:
- ❌ Requires web framework (Flask/Django/FastAPI)
- ❌ Hosting costs
- ❌ API key security concerns
- ❌ Complete rewrite (tkinter → HTML/CSS/JavaScript)
- ❌ Users must trust server with API keys

**Verdict**: Future enhancement, significant development effort

---

## 🎯 Recommended Approach

### Current Release (v2.4.1)

**For Windows Users**:
→ **Standalone .exe** (GitHub Releases)

**For macOS & Linux Users**:
→ **Python script** with clear installation instructions

### Why This Approach?

1. **Most users are on Windows** (translation industry is 70%+ Windows)
2. **Mac/Linux users are typically more technical** (comfortable with Python)
3. **Avoid maintenance burden** of 3 separate builds
4. **Lower barrier to contribution** (all platforms can run source code)
5. **Faster bug fixes** (no rebuild delays for Mac/Linux)

---

## 📝 Updated README Structure

Add this to your README.md:

```markdown
## 📥 Download & Installation

### Windows (Easiest - No Python Required)

**[⬇️ Download Supervertaler v2.4.1 for Windows](https://github.com/michaelbeijer/Supervertaler/releases/latest)**

1. Download `Supervertaler_v2.4.1_Windows.zip`
2. Extract to any folder
3. Edit `api_keys.txt` with your API keys
4. Double-click `Supervertaler.exe`

### macOS & Linux (Python Required)

**Requirements**: Python 3.8+, pip, tkinter

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/michaelbeijer/Supervertaler.git
   cd Supervertaler
   ```

2. **Install dependencies**:
   ```bash
   pip3 install anthropic openai google-generativeai python-docx pillow
   ```
   
   **Linux users**: Also install tkinter:
   - Ubuntu/Debian: `sudo apt install python3-tk`
   - Fedora: `sudo dnf install python3-tkinter`
   - Arch: `sudo pacman -S tk`

3. **Set up API keys**:
   ```bash
   cp api_keys.example.txt api_keys.txt
   # Edit api_keys.txt with your API keys
   ```

4. **Run**:
   ```bash
   python3 Supervertaler_v2.4.1.py
   ```

📖 **Detailed setup guide**: [docs/user_guides/INSTALLATION_LINUX_MACOS.md](docs/user_guides/INSTALLATION_LINUX_MACOS.md)

---

### 🍎 Want a macOS .app or Linux executable?

**Good news**: You can build one yourself! See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

Or vote for official builds: [Issue #XX - macOS/Linux Executables](link-to-issue)

If there's enough demand (10+ users), I'll create official builds for all platforms.
```

---

## 🚀 Future: Multi-Platform Builds (If Needed)

### When to Consider Official Mac/Linux Builds:

- ✅ **10+ users request it** (create GitHub issue to track demand)
- ✅ **You have access to Mac/Linux machines** (or CI/CD like GitHub Actions)
- ✅ **User base justifies maintenance effort**

### Automated Multi-Platform Builds (Advanced)

Use **GitHub Actions** to build on all platforms automatically:

```yaml
# .github/workflows/build.yml
name: Build Executables

on:
  release:
    types: [created]

jobs:
  build:
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install pyinstaller pillow anthropic openai google-generativeai python-docx
      
      - name: Build executable
        run: python build_executable.py
      
      - name: Upload to release
        uses: actions/upload-release-asset@v1
        # ... upload logic
```

**Benefits**:
- ✅ Automated builds on push/release
- ✅ No need for Mac/Linux machines
- ✅ Consistent build environment
- ✅ Free for open-source projects

---

## 📊 Platform Statistics (Translation Industry)

Based on industry data:
- **Windows**: ~70% of professional translators
- **macOS**: ~25% of professional translators
- **Linux**: ~5% of professional translators

**Recommendation**: Focus on Windows first, add Mac/Linux if demand grows.

---

## ✅ Action Items

### Now (v2.4.1):

- [x] Create Windows executable ✅ DONE
- [ ] Update README with Mac/Linux installation instructions
- [ ] Create detailed Mac/Linux setup guide
- [ ] Add "Request Mac/Linux builds" issue template

### Future (v2.5.0+):

- [ ] Gauge interest for Mac/Linux executables (GitHub issue)
- [ ] Set up GitHub Actions for automated builds (if demand exists)
- [ ] Create macOS .app (if 10+ Mac users request it)
- [ ] Create Linux AppImage (if 10+ Linux users request it)

---

## 💡 Bottom Line

**For v2.4.1**: 
- Windows users get an executable
- Mac/Linux users use the Python script (with clear instructions)

**This is standard practice** for many open-source projects:
- GitHub Desktop: Windows/Mac binaries, Linux uses source
- VS Code: All platforms, but started Windows-only
- Many Python tools: Source-first, executables on demand

**When you have 100+ users**, revisit multi-platform executables. For now, Python script works great for Mac/Linux users! 🚀
