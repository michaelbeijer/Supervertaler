# Script to enhance prompts for better quote detection

# Read the file
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the batch prompt to emphasize quote detection
old_batch_prompt = '''            # Build batch prompt with all changes
            batch_prompt = """You are a precision editor analyzing changes between multiple text versions.
For each numbered pair below, identify EXACTLY what changed.

CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
- Quote the exact words/phrases that changed
- Use format: "X" → "Y"
- For multiple changes in one segment: put each on its own line
- For punctuation/formatting: describe precisely
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text

"""'''

new_batch_prompt = '''            # Build batch prompt with all changes
            batch_prompt = """You are a precision editor analyzing changes between multiple text versions.
For each numbered pair below, identify EXACTLY what changed.

CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
- PAY SPECIAL ATTENTION to quote marks: " vs " vs " (curly vs straight)
- Check for apostrophe changes: ' vs ' (curly vs straight)
- Check for dash changes: - vs – vs — (hyphen vs en-dash vs em-dash)
- Quote the exact words/phrases that changed
- Use format: "X" → "Y"
- For multiple changes in one segment: put each on its own line
- For punctuation/formatting: describe precisely (e.g., 'Curly quotes → straight quotes: "word" → "word"')
- DO NOT say "No change" unless texts are 100% identical (byte-for-byte)
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text

IMPORTANT: If only punctuation changed (quotes, apostrophes, dashes), you MUST report it!

"""'''

content = content.replace(old_batch_prompt, new_batch_prompt)

# Update the report header prompt template to include quote detection
old_header_instructions = '''- Be extremely specific and precise
- Quote the exact words/phrases that changed
- Use this format: "X" → "Y"
- For single word changes: quote both words
- For multiple changes: put each on its own line
- For punctuation/formatting: describe precisely (e.g., "curly quotes → straight quotes")
- For additions: "Added: [exact text]"
- For deletions: "Removed: [exact text]"
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text'''

new_header_instructions = '''- Be extremely specific and precise
- PAY SPECIAL ATTENTION to quote marks: " vs " vs " (curly vs straight)
- Check for apostrophe changes: ' vs ' (curly vs straight)  
- Check for dash changes: - vs – vs — (hyphen vs en-dash vs em-dash)
- Quote the exact words/phrases that changed
- Use this format: "X" → "Y"
- For single word changes: quote both words
- For multiple changes: put each on its own line
- For punctuation/formatting: describe precisely
- For additions: "Added: [exact text]"
- For deletions: "Removed: [exact text]"
- DO NOT say "No change" unless texts are 100% identical
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text'''

content = content.replace(old_header_instructions, new_header_instructions)

# Update the single-segment prompt (get_ai_change_summary) for all three providers
old_single_instructions = '''CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
- Quote the exact words/phrases that changed
- Use this format: "X" changed to "Y" or "X" → "Y"
- For single word changes: quote both words
- For punctuation/formatting: describe precisely (e.g., "curly quotes → straight quotes")
- For additions: "Added: [exact text]"
- For deletions: "Removed: [exact text]"
- Keep response under 15 words
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text'''

new_single_instructions = '''CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
- PAY SPECIAL ATTENTION to quote marks: " vs " vs " (curly vs straight)
- Check for apostrophe changes: ' vs ' (curly vs straight)
- Check for dash changes: - vs – vs — (hyphen vs en-dash vs em-dash)
- Quote the exact words/phrases that changed
- Use this format: "X" → "Y"
- For single word changes: quote both words
- For punctuation/formatting: describe precisely
- For additions: "Added: [exact text]"
- For deletions: "Removed: [exact text]"
- Keep response under 15 words
- DO NOT say "No change" unless texts are 100% identical
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text'''

content = content.replace(old_single_instructions, new_single_instructions)

# Update examples to show quote changes more prominently
old_examples = '''Examples of single changes:
✓ "pre-cut" → "incision"
✓ Curly quotes → straight quotes: "roll" → "roll"  
✓ "package" → "packaging"

Examples of multiple changes (one per line):
✓ "split portions" → "divided portions"
  "connected by a" → "connected, via a"
  "that is located" → "which is located"'''

new_examples = '''Examples of single changes:
✓ "pre-cut" → "incision"
✓ Curly quotes → straight quotes: "word" → "word"
✓ Curly apostrophe → straight: don't → don't
✓ "package" → "packaging"

Examples of multiple changes (one per line):
✓ "split portions" → "divided portions"
  "connected by a" → "connected, via a"
  Curly quotes → straight quotes throughout'''

content = content.replace(old_examples, new_examples)

# Write back
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Enhanced AI prompts for quote/punctuation detection!')
print('   - Special attention to curly vs straight quotes (" " vs ")')
print('   - Checks for apostrophe changes (\' vs \')')
print('   - Checks for dash changes (- vs – vs —)')
print('   - Explicitly forbids saying "No change" unless 100% identical')
print('   - Updated examples to show quote changes prominently')
print('   - Applied to both batch and single-segment prompts')
