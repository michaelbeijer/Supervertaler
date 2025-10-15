# --- Supervertaler (v2.4.4-CLASSIC) - Multi-LLM AI-powered Translator & Proofreader with Project Management ---
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import threading
import queue
import os
import re
import math
import xml.etree.ElementTree as ET 
import io 
import sys
import zipfile  # Added for DOCX parsing
# ADD: base64 for image encoding (Claude/OpenAI multimodal)
import base64
import json  # For custom prompt management
import time  # For timestamp in saved prompts
import webbrowser  # For clickable email link
import subprocess  # For opening folder in file manager

# ADD: central version constant (was missing, caused NameError)
APP_VERSION = "2.4.4-CLASSIC"
print(f"=== Supervertaler v{APP_VERSION} starting ===")

# --- Private Features Flag ---
# Check for .supervertaler.local file to enable private features (for developers only)
# Users won't have this file, so they won't see confusing private folder options
ENABLE_PRIVATE_FEATURES = os.path.exists(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".supervertaler.local")
)
if ENABLE_PRIVATE_FEATURES:
    print("[DEV MODE] Private features enabled (.supervertaler.local found)")
    print("[DEV MODE] All user data will be saved to *_private folders")

# --- Path Resolver for Dev Mode ---
def get_user_data_path(folder_name):
    """
    Returns the appropriate path based on dev mode using parallel folder structure.
    In dev mode: Returns 'user data_private/folder_name'
    In user mode: Returns 'user data/folder_name'
    
    This creates two complete parallel directory trees:
    - user data/          (public, synced to GitHub)
    - user data_private/  (private, gitignored)
    
    Example:
        Dev mode:  get_user_data_path('TMs') -> 'user data_private/TMs'
        User mode: get_user_data_path('TMs') -> 'user data/TMs'
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if ENABLE_PRIVATE_FEATURES:
        # Dev mode - use parallel private structure
        user_data_root = os.path.join(script_dir, "user data_private")
    else:
        # User mode - use public structure
        user_data_root = os.path.join(script_dir, "user data")
    
    full_path = os.path.join(user_data_root, folder_name)
    
    # Create directory if it doesn't exist
    os.makedirs(full_path, exist_ok=True)
    
    return full_path

# --- Changelog (v2.4.1) ---
# NEW EXPERIMENTAL FEATURE: memoQ bilingual DOCX import/export
# - Import memoQ bilingual DOCX files directly
# - Extract source segments from bilingual table
# - Export translations back to bilingual format
# - Preserve segment IDs, metadata, and CAT tool tags
# - v2.4.0 remains untouched as stable production version

# --- Changelog (v2.1.1) ---
# - Added/updated external CHANGELOG.md with details for this release.
# - NEW: Advanced System Prompts section - collapsible GUI section allowing users to:
#   â€¢ View and edit underlying system prompts for Translation and Proofreading modes
#   â€¢ Use template variables like {source_lang} and {target_lang}
#   â€¢ Preview final prompts with current language settings
#   â€¢ Reset prompts to defaults
#   â€¢ Organize prompts in tabbed interface
# - Includes prior fixes:
#   â€¢ OutputGenerationAgent for TXT/TMX output.
#   â€¢ Restored core agents/factories (TMAgent, BilingualFileIngestionAgent, Gemini/Claude agents).
#   â€¢ TMX parsing deprecation fix in TMAgent (explicit None checks).
#   â€¢ Gemini proofreader implementation + parsing of summaries.
#   â€¢ Corrected Claude proofreader logging labels.
#   â€¢ UI enable_buttons to restore controls after run.
#   â€¢ Improved multimodal image handling (Gemini: PIL.Image; Claude: base64).
# --- End Changelog ---

PIL_AVAILABLE = False
try:
    from PIL import Image 
    PIL_AVAILABLE = True
except ImportError:
    print("WARNING: Pillow (PIL) library not found. Drawings Image Folder feature will be disabled.")

# --- Library Import Checks ---
GOOGLE_AI_AVAILABLE = False
GOOGLE_AI_IMPORT_ERROR_MESSAGE = ""
GENAI_VERSION = "unknown"

print("--- Supervertaler Script: Attempting to import google.generativeai ---")
try:
    import google.generativeai as genai
    try:
        from google.generativeai.types import GenerationConfig 
    except ImportError:
        print("Note: Could not import GenerationConfig from google.generativeai.types (may not be needed for this script version).")
    
    GENAI_VERSION = getattr(genai, '__version__', 'unknown')
    print(f"SUCCESS: google.generativeai imported. Version: {GENAI_VERSION}")
    GOOGLE_AI_AVAILABLE = True
except ImportError as e:
    GOOGLE_AI_IMPORT_ERROR_MESSAGE = f"ImportError: {e}\nThe library 'google-generativeai' could not be found by this script."
    print(f"FAIL: {GOOGLE_AI_IMPORT_ERROR_MESSAGE}")
except Exception as e_other:
    GOOGLE_AI_IMPORT_ERROR_MESSAGE = f"An unexpected error occurred during import: {e_other}"
    print(f"FAIL: {GOOGLE_AI_IMPORT_ERROR_MESSAGE}")

CLAUDE_AVAILABLE = False
CLAUDE_IMPORT_ERROR_MESSAGE = ""
ANTHROPIC_VERSION = "unknown"

print("--- Supervertaler Script: Attempting to import anthropic ---")
try:
    import anthropic
    ANTHROPIC_VERSION = getattr(anthropic, '__version__', 'unknown')
    print(f"SUCCESS: anthropic imported. Version: {ANTHROPIC_VERSION}")
    CLAUDE_AVAILABLE = True
except ImportError as e:
    CLAUDE_IMPORT_ERROR_MESSAGE = f"ImportError: {e}\nThe library 'anthropic' could not be found by this script."
    print(f"FAIL: {CLAUDE_IMPORT_ERROR_MESSAGE}")
except Exception as e_other:
    CLAUDE_IMPORT_ERROR_MESSAGE = f"An unexpected error occurred during import: {e_other}"
    print(f"FAIL: {CLAUDE_IMPORT_ERROR_MESSAGE}")

OPENAI_AVAILABLE = False
OPENAI_IMPORT_ERROR_MESSAGE = ""
OPENAI_VERSION = "unknown"

print("--- Supervertaler Script: Attempting to import openai ---")
try:
    import openai
    OPENAI_VERSION = getattr(openai, '__version__', 'unknown')
    print(f"SUCCESS: openai imported. Version: {OPENAI_VERSION}")
    OPENAI_AVAILABLE = True
except ImportError as e:
    OPENAI_IMPORT_ERROR_MESSAGE = f"ImportError: {e}\nThe library 'openai' could not be found by this script."
    print(f"FAIL: {OPENAI_IMPORT_ERROR_MESSAGE}")
except Exception as e_other:
    OPENAI_IMPORT_ERROR_MESSAGE = f"An unexpected error occurred during import: {e_other}"
    print(f"FAIL: {OPENAI_IMPORT_ERROR_MESSAGE}")

# --- API Key Configuration ---
def load_api_keys():
    """Load API keys from api_keys.txt file in the same directory as the script"""
    # Use PyInstaller-compatible logic to find api_keys.txt
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    api_keys_file = os.path.join(script_dir, "api_keys.txt")
    
    api_keys = {
        "google": "",
        "claude": "",
        "openai": ""
    }
    
    if os.path.exists(api_keys_file):
        try:
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        if key in ["google", "google_api_key", "gemini"]:
                            api_keys["google"] = value
                        elif key in ["claude", "claude_api_key", "anthropic"]:
                            api_keys["claude"] = value
                        elif key in ["openai", "openai_api_key", "chatgpt"]:
                            api_keys["openai"] = value
        except Exception as e:
            print(f"Error reading api_keys.txt: {e}")
    else:
        # Create template file
        try:
            with open(api_keys_file, 'w', encoding='utf-8') as f:
                f.write("# API Keys Configuration\n")
                f.write("# Format: key_name = your_api_key_here\n")
                f.write("# Remove the # at the beginning of the line to uncomment\n\n")
                f.write("# Google API Key for Gemini models\n")
                f.write("#google = YOUR_GOOGLE_API_KEY_HERE\n\n")
                f.write("# Claude API Key for Anthropic models\n")
                f.write("#claude = YOUR_CLAUDE_API_KEY_HERE\n\n")
                f.write("# OpenAI API Key for ChatGPT models\n")
                f.write("#openai = YOUR_OPENAI_API_KEY_HERE\n")
            print(f"Created template api_keys.txt file at: {api_keys_file}")
        except Exception as e:
            print(f"Could not create api_keys.txt template: {e}")
    
    return api_keys

# Load API keys
API_KEYS = load_api_keys()

# --- Model Definitions ---
GEMINI_MODELS = [
    "gemini-2.5-pro-preview-05-06",
    "gemini-2.5-pro-preview-12-17",
    "gemini-2.5-flash-preview-05-06", 
    "gemini-2.5-flash-preview-12-17",
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-flash"
]

CLAUDE_MODELS = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022", 
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307"
]

OPENAI_MODELS = [
    "gpt-5",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-4-turbo-preview",
    "gpt-4",
    "gpt-3.5-turbo"
]

# --- DOCX Change Reference Parser (Integrated from your original code) ---
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def tag(name: str) -> str:
    return f"{{{W_NS}}}{name}"

def collect_text(node, mode: str):
    """
    Recursively collect visible text from a node.
    mode='original' -> exclude insertions (<w:ins>), include deletions (<w:del> and <w:delText>)
    mode='final'    -> include insertions, exclude deletions
    """
    parts = []
    t = node.tag

    if t == tag("ins"):
        if mode == "final":
            for child in node:
                parts.extend(collect_text(child, mode))
        return parts  # in 'original' we ignore insertions

    if t == tag("del"):
        if mode == "original":
            for child in node:
                parts.extend(collect_text(child, mode))
        return parts  # in 'final' we ignore deletions

    # Runs and their children
    if t == tag("r"):
        for child in node:
            if child.tag == tag("t"):
                parts.append(child.text or "")
            elif child.tag == tag("delText"):
                if mode == "original":
                    parts.append(child.text or "")
            elif child.tag == tag("tab"):
                parts.append("\t")
            elif child.tag == tag("br"):
                parts.append("\n")
            else:
                parts.extend(collect_text(child, mode))
        return parts

    # Plain text nodes (rare at this level)
    if t == tag("t"):
        parts.append(node.text or "")
        return parts
    if t == tag("delText"):
        if mode == "original":
            parts.append(node.text or "")
        return parts
    if t == tag("tab"):
        parts.append("\t")
        return parts
    if t == tag("br"):
        parts.append("\n")
        return parts

    # Generic recursion
    for child in node:
        parts.extend(collect_text(child, mode))
    return parts

def tidy_text(s: str) -> str:
    # Collapse trailing spaces before newlines and duplicate line breaks, then strip
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n+", "\n", s)
    return s.strip()

def parse_docx_pairs(docx_path):
    """
    Return a list of (original_text, final_text) for paragraphs that changed.
    """
    try:
        with zipfile.ZipFile(docx_path) as z:
            try:
                xml = z.read("word/document.xml").decode("utf-8")
            except KeyError:
                raise RuntimeError("This file does not contain word/document.xml; is it a valid .docx?")

        root = ET.fromstring(xml)
        ns = {"w": W_NS}

        rows = []
        for p in root.findall(".//w:p", ns):
            original = "".join(collect_text(p, "original"))
            final    = "".join(collect_text(p, "final"))
            o_clean = tidy_text(original)
            f_clean = tidy_text(final)
            if o_clean != f_clean:
                rows.append((o_clean, f_clean))
        return rows
    except Exception as e:
        raise RuntimeError(f"Error parsing DOCX file: {e}")

# --- Tracked Changes Agent ---
class TrackedChangesAgent:
    def __init__(self, log_queue):
        self.log_queue = log_queue
        self.change_data = []  # List of (original_text, final_text) tuples
        self.files_loaded = []  # Track which files have been loaded
    
    def load_docx_changes(self, docx_path):
        """Load tracked changes from a DOCX file"""
        if not docx_path:
            return False
            
        self.log_queue.put(f"[Tracked Changes] Loading changes from: {docx_path}")
        
        try:
            new_changes = parse_docx_pairs(docx_path)
            
            # Add to existing changes
            self.change_data.extend(new_changes)
            self.files_loaded.append(os.path.basename(docx_path))
            
            self.log_queue.put(f"[Tracked Changes] Loaded {len(new_changes)} change pairs from {os.path.basename(docx_path)}")
            self.log_queue.put(f"[Tracked Changes] Total change pairs available: {len(self.change_data)}")
            
            return True
        except Exception as e:
            self.log_queue.put(f"[Tracked Changes] Error loading {docx_path}: {e}")
            messagebox.showerror("Tracked Changes Error", f"Failed to load tracked changes from {os.path.basename(docx_path)}: {e}")
            return False
    
    def load_tsv_changes(self, tsv_path):
        """Load tracked changes from a TSV file (original_text<tab>final_text format)"""
        if not tsv_path:
            return False
            
        self.log_queue.put(f"[Tracked Changes] Loading changes from: {tsv_path}")
        
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
                        self.log_queue.put(f"[Tracked Changes] Skipping line {line_num} in {os.path.basename(tsv_path)}: insufficient columns")
            
            # Add to existing changes
            self.change_data.extend(new_changes)
            self.files_loaded.append(os.path.basename(tsv_path))
            
            self.log_queue.put(f"[Tracked Changes] Loaded {len(new_changes)} change pairs from {os.path.basename(tsv_path)}")
            self.log_queue.put(f"[Tracked Changes] Total change pairs available: {len(self.change_data)}")
            
            return True
        except Exception as e:
            self.log_queue.put(f"[Tracked Changes] Error loading {tsv_path}: {e}")
            messagebox.showerror("Tracked Changes Error", f"Failed to load tracked changes from {os.path.basename(tsv_path)}: {e}")
            return False
    
    def clear_changes(self):
        """Clear all loaded tracked changes"""
        self.change_data.clear()
        self.files_loaded.clear()
        self.log_queue.put("[Tracked Changes] All tracked changes cleared")
    
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
        """Find tracked changes relevant to the current source segments being processed"""
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
        
        # Second pass: partial matches (contains)
        if len(relevant_changes) < max_changes:
            for segment in source_segments:
                segment_words = set(word.lower() for word in segment.split() if len(word) > 3)  # Only significant words
                for original, final in self.change_data:
                    if (original, final) in relevant_changes:
                        continue
                    
                    original_words = set(word.lower() for word in original.split() if len(word) > 3)
                    # Check if there's significant word overlap
                    if segment_words and original_words and len(segment_words.intersection(original_words)) >= min(2, len(segment_words) // 2):
                        relevant_changes.append((original, final))
                        if len(relevant_changes) >= max_changes:
                            return relevant_changes
        
        return relevant_changes

# --- Tracked Changes Browser Window ---
class TrackedChangesBrowser:
    def __init__(self, parent, tracked_changes_agent):
        self.parent = parent
        self.tracked_changes_agent = tracked_changes_agent
        self.window = None
    
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
        self.context_menu.add_command(label="Copy Original", command=self.copy_original)
        self.context_menu.add_command(label="Copy Final", command=self.copy_final)
        self.context_menu.add_command(label="Copy Both", command=self.copy_both)
        
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right click
        
        # Export button frame
        export_frame = tk.Frame(self.window)
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(export_frame, text="ðŸ“„ Export to TSV", command=self.export_to_tsv,
                 bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                 relief="raised", padx=10, pady=5).pack(side=tk.LEFT)
        
        tk.Label(export_frame, text="Export all tracked changes to a TSV file (Originalâ‡¥Final format)",
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

