# Test Suite

This folder contains test scripts for validating Supervertaler functionality.

## Database Tests

**test_database.py**
- Comprehensive database backend testing
- Tests FTS5 full-text search
- Validates fuzzy matching with SequenceMatcher
- Checks hash-based exact matching
- All tests passing ✅

**test_current_database.py**
- Tests current database state
- Validates schema integrity
- Checks data consistency

**test_delete_entry.py**
- Tests TMDatabase.delete_entry() method
- Validates proper delegation to DatabaseManager
- Checks deletion from both main table and FTS5 index
- All tests passing ✅

**test_tm_metadata.py**
- Tests TM metadata handling
- Validates tm_id and name associations

**test_tm_methods.py**
- Tests TM-specific methods
- Validates entry addition and retrieval

**test_fts5_special_chars.py**
- Tests FTS5 handling of special characters
- Validates query escaping
- All tests passing ✅

## API Tests

**test_google_translate_rest.py**
- Tests Google Cloud Translation REST API
- Validates API key handling
- Tests translation requests
- All tests passing ✅

**test_google_translate_locale.py**
- Tests language code conversion
- Validates locale handling (en-US → en)
- All tests passing ✅

**test_google_translate.py**
- Legacy Google Translate API tests
- Now superseded by REST implementation

**test_api_keys.py**
- Tests API key loading
- Validates configuration file parsing

**test_mt_apis.py**
- Tests multiple MT API integrations
- Validates provider selection

**test_lang_codes.py**
- Tests language code utilities
- Validates conversions and lookups

## Debug Scripts

**debug_fts5.py**
- Debug script for FTS5 query testing
- Used during special character fix implementation

## Running Tests

Run all tests:
```powershell
Get-ChildItem -Filter "test_*.py" | ForEach-Object { python $_.Name }
```

Run specific test:
```powershell
python test_database.py
```

## Test Results (v3.7.3)

All critical tests passing:
- ✅ Database operations (CRUD)
- ✅ FTS5 full-text search
- ✅ Fuzzy matching with similarity scores
- ✅ Delete TM entries
- ✅ Google Translate REST API
- ✅ Language code handling

## Notes

- Tests use in-memory SQLite databases (`:memory:`)
- No permanent data modifications
- Safe to run multiple times
- Add new tests here as features are implemented

---

**Last Updated:** October 23, 2025 (v3.7.3)
