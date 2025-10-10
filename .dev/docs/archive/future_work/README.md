# Archive - Future Work

This folder contains documentation for **future features** that are not yet implemented in the current release.

## Files

### Cross-Platform Distribution
- `CROSS_PLATFORM_DISTRIBUTION.md` - Plans for macOS and Linux distributions
- `CROSS_PLATFORM_IMPLEMENTATION_SUMMARY.md` - Implementation notes for cross-platform builds
- `QUICK_START_MACOS_LINUX.md` - Future quick start guide for macOS/Linux users

## Status

These features are planned for **future releases** (v2.6.0 or later). The current release (v2.4.1) is **Windows-only**.

## Implementation Notes

When implementing cross-platform support:
1. PyInstaller supports macOS and Linux
2. Will need to test on each platform
3. May need platform-specific icon formats
4. File paths need to be cross-platform compatible
5. Consider using `pathlib` instead of `os.path`

## Related Issues

Track progress on cross-platform support:
- GitHub Issue: TBD (create when starting this work)

---

**Status:** Planning / Not Implemented  
**Target Version:** v2.6.0+  
**Current Version:** v2.4.1 (Windows only)
