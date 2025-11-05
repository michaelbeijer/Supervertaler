# System Prompts (Layer 1: Infrastructure)

⚙️ **Layer 1** contains the core infrastructure prompts that define fundamental rules for translation quality, CAT tool compatibility, and output formatting.

## What Goes Here

System prompts define the essential infrastructure rules that apply to ALL translations:

- **CAT Tool Tag Preservation**: Rules for handling memoQ, Trados, CafeTran tags
- **Number Formatting**: Language-specific conventions for decimals, units, ranges
- **Output Format**: How to structure the translation output
- **Professional Context**: Disclaimer for medical/technical content
- **Quality Guidelines**: Accuracy, fluency, consistency requirements

## Why Layer 1 is Essential

These prompts ensure:
- 🎯 **Compatibility**: Translations work seamlessly with CAT tools
- 📊 **Consistency**: Number formatting matches target language conventions
- 🛡️ **Safety**: Proper context for medical/technical translations
- ⚡ **Reliability**: Clear output format for parsing and processing

## Files in This Folder

### Single Segment Translation (system prompt).md
Core infrastructure prompt for translating individual segments (Ctrl+T in the app).

**Used for:**
- Individual segment translation
- Context-aware translation with document reference
- Interactive translation workflow

**Contains:**
- CAT tool tag preservation rules (memoQ, Trados, CafeTran)
- Output format specifications
- Professional translation context
- Reference to Style Guide for number formatting (delegates to Layer 4)

## Customization

⚠️ **Edit with Caution**: These are infrastructure-level prompts. Changes here affect ALL translations.

**When you might customize:**
- Your CAT tool uses different tag formats
- You need specific number formatting rules
- You want different output structure
- You need custom quality guidelines

**Best Practices:**
- Test changes thoroughly before using in production
- Keep backup copies of original prompts
- Document your customizations
- Consider creating project-specific overrides in Layer 3 instead

## How Layer 1 Combines with Other Layers

Layer 1 (System Prompts) works as the foundation, with other layers adding specialization:

**Example Translation Stack:**
1. **Layer 1 (System)**: CAT tag rules, number formatting ← This layer
2. **Layer 2 (Domain)**: Medical translation expertise
3. **Layer 3 (Project)**: Client ABC's pharmaceutical project
4. **Layer 4 (Style)**: German style guide

Result: Expert medical translation for Client ABC with proper German formatting and CAT tool compatibility.

## File Format

System prompts are saved as Markdown (.md) for readability and ease of editing.

## Tips

1. **Start with Defaults**: Use the provided prompts as-is initially
2. **Test Changes**: Verify customizations work with your workflow
3. **Document Everything**: Note why you made changes
4. **Version Control**: Keep track of prompt versions
5. **Share Carefully**: Custom infrastructure prompts may not work for everyone

For more information, see the User Guide in the `docs/` folder.

