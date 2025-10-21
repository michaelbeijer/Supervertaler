# Phase 2 Implementation - Detailed Step-by-Step Checklist

## Overview
This document provides **line-by-line guidance** for implementing the Style Guides UI in Supervertaler. Follow each step sequentially.

**Total Time:** 6-9 hours  
**Complexity:** Medium (Tkinter UI + backend integration)

---

## ✅ STEP 1: Review Existing Infrastructure (30 minutes)

### 1.1 Verify Backend Module
- [ ] File exists: `c:\Dev\Supervertaler\modules\style_guide_manager.py`
- [ ] Verify it contains `StyleGuideLibrary` class with methods:
  - `get_all_languages()`
  - `get_guide(language)`
  - `update_guide(language, content)`
  - `append_to_guide(language, text)`
  - `append_to_all_guides(text)`
  - `export_guide(language, filepath)`
  - `import_guide(language, filepath)`
- [ ] Implementation verified: ✅ This is your data layer

### 1.2 Verify Default Guides Exist
- [ ] File: `user data/Style_Guides/Dutch.md` ✅
- [ ] File: `user data/Style_Guides/English.md` ✅
- [ ] File: `user data/Style_Guides/Spanish.md` ✅
- [ ] File: `user data/Style_Guides/German.md` ✅
- [ ] File: `user data/Style_Guides/French.md` ✅
- [ ] Each contains formatting rules for numbers, units, ranges, expressions, comparisons

### 1.3 Verify Main App Integration
**File:** `Supervertaler_v3.7.1.py`

Search for and verify:
- [ ] Line 202: `from modules.style_guide_manager import StyleGuideLibrary` (IMPORT EXISTS)
- [ ] Line 814: `self.style_guide_library = StyleGuideLibrary(...)` (INITIALIZATION EXISTS)
- [ ] Both are already in place ✅

---

## ✅ STEP 2: Understand the UI Template (30 minutes)

### 2.1 Open UI Template
- [ ] File: `docs/STYLE_GUIDES_UI_TEMPLATE.py`
- [ ] Total lines: ~380
- [ ] This file contains **complete Tkinter UI code** ready to copy

### 2.2 Review Template Structure
```
The template contains:
├── Imports (tkinter, ttk, ScrolledText)
├── create_style_guides_tab() method definition
├── UI frame setup (3 columns: list, content, chat)
├── Left panel: Language list (Treeview)
├── Center panel: Guide content (ScrolledText)
├── Right panel: Chat interface (Text + Entry)
├── Button event handlers
└── Backend integration methods
```

- [ ] Understand the 3-panel layout
- [ ] Understand button naming conventions
- [ ] Understand event handler patterns

### 2.3 Identify Key Component Names
- [ ] `self.style_guides_tree` - Language list widget
- [ ] `self.style_guides_text` - Content editor
- [ ] `self.style_guides_chat` - Chat display
- [ ] `self.style_guides_input` - Chat input
- [ ] `on_style_guide_select()` - List selection handler
- [ ] `on_style_guide_save()` - Save handler
- [ ] `on_style_guide_send_chat()` - Chat handler

---

## ✅ STEP 3: Prepare Main Application File (15 minutes)

### 3.1 Find Integration Location
**File:** `Supervertaler_v3.7.1.py`

**Task:** Locate where tabs are created (around line 15290)

Search for:
```python
self.assistant_notebook = ttk.Notebook(
```

- [ ] Find the section where `Prompt_Library_Tab` is created
- [ ] Find the section where `Custom_Instructions_Tab` is created
- [ ] This is where you'll add the Style Guides tab

### 3.2 Identify Tab Creation Pattern
Look for lines similar to:
```python
self.create_prompt_library_tab(self.assistant_notebook)
self.create_custom_instructions_tab(self.assistant_notebook)
```

- [ ] Copy this pattern for the new tab
- [ ] The Style Guides tab will follow the same structure

### 3.3 Verify Tab Method Pattern
**Find existing tab method in Supervertaler_v3.7.1.py** (search for `def create_prompt_library_tab`):

- [ ] Observe method signature: `def create_xyz_tab(self, parent_notebook)`
- [ ] Observe method return pattern (usually None, modifies parent)
- [ ] Note how widgets are added: `self.notebook_name.add(frame, text="Label")`

---

## ✅ STEP 4: Copy and Paste the UI Template (10 minutes)

### 4.1 Extract the Method from Template
**File:** `docs/STYLE_GUIDES_UI_TEMPLATE.py`

- [ ] Open this file
- [ ] Select ALL content (Ctrl+A)
- [ ] Copy (Ctrl+C)
- [ ] **DO NOT MODIFY YET** - just copy as-is

### 4.2 Create New Method Location
**File:** `Supervertaler_v3.7.1.py`

**Find:** The end of existing tab creation methods (after `create_custom_instructions_tab`)

- [ ] Find the last tab creation method
- [ ] Position your cursor after its closing bracket
- [ ] Add two blank lines
- [ ] Paste the entire template (Ctrl+V)

### 4.3 Verify Paste Success
- [ ] No syntax errors appear
- [ ] Method definition shows: `def create_style_guides_tab(self, parent_notebook):`
- [ ] All ~380 lines are intact
- [ ] Indentation looks correct (method is indented as class method)

**Result:** Method exists but is not yet called ✅

---

## ✅ STEP 5: Add Tab to Notebook (10 minutes)

### 5.1 Find Notebook Creation
**File:** `Supervertaler_v3.7.1.py` around line 15290

Find where tabs are added:
```python
self.create_prompt_library_tab(self.assistant_notebook)
self.create_custom_instructions_tab(self.assistant_notebook)
```

- [ ] Position cursor after the last `self.create_*_tab()` call
- [ ] Add new line

### 5.2 Add the Style Guides Tab Call
Insert:
```python
self.create_style_guides_tab(self.assistant_notebook)
```

- [ ] This calls your new method
- [ ] Passes the notebook as parent
- [ ] Tab will be automatically added to notebook

### 5.3 Test: Run Application
- [ ] Save `Supervertaler_v3.7.1.py`
- [ ] Start the application
- [ ] Navigate to Assistant panel
- [ ] Check if "Style Guides" tab appears
- [ ] Tab should be visible (even if buttons don't work yet)

**Expected:** Tab shows with empty content ✅

---

## ✅ STEP 6: Wire Up the List Widget (1-2 hours)

### 6.1 Find List Selection Handler
**In the template code you pasted, find:**
```python
def on_style_guide_select(self, event):
```

- [ ] This method is called when user selects a language from the list
- [ ] It should load and display that guide's content

### 6.2 Implement: Load Guide on Selection
**Replace the empty handler with:**

```python
def on_style_guide_select(self, event):
    """Load selected guide content when user clicks a language"""
    selection = self.style_guides_tree.selection()
    if not selection:
        return
    
    selected_language = self.style_guides_tree.item(selection[0])['values'][0]
    
    try:
        # Load guide content from backend
        content = self.style_guide_library.get_guide(selected_language)
        
        # Display in text widget
        self.style_guides_text.config(state=tk.NORMAL)
        self.style_guides_text.delete(1.0, tk.END)
        self.style_guides_text.insert(1.0, content)
        self.style_guides_text.config(state=tk.DISABLED)
        
        # Update status
        self.statusbar.config(text=f"Loaded: {selected_language}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load guide: {str(e)}")
```

- [ ] Method receives `event` parameter (from widget selection)
- [ ] Gets selected language from tree view
- [ ] Calls `self.style_guide_library.get_guide()`
- [ ] Displays content in `self.style_guides_text`
- [ ] Shows status message

### 6.3 Initialize List on Tab Creation
**Find in template:**
```python
# Populate list with languages
for language in self.style_guide_library.get_all_languages():
```

- [ ] Verify this code populates the list on startup
- [ ] Should show: Dutch, English, Spanish, German, French
- [ ] Check if working by clicking each language

### 6.4 Test: List Selection
- [ ] Run application
- [ ] Open Style Guides tab
- [ ] Click on each language
- [ ] Verify content loads in center panel
- [ ] Verify status bar updates

**Expected:** Content displays when language clicked ✅

---

## ✅ STEP 7: Implement Save Functionality (1 hour)

### 7.1 Find Save Button Handler
**In template, find:**
```python
def on_style_guide_save(self):
```

### 7.2 Implement Save to Backend
**Replace handler with:**

```python
def on_style_guide_save(self):
    """Save modified guide content to disk"""
    selection = self.style_guides_tree.selection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a language first")
        return
    
    selected_language = self.style_guides_tree.item(selection[0])['values'][0]
    content = self.style_guides_text.get(1.0, tk.END).strip()
    
    try:
        # Save to backend
        self.style_guide_library.update_guide(selected_language, content)
        self.statusbar.config(text=f"✅ Saved: {selected_language}")
        messagebox.showinfo("Success", f"Guide saved: {selected_language}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save guide: {str(e)}")
```

- [ ] Gets selected language
- [ ] Gets edited content from text widget
- [ ] Calls `self.style_guide_library.update_guide()`
- [ ] Shows confirmation message
- [ ] Updates status bar

### 7.3 Test: Save Functionality
- [ ] Run application
- [ ] Select a language
- [ ] Edit the content
- [ ] Click "Save"
- [ ] Verify success message appears
- [ ] Close and reopen app - changes should persist

**Expected:** Changes are saved to disk ✅

---

## ✅ STEP 8: Implement Export/Import (1-2 hours)

### 8.1 Export Button Handler
**Find in template:**
```python
def on_style_guide_export(self):
```

**Implement:**
```python
def on_style_guide_export(self):
    """Export selected guide to file"""
    selection = self.style_guides_tree.selection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a language")
        return
    
    selected_language = self.style_guides_tree.item(selection[0])['values'][0]
    
    # Ask user for file location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".md",
        filetypes=[("Markdown", "*.md"), ("Text", "*.txt")],
        initialfile=f"StyleGuide_{selected_language}.md"
    )
    
    if not file_path:
        return
    
    try:
        self.style_guide_library.export_guide(selected_language, file_path)
        messagebox.showinfo("Success", f"Exported to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {str(e)}")
```

- [ ] Gets selected language
- [ ] Opens file save dialog
- [ ] Calls backend export
- [ ] Shows confirmation

### 8.2 Import Button Handler
**Find in template:**
```python
def on_style_guide_import(self):
```

**Implement:**
```python
def on_style_guide_import(self):
    """Import guide from file"""
    # Ask user for file
    file_path = filedialog.askopenfilename(
        filetypes=[("Markdown", "*.md"), ("Text", "*.txt")]
    )
    
    if not file_path:
        return
    
    # Ask which language to import to
    language = simpledialog.askstring(
        "Select Language",
        "Which language to import to?\n(Dutch/English/Spanish/German/French)"
    )
    
    if not language:
        return
    
    try:
        self.style_guide_library.import_guide(language, file_path)
        # Reload display
        self.on_style_guide_select(None)
        messagebox.showinfo("Success", f"Imported to {language}")
    except Exception as e:
        messagebox.showerror("Error", f"Import failed: {str(e)}")
```

- [ ] Opens file dialog
- [ ] Asks which language to import to
- [ ] Calls backend import
- [ ] Reloads display

### 8.3 Test: Export/Import
- [ ] Run application
- [ ] Select a language
- [ ] Click "Export" - save file
- [ ] Edit the exported file
- [ ] Click "Import" - import back
- [ ] Verify changes are in app

**Expected:** Files can be exported and re-imported ✅

---

## ✅ STEP 9: Implement Batch Operations (1.5-2 hours)

### 9.1 "Add to All" Button Handler
**Find in template:**
```python
def on_style_guide_add_to_all(self):
```

**Implement:**
```python
def on_style_guide_add_to_all(self):
    """Add text to all languages"""
    text_to_add = simpledialog.askstring(
        "Add to All Languages",
        "Enter text to add to all style guides:"
    )
    
    if not text_to_add:
        return
    
    if not messagebox.askyesno("Confirm", "Add to all 5 language guides?"):
        return
    
    try:
        self.style_guide_library.append_to_all_guides(text_to_add)
        self.statusbar.config(text="✅ Added to all guides")
        messagebox.showinfo("Success", "Text added to all 5 language guides")
        # Reload current selection
        self.on_style_guide_select(None)
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {str(e)}")
```

- [ ] Prompts user for text
- [ ] Asks for confirmation
- [ ] Calls `append_to_all_guides()`
- [ ] Reloads display

### 9.2 "Add to Selected" Button Handler
**Find in template:**
```python
def on_style_guide_add_to_selected(self):
```

**Implement:**
```python
def on_style_guide_add_to_selected(self):
    """Add text to selected language"""
    selection = self.style_guides_tree.selection()
    if not selection:
        messagebox.showwarning("Warning", "Select a language first")
        return
    
    selected_language = self.style_guides_tree.item(selection[0])['values'][0]
    
    text_to_add = simpledialog.askstring(
        "Add to Guide",
        f"Enter text to add to {selected_language}:"
    )
    
    if not text_to_add:
        return
    
    try:
        self.style_guide_library.append_to_guide(selected_language, text_to_add)
        self.statusbar.config(text=f"✅ Added to {selected_language}")
        self.on_style_guide_select(None)
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {str(e)}")
```

- [ ] Gets selected language
- [ ] Prompts for text
- [ ] Calls `append_to_guide()`
- [ ] Reloads display

### 9.3 Test: Batch Operations
- [ ] Run application
- [ ] Click "Add to Selected" - add text to one language
- [ ] Verify it appears in guide
- [ ] Click "Add to All" - add text to all languages
- [ ] Verify text appears in all 5 guides

**Expected:** Batch operations work correctly ✅

---

## ✅ STEP 10: Implement Chat Interface (2-3 hours)

### 10.1 Initialize Chat on Tab Load
**In template, find:**
```python
# Initialize chat
self.style_guides_chat.insert(tk.END, "Welcome to Style Guides Chat...\n")
```

- [ ] This should show welcome message
- [ ] Verify message appears in chat widget

### 10.2 Chat Send Handler
**Find in template:**
```python
def on_style_guide_send_chat(self, event=None):
```

**Implement basic version first (before AI integration):**

```python
def on_style_guide_send_chat(self, event=None):
    """Handle chat message sending"""
    message = self.style_guides_input.get().strip()
    if not message:
        return
    
    # Display user message
    self.style_guides_chat.config(state=tk.NORMAL)
    self.style_guides_chat.insert(tk.END, f"\n[You]: {message}\n")
    self.style_guides_chat.see(tk.END)
    self.style_guides_chat.config(state=tk.DISABLED)
    
    # Clear input
    self.style_guides_input.delete(0, tk.END)
    
    # Parse command
    if message.lower().startswith("add to all"):
        # Extract text after "add to all"
        text_to_add = message[10:].strip()
        if text_to_add:
            self.style_guide_library.append_to_all_guides(text_to_add)
            self.display_chat_response("✅ Added to all guides")
    elif message.lower().startswith("add to"):
        # Parse: "add to Dutch: text"
        parts = message.split(":", 1)
        if len(parts) == 2:
            lang_part = parts[0].replace("add to", "").strip()
            text = parts[1].strip()
            self.style_guide_library.append_to_guide(lang_part, text)
            self.display_chat_response(f"✅ Added to {lang_part}")
    else:
        self.display_chat_response("Commands: 'add to all: text' or 'add to [Language]: text'")
    
    self.on_style_guide_select(None)

def display_chat_response(self, response):
    """Display bot response in chat"""
    self.style_guides_chat.config(state=tk.NORMAL)
    self.style_guides_chat.insert(tk.END, f"\n[Bot]: {response}\n")
    self.style_guides_chat.see(tk.END)
    self.style_guides_chat.config(state=tk.DISABLED)
```

- [ ] Gets message from input field
- [ ] Displays user message in chat
- [ ] Parses basic commands
- [ ] Executes batch operations
- [ ] Shows bot response

### 10.3 Test: Chat Interface
- [ ] Run application
- [ ] In Style Guides tab, in chat input type: `add to all: - New formatting rule`
- [ ] Verify message appears in chat
- [ ] Verify text is added to all guides
- [ ] Try: `add to Dutch: - Dutch specific rule`
- [ ] Verify it only adds to Dutch guide

**Expected:** Basic chat commands work ✅

---

## ✅ STEP 11: Integrate AI Assistant (2-3 hours)

### 11.1 Verify PromptAssistant Exists
**In Supervertaler_v3.7.1.py**, search for:
```python
self.prompt_assistant = PromptAssistant(...)
```

- [ ] Should find initialization in `__init__` method
- [ ] This is your AI integration point

### 11.2 Update Chat Handler to Call AI
**Replace the `on_style_guide_send_chat` method with:**

```python
def on_style_guide_send_chat(self, event=None):
    """Handle chat message with AI integration"""
    message = self.style_guides_input.get().strip()
    if not message:
        return
    
    # Display user message
    self.style_guides_chat.config(state=tk.NORMAL)
    self.style_guides_chat.insert(tk.END, f"\n[You]: {message}\n")
    self.style_guides_chat.see(tk.END)
    self.style_guides_chat.config(state=tk.DISABLED)
    
    # Clear input
    self.style_guides_input.delete(0, tk.END)
    self.style_guides_chat.config(state=tk.NORMAL)
    self.style_guides_chat.insert(tk.END, "\n[Bot]: Thinking...\n")
    self.style_guides_chat.config(state=tk.DISABLED)
    
    # Send to AI
    system_prompt = """You are a translation style guide assistant. 
Help users:
1. Add formatting rules to translation style guides
2. Suggest improvements to existing rules
3. Explain translation conventions
4. Handle batch operations to multiple language guides

When user says "add to [language]" or "add to all", extract the text to add 
and respond with what was added and to which guide(s)."""
    
    try:
        self.prompt_assistant.send_message(
            system_prompt=system_prompt,
            user_message=message,
            callback=self.on_style_guide_ai_response
        )
    except Exception as e:
        self.display_chat_response(f"Error: {str(e)}")

def on_style_guide_ai_response(self, response):
    """Handle AI response"""
    try:
        # Parse response and extract any "add to" commands
        if "add to" in response.lower():
            # AI might suggest adding to guides
            # Extract and apply
            self.display_chat_response(response)
            # Additional processing for batch operations if AI suggests them
        else:
            self.display_chat_response(response)
    except Exception as e:
        self.display_chat_response(f"Error processing response: {str(e)}")

def display_chat_response(self, response):
    """Display bot response in chat"""
    self.style_guides_chat.config(state=tk.NORMAL)
    self.style_guides_chat.delete("end-2c", tk.END)  # Remove "Thinking..."
    self.style_guides_chat.insert(tk.END, f"[Bot]: {response}\n")
    self.style_guides_chat.see(tk.END)
    self.style_guides_chat.config(state=tk.DISABLED)
```

- [ ] Creates system prompt for AI
- [ ] Calls `self.prompt_assistant.send_message()`
- [ ] Provides callback function
- [ ] AI response displayed in chat

### 11.3 Test: AI Integration
- [ ] Run application
- [ ] In chat, type: `Suggest a rule for number formatting in German`
- [ ] Wait for AI response
- [ ] Type: `add to German: German numbers should use periods as thousands separators`
- [ ] Verify AI responds and text is added

**Expected:** AI responds to questions and processes commands ✅

---

## ✅ STEP 12: Polish and Testing (1-2 hours)

### 12.1 Test Checklist
- [ ] **List Widget:**
  - [ ] All 5 languages display
  - [ ] Clicking each loads correct guide
  - [ ] Content displays properly

- [ ] **Content Editor:**
  - [ ] Text displays with proper formatting
  - [ ] Editing works
  - [ ] Save button saves changes
  - [ ] Changes persist after app restart

- [ ] **Export/Import:**
  - [ ] Export saves file correctly
  - [ ] Import loads file correctly
  - [ ] File format is readable

- [ ] **Batch Operations:**
  - [ ] "Add to Selected" works
  - [ ] "Add to All" works
  - [ ] Changes appear in all guides

- [ ] **Chat Interface:**
  - [ ] Messages display with timestamps
  - [ ] Commands are parsed correctly
  - [ ] AI responds appropriately
  - [ ] Chat history is maintained

- [ ] **Error Handling:**
  - [ ] Invalid operations show error messages
  - [ ] App doesn't crash on errors
  - [ ] Status bar updates appropriately

### 12.2 Common Issues & Fixes

**Issue: "AttributeError: StyleGuideLibrary not initialized"**
- Fix: Verify `self.style_guide_library` is initialized in `__init__` (line 814)

**Issue: Chat not connecting to AI**
- Fix: Verify `self.prompt_assistant` is initialized
- Check that `on_style_guide_ai_response` callback is defined

**Issue: Tab not appearing**
- Fix: Verify `self.create_style_guides_tab(self.assistant_notebook)` is called
- Check that tab is added to correct notebook

**Issue: Changes not saved**
- Fix: Verify `update_guide()` is being called
- Check file permissions in `user data/Style_Guides/`

### 12.3 UI Polish
- [ ] Verify button text is clear and concise
- [ ] Check that widget sizes are appropriate
- [ ] Ensure status bar provides helpful feedback
- [ ] Add keyboard shortcuts (Enter to send chat, Ctrl+S to save)
- [ ] Verify color scheme matches existing tabs

### 12.4 Documentation
- [ ] Add docstrings to all new methods
- [ ] Update README if needed
- [ ] Create user documentation for Style Guides feature

---

## 🎯 Summary of Implementation

| Step | Task | Estimated Time | Status |
|------|------|-----------------|--------|
| 1-5 | Setup & Template | 1.5 hours | 🔄 Current |
| 6 | List Widget | 1-2 hours | ⬜ Next |
| 7 | Save Functionality | 1 hour | ⬜ Pending |
| 8 | Export/Import | 1-2 hours | ⬜ Pending |
| 9 | Batch Operations | 1.5-2 hours | ⬜ Pending |
| 10 | Chat Interface | 2-3 hours | ⬜ Pending |
| 11 | AI Integration | 2-3 hours | ⬜ Pending |
| 12 | Testing & Polish | 1-2 hours | ⬜ Pending |
| **Total** | **All Phases** | **6-9 hours** | **🚀 Ready** |

---

## ✅ When Complete

After finishing Step 12:

1. ✅ Users can manage translation style guides for 5 languages
2. ✅ Users can edit guides with a full text editor
3. ✅ Users can export/import guides to/from files
4. ✅ Users can add content to single or all guides at once
5. ✅ AI assistant provides smart suggestions for guide content
6. ✅ Chat interface provides intuitive command handling

**Feature:** Style Guides Feature - COMPLETE ✅

---

## 📝 Next Steps When Done

- [ ] Test thoroughly with real user data
- [ ] Create video tutorial for users
- [ ] Add guide to main documentation
- [ ] Request beta testers
- [ ] Gather feedback for improvements

---

**Status:** Ready to implement  
**Start:** STEP 1: Review Existing Infrastructure  
**End Goal:** Fully functional Style Guides feature integrated with AI assistant
