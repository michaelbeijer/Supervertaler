# Supervertaler Quickmenu Integration Plan

**Date:** 2025-01-06  
**Status:** Planning Phase  
**Goal:** Integrate Beijer.bot (AutoHotkey) as "Supervertaler Quickmenu" companion tool

---

## 🎯 Executive Summary

This document outlines the plan to integrate Beijer.bot (an AutoHotkey-based productivity menu) with Supervertaler as a companion tool called **"Supervertaler Quickmenu"**.

### The Vision

Create a unified translator toolkit:
- **Supervertaler** (Python/Qt) - The main application for deep translation work
- **Supervertaler Quickmenu** (AutoHotkey) - Lightning-fast companion for instant access anywhere in Windows

---

## 📊 Analysis: What Makes Each Tool Powerful

### Supervertaler (Python/Qt)
- ✅ Full-featured CAT tool companion
- ✅ Deep AI integration with 4-layer prompt architecture
- ✅ Rich editing interface (Grid, List, Document views)
- ✅ Heavy lifting features (TMX editing, PDF rescue, etc.)
- ✅ Users work **inside** the application
- ✅ Context-aware translation with multiple data sources

### Beijer.bot / Quickmenu (AutoHotkey)
- ✅ Lightning-fast access **anywhere** in Windows
- ✅ Context menu integration = zero workflow disruption
- ✅ Hotstrings & hotkeys for instant text expansion
- ✅ Works across ALL applications (not just Supervertaler)
- ✅ System-level integration
- ✅ Instant snippets, searches, text manipulation
- ✅ ChatGPT integration for quick AI operations

### Key Insight
**Don't compete - complement!** Each tool excels in different scenarios:
- Supervertaler: Deep, focused translation work
- Quickmenu: Quick access, text snippets, instant searches, cross-application productivity

---

## 🎨 Integration Options Considered

### Option 1: Companion Tools (✅ RECOMMENDED)
Keep separate but branded together as an ecosystem.

**Pros:**
- Each tool does what it's best at
- AutoHotkey's speed + Python's power
- Unified brand
- Users can use either/both
- No loss of AutoHotkey superpowers

**Cons:**
- Two codebases to maintain
- Need integration bridges

---

### Option 2: Expand Universal Lookup
Expand Supervertaler's existing Universal Lookup into a full command palette.

**Pros:**
- Single application
- Unified interface
- All features in one place

**Cons:**
- Python keyboard hooks are slower than AutoHotkey
- Hotstrings in Python aren't as smooth
- More complex to maintain
- Requires Supervertaler to be running
- Loses AutoHotkey's system-level integration

---

### Option 3: Hybrid Architecture
Use AutoHotkey as frontend, Python as backend.

**Pros:**
- Best of both worlds
- AutoHotkey's instant responsiveness
- Python's AI/translation power
- Unified experience

**Cons:**
- Complex architecture
- Requires both systems running

---

## 🏆 Recommended Approach: Hybrid Companion Model

**Combine Option 1 + Option 3:** Keep tools separate but create tight integration through:

1. **Unified Branding** - "Supervertaler Quickmenu"
2. **Launcher Integration** - Quickmenu launches Supervertaler features
3. **Python CLI Bridge** - Quickmenu calls Supervertaler functions via CLI
4. **Shared Configuration** - Both tools read from shared config files

---

## 📦 Proposed Architecture

```
Supervertaler Ecosystem/
├── Supervertaler_Qt.exe             # Main application (Python/Qt)
├── Supervertaler_Quickmenu.exe      # Companion menu (AutoHotkey)
├── supervertaler_cli.py             # CLI bridge for integration
├── README.md
└── config/
    ├── supervertaler_config.ini     # Main app config
    └── quickmenu_config.ini         # Quickmenu config (shared data)
```

---

## 🔧 Implementation Details

### 1. Rebranding Beijer.bot

**Current structure:**
```autohotkey
MenuPopup.Add("Beijer.bot (click to edit)", EditBeijerBot)
MenuPopup.Add("• ChatGPT:", (*) => NOP())
MenuPopup.Add("• Translate (Dutch to English)", TranslateDutchEnglish)
// ... etc
```

**New structure:**
```autohotkey
MenuPopup.Add("Supervertaler Quickmenu v1.0", EditScript)
MenuPopup.Add("Open Supervertaler (Main App)", OpenSupervertaler)
MenuPopup.Add()

MenuPopup.Add("&SUPERVERTALER ACTIONS:", NOP)
MenuPopup.Add("• Quick Translate Selection", Quicktranslate)
MenuPopup.Add("• Universal Lookup", (*) => Send("^!l"))
MenuPopup.Add("• Open PDF Rescue", OpenPDFRescue)
MenuPopup.Add("• Open TMX Editor", OpenTMXEditor)
MenuPopup.Add()

MenuPopup.Add("&AI TRANSLATION:", NOP)
MenuPopup.Add("• Translate (Custom prompt)", TranslateCustom)
MenuPopup.Add("• Translate (NL→EN)", TranslateDutchEnglish)
MenuPopup.Add("• Translate (EN→NL)", TranslateEnglishDutch)
MenuPopup.Add("• Proofread", ProofreadMulti)
MenuPopup.Add("• Rephrase", Rephrase)
MenuPopup.Add()

MenuPopup.Add("&SNIPPET LIBRARY:", NOP)
// ... existing snippets ...

MenuPopup.Add("&SEARCHES:", NOP)
// ... existing searches ...

MenuPopup.Add("&TEXT TOOLS:", NOP)
// ... existing text tools ...
```

---

### 2. Integration Functions (AutoHotkey)

#### Launch Supervertaler Main App
```autohotkey
OpenSupervertaler(*) {
    ; Check if already running
    if WinExist("ahk_exe Supervertaler_Qt.exe") {
        WinActivate
    } else {
        Run "pythonw.exe `"" SupervertalerPath "\Supervertaler_Qt.py`""
    }
}
```

#### Quick Translate via Python Backend
```autohotkey
Quicktranslate(*) {
    ; Copy selected text
    A_Clipboard := ""
    Send "^c"
    if !ClipWait(2) {
        MsgBox "No text selected"
        return
    }
    
    text := A_Clipboard
    
    ; Escape quotes in text
    text := StrReplace(text, '"', '\"')
    
    ; Call Python CLI
    command := 'python "' SupervertalerPath '\supervertaler_cli.py" translate --quick "' text '"'
    
    ; Show progress
    ToolTip "Translating..."
    
    ; Execute and capture output
    result := RunWaitOutput(command)
    
    ToolTip
    
    if (result != "") {
        A_Clipboard := result
        Send "^v"
    } else {
        MsgBox "Translation failed"
    }
}

; Helper function to run command and capture output
RunWaitOutput(command) {
    shell := ComObject("WScript.Shell")
    exec := shell.Exec(A_ComSpec " /c " command)
    return exec.StdOut.ReadAll()
}
```

#### Launch Specific Modules
```autohotkey
OpenPDFRescue(*) {
    Run 'pythonw.exe "' SupervertalerPath '\modules\pdf_rescue_qt.py"'
}

OpenTMXEditor(*) {
    Run 'pythonw.exe "' SupervertalerPath '\modules\tmx_editor_qt.py"'
}

TriggerUniversalLookup(*) {
    ; Activate Supervertaler and send hotkey
    if WinExist("ahk_exe Supervertaler_Qt.exe") {
        WinActivate
        Sleep 100
        Send "^!l"
    } else {
        MsgBox "Supervertaler is not running"
    }
}
```

---

### 3. Python CLI Bridge

Create `supervertaler_cli.py` in Supervertaler project:

```python
#!/usr/bin/env python3
"""
Supervertaler CLI Bridge
Allows external tools (like Quickmenu) to call Supervertaler functions.
"""

import argparse
import sys
from pathlib import Path

# Add Supervertaler to path
sys.path.insert(0, str(Path(__file__).parent))

from supervertaler.core.translator import Translator
from supervertaler.core.config import Config


def quick_translate(text: str, source_lang: str = "auto", target_lang: str = "auto"):
    """
    Quick translation with default settings.
    
    Args:
        text: Text to translate
        source_lang: Source language (auto-detect if "auto")
        target_lang: Target language (auto-detect if "auto")
    
    Returns:
        Translated text
    """
    config = Config.load()
    translator = Translator(config)
    
    # Use default quick translation settings
    result = translator.translate_quick(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang
    )
    
    return result.translation


def main():
    parser = argparse.ArgumentParser(
        description="Supervertaler CLI - Bridge for external tools"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Translate command
    translate_parser = subparsers.add_parser('translate', help='Translate text')
    translate_parser.add_argument('text', help='Text to translate')
    translate_parser.add_argument('--quick', action='store_true', help='Quick translation mode')
    translate_parser.add_argument('--source', default='auto', help='Source language')
    translate_parser.add_argument('--target', default='auto', help='Target language')
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command == 'translate':
        try:
            result = quick_translate(
                text=args.text,
                source_lang=args.source,
                target_lang=args.target
            )
            print(result, end='')  # No newline for easy clipboard pasting
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
```

---

### 4. Shared Configuration

Both tools should be able to read shared configuration:

**quickmenu_config.ini:**
```ini
[Paths]
SupervertalerPath = C:\Dev\Supervertaler
PythonExecutable = pythonw.exe

[Integration]
EnableQuicktranslate = true
EnableModuleLaunchers = true
EnableUniversalLookup = true

[Hotkeys]
Quickmenu = ^+!k
UniversalLookup = ^!l
```

---

## 📋 Quickmenu Features to Keep

### Core Features (Keep as-is)
- ✅ **ChatGPT Integration** - Quick AI translations, proofreading, etc.
- ✅ **Snippet Library** - Boilerplate, dictionaries, prompts, HTML, etc.
- ✅ **Search Functions** - Multi-search, individual search engines
- ✅ **Text Manipulation** - Case conversion, quotes, brackets, etc.
- ✅ **Hotstrings** - Email addresses, special characters, etc.
- ✅ **Personal Data** - Passwords, phone numbers (for personal use)

### New Supervertaler Integration Features
- ➕ **Launch Supervertaler** - Open main app
- ➕ **Quick Translate** - Translate selection via Python backend
- ➕ **Module Launchers** - Open PDF Rescue, TMX Editor, etc.
- ➕ **Universal Lookup Trigger** - Activate Supervertaler's lookup

---

## 🎯 Menu Structure (Proposed)

```
Supervertaler Quickmenu
├─ About / Edit / Settings
├─ Open Supervertaler (Main App)
│
├─ SUPERVERTALER ACTIONS
│  ├─ Quick Translate Selection
│  ├─ Universal Lookup (Ctrl+Alt+L)
│  ├─ Open PDF Rescue
│  ├─ Open TMX Editor
│  └─ Open Termbase Editor
│
├─ AI TRANSLATION (Quick)
│  ├─ Translate (Custom prompt)
│  ├─ Translate (NL→EN)
│  ├─ Translate (EN→NL)
│  ├─ Proofread
│  ├─ Rephrase
│  ├─ Explain
│  ├─ Summarize
│  └─ Expand
│
├─ SNIPPET LIBRARY
│  ├─ Boilerplate
│  ├─ Dictionaries
│  ├─ HTML
│  ├─ Prompts
│  ├─ Special Characters
│  ├─ URLs
│  └─ Regex
│
├─ SEARCHES
│  ├─ Local Searches (Desktop, LogiTerm, GWIT)
│  ├─ Multi-Search (NL→EN / EN→NL)
│  └─ Individual Searches (IATE, Linguee, etc.)
│
├─ TEXT TOOLS
│  ├─ Case Conversion
│  ├─ Quote Conversion
│  ├─ Brackets
│  └─ Text Cleanup
│
└─ PERSONAL (Optional section for user customization)
   ├─ Email Addresses
   ├─ Phone Numbers
   └─ Credentials
```

---

## 🚀 Implementation Phases

### Phase 1: Core Rebranding ✅
**Goal:** Rename and restructure Quickmenu with Supervertaler branding

**Tasks:**
1. Rename script from `Beijer.bot.ahk` to `Supervertaler_Quickmenu.ahk`
2. Update all references (window titles, about text, etc.)
3. Restructure menu with new categories
4. Add Supervertaler integration section (placeholder)
5. Update icon to match Supervertaler branding
6. Create basic documentation

**Deliverables:**
- `Supervertaler_Quickmenu.ahk`
- Updated README
- New icon file

---

### Phase 2: Python CLI Bridge 🔄
**Goal:** Create communication layer between Quickmenu and Supervertaler

**Tasks:**
1. Create `supervertaler_cli.py` with translate command
2. Implement quick translate function in Supervertaler core
3. Add error handling and validation
4. Test CLI from command line
5. Create configuration system for paths

**Deliverables:**
- `supervertaler_cli.py`
- Updated Supervertaler core with quick translate
- Configuration file format
- CLI documentation

---

### Phase 3: Quickmenu Integration ⏳
**Goal:** Connect Quickmenu to Supervertaler via CLI

**Tasks:**
1. Implement `OpenSupervertaler()` function
2. Implement `Quicktranslate()` function
3. Add module launcher functions
4. Add Universal Lookup trigger
5. Create settings UI for paths
6. Test all integration functions

**Deliverables:**
- Working integration functions in Quickmenu
- Settings dialog for configuration
- Integration testing results

---

### Phase 4: Polish & Package ⏳
**Goal:** Professional distribution package

**Tasks:**
1. Compile both executables
2. Create unified installer/package
3. Write comprehensive documentation
4. Add update checking mechanism
5. Create demo video/screenshots
6. Set up GitHub releases

**Deliverables:**
- `Supervertaler_Package.zip`
- Installation instructions
- User guide
- Demo materials

---

## 🔐 Configuration & Settings

### Quickmenu Settings Dialog
Create a settings GUI for users to configure integration:

```autohotkey
ShowSettings(*) {
    SettingsGui := Gui("+Resize", "Supervertaler Quickmenu - Settings")
    
    ; Supervertaler Integration
    SettingsGui.Add("GroupBox", "w400 h150", "Supervertaler Integration")
    SettingsGui.Add("Text", "xp+10 yp+25", "Supervertaler Path:")
    pathEdit := SettingsGui.Add("Edit", "w300", SupervertalerPath)
    SettingsGui.Add("Button", "x+5 w70", "Browse").OnEvent("Click", BrowsePath)
    
    SettingsGui.Add("Text", "x20 y+10", "Python Executable:")
    pythonEdit := SettingsGui.Add("Edit", "w300", PythonExecutable)
    
    SettingsGui.Add("Checkbox", "x20 y+10", "Enable Quick Translate").Value := EnableQuicktranslate
    SettingsGui.Add("Checkbox", "x20 y+5", "Enable Module Launchers").Value := EnableModuleLaunchers
    
    ; Save/Cancel buttons
    SettingsGui.Add("Button", "x20 y+30 w100", "Save").OnEvent("Click", SaveSettings)
    SettingsGui.Add("Button", "x+10 w100", "Cancel").OnEvent("Click", (*) => SettingsGui.Destroy())
    
    SettingsGui.Show()
}
```

---

## 📖 Documentation Plan

### For Users
1. **Quick Start Guide** - Get started in 5 minutes
2. **User Manual** - Complete feature documentation
3. **Integration Guide** - How Quickmenu works with Supervertaler
4. **Hotkey Reference** - All keyboard shortcuts
5. **FAQ** - Common questions

### For Developers
1. **Architecture Overview** - System design
2. **CLI API Documentation** - Python CLI commands
3. **Configuration Reference** - All settings explained
4. **Extension Guide** - Adding custom features
5. **Build Instructions** - Compiling from source

---

## 🎨 Branding Consistency

### Visual Identity
- Use Supervertaler color scheme
- Consistent icon design
- Matching window styles
- Unified about dialogs

### Naming Convention
- Main tool: **Supervertaler**
- Companion: **Supervertaler Quickmenu**
- Shortened: **Quickmenu**
- CLI: **Supervertaler CLI**

### Messaging
- "The Ultimate Translator Toolkit"
- "Supervertaler: Deep translation work"
- "Quickmenu: Instant access anywhere"
- "Better together"

---

## ⚠️ Challenges & Solutions

### Challenge 1: Python Environment
**Problem:** Users might not have Python installed  
**Solution:** Package Python with PyInstaller or use embedded Python

### Challenge 2: Path Configuration
**Problem:** Users need to specify Supervertaler location  
**Solution:** Auto-detect common installation paths, provide setup wizard

### Challenge 3: Process Communication
**Problem:** AHK needs to wait for Python results  
**Solution:** Use proper timeout handling, show loading indicators

### Challenge 4: Two Tools Running
**Problem:** Users need both tools running for full integration  
**Solution:** 
- Quickmenu can auto-start Supervertaler if needed
- Quickmenu works standalone without Supervertaler
- Clear documentation on what requires Supervertaler

---

## 📊 Success Metrics

### User Adoption
- [ ] Users install both tools together
- [ ] 50%+ use at least one integration feature daily
- [ ] Positive feedback on unified experience

### Technical Success
- [ ] Integration functions work reliably (>99% success rate)
- [ ] Quick translate completes in <3 seconds
- [ ] No performance impact on either tool
- [ ] Error handling covers all edge cases

### Community Success
- [ ] Clear documentation helps users get started
- [ ] GitHub discussions show active usage
- [ ] Community creates custom snippets/prompts
- [ ] Positive reviews on forums

---

## 🔮 Future Possibilities

### Phase 5+: Advanced Integration
- **Bidirectional Communication** - Supervertaler can trigger Quickmenu functions
- **Shared Clipboard History** - Recent translations accessible in both tools
- **Synchronized Glossaries** - Quickmenu can insert from Supervertaler termbases
- **Smart Context** - Quickmenu detects active CAT tool and adjusts features
- **Voice Control** - Dragon/Talon integration for both tools
- **Cloud Sync** - Optional cloud sync for snippets and settings
- **Plugin System** - Community-created extensions for Quickmenu

---

## 📝 Next Steps

1. **Review this document** - Ensure alignment on vision and approach
2. **Finalize naming** - Confirm "Supervertaler Quickmenu" as official name
3. **Set up project structure** - Create folders in Supervertaler repo
4. **Start Phase 1** - Begin rebranding work
5. **Create CLI spec** - Define all CLI commands needed
6. **Plan testing strategy** - How to test integration

---

## 📞 Questions to Resolve

- [ ] Should Quickmenu be distributed separately or bundled with Supervertaler?
- [ ] What installation method: Installer vs. Portable zip?
- [ ] Should we create a public GitHub repo for Quickmenu or keep it in Supervertaler repo?
- [ ] What's the minimum Python version to support?
- [ ] Should Quickmenu have auto-update capability?
- [ ] Which features should require Supervertaler running vs. work standalone?

---

**Last Updated:** 2025-01-06  
**Authors:** Michael Beijer  
**Status:** ✅ Planning Complete - Ready for Implementation

