# Custom Instructions (Layer 3: Project Prompts)

Project prompts provide client-specific and project-specific instructions that customize how the AI translates for particular projects, clients, or document types.

## What Goes Here

Project prompts define project-level requirements:

- **Client Preferences**: Specific style requirements from clients
- **Project Context**: Document purpose, target audience, usage context
- **Terminology Guidelines**: Project-specific terms and preferred translations
- **Special Instructions**: Unique requirements for this project
- **Consistency Rules**: How to maintain consistency across documents
- **Output Requirements**: Specific formatting or structure needs

## How Project Prompts Work

Project prompts add a layer of customization on top of domain expertise:
- Tell the AI about the project context
- Define client-specific preferences
- Specify document-specific requirements
- Ensure consistency with previous work

## Difference from Domain Prompts

| **Domain Prompts (Layer 2)** | **Project Prompts (Layer 3)** |
|------------------------------|-------------------------------|
| Define AI's expertise | Define project requirements |
| "You are a legal expert" | "This is for Client ABC's contract" |
| Domain knowledge | Client preferences |
| Industry best practices | Project-specific rules |

## Example Project Prompts

This folder includes several useful project prompt templates:
- **Professional Tone & Style** - Ensures formal business language
- **Preserve Formatting & Layout** - Maintains original structure exactly
- **Prefer Translation Memory Matches** - Prioritizes TM consistency
- **Trados Tag Preservation** - Special handling for CAT tool tags

## File Formats

Project prompts can be saved as:
- **Markdown (.md)**: Recommended for readability and ease of editing
- **JSON (.json)**: For structured prompts with additional metadata

## Naming Convention

Use descriptive names that indicate the project or purpose:
- `Professional Tone & Style (project prompt).md`
- `Client ABC - User Manual (project prompt).md`
- `Prefer Translation Memory Matches (project prompt).md`

The "(project prompt)" suffix helps identify these as Layer 3 project prompts.

## Creating Your Own

Create custom project prompts for:
- Specific clients
- Ongoing projects
- Document types (user manuals, marketing materials, etc.)
- Team workflows

Use the "Create New Project Prompt" button in the Prompt Manager to get started with a template.

## Combining with Other Layers

Project prompts work best when combined with domain prompts and style guides:

**Example workflow:**
1. **Layer 2 (Domain)**: Medical Translation Specialist
2. **Layer 3 (Project)**: Client ABC - Clinical Trial Documentation ← This layer
3. **Layer 4 (Style)**: German style guide

Result: Expert medical translation customized for Client ABC's clinical trials using proper German formatting.

## Usage

Select a project prompt in the Prompt Manager → Project Prompts tab. You can use one project prompt alongside one domain prompt and one style guide for maximum customization.

## Tips

1. **Be Specific**: Clear instructions produce better results
2. **Include Context**: Help the AI understand the project's purpose
3. **Use Examples**: Show the AI what you want when possible
4. **Save Per Project**: Create a dedicated prompt for each major project
5. **Update as Needed**: Refine prompts based on client feedback
6. **Combine Strategically**: Pair with appropriate domain prompts and style guides

## Best Practices

- Keep project prompts focused on project-specific requirements
- Use domain prompts for general expertise
- Use style guides for formatting and conventions
- Don't duplicate information across layers
- Test combinations to find what works best

For more information, see the User Guide in the `docs/` folder.
