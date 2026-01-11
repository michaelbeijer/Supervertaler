# Contributing to Supervertaler

Thanks for your interest in contributing to **Supervertaler**!

Supervertaler is a professional desktop translation application built with **Python** and **PyQt6**. Contributions of all kinds are welcome: bug reports, feature requests, documentation fixes, and code improvements.

## Quick links

- Issues: https://github.com/michaelbeijer/Supervertaler/issues
- Documentation (Superdocs): https://supervertaler.gitbook.io/superdocs/

## Bug reports

Bug reports are hugely valuable. The best bug reports are reproducible.

Please include:

1. **Supervertaler version** (shown in the app and in `pyproject.toml`).
2. **OS** (Windows version; Linux distro if applicable).
3. **How you installed** (PyPI vs. run from source).
4. **Exact steps to reproduce** (ideally minimal).
5. **Expected vs. actual behavior**.
6. **Logs / tracebacks** if you have them.
7. **Sample files** *only if you can share them publicly*.

If the issue is file-specific (DOCX/SDLPPX/memoQ/etc.), try to attach a minimal example or a redacted sample.

### Security reports

If you believe you found a security vulnerability, please **do not** open a public issue.

Instead, email the maintainer at: **info@michaelbeijer.co.uk**

## Feature requests

Feature requests are welcome. A good feature request includes:

- **User story**: what you’re trying to accomplish
- **Why it matters**: who benefits and how often
- **Scope**: small/medium/large (your best guess)
- **Alternatives**: workarounds you’ve tried
- **UI/UX notes**: screenshots/mockups are welcome

If you’re proposing a larger change, it’s best to open an issue first so we can align on approach before you spend time implementing it.

## Pull requests

PRs are welcome — thank you.

### Before you start

- For small fixes (typos, small bugs), feel free to open a PR directly.
- For larger work, please open an issue first and describe the approach.

### PR checklist

- Keep PRs focused and reasonably sized.
- Match the existing style and architecture.
- Prefer fixing root causes over adding surface-level workarounds.
- Include a clear description of the change and how you tested it.
- Avoid committing secrets (API keys, tokens, private documents).

### Commit messages

Semantic-style prefixes are preferred:

- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation-only changes
- `refactor:` refactors (no user-facing change)
- `style:` formatting-only changes
- `chore:` maintenance tasks

### What not to include

- Do not add large generated files (build artifacts, big binaries).
- Do not commit anything under `user_data/` or `user_data_private/`.
- Do not include proprietary documents or customer data.

## Development setup

### Requirements

- Python **3.10+**
- Windows (primary) or Linux (supported)

### Clone

```bash
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler
```

### Create a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Install dependencies

Core (recommended for most development):

```bash
pip install -e .
```

All optional features (larger install):

```bash
pip install -e ".[all]"
```

If you’re working on a specific area (e.g., MT providers, WebEngine, Supermemory), you can install only the relevant extra:

```bash
pip install -e ".[mt]"
pip install -e ".[web]"
pip install -e ".[supermemory]"
```

### Running the app

```bash
python Supervertaler.py
```

### API keys (optional)

If you want to test LLM features, copy the example file and add your keys:

- Start from `api_keys.example.txt`
- Create your local `api_keys.txt` (gitignored)

### Tests / basic validation

If you’re touching non-UI logic, please run tests if available:

```bash
pytest
```

For quick sanity checking of syntax:

```bash
python -m py_compile Supervertaler.py
```

## Coding standards

This is a mature, user-facing desktop app; stability matters.

- Follow PEP 8 style conventions where practical.
- Keep changes minimal and consistent with surrounding code.
- Prefer explicit names over abbreviations.
- Avoid adding new global state unless necessary.
- When working with Qt, keep UI updates on the main thread (use signals for worker threads).
- When working with XML (SDLXLIFF/ElementTree), handle namespaces explicitly.
- Don’t add heavy new dependencies lightly — the project supports modular installs via extras.

### UI consistency

Supervertaler has an established UI look-and-feel (custom checkbox/radio widgets, consistent colors and spacing). Please follow existing patterns instead of introducing new widget styles.

## License

By contributing, you agree that your contributions will be licensed under the repository’s MIT license.
