# Supervertaler - AI Agent Documentation (Compact)

> **Purpose:** Fast, reliable handoff when context is low or chats reset.
> **Last Updated:** February 8, 2026 | **Version:** v1.9.241

---

## ⚡ 60-Second Resume Checklist

1. Read `CHANGELOG.md` top entry (latest release context).
2. Check `git status --short` (do not revert unrelated user changes).
3. Confirm version in `pyproject.toml`.
4. Confirm unified settings in `settings/settings.json`.
5. If deeper context is needed, open:
   - `docs/agent-archive/AGENTS_FULL_REFERENCE_v1.9.240_2026-02-08.md`

---

## 🎯 Current State

- **Current version:** `v1.9.241`
- **Main app:** `Supervertaler.py` (large monolithic PyQt6 file)
- **Latest major completed work:**
  - Unified settings system in `settings/settings.json`
  - Inline API key editing in Settings UI
  - One-time migration from legacy settings files (`.migrated`)
  - Custom OpenAI-compatible provider (`custom_openai`)

---

## 📁 Key Paths (Source of Truth)

- Main app: `Supervertaler.py`
- Modules: `modules/`
- Tests: `tests/`
- Changelog: `CHANGELOG.md`
- Version source: `pyproject.toml`
- Website version mention: `docs/index.html`
- Unified settings: `settings/settings.json`
- Archived full agent reference:
  - `docs/agent-archive/AGENTS_FULL_REFERENCE_v1.9.240_2026-02-08.md`

---

## 🏗️ Settings Architecture (v1.9.240+)

Primary config:
- `settings/settings.json`

Top-level sections:
- `api_keys`
- `general`
- `ui`
- `features`

Satellite files under `settings/`:
- `themes.json`
- `shortcuts.json`
- `recent_projects.json`
- `find_replace_history.json`
- `superlookup_history.json`
- `voice_commands.json`
- `model_version_cache.json`

Migration behavior:
- Legacy settings files are migrated at startup and renamed to `.migrated`.

---

## 🔑 API Keys

Primary storage:
- `settings/settings.json` under `api_keys`

Compatibility:
- Legacy `api_keys.txt` remains supported as fallback input.

Common key names:
- `openai`, `claude`, `google`, `gemini`, `custom_openai`, `deepl`, `google_translate`, `ollama_endpoint`

Notes:
- `google` and `gemini` are aliases.
- `custom_openai` supports OpenAI-compatible endpoints (endpoint/model configured in Settings > AI Settings).

---

## 🔌 LLM Providers

Supported providers:
- `openai`
- `claude`
- `gemini`
- `ollama`
- `custom_openai`

Relevant implementation files:
- `modules/llm_clients.py`
- `Supervertaler.py` (settings UI and provider wiring)

---

## 🧪 Testing Quick Start

Run:
```bash
pytest tests/
```

Manual smoke test checklist:
- Import DOCX, translate, export
- Save/load `.svproj`
- TM and termbase behavior
- AI translation with configured keys
- SDLPPX round-trip

---

## 📦 Release Checklist

1. Update version in `pyproject.toml`.
2. Update release notes in `CHANGELOG.md`.
3. Update version mention in `docs/index.html`.
4. Validate main workflows.
5. Build and upload:

```bash
python -m build
python -m twine upload dist/supervertaler-<version>*
```

Windows EXE packaging:
- `build_windows_release.ps1` (core/full)

---

## ⚠️ High-Value Pitfalls

1. `Supervertaler.py` is large: read/edit by line range, not full-file stream.
2. Qt table access: use `cellWidget()` for editors and `item()` for plain items.
3. Block signals during programmatic text updates to avoid cascades.
4. Style issues can be timing-related (hidden widgets, deferred visibility).
5. XML namespace formats (SDLXLIFF): always use namespace dicts.

---

## 📌 Active Priorities

1. Keep unified settings and migration stable.
2. Continue reducing monolith pressure in `Supervertaler.py`.
3. Maintain release reliability (PyPI + Windows core/full artifacts).
4. Keep this file short and operationally focused.

---

## 📚 Archived Reference

The full historical/long-form agent document is preserved at:
- `docs/agent-archive/AGENTS_FULL_REFERENCE_v1.9.240_2026-02-08.md`

When context is limited, use this compact file first and open the archive only when needed.
