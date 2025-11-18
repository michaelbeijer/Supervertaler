# Image Context Feature - Integration Summary

**Date:** November 18, 2025  
**Feature:** Multimodal AI Translation with Figure Context  
**Status:** ✅ Phase 1 Complete - UI & Module Integration

## Overview

The **Image Context** feature enables multimodal AI translation by automatically including figure images when translating technical text that references them. When a translator is working on a document with statements like "As shown in Figure 1, the drive shaft (17) connects to bearing (18)", the AI can "see" the actual technical drawing and provide more accurate translations of part references.

## What's Implemented (v1.6.3)

### ✅ UI Integration
- **Tab renamed:** "Reference Images" → "🎯 Image Context"
- **New section:** "Image Context - Load Images for AI Translation"
- **Load button:** Browse and load folder containing figure images
- **Clear button:** Remove all loaded images
- **Status display:** Shows count of loaded images and folder name
- **Help text:** Explains how figures are automatically matched

### ✅ Backend Integration
- **FigureContextManager initialized:** `self.figure_context` available globally
- **Module fully functional:**
  - `detect_figure_references(text)` - Finds "Figure 1", "fig 2A", etc.
  - `load_from_folder(path)` - Loads .png, .jpg, .jpeg, .gif, .bmp, .tiff
  - `get_images_for_text(text)` - Returns relevant images for translation
  - `normalize_figure_ref()` - Matches various naming formats
  - `pil_image_to_base64_png()` - Converts for Claude/OpenAI APIs

### ✅ Callback Methods
- `_on_load_image_context_folder()` - Folder browse dialog
- `_on_clear_image_context()` - Clear loaded images with confirmation

## Filename Matching Examples

The system automatically normalizes figure references to match various filename formats:

| Text Reference | Matches Filename |
|----------------|------------------|
| "Figure 1" | fig1.png, Figure 1.jpg, Fig.1.png |
| "see fig 2A" | fig2a.png, Figure 2A.jpg, Fig. 2-A.png |
| "Figuur 3B" | fig3b.png, Figure3B.jpg, figuur 3b.png |

## How It Works

1. **User loads images:** Click "📁 Load Images Folder" and select folder with figures
2. **System normalizes names:** "Figure 1.png" → ref '1', "fig2a.jpg" → ref '2a'
3. **Translation detects figures:** Text "As shown in Figure 1..." triggers detection
4. **AI receives image:** Image automatically included in GPT-4V/Claude/Gemini request
5. **Better translation:** AI "sees" the technical drawing and translates accurately

## Next Steps (Phase 2 - TODO)

### 🔄 Integration with AI Translation

To complete the feature, images need to be automatically included in AI translation requests:

**Files to modify:**
- `modules/llm_clients.py` - Add image support to API calls
- `Supervertaler.py` - Detect figures in source text before translation

**Implementation approach:**

```python
# In translate_with_ai() or similar method:
def translate_segment_with_ai(self, segment_id, provider, model):
    segment = self.current_project.segments[segment_id]
    source_text = segment.source
    
    # NEW: Detect figure references and get images
    figure_images = []
    if self.figure_context.has_images():
        figure_refs = self.figure_context.detect_figure_references(source_text)
        if figure_refs:
            figure_images = self.figure_context.get_images_for_text(source_text)
            self.log(f"[Image Context] Including {len(figure_images)} figure(s) with translation")
    
    # Pass images to LLM client
    translation = llm_client.translate(
        source_text,
        source_lang,
        target_lang,
        images=figure_images  # NEW parameter
    )
```

**LLM Client modifications needed:**

```python
# In llm_clients.py - OpenAI example:
def translate(self, source_text, source_lang, target_lang, images=None):
    messages = [...]
    
    if images:
        # Convert to base64 and add to message
        for ref, pil_image in images:
            base64_image = pil_image_to_base64_png(pil_image)
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Context image for {ref}:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            })
```

### 📊 Testing Requirements

1. **Test with patent documents** - Complex figure references
2. **Test filename matching** - Various naming conventions
3. **Test multiple figures** - "see Figures 1 and 2"
4. **Test performance** - Image encoding overhead
5. **Test API limits** - Image size restrictions per provider

### 📝 Documentation Needed

- [ ] User guide for Image Context feature
- [ ] Example workflow with patent document
- [ ] API provider compatibility matrix (GPT-4V, Claude 3, Gemini Pro Vision)
- [ ] Best practices for image naming and organization

## Technical Details

### Supported Image Formats
- PNG, JPG, JPEG, GIF, BMP, TIFF

### Figure Reference Patterns Detected
- `Figure X`, `figure X`, `FIGURE X`
- `Fig X`, `fig X`, `Fig. X`
- `Figuur X` (Dutch)
- With sub-references: `Figure 1A`, `fig 2-B`, `Figure 3.5`

### API Compatibility
- ✅ **OpenAI GPT-4V** - Supports vision (image_url format)
- ✅ **Claude 3 (Opus/Sonnet)** - Supports vision (base64 format)
- ✅ **Google Gemini Pro Vision** - Supports vision (PIL.Image directly)
- ❌ **Standard GPT-3.5/GPT-4** - No vision support
- ❌ **Google Translate MT** - No vision support

## Legacy Implementation Reference

This feature was previously implemented in:
- `legacy_versions/Supervertaler_v2.5.0-CLASSIC.py` (lines 1360-1750, 1800-1870, 1940-2100)
- `legacy_versions/Supervertaler_tkinter.py` (uses FigureContextManager)

Key code from legacy version showing figure detection:

```python
# Detect figure references in source text
fig_refs = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", 
                      source_text, re.IGNORECASE)

if PIL_AVAILABLE and fig_refs and drawings_images_map:
    for ref in fig_refs:
        norm = normalize_figure_ref(f"fig {ref}")
        if norm and norm in drawings_images_map:
            # Add image to prompt
            prompt_parts.append(f"\n--- Context Image: Figure {ref} ---")
            prompt_parts.append(drawings_images_map[norm])  # PIL.Image object
```

## Benefits

### For Patent Translators
- **Accurate part numbering:** AI sees the reference numbers in drawings
- **Correct spatial relationships:** "above", "below", "connected to" based on actual layout
- **Technical terminology:** Context from visual elements
- **Quality consistency:** Same accuracy as human translator seeing the figure

### For Technical Documentation
- **Assembly instructions:** Step-by-step with visual context
- **Maintenance manuals:** Part identification from diagrams
- **User guides:** UI element references with screenshots

### For All Users
- **Faster translation:** No need to manually check figures
- **Better quality:** AI understands visual context
- **Fewer errors:** Reduced mistakes in part references
- **Professional results:** CAT-tool-level integration

## File Structure

```
modules/
  └── figure_context_manager.py  # Core module (340 lines)
      ├── FigureContextManager class
      ├── normalize_figure_ref()
      └── pil_image_to_base64_png()

Supervertaler.py
  ├── Line 1896: FigureContextManager initialization
  ├── Line 2695: create_reference_images_tab() - UI creation
  ├── Line 3236: _on_load_image_context_folder() - Load images
  ├── Line 3277: _on_clear_image_context() - Clear images
  └── Line 3649: Tab registration "🎯 Image Context"
```

## Version History

- **v1.6.3 (Nov 18, 2025):** Phase 1 - UI integration complete
- **v2.5.0-CLASSIC:** Original implementation with full AI integration
- **v3.7.x (tkinter):** FigureContextManager module created

---

**Next milestone:** Phase 2 - Complete AI translation integration with automatic image inclusion
