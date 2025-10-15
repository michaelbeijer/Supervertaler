"""
Fix Tracked Changes feature in v3.2.0-beta:
1. Fix browse_tracked_changes to call show_browser() instead of show()
2. Remove TSV loading option from menu
3. Add Tracked Changes as a dedicated tab in the assistance panel
"""

with open('Supervertaler_v3.2.0-beta_CAT.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 70)
print("FIXING TRACKED CHANGES FEATURE IN v3.2.0-beta")
print("=" * 70)

# ========================================
# FIX 1: Change show() to show_browser()
# ========================================

old_browse_call = '''        self.tracked_changes_browser.show()'''
new_browse_call = '''        self.tracked_changes_browser.show_browser()'''

if old_browse_call in content:
    content = content.replace(old_browse_call, new_browse_call)
    print("\n✅ Fixed browse_tracked_changes to call show_browser()")
else:
    print("\n⚠️  Could not find show() call in browse_tracked_changes")

# ========================================
# FIX 2: Remove TSV menu option
# ========================================

old_tsv_menu = '''        translate_menu.add_command(label="📝 Load Tracked Changes (TSV)...", command=self.load_tracked_changes_tsv)'''

if old_tsv_menu in content:
    content = content.replace(old_tsv_menu, '')
    print("✅ Removed 'Load Tracked Changes (TSV)' menu option")
else:
    print("⚠️  TSV menu option not found")

# Also remove the Browse menu item (will be replaced by tab)
old_browse_menu = '''        translate_menu.add_command(label="🔍 Browse Tracked Changes...", command=self.browse_tracked_changes)'''

if old_browse_menu in content:
    content = content.replace(old_browse_menu, '')
    print("✅ Removed 'Browse Tracked Changes' menu option (replaced by tab)")
else:
    print("⚠️  Browse menu option not found")

# ========================================
# FIX 3: Add Tracked Changes tab
# ========================================

# Find the location after Settings tab and before Log tab
insertion_point = '''        # 11. Log (synchronized with main log window)
        if self.assist_visible_panels.get('log', True):
            log_tab_frame = tk.Frame(self.assist_notebook, bg='white')'''

new_tab_code = '''        # 11. Tracked Changes Analysis
        if self.assist_visible_panels.get('tracked_changes', True):
            tracked_changes_frame = tk.Frame(self.assist_notebook, bg='white')
            self.assist_notebook.add(tracked_changes_frame, text='📊 Changes')
            self.create_tracked_changes_tab(tracked_changes_frame)
        
        # 12. Log (synchronized with main log window)
        if self.assist_visible_panels.get('log', True):
            log_tab_frame = tk.Frame(self.assist_notebook, bg='white')'''

if insertion_point in content:
    content = content.replace(insertion_point, new_tab_code)
    print("✅ Added Tracked Changes tab to notebook")
else:
    print("⚠️  Could not find insertion point for tab")

# ========================================
# FIX 4: Add create_tracked_changes_tab method
# ========================================

# Find where to insert the new method (after create_settings_tab)
method_insertion = '''    def create_log_tab(self, parent):'''

new_method = '''    def create_tracked_changes_tab(self, parent):
        """Create the Tracked Changes Analysis tab"""
        parent.configure(bg='white')
        
        # Header
        header_frame = tk.Frame(parent, bg='#2c3e50', pady=8)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="📊 Post-Translation Analysis", 
                font=('Segoe UI', 12, 'bold'), bg='#2c3e50', fg='white').pack()
        tk.Label(header_frame, 
                text="Review differences between AI baseline and your final translations",
                font=('Segoe UI', 8), bg='#2c3e50', fg='#ecf0f1').pack()
        
        # Main content
        content_frame = tk.Frame(parent, bg='white', padx=10, pady=10)
        content_frame.pack(fill='both', expand=True)
        
        # Status section
        status_frame = tk.LabelFrame(content_frame, text="Current Status", 
                                    font=('Segoe UI', 10, 'bold'), bg='white', padx=10, pady=10)
        status_frame.pack(fill='x', pady=(0,10))
        
        self.tracked_changes_status_label = tk.Label(status_frame, 
                                                     text="No tracked changes loaded",
                                                     font=('Segoe UI', 10), fg='gray', bg='white')
        self.tracked_changes_status_label.pack(anchor='w', pady=5)
        
        # Update status if changes are loaded
        if hasattr(self, 'tracked_changes_agent') and self.tracked_changes_agent.change_data:
            count = len(self.tracked_changes_agent.change_data)
            files = len(self.tracked_changes_agent.files_loaded)
            self.tracked_changes_status_label.config(
                text=f"✅ {count} changes loaded from {files} file(s)",
                fg='green'
            )
        
        # Actions section
        actions_frame = tk.LabelFrame(content_frame, text="Actions", 
                                     font=('Segoe UI', 10, 'bold'), bg='white', padx=10, pady=10)
        actions_frame.pack(fill='x', pady=(0,10))
        
        # Load button
        load_btn = tk.Button(actions_frame, text="📂 Load Tracked Changes (DOCX)", 
                           command=self.load_tracked_changes_docx,
                           font=('Segoe UI', 10), bg='#3498db', fg='white',
                           cursor='hand2', relief='raised', bd=2, padx=15, pady=8)
        load_btn.pack(fill='x', pady=(0,5))
        
        # Browse/Export button
        browse_btn = tk.Button(actions_frame, text="📊 Browse & Export Analysis Report", 
                             command=self.browse_tracked_changes,
                             font=('Segoe UI', 10), bg='#27ae60', fg='white',
                             cursor='hand2', relief='raised', bd=2, padx=15, pady=8)
        browse_btn.pack(fill='x', pady=(0,5))
        
        # Clear button
        clear_btn = tk.Button(actions_frame, text="🗑 Clear All Changes", 
                            command=self.clear_tracked_changes,
                            font=('Segoe UI', 10), bg='#e74c3c', fg='white',
                            cursor='hand2', relief='raised', bd=2, padx=15, pady=8)
        clear_btn.pack(fill='x')
        
        # Info section
        info_frame = tk.LabelFrame(content_frame, text="How It Works", 
                                  font=('Segoe UI', 10, 'bold'), bg='white', padx=10, pady=10)
        info_frame.pack(fill='both', expand=True)
        
        info_text = """1. Complete your translation project in a CAT tool (memoQ, CafeTran, etc.)
   with tracked changes enabled

2. Export the bilingual document containing tracked changes

3. Click 'Load Tracked Changes' above to import the file

4. Click 'Browse & Export' to:
   • View all changes in a searchable browser
   • Export AI-powered analysis report (Markdown)
   • Configure batch processing (1-100 segments)
   • Get precise change summaries

Use this feature AFTER translation to:
✓ Review your editing decisions
✓ Track workflow improvements
✓ Document translation rationale
✓ Quality assurance checks"""
        
        info_label = tk.Label(info_frame, text=info_text, 
                            font=('Segoe UI', 9), bg='white', fg='#34495e',
                            justify='left', anchor='nw')
        info_label.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_log_tab(self, parent):'''

if method_insertion in content:
    content = content.replace(method_insertion, new_method)
    print("✅ Added create_tracked_changes_tab() method")
else:
    print("⚠️  Could not find insertion point for method")

# ========================================
# FIX 5: Add tracked_changes to default visible panels
# ========================================

old_visible_panels = '''        self.assist_visible_panels = {
            'projects': True,
            'system_prompts': True,
            'custom_instructions': True,
            'mt': True,
            'llm': True,
            'tm': True,
            'glossary': True,
            'reference_images': True,
            'nontrans': True,
            'settings': True,
            'log': True
        }'''

new_visible_panels = '''        self.assist_visible_panels = {
            'projects': True,
            'system_prompts': True,
            'custom_instructions': True,
            'mt': True,
            'llm': True,
            'tm': True,
            'glossary': True,
            'reference_images': True,
            'nontrans': True,
            'settings': True,
            'tracked_changes': True,
            'log': True
        }'''

if old_visible_panels in content:
    content = content.replace(old_visible_panels, new_visible_panels)
    print("✅ Added 'tracked_changes' to default visible panels")
else:
    print("⚠️  Could not find assist_visible_panels initialization")

# Write the updated content
with open('Supervertaler_v3.2.0-beta_CAT.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 70)
print("FIXES COMPLETE!")
print("=" * 70)
print("""
✅ Fixed browse_tracked_changes method call
✅ Removed TSV loading menu option
✅ Removed Browse menu option (replaced by tab)
✅ Added Tracked Changes tab to assistance panel
✅ Created create_tracked_changes_tab() method
✅ Added to default visible panels

CHANGES SUMMARY:
• Tracked Changes now appears as "📊 Changes" tab in right panel
• Tab includes: Status, Load button, Browse/Export button, Clear button, Info
• Browse button opens TrackedChangesBrowser window
• Export button generates AI-powered Markdown reports
• TSV import completely removed
• Menu items removed (functionality in tab)

TESTING:
1. Run Supervertaler_v3.2.0-beta_CAT.py
2. Check right panel has "📊 Changes" tab
3. Click tab to see Tracked Changes interface
4. Click "Load Tracked Changes (DOCX)"
5. Load a DOCX with tracked changes
6. Click "Browse & Export Analysis Report"
7. Verify browser window opens
8. Test export functionality
""")
