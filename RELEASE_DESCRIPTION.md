# Supervertaler v1.9.261

**Professional AI-enhanced translation workbench** with multi-LLM support (GPT-4, Claude, Gemini, Ollama), translation memory, glossary management, and seamless CAT tool integration (memoQ, Trados, CafeTran, Phrase, Deja Vu).

## What's New (v1.9.256 - v1.9.261)

### Performance
- **TM batch pre-translation is up to 30x faster** — A 912-segment document that took ~2 minutes now completes in ~4 seconds (exact match) or ~12 seconds (fuzzy matching). Batch SQL queries, source deduplication, single-commit optimization, and reduced UI overhead.
- **TM fuzzy matching rewritten** — Fuzzy matching now loads all TM candidates into memory with a single SQL query and applies a three-tier pre-filter cascade, replacing hundreds of individual FTS5 queries. Fuzzy matching that took 5-7 minutes now completes in seconds.

### New Features
- **`{{TARGET_TEXT}}` placeholder in Prompt Manager** — Reference the current segment's existing translation in your prompts. Ideal for review/proofreading workflows, e.g. *"Review this translation: {{SOURCE_TEXT}} -> {{TARGET_TEXT}}"*.

### Improvements
- **TM match status icons in grid** — After batch pre-translation, segments show ✅ for exact TM matches (100%) and 🔶 for fuzzy matches, with match percentage displayed next to the icon.
- **Match Panel shows batch TM results** — Clicking a pre-translated segment immediately displays TM source/target in the Match Panel without waiting for a background lookup.
- **Batch translate dialog labels clarified** — TM checkbox now shows "(exact + fuzzy >=75%)" and exact-only sub-option shows "(100% matches only - fastest)" for clearer mode distinction.

### Bug Fixes
- **Match Panel no longer overwrites batch TM data** — Background TM lookup no longer replaces pre-translation match data with empty results.
- **Editing confirmed segments now always resets status** — Copy Source to Target and all confirmed-like statuses are properly handled. ([#154](https://github.com/michaelbeijer/Supervertaler/issues/154))
- **Title bar shows correct version via pip** — Version reader now falls back to `importlib.metadata` for pip installs. ([#157](https://github.com/michaelbeijer/Supervertaler/issues/157))
- **Batch translation with Custom OpenAI provider now works** — Batch code path correctly reads API key from custom endpoint profile. ([#157](https://github.com/michaelbeijer/Supervertaler/issues/157))
- **Fixed `.strip()` mismatch** between confirm and edit paths for consistent status detection.

## Downloads

| Platform | File | Notes |
|----------|------|-------|
| **Windows** | `Supervertaler-1.9.261-Windows.zip` | Extract and run `Supervertaler.exe` |
| **macOS** | `Supervertaler-1.9.261-macOS.dmg` | Drag to Applications. Right-click -> Open on first launch. |
| **pip** | `pip install supervertaler` | Python 3.10+ required |

## Requirements

- **Windows**: Windows 10 or later (x64)
- **macOS**: macOS 13 (Ventura) or later (Apple Silicon or Intel)
- **pip**: Python 3.10+, PyQt6

## Links

- [Changelog](https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md)
- [Online Manual](https://supervertaler.gitbook.io/superdocs/)
- [Website](https://supervertaler.com)
- [PyPI](https://pypi.org/project/supervertaler/)
