"""
Style Guide Manager Module

Manages translation style guides for different languages.
Supports style guides as Markdown files with optional YAML frontmatter.

Extracted for modularity and reusability.
Supports both individual language-specific guides and optional user additions.
"""

import os
import json
import shutil
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class StyleGuideLibrary:
    """
    Manages translation style guides for multiple languages.
    Loads style guide files from appropriate folder based on dev mode.
    """
    
    # Supported languages for style guides
    SUPPORTED_LANGUAGES = [
        "Dutch",
        "English",
        "Spanish",
        "German",
        "French"
    ]
    
    def __init__(self, style_guides_dir=None, log_callback=None):
        """
        Initialize the Style Guide Library.
        
        Args:
            style_guides_dir: Path to style guides directory (if None, must be set later)
            log_callback: Function to call for logging messages
        """
        self.style_guides_dir = style_guides_dir
        self.log = log_callback if log_callback else print
        
        # Create directory if it doesn't exist and path is provided
        if self.style_guides_dir:
            os.makedirs(self.style_guides_dir, exist_ok=True)
        
        # Available style guides: {language: guide_data}
        self.guides = {}
        self.active_guide = None  # Currently selected guide
        self.active_guide_language = None
    
    def set_directory(self, style_guides_dir):
        """Set the directory after initialization"""
        self.style_guides_dir = style_guides_dir
        os.makedirs(self.style_guides_dir, exist_ok=True)
    
    def load_all_guides(self):
        """Load all style guides from the style guides directory"""
        self.guides = {}
        
        if not self.style_guides_dir or not os.path.exists(self.style_guides_dir):
            self.log("⚠ Style guides directory not found")
            return 0
        
        count = self._load_from_directory(self.style_guides_dir)
        self.log(f"✓ Loaded {count} style guides")
        return count
    
    def _load_from_directory(self, directory):
        """Load style guides from directory
        
        Expected file naming: <Language>.md or <Language>.txt
        Examples: Dutch.md, English.md, Spanish.txt, etc.
        
        Args:
            directory: Path to directory
        """
        count = 0
        
        if not directory or not os.path.exists(directory):
            return count
        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            
            # Skip directories
            if os.path.isdir(filepath):
                continue
            
            # Check if file matches supported language format
            if filename.endswith('.md') or filename.endswith('.txt'):
                language = filename.rsplit('.', 1)[0]  # Remove extension
                
                # Load content
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    guide_data = {
                        'language': language,
                        'content': content,
                        '_filename': filename,
                        '_filepath': filepath,
                        '_created': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat(),
                        '_modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat(),
                    }
                    
                    self.guides[language] = guide_data
                    count += 1
                    
                except Exception as e:
                    self.log(f"⚠ Failed to load {filename}: {e}")
        
        return count
    
    def get_guide(self, language: str) -> Optional[Dict]:
        """
        Get a specific style guide by language.
        
        Args:
            language: Language name (e.g., 'Dutch', 'English')
        
        Returns:
            Dictionary with guide data or None if not found
        """
        return self.guides.get(language)
    
    def get_all_languages(self) -> List[str]:
        """Get list of all available style guide languages"""
        return sorted(self.guides.keys())
    
    def get_guide_content(self, language: str) -> Optional[str]:
        """Get the content of a specific style guide"""
        guide = self.guides.get(language)
        return guide['content'] if guide else None
    
    def update_guide(self, language: str, new_content: str) -> bool:
        """
        Update a style guide with new content.
        
        Args:
            language: Language name
            new_content: New content for the guide
        
        Returns:
            True if successful, False otherwise
        """
        guide = self.guides.get(language)
        if not guide:
            self.log(f"⚠ Style guide not found: {language}")
            return False
        
        try:
            filepath = guide['_filepath']
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Update in memory
            guide['content'] = new_content
            guide['_modified'] = datetime.now().isoformat()
            
            self.log(f"✓ Updated style guide: {language}")
            return True
        
        except Exception as e:
            self.log(f"⚠ Failed to update {language}: {e}")
            return False
    
    def append_to_guide(self, language: str, additional_content: str) -> bool:
        """
        Append content to an existing style guide.
        
        Args:
            language: Language name
            additional_content: Content to append
        
        Returns:
            True if successful, False otherwise
        """
        guide = self.guides.get(language)
        if not guide:
            self.log(f"⚠ Style guide not found: {language}")
            return False
        
        current_content = guide['content']
        new_content = current_content.rstrip() + '\n\n' + additional_content.strip()
        
        return self.update_guide(language, new_content)
    
    def append_to_all_guides(self, additional_content: str) -> Tuple[int, int]:
        """
        Append content to all style guides.
        
        Args:
            additional_content: Content to append to all guides
        
        Returns:
            Tuple of (successful_count, failed_count)
        """
        successful = 0
        failed = 0
        
        for language in self.guides.keys():
            if self.append_to_guide(language, additional_content):
                successful += 1
            else:
                failed += 1
        
        self.log(f"✓ Updated {successful} guides. Failed: {failed}")
        return successful, failed
    
    def create_guide(self, language: str, content: str = "") -> bool:
        """
        Create a new style guide file.
        
        Args:
            language: Language name
            content: Initial content (optional)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.style_guides_dir:
            self.log("⚠ Style guides directory not set")
            return False
        
        if language in self.guides:
            self.log(f"⚠ Style guide already exists: {language}")
            return False
        
        try:
            filepath = os.path.join(self.style_guides_dir, f"{language}.md")
            
            # Create file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Add to guides dictionary
            guide_data = {
                'language': language,
                'content': content,
                '_filename': f"{language}.md",
                '_filepath': filepath,
                '_created': datetime.now().isoformat(),
                '_modified': datetime.now().isoformat(),
            }
            
            self.guides[language] = guide_data
            self.log(f"✓ Created style guide: {language}")
            return True
        
        except Exception as e:
            self.log(f"⚠ Failed to create {language}: {e}")
            return False
    
    def export_guide(self, language: str, export_path: str) -> bool:
        """
        Export a style guide to a file.
        
        Args:
            language: Language name
            export_path: Path where to save the exported guide
        
        Returns:
            True if successful, False otherwise
        """
        guide = self.guides.get(language)
        if not guide:
            self.log(f"⚠ Style guide not found: {language}")
            return False
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(guide['content'])
            
            self.log(f"✓ Exported style guide: {language}")
            return True
        
        except Exception as e:
            self.log(f"⚠ Failed to export {language}: {e}")
            return False
    
    def import_guide(self, language: str, import_path: str, append: bool = False) -> bool:
        """
        Import a style guide from a file.
        
        Args:
            language: Language name to import as
            import_path: Path to the file to import
            append: If True, append to existing guide; if False, replace
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if language not in self.guides:
                # Create new guide
                return self.create_guide(language, content)
            elif append:
                # Append to existing guide
                return self.append_to_guide(language, content)
            else:
                # Replace existing guide
                return self.update_guide(language, content)
        
        except Exception as e:
            self.log(f"⚠ Failed to import from {import_path}: {e}")
            return False
