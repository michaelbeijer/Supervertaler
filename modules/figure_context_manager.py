"""
Figure Context Manager
Handles loading, displaying, and providing visual context for technical translations.

This module manages figure images that can be automatically included with translation
requests when the source text references figures (e.g., "Figure 1A", "see fig 2").

Author: Michael Beijer + AI Assistant
Date: October 13, 2025
"""

from typing import Dict, List, Tuple, Any, Optional
import os
import re
import base64
import io

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None
    ImageTk = None


class FigureContextManager:
    """Manages figure context images for multimodal AI translation."""
    
    def __init__(self, app):
        """
        Initialize the Figure Context Manager.
        
        Args:
            app: Reference to main application (for logging and UI updates)
        """
        self.app = app
        self.figure_context_map: Dict[str, Any] = {}  # ref -> PIL Image
        self.figure_context_folder: Optional[str] = None
        self._photo_references = []  # Store PhotoImage references to prevent GC
        
    def detect_figure_references(self, text: str) -> List[str]:
        """
        Detect figure references in text and return normalized list.
        
        Examples:
            "As shown in Figure 1A" -> ['1a']
            "See Figures 2 and 3B" -> ['2', '3b']
            "refer to fig. 4" -> ['4']
        
        Args:
            text: Source text to scan for figure references
            
        Returns:
            List of normalized figure references (lowercase, no spaces)
        """
        if not text:
            return []
        
        # Pattern matches: figure/figuur/fig + optional period + space + identifier
        pattern = r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)"
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        normalized_refs = []
        for match in matches:
            normalized = normalize_figure_ref(f"fig {match}")
            if normalized and normalized not in normalized_refs:
                normalized_refs.append(normalized)
        
        return normalized_refs
    
    def load_from_folder(self, folder_path: str) -> int:
        """
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
        """
        if not PIL_AVAILABLE:
            raise Exception("PIL/Pillow library is not installed")
        
        if not os.path.exists(folder_path):
            raise Exception(f"Folder not found: {folder_path}")
        
        self.figure_context_folder = folder_path
        self.figure_context_map.clear()
        
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
        loaded_count = 0
        
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(image_extensions):
                img_path = os.path.join(folder_path, filename)
                try:
                    img = Image.open(img_path)
                    # Normalize the filename to match figure references
                    normalized_name = normalize_figure_ref(filename)
                    if normalized_name:
                        self.figure_context_map[normalized_name] = img
                        loaded_count += 1
                        if hasattr(self.app, 'log'):
                            self.app.log(f"[Figure Context] Loaded: {filename} as '{normalized_name}'")
                except Exception as e:
                    if hasattr(self.app, 'log'):
                        self.app.log(f"[Figure Context] Failed to load {filename}: {e}")
        
        return loaded_count
    
    def clear(self):
        """Clear all loaded figure context images."""
        self.figure_context_map.clear()
        self.figure_context_folder = None
        self._photo_references.clear()
    
    def get_images_for_text(self, text: str) -> List[Tuple[str, Any]]:
        """
        Get figure images relevant to the given text.
        
        Args:
            text: Source text that may contain figure references
            
        Returns:
            List of tuples (ref, PIL.Image) for detected and available figures
        """
        figure_refs = self.detect_figure_references(text)
        figure_images = []
        
        for ref in figure_refs:
            if ref in self.figure_context_map:
                figure_images.append((ref, self.figure_context_map[ref]))
        
        return figure_images
    
    def has_images(self) -> bool:
        """Check if any images are loaded."""
        return len(self.figure_context_map) > 0
    
    def get_image_count(self) -> int:
        """Get the number of loaded images."""
        return len(self.figure_context_map)
    
    def get_folder_name(self) -> Optional[str]:
        """Get the basename of the loaded folder, or None."""
        if self.figure_context_folder:
            return os.path.basename(self.figure_context_folder)
        return None
    
    def update_ui_display(self, image_folder_label=None, image_folder_var=None, 
                         thumbnails_frame=None, figure_canvas=None):
        """
        Update UI elements to reflect current figure context state.
        
        Args:
            image_folder_label: tk.Label widget for main Images tab
            image_folder_var: tk.StringVar for Context notebook
            thumbnails_frame: tk.Frame for displaying thumbnails
            figure_canvas: tk.Canvas for scrollable thumbnail area
        """
        # Update folder label
        if image_folder_label:
            if self.has_images():
                count = self.get_image_count()
                folder_name = self.get_folder_name() or "Unknown"
                image_folder_label.config(
                    text=f"✓ {count} image{'s' if count != 1 else ''} loaded from: {folder_name}",
                    fg='#4CAF50'
                )
            else:
                image_folder_label.config(
                    text="No figure context loaded",
                    fg='#999'
                )
        
        # Update image_folder_var for Context notebook
        if image_folder_var:
            if self.has_images():
                count = self.get_image_count()
                folder_name = self.get_folder_name() or "Unknown"
                image_folder_var.set(f"✓ {count} figure{'s' if count != 1 else ''} loaded from: {folder_name}")
            else:
                image_folder_var.set("No figure context loaded")
        
        # Update thumbnails display
        if thumbnails_frame:
            self._update_thumbnails(thumbnails_frame)
    
    def _update_thumbnails(self, thumbnails_frame):
        """
        Update the thumbnail display in the Images tab.
        
        Args:
            thumbnails_frame: tk.Frame to populate with thumbnails
        """
        import tkinter as tk
        
        # Clear existing thumbnails
        for widget in thumbnails_frame.winfo_children():
            widget.destroy()
        
        # Clear photo references
        self._photo_references.clear()
        
        if self.has_images() and PIL_AVAILABLE:
            # Display thumbnails
            for ref, img in sorted(self.figure_context_map.items()):
                # Create frame for each thumbnail
                thumb_frame = tk.Frame(thumbnails_frame, bg='white', relief='solid', borderwidth=1)
                thumb_frame.pack(fill='x', padx=5, pady=5)
                
                # Figure name label
                tk.Label(thumb_frame, text=f"Figure {ref.upper()}", 
                        font=('Segoe UI', 9, 'bold'), bg='white').pack(anchor='w', padx=5, pady=2)
                
                try:
                    # Create thumbnail (max 200px wide)
                    img_copy = img.copy()
                    img_copy.thumbnail((200, 200), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img_copy)
                    
                    # Store reference to prevent garbage collection
                    self._photo_references.append(photo)
                    
                    # Display thumbnail
                    img_label = tk.Label(thumb_frame, image=photo, bg='white')
                    img_label.pack(padx=5, pady=5)
                    
                    # Image info
                    info_text = f"{img.width} × {img.height} px"
                    tk.Label(thumb_frame, text=info_text, 
                            font=('Segoe UI', 8), fg='#999', bg='white').pack(anchor='w', padx=5, pady=2)
                    
                except Exception as e:
                    tk.Label(thumb_frame, text=f"Error displaying: {e}", 
                            font=('Segoe UI', 8), fg='red', bg='white').pack(padx=5, pady=2)
        else:
            # No images loaded - show placeholder
            tk.Label(thumbnails_frame, 
                    text="No images loaded\n\nUse 'Load figure context...' to add visual context for technical translations.",
                    font=('Segoe UI', 9), fg='#999', bg='white', 
                    justify='center').pack(expand=True, pady=20)
    
    def save_state(self) -> Dict[str, Any]:
        """
        Save current state for project persistence.
        
        Returns:
            Dictionary with folder_path and image_count
        """
        return {
            'folder_path': self.figure_context_folder,
            'image_count': self.get_image_count()
        }
    
    def restore_state(self, state: Dict[str, Any]) -> bool:
        """
        Restore state from saved project data.
        
        Args:
            state: Dictionary with figure context state
            
        Returns:
            True if images were successfully loaded, False otherwise
        """
        folder_path = state.get('folder_path')
        if folder_path and os.path.exists(folder_path):
            try:
                loaded_count = self.load_from_folder(folder_path)
                if loaded_count > 0:
                    if hasattr(self.app, 'log'):
                        self.app.log(f"✓ Loaded figure context: {loaded_count} images from {os.path.basename(folder_path)}")
                    return True
            except Exception as e:
                if hasattr(self.app, 'log'):
                    self.app.log(f"⚠ Failed to restore figure context: {e}")
        return False


# === Helper Functions ===

def normalize_figure_ref(text: str) -> Optional[str]:
    """
    Normalize a figure reference to a standard format.
    
    Examples:
        "Figure 1" -> "1"
        "fig. 2A" -> "2a"
        "Figure3-B.png" -> "3b"
    
    Args:
        text: Text containing figure reference or filename
        
    Returns:
        Normalized reference (lowercase, alphanumeric only) or None
    """
    if not text:
        return None
    
    # Remove common prefixes and file extensions
    text = text.lower()
    text = re.sub(r'\.(png|jpg|jpeg|gif|bmp|tiff)$', '', text)
    
    # Extract figure reference (letters and numbers)
    match = re.search(r'(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)', text, re.IGNORECASE)
    if match:
        ref = match.group(1)
        # Remove spaces, dots, dashes
        ref = re.sub(r'[\s\.\-]', '', ref)
        return ref.lower()
    
    return None


def pil_image_to_base64_png(img: Any) -> str:
    """
    Convert PIL Image to base64-encoded PNG string.
    
    Args:
        img: PIL.Image object
        
    Returns:
        Base64-encoded PNG data string
    """
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')
