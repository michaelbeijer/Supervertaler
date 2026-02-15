# Supervertaler - AI Agent Documentation (Compact)

> **Purpose:** Fast, reliable handoff when context is low or chats reset.
> **Last Updated:** February 15, 2026 | **Version:** v1.9.267

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

- **Current version:** `v1.9.267`
- **Main app:** `Supervertaler.py` (large monolithic PyQt6 file)
- **Latest major completed work:**
  - Standalone SDLXLIFF import/export without Trados package (v1.9.267)
  - TXT/MD sentence segmentation with "Split lines into sentences" checkbox (v1.9.265)
  - Markdown-aware segmenter (`modules/simple_segmenter.py::MarkdownSegmenter`) (v1.9.265)
  - Empty line handling: always preserved for export, hidden in grid (v1.9.265–266)
  - Export regroups segments by `paragraph_id` via `itertools.groupby` (v1.9.265)
  - Direct Markdown (.md) export support (v1.9.264)
  - Voice command AHK v2 syntax fix, AutoFingers support (v1.9.263)
  - Claude Opus 4.6 model + Anthropic /v1/models API discovery (v1.9.262)
  - Cross-platform support: macOS/Linux via `modules/platform_helpers.py` (v1.9.246)
  - Native global hotkey system replacing AHK-only approach (v1.9.246)
  - Unified settings system in `settings/settings.json`
  - Custom OpenAI-compatible provider (`custom_openai`)

---

## 📁 Key Paths (Source of Truth)

- Main app: `Supervertaler.py`
- Modules: `modules/`
- Sentence segmenter: `modules/simple_segmenter.py` (`SimpleSegmenter`, `MarkdownSegmenter`)
- Platform helpers: `modules/platform_helpers.py`
- Tests: `tests/`
- Changelog: `CHANGELOG.md`
- Version source: `pyproject.toml`
- Dependencies: `requirements.txt` (includes `pynput>=1.7.6`)
- Website version mention: `docs/index.html`
- Unified settings: `settings/settings.json`
- AHK hotkey script (Windows fallback): `supervertaler_hotkeys.ahk`
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

## 🌐 Cross-Platform Architecture (v1.9.246+)

Central module: `modules/platform_helpers.py`

Constants:
- `IS_WINDOWS`, `IS_MACOS`, `IS_LINUX`

Utilities:
- `open_file(path)` / `open_folder(path)` — replaces `os.startfile()`
- `get_hidden_subprocess_flags()` — `CREATE_NO_WINDOW` on Windows, empty dict elsewhere

Global hotkeys (`GlobalHotkeyManager`):
- Windows: `RegisterHotKey` API (background thread with `GetMessageW` loop)
- macOS/Linux: pynput `GlobalHotKeys` (requires Accessibility permission on macOS)
- Callbacks do **zero work** in the background thread — only signal Qt main thread via `QMetaObject.invokeMethod`
- Main thread handles: send Cmd/Ctrl+C → wait 250ms → read clipboard → dispatch

Keystroke injection (`CrossPlatformKeySender`):
- Windows: AHK subprocess (`Send "^c"` via temp `.ahk` file), PowerShell `SendKeys` fallback
- macOS: `osascript` (`tell application "System Events" to keystroke "c" using command down`)
- Linux: pynput `Controller`

Hotkey callback flow:
```
pynput/WinAPI thread → QMetaObject.invokeMethod (QueuedConnection)
  → @pyqtSlot _handle_superlookup_hotkey (main thread)
    → CrossPlatformKeySender.send_copy()
    → QTimer.singleShot(250ms) → read clipboard → on_ahk_capture(text)
```

---

## 🍎 macOS Hotkey Status — Pending Fixes

**Working:**
- pynput `GlobalHotKeys` registers successfully (shows "Active via PYNPUT")
- Accessibility permission grant flow works
- Crash fixed (was caused by doing pyperclip/pynput work in background thread)

**Known issues:**
1. `osascript` Cmd+C deletes selected text in source app (likely stray modifier keys from hotkey)
2. Cmd+C doesn't actually copy selections — only reads existing clipboard content
3. Reliability: sometimes works, sometimes doesn't

**Planned fixes:**
- Debug `osascript` keystroke injection (may need modifier release delay before sending)
- Consider using `pbcopy` via AppleScript instead of keystroke simulation
- Change macOS shortcuts: ⌃⌥L/M → **⌃⌘L/M** (Ctrl+Cmd, user-requested — easier to reach)

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

## 📝 TXT/MD Import Architecture (v1.9.265+)

- Import dialog offers "Split lines into sentences" checkbox (persisted in `general_settings.json` as `last_import_sentence_segment`)
- TXT files use `SimpleSegmenter`, MD files use `MarkdownSegmenter` (protects links, code, URLs via placeholder pattern)
- Multiple sentences from one line share the same `paragraph_id`
- Export regroups by `paragraph_id` using `itertools.groupby`, joining sentences with spaces
- Empty lines are imported as empty segments (hidden in grid, preserved for export round-trip)
- Empty segments are hidden by `_apply_pagination_to_grid()` and all filter/visibility functions
- Language settings: `general_settings.json` stores `last_import_source_lang`/`last_import_target_lang` (shared across DOCX, TXT/MD, multi-file dialogs)

---

## 📌 Active Priorities

1. **Fix macOS global hotkey Cmd+C issues** (deletes selection, doesn't copy).
2. **Make macOS shortcuts configurable** (⌃⌘L/M instead of ⌃⌥L/M).
3. **Test Linux global hotkeys** (pynput backend, untested).
4. Continue reducing monolith pressure in `Supervertaler.py`.
5. Maintain release reliability (PyPI + Windows core/full artifacts).
6. Keep this file short and operationally focused.

---

## 📚 Archived Reference

The full historical/long-form agent document is preserved at:
- `docs/agent-archive/AGENTS_FULL_REFERENCE_v1.9.240_2026-02-08.md`

When context is limited, use this compact file first and open the archive only when needed.
