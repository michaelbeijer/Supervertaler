"""Extract the Tag style definition from the document"""
from docx import Document

filepath = 'C:/Dev/Supervertaler/user data_private/Trados Studio 2024 bilingual review format test file (with formatting tags).docx'
doc = Document(filepath)

print("=== Available Styles ===\n")
for style in doc.styles:
    if 'tag' in style.name.lower():
        print(f"Style name: {style.name}")
        print(f"  Type: {style.type}")
        print(f"  Style ID: {style.style_id}")
        if hasattr(style, 'font'):
            print(f"  Font properties:")
            print(f"    name: {style.font.name}")
            print(f"    size: {style.font.size}")
            print(f"    bold: {style.font.bold}")
            print(f"    italic: {style.font.italic}")
            print(f"    color.rgb: {style.font.color.rgb if hasattr(style.font.color, 'rgb') else 'N/A'}")
            print(f"    color.theme_color: {style.font.color.theme_color if hasattr(style.font.color, 'theme_color') else 'N/A'}")
        
        # Get XML of style
        print(f"\n  Style XML:")
        print(f"    {style._element.xml}")
        print()
