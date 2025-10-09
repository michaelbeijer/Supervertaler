"""
MQXLIFF Handler Module
======================
Handles import/export of memoQ XLIFF (.mqxliff) files with proper formatting preservation.

MQXLIFF is an XLIFF 1.2 format with memoQ-specific extensions for CAT tool metadata
and formatting tags. This module provides robust parsing and generation of MQXLIFF files
while preserving inline formatting (bold, italic, underline) and complex structures like
hyperlinks.

Key Features:
- Parse XLIFF trans-units with source and target segments
- Extract and preserve inline formatting tags (bpt/ept pairs)
- Handle complex nested structures (hyperlinks with formatting)
- Generate valid MQXLIFF output with proper tag structure
- Maintain segment IDs and memoQ metadata

Formatting Tag Structure:
- <bpt id="X" ctype="bold">{}</bpt>...<ept id="X">{}</ept> - Bold text
- <bpt id="X" ctype="italic">{}</bpt>...<ept id="X">{}</ept> - Italic text
- <bpt id="X" ctype="underlined">{}</bpt>...<ept id="X">{}</ept> - Underlined text
- Nested tags for hyperlinks: <bpt><bpt><bpt>text</ept></ept></ept>
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple, Optional
import re


class FormattedSegment:
    """Represents a segment with inline formatting information."""
    
    def __init__(self, segment_id: str, plain_text: str, formatted_xml: str):
        """
        Initialize a formatted segment.
        
        Args:
            segment_id: Unique identifier for the segment (trans-unit id)
            plain_text: Plain text without any formatting tags
            formatted_xml: XML string with formatting tags preserved
        """
        self.id = segment_id
        self.plain_text = plain_text
        self.formatted_xml = formatted_xml
        self.formatting_tags = self._extract_formatting_tags(formatted_xml)
    
    def _extract_formatting_tags(self, xml_str: str) -> List[Dict]:
        """Extract formatting tag information from XML string."""
        tags = []
        # Match bpt tags with ctype attribute
        bpt_pattern = r'<bpt\s+id="(\d+)"\s+(?:rid="(\d+)"\s+)?ctype="([^"]+)">[^<]*</bpt>'
        for match in re.finditer(bpt_pattern, xml_str):
            tag_id = match.group(1)
            ctype = match.group(3)
            tags.append({
                'id': tag_id,
                'type': ctype,
                'is_bpt': True
            })
        return tags
    
    def __repr__(self):
        return f"FormattedSegment(id={self.id}, text='{self.plain_text[:50]}...', tags={len(self.formatting_tags)})"


class MQXLIFFHandler:
    """Handler for parsing and generating memoQ XLIFF files."""
    
    # Namespaces used in MQXLIFF files
    NAMESPACES = {
        'xliff': 'urn:oasis:names:tc:xliff:document:1.2',
        'mq': 'MQXliff'
    }
    
    def __init__(self):
        """Initialize the MQXLIFF handler."""
        self.tree = None
        self.root = None
        self.file_element = None
        self.body_element = None
        self.source_lang = None
        self.target_lang = None
        
    def load(self, file_path: str) -> bool:
        """
        Load and parse an MQXLIFF file.
        
        Args:
            file_path: Path to the .mqxliff file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            # Register namespaces for proper parsing
            for prefix, uri in self.NAMESPACES.items():
                ET.register_namespace(prefix, uri)
            
            self.tree = ET.parse(file_path)
            self.root = self.tree.getroot()
            
            # Find the file element
            self.file_element = self.root.find('.//xliff:file', self.NAMESPACES)
            if self.file_element is None:
                # Try without namespace
                self.file_element = self.root.find('.//file')
            
            if self.file_element is not None:
                self.source_lang = self.file_element.get('source-language', 'unknown')
                self.target_lang = self.file_element.get('target-language', 'unknown')
            
            # Find the body element
            self.body_element = self.root.find('.//xliff:body', self.NAMESPACES)
            if self.body_element is None:
                # Try without namespace
                self.body_element = self.root.find('.//body')
            
            return True
        except Exception as e:
            print(f"[MQXLIFF] Error loading file: {e}")
            return False
    
    def extract_source_segments(self) -> List[FormattedSegment]:
        """
        Extract all source segments from the MQXLIFF file.
        
        Returns:
            List of FormattedSegment objects containing source text and formatting
        """
        segments = []
        
        if self.body_element is None:
            return segments
        
        # Find all trans-unit elements (with or without namespace)
        trans_units = self.body_element.findall('.//xliff:trans-unit', self.NAMESPACES)
        if not trans_units:
            trans_units = self.body_element.findall('.//trans-unit')
        
        for trans_unit in trans_units:
            trans_unit_id = trans_unit.get('id', 'unknown')
            
            # Skip auxiliary segments (like hyperlink URLs with mq:nosplitjoin="true")
            nosplitjoin = trans_unit.get('{MQXliff}nosplitjoin', 'false')
            if nosplitjoin == 'true':
                continue
            
            # Find source element
            source_elem = trans_unit.find('xliff:source', self.NAMESPACES)
            if source_elem is None:
                source_elem = trans_unit.find('source')
            
            if source_elem is not None:
                # Get the XML string of the source element's content
                formatted_xml = ET.tostring(source_elem, encoding='unicode', method='xml')
                
                # Extract plain text (removing all tags)
                plain_text = self._extract_plain_text(source_elem)
                
                segment = FormattedSegment(trans_unit_id, plain_text, formatted_xml)
                segments.append(segment)
        
        return segments
    
    def _extract_plain_text(self, element: ET.Element) -> str:
        """
        Recursively extract plain text from an XML element, stripping all tags.
        
        Args:
            element: The XML element to extract text from
            
        Returns:
            Plain text string with all tags removed (including {} placeholders)
        """
        text_parts = []
        
        # Add the element's text
        if element.text:
            text_parts.append(element.text)
        
        # Recursively process child elements
        for child in element:
            text_parts.append(self._extract_plain_text(child))
            # Add the tail text (text after the child element's closing tag)
            if child.tail:
                text_parts.append(child.tail)
        
        full_text = ''.join(text_parts)
        
        # Remove {} placeholders that come from bpt/ept tags
        # These are used in MQXLIFF to mark tag positions
        full_text = full_text.replace('{}', '')
        
        return full_text
    
    def update_target_segments(self, translations: List[str]) -> int:
        """
        Update target segments in the MQXLIFF with translations.
        
        This method attempts to preserve formatting from the source segment by:
        1. Copying the source formatting structure
        2. Replacing the text content with the translation
        3. Adjusting tag IDs to avoid conflicts
        
        Args:
            translations: List of translated strings (plain text)
            
        Returns:
            Number of segments updated
        """
        if self.body_element is None:
            return 0
        
        # Find all trans-unit elements
        trans_units = self.body_element.findall('.//xliff:trans-unit', self.NAMESPACES)
        if not trans_units:
            trans_units = self.body_element.findall('.//trans-unit')
        
        translation_idx = 0
        segments_updated = 0
        
        for trans_unit in trans_units:
            # Skip auxiliary segments
            nosplitjoin = trans_unit.get('{MQXliff}nosplitjoin', 'false')
            if nosplitjoin == 'true':
                continue
            
            if translation_idx >= len(translations):
                break
            
            translation = translations[translation_idx]
            translation_idx += 1
            
            # Find source and target elements
            source_elem = trans_unit.find('xliff:source', self.NAMESPACES)
            if source_elem is None:
                source_elem = trans_unit.find('source')
            
            target_elem = trans_unit.find('xliff:target', self.NAMESPACES)
            if target_elem is None:
                target_elem = trans_unit.find('target')
            
            if source_elem is not None and target_elem is not None:
                # Copy formatting from source to target
                self._copy_formatting_to_target(source_elem, target_elem, translation)
                segments_updated += 1
                
                # Update segment status to Confirmed
                trans_unit.set('{MQXliff}status', 'Confirmed')
        
        return segments_updated
    
    def _copy_formatting_to_target(self, source_elem: ET.Element, target_elem: ET.Element, translation: str):
        """
        Copy formatting structure from source to target and insert translation text.
        
        Strategy:
        1. If source has no formatting tags, just set plain text
        2. If source has formatting, clone the structure and try to map text
        3. For complex cases, preserve tag structure but use translation text
        
        Args:
            source_elem: Source XML element with formatting
            target_elem: Target XML element to populate
            translation: Translated text (plain)
        """
        # Clear existing target content but preserve attributes
        target_attribs = target_elem.attrib.copy()
        target_elem.clear()
        target_elem.tag = 'target'  # Ensure it's a target element
        
        # Restore important attributes
        for key in ['{http://www.w3.org/XML/1998/namespace}space', 'mq:segpart']:
            if key in target_attribs:
                target_elem.set(key, target_attribs[key])
        
        # Preserve xml:space="preserve" if source has it
        space_attr = source_elem.get('{http://www.w3.org/XML/1998/namespace}space')
        if space_attr:
            target_elem.set('{http://www.w3.org/XML/1998/namespace}space', space_attr)
        
        # Check if source has formatting tags (child elements)
        has_formatting = len(list(source_elem)) > 0
        
        if not has_formatting:
            # Simple case: no formatting tags, just set text
            target_elem.text = translation
        else:
            # Complex case: has formatting tags
            # Strategy: Clone the structure and replace text content
            self._clone_with_translation(source_elem, target_elem, translation)
    
    def _clone_with_translation(self, source_elem: ET.Element, target_elem: ET.Element, translation: str):
        """
        Clone source element structure to target, replacing text with translation.
        
        Strategy: Clone the entire structure, then intelligently place translation text.
        
        Args:
            source_elem: Source element to clone from
            target_elem: Target element to populate
            translation: Translation text to insert
        """
        # Extract source text for comparison
        source_text = self._extract_plain_text(source_elem)
        
        # Clone all child elements (formatting tags) to preserve structure
        # Also copy the text that appears before the first child
        target_elem.text = source_elem.text
        
        for child in source_elem:
            cloned_child = self._deep_clone_element(child)
            target_elem.append(cloned_child)
        
        # Now replace the text content with the translation
        # For complex nested structures, we need to be very careful about where we place text
        # to avoid breaking the XML structure
        
        # If source and translation are identical, structure is already correct
        if source_text.strip() == translation.strip():
            return
        
        # Try to place the translation intelligently
        self._place_translation_carefully(target_elem, source_text, translation)
    
    def _deep_clone_element(self, element: ET.Element) -> ET.Element:
        """Deep clone an XML element with all its children."""
        cloned = ET.Element(element.tag, element.attrib)
        cloned.text = element.text
        cloned.tail = element.tail
        
        for child in element:
            cloned.append(self._deep_clone_element(child))
        
        return cloned
    
    def _place_translation_carefully(self, element: ET.Element, source_text: str, translation: str):
        """
        Carefully place translation text in the element structure.
        
        This is conservative: it only modifies text nodes that contain actual content words,
        not formatting codes. For complex cases, it may preserve more source text structure
        than ideal, but it won't break the XML.
        
        Args:
            element: The target element to modify
            source_text: Original source text
            translation: Translation to place
        """
        # Strategy: Find text nodes that contain actual words (not just "{}" or encoded tags)
        # and replace them with corresponding parts of the translation
        
        # For now, use a simple heuristic:
        # If there's text in element.text, replace it
        # If there's text in a child's tail (after a tag), replace it
        # But DON'T touch text inside <bpt>/<ept> tags (that's formatting metadata)
        
        # Collect all "real content" text nodes
        real_content_nodes = []
        
        if element.text and len(element.text.strip()) > 0:
            # Check if it's not just whitespace or formatting codes
            if not self._is_formatting_code(element.text):
                real_content_nodes.append(('root_text', element.text))
        
        # Check child tails (text after tags)
        for i, child in enumerate(element):
            if child.tail and len(child.tail.strip()) > 0:
                if not self._is_formatting_code(child.tail):
                    real_content_nodes.append(('child_tail', i, child.tail))
        
        # If we found content nodes, use simple replacement strategy
        if real_content_nodes:
            # Simple approach: Just try string replacement in each node
            # This works for simple cases and won't break complex structures
            for node_info in real_content_nodes:
                if node_info[0] == 'root_text':
                    # Try to replace source words with translation words
                    if element.text:
                        element.text = element.text.replace(source_text.strip(), translation.strip())
                elif node_info[0] == 'child_tail':
                    idx = node_info[1]
                    if element[idx].tail:
                        element[idx].tail = element[idx].tail.replace(source_text.strip(), translation.strip())
        else:
            # No obvious content nodes, check if text is inside nested structure
            # For these complex cases, just place translation where the source text was found
            self._recursive_text_replace(element, source_text, translation)
    
    def _recursive_text_replace(self, element: ET.Element, old_text: str, new_text: str):
        """
        Recursively search for old_text and replace with new_text.
        Only replaces in text nodes, not in tag attributes or structure.
        """
        if element.text and old_text.strip() in element.text:
            element.text = element.text.replace(old_text.strip(), new_text.strip())
        
        for child in element:
            if child.tail and old_text.strip() in child.tail:
                child.tail = child.tail.replace(old_text.strip(), new_text.strip())
            # Recurse into children
            self._recursive_text_replace(child, old_text, new_text)
    
    def _replace_all_text_content(self, element: ET.Element, old_text: str, new_text: str):
        """
        Replace text content in an element tree, handling text split across nodes.
        
        The challenge: Source text like "Hello world" might be split as:
        - element.text = "Hello "
        - child[0].text = "world"
        
        We need to collect all content text, replace it with the translation,
        then put it back in the structure.
        
        Args:
            element: The element to process
            old_text: The original source text (plain, no tags)
            new_text: The translation text to insert
        """
        # Clean both texts for comparison
        old_clean = old_text.strip()
        new_clean = new_text.strip()
        
        # If texts are identical, no replacement needed
        if old_clean == new_clean:
            return
        
        # Find all content text nodes (excluding <bpt>/<ept> formatting codes)
        content_nodes = []
        
        # Check element.text (text before first child)
        if element.text and not self._is_formatting_code(element.text):
            content_nodes.append(('root', None, element.text))
        
        # Check all children
        for i, child in enumerate(element):
            # For <bpt> and <ept> tags, their .text contains formatting codes like "{}" or "&lt;hlnk...&gt;"
            # We should NOT treat this as content
            if child.tag not in ['bpt', 'ept']:
                if child.text and not self._is_formatting_code(child.text):
                    content_nodes.append(('child_text', i, child.text))
            
            # child.tail is text AFTER the child tag, this is content
            if child.tail and not self._is_formatting_code(child.tail):
                content_nodes.append(('child_tail', i, child.tail))
        
        # If no content nodes, nothing to replace
        if not content_nodes:
            return
        
        # Strategy: Place entire translation in the first content node, clear others
        first_node = content_nodes[0]
        node_type, node_index, node_text = first_node
        
        if node_type == 'root':
            element.text = new_clean
        elif node_type == 'child_text':
            element[node_index].text = new_clean
        elif node_type == 'child_tail':
            element[node_index].tail = new_clean
        
        # Clear all other content nodes
        for node in content_nodes[1:]:
            node_type, node_index, node_text = node
            if node_type == 'root':
                element.text = ""
            elif node_type == 'child_text':
                element[node_index].text = ""
            elif node_type == 'child_tail':
                element[node_index].tail = ""

    
    def _is_formatting_code(self, text: str) -> bool:
        """
        Check if text is a formatting code rather than actual content.
        Formatting codes include: "{}", "&lt;...&gt;", whitespace-only
        """
        if not text:
            return True
        
        text_stripped = text.strip()
        if not text_stripped:
            return True  # Whitespace only
        
        # Check for common formatting placeholders
        if text_stripped == "{}":
            return True
        
        # Check for encoded XML tags (formatting metadata)
        if text_stripped.startswith("&lt;") and text_stripped.endswith("&gt;"):
            return True
        
        return False

    
    def save(self, output_path: str) -> bool:
        """
        Save the modified MQXLIFF file with proper namespace handling.
        
        Args:
            output_path: Path where to save the file
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            if self.tree is None:
                return False
            
            # Register namespaces to avoid namespace prefix issues
            # This ensures the default namespace is used correctly
            ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')
            ET.register_namespace('mq', 'MQXliff')
            ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
            
            # Write with XML declaration and UTF-8 encoding
            self.tree.write(output_path, encoding='utf-8', xml_declaration=True, method='xml')
            
            # Post-process to fix namespace issues that ElementTree might create
            # Read the file and ensure proper structure
            self._fix_namespace_prefixes(output_path)
            
            return True
        except Exception as e:
            print(f"[MQXLIFF] Error saving file: {e}")
            return False
    
    def _fix_namespace_prefixes(self, file_path: str):
        """
        Fix namespace prefix issues in the saved file.
        ElementTree sometimes adds unwanted prefixes. This method ensures
        the file matches the expected MQXLIFF format.
        
        Args:
            file_path: Path to the file to fix
        """
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix common ElementTree namespace issues
            # Replace xliff:xliff with xliff (default namespace)
            content = content.replace('<xliff:xliff ', '<xliff ')
            content = content.replace('</xliff:xliff>', '</xliff>')
            content = content.replace('xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2"',
                                    'xmlns="urn:oasis:names:tc:xliff:document:1.2"')
            
            # Remove xliff: prefixes from standard XLIFF elements
            # but keep mq: prefixes for memoQ extensions
            for tag in ['file', 'header', 'tool', 'body', 'trans-unit', 'source', 'target', 
                       'context-group', 'context', 'bpt', 'ept', 'ph', 'it', 'x']:
                content = content.replace(f'<xliff:{tag} ', f'<{tag} ')
                content = content.replace(f'<xliff:{tag}>', f'<{tag}>')
                content = content.replace(f'</xliff:{tag}>', f'</{tag}>')
            
            # Write back the corrected content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            print(f"[MQXLIFF] Warning: Could not fix namespace prefixes: {e}")
            # Non-fatal - file might still work
    
    def get_segment_count(self) -> int:
        """Get the number of translatable segments (excluding auxiliary segments)."""
        if self.body_element is None:
            return 0
        
        trans_units = self.body_element.findall('.//xliff:trans-unit', self.NAMESPACES)
        if not trans_units:
            trans_units = self.body_element.findall('.//trans-unit')
        
        count = 0
        for trans_unit in trans_units:
            nosplitjoin = trans_unit.get('{MQXliff}nosplitjoin', 'false')
            if nosplitjoin != 'true':
                count += 1
        
        return count


def test_mqxliff_handler():
    """Test function to verify MQXLIFF handler functionality."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python mqxliff_handler.py <path_to_mqxliff_file>")
        return
    
    file_path = sys.argv[1]
    
    print(f"Testing MQXLIFF Handler with: {file_path}")
    print("=" * 60)
    
    handler = MQXLIFFHandler()
    
    # Load file
    if not handler.load(file_path):
        print("Failed to load file!")
        return
    
    print(f"✓ File loaded successfully")
    print(f"  Source language: {handler.source_lang}")
    print(f"  Target language: {handler.target_lang}")
    print(f"  Segment count: {handler.get_segment_count()}")
    print()
    
    # Extract segments
    segments = handler.extract_source_segments()
    print(f"✓ Extracted {len(segments)} segments")
    print()
    
    # Display first 5 segments
    print("First 5 segments:")
    for i, seg in enumerate(segments[:5], 1):
        print(f"\n  Segment {i} (ID: {seg.id}):")
        print(f"    Plain text: {seg.plain_text}")
        if seg.formatting_tags:
            print(f"    Formatting: {seg.formatting_tags}")
    
    # Test update (with dummy translations)
    print("\n" + "=" * 60)
    print("Testing update with dummy translations...")
    dummy_translations = [f"TRANSLATED: {seg.plain_text}" for seg in segments]
    updated_count = handler.update_target_segments(dummy_translations)
    print(f"✓ Updated {updated_count} target segments")
    
    # Save test output
    output_path = file_path.replace('.mqxliff', '_test_output.mqxliff')
    if handler.save(output_path):
        print(f"✓ Saved test output to: {output_path}")
    else:
        print("✗ Failed to save output")


if __name__ == "__main__":
    test_mqxliff_handler()
