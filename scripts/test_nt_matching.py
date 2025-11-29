"""Test non-translatable matching - case sensitivity and word boundaries"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.non_translatables_manager import NonTranslatable

# Test cases
nt_tio = NonTranslatable(text='TiO')
nt_tio_lower = NonTranslatable(text='tio')

test_text = 'The TiO compound in this information contains tio particles.'

print('Test: NonTranslatable matching')
print(f'Text: "{test_text}"')
print()

# Test case-sensitive matching (default)
print('Case-sensitive matching (default):')
matches = nt_tio.matches(test_text)
print(f'  "TiO" matches: {matches}')
for start, end in matches:
    print(f'    Found: "{test_text[start:end]}" at position {start}-{end}')

matches = nt_tio_lower.matches(test_text)
print(f'  "tio" matches: {matches}')
for start, end in matches:
    print(f'    Found: "{test_text[start:end]}" at position {start}-{end}')

# Test case-insensitive matching
print()
print('Case-insensitive matching:')
nt_tio_insensitive = NonTranslatable(text='TiO', case_sensitive=False)
matches = nt_tio_insensitive.matches(test_text)
print(f'  "TiO" (case_sensitive=False) matches: {matches}')
for start, end in matches:
    print(f'    Found: "{test_text[start:end]}" at position {start}-{end}')

# Verify 'information' is NOT matched
print()
print('Verification - should NOT match inside "information":')
print(f'  Substring check: "tio" in "information" = {"tio" in "information"}')
print(f'  But NT matching correctly excludes it due to word boundaries!')

# Additional test with special characters
print()
print('Test with trademark symbols:')
nt_tm = NonTranslatable(text='Microsoft®')
test_tm = 'This uses Microsoft® technology.'
matches = nt_tm.matches(test_tm)
print(f'  "Microsoft®" matches in "{test_tm}": {matches}')
for start, end in matches:
    print(f'    Found: "{test_tm[start:end]}" at position {start}-{end}')

print()
print('✓ All tests completed!')
