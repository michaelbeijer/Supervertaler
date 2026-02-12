"""
Platform Helpers for Supervertaler
===================================
Cross-platform utilities for file operations, window management,
subprocess flags, global hotkeys, and keystroke automation.

Replaces scattered platform-specific code with a single, consistent API.
"""

import sys
import os
import subprocess
import shutil
import contextlib
import time
from pathlib import Path
from typing import Optional, Callable, Dict, List


# ---------------------------------------------------------------------------
# Platform detection constants
# ---------------------------------------------------------------------------
IS_WINDOWS = sys.platform == 'win32'
IS_MACOS = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')


# ---------------------------------------------------------------------------
# Cross-platform file/folder opening
# ---------------------------------------------------------------------------
def open_file(path: str) -> bool:
    """Open a file with the system's default application.

    Cross-platform replacement for os.startfile().
    Returns True on success, False on failure.
    """
    try:
        path_str = str(path)
        if IS_WINDOWS:
            os.startfile(path_str)
        elif IS_MACOS:
            subprocess.run(['open', path_str], check=True)
        else:
            subprocess.run(['xdg-open', path_str], check=True)
        return True
    except Exception as e:
        print(f"[platform_helpers] Failed to open file {path}: {e}")
        return False


def open_folder(path: str) -> bool:
    """Open a folder in the system file manager.

    If *path* is a file, opens its containing folder.
    """
    path_obj = Path(path)
    folder = path_obj.parent if path_obj.is_file() else path_obj
    return open_file(str(folder))


def open_folder_and_select(path: str) -> bool:
    """Open a folder in the file manager and highlight/select the given file.

    Falls back to open_folder() on unsupported platforms.
    """
    try:
        path_str = str(path)
        if IS_WINDOWS:
            subprocess.run(['explorer', '/select,', path_str])
            return True
        elif IS_MACOS:
            subprocess.run(['open', '-R', path_str])
            return True
        else:
            # xdg-open on the parent folder (no select support)
            return open_folder(path_str)
    except Exception as e:
        print(f"[platform_helpers] Failed to open folder for {path}: {e}")
        return False


# ---------------------------------------------------------------------------
# Cross-platform subprocess creation flags
# ---------------------------------------------------------------------------
def get_hidden_subprocess_flags() -> dict:
    """Return subprocess kwargs to hide the console window on Windows.

    Usage::

        subprocess.Popen([...], **get_hidden_subprocess_flags())
    """
    if IS_WINDOWS and hasattr(subprocess, 'CREATE_NO_WINDOW'):
        return {'creationflags': subprocess.CREATE_NO_WINDOW}
    return {}


# ---------------------------------------------------------------------------
# Cross-platform window activation
# ---------------------------------------------------------------------------
def activate_window_by_title(title: str) -> bool:
    """Best-effort attempt to bring a window with *title* to the foreground.

    Returns True if the operation was attempted (not guaranteed to succeed).
    On Windows we fall back to Qt's own raise/activate methods via the caller.
    """
    try:
        if IS_WINDOWS:
            # Use ctypes to find and activate the window.
            # Plain SetForegroundWindow fails when our app is in the background
            # (Windows prevents background apps from stealing focus).  The
            # workaround is AttachThreadInput: temporarily attach our thread to
            # the foreground window's thread so the OS treats our call as coming
            # from the foreground process.
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            EnumWindows = user32.EnumWindows
            GetWindowTextW = user32.GetWindowTextW
            GetWindowTextLengthW = user32.GetWindowTextLengthW
            IsWindowVisible = user32.IsWindowVisible
            SetForegroundWindow = user32.SetForegroundWindow
            ShowWindow = user32.ShowWindow
            GetForegroundWindow = user32.GetForegroundWindow
            GetWindowThreadProcessId = user32.GetWindowThreadProcessId
            GetCurrentThreadId = kernel32.GetCurrentThreadId
            AttachThreadInput = user32.AttachThreadInput
            BringWindowToTop = user32.BringWindowToTop
            SW_RESTORE = 9
            SW_SHOW = 5

            WNDENUMPROC = ctypes.WINFUNCTYPE(
                ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
            )
            target_hwnd = None

            def _enum_cb(hwnd, _lparam):
                nonlocal target_hwnd
                if IsWindowVisible(hwnd):
                    length = GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buf = ctypes.create_unicode_buffer(length + 1)
                        GetWindowTextW(hwnd, buf, length + 1)
                        if title.lower() in buf.value.lower():
                            target_hwnd = hwnd
                            return False  # stop enumeration
                return True

            EnumWindows(WNDENUMPROC(_enum_cb), 0)
            if target_hwnd:
                # Attach to the foreground thread so SetForegroundWindow succeeds
                fg_hwnd = GetForegroundWindow()
                fg_thread = GetWindowThreadProcessId(fg_hwnd, None)
                our_thread = GetCurrentThreadId()
                attached = False
                if fg_thread != our_thread:
                    attached = AttachThreadInput(fg_thread, our_thread, True)

                ShowWindow(target_hwnd, SW_RESTORE)
                BringWindowToTop(target_hwnd)
                SetForegroundWindow(target_hwnd)

                if attached:
                    AttachThreadInput(fg_thread, our_thread, False)
                return True
            return False

        elif IS_MACOS:
            subprocess.run(
                ['osascript', '-e',
                 f'tell application "System Events" to set frontmost of '
                 f'(first process whose name contains "{title}") to true'],
                capture_output=True
            )
            return True

        else:
            # Linux — try wmctrl, then xdotool
            wmctrl = shutil.which('wmctrl')
            if wmctrl:
                subprocess.run([wmctrl, '-a', title], capture_output=True)
                return True
            xdotool = shutil.which('xdotool')
            if xdotool:
                subprocess.run(
                    [xdotool, 'search', '--name', title, 'windowactivate'],
                    capture_output=True
                )
                return True
            return False

    except Exception as e:
        print(f"[platform_helpers] Window activation failed: {e}")
        return False


def get_foreground_window():
    """Return an opaque handle for the current foreground window.

    On Windows returns HWND (int), on macOS/Linux returns the window title
    (str) or None if detection fails.  Pass the result to
    ``activate_foreground_window()`` to restore focus later.
    """
    try:
        if IS_WINDOWS:
            import ctypes
            return ctypes.windll.user32.GetForegroundWindow()
        elif IS_MACOS:
            result = subprocess.run(
                ['osascript', '-e',
                 'tell application "System Events" to get name of '
                 'first process whose frontmost is true'],
                capture_output=True, text=True
            )
            name = result.stdout.strip()
            return name if name else None
        else:
            xdotool = shutil.which('xdotool')
            if xdotool:
                result = subprocess.run(
                    [xdotool, 'getactivewindow'], capture_output=True, text=True
                )
                wid = result.stdout.strip()
                return wid if wid else None
            return None
    except Exception:
        return None


def activate_foreground_window(handle):
    """Re-activate a window previously captured by ``get_foreground_window()``.

    Uses the same AttachThreadInput trick on Windows for reliable activation.
    Does NOT call ShowWindow(SW_RESTORE) — that would un-maximize a maximized
    window.  The target window is already visible; we just need to give it focus.
    """
    if handle is None:
        return False
    try:
        if IS_WINDOWS:
            import ctypes
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            # Attach to current foreground thread so SetForegroundWindow succeeds
            fg_hwnd = user32.GetForegroundWindow()
            fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
            our_thread = kernel32.GetCurrentThreadId()
            attached = False
            if fg_thread != our_thread:
                attached = user32.AttachThreadInput(fg_thread, our_thread, True)

            # Only SetForegroundWindow — don't call ShowWindow(SW_RESTORE)
            # as that would un-maximize a maximized browser/editor window
            user32.SetForegroundWindow(handle)

            if attached:
                user32.AttachThreadInput(fg_thread, our_thread, False)
            return True

        elif IS_MACOS:
            # handle is the process name
            subprocess.run(
                ['osascript', '-e',
                 f'tell application "System Events" to set frontmost of '
                 f'(first process whose name is "{handle}") to true'],
                capture_output=True
            )
            return True

        else:
            # handle is xdotool window ID
            xdotool = shutil.which('xdotool')
            if xdotool:
                subprocess.run(
                    [xdotool, 'windowactivate', str(handle)],
                    capture_output=True
                )
                return True
            return False

    except Exception as e:
        print(f"[platform_helpers] activate_foreground_window failed: {e}")
        return False


# ---------------------------------------------------------------------------
# Cross-platform Global Hotkey Manager
# ---------------------------------------------------------------------------
#
# On Windows: uses the native RegisterHotKey API (runs its own message pump
#   in a background thread — works perfectly alongside PyQt6).
# On macOS/Linux: uses pynput GlobalHotKeys.
# ---------------------------------------------------------------------------

# Windows virtual-key codes for RegisterHotKey
_VK_MAP = {
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46,
    'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A, 'k': 0x4B, 'l': 0x4C,
    'm': 0x4D, 'n': 0x4E, 'o': 0x4F, 'p': 0x50, 'q': 0x51, 'r': 0x52,
    's': 0x53, 't': 0x54, 'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58,
    'y': 0x59, 'z': 0x5A,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73, 'f5': 0x74,
    'f6': 0x75, 'f7': 0x76, 'f8': 0x77, 'f9': 0x78, 'f10': 0x79,
    'f11': 0x7A, 'f12': 0x7B,
    'space': 0x20, 'enter': 0x0D, 'return': 0x0D, 'tab': 0x09,
    'escape': 0x1B, 'esc': 0x1B, 'backspace': 0x08, 'delete': 0x2E,
}

_MOD_ALT = 0x0001
_MOD_CONTROL = 0x0002
_MOD_SHIFT = 0x0004
_MOD_WIN = 0x0008
_WM_HOTKEY = 0x0312


class GlobalHotkeyManager:
    """Cross-platform global hotkey registration.

    On Windows uses ``RegisterHotKey`` (native API, works with PyQt6).
    On macOS/Linux uses ``pynput.keyboard.GlobalHotKeys``.

    Usage::

        manager = GlobalHotkeyManager()
        manager.register('ctrl+alt+l', on_superlookup)
        manager.register('ctrl+alt+m', on_quicktrans)
        success = manager.start()
        ...
        manager.stop()
    """

    def __init__(self):
        self._hotkeys: Dict[str, Callable] = {}  # shortcut string -> callback
        self._running = False
        self._backend = None  # 'winapi' or 'pynput'

        # Windows-specific
        self._win_thread = None
        self._win_thread_id = None
        self._win_hotkey_ids: Dict[int, Callable] = {}  # hotkey_id -> callback
        self._next_id = 1

        # pynput-specific
        self._listener = None
        self._pynput_hotkeys: Dict[str, Callable] = {}

    # -- public API ----------------------------------------------------------

    @property
    def is_available(self) -> bool:
        if IS_WINDOWS:
            return True  # RegisterHotKey is always available
        # Check pynput
        try:
            from pynput.keyboard import GlobalHotKeys  # noqa: F401
            return True
        except ImportError:
            return False

    @property
    def running(self) -> bool:
        return self._running

    def register(self, shortcut: str, callback: Callable) -> bool:
        """Register a global hotkey.

        *shortcut* uses the format ``'ctrl+alt+l'``.  The *callback* will
        be invoked from a **background thread** — callers must dispatch to
        the Qt main thread themselves (e.g. via ``QTimer.singleShot``).
        """
        self._hotkeys[shortcut.lower()] = callback
        return True

    def start(self) -> bool:
        """Start listening for registered hotkeys.  Returns ``True`` on success."""
        if not self._hotkeys:
            return False

        if IS_WINDOWS:
            return self._start_winapi()
        else:
            return self._start_pynput()

    def stop(self):
        """Stop listening for hotkeys."""
        if self._backend == 'winapi':
            self._stop_winapi()
        elif self._backend == 'pynput':
            self._stop_pynput()
        self._running = False

    # -- Windows RegisterHotKey backend --------------------------------------

    def _start_winapi(self) -> bool:
        """Register hotkeys using the Windows RegisterHotKey API."""
        import ctypes
        import ctypes.wintypes
        import threading

        # Parse shortcuts and assign IDs
        self._win_hotkey_ids.clear()
        registrations = []
        for shortcut, callback in self._hotkeys.items():
            mods, vk = self._parse_shortcut_winapi(shortcut)
            if vk is None:
                print(f"[GlobalHotkeyManager] Unknown key in shortcut: {shortcut}")
                continue
            hk_id = self._next_id
            self._next_id += 1
            self._win_hotkey_ids[hk_id] = callback
            registrations.append((hk_id, mods, vk, shortcut))

        if not registrations:
            return False

        ready_event = threading.Event()
        success_flag = [False]

        def _message_pump():
            user32 = ctypes.windll.user32
            self._win_thread_id = ctypes.windll.kernel32.GetCurrentThreadId()

            all_ok = True
            for hk_id, mods, vk, shortcut in registrations:
                if not user32.RegisterHotKey(None, hk_id, mods, vk):
                    print(f"[GlobalHotkeyManager] Failed to register {shortcut} "
                          f"(may be in use by another application)")
                    all_ok = False
                else:
                    print(f"[GlobalHotkeyManager] Registered {shortcut} (WinAPI)")

            success_flag[0] = all_ok or len(self._win_hotkey_ids) > 0
            ready_event.set()

            if not success_flag[0]:
                return

            # Message loop — blocks until PostThreadMessage(WM_QUIT)
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
                if msg.message == _WM_HOTKEY:
                    hk_id = msg.wParam
                    cb = self._win_hotkey_ids.get(hk_id)
                    if cb:
                        try:
                            cb()
                        except Exception as e:
                            print(f"[GlobalHotkeyManager] Callback error: {e}")

            # Unregister on exit
            for hk_id in self._win_hotkey_ids:
                user32.UnregisterHotKey(None, hk_id)

        self._win_thread = threading.Thread(target=_message_pump, daemon=True,
                                            name="GlobalHotkeyManager-WinAPI")
        self._win_thread.start()
        ready_event.wait(timeout=2)

        if success_flag[0]:
            self._running = True
            self._backend = 'winapi'
            return True
        return False

    def _stop_winapi(self):
        """Stop the WinAPI message pump thread."""
        if self._win_thread_id:
            import ctypes
            # Post WM_QUIT to the thread's message queue
            ctypes.windll.user32.PostThreadMessageW(
                self._win_thread_id, 0x0012, 0, 0  # WM_QUIT
            )
            if self._win_thread:
                self._win_thread.join(timeout=2)
            self._win_thread = None
            self._win_thread_id = None

    @staticmethod
    def _parse_shortcut_winapi(shortcut: str):
        """Parse ``'ctrl+alt+l'`` into (modifiers, vk_code) for RegisterHotKey."""
        parts = shortcut.lower().split('+')
        mods = 0
        vk = None
        for part in parts:
            part = part.strip()
            if part in ('ctrl', 'control'):
                mods |= _MOD_CONTROL
            elif part == 'alt':
                mods |= _MOD_ALT
            elif part == 'shift':
                mods |= _MOD_SHIFT
            elif part in ('win', 'super', 'cmd'):
                mods |= _MOD_WIN
            else:
                vk = _VK_MAP.get(part)
        return mods, vk

    # -- pynput backend (macOS / Linux) --------------------------------------

    def _start_pynput(self) -> bool:
        """Register hotkeys using pynput GlobalHotKeys."""
        try:
            from pynput.keyboard import GlobalHotKeys
        except ImportError:
            print("[GlobalHotkeyManager] pynput not installed — "
                  "global hotkeys unavailable")
            return False

        self._pynput_hotkeys.clear()
        for shortcut, callback in self._hotkeys.items():
            pynput_key = self._convert_shortcut_pynput(shortcut)
            self._pynput_hotkeys[pynput_key] = callback

        try:
            self._listener = GlobalHotKeys(self._pynput_hotkeys)
            self._listener.daemon = True
            self._listener.start()
            self._running = True
            self._backend = 'pynput'
            registered = ', '.join(self._pynput_hotkeys.keys())
            print(f"[GlobalHotkeyManager] Started (pynput) — hotkeys: {registered}")
            if IS_MACOS:
                print("[GlobalHotkeyManager] macOS note: global hotkeys require "
                      "Accessibility permission (System Settings → Privacy & Security "
                      "→ Accessibility). If hotkeys don't work, check this setting.")
            return True
        except Exception as e:
            print(f"[GlobalHotkeyManager] pynput failed to start: {e}")
            if IS_MACOS:
                print("[GlobalHotkeyManager] macOS: grant Accessibility permission "
                      "to this app in System Settings → Privacy & Security → Accessibility")
            return False

    def _stop_pynput(self):
        """Stop the pynput listener."""
        if self._listener:
            try:
                self._listener.stop()
            except Exception:
                pass
            self._listener = None

    @staticmethod
    def _convert_shortcut_pynput(shortcut: str) -> str:
        """Convert ``'ctrl+alt+l'`` to pynput ``'<ctrl>+<alt>+l'``."""
        parts = shortcut.lower().split('+')
        converted: List[str] = []
        for part in parts:
            part = part.strip()
            if part in ('ctrl', 'control'):
                converted.append('<ctrl>')
            elif part == 'alt':
                converted.append('<alt>')
            elif part == 'shift':
                converted.append('<shift>')
            elif part in ('cmd', 'win', 'super'):
                converted.append('<cmd>')
            else:
                converted.append(part)
        return '+'.join(converted)


# ---------------------------------------------------------------------------
# Cross-platform Keystroke Sender (using pynput)
# ---------------------------------------------------------------------------
class CrossPlatformKeySender:
    """Send keystrokes programmatically.

    On Windows, uses AutoHotkey (proven reliable for cross-process keystroke
    injection) with a PowerShell ``SendKeys`` fallback.

    On macOS/Linux, uses ``pynput.keyboard.Controller``.
    """

    _ahk_exe: Optional[str] = None   # cached AHK path (class-level)
    _ahk_searched: bool = False

    def __init__(self):
        self._controller = None
        self._Key = None
        # Only need pynput Controller on Linux (macOS uses osascript,
        # Windows uses AHK/PowerShell)
        if IS_LINUX:
            try:
                from pynput.keyboard import Controller, Key
                self._controller = Controller()
                self._Key = Key
            except ImportError:
                print("[CrossPlatformKeySender] pynput not installed")
            except Exception as e:
                print(f"[CrossPlatformKeySender] pynput init error: {e}")

    @property
    def is_available(self) -> bool:
        if IS_WINDOWS or IS_MACOS:
            return True  # AHK/PowerShell on Windows, osascript on macOS
        return self._controller is not None  # Linux needs pynput

    # -- AHK path discovery (Windows) ----------------------------------------

    @classmethod
    def _find_ahk(cls) -> Optional[str]:
        """Locate AutoHotkey on Windows.  Result is cached."""
        if cls._ahk_searched:
            return cls._ahk_exe
        cls._ahk_searched = True

        # shutil.which covers PATH
        found = shutil.which('AutoHotkey')
        if found:
            cls._ahk_exe = found
            print(f"[CrossPlatformKeySender] AHK found on PATH: {found}")
            return cls._ahk_exe

        # Common installation directories
        username = os.environ.get('USERNAME', '')
        candidates = [
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey.exe",
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe",
            r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
            r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
            fr"C:\Users\{username}\AppData\Local\Programs\AutoHotkey\AutoHotkey.exe",
            r"C:\Program Files\AutoHotkey\v1.1\AutoHotkeyU64.exe",
            r"C:\Program Files\AutoHotkey\v1.1\AutoHotkeyU32.exe",
        ]
        for path in candidates:
            if os.path.isfile(path):
                cls._ahk_exe = path
                print(f"[CrossPlatformKeySender] AHK found: {path}")
                return cls._ahk_exe

        print("[CrossPlatformKeySender] AHK not found — will use PowerShell fallback")
        return None

    # -- Public API ----------------------------------------------------------

    def send_copy(self):
        """Send Ctrl+C (or Cmd+C on macOS) to copy the current selection.

        Each platform uses a proven external mechanism:
        - Windows: AHK subprocess (or PowerShell fallback)
        - macOS: ``osascript`` (AppleScript via System Events)
        - Linux: pynput Controller
        """
        if IS_WINDOWS:
            self._send_copy_win32()
        elif IS_MACOS:
            self._send_copy_macos()
        elif self._controller:
            Key = self._Key
            with self._controller.pressed(Key.ctrl):
                self._controller.tap('c')

    # -- macOS-specific implementation ---------------------------------------

    @staticmethod
    def _send_copy_macos():
        """Send Cmd+C via osascript (macOS native automation).

        Uses AppleScript ``System Events`` to inject a keystroke into the
        foreground application — equivalent to AHK on Windows.  Runs as a
        separate process, so it's thread-safe.
        """
        try:
            subprocess.run(
                ['osascript', '-e',
                 'tell application "System Events" to keystroke "c" using command down'],
                timeout=3,
                capture_output=True,
            )
        except Exception as e:
            print(f"[CrossPlatformKeySender] osascript Cmd+C failed: {e}")

    # -- Windows-specific implementation -------------------------------------

    @classmethod
    def _send_copy_win32(cls):
        """Send Ctrl+C to the foreground app on Windows.

        Strategy:
        1. AHK inline script  — ``Send ^c``  (works perfectly, proven)
        2. PowerShell SendKeys — ``[System.Windows.Forms.SendKeys]::SendWait('^c')``
        """
        ahk = cls._find_ahk()
        if ahk:
            cls._send_copy_via_ahk(ahk)
        else:
            cls._send_copy_via_powershell()

    @staticmethod
    def _send_copy_via_ahk(ahk_exe: str):
        """Run a minimal AHK script that sends Ctrl+C."""
        try:
            # AHK v2 syntax: Send "^c"
            # AHK v1 syntax: Send, ^c
            # Detect version from path
            is_v2 = 'v2' in ahk_exe.lower()
            if is_v2:
                script = 'Send "^c"\nSleep 100'
            else:
                script = 'Send, ^c\nSleep, 100'

            # /ErrorStdOut suppresses error dialogs; we pipe the script via
            # a temp file because AHK doesn't accept scripts on stdin reliably.
            import tempfile
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.ahk', delete=False, encoding='utf-8'
            ) as f:
                f.write(script + '\n')
                tmp_path = f.name

            subprocess.run(
                [ahk_exe, '/ErrorStdOut', tmp_path],
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        except Exception as e:
            print(f"[CrossPlatformKeySender] AHK Ctrl+C failed: {e}")
            # Fall back to PowerShell
            CrossPlatformKeySender._send_copy_via_powershell()

    @staticmethod
    def _send_copy_via_powershell():
        """Send Ctrl+C via PowerShell SendKeys (fallback if AHK unavailable)."""
        try:
            subprocess.run(
                [
                    'powershell', '-NoProfile', '-NonInteractive', '-Command',
                    'Add-Type -AssemblyName System.Windows.Forms; '
                    '[System.Windows.Forms.SendKeys]::SendWait("^c")'
                ],
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception as e:
            print(f"[CrossPlatformKeySender] PowerShell SendKeys failed: {e}")

    def send_paste(self):
        """Send Ctrl+V (or Cmd+V on macOS) to paste.

        Uses the same platform-native approach as ``send_copy()``:
        - Windows: AHK subprocess (or PowerShell fallback)
        - macOS: osascript (AppleScript via System Events)
        - Linux: pynput Controller
        """
        if IS_WINDOWS:
            self._send_paste_win32()
        elif IS_MACOS:
            self._send_paste_macos()
        elif self._controller:
            Key = self._Key
            with self._controller.pressed(Key.ctrl):
                self._controller.tap('v')

    def _send_paste_win32(self):
        """Send Ctrl+V on Windows via AHK or PowerShell.

        Uses the same temp-file approach as ``_send_copy_via_ahk`` because
        AHK does not reliably accept scripts via stdin.
        """
        ahk = self._find_ahk()
        if ahk:
            try:
                import tempfile
                is_v2 = 'v2' in ahk.lower()
                if is_v2:
                    script = 'Send "^v"\nSleep 100'
                else:
                    script = 'Send, ^v\nSleep, 100'

                with tempfile.NamedTemporaryFile(
                    mode='w', suffix='.ahk', delete=False, encoding='utf-8'
                ) as f:
                    f.write(script + '\n')
                    tmp_path = f.name

                subprocess.run(
                    [ahk, '/ErrorStdOut', tmp_path],
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )

                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                return
            except Exception as e:
                print(f"[CrossPlatformKeySender] AHK paste failed: {e}")

        # Fallback: PowerShell SendKeys
        try:
            subprocess.run(
                [
                    'powershell', '-NoProfile', '-NonInteractive', '-Command',
                    'Add-Type -AssemblyName System.Windows.Forms; '
                    '[System.Windows.Forms.SendKeys]::SendWait("^v")'
                ],
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception as e:
            print(f"[CrossPlatformKeySender] PowerShell paste failed: {e}")

    @staticmethod
    def _send_paste_macos():
        """Send Cmd+V via osascript (macOS)."""
        try:
            subprocess.run(
                ['osascript', '-e',
                 'tell application "System Events" to keystroke "v" '
                 'using command down'],
                capture_output=True, timeout=5,
            )
        except Exception as e:
            print(f"[CrossPlatformKeySender] macOS paste failed: {e}")

    def send_keystroke(self, keystroke: str):
        """Send a compound keystroke like ``'ctrl+s'``, ``'ctrl+shift+l'``,
        ``'f10'``, ``'shift+f10'``, etc.

        Supports modifiers: ctrl, alt, shift, cmd/win.
        Supports special keys: enter, tab, escape, backspace, delete,
        f1–f12, arrow keys, home, end, page up/down, space, insert.

        Uses the same platform-native approach as ``send_copy()``:
        - Windows: AHK subprocess (or PowerShell fallback)
        - macOS: osascript (AppleScript via System Events)
        - Linux: pynput Controller
        """
        if IS_WINDOWS:
            self._send_keystroke_win32(keystroke)
            return
        if IS_MACOS:
            self._send_keystroke_macos(keystroke)
            return

        # Linux: use pynput
        if not self._controller:
            return
        Key = self._Key

        parts = keystroke.lower().split('+')
        modifiers: List = []
        key = None

        modifier_map = {
            'ctrl': Key.ctrl, 'control': Key.ctrl,
            'alt': Key.alt,
            'shift': Key.shift,
            'cmd': Key.cmd, 'win': Key.cmd, 'super': Key.cmd,
        }

        special_map = {
            'enter': Key.enter, 'return': Key.enter,
            'tab': Key.tab,
            'escape': Key.esc, 'esc': Key.esc,
            'space': Key.space,
            'backspace': Key.backspace,
            'delete': Key.delete, 'del': Key.delete,
            'insert': Key.insert,
            'home': Key.home, 'end': Key.end,
            'pageup': Key.page_up, 'page_up': Key.page_up,
            'pagedown': Key.page_down, 'page_down': Key.page_down,
            'up': Key.up, 'down': Key.down,
            'left': Key.left, 'right': Key.right,
            'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3, 'f4': Key.f4,
            'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8,
            'f9': Key.f9, 'f10': Key.f10, 'f11': Key.f11, 'f12': Key.f12,
        }

        for part in parts:
            part = part.strip()
            if part in modifier_map:
                modifiers.append(modifier_map[part])
            elif part in special_map:
                key = special_map[part]
            else:
                key = part  # single character key

        with contextlib.ExitStack() as stack:
            for mod in modifiers:
                stack.enter_context(self._controller.pressed(mod))
            if key is not None:
                if isinstance(key, str):
                    self._controller.tap(key)
                else:
                    self._controller.tap(key)

    def _keystroke_to_ahk(self, keystroke: str) -> str:
        """Convert a keystroke string like ``'ctrl+alt+p'`` to AHK Send format."""
        modifiers = {
            'ctrl': '^', 'control': '^',
            'alt': '!',
            'shift': '+',
            'win': '#', 'windows': '#',
        }
        special_keys = {
            'enter': '{Enter}', 'return': '{Enter}',
            'tab': '{Tab}',
            'escape': '{Esc}', 'esc': '{Esc}',
            'space': '{Space}',
            'backspace': '{Backspace}',
            'delete': '{Delete}', 'del': '{Delete}',
            'insert': '{Insert}', 'ins': '{Insert}',
            'home': '{Home}', 'end': '{End}',
            'pageup': '{PgUp}', 'pgup': '{PgUp}',
            'pagedown': '{PgDn}', 'pgdn': '{PgDn}',
            'up': '{Up}', 'down': '{Down}',
            'left': '{Left}', 'right': '{Right}',
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
                result += part
        return result

    @staticmethod
    def _keystroke_to_applescript(keystroke: str) -> str:
        """Convert a keystroke string to an osascript command."""
        modifier_map = {
            'ctrl': 'control down', 'control': 'control down',
            'alt': 'option down',
            'shift': 'shift down',
            'cmd': 'command down', 'command': 'command down',
            'win': 'command down',
        }
        special_keys = {
            'enter': 'return', 'return': 'return',
            'tab': 'tab', 'escape': 'escape', 'esc': 'escape',
            'space': 'space', 'delete': 'delete', 'backspace': 'delete',
            'up': 'up arrow', 'down': 'down arrow',
            'left': 'left arrow', 'right': 'right arrow',
            'home': 'home', 'end': 'end',
            'pageup': 'page up', 'pagedown': 'page down',
            'f1': 'F1', 'f2': 'F2', 'f3': 'F3', 'f4': 'F4',
            'f5': 'F5', 'f6': 'F6', 'f7': 'F7', 'f8': 'F8',
            'f9': 'F9', 'f10': 'F10', 'f11': 'F11', 'f12': 'F12',
        }
        parts = keystroke.lower().replace(' ', '').split('+')
        mods = []
        key = None
        for part in parts:
            if part in modifier_map:
                mods.append(modifier_map[part])
            elif part in special_keys:
                key = special_keys[part]
            else:
                key = part
        if key is None:
            return ''
        # Determine if we need 'keystroke' (character) or 'key code' (special)
        is_special = keystroke.lower().replace(' ', '').split('+')[-1] in special_keys
        if is_special:
            action = f'key code (ASCII number of "{key}")'
            # For special keys, use 'keystroke' with the key name isn't ideal;
            # AppleScript uses 'keystroke' for characters. For special keys we
            # still use keystroke with the key name — AppleScript handles most.
        using = ''
        if mods:
            using = ' using {' + ', '.join(mods) + '}'
        return (f'tell application "System Events" to keystroke "{key}"'
                f'{using}')

    def _send_keystroke_win32(self, keystroke: str):
        """Send an arbitrary keystroke on Windows via AHK or PowerShell.

        Uses the same proven pattern as ``VoiceCommandManager._run_ahk_code``:
        AHK v2 script with ``#Requires``, ``Popen`` (non-blocking).
        """
        ahk = self._find_ahk()
        ahk_keys = self._keystroke_to_ahk(keystroke)
        if ahk:
            try:
                import tempfile
                # Always use AHK v2 syntax with #Requires header
                # (matches the proven pattern in voice_commands._run_ahk_code)
                script = (
                    f'#Requires AutoHotkey v2.0\n'
                    f'#SingleInstance Force\n'
                    f'Send "{ahk_keys}"\n'
                    f'ExitApp\n'
                )
                with tempfile.NamedTemporaryFile(
                    mode='w', suffix='.ahk', delete=False, encoding='utf-8'
                ) as f:
                    f.write(script)
                    tmp_path = f.name
                subprocess.Popen(
                    [ahk, tmp_path],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                return
            except Exception as e:
                print(f"[CrossPlatformKeySender] AHK keystroke failed: {e}")

        # Fallback: PowerShell SendKeys (limited — no Alt support)
        ps_keys = self._keystroke_to_powershell_sendkeys(keystroke)
        if ps_keys:
            try:
                subprocess.run(
                    [
                        'powershell', '-NoProfile', '-NonInteractive',
                        '-Command',
                        'Add-Type -AssemblyName System.Windows.Forms; '
                        f'[System.Windows.Forms.SendKeys]::SendWait("{ps_keys}")'
                    ],
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            except Exception as e:
                print(f"[CrossPlatformKeySender] PowerShell keystroke failed: {e}")

    @staticmethod
    def _keystroke_to_powershell_sendkeys(keystroke: str) -> str:
        """Convert keystroke to PowerShell SendKeys format (best-effort)."""
        mod_map = {'ctrl': '^', 'control': '^', 'alt': '%', 'shift': '+'}
        special = {
            'enter': '{ENTER}', 'return': '{ENTER}', 'tab': '{TAB}',
            'escape': '{ESC}', 'esc': '{ESC}', 'backspace': '{BACKSPACE}',
            'delete': '{DELETE}', 'del': '{DELETE}',
            'up': '{UP}', 'down': '{DOWN}', 'left': '{LEFT}',
            'right': '{RIGHT}', 'home': '{HOME}', 'end': '{END}',
            'pageup': '{PGUP}', 'pagedown': '{PGDN}',
            'f1': '{F1}', 'f2': '{F2}', 'f3': '{F3}', 'f4': '{F4}',
            'f5': '{F5}', 'f6': '{F6}', 'f7': '{F7}', 'f8': '{F8}',
            'f9': '{F9}', 'f10': '{F10}', 'f11': '{F11}', 'f12': '{F12}',
        }
        parts = keystroke.lower().replace(' ', '').split('+')
        prefix = ''
        key = ''
        for part in parts:
            if part in mod_map:
                prefix += mod_map[part]
            elif part in special:
                key = special[part]
            else:
                key = part
        if not key:
            return ''
        return prefix + key

    def _send_keystroke_macos(self, keystroke: str):
        """Send an arbitrary keystroke on macOS via osascript."""
        try:
            script = self._keystroke_to_applescript(keystroke)
            if script:
                subprocess.run(
                    ['osascript', '-e', script],
                    capture_output=True, timeout=5,
                )
        except Exception as e:
            print(f"[CrossPlatformKeySender] macOS keystroke failed: {e}")
