# Supervertaler Installation Guide - macOS & Linux

**Complete installation instructions for macOS and Linux users**

---

## 📋 System Requirements

- **Operating System**: macOS 10.13+ or Linux (any modern distribution)
- **Python**: 3.8 or higher (3.12 recommended)
- **Disk Space**: ~50 MB for Supervertaler + dependencies
- **Internet**: Required for AI API calls
- **API Keys**: At least one of:
  - OpenAI (GPT-4, GPT-4 Turbo, etc.)
  - Anthropic (Claude 3.5 Sonnet, etc.)
  - Google (Gemini 1.5 Pro, etc.)

---

## 🍎 macOS Installation

### Step 1: Check Python Installation

Most Macs come with Python pre-installed. Check your version:

```bash
python3 --version
```

**Expected output**: `Python 3.8.0` or higher

**If Python is missing or outdated**:

**Option A - Homebrew** (recommended):
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Option B - Official Installer**:
1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer
3. Check "Add Python to PATH" during installation

### Step 2: Download Supervertaler

**Option A - Git (recommended)**:
```bash
# Install git if needed
brew install git

# Clone repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler
```

**Option B - Direct Download**:
1. Go to https://github.com/michaelbeijer/Supervertaler
2. Click green "Code" button → "Download ZIP"
3. Extract to your desired location
4. Open Terminal and navigate:
   ```bash
   cd ~/Downloads/Supervertaler-main
   ```

### Step 3: Install Dependencies

```bash
pip3 install anthropic openai google-generativeai python-docx pillow
```

**Expected output**:
```
Successfully installed anthropic-0.x.x openai-1.x.x google-generativeai-0.x.x python-docx-1.x.x pillow-10.x.x
```

**If pip3 command not found**:
```bash
python3 -m pip install anthropic openai google-generativeai python-docx pillow
```

### Step 4: Set Up API Keys

```bash
# Create your API keys file
cp api_keys.example.txt api_keys.txt

# Edit with TextEdit or your preferred editor
open -a TextEdit api_keys.txt
```

**Add your API keys** (get them from the providers - see [API Keys Setup Guide](API_KEYS_SETUP_GUIDE.md)): 

```
openai_api_key=sk-proj-xxxxxxxxxxxxx
claude_api_key=sk-ant-xxxxxxxxxxxxx
google_api_key=AIzaSyxxxxxxxxxxxxx
```
**Save the file** and close the editor.

### Step 5: Run Supervertaler

```bash
python3 Supervertaler_v2.4.1.py
```

**The GUI should launch!** 🎉

---

## 🐧 Linux Installation

### Step 1: Check Python Installation

```bash
python3 --version
```

**Expected output**: `Python 3.8.0` or higher

**If Python is missing or outdated**:

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

**Fedora/RHEL/CentOS**:
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

**Arch Linux**:
```bash
sudo pacman -S python python-pip tk
```

**openSUSE**:
```bash
sudo zypper install python3 python3-pip python3-tk
```

### Step 2: Install tkinter (GUI Support)

**Critical for Linux**: Python's tkinter is often separate:

**Ubuntu/Debian**:
```bash
sudo apt install python3-tk
```

**Fedora/RHEL**:
```bash
sudo dnf install python3-tkinter
```

**Arch Linux**:
```bash
sudo pacman -S tk
```

**Test tkinter**:
```bash
python3 -m tkinter
```
A small window should appear. Close it to continue.

### Step 3: Download Supervertaler

**Option A - Git (recommended)**:
```bash
# Install git if needed
sudo apt install git  # Ubuntu/Debian
# or
sudo dnf install git  # Fedora/RHEL

# Clone repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler
```

**Option B - Direct Download**:
```bash
wget https://github.com/michaelbeijer/Supervertaler/archive/refs/heads/main.zip
unzip main.zip
cd Supervertaler-main
```

### Step 4: Install Python Dependencies

```bash
pip3 install anthropic openai google-generativeai python-docx pillow
```

**If permission denied**:
```bash
pip3 install --user anthropic openai google-generativeai python-docx pillow
```

**Verify installation**:
```bash
python3 -c "import anthropic, openai, google.generativeai, docx, PIL; print('All dependencies installed successfully!')"
```

### Step 5: Set Up API Keys

```bash
# Create your API keys file
cp api_keys.example.txt api_keys.txt

# Edit with nano (or vim, gedit, etc.)
nano api_keys.txt
```

**Add your API keys**:
```
openai_api_key=sk-proj-xxxxxxxxxxxxx
claude_api_key=sk-ant-xxxxxxxxxxxxx
google_api_key=AIzaSyxxxxxxxxxxxxx
```

**Save**: Press `Ctrl+O`, `Enter`, then `Ctrl+X`

### Step 6: Run Supervertaler

```bash
python3 Supervertaler_v2.4.1.py
```

**The GUI should launch!** 🎉

---

## 🚀 Optional: Create Desktop Shortcuts

### macOS - Create .app Bundle

**Option 1 - Automator (Easy)**:

1. Open **Automator** (in Applications/Utilities)
2. Click **"New Document"** → **"Application"**
3. Search for **"Run Shell Script"** and drag it to the workflow
4. Paste this script:
   ```bash
   cd /Users/YOUR_USERNAME/path/to/Supervertaler
   /usr/bin/python3 Supervertaler_v2.4.1.py
   ```
   *Replace with your actual path*

5. Save as **"Supervertaler"** to Applications folder
6. **Optional - Add Custom Icon**:
   - Download icon from `Screenshots/Supervertaler character/supervertaler_icon_colours.png`
   - Right-click Supervertaler.app → Get Info
   - Drag PNG to icon in top-left corner

**Option 2 - Shell Script**:

Create `~/Desktop/supervertaler.command`:
```bash
#!/bin/bash
cd /Users/YOUR_USERNAME/path/to/Supervertaler
/usr/bin/python3 Supervertaler_v2.4.1.py
```

Make executable:
```bash
chmod +x ~/Desktop/supervertaler.command
```

Double-click to launch!

### Linux - Create Desktop Entry

**Method 1 - Desktop File**:

Create `~/.local/share/applications/supervertaler.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Supervertaler
Comment=AI-powered translation tool
Exec=/usr/bin/python3 /home/YOUR_USERNAME/path/to/Supervertaler/Supervertaler_v2.4.1.py
Path=/home/YOUR_USERNAME/path/to/Supervertaler
Icon=/home/YOUR_USERNAME/path/to/Supervertaler/Supervertaler.ico
Terminal=false
Categories=Office;Translation;Utility;
```

*Replace `YOUR_USERNAME` and path with actual values*

**Make executable**:
```bash
chmod +x ~/.local/share/applications/supervertaler.desktop
```

**Find in Applications Menu**: Search for "Supervertaler"

**Method 2 - Desktop Shortcut**:

```bash
# Copy to desktop
cp ~/.local/share/applications/supervertaler.desktop ~/Desktop/

# Allow launching
chmod +x ~/Desktop/supervertaler.desktop
```

Right-click → "Allow Launching" (Ubuntu) or "Trust This Application" (Fedora)

---

## 🔄 Updating Supervertaler

### Git Method (Recommended)

```bash
cd /path/to/Supervertaler
git pull origin main
```

**That's it!** Your installation is updated.

### Manual Method

1. Download latest ZIP from GitHub
2. Extract to temporary location
3. Copy new `Supervertaler_vX.X.X.py` to your installation
4. Copy any new files from `custom_prompts/` if desired
5. **Don't overwrite** your `api_keys.txt` or `projects/` folder!

---

## 🔧 Troubleshooting

### "No module named 'tkinter'"

**macOS**:
```bash
brew install python-tk@3.12  # or your Python version
```

**Linux**:
```bash
sudo apt install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora/RHEL
```

### "No module named 'anthropic'" (or other dependency)

**Reinstall dependencies**:
```bash
pip3 install --force-reinstall anthropic openai google-generativeai python-docx pillow
```

### "Permission denied" when installing packages

**Use --user flag**:
```bash
pip3 install --user anthropic openai google-generativeai python-docx pillow
```

### GUI doesn't launch / "command not found"

**Check Python path**:
```bash
which python3
```

**Use full path**:
```bash
/usr/bin/python3 Supervertaler_v2.4.1.py
```

### API calls fail / "Invalid API key"

**Check api_keys.txt**:
```bash
cat api_keys.txt
```

**Verify format** (no quotes, no spaces around `=`):
```
openai_api_key=sk-proj-xxxxx
```

**Test API key**:
```bash
python3 -c "from openai import OpenAI; client = OpenAI(api_key='YOUR_KEY'); print('API key valid!')"
```

### "ModuleNotFoundError: No module named '_tkinter'"

**macOS**:
```bash
brew reinstall python-tk
```

**Linux - rebuild Python with tk support**:
```bash
sudo apt install python3-dev tk-dev
pip3 install --force-reinstall tkinter
```

### Slow startup / "Analyzing dependencies"

**Normal behavior** on first run - Python loads AI libraries (may take 5-10 seconds)

**Subsequent runs are faster** (libraries cached)

---

## 🎯 Quick Command Reference

### Run Supervertaler
```bash
cd /path/to/Supervertaler
python3 Supervertaler_v2.4.1.py
```

### Update from Git
```bash
cd /path/to/Supervertaler
git pull
```

### Reinstall Dependencies
```bash
pip3 install --force-reinstall anthropic openai google-generativeapi python-docx pillow
```

### Check Python Version
```bash
python3 --version
```

### Test tkinter
```bash
python3 -m tkinter
```

### View API Keys
```bash
cat api_keys.txt
```

---

## 📚 Next Steps

1. **Get API Keys**: See [API_KEYS_SETUP_GUIDE.md](API_KEYS_SETUP_GUIDE.md)
2. **Read User Guide**: [`Supervertaler User Guide (v2.4.0).md`](../../Supervertaler%20User%20Guide%20(v2.4.0).md)
3. **Try Bilingual Workflow**: [BILINGUAL_WORKFLOW_QUICK_START.md](BILINGUAL_WORKFLOW_QUICK_START.md)
4. **Explore Custom Prompts**: Check `custom_prompts/` folder

---

## 💡 Pro Tips

### Virtual Environment (Optional but Recommended)

Isolate Supervertaler dependencies:

```bash
cd /path/to/Supervertaler

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install anthropic openai google-generativeai python-docx pillow

# Run Supervertaler
python Supervertaler_v2.4.1.py

# Deactivate when done
deactivate
```

**Why?** Prevents conflicts with other Python projects.

### Alias for Quick Launch

**macOS/Linux** - Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias supervertaler='cd /path/to/Supervertaler && python3 Supervertaler_v2.4.1.py'
```

**Then just type**:
```bash
supervertaler
```

### Watch for Updates

**Enable GitHub notifications**:
1. Go to https://github.com/michaelbeijer/Supervertaler
2. Click "Watch" → "Releases only"
3. Get email when new versions are released

---

## 🐛 Still Having Issues?

1. **Check the FAQ**: [Common issues and solutions](../../README.md#troubleshooting)
2. **GitHub Issues**: https://github.com/michaelbeijer/Supervertaler/issues
3. **Email Support**: info@michaelbeijer.co.uk

**When reporting issues, include**:
- Operating system and version
- Python version (`python3 --version`)
- Error message (full text)
- Steps to reproduce

---

## 🎉 You're All Set!

Supervertaler is now installed and ready to use. Happy translating! 🚀

**Remember**: Your API keys stay on your machine. All processing is local except AI API calls.

---

**Last Updated**: October 8, 2025  
**Version**: Supervertaler v2.4.1
