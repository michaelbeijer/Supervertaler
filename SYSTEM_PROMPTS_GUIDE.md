# System Prompts & Custom Instructions Guide

## Overview
Supervertaler v2.5.0 separates global AI behavior (System Prompts) from project-specific guidance (Custom Instructions), giving you precise control over translation quality while maintaining flexibility for different projects.

## Architecture

### How Prompts Combine

```
┌─────────────────────────────────────────────────────────┐
│                    FINAL AI PROMPT                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. SYSTEM PROMPT (Global AI Behavior)                 │
│     └─ Defines: How to translate, output format,       │
│        quality standards, general rules                 │
│     └─ Variables replaced:                             │
│        {{SOURCE_LANGUAGE}} → English                   │
│        {{TARGET_LANGUAGE}} → Russian                   │
│        {{SOURCE_TEXT}} → [current segment]             │
│                                                         │
│  2. SPECIAL INSTRUCTIONS (if provided)                 │
│     └─ Adds: Project terminology, style preferences,   │
│        formatting rules, context                        │
│                                                         │
│  3. SENT TO AI → Translation Generated                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## System Prompts Tab (🌐 Global AI Behavior)

### Purpose
Define **how the AI should behave** across all projects. This is your foundation.

### Two Sub-tabs

#### 🌐 Translation
Controls AI behavior when translating new text.

**Default Prompt Includes**:
- Context awareness instructions
- Image and figure handling
- Output format requirements (numbered segments)
- Quality guidelines
- Special character preservation

**When to Edit**:
- Changing fundamental translation approach
- Modifying output format requirements
- Adding/removing general quality rules
- Updating variable placeholders

**Variables Available**:
- `{{SOURCE_LANGUAGE}}` - Replaced with project source language
- `{{TARGET_LANGUAGE}}` - Replaced with project target language
- `{{SOURCE_TEXT}}` - Replaced with current segment text

#### ✏️ Proofreading
Controls AI behavior when proofreading/reviewing translations.

**Default Prompt Includes**:
- Review approach guidelines
- Change tracking requirements
- Output format (original + corrected + summary)
- Quality checks to perform

**When to Edit**:
- Changing review methodology
- Modifying output format
- Adding specific quality checks

### Controls

**💾 Save**
- Saves current prompt in memory
- Applies to all future translations
- Persists until app restart (future: save to config)

**🔄 Reset to Default**
- Restores detailed prompts from v2.4.0
- Use if you've made changes and want to start over

**👁️ Preview**
- Shows prompt with variables replaced using current segment
- Helps verify variable placement and prompt structure

## Custom Instructions Tab (📋 Project-Specific)

### Purpose
Add **specialized guidance for THIS project** without changing global settings.

### Visual Distinction
- **Orange header** (vs blue for System Prompts)
- Labeled "Project-Specific" (vs "Global AI Behavior")
- Explanation box showing how it combines with system prompts

### Template Structure

```markdown
# Custom Translation Instructions for This Project

## 1. Style Guidelines
- Tone and formality: [e.g., formal, casual, technical]
- Register: [e.g., academic, conversational, business]
- Preferred terminology: [specific terms to use/avoid]

## 2. Project-Specific Terminology
- [Term 1]: [preferred translation]
- [Term 2]: [preferred translation]
- [Technical term]: [do not translate]

## 3. Formatting Rules
- Capitalization: [specific rules]
- Punctuation: [preferences]
- Number formatting: [standards]
- Date format: [e.g., DD/MM/YYYY]

## 4. Additional Context
- Target audience: [who will read this]
- Document purpose: [why it's being translated]
- Special considerations: [anything unusual]
```

### When to Use Custom Instructions

**Perfect For**:
- ✅ Client-specific terminology preferences
- ✅ Document-specific style requirements
- ✅ Target audience considerations
- ✅ Domain-specific vocabulary
- ✅ Formatting preferences unique to this project
- ✅ Background context that helps translation quality

**Not Ideal For**:
- ❌ General translation quality rules (use System Prompts)
- ❌ Output format requirements (use System Prompts)
- ❌ AI behavior instructions (use System Prompts)

### Controls

**💾 Save to Project**
- Saves instructions to project JSON file
- Automatically loads when project is opened
- Unique to this project only

**🔄 Reload Template**
- Restores the template structure
- Use if you want to start over

### Example Custom Instructions

#### Legal Document Translation
```markdown
# Custom Translation Instructions for This Project

## 1. Style Guidelines
- Tone: Formal and precise
- Register: Legal/professional
- Preferred terminology: Use standard legal terms from Russian Civil Code

## 2. Project-Specific Terminology
- "Agreement": "Соглашение" (not "Договор")
- "Party": "Сторона" (capitalize in legal context)
- "Hereby": "Настоящим"
- Force majeure: Keep in English (common in Russian legal texts)

## 3. Formatting Rules
- Capitalization: All section headers in Title Case
- Dates: DD.MM.YYYY format
- Numbers: Use spaces as thousands separator (1 000 000)

## 4. Additional Context
- Target audience: Russian lawyers and business executives
- Document purpose: Bilateral investment treaty
- Special considerations: Must align with existing treaty terminology
```

#### Marketing Brochure
```markdown
# Custom Translation Instructions for This Project

## 1. Style Guidelines
- Tone: Friendly, enthusiastic, persuasive
- Register: Conversational but professional
- Preferred terminology: Use consumer-friendly language, avoid jargon

## 2. Project-Specific Terminology
- Brand name "TechFlow": Keep in English
- "Smart home": "Умный дом"
- "AI-powered": "На основе ИИ" (not "искусственный интеллект")

## 3. Formatting Rules
- Capitalization: Product names always capitalized
- Exclamation marks: OK to use for emphasis (matching source)
- Emojis: Preserve all emojis from source

## 4. Additional Context
- Target audience: Tech-savvy consumers aged 25-45
- Document purpose: Product launch marketing
- Special considerations: Energetic tone is crucial, creativity encouraged
```

## Global Preview Button (🧪)

### Location
Always visible in Translation Workspace header:
```
┌────────────────────────────────────────────────────────┐
│ Translation Workspace  [🧪 Preview Prompt]  [⊞ Stacked] │
└────────────────────────────────────────────────────────┘
```

### Purpose
Show the **EXACT prompt** that will be sent to the AI, including:
- System prompt with variables replaced
- Custom instructions appended (if provided)
- Current segment text highlighted

### How to Use

1. **Select a segment** in the translation grid
2. **Click 🧪 Preview Prompt** button
3. **Review the dialog**:
   - Language pair and segment number
   - Composition breakdown (character counts)
   - Full combined prompt
   - Source text highlighted in yellow
4. **Copy to clipboard** if needed (for testing in other tools)

### Preview Dialog

```
┌──────────────────────────────────────────────────────┐
│ 🧪 Combined Translation Prompt Preview               │
├──────────────────────────────────────────────────────┤
│ Language Pair: English → Russian | Segment #5        │
│                                                       │
│ Composition:                                         │
│ • System Prompt: 1,247 characters                   │
│ • Custom Instructions: 412 characters                │
│ • Total: 1,659 characters                           │
│                                                       │
│ ─────────────────────────────────────────────────── │
│                                                       │
│ You are an expert translator specializing in        │
│ English to Russian translation. Your goal is to      │
│ provide high-quality, contextually appropriate       │
│ translations...                                      │
│                                                       │
│ [Full system prompt with variables replaced]         │
│                                                       │
│ **SPECIAL INSTRUCTIONS FOR THIS PROJECT:**          │
│                                                       │
│ ## 1. Style Guidelines                              │
│ - Tone: Formal and precise                          │
│ ...                                                  │
│                                                       │
│ Source Text: The Contracting Parties shall promote  │
│ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  │
│ [Highlighted in yellow background]                   │
│                                                       │
│ ─────────────────────────────────────────────────── │
│                        [📋 Copy] [Close]             │
└──────────────────────────────────────────────────────┘
```

### Benefits

**For Testing**:
- Verify custom instructions are combining correctly
- Check variable replacement
- Ensure no conflicts between system and custom prompts

**For Optimization**:
- See exact character counts (helps manage API costs)
- Identify unnecessarily long sections
- Balance detail vs. conciseness

**For Learning**:
- Understand how prompt engineering works
- See what the AI actually receives
- Improve your custom instructions based on results

**For Debugging**:
- Diagnose translation quality issues
- Verify terminology preferences are included
- Check if context is sufficient

## Best Practices

### System Prompts

**DO**:
- ✅ Keep general and reusable across projects
- ✅ Focus on AI behavior and output format
- ✅ Use variables for flexibility
- ✅ Test changes with preview before saving
- ✅ Document any customizations you make

**DON'T**:
- ❌ Include project-specific terminology
- ❌ Add client names or document details
- ❌ Change format requirements per project
- ❌ Override for temporary needs (use Custom Instructions)

### Custom Instructions

**DO**:
- ✅ Be specific about project requirements
- ✅ List key terminology with translations
- ✅ Provide context about target audience
- ✅ Include formatting preferences
- ✅ Update as project requirements evolve

**DON'T**:
- ❌ Duplicate information from system prompts
- ❌ Include general translation rules
- ❌ Write extremely long instructions (AI may miss details)
- ❌ Forget to save to project

### Testing Workflow

1. **Edit system prompt** (if needed) → Preview → Save
2. **Add custom instructions** → Save to Project
3. **Select a test segment** → Click 🧪 Preview Prompt
4. **Review combined prompt** → Verify it makes sense
5. **Translate segment** → Check quality
6. **Adjust instructions if needed** → Repeat

## Troubleshooting

### Problem: Custom instructions not appearing in translation
**Solution**: 
- Make sure to click "💾 Save to Project"
- Verify project is loaded (check Projects tab)
- Use 🧪 Preview Prompt to verify they're included

### Problem: Variables not replaced in preview
**Solution**:
- Ensure you have a segment selected
- Check variable spelling: {{SOURCE_LANGUAGE}}, {{TARGET_LANGUAGE}}, {{SOURCE_TEXT}}
- Variables are case-sensitive

### Problem: Translation quality not improving
**Solution**:
- Use 🧪 Preview Prompt to verify instructions are clear
- Check if custom instructions conflict with system prompt
- Try being more specific in terminology section
- Consider if AI provider supports your prompt length

### Problem: Lost custom instructions after closing app
**Solution**:
- Always click "💾 Save to Project" before closing
- Custom instructions save with project JSON file
- If project not saved, instructions are lost

## Technical Details

### Storage

**System Prompts**:
- Stored in memory (self.current_translate_prompt, self.current_proofread_prompt)
- Reset to defaults from lines ~380-415 in code
- Future: Will save to user config file

**Custom Instructions**:
- Saved in project JSON file under "custom_instructions" key
- Loaded automatically when project opens
- Unique per project

### Character Limits

**Recommended**:
- System Prompt: 1,000-2,000 characters
- Custom Instructions: 200-800 characters
- Combined Total: Under 3,000 characters for most AI providers

**API Limits** (approximate):
- Gemini: ~30,000 characters (prompt + response)
- OpenAI GPT-4: ~8,000 tokens (~32,000 characters)
- Claude: ~100,000 tokens

### Variables

Currently supported:
- `{{SOURCE_LANGUAGE}}` - Project source language name
- `{{TARGET_LANGUAGE}}` - Project target language name
- `{{SOURCE_TEXT}}` - Current segment text

Future additions:
- `{{DOCUMENT_TYPE}}`
- `{{TARGET_AUDIENCE}}`
- `{{FORMALITY_LEVEL}}`

## Examples by Project Type

### Technical Documentation
**System Prompt**: Standard (detailed, context-aware)
**Custom Instructions**:
```markdown
## Terminology
- "API": Keep in English
- "Database": "База данных"
- Code samples: Preserve exactly, do not translate

## Style
- Tone: Technical but clear
- Use imperative mood for instructions
```

### Literary Translation
**System Prompt**: Standard with creativity emphasis
**Custom Instructions**:
```markdown
## Style
- Preserve author's voice and rhythm
- Maintain metaphors and imagery
- Cultural references: Adapt for Russian readers

## Context
- Genre: Contemporary fiction
- Target audience: Adult readers
- Tone: Introspective, literary
```

### Business Email
**System Prompt**: Standard
**Custom Instructions**:
```markdown
## Style
- Tone: Professional but warm
- Register: Business formal
- Salutations: "Уважаемый/ая" for formal, "Здравствуйте" for semi-formal

## Formatting
- Preserve email structure
- Keep signatures in original language if English names
```

### Medical Device Manual
**System Prompt**: Standard with precision emphasis
**Custom Instructions**:
```markdown
## Terminology (from client glossary)
- "Surgical instrument": "Хирургический инструмент"
- "Sterilization": "Стерилизация"
- Brand names: Keep original

## Compliance
- Must align with Russian medical device regulations
- Safety warnings: Translate literally, no interpretation
- Measurements: Convert to metric if source is imperial

## Context
- Regulatory submission to Russian health authority
- Zero tolerance for errors
```

## Keyboard Shortcuts (Future)

Planned shortcuts:
- `Ctrl+Shift+P` - Open Preview Prompt
- `Ctrl+Shift+S` - Save Custom Instructions
- `Ctrl+Shift+R` - Reset System Prompt

## Summary

| Aspect | System Prompts | Custom Instructions |
|--------|---------------|---------------------|
| **Scope** | All projects | Single project |
| **Purpose** | AI behavior & format | Project context & preferences |
| **Update Frequency** | Rarely | Per project |
| **Storage** | Memory (future: config) | Project JSON file |
| **Header Color** | Blue | Orange |
| **Variables** | Yes ({{...}}) | No |
| **Preview** | Per sub-tab | Global button only |

**Key Insight**: System Prompts teach the AI **how to translate**. Custom Instructions tell it **what to know about this project**.

---

*For more information, see SESSION_SUMMARY_2025-10-05_EOD.md*
