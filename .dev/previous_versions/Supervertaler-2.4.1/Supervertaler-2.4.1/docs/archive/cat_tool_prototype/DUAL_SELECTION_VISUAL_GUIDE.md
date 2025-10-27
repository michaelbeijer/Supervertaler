# Dual Selection - Quick Visual Guide

**Feature**: Simultaneous text selection in source and target columns  
**Where**: Grid View only (for now)  
**Status**: Ready to test!

---

## 🖼️ Visual Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│ Grid View - Row #15 Selected                                       │
├─────┬──────┬────────┬─────────────────────┬─────────────────────────┤
│ ID  │ Type │ Status │ Source              │ Target                  │
├─────┼──────┼────────┼─────────────────────┼─────────────────────────┤
│ 15  │ para │ draft  │ The company has... │ Das Unternehmen hat...  │
│     │      │        │                     │                         │
│     │      │        │ ...established      │ ...verrechnungs-        │
│     │      │        │ ╔════════════════╗  │ ╔═════════════════╗     │
│     │      │        │ ║transfer pricing║  │ ║preisvereinbar-  ║     │
│     │      │        │ ║ arrangements   ║  │ ║ungen etabliert  ║     │
│     │      │        │ ╚════════════════╝  │ ╚═════════════════╝     │
│     │      │        │ with its...         │ mit seinen...           │
│     │      │        │                     │                         │
│     │      │        │ [Blue selection]    │ [Green selection]       │
└─────┴──────┴────────┴─────────────────────┴─────────────────────────┘

Status bar: "Source selection: 'transfer pricing arrangements' (27 chars)"
Status bar: "Target selection: 'verrechnungspreisvereinbarungen' (32 chars)"
```

**Notice:** Both selections are visible at the same time!

---

## 🎯 Step-by-Step Usage

### Step 1: Select a Row
```
Action: Click anywhere on row #15
Result: Row gets blue border, becomes current segment
```

### Step 2: Select Text in Source
```
Action: Click and drag in source column over "transfer pricing arrangements"

Before:
│ Source                                                              │
│ The company has established transfer pricing arrangements with...   │

After:
│ Source                                                              │
│ The company has established ╔══════════════════════════╗ with...   │
│                             ║transfer pricing          ║            │
│                             ║arrangements              ║            │
│                             ╚══════════════════════════╝            │
│                             [Light blue background]                 │
```

### Step 3: Select Text in Target
```
Action: Click and drag in target column over "verrechnungspreisvereinbarungen"

Before:
│ Target                                                              │
│ Das Unternehmen hat verrechnungspreisvereinbarungen etabliert...    │

After:
│ Target                                                              │
│ Das Unternehmen hat ╔═══════════════════════════════════╗ eta...   │
│                     ║verrechnungspreisvereinbarungen    ║           │
│                     ╚═══════════════════════════════════╝           │
│                     [Light green background]                        │
```

### Step 4: Both Selections Visible!
```
Current State:
┌──────────────────────────────────────┬──────────────────────────────────┐
│ Source                               │ Target                           │
├──────────────────────────────────────┼──────────────────────────────────┤
│ The company has established          │ Das Unternehmen hat              │
│ ╔══════════════════════════╗ with... │ ╔═══════════════════════════╗...│
│ ║transfer pricing          ║         │ ║verrechnungspreis-         ║   │
│ ║arrangements              ║         │ ║vereinbarungen             ║   │
│ ╚══════════════════════════╝         │ ╚═══════════════════════════╝   │
│ [Blue]                               │ [Green]                          │
└──────────────────────────────────────┴──────────────────────────────────┘

✅ Both selections remain visible!
✅ Easy to verify they correspond!
✅ Different colors prevent confusion!
```

---

## 🎨 Color Scheme

### Source Selection
```
┌─────────────────────────┐
│  transfer pricing       │  ← Light blue background (#B3E5FC)
│  arrangements           │  ← Dark blue text (#01579B)
└─────────────────────────┘
```

### Target Selection
```
┌─────────────────────────┐
│  verrechnungspreis-     │  ← Light green background (#C8E6C9)
│  vereinbarungen         │  ← Dark green text (#1B5E20)
└─────────────────────────┘
```

### Why Different Colors?
- **Blue for source** = Cold color = Incoming information
- **Green for target** = Warm color = Completed translation
- **High contrast** = Easy to distinguish at a glance
- **Distinct from other UI colors** = No confusion with status, filters, etc.

---

## 🔄 When Selections Clear

### Automatic Clearing

**1. Changing Rows**
```
Before: Row 15 selected, both source and target have selections
Action: Click on row 16
After: Row 16 selected, NO selections (fresh start)
```

**2. Entering Edit Mode**
```
Before: Row 15 selected, both source and target have selections
Action: Press F2 or double-click target
After: Edit mode active, selections cleared, yellow edit background
```

**3. Navigating**
```
Before: Row 15 selected, both source and target have selections
Action: Press Ctrl+Down to go to next segment
After: Row 16 selected, NO selections
```

---

## 💡 Use Cases

### Use Case 1: Long Legal Segment
```
Segment: 250-word paragraph about bilateral investment treaty

Workflow:
1. Select row
2. Source: Select "transfer of capital"
3. Target: Select "Kapitalübertragung"
4. ✅ Verify correspondence
5. Source: Select "repatriation of profits"
6. Target: Select "Rückführung von Gewinnen"
7. ✅ Verify correspondence
8. Continue through entire segment...

Result: Systematic verification, nothing missed!
```

### Use Case 2: Technical Term Verification
```
Segment: Technical specifications with industry jargon

Workflow:
1. Select row
2. Source: Select "thermal expansion coefficient"
3. Target: Look for corresponding term
4. Target: Select "thermischer Ausdehnungskoeffizient"
5. ✅ Both highlighted, easy visual check
6. Confidence that technical term is correct!
```

### Use Case 3: Marketing Copy Flow
```
Segment: Creative marketing paragraph with multiple clauses

Workflow:
1. Select row
2. Source: Select first clause
3. Target: Select corresponding reworded section
4. ✅ Verify flow maintained
5. Source: Select second clause
6. Target: Select corresponding creative adaptation
7. ✅ Verify tone and message preserved
```

---

## ⚡ Quick Reference

### Activate Dual Selection
```
1. Grid View (Ctrl+1)
2. Click row to select
3. Click & drag in source
4. Click & drag in target
```

### Colors
```
Source → Blue
Target → Green
```

### Deactivate
```
• Change row
• Enter edit mode (F2/Double-click)
• Navigate (Ctrl+Up/Down)
```

### Status Bar
```
Shows: "Source/Target selection: 'text' (X chars)"
```

---

## 🎯 Pro Tips

### Tip 1: Work Systematically
```
Start at beginning of long segment
→ Select small pieces
→ Verify correspondence
→ Move to next piece
→ Repeat until end of segment
```

### Tip 2: Use for QA
```
After translating long segment:
→ Go back through with dual selection
→ Verify each piece
→ Catch missed portions
```

### Tip 3: Don't Overthink It
```
It's simple:
1. Select in source (blue)
2. Select in target (green)
3. Both stay selected
4. That's it!
```

### Tip 4: Combine with Filters
```
Use filter mode to find specific content
→ Then use dual selection for detailed verification
→ Best of both worlds!
```

---

## 🔍 Visual Examples

### Example 1: Short Selections
```
Source: "sustainable development"
Target: "nachhaltige Entwicklung"

┌──────────────┬──────────────┐
│ sustainable  │ nachhaltige  │ ← Both selected
│ development  │ Entwicklung  │ ← Easy visual check
└──────────────┴──────────────┘
```

### Example 2: Multi-word Phrases
```
Source: "in accordance with the provisions of Article 12"
Target: "gemäß den Bestimmungen von Artikel 12"

┌─────────────────────────────────┬──────────────────────────────────┐
│ in accordance with the          │ gemäß den Bestimmungen von       │
│ provisions of Article 12        │ Artikel 12                       │
└─────────────────────────────────┴──────────────────────────────────┘
                                   ↑ Both selected, both visible
```

### Example 3: Nested in Longer Text
```
Full segment (200 words)
Selected portion in middle:

Source: "...the arbitration tribunal shall consist of three arbitrators..."
Target: "...das Schiedsgericht aus drei Schiedsrichtern bestehen..."

Only selected portion highlighted:
┌──────────────────────────┬─────────────────────────────┐
│ arbitration tribunal     │ Schiedsgericht              │ ← Selected
│ shall consist of three   │ aus drei Schiedsrichtern    │ ← Selected
│ arbitrators              │ bestehen                    │ ← Selected
└──────────────────────────┴─────────────────────────────┘
Rest of segment: not highlighted, still visible
```

---

## ✅ Quick Test

**Try this now:**

1. Open Grid View
2. Select any row with text
3. In source: Select a few words
   - Should see light blue background
4. In target: Select a few words
   - Should see light green background
5. **Both should be visible at once!**

If you see both selections → Feature working! 🎉

---

## 🎓 Comparison with Other CAT Tools

### memoQ
```
✅ Has dual selection
✅ Different colors for source/target
✅ Professional standard
→ Supervertaler now matches this!
```

### SDL Trados Studio
```
❌ Limited selection highlighting
❌ Less visual distinction
→ Supervertaler may be better!
```

### Memsource
```
⚠️ Has selection, but not as clear
→ Supervertaler competitive!
```

---

## 📊 Benefits Summary

| Benefit | How Dual Selection Helps |
|---------|--------------------------|
| **Accuracy** | Verify each piece translated correctly |
| **Confidence** | See correspondence visually |
| **Speed** | Quick systematic verification |
| **Quality** | Catch missed portions |
| **Professional** | Matches industry-leading tools |
| **Long Segments** | Break down complex text |
| **Visual** | At-a-glance checking |

---

## 🚀 What's Next?

### Already Planning
- Dual selection in List View
- Dual selection in Document View
- Statistics for selections
- Keyboard shortcuts

### Your Feedback Welcome!
- What works well?
- What could be better?
- What features would help?

---

**Bottom Line:**  
You can now select text in source and target at the same time.  
Both selections stay visible with different colors.  
This is a non-negotiable professional CAT tool feature.  
Supervertaler now has it! 🎉
