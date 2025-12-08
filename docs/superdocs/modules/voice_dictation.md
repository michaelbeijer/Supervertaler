# voice_dictation

**File:** `modules/voice_dictation.py`
**Lines:** 467
**Classes:** 3
**Functions:** 0

---

## Module Description

Voice Dictation Module for Supervertaler
Uses OpenAI Whisper for multilingual speech recognition
Supports English, Dutch, and 90+ other languages

---

## Classes

### `RecordingThread`

**Line:** 21

Background thread for audio recording

#### Methods

##### `run()`

Record audio in background

##### `stop()`

Stop recording


---

### `TranscriptionThread`

**Line:** 78

Background thread for transcription

#### Methods

##### `run()`

Transcribe audio in background


---

### `VoiceDictationWidget`

**Line:** 126

Voice Dictation Widget using Whisper

Features:
- Push-to-record button
- Multilingual support (100+ languages)
- Multiple model sizes (tiny, base, small, medium, large)
- Copy to clipboard functionality

#### Methods

##### `init_ui()`

Initialize the user interface

##### `setup_shortcuts()`

Setup keyboard shortcuts

##### `cancel_recording()`

Cancel ongoing recording

##### `toggle_recording()`

Start or stop recording

##### `start_recording()`

Start recording audio

##### `stop_recording()`

Stop recording audio

##### `on_recording_finished()`

Handle recording completion

##### `on_recording_error()`

Handle recording error

##### `transcribe_audio()`

Transcribe recorded audio

##### `on_transcription_progress()`

Update progress message

##### `on_transcription_finished()`

Handle transcription completion

##### `on_transcription_error()`

Handle transcription error

##### `copy_to_clipboard()`

Copy transcription to clipboard

##### `clear_text()`

Clear transcription text


---

