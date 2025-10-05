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

Author: Supervertaler Project (Michael Beijer + Claude)
Date: October 1, 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import re
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
    SPLIT = "split"    # List view with editor panel
    DOCUMENT = "document" # Document flow view with clickable segments


class Segment:
    """Represents a translation segment"""
    
    def __init__(self, seg_id: int, source: str, paragraph_id: int = 0, 
                 is_table_cell: bool = False, table_info: tuple = None,
                 style: str = None, document_position: int = 0):
        self.id = seg_id
        self.source = source
        self.target = ""
        self.status = "untranslated"  # untranslated, draft, translated, approved
        self.paragraph_id = paragraph_id
        self.document_position = document_position  # Position in original document
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
            'document_position': self.document_position,
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
                  data.get('style', 'Normal'), data.get('document_position', 0))
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
        
        # Filter state
        self.filtered_segments = []
        self.filter_active = False
        
        # Components
        self.segmenter = SimpleSegmenter()
        self.docx_handler = DOCXHandler()
        self.tag_manager = TagManager()
        
        # Setup UI
        self.setup_ui()
        
        # Status
        self.log("CAT Editor ready. Import a DOCX file to begin.")
        self.log("✨ Layout modes available: Grid (memoQ-style), List, Document")
    
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
        file_menu.add_command(label="Open Project...", command=self.load_project, accelerator="Ctrl+L")
        file_menu.add_command(label="Close Project", command=self.close_project)
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
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Grid View", command=lambda: self.switch_layout(LayoutMode.GRID), accelerator="Ctrl+1")
        view_menu.add_command(label="List View", command=lambda: self.switch_layout(LayoutMode.SPLIT), accelerator="Ctrl+2")
        view_menu.add_command(label="Document View", command=lambda: self.switch_layout(LayoutMode.DOCUMENT), accelerator="Ctrl+3")
        view_menu.add_separator()
        view_menu.add_command(label="Grid Columns...", command=self.show_column_visibility_dialog)
        view_menu.add_command(label="Toggle Style Colors", command=self.toggle_grid_style_colors)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Filter Mode", command=self.toggle_filter_mode, accelerator="Ctrl+M")
        view_menu.add_command(label="Apply Filters", command=self.apply_filters, accelerator="Ctrl+Shift+A")
        view_menu.add_command(label="Clear Filters", command=self.clear_filters)
        view_menu.add_command(label="Focus Filter", command=self.focus_filter_source, accelerator="Ctrl+Shift+F")
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.import_docx())
        self.root.bind('<Control-s>', lambda e: self.save_project())
        self.root.bind('<Control-l>', lambda e: self.load_project())
        self.root.bind('<Control-f>', lambda e: self.show_find_replace())
        self.root.bind('<Control-d>', lambda e: self.copy_source_to_target())
        
        # Layout switching shortcuts
        self.root.bind('<Control-Key-1>', lambda e: self.switch_layout(LayoutMode.GRID))
        self.root.bind('<Control-Key-2>', lambda e: self.switch_layout(LayoutMode.SPLIT))
        self.root.bind('<Control-Key-3>', lambda e: self.switch_layout(LayoutMode.DOCUMENT))
        
        # Filter shortcuts
        self.root.bind('<Control-m>', lambda e: self.toggle_filter_mode())  # Toggle filter mode
        self.root.bind('<Control-Shift-F>', lambda e: self.focus_filter_source())  # Focus source filter
        self.root.bind('<Control-Shift-A>', lambda e: self.apply_filters())  # Apply filters
        
        # Navigation shortcuts
        self.root.bind('<Control-Down>', lambda e: self.navigate_segment('next'))
        self.root.bind('<Control-Up>', lambda e: self.navigate_segment('prev'))
        
        # Grid View display options
        self.grid_style_colors_enabled = True  # Toggle for style-based font colors
        
        # Dual text selection state (for Grid View)
        self.dual_selection_row = None  # Currently active row index
        self.dual_selection_source = None  # Source Text widget with selection
        self.dual_selection_target = None  # Target Text widget with selection
        self.dual_selection_focused_widget = None  # 'source' or 'target' for keyboard selection
        self.dual_selection_source_cursor = None  # Remember cursor position in source
        self.dual_selection_target_cursor = None  # Remember cursor position in target
        
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
        
        self.layout_btn_split = tk.Button(self.toolbar, text="📋 List View",
                                          command=lambda: self.switch_layout(LayoutMode.SPLIT),
                                          padx=10, relief='raised')
        self.layout_btn_split.pack(side='left', padx=2)
        
        self.layout_btn_document = tk.Button(self.toolbar, text="📖 Document View",
                                             command=lambda: self.switch_layout(LayoutMode.DOCUMENT),
                                             padx=10, relief='raised')
        self.layout_btn_document.pack(side='left', padx=2)
        
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
        elif self.layout_mode == LayoutMode.DOCUMENT:
            self.create_document_layout()
    
    def create_grid_layout(self):
        """Create Grid View layout (memoQ-style with inline editing and dynamic row heights)"""
        
        # Create main horizontal paned window (grid on left, assistance panel on right)
        self.main_paned = ttk.PanedWindow(self.content_frame, orient='horizontal')
        self.main_paned.pack(fill='both', expand=True)
        
        # Left side: Grid and editor
        left_container = tk.Frame(self.main_paned)
        self.main_paned.add(left_container, weight=3)
        
        # Grid frame (top part - expandable)
        grid_frame = tk.LabelFrame(left_container, text="Translation Grid - Grid View (Click target to edit)", padx=5, pady=5)
        grid_frame.pack(side='top', fill='both', expand=True)
        
        # Filter panel (above the grid header)
        filter_frame = tk.Frame(grid_frame, bg='#f0f0f0', relief='ridge', borderwidth=1)
        filter_frame.pack(side='top', fill='x', pady=(0, 5))
        
        # Filter label
        tk.Label(filter_frame, text="🔍 Filter:", bg='#f0f0f0', 
                font=('Segoe UI', 9, 'bold')).pack(side='left', padx=5, pady=5)
        
        # Filter mode selection (radio-style buttons)
        self.filter_mode = 'filter'  # 'filter' or 'highlight'
        
        mode_frame = tk.Frame(filter_frame, bg='#f0f0f0', relief='solid', bd=1)
        mode_frame.pack(side='left', padx=5)
        
        self.filter_mode_btn = tk.Button(mode_frame, text="� Filter",
                                        command=lambda: self.set_filter_mode('filter'),
                                        bg='#4CAF50', fg='white', font=('Segoe UI', 9, 'bold'),
                                        relief='sunken', bd=2, cursor='hand2', width=10)
        self.filter_mode_btn.pack(side='left', padx=1, pady=1)
        
        self.highlight_mode_btn = tk.Button(mode_frame, text="💡 Highlight",
                                            command=lambda: self.set_filter_mode('highlight'),
                                            bg='#e0e0e0', fg='#666', font=('Segoe UI', 9),
                                            relief='raised', bd=2, cursor='hand2', width=10)
        self.highlight_mode_btn.pack(side='left', padx=1, pady=1)
        
        tk.Label(filter_frame, text="│", bg='#f0f0f0', fg='#ccc',
                font=('Segoe UI', 10)).pack(side='left', padx=5)
        
        # Source filter
        tk.Label(filter_frame, text="Source:", bg='#f0f0f0', 
                font=('Segoe UI', 9)).pack(side='left', padx=(10, 2))
        self.filter_source_var = tk.StringVar()
        source_filter_entry = tk.Entry(filter_frame, textvariable=self.filter_source_var,
                                      font=('Segoe UI', 9), width=25, relief='solid', borderwidth=1)
        source_filter_entry.pack(side='left', padx=2, pady=3)
        # Bind Enter key to apply filters
        source_filter_entry.bind('<Return>', lambda e: self.apply_filters())
        
        # Target filter
        tk.Label(filter_frame, text="Target:", bg='#f0f0f0', 
                font=('Segoe UI', 9)).pack(side='left', padx=(10, 2))
        self.filter_target_var = tk.StringVar()
        target_filter_entry = tk.Entry(filter_frame, textvariable=self.filter_target_var,
                                      font=('Segoe UI', 9), width=25, relief='solid', borderwidth=1)
        target_filter_entry.pack(side='left', padx=2, pady=3)
        # Bind Enter key to apply filters
        target_filter_entry.bind('<Return>', lambda e: self.apply_filters())
        
        # Status filter
        tk.Label(filter_frame, text="Status:", bg='#f0f0f0', 
                font=('Segoe UI', 9)).pack(side='left', padx=(10, 2))
        self.filter_status_var = tk.StringVar(value="All")
        status_filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_status_var,
                                          values=["All", "untranslated", "draft", "translated", "approved"],
                                          state='readonly', width=12, font=('Segoe UI', 9))
        status_filter_combo.pack(side='left', padx=2, pady=3)
        # Combobox selection triggers apply automatically (user expectation for dropdowns)
        status_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Apply filters button
        tk.Button(filter_frame, text="🔍 Apply", command=self.apply_filters,
                 bg='#2196F3', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief='raised', padx=10, pady=2, cursor='hand2').pack(side='left', padx=5)
        
        # Clear filters button
        tk.Button(filter_frame, text="✕ Clear", command=self.clear_filters,
                 bg='#ff9800', fg='white', font=('Segoe UI', 8),
                 relief='flat', padx=8, pady=2).pack(side='left', padx=5)
        
        # Filter results label
        self.filter_results_label = tk.Label(filter_frame, text="", bg='#f0f0f0',
                                            font=('Segoe UI', 9), fg='#666')
        self.filter_results_label.pack(side='left', padx=10)
        
        # Column configuration with adjustable source/target widths
        self.fixed_columns_width = 200  # ID + Type + Status combined
        self.source_width = 450  # Initial source width
        self.target_width = 450  # Initial target width
        self.dragging_splitter = False
        
        self.grid_columns = {
            'id': {'title': '#', 'width': 40, 'anchor': 'center', 'visible': True},
            'type': {'title': 'Type', 'width': 65, 'anchor': 'center', 'visible': True},
            'style': {'title': 'Style', 'width': 100, 'anchor': 'center', 'visible': True},
            'status': {'title': 'Status', 'width': 95, 'anchor': 'center', 'visible': True},
            'source': {'title': '📄 Source', 'width': self.source_width, 'anchor': 'w', 'visible': True},
            'target': {'title': '🎯 Target', 'width': self.target_width, 'anchor': 'w', 'visible': True}
        }
        
        # Initialize filter state
        self.filtered_segments = []
        self.filter_active = False
        
        # Create STICKY header row (outside canvas, fixed at top)
        self.header_container = tk.Frame(grid_frame, bg='white')
        self.header_container.pack(side='top', fill='x')
        self.create_grid_header()
        
        # Create scrollable content area
        content_area = tk.Frame(grid_frame, bg='white')
        content_area.pack(side='top', fill='both', expand=True)
        
        # Create custom grid canvas for rows
        self.grid_canvas = tk.Canvas(content_area, bg='white', highlightthickness=0)
        self.grid_canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(content_area, orient='vertical', command=self.grid_canvas.yview)
        h_scroll = ttk.Scrollbar(content_area, orient='horizontal', command=self.grid_canvas.xview)
        self.grid_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        
        # Create a frame inside canvas to hold all rows
        self.grid_inner_frame = tk.Frame(self.grid_canvas, bg='white')
        self.canvas_window = self.grid_canvas.create_window((0, 0), window=self.grid_inner_frame, anchor='nw')
        
        # Storage for row widgets
        self.grid_rows = []  # List of row data: {'segment': seg, 'widgets': {...}, 'row_frame': frame}
        self.current_row_index = -1
        
        # Bind canvas resize to update scroll region
        self.grid_inner_frame.bind('<Configure>', self.update_grid_scroll_region)
        self.grid_canvas.bind('<Configure>', self.on_grid_canvas_resize)
        
        # Keyboard bindings on canvas
        self.grid_canvas.bind('<Double-1>', self.on_grid_double_click)
        self.grid_canvas.bind('<Button-1>', self.on_grid_click)
        self.grid_canvas.bind('<F2>', self.enter_edit_mode)
        self.grid_canvas.bind('<Return>', lambda e: self.enter_edit_mode())
        self.grid_canvas.bind('<Control-d>', lambda e: self.copy_source_to_target())
        
        # Mouse wheel scrolling
        self.grid_canvas.bind('<MouseWheel>', self.on_grid_mousewheel)
        
        # Context menu
        self.create_context_menu()
        self.grid_canvas.bind('<Button-3>', self.show_grid_context_menu)
        
        # Focus the canvas so keyboard events work
        self.grid_canvas.focus_set()
        
        # Store reference to container for editor panel
        self.grid_left_container = left_container
        
        # Editor panel at bottom (hideable)
        self.grid_editor_visible = True
        self.create_grid_editor_panel()
        
        # Right side: Assistance panel (MT, TM, Glossary, etc.)
        self.create_assistance_panel()
    
    def create_grid_editor_panel(self):
        """Create the editor panel for Grid View"""
        # Toggle button above the editor panel
        toggle_btn_frame = tk.Frame(self.grid_left_container, bg='#f0f0f0')
        toggle_btn_frame.pack(side='bottom', fill='x', pady=(2, 0))
        
        self.grid_editor_toggle_btn = tk.Button(toggle_btn_frame, 
                                               text="🔽 Hide Editor Panel", 
                                               command=self.toggle_grid_editor,
                                               font=('Segoe UI', 9),
                                               relief='raised',
                                               bg='#4CAF50',
                                               fg='white',
                                               padx=10,
                                               pady=2)
        self.grid_editor_toggle_btn.pack(side='left', padx=5, pady=2)
        
        # Editor frame (bottom part)
        self.grid_editor_frame = tk.LabelFrame(self.grid_left_container, text="Segment Editor", padx=10, pady=10)
        self.grid_editor_frame.pack(side='bottom', fill='x', pady=(0, 0))
        
        # Segment info and status on same row
        info_frame = tk.Frame(self.grid_editor_frame)
        info_frame.pack(fill='x', pady=(0, 5))
        
        self.grid_seg_info_label = tk.Label(info_frame, text="No segment selected",
                                           font=('Segoe UI', 9, 'bold'))
        self.grid_seg_info_label.pack(side='left')
        
        # Status selector
        status_frame = tk.Frame(info_frame)
        status_frame.pack(side='right')
        
        tk.Label(status_frame, text="Status:").pack(side='left', padx=(0, 5))
        self.grid_status_var = tk.StringVar(value="untranslated")
        grid_status_combo = ttk.Combobox(status_frame, textvariable=self.grid_status_var,
                                        values=["untranslated", "draft", "translated", "approved"],
                                        state='readonly', width=12)
        grid_status_combo.pack(side='left')
        grid_status_combo.bind('<<ComboboxSelected>>', self.on_grid_editor_status_change)
        
        # Source (read-only)
        tk.Label(self.grid_editor_frame, text="Source:", font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.grid_source_text = tk.Text(self.grid_editor_frame, height=2, wrap='word', bg='#f5f5f5',
                                       state='disabled', font=('Segoe UI', 10))
        self.grid_source_text.pack(fill='x', pady=(2, 10))
        
        # Target (editable) with validation label
        target_header_frame = tk.Frame(self.grid_editor_frame)
        target_header_frame.pack(fill='x', anchor='w')
        tk.Label(target_header_frame, text="Target:", font=('Segoe UI', 9, 'bold')).pack(side='left')
        self.grid_tag_validation_label = tk.Label(target_header_frame, text="", font=('Segoe UI', 8))
        self.grid_tag_validation_label.pack(side='left', padx=(10, 0))
        
        self.grid_target_text = tk.Text(self.grid_editor_frame, height=2, wrap='word', font=('Segoe UI', 10))
        self.grid_target_text.pack(fill='x', pady=(2, 5))
        self.grid_target_text.bind('<KeyRelease>', self.on_grid_target_change)
        self.grid_target_text.bind('<Control-Return>', lambda e: self.save_grid_editor_and_next())
        self.grid_target_text.bind('<Control-b>', lambda e: self.insert_tag_grid('b'))
        self.grid_target_text.bind('<Control-i>', lambda e: self.insert_tag_grid('i'))
        self.grid_target_text.bind('<Control-u>', lambda e: self.insert_tag_grid('u'))
        
        # Tag buttons
        tag_button_frame = tk.Frame(self.grid_editor_frame)
        tag_button_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(tag_button_frame, text="Insert:").pack(side='left', padx=(0, 5))
        tk.Button(tag_button_frame, text="<b>Bold</b>", command=lambda: self.insert_tag_grid('b'),
                 relief='flat', bg='#ffcccc', font=('Segoe UI', 8)).pack(side='left', padx=2)
        tk.Button(tag_button_frame, text="<i>Italic</i>", command=lambda: self.insert_tag_grid('i'),
                 relief='flat', bg='#ccccff', font=('Segoe UI', 8, 'italic')).pack(side='left', padx=2)
        tk.Button(tag_button_frame, text="<u>Underline</u>", command=lambda: self.insert_tag_grid('u'),
                 relief='flat', bg='#ccffcc', font=('Segoe UI', 8, 'underline')).pack(side='left', padx=2)
        tk.Button(tag_button_frame, text="Strip Tags", command=self.strip_tags_from_grid_target,
                 relief='flat', bg='#eeeeee', font=('Segoe UI', 8)).pack(side='left', padx=10)
        tk.Button(tag_button_frame, text="Copy Source Tags", command=self.copy_source_tags_grid,
                 relief='flat', bg='#e6f3ff', font=('Segoe UI', 8)).pack(side='left', padx=2)
        
        # Action buttons
        button_frame = tk.Frame(self.grid_editor_frame)
        button_frame.pack(fill='x', pady=(0, 0))
        
        tk.Button(button_frame, text="Copy Source → Target", command=self.copy_source_to_target_grid_editor
                 ).pack(side='left', padx=(0, 5))
        tk.Button(button_frame, text="Clear Target", command=self.clear_grid_target
                 ).pack(side='left', padx=(0, 5))
        tk.Button(button_frame, text="Save & Next (Ctrl+Enter)", command=self.save_grid_editor_and_next,
                 bg='#4CAF50', fg='white').pack(side='right')

    
    def toggle_grid_editor(self):
        """Toggle visibility of Grid View editor panel"""
        if self.grid_editor_visible:
            # Hide the editor
            self.grid_editor_frame.pack_forget()
            self.grid_editor_visible = False
            # Update toolbar button
            self.grid_editor_toggle_btn.config(text="🔼 Show Editor Panel", relief='raised', bg='#E0E0E0', fg='black')
        else:
            # Show the editor
            self.grid_editor_frame.pack(side='bottom', fill='x', pady=(5, 0))
            self.grid_editor_visible = True
            # Update toolbar button
            self.grid_editor_toggle_btn.config(text="🔽 Hide Editor Panel", relief='sunken', bg='#4CAF50', fg='white')
    
    def on_grid_editor_status_change(self, event):
        """Handle status change from grid editor panel"""
        if hasattr(self, 'current_segment') and self.current_segment:
            new_status = self.grid_status_var.get()
            self.current_segment.status = new_status
            self.current_segment.modified = True
            self.modified = True
            self.update_progress()
            # Update the grid row if visible
            if self.current_row_index >= 0:
                self.update_grid_row(self.current_row_index)
    
    def copy_source_to_target_grid_editor(self):
        """Copy source to target in grid editor panel"""
        if hasattr(self, 'current_segment') and self.current_segment:
            self.grid_target_text.delete('1.0', 'end')
            self.grid_target_text.insert('1.0', self.current_segment.source)
    
    def save_grid_editor_segment(self):
        """Save the current segment from grid editor panel"""
        if hasattr(self, 'current_segment') and self.current_segment:
            target = self.grid_target_text.get('1.0', 'end-1c').strip()
            self.current_segment.target = target
            self.current_segment.status = self.grid_status_var.get()
            self.current_segment.modified = True
            self.modified = True
            self.update_progress()
            # Update the grid row
            if self.current_row_index >= 0:
                self.update_grid_row(self.current_row_index)
            self.log(f"✓ Segment #{self.current_segment.id} saved")
    
    def save_grid_editor_and_next(self):
        """Save and move to next segment"""
        self.save_grid_editor_segment()
        self.navigate_segment('next')
    
    def load_segment_to_grid_editor(self, segment):
        """Load a segment into the grid editor panel"""
        if not hasattr(self, 'grid_editor_frame'):
            return
        
        self.current_segment = segment
        self.grid_seg_info_label.config(text=f"Segment #{segment.id} | Paragraph {segment.paragraph_id}")
        
        # Source
        self.grid_source_text.config(state='normal')
        self.grid_source_text.delete('1.0', 'end')
        self.grid_source_text.insert('1.0', segment.source)
        self.grid_source_text.config(state='disabled')
        
        # Target
        self.grid_target_text.delete('1.0', 'end')
        if segment.target:
            self.grid_target_text.insert('1.0', segment.target)
        
        # Status
        self.grid_status_var.set(segment.status)
    
    def on_grid_target_change(self, event):
        """Handle target text changes in grid editor to validate tags"""
        if hasattr(self, 'current_segment') and self.current_segment:
            self.validate_tags_grid()
    
    def validate_tags_grid(self):
        """Validate HTML tags in grid editor target text"""
        if not hasattr(self, 'current_segment') or not self.current_segment:
            return
        
        source = self.current_segment.source
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
    
    def clear_grid_target(self):
        """Clear target text in grid editor"""
        self.grid_target_text.delete('1.0', 'end')
        self.grid_tag_validation_label.config(text="", fg='#666')
    
    def strip_tags_from_grid_target(self):
        """Remove all HTML tags from grid editor target text"""
        target = self.grid_target_text.get('1.0', 'end-1c')
        cleaned = re.sub(r'<[^>]+>', '', target)
        self.grid_target_text.delete('1.0', 'end')
        self.grid_target_text.insert('1.0', cleaned)
        self.validate_tags_grid()
    
    def copy_source_tags_grid(self):
        """Copy HTML tags from source to target in grid editor, preserving target text"""
        if not hasattr(self, 'current_segment') or not self.current_segment:
            return
        
        source = self.current_segment.source
        target = self.grid_target_text.get('1.0', 'end-1c')
        
        # Extract tags from source
        source_tags = re.findall(r'<[^>]+>', source)
        
        if not source_tags:
            self.log("No tags found in source")
            return
        
        # Remove existing tags from target
        clean_target = re.sub(r'<[^>]+>', '', target)
        
        # Try to intelligently place tags
        # For now, just wrap the target with the same tags
        result = clean_target
        for tag in source_tags:
            if not tag.startswith('</'):
                # Opening tag - add at start
                result = tag + result
            else:
                # Closing tag - add at end
                result = result + tag
        
        self.grid_target_text.delete('1.0', 'end')
        self.grid_target_text.insert('1.0', result)
        self.validate_tags_grid()
        self.log("✓ Tags copied from source")
    
    def create_assistance_panel(self):
        """Create the right-side assistance panel with dockable/stackable panes"""
        # Right panel container
        right_container = tk.Frame(self.main_paned, bg='#f9f9f9')
        self.main_paned.add(right_container, weight=1)
        
        # Header with controls
        header_frame = tk.Frame(right_container, bg='#e0e0e0', height=35)
        header_frame.pack(side='top', fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Translation Assistance", font=('Segoe UI', 10, 'bold'),
                bg='#e0e0e0').pack(side='left', padx=10, pady=5)
        
        # Layout mode button
        self.assist_layout_btn = tk.Button(header_frame, text="⊞ Stacked View",
                                          command=self.toggle_assistance_layout,
                                          font=('Segoe UI', 8), bg='#4CAF50', fg='white',
                                          relief='raised', padx=8, pady=2)
        self.assist_layout_btn.pack(side='right', padx=5)
        
        # Container for dynamic content (will switch between tabbed and stacked)
        self.assist_content_frame = tk.Frame(right_container, bg='#f9f9f9')
        self.assist_content_frame.pack(fill='both', expand=True)
        
        # Track which panels are visible
        self.assist_visible_panels = {'mt': True, 'llm': True, 'tm': True, 'glossary': True, 'nontrans': True}
        self.assist_layout_mode = 'tabbed'  # 'tabbed' or 'stacked'
        
        # Create initial tabbed layout
        self.create_tabbed_assistance()
        
        # Create detail view (always at bottom)
        self.create_detail_panel(right_container)
    
    def toggle_assistance_layout(self):
        """Toggle between tabbed and stacked layout for assistance panels"""
        if self.assist_layout_mode == 'tabbed':
            # Switch to stacked
            self.assist_layout_mode = 'stacked'
            self.assist_layout_btn.config(text="⊟ Tabbed View", bg='#FF9800')
            self.rebuild_assistance_layout()
        else:
            # Switch to tabbed
            self.assist_layout_mode = 'tabbed'
            self.assist_layout_btn.config(text="⊞ Stacked View", bg='#4CAF50')
            self.rebuild_assistance_layout()
    
    def rebuild_assistance_layout(self):
        """Rebuild the assistance panel layout"""
        # Clear current content
        for widget in self.assist_content_frame.winfo_children():
            widget.destroy()
        
        if self.assist_layout_mode == 'tabbed':
            self.create_tabbed_assistance()
        else:
            self.create_stacked_assistance()
    
    def create_tabbed_assistance(self):
        """Create tabbed notebook layout"""
        # Tabbed notebook for different suggestion types
        self.assist_notebook = ttk.Notebook(self.assist_content_frame)
        self.assist_notebook.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Create tabs for visible panels
        if self.assist_visible_panels.get('mt', True):
            mt_frame = tk.Frame(self.assist_notebook, bg='white')
            self.assist_notebook.add(mt_frame, text='🤖 MT')
            self.create_mt_tab(mt_frame)
        
        if self.assist_visible_panels.get('llm', True):
            llm_frame = tk.Frame(self.assist_notebook, bg='white')
            self.assist_notebook.add(llm_frame, text='✨ LLM')
            self.create_llm_tab(llm_frame)
        
        if self.assist_visible_panels.get('tm', True):
            tm_frame = tk.Frame(self.assist_notebook, bg='white')
            self.assist_notebook.add(tm_frame, text='💾 TM')
            self.create_tm_tab(tm_frame)
        
        if self.assist_visible_panels.get('glossary', True):
            glossary_frame = tk.Frame(self.assist_notebook, bg='white')
            self.assist_notebook.add(glossary_frame, text='📚 Glossary')
            self.create_glossary_tab(glossary_frame)
        
        if self.assist_visible_panels.get('nontrans', True):
            nt_frame = tk.Frame(self.assist_notebook, bg='white')
            self.assist_notebook.add(nt_frame, text='🔒 Non-trans')
            self.create_nontrans_tab(nt_frame)
    
    def create_stacked_assistance(self):
        """Create stacked collapsible panels layout with resizable panes"""
        # Create a vertical PanedWindow for resizable panels
        self.assist_stacked_paned = ttk.PanedWindow(self.assist_content_frame, orient='vertical')
        self.assist_stacked_paned.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Track panel weights for initial sizing
        panel_weights = []
        
        # Create collapsible panels in the PanedWindow
        if self.assist_visible_panels.get('mt', True):
            mt_container = self.create_collapsible_panel_resizable('🤖 Machine Translation', 'mt',
                                                                   self.create_mt_tab, expanded=True)
            self.assist_stacked_paned.add(mt_container, weight=1)
            panel_weights.append(1)
        
        if self.assist_visible_panels.get('llm', True):
            llm_container = self.create_collapsible_panel_resizable('✨ LLM Translation', 'llm',
                                                                    self.create_llm_tab, expanded=True)
            self.assist_stacked_paned.add(llm_container, weight=1)
            panel_weights.append(1)
        
        if self.assist_visible_panels.get('tm', True):
            tm_container = self.create_collapsible_panel_resizable('💾 Translation Memory', 'tm',
                                                                   self.create_tm_tab, expanded=False)
            self.assist_stacked_paned.add(tm_container, weight=1)
            panel_weights.append(1)
        
        if self.assist_visible_panels.get('glossary', True):
            glossary_container = self.create_collapsible_panel_resizable('📚 Glossary', 'glossary',
                                                                         self.create_glossary_tab, expanded=False)
            self.assist_stacked_paned.add(glossary_container, weight=1)
            panel_weights.append(1)
        
        if self.assist_visible_panels.get('nontrans', True):
            nontrans_container = self.create_collapsible_panel_resizable('🔒 Non-translatables', 'nontrans',
                                                                         self.create_nontrans_tab, expanded=False)
            self.assist_stacked_paned.add(nontrans_container, weight=1)
            panel_weights.append(1)

    
    
    def create_collapsible_panel_resizable(self, title, panel_id, content_creator, expanded=True):
        """Create a resizable collapsible panel with header and content for use in PanedWindow"""
        # Panel container - this will be added to the PanedWindow
        panel_container = tk.Frame(self.assist_stacked_paned, bg='#ffffff', relief='solid', borderwidth=1)
        
        # Header with collapse/expand button and visibility toggle
        header = tk.Frame(panel_container, bg='#e3f2fd', cursor='hand2')
        header.pack(fill='x')
        
        # Collapse/Expand button
        collapse_btn = tk.Label(header, text='▼' if expanded else '▶',
                               bg='#e3f2fd', font=('Segoe UI', 10),
                               cursor='hand2', width=2)
        collapse_btn.pack(side='left', padx=5, pady=3)
        
        # Title
        title_label = tk.Label(header, text=title, bg='#e3f2fd',
                              font=('Segoe UI', 9, 'bold'), cursor='hand2')
        title_label.pack(side='left', pady=3)
        
        # Resize indicator
        resize_label = tk.Label(header, text='⇕', bg='#e3f2fd',
                               font=('Segoe UI', 9), fg='#666')
        resize_label.pack(side='left', padx=10)
        
        # Undock button (removes from stack, returns to tabs)
        undock_btn = tk.Button(header, text='⊟', command=lambda: self.undock_panel(panel_id),
                              bg='#ff9800', fg='white', font=('Segoe UI', 8),
                              relief='flat', padx=4, pady=0, cursor='hand2')
        undock_btn.pack(side='right', padx=5, pady=3)
        
        # Content frame with minimum height
        content_frame = tk.Frame(panel_container, bg='white')
        if expanded:
            content_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Set minimum height for the panel
        panel_container.update_idletasks()
        
        # Create content using the provided creator function
        content_creator(content_frame)
        
        # Toggle function
        def toggle_panel():
            if content_frame.winfo_ismapped():
                content_frame.pack_forget()
                collapse_btn.config(text='▶')
                panel_container.config(height=30)  # Collapsed height (just header)
            else:
                content_frame.pack(fill='both', expand=True, padx=2, pady=2)
                collapse_btn.config(text='▼')
                panel_container.config(height=200)  # Expanded default height
        
        # Bind click events to header elements (but not the undock button)
        collapse_btn.bind('<Button-1>', lambda e: toggle_panel())
        title_label.bind('<Button-1>', lambda e: toggle_panel())
        
        # Return the container to be added to PanedWindow
        return panel_container
    
    def create_collapsible_panel(self, parent, title, panel_id, content_creator, expanded=True):
        """Create a collapsible panel with header and content"""
        # Panel container
        panel_container = tk.Frame(parent, bg='#ffffff', relief='solid', borderwidth=1)
        panel_container.pack(fill='both', expand=False, padx=3, pady=2)
        
        # Header with collapse/expand button and visibility toggle
        header = tk.Frame(panel_container, bg='#e3f2fd', cursor='hand2')
        header.pack(fill='x')
        
        # Collapse/Expand button
        collapse_btn = tk.Label(header, text='▼' if expanded else '▶',
                               bg='#e3f2fd', font=('Segoe UI', 10),
                               cursor='hand2', width=2)
        collapse_btn.pack(side='left', padx=5, pady=3)
        
        # Title
        title_label = tk.Label(header, text=title, bg='#e3f2fd',
                              font=('Segoe UI', 9, 'bold'), cursor='hand2')
        title_label.pack(side='left', pady=3)
        
        # Undock button (removes from stack, returns to tabs)
        undock_btn = tk.Button(header, text='⊟', command=lambda: self.undock_panel(panel_id),
                              bg='#ff9800', fg='white', font=('Segoe UI', 8),
                              relief='flat', padx=4, pady=0, cursor='hand2')
        undock_btn.pack(side='right', padx=5, pady=3)
        
        # Content frame
        content_frame = tk.Frame(panel_container, bg='white')
        if expanded:
            content_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Create content using the provided creator function
        content_creator(content_frame)
        
        # Toggle function
        def toggle_panel():
            if content_frame.winfo_ismapped():
                content_frame.pack_forget()
                collapse_btn.config(text='▶')
            else:
                content_frame.pack(fill='both', expand=True, padx=2, pady=2)
                collapse_btn.config(text='▼')
        
        # Bind click events to header elements
        collapse_btn.bind('<Button-1>', lambda e: toggle_panel())
        title_label.bind('<Button-1>', lambda e: toggle_panel())
        header.bind('<Button-1>', lambda e: toggle_panel())
    
    def undock_panel(self, panel_id):
        """Remove a panel from stacked view (will reappear when switching to tabbed)"""
        self.assist_visible_panels[panel_id] = False
        self.rebuild_assistance_layout()
        self.log(f"ℹ Panel '{panel_id}' hidden. Switch to Tabbed View to restore.")
    
    def create_detail_panel(self, parent):
        """Create the suggestion detail panel (shows source/target of selected item)"""
        detail_frame = tk.LabelFrame(parent, text="Suggestion Detail", padx=5, pady=5)
        detail_frame.pack(side='bottom', fill='x', padx=2, pady=2)
        
        # Source of selected suggestion
        tk.Label(detail_frame, text="Source:", font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.assist_detail_source = tk.Text(detail_frame, height=2, wrap='word', 
                                            bg='#f5f5f5', state='disabled',
                                            font=('Segoe UI', 9))
        self.assist_detail_source.pack(fill='x', pady=(2, 8))
        
        # Target of selected suggestion
        tk.Label(detail_frame, text="Target:", font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.assist_detail_target = tk.Text(detail_frame, height=2, wrap='word',
                                            bg='white', state='disabled',
                                            font=('Segoe UI', 9))
        self.assist_detail_target.pack(fill='x', pady=(2, 5))
        
        # Action buttons
        detail_btn_frame = tk.Frame(detail_frame)
        detail_btn_frame.pack(fill='x', pady=(5, 0))
        
        tk.Button(detail_btn_frame, text="📋 Copy to Target", 
                 command=self.copy_suggestion_to_target,
                 bg='#4CAF50', fg='white', font=('Segoe UI', 9)).pack(side='left', padx=2)
        tk.Button(detail_btn_frame, text="➕ Insert at Cursor",
                 command=self.insert_suggestion_at_cursor,
                 bg='#2196F3', fg='white', font=('Segoe UI', 9)).pack(side='left', padx=2)
    
    def create_mt_tab(self, parent):
        """Create Machine Translation tab content"""
        # Toolbar with provider selection and translate button
        toolbar = tk.Frame(parent, bg='#f0f0f0')
        toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Label(toolbar, text="Provider:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(side='left', padx=2)
        self.mt_provider_var = tk.StringVar(value="Google Translate")
        mt_provider_combo = ttk.Combobox(toolbar, textvariable=self.mt_provider_var,
                                        values=["Google Translate", "DeepL", "Microsoft Translator", 
                                               "Amazon Translate", "Custom MT"],
                                        state='readonly', width=18, font=('Segoe UI', 9))
        mt_provider_combo.pack(side='left', padx=5)
        
        tk.Button(toolbar, text="🔄 Translate", command=self.get_mt_translation,
                 bg='#4CAF50', fg='white', font=('Segoe UI', 9)).pack(side='left', padx=5)
        
        # Listbox for MT results
        list_frame = tk.Frame(parent)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical')
        self.mt_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                     font=('Segoe UI', 9), selectmode='single')
        scrollbar.config(command=self.mt_listbox.yview)
        
        self.mt_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.mt_listbox.bind('<<ListboxSelect>>', self.on_mt_select)
        self.mt_listbox.bind('<Double-Button-1>', lambda e: self.copy_suggestion_to_target())
        
        # Store MT results
        self.mt_results = []
    
    def create_llm_tab(self, parent):
        """Create LLM Translation tab content"""
        # Toolbar with model selection and translate button
        toolbar = tk.Frame(parent, bg='#f0f0f0')
        toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Label(toolbar, text="Model:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(side='left', padx=2)
        self.llm_model_var = tk.StringVar(value="Claude 3.5 Sonnet")
        llm_model_combo = ttk.Combobox(toolbar, textvariable=self.llm_model_var,
                                      values=["Claude 3.5 Sonnet", "GPT-4", "Gemini Pro",
                                             "Claude 3 Opus", "GPT-4 Turbo", "Supervertaler Custom"],
                                      state='readonly', width=18, font=('Segoe UI', 9))
        llm_model_combo.pack(side='left', padx=5)
        
        tk.Button(toolbar, text="✨ Generate", command=self.get_llm_translation,
                 bg='#9C27B0', fg='white', font=('Segoe UI', 9)).pack(side='left', padx=5)
        
        # Prompt template selector
        prompt_frame = tk.Frame(parent, bg='#f9f9f9')
        prompt_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Label(prompt_frame, text="Prompt:", bg='#f9f9f9', font=('Segoe UI', 9)).pack(side='left', padx=2)
        self.llm_prompt_var = tk.StringVar(value="Standard Translation")
        llm_prompt_combo = ttk.Combobox(prompt_frame, textvariable=self.llm_prompt_var,
                                       values=["Standard Translation", "Legal Translation",
                                              "Technical Translation", "Marketing Translation",
                                              "Medical Translation", "Custom Supervertaler Prompt"],
                                       state='readonly', width=25, font=('Segoe UI', 9))
        llm_prompt_combo.pack(side='left', padx=5)
        
        # Listbox for LLM results (can have multiple alternatives)
        list_frame = tk.Frame(parent)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical')
        self.llm_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                      font=('Segoe UI', 9), selectmode='single')
        scrollbar.config(command=self.llm_listbox.yview)
        
        self.llm_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.llm_listbox.bind('<<ListboxSelect>>', self.on_llm_select)
        self.llm_listbox.bind('<Double-Button-1>', lambda e: self.copy_suggestion_to_target())
        
        # Store LLM results
        self.llm_results = []
    
    def create_tm_tab(self, parent):
        """Create Translation Memory tab content"""
        # Toolbar with TM source selection and search button
        toolbar = tk.Frame(parent, bg='#f0f0f0')
        toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Label(toolbar, text="TM:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(side='left', padx=2)
        self.tm_source_var = tk.StringVar(value="Project TM")
        tm_source_combo = ttk.Combobox(toolbar, textvariable=self.tm_source_var,
                                      values=["Project TM", "Main TM", "Reference TM",
                                             "All TMs", "Custom TM"],
                                      state='readonly', width=15, font=('Segoe UI', 9))
        tm_source_combo.pack(side='left', padx=5)
        
        tk.Button(toolbar, text="🔍 Search", command=self.search_tm,
                 bg='#2196F3', fg='white', font=('Segoe UI', 9)).pack(side='left', padx=5)
        
        # Settings frame
        settings_frame = tk.Frame(parent, bg='#f9f9f9')
        settings_frame.pack(side='top', fill='x', padx=5, pady=2)
        
        tk.Label(settings_frame, text="Min. Match:", bg='#f9f9f9', 
                font=('Segoe UI', 8)).pack(side='left', padx=2)
        self.tm_threshold_var = tk.StringVar(value="75")
        tm_threshold_spin = ttk.Spinbox(settings_frame, from_=50, to=100, increment=5,
                                       textvariable=self.tm_threshold_var, width=5,
                                       font=('Segoe UI', 8))
        tm_threshold_spin.pack(side='left', padx=2)
        tk.Label(settings_frame, text="%", bg='#f9f9f9', font=('Segoe UI', 8)).pack(side='left')
        
        # Treeview for TM matches (shows match %, source, target)
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        self.tm_tree = ttk.Treeview(tree_frame, columns=('match', 'text'),
                                   show='headings', yscrollcommand=scrollbar.set,
                                   selectmode='browse', height=10)
        scrollbar.config(command=self.tm_tree.yview)
        
        self.tm_tree.heading('match', text='Match %')
        self.tm_tree.heading('text', text='Translation')
        
        self.tm_tree.column('match', width=70, minwidth=70, stretch=False)
        self.tm_tree.column('text', width=250, minwidth=150, stretch=True)
        
        self.tm_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Tag configuration for match percentage colors
        self.tm_tree.tag_configure('exact', background='#c8e6c9')  # Light green
        self.tm_tree.tag_configure('high', background='#fff9c4')   # Light yellow
        self.tm_tree.tag_configure('medium', background='#ffecb3') # Light orange
        
        self.tm_tree.bind('<<TreeviewSelect>>', self.on_tm_select)
        self.tm_tree.bind('<Double-Button-1>', lambda e: self.copy_suggestion_to_target())
        
        # Store TM results
        self.tm_results = []
    
    def create_glossary_tab(self, parent):
        """Create Glossary/Termbase tab content"""
        # Toolbar
        toolbar = tk.Frame(parent, bg='#f0f0f0')
        toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Label(toolbar, text="Glossary:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(side='left', padx=2)
        self.glossary_source_var = tk.StringVar(value="Project Glossary")
        glossary_combo = ttk.Combobox(toolbar, textvariable=self.glossary_source_var,
                                     values=["Project Glossary", "Main Termbase",
                                            "Domain Glossary", "All Glossaries"],
                                     state='readonly', width=18, font=('Segoe UI', 9))
        glossary_combo.pack(side='left', padx=5)
        
        tk.Button(toolbar, text="🔍 Search", command=self.search_glossary,
                 bg='#FF9800', fg='white', font=('Segoe UI', 9)).pack(side='left', padx=5)
        
        # Treeview for glossary matches
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        self.glossary_tree = ttk.Treeview(tree_frame, columns=('source_term', 'target_term', 'domain'),
                                         show='headings', yscrollcommand=scrollbar.set,
                                         selectmode='browse', height=10)
        scrollbar.config(command=self.glossary_tree.yview)
        
        self.glossary_tree.heading('source_term', text='Source Term')
        self.glossary_tree.heading('target_term', text='Target Term')
        self.glossary_tree.heading('domain', text='Domain')
        
        self.glossary_tree.column('source_term', width=120, minwidth=80, stretch=True)
        self.glossary_tree.column('target_term', width=120, minwidth=80, stretch=True)
        self.glossary_tree.column('domain', width=80, minwidth=60, stretch=False)
        
        self.glossary_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.glossary_tree.bind('<<TreeviewSelect>>', self.on_glossary_select)
        self.glossary_tree.bind('<Double-Button-1>', lambda e: self.insert_suggestion_at_cursor())
        
        # Store glossary results
        self.glossary_results = []
    
    def create_nontrans_tab(self, parent):
        """Create Non-translatables tab content"""
        # Info label
        info_frame = tk.Frame(parent, bg='#e3f2fd')
        info_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Label(info_frame, text="💡 Non-translatable elements detected in source",
                bg='#e3f2fd', font=('Segoe UI', 9)).pack(padx=10, pady=5)
        
        # Listbox for non-translatables
        list_frame = tk.Frame(parent)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical')
        self.nontrans_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                          font=('Segoe UI', 9), selectmode='single')
        scrollbar.config(command=self.nontrans_listbox.yview)
        
        self.nontrans_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.nontrans_listbox.bind('<<ListboxSelect>>', self.on_nontrans_select)
        self.nontrans_listbox.bind('<Double-Button-1>', lambda e: self.insert_suggestion_at_cursor())
        
        # Store non-translatables
        self.nontrans_results = []
        
    # Assistance panel action methods (placeholder implementations for now)
    
    def get_mt_translation(self):
        """Get machine translation for current segment"""
        if not hasattr(self, 'current_segment') or not self.current_segment:
            self.log("⚠ No segment selected")
            return
        
        provider = self.mt_provider_var.get()
        source_text = self.current_segment.source
        
        self.log(f"🤖 Requesting MT from {provider}...")
        
        # Placeholder: In real implementation, call MT API
        # For now, show example results
        self.mt_results = [
            {"provider": provider, "text": f"[MT] {source_text} (translated)", "confidence": 0.95},
            {"provider": provider, "text": f"[MT Alt] {source_text} (alternative)", "confidence": 0.85}
        ]
        
        self.mt_listbox.delete(0, 'end')
        for i, result in enumerate(self.mt_results):
            conf_pct = int(result['confidence'] * 100)
            self.mt_listbox.insert('end', f"{conf_pct}% - {result['text']}")
        
        self.log(f"✓ Received {len(self.mt_results)} MT suggestions")
    
    def get_llm_translation(self):
        """Get LLM translation for current segment"""
        if not hasattr(self, 'current_segment') or not self.current_segment:
            self.log("⚠ No segment selected")
            return
        
        model = self.llm_model_var.get()
        prompt_type = self.llm_prompt_var.get()
        source_text = self.current_segment.source
        
        self.log(f"✨ Requesting LLM translation from {model} with {prompt_type}...")
        
        # Placeholder: In real implementation, call LLM API
        # This is where Supervertaler integration will happen!
        self.llm_results = [
            {"model": model, "prompt": prompt_type, "text": f"[LLM] {source_text} (professional translation)", "quality": 0.98},
            {"model": model, "prompt": prompt_type, "text": f"[LLM Alt] {source_text} (alternative phrasing)", "quality": 0.92}
        ]
        
        self.llm_listbox.delete(0, 'end')
        for i, result in enumerate(self.llm_results):
            quality_pct = int(result['quality'] * 100)
            self.llm_listbox.insert('end', f"{quality_pct}% - {result['text']}")
        
        self.log(f"✓ Received {len(self.llm_results)} LLM suggestions")
        self.log(f"💡 Future: This will integrate with Supervertaler prompts and models")
    
    def search_tm(self):
        """Search translation memory for matches"""
        if not hasattr(self, 'current_segment') or not self.current_segment:
            self.log("⚠ No segment selected")
            return
        
        tm_source = self.tm_source_var.get()
        threshold = int(self.tm_threshold_var.get())
        source_text = self.current_segment.source
        
        self.log(f"🔍 Searching {tm_source} (min {threshold}% match)...")
        
        # Placeholder: In real implementation, search TM database
        self.tm_results = [
            {"match": 100, "source": source_text, "target": f"[100% TM] {source_text} (exact match)", "tm": tm_source},
            {"match": 95, "source": source_text, "target": f"[95% TM] {source_text} (fuzzy match)", "tm": tm_source},
            {"match": 80, "source": source_text, "target": f"[80% TM] {source_text} (partial match)", "tm": tm_source}
        ]
        
        # Filter by threshold
        self.tm_results = [r for r in self.tm_results if r['match'] >= threshold]
        
        # Clear and populate tree
        for item in self.tm_tree.get_children():
            self.tm_tree.delete(item)
        
        for result in self.tm_results:
            match_pct = result['match']
            if match_pct == 100:
                tag = 'exact'
            elif match_pct >= 90:
                tag = 'high'
            else:
                tag = 'medium'
            
            self.tm_tree.insert('', 'end', values=(f"{match_pct}%", result['target']), tags=(tag,))
        
        self.log(f"✓ Found {len(self.tm_results)} TM matches")
    
    def search_glossary(self):
        """Search glossary/termbase for terms"""
        if not hasattr(self, 'current_segment') or not self.current_segment:
            self.log("⚠ No segment selected")
            return
        
        glossary = self.glossary_source_var.get()
        source_text = self.current_segment.source
        
        self.log(f"📚 Searching {glossary}...")
        
        # Placeholder: In real implementation, search glossary database
        # Extract potential terms from source
        self.glossary_results = [
            {"source_term": "pivot point", "target_term": "draaipunt", "domain": "Technical"},
            {"source_term": "coupling bar", "target_term": "koppelstang", "domain": "Technical"},
            {"source_term": "frame", "target_term": "frame", "domain": "General"}
        ]
        
        # Clear and populate tree
        for item in self.glossary_tree.get_children():
            self.glossary_tree.delete(item)
        
        for result in self.glossary_results:
            self.glossary_tree.insert('', 'end', values=(
                result['source_term'],
                result['target_term'],
                result['domain']
            ))
        
        self.log(f"✓ Found {len(self.glossary_results)} glossary terms")
    
    def on_mt_select(self, event):
        """Handle MT suggestion selection"""
        selection = self.mt_listbox.curselection()
        if selection and self.mt_results:
            idx = selection[0]
            result = self.mt_results[idx]
            self.update_suggestion_detail(self.current_segment.source if hasattr(self, 'current_segment') else "",
                                         result['text'])
    
    def on_llm_select(self, event):
        """Handle LLM suggestion selection"""
        selection = self.llm_listbox.curselection()
        if selection and self.llm_results:
            idx = selection[0]
            result = self.llm_results[idx]
            self.update_suggestion_detail(self.current_segment.source if hasattr(self, 'current_segment') else "",
                                         result['text'])
    
    def on_tm_select(self, event):
        """Handle TM match selection"""
        selection = self.tm_tree.selection()
        if selection and self.tm_results:
            idx = self.tm_tree.index(selection[0])
            result = self.tm_results[idx]
            self.update_suggestion_detail(result['source'], result['target'])
    
    def on_glossary_select(self, event):
        """Handle glossary term selection"""
        selection = self.glossary_tree.selection()
        if selection and self.glossary_results:
            idx = self.glossary_tree.index(selection[0])
            result = self.glossary_results[idx]
            self.update_suggestion_detail(result['source_term'], result['target_term'])
    
    def on_nontrans_select(self, event):
        """Handle non-translatable selection"""
        selection = self.nontrans_listbox.curselection()
        if selection and self.nontrans_results:
            idx = selection[0]
            result = self.nontrans_results[idx]
            self.update_suggestion_detail("Non-translatable", result)
    
    def update_suggestion_detail(self, source, target):
        """Update the suggestion detail panel with source/target"""
        # Update source
        self.assist_detail_source.config(state='normal')
        self.assist_detail_source.delete('1.0', 'end')
        self.assist_detail_source.insert('1.0', source)
        self.assist_detail_source.config(state='disabled')
        
        # Update target
        self.assist_detail_target.config(state='normal')
        self.assist_detail_target.delete('1.0', 'end')
        self.assist_detail_target.insert('1.0', target)
        self.assist_detail_target.config(state='disabled')
    
    def copy_suggestion_to_target(self):
        """Copy the selected suggestion to the target field"""
        target_text = self.assist_detail_target.get('1.0', 'end-1c')
        if not target_text.strip():
            self.log("⚠ No suggestion selected")
            return
        
        # Insert into grid editor if visible
        if hasattr(self, 'grid_target_text'):
            self.grid_target_text.delete('1.0', 'end')
            self.grid_target_text.insert('1.0', target_text)
            self.log("✓ Suggestion copied to target")
    
    def insert_suggestion_at_cursor(self):
        """Insert the selected suggestion at cursor position in target field"""
        target_text = self.assist_detail_target.get('1.0', 'end-1c')
        if not target_text.strip():
            self.log("⚠ No suggestion selected")
            return
        
        # Insert at cursor position in grid editor
        if hasattr(self, 'grid_target_text'):
            self.grid_target_text.insert('insert', target_text)
            self.log("✓ Suggestion inserted at cursor")
    
    def create_split_layout(self):
        """Create List View layout (list with editor panel)"""
        
        # Create main horizontal paned window (list/editor on left, assistance panel on right)
        self.main_paned = ttk.PanedWindow(self.content_frame, orient='horizontal')
        self.main_paned.pack(fill='both', expand=True)
        
        # Left side: Grid and editor
        left_container = tk.Frame(self.main_paned)
        self.main_paned.add(left_container, weight=3)
        
        # Grid frame (top part)
        grid_frame = tk.LabelFrame(left_container, text="Translation Grid", padx=5, pady=5)
        grid_frame.pack(side='top', fill='both', expand=True)
        
        # Filter panel (above the treeview) - using same filter variables as Grid View
        filter_frame = tk.Frame(grid_frame, bg='#f0f0f0', relief='ridge', borderwidth=1)
        filter_frame.pack(side='top', fill='x', pady=(0, 5))
        
        # Filter label
        tk.Label(filter_frame, text="🔍 Filter:", bg='#f0f0f0', 
                font=('Segoe UI', 9, 'bold')).pack(side='left', padx=5, pady=5)
        
        # Filter mode selection - always create new buttons for this view
        mode_frame = tk.Frame(filter_frame, bg='#f0f0f0', relief='solid', bd=1)
        mode_frame.pack(side='left', padx=5)
        
        # Create buttons with current mode state
        filter_btn = tk.Button(mode_frame, text="🔍 Filter",
                              command=lambda: self.set_filter_mode('filter'),
                              bg='#4CAF50' if self.filter_mode == 'filter' else '#e0e0e0',
                              fg='white' if self.filter_mode == 'filter' else '#666',
                              font=('Segoe UI', 9, 'bold') if self.filter_mode == 'filter' else ('Segoe UI', 9),
                              relief='sunken' if self.filter_mode == 'filter' else 'raised',
                              bd=2, cursor='hand2', width=10)
        filter_btn.pack(side='left', padx=1, pady=1)
        
        highlight_btn = tk.Button(mode_frame, text="💡 Highlight",
                                 command=lambda: self.set_filter_mode('highlight'),
                                 bg='#FFA500' if self.filter_mode == 'highlight' else '#e0e0e0',
                                 fg='white' if self.filter_mode == 'highlight' else '#666',
                                 font=('Segoe UI', 9, 'bold') if self.filter_mode == 'highlight' else ('Segoe UI', 9),
                                 relief='sunken' if self.filter_mode == 'highlight' else 'raised',
                                 bd=2, cursor='hand2', width=10)
        highlight_btn.pack(side='left', padx=1, pady=1)
        
        # Store references for this view
        self.list_filter_mode_btn = filter_btn
        self.list_highlight_mode_btn = highlight_btn
        # Also update main references to point to these buttons
        self.filter_mode_btn = filter_btn
        self.highlight_mode_btn = highlight_btn
        
        tk.Label(filter_frame, text="│", bg='#f0f0f0', fg='#ccc',
                font=('Segoe UI', 10)).pack(side='left', padx=5)
        
        # Source filter - using shared variables
        if not hasattr(self, 'filter_source_var'):
            self.filter_source_var = tk.StringVar()
        
        tk.Label(filter_frame, text="Source:", bg='#f0f0f0',
                font=('Segoe UI', 9)).pack(side='left', padx=(0, 2))
        source_entry = tk.Entry(filter_frame, textvariable=self.filter_source_var, width=20,
                               font=('Segoe UI', 9))
        source_entry.pack(side='left', padx=(0, 10))
        # Bind Enter key to apply filters
        source_entry.bind('<Return>', lambda e: self.apply_filters())
        
        # Target filter
        if not hasattr(self, 'filter_target_var'):
            self.filter_target_var = tk.StringVar()
        
        tk.Label(filter_frame, text="Target:", bg='#f0f0f0',
                font=('Segoe UI', 9)).pack(side='left', padx=(0, 2))
        target_entry = tk.Entry(filter_frame, textvariable=self.filter_target_var, width=20,
                               font=('Segoe UI', 9))
        target_entry.pack(side='left', padx=(0, 10))
        # Bind Enter key to apply filters
        target_entry.bind('<Return>', lambda e: self.apply_filters())
        
        # Status filter
        if not hasattr(self, 'filter_status_var'):
            self.filter_status_var = tk.StringVar(value="All")
        
        tk.Label(filter_frame, text="Status:", bg='#f0f0f0',
                font=('Segoe UI', 9)).pack(side='left', padx=(0, 2))
        status_combo = ttk.Combobox(filter_frame, textvariable=self.filter_status_var,
                                   values=["All", "untranslated", "draft", "translated", "approved"],
                                   state='readonly', width=12, font=('Segoe UI', 9))
        status_combo.pack(side='left', padx=(0, 10))
        # Combobox selection triggers apply automatically (user expectation for dropdowns)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Apply button
        tk.Button(filter_frame, text="🔍 Apply", command=self.apply_filters,
                 bg='#2196F3', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief='raised', cursor='hand2', padx=8).pack(side='left', padx=5)
        
        # Clear button
        tk.Button(filter_frame, text="✕ Clear", command=self.clear_filters,
                 bg='#ff5252', fg='white', font=('Segoe UI', 8),
                 relief='raised', cursor='hand2').pack(side='left', padx=5)
        
        # Results label - always create new for this view
        self.filter_results_label = tk.Label(filter_frame, text="", bg='#f0f0f0',
                                            font=('Segoe UI', 9, 'italic'), fg='#666')
        self.filter_results_label.pack(side='left', padx=10)
        
        # Create a frame to hold treeview and scrollbars with grid layout
        tree_container = tk.Frame(grid_frame)
        tree_container.pack(side='top', fill='both', expand=True)
        
        # Create treeview for segments (parent is tree_container now)
        self.tree = ttk.Treeview(tree_container,
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
        v_scroll = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
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
        editor_frame = tk.LabelFrame(left_container, text="Segment Editor", padx=10, pady=10)
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
        self.target_text.bind('<Control-b>', lambda e: self.insert_tag('b'))
        self.target_text.bind('<Control-i>', lambda e: self.insert_tag('i'))
        self.target_text.bind('<Control-u>', lambda e: self.insert_tag('u'))
        
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
        
        # Right side: Assistance panel
        self.create_assistance_panel()
    
    def create_document_layout(self):
        """Create Document View layout - shows text in document flow with clickable segments"""
        
        # Create main horizontal paned window (document/editor on left, assistance panel on right)
        self.main_paned = ttk.PanedWindow(self.content_frame, orient='horizontal')
        self.main_paned.pack(fill='both', expand=True)
        
        # Left side: Document and editor
        left_container = tk.Frame(self.main_paned)
        self.main_paned.add(left_container, weight=3)
        
        # Filter panel (at the top) - using same filter variables as Grid View
        filter_frame = tk.Frame(left_container, bg='#f0f0f0', relief='ridge', borderwidth=1)
        filter_frame.pack(side='top', fill='x', pady=(0, 5))
        
        # Filter label
        tk.Label(filter_frame, text="🔍 Filter:", bg='#f0f0f0', 
                font=('Segoe UI', 9, 'bold')).pack(side='left', padx=5, pady=5)
        
        # Filter mode selection - always create new buttons for this view
        mode_frame = tk.Frame(filter_frame, bg='#f0f0f0', relief='solid', bd=1)
        mode_frame.pack(side='left', padx=5)
        
        # Create buttons with current mode state
        filter_btn = tk.Button(mode_frame, text="🔍 Filter",
                              command=lambda: self.set_filter_mode('filter'),
                              bg='#4CAF50' if self.filter_mode == 'filter' else '#e0e0e0',
                              fg='white' if self.filter_mode == 'filter' else '#666',
                              font=('Segoe UI', 9, 'bold') if self.filter_mode == 'filter' else ('Segoe UI', 9),
                              relief='sunken' if self.filter_mode == 'filter' else 'raised',
                              bd=2, cursor='hand2', width=10)
        filter_btn.pack(side='left', padx=1, pady=1)
        
        highlight_btn = tk.Button(mode_frame, text="💡 Highlight",
                                 command=lambda: self.set_filter_mode('highlight'),
                                 bg='#FFA500' if self.filter_mode == 'highlight' else '#e0e0e0',
                                 fg='white' if self.filter_mode == 'highlight' else '#666',
                                 font=('Segoe UI', 9, 'bold') if self.filter_mode == 'highlight' else ('Segoe UI', 9),
                                 relief='sunken' if self.filter_mode == 'highlight' else 'raised',
                                 bd=2, cursor='hand2', width=10)
        highlight_btn.pack(side='left', padx=1, pady=1)
        
        # Store references for this view
        self.doc_filter_mode_btn = filter_btn
        self.doc_highlight_mode_btn = highlight_btn
        # Also update main references to point to these buttons
        self.filter_mode_btn = filter_btn
        self.highlight_mode_btn = highlight_btn
        
        tk.Label(filter_frame, text="│", bg='#f0f0f0', fg='#ccc',
                font=('Segoe UI', 10)).pack(side='left', padx=5)
        
        # Source filter - using shared variables
        if not hasattr(self, 'filter_source_var'):
            self.filter_source_var = tk.StringVar()
        
        tk.Label(filter_frame, text="Source:", bg='#f0f0f0',
                font=('Segoe UI', 9)).pack(side='left', padx=(0, 2))
        source_entry = tk.Entry(filter_frame, textvariable=self.filter_source_var, width=20,
                               font=('Segoe UI', 9))
        source_entry.pack(side='left', padx=(0, 10))
        source_entry.bind('<Return>', lambda e: self.apply_filters())
        
        # Target filter
        if not hasattr(self, 'filter_target_var'):
            self.filter_target_var = tk.StringVar()
        
        tk.Label(filter_frame, text="Target:", bg='#f0f0f0',
                font=('Segoe UI', 9)).pack(side='left', padx=(0, 2))
        target_entry = tk.Entry(filter_frame, textvariable=self.filter_target_var, width=20,
                               font=('Segoe UI', 9))
        target_entry.pack(side='left', padx=(0, 10))
        target_entry.bind('<Return>', lambda e: self.apply_filters())
        
        # Status filter
        if not hasattr(self, 'filter_status_var'):
            self.filter_status_var = tk.StringVar(value="All")
        
        tk.Label(filter_frame, text="Status:", bg='#f0f0f0',
                font=('Segoe UI', 9)).pack(side='left', padx=(0, 2))
        status_combo = ttk.Combobox(filter_frame, textvariable=self.filter_status_var,
                                   values=["All", "untranslated", "draft", "translated", "approved"],
                                   state='readonly', width=12, font=('Segoe UI', 9))
        status_combo.pack(side='left', padx=(0, 10))
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Apply button
        tk.Button(filter_frame, text="🔍 Apply", command=self.apply_filters,
                 bg='#2196F3', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief='raised', cursor='hand2', padx=8).pack(side='left', padx=5)
        
        # Clear button
        tk.Button(filter_frame, text="✕ Clear", command=self.clear_filters,
                 bg='#ff5252', fg='white', font=('Segoe UI', 8),
                 relief='raised', cursor='hand2').pack(side='left', padx=5)
        
        # Results label - always create new for this view
        self.filter_results_label = tk.Label(filter_frame, text="", bg='#f0f0f0',
                                            font=('Segoe UI', 9, 'italic'), fg='#666')
        self.filter_results_label.pack(side='left', padx=10)
        
        # Split into document area (top) and editor panel (bottom)
        # Document area
        doc_container = tk.Frame(left_container)
        doc_container.pack(side='top', fill='both', expand=True)
        
        # Canvas for scrolling
        self.doc_canvas = tk.Canvas(doc_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(doc_container, orient='vertical', command=self.doc_canvas.yview)
        
        self.doc_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.doc_canvas.pack(side='left', fill='both', expand=True)
        
        # Inner frame to hold content
        self.doc_inner_frame = tk.Frame(self.doc_canvas, bg='white')
        self.doc_canvas_window = self.doc_canvas.create_window((0, 0), window=self.doc_inner_frame, anchor='nw')
        
        # Bind canvas resizing to update inner frame width
        def on_canvas_resize(event):
            # Set the inner frame width to match canvas width (minus scrollbar and padding)
            canvas_width = event.width - 80  # Account for padding (40px each side)
            self.doc_canvas.itemconfig(self.doc_canvas_window, width=canvas_width + 80)
            self.doc_inner_frame.config(width=canvas_width)
        
        self.doc_canvas.bind('<Configure>', on_canvas_resize)
        
        # Update scroll region when inner frame changes
        self.doc_inner_frame.bind('<Configure>', 
                                  lambda e: self.doc_canvas.configure(scrollregion=self.doc_canvas.bbox('all')))
        
        # Bind mouse wheel
        self.doc_canvas.bind('<MouseWheel>', lambda e: self.doc_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.doc_inner_frame.bind('<MouseWheel>', lambda e: self.doc_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Editor panel (bottom) - similar to Split View
        editor_frame = tk.LabelFrame(left_container, text="Segment Editor", padx=10, pady=10)
        editor_frame.pack(side='bottom', fill='x', pady=(5, 0))
        
        # Segment info
        info_frame = tk.Frame(editor_frame)
        info_frame.pack(fill='x', pady=(0, 5))
        
        self.doc_seg_info_label = tk.Label(info_frame, text="Click on any segment in the document to edit",
                                       font=('Segoe UI', 9, 'bold'))
        self.doc_seg_info_label.pack(side='left')
        
        # Status selector
        status_frame = tk.Frame(info_frame)
        status_frame.pack(side='right')
        
        tk.Label(status_frame, text="Status:").pack(side='left', padx=(0, 5))
        self.doc_status_var = tk.StringVar(value="untranslated")
        self.doc_status_combo = ttk.Combobox(status_frame, textvariable=self.doc_status_var,
                                        values=["untranslated", "draft", "translated", "approved"],
                                        state='readonly', width=12)
        self.doc_status_combo.pack(side='left')
        self.doc_status_combo.bind('<<ComboboxSelected>>', self.on_doc_status_change)
        
        # Source (read-only)
        tk.Label(editor_frame, text="Source:", font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.doc_source_text = tk.Text(editor_frame, height=2, wrap='word', bg='#f5f5f5',
                                   state='disabled', font=('Segoe UI', 10))
        self.doc_source_text.pack(fill='x', pady=(2, 10))
        
        # Target (editable)
        tk.Label(editor_frame, text="Target:", font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.doc_target_text = tk.Text(editor_frame, height=2, wrap='word', font=('Segoe UI', 10))
        self.doc_target_text.pack(fill='x', pady=(2, 5))
        self.doc_target_text.bind('<KeyRelease>', self.on_doc_target_change)
        self.doc_target_text.bind('<Control-Return>', lambda e: self.save_doc_segment_and_next())
        self.doc_target_text.bind('<Control-d>', lambda e: self.copy_source_to_target_doc())
        
        # Action buttons
        button_frame = tk.Frame(editor_frame)
        button_frame.pack(fill='x')
        
        tk.Button(button_frame, text="Copy Source → Target", command=self.copy_source_to_target_doc
                 ).pack(side='left', padx=(0, 5))
        tk.Button(button_frame, text="Clear Target", command=self.clear_doc_target
                 ).pack(side='left', padx=(0, 5))
        tk.Button(button_frame, text="Save & Next (Ctrl+Enter)", command=self.save_doc_segment_and_next,
                 bg='#4CAF50', fg='white').pack(side='right')
        
        # Store segment widgets for later reference
        self.doc_segment_widgets = {}
        self.doc_current_segment = None
        
        # Right side: Assistance panel
        self.create_assistance_panel()
    
    def load_segments_to_document(self):
        """Load segments into document view, grouped by paragraphs and tables"""
        # Clear existing content
        for widget in self.doc_inner_frame.winfo_children():
            widget.destroy()
        
        self.doc_segment_widgets = {}
        
        # Add top padding
        top_spacer = tk.Frame(self.doc_inner_frame, bg='white', height=30)
        top_spacer.pack(side='top', fill='x')
        
        # Use filtered segments if filter is active, otherwise all segments
        segments_to_show = self.filtered_segments if self.filter_active else self.segments
        
        # Debug: Check if we have segments to show
        if not segments_to_show:
            # No segments to display
            no_content_label = tk.Label(self.doc_inner_frame, 
                                       text="No segments to display.\n\nPlease import a document first.",
                                       bg='white', fg='#666', font=('Segoe UI', 12),
                                       pady=50)
            no_content_label.pack(fill='both', expand=True)
            return
        
        # Group segments by paragraph and identify tables
        paragraphs = {}
        tables = {}  # table_id -> {(row, col): segment}
        
        for seg in segments_to_show:
            if seg.is_table_cell and seg.table_info:
                # This is a table cell
                table_id, row_idx, col_idx = seg.table_info
                if table_id not in tables:
                    tables[table_id] = {}
                tables[table_id][(row_idx, col_idx)] = seg
            else:
                # Regular paragraph
                para_id = seg.paragraph_id
                if para_id not in paragraphs:
                    paragraphs[para_id] = []
                paragraphs[para_id].append(seg)
        
        # Render paragraphs and tables in order
        # We need to interleave them based on document position (not segment ID)
        rendered_items = []
        
        # Add paragraphs with their document position for sorting
        for para_id, para_segs in paragraphs.items():
            if para_segs:
                # Use document_position of first segment for sorting
                first_doc_pos = min(s.document_position for s in para_segs)
                rendered_items.append(('para', para_id, first_doc_pos, para_segs))
        
        # Add tables with their document position for sorting
        for table_id, table_cells in tables.items():
            if table_cells:
                # Use document_position of first cell for sorting
                first_doc_pos = min(s.document_position for s in table_cells.values())
                rendered_items.append(('table', table_id, first_doc_pos, table_cells))
        
        # Sort by document position to maintain original document order
        rendered_items.sort(key=lambda x: x[2])
        
        # Render each item
        for item_type, item_id, _, item_data in rendered_items:
            if item_type == 'para':
                self.render_paragraph(item_data)
            elif item_type == 'table':
                self.render_table(item_id, item_data)
        
        # Update scroll region after all content is added
        self.doc_inner_frame.update_idletasks()
        self.doc_canvas.update_idletasks()
        self.doc_canvas.configure(scrollregion=self.doc_canvas.bbox('all'))
    
    def render_paragraph(self, para_segments):
        """Render a paragraph with its segments"""
        # Check if this is a heading or special style
        first_seg = para_segments[0]
        style = first_seg.style
        
        # Create paragraph frame with padding
        para_frame = tk.Frame(self.doc_inner_frame, bg='white')
        para_frame.pack(fill='x', pady=(0, 15), padx=40, anchor='w')
        
        # Determine text style based on paragraph style
        font_size = 11
        font_weight = 'normal'
        font_style = 'roman'
        text_color = '#000000'
        
        if 'Heading 1' in style or 'Title' in style:
            font_size = 16
            font_weight = 'bold'
            text_color = '#003366'
        elif 'Heading 2' in style:
            font_size = 14
            font_weight = 'bold'
            text_color = '#0066cc'
        elif 'Heading 3' in style:
            font_size = 12
            font_weight = 'bold'
            text_color = '#3399ff'
        elif 'Subtitle' in style:
            font_size = 12
            font_style = 'italic'
            text_color = '#663399'
        
        # Create a Text widget for the paragraph (allows inline segments)
        # Set height to a large value initially, will be adjusted after content is added
        para_text = tk.Text(para_frame, wrap='word', bg='white', relief='flat',
                          font=('Segoe UI', font_size, font_weight),
                          fg=text_color, highlightthickness=0, borderwidth=0,
                          cursor='arrow', state='normal', height=50)  # Start with large height
        para_text.pack(fill='both', expand=True)
        
        # Bind mouse wheel to this text widget too
        para_text.bind('<MouseWheel>', lambda e: self.doc_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Insert each segment as a clickable span
        for i, seg in enumerate(para_segments):
            # Add space between sentences (except for first)
            if i > 0:
                para_text.insert('end', ' ')
            
            # Create tag for this segment
            tag_name = f"seg_{seg.id}"
            
            # Determine what to display:
            # - If target has content: show target
            # - If segment was modified but target is empty: show placeholder (user cleared it)
            # - If segment not modified yet: show source (initial state)
            if seg.target and seg.target.strip():
                # Target has content
                display_text = seg.target
            elif seg.modified and seg.target == '':
                # Segment was edited but target was cleared
                display_text = f"[Segment {seg.id} - Empty - Click to edit]"
            elif seg.source:
                # Not yet translated or target is empty, show source
                display_text = seg.source
            else:
                # Both source and target empty
                display_text = f"[Segment {seg.id} - Empty segment]"
            
            start_pos = para_text.index('insert')
            para_text.insert('end', display_text, tag_name)
            end_pos = para_text.index('insert')
            
            # Configure tag appearance based on status
            if seg.status == 'untranslated':
                bg_color = '#ffe6e6'
                hover_bg = '#ffcccc'
            elif seg.status == 'draft':
                bg_color = '#fff9e6'
                hover_bg = '#ffe6b3'
            elif seg.status == 'translated':
                bg_color = '#e6ffe6'
                hover_bg = '#ccffcc'
            elif seg.status == 'approved':
                bg_color = '#e6f3ff'
                hover_bg = '#cce6ff'
            else:
                bg_color = 'white'
                hover_bg = '#f0f0f0'
            
            # Apply tag styling
            para_text.tag_config(tag_name, background=bg_color, relief='flat')
            
            # Apply filter highlighting if active and segment matches
            if self.filter_active and self.should_highlight_segment(seg):
                # Highlight only the specific search terms within the segment
                self.highlight_search_terms_in_segment(para_text, start_pos, end_pos, seg, tag_name)
            
            # Bind click event to enter edit mode
            para_text.tag_bind(tag_name, '<Button-1>', 
                             lambda e, s=seg, pt=para_text, tn=tag_name: self.on_doc_segment_click(s, pt, tn))
            
            # Bind hover effects
            para_text.tag_bind(tag_name, '<Enter>', 
                             lambda e, pt=para_text, tn=tag_name, hbg=hover_bg: pt.tag_config(tn, background=hbg, relief='raised'))
            para_text.tag_bind(tag_name, '<Leave>', 
                             lambda e, pt=para_text, tn=tag_name, bg=bg_color: pt.tag_config(tn, background=bg, relief='flat'))
            
            # Store widget reference
            self.doc_segment_widgets[seg.id] = {
                'text_widget': para_text,
                'tag_name': tag_name,
                'segment': seg,
                'start': start_pos,
                'end': end_pos
            }
        
        # Make paragraph read-only
        para_text.config(state='disabled')
        
        # Now calculate the actual height needed for wrapped content
        para_text.update_idletasks()
        
        # Count the number of display lines (wrapped)
        # This uses dlineinfo which gives us info about each display line
        actual_lines = 0
        index = '1.0'
        while True:
            dline = para_text.dlineinfo(index)
            if dline is None:
                break
            actual_lines += 1
            # Move to next display line
            index = para_text.index(f"{index} + 1 display lines")
            if para_text.compare(index, '>=', 'end'):
                break
        
        # Set height to actual number of display lines (minimum 1)
        para_text.config(height=max(1, actual_lines))
    
    def render_table(self, table_id, table_cells):
        """Render a table with its cells"""
        # Find table dimensions
        max_row = max(pos[0] for pos in table_cells.keys())
        max_col = max(pos[1] for pos in table_cells.keys())
        
        # Create table frame with padding
        table_frame = tk.Frame(self.doc_inner_frame, bg='white')
        table_frame.pack(fill='x', pady=(0, 15), padx=40, anchor='w')
        
        # Create table grid
        for row_idx in range(max_row + 1):
            for col_idx in range(max_col + 1):
                seg = table_cells.get((row_idx, col_idx))
                
                if seg:
                    # Determine what to display
                    if seg.target and seg.target.strip():
                        display_text = seg.target
                    elif seg.modified and seg.target == '':
                        display_text = f"[Segment {seg.id} - Empty - Click to edit]"
                    elif seg.source:
                        display_text = seg.source
                    else:
                        display_text = f"[Segment {seg.id} - Empty segment]"
                    
                    # Configure tag appearance based on status
                    if seg.status == 'untranslated':
                        bg_color = '#ffe6e6'
                        hover_bg = '#ffcccc'
                    elif seg.status == 'draft':
                        bg_color = '#fff9e6'
                        hover_bg = '#ffe6b3'
                    elif seg.status == 'translated':
                        bg_color = '#e6ffe6'
                        hover_bg = '#ccffcc'
                    elif seg.status == 'approved':
                        bg_color = '#e6f3ff'
                        hover_bg = '#cce6ff'
                    else:
                        bg_color = 'white'
                        hover_bg = '#f0f0f0'
                    
                    # Create cell frame
                    cell_frame = tk.Frame(table_frame, relief='solid', bd=1, bg=bg_color)
                    cell_frame.grid(row=row_idx, column=col_idx, sticky='nsew', padx=1, pady=1)
                    
                    # Create text widget for cell
                    cell_text = tk.Text(cell_frame, wrap='word', font=('Segoe UI', 9),
                                       bg=bg_color, relief='flat', bd=0,
                                       highlightthickness=0, cursor='arrow',
                                       state='normal', height=1, width=20)
                    cell_text.pack(fill='both', expand=True, padx=3, pady=3)
                    
                    # Create tag for this cell
                    tag_name = f"seg_{seg.id}"
                    cell_text.insert('1.0', display_text, tag_name)
                    
                    # Apply tag styling
                    cell_text.tag_config(tag_name, background=bg_color, relief='flat')
                    
                    # Apply filter highlighting if active and segment matches
                    if self.filter_active and self.should_highlight_segment(seg):
                        # Highlight only the specific search terms within the cell
                        self.highlight_search_terms_in_segment(cell_text, '1.0', 'end-1c', seg, tag_name)
                    
                    # Bind click event
                    cell_text.tag_bind(tag_name, '<Button-1>',
                                     lambda e, s=seg, ct=cell_text, tn=tag_name: self.on_doc_segment_click(s, ct, tn))
                    
                    # Bind hover effects
                    cell_text.tag_bind(tag_name, '<Enter>',
                                     lambda e, ct=cell_text, tn=tag_name, hbg=hover_bg: ct.tag_config(tn, background=hbg, relief='raised'))
                    cell_text.tag_bind(tag_name, '<Leave>',
                                     lambda e, ct=cell_text, tn=tag_name, bg=bg_color: ct.tag_config(tn, background=bg, relief='flat'))
                    
                    # Bind mouse wheel
                    cell_text.bind('<MouseWheel>', lambda e: self.doc_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
                    
                    # Make read-only
                    cell_text.config(state='disabled')
                    
                    # Calculate height
                    cell_text.update_idletasks()
                    actual_lines = int(cell_text.index('end-1c').split('.')[0])
                    cell_text.config(height=max(1, actual_lines))
                    
                    # Store widget reference
                    self.doc_segment_widgets[seg.id] = {
                        'text_widget': cell_text,
                        'tag_name': tag_name,
                        'segment': seg,
                        'start': '1.0',
                        'end': 'end'
                    }
        
        # Make columns expand equally
        for col_idx in range(max_col + 1):
            table_frame.grid_columnconfigure(col_idx, weight=1, uniform="table_col")
    
    def on_doc_segment_click(self, segment, para_text, tag_name):
        """Handle click on a segment in document view - load into editor panel"""
        # Save any current edit first
        if self.doc_current_segment and self.doc_current_segment != segment:
            self.save_doc_segment()
        
        # Highlight the selected segment in the document
        if self.doc_current_segment:
            # Remove highlight from previous segment
            old_widget_info = self.doc_segment_widgets.get(self.doc_current_segment.id)
            if old_widget_info:
                old_tag = old_widget_info['tag_name']
                old_text = old_widget_info['text_widget']
                # Restore original status color
                if self.doc_current_segment.status == 'untranslated':
                    bg_color = '#ffe6e6'
                elif self.doc_current_segment.status == 'draft':
                    bg_color = '#fff9e6'
                elif self.doc_current_segment.status == 'translated':
                    bg_color = '#e6ffe6'
                elif self.doc_current_segment.status == 'approved':
                    bg_color = '#e6f3ff'
                else:
                    bg_color = 'white'
                old_text.tag_config(old_tag, background=bg_color, relief='flat', borderwidth=0)
        
        # Set current segment
        self.doc_current_segment = segment
        self.current_segment = segment
        
        # Highlight selected segment with a border
        para_text.tag_config(tag_name, relief='solid', borderwidth=2)
        
        # Scroll to make the segment visible
        # Get the text widget's position and scroll to it
        try:
            para_text.see(tag_name + '.first')
            # Also scroll the canvas to show this text widget
            self.doc_canvas.update_idletasks()
            # Get the bbox of the paragraph's parent frame
            para_frame = para_text.master
            para_frame.update_idletasks()
            # Scroll canvas to show the frame
            self.doc_canvas.yview_moveto(0)  # Reset
            bbox = self.doc_canvas.bbox('all')
            if bbox:
                # Calculate relative position
                para_y = para_frame.winfo_y()
                total_height = bbox[3] - bbox[1]
                if total_height > 0:
                    scroll_pos = para_y / total_height
                    self.doc_canvas.yview_moveto(max(0, scroll_pos - 0.1))  # Scroll with 10% margin
        except:
            pass
        
        # Load segment into editor panel
        self.doc_seg_info_label.config(text=f"Segment #{segment.id} - {segment.style}")
        
        # Update source
        self.doc_source_text.config(state='normal')
        self.doc_source_text.delete('1.0', 'end')
        self.doc_source_text.insert('1.0', segment.source)
        self.doc_source_text.config(state='disabled')
        
        # Update target
        self.doc_target_text.delete('1.0', 'end')
        if segment.target:
            self.doc_target_text.insert('1.0', segment.target)
        
        # Update status
        self.doc_status_var.set(segment.status)
        
        # Focus target text
        self.doc_target_text.focus_set()
        
        self.log(f"Editing Segment #{segment.id}")
    
    def on_doc_target_change(self, event=None):
        """Handle changes to target text in document view"""
        # No need to do anything here - just allow typing
        pass
    
    def on_doc_status_change(self, event=None):
        """Handle status change in document view"""
        if not self.doc_current_segment:
            return
        
        new_status = self.doc_status_var.get()
        self.doc_current_segment.status = new_status
        self.doc_current_segment.modified = True
        self.modified = True
        self.update_progress()
        
        # Update the segment's background color in the document
        widget_info = self.doc_segment_widgets.get(self.doc_current_segment.id)
        if widget_info:
            tag_name = widget_info['tag_name']
            para_text = widget_info['text_widget']
            
            if new_status == 'untranslated':
                bg_color = '#ffe6e6'
            elif new_status == 'draft':
                bg_color = '#fff9e6'
            elif new_status == 'translated':
                bg_color = '#e6ffe6'
            elif new_status == 'approved':
                bg_color = '#e6f3ff'
            else:
                bg_color = 'white'
            
            para_text.tag_config(tag_name, background=bg_color)
        
        self.log(f"✓ Status changed to {new_status}")
    
    def save_doc_segment(self):
        """Save current segment in document view"""
        if not self.doc_current_segment:
            return
        
        # Get new target text
        new_target = self.doc_target_text.get('1.0', 'end-1c')
        
        # Update segment
        self.doc_current_segment.target = new_target
        if self.doc_current_segment.status == 'untranslated' and new_target:
            self.doc_current_segment.status = 'draft'
            self.doc_status_var.set('draft')
        self.doc_current_segment.modified = True
        
        # Update the text in the document view
        widget_info = self.doc_segment_widgets.get(self.doc_current_segment.id)
        if widget_info:
            tag_name = widget_info['tag_name']
            para_text = widget_info['text_widget']
            
            # Get the range of the tag
            ranges = para_text.tag_ranges(tag_name)
            if len(ranges) >= 2:
                start, end = ranges[0], ranges[1]
                
                # Determine what to display based on new target
                if new_target.strip():
                    # Target has content
                    display_text = new_target
                elif new_target == '' and self.doc_current_segment.modified:
                    # Target explicitly cleared by user (and segment was modified)
                    display_text = f"[Segment {self.doc_current_segment.id} - Empty - Click to edit]"
                elif self.doc_current_segment.source:
                    # Fallback to source
                    display_text = self.doc_current_segment.source
                else:
                    # Both empty
                    display_text = f"[Segment {self.doc_current_segment.id} - Empty segment]"
                
                # Replace the text
                para_text.config(state='normal')
                para_text.delete(start, end)
                para_text.insert(start, display_text, tag_name)
                para_text.config(state='disabled')
                
                # Update background color based on status
                if self.doc_current_segment.status == 'draft':
                    bg_color = '#fff9e6'
                elif self.doc_current_segment.status == 'translated':
                    bg_color = '#e6ffe6'
                elif self.doc_current_segment.status == 'approved':
                    bg_color = '#e6f3ff'
                else:
                    bg_color = '#ffe6e6'
                
                para_text.tag_config(tag_name, background=bg_color)
        
        self.modified = True
        self.update_progress()
        self.log(f"✓ Segment #{self.doc_current_segment.id} saved")
    
    def save_doc_segment_and_next(self):
        """Save current segment and move to next"""
        if self.doc_current_segment:
            self.save_doc_segment()
            
            # Find next segment
            current_id = self.doc_current_segment.id
            for seg in self.segments:
                if seg.id > current_id:
                    if seg.id in self.doc_segment_widgets:
                        widget_info = self.doc_segment_widgets[seg.id]
                        self.on_doc_segment_click(seg, widget_info['text_widget'], widget_info['tag_name'])
                    break
        return 'break'
    
    def copy_source_to_target_doc(self):
        """Copy source to target in document view"""
        if not self.doc_current_segment:
            return 'break'
        
        # Copy source to target text widget
        self.doc_target_text.delete('1.0', 'end')
        self.doc_target_text.insert('1.0', self.doc_current_segment.source)
        
        self.log(f"✓ Copied source to target (Segment #{self.doc_current_segment.id})")
        return 'break'
    
    def clear_doc_target(self):
        """Clear target text in document view"""
        self.doc_target_text.delete('1.0', 'end')
    
    def navigate_document_segment(self, direction='next'):
        """Navigate to next/previous segment in document view"""
        if not self.doc_current_segment:
            # No current segment, select first
            if self.segments and self.segments[0].id in self.doc_segment_widgets:
                widget_info = self.doc_segment_widgets[self.segments[0].id]
                self.on_doc_segment_click(self.segments[0], widget_info['text_widget'], widget_info['tag_name'])
            return
        
        # Save current segment first
        self.save_doc_segment()
        
        current_id = self.doc_current_segment.id
        
        if direction == 'next':
            # Find next segment
            for seg in self.segments:
                if seg.id > current_id:
                    if seg.id in self.doc_segment_widgets:
                        widget_info = self.doc_segment_widgets[seg.id]
                        self.on_doc_segment_click(seg, widget_info['text_widget'], widget_info['tag_name'])
                    break
        else:
            # Find previous segment
            for seg in reversed(self.segments):
                if seg.id < current_id:
                    if seg.id in self.doc_segment_widgets:
                        widget_info = self.doc_segment_widgets[seg.id]
                        self.on_doc_segment_click(seg, widget_info['text_widget'], widget_info['tag_name'])
                    break
    
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
        
        # Save current segment if editing
        if hasattr(self, 'current_edit_widget') and self.current_edit_widget:
            try:
                # Check if widget still exists before trying to save
                if self.current_edit_widget.winfo_exists():
                    self.save_grid_edit(go_next=False)
            except:
                pass  # Widget already destroyed
            finally:
                self.current_edit_widget = None
        elif self.layout_mode == LayoutMode.DOCUMENT and hasattr(self, 'doc_current_segment') and self.doc_current_segment:
            try:
                self.save_doc_segment()
            except:
                pass  # Widget already destroyed
        
        # Remember current selection from any view mode
        current_seg_id = None
        if self.layout_mode == LayoutMode.GRID and self.current_segment:
            current_seg_id = self.current_segment.id
        elif self.layout_mode == LayoutMode.DOCUMENT and hasattr(self, 'doc_current_segment') and self.doc_current_segment:
            current_seg_id = self.doc_current_segment.id
        elif self.layout_mode == LayoutMode.SPLIT and hasattr(self, 'current_segment') and self.current_segment:
            current_seg_id = self.current_segment.id
        
        # Update layout mode
        self.layout_mode = new_mode
        
        # Update button states
        self.update_layout_buttons()
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Rebuild UI based on layout mode
        if new_mode == LayoutMode.GRID:
            self.create_grid_layout()
            self.load_segments_to_grid()
            # Restore selection
            if current_seg_id:
                for i, row_data in enumerate(self.grid_rows):
                    if row_data['segment'].id == current_seg_id:
                        self.select_grid_row(i)
                        break
        elif new_mode == LayoutMode.SPLIT:
            self.create_split_layout()
            self.load_segments_to_tree()
            # Restore selection
            if current_seg_id:
                for item in self.tree.get_children():
                    if int(self.tree.item(item)['values'][0]) == current_seg_id:
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        # Trigger selection event to load segment in editor
                        self.on_segment_select(None)
                        break
        elif new_mode == LayoutMode.DOCUMENT:
            self.create_document_layout()
            self.load_segments_to_document()
            # Restore selection by clicking first segment
            if current_seg_id and current_seg_id in self.doc_segment_widgets:
                widget_info = self.doc_segment_widgets[current_seg_id]
                self.on_doc_segment_click(widget_info['segment'], 
                                        widget_info['text_widget'], 
                                        widget_info['tag_name'])
        
        mode_names = {
            LayoutMode.GRID: "Grid View (memoQ-style)",
            LayoutMode.SPLIT: "List View",
            LayoutMode.DOCUMENT: "Document View (Flow)"
        }
        self.log(f"✓ Switched to {mode_names.get(new_mode, new_mode)}")
    
    def update_layout_buttons(self):
        """Update layout button visual states"""
        # Reset all buttons
        self.layout_btn_grid.config(relief='raised', bg='#E0E0E0', fg='black')
        self.layout_btn_split.config(relief='raised', bg='#E0E0E0', fg='black')
        self.layout_btn_document.config(relief='raised', bg='#E0E0E0', fg='black')
        
        # Highlight active button
        if self.layout_mode == LayoutMode.GRID:
            self.layout_btn_grid.config(relief='sunken', bg='#9C27B0', fg='white')
        elif self.layout_mode == LayoutMode.SPLIT:
            self.layout_btn_split.config(relief='sunken', bg='#9C27B0', fg='white')
        elif self.layout_mode == LayoutMode.DOCUMENT:
            self.layout_btn_document.config(relief='sunken', bg='#9C27B0', fg='white')
    
    # Custom Grid View methods
    
    def create_grid_header(self):
        """Create sticky header row for custom grid with resizable columns"""
        header_frame = tk.Frame(self.header_container, bg='#e0e0e0', relief='raised', bd=1)
        header_frame.pack(fill='x', side='top', pady=0)
        
        # Fixed columns - match exact row layout (Type, Style, Status order)
        for col_name in ['id', 'type', 'style', 'status']:
            col_info = self.grid_columns[col_name]
            if not col_info.get('visible', True):
                continue  # Skip hidden columns
            
            header_label = tk.Label(header_frame, 
                                   text=col_info['title'],
                                   font=('Segoe UI', 9, 'bold'),
                                   bg='#e0e0e0',
                                   fg='black',
                                   width=col_info['width'] // 8,
                                   anchor=col_info['anchor'],
                                   relief='raised',
                                   bd=1)
            header_label.pack(side='left', padx=1, pady=1)
        
        # Create container frame to match row structure
        header_content = tk.Frame(header_frame, bg='#e0e0e0')
        header_content.pack(side='left', fill='both', expand=True)
        
        # Source header - fixed width frame to match row source_frame
        source_header_frame = tk.Frame(header_content, bg='#e0e0e0', width=self.source_width)
        source_header_frame.pack(side='left', fill='both', expand=False)
        source_header_frame.pack_propagate(False)
        
        self.source_header = tk.Label(source_header_frame, 
                               text='📄 Source',
                               font=('Segoe UI', 9, 'bold'),
                               bg='#e0e0e0',
                               fg='black',
                               anchor='w',
                               relief='raised',
                               bd=1)
        self.source_header.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Draggable splitter - exactly 4px to match row splitter_space
        self.splitter = tk.Frame(header_content, bg='#666', width=4, cursor='sb_h_double_arrow', relief='raised')
        self.splitter.pack(side='left', fill='y', pady=0)
        
        # Bind splitter dragging events
        self.splitter.bind('<Button-1>', self.start_splitter_drag)
        self.splitter.bind('<B1-Motion>', self.on_splitter_drag)
        self.splitter.bind('<ButtonRelease-1>', self.end_splitter_drag)
        
        # Target header - expanding frame to match row target_frame
        target_header_frame = tk.Frame(header_content, bg='#e0e0e0')
        target_header_frame.pack(side='left', fill='both', expand=True)
        
        self.target_header = tk.Label(target_header_frame, 
                               text='🎯 Target',
                               font=('Segoe UI', 9, 'bold'),
                               bg='#e0e0e0',
                               fg='black',
                               anchor='w',
                               relief='raised',
                               bd=1)
        self.target_header.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Store header frames for width updates
        self.source_header_frame = source_header_frame
        self.target_header_frame = target_header_frame
    
    def update_header_widths(self):
        """Update header frame widths based on current source/target widths"""
        self.source_header_frame.config(width=self.source_width)
    
    def start_splitter_drag(self, event):
        """Start dragging the column splitter"""
        self.dragging_splitter = True
        self.drag_start_x = event.x_root
        self.drag_start_source_width = self.source_width
        self.drag_start_target_width = self.target_width
    
    def on_splitter_drag(self, event):
        """Handle splitter dragging"""
        if not self.dragging_splitter:
            return
        
        # Calculate delta
        delta = event.x_root - self.drag_start_x
        
        # Update widths (keep minimum of 200px each)
        new_source_width = max(200, self.drag_start_source_width + delta)
        new_target_width = max(200, self.drag_start_target_width - delta)
        
        self.source_width = new_source_width
        self.target_width = new_target_width
        
        # Update column config
        self.grid_columns['source']['width'] = self.source_width
        self.grid_columns['target']['width'] = self.target_width
        
        # Update headers
        self.update_header_widths()
        
        # Update all rows
        self.update_all_row_widths()
    
    def end_splitter_drag(self, event):
        """End dragging the column splitter"""
        self.dragging_splitter = False
    
    def update_all_row_widths(self):
        """Update all row column widths after splitter drag"""
        for row_data in self.grid_rows:
            widgets = row_data['widgets']
            
            # Update source frame width (fixed)
            if 'source_frame' in widgets:
                widgets['source_frame'].config(width=self.source_width)
            
            # Target frame expands automatically, no need to set width
        
        # Update canvas
        self.grid_canvas.update_idletasks()
        self.update_grid_scroll_region()
    
    def show_column_visibility_dialog(self):
        """Show dialog to toggle column visibility"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Grid View - Show/Hide Columns")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select columns to display:", 
                font=('Segoe UI', 10, 'bold')).pack(pady=10)
        
        # Create checkboxes for each column (except source/target which are always visible)
        # Order matches the actual column order: Type, Style, Status
        checkbox_vars = {}
        for col_name in ['id', 'type', 'style', 'status']:
            var = tk.BooleanVar(value=self.grid_columns[col_name].get('visible', True))
            checkbox_vars[col_name] = var
            
            cb = tk.Checkbutton(dialog, 
                              text=self.grid_columns[col_name]['title'],
                              variable=var,
                              font=('Segoe UI', 10))
            cb.pack(anchor='w', padx=20, pady=5)
        
        # Note about source/target
        tk.Label(dialog, text="Note: Source and Target are always visible",
                fg='gray', font=('Segoe UI', 8)).pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def apply_changes():
            # Update column visibility
            for col_name, var in checkbox_vars.items():
                self.grid_columns[col_name]['visible'] = var.get()
            
            # Rebuild grid
            self.rebuild_grid()
            dialog.destroy()
            self.log("Column visibility updated")
        
        def cancel():
            dialog.destroy()
        
        tk.Button(button_frame, text="Apply", command=apply_changes, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=cancel, width=10).pack(side='left', padx=5)
    
    def rebuild_grid(self):
        """Rebuild the entire grid (e.g., after column visibility changes)"""
        if self.layout_mode != LayoutMode.GRID:
            return
        
        # Store current selection
        current_selection = self.current_row_index
        
        # Clear existing grid
        for widget in self.grid_inner_frame.winfo_children():
            widget.destroy()
        self.grid_rows.clear()
        
        # Clear header
        for widget in self.header_container.winfo_children():
            widget.destroy()
        
        # Recreate header
        self.create_grid_header()
        
        # Recreate all rows
        segments = self.segments if not self.filter_active else self.filtered_segments
        for segment in segments:
            self.add_grid_row(segment)
        
        # Restore selection
        if 0 <= current_selection < len(self.grid_rows):
            self.select_grid_row(current_selection)
        
        # Update scroll region
        self.grid_canvas.update_idletasks()
        self.update_grid_scroll_region()
    
    def toggle_grid_style_colors(self):
        """Toggle style-based font colors in Grid View"""
        self.grid_style_colors_enabled = not self.grid_style_colors_enabled
        status = "enabled" if self.grid_style_colors_enabled else "disabled"
        self.log(f"Style colors {status}")
        
        # Rebuild grid to apply changes
        if self.layout_mode == LayoutMode.GRID:
            self.rebuild_grid()
    
    def apply_formatting_to_text_widget(self, text_widget, text_content, segment=None):
        """Apply visual formatting (bold, italic, underline) and style colors to text in a Text widget"""
        import re
        
        # Configure text tags for formatting
        text_widget.tag_configure('bold', font=('Segoe UI', 9, 'bold'))
        text_widget.tag_configure('italic', font=('Segoe UI', 9, 'italic'))
        text_widget.tag_configure('underline', font=('Segoe UI', 9, 'underline'))
        
        # Apply style-based colors if enabled (matching List View)
        if self.grid_style_colors_enabled and segment:
            if segment.is_table_cell:
                text_widget.tag_configure('style_color', foreground='#0066cc', font=('Segoe UI', 9, 'italic'))
                text_widget.tag_add('style_color', '1.0', 'end')
            elif segment.style:
                style_lower = segment.style.lower()
                if 'heading 1' in style_lower:
                    text_widget.tag_configure('style_color', foreground='#003366', font=('Segoe UI', 10, 'bold'))
                    text_widget.tag_add('style_color', '1.0', 'end')
                elif 'heading 2' in style_lower:
                    text_widget.tag_configure('style_color', foreground='#0066cc', font=('Segoe UI', 9, 'bold'))
                    text_widget.tag_add('style_color', '1.0', 'end')
                elif 'heading 3' in style_lower:
                    text_widget.tag_configure('style_color', foreground='#3399ff', font=('Segoe UI', 9, 'bold'))
                    text_widget.tag_add('style_color', '1.0', 'end')
                elif 'title' in style_lower and 'subtitle' not in style_lower:
                    text_widget.tag_configure('style_color', foreground='#663399', font=('Segoe UI', 11, 'bold'))
                    text_widget.tag_add('style_color', '1.0', 'end')
                elif 'subtitle' in style_lower:
                    text_widget.tag_configure('style_color', foreground='#663399', font=('Segoe UI', 9, 'italic'))
                    text_widget.tag_add('style_color', '1.0', 'end')
        
        # Find and apply bold tags <b>...</b>
        for match in re.finditer(r'<b>(.*?)</b>', text_content, re.DOTALL):
            start_pos = f"1.0 + {match.start()} chars"
            end_pos = f"1.0 + {match.end()} chars"
            # Get the actual position of the content (without tags)
            content_start = f"1.0 + {match.start(1)} chars"
            content_end = f"1.0 + {match.end(1)} chars"
            text_widget.tag_add('bold', content_start, content_end)
        
        # Find and apply italic tags <i>...</i>
        for match in re.finditer(r'<i>(.*?)</i>', text_content, re.DOTALL):
            content_start = f"1.0 + {match.start(1)} chars"
            content_end = f"1.0 + {match.end(1)} chars"
            text_widget.tag_add('italic', content_start, content_end)
        
        # Find and apply underline tags <u>...</u>
        for match in re.finditer(r'<u>(.*?)</u>', text_content, re.DOTALL):
            content_start = f"1.0 + {match.start(1)} chars"
            content_end = f"1.0 + {match.end(1)} chars"
            text_widget.tag_add('underline', content_start, content_end)
    
    def calculate_row_height(self, segment):
        """Calculate appropriate row height based on content with word wrapping"""
        import textwrap
        
        # Calculate character width based on actual column widths
        # Approximate: 8px per character
        source_width_chars = max(30, self.source_width // 8)
        target_width_chars = max(30, self.target_width // 8)
        
        # Calculate wrapped lines for source
        source_lines = 0
        if segment.source:
            # Split by existing newlines first
            source_paragraphs = segment.source.split('\n')
            for para in source_paragraphs:
                if para:
                    # Calculate how many lines this paragraph will wrap to
                    wrapped = textwrap.fill(para, width=source_width_chars)
                    source_lines += wrapped.count('\n') + 1
                else:
                    source_lines += 1
        
        # Calculate wrapped lines for target
        target_lines = 0
        if segment.target:
            target_paragraphs = segment.target.split('\n')
            for para in target_paragraphs:
                if para:
                    wrapped = textwrap.fill(para, width=target_width_chars)
                    target_lines += wrapped.count('\n') + 1
                else:
                    target_lines += 1
        else:
            target_lines = 1
        
        # Use the maximum of source and target
        max_lines = max(source_lines, target_lines)
        
        # Calculate height: 18px per line + 15px padding
        # Minimum 35px, maximum 250px
        height = max(35, min(250, max_lines * 18 + 15))
        
        return height
    
    def update_grid_scroll_region(self, event=None):
        """Update the scroll region of the canvas"""
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox('all'))
    
    def on_grid_canvas_resize(self, event):
        """Handle canvas resize to adjust inner frame width"""
        canvas_width = event.width
        self.grid_canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def on_grid_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.grid_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def on_grid_click(self, event):
        """Handle click on grid to select row"""
        # Find which row was clicked
        y_pos = self.grid_canvas.canvasy(event.y)
        
        for i, row_data in enumerate(self.grid_rows):
            row_frame = row_data['row_frame']
            if row_frame.winfo_y() <= y_pos <= row_frame.winfo_y() + row_frame.winfo_height():
                self.select_grid_row(i)
                self.grid_canvas.focus_set()
                break
    
    def on_grid_double_click(self, event):
        """Handle double-click to enter edit mode or show source"""
        # Find which row and column was clicked
        y_pos = self.grid_canvas.canvasy(event.y)
        x_pos = self.grid_canvas.canvasx(event.x)
        
        for i, row_data in enumerate(self.grid_rows):
            row_frame = row_data['row_frame']
            if row_frame.winfo_y() <= y_pos <= row_frame.winfo_y() + row_frame.winfo_height():
                self.select_grid_row(i)
                
                # Determine which column was clicked
                col_x = 0
                for col_name, col_info in self.grid_columns.items():
                    if col_x <= x_pos <= col_x + col_info['width']:
                        if col_name == 'target':
                            self.enter_edit_mode()
                        elif col_name == 'source':
                            self.show_source_popup(event)
                        break
                    col_x += col_info['width']
                break
    
    def show_grid_context_menu(self, event):
        """Show context menu for grid"""
        # Select row first
        self.on_grid_click(event)
        self.context_menu.post(event.x_root, event.y_root)
    
    def on_text_widget_click(self, event, row_index):
        """Handle click on source text widget - just select the row"""
        self.select_grid_row(row_index)
        return 'break'  # Prevent default Text widget behavior
    
    def on_target_click(self, event, row_index):
        """Handle single click on target - select row and enter edit mode"""
        # Select the row first
        self.select_grid_row(row_index)
        
        # Enter edit mode immediately
        self.enter_edit_mode()
        
        return 'break'  # Prevent default Text widget behavior
    
    def on_target_double_click(self, event, row_index):
        """Handle double-click on target - enter edit mode directly"""
        # Select the row first
        self.select_grid_row(row_index)
        
        # Enter edit mode for this row
        self.enter_edit_mode()
        
        return 'break'
    
    def on_source_right_click(self, event, row_index):
        """Handle right-click on source - select row and show source popup"""
        self.select_grid_row(row_index)
        self.show_source_popup(event)
        return 'break'
    
    def on_target_right_click(self, event, row_index):
        """Handle right-click on target - select row and show context menu"""
        self.select_grid_row(row_index)
        self.context_menu.post(event.x_root, event.y_root)
        return 'break'
    
    def select_grid_row(self, row_index):
        """Select a row in the custom grid"""
        if row_index < 0 or row_index >= len(self.grid_rows):
            return
        
        # Clear dual selection if changing rows
        if self.dual_selection_row is not None and self.dual_selection_row != row_index:
            self.clear_dual_selection()
        
        # Deselect previous row
        if self.current_row_index >= 0 and self.current_row_index < len(self.grid_rows):
            old_row = self.grid_rows[self.current_row_index]['row_frame']
            old_row.config(relief='flat', bd=1)
        
        # Select new row
        self.current_row_index = row_index
        row_data = self.grid_rows[row_index]
        row_frame = row_data['row_frame']
        row_frame.config(relief='solid', bd=2)
        
        # Update current segment
        self.current_segment = row_data['segment']
        
        # Ensure row is visible - scroll to it smoothly
        self.grid_canvas.update_idletasks()
        
        # Get canvas viewport height and row position
        canvas_height = self.grid_canvas.winfo_height()
        row_y = row_frame.winfo_y()
        row_height = row_frame.winfo_height()
        
        # Get current scroll position
        scroll_region = self.grid_canvas.cget('scrollregion').split()
        if len(scroll_region) == 4:
            total_height = float(scroll_region[3])
            
            # Check if row is visible
            current_view = self.grid_canvas.yview()
            view_top = current_view[0] * total_height
            view_bottom = current_view[1] * total_height
            
            # Only scroll if row is not fully visible
            if row_y < view_top:
                # Row is above viewport - scroll to show it at top
                self.grid_canvas.yview_moveto(row_y / total_height)
            elif row_y + row_height > view_bottom:
                # Row is below viewport - scroll to show it at bottom
                self.grid_canvas.yview_moveto((row_y + row_height - canvas_height) / total_height)
        
        # Load segment into editor panel
        self.load_segment_to_grid_editor(self.current_segment)
    
    def should_highlight_segment(self, segment):
        """
        Check if a segment matches the current filter criteria.
        Used in Highlight Mode to determine which segments to highlight.
        In Filter Mode, all visible segments already match, so highlighting is always applied.
        In Highlight Mode, all segments are visible, so we only highlight those that match.
        """
        # In filter mode, all visible segments match (already filtered)
        if self.filter_mode == 'filter':
            return True
        
        # In highlight mode, check if this segment matches the filters
        source_filter = self.filter_source_var.get().strip().lower()
        target_filter = self.filter_target_var.get().strip().lower()
        status_filter = self.filter_status_var.get()
        
        # Check source filter
        if source_filter and source_filter not in segment.source.lower():
            return False
        
        # Check target filter
        if target_filter and target_filter not in segment.target.lower():
            return False
        
        # Check status filter
        if status_filter != "All" and segment.status != status_filter:
            return False
        
        return True
    
    def highlight_search_terms_in_segment(self, text_widget, start_index, end_index, segment, tag_name):
        """
        Highlight only the specific search terms within a segment in Document View.
        This provides more precise visual feedback than highlighting the entire segment.
        """
        source_filter = self.filter_source_var.get().strip().lower()
        target_filter = self.filter_target_var.get().strip().lower()
        
        # Get the text content from the widget
        segment_text = text_widget.get(start_index, end_index)
        
        # Determine which text to search in based on what's displayed
        # If target has content, we're showing target; otherwise showing source
        if segment.target and segment.target.strip():
            display_text = segment.target
            search_term = target_filter
        else:
            display_text = segment.source
            search_term = source_filter
        
        # If we have a search term, highlight all occurrences
        if search_term:
            # Search for all occurrences (case-insensitive)
            search_lower = display_text.lower()
            search_term_lower = search_term.lower()
            
            start_pos = 0
            occurrence_count = 0
            
            while True:
                # Find next occurrence
                pos = search_lower.find(search_term_lower, start_pos)
                if pos == -1:
                    break
                
                # Calculate the actual position in the Text widget
                # We need to account for the start_index offset
                match_start = f"{start_index} + {pos} chars"
                match_end = f"{start_index} + {pos + len(search_term)} chars"
                
                # Create a unique tag for this highlight
                highlight_tag = f"search_highlight_{segment.id}_{occurrence_count}"
                
                # Add the tag to this occurrence
                text_widget.tag_add(highlight_tag, match_start, match_end)
                
                # Configure the tag with bright yellow background and bold
                text_widget.tag_config(highlight_tag, 
                                     background='#FFFF00',  # Bright yellow
                                     foreground='#000000',  # Black text
                                     font=('Segoe UI', 11, 'bold'))
                
                # Raise the tag so it appears above the segment background
                text_widget.tag_raise(highlight_tag)
                
                occurrence_count += 1
                start_pos = pos + 1  # Move past this occurrence to find next one
    
    def add_grid_row(self, segment):
        """Add a row to the custom grid with dynamic height"""
        # Calculate row height based on content
        row_height = self.calculate_row_height(segment)
        
        # Determine type label
        if segment.is_table_cell and segment.table_info:
            type_text = f"T{segment.table_info[0]+1}R{segment.table_info[1]+1}C{segment.table_info[2]+1}"
        else:
            type_text = "Para"
        
        # Determine background color based on status
        status_colors = {
            'untranslated': '#ffe6e6',
            'draft': '#fff9e6',
            'translated': '#e6ffe6',
            'approved': '#e6f3ff'
        }
        bg_color = status_colors.get(segment.status, 'white')
        
        # Create row frame
        row_frame = tk.Frame(self.grid_inner_frame, bg=bg_color, relief='flat', bd=1, height=row_height)
        row_frame.pack(fill='x', side='top', pady=0)
        row_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Create widgets for each column
        widgets = {}
        
        # ID column
        if self.grid_columns['id'].get('visible', True):
            id_label = tk.Label(row_frame, text=str(segment.id), 
                               bg=bg_color, font=('Segoe UI', 9),
                               width=self.grid_columns['id']['width'] // 8,
                               anchor='center')
            id_label.pack(side='left', padx=1)
            widgets['id'] = id_label
        
        # Type column
        if self.grid_columns['type'].get('visible', True):
            type_label = tk.Label(row_frame, text=type_text, 
                                 bg=bg_color, font=('Segoe UI', 9),
                                 width=self.grid_columns['type']['width'] // 8,
                                 anchor='center')
            type_label.pack(side='left', padx=1)
            widgets['type'] = type_label
        
        # Style column
        if self.grid_columns['style'].get('visible', True):
            style_text = segment.style if segment.style else "Normal"
            style_label = tk.Label(row_frame, text=style_text, 
                                  bg=bg_color, font=('Segoe UI', 9),
                                  width=self.grid_columns['style']['width'] // 8,
                                  anchor='center')
            style_label.pack(side='left', padx=1)
            widgets['style'] = style_label
        
        # Status column
        if self.grid_columns['status'].get('visible', True):
            status_label = tk.Label(row_frame, text=segment.status, 
                                   bg=bg_color, font=('Segoe UI', 9),
                                   width=self.grid_columns['status']['width'] // 8,
                                   anchor='center')
            status_label.pack(side='left', padx=1)
            widgets['status'] = status_label
        
        # Create a container frame for source + splitter + target to match header layout
        content_container = tk.Frame(row_frame, bg=bg_color)
        content_container.pack(side='left', fill='both', expand=True)
        
        # Source column (Text widget for multi-line, read-only) - fixed width
        source_frame = tk.Frame(content_container, bg=bg_color, width=self.source_width)
        source_frame.pack(side='left', fill='both', expand=False)
        source_frame.pack_propagate(False)
        
        source_text = tk.Text(source_frame, wrap='word', font=('Segoe UI', 9),
                             bg=bg_color, relief='solid', bd=1,
                             state='normal',
                             highlightthickness=0,
                             cursor='arrow',
                             padx=2, pady=2)
        source_text.insert('1.0', segment.source)
        
        # Apply formatting tags to source text (with optional style colors)
        self.apply_formatting_to_text_widget(source_text, segment.source, segment)
        
        # Highlight filter matches in source (only if segment matches filters in highlight mode)
        if self.filter_active and hasattr(self, 'filter_source_var'):
            source_filter = self.filter_source_var.get().strip()
            if source_filter and self.should_highlight_segment(segment):
                self.highlight_text_in_widget(source_text, source_filter, 'yellow')
        
        source_text.config(state='disabled')
        source_text.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Make source clickable to select row and support dual selection
        row_index = len(self.grid_rows)  # Current index before appending
        source_text.bind('<Button-1>', lambda e, idx=row_index: self.on_source_text_click(e, idx))
        source_text.bind('<ButtonRelease-1>', lambda e, idx=row_index: self.on_source_selection_made(e, idx))
        source_text.bind('<Button-3>', lambda e, idx=row_index: self.on_source_right_click(e, idx))
        source_text.bind('<MouseWheel>', self.on_grid_mousewheel)
        
        # Keyboard selection bindings (Ctrl+Shift+Arrow keys - memoQ style)
        source_text.bind('<Control-Shift-Left>', 
                        lambda e, w=source_text: self.extend_selection_keyboard(w, 'left', 'char', 'source'))
        source_text.bind('<Control-Shift-Right>', 
                        lambda e, w=source_text: self.extend_selection_keyboard(w, 'right', 'char', 'source'))
        source_text.bind('<Control-Shift-Control-Left>', 
                        lambda e, w=source_text: self.extend_selection_keyboard(w, 'left', 'word', 'source'))
        source_text.bind('<Control-Shift-Control-Right>', 
                        lambda e, w=source_text: self.extend_selection_keyboard(w, 'right', 'word', 'source'))
        source_text.bind('<Tab>', lambda e: self.switch_dual_selection_focus())
        source_text.bind('<Escape>', lambda e: (self.clear_dual_selection(), None)[1] or 'break')
        
        widgets['source'] = source_text
        widgets['source_frame'] = source_frame
        
        # Splitter placeholder (matches header splitter width)
        splitter_space = tk.Frame(content_container, bg=bg_color, width=4)
        splitter_space.pack(side='left', fill='y')
        
        # Target column (Text widget for multi-line, will be editable) - expands
        target_frame = tk.Frame(content_container, bg=bg_color)
        target_frame.pack(side='left', fill='both', expand=True)
        
        target_text = tk.Text(target_frame, wrap='word', font=('Segoe UI', 9),
                             bg=bg_color, relief='solid', bd=1,
                             state='normal',
                             highlightthickness=0,
                             cursor='xterm',
                             padx=2, pady=2)
        if segment.target:
            target_text.insert('1.0', segment.target)
            # Apply formatting tags to target text (with optional style colors)
            self.apply_formatting_to_text_widget(target_text, segment.target, segment)
        
        # Highlight filter matches in target (only if segment matches filters in highlight mode)
        if self.filter_active and hasattr(self, 'filter_target_var'):
            target_filter = self.filter_target_var.get().strip()
            if target_filter and self.should_highlight_segment(segment):
                self.highlight_text_in_widget(target_text, target_filter, 'lightgreen')
        
        target_text.config(state='disabled')  # Initially disabled, enabled in edit mode
        target_text.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Make target clickable - support dual selection and edit mode
        target_text.bind('<Button-1>', lambda e, idx=row_index: self.on_target_text_click(e, idx))
        target_text.bind('<ButtonRelease-1>', lambda e, idx=row_index: self.on_target_selection_made(e, idx))
        target_text.bind('<Double-Button-1>', lambda e, idx=row_index: self.on_target_double_click(e, idx))
        target_text.bind('<Button-3>', lambda e, idx=row_index: self.on_target_right_click(e, idx))
        target_text.bind('<MouseWheel>', self.on_grid_mousewheel)
        
        # Keyboard selection bindings (Ctrl+Shift+Arrow keys - memoQ style)
        target_text.bind('<Control-Shift-Left>', 
                        lambda e, w=target_text: self.extend_selection_keyboard(w, 'left', 'char', 'target'))
        target_text.bind('<Control-Shift-Right>', 
                        lambda e, w=target_text: self.extend_selection_keyboard(w, 'right', 'char', 'target'))
        target_text.bind('<Control-Shift-Control-Left>', 
                        lambda e, w=target_text: self.extend_selection_keyboard(w, 'left', 'word', 'target'))
        target_text.bind('<Control-Shift-Control-Right>', 
                        lambda e, w=target_text: self.extend_selection_keyboard(w, 'right', 'word', 'target'))
        target_text.bind('<Tab>', lambda e: self.switch_dual_selection_focus())
        target_text.bind('<Escape>', lambda e: (self.clear_dual_selection(), None)[1] or 'break')
        
        widgets['target'] = target_text
        widgets['target_frame'] = target_frame
        
        # Also bind mousewheel to the frames and labels
        content_container.bind('<MouseWheel>', self.on_grid_mousewheel)
        row_frame.bind('<MouseWheel>', self.on_grid_mousewheel)
        id_label.bind('<MouseWheel>', self.on_grid_mousewheel)
        type_label.bind('<MouseWheel>', self.on_grid_mousewheel)
        status_label.bind('<MouseWheel>', self.on_grid_mousewheel)
        
        # Store row data
        row_data = {
            'segment': segment,
            'widgets': widgets,
            'row_frame': row_frame
        }
        self.grid_rows.append(row_data)
        
        # Update scroll region
        self.grid_canvas.update_idletasks()
        self.update_grid_scroll_region()
    
    # Grid View inline editing methods
    
    def create_context_menu(self):
        """Create context menu for Grid View"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="📋 Copy Source → Target (Ctrl+D)", 
                                     command=self.copy_source_to_target)
        self.context_menu.add_command(label="📄 View Source Text", 
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
        # Clear dual selection when entering edit mode
        self.clear_dual_selection()
        
        if self.layout_mode == LayoutMode.GRID:
            # Custom grid edit mode
            if self.current_row_index < 0 or self.current_row_index >= len(self.grid_rows):
                return
            
            row_data = self.grid_rows[self.current_row_index]
            target_widget = row_data['widgets']['target']
            
            # Enable the target Text widget
            target_widget.config(state='normal', bg='#ffffcc', relief='solid', bd=2)
            target_widget.focus_set()
            
            # Bind save/cancel keys
            target_widget.bind('<Control-Return>', lambda e: self.save_grid_edit(go_next=True))
            target_widget.bind('<Escape>', lambda e: self.cancel_grid_edit())
            
            # Bind tag shortcuts
            target_widget.bind('<Control-b>', lambda e: self.insert_tag_grid('b'))
            target_widget.bind('<Control-i>', lambda e: self.insert_tag_grid('i'))
            target_widget.bind('<Control-u>', lambda e: self.insert_tag_grid('u'))
            
            # Real-time tag validation
            target_widget.bind('<KeyRelease>', self.validate_tags_grid)
            
            # Store current edit widget
            self.current_edit_widget = target_widget
            
            self.log("Edit mode: Ctrl+Enter to save & next, Escape to cancel")
            
        else:
            # Treeview edit mode (Split/Compact)
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
    
    def save_grid_edit(self, go_next=False):
        """Save grid edit for custom grid (Text widget)"""
        if not self.current_edit_widget or self.current_row_index < 0:
            return
        
        # Get edited text
        new_text = self.current_edit_widget.get('1.0', 'end-1c')
        
        # Validate tags
        if self.tag_manager and new_text:
            is_valid, error = self.tag_manager.validate_tags(new_text)
            if not is_valid:
                messagebox.showerror("Tag Error", error)
                self.current_edit_widget.focus()
                return
        
        # Save to segment
        row_data = self.grid_rows[self.current_row_index]
        segment = row_data['segment']
        segment.target = new_text
        if new_text and segment.status == 'untranslated':
            segment.status = 'translated'
        segment.modified = True
        segment.modified_at = datetime.now().isoformat()
        
        # Update the display
        self.update_grid_row(self.current_row_index)
        
        # Disable editing - keep border
        target_widget = row_data['widgets']['target']
        target_widget.config(state='disabled', bg=self.get_status_color(segment.status), relief='solid', bd=1)
        
        self.current_edit_widget = None
        self.modified = True
        self.update_progress()
        self.log(f"Segment #{segment.id} saved")
        
        # Move to next if requested
        if go_next:
            # Navigate to next segment
            if self.current_row_index < len(self.grid_rows) - 1:
                self.select_grid_row(self.current_row_index + 1)
                # Automatically enter edit mode on the next segment
                self.root.after(50, self.enter_edit_mode)  # Small delay to ensure row is selected
            else:
                self.log("✓ Reached last segment")
                self.grid_canvas.focus_set()
        else:
            # Return focus to canvas
            self.grid_canvas.focus_set()
    
    def cancel_grid_edit(self):
        """Cancel grid editing without saving"""
        if self.current_row_index >= 0 and self.current_row_index < len(self.grid_rows):
            row_data = self.grid_rows[self.current_row_index]
            target_widget = row_data['widgets']['target']
            segment = row_data['segment']
            
            # Restore original text
            target_widget.delete('1.0', 'end')
            if segment.target:
                target_widget.insert('1.0', segment.target)
            
            # Disable editing - keep border
            target_widget.config(state='disabled', bg=self.get_status_color(segment.status), relief='solid', bd=1)
        
        self.current_edit_widget = None
        self.tag_validation_label.config(text="")
        self.grid_canvas.focus_set()
        self.log("Edit cancelled")
    
    def get_status_color(self, status):
        """Get background color for status"""
        status_colors = {
            'untranslated': '#ffe6e6',
            'draft': '#fff9e6',
            'translated': '#e6ffe6',
            'approved': '#e6f3ff'
        }
        return status_colors.get(status, 'white')
    
    def update_grid_row(self, row_index):
        """Update a grid row after editing"""
        if row_index < 0 or row_index >= len(self.grid_rows):
            return
        
        row_data = self.grid_rows[row_index]
        segment = row_data['segment']
        widgets = row_data['widgets']
        row_frame = row_data['row_frame']
        
        # Update background color
        bg_color = self.get_status_color(segment.status)
        row_frame.config(bg=bg_color)
        for widget_name, widget in widgets.items():
            widget.config(bg=bg_color)
            # Keep borders on source and target
            if widget_name in ['source', 'target']:
                widget.config(relief='solid', bd=1)
        
        # Update status text
        widgets['status'].config(text=segment.status)
        
        # Update target text
        target_widget = widgets['target']
        target_widget.config(state='normal')
        target_widget.delete('1.0', 'end')
        if segment.target:
            target_widget.insert('1.0', segment.target)
        target_widget.config(state='disabled')
        
        # Recalculate and update row height
        new_height = self.calculate_row_height(segment)
        row_frame.config(height=new_height)
        
        # Update scroll region
        self.grid_canvas.update_idletasks()
        self.update_grid_scroll_region()
    
    def validate_tags_grid(self, event=None):
        """Validate tags and resize row dynamically during editing"""
        if not self.current_edit_widget or not self.tag_manager:
            return
        
        text = self.current_edit_widget.get('1.0', 'end-1c')
        
        # Validate tags
        if not text:
            self.tag_validation_label.config(text="", fg='#666')
        else:
            is_valid, error = self.tag_manager.validate_tags(text)
            if is_valid:
                self.tag_validation_label.config(text="✓ Tags valid", fg='green')
            else:
                self.tag_validation_label.config(text=f"✗ {error}", fg='red')
        
        # Dynamic row resizing while typing
        if self.current_row_index >= 0 and self.current_row_index < len(self.grid_rows):
            self.resize_row_during_edit()
    
    def resize_row_during_edit(self):
        """Dynamically resize the current row based on content while editing"""
        if self.current_row_index < 0 or self.current_row_index >= len(self.grid_rows):
            return
        
        import textwrap
        
        row_data = self.grid_rows[self.current_row_index]
        segment = row_data['segment']
        row_frame = row_data['row_frame']
        target_widget = row_data['widgets']['target']
        source_widget = row_data['widgets']['source']
        
        # Get current text from target widget (being edited)
        current_target_text = target_widget.get('1.0', 'end-1c')
        
        # Use dynamic column widths
        source_width_chars = max(30, self.source_width // 8)
        target_width_chars = max(30, self.target_width // 8)
        
        # Calculate wrapped lines for source (unchanged)
        source_lines = 0
        if segment.source:
            source_paragraphs = segment.source.split('\n')
            for para in source_paragraphs:
                if para:
                    wrapped = textwrap.fill(para, width=source_width_chars)
                    source_lines += wrapped.count('\n') + 1
                else:
                    source_lines += 1
        
        # Calculate wrapped lines for current target text
        target_lines = 0
        if current_target_text:
            target_paragraphs = current_target_text.split('\n')
            for para in target_paragraphs:
                if para:
                    wrapped = textwrap.fill(para, width=target_width_chars)
                    target_lines += wrapped.count('\n') + 1
                else:
                    target_lines += 1
        else:
            target_lines = 1
        
        # Use the maximum of source and target
        max_lines = max(source_lines, target_lines)
        
        # Calculate new height
        new_height = max(35, min(250, max_lines * 18 + 15))
        
        # Only update if height changed significantly (avoid constant tiny updates)
        current_height = row_frame.winfo_height()
        if abs(new_height - current_height) > 5:
            row_frame.config(height=new_height)
            
            # Update scroll region
            self.grid_canvas.update_idletasks()
            self.update_grid_scroll_region()
    
    def insert_tag_grid(self, tag_type):
        """Insert tag at cursor position in grid editor"""
        if self.current_edit_widget:
            opening = f"<{tag_type}>"
            closing = f"</{tag_type}>"
            self.current_edit_widget.insert(tk.INSERT, opening + closing)
            # Move cursor between tags
            current_pos = self.current_edit_widget.index(tk.INSERT)
            line, col = current_pos.split('.')
            new_pos = f"{line}.{int(col) - len(closing)}"
            self.current_edit_widget.mark_set(tk.INSERT, new_pos)
            self.current_edit_widget.focus()
            return 'break'  # Prevent default behavior
    
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
    
    # Dual text selection methods (Grid View)
    
    def on_source_text_click(self, event, row_index):
        """Handle click in source text - potential start of dual selection"""
        # First, handle row selection
        self.select_grid_row(row_index)
        
        # Clear any existing dual selection from other rows
        if self.dual_selection_row is not None and self.dual_selection_row != row_index:
            self.clear_dual_selection()
        
        self.dual_selection_row = row_index
        row_data = self.grid_rows[row_index]
        self.dual_selection_source = row_data['widgets']['source']
    
    def on_source_selection_made(self, event, row_index):
        """Handle selection made in source text"""
        if row_index != self.dual_selection_row:
            return
        
        source_widget = self.grid_rows[row_index]['widgets']['source']
        
        # Check if there's a selection
        try:
            selection_start = source_widget.index(tk.SEL_FIRST)
            selection_end = source_widget.index(tk.SEL_LAST)
            
            # Store the selection and highlight it
            if selection_start != selection_end:
                # Remove existing source selection tag
                source_widget.tag_remove('dual_sel_source', '1.0', tk.END)
                
                # Add colored tag for source selection
                source_widget.tag_add('dual_sel_source', selection_start, selection_end)
                source_widget.tag_config('dual_sel_source',
                                        background='#B3E5FC',  # Light blue
                                        foreground='#01579B')  # Dark blue
                
                # Raise the tag above other tags
                source_widget.tag_raise('dual_sel_source')
                
                selected_text = source_widget.get(selection_start, selection_end)
                self.log(f"Source selection: '{selected_text}' ({len(selected_text)} chars)")
        except tk.TclError:
            # No selection made
            pass
    
    def on_target_text_click(self, event, row_index):
        """Handle click in target text - potential start of dual selection"""
        # First, handle row selection
        self.select_grid_row(row_index)
        
        # Check if this is the same row
        if self.dual_selection_row is not None and self.dual_selection_row != row_index:
            self.clear_dual_selection()
        
        self.dual_selection_row = row_index
        row_data = self.grid_rows[row_index]
        self.dual_selection_target = row_data['widgets']['target']
        
        # Don't enter edit mode on single click - only on double-click
        # This allows for selection without editing
    
    def on_target_selection_made(self, event, row_index):
        """Handle selection made in target text"""
        if row_index != self.dual_selection_row:
            return
        
        target_widget = self.grid_rows[row_index]['widgets']['target']
        
        # Check if there's a selection
        try:
            selection_start = target_widget.index(tk.SEL_FIRST)
            selection_end = target_widget.index(tk.SEL_LAST)
            
            # Store the selection and highlight it
            if selection_start != selection_end:
                # Remove existing target selection tag
                target_widget.tag_remove('dual_sel_target', '1.0', tk.END)
                
                # Add colored tag for target selection
                target_widget.tag_add('dual_sel_target', selection_start, selection_end)
                target_widget.tag_config('dual_sel_target',
                                        background='#C8E6C9',  # Light green
                                        foreground='#1B5E20')  # Dark green
                
                # Raise the tag above other tags
                target_widget.tag_raise('dual_sel_target')
                
                selected_text = target_widget.get(selection_start, selection_end)
                self.log(f"Target selection: '{selected_text}' ({len(selected_text)} chars)")
        except tk.TclError:
            # No selection made
            pass
    
    def clear_dual_selection(self):
        """Clear dual text selection highlights"""
        if self.dual_selection_row is not None and self.dual_selection_row < len(self.grid_rows):
            row_data = self.grid_rows[self.dual_selection_row]
            
            # Clear source selection tag
            if 'source' in row_data['widgets']:
                source_widget = row_data['widgets']['source']
                source_widget.tag_remove('dual_sel_source', '1.0', tk.END)
            
            # Clear target selection tag
            if 'target' in row_data['widgets']:
                target_widget = row_data['widgets']['target']
                target_widget.tag_remove('dual_sel_target', '1.0', tk.END)
        
        self.dual_selection_row = None
        self.dual_selection_source = None
        self.dual_selection_target = None
        self.dual_selection_focused_widget = None
        # Reset cursor memory when clearing selection
        self.dual_selection_source_cursor = None
        self.dual_selection_target_cursor = None
    
    def switch_dual_selection_focus(self):
        """Switch focus between source and target for keyboard selection (Tab key)"""
        # Don't interfere with edit mode - Tab should save & next in edit mode
        if self.current_edit_widget:
            return  # Allow default Tab behavior (save & next)
        
        if self.current_row_index < 0 or self.current_row_index >= len(self.grid_rows):
            return 'break'
        
        row_data = self.grid_rows[self.current_row_index]
        
        if self.dual_selection_focused_widget == 'source':
            # Switch to target
            self.focus_target_for_selection(self.current_row_index)
        elif self.dual_selection_focused_widget == 'target':
            # Switch to source
            self.focus_source_for_selection(self.current_row_index)
        else:
            # Start with source
            self.focus_source_for_selection(self.current_row_index)
        
        return 'break'  # Prevent default Tab behavior
    
    def focus_source_for_selection(self, row_index):
        """Focus source widget for keyboard-based dual selection"""
        if row_index < 0 or row_index >= len(self.grid_rows):
            return
        
        row_data = self.grid_rows[row_index]
        source_widget = row_data['widgets']['source']
        
        # Enable source widget temporarily for keyboard input (usually disabled/readonly)
        source_widget.config(state='normal')
        source_widget.focus_set()
        
        # Position cursor - use remembered position or start at 1.0
        if self.dual_selection_source_cursor is not None:
            # Return to where we left off
            cursor_pos = self.dual_selection_source_cursor
        else:
            # First time - start at beginning
            cursor_pos = '1.0'
        
        source_widget.mark_set(tk.INSERT, cursor_pos)
        source_widget.see(cursor_pos)
        
        # Visual indicator - subtle border
        source_widget.config(relief='solid', bd=2, highlightthickness=1,
                           highlightbackground='#2196F3', highlightcolor='#2196F3')
        
        # Save target's cursor position before switching away
        if 'target' in row_data['widgets']:
            target_widget = row_data['widgets']['target']
            try:
                self.dual_selection_target_cursor = target_widget.index(tk.INSERT)
            except:
                pass
            target_widget.config(state='disabled', relief='solid', bd=1, highlightthickness=0)
        
        self.dual_selection_focused_widget = 'source'
        self.dual_selection_row = row_index
        self.log("Source focused - use Ctrl+Shift+Arrows to select, Tab to switch")
    
    def focus_target_for_selection(self, row_index):
        """Focus target widget for keyboard-based dual selection"""
        if row_index < 0 or row_index >= len(self.grid_rows):
            return
        
        row_data = self.grid_rows[row_index]
        target_widget = row_data['widgets']['target']
        
        # Enable target widget temporarily for keyboard input (may be disabled)
        target_widget.config(state='normal')
        target_widget.focus_set()
        
        # Position cursor - use remembered position or start at 1.0
        if self.dual_selection_target_cursor is not None:
            # Return to where we left off
            cursor_pos = self.dual_selection_target_cursor
        else:
            # First time - start at beginning
            cursor_pos = '1.0'
        
        target_widget.mark_set(tk.INSERT, cursor_pos)
        target_widget.see(cursor_pos)
        
        # Visual indicator - subtle border
        target_widget.config(relief='solid', bd=2, highlightthickness=1,
                           highlightbackground='#4CAF50', highlightcolor='#4CAF50')
        
        # Save source's cursor position before switching away
        if 'source' in row_data['widgets']:
            source_widget = row_data['widgets']['source']
            try:
                self.dual_selection_source_cursor = source_widget.index(tk.INSERT)
            except:
                pass
            source_widget.config(state='disabled', relief='solid', bd=1, highlightthickness=0)
        
        self.dual_selection_focused_widget = 'target'
        self.dual_selection_row = row_index
        self.log("Target focused - use Ctrl+Shift+Arrows to select, Tab to switch")
    
    def extend_selection_keyboard(self, widget, direction, unit, widget_type):
        """Extend selection using keyboard (Ctrl+Shift+Arrow keys)
        
        Args:
            widget: The Text widget (source or target)
            direction: 'left' or 'right'
            unit: 'char' or 'word'
            widget_type: 'source' or 'target'
        """
        try:
            # Get current insert position (cursor)
            current_pos = widget.index(tk.INSERT)
            
            # Check if we already have a selection
            try:
                sel_start = widget.index(tk.SEL_FIRST)
                sel_end = widget.index(tk.SEL_LAST)
                has_selection = True
                # Determine if cursor is at start or end to know direction of extension
                cursor_at_start = widget.compare(current_pos, "==", sel_start)
            except tk.TclError:
                # No existing selection, start from cursor
                sel_start = current_pos
                sel_end = current_pos
                has_selection = False
                cursor_at_start = False
            
            # Calculate new position based on direction and unit
            if direction == 'right':
                if unit == 'char':
                    new_pos = widget.index(f"{current_pos} + 1 char")
                else:  # word
                    new_pos = widget.index(f"{current_pos} wordend")
                    # If not at word boundary, move to next word end
                    if widget.compare(new_pos, "==", current_pos):
                        new_pos = widget.index(f"{new_pos} + 1 char wordend")
                
                # Extend selection
                if has_selection and cursor_at_start:
                    # Cursor at start, moving right shrinks selection
                    new_start = new_pos
                    new_end = sel_end
                else:
                    # Cursor at end or no selection, extend right
                    new_start = sel_start if has_selection else current_pos
                    new_end = new_pos
                
                cursor_pos = new_end
                
            else:  # left
                if unit == 'char':
                    new_pos = widget.index(f"{current_pos} - 1 char")
                else:  # word
                    new_pos = widget.index(f"{current_pos} wordstart")
                    # If not at word boundary, move to previous word start
                    if widget.compare(new_pos, "==", current_pos):
                        new_pos = widget.index(f"{new_pos} - 1 char wordstart")
                
                # Extend selection
                if has_selection and not cursor_at_start:
                    # Cursor at end, moving left shrinks selection
                    new_start = sel_start
                    new_end = new_pos
                else:
                    # Cursor at start or no selection, extend left
                    new_start = new_pos
                    new_end = sel_end if has_selection else current_pos
                
                cursor_pos = new_start
            
            # Don't go beyond text boundaries
            text_start = widget.index("1.0")
            text_end = widget.index("end-1c")
            
            # Clamp to boundaries
            if widget.compare(new_start, "<", text_start):
                new_start = text_start
            if widget.compare(new_end, ">", text_end):
                new_end = text_end
            
            # Ensure start is before end
            if widget.compare(new_start, ">", new_end):
                new_start, new_end = new_end, new_start
            
            # Apply the selection
            widget.tag_remove('sel', '1.0', tk.END)  # Clear default selection
            
            # Remove existing colored tag
            tag_name = f'dual_sel_{widget_type}'
            widget.tag_remove(tag_name, '1.0', tk.END)
            
            # Add new colored selection if there's a range
            if widget.compare(new_start, "!=", new_end):
                # Add Tkinter selection for cursor positioning
                widget.tag_add('sel', new_start, new_end)
                
                # Add colored tag
                widget.tag_add(tag_name, new_start, new_end)
                
                # Configure tag colors
                if widget_type == 'source':
                    widget.tag_config(tag_name,
                                    background='#B3E5FC',  # Light blue
                                    foreground='#01579B')  # Dark blue
                else:  # target
                    widget.tag_config(tag_name,
                                    background='#C8E6C9',  # Light green
                                    foreground='#1B5E20')  # Dark green
                
                widget.tag_raise(tag_name)
                
                # Update cursor position
                widget.mark_set(tk.INSERT, cursor_pos)
                widget.see(cursor_pos)  # Scroll to cursor
                
                # Show selection in status bar
                selected_text = widget.get(new_start, new_end)
                self.log(f"{widget_type.capitalize()} selection: '{selected_text}' ({len(selected_text)} chars)")
        
        except tk.TclError as e:
            # Handle edge cases silently
            pass
        
        return 'break'  # Prevent default behavior
    
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
            
            if self.layout_mode == LayoutMode.GRID:
                # Update custom grid
                if self.current_row_index >= 0:
                    self.update_grid_row(self.current_row_index)
            else:
                # Update treeview
                self.update_segment_in_grid(self.current_segment)
            
            self.modified = True
            self.update_progress()
            self.log(f"Segment #{self.current_segment.id} target cleared")
    
    def set_status_inline(self, status):
        """Set status of currently selected segment"""
        if self.current_segment:
            self.current_segment.status = status
            
            if self.layout_mode == LayoutMode.GRID:
                # Update custom grid
                if self.current_row_index >= 0:
                    self.update_grid_row(self.current_row_index)
            else:
                # Update treeview
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
        if self.layout_mode == LayoutMode.GRID:
            # Custom grid navigation
            if not self.grid_rows:
                return
            
            if self.current_row_index < 0:
                # No selection, select first
                self.select_grid_row(0)
                segment = self.grid_rows[0]['segment']
                seg_type = self.get_segment_type_label(segment)
                self.log(f"Segment #{segment.id} ({seg_type})")
                return
            
            if direction == 'next':
                if self.current_row_index < len(self.grid_rows) - 1:
                    self.select_grid_row(self.current_row_index + 1)
                    segment = self.grid_rows[self.current_row_index]['segment']
                    seg_type = self.get_segment_type_label(segment)
                    self.log(f"Segment #{segment.id} ({seg_type})")
                else:
                    self.log("Already at last segment")
            elif direction == 'prev':
                if self.current_row_index > 0:
                    self.select_grid_row(self.current_row_index - 1)
                    segment = self.grid_rows[self.current_row_index]['segment']
                    seg_type = self.get_segment_type_label(segment)
                    self.log(f"Segment #{segment.id} ({seg_type})")
                else:
                    self.log("Already at first segment")
        elif self.layout_mode == LayoutMode.DOCUMENT:
            # Document view navigation
            self.navigate_document_segment(direction)
            if self.current_segment:
                seg_type = self.get_segment_type_label(self.current_segment)
                self.log(f"Segment #{self.current_segment.id} ({seg_type})")
        else:
            # Treeview navigation
            selection = self.tree.selection()
            if not selection:
                # No selection, select first item
                children = self.tree.get_children()
                if children:
                    self.tree.selection_set(children[0])
                    self.tree.see(children[0])
                    self.tree.focus(children[0])
                    # Get segment info
                    if self.current_segment:
                        seg_type = self.get_segment_type_label(self.current_segment)
                        self.log(f"Segment #{self.current_segment.id} ({seg_type})")
                return
            
            item = selection[0]
            
            if direction == 'next':
                next_item = self.tree.next(item)
                if next_item:
                    self.tree.selection_set(next_item)
                    self.tree.see(next_item)
                    self.tree.focus(next_item)
                    if self.current_segment:
                        seg_type = self.get_segment_type_label(self.current_segment)
                        self.log(f"Segment #{self.current_segment.id} ({seg_type})")
                else:
                    self.log("Already at last segment")
            elif direction == 'prev':
                prev_item = self.tree.prev(item)
                if prev_item:
                    self.tree.selection_set(prev_item)
                    self.tree.see(prev_item)
                    self.tree.focus(prev_item)
                    if self.current_segment:
                        seg_type = self.get_segment_type_label(self.current_segment)
                        self.log(f"Segment #{self.current_segment.id} ({seg_type})")
                else:
                    self.log("Already at first segment")
    
    def get_segment_type_label(self, segment):
        """Get a user-friendly label for the segment type"""
        if segment.is_table_cell:
            return "Table"
        elif segment.style and "Heading" in segment.style:
            return segment.style  # e.g., "Heading 1", "Heading 2"
        elif segment.style and segment.style != "Normal":
            return segment.style  # e.g., "Title", "Subtitle"
        else:
            return "Para"  # Regular paragraph
    
    def show_source_popup(self, event):
        """Show source and target in a memoQ-style popup with clear divider"""
        if not self.current_segment:
            return
        
        # Calculate content-aware size
        source_lines = self.current_segment.source.count('\n') + 1
        target_lines = self.current_segment.target.count('\n') + 1 if self.current_segment.target else 1
        
        # Estimate height needed (30px per line + padding)
        source_height = max(60, min(200, source_lines * 30 + 40))
        target_height = max(60, min(200, target_lines * 30 + 40))
        total_height = source_height + target_height + 120  # Extra for labels and buttons
        
        # Width based on content length
        max_line_length = max(
            max(len(line) for line in self.current_segment.source.split('\n') or ['']) if self.current_segment.source else 0,
            max(len(line) for line in self.current_segment.target.split('\n') or ['']) if self.current_segment.target else 0
        )
        popup_width = max(500, min(800, max_line_length * 8 + 100))
        
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"Segment #{self.current_segment.id} - Source & Target")
        popup.geometry(f"{popup_width}x{total_height}")
        popup.transient(self.root)
        
        # Position near cursor
        popup.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        # Main content frame
        main_frame = tk.Frame(popup, padx=15, pady=10)
        main_frame.pack(fill='both', expand=True)
        
        # Source section
        source_label_frame = tk.Frame(main_frame)
        source_label_frame.pack(fill='x', pady=(0, 5))
        tk.Label(source_label_frame, text="📄 Source", 
                font=('Segoe UI', 10, 'bold'), fg='#0066cc').pack(side='left')
        tk.Label(source_label_frame, text="(Read-only, select to copy)", 
                font=('Segoe UI', 8), fg='#666').pack(side='left', padx=(10, 0))
        
        source_widget = scrolledtext.ScrolledText(main_frame, wrap='word', 
                                                  font=('Segoe UI', 10),
                                                  bg='#f0f8ff',
                                                  relief='solid',
                                                  borderwidth=1,
                                                  height=max(2, source_lines))
        source_widget.pack(fill='both', expand=True, pady=(0, 10))
        source_widget.insert('1.0', self.current_segment.source)
        source_widget.config(state='normal')  # Allow selection for copying
        
        # Clear divider line (memoQ-style)
        divider = tk.Frame(main_frame, height=2, bg='#0066cc', relief='solid')
        divider.pack(fill='x', pady=10)
        
        # Target section
        target_label_frame = tk.Frame(main_frame)
        target_label_frame.pack(fill='x', pady=(0, 5))
        tk.Label(target_label_frame, text="🎯 Target", 
                font=('Segoe UI', 10, 'bold'), fg='#009900').pack(side='left')
        tk.Label(target_label_frame, text="(Read-only)", 
                font=('Segoe UI', 8), fg='#666').pack(side='left', padx=(10, 0))
        
        target_widget = scrolledtext.ScrolledText(main_frame, wrap='word', 
                                                  font=('Segoe UI', 10),
                                                  bg='#f0fff0',
                                                  relief='solid',
                                                  borderwidth=1,
                                                  height=max(2, target_lines))
        target_widget.pack(fill='both', expand=True, pady=(0, 10))
        if self.current_segment.target:
            target_widget.insert('1.0', self.current_segment.target)
        else:
            target_widget.insert('1.0', '[No translation yet]')
            target_widget.config(fg='#999')
        target_widget.config(state='normal')  # Allow selection for copying
        
        # Button frame
        btn_frame = tk.Frame(popup, padx=15, pady=10, bg='#f0f0f0')
        btn_frame.pack(fill='x', side='bottom')
        
        tk.Button(btn_frame, text="📋 Copy Source to Clipboard", 
                 command=lambda: self.copy_to_clipboard(self.current_segment.source, popup),
                 bg='#2196F3', fg='white', padx=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="✨ Copy Source → Target", 
                 command=lambda: [self.copy_source_to_target(), popup.destroy()],
                 bg='#4CAF50', fg='white', padx=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="✖ Close", 
                 command=popup.destroy,
                 padx=10).pack(side='right', padx=5)
        
        # Auto-select source text for easy copying
        source_widget.tag_add('sel', '1.0', 'end')
        source_widget.focus()
        
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
                doc_position = para_id  # Use para_id as fallback
                
                if para_info:
                    # Get style information
                    style = para_info.style or "Normal"
                    
                    # Get document position for proper ordering
                    doc_position = para_info.document_position
                    
                    # Get table information
                    if para_info.is_table_cell:
                        is_table = True
                        table_info = (para_info.table_index, para_info.row_index, para_info.cell_index)
                
                segment = Segment(seg_id, text, para_id, is_table, table_info, style, doc_position)
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
    
    def load_segments_to_tree(self):
        """Load segments into Treeview (for List View)"""
        self.log(f"load_segments_to_tree() called. Has tree: {hasattr(self, 'tree')}")
        
        # Check if tree exists
        if not hasattr(self, 'tree'):
            self.log("⚠ Tree view not created yet, skipping load")
            return
        
        self.log(f"Tree exists, attempting to load segments...")
        
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Use filtered segments if filter is active, otherwise all segments
        segments_to_show = self.filtered_segments if self.filter_active else self.segments
        
        self.log(f"Segments info: total={len(self.segments)}, filter_active={self.filter_active}, filtered={len(self.filtered_segments)}, to_show={len(segments_to_show)}")
        
        # Debug: Check if we have segments
        if not segments_to_show:
            self.log(f"⚠ No segments to display in List View. filter_active={self.filter_active}, segments count={len(self.segments)}, filtered count={len(self.filtered_segments)}")
            return
        
        self.log(f"Loading {len(segments_to_show)} segments to tree...")
        
        # Add segments
        for seg in segments_to_show:
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
            
            # Prepare source and target text with potential highlighting
            source_text = self._truncate(seg.source, 75)
            target_text = self._truncate(seg.target, 75)
            
            # Note: Treeview doesn't support text highlighting like Text widget
            # In highlight mode, matches are shown but not visually highlighted in the tree
            # The highlighting will be visible in the editor panel below
            
            # Insert into tree
            item_id = self.tree.insert('', 'end',
                           values=(seg.id, type_label, style_display, seg.status.capitalize(),
                                  source_text, target_text),
                           tags=tuple(tags))
            if len(tags) == 0:  # Log first item only
                self.log(f"  Inserted segment {seg.id}: {source_text[:30]}... -> item_id={item_id}")
        
        # Select first segment if available
        children = self.tree.get_children()
        self.log(f"After loading, tree has {len(children)} children")
        if children:
            self.tree.selection_set(children[0])
            self.tree.focus(children[0])
            self.on_segment_select(None)
    
    
    
    def set_filter_mode(self, mode):
        """Set the filter mode and update button states"""
        if self.filter_mode == mode:
            return  # Already in this mode
        
        self.filter_mode = mode
        
        if mode == 'filter':
            # Filter mode active - show only matches
            self.filter_mode_btn.config(bg='#4CAF50', fg='white', 
                                       font=('Segoe UI', 9, 'bold'), relief='sunken')
            self.highlight_mode_btn.config(bg='#e0e0e0', fg='#666',
                                          font=('Segoe UI', 9), relief='raised')
            self.log("� Filter Mode: Only matching segments shown")
        else:
            # Highlight mode active - show all with highlights
            self.filter_mode_btn.config(bg='#e0e0e0', fg='#666',
                                       font=('Segoe UI', 9), relief='raised')
            self.highlight_mode_btn.config(bg='#FFA500', fg='white',
                                          font=('Segoe UI', 9, 'bold'), relief='sunken')
            self.log("� Highlight Mode: All segments shown with matches highlighted")
        
        # Reapply filters with new mode
        self.apply_filters()
    
    def apply_filters(self):
        """Apply filters to the segment list"""
        if not hasattr(self, 'segments') or not self.segments:
            return
        
        source_filter = self.filter_source_var.get().strip().lower()
        target_filter = self.filter_target_var.get().strip().lower()
        status_filter = self.filter_status_var.get()
        
        # Check if any filter is active
        self.filter_active = bool(source_filter or target_filter or (status_filter != "All"))
        
        if not self.filter_active:
            # No filters - show all segments
            self.filtered_segments = self.segments.copy()
            if hasattr(self, 'filter_results_label') and self.filter_results_label.winfo_exists():
                self.filter_results_label.config(text="")
        elif self.filter_mode == 'highlight':
            # Highlight mode: show ALL segments but highlight matches
            self.filtered_segments = self.segments.copy()
            
            # Count how many segments have matches (for info label)
            match_count = 0
            for seg in self.segments:
                has_match = True
                if source_filter and source_filter not in seg.source.lower():
                    has_match = False
                if target_filter and target_filter not in seg.target.lower():
                    has_match = False
                if status_filter != "All" and seg.status != status_filter:
                    has_match = False
                if has_match:
                    match_count += 1
            
            # Update results label
            total = len(self.segments)
            if hasattr(self, 'filter_results_label') and self.filter_results_label.winfo_exists():
                self.filter_results_label.config(
                    text=f"💡 Highlighting {match_count} of {total} segments",
                    fg='#4CAF50' if match_count > 0 else '#FF5722'
                )
        else:
            # Filter mode: show ONLY matching segments
            self.filtered_segments = []
            for seg in self.segments:
                # Source filter
                if source_filter and source_filter not in seg.source.lower():
                    continue
                
                # Target filter
                if target_filter and target_filter not in seg.target.lower():
                    continue
                
                # Status filter
                if status_filter != "All" and seg.status != status_filter:
                    continue
                
                # Segment passed all filters
                self.filtered_segments.append(seg)
            
            # Update results label
            total = len(self.segments)
            filtered = len(self.filtered_segments)
            if hasattr(self, 'filter_results_label') and self.filter_results_label.winfo_exists():
                self.filter_results_label.config(
                    text=f"🔍 Showing {filtered} of {total} segments",
                    fg='#4CAF50' if filtered > 0 else '#FF5722'
                )
        
        # Reload the grid with filtered segments
        self.reload_grid_with_filters()
    
    def clear_filters(self):
        """Clear all filters"""
        self.filter_source_var.set("")
        self.filter_target_var.set("")
        self.filter_status_var.set("All")
        self.filter_active = False
        if hasattr(self, 'filter_results_label') and self.filter_results_label.winfo_exists():
            self.filter_results_label.config(text="")
        self.log("✓ Filters cleared")
    
    def toggle_filter_mode(self):
        """Toggle between filter and highlight modes (Ctrl+M)"""
        new_mode = 'highlight' if self.filter_mode == 'filter' else 'filter'
        self.set_filter_mode(new_mode)
    
    def focus_filter_source(self):
        """Focus the source filter entry field (Ctrl+Shift+F)"""
        # Find the source filter entry in the current view
        # This is a bit tricky since we need to find the widget
        # We'll use a simple approach: find all Entry widgets and check their textvariable
        try:
            for widget in self.root.winfo_children():
                self._focus_filter_recursive(widget)
        except:
            pass
    
    def _focus_filter_recursive(self, widget):
        """Recursively search for source filter entry and focus it"""
        try:
            if isinstance(widget, tk.Entry):
                # Check if this entry uses the source filter variable
                if hasattr(widget, 'cget') and widget.cget('textvariable') == str(self.filter_source_var):
                    widget.focus_set()
                    return True
            # Recurse into children
            for child in widget.winfo_children():
                if self._focus_filter_recursive(child):
                    return True
        except:
            pass
        return False
    
    def highlight_text_in_widget(self, text_widget, search_text, color='yellow'):
        """Highlight all occurrences of search_text in a Text widget"""
        if not search_text:
            return
        
        # Configure tag for highlighting
        tag_name = f"highlight_{color}"
        text_widget.tag_configure(tag_name, background=color, foreground='black')
        
        # Get the content
        content = text_widget.get('1.0', 'end-1c')
        search_lower = search_text.lower()
        content_lower = content.lower()
        
        # Find all occurrences (case-insensitive)
        start_pos = 0
        while True:
            start_pos = content_lower.find(search_lower, start_pos)
            if start_pos == -1:
                break
            
            # Calculate Text widget position
            lines_before = content[:start_pos].count('\n')
            chars_in_line = start_pos - content.rfind('\n', 0, start_pos) - 1
            
            start_index = f"{lines_before + 1}.{chars_in_line}"
            end_index = f"{lines_before + 1}.{chars_in_line + len(search_text)}"
            
            # Apply tag
            text_widget.tag_add(tag_name, start_index, end_index)
            
            start_pos += len(search_text)
    
    def reload_grid_with_filters(self):
        """Reload the current view with filtered segments"""
        if self.layout_mode == LayoutMode.GRID:
            # Grid View: Clear and rebuild grid
            self.grid_rows = []
            for widget in self.grid_inner_frame.winfo_children():
                widget.destroy()
            
            # Use filtered segments if filter is active, otherwise all segments
            segments_to_show = self.filtered_segments if self.filter_active else self.segments
            
            # Add filtered segments to grid
            for seg in segments_to_show:
                self.add_grid_row(seg)
            
            # Select first row if available
            if self.grid_rows:
                self.select_grid_row(0)
        
        elif self.layout_mode == LayoutMode.SPLIT:
            # List View: Reload tree
            self.load_segments_to_tree()
        
        elif self.layout_mode == LayoutMode.DOCUMENT:
            # Document View: Reload document
            self.load_segments_to_document()
        # Log the filter result
        if self.filter_active:
            self.log(f"🔍 Filter applied: {len(segments_to_show)} segments match")
    
    def load_segments_to_grid(self):
        """Load segments into the grid"""
        if self.layout_mode == LayoutMode.GRID:
            # Clear existing custom grid rows
            self.grid_rows = []
            for widget in self.grid_inner_frame.winfo_children():
                widget.destroy()
            
            # Determine which segments to show (filtered or all)
            segments_to_show = self.filtered_segments if self.filter_active else self.segments
            
            # Add segments to custom grid
            for seg in segments_to_show:
                self.add_grid_row(seg)
            
            # Select first row if available
            if self.grid_rows:
                self.select_grid_row(0)
                
        else:
            # Use Treeview for Split/Compact modes
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
                
                # Insert with style column (6 columns)
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
    
    def _truncate_multiline(self, text: str, length: int) -> str:
        """Truncate text but preserve newlines for better multi-line display in grid"""
        if not text:
            return ""
        
        # If text is short enough, return as-is
        if len(text) <= length:
            return text
        
        # For longer text, show first 2 lines or up to length chars, whichever is less
        lines = text.split('\n')
        if len(lines) > 2:
            # Show first 2 lines + indicator
            result = '\n'.join(lines[:2])
            if len(result) > length:
                result = result[:length-3] + "..."
            else:
                result += "\n..."
            return result
        else:
            # Single line or 2 lines - just truncate if too long
            if len(text) > length:
                return text[:length-3] + "..."
            return text
    
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
                if self.layout_mode == LayoutMode.GRID:
                    # Grid: No style column (5 columns)
                    # Use multiline truncate for better display
                    self.tree.item(item,
                                 values=(segment.id, type_label, segment.status.capitalize(),
                                        self._truncate_multiline(segment.source, 150),
                                        self._truncate_multiline(segment.target, 150)),
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
            # In Grid mode with custom grid
            if self.current_row_index >= 0 and self.current_row_index < len(self.grid_rows):
                self.update_grid_row(self.current_row_index)
                
                # If currently editing, update the edit widget
                if self.current_edit_widget:
                    self.current_edit_widget.delete('1.0', 'end')
                    self.current_edit_widget.insert('1.0', self.current_segment.source)
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
                'segments': [s.to_dict() for s in self.segments],
                # Save filter preferences
                'filter_preferences': {
                    'mode': self.filter_mode,
                    'source_filter': self.filter_source_var.get() if hasattr(self, 'filter_source_var') else '',
                    'target_filter': self.filter_target_var.get() if hasattr(self, 'filter_target_var') else '',
                    'status_filter': self.filter_status_var.get() if hasattr(self, 'filter_status_var') else 'All',
                    'active': self.filter_active
                }
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
            if response is None:
                return
            elif response is True:
                self.save_project()
        
        file_path = filedialog.askopenfilename(
            title="Open Project",
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
            
            # Load filter preferences if they exist
            if 'filter_preferences' in data:
                prefs = data['filter_preferences']
                if hasattr(self, 'filter_source_var'):
                    self.filter_source_var.set(prefs.get('source_filter', ''))
                if hasattr(self, 'filter_target_var'):
                    self.filter_target_var.set(prefs.get('target_filter', ''))
                if hasattr(self, 'filter_status_var'):
                    self.filter_status_var.set(prefs.get('status_filter', 'All'))
                self.filter_mode = prefs.get('mode', 'filter')
                self.filter_active = prefs.get('active', False)
                
                # Update button states to match loaded mode
                if hasattr(self, 'filter_mode_btn') and hasattr(self, 'highlight_mode_btn'):
                    if self.filter_mode == 'filter':
                        self.filter_mode_btn.config(bg='#4CAF50', fg='white', 
                                                   font=('Segoe UI', 9, 'bold'), relief='sunken')
                        self.highlight_mode_btn.config(bg='#e0e0e0', fg='#666',
                                                      font=('Segoe UI', 9), relief='raised')
                    else:
                        self.filter_mode_btn.config(bg='#e0e0e0', fg='#666',
                                                   font=('Segoe UI', 9), relief='raised')
                        self.highlight_mode_btn.config(bg='#FFA500', fg='white',
                                                      font=('Segoe UI', 9, 'bold'), relief='sunken')
                
                # Apply the filters if they were active
                if self.filter_active:
                    self.apply_filters()
            
            # If original DOCX exists, load it for export
            if self.original_docx and os.path.exists(self.original_docx):
                self.docx_handler.import_docx(self.original_docx)
            
            # Load to grid
            self.load_segments_to_grid()
            
            self.modified = False
            self.log(f"✓ Project loaded: {os.path.basename(file_path)}")
            self.update_progress()
            
        except Exception as e:
            messagebox.showerror("Open Error", f"Failed to open project:\n{str(e)}")
    
    def close_project(self):
        """Close current project"""
        if not self.segments:
            messagebox.showinfo("No Project", "No project is currently open")
            return
        
        if self.modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "Save current project before closing?"
            )
            if response is None:
                return
            elif response is True:
                self.save_project()
        
        # Clear all data
        self.segments = []
        self.current_segment_index = None
        self.project_file = None
        self.original_docx = None
        self.modified = False
        
        # Clear the current view
        if self.current_layout_mode == LayoutMode.GRID:
            for item in self.tree.get_children():
                self.tree.delete(item)
        elif self.current_layout_mode == LayoutMode.SPLIT:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.source_text.config(state='normal')
            self.source_text.delete('1.0', 'end')
            self.source_text.config(state='disabled')
            self.target_text.delete('1.0', 'end')
        elif self.current_layout_mode == LayoutMode.DOCUMENT:
            # Clear document canvas
            for widget in self.doc_inner_frame.winfo_children():
                widget.destroy()
            self.doc_segment_widgets.clear()
            self.doc_current_segment = None
        
        self.log("✓ Project closed")
        self.update_progress()
    
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
