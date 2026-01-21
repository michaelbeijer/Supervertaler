"""
Non-Translatables Manager Module

Manages non-translatable (NT) content - terms, phrases, and patterns that should 
not be translated. These include brand names, product names, technical identifiers,
codes, abbreviations, and other content that must remain in the original language.

File Format: .ntl (Non-Translatable List)
- YAML frontmatter with metadata
- Simple line-by-line entries (one NT per line)
- Comments start with #
- Blank lines are ignored

Import Support:
- Native .svntl format
- memoQ .mqres non-translatable lists (XML format)

Features:
- Multiple NT lists per project
- Case-sensitive/insensitive matching options
- Merge import with duplicate detection
- Export to native format
"""

import os
import re
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime


@dataclass
class NonTranslatable:
    """Single non-translatable entry"""
    text: str
    case_sensitive: bool = True  # Default to case-sensitive matching
    category: str = ""
    notes: str = ""
    
    def matches(self, source_text: str) -> List[Tuple[int, int]]:
        """
        Find all occurrences of this NT in source text.
        
        Matching is:
        - Case-sensitive by default (case_sensitive=True)
        - Full word only (uses word boundaries to avoid matching inside other words)
        - Special characters (®, ™, etc.) are handled specially
        
        Returns:
            List of (start_pos, end_pos) tuples for each match
        """
        matches = []
        pattern = self.text
        
        # Escape special regex characters in the pattern
        escaped_pattern = re.escape(pattern)
        
        # Set regex flags based on case sensitivity
        flags = 0 if self.case_sensitive else re.IGNORECASE
        
        # Check if pattern starts/ends with word characters (letters, digits, underscore)
        # Word boundaries only work properly between word and non-word characters
        starts_with_word_char = pattern and pattern[0].isalnum()
        ends_with_word_char = pattern and pattern[-1].isalnum()
        
        # Build pattern with appropriate boundaries
        if starts_with_word_char:
            boundary_pattern = r'\b' + escaped_pattern
        else:
            # For patterns starting with special chars, use start of string or whitespace/punctuation
            boundary_pattern = r'(?:^|(?<=\s)|(?<=[^\w]))' + escaped_pattern
        
        if ends_with_word_char:
            boundary_pattern = boundary_pattern + r'\b'
        else:
            # For patterns ending with special chars (like ®, ™), no trailing boundary needed
            # The special char itself acts as a natural boundary
            pass
        
        try:
            for match in re.finditer(boundary_pattern, source_text, flags):
                matches.append((match.start(), match.end()))
        except re.error:
            # Fallback: try simpler word boundary pattern
            try:
                simple_pattern = r'\b' + escaped_pattern + r'\b'
                for match in re.finditer(simple_pattern, source_text, flags):
                    matches.append((match.start(), match.end()))
            except re.error:
                # Final fallback: match anywhere but verify it's not inside a word
                try:
                    for match in re.finditer(escaped_pattern, source_text, flags):
                        start, end = match.start(), match.end()
                        # Check if this is a standalone match (not inside a word)
                        before_ok = start == 0 or not source_text[start-1].isalnum()
                        after_ok = end == len(source_text) or not source_text[end].isalnum()
                        if before_ok and after_ok:
                            matches.append((start, end))
                except re.error:
                    pass
        
        return matches


@dataclass
class NonTranslatableList:
    """A list of non-translatables with metadata"""
    name: str
    entries: List[NonTranslatable] = field(default_factory=list)
    description: str = ""
    created_date: str = ""
    modified_date: str = ""
    source_language: str = ""
    target_language: str = ""
    is_active: bool = True
    filepath: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_date:
            self.created_date = datetime.now().isoformat()
        if not self.modified_date:
            self.modified_date = datetime.now().isoformat()
    
    @property
    def entry_count(self) -> int:
        return len(self.entries)
    
    def get_unique_texts(self) -> Set[str]:
        """Get set of all NT texts (lowercase for comparison)"""
        return {nt.text.lower() for nt in self.entries}
    
    def find_matches(self, source_text: str) -> List[Dict]:
        """
        Find all NT matches in source text.
        
        Returns:
            List of dicts with 'text', 'start', 'end', 'entry' keys
        """
        all_matches = []
        
        for entry in self.entries:
            positions = entry.matches(source_text)
            for start, end in positions:
                # Get the actual matched text from source (preserves original case)
                matched_text = source_text[start:end]
                all_matches.append({
                    'text': matched_text,
                    'start': start,
                    'end': end,
                    'entry': entry,
                    'list_name': self.name
                })
        
        # Sort by position, then by length (longer matches first for same position)
        all_matches.sort(key=lambda m: (m['start'], -(m['end'] - m['start'])))
        
        return all_matches


class NonTranslatablesManager:
    """Manages non-translatable lists: loading, saving, searching, import/export"""
    
    # File extension for native format
    FILE_EXTENSION = ".svntl"
    LEGACY_EXTENSION = ".ntl"  # For backward compatibility
    
    def __init__(self, base_path: str, log_callback=None):
        """
        Initialize manager.
        
        Args:
            base_path: Base path for NT files (typically user_data/resources/non_translatables)
            log_callback: Optional logging function
        """
        self.base_path = Path(base_path)
        self.log = log_callback if log_callback else print
        self.lists: Dict[str, NonTranslatableList] = {}  # name -> list
        self.active_lists: List[str] = []  # Names of active lists
        
        # Ensure directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    # ========================================================================
    # FILE FORMAT: .ntl (YAML frontmatter + line entries)
    # ========================================================================
    
    def save_list(self, nt_list: NonTranslatableList, filepath: Optional[str] = None) -> bool:
        """
        Save a non-translatable list to .ntl format.
        
        Format:
            ---
            name: List Name
            description: Optional description
            created_date: ISO date
            modified_date: ISO date
            source_language: en
            target_language: nl
            ---
            # Comments start with #
            Brand Name
            Product™
            Technical Term
        
        Args:
            nt_list: The list to save
            filepath: Optional specific path (defaults to base_path/name.ntl)
            
        Returns:
            True if successful
        """
        try:
            if filepath is None:
                # Sanitize name for filename
                safe_name = re.sub(r'[<>:"/\\|?*]', '_', nt_list.name)
                filepath = self.base_path / f"{safe_name}{self.FILE_EXTENSION}"
            
            filepath = Path(filepath)
            
            # Update modified date
            nt_list.modified_date = datetime.now().isoformat()
            nt_list.filepath = str(filepath)
            
            # Build YAML frontmatter
            metadata = {
                'name': nt_list.name,
                'description': nt_list.description,
                'created_date': nt_list.created_date,
                'modified_date': nt_list.modified_date,
                'source_language': nt_list.source_language,
                'target_language': nt_list.target_language,
                'is_active': nt_list.is_active,
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write YAML frontmatter
                f.write("---\n")
                yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                f.write("---\n\n")
                
                # Write entries (one per line)
                f.write("# Non-translatable entries (one per line)\n")
                f.write(f"# Total entries: {len(nt_list.entries)}\n\n")
                
                for entry in nt_list.entries:
                    # If entry has notes or category, add as comment
                    if entry.notes:
                        f.write(f"# {entry.notes}\n")
                    f.write(f"{entry.text}\n")
            
            self.log(f"✓ Saved NT list: {nt_list.name} ({len(nt_list.entries)} entries)")
            return True
            
        except Exception as e:
            self.log(f"✗ Error saving NT list: {e}")
            return False
    
    def load_list(self, filepath: str) -> Optional[NonTranslatableList]:
        """
        Load a non-translatable list from .ntl format.
        
        Args:
            filepath: Path to .ntl file
            
        Returns:
            NonTranslatableList or None if failed
        """
        try:
            filepath = Path(filepath)
            
            if not filepath.exists():
                self.log(f"✗ File not found: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter
            metadata = {}
            entries = []
            
            if content.startswith('---'):
                # Find the closing ---
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1].strip()
                    body = parts[2].strip()
                    
                    try:
                        metadata = yaml.safe_load(yaml_content) or {}
                    except yaml.YAMLError as e:
                        self.log(f"⚠️ YAML parse error, treating as plain text: {e}")
                        body = content
                else:
                    body = content
            else:
                body = content
            
            # Parse entries (one per line, skip comments and empty lines)
            for line in body.splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    entries.append(NonTranslatable(text=line))
            
            # Create list object
            nt_list = NonTranslatableList(
                name=metadata.get('name', filepath.stem),
                entries=entries,
                description=metadata.get('description', ''),
                created_date=metadata.get('created_date', ''),
                modified_date=metadata.get('modified_date', ''),
                source_language=metadata.get('source_language', ''),
                target_language=metadata.get('target_language', ''),
                is_active=metadata.get('is_active', True),
                filepath=str(filepath)
            )
            
            self.log(f"✓ Loaded NT list: {nt_list.name} ({len(entries)} entries)")
            return nt_list
            
        except Exception as e:
            self.log(f"✗ Error loading NT list: {e}")
            return None
    
    def load_from_plain_text(self, filepath: str, name: Optional[str] = None) -> Optional[NonTranslatableList]:
        """
        Load entries from a plain text file (one entry per line).
        
        Args:
            filepath: Path to text file
            name: Optional name for the list (defaults to filename)
            
        Returns:
            NonTranslatableList or None if failed
        """
        try:
            filepath = Path(filepath)
            
            if not filepath.exists():
                self.log(f"✗ File not found: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            entries = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    entries.append(NonTranslatable(text=line))
            
            list_name = name or filepath.stem
            
            nt_list = NonTranslatableList(
                name=list_name,
                entries=entries,
                description=f"Imported from {filepath.name}",
                filepath=str(filepath)
            )
            
            self.log(f"✓ Loaded {len(entries)} entries from plain text: {filepath.name}")
            return nt_list
            
        except Exception as e:
            self.log(f"✗ Error loading plain text file: {e}")
            return None
    
    # ========================================================================
    # MEMOQ IMPORT (.mqres XML format)
    # ========================================================================
    
    def import_memoq_mqres(self, filepath: str, name: Optional[str] = None) -> Optional[NonTranslatableList]:
        """
        Import non-translatables from memoQ .mqres format.
        
        memoQ format:
            <MemoQResource ResourceType="NonTrans" Version="1.0">
              <Resource>
                <Guid>...</Guid>
                <FileName>...</FileName>
                <Name>...</Name>
                <Description />
              </Resource>
            </MemoQResource>
            <?xml version="1.0" encoding="utf-8"?>
            <nonTrans version="1.0">
              <nonTransRule>term1</nonTransRule>
              <nonTransRule>term2</nonTransRule>
            </nonTrans>
        
        Args:
            filepath: Path to .mqres file
            name: Optional name override
            
        Returns:
            NonTranslatableList or None if failed
        """
        try:
            filepath = Path(filepath)
            
            if not filepath.exists():
                self.log(f"✗ File not found: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            entries = []
            list_name = name
            description = ""
            
            # memoQ files can have two XML documents concatenated
            # First: MemoQResource header, Second: nonTrans entries
            # We need to handle this specially
            
            # Try to find the name from MemoQResource header
            memoq_header_match = re.search(r'<MemoQResource.*?</MemoQResource>', content, re.DOTALL)
            if memoq_header_match:
                header_xml = memoq_header_match.group()
                try:
                    header_root = ET.fromstring(header_xml)
                    resource_elem = header_root.find('.//Resource')
                    if resource_elem is not None:
                        name_elem = resource_elem.find('Name')
                        if name_elem is not None and name_elem.text:
                            list_name = list_name or name_elem.text
                        desc_elem = resource_elem.find('Description')
                        if desc_elem is not None and desc_elem.text:
                            description = desc_elem.text
                except ET.ParseError:
                    pass
            
            # Find and parse the nonTrans section
            nontrans_match = re.search(r'<nonTrans.*?</nonTrans>', content, re.DOTALL)
            if nontrans_match:
                nontrans_xml = nontrans_match.group()
                # Clean up any XML declaration in the middle of the file
                nontrans_xml = re.sub(r'<\?xml[^?]*\?>', '', nontrans_xml)
                
                try:
                    root = ET.fromstring(nontrans_xml)
                    
                    # Find all nonTransRule elements
                    for rule in root.findall('.//nonTransRule'):
                        if rule.text and rule.text.strip():
                            entries.append(NonTranslatable(text=rule.text.strip()))
                    
                except ET.ParseError as e:
                    self.log(f"⚠️ XML parse error in nonTrans section: {e}")
            
            if not list_name:
                list_name = filepath.stem
            
            nt_list = NonTranslatableList(
                name=list_name,
                entries=entries,
                description=description or f"Imported from memoQ: {filepath.name}",
                filepath=str(filepath)
            )
            
            self.log(f"✓ Imported memoQ NT list: {list_name} ({len(entries)} entries)")
            return nt_list
            
        except Exception as e:
            self.log(f"✗ Error importing memoQ file: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
            return None
    
    # ========================================================================
    # LIST MANAGEMENT
    # ========================================================================
    
    def load_all_lists(self) -> int:
        """
        Load all .svntl and legacy .ntl files from the base directory.
        
        Returns:
            Number of lists loaded
        """
        self.lists.clear()
        count = 0
        
        # Load new .svntl files
        for filepath in self.base_path.glob(f"*{self.FILE_EXTENSION}"):
            nt_list = self.load_list(str(filepath))
            if nt_list:
                self.lists[nt_list.name] = nt_list
                if nt_list.is_active:
                    self.active_lists.append(nt_list.name)
                count += 1
        
        # Also load legacy .ntl files (backward compatibility)
        for filepath in self.base_path.glob(f"*{self.LEGACY_EXTENSION}"):
            nt_list = self.load_list(str(filepath))
            if nt_list and nt_list.name not in self.lists:  # Don't overwrite if already loaded
                self.lists[nt_list.name] = nt_list
                if nt_list.is_active:
                    self.active_lists.append(nt_list.name)
                count += 1
        
        self.log(f"Loaded {count} NT lists ({len(self.active_lists)} active)")
        return count
    
    def get_all_lists(self) -> List[NonTranslatableList]:
        """Get all loaded lists"""
        return list(self.lists.values())
    
    def get_active_lists(self) -> List[NonTranslatableList]:
        """Get only active lists"""
        return [self.lists[name] for name in self.active_lists if name in self.lists]
    
    def set_list_active(self, name: str, active: bool):
        """Set whether a list is active"""
        if name in self.lists:
            self.lists[name].is_active = active
            if active and name not in self.active_lists:
                self.active_lists.append(name)
            elif not active and name in self.active_lists:
                self.active_lists.remove(name)
    
    def create_list(self, name: str, description: str = "") -> NonTranslatableList:
        """Create a new empty NT list"""
        nt_list = NonTranslatableList(
            name=name,
            description=description
        )
        self.lists[name] = nt_list
        self.active_lists.append(name)
        return nt_list
    
    def delete_list(self, name: str) -> bool:
        """Delete a list (removes from memory and disk)"""
        if name not in self.lists:
            return False
        
        nt_list = self.lists[name]
        
        # Remove file if it exists
        if nt_list.filepath:
            try:
                filepath = Path(nt_list.filepath)
                if filepath.exists():
                    filepath.unlink()
            except Exception as e:
                self.log(f"⚠️ Could not delete file: {e}")
        
        # Remove from memory
        del self.lists[name]
        if name in self.active_lists:
            self.active_lists.remove(name)
        
        self.log(f"✓ Deleted NT list: {name}")
        return True
    
    # ========================================================================
    # MERGE & IMPORT
    # ========================================================================
    
    def merge_into_list(self, target_name: str, source_list: NonTranslatableList, 
                        ignore_duplicates: bool = True) -> Tuple[int, int]:
        """
        Merge entries from source list into target list.
        
        Args:
            target_name: Name of target list (must exist)
            source_list: Source list to merge from
            ignore_duplicates: If True, skip entries that already exist
            
        Returns:
            Tuple of (added_count, skipped_count)
        """
        if target_name not in self.lists:
            self.log(f"✗ Target list not found: {target_name}")
            return (0, 0)
        
        target = self.lists[target_name]
        existing = target.get_unique_texts()
        
        added = 0
        skipped = 0
        
        for entry in source_list.entries:
            if entry.text.lower() in existing:
                if ignore_duplicates:
                    skipped += 1
                    continue
            
            target.entries.append(entry)
            existing.add(entry.text.lower())
            added += 1
        
        target.modified_date = datetime.now().isoformat()
        
        self.log(f"✓ Merged into {target_name}: {added} added, {skipped} duplicates skipped")
        return (added, skipped)
    
    def add_entry(self, list_name: str, text: str, notes: str = "", category: str = "") -> bool:
        """Add a single entry to a list"""
        if list_name not in self.lists:
            return False
        
        entry = NonTranslatable(text=text, notes=notes, category=category)
        self.lists[list_name].entries.append(entry)
        self.lists[list_name].modified_date = datetime.now().isoformat()
        return True
    
    def remove_entry(self, list_name: str, text: str) -> bool:
        """Remove an entry from a list by text"""
        if list_name not in self.lists:
            return False
        
        nt_list = self.lists[list_name]
        original_count = len(nt_list.entries)
        nt_list.entries = [e for e in nt_list.entries if e.text != text]
        
        if len(nt_list.entries) < original_count:
            nt_list.modified_date = datetime.now().isoformat()
            return True
        return False
    
    # ========================================================================
    # SEARCH & MATCHING
    # ========================================================================
    
    def find_all_matches(self, source_text: str) -> List[Dict]:
        """
        Find all NT matches in source text from all active lists.
        
        Args:
            source_text: Text to search in
            
        Returns:
            List of match dicts sorted by position
        """
        all_matches = []
        
        for nt_list in self.get_active_lists():
            matches = nt_list.find_matches(source_text)
            all_matches.extend(matches)
        
        # Sort by position, remove overlapping matches (keep longer ones)
        all_matches.sort(key=lambda m: (m['start'], -(m['end'] - m['start'])))
        
        # Remove overlapping matches
        filtered = []
        last_end = -1
        for match in all_matches:
            if match['start'] >= last_end:
                filtered.append(match)
                last_end = match['end']
        
        return filtered
    
    def get_unique_entries_from_active(self) -> Set[str]:
        """Get all unique NT entries from active lists (lowercase)"""
        entries = set()
        for nt_list in self.get_active_lists():
            entries.update(nt_list.get_unique_texts())
        return entries
    
    # ========================================================================
    # EXPORT
    # ========================================================================
    
    def export_list(self, name: str, filepath: str) -> bool:
        """
        Export a list to .ntl format.
        
        Args:
            name: Name of list to export
            filepath: Destination file path
            
        Returns:
            True if successful
        """
        if name not in self.lists:
            self.log(f"✗ List not found: {name}")
            return False
        
        return self.save_list(self.lists[name], filepath)
    
    def export_to_plain_text(self, name: str, filepath: str) -> bool:
        """
        Export a list to plain text (one entry per line).
        
        Args:
            name: Name of list to export
            filepath: Destination file path
            
        Returns:
            True if successful
        """
        if name not in self.lists:
            self.log(f"✗ List not found: {name}")
            return False
        
        try:
            nt_list = self.lists[name]
            with open(filepath, 'w', encoding='utf-8') as f:
                for entry in nt_list.entries:
                    f.write(f"{entry.text}\n")
            
            self.log(f"✓ Exported to plain text: {filepath}")
            return True
            
        except Exception as e:
            self.log(f"✗ Error exporting: {e}")
            return False


# ============================================================================
# CONVENIENCE FUNCTION FOR CONVERSION
# ============================================================================

def convert_txt_to_ntl(input_path: str, output_path: Optional[str] = None, 
                       name: Optional[str] = None) -> bool:
    """
    Convert a plain text NT file to .ntl format.
    
    Args:
        input_path: Path to input .txt file
        output_path: Path for output .ntl file (defaults to same dir with .ntl extension)
        name: Name for the list (defaults to filename)
        
    Returns:
        True if successful
    """
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path.with_suffix('.ntl')
    
    manager = NonTranslatablesManager(str(input_path.parent))
    nt_list = manager.load_from_plain_text(str(input_path), name)
    
    if nt_list:
        return manager.save_list(nt_list, str(output_path))
    
    return False
