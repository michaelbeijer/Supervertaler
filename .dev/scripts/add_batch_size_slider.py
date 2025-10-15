"""
Add a configurable batch size slider to the tracked changes export
"""

import re

# Read the current file
with open('Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the section where AI analysis is requested and add batch size dialog
old_ai_question = '''        # Ask if user wants AI analysis
        ai_analysis = messagebox.askyesno(
            "AI Analysis",
            f"Generate AI-powered change summaries?\\n\\n"
            f"This will analyze {len(data_to_export)} changes using the currently selected AI model.\\n\\n"
            f"Note: This may take a few minutes and will use API credits.\\n\\n"
            f"Click 'No' to export without AI analysis."
        )'''

new_ai_question = '''        # Ask if user wants AI analysis
        ai_analysis = messagebox.askyesno(
            "AI Analysis",
            f"Generate AI-powered change summaries?\\n\\n"
            f"This will analyze {len(data_to_export)} changes using the currently selected AI model.\\n\\n"
            f"Note: This may take a few minutes and will use API credits.\\n\\n"
            f"Click 'No' to export without AI analysis."
        )
        
        # If AI analysis enabled, let user choose batch size
        batch_size = 25  # Default
        if ai_analysis:
            batch_dialog = tk.Toplevel(self.window)
            batch_dialog.title("Batch Size Configuration")
            batch_dialog.geometry("450x200")
            batch_dialog.transient(self.window)
            batch_dialog.grab_set()
            
            tk.Label(batch_dialog, text="Configure Batch Processing", 
                    font=("Segoe UI", 11, "bold")).pack(pady=10)
            tk.Label(batch_dialog, 
                    text=f"Choose how many segments to process per AI request\\n"
                         f"Larger batches = faster but more tokens per request",
                    font=("Segoe UI", 9)).pack(pady=5)
            
            # Slider for batch size
            batch_var = tk.IntVar(value=25)
            
            slider_frame = tk.Frame(batch_dialog)
            slider_frame.pack(pady=10, fill='x', padx=20)
            
            tk.Label(slider_frame, text="Batch Size:", font=("Segoe UI", 9)).pack(side='left')
            batch_label = tk.Label(slider_frame, text="25", font=("Segoe UI", 10, "bold"), fg="blue")
            batch_label.pack(side='right')
            
            def update_label(val):
                batch_label.config(text=str(int(float(val))))
            
            slider = tk.Scale(batch_dialog, from_=1, to=100, orient='horizontal',
                            variable=batch_var, command=update_label, length=350)
            slider.pack(pady=5)
            
            # Info label
            info_label = tk.Label(batch_dialog, 
                                text=f"Total changes: {len(data_to_export)} | "
                                     f"Estimated batches at size 25: {(len(data_to_export) + 24) // 25}",
                                font=("Segoe UI", 8), fg="gray")
            info_label.pack(pady=5)
            
            def update_info(*args):
                size = batch_var.get()
                batches = (len(data_to_export) + size - 1) // size
                info_label.config(text=f"Total changes: {len(data_to_export)} | "
                                      f"Estimated batches at size {size}: {batches}")
            
            batch_var.trace('w', update_info)
            
            # OK button
            def on_ok():
                nonlocal batch_size
                batch_size = batch_var.get()
                batch_dialog.destroy()
            
            tk.Button(batch_dialog, text="OK", command=on_ok, 
                     font=("Segoe UI", 10), width=15).pack(pady=10)
            
            # Wait for dialog to close
            batch_dialog.wait_window()'''

# Replace in content
if old_ai_question in content:
    content = content.replace(old_ai_question, new_ai_question)
    print("✅ Added batch size slider dialog!")
else:
    print("❌ Could not find AI analysis question section")
    exit(1)

# Now update the hardcoded batch_size = 25 to use the variable instead
old_batch_line = '''                # Process in batches of 25
                batch_size = 25
                total_batches = (len(data_to_export) + batch_size - 1) // batch_size'''

new_batch_line = '''                # Process in batches (user-configured)
                # batch_size already set from dialog above
                total_batches = (len(data_to_export) + batch_size - 1) // batch_size'''

if old_batch_line in content:
    content = content.replace(old_batch_line, new_batch_line)
    print("✅ Updated batch processing to use configurable batch_size!")
else:
    print("❌ Could not find batch size initialization")
    exit(1)

# Write the updated file
with open('Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("""
✅ Successfully added batch size slider!

Changes made:
1. Added interactive dialog after user confirms AI analysis
2. Slider allows choosing batch size from 1 to 100
3. Shows real-time estimate of number of batches needed
4. Default value: 25 (optimal balance)
5. Removed hardcoded batch_size = 25

User experience:
- When "Generate AI summaries?" → Yes
- New dialog appears with slider
- User adjusts batch size (1-100)
- Shows estimated number of API calls
- Click OK to proceed with chosen batch size
""")
