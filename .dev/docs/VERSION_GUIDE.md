# Documentation Organization Guide

> **📌 Version Scheme Update**: As of October 10, 2025, version numbering has changed to better reflect architectural differences. See [VERSION_RENUMBERING_v3.0.0.md](VERSION_RENUMBERING_v3.0.0.md) for details.

## Version Naming Scheme

### Current Versions

**v2.4.1-CLASSIC** (Production - DOCX Workflow)
- **File**: `Supervertaler_v2.4.1-CLASSIC.py`
- **Architecture**: Original DOCX-based workflow
- **Status**: ✅ Stable, production-ready
- **"-CLASSIC" suffix**: Indicates dignified legacy DOCX workflow architecture

**v3.0.0-beta** (Beta - CAT Editor)
- **File**: `Supervertaler_v3.0.0-beta_CAT.py`
- **Architecture**: Complete rewrite as segment-based CAT editor
- **Status**: 🧪 Beta testing phase
- **v3.x**: Major version bump reflects major architectural change
- **"beta" tag**: Indicates experimental/testing status

### Why the Major Version Bump?

The jump from v2.x to v3.x reflects a **major architectural change**:
- **v2.x-CLASSIC**: Document-centric DOCX workflow
- **v3.x**: Segment-centric CAT editor with grid/list/document views

This is not an incremental update but a fundamentally different application architecture.

---

## Version-Specific Documentation

### v2.4.1-CLASSIC (Production Ready)
**Primary Documentation**: [`user_guides/Supervertaler User Guide (v2.4.0).md`](user_guides/Supervertaler%20User%20Guide%20(v2.4.0).md)  
*(Note: v2.4.1 adds CafeTran/memoQ support - addendum coming soon)*

This is the **complete, comprehensive guide** for production use of Supervertaler. It includes:
- Quick start guide
- Complete feature documentation
- CAT tool integration workflows
- Domain-specific prompts
- Troubleshooting
- Advanced tips

**Additional v2.4.1 Documentation**:
- [`features/CAFETRAN_SUPPORT.md`](features/CAFETRAN_SUPPORT.md) - CafeTran bilingual DOCX workflow
- [`features/MEMOQ_SUPPORT.md`](features/MEMOQ_SUPPORT.md) - memoQ bilingual DOCX workflow
- [`user_guides/BILINGUAL_WORKFLOW_QUICK_START.md`](user_guides/BILINGUAL_WORKFLOW_QUICK_START.md) - Quick start for both

**Status**: ✅ Complete and stable

### v3.0.0-beta (Beta Testing)
**Documentation**: Distributed across multiple files

Since v3.0.0-beta represents a major rewrite, documentation is organized by feature:

**User Guides** (in `user_guides/`):
- [`SYSTEM_PROMPTS_GUIDE.md`](user_guides/SYSTEM_PROMPTS_GUIDE.md) - System Prompts & Custom Instructions
- [`TM_USER_GUIDE.md`](user_guides/TM_USER_GUIDE.md) - Translation Memory usage
- [`TRANSLATION_WORKSPACE_REDESIGN.md`](user_guides/TRANSLATION_WORKSPACE_REDESIGN.md) - Workspace interface
- [`WORKSPACE_VISUAL_GUIDE.md`](user_guides/WORKSPACE_VISUAL_GUIDE.md) - Visual UI guide

**Release Documentation**:
- [`RELEASE_NOTES_v3.0.0-beta.md`](RELEASE_NOTES_v3.0.0-beta.md) - What's new in v3.0.0-beta
- [`VERSION_RENUMBERING_v3.0.0.md`](VERSION_RENUMBERING_v3.0.0.md) - Why the version renumbering
- [`VERSION_3.0.0-beta_FILE_ORGANIZATION.md`](VERSION_3.0.0-beta_FILE_ORGANIZATION.md) - File structure

**Implementation Docs** (in `implementation/`):
- Technical details about new features
- Architecture decisions
- Integration plans
- Development progress

**Status**: 🚧 Beta testing - comprehensive user guide pending feature stabilization

---

## Quick Reference

| I want to... | For v2.4.1-CLASSIC | For v3.0.0-beta |
|--------------|------------|------------|
| **Get started** | Read the User Guide (v2.4.0) | Start with v2.4.1-CLASSIC, then explore v3.0.0-beta |
| **Learn features** | User Guide has everything | Check individual feature guides + Release Notes |
| **Understand technical details** | User Guide + implementation docs | Check `implementation/` folder + VERSION_RENUMBERING |
| **Report issues** | Use v2.4.1 guide as reference | Note which version (v3.0.0-beta) in issue report |
| **Contribute** | Follow v2.4.1 patterns | Check implementation docs for v3.0.0-beta |

---

## Documentation Status

### Complete Documentation ✅
- v2.4.0 User Guide (1,735 lines) - applies to v2.4.1-CLASSIC
- CafeTran Support Guide (v2.4.1-CLASSIC)
- memoQ Support Guide (v2.4.1-CLASSIC)
- Bilingual Workflow Quick Start (v2.4.1-CLASSIC)
- System Prompts Guide (v3.0.0-beta)
- TM User Guide (v3.0.0-beta)
- Translation Workspace guides (v3.0.0-beta)
- Version Renumbering Documentation (v3.0.0-beta)

### In Progress 🚧
- v3.0.0-beta Complete User Guide (pending feature stabilization)
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

**Important**: This guide was written for v2.4.0 but applies to v2.4.1-CLASSIC. The v2.4.1 version adds CafeTran and memoQ bilingual DOCX support - see the additional guides listed above.

Once you're comfortable with v2.4.1-CLASSIC, you can explore v3.0.0-beta experimental CAT editor features.

---

## For Developers

### Working on v2.4.1-CLASSIC
- Refer to User Guide for feature documentation
- Check `archive/` for historical context
- Maintain stability and backward compatibility
- DOCX workflow architecture

### Working on v3.0.0-beta
- Read implementation docs in `implementation/`
- Check session summaries for recent changes
- Update feature-specific guides as you develop
- Mark experimental features clearly
- CAT editor architecture (fundamentally different from v2.x)

---

*Last updated: October 10, 2025*
