"""
═══════════════════════════════════════════════════════════════════════════════
Image Extractor Module for Supervertaler
═══════════════════════════════════════════════════════════════════════════════

Purpose:
    Extract images from DOCX files and save them as sequentially numbered PNG files.
    Integrated into the Reference Images tab under Translation Resources.

Features:
    - Extract all images from DOCX documents
    - Save as PNG files with sequential naming (Fig. 1.png, Fig. 2.png, etc.)
    - Support for various image formats embedded in DOCX
    - Progress feedback during extraction
    - Can be used as standalone tool or within Translation Resources workflow

Author: Supervertaler Development Team
Created: 2025-11-17
Last Modified: 2025-11-17

═══════════════════════════════════════════════════════════════════════════════
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional
from zipfile import ZipFile
from io import BytesIO
from PIL import Image


class ImageExtractor:
    """Extract images from DOCX files and save as PNG"""
    
    def __init__(self):
        self.supported_formats = ['.docx']
    
    def extract_images_from_docx(self, docx_path: str, output_dir: str, 
                                 prefix: str = "Fig.") -> Tuple[int, List[str]]:
        """
        Extract all images from a DOCX file and save as PNG files.
        
        Args:
            docx_path: Path to the DOCX file
            output_dir: Directory where images will be saved
            prefix: Prefix for output filenames (default: "Fig.")
            
        Returns:
            Tuple of (number of images extracted, list of output file paths)
        """
        # Validate input
        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"DOCX file not found: {docx_path}")
        
        if not docx_path.lower().endswith('.docx'):
            raise ValueError("File must be a DOCX document")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        extracted_files = []
        image_count = 0
        
        try:
            # DOCX files are ZIP archives
            with ZipFile(docx_path, 'r') as zip_ref:
                # Images are typically in word/media/ folder
                image_files = [f for f in zip_ref.namelist() 
                             if f.startswith('word/media/')]
                
                for img_file in image_files:
                    image_count += 1
                    
                    # Read image data
                    img_data = zip_ref.read(img_file)
                    
                    # Open with PIL to convert to PNG
                    try:
                        img = Image.open(BytesIO(img_data))
                        
                        # Convert RGBA to RGB if necessary (for JPEG compatibility)
                        if img.mode in ('RGBA', 'LA', 'P'):
                            # Create white background
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                            img = background
                        elif img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Generate output filename
                        output_filename = f"{prefix} {image_count}.png"
                        output_path = os.path.join(output_dir, output_filename)
                        
                        # Save as PNG
                        img.save(output_path, 'PNG', optimize=True)
                        extracted_files.append(output_path)
                        
                    except Exception as e:
                        print(f"Warning: Could not process image {img_file}: {e}")
                        continue
        
        except Exception as e:
            raise Exception(f"Error extracting images: {e}")
        
        return image_count, extracted_files
    
    def extract_from_multiple_docx(self, docx_paths: List[str], output_dir: str,
                                   prefix: str = "Fig.") -> Tuple[int, List[str]]:
        """
        Extract images from multiple DOCX files.
        
        Args:
            docx_paths: List of paths to DOCX files
            output_dir: Directory where images will be saved
            prefix: Prefix for output filenames (default: "Fig.")
            
        Returns:
            Tuple of (total number of images extracted, list of output file paths)
        """
        all_extracted_files = []
        total_count = 0
        current_number = 1
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        for docx_path in docx_paths:
            try:
                # Extract images with sequential numbering across all files
                with ZipFile(docx_path, 'r') as zip_ref:
                    image_files = [f for f in zip_ref.namelist() 
                                 if f.startswith('word/media/')]
                    
                    for img_file in image_files:
                        img_data = zip_ref.read(img_file)
                        
                        try:
                            img = Image.open(BytesIO(img_data))
                            
                            # Convert to RGB
                            if img.mode in ('RGBA', 'LA', 'P'):
                                background = Image.new('RGB', img.size, (255, 255, 255))
                                if img.mode == 'P':
                                    img = img.convert('RGBA')
                                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                                img = background
                            elif img.mode != 'RGB':
                                img = img.convert('RGB')
                            
                            # Generate output filename with sequential numbering
                            output_filename = f"{prefix} {current_number}.png"
                            output_path = os.path.join(output_dir, output_filename)
                            
                            # Save as PNG
                            img.save(output_path, 'PNG', optimize=True)
                            all_extracted_files.append(output_path)
                            
                            current_number += 1
                            total_count += 1
                            
                        except Exception as e:
                            print(f"Warning: Could not process image from {docx_path}: {e}")
                            continue
            
            except Exception as e:
                print(f"Warning: Could not process file {docx_path}: {e}")
                continue
        
        return total_count, all_extracted_files


# Standalone usage example
if __name__ == "__main__":
    extractor = ImageExtractor()
    
    # Example usage
    docx_file = "example.docx"
    output_directory = "extracted_images"
    
    if os.path.exists(docx_file):
        count, files = extractor.extract_images_from_docx(docx_file, output_directory)
        print(f"Extracted {count} images:")
        for f in files:
            print(f"  - {f}")
    else:
        print(f"File not found: {docx_file}")
