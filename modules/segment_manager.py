"""
Segment Manager Module
Contains core classes for segment representation and layout modes

Author: Supervertaler Project (Michael Beijer + Claude)
Date: October 5, 2025
Version: 2.5.0
"""

from datetime import datetime
from typing import Dict, Any, List


class LayoutMode:
    """Layout mode constants for CAT editor display"""
    GRID = "grid"      # memoQ-style inline editing
    SPLIT = "split"    # List view with editor panel
    DOCUMENT = "document" # Document flow view with clickable segments


class Segment:
    """Represents a translation segment
    
    This is the core data structure for both CAT editor and AI translation workflows.
    Each segment contains source text, target translation, status, and metadata.
    """
    
    def __init__(self, seg_id: int, source: str, paragraph_id: int = 0, 
                 is_table_cell: bool = False, table_info: tuple = None,
                 style: str = None, document_position: int = 0):
        """Initialize a translation segment
        
        Args:
            seg_id: Unique segment identifier
            source: Source text to be translated
            paragraph_id: ID of the paragraph this segment belongs to
            is_table_cell: Whether this segment is from a table cell
            table_info: Tuple (table_idx, row_idx, cell_idx) if is_table_cell
            style: Paragraph style (e.g., "Heading 1", "Normal", "Title")
            document_position: Position in original document
        """
        self.id = seg_id
        self.source = source
        self.target = ""
        self.status = "untranslated"  # untranslated, draft, translated, approved
        self.paragraph_id = paragraph_id
        self.document_position = document_position  # Position in original document
        self.notes = ""
        self.modified = False
        self.created_at = datetime.now().isoformat()
        self.modified_at = datetime.now().isoformat()
        
        # Table information
        self.is_table_cell = is_table_cell
        self.table_info = table_info  # (table_idx, row_idx, cell_idx) if is_table_cell
        
        # Style information (Heading 1, Normal, Title, etc.)
        self.style = style or "Normal"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert segment to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'source': self.source,
            'target': self.target,
            'status': self.status,
            'paragraph_id': self.paragraph_id,
            'document_position': self.document_position,
            'notes': self.notes,
            'modified': self.modified,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'is_table_cell': self.is_table_cell,
            'table_info': self.table_info,
            'style': self.style
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Segment':
        """Create Segment from dictionary
        
        Args:
            data: Dictionary containing segment data
            
        Returns:
            Segment instance
        """
        seg = cls(data['id'], data['source'], data.get('paragraph_id', 0),
                  data.get('is_table_cell', False), data.get('table_info'),
                  data.get('style', 'Normal'), data.get('document_position', 0))
        seg.target = data.get('target', '')
        seg.status = data.get('status', 'untranslated')
        seg.notes = data.get('notes', '')
        seg.modified = data.get('modified', False)
        seg.created_at = data.get('created_at', datetime.now().isoformat())
        seg.modified_at = data.get('modified_at', datetime.now().isoformat())
        return seg
    
    def update_target(self, target_text: str, status: str = None):
        """Update target translation and mark as modified
        
        Args:
            target_text: New target text
            status: New status (if None, keeps current status)
        """
        self.target = target_text
        self.modified = True
        self.modified_at = datetime.now().isoformat()
        if status:
            self.status = status
    
    def __repr__(self):
        """String representation for debugging"""
        return f"Segment(id={self.id}, source='{self.source[:30]}...', status={self.status})"


class SegmentManager:
    """Manages a collection of segments with utility methods"""
    
    def __init__(self, segments: List[Segment] = None):
        """Initialize segment manager
        
        Args:
            segments: Optional initial list of segments
        """
        self.segments = segments or []
    
    def add_segment(self, segment: Segment):
        """Add a segment to the collection"""
        self.segments.append(segment)
    
    def get_segment(self, seg_id: int) -> Segment:
        """Get segment by ID
        
        Args:
            seg_id: Segment ID to find
            
        Returns:
            Segment with matching ID or None
        """
        for seg in self.segments:
            if seg.id == seg_id:
                return seg
        return None
    
    def get_untranslated_segments(self) -> List[Segment]:
        """Get all segments with 'untranslated' status"""
        return [seg for seg in self.segments if seg.status == "untranslated"]
    
    def get_all_source_texts(self) -> List[str]:
        """Get all source texts as a list"""
        return [seg.source for seg in self.segments]
    
    def update_translations(self, translations: List[str], status: str = "draft"):
        """Update all segments with translations
        
        Args:
            translations: List of translated texts (same order as segments)
            status: Status to set for updated segments
        """
        if len(translations) != len(self.segments):
            raise ValueError(f"Translation count ({len(translations)}) doesn't match segment count ({len(self.segments)})")
        
        for seg, trans in zip(self.segments, translations):
            seg.update_target(trans, status)
    
    def to_dict_list(self) -> List[Dict[str, Any]]:
        """Convert all segments to list of dictionaries"""
        return [seg.to_dict() for seg in self.segments]
    
    @classmethod
    def from_dict_list(cls, data_list: List[Dict[str, Any]]) -> 'SegmentManager':
        """Create SegmentManager from list of dictionaries
        
        Args:
            data_list: List of segment dictionaries
            
        Returns:
            SegmentManager instance with loaded segments
        """
        segments = [Segment.from_dict(data) for data in data_list]
        return cls(segments)
    
    def __len__(self):
        """Return number of segments"""
        return len(self.segments)
    
    def __iter__(self):
        """Make segments iterable"""
        return iter(self.segments)
