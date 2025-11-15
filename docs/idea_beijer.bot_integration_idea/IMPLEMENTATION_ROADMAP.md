# Implementation Roadmap: Supervertaler QuickMenu

**Purpose:** Step-by-step guide for implementing the Beijer.bot → Supervertaler QuickMenu integration.

---

## 🎯 Project Goals

1. **Rebrand** Beijer.bot as Supervertaler QuickMenu
2. **Integrate** with Supervertaler main application
3. **Create** Python CLI bridge for communication
4. **Package** as unified translator toolkit
5. **Document** comprehensively for users and developers

---

## 📅 Timeline & Phases

### Phase 1: Foundation (Week 1-2)
**Goal:** Set up project structure and basic rebranding

### Phase 2: CLI Bridge (Week 3-4)
**Goal:** Create Python CLI for integration

### Phase 3: Integration (Week 5-6)
**Goal:** Connect QuickMenu to Supervertaler

### Phase 4: Polish & Release (Week 7-8)
**Goal:** Testing, documentation, packaging

---

## 📋 Detailed Task Breakdown

### Phase 1: Foundation

#### Task 1.1: Project Structure Setup
**Location:** `C:\Dev\Supervertaler\`

```bash
# Create directory structure
Supervertaler/
├── quickmenu/                    # NEW: QuickMenu source files
│   ├── Supervertaler_QuickMenu.ahk
│   ├── config/
│   │   └── quickmenu_config.ini
│   ├── icons/
│   │   └── quickmenu.ico
│   └── README.md
├── docs/
│   └── integration/              # EXISTING: These docs
├── supervertaler_cli.py          # NEW: CLI bridge
└── supervertaler/
    └── cli/                      # NEW: CLI module
        ├── __init__.py
        ├── commands.py
        ├── translator.py
        └── output.py
```

**Actions:**
- [x] Create `quickmenu/` directory
- [ ] Copy Beijer.bot files to `quickmenu/`
- [ ] Rename main script to `Supervertaler_QuickMenu.ahk`
- [ ] Create `supervertaler/cli/` module structure
- [ ] Set up version control branches

**Time Estimate:** 1-2 hours

---

#### Task 1.2: Basic Rebranding
**File:** `quickmenu/Supervertaler_QuickMenu.ahk`

**Changes:**
```autohotkey
; OLD
MenuPopup.Add("Beijer.bot (click to edit)", EditBeijerBot)

; NEW
MenuPopup.Add("Supervertaler QuickMenu v1.0", EditScript)
MenuPopup.Add("Open Supervertaler (Main App)", OpenSupervertaler)
```

**Checklist:**
- [ ] Update script header comments
- [ ] Change window titles
- [ ] Update tray icon
- [ ] Change about dialog
- [ ] Update all menu references
- [ ] Update variable names (BeijerBot → QuickMenu)
- [ ] Update hotkey comments

**Time Estimate:** 2-3 hours

---

#### Task 1.3: Menu Restructuring
**Goal:** Reorganize menu with Supervertaler integration section

**New Menu Structure:**
```autohotkey
MenuPopup := Menu()
MenuPopup.Add("Supervertaler QuickMenu v1.0", ShowAbout)
MenuPopup.Add("Settings", ShowSettings)
MenuPopup.Add()

; SUPERVERTALER INTEGRATION (NEW)
MenuPopup.Add("&SUPERVERTALER:", NOP, "BarBreak")
MenuPopup.Add("• Open Supervertaler", OpenSupervertaler)
MenuPopup.Add("• Quick Translate Selection", QuickTranslate)  ; Will implement later
MenuPopup.Add("• Universal Lookup (Ctrl+Alt+L)", TriggerUniversalLookup)
MenuPopup.Add("• Open PDF Rescue", OpenPDFRescue)
MenuPopup.Add("• Open TMX Editor", OpenTMXEditor)
MenuPopup.Add()

; AI TRANSLATION (KEEP & EXPAND)
MenuPopup.Add("&AI TRANSLATION:", NOP)
// ... existing ChatGPT features ...

; SEARCHES (KEEP ALL)
MenuPopup.Add("&SEARCHES:", NOP, "BarBreak")
// ... existing search features ...

; TEXT TOOLS (KEEP ALL)
MenuPopup.Add("&TEXT TOOLS:", NOP)
// ... existing text manipulation ...

; SNIPPETS (REORGANIZE)
MenuPopup.Add("&SNIPPETS:", NOP, "BarBreak")
// ... existing snippets ...
```

**Checklist:**
- [ ] Create SUPERVERTALER section
- [ ] Add placeholder functions (OpenSupervertaler, QuickTranslate, etc.)
- [ ] Keep all existing features
- [ ] Test menu navigation
- [ ] Update hotkey assignments

**Time Estimate:** 3-4 hours

---

#### Task 1.4: Configuration System
**Goal:** Create settings dialog and config file system

**Create:** `quickmenu/config/quickmenu_config.ini`
```ini
[Supervertaler]
Path = C:\Dev\Supervertaler
PythonExecutable = python.exe
AutoStart = false

[Integration]
EnableQuickTranslate = true
EnableModuleLaunchers = true

[Hotkeys]
QuickMenu = ^+!k
UniversalLookup = ^!l
```

**Create Settings Dialog:**
```autohotkey
ShowSettings(*) {
    SettingsGui := Gui("+Resize", "QuickMenu Settings")
    SettingsGui.SetFont("s10")
    
    ; Supervertaler Integration
    SettingsGui.Add("GroupBox", "w450 h180", "Supervertaler Integration")
    
    SettingsGui.Add("Text", "xp+15 yp+30", "Supervertaler Installation Path:")
    PathEdit := SettingsGui.Add("Edit", "w350", SupervertalerPath)
    SettingsGui.Add("Button", "x+5 w70", "Browse").OnEvent("Click", BrowseSupervertalerPath)
    
    SettingsGui.Add("Text", "x30 y+15", "Python Executable:")
    PythonEdit := SettingsGui.Add("Edit", "w350", PythonExecutable)
    
    SettingsGui.Add("Checkbox", "x30 y+15 Checked" EnableQuickTranslate, "Enable Quick Translate")
    SettingsGui.Add("Checkbox", "x30 y+5 Checked" EnableModuleLaunchers, "Enable Module Launchers")
    
    ; Test Connection Button
    SettingsGui.Add("Button", "x30 y+15 w150", "Test Connection").OnEvent("Click", TestConnection)
    
    ; Save/Cancel
    SettingsGui.Add("Button", "x30 y+30 w100", "Save").OnEvent("Click", SaveSettings)
    SettingsGui.Add("Button", "x+10 w100", "Cancel").OnEvent("Click", (*) => SettingsGui.Destroy())
    
    SettingsGui.Show()
}

TestConnection(*) {
    ; Test if Supervertaler path is valid
    if FileExist(SupervertalerPath "\Supervertaler_Qt.py") {
        MsgBox "✓ Supervertaler found!`nPath is valid.", "Connection Test", "Iconi"
    } else {
        MsgBox "✗ Supervertaler not found at specified path.", "Connection Test", "IconX"
    }
}
```

**Checklist:**
- [ ] Create config file structure
- [ ] Implement IniRead/IniWrite functions
- [ ] Create settings dialog
- [ ] Add path validation
- [ ] Add test connection feature
- [ ] Handle first-run setup

**Time Estimate:** 4-5 hours

---

### Phase 2: CLI Bridge

#### Task 2.1: Basic CLI Structure
**Goal:** Create working CLI entry point

**Create:** `C:\Dev\Supervertaler\supervertaler_cli.py`

**Implementation:**
```python
#!/usr/bin/env python3
"""Supervertaler CLI Bridge"""

import sys
import argparse
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    parser = argparse.ArgumentParser(
        prog='supervertaler',
        description='Supervertaler CLI'
    )
    
    subparsers = parser.add_subparsers(dest='command')
    
    # Version command
    version_parser = subparsers.add_parser('version')
    
    # Translate command
    translate_parser = subparsers.add_parser('translate')
    translate_parser.add_argument('text')
    translate_parser.add_argument('--quick', action='store_true')
    translate_parser.add_argument('--source', default='auto')
    translate_parser.add_argument('--target', default='auto')
    
    args = parser.parse_args()
    
    if args.command == 'version':
        print("Supervertaler CLI v1.0.0")
        sys.exit(0)
    elif args.command == 'translate':
        # Placeholder - will implement in next task
        print("Translation not yet implemented")
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main()
```

**Test:**
```bash
cd C:\Dev\Supervertaler
python supervertaler_cli.py version
# Should output: Supervertaler CLI v1.0.0
```

**Checklist:**
- [ ] Create `supervertaler_cli.py`
- [ ] Set up argparse structure
- [ ] Test basic execution
- [ ] Add to git

**Time Estimate:** 2 hours

---

#### Task 2.2: CLI Module Structure
**Goal:** Create modular CLI architecture

**Create:** `supervertaler/cli/__init__.py`
```python
"""Supervertaler CLI Module"""
from .commands import register_all_commands, execute_command

__all__ = ['register_all_commands', 'execute_command']
```

**Create:** `supervertaler/cli/commands.py`
```python
"""CLI Command Implementations"""
import sys
from typing import Any

def register_all_commands(subparsers):
    """Register all CLI commands"""
    register_translate(subparsers)
    register_lookup(subparsers)
    register_version(subparsers)

def register_translate(subparsers):
    """Register translate command"""
    parser = subparsers.add_parser('translate', help='Translate text')
    parser.add_argument('text', help='Text to translate')
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--source', default='auto')
    parser.add_argument('--target', default='auto')
    parser.add_argument('--output', choices=['text', 'json'], default='text')

def execute_command(command: str, args) -> int:
    """Execute command and return exit code"""
    if command == 'translate':
        return execute_translate(args)
    elif command == 'version':
        return execute_version(args)
    else:
        return 1

def execute_translate(args) -> int:
    """Execute translate command"""
    # Will implement translation logic
    print(f"TODO: Translate '{args.text}'")
    return 0

def execute_version(args) -> int:
    """Show version info"""
    print("Supervertaler CLI v1.0.0")
    return 0
```

**Checklist:**
- [ ] Create `supervertaler/cli/` directory
- [ ] Create `__init__.py`
- [ ] Create `commands.py` with structure
- [ ] Update `supervertaler_cli.py` to use module
- [ ] Test command registration

**Time Estimate:** 3 hours

---

#### Task 2.3: Translation Implementation
**Goal:** Implement actual translation via Supervertaler core

**Update:** `supervertaler/cli/commands.py`

```python
def execute_translate(args) -> int:
    """Execute translate command"""
    try:
        from ..core.translator import Translator
        from ..core.config import Config
        
        # Load config
        config = Config.load()
        translator = Translator(config)
        
        # Translate
        result = translator.translate_quick(
            text=args.text,
            source_lang=args.source,
            target_lang=args.target
        )
        
        # Output
        if args.output == 'json':
            import json
            output = {
                'translation': result.translation,
                'source_lang': result.source_lang,
                'target_lang': result.target_lang
            }
            print(json.dumps(output, ensure_ascii=False))
        else:
            print(result.translation, end='')  # No newline
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 4
```

**Test:**
```bash
python supervertaler_cli.py translate "Hello world" --quick
# Should output Dutch translation
```

**Checklist:**
- [ ] Implement `translate_quick()` in Supervertaler core
- [ ] Add translation logic to CLI
- [ ] Test with various inputs
- [ ] Add error handling
- [ ] Test JSON output mode

**Time Estimate:** 6-8 hours

---

### Phase 3: Integration

#### Task 3.1: Launcher Functions (AutoHotkey)
**Goal:** QuickMenu can launch Supervertaler

**Implement in QuickMenu:**

```autohotkey
; Global config
SupervertalerPath := IniRead("config\quickmenu_config.ini", "Supervertaler", "Path", "C:\Dev\Supervertaler")
PythonExecutable := IniRead("config\quickmenu_config.ini", "Supervertaler", "PythonExecutable", "python.exe")

OpenSupervertaler(*) {
    supervertalerExe := SupervertalerPath "\Supervertaler_Qt.exe"
    supervertalerPy := SupervertalerPath "\Supervertaler_Qt.py"
    
    ; Check if already running
    if WinExist("ahk_exe Supervertaler_Qt.exe") {
        WinActivate
        return
    }
    
    ; Try .exe first, then .py
    if FileExist(supervertalerExe) {
        Run supervertalerExe
    } else if FileExist(supervertalerPy) {
        Run PythonExecutable ' "' supervertalerPy '"'
    } else {
        MsgBox "Supervertaler not found at:`n" SupervertalerPath "`n`nPlease configure the path in Settings.", "Supervertaler Not Found", "IconX"
    }
}

OpenPDFRescue(*) {
    pdfRescuePy := SupervertalerPath "\modules\pdf_rescue_qt.py"
    if FileExist(pdfRescuePy) {
        Run PythonExecutable ' "' pdfRescuePy '"'
    } else {
        MsgBox "PDF Rescue module not found.", "Module Not Found", "IconX"
    }
}

OpenTMXEditor(*) {
    tmxEditorPy := SupervertalerPath "\modules\tmx_editor_qt.py"
    if FileExist(tmxEditorPy) {
        Run PythonExecutable ' "' tmxEditorPy '"'
    } else {
        MsgBox "TMX Editor module not found.", "Module Not Found", "IconX"
    }
}

TriggerUniversalLookup(*) {
    if WinExist("ahk_exe Supervertaler_Qt.exe") {
        WinActivate
        Sleep 100
        Send "^!l"  ; Ctrl+Alt+L
    } else {
        MsgBox "Supervertaler is not running.`n`nPlease open Supervertaler first.", "Not Running", "Iconi"
    }
}
```

**Checklist:**
- [ ] Implement `OpenSupervertaler()`
- [ ] Implement module launchers
- [ ] Implement Universal Lookup trigger
- [ ] Add error handling
- [ ] Test all functions

**Time Estimate:** 3-4 hours

---

#### Task 3.2: Quick Translate (AutoHotkey)
**Goal:** Translate selected text via Python CLI

**Implement:**

```autohotkey
QuickTranslate(*) {
    ; Copy selected text
    savedClipboard := A_Clipboard
    A_Clipboard := ""
    Send "^c"
    
    if !ClipWait(2) {
        ToolTip "No text selected"
        SetTimer () => ToolTip(), -2000
        return
    }
    
    text := A_Clipboard
    A_Clipboard := savedClipboard
    
    ; Escape special characters
    text := StrReplace(text, '"', '\"')
    text := StrReplace(text, '`n', '\n')
    
    ; Build command
    cliPath := SupervertalerPath "\supervertaler_cli.py"
    command := PythonExecutable ' "' cliPath '" translate "' text '" --quick'
    
    ; Show progress
    ToolTip "Translating..."
    
    ; Execute
    try {
        shell := ComObject("WScript.Shell")
        exec := shell.Exec(A_ComSpec " /c " command)
        
        ; Wait with timeout
        timeout := 30000
        start := A_TickCount
        while (!exec.Status && (A_TickCount - start < timeout))
            Sleep 100
        
        ToolTip
        
        if (!exec.Status) {
            MsgBox "Translation timed out", "Error", "IconX"
            return
        }
        
        if (exec.ExitCode == 0) {
            result := exec.StdOut.ReadAll()
            A_Clipboard := result
            Send "^v"
            
            ; Success tooltip
            ToolTip "✓ Translated"
            SetTimer () => ToolTip(), -1500
        } else {
            error := exec.StdErr.ReadAll()
            MsgBox "Translation failed:`n`n" error, "Error", "IconX"
        }
    } catch as err {
        ToolTip
        MsgBox "Error executing translation:`n`n" err.Message, "Error", "IconX"
    }
}
```

**Checklist:**
- [ ] Implement Quick Translate
- [ ] Test with various text selections
- [ ] Add proper error handling
- [ ] Add loading indicator
- [ ] Test timeout handling
- [ ] Add success feedback

**Time Estimate:** 4-5 hours

---

### Phase 4: Polish & Package

#### Task 4.1: Testing
**Goal:** Comprehensive testing of all features

**Test Plan:**

1. **Integration Tests**
   - [ ] Launch Supervertaler from QuickMenu
   - [ ] Quick Translate functionality
   - [ ] Module launchers (PDF Rescue, TMX Editor)
   - [ ] Universal Lookup trigger
   - [ ] Settings dialog save/load

2. **CLI Tests**
   - [ ] All CLI commands execute correctly
   - [ ] Error handling works
   - [ ] JSON output format
   - [ ] Timeout handling

3. **Existing Features**
   - [ ] All search functions still work
   - [ ] Text manipulation tools work
   - [ ] Snippets function correctly
   - [ ] Hotstrings work
   - [ ] ChatGPT integration still functional

**Time Estimate:** 6-8 hours

---

#### Task 4.2: Documentation
**Goal:** Comprehensive user and developer documentation

**Create:**
- [ ] User Guide for QuickMenu
- [ ] Installation instructions
- [ ] Configuration guide
- [ ] Troubleshooting guide
- [ ] Developer documentation for CLI
- [ ] Integration examples

**Time Estimate:** 8-10 hours

---

#### Task 4.3: Packaging
**Goal:** Create distributable package

**Steps:**
1. **Compile QuickMenu**
   ```bash
   # Use Ahk2Exe to compile
   Ahk2Exe.exe /in "Supervertaler_QuickMenu.ahk" /out "Supervertaler_QuickMenu.exe"
   ```

2. **Create Package Structure**
   ```
   Supervertaler_Package/
   ├── Supervertaler_Qt.exe
   ├── Supervertaler_QuickMenu.exe
   ├── supervertaler_cli.py
   ├── README.md
   ├── INSTALL.md
   ├── config/
   │   ├── quickmenu_config.ini.template
   │   └── supervertaler_config.ini.template
   └── docs/
       ├── QuickMenu_Guide.pdf
       └── CLI_Reference.pdf
   ```

3. **Create Installer** (Optional)
   - Use Inno Setup or NSIS
   - Auto-detect Python
   - Configure paths
   - Create shortcuts

**Checklist:**
- [ ] Compile QuickMenu to .exe
- [ ] Create package structure
- [ ] Write installation guide
- [ ] Create installer (optional)
- [ ] Test installation process

**Time Estimate:** 6-8 hours

---

## 🚀 Quick Start Commands

### Set Up Development Environment
```bash
# Clone/navigate to Supervertaler
cd C:\Dev\Supervertaler

# Create QuickMenu directory
mkdir quickmenu
cd quickmenu

# Copy Beijer.bot files
cp "C:\Users\mbeijer\My Drive\Software\AutoHotkey\_current scripts\Beijer.bot\Beijer.bot.ahk" Supervertaler_QuickMenu.ahk

# Create CLI module
cd ..
mkdir -p supervertaler\cli
touch supervertaler\cli\__init__.py
touch supervertaler\cli\commands.py
```

### Test CLI
```bash
cd C:\Dev\Supervertaler
python supervertaler_cli.py version
python supervertaler_cli.py translate "Hello" --quick
```

### Test QuickMenu
```bash
# Open in VS Code or Cursor
code quickmenu\Supervertaler_QuickMenu.ahk

# Or run directly
"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe" quickmenu\Supervertaler_QuickMenu.ahk
```

---

## 📊 Progress Tracking

### Phase 1: Foundation
- [ ] Task 1.1: Project structure (1-2h)
- [ ] Task 1.2: Basic rebranding (2-3h)
- [ ] Task 1.3: Menu restructuring (3-4h)
- [ ] Task 1.4: Configuration system (4-5h)
**Total:** ~10-14 hours

### Phase 2: CLI Bridge
- [ ] Task 2.1: Basic CLI structure (2h)
- [ ] Task 2.2: CLI module structure (3h)
- [ ] Task 2.3: Translation implementation (6-8h)
**Total:** ~11-13 hours

### Phase 3: Integration
- [ ] Task 3.1: Launcher functions (3-4h)
- [ ] Task 3.2: Quick Translate (4-5h)
**Total:** ~7-9 hours

### Phase 4: Polish & Package
- [ ] Task 4.1: Testing (6-8h)
- [ ] Task 4.2: Documentation (8-10h)
- [ ] Task 4.3: Packaging (6-8h)
**Total:** ~20-26 hours

**Grand Total:** ~48-62 hours (6-8 days of full-time work)

---

## 🎯 Success Criteria

### Functional Requirements
- ✅ QuickMenu launches Supervertaler
- ✅ Quick Translate works via CLI
- ✅ Module launchers functional
- ✅ All existing features preserved
- ✅ Settings configurable via GUI
- ✅ Error handling comprehensive

### Quality Requirements
- ✅ No breaking bugs
- ✅ Fast response times (<3s for translation)
- ✅ Clear error messages
- ✅ Comprehensive documentation
- ✅ Easy installation process

### User Experience
- ✅ Intuitive menu structure
- ✅ Helpful tooltips/feedback
- ✅ Settings easy to configure
- ✅ Integration seamless
- ✅ Professional appearance

---

## 📝 Notes & Considerations

### Known Challenges
1. **Python Environment** - Users may not have Python
   - Solution: Bundle embedded Python or use PyInstaller

2. **Path Configuration** - First-time setup complexity
   - Solution: Auto-detect common paths, setup wizard

3. **Process Communication** - AHK ↔ Python reliability
   - Solution: Proper error handling, timeouts, retries

4. **Performance** - CLI startup time
   - Solution: Lazy imports, caching, persistent mode

---

**Last Updated:** 2025-01-06  
**Status:** ✅ Roadmap Complete - Ready to Start  
**Estimated Duration:** 6-8 days full-time work

