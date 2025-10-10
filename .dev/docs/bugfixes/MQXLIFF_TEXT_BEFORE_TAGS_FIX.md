# MQXLIFF Text Before Tags Fix

**Date**: October 9, 2025  
**Issue**: Text appearing BEFORE formatting tags was being lost  
**Status**: 🔧 In Progress

## Problem Analysis

### The Issue

When translating segments with text before formatting tags, the text was being lost:

**Source**:
```xml
<source>Pagano started his career at <bpt...>Atalanta</bpt>.</source>
```

**Expected Target** (with translation):
```xml
<target>Pagano begon zijn carrière bij <bpt...>Atalanta</bpt>.</target>
```

**Actual Target** (BROKEN):
```xml
<target><bpt...>Atalanta</bpt>.</target>
```

The text "Pagano started his career at " is **MISSING**!

### Root Cause

The `_clone_with_translation()` method was:
1. Cloning all child elements (formatting tags) ✓
2. NOT copying the `source_elem.text` (text before first child) ❌
3. Trying to use `_replace_all_text_content()` to replace text

But `_replace_all_text_content()` does string replacement like:
```python
element.text = element.text.replace(source_text, translation)
```

This doesn't work when:
- `source_text` = "Pagano started his career at Atalanta."
- `element.text` = "Pagano started his career at "
- `child[N].text` = "Atalanta"

The full source text is SPLIT across multiple text nodes, so replace() can't find it!

## Attempted Solutions

### Attempt 1: Copy source_elem.text
Added `target_elem.text = source_elem.text` before cloning children.

**Result**: Text before tags was preserved, but still same text as source (no translation)

### Attempt 2: Clear all text and place translation in root
Strategy: Put entire translation in `target_elem.text`, clear all child text nodes.

**Problem**: Cleared `<bpt>` tag content which contains formatting codes like `&lt;hlnk...&gt;`, breaking the structure!

### Attempt 3: Smart node detection
Try to detect "content" vs "formatting" text nodes and only clear content.

**Problem**: Too complex, hard to distinguish. Still broke the formatting tags.

### Attempt 4: Revert to _replace_all_text_content()
Go back to the replacement approach but fix the core issue.

**Current Status**: Working on this approach...

## The Real Solution Needed

The fundamental problem is that `replace(old, new)` doesn't work when `old` is split across multiple nodes.

We need to:
1. Collect ALL content text from all nodes (skipping `<bpt>`/`<ept>` internal formatting codes)
2. Concatenate it to verify it matches source_text  
3. Replace with translation
4. **Redistribute** the translation back to the SAME node positions with SAME proportions

Example:
- Source nodes: ["Pagano started his career at " (70%), "Atalanta" (25%), "." (5%)]
- Source text: "Pagano started his career at Atalanta."
- Translation: "Pagano begon zijn carrière bij Atalanta."
- Distribute: 
  - Node 1 (70%): "Pagano begon zijn carrière bij " 
  - Node 2 (25%): "Atalanta"
  - Node 3 (5%): "."

**OR** simpler approach:
- Always place ENTIRE translation in the FIRST content node
- Clear all other content nodes
- BUT preserve `<bpt>`/`<ept>` internal text which is formatting metadata

## Next Steps

1. Implement text redistribution logic
2. Test with segment 15 (Atalanta case)
3. Test with segment 16 (complex multi-hyperlink case)
4. Verify formatting codes in `<bpt>` tags are preserved

---

**Status**: Investigation in progress, multiple approaches tested, solution being refined.
