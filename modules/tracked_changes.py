"""
Tracked Changes Management Module

This module handles tracked changes from DOCX files or TSV files.
Provides AI with examples of preferred editing patterns to learn translator style.

Classes:
    - TrackedChangesAgent: Manages tracked changes data and provides search/filtering
    - TrackedChangesBrowser: UI window for browsing and analyzing tracked changes
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
import queue
from datetime import datetime
from typing import List, Tuple, Dict, Optional

# Import parse_docx_pairs from the parent modules (it's a standalone function)
# Note: This will be imported from the main file
# For now, we'll assume it's available in the calling context


class TrackedChangesAgent:
    """
    Manages tracked changes from DOCX files or TSV files.
    Provides AI with examples of preferred editing patterns to learn translator style.
    """
    def __init__(self, log_callback=None):
        self.change_data = []  # List of (original_text, final_text) tuples
        self.files_loaded = []  # Track which files have been loaded
        self.log_callback = log_callback or print
    
    def log(self, message):
        """Log a message"""
        if callable(self.log_callback):
            self.log_callback(message)
    
    def load_docx_changes(self, docx_path, parse_docx_pairs_func):
        """Load tracked changes from a DOCX file
        
        Args:
            docx_path: Path to DOCX file
            parse_docx_pairs_func: Function to parse DOCX and extract change pairs
        """
        if not docx_path:
            return False
            
        self.log(f"[Tracked Changes] Loading changes from: {os.path.basename(docx_path)}")
        
        try:
            new_changes = parse_docx_pairs_func(docx_path)
            
            # Clear existing changes to prevent duplicates
            self.change_data.clear()
            self.files_loaded.clear()
            
            # Add new changes
            self.change_data.extend(new_changes)
            self.files_loaded.append(os.path.basename(docx_path))
            
            self.log(f"[Tracked Changes] Loaded {len(new_changes)} change pairs from {os.path.basename(docx_path)}")
            self.log(f"[Tracked Changes] Total change pairs available: {len(self.change_data)}")
            
            return True
        except Exception as e:
            self.log(f"[Tracked Changes] Error loading {docx_path}: {e}")
            messagebox.showerror("Tracked Changes Error", 
                               f"Failed to load tracked changes from {os.path.basename(docx_path)}:\\n{e}")
            return False
    
    def load_tsv_changes(self, tsv_path):
        """Load tracked changes from a TSV file (original_text<tab>final_text format)"""
        if not tsv_path:
            return False
            
        self.log(f"[Tracked Changes] Loading changes from: {os.path.basename(tsv_path)}")
        
        try:
            new_changes = []
            with open(tsv_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.rstrip('\n\r')
                    if not line.strip():
                        continue
                    
                    # Skip header line if it looks like one
                    if line_num == 1 and ('original' in line.lower() and 'final' in line.lower()):
                        continue
                    
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        original = parts[0].strip()
                        final = parts[1].strip()
                        if original and final and original != final:  # Only add if actually different
                            new_changes.append((original, final))
                    else:
                        self.log(f"[Tracked Changes] Skipping line {line_num}: insufficient columns")
            
            # Add to existing changes
            self.change_data.extend(new_changes)
            self.files_loaded.append(os.path.basename(tsv_path))
            
            self.log(f"[Tracked Changes] Loaded {len(new_changes)} change pairs from {os.path.basename(tsv_path)}")
            self.log(f"[Tracked Changes] Total change pairs available: {len(self.change_data)}")
            
            return True
        except Exception as e:
            self.log(f"[Tracked Changes] Error loading {tsv_path}: {e}")
            messagebox.showerror("Tracked Changes Error", 
                               f"Failed to load tracked changes from {os.path.basename(tsv_path)}:\\n{e}")
            return False
    
    def clear_changes(self):
        """Clear all loaded tracked changes"""
        self.change_data.clear()
        self.files_loaded.clear()
        self.log("[Tracked Changes] All tracked changes cleared")
    
    def search_changes(self, search_text, exact_match=False):
        """Search for changes containing the search text"""
        if not search_text.strip():
            return self.change_data
        
        search_lower = search_text.lower()
        results = []
        
        for original, final in self.change_data:
            if exact_match:
                if search_text == original or search_text == final:
                    results.append((original, final))
            else:
                if (search_lower in original.lower() or 
                    search_lower in final.lower()):
                    results.append((original, final))
        
        return results

    def find_relevant_changes(self, source_segments, max_changes=10):
        """
        Find tracked changes relevant to the current source segments being processed.
        Uses two-pass algorithm: exact matches first, then partial word overlap.
        """
        if not self.change_data or not source_segments:
            return []
        
        relevant_changes = []
        
        # First pass: exact matches
        for segment in source_segments:
            segment_lower = segment.lower().strip()
            for original, final in self.change_data:
                original_lower = original.lower().strip()
                if segment_lower == original_lower and (original, final) not in relevant_changes:
                    relevant_changes.append((original, final))
                    if len(relevant_changes) >= max_changes:
                        return relevant_changes
        
        # Second pass: partial matches (word overlap)
        if len(relevant_changes) < max_changes:
            for segment in source_segments:
                segment_words = set(word.lower() for word in segment.split() if len(word) > 3)
                for original, final in self.change_data:
                    if (original, final) in relevant_changes:
                        continue
                    
                    original_words = set(word.lower() for word in original.split() if len(word) > 3)
                    # Check if there's significant word overlap
                    if segment_words and original_words:
                        overlap = len(segment_words.intersection(original_words))
                        min_overlap = min(2, len(segment_words) // 2)
                        if overlap >= min_overlap:
                            relevant_changes.append((original, final))
                            if len(relevant_changes) >= max_changes:
                                return relevant_changes
        
        return relevant_changes
    
    def get_entry_count(self):
        """Get number of loaded change pairs"""
        return len(self.change_data)


class TrackedChangesBrowser:
    """Browser UI for viewing and searching tracked changes"""
    
    def __init__(self, parent, tracked_changes_agent, parent_app=None, log_queue=None, 
                 gemini_available=False, anthropic_available=False, openai_available=False, app_version="3.6.0"):
        self.parent = parent
        self.tracked_changes_agent = tracked_changes_agent
        self.parent_app = parent_app  # Reference to main app for AI settings
        self.log_queue = log_queue if log_queue else queue.Queue()
        self.window = None
        
        # AI availability flags
        self.GEMINI_AVAILABLE = gemini_available
        self.ANTHROPIC_AVAILABLE = anthropic_available
        self.OPENAI_AVAILABLE = openai_available
        self.APP_VERSION = app_version
    
    def show_browser(self):
        """Show the tracked changes browser window"""
        if not self.tracked_changes_agent.change_data:
            messagebox.showinfo("No Changes", "No tracked changes loaded. Load a DOCX or TSV file with tracked changes first.")
            return
        
        # Create window if it doesn't exist
        if self.window is None or not self.window.winfo_exists():
            self.create_window()
        else:
            self.window.lift()
    
    def create_window(self):
        """Create the browser window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Tracked Changes Browser ({len(self.tracked_changes_agent.change_data)} pairs)")
        self.window.geometry("900x700")  # Taller to accommodate detail view
        
        # Search frame
        search_frame = tk.Frame(self.window)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(5,0))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        self.exact_match_var = tk.BooleanVar()
        tk.Checkbutton(search_frame, text="Exact match", variable=self.exact_match_var, 
                      command=self.on_search).pack(side=tk.LEFT, padx=(10,0))
        
        tk.Button(search_frame, text="Clear", command=self.clear_search).pack(side=tk.LEFT, padx=(10,0))
        
        # Results info
        self.results_label = tk.Label(self.window, text="")
        self.results_label.pack(pady=2)
        
        # Main content frame (results + detail)
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results frame with scrollbar (top half)
        results_frame = tk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for displaying changes
        columns = ('Original', 'Final')
        self.tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=12)
        
        # Define headings
        self.tree.heading('Original', text='Original Text')
        self.tree.heading('Final', text='Final Text')
        
        # Configure column widths
        self.tree.column('Original', width=400)
        self.tree.column('Final', width=400)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack tree and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Detail view frame (bottom half)
        detail_frame = tk.LabelFrame(main_frame, text="Selected Change Details", padx=5, pady=5)
        detail_frame.pack(fill=tk.BOTH, expand=False, pady=(10,0))
        
        # Original text display
        tk.Label(detail_frame, text="Original Text:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.original_text = tk.Text(detail_frame, height=4, wrap=tk.WORD, state="disabled", 
                                    bg="#f8f8f8", relief="solid", borderwidth=1)
        self.original_text.pack(fill=tk.X, pady=(2,5))
        
        # Final text display
        tk.Label(detail_frame, text="Final Text:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.final_text = tk.Text(detail_frame, height=4, wrap=tk.WORD, state="disabled",
                                 bg="#f0f8ff", relief="solid", borderwidth=1)
        self.final_text.pack(fill=tk.X, pady=(2,0))
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_selection_change)
        
        # Context menu for copying
        self.context_menu = tk.Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="Copy original", command=self.copy_original)
        self.context_menu.add_command(label="Copy final", command=self.copy_final)
        self.context_menu.add_command(label="Copy both", command=self.copy_both)
        
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right click
        
        # Export button frame
        export_frame = tk.Frame(self.window)
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(export_frame, text="📊 Export Report (MD)", command=self.export_to_md_report,
                 bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                 relief="raised", padx=10, pady=5).pack(side=tk.LEFT)
        
        tk.Label(export_frame, text="Export tracked changes report with AI-powered change analysis",
                fg="gray").pack(side=tk.LEFT, padx=(10,0))
        
        # Status bar
        status_frame = tk.Frame(self.window)
        status_frame.pack(fill=tk.X, padx=10, pady=2)
        
        files_text = f"Files loaded: {', '.join(self.tracked_changes_agent.files_loaded)}" if self.tracked_changes_agent.files_loaded else "No files loaded"
        tk.Label(status_frame, text=files_text, anchor=tk.W).pack(fill=tk.X)
        
        # Load all changes initially
        self.load_results(self.tracked_changes_agent.change_data)
    
    def on_selection_change(self, event=None):
        """Handle selection change in the tree"""
        selection = self.tree.selection()
        if not selection:
            # Clear detail view if no selection
            self.original_text.config(state="normal")
            self.original_text.delete(1.0, tk.END)
            self.original_text.config(state="disabled")
            self.final_text.config(state="normal")
            self.final_text.delete(1.0, tk.END)
            self.final_text.config(state="disabled")
            return
        
        # Get the selected change pair
        original, final = self.get_selected_change()
        if original and final:
            # Update original text display
            self.original_text.config(state="normal")
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(1.0, original)
            self.original_text.config(state="disabled")
            
            # Update final text display
            self.final_text.config(state="normal")
            self.final_text.delete(1.0, tk.END)
            self.final_text.insert(1.0, final)
            self.final_text.config(state="disabled")
    
    def on_search(self, event=None):
        """Handle search input"""
        search_text = self.search_var.get()
        exact_match = self.exact_match_var.get()
        
        results = self.tracked_changes_agent.search_changes(search_text, exact_match)
        self.load_results(results)
    
    def clear_search(self):
        """Clear search and show all results"""
        self.search_var.set("")
        self.load_results(self.tracked_changes_agent.change_data)
    
    def load_results(self, results):
        """Load results into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        for i, (original, final) in enumerate(results):
            # Truncate long text for display
            display_original = (original[:100] + "...") if len(original) > 100 else original
            display_final = (final[:100] + "...") if len(final) > 100 else final
            
            self.tree.insert('', 'end', values=(display_original, display_final))
        
        # Update results label
        total_changes = len(self.tracked_changes_agent.change_data)
        showing = len(results)
        if showing == total_changes:
            self.results_label.config(text=f"Showing all {total_changes} change pairs")
        else:
            self.results_label.config(text=f"Showing {showing} of {total_changes} change pairs")
    
    def show_context_menu(self, event):
        """Show context menu for copying"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def get_selected_change(self):
        """Get the currently selected change pair"""
        selection = self.tree.selection()
        if not selection:
            return None, None
        
        item = selection[0]
        index = self.tree.index(item)
        
        # Get current results (might be filtered)
        search_text = self.search_var.get()
        exact_match = self.exact_match_var.get()
        current_results = self.tracked_changes_agent.search_changes(search_text, exact_match)
        
        if 0 <= index < len(current_results):
            return current_results[index]
        return None, None
    
    def copy_original(self):
        """Copy original text to clipboard"""
        original, _ = self.get_selected_change()
        if original:
            self.window.clipboard_clear()
            self.window.clipboard_append(original)
    
    def copy_final(self):
        """Copy final text to clipboard"""
        _, final = self.get_selected_change()
        if final:
            self.window.clipboard_clear()
            self.window.clipboard_append(final)
    
    def copy_both(self):
        """Copy both texts to clipboard"""
        original, final = self.get_selected_change()
        if original and final:
            both_text = f"Original: {original}\n\nFinal: {final}"
            self.window.clipboard_clear()
            self.window.clipboard_append(both_text)

    
    def export_to_md_report(self):
        """Export tracked changes to a Markdown report with AI-powered change analysis"""
        if not self.tracked_changes_agent.change_data:
            messagebox.showwarning("No Data", "No tracked changes available to export.")
            return
        
        # Ask user whether to export all or filtered results
        search_text = self.search_var.get()
        if search_text:
            # User has active search filter
            result = messagebox.askyesnocancel(
                "Export Scope",
                f"You have an active search filter showing {len(self.tree.get_children())} of {len(self.tracked_changes_agent.change_data)} changes.\n\n"
                "Yes = Export filtered results only\n"
                "No = Export all tracked changes\n"
                "Cancel = Cancel export"
            )
            if result is None:  # Cancel
                return
            export_filtered = result
        else:
            export_filtered = False
        
        # Get the data to export
        if export_filtered:
            exact_match = self.exact_match_var.get()
            data_to_export = self.tracked_changes_agent.search_changes(search_text, exact_match)
            default_filename = "tracked_changes_filtered_report.md"
        else:
            data_to_export = self.tracked_changes_agent.change_data
            default_filename = "tracked_changes_report.md"
        
        # Ask for save location
        filepath = filedialog.asksaveasfilename(
            title="Export Tracked Changes Report",
            defaultextension=".md",
            filetypes=(("Markdown files", "*.md"), ("All files", "*.*")),
            initialfile=default_filename
        )
        
        if not filepath:
            return
        
        # Ask if user wants AI analysis
        ai_analysis = messagebox.askyesno(
            "AI Analysis",
            f"Generate AI-powered change summaries?\n\n"
            f"This will analyze {len(data_to_export)} changes using the currently selected AI model.\n\n"
            f"Note: This may take a few minutes and will use API credits.\n\n"
            f"Click 'No' to export without AI analysis."
        )
        
        # If AI analysis enabled, let user choose batch size
        batch_size = 25  # Default
        if ai_analysis:
            batch_dialog = tk.Toplevel(self.window)
            batch_dialog.title("Batch Size Configuration")
            batch_dialog.geometry("450x280")
            batch_dialog.transient(self.window)
            batch_dialog.grab_set()
            
            tk.Label(batch_dialog, text="Configure Batch Processing", 
                    font=("Segoe UI", 11, "bold")).pack(pady=10)
            tk.Label(batch_dialog, 
                    text=f"Choose how many segments to process per AI request\n"
                         f"Larger batches = faster but more tokens per request",
                    font=("Segoe UI", 9)).pack(pady=5)
            
            # Slider for batch size
            batch_var = tk.IntVar(value=25)
            
            slider_frame = tk.Frame(batch_dialog)
            slider_frame.pack(pady=10, fill='x', padx=20)
            
            tk.Label(slider_frame, text="Batch Size:", font=("Segoe UI", 9)).pack(side='left')
            batch_label = tk.Label(slider_frame, text="25", font=("Segoe UI", 10, "bold"), fg="blue")
            batch_label.pack(side='right')
            
            def update_label(val):
                batch_label.config(text=str(int(float(val))))
            
            slider = tk.Scale(batch_dialog, from_=1, to=100, orient='horizontal',
                            variable=batch_var, command=update_label, length=350)
            slider.pack(pady=5)
            
            # Info label
            info_label = tk.Label(batch_dialog, 
                                text=f"Total changes: {len(data_to_export)} | "
                                     f"Estimated batches at size 25: {(len(data_to_export) + 24) // 25}",
                                font=("Segoe UI", 8), fg="gray")
            info_label.pack(pady=5)
            
            def update_info(*args):
                size = batch_var.get()
                batches = (len(data_to_export) + size - 1) // size
                info_label.config(text=f"Total changes: {len(data_to_export)} | "
                                      f"Estimated batches at size {size}: {batches}")
            
            batch_var.trace('w', update_info)
            
            # OK button
            def on_ok():
                nonlocal batch_size
                batch_size = batch_var.get()
                batch_dialog.destroy()
            
            tk.Button(batch_dialog, text="OK", command=on_ok, 
                     font=("Segoe UI", 10), width=15).pack(pady=10)
            
            # Wait for dialog to close
            batch_dialog.wait_window()
        
        try:
            # Prepare report content
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Build AI prompt info for report header
            ai_prompt_info = ""
            if ai_analysis and hasattr(self, 'parent_app') and self.parent_app:
                provider = self.parent_app.current_llm_provider
                model = self.parent_app.current_llm_model
                # Capitalize provider name for display
                provider_display = provider.capitalize()
                ai_prompt_info = f"""

### AI Analysis Configuration

**Provider:** {provider_display}  
**Model:** {model}

**Prompt Template Used:**
```
You are a precision editor analyzing changes between two versions of text.
Compare the original and revised text and identify EXACTLY what changed.

CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
- PAY SPECIAL ATTENTION to quote marks: " vs " vs " (curly vs straight)
- Check for apostrophe changes: ' vs ' (curly vs straight)  
- Check for dash changes: - vs – vs — (hyphen vs en-dash vs em-dash)
- Quote the exact words/phrases that changed
- Use this format: "X" → "Y"
- For single word changes: quote both words
- For multiple changes: put each on its own line
- For punctuation/formatting: describe precisely
- For additions: "Added: [exact text]"
- For deletions: "Removed: [exact text]"
- DO NOT say "No change" unless texts are 100% identical
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text

Examples of single changes:
✓ "pre-cut" → "incision"
✓ Curly quotes → straight quotes: "word" → "word"
✓ Curly apostrophe → straight: don't → don't
✓ "package" → "packaging"

Examples of multiple changes (one per line):
✓ "split portions" → "divided portions"
  "connected by a" → "connected, via a"
  Curly quotes → straight quotes throughout
✓ Added: "carefully"
✓ "color" → "colour" (US to UK spelling)
✗ Clarified terminology (too vague)
✗ Fixed grammar (not specific)
✗ Improved word choice (not helpful)
```

---

"""
            
            md_content = f"""# Tracked Changes Analysis Report ([Supervertaler](https://github.com/michaelbeijer/Supervertaler) {self.APP_VERSION})

## What is this report?

This report analyzes the differences between AI-generated translations and your final edited versions exported from your CAT tool (memoQ, CafeTran, etc.). It shows exactly what you changed during post-editing, helping you review your editing decisions and track your translation workflow improvements.

**Use case:** After completing a translation project in your CAT tool with tracked changes enabled, export the bilingual document and load it here to see a detailed breakdown of all modifications made to the AI-generated baseline.

---

**Generated:** {timestamp}  
**Total Changes:** {len(data_to_export)}  
**Filter Applied:** {"Yes - " + search_text if export_filtered else "No"}  
**AI Analysis:** {"Enabled" if ai_analysis else "Disabled"}
{ai_prompt_info}
"""
            
            # Process changes with paragraph format
            if ai_analysis:
                # Show progress window
                self.log_queue.put(f"[Export] Generating AI summaries for {len(data_to_export)} changes in batches...")
                
                progress_window = tk.Toplevel(self.window)
                progress_window.title("Generating AI Analysis...")
                progress_window.geometry("400x150")
                progress_window.transient(self.window)
                progress_window.grab_set()
                
                tk.Label(progress_window, text="Analyzing tracked changes with AI (batched)...", 
                        font=("Segoe UI", 10)).pack(pady=10)
                progress_label = tk.Label(progress_window, text="Processing batch 0 of 0")
                progress_label.pack()
                batch_info_label = tk.Label(progress_window, text="", font=("Segoe UI", 8), fg="gray")
                batch_info_label.pack()
                
                # Process in batches (user-configured)
                # batch_size already set from dialog above
                total_batches = (len(data_to_export) + batch_size - 1) // batch_size
                all_summaries = {}
                
                for batch_num in range(total_batches):
                    start_idx = batch_num * batch_size
                    end_idx = min(start_idx + batch_size, len(data_to_export))
                    batch = data_to_export[start_idx:end_idx]
                    
                    progress_label.config(text=f"Processing batch {batch_num + 1} of {total_batches}")
                    batch_info_label.config(text=f"Segments {start_idx + 1}-{end_idx} of {len(data_to_export)}")
                    progress_window.update()
                    
                    # Generate AI summaries for this batch
                    try:
                        batch_summaries = self.get_ai_change_summaries_batch(batch, start_idx)
                        all_summaries.update(batch_summaries)
                        self.log_queue.put(f"[Export] Batch {batch_num + 1}/{total_batches} complete ({len(batch)} segments)")
                    except Exception as e:
                        self.log_queue.put(f"[Export] Error in batch {batch_num + 1}: {e}")
                        # Fill in error messages for failed batch
                        for i in range(start_idx, end_idx):
                            all_summaries[i] = f"_Error generating summary: {str(e)}_"
                
                progress_window.destroy()
                
                # Now build the markdown content with the summaries
                for i, (original, final) in enumerate(data_to_export):
                    summary = all_summaries.get(i, "_No summary available_")
                    
                    # Add segment in paragraph format
                    md_content += f"""### Segment {i + 1}

**Target (Original):**  
{original}

**Target (Revised):**  
{final}

**Change Summary:**  
{summary}

---

"""
            else:
                # No AI analysis - simpler paragraph format
                for i, (original, final) in enumerate(data_to_export, 1):
                    md_content += f"""### Segment {i}

**Target (Original):**  
{original}

**Target (Revised):**  
{final}

---

"""
            
            md_content += f"""

---

## Summary Statistics

- **Total Segments Analyzed:** {len(data_to_export)}
- **AI Analysis:** {"Enabled" if ai_analysis else "Disabled"}
- **Export Type:** {"Filtered" if export_filtered else "Complete"}

*This report was generated by [Supervertaler](https://github.com/michaelbeijer/Supervertaler) {self.APP_VERSION}*
"""
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            messagebox.showinfo(
                "Export Successful",
                f"Exported {len(data_to_export)} tracked changes to:\n{filepath}\n\n"
                + ("AI change summaries included." if ai_analysis else "Export completed without AI analysis.")
            )
            
            self.log_queue.put(f"[Export] Report saved to: {filepath}")
            
        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"Failed to export tracked changes report:\n{str(e)}"
            )
            self.log_queue.put(f"[Export] Error: {e}")
    
    def get_ai_change_summaries_batch(self, changes_batch, start_index):
        """Get AI summaries for a batch of changes - much faster than one-by-one"""
        if not hasattr(self, 'parent_app') or not self.parent_app:
            # Fallback for batch
            return {i: "Modified text" for i in range(start_index, start_index + len(changes_batch))}
        
        try:
            provider = self.parent_app.current_llm_provider
            model_name = self.parent_app.current_llm_model
            api_key = ""
            
            # Debug logging
            self.log_queue.put(f"[Export] Using provider: {provider}, model: {model_name}")
            
            if provider == "claude":
                api_key = self.parent_app.api_keys.get("claude", "")
            elif provider == "gemini":
                api_key = self.parent_app.api_keys.get("google", "")
            elif provider == "openai":
                api_key = self.parent_app.api_keys.get("openai", "")
            
            if not api_key:
                self.log_queue.put(f"[Export] ERROR: No API key found for provider: {provider}")
                return {i: "AI unavailable - no API key" for i in range(start_index, start_index + len(changes_batch))}
            
            self.log_queue.put(f"[Export] API key found, calling {provider}...")
            
            # Build batch prompt with all changes
            batch_prompt = """You are a precision editor analyzing changes between multiple text versions.
For each numbered pair below, identify EXACTLY what changed.

CRITICAL INSTRUCTIONS:
- Be extremely specific and precise
- PAY SPECIAL ATTENTION to quote marks: " vs " vs " (curly vs straight)
- Check for apostrophe changes: ' vs ' (curly vs straight)
- Check for dash changes: - vs – vs — (hyphen vs en-dash vs em-dash)
- Quote the exact words/phrases that changed
- Use format: "X" → "Y"
- For multiple changes in one segment: put each on its own line
- For punctuation/formatting: describe precisely (e.g., 'Curly quotes → straight quotes: "word" → "word"')
- DO NOT say "No change" unless texts are 100% identical (byte-for-byte)
- DO NOT use vague terms like "clarified", "improved", "fixed"
- DO quote the actual changed text

IMPORTANT: If only punctuation changed (quotes, apostrophes, dashes), you MUST report it!

"""
            
            # Add all changes to the prompt
            for i, (original, final) in enumerate(changes_batch):
                batch_prompt += f"""
[{i + 1}] ORIGINAL: {original}
    REVISED: {final}

"""
            
            batch_prompt += """
Now provide the change summary for each segment, formatted as:

[1] your precise summary here
[2] your precise summary here
[3] your precise summary here

(etc. for all segments)"""
            
            # Call AI based on provider
            self.log_queue.put(f"[Export] Checking provider condition: {provider} == gemini? {provider == 'gemini'}, GEMINI_AVAILABLE? {self.GEMINI_AVAILABLE}")
            if provider == "gemini" and self.GEMINI_AVAILABLE:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content(batch_prompt)
                response_text = response.text.strip()
                
            elif provider == "claude" and self.ANTHROPIC_AVAILABLE:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                
                message = client.messages.create(
                    model=model_name,
                    max_tokens=2000,  # Larger for batch
                    messages=[{
                        "role": "user",
                        "content": batch_prompt
                    }]
                )
                
                response_text = message.content[0].text.strip()
                
            elif provider == "openai" and self.OPENAI_AVAILABLE:
                import openai
                client = openai.OpenAI(api_key=api_key)
                
                response = client.chat.completions.create(
                    model=model_name,
                    max_tokens=2000,  # Larger for batch
                    messages=[{
                        "role": "user",
                        "content": batch_prompt
                    }]
                )
                
                response_text = response.choices[0].message.content.strip()
            else:
                self.log_queue.put(f"[Export] ERROR: No matching provider condition for {provider}")
                return {i: "Provider not available" for i in range(start_index, start_index + len(changes_batch))}
            
            # Parse the response to extract individual summaries
            summaries = {}
            current_num = None
            current_summary_lines = []
            
            for line in response_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                # Check if line starts with [N]
                match = re.match(r'^\[(\d+)\]\s*(.*)$', line)
                if match:
                    # Save previous summary if any
                    if current_num is not None:
                        summary_text = '\n'.join(current_summary_lines).strip()
                        summaries[start_index + current_num - 1] = summary_text
                    
                    # Start new summary
                    current_num = int(match.group(1))
                    summary_start = match.group(2).strip()
                    current_summary_lines = [summary_start] if summary_start else []
                elif current_num is not None:
                    # Continuation of current summary
                    current_summary_lines.append(line)
            
            # Save last summary
            if current_num is not None:
                summary_text = '\n'.join(current_summary_lines).strip()
                summaries[start_index + current_num - 1] = summary_text
            
            # Fill in any missing summaries
            for i in range(len(changes_batch)):
                if (start_index + i) not in summaries:
                    summaries[start_index + i] = "_Summary not parsed correctly_"
            
            return summaries
            
        except Exception as e:
            self.log_queue.put(f"[AI Batch] Error: {e}")
            return {i: f"Analysis failed: {str(e)}" for i in range(start_index, start_index + len(changes_batch))}


def format_tracked_changes_context(tracked_changes_list, max_length=1000):
    """Format tracked changes for AI context, keeping within token limits"""
    if not tracked_changes_list:
        return ""
    
    context_parts = ["TRACKED CHANGES REFERENCE (Original→Final editing patterns):"]
    current_length = len(context_parts[0])
    
    for i, (original, final) in enumerate(tracked_changes_list):
        change_text = f"• \"{original}\" → \"{final}\""
        if current_length + len(change_text) > max_length:
            if i > 0:  # Only add if we have at least one example
                context_parts.append("(Additional examples truncated to save space)")
            break
        context_parts.append(change_text)
        current_length += len(change_text)
    
    return "\n".join(context_parts) + "\n"
