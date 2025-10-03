"""
CAT Editor Prototype v0.1
Standalone Computer-Aided Translation Editor

Features:
- Import DOCX files
- Sentence segmentation
- Editable grid interface
- Export to DOCX (with formatting), TSV, and JSON
- Find/Replace functionality
- Status tracking
- Progress monitoring

Author: Supervertaler Project
Date: October 1, 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import our custom modules
try:
    from simple_segmenter import SimpleSegmenter
    from docx_handler import DOCXHandler
    from tag_manager import TagManager
except ImportError:
    print("ERROR: Could not import required modules")
    print("Make sure simple_segmenter.py, docx_handler.py, and tag_manager.py are in the same folder")
    import sys
    sys.exit(1)


class LayoutMode:
    """Layout mode constants"""
    GRID = "grid"      # memoQ-style inline editing
    SPLIT = "split"    # Current style with editor panel
    COMPACT = "compact" # Maximum density view


class Segment:
    """Represents a translation segment"""
    
    def __init__(self, seg_id: int, source: str, paragraph_id: int = 0, 
                 is_table_cell: bool = False, table_info: tuple = None,
                 style: str = None):
        self.id = seg_id
        self.source = source
        self.target = ""
        self.status = "untranslated"  # untranslated, draft, translated, approved
        self.paragraph_id = paragraph_id
        self.notes = ""
        self.modified = False
        self.created_at = datetime.now().isoformat()
        self.modified_at = datetime.now().isoformat()
        
        # Table information
        self.is_table_cell = is_table_cell
        self.table_info = table_info  # (table_idx, row_idx, cell_idx) if is_table_cell
        
        # Style information (Heading 1, Normal, Title, etc.)
        self.style = style or "Normal"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'source': self.source,
            'target': self.target,
            'status': self.status,
            'paragraph_id': self.paragraph_id,
            'notes': self.notes,
            'modified': self.modified,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'is_table_cell': self.is_table_cell,
            'table_info': self.table_info,
            'style': self.style
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Segment':
        """Create Segment from dictionary"""
        seg = cls(data['id'], data['source'], data.get('paragraph_id', 0),
                  data.get('is_table_cell', False), data.get('table_info'),
                  data.get('style', 'Normal'))
        seg.target = data.get('target', '')
        seg.status = data.get('status', 'untranslated')
        seg.notes = data.get('notes', '')
        seg.modified = data.get('modified', False)
        seg.created_at = data.get('created_at', datetime.now().isoformat())
        seg.modified_at = data.get('modified_at', datetime.now().isoformat())
        return seg


class CATEditorPrototype:
    """Main CAT Editor application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Supervertaler CAT Editor - Prototype v0.4.0")
        self.root.geometry("1200x800")
        
        # Layout mode
        self.layout_mode = LayoutMode.GRID  # Default to memoQ-style
        self.current_edit_widget = None  # For inline editing in Grid mode
        
        # Data
        self.segments: List[Segment] = []
        self.current_segment: Optional[Segment] = None
        self.project_file: Optional[str] = None
        self.original_docx: Optional[str] = None
        self.modified = False
        
        # Components
        self.segmenter = SimpleSegmenter()
        self.docx_handler = DOCXHandler()
        self.tag_manager = TagManager()
        
        # Setup UI
        self.setup_ui()
        
        # Status
        self.log("CAT Editor ready. Import a DOCX file to begin.")
        self.log("✨ Layout modes available: Grid (memoQ-style), Split, Compact")
    
    def setup_ui(self):
        """Create the user interface"""
        
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import DOCX...", command=self.import_docx, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save Project", command=self.save_project, accelerator="Ctrl+S")
        file_menu.add_command(label="Save Project As...", command=self.save_project_as)
        file_menu.add_command(label="Load Project...", command=self.load_project, accelerator="Ctrl+L")
        file_menu.add_separator()
        file_menu.add_command(label="Export to DOCX...", command=self.export_docx)
        file_menu.add_command(label="Export to Bilingual DOCX...", command=self.export_bilingual_docx)
        file_menu.add_command(label="Export to TSV...", command=self.export_tsv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Find/Replace...", command=self.show_find_replace, accelerator="Ctrl+F")
        edit_menu.add_separator()
        edit_menu.add_command(label="Copy Source to Target", command=self.copy_source_to_target, accelerator="Ctrl+D")
        edit_menu.add_command(label="Clear Target", command=self.clear_target)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.import_docx())
        self.root.bind('<Control-s>', lambda e: self.save_project())
        self.root.bind('<Control-l>', lambda e: self.load_project())
        self.root.bind('<Control-f>', lambda e: self.show_find_replace())
        self.root.bind('<Control-d>', lambda e: self.copy_source_to_target())
        
        # Layout switching shortcuts
        self.root.bind('<Control-Key-1>', lambda e: self.switch_layout(LayoutMode.GRID))
        self.root.bind('<Control-Key-2>', lambda e: self.switch_layout(LayoutMode.SPLIT))
        self.root.bind('<Control-Key-3>', lambda e: self.switch_layout(LayoutMode.COMPACT))
        
        # Navigation shortcuts
        self.root.bind('<Control-Down>', lambda e: self.navigate_segment('next'))
        self.root.bind('<Control-Up>', lambda e: self.navigate_segment('prev'))
        
        # F2 to enter edit mode (works globally when segment is selected)
        self.root.bind('<F2>', lambda e: self.enter_edit_mode_global())
        
        # Toolbar
        self.toolbar = tk.Frame(self.root, bg='#f0f0f0', height=40)
        self.toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Button(self.toolbar, text="📁 Import DOCX", command=self.import_docx,
                 bg='#4CAF50', fg='white', padx=10).pack(side='left', padx=2)
        tk.Button(self.toolbar, text="💾 Save Project", command=self.save_project,
                 bg='#2196F3', fg='white', padx=10).pack(side='left', padx=2)
        tk.Button(self.toolbar, text="📤 Export DOCX", command=self.export_docx,
                 bg='#FF9800', fg='white', padx=10).pack(side='left', padx=2)
        
        ttk.Separator(self.toolbar, orient='vertical').pack(side='left', fill='y', padx=10)
        
        # Layout mode buttons
        self.layout_btn_grid = tk.Button(self.toolbar, text="📊 Grid View", 
                                         command=lambda: self.switch_layout(LayoutMode.GRID),
                                         bg='#9C27B0', fg='white', padx=10, relief='sunken')
        self.layout_btn_grid.pack(side='left', padx=2)
        
        self.layout_btn_split = tk.Button(self.toolbar, text="📋 Split View",
                                          command=lambda: self.switch_layout(LayoutMode.SPLIT),
                                          padx=10, relief='raised')
        self.layout_btn_split.pack(side='left', padx=2)
        
        self.layout_btn_compact = tk.Button(self.toolbar, text="📄 Compact View",
                                            command=lambda: self.switch_layout(LayoutMode.COMPACT),
                                            padx=10, relief='raised')
        self.layout_btn_compact.pack(side='left', padx=2)
        
        ttk.Separator(self.toolbar, orient='vertical').pack(side='left', fill='y', padx=10)
        
        tk.Button(self.toolbar, text="🔍 Find/Replace", command=self.show_find_replace,
                 padx=10).pack(side='left', padx=2)
        
        # Progress info
        self.progress_label = tk.Label(self.toolbar, text="No document loaded", bg='#f0f0f0')
        self.progress_label.pack(side='right', padx=10)
        
        # Main content area - will be populated based on layout mode
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        
        # Create the appropriate layout
        self.create_layout_ui()
        
        # Log/Status area
        log_frame = tk.LabelFrame(self.root, text="Log", padx=5, pady=5)
        log_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=4, wrap='word',
                                                  font=('Consolas', 9), state='disabled')
        self.log_text.pack(fill='both', expand=True)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_layout_ui(self):
        """Create UI based on current layout mode"""
        if self.layout_mode == LayoutMode.GRID:
            self.create_grid_layout()
        elif self.layout_mode == LayoutMode.SPLIT:
            self.create_split_layout()
        elif self.layout_mode == LayoutMode.COMPACT:
            self.create_compact_layout()
    
    def create_grid_layout(self):
        """Create Grid View layout (memoQ-style with inline editing)"""
        
        # Grid frame
        grid_frame = tk.LabelFrame(self.content_frame, text="Translation Grid - Grid View (Double-click target to edit)", padx=5, pady=5)
        grid_frame.pack(side='top', fill='both', expand=True)
        
        # Create treeview with 5 columns (no Style column)
        self.tree = ttk.Treeview(grid_frame,
                                columns=('id', 'type', 'status', 'source', 'target'),
                                show='headings',
                                selectmode='browse')
        
        # Define columns - wider source/target for better readability
        self.tree.heading('id', text='#')
        self.tree.heading('type', text='Type')
        self.tree.heading('status', text='Status')
        self.tree.heading('source', text='Source')
        self.tree.heading('target', text='Target')
        
        self.tree.column('id', width=40, minwidth=40, anchor='center', stretch=False)
        self.tree.column('type', width=65, minwidth=60, anchor='center', stretch=False)
        self.tree.column('status', width=95, minwidth=90, anchor='center', stretch=False)
        self.tree.column('source', width=500, minwidth=300, anchor='w', stretch=True)
        self.tree.column('target', width=500, minwidth=300, anchor='w', stretch=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(grid_frame, orient='vertical', command=self.tree.yview)
        h_scroll = ttk.Scrollbar(grid_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        grid_frame.grid_rowconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(0, weight=1)
        
        # Configure row colors
        self.tree.tag_configure('untranslated', background='#ffe6e6')
        self.tree.tag_configure('draft', background='#fff9e6')
        self.tree.tag_configure('translated', background='#e6ffe6')
        self.tree.tag_configure('approved', background='#e6f3ff')
        self.tree.tag_configure('table_cell', foreground='#0066cc', font=('TkDefaultFont', 9, 'italic'))
        
        # Configure style-specific formatting
        self.tree.tag_configure('heading1', font=('TkDefaultFont', 10, 'bold'), foreground='#003366')
        self.tree.tag_configure('heading2', font=('TkDefaultFont', 9, 'bold'), foreground='#0066cc')
        self.tree.tag_configure('heading3', font=('TkDefaultFont', 9, 'bold'), foreground='#3399ff')
        self.tree.tag_configure('title', font=('TkDefaultFont', 11, 'bold'), foreground='#663399')
        self.tree.tag_configure('subtitle', font=('TkDefaultFont', 9, 'italic'), foreground='#663399')
        
        # Bind events for inline editing
        self.tree.bind('<<TreeviewSelect>>', self.on_segment_select_grid)
        self.tree.bind('<Double-1>', self.on_cell_double_click)
        self.tree.bind('<F2>', self.enter_edit_mode)
        self.tree.bind('<Return>', lambda e: self.enter_edit_mode())
        
        # Bind Ctrl+D for copy source to target in Grid mode
        self.tree.bind('<Control-d>', lambda e: self.copy_source_to_target())
        
        # Context menu
        self.create_context_menu()
        self.tree.bind('<Button-3>', self.show_context_menu)  # Right-click
        
        # Tag validation indicator (below grid)
        self.tag_validation_label = tk.Label(self.content_frame, text="", 
                                            font=('Segoe UI', 9), fg='#666')
        self.tag_validation_label.pack(side='bottom', pady=5)
    
    def create_split_layout(self):
        """Create Split View layout (current style with editor panel)"""
        
        # Grid frame (top part)
        grid_frame = tk.LabelFrame(self.content_frame, text="Translation Grid", padx=5, pady=5)
        grid_frame.pack(side='top', fill='both', expand=True)
        
        # Create treeview for segments
        self.tree = ttk.Treeview(grid_frame,
                                columns=('id', 'type', 'style', 'status', 'source', 'target'),
                                show='headings',
                                selectmode='browse')
        
        # Define columns
        self.tree.heading('id', text='#')
        self.tree.heading('type', text='Type')
        self.tree.heading('style', text='Style')
        self.tree.heading('status', text='Status')
        self.tree.heading('source', text='Source')
        self.tree.heading('target', text='Target')
        
        self.tree.column('id', width=40, minwidth=40, anchor='center', stretch=False)
        self.tree.column('type', width=65, minwidth=60, anchor='center', stretch=False)
        self.tree.column('style', width=80, minwidth=70, anchor='w', stretch=False)
        self.tree.column('status', width=95, minwidth=90, anchor='center', stretch=False)
        self.tree.column('source', width=400, minwidth=200, anchor='w', stretch=True)
        self.tree.column('target', width=400, minwidth=200, anchor='w', stretch=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(grid_frame, orient='vertical', command=self.tree.yview)
        h_scroll = ttk.Scrollbar(grid_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        grid_frame.grid_rowconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(0, weight=1)
        
        # Configure row colors
        self.tree.tag_configure('untranslated', background='#ffe6e6')
        self.tree.tag_configure('draft', background='#fff9e6')
        self.tree.tag_configure('translated', background='#e6ffe6')
        self.tree.tag_configure('approved', background='#e6f3ff')
        self.tree.tag_configure('table_cell', foreground='#0066cc', font=('TkDefaultFont', 9, 'italic'))
        
        # Configure style-specific formatting
        self.tree.tag_configure('heading1', font=('TkDefaultFont', 10, 'bold'), foreground='#003366')
        self.tree.tag_configure('heading2', font=('TkDefaultFont', 9, 'bold'), foreground='#0066cc')
        self.tree.tag_configure('heading3', font=('TkDefaultFont', 9, 'bold'), foreground='#3399ff')
        self.tree.tag_configure('title', font=('TkDefaultFont', 11, 'bold'), foreground='#663399')
        self.tree.tag_configure('subtitle', font=('TkDefaultFont', 9, 'italic'), foreground='#663399')
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_segment_select)
        self.tree.bind('<Return>', lambda e: self.focus_target_editor())
        self.tree.bind('<Double-1>', lambda e: self.focus_target_editor())
        
        # Editor frame (bottom part)
        editor_frame = tk.LabelFrame(self.content_frame, text="Segment Editor", padx=10, pady=10)
        editor_frame.pack(side='bottom', fill='x', pady=(5, 0))
        
        # Segment info
        info_frame = tk.Frame(editor_frame)
        info_frame.pack(fill='x', pady=(0, 5))
        
        self.seg_info_label = tk.Label(info_frame, text="No segment selected",
                                       font=('Segoe UI', 9, 'bold'))
        self.seg_info_label.pack(side='left')
        
        # Status selector
        status_frame = tk.Frame(info_frame)
        status_frame.pack(side='right')
        
        tk.Label(status_frame, text="Status:").pack(side='left', padx=(0, 5))
        self.status_var = tk.StringVar(value="untranslated")
        self.status_combo = ttk.Combobox(status_frame, textvariable=self.status_var,
                                        values=["untranslated", "draft", "translated", "approved"],
                                        state='readonly', width=12)
        self.status_combo.pack(side='left')
        self.status_combo.bind('<<ComboboxSelected>>', self.on_status_change)
        
        # Source (read-only)
        tk.Label(editor_frame, text="Source:", font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.source_text = tk.Text(editor_frame, height=2, wrap='word', bg='#f5f5f5',
                                   state='disabled', font=('Segoe UI', 10))
        self.source_text.pack(fill='x', pady=(2, 10))
        
        # Target (editable)
        target_header_frame = tk.Frame(editor_frame)
        target_header_frame.pack(fill='x', anchor='w')
        tk.Label(target_header_frame, text="Target:", font=('Segoe UI', 9, 'bold')).pack(side='left')
        self.tag_validation_label = tk.Label(target_header_frame, text="", font=('Segoe UI', 8))
        self.tag_validation_label.pack(side='left', padx=(10, 0))
        
        self.target_text = tk.Text(editor_frame, height=2, wrap='word', font=('Segoe UI', 10))
        self.target_text.pack(fill='x', pady=(2, 5))
        self.target_text.bind('<KeyRelease>', self.on_target_change)
        self.target_text.bind('<Control-Return>', lambda e: self.save_segment_and_next())
        
        # Tag buttons
        tag_button_frame = tk.Frame(editor_frame)
        tag_button_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(tag_button_frame, text="Insert:").pack(side='left', padx=(0, 5))
        tk.Button(tag_button_frame, text="<b>Bold</b>", command=lambda: self.insert_tag('b'),
                 relief='flat', bg='#ffcccc', font=('Segoe UI', 8)).pack(side='left', padx=2)
        tk.Button(tag_button_frame, text="<i>Italic</i>", command=lambda: self.insert_tag('i'),
                 relief='flat', bg='#ccccff', font=('Segoe UI', 8, 'italic')).pack(side='left', padx=2)
        tk.Button(tag_button_frame, text="<u>Underline</u>", command=lambda: self.insert_tag('u'),
                 relief='flat', bg='#ccffcc', font=('Segoe UI', 8, 'underline')).pack(side='left', padx=2)
        tk.Button(tag_button_frame, text="Strip Tags", command=self.strip_tags_from_target,
                 relief='flat', bg='#eeeeee', font=('Segoe UI', 8)).pack(side='left', padx=10)
        tk.Button(tag_button_frame, text="Copy Source Tags", command=self.copy_source_tags,
                 relief='flat', bg='#e6f3ff', font=('Segoe UI', 8)).pack(side='left', padx=2)
        
        # Action buttons
        button_frame = tk.Frame(editor_frame)
        button_frame.pack(fill='x')
        
        tk.Button(button_frame, text="Copy Source → Target", command=self.copy_source_to_target
                 ).pack(side='left', padx=(0, 5))
        tk.Button(button_frame, text="Clear Target", command=self.clear_target
                 ).pack(side='left', padx=(0, 5))
        tk.Button(button_frame, text="Save & Next (Ctrl+Enter)", command=self.save_segment_and_next,
                 bg='#4CAF50', fg='white').pack(side='right')
    
    def create_compact_layout(self):
        """Create Compact View layout (minimal columns, maximum density)"""
        # TODO: Implement compact layout
        # For now, create same as grid but will be enhanced later
        self.create_grid_layout()
    
    def log(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
    
    def switch_layout(self, new_mode: str):
        """Switch between layout modes"""
        if new_mode == self.layout_mode:
            return  # Already in this mode
        
        self.log(f"Switching to {new_mode} layout...")
        
        # Save current segment if any
        if self.current_segment:
            self.save_current_segment()
        
        # Remember current selection
        selection = self.tree.selection()
        current_seg_id = None
        if selection:
            item = selection[0]
            current_seg_id = int(self.tree.item(item)['values'][0])
        
        # Update layout mode
        self.layout_mode = new_mode
        
        # Update button states
        self.update_layout_buttons()
        
        # For now, just log the change (UI rebuild will come in next phase)
        mode_names = {
            LayoutMode.GRID: "Grid View (memoQ-style)",
            LayoutMode.SPLIT: "Split View (Current)",
            LayoutMode.COMPACT: "Compact View"
        }
        self.log(f"✓ Switched to {mode_names.get(new_mode, new_mode)}")
        
        # TODO: Rebuild UI based on layout mode
        # This will be implemented in the next phase
    
    def update_layout_buttons(self):
        """Update layout button visual states"""
        # Reset all buttons
        self.layout_btn_grid.config(relief='raised', bg='#E0E0E0', fg='black')
        self.layout_btn_split.config(relief='raised', bg='#E0E0E0', fg='black')
        self.layout_btn_compact.config(relief='raised', bg='#E0E0E0', fg='black')
        
        # Highlight active button
        if self.layout_mode == LayoutMode.GRID:
            self.layout_btn_grid.config(relief='sunken', bg='#9C27B0', fg='white')
        elif self.layout_mode == LayoutMode.SPLIT:
            self.layout_btn_split.config(relief='sunken', bg='#9C27B0', fg='white')
        elif self.layout_mode == LayoutMode.COMPACT:
            self.layout_btn_compact.config(relief='sunken', bg='#9C27B0', fg='white')
    
    # Grid View inline editing methods
    
    def create_context_menu(self):
        """Create context menu for Grid View"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="📋 Copy Source → Target (Ctrl+D)", 
                                     command=self.copy_source_to_target)
        self.context_menu.add_command(label="📄 View Source Text (Double-click source)", 
                                     command=lambda: self.show_source_popup_from_menu())
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Insert <b>Bold</b> Tag (Ctrl+B)", 
                                     command=lambda: self.insert_tag_inline('b'))
        self.context_menu.add_command(label="Insert <i>Italic</i> Tag (Ctrl+I)", 
                                     command=lambda: self.insert_tag_inline('i'))
        self.context_menu.add_command(label="Insert <u>Underline</u> Tag (Ctrl+U)", 
                                     command=lambda: self.insert_tag_inline('u'))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Clear Target", 
                                     command=self.clear_target_inline)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✅ Mark as Translated", 
                                     command=lambda: self.set_status_inline('translated'))
        self.context_menu.add_command(label="⭐ Mark as Approved", 
                                     command=lambda: self.set_status_inline('approved'))
        self.context_menu.add_command(label="📝 Mark as Draft", 
                                     command=lambda: self.set_status_inline('draft'))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="⬇️ Next Segment (Ctrl+Down)", 
                                     command=lambda: self.navigate_segment('next'))
        self.context_menu.add_command(label="⬆️ Previous Segment (Ctrl+Up)", 
                                     command=lambda: self.navigate_segment('prev'))
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the row under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def show_source_popup_from_menu(self):
        """Show source popup from context menu"""
        # Create a fake event at center of screen
        class FakeEvent:
            pass
        event = FakeEvent()
        event.x_root = self.root.winfo_x() + self.root.winfo_width() // 2
        event.y_root = self.root.winfo_y() + self.root.winfo_height() // 2
        self.show_source_popup(event)
    
    def on_segment_select_grid(self, event):
        """Handle segment selection in Grid View (minimal action)"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        seg_id = int(self.tree.item(item)['values'][0])
        
        # Find and set current segment
        for seg in self.segments:
            if seg.id == seg_id:
                self.current_segment = seg
                break
    
    def on_cell_double_click(self, event):
        """Handle double-click on cell - check if it's the target column"""
        # Identify what was clicked
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        column = self.tree.identify_column(event.x)
        # Column #4 is source, #5 is target (0-indexed: #0 is tree column, #1-5 are our columns)
        if column == '#4':  # Source column
            self.show_source_popup(event)
        elif column == '#5':  # Target column
            self.enter_edit_mode()
    
    def enter_edit_mode_global(self):
        """Enter edit mode from anywhere - works in Grid or Split mode"""
        if not self.current_segment:
            return
        
        if self.layout_mode == LayoutMode.GRID:
            # In Grid mode, enter inline editing
            self.enter_edit_mode()
        else:
            # In Split mode, focus the target text widget
            if hasattr(self, 'target_text'):
                self.target_text.focus()
    
    def enter_edit_mode(self, event=None):
        """Enter inline edit mode for target cell"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        
        # Get cell bounds for target column
        bbox = self.tree.bbox(item, column='#5')  # Target column
        if not bbox:
            return
        
        # Create Entry widget overlay
        self.current_edit_widget = tk.Entry(
            self.tree,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=2,
            bg='#ffffcc'  # Yellow background to indicate edit mode
        )
        
        # Position over cell
        x, y, width, height = bbox
        self.current_edit_widget.place(
            x=x, y=y, width=width, height=height
        )
        
        # Get current target text
        segment = self.current_segment
        if segment:
            self.current_edit_widget.insert(0, segment.target)
            self.current_edit_widget.select_range(0, tk.END)
            self.current_edit_widget.focus()
        
        # Bind keys
        self.current_edit_widget.bind('<Return>', 
            lambda e: self.save_inline_edit(go_next=False))
        self.current_edit_widget.bind('<Control-Return>', 
            lambda e: self.save_inline_edit(go_next=True))
        self.current_edit_widget.bind('<Escape>', 
            lambda e: self.cancel_inline_edit())
        self.current_edit_widget.bind('<FocusOut>', 
            lambda e: self.save_inline_edit(go_next=False))
        
        # Real-time tag validation
        self.current_edit_widget.bind('<KeyRelease>', 
            self.validate_tags_inline)
        
        self.log("Edit mode: Press Enter to save, Ctrl+Enter for save & next, Escape to cancel")
    
    def save_inline_edit(self, go_next=False):
        """Save inline edit and optionally move to next"""
        if not self.current_edit_widget:
            return
        
        # Get edited text
        new_text = self.current_edit_widget.get()
        
        # Validate tags
        if self.tag_manager and new_text:
            is_valid, error = self.tag_manager.validate_tags(new_text)
            if not is_valid:
                messagebox.showerror("Tag Error", error)
                self.current_edit_widget.focus()
                return
        
        # Save to segment
        if self.current_segment:
            self.current_segment.target = new_text
            if new_text and self.current_segment.status == 'untranslated':
                self.current_segment.status = 'translated'
            self.current_segment.modified = True
            self.current_segment.modified_at = datetime.now().isoformat()
            
            # Update grid
            self.update_segment_in_grid(self.current_segment)
            
            self.modified = True
            self.update_progress()
            self.log(f"Segment #{self.current_segment.id} saved")
        
        # Destroy edit widget
        self.current_edit_widget.destroy()
        self.current_edit_widget = None
        
        # Clear validation label
        self.tag_validation_label.config(text="")
        
        # Move to next if requested
        if go_next:
            self.next_segment()
    
    def cancel_inline_edit(self):
        """Cancel inline editing without saving"""
        if self.current_edit_widget:
            self.current_edit_widget.destroy()
            self.current_edit_widget = None
            self.tag_validation_label.config(text="")
            self.log("Edit cancelled")
    
    def validate_tags_inline(self, event=None):
        """Validate tags in real-time during inline editing"""
        if not self.current_edit_widget or not self.tag_manager:
            return
        
        text = self.current_edit_widget.get()
        if not text:
            self.tag_validation_label.config(text="", fg='#666')
            return
        
        is_valid, error = self.tag_manager.validate_tags(text)
        if is_valid:
            self.tag_validation_label.config(text="✓ Tags valid", fg='green')
        else:
            self.tag_validation_label.config(text=f"✗ {error}", fg='red')
    
    def insert_tag_inline(self, tag_type):
        """Insert tag at cursor position in inline editor"""
        if self.current_edit_widget:
            # Insert in the edit widget
            pos = self.current_edit_widget.index(tk.INSERT)
            opening = f"<{tag_type}>"
            closing = f"</{tag_type}>"
            self.current_edit_widget.insert(pos, opening + closing)
            # Move cursor between tags
            self.current_edit_widget.icursor(pos + len(opening))
            self.current_edit_widget.focus()
    
    def clear_target_inline(self):
        """Clear target of currently selected segment"""
        if self.current_segment:
            self.current_segment.target = ""
            self.current_segment.status = "untranslated"
            self.update_segment_in_grid(self.current_segment)
            self.modified = True
            self.update_progress()
            self.log(f"Segment #{self.current_segment.id} target cleared")
    
    def set_status_inline(self, status):
        """Set status of currently selected segment"""
        if self.current_segment:
            self.current_segment.status = status
            self.update_segment_in_grid(self.current_segment)
            self.modified = True
            self.log(f"Segment #{self.current_segment.id} marked as {status}")
    
    def next_segment(self):
        """Move to next segment"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Get next item
        item = selection[0]
        next_item = self.tree.next(item)
        
        if next_item:
            self.tree.selection_set(next_item)
            self.tree.see(next_item)
            self.tree.focus(next_item)
            
            # If in Grid mode, could auto-enter edit mode
            if self.layout_mode == LayoutMode.GRID:
                # Small delay to allow selection to update
                self.root.after(100, self.enter_edit_mode)
    
    def navigate_segment(self, direction='next'):
        """Navigate to next or previous segment"""
        selection = self.tree.selection()
        if not selection:
            # No selection, select first item
            children = self.tree.get_children()
            if children:
                self.tree.selection_set(children[0])
                self.tree.see(children[0])
                self.tree.focus(children[0])
            return
        
        item = selection[0]
        
        if direction == 'next':
            next_item = self.tree.next(item)
            if next_item:
                self.tree.selection_set(next_item)
                self.tree.see(next_item)
                self.tree.focus(next_item)
        elif direction == 'prev':
            prev_item = self.tree.prev(item)
            if prev_item:
                self.tree.selection_set(prev_item)
                self.tree.see(prev_item)
                self.tree.focus(prev_item)
    
    def show_source_popup(self, event):
        """Show source text in a popup for easy reading/copying"""
        if not self.current_segment:
            return
        
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"Source - Segment #{self.current_segment.id}")
        popup.geometry("600x300")
        popup.transient(self.root)
        
        # Position near cursor
        popup.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        # Add text widget
        text_frame = tk.Frame(popup, padx=10, pady=10)
        text_frame.pack(fill='both', expand=True)
        
        tk.Label(text_frame, text="Source Text (Read-only, select to copy)", 
                font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(0, 5))
        
        text_widget = scrolledtext.ScrolledText(text_frame, wrap='word', 
                                                font=('Segoe UI', 10),
                                                bg='#f5f5f5')
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', self.current_segment.source)
        text_widget.config(state='normal')  # Allow selection for copying
        
        # Button frame
        btn_frame = tk.Frame(popup, padx=10, pady=5)
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text="Copy to Clipboard", 
                 command=lambda: self.copy_to_clipboard(self.current_segment.source, popup),
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Copy to Target", 
                 command=lambda: [self.copy_source_to_target(), popup.destroy()],
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Close", 
                 command=popup.destroy).pack(side='right', padx=5)
        
        # Auto-select all text for easy copying
        text_widget.tag_add('sel', '1.0', 'end')
        text_widget.focus()
        
        # Close on Escape
        popup.bind('<Escape>', lambda e: popup.destroy())
    
    def copy_to_clipboard(self, text, popup=None):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.log("✓ Copied to clipboard")
        if popup:
            popup.destroy()
    
    def import_docx(self):
        """Import a DOCX file"""
        file_path = filedialog.askopenfilename(
            title="Select DOCX file",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.log(f"Importing: {os.path.basename(file_path)}")
            
            # Import DOCX
            paragraphs = self.docx_handler.import_docx(file_path)
            self.original_docx = file_path
            
            # Segment paragraphs
            self.log("Segmenting text...")
            segmented = self.segmenter.segment_paragraphs(paragraphs)
            
            # Create segments with table and style information
            self.segments = []
            for seg_id, (para_id, text) in enumerate(segmented, 1):
                # Get paragraph info to check if it's a table cell and get style
                para_info = self.docx_handler._get_para_info(para_id)
                
                is_table = False
                table_info = None
                style = "Normal"  # Default style
                
                if para_info:
                    # Get style information
                    style = para_info.style or "Normal"
                    
                    # Get table information
                    if para_info.is_table_cell:
                        is_table = True
                        table_info = (para_info.table_index, para_info.row_index, para_info.cell_index)
                
                segment = Segment(seg_id, text, para_id, is_table, table_info, style)
                self.segments.append(segment)
            
            # Load into grid
            self.load_segments_to_grid()
            
            # Update status
            self.log(f"✓ Loaded {len(self.segments)} segments from {len(paragraphs)} paragraphs")
            self.update_progress()
            self.modified = False
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import DOCX:\n{str(e)}")
            self.log(f"✗ Import failed: {str(e)}")
    
    def load_segments_to_grid(self):
        """Load segments into the treeview grid"""
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add segments
        for seg in self.segments:
            # Determine type label
            if seg.is_table_cell and seg.table_info:
                type_label = f"T{seg.table_info[0]+1}R{seg.table_info[1]+1}C{seg.table_info[2]+1}"
            else:
                type_label = "Para"
            
            # Format style name for display
            style_display = self._format_style_name(seg.style)
            
            # Set tags for styling
            tags = [seg.status]
            if seg.is_table_cell:
                tags.append('table_cell')
            
            # Add style-specific tag for visual formatting
            style_tag = self._get_style_tag(seg.style)
            if style_tag:
                tags.append(style_tag)
            
            # Different column layouts for different modes
            if self.layout_mode == LayoutMode.GRID or self.layout_mode == LayoutMode.COMPACT:
                # Grid/Compact: No style column (5 columns)
                self.tree.insert('', 'end',
                               values=(seg.id, type_label, seg.status.capitalize(),
                                      self._truncate(seg.source, 100),
                                      self._truncate(seg.target, 100)),
                               tags=tuple(tags))
            else:
                # Split: Include style column (6 columns)
                self.tree.insert('', 'end',
                               values=(seg.id, type_label, style_display, seg.status.capitalize(),
                                      self._truncate(seg.source, 75),
                                      self._truncate(seg.target, 75)),
                               tags=tuple(tags))
    
    def _truncate(self, text: str, length: int) -> str:
        """Truncate text for display"""
        if len(text) <= length:
            return text
        return text[:length-3] + "..."
    
    def _format_style_name(self, style: str) -> str:
        """Format style name for display in grid"""
        if not style or style == "Normal":
            return "Normal"
        # Shorten common styles for better display
        style = style.replace("Heading", "H").replace("heading", "H")
        # Limit length
        if len(style) > 12:
            return style[:12]
        return style
    
    def _get_style_tag(self, style: str) -> str:
        """Get treeview tag for style-specific formatting"""
        if not style:
            return None
        style_lower = style.lower()
        if 'heading 1' in style_lower or style_lower == 'heading1':
            return 'heading1'
        elif 'heading 2' in style_lower or style_lower == 'heading2':
            return 'heading2'
        elif 'heading 3' in style_lower or style_lower == 'heading3':
            return 'heading3'
        elif 'title' in style_lower and 'sub' not in style_lower:
            return 'title'
        elif 'subtitle' in style_lower:
            return 'subtitle'
        return None
    
    def on_segment_select(self, event):
        """Handle segment selection in grid"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Save current segment first
        if self.current_segment:
            self.save_current_segment()
        
        # Get selected segment
        item = selection[0]
        values = self.tree.item(item, 'values')
        seg_id = int(values[0])
        
        # Find segment
        self.current_segment = next((s for s in self.segments if s.id == seg_id), None)
        
        if self.current_segment:
            self.load_segment_to_editor(self.current_segment)
    
    def load_segment_to_editor(self, segment: Segment):
        """Load segment into editor panel"""
        self.seg_info_label.config(text=f"Segment #{segment.id} | Paragraph {segment.paragraph_id}")
        
        # Source
        self.source_text.config(state='normal')
        self.source_text.delete('1.0', 'end')
        self.source_text.insert('1.0', segment.source)
        self.source_text.config(state='disabled')
        
        # Target
        self.target_text.delete('1.0', 'end')
        if segment.target:
            self.target_text.insert('1.0', segment.target)
        
        # Status
        self.status_var.set(segment.status)
        
        # Focus target
        self.target_text.focus_set()
    
    def save_current_segment(self):
        """Save current segment from editor"""
        if not self.current_segment:
            return
        
        # Get values
        target = self.target_text.get('1.0', 'end-1c').strip()
        status = self.status_var.get()
        
        # Update segment
        if target != self.current_segment.target or status != self.current_segment.status:
            self.current_segment.target = target
            self.current_segment.status = status
            self.current_segment.modified = True
            self.current_segment.modified_at = datetime.now().isoformat()
            self.modified = True
            
            # Update grid
            self.update_segment_in_grid(self.current_segment)
            self.update_progress()
    
    def update_segment_in_grid(self, segment: Segment):
        """Update segment display in grid"""
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if int(values[0]) == segment.id:
                # Determine type label
                if segment.is_table_cell and segment.table_info:
                    type_label = f"T{segment.table_info[0]+1}R{segment.table_info[1]+1}C{segment.table_info[2]+1}"
                else:
                    type_label = "Para"
                
                # Format style name
                style_display = self._format_style_name(segment.style)
                
                # Set tags for styling
                tags = [segment.status]
                if segment.is_table_cell:
                    tags.append('table_cell')
                style_tag = self._get_style_tag(segment.style)
                if style_tag:
                    tags.append(style_tag)
                
                # Different column layouts for different modes
                if self.layout_mode == LayoutMode.GRID or self.layout_mode == LayoutMode.COMPACT:
                    # Grid/Compact: No style column (5 columns)
                    self.tree.item(item,
                                 values=(segment.id, type_label, segment.status.capitalize(),
                                        self._truncate(segment.source, 100),
                                        self._truncate(segment.target, 100)),
                                 tags=tuple(tags))
                else:
                    # Split: Include style column (6 columns)
                    self.tree.item(item,
                                 values=(segment.id, type_label, style_display, segment.status.capitalize(),
                                        self._truncate(segment.source, 75),
                                        self._truncate(segment.target, 75)),
                                 tags=tuple(tags))
                break
    
    def on_status_change(self, event):
        """Handle status change"""
        self.save_current_segment()
    
    def on_target_change(self, event):
        """Handle target text change - validate tags"""
        target = self.target_text.get('1.0', 'end-1c')
        
        # Validate tags
        is_valid, error_msg = self.tag_manager.validate_tags(target)
        
        if not is_valid:
            self.tag_validation_label.config(text=f"⚠️ {error_msg}", fg='red')
        else:
            # Count tags
            tag_counts = self.tag_manager.count_tags(target)
            if tag_counts:
                tag_text = ', '.join([f"{count} {tag}" for tag, count in tag_counts.items()])
                self.tag_validation_label.config(text=f"✓ Tags: {tag_text}", fg='green')
            else:
                self.tag_validation_label.config(text="", fg='black')
    
    def insert_tag(self, tag_name: str):
        """Insert formatting tag at cursor position"""
        try:
            # Get current selection or cursor position
            try:
                start = self.target_text.index('sel.first')
                end = self.target_text.index('sel.last')
                selected_text = self.target_text.get(start, end)
                
                # Wrap selection in tags
                tagged_text = f"<{tag_name}>{selected_text}</{tag_name}>"
                self.target_text.delete(start, end)
                self.target_text.insert(start, tagged_text)
            except tk.TclError:
                # No selection, insert empty tags at cursor
                cursor_pos = self.target_text.index('insert')
                self.target_text.insert(cursor_pos, f"<{tag_name}></{tag_name}>")
                # Move cursor between tags
                self.target_text.mark_set('insert', f"{cursor_pos}+{len(tag_name)+2}c")
            
            self.target_text.focus_set()
            # Trigger validation
            self.on_target_change(None)
        except Exception as e:
            self.log(f"Error inserting tag: {str(e)}")
    
    def strip_tags_from_target(self):
        """Remove all formatting tags from target"""
        if not self.current_segment:
            return
        
        target = self.target_text.get('1.0', 'end-1c')
        clean_text = self.tag_manager.strip_tags(target)
        
        self.target_text.delete('1.0', 'end')
        self.target_text.insert('1.0', clean_text)
        self.on_target_change(None)
    
    def copy_source_tags(self):
        """Copy tag structure from source to target"""
        if not self.current_segment:
            return
        
        source = self.current_segment.source
        target = self.target_text.get('1.0', 'end-1c')
        
        # Extract tag positions from source
        source_tags = self.tag_manager.count_tags(source)
        
        if not source_tags:
            messagebox.showinfo("No Tags", "Source segment has no formatting tags.")
            return
        
        # If target is empty, copy source structure
        if not target.strip():
            self.target_text.delete('1.0', 'end')
            self.target_text.insert('1.0', source)
            messagebox.showinfo("Tags Copied", "Source formatting structure copied to target. Now translate the text.")
        else:
            messagebox.showinfo("Tag Structure", 
                              f"Source has: {', '.join([f'{c} {t}' for t, c in source_tags.items()])}\n\n"
                              "Use the Insert buttons to add matching tags to your translation.")
        
        self.on_target_change(None)
    
    def copy_source_to_target(self):
        """Copy source to target - works in both Grid and Split modes"""
        if not self.current_segment:
            self.log("⚠️ No segment selected")
            return
        
        # Update the segment
        self.current_segment.target = self.current_segment.source
        if self.current_segment.status == 'untranslated':
            self.current_segment.status = 'draft'
        self.current_segment.modified = True
        
        # Update UI based on mode
        if self.layout_mode == LayoutMode.GRID:
            # In Grid mode, update the grid directly
            self.update_segment_in_grid(self.current_segment)
            
            # If currently editing, update the edit widget
            if self.current_edit_widget:
                self.current_edit_widget.delete(0, tk.END)
                self.current_edit_widget.insert(0, self.current_segment.source)
        else:
            # In Split mode, update the target text widget
            if hasattr(self, 'target_text'):
                self.target_text.delete('1.0', 'end')
                self.target_text.insert('1.0', self.current_segment.source)
        
        self.modified = True
        self.update_progress()
        self.log(f"✓ Copied source to target (Segment #{self.current_segment.id})")
    
    def clear_target(self):
        """Clear target text"""
        if hasattr(self, 'target_text'):
            self.target_text.delete('1.0', 'end')
    
    def save_segment_and_next(self):
        """Save current segment and move to next"""
        self.save_current_segment()
        
        # Select next segment
        selection = self.tree.selection()
        if selection:
            current_item = selection[0]
            next_item = self.tree.next(current_item)
            if next_item:
                self.tree.selection_set(next_item)
                self.tree.see(next_item)
    
    def focus_target_editor(self):
        """Focus the target text editor"""
        self.target_text.focus_set()
    
    def update_progress(self):
        """Update progress label"""
        if not self.segments:
            self.progress_label.config(text="No document loaded")
            return
        
        total = len(self.segments)
        translated = sum(1 for s in self.segments if s.status in ['translated', 'approved'])
        percentage = (translated / total * 100) if total > 0 else 0
        
        self.progress_label.config(
            text=f"Progress: {translated}/{total} ({percentage:.1f}%) | "
                 f"{'Modified' if self.modified else 'Saved'}"
        )
    
    def save_project(self):
        """Save project to JSON"""
        if not self.project_file:
            self.save_project_as()
            return
        
        self.save_current_segment()
        
        try:
            data = {
                'version': '0.3.2',
                'created_at': datetime.now().isoformat(),
                'original_docx': self.original_docx,
                'segments': [s.to_dict() for s in self.segments]
            }
            
            with open(self.project_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.modified = False
            self.log(f"✓ Project saved: {os.path.basename(self.project_file)}")
            self.update_progress()
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save project:\n{str(e)}")
    
    def save_project_as(self):
        """Save project as new file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Project As",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.project_file = file_path
            self.save_project()
    
    def load_project(self):
        """Load project from JSON"""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "Save current project before loading?"
            )
            if response is True:
                self.save_project()
            elif response is None:
                return
        
        file_path = filedialog.askopenfilename(
            title="Load Project",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load segments
            self.segments = [Segment.from_dict(s) for s in data['segments']]
            self.original_docx = data.get('original_docx')
            self.project_file = file_path
            
            # If original DOCX exists, load it for export
            if self.original_docx and os.path.exists(self.original_docx):
                self.docx_handler.import_docx(self.original_docx)
            
            # Load to grid
            self.load_segments_to_grid()
            
            self.modified = False
            self.log(f"✓ Project loaded: {os.path.basename(file_path)}")
            self.update_progress()
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load project:\n{str(e)}")
    
    def export_docx(self):
        """Export to translated DOCX"""
        if not self.segments:
            messagebox.showwarning("No Data", "No segments to export")
            return
        
        if not self.original_docx or not os.path.exists(self.original_docx):
            messagebox.showerror("No Original",
                               "Original DOCX file not found. Cannot export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export to DOCX",
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.save_current_segment()
            
            # Prepare segments for export
            seg_dicts = [s.to_dict() for s in self.segments]
            
            # Export
            self.docx_handler.export_docx(seg_dicts, file_path)
            
            self.log(f"✓ Exported to DOCX: {os.path.basename(file_path)}")
            messagebox.showinfo("Export Complete",
                              f"Document exported successfully to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export DOCX:\n{str(e)}")
            self.log(f"✗ Export failed: {str(e)}")
    
    def export_bilingual_docx(self):
        """Export to bilingual DOCX (table format)"""
        if not self.segments:
            messagebox.showwarning("No Data", "No segments to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export to Bilingual DOCX",
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.save_current_segment()
            seg_dicts = [s.to_dict() for s in self.segments]
            self.docx_handler.export_bilingual_docx(seg_dicts, file_path)
            
            self.log(f"✓ Exported bilingual DOCX: {os.path.basename(file_path)}")
            messagebox.showinfo("Export Complete", "Bilingual document exported successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")
    
    def export_tsv(self):
        """Export to TSV (tab-separated values)"""
        if not self.segments:
            messagebox.showwarning("No Data", "No segments to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export to TSV",
            defaultextension=".tsv",
            filetypes=[("TSV Files", "*.tsv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.save_current_segment()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                # Header
                f.write("ID\tStatus\tSource\tTarget\tParagraph\tNotes\n")
                
                # Data
                for seg in self.segments:
                    f.write(f"{seg.id}\t{seg.status}\t{seg.source}\t{seg.target}\t"
                           f"{seg.paragraph_id}\t{seg.notes}\n")
            
            self.log(f"✓ Exported to TSV: {os.path.basename(file_path)}")
            messagebox.showinfo("Export Complete", "TSV file exported successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export TSV:\n{str(e)}")
    
    def show_find_replace(self):
        """Show find/replace dialog"""
        FindReplaceDialog(self.root, self)
    
    def on_closing(self):
        """Handle window closing"""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "Save project before closing?"
            )
            if response is True:
                self.save_project()
                self.root.destroy()
            elif response is False:
                self.root.destroy()
        else:
            self.root.destroy()


class FindReplaceDialog:
    """Find and replace dialog"""
    
    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Find and Replace")
        self.window.geometry("500x250")
        self.window.transient(parent)
        
        # Find
        tk.Label(self.window, text="Find:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=10, pady=(10,2))
        self.find_var = tk.StringVar()
        tk.Entry(self.window, textvariable=self.find_var, width=60).pack(padx=10, pady=2)
        
        # Replace
        tk.Label(self.window, text="Replace with:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=10, pady=(10,2))
        self.replace_var = tk.StringVar()
        tk.Entry(self.window, textvariable=self.replace_var, width=60).pack(padx=10, pady=2)
        
        # Options
        options_frame = tk.Frame(self.window)
        options_frame.pack(pady=10)
        
        self.match_case_var = tk.BooleanVar()
        tk.Checkbutton(options_frame, text="Match case", variable=self.match_case_var).pack(side='left', padx=5)
        
        self.search_in_var = tk.StringVar(value="target")
        tk.Label(options_frame, text="Search in:").pack(side='left', padx=(20,5))
        ttk.Combobox(options_frame, textvariable=self.search_in_var,
                    values=["source", "target", "both"], state='readonly', width=10).pack(side='left')
        
        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Find Next", command=self.find_next, width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Replace", command=self.replace_current, width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Replace All", command=self.replace_all, width=12,
                 bg='#FF9800', fg='white').pack(side='left', padx=5)
        
        # Results
        self.result_label = tk.Label(self.window, text="", fg='blue')
        self.result_label.pack(pady=5)
        
        self.current_match_index = -1
        self.matches = []
    
    def find_next(self):
        """Find next occurrence"""
        query = self.find_var.get()
        if not query:
            self.result_label.config(text="Please enter search text")
            return
        
        search_in = self.search_in_var.get()
        case_sensitive = self.match_case_var.get()
        
        # Search segments
        self.matches = []
        for seg in self.app.segments:
            source = seg.source if case_sensitive else seg.source.lower()
            target = seg.target if case_sensitive else seg.target.lower()
            query_cmp = query if case_sensitive else query.lower()
            
            found = False
            if search_in in ['source', 'both'] and query_cmp in source:
                found = True
            if search_in in ['target', 'both'] and query_cmp in target:
                found = True
            
            if found:
                self.matches.append(seg.id)
        
        if not self.matches:
            self.result_label.config(text="No matches found")
            return
        
        # Move to next match
        self.current_match_index = (self.current_match_index + 1) % len(self.matches)
        match_id = self.matches[self.current_match_index]
        
        # Select in grid
        for item in self.app.tree.get_children():
            values = self.app.tree.item(item, 'values')
            if int(values[0]) == match_id:
                self.app.tree.selection_set(item)
                self.app.tree.see(item)
                break
        
        self.result_label.config(
            text=f"Match {self.current_match_index + 1} of {len(self.matches)}"
        )
    
    def replace_current(self):
        """Replace current match"""
        if not self.app.current_segment:
            self.result_label.config(text="No segment selected")
            return
        
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        
        if not find_text:
            return
        
        # Replace in target
        if self.match_case_var.get():
            new_target = self.app.current_segment.target.replace(find_text, replace_text)
        else:
            import re
            new_target = re.sub(re.escape(find_text), replace_text,
                              self.app.current_segment.target, flags=re.IGNORECASE)
        
        # Update
        self.app.target_text.delete('1.0', 'end')
        self.app.target_text.insert('1.0', new_target)
        self.app.save_current_segment()
        
        self.result_label.config(text="Replaced")
    
    def replace_all(self):
        """Replace all occurrences"""
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        
        if not find_text:
            return
        
        search_in = self.search_in_var.get()
        count = 0
        
        for seg in self.app.segments:
            if search_in in ['target', 'both']:
                if self.match_case_var.get():
                    if find_text in seg.target:
                        seg.target = seg.target.replace(find_text, replace_text)
                        count += 1
                else:
                    import re
                    if re.search(re.escape(find_text), seg.target, re.IGNORECASE):
                        seg.target = re.sub(re.escape(find_text), replace_text,
                                          seg.target, flags=re.IGNORECASE)
                        count += 1
        
        # Refresh grid
        self.app.load_segments_to_grid()
        self.app.modified = True
        self.app.update_progress()
        
        self.result_label.config(text=f"Replaced {count} occurrences")


# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = CATEditorPrototype(root)
    root.mainloop()
