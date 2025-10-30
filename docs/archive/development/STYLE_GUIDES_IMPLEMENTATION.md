# Style Guides Feature - Implementation Guide

## Overview
The Style Guides feature enables users to manage and apply language-specific translation style guidelines within Supervertaler. This feature is designed to work seamlessly with the existing Prompt Assistant and uses a similar UI pattern.

## Architecture

### 1. Core Module: `style_guide_manager.py`
Located in: `modules/style_guide_manager.py`

**Class:** `StyleGuideLibrary`
- Manages loading, reading, and updating style guides
- Supports Markdown (.md) and text (.txt) file formats
- Methods:
  - `load_all_guides()` - Load all guides from the style guides directory
  - `get_guide(language)` - Get a specific style guide
  - `get_all_languages()` - Get list of all available languages
  - `update_guide(language, new_content)` - Update a guide's content
  - `append_to_guide(language, content)` - Append content to a guide
  - `append_to_all_guides(content)` - Append content to all guides
  - `create_guide(language, content)` - Create a new style guide
  - `export_guide(language, path)` - Export a guide to file
  - `import_guide(language, path, append)` - Import content from file

### 2. Default Style Guides
Located in: `user data/Style_Guides/`
- `Dutch.md` - Dutch translation guidelines
- `English.md` - English translation guidelines
- `Spanish.md` - Spanish translation guidelines
- `German.md` - German translation guidelines
- `French.md` - French translation guidelines

Each guide contains:
- Number formatting rules
- Units and measurements conventions
- Range and mathematical expression formats
- Comparison and symbol usage
- Terminology and style guidelines
- Additional language-specific notes

### 3. Configuration
- Added `Style_Guides` to `REQUIRED_FOLDERS` in `config_manager.py`
- Folder is automatically created during first-time setup
- Path resolution uses existing `get_subfolder_path()` method

### 4. Main Application Integration
- Import: `from modules.style_guide_manager import StyleGuideLibrary`
- Initialization in `Supervertaler_v3.7.1.py`:
  ```python
  style_guides_dir = get_user_data_path("Style_Guides")
  self.style_guide_library = StyleGuideLibrary(
      style_guides_dir=style_guides_dir,
      log_callback=self.log
  )
  ```

## UI Implementation (TODO)

### 5. Style Tab in Assistant Panel
The "Style" tab should be added to the assistant panel's notebook with:

**Left Panel:**
- List of available languages (scrollable)
- Similar styling to System Prompts/Custom Instructions tabs
- Columns: Language Name, Last Modified
- Support for selecting a language guide

**Right Panel - Content View:**
- Display content of selected style guide
- Scrollable text area
- Edit button for modifying guide
- Quick action buttons:
  - "📤 Export" - Save guide to file
  - "📥 Import" - Load content from file
  - "+" Add to Selected - For adding new text to selected guide
  - "⊕ Add to All" - For adding new text to all guides

**Right Panel - Chat Interface:**
- Chat history similar to Prompt Assistant
- Input field for user requests
- Support for commands like:
  - "Integrate this into Dutch guide"
  - "Add this to all guides"
  - "Review and suggest improvements"

### 6. AI Integration (TODO)
The Style tab's chat interface should:
1. Accept text input from user
2. Allow AI-assisted integration of content into guides
3. Provide options to:
   - Add text to individual guide
   - Add text to all guides
   - Suggest improvements to existing guides
   - Review guide for consistency

Example workflow:
```
User: "Integrate this into all style guides: [paste company style standards]"
AI: Processes and suggests how to integrate into each language guide
User: Approves changes
App: Updates all guides with new content
```

## Data Format

### Style Guide File Format
Plain text or Markdown files with the following structure:

```markdown
# [Language] Style Guide

## Category 1
- Item 1
- Item 2

## Category 2
- Item 3
- Item 4
```

### Metadata Storage
- File modification time is tracked
- Created time is captured on load
- Language name derived from filename (Dutch.md → "Dutch")

## Usage Examples

### Loading and Accessing Guides
```python
# Initialize
guides = StyleGuideLibrary("path/to/Style_Guides")
guides.load_all_guides()

# Get all languages
languages = guides.get_all_languages()  # ['Dutch', 'English', ...]

# Get specific guide
dutch_guide = guides.get_guide('Dutch')
print(dutch_guide['content'])

# Update guide
new_content = "Updated style information..."
guides.update_guide('Dutch', new_content)
```

### Batch Operations
```python
# Add guidelines to all languages
additional_text = "Company-specific formatting rules..."
guides.append_to_all_guides(additional_text)

# Export a guide
guides.export_guide('Dutch', '/path/to/export/Dutch_Styles.md')

# Import from file
guides.import_guide('Dutch', '/path/to/import/dutch_rules.txt', append=True)
```

## Integration with Prompt Assistant

The Style Guides feature can work in conjunction with the Prompt Assistant:
- Both use similar UI patterns (list on left, content on right)
- Both support AI-powered improvements
- Both are accessible from the Assistant panel

## File Organization

```
Supervertaler/
├── modules/
│   ├── style_guide_manager.py    [NEW] Core style guide management
│   ├── prompt_library.py          [EXISTING] Prompt management
│   ├── prompt_assistant.py        [EXISTING] AI prompt improvements
│   └── ...
├── user data/
│   ├── Style_Guides/             [NEW] User's style guides
│   │   ├── Dutch.md
│   │   ├── English.md
│   │   ├── Spanish.md
│   │   ├── German.md
│   │   └── French.md
│   ├── Prompt_Library/
│   └── Translation_Resources/
└── Supervertaler_v3.7.1.py       [UPDATED] Added StyleGuideLibrary import and init
```

## Next Steps

1. **UI Implementation:**
   - Add "Style" tab to assistant panel notebook
   - Create style guide list widget
   - Create style guide content view and edit interface

2. **Chat Integration:**
   - Add chat input field for style guide requests
   - Connect to prompt assistant for AI processing
   - Implement request handlers for:
     - Individual guide updates
     - Batch guide updates
     - Style analysis and suggestions

3. **Testing:**
   - Test loading default guides
   - Test updating individual guides
   - Test batch updates
   - Test import/export functionality
   - Test UI interactions and chat interface

4. **Future Enhancements:**
   - Version history for style guides
   - Style guide templates library
   - Collaborative style guide sharing
   - Style guide comparison across languages
   - Auto-suggestion of style inconsistencies in translations
