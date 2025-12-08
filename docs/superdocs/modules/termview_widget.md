# termview_widget

**File:** `modules/termview_widget.py`
**Lines:** 885
**Classes:** 4
**Functions:** 0

---

## Module Description

Termview Widget - RYS-style Inline Terminology Display

Displays source text with termbase translations shown directly underneath each word/phrase.
Inspired by the RYS Trados plugin's inline term visualization.

Features:
- Visual mapping: translations appear under their source terms
- Hover tooltips: show synonyms/alternatives
- Click to insert: click any translation to insert into target
- Multi-word term support: handles both single words and phrases

---

## Classes

### `FlowLayout`

**Line:** 22

Flow layout that wraps widgets to next line when needed

#### Methods

##### `addItem()`

No docstring

##### `horizontalSpacing()`

No docstring

##### `verticalSpacing()`

No docstring

##### `count()`

No docstring

##### `itemAt()`

No docstring

##### `takeAt()`

No docstring

##### `expandingDirections()`

No docstring

##### `hasHeightForWidth()`

No docstring

##### `heightForWidth()`

No docstring

##### `setGeometry()`

No docstring

##### `sizeHint()`

No docstring

##### `minimumSize()`

No docstring

##### `doLayout()`

No docstring

##### `smartSpacing()`

No docstring


---

### `TermBlock`

**Line:** 128

Individual term block showing source word and its translation(s)

#### Methods

##### `init_ui()`

Create the visual layout for this term block - COMPACT RYS-style

##### `on_translation_clicked()`

Handle click on translation to insert into target


---

### `NTBlock`

**Line:** 255

Non-translatable block showing source word with pastel yellow styling

#### Methods

##### `init_ui()`

Create the visual layout for this NT block - pastel yellow styling

##### `on_nt_clicked()`

Handle click on NT to insert source text as-is


---

### `TermviewWidget`

**Line:** 333

Main Termview widget showing inline terminology for current segment

#### Methods

##### `init_ui()`

Initialize the UI

##### `update_with_matches()`

Update the termview display with pre-computed termbase and NT matches

RYS-STYLE DISPLAY: Show source text as tokens with translations underneath

Args:
    source_text: Source segment text
    termbase_matches: List of termbase match dicts from Translation Results
    nt_matches: Optional list of NT match dicts with 'text', 'start', 'end', 'list_name' keys

##### `update_for_segment()`

DEPRECATED: Use update_with_matches() instead

Update the termview display for a new segment

Args:
    source_text: Source segment text
    source_lang: Source language code
    target_lang: Target language code
    project_id: Project ID for termbase priority lookup

##### `get_all_termbase_matches()`

Get all termbase matches for text by using the proper termbase search

This uses the SAME search logic as the Translation Results panel,
ensuring we only show terms that actually match, not false positives.

Args:
    text: Source text
    
Returns:
    Dict mapping source term (lowercase) to list of translation dicts

##### `tokenize_with_multiword_terms()`

Tokenize text, preserving multi-word terms found in termbase

Args:
    text: Source text
    matches: Dict of termbase matches (from get_all_termbase_matches)
    
Returns:
    List of tokens (words/phrases/numbers), with multi-word terms kept together

##### `tokenize_source()`

Tokenize source text into words/phrases

DEPRECATED: Use tokenize_with_multiword_terms instead for proper multi-word handling

Args:
    text: Source text
    
Returns:
    List of tokens (words/phrases)

##### `search_term()`

Search termbases for a specific term

Args:
    term: Source term to search
    
Returns:
    List of translation dicts (filtered to only include terms that exist in current segment)

##### `clear_terms()`

Clear all term blocks

##### `on_term_insert_requested()`

Handle request to insert a translation


---

