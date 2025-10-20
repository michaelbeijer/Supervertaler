"""
Configuration Manager for Supervertaler
Handles user data folder location, first-time setup, and configuration persistence.

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
    Manages Supervertaler configuration and user data paths.
    
    Stores configuration in home directory as .supervertaler_config.json
    Allows users to choose their own user data folder location.
    """
    
    CONFIG_FILENAME = ".supervertaler_config.json"
    DEFAULT_USER_DATA_FOLDER = "Supervertaler_Data"
    
    # Folder structure that must exist in user data directory
    REQUIRED_FOLDERS = [
        "Prompt_Library/System_prompts",
        "Prompt_Library/Custom_instructions",
        "Translation_Resources/Glossaries",
        "Translation_Resources/TMs",
        "Translation_Resources/Non-translatables",
        "Translation_Resources/Segmentation_rules",
        "Projects",
    ]
    
    def __init__(self):
        """Initialize ConfigManager."""
        self.config_path = self._get_config_file_path()
        self.config = self._load_config()
    
    @staticmethod
    def _get_config_file_path() -> str:
        """Get the full path to the config file in home directory."""
        home = str(Path.home())
        return os.path.join(home, ConfigManager.CONFIG_FILENAME)
    
    @staticmethod
    def _get_default_user_data_path() -> str:
        """Get the default suggested user data path."""
        home = str(Path.home())
        return os.path.join(home, ConfigManager.DEFAULT_USER_DATA_FOLDER)
    
    def _load_config(self) -> dict:
        """Load configuration from file. Return empty dict if file doesn't exist."""
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
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"[Config] Error saving config: {e}")
            return False
    
    def is_first_launch(self) -> bool:
        """Check if this is the first launch (no user data path set)."""
        return 'user_data_path' not in self.config or not self.config['user_data_path']
    
    def get_user_data_path(self) -> str:
        """
        Get the current user data path.
        
        If not configured, returns default suggestion (doesn't create it).
        Use ensure_user_data_exists() to create the folder.
        """
        if 'user_data_path' in self.config and self.config['user_data_path']:
            return self.config['user_data_path']
        return self._get_default_user_data_path()
    
    def set_user_data_path(self, path: str) -> Tuple[bool, str]:
        """
        Set the user data path and save configuration.
        
        Args:
            path: Full path to user data folder
            
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
        Validate that a path is suitable for user data.
        
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
        Ensure user data folder exists with proper structure.
        
        Creates all required subdirectories if they don't exist.
        
        Args:
            user_data_path: Optional specific path. If None, uses configured path.
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if user_data_path is None:
            user_data_path = self.get_user_data_path()
        
        try:
            # Create root user data folder
            Path(user_data_path).mkdir(parents=True, exist_ok=True)
            
            # Create all required subdirectories
            for folder in self.REQUIRED_FOLDERS:
                folder_path = os.path.join(user_data_path, folder)
                Path(folder_path).mkdir(parents=True, exist_ok=True)
            
            return True, f"User data folder structure created at: {user_data_path}"
        except Exception as e:
            return False, f"Failed to create user data structure: {e}"
    
    def get_subfolder_path(self, subfolder: str) -> str:
        """
        Get the full path to a subfolder in user data.
        
        Example:
            config.get_subfolder_path('Translation_Resources/TMs')
            -> '/home/user/Supervertaler_Data/Translation_Resources/TMs'
        """
        user_data_path = self.get_user_data_path()
        full_path = os.path.join(user_data_path, subfolder)
        
        # Ensure subfolder exists
        Path(full_path).mkdir(parents=True, exist_ok=True)
        
        return full_path
    
    def get_existing_user_data_folder(self) -> Optional[str]:
        """
        Detect if there's existing user data in the script directory (from development).
        
        Returns path if found, None otherwise.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        old_user_data_path = os.path.join(script_dir, "user data")
        
        if os.path.exists(old_user_data_path) and os.path.isdir(old_user_data_path):
            # Check if it has any content
            if os.listdir(old_user_data_path):
                return old_user_data_path
        
        return None
    
    def migrate_user_data(self, old_path: str, new_path: str) -> Tuple[bool, str]:
        """
        Migrate user data from old location to new location.
        
        Args:
            old_path: Current user data location
            new_path: New user data location
            
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
    
    def get_all_config_info(self) -> dict:
        """Get all configuration information for debugging."""
        return {
            'config_file': self.config_path,
            'user_data_path': self.get_user_data_path(),
            'is_first_launch': self.is_first_launch(),
            'config': self.config,
        }


# Convenience function for easy access
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get or create the global ConfigManager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
