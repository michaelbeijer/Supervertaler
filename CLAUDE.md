# Supervertaler — Claude Code Reference

> Concise project reference for AI-assisted development. Check `CHANGELOG.md` for latest version and recent work.

## Project Overview

Supervertaler is a desktop CAT (Computer-Assisted Translation) tool built with PyQt6. It combines AI translation (multiple LLM providers), translation memory, terminology management, and quality assurance in a single application.

## Key Paths

| What | Path |
|------|------|
| Main app (monolithic) | `Supervertaler.py` |
| Modules | `modules/` |
| Version (source of truth) | `pyproject.toml` |
| Changelog | `CHANGELOG.md` |
| Website (landing) | `docs/index.html` |
| Website (Desktop page) | `docs/desktop.html` |
| Website (Trados page) | `docs/trados.html` |
| Website CSS | `docs/styles.css` |
| Help — Desktop (GitBook) | `docs/help/supervertaler/` |
| Help — Trados (GitBook) | `docs/help/supervertaler-for-trados/` |
| Help — Desktop (old, git-synced) | `docs/superdocs/` |
| Tests | `tests/` |
| Settings | `settings/settings.json` |
| Dependencies | `requirements.txt` |

### Important modules

- `modules/termlens_widget.py` — TermLens inline terminology display (`TermLensWidget`)
- `modules/llm_clients.py` — LLM provider abstraction
- `modules/termbase_manager.py` — glossary/termbase CRUD
- `modules/database_manager.py` — SQLite database layer
- `modules/translation_results_panel.py` — match panel UI
- `modules/shortcut_manager.py` — keyboard shortcut system
- `modules/simple_segmenter.py` — sentence segmentation (`SimpleSegmenter`, `MarkdownSegmenter`)
- `modules/platform_helpers.py` — cross-platform utilities (Windows/macOS/Linux)

## Settings Architecture

Primary config: `settings/settings.json` with top-level sections: `api_keys`, `general`, `ui`, `features`.

Satellite files under `settings/`: `themes.json`, `shortcuts.json`, `recent_projects.json`, `find_replace_history.json`, `superlookup_history.json`, `voice_commands.json`, `model_version_cache.json`.

Legacy settings files are auto-migrated at startup and renamed to `.migrated`.

## Pitfalls

1. `Supervertaler.py` is very large — always read/edit by line range, never full-file.
2. Qt table access: use `cellWidget()` for editors, `item()` for plain items.
3. Block signals during programmatic text updates to avoid cascades.
4. Style issues can be timing-related (hidden widgets, deferred visibility).
5. XML namespace formats (SDLXLIFF): always use namespace dicts.

## Testing

```bash
pytest tests/
```

Manual smoke test: import DOCX → translate → export, save/load `.svproj`, TM + termbase matching, AI translation, SDLPPX round-trip.
