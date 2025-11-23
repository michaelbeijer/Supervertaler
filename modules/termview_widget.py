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
                              QHBoxLayout, QPushButton, QToolTip)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QCursor
from typing import Dict, List, Optional, Tuple
import re


class TermBlock(QWidget):
    """Individual term block showing source word and its translation(s)"""
    
    term_clicked = pyqtSignal(str, str)  # source_term, target_term
    
    def __init__(self, source_text: str, translations: List[Dict], parent=None):
        """
        Args:
            source_text: Source word/phrase
            translations: List of dicts with keys: 'target', 'termbase_name', 'priority', etc.
        """
        super().__init__(parent)
        self.source_text = source_text
        self.translations = translations
        self.init_ui()
        
    def init_ui(self):
        """Create the visual layout for this term block"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 2, 3, 2)
        layout.setSpacing(2)
        
        # Source text (top)
        source_label = QLabel(self.source_text)
        source_font = QFont()
        source_font.setPointSize(10)
        source_label.setFont(source_font)
        source_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        source_label.setStyleSheet("""
            QLabel {
                color: #333;
                padding: 2px 4px;
                background-color: #f0f0f0;
                border-radius: 3px;
            }
        """)
        layout.addWidget(source_label)
        
        # Arrow indicator
        arrow_label = QLabel("↓")
        arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow_label.setStyleSheet("color: #999; font-size: 10px;")
        layout.addWidget(arrow_label)
        
        # Target translation (bottom) - show first/best match
        if self.translations:
            primary_translation = self.translations[0]
            target_text = primary_translation.get('target_term', primary_translation.get('target', ''))
            termbase_name = primary_translation.get('termbase_name', '')
            is_project = primary_translation.get('is_project_termbase', False)
            
            # Color based on termbase type
            bg_color = "#FFE5F0" if is_project else "#E3F2FD"  # Pink for project, blue for regular
            
            target_label = QLabel(target_text)
            target_font = QFont()
            target_font.setPointSize(10)
            target_font.setBold(True)
            target_label.setFont(target_font)
            target_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            target_label.setStyleSheet(f"""
                QLabel {{
                    color: #1565C0;
                    padding: 3px 6px;
                    background-color: {bg_color};
                    border-radius: 4px;
                    border: 1px solid #90CAF9;
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
            
            # Show count if multiple translations
            if len(self.translations) > 1:
                count_label = QLabel(f"+{len(self.translations) - 1} more")
                count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                count_label.setStyleSheet("""
                    QLabel {
                        color: #666;
                        font-size: 9px;
                        font-style: italic;
                    }
                """)
                layout.addWidget(count_label)
        else:
            # No translation found
            no_match_label = QLabel("—")
            no_match_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_match_label.setStyleSheet("color: #ccc; font-size: 12px;")
            layout.addWidget(no_match_label)
    
    def on_translation_clicked(self, target_text: str):
        """Handle click on translation to insert into target"""
        self.term_clicked.emit(self.source_text, target_text)


class TermviewWidget(QWidget):
    """Main Termview widget showing inline terminology for current segment"""
    
    term_insert_requested = pyqtSignal(str)  # Emits target text to insert
    
    def __init__(self, parent=None, db_manager=None, log_callback=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.log = log_callback if log_callback else print
        self.current_source = ""
        self.current_source_lang = None
        self.current_target_lang = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Header
        header = QLabel("🔍 Termview - Inline Terminology")
        header.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 12px;
                color: #1565C0;
                padding: 5px;
                background-color: #E3F2FD;
                border-radius: 4px;
            }
        """)
        layout.addWidget(header)
        
        # Scroll area for term blocks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        
        # Container for term blocks (horizontal layout)
        self.terms_container = QWidget()
        self.terms_layout = QHBoxLayout(self.terms_container)
        self.terms_layout.setContentsMargins(10, 10, 10, 10)
        self.terms_layout.setSpacing(8)
        self.terms_layout.addStretch()  # Push blocks to left initially
        
        scroll.setWidget(self.terms_container)
        layout.addWidget(scroll)
        
        # Info label
        self.info_label = QLabel("No segment selected")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("color: #999; font-size: 10px; padding: 5px;")
        layout.addWidget(self.info_label)
    
    def update_for_segment(self, source_text: str, source_lang: str, target_lang: str):
        """
        Update the termview display for a new segment
        
        Args:
            source_text: Source segment text
            source_lang: Source language code
            target_lang: Target language code
        """
        self.current_source = source_text
        self.current_source_lang = source_lang
        self.current_target_lang = target_lang
        
        # Clear existing blocks
        self.clear_terms()
        
        if not source_text or not source_text.strip():
            self.info_label.setText("No segment selected")
            return
        
        # Get all termbase matches first to detect multi-word terms
        all_matches = self.get_all_termbase_matches(source_text)
        
        # Create tokens, respecting multi-word terms
        tokens = self.tokenize_with_multiword_terms(source_text, all_matches)
        
        if not tokens:
            self.info_label.setText("No words to analyze")
            return
        
        # Search termbases for each token (use pre-fetched matches)
        term_blocks_created = 0
        for token in tokens:
            # Check if we already have matches for this token
            translations = all_matches.get(token.lower(), [])
            
            # If no exact match, try searching (for single words)
            if not translations and ' ' not in token:
                translations = self.search_term(token)
            
            # Create term block
            term_block = TermBlock(token, translations, self)
            term_block.term_clicked.connect(self.on_term_insert_requested)
            
            # Insert before the stretch
            self.terms_layout.insertWidget(self.terms_layout.count() - 1, term_block)
            
            if translations:
                term_blocks_created += 1
        
        # Update info
        if term_blocks_created > 0:
            self.info_label.setText(f"✓ Found terminology for {term_blocks_created} of {len(tokens)} terms/words")
        else:
            self.info_label.setText(f"No terminology matches found for this segment")
    
    def get_all_termbase_matches(self, text: str) -> Dict[str, List[Dict]]:
        """
        Get all termbase matches for text, including multi-word terms
        
        Strategy: Get all active termbase entries, then check which ones appear in the text
        
        Args:
            text: Source text
            
        Returns:
            Dict mapping source term (lowercase) to list of translation dicts
        """
        if not self.db_manager or not self.current_source_lang or not self.current_target_lang:
            return {}
        
        matches = {}
        
        try:
            # Get all termbase entries for this language pair
            # Query database directly for efficiency
            query = """
                SELECT 
                    t.id, t.source_term, t.target_term, t.termbase_id, t.priority, 
                    t.forbidden, t.source_lang, t.target_lang, t.definition, t.domain,
                    t.notes, t.project, t.client,
                    tb.name as termbase_name,
                    tb.is_project_termbase,
                    tb.ranking
                FROM termbase_terms t
                LEFT JOIN termbases tb ON CAST(t.termbase_id AS INTEGER) = tb.id
                WHERE tb.read_only = 0
                AND (
                    (t.source_lang = ? OR (t.source_lang IS NULL AND tb.source_lang = ?))
                    OR (t.source_lang IS NULL AND tb.source_lang IS NULL)
                )
                AND (
                    (t.target_lang = ? OR (t.target_lang IS NULL AND tb.target_lang = ?))
                    OR (t.target_lang IS NULL AND tb.target_lang IS NULL)
                )
                ORDER BY LENGTH(t.source_term) DESC
            """
            
            cursor = self.db_manager.cursor
            cursor.execute(query, [
                self.current_source_lang, self.current_source_lang,
                self.current_target_lang, self.current_target_lang
            ])
            
            text_lower = text.lower()
            
            # Check each termbase entry to see if it appears in the text
            for row in cursor.fetchall():
                result_dict = dict(row)
                source_term = result_dict.get('source_term', '')
                
                if not source_term:
                    continue
                
                # Check if this term appears in the text (case-insensitive, word boundary check)
                # Use word boundaries for single words, substring search for multi-word terms
                if ' ' in source_term:
                    # Multi-word term: check if it appears as substring
                    if source_term.lower() in text_lower:
                        key = source_term.lower()
                        if key not in matches:
                            matches[key] = []
                        matches[key].append(result_dict)
                else:
                    # Single word: use word boundary check
                    pattern = r'\b' + re.escape(source_term.lower()) + r'\b'
                    if re.search(pattern, text_lower):
                        key = source_term.lower()
                        if key not in matches:
                            matches[key] = []
                        matches[key].append(result_dict)
            
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
            List of tokens (words/phrases), with multi-word terms kept together
        """
        # Sort matched terms by length (longest first) to match multi-word terms first
        matched_terms = sorted(matches.keys(), key=len, reverse=True)
        
        # Track which parts of the text have been matched
        text_lower = text.lower()
        used_positions = set()
        tokens_with_positions = []
        
        # First pass: find multi-word terms
        for term in matched_terms:
            if ' ' in term:  # Only process multi-word terms in first pass
                # Find all occurrences of this term
                start = 0
                while True:
                    pos = text_lower.find(term, start)
                    if pos == -1:
                        break
                    
                    # Check if this position overlaps with already matched terms
                    term_positions = set(range(pos, pos + len(term)))
                    if not term_positions.intersection(used_positions):
                        # Extract the original case version
                        original_term = text[pos:pos + len(term)]
                        tokens_with_positions.append((pos, len(term), original_term))
                        used_positions.update(term_positions)
                    
                    start = pos + 1
        
        # Second pass: fill in gaps with single words
        words = re.findall(r'\b[\w-]+\b', text, re.UNICODE)
        word_pattern = re.compile(r'\b[\w-]+\b', re.UNICODE)
        
        for match in word_pattern.finditer(text):
            word_start = match.start()
            word_end = match.end()
            word_positions = set(range(word_start, word_end))
            
            # Only add if not already covered by a multi-word term
            if not word_positions.intersection(used_positions):
                word = match.group()
                # Filter out very short words unless they're all caps
                if len(word) >= 3 or word.isupper():
                    tokens_with_positions.append((word_start, len(word), word))
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
            List of translation dicts
        """
        if not self.db_manager or not self.current_source_lang or not self.current_target_lang:
            return []
        
        try:
            # Use database manager's search_termbases method
            results = self.db_manager.search_termbases(
                search_term=term,
                source_lang=self.current_source_lang,
                target_lang=self.current_target_lang,
                min_length=2
            )
            
            return results
        except Exception as e:
            self.log(f"✗ Error searching term '{term}': {e}")
            return []
    
    def clear_terms(self):
        """Clear all term blocks"""
        # Remove all widgets except the stretch
        while self.terms_layout.count() > 1:
            item = self.terms_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def on_term_insert_requested(self, source_term: str, target_term: str):
        """Handle request to insert a translation"""
        self.log(f"💡 Termview: Inserting '{target_term}' for '{source_term}'")
        self.term_insert_requested.emit(target_term)
