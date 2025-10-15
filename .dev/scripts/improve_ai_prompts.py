# Script to improve AI change summary prompts for precision

# Read the file
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. First, update the report header to include AI prompt information
old_header = '''            md_content = f"""# Tracked Changes Analysis Report

**Generated:** {timestamp}  
**Total Changes:** {len(data_to_export)}  
**Filter Applied:** {"Yes - " + search_text if export_filtered else "No"}  
**AI Analysis:** {"Enabled" if ai_analysis else "Disabled"}

---

"""'''

new_header = '''            # Build AI prompt info for report header
            ai_prompt_info = ""
            if ai_analysis and hasattr(self, 'parent_app') and self.parent_app:
                provider = self.parent_app.provider_var.get()
                model = self.parent_app.model_var.get()
                ai_prompt_info = f"""

### AI Analysis Configuration

**Provider:** {provider}  
**Model:** {model}

**Prompt Template Used:**
```
You are a precision editor analyzing changes between two versions of text.
Compare the original and revised text and identify EXACTLY what changed.

CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
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
✓ "package" → "packaging"
✓ Added: "carefully"
✓ "color" → "colour" (US to UK spelling)
✗ Clarified terminology (too vague)
✗ Fixed grammar (not specific)
✗ Improved word choice (not helpful)
```

---

"""
            
            md_content = f"""# Tracked Changes Analysis Report

**Generated:** {timestamp}  
**Total Changes:** {len(data_to_export)}  
**Filter Applied:** {"Yes - " + search_text if export_filtered else "No"}  
**AI Analysis:** {"Enabled" if ai_analysis else "Disabled"}
{ai_prompt_info}
"""'''

content = content.replace(old_header, new_header)

# 2. Update Gemini prompt
old_gemini_prompt = '''                prompt = f"""Analyze this editing change and provide a VERY brief summary (max 10 words):

Original: {original_text}
Revised: {revised_text}

Summarize what changed (e.g., "Fixed grammar", "Clarified meaning", "Added detail", "Changed tone"):"""'''

new_gemini_prompt = '''                prompt = f"""You are a precision editor analyzing changes between two versions of text.
Compare the original and revised text and identify EXACTLY what changed.

Original: {original_text}
Revised: {revised_text}

CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
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
✓ "package" → "packaging"
✗ Clarified terminology
✗ Fixed grammar

Your precise change summary:"""'''

content = content.replace(old_gemini_prompt, new_gemini_prompt)

# 3. Update Claude prompt
old_claude_prompt = '''                message = client.messages.create(
                    model=model_name,
                    max_tokens=50,
                    messages=[{
                        "role": "user",
                        "content": f"""Analyze this editing change and provide a VERY brief summary (max 10 words):

Original: {original_text}
Revised: {revised_text}

Summarize what changed (e.g., "Fixed grammar", "Clarified meaning", "Added detail"):"""
                    }]
                )'''

new_claude_prompt = '''                message = client.messages.create(
                    model=model_name,
                    max_tokens=100,
                    messages=[{
                        "role": "user",
                        "content": f"""You are a precision editor analyzing changes between two versions of text.
Compare the original and revised text and identify EXACTLY what changed.

Original: {original_text}
Revised: {revised_text}

CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
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
✓ "package" → "packaging"
✗ Clarified terminology
✗ Fixed grammar

Your precise change summary:"""
                    }]
                )'''

content = content.replace(old_claude_prompt, new_claude_prompt)

# 4. Update OpenAI prompt
old_openai_prompt = '''                response = client.chat.completions.create(
                    model=model_name,
                    max_tokens=50,
                    messages=[{
                        "role": "user",
                        "content": f"""Analyze this editing change and provide a VERY brief summary (max 10 words):

Original: {original_text}
Revised: {revised_text}

Summarize what changed (e.g., "Fixed grammar", "Clarified meaning", "Added detail"):"""
                    }]
                )'''

new_openai_prompt = '''                response = client.chat.completions.create(
                    model=model_name,
                    max_tokens=100,
                    messages=[{
                        "role": "user",
                        "content": f"""You are a precision editor analyzing changes between two versions of text.
Compare the original and revised text and identify EXACTLY what changed.

Original: {original_text}
Revised: {revised_text}

CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
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
✓ "package" → "packaging"
✗ Clarified terminology
✗ Fixed grammar

Your precise change summary:"""
                    }]
                )'''

content = content.replace(old_openai_prompt, new_openai_prompt)

# 5. Update token limits to remove word count truncation (we want precise answers, not cut-off ones)
content = content.replace('# Limit to first sentence or 10 words', '# Clean up the response')
content = content.replace('''                summary = response.text.strip()
                # Limit to first sentence or 10 words
                summary = summary.split('.')[0].split('\\n')[0]
                words = summary.split()
                if len(words) > 10:
                    summary = ' '.join(words[:10]) + '...'
                return summary''', '''                summary = response.text.strip()
                # Clean up the response - remove extra formatting
                summary = summary.replace('Your precise change summary:', '').strip()
                summary = summary.split('\\n')[0]  # First line only
                return summary''')

content = content.replace('''                summary = message.content[0].text.strip()
                words = summary.split()
                if len(words) > 10:
                    summary = ' '.join(words[:10]) + '...'
                return summary''', '''                summary = message.content[0].text.strip()
                # Clean up the response - remove extra formatting
                summary = summary.replace('Your precise change summary:', '').strip()
                summary = summary.split('\\n')[0]  # First line only
                return summary''')

content = content.replace('''                summary = response.choices[0].message.content.strip()
                words = summary.split()
                if len(words) > 10:
                    summary = ' '.join(words[:10]) + '...'
                return summary''', '''                summary = response.choices[0].message.content.strip()
                # Clean up the response - remove extra formatting
                summary = summary.replace('Your precise change summary:', '').strip()
                summary = summary.split('\\n')[0]  # First line only
                return summary''')

# Write back
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Updated AI change summary prompts!')
print('   - Much more specific and precise instructions')
print('   - AI will now quote exact changed words/phrases')
print('   - Examples provided: "pre-cut" → "incision"')
print('   - No more vague terms like "clarified" or "improved"')
print('   - Increased token limits (50 → 100) for complete responses')
print('   - Report header now includes the AI prompt template')
print('   - Better handling of punctuation/formatting changes')
