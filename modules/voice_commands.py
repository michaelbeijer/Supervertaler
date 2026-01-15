"""
Voice Commands Module for Supervertaler
Talon-style voice command system with 3 tiers:
- Tier 1: In-app commands (Python/PyQt6)
- Tier 2: System commands (AutoHotkey scripts)
- Tier 3: Dictation fallback (insert as text)
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Callable, Tuple
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from PyQt6.QtCore import QObject, pyqtSignal


@dataclass
class VoiceCommand:
    """Represents a single voice command"""
    phrase: str  # The spoken phrase (e.g., "confirm segment")
    aliases: List[str] = field(default_factory=list)  # Alternative phrases
    action_type: str = "internal"  # "internal", "keystroke", "ahk_script", "ahk_inline"
    action: str = ""  # Action to execute
    description: str = ""  # Human-readable description
    category: str = "general"  # Category for organization
    enabled: bool = True
    
    def matches(self, spoken_text: str, threshold: float = 0.85) -> Tuple[bool, float]:
        """
        Check if spoken text matches this command.
        Returns (is_match, confidence_score)
        """
        spoken_lower = spoken_text.lower().strip()
        
        # Check exact matches first
        all_phrases = [self.phrase.lower()] + [a.lower() for a in self.aliases]
        for phrase in all_phrases:
            if spoken_lower == phrase:
                return (True, 1.0)
        
        # Check fuzzy matches
        best_score = 0.0
        for phrase in all_phrases:
            # Use SequenceMatcher for fuzzy matching
            score = SequenceMatcher(None, spoken_lower, phrase).ratio()
            best_score = max(best_score, score)
            
            # Also check if spoken text contains the phrase
            if phrase in spoken_lower or spoken_lower in phrase:
                # Boost score for partial matches
                length_ratio = min(len(phrase), len(spoken_lower)) / max(len(phrase), len(spoken_lower))
                best_score = max(best_score, 0.9 * length_ratio)
        
        return (best_score >= threshold, best_score)


class VoiceCommandManager(QObject):
    """
    Manages voice commands - matching spoken text to actions and executing them.
    """
    
    # Signals
    command_executed = pyqtSignal(str, str)  # (command_phrase, result_message)
    command_not_found = pyqtSignal(str)  # spoken_text that didn't match
    error_occurred = pyqtSignal(str)  # error message
    
    # Default commands
    DEFAULT_COMMANDS = [
        # Navigation
        VoiceCommand("next segment", ["next", "down"], "internal", "navigate_next", 
                    "Move to next segment", "navigation"),
        VoiceCommand("previous segment", ["previous", "back", "up"], "internal", "navigate_previous",
                    "Move to previous segment", "navigation"),
        VoiceCommand("first segment", ["go to start", "beginning"], "internal", "navigate_first",
                    "Jump to first segment", "navigation"),
        VoiceCommand("last segment", ["go to end", "end"], "internal", "navigate_last",
                    "Jump to last segment", "navigation"),
        
        # Segment actions
        VoiceCommand("confirm", ["confirm segment", "done", "okay"], "internal", "confirm_segment",
                    "Confirm current segment", "editing"),
        VoiceCommand("copy source", ["copy from source", "source to target"], "internal", "copy_source_to_target",
                    "Copy source text to target", "editing"),
        VoiceCommand("clear target", ["clear", "delete target"], "internal", "clear_target",
                    "Clear target text", "editing"),
        VoiceCommand("undo", [], "keystroke", "ctrl+z",
                    "Undo last action", "editing"),
        VoiceCommand("redo", [], "keystroke", "ctrl+y",
                    "Redo last action", "editing"),
        
        # Translation
        VoiceCommand("translate", ["translate segment", "translate this"], "internal", "translate_segment",
                    "AI translate current segment", "translation"),
        VoiceCommand("translate all", ["batch translate"], "internal", "batch_translate",
                    "Translate all segments", "translation"),
        
        # Lookup & Search
        VoiceCommand("lookup", ["super lookup", "search"], "internal", "open_superlookup",
                    "Open Superlookup (Ctrl+K)", "lookup"),
        VoiceCommand("concordance", ["search memory", "search TM"], "internal", "concordance_search",
                    "Open concordance search", "lookup"),
        
        # File operations
        VoiceCommand("save project", ["save"], "keystroke", "ctrl+s",
                    "Save current project", "file"),
        VoiceCommand("open project", ["open"], "keystroke", "ctrl+o",
                    "Open project", "file"),
        
        # View
        VoiceCommand("show log", ["open log", "log tab"], "internal", "show_log",
                    "Show log panel", "view"),
        VoiceCommand("show editor", ["editor tab", "go to editor"], "internal", "show_editor",
                    "Show editor panel", "view"),
        
        # Dictation control
        VoiceCommand("start dictation", ["dictate", "voice input"], "internal", "start_dictation",
                    "Start voice dictation mode", "dictation"),
        VoiceCommand("stop listening", ["stop", "pause"], "internal", "stop_listening",
                    "Stop voice recognition", "dictation"),
        
        # memoQ-specific (AHK)
        VoiceCommand("glossary", ["add term", "add to glossary"], "ahk_inline", 
                    "Send, !{Down}",  # Alt+Down
                    "Add term pair to memoQ termbase", "memoq"),
        VoiceCommand("tag next", ["next tag", "insert tag"], "ahk_inline",
                    "Send, ^{PgDn}\nSleep, 100\nSend, {F9}\nSleep, 100\nSend, ^{Enter}",
                    "Go to end, insert next tag, confirm", "memoq"),
        VoiceCommand("confirm memoQ", ["confirm memo"], "ahk_inline",
                    "Send, ^{Enter}",
                    "Confirm segment in memoQ", "memoq"),
        
        # Trados-specific (AHK)
        VoiceCommand("confirm trados", ["confirm studio"], "ahk_inline",
                    "Send, ^{Enter}",
                    "Confirm segment in Trados Studio", "trados"),
    ]
    
    def __init__(self, user_data_path: Path, main_window=None):
        super().__init__()
        self.user_data_path = user_data_path
        self.main_window = main_window
        self.commands: List[VoiceCommand] = []
        self.commands_file = user_data_path / "voice_commands.json"
        self.ahk_script_dir = user_data_path / "voice_scripts"
        self.match_threshold = 0.85  # Minimum similarity for fuzzy matching
        
        # Internal action handlers (mapped to main_window methods)
        self.internal_handlers: Dict[str, Callable] = {}
        
        # Ensure directories exist
        self.ahk_script_dir.mkdir(parents=True, exist_ok=True)
        
        # Load commands
        self.load_commands()
        
        # Register internal handlers if main_window provided
        if main_window:
            self.register_main_window_handlers(main_window)
    
    def register_main_window_handlers(self, main_window):
        """Register handlers that call main window methods"""
        self.main_window = main_window
        
        self.internal_handlers = {
            # Navigation - using correct method names from Supervertaler.py
            "navigate_next": lambda: main_window.go_to_next_segment() if hasattr(main_window, 'go_to_next_segment') else self._log_missing('go_to_next_segment'),
            "navigate_previous": lambda: main_window.go_to_previous_segment() if hasattr(main_window, 'go_to_previous_segment') else self._log_missing('go_to_previous_segment'),
            "navigate_first": lambda: main_window.go_to_first_segment() if hasattr(main_window, 'go_to_first_segment') else self._log_missing('go_to_first_segment'),
            "navigate_last": lambda: main_window.go_to_last_segment() if hasattr(main_window, 'go_to_last_segment') else self._log_missing('go_to_last_segment'),
            
            # Editing - confirm_and_next_unconfirmed is the Enter key behavior
            "confirm_segment": lambda: main_window.confirm_and_next_unconfirmed() if hasattr(main_window, 'confirm_and_next_unconfirmed') else self._log_missing('confirm_and_next_unconfirmed'),
            "copy_source_to_target": lambda: main_window.copy_source_to_grid_target() if hasattr(main_window, 'copy_source_to_grid_target') else self._log_missing('copy_source_to_grid_target'),
            "clear_target": lambda: main_window.clear_grid_target() if hasattr(main_window, 'clear_grid_target') else self._log_missing('clear_grid_target'),
            
            # Translation
            "translate_segment": lambda: main_window.translate_current_segment() if hasattr(main_window, 'translate_current_segment') else self._log_missing('translate_current_segment'),
            "batch_translate": lambda: main_window.translate_batch() if hasattr(main_window, 'translate_batch') else self._log_missing('translate_batch'),
            
            # Lookup
            "open_superlookup": lambda: main_window._go_to_superlookup() if hasattr(main_window, '_go_to_superlookup') else self._log_missing('_go_to_superlookup'),
            "concordance_search": lambda: main_window.show_concordance_search() if hasattr(main_window, 'show_concordance_search') else self._log_missing('show_concordance_search'),
            
            # View
            "show_log": lambda: self._show_tab(main_window, "Log"),
            "show_editor": lambda: self._show_tab(main_window, "Editor"),
            
            # Dictation
            "start_dictation": lambda: main_window.start_voice_dictation() if hasattr(main_window, 'start_voice_dictation') else self._log_missing('start_voice_dictation'),
            "stop_listening": lambda: self._stop_voice_recognition(),
        }
    
    def _log_missing(self, method_name: str):
        """Log when a method is missing from main_window"""
        print(f"⚠️ Voice command: Method '{method_name}' not found on main window")
        if self.main_window and hasattr(self.main_window, 'log'):
            self.main_window.log(f"⚠️ Voice command: Method '{method_name}' not found")
    
    def _show_tab(self, main_window, tab_name: str):
        """Helper to switch to a specific tab"""
        if hasattr(main_window, 'main_tabs'):
            for i in range(main_window.main_tabs.count()):
                if tab_name.lower() in main_window.main_tabs.tabText(i).lower():
                    main_window.main_tabs.setCurrentIndex(i)
                    return
    
    def _stop_voice_recognition(self):
        """Stop the voice recognition system"""
        if self.main_window and hasattr(self.main_window, 'voice_command_listener'):
            listener = self.main_window.voice_command_listener
            if listener and hasattr(listener, 'stop'):
                listener.stop()
    
    def load_commands(self):
        """Load commands from JSON file, or create defaults"""
        if self.commands_file.exists():
            try:
                with open(self.commands_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.commands = []
                self.match_threshold = data.get('match_threshold', 0.85)
                
                for cmd_data in data.get('commands', []):
                    self.commands.append(VoiceCommand(
                        phrase=cmd_data['phrase'],
                        aliases=cmd_data.get('aliases', []),
                        action_type=cmd_data.get('action_type', 'internal'),
                        action=cmd_data.get('action', ''),
                        description=cmd_data.get('description', ''),
                        category=cmd_data.get('category', 'general'),
                        enabled=cmd_data.get('enabled', True)
                    ))
                
                return
            except Exception as e:
                print(f"Error loading voice commands: {e}")
        
        # Use defaults
        self.commands = self.DEFAULT_COMMANDS.copy()
        self.save_commands()
    
    def save_commands(self):
        """Save commands to JSON file"""
        data = {
            'version': '1.0',
            'match_threshold': self.match_threshold,
            'commands': [
                {
                    'phrase': cmd.phrase,
                    'aliases': cmd.aliases,
                    'action_type': cmd.action_type,
                    'action': cmd.action,
                    'description': cmd.description,
                    'category': cmd.category,
                    'enabled': cmd.enabled
                }
                for cmd in self.commands
            ]
        }
        
        try:
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.error_occurred.emit(f"Failed to save voice commands: {e}")
    
    def find_matching_command(self, spoken_text: str) -> Optional[Tuple[VoiceCommand, float]]:
        """
        Find the best matching command for spoken text.
        Returns (command, confidence) or None if no match.
        """
        spoken_text = spoken_text.strip()
        if not spoken_text:
            return None
        
        best_match = None
        best_score = 0.0
        
        for cmd in self.commands:
            if not cmd.enabled:
                continue
            
            is_match, score = cmd.matches(spoken_text, self.match_threshold)
            if is_match and score > best_score:
                best_match = cmd
                best_score = score
        
        if best_match:
            return (best_match, best_score)
        return None
    
    def execute_command(self, command: VoiceCommand) -> bool:
        """Execute a voice command. Returns True on success."""
        try:
            if command.action_type == "internal":
                return self._execute_internal(command)
            elif command.action_type == "keystroke":
                return self._execute_keystroke(command)
            elif command.action_type == "ahk_script":
                return self._execute_ahk_script(command)
            elif command.action_type == "ahk_inline":
                return self._execute_ahk_inline(command)
            else:
                self.error_occurred.emit(f"Unknown action type: {command.action_type}")
                return False
        except Exception as e:
            import traceback
            self.error_occurred.emit(f"Error executing '{command.phrase}': {e}\n{traceback.format_exc()}")
            return False
    
    def _execute_internal(self, command: VoiceCommand) -> bool:
        """Execute an internal Python action"""
        handler = self.internal_handlers.get(command.action)
        if handler:
            try:
                result = handler()
                # Log success to main window if available
                if self.main_window and hasattr(self.main_window, 'log'):
                    self.main_window.log(f"✓ Voice command executed: {command.phrase} → {command.action}")
                self.command_executed.emit(command.phrase, f"✓ {command.description}")
                return True
            except Exception as e:
                import traceback
                error_msg = f"Error in handler for '{command.phrase}': {e}"
                if self.main_window and hasattr(self.main_window, 'log'):
                    self.main_window.log(f"❌ {error_msg}")
                    self.main_window.log(traceback.format_exc())
                self.error_occurred.emit(error_msg)
                return False
        else:
            error_msg = f"No handler for internal action: {command.action}"
            if self.main_window and hasattr(self.main_window, 'log'):
                self.main_window.log(f"❌ {error_msg}")
                self.main_window.log(f"   Available handlers: {list(self.internal_handlers.keys())}")
            self.error_occurred.emit(error_msg)
            return False
    
    def _execute_keystroke(self, command: VoiceCommand) -> bool:
        """Execute a keystroke via AutoHotkey"""
        # Convert keystroke format (e.g., "ctrl+s") to AHK format
        ahk_keys = self._convert_to_ahk_keys(command.action)
        ahk_code = f"Send, {ahk_keys}"
        return self._run_ahk_code(ahk_code, command)
    
    def _execute_ahk_script(self, command: VoiceCommand) -> bool:
        """Execute a saved AHK script file"""
        script_path = self.ahk_script_dir / f"{command.action}.ahk"
        if not script_path.exists():
            self.error_occurred.emit(f"AHK script not found: {script_path}")
            return False
        
        try:
            # Find AutoHotkey executable
            ahk_exe = self._find_ahk_executable()
            if not ahk_exe:
                self.error_occurred.emit("AutoHotkey not found. Please install AutoHotkey v2.")
                return False
            
            subprocess.Popen([ahk_exe, str(script_path)], 
                           creationflags=subprocess.CREATE_NO_WINDOW)
            self.command_executed.emit(command.phrase, f"✓ {command.description}")
            return True
        except Exception as e:
            self.error_occurred.emit(f"Failed to run AHK script: {e}")
            return False
    
    def _execute_ahk_inline(self, command: VoiceCommand) -> bool:
        """Execute inline AHK code"""
        return self._run_ahk_code(command.action, command)
    
    def _run_ahk_code(self, ahk_code: str, command: VoiceCommand) -> bool:
        """Run arbitrary AHK code"""
        try:
            ahk_exe = self._find_ahk_executable()
            if not ahk_exe:
                self.error_occurred.emit("AutoHotkey not found. Please install AutoHotkey v2.")
                return False
            
            # Create temporary script
            temp_script = self.ahk_script_dir / "_temp_voice_cmd.ahk"
            
            # Wrap code in AHK v2 format
            full_script = f"""#Requires AutoHotkey v2.0
#SingleInstance Force
{ahk_code}
ExitApp
"""
            
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(full_script)
            
            # Run script
            subprocess.Popen([ahk_exe, str(temp_script)],
                           creationflags=subprocess.CREATE_NO_WINDOW)
            
            self.command_executed.emit(command.phrase, f"✓ {command.description}")
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to run AHK code: {e}")
            return False
    
    def _convert_to_ahk_keys(self, keystroke: str) -> str:
        """Convert keystroke string to AHK Send format"""
        # Map modifier names to AHK symbols
        modifiers = {
            'ctrl': '^',
            'control': '^',
            'alt': '!',
            'shift': '+',
            'win': '#',
            'windows': '#'
        }
        
        # Special key names
        special_keys = {
            'enter': '{Enter}',
            'return': '{Enter}',
            'tab': '{Tab}',
            'escape': '{Esc}',
            'esc': '{Esc}',
            'space': '{Space}',
            'backspace': '{Backspace}',
            'delete': '{Delete}',
            'del': '{Delete}',
            'insert': '{Insert}',
            'ins': '{Insert}',
            'home': '{Home}',
            'end': '{End}',
            'pageup': '{PgUp}',
            'pgup': '{PgUp}',
            'pagedown': '{PgDn}',
            'pgdn': '{PgDn}',
            'up': '{Up}',
            'down': '{Down}',
            'left': '{Left}',
            'right': '{Right}',
            'f1': '{F1}', 'f2': '{F2}', 'f3': '{F3}', 'f4': '{F4}',
            'f5': '{F5}', 'f6': '{F6}', 'f7': '{F7}', 'f8': '{F8}',
            'f9': '{F9}', 'f10': '{F10}', 'f11': '{F11}', 'f12': '{F12}',
        }
        
        parts = keystroke.lower().replace(' ', '').split('+')
        result = ''
        
        for part in parts:
            if part in modifiers:
                result += modifiers[part]
            elif part in special_keys:
                result += special_keys[part]
            else:
                # Regular key
                result += part
        
        return result
    
    def _find_ahk_executable(self) -> Optional[str]:
        """Find AutoHotkey v2 executable"""
        # Common installation paths
        possible_paths = [
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe",
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey32.exe",
            r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
            r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
        ]
        
        # Check PATH first
        import shutil
        ahk_in_path = shutil.which("AutoHotkey64") or shutil.which("AutoHotkey")
        if ahk_in_path:
            return ahk_in_path
        
        # Check common locations
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def process_spoken_text(self, spoken_text: str) -> Tuple[bool, str]:
        """
        Process spoken text - try to match command, return success status and message.
        Returns (was_command, message_or_text)
        - If command matched: (True, "Command executed: ...")
        - If no match: (False, original_spoken_text) for dictation fallback
        """
        match_result = self.find_matching_command(spoken_text)
        
        if match_result:
            command, confidence = match_result
            success = self.execute_command(command)
            if success:
                return (True, f"✓ {command.phrase} ({confidence:.0%})")
            else:
                return (True, f"✗ Failed: {command.phrase}")
        
        # No command matched - return text for dictation
        self.command_not_found.emit(spoken_text)
        return (False, spoken_text)
    
    def add_command(self, command: VoiceCommand):
        """Add a new command"""
        self.commands.append(command)
        self.save_commands()
    
    def remove_command(self, phrase: str):
        """Remove a command by phrase"""
        self.commands = [c for c in self.commands if c.phrase != phrase]
        self.save_commands()
    
    def get_commands_by_category(self) -> Dict[str, List[VoiceCommand]]:
        """Get commands organized by category"""
        categories: Dict[str, List[VoiceCommand]] = {}
        for cmd in self.commands:
            if cmd.category not in categories:
                categories[cmd.category] = []
            categories[cmd.category].append(cmd)
        return categories
    
    def export_commands(self, filepath: Path):
        """Export commands to a file"""
        data = {
            'version': '1.0',
            'match_threshold': self.match_threshold,
            'commands': [
                {
                    'phrase': cmd.phrase,
                    'aliases': cmd.aliases,
                    'action_type': cmd.action_type,
                    'action': cmd.action,
                    'description': cmd.description,
                    'category': cmd.category,
                    'enabled': cmd.enabled
                }
                for cmd in self.commands
            ]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def import_commands(self, filepath: Path, merge: bool = True):
        """Import commands from a file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        imported_commands = []
        for cmd_data in data.get('commands', []):
            imported_commands.append(VoiceCommand(
                phrase=cmd_data['phrase'],
                aliases=cmd_data.get('aliases', []),
                action_type=cmd_data.get('action_type', 'internal'),
                action=cmd_data.get('action', ''),
                description=cmd_data.get('description', ''),
                category=cmd_data.get('category', 'general'),
                enabled=cmd_data.get('enabled', True)
            ))
        
        if merge:
            # Add imported commands, skip duplicates
            existing_phrases = {c.phrase for c in self.commands}
            for cmd in imported_commands:
                if cmd.phrase not in existing_phrases:
                    self.commands.append(cmd)
        else:
            # Replace all commands
            self.commands = imported_commands
        
        self.save_commands()


class ContinuousVoiceListener(QObject):
    """
    Continuous voice listening with Voice Activity Detection (VAD).
    
    How it works:
    1. Continuously monitors microphone audio levels
    2. When speech is detected (audio above threshold), starts recording
    3. When silence is detected (audio below threshold for X ms), stops recording
    4. Sends recording to Whisper for transcription
    5. Processes result (command or dictation)
    6. Repeats
    
    This eliminates the need to press F9 twice - just speak and it listens.
    """
    
    # Signals
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    speech_detected = pyqtSignal(str)  # Raw transcribed text
    command_detected = pyqtSignal(str, str)  # (phrase, result)
    text_for_dictation = pyqtSignal(str)  # Text that didn't match any command
    status_update = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    vad_status_changed = pyqtSignal(str)  # "listening", "recording", "processing"
    
    def __init__(self, command_manager: VoiceCommandManager, 
                 model_name: str = "base",
                 language: str = "auto",
                 use_api: bool = False,
                 api_key: str = None):
        super().__init__()
        self.command_manager = command_manager
        self.model_name = model_name
        self.language = None if language == "auto" else language
        self.use_api = use_api
        self.api_key = api_key
        
        # VAD settings
        self.speech_threshold = 0.02  # RMS threshold to detect speech (adjustable)
        self.silence_duration = 0.8  # Seconds of silence before stopping recording
        self.min_speech_duration = 0.3  # Minimum speech duration to process
        self.max_speech_duration = 15.0  # Maximum recording duration
        self.is_listening = False
        self._thread = None
        self._whisper_model = None  # Cached Whisper model
        
    def start(self):
        """Start continuous listening"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self._thread = _VADListenerThread(self)
        self._thread.transcription_ready.connect(self._on_transcription)
        self._thread.status_update.connect(self.status_update.emit)
        self._thread.error_occurred.connect(self.error_occurred.emit)
        self._thread.vad_status.connect(self.vad_status_changed.emit)
        self._thread.start()
        self.listening_started.emit()
    
    def stop(self):
        """Stop continuous listening"""
        self.is_listening = False
        if self._thread:
            self._thread.stop()
            self._thread = None
        self.listening_stopped.emit()
    
    def set_sensitivity(self, level: str):
        """
        Set microphone sensitivity level.
        - "low": Requires loud speech (noisy environment)
        - "medium": Normal sensitivity
        - "high": Picks up quiet speech (quiet environment)
        """
        thresholds = {
            "low": 0.04,
            "medium": 0.02,
            "high": 0.01
        }
        self.speech_threshold = thresholds.get(level, 0.02)
    
    def _on_transcription(self, text: str):
        """Handle transcribed speech"""
        self.speech_detected.emit(text)
        
        # Try to match as command
        was_command, result = self.command_manager.process_spoken_text(text)
        
        if was_command:
            self.command_detected.emit(text, result)
        else:
            # Pass to dictation
            self.text_for_dictation.emit(text)


class _VADListenerThread(QObject):
    """
    Voice Activity Detection listener thread.
    Uses amplitude-based VAD to detect speech start/end.
    """
    
    transcription_ready = pyqtSignal(str)
    status_update = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    vad_status = pyqtSignal(str)  # "waiting", "recording", "processing"
    
    def __init__(self, listener: ContinuousVoiceListener):
        super().__init__()
        self.listener = listener
        self._running = False
        self._thread = None
        self._model = None  # Cached whisper model
    
    def start(self):
        """Start the listener thread"""
        import threading
        
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Stop the listener thread"""
        self._running = False
    
    def _run(self):
        """Main VAD listening loop"""
        try:
            import sounddevice as sd
            import numpy as np
            import tempfile
            import wave
            import os
            import time
            
            # Sample rate and chunk settings
            sample_rate = 16000
            chunk_samples = int(0.1 * sample_rate)  # 100ms chunks for VAD
            
            # Get settings from listener
            speech_threshold = self.listener.speech_threshold
            silence_duration = self.listener.silence_duration
            min_speech_duration = self.listener.min_speech_duration
            max_speech_duration = self.listener.max_speech_duration
            
            # Check if using API or local model
            if self.listener.use_api and self.listener.api_key:
                self.status_update.emit("🎤 Using OpenAI Whisper API (fast & accurate)")
                self._model = None  # No local model needed
            else:
                # Load local Whisper model once
                self.status_update.emit("🎤 Loading local speech model...")
                self.vad_status.emit("loading")
                try:
                    import whisper
                except ImportError:
                    self.error_occurred.emit(
                        "Local Whisper is not installed.\n\n"
                        "Option A (recommended): Choose 'OpenAI Whisper API' in Settings → Supervoice (requires OpenAI API key).\n"
                        "Option B: Install Local Whisper:\n"
                        "  pip install supervertaler[local-whisper]"
                    )
                    self._running = False
                    return
                self._model = whisper.load_model(self.listener.model_name)
            
            self.status_update.emit("🎤 Always-on listening active (waiting for speech...)")
            self.vad_status.emit("waiting")
            
            # Audio buffer for recording
            audio_buffer = []
            is_recording = False
            silence_start = None
            speech_start = None
            
            def audio_callback(indata, frames, time_info, status):
                """Callback for audio stream - processes each chunk"""
                nonlocal audio_buffer, is_recording, silence_start, speech_start
                
                if not self._running:
                    return
                
                # Calculate RMS amplitude
                rms = np.sqrt(np.mean(indata**2))
                is_speech = rms > speech_threshold
                
                if is_speech:
                    if not is_recording:
                        # Speech started
                        is_recording = True
                        speech_start = time.time()
                        audio_buffer = []
                        self.vad_status.emit("recording")
                        self.status_update.emit("🔴 Recording...")
                    
                    # Reset silence counter
                    silence_start = None
                    
                    # Add to buffer
                    audio_buffer.append(indata.copy())
                    
                    # Check max duration
                    if time.time() - speech_start > max_speech_duration:
                        # Force stop recording
                        is_recording = False
                        self._process_audio(audio_buffer, sample_rate)
                        audio_buffer = []
                        self.vad_status.emit("waiting")
                        
                else:  # Silence
                    if is_recording:
                        # Still recording, add silence chunk
                        audio_buffer.append(indata.copy())
                        
                        # Start or continue silence timer
                        if silence_start is None:
                            silence_start = time.time()
                        
                        # Check if silence duration exceeded
                        if time.time() - silence_start > silence_duration:
                            # Speech ended - process if long enough
                            speech_duration = time.time() - speech_start
                            is_recording = False
                            
                            if speech_duration >= min_speech_duration:
                                self._process_audio(audio_buffer, sample_rate)
                            else:
                                self.status_update.emit("🎤 (too short, ignored)")
                            
                            audio_buffer = []
                            silence_start = None
                            self.vad_status.emit("waiting")
                            self.status_update.emit("🎤 Listening...")
            
            # Start audio stream
            with sd.InputStream(
                samplerate=sample_rate,
                channels=1,
                dtype='float32',
                blocksize=chunk_samples,
                callback=audio_callback
            ):
                while self._running:
                    time.sleep(0.1)
                    
        except Exception as e:
            import traceback
            self.error_occurred.emit(f"Listener error: {e}\n{traceback.format_exc()}")
        finally:
            self.vad_status.emit("stopped")
            self.status_update.emit("🔇 Stopped listening")
    
    def _process_audio(self, audio_buffer: list, sample_rate: int):
        """Process recorded audio - save to file and transcribe"""
        try:
            import numpy as np
            import tempfile
            import wave
            import os
            
            self.vad_status.emit("processing")
            self.status_update.emit("⏳ Transcribing...")
            
            # Concatenate audio chunks
            if not audio_buffer:
                return
            
            audio_data = np.concatenate(audio_buffer, axis=0)
            
            # Convert to int16
            audio_int16 = np.int16(audio_data * 32767)
            
            # Save to temp file
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"sv_vad_{os.getpid()}.wav")
            
            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_int16.tobytes())
            
            # Transcribe using API or local model
            if self.listener.use_api and self.listener.api_key:
                text = self._transcribe_with_api(temp_path)
            else:
                text = self._transcribe_with_local(temp_path)
            
            # Clean up
            try:
                os.unlink(temp_path)
            except:
                pass
            
            # Emit result
            if text:
                self.transcription_ready.emit(text)
                
        except Exception as e:
            import traceback
            self.error_occurred.emit(f"Processing error: {e}\n{traceback.format_exc()}")

    def _transcribe_with_api(self, audio_path: str) -> str:
        """Transcribe using OpenAI Whisper API - much more accurate"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.listener.api_key)
            
            with open(audio_path, "rb") as audio_file:
                # Use whisper-1 model (OpenAI's hosted Whisper)
                kwargs = {"model": "whisper-1", "file": audio_file}
                
                # Add language hint if specified
                if self.listener.language:
                    kwargs["language"] = self.listener.language
                
                response = client.audio.transcriptions.create(**kwargs)
            
            return response.text.strip()
            
        except Exception as e:
            self.error_occurred.emit(f"OpenAI API error: {e}")
            return ""

    def _transcribe_with_local(self, audio_path: str) -> str:
        """Transcribe using local Whisper model"""
        try:
            if self.listener.language:
                result = self._model.transcribe(audio_path, language=self.listener.language)
            else:
                result = self._model.transcribe(audio_path)
            
            return result["text"].strip()
            
        except Exception as e:
            self.error_occurred.emit(f"Local transcription error: {e}")
            return ""


# Legacy class for backwards compatibility
class _ListenerThread(_VADListenerThread):
    """Legacy alias for _VADListenerThread"""
    pass

