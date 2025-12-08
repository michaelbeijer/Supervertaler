# superlookup

**File:** `modules/superlookup.py`
**Lines:** 228
**Classes:** 2
**Functions:** 0

---

## Module Description

Superlookup Engine
==================
System-wide translation lookup that works anywhere on your computer.
Captures text from any application and provides:
- TM matches from Supervertaler database
- Glossary term lookups
- MT/AI translations
- Web search integration

Can operate in different modes:
- memoQ mode (with CAT tool shortcuts)
- Trados mode
- CafeTran mode
- Universal mode (works in any text box)

---

## Classes

### `LookupResult`

**Line:** 25

Single lookup result

#### Methods


---

### `SuperlookupEngine`

**Line:** 38

Superlookup text lookup engine.
Captures text from any application and provides translation results.

#### Methods

##### `capture_text()`

Capture text - just copy what's selected and get clipboard.

Returns:
    Captured text or None if failed

##### `set_tm_database()`

Set the TM database for lookups

##### `set_glossary_database()`

Set the glossary database for term lookups

##### `search_tm()`

Search translation memory for matches.

Args:
    text: Source text to search for
    max_results: Maximum number of results to return
    
Returns:
    List of TM match results

##### `search_glossary()`

Search glossary for term matches.

Args:
    text: Text to extract terms from and search
    
Returns:
    List of glossary term matches

##### `get_mt_translations()`

Get machine translation suggestions.

Args:
    text: Text to translate
    
Returns:
    List of MT results

##### `lookup_all()`

Perform all types of lookups on the text.

Args:
    text: Text to look up
    
Returns:
    Dictionary with 'tm', 'glossary', 'mt' keys containing results


---

