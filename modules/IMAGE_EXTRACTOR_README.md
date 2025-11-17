# 🖼️ Image Extractor (Superimage)

## Overview

The Image Extractor module extracts images from DOCX files and saves them as sequentially numbered PNG files. It's integrated into the Reference Images tab under Translation Resources and also accessible via Tools menu.

## Features

- ✅ **DOCX Support**: Extract images from Microsoft Word documents
- ✅ **Sequential Naming**: Automatically numbers images (Fig. 1.png, Fig. 2.png, etc.)
- ✅ **Custom Prefix**: Configure filename prefix (e.g., "Fig.", "Image", "Photo")
- ✅ **Batch Processing**: Process multiple DOCX files at once
- ✅ **Folder Import**: Add all DOCX files from a folder
- ✅ **Auto-Folder Mode**: Automatically create "Images" subfolder next to each DOCX file
- ✅ **Image Preview**: Built-in image viewer with navigation
- ✅ **PNG Output**: All images converted to PNG format
- ✅ **Format Conversion**: Handles various embedded image formats (JPEG, PNG, BMP, etc.)

## Usage

### Access Methods

**Method 1: Translation Resources Tab**
1. Go to **Translation Resources** → **Reference Images**
2. The Image Extractor interface is ready to use

**Method 2: Tools Menu**
1. Click **Tools** → **Image Extractor (Superimage)**
2. This opens the Translation Resources → Reference Images tab

### Extraction Process

1. **Add DOCX Files**
   - Click **"📄 Add DOCX File"** to select individual files
   - Or click **"📁 Add Folder"** to add all DOCX files from a directory
   - Files appear in the list (duplicates are automatically prevented)

2. **Configure Output**
   - **Auto-Folder Mode** (Optional): Check "📁 Auto: Create 'Images' folder next to DOCX file(s)"
     - When enabled: Images are saved in an "Images" subfolder next to each DOCX file
     - When disabled: All images go to a single output directory you choose
   - **Output Directory**: Click "Browse..." to select where images will be saved (disabled in Auto-Folder mode)
   - **Filename Prefix**: Enter a prefix for the filenames (default: "Fig.")
     - Example with "Fig.": `Fig. 1.png`, `Fig. 2.png`, `Fig. 3.png`
     - Example with "Image": `Image 1.png`, `Image 2.png`, `Image 3.png`

3. **Extract**
   - Click **"🖼️ Extract Images"** button
   - Progress and results appear in the status area
   - A success dialog shows the total count and output location

4. **Results & Preview**
   - All extracted images are saved in the output directory (or auto-created subfolders)
   - Images are numbered sequentially across all processed files
   - Original image quality is preserved
   - **Image Preview**: View extracted images in the built-in preview panel
     - Use ◀ Previous / Next ▶ buttons to navigate through images
     - Images are scaled to fit while maintaining aspect ratio
     - Current image filename and position shown below preview

## Technical Details

### Module Location
- **File**: `modules/image_extractor.py`
- **Class**: `ImageExtractor`

### Supported Formats
- **Input**: `.docx` (Microsoft Word documents)
- **Output**: `.png` (Portable Network Graphics)

### How It Works

1. **DOCX Structure**: DOCX files are ZIP archives containing images in `word/media/` folder
2. **Image Extraction**: Module extracts all images from the media folder
3. **Format Conversion**: Uses PIL/Pillow to convert images to PNG
4. **Color Handling**: Automatically converts RGBA to RGB with white background
5. **Sequential Numbering**: Maintains continuous numbering across multiple files

### Code Example

```python
from modules.image_extractor import ImageExtractor

# Initialize extractor
extractor = ImageExtractor()

# Extract from single file
count, files = extractor.extract_images_from_docx(
    docx_path="document.docx",
    output_dir="extracted_images",
    prefix="Fig."
)

print(f"Extracted {count} images")

# Extract from multiple files
docx_files = ["file1.docx", "file2.docx", "file3.docx"]
total_count, all_files = extractor.extract_from_multiple_docx(
    docx_paths=docx_files,
    output_dir="extracted_images",
    prefix="Image"
)

print(f"Total extracted: {total_count} images")
```

## Dependencies

- **Pillow (PIL)**: For image processing and format conversion
  ```bash
  pip install Pillow
  ```

## Use Cases

### Translation Projects
- Extract diagrams and figures from source documents
- Create visual reference library for translators
- Document image assets for localization projects

### Documentation
- Extract all figures from technical documentation
- Create image galleries from reports
- Archive visual assets from Word documents

### Content Management
- Batch extract images for web publishing
- Create image libraries from document collections
- Migrate visual content to new formats

## Future Enhancements

Potential features for future versions:

- [ ] **Additional Input Formats**: Support PDF, PPTX, XLSX
- [ ] **Image Metadata**: Extract alt text and captions from DOCX
- [ ] **Size Options**: Resize/optimize images during extraction
- [ ] **Format Options**: Support JPEG, WebP output formats
- [x] ~~**Preview**: Show thumbnails of extracted images~~ ✅ **IMPLEMENTED**
- [ ] **Selective Extraction**: Choose specific images to extract
- [ ] **OCR Integration**: Extract text from images
- [ ] **Cloud Storage**: Direct upload to cloud services
- [ ] **Zoom Controls**: Zoom in/out on preview images
- [ ] **Export Preview List**: Save list of extracted images as text file

## Troubleshooting

### No Images Extracted
- **Check**: Does the DOCX file actually contain images?
- **Verify**: Are images embedded (not linked externally)?
- **Test**: Open the DOCX in Word to confirm images are present

### Error: "File must be a DOCX document"
- **Issue**: File extension is not .docx
- **Solution**: Only DOCX format is supported (not DOC, RTF, etc.)

### Error: "DOCX file not found"
- **Issue**: File path is incorrect or file was moved
- **Solution**: Re-add the file to the list

### Permission Errors
- **Issue**: No write permission for output directory
- **Solution**: Choose a different output directory or adjust permissions

## License

Part of the Supervertaler translation productivity suite.

## Version History

- **v1.1** (2025-11-17): Feature enhancement
  - Added Auto-Folder mode (create "Images" subfolder next to DOCX)
  - Added built-in image preview with navigation
  - Improved UI layout with split view (results + preview)

- **v1.0** (2025-11-17): Initial release
  - DOCX image extraction
  - Sequential PNG output
  - Batch processing
  - Integration with Translation Resources

---

**Related Modules**: Translation Resources, Reference Materials, PDF Rescue
