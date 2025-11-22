"""
TMX Generator Module

Helper class for generating TMX (Translation Memory eXchange) files.
Supports TMX 1.4 format with proper XML structure.

Extracted from main Supervertaler file for better modularity.
"""

import xml.etree.ElementTree as ET
from datetime import datetime


def get_simple_lang_code(lang_name_or_code_input):
    """
    Convert language name or code to ISO 639-1 format (2-letter) or ISO 639-1 + region (e.g., en-US)
    
    Supports:
    - Language names: "English" → "en", "Dutch" → "nl"
    - ISO codes: "en" → "en", "nl-NL" → "nl-NL"
    - Variants: "en-US", "nl-BE", "fr-CA" → preserved as-is
    
    Returns base code if no variant specified, or full code with variant if provided.
    """
    if not lang_name_or_code_input:
        return "en"  # Default to English
    
    lang_input = lang_name_or_code_input.strip()
    lang_lower = lang_input.lower()
    
    # Comprehensive language name to ISO 639-1 mapping
    lang_map = {
        # Major languages
        "english": "en",
        "dutch": "nl",
        "german": "de",
        "french": "fr",
        "spanish": "es",
        "italian": "it",
        "portuguese": "pt",
        "russian": "ru",
        "chinese": "zh",
        "japanese": "ja",
        "korean": "ko",
        "arabic": "ar",
        
        # European languages
        "afrikaans": "af",
        "albanian": "sq",
        "armenian": "hy",
        "basque": "eu",
        "bengali": "bn",
        "bulgarian": "bg",
        "catalan": "ca",
        "croatian": "hr",
        "czech": "cs",
        "danish": "da",
        "estonian": "et",
        "finnish": "fi",
        "galician": "gl",
        "georgian": "ka",
        "greek": "el",
        "hebrew": "he",
        "hindi": "hi",
        "hungarian": "hu",
        "icelandic": "is",
        "indonesian": "id",
        "irish": "ga",
        "latvian": "lv",
        "lithuanian": "lt",
        "macedonian": "mk",
        "malay": "ms",
        "norwegian": "no",
        "persian": "fa",
        "polish": "pl",
        "romanian": "ro",
        "serbian": "sr",
        "slovak": "sk",
        "slovenian": "sl",
        "swahili": "sw",
        "swedish": "sv",
        "thai": "th",
        "turkish": "tr",
        "ukrainian": "uk",
        "urdu": "ur",
        "vietnamese": "vi",
        "welsh": "cy",
        
        # Chinese variants
        "chinese (simplified)": "zh-CN",
        "chinese (traditional)": "zh-TW",
    }
    
    # Check if it's a full language name
    if lang_lower in lang_map:
        return lang_map[lang_lower]
    
    # Check if already ISO code (2-letter or with variant)
    # Examples: "en", "en-US", "nl-NL", "fr-CA"
    if '-' in lang_input or '_' in lang_input:
        # Has variant - preserve it
        parts = lang_input.replace('_', '-').split('-')
        if len(parts[0]) == 2:
            # Valid format like "en-US"
            return f"{parts[0].lower()}-{parts[1].upper()}"
    
    # Extract base code if it looks like an ISO code
    base_code = lang_lower.split('-')[0].split('_')[0]
    if len(base_code) == 2 and base_code.isalpha():
        return base_code
    
    # Fallback: return first 2 characters or default
    if len(lang_input) >= 2:
        return lang_input[:2].lower()
    
    return "en"  # Ultimate fallback


def get_base_lang_code(lang_code: str) -> str:
    """Extract base language code from variant (e.g., 'en-US' → 'en', 'nl-BE' → 'nl')"""
    if not lang_code:
        return "en"
    return lang_code.split('-')[0].split('_')[0].lower()


def normalize_lang_variant(lang_code: str) -> str:
    """Normalize language variant to lowercase-UPPERCASE format (e.g., 'en-us' → 'en-US', 'nl-be' → 'nl-BE').
    
    Handles various input formats:
    - nl-nl → nl-NL
    - nl-NL → nl-NL  
    - NL-NL → nl-NL
    - nl_BE → nl-BE
    - nl → nl (base code unchanged)
    """
    if not lang_code:
        return lang_code
    
    # Replace underscores with hyphens
    lang_code = lang_code.replace('_', '-')
    
    parts = lang_code.split('-')
    if len(parts) == 1:
        # Base language code only (e.g., 'nl', 'en')
        return parts[0].lower()
    elif len(parts) == 2:
        # Language variant (e.g., 'en-US', 'nl-BE')
        return f"{parts[0].lower()}-{parts[1].upper()}"
    else:
        # Unexpected format, just lowercase the first part
        return parts[0].lower()


def languages_are_compatible(lang1: str, lang2: str) -> bool:
    """Check if two language codes are compatible (same base language)"""
    return get_base_lang_code(lang1) == get_base_lang_code(lang2)


class TMXGenerator:
    """Helper class for generating TMX (Translation Memory eXchange) files"""
    
    def __init__(self, log_callback=None):
        self.log = log_callback if log_callback else lambda msg: None
    
    def generate_tmx(self, source_segments, target_segments, source_lang, target_lang):
        """Generate TMX content from parallel segments"""
        # Basic TMX structure
        tmx = ET.Element('tmx')
        tmx.set('version', '1.4')
        
        header = ET.SubElement(tmx, 'header')
        header.set('creationdate', datetime.now().strftime('%Y%m%dT%H%M%SZ'))
        header.set('srclang', get_simple_lang_code(source_lang))
        header.set('adminlang', 'en')
        header.set('segtype', 'sentence')
        header.set('creationtool', 'Supervertaler')
        header.set('creationtoolversion', '3.6.0-beta')
        header.set('datatype', 'plaintext')
        
        body = ET.SubElement(tmx, 'body')
        
        # Add translation units
        added_count = 0
        for src, tgt in zip(source_segments, target_segments):
            if not src.strip() or not tgt or '[ERR' in str(tgt) or '[Missing' in str(tgt):
                continue
                
            tu = ET.SubElement(body, 'tu')
            
            # Source segment
            tuv_src = ET.SubElement(tu, 'tuv')
            tuv_src.set('xml:lang', get_simple_lang_code(source_lang))
            seg_src = ET.SubElement(tuv_src, 'seg')
            seg_src.text = src.strip()
            
            # Target segment
            tuv_tgt = ET.SubElement(tu, 'tuv')
            tuv_tgt.set('xml:lang', get_simple_lang_code(target_lang))
            seg_tgt = ET.SubElement(tuv_tgt, 'seg')
            seg_tgt.text = str(tgt).strip()
            
            added_count += 1
        
        self.log(f"[TMX Generator] Created TMX with {added_count} translation units")
        return ET.ElementTree(tmx)
    
    def save_tmx(self, tmx_tree, output_path):
        """Save TMX tree to file with proper XML formatting"""
        try:
            # Pretty print with indentation
            self._indent(tmx_tree.getroot())
            tmx_tree.write(output_path, encoding='utf-8', xml_declaration=True)
            self.log(f"[TMX Generator] Saved TMX file: {output_path}")
            return True
        except Exception as e:
            self.log(f"[TMX Generator] Error saving TMX: {e}")
            return False
    
    def _indent(self, elem, level=0):
        """Add indentation to XML for pretty printing"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
