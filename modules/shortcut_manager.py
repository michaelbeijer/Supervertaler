"""
Keyboard Shortcut Manager for Supervertaler Qt
Centralized management of all keyboard shortcuts
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PyQt6.QtGui import QKeySequence
from PyQt6.QtCore import QSettings

class ShortcutManager:
    """Manages all keyboard shortcuts for Supervertaler"""
    
    # Define all shortcuts with their categories, descriptions, and defaults
    DEFAULT_SHORTCUTS = {
        # File Operations
        "file_new": {
            "category": "File",
            "description": "New Project",
            "default": "",
            "action": "new_project"
        },
        "editor_focus_notes": {
            "category": "Edit",
            "description": "Focus Segment Note Tab (Ctrl+N)",
            "default": "Ctrl+N",
            "action": "focus_segment_notes"
        },
        "file_open": {
            "category": "File",
            "description": "Open Project",
            "default": "Ctrl+O",
            "action": "open_project"
        },
        "file_save": {
            "category": "File",
            "description": "Save Project",
            "default": "Ctrl+S",
            "action": "save_project"
        },

        "file_quit": {
            "category": "File",
            "description": "Quit Application",
            "default": "Alt+F4",
            "action": "close"
        },
        
        # Edit Operations
        "edit_undo": {
            "category": "Edit",
            "description": "Undo",
            "default": "Ctrl+Z",
            "action": "undo"
        },
        "edit_redo": {
            "category": "Edit",
            "description": "Redo",
            "default": "Ctrl+Y",
            "action": "redo"
        },
        "edit_find": {
            "category": "Edit",
            "description": "Find",
            "default": "Ctrl+F",
            "action": "show_find_replace_dialog"
        },
        "edit_replace": {
            "category": "Edit",
            "description": "Replace",
            "default": "Ctrl+H",
            "action": "show_find_replace_dialog"
        },
        "edit_goto": {
            "category": "Edit",
            "description": "Go to Segment",
            "default": "Ctrl+G",
            "action": "show_goto_dialog"
        },
        
        # Translation Operations
        "translate_current": {
            "category": "Translation",
            "description": "Translate Current Segment",
            "default": "Ctrl+T",
            "action": "translate_current_segment"
        },
        "translate_batch": {
            "category": "Translation",
            "description": "Translate Multiple Segments",
            "default": "Ctrl+Shift+T",
            "action": "translate_batch"
        },
        
        # View Operations
        "view_grid": {
            "category": "View",
            "description": "Switch to Grid View",
            "default": "Ctrl+1",
            "action": "switch_to_grid_view"
        },
        "view_list": {
            "category": "View",
            "description": "Switch to List View",
            "default": "Ctrl+2",
            "action": "switch_to_list_view"
        },
        "view_document": {
            "category": "View",
            "description": "Switch to Document View",
            "default": "Ctrl+3",
            "action": "switch_to_document_view"
        },
        "view_toggle_tags": {
            "category": "View",
            "description": "Toggle Tag View",
            "default": "Ctrl+Alt+T",
            "action": "toggle_tag_view"
        },
        
        # Grid Text Zoom
        "grid_zoom_in": {
            "category": "View",
            "description": "Grid Zoom In",
            "default": "Ctrl++",
            "action": "increase_font_size"
        },
        "grid_zoom_out": {
            "category": "View",
            "description": "Grid Zoom Out",
            "default": "Ctrl+-",
            "action": "decrease_font_size"
        },
        
        # Results Pane Zoom
        "results_zoom_in": {
            "category": "View",
            "description": "Results Pane Zoom In",
            "default": "Ctrl+Shift+=",
            "action": "results_pane_zoom_in"
        },
        "results_zoom_out": {
            "category": "View",
            "description": "Results Pane Zoom Out",
            "default": "Ctrl+Shift+-",
            "action": "results_pane_zoom_out"
        },
        
        # Resources & Tools
        "tools_tm_manager_tab": {
            "category": "Resources",
            "description": "TM Manager (Launch in tab)",
            "default": "Ctrl+M",
            "action": "show_tm_manager_in_tab"
        },
        "tools_tm_manager_window": {
            "category": "Resources",
            "description": "TM Manager (Separate window)",
            "default": "Ctrl+Shift+M",
            "action": "show_tm_manager"
        },
        "tools_concordance_search": {
            "category": "Resources",
            "description": "Quick Concordance Search",
            "default": "Ctrl+K",
            "action": "show_concordance_search"
        },
        "tools_universal_lookup": {
            "category": "Resources",
            "description": "Universal Lookup",
            "default": "Ctrl+Alt+L",
            "action": "show_universal_lookup"
        },
        "tools_autofingers": {
            "category": "Resources",
            "description": "AutoFingers",
            "default": "Ctrl+Shift+A",
            "action": "show_autofingers"
        },
        "tools_force_refresh": {
            "category": "Resources",
            "description": "Force Refresh Matches (clear cache)",
            "default": "F5",
            "action": "force_refresh_matches"
        },

        # Special
        "voice_dictate": {
            "category": "Special",
            "description": "Voice Dictation",
            "default": "F9",
            "action": "start_voice_dictation"
        },

        # Match Insertion (Direct)
        "match_insert_1": {
            "category": "Match Insertion",
            "description": "Insert Match #1",
            "default": "",
            "action": "insert_match_1",
            "context": "editor"
        },
        "match_insert_2": {
            "category": "Match Insertion",
            "description": "Insert Match #2",
            "default": "",
            "action": "insert_match_2",
            "context": "editor"
        },
        "match_insert_3": {
            "category": "Match Insertion",
            "description": "Insert Match #3",
            "default": "",
            "action": "insert_match_3",
            "context": "editor"
        },
        "match_insert_4": {
            "category": "Match Insertion",
            "description": "Insert Match #4",
            "default": "",
            "action": "insert_match_4",
            "context": "editor"
        },
        "match_insert_5": {
            "category": "Match Insertion",
            "description": "Insert Match #5",
            "default": "",
            "action": "insert_match_5",
            "context": "editor"
        },
        "match_insert_6": {
            "category": "Match Insertion",
            "description": "Insert Match #6",
            "default": "",
            "action": "insert_match_6",
            "context": "editor"
        },
        "match_insert_7": {
            "category": "Match Insertion",
            "description": "Insert Match #7",
            "default": "",
            "action": "insert_match_7",
            "context": "editor"
        },
        "match_insert_8": {
            "category": "Match Insertion",
            "description": "Insert Match #8",
            "default": "",
            "action": "insert_match_8",
            "context": "editor"
        },
        "match_insert_9": {
            "category": "Match Insertion",
            "description": "Insert Match #9",
            "default": "",
            "action": "insert_match_9",
            "context": "editor"
        },

        # Compare Panel Insertion
        "compare_insert_alt0": {
            "category": "Compare Panel",
            "description": "Insert Compare Panel MT (Alt+0) / TM Target (Alt+0,0)",
            "default": "Alt+0",
            "action": "insert_compare_panel_alt0",
            "context": "editor"
        },

        # Compare Panel Navigation
        "compare_nav_mt_prev": {
            "category": "Compare Panel",
            "description": "Compare Panel: Previous MT result",
            "default": "Ctrl+Alt+Left",
            "action": "compare_panel_nav_mt_prev",
            "context": "editor"
        },
        "compare_nav_mt_next": {
            "category": "Compare Panel",
            "description": "Compare Panel: Next MT result",
            "default": "Ctrl+Alt+Right",
            "action": "compare_panel_nav_mt_next",
            "context": "editor"
        },
        "compare_nav_tm_prev": {
            "category": "Compare Panel",
            "description": "Compare Panel: Previous TM match",
            "default": "Ctrl+Alt+Up",
            "action": "compare_panel_nav_tm_prev",
            "context": "editor"
        },
        "compare_nav_tm_next": {
            "category": "Compare Panel",
            "description": "Compare Panel: Next TM match",
            "default": "Ctrl+Alt+Down",
            "action": "compare_panel_nav_tm_next",
            "context": "editor"
        },
        
        # TermView Insertion (Alt+0-9, double-tap for 00-99)
        "termview_insert_0": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [0] (or [00] if double-tap)",
            "default": "",
            "action": "insert_termview_0",
            "context": "editor"
        },
        "termview_insert_1": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [1] (or [11] if double-tap)",
            "default": "Alt+1",
            "action": "insert_termview_1",
            "context": "editor"
        },
        "termview_insert_2": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [2] (or [22] if double-tap)",
            "default": "Alt+2",
            "action": "insert_termview_2",
            "context": "editor"
        },
        "termview_insert_3": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [3] (or [33] if double-tap)",
            "default": "Alt+3",
            "action": "insert_termview_3",
            "context": "editor"
        },
        "termview_insert_4": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [4] (or [44] if double-tap)",
            "default": "Alt+4",
            "action": "insert_termview_4",
            "context": "editor"
        },
        "termview_insert_5": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [5] (or [55] if double-tap)",
            "default": "Alt+5",
            "action": "insert_termview_5",
            "context": "editor"
        },
        "termview_insert_6": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [6] (or [66] if double-tap)",
            "default": "Alt+6",
            "action": "insert_termview_6",
            "context": "editor"
        },
        "termview_insert_7": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [7] (or [77] if double-tap)",
            "default": "Alt+7",
            "action": "insert_termview_7",
            "context": "editor"
        },
        "termview_insert_8": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [8] (or [88] if double-tap)",
            "default": "Alt+8",
            "action": "insert_termview_8",
            "context": "editor"
        },
        "termview_insert_9": {
            "category": "TermView Insertion",
            "description": "Insert TermView Term [9] (or [99] if double-tap)",
            "default": "Alt+9",
            "action": "insert_termview_9",
            "context": "editor"
        },
        
        # Match Navigation
        "match_next": {
            "category": "Match Navigation",
            "description": "Next Match (in results panel)",
            "default": "Down",
            "action": "next_match",
            "context": "match_panel"
        },
        "match_previous": {
            "category": "Match Navigation",
            "description": "Previous Match (in results panel)",
            "default": "Up",
            "action": "previous_match",
            "context": "match_panel"
        },
        "match_cycle_next": {
            "category": "Match Navigation",
            "description": "Cycle to Next Match (from grid)",
            "default": "Ctrl+Down",
            "action": "select_next_match",
            "context": "grid"
        },
        "match_cycle_previous": {
            "category": "Match Navigation",
            "description": "Cycle to Previous Match (from grid)",
            "default": "Ctrl+Up",
            "action": "select_previous_match",
            "context": "grid"
        },
        "match_insert_selected": {
            "category": "Match Navigation",
            "description": "Insert Selected Match",
            "default": "Space or Enter",
            "action": "insert_selected_match",
            "context": "match_panel"
        },
        "match_insert_selected_ctrl": {
            "category": "Match Navigation",
            "description": "Insert Selected Match (from grid)",
            "default": "Ctrl+Space",
            "action": "insert_selected_match",
            "context": "grid"
        },
        
        # Grid Navigation
        "segment_next": {
            "category": "Grid Navigation",
            "description": "Next Segment",
            "default": "Alt+Down",
            "action": "go_to_next_segment"
        },
        "segment_previous": {
            "category": "Grid Navigation",
            "description": "Previous Segment",
            "default": "Alt+Up",
            "action": "go_to_previous_segment"
        },
        "segment_go_to_top": {
            "category": "Grid Navigation",
            "description": "Go to First Segment",
            "default": "Ctrl+Home",
            "action": "go_to_first_segment"
        },
        "segment_go_to_bottom": {
            "category": "Grid Navigation",
            "description": "Go to Last Segment",
            "default": "Ctrl+End",
            "action": "go_to_last_segment"
        },
        "page_prev": {
            "category": "Grid Navigation",
            "description": "Previous Page (pagination)",
            "default": "PgUp",
            "action": "go_to_prev_page"
        },
        "page_next": {
            "category": "Grid Navigation",
            "description": "Next Page (pagination)",
            "default": "PgDown",
            "action": "go_to_next_page"
        },
        "select_range_up": {
            "category": "Grid Navigation",
            "description": "Select Range Upward (one page)",
            "default": "Shift+PgUp",
            "action": "select_range_page_up"
        },
        "select_range_down": {
            "category": "Grid Navigation",
            "description": "Select Range Downward (one page)",
            "default": "Shift+PgDown",
            "action": "select_range_page_down"
        },
        
        # Editor Operations
        "editor_save_and_next": {
            "category": "Editor",
            "description": "Save & Next Segment",
            "default": "Ctrl+Enter",
            "action": "save_and_next",
            "context": "editor"
        },
        "editor_confirm_selected": {
            "category": "Editor",
            "description": "Confirm All Selected Segments",
            "default": "Ctrl+Shift+Enter",
            "action": "confirm_selected_segments",
            "context": "editor"
        },
        "editor_line_break": {
            "category": "Editor",
            "description": "Insert Line Break",
            "default": "Ctrl+Enter",
            "action": "insert_line_break",
            "context": "editor_alt"
        },
        "editor_cycle_source_target": {
            "category": "Editor",
            "description": "Cycle between Source/Target cells",
            "default": "Tab",
            "action": "cycle_source_target",
            "context": "grid_editor"
        },
        "editor_insert_tab": {
            "category": "Editor",
            "description": "Insert Tab character",
            "default": "Ctrl+Tab",
            "action": "insert_tab",
            "context": "grid_editor"
        },
        "editor_add_to_termbase": {
            "category": "Editor",
            "description": "Add selected term pair to termbase (with dialog)",
            "default": "Ctrl+E",
            "action": "add_to_termbase",
            "context": "grid_editor"
        },
        "editor_quick_add_to_termbase": {
            "category": "Editor",
            "description": "Quick add term pair to last-used termbase",
            "default": "Alt+Left",
            "action": "quick_add_to_termbase",
            "context": "grid_editor"
        },
        "editor_quick_add_priority_1": {
            "category": "Editor",
            "description": "Quick add term pair with Priority 1",
            "default": "Ctrl+Shift+1",
            "action": "quick_add_term_priority_1",
            "context": "grid_editor"
        },
        "editor_quick_add_priority_2": {
            "category": "Editor",
            "description": "Quick add term pair with Priority 2",
            "default": "Ctrl+Shift+2",
            "action": "quick_add_term_priority_2",
            "context": "grid_editor"
        },
        "editor_add_to_non_translatables": {
            "category": "Editor",
            "description": "Add selected text to non-translatables list",
            "default": "Ctrl+Alt+N",
            "action": "add_to_non_translatables",
            "context": "grid_editor"
        },
        "editor_insert_next_tag": {
            "category": "Editor",
            "description": "Insert next tag (memoQ/CafeTran) or wrap selection",
            "default": "Ctrl+,",
            "action": "insert_next_tag",
            "context": "grid_editor"
        },
        "editor_copy_source_to_target": {
            "category": "Editor",
            "description": "Copy source text to target",
            "default": "Ctrl+Shift+S",
            "action": "copy_source_to_target",
            "context": "grid_editor"
        },
        "editor_add_to_dictionary": {
            "category": "Editor",
            "description": "Add word at cursor to custom dictionary",
            "default": "Alt+D",
            "action": "add_word_to_dictionary",
            "context": "grid_editor"
        },
        "editor_open_quickmenu": {
            "category": "Editor",
            "description": "Open QuickMenu for AI prompt actions",
            "default": "Alt+K",
            "action": "open_quickmenu",
            "context": "grid_editor"
        },
        "editor_show_context_menu_double_shift": {
            "category": "Editor",
            "description": "Show context menu (double-tap Shift)",
            "default": "",  # Requires AutoHotkey script: supervertaler_hotkeys.ahk
            "action": "show_context_menu_double_shift",
            "context": "grid_editor",
            "note": "Requires AutoHotkey. Run supervertaler_hotkeys.ahk for this feature."
        },
        
        # Filter Operations
        "filter_selected_text": {
            "category": "Filter",
            "description": "Filter on selected text / Clear filter (toggle)",
            "default": "Ctrl+Shift+F",
            "action": "filter_on_selected_text"
        },
        "clear_filter": {
            "category": "Filter",
            "description": "Clear filter (same as above - toggle behavior)",
            "default": "Ctrl+Shift+F",
            "action": "filter_on_selected_text"
        },
    }
    
    def __init__(self, settings_file: Optional[Path] = None):
        """
        Initialize ShortcutManager
        
        Args:
            settings_file: Path to JSON file for storing custom shortcuts
        """
        self.settings_file = settings_file or Path("user_data/shortcuts.json")
        self.custom_shortcuts = {}
        self.disabled_shortcuts = set()  # Set of disabled shortcut IDs
        self.load_shortcuts()
    
    def load_shortcuts(self):
        """Load custom shortcuts from file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Support both old format (dict of shortcuts) and new format (dict with shortcuts + disabled)
                    if isinstance(data, dict):
                        if "shortcuts" in data:
                            # New format: {"shortcuts": {...}, "disabled": [...]}
                            self.custom_shortcuts = data.get("shortcuts", {})
                            self.disabled_shortcuts = set(data.get("disabled", []))
                        else:
                            # Old format: just the shortcuts dict
                            self.custom_shortcuts = data
                            self.disabled_shortcuts = set()
                    else:
                        self.custom_shortcuts = {}
                        self.disabled_shortcuts = set()
            except Exception as e:
                print(f"Error loading shortcuts: {e}")
                self.custom_shortcuts = {}
                self.disabled_shortcuts = set()
    
    def save_shortcuts(self):
        """Save custom shortcuts to file"""
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            # Save in new format that includes both shortcuts and disabled list
            save_data = {
                "shortcuts": self.custom_shortcuts,
                "disabled": list(self.disabled_shortcuts)
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2)
        except Exception as e:
            print(f"Error saving shortcuts: {e}")
    
    def get_shortcut(self, shortcut_id: str) -> str:
        """
        Get the current shortcut for a given ID
        
        Args:
            shortcut_id: The shortcut identifier
            
        Returns:
            The key sequence string (e.g., "Ctrl+T")
        """
        if shortcut_id in self.custom_shortcuts:
            return self.custom_shortcuts[shortcut_id]
        
        if shortcut_id in self.DEFAULT_SHORTCUTS:
            return self.DEFAULT_SHORTCUTS[shortcut_id]["default"]
        
        return ""
    
    def is_enabled(self, shortcut_id: str) -> bool:
        """
        Check if a shortcut is enabled
        
        Args:
            shortcut_id: The shortcut identifier
            
        Returns:
            True if enabled (not in disabled set), False if disabled
        """
        return shortcut_id not in self.disabled_shortcuts
    
    def enable_shortcut(self, shortcut_id: str):
        """
        Enable a previously disabled shortcut
        
        Args:
            shortcut_id: The shortcut identifier
        """
        self.disabled_shortcuts.discard(shortcut_id)
    
    def disable_shortcut(self, shortcut_id: str):
        """
        Disable a shortcut
        
        Args:
            shortcut_id: The shortcut identifier
        """
        self.disabled_shortcuts.add(shortcut_id)
    
    def set_shortcut(self, shortcut_id: str, key_sequence: str):
        """
        Set a custom shortcut
        
        Args:
            shortcut_id: The shortcut identifier
            key_sequence: The new key sequence string
        """
        if key_sequence:
            self.custom_shortcuts[shortcut_id] = key_sequence
        elif shortcut_id in self.custom_shortcuts:
            del self.custom_shortcuts[shortcut_id]
    
    def reset_shortcut(self, shortcut_id: str):
        """Reset a shortcut to its default value"""
        if shortcut_id in self.custom_shortcuts:
            del self.custom_shortcuts[shortcut_id]
    
    def reset_all_shortcuts(self):
        """Reset all shortcuts to defaults"""
        self.custom_shortcuts = {}
    
    def get_all_shortcuts(self) -> Dict:
        """
        Get all shortcuts with their current values
        
        Returns:
            Dictionary of all shortcuts with metadata
        """
        result = {}
        for shortcut_id, data in self.DEFAULT_SHORTCUTS.items():
            result[shortcut_id] = {
                **data,
                "current": self.get_shortcut(shortcut_id),
                "is_custom": shortcut_id in self.custom_shortcuts,
                "is_enabled": self.is_enabled(shortcut_id)
            }
        return result
    
    def get_shortcuts_by_category(self) -> Dict[str, List[Tuple[str, Dict]]]:
        """
        Get shortcuts organized by category
        
        Returns:
            Dictionary with categories as keys, list of (id, data) tuples as values
        """
        categories = {}
        all_shortcuts = self.get_all_shortcuts()
        
        for shortcut_id, data in all_shortcuts.items():
            category = data["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((shortcut_id, data))
        
        return categories
    
    def find_conflicts(self, shortcut_id: str, key_sequence: str) -> List[str]:
        """
        Find conflicts with a proposed shortcut
        
        Args:
            shortcut_id: The shortcut being changed
            key_sequence: The proposed new key sequence
            
        Returns:
            List of conflicting shortcut IDs
        """
        conflicts = []
        for other_id, data in self.get_all_shortcuts().items():
            if other_id != shortcut_id and data["current"] == key_sequence:
                # Check if they're in different contexts (context-specific shortcuts don't conflict)
                this_context = self.DEFAULT_SHORTCUTS.get(shortcut_id, {}).get("context")
                other_context = self.DEFAULT_SHORTCUTS.get(other_id, {}).get("context")
                
                # Only conflict if same context or no context specified
                if this_context == other_context or not this_context or not other_context:
                    conflicts.append(other_id)
        
        return conflicts
    
    def export_shortcuts(self, file_path: Path):
        """
        Export shortcuts to a JSON file
        
        Args:
            file_path: Path to export file
        """
        export_data = {
            "version": "1.0",
            "shortcuts": self.custom_shortcuts,
            "disabled": list(self.disabled_shortcuts)
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
    
    def import_shortcuts(self, file_path: Path) -> bool:
        """
        Import shortcuts from a JSON file
        
        Args:
            file_path: Path to import file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if "shortcuts" in import_data:
                self.custom_shortcuts = import_data["shortcuts"]
                self.disabled_shortcuts = set(import_data.get("disabled", []))
                return True
            return False
        except Exception as e:
            print(f"Error importing shortcuts: {e}")
            return False
    
    def export_html_cheatsheet(self, file_path: Path):
        """
        Export shortcuts as an HTML cheatsheet
        
        Args:
            file_path: Path to export HTML file
        """
        categories = self.get_shortcuts_by_category()
        
        html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Supervertaler - Keyboard Shortcuts</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #2196F3;
            text-align: center;
            border-bottom: 3px solid #2196F3;
            padding-bottom: 20px;
        }
        h2 {
            color: #1976D2;
            margin-top: 40px;
            margin-bottom: 20px;
            border-left: 5px solid #2196F3;
            padding-left: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        th {
            background-color: #2196F3;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .shortcut {
            font-family: 'Courier New', monospace;
            background-color: #e3f2fd;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 600;
            color: #1976D2;
        }
        .custom {
            color: #4CAF50;
            font-weight: 600;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #666;
            font-size: 0.9em;
        }
        @media print {
            body {
                background-color: white;
            }
            table {
                box-shadow: none;
                page-break-inside: avoid;
            }
        }
    </style>
</head>
<body>
    <h1>🌐 Supervertaler - Keyboard Shortcuts</h1>
    <div class="footer" style="text-align: center; margin-bottom: 30px;">
        <p>The Ultimate Translation Workbench</p>
    </div>
"""
        
        # Add each category
        for category in sorted(categories.keys()):
            shortcuts = categories[category]
            html += f"    <h2>{category}</h2>\n"
            html += "    <table>\n"
            html += "        <tr><th>Action</th><th>Shortcut</th></tr>\n"
            
            for shortcut_id, data in sorted(shortcuts, key=lambda x: x[1]["description"]):
                description = data["description"]
                current = data["current"]
                is_custom = data["is_custom"]
                
                custom_mark = " <span class='custom'>(Custom)</span>" if is_custom else ""
                
                html += f"        <tr>\n"
                html += f"            <td>{description}{custom_mark}</td>\n"
                html += f"            <td><span class='shortcut'>{current}</span></td>\n"
                html += f"        </tr>\n"
            
            html += "    </table>\n"
        
        html += """
    <div class="footer">
        <p>Generated by Supervertaler Qt Edition</p>
        <p>For more information, visit <a href="https://supervertaler.com">supervertaler.com</a></p>
    </div>
</body>
</html>
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)

