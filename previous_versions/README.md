# Previous Versions Archive

This folder contains archived versions of Supervertaler for rollback or reference purposes.

## Structure

```
previous_versions/
├─ qt/
│   └─ Supervertaler_Qt_v1.0.0.py (archived when v1.1.0 released)
└─ tkinter/
    └─ Supervertaler_tkinter_v3.7.7.py (archived when v3.7.8 released)
```

## Current Versions (Always Latest)

The main files in the root directory are always the latest stable releases:
- `Supervertaler_Qt.py` - Latest Qt edition
- `Supervertaler_tkinter.py` - Latest tkinter edition

## How Versions Are Archived

When a new version is released:
1. Current main file is copied to this archive with version number in filename
2. Main file is updated with new version
3. Version history is preserved

## Finding a Specific Version

- Check CHANGELOG.md for version history
- Look in the appropriate subfolder (qt/ or tkinter/)
- Version number is in the filename

## Rollback

To use a previous version:
1. Copy the desired version from this archive to your working directory
2. Or replace the main file temporarily

---

*Note: Only stable releases are archived. Development versions are tracked in git history.*
