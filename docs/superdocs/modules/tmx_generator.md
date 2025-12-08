# tmx_generator

**File:** `modules/tmx_generator.py`
**Lines:** 284
**Classes:** 1
**Functions:** 5

---

## Module Description

TMX Generator Module

Helper class for generating TMX (Translation Memory eXchange) files.
Supports TMX 1.4 format with proper XML structure.

Extracted from main Supervertaler file for better modularity.

---

## Classes

### `TMXGenerator`

**Line:** 210

Helper class for generating TMX (Translation Memory eXchange) files

#### Methods

##### `generate_tmx()`

Generate TMX content from parallel segments

##### `save_tmx()`

Save TMX tree to file with proper XML formatting


---

## Functions

### `get_simple_lang_code()`

**Line:** 14

Convert language name or code to ISO 639-1 format (2-letter) or ISO 639-1 + region (e.g., en-US)

Supports:
- Language names: "English" → "en", "Dutch" → "nl"
- ISO codes: "en" → "en", "nl-NL" → "nl-NL"
- Variants: "en-US", "nl-BE", "fr-CA" → preserved as-is

Returns base code if no variant specified, or full code with variant if provided.

---

### `get_base_lang_code()`

**Line:** 119

Extract base language code from variant (e.g., 'en-US' → 'en', 'nl-BE' → 'nl', 'Dutch' → 'nl')

---

### `get_lang_match_variants()`

**Line:** 131

Get all possible string variants for matching a language in database queries.

Returns list of strings that could be used to match this language, including:
- Base ISO code (e.g., 'nl', 'en')
- Full language names (e.g., 'Dutch', 'English')
- Common variants (e.g., 'nl-NL', 'en-US')

This helps match database entries that may have inconsistent language formats.

---

### `normalize_lang_variant()`

**Line:** 177

Normalize language variant to lowercase-UPPERCASE format (e.g., 'en-us' → 'en-US', 'nl-be' → 'nl-BE').

Handles various input formats:
- nl-nl → nl-NL
- nl-NL → nl-NL  
- NL-NL → nl-NL
- nl_BE → nl-BE
- nl → nl (base code unchanged)

---

### `languages_are_compatible()`

**Line:** 205

Check if two language codes are compatible (same base language)

---

