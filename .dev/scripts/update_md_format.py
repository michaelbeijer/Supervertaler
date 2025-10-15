# Script to update MD export format from table to readable paragraphs

# Read the file
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the report generation section
old_section = '''            md_content = f"""# Tracked Changes Analysis Report

**Generated:** {timestamp}  
**Total Changes:** {len(data_to_export)}  
**Filter Applied:** {"Yes - " + search_text if export_filtered else "No"}

---

## Changes Overview

"""
            
            if ai_analysis:
                md_content += "| # | Source | Target (Original) | Target (Revised) | Change Summary |\\n"
                md_content += "|---|--------|-------------------|------------------|----------------|\\n"
            else:
                md_content += "| # | Source | Target (Original) | Target (Revised) |\\n"
                md_content += "|---|--------|-------------------|------------------|\\n"
            
            # Process changes
            if ai_analysis:
                # Get AI agent from parent app (need to access the main app instance)
                # We'll generate summaries in batches to be efficient
                self.log_queue.put(f"[Export] Generating AI summaries for {len(data_to_export)} changes...")
                
                # Show progress window
                progress_window = tk.Toplevel(self.window)
                progress_window.title("Generating AI Analysis...")
                progress_window.geometry("400x100")
                progress_window.transient(self.window)
                progress_window.grab_set()
                
                tk.Label(progress_window, text="Analyzing tracked changes with AI...", 
                        font=("Segoe UI", 10)).pack(pady=10)
                progress_label = tk.Label(progress_window, text="Processing change 0 of " + str(len(data_to_export)))
                progress_label.pack()
                
                for i, (original, final) in enumerate(data_to_export, 1):
                    progress_label.config(text=f"Processing change {i} of {len(data_to_export)}")
                    progress_window.update()
                    
                    # Escape pipe characters for markdown tables
                    original_escaped = original.replace('|', '\\\\|').replace('\\n', ' ')
                    final_escaped = final.replace('|', '\\\\|').replace('\\n', ' ')
                    
                    # Generate AI summary for this change
                    try:
                        summary = self.get_ai_change_summary(original, final)
                        summary_escaped = summary.replace('|', '\\\\|').replace('\\n', ' ')
                    except Exception as e:
                        summary_escaped = f"Error: {str(e)}"
                        self.log_queue.put(f"[Export] Error generating summary for change {i}: {e}")
                    
                    # For source, we use original (before any changes)
                    # But tracked changes only have original→final pairs
                    # So we'll treat "original" as the source and "final" as revised
                    md_content += f"| {i} | {original_escaped} | _(same as source)_ | {final_escaped} | {summary_escaped} |\\n"
                
                progress_window.destroy()
            else:
                # No AI analysis - just export the data
                for i, (original, final) in enumerate(data_to_export, 1):
                    original_escaped = original.replace('|', '\\\\|').replace('\\n', ' ')
                    final_escaped = final.replace('|', '\\\\|').replace('\\n', ' ')
                    md_content += f"| {i} | {original_escaped} | _(same as source)_ | {final_escaped} |\\n"'''

new_section = '''            md_content = f"""# Tracked Changes Analysis Report

**Generated:** {timestamp}  
**Total Changes:** {len(data_to_export)}  
**Filter Applied:** {"Yes - " + search_text if export_filtered else "No"}  
**AI Analysis:** {"Enabled" if ai_analysis else "Disabled"}

---

"""
            
            # Process changes with paragraph format
            if ai_analysis:
                # Show progress window
                self.log_queue.put(f"[Export] Generating AI summaries for {len(data_to_export)} changes...")
                
                progress_window = tk.Toplevel(self.window)
                progress_window.title("Generating AI Analysis...")
                progress_window.geometry("400x100")
                progress_window.transient(self.window)
                progress_window.grab_set()
                
                tk.Label(progress_window, text="Analyzing tracked changes with AI...", 
                        font=("Segoe UI", 10)).pack(pady=10)
                progress_label = tk.Label(progress_window, text="Processing change 0 of " + str(len(data_to_export)))
                progress_label.pack()
                
                for i, (original, final) in enumerate(data_to_export, 1):
                    progress_label.config(text=f"Processing change {i} of {len(data_to_export)}")
                    progress_window.update()
                    
                    # Generate AI summary for this change
                    try:
                        summary = self.get_ai_change_summary(original, final)
                    except Exception as e:
                        summary = f"_Error generating summary: {str(e)}_"
                        self.log_queue.put(f"[Export] Error generating summary for change {i}: {e}")
                    
                    # Add segment in paragraph format
                    md_content += f"""### Segment {i}

**Target (Original):**  
{original}

**Target (Revised):**  
{final}

**Change Summary:**  
{summary}

---

"""
                
                progress_window.destroy()
            else:
                # No AI analysis - simpler paragraph format
                for i, (original, final) in enumerate(data_to_export, 1):
                    md_content += f"""### Segment {i}

**Target (Original):**  
{original}

**Target (Revised):**  
{final}

---

"""'''

content = content.replace(old_section, new_section)

# Write back
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Updated MD export format!')
print('   - Replaced wide table with readable paragraph format')
print('   - Each segment is now a separate section')
print('   - Much easier to read and compare changes')
print('   - AI summaries (when enabled) are clearly displayed')
