# Supervoice Deployment Guide

## Overview

**Supervoice** is Supervertaler's voice dictation module for hands-free translation input.

Supervoice uses OpenAI Whisper for speech recognition. Whisper requires **FFmpeg** to process audio files. This guide explains how to handle FFmpeg and Whisper models for different deployment scenarios.

## For Developers (Running from Source)

If someone clones your repo and runs Supervertaler:

### Requirements
1. **Python packages** (installed via pip):
   - `openai-whisper`
   - `sounddevice`
   - `numpy`
   - `PyAudio` (optional, for some audio backends)

2. **FFmpeg** (must be installed separately):
   - **Windows**: `winget install FFmpeg` or `choco install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` or `sudo yum install ffmpeg`
   - **macOS**: `brew install ffmpeg`

### What Happens Without FFmpeg?
- First dictation attempt will show a user-friendly error dialog
- Error message includes installation instructions
- All other Supervertaler features work normally

### Whisper Model Downloads

Whisper speech recognition models are **not** included in the repository. They download automatically on first use.

**Model Sizes & Download Locations:**

| Model | Download Size | RAM Usage | Storage Location |
|-------|--------------|-----------|------------------|
| tiny | 75 MB | ~1 GB | `%USERPROFILE%\.cache\whisper` |
| base | 142 MB | ~1 GB | `%USERPROFILE%\.cache\whisper` |
| small | 466 MB | ~2 GB | `%USERPROFILE%\.cache\whisper` |
| medium | 1.5 GB | ~5 GB | `%USERPROFILE%\.cache\whisper` |
| large | 2.9 GB | ~10 GB | `%USERPROFILE%\.cache\whisper` |

**On Windows:** Models stored in `C:\Users\<username>\.cache\whisper\`
**On Linux/Mac:** Models stored in `~/.cache/whisper/`

**First Use Experience:**
- User selects model in Settings → 🎤 Supervoice
- First dictation triggers automatic download
- Progress shown in console/log
- Subsequent uses are instant (model cached)

---

## For .exe Distribution (Bundled Release)

You have **two options** for distributing Supervertaler as a standalone .exe:

### Option 1: Bundle FFmpeg (Recommended)

**Pros:**
- Users don't need to install anything
- Works out of the box
- Best user experience

**Cons:**
- Adds ~70 MB to .exe size
- Slightly larger download

**Steps:**

1. **Download FFmpeg static binary**:
   - Get from: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip` (Windows)
   - Extract `ffmpeg.exe` from `bin/` folder

2. **Add to your project**:
   ```
   C:\Dev\Supervertaler\
   ├── binaries\
   │   └── ffmpeg.exe      (place here)
   ├── modules\
   ├── Supervertaler.py
   └── ...
   ```

3. **Update PyInstaller spec** (if using PyInstaller):
   ```python
   # In your .spec file:
   a = Analysis(
       ['Supervertaler.py'],
       datas=[
           ('binaries/ffmpeg.exe', 'binaries'),  # Add this line
           # ... other data files
       ],
       # ... rest of spec
   )
   ```

4. **Build your .exe**:
   ```bash
   pyinstaller Supervertaler.spec
   ```

**How it works:**
- The code automatically detects bundled FFmpeg
- Adds it to PATH at runtime
- No user action required

---

### Option 2: Require User Installation

**Pros:**
- Smaller .exe size (~70 MB smaller)
- Smaller download

**Cons:**
- Users must install FFmpeg separately
- Extra setup step
- More support questions

**Implementation:**
- Already implemented! The error message guides users to install FFmpeg
- Shows: `winget install FFmpeg` or `choco install ffmpeg`

---

## For Standalone Voice Dictation App

If you want to distribute `run_voice_dictation.py` as a standalone tool:

### Option 1: With FFmpeg Bundled
```bash
pyinstaller --onefile --windowed \
  --add-data "binaries/ffmpeg.exe;binaries" \
  --name "VoiceDictation" \
  run_voice_dictation.py
```

### Option 2: Without FFmpeg
```bash
pyinstaller --onefile --windowed \
  --name "VoiceDictation" \
  run_voice_dictation.py
```
(User must have FFmpeg installed)

---

## Technical Details

### FFmpeg Detection Logic

The code checks for FFmpeg in this order:

1. **System PATH**: Checks if `ffmpeg` command is available
   - Windows: Checks `C:\Program Files\FFmpeg\bin\`, etc.
   - Respects user's PATH environment variable

2. **Bundled FFmpeg**: Checks `binaries/ffmpeg.exe`
   - For .exe: Checks in PyInstaller's `_MEIPASS` temp folder
   - For script: Checks relative to project root

3. **Error if not found**: Shows user-friendly installation instructions

### Code Location
- Detection logic: [modules/voice_dictation_lite.py](modules/voice_dictation_lite.py) - `ensure_ffmpeg_available()`
- Error handling: [Supervertaler.py](Supervertaler.py) - `on_dictation_error()`

---

## Recommended Approach

**For professional distribution**: **Bundle FFmpeg** (Option 1)

Reasons:
- Best user experience (zero setup)
- Fewer support requests
- Professional appearance
- 70 MB is negligible for modern systems
- Users can start translating immediately

**For development/testing**: Let users install FFmpeg (Option 2)
- Developers are comfortable with command line
- Keeps repo size small
- Easy to update FFmpeg independently

---

## Testing Your Distribution

### Test with FFmpeg bundled:
1. Build .exe with bundled FFmpeg
2. Copy to clean machine (without FFmpeg installed)
3. Run Supervertaler
4. Press F9 or click Dictate button
5. Should work immediately ✓

### Test without FFmpeg:
1. Build .exe without bundled FFmpeg
2. Ensure FFmpeg is NOT in system PATH
3. Run Supervertaler
4. Press F9 or click Dictate button
5. Should show error dialog with instructions ✓
6. Install FFmpeg (winget/choco)
7. Restart Supervertaler
8. Dictation should now work ✓

---

## FFmpeg Licensing

FFmpeg is **LGPL/GPL licensed**:
- ✓ You CAN distribute FFmpeg with your application
- ✓ You CAN use it commercially
- ✓ You DON'T need to open-source Supervertaler
- ✓ You SHOULD include FFmpeg's license file

**Include in your distribution:**
```
C:\Dev\Supervertaler\
├── binaries\
│   ├── ffmpeg.exe
│   └── FFMPEG_LICENSE.txt    (add this)
```

Download license from: https://github.com/FFmpeg/FFmpeg/blob/master/COPYING.LGPLv2.1

---

## Troubleshooting

### "FFmpeg not found" error on .exe
- FFmpeg.exe not bundled correctly
- Check PyInstaller spec includes `binaries/` folder
- Verify `ffmpeg.exe` is in build output

### "Access denied" error
- Antivirus blocking FFmpeg
- Windows SmartScreen blocking unsigned .exe
- Sign your .exe with code signing certificate

### Dictation works in dev but not .exe
- FFmpeg path not set correctly in frozen app
- Check `sys._MEIPASS` logic in `ensure_ffmpeg_available()`

---

## Summary

| Scenario | FFmpeg Requirement | User Action |
|----------|-------------------|-------------|
| **Dev (source)** | User installs separately | Run: `winget install FFmpeg` |
| **.exe (bundled)** | Included in .exe | None - works immediately |
| **.exe (not bundled)** | User installs separately | Run: `winget install FFmpeg` |

**Recommendation**: Bundle FFmpeg for professional releases, let developers install separately.
