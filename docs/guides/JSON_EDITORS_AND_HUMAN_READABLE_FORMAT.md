# JSON Prompt Editors and Human-Readable Format Proposal

**Date**: October 17, 2025  
**Topic**: Better ways to view/edit JSON prompts and proposal for human-readable format

---

## Recommended JSON Editors/Viewers (Free & Open Source)

### 1. **VS Code with JSON Extension** ⭐ BEST OPTION
**Cost**: Free  
**Source**: Open Source  
**Platform**: Windows, Mac, Linux

**Why it's perfect**:
- Shows `\n` as actual line breaks in preview
- Syntax highlighting
- Folding/expanding sections
- Built-in JSON validation
- Search and replace
- Already installed if you use VS Code!

**How to use**:
1. Open JSON file in VS Code
2. Right-click → "Format Document" (Shift+Alt+F)
3. Install extension: "JSON Tools" for even better formatting
4. Preview markdown sections: Select text → Ctrl+Shift+V

### 2. **JSONView Browser Extension**
**Cost**: Free  
**Source**: Open Source  
**Platform**: Chrome, Firefox, Edge

**Features**:
- View JSON files in browser with collapsible trees
- Copy values
- Search within JSON
- No installation needed - just drag JSON file to browser

### 3. **Notepad++ with JSON Viewer Plugin**
**Cost**: Free  
**Source**: Open Source  
**Platform**: Windows only

**Features**:
- Lightweight
- Tree view of JSON structure
- Format/minify JSON
- Search in JSON

---

## Better Alternative: YAML Format

Instead of inventing a new format, consider **YAML** - it's designed to be human-readable!

### Current JSON Format:
```json
{
  "name": "Patent Translation Specialist",
  "description": "Enhanced patent-specific prompts with technical precision and legal accuracy",
  "domain": "Intellectual Property",
  "version": "2.2.0",
  "task_type": "Translation",
  "created": "2025-09-08 - Supervertaler v2.2.0",
  "modified": "2025-10-16",
  "translate_prompt": "You are an expert {source_lang} to {target_lang} patent translator...\n\nKey patent translation principles:\n• Maintain technical precision\n• Preserve claim structure\n..."
}
```

### Same in YAML Format:
```yaml
name: Patent Translation Specialist
description: Enhanced patent-specific prompts with technical precision and legal accuracy
domain: Intellectual Property
version: 2.2.0
task_type: Translation
created: 2025-09-08 - Supervertaler v2.2.0
modified: 2025-10-16

translate_prompt: |
  You are an expert {source_lang} to {target_lang} patent translator...
  
  Key patent translation principles:
  • Maintain technical precision
  • Preserve claim structure
  ...

proofread_prompt: |
  [Optional proofreading instructions here]
```

**Benefits of YAML**:
- ✅ No escape sequences needed (`\n` is actual line break)
- ✅ Cleaner, more readable
- ✅ Python has built-in YAML support (`pip install pyyaml`)
- ✅ Industry standard (used by Docker, Kubernetes, GitHub Actions)
- ✅ Comments supported (`# This is a comment`)
- ✅ Multi-line text is natural (use `|` or `>`)

---

## Your Proposed Format

Your idea of a header + body format is actually similar to **Markdown with YAML front matter**!

### Example: `.md` file with YAML header
```markdown
---
name: Patent Translation Specialist
description: Enhanced patent-specific prompts with technical precision and legal accuracy
domain: Intellectual Property
version: 2.2.0
task_type: Translation
created: 2025-09-08 - Supervertaler v2.2.0
modified: 2025-10-16
---

# SYSTEM PROMPT

You are an expert {source_lang} to {target_lang} patent translator with deep expertise in intellectual property, technical terminology, and patent law requirements.

## Key patent translation principles

• Maintain technical precision and legal accuracy
• Preserve claim structure and dependency relationships
• Use consistent terminology throughout (especially for technical terms)
• Ensure numerical references, measurements, and chemical formulas remain accurate
• Maintain the formal, precise tone required for patent documentation

## Figure References

If a sentence refers to figures, drawings, or diagrams (e.g., 'Figure 1A', 'FIG. 2B', 'Figuur X'), relevant patent drawings may be provided just before that sentence. Use these visual elements as crucial context for accurately translating references to components, structural relationships, process steps, or technical features shown in the patent illustrations.

## Output Format

Present your output ONLY as a numbered list of translations for the requested sentences, using their original numbering. Maintain patent-appropriate terminology, technical accuracy, and the formal register required for intellectual property documentation.
```

**This format**:
- ✅ Human-readable
- ✅ Beautiful in text editor
- ✅ Can preview as formatted markdown
- ✅ Standard format (Jekyll, Hugo, many static site generators use this)
- ✅ Easy to parse in Python

---

## Implementation Comparison

### Staying with JSON
**Pros**:
- Already implemented
- No migration needed
- Industry standard for APIs
- All Python libraries support it

**Cons**:
- Requires escape sequences
- Hard to read/edit manually
- Need special editor

### Switching to YAML
**Pros**:
- Much more readable
- No escape sequences
- Comments supported
- Easy migration (can convert automatically)

**Cons**:
- Need to update `prompt_library.py` to load YAML
- Small learning curve
- Need `pyyaml` dependency

### Markdown + YAML Front Matter
**Pros**:
- MOST human-readable
- Beautiful in text editor AND preview
- Easy to edit
- Can include formatting, examples, documentation

**Cons**:
- Need custom parser for front matter
- Less standard for data storage
- Mixing concerns (data + documentation)

---

## Recommendation: Quick Win

**For immediate improvement**: Use **VS Code** with these extensions:
1. Built-in JSON formatter (Shift+Alt+F)
2. Install "JSON Tools" extension
3. Install "Markdown Preview Enhanced" to preview markdown sections

**For long-term**: Consider migrating to **YAML** format:
- More human-friendly
- Still machine-readable
- Easy migration path
- Industry standard

---

## Migration Script (JSON → YAML)

If you want to try YAML, here's a quick converter:

```python
import json
import yaml
import os

def convert_json_to_yaml(json_path, yaml_path):
    """Convert JSON prompt file to YAML"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Converted {json_path} → {yaml_path}")

# Convert all JSON prompts in a folder
prompts_dir = "c:/Dev/Supervertaler/user data_private/System_prompts"
for filename in os.listdir(prompts_dir):
    if filename.endswith('.json'):
        json_path = os.path.join(prompts_dir, filename)
        yaml_path = json_path.replace('.json', '.yaml')
        convert_json_to_yaml(json_path, yaml_path)
```

---

## Simple JSON Viewer Tool

Here's a quick Python script to view JSON prompts in readable format:

```python
import json
import sys

def view_prompt(json_file):
    """Display JSON prompt in human-readable format"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 80)
    print(f"📄 {data.get('name', 'Unnamed Prompt')}")
    print("=" * 80)
    print()
    
    # Metadata
    print("📋 METADATA")
    print("-" * 80)
    print(f"Description: {data.get('description', 'N/A')}")
    print(f"Domain: {data.get('domain', 'N/A')}")
    print(f"Version: {data.get('version', 'N/A')}")
    print(f"Task Type: {data.get('task_type', 'N/A')}")
    print(f"Created: {data.get('created', 'N/A')}")
    print(f"Modified: {data.get('modified', 'N/A')}")
    print()
    
    # Main prompt
    print("📝 TRANSLATION PROMPT")
    print("-" * 80)
    print(data.get('translate_prompt', 'N/A'))
    print()
    
    # Proofread prompt (if exists)
    if data.get('proofread_prompt'):
        print("✏️ PROOFREADING PROMPT")
        print("-" * 80)
        print(data['proofread_prompt'])
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python view_prompt.py <prompt.json>")
        sys.exit(1)
    
    view_prompt(sys.argv[1])
```

**Usage**:
```powershell
python view_prompt.py "C:\Dev\Supervertaler\user data_private\System_prompts\Patent Translation Specialist.json"
```

---

## Conclusion

**Immediate solution**: Use VS Code - you already have it!  
**Long-term solution**: Consider YAML for better human-readability  
**Your custom format idea**: Great thinking! YAML + Markdown front matter achieves this

The key insight is: **Don't invent a new format when excellent standards exist** (YAML, TOML, or Markdown with front matter).
