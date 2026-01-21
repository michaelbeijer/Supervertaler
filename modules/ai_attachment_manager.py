"""
AI Assistant Attachment Manager

Manages persistent storage of attached files for the AI Assistant.
Files are converted to markdown and stored with metadata.
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class AttachmentManager:
    """
    Manages file attachments for AI Assistant conversations.

    Features:
    - Persistent storage of converted markdown files
    - Metadata tracking (original name, path, type, size, date)
    - Session-based organization
    - Master index for quick lookup
    """

    def __init__(self, base_dir: str = None, log_callback=None):
        """
        Initialize the AttachmentManager.

        Args:
            base_dir: Base directory for attachments (default: user_data_private/ai_assistant)
            log_callback: Function to call for logging messages
        """
        self.log = log_callback if log_callback else print

        # Set base directory
        if base_dir is None:
            # Default to user_data_private/ai_assistant
            base_dir = Path("user_data_private") / "ai_assistant"

        self.base_dir = Path(base_dir)
        self.attachments_dir = self.base_dir / "attachments"
        self.conversations_dir = self.base_dir / "conversations"
        self.index_file = self.base_dir / "index.json"

        # Create directory structure
        self._init_directories()

        # Load index
        self.index = self._load_index()

        # Current session ID
        self.current_session_id = None

    def _init_directories(self):
        """Create necessary directories if they don't exist"""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.attachments_dir.mkdir(parents=True, exist_ok=True)
        self.conversations_dir.mkdir(parents=True, exist_ok=True)

        self.log(f"✓ Attachment directories initialized: {self.base_dir}")

    def _load_index(self) -> Dict:
        """Load the master index of all attachments"""
        if not self.index_file.exists():
            return {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "attachments": {},  # file_id -> metadata
                "sessions": {}      # session_id -> [file_ids]
            }

        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"⚠ Failed to load index: {e}")
            return {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "attachments": {},
                "sessions": {}
            }

    def _save_index(self):
        """Save the master index"""
        try:
            self.index["updated"] = datetime.now().isoformat()
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"✗ Failed to save index: {e}")

    def _generate_file_id(self, original_path: str, content: str) -> str:
        """Generate unique file ID based on path and content hash"""
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
        path_hash = hashlib.sha256(original_path.encode('utf-8')).hexdigest()[:8]
        return f"{path_hash}_{content_hash}"

    def set_session(self, session_id: str):
        """Set the current session ID"""
        self.current_session_id = session_id

        # Create session directory
        session_dir = self.attachments_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        # Initialize session in index
        if session_id not in self.index["sessions"]:
            self.index["sessions"][session_id] = []
            self._save_index()

    def attach_file(
        self,
        original_path: str,
        markdown_content: str,
        original_name: str = None,
        conversation_id: str = None
    ) -> Optional[str]:
        """
        Save an attached file with metadata.

        Args:
            original_path: Full path to original file
            markdown_content: Converted markdown content
            original_name: Original filename (optional, extracted from path if not provided)
            conversation_id: ID of conversation this file belongs to

        Returns:
            file_id if successful, None otherwise
        """
        try:
            # Ensure session is set
            if self.current_session_id is None:
                self.set_session(datetime.now().strftime("%Y%m%d_%H%M%S"))

            # Extract filename if not provided
            if original_name is None:
                original_name = Path(original_path).name

            # Generate file ID
            file_id = self._generate_file_id(original_path, markdown_content)

            # Check if already attached
            if file_id in self.index["attachments"]:
                self.log(f"⚠ File already attached: {original_name}")
                return file_id

            # Session directory
            session_dir = self.attachments_dir / self.current_session_id

            # Save markdown content
            md_file = session_dir / f"{file_id}.md"
            md_file.write_text(markdown_content, encoding='utf-8')

            # Create metadata
            file_type = Path(original_path).suffix
            metadata = {
                "file_id": file_id,
                "original_name": original_name,
                "original_path": str(original_path),
                "file_type": file_type,
                "size_bytes": len(markdown_content.encode('utf-8')),
                "size_chars": len(markdown_content),
                "attached_at": datetime.now().isoformat(),
                "session_id": self.current_session_id,
                "conversation_id": conversation_id,
                "markdown_path": str(md_file.relative_to(self.base_dir))
            }

            # Save metadata
            meta_file = session_dir / f"{file_id}.meta.json"
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            # Update index
            self.index["attachments"][file_id] = metadata
            self.index["sessions"][self.current_session_id].append(file_id)
            self._save_index()

            self.log(f"✓ Attached file: {original_name} ({file_id})")
            return file_id

        except Exception as e:
            self.log(f"✗ Failed to attach file: {e}")
            return None

    def get_file(self, file_id: str) -> Optional[Dict]:
        """
        Get file metadata and content.

        Args:
            file_id: File ID

        Returns:
            Dictionary with metadata and content, or None if not found
        """
        if file_id not in self.index["attachments"]:
            return None

        metadata = self.index["attachments"][file_id].copy()

        # Load markdown content
        md_path = self.base_dir / metadata["markdown_path"]
        if md_path.exists():
            metadata["content"] = md_path.read_text(encoding='utf-8')
        else:
            metadata["content"] = None

        return metadata

    def remove_file(self, file_id: str) -> bool:
        """
        Remove an attached file.

        Args:
            file_id: File ID to remove

        Returns:
            True if successful, False otherwise
        """
        if file_id not in self.index["attachments"]:
            self.log(f"⚠ File not found: {file_id}")
            return False

        try:
            metadata = self.index["attachments"][file_id]
            session_id = metadata["session_id"]

            # Delete files
            session_dir = self.attachments_dir / session_id
            md_file = session_dir / f"{file_id}.md"
            meta_file = session_dir / f"{file_id}.meta.json"

            if md_file.exists():
                md_file.unlink()
            if meta_file.exists():
                meta_file.unlink()

            # Update index
            del self.index["attachments"][file_id]
            if session_id in self.index["sessions"]:
                if file_id in self.index["sessions"][session_id]:
                    self.index["sessions"][session_id].remove(file_id)

            self._save_index()

            self.log(f"✓ Removed file: {file_id}")
            return True

        except Exception as e:
            self.log(f"✗ Failed to remove file: {e}")
            return False

    def list_session_files(self, session_id: str = None) -> List[Dict]:
        """
        List all files in a session.

        Args:
            session_id: Session ID (uses current session if None)

        Returns:
            List of file metadata dictionaries
        """
        if session_id is None:
            session_id = self.current_session_id

        if session_id is None or session_id not in self.index["sessions"]:
            return []

        file_ids = self.index["sessions"][session_id]
        files = []

        for file_id in file_ids:
            if file_id in self.index["attachments"]:
                files.append(self.index["attachments"][file_id].copy())

        # Sort by attached_at (most recent first)
        files.sort(key=lambda x: x.get("attached_at", ""), reverse=True)

        return files

    def list_all_files(self) -> List[Dict]:
        """
        List all attached files across all sessions.

        Returns:
            List of file metadata dictionaries
        """
        files = [
            metadata.copy()
            for metadata in self.index["attachments"].values()
        ]

        # Sort by attached_at (most recent first)
        files.sort(key=lambda x: x.get("attached_at", ""), reverse=True)

        return files

    def get_stats(self) -> Dict:
        """
        Get statistics about attachments.

        Returns:
            Dictionary with stats (total_files, total_size, sessions, etc.)
        """
        total_files = len(self.index["attachments"])
        total_size = sum(
            meta.get("size_bytes", 0)
            for meta in self.index["attachments"].values()
        )
        total_sessions = len(self.index["sessions"])

        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "total_sessions": total_sessions,
            "current_session": self.current_session_id
        }

    def cleanup_empty_sessions(self):
        """Remove sessions with no files"""
        empty_sessions = [
            session_id
            for session_id, file_ids in self.index["sessions"].items()
            if len(file_ids) == 0
        ]

        for session_id in empty_sessions:
            del self.index["sessions"][session_id]

            # Remove session directory if empty
            session_dir = self.attachments_dir / session_id
            if session_dir.exists() and not any(session_dir.iterdir()):
                session_dir.rmdir()

        if empty_sessions:
            self._save_index()
            self.log(f"✓ Cleaned up {len(empty_sessions)} empty sessions")

        return len(empty_sessions)
