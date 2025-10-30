# Supervertaler Qt v1.0.0 - Phase 5 Release Notes

**Release Date**: October 29, 2025  
**Version**: Qt v1.0.0 Phase 5  
**Status**: Production Ready

---

## 🎯 Phase 5 Overview: Universal Lookup & UI Polish

Phase 5 introduces **Universal Lookup**, a revolutionary feature that lets you search your translation memory from anywhere on your computer, and comprehensive UI improvements for a polished professional experience.

---

## ✨ Major Features

### 🔍 Universal Lookup - System-Wide TM Search

**What is it?**  
Universal Lookup lets you search your translation memory from ANY application on your computer - not just Supervertaler. Select text in memoQ, Trados, Word, a browser, or any text editor, press **Ctrl+Alt+L**, and get instant TM matches.

**Key Features**:
- 🌍 **Works anywhere** - Any application, any text box
- ⚡ **Instant results** - TM matches appear in less than a second
- 🎯 **Non-destructive** - Doesn't delete or modify your selected text
- 🖥️ **Multi-monitor support** - Automatically activates Supervertaler window across monitors
- 🔒 **Reliable** - Hybrid Python+AutoHotkey architecture for robust operation

**How to Use**:
1. Open Supervertaler Qt (Universal Lookup tab is Tab 0)
2. Work in any application (memoQ, Word, browser, etc.)
3. Select text you want to look up
4. Press **Ctrl+Alt+L**
5. Supervertaler pops up with TM/Glossary matches
6. Copy or insert translations as needed

**Supported Platforms**:
- ✅ **Windows** - Full support with global hotkey (requires AutoHotkey v2)
- ⚠️ **Mac/Linux** - Manual paste mode (copy text, paste into Universal Lookup tab)

**Installation Requirements** (Windows):
```bash
# Install AutoHotkey v2
# Download from: https://www.autohotkey.com/

# Python dependencies (already included)
pip install pyperclip
```

**Technical Highlights**:
- AutoHotkey v2 handles clipboard operations (Python's clipboard is unreliable on Windows)
- File-based signaling between AHK and Python (100% thread-safe)
- Automatic cleanup on exit (no orphaned processes)
- Windows API AttachThreadInput for cross-monitor focus stealing

---

### 🎨 Theme System Enhancements

**6 Predefined Themes**:
1. **Light (Default)** - Clean, bright workspace
2. **Soft Gray** - Gentle on the eyes
3. **Sepia** - Warm, paper-like tones
4. **Dark** - Modern dark mode
5. **High Contrast Blue** - Maximum readability
6. **High Contrast Yellow** - Alternative high visibility

**Custom Theme Editor**:
- Create your own color schemes
- Save and load custom themes
- Live preview of changes
- Full color customization for all UI elements

**UI Spacing Improvements**:
- Fixed "squished" text in dialogs
- Proper padding in group boxes (18px top, 10px sides/bottom)
- Label padding for better readability (3px vertical)
- Form layout spacing (8px between rows)
- Activity Log readability improvements (8px padding, 1.4 line-height)

---

### ⌨️ Keyboard Shortcuts Update

**Conflict Resolution**:
- Changed AutoFingers loop mode shortcut to avoid conflicts
- Separated Universal Lookup and AutoFingers shortcuts clearly

**Updated Shortcuts**:

**Universal Lookup**:
- **Ctrl+Alt+L** - Capture text and search TM (works anywhere)

**AutoFingers**:
- **Ctrl+Alt+P** - Process single segment
- **Ctrl+Shift+L** - Toggle loop mode (changed from Ctrl+Alt+L)
- **Ctrl+Alt+S** - Stop loop
- **Ctrl+Alt+R** - Reload TMX

**Why the Change?**:
- Ctrl+Alt+L reserved for Universal Lookup (primary feature)
- Ctrl+Alt+O and Ctrl+Alt+I conflicted with memoQ diacritic shortcuts
- Ctrl+Shift+L is safe and memorable (same "L", different modifiers)

---

## 🐛 Bug Fixes

### AutoHotkey Process Management
- ✅ **Fixed orphaned AHK processes** - No more scripts running after Supervertaler closes
- ✅ **No "script already running" popups** - Automatic cleanup of existing instances
- ✅ **Multiple cleanup layers** - `atexit`, `closeEvent`, `__del__`, `unregister_global_hotkey`
- ✅ **Global tracking** - `_ahk_process` variable ensures cleanup on any exit condition

### Window Activation
- ✅ **Multi-monitor support** - Windows API AttachThreadInput for cross-monitor focus
- ✅ **Maximized state preservation** - Detects and restores maximized windows
- ✅ **No flicker** - Removed WindowStaysOnTopHint approach

### UI Polish
- ✅ **Fixed cut-off text** - Proper padding in Theme Editor, AutoFingers, Options dialogs
- ✅ **Group box titles** - No longer cut off at the top
- ✅ **Form labels** - Adequate spacing prevents cramped appearance
- ✅ **Activity Log** - Comfortable reading with proper line-height

---

## 📦 Technical Details

### Files Modified

**Main Application**:
- `Supervertaler_Qt_v1.0.0.py` (4972 lines)
  - Universal Lookup tab as Tab 0
  - Global AHK process tracking and cleanup
  - Window `closeEvent` for cleanup
  - Multi-monitor activation logic

**New Files**:
- `universal_lookup_hotkey.ahk` (39 lines)
  - AutoHotkey v2 script for global hotkey
  - Ctrl+Alt+L hotkey registration
  - Clipboard copy with proper timing
  - File-based signaling to Python

**Modules**:
- `modules/universal_lookup.py` (239 lines)
  - Universal Lookup engine
  - Non-destructive text capture
  - TM/Glossary search integration
  - Multiple CAT tool modes
  
- `modules/theme_manager.py` (481 lines)
  - Enhanced QGroupBox styling
  - QLabel padding for readability
  - QFormLayout vertical spacing
  - 6 predefined themes + custom editor

### Architecture Decisions

**Why AutoHotkey?**
- Python's clipboard handling on Windows is unreliable
- Python keyboard libraries cause destructive behavior (deleting text, selecting all)
- AutoHotkey is the standard for reliable global hotkeys on Windows

**Why File-Based Signaling?**
- Thread-safe communication between AHK and Qt
- No callback complexity or race conditions
- Simple, reliable, debuggable

**Why atexit?**
- Most reliable way to ensure cleanup on any exit condition
- Handles normal close, crashes, Ctrl+C, etc.
- Python guarantees atexit handlers run before interpreter shutdown

**Why Windows API AttachThreadInput?**
- Only way to bypass Windows focus-stealing prevention
- Essential for cross-monitor window activation
- Native Windows solution for professional applications

### Dependencies

**New**:
- AutoHotkey v2 (Windows only) - For global hotkey support
- pyperclip - For clipboard operations

**Existing**:
- PyQt6 - GUI framework
- All previous dependencies remain unchanged

---

## 🎯 Platform Support

| Platform | Global Hotkey | Manual Paste | Status |
|----------|---------------|--------------|--------|
| Windows  | ✅ Yes        | ✅ Yes       | Full Support |
| Mac      | ❌ No         | ✅ Yes       | Partial Support |
| Linux    | ❌ No         | ✅ Yes       | Partial Support |

---

## 📝 Known Limitations

1. **Global hotkey Windows-only** - Ctrl+Alt+L requires AutoHotkey v2 on Windows
2. **Manual paste on Mac/Linux** - No global hotkey support on these platforms
3. **AutoHotkey background process** - Runs while Supervertaler is open (auto-managed)

---

## 🚀 What's Next?

**Future Enhancements**:
- Mac/Linux native clipboard solutions
- Customizable hotkey configuration
- MT provider integration (DeepL, OpenAI, Google Translate)
- Glossary term extraction from selected text
- Popup window mode (floating lookup window)
- System tray integration

---

## 🎓 Migration Guide

### From v3.7.x to Qt v1.0.0

**What's Different?**:
- Modern PyQt6 interface (cleaner, faster)
- Universal Lookup is new (not in v3.7.x)
- Theme system is new (not in v3.7.x)
- AutoFingers shortcuts changed (see above)

**What's the Same?**:
- Project file format (JSON)
- TMX file format
- Translation workflow
- Core CAT features

**Recommended Approach**:
- Run both versions in parallel during transition
- Test critical workflows in Qt version
- Report any issues or missing features

---

## 📞 Support

**Issues**: Report on GitHub repository  
**Documentation**: See `/docs` folder  
**Changelog**: See `CHANGELOG.md`  

---

## 🙏 Credits

**Developed by**: Michael Beijer  
**Testing**: Michael Beijer  
**Architecture**: Hybrid Python+AutoHotkey approach  
**Inspired by**: memoQ, Trados, CafeTran, Heartsome TMX Editor  

---

*Phase 5 represents a major milestone in Supervertaler's evolution, bringing system-wide translation lookup to professional translators worldwide.*
