"""
Unified Prompt Library Module

Simplified 2-layer architecture:
1. System Prompts (in Settings) - mode-specific, auto-selected
2. Prompt Library (main UI) - unified workspace with folders, favorites, multi-attach

Replaces the old 4-layer system (System/Domain/Project/Style Guides).
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class UnifiedPromptLibrary:
    """
    Manages prompts in a unified library structure with:
    - Nested folder support (unlimited depth)
    - Favorites and Quick Run menu
    - Multi-attach capability
    - Markdown files with YAML frontmatter
    """
    
    def __init__(self, library_dir=None, log_callback=None):
        """
        Initialize the Unified Prompt Library.
        
        Args:
            library_dir: Path to unified library directory (user_data/prompt_library)
            log_callback: Function to call for logging messages
        """
        self.library_dir = Path(library_dir) if library_dir else None
        self.log = log_callback if log_callback else print
        
        # Create directory if it doesn't exist
        if self.library_dir:
            self.library_dir.mkdir(parents=True, exist_ok=True)
        
        # Prompts storage: {relative_path: prompt_data}
        self.prompts = {}
        
        # Active prompt configuration
        self.active_primary_prompt = None  # Main prompt
        self.active_primary_prompt_path = None
        self.attached_prompts = []  # List of attached prompt data
        self.attached_prompt_paths = []  # List of paths
        
        # Cached lists for quick access
        self._favorites = []
        # Backward-compatible name; now represents QuickMenu (future app-level menu)
        self._quick_run = []
        self._quickmenu_grid = []
    
    def set_directory(self, library_dir):
        """Set the library directory after initialization"""
        self.library_dir = Path(library_dir)
        self.library_dir.mkdir(parents=True, exist_ok=True)
    
    def load_all_prompts(self):
        """Load all prompts from library directory (recursive)"""
        self.prompts = {}
        
        if not self.library_dir or not self.library_dir.exists():
            self.log("⚠ Library directory not found")
            return 0
        
        count = self._load_from_directory_recursive(self.library_dir, "")
        self.log(f"✓ Loaded {count} prompts from unified library")
        
        # Update cached lists
        self._update_favorites_list()
        self._update_quick_run_list()
        self._update_quickmenu_grid_list()
        
        return count
    
    def _load_from_directory_recursive(self, directory: Path, relative_path: str) -> int:
        """
        Recursively load prompts from directory and subdirectories.
        
        Args:
            directory: Absolute path to directory
            relative_path: Relative path from library root (for organization)
        
        Returns:
            Number of prompts loaded
        """
        count = 0
        
        if not directory.exists():
            return count
        
        for item in directory.iterdir():
            # Skip hidden files and __pycache__
            if item.name.startswith('.') or item.name == '__pycache__':
                continue
            
            # Recurse into subdirectories
            if item.is_dir():
                sub_relative = str(Path(relative_path) / item.name) if relative_path else item.name
                count += self._load_from_directory_recursive(item, sub_relative)
                continue
            
            # Load prompt files (.svprompt is the new format, .md and .txt for legacy)
            if item.suffix.lower() in ['.svprompt', '.md', '.txt']:
                prompt_data = self._parse_markdown(item)
                
                if prompt_data:
                    # Store with relative path as key
                    rel_path = str(Path(relative_path) / item.name) if relative_path else item.name
                    prompt_data['_filepath'] = str(item)
                    prompt_data['_relative_path'] = rel_path
                    prompt_data['_folder'] = relative_path
                    
                    self.prompts[rel_path] = prompt_data
                    count += 1
        
        return count
    
    def _parse_markdown(self, filepath: Path) -> Optional[Dict]:
        """
        Parse Markdown file with YAML frontmatter.
        
        Format:
        ---
        name: "Prompt Name"
        description: "Description"
        favorite: false
        quick_run: false
        folder: "Domain Expertise"
        tags: ["medical", "technical"]
        ---
        
        # Content
        Actual prompt content here...
        """
        try:
            content = filepath.read_text(encoding='utf-8')
            
            # Split frontmatter from content
            if content.startswith('---'):
                content = content[3:].lstrip('\n')
                
                if '---' in content:
                    frontmatter_str, prompt_content = content.split('---', 1)
                    prompt_content = prompt_content.lstrip('\n')
                else:
                    self.log(f"⚠ Invalid format in {filepath.name}: closing --- not found")
                    return None
            else:
                # No frontmatter - treat entire file as content
                prompt_content = content
                frontmatter_str = ""
            
            # Parse YAML frontmatter
            prompt_data = self._parse_yaml(frontmatter_str) if frontmatter_str else {}
            
            # Use filename as name if not specified
            if 'name' not in prompt_data:
                prompt_data['name'] = filepath.stem
            
            # Store content
            prompt_data['content'] = prompt_content.strip()
            
            # Ensure boolean fields exist
            prompt_data.setdefault('favorite', False)
            # Backward compatibility: quick_run is the legacy field; internally we
            # treat it as the "QuickMenu (future app menu)" flag.
            prompt_data.setdefault('quick_run', False)
            # Support legacy quickmenu_quickmenu field (rename to sv_quickmenu)
            if 'quickmenu_quickmenu' in prompt_data:
                prompt_data['sv_quickmenu'] = prompt_data['quickmenu_quickmenu']
            prompt_data['sv_quickmenu'] = bool(
                prompt_data.get('sv_quickmenu', prompt_data.get('quick_run', False))
            )
            # Keep legacy field in sync so older code/versions still behave.
            prompt_data['quick_run'] = bool(prompt_data['sv_quickmenu'])

            # New QuickMenu fields
            prompt_data.setdefault('quickmenu_grid', False)
            prompt_data.setdefault('quickmenu_label', prompt_data.get('name', filepath.stem))
            prompt_data.setdefault('tags', [])
            
            return prompt_data
            
        except Exception as e:
            self.log(f"⚠ Failed to parse {filepath.name}: {e}")
            return None
    
    def _parse_yaml(self, yaml_str: str) -> Dict:
        """
        Simple YAML parser for frontmatter.
        
        Supports:
        - Simple strings: key: "value" or key: value
        - Booleans: key: true/false
        - Numbers: key: 1.0
        - Arrays: tags: ["item1", "item2"] or tags: [item1, item2]
        """
        data = {}
        
        for line in yaml_str.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Handle arrays
            if value.startswith('[') and value.endswith(']'):
                # Remove brackets and split by comma
                array_str = value[1:-1]
                items = [item.strip().strip('"').strip("'") for item in array_str.split(',')]
                data[key] = [item for item in items if item]  # Filter empty
                continue
            
            # Handle booleans
            if value.lower() in ['true', 'false']:
                data[key] = value.lower() == 'true'
                continue
            
            # Remove quotes
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            # Handle numbers
            if value.replace('.', '', 1).replace('-', '', 1).isdigit():
                try:
                    value = float(value) if '.' in value else int(value)
                except:
                    pass
            
            data[key] = value
        
        return data
    
    def save_prompt(self, relative_path: str, prompt_data: Dict) -> bool:
        """
        Save prompt as Markdown file with YAML frontmatter.
        
        Args:
            relative_path: Relative path within library (e.g., "Domain Expertise/Medical.md")
            prompt_data: Dictionary with prompt info and content
        
        Returns:
            True if successful
        """
        try:
            if not self.library_dir:
                self.log("✗ Library directory not set")
                return False
            
            # Construct full path
            filepath = self.library_dir / relative_path
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Build frontmatter
            frontmatter = ['---']
            
            # Fields to include in frontmatter (in order)
            frontmatter_fields = [
                'name', 'description', 'domain', 'version', 'task_type', 
                'favorite',
                # QuickMenu
                'quickmenu_label', 'quickmenu_grid', 'sv_quickmenu',
                # Legacy (kept for backward compatibility)
                'quick_run',
                'folder', 'tags',
                'created', 'modified'
            ]
            
            for field in frontmatter_fields:
                if field in prompt_data:
                    value = prompt_data[field]
                    
                    # Format based on type
                    if isinstance(value, bool):
                        frontmatter.append(f'{field}: {str(value).lower()}')
                    elif isinstance(value, list):
                        # Format arrays
                        items = ', '.join([f'"{item}"' for item in value])
                        frontmatter.append(f'{field}: [{items}]')
                    elif isinstance(value, str):
                        frontmatter.append(f'{field}: "{value}"')
                    else:
                        frontmatter.append(f'{field}: {value}')
            
            frontmatter.append('---')
            
            # Get content
            content = prompt_data.get('content', '')
            
            # Build final file content
            file_content = '\n'.join(frontmatter) + '\n\n' + content.strip()
            
            # Write file
            filepath.write_text(file_content, encoding='utf-8')
            
            # Update in-memory storage
            prompt_data['_filepath'] = str(filepath)
            prompt_data['_relative_path'] = relative_path

            # Keep legacy field in sync
            if 'sv_quickmenu' in prompt_data:
                prompt_data['quick_run'] = bool(prompt_data.get('sv_quickmenu', False))
            self.prompts[relative_path] = prompt_data
            
            self.log(f"✓ Saved prompt: {prompt_data.get('name', relative_path)}")
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to save prompt: {e}")
            return False
    
    def get_folder_structure(self) -> Dict:
        """
        Get hierarchical folder structure with prompts.
        
        Returns:
            Nested dictionary representing folder tree
        """
        structure = {}
        
        for rel_path, prompt_data in self.prompts.items():
            parts = Path(rel_path).parts
            
            # Build nested structure
            current = structure
            for i, part in enumerate(parts[:-1]):  # Folders only
                if part not in current:
                    current[part] = {'_folders': {}, '_prompts': []}
                current = current[part]['_folders']
            
            # Add prompt to final folder
            folder_name = parts[-2] if len(parts) > 1 else '_root'
            if folder_name not in current:
                current[folder_name] = {'_folders': {}, '_prompts': []}
            
            current[folder_name]['_prompts'].append({
                'path': rel_path,
                'name': prompt_data.get('name', Path(rel_path).stem),
                'favorite': prompt_data.get('favorite', False),
                'quick_run': prompt_data.get('quick_run', False),
                'quickmenu_grid': prompt_data.get('quickmenu_grid', False),
                'quickmenu_quickmenu': prompt_data.get('quickmenu_quickmenu', prompt_data.get('quick_run', False)),
                'quickmenu_label': prompt_data.get('quickmenu_label', prompt_data.get('name', Path(rel_path).stem)),
            })
        
        return structure
    
    def set_primary_prompt(self, relative_path: str) -> bool:
        """Set the primary (main) active prompt"""
        if relative_path not in self.prompts:
            self.log(f"✗ Prompt not found: {relative_path}")
            return False
        
        self.active_primary_prompt = self.prompts[relative_path]['content']
        self.active_primary_prompt_path = relative_path
        self.log(f"✓ Set primary prompt: {self.prompts[relative_path].get('name', relative_path)}")
        return True
    
    def set_external_primary_prompt(self, file_path: str) -> Tuple[bool, str]:
        """
        Set an external file (not in library) as the primary prompt.
        
        Args:
            file_path: Absolute path to the external prompt file
        
        Returns:
            Tuple of (success, display_name or error_message)
        """
        path = Path(file_path)
        
        if not path.exists():
            self.log(f"✗ File not found: {file_path}")
            return False, "File not found"
        
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            self.log(f"✗ Error reading file: {e}")
            return False, f"Error reading file: {e}"
        
        # Use filename (without extension) as display name
        display_name = path.stem
        
        # Mark as external with special prefix
        self.active_primary_prompt = content
        self.active_primary_prompt_path = f"[EXTERNAL] {file_path}"
        
        self.log(f"✓ Set external primary prompt: {display_name}")
        return True, display_name
    
    def attach_prompt(self, relative_path: str) -> bool:
        """Attach a prompt to the active configuration"""
        if relative_path not in self.prompts:
            self.log(f"✗ Prompt not found: {relative_path}")
            return False
        
        # Don't attach if already attached
        if relative_path in self.attached_prompt_paths:
            self.log(f"⚠ Already attached: {relative_path}")
            return False
        
        prompt_data = self.prompts[relative_path]
        self.attached_prompts.append(prompt_data['content'])
        self.attached_prompt_paths.append(relative_path)
        
        self.log(f"✓ Attached: {prompt_data.get('name', relative_path)}")
        return True
    
    def detach_prompt(self, relative_path: str) -> bool:
        """Remove an attached prompt"""
        if relative_path not in self.attached_prompt_paths:
            return False
        
        idx = self.attached_prompt_paths.index(relative_path)
        self.attached_prompts.pop(idx)
        self.attached_prompt_paths.pop(idx)
        
        self.log(f"✓ Detached: {relative_path}")
        return True
    
    def clear_attachments(self):
        """Clear all attached prompts"""
        self.attached_prompts = []
        self.attached_prompt_paths = []
        self.log("✓ Cleared all attachments")
    
    def toggle_favorite(self, relative_path: str) -> bool:
        """Toggle favorite status for a prompt"""
        if relative_path not in self.prompts:
            return False
        
        prompt_data = self.prompts[relative_path]
        prompt_data['favorite'] = not prompt_data.get('favorite', False)
        prompt_data['modified'] = datetime.now().strftime("%Y-%m-%d")
        
        # Save updated prompt
        self.save_prompt(relative_path, prompt_data)
        self._update_favorites_list()
        
        return True
    
    def toggle_quick_run(self, relative_path: str) -> bool:
        """Toggle QuickMenu (future app menu) status for a prompt (legacy name: quick_run)."""
        if relative_path not in self.prompts:
            return False
        
        prompt_data = self.prompts[relative_path]
        new_value = not bool(prompt_data.get('sv_quickmenu', prompt_data.get('quick_run', False)))
        prompt_data['sv_quickmenu'] = new_value
        prompt_data['quick_run'] = new_value  # keep legacy in sync
        prompt_data['modified'] = datetime.now().strftime("%Y-%m-%d")
        
        # Save updated prompt
        self.save_prompt(relative_path, prompt_data)
        self._update_quick_run_list()
        self._update_quickmenu_grid_list()
        
        return True

    def toggle_quickmenu_grid(self, relative_path: str) -> bool:
        """Toggle whether this prompt appears in the Grid right-click QuickMenu."""
        if relative_path not in self.prompts:
            return False

        prompt_data = self.prompts[relative_path]
        prompt_data['quickmenu_grid'] = not bool(prompt_data.get('quickmenu_grid', False))
        prompt_data['modified'] = datetime.now().strftime("%Y-%m-%d")

        self.save_prompt(relative_path, prompt_data)
        self._update_quickmenu_grid_list()
        return True
    
    def _update_favorites_list(self):
        """Update cached favorites list"""
        self._favorites = [
            (path, data.get('name', Path(path).stem))
            for path, data in self.prompts.items()
            if data.get('favorite', False)
        ]
    
    def _update_quick_run_list(self):
        """Update cached QuickMenu (future app menu) list (legacy name: quick_run)."""
        self._quick_run = []
        for path, data in self.prompts.items():
            is_enabled = bool(data.get('sv_quickmenu', data.get('quick_run', False)))
            if not is_enabled:
                continue
            label = (data.get('quickmenu_label') or data.get('name') or Path(path).stem).strip()
            self._quick_run.append((path, label))

    def _update_quickmenu_grid_list(self):
        """Update cached Grid QuickMenu list."""
        self._quickmenu_grid = []
        for path, data in self.prompts.items():
            if not bool(data.get('quickmenu_grid', False)):
                continue
            label = (data.get('quickmenu_label') or data.get('name') or Path(path).stem).strip()
            self._quickmenu_grid.append((path, label))
    
    def get_favorites(self) -> List[Tuple[str, str]]:
        """Get list of favorite prompts (path, name)"""
        return self._favorites
    
    def get_quick_run_prompts(self) -> List[Tuple[str, str]]:
        """Get list of QuickMenu (future app menu) prompts (path, label)."""
        return self._quick_run

    def get_quickmenu_prompts(self) -> List[Tuple[str, str]]:
        """Alias for get_quick_run_prompts(), using the new naming."""
        return self.get_quick_run_prompts()

    def get_quickmenu_grid_prompts(self) -> List[Tuple[str, str]]:
        """Get list of prompts shown in the Grid right-click QuickMenu (path, label)."""
        return self._quickmenu_grid
    
    def create_folder(self, folder_path: str) -> bool:
        """Create a new folder in the library"""
        try:
            if not self.library_dir:
                return False
            
            full_path = self.library_dir / folder_path
            full_path.mkdir(parents=True, exist_ok=True)
            
            self.log(f"✓ Created folder: {folder_path}")
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to create folder: {e}")
            return False
    
    def move_prompt(self, old_path: str, new_path: str) -> bool:
        """Move a prompt to a different folder"""
        try:
            if old_path not in self.prompts:
                return False
            
            old_file = Path(self.prompts[old_path]['_filepath'])
            new_file = self.library_dir / new_path
            
            # Create destination folder
            new_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            shutil.move(str(old_file), str(new_file))
            
            # Update in-memory storage
            prompt_data = self.prompts.pop(old_path)
            prompt_data['_filepath'] = str(new_file)
            prompt_data['_relative_path'] = new_path
            self.prompts[new_path] = prompt_data
            
            # Update active references if needed
            if self.active_primary_prompt_path == old_path:
                self.active_primary_prompt_path = new_path
            
            if old_path in self.attached_prompt_paths:
                idx = self.attached_prompt_paths.index(old_path)
                self.attached_prompt_paths[idx] = new_path
            
            self.log(f"✓ Moved: {old_path} → {new_path}")
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to move prompt: {e}")
            return False

    def move_folder(self, old_folder: str, new_folder: str) -> bool:
        """Move a folder (and all contained prompts/subfolders) within the library."""
        try:
            if not self.library_dir:
                return False

            old_folder = old_folder or ""
            new_folder = new_folder or ""

            old_dir = self.library_dir / old_folder
            new_dir = self.library_dir / new_folder

            if not old_dir.exists() or not old_dir.is_dir():
                return False

            # Prevent moving a folder into itself / a descendant
            old_parts = Path(old_folder).parts
            new_parts = Path(new_folder).parts
            if old_parts and len(new_parts) >= len(old_parts) and new_parts[:len(old_parts)] == old_parts:
                return False

            new_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_dir), str(new_dir))

            old_prefix = f"{old_folder}/" if old_folder else ""
            new_prefix = f"{new_folder}/" if new_folder else ""

            def rewrite_path(path: Optional[str]) -> Optional[str]:
                if not path:
                    return path
                if old_folder and (path == old_folder or path.startswith(old_prefix)):
                    return new_folder + path[len(old_folder):]
                if not old_folder and path:
                    # moving root is not supported
                    return path
                return path

            # Update active references (paths only). Caller should reload prompts.
            self.active_primary_prompt_path = rewrite_path(self.active_primary_prompt_path)

            new_attached = []
            for p in self.attached_prompt_paths:
                new_attached.append(rewrite_path(p))
            self.attached_prompt_paths = new_attached

            self.log(f"✓ Moved folder: {old_folder} → {new_folder}")
            return True

        except Exception as e:
            self.log(f"✗ Failed to move folder: {e}")
            return False
    
    def delete_prompt(self, relative_path: str) -> bool:
        """Delete a prompt"""
        try:
            if relative_path not in self.prompts:
                return False
            
            filepath = Path(self.prompts[relative_path]['_filepath'])
            filepath.unlink()
            
            # Remove from memory
            del self.prompts[relative_path]
            
            # Clear from active if needed
            if self.active_primary_prompt_path == relative_path:
                self.active_primary_prompt = None
                self.active_primary_prompt_path = None
            
            if relative_path in self.attached_prompt_paths:
                self.detach_prompt(relative_path)
            
            self.log(f"✓ Deleted: {relative_path}")
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to delete prompt: {e}")
            return False
