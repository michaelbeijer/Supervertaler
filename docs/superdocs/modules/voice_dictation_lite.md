# voice_dictation_lite

**File:** `modules/voice_dictation_lite.py`
**Lines:** 194
**Classes:** 1
**Functions:** 1

---

## Module Description

Lightweight Voice Dictation for Supervertaler
Minimal version for integration into target editors

---

## Classes

### `QuickDictationThread`

**Line:** 44

Quick voice dictation thread - records and transcribes in one go
Minimal UI, fast operation

#### Methods

##### `stop_recording()`

Stop recording early (called from main thread)

##### `run()`

Record and transcribe audio

##### `stop()`

Stop recording


---

## Functions

### `ensure_ffmpeg_available()`

**Line:** 16

Ensure FFmpeg is available for Whisper
Returns True if FFmpeg is found, False otherwise

---

