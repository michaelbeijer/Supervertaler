"""
Setup Wizard for Supervertaler First Launch
Guides new users to select their user data folder location.

Author: Michael Beijer
License: MIT
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional, Tuple
from modules.config_manager import ConfigManager


class SetupWizard:
    """
    First-launch setup wizard for Supervertaler.
    
    Guides users through:
    1. Welcome and explanation
    2. Folder selection
    3. Migration of existing data (if applicable)
    4. Confirmation
    """
    
    def __init__(self, parent_window: Optional[tk.Tk] = None):
        """
        Initialize the setup wizard.
        
        Args:
            parent_window: Parent tkinter window (optional)
        """
        self.config = ConfigManager()
        self.parent = parent_window
        self.selected_path = None
        self.should_migrate = False
        self.migration_source = None
    
    def run(self) -> Tuple[bool, str]:
        """
        Run the full setup wizard.
        
        Returns:
            Tuple of (success: bool, user_data_path: str)
        """
        # Create root window if no parent
        if self.parent is None:
            root = tk.Tk()
            root.withdraw()  # Hide until needed
            self.parent = root
            cleanup_root = True
        else:
            cleanup_root = False
        
        try:
            # Step 1: Welcome
            self._show_welcome()
            
            # Step 2: Select folder
            self.selected_path = self._select_folder()
            if self.selected_path is None:
                # User cancelled
                messagebox.showinfo(
                    "Setup Cancelled",
                    "Supervertaler setup was cancelled. The application will exit."
                )
                return False, ""
            
            # Step 3: Check for existing data to migrate
            existing_data = self.config.get_existing_user_data_folder()
            if existing_data:
                self.should_migrate = self._ask_migrate(existing_data)
                if self.should_migrate:
                    self.migration_source = existing_data
            
            # Step 3b: Show confirmation of what will be created
            confirm_message = (
                "Supervertaler will create the following structure:\n\n"
                f"{self.selected_path}\n"
                f"  ├── api_keys.txt\n"
                f"  ├── Prompt_Library/\n"
                f"  │   ├── System_prompts/\n"
                f"  │   └── Custom_instructions/\n"
                f"  ├── Translation_Resources/\n"
                f"  │   ├── TMs/\n"
                f"  │   ├── Glossaries/\n"
                f"  │   ├── Non-translatables/\n"
                f"  │   └── Segmentation_rules/\n"
                f"  └── Projects/\n\n"
                "Is this correct?"
            )
            
            if not messagebox.askyesno("Confirm Folder Location", confirm_message):
                # User wants to go back and select again
                self.selected_path = self._select_folder()
                if self.selected_path is None:
                    messagebox.showinfo("Setup Cancelled", "Supervertaler setup was cancelled.")
                    return False, ""
                # Loop back to confirmation by recursing (or just continue with the new path)
            
            # Step 4: Validate and create folder structure
            success, message = self.config.ensure_user_data_exists(self.selected_path)
            if not success:
                messagebox.showerror("Setup Error", f"Failed to create folder structure:\n{message}")
                return False, ""
            
            # Step 5: Perform migration if needed
            if self.should_migrate and self.migration_source:
                success, message = self.config.migrate_user_data(
                    self.migration_source,
                    self.selected_path
                )
                if not success:
                    messagebox.showwarning(
                        "Migration Incomplete",
                        f"Partial migration occurred.\n{message}"
                    )
                else:
                    messagebox.showinfo("Migration Complete", message)
            
            # Step 5b: Migrate api_keys.txt from installation folder if needed
            success, message = self.config.migrate_api_keys_from_installation(self.selected_path)
            if success and "Migrated" in message:
                messagebox.showinfo("API Keys Migrated", message)
            
            # Step 6: Save configuration
            success, message = self.config.set_user_data_path(self.selected_path)
            if not success:
                messagebox.showerror("Configuration Error", f"Failed to save configuration:\n{message}")
                return False, ""
            
            # Success!
            messagebox.showinfo(
                "Setup Complete",
                f"✅ Supervertaler is ready!\n\n"
                f"Your data folder: {self.selected_path}\n\n"
                f"Created:\n"
                f"  • api_keys.txt (add your API keys here)\n"
                f"  • Prompt_Library/ (your prompts)\n"
                f"  • Translation_Resources/ (TMs, glossaries)\n"
                f"  • Projects/ (your work)\n\n"
                f"All your translation memories, prompts, and projects\n"
                f"will be stored in this location."
            )
            
            return True, self.selected_path
        
        finally:
            if cleanup_root:
                self.parent.destroy()
    
    def _show_welcome(self):
        """Show welcome dialog explaining what's happening."""
        welcome_message = (
            "Welcome to Supervertaler!\n\n"
            "This is your first launch. We need to set up your data folder.\n\n"
            "This folder is where Supervertaler will store:\n"
            "  • api_keys.txt (your API credentials)\n"
            "  • Translation Memories (TMs)\n"
            "  • Glossaries and Non-translatables\n"
            "  • System Prompts and Custom Instructions\n"
            "  • Your translation projects\n"
            "  • Segmentation rules\n"
            "  • Session reports and configuration\n\n"
            "IMPORTANT: Select a NEW or EMPTY folder location.\n"
            "Examples: Documents/Supervertaler_Data or Desktop/Supervertaler\n\n"
            "Supervertaler will automatically create the full folder\n"
            "structure inside the location you select.\n\n"
            "Click OK to browse for your folder location."
        )
        
        messagebox.showinfo("First Time Setup", welcome_message)
    
    def _select_folder(self) -> Optional[str]:
        """
        Show folder browser dialog and return selected path.
        
        Returns:
            Selected folder path, or None if cancelled
        """
        default_path = self.config._get_default_user_data_path()
        
        folder_selected = filedialog.askdirectory(
            title="Select WHERE to create your Supervertaler Data Folder\n(e.g., Documents or Desktop - NOT the program folder)",
            initialdir=str(Path.home()),
            mustexist=False
        )
        
        if not folder_selected:
            return None
        
        # Normalize path
        return os.path.normpath(folder_selected)
    
    def _ask_migrate(self, existing_data_path: str) -> bool:
        """
        Ask user if they want to migrate existing data.
        
        Args:
            existing_data_path: Path to existing user data
            
        Returns:
            True if user wants to migrate, False otherwise
        """
        migrate_message = (
            "We found your existing Supervertaler data!\n\n"
            f"Location: {existing_data_path}\n\n"
            "Would you like to move this data to your new location?\n\n"
            "Click YES to migrate your data to the new folder.\n"
            "Click NO to start fresh (data will remain in old location)."
        )
        
        result = messagebox.askyesno(
            "Migrate Existing Data?",
            migrate_message,
            default=True
        )
        
        return result


class SetupWizardWindow:
    """
    Alternative: Full window-based setup wizard (more elegant, optional).
    Can be used instead of dialog-based approach.
    """
    
    def __init__(self, on_complete_callback=None):
        """
        Initialize window-based setup wizard.
        
        Args:
            on_complete_callback: Function to call when setup completes
                                 Receives (success: bool, path: str)
        """
        self.config = ConfigManager()
        self.on_complete = on_complete_callback
        self.window = None
        self.selected_path = None
        self.current_step = 1
    
    def run(self) -> Tuple[bool, str]:
        """Run the window-based wizard."""
        self.window = tk.Tk()
        self.window.title("Supervertaler - First Time Setup")
        self.window.geometry("600x400")
        self.window.resizable(False, False)
        
        # Center window on screen
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (300)
        y = (self.window.winfo_screenheight() // 2) - (200)
        self.window.geometry(f"+{x}+{y}")
        
        self._show_step_1()
        self.window.mainloop()
        
        return getattr(self, '_result', (False, ""))
    
    def _show_step_1(self):
        """Show welcome/explanation step."""
        for widget in self.window.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(
            frame,
            text="Welcome to Supervertaler!",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)
        
        explanation = tk.Label(
            frame,
            text=(
                "This is your first launch.\n\n"
                "Supervertaler needs to know where to store your data:\n"
                "• Translation Memories\n"
                "• Glossaries\n"
                "• Prompts and Instructions\n"
                "• Projects\n\n"
                "You can choose any location you prefer.\n"
                "Popular choices: Documents folder or Desktop."
            ),
            font=("Arial", 11),
            justify=tk.LEFT
        )
        explanation.pack(pady=20, anchor=tk.W)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=self._cancel,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Continue →",
            command=self._show_step_2,
            width=10
        ).pack(side=tk.RIGHT, padx=5)
    
    def _show_step_2(self):
        """Show folder selection step."""
        # Implementation similar to dialog version
        # For brevity, using standard filedialog
        folder = filedialog.askdirectory(
            title="Select User Data Folder"
        )
        
        if folder:
            self.selected_path = os.path.normpath(folder)
            self._show_step_3()
        else:
            self._cancel()
    
    def _show_step_3(self):
        """Show confirmation and complete setup."""
        # Create folders and save config
        success, message = self.config.ensure_user_data_exists(self.selected_path)
        if success:
            self.config.set_user_data_path(self.selected_path)
            self._result = (True, self.selected_path)
            
            messagebox.showinfo(
                "Setup Complete",
                f"Your data folder is ready!\n{self.selected_path}"
            )
        else:
            messagebox.showerror("Setup Error", message)
            self._result = (False, "")
        
        if self.on_complete:
            self.on_complete(*self._result)
        
        self.window.quit()
    
    def _cancel(self):
        """Cancel setup."""
        self._result = (False, "")
        if self.on_complete:
            self.on_complete(*self._result)
        self.window.quit()
