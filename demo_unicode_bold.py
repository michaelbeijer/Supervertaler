#!/usr/bin/env python3
"""
Demo: TMX Editor Unicode Bold Highlighting
Shows how search terms appear in bold in the Treeview grid
"""

def to_unicode_bold(text):
    """Convert text to Unicode bold characters"""
    bold_map = {
        **{chr(ord('A') + i): chr(0x1D400 + i) for i in range(26)},  # A-Z
        **{chr(ord('a') + i): chr(0x1D41A + i) for i in range(26)},  # a-z
        **{chr(ord('0') + i): chr(0x1D7CE + i) for i in range(10)},  # 0-9
    }
    return ''.join(bold_map.get(c, c) for c in text)

print("=" * 60)
print("TMX Editor - Unicode Bold Highlighting Demo")
print("=" * 60)
print()
print("When you search for a term, it appears in BOLD in the grid:")
print()

# Example 1
search_term = "concrete"
bold_term = to_unicode_bold(search_term)
print(f"Search term: \"{search_term}\"")
print()
print("Results in grid (with light yellow background):")
print(f"  001 | T-shaped {bold_term} base (configuration 2)")
print(f"  002 | T-shaped {bold_term} base")
print(f"  003 | Reinforced {bold_term} structure")
print(f"  004 | Pre-cast {bold_term} element")
print()

# Example 2
print("-" * 60)
search_term2 = "Base"
bold_term2 = to_unicode_bold(search_term2)
print(f"Search term: \"{search_term2}\"")
print()
print("Results in grid:")
print(f"  010 | {bold_term2} plate assembly")
print(f"  011 | Foundation {bold_term2} 123")
print(f"  012 | Steel {bold_term2} configuration")
print()

# Comparison
print("=" * 60)
print("Character Comparison:")
print("=" * 60)
examples = ["concrete", "Base", "Test123", "Foundation"]
for ex in examples:
    bold = to_unicode_bold(ex)
    print(f"  Normal: {ex:<15} Bold: {bold}")
print()
print("✅ True bold text in Treeview - no markers, no special chars!")
print("✅ Combined with light yellow row background for easy scanning")
