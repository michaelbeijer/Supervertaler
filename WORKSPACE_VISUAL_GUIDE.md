# Translation Workspace - Quick Visual Guide

## Tab Overview

```
┌────────────────────────────────────────────────────────────────┐
│  TRANSLATION WORKSPACE                            [⊞ Stacked]  │
├────────────────────────────────────────────────────────────────┤
│ [📝 Prompts] [📁 Projects] [🔗 Context] [🤖 MT] [✨ LLM]       │
│ [💾 TM] [📚 Glossary] [🔒 Non-trans] [⚙️ Settings]             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  (Active tab content displays here)                            │
│                                                                 │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Tab Groups

### 📚 LIBRARY & MANAGEMENT
```
┌─ 📝 Prompts ──────────────────────────────────────┐
│  • Select translation style/domain                 │
│  • Standard, Legal, Medical, Technical             │
│  • Edit and create custom prompts                  │
└────────────────────────────────────────────────────┘

┌─ 📁 Projects ──────────────────────────────────────┐
│  • Quick access to recent projects                 │
│  • Project statistics and progress                 │
│  • One-click project loading                       │
└────────────────────────────────────────────────────┘

┌─ 🔗 Context ───────────────────────────────────────┐
│  • TM: Translation Memory management               │
│  • Images: Reference images (future)               │
│  • Instructions: Custom AI instructions            │
└────────────────────────────────────────────────────┘
```

### 🤖 TRANSLATION ASSISTANCE
```
┌─ 🤖 MT ────────────────────────────────────────────┐
│  Machine Translation suggestions                   │
│  (Google, DeepL, Microsoft, Amazon)                │
└────────────────────────────────────────────────────┘

┌─ ✨ LLM ───────────────────────────────────────────┐
│  LLM Translation with AI models                    │
│  (GPT-4, Claude, Gemini)                           │
└────────────────────────────────────────────────────┘

┌─ 💾 TM ────────────────────────────────────────────┐
│  Translation Memory matches                        │
│  (Exact and fuzzy matches with %)                  │
└────────────────────────────────────────────────────┘

┌─ 📚 Glossary ──────────────────────────────────────┐
│  Terminology database                              │
│  (Approved terms and definitions)                  │
└────────────────────────────────────────────────────┘

┌─ 🔒 Non-trans ─────────────────────────────────────┐
│  Non-translatables                                 │
│  (Names, brands, code, etc.)                       │
└────────────────────────────────────────────────────┘
```

### ⚙️ CONFIGURATION
```
┌─ ⚙️ Settings ──────────────────────────────────────┐
│  • LLM Provider: OpenAI / gpt-4o                   │
│  • Language Pair: English → Dutch                  │
│  • Preferences:                                    │
│    ☑ Include context                               │
│    ☑ Check TM before API                           │
│    ☐ Auto-propagate matches                        │
└────────────────────────────────────────────────────┘
```

## Typical Workflows

### Workflow 1: Starting a New Project
```
1. Click "📁 Projects" tab
   └─> Browse Projects → Select DOCX file

2. Click "⚙️ Settings" tab
   └─> Verify: Language Pair, LLM Provider

3. Click "📝 Prompts" tab
   └─> Select domain-specific prompt (e.g., "Legal Translation")

4. Click "🔗 Context" tab → "TM" sub-tab
   └─> Load TM File (if you have existing translations)

5. Start translating!
   └─> TM matches appear automatically in "💾 TM" tab
   └─> Click "✨ LLM" tab to get AI translations
```

### Workflow 2: Quick Translation Session
```
1. Click "📁 Projects" tab
   └─> Double-click recent project

2. Check "💾 TM" tab
   └─> See how many TM entries loaded

3. Select segment
   └─> TM matches show automatically if available
   └─> Press Ctrl+T to translate with AI

4. Review suggestions
   └─> "💾 TM" tab: Translation memory matches
   └─> "✨ LLM" tab: AI-generated alternatives
   └─> "🤖 MT" tab: Machine translation options
```

### Workflow 3: Customizing Translation Style
```
1. Click "📝 Prompts" tab
   └─> Browse available prompts
   └─> Select "Marketing Translation" for creative content

2. Click "🔗 Context" tab → "Instructions" sub-tab
   └─> Add custom instructions:
       "Keep brand names in English"
       "Use casual, friendly tone"
       "Target audience: young adults"

3. Click "⚙️ Settings" tab
   └─> Enable "☑ Include context" for better AI understanding

4. Translate!
   └─> AI uses your prompt + instructions + context
```

## Tab Navigation Tips

### Keyboard Shortcuts
- **Ctrl+Tab**: Next tab
- **Ctrl+Shift+Tab**: Previous tab
- **Alt+1** to **Alt+9**: Jump to tab 1-9 (future enhancement)

### Visual Indicators
- **Green bold text** (🎯): Currently active item
- **Colored info boxes**: Category-specific (blue=TM, orange=Images, purple=Instructions)
- **Emoji icons**: Quick visual identification

### Layout Modes
- **Tabbed View** (default): All tabs in notebook, one visible at a time
- **Stacked View**: All panels visible, vertically stacked with scroll
  - Click "⊞ Stacked View" button to toggle

## Tab Color Coding

Each tab has a thematic color scheme:

```
📝 Prompts    → Blue (#e3f2fd)    - Information, knowledge
📁 Projects   → Green (#e8f5e9)   - Active, growing
🔗 Context    → 
   TM         → Blue (#e3f2fd)    - Data, structure
   Images     → Orange (#fff3e0)  - Visual, creative
   Instructions → Purple (#f3e5f5) - Custom, special
⚙️ Settings   → Grey (#f0f0f0)    - Neutral, functional
```

## What Each Tab Does

### 📝 Prompts
**When to use**: Before starting translation, when changing domains
**Why**: Sets the AI's "personality" and translation style

### 📁 Projects
**When to use**: Opening projects, checking progress
**Why**: Quick access without File menu navigation

### 🔗 Context
**When to use**: Loading resources, adding domain knowledge
**Why**: Improves translation quality with external context

### 🤖 MT
**When to use**: Want quick machine translation
**Why**: Fast, free alternatives to AI (no API costs)

### ✨ LLM
**When to use**: Need high-quality AI translation
**Why**: Best quality, context-aware, style-matching

### 💾 TM
**When to use**: Automatically activated for all segments
**Why**: Reuse previous translations, ensure consistency

### 📚 Glossary
**When to use**: Technical terms, industry jargon
**Why**: Enforce approved terminology

### 🔒 Non-trans
**When to use**: Names, brands, code snippets
**Why**: Prevent AI from translating what shouldn't be translated

### ⚙️ Settings
**When to use**: Setup, troubleshooting, preference changes
**Why**: All configuration in one place

## Quick Reference Card

```
╔══════════════════════════════════════════════════════╗
║ TRANSLATION WORKSPACE QUICK REFERENCE                ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  SETUP (do once per project)                        ║
║  ├─ 📁 Projects: Open project                       ║
║  ├─ ⚙️ Settings: Check language pair               ║
║  ├─ 📝 Prompts: Select domain style                 ║
║  └─ 🔗 Context: Load TM, add instructions           ║
║                                                      ║
║  TRANSLATE (do for each segment)                    ║
║  ├─ 💾 TM: Check for existing matches               ║
║  ├─ ✨ LLM: Get AI translation (Ctrl+T)            ║
║  ├─ 🤖 MT: Compare with machine translation         ║
║  └─ 📚 Glossary: Verify terminology                 ║
║                                                      ║
║  ADJUST (as needed)                                 ║
║  ├─ 📝 Prompts: Change style mid-project            ║
║  ├─ 🔗 Instructions: Update custom notes            ║
║  └─ ⚙️ Settings: Toggle preferences                 ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

## Tips for Efficiency

### 1. **Tab Pinning** (Future Enhancement)
Pin frequently used tabs for quick access

### 2. **Tab Memory**
App remembers last active tab between sessions

### 3. **Multi-Monitor Setup**
Undock panels to separate window (future enhancement)

### 4. **Quick Actions**
Most tabs have action buttons at bottom for common tasks

### 5. **Status Indicators**
Tabs show badges for counts (e.g., "💾 TM (1,247)" - future)

## Comparison: Old vs New

### OLD (v2.4.0)
```
Menus only:
File → Open → Navigate → Select → OK
Translate → API Settings → Configure → OK
Translate → Custom Prompts → Edit → OK
Translate → Load TM → Navigate → OK

Result: 15+ clicks to set up
```

### NEW (v2.5.0)
```
Tabs:
Projects tab → Double-click
Settings tab → Glance at config
Prompts tab → Click prompt
Context tab → Already shows TM count

Result: 3 clicks to set up
```

**Improvement**: **80% fewer clicks** for common workflows!

---

**File**: `WORKSPACE_VISUAL_GUIDE.md`
**Date**: October 5, 2025
**For**: Supervertaler v2.5.0 users
