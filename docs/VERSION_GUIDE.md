# Documentation Organization Guide

## Version-Specific Documentation

### v2.4.0 (Stable - Production Ready)
**Primary Documentation**: [`user_guides/Supervertaler User Guide (v2.4.0).md`](user_guides/Supervertaler%20User%20Guide%20(v2.4.0).md)

This is the **complete, comprehensive guide** for production use of Supervertaler. It includes:
- Quick start guide
- Complete feature documentation
- CAT tool integration workflows
- Domain-specific prompts
- Troubleshooting
- Advanced tips

**Status**: ✅ Complete and stable

### v2.5.0 (Experimental - CAT Editor Development)
**Documentation**: Distributed across multiple files

Since v2.5.0 is under active development, documentation is organized by feature:

**User Guides** (in `user_guides/`):
- [`SYSTEM_PROMPTS_GUIDE.md`](user_guides/SYSTEM_PROMPTS_GUIDE.md) - System Prompts & Custom Instructions
- [`TM_USER_GUIDE.md`](user_guides/TM_USER_GUIDE.md) - Translation Memory usage
- [`TRANSLATION_WORKSPACE_REDESIGN.md`](user_guides/TRANSLATION_WORKSPACE_REDESIGN.md) - Workspace interface
- [`WORKSPACE_VISUAL_GUIDE.md`](user_guides/WORKSPACE_VISUAL_GUIDE.md) - Visual UI guide

**Implementation Docs** (in `implementation/`):
- Technical details about new features
- Architecture decisions
- Integration plans
- Development progress

**Status**: 🚧 In progress - full user guide will be created once features stabilize

---

## Quick Reference

| I want to... | For v2.4.0 | For v2.5.0 |
|--------------|------------|------------|
| **Get started** | Read the User Guide (v2.4.0) | Start with v2.4.0, then explore v2.5.0 |
| **Learn features** | User Guide has everything | Check individual feature guides |
| **Understand technical details** | User Guide + implementation docs | Check `implementation/` folder |
| **Report issues** | Use v2.4.0 guide as reference | Note which version in issue report |
| **Contribute** | Follow v2.4.0 patterns | Check implementation docs for v2.5.0 |

---

## Documentation Status

### Complete Documentation ✅
- v2.4.0 User Guide (1,735 lines)
- System Prompts Guide (v2.5.0)
- TM User Guide (v2.5.0)
- Translation Workspace guides (v2.5.0)

### In Progress 🚧
- v2.5.0 Complete User Guide (pending feature stabilization)
- Context-aware translation guide
- Batch translation guide
- Prompt Library guide

---

## For New Users

**Start Here**: [`user_guides/Supervertaler User Guide (v2.4.0).md`](user_guides/Supervertaler%20User%20Guide%20(v2.4.0).md)

This comprehensive guide will teach you:
1. How Supervertaler works
2. How to integrate with your CAT tool
3. All available features
4. Best practices
5. Troubleshooting

Once you're comfortable with v2.4.0, you can explore v2.5.0 experimental features.

---

## For Developers

### Working on v2.4.0
- Refer to User Guide for feature documentation
- Check `archive/` for historical context
- Maintain stability and backward compatibility

### Working on v2.5.0
- Read implementation docs in `implementation/`
- Check session summaries for recent changes
- Update feature-specific guides as you develop
- Mark experimental features clearly

---

*Last updated: October 6, 2025*
