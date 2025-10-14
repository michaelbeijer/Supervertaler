# Task Type System - Implementation Specification

**Date:** October 14, 2025  
**Version:** 1.0  
**For:** Supervertaler v3.6.0 (planned)

---

## Overview

Add a **"Task Type"** classification system to the Prompt Library to distinguish between different types of text processing workflows.

---

## Task Types

Standard task types to support:

1. **Translation** - Converting text from one language to another
2. **Localization** - Adapting text for regional/cultural variants (e.g., en-US → en-GB)
3. **Proofreading** - Reviewing and correcting existing translations
4. **QA (Quality Assurance)** - Systematic quality checking
5. **Copyediting** - Improving style and readability
6. **Post-editing** - Refining machine translation output
7. **Transcreation** - Creative adaptation for marketing/advertising
8. **Terminology Extraction** - Identifying key terms for glossaries

---

## Implementation Plan

### Phase 1: Data Structure (v3.6.0)

**1. Add `task_type` field to prompt JSON files:**

```json
{
  "title": "Medical Translation Specialist",
  "version": "1.0",
  "task_type": "Translation",  ← NEW FIELD
  "description": "...",
  "prompt": "..."
}
```

**2. Update Prompt Library UI:**

- Add "Task Type" column to the prompt list (after Title, before Domain)
- Add filter dropdown: "All Tasks" | "Translation" | "Localization" | "Proofreading" | etc.
- Add task type badge/icon in prompt cards
- Sort prompts by task type

**3. Backward Compatibility:**

- If `task_type` field missing → default to "Translation"
- Graceful handling of unknown task types

---

### Phase 2: Localization Workflow (v3.6.0)

**Special handling for Localization task type:**

**memoQ Bilingual Table Integration:**

When processing with a Localization prompt:

1. **Input:** memoQ bilingual DOCX with Source | Target | Comments columns
2. **Processing:** 
   - Keep Source column unchanged
   - Update Target column with localized text
   - Add brief explanation to Comments column (if significant changes made)
3. **Output:** Updated bilingual table ready for reimport

**Comment Format:**
```
Changed: [brief explanation]
Examples:
- "organisation → organization (US spelling)"
- "toll-free → freephone (UK term)"
- "licenced → licensed (UK adjective form)"
```

**Implementation:**

```python
def process_localization_memoq(self, segments, prompt):
    """
    Process segments with localization prompt.
    Updates target text and adds comments about changes.
    """
    for segment in segments:
        # Call LLM with localization prompt
        response = self.call_llm_api(prompt, segment.source)
        
        # Parse response
        localized_text, change_note = self.parse_localization_response(response)
        
        # Update segment
        segment.target = localized_text
        
        # Add change note to comments if significant
        if change_note:
            if segment.notes:
                segment.notes += f"\n{change_note}"
            else:
                segment.notes = change_note
        
        # Update status
        segment.status = "translated"
    
    return segments
```

---

### Phase 3: UI Enhancements (v3.6.0)

**1. Prompt Selection Dialog:**

Add task type filter:
```
┌─ Select Prompt ──────────────────┐
│ Task Type: [Localization ▼]      │
│                                   │
│ ○ Localization - en-US to en-GB │
│ ○ Localization - en-GB to en-US │
│                                   │
│          [Select] [Cancel]        │
└───────────────────────────────────┘
```

**2. Assistant Panel:**

Show active task type:
```
┌─ Assistant ─────────────────────┐
│ Task: Localization              │
│ Prompt: en-US to en-GB          │
│ Model: GPT-4                    │
│                                  │
│ [Translate Selection]           │
└──────────────────────────────────┘
```

**3. Batch Translation Dialog:**

Include task type awareness:
```
┌─ Batch Process ─────────────────┐
│ Task Type: Localization         │
│ Prompt: en-US to en-GB          │
│                                  │
│ ☑ Add change notes to comments  │
│ ☑ Preserve technical terms      │
│                                  │
│ Segments: 1-50                  │
│                                  │
│         [Start] [Cancel]         │
└──────────────────────────────────┘
```

---

## Localization-Specific Features

### Comment Generation

**Automatic change tracking for localizations:**

```python
def generate_localization_comment(source, target, changes):
    """
    Generate concise comment about what was changed.
    
    Args:
        source: Original text
        target: Localized text
        changes: List of (from, to, reason) tuples
    
    Returns:
        Brief comment string
    """
    if not changes or len(changes) == 0:
        return None
    
    if len(changes) == 1:
        from_word, to_word, reason = changes[0]
        return f"{from_word} → {to_word} ({reason})"
    
    elif len(changes) <= 3:
        parts = [f"{f} → {t}" for f, t, _ in changes]
        return f"Changed: {', '.join(parts)}"
    
    else:
        return f"Multiple changes ({len(changes)} items)"
```

### Quality Checks

**For localization tasks, add specific QA:**

- Spell check in target locale
- Terminology consistency check
- Date/number format validation
- Currency symbol check ($ vs £ vs €)

---

## Prompt Library Updates

### New Columns

| Title | Task Type | Domain | Version | Actions |
|-------|-----------|--------|---------|---------|
| Medical Translation | Translation | Medical | 1.0 | Use / Edit |
| en-US to en-GB | Localization | General | 1.0 | Use / Edit |
| Financial Proofreading | Proofreading | Finance | 1.0 | Use / Edit |

### Filter System

```
Task Type: [All ▼] [Translation] [Localization] [Proofreading] [QA]
Domain:    [All ▼] [Medical] [Legal] [Technical] [Finance]
Search:    [____________]
```

---

## Migration Path

### Step 1: Update existing prompts

Add `task_type` field to all existing System Prompts:

```python
# Migration script
def migrate_prompts():
    prompts_dir = "user data/System_prompts/"
    
    for file in os.listdir(prompts_dir):
        if file.endswith('.json'):
            with open(file, 'r') as f:
                data = json.load(f)
            
            # Add task_type if missing
            if 'task_type' not in data:
                data['task_type'] = infer_task_type(data['title'])
            
            with open(file, 'w') as f:
                json.dump(data, f, indent=2)

def infer_task_type(title):
    """Infer task type from prompt title."""
    title_lower = title.lower()
    
    if 'localization' in title_lower or 'localisation' in title_lower:
        return 'Localization'
    elif 'proofread' in title_lower:
        return 'Proofreading'
    elif 'qa' in title_lower or 'quality' in title_lower:
        return 'QA'
    else:
        return 'Translation'  # Default
```

### Step 2: Update UI gradually

1. v3.6.0-alpha: Add task_type field (hidden from UI)
2. v3.6.0-beta: Show task type in Prompt Library
3. v3.6.0-rc: Add filtering and special localization handling
4. v3.6.0-final: Full task type system with all features

---

## Testing Plan

### Test Cases

**1. Localization en-US → en-GB:**
- Input: "The organization will authorize the license."
- Expected: "The organisation will authorise the licence."
- Comment: "Multiple UK spellings: -isation, -ise, licence"

**2. Localization en-GB → en-US:**
- Input: "Services delivered by licenced professionals."
- Expected: "Services delivered by licensed professionals."
- Comment: "licenced → licensed (US form)"

**3. Comment Generation:**
- Test that comments are concise (< 100 chars)
- Test that multiple changes are summarized
- Test that trivial changes don't generate comments

**4. Backward Compatibility:**
- Old prompts without task_type still work
- Custom prompts without task_type default to Translation

---

## Future Enhancements (v3.7.0+)

### Task-Specific Settings

Each task type could have custom settings:

**Translation:**
- Source/target languages
- Formality level
- Domain specialization

**Localization:**
- Regional variant (en-US, en-GB, en-AU, en-CA, etc.)
- Date/number format handling
- Currency conversion
- Measurement units

**Proofreading:**
- Error categories to check
- Severity levels
- Track changes mode

**QA:**
- Checklist items
- Pass/fail criteria
- Report format

### Analytics

Track task type usage:
```
Task Type Distribution (Last 30 Days):
- Translation:   65%
- Localization:  20%
- Proofreading:  10%
- QA:             5%
```

---

## Benefits

✅ **Clear Workflow Distinction** - Users understand what each prompt does  
✅ **Better Organization** - Prompts grouped by purpose  
✅ **Specialized Features** - Task-specific UI and processing  
✅ **Scalability** - Easy to add new task types in future  
✅ **Professional** - Matches CAT tool workflows  

---

## Related Files

- `Localization - en-US to en-GB.json` - US to UK localization prompt
- `Localization - en-GB to en-US.json` - UK to US localization prompt
- Future: Additional localization pairs (en-CA, en-AU, es-ES/es-MX, pt-PT/pt-BR, etc.)

---

**Implementation Timeline:**
- v3.6.0-alpha: Data structure + basic UI (1 week)
- v3.6.0-beta: Full UI + localization workflow (2 weeks)
- v3.6.0-final: Polish + testing + documentation (1 week)
- **Total: ~1 month**
