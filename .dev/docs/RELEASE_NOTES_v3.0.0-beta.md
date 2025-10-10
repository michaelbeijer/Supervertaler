# Supervertaler v3.0.0-beta - Release Notes

> **📌 Version Note**: This version was previously numbered v2.5.2. The jump to v3.0 reflects a **major architectural change** - a complete rewrite from the original DOCX workflow (v2.x-CLASSIC) to a segment-based CAT editor. See [VERSION_RENUMBERING_v3.0.0.md](VERSION_RENUMBERING_v3.0.0.md) for details.

**Release Date**: October 9, 2025  
**Type**: Major Release (CAT Editor Architecture)  
**Status**: Beta Testing Phase

---

## 🎉 What's New

### ⚡ Grid Pagination System - 10x Performance Boost!

**The Problem**: Loading 355 segments in grid view took 6-7 seconds and could freeze the UI.

**The Solution**: Smart pagination system that loads only what you need.

#### Features:
- **Page size options**: 25, 50, 100, 200, or "All" segments per page
- **Navigation controls**:
  - ⏮ First Page
  - ◀ Previous Page
  - Page number input (jump to any page)
  - Next Page ▶
  - Last Page ⏭
- **Real-time status**: "Segments 1-50 of 355"
- **Dynamic page selector**: Choose how many segments to view

#### Benefits:
- ✅ **10x faster**: Grid view loads in ~0.5 seconds instead of 6-7 seconds
- ✅ **No more freezing**: Eliminates UI freeze when switching views
- ✅ **Professional behavior**: Works like memoQ, Trados, and other CAT tools
- ✅ **Works with filters**: Filtered segments are also paginated

---

### 🧠 Smart Paragraph Detection

**The Problem**: Imported memoQ/CafeTran documents showed every segment as its own paragraph, breaking document flow.

**The Solution**: Intelligent paragraph grouping using smart heuristics.

#### How it works:
1. **Detects headings**: Short, all-caps text without ending punctuation = new paragraph
2. **Groups related sentences**: Sentences under the same heading flow together
3. **Identifies natural breaks**: Previous heading + new heading = paragraph break

#### Benefits:
- ✅ **Proper document structure**: Headings separated from body text
- ✅ **Natural text flow**: Sentences within paragraphs flow with spaces
- ✅ **Maintains hierarchy**: Document structure preserved
- ✅ **Applies automatically**: Works on memoQ and CafeTran imports

#### Example:
**Before** (v2.5.1):
```
HEADING ONE

First sentence.

Second sentence.

Third sentence.
```

**After** (v3.0.0-beta):
```
HEADING ONE

First sentence. Second sentence. Third sentence.
```

---

### 🛡️ Enhanced Loading Protection

**The Problem**: Clicking in the grid while loading could cause window resize/freeze issues.

**The Solution**: Full-screen interaction blocker during loading.

#### Features:
- **Visual overlay**: "Loading page... Please wait." message
- **Complete event blocking**: Prevents all mouse/keyboard input during load
- **Automatic removal**: Overlay disappears when loading completes

#### Benefits:
- ✅ **Prevents crashes**: No more accidental clicks during loading
- ✅ **Clear feedback**: Users know the system is working
- ✅ **Guaranteed safety**: Uses try/finally to ensure cleanup

---

## 📊 Performance Comparison

| Operation | v2.5.1 | v3.0.0-beta | Improvement |
|-----------|--------|-------------|-------------|
| Grid view load (355 segments) | 6-7 sec | 0.5 sec | **10-13x faster** |
| View switching | Freezes | Instant | **∞x better** 😊 |
| Document view formatting | All separate | Smart paragraphs | **Much cleaner** |

---

## 🔄 Upgrade Path

### From v2.5.1 or v2.5.2:
- ✅ **Renumbered**: v2.5.2 is now v3.0.0-beta (reflects major architecture change)
- ✅ **Automatic**: Just run v3.0.0-beta
- ✅ **No breaking changes**: All existing projects work
- ✅ **New imports benefit**: Only newly imported documents get smart paragraph detection
- ℹ️ **Existing projects**: Will use old paragraph structure (each segment = paragraph)

### From v2.4.1-CLASSIC:
- ⚠️ **Different architecture**: v3.0.0-beta is completely rewritten CAT editor
- 💡 **Recommendation**: Keep v2.4.1-CLASSIC for production, test v3.0.0-beta separately

---

## 🐛 Known Issues

None currently reported! 🎉

---

## 📖 Documentation Updates

- ✅ **CHANGELOG.md**: Updated with v3.0.0-beta entry and renumbering explanation
- ✅ **README.md**: Version info updated, v3.0.0-beta highlighted
- ✅ **In-app version**: Updated to v3.0.0-beta in title bar and logs
- ✅ **VERSION_RENUMBERING_v3.0.0.md**: New doc explaining version scheme change

---

## 🙏 Credits

**Development**: Michael Beijer + GitHub Copilot  
**Testing**: Michael Beijer  
**Feedback**: Real-world translation workflow requirements

---

## 📬 Feedback

This is a **beta release**. Please report:
- 🐛 Bugs or unexpected behavior
- 💡 Feature requests
- 📊 Performance observations
- 🎨 UX suggestions

---

## 🚀 What's Next?

Potential future improvements:
- 🔍 Search within current page
- 📑 Bookmarks/favorites for quick navigation
- ⌨️ Keyboard shortcuts for page navigation (Ctrl+PageUp/Down)
- 📊 Segment statistics per page
- 🎯 "Jump to segment #" feature

---

**Enjoy the blazing-fast performance!** ⚡
