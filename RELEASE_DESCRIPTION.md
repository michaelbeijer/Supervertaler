# Supervertaler v1.9.272

**Professional AI-enhanced translation workbench** with multi-LLM support (GPT-4, Claude, Gemini, Ollama), translation memory, glossary management, and seamless CAT tool integration (memoQ, Trados, CafeTran, Phrase, Deja Vu).

## What's New (v1.9.272)

### Bug Fixes
- **Fixed Trados return package with missing `<target>` elements** — Trados Studio 2024 creates SDLXLIFF files where untranslated segments have no `<target>` element at all. The export engine now creates `<target>` by cloning the `<seg-source>` structure with translations inserted. Also handles targets without `<mrk>` tags. Resolves [#161](https://github.com/michaelbeijer/Supervertaler/issues/161).
- **Fixed XML entity escaping in SDLXLIFF export** — Source text containing `&`, `<`, or `>` characters was written unescaped, causing Trados Studio to reject the return package. Now properly escaped in XML output.
- **`conf="Translated"` attribute now added when missing** — Ensures Trados Studio recognizes segments as translated even when the original SDLXLIFF had no `conf` attribute.
- **Grid-to-segment sync now reverses invisible characters** — Display characters (middle dots, arrows) are converted back to actual whitespace before export. Stripped outer wrapping tags are also restored.

### Improvements
- **Enhanced Trados export diagnostics** — The export pipeline now logs segment counts, translation counts, and warns when file content is unchanged after replacement.

## Downloads

| Platform | File | Notes |
|----------|------|-------|
| **Windows** | `Supervertaler-1.9.272-Windows.zip` | Extract and run `Supervertaler.exe` |
| **macOS** | `Supervertaler-1.9.272-macOS.dmg` | Drag to Applications. Right-click -> Open on first launch. |
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
