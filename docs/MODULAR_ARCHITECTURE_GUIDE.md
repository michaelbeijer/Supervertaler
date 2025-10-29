# Supervertaler Modular Architecture Guide

## Purpose

This guide documents the modular architecture pattern used in Supervertaler to keep the codebase maintainable and AI-agent friendly.

## Core Principles

### 1. File Size Management
- **Individual files should stay under 3000 lines** to work well with AI coding agents
- When files grow too large, extract functionality into specialized modules
- Keep main application files focused on UI and orchestration

### 2. Specialized Independent Modules
- Modules in `modules/` folder should be:
  - **Self-contained**: Can work independently
  - **Single-purpose**: Each module handles one specific domain
  - **Standalone-runnable**: Include `if __name__ == "__main__"` examples
  - **Well-documented**: Clear docstrings and usage examples

### 3. Clear Separation of Concerns
- **Main Application**: UI, user interaction, project management
- **Modules**: Business logic, API clients, data processing
- **Shared Types**: Common data structures (Project, Segment, etc.)

## Module Guidelines

### Creating a New Module

1. **Choose the right location**:
   - `modules/` - For general-purpose utilities
   - Should be importable: `from modules.module_name import Class`

2. **Module Structure**:
```python
"""
Module Name
===========

Brief description of what this module does.

Supported Features:
- Feature 1
- Feature 2

Usage:
    from modules.module_name import MainClass
    
    instance = MainClass(param1, param2)
    result = instance.do_something()
"""

# Imports
from typing import ...

# Type definitions
@dataclass
class Config:
    """Configuration for this module"""
    pass

# Main class
class MainClass:
    """Main functionality"""
    
    def __init__(self, ...):
        """Initialize with clear parameters"""
        pass
    
    def public_method(self):
        """Public API - well documented"""
        pass
    
    def _private_method(self):
        """Internal implementation"""
        pass

# Standalone usage
def main():
    """Example showing how to use this module independently"""
    import sys
    # Demonstrate usage
    pass

if __name__ == "__main__":
    main()
```

3. **Documentation Requirements**:
   - Module-level docstring explaining purpose
   - Usage examples in docstring
   - Type hints for all public methods
   - Clear parameter descriptions

### Example: LLM Clients Module

The `modules/llm_clients.py` is a reference implementation:

**✅ Good Practices Demonstrated**:
- Self-contained: All LLM logic in one place
- Independent: Can be imported or run standalone
- Type-safe: Uses dataclasses and type hints
- Documented: Clear docstrings and usage examples
- Configurable: Easy to extend with new providers
- Tested: Includes standalone test mode

**Usage in Main Application**:
```python
# Import the module
from modules.llm_clients import LLMClient

# Use it
client = LLMClient(api_key=key, provider='openai')
result = client.translate(text, source_lang='en', target_lang='nl')
```

**Standalone Usage**:
```bash
python modules/llm_clients.py openai sk-key... "Hello world"
```

## Current Modules

### modules/llm_clients.py
**Purpose**: Universal LLM client for translation
**Providers**: OpenAI, Claude, Gemini
**Features**:
- Automatic temperature detection (1.0 for reasoning models, 0.3 for standard)
- Multi-provider support
- Translation-optimized prompts
- Standalone testing capability

### modules/config_manager.py
**Purpose**: Configuration and settings management
**Features**: API key loading, user preferences

### modules/style_guide_manager.py
**Purpose**: Style guide integration for translations
**Features**: Load and apply style guides to translations

### modules/translation_memory.py
**Purpose**: Translation Memory (TM) system
**Features**: SQLite-based TM, fuzzy matching, concordance

## Refactoring Checklist

When extracting code into a module:

- [ ] Identify self-contained functionality
- [ ] Create new module file in `modules/`
- [ ] Add comprehensive docstring
- [ ] Implement class/functions with type hints
- [ ] Add `main()` function for standalone usage
- [ ] Test standalone functionality
- [ ] Update main application to import and use module
- [ ] Test integration in main application
- [ ] Document in this guide

## Integration Pattern

### Before Refactoring
```python
class MainApp:
    def translate_segment(self):
        # 50+ lines of LLM API code here
        client = OpenAI(api_key=...)
        response = client.chat.completions.create(...)
        # Temperature handling
        # Error handling
        # etc.
```

### After Refactoring
```python
class MainApp:
    def translate_segment(self):
        from modules.llm_clients import LLMClient
        
        client = LLMClient(api_key=key, provider='openai')
        result = client.translate(text, source_lang, target_lang)
```

**Benefits**:
- Main file stays focused and readable
- LLM logic can be tested independently
- Other applications can use the same module
- AI agents can understand both files easily

## Future Modules to Create

### Planned Extractions

1. **modules/document_processors.py**
   - DOCX processing logic
   - MQXLIFF handling
   - Import/export functionality

2. **modules/segment_analysis.py**
   - Quality checks
   - Consistency verification
   - Statistics calculation

3. **modules/batch_translator.py**
   - Multi-segment translation
   - Progress tracking
   - Chunking logic

4. **modules/prompt_builder.py**
   - System prompt generation
   - Context injection
   - Template management

## Benefits for AI Agents

### Why This Matters

1. **Context Window Management**
   - AI agents have limited context windows
   - Small, focused files fit entirely in context
   - Can understand and modify code accurately

2. **Comprehensibility**
   - Clear module boundaries
   - Single responsibility principle
   - Easy to locate relevant code

3. **Testability**
   - Modules can be tested independently
   - Changes have predictable scope
   - Less risk of breaking unrelated features

4. **Collaboration**
   - Multiple AI agents can work on different modules
   - Human developers can understand structure quickly
   - New features have clear home locations

## Best Practices Summary

### DO ✅
- Keep main files under 3000 lines
- Extract specialized functionality to modules
- Include standalone usage examples
- Use type hints everywhere
- Document thoroughly
- Make modules independently runnable
- Test both standalone and integrated

### DON'T ❌
- Create god classes with all functionality
- Mix UI and business logic
- Skip documentation
- Make modules depend on main app
- Ignore type safety
- Leave unused code in modules

## Versioning

When creating modules for new features:
- Module version should match app version initially
- Document breaking changes in module docstrings
- Keep backward compatibility when possible

---

**Last Updated**: 2025 (Qt v1.0.0 refactoring)
**Maintained By**: Supervertaler Development Team
