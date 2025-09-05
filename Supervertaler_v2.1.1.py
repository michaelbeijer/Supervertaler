# --- Supervertaler (v2.1.1) - Multi-LLM AI-powered Translator & Proofreader with DOCX Change References ---
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

# ADD: central version constant (was missing, caused NameError)
APP_VERSION = "2.1.1"
print(f"=== Supervertaler v{APP_VERSION} starting ===")

# --- Changelog (v2.1.1) ---
# - Bumped version to 2.1.1.
# - Added/updated external CHANGELOG.md with details for this release.
# - No functional changes vs. prior applied fixes; includes:
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
        tk.Label(detail_frame, text="Original Text:", font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        self.original_text = tk.Text(detail_frame, height=4, wrap=tk.WORD, state="disabled", 
                                    bg="#f8f8f8", relief="solid", borderwidth=1)
        self.original_text.pack(fill=tk.X, pady=(2,5))
        
        # Final text display  
        tk.Label(detail_frame, text="Final Text:", font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
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
                                                       tracked_changes_data=None):
        if not self.model:
            self.log_queue.put(f"[Gemini Translator] Model ('{self.model_name}') not init.")
            return {n: f"[Err: Model not init]" for n in lines_map_to_translate.keys()}
        if not lines_map_to_translate:
            self.log_queue.put(f"[Gemini Translator] No lines for chunk.")
            return {}

        line_nums = sorted(list(lines_map_to_translate.keys()))
        self.log_queue.put(f"[Gemini Translator] Translating {len(line_nums)} lines: {line_nums[:3]}... w/ '{self.model_name}' (drawings + tracked changes if available)...")

        prompt_parts = []
        prompt_parts.append(f"You are an expert {source_lang} to {target_lang} translator specialized in patent documents.")
        if user_custom_instructions:
            prompt_parts.append(f"\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}\n")

        if tracked_changes_data:
            current_src = [all_source_segments_original_list[n-1] for n in line_nums]
            rel = tracked_changes_data.find_relevant_changes(current_src)
            if rel:
                prompt_parts.append(format_tracked_changes_context(rel))
                self.log_queue.put(f"[Gemini Translator] Added {len(rel)} relevant tracked changes as context")

        prompt_parts.extend([
            "The full patent text for overall context is in 'FULL PATENT CONTEXT' below. Translate ONLY sentences from 'PATENT SENTENCES TO TRANSLATE' later. These are listed with their original line numbers from the full document.",
            "If a sentence refers to a Figure (e.g., 'Figure 1A', 'Figuur X'), relevant images may be provided just before that sentence. Use these images as crucial context for accurately translating references to parts, features, or relationships shown in those figures.",
            "Present your output ONLY as a numbered list of the translations for the requested sentences, using their original numbering. Maintain accuracy and appropriate patent terminology.\n",
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
                                             user_custom_instructions="", tracked_changes_data=None):
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

        prompt_parts = [
            f"You are an expert proofreader and editor for {source_lang} → {target_lang} translations, specializing in patent documents."
        ]
        if user_custom_instructions:
            prompt_parts.append(f"\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}\n")

        if tracked_changes_data:
            current_src = [all_source_segments_original_list[n-1] for n in line_nums]
            rel = tracked_changes_data.find_relevant_changes(current_src)
            if rel:
                prompt_parts.append(format_tracked_changes_context(rel))
                self.log_queue.put(f"[Gemini Proofreader] Added {len(rel)} relevant tracked changes as context")

        prompt_parts.extend([
            "For each segment you get SOURCE SEGMENT and EXISTING TRANSLATION.",
            "Tasks: accuracy, terminology consistency, patent tone, grammar, fluency, completeness, figure-reference consistency.",
            f"OUTPUT FORMAT STRICTLY:\n1) Numbered list of revised {target_lang} translations (use same numbering; if no change, reproduce original).\n"
            "2) Then a section:\n---CHANGES SUMMARY START---\n"
            "Per modified line: '<line>. <brief description of changes>' OR if none changed: 'No changes made to any segment in this batch.'\n"
            "---CHANGES SUMMARY END---",
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
            msg = {"role": "user", "content": prompt_parts}
            response = self.model.generate_content(msg)
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
                                                       tracked_changes_data=None):
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
                                             user_custom_instructions="", tracked_changes_data=None):
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

# --- Agent Factory Functions ---
def create_translation_agent(provider, api_key, log_queue, model_name):
    if provider.lower() == "gemini":
        return GeminiTranslationAgent(api_key, log_queue, model_name)
    elif provider.lower() == "claude":
        return ClaudeTranslationAgent(api_key, log_queue, model_name)
    elif provider.lower() == "openai":
        log_queue.put("[Factory] OpenAI translator not implemented in this build.")
        return None
    else:
        log_queue.put(f"[Factory] Unknown provider: {provider}")
        return None

def create_proofreading_agent(provider, api_key, log_queue, model_name):
    if provider.lower() == "gemini":
        return GeminiProofreadingAgent(api_key, log_queue, model_name)
    elif provider.lower() == "claude":
        return ClaudeProofreadingAgent(api_key, log_queue, model_name)
    elif provider.lower() == "openai":
        log_queue.put("[Factory] OpenAI proofreader not implemented in this build.")
        return None
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
        root.title(f"Supervertaler (v{APP_VERSION}) - Multi-LLM AI-powered Translator & Proofreader with Tracked Changes") 
        root.geometry("1100x950")  # Wider to accommodate right-side log

        self.log_queue = queue.Queue()
        self.api_keys = API_KEYS
        self.tm_agent = TMAgent(self.log_queue)
        self.tracked_changes_agent = TrackedChangesAgent(self.log_queue)  # UPDATED: Use TrackedChangesAgent
        self.drawings_images_map = {} 
        self.tracked_changes_browser = None  # Reference to the tracked changes browser window

        # Create the log widget instance early to make it available for logging during init
        self.log_text = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD, state="disabled")

        # --- UPDATED UNIFIED INFO TEXT ---
        self.info_text_content_unified = (
            "Supervertaler is an AI-powered document translation & proofreading tool operating in two modes: TRANSLATE or PROOFREAD. "
            "It leverages multiple context sources for enhanced accuracy.\n\n"
            "COMMON CONTEXT SOURCES (both modes):\n"
            "• Full Document Content: Entire source (and existing target in Proofread mode) provided for context.\n"
            "• Images: If a 'Document Images Folder' is set, figures (e.g., 'Fig 1A.png') are shown to the AI when referenced.\n"
            "• Tracked Changes: Load DOCX (with tracked changes) and/or TSV (Original<TAB>Final) to supply editing pattern examples.\n"
            "• Custom Instructions: Freeform guidance appended to the system prompt.\n\n"
            "MODE DETAILS:\n\n"
            "TRANSLATE MODE:\n"
            "• Input Format: Text file (.txt) with one source segment per line.\n"
            "• TM Usage: Exact matches from TM (.tmx or .txt) populate target before any LLM calls.\n"
            "• Output Format: source_text<TAB>translated_text.txt + TMX\n"
            "  (Always exactly two columns. Previous extra columns are not propagated.)\n"
            "• Re-translation: Supplying a previously exported 2‑column file is safe; only column 1 is read and a fresh translation is written as column 2.\n\n"
            "PROOFREAD MODE:\n"
            "• Input Format: source_text<TAB>EXISTING_target_text<TAB>[optional_comment]\n"
            "• TM Usage: Not applied (all segments go to the model).\n"
            "• Output Format: source_text<TAB>REVISED_target_text<TAB>COMMENT\n"
            "  COMMENT merges (if present): original comment + AI change summary (only if changes or summary supplied).\n\n"
            "OUTPUT FILES:\n"
            "• Tab-delimited TXT: Primary result (see mode-specific formats above).\n"
            "• TMX (Translate mode only): Auto-generated alongside TXT (same basename) excluding error/empty segments.\n\n"
            "OTHER FEATURES:\n"
            "• Chunking: Large inputs split into batches (size = Chunk Size lines).\n"
            "• Figure/Image Matching: Filenames normalized (e.g., 'Figure_1-A.PNG' recognized as 'fig1a').\n"
            "• Tracked Changes Context: A capped sample of relevant original→final pairs is injected per batch.\n"
            "• Providers: Claude / Gemini / OpenAI.\n"
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

        # Create main frame to split left (controls) and right (log)
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left frame for all controls
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5))
        
        # Right frame for log
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        current_row = 0
        self.info_label = tk.Label(left_frame,text=self.info_text_content_unified,wraplength=650,justify=tk.LEFT,anchor="w",relief=tk.SOLID,borderwidth=1,padx=5, pady=5)
        self.info_label.grid(row=current_row, column=0, columnspan=3, padx=5, pady=(5,10), sticky="ew"); current_row += 1
        
        mode_frame = tk.Frame(left_frame)
        mode_frame.grid(row=current_row, column=0, columnspan=3, pady=2, sticky="w", padx=5)
        tk.Label(mode_frame, text="Operation Mode:").pack(side=tk.LEFT, padx=(0,5))
        self.operation_mode_var = tk.StringVar(value="Translate")
        tk.Radiobutton(mode_frame, text="Translate", variable=self.operation_mode_var, value="Translate", command=self.update_ui_for_mode).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Proofread", variable=self.operation_mode_var, value="Proofread", command=self.update_ui_for_mode).pack(side=tk.LEFT, padx=(10,0))
        current_row += 1

        self.input_file_var = tk.StringVar(); self.output_file_var = tk.StringVar()
        self.tm_file_var = tk.StringVar(); self.drawings_folder_var = tk.StringVar() 

        self.input_file_label = tk.Label(left_frame, text="Input Text File (one source per line):") 
        self.input_file_label.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(left_frame, textvariable=self.input_file_var, width=50, state="readonly").grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(left_frame, text="Browse...", command=self.browse_input_file).grid(row=current_row, column=2, padx=5, pady=2); current_row += 1
        
        tk.Label(left_frame, text="Output File:").grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(left_frame, textvariable=self.output_file_var, width=50, state="readonly").grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(left_frame, text="Browse...", command=self.browse_output_file).grid(row=current_row, column=2, padx=5, pady=2); current_row += 1

        # Context Sources Section
        context_sources_frame = tk.LabelFrame(left_frame, text="Context Sources", font=("TkDefaultFont", 9, "bold"), padx=5, pady=5)
        context_sources_frame.grid(row=current_row, column=0, columnspan=3, padx=5, pady=(10,5), sticky="ew"); current_row += 1

        # TM File row
        context_row = 0
        self.tm_file_label = tk.Label(context_sources_frame, text="TM File (txt/tmx):") 
        self.tm_file_label.grid(row=context_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(context_sources_frame, textvariable=self.tm_file_var, width=50, state="readonly").grid(row=context_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(context_sources_frame, text="Browse TM...", command=self.browse_tm_file).grid(row=context_row, column=2, padx=5, pady=2); context_row += 1

        # Tracked Changes row
        tk.Label(context_sources_frame, text="Tracked-changes:").grid(row=context_row, column=0, padx=5, pady=2, sticky="w")
        

        tracked_changes_inner_frame = tk.Frame(context_sources_frame)
        tracked_changes_inner_frame.grid(row=context_row, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        
        self.tracked_changes_status_label = tk.Label(tracked_changes_inner_frame, text="No tracked changes loaded", fg="gray")
        self.tracked_changes_status_label.pack(side=tk.LEFT)
        
        tk.Button(tracked_changes_inner_frame, text="Load Files...", command=self.load_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        tk.Button(tracked_changes_inner_frame, text="Browse Changes", command=self.browse_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        tk.Button(tracked_changes_inner_frame, text="Clear", command=self.clear_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        context_row += 1

        # Document Images Folder row
        self.document_images_label = tk.Label(context_sources_frame, text="Document Images Folder:")
        self.document_images_label.grid(row=context_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(context_sources_frame, textvariable=self.drawings_folder_var, width=50, state="readonly").grid(row=context_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(context_sources_frame, text="Browse...", command=self.browse_drawings_folder).grid(row=context_row, column=2, padx=5, pady=2); context_row += 1

        # Custom Instructions row
        tk.Label(context_sources_frame, text="Custom Instructions for AI:").grid(row=context_row, column=0, padx=5, pady=(5,0), sticky="nw")
        self.custom_instructions_text = tk.Text(context_sources_frame, height=4, width=50, wrap=tk.WORD, borderwidth=1, relief="solid")
        self.custom_instructions_text.grid(row=context_row, column=1, columnspan=2, padx=5, pady=2, sticky="ew"); context_row += 1

        # Configure column weights for context sources frame
        context_sources_frame.grid_columnconfigure(1, weight=1)
        
        self.source_lang_var = tk.StringVar(value="Dutch")
        self.target_lang_var = tk.StringVar(value="English")
        self.chunk_size_var = tk.StringVar(value="100")

        # AI Provider and Model Selection
        provider_frame = tk.Frame(left_frame)
        provider_frame.grid(row=current_row, column=0, columnspan=3, pady=2, sticky="ew", padx=5)
        tk.Label(provider_frame, text="AI Provider:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        
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
        
        tk.Label(provider_frame, text="Model:").grid(row=0, column=2, padx=(20,5), pady=2, sticky="w")
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
            tk.Label(left_frame, text=text).grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
            tk.Entry(left_frame, textvariable=var, width=width).grid(row=current_row, column=1, padx=5, pady=2, sticky="w"); current_row += 1

        buttons_frame = tk.Frame(left_frame); buttons_frame.grid(row=current_row, column=0, columnspan=3, pady=5); current_row += 1
        self.process_button = tk.Button(buttons_frame, text="Start Process", command=self.start_processing_thread, width=15, height=2); self.process_button.pack(side=tk.LEFT, padx=10) 
        self.list_models_button = tk.Button(buttons_frame, text="List Models", command=self.list_available_models, width=15); self.list_models_button.pack(side=tk.LEFT, padx=10) 
        self.refresh_models_button = tk.Button(buttons_frame, text="Refresh Models", command=self.update_available_models, width=15); self.refresh_models_button.pack(side=tk.LEFT, padx=10)
        
        # Log section in right frame
        tk.Label(right_frame, text="Log:", font=("TkDefaultFont", 9, "bold")).pack(anchor="w", padx=5, pady=(0,2))
        self.log_text = scrolledtext.ScrolledText(right_frame, width=50, height=35, wrap=tk.WORD, state="disabled")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=0)
        
        # Configure main window column weights
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

    def browse_output_file(self):
        filepath = filedialog.asksaveasfilename(title="Save Output File As", filetypes=(("Text files", "*.txt"),("All files", "*.*")), defaultextension=".txt")
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
                                        self.drawings_images_map, custom_instr)) 
        thread.daemon = True; thread.start()

    def run_pipeline(self, mode, input_f, output_f, source_lang, target_lang, provider, model_name, chunk_s, drawings_map, user_custom_instructions):
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
                        tracked_changes_data=self.tracked_changes_agent)
                elif mode == "Proofread":
                    lines_map_for_llm = {orig_idx + 1: {"source": source_segments_original[orig_idx], "target_original": original_target_segments[orig_idx]} for orig_idx in current_orig_doc_indices}
                    chunk_results = proofreader.proofread_specific_lines_with_context(
                        lines_map_for_llm, full_source_doc_str, full_original_target_doc_str,
                        source_lang, target_lang, source_segments_original, drawings_map,
                        user_custom_instructions, tracked_changes_data=self.tracked_changes_agent)
                
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
                if existing_comment: comment_parts.append(f"ORIGINAL COMMENT:\n{existing_comment}")
                if revised_target.strip() != original_target_segments[i].strip(): 
                    if ai_summary and "No changes made" not in ai_summary:
                        comment_parts.append(f"PROOFREADER COMMENT (AI):\n{ai_summary}")
                    else: 
                        comment_parts.append(f"PROOFREADER COMMENT (AI):\nSegment was modified by AI.")
                        modified_lines_count +=1
                elif ai_summary and "No changes made" not in ai_summary: 
                     comment_parts.append(f"PROOFREADER COMMENT (AI):\n{ai_summary} (Note: Text appears identical to original despite summary.)")
                output_comment_list.append("\n\n".join(comment_parts).strip() if comment_parts else None)
        
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