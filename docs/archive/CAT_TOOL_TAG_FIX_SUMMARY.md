# CAT Tool Tag Preservation - Quick Reference

## The Problem (Identified October 7, 2025)

AI models were **omitting** CAT tool formatting placeholder tags during translation:

❌ **BEFORE FIX:**
```
Source:  [1}De uitvoer van de USSR naar de BLEU{2]
Output:  USSR exports to the BLEU  ← Missing tags!
```

✅ **AFTER FIX:**
```
Source:  [1}De uitvoer van de USSR naar de BLEU{2]
Output:  [1}USSR exports to the BLEU{2]  ← Tags preserved!
```

---

## What Are CAT Tool Placeholder Tags?

**Format Examples**: 
- memoQ: `[1}text{2]`
- CafeTran: `|1|text|2|`
- Trados: (various formats)
- Wordfast: (various formats)

**What They Represent**:
- Inline formatting (bold, italic, underline)
- Hyperlinks
- Special characters
- Other formatting elements

**How They Work**:
- CAT tool exports formatting as numbered placeholder tags
- Translator works with plain text + numbered tags
- CAT tool converts tags back to original formatting on re-import

**Critical Rule**: Tags should **move with the content they wrap**, not stay in fixed positions

---

## The Fix

Added explicit instructions to **ALL prompts** in both v2.4.0 and v2.5.0:

### New Instruction Section:
```
**CRITICAL: CAT TOOL TAG PRESERVATION**:
- Source may contain CAT tool formatting tags like [1}, {2], |1|, or other 
  bracketed/special characters
- These are placeholder tags from memoQ, Trados, CafeTran, Wordfast 
  representing formatting (bold, italic, links, etc.)
- PRESERVE ALL tags - if source has tags, target must have same number
- Keep tags with their content: '[1}De uitvoer{2]' → '[1}The exports{2]'
- Tags can reposition if sentence structure changes between languages
- Never translate or omit tags - only reposition appropriately
```

---

## What Changed?

### v2.4.0 - 2 Prompts Updated:
1. ✅ `default_translate_prompt`
2. ✅ `default_proofread_prompt`

### v2.5.0 - 4 Prompts Updated:
1. ✅ `single_segment_prompt`
2. ✅ `batch_docx_prompt`
3. ✅ `batch_bilingual_prompt` ⭐ (Most critical for TXT workflow)
4. ✅ `default_proofread_prompt`

---

## Why This Matters

**Without Proper Tags:**
❌ Translated files can't be re-imported into CAT tools  
❌ Formatting is lost  
❌ Manual tag correction required  
❌ Professional workflow disrupted  

**With Proper Tags:**
✅ Seamless round-trip: CAT tool → Supervertaler → CAT tool  
✅ Formatting preserved  
✅ No manual corrections needed  
✅ Professional workflow intact  

---

## Tag Behavior Examples

### Example 1: Tags Move With Content
```
Source:  [1}De uitvoer van de USSR naar de BLEU{2]
Correct: [1}USSR exports to the BLEU{2]
```
→ Tags wrap the formatted phrase, they move with it

### Example 2: Multiple Tag Pairs
```
Source:  [1}De uitvoer van machines{2] [3}stelt niets voor{4]
Correct: [1}Exports of machinery{2] [3}mean nothing{4]
```
→ Each tag pair wraps its respective content

### Example 3: Tags Can Reposition for Natural Target Language
```
Source:  [1}word A{2] [3}word B{4]
Could become: [3}word B{4] [1}word A{2]
```
→ If target language puts B before A naturally

### Example 4: Empty Tag Pairs
```
Source:  [1}Text{2][3} {4]
Correct: [1}Translation{2][3} {4]
```
→ Empty tag pairs like `[3} {4]` (possibly line breaks or special spaces) must also be preserved

---

## Key Principles

✅ **Tag Count Must Match**: Source has 4 tags → Target must have 4 tags  
✅ **Tags Move With Content**: Keep tags wrapping the same conceptual content  
✅ **Tags Can Reposition**: Adjust for natural target language word order  
✅ **Never Translate Tags**: `[1}` stays `[1}`, never becomes `[1}translated{2]`  
✅ **Never Omit Tags**: All tags must appear in output  
✅ **Various Formats**: Recognize brackets, pipes, or other tag formats  

---

## Technical Notes

### Tag Formats by CAT Tool:

**memoQ**: `[N}...{N]` pattern
- Opening: `[1}`, `[2}`, `[3}`, etc.
- Closing: `{1]`, `{2]`, `{3]`, etc.

**CafeTran**: `|N|...|N|` pattern (from memory)
- Uses pipe symbols as delimiters

**Trados/Wordfast**: (Various formats - to be documented)

### Pairing Rules:
- Tags are typically paired: `[1}` with `{2]`
- Number sequences indicate pairing: 1-2, 3-4, 5-6, etc.
- Empty pairs can exist: `[3} {4]`

---

## Status

✅ **Fixed**: October 7, 2025  
✅ **Versions**: v2.4.0 and v2.5.0  
✅ **Priority**: CRITICAL (breaks CAT tool workflow)  
✅ **Understanding**: Tags are **formatting placeholders**, not segmentation markers  

---

## Related Documentation

📄 **Detailed Analysis**: `docs/bugfixes/BUGFIX_CAT_TOOL_TAG_PRESERVATION_2025-10-07.md`  
📄 **TXT Workflow Guide**: `docs/user_guides/QUICK_START_bilingual_txt_workflow.md`  
📄 **Strategic Direction**: `docs/planning/STRATEGIC_PIVOT_TXT_bilingual_first.md`  

---

**Remember**: Tags represent formatting and should move naturally with the content they format! 🎉
