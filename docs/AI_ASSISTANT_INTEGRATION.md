# AI Assistant Integration Guide

## Overview

The AI Assistant in the Prompt Manager can access the current project and document information from the main Supervertaler application.

## Integration Steps

### 1. Pass Parent App Reference

When creating the UnifiedPromptManagerQt instance, ensure you pass a reference to the main application:

```python
# In Supervertaler_Qt.py
self.prompt_manager = UnifiedPromptManagerQt(
    parent_app=self,  # Pass self reference
    standalone=False
)
```

### 2. Required Attributes in Main App

The AI Assistant will look for these attributes in the parent application:

**Required for Document Display:**
- `current_project` - The currently active Project object (or None)
- `current_document_path` - Path to the current document file (optional)

**Optional Project Attributes:**
- `project.name` - Project name
- `project.source_file` - Source document path
- `project.source_lang` - Source language code
- `project.target_lang` - Target language code

**Optional for Document Content Access:**
- `segments` - List of segment objects with `.source` attribute
- `project.source_segments` - List of source text segments (strings or objects with `.text`)

**For Full Segment-Level Access:**
When `current_project.segments` is available (list of Segment objects), the AI Assistant gains:
- Total segment count and translation progress statistics
- Access to first 10 segments in context (automatically)
- Ability to query specific segments by ID using AI actions
- Full segment properties: id, source, target, status, type, notes, match_percent, etc.

The AI Assistant will try to access document content in this order:
1. `project.segments` - Full segment objects (PREFERRED - enables segment-level operations)
2. `parent_app.segments` - Currently loaded segments
3. `project.source_segments` - Project's source text segments
4. Cached markdown conversion (from previous access)
5. Direct file conversion with `markitdown` - Converts DOCX, PDF, PPTX, etc. to markdown

When method 5 is used, the markdown version is:
- Cached in memory for the session
- **Saved to disk** at `user_data_private/AI_Assistant/current_document/`
- Available for the user to access and use elsewhere

**Required for LLM Integration:**
- `current_provider` - LLM provider name ('openai', 'anthropic', 'google')
- `current_model` - Model name (e.g., 'gpt-4', 'claude-3-5-sonnet-20241022')

### 3. Call refresh_context() When Project Changes

To keep the AI Assistant's context up to date, call the refresh method whenever the project or document changes:

```python
# In Supervertaler_Qt.py

def load_project(self, project_id):
    """Load a project"""
    # ... load project code ...
    self.current_project = project

    # Update AI Assistant context
    if hasattr(self, 'prompt_manager'):
        self.prompt_manager.refresh_context()

def open_document(self, file_path):
    """Open a document"""
    self.current_document_path = file_path

    # Update AI Assistant context
    if hasattr(self, 'prompt_manager'):
        self.prompt_manager.refresh_context()
```

### 4. Automatic Updates

The AI Assistant will automatically update its context when:
- User switches to the "✨ AI Assistant" tab
- The `refresh_context()` method is called

## What Gets Displayed

### In the Context Sidebar

**📄 Current Document Section:**
```
Project Name
document.docx
```

### In the AI System Prompt

The AI receives this information:
```
AVAILABLE RESOURCES:
- Current Project: Project Name
- Current Document: document.docx
- Language Pair: en → nl

CURRENT DOCUMENT CONTENT (first 3000 characters):
[First 50 segments of the document...]

- Prompt Library: 38 prompts
- Attached Files: 2 files
```

**Note:** Document content is included via multiple methods, with segment-level access being preferred.

### With Segment Information

When `project.segments` is available, the AI receives detailed segment statistics:
```
AVAILABLE RESOURCES:
- Current Project: Medical Translation Project
- Current Document: patient_info.docx
- Language Pair: en → nl

DOCUMENT SEGMENTS:
- Total segments: 150
- Translated: 85/150

First 10 segments (use segment numbers to reference specific segments):

  Segment 1:
    Source: Patient demographics and medical history
    Target: Patiëntdemografie en medische geschiedenis
    Status: confirmed

  Segment 2:
    Source: The patient is a 45-year-old male...
    Target: De patiënt is een 45-jarige man...
    Status: confirmed

  ... and 140 more segments

NOTE: You can access individual segments by their segment number.
Use get_segment_info action to retrieve details of specific segments.
```

The AI can then:
- Answer "How many segments are in this document?" → "150 segments"
- Answer "What is segment 5?" → Uses `get_segment_info` action with `segment_id: 5`
- Answer "Show me segments 10-15" → Uses `get_segment_info` action with range

## Example Implementation

```python
class SupervertalerQt(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize project state
        self.current_project = None
        self.current_document_path = None
        self.current_provider = 'openai'
        self.current_model = 'gpt-4'

        # Create Prompt Manager
        self.prompt_manager = UnifiedPromptManagerQt(
            parent_app=self,
            standalone=False
        )

        # ... rest of initialization ...

    def on_project_changed(self):
        """Called when project is loaded or changed"""
        # Update context
        if hasattr(self, 'prompt_manager'):
            self.prompt_manager.refresh_context()

    def on_document_opened(self, file_path):
        """Called when a document is opened"""
        self.current_document_path = file_path

        # Update context
        if hasattr(self, 'prompt_manager'):
            self.prompt_manager.refresh_context()
```

## Markdown Document Conversion

The AI Assistant can convert documents to markdown in two ways:

### Automatic Conversion (Optional)

When **enabled in Settings → General → AI Assistant Settings**, Supervertaler will automatically convert every imported document to markdown. This happens immediately after document import.

To enable:
1. Open Settings (⚙️ button)
2. Go to "General" tab
3. Check "Auto-generate markdown for imported documents"
4. Click "Save General Settings"

### On-Demand Conversion

When auto-conversion is disabled, the AI Assistant will convert documents on-demand when it needs document content and segments aren't available.

Both methods:

1. **Convert to markdown** using `markitdown`
2. **Save to disk** at: `user_data_private/AI_Assistant/current_document/`
3. **Create metadata** file with conversion information

**File Structure:**
```
user_data_private/
  AI_Assistant/
    current_document/
      document_name.md          # Converted markdown
      document_name.meta.json   # Metadata (original file, conversion time, etc.)
```

**Metadata Example:**
```json
{
  "original_file": "C:/path/to/document.docx",
  "original_name": "document.docx",
  "converted_at": "2025-11-09T15:30:00",
  "markdown_file": "user_data_private/AI_Assistant/current_document/document.md",
  "size_chars": 45678
}
```

**Benefits:**
- Users can access the markdown version of their documents
- Useful for text processing, analysis, or reference
- Conversion is cached - only done once per document
- Cache is cleared when document/project changes

## Segment-Level AI Actions

The AI Assistant can perform operations on segments using AI actions. These actions are automatically available when `parent_app.current_project.segments` is accessible.

### Available Segment Actions

#### 1. get_segment_count
Get total segment count and translation progress.

**Example AI response:**
```
Let me check the segment count for you.

ACTION:get_segment_count
PARAMS:{}

The document has 150 segments total, with 85 already translated.
```

**Returns:**
```json
{
  "total_segments": 150,
  "translated": 85,
  "untranslated": 65
}
```

#### 2. get_segment_info
Get detailed information about specific segment(s).

**Example - Single segment:**
```
ACTION:get_segment_info
PARAMS:{"segment_id": 5}
```

**Example - Multiple segments:**
```
ACTION:get_segment_info
PARAMS:{"segment_ids": [1, 5, 10]}
```

**Example - Range of segments:**
```
ACTION:get_segment_info
PARAMS:{"start_id": 10, "end_id": 15}
```

**Returns:**
```json
{
  "segments": [
    {
      "id": 5,
      "source": "The patient is a 45-year-old male...",
      "target": "De patiënt is een 45-jarige man...",
      "status": "confirmed",
      "type": "para",
      "notes": "",
      "match_percent": 95,
      "locked": false,
      "paragraph_id": 2,
      "style": "Normal",
      "document_position": 5,
      "is_table_cell": false
    }
  ],
  "count": 1
}
```

### Use Cases

The AI can help users with segment-level tasks:

**User:** "How many segments are in this document?"
**AI:** Executes `get_segment_count` → "The document has 150 segments."

**User:** "What's the text in segment 42?"
**AI:** Executes `get_segment_info` with `segment_id: 42` → Shows source and target text.

**User:** "Show me segments 10 through 15"
**AI:** Executes `get_segment_info` with `start_id: 10, end_id: 15` → Lists the segments.

**User:** "What's the translation progress?"
**AI:** Executes `get_segment_count` → "85 out of 150 segments are translated (57%)."

## Troubleshooting

**Problem:** Current Document shows "No document loaded"

**Solutions:**
1. Check that `parent_app.current_project` is set and not None
2. Check that either `parent_app.current_document_path` or `project.source_file` is set
3. Call `prompt_manager.refresh_context()` after loading a project/document

**Problem:** AI doesn't know about the current project

**Solutions:**
1. Verify the parent_app reference is passed correctly
2. Check that project attributes (name, source_lang, target_lang) are set
3. The context updates automatically when switching to AI Assistant tab

**Problem:** Document conversion fails

**Solutions:**
1. Check that `markitdown` is installed
2. Verify the document file exists and is accessible
3. Check console/log for conversion errors
4. Try providing segments instead (`parent_app.segments`)

**Problem:** AI can't answer segment count questions

**Solutions:**
1. Verify that `parent_app.current_project.segments` is populated with Segment objects
2. Check that segments have the required attributes (id, source, target, status, etc.)
3. Call `prompt_manager.refresh_context()` after loading segments
4. Check that the AI Action System was initialized with `parent_app` parameter

**Problem:** Segment actions return "No project currently loaded"

**Solutions:**
1. Ensure `parent_app.current_project` is set before accessing segments
2. The project must have a `segments` attribute (list of Segment objects)
3. Verify the parent_app reference is passed correctly to UnifiedPromptManagerQt

## Testing

To test the integration:

1. Load a project in Supervertaler
2. Open the Prompt Manager
3. Switch to the "✨ AI Assistant" tab
4. Check the "📄 Current Document" section in the sidebar
5. Ask the AI: "What document am I currently working on?"
6. The AI should know the project name and document name

### Testing Segment Access

To test segment-level features:

1. Load a project with segments in Supervertaler
2. Open the Prompt Manager and switch to AI Assistant tab
3. Ask: "How many segments are in this document?"
4. The AI should execute `get_segment_count` and report the total
5. Ask: "What is segment 5?"
6. The AI should execute `get_segment_info` and show the segment details
7. Ask: "Show me segments 10 through 15"
8. The AI should retrieve and display the range

## Notes

- The context update is automatic when switching to the AI Assistant tab
- No need to manually refresh unless you want immediate updates
- All project information is optional - the AI Assistant works without it
- The system gracefully handles missing attributes
- **Segment-level access** requires `current_project.segments` to be a list of Segment objects
- AI actions for segments are automatically available when segments are present
- The AI receives the first 10 segments in its context automatically for quick reference
