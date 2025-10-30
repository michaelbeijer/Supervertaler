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
    match_type: str  # "NT", "MT", "TM", "Termbase"
    compare_source: Optional[str] = None  # For TM compare boxes


class CompactMatchItem(QFrame):
    """Compact match display (like memoQ compact view) with match number on same line"""
    
    match_selected = pyqtSignal(TranslationMatch)
    
    def __init__(self, match: TranslationMatch, match_number: int = 0, parent=None):
        super().__init__(parent)
        self.match = match
        self.match_number = match_number
        self.is_selected = False
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.update_styling()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(1)
        
        # Source and Target side-by-side with number on left
        content_layout = QHBoxLayout()
        content_layout.setSpacing(4)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Match number (left)
        if match_number > 0:
            num_label = QLabel(f"#{match_number}")
            num_label.setStyleSheet("font-weight: bold; font-size: 9px; min-width: 20px;")
            num_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            content_layout.addWidget(num_label)
        
        # Source (light blue, left)
        source_frame = QFrame()
        source_frame.setStyleSheet("""
            QFrame {
                background-color: #e8f4f8;
                border: none;
                padding: 2px;
            }
        """)
        source_layout = QVBoxLayout(source_frame)
        source_layout.setContentsMargins(3, 1, 3, 1)
        source_layout.setSpacing(0)
        
        source_text = QLabel(match.source)
        source_text.setWordWrap(True)
        source_text.setMinimumHeight(30)  # Min height but allow expansion
        source_font = QFont()
        source_font.setPointSize(8)
        source_text.setFont(source_font)
        source_layout.addWidget(source_text)
        
        # Target (light green, right)
        target_frame = QFrame()
        target_frame.setStyleSheet("""
            QFrame {
                background-color: #e8f8e8;
                border: none;
                padding: 2px;
            }
        """)
        target_layout = QVBoxLayout(target_frame)
        target_layout.setContentsMargins(3, 1, 3, 1)
        target_layout.setSpacing(0)
        
        target_text = QLabel(match.target)
        target_text.setWordWrap(True)
        target_text.setMinimumHeight(30)  # Min height but allow expansion
        target_font = QFont()
        target_font.setPointSize(8)
        target_text.setFont(target_font)
        target_layout.addWidget(target_text)
        
        content_layout.addWidget(source_frame, 1)
        content_layout.addWidget(target_frame, 1)
        layout.addLayout(content_layout)
        
        # Relevance % on same line (compact)
        rel_layout = QHBoxLayout()
        rel_layout.setContentsMargins(0, 0, 0, 0)
        rel_layout.setSpacing(0)
        rel_layout.addStretch()
        
        rel_label = QLabel(f"{match.relevance}%")
        rel_label.setStyleSheet("font-size: 8px; color: #888;")
        rel_layout.addWidget(rel_label)
        
        layout.addLayout(rel_layout)
        
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.mousePressEvent = self._on_click
    
    def _on_click(self, event):
        """Emit signal when clicked"""
        self.match_selected.emit(self.match)
        self.select()
    
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
        # Color code by match type: TM=red, Termbase=blue, MT=green, NT=gray
        type_color_map = {
            "TM": "#ff6b6b",
            "Termbase": "#4d94ff",
            "MT": "#51cf66",
            "NT": "#adb5bd"
        }
        
        type_color = type_color_map.get(self.match.match_type, "#adb5bd")
        
        if self.is_selected:
            # Selected: darker shade of type color with contrast text
            darker_color = self._darken_color(type_color)
            self.setStyleSheet(f"""
                CompactMatchItem {{
                    background-color: {type_color};
                    border: 2px solid {darker_color};
                    border-radius: 2px;
                    margin: 1px;
                    padding: 3px;
                }}
                QLabel {{
                    color: #000000;
                    font-weight: bold;
                }}
            """)
        else:
            # Unselected: light background with subtle type color border
            light_color = self._lighten_color(type_color, 0.9)
            self.setStyleSheet(f"""
                CompactMatchItem {{
                    background-color: {light_color};
                    border: 1px solid {type_color};
                    border-radius: 2px;
                    margin: 1px;
                    padding: 3px;
                }}
                CompactMatchItem:hover {{
                    background-color: {self._lighten_color(type_color, 0.8)};
                    border: 1px solid {type_color};
                }}
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
    
    def __init__(self, title: str, matches: List[TranslationMatch], parent=None):
        super().__init__(parent)
        self.title = title
        self.matches = matches
        self.is_expanded = True
        self.match_items = []
        self.selected_index = -1
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Section header (collapsible)
        header = self._create_header()
        layout.addWidget(header)
        
        # Matches container
        self.matches_container = QWidget()
        self.matches_layout = QVBoxLayout(self.matches_container)
        self.matches_layout.setContentsMargins(2, 2, 2, 2)
        self.matches_layout.setSpacing(2)
        
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
        """Populate section with matches"""
        for idx, match in enumerate(self.matches, 1):
            item = CompactMatchItem(match, match_number=idx)
            item.match_selected.connect(lambda m, i=idx-1: self._on_match_selected(m, i))
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
    """
    
    match_selected = pyqtSignal(TranslationMatch)
    match_inserted = pyqtSignal(str)  # Emitted when user wants to insert match into target
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.matches_by_type: Dict[str, List[TranslationMatch]] = {}
        self.current_selection: Optional[TranslationMatch] = None
        self.all_matches: List[TranslationMatch] = []
        self.match_sections: Dict[str, MatchSection] = {}
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
        
        # Compare box (shown when match selected) - VERTICAL STACKED LAYOUT
        self.compare_frame = self._create_compare_box()
        main_splitter.addWidget(self.compare_frame)
        self.compare_frame.hide()  # Hidden by default
        
        # Set splitter proportions (60% matches, 40% compare)
        main_splitter.setSizes([600, 400])
        main_splitter.setCollapsible(0, False)
        main_splitter.setCollapsible(1, True)
        
        layout.addWidget(main_splitter)
        
        # Notes section (compact)
        notes_label = QLabel("📝 Notes (segment annotations)")
        notes_label.setStyleSheet("font-weight: bold; font-size: 9px; color: #333;")
        layout.addWidget(notes_label)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(50)
        self.notes_edit.setPlaceholderText("Add notes about this segment, context, or translation concerns...")
        self.notes_edit.setStyleSheet("font-size: 9px; padding: 4px;")
        layout.addWidget(self.notes_edit)
    
    def _create_compare_box(self) -> QFrame:
        """Create compare box frame with VERTICAL stacked layout and resizable sections"""
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
        title = QLabel("📊 Compare Box (Vertically Stacked & Resizable)")
        title.setStyleSheet("font-weight: bold; font-size: 9px; color: #666;")
        layout.addWidget(title)
        
        # Use splitter for vertical resizing of compare boxes
        compare_splitter = QSplitter(Qt.Orientation.Vertical)
        compare_splitter.setStyleSheet("""
            QSplitter { background-color: #fafafa; }
            QSplitter::handle { 
                background-color: #d0d0d0; 
                height: 5px;
                margin: 2px 0px;
            }
            QSplitter::handle:hover { 
                background-color: #0066cc; 
            }
        """)
        
        # Box 1: Current Source
        box1 = self._create_compare_text_box("Current Source:", "#e3f2fd")
        self.compare_current = box1[1]
        compare_splitter.addWidget(box1[0])
        
        # Box 2: TM Source (with diff highlighting capability)
        box2 = self._create_compare_text_box("TM Source:", "#fff3cd")
        self.compare_tm_source = box2[1]
        compare_splitter.addWidget(box2[0])
        
        # Box 3: TM Target
        box3 = self._create_compare_text_box("TM Target:", "#d4edda")
        self.compare_tm_target = box3[1]
        compare_splitter.addWidget(box3[0])
        
        # Equal heights for each box (33% each)
        compare_splitter.setSizes([33, 33, 34])
        compare_splitter.setCollapsible(0, False)
        compare_splitter.setCollapsible(1, False)
        compare_splitter.setCollapsible(2, False)
        
        layout.addWidget(compare_splitter)
        
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
                font-size: 8px;
                padding: 4px;
                margin: 0px;
            }}
        """)
        layout.addWidget(text_edit)
        
        return (container, text_edit)
    
    def set_matches(self, matches_dict: Dict[str, List[TranslationMatch]]):
        """
        Set matches from different sources
        
        Args:
            matches_dict: Dict with keys like "NT", "MT", "TM", "Termbases"
        """
        self.matches_by_type = matches_dict
        self.all_matches = []
        self.match_sections = {}
        
        # Clear existing sections
        while self.main_layout.count() > 0:
            item = self.main_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        # Add sections for each match type in order
        order = ["NT", "MT", "TM", "Termbases"]
        for match_type in order:
            if match_type in matches_dict and matches_dict[match_type]:
                section = MatchSection(match_type, matches_dict[match_type])
                section.match_selected.connect(self._on_match_selected)
                self.main_layout.addWidget(section)
                self.match_sections[match_type] = section
                self.all_matches.extend(matches_dict[match_type])
        
        self.main_layout.addStretch()
    
    def _on_match_selected(self, match: TranslationMatch):
        """Handle match selection"""
        self.current_selection = match
        self.match_selected.emit(match)
        
        # Update compare box
        if match.match_type == "TM" and match.compare_source:
            self.compare_frame.show()
            self.compare_current.setText("")  # Would be filled from segment
            self.compare_tm_source.setText(match.compare_source)
            self.compare_tm_target.setText(match.target)
        else:
            self.compare_frame.hide()
    
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
        self.notes_edit.clear()
        
        while self.main_layout.count() > 0:
            item = self.main_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
    
    def get_selected_match(self) -> Optional[TranslationMatch]:
        """Get currently selected match"""
        return self.current_selection
    
    def keyPressEvent(self, event):
        """
        Handle keyboard events for navigation and insertion
        
        Shortcuts:
        - Up/Down arrows: Navigate matches within current section
        - Spacebar: Insert selected match into target
        - Return/Enter: Insert selected match into target
        - Ctrl+1 to Ctrl+9: Insert specific match by number (global)
        
        Note: Ctrl+Up/Down are reserved for grid navigation (not match navigation)
        """
        # Ctrl+1 through Ctrl+9: Insert match by number (global, not per-section)
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() >= Qt.Key.Key_1 and event.key() <= Qt.Key.Key_9:
                match_num = event.key() - Qt.Key.Key_0  # Convert key to number
                if 0 < match_num <= len(self.all_matches):
                    # Find and select the match
                    match = self.all_matches[match_num - 1]
                    
                    # Find which section it belongs to and select it
                    for section in self.match_sections.values():
                        if match in section.matches:
                            local_index = section.matches.index(match) + 1
                            section.select_by_number(local_index)
                            break
                    
                    # Emit insert signal
                    self.match_inserted.emit(match.target)
                event.accept()
                return
        
        # Up/Down arrows: Navigate matches (NOT Ctrl+Up/Down - those are for grid)
        if event.key() == Qt.Key.Key_Up:
            if not (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
                for section in self.match_sections.values():
                    if section.navigate(-1):
                        event.accept()
                        return
        elif event.key() == Qt.Key.Key_Down:
            if not (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
                for section in self.match_sections.values():
                    if section.navigate(1):
                        event.accept()
                        return
        
        # Spacebar or Return/Enter: Insert selected match
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            if self.current_selection:
                self.match_inserted.emit(self.current_selection.target)
                event.accept()
                return
        
        super().keyPressEvent(event)

