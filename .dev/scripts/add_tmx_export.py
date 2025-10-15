# Script to add TMX export button and method

# Read the file
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add TMX button after TSV button
old_button_section = '''        tk.Button(export_frame, text="📄 Export to TSV", command=self.export_to_tsv,
                 bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                 relief="raised", padx=10, pady=5).pack(side=tk.LEFT)
        
        tk.Label(export_frame, text="Export all tracked changes to a TSV file (Original⇥Final format)",
                fg="gray").pack(side=tk.LEFT, padx=(10,0))'''

new_button_section = '''        tk.Button(export_frame, text="📄 Export to TSV", command=self.export_to_tsv,
                 bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                 relief="raised", padx=10, pady=5).pack(side=tk.LEFT, padx=(0,5))
        
        tk.Button(export_frame, text="💾 Export to TMX", command=self.export_to_tmx,
                 bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold"),
                 relief="raised", padx=10, pady=5).pack(side=tk.LEFT)
        
        tk.Label(export_frame, text="Export tracked changes for translation memory",
                fg="gray").pack(side=tk.LEFT, padx=(10,0))'''

content = content.replace(old_button_section, new_button_section)

# 2. Add export_to_tmx method after export_to_tsv
old_method_end = '''        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"Failed to export tracked changes:\\n{str(e)}"
            )

# --- Helper Functions ---'''

new_method_end = '''        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"Failed to export tracked changes:\\n{str(e)}"
            )
    
    def export_to_tmx(self):
        """Export tracked changes to TMX (Translation Memory eXchange) format"""
        from tkinter import filedialog, messagebox
        import xml.etree.ElementTree as ET
        from datetime import datetime
        
        if not self.tracked_changes_agent.change_data:
            messagebox.showwarning("No Data", "No tracked changes available to export.")
            return
        
        # Ask user whether to export all or filtered results
        search_text = self.search_var.get()
        if search_text:
            # User has active search filter
            result = messagebox.askyesnocancel(
                "Export Scope",
                f"You have an active search filter showing {len(self.tree.get_children())} of {len(self.tracked_changes_agent.change_data)} changes.\\n\\n"
                "Yes = Export filtered results only\\n"
                "No = Export all tracked changes\\n"
                "Cancel = Cancel export"
            )
            if result is None:  # Cancel
                return
            export_filtered = result
        else:
            export_filtered = False
        
        # Get the data to export
        if export_filtered:
            exact_match = self.exact_match_var.get()
            data_to_export = self.tracked_changes_agent.search_changes(search_text, exact_match)
            default_filename = "tracked_changes_filtered.tmx"
        else:
            data_to_export = self.tracked_changes_agent.change_data
            default_filename = "tracked_changes.tmx"
        
        # Ask for save location
        filepath = filedialog.asksaveasfilename(
            title="Export Tracked Changes to TMX",
            defaultextension=".tmx",
            filetypes=(("TMX files", "*.tmx"), ("All files", "*.*")),
            initialfile=default_filename
        )
        
        if not filepath:
            return
        
        try:
            # Create TMX structure
            tmx = ET.Element('tmx')
            tmx.set('version', '1.4')
            
            header = ET.SubElement(tmx, 'header')
            header.set('creationdate', datetime.now().strftime('%Y%m%dT%H%M%SZ'))
            header.set('srclang', 'en')  # Source is "original" text
            header.set('adminlang', 'en')
            header.set('segtype', 'sentence')
            header.set('creationtool', 'Supervertaler')
            header.set('creationtoolversion', APP_VERSION)
            header.set('datatype', 'plaintext')
            header.set('o-tmf', 'tracked-changes')
            
            # Add note about the content
            note = ET.SubElement(header, 'note')
            note.text = f'Tracked changes exported from document revisions. Original text → Final text pairs. Total segments: {len(data_to_export)}'
            
            body = ET.SubElement(tmx, 'body')
            
            # Add translation units
            for i, (original, final) in enumerate(data_to_export, 1):
                if not original.strip() or not final.strip():
                    continue
                    
                tu = ET.SubElement(body, 'tu')
                tu.set('tuid', f'tc_{i}')
                
                # Add creation date
                prop_date = ET.SubElement(tu, 'prop')
                prop_date.set('type', 'x-creation-date')
                prop_date.text = datetime.now().strftime('%Y%m%d')
                
                # Source segment (original text)
                tuv_src = ET.SubElement(tu, 'tuv')
                tuv_src.set('xml:lang', 'original')
                seg_src = ET.SubElement(tuv_src, 'seg')
                seg_src.text = original.strip()
                
                # Target segment (final/revised text)
                tuv_tgt = ET.SubElement(tu, 'tuv')
                tuv_tgt.set('xml:lang', 'revised')
                seg_tgt = ET.SubElement(tuv_tgt, 'seg')
                seg_tgt.text = final.strip()
            
            # Write TMX file
            tree = ET.ElementTree(tmx)
            ET.indent(tree, space='  ')  # Pretty print
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            
            messagebox.showinfo(
                "Export Successful",
                f"Exported {len(data_to_export)} tracked changes to TMX format:\\n{filepath}\\n\\n"
                f"This TMX can be imported into CAT tools as a reference translation memory."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"Failed to export tracked changes to TMX:\\n{str(e)}"
            )

# --- Helper Functions ---'''

content = content.replace(old_method_end, new_method_end)

# Write back
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ TMX export button and method added successfully!')
