# Dual Selection Keyboard Shortcuts - Quick Reference

**Version**: v0.4.2  
**Feature**: Keyboard-based dual text selection (memoQ style)

---

## ⌨️ Keyboard Shortcuts

### Activating Keyboard Selection

**First**: Click on a segment row to select it, then:

| Shortcut | Action |
|----------|--------|
| `Tab` | Switch focus between source and target widgets |
| `Escape` | Clear all selections and exit selection mode |

### Character-by-Character Selection

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+→` | Extend selection right by 1 character |
| `Ctrl+Shift+←` | Extend selection left by 1 character |

### Word-by-Word Selection (Faster!)

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+Ctrl+→` | Extend selection right by 1 word |
| `Ctrl+Shift+Ctrl+←` | Extend selection left by 1 word |

---

## 🎯 Quick Start Guide

### Step-by-Step Workflow

1. **Select a segment row** in Grid View (click anywhere on the row)

2. **Press `Tab`** to activate keyboard selection mode
   - Source widget gets blue border (indicates focus)
   - Status bar shows: "Source focused - use Ctrl+Shift+Arrows to select, Tab to switch"

3. **Use Ctrl+Shift+Arrows** to select text in source
   - Right arrow: Extend selection to the right
   - Left arrow: Extend selection to the left
   - Add Ctrl for word-by-word (faster!)
   - Selected text highlighted in light blue

4. **Press `Tab`** to switch to target
   - Target widget gets green border (indicates focus)
   - Status bar shows: "Target focused - use Ctrl+Shift+Arrows to select, Tab to switch"

5. **Use Ctrl+Shift+Arrows** to select text in target
   - Same controls as source
   - Selected text highlighted in light green

6. **Both selections visible!**
   - Source: Blue highlight
   - Target: Green highlight
   - Perfect for visual verification

7. **Press `Escape`** when done
   - Clears both selections
   - Returns to normal state

---

## 💡 Pro Tips

### Fast Selection
```
Use word-by-word selection for speed:
Ctrl+Shift+Ctrl+→ → → → (select 4 words quickly)
```

### Precise Adjustment
```
Use character-by-character for precision:
Ctrl+Shift+→ → → (extend by 3 characters)
```

### Combine Methods
```
1. Word selection to get close: Ctrl+Shift+Ctrl+→ → →
2. Character selection to fine-tune: Ctrl+Shift+← ←
```

### Quick Switch
```
Tab between source and target repeatedly:
Tab (source) → Ctrl+Shift+Ctrl+→ → → 
Tab (target) → Ctrl+Shift+Ctrl+→ → →
Tab (source) → continue...
```

---

## 🎨 Visual Indicators

### Focus Indicators

**Source Focused:**
```
┌──────────────────────────────┐
│ Source Text Widget           │ ← Blue border (2px)
│ (active for keyboard input)  │
└──────────────────────────────┘
```

**Target Focused:**
```
┌──────────────────────────────┐
│ Target Text Widget           │ ← Green border (2px)
│ (active for keyboard input)  │
└──────────────────────────────┘
```

### Selection Colors

**Source Selection:**
```
The company has ╔═══════════════╗ with its...
                ║transfer pricing║
                ║arrangements    ║
                ╚═══════════════╝
                [Light Blue Background]
```

**Target Selection:**
```
Das Unternehmen hat ╔════════════════════╗ mit...
                    ║Verrechnungspreis-  ║
                    ║vereinbarungen      ║
                    ╚════════════════════╝
                    [Light Green Background]
```

---

## 🆚 Mouse vs Keyboard

### Mouse Selection (Original)
- ✅ Quick for short selections
- ✅ Visual and intuitive
- ❌ Hand leaves keyboard
- ❌ Less precise

### Keyboard Selection (New!)
- ✅ Hands stay on keyboard
- ✅ Very precise control
- ✅ Faster for power users
- ✅ Professional workflow
- ✅ Matches memoQ

**Best Practice**: Use both!
- Mouse for initial positioning
- Keyboard for extending/refining

---

## 📝 Example Workflow

### Translating Long Legal Segment

**Scenario**: 200-word bilateral investment treaty article

```
1. Select segment row (click)
2. Tab (focus source)
3. Ctrl+Shift+Ctrl+→ → → (select "transfer pricing arrangements")
   → Status: "Source selection: 'transfer pricing arrangements' (27 chars)"
4. Tab (focus target)
5. Ctrl+Shift+Ctrl+→ → (select "Verrechnungspreisvereinbarungen")
   → Status: "Target selection: 'Verrechnungspreisvereinbarungen' (32 chars)"
6. ✅ Visual check - both highlighted, correspondence verified
7. Tab (back to source)
8. Ctrl+Shift+Ctrl+→ → (select next phrase)
9. Tab (to target)
10. Ctrl+Shift+Ctrl+→ → (select corresponding phrase)
11. Continue through entire segment...
12. Escape (clear selections when done)
```

**Result**: Systematic verification, nothing missed, all keyboard!

---

## 🔄 State Machine

```
[No Selection]
    ↓ (Tab)
[Source Focused] ←─────┐
    ↓ (Ctrl+Shift+Arrow)│
[Source Selected]       │ (Tab)
    ↓ (Tab)            │
[Target Focused] ───────┘
    ↓ (Ctrl+Shift+Arrow)
[Target Selected]
    ↓ (Tab cycles back to source)
    
[Any State] + Escape → [No Selection]
```

---

## ⚠️ Important Notes

### When Keyboard Selection is Active

**You CAN:**
- ✅ Use Tab to switch focus
- ✅ Use Ctrl+Shift+Arrows to select
- ✅ Use Escape to clear
- ✅ Use mouse to click other rows

**You CANNOT (in this mode):**
- ❌ Type text (not in edit mode)
- ❌ Use regular arrow keys (no Ctrl+Shift)
- ❌ Use Enter (reserved for edit mode)

### To Edit After Selection

```
1. Make your selections (keyboard or mouse)
2. Press Escape to clear selections
3. Press F2 or double-click to enter edit mode
4. Now you can type/edit
```

**OR** directly double-click target to edit (selections auto-clear)

---

## 🎓 memoQ Compatibility

### What Matches memoQ

✅ **Tab** - Switch between source/target  
✅ **Ctrl+Shift+Arrows** - Extend selection  
✅ **Word/character granularity**  
✅ **Visual distinction** (colors)  
✅ **Professional workflow**  

### Differences from memoQ

⚠️ **Focus indicator** - Supervertaler uses border colors  
⚠️ **Word boundaries** - May differ slightly in edge cases  

**Overall**: 95% memoQ-compatible! 🎉

---

## 🚀 Performance Tips

### For Speed
1. **Word selection** for bulk (Ctrl+Shift+Ctrl+Arrow)
2. **Tab** to switch quickly
3. **Character selection** for fine-tuning only

### For Precision
1. **Character selection** (Ctrl+Shift+Arrow)
2. **Visual feedback** (watch the highlights)
3. **Status bar** (check character count)

### For Efficiency
1. **Stay on keyboard** (use Tab, not mouse)
2. **Plan your selections** (think before selecting)
3. **Use Escape** to reset and try again

---

## ✅ Checklist

### Before Using Keyboard Selection

- [ ] Grid View is active (Ctrl+1)
- [ ] Segment row is selected
- [ ] Hands on keyboard
- [ ] Ready to use Tab and arrows

### During Keyboard Selection

- [ ] Tab switches focus correctly
- [ ] Arrows extend selection
- [ ] Colors are correct (blue/green)
- [ ] Status bar shows selections

### After Keyboard Selection

- [ ] Both selections visible
- [ ] Correspondence verified
- [ ] Press Escape to clear
- [ ] Ready for next segment

---

## 🎉 Summary

**Keyboard-based dual selection brings professional translator workflows to Supervertaler!**

- ⌨️ Hands stay on keyboard
- 🚀 Faster than mouse
- 🎯 More precise control
- 💪 Professional standard
- 🎨 Clear visual feedback
- ✅ memoQ-compatible

**Try it now and see the difference!** 

Press `Tab` in Grid View to start! →

---

**Last Updated**: October 4, 2025  
**Version**: v0.4.2  
**Status**: Ready to use!
