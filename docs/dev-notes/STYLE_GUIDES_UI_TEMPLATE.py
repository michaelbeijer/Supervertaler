"""
Style Guides Tab UI Template

This code template shows how to integrate the Style Guides tab into the 
Supervertaler assistant panel. This should be added to Supervertaler_v3.7.1.py
in the method that creates the assistant panel tabs.

Location in main file: Around line 14500-15300 where other tabs are created
or in a new method: create_style_guides_tab(parent)

Usage:
1. Create a method like: def create_style_guides_tab(self, parent)
2. Add this code to that method
3. In the notebook creation section, add:
   notebook.add(style_tab, text='📖 Style', sticky='nsew')
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime


def create_style_guides_tab(self, parent):
    """
    Create the Style Guides tab for the assistant panel.
    
    Layout:
    - Left panel: List of available style guides (languages)
    - Right panel: Style guide content + chat interface
    """
    
    # Main container
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    # === LEFT PANEL: Style Guide List ===
    left_frame = ttk.LabelFrame(main_frame, text="📚 Style Guides", padding=5)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
    
    # Load button
    load_guides_btn = ttk.Button(left_frame, text="🔄 Refresh", 
                                 command=lambda: refresh_guide_list())
    load_guides_btn.pack(fill=tk.X, pady=(0, 5))
    
    # Create treeview for style guides list
    tree_frame = ttk.Frame(left_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    
    # Treeview with scrollbar
    tree_scrollbar = ttk.Scrollbar(tree_frame)
    tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    style_guides_tree = ttk.Treeview(tree_frame, 
                                     columns=('language', 'modified'),
                                     height=15,
                                     yscrollcommand=tree_scrollbar.set)
    tree_scrollbar.config(command=style_guides_tree.yview)
    style_guides_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Configure columns
    style_guides_tree.column('#0', width=0, stretch=tk.NO)
    style_guides_tree.column('language', anchor=tk.W, width=100)
    style_guides_tree.column('modified', anchor=tk.W, width=100)
    
    style_guides_tree.heading('#0', text='', anchor=tk.W)
    style_guides_tree.heading('language', text='Language', anchor=tk.W)
    style_guides_tree.heading('modified', text='Modified', anchor=tk.W)
    
    # Track selected guide
    selected_guide = {'language': None, 'data': None}
    
    # === RIGHT PANEL: Content + Chat ===
    right_frame = ttk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Right panel header
    header_frame = ttk.Frame(right_frame)
    header_frame.pack(fill=tk.X, padx=5, pady=5)
    
    ttk.Label(header_frame, text="📖 Style Guide Content", 
             font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
    
    # Button frame for quick actions
    action_frame = ttk.Frame(header_frame)
    action_frame.pack(side=tk.RIGHT)
    
    # === TOP RIGHT: Content View ===
    content_frame = ttk.LabelFrame(right_frame, text="Content", padding=5)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
    
    # Content text with scrollbar
    content_scroll = ttk.Scrollbar(content_frame)
    content_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    guide_content = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, 
                                             height=10, font=('Consolas', 9),
                                             yscrollcommand=content_scroll.set)
    guide_content.pack(fill=tk.BOTH, expand=True)
    content_scroll.config(command=guide_content.yview)
    guide_content.config(state='disabled')
    
    # Content buttons
    content_btn_frame = ttk.Frame(right_frame)
    content_btn_frame.pack(fill=tk.X, padx=5, pady=5)
    
    def save_guide_changes():
        """Save changes to the selected guide"""
        if not selected_guide['language']:
            messagebox.showwarning("No Guide Selected", 
                                 "Please select a guide first")
            return
        
        new_content = guide_content.get('1.0', tk.END).strip()
        if self.style_guide_library.update_guide(selected_guide['language'], new_content):
            messagebox.showinfo("Success", 
                              f"Updated {selected_guide['language']} guide")
            selected_guide['data']['content'] = new_content
        else:
            messagebox.showerror("Error", 
                               "Failed to update guide")
    
    def export_guide():
        """Export selected guide to file"""
        if not selected_guide['language']:
            messagebox.showwarning("No Guide Selected", 
                                 "Please select a guide first")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            initialfile=f"{selected_guide['language']}_style_guide.md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), 
                      ("All files", "*.*")]
        )
        
        if file_path:
            if self.style_guide_library.export_guide(selected_guide['language'], file_path):
                messagebox.showinfo("Success", 
                                  f"Guide exported to {file_path}")
            else:
                messagebox.showerror("Error", "Failed to export guide")
    
    ttk.Button(content_btn_frame, text="💾 Save Changes", 
              command=save_guide_changes).pack(side=tk.LEFT, padx=2)
    ttk.Button(content_btn_frame, text="📥 Import", 
              command=lambda: import_guide_content()).pack(side=tk.LEFT, padx=2)
    ttk.Button(content_btn_frame, text="📤 Export", 
              command=export_guide).pack(side=tk.LEFT, padx=2)
    
    # === BOTTOM RIGHT: Chat Interface ===
    chat_frame = ttk.LabelFrame(right_frame, text="🤖 AI Assistant Chat", padding=5)
    chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
    
    # Chat history
    chat_scroll = ttk.Scrollbar(chat_frame)
    chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    chat_history = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=8,
                                            font=('Segoe UI', 9),
                                            yscrollcommand=chat_scroll.set)
    chat_history.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
    chat_scroll.config(command=chat_history.yview)
    chat_history.config(state='disabled')
    
    # Configure chat tags
    chat_history.tag_config('user', foreground='#0066cc', font=('Segoe UI', 9, 'bold'))
    chat_history.tag_config('assistant', foreground='#28a745', font=('Segoe UI', 9, 'bold'))
    chat_history.tag_config('error', foreground='#dc3545', font=('Segoe UI', 9, 'bold'))
    chat_history.tag_config('timestamp', foreground='#999', font=('Segoe UI', 8))
    
    # Input field
    input_frame = ttk.Frame(chat_frame)
    input_frame.pack(fill=tk.X)
    
    input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=3,
                                          font=('Segoe UI', 9))
    input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
    
    def add_chat_message(role, message):
        """Add message to chat history"""
        chat_history.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        chat_history.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        if role == 'user':
            chat_history.insert(tk.END, "You: ", 'user')
        elif role == 'assistant':
            chat_history.insert(tk.END, "AI: ", 'assistant')
        elif role == 'error':
            chat_history.insert(tk.END, "Error: ", 'error')
        
        chat_history.insert(tk.END, f"{message}\n\n")
        chat_history.see(tk.END)
        chat_history.config(state='disabled')
    
    def send_request():
        """Send request to AI for style guide modification"""
        if not selected_guide['language']:
            messagebox.showwarning("No Guide Selected", 
                                 "Please select a guide first")
            return
        
        request = input_text.get('1.0', tk.END).strip()
        if not request:
            messagebox.showwarning("Empty Request", 
                                 "Please enter a request")
            return
        
        # Add user message
        add_chat_message('user', request)
        input_text.delete('1.0', tk.END)
        
        # Check API configuration
        if not self.api_keys or self.current_llm_provider not in self.api_keys:
            add_chat_message('error', 
                           f"API key not configured for {self.current_llm_provider}")
            return
        
        # Show processing
        send_btn.config(state='disabled', text="⏳ Processing...")
        parent.update()
        
        try:
            # TODO: Implement AI processing for style guide requests
            # This should use self.prompt_assistant to process:
            # 1. "Add this to [language] guide" - append to specific guide
            # 2. "Add this to all guides" - append to all guides
            # 3. "Review this guide" - get AI suggestions for improvement
            
            # Placeholder response
            add_chat_message('assistant', 
                           "Feature coming soon! AI integration for style guides.")
            
        except Exception as e:
            add_chat_message('error', f"Error: {str(e)}")
        
        finally:
            send_btn.config(state='normal', text="📤 Send")
    
    send_btn = ttk.Button(input_frame, text="📤 Send", command=send_request)
    send_btn.pack(side=tk.RIGHT, padx=(5, 0))
    
    # === Helper Functions ===
    
    def refresh_guide_list():
        """Refresh the list of style guides"""
        style_guides_tree.delete(*style_guides_tree.get_children())
        count = self.style_guide_library.load_all_guides()
        
        for language in self.style_guide_library.get_all_languages():
            guide = self.style_guide_library.get_guide(language)
            modified = guide['_modified'].split('T')[0]  # Show only date
            style_guides_tree.insert('', tk.END, text='',
                                    values=(language, modified))
        
        self.log(f"✓ Loaded {count} style guides")
    
    def on_guide_selected(event):
        """Handle style guide selection"""
        selection = style_guides_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = style_guides_tree.item(item, 'values')
        language = values[0] if values else None
        
        if language:
            guide = self.style_guide_library.get_guide(language)
            if guide:
                selected_guide['language'] = language
                selected_guide['data'] = guide
                
                # Display content
                guide_content.config(state='normal')
                guide_content.delete('1.0', tk.END)
                guide_content.insert('1.0', guide['content'])
                guide_content.config(state='normal')  # Allow editing
                
                # Update header
                header_frame.winfo_children()[0].config(
                    text=f"📖 {language} Style Guide - Last modified: {guide['_modified']}"
                )
    
    def import_guide_content():
        """Import style guide content from file"""
        if not selected_guide['language']:
            messagebox.showwarning("No Guide Selected", 
                                 "Please select a guide first")
            return
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), 
                      ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Ask whether to append or replace
                if messagebox.askyesno("Import Option",
                                      "Append to existing guide?\n\n"
                                      "Yes = Append\n"
                                      "No = Replace"):
                    self.style_guide_library.append_to_guide(
                        selected_guide['language'], content)
                else:
                    self.style_guide_library.update_guide(
                        selected_guide['language'], content)
                
                # Refresh display
                guide = self.style_guide_library.get_guide(selected_guide['language'])
                guide_content.config(state='normal')
                guide_content.delete('1.0', tk.END)
                guide_content.insert('1.0', guide['content'])
                guide_content.config(state='normal')
                
                messagebox.showinfo("Success", "Guide updated successfully")
                selected_guide['data'] = guide
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")
    
    # Bind selection event
    style_guides_tree.bind('<<TreeviewSelect>>', on_guide_selected)
    
    # Initial load
    refresh_guide_list()
    
    return main_frame
