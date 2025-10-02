"""Debug script to find why Subtitle is missing"""
from docx import Document

doc = Document('test_style_preservation_input.docx')

print("All paragraphs in document:")
print("=" * 80)
for i, para in enumerate(doc.paragraphs):
    is_empty = not para.text.strip()
    style = para.style.name
    text = para.text
    print(f"{i:2d}. Empty={is_empty}, Style={style:20s}, Text=\"{text}\"")
