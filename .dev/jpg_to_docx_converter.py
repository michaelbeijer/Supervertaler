"""
JPG to DOCX Converter
Converts a series of JPG/PNG screenshots (e.g., from PDF) into a Word document
Each image is placed on its own page, scaled to fit the page dimensions

Usage:
    python jpg_to_docx_converter.py
    
    Then select the folder containing your JPG files via file dialog,
    or drag & drop JPGs onto the script window.
"""

import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from docx import Document
from docx.shared import Inches, Pt
from PIL import Image

class JPGtoDOCXConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JPG to DOCX Converter")
        self.root.geometry("600x400")
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title = tk.Label(main_frame, text="JPG/PNG to DOCX Converter", 
                        font=('Segoe UI', 16, 'bold'))
        title.pack(pady=(0, 10))
        
        # Instructions
        instructions = tk.Label(main_frame, 
                               text="Convert a series of image files into a Word document\n"
                                    "Each image will be placed on its own page",
                               font=('Segoe UI', 9), justify='center')
        instructions.pack(pady=(0, 20))
        
        # File list
        list_frame = tk.LabelFrame(main_frame, text="Images to Convert", padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Scrollbar and listbox
        scroll = tk.Scrollbar(list_frame, orient='vertical')
        scroll.pack(side='right', fill='y')
        
        self.file_listbox = tk.Listbox(list_frame, yscrollcommand=scroll.set, 
                                       font=('Consolas', 9))
        self.file_listbox.pack(fill='both', expand=True)
        scroll.config(command=self.file_listbox.yview)
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(btn_frame, text="📁 Add Files", command=self.add_files,
                 bg='#2196F3', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=10, pady=5).pack(side='left', padx=(0, 5))
        
        tk.Button(btn_frame, text="📂 Add Folder", command=self.add_folder,
                 bg='#2196F3', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=10, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🗑️ Clear List", command=self.clear_list,
                 bg='#9E9E9E', fg='white', font=('Segoe UI', 9),
                 padx=10, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🔼 Move Up", command=self.move_up,
                 bg='#607D8B', fg='white', font=('Segoe UI', 9),
                 padx=10, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🔽 Move Down", command=self.move_down,
                 bg='#607D8B', fg='white', font=('Segoe UI', 9),
                 padx=10, pady=5).pack(side='left', padx=5)
        
        # Convert button
        tk.Button(main_frame, text="📄 Convert to DOCX", command=self.convert,
                 bg='#4CAF50', fg='white', font=('Segoe UI', 12, 'bold'),
                 padx=20, pady=10).pack(fill='x', pady=(10, 0))
        
        # Status
        self.status_label = tk.Label(main_frame, text="Ready", 
                                     font=('Segoe UI', 9), fg='#666')
        self.status_label.pack(pady=(5, 0))
        
        self.image_files = []
        
    def add_files(self):
        """Add individual image files"""
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("JPG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            for file in files:
                if file not in self.image_files:
                    self.image_files.append(file)
            self.update_listbox()
            self.status_label.config(text=f"Added {len(files)} file(s)")
    
    def add_folder(self):
        """Add all images from a folder"""
        folder = filedialog.askdirectory(title="Select Folder with Images")
        
        if folder:
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
            files = []
            
            for file in sorted(os.listdir(folder)):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    ext = os.path.splitext(file)[1].lower()
                    if ext in image_extensions and file_path not in self.image_files:
                        files.append(file_path)
            
            self.image_files.extend(files)
            self.update_listbox()
            self.status_label.config(text=f"Added {len(files)} file(s) from folder")
    
    def clear_list(self):
        """Clear all files from list"""
        if self.image_files and messagebox.askyesno("Clear List", "Remove all files from the list?"):
            self.image_files = []
            self.update_listbox()
            self.status_label.config(text="List cleared")
    
    def move_up(self):
        """Move selected file up in the list"""
        selection = self.file_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        
        idx = selection[0]
        self.image_files[idx], self.image_files[idx-1] = self.image_files[idx-1], self.image_files[idx]
        self.update_listbox()
        self.file_listbox.selection_set(idx-1)
    
    def move_down(self):
        """Move selected file down in the list"""
        selection = self.file_listbox.curselection()
        if not selection or selection[0] >= len(self.image_files) - 1:
            return
        
        idx = selection[0]
        self.image_files[idx], self.image_files[idx+1] = self.image_files[idx+1], self.image_files[idx]
        self.update_listbox()
        self.file_listbox.selection_set(idx+1)
    
    def update_listbox(self):
        """Update the listbox display"""
        self.file_listbox.delete(0, tk.END)
        for i, file in enumerate(self.image_files, 1):
            filename = os.path.basename(file)
            self.file_listbox.insert(tk.END, f"{i:3d}. {filename}")
    
    def convert(self):
        """Convert images to DOCX"""
        if not self.image_files:
            messagebox.showwarning("No Files", "Please add image files first!")
            return
        
        # Ask for output location
        output_file = filedialog.asksaveasfilename(
            title="Save DOCX As",
            defaultextension=".docx",
            filetypes=[("Word Document", "*.docx"), ("All files", "*.*")],
            initialfile="converted_images.docx"
        )
        
        if not output_file:
            return
        
        try:
            self.status_label.config(text="Converting... Please wait...")
            self.root.update()
            
            # Create document
            doc = Document()
            
            # Set narrow margins (0.5 inch) to maximize image space
            sections = doc.sections
            for section in sections:
                section.top_margin = Inches(0.5)
                section.bottom_margin = Inches(0.5)
                section.left_margin = Inches(0.5)
                section.right_margin = Inches(0.5)
            
            # Add each image
            for i, image_path in enumerate(self.image_files, 1):
                self.status_label.config(text=f"Processing image {i}/{len(self.image_files)}...")
                self.root.update()
                
                try:
                    # Get image dimensions
                    with Image.open(image_path) as img:
                        img_width, img_height = img.size
                    
                    # Calculate scaling to fit page
                    # US Letter: 8.5 x 11 inches, minus 1 inch margins = 7.5 x 10 inches usable
                    max_width = 7.5
                    max_height = 10.0
                    
                    # Calculate aspect ratios
                    img_aspect = img_width / img_height
                    page_aspect = max_width / max_height
                    
                    # Scale to fit within page bounds
                    if img_aspect > page_aspect:
                        # Image is wider - constrain by width
                        width = Inches(max_width)
                        height = Inches(max_width / img_aspect)
                    else:
                        # Image is taller - constrain by height
                        height = Inches(max_height)
                        width = Inches(max_height * img_aspect)
                    
                    # Add image to document
                    doc.add_picture(image_path, width=width, height=height)
                    
                    # Add page break after each image except the last
                    if i < len(self.image_files):
                        doc.add_page_break()
                
                except Exception as e:
                    messagebox.showerror("Image Error", 
                                       f"Failed to process image {i}:\n{os.path.basename(image_path)}\n\n{str(e)}")
                    continue
            
            # Save document
            doc.save(output_file)
            
            self.status_label.config(text=f"✓ Converted {len(self.image_files)} images successfully!")
            messagebox.showinfo("Success", 
                              f"Document created successfully!\n\n{len(self.image_files)} images converted\n\nSaved to:\n{output_file}")
            
            # Ask if user wants to open the file
            if messagebox.askyesno("Open File", "Would you like to open the document now?"):
                os.startfile(output_file)
        
        except Exception as e:
            self.status_label.config(text="❌ Conversion failed")
            messagebox.showerror("Error", f"Failed to create document:\n\n{str(e)}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    # Check for required packages
    try:
        import docx
        import PIL
    except ImportError as e:
        print("Missing required package!")
        print("\nPlease install required packages:")
        print("  pip install python-docx Pillow")
        print("\nOr install both at once:")
        print("  pip install python-docx Pillow")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    app = JPGtoDOCXConverter()
    app.run()
