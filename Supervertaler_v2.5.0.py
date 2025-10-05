# --- Supervertaler (v2.5.0) - Professional CAT tool with multicontextual AI translation system ---
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

# CAT Editor Integration Imports (v2.5.0)
from modules.segment_manager import Segment, SegmentManager, LayoutMode
from modules.ai_pretranslation_agent import AIPreTranslationAgent
from modules.docx_handler import DOCXHandler
from modules.simple_segmenter import SimpleSegmenter
from modules.tag_manager import TagManager

# ADD: central version constant
APP_VERSION = "2.5.0"
print(f"=== Supervertaler v{APP_VERSION} - Professional CAT tool with multicontextual AI translation system ===")
print(f"=== Starting application... ===")

# --- Changelog (v2.1.1) ---
# - Added/updated external CHANGELOG.md with details for this release.
# - NEW: Advanced System Prompts section - collapsible GUI section allowing users to:
#   • View and edit underlying system prompts for Translation and Proofreading modes
#   • Use template variables like {source_lang} and {target_lang}
#   • Preview final prompts with current language settings
#   • Reset prompts to defaults
#   • Organize prompts in tabbed interface
# - Includes prior fixes:
#   • OutputGenerationAgent for TXT/TMX output.
#   • Restored core agents/factories (TMAgent, BilingualFileIngestionAgent, Gemini/Claude agents).
#   • TMX parsing deprecation fix in TMAgent (explicit None checks).
#   • Gemini proofreader implementation + parsing of summaries.
#   • Corrected Claude proofreader logging labels.
#   • UI enable_buttons to restore controls after run.
#   • Improved multimodal image handling (Gemini: PIL.Image; Claude: base64).
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

# --- Helper Functions ---
def get_simple_lang_code(lang_name_or_code_input):
    if not lang_name_or_code_input: return ""
    lang_lower = lang_name_or_code_input.strip().lower()
    lang_map = {
        "english": "en", "dutch": "nl", "german": "de", "french": "fr",
        "spanish": "es", "italian": "it", "japanese": "ja", "chinese": "zh",
        "russian": "ru", "portuguese": "pt",
    }
    if lang_lower in lang_map: return lang_map[lang_lower]
    base_code = lang_lower.split('-')[0].split('_')[0]
    if len(base_code) == 2: return base_code
    return lang_lower[:2]

def normalize_figure_ref(ref_text):
    if not ref_text: return None
    match = re.search(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", ref_text, re.IGNORECASE)
    if match:
        identifier = match.group(1); return re.sub(r"[\s\.\-]", "", identifier).lower()
    base_name = os.path.splitext(ref_text)[0]
    cleaned_base = re.sub(r"(?:figure|figuur|fig\.?)\s*", "", base_name, flags=re.IGNORECASE)
    normalized = re.sub(r"[\s\.\-]", "", cleaned_base).lower()
    if normalized: return normalized
    return None

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

def pil_image_to_base64_png(img):
    """Encode a PIL image to base64 PNG (ascii) for Claude/OpenAI data URLs."""
    try:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("ascii")
    except Exception:
        return None

# --- TMX Generator Class ---
class TMXGenerator:
    """Helper class for generating TMX files"""
    def __init__(self):
        pass
    
    def generate_tmx(self, source_segments, target_segments, source_lang, target_lang):
        """Generate TMX content from parallel segments"""
        from datetime import datetime
        
        # Basic TMX structure
        tmx = ET.Element('tmx')
        tmx.set('version', '1.4')
        
        header = ET.SubElement(tmx, 'header')
        header.set('creationdate', datetime.now().strftime('%Y%m%dT%H%M%SZ'))
        header.set('srclang', get_simple_lang_code(source_lang))
        header.set('adminlang', 'en')
        header.set('segtype', 'sentence')
        header.set('creationtool', 'Supervertaler')
        header.set('creationtoolversion', APP_VERSION)
        header.set('datatype', 'plaintext')
        
        body = ET.SubElement(tmx, 'body')
        
        # Add translation units
        for src, tgt in zip(source_segments, target_segments):
            if not src.strip() or not tgt or '[ERR' in str(tgt) or '[Missing' in str(tgt):
                continue
                
            tu = ET.SubElement(body, 'tu')
            
            # Source segment
            tuv_src = ET.SubElement(tu, 'tuv')
            tuv_src.set('xml:lang', get_simple_lang_code(source_lang))
            seg_src = ET.SubElement(tuv_src, 'seg')
            seg_src.text = src.strip()
            
            # Target segment
            tuv_tgt = ET.SubElement(tu, 'tuv')
            tuv_tgt.set('xml:lang', get_simple_lang_code(target_lang))
            seg_tgt = ET.SubElement(tuv_tgt, 'seg')
            seg_tgt.text = str(tgt).strip()
        
        return ET.ElementTree(tmx)

# === NEW: Output file writer ===
class OutputGenerationAgent:
    """Writes TXT output and, for Translate mode, TMX alongside it."""
    def process(self, source_list, target_list, output_path, log_queue, mode, comments_list_for_output=None, source_lang=None, target_lang=None):
        try:
            # Normalize lengths
            n = min(len(source_list), len(target_list))
            src = source_list[:n]
            tgt = [(t if t is not None else "") for t in target_list[:n]]

            # Write TXT
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                if mode == "Translate":
                    for s, t in zip(src, tgt):
                        f.write(f"{s}\t{t}\n")
                else:  # Proofread
                    comments = comments_list_for_output or []
                    # pad comments to length n
                    if len(comments) < n:
                        comments = comments + [None] * (n - len(comments))
                    for i in range(n):
                        comment = comments[i] if comments[i] is not None else ""
                        f.write(f"{src[i]}\t{tgt[i]}\t{comment}\n")
            log_queue.put(f"[Output] TXT written: {output_path}")

            # Write TMX in Translate mode
            if mode == "Translate":
                try:
                    tmx_path = os.path.splitext(output_path)[0] + ".tmx"
                    tree = TMXGenerator().generate_tmx(src, tgt, source_lang or "en", target_lang or "en")
                    # Pretty print (optional); ensure we write UTF-8
                    tree.write(tmx_path, encoding='utf-8', xml_declaration=True)
                    log_queue.put(f"[Output] TMX written: {tmx_path}")
                except Exception as te:
                    log_queue.put(f"[Output] WARN: TMX not written: {te}")

            return True
        except Exception as e:
            log_queue.put(f"[Output] ERROR writing files: {e}")
            return False

# === RESTORE: Agents, TM, factories (required by GUI) ===

class BilingualFileIngestionAgent:
    def process(self, file_path, log_queue, mode="Translate"):
        log_queue.put(f"[Ingestor] Processing: {file_path} for mode: {mode}")
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.rstrip('\n\r')
                    if not line.strip():
                        continue
                    if mode == "Translate":
                        # Only take first column if tabs present
                        if '\t' in line:
                            parts = line.split('\t')
                            if len(parts) > 1:
                                log_queue.put(f"[Ingestor] Note: Line {line_num} has {len(parts)} tab-separated fields; using only first as source.")
                            source_text = parts[0].strip()
                        else:
                            source_text = line.strip()
                        if source_text:
                            data.append(source_text)
                        else:
                            log_queue.put(f"[Ingestor] Warn: Empty source after trimming on line {line_num}.")
                    elif mode == "Proofread":
                        parts = line.split('\t', 2)
                        if len(parts) == 2:
                            data.append({"source": parts[0], "target": parts[1], "comment": None})
                        elif len(parts) == 3:
                            data.append({"source": parts[0], "target": parts[1], "comment": parts[2]})
                        else:
                            log_queue.put(f"[Ingestor] Warn (Proofread): Skip line {line_num} (needs 2 or 3 tab-sep cols): {line}")
        except Exception as e:
            log_queue.put(f"[Ingestor] Err reading {file_path}: {e}")
            return []
        log_queue.put(f"[Ingestor] Done. {len(data)} entries/lines loaded.")
        return data

class TMAgent:
    def __init__(self, log_queue):
        self.log_queue = log_queue
        self.tm_data = {}

    def _parse_tmx_lang_xml_code(self, lang_attr_val):
        if lang_attr_val:
            return lang_attr_val.split('-')[0].split('_')[0].lower()
        return ""

    def load_tm(self, tm_fp, src_lang_gui, tgt_lang_gui):
        self.tm_data = {}
        loaded_count = 0
        if not tm_fp:
            return
        _, ext = os.path.splitext(tm_fp)
        self.log_queue.put(f"[TM Load] Attempting: {tm_fp}")
        gui_src = get_simple_lang_code(src_lang_gui)
        gui_tgt = get_simple_lang_code(tgt_lang_gui)
        self.log_queue.put(f"[TM Load] GUI Langs for TM: Src='{gui_src}', Tgt='{gui_tgt}'")
        if not gui_src or not gui_tgt:
            self.log_queue.put("[TM Load] Err: GUI langs for TM not set.")
            messagebox.showerror("TM Error", "Set GUI Source/Target Langs for TM.")
            return
        try:
            if ext.lower() == ".tmx":
                tree = ET.parse(tm_fp)
                root = tree.getroot()
                xml_ns = "http://www.w3.org/XML/1998/namespace"
                for tu in root.findall('.//tu'):
                    src_tuv, tgt_tuv = None, None
                    for tuv_node in tu.findall('tuv'):
                        lang_attr = tuv_node.get(f'{{{xml_ns}}}lang')
                        if not lang_attr:
                            continue
                        tmx_simple_code = self._parse_tmx_lang_xml_code(lang_attr)
                        if tmx_simple_code == gui_src:
                            src_tuv = tuv_node
                        elif tmx_simple_code == gui_tgt:
                            tgt_tuv = tuv_node
                    # FIX: explicit None checks (avoid deprecation)
                    if src_tuv is not None and tgt_tuv is not None:
                        src_seg_node, tgt_seg_node = src_tuv.find('seg'), tgt_tuv.find('seg')
                        if src_seg_node is not None and tgt_seg_node is not None:
                            try:
                                src_txt = ET.tostring(src_seg_node, encoding='unicode', method='text').strip()
                                tgt_txt = ET.tostring(tgt_seg_node, encoding='unicode', method='text').strip()
                            except Exception:
                                src_txt = "".join(src_seg_node.itertext()).strip()
                                tgt_txt = "".join(tgt_seg_node.itertext()).strip()
                            if src_txt:
                                self.tm_data[src_txt] = tgt_txt or ""
                                loaded_count += 1
                self.log_queue.put(f"[TM Load] Loaded {loaded_count} from TMX.")
            elif ext.lower() == ".txt":
                with open(tm_fp, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split('\t', 1)
                        if len(parts) == 2:
                            self.tm_data[parts[0]] = parts[1]
                            loaded_count += 1
                self.log_queue.put(f"[TM Load] Loaded {loaded_count} from TXT.")
            else:
                self.log_queue.put(f"[TM Load] Err: Unsupported TM ext: {ext}")
                messagebox.showerror("TM Error", f"Unsupported TM type: {ext}.")
        except Exception as e:
            self.log_queue.put(f"[TM Load] Err: {e}")
            messagebox.showerror("TM Load Error", f"TM Load Error: {e}")

    def get_translation(self, src_seg):
        return self.tm_data.get(src_seg.strip())

# --- Base Agent Classes ---
class BaseTranslationAgent:
    def __init__(self, api_key, log_queue, model_name, provider):
        self.log_queue = log_queue
        self.model = None
        self.model_name = model_name
        self.provider = provider
        self.api_key = api_key

class BaseProofreadingAgent:
    def __init__(self, api_key, log_queue, model_name, provider):
        self.log_queue = log_queue
        self.model = None
        self.model_name = model_name
        self.provider = provider
        self.api_key = api_key

# --- Gemini Agents ---
class GeminiTranslationAgent(BaseTranslationAgent):
    def __init__(self, api_key, log_queue, model_name='gemini-2.5-pro-preview-05-06'):
        super().__init__(api_key, log_queue, model_name, "Gemini")
        self.model_name = model_name.split('/')[-1] if model_name.startswith("models/") else model_name
        if not GOOGLE_AI_AVAILABLE:
            self.log_queue.put("[Gemini Translator] ERROR: Google AI library not available.")
            return
        if not api_key:
            self.log_queue.put("[Gemini Translator] ERROR: API Key is missing.")
            return
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.log_queue.put(f"[Gemini Translator] Agent with model '{self.model_name}' initialized.")
        except Exception as e:
            self.log_queue.put(f"[Gemini Translator] ERROR init ('{self.model_name}'): {e}.")

    def translate_specific_lines_with_drawings_context(self,
                                                       lines_map_to_translate,
                                                       full_document_context_text_str,
                                                       source_lang, target_lang,
                                                       all_source_segments_original_list,
                                                       drawings_images_map,
                                                       user_custom_instructions="",
                                                       tracked_changes_data=None,
                                                       custom_system_prompt=None):
        if not self.model:
            self.log_queue.put(f"[Gemini Translator] Model ('{self.model_name}') not init.")
            return {n: f"[Err: Model not init]" for n in lines_map_to_translate.keys()}
        if not lines_map_to_translate:
            self.log_queue.put(f"[Gemini Translator] No lines for chunk.")
            return {}

        line_nums = sorted(list(lines_map_to_translate.keys()))
        self.log_queue.put(f"[Gemini Translator] Translating {len(line_nums)} lines: {line_nums[:3]}... w/ '{self.model_name}' (drawings + tracked changes if available)...")

        prompt_parts = []
        
        # Use custom system prompt if provided, otherwise use default
        if custom_system_prompt:
            try:
                system_prompt = custom_system_prompt.format(source_lang=source_lang, target_lang=target_lang)
                prompt_parts.append(system_prompt)
            except KeyError as e:
                self.log_queue.put(f"[Gemini Translator] Error in custom prompt template: {e}. Using default.")
                prompt_parts.append(f"You are an expert {source_lang} to {target_lang} translator specialized in patent documents.")
        else:
            prompt_parts.append(f"You are an expert {source_lang} to {target_lang} translator specialized in patent documents.")
        
        if user_custom_instructions:
            prompt_parts.append(f"\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}\n")

        if tracked_changes_data:
            current_src = [all_source_segments_original_list[n-1] for n in line_nums]
            rel = tracked_changes_data.find_relevant_changes(current_src)
            if rel:
                prompt_parts.append(format_tracked_changes_context(rel))
                self.log_queue.put(f"[Gemini Translator] Added {len(rel)} relevant tracked changes as context")

        # Add context and instructions if not using custom prompt (to avoid duplication)
        if not custom_system_prompt:
            prompt_parts.extend([
                "The full patent text for overall context is in 'FULL PATENT CONTEXT' below. Translate ONLY sentences from 'PATENT SENTENCES TO TRANSLATE' later. These are listed with their original line numbers from the full document.",
                "If a sentence refers to a Figure (e.g., 'Figure 1A', 'Figuur X'), relevant images may be provided just before that sentence. Use these images as crucial context for accurately translating references to parts, features, or relationships shown in those figures.",
                "Present your output ONLY as a numbered list of the translations for the requested sentences, using their original numbering. Maintain accuracy and appropriate patent terminology.\n"
            ])
        
        prompt_parts.extend([
            f"FULL PATENT CONTEXT:\n{full_document_context_text_str}\n",
            "PATENT SENTENCES TO TRANSLATE (translate only these, using preceding images if provided for a figure reference):\n"
        ])

        images_added = set()
        for ln in line_nums:
            src_text_scan = all_source_segments_original_list[ln - 1]
            numbered_src_line = lines_map_to_translate[ln]
            fig_refs = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", src_text_scan, re.IGNORECASE)
            img_added = False
            if PIL_AVAILABLE and fig_refs and drawings_images_map:
                for ref in fig_refs:
                    norm = normalize_figure_ref(f"fig {ref}")
                    if norm and norm in drawings_images_map and norm not in images_added:
                        prompt_parts.append(f"\n--- Context Image: Figure {ref} (Referenced in or near the following text) ---")
                        prompt_parts.append(drawings_images_map[norm])  # PIL.Image is supported by Gemini SDK
                        images_added.add(norm)
                        img_added = True
                        break
            prompt_parts.append(numbered_src_line)
            if img_added:
                prompt_parts.append("\n")

        prompt_parts.append("\nTRANSLATED SENTENCES (numbered list for 'PATENT SENTENCES TO TRANSLATE' only):")

        try:
            response = self.model.generate_content(prompt_parts)
            raw_text = getattr(response, "text", "") or ""
            if not raw_text:
                self.log_queue.put(f"[Gemini Translator] Warn: Empty response for lines {line_nums}. Response: {response}")
        except Exception as e:
            self.log_queue.put(f"[Gemini Translator] Error enhanced TL ('{self.model_name}'): {e}")
            return {n: f"[TL Err line {n} (enhanced): {e}]" for n in lines_map_to_translate.keys()}

        translations = {}
        for line in (raw_text or "").splitlines():
            m = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
            if m:
                num = int(m.group(1))
                txt = m.group(2).strip()
                if num in line_nums:
                    translations[num] = txt
        for num in line_nums:
            if num not in translations:
                self.log_queue.put(f"[Gemini Translator] Warn: Missing TL line {num}. Placeholder.")
                translations[num] = f"[TL Missing line {num}]"
        return translations

class GeminiProofreadingAgent(BaseProofreadingAgent):
    def __init__(self, api_key, log_queue, model_name='gemini-2.5-pro-preview-05-06'):
        super().__init__(api_key, log_queue, model_name, "Gemini")
        self.model_name = model_name.split('/')[-1] if model_name.startswith("models/") else model_name
        if not GOOGLE_AI_AVAILABLE:
            self.log_queue.put("[Gemini Proofreader] ERROR: Google AI library not available.")
            return
        if not api_key:
            self.log_queue.put("[Gemini Proofreader] ERROR: API Key is missing.")
            return
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.log_queue.put(f"[Gemini Proofreader] Agent initialized with model '{self.model_name}'.")
        except Exception as e:
            self.log_queue.put(f"[Gemini Proofreader] ERROR initializing ('{self.model_name}'): {e}.")

    def proofread_specific_lines_with_context(self, lines_to_proofread_map, full_source_doc_str,
                                             full_original_target_doc_str, source_lang, target_lang,
                                             all_source_segments_original_list, drawings_images_map,
                                             user_custom_instructions="", tracked_changes_data=None,
                                             custom_system_prompt=None):
        if not self.model:
            self.log_queue.put(f"[Gemini Proofreader] Model not initialized.")
            return {n: {"revised_target": lines_to_proofread_map[n]["target_original"],
                        "changes_summary": "[Proofread Err: Model not init]",
                        "original_target": lines_to_proofread_map[n]["target_original"]} for n in lines_to_proofread_map.keys()}
        if not lines_to_proofread_map:
            self.log_queue.put(f"[Gemini Proofreader] No lines for proofreading chunk.")
            return {}

        line_nums = sorted(lines_to_proofread_map.keys())
        self.log_queue.put(f"[Gemini Proofreader] Proofreading {len(line_nums)} lines: {line_nums[:3]}... w/ '{self.model_name}' (images + tracked changes)...")

        prompt_parts = []
        
        # Use custom system prompt if provided, otherwise use default
        if custom_system_prompt:
            try:
                system_prompt = custom_system_prompt.format(source_lang=source_lang, target_lang=target_lang)
                prompt_parts.append(system_prompt)
            except KeyError as e:
                self.log_queue.put(f"[Gemini Proofreader] Error in custom prompt template: {e}. Using default.")
                prompt_parts.append(f"You are an expert proofreader and editor for {source_lang} → {target_lang} translations, specializing in patent documents.")
        else:
            prompt_parts.append(f"You are an expert proofreader and editor for {source_lang} → {target_lang} translations, specializing in patent documents.")
        
        if user_custom_instructions:
            prompt_parts.append(f"\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}\n")

        if tracked_changes_data:
            current_src = [all_source_segments_original_list[n-1] for n in line_nums]
            rel = tracked_changes_data.find_relevant_changes(current_src)
            if rel:
                prompt_parts.append(format_tracked_changes_context(rel))
                self.log_queue.put(f"[Gemini Proofreader] Added {len(rel)} relevant tracked changes as context")

        # Add context and instructions if not using custom prompt (to avoid duplication)
        if not custom_system_prompt:
            prompt_parts.extend([
                "For each segment you get SOURCE SEGMENT and EXISTING TRANSLATION.",
                "Tasks: accuracy, terminology consistency, patent tone, grammar, fluency, completeness, figure-reference consistency.",
                f"OUTPUT FORMAT STRICTLY:\n1) Numbered list of revised {target_lang} translations (use same numbering; if no change, reproduce original).\n"
                "2) Then a section:\n---CHANGES SUMMARY START---\n"
                "Per modified line: '<line>. <brief description of changes>' OR if none changed: 'No changes made to any segment in this batch.'\n"
                "---CHANGES SUMMARY END---"
            ])
        
        prompt_parts.extend([
            f"\nFULL SOURCE DOCUMENT CONTEXT (reference only):\n{full_source_doc_str}\n",
            f"FULL ORIGINAL TARGET DOCUMENT CONTEXT (for consistency):\n{full_original_target_doc_str}\n",
            "SEGMENTS FOR PROOFREADING:\n"
        ])

        images_added = set()
        for ln in line_nums:
            src_text = lines_to_proofread_map[ln]["source"]
            orig_target = lines_to_proofread_map[ln]["target_original"]
            fig_refs = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", src_text, re.IGNORECASE)
            if PIL_AVAILABLE and fig_refs and drawings_images_map:
                for ref in fig_refs:
                    norm = normalize_figure_ref(f"fig {ref}")
                    if norm and norm in drawings_images_map and norm not in images_added:
                        prompt_parts.append(f"\n--- Context Image: Figure {ref} (for line {ln}) ---")
                        prompt_parts.append(drawings_images_map[norm])
                        images_added.add(norm)
                        break
            prompt_parts.append(f"{ln}. SOURCE SEGMENT: {src_text}")
            prompt_parts.append(f"{ln}. EXISTING TRANSLATION: {orig_target}\n")

        prompt_parts.append("\nREVISED TRANSLATIONS (numbered list only):")

        try:
            response = self.model.generate_content(prompt_parts)
            raw_text = getattr(response, "text", "") or ""
            if not raw_text:
                self.log_queue.put(f"[Gemini Proofreader] Warn: Empty response for lines {line_nums}. Response: {response}")
        except Exception as e:
            self.log_queue.put(f"[Gemini Proofreader] Error during call: {e}")
            return {n: {"revised_target": lines_to_proofread_map[n]["target_original"],
                        "changes_summary": f"[Proofread Err line {n}: {e}]",
                        "original_target": lines_to_proofread_map[n]["target_original"]} for n in line_nums}

        translations_block = raw_text
        summary_block = ""
        summary_start = "---CHANGES SUMMARY START---"
        summary_end = "---CHANGES SUMMARY END---"
        if summary_start in raw_text:
            parts = raw_text.split(summary_start, 1)
            translations_block = parts[0].strip()
            remainder = parts[1]
            summary_block = remainder.split(summary_end, 1)[0].strip() if summary_end in remainder else remainder.strip()

        results = {}
        for line in translations_block.splitlines():
            m = re.match(r"^\s*(\d+)\.\s*(.*)$", line.strip())
            if m:
                num = int(m.group(1))
                txt = m.group(2).strip()
                if num in line_nums:
                    results.setdefault(num, {})["revised_target"] = txt

        parsed_summaries = {}
        if summary_block and "No changes made to any segment in this batch." not in summary_block:
            for line in summary_block.splitlines():
                m = re.match(r"^\s*(\d+)\.\s*(.*)$", line.strip())
                if m:
                    parsed_summaries[m.group(1)] = m.group(2).strip()

        for num in line_nums:
            original_target = lines_to_proofread_map[num]["target_original"]
            entry = results.setdefault(num, {})
            if "revised_target" not in entry or not entry["revised_target"].strip():
                entry["revised_target"] = original_target
                self.log_queue.put(f"[Gemini Proofreader] Note: Using original translation for line {num} (missing or empty revised output).")
            entry["changes_summary"] = parsed_summaries.get(str(num))
            entry["original_target"] = original_target

        self.log_queue.put(f"[Gemini Proofreader] Proofreading parse complete. Segments: {len(results)}.")
        return results

# --- Claude Agents ---
class ClaudeTranslationAgent(BaseTranslationAgent):
    def __init__(self, api_key, log_queue, model_name='claude-3-5-sonnet-20241022'):
        super().__init__(api_key, log_queue, model_name, "Claude")
        if not CLAUDE_AVAILABLE:
            self.log_queue.put("[Claude Translator] ERROR: anthropic library not available.")
            return
        if not api_key:
            self.log_queue.put("[Claude Translator] ERROR: API Key is missing.")
            return
        try:
            self.client = anthropic.Anthropic(api_key=api_key) if hasattr(anthropic, "Anthropic") else anthropic.Client(api_key=api_key)
            self.model = self.model_name
            self.log_queue.put(f"[Claude Translator] Agent with model '{self.model_name}' initialized.")
        except Exception as e:
            self.log_queue.put(f"[Claude Translator] ERROR init ('{self.model_name}'): {e}.")

    def translate_specific_lines_with_drawings_context(self, lines_map_to_translate, full_document_context_text_str,
                                                       source_lang, target_lang, all_source_segments_original_list,
                                                       drawings_images_map, user_custom_instructions="",
                                                       tracked_changes_data=None, custom_system_prompt=None):
        if not self.model:
            return {n: f"[Err: Model not init]" for n in lines_map_to_translate.keys()}
        if not lines_map_to_translate:
            return {}
        line_nums = sorted(list(lines_map_to_translate.keys()))
        self.log_queue.put(f"[Claude Translator] Translating {len(line_nums)} lines: {line_nums[:3]}... w/ '{self.model_name}' (images + tracked changes)...")

        content_parts = []
        def add_text(t):
            if t:
                content_parts.append({"type": "text", "text": t})

        # Use custom system prompt if provided, otherwise use default
        if custom_system_prompt:
            try:
                system_prompt = custom_system_prompt.format(source_lang=source_lang, target_lang=target_lang)
                add_text(system_prompt)
            except KeyError as e:
                self.log_queue.put(f"[Claude Translator] Error in custom prompt template: {e}. Using default.")
                add_text(f"You are an expert {source_lang} to {target_lang} translator specialized in patent documents.")
        else:
            add_text(f"You are an expert {source_lang} to {target_lang} translator specialized in patent documents.")
        
        if user_custom_instructions:
            add_text(f"\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}\n")

        if tracked_changes_data:
            current_src = [all_source_segments_original_list[n-1] for n in line_nums]
            rel = tracked_changes_data.find_relevant_changes(current_src)
            if rel:
                add_text(format_tracked_changes_context(rel))
                self.log_queue.put(f"[Claude Translator] Added {len(rel)} relevant tracked changes as context")

        add_text("The full patent text for overall context is in 'FULL PATENT CONTEXT' below. Translate ONLY sentences from 'PATENT SENTENCES TO TRANSLATE' later. These are listed with their original line numbers from the full document.")
        add_text("If a sentence refers to a Figure (e.g., 'Figure 1A', 'Figuur X'), relevant images may be provided just before that sentence. Use these images as crucial context.")
        add_text("Present your output ONLY as a numbered list of the translations for the requested sentences, using their original numbering.\n")
        add_text(f"FULL PATENT CONTEXT:\n{full_document_context_text_str}\n")
        add_text("PATENT SENTENCES TO TRANSLATE (translate only these, using preceding images if provided for a figure reference):\n")

        images_added = set()
        for ln in line_nums:
            src_text_scan = all_source_segments_original_list[ln - 1]
            numbered_src_line = lines_map_to_translate[ln]
            fig_refs = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", src_text_scan, re.IGNORECASE)
            img_added = False
            if PIL_AVAILABLE and fig_refs and drawings_images_map:
                for ref in fig_refs:
                    norm = normalize_figure_ref(f"fig {ref}")
                    if norm and norm in drawings_images_map and norm not in images_added:
                        b64 = pil_image_to_base64_png(drawings_images_map[norm])
                        if b64:
                            add_text(f"\n--- Context Image: Figure {ref} (Referenced in or near the following text) ---")
                            content_parts.append({"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}})
                            images_added.add(norm)
                            img_added = True
                        break
            add_text(numbered_src_line)
            if img_added: add_text("\n")
        add_text("\nTRANSLATED SENTENCES (numbered list for 'PATENT SENTENCES TO TRANSLATE' only):")

        try:
            msg = {"role": "user", "content": content_parts}
            response = self.client.messages.create(model=self.model_name, max_tokens=2048, messages=[msg])
            raw_text = ""
            try:
                if hasattr(response, "content"):
                    raw_text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
            except Exception:
                raw_text = getattr(response, "text", "") or str(response)
        except Exception as e:
            self.log_queue.put(f"[Claude Translator] Error: {e}")
            return {n: f"[TL Err line {n} (Claude): {e}]" for n in lines_map_to_translate.keys()}

        translations = {}
        for line in (raw_text or "").splitlines():
            m = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
            if m:
                num = int(m.group(1)); txt = m.group(2).strip()
                if num in line_nums: translations[num] = txt
        for num in line_nums:
            if num not in translations:
                self.log_queue.put(f"[Claude Translator] Warn: Missing TL line {num}. Placeholder.")
                translations[num] = f"[TL Missing line {num}]"
        return translations

class ClaudeProofreadingAgent(BaseProofreadingAgent):
    def __init__(self, api_key, log_queue, model_name='claude-3-5-sonnet-20241022'):
        super().__init__(api_key, log_queue, model_name, "Claude")
        if not CLAUDE_AVAILABLE:
            self.log_queue.put("[Claude Proofreader] ERROR: anthropic library not available."); return
        if not api_key:
            self.log_queue.put("[Claude Proofreader] ERROR: API Key is missing."); return
        try:
            self.client = anthropic.Anthropic(api_key=api_key) if hasattr(anthropic, "Anthropic") else anthropic.Client(api_key=api_key)
            self.model = self.model_name
            self.log_queue.put(f"[Claude Proofreader] Agent with model '{self.model_name}' initialized.")
        except Exception as e:
            self.log_queue.put(f"[Claude Proofreader] ERROR init ('{self.model_name}'): {e}.")

    def proofread_specific_lines_with_context(self, lines_to_proofread_map, full_source_doc_str,
                                             full_original_target_doc_str, source_lang, target_lang,
                                             all_source_segments_original_list, drawings_images_map,
                                             user_custom_instructions="", tracked_changes_data=None,
                                             custom_system_prompt=None):
        if not self.model:
            return {n: {"revised_target": lines_to_proofread_map[n]["target_original"],
                        "changes_summary": "[Proofread Err: Model not init]",
                        "original_target": lines_to_proofread_map[n]["target_original"]} for n in lines_to_proofread_map.keys()}
        if not lines_to_proofread_map:
            self.log_queue.put(f"[Claude Proofreader] No lines for proofreading chunk.")
            return {}

        line_nums = sorted(lines_to_proofread_map.keys())
        self.log_queue.put(f"[Claude Proofreader] Proofreading {len(line_nums)} lines: {line_nums[:3]}... w/ '{self.model_name}' (images + tracked changes)...")

        content_parts = []
        def add_text(t):
            if t:
                content_parts.append({"type": "text", "text": t})

        # Use custom system prompt if provided, otherwise use default
        if custom_system_prompt:
            try:
                system_prompt = custom_system_prompt.format(source_lang=source_lang, target_lang=target_lang)
                add_text(system_prompt)
            except KeyError as e:
                self.log_queue.put(f"[Claude Proofreader] Error in custom prompt template: {e}. Using default.")
                add_text(f"You are an expert proofreader and editor for {source_lang} → {target_lang} translations, specializing in patent documents.")
        else:
            add_text(f"You are an expert proofreader and editor for {source_lang} → {target_lang} translations, specializing in patent documents.")
        
        if user_custom_instructions:
            add_text(f"\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}\n")
        if tracked_changes_data:
            current_src = [all_source_segments_original_list[n-1] for n in line_nums]
            rel = tracked_changes_data.find_relevant_changes(current_src)
            if rel:
                add_text(format_tracked_changes_context(rel))
                self.log_queue.put(f"[Claude Proofreader] Added {len(rel)} relevant tracked changes as context")

        add_text("SEGMENTS FOR PROOFREADING:\n")
        images_added = set()
        for ln in line_nums:
            src_text = lines_to_proofread_map[ln]["source"]
            orig_target = lines_to_proofread_map[ln]["target_original"]
            fig_refs = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", src_text, re.IGNORECASE)
            if PIL_AVAILABLE and fig_refs and drawings_images_map:
                for ref in fig_refs:
                    normalized = normalize_figure_ref(f"fig {ref}")
                    if normalized and normalized in drawings_images_map and normalized not in images_added:
                        b64 = pil_image_to_base64_png(drawings_images_map[normalized])
                        if b64:
                            add_text(f"\n--- Context Image: Figure {ref} (for line {ln}) ---")
                            content_parts.append({"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}})
                            images_added.add(normalized)
                        break
            add_text(f"{ln}. SOURCE SEGMENT: {src_text}")
            add_text(f"{ln}. EXISTING TRANSLATION: {orig_target}\n")
        add_text("\nREVISED TRANSLATIONS (numbered list only):")

        try:
            msg = {"role": "user", "content": content_parts}
            response = self.client.messages.create(model=self.model_name, max_tokens=2048, messages=[msg])
            raw_text = ""
            try:
                if hasattr(response, "content"):
                    raw_text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
            except Exception:
                raw_text = getattr(response, "text", "") or str(response)
        except Exception as e:
            self.log_queue.put(f"[Claude Proofreader] Error during call: {e}")
            return {n: {"revised_target": lines_to_proofread_map[n]["target_original"],
                        "changes_summary": f"[Proofread Err line {n}: {e}]",
                        "original_target": lines_to_proofread_map[n]["target_original"]} for n in line_nums}

        translations_block = raw_text
        summary_block = ""
        summary_start = "---CHANGES SUMMARY START---"
        summary_end = "---CHANGES SUMMARY END---"
        if summary_start in raw_text:
            parts = raw_text.split(summary_start, 1)
            translations_block = parts[0].strip()
            remainder = parts[1]
            summary_block = remainder.split(summary_end, 1)[0].strip() if summary_end in remainder else remainder.strip()

        results = {}
        for line in translations_block.splitlines():
            m = re.match(r"^\s*(\d+)\.\s*(.*)$", line.strip())
            if m:
                num = int(m.group(1))
                txt = m.group(2).strip()
                if num in line_nums:
                    results.setdefault(num, {})["revised_target"] = txt

        parsed_summaries = {}
        if summary_block and "No changes made to any segment in this batch." not in summary_block:
            for line in summary_block.splitlines():
                m = re.match(r"^\s*(\d+)\.\s*(.*)$", line.strip())
                if m:
                    parsed_summaries[m.group(1)] = m.group(2).strip()

        for num in line_nums:
            original_target = lines_to_proofread_map[num]["target_original"]
            entry = results.setdefault(num, {})
            if "revised_target" not in entry or not entry["revised_target"].strip():
                entry["revised_target"] = original_target
                self.log_queue.put(f"[Claude Proofreader] Note: Using original translation for line {num} (missing or empty revised output).")
            entry["changes_summary"] = parsed_summaries.get(str(num))
            entry["original_target"] = original_target

        self.log_queue.put(f"[Claude Proofreader] Proofreading parse complete. Segments: {len(results)}.")
        return results

# --- OpenAI Agents ---
class OpenAITranslationAgent(BaseTranslationAgent):
    def __init__(self, api_key, log_queue, model_name='gpt-4o'):
        super().__init__(api_key, log_queue, model_name, "OpenAI")
        if not OPENAI_AVAILABLE:
            self.log_queue.put("[OpenAI Translator] ERROR: openai library not available.")
            return
        if not api_key:
            self.log_queue.put("[OpenAI Translator] ERROR: API Key is missing.")
            return
        try:
            self.client = openai.OpenAI(api_key=api_key)
            self.model = self.model_name
            self.log_queue.put(f"[OpenAI Translator] Agent with model '{self.model_name}' initialized.")
        except Exception as e:
            self.log_queue.put(f"[OpenAI Translator] ERROR init ('{self.model_name}'): {e}.")

    def get_token_parameter(self, token_count):
        """Get the correct token parameter name and value based on the model."""
        # GPT-5 and newer models use max_completion_tokens
        if "gpt-5" in self.model_name.lower():
            return {"max_completion_tokens": token_count}
        else:
            return {"max_tokens": token_count}
    
    def get_temperature_parameter(self):
        """Get the correct temperature parameter based on the model."""
        # GPT-5 only supports default temperature (1.0)
        if "gpt-5" in self.model_name.lower():
            return {}  # Don't include temperature parameter for GPT-5
        else:
            return {"temperature": 0.1}

    def translate_specific_lines_with_drawings_context(self, lines_map_to_translate, full_document_context_text_str,
                                                       source_lang, target_lang, all_source_segments_original_list,
                                                       drawings_images_map, user_custom_instructions="",
                                                       tracked_changes_data=None, custom_system_prompt=None):
        if not self.model:
            return {n: f"[Err: Model not init]" for n in lines_map_to_translate.keys()}
        if not lines_map_to_translate:
            return {}
        line_nums = sorted(list(lines_map_to_translate.keys()))
        self.log_queue.put(f"[OpenAI Translator] Translating {len(line_nums)} lines: {line_nums[:3]}... w/ '{self.model_name}' (images + tracked changes)...")

        content_parts = []
        def add_text(t):
            if t:
                content_parts.append({"type": "text", "text": t})
        
        def add_image(img):
            if img:
                import io
                import base64
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                content_parts.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_base64}"
                    }
                })

        # Use custom system prompt if provided, otherwise use default
        if custom_system_prompt:
            try:
                system_prompt = custom_system_prompt.format(source_lang=source_lang, target_lang=target_lang)
            except:
                system_prompt = custom_system_prompt
        else:
            if "gpt-5" in self.model_name.lower():
                system_prompt = f"""You are an expert {source_lang} to {target_lang} translator. 

CRITICAL: The input sentences may have numbers like "1. CLAIMS" or "2. A vehicle control method".

IGNORE those numbers completely. They are just for internal processing.

Extract only the actual text content after the number and translate that.

Example:
Input: "1. CLAIMS" → Extract: "CLAIMS" → Translate: "CONCLUSIES"
Input: "2. A vehicle control method" → Extract: "A vehicle control method" → Translate: "Een voertuigbesturingsmethode"

Your output should be ONLY the translations, one per line, with NO numbering:
CONCLUSIES
Een voertuigbesturingsmethode
[more translations...]

Do NOT include any line numbers, bullets, or numbering in your response."""
            else:
                system_prompt = f"You are an expert {source_lang} to {target_lang} translator. Translate ONLY the sentences from 'PATENT SENTENCES TO TRANSLATE' later, maintaining their original line numbers.\n\nPresent your output ONLY as a numbered list of translations for the requested sentences."

        # Add context
        add_text(f"FULL DOCUMENT CONTEXT for reference:\n{full_document_context_text_str}\n\n")
        if user_custom_instructions:
            add_text(f"ADDITIONAL INSTRUCTIONS:\n{user_custom_instructions}\n\n")
        if tracked_changes_data and tracked_changes_data != "No tracked changes found.":
            add_text(f"TRACKED CHANGES:\n{tracked_changes_data}\n\n")

        # Add sentences to translate
        add_text("PATENT SENTENCES TO TRANSLATE:\n")
        numbered_src_line = ""
        for num in line_nums:
            img_added = False  # Initialize img_added for each iteration
            src_line = lines_map_to_translate[num]
            if num in drawings_images_map:
                ref_name = f"FIGURE {num}"
                for ref, img in drawings_images_map.items():
                    if ref.upper().replace(" ", "").replace(".", "") == ref_name.upper().replace(" ", "").replace(".", ""):
                        add_text(numbered_src_line)
                        add_image(img)
                        numbered_src_line = f"\n{num}. {src_line}\n"
                        img_added = True
                        break
            numbered_src_line += f"{num}. {src_line}\n"
            if img_added:
                add_text(numbered_src_line)
                numbered_src_line = ""
        add_text(numbered_src_line)
        add_text("TRANSLATED SENTENCES (numbered list for 'PATENT SENTENCES TO TRANSLATE' only):")

        try:
            # For GPT-5, try a simpler message format if we have complex content
            if "gpt-5" in self.model_name.lower() and isinstance(content_parts, list) and len(content_parts) > 1:
                # Convert complex content to simple text for GPT-5
                text_content = ""
                for part in content_parts:
                    if part.get('type') == 'text':
                        text_content += part.get('text', '') + "\n"
                    elif part.get('type') == 'image_url':
                        text_content += "[IMAGE CONTENT OMITTED FOR GPT-5 COMPATIBILITY]\n"
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_content}
                ]
                self.log_queue.put(f"[OpenAI Translator] DEBUG - Using simplified text-only format for GPT-5")
            else:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content_parts}
                ]
            
            # Debug logging for GPT-5 API call
            if "gpt-5" in self.model_name.lower():
                self.log_queue.put(f"[OpenAI Translator] DEBUG - System prompt length: {len(system_prompt)} chars")
                user_content = messages[1]["content"]
                if isinstance(user_content, str):
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - User content (string): {len(user_content)} chars")
                else:
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - User content parts count: {len(user_content) if isinstance(user_content, list) else 'not a list'}")
            
            # Get the correct token parameter based on the model and segment count
            # GPT-5 needs much more tokens due to reasoning tokens
            if "gpt-5" in self.model_name.lower():
                # For GPT-5, use a very high token limit to account for reasoning
                segment_count = len(lines_map_to_translate)
                # GPT-5 can use huge amounts of tokens for reasoning
                # Start with a very generous limit
                token_limit = max(32000, segment_count * 500)  # Much higher: 32K minimum, 500 per segment
                # Cap at reasonable maximum
                token_limit = min(token_limit, 50000)
                self.log_queue.put(f"[OpenAI Translator] DEBUG - GPT-5 token limit set to {token_limit} for {segment_count} segments")
            else:
                token_limit = 2048
            
            token_params = self.get_token_parameter(int(token_limit))
            temp_params = self.get_temperature_parameter()
            
            self.log_queue.put(f"[OpenAI Translator] DEBUG - Making API call with token_params: {token_params}, temp_params: {temp_params}")
            
            # For GPT-5, add reasoning_effort parameter to control thinking
            extra_params = {}
            if "gpt-5" in self.model_name.lower():
                extra_params["reasoning_effort"] = "low"  # Use less reasoning to save tokens for output
                self.log_queue.put(f"[OpenAI Translator] DEBUG - Adding reasoning_effort=low for GPT-5")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                **token_params,
                **temp_params,
                **extra_params
            )
            
            # Debug the response structure
            if "gpt-5" in self.model_name.lower():
                self.log_queue.put(f"[OpenAI Translator] DEBUG - Response object type: {type(response)}")
                self.log_queue.put(f"[OpenAI Translator] DEBUG - Response choices count: {len(response.choices) if response.choices else 0}")
                if response.choices:
                    choice = response.choices[0]
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - First choice message type: {type(choice.message) if choice.message else None}")
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - First choice content type: {type(choice.message.content) if choice.message else None}")
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - First choice finish_reason: {choice.finish_reason}")
                    
                    # Check if there are any usage stats or other response details
                    if hasattr(response, 'usage'):
                        self.log_queue.put(f"[OpenAI Translator] DEBUG - Usage: {response.usage}")
                    if hasattr(response, 'system_fingerprint'):
                        self.log_queue.put(f"[OpenAI Translator] DEBUG - System fingerprint: {response.system_fingerprint}")
                    
                    # Log the raw content value (might be None vs empty string)
                    raw_content = choice.message.content
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - Raw content repr: {repr(raw_content)}")
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - Raw content is None: {raw_content is None}")
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - Raw content is empty string: {raw_content == ''}")
            
            raw_text = response.choices[0].message.content if response.choices else ""
        except Exception as e:
            self.log_queue.put(f"[OpenAI Translator] Error: {e}")
            return {n: f"[TL Err line {n} (OpenAI): {e}]" for n in lines_map_to_translate.keys()}

        # Debug logging for GPT-5 response format issues
        if "gpt-5" in self.model_name.lower():
            self.log_queue.put(f"[OpenAI Translator] DEBUG - Raw response length: {len(raw_text or '')} chars")
            if raw_text:
                preview = raw_text[:200] + "..." if len(raw_text) > 200 else raw_text
                self.log_queue.put(f"[OpenAI Translator] DEBUG - Response preview: {repr(preview)}")
            else:
                # If GPT-5 returns empty, try a simple test request
                self.log_queue.put(f"[OpenAI Translator] DEBUG - Empty response detected, testing with simple request...")
                try:
                    test_messages = [
                        {"role": "system", "content": "You are a translator."},
                        {"role": "user", "content": "Translate to English: Hello world"}
                    ]
                    test_response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=test_messages,
                        **self.get_token_parameter(100),
                        **self.get_temperature_parameter()
                    )
                    test_content = test_response.choices[0].message.content if test_response.choices else ""
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - Test response: {repr(test_content)}")
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - Test finish_reason: {test_response.choices[0].finish_reason if test_response.choices else 'None'}")
                except Exception as test_e:
                    self.log_queue.put(f"[OpenAI Translator] DEBUG - Test request failed: {test_e}")

        translations = {}
        
        # Special parsing for GPT-5 which now outputs without line numbers
        if "gpt-5" in self.model_name.lower():
            lines = [line.strip() for line in (raw_text or "").splitlines() if line.strip()]
            for i, line in enumerate(lines):
                if i < len(line_nums):
                    # GPT-5 tends to add double numbering like "1. 1. CLAIMS"
                    # Strip any leading numbering patterns
                    cleaned_line = line
                    
                    # Remove patterns like "1. 1. Text" → "Text"
                    cleaned_line = re.sub(r'^\d+\.\s*\d+\.\s*', '', cleaned_line)
                    # Remove patterns like "1. Text" → "Text" 
                    cleaned_line = re.sub(r'^\d+\.\s*', '', cleaned_line)
                    # Remove patterns like "1) Text" → "Text"
                    cleaned_line = re.sub(r'^\d+\)\s*', '', cleaned_line)
                    
                    translations[line_nums[i]] = cleaned_line.strip()
            
            # Fill in any missing translations
            for num in line_nums:
                if num not in translations:
                    self.log_queue.put(f"[OpenAI Translator] Warn: Missing TL line {num}. Placeholder.")
                    translations[num] = f"[TL Missing line {num}]"
        else:
            # Original parsing logic for other models that include line numbers
            for line in (raw_text or "").splitlines():
                # More flexible regex patterns to handle different formatting
                line_stripped = line.strip()
                
                # Pattern 1: "1. Translation" (standard expected format)
                m = re.match(r"^\s*(\d+)\.\s*(.*)", line_stripped)
                if m:
                    num = int(m.group(1)); txt = m.group(2).strip()
                    if num in line_nums: translations[num] = txt
                    continue
                    
                # Pattern 2: "1) Translation" (alternative format)
                m = re.match(r"^\s*(\d+)\)\s*(.*)", line_stripped)
                if m:
                    num = int(m.group(1)); txt = m.group(2).strip()
                    if num in line_nums: translations[num] = txt
                    continue
                    
                # Pattern 3: "1: Translation" (colon format)
                m = re.match(r"^\s*(\d+):\s*(.*)", line_stripped)
                if m:
                    num = int(m.group(1)); txt = m.group(2).strip()
                    if num in line_nums: translations[num] = txt
                    continue
                    
            for num in line_nums:
                if num not in translations:
                    self.log_queue.put(f"[OpenAI Translator] Warn: Missing TL line {num}. Placeholder.")
                    translations[num] = f"[TL Missing line {num}]"
        return translations

class OpenAIProofreadingAgent(BaseProofreadingAgent):
    def __init__(self, api_key, log_queue, model_name='gpt-4o'):
        super().__init__(api_key, log_queue, model_name, "OpenAI")
        if not OPENAI_AVAILABLE:
            self.log_queue.put("[OpenAI Proofreader] ERROR: openai library not available.")
            return
        if not api_key:
            self.log_queue.put("[OpenAI Proofreader] ERROR: API Key is missing.")
            return
        try:
            self.client = openai.OpenAI(api_key=api_key)
            self.model = self.model_name
            self.log_queue.put(f"[OpenAI Proofreader] Agent with model '{self.model_name}' initialized.")
        except Exception as e:
            self.log_queue.put(f"[OpenAI Proofreader] ERROR init ('{self.model_name}'): {e}.")

    def get_token_parameter(self, token_count):
        """Get the correct token parameter name and value based on the model."""
        # GPT-5 and newer models use max_completion_tokens
        if "gpt-5" in self.model_name.lower():
            return {"max_completion_tokens": token_count}
        else:
            return {"max_tokens": token_count}
    
    def get_temperature_parameter(self):
        """Get the correct temperature parameter based on the model."""
        # GPT-5 only supports default temperature (1.0)
        if "gpt-5" in self.model_name.lower():
            return {}  # Don't include temperature parameter for GPT-5
        else:
            return {"temperature": 0.1}

    def extract_corrected_text_and_explanation(self, response_text, lines_data, line_num):
        """Extract both the corrected text and explanation from AI response."""
        if not response_text:
            return "", ""
            
        # Get the original target text for this line
        original_target = ""
        for item in lines_data:
            if item.get("line_num") == line_num:
                original_target = item.get("target", "")
                break
        
        # Common patterns indicating no changes needed
        no_change_patterns = [
            "no change needed",
            "no changes needed", 
            "unchanged",
            "text appears identical",
            "keep as is",
            "original is correct",
            "no revision required"
        ]
        
        response_lower = response_text.lower()
        if any(pattern in response_lower for pattern in no_change_patterns):
            return original_target, response_text
            
        # Pattern for explicit corrections like 'Corrected "old" to "new"'
        correction_patterns = [
            r'corrected\s+["\']([^"\']+)["\']\s+to\s+["\']([^"\']+)["\']',
            r'changed\s+["\']([^"\']+)["\']\s+to\s+["\']([^"\']+)["\']',
            r'replaced\s+["\']([^"\']+)["\']\s+with\s+["\']([^"\']+)["\']'
        ]
        
        for pattern in correction_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                old_text = match.group(1)
                new_text = match.group(2)
                # Replace the old text with new text in the original target
                if old_text.lower() in original_target.lower():
                    # Find the actual case in the original
                    original_lower = original_target.lower()
                    start_idx = original_lower.find(old_text.lower())
                    if start_idx != -1:
                        end_idx = start_idx + len(old_text)
                        corrected_text = original_target[:start_idx] + new_text + original_target[end_idx:]
                        return corrected_text, response_text
        
        # Special patterns for rephrasings and replacements
        rephrase_patterns = [
            r'rephrased to ["\']([^"\']+)["\']',
            r'standardized to ["\']([^"\']+)["\']',
            r'harmonized to ["\']([^"\']+)["\']',
            r'adjusted to ["\']([^"\']+)["\']'
        ]
        
        for pattern in rephrase_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                new_text = match.group(1)
                return new_text, response_text
        
        # Check if response looks like a partial replacement (just the new term)
        # This catches cases like "model voor multimodale informatieverwerking" or "omvatten"
        if (len(response_text.split()) <= 10 and  # Short response
            not any(word in response_lower for word in ["for", "to", "with", "standardized", "replaced", "rephrased", "adjusted"]) and
            response_text != original_target and
            not response_text.lower().startswith(("note:", "explanation:", "comment:"))):
            
            # This might be just the corrected term/phrase
            # Try to find where it should go in the original
            if response_text.lower() in original_target.lower():
                # It's already in the original, return original
                return original_target, response_text
            else:
                # Check if this could be a replacement for a specific part
                # For now, if it's very short and doesn't contain explanation words, treat as corrected text
                if len(response_text.split()) <= 3:
                    # Very short - likely just a term replacement, but we need context
                    # For safety, return original with explanation
                    return original_target, response_text
                else:
                    # Longer response that might be the corrected text
                    return response_text, response_text
        
        # If the response looks like an explanation rather than corrected text
        explanation_indicators = [
            "standardized", "harmonized", "adjusted", "improved", "refined", "enhanced", 
            "for clarity", "for consistency", "to match", "to reflect", "maintains meaning",
            "added", "removed", "replaced", "modified", "rephrased"
        ]
        
        if any(indicator in response_lower for indicator in explanation_indicators):
            # This looks like an explanation, try to extract quoted corrections
            quoted_text = re.findall(r'"([^"]+)"', response_text)
            if len(quoted_text) >= 2:
                # Look for "from" to "to" pattern in quotes
                for i in range(len(quoted_text) - 1):
                    old_candidate = quoted_text[i]
                    new_candidate = quoted_text[i + 1]
                    if old_candidate.lower() in original_target.lower():
                        # Apply the correction
                        original_lower = original_target.lower()
                        old_lower = old_candidate.lower()
                        start_idx = original_lower.find(old_lower)
                        if start_idx != -1:
                            end_idx = start_idx + len(old_candidate)
                            corrected_text = original_target[:start_idx] + new_candidate + original_target[end_idx:]
                            return corrected_text, response_text
                            
                # If no clear correction found, check if last quote is different from original
                if quoted_text[-1] != original_target and quoted_text[-1].lower() != original_target.lower():
                    # Check if it's a substantial piece of text (not just a word)
                    if len(quoted_text[-1].split()) > 3:
                        return quoted_text[-1], response_text
            elif len(quoted_text) == 1:
                # Single quote might be the correction if it's substantial and different
                if (quoted_text[0] != original_target and 
                    quoted_text[0].lower() != original_target.lower() and
                    len(quoted_text[0].split()) > 3):
                    return quoted_text[0], response_text
            
            # If we can't extract a clear correction, return original with explanation
            return original_target, response_text
        
        # If response seems to be the corrected text itself (longer, substantive text)
        if (len(response_text.split()) > 5 and 
            not response_text.lower().startswith(("note:", "explanation:", "comment:"))):
            return response_text, response_text
            
        # Default: return original with explanation
        return original_target, response_text

    def proofread_specific_lines_with_context(self, lines_data, full_document_context_text_str,
                                            source_lang, target_lang, user_custom_instructions="",
                                            tracked_changes_data=None, custom_system_prompt=None):
        if not self.model:
            return [{"line_num": item.get("line_num", 0), "original_target": item.get("target", ""), 
                    "revised_target": f"[Err: Model not init]", "changes_summary": ""} for item in lines_data]
        if not lines_data:
            return []

        line_nums = [item.get("line_num") for item in lines_data]
        self.log_queue.put(f"[OpenAI Proofreader] Proofreading {len(line_nums)} lines: {line_nums[:3]}... w/ '{self.model_name}'...")

        # Use custom system prompt if provided, otherwise use default
        if custom_system_prompt:
            try:
                system_prompt = custom_system_prompt.format(source_lang=source_lang, target_lang=target_lang)
            except:
                system_prompt = custom_system_prompt
        else:
            # Enhanced system prompt for GPT-5 clarity
            system_prompt = f"""You are an expert {source_lang}-{target_lang} translation proofreader. 

Review and improve the translations provided, maintaining accuracy and fluency.

OUTPUT FORMAT: Provide only a numbered list of revised translations. Use this exact format:
1. [revised translation for line 1]
2. [revised translation for line 2]
3. [revised translation for line 3]

If a translation needs no changes, output the original translation for that line number.
Do not include explanations or comments - only the numbered translations."""

        # Build content
        content = f"FULL DOCUMENT CONTEXT for reference:\n{full_document_context_text_str}\n\n"
        if user_custom_instructions:
            content += f"ADDITIONAL INSTRUCTIONS:\n{user_custom_instructions}\n\n"
        if tracked_changes_data and tracked_changes_data != "No tracked changes found.":
            content += f"TRACKED CHANGES:\n{tracked_changes_data}\n\n"
        
        content += "TRANSLATIONS TO REVIEW:\n"
        for item in lines_data:
            line_num = item.get("line_num")
            source = item.get("source", "")
            target = item.get("target", "")
            content += f"{line_num}. SOURCE: {source}\n   TARGET: {target}\n\n"
        
        content += "REVISED TRANSLATIONS (numbered list only, no explanations):"

        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ]
            
            # Get the correct token parameter based on the model
            # For GPT-5, use dynamic token allocation like the translation agent
            if "gpt-5" in self.model_name.lower():
                # Calculate dynamic token limit based on number of lines (like translation agent)
                segment_count = len(lines_data)
                token_limit = max(32000, segment_count * 500)  # 32K minimum, 500 per segment
                # Cap at 50K to prevent excessive costs
                token_limit = min(token_limit, 50000)
                self.log_queue.put(f"[OpenAI Proofreader] DEBUG - GPT-5 dynamic token limit: {token_limit} for {segment_count} segments")
                token_params = self.get_token_parameter(token_limit)
            else:
                token_params = self.get_token_parameter(3000)
            
            temp_params = self.get_temperature_parameter()
            
            # For GPT-5, add reasoning_effort parameter to control thinking
            extra_params = {}
            if "gpt-5" in self.model_name.lower():
                extra_params["reasoning_effort"] = "low"  # Use less reasoning to save tokens for output
                self.log_queue.put(f"[OpenAI Proofreader] DEBUG - Adding reasoning_effort=low for GPT-5")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                **token_params,
                **temp_params,
                **extra_params
            )
            raw_text = response.choices[0].message.content if response.choices else ""
            
            # Debug: Log what GPT-5 actually returns
            self.log_queue.put(f"[OpenAI Proofreader DEBUG] Raw GPT-5 response (first 200 chars): {raw_text[:200]}...")
            
            # Enhanced GPT-5 debugging like the translation agent
            if "gpt-5" in self.model_name.lower():
                self.log_queue.put(f"[OpenAI Proofreader] DEBUG - Response object type: {type(response)}")
                self.log_queue.put(f"[OpenAI Proofreader] DEBUG - First choice finish_reason: {response.choices[0].finish_reason if response.choices else 'no choices'}")
                if hasattr(response, 'usage') and response.usage:
                    completion_tokens = getattr(response.usage, 'completion_tokens', 'unknown')
                    reasoning_tokens = getattr(response.usage, 'reasoning_tokens', 'unknown')
                    self.log_queue.put(f"[OpenAI Proofreader] DEBUG - Usage: completion_tokens={completion_tokens}, reasoning_tokens={reasoning_tokens}")
                else:
                    self.log_queue.put(f"[OpenAI Proofreader] DEBUG - No usage information available")
                self.log_queue.put(f"[OpenAI Proofreader] DEBUG - Raw response length: {len(raw_text)} chars")
                if not raw_text.strip():
                    self.log_queue.put(f"[OpenAI Proofreader] WARNING - GPT-5 returned empty response!")
            
        except Exception as e:
            self.log_queue.put(f"[OpenAI Proofreader] Error: {e}")
            return [{"line_num": item.get("line_num", 0), "original_target": item.get("target", ""), 
                    "revised_target": f"[PR Err line {item.get('line_num', 0)} (OpenAI): {e}]", 
                    "changes_summary": ""} for item in lines_data]

        # Parse responses - handle both "1." and "1)" formats that GPT-5 might use
        parsed_translations = {}
        parsed_explanations = {}
        for line in (raw_text or "").splitlines():
            # Updated regex to match both "1." and "1)" formats
            m = re.match(r"^\s*(\d+)[\.\)]\s*(.*)", line.strip())
            if m:
                num = int(m.group(1)); txt = m.group(2).strip()
                if num in line_nums: 
                    # Process the response to extract actual corrected text and explanation
                    corrected_text, explanation = self.extract_corrected_text_and_explanation(txt, lines_data, num)
                    parsed_translations[num] = corrected_text
                    parsed_explanations[num] = explanation

        results = []
        for item in lines_data:
            line_num = item.get("line_num")
            original_target = item.get("target", "")
            entry = {
                "line_num": line_num,
                "source": item.get("source", ""),
                "original_target": original_target,
                "comment": item.get("comment", "")
            }
            if line_num in parsed_translations:
                corrected_text = parsed_translations[line_num]
                explanation = parsed_explanations.get(line_num, "")
                
                entry["revised_target"] = corrected_text
                
                # Create enhanced comment with explanation
                base_comment = "Revised by OpenAI" if corrected_text != original_target else "No changes needed"
                if explanation and explanation != corrected_text:
                    # Add the explanation to the comment
                    entry["changes_summary"] = f"{base_comment}: {explanation}"
                else:
                    entry["changes_summary"] = base_comment
            else:
                entry["revised_target"] = original_target
                entry["changes_summary"] = "No changes needed"
                self.log_queue.put(f"[OpenAI Proofreader] Note: Using original translation for line {line_num} (missing or empty revised output).")
            results.append(entry)

        self.log_queue.put(f"[OpenAI Proofreader] Proofreading parse complete. Segments: {len(results)}.")
        return results

# --- Agent Factory Functions ---
def create_translation_agent(provider, api_key, log_queue, model_name):
    if provider.lower() == "gemini":
        return GeminiTranslationAgent(api_key, log_queue, model_name)
    elif provider.lower() == "claude":
        return ClaudeTranslationAgent(api_key, log_queue, model_name)
    elif provider.lower() == "openai":
        return OpenAITranslationAgent(api_key, log_queue, model_name)
    else:
        log_queue.put(f"[Factory] Unknown provider: {provider}")
        return None

def create_proofreading_agent(provider, api_key, log_queue, model_name):
    if provider.lower() == "gemini":
        return GeminiProofreadingAgent(api_key, log_queue, model_name)
    elif provider.lower() == "claude":
        return ClaudeProofreadingAgent(api_key, log_queue, model_name)
    elif provider.lower() == "openai":
        return OpenAIProofreadingAgent(api_key, log_queue, model_name)
    else:
        log_queue.put(f"[Factory] Unknown provider: {provider}")
        return None

def get_available_models(provider, api_key, log_queue):
    if provider.lower() == "gemini":
        if not GOOGLE_AI_AVAILABLE or not api_key:
            return GEMINI_MODELS
        try:
            genai.configure(api_key=api_key)
            dynamic_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name.split('/')[-1] if '/' in m.name else m.name
                    dynamic_models.append(model_name)
            return dynamic_models if dynamic_models else GEMINI_MODELS
        except Exception as e:
            log_queue.put(f"[Models] Error fetching Gemini models: {e}")
            return GEMINI_MODELS
    elif provider.lower() == "claude":
        return CLAUDE_MODELS
    elif provider.lower() == "openai":
        return OPENAI_MODELS
    else:
        return []

# --- Supervertaler GUI Application Class ---
class TranslationApp:
    def __init__(self, root):
        self.root = root
        root.title(f"Supervertaler v{APP_VERSION} - Dashboard (by Michael Beijer)") 
        root.geometry("1100x950")  # Wider to accommodate right-side log

        self.log_queue = queue.Queue()
        self.api_keys = API_KEYS
        self.tm_agent = TMAgent(self.log_queue)
        self.tracked_changes_agent = TrackedChangesAgent(self.log_queue)  # UPDATED: Use TrackedChangesAgent
        self.drawings_images_map = {} 
        self.tracked_changes_browser = None  # Reference to the tracked changes browser window

        # CAT Editor Integration (v2.5.0)
        self.cat_mode_active = False  # Track if CAT editor mode is active
        self.segment_manager = None  # Will hold SegmentManager instance
        self.current_docx_path = None  # Path to currently loaded DOCX
        self.docx_handler = None  # DOCXHandler instance
        self.ai_pretranslation_agent = AIPreTranslationAgent(self.log_queue)
        self.cat_editor_frame = None  # Will hold the CAT editor UI frame
        self.cat_segments_tree = None  # Treeview widget for segments

        # Create the log widget instance early to make it available for logging during init
        self.log_text = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD, state="disabled")

        # --- COMPACT INFO TEXT FOR v2.5.0 ---
        self.info_text_content_unified = (
            "🎯 Supervertaler v2.5.0\n"
            "Professional CAT tool with multicontextual AI translation\n"
            "By Michael Beijer\n\n"
            "🧠 MULTICONTEXTUAL INTELLIGENCE:\n"
            "Unlike basic MT, Supervertaler provides:\n"
            "• Full document context for every segment\n"
            "• Tracked changes learning from DOCX revisions\n"
            "• Translation memory (TMX/TXT) integration\n"
            "• Multimodal support (AI sees referenced images)\n"
            "• Custom instructions & advanced prompt libraries\n\n"
            "� SIMPLE WORKFLOW:\n\n"
            "1️⃣ INPUT: Choose TXT or DOCX\n"
            "   • TXT: From memoQ/Trados\n"
            "   • DOCX: Direct import\n\n"
            "2️⃣ VIEW: Choose editing mode\n"
            "   • Grid: Table editing (memoQ-style)\n"
            "   • Split: List + editor panel\n"
            "   • Document: Flow with clickable segments\n\n"
            "3️⃣ AI: Optional assistance\n"
            "   • Pre-Translation: AI fills all\n"
            "   • Proofreading: AI reviews\n"
            "   • Manual: No AI (traditional CAT)\n\n"
            "🔧 FEATURES:\n"
            "• Multi-Provider AI (Claude, Gemini, OpenAI)\n"
            "• Three professional view modes\n"
            "• Intelligent chunking\n"
            "• Project management\n\n"
            "📚 Full docs: User Guide & Quick Start"
        )
        
        # Check if any libraries are available
        libraries_available = GOOGLE_AI_AVAILABLE or CLAUDE_AVAILABLE or OPENAI_AVAILABLE
        if not libraries_available: 
            error_msg = "Critical Error: No AI libraries available!\n"
            if not GOOGLE_AI_AVAILABLE: error_msg += f"Google AI: {GOOGLE_AI_IMPORT_ERROR_MESSAGE}\n"
            if not CLAUDE_AVAILABLE: error_msg += f"Claude: {CLAUDE_IMPORT_ERROR_MESSAGE}\n"
            if not OPENAI_AVAILABLE: error_msg += f"OpenAI: {OPENAI_IMPORT_ERROR_MESSAGE}\n"
            messagebox.showerror("Critical Error", error_msg + "App will close.")
            root.destroy()
            return

        # Check API keys
        if not self.api_keys["google"] and not self.api_keys["claude"] and not self.api_keys["openai"]:
            messagebox.showwarning("API Keys Missing", "No API keys found in api_keys.txt. Please configure at least one API key.")
            self.update_log("CRITICAL: No API keys configured. Check api_keys.txt file.")

        # Create main horizontal paned window (left: functions, right: info+log)
        main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=8, sashrelief=tk.RAISED)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel with scrollable canvas for all controls
        left_container = tk.Frame(main_paned, bg="white", relief=tk.SUNKEN, bd=2)
        main_paned.add(left_container, minsize=500, width=600)
        
        # Create canvas and scrollbar for left panel
        left_canvas = tk.Canvas(left_container, bg="white", highlightthickness=0)
        left_scrollbar = tk.Scrollbar(left_container, orient="vertical", command=left_canvas.yview)
        left_frame = tk.Frame(left_canvas, bg="white")
        
        # Configure scrolling
        left_frame.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )
        
        left_canvas.create_window((0, 0), window=left_frame, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        # Pack canvas and scrollbar
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel scrolling
        def _on_mousewheel(event):
            left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        left_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Right paned window for info (top) and log (bottom)
        right_paned = tk.PanedWindow(main_paned, orient=tk.VERTICAL, sashwidth=8, sashrelief=tk.RAISED)
        main_paned.add(right_paned, minsize=400, width=500)
        
        # Info frame (top right) - white background for consistency
        info_frame = tk.Frame(right_paned, bg="white", relief=tk.SUNKEN, bd=2)
        right_paned.add(info_frame, minsize=350, height=800)
        
        # Log frame (bottom right) - white background for consistency
        log_frame = tk.Frame(right_paned, bg="white", relief=tk.SUNKEN, bd=2)
        right_paned.add(log_frame, minsize=150, height=200)

        current_row = 0
        
        # Add program title at top of functions panel - extra sharp font
        title_label = tk.Label(left_frame, text=f"Supervertaler v{APP_VERSION} - Dashboard", 
                              font=("Segoe UI", 16, "bold"), fg="#1a365d", bg="white")
        title_label.grid(row=current_row, column=0, columnspan=3, padx=5, pady=(10,2), sticky="ew")
        current_row += 1
        
        subtitle_label = tk.Label(left_frame, text="Professional CAT tool with multicontextual AI translation system",
                                 font=("Segoe UI", 8), fg="gray", bg="white")
        subtitle_label.grid(row=current_row, column=0, columnspan=3, padx=5, pady=(0,10), sticky="ew")
        current_row += 1
        
        # Move info to top right - extra sharp heading font
        tk.Label(info_frame, text="ℹ️ Quick Reference", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=(5,2))
        self.info_label = tk.Label(info_frame, text=self.info_text_content_unified, wraplength=400, justify=tk.LEFT, 
                                  anchor="nw", relief=tk.SOLID, borderwidth=1, padx=8, pady=8, bg="white", 
                                  font=("Segoe UI", 8))
        self.info_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,5))
        
        # Add website link at bottom of info panel
        def open_website():
            webbrowser.open("https://michaelbeijer.co.uk/")
        
        # Create frame for the info text and clickable link
        link_frame = tk.Frame(info_frame, bg="white")
        link_frame.pack(anchor="w", padx=5, pady=(0,5))
        
        # Non-clickable "Info @" text
        tk.Label(link_frame, text="Info @ ", font=("Segoe UI", 8), fg="black", bg="white").pack(side=tk.LEFT)
        
        # Clickable website URL
        website_label = tk.Label(link_frame, text="https://michaelbeijer.co.uk/", 
                                font=("Segoe UI", 8, "underline"), fg="#0066cc", bg="white", cursor="hand2")
        website_label.pack(side=tk.LEFT)
        website_label.bind("<Button-1>", lambda e: open_website())
        
        # === AI MODE SELECTION (For AI-Assisted Workflows) ===
        mode_section = tk.LabelFrame(left_frame, text="🤖 AI-Assisted Workflows (Optional)", 
                                     font=("Segoe UI", 11, "bold"), padx=10, pady=10, bg="white", 
                                     relief="groove", borderwidth=2)
        mode_section.grid(row=current_row, column=0, columnspan=3, pady=(5,10), sticky="ew", padx=5)
        current_row += 1
        
        mode_info = tk.Label(mode_section, 
                            text="Select AI mode if you want AI assistance, or skip this for traditional CAT editing:",
                            bg="white", font=("Segoe UI", 8), fg="#1a365d", wraplength=580)
        mode_info.pack(anchor="w", pady=(0,5))
        
        mode_frame = tk.Frame(mode_section, bg="white")
        mode_frame.pack(fill=tk.X, pady=5)
        
        self.operation_mode_var = tk.StringVar(value="Translate")
        
        # Pre-Translation option with description
        pretrans_frame = tk.Frame(mode_frame, bg="white")
        pretrans_frame.pack(anchor="w", pady=2)
        tk.Radiobutton(pretrans_frame, text="AI Pre-Translation Mode", 
                      variable=self.operation_mode_var, value="Translate", 
                      command=self.update_ui_for_mode, bg="white", 
                      font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        tk.Label(pretrans_frame, text="  (Use AI to translate source text)", 
                fg="gray", bg="white", font=("Segoe UI", 8)).pack(side=tk.LEFT)
        
        # Proofreading option with description
        proofread_frame = tk.Frame(mode_frame, bg="white")
        proofread_frame.pack(anchor="w", pady=2)
        tk.Radiobutton(proofread_frame, text="AI Proofreading Mode", 
                      variable=self.operation_mode_var, value="Proofread", 
                      command=self.update_ui_for_mode, bg="white", 
                      font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        tk.Label(proofread_frame, text="  (Use AI to revise existing translations)", 
                fg="gray", bg="white", font=("Segoe UI", 8)).pack(side=tk.LEFT)
        
        # Note about working without AI
        traditional_note = tk.Label(mode_section, 
                                   text="💡 TIP: You can also work without AI - just import your file and choose a view mode below",
                                   bg="#fffacd", font=("Segoe UI", 8, "italic"), fg="#8b4513", 
                                   relief="solid", borderwidth=1, padx=5, pady=3)
        traditional_note.pack(fill=tk.X, pady=(5,0))

        self.input_file_var = tk.StringVar(); self.output_file_var = tk.StringVar()
        self.tm_file_var = tk.StringVar(); self.drawings_folder_var = tk.StringVar()
        self.cat_docx_file_var = tk.StringVar()

        # === INPUT FORMAT SECTION ===
        input_section = tk.LabelFrame(left_frame, text="� Input Document", 
                                      font=("Segoe UI", 11, "bold"), padx=10, pady=10, bg="white", 
                                      relief="groove", borderwidth=2)
        input_section.grid(row=current_row, column=0, columnspan=3, pady=(5,10), sticky="ew", padx=5)
        current_row += 1
        
        input_info = tk.Label(input_section, 
                             text="Choose your input format - both can be opened in Grid/Split/Document view:",
                             bg="white", font=("Segoe UI", 9), fg="#1a365d")
        input_info.pack(anchor="w", pady=(0,8))
        
        # TXT Input Option
        txt_input_frame = tk.LabelFrame(input_section, text="Option 1: TXT File (from memoQ/Trados)", 
                                       font=("Segoe UI", 9, "bold"), padx=8, pady=8, bg="#f0f8ff", 
                                       relief="solid", borderwidth=1, fg="#003d82")
        txt_input_frame.pack(fill=tk.X, pady=(0,8))
        
        txt_row = 0
        tk.Label(txt_input_frame, text="For bilingual TXT files (one segment per line)", 
                bg="#f0f8ff", font=("Segoe UI", 8), fg="gray").grid(row=txt_row, column=0, columnspan=3, sticky="w", padx=5, pady=(0,4))
        txt_row += 1
        
        self.input_file_label = tk.Label(txt_input_frame, text="Input TXT File:", bg="#f0f8ff") 
        self.input_file_label.grid(row=txt_row, column=0, padx=5, pady=4, sticky="w")
        tk.Entry(txt_input_frame, textvariable=self.input_file_var, width=50, state="readonly").grid(row=txt_row, column=1, padx=5, pady=4, sticky="ew")
        tk.Button(txt_input_frame, text="Browse & Load...", command=self.browse_and_load_txt).grid(row=txt_row, column=2, padx=5, pady=4)
        txt_row += 1
        
        tk.Label(txt_input_frame, text="Output File (TXT + TMX):", bg="#f0f8ff").grid(row=txt_row, column=0, padx=5, pady=4, sticky="w")
        tk.Entry(txt_input_frame, textvariable=self.output_file_var, width=50, state="readonly").grid(row=txt_row, column=1, padx=5, pady=4, sticky="ew")
        tk.Button(txt_input_frame, text="Set Output...", command=self.browse_output_file).grid(row=txt_row, column=2, padx=5, pady=4)
        
        txt_input_frame.grid_columnconfigure(1, weight=1)
        
        # DOCX Input Option
        docx_input_frame = tk.LabelFrame(input_section, text="Option 2: DOCX File (direct import)", 
                                        font=("Segoe UI", 9, "bold"), padx=8, pady=8, bg="#f0fff0", 
                                        relief="solid", borderwidth=1, fg="#006600")
        docx_input_frame.pack(fill=tk.X, pady=(0,0))
        
        docx_row = 0
        tk.Label(docx_input_frame, text="For Word documents with formatting preservation", 
                bg="#f0fff0", font=("Segoe UI", 8), fg="gray").grid(row=docx_row, column=0, columnspan=3, sticky="w", padx=5, pady=(0,4))
        docx_row += 1
        
        tk.Label(docx_input_frame, text="Input DOCX File:", bg="#f0fff0").grid(row=docx_row, column=0, padx=5, pady=4, sticky="w")
        tk.Entry(docx_input_frame, textvariable=self.cat_docx_file_var, width=50, state="readonly").grid(row=docx_row, column=1, padx=5, pady=4, sticky="ew")
        tk.Button(docx_input_frame, text="Browse & Load...", command=self.import_docx_file).grid(row=docx_row, column=2, padx=5, pady=4)
        docx_row += 1
        
        # Statistics row
        self.cat_stats_label = tk.Label(docx_input_frame, text="No document loaded", 
                                       fg="gray", bg="#f0fff0", font=("Segoe UI", 8))
        self.cat_stats_label.grid(row=docx_row, column=0, columnspan=3, sticky="w", padx=5, pady=(0,4))
        
        docx_input_frame.grid_columnconfigure(1, weight=1)

        # === VIEW MODE SECTION ===
        view_section = tk.LabelFrame(left_frame, text="🖥️ Editor View Mode", 
                                     font=("Segoe UI", 11, "bold"), padx=10, pady=10, bg="white", 
                                     relief="groove", borderwidth=2)
        view_section.grid(row=current_row, column=0, columnspan=3, pady=(5,10), sticky="ew", padx=5)
        current_row += 1
        
        view_info = tk.Label(view_section, 
                            text="After loading a file, choose how to view and edit your segments:",
                            bg="white", font=("Segoe UI", 9), fg="#1a365d")
        view_info.pack(anchor="w", pady=(0,8))
        
        # View buttons frame
        view_buttons_frame = tk.Frame(view_section, bg="white")
        view_buttons_frame.pack(fill=tk.X, pady=(0,8))
        
        self.grid_view_btn = tk.Button(view_buttons_frame, text="📊 Grid View", 
                                      command=self.open_grid_view, width=18, height=2,
                                      state="disabled", font=("Segoe UI", 9, "bold"))
        self.grid_view_btn.pack(side=tk.LEFT, padx=(0,5))
        
        self.split_view_btn = tk.Button(view_buttons_frame, text="📑 Split View", 
                                       command=self.open_split_view, width=18, height=2,
                                       state="disabled", font=("Segoe UI", 9, "bold"))
        self.split_view_btn.pack(side=tk.LEFT, padx=(0,5))
        
        self.document_view_btn = tk.Button(view_buttons_frame, text="📄 Document View", 
                                          command=self.open_document_view, width=18, height=2,
                                          state="disabled", font=("Segoe UI", 9, "bold"))
        self.document_view_btn.pack(side=tk.LEFT)
        
        # View descriptions
        view_desc_frame = tk.Frame(view_section, bg="white")
        view_desc_frame.pack(fill=tk.X)
        
        tk.Label(view_desc_frame, text="• Grid View: Inline table editing (memoQ-style)", 
                bg="white", font=("Segoe UI", 8), fg="gray").pack(anchor="w", padx=5, pady=1)
        tk.Label(view_desc_frame, text="• Split View: Segment list + editor panel (side-by-side)", 
                bg="white", font=("Segoe UI", 8), fg="gray").pack(anchor="w", padx=5, pady=1)
        tk.Label(view_desc_frame, text="• Document View: Document flow with clickable segments", 
                bg="white", font=("Segoe UI", 8), fg="gray").pack(anchor="w", padx=5, pady=1)
        
        # AI Pre-Translation button (works with any view)
        ai_actions_frame = tk.Frame(view_section, bg="white")
        ai_actions_frame.pack(fill=tk.X, pady=(10,0))
        
        self.cat_pretranslate_btn = tk.Button(ai_actions_frame, text="🤖 AI-Assisted Pre-Translation", 
                                             command=self.ai_pretranslate_segments,
                                             state="disabled", font=("Segoe UI", 9))
        self.cat_pretranslate_btn.pack(side=tk.LEFT, padx=(0,5))
        
        self.cat_export_btn = tk.Button(ai_actions_frame, text="💾 Export Translated Document", 
                                       command=self.export_translated_docx,
                                       state="disabled", font=("Segoe UI", 9))
        self.cat_export_btn.pack(side=tk.LEFT, padx=(0,5))
        
        tk.Button(ai_actions_frame, text="🗑️ Clear Document", 
                 command=self.clear_cat_document).pack(side=tk.LEFT)

        # Shared Settings Section - COLLAPSIBLE
        self.shared_settings_frame = tk.LabelFrame(left_frame, text="⚙️ Shared Settings - Click to expand/collapse", 
                                                  font=("Segoe UI", 11, "bold"), padx=10, pady=8, cursor="hand2",
                                                  bg="white", relief="groove", borderwidth=2)
        self.shared_settings_frame.grid(row=current_row, column=0, columnspan=3, padx=5, pady=(10,10), sticky="ew", ipadx=5, ipady=5)
        self.shared_settings_frame.bind("<Button-1>", self.toggle_shared_settings)
        current_row += 1
        
        # Initially hidden content frame
        self.shared_settings_content = tk.Frame(self.shared_settings_frame, bg="white")
        self.shared_settings_visible = False  # Start collapsed
        
        # Debug label
        settings_debug_label = tk.Label(self.shared_settings_frame, 
                                       text="🔧 TM, Tracked Changes, Document Images, Custom Instructions", 
                                       font=("TkDefaultFont", 8), fg="gray", bg="white")
        settings_debug_label.pack(pady=2)
        
        self.setup_shared_settings_content()

        # Advanced Prompts Section (collapsible) - SHARED BY BOTH WORKFLOWS
        self.advanced_prompts_frame = tk.LabelFrame(left_frame, text="📝 Prompt Library - Optional Enhancement (Click to expand/collapse)", 
                                                   font=("Segoe UI", 11, "bold"), padx=10, pady=8, cursor="hand2", 
                                                   bg="white", relief="groove", borderwidth=2)
        self.advanced_prompts_frame.grid(row=current_row, column=0, columnspan=3, padx=5, pady=(15,10), sticky="ew", ipadx=5, ipady=5); current_row += 1
        self.advanced_prompts_frame.bind("<Button-1>", self.toggle_advanced_prompts)
        
        # Initially hidden content frame
        self.advanced_prompts_content = tk.Frame(self.advanced_prompts_frame)
        self.advanced_prompts_visible = False  # Start collapsed
        
        self.setup_advanced_prompts_content()
        
        # Description label
        debug_label = tk.Label(self.advanced_prompts_frame, text="✏ Customize AI system prompts for specialized domains (legal, medical, etc.)", 
                              font=("TkDefaultFont", 8), fg="gray", bg="white")
        debug_label.pack(pady=2)
        
        # Project Library Section (collapsible) 
        self.project_library_frame = tk.LabelFrame(left_frame, text="💼 Project Library (Click to expand/collapse)", 
                                                  font=("Segoe UI", 11, "bold"), padx=10, pady=8, cursor="hand2", 
                                                  bg="white", relief="groove", borderwidth=2)
        self.project_library_frame.grid(row=current_row, column=0, columnspan=3, padx=5, pady=(15,10), sticky="ew", ipadx=5, ipady=5); current_row += 1
        self.project_library_frame.bind("<Button-1>", self.toggle_project_library)
        
        # Initially hidden content frame
        self.project_library_content = tk.Frame(self.project_library_frame)
        self.project_library_visible = False  # Start collapsed
        
        self.setup_project_library_content()
        
        # Project Library debug label
        project_debug_label = tk.Label(self.project_library_frame, text="💾 Project management - Save entire workspace state", 
                                      font=("TkDefaultFont", 8), fg="gray")
        project_debug_label.pack(pady=2)
        
        self.source_lang_var = tk.StringVar(value="Dutch")
        self.target_lang_var = tk.StringVar(value="English")
        self.chunk_size_var = tk.StringVar(value="100")

        # AI Provider and Model Selection
        provider_frame = tk.Frame(left_frame, bg="white")
        provider_frame.grid(row=current_row, column=0, columnspan=3, pady=2, sticky="ew", padx=5)
        tk.Label(provider_frame, text="AI Provider:", bg="white").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        
        self.provider_var = tk.StringVar(value="Claude")  # Claude as default
        provider_combo = ttk.Combobox(provider_frame, textvariable=self.provider_var, width=15, state="readonly")
        available_providers = []
        if CLAUDE_AVAILABLE and self.api_keys["claude"]: available_providers.append("Claude")
        if GOOGLE_AI_AVAILABLE and self.api_keys["google"]: available_providers.append("Gemini")
        if OPENAI_AVAILABLE and self.api_keys["openai"]: available_providers.append("OpenAI")
        
        if not available_providers:
            # Add all providers but with warnings
            if CLAUDE_AVAILABLE: available_providers.append("Claude")
            if GOOGLE_AI_AVAILABLE: available_providers.append("Gemini")
            if OPENAI_AVAILABLE: available_providers.append("OpenAI")
        
        provider_combo['values'] = available_providers
        if available_providers and self.provider_var.get() not in available_providers:
            self.provider_var.set(available_providers[0])
        provider_combo.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        provider_combo.bind('<<ComboboxSelected>>', self.on_provider_changed)
        
        tk.Label(provider_frame, text="Model:", bg="white").grid(row=0, column=2, padx=(20,5), pady=2, sticky="w")
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(provider_frame, textvariable=self.model_var, width=30, state="readonly")
        self.model_combo.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        
        # Initialize models for default provider
        self.update_available_models()
        current_row += 1

        setting_fields_data = [
            ("Source Language:", self.source_lang_var, 30), ("Target Language:", self.target_lang_var, 30),
            ("Chunk Size (lines):", self.chunk_size_var, 10)
        ]
        for text, var, width in setting_fields_data:
            tk.Label(left_frame, text=text, bg="white").grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
            tk.Entry(left_frame, textvariable=var, width=width).grid(row=current_row, column=1, padx=5, pady=2, sticky="w"); current_row += 1

        # Switch Languages button
        switch_lang_frame = tk.Frame(left_frame, bg="white")
        switch_lang_frame.grid(row=current_row-2, column=2, padx=(10,5), pady=2, sticky="w")  # Align with language fields
        self.switch_lang_button = tk.Button(switch_lang_frame, text="⇄ Switch languages", command=self.switch_languages, width=14, height=1)
        self.switch_lang_button.pack()

        buttons_frame = tk.Frame(left_frame, bg="white"); buttons_frame.grid(row=current_row, column=0, columnspan=3, pady=5); current_row += 1
        self.process_button = tk.Button(buttons_frame, text="Start Process", command=self.start_processing_thread, width=15, height=2); self.process_button.pack(side=tk.LEFT, padx=10) 
        self.list_models_button = tk.Button(buttons_frame, text="List Models", command=self.list_available_models, width=15); self.list_models_button.pack(side=tk.LEFT, padx=10) 
        self.refresh_models_button = tk.Button(buttons_frame, text="Refresh Models", command=self.update_available_models, width=15); self.refresh_models_button.pack(side=tk.LEFT, padx=10)
        
        # Log section in bottom right frame - extra sharp heading font
        tk.Label(log_frame, text="📝 Processing Log", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=(5,2))
        self.log_text = scrolledtext.ScrolledText(log_frame, width=40, height=15, wrap=tk.WORD, state="disabled", 
                                                 bg="white", font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,5))
        
        # Configure main window column weights for left frame
        left_frame.grid_columnconfigure(1, weight=1)
        
        self.check_log_queue()
        if not PIL_AVAILABLE: self.update_log("WARN: Document Images Folder feature limited (Pillow library not found).")
        self.update_log("Select operation mode. Ensure input file format matches selected mode.")
        
        # Final library checks
        if not GOOGLE_AI_AVAILABLE: self.update_log(f"WARN: Google AI unavailable: {GOOGLE_AI_IMPORT_ERROR_MESSAGE}")
        if not CLAUDE_AVAILABLE: self.update_log(f"WARN: Claude unavailable: {CLAUDE_IMPORT_ERROR_MESSAGE}")
        if not OPENAI_AVAILABLE: self.update_log(f"WARN: OpenAI unavailable: {OPENAI_IMPORT_ERROR_MESSAGE}")
        
        # Disable buttons if no working providers
        working_providers = self.get_working_providers()
        if not working_providers:
            self.update_log("CRITICAL: No working AI providers available!")
            self.process_button.config(state="disabled")
            self.list_models_button.config(state="disabled")
            self.refresh_models_button.config(state="disabled")

    def get_working_providers(self):
        """Get list of providers that have both library and API key available"""
        working = []
        if CLAUDE_AVAILABLE and self.api_keys["claude"]:
            working.append("Claude")
        if GOOGLE_AI_AVAILABLE and self.api_keys["google"]:
            working.append("Gemini")
        if OPENAI_AVAILABLE and self.api_keys["openai"]:
            working.append("OpenAI")
        return working

    def on_provider_changed(self, event=None):
        """Called when user changes AI provider"""
        self.update_available_models()

    def switch_languages(self):
        """Switch source and target languages"""
        # Get current values
        current_source = self.source_lang_var.get()
        current_target = self.target_lang_var.get()
        
        # Swap them
        self.source_lang_var.set(current_target)
        self.target_lang_var.set(current_source)
        
        # Log the switch
        self.log_queue.put(f"[GUI] Languages switched: {current_source} ⇄ {current_target}")

    def update_available_models(self):
        """Update the model dropdown based on selected provider"""
        provider = self.provider_var.get()
        if not provider:
            return
            
        # Get appropriate API key
        api_key = ""
        if provider == "Claude":
            api_key = self.api_keys["claude"]
        elif provider == "Gemini":
            api_key = self.api_keys["google"]
        elif provider == "OpenAI":
            api_key = self.api_keys["openai"]
        
        # Get available models
        models = get_available_models(provider, api_key, self.log_queue)
        self.model_combo['values'] = models
        
        # Set default model
        if models:
            if provider == "Claude":
                default_model = "claude-3-5-sonnet-20241022"
            elif provider == "OpenAI":
                default_model = "gpt-4o"
            else:  # Gemini
                default_model = "gemini-2.5-pro-preview-05-06"
            
            if default_model in models:
                self.model_var.set(default_model)
            else:
                self.model_var.set(models[0])
        
        self.update_log(f"Updated models for {provider}: {len(models)} available")

    def update_ui_for_mode(self):
        mode = self.operation_mode_var.get()
        if mode == "Translate":
            self.input_file_label.config(text="Input Text File (one source per line):")
            self.tm_file_label.config(text="TM File (txt/tmx):") 
            self.process_button.config(text="Translate")
        elif mode == "Proofread":
            self.input_file_label.config(text="Input Text File (source<tab>TARGET<tab>[comment]):")
            self.tm_file_label.config(text="TM File (N/A for Proofread):") 
            self.process_button.config(text="Proofread")

    def setup_advanced_prompts_content(self):
        """Setup the content of the advanced prompts section"""
        # Initialize default system prompts (generic for all document types)
        self.default_translate_prompt = ("You are an expert {source_lang} to {target_lang} translator with deep understanding of context and nuance. "
                                       "The full document context is provided in 'FULL DOCUMENT CONTEXT' below for reference. "
                                       "Translate ONLY the sentences from 'SENTENCES TO TRANSLATE' later, maintaining their original line numbers.\n\n"
                                       "If a sentence refers to figures, images, or diagrams (e.g., 'Figure 1A', 'Chart 2', 'Diagram B'), relevant images may be provided just before that sentence. "
                                       "Use these visual elements as crucial context for accurately translating references to parts, features, relationships, or data shown in those figures.\n\n"
                                       "Present your output ONLY as a numbered list of translations for the requested sentences, using their original numbering. "
                                       "Maintain accuracy, appropriate terminology for the document type, and natural fluency in the target language.")

        self.default_proofread_prompt = ("You are an expert proofreader and editor for {source_lang} → {target_lang} translations, skilled in various document types and domains.\n\n"
                                       "For each segment you receive a SOURCE SEGMENT and EXISTING TRANSLATION. "
                                       "Your tasks: improve accuracy, ensure terminology consistency, enhance readability, correct grammar, improve fluency, verify completeness, and maintain consistency with visual elements.\n\n"
                                       "OUTPUT FORMAT STRICTLY:\n"
                                       "1) Numbered list of revised {target_lang} translations (use same numbering; if no changes needed, reproduce the original).\n"
                                       "2) Then a section:\n---CHANGES SUMMARY START---\n"
                                       "Per modified line: '<line>. <brief description of changes>' OR if none changed: 'No changes made to any segment in this batch.'\n"
                                       "---CHANGES SUMMARY END---")

        # Store current prompts (initially same as defaults)
        self.current_translate_prompt = self.default_translate_prompt
        self.current_proofread_prompt = self.default_proofread_prompt

    def setup_shared_settings_content(self):
        """Setup the shared settings content (TM, tracked changes, etc.)"""
        # This will be populated when expanded
        pass
    
    def toggle_shared_settings(self, event=None):
        """Toggle visibility of shared settings section"""
        if not self.shared_settings_visible:
            self.show_shared_settings()
        else:
            self.hide_shared_settings()
    
    def show_shared_settings(self):
        """Show the shared settings content"""
        self.shared_settings_visible = True
        self.shared_settings_frame.config(text="⚙️ Shared Settings (Click to collapse) ▼")
        
        # Show content frame
        self.shared_settings_content.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Clear and rebuild content
        for widget in self.shared_settings_content.winfo_children():
            widget.destroy()
        
        # Description
        tk.Label(self.shared_settings_content, 
                text="These context sources enhance AI translation quality in both Legacy and CAT workflows:",
                bg="white", font=("Segoe UI", 8), fg="gray", wraplength=560, justify=tk.LEFT).grid(
                row=0, column=0, columnspan=3, padx=5, pady=(0,8), sticky="w")
        
        context_row = 1
        
        # TM File row
        self.tm_file_label = tk.Label(self.shared_settings_content, text="Translation Memory (TXT/TMX):", bg="white") 
        self.tm_file_label.grid(row=context_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(self.shared_settings_content, textvariable=self.tm_file_var, width=50, state="readonly").grid(row=context_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(self.shared_settings_content, text="Browse TM...", command=self.browse_tm_file).grid(row=context_row, column=2, padx=5, pady=2)
        context_row += 1

        # Tracked Changes row
        tk.Label(self.shared_settings_content, text="Tracked-changes:", bg="white").grid(row=context_row, column=0, padx=5, pady=2, sticky="w")
        
        tracked_changes_inner_frame = tk.Frame(self.shared_settings_content, bg="white")
        tracked_changes_inner_frame.grid(row=context_row, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        
        self.tracked_changes_status_label = tk.Label(tracked_changes_inner_frame, text="No tracked changes loaded", fg="gray", bg="white")
        self.tracked_changes_status_label.pack(side=tk.LEFT)
        
        tk.Button(tracked_changes_inner_frame, text="Load Files...", command=self.load_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        tk.Button(tracked_changes_inner_frame, text="Browse Changes", command=self.browse_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        tk.Button(tracked_changes_inner_frame, text="Clear", command=self.clear_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        context_row += 1

        # Document Images Folder row
        self.document_images_label = tk.Label(self.shared_settings_content, text="Document Images Folder:", bg="white")
        self.document_images_label.grid(row=context_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(self.shared_settings_content, textvariable=self.drawings_folder_var, width=50, state="readonly").grid(row=context_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(self.shared_settings_content, text="Browse...", command=self.browse_drawings_folder).grid(row=context_row, column=2, padx=5, pady=2)
        context_row += 1

        # Custom Instructions row
        tk.Label(self.shared_settings_content, text="Custom Instructions for AI:", bg="white").grid(row=context_row, column=0, padx=5, pady=(5,0), sticky="nw")
        self.custom_instructions_text = tk.Text(self.shared_settings_content, height=4, width=50, wrap=tk.WORD, borderwidth=1, relief="solid")
        self.custom_instructions_text.grid(row=context_row, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        context_row += 1

        # Configure column weights
        self.shared_settings_content.grid_columnconfigure(1, weight=1)
    
    def hide_shared_settings(self):
        """Hide the shared settings content"""
        self.shared_settings_visible = False
        self.shared_settings_frame.config(text="⚙️ Shared Settings - Click to expand ▶")
        self.shared_settings_content.pack_forget()

    def toggle_advanced_prompts(self, event=None):
        """Toggle visibility of advanced prompts section"""
        if not self.advanced_prompts_visible:
            self.show_advanced_prompts()
        else:
            self.hide_advanced_prompts()

    def show_advanced_prompts(self):
        """Show the advanced prompts content"""
        self.advanced_prompts_visible = True
        self.advanced_prompts_frame.config(text="📝 Prompt Library (Click to collapse) ▼")
        
        # Create the content frame if it doesn't exist
        self.advanced_prompts_content.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Clear any existing content
        for widget in self.advanced_prompts_content.winfo_children():
            widget.destroy()
            
        # Create notebook for tabs
        notebook = ttk.Notebook(self.advanced_prompts_content)
        notebook.pack(fill="both", expand=True)
        
        # Translation prompt tab
        translate_frame = ttk.Frame(notebook)
        notebook.add(translate_frame, text="⚡ Translation Prompt")
        
        tk.Label(translate_frame, text="ACTIVE system prompt for Translation mode:", 
                font=("Segoe UI", 10, "bold"), bg="white", fg="#2d5a2d").pack(anchor="w", padx=5, pady=(5,2))
        
        tk.Label(translate_frame, text="Available variables: {source_lang}, {target_lang}", 
                fg="gray", font=("Segoe UI", 8), bg="white").pack(anchor="w", padx=5)
        
        self.translate_prompt_text = tk.Text(translate_frame, height=12, wrap=tk.WORD, 
                                           borderwidth=1, relief="solid", font=("Consolas", 9))
        self.translate_prompt_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.translate_prompt_text.insert("1.0", self.current_translate_prompt)
        
        translate_buttons = tk.Frame(translate_frame, bg="white")
        translate_buttons.pack(fill="x", padx=5, pady=(0,5))
        tk.Button(translate_buttons, text="Reset to Default", 
                 command=self.reset_translate_prompt).pack(side="left", padx=(0,5))
        tk.Button(translate_buttons, text="Preview Final Prompt", 
                 command=self.preview_translate_prompt).pack(side="left", padx=(0,5))
        
        # Proofreading prompt tab
        proofread_frame = ttk.Frame(notebook)
        notebook.add(proofread_frame, text="⚡ Proofreading Prompt")
        
        tk.Label(proofread_frame, text="ACTIVE system prompt for Proofreading mode:", 
                font=("Segoe UI", 10, "bold"), bg="white", fg="#2d5a2d").pack(anchor="w", padx=5, pady=(5,2))
        
        tk.Label(proofread_frame, text="Available variables: {source_lang}, {target_lang}", 
                fg="gray", font=("Segoe UI", 8), bg="white").pack(anchor="w", padx=5)
        
        self.proofread_prompt_text = tk.Text(proofread_frame, height=12, wrap=tk.WORD, 
                                           borderwidth=1, relief="solid", font=("Consolas", 9))
        self.proofread_prompt_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.proofread_prompt_text.insert("1.0", self.current_proofread_prompt)
        
        proofread_buttons = tk.Frame(proofread_frame, bg="white")
        proofread_buttons.pack(fill="x", padx=5, pady=(0,5))
        tk.Button(proofread_buttons, text="Reset to Default", 
                 command=self.reset_proofread_prompt).pack(side="left", padx=(0,5))
        tk.Button(proofread_buttons, text="Preview Final Prompt", 
                 command=self.preview_proofread_prompt).pack(side="left", padx=(0,5))
        
        # Custom Prompt Management tab
        management_frame = ttk.Frame(notebook)
        notebook.add(management_frame, text="📁 Prompt Library")
        
        # Create custom prompts directory if it doesn't exist
        self.custom_prompts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompts")
        os.makedirs(self.custom_prompts_dir, exist_ok=True)
        
        tk.Label(management_frame, text="Custom System Prompt Library", 
                font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w", padx=5, pady=(5,2))
        
        tk.Label(management_frame, text="Save, load, and manage your custom system prompt templates:", 
                fg="gray", font=("Segoe UI", 8), bg="white").pack(anchor="w", padx=5, pady=(0,5))
        
        # Prompt name entry
        name_frame = tk.Frame(management_frame, bg="white")
        name_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(name_frame, text="Prompt Set Name:", bg="white").pack(side="left", padx=(0,5))
        self.prompt_name_var = tk.StringVar()
        tk.Entry(name_frame, textvariable=self.prompt_name_var, width=30).pack(side="left", padx=(0,5))
        
        # Private checkbox for custom prompts
        self.prompt_private_var = tk.BooleanVar(value=False)
        tk.Checkbutton(name_frame, text="Save to Private Folder", 
                      variable=self.prompt_private_var, bg="white").pack(side="left", padx=(10,0))
        
        # Save/Load buttons
        save_load_frame = tk.Frame(management_frame, bg="white")
        save_load_frame.pack(fill="x", padx=5, pady=5)
        tk.Button(save_load_frame, text="💾 Save Current Prompts", 
                 command=self.save_custom_prompts).pack(side="left", padx=(0,5))
        tk.Button(save_load_frame, text="📂 Load Selected", 
                 command=self.load_custom_prompts).pack(side="left", padx=(0,5))
        tk.Button(save_load_frame, text="🗑️ Delete Selected", 
                 command=self.delete_custom_prompts).pack(side="left", padx=(0,5))
        
        # Available prompts list
        tk.Label(management_frame, text="Saved Prompt Sets:", 
                font=("Segoe UI", 9, "bold"), bg="white").pack(anchor="w", padx=5, pady=(10,2))
        
        # Show clickable folder location
        custom_prompts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompts")
        folder_frame = tk.Frame(management_frame, bg="white")
        folder_frame.pack(anchor="w", padx=5, pady=(0,5))
        
        tk.Label(folder_frame, text="📁 Folder:", 
                font=("Segoe UI", 8), fg="gray", bg="white").pack(side="left")
        
        folder_button = tk.Button(folder_frame, text=custom_prompts_path,
                                 font=("Segoe UI", 8), fg="blue", bg="white",
                                 relief="flat", cursor="hand2", bd=0,
                                 command=self.open_custom_prompts_folder)
        folder_button.pack(side="left", padx=(3,0))
        
        # Add hover effects for the clickable path
        def on_enter(event):
            folder_button.config(fg="darkblue", font=("Segoe UI", 8, "underline"))
        def on_leave(event):
            folder_button.config(fg="blue", font=("Segoe UI", 8))
            
        folder_button.bind("<Enter>", on_enter)
        folder_button.bind("<Leave>", on_leave)
        
        list_frame = tk.Frame(management_frame, bg="white")
        list_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
        
        # Listbox with scrollbar
        list_scroll_frame = tk.Frame(list_frame, bg="white")
        list_scroll_frame.pack(fill="both", expand=True)
        
        self.prompts_listbox = tk.Listbox(list_scroll_frame, height=8, font=("Segoe UI", 9))
        prompts_scrollbar = tk.Scrollbar(list_scroll_frame, orient="vertical", command=self.prompts_listbox.yview)
        self.prompts_listbox.config(yscrollcommand=prompts_scrollbar.set)
        
        self.prompts_listbox.pack(side="left", fill="both", expand=True)
        prompts_scrollbar.pack(side="right", fill="y")
        
        # Bind selection event
        self.prompts_listbox.bind('<<ListboxSelect>>', self.on_prompt_selection)
        
        # Refresh the list
        self.refresh_prompts_list()

    def hide_advanced_prompts(self):
        """Hide the advanced prompts content"""
        self.advanced_prompts_visible = False
        self.advanced_prompts_frame.config(text="📝 Prompt Library (Click to expand) ▶")
        
        # Save current prompt content before hiding
        if hasattr(self, 'translate_prompt_text'):
            self.current_translate_prompt = self.translate_prompt_text.get("1.0", tk.END).strip()
        if hasattr(self, 'proofread_prompt_text'):
            self.current_proofread_prompt = self.proofread_prompt_text.get("1.0", tk.END).strip()
        
        self.advanced_prompts_content.pack_forget()

    def reset_translate_prompt(self):
        """Reset translation prompt to default"""
        self.translate_prompt_text.delete("1.0", tk.END)
        self.translate_prompt_text.insert("1.0", self.default_translate_prompt)
        self.update_log("Translation prompt reset to default")

    def reset_proofread_prompt(self):
        """Reset proofreading prompt to default"""
        self.proofread_prompt_text.delete("1.0", tk.END)
        self.proofread_prompt_text.insert("1.0", self.default_proofread_prompt)
        self.update_log("Proofreading prompt reset to default")

    def preview_translate_prompt(self):
        """Show preview of final translation prompt with current language settings"""
        current_prompt = self.translate_prompt_text.get("1.0", tk.END).strip()
        source_lang = self.source_lang_var.get()
        target_lang = self.target_lang_var.get()
        
        try:
            final_prompt = current_prompt.format(source_lang=source_lang, target_lang=target_lang)
            self.show_prompt_preview("Translation Prompt Preview", final_prompt)
        except KeyError as e:
            messagebox.showerror("Template Error", f"Invalid template variable: {e}")

    def preview_proofread_prompt(self):
        """Show preview of final proofreading prompt with current language settings"""
        current_prompt = self.proofread_prompt_text.get("1.0", tk.END).strip()
        source_lang = self.source_lang_var.get()
        target_lang = self.target_lang_var.get()
        
        try:
            final_prompt = current_prompt.format(source_lang=source_lang, target_lang=target_lang)
            self.show_prompt_preview("Proofreading Prompt Preview", final_prompt)
        except KeyError as e:
            messagebox.showerror("Template Error", f"Invalid template variable: {e}")

    def show_prompt_preview(self, title, prompt_text):
        """Show a preview window with the final prompt"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title(title)
        preview_window.geometry("800x600")
        
        # Make it modal
        preview_window.transient(self.root)
        preview_window.grab_set()
        
        tk.Label(preview_window, text=f"{title} (with current language settings)", 
                font=("Segoe UI", 11, "bold")).pack(padx=10, pady=(10,5))
        
        text_widget = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD, 
                                              font=("Consolas", 9), state="normal")
        text_widget.pack(fill="both", expand=True, padx=10, pady=5)
        text_widget.insert("1.0", prompt_text)
        text_widget.config(state="disabled")
        
        button_frame = tk.Frame(preview_window)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Close", command=preview_window.destroy).pack()

    def get_custom_system_prompt(self, mode):
        """Get the current custom system prompt for the specified mode"""
        if mode == "Translate":
            if hasattr(self, 'translate_prompt_text') and self.advanced_prompts_visible:
                return self.translate_prompt_text.get("1.0", tk.END).strip()
            else:
                return self.current_translate_prompt
        elif mode == "Proofread":
            if hasattr(self, 'proofread_prompt_text') and self.advanced_prompts_visible:
                return self.proofread_prompt_text.get("1.0", tk.END).strip()
            else:
                return self.current_proofread_prompt
        return ""

    # === Custom Prompt Management Methods ===
    
    def save_custom_prompts(self):
        """Save current prompts to a custom file"""
        prompt_name = self.prompt_name_var.get().strip()
        if not prompt_name:
            messagebox.showwarning("No Name", "Please enter a name for your prompt set.")
            return
            
        # Sanitize filename
        safe_name = "".join(c for c in prompt_name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_name:
            messagebox.showwarning("Invalid Name", "Please enter a valid name (letters, numbers, spaces, hyphens, underscores only).")
            return
            
        filename = f"{safe_name}.json"
        
        # Determine which directory to save to
        if self.prompt_private_var.get():
            # Save to private folder
            save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompts_private")
            os.makedirs(save_dir, exist_ok=True)
        else:
            # Save to public folder
            save_dir = self.custom_prompts_dir
            
        filepath = os.path.join(save_dir, filename)
        
        # Get current prompts from the text widgets
        translate_prompt = self.translate_prompt_text.get("1.0", tk.END).strip() if hasattr(self, 'translate_prompt_text') else self.current_translate_prompt
        proofread_prompt = self.proofread_prompt_text.get("1.0", tk.END).strip() if hasattr(self, 'proofread_prompt_text') else self.current_proofread_prompt
        
        prompt_data = {
            "name": prompt_name,
            "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "translate_prompt": translate_prompt,
            "proofread_prompt": proofread_prompt,
            "version": "2.2.0"
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
            
            self.refresh_prompts_list()
            folder_type = "private" if self.prompt_private_var.get() else "public"
            self.update_log(f"[Prompts] Saved custom prompt set to {folder_type} folder: '{prompt_name}'")
            messagebox.showinfo("Saved", f"Prompt set '{prompt_name}' saved successfully to {folder_type} folder!")
            
            # Select the newly saved item
            items = list(self.prompts_listbox.get(0, tk.END))
            try:
                # Add [Private] prefix if it's a private prompt for selection
                search_name = f"[Private] {prompt_name}" if self.prompt_private_var.get() else prompt_name
                index = items.index(search_name)
                self.prompts_listbox.selection_clear(0, tk.END)
                self.prompts_listbox.selection_set(index)
            except ValueError:
                pass
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save prompt set: {str(e)}")
            self.update_log(f"[ERROR] Failed to save prompts: {str(e)}")

    def load_custom_prompts(self):
        """Load selected custom prompts"""
        selection = self.prompts_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a prompt set to load.")
            return
            
        selected_name = self.prompts_listbox.get(selection[0])
        if selected_name == "[Default System Prompts]":
            # Reset to defaults
            self.reset_translate_prompt()
            self.reset_proofread_prompt()
            self.update_log("[Prompts] Loaded default system prompts")
            messagebox.showinfo("Loaded", "Default system prompts loaded.")
            return
            
        # Determine if this is a private prompt and get the correct path
        if selected_name.startswith("[Private] "):
            # Private prompt - remove prefix and look in private folder
            actual_name = selected_name[10:]  # Remove "[Private] " prefix
            filename = f"{actual_name}.json"
            private_prompts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompts_private")
            filepath = os.path.join(private_prompts_dir, filename)
        else:
            # Public prompt - look in public folder
            filename = f"{selected_name}.json"
            filepath = os.path.join(self.custom_prompts_dir, filename)
        
        if not os.path.exists(filepath):
            messagebox.showerror("File Not Found", f"Prompt file not found: {filename}")
            self.refresh_prompts_list()
            return
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                prompt_data = json.load(f)
            
            # Load into text widgets if they exist
            if hasattr(self, 'translate_prompt_text'):
                self.translate_prompt_text.delete("1.0", tk.END)
                self.translate_prompt_text.insert("1.0", prompt_data.get("translate_prompt", ""))
                
            if hasattr(self, 'proofread_prompt_text'):
                self.proofread_prompt_text.delete("1.0", tk.END)
                self.proofread_prompt_text.insert("1.0", prompt_data.get("proofread_prompt", ""))
            
            # Update current prompts
            self.current_translate_prompt = prompt_data.get("translate_prompt", self.default_translate_prompt)
            self.current_proofread_prompt = prompt_data.get("proofread_prompt", self.default_proofread_prompt)
            
            self.update_log(f"[Prompts] Loaded custom prompt set: '{selected_name}'")
            messagebox.showinfo("Loaded", f"Prompt set '{selected_name}' loaded successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load prompt set: {str(e)}")
            self.update_log(f"[ERROR] Failed to load prompts: {str(e)}")

    def open_custom_prompts_folder(self):
        """Open the custom prompts folder in the system file manager"""
        try:
            custom_prompts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompts")
            
            # Ensure the folder exists
            if not os.path.exists(custom_prompts_path):
                os.makedirs(custom_prompts_path)
            
            # Open folder in system file manager (cross-platform)
            if sys.platform == "win32":
                subprocess.run(["explorer", custom_prompts_path])
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", custom_prompts_path])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", custom_prompts_path])
                
            self.update_log(f"[INFO] Opened folder: {custom_prompts_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {str(e)}")
            self.update_log(f"[ERROR] Failed to open folder: {str(e)}")

    def delete_custom_prompts(self):
        """Delete selected custom prompt set"""
        selection = self.prompts_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a prompt set to delete.")
            return
            
        selected_name = self.prompts_listbox.get(selection[0])
        if selected_name == "[Default System Prompts]":
            messagebox.showwarning("Cannot Delete", "Cannot delete the default system prompts.")
            return
            
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the prompt set '{selected_name}'?\n\nThis action cannot be undone."):
            return
            
        # Determine if this is a private prompt and get the correct path
        if selected_name.startswith("[Private] "):
            # Private prompt - remove prefix and look in private folder
            actual_name = selected_name[10:]  # Remove "[Private] " prefix
            filename = f"{actual_name}.json"
            private_prompts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompts_private")
            filepath = os.path.join(private_prompts_dir, filename)
        else:
            # Public prompt - look in public folder
            filename = f"{selected_name}.json"
            filepath = os.path.join(self.custom_prompts_dir, filename)
        
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self.refresh_prompts_list()
                self.update_log(f"[Prompts] Deleted custom prompt set: '{selected_name}'")
                messagebox.showinfo("Deleted", f"Prompt set '{selected_name}' deleted successfully!")
            else:
                messagebox.showerror("File Not Found", f"Prompt file not found: {filename}")
                self.refresh_prompts_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete prompt set: {str(e)}")
            self.update_log(f"[ERROR] Failed to delete prompts: {str(e)}")

    def refresh_prompts_list(self):
        """Refresh the list of available custom prompts"""
        self.prompts_listbox.delete(0, tk.END)
        
        # Add default option
        self.prompts_listbox.insert(tk.END, "[Default System Prompts]")
        
        # Scan both custom prompts directories
        prompt_files = []
        
        # Scan public custom prompts directory
        if os.path.exists(self.custom_prompts_dir):
            try:
                for filename in sorted(os.listdir(self.custom_prompts_dir)):
                    if filename.endswith('.json'):
                        prompt_name = filename[:-5]  # Remove .json extension
                        prompt_files.append(prompt_name)
            except Exception as e:
                self.update_log(f"[ERROR] Failed to scan custom prompts: {str(e)}")
        
        # Scan private custom prompts directory
        private_prompts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompts_private")
        if os.path.exists(private_prompts_dir):
            try:
                for filename in sorted(os.listdir(private_prompts_dir)):
                    if filename.endswith('.json'):
                        prompt_name = filename[:-5]  # Remove .json extension
                        # Add [Private] prefix to distinguish from public prompts
                        prompt_files.append(f"[Private] {prompt_name}")
            except Exception as e:
                self.update_log(f"[ERROR] Failed to scan private custom prompts: {str(e)}")
        
        # Add all prompts to listbox
        for prompt_name in sorted(prompt_files):
            self.prompts_listbox.insert(tk.END, prompt_name)

    def on_prompt_selection(self, event=None):
        """Handle prompt selection in listbox"""
        selection = self.prompts_listbox.curselection()
        if selection:
            selected_name = self.prompts_listbox.get(selection[0])
            # Update the name field (except for default)
            if selected_name != "[Default System Prompts]":
                # Remove [Private] prefix for display in name field
                if selected_name.startswith("[Private] "):
                    display_name = selected_name[10:]  # Remove "[Private] " prefix
                    self.prompt_private_var.set(True)
                else:
                    display_name = selected_name
                    self.prompt_private_var.set(False)
                self.prompt_name_var.set(display_name)
            else:
                self.prompt_name_var.set("")
                self.prompt_private_var.set(False)

    # ===== PROJECT LIBRARY METHODS =====
    
    def toggle_project_library(self, event=None):
        """Toggle the Project Library section visibility"""
        if self.project_library_visible:
            self.project_library_content.pack_forget()
            self.project_library_frame.config(text="💼 Project Library (Click to expand) ▶")
            self.project_library_visible = False
        else:
            self.project_library_content.pack(fill="both", expand=True, pady=(10,0))
            self.project_library_frame.config(text="💼 Project Library (Click to collapse) ▼")
            self.project_library_visible = True
            self.refresh_projects_list()

    def setup_project_library_content(self):
        """Setup the Project Library content area"""
        # Create projects directory
        self.projects_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects")
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)

        # Project name input and save button
        save_frame = tk.Frame(self.project_library_content, bg="white")
        save_frame.pack(fill="x", padx=5, pady=(5,10))

        tk.Label(save_frame, text="Project Name:", font=("Segoe UI", 9, "bold"), bg="white").pack(anchor="w")
        self.project_name_var = tk.StringVar()
        project_name_entry = tk.Entry(save_frame, textvariable=self.project_name_var, width=30, font=("Segoe UI", 9))
        project_name_entry.pack(fill="x", pady=(2,5))
        
        # Private checkbox for projects
        self.project_private_var = tk.BooleanVar(value=False)
        tk.Checkbutton(save_frame, text="Save to Private Folder", 
                      variable=self.project_private_var, bg="white", 
                      font=("Segoe UI", 9)).pack(anchor="w", pady=(2,5))

        # Save/Load/Delete buttons
        buttons_frame = tk.Frame(save_frame, bg="white")
        buttons_frame.pack(fill="x")
        
        tk.Button(buttons_frame, text="💾 Save Project", 
                 command=self.save_project).pack(side="left", padx=(0,5))
        tk.Button(buttons_frame, text="📁 Load Selected", 
                 command=self.load_project).pack(side="left", padx=(0,5))
        tk.Button(buttons_frame, text="🗑️ Delete Selected", 
                 command=self.delete_project).pack(side="left", padx=(0,5))

        # Available projects management
        management_frame = tk.Frame(self.project_library_content, bg="white")
        management_frame.pack(fill="both", expand=True, padx=5)

        # Available projects list
        tk.Label(management_frame, text="Saved Projects:", 
                font=("Segoe UI", 9, "bold"), bg="white").pack(anchor="w", padx=5, pady=(10,2))
        
        # Show clickable folder location
        projects_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects")
        folder_frame = tk.Frame(management_frame, bg="white")
        folder_frame.pack(anchor="w", padx=5, pady=(0,5))
        
        tk.Label(folder_frame, text="📁 Folder:", 
                font=("Segoe UI", 8), fg="gray", bg="white").pack(side="left")
        
        folder_button = tk.Button(folder_frame, text=projects_path,
                                 font=("Segoe UI", 8), fg="blue", bg="white",
                                 relief="flat", cursor="hand2", bd=0,
                                 command=self.open_projects_folder)
        folder_button.pack(side="left", padx=(3,0))
        
        # Add hover effects for the clickable path
        def on_enter(event):
            folder_button.config(fg="darkblue", font=("Segoe UI", 8, "underline"))
        def on_leave(event):
            folder_button.config(fg="blue", font=("Segoe UI", 8))
            
        folder_button.bind("<Enter>", on_enter)
        folder_button.bind("<Leave>", on_leave)

        list_frame = tk.Frame(management_frame, bg="white")
        list_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))

        # Listbox with scrollbar
        list_scroll_frame = tk.Frame(list_frame, bg="white")
        list_scroll_frame.pack(fill="both", expand=True)

        self.projects_listbox = tk.Listbox(list_scroll_frame, height=6, font=("Segoe UI", 9))
        projects_scrollbar = tk.Scrollbar(list_scroll_frame, orient="vertical", command=self.projects_listbox.yview)
        self.projects_listbox.config(yscrollcommand=projects_scrollbar.set)

        self.projects_listbox.pack(side="left", fill="both", expand=True)
        projects_scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.projects_listbox.bind("<<ListboxSelect>>", self.on_project_selection)

    def save_project(self):
        """Save current project state to JSON file"""
        project_name = self.project_name_var.get().strip()
        if not project_name:
            messagebox.showwarning("No Name", "Please enter a project name.")
            return

        # Collect current state
        project_data = {
            "name": project_name,
            "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "version": APP_VERSION,
            "settings": {
                "source_lang": self.source_lang_var.get(),
                "target_lang": self.target_lang_var.get(),
                "provider": self.provider_var.get(),
                "model": self.model_var.get() if hasattr(self, 'model_var') else "",
                "mode": self.operation_mode_var.get(),
                "chunk_size": self.chunk_size_var.get(),
            },
            "content": {
                "custom_instructions": self.custom_instructions_text.get("1.0", tk.END).strip() if hasattr(self, 'custom_instructions_text') else "",
            },
            "file_paths": {
                "input_file": self.input_file_var.get(),
                "output_file": self.output_file_var.get(),
                "tm_file": self.tm_file_var.get(),
                "drawings_folder": self.drawings_folder_var.get(),
            },
            "prompts": {
                "current_translate": getattr(self, 'current_translate_prompt', ''),
                "current_proofread": getattr(self, 'current_proofread_prompt', ''),
            }
        }

        # Save to file
        filename = f"{project_name}.json"
        
        # Determine which directory to save to
        if self.project_private_var.get():
            # Save to private folder
            save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects_private")
            os.makedirs(save_dir, exist_ok=True)
        else:
            # Save to public folder
            save_dir = self.projects_dir
            
        filepath = os.path.join(save_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            
            self.refresh_projects_list()
            folder_type = "private" if self.project_private_var.get() else "public"
            self.update_log(f"[Project] Saved project to {folder_type} folder: '{project_name}'")
            messagebox.showinfo("Saved", f"Project '{project_name}' saved successfully to {folder_type} folder!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save project: {str(e)}")
            self.update_log(f"[ERROR] Failed to save project: {str(e)}")

    def load_project(self):
        """Load selected project from JSON file"""
        selection = self.projects_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a project to load.")
            return

        selected_name = self.projects_listbox.get(selection[0])
        
        # Determine if this is a private project and get the correct path
        if selected_name.startswith("[Private] "):
            # Private project - remove prefix and look in private folder
            actual_name = selected_name[10:]  # Remove "[Private] " prefix
            filename = f"{actual_name}.json"
            private_projects_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects_private")
            filepath = os.path.join(private_projects_dir, filename)
        else:
            # Public project - look in public folder
            filename = f"{selected_name}.json"
            filepath = os.path.join(self.projects_dir, filename)
        
        if not os.path.exists(filepath):
            messagebox.showerror("File Not Found", f"Project file not found: {filename}")
            self.refresh_projects_list()
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                project_data = json.load(f)

            # Restore settings
            settings = project_data.get("settings", {})
            self.source_lang_var.set(settings.get("source_lang", "Dutch"))
            self.target_lang_var.set(settings.get("target_lang", "English"))
            self.provider_var.set(settings.get("provider", "Claude"))
            if hasattr(self, 'model_var'):
                self.model_var.set(settings.get("model", ""))
            self.operation_mode_var.set(settings.get("mode", "Translate"))
            self.chunk_size_var.set(settings.get("chunk_size", "100"))

            # Restore content
            content = project_data.get("content", {})
            if hasattr(self, 'custom_instructions_text') and content.get("custom_instructions"):
                self.custom_instructions_text.delete("1.0", tk.END)
                self.custom_instructions_text.insert("1.0", content.get("custom_instructions", ""))

            # Restore file paths
            file_paths = project_data.get("file_paths", {})
            self.input_file_var.set(file_paths.get("input_file", ""))
            self.output_file_var.set(file_paths.get("output_file", ""))
            self.tm_file_var.set(file_paths.get("tm_file", ""))
            self.drawings_folder_var.set(file_paths.get("drawings_folder", ""))

            # Restore prompts
            prompts = project_data.get("prompts", {})
            if prompts.get("current_translate"):
                self.current_translate_prompt = prompts["current_translate"]
            if prompts.get("current_proofread"):
                self.current_proofread_prompt = prompts["current_proofread"]

            self.update_log(f"[Project] Loaded project: '{selected_name}'")
            messagebox.showinfo("Loaded", f"Project '{selected_name}' loaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load project: {str(e)}")
            self.update_log(f"[ERROR] Failed to load project: {str(e)}")

    def delete_project(self):
        """Delete selected project"""
        selection = self.projects_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a project to delete.")
            return

        selected_name = self.projects_listbox.get(selection[0])

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the project '{selected_name}'?\n\nThis action cannot be undone."):
            return

        # Determine if this is a private project and get the correct path
        if selected_name.startswith("[Private] "):
            # Private project - remove prefix and look in private folder
            actual_name = selected_name[10:]  # Remove "[Private] " prefix
            filename = f"{actual_name}.json"
            private_projects_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects_private")
            filepath = os.path.join(private_projects_dir, filename)
        else:
            # Public project - look in public folder
            filename = f"{selected_name}.json"
            filepath = os.path.join(self.projects_dir, filename)

        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self.refresh_projects_list()
                self.update_log(f"[Project] Deleted project: '{selected_name}'")
                messagebox.showinfo("Deleted", f"Project '{selected_name}' deleted successfully!")
            else:
                messagebox.showerror("File Not Found", f"Project file not found: {filename}")
                self.refresh_projects_list()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete project: {str(e)}")
            self.update_log(f"[ERROR] Failed to delete project: {str(e)}")

    def refresh_projects_list(self):
        """Refresh the list of available projects"""
        self.projects_listbox.delete(0, tk.END)

        # Scan both projects directories
        project_files = []
        
        # Scan public projects directory
        if os.path.exists(self.projects_dir):
            try:
                for filename in sorted(os.listdir(self.projects_dir)):
                    if filename.endswith('.json'):
                        project_name = filename[:-5]  # Remove .json extension
                        project_files.append(project_name)
            except Exception as e:
                self.update_log(f"[ERROR] Failed to scan projects: {str(e)}")
        
        # Scan private projects directory
        private_projects_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects_private")
        if os.path.exists(private_projects_dir):
            try:
                for filename in sorted(os.listdir(private_projects_dir)):
                    if filename.endswith('.json'):
                        project_name = filename[:-5]  # Remove .json extension
                        # Add [Private] prefix to distinguish from public projects
                        project_files.append(f"[Private] {project_name}")
            except Exception as e:
                self.update_log(f"[ERROR] Failed to scan private projects: {str(e)}")
        
        # Add all projects to listbox
        for project_name in sorted(project_files):
            self.projects_listbox.insert(tk.END, project_name)

    def on_project_selection(self, event=None):
        """Handle project selection in listbox"""
        selection = self.projects_listbox.curselection()
        if selection:
            selected_name = self.projects_listbox.get(selection[0])
            # Remove [Private] prefix for display in name field
            if selected_name.startswith("[Private] "):
                display_name = selected_name[10:]  # Remove "[Private] " prefix
                self.project_private_var.set(True)
            else:
                display_name = selected_name
                self.project_private_var.set(False)
            self.project_name_var.set(display_name)

    def open_projects_folder(self):
        """Open the projects folder in the system file manager"""
        try:
            projects_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects")
            
            # Ensure the folder exists
            if not os.path.exists(projects_path):
                os.makedirs(projects_path)
            
            # Open folder in system file manager (cross-platform)
            if sys.platform == "win32":
                subprocess.run(["explorer", projects_path])
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", projects_path])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", projects_path])
                
            self.update_log(f"[INFO] Opened folder: {projects_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {str(e)}")
            self.update_log(f"[ERROR] Failed to open folder: {str(e)}")

    # ===== CAT EDITOR METHODS (v2.5.0) =====

    def import_docx_file(self):
        """Import DOCX file and extract segments"""
        file_path = filedialog.askopenfilename(
            title="Select DOCX File",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.update_log(f"[CAT] Importing DOCX: {os.path.basename(file_path)}")
            
            # Initialize DOCX handler
            self.docx_handler = DOCXHandler()
            self.current_docx_path = file_path
            self.cat_docx_file_var.set(os.path.basename(file_path))
            
            # Extract all content (paragraphs and tables)
            all_paragraphs = self.docx_handler.import_docx(file_path, extract_formatting=False)
            self.update_log(f"[CAT] Extracted {len(all_paragraphs)} text items from document")
            
            # Segment the content
            segmenter = SimpleSegmenter()
            segments_list = []
            seg_id = 1
            
            # Process all paragraphs (includes table cells from import_docx)
            for para_idx, para_text in enumerate(all_paragraphs):
                if not para_text.strip():
                    continue
                
                # Get paragraph info from docx_handler
                para_info = self.docx_handler.paragraphs_info[para_idx] if para_idx < len(self.docx_handler.paragraphs_info) else None
                
                # Segment the paragraph text
                sentences = segmenter.segment_text(para_text)
                for sentence in sentences:
                    segment = Segment(
                        seg_id=seg_id,
                        source=sentence,
                        paragraph_id=para_idx,
                        style=para_info.style if para_info else "Normal",
                        is_table_cell=para_info.is_table_cell if para_info else False,
                        table_info=(para_info.table_index, para_info.row_index, para_info.cell_index) if para_info and para_info.is_table_cell else None,
                        document_position=seg_id
                    )
                    segments_list.append(segment)
                    seg_id += 1
            
            # Create segment manager
            self.segment_manager = SegmentManager(segments_list)
            
            # Update UI - enable view buttons and update statistics
            self.update_cat_statistics()
            self.enable_view_buttons()
            
            self.update_log(f"[CAT] ✓ Created {len(segments_list)} segments")
            messagebox.showinfo("Success", f"DOCX imported successfully!\n{len(segments_list)} segments created.\n\nYou can now open Grid, Split, or Document view.")
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import DOCX:\n{str(e)}")
            self.update_log(f"[CAT ERROR] Import failed: {str(e)}")

    def update_cat_statistics(self):
        """Update segment statistics display"""
        if not self.segment_manager:
            self.cat_stats_label.config(text="No document loaded", fg="gray")
            return
        
        stats = self.ai_pretranslation_agent.get_translation_statistics(self.segment_manager.segments)
        
        stats_text = (f"📊 {stats['total']} segments | "
                     f"🔴 {stats['untranslated']} untranslated | "
                     f"🟡 {stats['draft']} draft | "
                     f"🟢 {stats['translated']} translated | "
                     f"Progress: {stats['progress_percentage']}%")
        
        self.cat_stats_label.config(text=stats_text, fg="black")

    def ai_pretranslate_segments(self):
        """Use AI to pre-translate all untranslated segments"""
        if not self.segment_manager:
            messagebox.showwarning("No Document", "Please import a DOCX file first.")
            return
        
        untranslated = [seg for seg in self.segment_manager.segments if seg.status == "untranslated"]
        if not untranslated:
            messagebox.showinfo("All Translated", "All segments have been translated!")
            return
        
        # Confirm action
        response = messagebox.askyesno(
            "AI-Assisted Pre-Translation",
            f"Translate {len(untranslated)} untranslated segments using AI?\n\n"
            f"Provider: {self.provider_var.get()}\n"
            f"Languages: {self.source_lang_var.get()} → {self.target_lang_var.get()}\n\n"
            "This may take a few moments..."
        )
        
        if not response:
            return
        
        try:
            self.update_log(f"[CAT] Starting AI-assisted pre-translation ({len(untranslated)} segments)...")
            
            # Get custom instructions
            custom_instructions = self.custom_instructions_text.get("1.0", "end-1c").strip()
            
            # Set up the translation agent
            provider = self.provider_var.get().lower()
            if provider == "gemini":
                agent = self.create_gemini_agent()
            elif provider == "claude":
                agent = self.create_claude_agent()
            elif provider == "openai":
                agent = self.create_openai_agent()
            else:
                raise ValueError(f"Unknown provider: {provider}")
            
            self.ai_pretranslation_agent.set_translation_agent(agent)
            
            # Disable button during translation
            self.cat_pretranslate_btn.config(state="disabled", text="🔄 Translating...")
            self.root.update()
            
            # Translate
            self.ai_pretranslation_agent.pretranslate_untranslated_only(
                self.segment_manager.segments,
                self.source_lang_var.get(),
                self.target_lang_var.get(),
                custom_instructions
            )
            
            # Update UI
            self.update_cat_statistics()
            if self.cat_grid_visible:
                self.refresh_cat_grid()
            
            self.update_log(f"[CAT] ✓ Pre-translation complete!")
            messagebox.showinfo("Success", "AI-assisted pre-translation completed!\n\n"
                                         "Segments are marked as 'draft' - please review and edit as needed.")
            
        except Exception as e:
            messagebox.showerror("Translation Error", f"Failed to translate:\n{str(e)}")
            self.update_log(f"[CAT ERROR] Translation failed: {str(e)}")
        
        finally:
            self.cat_pretranslate_btn.config(state="normal", text="🤖 AI-Assisted Pre-Translation")

    def export_translated_docx(self):
        """Export translated DOCX with formatting preserved"""
        if not self.segment_manager or not self.current_docx_path:
            messagebox.showwarning("No Document", "Please import a DOCX file first.")
            return
        
        # Check if any translations exist
        translated_count = sum(1 for seg in self.segment_manager.segments if seg.target)
        if translated_count == 0:
            response = messagebox.askyesno(
                "No Translations",
                "No segments have been translated yet.\n\nExport anyway with empty translations?"
            )
            if not response:
                return
        
        # Get output file
        default_name = os.path.splitext(os.path.basename(self.current_docx_path))[0] + "_translated.docx"
        output_path = filedialog.asksaveasfilename(
            title="Save Translated DOCX",
            initialfile=default_name,
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        
        if not output_path:
            return
        
        try:
            self.update_log(f"[CAT] Exporting translated DOCX...")
            
            # Build segments list for export
            export_segments = []
            for seg in self.segment_manager.segments:
                export_segments.append({
                    'paragraph_id': seg.paragraph_id,
                    'source': seg.source,
                    'target': seg.target if seg.target else seg.source  # Use source if no translation
                })
            
            # Export to DOCX using docx_handler
            self.docx_handler.export_docx(
                export_segments,
                output_path,
                preserve_formatting=True
            )
            
            self.update_log(f"[CAT] ✓ Exported: {os.path.basename(output_path)}")
            messagebox.showinfo("Success", f"Translated DOCX exported successfully!\n\n{output_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export DOCX:\n{str(e)}")
            self.update_log(f"[CAT ERROR] Export failed: {str(e)}")

    def clear_cat_document(self):
        """Clear the current CAT document"""
        if not self.segment_manager:
            return
        
        response = messagebox.askyesno(
            "Clear Document",
            "Clear the current document and all translations?\n\nThis cannot be undone."
        )
        
        if response:
            self.segment_manager = None
            self.current_docx_path = None
            self.docx_handler = None
            self.cat_docx_file_var.set("")
            self.cat_stats_label.config(text="No document loaded", fg="gray")
            self.cat_pretranslate_btn.config(state="disabled")
            self.cat_export_btn.config(state="disabled")
            
            # Disable view buttons
            self.grid_view_btn.config(state="disabled")
            self.split_view_btn.config(state="disabled")
            self.doc_view_btn.config(state="disabled")
            
            if self.cat_grid_visible:
                self.toggle_cat_grid()
            
            self.update_log("[CAT] Document cleared")

    def toggle_cat_grid(self):
        """Toggle visibility of the segment grid"""
        if not hasattr(self, 'cat_grid_window') or not self.cat_grid_window.winfo_exists():
            self.show_cat_grid()
        else:
            self.cat_grid_window.destroy()
            self.cat_grid_visible = False

    def show_cat_grid(self):
        """Show segment grid in a new window"""
        if not self.segment_manager or not self.segment_manager.segments:
            messagebox.showwarning("No Segments", "Please import a DOCX file first.")
            return
        
        # Create new window
        self.cat_grid_window = tk.Toplevel(self.root)
        self.cat_grid_window.title("CAT Editor - Segment Grid")
        self.cat_grid_window.geometry("1200x600")
        
        # Create frame with scrollbars
        grid_frame = tk.Frame(self.cat_grid_window)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview with scrollbars
        tree_scroll_y = tk.Scrollbar(grid_frame, orient=tk.VERTICAL)
        tree_scroll_x = tk.Scrollbar(grid_frame, orient=tk.HORIZONTAL)
        
        self.cat_segments_tree = ttk.Treeview(grid_frame, 
                                             columns=("ID", "Source", "Target", "Status"),
                                             show="headings",
                                             yscrollcommand=tree_scroll_y.set,
                                             xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.cat_segments_tree.yview)
        tree_scroll_x.config(command=self.cat_segments_tree.xview)
        
        # Configure columns
        self.cat_segments_tree.heading("ID", text="ID")
        self.cat_segments_tree.heading("Source", text="Source Text")
        self.cat_segments_tree.heading("Target", text="Target Text")
        self.cat_segments_tree.heading("Status", text="Status")
        
        self.cat_segments_tree.column("ID", width=50, anchor="center")
        self.cat_segments_tree.column("Source", width=450)
        self.cat_segments_tree.column("Target", width=450)
        self.cat_segments_tree.column("Status", width=100, anchor="center")
        
        # Pack treeview and scrollbars
        self.cat_segments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Populate grid
        self.refresh_cat_grid()
        
        # Bind double-click to edit
        self.cat_segments_tree.bind("<Double-1>", self.edit_cat_segment)
        
        # Update status
        self.cat_grid_visible = True
        self.update_log(f"[CAT] Grid opened with {len(self.segment_manager.segments)} segments")
        
        # Handle window close
        self.cat_grid_window.protocol("WM_DELETE_WINDOW", lambda: self.toggle_cat_grid())

    def refresh_cat_grid(self):
        """Refresh the segment grid display"""
        if not hasattr(self, 'cat_segments_tree') or not self.cat_segments_tree.winfo_exists():
            return
        
        # Clear existing items
        for item in self.cat_segments_tree.get_children():
            self.cat_segments_tree.delete(item)
        
        # Add segments
        for segment in self.segment_manager.segments:
            self.cat_segments_tree.insert("", "end", iid=str(segment.id),
                                         values=(segment.id, 
                                                segment.source,
                                                segment.target if segment.target else "[Not translated]",
                                                segment.status.upper()))
    
    def edit_cat_segment(self, event):
        """Edit a segment when double-clicked"""
        selection = self.cat_segments_tree.selection()
        if not selection:
            return
        
        seg_id = int(selection[0])
        segment = next((s for s in self.segment_manager.segments if s.id == seg_id), None)
        
        if not segment:
            return
        
        # Create edit dialog
        edit_window = tk.Toplevel(self.cat_grid_window)
        edit_window.title(f"Edit Segment {seg_id}")
        edit_window.geometry("700x400")
        
        # Source text (read-only)
        tk.Label(edit_window, text="Source:", font=("bold",)).pack(anchor="w", padx=10, pady=(10,2))
        source_text = tk.Text(edit_window, height=6, wrap=tk.WORD, bg="#f0f0f0", state="disabled")
        source_text.pack(fill=tk.X, padx=10, pady=5)
        source_text.config(state="normal")
        source_text.insert("1.0", segment.source)
        source_text.config(state="disabled")
        
        # Target text (editable)
        tk.Label(edit_window, text="Target:", font=("bold",)).pack(anchor="w", padx=10, pady=(10,2))
        target_text = tk.Text(edit_window, height=6, wrap=tk.WORD)
        target_text.pack(fill=tk.X, padx=10, pady=5)
        target_text.insert("1.0", segment.target if segment.target else "")
        
        # Status dropdown
        status_frame = tk.Frame(edit_window)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(status_frame, text="Status:").pack(side=tk.LEFT, padx=(0,5))
        status_var = tk.StringVar(value=segment.status)
        status_combo = ttk.Combobox(status_frame, textvariable=status_var, 
                                   values=["untranslated", "draft", "translated", "approved"],
                                   state="readonly", width=15)
        status_combo.pack(side=tk.LEFT)
        
        # Save button
        def save_edit():
            segment.target = target_text.get("1.0", "end-1c")
            segment.status = status_var.get()
            segment.modified = True
            self.refresh_cat_grid()
            self.update_cat_statistics()
            edit_window.destroy()
            self.update_log(f"[CAT] Segment {seg_id} updated")
        
        tk.Button(edit_window, text="Save", command=save_edit, width=15).pack(pady=10)
    
    def open_grid_view(self):
        """Open Professional Grid View with filters, color-coding, and editor panel"""
        if not self.segment_manager or not self.segment_manager.segments:
            messagebox.showwarning("No Document", "Please load a TXT or DOCX file first.")
            return
        
        # Create grid view window
        self.grid_window = tk.Toplevel(self.root)
        self.grid_window.title("CAT Editor - Grid View")
        self.grid_window.geometry("1600x900")
        
        # Initialize filter state
        self.grid_filter_active = False
        self.grid_filtered_segments = []
        self.grid_filter_mode = 'filter'  # 'filter' or 'highlight'
        
        # Create main container
        main_container = tk.Frame(self.grid_window)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ===== FILTER PANEL =====
        filter_frame = tk.Frame(main_container, bg='#f0f0f0', relief='ridge', borderwidth=2)
        filter_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        
        # Filter label
        tk.Label(filter_frame, text="🔍 Filter:", bg='#f0f0f0', 
                font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=8, pady=8)
        
        # Filter mode toggle buttons (Filter vs Highlight)
        mode_frame = tk.Frame(filter_frame, bg='#f0f0f0', relief='solid', bd=1)
        mode_frame.pack(side=tk.LEFT, padx=5)
        
        self.grid_filter_mode_btn = tk.Button(mode_frame, text="🚫 Filter",
                                             command=lambda: self.set_grid_filter_mode('filter'),
                                             bg='#4CAF50', fg='white', font=('Segoe UI', 9, 'bold'),
                                             relief='sunken', bd=2, cursor='hand2', width=10)
        self.grid_filter_mode_btn.pack(side=tk.LEFT, padx=1, pady=1)
        
        self.grid_highlight_mode_btn = tk.Button(mode_frame, text="💡 Highlight",
                                                command=lambda: self.set_grid_filter_mode('highlight'),
                                                bg='#e0e0e0', fg='#666', font=('Segoe UI', 9),
                                                relief='raised', bd=2, cursor='hand2', width=10)
        self.grid_highlight_mode_btn.pack(side=tk.LEFT, padx=1, pady=1)
        
        tk.Label(filter_frame, text="│", bg='#f0f0f0', fg='#ccc',
                font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        
        # Source filter
        tk.Label(filter_frame, text="Source:", bg='#f0f0f0', 
                font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(15, 3))
        self.grid_filter_source_var = tk.StringVar()
        source_filter_entry = tk.Entry(filter_frame, textvariable=self.grid_filter_source_var,
                                      font=('Segoe UI', 9), width=25, relief='solid', borderwidth=1)
        source_filter_entry.pack(side=tk.LEFT, padx=3, pady=5)
        source_filter_entry.bind('<Return>', lambda e: self.apply_grid_filters())
        
        # Target filter
        tk.Label(filter_frame, text="Target:", bg='#f0f0f0', 
                font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(15, 3))
        self.grid_filter_target_var = tk.StringVar()
        target_filter_entry = tk.Entry(filter_frame, textvariable=self.grid_filter_target_var,
                                      font=('Segoe UI', 9), width=25, relief='solid', borderwidth=1)
        target_filter_entry.pack(side=tk.LEFT, padx=3, pady=5)
        target_filter_entry.bind('<Return>', lambda e: self.apply_grid_filters())
        
        # Status filter
        tk.Label(filter_frame, text="Status:", bg='#f0f0f0', 
                font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(15, 3))
        self.grid_filter_status_var = tk.StringVar(value="All")
        status_filter_combo = ttk.Combobox(filter_frame, textvariable=self.grid_filter_status_var,
                                          values=["All", "untranslated", "draft", "translated", "approved"],
                                          state='readonly', width=12, font=('Segoe UI', 9))
        status_filter_combo.pack(side=tk.LEFT, padx=3, pady=5)
        status_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_grid_filters())
        
        # Apply/Clear buttons
        tk.Button(filter_frame, text="🔍 Apply", command=self.apply_grid_filters,
                 bg='#2196F3', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief='raised', padx=12, pady=3, cursor='hand2').pack(side=tk.LEFT, padx=8)
        
        tk.Button(filter_frame, text="✕ Clear", command=self.clear_grid_filters,
                 bg='#ff9800', fg='white', font=('Segoe UI', 9),
                 relief='flat', padx=10, pady=3).pack(side=tk.LEFT, padx=3)
        
        # Filter results label
        self.grid_filter_results_label = tk.Label(filter_frame, text="", bg='#f0f0f0',
                                                 font=('Segoe UI', 9), fg='#666')
        self.grid_filter_results_label.pack(side=tk.LEFT, padx=15)
        
        # ===== CANVAS-BASED GRID AREA =====
        grid_frame = tk.LabelFrame(main_container, text="Translation Grid - Canvas View", padx=5, pady=5)
        grid_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Column configuration
        self.grid_columns = {
            'id': {'title': '#', 'width': 50, 'visible': True},
            'type': {'title': 'Type', 'width': 70, 'visible': True},
            'style': {'title': 'Style', 'width': 100, 'visible': True},
            'source': {'title': '📄 Source', 'width': 500, 'visible': True},
            'target': {'title': '🎯 Target', 'width': 500, 'visible': True},
            'status': {'title': 'Status', 'width': 100, 'visible': True}
        }
        
        # Create sticky header row (outside canvas, fixed at top)
        header_frame = tk.Frame(grid_frame, bg='#e0e0e0', relief='raised', bd=1)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Create header labels for each column
        x_offset = 0
        for col_key in ['id', 'type', 'style', 'source', 'target', 'status']:
            col_info = self.grid_columns[col_key]
            if col_info.get('visible', True):
                header_label = tk.Label(header_frame, text=col_info['title'],
                                       bg='#e0e0e0', font=('Segoe UI', 9, 'bold'),
                                       width=col_info['width'] // 8,  # Convert pixels to characters
                                       relief='ridge', bd=1, anchor='center')
                header_label.pack(side=tk.LEFT, padx=0)
        
        # Create scrollable content area
        content_area = tk.Frame(grid_frame, bg='white')
        content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Create canvas for rows
        self.grid_canvas = tk.Canvas(content_area, bg='white', highlightthickness=0)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(content_area, orient='vertical', command=self.grid_canvas.yview)
        h_scroll = ttk.Scrollbar(content_area, orient='horizontal', command=self.grid_canvas.xview)
        self.grid_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Pack canvas and scrollbars
        self.grid_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create inner frame to hold all rows
        self.grid_inner_frame = tk.Frame(self.grid_canvas, bg='white')
        self.canvas_window = self.grid_canvas.create_window((0, 0), window=self.grid_inner_frame, anchor='nw')
        
        # Storage for row data
        self.grid_rows = []  # List of {'segment': seg, 'widgets': {...}, 'row_frame': frame, 'row_index': idx}
        self.grid_current_row_index = -1
        
        # Bind canvas resize to update scroll region
        self.grid_inner_frame.bind('<Configure>', self.update_grid_scroll_region)
        self.grid_canvas.bind('<Configure>', self.on_grid_canvas_resize)
        
        # Keyboard bindings on canvas
        self.grid_canvas.bind('<Up>', self.on_grid_arrow_up)
        self.grid_canvas.bind('<Down>', self.on_grid_arrow_down)
        self.grid_canvas.bind('<F2>', self.on_grid_f2_edit)
        self.grid_canvas.bind('<Return>', self.on_grid_enter)
        self.grid_canvas.bind('<Control-d>', self.on_grid_ctrl_d_copy)
        self.grid_canvas.bind('<Control-D>', self.on_grid_ctrl_d_copy)
        self.grid_canvas.bind('<Escape>', self.on_grid_escape)
        self.grid_canvas.bind('<Control-s>', self.on_grid_ctrl_s_save)
        self.grid_canvas.bind('<Control-S>', self.on_grid_ctrl_s_save)
        
        # Mouse wheel scrolling
        self.grid_canvas.bind('<MouseWheel>', self.on_grid_mousewheel)
        
        # Context menu
        self.create_grid_context_menu()
        
        # Give canvas focus for keyboard navigation
        self.grid_canvas.focus_set()
        
        # ===== EDITOR PANEL =====
        editor_frame = tk.LabelFrame(main_container, text="Segment Editor", padx=10, pady=10)
        editor_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # Segment info and status on same row
        info_frame = tk.Frame(editor_frame)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.grid_seg_info_label = tk.Label(info_frame, text="Select a segment to edit",
                                           font=('Segoe UI', 9, 'bold'))
        self.grid_seg_info_label.pack(side=tk.LEFT)
        
        # Status selector
        status_frame = tk.Frame(info_frame)
        status_frame.pack(side=tk.RIGHT)
        
        tk.Label(status_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 5))
        self.grid_current_status_var = tk.StringVar(value="untranslated")
        grid_status_combo = ttk.Combobox(status_frame, textvariable=self.grid_current_status_var,
                                        values=["untranslated", "draft", "translated", "approved"],
                                        state='readonly', width=12)
        grid_status_combo.pack(side=tk.LEFT)
        grid_status_combo.bind('<<ComboboxSelected>>', self.on_grid_status_change)
        
        # Source (read-only)
        tk.Label(editor_frame, text="Source:", font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.grid_source_text = tk.Text(editor_frame, height=3, wrap='word', bg='#f5f5f5',
                                       state='disabled', font=('Segoe UI', 10))
        self.grid_source_text.pack(fill=tk.X, pady=(2, 10))
        
        # Target (editable) with validation label
        target_header_frame = tk.Frame(editor_frame)
        target_header_frame.pack(fill=tk.X, anchor='w')
        tk.Label(target_header_frame, text="Target:", font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT)
        self.grid_tag_validation_label = tk.Label(target_header_frame, text="", font=('Segoe UI', 8))
        self.grid_tag_validation_label.pack(side=tk.LEFT, padx=(10, 0))
        
        self.grid_target_text = tk.Text(editor_frame, height=3, wrap='word', font=('Segoe UI', 10))
        self.grid_target_text.pack(fill=tk.X, pady=(2, 5))
        self.grid_target_text.bind('<Control-Return>', lambda e: self.save_grid_segment_and_next())
        self.grid_target_text.bind('<KeyRelease>', self.on_grid_target_change)
        # Keyboard shortcuts for tag insertion
        self.grid_target_text.bind('<Control-b>', lambda e: self.insert_grid_tag('b'))
        self.grid_target_text.bind('<Control-i>', lambda e: self.insert_grid_tag('i'))
        self.grid_target_text.bind('<Control-u>', lambda e: self.insert_grid_tag('u'))
        
        # Tag buttons
        tag_button_frame = tk.Frame(editor_frame)
        tag_button_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(tag_button_frame, text="Insert Tags:", font=('Segoe UI', 8)).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(tag_button_frame, text="<b>Bold</b>", command=lambda: self.insert_grid_tag('b'),
                 relief='flat', bg='#ffcccc', font=('Segoe UI', 8, 'bold')).pack(side=tk.LEFT, padx=2)
        tk.Button(tag_button_frame, text="<i>Italic</i>", command=lambda: self.insert_grid_tag('i'),
                 relief='flat', bg='#ccccff', font=('Segoe UI', 8, 'italic')).pack(side=tk.LEFT, padx=2)
        tk.Button(tag_button_frame, text="<u>Underline</u>", command=lambda: self.insert_grid_tag('u'),
                 relief='flat', bg='#ccffcc', font=('Segoe UI', 8, 'underline')).pack(side=tk.LEFT, padx=2)
        tk.Button(tag_button_frame, text="Strip All Tags", command=self.strip_tags_grid,
                 relief='flat', bg='#eeeeee', font=('Segoe UI', 8)).pack(side=tk.LEFT, padx=10)
        tk.Button(tag_button_frame, text="Copy Source Tags", command=self.copy_source_tags_grid,
                 relief='flat', bg='#e6f3ff', font=('Segoe UI', 8)).pack(side=tk.LEFT, padx=2)
        
        # Action buttons
        button_frame = tk.Frame(editor_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Button(button_frame, text="Copy Source → Target", 
                 command=self.copy_source_to_target_grid,
                 font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(button_frame, text="Clear Target", 
                 command=self.clear_target_grid,
                 font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(button_frame, text="💾 Save", 
                 command=self.save_grid_segment,
                 bg='#4CAF50', fg='white', font=('Segoe UI', 9, 'bold')).pack(side=tk.RIGHT, padx=(5, 0))
        tk.Button(button_frame, text="Save & Next (Ctrl+Enter)", 
                 command=self.save_grid_segment_and_next,
                 bg='#2196F3', fg='white', font=('Segoe UI', 9)).pack(side=tk.RIGHT)
        
        # Load all segments
        self.load_segments_to_grid_view()
        
        # Store current selection
        self.grid_current_segment = None
        self.grid_current_item = None
        
        self.update_log(f"[VIEW] Professional Grid View opened with {len(self.segment_manager.segments)} segments")
    
    def update_grid_scroll_region(self, event=None):
        """Update the scroll region of the canvas to fit all rows"""
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox("all"))
    
    def on_grid_canvas_resize(self, event):
        """Handle canvas resize to adjust inner frame width"""
        canvas_width = event.width
        self.grid_canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def on_grid_mousewheel(self, event):
        """Handle mouse wheel scrolling on canvas"""
        self.grid_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def load_segments_to_grid_view(self):
        """Load segments into the canvas-based grid"""
        # Clear existing rows
        for row_data in self.grid_rows:
            row_data['row_frame'].destroy()
        self.grid_rows = []
        self.grid_current_row_index = -1
        
        # Determine which segments to show
        if self.grid_filter_mode == 'filter' and self.grid_filter_active:
            # Filter mode: only show matching segments
            segments_to_show = self.grid_filtered_segments
        else:
            # Highlight mode or no filter: show all segments
            segments_to_show = self.segment_manager.segments
        
        # Add each segment as a row
        for idx, seg in enumerate(segments_to_show):
            self.add_grid_row(seg, idx)
        
        # Update filter label
        if self.grid_filter_active:
            total = len(self.segment_manager.segments)
            shown = len(segments_to_show)
            
            if self.grid_filter_mode == 'filter':
                self.grid_filter_results_label.config(
                    text=f"🚫 Showing {shown} of {total} segments",
                    fg='#4CAF50', font=('Segoe UI', 9, 'bold'))
            else:
                self.grid_filter_results_label.config(
                    text=f"💡 Highlighting {len(self.grid_filtered_segments)} of {total} segments",
                    fg='#FF9800', font=('Segoe UI', 9, 'bold'))
        else:
            self.grid_filter_results_label.config(text="", fg='#666')
        
        # Update scroll region
        self.grid_canvas.update_idletasks()
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox("all"))
        
        self.log_message(f"[GRID] Loaded {len(segments_to_show)} segments into canvas grid")
    
    def add_grid_row(self, segment, row_index):
        """Add a row to the canvas grid"""
        # Determine type label
        if hasattr(segment, 'is_table_cell') and segment.is_table_cell:
            type_text = "Table"
        else:
            type_text = "Para"
        
        # Determine background color based on status
        status_colors = {
            'untranslated': '#ffcccc',  # Light red
            'draft': '#fff9e6',  # Light yellow
            'translated': '#e8f5e9',  # Light green
            'approved': '#c8e6c9'  # Darker green
        }
        bg_color = status_colors.get(segment.status, 'white')
        
        # Check if this segment should be highlighted (in highlight mode)
        if self.grid_filter_mode == 'highlight' and self.grid_filter_active:
            if self.should_highlight_segment(segment):
                bg_color = '#fff59d'  # Bright yellow for highlighted segments
        
        # Create row frame with fixed height (can be made dynamic later)
        row_height = 40  # Minimum height
        row_frame = tk.Frame(self.grid_inner_frame, bg=bg_color, relief='flat', bd=1, height=row_height)
        row_frame.pack(fill='x', side='top', pady=0)
        row_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Create widgets for each column
        widgets = {}
        
        # ID column
        id_label = tk.Label(row_frame, text=str(segment.id), 
                           bg=bg_color, font=('Segoe UI', 9),
                           width=self.grid_columns['id']['width'] // 8,
                           anchor='center')
        id_label.pack(side='left', padx=1)
        widgets['id'] = id_label
        
        # Type column
        type_label = tk.Label(row_frame, text=type_text, 
                             bg=bg_color, font=('Segoe UI', 9),
                             width=self.grid_columns['type']['width'] // 8,
                             anchor='center')
        type_label.pack(side='left', padx=1)
        widgets['type'] = type_label
        
        # Style column
        style_text = segment.style if hasattr(segment, 'style') and segment.style else "Normal"
        style_label = tk.Label(row_frame, text=style_text, 
                              bg=bg_color, font=('Segoe UI', 9),
                              width=self.grid_columns['style']['width'] // 8,
                              anchor='center')
        style_label.pack(side='left', padx=1)
        widgets['style'] = style_label
        
        # Source column (truncated text)
        source_text = self._truncate_text(segment.source, 60)
        source_label = tk.Label(row_frame, text=source_text, 
                               bg=bg_color, font=('Segoe UI', 9),
                               width=self.grid_columns['source']['width'] // 8,
                               anchor='w', justify='left')
        source_label.pack(side='left', padx=2, fill='x', expand=False)
        widgets['source'] = source_label
        
        # Target column (truncated text)
        target_text = self._truncate_text(segment.target if segment.target else "[Not translated]", 60)
        target_label = tk.Label(row_frame, text=target_text, 
                               bg=bg_color, font=('Segoe UI', 9),
                               width=self.grid_columns['target']['width'] // 8,
                               anchor='w', justify='left')
        target_label.pack(side='left', padx=2, fill='x', expand=False)
        widgets['target'] = target_label
        
        # Status column
        status_label = tk.Label(row_frame, text=segment.status.upper(), 
                               bg=bg_color, font=('Segoe UI', 9),
                               width=self.grid_columns['status']['width'] // 8,
                               anchor='center')
        status_label.pack(side='left', padx=1)
        widgets['status'] = status_label
        
        # Bind click to select row
        row_frame.bind('<Button-1>', lambda e, idx=row_index: self.select_grid_row(idx))
        for widget in widgets.values():
            widget.bind('<Button-1>', lambda e, idx=row_index: self.select_grid_row(idx))
        
        # Bind right-click for context menu
        row_frame.bind('<Button-3>', lambda e, idx=row_index: self.show_grid_row_context_menu(e, idx))
        for widget in widgets.values():
            widget.bind('<Button-3>', lambda e, idx=row_index: self.show_grid_row_context_menu(e, idx))
        
        # Store row data
        row_data = {
            'segment': segment,
            'widgets': widgets,
            'row_frame': row_frame,
            'row_index': row_index
        }
        self.grid_rows.append(row_data)
    
    def should_highlight_segment(self, segment):
        """Check if segment matches filter criteria (for highlight mode)"""
        if self.grid_filter_mode == 'filter':
            return True  # In filter mode, all visible segments match
        
        # In highlight mode, check filters
        source_filter = self.grid_filter_source_var.get().lower()
        target_filter = self.grid_filter_target_var.get().lower()
        status_filter = self.grid_filter_status_var.get()
        
        # Check source filter
        if source_filter and source_filter not in segment.source.lower():
            return False
        
        # Check target filter
        if target_filter:
            target_text = segment.target.lower() if segment.target else ""
            if target_filter not in target_text:
                return False
        
        # Check status filter
        if status_filter != "All" and segment.status != status_filter:
            return False
        
        return True
    
    def select_grid_row(self, row_index):
        """Select a row in the canvas grid"""
        if row_index < 0 or row_index >= len(self.grid_rows):
            return
        
        # Deselect previous row
        if self.grid_current_row_index >= 0 and self.grid_current_row_index < len(self.grid_rows):
            old_row = self.grid_rows[self.grid_current_row_index]['row_frame']
            old_row.config(relief='flat', bd=1)
        
        # Select new row
        self.grid_current_row_index = row_index
        row_data = self.grid_rows[row_index]
        row_frame = row_data['row_frame']
        row_frame.config(relief='solid', bd=2)
        
        # Update current segment
        self.grid_current_segment = row_data['segment']
        
        # Load segment into editor panel
        self.load_segment_to_grid_editor(self.grid_current_segment)
        
        # Scroll to ensure row is visible
        self.scroll_to_grid_row(row_index)
        
        # Focus canvas for keyboard navigation
        self.grid_canvas.focus_set()
    
    def scroll_to_grid_row(self, row_index):
        """Scroll canvas to make specified row visible"""
        if row_index < 0 or row_index >= len(self.grid_rows):
            return
        
        row_frame = self.grid_rows[row_index]['row_frame']
        self.grid_canvas.update_idletasks()
        
        # Get canvas viewport height and row position
        canvas_height = self.grid_canvas.winfo_height()
        row_y = row_frame.winfo_y()
        row_height = row_frame.winfo_height()
        
        # Get scroll region
        scroll_region = self.grid_canvas.cget('scrollregion').split()
        if len(scroll_region) == 4:
            total_height = float(scroll_region[3])
            if total_height == 0:
                return
            
            # Get current view
            current_view = self.grid_canvas.yview()
            view_top = current_view[0] * total_height
            view_bottom = current_view[1] * total_height
            
            # Scroll if row is not fully visible
            if row_y < view_top:
                self.grid_canvas.yview_moveto(row_y / total_height)
            elif row_y + row_height > view_bottom:
                self.grid_canvas.yview_moveto((row_y + row_height - canvas_height) / total_height)
    
    def show_grid_row_context_menu(self, event, row_index):
        """Show context menu for a grid row"""
        # Select the row first
        self.select_grid_row(row_index)
        # Show the context menu
        if hasattr(self, 'grid_context_menu'):
            self.grid_context_menu.tk_popup(event.x_root, event.y_root)
    
    def load_segment_to_grid_editor(self, segment):
        """Load a segment into the editor panel"""
        self.grid_seg_info_label.config(
            text=f"Segment #{segment.id} | Paragraph {getattr(segment, 'paragraph_id', '?')}")
        
        # Load source (read-only)
        self.grid_source_text.config(state='normal')
        self.grid_source_text.delete('1.0', 'end')
        self.grid_source_text.insert('1.0', segment.source)
        self.grid_source_text.config(state='disabled')
        
        # Load target (editable)
        self.grid_target_text.delete('1.0', 'end')
        if segment.target:
            self.grid_target_text.insert('1.0', segment.target)
        
        # Load status
        self.grid_current_status_var.set(segment.status)
        
        # Validate tags
        self.validate_grid_tags()
        
        # Focus target field for editing
        self.grid_target_text.focus_set()
    
    def _truncate_text(self, text, max_length):
        """Truncate text for display in grid"""
        if not text:
            return ""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def set_grid_filter_mode(self, mode):
        """Set filter mode: 'filter' (hide non-matching) or 'highlight' (color matching)"""
        self.grid_filter_mode = mode
        
        # Update button styles
        if mode == 'filter':
            # Filter button active (green/sunken)
            self.grid_filter_mode_btn.config(bg='#4CAF50', fg='white', 
                                            font=('Segoe UI', 9, 'bold'),
                                            relief='sunken', bd=2)
            # Highlight button inactive (gray/raised)
            self.grid_highlight_mode_btn.config(bg='#e0e0e0', fg='#666',
                                               font=('Segoe UI', 9),
                                               relief='raised', bd=2)
        else:  # highlight
            # Filter button inactive
            self.grid_filter_mode_btn.config(bg='#e0e0e0', fg='#666',
                                            font=('Segoe UI', 9),
                                            relief='raised', bd=2)
            # Highlight button active (orange/sunken)
            self.grid_highlight_mode_btn.config(bg='#FF9800', fg='white',
                                               font=('Segoe UI', 9, 'bold'),
                                               relief='sunken', bd=2)
        
        # Reapply filters if active
        if self.grid_filter_active:
            self.apply_grid_filters()
        
        self.log_message(f"[GRID] Filter mode set to: {mode.upper()}")
    
    def apply_grid_filters(self):
        """Apply filters to grid view (Filter mode: hide non-matching; Highlight mode: color matching)"""
        source_filter = self.grid_filter_source_var.get().lower()
        target_filter = self.grid_filter_target_var.get().lower()
        status_filter = self.grid_filter_status_var.get()
        
        # If all filters are empty/default, clear filtering
        if not source_filter and not target_filter and status_filter == "All":
            self.clear_grid_filters()
            return
        
        # Find matching segments
        self.grid_filtered_segments = []
        for seg in self.segment_manager.segments:
            # Check source filter
            if source_filter and source_filter not in seg.source.lower():
                continue
            
            # Check target filter
            if target_filter:
                target_text = seg.target.lower() if seg.target else ""
                if target_filter not in target_text:
                    continue
            
            # Check status filter
            if status_filter != "All" and seg.status != status_filter:
                continue
            
            # Segment passed all filters
            self.grid_filtered_segments.append(seg)
        
        # Mark as filtered and reload grid
        self.grid_filter_active = True
        self.load_segments_to_grid_view()
        
        if self.grid_filter_mode == 'filter':
            self.log_message(f"[GRID] Filter applied: {len(self.grid_filtered_segments)} segments match (hiding others)")
        else:
            self.log_message(f"[GRID] Highlight applied: {len(self.grid_filtered_segments)} segments highlighted (showing all)")
    
    def clear_grid_filters(self):
        """Clear all filters and show all segments"""
        self.grid_filter_source_var.set("")
        self.grid_filter_target_var.set("")
        self.grid_filter_status_var.set("All")
        self.grid_filter_active = False
        self.grid_filtered_segments = []
        self.grid_filter_results_label.config(text="", fg='#666')
        self.load_segments_to_grid_view()
        self.log_message("[GRID] Filters cleared")
    
    def on_grid_status_change(self, event):
        """Handle status change in grid editor"""
        if self.grid_current_segment:
            self.grid_current_segment.status = self.grid_current_status_var.get()
            self.grid_current_segment.modified = True
            self.update_grid_row()
    
    def copy_source_to_target_grid(self):
        """Copy source to target in grid editor"""
        if self.grid_current_segment:
            self.grid_target_text.delete('1.0', 'end')
            self.grid_target_text.insert('1.0', self.grid_current_segment.source)
    
    def clear_target_grid(self):
        """Clear target text in grid editor"""
        self.grid_target_text.delete('1.0', 'end')
    
    def save_grid_segment_silently(self):
        """Save current segment without messages"""
        if not self.grid_current_segment:
            return
        
        target = self.grid_target_text.get('1.0', 'end-1c').strip()
        self.grid_current_segment.target = target
        self.grid_current_segment.status = self.grid_current_status_var.get()
        self.grid_current_segment.modified = True
        self.update_grid_row()
    
    def save_grid_segment(self):
        """Save current segment with confirmation"""
        if not self.grid_current_segment:
            return
        
        self.save_grid_segment_silently()
        self.update_log(f"[GRID] Segment #{self.grid_current_segment.id} saved")
    
    def save_grid_segment_and_next(self):
        """Save and move to next segment"""
        if not self.grid_current_segment:
            return
        
        self.save_grid_segment_silently()
        
        # Find next segment
        current_index = None
        children = self.grid_tree.get_children()
        for i, item in enumerate(children):
            if item == self.grid_current_item:
                current_index = i
                break
        
        # Select next if exists
        if current_index is not None and current_index < len(children) - 1:
            next_item = children[current_index + 1]
            self.grid_tree.selection_set(next_item)
            self.grid_tree.see(next_item)
            self.grid_tree.focus(next_item)
            # Trigger selection event
            self.grid_tree.event_generate('<<TreeviewSelect>>')
        
        self.update_log(f"[GRID] Segment #{self.grid_current_segment.id} saved, moving to next")
    
    def update_grid_row(self):
        """Update the current row in the canvas grid after editing"""
        if self.grid_current_row_index < 0 or self.grid_current_row_index >= len(self.grid_rows):
            return
        
        row_data = self.grid_rows[self.grid_current_row_index]
        segment = row_data['segment']
        widgets = row_data['widgets']
        row_frame = row_data['row_frame']
        
        # Update target label
        target_text = self._truncate_text(segment.target if segment.target else "[Not translated]", 60)
        widgets['target'].config(text=target_text)
        
        # Update status label
        widgets['status'].config(text=segment.status.upper())
        
        # Update background color based on status
        status_colors = {
            'untranslated': '#ffcccc',
            'draft': '#fff9e6',
            'translated': '#e8f5e9',
            'approved': '#c8e6c9'
        }
        bg_color = status_colors.get(segment.status, 'white')
        
        # Apply new background to all widgets
        row_frame.config(bg=bg_color)
        for widget in widgets.values():
            widget.config(bg=bg_color)
    
    def on_grid_target_change(self, event):
        """Handle target text changes to validate tags"""
        if self.grid_current_segment:
            self.validate_grid_tags()
    
    def validate_grid_tags(self):
        """Validate HTML tags in grid editor target text"""
        if not self.grid_current_segment:
            return
        
        source = self.grid_current_segment.source
        target = self.grid_target_text.get('1.0', 'end-1c')
        
        # Extract tags from source and target
        source_tags = re.findall(r'<[^>]+>', source)
        target_tags = re.findall(r'<[^>]+>', target)
        
        # Compare
        if source_tags == target_tags:
            self.grid_tag_validation_label.config(text="✓ Tags match", fg='#4CAF50')
        elif not source_tags and not target_tags:
            self.grid_tag_validation_label.config(text="", fg='#666')
        else:
            self.grid_tag_validation_label.config(text="⚠ Tags differ from source", fg='#FF9800')
    
    def insert_grid_tag(self, tag_name):
        """Insert HTML tag pair at cursor position in grid editor"""
        try:
            # Get cursor position
            cursor_pos = self.grid_target_text.index(tk.INSERT)
            
            # Check if there's selected text
            try:
                sel_start = self.grid_target_text.index(tk.SEL_FIRST)
                sel_end = self.grid_target_text.index(tk.SEL_LAST)
                selected_text = self.grid_target_text.get(sel_start, sel_end)
                
                # Wrap selected text
                self.grid_target_text.delete(sel_start, sel_end)
                self.grid_target_text.insert(sel_start, f"<{tag_name}>{selected_text}</{tag_name}>")
            except tk.TclError:
                # No selection - insert tag pair at cursor
                self.grid_target_text.insert(cursor_pos, f"<{tag_name}></{tag_name}>")
                # Move cursor between tags
                new_pos = self.grid_target_text.index(f"{cursor_pos}+{len(tag_name)+2}c")
                self.grid_target_text.mark_set(tk.INSERT, new_pos)
            
            self.validate_grid_tags()
            self.grid_target_text.focus_set()
        except Exception as e:
            self.update_log(f"[GRID] Error inserting tag: {str(e)}")
    
    def strip_tags_grid(self):
        """Remove all HTML tags from grid editor target text"""
        target = self.grid_target_text.get('1.0', 'end-1c')
        cleaned = re.sub(r'<[^>]+>', '', target)
        self.grid_target_text.delete('1.0', 'end')
        self.grid_target_text.insert('1.0', cleaned)
        self.validate_grid_tags()
        self.update_log("[GRID] Tags stripped from target")
    
    def copy_source_tags_grid(self):
        """Copy HTML tags from source to target in grid editor, preserving target text"""
        if not self.grid_current_segment:
            return
        
        source = self.grid_current_segment.source
        target = self.grid_target_text.get('1.0', 'end-1c')
        
        # Extract tags from source
        source_tags = re.findall(r'<[^>]+>', source)
        
        if not source_tags:
            self.update_log("[GRID] No tags found in source")
            return
        
        # Remove existing tags from target
        clean_target = re.sub(r'<[^>]+>', '', target)
        
        # Build result by wrapping clean target with source tags
        # Opening tags go at start, closing tags at end
        opening_tags = [tag for tag in source_tags if not tag.startswith('</')]
        closing_tags = [tag for tag in source_tags if tag.startswith('</')]
        
        result = clean_target
        for tag in opening_tags:
            result = tag + result
        for tag in closing_tags:
            result = result + tag
        
        self.grid_target_text.delete('1.0', 'end')
        self.grid_target_text.insert('1.0', result)
        self.validate_grid_tags()
        self.update_log("[GRID] ✓ Tags copied from source")
    
    def create_grid_context_menu(self):
        """Create context menu for grid view"""
        self.grid_context_menu = tk.Menu(self.grid_window, tearoff=0)
        
        # Editing actions
        self.grid_context_menu.add_command(label="✏️ Edit Segment (F2)", 
                                          command=self.context_edit_segment)
        self.grid_context_menu.add_separator()
        
        # Clipboard actions
        self.grid_context_menu.add_command(label="📋 Copy Source", 
                                          command=self.context_copy_source)
        self.grid_context_menu.add_command(label="📋 Copy Target", 
                                          command=self.context_copy_target)
        self.grid_context_menu.add_separator()
        
        # Quick actions
        self.grid_context_menu.add_command(label="➡️ Copy Source → Target (Ctrl+D)", 
                                          command=self.copy_source_to_target_grid)
        self.grid_context_menu.add_command(label="🗑️ Clear Target", 
                                          command=self.clear_target_grid)
        self.grid_context_menu.add_separator()
        
        # Status submenu
        status_menu = tk.Menu(self.grid_context_menu, tearoff=0)
        status_menu.add_command(label="⭕ Untranslated", 
                               command=lambda: self.context_set_status('untranslated'))
        status_menu.add_command(label="🟡 Draft", 
                               command=lambda: self.context_set_status('draft'))
        status_menu.add_command(label="🟢 Translated", 
                               command=lambda: self.context_set_status('translated'))
        status_menu.add_command(label="✅ Approved", 
                               command=lambda: self.context_set_status('approved'))
        self.grid_context_menu.add_cascade(label="🏷️ Change Status", menu=status_menu)
        
        self.grid_context_menu.add_separator()
        
        # Tag actions
        tag_menu = tk.Menu(self.grid_context_menu, tearoff=0)
        tag_menu.add_command(label="<b> Insert Bold", 
                            command=lambda: self.insert_grid_tag('b'))
        tag_menu.add_command(label="<i> Insert Italic", 
                            command=lambda: self.insert_grid_tag('i'))
        tag_menu.add_command(label="<u> Insert Underline", 
                            command=lambda: self.insert_grid_tag('u'))
        tag_menu.add_separator()
        tag_menu.add_command(label="Strip All Tags", 
                            command=self.strip_tags_grid)
        tag_menu.add_command(label="Copy Source Tags", 
                            command=self.copy_source_tags_grid)
        self.grid_context_menu.add_cascade(label="🏷️ Tags", menu=tag_menu)
    
    def show_grid_context_menu(self, event):
        """Show context menu at cursor position"""
        try:
            # Select the row that was right-clicked
            row_id = self.grid_tree.identify_row(event.y)
            if row_id:
                self.grid_tree.selection_set(row_id)
                self.grid_tree.focus(row_id)
                # Trigger selection event to load segment
                self.grid_tree.event_generate('<<TreeviewSelect>>')
                # Show menu
                self.grid_context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            self.update_log(f"[GRID] Context menu error: {str(e)}")
    
    def context_edit_segment(self):
        """Focus target field for editing (from context menu)"""
        if self.grid_current_segment:
            self.grid_target_text.focus_set()
            self.grid_target_text.mark_set(tk.INSERT, '1.0')
    
    def context_copy_source(self):
        """Copy source text to clipboard"""
        if self.grid_current_segment:
            self.grid_window.clipboard_clear()
            self.grid_window.clipboard_append(self.grid_current_segment.source)
            self.update_log("[GRID] Source copied to clipboard")
    
    def context_copy_target(self):
        """Copy target text to clipboard"""
        if self.grid_current_segment and self.grid_current_segment.target:
            self.grid_window.clipboard_clear()
            self.grid_window.clipboard_append(self.grid_current_segment.target)
            self.update_log("[GRID] Target copied to clipboard")
    
    def context_set_status(self, new_status):
        """Set status of current segment (from context menu)"""
        if self.grid_current_segment:
            self.grid_current_segment.status = new_status
            self.grid_current_segment.modified = True
            self.grid_current_status_var.set(new_status)
            self.update_grid_row(self.grid_current_item)
            self.update_log(f"[GRID] Status changed to: {new_status}")
    
    def on_grid_arrow_up(self, event):
        """Handle Up arrow key - navigate to previous segment"""
        # Save current segment before moving
        if self.grid_current_segment:
            self.save_grid_segment_silently()
        
        # Move to previous row
        if self.grid_current_row_index > 0:
            self.select_grid_row(self.grid_current_row_index - 1)
        
        return "break"  # Prevent default behavior
    
    def on_grid_arrow_down(self, event):
        """Handle Down arrow key - navigate to next segment"""
        # Save current segment before moving
        if self.grid_current_segment:
            self.save_grid_segment_silently()
        
        # Move to next row
        if self.grid_current_row_index < len(self.grid_rows) - 1:
            self.select_grid_row(self.grid_current_row_index + 1)
        
        return "break"  # Prevent default behavior
    
    def on_grid_f2_edit(self, event):
        """Handle F2 key - start editing target field"""
        if self.grid_current_segment:
            self.grid_target_text.focus_set()
            self.grid_target_text.mark_set(tk.INSERT, '1.0')
            self.update_log("[GRID] F2 - Edit mode activated")
        return "break"
    
    def on_grid_ctrl_d_copy(self, event):
        """Handle Ctrl+D - copy source to target"""
        if self.grid_current_segment:
            self.copy_source_to_target_grid()
            self.update_log("[GRID] Ctrl+D - Source copied to target")
        return "break"
    
    def on_grid_escape(self, event):
        """Handle Escape key - cancel editing and return focus to grid"""
        # Reload current segment (discard unsaved changes)
        if self.grid_current_segment and self.grid_current_item:
            self.load_segment_to_grid_editor(self.grid_current_segment, self.grid_current_item)
            self.grid_tree.focus_set()
            self.update_log("[GRID] Escape - Changes discarded")
        return "break"
    
    def on_grid_enter(self, event):
        """Handle Enter key - start editing or save and move to next"""
        # Check if we're in the tree (not in the text editor)
        focused_widget = self.grid_window.focus_get()
        
        if focused_widget == self.grid_tree:
            # In tree - start editing
            if self.grid_current_segment:
                self.grid_target_text.focus_set()
                self.grid_target_text.mark_set(tk.INSERT, '1.0')
        
        return "break"
    
    def on_grid_ctrl_s_save(self, event):
        """Handle Ctrl+S - save current segment"""
        if self.grid_current_segment:
            self.save_grid_segment()
            self.grid_tree.focus_set()  # Return focus to grid
        return "break"
    
    def open_split_view(self):
        """Open Split View (list + editor panel)"""
        if not self.segment_manager or not self.segment_manager.segments:
            messagebox.showwarning("No Document", "Please load a TXT or DOCX file first.")
            return
        
        # Create split view window
        split_window = tk.Toplevel(self.root)
        split_window.title("CAT Editor - Split View")
        split_window.geometry("1400x700")
        
        # Create main paned window (left: list, right: editor)
        main_paned = tk.PanedWindow(split_window, orient=tk.HORIZONTAL, sashwidth=8)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel: Segment list
        left_frame = tk.Frame(main_paned)
        main_paned.add(left_frame, minsize=400, width=500)
        
        tk.Label(left_frame, text="Segments", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        
        # Segment listbox with scrollbar
        list_frame = tk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        segment_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Consolas", 9))
        scrollbar.config(command=segment_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        segment_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Populate listbox
        for seg in self.segment_manager.segments:
            status_icon = {"untranslated": "⭕", "draft": "🟡", "translated": "🟢", "approved": "✅"}.get(seg.status, "⭕")
            segment_listbox.insert(tk.END, f"{seg.id:3d} {status_icon} {seg.source[:70]}...")
        
        # Right panel: Editor
        right_frame = tk.Frame(main_paned)
        main_paned.add(right_frame, minsize=600, width=800)
        
        tk.Label(right_frame, text="Edit Segment", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        
        # Current segment ID
        current_seg_label = tk.Label(right_frame, text="Select a segment from the list", font=("Segoe UI", 10))
        current_seg_label.pack(anchor="w", padx=5, pady=2)
        
        # Source text
        tk.Label(right_frame, text="Source:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=5, pady=(10,2))
        source_text = tk.Text(right_frame, height=8, wrap=tk.WORD, bg="#f0f0f0", font=("Segoe UI", 10))
        source_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Target text
        tk.Label(right_frame, text="Target:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=5, pady=(10,2))
        target_text = tk.Text(right_frame, height=8, wrap=tk.WORD, font=("Segoe UI", 10))
        target_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Status and save
        control_frame = tk.Frame(right_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=10)
        
        tk.Label(control_frame, text="Status:").pack(side=tk.LEFT, padx=(0,5))
        status_var = tk.StringVar(value="untranslated")
        status_combo = ttk.Combobox(control_frame, textvariable=status_var, 
                                   values=["untranslated", "draft", "translated", "approved"],
                                   state="readonly", width=15)
        status_combo.pack(side=tk.LEFT, padx=(0,10))
        
        current_segment = [None]  # Mutable container for current segment
        
        def load_segment(event=None):
            selection = segment_listbox.curselection()
            if not selection:
                return
            
            seg_id = selection[0] + 1  # Listbox is 0-indexed
            segment = next((s for s in self.segment_manager.segments if s.id == seg_id), None)
            
            if segment:
                current_segment[0] = segment
                current_seg_label.config(text=f"Segment {seg_id} of {len(self.segment_manager.segments)}")
                
                source_text.config(state="normal")
                source_text.delete("1.0", tk.END)
                source_text.insert("1.0", segment.source)
                source_text.config(state="disabled")
                
                target_text.delete("1.0", tk.END)
                target_text.insert("1.0", segment.target if segment.target else "")
                
                status_var.set(segment.status)
        
        def save_segment():
            if current_segment[0]:
                seg = current_segment[0]
                seg.target = target_text.get("1.0", "end-1c")
                seg.status = status_var.get()
                seg.modified = True
                
                # Update listbox
                idx = seg.id - 1
                status_icon = {"untranslated": "⭕", "draft": "🟡", "translated": "🟢", "approved": "✅"}.get(seg.status, "⭕")
                segment_listbox.delete(idx)
                segment_listbox.insert(idx, f"{seg.id:3d} {status_icon} {seg.source[:70]}...")
                segment_listbox.selection_set(idx)
                
                self.update_log(f"[SPLIT VIEW] Segment {seg.id} saved")
                
                # Move to next segment
                if idx < len(self.segment_manager.segments) - 1:
                    segment_listbox.selection_clear(0, tk.END)
                    segment_listbox.selection_set(idx + 1)
                    segment_listbox.see(idx + 1)
                    load_segment()
        
        tk.Button(control_frame, text="💾 Save & Next", command=save_segment, width=15).pack(side=tk.LEFT)
        
        # Bind listbox selection
        segment_listbox.bind("<<ListboxSelect>>", load_segment)
        
        # Load first segment
        segment_listbox.selection_set(0)
        load_segment()
        
        self.update_log(f"[VIEW] Split View opened with {len(self.segment_manager.segments)} segments")
    
    def open_document_view(self):
        """Open Document View (document flow with clickable segments)"""
        if not self.segment_manager or not self.segment_manager.segments:
            messagebox.showwarning("No Document", "Please load a TXT or DOCX file first.")
            return
        
        # Create document view window
        doc_window = tk.Toplevel(self.root)
        doc_window.title("CAT Editor - Document View")
        doc_window.geometry("1200x700")
        
        # Create main frame with scrollbar
        main_frame = tk.Frame(doc_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(main_frame, text="Document View", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        tk.Label(main_frame, text="Click any segment to edit it", font=("Segoe UI", 9), fg="gray").pack(anchor="w", padx=5)
        
        # Scrolled text widget
        doc_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=("Segoe UI", 11), padx=10, pady=10)
        doc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure tags for segments
        doc_text.tag_config("segment", background="#e8f4f8", relief="raised", borderwidth=1)
        doc_text.tag_config("translated", background="#d4edda")
        doc_text.tag_config("draft", background="#fff3cd")
        doc_text.tag_config("approved", background="#c3e6cb")
        
        # Insert all segments
        segment_positions = {}  # Track segment positions
        
        for seg in self.segment_manager.segments:
            start_pos = doc_text.index(tk.INSERT)
            
            # Insert source text
            doc_text.insert(tk.END, seg.source)
            
            # If translated, insert target below
            if seg.target:
                doc_text.insert(tk.END, "\n")
                doc_text.insert(tk.END, f"→ {seg.target}")
            
            doc_text.insert(tk.END, "\n\n")
            
            end_pos = doc_text.index(tk.INSERT)
            
            # Tag the segment
            tag_name = f"seg_{seg.id}"
            doc_text.tag_add(tag_name, start_pos, end_pos)
            doc_text.tag_add("segment", start_pos, end_pos)
            
            # Apply status color
            if seg.status != "untranslated":
                doc_text.tag_add(seg.status, start_pos, end_pos)
            
            segment_positions[tag_name] = seg
            
            # Bind click event
            doc_text.tag_bind(tag_name, "<Button-1>", lambda e, s=seg: edit_document_segment(s))
            doc_text.tag_config(tag_name, cursor="hand2")
        
        doc_text.config(state="disabled")
        
        def edit_document_segment(segment):
            """Edit a segment when clicked"""
            # Create edit dialog (reuse from grid view)
            edit_win = tk.Toplevel(doc_window)
            edit_win.title(f"Edit Segment {segment.id}")
            edit_win.geometry("700x400")
            
            tk.Label(edit_win, text="Source:", font=("bold",)).pack(anchor="w", padx=10, pady=(10,2))
            src_txt = tk.Text(edit_win, height=6, wrap=tk.WORD, bg="#f0f0f0", state="disabled")
            src_txt.pack(fill=tk.X, padx=10, pady=5)
            src_txt.config(state="normal")
            src_txt.insert("1.0", segment.source)
            src_txt.config(state="disabled")
            
            tk.Label(edit_win, text="Target:", font=("bold",)).pack(anchor="w", padx=10, pady=(10,2))
            tgt_txt = tk.Text(edit_win, height=6, wrap=tk.WORD)
            tgt_txt.pack(fill=tk.X, padx=10, pady=5)
            tgt_txt.insert("1.0", segment.target if segment.target else "")
            
            status_frm = tk.Frame(edit_win)
            status_frm.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(status_frm, text="Status:").pack(side=tk.LEFT, padx=(0,5))
            stat_var = tk.StringVar(value=segment.status)
            stat_combo = ttk.Combobox(status_frm, textvariable=stat_var, 
                                     values=["untranslated", "draft", "translated", "approved"],
                                     state="readonly", width=15)
            stat_combo.pack(side=tk.LEFT)
            
            def save_doc_edit():
                segment.target = tgt_txt.get("1.0", "end-1c")
                segment.status = stat_var.get()
                segment.modified = True
                
                # Refresh document view
                doc_text.config(state="normal")
                tag_name = f"seg_{segment.id}"
                start, end = doc_text.tag_ranges(tag_name)[0:2]
                doc_text.delete(start, end)
                
                doc_text.mark_set(tk.INSERT, start)
                doc_text.insert(tk.INSERT, segment.source)
                if segment.target:
                    doc_text.insert(tk.INSERT, "\n")
                    doc_text.insert(tk.INSERT, f"→ {segment.target}")
                doc_text.insert(tk.INSERT, "\n\n")
                
                new_end = doc_text.index(tk.INSERT)
                doc_text.tag_add(tag_name, start, new_end)
                doc_text.tag_add("segment", start, new_end)
                if segment.status != "untranslated":
                    doc_text.tag_add(segment.status, start, new_end)
                
                doc_text.config(state="disabled")
                edit_win.destroy()
                self.update_log(f"[DOCUMENT VIEW] Segment {segment.id} updated")
            
            tk.Button(edit_win, text="Save", command=save_doc_edit, width=15).pack(pady=10)
        
        self.update_log(f"[VIEW] Document View opened with {len(self.segment_manager.segments)} segments")

    def create_gemini_agent(self):
        """Create and return a Gemini translation agent"""
        return GeminiTranslationAgent(
            self.api_keys["google"],
            self.log_queue,
            self.model_var.get()
        )

    def create_claude_agent(self):
        """Create and return a Claude translation agent"""
        return ClaudeTranslationAgent(
            self.api_keys["claude"],
            self.log_queue,
            self.model_var.get()
        )

    def create_openai_agent(self):
        """Create and return an OpenAI translation agent"""
        return OpenAITranslationAgent(
            self.api_keys["openai"],
            self.log_queue,
            self.model_var.get()
        )

    def browse_drawings_folder(self):
        if not PIL_AVAILABLE: messagebox.showwarning("Feature Disabled", "Pillow (PIL) library not found."); return
        folderpath = filedialog.askdirectory(title="Select Folder Containing Document Images")
        if folderpath: self.drawings_folder_var.set(folderpath); self.update_log(f"Document images folder: {folderpath}")
    
    def browse_tm_file(self):
        filepath = filedialog.askopenfilename(title="Select TM File", filetypes=(("TMX", "*.tmx"),("TXT", "*.txt"),("All", "*.*")))
        if filepath: self.tm_file_var.set(filepath); self.update_log(f"TM file: {filepath}")
    
    # NEW: Tracked Changes Methods
    def load_tracked_changes(self):
        """Load tracked changes from DOCX or TSV files"""
        filetypes = [
            ("Word & TSV files", "*.docx;*.tsv"),
            ("Word documents", "*.docx"),
            ("TSV files", "*.tsv"),
            ("All files", "*.*")
        ]
        
        filepaths = filedialog.askopenfilenames(
            title="Select DOCX or TSV files with tracked changes",
            filetypes=filetypes
        )
        
        if not filepaths:
            return
        
        success_count = 0
        for filepath in filepaths:
            _, ext = os.path.splitext(filepath.lower())
            
            if ext == '.docx':
                if self.tracked_changes_agent.load_docx_changes(filepath):
                    success_count += 1
            elif ext == '.tsv':
                if self.tracked_changes_agent.load_tsv_changes(filepath):
                    success_count += 1
            else:
                self.update_log(f"[Tracked Changes] Skipping unsupported file type: {filepath}")
        
        # Update status label
        total_pairs = len(self.tracked_changes_agent.change_data)
        files_loaded = len(self.tracked_changes_agent.files_loaded)
        
        if total_pairs > 0:
            self.tracked_changes_status_label.config(
                text=f"{total_pairs} change pairs from {files_loaded} file(s)",
                fg="green"
            )
        else:
            self.tracked_changes_status_label.config(text="No tracked changes loaded", fg="gray")
        
        if success_count > 0:
            self.update_log(f"Tracked changes loaded: {success_count} files, {total_pairs} total pairs")
    
    def browse_tracked_changes(self):
        """Open the tracked changes browser"""
        if not hasattr(self, 'tracked_changes_browser') or self.tracked_changes_browser is None:
            self.tracked_changes_browser = TrackedChangesBrowser(self.root, self.tracked_changes_agent)

        
        self.tracked_changes_browser.show_browser()
    
    def clear_tracked_changes(self):
        """Clear all loaded tracked changes"""
        self.tracked_changes_agent.clear_changes()
        self.tracked_changes_status_label.config(text="No tracked changes loaded", fg="gray")
        
        # Close browser window if open
        if (hasattr(self, 'tracked_changes_browser') and 
            self.tracked_changes_browser is not None and 
            self.tracked_changes_browser.window is not None and 
            self.tracked_changes_browser.window.winfo_exists()):
            self.tracked_changes_browser.window.destroy()
    
    def browse_input_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filepath: 
            self.input_file_var.set(filepath)
            if not self.output_file_var.get(): 
                base, ext = os.path.splitext(filepath)
                suffix = "_proofread" if self.operation_mode_var.get() == "Proofread" else "_translated"
                self.output_file_var.set(f"{base}{suffix}{ext}")
    
    def browse_and_load_txt(self):
        """Browse for TXT file and load it into segment manager"""
        filepath = filedialog.askopenfilename(
            title="Select TXT File to Load",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if not filepath:
            return
        
        try:
            self.input_file_var.set(filepath)
            
            # Set output file if not set
            if not self.output_file_var.get(): 
                base, ext = os.path.splitext(filepath)
                self.output_file_var.set(f"{base}_translated{ext}")
            
            # Load file and create segments
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            # Create segments from lines
            from modules.segment_manager import Segment
            segments_list = []
            for idx, line in enumerate(lines, 1):
                segment = Segment(
                    seg_id=idx,
                    source=line,
                    paragraph_id=idx-1,
                    document_position=idx
                )
                segments_list.append(segment)
            
            # Create segment manager
            from modules.segment_manager import SegmentManager
            self.segment_manager = SegmentManager(segments_list)
            self.current_docx_path = None  # TXT mode, not DOCX
            
            # Enable view buttons
            self.enable_view_buttons()
            
            # Update status
            self.update_log(f"[TXT] ✓ Loaded {len(segments_list)} segments from TXT file")
            messagebox.showinfo("Success", f"TXT file loaded successfully!\n{len(segments_list)} segments created.")
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load TXT file:\n{str(e)}")
            self.update_log(f"[TXT ERROR] Load failed: {str(e)}")
    
    def enable_view_buttons(self):
        """Enable all view buttons after loading a file"""
        self.grid_view_btn.config(state="normal")
        self.split_view_btn.config(state="normal")
        self.document_view_btn.config(state="normal")
        self.cat_pretranslate_btn.config(state="normal")
        self.cat_export_btn.config(state="normal")

    def browse_output_file(self):
        filepath = filedialog.asksaveasfilename(title="Save Output Files As (TXT + TMX will be generated)", filetypes=(("Text files", "*.txt"),("All files", "*.*")), defaultextension=".txt")
        if filepath: self.output_file_var.set(filepath)
    
    def update_log(self, msg): 
        self.log_text.config(state="normal"); self.log_text.insert(tk.END, str(msg) + "\n"); self.log_text.see(tk.END); self.log_text.config(state="disabled"); self.root.update_idletasks()
    
    def check_log_queue(self): 
        while not self.log_queue.empty(): self.update_log(self.log_queue.get_nowait())
        self.root.after(100, self.check_log_queue)
    
    def list_available_models(self):
        provider = self.provider_var.get()
        if not provider:
            messagebox.showerror("Error", "No provider selected")
            return
            
        self.update_log(f"\n--- Listing Models for {provider} ---")
        
        # Get appropriate API key
        api_key = ""
        if provider == "Claude":
            api_key = self.api_keys["claude"]
        elif provider == "Gemini":
            api_key = self.api_keys["google"]
        elif provider == "OpenAI":
            api_key = self.api_keys["openai"]
        
        if not api_key:
            self.update_log(f"API Key missing for {provider}")
            return
            
        if provider == "Gemini" and GOOGLE_AI_AVAILABLE:
            try:
                genai.configure(api_key=api_key)
                self.update_log("Fetching Gemini models...")
                models_info = []
                for m in genai.list_models():
                    model_desc_text = m.description if hasattr(m, 'description') and m.description else "N/A"
                    models_info.append(f"Model: {m.name}\n  Display: {m.display_name}\n  Desc: {model_desc_text[:100]}...\n  Methods: {m.supported_generation_methods}\n  {'✅ genContent' if 'generateContent' in m.supported_generation_methods else '❌ No genContent'}")
                if not models_info: self.update_log("No Gemini models found.")
                else: self.update_log("\n---\n".join(models_info)); self.update_log(f"\nFound {len(models_info)} Gemini models. For drawings, use multimodal.")
            except Exception as e: self.update_log(f"Error listing Gemini models: {e}"); messagebox.showerror("List Models Error", f"{e}")
        elif provider == "Claude":
            self.update_log("Available Claude models:")
            for i, model in enumerate(CLAUDE_MODELS, 1):
                self.update_log(f"{i}. {model}")
            self.update_log(f"\nFound {len(CLAUDE_MODELS)} Claude models. All support multimodal capabilities.")
        elif provider == "OpenAI":
            self.update_log("Available OpenAI models:")
            for i, model in enumerate(OPENAI_MODELS, 1):
                self.update_log(f"{i}. {model}")
            self.update_log(f"\nFound {len(OPENAI_MODELS)} OpenAI models. Models with 'gpt-4' prefix support multimodal capabilities.")
        else:
            self.update_log(f"Cannot list models for {provider} - library not available or API key missing")
            
        self.update_log("--- Done Listing ---\n")
    
    def load_drawing_images_from_folder(self, folder_path):
        if not PIL_AVAILABLE or not folder_path: self.log_queue.put("[Drawings] Pillow lib not avail or no folder path."); return {}
        loaded_images_map = {}; self.log_queue.put(f"[Drawings] Loading images from: {folder_path}")
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp'); count = 0
        try:
            for fname in os.listdir(folder_path):
                if fname.lower().endswith(valid_extensions):
                    try:
                        base_name = os.path.splitext(fname)[0]; normalized_ref = normalize_figure_ref(base_name)
                        if normalized_ref: img = Image.open(os.path.join(folder_path, fname)); loaded_images_map[normalized_ref] = img; self.log_queue.put(f"[Drawings] Loaded '{fname}' as Fig Ref '{normalized_ref}'."); count += 1
                        else: self.log_queue.put(f"[Drawings] Could not normalize: {fname}")
                    except Exception as e_img: self.log_queue.put(f"[Drawings] Err loading img {fname}: {e_img}")
            self.log_queue.put(f"[Drawings] Loaded {count} images."); 
        except Exception as e_list_dir: self.log_queue.put(f"[Drawings] Error listing dir {folder_path}: {e_list_dir}"); messagebox.showerror("Drawings Folder Error", f"Could not read drawings folder: {e_list_dir}")
        return loaded_images_map

    def start_processing_thread(self):
        provider = self.provider_var.get()
        model_name = self.model_var.get()
        mode = self.operation_mode_var.get()
        
        # Validate provider and model
        if not provider or not model_name:
            messagebox.showerror("Error", "Please select both AI provider and model")
            return
            
        # Check if provider is working
        working_providers = self.get_working_providers()
        if provider not in working_providers:
            api_key_type = "OpenAI" if provider == "OpenAI" else "Claude" if provider == "Claude" else "Google"
            messagebox.showerror("Error", f"{provider} not available. Check if {api_key_type} API key is configured in api_keys.txt and library is installed.")
            return
        
        input_f = self.input_file_var.get(); output_f = self.output_file_var.get()
        tm_f = self.tm_file_var.get(); drawings_folder = self.drawings_folder_var.get()
        src_l = self.source_lang_var.get(); tgt_l = self.target_lang_var.get()
        custom_instr = self.custom_instructions_text.get("1.0", tk.END).strip()
        
        # Get custom system prompt for the current mode
        custom_system_prompt = self.get_custom_system_prompt(mode)
        
        try: chunk_s = int(self.chunk_size_var.get()); assert chunk_s > 0
        except: messagebox.showerror("Error", "Invalid Chunk Size."); return
        
        if not input_f or not output_f: messagebox.showerror("File Error", "Select input & output files."); return
        if drawings_folder and not PIL_AVAILABLE: messagebox.showerror("Image Error", "Pillow (PIL) library needed for drawings folder feature."); return

        self.process_button.config(state="disabled", text=f"{mode}ing...")
        self.list_models_button.config(state="disabled")
        self.refresh_models_button.config(state="disabled")
        self.update_log(f"--- Starting {mode} Process with {provider} ({model_name}) ---")
        
        if mode == "Translate" and tm_f: self.tm_agent.load_tm(tm_f, src_l, tgt_l)
        self.drawings_images_map = {} 
        if drawings_folder and PIL_AVAILABLE: self.drawings_images_map = self.load_drawing_images_from_folder(drawings_folder)
        
        thread = threading.Thread(target=self.run_pipeline,
                                  args=(mode, input_f, output_f, src_l, tgt_l, provider, model_name, chunk_s, 
                                        self.drawings_images_map, custom_instr, custom_system_prompt, tm_f)) 
        thread.daemon = True; thread.start()

    def generate_session_report(self, mode, input_f, output_f, source_lang, target_lang, provider, model_name, 
                               chunk_s, drawings_map, user_custom_instructions, custom_system_prompt, 
                               tm_file=None, tracked_changes_data=None):
        """Generate comprehensive markdown report of session settings and AI prompts"""
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine default vs custom prompts
        if mode == "Translate":
            default_prompt = self.default_translate_prompt
            current_prompt = self.current_translate_prompt if hasattr(self, 'current_translate_prompt') else default_prompt
        else:  # Proofread
            default_prompt = self.default_proofread_prompt  
            current_prompt = self.current_proofread_prompt if hasattr(self, 'current_proofread_prompt') else default_prompt
        
        is_custom_prompt = current_prompt != default_prompt
        custom_prompt_source = "Custom loaded prompt" if is_custom_prompt else "Default system prompt"
        
        # Get active custom prompt name if available
        active_prompt_name = "Default System Prompts"
        if hasattr(self, 'prompts_listbox'):
            try:
                selection = self.prompts_listbox.curselection()
                if selection:
                    active_prompt_name = self.prompts_listbox.get(selection[0])
            except:
                pass
        
        # Build comprehensive markdown report
        report = f"""# Supervertaler Session Report

## Session Information
- **Date & Time**: {timestamp}
- **Supervertaler Version**: {APP_VERSION}
- **Operation Mode**: {mode}
- **AI Provider**: {provider}
- **AI Model**: {model_name}

## File Settings
- **Input File**: `{input_f}`
- **Output Files**: 
  - **TXT**: `{output_f}` (tab-separated source/target)
  - **TMX**: `{output_f.replace('.txt', '.tmx') if output_f.endswith('.txt') else output_f + '.tmx'}` (translation memory)
  - **Report**: `{output_f.replace('.txt', '_report.md') if output_f.endswith('.txt') else output_f + '_report.md'}` (session details)
- **Source Language**: {source_lang}
- **Target Language**: {target_lang}
- **Chunk Size**: {chunk_s} segments per batch

## Optional Resources
- **Translation Memory File**: {"None" if not tm_file else f"`{tm_file}`"}
- **Drawings/Images Folder**: {"None" if not drawings_map else f"✅ {len(drawings_map)} images loaded"}
- **Tracked Changes Data**: {"None" if not tracked_changes_data or tracked_changes_data == "No tracked changes found." else "✅ Tracked changes detected"}

## AI Prompt Configuration

### Active Prompt Set
- **Source**: {custom_prompt_source}
- **Prompt Name**: {active_prompt_name}

### System Prompt Sent to AI
```
{custom_system_prompt if custom_system_prompt else current_prompt}
```

### Custom Instructions
"""
        
        if user_custom_instructions and user_custom_instructions.strip():
            report += f"""```
{user_custom_instructions}
```
"""
        else:
            report += "None provided\n"
        
        # Add application state information
        report += f"""
## Application Settings

### UI State
- **Provider Selection**: {provider}
- **Model Selection**: {model_name}  
- **Processing Mode**: {mode}
- **Language Pair**: {source_lang} → {target_lang}

### Library Availability
- **Google AI (Gemini)**: {"✅ Available" if GOOGLE_AI_AVAILABLE else "❌ Not Available"}
- **Anthropic (Claude)**: {"✅ Available" if CLAUDE_AVAILABLE else "❌ Not Available"}  
- **OpenAI**: {"✅ Available" if OPENAI_AVAILABLE else "❌ Not Available"}
- **PIL (Image Processing)**: {"✅ Available" if PIL_AVAILABLE else "❌ Not Available"}

### API Key Status
- **Google/Gemini**: {"✅ Configured" if self.api_keys.get("google") else "❌ Not Configured"}
- **Claude**: {"✅ Configured" if self.api_keys.get("claude") else "❌ Not Configured"}
- **OpenAI**: {"✅ Configured" if self.api_keys.get("openai") else "❌ Not Configured"}

## Processing Details

### Prompt Template Variables
- **{{source_lang}}**: {source_lang}
- **{{target_lang}}**: {target_lang}

### Additional Context Provided to AI
"""
        
        context_items = []
        if tm_file:
            context_items.append("- Translation Memory entries")
        if drawings_map:
            context_items.append(f"- {len(drawings_map)} patent drawings/images")  
        if tracked_changes_data and tracked_changes_data != "No tracked changes found.":
            context_items.append("- Document tracked changes")
        if user_custom_instructions and user_custom_instructions.strip():
            context_items.append("- User custom instructions")
            
        if context_items:
            report += "\n".join(context_items) + "\n"
        else:
            report += "None\n"
            
        report += f"""
## Technical Information
- **Processing Method**: Chunked processing ({chunk_s} segments per API call)
- **Output Formats**: TXT (tab-separated) + TMX (translation memory)
- **Report Generated**: {timestamp}

---
*This report was automatically generated by Supervertaler v{APP_VERSION}*
"""
        
        return report

    def run_pipeline(self, mode, input_f, output_f, source_lang, target_lang, provider, model_name, chunk_s, drawings_map, user_custom_instructions, custom_system_prompt=None, tm_file=None):
        ingestor = BilingualFileIngestionAgent(); output_gen = OutputGenerationAgent()
        
        all_original_data = ingestor.process(input_f, self.log_queue, mode=mode) 
        if not all_original_data: self.log_queue.put("No data from input file."); messagebox.showerror("Input Err", "No data in input file."); self.root.after(0, self.enable_buttons); return

        source_segments_original = []
        original_target_segments = [] 
        original_comments = []    
        modified_lines_count = 0

        # Get appropriate API key
        api_key = ""
        if provider == "Claude":
            api_key = self.api_keys["claude"]
        elif provider == "Gemini":
            api_key = self.api_keys["google"]
        elif provider == "OpenAI":
            api_key = self.api_keys["openai"]
        
        if not api_key:
            self.log_queue.put(f"No API key available for {provider}")
            messagebox.showerror("API Key Error", f"No API key configured for {provider}")
            self.root.after(0, self.enable_buttons)
            return

        if mode == "Translate":
            source_segments_original = all_original_data
            translator = create_translation_agent(provider, api_key, self.log_queue, model_name)
            if not translator or not translator.model: self.log_queue.put("Translator init fail."); messagebox.showerror("Model Err", "Translator model init failed."); self.root.after(0, self.enable_buttons); return
        elif mode == "Proofread":
            proofreader = create_proofreading_agent(provider, api_key, self.log_queue, model_name)
            if not proofreader or not proofreader.model: self.log_queue.put("Proofreader init fail."); messagebox.showerror("Model Err", "Proofreader model init failed."); self.root.after(0, self.enable_buttons); return
            for item in all_original_data:
                source_segments_original.append(item["source"])
                original_target_segments.append(item["target"])
                original_comments.append(item["comment"]) 

        final_output_targets_or_proofread_results = [None] * len(source_segments_original)
        tm_hits = 0; llm_processed_map = {}

        if mode == "Translate":
            if self.tm_agent.tm_data:
                self.log_queue.put(f"[TM] Applying {len(self.tm_agent.tm_data)} TM entries...")
                for i, seg in enumerate(source_segments_original):
                    tm_tgt = self.tm_agent.get_translation(seg)
                    if tm_tgt is not None: final_output_targets_or_proofread_results[i] = tm_tgt; tm_hits += 1
                self.log_queue.put(f"[TM] Applied TM to {tm_hits} segments.")
            else: self.log_queue.put("[TM] No TM data or file not specified.")
        
        full_source_doc_str = "\n".join([f"{i+1}. {line}" for i, line in enumerate(source_segments_original)])
        full_original_target_doc_str = "\n".join([f"{i+1}. {line}" for i, line in enumerate(original_target_segments)]) if mode == "Proofread" else ""
        
        lines_needing_llm_count = len(source_segments_original) - (tm_hits if mode == "Translate" else 0)

        if lines_needing_llm_count > 0:
            llm_indices = [i for i, processed_item in enumerate(final_output_targets_or_proofread_results) if processed_item is None]
            num_llm_chunks = math.ceil(lines_needing_llm_count / chunk_s)
            self.log_queue.put(f"LLM Segments for {mode}: {lines_needing_llm_count}. LLM Chunks: {num_llm_chunks if num_llm_chunks > 0 else '0'}")
            
            for i in range(num_llm_chunks):
                current_orig_doc_indices = llm_indices[i * chunk_s : min((i + 1) * chunk_s, lines_needing_llm_count)] 
                if not current_orig_doc_indices: continue
                self.log_queue.put(f"LLM Chunk {i+1}/{num_llm_chunks} ({mode}): Sending {len(current_orig_doc_indices)} segments...")
                
                if mode == "Translate":
                    lines_map_for_llm = {orig_idx + 1: f"{orig_idx + 1}. {source_segments_original[orig_idx]}" for orig_idx in current_orig_doc_indices}
                    chunk_results = translator.translate_specific_lines_with_drawings_context(
                        lines_map_for_llm, full_source_doc_str, source_lang, target_lang,
                        source_segments_original, drawings_map, user_custom_instructions,
                        tracked_changes_data=self.tracked_changes_agent, custom_system_prompt=custom_system_prompt)
                elif mode == "Proofread":
                    lines_map_for_llm = {orig_idx + 1: {"source": source_segments_original[orig_idx], "target_original": original_target_segments[orig_idx]} for orig_idx in current_orig_doc_indices}
                    
                    # OpenAI agent has different method signature
                    if isinstance(proofreader, OpenAIProofreadingAgent):
                        # Convert lines_map to the format expected by OpenAI agent
                        lines_data = [{"line_num": line_num, "source": data["source"], "target": data["target_original"]} 
                                     for line_num, data in lines_map_for_llm.items()]
                        openai_results = proofreader.proofread_specific_lines_with_context(
                            lines_data, full_source_doc_str, source_lang, target_lang,
                            user_custom_instructions, self.tracked_changes_agent, custom_system_prompt)
                        
                        # Convert OpenAI list format to dictionary format expected by the pipeline
                        chunk_results = {}
                        for result in openai_results:
                            line_num = result.get("line_num")
                            if line_num:
                                chunk_results[line_num] = {
                                    "revised_target": result.get("revised_target", result.get("original_target", "")),
                                    "changes_summary": result.get("changes_summary", "")
                                }
                    else:
                        # Gemini/Claude agents use the full parameter set
                        chunk_results = proofreader.proofread_specific_lines_with_context(
                            lines_map_for_llm, full_source_doc_str, full_original_target_doc_str,
                            source_lang, target_lang, source_segments_original, drawings_map,
                            user_custom_instructions, self.tracked_changes_agent, 
                            custom_system_prompt)
                
                llm_processed_map.update(chunk_results)
                self.log_queue.put(f"Finished LLM Chunk {i+1}/{num_llm_chunks} for {mode}.")
        else: self.log_queue.put(f"No segments require LLM {mode} after TM (if applicable).")

        output_source_list = []
        output_target_list = []
        output_comment_list = [] 

        for i in range(len(source_segments_original)):
            source_text = source_segments_original[i]
            output_source_list.append(source_text)
            if mode == "Translate":
                target_text = final_output_targets_or_proofread_results[i] if final_output_targets_or_proofread_results[i] is not None else llm_processed_map.get(i + 1)
                output_target_list.append(target_text if target_text is not None else "[ERR - No TL]")
            elif mode == "Proofread":
                proofread_entry = llm_processed_map.get(i + 1) 
                original_target_text = original_target_segments[i]
                
                if proofread_entry:
                    revised_target = proofread_entry.get("revised_target", original_target_text)
                    ai_summary = proofread_entry.get("changes_summary")
                else: 
                    revised_target = original_target_text
                    ai_summary = "[Segment not processed by AI Proofreader]"
                
                output_target_list.append(revised_target)
                existing_comment = original_comments[i]
                comment_parts = []
                if existing_comment: comment_parts.append(f"ORIGINAL COMMENT: {existing_comment}")
                if revised_target.strip() != original_target_segments[i].strip(): 
                    if ai_summary and "No changes made" not in ai_summary:
                        comment_parts.append(f"PROOFREADER COMMENT (AI): {ai_summary}")
                    else: 
                        comment_parts.append(f"PROOFREADER COMMENT (AI): Segment was modified by AI.")
                        modified_lines_count +=1
                elif ai_summary and "No changes made" not in ai_summary: 
                     comment_parts.append(f"PROOFREADER COMMENT (AI): {ai_summary} (Note: Text appears identical to original despite summary.)")
                output_comment_list.append(" | ".join(comment_parts).strip() if comment_parts else None)
        
        had_errors = any(t is None or "[Err" in str(t) or "[Missing" in str(t) or "[SYS ERR" in str(t) for t in output_target_list)
        file_ok = output_gen.process(
            output_source_list,
            output_target_list,
            output_f,
            self.log_queue,
            mode=mode,
            comments_list_for_output=output_comment_list if mode == "Proofread" else None,
            source_lang=source_lang,
            target_lang=target_lang  # FIX: use correct parameter name
        )

        # Generate session report if processing was successful
        if file_ok:
            try:
                # Create report filename by replacing output extension with '_report.md'
                base_name = os.path.splitext(output_f)[0]
                report_filename = f"{base_name}_report.md"
                
                # Generate the comprehensive session report
                report_content = self.generate_session_report(
                    mode=mode,
                    input_f=input_f,
                    output_f=output_f,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    provider=provider,
                    model_name=model_name,
                    chunk_s=chunk_s,
                    drawings_map=drawings_map,
                    user_custom_instructions=user_custom_instructions,
                    custom_system_prompt=custom_system_prompt,
                    tm_file=tm_file,
                    tracked_changes_data=getattr(self.tracked_changes_agent, 'change_data', None)
                )
                
                # Write the report to file
                with open(report_filename, 'w', encoding='utf-8') as report_file:
                    report_file.write(report_content)
                
                self.log_queue.put(f"Session report saved: {report_filename}")
                
            except Exception as e:
                # Don't let report generation errors disrupt the main workflow
                self.log_queue.put(f"Warning: Could not generate session report: {str(e)}")

        msg_title = "Success" if file_ok and not had_errors else "Partial Success" if file_ok else "Error"
        msg_detail_key = "SUCCESS" if file_ok and not had_errors else "PARTIAL" if file_ok else "FAIL"

        base_log_message_suffix = f"Output: {output_f}"
        if msg_detail_key == "PARTIAL":
            base_log_message_suffix += ". Check logs."
        elif msg_detail_key == "FAIL":
            base_log_message_suffix = "Check logs."

        final_log_message = f"\n--- {mode.upper()} {msg_detail_key}! "
        if mode == "Translate":
            final_log_message += f"TM Hits: {tm_hits}. LLM Segs processed: {len(llm_processed_map)}. "
        else:
            final_log_message += f"LLM Segs processed: {len(llm_processed_map)}. Lines Modified by AI: {modified_lines_count}. "
        if self.tracked_changes_agent.change_data:
            final_log_message += f"Tracked Changes: {len(self.tracked_changes_agent.change_data)} pairs used as context. "
        final_log_message += base_log_message_suffix + " ---"
        self.log_queue.put(final_log_message)

        messagebox_func = (
            messagebox.showinfo if msg_title == "Success"
            else messagebox.showwarning if msg_title == "Partial Success"
            else messagebox.showerror
        )
        messagebox_func(
            msg_title,
            f"{mode} {msg_detail_key.lower()}! Output: {output_f if file_ok else 'not saved'}\nSee logs for details."
        )
        self.root.after(0, self.enable_buttons)

    # NEW: re-enable buttons after processing
    def enable_buttons(self):
        try:
            mode = self.operation_mode_var.get()
            self.process_button.config(state="normal", text=("Translate" if mode == "Translate" else "Proofread"))
            self.list_models_button.config(state="normal")
            self.refresh_models_button.config(state="normal")
        except Exception:
            # Fail-safe: ignore UI reset errors
            pass

# ADD: main guard to launch GUI
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TranslationApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Fatal startup error: {e}")