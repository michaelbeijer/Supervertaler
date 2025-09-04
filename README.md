# Supervertaler (v2.0.0)
Multicontextual AI-powered Translator &amp; Proofreader (currently supports Gemini, Claude and OpenAI models via their APIs)

![supervertaler_screenshot_v2 0 0_with_source code](https://github.com/user-attachments/assets/7ec606a5-9e62-47ba-9136-b85b1e4ab9b5)

**Supervertaler** can operate in two modes: TRANSLATE or PROOFREAD. It leverages multiple context sources for enhanced accuracy:

## GENERAL FEATURES
### Multiple context sources:
- **Full document content**: The AI considers the entire document when translating each sentence, for better contextual understanding.
- **Images**: If a "Drawings Image Folder" is provided, images (e.g., "Fig 1A.png") are shown to the AI when the text references them, aiding in visual context.
- **Translation Memory** (.txt/.tmx): For exact matches before AI processing; particularly  useful in ongoing projects.
- **Tracked-changes**: Previous editing decisions (in the target language) can be imported from memoQ-generated bilingual DOCX files and passed to the AIs as another source of valuable context. 
- **Custom instructions** text field: To be added to system prompt on-the-fly, for adding important context about the document or any other instructions.

### Other features:

- Multiple AI Providers: Choose between Claude (Anthropic), Gemini (Google), and ChatGPT (OpenAI) models
- System prompt (partially) editable in python code
- Chunking: System breaks large documents into manageable chunks for the AI.

## MODE-SPECIFIC FEATURES

### Translate mode:
- Function: Translates source text to the target language.
- TM Usage: Uses a Translation Memory (.txt/.tmx) for exact matches before AI processing.
- Input Format: Text file with one source text per line.
- Output Format: "source_text{tab}translated_text".

### Proofread mode:
- Function: Reviews and revises existing target text against the source text.
- TM Usage: TM is bypassed in this mode; all segments are sent to the AI for review.
- Input Format: Text file with "source_text{tab}EXISTING_target_text{tab}[optional_original_comment]". (3rd column is optional).
- Output Format: "source_text{tab}REVISED_target_text{tab}[comments_including_AI_changes_and_original]".

Contact me at info@michaelbeijer.co.uk for further info. 
