# Superdocs — Landing Page Draft

Welcome to Superdocs — the official online manual and help center for Supervertaler. This draft proposes a concise landing structure, suggested section order, and microcopy for the Quick Start to help new users get productive quickly.

---

## Proposed Landing Structure

- Hero blurb: One-line value proposition + CTA to Quick Start
- Quick Start: 3–5 step onboarding (install, open project, import file, translate, export)
- Core Guides: AI Translation, CAT Tool Integration, Project Workflows
- Reference: Keyboard Shortcuts, Changelog, System Requirements, File Formats
- Troubleshooting & FAQ: Common issues and solutions
- Advanced: TM/Termbase management, Supermemory, Local LLM setup
- Links: GitHub Issues, Discussions, Download

---

## Hero (short)

Superdocs — everything you need to install, configure, and use Supervertaler.

Start with the Quick Start if you're installing for the first time, or browse Guides for workflows and advanced features.

[Open Quick Start](get-started/quick-start.md)

---

## Quick Start (microcopy)

1. Install Supervertaler

   - Windows: Download the installer from the Releases page and run it.
   - From source: `pip install -r requirements.txt && python Supervertaler.py`

2. Create a new project

   - File → New Project → choose source/target languages

3. Import a bilingual file

   - File → Import → Select DOCX / memoQ / SDLPPX

4. Translate using AI

   - Select segments and press the Translate button or use the Batch Translate dialog.
   - Configure prompts in the Prompt Manager; use the AI Assistant for suggestions.

5. Export changes back to your CAT tool

   - File → Export → choose bilingual DOCX, SDLRPX, or TMX

---

## Suggested Section Titles & Short Descriptions

- Quick Start — Get up and running in five minutes
- AI Translation — Prompt library, assistant, and provider setup
- CAT Tool Integration — memoQ, Trados, Phrase, CafeTran workflows
- Translation Memory — TM import/export, fuzzy matching, Supermemory
- Termbases & Glossaries — Create, import, and prioritize terms
- Editor & Grid UX — Keyboard navigation, shortcuts, and tips
- Troubleshooting — Common fixes and diagnostics

---

## Notes for Publication

- Keep landing blurb short and action-oriented.
- Ensure Quick Start links directly to single-page step-by-step content.
- Add screenshots for each Quick Start step to lower friction.

---

If you want, I can commit this draft to `docs/superdocs/` as a landing suggestion and/or turn the Quick Start microcopy into a full `get-started/quick-start.md` page with step-by-step instructions and screenshots.
