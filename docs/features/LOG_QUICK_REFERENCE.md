# Log Window Enhancement - Quick Reference

## Quick Overview

**New in v2.5.0**: Resizable log window + Log tab in Translation Workspace

## 1. Resizable Main Log Window

### How to Resize

```
┌─────────────────────────────────────────┐
│  Translation Workspace / Editor         │
│  (Main Content Area)                    │
│                                         │
│                                         │
├═════════════ DRAG HERE ═════════════════┤  ← Sash Bar (draggable)
│  Log                              [─][□][×]│
│  [10:23:45] Session started            │
│  [10:23:46] Loading project...         │
│  [10:23:47] Project loaded             │
│  [10:23:48] Ready to translate         │
└─────────────────────────────────────────┘
```

**Steps**:
1. Find the raised sash bar between content and log
2. Click and hold on the sash bar
3. Drag up to make log larger
4. Drag down to make log smaller
5. Release to set size

**Tips**:
- Initial height: ~100px (10+ lines)
- Sash has raised relief - easy to spot
- Main content auto-adjusts as you drag
- Size persists while app is open

## 2. Log Tab in Translation Workspace

### Where to Find

```
Translation Workspace Tabs:
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│📁   │📝   │📋   │🤖   │✨   │💾   │📚   │🖼   │🔒   │⚙   │📋   │
│Proj │Syst │Cust │MT   │LLM  │TM   │Glos │Img  │Non- │Set  │Log  │  ← NEW
│     │Prom │Inst │     │     │     │     │     │trans│     │     │
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
                                                              ↑
                                                        Click here
```

### What You See

```
┌─────────────────────────────────────────────────────────┐
│ 📋 Session Log                                          │
│ All system messages, API calls, and operations are      │
│ logged here in real-time.                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ [10:23:45] Session started                             │
│ [10:23:46] Loading project: Patent Translation.json    │
│ [10:23:47] Project loaded successfully                 │
│ [10:23:48] TM loaded: 1,234 segments                   │
│ [10:23:49] Glossary loaded: 567 terms                  │
│ [10:23:50] Ready to translate                          │
│ [10:24:15] Translating segment 1/50...                 │
│ [10:24:17] ✓ Translation complete (2.3s)               │
│ [10:24:18] Added to TM                                 │
│                                                         │
│ ↓ (Auto-scrolls to latest)                             │
├─────────────────────────────────────────────────────────┤
│ [🗑️ Clear Log]  ℹ️ Synchronized with main log window   │
└─────────────────────────────────────────────────────────┘
```

## 3. Synchronized Behavior

### Both Logs Show Same Content

```
Main Log Window (Bottom):          Workspace Log Tab:
┌──────────────────────┐          ┌──────────────────────┐
│ [10:24:15] New msg ← │ SAME     │ [10:24:15] New msg ← │
│ [10:24:14] ...       │ CONTENT  │ [10:24:14] ...       │
└──────────────────────┘          └──────────────────────┘
```

**Features**:
- ✅ Same timestamps
- ✅ Same messages
- ✅ Both auto-scroll
- ✅ Both cleared together
- ✅ Real-time sync

### Clear Log Button

**Location**: Bottom of Log tab toolbar

**Effect**:
- Clears main log window
- Clears workspace log tab
- Shows "Log cleared" confirmation

**Use Case**: Fresh start for new translation session

## 4. When to Use Each

### Use Main Log Window When:
- ✓ Quick glance at recent messages
- ✓ Monitoring during active work
- ✓ Want more screen space for content
- ✓ Checking status while translating

### Use Workspace Log Tab When:
- ✓ Need full log history review
- ✓ Working in Translation Workspace
- ✓ Debugging issues
- ✓ Want permanent log visibility
- ✓ Analyzing workflow patterns

## 5. Common Scenarios

### Scenario 1: "I need more log space temporarily"

**Solution**: Drag sash bar up in main window
```
Before:                 After:
┌─────────────┐        ┌─────────────┐
│ Content 90% │        │ Content 70% │
├═════════════┤   →    ├═════════════┤
│ Log 10%     │        │ Log 30%     │
└─────────────┘        └─────────────┘
```

### Scenario 2: "I'm working in Workspace and need log"

**Solution**: Click Log tab (no need to scroll to bottom)
```
Translation Workspace > 📋 Log tab
(Full log history immediately accessible)
```

### Scenario 3: "Log is cluttered from previous work"

**Solution**: Click "Clear Log" button in Log tab
```
Before Clear:           After Clear:
[100+ messages]    →    [Log cleared]
                        (Fresh start)
```

### Scenario 4: "Checking if translation finished"

**Solution**: Either location shows latest message:
```
Main Log:  [10:45:23] ✓ Batch translation complete (47/50)
Tab Log:   [10:45:23] ✓ Batch translation complete (47/50)
                      ↑ Same message, same time
```

## 6. Keyboard Shortcuts

Currently no dedicated keyboard shortcuts for log features.

**Future Enhancement**: Consider adding:
- `Ctrl+L`: Focus log tab
- `Ctrl+Shift+L`: Clear log
- `Ctrl+Alt+L`: Toggle log window size

## 7. Troubleshooting

### "I can't see the sash bar"

**Check**:
- Look for raised line between content and log
- Try hovering mouse between panels
- Sash is 4px thick with raised relief

**Solution**: 
- Window might be too small
- Try maximizing window
- Sash becomes more visible with larger window

### "Log tab is not showing"

**Check**:
- Translation Workspace must be active (Grid or Split view)
- Look for 📋 Log tab (rightmost tab)
- Check if tab got hidden in panel settings

**Solution**:
- Switch to Grid/Split view
- Check `assist_visible_panels['log']` setting

### "Logs are out of sync"

**This shouldn't happen**, but if it does:
1. Close and reopen Translation Workspace
2. Check console for errors
3. Clear log and start fresh

## 8. Visual Indicators

### Sash Bar Appearance
- **Style**: Raised relief (3D effect)
- **Width**: 4px
- **Color**: System default (usually gray)
- **Cursor**: Changes to resize cursor on hover
- **Position**: Between content and log frames

### Log Tab Icon
- **Icon**: 📋 (clipboard)
- **Position**: Rightmost tab after ⚙ Settings
- **Label**: "Log"

### Log Message Format
```
[HH:MM:SS] Message text
 └──┬──┘   └────┬────┘
    │           └─ Log message content
    └─ 24-hour timestamp
```

## Summary

**Two Ways to View Logs**:
1. **Main Window**: Resizable bottom panel (drag sash)
2. **Workspace Tab**: Full-height dedicated tab

**Both Stay Synchronized**:
- Same content
- Same timing
- Same clearing

**Choose Based on Need**:
- Main window: Quick monitoring
- Workspace tab: Deep analysis

**Pro Tip**: 
Keep log visible in workspace tab while working on complex translations. Use main window for quick status checks.
