"""
TMX Generator Module

Helper class for generating TMX (Translation Memory eXchange) files.
Supports TMX 1.4 format with proper XML structure.

Extracted from main Supervertaler file for better modularity.
"""

import re
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
    """Extract base language code from variant (e.g., 'en-US' → 'en', 'nl-BE' → 'nl', 'Dutch' → 'nl')"""
    if not lang_code:
        return "en"
    
    # First convert full language names to ISO codes
    iso_code = get_simple_lang_code(lang_code)
    
    # Then extract base code from variant
    return iso_code.split('-')[0].split('_')[0].lower()


def get_lang_match_variants(lang_code: str) -> list:
    """
    Get all possible string variants for matching a language in database queries.
    
    Returns list of strings that could be used to match this language, including:
    - Base ISO code (e.g., 'nl', 'en')
    - Full language names (e.g., 'Dutch', 'English')
    - Common variants (e.g., 'nl-NL', 'en-US')
    
    This helps match database entries that may have inconsistent language formats.
    """
    if not lang_code:
        return ['en', 'English']
    
    # Reverse mapping from ISO codes to full names
    code_to_name = {
        "en": "English",
        "nl": "Dutch",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ar": "Arabic",
        "pl": "Polish",
        "sv": "Swedish",
        "da": "Danish",
        "no": "Norwegian",
        "fi": "Finnish",
    }
    
    # Get the base ISO code
    base_code = get_base_lang_code(lang_code)
    
    variants = [base_code]
    
    # Add full language name if we know it
    if base_code in code_to_name:
        variants.append(code_to_name[base_code])
    
    return variants

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


# ---------------------------------------------------------------------------
# TMX inline tag helpers
# ---------------------------------------------------------------------------

# Outer wrapping tags that should be stripped entirely before TMX export.
# These are structural/segment-level tags — they carry no meaning inside a TM.
_OUTER_TAGS = {
    'li-o', 'li-b', 'li', 'p', 'td', 'th', 'tr', 'div', 'span',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title', 'caption',
    'blockquote', 'pre', 'code', 'dt', 'dd', 'header', 'footer',
    'article', 'section', 'aside', 'nav', 'main', 'figure', 'figcaption',
}

# Inline formatting tags that become <bpt>/<ept> paired tags in TMX.
_FORMATTING_TAG_TYPES = {
    'b': 'bold', 'i': 'italic', 'u': 'underline',
    'em': 'italic', 'strong': 'bold',
    'sub': 'subscript', 'sup': 'superscript',
    's': 'strikethrough', 'strike': 'strikethrough',
    'mark': 'highlight',
}

# Pre-compiled regex: matches opening or closing formatting tags.
_FMT_TAG_RE = re.compile(
    r'<(/?)(' + '|'.join(re.escape(t) for t in _FORMATTING_TAG_TYPES) + r')(?:\s[^>]*)?>',
    re.IGNORECASE,
)

# Pre-compiled regex: matches an outer wrapping tag pair.
_OUTER_OPEN_RE = re.compile(
    r'^<(' + '|'.join(re.escape(t) for t in _OUTER_TAGS) + r')(?:\s[^>]*)?>',
    re.IGNORECASE,
)


def _strip_outer_tags(text: str) -> str:
    """Remove outermost structural tag pair if it wraps the entire text."""
    text = text.strip()
    m = _OUTER_OPEN_RE.match(text)
    if not m:
        return text
    tag = m.group(1).lower()
    closing = f'</{tag}>'
    if not text.lower().endswith(closing):
        return text
    inner = text[m.end():-len(closing)]
    # Reject if the same tag is nested inside
    if re.search(rf'<{re.escape(tag)}[\s>]', inner, re.IGNORECASE):
        return inner  # still strip — nested duplicates are rare and harmless
    return inner


def _build_seg(parent: ET.Element, text: str) -> ET.Element:
    """Build a <seg> element with proper TMX <bpt>/<ept> inline tags.

    1. Strips outer wrapping tags (``<li-b>``, ``<p>``, …).
    2. Converts formatting tags (``<b>``, ``<i>``, …) to TMX ``<bpt>``/``<ept>``
       paired elements following Trados conventions.
    3. Returns the <seg> element (already attached to *parent*).
    """
    seg = ET.SubElement(parent, 'seg')
    text = _strip_outer_tags(text.strip())

    # Fast path: no formatting tags at all → plain text segment
    if not _FMT_TAG_RE.search(text):
        seg.text = text
        return seg

    # --- Slow path: build mixed content with <bpt>/<ept> children ---------
    tag_counter = 0
    open_stack: dict[str, list[int]] = {}   # tag_name → [counter, …]
    last_end = 0
    last_elem = None  # most-recently-added child (for setting .tail)

    for match in _FMT_TAG_RE.finditer(text):
        is_closing = match.group(1) == '/'
        tag_name = match.group(2).lower()

        # Text fragment before this tag
        fragment = text[last_end:match.start()]
        if fragment:
            if last_elem is None:
                seg.text = (seg.text or '') + fragment
            else:
                last_elem.tail = (last_elem.tail or '') + fragment

        if not is_closing:
            # Opening tag → <bpt i="N" type="bold">
            tag_counter += 1
            bpt = ET.SubElement(seg, 'bpt')
            bpt.set('i', str(tag_counter))
            bpt.set('type', _FORMATTING_TAG_TYPES.get(tag_name, tag_name))
            bpt.tail = ''
            last_elem = bpt
            open_stack.setdefault(tag_name, []).append(tag_counter)
        else:
            # Closing tag → <ept i="N">
            i_val = open_stack.get(tag_name, [tag_counter])
            i_val = i_val.pop() if i_val else tag_counter
            ept = ET.SubElement(seg, 'ept')
            ept.set('i', str(i_val))
            ept.tail = ''
            last_elem = ept

        last_end = match.end()

    # Remaining text after the last tag
    remaining = text[last_end:]
    if remaining:
        if last_elem is None:
            seg.text = (seg.text or '') + remaining
        else:
            last_elem.tail = (last_elem.tail or '') + remaining

    return seg


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
        header.set('datatype', 'unknown')

        body = ET.SubElement(tmx, 'body')

        # Add translation units
        added_count = 0
        for src, tgt in zip(source_segments, target_segments):
            if not src.strip() or not tgt or '[ERR' in str(tgt) or '[Missing' in str(tgt):
                continue

            tu = ET.SubElement(body, 'tu')

            # Source segment — outer tags stripped, formatting → bpt/ept
            tuv_src = ET.SubElement(tu, 'tuv')
            tuv_src.set('xml:lang', get_simple_lang_code(source_lang))
            _build_seg(tuv_src, src)

            # Target segment — same treatment
            tuv_tgt = ET.SubElement(tu, 'tuv')
            tuv_tgt.set('xml:lang', get_simple_lang_code(target_lang))
            _build_seg(tuv_tgt, str(tgt))

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
        """Add indentation to XML for pretty printing.

        Skips <seg> elements entirely — their mixed content (text + bpt/ept
        children) must not be touched or whitespace will leak into the TM.
        """
        if elem.tag == 'seg':
            # Only set tail so the *parent* structure stays tidy
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = "\n" + level * "  "
            return

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
