"""
TMX Editor Module - Professional Translation Memory Editor

A standalone, nimble TMX editor inspired by Heartsome TMX Editor 8.
Can run independently or integrate with Supervertaler.

Key Features (inspired by Heartsome):
- Dual-language grid editor (source/target columns)
- Fast filtering by language, content, status
- In-place editing with validation
- TMX file validation and repair
- Header metadata editing
- Large file support with pagination
- Import/Export multiple formats
- Multi-language support (view any language pair)

Architecture:
- Standalone mode: Run this file directly
- Integrated mode: Called from Supervertaler as a module

Designer: Michael Beijer
Based on concepts from: Heartsome TMX Editor 8 (Java/Eclipse RCP)
License: MIT - Open Source and Free
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import os
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class TmxSegment:
    """Translation unit variant (segment in one language)"""
    lang: str
    text: str
    creation_date: str = ""
    creation_id: str = ""
    change_date: str = ""
    change_id: str = ""
    

@dataclass
class TmxTranslationUnit:
    """Translation unit (TU) containing multiple language variants"""
    tu_id: int
    segments: Dict[str, TmxSegment] = field(default_factory=dict)
    creation_date: str = ""
    creation_id: str = ""
    change_date: str = ""
    change_id: str = ""
    srclang: str = ""
    
    def get_segment(self, lang: str) -> Optional[TmxSegment]:
        """Get segment for specific language"""
        return self.segments.get(lang)
    
    def set_segment(self, lang: str, text: str):
        """Set or update segment for specific language"""
        if lang in self.segments:
            self.segments[lang].text = text
            self.segments[lang].change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        else:
            self.segments[lang] = TmxSegment(lang=lang, text=text,
                                            creation_date=datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"))


@dataclass
class TmxHeader:
    """TMX file header information"""
    creation_tool: str = "Supervertaler TMX Editor"
    creation_tool_version: str = "1.0"
    segtype: str = "sentence"
    o_tmf: str = "unknown"
    adminlang: str = "en-US"
    srclang: str = "en-US"
    datatype: str = "unknown"
    creation_date: str = ""
    creation_id: str = ""
    change_date: str = ""
    change_id: str = ""
    
    def __post_init__(self):
        if not self.creation_date:
            self.creation_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


class TmxFile:
    """TMX file data model"""
    
    def __init__(self):
        self.header = TmxHeader()
        self.translation_units: List[TmxTranslationUnit] = []
        self.languages: List[str] = []
        self.file_path: Optional[str] = None
        self.is_modified: bool = False
        self.version: str = "1.4"
    
    def add_translation_unit(self, tu: TmxTranslationUnit):
        """Add a translation unit and update language list"""
        self.translation_units.append(tu)
        for lang in tu.segments.keys():
            if lang not in self.languages:
                self.languages.append(lang)
        self.is_modified = True
    
    def get_languages(self) -> List[str]:
        """Get list of all languages in the TMX file"""
        return sorted(self.languages)
    
    def get_tu_by_id(self, tu_id: int) -> Optional[TmxTranslationUnit]:
        """Get translation unit by ID"""
        for tu in self.translation_units:
            if tu.tu_id == tu_id:
                return tu
        return None
    
    def get_tu_count(self) -> int:
        """Get total number of translation units"""
        return len(self.translation_units)


class TmxParser:
    """TMX file parser and writer"""
    
    @staticmethod
    def parse_file(file_path: str) -> TmxFile:
        """Parse TMX file and return TmxFile object"""
        tmx = TmxFile()
        tmx.file_path = file_path
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Parse header
            header_elem = root.find('header')
            if header_elem is not None:
                tmx.header = TmxHeader(
                    creation_tool=header_elem.get('creationtool', 'unknown'),
                    creation_tool_version=header_elem.get('creationtoolversion', '1.0'),
                    segtype=header_elem.get('segtype', 'sentence'),
                    o_tmf=header_elem.get('o-tmf', 'unknown'),
                    adminlang=header_elem.get('adminlang', 'en-US'),
                    srclang=header_elem.get('srclang', 'en-US'),
                    datatype=header_elem.get('datatype', 'unknown'),
                    creation_date=header_elem.get('creationdate', ''),
                    creation_id=header_elem.get('creationid', ''),
                    change_date=header_elem.get('changedate', ''),
                    change_id=header_elem.get('changeid', '')
                )
            
            # Get TMX version
            tmx.version = root.get('version', '1.4')
            
            # Parse translation units
            body = root.find('body')
            if body is not None:
                for idx, tu_elem in enumerate(body.findall('tu'), start=1):
                    tu = TmxTranslationUnit(
                        tu_id=idx,
                        creation_date=tu_elem.get('creationdate', ''),
                        creation_id=tu_elem.get('creationid', ''),
                        change_date=tu_elem.get('changedate', ''),
                        change_id=tu_elem.get('changeid', ''),
                        srclang=tu_elem.get('srclang', '')
                    )
                    
                    # Parse segments (tuvs)
                    for tuv_elem in tu_elem.findall('tuv'):
                        lang = tuv_elem.get('{http://www.w3.org/XML/1998/namespace}lang', 
                                           tuv_elem.get('lang', 'unknown'))
                        
                        seg_elem = tuv_elem.find('seg')
                        if seg_elem is not None:
                            # Get text content including any inline tags
                            text = TmxParser._get_element_text(seg_elem)
                            
                            segment = TmxSegment(
                                lang=lang,
                                text=text,
                                creation_date=tuv_elem.get('creationdate', ''),
                                creation_id=tuv_elem.get('creationid', ''),
                                change_date=tuv_elem.get('changedate', ''),
                                change_id=tuv_elem.get('changeid', '')
                            )
                            tu.segments[lang] = segment
                            
                            if lang not in tmx.languages:
                                tmx.languages.append(lang)
                    
                    tmx.translation_units.append(tu)
            
            tmx.is_modified = False
            return tmx
            
        except Exception as e:
            raise Exception(f"Failed to parse TMX file: {str(e)}")
    
    @staticmethod
    def _get_element_text(element) -> str:
        """Get all text content from element including tail text of children"""
        text_parts = []
        if element.text:
            text_parts.append(element.text)
        for child in element:
            # Add child tag representation
            text_parts.append(ET.tostring(child, encoding='unicode', method='html'))
        if element.tail:
            text_parts.append(element.tail)
        return ''.join(text_parts).strip()
    
    @staticmethod
    def save_file(tmx: TmxFile, file_path: Optional[str] = None) -> bool:
        """Save TMX file"""
        if file_path is None:
            file_path = tmx.file_path
        
        if not file_path:
            raise ValueError("No file path specified")
        
        try:
            # Create root element
            root = ET.Element('tmx', version=tmx.version)
            
            # Create header
            header = ET.SubElement(root, 'header',
                                  creationtool=tmx.header.creation_tool,
                                  creationtoolversion=tmx.header.creation_tool_version,
                                  segtype=tmx.header.segtype,
                                  **{'o-tmf': tmx.header.o_tmf},
                                  adminlang=tmx.header.adminlang,
                                  srclang=tmx.header.srclang,
                                  datatype=tmx.header.datatype)
            
            if tmx.header.creation_date:
                header.set('creationdate', tmx.header.creation_date)
            if tmx.header.creation_id:
                header.set('creationid', tmx.header.creation_id)
            if tmx.header.change_date:
                header.set('changedate', tmx.header.change_date)
            if tmx.header.change_id:
                header.set('changeid', tmx.header.change_id)
            
            # Create body
            body = ET.SubElement(root, 'body')
            
            # Add translation units
            for tu_data in tmx.translation_units:
                tu = ET.SubElement(body, 'tu')
                
                if tu_data.creation_date:
                    tu.set('creationdate', tu_data.creation_date)
                if tu_data.creation_id:
                    tu.set('creationid', tu_data.creation_id)
                if tu_data.change_date:
                    tu.set('changedate', tu_data.change_date)
                if tu_data.change_id:
                    tu.set('changeid', tu_data.change_id)
                if tu_data.srclang:
                    tu.set('srclang', tu_data.srclang)
                
                # Add segments (sorted by language for consistency)
                for lang in sorted(tu_data.segments.keys()):
                    segment = tu_data.segments[lang]
                    tuv = ET.SubElement(tu, 'tuv')
                    tuv.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
                    
                    if segment.creation_date:
                        tuv.set('creationdate', segment.creation_date)
                    if segment.creation_id:
                        tuv.set('creationid', segment.creation_id)
                    if segment.change_date:
                        tuv.set('changedate', segment.change_date)
                    if segment.change_id:
                        tuv.set('changeid', segment.change_id)
                    
                    seg = ET.SubElement(tuv, 'seg')
                    seg.text = segment.text
            
            # Write to file with pretty formatting
            tree = ET.ElementTree(root)
            ET.register_namespace('xml', 'http://www.w3.org/XML/1998/namespace')
            
            # Pretty print
            TmxParser._indent(root)
            
            with open(file_path, 'wb') as f:
                f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write(b'<!DOCTYPE tmx SYSTEM "tmx14.dtd">\n')
                tree.write(f, encoding='utf-8', xml_declaration=False)
            
            tmx.file_path = file_path
            tmx.is_modified = False
            return True
            
        except Exception as e:
            raise Exception(f"Failed to save TMX file: {str(e)}")
    
    @staticmethod
    def _indent(elem, level=0):
        """Add pretty-printing indentation to XML"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                TmxParser._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


class TmxEditorUI:
    """TMX Editor user interface"""
    
    def __init__(self, parent=None, standalone=True):
        """
        Initialize TMX Editor UI
        
        Args:
            parent: Parent widget (None for standalone window)
            standalone: If True, creates own window. If False, embeds in parent
        """
        self.tmx_file: Optional[TmxFile] = None
        self.current_page = 0
        self.items_per_page = 50
        self.filtered_tus: List[TmxTranslationUnit] = []
        self.src_lang = ""
        self.tgt_lang = ""
        self.filter_source = ""
        self.filter_target = ""
        self.standalone = standalone
        
        if standalone:
            # Create standalone window
            self.root = tk.Tk()
            self.root.title("TMX Editor - Supervertaler")
            self.root.geometry("1200x700")
            self.container = self.root
        else:
            # Embed in parent widget
            self.root = parent
            self.container = tk.Frame(parent)
            self.container.pack(fill='both', expand=True)
        
        self.create_ui()
        
        if standalone:
            # Bind close event
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        """Create the user interface"""
        # Menu bar (only for standalone)
        if self.standalone:
            self.create_menu_bar()
        
        # Toolbar
        self.create_toolbar()
        
        # Main content area
        content_frame = tk.Frame(self.container)
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Language selector panel
        self.create_language_panel(content_frame)
        
        # Filter panel
        self.create_filter_panel(content_frame)
        
        # Integrated edit panel (above the grid)
        self.create_edit_panel(content_frame)
        
        # Grid editor
        self.create_grid_editor(content_frame)
        
        # Pagination controls
        self.create_pagination_controls(content_frame)
        
        # Status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create menu bar for standalone mode"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New TMX", command=self.new_tmx)
        file_menu.add_command(label="Open TMX...", command=self.open_tmx)
        file_menu.add_command(label="Save", command=self.save_tmx, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_tmx_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Add Translation Unit", command=self.add_translation_unit)
        edit_menu.add_command(label="Delete Selected", command=self.delete_selected_tu)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find/Replace...", command=self.show_find_replace)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="TMX Header...", command=self.edit_header)
        view_menu.add_command(label="Statistics", command=self.show_statistics)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Validate TMX", command=self.validate_tmx)
        tools_menu.add_command(label="Export to...", command=self.export_tmx)
        
        # Keyboard shortcuts
        self.root.bind('<Control-s>', lambda e: self.save_tmx())
        self.root.bind('<Control-o>', lambda e: self.open_tmx())
        self.root.bind('<Control-n>', lambda e: self.new_tmx())
    
    def create_toolbar(self):
        """Create toolbar with common actions"""
        toolbar = tk.Frame(self.container, bg='#f0f0f0', relief='raised', bd=1)
        toolbar.pack(side='top', fill='x', padx=2, pady=2)
        
        # File operations
        tk.Button(toolbar, text="📁 New", command=self.new_tmx,
                 relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        tk.Button(toolbar, text="📂 Open", command=self.open_tmx,
                 relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        tk.Button(toolbar, text="💾 Save", command=self.save_tmx,
                 relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        
        tk.Frame(toolbar, width=2, bg='#ccc').pack(side='left', fill='y', padx=5, pady=2)
        
        # Edit operations
        tk.Button(toolbar, text="➕ Add TU", command=self.add_translation_unit,
                 relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        tk.Button(toolbar, text="❌ Delete", command=self.delete_selected_tu,
                 relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        
        tk.Frame(toolbar, width=2, bg='#ccc').pack(side='left', fill='y', padx=5, pady=2)
        
        # View operations
        tk.Button(toolbar, text="ℹ️ Header", command=self.edit_header,
                 relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        tk.Button(toolbar, text="📊 Stats", command=self.show_statistics,
                 relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        tk.Button(toolbar, text="✓ Validate", command=self.validate_tmx,
                 relief='flat', padx=10, pady=5).pack(side='left', padx=2)
    
    def create_language_panel(self, parent):
        """Create language selection panel"""
        lang_frame = tk.Frame(parent, bg='#e8f4f8', relief='ridge', bd=1)
        lang_frame.pack(side='top', fill='x', pady=(0, 5))
        
        tk.Label(lang_frame, text="📖 Language Pair:", bg='#e8f4f8',
                font=('Segoe UI', 9, 'bold')).pack(side='left', padx=10, pady=5)
        
        tk.Label(lang_frame, text="Source:", bg='#e8f4f8').pack(side='left', padx=(10, 2))
        self.src_lang_combo = ttk.Combobox(lang_frame, width=15, state='readonly')
        self.src_lang_combo.pack(side='left', padx=(0, 10))
        self.src_lang_combo.bind('<<ComboboxSelected>>', self.on_language_changed)
        
        tk.Label(lang_frame, text="→", bg='#e8f4f8', font=('Segoe UI', 12)).pack(side='left', padx=5)
        
        tk.Label(lang_frame, text="Target:", bg='#e8f4f8').pack(side='left', padx=(0, 2))
        self.tgt_lang_combo = ttk.Combobox(lang_frame, width=15, state='readonly')
        self.tgt_lang_combo.pack(side='left', padx=(0, 10))
        self.tgt_lang_combo.bind('<<ComboboxSelected>>', self.on_language_changed)
        
        # Show all languages button
        tk.Button(lang_frame, text="🌐 All Languages", command=self.show_all_languages,
                 relief='flat', bg='#4CAF50', fg='white', padx=10, pady=3).pack(side='right', padx=10)
    
    def create_filter_panel(self, parent):
        """Create filter panel"""
        filter_frame = tk.Frame(parent, bg='#fff3cd', relief='ridge', bd=1)
        filter_frame.pack(side='top', fill='x', pady=(0, 5))
        
        tk.Label(filter_frame, text="🔍 Filter:", bg='#fff3cd',
                font=('Segoe UI', 9, 'bold')).pack(side='left', padx=10, pady=5)
        
        tk.Label(filter_frame, text="Source:", bg='#fff3cd').pack(side='left', padx=(10, 2))
        self.filter_source_entry = tk.Entry(filter_frame, width=25)
        self.filter_source_entry.pack(side='left', padx=(0, 10))
        self.filter_source_entry.bind('<Return>', lambda e: self.apply_filters())
        
        tk.Label(filter_frame, text="Target:", bg='#fff3cd').pack(side='left', padx=(0, 2))
        self.filter_target_entry = tk.Entry(filter_frame, width=25)
        self.filter_target_entry.pack(side='left', padx=(0, 10))
        self.filter_target_entry.bind('<Return>', lambda e: self.apply_filters())
        
        tk.Button(filter_frame, text="Apply Filter", command=self.apply_filters,
                 relief='flat', bg='#ff9800', fg='white', padx=10, pady=3).pack(side='left', padx=5)
        tk.Button(filter_frame, text="Clear", command=self.clear_filters,
                 relief='flat', bg='#9e9e9e', fg='white', padx=10, pady=3).pack(side='left', padx=2)
    
    def create_edit_panel(self, parent):
        """Create integrated edit panel above the grid"""
        edit_frame = tk.Frame(parent, bg='#e8f4f8', relief='ridge', bd=2)
        edit_frame.pack(side='top', fill='x', pady=(0, 5))
        
        # Header
        header = tk.Frame(edit_frame, bg='#e8f4f8')
        header.pack(fill='x', padx=5, pady=5)
        
        tk.Label(header, text="✏️ Edit Translation Unit", bg='#e8f4f8',
                font=('Segoe UI', 10, 'bold')).pack(side='left')
        
        self.edit_id_label = tk.Label(header, text="(Double-click a segment to edit)", 
                                      bg='#e8f4f8', fg='#666', font=('Segoe UI', 9))
        self.edit_id_label.pack(side='left', padx=10)
        
        # Edit area
        edit_content = tk.Frame(edit_frame, bg='#e8f4f8')
        edit_content.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Source column
        src_frame = tk.Frame(edit_content, bg='#e8f4f8')
        src_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        tk.Label(src_frame, text="Source:", bg='#e8f4f8', 
                font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.edit_src_lang_label = tk.Label(src_frame, text="", bg='#e8f4f8', 
                                            fg='#666', font=('Segoe UI', 8))
        self.edit_src_lang_label.pack(anchor='w')
        
        self.edit_source_text = tk.Text(src_frame, height=4, wrap='word', 
                                       font=('Segoe UI', 9), state='disabled')
        self.edit_source_text.pack(fill='both', expand=True)
        
        # Target column
        tgt_frame = tk.Frame(edit_content, bg='#e8f4f8')
        tgt_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        tk.Label(tgt_frame, text="Target:", bg='#e8f4f8',
                font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.edit_tgt_lang_label = tk.Label(tgt_frame, text="", bg='#e8f4f8',
                                            fg='#666', font=('Segoe UI', 8))
        self.edit_tgt_lang_label.pack(anchor='w')
        
        self.edit_target_text = tk.Text(tgt_frame, height=4, wrap='word',
                                       font=('Segoe UI', 9), state='disabled')
        self.edit_target_text.pack(fill='both', expand=True)
        
        # Buttons
        btn_frame = tk.Frame(edit_frame, bg='#e8f4f8')
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.save_edit_btn = tk.Button(btn_frame, text="💾 Save Changes", 
                                       command=self.save_integrated_edit,
                                       bg='#4CAF50', fg='white', padx=15, pady=5,
                                       state='disabled')
        self.save_edit_btn.pack(side='left', padx=(0, 5))
        
        self.cancel_edit_btn = tk.Button(btn_frame, text="❌ Cancel", 
                                         command=self.cancel_integrated_edit,
                                         bg='#f44336', fg='white', padx=15, pady=5,
                                         state='disabled')
        self.cancel_edit_btn.pack(side='left')
        
        # Store currently edited TU
        self.current_edit_tu = None
    
    def create_grid_editor(self, parent):
        """Create grid editor for translation units using Treeview (supports selection & resizing)"""
        # Container with scrollbar
        grid_container = tk.Frame(parent)
        grid_container.pack(fill='both', expand=True)
        
        # Create Treeview with resizable columns
        columns = ('ID', 'Source', 'Target')
        self.tree = ttk.Treeview(grid_container, columns=columns, show='headings',
                                selectmode='browse', height=20)
        
        # Configure columns (resizable by user)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Source', text=f'Source ({self.src_lang if hasattr(self, "src_lang") and self.src_lang else ""})')
        self.tree.heading('Target', text=f'Target ({self.tgt_lang if hasattr(self, "tgt_lang") and self.tgt_lang else ""})')
        
        self.tree.column('ID', width=60, anchor='center', stretch=False)
        self.tree.column('Source', width=500, anchor='w', stretch=True)
        self.tree.column('Target', width=500, anchor='w', stretch=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(grid_container, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(grid_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        grid_container.grid_rowconfigure(0, weight=1)
        grid_container.grid_columnconfigure(0, weight=1)
        
        # Configure tag for search match highlighting (background color for matching rows)
        self.tree.tag_configure('match', background='#fffacd')  # Light yellow for matching rows
        
        # Double-click to edit
        self.tree.bind('<Double-Button-1>', self.on_tree_double_click)
        
        # Single-click to select and show in edit panel
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        # Store TU map
        self.tu_item_map = {}  # Maps tree item ID to TU object
        
        # Context menu
        self.create_context_menu()
    
    def create_pagination_controls(self, parent):
        """Create pagination controls"""
        page_frame = tk.Frame(parent, bg='#f0f0f0', relief='raised', bd=1)
        page_frame.pack(side='bottom', fill='x', pady=(5, 0))
        
        self.page_label = tk.Label(page_frame, text="Page 0 of 0 (0 TUs)",
                                   bg='#f0f0f0', font=('Segoe UI', 9))
        self.page_label.pack(side='left', padx=10, pady=5)
        
        # Navigation buttons
        nav_frame = tk.Frame(page_frame, bg='#f0f0f0')
        nav_frame.pack(side='right', padx=10)
        
        tk.Button(nav_frame, text="⏮️ First", command=self.first_page,
                 relief='flat', padx=8, pady=3).pack(side='left', padx=2)
        tk.Button(nav_frame, text="◀️ Prev", command=self.prev_page,
                 relief='flat', padx=8, pady=3).pack(side='left', padx=2)
        tk.Button(nav_frame, text="Next ▶️", command=self.next_page,
                 relief='flat', padx=8, pady=3).pack(side='left', padx=2)
        tk.Button(nav_frame, text="Last ⏭️", command=self.last_page,
                 relief='flat', padx=8, pady=3).pack(side='left', padx=2)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Label(self.container, text="Ready", bd=1, relief='sunken',
                                  anchor='w', bg='#e0e0e0')
        self.status_bar.pack(side='bottom', fill='x')
    
    def create_context_menu(self):
        """Create right-click context menu"""
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_selected_tu)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Refresh", command=self.refresh_current_page)
        
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    # ===== File Operations =====
    
    def new_tmx(self):
        """Create new TMX file"""
        if self.tmx_file and self.tmx_file.is_modified:
            if not messagebox.askyesno("Unsaved Changes",
                                      "Current file has unsaved changes. Continue?"):
                return
        
        # Prompt for languages
        dialog = tk.Toplevel(self.root if self.standalone else self.root.winfo_toplevel())
        dialog.title("New TMX File")
        dialog.geometry("400x250")
        dialog.transient(self.root if self.standalone else self.root.winfo_toplevel())
        
        tk.Label(dialog, text="Create New TMX File", font=('Segoe UI', 12, 'bold')).pack(pady=10)
        
        form_frame = tk.Frame(dialog)
        form_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(form_frame, text="Source Language:").grid(row=0, column=0, sticky='w', pady=5)
        src_entry = tk.Entry(form_frame, width=20)
        src_entry.grid(row=0, column=1, pady=5, padx=10)
        src_entry.insert(0, "en-US")
        
        tk.Label(form_frame, text="Target Language:").grid(row=1, column=0, sticky='w', pady=5)
        tgt_entry = tk.Entry(form_frame, width=20)
        tgt_entry.grid(row=1, column=1, pady=5, padx=10)
        tgt_entry.insert(0, "nl-NL")
        
        tk.Label(form_frame, text="Creator ID:").grid(row=2, column=0, sticky='w', pady=5)
        creator_entry = tk.Entry(form_frame, width=20)
        creator_entry.grid(row=2, column=1, pady=5, padx=10)
        creator_entry.insert(0, os.getlogin() if hasattr(os, 'getlogin') else "user")
        
        def create():
            src = src_entry.get().strip()
            tgt = tgt_entry.get().strip()
            creator = creator_entry.get().strip()
            
            if not src or not tgt:
                messagebox.showerror("Error", "Please enter both source and target languages")
                return
            
            self.tmx_file = TmxFile()
            self.tmx_file.header.srclang = src
            self.tmx_file.header.creation_id = creator
            self.tmx_file.header.change_id = creator
            self.tmx_file.languages = [src, tgt]
            
            # Add one empty translation unit
            tu = TmxTranslationUnit(tu_id=1, creation_id=creator)
            tu.set_segment(src, "")
            tu.set_segment(tgt, "")
            self.tmx_file.add_translation_unit(tu)
            
            self.src_lang = src
            self.tgt_lang = tgt
            
            self.refresh_ui()
            dialog.destroy()
            self.set_status(f"Created new TMX file: {src} → {tgt}")
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Create", command=create, bg='#4CAF50', fg='white',
                 padx=20, pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 padx=20, pady=5).pack(side='left', padx=5)
    
    def open_tmx(self):
        """Open TMX file"""
        if self.tmx_file and self.tmx_file.is_modified:
            if not messagebox.askyesno("Unsaved Changes",
                                      "Current file has unsaved changes. Continue?"):
                return
        
        file_path = filedialog.askopenfilename(
            title="Open TMX File",
            filetypes=[("TMX files", "*.tmx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.tmx_file = TmxParser.parse_file(file_path)
                
                # Set default languages (first two in file)
                langs = self.tmx_file.get_languages()
                if len(langs) >= 2:
                    self.src_lang = langs[0]
                    self.tgt_lang = langs[1]
                elif len(langs) == 1:
                    self.src_lang = langs[0]
                    self.tgt_lang = langs[0]
                
                self.refresh_ui()
                self.set_status(f"Opened: {os.path.basename(file_path)} ({self.tmx_file.get_tu_count()} TUs)")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open TMX file:\n{str(e)}")
    
    def save_tmx(self):
        """Save TMX file"""
        if not self.tmx_file:
            return
        
        if not self.tmx_file.file_path:
            self.save_tmx_as()
            return
        
        try:
            # Update change date
            self.tmx_file.header.change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            
            TmxParser.save_file(self.tmx_file)
            self.set_status(f"Saved: {os.path.basename(self.tmx_file.file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save TMX file:\n{str(e)}")
    
    def save_tmx_as(self):
        """Save TMX file with new name"""
        if not self.tmx_file:
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save TMX File As",
            defaultextension=".tmx",
            filetypes=[("TMX files", "*.tmx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Update change date
                self.tmx_file.header.change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
                
                TmxParser.save_file(self.tmx_file, file_path)
                self.set_status(f"Saved as: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save TMX file:\n{str(e)}")
    
    # ===== Edit Operations =====
    
    def add_translation_unit(self):
        """Add new translation unit"""
        if not self.tmx_file:
            messagebox.showwarning("Warning", "Please create or open a TMX file first")
            return
        
        if not self.src_lang or not self.tgt_lang:
            messagebox.showwarning("Warning", "Please select source and target languages")
            return
        
        # Create new TU
        new_id = self.tmx_file.get_tu_count() + 1
        tu = TmxTranslationUnit(tu_id=new_id,
                               creation_id=self.tmx_file.header.creation_id)
        tu.set_segment(self.src_lang, "")
        tu.set_segment(self.tgt_lang, "")
        
        self.tmx_file.add_translation_unit(tu)
        self.apply_filters()  # Refresh view
        self.set_status(f"Added TU #{new_id}")
    
    def delete_selected_tu(self):
        """Delete translation unit (placeholder)"""
        messagebox.showinfo("Info", "To delete a TU, double-click to edit it.\nDeletion feature coming soon.")
    
    def edit_selected_tu(self):
        """Edit selected translation unit (placeholder)"""
        messagebox.showinfo("Info", "Double-click on a TU to edit it.")
    
    def open_edit_dialog(self, tu: TmxTranslationUnit, tree_item=None):
        """Open dialog to edit translation unit"""
        dialog = tk.Toplevel(self.root if self.standalone else self.root.winfo_toplevel())
        dialog.title(f"Edit TU #{tu.tu_id}")
        dialog.geometry("800x400")
        dialog.transient(self.root if self.standalone else self.root.winfo_toplevel())
        
        # Source text
        tk.Label(dialog, text=f"Source ({self.src_lang}):", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 2))
        src_text = tk.Text(dialog, height=8, wrap='word', font=('Segoe UI', 10))
        src_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        src_seg = tu.get_segment(self.src_lang)
        if src_seg:
            src_text.insert('1.0', src_seg.text)
        
        # Target text
        tk.Label(dialog, text=f"Target ({self.tgt_lang}):", font=('Segoe UI', 10, 'bold')).pack(pady=(5, 2))
        tgt_text = tk.Text(dialog, height=8, wrap='word', font=('Segoe UI', 10))
        tgt_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        tgt_seg = tu.get_segment(self.tgt_lang)
        if tgt_seg:
            tgt_text.insert('1.0', tgt_seg.text)
        
        def save_changes():
            # Update segments
            tu.set_segment(self.src_lang, src_text.get('1.0', 'end-1c'))
            tu.set_segment(self.tgt_lang, tgt_text.get('1.0', 'end-1c'))
            tu.change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            
            self.tmx_file.is_modified = True
            
            # Refresh display
            self.refresh_current_page()
            
            dialog.destroy()
            self.set_status(f"Updated TU #{tu.tu_id}")
        
        # Buttons
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Save", command=save_changes, bg='#4CAF50', fg='white',
                 padx=20, pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 padx=20, pady=5).pack(side='left', padx=5)
        
        # Buttons
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Save", command=save_changes, bg='#4CAF50', fg='white',
                 padx=20, pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 padx=20, pady=5).pack(side='left', padx=5)
    
    def copy_source_to_target(self):
        """Copy source text to target (placeholder)"""
        messagebox.showinfo("Info", "Double-click a TU to edit it manually.")
    
    # ===== View Operations =====
    
    def on_language_changed(self, event=None):
        """Handle language selection change"""
        self.src_lang = self.src_lang_combo.get()
        self.tgt_lang = self.tgt_lang_combo.get()
        self.apply_filters()
    
    def show_all_languages(self):
        """Show dialog with all languages in TMX"""
        if not self.tmx_file:
            return
        
        dialog = tk.Toplevel(self.root if self.standalone else self.root.winfo_toplevel())
        dialog.title("All Languages")
        dialog.geometry("400x400")
        
        tk.Label(dialog, text="Languages in this TMX file:",
                font=('Segoe UI', 11, 'bold')).pack(pady=10)
        
        # List of languages
        lang_frame = tk.Frame(dialog)
        lang_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        listbox = tk.Listbox(lang_frame, font=('Segoe UI', 10))
        scrollbar = tk.Scrollbar(lang_frame, orient='vertical', command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
        
        for lang in self.tmx_file.get_languages():
            listbox.insert('end', lang)
        
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        tk.Button(dialog, text="Close", command=dialog.destroy,
                 padx=20, pady=5).pack(pady=10)
    
    def edit_header(self):
        """Edit TMX header metadata"""
        if not self.tmx_file:
            messagebox.showwarning("Warning", "Please create or open a TMX file first")
            return
        
        dialog = tk.Toplevel(self.root if self.standalone else self.root.winfo_toplevel())
        dialog.title("TMX Header Metadata")
        dialog.geometry("500x500")
        
        tk.Label(dialog, text="TMX Header Information",
                font=('Segoe UI', 12, 'bold')).pack(pady=10)
        
        # Form
        form_frame = tk.Frame(dialog)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        fields = {}
        row = 0
        
        for field_name, field_label in [
            ('creation_tool', 'Creation Tool'),
            ('creation_tool_version', 'Tool Version'),
            ('segtype', 'Segment Type'),
            ('o_tmf', 'O-TMF'),
            ('adminlang', 'Admin Language'),
            ('srclang', 'Source Language'),
            ('datatype', 'Data Type'),
            ('creation_id', 'Creator ID'),
            ('change_id', 'Last Modified By')
        ]:
            tk.Label(form_frame, text=f"{field_label}:").grid(row=row, column=0, sticky='w', pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=row, column=1, pady=5, padx=10, sticky='ew')
            entry.insert(0, getattr(self.tmx_file.header, field_name, ''))
            fields[field_name] = entry
            row += 1
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Read-only dates
        tk.Label(form_frame, text="Creation Date:").grid(row=row, column=0, sticky='w', pady=5)
        tk.Label(form_frame, text=self.tmx_file.header.creation_date,
                fg='#666').grid(row=row, column=1, sticky='w', pady=5, padx=10)
        row += 1
        
        tk.Label(form_frame, text="Last Modified:").grid(row=row, column=0, sticky='w', pady=5)
        tk.Label(form_frame, text=self.tmx_file.header.change_date,
                fg='#666').grid(row=row, column=1, sticky='w', pady=5, padx=10)
        
        def save_header():
            for field_name, entry in fields.items():
                setattr(self.tmx_file.header, field_name, entry.get())
            
            self.tmx_file.header.change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            self.tmx_file.is_modified = True
            
            dialog.destroy()
            self.set_status("Header updated")
        
        # Buttons
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Save", command=save_header, bg='#4CAF50', fg='white',
                 padx=20, pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 padx=20, pady=5).pack(side='left', padx=5)
    
    def show_statistics(self):
        """Show TMX file statistics"""
        if not self.tmx_file:
            return
        
        total_tus = self.tmx_file.get_tu_count()
        languages = self.tmx_file.get_languages()
        
        # Count segments per language
        lang_counts = {lang: 0 for lang in languages}
        total_chars = {lang: 0 for lang in languages}
        
        for tu in self.tmx_file.translation_units:
            for lang, segment in tu.segments.items():
                lang_counts[lang] += 1
                total_chars[lang] += len(segment.text)
        
        # Build statistics message
        stats = f"TMX File Statistics\n\n"
        stats += f"Total Translation Units: {total_tus}\n"
        stats += f"Languages: {len(languages)}\n\n"
        stats += "Segments per Language:\n"
        
        for lang in sorted(languages):
            avg_chars = total_chars[lang] / lang_counts[lang] if lang_counts[lang] > 0 else 0
            stats += f"  {lang}: {lang_counts[lang]} segments (avg {avg_chars:.1f} chars)\n"
        
        messagebox.showinfo("Statistics", stats)
    
    # ===== Filter Operations =====
    
    def apply_filters(self):
        """Apply filters and refresh grid"""
        if not self.tmx_file:
            return
        
        self.filter_source = self.filter_source_entry.get().lower()
        self.filter_target = self.filter_target_entry.get().lower()
        
        # Filter TUs
        self.filtered_tus = []
        for tu in self.tmx_file.translation_units:
            src_seg = tu.get_segment(self.src_lang)
            tgt_seg = tu.get_segment(self.tgt_lang)
            
            src_text = src_seg.text.lower() if src_seg else ""
            tgt_text = tgt_seg.text.lower() if tgt_seg else ""
            
            # Apply filters
            if self.filter_source and self.filter_source not in src_text:
                continue
            if self.filter_target and self.filter_target not in tgt_text:
                continue
            
            self.filtered_tus.append(tu)
        
        self.current_page = 0
        self.refresh_current_page()
    
    def clear_filters(self):
        """Clear all filters"""
        self.filter_source_entry.delete(0, 'end')
        self.filter_target_entry.delete(0, 'end')
        self.filter_source = ""
        self.filter_target = ""
        self.apply_filters()
    
    # ===== Helper Methods =====
    
    def _highlight_text_in_range(self, text_widget, start_index, end_index, search_term):
        """Highlight all occurrences of search_term in the given range (from concordance search)"""
        if not search_term:
            return
        
        search_term_lower = search_term.lower()
        start_line = int(start_index.split('.')[0])
        end_line = int(end_index.split('.')[0])
        
        for line_num in range(start_line, end_line + 1):
            line_text = text_widget.get(f"{line_num}.0", f"{line_num}.end")
            line_text_lower = line_text.lower()
            
            # Find all occurrences in this line
            start_pos = 0
            while True:
                pos = line_text_lower.find(search_term_lower, start_pos)
                if pos == -1:
                    break
                
                # Apply highlight tag
                highlight_start = f"{line_num}.{pos}"
                highlight_end = f"{line_num}.{pos + len(search_term_lower)}"
                text_widget.tag_add('highlight', highlight_start, highlight_end)
                
                start_pos = pos + len(search_term_lower)
    
    def highlight_search_term_in_text(self, text, search_term):
        """Highlight search term in text using Unicode bold characters
        
        Args:
            text: Text to search in
            search_term: Term to highlight
        
        Returns:
            Text with search term converted to Unicode bold
        """
        if not search_term or not text:
            return text
        
        # Case-insensitive search
        search_lower = search_term.lower()
        text_lower = text.lower()
        
        # Find all occurrences
        result = []
        last_pos = 0
        
        pos = text_lower.find(search_lower)
        while pos != -1:
            # Add text before match
            result.append(text[last_pos:pos])
            
            # Convert match to Unicode bold
            match_text = text[pos:pos + len(search_term)]
            bold_text = self._to_unicode_bold(match_text)
            result.append(bold_text)
            
            last_pos = pos + len(search_term)
            pos = text_lower.find(search_lower, last_pos)
        
        # Add remaining text
        result.append(text[last_pos:])
        
        return ''.join(result)
    
    def _to_unicode_bold(self, text):
        """Convert text to Unicode bold characters
        
        Unicode has Mathematical Bold characters that display as bold.
        This works in Treeview where normal formatting doesn't.
        """
        # Unicode bold character mappings
        bold_map = {
            # Uppercase A-Z: U+1D400 to U+1D419
            **{chr(ord('A') + i): chr(0x1D400 + i) for i in range(26)},
            # Lowercase a-z: U+1D41A to U+1D433
            **{chr(ord('a') + i): chr(0x1D41A + i) for i in range(26)},
            # Digits 0-9: U+1D7CE to U+1D7D7
            **{chr(ord('0') + i): chr(0x1D7CE + i) for i in range(10)},
        }
        
        # Convert each character
        return ''.join(bold_map.get(c, c) for c in text)
    
    # ===== Pagination =====
    
    def refresh_current_page(self):
        """Refresh current page in Treeview grid"""
        if not self.tmx_file:
            return
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tu_item_map.clear()
        
        # Update column headers with language codes
        self.tree.heading('Source', text=f'Source ({self.src_lang})')
        self.tree.heading('Target', text=f'Target ({self.tgt_lang})')
        
        # Calculate page range
        total_items = len(self.filtered_tus)
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
        
        if total_pages == 0:
            self.page_label.config(text="No items")
            return
        
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, total_items)
        
        # Add items to tree
        for tu in self.filtered_tus[start_idx:end_idx]:
            src_seg = tu.get_segment(self.src_lang)
            tgt_seg = tu.get_segment(self.tgt_lang)
            
            src_text = src_seg.text if src_seg else ""
            tgt_text = tgt_seg.text if tgt_seg else ""
            
            # Clean up text for display (remove newlines)
            src_display = src_text.replace('\n', ' ').replace('\r', '')
            tgt_display = tgt_text.replace('\n', ' ').replace('\r', '')
            
            # Highlight search terms with markers
            if self.filter_source:
                src_display = self.highlight_search_term_in_text(src_display, self.filter_source)
            if self.filter_target:
                tgt_display = self.highlight_search_term_in_text(tgt_display, self.filter_target)
            
            # Check if this row matches search (for light background highlighting)
            tags = ()
            if self.filter_source and self.filter_source.lower() in src_text.lower():
                tags = ('match',)
            elif self.filter_target and self.filter_target.lower() in tgt_text.lower():
                tags = ('match',)
            
            # Insert into tree
            item_id = self.tree.insert('', 'end', values=(tu.tu_id, src_display, tgt_display), tags=tags)
            
            # Store TU reference
            self.tu_item_map[item_id] = tu
        
        # Update page label
        self.page_label.config(text=f"Page {self.current_page + 1} of {total_pages} ({total_items} TUs)")
    
    def on_tree_select(self, event):
        """Handle tree selection - load into edit panel"""
        selected = self.tree.selection()
        if selected:
            item_id = selected[0]
            if item_id in self.tu_item_map:
                tu = self.tu_item_map[item_id]
                self.load_tu_into_edit_panel(tu)
    
    def on_tree_double_click(self, event):
        """Handle double-click on tree - load into edit panel and focus"""
        selected = self.tree.selection()
        if selected:
            item_id = selected[0]
            if item_id in self.tu_item_map:
                tu = self.tu_item_map[item_id]
                self.load_tu_into_edit_panel(tu)
                # Focus on target text for editing
                self.edit_target_text.focus_set()
    
    def edit_selected_tu(self):
        """Edit selected TU from context menu"""
        selected = self.tree.selection()
        if selected:
            item_id = selected[0]
            if item_id in self.tu_item_map:
                tu = self.tu_item_map[item_id]
                self.load_tu_into_edit_panel(tu)
                self.edit_target_text.focus_set()
    
    def load_tu_into_edit_panel(self, tu: TmxTranslationUnit):
        """Load a TU into the integrated edit panel"""
        self.current_edit_tu = tu
        
        # Update labels
        self.edit_id_label.config(text=f"Editing TU #{tu.tu_id}")
        self.edit_src_lang_label.config(text=f"({self.src_lang})")
        self.edit_tgt_lang_label.config(text=f"({self.tgt_lang})")
        
        # Load text
        self.edit_source_text.config(state='normal')
        self.edit_source_text.delete('1.0', 'end')
        src_seg = tu.get_segment(self.src_lang)
        if src_seg:
            self.edit_source_text.insert('1.0', src_seg.text)
        
        self.edit_target_text.config(state='normal')
        self.edit_target_text.delete('1.0', 'end')
        tgt_seg = tu.get_segment(self.tgt_lang)
        if tgt_seg:
            self.edit_target_text.insert('1.0', tgt_seg.text)
        
        # Enable buttons
        self.save_edit_btn.config(state='normal')
        self.cancel_edit_btn.config(state='normal')
        
        self.set_status(f"Editing TU #{tu.tu_id}")
    
    def save_integrated_edit(self):
        """Save changes from integrated edit panel"""
        if not self.current_edit_tu:
            return
        
        # Get updated text
        src_text = self.edit_source_text.get('1.0', 'end-1c')
        tgt_text = self.edit_target_text.get('1.0', 'end-1c')
        
        # Update TU
        self.current_edit_tu.set_segment(self.src_lang, src_text)
        self.current_edit_tu.set_segment(self.tgt_lang, tgt_text)
        self.current_edit_tu.change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        
        self.tmx_file.is_modified = True
        
        # Refresh display
        self.refresh_current_page()
        
        self.set_status(f"Saved changes to TU #{self.current_edit_tu.tu_id}")
        
        # Clear edit panel
        self.cancel_integrated_edit()
    
    def cancel_integrated_edit(self):
        """Cancel editing and clear the integrated edit panel"""
        self.current_edit_tu = None
        
        # Clear text
        self.edit_source_text.config(state='normal')
        self.edit_source_text.delete('1.0', 'end')
        self.edit_source_text.config(state='disabled')
        
        self.edit_target_text.config(state='normal')
        self.edit_target_text.delete('1.0', 'end')
        self.edit_target_text.config(state='disabled')
        
        # Reset labels
        self.edit_id_label.config(text="(Double-click a segment to edit)")
        self.edit_src_lang_label.config(text="")
        self.edit_tgt_lang_label.config(text="")
        
        # Disable buttons
        self.save_edit_btn.config(state='disabled')
        self.cancel_edit_btn.config(state='disabled')
        
        self.set_status("Ready")
    
    def first_page(self):
        """Go to first page"""
        self.current_page = 0
        self.refresh_current_page()
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh_current_page()
    
    def next_page(self):
        """Go to next page"""
        total_items = len(self.filtered_tus)
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
        
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.refresh_current_page()
    
    def last_page(self):
        """Go to last page"""
        total_items = len(self.filtered_tus)
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
        
        if total_pages > 0:
            self.current_page = total_pages - 1
            self.refresh_current_page()
    
    # ===== Tools =====
    
    def validate_tmx(self):
        """Validate TMX file structure"""
        if not self.tmx_file:
            messagebox.showwarning("Warning", "Please create or open a TMX file first")
            return
        
        issues = []
        
        # Check header
        if not self.tmx_file.header.srclang:
            issues.append("Missing source language in header")
        
        # Check translation units
        for tu in self.tmx_file.translation_units:
            if not tu.segments:
                issues.append(f"TU #{tu.tu_id}: No segments")
                continue
            
            # Check for empty segments
            for lang, seg in tu.segments.items():
                if not seg.text.strip():
                    issues.append(f"TU #{tu.tu_id}: Empty segment for {lang}")
        
        if issues:
            issues_text = "\n".join(issues[:20])  # Show first 20 issues
            if len(issues) > 20:
                issues_text += f"\n... and {len(issues) - 20} more issues"
            
            messagebox.showwarning("Validation Issues", 
                                  f"Found {len(issues)} issue(s):\n\n{issues_text}")
        else:
            messagebox.showinfo("Validation", "✓ No issues found. TMX file is valid!")
    
    def show_find_replace(self):
        """Show find/replace dialog"""
        messagebox.showinfo("Find/Replace", "Find/Replace feature coming soon!")
    
    def export_tmx(self):
        """Export TMX to other formats"""
        messagebox.showinfo("Export", "Export feature coming soon!")
    
    # ===== UI Helpers =====
    
    def refresh_ui(self):
        """Refresh entire UI after loading file"""
        if not self.tmx_file:
            return
        
        # Update language combos
        languages = self.tmx_file.get_languages()
        self.src_lang_combo['values'] = languages
        self.tgt_lang_combo['values'] = languages
        
        if self.src_lang in languages:
            self.src_lang_combo.set(self.src_lang)
        elif languages:
            self.src_lang_combo.set(languages[0])
            self.src_lang = languages[0]
        
        if self.tgt_lang in languages:
            self.tgt_lang_combo.set(self.tgt_lang)
        elif len(languages) > 1:
            self.tgt_lang_combo.set(languages[1])
            self.tgt_lang = languages[1]
        elif languages:
            self.tgt_lang_combo.set(languages[0])
            self.tgt_lang = languages[0]
        
        # Apply filters (will refresh grid)
        self.apply_filters()
    
    def set_status(self, message: str):
        """Set status bar message"""
        self.status_bar.config(text=message)
    
    def on_closing(self):
        """Handle window closing"""
        if self.tmx_file and self.tmx_file.is_modified:
            response = messagebox.askyesnocancel("Unsaved Changes",
                                                "Save changes before closing?")
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_tmx()
        
        if self.standalone:
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Run the application (standalone mode only)"""
        if self.standalone:
            self.root.mainloop()


# ===== Standalone Entry Point =====

def main():
    """Main entry point for standalone execution"""
    app = TmxEditorUI(standalone=True)
    app.run()


if __name__ == '__main__':
    main()
