# Style Guides Integration - Visual Architecture

## Current Prompt Flow (Before Style Guides)

```
TRANSLATION OPERATION
    ↓
select_segment() / translate_segment()
    ↓
get_context_aware_prompt(mode="single")
    ↓
    ┌─────────────────────────────────────┐
    │  BASE SYSTEM PROMPT                 │
    │  (selected by user or mode-based)   │
    │                                     │
    │  "You are a translator..."          │
    │  "Translate the following text..."  │
    │  ... 2,500 characters ...           │
    └─────────────────────────────────────┘
    ↓
    IF active_custom_instruction EXISTS:
    ├─ APPEND custom instructions
    │  ┌──────────────────────────────────┐
    │  │  # CUSTOM INSTRUCTIONS            │
    │  │                                  │
    │  │  "Preserve formatting..."        │
    │  │  "Maintain terminology..."       │
    │  │  ... 1,200 characters ...        │
    │  └──────────────────────────────────┘
    └─→ COMBINED PROMPT
    ↓
SEND TO AI
    ↓
AI TRANSLATION

RESULT: System Prompt + Custom Instructions
```

---

## NEW: Prompt Flow (With Style Guides)

```
TRANSLATION OPERATION
    ↓
select_segment() / translate_segment()
    ↓
get_context_aware_prompt(mode="single")
    ↓
    ┌─────────────────────────────────────┐
    │  LEVEL 1: BASE SYSTEM PROMPT        │
    │  (selected by user or mode-based)   │
    │                                     │
    │  "You are a translator..."          │
    │  "Translate the following text..."  │
    │  ... 2,500 characters ...           │
    └─────────────────────────────────────┘
    ↓
    IF active_custom_instruction EXISTS:
    ├─ LEVEL 2: APPEND CUSTOM INSTRUCTIONS
    │  ┌──────────────────────────────────┐
    │  │  # CUSTOM INSTRUCTIONS            │
    │  │                                  │
    │  │  "Preserve formatting..."        │
    │  │  "Maintain terminology..."       │
    │  │  ... 1,200 characters ...        │
    │  └──────────────────────────────────┘
    └─→ INTERMEDIATE PROMPT
    ↓
    IF active_style_guide EXISTS:    ← NEW!
    ├─ LEVEL 3: APPEND STYLE GUIDE
    │  ┌──────────────────────────────────┐
    │  │  # STYLE GUIDE & FORMATTING      │
    │  │  (Dutch)                         │
    │  │                                  │
    │  │  • Use en-dashes for ranges      │
    │  │  • Numbers: comma = thousands    │
    │  │  • Currency: €1.000,00           │
    │  │  • Abbreviations: with periods   │
    │  │  • Gender-inclusive language     │
    │  │  ... 800 characters ...          │
    │  └──────────────────────────────────┘
    └─→ FINAL COMBINED PROMPT
    ↓
SEND TO AI
    ↓
AI TRANSLATION with:
✓ System instruction
✓ Custom rules
✓ Style guide formatting  ← ENFORCED BY AI

RESULT: System Prompt + Custom Instructions + Style Guide
```

---

## User Interface Flow

### Before: Prompt Selection Only

```
┌─ Toolbar ──────────────────────────────────┐
│ [System Prompt: Translation Specialist ▼] │
│                    ↑                       │
│         Only system prompt shown          │
└────────────────────────────────────────────┘
```

### After: Three-Level Selection

```
┌─ Toolbar ──────────────────────────────────────────────────────────┐
│ [System: Translator ▼] [Custom: None ▼] [Style: Dutch ▼]          │
│                                          ↑ NEW                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## Preview Panel Updates

### Before: System + Custom Only

```
┌─ 🧪 Complete Prompt Preview ──────────────────────────┐
│                                                        │
│ 💡 This is the EXACT prompt that will be sent to AI  │
│                                                        │
│ 📋 Composition:                                        │
│   • System Prompt (Translation Specialist): 2,500 chars
│   • Custom Instructions (Preserve Formatting): 1,200  │
│   • Total prompt length: 3,700 characters             │
│                                                        │
│ ────────────────────────────────────────────────────  │
│ You are an expert translator...                       │
│ [Full prompt text shown here]                         │
│ # CUSTOM INSTRUCTIONS                                 │
│ Preserve formatting...                                │
└────────────────────────────────────────────────────────┘
```

### After: System + Custom + Style

```
┌─ 🧪 Complete Prompt Preview ──────────────────────────┐
│                                                        │
│ 💡 This is the EXACT prompt that will be sent to AI  │
│                                                        │
│ 📋 Composition:                                        │
│   • System Prompt (Translation Specialist): 2,500 chars
│   • Custom Instructions (Preserve Formatting): 1,200  │
│   • Style Guide (Dutch): 800 characters ← NEW         │
│   • Total prompt length: 4,500 characters             │
│                                                        │
│ ────────────────────────────────────────────────────  │
│ You are an expert translator...                       │
│ [Full prompt text shown here]                         │
│ # CUSTOM INSTRUCTIONS                                 │
│ Preserve formatting...                                │
│ # STYLE GUIDE & FORMATTING RULES                      │
│ Dutch Formatting Rules:                               │
│ • Use en-dashes for ranges...                         │
└────────────────────────────────────────────────────────┘
```

---

## Project Data Structure

### Before: Project File

```json
{
  "project_metadata": {
    "source_language": "English",
    "target_language": "Dutch",
    "active_system_prompt_name": "Translation Specialist",
    "active_custom_instruction_name": "Preserve Formatting"
  },
  "segments": [...]
}
```

### After: Project File (With Style Guide)

```json
{
  "project_metadata": {
    "source_language": "English",
    "target_language": "Dutch",
    "active_system_prompt_name": "Translation Specialist",
    "active_custom_instruction_name": "Preserve Formatting",
    "active_style_guide_name": "Dutch",        ← NEW
    "active_style_guide_language": "Dutch",    ← NEW
    "active_style_guide_format": "markdown"    ← NEW
  },
  "segments": [...]
}
```

---

## Data Flow Diagram

### Complete Prompt Building Process

```
┌─────────────────────────────────────────────────────────────────┐
│ When User Translates Segment:                                   │
│                                                                 │
│ 1. translate_current_segment() called                           │
│    ↓                                                            │
│ 2. get_context_aware_prompt() gathers all prompt components    │
│    ├─ Select base prompt (system)                              │
│    │  ├─ Read: self.current_translate_prompt                   │
│    │  └─ Source: System Prompts Library                         │
│    │                                                            │
│    ├─ Check custom instructions (if active)                    │
│    │  ├─ Read: self.active_custom_instruction                  │
│    │  └─ Source: Custom Instructions Library                   │
│    │                                                            │
│    └─ Check style guide (if active) ← NEW                      │
│       ├─ Read: self.active_style_guide                         │
│       └─ Source: Style Guides Library                          │
│    ↓                                                            │
│ 3. Combine all three into single prompt string                 │
│    └─ Append with clear section headers                        │
│    ↓                                                            │
│ 4. Return combined prompt                                       │
│    ↓                                                            │
│ 5. Send to AI API                                              │
│    ↓                                                            │
│ 6. AI processes with full context (system + custom + style)   │
│    ↓                                                            │
│ 7. Translation result respects all three levels                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Instance Variables to Add

### In `__init__` method (~line 750)

```python
# Current (System & Custom Prompts)
self.current_translate_prompt = None          # Active system prompt content
self.active_translate_prompt_name = None      # Name for display
self.active_custom_instruction = None         # Active custom instruction content
self.active_custom_instruction_name = None    # Name for display

# NEW (Style Guides)
self.active_style_guide = None                # Active style guide content
self.active_style_guide_name = None           # Name for display (e.g., "Dutch")
self.active_style_guide_language = None       # Language of guide
self.active_style_guide_format = "markdown"   # Format type
```

---

## Code Change: Core Method

### Modified `get_context_aware_prompt()` at line 907

**Before:**
```python
def get_context_aware_prompt(self, mode: str = "single") -> str:
    """Get translation prompt with Custom Instructions if active"""
    
    # Select base prompt
    base_prompt = self._select_base_prompt(mode)
    
    # Append Custom Instructions if active
    if hasattr(self, 'active_custom_instruction') and self.active_custom_instruction:
        combined_prompt = base_prompt + "\n\n" + "# CUSTOM INSTRUCTIONS\n\n" + self.active_custom_instruction
        return combined_prompt
    
    return base_prompt
```

**After:**
```python
def get_context_aware_prompt(self, mode: str = "single") -> str:
    """Get translation prompt with Custom Instructions + Style Guide if active"""
    
    # Select base prompt
    base_prompt = self._select_base_prompt(mode)
    combined_prompt = base_prompt
    
    # Append Custom Instructions if active
    if hasattr(self, 'active_custom_instruction') and self.active_custom_instruction:
        combined_prompt += "\n\n" + "# CUSTOM INSTRUCTIONS\n\n" + self.active_custom_instruction
    
    # APPEND STYLE GUIDE IF ACTIVE (NEW)
    if hasattr(self, 'active_style_guide') and self.active_style_guide:
        style_guide_header = f"# STYLE GUIDE & FORMATTING RULES ({self.active_style_guide_language})"
        combined_prompt += "\n\n" + style_guide_header + "\n\n" + self.active_style_guide
    
    return combined_prompt
```

**Difference:** 
- +7 lines of code
- +1 new condition
- No breaking changes
- Follows same pattern as custom instructions

---

## Selector UI Mockup

### Style Guide Dropdown Dialog

```
┌─ Select Style Guide for Project ─────────────────┐
│                                                  │
│  Select style guide to apply to all translations:
│                                                  │
│  ◉ None (No style guide)                         │
│  ○ Dutch                                         │
│  ○ English                                       │
│  ○ Spanish                                       │
│  ○ German                                        │
│  ○ French                                        │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │ Preview:                                 │   │
│  │ Dutch Formatting Guide                   │   │
│  │ • Use en-dashes for ranges (–)           │   │
│  │ • Numbers: comma=thousands (1.000,00)    │   │
│  │ • Currency: € (no space before amount)   │   │
│  │ • 800 characters total                   │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│                         [Apply] [Cancel]        │
└──────────────────────────────────────────────────┘
```

---

## Prompt Size Comparison

### With Just System Prompt
```
System Prompt: 2,500 chars
Total: 2,500 chars
```

### System + Custom Instructions
```
System Prompt: 2,500 chars
Custom Instructions: 1,200 chars
Total: 3,700 chars
```

### System + Custom + Style Guide (NEW)
```
System Prompt: 2,500 chars
Custom Instructions: 1,200 chars
Style Guide: 800 chars
Total: 4,500 chars

[+22% additional context]
```

**Note:** Still well within token limits for OpenAI (typically 4,000-128,000 tokens available)

---

## Task Types Support

### Applies to All Tasks
```
TRANSLATION
├─ Single Segment: Gets style guide ✓
├─ Batch DOCX: Gets style guide ✓
└─ Batch Bilingual: Gets style guide ✓

PROOFREADING
└─ Gets style guide ✓

COPYWRITING
└─ Gets style guide ✓

Any task using get_context_aware_prompt()
└─ Automatically gets style guide ✓
```

---

## Key Benefits

### For Consistency
```
❌ Without Style Guide:
   - User must remember formatting rules
   - AI may not follow conventions
   - Inconsistent across segments

✓ With Style Guide:
   - Rules embedded in every prompt
   - AI explicitly instructed on formatting
   - Consistent across all segments
```

### For Workflow
```
❌ Without:
   - User reviews AI output for formatting issues
   - Manual corrections needed
   - Back-and-forth with AI

✓ With Style Guide:
   - Formatting correct from first attempt
   - Faster review cycle
   - Higher confidence in AI output
```

---

## Summary

The style guide integration follows the **existing pattern** of custom instructions:

1. **Data Storage** - Instance variables store active guide content
2. **Project Persistence** - Saved/loaded with project
3. **UI Selection** - User selects via dropdown
4. **Automatic Application** - Included in every translate operation
5. **Transparent** - Visible in preview but users don't manually edit

**Result:** Seamless integration that feels like a natural part of Supervertaler's prompt management system.
