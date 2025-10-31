# Standardized Tab Header Pattern

## Overview
This document defines the standardized pattern for tab headers in Supervertaler. All tabs use a consistent style matching Universal Lookup and AutoFingers.

## Standard Tab Header Pattern

### Style Specification

**Header (Title)**
- Font: 16pt, bold
- Color: `#1976D2` (blue)
- Emoji prefix (see list below)

**Description Box**
- Background: `#E3F2FD` (light blue)
- Text color: `#666` (medium gray)
- Padding: 5px
- Border radius: 3px
- Word wrap: enabled
- 1-2 lines of concise description

**Layout**
- Container margins: `(10, 10, 10, 10)`
- Spacing: `5` (tighter spacing between header, description, and content)
- **Stretch factors**: Use `0` for header/description (stays compact), `1` for main content (expands to fill space)

### Responsive Design (Important!)

To ensure the layout works well on both large and small screens, use **stretch factors** when adding widgets:

```python
# Header and description: stretch factor 0 (stays compact)
main_layout.addWidget(header, 0)
main_layout.addWidget(description, 0)

# Main content (splitter/editor): stretch factor 1 (expands to fill space)
main_layout.addWidget(splitter, 1)

# Bottom widgets: stretch factor 0 (stays compact)
main_layout.addLayout(action_layout, 0)
main_layout.addWidget(status_label, 0)
main_layout.addWidget(progress_bar, 0)
```

This ensures:
- Header stays at the top with minimal space
- Main content expands to use available screen space
- Works well on both small and large monitors

### Implementation Pattern

#### For Standalone Modules (like PDF Rescue)

In the module file (e.g., `modules/pdf_rescue_Qt.py`):

```python
def create_tab(self, parent):
    """Create the module UI"""
    # Main layout
    main_layout = QVBoxLayout(parent)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(5)  # Tighter spacing
    
    # Header (matches Universal Lookup / AutoFingers style)
    header = QLabel("🔍 Module Name")
    header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
    main_layout.addWidget(header, 0)  # 0 = no stretch, stays compact
    
    # Description box (matches Universal Lookup / AutoFingers style)
    description = QLabel(
        "Brief description of what this module does.\n"
        "Second line with additional info if needed."
    )
    description.setWordWrap(True)
    description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
    main_layout.addWidget(description, 0)  # 0 = no stretch, stays compact
    
    # ... rest of your UI (main content) ...
    main_layout.addWidget(main_content_widget, 1)  # 1 = stretch, expands to fill space
```

#### For Non-Standalone Tabs (like TMX Editor)

In Supervertaler_Qt.py:

```python
def create_your_tab(self) -> QWidget:
    """Create Your Tab"""
    from modules.your_module import YourModule
    
    # Create container widget with standardized header
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(5)  # Tighter spacing
    
    # Header (matches Universal Lookup / AutoFingers / PDF Rescue style)
    header = QLabel("📝 Module Name")
    header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
    layout.addWidget(header, 0)  # 0 = no stretch
    
    # Description box
    description = QLabel(
        "Brief description of what this module does.\n"
        "Second line with additional info if needed."
    )
    description.setWordWrap(True)
    description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
    layout.addWidget(description, 0)  # 0 = no stretch
    
    # Create and add the actual module widget
    module_widget = YourModule(parent=None)
    layout.addWidget(module_widget, 1)  # 1 = stretch to fill space
    
    return container
```

## Emoji Icons (Use one per tab)

- 🔍 **Universal Lookup** - Search/lookup functionality
- 🔍 **PDF Rescue** - PDF/OCR extraction
- 📝 **TMX Editor** - Editing/writing
- 🤖 **AutoFingers** - Automation
- 🏠 **Project Home** - Home/dashboard
- 📚 **Termbases** - Terminology management
- 🚫 **Non-Translatables** - Exclusions/blocking
- 💬 **Prompt Manager** - AI prompts
- 📄 **TMX Editor** - File editing
- 🖼️ **Reference Images** - Visual resources
- 🔧 **Encoding Repair** - Technical fixes
- 📊 **Encoding Result** - Results/output
- 🔄 **Tracked Changes** - Version control
- ⚙️ **Settings** - Configuration
- 🔖 **Mag** - Magazine/collections

## Complete Examples

### Example 1: Universal Lookup Tab
```python
# Header
header = QLabel("🔍 Universal Lookup")
header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
layout.addWidget(header)

# Description
description = QLabel(
    "Look up translations anywhere on your computer.\n"
    "Press Ctrl+Alt+L or paste text manually to search your translation memory."
)
description.setWordWrap(True)
description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
layout.addWidget(description)
```

### Example 2: PDF Rescue Tab
```python
# Header
header = QLabel("🔍 PDF Rescue")
header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
main_layout.addWidget(header)

# Description
description = QLabel(
    "Extract text from poorly formatted PDFs using AI Vision (GPT-4 Vision API).\n"
    "Upload PDF files or images to extract clean, editable text."
)
description.setWordWrap(True)
description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
main_layout.addWidget(description)
```

### Example 3: TMX Editor Tab
```python
# Header
header = QLabel("📝 TMX Editor")
header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
layout.addWidget(header)

# Description
description = QLabel(
    "Edit translation memory files directly - inspired by Heartsome TMX Editor.\n"
    "Open, edit, filter, and manage your TMX translation memories."
)
description.setWordWrap(True)
description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
layout.addWidget(description)
```

## Current Implementation Status

✅ **Universal Lookup** - Fully standardized with blue header and stretch factors  
✅ **AutoFingers** - Fully standardized with blue header and stretch factors  
✅ **PDF Rescue** - Fully standardized with blue header and stretch factors  
✅ **TMX Editor** - Fully standardized with blue header and stretch factors  
🔲 **Other tabs** - Update as needed when created

## Benefits

1. **Visual Consistency** - All tabs look unified and professional
2. **User Recognition** - Users instantly recognize the pattern
3. **Easy Maintenance** - Simple to update all headers at once
4. **Scalability** - Easy pattern to follow for new tabs
5. **Accessibility** - Clear hierarchy and readable text

## Migration Checklist

When updating existing tabs to this pattern:
- [ ] Change layout margins to `(10, 10, 10, 10)`
- [ ] Change layout spacing to `10`
- [ ] Add 16pt bold blue header with emoji
- [ ] Add light blue description box with word wrap
- [ ] Remove old banner/frame-style headers
- [ ] Test on multiple monitor sizes
- [ ] Verify both embedded and standalone modes (if applicable)
