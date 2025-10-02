# 🔗 FULL INTEGRATION PLAN: CAT Editor → Supervertaler v2.5.0

**Date**: October 2, 2025  
**Goal**: Fully integrate CAT Editor prototype into main Supervertaler application  
**Approach**: Option B - Full Integration (proper, professional implementation)  
**Timeline**: No rush - quality over speed  
**Target Version**: v2.5.0

---

## 🎯 INTEGRATION VISION

### What Success Looks Like

**Unified Translation Workflow:**
```
User Flow:
1. File → Import DOCX (with inline formatting & tables)
2. Segments appear in grid with source text + inline tags
3. Click "Translate" → AI translates all segments using current settings
4. Review/edit in grid (with tag validation)
5. Export to DOCX with formatting + TMX memory
6. Professional, integrated experience
```

**Key Benefits:**
- ✅ Single application for entire workflow
- ✅ DOCX import/export with formatting
- ✅ AI translation with multicontextual intelligence
- ✅ Interactive segment grid for review/editing
- ✅ Inline tag support (bold/italic/underline)
- ✅ Table cell segmentation (after Phase 1)
- ✅ Integration with TM, Custom Prompts, Project Library
- ✅ Professional single-tool experience

---

## 📋 PRE-INTEGRATION CHECKLIST

### ✅ Phase 0: Prepare CAT Editor (COMPLETE BEFORE INTEGRATION)

#### Step 0.1: Add Table Support (2-3 hours)
**Status**: Not started  
**Priority**: HIGH - Essential for professional documents

**Implementation**:
- Detect tables in DOCX
- Segment each table cell individually
- Track table structure (rows, columns, merged cells)
- Preserve table layout on export
- Handle nested tables if needed

**Files to modify**:
- `cat_tool_prototype/docx_handler.py` - Add table detection/export
- `cat_tool_prototype/simple_segmenter.py` - Add table segmentation
- `cat_tool_prototype/cat_editor_prototype.py` - Display table segments differently

**Test criteria**:
- [ ] Import DOCX with tables
- [ ] Each cell appears as separate segment
- [ ] Table structure preserved on export
- [ ] Merged cells handled correctly
- [ ] Nested tables work (if applicable)

#### Step 0.2: Real-World Testing (1-2 days)
**Status**: Not started  
**Priority**: HIGH - Validate before integration

**Test documents**:
- [ ] Patent document with figures and technical terms
- [ ] Contract with tables and formatted sections
- [ ] Technical manual with mixed content
- [ ] Marketing document with creative formatting
- [ ] Document with complex table structures

**Test scenarios**:
- [ ] Full import → translate → export cycle
- [ ] Inline tags preserved correctly
- [ ] No formatting loss
- [ ] No crashes or errors
- [ ] Performance acceptable (< 30 sec for 1000 segments)

#### Step 0.3: Bug Fixes & Polish (as needed)
**Status**: Ongoing  
**Priority**: MEDIUM - Fix issues found during testing

**Known potential issues**:
- Edge cases in tag validation
- Complex DOCX structures
- Very large documents (>5000 segments)
- Special characters in different languages

---

## 🏗️ INTEGRATION ARCHITECTURE

### Current Supervertaler Structure

```
Supervertaler_v2.4.0.py
├── TranslationApp class (main GUI)
├── Translation Agents (Gemini, Claude, OpenAI)
├── TMAgent (translation memory)
├── BilingualFileIngestionAgent (input processing)
├── OutputGenerationAgent (export)
├── TrackedChangesAgent (DOCX tracked changes)
├── Custom Prompts system
├── Project Library system
└── API key management
```

### Target Integrated Structure (v2.5.0)

```
Supervertaler_v2.5.0.py
├── TranslationApp class (enhanced)
│   ├── DOCX Import (NEW - from CAT Editor)
│   │   ├── docx_handler module
│   │   ├── tag_manager module
│   │   └── table_handler module (NEW in Phase 0.1)
│   ├── Segment Grid UI (NEW - from CAT Editor)
│   │   ├── Treeview with source/target/status
│   │   ├── Segment editor panel
│   │   ├── Tag validation & insertion
│   │   └── Status tracking
│   ├── Translation Pipeline (ENHANCED)
│   │   ├── Existing Translation Agents
│   │   ├── Segment-by-segment processing
│   │   ├── TM matching per segment
│   │   └── Custom Prompts per project
│   ├── DOCX Export (NEW - from CAT Editor)
│   │   ├── Format reconstruction
│   │   ├── Tag-to-formatting conversion
│   │   ├── Table structure preservation
│   │   └── Bilingual export option
│   └── Project Library (ENHANCED)
│       └── Save/load DOCX projects with segments
```

---

## 📐 IMPLEMENTATION PHASES

### PHASE 1: Foundation Setup (Day 1 - ~4 hours)

#### 1.1: Copy CAT Editor Modules
**Time**: 30 minutes

**Action**:
1. Copy these files to main Supervertaler directory:
   - `cat_tool_prototype/tag_manager.py` → `tag_manager.py`
   - `cat_tool_prototype/docx_handler.py` → `docx_handler.py`
   - `cat_tool_prototype/simple_segmenter.py` → `segmenter.py`

2. Update imports in copied files to work standalone

3. Test imports in main app:
```python
from tag_manager import TagManager
from docx_handler import DOCXHandler
from segmenter import SimpleSegmenter
```

**Files to create/modify**:
- New: `tag_manager.py`
- New: `docx_handler.py`
- New: `segmenter.py`
- Modified: `Supervertaler_v2.4.0.py` (add imports)

**Test criteria**:
- [ ] All modules import without errors
- [ ] No dependency conflicts
- [ ] python-docx available

#### 1.2: Create Segment Data Model
**Time**: 1 hour

**Action**:
1. Add Segment class to main application:
```python
class Segment:
    def __init__(self, seg_id, source, paragraph_id=0, table_cell=None):
        self.id = seg_id
        self.source = source
        self.target = ""
        self.status = "untranslated"
        self.paragraph_id = paragraph_id
        self.table_cell = table_cell  # NEW: (table_idx, row, col)
        self.notes = ""
        self.modified = False
        self.created_at = datetime.now().isoformat()
        self.modified_at = datetime.now().isoformat()
```

2. Add segment list to TranslationApp:
```python
self.segments = []  # List of Segment objects
self.current_segment = None
self.docx_handler = DOCXHandler()
self.tag_manager = TagManager()
self.segmenter = SimpleSegmenter()
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (add Segment class and attributes)

**Test criteria**:
- [ ] Segment class instantiates correctly
- [ ] Can create list of segments
- [ ] Attributes accessible

#### 1.3: Add DOCX Import UI
**Time**: 2 hours

**Action**:
1. Add "Import DOCX" button to existing file input area
2. Add file browser for DOCX selection
3. Add status label showing segment count
4. Update UI layout to accommodate new button

**UI Changes**:
```python
# Add after existing "Browse" button
self.import_docx_button = tk.Button(
    file_frame, 
    text="📄 Import DOCX", 
    command=self.import_docx_file,
    width=15,
    bg="#4CAF50",
    fg="white"
)
self.import_docx_button.pack(side=tk.LEFT, padx=5)

# Add status label
self.docx_status_label = tk.Label(
    file_frame,
    text="No DOCX loaded",
    font=("Segoe UI", 9),
    fg="#666666"
)
self.docx_status_label.pack(side=tk.LEFT, padx=10)
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (GUI setup section)

**Test criteria**:
- [ ] Button appears in UI
- [ ] File browser opens
- [ ] Can select DOCX file
- [ ] Status label updates

#### 1.4: Implement DOCX Import Logic
**Time**: 30 minutes

**Action**:
```python
def import_docx_file(self):
    """Import DOCX file and create segments"""
    file_path = filedialog.askopenfilename(
        title="Select DOCX File",
        filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
    )
    
    if not file_path:
        return
    
    try:
        self.update_log(f"Importing DOCX: {os.path.basename(file_path)}")
        
        # Import with formatting
        paragraphs = self.docx_handler.import_docx(file_path, extract_formatting=True)
        
        # Segment each paragraph
        self.segments = []
        seg_id = 1
        for para_id, para_text in enumerate(paragraphs):
            sentences = self.segmenter.segment_text(para_text)
            for sentence in sentences:
                segment = Segment(seg_id, sentence, para_id)
                self.segments.append(segment)
                seg_id += 1
        
        # Update UI
        self.docx_status_label.config(
            text=f"✓ Loaded: {len(self.segments)} segments from {len(paragraphs)} paragraphs",
            fg="#4CAF50"
        )
        self.update_log(f"✓ Created {len(self.segments)} segments")
        
        # Enable translation button
        self.process_button.config(state="normal")
        
    except Exception as e:
        messagebox.showerror("Import Error", f"Failed to import DOCX:\n{str(e)}")
        self.update_log(f"✗ Import failed: {str(e)}")
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (add method)

**Test criteria**:
- [ ] DOCX imports successfully
- [ ] Segments created correctly
- [ ] Paragraph IDs tracked
- [ ] Tags preserved in source text
- [ ] Status updates in UI
- [ ] Errors handled gracefully

---

### PHASE 2: Segment Grid UI (Day 2 - ~6 hours)

#### 2.1: Create Segment Grid Frame
**Time**: 2 hours

**Action**:
1. Add collapsible segment grid section to main UI
2. Create Treeview widget for segment display
3. Add scrollbars and column headers
4. Add expand/collapse toggle

**UI Structure**:
```python
# Add segment grid frame (collapsible)
self.segment_grid_frame = tk.LabelFrame(
    left_frame,
    text="📊 Translation Segments (Click to expand) ▶",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    cursor="hand2"
)
self.segment_grid_frame.grid(row=X, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
self.segment_grid_frame.bind("<Button-1>", self.toggle_segment_grid)

# Initially hidden content
self.segment_grid_content = tk.Frame(self.segment_grid_frame, bg="white")
self.segment_grid_visible = False

# Treeview for segments
self.segments_tree = ttk.Treeview(
    self.segment_grid_content,
    columns=('id', 'status', 'source', 'target'),
    show='headings',
    selectmode='browse',
    height=10
)

# Column configuration
self.segments_tree.heading('id', text='#')
self.segments_tree.heading('status', text='Status')
self.segments_tree.heading('source', text='Source')
self.segments_tree.heading('target', text='Target')

self.segments_tree.column('id', width=50, anchor='center')
self.segments_tree.column('status', width=100, anchor='center')
self.segments_tree.column('source', width=400, anchor='w')
self.segments_tree.column('target', width=400, anchor='w')

# Status colors
self.segments_tree.tag_configure('untranslated', background='#ffe6e6')
self.segments_tree.tag_configure('draft', background='#fff9e6')
self.segments_tree.tag_configure('translated', background='#e6ffe6')
self.segments_tree.tag_configure('approved', background='#e6f3ff')
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (GUI setup)

**Test criteria**:
- [ ] Grid appears in UI
- [ ] Can expand/collapse
- [ ] Columns sized correctly
- [ ] Scrollbars work

#### 2.2: Load Segments to Grid
**Time**: 1 hour

**Action**:
```python
def load_segments_to_grid(self):
    """Load segments into the treeview grid"""
    # Clear existing
    for item in self.segments_tree.get_children():
        self.segments_tree.delete(item)
    
    # Add segments
    for seg in self.segments:
        # Truncate for display
        source_display = seg.source[:80] + "..." if len(seg.source) > 80 else seg.source
        target_display = seg.target[:80] + "..." if len(seg.target) > 80 else seg.target
        
        self.segments_tree.insert(
            '', 'end',
            values=(
                seg.id,
                seg.status.capitalize(),
                source_display,
                target_display
            ),
            tags=(seg.status,)
        )
    
    self.update_log(f"Loaded {len(self.segments)} segments to grid")
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (add method)

**Test criteria**:
- [ ] Segments appear in grid
- [ ] Status colors applied
- [ ] Text truncated properly
- [ ] All segments visible

#### 2.3: Add Segment Editor Panel
**Time**: 2 hours

**Action**:
1. Create segment editor panel below grid
2. Add source/target text areas
3. Add status dropdown
4. Add tag insertion buttons
5. Add action buttons (Copy Source, Clear, Next, etc.)

**UI Structure**:
```python
# Segment editor panel
editor_frame = tk.LabelFrame(
    self.segment_grid_content,
    text="✏️ Segment Editor",
    font=("Segoe UI", 9, "bold"),
    bg="white"
)
editor_frame.pack(fill='x', padx=5, pady=5)

# Segment info
self.seg_info_label = tk.Label(
    editor_frame,
    text="No segment selected",
    font=("Segoe UI", 9, "bold"),
    bg="white"
)
self.seg_info_label.pack(anchor='w', padx=5, pady=5)

# Source (read-only)
tk.Label(editor_frame, text="Source:", font=("Segoe UI", 9, "bold"), bg="white").pack(anchor='w', padx=5)
self.segment_source_text = tk.Text(editor_frame, height=2, wrap='word', bg='#f5f5f5', state='disabled')
self.segment_source_text.pack(fill='x', padx=5, pady=2)

# Target (editable)
tk.Label(editor_frame, text="Target:", font=("Segoe UI", 9, "bold"), bg="white").pack(anchor='w', padx=5)
self.segment_target_text = tk.Text(editor_frame, height=2, wrap='word')
self.segment_target_text.pack(fill='x', padx=5, pady=2)

# Tag buttons
tag_frame = tk.Frame(editor_frame, bg="white")
tag_frame.pack(fill='x', padx=5, pady=2)
tk.Button(tag_frame, text="<b>Bold</b>", command=lambda: self.insert_segment_tag('b')).pack(side='left', padx=2)
tk.Button(tag_frame, text="<i>Italic</i>", command=lambda: self.insert_segment_tag('i')).pack(side='left', padx=2)
tk.Button(tag_frame, text="<u>Underline</u>", command=lambda: self.insert_segment_tag('u')).pack(side='left', padx=2)

# Status selector
status_frame = tk.Frame(editor_frame, bg="white")
status_frame.pack(fill='x', padx=5, pady=2)
tk.Label(status_frame, text="Status:", bg="white").pack(side='left')
self.segment_status_var = tk.StringVar(value="untranslated")
ttk.Combobox(status_frame, textvariable=self.segment_status_var, 
             values=["untranslated", "draft", "translated", "approved"],
             state='readonly', width=12).pack(side='left', padx=5)
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (GUI setup)

**Test criteria**:
- [ ] Editor panel displays
- [ ] Text areas work
- [ ] Buttons functional
- [ ] Status dropdown works

#### 2.4: Implement Segment Selection
**Time**: 1 hour

**Action**:
```python
def on_segment_select(self, event):
    """Handle segment selection in grid"""
    selection = self.segments_tree.selection()
    if not selection:
        return
    
    # Save current segment first
    if self.current_segment:
        self.save_current_segment()
    
    # Get selected segment
    item = selection[0]
    values = self.segments_tree.item(item, 'values')
    seg_id = int(values[0])
    
    # Find segment
    self.current_segment = next((s for s in self.segments if s.id == seg_id), None)
    
    if self.current_segment:
        self.load_segment_to_editor(self.current_segment)

def load_segment_to_editor(self, segment):
    """Load segment into editor panel"""
    self.seg_info_label.config(text=f"Segment #{segment.id} | Paragraph {segment.paragraph_id}")
    
    # Source
    self.segment_source_text.config(state='normal')
    self.segment_source_text.delete('1.0', 'end')
    self.segment_source_text.insert('1.0', segment.source)
    self.segment_source_text.config(state='disabled')
    
    # Target
    self.segment_target_text.delete('1.0', 'end')
    if segment.target:
        self.segment_target_text.insert('1.0', segment.target)
    
    # Status
    self.segment_status_var.set(segment.status)
    
    # Focus target
    self.segment_target_text.focus_set()

def save_current_segment(self):
    """Save current segment from editor"""
    if not self.current_segment:
        return
    
    target = self.segment_target_text.get('1.0', 'end-1c').strip()
    status = self.segment_status_var.get()
    
    if target != self.current_segment.target or status != self.current_segment.status:
        self.current_segment.target = target
        self.current_segment.status = status
        self.current_segment.modified = True
        self.current_segment.modified_at = datetime.now().isoformat()
        
        # Update grid
        self.update_segment_in_grid(self.current_segment)
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (add methods)

**Test criteria**:
- [ ] Click segment loads it in editor
- [ ] Source shows correctly
- [ ] Target editable
- [ ] Changes saved
- [ ] Grid updates

---

### PHASE 3: Translation Pipeline Integration (Day 3 - ~6 hours)

#### 3.1: Modify Translation Process
**Time**: 3 hours

**Action**:
1. Update main translation process to work with segments
2. Add segment-by-segment translation loop
3. Integrate with existing Translation Agents
4. Apply TM matching per segment
5. Use Custom Prompts if configured

**Core logic**:
```python
def process_translation(self):
    """Main translation process - enhanced for DOCX segments"""
    
    # Check if we have DOCX segments
    if self.segments:
        self.translate_segments()
    else:
        # Use existing TXT file translation
        self.translate_from_txt()

def translate_segments(self):
    """Translate DOCX segments using AI"""
    
    # Get settings
    provider = self.provider_var.get()
    model = self.model_var.get()
    source_lang = self.source_language_entry.get()
    target_lang = self.target_language_entry.get()
    
    # Get TM matches first
    if self.tm_file_path:
        self.update_log("Checking Translation Memory...")
        for segment in self.segments:
            tm_match = self.tm_agent.get_exact_match(segment.source)
            if tm_match:
                segment.target = tm_match
                segment.status = "translated"
                self.update_log(f"TM match for segment {segment.id}")
    
    # Get untranslated segments
    to_translate = [s for s in self.segments if s.status == "untranslated"]
    
    if not to_translate:
        self.update_log("All segments already translated!")
        return
    
    self.update_log(f"Translating {len(to_translate)} segments with {provider} {model}...")
    
    # Create full document context (for AI)
    full_context = "\n".join([s.source for s in self.segments])
    
    # Prepare segments for translation (in chunks)
    chunk_size = self.chunk_size_var.get()
    chunks = [to_translate[i:i+chunk_size] for i in range(0, len(to_translate), chunk_size)]
    
    # Translate each chunk
    for chunk_idx, chunk in enumerate(chunks, 1):
        self.update_log(f"Processing chunk {chunk_idx}/{len(chunks)} ({len(chunk)} segments)...")
        
        # Prepare batch text
        batch_text = "\n".join([f"{s.id}. {s.source}" for s in chunk])
        
        # Get custom prompt if configured
        system_prompt = self.current_translate_prompt  # Use existing prompt system
        
        # Call translation agent
        if provider == "Gemini":
            translations = self.gemini_translate_batch(batch_text, system_prompt, full_context, source_lang, target_lang, model)
        elif provider == "Claude":
            translations = self.claude_translate_batch(batch_text, system_prompt, full_context, source_lang, target_lang, model)
        elif provider == "OpenAI":
            translations = self.openai_translate_batch(batch_text, system_prompt, full_context, source_lang, target_lang, model)
        
        # Parse translations and update segments
        for segment in chunk:
            # Extract translation for this segment ID
            translation = self.extract_translation_for_segment(translations, segment.id)
            if translation:
                segment.target = translation
                segment.status = "draft"
                segment.modified_at = datetime.now().isoformat()
        
        # Update grid
        self.load_segments_to_grid()
    
    self.update_log("✓ Translation complete!")
    messagebox.showinfo("Translation Complete", f"Translated {len(to_translate)} segments")
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (modify main translation logic)

**Test criteria**:
- [ ] Translation runs without errors
- [ ] Segments get translated
- [ ] TM matches applied first
- [ ] Grid updates during translation
- [ ] Status changes to "draft"

#### 3.2: Add Progress Tracking
**Time**: 1 hour

**Action**:
1. Add progress bar for segment translation
2. Update segment count display
3. Show current segment being translated
4. Add cancel button

**Implementation**:
```python
# Progress bar
self.translation_progress = ttk.Progressbar(
    status_frame,
    orient="horizontal",
    length=300,
    mode="determinate"
)

# Update during translation
def update_translation_progress(self, current, total):
    progress = (current / total) * 100
    self.translation_progress['value'] = progress
    self.root.update_idletasks()
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (add progress tracking)

**Test criteria**:
- [ ] Progress bar shows during translation
- [ ] Updates smoothly
- [ ] Shows accurate progress

#### 3.3: Integrate Custom Prompts
**Time**: 1 hour

**Action**:
1. Use existing Custom Prompt system
2. Apply custom instructions to segment translation
3. Show which prompt is active
4. Allow prompt switching mid-project

**Implementation**:
```python
# Use existing custom prompt if loaded
if self.loaded_custom_prompt:
    self.update_log(f"Using custom prompt: {self.loaded_custom_prompt['name']}")
    system_prompt = self.loaded_custom_prompt['translation_prompt']
else:
    system_prompt = self.current_translate_prompt
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (integrate with existing system)

**Test criteria**:
- [ ] Custom prompts work with segments
- [ ] Prompt selection affects translation
- [ ] Can switch prompts between chunks

#### 3.4: Add TM Learning
**Time**: 1 hour

**Action**:
1. Learn from approved segments
2. Add to TM during translation
3. Export final TMX with all segments

**Implementation**:
```python
def export_segments_to_tmx(self):
    """Export segments to TMX file"""
    source_lang = self.source_language_entry.get()
    target_lang = self.target_language_entry.get()
    
    # Filter translated segments
    translated = [s for s in self.segments if s.target and s.status in ["translated", "approved"]]
    
    if not translated:
        messagebox.showwarning("No Translations", "No translated segments to export")
        return
    
    # Create TMX
    tmx_path = filedialog.asksaveasfilename(
        title="Save TMX",
        defaultextension=".tmx",
        filetypes=[("TMX Files", "*.tmx")]
    )
    
    if tmx_path:
        # Use existing TMAgent export functionality
        self.tm_agent.export_to_tmx(
            [(s.source, s.target) for s in translated],
            source_lang,
            target_lang,
            tmx_path
        )
        self.update_log(f"✓ Exported {len(translated)} segments to TMX")
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (add method)

**Test criteria**:
- [ ] TMX export works
- [ ] All translated segments included
- [ ] TMX format valid
- [ ] Can import back into TM

---

### PHASE 4: DOCX Export Integration (Day 4 - ~4 hours)

#### 4.1: Add Export UI
**Time**: 1 hour

**Action**:
1. Add "Export to DOCX" button
2. Add "Export Bilingual DOCX" button
3. Add export options (format selection)
4. Update existing export buttons

**UI Changes**:
```python
# Export section (enhance existing)
export_frame = tk.LabelFrame(left_frame, text="📤 Export", bg="white")

# DOCX export button
self.export_docx_button = tk.Button(
    export_frame,
    text="💾 Export to DOCX",
    command=self.export_to_docx,
    state="disabled",
    bg="#2196F3",
    fg="white",
    width=20
)
self.export_docx_button.pack(side='left', padx=5, pady=5)

# Bilingual DOCX button
self.export_bilingual_button = tk.Button(
    export_frame,
    text="📋 Export Bilingual DOCX",
    command=self.export_bilingual_docx,
    state="disabled",
    bg="#9C27B0",
    fg="white",
    width=20
)
self.export_bilingual_button.pack(side='left', padx=5, pady=5)

# TMX button (enhance existing)
self.export_tmx_button.config(text="💾 Export to TMX", bg="#FF9800")
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (GUI export section)

**Test criteria**:
- [ ] Export buttons appear
- [ ] Buttons disabled until ready
- [ ] Enable after translation

#### 4.2: Implement DOCX Export
**Time**: 2 hours

**Action**:
```python
def export_to_docx(self):
    """Export translated segments back to DOCX"""
    if not self.segments:
        messagebox.showwarning("No Segments", "No segments to export")
        return
    
    # Check if translations exist
    translated = [s for s in self.segments if s.target]
    if not translated:
        messagebox.showwarning("No Translations", "No translated segments to export")
        return
    
    # Get output path
    output_path = filedialog.asksaveasfilename(
        title="Export to DOCX",
        defaultextension=".docx",
        filetypes=[("Word Documents", "*.docx")]
    )
    
    if not output_path:
        return
    
    try:
        self.update_log("Exporting to DOCX...")
        
        # Prepare segment data for export
        seg_dicts = [s.to_dict() for s in self.segments]
        
        # Export using docx_handler
        self.docx_handler.export_docx(seg_dicts, output_path, preserve_formatting=True)
        
        self.update_log(f"✓ Exported to: {output_path}")
        messagebox.showinfo("Export Complete", f"Document exported successfully:\n{output_path}")
        
        # Ask if user wants to open the file
        if messagebox.askyesno("Open File", "Would you like to open the exported document?"):
            os.startfile(output_path)  # Windows
            # For Mac: subprocess.run(['open', output_path])
            # For Linux: subprocess.run(['xdg-open', output_path])
        
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export DOCX:\n{str(e)}")
        self.update_log(f"✗ Export failed: {str(e)}")

def export_bilingual_docx(self):
    """Export bilingual document (source | target table)"""
    if not self.segments:
        messagebox.showwarning("No Segments", "No segments to export")
        return
    
    output_path = filedialog.asksaveasfilename(
        title="Export Bilingual DOCX",
        defaultextension=".docx",
        filetypes=[("Word Documents", "*.docx")]
    )
    
    if not output_path:
        return
    
    try:
        self.update_log("Exporting bilingual DOCX...")
        
        seg_dicts = [s.to_dict() for s in self.segments]
        self.docx_handler.export_bilingual_docx(seg_dicts, output_path)
        
        self.update_log(f"✓ Bilingual export complete: {output_path}")
        messagebox.showinfo("Export Complete", "Bilingual document exported successfully")
        
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export bilingual DOCX:\n{str(e)}")
        self.update_log(f"✗ Export failed: {str(e)}")
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (add methods)

**Test criteria**:
- [ ] DOCX export creates valid file
- [ ] Formatting preserved
- [ ] Tags converted to formatting
- [ ] Bilingual export works
- [ ] Can open exported file

#### 4.3: Add Export Validation
**Time**: 1 hour

**Action**:
1. Check for untranslated segments before export
2. Warn about draft segments
3. Validate tag integrity
4. Confirm export options

**Implementation**:
```python
def validate_before_export(self):
    """Validate segments before export"""
    untranslated = [s for s in self.segments if not s.target]
    draft = [s for s in self.segments if s.status == "draft"]
    
    if untranslated:
        msg = f"Warning: {len(untranslated)} segments are untranslated.\n"
        msg += "These will be exported with source text.\n\n"
        msg += "Continue with export?"
        if not messagebox.askyesno("Untranslated Segments", msg):
            return False
    
    if draft:
        msg = f"Note: {len(draft)} segments are marked as 'draft'.\n"
        msg += "Consider reviewing before export.\n\n"
        msg += "Continue?"
        if not messagebox.askyesno("Draft Segments", msg):
            return False
    
    # Validate tags
    invalid_tags = []
    for seg in self.segments:
        if seg.target:
            is_valid, error_msg = self.tag_manager.validate_tags(seg.target)
            if not is_valid:
                invalid_tags.append(f"Segment {seg.id}: {error_msg}")
    
    if invalid_tags:
        msg = "Tag validation errors found:\n\n"
        msg += "\n".join(invalid_tags[:5])  # Show first 5
        if len(invalid_tags) > 5:
            msg += f"\n... and {len(invalid_tags)-5} more"
        msg += "\n\nExport may fail or lose formatting.\nContinue anyway?"
        if not messagebox.askyesno("Tag Errors", msg):
            return False
    
    return True
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (add validation method)

**Test criteria**:
- [ ] Validation catches issues
- [ ] User can cancel export
- [ ] Tag errors detected
- [ ] Warnings clear and helpful

---

### PHASE 5: Project Library Integration (Day 5 - ~3 hours)

#### 5.1: Enhance Project Save
**Time**: 1.5 hours

**Action**:
1. Save segments with project
2. Save DOCX path and metadata
3. Save segment status and modifications

**Implementation**:
```python
def save_project(self, file_path=None):
    """Save project including DOCX segments"""
    # ... existing project save code ...
    
    # Add segment data
    if self.segments:
        project_data['docx'] = {
            'original_path': self.docx_handler.original_path,
            'segment_count': len(self.segments),
            'segments': [s.to_dict() for s in self.segments]
        }
    
    # ... rest of existing save code ...
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (enhance save_project method)

**Test criteria**:
- [ ] Segments saved with project
- [ ] All segment data preserved
- [ ] Can save without segments (backward compatible)

#### 5.2: Enhance Project Load
**Time**: 1.5 hours

**Action**:
```python
def load_project(self, file_path):
    """Load project including DOCX segments"""
    # ... existing project load code ...
    
    # Load segments if present
    if 'docx' in project_data:
        docx_data = project_data['docx']
        self.update_log(f"Loading {docx_data['segment_count']} segments...")
        
        # Reconstruct segments
        self.segments = []
        for seg_dict in docx_data['segments']:
            segment = Segment.from_dict(seg_dict)
            self.segments.append(segment)
        
        # Update UI
        self.docx_status_label.config(
            text=f"✓ Loaded: {len(self.segments)} segments",
            fg="#4CAF50"
        )
        self.load_segments_to_grid()
        
        # Enable export buttons
        self.export_docx_button.config(state="normal")
        self.export_bilingual_button.config(state="normal")
    
    # ... rest of existing load code ...
```

**Files to modify**:
- `Supervertaler_v2.4.0.py` (enhance load_project method)

**Test criteria**:
- [ ] Projects load with segments
- [ ] Grid populated correctly
- [ ] Status and translations preserved
- [ ] Old projects still load (no segments)

---

### PHASE 6: Polish & Testing (Day 6 - ~6 hours)

#### 6.1: UI Refinements
**Time**: 2 hours

**Actions**:
- Improve layout and spacing
- Add keyboard shortcuts (Ctrl+S for save segment, Ctrl+Enter for next)
- Add tooltips for buttons
- Enhance status indicators
- Add progress indicators
- Polish colors and fonts

#### 6.2: Error Handling
**Time**: 2 hours

**Actions**:
- Add try-catch blocks throughout
- Validate inputs at each step
- Graceful degradation if modules missing
- Clear error messages
- Log all errors properly

#### 6.3: Comprehensive Testing
**Time**: 2 hours

**Test scenarios**:
- [ ] Import DOCX with various structures
- [ ] Import DOCX with tables
- [ ] Import DOCX with complex formatting
- [ ] Translate with each AI provider
- [ ] TM matching works correctly
- [ ] Custom prompts apply correctly
- [ ] Export preserves formatting
- [ ] Bilingual export works
- [ ] TMX export valid
- [ ] Project save/load with segments
- [ ] Backward compatibility (old projects without segments)
- [ ] Large documents (1000+ segments)
- [ ] Special characters in various languages
- [ ] Tag validation and insertion
- [ ] Segment editing and status changes

---

## 📊 IMPLEMENTATION TIMELINE

### Optimistic Schedule (Full-time work)
- **Day 1**: Phase 1 (Foundation) - 4 hours
- **Day 2**: Phase 2 (Segment Grid) - 6 hours
- **Day 3**: Phase 3 (Translation) - 6 hours
- **Day 4**: Phase 4 (Export) - 4 hours
- **Day 5**: Phase 5 (Projects) - 3 hours
- **Day 6**: Phase 6 (Polish) - 6 hours
- **Total**: ~29 hours (~4 days full-time)

### Realistic Schedule (Part-time work)
- **Week 1**: Phase 0 (Tables) + Phase 1 (Foundation)
- **Week 2**: Phase 2 (Segment Grid) + Phase 3 (Translation)
- **Week 3**: Phase 4 (Export) + Phase 5 (Projects)
- **Week 4**: Phase 6 (Polish) + Testing
- **Total**: ~4 weeks part-time

### Your Schedule (No rush)
- Work at comfortable pace
- Test thoroughly between phases
- Iterate on feedback
- **Estimated**: 2-3 weeks

---

## 🧪 TESTING STRATEGY

### Unit Testing (Per Phase)
Test each phase independently before moving to next

### Integration Testing (After Each Phase)
Ensure new features don't break existing functionality

### Regression Testing (Before Release)
Verify all existing Supervertaler features still work:
- [ ] TXT file translation
- [ ] Proofreading mode
- [ ] Tracked changes
- [ ] Image folder processing
- [ ] Custom prompts
- [ ] Project library (old projects)
- [ ] All AI providers
- [ ] TMX import/export

### User Acceptance Testing
Test with real documents and real workflows

---

## 🔄 ROLLBACK PLAN

### Version Control
- Create branch: `feature/cat-editor-integration`
- Commit after each phase
- Keep `main` branch stable

### Backup Current Version
```powershell
# Create backup before starting
cp Supervertaler_v2.4.0.py Supervertaler_v2.4.0_BACKUP.py
```

### Rollback Process
If integration causes issues:
1. Revert to backup
2. Review what went wrong
3. Adjust plan
4. Try again

---

## 📝 DOCUMENTATION TO UPDATE

### After Integration Complete

1. **User Guide** - Add DOCX workflow section
2. **Quick Start Guide** - Update with DOCX example
3. **CHANGELOG.md** - Comprehensive v2.5.0 entry
4. **README.md** - Highlight DOCX capabilities
5. **SESSION_PROGRESS_REPORT.md** - Update with integration results

---

## 🎯 SUCCESS CRITERIA

### Must Have (v2.5.0)
- ✅ DOCX import with inline tags
- ✅ Segment grid UI
- ✅ AI translation of segments
- ✅ DOCX export with formatting
- ✅ TMX export from segments
- ✅ Project save/load with segments
- ✅ Backward compatibility

### Should Have
- ✅ Table cell segmentation (Phase 0.1)
- ✅ Bilingual DOCX export
- ✅ Tag validation UI
- ✅ Progress indicators
- ✅ Keyboard shortcuts

### Nice to Have
- ⚪ QA checks (tag consistency)
- ⚪ Auto-propagation
- ⚪ SRX segmentation rules
- ⚪ Segment filtering
- ⚪ Statistics dashboard

---

## 🚀 GETTING STARTED

### Next Steps (In Order)

1. **Review this plan** - Make sure you understand and agree
2. **Phase 0.1: Add table support** - Complete CAT Editor first
3. **Phase 0.2: Test CAT Editor** - Validate with real documents
4. **Phase 1: Start integration** - Foundation setup
5. **Continue phases** - One at a time, test thoroughly

---

## 💬 QUESTIONS & DECISIONS NEEDED

### Before Starting

1. **Version Number**: Confirm v2.5.0 for integrated version?
2. **UI Layout**: Segment grid expanded by default or collapsed?
3. **Default Behavior**: DOCX import replaces TXT import or coexists?
4. **Export Options**: Which exports should be default?
5. **Keyboard Shortcuts**: Any specific preferences?

### During Implementation

- Regular check-ins after each phase
- Adjust plan based on what we learn
- Prioritize features as needs emerge

---

## 📞 SUPPORT & ASSISTANCE

I'll be here to help with:
- ✅ Writing all the code
- ✅ Debugging issues
- ✅ Testing guidance
- ✅ Architecture decisions
- ✅ Documentation
- ✅ Answering questions

Just let me know when you're ready to start, and we'll proceed phase by phase!

---

**Document**: FULL_INTEGRATION_PLAN.md  
**Created**: October 2, 2025  
**Status**: Ready to Execute  
**First Step**: Phase 0.1 - Add Table Support (2-3 hours)

**Let's build something amazing! 🚀**
