# Supervertaler v2.5.0 - Dashboard Layout Guide

**Date**: October 5, 2025  
**Purpose**: Clear workflow organization for three distinct use cases

---

## 📋 Dashboard Structure Overview

The dashboard is now organized to clearly show **three workflow options**:

1. **AI Pre-Translation** (works with Legacy TXT or CAT DOCX)
2. **AI Proofreading** (works with Legacy TXT only)
3. **Traditional CAT Editing** (works with CAT DOCX only - NO AI required)

---

## 🎯 Visual Layout (Top to Bottom)

### **Header Section**
```
┌─────────────────────────────────────────────┐
│ Supervertaler v2.5.0 - Dashboard           │
│ Professional CAT tool with multicontextual  │
│ AI translation system                       │
└─────────────────────────────────────────────┘
```

### **Section 1: 🤖 AI-Assisted Workflows (Optional)**
```
┌─────────────────────────────────────────────────────────────┐
│ Select AI mode if you want AI assistance, or skip this for  │
│ traditional CAT editing:                                     │
│                                                              │
│ ○ AI Pre-Translation Mode (Use AI to translate source text) │
│ ○ AI Proofreading Mode (Use AI to revise translations)      │
│                                                              │
│ 💡 TIP: To use traditional CAT editing (no AI), skip to     │
│    CAT Editor section below                                 │
└─────────────────────────────────────────────────────────────┘
```

**Purpose**: Makes it clear that AI is OPTIONAL. Users can skip this entirely for traditional CAT work.

---

### **Section 2: 📋 Workflow Selection**

#### **Option 1: Legacy TXT Workflow (AI Required)**
```
┌─────────────────────────────────────────────────────────────┐
│ For memoQ/Trados users with bilingual TXT files             │
│ ⚠ Requires AI mode selection above                          │
│                                                              │
│ Input Text File:  [________________] [Browse...]            │
│ Output File:      [________________] [Browse...]            │
└─────────────────────────────────────────────────────────────┘
```

**Use Case**:
- User has bilingual TXT files from memoQ/Trados
- **Must** use AI (Pre-Translation or Proofreading mode)
- AI translates/proofreads → outputs TXT + TMX

---

#### **Option 2: CAT Editor Workflow (AI Optional)**
```
┌─────────────────────────────────────────────────────────────┐
│ Direct DOCX translation with professional CAT grid interface │
│                                                              │
│ • With AI: Import DOCX → AI pre-translate → edit → export   │
│ • Without AI: Import DOCX → manual translate → export       │
│   (Like traditional CAT tools: memoQ, Trados, etc.)         │
│                                                              │
│ 👉 Configure below in '🔧 CAT Editor' section               │
└─────────────────────────────────────────────────────────────┘
```

**Use Case A** (With AI):
- User imports DOCX
- Clicks "AI Pre-Translate" button
- AI fills translations using multicontextual intelligence
- User edits in grid
- Exports translated DOCX

**Use Case B** (Without AI):
- User imports DOCX
- Skips AI button entirely
- Translates manually in grid (like traditional CAT tool)
- Can use MT, TM, glossaries (future features)
- Exports translated DOCX

---

### **Section 3: ⚙️ Shared Settings (used by both workflows)**
```
┌─────────────────────────────────────────────────────────────┐
│ These context sources enhance AI translation quality in     │
│ both Legacy and CAT workflows:                              │
│                                                              │
│ Translation Memory (TXT/TMX): [____________] [Browse TM...] │
│ Tracked Changes:              [Status] [Load] [Browse] [Clr]│
│ Document Images Folder:       [____________] [Browse...]    │
│ Custom Instructions for AI:   [Text area]                   │
└─────────────────────────────────────────────────────────────┘
```

**Purpose**: 
- Used by BOTH Legacy TXT and CAT DOCX workflows
- Used by BOTH AI and non-AI workflows
- TM/Glossaries work even without AI (traditional CAT feature)

---

### **Section 4: 📝 Prompt Library - Optional Enhancement**
```
┌─────────────────────────────────────────────────────────────┐
│ 📝 Prompt Library - Optional (Click to expand)              │
│ ✏ Customize AI system prompts for specialized domains       │
└─────────────────────────────────────────────────────────────┘
```

**Purpose**: Advanced users can customize AI behavior for specialized domains (legal, medical, etc.)

---

### **Section 5: 💼 Project Library**
```
┌─────────────────────────────────────────────────────────────┐
│ 💼 Project Library (Click to expand)                        │
│ 💾 Project management - Save entire workspace state         │
└─────────────────────────────────────────────────────────────┘
```

**Purpose**: Save/restore complete workspace configurations

---

### **Section 6: 🔧 CAT Editor - DOCX Translation (AI Optional)**
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 CAT Editor - DOCX Translation (AI Optional) - Expand     │
│ 📄 Import DOCX → Edit in Grid (with/without AI) → Export    │
│ Like memoQ/Trados but integrated                            │
└─────────────────────────────────────────────────────────────┘

When expanded:
├─ DOCX File: [Test document.docx] [Import DOCX]
├─ Segments: 28 | Untranslated: 28 | Progress: 0.0%
├─ [AI-Assisted Pre-Translation] [Export Translated DOCX] [Clear]
├─ [Show Segment Grid] ← Opens grid for manual editing
└─ AI Provider: Claude | Model: claude-3-5-sonnet
```

**Workflow A (With AI)**:
1. Import DOCX
2. Click "AI-Assisted Pre-Translation"
3. AI fills all segments with translations
4. User reviews/edits in grid
5. Export DOCX

**Workflow B (Without AI - Traditional CAT)**:
1. Import DOCX
2. Click "Show Segment Grid"
3. Translate manually segment-by-segment
4. Use TM matches, glossaries (when implemented)
5. Export DOCX

---

## 🎨 Color Coding

- **Blue boxes** (#f0f8ff) = Legacy TXT workflow (AI required)
- **Green boxes** (#f0fff0) = CAT DOCX workflow (AI optional)
- **Yellow notes** (#fffacd) = Important tips/clarifications
- **White boxes** = Shared settings (used by all workflows)

---

## ✨ Key Improvements from Original Layout

### Before:
- ❌ "Operation Mode: Translate / Proofread" → unclear what this means
- ❌ No distinction between AI and non-AI workflows
- ❌ Unclear that CAT Editor can work without AI
- ❌ Files/settings scattered without logical grouping

### After:
- ✅ Clear "AI-Assisted Workflows (Optional)" section with skip tip
- ✅ Three distinct use cases explained upfront
- ✅ Workflow options numbered (Option 1, Option 2)
- ✅ Visual distinction: AI required vs AI optional
- ✅ Shared settings grouped separately
- ✅ Emphasis that CAT Editor = "Like memoQ/Trados but integrated"

---

## 🎯 User Mental Model

### **"I want AI to translate for me"**
→ Select AI Pre-Translation mode  
→ Choose Legacy TXT OR CAT DOCX workflow  
→ Configure settings → Start Process / AI Pre-Translate

### **"I want AI to proofread my existing translations"**
→ Select AI Proofreading mode  
→ Use Legacy TXT workflow  
→ Configure settings → Start Process

### **"I want to translate manually like in memoQ/Trados"**
→ SKIP AI section entirely  
→ Go to CAT Editor section  
→ Import DOCX → Show Grid → Translate manually → Export

---

## 📊 Information Panel (Compact)

Reduced from ~40 lines to ~25 lines while keeping essential info:

```
🎯 Supervertaler v2.5.0
Professional CAT tool with multicontextual AI translation
By Michael Beijer

🧠 MULTICONTEXTUAL INTELLIGENCE:
• Full document context for every segment
• Tracked changes learning from DOCX revisions
• Translation memory (TMX/TXT) integration
• Multimodal support (AI sees referenced images)
• Custom instructions & advanced prompt libraries

📝 THREE WORKFLOW OPTIONS:
1️⃣ AI PRE-TRANSLATION (with AI)
   • Legacy: TXT → AI → TXT+TMX
   • CAT Grid: DOCX → AI pre-fill → edit → export

2️⃣ AI PROOFREADING (with AI)
   • Input: source<TAB>target → AI revision → output
   • Best with Gemini

3️⃣ TRADITIONAL CAT EDITING (no AI)
   • DOCX → manual translation in grid
   • Like memoQ/Trados (MT/TM/Glossary support)
```

---

## 🚀 Implementation Status

- ✅ Dashboard layout restructured
- ✅ Clear AI vs non-AI distinction
- ✅ Three workflows explained
- ✅ Color coding for visual distinction
- ✅ Info panel compacted
- ✅ Shared settings grouped
- ✅ CAT Editor emphasizes AI optional
- ✅ Traditional CAT use case highlighted

**Next Steps**:
- Test user comprehension with real users
- Add tooltips for complex sections
- Consider workflow wizard for first-time users
- Future: MT engine integration for non-AI CAT mode
- Future: Glossary/termbase support

---

## 📚 Related Documentation

- `INTEGRATION_PLAN_v2.5.0.md` - Technical architecture
- `CHANGELOG.md` - Version history
- `Supervertaler User Guide (v2.4.0).md` - Full user manual
- `cat_tool_prototype/QUICK_START.md` - CAT editor guide

---

**Last Updated**: October 5, 2025  
**Version**: 2.5.0  
**Status**: ✅ Implemented and ready for user testing
