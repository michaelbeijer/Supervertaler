# ai_attachment_manager

**File:** `modules/ai_attachment_manager.py`
**Lines:** 343
**Classes:** 1
**Functions:** 0

---

## Module Description

AI Assistant Attachment Manager

Manages persistent storage of attached files for the AI Assistant.
Files are converted to markdown and stored with metadata.

---

## Classes

### `AttachmentManager`

**Line:** 16

Manages file attachments for AI Assistant conversations.

Features:
- Persistent storage of converted markdown files
- Metadata tracking (original name, path, type, size, date)
- Session-based organization
- Master index for quick lookup

#### Methods

##### `set_session()`

Set the current session ID

##### `attach_file()`

Save an attached file with metadata.

Args:
    original_path: Full path to original file
    markdown_content: Converted markdown content
    original_name: Original filename (optional, extracted from path if not provided)
    conversation_id: ID of conversation this file belongs to

Returns:
    file_id if successful, None otherwise

##### `get_file()`

Get file metadata and content.

Args:
    file_id: File ID

Returns:
    Dictionary with metadata and content, or None if not found

##### `remove_file()`

Remove an attached file.

Args:
    file_id: File ID to remove

Returns:
    True if successful, False otherwise

##### `list_session_files()`

List all files in a session.

Args:
    session_id: Session ID (uses current session if None)

Returns:
    List of file metadata dictionaries

##### `list_all_files()`

List all attached files across all sessions.

Returns:
    List of file metadata dictionaries

##### `get_stats()`

Get statistics about attachments.

Returns:
    Dictionary with stats (total_files, total_size, sessions, etc.)

##### `cleanup_empty_sessions()`

Remove sessions with no files


---

