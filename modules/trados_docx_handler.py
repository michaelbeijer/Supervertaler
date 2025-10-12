"""
Trados Studio Bilingual DOCX Handler

Handles import and export of Trados Studio 2024 bilingual review format DOCX files.

Trados Bilingual Structure:
- Single table with 4 columns
- Row 0: Header ('Segment ID', 'Segment status', 'Source segment', 'Target segment')
- Row 1+: Segment data with UUID, status, source, and target

Status values from Trados:
- "Not Translated (0%)"
- "Draft (X%)" where X is fuzzy match percentage
- "Translated (100%)"
- "Approved Sign-off"
- etc.

Author: Michael Beijer + AI Assistant
Date: October 12, 2025
"""

from docx import Document
from docx.shared import RGBColor, Pt
from docx.enum.text import WD_COLOR_INDEX
import re
from typing import List, Dict, Tuple, Optional


class TradosDOCXHandler:
    """Handler for Trados Studio bilingual DOCX files"""
    
    @staticmethod
    def is_trados_bilingual_docx(filepath: str) -> bool:
        """
        Check if a DOCX file is a Trados Studio bilingual document.
        
        Args:
            filepath: Path to DOCX file
            
        Returns:
            True if file matches Trados bilingual format
        """
        try:
            doc = Document(filepath)
            
            # Must have exactly one table
            if len(doc.tables) != 1:
                return False
            
            table = doc.tables[0]
            
            # Must have at least 2 rows (header + data)
            if len(table.rows) < 2:
                return False
            
            # Must have exactly 4 columns
            if len(table.columns) != 4:
                return False
            
            # Check header row
            header_row = table.rows[0]
            expected_headers = ['Segment ID', 'Segment status', 'Source segment', 'Target segment']
            
            actual_headers = [cell.text.strip() for cell in header_row.cells]
            
            # Flexible header matching (Trados may vary slightly)
            if len(actual_headers) != 4:
                return False
            
            # Check for key header terms
            has_id = any('id' in h.lower() for h in actual_headers)
            has_status = any('status' in h.lower() for h in actual_headers)
            has_source = any('source' in h.lower() for h in actual_headers)
            has_target = any('target' in h.lower() for h in actual_headers)
            
            return has_id and has_status and has_source and has_target
            
        except Exception:
            return False
    
    @staticmethod
    def extract_segments(filepath: str) -> List[Dict[str, str]]:
        """
        Extract segments from Trados bilingual DOCX.
        
        Args:
            filepath: Path to Trados bilingual DOCX file
            
        Returns:
            List of segment dictionaries with keys:
            - 'id': Segment number (1-indexed)
            - 'trados_id': UUID from Trados
            - 'status': Trados status string
            - 'source': Source text
            - 'target': Target text
            - 'source_formatted': Source with <b>, <i>, <u> tags
            - 'target_formatted': Target with <b>, <i>, <u> tags
        """
        doc = Document(filepath)
        table = doc.tables[0]
        
        segments = []
        
        # Skip header row (row 0)
        for seg_num, row in enumerate(table.rows[1:], 1):
            # Extract cell data
            trados_id = row.cells[0].text.strip()
            status = row.cells[1].text.strip()
            source_cell = row.cells[2]
            target_cell = row.cells[3]
            
            # Extract plain text
            source_text = source_cell.text.strip()
            target_text = target_cell.text.strip()
            
            # Extract formatted text (with <b>, <i>, <u> tags)
            source_formatted = TradosDOCXHandler._extract_formatted_text(source_cell)
            target_formatted = TradosDOCXHandler._extract_formatted_text(target_cell)
            
            segment = {
                'id': seg_num,
                'trados_id': trados_id,
                'status': status,
                'source': source_text,
                'target': target_text,
                'source_formatted': source_formatted,
                'target_formatted': target_formatted
            }
            
            segments.append(segment)
        
        return segments
    
    @staticmethod
    def _extract_formatted_text(cell) -> str:
        """
        Extract text from cell with formatting tags.
        
        Converts Word formatting to HTML-style tags:
        - Bold → <b>text</b>
        - Italic → <i>text</i>
        - Underline → <u>text</u>
        
        Args:
            cell: DOCX table cell
            
        Returns:
            Text with formatting tags
        """
        result = []
        
        for paragraph in cell.paragraphs:
            para_parts = []
            
            for run in paragraph.runs:
                text = run.text
                
                # Check formatting
                is_bold = run.bold == True
                is_italic = run.italic == True
                is_underline = run.underline == True
                
                # Wrap with tags
                if is_bold:
                    text = f"<b>{text}</b>"
                if is_italic:
                    text = f"<i>{text}</i>"
                if is_underline:
                    text = f"<u>{text}</u>"
                
                para_parts.append(text)
            
            result.append(''.join(para_parts))
        
        return '\n'.join(result)
    
    @staticmethod
    def map_trados_status_to_supervertaler(trados_status: str) -> str:
        """
        Map Trados status to Supervertaler status.
        
        Args:
            trados_status: Trados status string (e.g., "Draft (95%)", "Not Translated (0%)")
            
        Returns:
            Supervertaler status: 'untranslated', 'translated', or 'approved'
        """
        status_lower = trados_status.lower()
        
        if 'not translated' in status_lower or '(0%)' in status_lower:
            return 'untranslated'
        elif 'approved' in status_lower or 'sign-off' in status_lower:
            return 'approved'
        elif 'translated (100%)' in status_lower:
            return 'translated'
        elif 'draft' in status_lower or '%' in status_lower:
            return 'translated'  # Draft = partially translated
        else:
            return 'untranslated'  # Default
    
    @staticmethod
    def create_bilingual_docx(segments: List[Dict], output_path: str, 
                             source_lang: str = "English", target_lang: str = "Dutch"):
        """
        Create a Trados-style bilingual DOCX file.
        
        Args:
            segments: List of segment dictionaries with 'source', 'target', 'status'
            output_path: Path for output DOCX file
            source_lang: Source language name
            target_lang: Target language name
        """
        doc = Document()
        
        # Add title
        title = doc.add_paragraph()
        title_run = title.add_run(f"Trados-style Bilingual Review - {source_lang} → {target_lang}")
        title_run.bold = True
        title_run.font.size = Pt(14)
        
        # Create table (4 columns: ID, Status, Source, Target)
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Light Grid Accent 1'
        
        # Header row
        header_cells = table.rows[0].cells
        header_cells[0].text = 'Segment ID'
        header_cells[1].text = 'Segment status'
        header_cells[2].text = 'Source segment'
        header_cells[3].text = 'Target segment'
        
        # Make header bold
        for cell in header_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True
        
        # Add segments
        for seg in segments:
            row_cells = table.add_row().cells
            
            # Segment ID (can be UUID string or integer)
            seg_id = seg.get('id', 0)
            # If it's already a string (UUID), use as-is; otherwise format as number
            if isinstance(seg_id, str):
                row_cells[0].text = seg_id
            else:
                row_cells[0].text = f"seg-{seg_id:04d}"
            
            # Status
            status = seg.get('status', 'untranslated')
            if status == 'approved':
                row_cells[1].text = 'Approved Sign-off'
            elif status == 'translated':
                row_cells[1].text = 'Translated (100%)'
            else:
                row_cells[1].text = 'Not Translated (0%)'
            
            # Source
            source_text = seg.get('source', '')
            TradosDOCXHandler._add_formatted_text_to_cell(row_cells[2], source_text)
            
            # Target
            target_text = seg.get('target', '')
            TradosDOCXHandler._add_formatted_text_to_cell(row_cells[3], target_text)
        
        # Save document
        doc.save(output_path)
    
    @staticmethod
    def _add_formatted_text_to_cell(cell, text: str):
        """
        Add formatted text to cell, converting HTML-style tags to Word formatting.
        
        Args:
            cell: DOCX table cell
            text: Text with optional <b>, <i>, <u> tags
        """
        # Clear existing content
        cell.text = ''
        
        # Parse and add formatted text
        para = cell.paragraphs[0]
        
        # Simple tag parser (handles nested tags)
        parts = TradosDOCXHandler._parse_formatted_text(text)
        
        for part_text, is_bold, is_italic, is_underline in parts:
            run = para.add_run(part_text)
            if is_bold:
                run.bold = True
            if is_italic:
                run.italic = True
            if is_underline:
                run.underline = True
    
    @staticmethod
    def _parse_formatted_text(text: str) -> List[Tuple[str, bool, bool, bool]]:
        """
        Parse text with formatting tags into (text, bold, italic, underline) tuples.
        
        Args:
            text: Text with <b>, <i>, <u> tags
            
        Returns:
            List of (text, is_bold, is_italic, is_underline) tuples
        """
        # Simple regex-based parser
        # This handles basic cases; doesn't handle deeply nested tags perfectly
        
        parts = []
        
        # Split by tags
        pattern = r'(</?[biu]>)'
        tokens = re.split(pattern, text)
        
        is_bold = False
        is_italic = False
        is_underline = False
        
        for token in tokens:
            if token == '<b>':
                is_bold = True
            elif token == '</b>':
                is_bold = False
            elif token == '<i>':
                is_italic = True
            elif token == '</i>':
                is_italic = False
            elif token == '<u>':
                is_underline = True
            elif token == '</u>':
                is_underline = False
            elif token:  # Non-empty text
                parts.append((token, is_bold, is_italic, is_underline))
        
        return parts
    
    @staticmethod
    def update_bilingual_docx(original_filepath: str, segments: List[Dict], output_path: str):
        """
        Update an existing Trados bilingual DOCX file with translated segments.
        
        This preserves the EXACT original format, styles, and structure - critical for
        Trados Studio re-import compatibility.
        
        CRITICAL: Trados tags must maintain the "Tag" character style (italic, pink color).
        
        Args:
            original_filepath: Path to original Trados bilingual DOCX
            segments: List of segment dicts with 'id', 'status', 'target'
            output_path: Path for output DOCX file
        """
        # Load the original document (preserves all styles including "Tag" style)
        doc = Document(original_filepath)
        table = doc.tables[0]
        
        # Verify "Tag" style exists
        tag_style_exists = False
        try:
            tag_style = doc.styles['Tag']
            tag_style_exists = True
        except KeyError:
            # Tag style doesn't exist - will apply formatting manually
            tag_style_exists = False
        
        # Create lookup by Trados UUID
        segments_by_id = {seg.get('id'): seg for seg in segments}
        
        # Update only the target cells and status cells
        # Skip header row (row 0)
        for row_idx, row in enumerate(table.rows[1:], 1):
            # Get the Trados UUID from first column
            trados_id = row.cells[0].text.strip()
            
            # Find matching segment
            if trados_id in segments_by_id:
                seg = segments_by_id[trados_id]
                
                # Update status (column 1)
                status = seg.get('status', '')
                if status:
                    row.cells[1].text = status
                
                # Update target (column 3)
                target_text = seg.get('target', '')
                if target_text:
                    # Clear existing content while preserving cell structure
                    target_cell = row.cells[3]
                    target_cell.text = ''
                    
                    # Get or create paragraph
                    if target_cell.paragraphs:
                        para = target_cell.paragraphs[0]
                    else:
                        para = target_cell.add_paragraph()
                    
                    # Parse and add text with proper tag styling
                    TradosDOCXHandler._add_text_with_tag_styles(para, target_text, tag_style_exists)
        
        # Save to output path
        doc.save(output_path)
        
        # CRITICAL: Post-process to fix XML declaration for Trados compatibility
        # Trados requires: <?xml version="1.0" encoding="utf-8"?>
        # python-docx creates: <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        TradosDOCXHandler._fix_xml_declarations_for_trados(output_path)
    
    @staticmethod
    def _add_text_with_tag_styles(paragraph, text: str, tag_style_exists: bool):
        """
        Add text to paragraph, applying the "Tag" style to Trados tags.
        
        Trados tags follow patterns like <13>, </13>, <231/>, etc.
        These must be styled with the "Tag" character style (italic, pink FF0066).
        
        Args:
            paragraph: DOCX paragraph object
            text: Text containing potential Trados tags
            tag_style_exists: Whether the "Tag" style is available
        """
        # Pattern to match Trados tags: <NUMBER> or </NUMBER> or <NUMBER/>
        tag_pattern = r'(</?(\d+)(/?>))'
        
        import re
        parts = re.split(tag_pattern, text)
        
        for i, part in enumerate(parts):
            if not part:  # Skip empty strings
                continue
            
            # Check if this part is a tag
            is_tag = re.match(r'^</?(\d+)(/?>)$', part)
            
            if is_tag:
                # This is a Trados tag - apply Tag style
                run = paragraph.add_run(part)
                
                if tag_style_exists:
                    # Apply the "Tag" character style
                    run.style = 'Tag'
                else:
                    # Manually apply Tag formatting (italic, pink)
                    run.italic = True
                    from docx.shared import RGBColor
                    run.font.color.rgb = RGBColor(0xFF, 0x00, 0x66)
            else:
                # Regular text - no special styling
                paragraph.add_run(part)
    
    @staticmethod
    def _fix_xml_declarations_for_trados(docx_path: str):
        """
        Post-process DOCX file to fix XML declarations for Trados compatibility.
        
        Trados Studio requires EXACT XML declaration format:
        - <?xml version="1.0" encoding="utf-8"?>
        
        python-docx (via lxml) creates:
        - <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        
        This function rewrites the XML files to match Trados expectations.
        
        Args:
            docx_path: Path to DOCX file to fix
        """
        import zipfile
        import tempfile
        import shutil
        import os
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract DOCX
            extract_path = os.path.join(temp_dir, 'docx_content')
            with zipfile.ZipFile(docx_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            # Fix XML declarations in critical files
            xml_files_to_fix = [
                'word/document.xml',
                'word/styles.xml',
                'word/settings.xml',
                'word/comments.xml'
            ]
            
            for xml_file in xml_files_to_fix:
                xml_path = os.path.join(extract_path, xml_file)
                if os.path.exists(xml_path):
                    with open(xml_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace XML declaration
                    # Match various forms of the declaration
                    import re
                    pattern = r'<\?xml[^?]*\?>'
                    trados_declaration = '<?xml version="1.0" encoding="utf-8"?>'
                    
                    content = re.sub(pattern, trados_declaration, content, count=1)
                    
                    # Write back
                    with open(xml_path, 'w', encoding='utf-8') as f:
                        f.write(content)
            
            # Re-create DOCX
            temp_docx = os.path.join(temp_dir, 'temp.docx')
            with zipfile.ZipFile(temp_docx, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                # Walk through extracted content and add to new zip
                for root, dirs, files in os.walk(extract_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, extract_path)
                        zip_out.write(file_path, arc_name)
            
            # Replace original file
            shutil.copy(temp_docx, docx_path)
