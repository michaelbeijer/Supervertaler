# Final Fixes: Glossary and Tab Initialization

**Date**: October 17, 2025  
**Issues**: Empty glossary table, tab initialization error

---

## Issues Fixed

### 1. ✅ Empty Glossary Table

**Problem**: The Custom Instructions only showed the header row, no actual glossary data

**Root Cause**: The AI prompt generator wasn't being explicit enough about copying the complete glossary table

**Fix**: Made the instructions much more explicit and demanding:

**BEFORE**:
```
- CRITICAL: Include a "KEY TERMINOLOGY" section with the complete bilingual glossary
- Format glossary as a markdown table
```

**AFTER**:
```
- CRITICAL REQUIREMENT: You MUST include a "KEY TERMINOLOGY" section with the COMPLETE bilingual glossary table from the analysis above
- The glossary table is in the analysis - copy it EXACTLY and completely (all rows)
- Format: Use the same markdown table format as in the analysis (| Dutch term | English equivalent | Notes |)
- DO NOT summarize or truncate the glossary - include ALL terms from the analysis
```

This should force the AI to actually copy the full table instead of just referencing it.

---

### 2. ✅ Tab Initialization Error

**Problem**: "Custom Instructions tab not initialized" error when clicking "Apply to Project Now"

**Root Cause - Confusion**: 
- I initially thought "LLM Translation" was a main notebook tab
- It's actually a **collapsible panel in the Assistant sidebar**!
- The `custom_instructions_text` widget is created in `create_prompt_library_tab()` (line 4648)
- This function is only called when the **Prompt Library** panel is first expanded

**What "LLM Translation" Actually Is**:
- **"✨ LLM Translation"** = Collapsible panel in Assistant sidebar (for AI translation of segments)
- **"📚 Prompt Library"** = Collapsible panel containing Custom Instructions widget

**Fix**: Create the widget directly if it doesn't exist

```python
def apply_custom_instructions():
    # Ensure the custom_instructions_text widget exists
    if not hasattr(self, 'custom_instructions_text'):
        # Create a temporary frame and initialize the tab
        temp_frame = tk.Frame(self.root)
        self.create_prompt_library_tab(temp_frame)
        temp_frame.destroy()  # Keep widget, discard frame
        
        if not hasattr(self, 'custom_instructions_text'):
            messagebox.showerror("Error", 
                "Could not initialize widget.\\n\\n"
                "Please open the Prompt Library panel first.")
            return
    
    # Apply the instructions
    self.custom_instructions_text.delete('1.0', tk.END)
    self.custom_instructions_text.insert('1.0', custom_instructions_text)
    ...
```

**Behavior**:
- First click: Creates the widget invisibly, then applies
- Should work without errors now

---

## Understanding the UI Structure

Since there was confusion, here's the actual layout:

```
Supervertaler Window
├── Workspace (left side)
│   └── Main Notebook Tabs:
│       ├── 📊 Translation Workspace
│       ├── 📄 Document View  
│       └── 📈 QA & Stats
│
└── Assistant Sidebar (right side)
    └── Collapsible Panels:
        ├── 🗂️ Projects
        ├── 📚 Prompt Library ⬅️ Contains Custom Instructions widget
        │   ├── System Prompts (global reusable prompts)
        │   └── Custom Instructions (project-specific text area)
        ├── 🤖 Machine Translation
        ├── ✨ LLM Translation ⬅️ NOT where Custom Instructions lives!
        ├── 💼 TM Matches
        ├── 📖 Glossary
        ├── 🖼️ Images
        ├── 🤖 AI Assistant ⬅️ Where document analysis happens
        ├── 📄 PDF Rescue
        ├── 🚫 Non-Translatables
        ├── 📝 Tracked Changes
        ├── ⚙️ Settings
        └── 📋 Log
```

**Key Point**: 
- **Custom Instructions text area** lives in **"📚 Prompt Library"** panel
- **NOT** in "✨ LLM Translation" panel

---

## About YAML Migration

You asked: "I would actually like to migrate to YAML as soon as possible. Should we sort this mess out first?"

**My Recommendation**: ✅ **Yes, fix current issues first, THEN migrate to YAML**

**Reason**: 
- The JSON schema issues are now fixed
- Glossary should now populate correctly
- Tab initialization should work
- **Once everything works with JSON**, migration to YAML will be straightforward
- Don't want to debug two things at once!

**YAML Migration Plan** (after current fixes work):

### Phase 1: Preparation (1 hour)
1. Install PyYAML: `pip install pyyaml`
2. Test the conversion script (in docs/guides)
3. Convert a few test prompts manually
4. Verify they work

### Phase 2: Update Code (2-3 hours)
1. Update `modules/prompt_library.py` to load both `.json` and `.yaml`
2. Modify `load_all_prompts()` to check file extension
3. Add YAML parsing alongside JSON parsing
4. Test with mixed formats

### Phase 3: Migration (30 minutes)
1. Run conversion script on all JSON prompts
2. Keep JSON files as backup
3. Test all prompts work
4. Remove JSON files when confident

### Phase 4: New Prompt Generation (1 hour)
1. Update AI prompt generator to create YAML instead of JSON
2. Update save functions
3. Test full workflow

**Total Time**: ~5 hours of dev work

**Benefits**:
- ✅ Much more readable
- ✅ No more `\n` escaping
- ✅ Comments supported
- ✅ Industry standard
- ✅ Can still keep JSON for compatibility

---

## Testing Instructions

### Test 1: Glossary Inclusion

1. Restart Supervertaler
2. Analyze a document (use your PVET patent)
3. Verify analysis shows glossary with 25-40 terms
4. Click "🎯 Generate Prompts"
5. Check Custom Instructions tab
6. **Expected**: Should now show FULL glossary table with all rows

**If still empty**: 
- Copy the analysis result
- Check if glossary table is actually in the analysis
- If yes, it's an AI parsing issue
- If no, the analysis itself needs fixing

### Test 2: Apply to Project

1. After generating prompts
2. Click "✅ Apply to Project Now"
3. **Expected**: 
   - No error message
   - Custom Instructions applied successfully
   - If project loaded: Instructions saved

**If still shows error**:
- Try opening "📚 Prompt Library" panel manually first
- Then try "Apply to Project Now" again

---

## Files Changed

- `Supervertaler_v3.6.0-beta_CAT.py`:
  - Lines 5349-5366: Fixed apply_custom_instructions() to create widget if needed
  - Lines 5111-5120: Made glossary requirement much more explicit

---

## Next Steps

1. **Test the fixes** (glossary + apply button)
2. **If working**: Start planning YAML migration
3. **If not working**: Diagnose what's still wrong
4. **Long term**: Migrate to YAML for better human-readability

The path forward is clear - just need to verify these fixes work!
