"""
Lightweight Voice Dictation for Supervertaler
Minimal version for integration into target editors
"""

# Note: Heavy imports (whisper, sounddevice, numpy) are loaded lazily in run()
# to avoid slow startup. These libraries add 5+ seconds of import time.
import tempfile
import wave
import os
import sys
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal


def ensure_ffmpeg_available():
    """
    Ensure FFmpeg is available for Whisper
    Returns True if FFmpeg is found, False otherwise
    """
    import shutil

    # Check if ffmpeg is already in system PATH
    if shutil.which('ffmpeg'):
        return True

    # Check for bundled ffmpeg (for .exe distributions)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        bundle_dir = Path(sys._MEIPASS)
    else:
        # Running as script
        bundle_dir = Path(__file__).parent.parent

    bundled_ffmpeg = bundle_dir / 'binaries' / 'ffmpeg.exe'
    if bundled_ffmpeg.exists():
        # Add bundled ffmpeg directory to PATH
        os.environ['PATH'] = str(bundled_ffmpeg.parent) + os.pathsep + os.environ['PATH']
        return True

    return False


class QuickDictationThread(QThread):
    """
    Quick voice dictation thread - records and transcribes in one go
    Minimal UI, fast operation
    """
    transcription_ready = pyqtSignal(str)  # Emits transcribed text
    status_update = pyqtSignal(str)  # Status messages
    error_occurred = pyqtSignal(str)  # Errors
    model_loading_started = pyqtSignal(str)  # Model name being loaded/downloaded
    model_loading_finished = pyqtSignal()  # Model loaded successfully

    def __init__(self, model_name="base", language="auto", duration=10, use_api: bool = False, api_key: str | None = None):
        super().__init__()
        self.model_name = model_name
        self.language = None if language == "auto" else language
        self.duration = duration  # Max recording duration
        self.use_api = use_api
        self.api_key = api_key
        self.sample_rate = 16000
        self.is_recording = False
        self.stop_requested = False
        self.recording_stream = None

    def stop_recording(self):
        """Stop recording early (called from main thread)"""
        self.stop_requested = True

    def run(self):
        """Record and transcribe audio"""
        try:
            # Lazy import heavy libraries to avoid slow startup
            import sounddevice as sd
            import numpy as np

            # Local Whisper needs FFmpeg; API mode does not.
            if not self.use_api:
                if not ensure_ffmpeg_available():
                    self.error_occurred.emit(
                        "FFmpeg not found. Local Whisper requires FFmpeg.\n\n"
                        "Option A (recommended): Switch to 'OpenAI Whisper API' in Settings → Supervoice.\n\n"
                        "Option B: Install FFmpeg (PowerShell as Admin):\n"
                        "winget install FFmpeg  (or)  choco install ffmpeg"
                    )
                    return

            # Step 1: Record audio
            self.status_update.emit("🔴 Recording... (Press F9 or click Stop to finish)")
            self.is_recording = True
            self.stop_requested = False

            # Start recording
            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )

            # Wait for recording to complete OR manual stop
            import time
            elapsed = 0
            check_interval = 0.1  # Check every 100ms
            while elapsed < self.duration and not self.stop_requested:
                time.sleep(check_interval)
                elapsed += check_interval

            # Stop recording
            sd.stop()
            self.is_recording = False
            self.status_update.emit(f"🛑 Recording stopped ({elapsed:.1f}s recorded)")

            # Calculate actual recorded samples
            actual_samples = int(min(elapsed, self.duration) * self.sample_rate)
            recording = recording[:actual_samples]  # Trim to actual length
            self.status_update.emit(f"📊 Processing {actual_samples} audio samples...")

            # Convert to int16
            audio_data = np.int16(recording * 32767)

            # Save to temp WAV
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"sv_dictation_{os.getpid()}.wav")
            self.status_update.emit(f"💾 Saving audio to {temp_path}")

            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())

            self.status_update.emit(f"✓ Audio saved ({len(audio_data)} bytes)")

            # Step 2: Transcribe
            self.status_update.emit("⏳ Transcribing...")

            if self.use_api:
                if not self.api_key:
                    self.error_occurred.emit(
                        "OpenAI API key missing.\n\n"
                        "Set your OpenAI API key in Settings → AI Settings, or switch to Local Whisper (offline)."
                    )
                    try:
                        Path(temp_path).unlink()
                    except:
                        pass
                    return

                self.status_update.emit("🎤 Using OpenAI Whisper API (fast & accurate)")
                text = self._transcribe_with_api(temp_path)
            else:
                text = self._transcribe_with_local(temp_path)

            # Clean up temp file
            try:
                Path(temp_path).unlink()
            except:
                pass

            # Emit result
            if text:
                self.transcription_ready.emit(text)
                self.status_update.emit("✅ Done")
            else:
                self.error_occurred.emit("No speech detected")

        except Exception as e:
            self.is_recording = False
            import traceback
            error_details = traceback.format_exc()
            self.error_occurred.emit(f"Error: {str(e)}\n\nTraceback:\n{error_details}")

    def _transcribe_with_api(self, audio_path: str) -> str:
        """Transcribe using OpenAI Whisper API (no local Whisper required)."""
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            with open(audio_path, "rb") as audio_file:
                kwargs = {"model": "whisper-1", "file": audio_file}
                if self.language:
                    kwargs["language"] = self.language
                response = client.audio.transcriptions.create(**kwargs)

            return (response.text or "").strip()
        except Exception as e:
            self.error_occurred.emit(f"OpenAI API error: {e}")
            return ""

    def _transcribe_with_local(self, audio_path: str) -> str:
        """Transcribe using Local Whisper (requires optional dependency)."""
        try:
            # Lazy import whisper to avoid slow startup (PyTorch takes seconds to import)
            try:
                import whisper
            except ImportError:
                self.error_occurred.emit(
                    "Local Whisper is not installed.\n\n"
                    "Install it with:\n"
                    "  pip install supervertaler[local-whisper]\n\n"
                    "Or switch to 'OpenAI Whisper API' in Settings → Supervoice."
                )
                return ""

            # Check if model needs to be downloaded
            cache_dir = os.path.expanduser("~/.cache/whisper")
            if os.name == 'nt':  # Windows
                cache_dir = os.path.join(os.environ.get('USERPROFILE', ''), '.cache', 'whisper')

            model_files = [
                f"{self.model_name}.pt",
                f"{self.model_name}.en.pt",
                f"{self.model_name}-v3.pt"  # For large model
            ]
            model_exists = any(os.path.exists(os.path.join(cache_dir, f)) for f in model_files)

            # Load model (cached after first use, may download on first use)
            self.model_loading_started.emit(self.model_name)
            if not model_exists:
                self.status_update.emit(f"📥 Downloading {self.model_name} model... (this may take several minutes)")
            else:
                self.status_update.emit(f"⏳ Loading {self.model_name} model...")

            model = whisper.load_model(self.model_name)
            self.model_loading_finished.emit()

            # Transcribe
            self.status_update.emit("⏳ Transcribing audio...")
            if self.language:
                result = model.transcribe(audio_path, language=self.language)
            else:
                result = model.transcribe(audio_path)

            return (result.get("text") or "").strip()
        except Exception as e:
            self.error_occurred.emit(f"Local transcription error: {e}")
            return ""

    def stop(self):
        """Stop recording"""
        if self.is_recording:
            self.is_recording = False
            try:
                import sounddevice as sd
                sd.stop()
            except:
                pass
