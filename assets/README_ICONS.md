# Icon Generation Guide

## Problem: Pixelated Icons

The original `icon.ico` was only 836 bytes with a single low resolution, causing pixelation in:
- Windows Start Menu
- Taskbar
- Application window title bar
- Desktop shortcuts

## Solution: Multi-Resolution .ico File

Windows .ico files should contain multiple resolutions for crisp display:
- **16x16** - Small icons, file explorer details view
- **32x32** - Standard icons, file explorer list view
- **48x48** - Large icons, file explorer thumbnail view
- **256x256** - High-DPI displays, Windows 10/11 Start Menu tiles

## How to Generate a New Icon

### Step 1: Install Dependencies

```bash
pip install Pillow cairosvg
```

### Step 2: Choose Your SVG Source

Available SVG files in this folder:
- `icon_sv_website.svg` - Current website icon (blue gradient circle with "Sv")
- `icon_sv_simple.svg` - Simplified version
- `icon_sv_modern.svg` - Modern variant
- `icon_sv_modern_paths.svg` - Modern variant with paths

### Step 3: Run the Generator

```bash
python create_icon_from_svg.py
```

This will:
1. Convert the SVG to PNG at sizes: 16x16, 32x32, 48x48, 256x256
2. Combine all PNGs into a single `icon.ico` file
3. Replace the old icon.ico in the assets folder

### Step 4: Rebuild the Windows EXE

```bash
.\build_windows_release.ps1
```

The new multi-resolution icon will be embedded in `Supervertaler.exe` via the PyInstaller spec file.

## Customizing

To use a different SVG or different sizes, edit `create_icon_from_svg.py`:

```python
# Change the source SVG
svg_path = assets_dir / 'icon_sv_modern.svg'

# Change the output sizes
sizes = [16, 24, 32, 48, 64, 128, 256]
```

## Technical Details

- **Format**: Windows ICO (multi-resolution)
- **Tool**: cairosvg for SVG→PNG, Pillow for PNG→ICO
- **Expected Size**: ~15-30 KB for multi-resolution .ico
- **Original Size**: 836 bytes (single resolution, pixelated)

## Alternatives

If you don't want to install cairosvg, you can:
1. Use an online converter (e.g., CloudConvert, RealFaviconGenerator)
2. Use GIMP: Open SVG → Export as .ico → Select multiple sizes
3. Use ImageMagick: `convert icon.svg -resize 256x256 -define icon:auto-resize="256,128,64,48,32,16" icon.ico`
