# Style Guides Integration into Translation Workflow

## Current Architecture Overview

### How System Prompts & Custom Instructions Work Now

```
┌─────────────────────────────────────────────────────────────┐
│              get_context_aware_prompt()                     │
│                                                              │
│  Base Prompt (mode-specific):                               │
│  • single_segment_prompt                                    │
│  • batch_docx_prompt                                        │
│  • batch_bilingual_prompt                                   │
│                    ↓                                         │
│  + Custom Instructions (if active)                          │
│                    ↓                                         │
│  = COMBINED PROMPT for AI                                   │
│                                                              │
│  Sent to: preview_combined_prompt()                         │
│           translate operations                              │
└─────────────────────────────────────────────────────────────┘
```

**Current Flow:**
1. User selects system prompt (or uses default)
2. User optionally activates custom instructions
3. At translate time: `get_context_aware_prompt()` combines them
4. Result is sent to AI + used in preview

---

## Proposed Style Guides Integration

### Design Principles

1. **Non-intrusive** - Style guides are optional
2. **Project-scoped** - Selected per project/task
3. **Additive** - Added to prompt hierarchy (not replacing anything)
4. **Activatable** - Can be toggled on/off
5. **Composable** - Can combine multiple guides
6. **Contextual** - Can be language-specific

---

## Architecture: Three-Level Prompt Hierarchy

```
┌──────────────────────────────────────────────────────────────┐
│           UNIFIED INTEGRATED PROMPT STRUCTURE                │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  LEVEL 1: BASE SYSTEM PROMPT (mode-specific)                 │
│  └─ single_segment_prompt / batch_docx_prompt / etc.        │
│                                                               │
│  LEVEL 2: CUSTOM INSTRUCTIONS (optional, user-added)        │
│  └─ active_custom_instruction (if selected)                 │
│                                                               │
│  LEVEL 3: STYLE GUIDES (NEW - optional, project-specific)   │
│  └─ active_style_guide (if selected for project)            │
│     └─ Language-specific formatting rules                    │
│     └─ Terminology & consistency guidance                    │
│                                                               │
│  COMPOSITION BREAKDOWN (shown in preview):                   │
│  • System Prompt: 2,500 chars                                │
│  • Custom Instructions: 1,200 chars                          │
│  • Style Guide: 800 chars ← NEW                              │
│  • TOTAL: 4,500 chars                                        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Data Structure & Storage

**1.1 Track Active Style Guide**

Add to Supervertaler `__init__`:
```python
# Style guide configuration
self.active_style_guide = None          # Selected style guide content
self.active_style_guide_name = None     # Display name
self.active_style_guide_language = None # Which language guide is active
self.active_style_guide_format = "markdown"  # How it's formatted
```

**1.2 Store Selection in Project File**

When saving project, include:
```json
{
  "project_metadata": {
    "active_style_guide_name": "Dutch",
    "active_style_guide_format": "markdown"
  }
}
```

When loading project, restore the selection.

---

### Phase 2: UI Components

**2.1 Style Guide Selector (in main toolbar)**

Add button/dropdown near "System Prompt" selector:
```
[System Prompt: Translation Specialist] [Custom Instr: None] [Style Guide: Dutch ▼]
                                                              ↑ NEW
```

**2.2 Selection Dialog**

When clicking style guide dropdown:
- Show list of available languages
- Show preview of each
- Allow "None" / "Off"
- Remember last selection

**2.3 Update Preview Panel**

In `preview_combined_prompt()`, add style guide section:
```
📋 Composition:
  • System Prompt (Translation Specialist): 2,500 chars
  • Custom Instructions (Preserve Formatting): 1,200 chars
  • Style Guide (Dutch): 800 chars ← NEW
  • Total prompt length: 4,500 chars
```

---

### Phase 3: Integration into Prompt System

**3.1 Modify `get_context_aware_prompt()`**

Current:
```python
def get_context_aware_prompt(self, mode: str = "single") -> str:
    base_prompt = [select base prompt]
    
    # Append Custom Instructions if active
    if self.active_custom_instruction:
        combined_prompt = base_prompt + "\n\n" + "# CUSTOM INSTRUCTIONS\n\n" + self.active_custom_instruction
        return combined_prompt
    
    return base_prompt
```

New:
```python
def get_context_aware_prompt(self, mode: str = "single") -> str:
    base_prompt = [select base prompt]
    
    # Append Custom Instructions if active
    if self.active_custom_instruction:
        combined_prompt = base_prompt + "\n\n" + "# CUSTOM INSTRUCTIONS\n\n" + self.active_custom_instruction
    else:
        combined_prompt = base_prompt
    
    # APPEND STYLE GUIDE IF ACTIVE (NEW)
    if self.active_style_guide:
        combined_prompt += "\n\n" + "# STYLE GUIDE & FORMATTING RULES\n\n" + self.active_style_guide
    
    return combined_prompt
```

**Result:** Style guide automatically included in all translation operations!

---

### Phase 4: UI Methods to Add

**4.1 Show Style Guide Selector**

```python
def show_style_guide_selector(self):
    """Show dialog to select style guide for current project"""
    dialog = tk.Toplevel(self.root)
    dialog.title("Select Style Guide")
    dialog.geometry("500x400")
    
    # List of available guides
    guides = self.style_guide_library.get_all_languages()
    
    # Show radiobuttons for each
    selected = tk.StringVar(value=self.active_style_guide_name or "None")
    
    tk.Label(dialog, text="Select style guide for this project:").pack(pady=10)
    
    tk.Radiobutton(dialog, text="None (No style guide)",
                   variable=selected, value="None").pack(anchor='w')
    
    for guide_name in guides:
        tk.Radiobutton(dialog, text=guide_name,
                       variable=selected, value=guide_name).pack(anchor='w')
    
    def apply_selection():
        if selected.get() == "None":
            self.active_style_guide = None
            self.active_style_guide_name = None
            self.active_style_guide_language = None
            self.log("✓ Style guide deactivated")
        else:
            lang = selected.get()
            self.active_style_guide = self.style_guide_library.get_guide_content(lang)
            self.active_style_guide_name = lang
            self.active_style_guide_language = lang
            self.log(f"✓ Style guide activated: {lang}")
        
        dialog.destroy()
        self.update_prompt_info_label()  # Update display
    
    tk.Button(dialog, text="Apply", command=apply_selection).pack(pady=10)
```

**4.2 Update Preview to Show Style Guide**

```python
def preview_combined_prompt(self):
    # ... existing code ...
    
    # Composition breakdown - ADD STYLE GUIDE
    composition_text = "📋 Composition:\n"
    base_prompt_name = getattr(self, 'active_translate_prompt_name', 'Default')
    composition_text += f"  • System Prompt ({base_prompt_name}): {len(self.current_translate_prompt)} characters\n"
    
    if hasattr(self, 'active_custom_instruction') and self.active_custom_instruction:
        custom_name = getattr(self, 'active_custom_instruction_name', 'Custom')
        composition_text += f"  • Custom Instructions ({custom_name}): {len(self.active_custom_instruction)} characters\n"
    
    # STYLE GUIDE - NEW
    if hasattr(self, 'active_style_guide') and self.active_style_guide:
        style_guide_name = getattr(self, 'active_style_guide_name', 'Style Guide')
        composition_text += f"  • Style Guide ({style_guide_name}): {len(self.active_style_guide)} characters\n"
    
    composition_text += f"  • Total prompt length: {len(prompt)} characters"
```

---

## Usage Example

### User Workflow

1. **Load Project**
   - Opens existing translation project
   - Restores previously selected style guide

2. **Select Style Guide** (if not already set)
   - Clicks "Style Guide: Dutch ▼"
   - Dialog shows: Dutch, English, Spanish, German, French
   - Selects "Dutch"
   - UI confirms: "✓ Style guide activated: Dutch"

3. **Preview Prompt**
   - Clicks "🧪 Preview Prompt"
   - Shows:
     - System Prompt (2,500 chars)
     - Custom Instructions (1,200 chars)
     - **Style Guide (800 chars)** ← Included
   - Total: 4,500 chars

4. **Translate**
   - User selects segment
   - Clicks "Translate"
   - AI receives FULL prompt including style guide
   - Formatting follows Dutch style guide rules

---

## Benefits of This Design

### ✅ For Users
- Style guides automatically applied to all translations
- No need to remember formatting rules
- Consistency enforced by AI
- Quick toggle between guides per project

### ✅ For Architecture
- Minimal code changes (15-20 lines in core method)
- Follows existing pattern (like custom instructions)
- Non-breaking change
- Modular and extensible

### ✅ For Future
- Easy to add more style guides
- Can support industry-specific templates
- Ready for multi-guide compositions
- Can add conditional style guide inclusion

---

## Implementation Checklist

### Stage 1: Data Structure (15 min)
- [ ] Add `self.active_style_guide` instance variables
- [ ] Initialize in `__init__`
- [ ] Add to project save/load

### Stage 2: Core Integration (20 min)
- [ ] Modify `get_context_aware_prompt()`
- [ ] Add check for active style guide
- [ ] Format as markdown section

### Stage 3: UI Components (30 min)
- [ ] Add selector button/dropdown
- [ ] Create selection dialog
- [ ] Update preview panel
- [ ] Add log messages

### Stage 4: Testing (20 min)
- [ ] Test style guide selection
- [ ] Verify prompt includes guide
- [ ] Test preview display
- [ ] Test project save/load

**Total Implementation Time:** ~85 minutes

---

## Code Locations to Modify

1. **`__init__` method** (line ~750)
   - Add instance variables for active guide

2. **`get_context_aware_prompt()` method** (line 907)
   - Add style guide appending logic

3. **`preview_combined_prompt()` method** (line 5577)
   - Add style guide to composition breakdown
   - Add style guide text to preview

4. **Project save/load methods**
   - Include style guide selection in project data

5. **Toolbar creation** (line ~1969)
   - Add style guide selector UI

---

## Questions to Consider

1. **Multiple Style Guides?**
   - Should we support combining multiple guides (e.g., Dutch + Terminology)?
   - Current proposal: Single active guide per project
   - Future: Could be extended to multi-guide

2. **Style Guide Formatting in Prompt?**
   - Should it say "# STYLE GUIDE & FORMATTING RULES" or "# STYLE GUIDE (Dutch)"?
   - Should it include metadata about the guide?
   - Current proposal: Clear section header with language name

3. **Conditional Inclusion?**
   - Should style guide be included based on task type?
   - E.g., "Only include for translation, not for proofreading"
   - Current proposal: Simple toggle, same for all tasks

4. **User Customization?**
   - Can users edit the active guide for the project?
   - Or should it always be read-only from library?
   - Current proposal: Read-only, edit via Style Guides tab

---

## Next Steps

Would you like me to proceed with implementing this design? I recommend:

1. **Start with Phase 1-2**: Get data structure and UI selector working
2. **Then Phase 3**: Integrate into `get_context_aware_prompt()`
3. **Then Phase 4**: UI methods and preview updates
4. **Finally**: Testing and refinement

Should I go ahead with implementation?
