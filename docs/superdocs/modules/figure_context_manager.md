# figure_context_manager

**File:** `modules/figure_context_manager.py`
**Lines:** 340
**Classes:** 1
**Functions:** 2

---

## Module Description

Figure Context Manager
Handles loading, displaying, and providing visual context for technical translations.

This module manages figure images that can be automatically included with translation
requests when the source text references figures (e.g., "Figure 1A", "see fig 2").

Author: Michael Beijer + AI Assistant
Date: October 13, 2025

---

## Classes

### `FigureContextManager`

**Line:** 27

Manages figure context images for multimodal AI translation.

#### Methods

##### `detect_figure_references()`

Detect figure references in text and return normalized list.

Examples:
    "As shown in Figure 1A" -> ['1a']
    "See Figures 2 and 3B" -> ['2', '3b']
    "refer to fig. 4" -> ['4']

Args:
    text: Source text to scan for figure references
    
Returns:
    List of normalized figure references (lowercase, no spaces)

##### `load_from_folder()`

Load all figure images from a folder.

Supported formats: .png, .jpg, .jpeg, .gif, .bmp, .tiff

Filename examples:
    - "Figure 1.png" -> ref '1'
    - "Figure 2A.jpg" -> ref '2a'
    - "fig3b.png" -> ref '3b'

Args:
    folder_path: Path to folder containing figure images
    
Returns:
    Number of successfully loaded images
    
Raises:
    Exception: If folder doesn't exist or PIL is not available

##### `clear()`

Clear all loaded figure context images.

##### `get_images_for_text()`

Get figure images relevant to the given text.

Args:
    text: Source text that may contain figure references
    
Returns:
    List of tuples (ref, PIL.Image) for detected and available figures

##### `has_images()`

Check if any images are loaded.

##### `get_image_count()`

Get the number of loaded images.

##### `get_folder_name()`

Get the basename of the loaded folder, or None.

##### `update_ui_display()`

Update UI elements to reflect current figure context state.

Args:
    image_folder_label: tk.Label widget for main Images tab
    image_folder_var: tk.StringVar for Context notebook
    thumbnails_frame: tk.Frame for displaying thumbnails
    figure_canvas: tk.Canvas for scrollable thumbnail area

##### `save_state()`

Save current state for project persistence.

Returns:
    Dictionary with folder_path and image_count

##### `restore_state()`

Restore state from saved project data.

Args:
    state: Dictionary with figure context state
    
Returns:
    True if images were successfully loaded, False otherwise


---

## Functions

### `normalize_figure_ref()`

**Line:** 294

Normalize a figure reference to a standard format.

Examples:
    "Figure 1" -> "1"
    "fig. 2A" -> "2a"
    "Figure3-B.png" -> "3b"

Args:
    text: Text containing figure reference or filename
    
Returns:
    Normalized reference (lowercase, alphanumeric only) or None

---

### `pil_image_to_base64_png()`

**Line:** 327

Convert PIL Image to base64-encoded PNG string.

Args:
    img: PIL.Image object
    
Returns:
    Base64-encoded PNG data string

---

