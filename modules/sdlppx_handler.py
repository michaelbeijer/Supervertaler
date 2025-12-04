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
        Save all modified SDLXLIFF files.
        
        Returns:
            True if all files saved successfully
        """
        if not self.package:
            return False
        
        # TODO: Implement proper XLIFF modification
        # This requires updating the XML tree with new translations
        # while preserving all SDL-specific attributes
        
        self.log("Saving SDLXLIFF files...")
        
        for xliff_file in self.package.xliff_files:
            if xliff_file.tree and xliff_file.root:
                # Update segments in the XML tree
                self._update_xliff_tree(xliff_file)
                
                # Save the file
                xliff_file.tree.write(
                    xliff_file.file_path,
                    encoding='utf-8',
                    xml_declaration=True
                )
                self.log(f"  Saved: {Path(xliff_file.file_path).name}")
        
        return True
    
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
    
    def _set_element_text(self, elem: ET.Element, text: str):
        """Set element text, handling tags appropriately."""
        # For now, just set the text
        # TODO: Convert Supervertaler tags back to XLIFF format
        elem.text = text
        # Clear child elements (simple approach)
        for child in list(elem):
            if child.tag.endswith('mrk') and child.get('mtype') != 'seg':
                # Keep non-segment markers
                pass
            else:
                elem.remove(child)
    
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
            
            # Generate output path if not specified
            if not output_path:
                original = Path(self.package.package_path)
                output_path = original.parent / f"{original.stem}_translated.sdlrpx"
            
            output_path = Path(output_path)
            
            # Create the return package (ZIP)
            self.log(f"Creating return package: {output_path.name}")
            
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Add all files from extracted directory
                extract_path = Path(self.extract_dir)
                for file_path in extract_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(extract_path)
                        zf.write(file_path, arcname)
            
            self.log(f"Created return package: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.log(f"ERROR creating return package: {e}")
            traceback.print_exc()
            return None
    
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
