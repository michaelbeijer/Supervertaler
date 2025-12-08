# Icon Conversion Guide for Supervertaler

We're using **Option 8 (Sv Modern Circle)** as the official icon!

## Quick Conversion (Recommended)

### For Windows (.ico):

1. Go to **https://cloudconvert.com/svg-to-ico**
2. Upload `icon_sv_modern.svg`
3. Click "Options" and select these sizes:
   - ☑ 16x16
   - ☑ 24x24
   - ☑ 32x32
   - ☑ 48x48
   - ☑ 64x64
   - ☑ 128x128
   - ☑ 256x256
4. Convert and download as `icon.ico`
5. Place in `assets/` folder

### For Website Favicon:

1. Go to **https://realfavicongenerator.net/**
2. Upload `icon_sv_modern.svg`
3. Generate all formats (it creates perfect sizes for all browsers)
4. Download the package
5. Copy `favicon.ico` to `docs/` folder
6. Copy other generated files (apple-touch-icon.png, etc.) to `docs/` folder

### For macOS (.icns):

**Option A - Online:**
1. Go to **https://cloudconvert.com/svg-to-icns**
2. Upload `icon_sv_modern.svg`
3. Convert and download

**Option B - macOS Terminal:**
```bash
# 1. Create iconset folder
mkdir icon.iconset

# 2. Convert SVG to PNGs at different sizes (use online converter)
# Upload icon_sv_modern.svg to https://ezgif.com/svg-to-png
# Download these sizes into icon.iconset/:
# - icon_16x16.png
# - icon_16x16@2x.png (32x32)
# - icon_32x32.png
# - icon_32x32@2x.png (64x64)
# - icon_128x128.png
# - icon_128x128@2x.png (256x256)
# - icon_256x256.png
# - icon_256x256@2x.png (512x512)
# - icon_512x512.png
# - icon_512x512@2x.png (1024x1024)

# 3. Convert to .icns
iconutil -c icns icon.iconset

# 4. Place icon.icns in assets/ folder
```

## Sizes Reference

### Windows Application Icon (.ico)
- 16×16 - Window title bar, taskbar (small)
- 24×24 - Taskbar
- 32×32 - Taskbar, File Explorer
- 48×48 - File Explorer, Alt+Tab
- 64×64 - File Explorer (large icons)
- 128×128 - Shortcuts, Explorer (extra large)
- 256×256 - High DPI displays

### Website Icons
- **favicon.ico**: 16×16, 32×32, 48×48
- **apple-touch-icon.png**: 180×180 (iOS home screen)
- **icon-192.png**: 192×192 (Android)
- **icon-512.png**: 512×512 (Android splash, PWA)

### macOS Application Icon (.icns)
- 16×16, 32×32, 64×64, 128×128, 256×256, 512×512, 1024×1024
- Each size should have @2x retina variant

## Current Status

✅ **Created:** icon_sv_modern.svg (source file)
⏳ **Needed:**
  - [ ] icon.ico (Windows)
  - [ ] favicon.ico (Website)
  - [ ] icon.icns (macOS - optional for now)
  - [ ] apple-touch-icon.png (Website - iOS)

## Once You Have icon.ico

The icon will be automatically integrated into PyQt6 in the next step!
