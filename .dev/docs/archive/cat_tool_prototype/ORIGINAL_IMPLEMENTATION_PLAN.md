# Supervertaler CAT Tool Implementation Plan

**Created:** October 1, 2025  
**Purpose:** Transform Supervertaler into a full-featured CAT (Computer-Aided Translation) tool

---

## 🎯 Project Goals

Transform Supervertaler from a batch translation tool into a professional CAT tool with:
- DOCX file import/export
- SRX-based segmentation
- Interactive segment grid editor
- Inline formatting tag support
- Find/replace across segments
- Segment filtering capabilities

---

## 📋 High-Level Implementation Plan

### **Phase 1: Foundation & Architecture (Weeks 1-2)**
Restructure the application to support CAT tool functionality alongside existing features.

### **Phase 2: DOCX Import & Segmentation (Weeks 3-4)**
Implement robust file parsing and SRX-based segmentation.

### **Phase 3: Grid Editor Interface (Weeks 5-6)**
Build the core editing interface with segment management.

### **Phase 4: Tag Handling & Formatting (Week 7)**
Implement inline formatting preservation.

### **Phase 5: Search & Filter Features (Week 8)**
Add find/replace and filtering capabilities.

### **Phase 6: Integration & Polish (Week 9+)**
Connect with existing translation features and refine UX.

---

## 🔍 Detailed Step-by-Step Plan

### **PHASE 1: Foundation & Architecture**

#### Step 1.1: Create New Application Mode
- Add "CAT Editor" mode alongside "Translate" and "Proofread"
- Create separate UI section for CAT tool features
- Design data structures for segment management

**Implementation Notes:**
```python
# Add to mode selection in GUI
MODES = ["Translate", "Proofread", "CAT Editor"]

# Update mode change handler
def update_ui_for_mode(self):
    mode = self.mode_var.get()
    if mode == "CAT Editor":
        self.show_cat_editor_interface()
    # ... existing code
```

#### Step 1.2: Set Up Project Structure
```python
# New classes to add:
- SegmentManager: Handles segment storage and manipulation
- DocumentParser: Parses DOCX files
- SRXSegmenter: Applies SRX rules for segmentation
- GridEditor: Manages the editing grid UI
- TagManager: Handles inline formatting tags
- FindReplaceDialog: Search and replace functionality
- FilterPanel: Segment filtering
- DOCXExporter: Export translated documents
```

#### Step 1.3: Install Required Libraries
```powershell
# Run in terminal
pip install python-docx    # Better DOCX handling than zipfile
pip install lxml           # For SRX parsing
pip install regex          # For advanced segmentation rules
pip install chardet        # For encoding detection
```

**Add to imports:**
```python
# At top of Supervertaler_v2.x.x.py
try:
    from docx import Document
    PYTHON_DOCX_AVAILABLE = True
except ImportError:
    PYTHON_DOCX_AVAILABLE = False
    print("WARNING: python-docx not installed. CAT Editor features disabled.")

try:
    import regex as re2  # More powerful than standard re
    REGEX_AVAILABLE = True
except ImportError:
    REGEX_AVAILABLE = False
    print("WARNING: regex library not installed. Using standard re module.")
```

---

### **PHASE 2: DOCX Import & Segmentation**

#### Step 2.1: Implement DOCX Parser

**Create new file: `cat_tool/docx_parser.py`**

```python
"""
DOCX Parser for CAT Tool
Extracts text with formatting information from DOCX files
"""

from docx import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import re

class FormattingRun:
    """Represents a run of text with specific formatting"""
    def __init__(self, text, bold=False, italic=False, underline=False, 
                 font_name=None, font_size=None, hyperlink=None):
        self.text = text
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.font_name = font_name
        self.font_size = font_size
        self.hyperlink = hyperlink
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'text': self.text,
            'bold': self.bold,
            'italic': self.italic,
            'underline': self.underline,
            'font_name': self.font_name,
            'font_size': self.font_size,
            'hyperlink': self.hyperlink
        }

class ParsedParagraph:
    """Represents a paragraph with formatting information"""
    def __init__(self, runs, style=None, alignment=None):
        self.runs = runs  # List of FormattingRun objects
        self.style = style
        self.alignment = alignment
        
    def get_plain_text(self):
        """Get plain text without formatting"""
        return ''.join(run.text for run in self.runs)
    
    def get_text_with_tags(self):
        """Get text with inline formatting tags"""
        result = []
        tag_counter = 1
        
        for run in self.runs:
            text = run.text
            
            # Wrap with formatting tags
            if run.bold:
                text = f"<b{tag_counter}>{text}</b{tag_counter}>"
                tag_counter += 1
            if run.italic:
                text = f"<i{tag_counter}>{text}</i{tag_counter}>"
                tag_counter += 1
            if run.underline:
                text = f"<u{tag_counter}>{text}</u{tag_counter}>"
                tag_counter += 1
            if run.hyperlink:
                text = f"<link{tag_counter} url='{run.hyperlink}'>{text}</link{tag_counter}>"
                tag_counter += 1
                
            result.append(text)
        
        return ''.join(result)

class DOCXParser:
    """Extract text with formatting information from DOCX files"""
    
    def __init__(self, log_queue=None):
        self.log_queue = log_queue
        self.document = None
        
    def log(self, message):
        """Log message to queue if available"""
        if self.log_queue:
            self.log_queue.put(f"[DOCX Parser] {message}")
        else:
            print(f"[DOCX Parser] {message}")
    
    def parse_document(self, docx_path):
        """
        Parse DOCX file and extract paragraphs with formatting
        
        Returns: List of ParsedParagraph objects
        """
        self.log(f"Parsing DOCX file: {docx_path}")
        
        try:
            self.document = Document(docx_path)
        except Exception as e:
            self.log(f"ERROR: Failed to open DOCX: {e}")
            return []
        
        paragraphs = []
        
        # Parse all paragraphs (including those in tables)
        for element in self.document.element.body:
            if isinstance(element, CT_P):
                # Regular paragraph
                para = Paragraph(element, self.document)
                parsed = self._parse_paragraph(para)
                if parsed:
                    paragraphs.append(parsed)
                    
            elif isinstance(element, CT_Tbl):
                # Table - parse cells
                table = Table(element, self.document)
                for row in table.rows:
                    for cell in row.cells:
                        for para in cell.paragraphs:
                            parsed = self._parse_paragraph(para)
                            if parsed:
                                paragraphs.append(parsed)
        
        self.log(f"Parsed {len(paragraphs)} paragraphs")
        return paragraphs
    
    def _parse_paragraph(self, paragraph):
        """Parse a single paragraph and extract runs with formatting"""
        if not paragraph.text.strip():
            return None  # Skip empty paragraphs
        
        runs = []
        
        for run in paragraph.runs:
            if not run.text:
                continue
                
            # Extract formatting
            formatting_run = FormattingRun(
                text=run.text,
                bold=run.bold,
                italic=run.italic,
                underline=run.underline,
                font_name=run.font.name if run.font.name else None,
                font_size=run.font.size.pt if run.font.size else None,
                hyperlink=self._get_hyperlink(run)
            )
            runs.append(formatting_run)
        
        return ParsedParagraph(
            runs=runs,
            style=paragraph.style.name if paragraph.style else None,
            alignment=str(paragraph.alignment) if paragraph.alignment else None
        )
    
    def _get_hyperlink(self, run):
        """Extract hyperlink URL if run contains one"""
        # Check if run is part of a hyperlink
        try:
            # Navigate up to find hyperlink element
            element = run._element
            if element.tag.endswith('hyperlink'):
                return element.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        except:
            pass
        return None
    
    def extract_with_tags(self, docx_path):
        """
        Extract text with inline tags
        
        Returns: List of strings with inline formatting tags
        Example: ["This is <b1>bold</b1> and <i2>italic</i2> text."]
        """
        paragraphs = self.parse_document(docx_path)
        return [para.get_text_with_tags() for para in paragraphs if para]
    
    def extract_plain_text(self, docx_path):
        """
        Extract plain text only (no formatting)
        
        Returns: List of plain text strings
        """
        paragraphs = self.parse_document(docx_path)
        return [para.get_plain_text() for para in paragraphs if para]
```

#### Step 2.2: Implement SRX Segmenter

**Create new file: `cat_tool/srx_segmenter.py`**

```python
"""
SRX (Segmentation Rules eXchange) Segmenter
Implements industry-standard segmentation rules
"""

import re
import regex as re2  # More powerful regex library
from lxml import etree
from typing import List, Tuple

class SegmentationRule:
    """Represents a single SRX segmentation rule"""
    def __init__(self, break_rule=True, before_pattern="", after_pattern=""):
        self.break_rule = break_rule  # True = break, False = exception
        self.before_pattern = before_pattern
        self.after_pattern = after_pattern
        
    def matches(self, text, position):
        """Check if rule matches at given position"""
        before_text = text[:position]
        after_text = text[position:]
        
        # Check before pattern
        if self.before_pattern:
            if not re.search(self.before_pattern + r'$', before_text):
                return False
        
        # Check after pattern
        if self.after_pattern:
            if not re.match(r'^' + self.after_pattern, after_text):
                return False
        
        return True

class SRXSegmenter:
    """Segment text using SRX (Segmentation Rules eXchange) rules"""
    
    def __init__(self, log_queue=None):
        self.log_queue = log_queue
        self.rules = []  # List of SegmentationRule objects
        self.language_rules = {}  # Language-specific rules
        
    def log(self, message):
        """Log message to queue if available"""
        if self.log_queue:
            self.log_queue.put(f"[SRX Segmenter] {message}")
        else:
            print(f"[SRX Segmenter] {message}")
    
    def load_srx_file(self, srx_file_path, language_code='en'):
        """
        Parse SRX XML file and load rules for specified language
        
        SRX file structure:
        <srx>
          <body>
            <languagerules>
              <languagerule languagerulename="English">
                <rule break="yes">
                  <beforebreak>...</beforebreak>
                  <afterbreak>...</afterbreak>
                </rule>
              </languagerule>
            </languagerules>
          </body>
        </srx>
        """
        self.log(f"Loading SRX rules from: {srx_file_path}")
        
        try:
            tree = etree.parse(srx_file_path)
            root = tree.getroot()
            
            # Find language rules
            for lang_rule in root.xpath('.//languagerule'):
                lang_name = lang_rule.get('languagerulename', '').lower()
                
                # Check if this is the language we want
                if language_code.lower() not in lang_name and lang_name not in language_code.lower():
                    continue
                
                rules = []
                
                # Parse rules
                for rule in lang_rule.xpath('.//rule'):
                    break_attr = rule.get('break', 'yes')
                    is_break = (break_attr.lower() == 'yes')
                    
                    before_elem = rule.find('beforebreak')
                    after_elem = rule.find('afterbreak')
                    
                    before_pattern = before_elem.text if before_elem is not None else ""
                    after_pattern = after_elem.text if after_elem is not None else ""
                    
                    seg_rule = SegmentationRule(
                        break_rule=is_break,
                        before_pattern=before_pattern,
                        after_pattern=after_pattern
                    )
                    rules.append(seg_rule)
                
                self.language_rules[language_code] = rules
                self.log(f"Loaded {len(rules)} rules for {language_code}")
                return True
        
        except Exception as e:
            self.log(f"ERROR loading SRX file: {e}")
            return False
    
    def load_default_rules(self, language_code='en'):
        """Load simple default rules if no SRX file available"""
        self.log("Loading default segmentation rules")
        
        # Simple sentence-ending rules
        default_rules = [
            # Exception: Don't break after abbreviations
            SegmentationRule(break_rule=False, 
                           before_pattern=r'\b(Mr|Mrs|Dr|Prof|Inc|Ltd|etc|vs|e\.g|i\.e)',
                           after_pattern=r'\s'),
            
            # Exception: Don't break after single letters followed by period
            SegmentationRule(break_rule=False,
                           before_pattern=r'\b[A-Z]',
                           after_pattern=r'\s'),
            
            # Break: After period, question mark, or exclamation followed by space and capital
            SegmentationRule(break_rule=True,
                           before_pattern=r'[.!?]',
                           after_pattern=r'\s+[A-Z]'),
            
            # Break: After colon followed by newline
            SegmentationRule(break_rule=True,
                           before_pattern=r':',
                           after_pattern=r'\n'),
        ]
        
        self.language_rules[language_code] = default_rules
        self.log(f"Loaded {len(default_rules)} default rules")
    
    def segment_text(self, text, language_code='en'):
        """
        Apply segmentation rules to text
        
        Returns: List of segments (strings)
        """
        if not text.strip():
            return []
        
        # Load rules if not already loaded
        if language_code not in self.language_rules:
            self.load_default_rules(language_code)
        
        rules = self.language_rules.get(language_code, [])
        
        # Find break points
        break_points = [0]  # Start of text
        
        # Check each position in text
        for i in range(1, len(text)):
            # Check if any break rule matches
            for rule in rules:
                if rule.break_rule and rule.matches(text, i):
                    # Check if any exception rule prevents this break
                    blocked = False
                    for exception in rules:
                        if not exception.break_rule and exception.matches(text, i):
                            blocked = True
                            break
                    
                    if not blocked:
                        break_points.append(i)
                        break
        
        break_points.append(len(text))  # End of text
        
        # Extract segments
        segments = []
        for i in range(len(break_points) - 1):
            start = break_points[i]
            end = break_points[i + 1]
            segment = text[start:end].strip()
            if segment:
                segments.append(segment)
        
        self.log(f"Segmented text into {len(segments)} segments")
        return segments
    
    def segment_paragraphs(self, paragraphs, language_code='en'):
        """
        Segment a list of paragraphs
        
        Returns: List of (paragraph_index, segment_text) tuples
        """
        all_segments = []
        
        for para_idx, paragraph in enumerate(paragraphs):
            segments = self.segment_text(paragraph, language_code)
            for segment in segments:
                all_segments.append((para_idx, segment))
        
        return all_segments
    
    def segment_with_tags(self, text_with_tags, language_code='en'):
        """
        Segment text while preserving inline formatting tags
        
        Example input: "This is <b1>bold</b1>. Another sentence."
        Example output: ["This is <b1>bold</b1>.", "Another sentence."]
        """
        # First, extract tags and their positions
        tag_pattern = r'<(/?)([a-z]+)(\d+)([^>]*)>'
        tags = []
        plain_text = text_with_tags
        
        for match in re.finditer(tag_pattern, text_with_tags):
            tags.append({
                'full': match.group(0),
                'pos': match.start(),
                'length': len(match.group(0))
            })
        
        # Remove tags temporarily for segmentation
        plain_text = re.sub(tag_pattern, '', text_with_tags)
        
        # Segment plain text
        segments = self.segment_text(plain_text, language_code)
        
        # Re-insert tags into appropriate segments
        # (This is simplified - full implementation needs position tracking)
        # For now, keep tags with the segment they belong to
        
        return segments  # TODO: Implement full tag preservation
```

#### Step 2.3: Create Default SRX Rules

**Create file: `segmentation_rules/default_en.srx`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<srx version="2.0" xmlns="http://www.lisa.org/srx20">
  <header segmentsubflows="yes" cascade="yes">
    <formathandle type="start" include="no"/>
    <formathandle type="end" include="yes"/>
    <formathandle type="isolated" include="no"/>
  </header>
  <body>
    <languagerules>
      <languagerule languagerulename="English">
        <!-- Exception rules (break="no") -->
        <rule break="no">
          <beforebreak>\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|Inc|Ltd|Co|Corp)</beforebreak>
          <afterbreak>\.\s</afterbreak>
        </rule>
        <rule break="no">
          <beforebreak>\b(etc|vs|e\.g|i\.e|cf|approx|ca)</beforebreak>
          <afterbreak>\.\s</afterbreak>
        </rule>
        <rule break="no">
          <beforebreak>\b[A-Z]</beforebreak>
          <afterbreak>\.\s</afterbreak>
        </rule>
        <rule break="no">
          <beforebreak>\d</beforebreak>
          <afterbreak>\.\d</afterbreak>
        </rule>
        
        <!-- Break rules (break="yes") -->
        <rule break="yes">
          <beforebreak>[.!?]</beforebreak>
          <afterbreak>\s+[A-Z\"]</afterbreak>
        </rule>
        <rule break="yes">
          <beforebreak>[.!?]</beforebreak>
          <afterbreak>\n</afterbreak>
        </rule>
        <rule break="yes">
          <beforebreak>:</beforebreak>
          <afterbreak>\n</afterbreak>
        </rule>
      </languagerule>
    </languagerules>
  </body>
</srx>
```

**Create file: `segmentation_rules/README.md`**

```markdown
# Segmentation Rules

This folder contains SRX (Segmentation Rules eXchange) files for different languages.

## Files

- `default_en.srx` - English segmentation rules
- `default_nl.srx` - Dutch segmentation rules (to be added)
- `default_de.srx` - German segmentation rules (to be added)

## Custom Rules

You can add your own SRX files to the `custom_rules/` subfolder.

## SRX Format

SRX files define rules for where to break text into segments (sentences).
Each rule has:
- `break="yes"` - Create a segment break here
- `break="no"` - Exception: Don't break here even if it looks like a break point
- `<beforebreak>` - Pattern that must match before the break point
- `<afterbreak>` - Pattern that must match after the break point

## Resources

- SRX 2.0 Specification: http://www.gala-global.org/srx-20-april-7-2008
- SRX Tool: https://github.com/rrays/srx
```

---

### **PHASE 3: Grid Editor Interface**

#### Step 3.1: Design Segment Data Model

**Create file: `cat_tool/segment_manager.py`**

```python
"""
Segment Manager
Handles segment data storage and manipulation
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json

@dataclass
class Tag:
    """Represents an inline formatting tag"""
    type: str  # 'bold', 'italic', 'underline', 'hyperlink'
    tag_id: int  # Unique ID for matching
    start: int  # Character position in text
    end: int
    attributes: dict = field(default_factory=dict)  # For hyperlinks, etc.
    
    def to_dict(self):
        return {
            'type': self.type,
            'tag_id': self.tag_id,
            'start': self.start,
            'end': self.end,
            'attributes': self.attributes
        }

@dataclass
class Segment:
    """Represents a translation segment"""
    id: int
    source_text: str
    target_text: str = ""
    source_tags: List[Tag] = field(default_factory=list)
    target_tags: List[Tag] = field(default_factory=list)
    status: str = "untranslated"  # untranslated, draft, translated, approved, locked
    modified: bool = False
    locked: bool = False
    notes: str = ""
    paragraph_id: int = 0  # For document reconstruction
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Translation memory match info
    tm_match_score: int = 0  # 0-100
    tm_match_source: str = ""
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'source_text': self.source_text,
            'target_text': self.target_text,
            'source_tags': [tag.to_dict() for tag in self.source_tags],
            'target_tags': [tag.to_dict() for tag in self.target_tags],
            'status': self.status,
            'modified': self.modified,
            'locked': self.locked,
            'notes': self.notes,
            'paragraph_id': self.paragraph_id,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'tm_match_score': self.tm_match_score,
            'tm_match_source': self.tm_match_source
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Segment from dictionary"""
        # Reconstruct tags
        source_tags = [Tag(**tag) for tag in data.get('source_tags', [])]
        target_tags = [Tag(**tag) for tag in data.get('target_tags', [])]
        
        return cls(
            id=data['id'],
            source_text=data['source_text'],
            target_text=data.get('target_text', ''),
            source_tags=source_tags,
            target_tags=target_tags,
            status=data.get('status', 'untranslated'),
            modified=data.get('modified', False),
            locked=data.get('locked', False),
            notes=data.get('notes', ''),
            paragraph_id=data.get('paragraph_id', 0),
            created_at=data.get('created_at', datetime.now().isoformat()),
            modified_at=data.get('modified_at', datetime.now().isoformat()),
            tm_match_score=data.get('tm_match_score', 0),
            tm_match_source=data.get('tm_match_source', '')
        )

class SegmentManager:
    """Manages a collection of segments"""
    
    def __init__(self):
        self.segments: List[Segment] = []
        self.current_segment_id: Optional[int] = None
        self.modified: bool = False
        
    def add_segment(self, segment: Segment):
        """Add a segment to the collection"""
        self.segments.append(segment)
        self.modified = True
        
    def get_segment(self, segment_id: int) -> Optional[Segment]:
        """Get segment by ID"""
        for seg in self.segments:
            if seg.id == segment_id:
                return seg
        return None
    
    def update_segment(self, segment_id: int, target_text: str, 
                      status: str = None, notes: str = None):
        """Update segment target text and optional metadata"""
        segment = self.get_segment(segment_id)
        if segment:
            segment.target_text = target_text
            segment.modified = True
            segment.modified_at = datetime.now().isoformat()
            
            if status:
                segment.status = status
            if notes is not None:
                segment.notes = notes
                
            self.modified = True
            return True
        return False
    
    def get_segments_by_status(self, status: str) -> List[Segment]:
        """Get all segments with given status"""
        return [seg for seg in self.segments if seg.status == status]
    
    def get_untranslated_count(self) -> int:
        """Count untranslated segments"""
        return len([s for s in self.segments if s.status == "untranslated"])
    
    def get_completion_percentage(self) -> float:
        """Calculate completion percentage"""
        if not self.segments:
            return 0.0
        translated = len([s for s in self.segments 
                         if s.status in ["translated", "approved"]])
        return (translated / len(self.segments)) * 100
    
    def search_segments(self, query: str, search_in: str = "both", 
                       case_sensitive: bool = False) -> List[Segment]:
        """
        Search for segments containing query
        search_in: 'source', 'target', or 'both'
        """
        results = []
        
        if not case_sensitive:
            query = query.lower()
        
        for segment in self.segments:
            source = segment.source_text if case_sensitive else segment.source_text.lower()
            target = segment.target_text if case_sensitive else segment.target_text.lower()
            
            found = False
            if search_in in ['source', 'both'] and query in source:
                found = True
            if search_in in ['target', 'both'] and query in target:
                found = True
            
            if found:
                results.append(segment)
        
        return results
    
    def save_to_file(self, filepath: str):
        """Save segments to JSON file"""
        data = {
            'segments': [seg.to_dict() for seg in self.segments],
            'saved_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.modified = False
    
    def load_from_file(self, filepath: str):
        """Load segments from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.segments = [Segment.from_dict(seg_data) 
                        for seg_data in data['segments']]
        self.modified = False
```

#### Step 3.2: Create Grid Widget

**Create file: `cat_tool/grid_editor.py`**

```python
"""
Segment Grid Editor
Main editing interface for CAT tool
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional
from .segment_manager import Segment, SegmentManager

class SegmentGrid:
    """Main editing grid for segments with Excel-like interface"""
    
    def __init__(self, parent, segment_manager: SegmentManager, 
                 on_segment_select: Optional[Callable] = None):
        self.parent = parent
        self.segment_manager = segment_manager
        self.on_segment_select = on_segment_select
        
        # Create frame
        self.frame = tk.Frame(parent)
        
        # Create Treeview with columns
        self.tree = ttk.Treeview(self.frame, 
                                 columns=('num', 'status', 'source', 'target', 'match'),
                                 show='tree headings',
                                 selectmode='browse')
        
        # Define column headings
        self.tree.heading('num', text='#')
        self.tree.heading('status', text='Status')
        self.tree.heading('source', text='Source')
        self.tree.heading('target', text='Target')
        self.tree.heading('match', text='TM%')
        
        # Configure column widths
        self.tree.column('#0', width=0, stretch=False)  # Hide tree column
        self.tree.column('num', width=50, anchor='center')
        self.tree.column('status', width=100, anchor='center')
        self.tree.column('source', width=400, anchor='w')
        self.tree.column('target', width=400, anchor='w')
        self.tree.column('match', width=50, anchor='center')
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, 
                                    command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL,
                                    command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set,
                           xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        self.tree.bind('<Double-1>', self._on_double_click)
        self.tree.bind('<Return>', self._on_enter_key)
        
        # Configure row colors based on status
        self.tree.tag_configure('untranslated', background='#ffe6e6')  # Light red
        self.tree.tag_configure('draft', background='#fff9e6')  # Light yellow
        self.tree.tag_configure('translated', background='#e6ffe6')  # Light green
        self.tree.tag_configure('approved', background='#e6f3ff')  # Light blue
        self.tree.tag_configure('locked', background='#f0f0f0')  # Gray
        
        # Store segment ID to tree item mapping
        self.segment_to_item = {}
        
    def pack(self, **kwargs):
        """Pack the grid frame"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the grid frame"""
        self.frame.grid(**kwargs)
    
    def load_segments(self, segments: List[Segment] = None):
        """Populate grid with segments"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.segment_to_item.clear()
        
        # Use segments from manager if not provided
        if segments is None:
            segments = self.segment_manager.segments
        
        # Add segments to tree
        for segment in segments:
            self._add_segment_to_tree(segment)
    
    def _add_segment_to_tree(self, segment: Segment):
        """Add a single segment to the tree"""
        # Prepare display values
        num = str(segment.id)
        status = segment.status.capitalize()
        source = self._truncate_text(segment.source_text, 100)
        target = self._truncate_text(segment.target_text, 100) if segment.target_text else ""
        match = f"{segment.tm_match_score}%" if segment.tm_match_score > 0 else ""
        
        # Insert into tree
        item = self.tree.insert('', 'end', 
                               values=(num, status, source, target, match),
                               tags=(segment.status,))
        
        # Store mapping
        self.segment_to_item[segment.id] = item
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text for display"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def update_segment_display(self, segment_id: int):
        """Update the display for a specific segment"""
        segment = self.segment_manager.get_segment(segment_id)
        if not segment:
            return
        
        item = self.segment_to_item.get(segment_id)
        if not item:
            return
        
        # Update values
        status = segment.status.capitalize()
        target = self._truncate_text(segment.target_text, 100) if segment.target_text else ""
        match = f"{segment.tm_match_score}%" if segment.tm_match_score > 0 else ""
        
        self.tree.item(item, values=(segment.id, status, 
                                     self._truncate_text(segment.source_text, 100),
                                     target, match),
                      tags=(segment.status,))
    
    def get_selected_segment(self) -> Optional[Segment]:
        """Return currently selected segment"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        # Get segment ID from first column
        values = self.tree.item(selection[0], 'values')
        if not values:
            return None
        
        segment_id = int(values[0])
        return self.segment_manager.get_segment(segment_id)
    
    def select_segment(self, segment_id: int):
        """Select a specific segment by ID"""
        item = self.segment_to_item.get(segment_id)
        if item:
            self.tree.selection_set(item)
            self.tree.see(item)
            self.tree.focus(item)
    
    def select_next(self):
        """Select next segment"""
        selection = self.tree.selection()
        if not selection:
            # Select first item
            children = self.tree.get_children()
            if children:
                self.tree.selection_set(children[0])
                self.tree.see(children[0])
            return
        
        current = selection[0]
        next_item = self.tree.next(current)
        if next_item:
            self.tree.selection_set(next_item)
            self.tree.see(next_item)
    
    def select_previous(self):
        """Select previous segment"""
        selection = self.tree.selection()
        if not selection:
            return
        
        current = selection[0]
        prev_item = self.tree.prev(current)
        if prev_item:
            self.tree.selection_set(prev_item)
            self.tree.see(prev_item)
    
    def _on_select(self, event):
        """Handle segment selection"""
        segment = self.get_selected_segment()
        if segment and self.on_segment_select:
            self.on_segment_select(segment)
    
    def _on_double_click(self, event):
        """Handle double-click to edit"""
        # Could open detail editor or inline editing
        pass
    
    def _on_enter_key(self, event):
        """Handle Enter key - move to next segment"""
        self.select_next()
```

#### Step 3.3: Add Segment Editor Panel

**Create file: `cat_tool/segment_editor.py`**

```python
"""
Segment Editor Panel
Detailed editor for individual segments
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from .segment_manager import Segment, SegmentManager

class SegmentEditor:
    """Detailed editor panel for current segment"""
    
    def __init__(self, parent, segment_manager: SegmentManager,
                 on_save: Optional[Callable] = None):
        self.parent = parent
        self.segment_manager = segment_manager
        self.on_save = on_save
        self.current_segment: Optional[Segment] = None
        
        # Create main frame
        self.frame = tk.LabelFrame(parent, text="Segment Editor", padx=10, pady=10)
        
        # Segment info header
        info_frame = tk.Frame(self.frame)
        info_frame.pack(fill='x', pady=(0, 10))
        
        self.segment_info_label = tk.Label(info_frame, text="No segment selected",
                                           font=('Segoe UI', 9, 'bold'))
        self.segment_info_label.pack(side='left')
        
        # Status selector
        status_frame = tk.Frame(info_frame)
        status_frame.pack(side='right')
        
        tk.Label(status_frame, text="Status:").pack(side='left', padx=(0, 5))
        self.status_var = tk.StringVar(value="untranslated")
        self.status_combo = ttk.Combobox(status_frame, textvariable=self.status_var,
                                        values=["untranslated", "draft", "translated", 
                                               "approved", "locked"],
                                        state='readonly', width=12)
        self.status_combo.pack(side='left')
        self.status_combo.bind('<<ComboboxSelected>>', self._on_status_change)
        
        # Source text (read-only)
        source_label = tk.Label(self.frame, text="Source:", anchor='w',
                               font=('Segoe UI', 9, 'bold'))
        source_label.pack(fill='x')
        
        self.source_text = tk.Text(self.frame, height=3, wrap='word',
                                   bg='#f5f5f5', state='disabled',
                                   font=('Segoe UI', 10))
        self.source_text.pack(fill='x', pady=(2, 10))
        
        # Target text (editable)
        target_label = tk.Label(self.frame, text="Target:", anchor='w',
                               font=('Segoe UI', 9, 'bold'))
        target_label.pack(fill='x')
        
        self.target_text = tk.Text(self.frame, height=3, wrap='word',
                                   font=('Segoe UI', 10))
        self.target_text.pack(fill='x', pady=(2, 10))
        self.target_text.bind('<KeyRelease>', self._on_text_change)
        
        # Quick actions
        actions_frame = tk.Frame(self.frame)
        actions_frame.pack(fill='x', pady=(0, 10))
        
        tk.Button(actions_frame, text="Copy Source to Target",
                 command=self._copy_source_to_target).pack(side='left', padx=(0, 5))
        tk.Button(actions_frame, text="Clear Target",
                 command=self._clear_target).pack(side='left', padx=(0, 5))
        tk.Button(actions_frame, text="Save",
                 command=self._save_segment,
                 bg='#4CAF50', fg='white').pack(side='right')
        
        # Notes section
        notes_label = tk.Label(self.frame, text="Notes:", anchor='w',
                              font=('Segoe UI', 9, 'bold'))
        notes_label.pack(fill='x')
        
        self.notes_text = tk.Text(self.frame, height=2, wrap='word',
                                 font=('Segoe UI', 9))
        self.notes_text.pack(fill='x', pady=(2, 0))
        
        # TM match info (if available)
        self.tm_info_label = tk.Label(self.frame, text="", anchor='w',
                                      fg='#666', font=('Segoe UI', 8))
        self.tm_info_label.pack(fill='x', pady=(5, 0))
        
    def pack(self, **kwargs):
        """Pack the editor frame"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the editor frame"""
        self.frame.grid(**kwargs)
    
    def load_segment(self, segment: Segment):
        """Load a segment for editing"""
        self.current_segment = segment
        
        # Update header
        self.segment_info_label.config(
            text=f"Segment #{segment.id} | Paragraph {segment.paragraph_id}")
        
        # Load source text
        self.source_text.config(state='normal')
        self.source_text.delete('1.0', 'end')
        self.source_text.insert('1.0', segment.source_text)
        self.source_text.config(state='disabled')
        
        # Load target text
        self.target_text.delete('1.0', 'end')
        if segment.target_text:
            self.target_text.insert('1.0', segment.target_text)
        
        # Load status
        self.status_var.set(segment.status)
        
        # Load notes
        self.notes_text.delete('1.0', 'end')
        if segment.notes:
            self.notes_text.insert('1.0', segment.notes)
        
        # Show TM match info
        if segment.tm_match_score > 0:
            self.tm_info_label.config(
                text=f"TM Match: {segment.tm_match_score}% from {segment.tm_match_source}")
        else:
            self.tm_info_label.config(text="")
        
        # Focus target editor
        self.target_text.focus_set()
    
    def clear_segment(self):
        """Clear the editor"""
        self.current_segment = None
        self.segment_info_label.config(text="No segment selected")
        
        self.source_text.config(state='normal')
        self.source_text.delete('1.0', 'end')
        self.source_text.config(state='disabled')
        
        self.target_text.delete('1.0', 'end')
        self.notes_text.delete('1.0', 'end')
        self.status_var.set("untranslated")
        self.tm_info_label.config(text="")
    
    def _save_segment(self):
        """Save current segment"""
        if not self.current_segment:
            return
        
        # Get updated values
        target_text = self.target_text.get('1.0', 'end-1c').strip()
        status = self.status_var.get()
        notes = self.notes_text.get('1.0', 'end-1c').strip()
        
        # Update segment
        self.segment_manager.update_segment(
            self.current_segment.id,
            target_text=target_text,
            status=status,
            notes=notes
        )
        
        # Callback
        if self.on_save:
            self.on_save(self.current_segment.id)
    
    def _on_text_change(self, event):
        """Handle text changes"""
        # Could auto-save or mark as modified
        pass
    
    def _on_status_change(self, event):
        """Handle status change"""
        # Auto-save when status changes
        self._save_segment()
    
    def _copy_source_to_target(self):
        """Copy source text to target"""
        if not self.current_segment:
            return
        
        self.target_text.delete('1.0', 'end')
        self.target_text.insert('1.0', self.current_segment.source_text)
    
    def _clear_target(self):
        """Clear target text"""
        self.target_text.delete('1.0', 'end')
```

---

### **PHASE 4: Tag Handling & Formatting**

*(Implementation details for tag handling - to be continued...)*

---

### **PHASE 5: Search & Filter Features**

*(Implementation details for search/filter - to be continued...)*

---

### **PHASE 6: Integration & Polish**

*(Implementation details for integration - to be continued...)*

---

## 🎯 Minimum Viable Product (MVP) Checklist

For the first working version:

- [ ] Basic DOCX import (paragraphs only)
- [ ] Simple sentence segmentation (regex-based)
- [ ] Grid display with source/target columns
- [ ] Editable target column
- [ ] Save/load segment data (JSON)
- [ ] Basic find/replace in target
- [ ] Simple status filter
- [ ] Export to TSV/TXT
- [ ] Segment counter and progress bar

---

## 📦 Required Python Packages

```bash
pip install python-docx    # DOCX handling
pip install lxml           # XML parsing for SRX
pip install regex          # Advanced regex
```

---

## 🔧 Integration Points with Existing Supervertaler

1. **Translation Agent Integration**: Use existing AI agents to translate selected segments
2. **TM Integration**: Use TMAgent to pre-populate segments with TM matches
3. **Project Management**: Save CAT projects alongside existing projects
4. **Custom Prompts**: Apply custom prompts when translating segments
5. **Tracked Changes**: Use for terminology consistency

---

## 📈 Future Enhancements (Post-MVP)

- XLIFF import/export
- SDL SDLXLIFF support
- Real-time collaboration
- Terminology database
- QA checks (numbers, punctuation, tags)
- Segment splitting/merging
- Concordance search
- Auto-propagation
- Fuzzy TM matching
- Machine translation integration
- Comment threads per segment

---

## 🎨 UI Mockup Concept

```
┌─────────────────────────────────────────────────────────────┐
│  Supervertaler CAT Editor                          [_][□][X] │
├─────────────────────────────────────────────────────────────┤
│ File  Edit  View  Tools  Translation  Help                  │
├─────────────────────────────────────────────────────────────┤
│ [Open DOCX] [Save] [Export] │ Filter: [All ▼] Search: [...] │
├─────────────────────────────────────────────────────────────┤
│  # │ Status      │ Source             │ Target              │
├────┼─────────────┼────────────────────┼─────────────────────┤
│  1 │ Translated  │ This is a test.    │ Dit is een test.    │
│  2 │ Draft       │ Another sentence.  │ Nog een zin.        │
│  3 │ Untranslated│ Third example.     │                     │
│  4 │ Approved    │ Final text.        │ Laatste tekst.      │
├─────────────────────────────────────────────────────────────┤
│ Segment Editor                                               │
│ Segment #3 | Paragraph 2                    Status: [Draft▼]│
│ Source: Third example.                                       │
│ Target: [_______________________________________________]    │
│ Notes:  [_______________________________________________]    │
│ [Copy Source] [Clear] [AI Translate]              [Save]    │
├─────────────────────────────────────────────────────────────┤
│ Progress: 75% (3/4 translated) │ Modified: Yes │ Words: 428 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Implementation Notes

### Key Design Decisions

1. **Data Storage**: Use JSON for segment storage (easy to read/edit, version control friendly)
2. **Grid Widget**: Use Tkinter Treeview (built-in, no dependencies)
3. **Segmentation**: Start with simple regex, add SRX support later
4. **Tags**: Use inline format like `<b1>text</b1>` initially
5. **Auto-save**: Save on segment change to prevent data loss

### Performance Considerations

- For large documents (>10,000 segments), implement virtual scrolling
- Cache formatted text to avoid re-rendering
- Use background threads for AI translation to keep UI responsive
- Implement undo/redo with limited history (last 50 actions)

### Testing Strategy

1. Unit tests for segmenter
2. Test with various DOCX files (Word 2007+)
3. Test with documents containing:
   - Complex formatting
   - Tables
   - Images
   - Hyperlinks
   - Track changes
4. Load testing with large documents

---

## 🚀 Next Steps

1. **Review this plan** and adjust priorities
2. **Set up development branch** for CAT features
3. **Implement MVP components** in order
4. **Create prototype UI** for user testing
5. **Iterate based on feedback**

---

## 📞 Questions to Consider

Before starting implementation:

1. Should CAT editor be a separate mode or separate window?
2. Should we support opening multiple documents simultaneously?
3. What file formats are highest priority? (DOCX, PDF, TXT?)
4. Should we implement our own SRX engine or use existing library?
5. How to handle conflicts between manual edits and AI suggestions?
6. Should we support plugins/extensions for future features?

---

**End of Implementation Plan**

This document will be updated as development progresses.
