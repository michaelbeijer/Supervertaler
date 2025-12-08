# term_extractor

**File:** `modules/term_extractor.py`
**Lines:** 270
**Classes:** 1
**Functions:** 1

---

## Module Description

Term Extractor Module

Extracts potential terminology from source text for project termbases.
Can be used as a standalone tool or integrated into Supervertaler.

Author: Michael Beijer
License: MIT

---

## Classes

### `TermExtractor`

**Line:** 17

Extract terminology from source text using various algorithms

#### Methods

##### `extract_terms()`

Extract potential terms from text

Args:
    text: Source text to analyze
    use_frequency: Consider term frequency in ranking
    use_capitalization: Give higher weight to capitalized terms
    use_special_chars: Consider terms with hyphens, underscores, etc.
    
Returns:
    List of term dictionaries with fields: term, frequency, score, type

##### `extract_from_segments()`

Extract terms from a list of segments (e.g., translation project)

Args:
    segments: List of source text segments
    
Returns:
    List of extracted term dictionaries

##### `filter_by_frequency()`

Filter terms by frequency range

##### `filter_by_type()`

Filter terms by type

##### `filter_by_score()`

Filter terms by minimum score

##### `deduplicate_terms()`

Remove duplicate terms (case-insensitive)


---

## Functions

### `extract_terms_from_text()`

**Line:** 237

Quick term extraction - returns just the term strings

Args:
    text: Source text
    source_lang: Language code
    min_frequency: Minimum occurrences
    max_terms: Maximum number of terms to return
    
Returns:
    List of term strings

---

