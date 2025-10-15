# Script to update AI prompts for line-separated changes

# Read the file
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the prompt template shown in the report header
old_instructions = '''- Be extremely specific and precise
- Quote the exact words/phrases that changed
- Use this format: "X" changed to "Y" or "X" → "Y"
- For single word changes: quote both words
- For punctuation/formatting: describe precisely (e.g., "curly quotes → straight quotes")
- For additions: "Added: [exact text]"
- For deletions: "Removed: [exact text]"
- Keep response under 15 words
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text

Examples:
✓ "pre-cut" → "incision"
✓ Curly quotes → straight quotes: "roll" → "roll"  
✓ "package" → "packaging"'''

new_instructions = '''- Be extremely specific and precise
- Quote the exact words/phrases that changed
- Use this format: "X" → "Y"
- For single word changes: quote both words
- For multiple changes: put each on its own line
- For punctuation/formatting: describe precisely (e.g., "curly quotes → straight quotes")
- For additions: "Added: [exact text]"
- For deletions: "Removed: [exact text]"
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text

Examples of single changes:
✓ "pre-cut" → "incision"
✓ Curly quotes → straight quotes: "roll" → "roll"  
✓ "package" → "packaging"

Examples of multiple changes (one per line):
✓ "split portions" → "divided portions"
  "connected by a" → "connected, via a"
  "that is located" → "which is located"'''

content = content.replace(old_instructions, new_instructions)

# Write back
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Updated AI prompts for multi-line changes!')
print('   - Multiple changes now appear one per line')
print('   - Much more readable when there are several edits')
print('   - Example: Each "X" → "Y" on its own line')
