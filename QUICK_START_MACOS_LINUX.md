# Quick Start - macOS & Linux

**Get Supervertaler running in 5 minutes!**

---

## ⚡ Express Installation

### macOS
```bash
# 1. Install dependencies (if needed)
brew install python3

# 2. Clone & navigate
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# 3. Install Python packages
pip3 install anthropic openai google-generativeai python-docx pillow

# 4. Set up API keys
cp api_keys.example.txt api_keys.txt
open -a TextEdit api_keys.txt  # Add your keys and save

# 5. Run!
python3 Supervertaler_v2.4.1.py
```

### Linux (Ubuntu/Debian)
```bash
# 1. Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-tk git

# 2. Clone & navigate
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# 3. Install Python packages
pip3 install anthropic openai google-generativeai python-docx pillow

# 4. Set up API keys
cp api_keys.example.txt api_keys.txt
nano api_keys.txt  # Add your keys, Ctrl+O to save, Ctrl+X to exit

# 5. Run!
python3 Supervertaler_v2.4.1.py
```

### Linux (Fedora/RHEL)
```bash
# 1. Install dependencies
sudo dnf install python3 python3-pip python3-tkinter git

# 2-5. Same as Ubuntu above
```

---

## 🔑 Get API Keys (Choose One or More)

**OpenAI** (GPT-4, GPT-4 Turbo):
- https://platform.openai.com/api-keys
- Click "Create new secret key"
- Copy key starting with `sk-proj-`

**Anthropic** (Claude 3.5 Sonnet):
- https://console.anthropic.com/
- Click "Get API Keys"
- Copy key starting with `sk-ant-`

**Google** (Gemini 1.5 Pro):
- https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy key starting with `AIzaSy`

**Add to api_keys.txt**:
```
openai_api_key=sk-proj-xxxxxxxxxxxxx
anthropic_api_key=sk-ant-xxxxxxxxxxxxx
google_api_key=AIzaSyxxxxxxxxxxxxx
```

---

## 🎯 Daily Usage

### Launch Supervertaler
```bash
cd /path/to/Supervertaler
python3 Supervertaler_v2.4.1.py
```

### Update to Latest Version
```bash
cd /path/to/Supervertaler
git pull
```

---

## 🚀 Create Desktop Shortcut (Optional)

### macOS - Automator App

1. Open **Automator** → New **Application**
2. Add **"Run Shell Script"**
3. Paste:
   ```bash
   cd /Users/YOUR_USERNAME/Supervertaler
   /usr/bin/python3 Supervertaler_v2.4.1.py
   ```
4. Save as "Supervertaler" in Applications
5. Now in Spotlight: Type "Supervertaler" → Enter

### Linux - Desktop Entry

Create `~/.local/share/applications/supervertaler.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Supervertaler
Exec=python3 /home/YOUR_USERNAME/Supervertaler/Supervertaler_v2.4.1.py
Path=/home/YOUR_USERNAME/Supervertaler
Terminal=false
Categories=Office;Translation;
```

Make executable:
```bash
chmod +x ~/.local/share/applications/supervertaler.desktop
```

Now in Applications Menu: Search "Supervertaler"

---

## ⚠️ Troubleshooting

### "No module named 'tkinter'"
**macOS**: `brew install python-tk`  
**Linux**: `sudo apt install python3-tk` (Ubuntu) or `sudo dnf install python3-tkinter` (Fedora)

### "No module named 'anthropic'"
```bash
pip3 install --force-reinstall anthropic openai google-generativeai python-docx pillow
```

### "Permission denied"
```bash
pip3 install --user anthropic openai google-generativeai python-docx pillow
```

### GUI doesn't appear
Test tkinter: `python3 -m tkinter` (should show small window)

---

## 📚 Full Documentation

- **Complete Installation Guide**: [docs/user_guides/INSTALLATION_LINUX_MACOS.md](docs/user_guides/INSTALLATION_LINUX_MACOS.md)
- **User Guide**: [Supervertaler User Guide (v2.4.0).md](Supervertaler%20User%20Guide%20(v2.4.0).md)
- **API Keys Setup**: [docs/user_guides/API_KEYS_SETUP_GUIDE.md](docs/user_guides/API_KEYS_SETUP_GUIDE.md)
- **Bilingual Workflow**: [docs/user_guides/BILINGUAL_WORKFLOW_QUICK_START.md](docs/user_guides/BILINGUAL_WORKFLOW_QUICK_START.md)

---

## 🍎🐧 Want a Native App?

**Vote for macOS/Linux executables!**

Currently available:
- ✅ Windows `.exe` (no Python needed)
- ⚠️ Mac/Linux: Python script (what you're using now)

**Request native builds**:
1. Go to https://github.com/michaelbeijer/Supervertaler/issues
2. Find "Request macOS/Linux Executable" issue
3. 👍 Thumbs up to vote!

**When we reach 10+ votes**, official builds will be created! 🎉

**Or build your own** (15 minutes):
```bash
pip install pyinstaller
python build_executable.py
# Result: dist/Supervertaler.app (macOS) or dist/Supervertaler/ (Linux)
```

---

## ✅ You're Ready!

Launch Supervertaler and start translating! 🚀

**Questions?** info@michaelbeijer.co.uk  
**Issues?** https://github.com/michaelbeijer/Supervertaler/issues

---

**Last Updated**: October 8, 2025  
**Version**: v2.4.1
