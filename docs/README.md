# Supervertaler Documentation

This directory contains all documentation for the Supervertaler project, organized by type and audience.

## Directory Structure

### 📘 user_guides/
**Audience**: End users and translators

User-facing documentation, guides, and tutorials:
- `API_KEYS_SETUP_GUIDE.md` - How to configure API keys for translation services
- `SYSTEM_PROMPTS_GUIDE.md` - Complete guide to System Prompts and Custom Instructions
- `TM_USER_GUIDE.md` - Translation Memory user guide
- `TRANSLATION_WORKSPACE_REDESIGN.md` - Guide to the Translation Workspace interface
- `WORKSPACE_VISUAL_GUIDE.md` - Visual guide with UI explanations
- `Supervertaler User Guide (v2.4.0).md` - Complete user guide for v2.4.0

**When to add here**: Documentation that helps users understand and use Supervertaler features.

### 🔧 implementation/
**Audience**: Developers and contributors

Technical implementation documentation and design decisions:
- `DASHBOARD_FIXES_v2.5.0.md` - Dashboard bug fixes
- `DASHBOARD_LAYOUT_v2.5.0.md` - Dashboard layout implementation
- `FINAL_TAB_ORGANIZATION_v2.5.0.md` - Tab organization structure
- `INTEGRATION_PLAN_v2.5.0.md` - CAT editor integration plan
- `INTEGRATION_PROGRESS_v2.5.0.md` - Integration progress tracking
- `SEGMENT_GRID_IMPLEMENTATION_v2.5.0.md` - Segment grid technical details
- `TAB_REORGANIZATION_v2.5.0.md` - Tab reorganization process
- `TRANSLATION_MEMORY_IMPLEMENTATION.md` - TM technical implementation
- `RELEASE_SUMMARY_v2.5.0.md` - v2.5.0 release summary

**When to add here**: Technical documentation about how features are implemented.

### 📝 session_summaries/
**Audience**: Development team and project history

Daily session summaries and progress reports:
- `COMPLETE_SESSION_SUMMARY_2025-10-03.md` - October 3 session
- `SESSION_SUMMARY_2025-10-05.md` - October 5 session
- `SESSION_SUMMARY_2025-10-05_EOD.md` - October 5 end-of-day summary
- `SESSION_CHECKPOINT_v2.5.0.md` - Development checkpoint

**When to add here**: End-of-day summaries, session notes, progress checkpoints.

### 📦 archive/
**Audience**: Reference and historical context

Historical documentation and misc files:
- `MAIN_DIRECTORY_CLEANUP_COMPLETE.md` - Previous cleanup report
- `MAIN_DIRECTORY_CLEANUP_REVIEW.md` - Cleanup review
- `Supervertaler's Competition (apps that do dimilar things).md` - Competitive analysis

**When to add here**: Completed cleanup reports, historical notes, misc documentation.

## Core Documentation (in root)

These files remain in the root directory for visibility:
- `README.md` - Project overview and getting started
- `CHANGELOG.md` - Version history and changes
- `REPOSITORY_CLEANUP_RECOMMENDATIONS.md` - Cleanup recommendations (latest)
- `REPOSITORY_CLEANUP_COMPLETED.md` - Cleanup completion report (latest)

## Documentation Guidelines

### For New User-Facing Features
1. Create guide in `user_guides/`
2. Update main `README.md` with brief mention
3. Add entry to `CHANGELOG.md`

### For Technical Implementations
1. Create detailed doc in `implementation/`
2. Reference in relevant user guide if needed
3. Update `CHANGELOG.md` with technical details

### For Session Summaries
1. Create in `session_summaries/`
2. Use naming format: `SESSION_SUMMARY_YYYY-MM-DD.md`
3. Include: accomplishments, code changes, next steps

### For Completed/Historical Docs
1. Move to `archive/` when no longer active
2. Keep for reference and project history
3. Update references in other docs if needed

## Quick Reference

| I need to... | Look in... |
|--------------|------------|
| Learn how to use a feature | `user_guides/` |
| Understand how something works | `implementation/` |
| See what was done on a specific day | `session_summaries/` |
| Find historical context | `archive/` |
| Get started quickly | `../README.md` (root) |
| See version changes | `../CHANGELOG.md` (root) |

## Contributing Documentation

When adding new documentation:
1. Choose the appropriate directory based on audience
2. Use clear, descriptive filenames
3. Include version numbers for version-specific docs
4. Keep README.md and CHANGELOG.md in sync
5. Cross-reference related docs when helpful

---

*Documentation structure established: October 6, 2025*
