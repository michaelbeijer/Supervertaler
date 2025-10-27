"""
Quick test script for TMX export functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the TMXGenerator class
from datetime import datetime
import xml.etree.ElementTree as ET

def get_simple_lang_code(lang_name_or_code_input):
    """Convert language name to simple 2-letter code"""
    if not lang_name_or_code_input:
        return ""
    lang_lower = lang_name_or_code_input.strip().lower()
    lang_map = {
        "english": "en", "dutch": "nl", "german": "de", "french": "fr",
        "spanish": "es", "italian": "it", "japanese": "ja", "chinese": "zh",
        "russian": "ru", "portuguese": "pt",
    }
    if lang_lower in lang_map:
        return lang_map[lang_lower]
    base_code = lang_lower.split('-')[0].split('_')[0]
    if len(base_code) == 2:
        return base_code
    return lang_lower[:2]

class TMXGenerator:
    """Helper class for generating TMX (Translation Memory eXchange) files"""
    
    def __init__(self, log_callback=None):
        self.log = log_callback if log_callback else lambda msg: print(msg)
    
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
        header.set('creationtoolversion', '2.5.0')
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


# Test the TMX generator
if __name__ == "__main__":
    print("Testing TMXGenerator...")
    
    # Create test data
    source_segments = [
        "This is a test sentence.",
        "The method comprises the following steps.",
        "Figure 1 shows an example embodiment."
    ]
    
    target_segments = [
        "Dit is een testzin.",
        "De werkwijze omvat de volgende stappen.",
        "Figuur 1 toont een voorbeelduitvoeringsvorm."
    ]
    
    # Create TMX generator
    generator = TMXGenerator()
    
    # Generate TMX
    print("\nGenerating TMX...")
    tmx_tree = generator.generate_tmx(
        source_segments,
        target_segments,
        "English",
        "Dutch"
    )
    
    # Save TMX
    output_file = "test_output.tmx"
    print(f"\nSaving to {output_file}...")
    if generator.save_tmx(tmx_tree, output_file):
        print(f"✓ Success! TMX file created: {output_file}")
        
        # Read and display content
        print("\nTMX file content:")
        print("-" * 60)
        with open(output_file, 'r', encoding='utf-8') as f:
            print(f.read())
        print("-" * 60)
        
        # Clean up
        print(f"\nCleaning up test file...")
        os.remove(output_file)
        print("✓ Test complete!")
    else:
        print("✗ Failed to create TMX file")
