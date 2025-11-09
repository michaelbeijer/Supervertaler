# AI Assistant Enhancement Plan

## Overview
This document outlines the plan to enhance the AI Assistant with:
1. Persistent file attachment storage
2. UI for viewing/managing attached files
3. AI actions to interact with the prompt library

---

## Phase 1: File Attachment Persistence & Viewing

### Current Issues:
- Attached files are only stored in memory (`self.attached_files` list)
- Files are lost when the application closes
- Users cannot view/review attached files after uploading
- No visual list of attached files beyond a counter

### Solution:

#### 1.1 Storage Structure
Create dedicated storage folder:
```
user_data_private/
  AI_Assistant/
    attachments/
      {session_id}/
        {file_hash}.md        # Converted markdown content
        {file_hash}.meta.json # Metadata (original name, type, date)
    index.json               # Master index of all attachments
    conversations/
      {conversation_id}.json # Conversation history with references
```

#### 1.2 Metadata Format
```json
{
  "file_id": "abc123...",
  "original_name": "project_brief.pdf",
  "original_path": "/path/to/original.pdf",
  "file_type": ".pdf",
  "size_bytes": 123456,
  "size_chars": 45678,
  "attached_at": "2025-11-09T10:30:00",
  "conversation_id": "conv_xyz",
  "markdown_path": "attachments/conv_xyz/abc123.md"
}
```

#### 1.3 UI Enhancements
**Attached Files Panel** (expandable section in context sidebar):
```
📎 Attached Files (3)  [▼]
  ├─ 📄 project_brief.pdf (45 KB) - Nov 9, 10:30
  │  [👁 View] [❌ Remove]
  ├─ 📄 style_guide.docx (12 KB) - Nov 9, 10:32
  │  [👁 View] [❌ Remove]
  └─ 📄 glossary.txt (3 KB) - Nov 9, 10:35
     [👁 View] [❌ Remove]
```

**View Dialog:**
- Shows original filename
- Displays converted markdown in read-only editor
- Allows copying content
- Shows conversion metadata

---

## Phase 2: AI Assistant <-> Prompt Library Integration

### Current Issues:
- AI can see prompts exist but cannot access them
- AI cannot create new prompts
- AI cannot modify existing prompts
- No structured way for AI to perform actions

### Solution:

#### 2.1 Function Calling Interface
Implement a "tools" system similar to OpenAI's function calling:

**Available Tools:**
1. `list_prompts()` - List all prompts in library
2. `get_prompt(path)` - Get content of specific prompt
3. `create_prompt(name, content, folder)` - Create new prompt
4. `update_prompt(path, content)` - Update existing prompt
5. `search_prompts(query)` - Search prompts by content/name

#### 2.2 Implementation Approach

**Option A: Structured Response Parsing** (Simpler, works with all LLMs)
```python
# AI response format:
"""
Here's the prompt I created for you:

ACTION: create_prompt
NAME: Medical Translation - Cardiology
FOLDER: Medical
CONTENT:
You are translating medical cardiology documents...
END_ACTION

I've created a new prompt called "Medical Translation - Cardiology"...
"""
```

**Option B: JSON Function Calling** (Better, OpenAI/Claude/Gemini support)
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_prompt",
            "description": "Create a new prompt in the library",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "content": {"type": "string"},
                    "folder": {"type": "string"}
                }
            }
        }
    }
]
```

#### 2.3 System Prompt Enhancement
```
You are an AI assistant for Supervertaler, a professional translation tool.

AVAILABLE ACTIONS:
You can perform the following actions by using the ACTION format:

1. CREATE_PROMPT
   - Create a new translation prompt
   - Format: ACTION: create_prompt | NAME: ... | FOLDER: ... | CONTENT: ...

2. LIST_PROMPTS
   - List all available prompts
   - Format: ACTION: list_prompts

3. GET_PROMPT
   - Retrieve a specific prompt
   - Format: ACTION: get_prompt | PATH: ...

When a user asks you to create, modify, or manage prompts, use these actions.
```

---

## Phase 3: Implementation Steps

### Step 1: File Persistence (Priority: HIGH)
1. Create `AttachmentManager` class
2. Implement save/load methods
3. Create directory structure on first use
4. Modify `_attach_file()` to save to disk
5. Load attachments on startup

### Step 2: File Viewing UI (Priority: HIGH)
1. Create expandable attached files section
2. Add file list with view/remove buttons
3. Implement view dialog with markdown preview
4. Add remove confirmation dialog

### Step 3: AI Actions System (Priority: MEDIUM)
1. Define action interface/protocol
2. Implement response parser
3. Add actions to system prompt
4. Create action handlers
5. Test with real scenarios

---

## Implementation Files

### New Files:
- `modules/ai_attachment_manager.py` - File attachment persistence
- `modules/ai_actions.py` - AI action system and handlers
- `modules/ai_file_viewer_dialog.py` - File viewing dialog

### Modified Files:
- `modules/unified_prompt_manager_qt.py` - UI enhancements, integration
- `user_data_private/AI_Assistant/` - Storage directory (created)

---

## Testing Checklist

### File Attachment:
- [ ] Attach PDF, convert to markdown, save to disk
- [ ] Attach DOCX, convert to markdown, save to disk
- [ ] Attach TXT file directly
- [ ] View attached file in dialog
- [ ] Remove attached file
- [ ] Close and reopen app - attachments persist
- [ ] File appears in attached files list

### AI Actions:
- [ ] Ask AI to "list all prompts" - gets list
- [ ] Ask AI to "create a medical translation prompt" - prompt created
- [ ] Ask AI to "show me the X prompt" - prompt retrieved
- [ ] Ask AI to "update the X prompt" - prompt modified
- [ ] Verify created prompts appear in Prompt Library tab

---

## Timeline Estimate

- **Phase 1 (File Persistence & Viewing):** 2-3 hours
- **Phase 2 (AI Actions System):** 3-4 hours
- **Testing & Refinement:** 1-2 hours

**Total:** 6-9 hours development time

---

## Priority Recommendation

**Implement in this order:**
1. ✅ File persistence (most critical - prevents data loss)
2. ✅ File viewing UI (user-facing benefit)
3. ⏳ AI actions (nice-to-have, complex feature)

Would you like me to proceed with Phase 1 (file persistence) first?
