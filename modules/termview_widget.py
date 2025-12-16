"""
Termview Widget - RYS-style Inline Terminology Display

Displays source text with termbase translations shown directly underneath each word/phrase.
Inspired by the RYS Trados plugin's inline term visualization.

Features:
- Visual mapping: translations appear under their source terms
- Hover tooltips: show synonyms/alternatives
- Click to insert: click any translation to insert into target
- Multi-word term support: handles both single words and phrases
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea,
                              QHBoxLayout, QPushButton, QToolTip, QLayout, QLayoutItem, QSizePolicy, QStyle)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QRect, QSize
from PyQt6.QtGui import QFont, QCursor
from typing import Dict, List, Optional, Tuple
import re


class FlowLayout(QLayout):
    """Flow layout that wraps widgets to next line when needed"""
    
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.itemList = []
        self.m_hSpace = spacing
        self.m_vSpace = spacing
        self.setContentsMargins(margin, margin, margin, margin)
    
    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)
    
    def addItem(self, item):
        self.itemList.append(item)
    
    def horizontalSpacing(self):
        if self.m_hSpace >= 0:
            return self.m_hSpace
        else:
            return self.smartSpacing(QStyle.PixelMetric.PM_LayoutHorizontalSpacing)
    
    def verticalSpacing(self):
        if self.m_vSpace >= 0:
            return self.m_vSpace
        else:
            return self.smartSpacing(QStyle.PixelMetric.PM_LayoutVerticalSpacing)
    
    def count(self):
        return len(self.itemList)
    
    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None
    
    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None
    
    def expandingDirections(self):
        return Qt.Orientation(0)
    
    def hasHeightForWidth(self):
        return True
    
    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height
    
    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)
    
    def sizeHint(self):
        return self.minimumSize()
    
    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        margin = self.contentsMargins().left()
        size += QSize(2 * margin, 2 * margin)
        return size
    
    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0
        spacing = self.horizontalSpacing()
        if spacing < 0:
            spacing = 5  # Default spacing
        
        for item in self.itemList:
            wid = item.widget()
            spaceX = spacing
            spaceY = spacing
            
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0
            
            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
        
        return y + lineHeight - rect.y()
    
    def smartSpacing(self, pm):
        parent = self.parent()
        if not parent:
            return -1
        if parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()


class TermBlock(QWidget):
    """Individual term block showing source word and its translation(s)"""
    
    term_clicked = pyqtSignal(str, str)  # source_term, target_term
    
    def __init__(self, source_text: str, translations: List[Dict], parent=None, theme_manager=None):
        """
        Args:
            source_text: Source word/phrase
            translations: List of dicts with keys: 'target', 'termbase_name', 'priority', etc.
            theme_manager: Optional theme manager for dark mode support
        """
        super().__init__(parent)
        self.source_text = source_text
        self.translations = translations
        self.theme_manager = theme_manager
        self.init_ui()
        
    def init_ui(self):
        """Create the visual layout for this term block - COMPACT RYS-style"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 0, 1, 1)
        layout.setSpacing(0)
        
        # Get theme colors
        is_dark = self.theme_manager and self.theme_manager.current_theme.name == "Dark"
        separator_color = "#555555" if is_dark else "#CCCCCC"
        source_text_color = "#E0E0E0" if is_dark else "#333"
        no_match_color = "#666666" if is_dark else "#ddd"
        no_match_bg = "#2A2A2A" if is_dark else "#F5F5F5"
        
        # Add thin gray separator line at top (like RYS)
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background-color: {separator_color}; border: none;")
        layout.addWidget(separator)
        
        # Determine border color based on whether we have translations
        if self.translations:
            primary_translation = self.translations[0]
            is_project = primary_translation.get('is_project_termbase', False)
            ranking = primary_translation.get('ranking', None)
            
            # IMPORTANT: Treat ranking #1 as project termbase (matches main app logic)
            is_effective_project = is_project or (ranking == 1)
            
            # Background color: pink for project termbase, blue for regular termbase
            self.bg_color = "#FFE5F0" if is_effective_project else "#D6EBFF"
            self.is_effective_project = is_effective_project
        else:
            self.bg_color = no_match_bg  # Theme-aware for no matches
            self.is_effective_project = False
        
        # Source text (top) - compact
        source_label = QLabel(self.source_text)
        source_font = QFont()
        source_font.setPointSize(8)
        source_label.setFont(source_font)
        source_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        source_label.setStyleSheet(f"""
            QLabel {{
                color: {source_text_color};
                padding: 1px 3px;
                background-color: transparent;
                border: none;
            }}
        """)
        layout.addWidget(source_label)
        
        # Target translation (bottom) - show first/best match - COMPACT
        if self.translations:
            target_text = primary_translation.get('target_term', primary_translation.get('target', ''))
            termbase_name = primary_translation.get('termbase_name', '')
            
            # Background color based on termbase type
            bg_color = "#FFE5F0" if self.is_effective_project else "#D6EBFF"  # Pink for project, light blue for regular
            
            target_label = QLabel(target_text)
            target_font = QFont()
            target_font.setPointSize(8)
            target_font.setBold(False)  # Less bold for compactness
            target_label.setFont(target_font)
            target_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            target_label.setStyleSheet(f"""
                QLabel {{
                    color: #0052A3;
                    padding: 1px 3px;
                    background-color: {bg_color};
                    border: none;
                }}
                QLabel:hover {{
                    background-color: #BBDEFB;
                    cursor: pointer;
                }}
            """)
            target_label.setCursor(Qt.CursorShape.PointingHandCursor)
            target_label.mousePressEvent = lambda e: self.on_translation_clicked(target_text)
            
            # Set tooltip if multiple translations exist
            if len(self.translations) > 1:
                tooltip_lines = [f"<b>{target_text}</b> (click to insert)<br>"]
                tooltip_lines.append("<br><b>Alternatives:</b>")
                for i, trans in enumerate(self.translations[1:], 1):
                    alt_target = trans.get('target_term', trans.get('target', ''))
                    alt_termbase = trans.get('termbase_name', '')
                    tooltip_lines.append(f"{i}. {alt_target} ({alt_termbase})")
                target_label.setToolTip("<br>".join(tooltip_lines))
            else:
                target_label.setToolTip(f"<b>{target_text}</b><br>From: {termbase_name}<br>(click to insert)")
            
            layout.addWidget(target_label)
            
            # Show count if multiple translations - very compact
            if len(self.translations) > 1:
                count_label = QLabel(f"+{len(self.translations) - 1}")
                count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                count_label.setStyleSheet("""
                    QLabel {
                        color: #999;
                        font-size: 7px;
                    }
                """)
                layout.addWidget(count_label)
        else:
            # No translation found - very subtle (theme-aware)
            is_dark = self.theme_manager and self.theme_manager.current_theme.name == "Dark"
            no_match_dot_color = "#666666" if is_dark else "#ddd"
            no_match_label = QLabel("·")
            no_match_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_match_label.setStyleSheet(f"color: {no_match_dot_color}; font-size: 8px;")
            layout.addWidget(no_match_label)
    
    def on_translation_clicked(self, target_text: str):
        """Handle click on translation to insert into target"""
        self.term_clicked.emit(self.source_text, target_text)


class NTBlock(QWidget):
    """Non-translatable block showing source word with pastel yellow styling"""
    
    nt_clicked = pyqtSignal(str)  # Emits NT text to insert as-is
    
    def __init__(self, source_text: str, list_name: str = "", parent=None, theme_manager=None):
        """
        Args:
            source_text: Non-translatable word/phrase
            list_name: Name of the NT list it comes from
            theme_manager: Optional theme manager for dark mode support
        """
        super().__init__(parent)
        self.source_text = source_text
        self.list_name = list_name
        self.theme_manager = theme_manager
        self.init_ui()
        
    def init_ui(self):
        """Create the visual layout for this NT block - pastel yellow styling"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)
        
        # Get theme colors
        is_dark = self.theme_manager and self.theme_manager.current_theme.name == "Dark"
        source_text_color = "#E0E0E0" if is_dark else "#5D4E37"
        
        # Pastel yellow border for non-translatables
        border_color = "#E6C200"  # Darker yellow for border
        
        self.setStyleSheet(f"""
            QWidget {{
                border-top: 2px solid {border_color};
                border-radius: 0px;
            }}
        """)
        
        # Source text (top)
        source_label = QLabel(self.source_text)
        source_font = QFont()
        source_font.setPointSize(8)
        source_label.setFont(source_font)
        source_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        source_label.setStyleSheet(f"""
            QLabel {{
                color: {source_text_color};
                padding: 1px 3px;
                background-color: transparent;
            }}
        """)
        layout.addWidget(source_label)
        
        # "Do not translate" indicator with pastel yellow background
        nt_label = QLabel("🚫 NT")
        nt_font = QFont()
        nt_font.setPointSize(7)
        nt_label.setFont(nt_font)
        nt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nt_label.setStyleSheet("""
            QLabel {
                color: #5D4E37;
                padding: 1px 3px;
                background-color: #FFFDD0;
                border-radius: 2px;
            }
            QLabel:hover {
                background-color: #FFF9B0;
                cursor: pointer;
            }
        """)
        nt_label.setCursor(Qt.CursorShape.PointingHandCursor)
        nt_label.mousePressEvent = lambda e: self.on_nt_clicked()
        
        tooltip = f"<b>🚫 Non-Translatable</b><br>{self.source_text}<br><br>From: {self.list_name}<br>(click to insert as-is)"
        nt_label.setToolTip(tooltip)
        
        layout.addWidget(nt_label)
    
    def on_nt_clicked(self):
        """Handle click on NT to insert source text as-is"""
        self.nt_clicked.emit(self.source_text)


class TermviewWidget(QWidget):
    """Main Termview widget showing inline terminology for current segment"""
    
    term_insert_requested = pyqtSignal(str)  # Emits target text to insert
    
    def __init__(self, parent=None, db_manager=None, log_callback=None, theme_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.log = log_callback if log_callback else print
        self.theme_manager = theme_manager
        self.current_source = ""
        self.current_source_lang = None
        self.current_target_lang = None
        self.current_project_id = None  # Store project ID for termbase priority lookup

        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Get theme colors
        if self.theme_manager:
            theme = self.theme_manager.current_theme
            bg_color = theme.base
            border_color = theme.border
            header_bg = theme.panel_info
            header_text = theme.button_info
            info_text = theme.text_disabled
        else:
            # Fallback colors if no theme manager
            bg_color = "white"
            border_color = "#ddd"
            header_bg = "#E3F2FD"
            header_text = "#1565C0"
            info_text = "#999"

        # Header
        header = QLabel("🔍 Termview - Inline Terminology")
        header.setStyleSheet(f"""
            QLabel {{
                font-weight: bold;
                font-size: 12px;
                color: {header_text};
                padding: 5px;
                background-color: {header_bg};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(header)

        # Scroll area for term blocks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # No horizontal scroll
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {border_color};
                border-radius: 4px;
                background-color: {bg_color};
            }}
        """)

        # Container for term blocks (flow layout with wrapping)
        self.terms_container = QWidget()
        self.terms_layout = FlowLayout(self.terms_container, margin=5, spacing=4)

        scroll.setWidget(self.terms_container)
        layout.addWidget(scroll)

        # Info label - use slightly brighter text for dark mode
        self.info_label = QLabel("No segment selected")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        is_dark = self.theme_manager and self.theme_manager.current_theme.name == "Dark"
        info_label_color = "#909090" if is_dark else info_text
        self.info_label.setStyleSheet(f"color: {info_label_color}; font-size: 10px; padding: 5px;")
        layout.addWidget(self.info_label)
        
        # Store references for theme refresh
        self.header = header
        self.scroll = scroll
    
    def apply_theme(self):
        """Refresh all theme-dependent colors when theme changes"""
        if not self.theme_manager:
            return
        
        theme = self.theme_manager.current_theme
        bg_color = theme.base
        border_color = theme.border
        header_bg = theme.panel_info
        header_text = theme.button_info
        info_text = theme.text_disabled
        
        # Update header
        if hasattr(self, 'header'):
            self.header.setStyleSheet(f"""
                QLabel {{
                    font-weight: bold;
                    font-size: 12px;
                    color: {header_text};
                    padding: 5px;
                    background-color: {header_bg};
                    border-radius: 4px;
                }}
            """)
        
        # Update scroll area
        if hasattr(self, 'scroll'):
            self.scroll.setStyleSheet(f"""
                QScrollArea {{
                    border: 1px solid {border_color};
                    border-radius: 4px;
                    background-color: {bg_color};
                }}
            """)
        
        # Update info label - use slightly brighter text for better visibility in dark mode
        if hasattr(self, 'info_label'):
            is_dark = theme.name == "Dark"
            info_label_color = "#909090" if is_dark else info_text
            self.info_label.setStyleSheet(f"color: {info_label_color}; font-size: 10px; padding: 5px;")
    
    def update_with_matches(self, source_text: str, termbase_matches: List[Dict], nt_matches: List[Dict] = None):
        """
        Update the termview display with pre-computed termbase and NT matches
        
        RYS-STYLE DISPLAY: Show source text as tokens with translations underneath
        
        Args:
            source_text: Source segment text
            termbase_matches: List of termbase match dicts from Translation Results
            nt_matches: Optional list of NT match dicts with 'text', 'start', 'end', 'list_name' keys
        """
        print(f"🔍 TERMVIEW.update_with_matches called: source_len={len(source_text) if source_text else 0}, matches={len(termbase_matches) if termbase_matches else 0}, nt={len(nt_matches) if nt_matches else 0}")
        
        self.current_source = source_text
        
        # Clear existing blocks
        self.clear_terms()
        print(f"🔍 TERMVIEW: Cleared existing terms")
        
        if not source_text or not source_text.strip():
            self.info_label.setText("No segment selected")
            print(f"🔍 TERMVIEW: No source text")
            return
        
        has_termbase = termbase_matches and len(termbase_matches) > 0
        has_nt = nt_matches and len(nt_matches) > 0
        
        if not has_termbase and not has_nt:
            self.info_label.setText("No terminology or NT matches for this segment")
            print(f"🔍 TERMVIEW: No matches")
            return
        
        print(f"🔍 TERMVIEW: Processing {len(termbase_matches) if termbase_matches else 0} termbase + {len(nt_matches) if nt_matches else 0} NT matches...")
        
        # Convert termbase matches to dict for easy lookup: {source_term.lower(): [translations]}
        matches_dict = {}
        if termbase_matches:
            for match in termbase_matches:
                source_term = match.get('source_term', match.get('source', ''))
                target_term = match.get('target_term', match.get('translation', ''))
                
                if not source_term or not target_term:
                    continue
                
                key = source_term.lower()
                if key not in matches_dict:
                    matches_dict[key] = []
                
                # Add main target term
                matches_dict[key].append({
                    'target_term': target_term,
                    'termbase_name': match.get('termbase_name', ''),
                    'ranking': match.get('ranking', 99),
                    'is_project_termbase': match.get('is_project_termbase', False)
                })
                
                # Add synonyms as additional translations
                target_synonyms = match.get('target_synonyms', [])
                for synonym in target_synonyms:
                    matches_dict[key].append({
                        'target_term': synonym,
                        'termbase_name': match.get('termbase_name', '') + ' (syn)',
                        'ranking': match.get('ranking', 99) + 1,  # Slightly lower priority
                        'is_project_termbase': match.get('is_project_termbase', False)
                    })
        
        # Convert NT matches to dict: {text.lower(): list_name}
        nt_dict = {}
        if nt_matches:
            for match in nt_matches:
                nt_text = match.get('text', '')
                if nt_text:
                    nt_dict[nt_text.lower()] = match.get('list_name', 'Non-Translatables')
        
        print(f"🔍 TERMVIEW: Organized into {len(matches_dict)} termbase terms + {len(nt_dict)} NTs")
        
        # Combine all known multi-word terms for tokenization
        all_terms_dict = dict(matches_dict)
        for nt_key in nt_dict:
            if nt_key not in all_terms_dict:
                all_terms_dict[nt_key] = []  # Empty list = NT only
        
        # Tokenize source text, respecting multi-word terms
        tokens = self.tokenize_with_multiword_terms(source_text, all_terms_dict)
        print(f"🔍 TERMVIEW: Created {len(tokens)} tokens from source text")
        
        if not tokens:
            self.info_label.setText("No words to analyze")
            return
        
        # Create blocks for each token
        blocks_with_translations = 0
        blocks_with_nt = 0
        
        for token in tokens:
            # Strip trailing punctuation for lookup
            token_clean = token.rstrip('.,;:!?')
            lookup_key = token_clean.lower()
            
            # Check if this is a non-translatable
            if lookup_key in nt_dict:
                # Create NT block
                nt_block = NTBlock(token, nt_dict[lookup_key], self, theme_manager=self.theme_manager)
                nt_block.nt_clicked.connect(self.on_term_insert_requested)
                self.terms_layout.addWidget(nt_block)
                blocks_with_nt += 1
            else:
                # Get termbase translations for this token
                translations = matches_dict.get(lookup_key, [])
                
                # Create term block (even if no translation - shows source word)
                term_block = TermBlock(token, translations, self, theme_manager=self.theme_manager)
                term_block.term_clicked.connect(self.on_term_insert_requested)
                self.terms_layout.addWidget(term_block)
                
                if translations:
                    blocks_with_translations += 1
        
        info_parts = []
        if blocks_with_translations > 0:
            info_parts.append(f"{blocks_with_translations} terms")
        if blocks_with_nt > 0:
            info_parts.append(f"{blocks_with_nt} NTs")
        
        if info_parts:
            self.info_label.setText(f"✓ Found {', '.join(info_parts)} in {len(tokens)} words")
        else:
            self.info_label.setText(f"No matches in {len(tokens)} words")
        
        print(f"🔍 TERMVIEW: Completed - {blocks_with_translations} terms, {blocks_with_nt} NTs in {len(tokens)} tokens")
    
    def update_for_segment(self, source_text: str, source_lang: str, target_lang: str, project_id: int = None):
        """
        DEPRECATED: Use update_with_matches() instead
        
        Update the termview display for a new segment
        
        Args:
            source_text: Source segment text
            source_lang: Source language code
            target_lang: Target language code
            project_id: Project ID for termbase priority lookup
        """
        self.current_source = source_text
        self.current_source_lang = source_lang
        self.current_target_lang = target_lang
        self.current_project_id = project_id
        
        # Clear existing blocks
        self.clear_terms()
        
        if not source_text or not source_text.strip():
            self.info_label.setText("No segment selected")
            return
        
        # Get all termbase matches first to detect multi-word terms
        all_matches = self.get_all_termbase_matches(source_text)
        
        # DEBUG: Log what matches were found
        if all_matches:
            self.log(f"🔍 Termview: Found {len(all_matches)} unique terms in termbase")
            for term_key in sorted(all_matches.keys(), key=len, reverse=True)[:5]:
                self.log(f"  - '{term_key}' ({len(all_matches[term_key])} translation(s))")
        
        # Create tokens, respecting multi-word terms
        tokens = self.tokenize_with_multiword_terms(source_text, all_matches)
        
        # DEBUG: Log the tokens created
        if tokens:
            self.log(f"🔍 Termview: Created {len(tokens)} tokens")
            if len(tokens) <= 15:
                self.log(f"  Tokens: {tokens}")
        
        if not tokens:
            self.info_label.setText("No words to analyze")
            return
        
        # DEBUG: Log ALL tokens with their lookups
        if len(tokens) > 0:
            self.log(f"🔍 ALL {len(tokens)} tokens and lookups:")
            for i, tok in enumerate(tokens):
                tok_clean = tok.rstrip('.,;:!?')
                lookup_key = tok_clean.lower()
                found = lookup_key in all_matches
                self.log(f"  {i+1}. '{tok}' → {'FOUND' if found else 'not found'}")
        
        # Search termbases for each token (use pre-fetched matches)
        term_blocks_created = 0
        for i, token in enumerate(tokens):
            # Strip trailing punctuation for lookup (matches what we did in get_all_termbase_matches)
            token_clean = token.rstrip('.,;:!?')
            
            # Check if we already have matches for this token
            translations = all_matches.get(token_clean.lower(), [])
            
            # If no exact match, try searching (for single words)
            if not translations and ' ' not in token_clean:
                translations = self.search_term(token_clean)
            
            # DEBUG: Log translations for first token (the multi-word term)
            if i == 0 and ' ' in token:
                self.log(f"🔍 Token #1 '{token}' has {len(translations)} translation(s):")
                for j, trans in enumerate(translations):
                    target = trans.get('target_term', trans.get('target', ''))
                    self.log(f"    {j+1}. '{target}'")
            
            # Create term block
            term_block = TermBlock(token, translations, self, theme_manager=self.theme_manager)
            term_block.term_clicked.connect(self.on_term_insert_requested)
            
            # Add to flow layout
            self.terms_layout.addWidget(term_block)
            
            if translations:
                term_blocks_created += 1
        
        # Update info
        if term_blocks_created > 0:
            self.info_label.setText(f"✓ Found terminology for {term_blocks_created} of {len(tokens)} terms/words")
        else:
            self.info_label.setText(f"No terminology matches found for this segment")
    
    def get_all_termbase_matches(self, text: str) -> Dict[str, List[Dict]]:
        """
        Get all termbase matches for text by using the proper termbase search
        
        This uses the SAME search logic as the Translation Results panel,
        ensuring we only show terms that actually match, not false positives.
        
        Args:
            text: Source text
            
        Returns:
            Dict mapping source term (lowercase) to list of translation dicts
        """
        if not self.db_manager or not self.current_source_lang or not self.current_target_lang:
            return {}
        
        matches = {}
        
        try:
            # Extract all words from the text to search
            # Use the same token pattern as we use for display
            token_pattern = re.compile(r'(?<!\w)[\w.,%-]+(?!\w)', re.UNICODE)
            tokens = [match.group() for match in token_pattern.finditer(text)]
            
            # Also check for multi-word phrases (up to 8 words)
            words = re.findall(r'\b[\w-]+\b', text, re.UNICODE)
            phrases_to_check = []
            
            # Generate n-grams for multi-word term detection
            for n in range(2, min(9, len(words) + 1)):
                for i in range(len(words) - n + 1):
                    phrase = ' '.join(words[i:i+n])
                    phrases_to_check.append(phrase)
            
            # Search each token and phrase using the database's search_termbases method
            all_search_terms = set(tokens + phrases_to_check)
            
            for search_term in all_search_terms:
                if not search_term or len(search_term) < 2:
                    continue
                
                # Strip trailing punctuation for search (but keep internal punctuation like "gew.%")
                # This handles cases like "edelmetalen." → "edelmetalen"
                search_term_clean = search_term.rstrip('.,;:!?')
                if not search_term_clean or len(search_term_clean) < 2:
                    continue
                
                # Use the SAME search method as translation results panel
                results = self.db_manager.search_termbases(
                    search_term=search_term_clean,
                    source_lang=self.current_source_lang,
                    target_lang=self.current_target_lang,
                    project_id=self.current_project_id,
                    min_length=2
                )
                
                # Add results to matches dict, but ONLY if the source term actually exists in the text
                for result in results:
                    source_term = result.get('source_term', '')
                    if not source_term:
                        continue
                    
                    # CRITICAL FIX: Verify the source term actually exists in the segment
                    # This prevents false positives like "het gebruik van" showing when only "het" exists
                    source_lower = source_term.lower()
                    text_lower = text.lower()
                    
                    # Use word boundaries to match complete words/phrases only
                    if ' ' in source_term:
                        # Multi-word term - must exist as exact phrase
                        pattern = r'\b' + re.escape(source_lower) + r'\b'
                    else:
                        # Single word
                        pattern = r'\b' + re.escape(source_lower) + r'\b'
                    
                    if not re.search(pattern, text_lower):
                        continue  # Skip - term not actually in segment
                    
                    key = source_lower
                    if key not in matches:
                        matches[key] = []
                    
                    # DEDUPLICATION: Only add if not already present
                    # Check by target_term to avoid duplicate translations
                    target_term = result.get('target_term', '')
                    already_exists = any(
                        m.get('target_term', '') == target_term 
                        for m in matches[key]
                    )
                    if not already_exists:
                        matches[key].append(result)
            
            return matches
        except Exception as e:
            self.log(f"✗ Error getting termbase matches: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def tokenize_with_multiword_terms(self, text: str, matches: Dict[str, List[Dict]]) -> List[str]:
        """
        Tokenize text, preserving multi-word terms found in termbase
        
        Args:
            text: Source text
            matches: Dict of termbase matches (from get_all_termbase_matches)
            
        Returns:
            List of tokens (words/phrases/numbers), with multi-word terms kept together
        """
        # DEBUG: Log multi-word terms we're looking for
        multi_word_terms = [k for k in matches.keys() if ' ' in k]
        if multi_word_terms:
            self.log(f"🔍 Tokenize: Looking for {len(multi_word_terms)} multi-word terms:")
            for term in sorted(multi_word_terms, key=len, reverse=True)[:3]:
                self.log(f"    - '{term}'")
        
        # Sort matched terms by length (longest first) to match multi-word terms first
        matched_terms = sorted(matches.keys(), key=len, reverse=True)
        
        # Track which parts of the text have been matched
        text_lower = text.lower()
        used_positions = set()
        tokens_with_positions = []
        
        # First pass: find multi-word terms with proper word boundary checking
        for term in matched_terms:
            if ' ' in term:  # Only process multi-word terms in first pass
                # Use regex with word boundaries to find term
                term_escaped = re.escape(term)
                
                # Check if term has punctuation - use different pattern
                if any(char in term for char in ['.', '%', ',', '-', '/']):
                    pattern = r'(?<!\w)' + term_escaped + r'(?!\w)'
                else:
                    pattern = r'\b' + term_escaped + r'\b'
                
                # DEBUG: Check if multi-word term is found
                found = re.search(pattern, text_lower)
                self.log(f"🔍 Tokenize: Pattern '{pattern}' for '{term}' → {'FOUND' if found else 'NOT FOUND'}")
                if found:
                    self.log(f"    Match at position {found.span()}: '{text[found.start():found.end()]}'")
                
                # Find all matches using regex
                for match in re.finditer(pattern, text_lower):
                    pos = match.start()
                    
                    # Check if this position overlaps with already matched terms
                    term_positions = set(range(pos, pos + len(term)))
                    if not term_positions.intersection(used_positions):
                        # Extract the original case version
                        original_term = text[pos:pos + len(term)]
                        tokens_with_positions.append((pos, len(term), original_term))
                        used_positions.update(term_positions)
                        self.log(f"    ✅ Added multi-word token: '{original_term}' covering positions {pos}-{pos+len(term)}")
        
        # DEBUG: Log used_positions after first pass
        if ' ' in sorted(matches.keys(), key=len, reverse=True)[0]:
            self.log(f"🔍 After first pass: {len(used_positions)} positions marked as used")
            self.log(f"    Used positions: {sorted(list(used_positions))[:20]}...")
        
        # Second pass: fill in gaps with ALL words/numbers/punctuation combos
        # Enhanced pattern to capture words, numbers, and combinations like "gew.%", "0,1", etc.
        # Use (?<!\w) and (?!\w) instead of \b to handle punctuation properly
        token_pattern = re.compile(r'(?<!\w)[\w.,%-]+(?!\w)', re.UNICODE)
        
        for match in token_pattern.finditer(text):
            word_start = match.start()
            word_end = match.end()
            word_positions = set(range(word_start, word_end))
            
            # Only add if not already covered by a multi-word term
            if not word_positions.intersection(used_positions):
                token = match.group()
                # Include ALL tokens - no filtering by length
                tokens_with_positions.append((word_start, len(token), token))
                used_positions.update(word_positions)
        
        # Sort by position and extract tokens
        tokens_with_positions.sort(key=lambda x: x[0])
        tokens = [token for pos, length, token in tokens_with_positions]
        
        return tokens
    
    def tokenize_source(self, text: str) -> List[str]:
        """
        Tokenize source text into words/phrases
        
        DEPRECATED: Use tokenize_with_multiword_terms instead for proper multi-word handling
        
        Args:
            text: Source text
            
        Returns:
            List of tokens (words/phrases)
        """
        # Remove punctuation and split
        # Keep hyphens as they're common in compound terms
        words = re.findall(r'\b[\w-]+\b', text, re.UNICODE)
        
        # Filter out very short words (articles, etc.) unless they're all caps
        filtered = [w for w in words if len(w) >= 3 or w.isupper()]
        
        return filtered
    
    def search_term(self, term: str) -> List[Dict]:
        """
        Search termbases for a specific term
        
        Args:
            term: Source term to search
            
        Returns:
            List of translation dicts (filtered to only include terms that exist in current segment)
        """
        if not self.db_manager or not self.current_source_lang or not self.current_target_lang:
            return []
        
        try:
            # Use database manager's search_termbases method
            results = self.db_manager.search_termbases(
                search_term=term,
                source_lang=self.current_source_lang,
                target_lang=self.current_target_lang,
                project_id=self.current_project_id,
                min_length=2
            )
            
            # CRITICAL FIX: Filter out results where the source term doesn't exist in the segment
            # This prevents "het gebruik van" from showing when searching "het" if the phrase isn't in the segment
            filtered_results = []
            segment_lower = self.current_source.lower()
            
            for result in results:
                source_term = result.get('source_term', '')
                if not source_term:
                    continue
                
                # Check if this term actually exists in the current segment
                source_lower = source_term.lower()
                
                # Use word boundaries to match complete words/phrases only
                if ' ' in source_term:
                    # Multi-word term - must exist as exact phrase
                    pattern = r'\b' + re.escape(source_lower) + r'\b'
                else:
                    # Single word
                    pattern = r'\b' + re.escape(source_lower) + r'\b'
                
                if re.search(pattern, segment_lower):
                    filtered_results.append(result)
            
            return filtered_results
        except Exception as e:
            self.log(f"✗ Error searching term '{term}': {e}")
            return []
    
    def clear_terms(self):
        """Clear all term blocks"""
        # Remove all widgets from flow layout
        while self.terms_layout.count() > 0:
            item = self.terms_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
    
    def on_term_insert_requested(self, source_term: str, target_term: str):
        """Handle request to insert a translation"""
        self.log(f"💡 Termview: Inserting '{target_term}' for '{source_term}'")
        self.term_insert_requested.emit(target_term)
