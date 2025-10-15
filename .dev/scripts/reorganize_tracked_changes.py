"""
1. Add explanation to the markdown report header
2. Move Tracked Changes out of Context Sources to its own section
"""

import re

# Read the current file
with open('Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ========================================
# CHANGE 1: Add explanation to MD report
# ========================================

old_md_header = '''            md_content = f"""# Tracked Changes Analysis Report

**Generated:** {timestamp}  
**Total Changes:** {len(data_to_export)}  
**Filter Applied:** {"Yes - " + search_text if export_filtered else "No"}  
**AI Analysis:** {"Enabled" if ai_analysis else "Disabled"}
{ai_prompt_info}
"""'''

new_md_header = '''            md_content = f"""# Tracked Changes Analysis Report

## What is this report?

This report analyzes the differences between AI-generated translations and your final edited versions exported from your CAT tool (memoQ, CafeTran, etc.). It shows exactly what you changed during post-editing, helping you review your editing decisions and track your translation workflow improvements.

**Use case:** After completing a translation project in your CAT tool with tracked changes enabled, export the bilingual document and load it here to see a detailed breakdown of all modifications made to the AI-generated baseline.

---

**Generated:** {timestamp}  
**Total Changes:** {len(data_to_export)}  
**Filter Applied:** {"Yes - " + search_text if export_filtered else "No"}  
**AI Analysis:** {"Enabled" if ai_analysis else "Disabled"}
{ai_prompt_info}
"""'''

if old_md_header in content:
    content = content.replace(old_md_header, new_md_header)
    print("✅ Added explanation to markdown report header!")
else:
    print("❌ Could not find MD report header")
    exit(1)

# ========================================
# CHANGE 2: Move Tracked Changes section
# ========================================

# First, find and extract the tracked changes section from Context Sources
old_tracked_changes_in_context = '''        # Tracked Changes row
        tk.Label(context_sources_frame, text="Tracked-changes:", bg="white").grid(row=context_row, column=0, padx=5, pady=2, sticky="w")
        

        tracked_changes_inner_frame = tk.Frame(context_sources_frame, bg="white")
        tracked_changes_inner_frame.grid(row=context_row, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        
        self.tracked_changes_status_label = tk.Label(tracked_changes_inner_frame, text="No tracked changes loaded", fg="gray", bg="white")
        self.tracked_changes_status_label.pack(side=tk.LEFT)
        
        tk.Button(tracked_changes_inner_frame, text="Load Files...", command=self.load_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        tk.Button(tracked_changes_inner_frame, text="Browse Changes", command=self.browse_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        tk.Button(tracked_changes_inner_frame, text="Clear", command=self.clear_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        context_row += 1'''

# Replace it with just a comment
new_context_without_tracked = '''        # Tracked Changes section moved below (not a context source for translation)'''

if old_tracked_changes_in_context in content:
    content = content.replace(old_tracked_changes_in_context, new_context_without_tracked)
    print("✅ Removed Tracked Changes from Context Sources section!")
else:
    print("❌ Could not find tracked changes in context sources")
    exit(1)

# Now find where to insert the new standalone section (after Context Sources frame, before Advanced Prompts)
insertion_point = '''        # Configure column weights for context sources frame
        context_sources_frame.grid_columnconfigure(1, weight=1)

        # Advanced Prompts Section (collapsible) - extra sharp heading font'''

new_insertion = '''        # Configure column weights for context sources frame
        context_sources_frame.grid_columnconfigure(1, weight=1)

        # Post-Translation Analysis Section
        analysis_frame = tk.LabelFrame(left_frame, text="📊 Post-Translation Analysis", font=("Segoe UI", 11, "bold"), padx=5, pady=5, bg="white")
        analysis_frame.grid(row=current_row, column=0, columnspan=3, padx=5, pady=(10,5), sticky="ew"); current_row += 1

        # Tracked Changes row
        tk.Label(analysis_frame, text="Tracked Changes Review:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        tracked_changes_inner_frame = tk.Frame(analysis_frame, bg="white")
        tracked_changes_inner_frame.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        self.tracked_changes_status_label = tk.Label(tracked_changes_inner_frame, text="No tracked changes loaded", fg="gray", bg="white")
        self.tracked_changes_status_label.pack(side=tk.LEFT)
        
        tk.Button(tracked_changes_inner_frame, text="Load Files...", command=self.load_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        tk.Button(tracked_changes_inner_frame, text="Browse Changes", command=self.browse_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        tk.Button(tracked_changes_inner_frame, text="Clear", command=self.clear_tracked_changes).pack(side=tk.RIGHT, padx=(5,0))
        
        # Info label explaining the feature
        info_label = tk.Label(analysis_frame, 
                            text="Load bilingual exports from CAT tools (memoQ, CafeTran) to analyze editing changes",
                            font=("Segoe UI", 8), fg="gray", bg="white", wraplength=600, justify="left")
        info_label.grid(row=1, column=0, columnspan=3, padx=5, pady=(0,5), sticky="w")
        
        # Configure column weights for analysis frame
        analysis_frame.grid_columnconfigure(1, weight=1)

        # Advanced Prompts Section (collapsible) - extra sharp heading font'''

if insertion_point in content:
    content = content.replace(insertion_point, new_insertion)
    print("✅ Created new 'Post-Translation Analysis' section with Tracked Changes!")
else:
    print("❌ Could not find insertion point")
    exit(1)

# Write the updated file
with open('Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("""
✅ Successfully reorganized Tracked Changes feature!

Changes made:

1. MARKDOWN REPORT HEADER:
   - Added clear explanation of what the report is
   - Explains it's for reviewing AI vs final edited versions
   - Notes the use case (post CAT tool export)
   
2. GUI REORGANIZATION:
   - Removed Tracked Changes from "Context Sources" section
   - Created new section: "📊 Post-Translation Analysis"
   - Placed AFTER Context Sources, BEFORE Advanced Prompts
   - Added explanatory label: "Load bilingual exports from CAT tools..."
   - Changed label from "Tracked-changes:" to "Tracked Changes Review:"
   
Purpose:
- Clarifies that this is NOT a translation context source
- It's a post-translation review tool for analyzing editing decisions
- Used AFTER translation is complete in CAT tools
- Shows how much the AI translation was modified

The feature now has its own dedicated section reflecting its true purpose!
""")
