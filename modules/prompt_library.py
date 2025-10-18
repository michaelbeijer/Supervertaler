"""
Prompt Library Manager Module

Manages translation prompts with domain-specific expertise.
Supports two types:
- System Prompts: Define AI role and expertise
- Custom Instructions: Additional context and preferences

Supports both JSON (legacy) and Markdown (recommended) formats.
Markdown files use YAML frontmatter for metadata.

Extracted from main Supervertaler file for better modularity.
"""

import os
import json
import shutil
import re
from datetime import datetime
from tkinter import messagebox


def get_user_data_path(subfolder):
    """
    Get path to user data folder, handling DEV_MODE.
    This is imported from the main module's implementation.
    """
    # Import from parent if needed, or accept as parameter
    # For now, we'll make this module require the path to be passed in __init__
    pass


class PromptLibrary:
    """
    Manages translation prompts with domain-specific expertise.
    Supports two types:
    - System Prompts: Define AI role and expertise
    - Custom Instructions: Additional context and preferences
    
    Loads JSON files from appropriate folders based on dev mode.
    """
    def __init__(self, system_prompts_dir=None, custom_instructions_dir=None, log_callback=None):
        """
        Initialize the Prompt Library.
        
        Args:
            system_prompts_dir: Path to system prompts directory (if None, must be set later)
            custom_instructions_dir: Path to custom instructions directory (if None, must be set later)
            log_callback: Function to call for logging messages
        """
        self.system_prompts_dir = system_prompts_dir
        self.custom_instructions_dir = custom_instructions_dir
        
        self.log = log_callback if log_callback else print
        
        # Create directories if they don't exist and paths are provided
        if self.system_prompts_dir:
            os.makedirs(self.system_prompts_dir, exist_ok=True)
        if self.custom_instructions_dir:
            os.makedirs(self.custom_instructions_dir, exist_ok=True)
        
        # Available prompts: {filename: prompt_data}
        self.prompts = {}
        self.active_prompt = None  # Currently selected prompt
        self.active_prompt_name = None
    
    def set_directories(self, system_prompts_dir, custom_instructions_dir):
        """Set the directories after initialization"""
        self.system_prompts_dir = system_prompts_dir
        self.custom_instructions_dir = custom_instructions_dir
        os.makedirs(self.system_prompts_dir, exist_ok=True)
        os.makedirs(self.custom_instructions_dir, exist_ok=True)
        
    def load_all_prompts(self):
        """Load all prompts (system prompts and custom instructions) from appropriate directories"""
        self.prompts = {}
        
        # Load from the appropriate directories based on dev mode
        sys_count = self._load_from_directory(self.system_prompts_dir, prompt_type="system_prompt")
        inst_count = self._load_from_directory(self.custom_instructions_dir, prompt_type="custom_instruction")
        
        total = sys_count + inst_count
        self.log(f"✓ Loaded {total} prompts ({sys_count} system prompts, {inst_count} custom instructions)")
        return total
    
    def _load_from_directory(self, directory, prompt_type="system_prompt"):
        """Load prompts from a specific directory
        
        Args:
            directory: Path to directory
            prompt_type: Either 'system_prompt' or 'custom_instruction'
        """
        count = 0
        
        if not directory or not os.path.exists(directory):
            return count
        
        for filename in os.listdir(directory):
            if not filename.endswith('.json'):
                continue
            
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    prompt_data = json.load(f)
                    
                    # Add metadata
                    prompt_data['_filename'] = filename
                    prompt_data['_filepath'] = filepath
                    prompt_data['_type'] = prompt_type  # Add type field
                    
                    # Add task_type with backward compatibility
                    if 'task_type' not in prompt_data:
                        # Infer task type from title/name for backward compatibility
                        prompt_data['task_type'] = self._infer_task_type(prompt_data.get('name', ''))
                    
                    # Validate required fields
                    if 'name' not in prompt_data or 'translate_prompt' not in prompt_data:
                        self.log(f"⚠ Skipping {filename}: missing required fields (name, translate_prompt)")
                        continue
                    
                    self.prompts[filename] = prompt_data
                    count += 1
                    
            except Exception as e:
                self.log(f"⚠ Failed to load {filename}: {e}")
                
        return count
    
    def _infer_task_type(self, title):
        """Infer task type from prompt title for backward compatibility
        
        Args:
            title: Prompt title/name
            
        Returns:
            str: Inferred task type
        """
        title_lower = title.lower()
        
        if 'localization' in title_lower or 'localisation' in title_lower:
            return 'Localization'
        elif 'proofread' in title_lower:
            return 'Proofreading'
        elif 'qa' in title_lower or 'quality' in title_lower:
            return 'QA'
        elif 'copyedit' in title_lower or 'copy-edit' in title_lower:
            return 'Copyediting'
        elif 'post-edit' in title_lower or 'postedit' in title_lower:
            return 'Post-editing'
        elif 'transcreation' in title_lower:
            return 'Transcreation'
        else:
            return 'Translation'  # Default
    
    def get_prompt_list(self):
        """Get list of available prompts with metadata"""
        prompt_list = []
        for filename, data in sorted(self.prompts.items()):
            prompt_list.append({
                'filename': filename,
                'name': data.get('name', 'Unnamed'),
                'description': data.get('description', ''),
                'domain': data.get('domain', 'General'),
                'version': data.get('version', '1.0'),
                'task_type': data.get('task_type', 'Translation'),  # NEW: Include task type
                'filepath': data.get('_filepath', ''),
                '_type': data.get('_type', 'system_prompt')  # Include type for filtering
            })
        return prompt_list
    
    def get_prompt(self, filename):
        """Get full prompt data by filename"""
        return self.prompts.get(filename)
    
    def set_active_prompt(self, filename):
        """Set the active custom prompt"""
        if filename not in self.prompts:
            self.log(f"✗ Prompt not found: {filename}")
            return False
        
        self.active_prompt = self.prompts[filename]
        self.active_prompt_name = self.active_prompt.get('name', filename)
        self.log(f"✓ Active prompt: {self.active_prompt_name}")
        return True
    
    def clear_active_prompt(self):
        """Clear active prompt (use default)"""
        self.active_prompt = None
        self.active_prompt_name = None
        self.log("✓ Using default translation prompt")
    
    def get_translate_prompt(self):
        """Get the translate_prompt from active prompt, or None if using default"""
        if self.active_prompt:
            return self.active_prompt.get('translate_prompt')
        return None
    
    def get_proofread_prompt(self):
        """Get the proofread_prompt from active prompt, or None if using default"""
        if self.active_prompt:
            return self.active_prompt.get('proofread_prompt')
        return None
    
    def search_prompts(self, search_text):
        """Search prompts by name, description, or domain"""
        if not search_text:
            return self.get_prompt_list()
        
        search_lower = search_text.lower()
        results = []
        
        for filename, data in sorted(self.prompts.items()):
            name = data.get('name', '').lower()
            desc = data.get('description', '').lower()
            domain = data.get('domain', '').lower()
            
            if search_lower in name or search_lower in desc or search_lower in domain:
                results.append({
                    'filename': filename,
                    'name': data.get('name', 'Unnamed'),
                    'description': data.get('description', ''),
                    'domain': data.get('domain', 'General'),
                    'version': data.get('version', '1.0'),
                    'filepath': data.get('_filepath', '')
                })
        
        return results
    
    def create_new_prompt(self, name, description, domain, translate_prompt, proofread_prompt="", 
                         version="1.0", task_type="Translation", prompt_type="system_prompt"):
        """Create a new prompt and save to JSON
        
        Args:
            prompt_type: Either 'system_prompt' or 'custom_instruction'
            task_type: Type of translation task
        """
        # Create filename from name
        filename = name.replace(' ', '_').replace('/', '_') + '.json'
        
        # Choose directory based on type
        if prompt_type == "custom_instruction":
            directory = self.custom_instructions_dir
        else:  # system_prompt
            directory = self.system_prompts_dir
            
        filepath = os.path.join(directory, filename)
        
        # Create prompt data
        prompt_data = {
            'name': name,
            'description': description,
            'domain': domain,
            'version': version,
            'task_type': task_type,
            'created': datetime.now().strftime('%Y-%m-%d'),
            'translate_prompt': translate_prompt,
            'proofread_prompt': proofread_prompt
        }
        
        # Save to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
            
            # Add to loaded prompts
            prompt_data['_filename'] = filename
            prompt_data['_filepath'] = filepath
            prompt_data['_type'] = prompt_type
            self.prompts[filename] = prompt_data
            
            self.log(f"✓ Created new prompt: {name}")
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to create prompt: {e}")
            messagebox.showerror("Save Error", f"Failed to save prompt:\n{e}")
            return False
    
    def update_prompt(self, filename, name, description, domain, translate_prompt, 
                     proofread_prompt="", version="1.0", task_type="Translation"):
        """Update an existing prompt"""
        if filename not in self.prompts:
            self.log(f"✗ Prompt not found: {filename}")
            return False
        
        filepath = self.prompts[filename]['_filepath']
        
        # Update prompt data
        prompt_data = {
            'name': name,
            'description': description,
            'domain': domain,
            'version': version,
            'task_type': task_type,
            'created': self.prompts[filename].get('created', datetime.now().strftime('%Y-%m-%d')),
            'modified': datetime.now().strftime('%Y-%m-%d'),
            'translate_prompt': translate_prompt,
            'proofread_prompt': proofread_prompt
        }
        
        # Save to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
            
            # Update loaded prompts
            prompt_data['_filename'] = filename
            prompt_data['_filepath'] = filepath
            prompt_data['_type'] = self.prompts[filename].get('_type', 'system_prompt')
            self.prompts[filename] = prompt_data
            
            self.log(f"✓ Updated prompt: {name}")
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to update prompt: {e}")
            messagebox.showerror("Save Error", f"Failed to update prompt:\n{e}")
            return False
    
    def delete_prompt(self, filename):
        """Delete a custom prompt"""
        if filename not in self.prompts:
            return False
        
        filepath = self.prompts[filename]['_filepath']
        prompt_name = self.prompts[filename].get('name', filename)
        
        try:
            os.remove(filepath)
            del self.prompts[filename]
            
            # Clear active if this was active
            if self.active_prompt and self.active_prompt.get('_filename') == filename:
                self.clear_active_prompt()
            
            self.log(f"✓ Deleted prompt: {prompt_name}")
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to delete prompt: {e}")
            messagebox.showerror("Delete Error", f"Failed to delete prompt:\n{e}")
            return False
    
    def export_prompt(self, filename, export_path):
        """Export a prompt to a specific location"""
        if filename not in self.prompts:
            return False
        
        try:
            source = self.prompts[filename]['_filepath']
            shutil.copy2(source, export_path)
            self.log(f"✓ Exported prompt to: {export_path}")
            return True
        except Exception as e:
            self.log(f"✗ Export failed: {e}")
            return False
    
    def import_prompt(self, import_path, prompt_type="system_prompt"):
        """Import a prompt from an external file
        
        Args:
            import_path: Path to JSON file to import
            prompt_type: Either 'system_prompt' or 'custom_instruction'
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                prompt_data = json.load(f)
            
            # Validate
            if 'name' not in prompt_data or 'translate_prompt' not in prompt_data:
                messagebox.showerror("Invalid Prompt", "Missing required fields: name, translate_prompt")
                return False
            
            # Copy to appropriate directory based on type
            filename = os.path.basename(import_path)
            if prompt_type == "custom_instruction":
                directory = self.custom_instructions_dir
            else:  # system_prompt
                directory = self.system_prompts_dir
            dest_path = os.path.join(directory, filename)
            
            shutil.copy2(import_path, dest_path)
            
            # Add metadata and load
            prompt_data['_filename'] = filename
            prompt_data['_filepath'] = dest_path
            prompt_data['_type'] = prompt_type
            self.prompts[filename] = prompt_data
            
            self.log(f"✓ Imported prompt: {prompt_data['name']}")
            return True
            
        except Exception as e:
            self.log(f"✗ Import failed: {e}")
            messagebox.showerror("Import Error", f"Failed to import prompt:\n{e}")
            return False
