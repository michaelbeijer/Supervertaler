"""
File Dialog Helper for Supervertaler
Wraps PyQt6 QFileDialog to remember last used directory across all dialogs.

Author: Michael Beijer
License: MIT
"""

from PyQt6.QtWidgets import QFileDialog, QWidget
from typing import Optional, Tuple, List
from modules.config_manager import get_config_manager


def get_open_file_name(
    parent: Optional[QWidget] = None,
    caption: str = "",
    filter: str = "",
    initial_filter: str = ""
) -> Tuple[str, str]:
    """
    Show an open file dialog that remembers the last directory.
    
    Args:
        parent: Parent widget
        caption: Dialog title
        filter: File type filters (e.g., "Text Files (*.txt);;All Files (*)")
        initial_filter: Initially selected filter
        
    Returns:
        Tuple of (selected_file_path, selected_filter)
    """
    config = get_config_manager()
    start_dir = config.get_last_directory()
    
    file_path, selected_filter = QFileDialog.getOpenFileName(
        parent,
        caption,
        start_dir,
        filter,
        initial_filter
    )
    
    if file_path:
        config.update_last_directory_from_file(file_path)
    
    return file_path, selected_filter


def get_open_file_names(
    parent: Optional[QWidget] = None,
    caption: str = "",
    filter: str = "",
    initial_filter: str = ""
) -> Tuple[List[str], str]:
    """
    Show an open multiple files dialog that remembers the last directory.
    
    Args:
        parent: Parent widget
        caption: Dialog title
        filter: File type filters
        initial_filter: Initially selected filter
        
    Returns:
        Tuple of (list_of_selected_files, selected_filter)
    """
    config = get_config_manager()
    start_dir = config.get_last_directory()
    
    file_paths, selected_filter = QFileDialog.getOpenFileNames(
        parent,
        caption,
        start_dir,
        filter,
        initial_filter
    )
    
    if file_paths:
        config.update_last_directory_from_file(file_paths[0])
    
    return file_paths, selected_filter


def get_save_file_name(
    parent: Optional[QWidget] = None,
    caption: str = "",
    filter: str = "",
    initial_filter: str = ""
) -> Tuple[str, str]:
    """
    Show a save file dialog that remembers the last directory.
    
    Args:
        parent: Parent widget
        caption: Dialog title
        filter: File type filters
        initial_filter: Initially selected filter
        
    Returns:
        Tuple of (selected_file_path, selected_filter)
    """
    config = get_config_manager()
    start_dir = config.get_last_directory()
    
    file_path, selected_filter = QFileDialog.getSaveFileName(
        parent,
        caption,
        start_dir,
        filter,
        initial_filter
    )
    
    if file_path:
        config.update_last_directory_from_file(file_path)
    
    return file_path, selected_filter


def get_existing_directory(
    parent: Optional[QWidget] = None,
    caption: str = "",
    options: QFileDialog.Option = QFileDialog.Option.ShowDirsOnly
) -> str:
    """
    Show a directory selection dialog that remembers the last directory.
    
    Args:
        parent: Parent widget
        caption: Dialog title
        options: Dialog options
        
    Returns:
        Selected directory path
    """
    config = get_config_manager()
    start_dir = config.get_last_directory()
    
    directory = QFileDialog.getExistingDirectory(
        parent,
        caption,
        start_dir,
        options
    )
    
    if directory:
        config.set_last_directory(directory)
    
    return directory
