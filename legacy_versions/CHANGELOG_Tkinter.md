# Supervertaler Tkinter Edition - Changelog

All notable changes to the **Tkinter Edition (Classic)** of Supervertaler are documented in this file.

The Tkinter Edition is the **legacy version** in maintenance mode. Primary development continues in the [Qt Edition](../CHANGELOG.md).

---

## [2.5.0] - October 30, 2025

### Status
- **Maintenance Mode** - No new features planned
- **Support** - Critical bug fixes only
- **Migration Path** - Features being ported to Qt Edition (primary)

### Key Features
- Stable DOCX-based translation workflow
- Full Translation Memory support with fuzzy matching
- Termbases with multi-language support
- AI integration (OpenAI, Claude, local LLMs)
- AutoHotkey system integration
- Complete CAT functionality for professional translation

---

## Version History

### Previous Stable Releases
- **v3.7.7** (October 27, 2025) - Last active development release
- **v3.7.6** (September 2025) - Stability improvements
- **v3.1.1** - Beta CAT Editor (experimental)
- **v2.5.0** - Tkinter base edition

---

## Maintenance Policy

### Critical Issues
- Will be fixed immediately
- Must affect core functionality (TM, project loading, data integrity)

### Feature Requests
- Not accepted - development continues in Qt Edition
- Users encouraged to migrate to Qt Edition for new features

### Deprecation Timeline
- **v2.5.x** (Current) - Full support in maintenance mode
- **v3.0.0** (Future) - Deprecation notice
- **v4.0.0** (Later) - Removal from distribution

---

## Migration to Qt Edition

Users of the Tkinter Edition are encouraged to migrate to the Qt Edition (v1.0+) which offers:
- Modern PyQt6 interface
- Enhanced performance
- New features under active development
- Better AI integration
- Easier customization

**Migration Path:** Data (projects, TM, termbases) is compatible with Qt Edition.

---

**Note:** This changelog focuses on the Tkinter Edition (legacy). See [CHANGELOG.md](../CHANGELOG.md) for the primary Qt Edition.

**Last Updated:** October 30, 2025

### Key Features (Complete List)
- ✅ **DOCX Editing** - Native Microsoft Word document editing
- ✅ **AI Translation** - Multiple LLM provider integration
- ✅ **Glossaries** - Terminology management system
- ✅ **Translation Memory** - TMX-based TM with search
- ✅ **AutoHotkey Integration** - System-wide lookup hotkeys
- ✅ **Segmentation** - Professional sentence segmentation
- ✅ **Diff Highlighting** - Visual translation comparison
- ✅ **Batch Processing** - Process multiple documents
- ✅ **Project Management** - Organize translation projects
- ✅ **CAT-like Interface** - Professional UI for translators

### Modules Included
- `cafetran_docx_handler.py` - DOCX file processing
- `autofingers_engine.py` - Auto-completion engine
- `database_manager.py` - SQLite backend
- `universal_lookup.py` - Dictionary integration
- `config_manager.py` - Configuration management

---

## [v3.7.6] - 2025-10-15 📄 DOCX Stability

### Improvements
- ✅ Enhanced DOCX reading reliability
- ✅ Improved table detection and parsing
- ✅ Better formatting preservation
- ✅ Fixed encoding issues with various document types

---

## [v3.7.5] - 2025-09-20 🔧 Bug Fixes & Optimization

### Features
- ✅ Improved glossary search performance
- ✅ Enhanced AutoHotkey integration
- ✅ Better error handling in batch mode
- ✅ Optimized database queries

---

## [v3.7.4] - 2025-09-10 🤖 AI Provider Updates

### Enhancements
- ✅ Support for latest OpenAI models (GPT-4 Turbo)
- ✅ Anthropic Claude 3 support
- ✅ Google Gemini integration
- ✅ Improved local LLM support

---

## [v3.7.3] - 2025-08-25 🌍 Multi-Language Support

### Improvements
- ✅ Enhanced language pair detection
- ✅ Improved Unicode support
- ✅ Better RTL language handling
- ✅ Regional character encoding support

---

## [v3.7.2] - 2025-08-10 🎨 UI Polish

### Features
- ✅ Dark mode support
- ✅ Improved theme system
- ✅ Better font handling
- ✅ Enhanced visual styling

---

## [v3.7.1] - 2025-07-15 🔐 Security & Stability

### Improvements
- ✅ API key encryption
- ✅ Improved error handling
- ✅ Better exception reporting
- ✅ Enhanced logging system

---

## [v3.7.0] - 2025-06-20 📊 Project Management

### Features
- ✅ Project save/load system
- ✅ Recent files management
- ✅ Project history tracking
- ✅ Batch processing projects

---

## [v3.6.x] - 2025-05 🔤 Segmentation & TM

### Features (Multiple releases)
- ✅ Professional sentence segmentation
- ✅ TMX format support
- ✅ TM search and matching
- ✅ Match statistics

---

## [v3.5.x] - 2025-04 🤖 AI Integration Foundation

### Foundation
- ✅ Multi-provider LLM support
- ✅ Streaming response handling
- ✅ Custom prompt management
- ✅ Cost tracking

---

## [v3.0.x] - 2024-2025 Core Features

### Major Milestones
- ✅ DOCX editing core
- ✅ AutoHotkey integration
- ✅ Basic AI translation
- ✅ Database backend
- ✅ Professional UI

---

## Migration Path: Tkinter → Qt

The Tkinter edition serves as the **feature reference** for the Qt Edition. As features are implemented in Qt, they will be tested and validated here before being moved to the newer codebase.

**Features Successfully Migrated to Qt**:
- ✅ Project management interface
- ✅ Translation grid layout
- ✅ Universal lookup tool
- ✅ Database infrastructure
- ✅ AI integration

**Planned Features for Qt Migration**:
- ⏳ Termbases (terminology base) - Now implemented in Qt v1.0.1
- ⏳ Advanced TM features
- ⏳ Batch processing
- ⏳ DOCX editing (requires different approach in Qt)

---

## Known Limitations (Maintenance Mode)

- **No New Features** - All new development is in Qt Edition
- **Tkinter Framework Constraints** - Limited to Tkinter's capabilities
- **Python Version Support** - Tested on Python 3.8+
- **DOCX Only** - Focused on Word document workflows

---

## Support & Migration

If you're using Supervertaler Tkinter:
1. **Stay Current** - Receive bug fixes and maintenance updates
2. **Evaluate Qt** - Consider trying the new Qt edition
3. **Report Issues** - Report bugs in both versions
4. **Migrate When Ready** - Qt will have full feature parity eventually

---

## Version Numbering

Supervertaler Tkinter uses semantic versioning:
- **MAJOR** (v3) - Python 3.x era
- **MINOR** - Feature releases and improvements
- **PATCH** - Bug fixes and updates

**Current**: v3.7.7
