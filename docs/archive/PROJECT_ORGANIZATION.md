# 🗂️ Project Organization Guide

Quick reference for finding files and features in the Supervertaler project.

## 📁 Directory Structure

```
Supervertaler/
├── 📄 Supervertaler_v3.7.3.py          # Main application (CURRENT VERSION)
├── 📁 modules/                          # Core functionality modules
│   ├── database_manager.py             # SQLite backend (570 lines)
│   ├── translation_memory.py           # TM management
│   ├── prompt_assistant.py             # AI prompt system
│   ├── style_guide_manager.py          # Style guides
│   └── [other modules...]
├── 📁 tests/                            # All test scripts
│   ├── README.md                       # Test documentation
│   ├── test_database.py                # Database tests ✅
│   ├── test_delete_entry.py            # Delete functionality ✅
│   ├── test_google_translate_rest.py   # Google API tests ✅
│   └── [other tests...]
├── 📁 docs/                             # User documentation & website
│   ├── index.html                      # Website (GitHub Pages)
│   ├── DATABASE_IMPLEMENTATION.md      # Technical spec
│   ├── DATABASE_QUICK_REFERENCE.md     # API reference
│   └── guides/                         # User guides
├── 📁 .dev/                             # Development files
│   ├── previous_versions/              # Old version archives
│   │   └── Supervertaler_v3.7.2.py    # Previous version
│   └── development_notes/              # Implementation notes
│       ├── README.md                   # 🎯 FUTURE FEATURES & IDEAS
│       ├── API_CONFIGURATION_COMPLETE.md
│       ├── GOOGLE_TRANSLATE_FIXED.md
│       └── [implementation notes...]
├── 📁 user data/                        # User data (gitignored)
│   ├── Translation_Resources/
│   │   └── supervertaler.db           # 🗄️ MAIN DATABASE
│   └── [other user data...]
└── 📁 user data_private/                # Private data (gitignored)
    └── api_keys.txt                    # API credentials
```

## 🎯 Quick Access

### Current Development
**⭐ Start here for new features:**
- `.dev/development_notes/README.md` - Future features roadmap

### Database
**🗄️ Database location:**
- `user data/Translation_Resources/supervertaler.db`

**📚 Database documentation:**
- `docs/DATABASE_IMPLEMENTATION.md` - Architecture
- `docs/DATABASE_QUICK_REFERENCE.md` - API reference
- `modules/DATABASE_README.md` - User guide

### Testing
**🧪 Test suite:**
- `tests/` - All test scripts
- `tests/README.md` - Test documentation

### Version History
**📦 Previous versions:**
- `.dev/previous_versions/` - Archived versions

## 🚀 Next Features to Implement

**Phase 2: Enhanced TM Management** (Database schema ready!)
1. **Glossary System** - Terminology management
2. **Non-Translatables** - Pattern protection
3. **Segmentation Rules** - Custom sentence breaking
4. **Project Management** - Multi-file projects

**Phase 3: Machine Translation**
- DeepL API integration
- Microsoft Translator
- MT provider selection UI
- Cost tracking

**See `.dev/development_notes/README.md` for full details!**

## 📝 Important Notes

### Database Backend (v3.7.3)
- ✅ SQLite with FTS5 full-text search
- ✅ 10-20x faster than old dictionary system
- ✅ Real similarity scores with SequenceMatcher
- ✅ Usage tracking and context storage
- ✅ Schema prepared for Phase 2 features

### Recent Fixes (v3.7.3)
- ✅ Word-level highlighting in concordance search
- ✅ Delete TM entries (from matches & concordance)
- ✅ Google Cloud Translation REST API working
- ✅ Language code handling (locale → base)

### File Organization
- **Root:** Only essential files (main app, config, docs)
- **Tests:** All test scripts in `tests/` folder
- **Dev Notes:** Implementation details in `.dev/development_notes/`
- **Archives:** Old versions in `.dev/previous_versions/`

## 🔍 Finding Things

**Looking for implementation notes?**
→ `.dev/development_notes/`

**Want to see what tests exist?**
→ `tests/README.md`

**Need to check database schema?**
→ `modules/database_manager.py` (lines 78-180)

**Planning new features?**
→ `.dev/development_notes/README.md`

**Want to see what changed?**
→ `CHANGELOG.md`

**Need API documentation?**
→ `docs/DATABASE_QUICK_REFERENCE.md`

---

**Last Updated:** October 23, 2025 (v3.7.3)  
**Current Focus:** Clean, organized codebase ready for Phase 2
