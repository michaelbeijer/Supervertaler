"""Check for Trados-specific XML metadata and custom properties"""
from docx import Document
import zipfile
import xml.etree.ElementTree as ET

trados_file = r'C:\Dev\Supervertaler\user data_private\Projects\trados test\trados-test\External Review\en-US\trados-test.docx.review.docx'
supervertaler_file = r'C:\Dev\Supervertaler\user data_private\Projects\trados test\trados-test\External Review\en-US\trados_bilingual_export.review.docx'

def check_custom_properties(filepath, label):
    """Check for custom document properties"""
    print(f"\n{'='*80}")
    print(f"{label} - CUSTOM PROPERTIES")
    print(f"{'='*80}")
    
    doc = Document(filepath)
    core_props = doc.core_properties
    
    print(f"\n📋 Core Properties:")
    print(f"   Title: {core_props.title}")
    print(f"   Subject: {core_props.subject}")
    print(f"   Author: {core_props.author}")
    print(f"   Keywords: {core_props.keywords}")
    print(f"   Comments: {core_props.comments}")
    print(f"   Last modified by: {core_props.last_modified_by}")
    print(f"   Created: {core_props.created}")
    print(f"   Modified: {core_props.modified}")

def check_xml_files(filepath, label):
    """Check all XML files in the DOCX package"""
    print(f"\n{'='*80}")
    print(f"{label} - XML PACKAGE CONTENTS")
    print(f"{'='*80}")
    
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        
        print(f"\n📦 Package files ({len(file_list)}):")
        for filename in sorted(file_list):
            print(f"   {filename}")
        
        # Check for Trados-specific files
        print(f"\n🔍 Trados-specific files:")
        trados_files = [f for f in file_list if 'sdl' in f.lower() or 'trados' in f.lower()]
        if trados_files:
            for tf in trados_files:
                print(f"   ✅ {tf}")
        else:
            print(f"   ❌ No Trados-specific files found")
        
        # Check custom XML
        print(f"\n📄 Custom XML files:")
        custom_xml = [f for f in file_list if 'customXml' in f]
        if custom_xml:
            for cx in custom_xml:
                print(f"   ✅ {cx}")
                # Try to read and show content
                try:
                    content = zip_ref.read(cx)
                    print(f"      Size: {len(content)} bytes")
                    if content and len(content) < 1000:
                        print(f"      Content: {content[:500].decode('utf-8', errors='ignore')}")
                except Exception as e:
                    print(f"      Error reading: {e}")
        else:
            print(f"   ❌ No custom XML files found")
        
        # Check document.xml for differences
        print(f"\n📝 Checking document.xml structure...")
        try:
            doc_xml = zip_ref.read('word/document.xml')
            # Parse XML
            root = ET.fromstring(doc_xml)
            
            # Count elements
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            tables = root.findall('.//w:tbl', namespaces)
            paragraphs = root.findall('.//w:p', namespaces)
            
            print(f"   Tables in XML: {len(tables)}")
            print(f"   Paragraphs in XML: {len(paragraphs)}")
            
            # Check for any SDL/Trados namespaces
            print(f"\n   Namespaces:")
            for prefix, uri in root.attrib.items():
                if 'xmlns' in prefix:
                    ns_name = prefix.replace('xmlns:', '').replace('xmlns', 'default')
                    print(f"      {ns_name}: {uri}")
                    if 'sdl' in uri.lower() or 'trados' in uri.lower():
                        print(f"         ⚠️ TRADOS NAMESPACE FOUND!")
        
        except Exception as e:
            print(f"   Error parsing document.xml: {e}")

# Analyze both files
check_custom_properties(trados_file, "TRADOS FILE")
check_custom_properties(supervertaler_file, "SUPERVERTALER FILE")

check_xml_files(trados_file, "TRADOS FILE")
check_xml_files(supervertaler_file, "SUPERVERTALER FILE")

print(f"\n\n{'='*80}")
print("KEY FINDINGS")
print(f"{'='*80}")
print("""
Look for differences in:
1. Custom XML files (Trados may embed metadata here)
2. Trados-specific namespaces in document.xml
3. Custom properties (author, keywords, etc.)
4. Additional package files

These could be required for Trados to recognize the file as valid for re-import.
""")
