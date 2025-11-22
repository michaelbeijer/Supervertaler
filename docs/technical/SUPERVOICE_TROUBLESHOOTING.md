# Supervoice Troubleshooting Guide

## Corrupt Model Files

### Problem: Interrupted Download

If you closed Supervertaler while a Whisper model was downloading, the model file may be corrupt.

**Symptoms:**
- Model file exists but is much smaller than expected
- Dictation fails or hangs when using that model
- Error messages about model loading

**Example:**
```
File: C:\Users\username\.cache\whisper\large-v3.pt
Size: 95 MB (should be ~2.9 GB)
Status: CORRUPT - download was interrupted
```

### Solution: Delete and Re-download

**Step 1: Locate the corrupt file**

Model files are stored at:
- **Windows**: `C:\Users\<username>\.cache\whisper\`
- **Linux/Mac**: `~/.cache/whisper/`

**Step 2: Check file sizes**

| Model | Expected Size | File Name |
|-------|--------------|-----------|
| tiny | ~75 MB | tiny.pt or tiny.en.pt |
| base | ~142 MB | base.pt or base.en.pt |
| small | ~466 MB | small.pt or small.en.pt |
| medium | ~1.5 GB | medium.pt or medium.en.pt |
| large | ~2.9 GB | large-v3.pt |

If a file is much smaller than expected, it's corrupt.

**Step 3: Delete the corrupt file**

1. Close Supervertaler
2. Navigate to `C:\Users\<username>\.cache\whisper\`
3. Delete the corrupt .pt file (e.g., `large-v3.pt`)
4. Empty Recycle Bin (frees disk space immediately)

**Step 4: Re-download**

1. Open Supervertaler
2. Go to **Settings → 🎤 Supervoice**
3. Select the model you want (e.g., "large")
4. Click "💾 Save Supervoice Settings"
5. Press F9 or click "Dictate" to start a dictation
6. Model will download automatically (progress shown in Log)
7. **⚠️ Don't close Supervertaler until download completes!**

### Prevention

**New in this version:** Supervertaler now prevents accidental download interruption!

If you try to close while a model is downloading:
- ⚠️ Warning dialog appears
- Shows model name, size, and download location
- Offers "Force Quit" option if you need to close
- Default: Stay open and finish download

## Model Selection Guide

Choose the right model for your needs:

| Model | Speed | Accuracy | RAM | Download | Best For |
|-------|-------|----------|-----|----------|----------|
| **tiny** | ⚡⚡⚡ | ⭐ | ~1 GB | 75 MB | Quick notes, low-end PCs |
| **base** | ⚡⚡ | ⭐⭐ | ~1 GB | 142 MB | **Recommended** - Good balance |
| **small** | ⚡ | ⭐⭐⭐ | ~2 GB | 466 MB | Better accuracy needed |
| **medium** | 🐢 | ⭐⭐⭐⭐ | ~5 GB | 1.5 GB | High accuracy, powerful PC |
| **large** | 🐢🐢 | ⭐⭐⭐⭐⭐ | ~10 GB | 2.9 GB | Best quality, very powerful PC |

**Recommendation:** Start with **base** - it's fast and accurate enough for most translation work.

Only upgrade to larger models if:
- You frequently dictate technical/medical terms
- You work with accents or noisy environments
- You have a powerful computer (16+ GB RAM)

## Common Issues

### Issue: "FFmpeg not found"

**Solution:**
1. Open PowerShell as Administrator
2. Run: `winget install FFmpeg` or `choco install ffmpeg`
3. Restart Supervertaler

### Issue: Dictation is very slow

**Cause:** Model too large for your computer

**Solution:**
1. Go to Settings → 🎤 Supervoice
2. Select a smaller model (try "tiny" or "base")
3. Save and test

### Issue: Can't find .cache folder on Windows

**Solution:**
1. Open File Explorer
2. Type in address bar: `%USERPROFILE%\.cache\whisper`
3. Press Enter
4. Or manually navigate to: `C:\Users\<YourUsername>\.cache\whisper\`

### Issue: Model keeps re-downloading every time

**Cause:** Windows treating .cache as temporary folder

**Solution:**
1. Check folder properties
2. Ensure it's not marked as "Temporary"
3. Check disk space (downloads may fail silently if disk full)

## Getting Help

If you encounter other issues:

1. Check the **Log** tab in Settings
2. Look for error messages
3. Note which model you're using
4. Check available disk space
5. Report issue with details from log

## Technical Details

**Whisper Model Storage:**
- Models cached permanently after first download
- Shared between all apps using Whisper
- Can be deleted to free space (will re-download on next use)
- Download handled by OpenAI Whisper library automatically

**Download Process:**
1. User presses F9 or clicks Dictate
2. Supervoice checks if model exists in cache
3. If not found, downloads from OpenAI servers
4. Progress shown in log window
5. Download interruption protection active
6. Model saved to cache for future use

**Cache Management:**
- No automatic cleanup
- Models persist forever (until manually deleted)
- Multiple model versions can coexist
- Safe to delete unused models to free space
