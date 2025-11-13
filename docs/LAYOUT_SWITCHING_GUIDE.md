# Layout Switching Feature Guide

## Overview
Supervertaler Qt now supports two layout modes to optimize your workflow:

1. **Split View** (Default) - Traditional sidebar + main view layout
2. **Unified View** - All-in-one tabbed interface for maximum screen space

## How to Switch Layouts

### Using the Menu
1. Open **View → Layout** in the menu bar
2. Choose between:
   - **📱 Split View (Sidebar + View)** - Classic layout with sidebar on left
   - **🖥️ Unified View (All Tabs)** - Full-width tabbed layout

### Layout Persistence
Your layout preference is automatically saved and restored when you restart the application.

## Split View Layout
**Best for**: Multi-tasking with quick access to prompts and tools

- Left sidebar (~40% width): Prompt Manager, Resources, Tools, Settings
- Right panel (~60% width): Grid View, List View, Document View
- Adjustable splitter between panels
- Navigate menu provides quick access to different views

**Use cases**:
- Working with prompts while translating
- Accessing tools while viewing segments
- Managing resources alongside your work

## Unified View Layout
**Best for**: Maximizing translation grid or document space

- All tabs in a single QTabWidget (100% width)
- Tab order: Grid View, List View, Document View, [separator], Prompt Manager, Resources, Tools, Settings
- More screen space for wide translation grids
- Better for working with long segments

**Use cases**:
- Large translation grids with many columns
- Long document segments that need full width
- Focused single-task workflow

## Technical Details

### Implementation
- **Split View**: Uses `QSplitter` to divide left sidebar and right view panel
- **Unified View**: Uses single `QTabWidget` with all tabs
- Widget reparenting via `removeTab()` / `addTab()` when switching
- Preference saved to `ui_preferences.json`

### Shortcuts
Currently no keyboard shortcut assigned. Consider adding:
- **Ctrl+Shift+L** - Toggle layout mode
- **Ctrl+1** through **Ctrl+8** - Quick tab navigation (unified view)

## Future Enhancements
Potential improvements:
- Quick toggle button in toolbar
- Keyboard shortcut for switching
- Remember tab selection when switching modes
- Custom tab order in unified view
- Detachable panels for multi-monitor setups

## Troubleshooting

### Widgets appear in wrong locations after switching
- Restart the application
- Check `ui_preferences.json` for corrupted data
- Delete preferences file to reset to defaults

### Layout doesn't persist after restart
- Verify write permissions for `user_data/` or `user_data_private/` folder
- Check console for JSON save errors

## Technical Reference

### Files Modified
- `Supervertaler_Qt.py`:
  - Added `switch_layout_mode(mode)` method (line ~1725)
  - Added `_create_split_layout()` method (line ~1750)
  - Added `_create_unified_layout()` method (line ~1780)
  - Added `save_layout_preference()` / `load_layout_preference()` (line ~1810)
  - Updated `create_menus()` with Layout submenu (line ~1335)
  - Updated `init_ui()` to load saved preference (line ~1119)

### Settings File
Location: `user_data/ui_preferences.json` or `user_data_private/ui_preferences.json`

Format:
```json
{
  "layout_mode": "split"  // or "unified"
}
```

---

**Version**: Implemented in v1.4.1
**Date**: January 2025
**Status**: Stable, ready for production use
