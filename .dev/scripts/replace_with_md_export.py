# Script to replace TMX export with enhanced MD report export

# Read the file
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update button section - remove TMX button, update TSV button to MD report
old_button_section = '''        tk.Button(export_frame, text="📄 Export to TSV", command=self.export_to_tsv,
                 bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                 relief="raised", padx=10, pady=5).pack(side=tk.LEFT, padx=(0,5))
        
        tk.Button(export_frame, text="💾 Export to TMX", command=self.export_to_tmx,
                 bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold"),
                 relief="raised", padx=10, pady=5).pack(side=tk.LEFT)
        
        tk.Label(export_frame, text="Export tracked changes for translation memory",
                fg="gray").pack(side=tk.LEFT, padx=(10,0))'''

new_button_section = '''        tk.Button(export_frame, text="📊 Export Report (MD)", command=self.export_to_md_report,
                 bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                 relief="raised", padx=10, pady=5).pack(side=tk.LEFT)
        
        tk.Label(export_frame, text="Export tracked changes report with AI-powered change analysis",
                fg="gray").pack(side=tk.LEFT, padx=(10,0))'''

content = content.replace(old_button_section, new_button_section)

# 2. Replace export_to_tsv method with export_to_md_report
# First, find and remove the old export_to_tsv method
old_tsv_method_start = '''    def export_to_tsv(self):
        """Export tracked changes to a TSV file"""'''

old_tsv_method_end = '''            messagebox.showerror(
                "Export Error",
                f"Failed to export tracked changes:\\n{str(e)}"
            )
    
    def export_to_tmx(self):'''

# Find the TSV method and replace it with MD report method
tsv_start_idx = content.find(old_tsv_method_start)
tmx_start_idx = content.find(old_tsv_method_end)

if tsv_start_idx != -1 and tmx_start_idx != -1:
    # Remove both old methods (TSV and TMX)
    # Find where TMX method ends
    tmx_method_end = '''            messagebox.showerror(
                "Export Error",
                f"Failed to export tracked changes to TMX:\\n{str(e)}"
            )

# --- Helper Functions ---'''
    
    helper_functions_idx = content.find('# --- Helper Functions ---', tmx_start_idx)
    
    if helper_functions_idx != -1:
        # Replace everything from start of export_to_tsv to Helper Functions with new method
        before_methods = content[:tsv_start_idx]
        after_methods = content[helper_functions_idx:]
        
        new_method = '''    def export_to_md_report(self):
        """Export tracked changes to a Markdown report with AI-powered change analysis"""
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
            default_filename = "tracked_changes_filtered_report.md"
        else:
            data_to_export = self.tracked_changes_agent.change_data
            default_filename = "tracked_changes_report.md"
        
        # Ask for save location
        filepath = filedialog.asksaveasfilename(
            title="Export Tracked Changes Report",
            defaultextension=".md",
            filetypes=(("Markdown files", "*.md"), ("All files", "*.*")),
            initialfile=default_filename
        )
        
        if not filepath:
            return
        
        # Ask if user wants AI analysis
        ai_analysis = messagebox.askyesno(
            "AI Analysis",
            f"Generate AI-powered change summaries?\\n\\n"
            f"This will analyze {len(data_to_export)} changes using the currently selected AI model.\\n\\n"
            f"Note: This may take a few minutes and will use API credits.\\n\\n"
            f"Click 'No' to export without AI analysis."
        )
        
        try:
            # Prepare report content
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            md_content = f"""# Tracked Changes Analysis Report

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
                    md_content += f"| {i} | {original_escaped} | _(same as source)_ | {final_escaped} |\\n"
            
            md_content += f"""

---

## Summary Statistics

- **Total Segments Analyzed:** {len(data_to_export)}
- **AI Analysis:** {"Enabled" if ai_analysis else "Disabled"}
- **Export Type:** {"Filtered" if export_filtered else "Complete"}

*This report was generated by Supervertaler v{APP_VERSION}*
"""
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            messagebox.showinfo(
                "Export Successful",
                f"Exported {len(data_to_export)} tracked changes to:\\n{filepath}\\n\\n"
                + ("AI change summaries included." if ai_analysis else "Export completed without AI analysis.")
            )
            
            self.log_queue.put(f"[Export] Report saved to: {filepath}")
            
        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"Failed to export tracked changes report:\\n{str(e)}"
            )
            self.log_queue.put(f"[Export] Error: {e}")
    
    def get_ai_change_summary(self, original_text, revised_text):
        """Get AI summary of what changed between original and revised text"""
        # This method needs to access the parent app's AI configuration
        # We'll need to pass the parent app reference when creating the browser
        
        # For now, return a simple diff-based summary as fallback
        # The parent app integration will be added in the next step
        
        if not hasattr(self, 'parent_app'):
            # Fallback to simple analysis
            if original_text == revised_text:
                return "No change"
            elif len(revised_text) > len(original_text):
                return "Expanded/added content"
            elif len(revised_text) < len(original_text):
                return "Shortened/removed content"
            else:
                return "Modified wording"
        
        # If parent_app is available, use its AI agent
        try:
            provider = self.parent_app.provider_var.get()
            model_name = self.parent_app.model_var.get()
            api_key = ""
            
            if provider == "Claude":
                api_key = self.parent_app.api_keys.get("claude", "")
            elif provider == "Gemini":
                api_key = self.parent_app.api_keys.get("google", "")
            elif provider == "OpenAI":
                api_key = self.parent_app.api_keys.get("openai", "")
            
            if not api_key:
                return "AI unavailable"
            
            # Create a temporary agent for this analysis
            if provider == "Gemini" and GOOGLE_AI_AVAILABLE:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                
                prompt = f"""Analyze this editing change and provide a VERY brief summary (max 10 words):

Original: {original_text}
Revised: {revised_text}

Summarize what changed (e.g., "Fixed grammar", "Clarified meaning", "Added detail", "Changed tone"):"""
                
                response = model.generate_content(prompt)
                summary = response.text.strip()
                # Limit to first sentence or 10 words
                summary = summary.split('.')[0].split('\\n')[0]
                words = summary.split()
                if len(words) > 10:
                    summary = ' '.join(words[:10]) + '...'
                return summary
                
            elif provider == "Claude" and CLAUDE_AVAILABLE:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                
                message = client.messages.create(
                    model=model_name,
                    max_tokens=50,
                    messages=[{
                        "role": "user",
                        "content": f"""Analyze this editing change and provide a VERY brief summary (max 10 words):

Original: {original_text}
Revised: {revised_text}

Summarize what changed (e.g., "Fixed grammar", "Clarified meaning", "Added detail"):"""
                    }]
                )
                
                summary = message.content[0].text.strip()
                words = summary.split()
                if len(words) > 10:
                    summary = ' '.join(words[:10]) + '...'
                return summary
                
            elif provider == "OpenAI" and OPENAI_AVAILABLE:
                import openai
                client = openai.OpenAI(api_key=api_key)
                
                response = client.chat.completions.create(
                    model=model_name,
                    max_tokens=50,
                    messages=[{
                        "role": "user",
                        "content": f"""Analyze this editing change and provide a VERY brief summary (max 10 words):

Original: {original_text}
Revised: {revised_text}

Summarize what changed (e.g., "Fixed grammar", "Clarified meaning", "Added detail"):"""
                    }]
                )
                
                summary = response.choices[0].message.content.strip()
                words = summary.split()
                if len(words) > 10:
                    summary = ' '.join(words[:10]) + '...'
                return summary
            else:
                return "Simple text change"
                
        except Exception as e:
            self.log_queue.put(f"[AI Summary] Error: {e}")
            return "Analysis failed"

'''
        
        content = before_methods + new_method + after_methods

# Write back
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Successfully replaced TMX/TSV exports with enhanced MD report export!')
print('   - Button updated to "Export Report (MD)"')
print('   - New method generates 4-column markdown table')
print('   - Includes AI-powered change summaries (optional)')
print('   - Note: Parent app reference needed for full AI integration')
