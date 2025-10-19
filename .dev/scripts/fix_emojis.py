#!/usr/bin/env python3
"""Fix emoji characters in source files"""

import os
from pathlib import Path

emoji_map = {
    '✓': '[OK]',
    '✗': '[ERROR]',
    '⚠': '[WARNING]',
    '🔄': '[CONVERTING]',
}

files_to_fix = [
    'modules/prompt_library.py',
]

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for emoji, text in emoji_map.items():
        if emoji in content:
            count = content.count(emoji)
            print(f'Replacing {count}x "{emoji}" with "{text}" in {filepath}')
            content = content.replace(emoji, text)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓ Updated {filepath}')
    else:
        print(f'- No changes needed in {filepath}')

print('\n[OK] Emoji replacement complete')
