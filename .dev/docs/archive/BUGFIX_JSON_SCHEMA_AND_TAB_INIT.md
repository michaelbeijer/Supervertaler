# Bug Fixes Round 2: JSON Schema and Tab Initialization

**Date**: October 17, 2025  
**Version**: v3.6.6-beta  
**Issues**: Custom Instructions tab error, JSON schema mismatch, glossary placement

---

## Issues Fixed

### 1. ✅ "Custom Instructions tab not initialized" Error

**Problem**: Clicking "✅ Apply to Project Now" showed error even though tab exists

**Root Cause**: The `apply_custom_instructions()` function checked for `self.custom_instructions_text` widget immediately, but this widget is only created when the "LLM Translation" tab is first visited (lazy initialization)

**Fix**: Added tab initialization logic
```python
def apply_custom_instructions():
    # First ensure the LLM Translation tab is initialized
    if not hasattr(self, 'custom_instructions_text'):
        # Navigate to LLM Translation tab to initialize it
        if hasattr(self, 'notebook'):
            for i in range(self.notebook.index('end')):
                if 'LLM Translation' in self.notebook.tab(i, 'text'):
                    self.notebook.select(i)
                    self.root.update_idletasks()
                    break
        
        # Wait for tab to initialize
        import time
        time.sleep(0.1)
        self.root.update()
    
    # Now check again and apply
    if hasattr(self, 'custom_instructions_text'):
        # ... apply logic
```

**Behavior**:
- First click: Automatically switches to LLM Translation tab and applies
- Subsequent clicks: Works immediately (tab already initialized)

---

### 2. ✅ JSON Schema Mismatch

**Problem**: AI-generated prompts had different structure than existing prompts

**Comparison**:

**OLD Generated Format** (Wrong):
```json
{
  "name": "Patent_Dutch_to_English",
  "domain": "Intellectual Property",
  "task_type": "Translation",
  "version": "1.0",
  "translate_prompt": "As a translator working on Dutch to English...",
  "description": "AI-generated system prompt for Dutch to English translation...",
  "created_at": "2025-10-17T23:07:48.331520",
  "source_language": "Dutch",
  "target_language": "English"
}
```

**Existing Format** (Correct):
```json
{
  "name": "Patent Translation Specialist",
  "description": "Enhanced patent-specific prompts...",
  "domain": "Intellectual Property",
  "version": "2.2.0",
  "task_type": "Translation",
  "created": "2025-09-08 - Supervertaler v2.2.0",
  "modified": "2025-10-16",
  "translate_prompt": "You are an expert {source_lang} to {target_lang} patent translator...",
  "proofread_prompt": ""
}
```

**Key Differences**:
1. ❌ Field order different
2. ❌ `created_at` (ISO timestamp) vs `created` (human-readable date)
3. ❌ `source_language`/`target_language` fields (shouldn't exist - prompts should be reusable!)
4. ❌ Hardcoded language names instead of `{source_lang}` and `{target_lang}` placeholders
5. ❌ Missing `modified` field
6. ❌ Missing `proofread_prompt` field

**NEW Generated Format** (Fixed):
```json
{
  "name": "Patent_Dutch_to_English",
  "description": "AI-generated system prompt for translation in patent domain",
  "domain": "Intellectual Property",
  "version": "1.0",
  "task_type": "Translation",
  "created": "2025-10-17 - AI Generated",
  "modified": "2025-10-17",
  "translate_prompt": "As a translator working on {source_lang} to {target_lang}...",
  "proofread_prompt": ""
}
```

**What Changed**:
```python
# Replace language names with placeholders for reusability
prompt_with_placeholders = system_prompt_text.replace(source_lang, "{source_lang}").replace(target_lang, "{target_lang}")

# Create JSON structure matching existing prompt library schema
prompt_data = {
    "name": default_name,
    "description": f"AI-generated system prompt for translation in {doc_type.lower()} domain",
    "domain": domain,
    "version": "1.0",
    "task_type": "Translation",
    "created": datetime.now().strftime("%Y-%m-%d") + " - AI Generated",
    "modified": datetime.now().strftime("%Y-%m-%d"),
    "translate_prompt": prompt_with_placeholders,
    "proofread_prompt": ""
}
```

**Benefits**:
- ✅ Matches existing prompt structure exactly
- ✅ Prompts are now **reusable** for any language pair (uses placeholders)
- ✅ Compatible with prompt library loader
- ✅ Can be selected and activated like other prompts
- ✅ Proper metadata for searching/filtering

---

### 3. ✅ Glossary Placement Confusion

**Problem**: Glossary was being included in System Prompt (global), but should be in Custom Instructions (project-specific)

**Why it matters**:
- **System Prompt** = Global translation strategy, reusable across projects
- **Custom Instructions** = Project-specific details, including document's actual glossary

**Example**:
- ✅ System Prompt: "Use consistent terminology from provided glossary" (general instruction)
- ✅ Custom Instructions: "voegplaat → joint plate, verankeringsrib → anchoring rib, ..." (actual terms)

**Fix**: Updated prompt generator instructions

**BEFORE** (Wrong):
```
1. SYSTEM PROMPT:
   - CRITICAL: Include a "KEY TERMINOLOGY" section with the bilingual glossary
   - Format glossary as markdown table

2. CUSTOM INSTRUCTIONS:
   - Reference key terms from the glossary with examples
```

**AFTER** (Correct):
```
1. SYSTEM PROMPT:
   - Include translation direction using PLACEHOLDERS: {source_lang} → {target_lang}
   - Specify domain, tone, register GENERALLY (not document-specific)
   - Make it GENERIC and REUSABLE for similar documents
   - Do NOT include specific glossary terms - keep it general
   - Use {source_lang} and {target_lang} placeholders, NOT specific language names

2. CUSTOM INSTRUCTIONS:
   - CRITICAL: Include "KEY TERMINOLOGY" section with complete bilingual glossary
   - Format glossary as markdown table
   - Reference specific key terms with translation examples
   - Document-specific requirements and challenges
```

**Result**: 
- System Prompt is now reusable for any patent document
- Custom Instructions contain the document-specific glossary (25-40 terms)
- Proper separation of concerns

---

## Additional Improvements

### JSON Viewer Tool Created

Created `view_prompt.py` - a command-line tool to view JSON prompts with proper formatting:

```powershell
# View a specific prompt
python view_prompt.py "Patent Translation Specialist.json"

# List all prompts in a folder
python view_prompt.py --list "C:\Dev\Supervertaler\user data_private\System_prompts"
```

**Output Example**:
```
================================================================================
📄 Patent Translation Specialist
================================================================================

📋 METADATA
--------------------------------------------------------------------------------
Description         : Enhanced patent-specific prompts with technical precision
Domain              : Intellectual Property
Version             : 2.2.0
Task Type           : Translation
Created             : 2025-09-08 - Supervertaler v2.2.0
Modified            : 2025-10-16

📝 TRANSLATION PROMPT
--------------------------------------------------------------------------------
You are an expert {source_lang} to {target_lang} patent translator with deep
expertise in intellectual property, technical terminology, and patent law...

Key patent translation principles:
• Maintain technical precision and legal accuracy
• Preserve claim structure and dependency relationships
...
```

### Documentation Created

Created `docs/guides/JSON_EDITORS_AND_HUMAN_READABLE_FORMAT.md` with:
- Recommendations for JSON editors (VS Code, JSONView, Notepad++)
- Proposal to migrate to YAML for better human-readability
- Comparison of JSON vs YAML vs Markdown+YAML
- Migration scripts
- Analysis of custom format ideas

**Key Recommendation**: Use VS Code with built-in JSON formatter (already installed!)

---

## Testing Instructions

### Test 1: Apply Custom Instructions (Tab Initialization)

1. Open Supervertaler
2. **Do NOT navigate to LLM Translation tab yet**
3. Analyze Document → Generate Prompts
4. Click "✅ Apply to Project Now" in Custom Instructions tab
5. **Expected**: 
   - App automatically switches to LLM Translation tab
   - Custom Instructions applied successfully
   - If project loaded: Instructions saved automatically

### Test 2: JSON Schema Compatibility

1. Generate new system prompt from analysis
2. Save as "Test_Prompt"
3. Check file structure matches existing prompts:
   ```powershell
   python view_prompt.py "Test_Prompt.json"
   ```
4. Go to Prompt Library → System Prompts
5. **Expected**: New prompt appears in list
6. Select and activate it
7. **Expected**: Works correctly (no errors)
8. Check prompt text uses `{source_lang}` not "Dutch"

### Test 3: Glossary in Custom Instructions

1. Analyze document with rich terminology
2. Generate Prompts
3. Check **System Prompt tab**: Should be generic, no specific terms
4. Check **Custom Instructions tab**: Should contain full glossary table
5. **Expected distribution**:
   - System Prompt: "Use consistent terminology..." (general)
   - Custom Instructions: "voegplaat → joint plate, deuvel → dowel..." (specific)

---

## Files Changed

1. `Supervertaler_v3.6.0-beta_CAT.py`:
   - Lines 5337-5367: Fixed `apply_custom_instructions()` with tab initialization
   - Lines 5258-5277: Updated JSON schema to match existing format
   - Lines 5094-5116: Moved glossary from System Prompt to Custom Instructions

2. **Created**:
   - `view_prompt.py`: Command-line JSON viewer tool
   - `docs/guides/JSON_EDITORS_AND_HUMAN_READABLE_FORMAT.md`: Documentation

---

## Summary

### ✅ All Issues Fixed

1. **Tab initialization error** → Auto-navigates and initializes tab
2. **JSON schema mismatch** → Now matches existing prompts exactly
3. **Glossary placement** → Moved to Custom Instructions (project-specific)

### 🎯 Key Improvements

- System Prompts are now **reusable** (use `{source_lang}` placeholders)
- Custom Instructions contain **document-specific glossary**
- JSON structure matches **existing prompt library**
- Created tools for **viewing JSON in human-readable format**

### 📝 Next Steps

Consider migrating to **YAML format** in the future for better human-readability:
- No escape sequences needed
- Comments supported
- Industry standard
- Easy migration with provided scripts

For now, use **VS Code** to view/edit JSON prompts with proper formatting!
