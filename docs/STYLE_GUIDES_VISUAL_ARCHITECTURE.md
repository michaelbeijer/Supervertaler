# 🎨 Style Guides Feature - Visual Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SUPERVERTALER APPLICATION                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │           ASSISTANT PANEL (Right side of app)               │   │
│  ├──────────────────────────────────────────────────────────────┤   │
│  │                                                               │   │
│  │  ┌─────┬────────┬──────────────┬────────────────────────┐   │   │
│  │  │ 🤖  │ 📝    │ 💬          │ 📖 STYLE ← NEW!     │   │   │
│  │  │ Asst│ Prompts│ Custom      │                      │   │   │
│  │  │ Panel│       │ Instruct    │                      │   │   │
│  │  └─────┴────────┴──────────────┴────────────────────────┘   │   │
│  │                         Tab Notebook                         │   │
│  │                                                               │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │              STYLE GUIDES TAB (NEW)                   │  │   │
│  │  ├────────────────────────────────────────────────────────┤  │   │
│  │  │                                                         │  │   │
│  │  │  ┌────────────────┐  ┌─────────────────────────────┐  │  │   │
│  │  │  │  LEFT PANEL    │  │   RIGHT PANEL              │  │  │   │
│  │  │  │  (List)        │  │   (Content + Chat)         │  │  │   │
│  │  │  ├────────────────┤  ├─────────────────────────────┤  │  │   │
│  │  │  │                │  │  TOP RIGHT:                 │  │  │   │
│  │  │  │ 🔄 Refresh    │  │  ┌──────────────────────┐   │  │  │   │
│  │  │  │                │  │  │  Content Viewer      │   │  │  │   │
│  │  │  │ ┌────────────┐ │  │  │  (Editable)          │   │  │  │   │
│  │  │  │ │ Dutch      │ │  │  │                      │   │  │  │   │
│  │  │  │ │ 10/21 ✓    │ │  │  │  [Save] [Export]     │   │  │  │   │
│  │  │  │ ├────────────┤ │  │  └──────────────────────┘   │  │  │   │
│  │  │  │ │ English    │ │  │                             │  │  │   │
│  │  │  │ │ 10/21 ✓    │ │  │  BOTTOM RIGHT:              │  │  │   │
│  │  │  │ ├────────────┤ │  │  ┌──────────────────────┐   │  │  │   │
│  │  │  │ │ Spanish    │ │  │  │  Chat History        │   │  │  │   │
│  │  │  │ │ 10/21 ✓    │ │  │  │                      │   │  │  │   │
│  │  │  │ ├────────────┤ │  │  │  [You]: Add this to  │   │  │  │   │
│  │  │  │ │ German     │ │  │  │  Dutch guide         │   │  │  │   │
│  │  │  │ │ 10/21 ✓    │ │  │  │                      │   │  │  │   │
│  │  │  │ ├────────────┤ │  │  │  [AI]: Done! Added   │   │  │  │   │
│  │  │  │ │ French     │ │  │  │                      │   │  │  │   │
│  │  │  │ │ 10/21 ✓    │ │  │  └──────────────────────┘   │  │  │   │
│  │  │  │ └────────────┘ │  │                             │  │  │   │
│  │  │  │                │  │  [Input] [Send]             │  │  │   │
│  │  │  │ Scrollable     │  │                             │  │  │   │
│  │  │  └────────────────┘  └─────────────────────────────┘  │  │   │
│  │  │                                                        │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  │                                                               │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                 BACKEND SERVICES                             │   │
│  ├──────────────────────────────────────────────────────────────┤   │
│  │                                                               │   │
│  │  ┌──────────────────────┐      ┌──────────────────────┐     │   │
│  │  │  StyleGuideLibrary   │◄────►│   PromptAssistant   │     │   │
│  │  │  (NEW MODULE)        │      │   (Existing)        │     │   │
│  │  └──────────────────────┘      └──────────────────────┘     │   │
│  │           │                              │                   │   │
│  │           │                              │                   │   │
│  │           ▼                              ▼                   │   │
│  │  ┌──────────────────────┐      ┌──────────────────────┐     │   │
│  │  │  User Data Path      │      │   LLM Clients        │     │   │
│  │  │  Style_Guides/       │      │   (OpenAI, Anthropic)     │   │
│  │  │  ├─ Dutch.md         │      └──────────────────────┘     │   │
│  │  │  ├─ English.md       │                                   │   │
│  │  │  ├─ Spanish.md       │      ┌──────────────────────┐     │   │
│  │  │  ├─ German.md        │      │  ConfigManager       │     │   │
│  │  │  └─ French.md        │      │  (Existing)          │     │   │
│  │  └──────────────────────┘      └──────────────────────┘     │   │
│  │                                                               │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER WORKFLOWS                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │

WORKFLOW 1: Browse and Edit Guide
───────────────────────────────────
User selects                      App loads                   User can
"Dutch" in list  ─────────────►  from disk  ────────────►  read/edit
    │                               │                            │
    └─────────────────────┬─────────┴────────────────────────────┘
                          │
                          ▼
                     Display in
                     content view

WORKFLOW 2: Add to Single Guide
─────────────────────────────────
User pastes             User selects              AI processes        Guide
company standard   ──►  "Add to Dutch"  ───────►  integration   ──►  updated
    │                                                │
    └────────────────────────────────────────────────┘
                        Chat Interface

WORKFLOW 3: Add to All Guides
──────────────────────────────
User pastes              User clicks          AI suggests         All 5
new standard    ───►  "Add to All"  ───────►  how to merge  ─►  guides
    │                                             │                updated
    └─────────────────────────────────────────────┘
                  Chat Interface

WORKFLOW 4: Import External File
──────────────────────────────────
User selects       User chooses         Content loaded          Guide
external file  ─►  language &      ─►  from file      ────►   updated
                   append/replace

WORKFLOW 5: Export for Sharing
────────────────────────────────
User selects      User clicks       File saved to           Can share
language      ─►  "Export"    ─►    local path        ──►   with team
              
```

## Module Dependency Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                   Supervertaler Main App                     │
│                  (Supervertaler_v3.7.1.py)                  │
└──────────────────────────┬───────────────────────────────────┘
                           │
                ┌──────────┼──────────┐
                │          │          │
                ▼          ▼          ▼
        ┌──────────────┐  ┌──────────────────┐  ┌───────────────┐
        │ Prompt       │  │ Style Guide      │  │ Prompt        │
        │ Library      │  │ Library          │  │ Assistant     │
        │              │  │ (NEW)            │  │               │
        └──────────────┘  └────────┬─────────┘  └───────────────┘
                                   │
                         ┌─────────┼─────────┐
                         │         │         │
                         ▼         ▼         ▼
                    ┌─────────────────────────────┐
                    │  File System (Disk)         │
                    │  user data/Style_Guides/    │
                    │  ├─ Dutch.md                │
                    │  ├─ English.md              │
                    │  ├─ Spanish.md              │
                    │  ├─ German.md               │
                    │  └─ French.md               │
                    └─────────────────────────────┘

Imports & Initialization:
┌──────────────────────────────────────────────────────────────┐
│  Line 202: from modules.style_guide_manager import           │
│  Lines 812-816: self.style_guide_library = StyleGuideLibrary │
└──────────────────────────────────────────────────────────────┘
```

## Feature Comparison Matrix

```
╔═══════════════════╦════════════╦═════════════╦═══════════════╗
║ Feature           ║ Prompt     ║ Custom      ║ Style         ║
║                   ║ Library    ║ Instructions║ Guides        ║
╠═══════════════════╬════════════╬═════════════╬═══════════════╣
║ Multiple items    ║    ✅      ║     ✅      ║      ✅       ║
║ Organize by type  ║    ✅      ║     ✅      ║      ✅       ║
║ AI modification   ║    ✅      ║     ✅      ║      ✅       ║
║ Chat interface    ║    ✅      ║     ✅      ║      ✅       ║
║ Import/Export     ║    ❌      ║     ❌      ║      ✅       ║
║ Batch operations  ║    ❌      ║     ❌      ║      ✅       ║
║ Language-focused  ║    ❌      ║     ❌      ║      ✅       ║
╚═══════════════════╩════════════╩═════════════╩═══════════════╝
```

## File Organization

```
Supervertaler/
│
├── modules/
│   ├── style_guide_manager.py ──────────────┬──────► 207 lines
│   │                                         │       Full CRUD ops
│   ├── prompt_library.py                    │       Pattern reference
│   ├── prompt_assistant.py                  │       AI integration
│   └── config_manager.py ──────────────┬────┘
│                                       │
│                          Updated with Style_Guides
│
├── user data/
│   ├── Style_Guides/ ─────────────────────┬────────► [NEW]
│   │   ├── Dutch.md          ────────────┬┘         Yaxincheng data
│   │   ├── English.md        ────────────┤          from Excel
│   │   ├── Spanish.md        ────────────┤
│   │   ├── German.md         ────────────┤
│   │   └── French.md         ────────────┤
│   │
│   ├── Prompt_Library/
│   │   ├── System_prompts/
│   │   └── Custom_instructions/
│   │
│   └── Translation_Resources/
│       ├── Glossaries/
│       ├── TMs/
│       └── Segmentation_rules/
│
├── docs/
│   ├── STYLE_GUIDES_PROJECT_COMPLETION.md
│   ├── STYLE_GUIDES_QUICK_REFERENCE.md
│   ├── STYLE_GUIDES_FEATURE_SUMMARY.md
│   ├── STYLE_GUIDES_IMPLEMENTATION.md
│   ├── STYLE_GUIDES_UI_TEMPLATE.py ◄────────────── Copy for Phase 2
│   ├── DUTCH_EXCEL_INTEGRATION_GUIDE.md
│   ├── STYLE_GUIDES_DOCUMENTATION_INDEX.md
│   └── STYLE_GUIDES_VISUAL_ARCHITECTURE.md ◄────── This file
│
└── Supervertaler_v3.7.1.py
    ├── Line 202: Added import
    └── Lines 812-816: Added initialization
```

## Processing Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  USER INPUT IN CHAT INTERFACE                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Parse User Request          │
        │  - "Add to Dutch"            │
        │  - "Add to All"              │
        │  - "Review guide"            │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Route to Handler            │
        ├──────────────────────────────┤
        │  ├─ append_to_guide()        │
        │  ├─ append_to_all_guides()   │
        │  └─ AI suggestion handler    │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Process with AI (Future)    │
        │  - Connect to PromptAssistant│
        │  - Get AI suggestions        │
        │  - Format output             │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Update Files                │
        │  - Write to disk             │
        │  - Update metadata           │
        │  - Log changes               │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Display Result              │
        │  - Show confirmation         │
        │  - Refresh content view      │
        │  - Update list               │
        └──────────────────────────────┘
```

## Status Timeline

```
PHASE 1 (✅ COMPLETE) - October 21, 2025
──────────────────────────────────────────
✅ Design architecture
✅ Create StyleGuideLibrary module
✅ Create default guides (5 languages)
✅ Integrate with ConfigManager
✅ Initialize in main app
✅ Document everything
✅ Provide UI template

           │
           ▼

PHASE 2 (🔲 READY TO START) - Next
─────────────────────────────────────
🔲 Implement UI tab           (2-3 hrs)
🔲 Connect to backend         (1 hr)
🔲 Build chat interface       (2-3 hrs)
🔲 AI integration             (2-3 hrs)
🔲 Testing & refinement       (1-2 hrs)

Total Phase 2: ~9 hours of development
```

## Technology Stack

```
Frontend (Phase 2):
├── tkinter (GUI)
│   ├── ttk.Notebook (Tab container)
│   ├── ttk.Treeview (Language list)
│   ├── ScrolledText (Content editor)
│   └── Text widgets (Chat interface)
└── Threading (For async AI calls)

Backend:
├── Python 3.7+
├── File I/O (markdown/text files)
├── Path handling (OS independent)
└── JSON/YAML (metadata)

Integration Points:
├── prompt_assistant.py (AI integration)
├── config_manager.py (Path management)
└── LLM Clients (OpenAI, Anthropic, Google)
```

## Summary

✅ **Backend:** 100% Complete - Modular, tested, documented
✅ **Default Data:** 100% Complete - 5 languages with your Excel data
✅ **Configuration:** 100% Complete - Integrated with system
✅ **Documentation:** 100% Complete - Comprehensive guides
✅ **UI Template:** 100% Complete - Ready to implement

🔲 **Phase 2:** Ready to implement - 9 hours estimated
   - UI implementation
   - Chat interface
   - AI integration
   - Testing

Ready to build! 🚀
