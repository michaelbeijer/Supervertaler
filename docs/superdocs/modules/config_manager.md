# config_manager

**File:** `modules/config_manager.py`
**Lines:** 469
**Classes:** 1
**Functions:** 1

---

## Module Description

Configuration Manager for Supervertaler
Handles user_data folder location, first-time setup, and configuration persistence.

Author: Michael Beijer
License: MIT

---

## Classes

### `ConfigManager`

**Line:** 16

Manages Supervertaler configuration and user_data paths.

MODES:
- Dev mode: .supervertaler.local exists → uses user_data_private/ folder (git-ignored)
- User mode: No .supervertaler.local → uses ~/.supervertaler_config.json to store path

Stores configuration in home directory as .supervertaler_config.json
Allows users to choose their own user_data folder location.

#### Methods

##### `is_first_launch()`

Check if this is the first launch (no user_data path set).

Dev mode: Always False (dev doesn't need first-launch wizard)
User mode: True if no path in config

##### `get_user_data_path()`

Get the current user_data path.

Dev mode: Returns ./user_data_private/ (in repo root)
User mode: Returns configured path from ~/.supervertaler_config.json

If not configured, returns default suggestion (doesn't create it).
Use ensure_user_data_exists() to create the folder.

##### `set_user_data_path()`

Set the user_data path and save configuration.

Args:
    path: Full path to user_data folder
    
Returns:
    Tuple of (success: bool, message: str)

##### `ensure_user_data_exists()`

Ensure user_data folder exists with proper structure.

Creates all required subdirectories if they don't exist.
Also copies api_keys.example.txt → api_keys.txt if not present.

Args:
    user_data_path: Optional specific path. If None, uses configured path.
    
Returns:
    Tuple of (success: bool, message: str)

##### `get_subfolder_path()`

Get the full path to a subfolder in user_data.

Example:
    config.get_subfolder_path('Translation_Resources/TMs')
    -> '/home/user/Supervertaler_Data/Translation_Resources/TMs'

##### `get_existing_user_data_folder()`

Detect if there's existing user_data in the script directory (from development).

Returns path if found, None otherwise.

##### `migrate_user_data()`

Migrate user_data from old location to new location.

Also handles migration of api_keys.txt if it exists in old location.

Args:
    old_path: Current user_data location
    new_path: New user_data location
    
Returns:
    Tuple of (success: bool, message: str)

##### `migrate_api_keys_from_installation()`

Migrate api_keys.txt from installation folder to user_data folder if it exists.

This handles migration for users upgrading from older versions.

Args:
    user_data_path: Target user_data folder
    
Returns:
    Tuple of (success: bool, message: str)

##### `validate_current_path()`

Validate that the currently configured path is still valid.

Returns:
    Tuple of (is_valid: bool, error_message: str)

##### `get_preferences_path()`

Get the path to the UI preferences file.

##### `load_preferences()`

Load UI preferences from file.

##### `save_preferences()`

Save UI preferences to file.

##### `get_all_config_info()`

Get all configuration information for debugging.

##### `get_last_directory()`

Get the last directory used in file dialogs.
Returns empty string if no directory has been saved yet.

##### `set_last_directory()`

Save the last directory used in file dialogs.

Args:
    directory: Full path to the directory to remember

##### `update_last_directory_from_file()`

Extract and save the directory from a file path.

Args:
    file_path: Full path to a file


---

## Functions

### `get_config_manager()`

**Line:** 464

Get or create the global ConfigManager instance.

---

