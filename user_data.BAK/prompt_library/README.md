# Prompt Library

This folder contains all prompt-related files that control how the AI translates your content. The Prompt Library uses a 4-layer architecture to provide maximum flexibility and precision.

## 📁 Folder Structure

### `1_System_Prompts/`
**Layer 1: Infrastructure Prompts** - Core rules for CAT tool compatibility and output formatting

- CAT tool tag preservation (memoQ, Trados, CafeTran)
- Output format specifications
- Professional translation context
- Reference to Style Guide for formatting conventions

These prompts are foundational and apply to ALL translations. They ensure compatibility with CAT tools and maintain quality standards.

### `2_Domain_Prompts/`
**Layer 2: Domain Expertise** - Specialized knowledge for different industries and fields

- Medical translations
- Legal documents
- Technical manuals
- Marketing content
- Financial documents
- Patent translations
- And more...

These prompts give the AI expert knowledge in specific domains to improve translation quality.

### `3_Project_Prompts/`
**Layer 3: Project/Client Instructions** - Client-specific and project-specific requirements

- Project-specific terminology
- Client style preferences
- Document-specific requirements
- Special handling rules
- Consistency preferences

Use these to customize translations for specific projects or clients.

### `4_Style_Guides/`
**Layer 4: Language Conventions** - Language-specific formatting and style rules

- Number formatting (1,000 vs 1.000)
- Date formats
- Unit conventions
- Punctuation rules
- Tone and register

Style guides ensure consistency across languages and meet regional expectations.

## 🎯 How the 4-Layer Architecture Works

All four layers combine to create the perfect translation:

1. **Layer 1 (Infrastructure)** - "Preserve CAT tags, use proper number formatting"
2. **Layer 2 (Domain)** - "I'm a medical translation expert"
3. **Layer 3 (Project)** - "This is for Client ABC's user manual"
4. **Layer 4 (Style)** - "Use British English conventions"

**Result:** Expert medical translation with CAT tool compatibility, tailored to the client using proper British English formatting.

## 📝 File Formats

- **Markdown (.md)**: Human-readable format, recommended for most prompts
- **JSON (.json)**: Structured format for complex prompts with metadata

## 🚀 Getting Started

1. Browse the example prompts in each numbered folder
2. Select prompts in the Prompt Manager tab
3. Combine multiple layers for best results
4. Create your own custom prompts as needed

## 💡 Tips

- **Layer 1** is usually left as default (infrastructure)
- **Layer 2** should match your content type (medical, legal, etc.)
- **Layer 3** can be project/client-specific
- **Layer 4** should match your target language conventions

For more information, see the User Guide in the `docs/` folder.
