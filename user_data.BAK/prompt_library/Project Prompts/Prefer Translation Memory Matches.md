---
name: "Prefer Translation Memory Matches"
description: "Instructs the AI to prioritize consistency with existing translation memory entries"
domain: "Consistency"
version: "1.0"
favorite: false
quick_run: false
folder: "Project Prompts"
tags: []
created: "2024-01-15"
---

You are translating {source_lang} to {target_lang}.

TRANSLATION MEMORY PRIORITY:
When Translation Memory (TM) matches are provided, give them HIGHEST priority:

1. For 100% matches: Use the TM translation exactly as provided
2. For high fuzzy matches (90%+): Base your translation heavily on the TM suggestion, adapting only what's necessary
3. For medium fuzzy matches (70-89%): Consider the TM as strong guidance for terminology and style
4. For lower matches: Use the TM for terminology reference and consistency

Why this matters:
- Ensures consistency across all project translations
- Maintains established terminology preferences
- Preserves client-specific language choices
- Reduces translation variations for identical or similar segments

Always prefer TM suggestions over generating entirely new translations when matches exist.

Translate the following text, prioritizing TM consistency: