# Voice Dictation Module - User Guide

## Overview

The Voice Dictation module provides **multilingual speech recognition** powered by OpenAI Whisper. Record your voice and get instant transcription in 100+ languages.

## Quick Start

### 1. Run the Standalone App

```bash
python run_voice_dictation.py
```

### 2. Use the Interface

1. **Select Model** (default: Base)
   - **Tiny**: Fastest, ~1GB RAM
   - **Base**: Good balance, ~1GB RAM (recommended)
   - **Small**: Better quality, ~2GB RAM
   - **Medium**: High quality, ~5GB RAM
   - **Large**: Best quality, ~10GB RAM

2. **Select Language**
   - Auto-detect (default)
   - English
   - Dutch
   - Or any of 100+ supported languages

3. **Click "Start Recording"**
   - Speak clearly into your microphone
   - Maximum 30 seconds per recording
   - Click "Stop Recording" when done

4. **Get Transcription**
   - Transcription appears automatically
   - Multiple recordings accumulate in the text area
   - Click "Copy to Clipboard" to use the text

## Features

- ✅ **Multilingual**: 100+ languages supported
- ✅ **High Accuracy**: Uses state-of-the-art Whisper model
- ✅ **Multiple Sizes**: Choose speed vs. quality
- ✅ **Easy to Use**: Simple push-to-record interface
- ✅ **Clipboard Ready**: One-click copy
- ✅ **Standalone or Integrated**: Works independently or as Supervertaler module

## Supported Languages

English, Dutch, German, French, Spanish, Italian, Portuguese, Polish, Russian, Chinese, Japanese, Korean, and 90+ more.

See: https://github.com/openai/whisper#available-models-and-languages

## First-Time Setup

**On first use**, Whisper will download the selected model:

| Model  | Size    | Download Time (approx) |
|--------|---------|------------------------|
| Tiny   | ~75 MB  | < 1 minute            |
| Base   | ~145 MB | ~1-2 minutes          |
| Small  | ~460 MB | ~3-5 minutes          |
| Medium | ~1.5 GB | ~10-15 minutes        |
| Large  | ~2.9 GB | ~20-30 minutes        |

Models are cached locally and only downloaded once.

## System Requirements

- **Microphone**: Any working microphone (USB, built-in, headset)
- **RAM**:
  - Tiny/Base: 1-2 GB free
  - Small: 2-3 GB free
  - Medium: 5-6 GB free
  - Large: 10+ GB free
- **Disk Space**: 75 MB to 3 GB (depending on model)
- **Internet**: Only for first-time model download

## Tips for Best Results

1. **Use a good microphone**: USB or headset mics work better than built-in laptop mics
2. **Speak clearly**: Avoid mumbling or very fast speech
3. **Quiet environment**: Background noise reduces accuracy
4. **Model selection**:
   - Quick notes → Use "Tiny" or "Base"
   - Important text → Use "Small" or "Medium"
   - Critical accuracy → Use "Large"
5. **Language selection**: Specify language if known (faster than auto-detect)

## Troubleshooting

### "No microphone detected"
- Check Windows sound settings
- Ensure microphone is plugged in and enabled
- Grant microphone permission if prompted

### "Recording failed"
- Try restarting the application
- Check if another app is using the microphone
- Update audio drivers

### "Model download slow"
- Download happens once per model
- Subsequent uses are instant
- Try a smaller model (Tiny or Base)

### "Poor transcription quality"
- Try a larger model (Medium or Large)
- Improve microphone quality
- Reduce background noise
- Speak more clearly and slower

## Integration with Supervertaler

The module can be integrated into Supervertaler's main interface:

```python
from modules.voice_dictation import VoiceDictationWidget

# Add to toolbar or new tab
dictation_widget = VoiceDictationWidget()
```

This allows voice dictation while translating!

## Technical Details

**Dependencies:**
- `openai` - OpenAI Whisper API (recommended)
- `openai-whisper` (optional) - Offline/local Whisper model (very large dependency; installs PyTorch)
- `pyaudio` - Audio recording
- `sounddevice` - Audio I/O
- `PyQt6` - GUI framework

**Model Location:**
Models are cached in: `~/.cache/whisper/`

**Audio Format:**
- Sample rate: 16 kHz (required by Whisper)
- Channels: Mono
- Format: 16-bit PCM WAV

## License

Uses OpenAI Whisper (MIT License)
Compatible with Supervertaler Apache-2.0 license

## Credits

- **OpenAI Whisper**: https://github.com/openai/whisper
- **Developed for**: Supervertaler CAT tool
- **Created**: November 2025

---

**Need help?** Report issues at: https://github.com/michaelbeijer/Supervertaler/issues
