#!/usr/bin/env python3
"""
Test language detection from DOCX files
"""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def detect_docx_language(docx_path):
    """
    Detect language from DOCX file metadata and content
    """
    try:
        languages_found = set()
        
        with zipfile.ZipFile(docx_path, 'r') as docx:
            # Method 1: Check document.xml for language attributes
            try:
                doc_xml = docx.read('word/document.xml')
                root = ET.fromstring(doc_xml)
                
                # Look for language attributes in runs
                for elem in root.iter():
                    if 'lang' in elem.attrib:
                        lang = elem.attrib['lang']
                        if lang:
                            # Take first two letters (e.g., "en-US" -> "en")
                            languages_found.add(lang[:2].lower())
                    
                    # Look for w:lang elements
                    if elem.tag.endswith('}lang'):
                        for attr in ['val', 'eastAsia', 'bidi']:
                            if attr in elem.attrib:
                                lang = elem.attrib[attr]
                                if lang and lang != 'none':
                                    languages_found.add(lang[:2].lower())
                
            except Exception as e:
                print(f"Error reading document.xml: {e}")
            
            # Method 2: Check app.xml for document properties
            try:
                app_xml = docx.read('docProps/app.xml')
                root = ET.fromstring(app_xml)
                
                # Look for language in application properties
                for elem in root.iter():
                    if 'language' in elem.tag.lower() and elem.text:
                        languages_found.add(elem.text[:2].lower())
                        
            except Exception as e:
                print(f"Error reading app.xml: {e}")
            
            # Method 3: Check core.xml for core properties
            try:
                core_xml = docx.read('docProps/core.xml')
                root = ET.fromstring(core_xml)
                
                # Look for language in core properties
                for elem in root.iter():
                    if 'language' in elem.tag.lower() and elem.text:
                        languages_found.add(elem.text[:2].lower())
                        
            except Exception as e:
                print(f"Error reading core.xml: {e}")
        
        # Filter out invalid language codes
        valid_languages = []
        for lang in languages_found:
            if len(lang) == 2 and lang.isalpha():
                valid_languages.append(lang)
        
        return list(set(valid_languages))  # Remove duplicates
        
    except Exception as e:
        print(f"Error detecting language from {docx_path}: {e}")
        return []

# Test with your Dutch document if it exists
test_files = [
    "test.docx",
    "../test.docx", 
    "sample.docx"
]

for test_file in test_files:
    if Path(test_file).exists():
        print(f"\nTesting: {test_file}")
        languages = detect_docx_language(test_file)
        print(f"Detected languages: {languages}")
        break
else:
    print("No test DOCX files found. Create a test.docx file to test language detection.")