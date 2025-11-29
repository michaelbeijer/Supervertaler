"""
Translation Results Panel
Compact memoQ-style right-side panel for displaying translation matches
Supports stacked match sections, drag/drop, and compare boxes with diff highlighting

Keyboard Shortcuts:
- ↑/↓ arrows: Navigate through matches (cycle through sections)
- Spacebar/Enter: Insert currently selected match into target cell
- Ctrl+1-9: Insert specific match directly (by number, global across all sections)
- Escape: Deselect match (when focus on panel)

Compare boxes: Vertical stacked with resizable splitter
Text display: Supports long segments with text wrapping
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData
from PyQt6.QtGui import QDrag, QCursor, QFont
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class TranslationMatch:
    """Represents a single translation match"""
    source: str
    target: str
    relevance: int  # 0-100
    metadata: Dict[str, Any]  # Context, domain, timestamp, etc.
    match_type: str  # "NT", "MT", "TM", "Termbase", "LLM"
    compare_source: Optional[str] = None  # For TM compare boxes
    provider_code: Optional[str] = None  # Provider code: "GT", "AT", "MMT", "CL", "GPT", "GEM", etc.


class CompactMatchItem(QFrame):
    """Compact match display (like memoQ) with source and target in separate columns"""
    
    match_selected = pyqtSignal(TranslationMatch)
    
    # Class variables (can be changed globally)
    font_size_pt = 9
    show_tags = False  # When False, HTML/XML tags are hidden
    tag_highlight_color = '#FFB6C1'  # Default light pink for tag highlighting
    
    def __init__(self, match: TranslationMatch, match_number: int = 0, parent=None):
        super().__init__(parent)
        self.match = match
        self.match_number = match_number
        self.is_selected = False
        self.num_label_ref = None  # Initialize FIRST before update_styling()
        self.source_label = None
        self.target_label = None
        
        self.setFrameStyle(QFrame.Shape.NoFrame)  # No frame border
        self.setMinimumHeight(20)  # Minimum height (can expand)
        self.setMaximumHeight(100)  # Allow up to 100px if text wraps
        
        # Vertical layout with 2 rows: number+relevance on left, then source and target on right
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(2, 1, 2, 1)  # Minimal padding
        main_layout.setSpacing(3)
        
        # Left side: Match number box (small colored box)
        if match_number > 0:
            num_label = QLabel(f"{match_number}")
            num_label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 9px;
                    padding: 1px;
                    border-radius: 2px;
                    margin: 0px;
                }
            """)
            num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            num_label.setFixedWidth(22)
            num_label.setFixedHeight(18)
            
            # Add tooltip based on match type
            match_type_tooltips = {
                "LLM": "LLM Translation (AI-generated)",
                "TM": "Translation Memory (Previously approved)",
                "Termbase": "Termbase",
                "MT": "Machine Translation",
                "NT": "New Translation",
                "NonTrans": "🚫 Non-Translatable (do not translate)"
            }
            tooltip_text = match_type_tooltips.get(match.match_type, "Translation Match")
            num_label.setToolTip(tooltip_text)
            
            self.num_label_ref = num_label  # Set BEFORE calling update_styling()
            main_layout.addWidget(num_label, 0, Qt.AlignmentFlag.AlignTop)
        
        # Middle: Relevance % (vertical)
        rel_label = QLabel(f"{match.relevance}%")
        rel_label.setStyleSheet("font-size: 7px; color: #666; padding: 0px; margin: 0px;")
        rel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rel_label.setFixedWidth(32)
        rel_label.setFixedHeight(18)
        main_layout.addWidget(rel_label, 0, Qt.AlignmentFlag.AlignTop)
        
        # Right side: Source and Target in a horizontal layout (like spreadsheet columns)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(6)
        
        # Source column - NO truncation, allow wrapping
        self.source_label = QLabel(self._format_text(match.source))
        self.source_label.setWordWrap(True)  # Allow wrapping
        # Always use RichText when tags are shown (for highlighting), otherwise RichText for rendering
        self.source_label.setTextFormat(Qt.TextFormat.RichText)
        self.source_label.setStyleSheet(f"font-size: {self.font_size_pt}px; color: #333; padding: 0px; margin: 0px;")
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.source_label.setMinimumWidth(150)  # Much wider minimum
        content_layout.addWidget(self.source_label, 1)
        
        # Target column - NO truncation, allow wrapping
        self.target_label = QLabel(self._format_text(match.target))
        self.target_label.setWordWrap(True)  # Allow wrapping
        # Always use RichText when tags are shown (for highlighting), otherwise RichText for rendering
        self.target_label.setTextFormat(Qt.TextFormat.RichText)
        self.target_label.setStyleSheet(f"font-size: {self.font_size_pt}px; color: #555; padding: 0px; margin: 0px;")
        self.target_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.target_label.setMinimumWidth(150)  # Much wider minimum
        content_layout.addWidget(self.target_label, 1)
        
        # Provider code column (tiny, after target text) - always reserve space for alignment
        # Determine provider code text and styling
        provider_code_text = match.provider_code if match.provider_code else ""

        # Determine if this is a project termbase or project TM
        # For termbases: explicit flag OR ranking #1 = project termbase
        is_project_tb_flag = match.match_type == 'Termbase' and match.metadata.get('is_project_termbase', False)
        is_ranking_1 = match.match_type == 'Termbase' and match.metadata.get('ranking') == 1
        is_project_tb = is_project_tb_flag or is_ranking_1
        is_project_tm = match.match_type == 'TM' and match.metadata.get('is_project_tm', False)

        provider_label = QLabel(provider_code_text)

        # Use bold font for project termbases/TMs, normal font for background resources
        font_weight = "bold" if (is_project_tb or is_project_tm) else "normal"
        # Use darker color for better visibility (changed from #888 to #333)
        provider_label.setStyleSheet(f"font-size: 7px; color: #333; padding: 0px; margin: 0px; font-weight: {font_weight};")
        provider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        provider_label.setFixedWidth(28)  # Tiny column, just wide enough for "GPT", "MMT", etc.
        provider_label.setFixedHeight(18)
        # Add tooltip with full provider name (only if code exists)
        if match.provider_code:
            provider_tooltips = {
                "GT": "Google Translate",
                "AT": "Amazon Translate",
                "MMT": "ModernMT",
                "DL": "DeepL",
                "MS": "Microsoft Translator",
                "MM": "MyMemory",
                "CL": "Claude",
                "GPT": "OpenAI",
                "GEM": "Gemini"
            }
            # Add any custom termbase codes to tooltips (they'll show termbase name from metadata)
            if match.match_type == 'Termbase' and match.metadata.get('termbase_name'):
                provider_tooltips[match.provider_code] = match.metadata.get('termbase_name', match.provider_code)
            full_name = provider_tooltips.get(match.provider_code, match.provider_code)
            provider_label.setToolTip(full_name)
        content_layout.addWidget(provider_label, 0, Qt.AlignmentFlag.AlignTop)
        
        main_layout.addLayout(content_layout, 1)  # Expand to fill remaining space
        
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # NOW call update_styling() after num_label_ref is set
        self.update_styling()
    
    def _format_text(self, text: str) -> str:
        """Format text based on show_tags setting"""
        if self.show_tags:
            # Show tags with text color
            import re
            # Escape HTML entities first to prevent double-escaping
            text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Now color the escaped tags
            tag_pattern = re.compile(r'&lt;/?[a-zA-Z][a-zA-Z0-9]*/?&gt;')
            text = tag_pattern.sub(lambda m: f'<span style="color: {self.tag_highlight_color};">{m.group()}</span>', text)
            return text
        else:
            # Let QLabel interpret as HTML (tags will be rendered/hidden)
            return text
    
    def update_tag_color(self, color: str):
        """Update tag highlight color for this item"""
        self.tag_highlight_color = color
        # Refresh text if tags are shown
        if self.show_tags and self.source_label and self.target_label:
            self.source_label.setText(self._format_text(self.match.source))
            self.target_label.setText(self._format_text(self.match.target))
    
    @classmethod
    def set_font_size(cls, size: int):
        """Set the font size for all match items"""
        cls.font_size_pt = size
    
    def update_font_size(self):
        """Update font size for this item"""
        if self.source_label:
            self.source_label.setStyleSheet(f"font-size: {self.font_size_pt}px; color: #333; padding: 0px; margin: 0px;")
        if self.target_label:
            self.target_label.setStyleSheet(f"font-size: {self.font_size_pt}px; color: #555; padding: 0px; margin: 0px;")
    
    def mousePressEvent(self, event):
        """Emit signal when clicked"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.match_selected.emit(self.match)
            self.select()
        elif event.button() == Qt.MouseButton.RightButton:
            self._show_context_menu(event.globalPosition().toPoint())
    
    def _show_context_menu(self, pos):
        """Show context menu for this match item"""
        # Only show edit option for termbase matches
        if self.match.match_type != "Termbase":
            return
        
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction
        
        menu = QMenu()
        
        # Edit entry action
        edit_action = QAction("✏️ Edit Termbase Entry", menu)
        edit_action.triggered.connect(self._edit_termbase_entry)
        menu.addAction(edit_action)
        
        # Delete entry action
        delete_action = QAction("🗑️ Delete Termbase Entry", menu)
        delete_action.triggered.connect(self._delete_termbase_entry)
        menu.addAction(delete_action)
        
        menu.exec(pos)
    
    def _edit_termbase_entry(self):
        """Open termbase entry editor for this match"""
        if self.match.match_type != "Termbase":
            return
        
        # Get term_id and termbase_id from metadata
        term_id = self.match.metadata.get('term_id')
        termbase_id = self.match.metadata.get('termbase_id')
        
        if term_id and termbase_id:
            from modules.termbase_entry_editor import TermbaseEntryEditor
            
            # Get parent window (main application)
            parent_window = self.window()
            
            dialog = TermbaseEntryEditor(
                parent=parent_window,
                db_manager=getattr(parent_window, 'db_manager', None),
                termbase_id=termbase_id,
                term_id=term_id
            )
            
            if dialog.exec():
                # Entry was edited, refresh if needed
                # Signal could be emitted here to refresh the translation results panel
                pass
    
    def _delete_termbase_entry(self):
        """Delete this termbase entry"""
        from PyQt6.QtWidgets import QMessageBox
        
        if self.match.match_type != "Termbase":
            return
        
        # Get term_id and termbase_id from metadata
        term_id = self.match.metadata.get('term_id')
        termbase_id = self.match.metadata.get('termbase_id')
        source_term = self.match.source
        target_term = self.match.target
        
        if term_id and termbase_id:
            # Confirm deletion
            parent_window = self.window()
            reply = QMessageBox.question(
                parent_window,
                "Confirm Deletion",
                f"Delete termbase entry?\n\nSource: {source_term}\nTarget: {target_term}\n\nThis action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                db_manager = getattr(parent_window, 'db_manager', None)
                if db_manager:
                    try:
                        # Log database path for debugging
                        if hasattr(parent_window, 'log'):
                            db_path = getattr(db_manager, 'db_path', 'unknown')
                            parent_window.log(f"🗑️ Deleting term ID {term_id} from database: {db_path}")
                        
                        cursor = db_manager.cursor
                        # First verify the term exists
                        cursor.execute("SELECT source_term, target_term FROM termbase_terms WHERE id = ?", (term_id,))
                        existing = cursor.fetchone()
                        if hasattr(parent_window, 'log'):
                            if existing:
                                parent_window.log(f"   Found term to delete: {existing[0]} → {existing[1]}")
                            else:
                                parent_window.log(f"   ⚠️ Term ID {term_id} not found in database!")
                        
                        # Delete the term
                        cursor.execute("DELETE FROM termbase_terms WHERE id = ?", (term_id,))
                        rows_deleted = cursor.rowcount
                        db_manager.connection.commit()
                        
                        if hasattr(parent_window, 'log'):
                            parent_window.log(f"   ✅ Deleted {rows_deleted} row(s) from database")
                        
                        # Clear termbase cache to force refresh
                        if hasattr(parent_window, 'termbase_cache'):
                            with parent_window.termbase_cache_lock:
                                parent_window.termbase_cache.clear()
                                if hasattr(parent_window, 'log'):
                                    parent_window.log(f"   ✅ Cleared termbase cache")
                        
                        # Reset the last selected row to force re-highlighting when returning to this segment
                        if hasattr(parent_window, '_last_selected_row'):
                            parent_window._last_selected_row = None
                        
                        # Trigger re-highlighting of source text to remove deleted term
                        if hasattr(parent_window, 'table') and hasattr(parent_window, 'find_termbase_matches_in_source'):
                            current_row = parent_window.table.currentRow()
                            if current_row >= 0:
                                # Get source text widget
                                source_widget = parent_window.table.cellWidget(current_row, 2)
                                if source_widget and hasattr(source_widget, 'toPlainText'):
                                    source_text = source_widget.toPlainText()
                                    # Re-find matches and re-highlight
                                    termbase_matches = parent_window.find_termbase_matches_in_source(source_text)
                                    if hasattr(source_widget, 'highlight_termbase_matches'):
                                        source_widget.highlight_termbase_matches(termbase_matches)
                                    # Update the widget's stored matches to reflect the deletion
                                    if hasattr(source_widget, 'termbase_matches'):
                                        source_widget.termbase_matches = termbase_matches
                        
                        QMessageBox.information(parent_window, "Success", "Termbase entry deleted")
                        # Hide this match card since it's been deleted
                        self.hide()
                    except Exception as e:
                        QMessageBox.critical(parent_window, "Error", f"Failed to delete entry: {e}")
    
    def select(self):
        """Select this match"""
        self.is_selected = True
        self.update_styling()
    
    def deselect(self):
        """Deselect this match"""
        self.is_selected = False
        self.update_styling()
    
    def update_styling(self):
        """Update visual styling based on selection state and match type"""
        # Color code by match type: LLM=purple, TM=red, Termbase=green, MT=orange, NT=gray, NonTrans=yellow
        base_color_map = {
            "LLM": "#9c27b0",  # Purple for LLM translations
            "TM": "#ff6b6b",  # Red for Translation Memory
            "Termbase": "#4CAF50",  # Green for all termbase matches (Material Design Green 500)
            "MT": "#ff9800",  # Orange for Machine Translation
            "NT": "#adb5bd",  # Gray for New Translation
            "NonTrans": "#E6C200"  # Pastel yellow for Non-Translatables
        }

        base_color = base_color_map.get(self.match.match_type, "#adb5bd")
        
        # Special styling for Non-Translatables
        if self.match.match_type == "NonTrans":
            type_color = "#FFFDD0"  # Pastel yellow background
        # For termbase matches, apply ranking-based green shading
        elif self.match.match_type == "Termbase":
            is_forbidden = self.match.metadata.get('forbidden', False)
            is_project_termbase_flag = self.match.metadata.get('is_project_termbase', False)
            termbase_ranking = self.match.metadata.get('ranking', None)

            # EFFECTIVE project termbase = explicit flag OR ranking #1
            is_effective_project = is_project_termbase_flag or (termbase_ranking == 1)
            is_project_termbase = is_effective_project  # For later use in background styling

            if is_forbidden:
                type_color = "#000000"  # Forbidden terms: black
            else:
                # Use ranking to determine SOFT pastel green shade
                # All shades are subtle to stay in the background
                if termbase_ranking is not None:
                    # Map ranking to soft pastel green shades:
                    # Ranking #1: Soft medium green (Green 200)
                    # Ranking #2: Soft light green (Green 100)
                    # Ranking #3: Very soft light green (Light Green 100)
                    # Ranking #4+: Extremely soft pastel green (Green 50)
                    ranking_colors = {
                        1: "#A5D6A7",  # Soft medium green (Green 200)
                        2: "#C8E6C9",  # Soft light green (Green 100)
                        3: "#DCEDC8",  # Very soft light green (Light Green 100)
                    }
                    type_color = ranking_colors.get(termbase_ranking, "#E8F5E9")  # Green 50 for 4+ (Extremely soft)
                else:
                    # No ranking - use soft light green
                    type_color = "#C8E6C9"  # Green 100 (fallback)
        else:
            type_color = base_color
        
        # Update styling only for the number label, not the entire item
        if hasattr(self, 'num_label_ref') and self.num_label_ref:
            if self.is_selected:
                # Selected: darker shade of type color with white text
                darker_color = self._darken_color(type_color)
                self.num_label_ref.setStyleSheet(f"""
                    QLabel {{
                        background-color: {darker_color};
                        color: white;
                        font-weight: bold;
                        font-size: 9px;
                        min-width: 20px;
                        padding: 2px;
                        border-radius: 2px;
                    }}
                """)
                # Add background to the entire item only when selected
                self.setStyleSheet(f"""
                    CompactMatchItem {{
                        background-color: {self._lighten_color(type_color, 0.95)};
                        border: 1px solid {type_color};
                    }}
                """)
            else:
                # Unselected: number badge colored (same styling for all match types)
                self.num_label_ref.setStyleSheet(f"""
                    QLabel {{
                        background-color: {type_color};
                        color: white;
                        font-weight: bold;
                        font-size: 9px;
                        min-width: 20px;
                        padding: 1px;
                        border-radius: 2px;
                    }}
                """)
                # All matches have white background with subtle hover effect
                self.setStyleSheet("""
                    CompactMatchItem {
                        background-color: white;
                        border: none;
                    }
                    CompactMatchItem:hover {
                        background-color: #f5f5f5;
                    }
                """)
    
    @staticmethod
    def _lighten_color(hex_color: str, factor: float) -> str:
        """Lighten a hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r + (255 - r) * (1 - factor))
        g = int(g + (255 - g) * (1 - factor))
        b = int(b + (255 - b) * (1 - factor))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    @staticmethod
    def _darken_color(hex_color: str, factor: float = 0.7) -> str:
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def mouseMoveEvent(self, event):
        """Support drag/drop"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.match.target)
            mime_data.setData("application/x-match", str(self.match.target).encode())
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)


class MatchSection(QWidget):
    """Stacked section for a match type (NT/MT/TM/Termbases)"""
    
    match_selected = pyqtSignal(TranslationMatch)
    
    def __init__(self, title: str, matches: List[TranslationMatch], parent=None, global_number_start: int = 1):
        super().__init__(parent)
        self.title = title
        self.matches = matches
        self.is_expanded = True
        self.match_items = []
        self.selected_index = -1
        self.global_number_start = global_number_start  # For global numbering across sections
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Section header (collapsible)
        header = self._create_header()
        layout.addWidget(header)
        
        # Matches container
        self.matches_container = QWidget()
        self.matches_layout = QVBoxLayout(self.matches_container)
        self.matches_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.matches_layout.setSpacing(0)  # No spacing between matches
        
        # Populate with matches
        self._populate_matches()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.matches_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: white; }")
        layout.addWidget(self.scroll_area)
    
    def _create_header(self) -> QWidget:
        """Create collapsible header"""
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(4, 2, 4, 2)
        
        # Toggle button
        self.toggle_btn = QPushButton("▼" if self.is_expanded else "▶")
        self.toggle_btn.setMaximumWidth(20)
        self.toggle_btn.setMaximumHeight(20)
        self.toggle_btn.setFlat(True)
        self.toggle_btn.clicked.connect(self._toggle_section)
        header_layout.addWidget(self.toggle_btn)
        
        # Title + match count
        title_text = f"{self.title}"
        if self.matches:
            title_text += f" ({len(self.matches)})"
        
        title_label = QLabel(title_text)
        title_label.setStyleSheet("font-weight: bold; font-size: 10px; color: #333;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        header.setStyleSheet("""
            background-color: #f0f0f0;
            border-bottom: 1px solid #ddd;
            padding: 2px;
        """)
        
        return header
    
    def _populate_matches(self):
        """Populate section with matches using global numbering"""
        for local_idx, match in enumerate(self.matches):
            global_number = self.global_number_start + local_idx
            item = CompactMatchItem(match, match_number=global_number)
            item.match_selected.connect(lambda m, i=local_idx: self._on_match_selected(m, i))
            self.matches_layout.addWidget(item)
            self.match_items.append(item)
        
        self.matches_layout.addStretch()
    
    def _toggle_section(self):
        """Toggle section expansion"""
        self.is_expanded = not self.is_expanded
        self.toggle_btn.setText("▼" if self.is_expanded else "▶")
        self.scroll_area.setVisible(self.is_expanded)
    
    def _on_match_selected(self, match: TranslationMatch, index: int):
        """Handle match selection"""
        # Deselect previous
        if 0 <= self.selected_index < len(self.match_items):
            self.match_items[self.selected_index].deselect()
        
        # Select new
        self.selected_index = index
        if 0 <= index < len(self.match_items):
            self.match_items[index].select()
        
        self.match_selected.emit(match)
    
    def select_by_number(self, number: int):
        """Select match by number (1-based)"""
        if 1 <= number <= len(self.match_items):
            self._on_match_selected(self.matches[number-1], number-1)
            # Scroll to visible
            self.scroll_area.ensureWidgetVisible(self.match_items[number-1])
    
    def navigate(self, direction: int):
        """Navigate matches: direction=1 for next, -1 for previous"""
        new_index = self.selected_index + direction
        if 0 <= new_index < len(self.match_items):
            self._on_match_selected(self.matches[new_index], new_index)
            self.scroll_area.ensureWidgetVisible(self.match_items[new_index])
            return True
        return False


class TranslationResultsPanel(QWidget):
    """
    Main translation results panel (right side of editor)
    Compact memoQ-style design with stacked match sections
    
    Features:
    - Keyboard navigation: Up/Down arrows to cycle through matches
    - Insert selected match: Press Enter
    - Quick insert by number: Ctrl+1 through Ctrl+9 (1-based index)
    - Vertical compare boxes with resizable splitter
    - Match numbering display
    - Zoom controls for both match list and compare boxes
    """
    
    match_selected = pyqtSignal(TranslationMatch)
    match_inserted = pyqtSignal(str)  # Emitted when user wants to insert match into target
    
    # Class variables for font sizes
    compare_box_font_size = 9
    
    def __init__(self, parent=None, parent_app=None):
        super().__init__(parent)
        self.parent_app = parent_app  # Reference to main app for settings access
        self.matches_by_type: Dict[str, List[TranslationMatch]] = {}
        self.current_selection: Optional[TranslationMatch] = None
        self.all_matches: List[TranslationMatch] = []
        self.match_sections: Dict[str, MatchSection] = {}
        self.match_items: List[CompactMatchItem] = []
        self.selected_index = -1
        self.compare_text_edits = []  # Track compare boxes for font size updates
        self.setup_ui()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Ensure widget receives keyboard events

    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        
        # Header with segment info
        self.segment_label = QLabel("No segment selected")
        self.segment_label.setStyleSheet("font-weight: bold; font-size: 10px; color: #666;")
        layout.addWidget(self.segment_label)
        
        # Use splitter for resizable sections (matches vs compare boxes)
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.setStyleSheet("QSplitter::handle { background-color: #e0e0e0; }")
        
        # Matches scroll area
        self.matches_scroll = QScrollArea()
        self.matches_scroll.setWidgetResizable(True)
        self.matches_scroll.setStyleSheet("""
            QScrollArea { 
                border: 1px solid #ddd; 
                background-color: white;
                border-radius: 3px;
            }
        """)
        
        self.matches_container = QWidget()
        self.main_layout = QVBoxLayout(self.matches_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(2)
        
        self.matches_scroll.setWidget(self.matches_container)
        main_splitter.addWidget(self.matches_scroll)
        
        # Compare box (shown when TM match selected) - VERTICAL STACKED LAYOUT
        self.compare_frame = self._create_compare_box()
        main_splitter.addWidget(self.compare_frame)
        self.compare_frame.hide()  # Hidden by default
        
        # TM metadata info panel (shown below compare box when TM match selected)
        self.tm_info_frame = self._create_tm_info_panel()
        main_splitter.addWidget(self.tm_info_frame)
        self.tm_info_frame.hide()  # Hidden by default
        
        # Termbase data viewer (shown when termbase match selected)
        self.termbase_frame = self._create_termbase_viewer()
        main_splitter.addWidget(self.termbase_frame)
        self.termbase_frame.hide()  # Hidden by default
        
        # Notes section with its own container
        notes_widget = QWidget()
        notes_layout = QVBoxLayout(notes_widget)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        notes_layout.setSpacing(2)
        
        notes_label = QLabel("📝 Notes (segment annotations)")
        notes_label.setStyleSheet("font-weight: bold; font-size: 9px; color: #333;")
        notes_layout.addWidget(notes_label)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setPlaceholderText("Add notes about this segment, context, or translation concerns...")
        self.notes_edit.setStyleSheet("font-size: 9px; padding: 4px;")
        notes_layout.addWidget(self.notes_edit)
        
        main_splitter.addWidget(notes_widget)
        
        # Set splitter proportions (50% matches, 35% compare, 15% notes)
        main_splitter.setSizes([500, 350, 150])
        main_splitter.setCollapsible(0, False)
        main_splitter.setCollapsible(1, True)
        main_splitter.setCollapsible(2, False)
        
        layout.addWidget(main_splitter)
    
    def _create_compare_box(self) -> QFrame:
        """Create compare box frame with VERTICAL stacked layout - all boxes resize together"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 4px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        
        # Title
        title = QLabel("📊 Compare Box")
        title.setStyleSheet("font-weight: bold; font-size: 9px; color: #666;")
        layout.addWidget(title)
        
        # Box 1: Current Source
        box1 = self._create_compare_text_box("Current Source:", "#e3f2fd")
        self.compare_current = box1[1]
        self.compare_current_label = box1[2]
        layout.addWidget(box1[0], 1)  # stretch factor 1
        
        # Box 2: TM Source (with diff highlighting capability)
        box2 = self._create_compare_text_box("TM Source:", "#fff3cd")
        self.compare_tm_source = box2[1]
        self.compare_source_label = box2[2]
        self.compare_source_container = box2[0]
        layout.addWidget(box2[0], 1)  # stretch factor 1
        
        # Box 3: TM Target
        box3 = self._create_compare_text_box("TM Target:", "#d4edda")
        self.compare_tm_target = box3[1]
        self.compare_target_label = box3[2]
        layout.addWidget(box3[0], 1)  # stretch factor 1
        
        return frame
    
    def _create_compare_text_box(self, label: str, bg_color: str) -> tuple:
        """Create a single compare text box"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-weight: bold; font-size: 8px; color: #666;")
        layout.addWidget(label_widget)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg_color};
                border: 1px solid #ccc;
                border-radius: 2px;
                font-size: {self.compare_box_font_size}px;
                padding: 4px;
                margin: 0px;
            }}
        """)
        layout.addWidget(text_edit)
        
        # Track this text edit for font size updates
        self.compare_text_edits.append(text_edit)
        
        return (container, text_edit, label_widget)
    
    def _create_termbase_viewer(self) -> QFrame:
        """Create termbase data viewer frame"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 4px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Title with termbase name (will be updated dynamically)
        header_layout = QHBoxLayout()
        self.termbase_title = QLabel("📖 Term Info")
        self.termbase_title.setStyleSheet("font-weight: bold; font-size: 9px; color: #666;")
        header_layout.addWidget(self.termbase_title)
        header_layout.addStretch()
        
        # Refresh button
        self.termbase_refresh_btn = QPushButton("🔄 Refresh data")
        self.termbase_refresh_btn.setStyleSheet("""
            QPushButton {
                font-size: 8px;
                padding: 2px 6px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.termbase_refresh_btn.setFixedHeight(20)
        self.termbase_refresh_btn.setToolTip("Refresh entry from database")
        self.termbase_refresh_btn.clicked.connect(self._on_refresh_termbase_entry)
        header_layout.addWidget(self.termbase_refresh_btn)
        
        # Edit button
        self.termbase_edit_btn = QPushButton("✏️ Edit")
        self.termbase_edit_btn.setStyleSheet("""
            QPushButton {
                font-size: 8px;
                padding: 2px 6px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.termbase_edit_btn.setFixedHeight(20)
        self.termbase_edit_btn.clicked.connect(self._on_edit_termbase_entry)
        header_layout.addWidget(self.termbase_edit_btn)
        
        layout.addLayout(header_layout)
        
        # Source and Target terms
        terms_container = QWidget()
        terms_layout = QVBoxLayout(terms_container)
        terms_layout.setContentsMargins(2, 2, 2, 2)
        terms_layout.setSpacing(3)
        
        # Source term
        source_label = QLabel("Source Term:")
        source_label.setStyleSheet("font-weight: bold; font-size: 8px; color: #666;")
        terms_layout.addWidget(source_label)
        
        self.termbase_source = QLabel()
        self.termbase_source.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #ccc;
                border-radius: 2px;
                font-size: 10px;
                padding: 6px;
                margin: 0px;
            }
        """)
        self.termbase_source.setWordWrap(True)
        terms_layout.addWidget(self.termbase_source)
        
        # Target term
        target_label = QLabel("Target Term:")
        target_label.setStyleSheet("font-weight: bold; font-size: 8px; color: #666;")
        terms_layout.addWidget(target_label)
        
        self.termbase_target = QLabel()
        self.termbase_target.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                border: 1px solid #ccc;
                border-radius: 2px;
                font-size: 10px;
                padding: 6px;
                margin: 0px;
            }
        """)
        self.termbase_target.setWordWrap(True)
        terms_layout.addWidget(self.termbase_target)
        
        layout.addWidget(terms_container)
        
        # Metadata area
        metadata_label = QLabel("Metadata:")
        metadata_label.setStyleSheet("font-weight: bold; font-size: 8px; color: #666;")
        layout.addWidget(metadata_label)
        
        from PyQt6.QtWidgets import QTextBrowser
        self.termbase_metadata = QTextBrowser()
        self.termbase_metadata.setReadOnly(True)
        self.termbase_metadata.setMaximumHeight(80)
        self.termbase_metadata.setStyleSheet(f"""
            QTextBrowser {{
                background-color: #fff3cd;
                border: 1px solid #ccc;
                border-radius: 2px;
                font-size: {self.compare_box_font_size}px;
                padding: 4px;
                margin: 0px;
            }}
        """)
        # Enable clickable links
        self.termbase_metadata.setOpenExternalLinks(True)
        layout.addWidget(self.termbase_metadata)
        
        # Track metadata text edit for font size updates
        self.compare_text_edits.append(self.termbase_metadata)
        
        return frame
    
    def _create_tm_info_panel(self) -> QFrame:
        """Create TM metadata info panel (memoQ-style) - shown when TM match is selected"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 4px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(3)
        
        # Title
        title = QLabel("💾 TM Info")
        title.setStyleSheet("font-weight: bold; font-size: 9px; color: #666; margin-bottom: 2px;")
        layout.addWidget(title)
        
        # Info grid (compact 2-column layout)
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)
        
        # TM Name
        self.tm_name_label = QLabel()
        self.tm_name_label.setStyleSheet("font-size: 9px; color: #333; font-weight: bold;")
        self.tm_name_label.setWordWrap(True)
        info_layout.addWidget(self.tm_name_label)
        
        # Languages (smaller)
        self.tm_languages_label = QLabel()
        self.tm_languages_label.setStyleSheet("font-size: 8px; color: #666;")
        info_layout.addWidget(self.tm_languages_label)
        
        # Entry count and modified date in single line
        self.tm_stats_label = QLabel()
        self.tm_stats_label.setStyleSheet("font-size: 8px; color: #666;")
        self.tm_stats_label.setWordWrap(True)
        info_layout.addWidget(self.tm_stats_label)
        
        # Description (if available)
        self.tm_description_label = QLabel()
        self.tm_description_label.setStyleSheet("""
            QLabel {
                font-size: 8px;
                color: #555;
                background-color: #fff;
                padding: 3px;
                border: 1px solid #ddd;
                border-radius: 2px;
            }
        """)
        self.tm_description_label.setWordWrap(True)
        self.tm_description_label.hide()  # Hidden if no description
        info_layout.addWidget(self.tm_description_label)
        
        layout.addWidget(info_container)
        
        return frame
    
    def _on_edit_termbase_entry(self):
        """Handle edit button click - open termbase entry editor dialog"""
        if not self.current_selection or self.current_selection.match_type != "Termbase":
            return
        
        # Get term_id from metadata if available
        term_id = self.current_selection.metadata.get('term_id')
        termbase_id = self.current_selection.metadata.get('termbase_id')
        
        if term_id and termbase_id:
            # Import and show editor dialog
            from modules.termbase_entry_editor import TermbaseEntryEditor
            
            # Get parent window (main application)
            parent_window = self.window()
            
            dialog = TermbaseEntryEditor(
                parent=parent_window,
                db_manager=getattr(parent_window, 'db_manager', None),
                termbase_id=termbase_id,
                term_id=term_id
            )
            
            if dialog.exec():
                # Entry was edited, refresh the display
                # Get updated term data and refresh the termbase viewer
                self._refresh_termbase_viewer()
    
    def _on_refresh_termbase_entry(self):
        """Handle refresh button click - reload entry from database"""
        if not self.current_selection or self.current_selection.match_type != "Termbase":
            return
        
        # Get term_id from metadata
        term_id = self.current_selection.metadata.get('term_id')
        if not term_id:
            return
        
        # Get parent window and database manager
        parent_window = self.window()
        db_manager = getattr(parent_window, 'db_manager', None)
        
        if not db_manager:
            return
        
        try:
            # Fetch fresh data from database
            cursor = db_manager.cursor
            cursor.execute("""
                SELECT source_term, target_term, priority, domain, notes, 
                       project, client, forbidden, termbase_id
                FROM termbase_terms
                WHERE id = ?
            """, (term_id,))
            
            row = cursor.fetchone()
            if row:
                # Update the current selection metadata with fresh data
                self.current_selection.source = row[0]
                self.current_selection.target = row[1]
                self.current_selection.metadata['priority'] = row[2] or 99
                self.current_selection.metadata['domain'] = row[3] or ''
                self.current_selection.metadata['notes'] = row[4] or ''
                self.current_selection.metadata['project'] = row[5] or ''
                self.current_selection.metadata['client'] = row[6] or ''
                self.current_selection.metadata['forbidden'] = row[7] or False
                self.current_selection.metadata['termbase_id'] = row[8]
                
                # Re-display with updated data
                self._display_termbase_data(self.current_selection)
                
        except Exception as e:
            print(f"Error refreshing termbase entry: {e}")
    
    def _refresh_termbase_viewer(self):
        """Refresh termbase viewer with latest data from database"""
        if not self.current_selection or self.current_selection.match_type != "Termbase":
            return
        
        # Use the refresh handler to fetch and display fresh data
        self._on_refresh_termbase_entry()
    
    def _display_termbase_data(self, match: TranslationMatch):
        """Display termbase entry data in the viewer"""
        # Keep consistent "Term Info" title
        self.termbase_title.setText("📖 Term Info")
        
        # Display source and target terms
        self.termbase_source.setText(match.source)
        
        # Include synonyms in target display if available
        target_synonyms = match.metadata.get('target_synonyms', [])
        if target_synonyms:
            # Show main term with synonyms
            synonyms_text = ", ".join(target_synonyms)
            self.termbase_target.setText(f"{match.target} | {synonyms_text}")
        else:
            self.termbase_target.setText(match.target)
        
        # Build metadata text
        metadata_parts = []
        
        # Termbase name
        termbase_name = match.metadata.get('termbase_name', 'Unknown')
        metadata_parts.append(f"<b>Termbase:</b> {termbase_name}")
        
        # Priority
        priority = match.metadata.get('priority', 50)
        metadata_parts.append(f"<b>Priority:</b> {priority}")
        
        # Domain
        domain = match.metadata.get('domain', '')
        if domain:
            metadata_parts.append(f"<b>Domain:</b> {domain}")
        
        # Notes
        notes = match.metadata.get('notes', '')
        if notes:
            # Truncate long notes for display
            if len(notes) > 200:
                notes = notes[:200] + "..."
            # Convert URLs to clickable links
            import re
            url_pattern = r'(https?://[^\s]+)'
            notes = re.sub(url_pattern, r'<a href="\1">\1</a>', notes)
            metadata_parts.append(f"<b>Notes:</b> {notes}")
        
        # Project
        project = match.metadata.get('project', '')
        if project:
            metadata_parts.append(f"<b>Project:</b> {project}")
        
        # Client
        client = match.metadata.get('client', '')
        if client:
            metadata_parts.append(f"<b>Client:</b> {client}")
        
        # Forbidden status
        forbidden = match.metadata.get('forbidden', False)
        if forbidden:
            metadata_parts.append("<b><span style='color: red;'>⚠️ FORBIDDEN TERM</span></b>")
        
        # Term ID (for debugging)
        term_id = match.metadata.get('term_id', '')
        if term_id:
            metadata_parts.append(f"<span style='color: #888; font-size: 7px;'>Term ID: {term_id}</span>")
        
        metadata_html = "<br>".join(metadata_parts) if metadata_parts else "<i>No metadata</i>"
        self.termbase_metadata.setHtml(metadata_html)
    
    def _display_tm_metadata(self, match: TranslationMatch):
        """Display TM metadata in the info panel (memoQ-style)"""
        # Get TM metadata from match
        tm_name = match.metadata.get('tm_name', 'Unknown TM')
        tm_id = match.metadata.get('tm_id', '')
        source_lang = match.metadata.get('source_lang', '')
        target_lang = match.metadata.get('target_lang', '')
        entry_count = match.metadata.get('entry_count', 0)
        modified_date = match.metadata.get('modified_date', '')
        description = match.metadata.get('description', '')
        
        # Update TM name
        self.tm_name_label.setText(f"📝 {tm_name}")
        
        # Update languages
        if source_lang and target_lang:
            self.tm_languages_label.setText(f"🌐 {source_lang} → {target_lang}")
        else:
            self.tm_languages_label.setText("")
        
        # Update stats (entry count + modified date)
        stats_parts = []
        if entry_count:
            stats_parts.append(f"📊 {entry_count:,} entries")
        if modified_date:
            # Format date nicely if it's ISO format
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(modified_date)
                formatted_date = dt.strftime("%Y-%m-%d %H:%M")
                stats_parts.append(f"🕒 Modified: {formatted_date}")
            except:
                stats_parts.append(f"🕒 {modified_date}")
        
        self.tm_stats_label.setText(" • ".join(stats_parts) if stats_parts else "")
        
        # Update description (show/hide based on content)
        if description and description.strip():
            self.tm_description_label.setText(f"💬 {description}")
            self.tm_description_label.show()
        else:
            self.tm_description_label.hide()
    
    def add_matches(self, new_matches_dict: Dict[str, List[TranslationMatch]]):
        """
        Add new matches to existing matches (for progressive loading)
        Merges new matches with existing ones and re-renders the display
        Includes deduplication to prevent showing identical matches
        
        Args:
            new_matches_dict: Dict with keys like "NT", "MT", "TM", "Termbases"
        """
        # Merge new matches with existing matches_by_type
        if not hasattr(self, 'matches_by_type') or not self.matches_by_type:
            # No existing matches, just set them
            self.set_matches(new_matches_dict)
            return
        
        # Merge: Update existing match types with new matches (with deduplication)
        for match_type, new_matches in new_matches_dict.items():
            if new_matches:  # Only merge non-empty lists
                if match_type in self.matches_by_type:
                    # Deduplicate: Only add matches that don't already exist
                    existing_targets = {match.target for match in self.matches_by_type[match_type]}
                    unique_new_matches = [m for m in new_matches if m.target not in existing_targets]
                    if unique_new_matches:
                        self.matches_by_type[match_type].extend(unique_new_matches)
                else:
                    # New match type, add it
                    self.matches_by_type[match_type] = new_matches
        
        # Re-render with merged matches
        self.set_matches(self.matches_by_type)

    def _sort_termbase_matches(self, matches: List[TranslationMatch]) -> List[TranslationMatch]:
        """
        Sort termbase matches based on user preference.

        Args:
            matches: List of termbase matches

        Returns:
            Sorted list of matches
        """
        if not self.parent_app:
            return matches  # No sorting if no parent app

        sort_order = getattr(self.parent_app, 'termbase_display_order', 'appearance')

        if sort_order == 'alphabetical':
            # Sort alphabetically by source term (case-insensitive)
            return sorted(matches, key=lambda m: m.source.lower())
        elif sort_order == 'length':
            # Sort by source term length (longest first)
            return sorted(matches, key=lambda m: len(m.source), reverse=True)
        elif sort_order == 'appearance':
            # Sort by position in source text (if available in metadata)
            # If position not available, keep original order
            def get_position(match):
                pos = match.metadata.get('position_in_source', -1)
                # If no position, put at end
                return pos if pos >= 0 else 999999
            return sorted(matches, key=get_position)
        else:
            # Default: keep original order
            return matches

    def _filter_shorter_matches(self, matches: List[TranslationMatch]) -> List[TranslationMatch]:
        """
        Filter out shorter termbase matches that are substrings of longer matches.

        Args:
            matches: List of termbase matches

        Returns:
            Filtered list with shorter substring matches removed
        """
        if not self.parent_app:
            return matches  # No filtering if no parent app

        hide_shorter = getattr(self.parent_app, 'termbase_hide_shorter_matches', False)

        if not hide_shorter:
            return matches

        # Create a list to track which matches to keep
        filtered_matches = []

        for i, match in enumerate(matches):
            # Check if this match's source is a substring of any other match's source
            is_substring = False
            source_lower = match.source.lower()

            for j, other_match in enumerate(matches):
                if i == j:
                    continue
                other_source_lower = other_match.source.lower()

                # Check if current match is a substring of the other match
                # and is shorter than the other match
                if (source_lower in other_source_lower and
                    len(source_lower) < len(other_source_lower)):
                    is_substring = True
                    break

            # Keep the match if it's not a substring of a longer match
            if not is_substring:
                filtered_matches.append(match)

        return filtered_matches

    def set_matches(self, matches_dict: Dict[str, List[TranslationMatch]]):
        """
        Set matches from different sources in unified flat list with GLOBAL consecutive numbering
        (memoQ-style: single grid, color coding only identifies match type)
        
        Args:
            matches_dict: Dict with keys like "NT", "MT", "TM", "Termbases"
        """
        print(f"🎯 TranslationResultsPanel.set_matches() called with matches_dict keys: {list(matches_dict.keys())}")
        for match_type, matches in matches_dict.items():
            print(f"  {match_type}: {len(matches)} matches")
            if match_type == "Termbases" and matches:
                for i, match in enumerate(matches[:2]):  # Show first 2 for debugging
                    print(f"    [{i}] {match.source} → {match.target}")
        
        # Store current matches for delayed search access
        self._current_matches = matches_dict.copy()
        self.matches_by_type = matches_dict
        self.all_matches = []
        self.match_items = []  # Track all match items for navigation
        self.selected_index = -1
        
        # Clear existing matches
        while self.main_layout.count() > 0:
            item = self.main_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        # Apply match limits per type (configurable, defaults provided)
        match_limits = getattr(self, 'match_limits', {
            "LLM": 3,
            "NT": 5,
            "MT": 3,
            "TM": 5,
            "Termbases": 10,
            "NonTrans": 20  # Non-translatables (show more since they're important)
        })
        
        # Build flat list of all matches with global numbering
        global_number = 1
        order = ["LLM", "NonTrans", "NT", "MT", "TM", "Termbases"]  # LLM first, NonTrans early (important for translator)
        
        for match_type in order:
            if match_type in matches_dict and matches_dict[match_type]:
                # Get matches for this type
                type_matches = matches_dict[match_type]

                # Apply sorting and filtering for termbase matches
                if match_type == "Termbases":
                    # First filter out shorter substring matches (if enabled)
                    type_matches = self._filter_shorter_matches(type_matches)
                    # Then sort according to user preference
                    type_matches = self._sort_termbase_matches(type_matches)

                # Apply limit for this match type
                limit = match_limits.get(match_type, 5)
                limited_matches = type_matches[:limit]

                for match in limited_matches:
                    self.all_matches.append(match)
                    
                    # Create match item with global number
                    item = CompactMatchItem(match, match_number=global_number)
                    item.match_selected.connect(lambda m, idx=len(self.match_items): self._on_match_item_selected(m, idx))
                    self.main_layout.addWidget(item)
                    self.match_items.append(item)
                    
                    global_number += 1
        
        self.main_layout.addStretch()
    
    def _on_match_item_selected(self, match: TranslationMatch, index: int):
        """Handle match item selection"""
        # Deselect previous
        if 0 <= self.selected_index < len(self.match_items):
            self.match_items[self.selected_index].deselect()
        
        # Select new
        self.selected_index = index
        if 0 <= index < len(self.match_items):
            self.match_items[index].select()
        
        self._on_match_selected(match)
    
    def _on_match_selected(self, match: TranslationMatch):
        """Handle match selection"""
        print(f"🔍 DEBUG: _on_match_selected called with match_type='{match.match_type}'")
        self.current_selection = match
        self.match_selected.emit(match)
        
        # Show appropriate viewer based on match type
        if match.match_type == "TM" and match.compare_source:
            # Show TM compare box
            print("📊 DEBUG: Showing TM compare box")
            self.compare_frame.show()
            self.tm_info_frame.show()  # Show TM metadata below compare box
            self.termbase_frame.hide()
            
            # Update labels for TM
            self.compare_source_label.setText("TM Source:")
            self.compare_target_label.setText("TM Target:")
            self.compare_source_container.show()  # Show TM source box
            
            # Current source is already set via set_segment_info
            self.compare_tm_source.setText(match.compare_source)
            self.compare_tm_target.setText(match.target)
            
            # Populate TM metadata panel
            self._display_tm_metadata(match)
            
        elif match.match_type in ("MT", "LLM") and match.compare_source:
            # Show MT/LLM compare box (simplified - just current source and translation)
            print(f"🤖 DEBUG: Showing {match.match_type} compare box")
            self.compare_frame.show()
            self.tm_info_frame.hide()  # No TM metadata for MT/LLM
            self.termbase_frame.hide()
            
            # Update labels for MT/LLM
            provider_name = match.metadata.get('provider', match.match_type)
            self.compare_source_container.hide()  # Hide source box for MT/LLM (source = current)
            self.compare_target_label.setText(f"{match.match_type} Translation ({provider_name}):")
            
            # Set target text
            self.compare_tm_target.setText(match.target)
            
        elif match.match_type == "Termbase":
            # Show termbase data viewer
            print("📖 DEBUG: Showing termbase viewer!")
            self.compare_frame.hide()
            self.tm_info_frame.hide()
            self.termbase_frame.show()
            self._display_termbase_data(match)
        else:
            # Hide all viewers
            print(f"❌ DEBUG: Match type '{match.match_type}' - hiding all viewers")
            self.compare_frame.hide()
            self.tm_info_frame.hide()
            self.termbase_frame.hide()
    
    def set_segment_info(self, segment_num: int, source_text: str):
        """Update segment info display"""
        self.segment_label.setText(f"Segment {segment_num}: {source_text[:50]}...")
        self.compare_current.setText(source_text)
    
    def clear(self):
        """Clear all matches"""
        self.matches_by_type = {}
        self.current_selection = None
        self.all_matches = []
        self.compare_frame.hide()
        self.tm_info_frame.hide()
        self.termbase_frame.hide()
        self.notes_edit.clear()
        
        while self.main_layout.count() > 0:
            item = self.main_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
    
    def get_selected_match(self) -> Optional[TranslationMatch]:
        """Get currently selected match"""
        return self.current_selection
    
    def set_font_size(self, size: int):
        """Set font size for all match items (for zoom control)"""
        CompactMatchItem.set_font_size(size)
        # Update all currently displayed items
        for item in self.match_items:
            item.update_font_size()
            item.adjustSize()
        self.matches_scroll.update()
    
    def set_compare_box_font_size(self, size: int):
        """Set font size for compare boxes"""
        TranslationResultsPanel.compare_box_font_size = size
        for text_edit in self.compare_text_edits:
            text_edit.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {self._get_box_color(text_edit)};
                    border: 1px solid #ccc;
                    border-radius: 2px;
                    font-size: {size}px;
                    padding: 4px;
                    margin: 0px;
                }}
            """)
    
    def set_show_tags(self, show: bool):
        """Set whether to show HTML/XML tags in matches"""
        CompactMatchItem.show_tags = show
        # Refresh all match items
        for item in self.match_items:
            if hasattr(item, 'source_label') and hasattr(item, 'target_label'):
                # Always use RichText (needed for both tag rendering and highlighting)
                item.source_label.setTextFormat(Qt.TextFormat.RichText)
                item.target_label.setTextFormat(Qt.TextFormat.RichText)
                # Refresh text
                item.source_label.setText(item._format_text(item.match.source))
                item.target_label.setText(item._format_text(item.match.target))
    
    def set_tag_color(self, color: str):
        """Set tag highlight color for all match items"""
        CompactMatchItem.tag_highlight_color = color
        # Refresh all match items to apply new color
        for item in self.match_items:
            if hasattr(item, 'update_tag_color'):
                item.update_tag_color(color)
    
    def _get_box_color(self, text_edit) -> str:
        """Get background color for a compare box (mapping hack)"""
        # This is a workaround - in production, store colors with the widgets
        colors = ["#e3f2fd", "#fff3cd", "#d4edda"]
        if text_edit in self.compare_text_edits:
            return colors[self.compare_text_edits.index(text_edit) % len(colors)]
        return "#fafafa"
    
    def zoom_in(self):
        """Increase font size for both match list and compare boxes"""
        new_size = CompactMatchItem.font_size_pt + 1
        if new_size <= 16:  # Max 16pt
            self.set_font_size(new_size)
            # Also increase compare boxes
            compare_size = TranslationResultsPanel.compare_box_font_size + 1
            if compare_size <= 14:
                self.set_compare_box_font_size(compare_size)
            return new_size
        return CompactMatchItem.font_size_pt
    
    def zoom_out(self):
        """Decrease font size for both match list and compare boxes"""
        new_size = CompactMatchItem.font_size_pt - 1
        if new_size >= 7:  # Min 7pt
            self.set_font_size(new_size)
            # Also decrease compare boxes
            compare_size = TranslationResultsPanel.compare_box_font_size - 1
            if compare_size >= 7:
                self.set_compare_box_font_size(compare_size)
            return new_size
        return CompactMatchItem.font_size_pt
    
    def reset_zoom(self):
        """Reset font size to defaults"""
        self.set_font_size(9)
        self.set_compare_box_font_size(9)
        return 9
    
    def select_previous_match(self):
        """Navigate to previous match (Ctrl+Up from main window)"""
        if self.selected_index > 0:
            new_index = self.selected_index - 1
            self._on_match_item_selected(self.all_matches[new_index], new_index)
            # Scroll to make it visible
            if 0 <= new_index < len(self.match_items):
                self.matches_scroll.ensureWidgetVisible(self.match_items[new_index])
        elif self.selected_index == -1 and self.all_matches:
            # No selection, select last match
            new_index = len(self.all_matches) - 1
            self._on_match_item_selected(self.all_matches[new_index], new_index)
            if 0 <= new_index < len(self.match_items):
                self.matches_scroll.ensureWidgetVisible(self.match_items[new_index])
    
    def select_next_match(self):
        """Navigate to next match (Ctrl+Down from main window)"""
        if self.selected_index < len(self.all_matches) - 1:
            new_index = self.selected_index + 1
            self._on_match_item_selected(self.all_matches[new_index], new_index)
            # Scroll to make it visible
            if 0 <= new_index < len(self.match_items):
                self.matches_scroll.ensureWidgetVisible(self.match_items[new_index])
        elif self.selected_index == -1 and self.all_matches:
            # No selection, select first match
            new_index = 0
            self._on_match_item_selected(self.all_matches[new_index], new_index)
            if 0 <= new_index < len(self.match_items):
                self.matches_scroll.ensureWidgetVisible(self.match_items[new_index])
    
    def insert_match_by_number(self, match_number: int):
        """Insert match by its number (1-based index) - for Ctrl+1-9 shortcuts"""
        if 0 < match_number <= len(self.all_matches):
            match = self.all_matches[match_number - 1]
            # Select it visually
            self._on_match_item_selected(match, match_number - 1)
            # Scroll to it
            if 0 <= match_number - 1 < len(self.match_items):
                self.matches_scroll.ensureWidgetVisible(self.match_items[match_number - 1])
            # Emit insert signal
            self.match_inserted.emit(match.target)
            return True
        return False
    
    def insert_selected_match(self):
        """Insert currently selected match (Ctrl+Space)"""
        if self.current_selection:
            self.match_inserted.emit(self.current_selection.target)
            return True
        return False
    
    def keyPressEvent(self, event):
        """
        Handle keyboard events for navigation and insertion
        
        Shortcuts:
        - Up/Down arrows: Navigate matches (plain arrows, no Ctrl)
        - Spacebar: Insert selected match into target
        - Return/Enter: Insert selected match into target
        - Ctrl+Space: Insert selected match (alternative)
        - Ctrl+1 to Ctrl+9: Insert specific match by number (global)
        
        Note: Ctrl+Up/Down are handled at main window level for grid navigation
        """
        # Ctrl+Space: Insert currently selected match
        if (event.modifiers() & Qt.KeyboardModifier.ControlModifier and 
            event.key() == Qt.Key.Key_Space):
            if self.insert_selected_match():
                event.accept()
                return
        
        # Ctrl+1 through Ctrl+9: Insert match by number
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() >= Qt.Key.Key_1 and event.key() <= Qt.Key.Key_9:
                match_num = event.key() - Qt.Key.Key_0  # Convert key to number
                if self.insert_match_by_number(match_num):
                    event.accept()
                    return
        
        # Up/Down arrows: Navigate matches (plain arrows only, NOT Ctrl+Up/Down)
        if event.key() == Qt.Key.Key_Up:
            if not (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
                self.select_previous_match()
                event.accept()
                return
        elif event.key() == Qt.Key.Key_Down:
            if not (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
                self.select_next_match()
                event.accept()
                return
        
        # Spacebar or Return/Enter: Insert selected match
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            if self.current_selection:
                self.match_inserted.emit(self.current_selection.target)
                event.accept()
                return
        
        super().keyPressEvent(event)

