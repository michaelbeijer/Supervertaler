"""
Superlookup Engine
==================
System-wide translation lookup that works anywhere on your computer.
Captures text from any application and provides:
- TM matches from Supervertaler database
- Glossary term lookups
- MT/AI translations
- Web search integration

Can operate in different modes:
- memoQ mode (with CAT tool shortcuts)
- Trados mode
- CafeTran mode
- Universal mode (works in any text box)
"""

import pyperclip
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class LookupResult:
    """Single lookup result"""
    source: str
    target: str
    match_percent: int
    source_type: str  # 'tm', 'glossary', 'mt', 'ai'
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SuperlookupEngine:
    """
    Superlookup text lookup engine.
    Captures text from any application and provides translation results.
    """
    
    def __init__(self, mode='universal'):
        """
        Initialize the lookup engine.
        
        Args:
            mode: Operating mode - 'memoq', 'trados', 'cafetran', or 'universal'
        """
        self.mode = mode
        self.tm_database = None
        self.glossary_database = None
        self.mt_providers = []
        
        # Mode-specific shortcuts
        self.mode_shortcuts = {
            'memoq': {
                'copy_source_to_target': ('ctrl', 'shift', 's'),
                'select_all': ('ctrl', 'a'),
                'copy': ('ctrl', 'c'),
                'paste': ('ctrl', 'v'),
            },
            'trados': {
                'copy_source_to_target': ('ctrl', 'insert'),  # Example - verify
                'select_all': ('ctrl', 'a'),
                'copy': ('ctrl', 'c'),
                'paste': ('ctrl', 'v'),
            },
            'cafetran': {
                'copy_source_to_target': ('ctrl', 'g'),  # Example - verify
                'select_all': ('ctrl', 'a'),
                'copy': ('ctrl', 'c'),
                'paste': ('ctrl', 'v'),
            },
            'universal': {
                'select_all': ('ctrl', 'a'),
                'copy': ('ctrl', 'c'),
                'paste': ('ctrl', 'v'),
            }
        }
    
    def capture_text(self) -> Optional[str]:
        """
        Capture text - just copy what's selected and get clipboard.
        
        Returns:
            Captured text or None if failed
        """
        try:
            # keyboard module is Windows-only
            try:
                import keyboard
                # Wait for hotkey to release before sending Ctrl+C
                time.sleep(0.2)
                # Use keyboard library to send Ctrl+C
                keyboard.press_and_release('ctrl+c')
                time.sleep(0.2)
            except ImportError:
                # On non-Windows, just try to get clipboard content directly
                # (user needs to have copied text manually)
                pass
            
            # Get clipboard
            text = pyperclip.paste()
            return text if text else None
            
        except Exception as e:
            print(f"Error capturing text: {e}")
            return None
    
    def set_tm_database(self, tm_db):
        """Set the TM database for lookups"""
        self.tm_database = tm_db
    
    def set_enabled_tm_ids(self, tm_ids: List[str]):
        """Set which TM IDs to search (for independent Superlookup selection)"""
        self.enabled_tm_ids = tm_ids if tm_ids else None
    
    def set_glossary_database(self, glossary_db):
        """Set the glossary database for term lookups"""
        self.glossary_database = glossary_db
    
    def search_tm(self, text: str, max_results: int = 10, direction: str = 'both',
                  source_lang: str = None, target_lang: str = None) -> List[LookupResult]:
        """
        Search translation memory for matches.
        Uses concordance search to find entries containing the search text.
        
        Args:
            text: Source text to search for
            max_results: Maximum number of results to return
            direction: 'source' = search source only, 'target' = search target only, 'both' = bidirectional
            source_lang: Filter by source language (None = any)
            target_lang: Filter by target language (None = any)
            
        Returns:
            List of TM match results
        """
        results = []
        
        if not self.tm_database:
            print(f"[DEBUG] SuperlookupEngine.search_tm: tm_database is None!")
            return results
        
        try:
            # Use concordance search - finds entries CONTAINING the search text
            # This is better for Superlookup than fuzzy matching
            tm_ids_to_use = self.enabled_tm_ids if hasattr(self, 'enabled_tm_ids') and self.enabled_tm_ids else None
            print(f"[DEBUG] SuperlookupEngine.search_tm: Using concordance_search with tm_ids={tm_ids_to_use}, direction={direction}, source_lang={source_lang}, target_lang={target_lang}")
            
            if hasattr(self.tm_database, 'concordance_search'):
                matches = self.tm_database.concordance_search(
                    query=text,
                    tm_ids=tm_ids_to_use,
                    direction=direction,
                    source_lang=source_lang,
                    target_lang=target_lang
                )
                print(f"[DEBUG] SuperlookupEngine.search_tm: Concordance search returned {len(matches)} matches")
                
                # Convert to LookupResult format (limit results)
                for match in matches[:max_results]:
                    # Use 'source' and 'target' keys (matches database column names)
                    source_text = match.get('source', '')
                    target_text = match.get('target', '')
                    print(f"[Superlookup] Extracted: source='{source_text[:50]}...', target='{target_text[:50]}...'")
                    results.append(LookupResult(
                        source=source_text,
                        target=target_text,
                        match_percent=100,  # Concordance = contains the text
                        source_type='tm',
                        metadata={
                            'match_type': 'concordance',
                            'tm_name': match.get('tm_name', 'Unknown'),
                            'tm_id': match.get('tm_id', '')
                        }
                    ))
            else:
                print(f"[DEBUG] SuperlookupEngine.search_tm: tm_database has no concordance_search method!")
            
        except Exception as e:
            print(f"Error searching TM: {e}")
            import traceback
            traceback.print_exc()
        
        return results
    
    def search_glossary(self, text: str) -> List[LookupResult]:
        """
        Search glossary for term matches.
        
        Args:
            text: Text to extract terms from and search
            
        Returns:
            List of glossary term matches
        """
        results = []
        
        if not self.glossary_database:
            return results
        
        try:
            # Simple word-by-word lookup for now
            # TODO: Implement proper term extraction
            words = text.lower().split()
            
            if hasattr(self.glossary_database, 'search_terms'):
                terms = self.glossary_database.search_terms(words)
                for term, translation in terms:
                    results.append(LookupResult(
                        source=term,
                        target=translation,
                        match_percent=100,
                        source_type='glossary',
                        metadata={'context': text}
                    ))
            
        except Exception as e:
            print(f"Error searching glossary: {e}")
        
        return results
    
    def get_mt_translations(self, text: str) -> List[LookupResult]:
        """
        Get machine translation suggestions.
        
        Args:
            text: Text to translate
            
        Returns:
            List of MT results
        """
        results = []
        
        # TODO: Integrate with MT providers (DeepL, Google, OpenAI)
        # For now, return placeholder
        
        return results
    
    def lookup_all(self, text: str) -> Dict[str, List[LookupResult]]:
        """
        Perform all types of lookups on the text.
        
        Args:
            text: Text to look up
            
        Returns:
            Dictionary with 'tm', 'glossary', 'mt' keys containing results
        """
        return {
            'tm': self.search_tm(text),
            'glossary': self.search_glossary(text),
            'mt': self.get_mt_translations(text)
        }
