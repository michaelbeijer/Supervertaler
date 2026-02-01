#!/usr/bin/env python3
"""
Create multi-resolution Windows .ico file using Pillow only (no Cairo dependency)

This script creates a high-quality .ico file with multiple resolutions
(16x16, 32x32, 48x48, 256x256) by manually drawing the Supervertaler logo.

Requirements:
    pip install Pillow
"""

from pathlib import Path
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("\nPlease install Pillow:")
    print("  pip install Pillow")
    exit(1)


def create_sv_icon(size: int) -> Image.Image:
    """
    Create Supervertaler icon at specified size

    Args:
        size: Icon size in pixels (square)

    Returns:
        PIL Image with the Sv logo
    """
    # Create image with transparency
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Calculate dimensions
    center = size // 2
    radius = int(size * 0.44)  # 112/256 ≈ 0.44

    # Draw blue gradient circle (simplified as solid color for Pillow)
    # Using a mid-tone between #1976D2 and #2196F3
    circle_color = (33, 142, 227)  # #218EE3

    # Draw circle
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill=circle_color
    )

    # Draw "Sv" text
    # Font sizes matching SVG proportions (135/256 and 112/256)
    s_size = int(size * 0.527)  # 135/256
    v_size = int(size * 0.437)  # 112/256

    try:
        # Try to use Arial Bold
        font_s = ImageFont.truetype("arialbd.ttf", s_size)
        font_v = ImageFont.truetype("arialbd.ttf", v_size)
    except:
        # Fallback to default font
        font_s = ImageFont.load_default()
        font_v = ImageFont.load_default()

    # Get text dimensions for proper centering
    s_bbox = draw.textbbox((0, 0), "S", font=font_s)
    s_width = s_bbox[2] - s_bbox[0]
    s_height = s_bbox[3] - s_bbox[1]

    v_bbox = draw.textbbox((0, 0), "v", font=font_v)
    v_width = v_bbox[2] - v_bbox[0]
    v_height = v_bbox[3] - v_bbox[1]

    # Total width for centering
    total_width = s_width + v_width - int(size * 0.02)  # Slight overlap

    # Position text to match website (centered in circle)
    # SVG has y=178 for 256px baseline (178/256 = 0.695)
    text_baseline_y = int(size * 0.70)

    # Draw "S" (use baseline for consistent positioning)
    s_x = center - total_width // 2
    draw.text((s_x, text_baseline_y - s_height), "S", font=font_s, fill='white', anchor="lt")

    # Draw "v" with subscript offset (slightly lower than S baseline)
    v_x = s_x + s_width - int(size * 0.02)
    v_y_offset = int(size * 0.015)  # Small downward offset for subscript
    draw.text((v_x, text_baseline_y - v_height + v_y_offset), "v", font=font_v, fill='white', anchor="lt")

    return img


def create_multisize_ico(ico_path: Path, sizes: list[int] = None):
    """
    Create multi-resolution .ico file

    Args:
        ico_path: Path to output .ico file
        sizes: List of icon sizes to include (default: [16, 32, 48, 256])
    """
    if sizes is None:
        sizes = [16, 32, 48, 256]  # Standard Windows icon sizes

    print(f"Creating multi-resolution .ico...")
    print(f"Generating sizes: {', '.join(str(s) for s in sizes)}px")

    # Create icon at each size
    images = []
    for size in sizes:
        print(f"  Rendering {size}x{size}...")
        img = create_sv_icon(size)
        # Convert to RGB mode for better ICO compatibility (smaller sizes)
        if size <= 48:
            # Use palette mode for smaller sizes
            img_rgb = img.convert('RGB')
            images.append(img_rgb)
        else:
            images.append(img)

    # Save all sizes to .ico file
    print(f"  Saving to {ico_path}...")
    # Save using list of images - Pillow should automatically include all
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
    )

    # Show file size
    size_kb = ico_path.stat().st_size / 1024
    print(f"[OK] Created {ico_path.name} ({size_kb:.1f} KB)")
    print(f"  Contains {len(images)} resolutions for crisp display at all sizes")


if __name__ == '__main__':
    # Paths
    assets_dir = Path(__file__).parent / 'assets'
    ico_path = assets_dir / 'icon.ico'

    # Create multi-resolution icon
    create_multisize_ico(ico_path)

    print("\nDone! The new icon.ico will be used:")
    print("  - In PyInstaller builds (via Supervertaler.spec)")
    print("  - In Start Menu shortcuts")
    print("  - In taskbar when app is running")
    print("\nRebuild the Windows EXE to see the new icon.")
