# Supervertaler CLI Bridge - Technical Specification

**Purpose:** Define the command-line interface that allows external tools (like QuickMenu) to interact with Supervertaler.

---

## 📋 Overview

The CLI Bridge enables:
- External tools to call Supervertaler functions
- Command-line usage for automation
- Integration with AutoHotkey, PowerShell, Bash, etc.
- Quick operations without opening the GUI

**File Location:** `C:\Dev\Supervertaler\supervertaler_cli.py`

---

## 🎯 Design Principles

1. **Simple Interface** - Easy to call from any tool
2. **Fast Execution** - Return results quickly
3. **Clear Output** - Predictable, parseable responses
4. **Error Handling** - Graceful failures with helpful messages
5. **Stateless** - Each call is independent
6. **Backward Compatible** - Future-proof API design

---

## 🔧 Command Structure

### General Format
```bash
python supervertaler_cli.py [command] [arguments] [options]
```

### Exit Codes
- `0` - Success
- `1` - General error
- `2` - Invalid arguments
- `3` - Configuration error
- `4` - API error (e.g., OpenAI failure)

---

## 📖 Commands

### 1. `translate` - Translate Text

Translate text using Supervertaler's translation engine.

#### Syntax
```bash
python supervertaler_cli.py translate [text] [options]
```

#### Arguments
- `text` (required) - Text to translate

#### Options
- `--source LANG` - Source language (default: auto-detect)
- `--target LANG` - Target language (default: auto-detect)
- `--prompt NAME` - Use specific prompt (default: none)
- `--quick` - Use quick translation mode (fast, basic context)
- `--model MODEL` - Specify AI model (gpt-4, claude-3-5-sonnet, etc.)
- `--output FORMAT` - Output format: text (default), json

#### Examples
```bash
# Quick translation (auto-detect languages)
python supervertaler_cli.py translate "Hello world" --quick

# Translate with specific languages
python supervertaler_cli.py translate "Hello world" --source en --target nl

# Translate with custom prompt
python supervertaler_cli.py translate "Legal text here" --prompt legal-nl-en

# JSON output for programmatic use
python supervertaler_cli.py translate "Hello" --output json
```

#### Output (text format)
```
Translated text goes here
```

#### Output (json format)
```json
{
  "source_text": "Hello world",
  "translated_text": "Hallo wereld",
  "source_lang": "en",
  "target_lang": "nl",
  "model": "gpt-4o-mini",
  "tokens_used": 42,
  "time_seconds": 1.23
}
```

---

### 2. `lookup` - Dictionary Lookup

Query Supervertaler's termbase and translation memory.

#### Syntax
```bash
python supervertaler_cli.py lookup [term] [options]
```

#### Arguments
- `term` (required) - Term to look up

#### Options
- `--source LANG` - Source language
- `--target LANG` - Target language
- `--tb PATH` - Specific termbase file
- `--tm PATH` - Specific TM file
- `--output FORMAT` - Output format: text (default), json

#### Examples
```bash
# Look up term in all sources
python supervertaler_cli.py lookup "patent"

# Look up in specific direction
python supervertaler_cli.py lookup "octrooi" --source nl --target en

# JSON output
python supervertaler_cli.py lookup "patent" --output json
```

#### Output (text format)
```
patent (EN → NL):
  [TB] octrooi (n) - patent
  [TM] octrooirecht - patent law (95% match)
  [TM] octrooiaanvraag - patent application (87% match)
```

#### Output (json format)
```json
{
  "term": "patent",
  "matches": [
    {
      "source": "termbase",
      "source_term": "patent",
      "target_term": "octrooi",
      "pos": "noun",
      "note": ""
    },
    {
      "source": "tm",
      "source_text": "patent law",
      "target_text": "octrooirecht",
      "similarity": 0.95
    }
  ]
}
```

---

### 3. `proofread` - Proofread Text

Check text for errors and suggest corrections.

#### Syntax
```bash
python supervertaler_cli.py proofread [text] [options]
```

#### Arguments
- `text` (required) - Text to proofread

#### Options
- `--lang LANG` - Language (default: auto-detect)
- `--style STYLE` - Style guide to use (formal, casual, technical)
- `--output FORMAT` - Output format: text (default), json

#### Examples
```bash
# Basic proofreading
python supervertaler_cli.py proofread "This is a textt with errrors"

# With specific language and style
python supervertaler_cli.py proofread "Tekst met fouten" --lang nl --style formal
```

---

### 4. `rephrase` - Rephrase Text

Generate alternative phrasings.

#### Syntax
```bash
python supervertaler_cli.py rephrase [text] [options]
```

#### Arguments
- `text` (required) - Text to rephrase

#### Options
- `--lang LANG` - Language (default: auto-detect)
- `--count N` - Number of alternatives (default: 3, max: 10)
- `--style STYLE` - Target style (formal, casual, concise, elaborate)
- `--output FORMAT` - Output format: text (default), json

#### Examples
```bash
# Generate 3 alternatives
python supervertaler_cli.py rephrase "This is a sentence"

# Generate 5 formal alternatives
python supervertaler_cli.py rephrase "Hey there" --count 5 --style formal
```

---

### 5. `explain` - Explain Text

Get explanations for text, terms, or concepts.

#### Syntax
```bash
python supervertaler_cli.py explain [text] [options]
```

#### Arguments
- `text` (required) - Text to explain

#### Options
- `--lang LANG` - Explanation language (default: auto-detect)
- `--depth LEVEL` - Detail level: basic, detailed, expert (default: detailed)
- `--output FORMAT` - Output format: text (default), json

#### Examples
```bash
# Basic explanation
python supervertaler_cli.py explain "quantum entanglement"

# Detailed technical explanation
python supervertaler_cli.py explain "REST API" --depth expert
```

---

### 6. `config` - Manage Configuration

View or modify CLI configuration.

#### Syntax
```bash
python supervertaler_cli.py config [action] [options]
```

#### Actions
- `show` - Display current configuration
- `set KEY VALUE` - Set configuration value
- `reset` - Reset to defaults

#### Examples
```bash
# Show current config
python supervertaler_cli.py config show

# Set default model
python supervertaler_cli.py config set default_model gpt-4o

# Reset to defaults
python supervertaler_cli.py config reset
```

---

### 7. `version` - Version Information

Display version and system information.

#### Syntax
```bash
python supervertaler_cli.py version
```

#### Output
```
Supervertaler CLI v1.0.0
Python: 3.12.1
Platform: Windows-10-10.0.26200
Supervertaler Core: 1.2.1
API Keys: OpenAI ✓, Claude ✓, Gemini ✗
```

---

## 🏗️ Implementation Details

### File Structure
```
C:\Dev\Supervertaler\
├── supervertaler_cli.py          # Main CLI entry point
├── supervertaler/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── commands.py            # Command implementations
│   │   ├── translator.py          # Translation logic
│   │   ├── output.py              # Output formatting
│   │   └── config.py              # CLI configuration
│   └── core/
│       └── ...                    # Existing core modules
```

### Python Code Structure

#### Main Entry Point (`supervertaler_cli.py`)
```python
#!/usr/bin/env python3
"""
Supervertaler CLI Bridge
Command-line interface for Supervertaler functionality.
"""

import sys
import argparse
from pathlib import Path

# Add Supervertaler to path
sys.path.insert(0, str(Path(__file__).parent))

from supervertaler.cli import commands


def main():
    parser = argparse.ArgumentParser(
        prog='supervertaler',
        description='Supervertaler CLI - AI-powered translation tools'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Register all commands
    commands.register_translate(subparsers)
    commands.register_lookup(subparsers)
    commands.register_proofread(subparsers)
    commands.register_rephrase(subparsers)
    commands.register_explain(subparsers)
    commands.register_config(subparsers)
    commands.register_version(subparsers)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command:
        try:
            result = commands.execute(args.command, args)
            sys.exit(result)
        except KeyboardInterrupt:
            print("\nInterrupted by user", file=sys.stderr)
            sys.exit(130)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main()
```

#### Command Implementation (`supervertaler/cli/commands.py`)
```python
"""CLI Command Implementations"""

import sys
import json
from typing import Any, Dict

from ..core.translator import Translator
from ..core.config import Config
from .output import format_output, OutputFormat


def register_translate(subparsers):
    """Register translate command"""
    parser = subparsers.add_parser('translate', help='Translate text')
    parser.add_argument('text', help='Text to translate')
    parser.add_argument('--source', default='auto', help='Source language')
    parser.add_argument('--target', default='auto', help='Target language')
    parser.add_argument('--prompt', help='Custom prompt name')
    parser.add_argument('--quick', action='store_true', help='Quick mode')
    parser.add_argument('--model', help='AI model to use')
    parser.add_argument('--output', choices=['text', 'json'], default='text')


def execute_translate(args) -> int:
    """Execute translate command"""
    try:
        config = Config.load()
        translator = Translator(config)
        
        # Configure model
        if args.model:
            translator.set_model(args.model)
        
        # Translate
        result = translator.translate(
            text=args.text,
            source_lang=args.source,
            target_lang=args.target,
            prompt=args.prompt,
            quick_mode=args.quick
        )
        
        # Format output
        if args.output == 'json':
            output = {
                'source_text': args.text,
                'translated_text': result.translation,
                'source_lang': result.source_lang,
                'target_lang': result.target_lang,
                'model': result.model_used,
                'tokens_used': result.tokens,
                'time_seconds': result.time_seconds
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            # Text output (no newline for easy clipboard)
            print(result.translation, end='')
        
        return 0
        
    except Exception as e:
        print(f"Translation failed: {e}", file=sys.stderr)
        return 4


def execute(command: str, args) -> int:
    """Execute command and return exit code"""
    commands = {
        'translate': execute_translate,
        'lookup': execute_lookup,
        'proofread': execute_proofread,
        'rephrase': execute_rephrase,
        'explain': execute_explain,
        'config': execute_config,
        'version': execute_version,
    }
    
    if command in commands:
        return commands[command](args)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        return 2
```

---

## 🔒 Security Considerations

### API Key Handling
- ❌ **Never** pass API keys as command-line arguments
- ✅ Read from config file or environment variables
- ✅ Use same config as main Supervertaler app

### Input Validation
- ✅ Sanitize all user input
- ✅ Limit text length to prevent abuse
- ✅ Validate language codes
- ✅ Check file paths for directory traversal

### Error Messages
- ✅ Don't expose sensitive information in errors
- ✅ Provide helpful but not revealing messages
- ✅ Log detailed errors separately (not to stdout)

---

## ⚡ Performance Optimization

### Fast Startup
```python
# Use lazy imports for speed
def execute_translate(args):
    from ..core.translator import Translator  # Import only when needed
    # ... rest of function
```

### Caching
- Cache frequently used data (glossaries, prompts)
- Reuse AI models when possible
- Cache configuration

### Timeout Handling
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

# Set timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout
```

---

## 🧪 Testing Strategy

### Unit Tests
```python
def test_translate_basic():
    """Test basic translation"""
    result = execute_translate(MockArgs(
        text="Hello",
        source="en",
        target="nl",
        quick=True,
        output="text"
    ))
    assert result == 0


def test_translate_invalid_lang():
    """Test with invalid language code"""
    result = execute_translate(MockArgs(
        text="Hello",
        source="invalid",
        target="nl"
    ))
    assert result != 0
```

### Integration Tests
```bash
# Test actual CLI execution
python supervertaler_cli.py translate "Hello" --quick
# Should output Dutch translation

python supervertaler_cli.py translate "Invalid" --source xx
# Should exit with error code

python supervertaler_cli.py version
# Should show version info
```

---

## 📝 Configuration File

### Location
- Windows: `%APPDATA%\Supervertaler\cli_config.ini`
- Linux/Mac: `~/.config/supervertaler/cli_config.ini`

### Format
```ini
[CLI]
default_model = gpt-4o-mini
quick_mode_model = gpt-4o-mini
timeout_seconds = 30
max_text_length = 10000

[Output]
default_format = text
json_indent = 2
color_output = true

[Translation]
auto_detect_threshold = 0.8
default_source_lang = auto
default_target_lang = auto
```

---

## 🔄 AutoHotkey Integration Examples

### Basic Translation
```autohotkey
QuickTranslate(*) {
    ; Get selected text
    A_Clipboard := ""
    Send "^c"
    if !ClipWait(2)
        return
    
    text := A_Clipboard
    text := StrReplace(text, '"', '\"')  ; Escape quotes
    
    ; Call CLI
    command := 'python "' SupervertalerPath '\supervertaler_cli.py" translate "' text '" --quick'
    
    ; Execute and get output
    shell := ComObject("WScript.Shell")
    exec := shell.Exec(A_ComSpec " /c " command)
    result := exec.StdOut.ReadAll()
    
    ; Paste result
    if (result != "") {
        A_Clipboard := result
        Send "^v"
    }
}
```

### With Error Handling
```autohotkey
QuickTranslate(*) {
    A_Clipboard := ""
    Send "^c"
    if !ClipWait(2) {
        ToolTip "No text selected"
        SetTimer () => ToolTip(), -2000
        return
    }
    
    text := A_Clipboard
    text := StrReplace(text, '"', '\"')
    
    command := 'python "' SupervertalerPath '\supervertaler_cli.py" translate "' text '" --quick'
    
    ToolTip "Translating..."
    
    shell := ComObject("WScript.Shell")
    exec := shell.Exec(A_ComSpec " /c " command)
    
    ; Wait for completion (with timeout)
    timeout := 30000  ; 30 seconds
    start := A_TickCount
    while (!exec.Status && (A_TickCount - start < timeout))
        Sleep 100
    
    ToolTip
    
    if (!exec.Status) {
        MsgBox "Translation timed out"
        return
    }
    
    exitCode := exec.ExitCode
    
    if (exitCode == 0) {
        result := exec.StdOut.ReadAll()
        A_Clipboard := result
        Send "^v"
    } else {
        error := exec.StdErr.ReadAll()
        MsgBox "Translation failed:`n`n" error
    }
}
```

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Batch processing mode
- [ ] Interactive mode (REPL)
- [ ] Streaming output for long translations
- [ ] WebSocket server mode for persistent connection
- [ ] Plugin system for custom commands
- [ ] Shell completion scripts (bash, zsh, PowerShell)

### API Versioning
```bash
# Version in command
python supervertaler_cli.py --api-version 2 translate "text"

# Or environment variable
export SUPERVERTALER_API_VERSION=2
```

---

## 📖 Documentation

### Help System
```bash
# General help
python supervertaler_cli.py --help

# Command-specific help
python supervertaler_cli.py translate --help

# Show examples
python supervertaler_cli.py translate --examples
```

### Man Page (Linux/Mac)
Create `supervertaler.1` man page for Unix systems.

---

**Last Updated:** 2025-01-06  
**Status:** ✅ Specification Complete - Ready for Implementation  
**Version:** 1.0.0

