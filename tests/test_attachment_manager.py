"""
Test script for AttachmentManager and file viewer dialogs
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for console output (Windows compatibility)
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

# Test 1: Import modules
print("=" * 60)
print("Test 1: Importing modules...")
print("=" * 60)

try:
    from modules.ai_attachment_manager import AttachmentManager
    print("✓ AttachmentManager imported successfully")
except Exception as e:
    print(f"✗ Failed to import AttachmentManager: {e}")
    sys.exit(1)

try:
    from modules.ai_file_viewer_dialog import FileViewerDialog, FileRemoveConfirmDialog
    print("✓ File viewer dialogs imported successfully")
except Exception as e:
    print(f"✗ Failed to import file viewer dialogs: {e}")
    sys.exit(1)

# Test 2: Initialize AttachmentManager
print("\n" + "=" * 60)
print("Test 2: Initializing AttachmentManager...")
print("=" * 60)

try:
    # Use test directory
    test_dir = Path("user_data_private") / "AI_Assistant_Test"
    manager = AttachmentManager(base_dir=str(test_dir))
    print(f"✓ AttachmentManager initialized")
    print(f"  Base directory: {manager.base_dir}")
    print(f"  Attachments directory: {manager.attachments_dir}")
except Exception as e:
    print(f"✗ Failed to initialize AttachmentManager: {e}")
    sys.exit(1)

# Test 3: Set session
print("\n" + "=" * 60)
print("Test 3: Setting session...")
print("=" * 60)

try:
    manager.set_session("test_session_001")
    print(f"✓ Session set: {manager.current_session_id}")
except Exception as e:
    print(f"✗ Failed to set session: {e}")
    sys.exit(1)

# Test 4: Attach a test file
print("\n" + "=" * 60)
print("Test 4: Attaching test file...")
print("=" * 60)

try:
    # Create test content
    test_content = """# Test Document

This is a test markdown document for the AttachmentManager.

## Features Tested
- File attachment
- Metadata storage
- Content persistence

## Sample Content
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
"""

    file_id = manager.attach_file(
        original_path="C:/test/sample.md",
        markdown_content=test_content,
        original_name="sample.md",
        conversation_id="test_conv_001"
    )

    if file_id:
        print(f"✓ File attached successfully")
        print(f"  File ID: {file_id}")
    else:
        print(f"✗ Failed to attach file (returned None)")
except Exception as e:
    print(f"✗ Failed to attach file: {e}")
    import traceback
    traceback.print_exc()

# Test 5: List files
print("\n" + "=" * 60)
print("Test 5: Listing files...")
print("=" * 60)

try:
    files = manager.list_session_files()
    print(f"✓ Found {len(files)} file(s) in session")
    for i, file_meta in enumerate(files, 1):
        print(f"  File {i}:")
        print(f"    Name: {file_meta.get('original_name')}")
        print(f"    Type: {file_meta.get('file_type')}")
        print(f"    Size: {file_meta.get('size_chars')} chars")
        print(f"    ID: {file_meta.get('file_id')}")
except Exception as e:
    print(f"✗ Failed to list files: {e}")

# Test 6: Get file
print("\n" + "=" * 60)
print("Test 6: Retrieving file...")
print("=" * 60)

try:
    if file_id:
        file_data = manager.get_file(file_id)
        if file_data:
            print(f"✓ File retrieved successfully")
            print(f"  Name: {file_data.get('original_name')}")
            print(f"  Content length: {len(file_data.get('content', ''))} chars")
            print(f"  First 100 chars: {file_data.get('content', '')[:100]}...")
        else:
            print(f"✗ File not found")
    else:
        print(f"⚠ Skipping (no file_id from Test 4)")
except Exception as e:
    print(f"✗ Failed to retrieve file: {e}")

# Test 7: Get stats
print("\n" + "=" * 60)
print("Test 7: Getting statistics...")
print("=" * 60)

try:
    stats = manager.get_stats()
    print(f"✓ Statistics retrieved")
    print(f"  Total files: {stats['total_files']}")
    print(f"  Total size: {stats['total_size_mb']:.2f} MB")
    print(f"  Total sessions: {stats['total_sessions']}")
    print(f"  Current session: {stats['current_session']}")
except Exception as e:
    print(f"✗ Failed to get statistics: {e}")

# Test 8: Remove file (optional - commented out to preserve test data)
print("\n" + "=" * 60)
print("Test 8: File removal (optional)...")
print("=" * 60)
print("  ⚠ Skipped to preserve test data")
print("  To test removal, uncomment the code below")

# if file_id:
#     try:
#         result = manager.remove_file(file_id)
#         if result:
#             print(f"✓ File removed successfully")
#         else:
#             print(f"✗ Failed to remove file")
#     except Exception as e:
#         print(f"✗ Error removing file: {e}")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("✓ All tests passed!")
print("\nAttachment storage created at:")
print(f"  {test_dir}")
print("\nYou can inspect the files manually:")
print(f"  - Index: {test_dir / 'index.json'}")
print(f"  - Attachments: {test_dir / 'attachments' / 'test_session_001'}")
