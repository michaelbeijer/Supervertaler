# autofingers_engine

**File:** `modules/autofingers_engine.py`
**Lines:** 466
**Classes:** 2
**Functions:** 1

---

## Module Description

AutoFingers Translation Automation Engine
Replicates AutoHotkey AutoFingers functionality in Python
Automates translation pasting in memoQ from TMX translation memory

---

## Classes

### `TranslationMatch`

**Line:** 48

Result of a translation lookup

---

### `AutoFingersEngine`

**Line:** 55

Translation automation engine for CAT tools like memoQ.
Loads translations from TMX and automates the paste workflow.

#### Methods

##### `load_tmx()`

Load and parse TMX translation memory file.

Returns:
    Tuple of (success: bool, message: str)

##### `lookup_translation()`

Look up translation for source text in TM database.
First tries exact match, then fuzzy if enabled.

Args:
    source_text: Source text to translate
    
Returns:
    TranslationMatch with translation, match_type, and match_percent
    Returns None if no match found

##### `process_single_segment()`

Process a single translation segment in memoQ.
Automates: copy source to target, lookup translation, paste, confirm.

Behavior for fuzzy matches:
- If fuzzy match found: paste it but DON'T auto-confirm
- Translator can then review and press Ctrl+Enter to confirm
- AutoFingers automatically moves to next segment

Returns:
    Tuple of (success: bool, message: str)

##### `process_multiple_segments()`

Process multiple segments in loop mode.

Args:
    max_segments: Maximum segments to process (0 = infinite)
    callback: Optional callback function(success, message) called after each segment
    
Returns:
    Tuple of (segments_processed: int, final_message: str)

##### `stop()`

Stop the automation loop.

##### `create_empty_tmx()`

Create an empty TMX file with proper structure.

Returns:
    True if successful, False otherwise


---

## Functions

### `get_ahk()`

**Line:** 35

Get or create AHK instance lazily

---

