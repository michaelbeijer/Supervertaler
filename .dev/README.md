# .dev/ - Development & Internal Documentation

This folder contains development resources, build files, and internal documentation that are not essential for end users.

---

## 📂 Folder Structure

### `scripts/`
**Development utility scripts**

One-off scripts created during development for:
- Feature implementation (`add_*.py`, `implement_*.py`)
- Code refactoring (`reorganize_*.py`, `port_*.py`)
- Bug fixes (`fix_*.py`, `enhance_*.py`)
- Format updates (`update_*.py`, `replace_*.py`)
- Version management (`bump_*.py`)
- Verification (`verify_*.py`)

These scripts are kept for reference but are not part of the main application.

**Note**: New development scripts should be created in this folder to keep root clean.

---

### `build/`
**Build and release automation**

Contains scripts and configuration files for building Windows executables:
- `build_release.ps1` - PowerShell script to build release packages
- `post_build.py` - Post-build processing script
- `Supervertaler.spec` - PyInstaller configuration
- `BUILD_REQUIREMENTS.md` - Build dependencies and requirements
- `BUILD_COMPLETE_SUMMARY.md` - Build process documentation

**For**: Contributors who want to create executable releases

---

### `docs/`
**Development documentation and history**

Comprehensive documentation of the development process, including:

#### `docs/features/`
- Detailed feature guides (CafeTran support, memoQ support, etc.)
- Implementation specifications
- Feature design documents

#### `docs/user_guides/`
- System prompts guide
- Translation memory guide
- Workspace redesign documentation
- Installation guides for Linux/macOS

#### `docs/implementation/`
- Technical implementation details
- Architecture decisions
- Integration guides

#### `docs/planning/`
- Feature planning documents
- Roadmap discussions
- Design proposals

#### `docs/session_summaries/`
- Development session logs
- Progress tracking
- Decision history

#### `docs/bugfixes/`
- Bug fix documentation
- Issue resolution notes

#### `docs/archive/`
- Historical documentation
- Abandoned features
- Legacy documentation

**For**: Contributors, developers, maintainers

---

### `previous_versions/`
**Archived application versions**

Contains older versions of Supervertaler for reference:
- Previous stable releases
- Archived experimental versions
- Version history preservation

**For**: Reference, rollback, version comparison

---

### `tests/`
**Unit tests and test infrastructure**

Contains test files and testing infrastructure:
- Unit tests
- Integration tests
- Test utilities

**For**: Contributors running tests or adding new test coverage

---

## 🎯 For End Users

**You don't need anything in this folder to use Supervertaler!**

Everything you need is in the main repository root:
- `README.md` - Project overview
- `USER_GUIDE.md` - How to use Supervertaler
- `INSTALLATION.md` - Installation instructions
- `CHANGELOG.md` - Version history
- `Supervertaler_v*.py` - The applications themselves

---

## 👥 For Contributors

If you're contributing to Supervertaler development, this folder contains:
- **Build tools** to create release packages
- **Development docs** explaining implementation decisions
- **Session logs** showing how features were developed
- **Test suite** for validation
- **Previous versions** for comparison

Browse the folders above to find what you need!

---

## 📋 Quick Links

- **Want to build an executable?** → See `build/BUILD_REQUIREMENTS.md`
- **Want to understand a feature?** → See `docs/features/`
- **Want implementation details?** → See `docs/implementation/`
- **Want development history?** → See `docs/session_summaries/`
- **Want to run tests?** → See `tests/`

---

**Last updated**: October 10, 2025
