"""Compare the customXML content between files"""
import zipfile
import xml.dom.minidom as minidom

trados_file = r'C:\Dev\Supervertaler\user data_private\Projects\trados test\trados-test\External Review\en-US\trados-test.docx.review.docx'
supervertaler_file = r'C:\Dev\Supervertaler\user data_private\Projects\trados test\trados-test\External Review\en-US\trados_bilingual_export.review.docx'

def read_and_format_xml(filepath, xml_path):
    """Read and pretty-print XML from DOCX"""
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        try:
            content = zip_ref.read(xml_path)
            # Pretty print
            dom = minidom.parseString(content)
            return dom.toprettyxml(indent="  ")
        except Exception as e:
            return f"Error: {e}"

print("="*80)
print("CUSTOM XML COMPARISON")
print("="*80)

# Check customXML/item.xml
print("\n📄 customXML/item.xml")
print("\n--- TRADOS FILE ---")
trados_custom_xml = read_and_format_xml(trados_file, 'customXML/item.xml')
print(trados_custom_xml[:2000])

print("\n--- SUPERVERTALER FILE ---")
super_custom_xml = read_and_format_xml(supervertaler_file, 'customXML/item.xml')
print(super_custom_xml[:2000])

print("\n📊 COMPARISON:")
if trados_custom_xml == super_custom_xml:
    print("✅ customXML/item.xml is IDENTICAL")
else:
    print("❌ customXML/item.xml is DIFFERENT")
    print("\nShowing differences...")
    
    # Simple line-by-line diff
    trados_lines = trados_custom_xml.split('\n')
    super_lines = super_custom_xml.split('\n')
    
    for i, (t_line, s_line) in enumerate(zip(trados_lines[:50], super_lines[:50])):
        if t_line != s_line:
            print(f"\nLine {i}:")
            print(f"  Trados:        {t_line}")
            print(f"  Supervertaler: {s_line}")

# Also check itemProps
print("\n\n📄 customXML/itemProps1.xml")
print("\n--- TRADOS FILE ---")
trados_props = read_and_format_xml(trados_file, 'customXML/itemProps1.xml')
print(trados_props)

print("\n--- SUPERVERTALER FILE ---")
super_props = read_and_format_xml(supervertaler_file, 'customXML/itemProps1.xml')
print(super_props)

print("\n📊 COMPARISON:")
if trados_props == super_props:
    print("✅ customXML/itemProps1.xml is IDENTICAL")
else:
    print("❌ customXML/itemProps1.xml is DIFFERENT")
