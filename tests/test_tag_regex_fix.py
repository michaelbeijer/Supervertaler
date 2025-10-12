"""Test the tag regex fix"""
import re

# The problematic text
test_text = "<14>Biagio Pagano</14> (geboren op 29 januari 1983)"

# OLD pattern (broken - has capturing groups)
old_pattern = r'(</?(\d+)(/?>))'
old_parts = re.split(old_pattern, test_text)
print("OLD PATTERN (BROKEN):")
print(f"  Pattern: {old_pattern}")
print(f"  Split result: {old_parts}")
print(f"  Number of parts: {len(old_parts)}")

# NEW pattern (fixed - only one capturing group for the whole tag)
new_pattern = r'(</?\d+/?>)'
new_parts = re.split(new_pattern, test_text)
print("\nNEW PATTERN (FIXED):")
print(f"  Pattern: {new_pattern}")
print(f"  Split result: {new_parts}")
print(f"  Number of parts: {len(new_parts)}")

# Verify the new pattern works correctly
print("\nVERIFICATION:")
expected = ['', '<14>', 'Biagio Pagano', '</14>', ' (geboren op 29 januari 1983)']
if new_parts == expected:
    print("  ✅ Split is CORRECT!")
else:
    print(f"  ❌ Split is wrong")
    print(f"     Expected: {expected}")
    print(f"     Got: {new_parts}")

# Test reconstruction
reconstructed = ''.join(new_parts)
if reconstructed == test_text:
    print(f"  ✅ Reconstruction is CORRECT!")
else:
    print(f"  ❌ Reconstruction failed")
    print(f"     Original: {test_text}")
    print(f"     Reconstructed: {reconstructed}")

# Test with more tag types
test_cases = [
    "<14>text</14>",
    "<231/>",
    "before <14>text</14> after",
    "<1>a</1> <2>b</2>",
]

print("\nTEST CASES:")
for test in test_cases:
    parts = re.split(new_pattern, test)
    print(f"  '{test}' → {parts}")
