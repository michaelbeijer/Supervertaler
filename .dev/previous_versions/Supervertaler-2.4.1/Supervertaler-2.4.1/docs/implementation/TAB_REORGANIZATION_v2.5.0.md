# Tab Reorganization - Supervertaler v2.5.0

## What Changed? 📋

### Before (Nested Structure)
```
Translation Workspace Tabs:
├── 📝 Prompts
├── 📁 Projects
├── 🔗 Context (nested sub-tabs)
│   ├── 💾 TM
│   ├── 🖼️ Images
│   └── 📋 Instructions
├── 🤖 MT
├── ✨ LLM
├── 💾 TM (duplicate!)
├── 📚 Glossary
├── 🔒 Non-trans
└── ⚙️ Settings
```

**Problems:**
- ❌ Context tab had nested sub-tabs (extra clicks to access)
- ❌ Two different "TM" tabs with confusing purposes
- ❌ "Prompts" was unclear (system vs user prompts?)
- ❌ "Instructions" was vague

### After (Flat Structure) ✅
```
Translation Workspace Tabs:
├── 📝 System Prompts      (renamed from "Prompts")
├── 📁 Projects
├── 💾 TM Manager          (extracted from Context → TM)
├── 🖼️ Images              (extracted from Context → Images)
├── 📋 Custom Instructions (extracted from Context → Instructions, renamed)
├── 🤖 MT
├── ✨ LLM
├── 🔍 TM Matches          (renamed from "TM" for clarity)
├── 📚 Glossary
├── 🔒 Non-trans
└── ⚙️ Settings
```

**Improvements:**
- ✅ All tabs at the same level (no nesting)
- ✅ Clear distinction between TM tabs:
  - **TM Manager** = Load/manage your TM database
  - **TM Matches** = View matches for current segment
- ✅ Clear naming:
  - **System Prompts** = Pre-built translation prompts
  - **Custom Instructions** = Your personalized guidelines

---

## New Tab Purposes 🎯

### 📝 System Prompts
**Purpose:** Browse and apply pre-built translation prompts  
**Use case:** Select specialized prompts (legal, medical, marketing, etc.)  
**Status:** Working (hierarchical tree view)

### 📁 Projects
**Purpose:** Quick access to recent projects  
**Use case:** Load previous translation projects  
**Status:** Working (shows current project)

### 💾 TM Manager
**Purpose:** Manage Translation Memory database  
**Features:**
- View TM entry count and fuzzy threshold
- Load TMX/TXT files
- Open full TM Manager dialog
- Quick info about TM benefits

**Use case:** Load TM files before starting translation

### 🖼️ Images
**Purpose:** Attach reference images for multimodal AI  
**Features:**
- Select image folder
- Provide visual context to GPT-4 Vision, Claude Vision
- Help AI understand UI elements and layout

**Status:** Coming soon (placeholder UI ready)

### 📋 Custom Instructions
**Purpose:** Provide personalized translation guidelines  
**Features:**
- Rich text editor for instructions
- Style guidelines (formal/informal tone)
- Terminology preferences
- Formatting rules
- Project context

**Use case:** Define consistent translation rules for AI

**Example:**
```markdown
# Custom Translation Instructions

## Style Guidelines:
- Use formal tone (use 'u' instead of 'je' in Dutch)
- Maintain professional business language

## Terminology Preferences:
- Keep technical terms in English unless standard translation exists
- 'user interface' → 'gebruikersinterface' (not 'interface')
- 'dashboard' → 'dashboard' (keep in English)

## Context:
This is a software localization project for a business analytics platform.
Target audience: Business professionals and data analysts.
```

### 🔍 TM Matches
**Purpose:** View TM matches for currently selected segment  
**Features:**
- Shows exact matches (100%)
- Shows fuzzy matches (75%+)
- Quick apply translation from match
- Similarity percentage display

**Use case:** Find and reuse similar translations while working

---

## Answering Your Question: Why Two TM Tabs? 🤔

### Original Design (Confusing)
We had two "TM" tabs because they served different purposes, but the naming made it unclear:

1. **Context → TM** (nested) = TM Management tools
2. **TM** (main level) = TM Matches display

### New Design (Clear)
Now they have distinct names that explain their purpose:

1. **💾 TM Manager** = "I want to configure my TM"
   - Load TM files
   - View statistics
   - Configure settings
   - **Think:** Like opening your TM database

2. **🔍 TM Matches** = "Show me similar translations"
   - View matches for current segment
   - Apply existing translations
   - See similarity scores
   - **Think:** Like search results in your TM database

**Analogy:**
- **TM Manager** = Your music library settings (import songs, organize playlists)
- **TM Matches** = Search results when you look for a song

---

## Technical Changes 🛠️

### Code Changes

**1. Updated Panel Dictionary** (line ~1003):
```python
self.assist_visible_panels = {
    'system_prompts': True,       # NEW NAME
    'projects': True,
    'tm_manager': True,           # NEW (extracted)
    'reference_images': True,     # NEW (extracted)
    'custom_instructions': True,  # NEW (extracted, renamed)
    'mt': True,
    'llm': True,
    'tm_matches': True,          # RENAMED
    'glossary': True,
    'nontrans': True,
    'settings': True
}
```

**2. Created New Tab Functions**:
- `create_tm_manager_tab()` - TM management interface
- `create_reference_images_tab()` - Image attachment (future)
- `create_custom_instructions_tab()` - Rich text instruction editor

**3. Deprecated Old Function**:
- `create_context_tab()` - Marked as deprecated, kept for compatibility

**4. Updated Tabbed Layout** (line ~1050):
- Removed nested Context tab
- Added three separate tabs
- Renamed existing tabs

**5. Updated Stacked Layout** (line ~1113):
- Changed `'tm'` to `'tm_matches'`
- Updated display name to "🔍 TM Matches"

---

## User Benefits 🎁

### Faster Access
**Before:** System Prompts → Click → Context → Click → TM sub-tab = 3 clicks  
**After:** System Prompts → Click = 1 click

### Clearer Purpose
**Before:** "What's the difference between these two TM tabs?"  
**After:** "TM Manager for setup, TM Matches for results - got it!"

### Better Organization
All tabs now have clear, distinct purposes at the same level.

---

## Migration Notes 📌

### For Existing Users
- No project file changes required
- All functionality remains the same
- Just reorganized for better UX

### For Developers
- `create_context_tab()` is deprecated but still exists
- New functions follow same pattern as existing tab creators
- Panel visibility system unchanged

---

## Future Enhancements 🚀

### Custom Instructions Integration
When context-aware translation is implemented (Task #3), custom instructions will be:
- Automatically included in translation prompts
- Saved with project files
- Applied consistently across all segments

### Reference Images
When multimodal AI is implemented:
- Images will be sent to GPT-4 Vision/Claude Vision
- Visual context will improve UI translation quality
- Screenshots can be attached to specific segments

---

## Testing Checklist ✅

- [x] All 11 tabs render correctly
- [x] Tab switching works smoothly
- [x] TM Manager shows entry count
- [x] Custom Instructions text editor works
- [x] Images tab shows "coming soon" message
- [x] Stacked layout uses updated panel names
- [x] No errors in console
- [x] Application launches successfully

---

**Last Updated:** October 5, 2025  
**Version:** 2.5.0  
**Changes By:** GitHub Copilot (requested by user)  
**Status:** ✅ Complete and tested
