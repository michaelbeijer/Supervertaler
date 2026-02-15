"""
Trados Studio Package Handler (SDLPPX/SDLRPX)

This module handles the import and export of Trados Studio project packages.
SDLPPX = Project Package (sent to translator)
SDLRPX = Return Package (sent back to PM)

Package Structure:
- .sdlppx/.sdlrpx = ZIP archive containing:
  - *.sdlproj = XML project file with settings
  - {source-lang}/*.sdlxliff = Bilingual XLIFF files
  - {target-lang}/*.sdlxliff = Target language files (may be copies)
  - Reports/ = Analysis reports (optional)

SDLXLIFF Format:
- XLIFF 1.2 with SDL namespace extensions
- <g> tags for inline formatting
- <x> tags for standalone elements
- <mrk mtype="seg"> for segment boundaries
- sdl:conf attribute for confirmation status

Author: Supervertaler
"""

import os
import re
import zipfile
import shutil
import tempfile
import traceback
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from xml.etree import ElementTree as ET
from copy import deepcopy

# Namespaces used in SDLXLIFF
NAMESPACES = {
    'xliff': 'urn:oasis:names:tc:xliff:document:1.2',
    'sdl': 'http://sdl.com/FileTypes/SdlXliff/1.0',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# Register namespaces for proper output
for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix if prefix != 'xliff' else '', uri)

# XLIFF namespace URI (for creating elements)
XLIFF_NS = NAMESPACES['xliff']

# Regex for Supervertaler inline tag markers:
#   <ID>...</ID>  = paired tag (maps to <g id="ID">...</g>)
#   <ID/>         = standalone tag (maps to <x id="ID"/>)
# Tag IDs can be numeric (e.g. "14") or alphanumeric (e.g. "qSuperscript").
_TAG_ID = r'[A-Za-z0-9_]+'
_PAIRED_TAG_RE = re.compile(rf'<({_TAG_ID})>(.*?)</\1>', re.DOTALL)
_STANDALONE_TAG_RE = re.compile(rf'<({_TAG_ID})/>')


@dataclass
class SDLSegment:
    """Represents a segment from an SDLXLIFF file"""
    segment_id: str  # Unique ID within file
    trans_unit_id: str  # Parent trans-unit ID
    source_text: str  # Plain text (tags converted to markers)
    target_text: str  # Plain text translation
    source_xml: str  # Original XML with tags
    target_xml: str  # Target XML with tags
    status: str  # not_translated, draft, translated, etc.
    match_percent: int = 0  # TM match percentage
    origin: str = ""  # mt, tm, document-match, etc.
    text_match: str = ""  # SourceAndTarget = CM, Source = 100%
    locked: bool = False
    file_path: str = ""  # Source SDLXLIFF file


@dataclass
class SDLXLIFFFile:
    """Represents an SDLXLIFF file within a package"""
    file_path: str  # Path within package
    original_name: str  # Original document name
    source_lang: str
    target_lang: str
    segments: List[SDLSegment] = field(default_factory=list)
    
    # Store the parsed XML for modification
    tree: Any = None
    root: Any = None


@dataclass 
class TradosPackage:
    """Represents a Trados Studio project package"""
    package_path: str
    package_type: str  # 'sdlppx' or 'sdlrpx'
    project_name: str
    source_lang: str
    target_lang: str
    created_at: str
    created_by: str
    
    # Files in the package
    xliff_files: List[SDLXLIFFFile] = field(default_factory=list)
    
    # Extracted location
    extract_dir: str = ""


class SDLXLIFFParser:
    """
    Parser for SDLXLIFF files (Trados bilingual XLIFF format).
    Handles the SDL-specific extensions to standard XLIFF.
    """
    
    # Tag pattern for SDL inline tags
    TAG_PATTERN = re.compile(r'<(g|x|bx|ex|ph|it|mrk)\s[^>]*>|</(g|x|bx|ex|ph|it|mrk)>')
    
    def __init__(self, log_callback=None):
        self.log = log_callback or print
    
    def parse_file(self, file_path: str) -> Optional[SDLXLIFFFile]:
        """
        Parse an SDLXLIFF file and extract segments.
        
        Args:
            file_path: Path to the SDLXLIFF file
            
        Returns:
            SDLXLIFFFile object with parsed segments
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Get file element
            file_elem = root.find('xliff:file', NAMESPACES)
            if file_elem is None:
                # Try without namespace
                file_elem = root.find('file')
            
            if file_elem is None:
                self.log(f"ERROR: No <file> element found in {file_path}")
                return None
            
            original = file_elem.get('original', Path(file_path).stem)
            source_lang = file_elem.get('source-language', 'en')
            target_lang = file_elem.get('target-language', '')
            
            xliff_file = SDLXLIFFFile(
                file_path=file_path,
                original_name=original,
                source_lang=source_lang,
                target_lang=target_lang,
                tree=tree,
                root=root
            )
            
            # Find all trans-units
            body = file_elem.find('xliff:body', NAMESPACES)
            if body is None:
                body = file_elem.find('body')
            
            if body is None:
                self.log(f"ERROR: No <body> element found in {file_path}")
                return xliff_file
            
            # Process trans-units (may be in groups)
            trans_units = body.findall('.//xliff:trans-unit', NAMESPACES)
            if not trans_units:
                trans_units = body.findall('.//trans-unit')
            
            for tu in trans_units:
                segments = self._parse_trans_unit(tu, file_path)
                xliff_file.segments.extend(segments)
            
            self.log(f"Parsed {len(xliff_file.segments)} segments from {Path(file_path).name}")
            return xliff_file
            
        except Exception as e:
            self.log(f"ERROR parsing SDLXLIFF: {e}")
            traceback.print_exc()
            return None
    
    def _parse_trans_unit(self, tu: ET.Element, file_path: str) -> List[SDLSegment]:
        """Parse a trans-unit element into segments."""
        segments = []
        tu_id = tu.get('id', '')
        
        # Get source element
        source_elem = tu.find('xliff:source', NAMESPACES)
        if source_elem is None:
            source_elem = tu.find('source')
        
        # Get target element
        target_elem = tu.find('xliff:target', NAMESPACES)
        if target_elem is None:
            target_elem = tu.find('target')
        
        # Get seg-source for segmented content
        seg_source = tu.find('xliff:seg-source', NAMESPACES)
        if seg_source is None:
            seg_source = tu.find('seg-source')
        
        if source_elem is None:
            return segments
        
        # Check if this is a segmented trans-unit (has mrk elements)
        if seg_source is not None:
            # Parse segmented content
            segments = self._parse_segmented_unit(tu, tu_id, seg_source, target_elem, file_path)
        else:
            # Single segment
            source_xml = self._element_to_string(source_elem)
            source_text = self._extract_text(source_elem)
            
            target_xml = ""
            target_text = ""
            if target_elem is not None:
                target_xml = self._element_to_string(target_elem)
                target_text = self._extract_text(target_elem)
            
            # Get SDL-specific attributes
            sdl_seg = tu.find('.//sdl:seg', {'sdl': NAMESPACES['sdl']})
            status = self._get_segment_status(tu, sdl_seg)
            match_percent = self._get_match_percent(sdl_seg)
            origin = self._get_origin(sdl_seg)
            text_match = self._get_text_match(sdl_seg)
            locked = self._is_locked(tu, sdl_seg)
            
            segment = SDLSegment(
                segment_id=tu_id,
                trans_unit_id=tu_id,
                source_text=source_text,
                target_text=target_text,
                source_xml=source_xml,
                target_xml=target_xml,
                status=status,
                match_percent=match_percent,
                origin=origin,
                text_match=text_match,
                locked=locked,
                file_path=file_path
            )
            segments.append(segment)
        
        return segments
    
    def _parse_segmented_unit(self, tu: ET.Element, tu_id: str, 
                              seg_source: ET.Element, target_elem: ET.Element,
                              file_path: str) -> List[SDLSegment]:
        """Parse a trans-unit with segmented (mrk) content."""
        segments = []
        
        # Find all mrk elements with mtype="seg" in seg-source
        source_mrks = seg_source.findall('.//xliff:mrk[@mtype="seg"]', NAMESPACES)
        if not source_mrks:
            source_mrks = seg_source.findall('.//mrk[@mtype="seg"]')
        
        # Find corresponding target mrk elements
        target_mrks = []
        if target_elem is not None:
            target_mrks = target_elem.findall('.//xliff:mrk[@mtype="seg"]', NAMESPACES)
            if not target_mrks:
                target_mrks = target_elem.findall('.//mrk[@mtype="seg"]')
        
        # Create a map of target mrks by mid
        target_mrk_map = {mrk.get('mid'): mrk for mrk in target_mrks}
        
        # Get seg-defs for segment metadata
        seg_defs = tu.find('sdl:seg-defs', {'sdl': NAMESPACES['sdl']})
        seg_def_map = {}
        if seg_defs is not None:
            for seg in seg_defs.findall('sdl:seg', {'sdl': NAMESPACES['sdl']}):
                mid = seg.get('id')
                if mid:
                    seg_def_map[mid] = seg
        
        for source_mrk in source_mrks:
            mid = source_mrk.get('mid')
            if not mid:
                continue
            
            source_xml = self._element_inner_xml(source_mrk)
            source_text = self._extract_text(source_mrk)
            
            target_mrk = target_mrk_map.get(mid)
            target_xml = ""
            target_text = ""
            if target_mrk is not None:
                target_xml = self._element_inner_xml(target_mrk)
                target_text = self._extract_text(target_mrk)
            
            # Get segment definition
            seg_def = seg_def_map.get(mid)
            status = self._get_segment_status(tu, seg_def)
            match_percent = self._get_match_percent(seg_def)
            origin = self._get_origin(seg_def)
            text_match = self._get_text_match(seg_def)
            locked = self._is_locked(tu, seg_def)
            
            segment = SDLSegment(
                segment_id=f"{tu_id}_{mid}",
                trans_unit_id=tu_id,
                source_text=source_text,
                target_text=target_text,
                source_xml=source_xml,
                target_xml=target_xml,
                status=status,
                match_percent=match_percent,
                origin=origin,
                text_match=text_match,
                locked=locked,
                file_path=file_path
            )
            segments.append(segment)
        
        return segments
    
    def _element_to_string(self, elem: ET.Element) -> str:
        """Convert element to string including tags."""
        return ET.tostring(elem, encoding='unicode')
    
    def _element_inner_xml(self, elem: ET.Element) -> str:
        """Get inner XML of an element (content without the element itself)."""
        result = elem.text or ""
        for child in elem:
            result += ET.tostring(child, encoding='unicode')
        return result
    
    def _extract_text(self, elem: ET.Element) -> str:
        """Extract plain text from element, converting tags to markers."""
        text_parts = []
        
        def process_element(el, depth=0):
            # Add element's text
            if el.text:
                text_parts.append(el.text)
            
            # Process children
            for child in el:
                tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                
                if tag_name == 'g':
                    # Paired tag - convert to Supervertaler format
                    tag_id = child.get('id', '')
                    text_parts.append(f'<{tag_id}>')
                    process_element(child, depth + 1)
                    text_parts.append(f'</{tag_id}>')
                elif tag_name in ('x', 'ph', 'bx', 'ex'):
                    # Standalone tag
                    tag_id = child.get('id', '')
                    text_parts.append(f'<{tag_id}/>')
                elif tag_name == 'mrk':
                    # Marker - just process content
                    process_element(child, depth + 1)
                else:
                    # Unknown - include as-is
                    process_element(child, depth + 1)
                
                # Add tail text
                if child.tail:
                    text_parts.append(child.tail)
        
        process_element(elem)
        return ''.join(text_parts)
    
    def _get_segment_status(self, tu: ET.Element, seg_def: ET.Element) -> str:
        """Get segment status from SDL attributes."""
        if seg_def is not None:
            conf = seg_def.get('conf')
            if conf:
                status_map = {
                    'Draft': 'draft',
                    'Translated': 'translated',
                    'ApprovedTranslation': 'approved',
                    'ApprovedSignOff': 'approved',
                    'RejectedTranslation': 'rejected',
                    'RejectedSignOff': 'rejected'
                }
                return status_map.get(conf, 'not_translated')
        return 'not_translated'
    
    def _get_match_percent(self, seg_def: ET.Element) -> int:
        """Get TM match percentage."""
        if seg_def is not None:
            percent = seg_def.get('percent')
            if percent:
                try:
                    return int(percent)
                except ValueError:
                    pass
        return 0
    
    def _get_origin(self, seg_def: ET.Element) -> str:
        """Get segment origin (tm, mt, document-match, etc.)."""
        if seg_def is not None:
            origin = seg_def.get('origin')
            if origin:
                return origin.lower()
        return ""
    
    def _get_text_match(self, seg_def: ET.Element) -> str:
        """Get text-match attribute (SourceAndTarget = CM, Source = 100%)."""
        if seg_def is not None:
            text_match = seg_def.get('text-match')
            if text_match:
                return text_match
        return ""
    
    def _is_locked(self, tu: ET.Element, seg_def: ET.Element) -> bool:
        """Check if segment is locked."""
        if seg_def is not None:
            locked = seg_def.get('locked')
            if locked and locked.lower() == 'true':
                return True
        
        # Check translate attribute on trans-unit
        translate = tu.get('translate')
        if translate and translate.lower() == 'no':
            return True
        
        return False


# ─── Module-level save helpers (used by both Standalone and Package handlers) ───

def _markers_to_xml(text: str) -> str:
    """
    Convert Supervertaler marker tags in text to SDLXLIFF XML elements.

    <N>content</N>  → <g id="N">content</g>
    <N/>            → <x id="N"/>

    Uses the XLIFF default namespace (no prefix needed since <g> and <x>
    live in the default xliff namespace in SDLXLIFF files).
    """
    if not text or not re.search(r'<[A-Za-z0-9_]+[>/]', text):
        return text

    _tid = _TAG_ID

    # Repeatedly resolve innermost paired tags until none remain
    prev = None
    result = text
    while prev != result:
        prev = result
        result = re.sub(
            rf'<({_tid})>(.*?)</\1>',
            r'<g id="\1">\2</g>',
            result,
            flags=re.DOTALL
        )

    # Convert standalone tags
    result = re.sub(rf'<({_tid})/>', r'<x id="\1"/>', result)

    return result


def _replace_target_content(content: str, xliff_file: SDLXLIFFFile,
                            segment_map: Dict[str, 'SDLSegment']) -> str:
    """
    Replace <mrk> content inside <target> elements with translated text.

    Strategy: find each <trans-unit>, locate its <target> block, then
    replace <mrk mtype="seg" mid="N"> content within it.
    """
    def _replace_tu_target(tu_match):
        tu_block = tu_match.group(0)
        tu_id_m = re.search(r'<trans-unit\s+[^>]*?id="([^"]+)"', tu_block)
        if not tu_id_m:
            return tu_block
        tu_id = tu_id_m.group(1)

        # Find <target>...</target> within this TU
        target_m = re.search(r'(<target[^>]*>)(.*?)(</target>)', tu_block, re.DOTALL)
        if not target_m:
            return tu_block

        target_open = target_m.group(1)
        target_inner = target_m.group(2)
        target_close = target_m.group(3)

        # Replace each <mrk mtype="seg" mid="N">...</mrk> in the target
        def _replace_mrk(mrk_match):
            mrk_open = mrk_match.group(1)  # <mrk mtype="seg" mid="N">
            mid = mrk_match.group(2)        # N
            mrk_close = '</mrk>'

            segment_id = f"{tu_id}_{mid}"
            segment = segment_map.get(segment_id)
            if segment and segment.target_text:
                new_content = _markers_to_xml(segment.target_text)
                return f'{mrk_open}{new_content}{mrk_close}'
            return mrk_match.group(0)

        new_target_inner = re.sub(
            r'(<mrk\s+mtype="seg"\s+mid="(\d+)"[^>]*>)(.*?)(</mrk>)',
            lambda m: _replace_mrk(m),
            target_inner,
            flags=re.DOTALL
        )

        new_target = f'{target_open}{new_target_inner}{target_close}'
        return tu_block[:target_m.start()] + new_target + tu_block[target_m.end():]

    # Process each trans-unit
    content = re.sub(
        r'<trans-unit\s[^>]*>.*?</trans-unit>',
        _replace_tu_target,
        content,
        flags=re.DOTALL
    )
    return content


def _replace_seg_attributes(content: str, xliff_file: SDLXLIFFFile,
                            segment_map: Dict[str, 'SDLSegment']) -> str:
    """
    Update conf and origin attributes on <sdl:seg> elements.

    For translated segments: set conf="Translated", origin="interactive",
    and remove stale TM/MT attributes (origin-system, percent, text-match).
    """
    def _replace_seg(seg_match):
        seg_text = seg_match.group(0)
        seg_id = seg_match.group(1)

        # Try to find this segment in any TU
        # seg IDs in sdl:seg-defs correspond to mrk mid values
        # We need to find which TU this belongs to by looking at context
        # But since we're doing global replacement, we check all possible TU+seg combos
        matching_segment = None
        for sid, seg in segment_map.items():
            if sid.endswith(f'_{seg_id}'):
                matching_segment = seg
                break

        if not matching_segment or not matching_segment.target_text:
            return seg_text

        if matching_segment.status in ('translated', 'approved', 'confirmed'):
            # Update conf
            seg_text = re.sub(r'conf="[^"]*"', 'conf="Translated"', seg_text)

            # Update origin to interactive
            if 'origin="' in seg_text:
                seg_text = re.sub(r'origin="[^"]*"', 'origin="interactive"', seg_text)
            else:
                seg_text = seg_text.replace('<sdl:seg ', '<sdl:seg origin="interactive" ', 1)

            # Remove stale TM/MT attributes
            seg_text = re.sub(r'\s+origin-system="[^"]*"', '', seg_text)
            seg_text = re.sub(r'\s+percent="[^"]*"', '', seg_text)
            seg_text = re.sub(r'\s+text-match="[^"]*"', '', seg_text)

        return seg_text

    content = re.sub(
        r'<sdl:seg\s+id="(\d+)"[^>]*(?:/>|>)',
        _replace_seg,
        content
    )
    return content


def _save_sdlxliff_file(xliff_file: SDLXLIFFFile, output_path: str,
                         log_callback=None) -> bool:
    """
    Save a single SDLXLIFF file using text-based replacement.

    Reads the original source file as raw bytes (preserving BOM),
    applies regex replacements for translated content and status
    attributes, then writes to output_path.

    Args:
        xliff_file: Parsed SDLXLIFF file with updated segments
        output_path: Path to write the output file
        log_callback: Optional logging function

    Returns:
        True if saved successfully
    """
    log = log_callback or (lambda msg: None)

    if not xliff_file.file_path:
        return False

    try:
        # Build segment map for quick lookup
        segment_map = {s.segment_id: s for s in xliff_file.segments}

        # Read the original file as raw bytes to preserve BOM
        source_path = Path(xliff_file.file_path)
        raw_bytes = source_path.read_bytes()

        # Detect and preserve BOM
        bom = b''
        if raw_bytes.startswith(b'\xef\xbb\xbf'):
            bom = b'\xef\xbb\xbf'
            raw_bytes = raw_bytes[3:]

        content = raw_bytes.decode('utf-8')

        # Apply text-based replacements
        content = _replace_target_content(content, xliff_file, segment_map)
        content = _replace_seg_attributes(content, xliff_file, segment_map)

        # Write to output path with original BOM
        out = Path(output_path)
        out.write_bytes(bom + content.encode('utf-8'))
        log(f"  Saved: {out.name}")
        return True
    except Exception as e:
        log(f"  Error saving {xliff_file.file_path}: {e}")
        return False


# ─── Standalone SDLXLIFF Handler ───────────────────────────────────────────────

class StandaloneSDLXLIFFHandler:
    """
    Handler for standalone .sdlxliff files (without a Trados package wrapper).

    Supports loading one or more .sdlxliff files, extracting segments,
    updating translations, and saving back with text-based replacement
    (preserving BOM, XML formatting, and namespaces).
    """

    def __init__(self, log_callback=None):
        self.log = log_callback or print
        self.parser = SDLXLIFFParser(log_callback)
        self.xliff_files: List[SDLXLIFFFile] = []
        self.source_paths: List[str] = []

    def load(self, file_paths: List[str]) -> bool:
        """
        Load one or more .sdlxliff files.

        Validates that all files share the same language pair.

        Returns:
            True if at least one file loaded successfully
        """
        self.xliff_files = []
        self.source_paths = []

        for file_path in file_paths:
            try:
                xliff_file = self.parser.parse_file(file_path)
                if xliff_file and xliff_file.segments:
                    self.xliff_files.append(xliff_file)
                    self.source_paths.append(file_path)
                    self.log(f"  Loaded: {Path(file_path).name} ({len(xliff_file.segments)} segments)")
                else:
                    self.log(f"  Warning: No segments found in {Path(file_path).name}")
            except Exception as e:
                self.log(f"  Error loading {Path(file_path).name}: {e}")
                traceback.print_exc()

        if not self.xliff_files:
            return False

        # Validate language consistency across files
        if len(self.xliff_files) > 1:
            ref_src = self.xliff_files[0].source_lang
            ref_tgt = self.xliff_files[0].target_lang
            for xf in self.xliff_files[1:]:
                if xf.source_lang != ref_src or xf.target_lang != ref_tgt:
                    self.log(f"  Warning: Language mismatch in {Path(xf.file_path).name} "
                             f"({xf.source_lang}→{xf.target_lang} vs {ref_src}→{ref_tgt})")

        total = sum(len(xf.segments) for xf in self.xliff_files)
        self.log(f"Loaded {len(self.xliff_files)} file(s), {total} segments total")
        return True

    def get_all_segments(self) -> List[SDLSegment]:
        """Get all segments from all loaded files as a flat list."""
        segments = []
        for xliff_file in self.xliff_files:
            segments.extend(xliff_file.segments)
        return segments

    def get_source_lang(self) -> str:
        """Return source language from first loaded file."""
        return self.xliff_files[0].source_lang if self.xliff_files else ''

    def get_target_lang(self) -> str:
        """Return target language from first loaded file."""
        return self.xliff_files[0].target_lang if self.xliff_files else ''

    def update_translations(self, translations: Dict[str, str]) -> int:
        """
        Batch update translations by segment_id → target_text.

        Returns:
            Number of segments updated
        """
        count = 0
        for xliff_file in self.xliff_files:
            for segment in xliff_file.segments:
                if segment.segment_id in translations:
                    segment.target_text = translations[segment.segment_id]
                    segment.status = 'translated'
                    count += 1
        return count

    def save_file(self, xliff_file: SDLXLIFFFile, output_path: str) -> bool:
        """Save a single SDLXLIFF file to the given path."""
        return _save_sdlxliff_file(xliff_file, output_path, self.log)

    def save_all(self, output_dir: str) -> List[str]:
        """
        Save all modified SDLXLIFF files to output_dir with '_translated' suffix.

        Returns:
            List of saved file paths
        """
        saved = []
        for xliff_file in self.xliff_files:
            stem = Path(xliff_file.file_path).stem
            ext = Path(xliff_file.file_path).suffix
            output_path = str(Path(output_dir) / f"{stem}_translated{ext}")
            if self.save_file(xliff_file, output_path):
                saved.append(output_path)
        return saved


# ─── Trados Package Handler ────────────────────────────────────────────────────

class TradosPackageHandler:
    """
    Handler for Trados Studio project packages (SDLPPX/SDLRPX).
    
    This class provides methods to:
    - Extract and parse SDLPPX packages
    - Import segments into Supervertaler projects
    - Update translations in SDLXLIFF files
    - Create return packages (SDLRPX)
    """
    
    def __init__(self, log_callback=None):
        self.log = log_callback or print
        self.parser = SDLXLIFFParser(log_callback)
        self.package: Optional[TradosPackage] = None
        self.extract_dir: Optional[str] = None
    
    def load_package(self, package_path: str, extract_dir: str = None) -> Optional[TradosPackage]:
        """
        Load and extract a Trados package.
        
        Args:
            package_path: Path to .sdlppx or .sdlrpx file
            extract_dir: Directory to extract to (temp if not specified)
            
        Returns:
            TradosPackage object with parsed content
        """
        try:
            package_path = Path(package_path)
            
            if not package_path.exists():
                self.log(f"ERROR: Package not found: {package_path}")
                return None
            
            # Determine package type
            ext = package_path.suffix.lower()
            if ext not in ['.sdlppx', '.sdlrpx']:
                self.log(f"ERROR: Not a Trados package: {ext}")
                return None
            
            package_type = 'sdlppx' if ext == '.sdlppx' else 'sdlrpx'
            
            # Create extraction directory
            if extract_dir:
                self.extract_dir = Path(extract_dir)
            else:
                self.extract_dir = Path(tempfile.mkdtemp(prefix='sdlppx_'))
            
            self.extract_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract the ZIP
            self.log(f"Extracting {package_path.name}...")
            with zipfile.ZipFile(package_path, 'r') as zf:
                zf.extractall(self.extract_dir)
            
            # Find and parse the project file
            project_file = None
            for f in self.extract_dir.glob('*.sdlproj'):
                project_file = f
                break
            
            if not project_file:
                self.log("ERROR: No .sdlproj file found in package")
                return None
            
            # Parse project file
            project_info = self._parse_project_file(project_file)
            
            # Create package object
            self.package = TradosPackage(
                package_path=str(package_path),
                package_type=package_type,
                project_name=project_info.get('name', package_path.stem),
                source_lang=project_info.get('source_lang', 'en'),
                target_lang=project_info.get('target_lang', ''),
                created_at=project_info.get('created_at', ''),
                created_by=project_info.get('created_by', ''),
                extract_dir=str(self.extract_dir)
            )
            
            # Find and parse SDLXLIFF files
            self._load_xliff_files()
            
            total_segments = sum(len(f.segments) for f in self.package.xliff_files)
            self.log(f"Loaded package: {self.package.project_name}")
            self.log(f"  Languages: {self.package.source_lang} → {self.package.target_lang}")
            self.log(f"  Files: {len(self.package.xliff_files)}")
            self.log(f"  Segments: {total_segments}")
            
            return self.package
            
        except Exception as e:
            self.log(f"ERROR loading package: {e}")
            traceback.print_exc()
            return None
    
    def _parse_project_file(self, project_file: Path) -> Dict:
        """Parse the .sdlproj XML file for project metadata."""
        info = {}
        
        try:
            tree = ET.parse(project_file)
            root = tree.getroot()
            
            # Project name (from filename or attribute)
            info['name'] = project_file.stem.split('-')[0] if '-' in project_file.stem else project_file.stem
            
            # Package metadata
            info['created_at'] = root.get('PackageCreatedAt', '')
            info['created_by'] = root.get('PackageCreatedBy', '')
            
            # Language directions
            lang_dir = root.find('.//LanguageDirection')
            if lang_dir is not None:
                info['source_lang'] = lang_dir.get('SourceLanguageCode', 'en')
                info['target_lang'] = lang_dir.get('TargetLanguageCode', '')
            
        except Exception as e:
            self.log(f"Warning: Could not parse project file: {e}")
        
        return info
    
    def _load_xliff_files(self):
        """Find and load SDLXLIFF files from the TARGET language folder only.
        
        Trados packages contain SDLXLIFF files in both source and target language
        folders. We only want to load from the target folder (e.g., nl-nl/) since
        that's where the translator works.
        """
        if not self.package or not self.extract_dir:
            return
        
        extract_path = Path(self.extract_dir)
        target_lang = self.package.target_lang.lower()
        
        # Look for SDLXLIFF files in the target language folder
        target_folder = extract_path / target_lang
        
        if target_folder.exists():
            # Load from target language folder
            self.log(f"Loading SDLXLIFF files from target folder: {target_lang}/")
            for xliff_path in target_folder.glob('*.sdlxliff'):
                xliff_file = self.parser.parse_file(str(xliff_path))
                if xliff_file:
                    self.package.xliff_files.append(xliff_file)
        else:
            # Fallback: try to find target folder by matching language code patterns
            # (e.g., nl-NL, nl-nl, nl_NL, etc.)
            self.log(f"Target folder '{target_lang}' not found, searching alternatives...")
            found = False
            for folder in extract_path.iterdir():
                if folder.is_dir():
                    folder_lower = folder.name.lower().replace('_', '-')
                    if folder_lower == target_lang or folder_lower.startswith(target_lang.split('-')[0]):
                        # Skip if this looks like the source language
                        source_lang = self.package.source_lang.lower()
                        if folder_lower == source_lang or folder_lower.startswith(source_lang.split('-')[0]):
                            continue
                        
                        self.log(f"Loading SDLXLIFF files from folder: {folder.name}/")
                        for xliff_path in folder.glob('*.sdlxliff'):
                            xliff_file = self.parser.parse_file(str(xliff_path))
                            if xliff_file:
                                self.package.xliff_files.append(xliff_file)
                        found = True
                        break
            
            if not found:
                self.log(f"Warning: Could not find target language folder for {target_lang}")
    
    def get_all_segments(self) -> List[SDLSegment]:
        """Get all segments from all files in the package."""
        if not self.package:
            return []
        
        segments = []
        for xliff_file in self.package.xliff_files:
            segments.extend(xliff_file.segments)
        
        return segments
    
    def update_segment(self, segment_id: str, target_text: str, status: str = 'translated') -> bool:
        """
        Update a segment's translation.
        
        Args:
            segment_id: The segment ID to update
            target_text: New target text
            status: New status (translated, approved, etc.)
            
        Returns:
            True if updated successfully
        """
        if not self.package:
            return False
        
        for xliff_file in self.package.xliff_files:
            for segment in xliff_file.segments:
                if segment.segment_id == segment_id:
                    segment.target_text = target_text
                    segment.status = status
                    return True
        
        return False
    
    def update_translations(self, translations: Dict[str, str]) -> int:
        """
        Batch update translations.
        
        Args:
            translations: Dict mapping segment_id to target_text
            
        Returns:
            Number of segments updated
        """
        count = 0
        for segment_id, target_text in translations.items():
            if self.update_segment(segment_id, target_text):
                count += 1
        return count
    
    def save_xliff_files(self) -> bool:
        """
        Save all modified SDLXLIFF files using text-based replacement.

        Instead of round-tripping through ElementTree.write() (which mangles
        BOM, XML declaration quotes, namespace prefixes, and whitespace), we
        read the original file as raw text and do targeted regex replacements
        for <target> content and sdl:seg attributes. This preserves the
        original file byte-for-byte except for the changed segments.

        Returns:
            True if all files saved successfully
        """
        if not self.package:
            return False

        self.log("Saving SDLXLIFF files...")

        for xliff_file in self.package.xliff_files:
            if not xliff_file.file_path:
                continue

            # Build segment map for quick lookup
            segment_map = {s.segment_id: s for s in xliff_file.segments}

            # Read the original file as raw bytes to preserve BOM
            file_path = Path(xliff_file.file_path)
            raw_bytes = file_path.read_bytes()

            # Detect and preserve BOM
            bom = b''
            if raw_bytes.startswith(b'\xef\xbb\xbf'):
                bom = b'\xef\xbb\xbf'
                raw_bytes = raw_bytes[3:]

            content = raw_bytes.decode('utf-8')

            # Apply text-based replacements
            content = self._replace_target_content(content, xliff_file, segment_map)
            content = self._replace_seg_attributes(content, xliff_file, segment_map)

            # Write back with original BOM
            file_path.write_bytes(bom + content.encode('utf-8'))
            self.log(f"  Saved: {file_path.name}")

        return True
    
    def _markers_to_xml(self, text: str) -> str:
        """Delegate to module-level function (backward compatibility)."""
        return _markers_to_xml(text)

    def _replace_target_content(self, content: str, xliff_file: SDLXLIFFFile,
                                segment_map: Dict[str, 'SDLSegment']) -> str:
        """Delegate to module-level function (backward compatibility)."""
        return _replace_target_content(content, xliff_file, segment_map)

    def _replace_seg_attributes(self, content: str, xliff_file: SDLXLIFFFile,
                                segment_map: Dict[str, 'SDLSegment']) -> str:
        """Delegate to module-level function (backward compatibility)."""
        return _replace_seg_attributes(content, xliff_file, segment_map)

    def _update_xliff_tree(self, xliff_file: SDLXLIFFFile):
        """Update the XML tree with segment translations."""
        # Build segment map for quick lookup
        segment_map = {s.segment_id: s for s in xliff_file.segments}
        
        root = xliff_file.root
        
        # Find all trans-units
        for tu in root.findall('.//xliff:trans-unit', NAMESPACES):
            tu_id = tu.get('id', '')
            
            # Get target element (create if missing)
            target_elem = tu.find('xliff:target', NAMESPACES)
            if target_elem is None:
                target_elem = tu.find('target')
            
            # Check for segmented content
            seg_source = tu.find('xliff:seg-source', NAMESPACES)
            if seg_source is None:
                seg_source = tu.find('seg-source')
            
            if seg_source is not None:
                # Update segmented content
                self._update_segmented_target(tu, target_elem, segment_map)
            else:
                # Single segment
                segment = segment_map.get(tu_id)
                if segment and target_elem is not None:
                    # Update target text
                    self._set_element_text(target_elem, segment.target_text)
            
            # Update segment confirmation status in sdl:seg-defs
            self._update_segment_status(tu, segment_map, tu_id)
    
    def _update_segmented_target(self, tu: ET.Element, target_elem: ET.Element, 
                                  segment_map: Dict[str, SDLSegment]):
        """Update segmented target content with translations."""
        if target_elem is None:
            return
        
        tu_id = tu.get('id', '')
        
        # Find all target mrk elements
        target_mrks = target_elem.findall('.//xliff:mrk[@mtype="seg"]', NAMESPACES)
        if not target_mrks:
            target_mrks = target_elem.findall('.//mrk[@mtype="seg"]')
        
        for mrk in target_mrks:
            mid = mrk.get('mid')
            if mid:
                segment_id = f"{tu_id}_{mid}"
                segment = segment_map.get(segment_id)
                if segment:
                    # Update the mrk element text
                    self._set_element_text(mrk, segment.target_text)
    
    def _update_segment_status(self, tu: ET.Element, segment_map: Dict[str, SDLSegment], tu_id: str):
        """
        Update segment confirmation status in sdl:seg-defs.
        
        Changes the conf attribute from 'Draft' to 'Translated' for segments
        that have been translated in Supervertaler.
        """
        # Status mapping from internal to SDL format
        status_to_conf = {
            'translated': 'Translated',
            'approved': 'ApprovedTranslation',
            'confirmed': 'ApprovedTranslation',
            'draft': 'Draft',
            'not_translated': 'Draft',
        }
        
        # Find sdl:seg-defs within this trans-unit (try with namespace first)
        seg_defs = tu.find('.//sdl:seg-defs', {'sdl': NAMESPACES['sdl']})
        if seg_defs is None:
            seg_defs = tu.find('.//{%s}seg-defs' % NAMESPACES['sdl'])
        if seg_defs is None:
            # Try without namespace
            for child in tu:
                if child.tag.endswith('seg-defs'):
                    seg_defs = child
                    break
        
        if seg_defs is None:
            return
        
        # Update each seg element
        for seg_elem in seg_defs:
            if not seg_elem.tag.endswith('seg'):
                continue
                
            seg_id = seg_elem.get('id', '')
            
            # Build segment_id to look up in our map
            # For segmented content: tu_id_seg_id
            # For single segment: tu_id
            segment = segment_map.get(f"{tu_id}_{seg_id}")
            if not segment:
                segment = segment_map.get(tu_id)
            
            if segment:
                # Get the new conf value based on segment status
                new_conf = status_to_conf.get(segment.status, 'Translated')
                
                # If segment has target text and is translated/approved, set to Translated
                if segment.target_text and segment.status in ('translated', 'approved', 'confirmed'):
                    new_conf = 'Translated'

                # Update the conf attribute
                current_conf = seg_elem.get('conf', '')
                if current_conf != new_conf:
                    seg_elem.set('conf', new_conf)

                # Update origin to 'interactive' for translated segments
                # (translator takes responsibility for the content)
                if new_conf in ('Translated', 'ApprovedTranslation') and segment.target_text:
                    seg_elem.set('origin', 'interactive')
                    # Remove stale TM/MT match attributes
                    for attr in ('origin-system', 'percent', 'text-match'):
                        if attr in seg_elem.attrib:
                            del seg_elem.attrib[attr]

    def _set_element_text(self, elem: ET.Element, text: str):
        """
        Set element text, converting Supervertaler marker tags back to SDLXLIFF
        XML elements.

        Marker format (from import):
          <N>content</N>  → <g id="N">content</g>  (paired formatting tag)
          <N/>            → <x id="N"/>             (standalone tag)
        """
        # Clear existing children (we rebuild from marker text)
        for child in list(elem):
            elem.remove(child)
        elem.text = None

        if not text:
            elem.text = ''
            return

        # Check if text contains any marker tags at all (fast path)
        if not re.search(r'<[A-Za-z0-9_]+[>/]', text):
            elem.text = text
            return

        # Resolve paired tags from innermost outward by repeatedly
        # replacing the innermost match until none remain
        self._build_element_content(elem, text)

    def _build_element_content(self, parent: ET.Element, text: str):
        """
        Parse marker text and build mixed XML content on parent element.

        Handles nested paired tags by resolving innermost first.
        E.g. "before <14>177</14>Lu after" becomes:
          parent.text = "before "
          <g id="14"> with text "177" and tail "Lu after"
        """
        g_tag = f'{{{XLIFF_NS}}}g'
        x_tag = f'{{{XLIFF_NS}}}x'

        # Tokenize: split text into plain-text and tag tokens
        # Pattern matches: <ID>  </ID>  <ID/>  (numeric or alphanumeric IDs)
        _tid = _TAG_ID
        token_re = re.compile(rf'(<{_tid}>|</{_tid}>|<{_tid}/>)')
        tokens = token_re.split(text)

        # Build a tree using a stack approach
        # Each stack frame is (element, tag_id or None for root)
        stack = [(parent, None)]

        for token in tokens:
            if not token:
                continue

            # Opening paired tag: <ID>
            m_open = re.fullmatch(rf'<({_tid})>', token)
            if m_open:
                tag_id = m_open.group(1)
                g_elem = ET.SubElement(stack[-1][0], g_tag)
                g_elem.set('id', tag_id)
                stack.append((g_elem, tag_id))
                continue

            # Closing paired tag: </ID>
            m_close = re.fullmatch(rf'</({_tid})>', token)
            if m_close:
                tag_id = m_close.group(1)
                # Pop matching frame (or ignore if mismatched)
                if len(stack) > 1 and stack[-1][1] == tag_id:
                    stack.pop()
                continue

            # Standalone tag: <ID/>
            m_standalone = re.fullmatch(rf'<({_tid})/>',  token)
            if m_standalone:
                tag_id = m_standalone.group(1)
                x_elem = ET.SubElement(stack[-1][0], x_tag)
                x_elem.set('id', tag_id)
                continue

            # Plain text — append to the current element
            current_elem = stack[-1][0]
            children = list(current_elem)
            if children:
                # Append as tail of the last child
                last_child = children[-1]
                last_child.tail = (last_child.tail or '') + token
            else:
                # Append to element's own text
                current_elem.text = (current_elem.text or '') + token

    def create_return_package(self, output_path: str = None) -> Optional[str]:
        """
        Create a return package (SDLRPX) with translations.

        Args:
            output_path: Path for the return package (auto-generated if not specified)

        Returns:
            Path to the created package
        """
        if not self.package or not self.extract_dir:
            self.log("ERROR: No package loaded")
            return None

        try:
            # Save all XLIFF files first
            self.save_xliff_files()

            # Update .sdlproj for return package
            self._update_project_file_for_return()

            # Generate output path if not specified
            if not output_path:
                original = Path(self.package.package_path)
                output_path = original.parent / f"{original.stem}_translated.sdlrpx"

            output_path = Path(output_path)
            target_lang = self.package.target_lang.lower()
            source_lang = self.package.source_lang.lower()

            # Create the return package (ZIP)
            # Include: .sdlproj + source lang SDLXLIFF (unchanged) + target lang SDLXLIFF
            # Exclude: Reports/, File Types/, and other non-essential files
            self.log(f"Creating return package: {output_path.name}")

            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                extract_path = Path(self.extract_dir)
                for file_path in extract_path.rglob('*'):
                    if not file_path.is_file():
                        continue
                    rel_path = file_path.relative_to(extract_path)
                    parts = rel_path.parts

                    # Include .sdlproj files at root level
                    if len(parts) == 1 and file_path.suffix.lower() == '.sdlproj':
                        zf.write(file_path, rel_path)
                        continue

                    # Include files in source language folder (unchanged)
                    if parts and parts[0].lower() == source_lang:
                        zf.write(file_path, rel_path)
                        continue

                    # Include files in target language folder
                    if parts and parts[0].lower() == target_lang:
                        zf.write(file_path, rel_path)
                        continue

                    # Skip everything else (Reports/, File Types/, etc.)

            self.log(f"Created return package: {output_path}")
            return str(output_path)

        except Exception as e:
            self.log(f"ERROR creating return package: {e}")
            traceback.print_exc()
            return None

    def _update_project_file_for_return(self):
        """
        Modify the .sdlproj XML for a return package.

        Uses regex-based string replacement to preserve exact XML formatting
        while changing key attributes that Trados Studio expects in a return package.
        """
        proj_files = list(Path(self.extract_dir).glob('*.sdlproj'))
        if not proj_files:
            self.log("Warning: No .sdlproj found to update")
            return

        proj_path = proj_files[0]
        try:
            content = proj_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = proj_path.read_text(encoding='utf-8-sig')

        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.0000000Z')
        username = os.environ.get('USERNAME', os.environ.get('USER', 'Supervertaler'))

        # 1. PackageType → ReturnPackage
        content = content.replace(
            'PackageType="ProjectPackage"',
            'PackageType="ReturnPackage"'
        )

        # 2. Update PackageCreatedAt timestamp
        content = re.sub(
            r'PackageCreatedAt="[^"]*"',
            f'PackageCreatedAt="{now}"',
            content
        )

        # 3. Update PackageCreatedBy only (not other CreatedBy attributes!)
        content = re.sub(
            r'PackageCreatedBy="[^"]*"',
            f'PackageCreatedBy="{username}"',
            content
        )

        # 4. ConfirmationStatistics: move Draft counts to Translated
        def _swap_draft_to_translated(match):
            block = match.group(0)
            draft_m = re.search(r'<Draft\s+([^/]*)/>', block)
            translated_m = re.search(r'<Translated\s+([^/]*)/>', block)
            if draft_m and translated_m:
                draft_attrs = draft_m.group(1).strip()
                block = re.sub(
                    r'<Draft\s+[^/]*/>',
                    '<Draft Words="0" Characters="0" Segments="0" Placeables="0" Tags="0" />',
                    block
                )
                block = re.sub(
                    r'<Translated\s+[^/]*/>',
                    f'<Translated {draft_attrs}/>',
                    block
                )
            return block

        content = re.sub(
            r'<ConfirmationStatistics[^>]*>.*?</ConfirmationStatistics>',
            _swap_draft_to_translated,
            content,
            flags=re.DOTALL
        )

        # 5. ManualTask: mark as completed
        def _complete_manual_task(match):
            block = match.group(0)
            block = re.sub(r'PercentComplete="\d+"', 'PercentComplete="100"', block)
            block = re.sub(r'Status="[^"]*"', 'Status="Completed"', block)
            # Add CompletedAt if not present
            if 'CompletedAt=' not in block:
                block = re.sub(
                    r'(<ManualTask\s[^>]*?)(>)',
                    rf'\1 CompletedAt="{now}"\2',
                    block
                )
            # Mark TaskFile(s) as completed
            block = block.replace('Completed="false"', 'Completed="true"')
            return block

        content = re.sub(
            r'<ManualTask\s.*?</ManualTask>',
            _complete_manual_task,
            content,
            flags=re.DOTALL
        )

        # 6. Remove AutomaticTask sections (not needed in return package)
        content = re.sub(
            r'\s*<AutomaticTask\s.*?</AutomaticTask>',
            '',
            content,
            flags=re.DOTALL
        )

        # 7. Remove TermbaseConfiguration section (not needed in return package)
        content = re.sub(
            r'\s*<TermbaseConfiguration[^>]*>.*?</TermbaseConfiguration>',
            '',
            content,
            flags=re.DOTALL
        )

        proj_path.write_text(content, encoding='utf-8')
        self.log(f"  Updated .sdlproj: PackageType=ReturnPackage, CreatedBy={username}")
    
    def cleanup(self):
        """Clean up extracted files."""
        if self.extract_dir and Path(self.extract_dir).exists():
            try:
                shutil.rmtree(self.extract_dir)
                self.log("Cleaned up extracted files")
            except Exception as e:
                self.log(f"Warning: Could not clean up: {e}")


def detect_trados_package_type(file_path: str) -> Optional[str]:
    """
    Detect if a file is a Trados package and return its type.
    
    Returns:
        'sdlppx', 'sdlrpx', or None if not a Trados package
    """
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext == '.sdlppx':
        return 'sdlppx'
    elif ext == '.sdlrpx':
        return 'sdlrpx'
    
    # Check if it's a ZIP with SDLXLIFF files
    if ext == '.zip':
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                names = zf.namelist()
                if any(n.endswith('.sdlxliff') for n in names):
                    if any(n.endswith('.sdlproj') for n in names):
                        return 'sdlppx'  # Assume project package
        except:
            pass
    
    return None
