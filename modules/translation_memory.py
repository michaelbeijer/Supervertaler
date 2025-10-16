"""
Translation Memory Module

Manages translation memory with fuzzy matching capabilities.
Supports multiple TMs: Project TM, Big Mama TM, and custom TMX files.

Extracted from main Supervertaler file for better modularity.
"""

import os
import xml.etree.ElementTree as ET
from datetime import datetime
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple


class TM:
    """Individual Translation Memory with metadata"""
    
    def __init__(self, name: str, tm_id: str, enabled: bool = True, read_only: bool = False):
        self.name = name
        self.tm_id = tm_id
        self.enabled = enabled
        self.read_only = read_only
        self.entries: Dict[str, str] = {}  # source -> target mapping
        self.metadata = {
            'source_lang': None,
            'target_lang': None,
            'file_path': None,
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        }
        self.fuzzy_threshold = 0.75
    
    def add_entry(self, source: str, target: str):
        """Add translation pair to this TM"""
        if not self.read_only and source and target:
            self.entries[source.strip()] = target.strip()
            self.metadata['modified'] = datetime.now().isoformat()
    
    def get_exact_match(self, source: str) -> Optional[str]:
        """Get exact match from this TM"""
        return self.entries.get(source.strip())
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity ratio between two texts"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def get_fuzzy_matches(self, source: str, max_matches: int = 5) -> List[Dict]:
        """Get fuzzy matches from this TM"""
        source = source.strip()
        matches = []
        
        for tm_source, tm_target in self.entries.items():
            similarity = self.calculate_similarity(source, tm_source)
            if similarity >= self.fuzzy_threshold:
                matches.append({
                    'source': tm_source,
                    'target': tm_target,
                    'similarity': similarity,
                    'match_pct': int(similarity * 100),
                    'tm_name': self.name,
                    'tm_id': self.tm_id
                })
        
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches[:max_matches]
    
    def get_entry_count(self) -> int:
        """Get number of entries in this TM"""
        return len(self.entries)
    
    def to_dict(self) -> Dict:
        """Serialize TM to dictionary for JSON storage"""
        return {
            'name': self.name,
            'tm_id': self.tm_id,
            'enabled': self.enabled,
            'read_only': self.read_only,
            'entries': self.entries,
            'metadata': self.metadata,
            'fuzzy_threshold': self.fuzzy_threshold
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'TM':
        """Deserialize TM from dictionary"""
        tm = TM(
            name=data.get('name', 'Unnamed TM'),
            tm_id=data.get('tm_id', 'unknown'),
            enabled=data.get('enabled', True),
            read_only=data.get('read_only', False)
        )
        tm.entries = data.get('entries', {})
        tm.metadata = data.get('metadata', {})
        tm.fuzzy_threshold = data.get('fuzzy_threshold', 0.75)
        return tm


class TMDatabase:
    """Manages multiple Translation Memories"""
    
    def __init__(self):
        # Core TMs
        self.project_tm = TM(name='Project TM', tm_id='project', enabled=True, read_only=False)
        self.big_mama_tm = TM(name='Big Mama', tm_id='big_mama', enabled=True, read_only=False)
        
        # Custom TMs (user-loaded TMX files)
        self.custom_tms: Dict[str, TM] = {}
        
        # Global fuzzy threshold (can be overridden per TM)
        self.fuzzy_threshold = 0.75
    
    def get_tm(self, tm_id: str) -> Optional[TM]:
        """Get TM by ID"""
        if tm_id == 'project':
            return self.project_tm
        elif tm_id == 'big_mama' or tm_id == 'main':  # Support legacy 'main' ID
            return self.big_mama_tm
        else:
            return self.custom_tms.get(tm_id)
    
    def get_all_tms(self, enabled_only: bool = False) -> List[TM]:
        """Get all TMs (optionally only enabled ones)"""
        tms = [self.project_tm, self.big_mama_tm] + list(self.custom_tms.values())
        if enabled_only:
            tms = [tm for tm in tms if tm.enabled]
        return tms
    
    def add_custom_tm(self, name: str, tm_id: str = None, read_only: bool = False) -> TM:
        """Add a new custom TM"""
        if tm_id is None:
            tm_id = f"custom_{len(self.custom_tms)}"
        tm = TM(name=name, tm_id=tm_id, enabled=True, read_only=read_only)
        self.custom_tms[tm_id] = tm
        return tm
    
    def remove_custom_tm(self, tm_id: str) -> bool:
        """Remove a custom TM"""
        if tm_id in self.custom_tms:
            del self.custom_tms[tm_id]
            return True
        return False
    
    def search_all(self, source: str, tm_ids: List[str] = None, enabled_only: bool = True) -> List[Dict]:
        """
        Search across multiple TMs
        Args:
            source: Source text to search for
            tm_ids: Specific TM IDs to search (None = search all)
            enabled_only: Only search enabled TMs
        Returns:
            List of match dictionaries sorted by similarity
        """
        all_matches = []
        
        # Determine which TMs to search
        if tm_ids:
            tms = [self.get_tm(tm_id) for tm_id in tm_ids if self.get_tm(tm_id)]
        else:
            tms = self.get_all_tms(enabled_only=enabled_only)
        
        # Search each TM
        for tm in tms:
            if tm and (not enabled_only or tm.enabled):
                matches = tm.get_fuzzy_matches(source, max_matches=10)
                all_matches.extend(matches)
        
        # Sort by similarity (highest first)
        all_matches.sort(key=lambda x: x['similarity'], reverse=True)
        return all_matches
    
    def add_to_project_tm(self, source: str, target: str):
        """Add entry to Project TM (convenience method)"""
        self.project_tm.add_entry(source, target)
    
    def get_entry_count(self, enabled_only: bool = False) -> int:
        """Get total entry count across all TMs"""
        tms = self.get_all_tms(enabled_only=enabled_only)
        return sum(tm.get_entry_count() for tm in tms)
    
    def load_tmx_file(self, filepath: str, src_lang: str, tgt_lang: str, 
                      tm_name: str = None, read_only: bool = False) -> tuple[str, int]:
        """
        Load TMX file into a new custom TM
        Returns: (tm_id, entry_count)
        """
        if tm_name is None:
            tm_name = os.path.basename(filepath).replace('.tmx', '')
        
        # Create new custom TM
        tm_id = f"custom_{os.path.basename(filepath).replace('.', '_')}"
        tm = self.add_custom_tm(tm_name, tm_id, read_only=read_only)
        
        # Load TMX content
        loaded_count = self._load_tmx_into_tm(filepath, src_lang, tgt_lang, tm)
        
        # Update metadata
        tm.metadata['file_path'] = filepath
        tm.metadata['source_lang'] = src_lang
        tm.metadata['target_lang'] = tgt_lang
        
        return tm_id, loaded_count
    
    def _load_tmx_into_tm(self, filepath: str, src_lang: str, tgt_lang: str, tm: TM) -> int:
        """Internal: Load TMX content into specific TM"""
        loaded_count = 0
        
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            xml_ns = "http://www.w3.org/XML/1998/namespace"
            
            # Normalize language codes
            src_lang = src_lang.split('-')[0].split('_')[0].lower()
            tgt_lang = tgt_lang.split('-')[0].split('_')[0].lower()
            
            for tu in root.findall('.//tu'):
                src_text, tgt_text = None, None
                
                for tuv_node in tu.findall('tuv'):
                    lang_attr = tuv_node.get(f'{{{xml_ns}}}lang')
                    if not lang_attr:
                        continue
                    
                    tmx_lang = lang_attr.split('-')[0].split('_')[0].lower()
                    
                    seg_node = tuv_node.find('seg')
                    if seg_node is not None:
                        try:
                            text = ET.tostring(seg_node, encoding='unicode', method='text').strip()
                        except:
                            text = "".join(seg_node.itertext()).strip()
                        
                        if tmx_lang == src_lang:
                            src_text = text
                        elif tmx_lang == tgt_lang:
                            tgt_text = text
                
                if src_text and tgt_text:
                    tm.add_entry(src_text, tgt_text)
                    loaded_count += 1
            
            return loaded_count
        except Exception as e:
            print(f"Error loading TMX: {e}")
            return 0
    
    def detect_tmx_languages(self, filepath: str) -> List[str]:
        """Detect all language codes present in a TMX file"""
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            xml_ns = "http://www.w3.org/XML/1998/namespace"
            
            languages = set()
            for tuv in root.findall('.//tuv'):
                lang_attr = tuv.get(f'{{{xml_ns}}}lang')
                if lang_attr:
                    languages.add(lang_attr)
            
            return sorted(list(languages))
        except:
            return []
    
    def to_dict(self) -> Dict:
        """Serialize entire database to dictionary"""
        return {
            'project_tm': self.project_tm.to_dict(),
            'big_mama_tm': self.big_mama_tm.to_dict(),
            'custom_tms': {tm_id: tm.to_dict() for tm_id, tm in self.custom_tms.items()},
            'fuzzy_threshold': self.fuzzy_threshold
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'TMDatabase':
        """Deserialize database from dictionary"""
        db = TMDatabase()
        
        if 'project_tm' in data:
            db.project_tm = TM.from_dict(data['project_tm'])
        if 'big_mama_tm' in data:
            db.big_mama_tm = TM.from_dict(data['big_mama_tm'])
        elif 'main_tm' in data:  # Legacy support
            db.big_mama_tm = TM.from_dict(data['main_tm'])
            db.big_mama_tm.name = 'Big Mama'  # Update name
            db.big_mama_tm.tm_id = 'big_mama'
        if 'custom_tms' in data:
            db.custom_tms = {tm_id: TM.from_dict(tm_data) 
                            for tm_id, tm_data in data['custom_tms'].items()}
        db.fuzzy_threshold = data.get('fuzzy_threshold', 0.75)
        
        return db


class TMAgent:
    """Legacy wrapper for backwards compatibility - delegates to TMDatabase"""
    
    def __init__(self):
        self.tm_database = TMDatabase()
        self.fuzzy_threshold = 0.75
    
    @property
    def tm_data(self):
        """Legacy property - returns Project TM entries"""
        return self.tm_database.project_tm.entries
    
    @tm_data.setter
    def tm_data(self, value: Dict[str, str]):
        """Legacy property setter"""
        self.tm_database.project_tm.entries = value
    
    def add_entry(self, source: str, target: str):
        """Add to Project TM"""
        self.tm_database.add_to_project_tm(source, target)
    
    def get_exact_match(self, source: str) -> Optional[str]:
        """Search all enabled TMs for exact match"""
        matches = self.tm_database.search_all(source, enabled_only=True)
        for match in matches:
            if match['match_pct'] == 100:
                return match['target']
        return None
    
    def get_fuzzy_matches(self, source: str, max_matches: int = 5) -> List[Tuple[str, str, float]]:
        """Legacy format - returns tuples"""
        matches = self.tm_database.search_all(source, enabled_only=True)
        return [(m['source'], m['target'], m['similarity']) for m in matches[:max_matches]]
    
    def get_best_match(self, source: str) -> Optional[Tuple[str, str, float]]:
        """Get best match in legacy format"""
        matches = self.get_fuzzy_matches(source, max_matches=1)
        return matches[0] if matches else None
    
    def load_from_tmx(self, filepath: str, src_lang: str = "en", tgt_lang: str = "nl") -> int:
        """Legacy TMX load - loads into a new custom TM"""
        tm_id, count = self.tm_database.load_tmx_file(filepath, src_lang, tgt_lang)
        return count
    
    def get_entry_count(self) -> int:
        """Get total entry count"""
        return self.tm_database.get_entry_count(enabled_only=False)
    
    def clear(self):
        """Clear Project TM only"""
        self.tm_database.project_tm.entries.clear()
