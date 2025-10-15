# Script to insert export_to_tsv method

# Read the file
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find insertion point
insert_index = None
for i, line in enumerate(lines):
    if '# --- Helper Functions ---' in line and i > 500:
        insert_index = i
        break

if not insert_index:
    print('ERROR: Could not find insertion point')
    exit(1)

# Method to insert
method_code = '''    
    def export_to_tsv(self):
        """Export tracked changes to a TSV file"""
        from tkinter import filedialog, messagebox
        
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
            default_filename = "tracked_changes_filtered.tsv"
        else:
            data_to_export = self.tracked_changes_agent.change_data
            default_filename = "tracked_changes.tsv"
        
        # Ask for save location
        filepath = filedialog.asksaveasfilename(
            title="Export Tracked Changes to TSV",
            defaultextension=".tsv",
            filetypes=(("TSV files", "*.tsv"), ("All files", "*.*")),
            initialfile=default_filename
        )
        
        if not filepath:
            return
        
        try:
            # Write TSV file
            with open(filepath, 'w', encoding='utf-8') as f:
                for original, final in data_to_export:
                    # Escape tabs and newlines in the data
                    original_escaped = original.replace('\\t', ' ').replace('\\n', ' ').replace('\\r', '')
                    final_escaped = final.replace('\\t', ' ').replace('\\n', ' ').replace('\\r', '')
                    f.write(f"{original_escaped}\\t{final_escaped}\\n")
            
            messagebox.showinfo(
                "Export Successful",
                f"Exported {len(data_to_export)} change pairs to:\\n{filepath}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"Failed to export tracked changes:\\n{str(e)}"
            )

'''

# Insert the method
lines.insert(insert_index, method_code)

# Write back
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ Method inserted successfully!')
print(f'File now has {len(lines)} lines (was 4981, should be ~5052)')
