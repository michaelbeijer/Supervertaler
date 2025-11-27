# Instructions for AI Agents

## Project Context File

**Location:** `C:\Dev\Supervertaler\PROJECT_CONTEXT.md` (repository root)

This file contains the complete project history, architecture decisions, and recent development activity. 

### Update Requirements

**Please update PROJECT_CONTEXT.md regularly during development sessions:**

1. **At the end of each session** - Add a summary of what was accomplished
2. **After major features** - Document new functionality, files changed, design decisions
3. **After bug fixes** - Note the issue and solution for future reference

### What to Include

- Date and version number
- Features added or modified
- Files created/changed
- Technical decisions and rationale
- Known issues or TODOs

This helps other AI agents (and human developers) understand the project state and recent changes.

---

## Quick Reference

- **Current Version:** Check `__version__` in `Supervertaler.py`
- **Changelog:** `CHANGELOG.md` in repository root
- **Main Application:** `Supervertaler.py` (~25,000+ lines)
- **Modules:** `modules/` directory (50+ specialized modules)
- **User Data:** `user_data/` (prompts, termbases, TMs)
