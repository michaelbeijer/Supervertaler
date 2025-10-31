# Supervertaler Release Notes

## Current Release: v1.0.2-Qt (October 31, 2025)

### What's New

**UI Improvements & Bug Fixes** ✅
- Fixed broken emoji icons in tab labels (Termbases 🏷️, Prompt Manager 💡, Encoding Repair 🔧, Tracked Changes 🔄)
- Improved checkbox styling with custom green checkboxes and white checkmarks
- Better small-screen support with reorganized AutoFingers layout
- Activity Log moved to right side for improved space utilization

**Previous Release (v1.0.1): Termbases Feature Complete** ✅
- Full termbase CRUD operations (Create, Read, Update, Delete)
- Multiple termbases per project with independent term sets
- Global and project-specific termbase scopes
- Sample data with 3 test termbases (48 terms total)

**Terminology Standardization**
- All references standardized to "Termbase" (single word)
- Consistent terminology throughout UI and codebase
- Eliminated ambiguity between "glossary" vs "termbase"

### Key Improvements

- **UI Polish:** Custom checkbox styling for better visual feedback
- **Layout:** 2-column grid layout for AutoFingers Settings section
- **Responsive Design:** Improved rendering on smaller laptop displays
- **Database:** Fixed NOT NULL constraint errors on language fields (v1.0.1)
- **Code Quality:** Fixed method naming and Project object access patterns

### System Requirements

- **Python:** 3.8+
- **OS:** Windows, macOS, Linux
- **GUI Framework:** PyQt6
- **Database:** SQLite (built-in)

---

## Known Issues

- None reported for v1.0.2

---

## Deprecated Features

- **Tkinter Edition:** Now in maintenance mode. Features being ported to Qt Edition.

---

## Breaking Changes

None in this release.

---

## Upgrading

### From v1.0.1 to v1.0.2

No database migration required. Simply install the new version:

### From v1.0.0 to v1.0.1

No database migration required. Simply install the new version:

```bash
python Supervertaler_Qt.py
```

---

## Support

For questions or bug reports, see [PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) for development team information.

---

## Future Releases

### v1.1.0 (Planned)
- Terminology Search (Ctrl+P)
- Concordance Search (Ctrl+K)
- Enhanced create/edit dialogs

### v1.2.0 (Planned)
- TMX Editor with visual highlighting
- Advanced filtering
- Custom keyboard shortcuts

### v2.0.0 (Future)
- Full feature parity with Tkinter edition
- Tkinter deprecation

---

**Documentation:** See [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) for complete project information.

**Last Updated:** October 31, 2025
