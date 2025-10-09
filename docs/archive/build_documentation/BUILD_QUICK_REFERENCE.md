# Supervertaler v2.4.1 - Executable Build Quick Reference

## 🚀 Quick Build (One Command)

```powershell
python build_executable.py
```

**That's it!** The script handles everything automatically.

---

## 📋 What You Need First

### Install PyInstaller (once)
```powershell
pip install pyinstaller
```

### Install Pillow for Icon (once)
```powershell
pip install Pillow
```

---

## 🎯 Three Ways to Build

### 1. Automated (Recommended)
```powershell
python build_executable.py
```
✅ Full automation  
✅ Creates icon  
✅ Sets up folders  
✅ Includes docs  

### 2. Using Spec File
```powershell
pyinstaller Supervertaler.spec --clean
```
⚡ Faster (no checks)  
⚠️ Manual folder setup needed  

### 3. Command Line (Basic)
```powershell
pyinstaller --onedir --windowed --icon=Supervertaler.ico Supervertaler_v2.4.1.py
```
🔧 Custom control  
⚠️ No folder structure  

---

## 📁 Output Location

```
dist/Supervertaler_v2.4.1/
└── Supervertaler.exe  ← Double-click to run
```

---

## 🧪 Test the Build

```powershell
cd dist/Supervertaler_v2.4.1
.\Supervertaler.exe
```

---

## 📦 Create Distribution Package

```powershell
Compress-Archive -Path "dist/Supervertaler_v2.4.1" -DestinationPath "Supervertaler_v2.4.1_Windows.zip"
```

---

## 🔄 Rebuild After Changes

```powershell
python build_executable.py
```

Automatically cleans old build and creates fresh package.

---

## 🎨 Create Icon from Image

```powershell
python create_icon.py
```

Converts `Screenshots/Supervertaler_character.JPG` → `Supervertaler.ico`

---

## 📊 Typical Build Stats

| Item | Size | Time |
|------|------|------|
| Build process | - | 3-5 min |
| Supervertaler.exe | ~3 MB | - |
| Total package | ~150 MB | - |
| ZIP file | ~120 MB | - |

---

## ⚠️ Common Issues

### "Module not found"
→ Add to `hiddenimports` in `Supervertaler.spec`

### Icon not showing
→ Check `Supervertaler.ico` exists in project root

### Large file size
→ Normal! Includes Python + libraries

### Slow startup
→ Using `--onedir` (recommended) not `--onefile`

---

## 📖 Full Documentation

- **BUILD_INSTRUCTIONS.md** - Detailed build guide
- **DISTRIBUTION_GUIDE.md** - How to distribute
- **Supervertaler.spec** - PyInstaller config

---

## ✅ Build Checklist

Before distributing:

- [ ] Build completed
- [ ] Tested executable
- [ ] api_keys.txt is empty/example
- [ ] Docs included
- [ ] Create ZIP
- [ ] Upload to GitHub Releases

---

## 🆘 Help

If build fails:
1. Check dependencies: `pip list`
2. Try manual build: `pyinstaller Supervertaler.spec --clean`
3. Check `build.log` for errors
4. Contact: info@michaelbeijer.co.uk

---

**Ready?** Run `python build_executable.py` and you're done! 🎉
