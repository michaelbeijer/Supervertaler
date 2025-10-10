# Supervertaler v2.5.0 - CAT Editor Integration Plan

**Date:** October 5, 2025  
**Version:** 2.5.0  
**Status:** In Development

---

## Executive Summary

Supervertaler v2.5.0 represents a major evolution: integrating a full Computer-Aided Translation (CAT) editor into the existing prompt engineering framework. This creates a unified application supporting both:
- **Legacy TXT workflow** - for memoQ/Trados bilingual file processing
- **New DOCX workflow** - direct document translation with embedded CAT editor

---

## Architecture Overview

### Module Structure

```
Supervertaler v2.5.0/
│
├── Supervertaler_v2.5.0.py          # Main application
│
├── modules/                          # NEW: Modular components
│   ├── __init__.py
│   ├── cat_editor_core.py           # CAT editor UI and logic
│   ├── segment_manager.py           # Segment class and management
│   ├── docx_handler.py              # DOCX import/export (from cat_tool_prototype)
│   ├── simple_segmenter.py          # Sentence segmentation (from cat_tool_prototype)
│   └── tag_manager.py               # Inline tag handling (from cat_tool_prototype)
│
└── cat_tool_prototype/              # Original CAT editor (preserved for reference)
    └── cat_editor_prototype.py      # Original standalone version
```

---

## Dual Workflow Design

### Workflow 1: TXT Files (Legacy - for memoQ/Trados)

**USE CASE:** Users working with memoQ or Trados bilingual files

```
INPUT: .txt file (one segment per line)
  ↓
Bilingual File Ingestion
  ↓
AI Translation Engines
  ↓
OUTPUT: .txt + .tmx files
```

**Status:** Fully preserved - no breaking changes

---

### Workflow 2: DOCX Files (NEW - Direct Translation)

**USE CASE:** Direct document translation without external CAT tools

```
INPUT: .docx file
  ↓
DOCXHandler.extract_segments()
  ↓
CAT Editor opens (embedded panel/tab)
  ↓
User reviews segmentation
  ↓
[OPTIONAL] AI-Assisted Pre-Translation
  │  ↓
  │  User configures prompts (Supervertaler UI)
  │  ↓
  │  AI translates all segments
  │  ↓
  │  Results auto-populate in CAT editor grid
  ↓
User reviews/edits translations
  ↓
DOCXHandler.apply_translations()
  ↓
OUTPUT: .docx file with formatting preserved
```

**Key Innovation:** "AI-Assisted Pre-Translation" - brings LLM power to CAT workflow

---

## User Interface Integration

### Main Application: Supervertaler v2.5.0

#### Menu Structure

```
File
├── Import TXT File (legacy)
├── Import DOCX File (NEW)
├── Export Output
├── ─────────────
├── Save Project
├── Load Project
└── Exit

CAT Editor (NEW)
├── Open CAT Editor
├── Close CAT Editor
├── ─────────────
├── AI-Assisted Pre-Translation
└── Export Translated DOCX

Tools
├── Translation Mode
├── Proofreading Mode
├── ─────────────
├── Browse Tracked Changes
└── Manage Translation Memory

Settings
├── API Keys
├── Custom Prompts
├── Advanced System Prompts
└── Preferences
```

#### Layout: Embedded CAT Editor

```
┌─────────────────────────────────────────────────────────┐
│ Supervertaler v2.5.0                    [Menu] [Toolbar]│
├───────────────────────┬─────────────────────────────────┤
│                       │                                 │
│  PROMPT ENGINEERING   │  INFO PANEL                     │
│  PANEL                │                                 │
│                       │  (Existing Supervertaler UI)    │
│  (Existing UI)        │                                 │
│                       │                                 │
├───────────────────────┴─────────────────────────────────┤
│                                                         │
│  CAT EDITOR PANEL (NEW - toggleable)                    │
│  ┌────────────────────────────────────────────────┐    │
│  │ [Grid/Split/Document] [AI Pre-Translate]       │    │
│  ├────┬──────────────────┬──────────────────┬─────┤    │
│  │ ID │ Source           │ Target           │ Stat│    │
│  ├────┼──────────────────┼──────────────────┼─────┤    │
│  │ 1  │ Hello world      │ [Edit here]      │ 🔴  │    │
│  │ 2  │ How are you?     │ Comment ça va?   │ 🟢  │    │
│  └────┴──────────────────┴──────────────────┴─────┘    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  LOG PANEL (shared between both workflows)              │
└─────────────────────────────────────────────────────────┘
```

---

## Integration Points

### 1. Segment Management

**Class:** `Segment` (from cat_editor_prototype.py)

```python
class Segment:
    def __init__(self, seg_id, source, target="", status="untranslated"):
        self.id = seg_id
        self.source = source
        self.target = target
        self.status = status  # untranslated, draft, translated, approved
        # ... additional metadata
```

**Integration:** Segments become the universal data structure for both workflows

---

### 2. AI Translation Bridge

**NEW Class:** `AIPreTranslationAgent`

```python
class AIPreTranslationAgent:
    """Bridge between Supervertaler's AI engines and CAT editor segments"""
    
    def __init__(self, translation_agent, log_queue):
        self.agent = translation_agent  # GeminiTranslationAgent, etc.
        self.log_queue = log_queue
    
    def pretranslate_segments(self, segments: List[Segment], 
                             source_lang: str, 
                             target_lang: str,
                             custom_instructions: str = "") -> List[Segment]:
        """
        Send segments to AI for translation
        Returns updated segments with translations in .target field
        """
        # Extract source texts
        source_texts = [seg.source for seg in segments]
        
        # Call Supervertaler's translation engine
        translations = self.agent.translate_batch(
            source_texts, 
            source_lang, 
            target_lang,
            custom_instructions
        )
        
        # Update segments
        for seg, translation in zip(segments, translations):
            seg.target = translation
            seg.status = "draft"  # Mark as AI-generated draft
            seg.modified = True
        
        return segments
```

---

### 3. DOCX Import/Export

**Existing Classes** (from cat_tool_prototype):
- `DOCXHandler` - Extract segments from DOCX, apply translations back
- `SimpleSegmenter` - Sentence boundary detection
- `TagManager` - Handle inline formatting tags

**Integration:** These become shared modules in `modules/` folder

---

## Implementation Steps

### Phase 1: Refactoring (Preparation)
1. ✅ Create `modules/` folder
2. ✅ Extract core classes from `cat_editor_prototype.py`:
   - `Segment`, `LayoutMode` → `segment_manager.py`
   - `CATEditorApp` → `cat_editor_core.py`
3. ✅ Copy supporting files:
   - `docx_handler.py` → `modules/`
   - `simple_segmenter.py` → `modules/`
   - `tag_manager.py` → `modules/`

### Phase 2: Core Integration
4. ✅ Create `Supervertaler_v2.5.0.py` (copy from v2.4.0)
5. ✅ Add CAT editor imports
6. ✅ Create `AIPreTranslationAgent` class
7. ✅ Update menu system
8. ✅ Add CAT editor panel to UI

### Phase 3: DOCX Workflow
9. ✅ Add "Import DOCX" button
10. ✅ Implement DOCX → Segments → CAT editor flow
11. ✅ Add "AI-Assisted Pre-Translation" button
12. ✅ Connect AI engines to segment translation
13. ✅ Implement "Export Translated DOCX"

### Phase 4: Testing & Documentation
14. ✅ Test TXT workflow (ensure no regression)
15. ✅ Test DOCX workflow end-to-end
16. ✅ Update CHANGELOG.md
17. ✅ Update user documentation

---

## Key Features

### AI-Assisted Pre-Translation

**What it does:**
Traditional CAT tools use basic MT (Google Translate, DeepL) for pre-translation. Supervertaler brings **contextual LLM translation** to the CAT workflow:

1. User imports DOCX → segments appear in CAT editor grid
2. User clicks "AI-Assisted Pre-Translation"
3. Supervertaler prompt engineering UI appears:
   - Select AI provider (Gemini/Claude/OpenAI)
   - Configure custom instructions
   - Add TM matches
   - Add tracked changes context
   - Set advanced system prompts
4. AI translates all segments considering full document context
5. Translations auto-populate in grid with "draft" status
6. User reviews and edits as needed
7. Export to DOCX with formatting intact

**Advantage over traditional CAT tools:**
- Full document context awareness
- Custom domain prompts
- Multiple AI providers
- TM integration
- Tracked changes learning

---

## Backward Compatibility

### TXT Workflow Preservation

**Guarantee:** All existing v2.4.0 functionality remains identical

- Import TXT files → works as before
- Translation/Proofreading modes → unchanged
- TMX generation → unchanged
- Custom prompts → unchanged
- Project management → unchanged

**Implementation:** No changes to existing classes:
- `BilingualFileIngestionAgent`
- `TMAgent`
- `GeminiTranslationAgent`, `ClaudeTranslationAgent`, `OpenAITranslationAgent`
- `OutputGenerationAgent`

---

## Technical Considerations

### Module Dependencies

```python
# Supervertaler_v2.5.0.py imports:
from modules.segment_manager import Segment, LayoutMode
from modules.cat_editor_core import CATEditorApp
from modules.docx_handler import DOCXHandler
from modules.simple_segmenter import SimpleSegmenter
from modules.tag_manager import TagManager
```

### State Management

- **TXT mode:** Uses existing state variables (self.txt_data, etc.)
- **CAT mode:** New state variables (self.cat_segments, self.cat_editor)
- **Shared:** Log queue, API keys, translation agents

---

## Success Criteria

### Must Have
- ✅ TXT workflow works identically to v2.4.0
- ✅ DOCX import → segmentation → CAT editor
- ✅ AI-assisted pre-translation functional
- ✅ DOCX export with translations
- ✅ All existing features preserved

### Nice to Have
- 🎯 Seamless switching between TXT and CAT modes
- 🎯 Save CAT projects (segments + translations)
- 🎯 Integration with existing project management
- 🎯 Quality metrics for AI translations

---

## Version Timeline

- **v2.4.0** - Current (Prompt engineering + TXT workflow)
- **v2.5.0** - Target (+ CAT editor integration)
- **v3.0.0** - Future (Full workflow automation?)

---

## Questions & Decisions

### Resolved
- ✅ UI integration: Embedded panel (not separate window)
- ✅ DOCX workflow: Import → CAT editor → AI pre-translate → Export
- ✅ Module organization: New `modules/` folder
- ✅ Version: New file `Supervertaler_v2.5.0.py`

### Open Questions
- ⏳ Should CAT editor projects be separate from Supervertaler projects?
- ⏳ How to handle very large DOCX files (memory management)?
- ⏳ Should we support XLSX (Excel) files in future?

---

## Conclusion

This integration represents a paradigm shift: combining **prompt engineering power** with **CAT tool workflow**. Users get the best of both worlds:
- Professional translators: Familiar CAT interface with AI superpowers
- Casual users: Direct DOCX translation without learning CAT tools
- Power users: Full control over prompts + segment-level editing

**Next Step:** Begin Phase 1 refactoring - create modules and extract core classes.

---

*Document created: October 5, 2025*  
*Author: Michael Beijer + GitHub Copilot*
