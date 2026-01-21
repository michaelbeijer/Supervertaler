"""
Configuration Manager for Supervertaler
Handles user_data folder location, first-time setup, and configuration persistence.

Author: Michael Beijer
License: MIT
"""

import os
import json
import shutil
from pathlib import Path
from typing import Optional, Tuple


class ConfigManager:
    """
    Manages Supervertaler configuration and user_data paths.
    
    MODES:
    - Dev mode: .supervertaler.local exists → uses user_data_private/ folder (git-ignored)
    - User mode: No .supervertaler.local → uses ~/.supervertaler_config.json to store path
    
    Stores configuration in home directory as .supervertaler_config.json
    Allows users to choose their own user_data folder location.
    """
    
    CONFIG_FILENAME = ".supervertaler_config.json"
    DEFAULT_USER_DATA_FOLDER = "Supervertaler_Data"
    DEV_MODE_FLAG = ".supervertaler.local"
    API_KEYS_EXAMPLE_FILENAME = "api_keys.example.txt"
    API_KEYS_FILENAME = "api_keys.txt"
    
    # Folder structure that must exist in user_data directory
    REQUIRED_FOLDERS = [
        # Note: Old numbered folders (1_System_Prompts, 2_Domain_Prompts, etc.) are deprecated
        # Migration moves them to unified Library structure
        "prompt_library/domain_expertise",
        "prompt_library/project_prompts",
        "prompt_library/style_guides",
        "resources/termbases",
        "resources/tms",
        "resources/non_translatables",
        "resources/segmentation_rules",
        "projects",
    ]
    
    def __init__(self):
        """Initialize ConfigManager."""
        self.dev_mode = self._is_dev_mode()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = self._get_config_file_path()
        self.config = self._load_config()
    
    @staticmethod
    def _is_dev_mode() -> bool:
        """Check if running in dev mode (looking for .supervertaler.local flag)."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)  # Go up one level from modules/
        dev_flag_path = os.path.join(repo_root, ConfigManager.DEV_MODE_FLAG)
        return os.path.exists(dev_flag_path)
    
    def _get_config_file_path(self) -> str:
        """
        Get the full path to the config file.
        
        Dev mode: No config file needed (uses user_data_private/)
        User mode: ~/.supervertaler_config.json
        """
        if self.dev_mode:
            return None  # Dev mode doesn't use config file
        home = str(Path.home())
        return os.path.join(home, ConfigManager.CONFIG_FILENAME)
    
    @staticmethod
    def _get_default_user_data_path() -> str:
        """Get the default suggested user_data path."""
        home = str(Path.home())
        return os.path.join(home, ConfigManager.DEFAULT_USER_DATA_FOLDER)
    
    def _load_config(self) -> dict:
        """Load configuration from file. Return empty dict if file doesn't exist."""
        # Dev mode doesn't use config file
        if self.dev_mode:
            return {}
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"[Config] Error loading config: {e}. Using defaults.")
                return {}
        return {}
    
    def _save_config(self) -> bool:
        """Save configuration to file. Return True if successful."""
        # Dev mode doesn't use config file
        if self.dev_mode:
            return True
        
        if self.config_path is None:
            return False
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"[Config] Error saving config: {e}")
            return False
    
    def is_first_launch(self) -> bool:
        """
        Check if this is the first launch (no user_data path set).
        
        Dev mode: Always False (dev doesn't need first-launch wizard)
        User mode: True if no path in config
        """
        if self.dev_mode:
            return False
        return 'user_data_path' not in self.config or not self.config['user_data_path']
    
    def get_user_data_path(self) -> str:
        """
        Get the current user_data path.
        
        Dev mode: Returns ./user_data_private/ (in repo root)
        User mode: Returns configured path from ~/.supervertaler_config.json
        
        If not configured, returns default suggestion (doesn't create it).
        Use ensure_user_data_exists() to create the folder.
        """
        if self.dev_mode:
            # Dev mode: use user_data_private folder
            repo_root = os.path.dirname(self.script_dir)
            return os.path.join(repo_root, "user_data_private")
        
        # User mode: use configured path
        if 'user_data_path' in self.config and self.config['user_data_path']:
            return self.config['user_data_path']
        return self._get_default_user_data_path()
    
    def set_user_data_path(self, path: str) -> Tuple[bool, str]:
        """
        Set the user_data path and save configuration.
        
        Args:
            path: Full path to user_data folder
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate path
        is_valid, error_msg = self._validate_path(path)
        if not is_valid:
            return False, error_msg
        
        # Normalize path
        path = os.path.normpath(path)
        
        # Save configuration
        self.config['user_data_path'] = path
        self.config['last_modified'] = str(Path.ctime(Path(self.config_path))) if os.path.exists(self.config_path) else None
        
        if self._save_config():
            return True, f"User data path set to: {path}"
        else:
            return False, "Failed to save configuration"
    
    @staticmethod
    def _validate_path(path: str) -> Tuple[bool, str]:
        """
        Validate that a path is suitable for user_data.
        
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if not path or not isinstance(path, str):
            return False, "Path must be a non-empty string"
        
        try:
            path_obj = Path(path)
            
            # Try to create the path
            path_obj.mkdir(parents=True, exist_ok=True)
            
            # Check if writable
            test_file = path_obj / ".supervertaler_test"
            test_file.touch()
            test_file.unlink()
            
            return True, ""
        except PermissionError:
            return False, f"Permission denied: Cannot write to {path}"
        except OSError as e:
            return False, f"Invalid path: {e}"
    
    def ensure_user_data_exists(self, user_data_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        Ensure user_data folder exists with proper structure.
        
        Creates all required subdirectories if they don't exist.
        Also copies api_keys.example.txt → api_keys.txt if not present.
        
        Args:
            user_data_path: Optional specific path. If None, uses configured path.
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if user_data_path is None:
            user_data_path = self.get_user_data_path()
        
        try:
            # Create root user_data folder
            Path(user_data_path).mkdir(parents=True, exist_ok=True)
            
            # Create all required subdirectories
            for folder in self.REQUIRED_FOLDERS:
                folder_path = os.path.join(user_data_path, folder)
                Path(folder_path).mkdir(parents=True, exist_ok=True)
            
            # Copy api_keys.example.txt if it exists and api_keys.txt doesn't
            self._setup_api_keys(user_data_path)
            
            return True, f"User data folder structure created at: {user_data_path}"
        except Exception as e:
            return False, f"Failed to create user_data structure: {e}"
    
    def _setup_api_keys(self, user_data_path: str) -> Tuple[bool, str]:
        """
        Copy api_keys.example.txt to api_keys.txt in user_data folder.
        
        Only creates if api_keys.txt doesn't already exist.
        """
        try:
            # Get paths
            repo_root = os.path.dirname(self.script_dir)
            example_source = os.path.join(repo_root, self.API_KEYS_EXAMPLE_FILENAME)
            api_keys_dest = os.path.join(user_data_path, self.API_KEYS_FILENAME)
            
            # If api_keys.txt already exists, nothing to do
            if os.path.exists(api_keys_dest):
                return True, "api_keys.txt already exists"
            
            # If example file exists, copy it
            if os.path.exists(example_source):
                shutil.copy2(example_source, api_keys_dest)
                print(f"[Config] Created {api_keys_dest} from template")
                return True, f"Created api_keys.txt from template"
            else:
                # Create empty api_keys.txt with instructions
                with open(api_keys_dest, 'w', encoding='utf-8') as f:
                    f.write("# API Keys Configuration\n")
                    f.write("# Add your API keys here in the format: KEY_NAME=value\n")
                    f.write("# Example:\n")
                    f.write("# OPENAI_API_KEY=sk-...\n")
                    f.write("# ANTHROPIC_API_KEY=sk-ant-...\n\n")
                print(f"[Config] Created empty {api_keys_dest} with instructions")
                return True, "Created api_keys.txt with instructions"
        except Exception as e:
            print(f"[Config] Error setting up api_keys: {e}")
            return False, f"Failed to setup api_keys.txt: {e}"
    
    def get_subfolder_path(self, subfolder: str) -> str:
        """
        Get the full path to a subfolder in user_data.
        
        Example:
            config.get_subfolder_path('resources/tms')
            -> '/home/user/Supervertaler/resources/tms'
        """
        user_data_path = self.get_user_data_path()
        full_path = os.path.join(user_data_path, subfolder)
        
        # Ensure subfolder exists
        Path(full_path).mkdir(parents=True, exist_ok=True)
        
        return full_path
    
    def get_existing_user_data_folder(self) -> Optional[str]:
        """
        Detect if there's existing user_data in the script directory (from development).
        
        Returns path if found, None otherwise.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        old_user_data_path = os.path.join(script_dir, "user_data")
        
        if os.path.exists(old_user_data_path) and os.path.isdir(old_user_data_path):
            # Check if it has any content
            if os.listdir(old_user_data_path):
                return old_user_data_path
        
        return None
    
    def migrate_user_data(self, old_path: str, new_path: str) -> Tuple[bool, str]:
        """
        Migrate user_data from old location to new location.
        
        Also handles migration of api_keys.txt if it exists in old location.
        
        Args:
            old_path: Current user_data location
            new_path: New user_data location
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not os.path.exists(old_path):
            return False, f"Old path does not exist: {old_path}"
        
        try:
            # Ensure new location exists
            Path(new_path).mkdir(parents=True, exist_ok=True)
            
            # Move all items from old to new
            files_moved = 0
            for item in os.listdir(old_path):
                old_item_path = os.path.join(old_path, item)
                new_item_path = os.path.join(new_path, item)
                
                # Skip if item already exists at destination
                if os.path.exists(new_item_path):
                    print(f"[Migration] Skipping (exists): {item}")
                    continue
                
                try:
                    if os.path.isdir(old_item_path):
                        shutil.copytree(old_item_path, new_item_path)
                    else:
                        shutil.copy2(old_item_path, new_item_path)
                    files_moved += 1
                except Exception as e:
                    print(f"[Migration] Error moving {item}: {e}")
                    continue
            
            return True, f"Migrated {files_moved} items from {old_path} to {new_path}"
        except Exception as e:
            return False, f"Migration failed: {e}"
    
    def migrate_api_keys_from_installation(self, user_data_path: str) -> Tuple[bool, str]:
        """
        Migrate api_keys.txt from installation folder to user_data folder if it exists.
        
        This handles migration for users upgrading from older versions.
        
        Args:
            user_data_path: Target user_data folder
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            repo_root = os.path.dirname(self.script_dir)
            old_api_keys = os.path.join(repo_root, self.API_KEYS_FILENAME)
            new_api_keys = os.path.join(user_data_path, self.API_KEYS_FILENAME)
            
            # If old api_keys.txt exists and new one doesn't, move it
            if os.path.exists(old_api_keys) and not os.path.exists(new_api_keys):
                shutil.copy2(old_api_keys, new_api_keys)
                print(f"[Migration] Migrated api_keys.txt to {new_api_keys}")
                return True, f"Migrated api_keys.txt to user_data folder"
            
            return True, "api_keys.txt migration not needed"
        except Exception as e:
            print(f"[Migration] Error migrating api_keys.txt: {e}")
            return False, f"Failed to migrate api_keys.txt: {e}"
    
    def validate_current_path(self) -> Tuple[bool, str]:
        """
        Validate that the currently configured path is still valid.
        
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        user_data_path = self.get_user_data_path()
        
        # Check if path exists and is writable
        if not os.path.exists(user_data_path):
            return False, f"User data path no longer exists: {user_data_path}"
        
        try:
            # Try to write test file
            test_file = os.path.join(user_data_path, ".supervertaler_test")
            Path(test_file).touch()
            Path(test_file).unlink()
            return True, ""
        except Exception as e:
            return False, f"User data path is not writable: {e}"
    
    def get_preferences_path(self) -> str:
        """Get the path to the UI preferences file."""
        user_data_path = self.get_user_data_path()
        return os.path.join(user_data_path, 'ui_preferences.json')
    
    def load_preferences(self) -> dict:
        """Load UI preferences from file."""
        prefs_path = self.get_preferences_path()
        if os.path.exists(prefs_path):
            try:
                with open(prefs_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"[Config] Error loading preferences: {e}")
        return {}
    
    def save_preferences(self, preferences: dict) -> bool:
        """Save UI preferences to file."""
        prefs_path = self.get_preferences_path()
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(prefs_path), exist_ok=True)
            with open(prefs_path, 'w', encoding='utf-8') as f:
                json.dump(preferences, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"[Config] Error saving preferences: {e}")
            return False
    
    def get_all_config_info(self) -> dict:
        """Get all configuration information for debugging."""
        return {
            'config_file': self.config_path,
            'user_data_path': self.get_user_data_path(),
            'is_first_launch': self.is_first_launch(),
            'config': self.config,
        }
    
    def get_last_directory(self) -> str:
        """
        Get the last directory used in file dialogs.
        Returns empty string if no directory has been saved yet.
        """
        return self.config.get('last_directory', '')
    
    def set_last_directory(self, directory: str) -> None:
        """
        Save the last directory used in file dialogs.
        
        Args:
            directory: Full path to the directory to remember
        """
        if directory and os.path.isdir(directory):
            self.config['last_directory'] = os.path.normpath(directory)
            self._save_config()
    
    def update_last_directory_from_file(self, file_path: str) -> None:
        """
        Extract and save the directory from a file path.
        
        Args:
            file_path: Full path to a file
        """
        if file_path:
            directory = os.path.dirname(file_path)
            self.set_last_directory(directory)


# Convenience function for easy access
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get or create the global ConfigManager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
