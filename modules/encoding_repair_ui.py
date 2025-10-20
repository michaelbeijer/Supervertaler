"""
Encoding Repair Tool UI - Menu-based interface for the encoding repair module

Provides a user-friendly GUI for detecting and fixing text encoding corruption.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
from modules.encoding_repair import EncodingRepair


class EncodingRepairWindow:
    """GUI window for encoding repair operations."""
    
    def __init__(self, parent, theme_colors=None):
        """
        Initialize the encoding repair window.
        
        Args:
            parent: Parent tkinter widget
            theme_colors: Optional dict with color scheme
        """
        self.parent = parent
        self.colors = theme_colors or {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'accent': '#0066cc',
            'success': '#4CAF50',
            'error': '#f44336',
            'warning': '#ff9800',
        }
        
        self.window = tk.Toplevel(parent)
        self.window.title("Text Encoding Repair Tool")
        self.window.geometry("700x600")
        self.window.resizable(True, True)
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Text Encoding Corruption Repair",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc = ttk.Label(
            main_frame,
            text="Detects and fixes text encoding issues (mojibake) caused by UTF-8\n"
                 "being incorrectly decoded as Latin-1 or Windows-1252.",
            font=("Arial", 9),
            justify=tk.LEFT,
        )
        desc.pack(pady=(0, 15), fill=tk.X)
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill=tk.X)
        
        self.file_path_var = tk.StringVar()
        ttk.Button(
            button_frame,
            text="📂 Select File",
            command=self._select_file
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="📁 Select Folder",
            command=self._select_folder
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # File path display
        self.path_label = ttk.Label(
            file_frame,
            text="No file selected",
            font=("Arial", 9),
            foreground="#666666"
        )
        self.path_label.pack(pady=(10, 0), fill=tk.X)
        
        # Action buttons frame
        action_frame = ttk.LabelFrame(main_frame, text="Actions", padding=10)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_row1 = ttk.Frame(action_frame)
        button_row1.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            button_row1,
            text="🔍 Scan File",
            command=self._scan_file,
            width=20
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_row1,
            text="🔧 Repair File",
            command=self._repair_file,
            width=20
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        button_row2 = ttk.Frame(action_frame)
        button_row2.pack(fill=tk.X)
        
        ttk.Button(
            button_row2,
            text="📂 Scan Folder",
            command=self._scan_folder,
            width=20
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_row2,
            text="🔧 Repair Folder",
            command=self._repair_folder,
            width=20
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=12,
            font=("Courier New", 9),
            bg="white",
            fg="#333333",
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Add tags for colorization
        self.results_text.tag_config("success", foreground="#4CAF50", font=("Courier New", 9, "bold"))
        self.results_text.tag_config("error", foreground="#f44336", font=("Courier New", 9, "bold"))
        self.results_text.tag_config("warning", foreground="#ff9800", font=("Courier New", 9, "bold"))
        self.results_text.tag_config("info", foreground="#0066cc")
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 8),
            foreground="#666666"
        )
        status_bar.pack(fill=tk.X)
    
    def _select_file(self):
        """Open file selection dialog."""
        file_path = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("TSV files", "*.tsv"),
                ("Markdown files", "*.md"),
                ("All files", "*.*"),
            ]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            self.path_label.config(text=f"📄 {Path(file_path).name}")
            self._update_status(f"Selected: {Path(file_path).name}")
    
    def _select_folder(self):
        """Open folder selection dialog."""
        folder_path = filedialog.askdirectory(title="Select a folder")
        
        if folder_path:
            self.file_path_var.set(folder_path)
            self.path_label.config(text=f"📁 {Path(folder_path).name}")
            self._update_status(f"Selected: {Path(folder_path).name}")
    
    def _scan_file(self):
        """Scan a single file for encoding issues."""
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showwarning("No file selected", "Please select a file first.")
            return
        
        self._clear_results()
        self._update_status("Scanning file...")
        
        def scan():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                has_corruption, count, patterns = EncodingRepair.detect_corruption(content)
                
                # Display results
                self.results_text.insert(tk.END, f"File: {Path(file_path).name}\n", "info")
                self.results_text.insert(tk.END, f"Path: {file_path}\n", "info")
                self.results_text.insert(tk.END, f"Size: {len(content):,} characters\n\n", "info")
                
                if has_corruption:
                    self.results_text.insert(
                        tk.END,
                        f"⚠️  ENCODING CORRUPTION DETECTED\n",
                        "warning"
                    )
                    self.results_text.insert(tk.END, f"Total corruptions: {count}\n\n", "warning")
                    self.results_text.insert(tk.END, "Patterns found:\n", "warning")
                    
                    for i, pattern in enumerate(patterns, 1):
                        self.results_text.insert(tk.END, f"  {i}. {pattern}\n")
                    
                    self.results_text.insert(
                        tk.END,
                        "\n✅ You can repair this file using the 'Repair File' button.\n",
                        "success"
                    )
                else:
                    self.results_text.insert(
                        tk.END,
                        "✅ NO ENCODING CORRUPTION DETECTED\n",
                        "success"
                    )
                    self.results_text.insert(
                        tk.END,
                        "This file appears to be properly encoded.\n",
                        "success"
                    )
                
                self._update_status("Scan complete")
                
            except Exception as e:
                self.results_text.insert(tk.END, f"❌ Error: {str(e)}\n", "error")
                self._update_status("Scan failed")
        
        # Run in background thread
        thread = threading.Thread(target=scan, daemon=True)
        thread.start()
    
    def _repair_file(self):
        """Repair encoding issues in a single file."""
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showwarning("No file selected", "Please select a file first.")
            return
        
        if not Path(file_path).is_file():
            messagebox.showerror("Invalid file", "The selected path is not a file.")
            return
        
        # Confirm before repair
        if not messagebox.askyesno("Confirm Repair", f"Repair {Path(file_path).name}?\n\nA backup will be created."):
            return
        
        self._clear_results()
        self._update_status("Repairing file...")
        
        def repair():
            try:
                # Create backup
                backup_path = f"{file_path}.backup"
                Path(file_path).read_text(encoding='utf-8', errors='ignore')
                with open(file_path, 'rb') as f_src:
                    with open(backup_path, 'wb') as f_dst:
                        f_dst.write(f_src.read())
                
                # Repair
                success, message, info = EncodingRepair.repair_with_encoding_fallback(file_path)
                
                if success:
                    self.results_text.insert(tk.END, message + "\n\n", "success")
                    self.results_text.insert(tk.END, f"Backup created: {backup_path}\n", "info")
                    messagebox.showinfo("Success", f"File repaired successfully!\n\n{message}")
                    self._update_status("File repaired successfully")
                else:
                    self.results_text.insert(tk.END, message + "\n", "error")
                    self._update_status("Repair failed")
                
            except Exception as e:
                error_msg = f"❌ Error during repair: {str(e)}\n"
                self.results_text.insert(tk.END, error_msg, "error")
                messagebox.showerror("Repair Failed", error_msg)
                self._update_status("Repair failed")
        
        # Run in background thread
        thread = threading.Thread(target=repair, daemon=True)
        thread.start()
    
    def _scan_folder(self):
        """Scan a folder for files with encoding issues."""
        folder_path = self.file_path_var.get()
        
        if not folder_path:
            messagebox.showwarning("No folder selected", "Please select a folder first.")
            return
        
        if not Path(folder_path).is_dir():
            messagebox.showerror("Invalid folder", "The selected path is not a folder.")
            return
        
        self._clear_results()
        self._update_status("Scanning folder...")
        
        def scan():
            try:
                results = EncodingRepair.scan_directory(folder_path)
                
                self.results_text.insert(tk.END, f"Folder: {Path(folder_path).name}\n", "info")
                self.results_text.insert(tk.END, f"Path: {folder_path}\n\n", "info")
                self.results_text.insert(tk.END, f"Files scanned: {results['files_scanned']}\n", "info")
                
                if results['files_with_corruption']:
                    self.results_text.insert(
                        tk.END,
                        f"⚠️  Files with corruption: {len(results['files_with_corruption'])}\n",
                        "warning"
                    )
                    self.results_text.insert(
                        tk.END,
                        f"Total corruptions found: {results['total_corruptions']}\n\n",
                        "warning"
                    )
                    
                    for file_info in results['files_with_corruption']:
                        self.results_text.insert(
                            tk.END,
                            f"📄 {Path(file_info['file']).name}\n",
                            "warning"
                        )
                        self.results_text.insert(
                            tk.END,
                            f"   Corruptions: {file_info['corruptions']}\n",
                            "info"
                        )
                        for pattern in file_info['patterns']:
                            self.results_text.insert(tk.END, f"   • {pattern}\n", "info")
                        self.results_text.insert(tk.END, "\n")
                else:
                    self.results_text.insert(
                        tk.END,
                        "✅ NO ENCODING CORRUPTION DETECTED\n",
                        "success"
                    )
                    self.results_text.insert(
                        tk.END,
                        "All files in this folder are properly encoded.\n",
                        "success"
                    )
                
                self._update_status("Folder scan complete")
                
            except Exception as e:
                self.results_text.insert(tk.END, f"❌ Error: {str(e)}\n", "error")
                self._update_status("Scan failed")
        
        # Run in background thread
        thread = threading.Thread(target=scan, daemon=True)
        thread.start()
    
    def _repair_folder(self):
        """Repair encoding issues in all files in a folder."""
        folder_path = self.file_path_var.get()
        
        if not folder_path:
            messagebox.showwarning("No folder selected", "Please select a folder first.")
            return
        
        if not Path(folder_path).is_dir():
            messagebox.showerror("Invalid folder", "The selected path is not a folder.")
            return
        
        # First scan to show what will be repaired
        results = EncodingRepair.scan_directory(folder_path)
        
        if not results['files_with_corruption']:
            messagebox.showinfo("No issues found", "No encoding corruption detected in this folder.")
            return
        
        files_to_repair = len(results['files_with_corruption'])
        if not messagebox.askyesno(
            "Confirm Repair",
            f"Repair {files_to_repair} file(s) with encoding issues?\n\nBackups will be created."
        ):
            return
        
        self._clear_results()
        self._update_status("Repairing folder...")
        
        def repair():
            repaired_count = 0
            failed_count = 0
            
            self.results_text.insert(tk.END, f"Repairing {files_to_repair} file(s)...\n\n", "info")
            
            for file_info in results['files_with_corruption']:
                file_path = file_info['file']
                try:
                    # Create backup
                    backup_path = f"{file_path}.backup"
                    with open(file_path, 'rb') as f_src:
                        with open(backup_path, 'wb') as f_dst:
                            f_dst.write(f_src.read())
                    
                    # Repair
                    success, message, _ = EncodingRepair.repair_with_encoding_fallback(file_path)
                    
                    if success:
                        self.results_text.insert(
                            tk.END,
                            f"✅ {Path(file_path).name}\n",
                            "success"
                        )
                        repaired_count += 1
                    else:
                        self.results_text.insert(
                            tk.END,
                            f"❌ {Path(file_path).name}: {message}\n",
                            "error"
                        )
                        failed_count += 1
                
                except Exception as e:
                    self.results_text.insert(
                        tk.END,
                        f"❌ {Path(file_path).name}: {str(e)}\n",
                        "error"
                    )
                    failed_count += 1
            
            # Summary
            self.results_text.insert(tk.END, f"\n{'='*50}\n", "info")
            self.results_text.insert(
                tk.END,
                f"Repair complete: {repaired_count} succeeded, {failed_count} failed\n",
                "success" if failed_count == 0 else "warning"
            )
            
            self._update_status("Folder repair complete")
            messagebox.showinfo(
                "Repair Complete",
                f"Repaired {repaired_count} file(s)\n"
                f"Failed: {failed_count} file(s)"
            )
        
        # Run in background thread
        thread = threading.Thread(target=repair, daemon=True)
        thread.start()
    
    def _clear_results(self):
        """Clear the results text area."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
    
    def _update_status(self, message: str):
        """Update the status bar."""
        self.status_var.set(message)
        self.window.update()


def open_encoding_repair_tool(parent, theme_colors=None):
    """
    Open the encoding repair tool window.
    
    Args:
        parent: Parent tkinter widget
        theme_colors: Optional dict with color scheme
    """
    window = EncodingRepairWindow(parent, theme_colors)
    return window
