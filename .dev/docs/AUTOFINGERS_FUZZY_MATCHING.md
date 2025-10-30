# AutoFingers Fuzzy Matching Feature

**Feature Status:** ✅ Implemented and Tested  
**Date:** October 29, 2025  
**Version:** AutoFingers v2.0 (with fuzzy matching)

---

## 🎯 Overview

**Fuzzy Matching** is a new feature for AutoFingers that enables **fallback translation lookup** when segments contain formatting tags that prevent exact matching.

### The Problem You Had

Your segment in memoQ:
```
"The on-site user can disconnect by clicking the ￼Disconnect￼ button in the remote assistance toolbar on the Console device."
```

In TMX (with tags):
```
en: The on-site user can disconnect by clicking the [1}Disconnect{2] button in the remote assistance toolbar on the Console device.
nl: De gebruiker op locatie kan de verbinding verbreken door op de knop [1}Disconnect{2] te klikken in de werkbalk voor externe assistentie op het Console-apparaat.
```

**What happened before:** AutoFingers skipped this segment because the exact text with tags `[1}Disconnect{2]` wasn't in the TM.

**What happens now:** AutoFingers finds a **97% fuzzy match** and automatically inserts it (unconfirmed).

---

## ✨ Key Features

### 1. **Automatic Fuzzy Fallback**
When AutoFingers doesn't find a 100% exact match, it searches for similar translations using fuzzy matching.

**Algorithm:** SequenceMatcher similarity ratio (Python's `difflib`)
- Compares text structure and content
- Normalized to 0.0 (no match) to 1.0 (perfect match)
- Configurable threshold (default: 80%)

### 2. **Best Match Selection**
Returns the single best matching translation instead of multiple options.
- Faster (scans entire TM once)
- Simpler (no popup dialogs)
- Cleaner (one decision point per segment)

### 3. **Unconfirmed Insertion (Key Feature)**
Fuzzy matches are **inserted but NOT auto-confirmed**:
- ✅ Translation appears in target field
- ❌ Segment remains unconfirmed
- 📝 Translator sees what was inserted
- ✏️ Can edit before confirmation
- ⏭️ AutoFingers continues to next segment

**Result:** Translator can review decisions quickly without pausing.

### 4. **Match Type Tracking**
Distinguishes between exact and fuzzy matches in logging:
```
[100% exact] Source text → Target translation
[97% fuzzy] Source text (unconfirmed) → Target translation
```

---

## 🔧 Configuration

### Basic Settings

```python
engine = AutoFingersEngine(
    tmx_file="my_translation.tmx",
    source_lang="en",
    target_lang="nl"
)

# Enable/disable fuzzy matching
engine.enable_fuzzy_matching = True

# Similarity threshold (0.0 to 1.0)
# Default: 0.80 (80%)
# Lower = more matches, but lower quality
# Higher = fewer matches, but higher quality
engine.fuzzy_threshold = 0.80

# Auto-confirm fuzzy matches?
# False (default) = insert but don't confirm
# True = insert AND confirm (rare use case)
engine.auto_confirm_fuzzy = False

# Skip segments with no match?
# False (default) = pause for manual translation
# True = skip segment and continue
engine.skip_no_match = False
```

### Recommended Thresholds

| Threshold | Use Case | Behavior |
|-----------|----------|----------|
| **0.70** | Very flexible, catch distant matches | Catches many fuzzy matches, more review needed |
| **0.80** | **Recommended (default)** | Good balance of recall and precision |
| **0.85** | More conservative | Fewer false positives, misses some valid matches |
| **0.90** | Very strict | Only very similar matches, highest confidence |

---

## 📊 How It Works: Step-by-Step

### Scenario: Segment with Tags

**memoQ source field:**
```
The on-site user can disconnect by clicking the ￼Disconnect￼ button...
```

**AutoFingers workflow:**

1. **Copy source to clipboard** (contains tags: `[1}Disconnect{2]`)
2. **Search for exact match**
   - Looks for: `"The on-site user can ... [1}Disconnect{2] button ..."`
   - Result: ❌ Not found (tags prevent exact matching)

3. **Search for fuzzy match** (fuzzy_threshold=0.80)
   - Compares against all TM entries
   - Finds: `"The on-site user can ... Disconnect button ..."`
   - Similarity: **97%** (very high!)
   - Result: ✅ Match found

4. **Insert translation**
   - Pastes Dutch translation to target field
   - Status: **Unconfirmed** (not auto-confirmed)
   - Log: `[97% fuzzy] The on-site user ... → De gebruiker op locatie ...`

5. **Continue workflow**
   - Moves to **next segment** automatically
   - Translator sees inserted text briefly
   - Can review if needed (optional)

---

## 🚀 Usage Examples

### Example 1: Basic Usage (Recommended)

```python
from modules.autofingers_engine import AutoFingersEngine

# Setup
engine = AutoFingersEngine(
    tmx_file="my_project.tmx",
    source_lang="en",
    target_lang="nl"
)

# Load translations
success, msg = engine.load_tmx()
print(msg)  # "Loaded 1,234 translation units"

# Process single segment
print("Switch to memoQ and press Enter...")
input()

success, msg = engine.process_single_segment()
if success:
    print(f"✓ {msg}")
else:
    print(f"✗ {msg}")
```

### Example 2: Batch Processing with Fuzzy Matching

```python
# Configure for batch processing
engine.fuzzy_threshold = 0.80        # Find similar matches
engine.auto_confirm_fuzzy = False    # Don't auto-confirm
engine.skip_no_match = True          # Skip segments with no match

# Process 100 segments
print("Starting batch processing in 5 seconds...")
time.sleep(5)

count, msg = engine.process_multiple_segments(max_segments=100)
print(f"Processed {count} segments: {msg}")
```

### Example 3: Conservative Matching

```python
# Only accept very high-confidence fuzzy matches
engine.fuzzy_threshold = 0.90        # 90%+ similarity required

# For segments with no match at all:
# Option A: Skip them
engine.skip_no_match = True

# Option B: Pause for manual translation
engine.skip_no_match = False

# Process and let translator review any paused segments
```

### Example 4: Programmatic Match Checking

```python
# Check what match would be found
source_text = "Your segment text here"
result = engine.lookup_translation(source_text)

if result:
    print(f"Match found:")
    print(f"  Translation: {result.translation}")
    print(f"  Type: {result.match_type}")  # "exact" or "fuzzy"
    print(f"  Confidence: {result.match_percent}%")
else:
    print("No match found")
```

---

## 📋 Return Value Structure

### TranslationMatch (Named Tuple)

```python
class TranslationMatch(NamedTuple):
    translation: str      # The actual translation text
    match_type: str       # "exact" or "fuzzy"
    match_percent: int    # 100 for exact, 0-99 for fuzzy
```

### Example

```python
result = engine.lookup_translation("Hello world with tags")

# Access results:
result.translation    # "Hola mundo con etiquetas"
result.match_type     # "fuzzy"
result.match_percent  # 85
```

---

## 🧪 Testing Your Configuration

Run the test suite to verify fuzzy matching works:

```bash
cd c:\Dev\Supervertaler
python test_autofingers_fuzzy.py
```

**Output shows:**
- ✅ Exact matches still work perfectly
- ✅ Fuzzy matches find 80%+ similar translations
- ✅ Threshold configuration is flexible
- ✅ No-match behavior respects skip_no_match setting

---

## 🎓 Understanding Match Percentages

### Exact Matches (100%)

- **Requirement:** Source text **identical** to TM entry
- **Auto-confirm:** Yes (instant, no translator review needed)
- **Confidence:** 100% - This is the exact translation

### Fuzzy Matches (80-99%)

Your example: **97% match**
```
TM entry:    "The on-site user ... Disconnect button ..."
Your text:   "The on-site user ... [1}Disconnect{2] button ..."
Match %:     97% (only the tags differ)
```

- **Requirement:** Source text **similar** to TM entry (above threshold)
- **Auto-confirm:** No (translator reviews)
- **Confidence:** 97% - Very likely correct, but translator confirms

### Low Matches (< 80%, not used)

- **Requirement:** Similarity below threshold
- **Action:** No match used, either skip or pause
- **Confidence:** Not confident enough to use

---

## 💡 Best Practices

### 1. **Set Appropriate Threshold**
- **Start with 0.80** (80%) - good default
- **Test with your data** - run test_autofingers_fuzzy.py
- **Adjust if needed:**
  - Too many skips? Lower to 0.75
  - Too many false matches? Raise to 0.85

### 2. **Monitor Match Quality**
- Check log messages for `[fuzzy]` matches
- Review what percentage they are
- If too many low-confidence matches, raise threshold

### 3. **Workflow Strategy**
```
Option A (Recommended): 
  skip_no_match = True, 
  auto_confirm_fuzzy = False
  → Fuzzy inserted unconfirmed, then continue
  → No exact matches skipped, translator reviews fuzzy
  
Option B (Conservative):
  skip_no_match = True, 
  fuzzy_threshold = 0.90
  → Only use 90%+ matches
  → Lower risk of mistakes
  
Option C (Maximum Automation):
  skip_no_match = True, 
  auto_confirm_fuzzy = True
  → Auto-confirm all fuzzy matches too
  → Fastest but requires trust in TM quality
```

### 4. **Handle Tags Consistently**
- TMX should match how memoQ exports tags
- Common formats: `[1}text{2]`, `<1>text</1>`, `{1}text{2}`
- Fuzzy matching ignores tag differences automatically

---

## 🔍 Troubleshooting

### Problem: "No fuzzy matches found"
**Cause:** Threshold too high for your TM  
**Solution:** 
```python
engine.fuzzy_threshold = 0.75  # Lower threshold
# Try again
```

### Problem: "Too many fuzzy matches, low quality"
**Cause:** Threshold too low  
**Solution:**
```python
engine.fuzzy_threshold = 0.85  # Raise threshold
# Try again
```

### Problem: "Segments skipped even though similar text in TM"
**Cause:** `skip_no_match = True` and no fuzzy matches above threshold  
**Solution:**
- Lower fuzzy_threshold, OR
- Set `skip_no_match = False` to pause instead (slower but catches more)

### Problem: "Still not finding tags with differences"
**Cause:** Tags are too different (e.g., `[1}text{2]` vs `<1>text</1>`)  
**Solution:** Manually edit your TMX to use consistent tag format

---

## 📈 Performance Notes

- **Fuzzy matching is O(n):** Scans all TM entries once
- **For 10,000 entries:** Takes ~100-200ms per lookup
- **Acceptable for:** Manual batch processing (1-2 segments per minute)
- **Not suitable for:** Real-time context menu lookups (too slow)

---

## 🔄 Workflow Summary

### Your Exact Use Case

**Before (without fuzzy matching):**
```
AutoFingers: Looking for exact match...
AutoFingers: Not found. Skipping segment.
(You manually translate this segment)
```

**After (with fuzzy matching):**
```
AutoFingers: Looking for exact match...
AutoFingers: Not found. Trying fuzzy match (80%+ threshold)...
AutoFingers: Found 97% match! Inserting...
(Translation appears in target field, unconfirmed)
AutoFingers: Moving to next segment
(You quickly review the fuzzy match and confirm or edit)
```

---

## 📚 Related Files

- **Implementation:** `modules/autofingers_engine.py`
- **Tests:** `test_autofingers_fuzzy.py`
- **Documentation:** This file (AUTOFINGERS_FUZZY_MATCHING.md)
- **Example TMX:** See `test_autofingers_fuzzy.py` for test TMX format

---

## ✅ Checklist: Setting Up Fuzzy Matching

- [ ] Update AutoFingers to latest version (with TranslationMatch class)
- [ ] Read this documentation
- [ ] Run `test_autofingers_fuzzy.py` to verify it works
- [ ] Determine your threshold (start with 0.80)
- [ ] Configure engine settings:
  ```python
  engine.enable_fuzzy_matching = True
  engine.fuzzy_threshold = 0.80
  engine.auto_confirm_fuzzy = False
  engine.skip_no_match = True
  ```
- [ ] Test with your real TMX file
- [ ] Monitor log output for match percentages
- [ ] Adjust threshold if needed
- [ ] Deploy and use in production

---

**Questions?** Check the test file for working examples of all features.

