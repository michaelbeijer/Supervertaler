"""
Lightweight Voice Dictation for Supervertaler
Minimal version for integration into target editors
"""

import whisper
import sounddevice as sd
import numpy as np
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

    def __init__(self, model_name="base", language="auto", duration=10):
        super().__init__()
        self.model_name = model_name
        self.language = None if language == "auto" else language
        self.duration = duration  # Max recording duration
        self.sample_rate = 16000
        self.is_recording = False

    def run(self):
        """Record and transcribe audio"""
        try:
            # Check FFmpeg availability first
            if not ensure_ffmpeg_available():
                self.error_occurred.emit(
                    "FFmpeg not found. Please install FFmpeg or contact support.\n\n"
                    "Quick install: Open PowerShell as Admin and run:\n"
                    "winget install FFmpeg  (or)  choco install ffmpeg"
                )
                return

            # Step 1: Record audio
            self.status_update.emit("🔴 Recording...")
            self.is_recording = True

            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )

            sd.wait()  # Wait for recording to complete
            self.is_recording = False

            # Convert to int16
            audio_data = np.int16(recording * 32767)

            # Save to temp WAV
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"sv_dictation_{os.getpid()}.wav")

            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())

            # Step 2: Transcribe
            self.status_update.emit("⏳ Transcribing...")

            # Load model (cached after first use)
            model = whisper.load_model(self.model_name)

            # Transcribe
            if self.language:
                result = model.transcribe(temp_path, language=self.language)
            else:
                result = model.transcribe(temp_path)

            # Clean up temp file
            try:
                Path(temp_path).unlink()
            except:
                pass

            # Emit result
            text = result["text"].strip()
            if text:
                self.transcription_ready.emit(text)
                self.status_update.emit("✅ Done")
            else:
                self.error_occurred.emit("No speech detected")

        except Exception as e:
            self.is_recording = False
            self.error_occurred.emit(f"Error: {str(e)}")

    def stop(self):
        """Stop recording"""
        if self.is_recording:
            self.is_recording = False
            sd.stop()
