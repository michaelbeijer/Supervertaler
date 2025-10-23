# FTS5 Syntax Error Fix - October 23, 2025

## Issue

**Error Message:**
```
sqlite3.OperationalError: fts5: syntax error near ","
```

**Symptoms:**
- Translation fails on segments containing commas or special punctuation
- Auto-search crashes with FTS5 syntax error
- Manual TM search fails
- Error occurs in `database_manager.py` line 488 (`search_fuzzy_matches`)

## Root Cause

The FTS5 full-text search engine in SQLite has special characters that cause syntax errors when used in queries:
- Commas: `,`
- Parentheses: `(` `)`
- Quotes: `"` `'`
- Colons: `:`
- Hyphens: `-`
- And other punctuation

When segment text like "De uitvinding heeft betrekking op een voegplaat, voorzien van een wapening." was tokenized, the commas were passed directly to FTS5, causing a syntax error.

**Original problematic code:**
```python
search_terms = source.strip().split()
fts_query = ' OR '.join(search_terms)  # e.g., "text, with, commas"
```

This created invalid FTS5 queries like: `text, OR with, OR commas`

## Solution

### 1. Sanitize Input Text
Remove special characters before tokenizing:
```python
import re
# Remove special FTS5 characters and split into words
clean_text = re.sub(r'[^\w\s]', ' ', source)  # Replace special chars with spaces
search_terms = [term for term in clean_text.strip().split() if len(term) > 1]
```

### 2. Quote Terms
Quote each search term to prevent FTS5 interpretation:
```python
# Quote each term to prevent FTS5 syntax errors
fts_query = ' OR '.join(f'"{term}"' for term in search_terms)
```

### 3. Handle Empty Queries
Return empty results if no valid terms remain:
```python
if not search_terms:
    return []
```

## Files Modified

### `modules/database_manager.py`
**Function:** `search_fuzzy_matches()` (lines ~449-470)

**Changes:**
```python
def search_fuzzy_matches(self, source: str, tm_ids: List[str] = None,
                        threshold: float = 0.75, max_results: int = 5,
                        source_lang: str = None, target_lang: str = None) -> List[Dict]:
    """Search for fuzzy matches using FTS5 with proper similarity calculation"""
    
    # For better FTS5 matching, tokenize the query and escape special chars
    # FTS5 special characters: " ( ) - : , . ! ? 
    import re
    # Remove special FTS5 characters and split into words
    clean_text = re.sub(r'[^\w\s]', ' ', source)  # Replace special chars with spaces
    search_terms = [term for term in clean_text.strip().split() if len(term) > 1]
    
    if not search_terms:
        # If no valid terms, return empty results
        return []
    
    # Quote each term to prevent FTS5 syntax errors
    fts_query = ' OR '.join(f'"{term}"' for term in search_terms)
    
    # Rest of function unchanged...
```

### `modules/translation_memory.py`
**Function:** Added `get_all_tms()` method (line ~376)

**Changes:**
```python
def get_all_tms(self, enabled_only: bool = False) -> List[Dict]:
    """Alias for get_tm_list() for backward compatibility"""
    return self.get_tm_list(enabled_only=enabled_only)
```

## Testing

### Test Cases
Created `test_fts5_special_chars.py` to verify fix:

```python
test_queries = [
    "De uitvinding heeft betrekking op een voegplaat, voorzien van een wapening.",
    "voorzien van een wapening, die",
    "test, with, commas",
    "(parentheses) and punctuation!",
    "quotes: 'single' and \"double\"",
]
```

### Results
```
Testing problematic queries:
------------------------------------------------------------

1. Query: 'De uitvinding heeft betrekking op een voegplaat, voorzien van een wapening.'
   ✓ Success! Found 2 matches
     • 82%: De uitvinding heeft betrekking op een vo...
     • 82%: De uitvinding heeft betrekking op een vo...

2. Query: 'voorzien van een wapening, die'
   ✓ Success! Found 0 matches

3. Query: 'test, with, commas'
   ✓ Success! Found 0 matches

4. Query: '(parentheses) and punctuation!'
   ✓ Success! Found 0 matches

5. Query: 'quotes: 'single' and "double"'
   ✓ Success! Found 0 matches

✓ All tests complete!
```

All queries now work without syntax errors, even with complex punctuation.

## Impact

### Fixed
- ✅ Translation works on all segments regardless of punctuation
- ✅ Auto-search no longer crashes
- ✅ Manual TM search handles special characters
- ✅ TM Manager opens without error
- ✅ Fuzzy matching returns real similarity scores (82%, 73%, etc.)

### Performance
- No performance impact - regex sanitization is fast
- FTS5 still provides fast candidate retrieval
- SequenceMatcher calculates final similarity on candidates only

## Related Issues

This fix also resolved the TM Manager error by adding the missing `get_all_tms()` method to both:
- `database_manager.py` - Database backend
- `translation_memory.py` - TMDatabase wrapper class

## Prevention

Future FTS5 queries should:
1. Always sanitize input before passing to FTS5
2. Quote individual search terms
3. Handle empty query cases gracefully
4. Test with real-world punctuation-heavy text

## Notes

- FTS5 syntax is strict about special characters
- The regex `r'[^\w\s]'` removes all non-word, non-space characters
- Quoted terms like `"word"` are treated as exact tokens by FTS5
- SequenceMatcher still sees original punctuation for final similarity calculation
