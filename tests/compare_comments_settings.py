"""Compare comments.xml and check for tracked changes"""
import zipfile
import xml.dom.minidom as minidom

trados_file = r'C:\Dev\Supervertaler\user data_private\Projects\trados test\trados-test\External Review\en-US\trados-test.docx.review.docx'
supervertaler_file = r'C:\Dev\Supervertaler\user data_private\Projects\trados test\trados-test\External Review\en-US\trados_bilingual_export.review.docx'

def read_and_format_xml(filepath, xml_path):
    """Read and pretty-print XML from DOCX"""
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        try:
            content = zip_ref.read(xml_path)
            dom = minidom.parseString(content)
            return dom.toprettyxml(indent="  ")
        except Exception as e:
            return f"Error: {e}"

print("="*80)
print("COMMENTS.XML COMPARISON")
print("="*80)

print("\n--- TRADOS FILE comments.xml ---")
trados_comments = read_and_format_xml(trados_file, 'word/comments.xml')
print(trados_comments[:3000])

print("\n\n--- SUPERVERTALER FILE comments.xml ---")
super_comments = read_and_format_xml(supervertaler_file, 'word/comments.xml')
print(super_comments[:3000])

print("\n📊 COMPARISON:")
if trados_comments == super_comments:
    print("✅ comments.xml is IDENTICAL")
else:
    print("❌ comments.xml is DIFFERENT")

# Also check settings.xml
print("\n\n" + "="*80)
print("SETTINGS.XML COMPARISON")
print("="*80)

print("\n--- TRADOS FILE settings.xml ---")
trados_settings = read_and_format_xml(trados_file, 'word/settings.xml')
print(trados_settings[:2000])

print("\n\n--- SUPERVERTALER FILE settings.xml ---")
super_settings = read_and_format_xml(supervertaler_file, 'word/settings.xml')
print(super_settings[:2000])

print("\n📊 COMPARISON:")
if trados_settings == super_settings:
    print("✅ settings.xml is IDENTICAL")
else:
    print("❌ settings.xml is DIFFERENT - THIS MIGHT BE THE PROBLEM!")
