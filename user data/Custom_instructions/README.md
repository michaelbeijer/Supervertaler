# Custom Instructions

This folder contains **Custom Instruction** prompt files that modify how the AI processes your translations.

## What are Custom Instructions?

Custom Instructions are user preferences and contextual guidelines that tell the AI **HOW** to translate, rather than **WHO** it should be (which is what System Prompts do).

### Difference from System Prompts:

| **System Prompts** | **Custom Instructions** |
|-------------------|------------------------|
| Define AI's role/expertise | Define user preferences/context |
| "You are a legal expert" | "Maintain professional tone" |
| Domain-specific knowledge | Formatting/style requirements |
| Translation specialization | Consistency preferences |

## Example Custom Instructions:

- **Professional Tone & Style** - Ensures formal business language
- **Preserve Formatting & Layout** - Maintains original structure exactly
- **Prefer Translation Memory Matches** - Prioritizes TM consistency
- **Avoid Contractions** - Uses full forms only
- **Gender-Neutral Language** - Uses inclusive terminology
- **Technical Abbreviations** - Expands acronyms on first use

## Creating Custom Instructions:

1. Open **Prompt Library** (📚 Browse Prompts button)
2. Click **Create New** button
3. Select **Type: custom_instruction**
4. Fill in:
   - **Name**: Short descriptive title
   - **Description**: What this instruction does
   - **Domain**: General, Business, Technical, etc.
   - **Translation Prompt**: Instructions for translation
   - **Proofreading Prompt**: Instructions for quality check
5. Choose **Private** if this is personal/confidential

## Using Custom Instructions:

Custom Instructions work **alongside** System Prompts:
- **System Prompt** defines the AI's expertise (e.g., "Legal Translation Specialist")
- **Custom Instruction** adds your preferences (e.g., "Professional Tone & Style")

You can apply one System Prompt + one Custom Instruction together for powerful, personalized translation workflows.

## Public vs Private:

- **Public** (`Custom_instructions/`): Shared via Git, visible to team
- **Private** (`Custom_instructions_private/`): Local only, excluded from Git sync

Choose **Private** for:
- Client-specific style guides
- Confidential terminology preferences
- Personal workflow adaptations

## File Format:

Custom Instruction files are JSON with this structure:

```json
{
    "name": "Your Instruction Name",
    "description": "What this instruction does",
    "domain": "General",
    "version": "1.0",
    "created": "2024-01-15",
    "translate_prompt": "Instructions for translation...",
    "proofread_prompt": "Instructions for proofreading..."
}
```

## Tips:

1. **Be Specific**: Clear instructions produce better results
2. **Use Examples**: Show the AI what you want when possible
3. **Test Iteratively**: Refine your instructions based on results
4. **Combine Wisely**: Pair complementary instructions with appropriate System Prompts
5. **Version Control**: Update version numbers when you modify instructions

## Questions?

See the main **USER_GUIDE.md** for comprehensive documentation on the Prompt Library feature.
