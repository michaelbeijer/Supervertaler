# Supervertaler Dual-Version Strategy

## Overview

Two parallel versions during Qt migration:

### 1. **Supervertaler_v3.7.x.py** (tkinter)
- **Status:** Maintenance mode
- **Purpose:** Stable production version with all features
- **Changes:** Bug fixes only, no new features
- **Current:** v3.7.6 (Grid2 removed)
- **Next:** v3.7.7 (if bug fixes needed)
- **Lifetime:** Until Qt version reaches feature parity (v2.0.0)

### 2. **Supervertaler_Qt_v1.x.py** (PyQt6)
- **Status:** Active development
- **Purpose:** Future production version
- **Changes:** Progressive feature migration + new Qt-exclusive features
- **Current:** v1.0.0 (Core infrastructure)
- **Next:** v1.1.0 (Project management + recent projects)
- **Lifetime:** Ongoing - this is the future

---

## Version Numbering

### tkinter (v3.7.x)
```
Supervertaler_v3.7.6.py  ← Current (Grid2 removed)
Supervertaler_v3.7.7.py  ← Next (if bug fix needed)
Supervertaler_v3.7.8.py  ← Future (if more bug fixes)
```

**When to increment:**
- Critical bugs only
- No new features
- Compatibility fixes

### Qt (v1.x.y)
```
Supervertaler_Qt_v1.0.0.py  ← Current (Phase 1)
Supervertaler_Qt_v1.1.0.py  ← Next (Phase 2a - Project management)
Supervertaler_Qt_v1.2.0.py  ← Future (Phase 2b - Import/Export)
...
Supervertaler_Qt_v2.0.0.py  ← Goal (Feature parity + Qt exclusives)
```

**Versioning scheme:**
- **MAJOR.MINOR.PATCH**
- **MAJOR (1):** Initial Qt version, becomes 2 at feature parity
- **MINOR:** New features added (0→1→2→3...)
- **PATCH:** Bug fixes within same feature set

---

## When to Use Which Version

### Use tkinter v3.7.x when:
- ✅ Need all current features (TM, AI assistant, all import/export formats)
- ✅ Production translation work
- ✅ Tried-and-tested reliability
- ✅ Qt version missing features you need

### Use Qt v1.x when:
- ✅ Want better grid display and auto-sizing
- ✅ Need sharp, crisp fonts
- ✅ Testing new features as they're added
- ✅ Willing to provide feedback
- ✅ Enjoy being on the cutting edge

---

## Files in Repository

```
c:\Dev\Supervertaler\
├── Supervertaler_v3.7.6.py          # tkinter current
├── Supervertaler_Qt_v1.0.0.py       # Qt current
├── qt_grid_demo.py                  # Qt proof of concept (keep for reference)
├── modules\                         # Shared business logic
│   ├── translation_memory.py        # ← Used by BOTH versions
│   ├── docx_handler.py             # ← Used by BOTH versions
│   └── ...                          # ← All other modules
└── docs\
    ├── QT_MIGRATION_PLAN.md         # This migration roadmap
    └── DUAL_VERSION_STRATEGY.md     # This document
```

**Important:** Both versions share the same `modules/` folder!

---

## Development Workflow

### Working on tkinter v3.7.x
1. Open `Supervertaler_v3.7.6.py`
2. Fix bug
3. Save as `Supervertaler_v3.7.7.py`
4. Update version string in code
5. Test
6. Commit

### Working on Qt v1.x
1. Open `Supervertaler_Qt_v1.0.0.py`
2. Add feature
3. Test until working
4. Save as `Supervertaler_Qt_v1.1.0.py`
5. Update version string in code
6. Update `QT_MIGRATION_PLAN.md` (mark feature complete)
7. Commit

---

## Project File Compatibility

**Good news:** Both versions use the same JSON format!

```json
{
  "name": "My Translation",
  "source_lang": "en",
  "target_lang": "nl",
  "segments": [
    {
      "id": 1,
      "source": "Hello",
      "target": "Hallo",
      "status": "translated",
      "type": "para"
    }
  ],
  "created": "2025-10-26T10:00:00",
  "modified": "2025-10-26T11:30:00"
}
```

**This means:**
- Projects created in tkinter work in Qt
- Projects created in Qt work in tkinter
- No conversion needed
- Easy to switch between versions

---

## Migration Timeline

### Short-term (Next 2-4 weeks)
- Keep using tkinter v3.7.6 for production
- Test Qt v1.0.0 with small projects
- Add features to Qt as needed
- Qt catches up gradually

### Medium-term (2-6 months)
- Qt v1.x has most common features
- Start preferring Qt for new projects
- Keep tkinter for complex features
- Qt becomes daily driver

### Long-term (6-12 months)
- Qt v2.0.0 reaches feature parity
- Add Qt-exclusive features (tabs, dark mode, etc.)
- Deprecate tkinter version
- Qt is the one and only

---

## Communication Strategy

### Filename is Self-Documenting

```
Supervertaler_v3.7.6.py          # Clearly tkinter
Supervertaler_Qt_v1.0.0.py       # Clearly Qt
```

**Users instantly know:**
- Which framework
- Which version
- Which is newer

### README Updates

Update main README.md:

```markdown
## Versions

### Supervertaler v3.7.x (tkinter) - Stable
Full-featured translation tool. Recommended for production use.
- File: `Supervertaler_v3.7.6.py`
- Status: Maintenance mode (bug fixes only)
- Features: Complete

### Supervertaler Qt v1.x (PyQt6) - Development
Next-generation version with superior UI. Under active development.
- File: `Supervertaler_Qt_v1.0.0.py`
- Status: Active development
- Features: Growing (see QT_MIGRATION_PLAN.md)

**Note:** Both versions share project files (.json format).
```

---

## Git Branching Strategy (Optional)

If using Git:

```
main
├── Supervertaler_v3.7.6.py           # Stable tkinter
├── Supervertaler_Qt_v1.0.0.py        # Qt development
└── modules/                          # Shared

branches:
├── main                              # Both versions
├── feature/qt-recent-projects        # Qt feature branches
└── hotfix/v3.7.7-encoding-fix        # tkinter hotfixes
```

**Or keep it simple:** Just use main branch with both files side-by-side.

---

## Testing Strategy

### tkinter v3.7.x
- **When:** Before releasing bug fix version
- **What:** Regression testing (ensure fix doesn't break existing features)
- **How:** Load sample projects, test affected feature

### Qt v1.x
- **When:** After adding each new feature
- **What:** Feature testing + basic functionality
- **How:** 
  1. Test new feature works
  2. Test existing features still work
  3. Test project load/save
  4. Test with real translation project

---

## Documentation Strategy

### User Documentation

**For tkinter v3.7.x:**
- Maintain existing docs
- No new feature docs
- Focus on bug fix notes

**For Qt v1.x:**
- Update docs as features are added
- Note which features are "Coming soon"
- Keep changelog in migration plan

### Developer Documentation

- **QT_MIGRATION_PLAN.md** - Roadmap and feature tracking
- **DUAL_VERSION_STRATEGY.md** - This document
- Code comments explaining differences

---

## Deprecation Plan

### When Qt Reaches Feature Parity (v2.0.0)

1. **Announce deprecation** of tkinter version
2. **Mark as legacy** in README
3. **Keep file available** for 6 months
4. **Eventually remove** or move to `legacy/` folder

### Estimated Timeline

```
Now (Oct 2025)
├── tkinter v3.7.x - Active
└── Qt v1.0.x - Development

Q1 2026
├── tkinter v3.7.x - Maintenance
└── Qt v1.5.x - Active

Q3 2026
├── tkinter v3.7.x - Legacy
└── Qt v2.0.x - Active

2027
└── Qt v2.x - Only version
```

---

## Key Principles

1. **No feature removal** - tkinter stays functional
2. **No forced migration** - Users choose when to switch
3. **No breaking changes** - Project files compatible
4. **No rush** - Quality over speed
5. **No duplication** - Modules shared between versions

---

## Success Metrics

### Phase 1 (v1.0-1.2) - Foundation
- ✅ Qt version can load and edit projects
- ✅ Users prefer Qt grid over tkinter
- ✅ Basic workflow functional

### Phase 2 (v1.3-1.6) - Feature Migration
- ⏳ Most common features available in Qt
- ⏳ Qt used for 50% of translation work
- ⏳ Users report fewer issues than tkinter

### Phase 3 (v1.7-1.9) - Near Parity
- ⏳ All essential features in Qt
- ⏳ Qt used for 80% of translation work
- ⏳ Qt has unique features tkinter lacks

### Phase 4 (v2.0+) - Dominance
- ⏳ Complete feature parity achieved
- ⏳ Qt-exclusive features compelling
- ⏳ tkinter deprecated
- ⏳ Qt is the only recommended version

---

## FAQ

**Q: Can I delete the tkinter version once Qt works?**  
A: Keep it until Qt v2.0.0 for safety. Disk space is cheap, peace of mind is priceless.

**Q: Will my project files work in both?**  
A: Yes! Same JSON format, fully compatible.

**Q: Should I fix bugs in both versions?**  
A: No. If it's in tkinter, fix there. If it's in Qt, fix there. They're separate.

**Q: What if Qt development stops?**  
A: tkinter v3.7.x still works perfectly. No risk.

**Q: Can I add a feature to just Qt?**  
A: Absolutely! That's the whole point - make Qt better.

**Q: When should I switch my daily work to Qt?**  
A: When Qt has the features you need most. Start testing with small projects now.

---

## Conclusion

This dual-version strategy:

✅ **Protects your investment** - tkinter stays working  
✅ **Enables progress** - Qt develops freely  
✅ **Reduces risk** - No big-bang migration  
✅ **Maintains compatibility** - Same file formats  
✅ **Provides flexibility** - Use what works best  
✅ **Ensures quality** - No rush, no pressure  

You're not abandoning tkinter - you're building something better alongside it.

---

**Last Updated:** October 26, 2025  
**Next Review:** When Qt v1.1.0 is released
