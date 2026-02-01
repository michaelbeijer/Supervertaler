#!/usr/bin/env python3
"""
Create multi-resolution Windows .ico file by manually constructing the ICO format

Requirements:
    pip install Pillow
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import struct
from io import BytesIO


def create_sv_icon(size: int) -> Image.Image:
    """Create Supervertaler icon at specified size"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2
    radius = int(size * 0.44)
    circle_color = (33, 142, 227)  # #218EE3

    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill=circle_color
    )

    # For very small sizes (16x16), optimize font sizes for clarity while keeping "Sv"
    if size <= 16:
        s_size = 9  # Fixed pixel size for sharpness
        v_size = 7  # Fixed pixel size for sharpness
    else:
        # Font sizes matching SVG proportions for larger icons
        s_size = int(size * 0.527)  # 135/256
        v_size = int(size * 0.437)  # 112/256

    try:
        font_s = ImageFont.truetype("arialbd.ttf", s_size)
        font_v = ImageFont.truetype("arialbd.ttf", v_size)
    except:
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
    if size <= 16:
        total_width = s_width + v_width - 1  # Tighter spacing for small sizes
    else:
        total_width = s_width + v_width - int(size * 0.02)  # Slight overlap

    # Position text to match website (centered in circle)
    text_baseline_y = int(size * 0.70)

    # Draw "S" (use baseline for consistent positioning)
    s_x = center - total_width // 2
    draw.text((s_x, text_baseline_y - s_height), "S", font=font_s, fill='white', anchor="lt")

    # Draw "v" with subscript offset (slightly lower than S baseline)
    if size <= 16:
        v_x = s_x + s_width - 1  # Tighter spacing
        v_y_offset = 1  # Minimal offset for small size
    else:
        v_x = s_x + s_width - int(size * 0.02)
        v_y_offset = int(size * 0.015)  # Small downward offset for subscript

    draw.text((v_x, text_baseline_y - v_height + v_y_offset), "v", font=font_v, fill='white', anchor="lt")

    return img


def create_ico_manual(ico_path: Path, sizes: list[int]):
    """Manually construct ICO file with multiple resolutions"""

    print(f"Creating multi-resolution .ico manually...")
    print(f"Generating sizes: {', '.join(str(s) for s in sizes)}px")

    # Create images and convert to PNG bytes
    image_data = []
    for size in sizes:
        print(f"  Rendering {size}x{size}...")
        img = create_sv_icon(size)

        # Convert to PNG bytes
        png_buffer = BytesIO()
        img.save(png_buffer, 'PNG')
        png_bytes = png_buffer.getvalue()

        image_data.append((size, png_bytes))

    print(f"  Building ICO structure...")

    # Build ICO file manually
    # ICO format: ICONDIR (6 bytes) + ICONDIRENTRY array (16 bytes each) + image data

    ico_bytes = bytearray()

    # ICONDIR header
    ico_bytes += struct.pack('<HHH',
        0,              # Reserved (must be 0)
        1,              # Type (1 for .ICO)
        len(sizes)      # Number of images
    )

    # Calculate offsets
    header_size = 6 + (16 * len(sizes))
    current_offset = header_size

    # ICONDIRENTRY for each image
    for size, png_bytes in image_data:
        ico_bytes += struct.pack('<BBBBHHII',
            size if size < 256 else 0,  # Width (0 means 256)
            size if size < 256 else 0,  # Height (0 means 256)
            0,                          # Color palette (0 for PNG)
            0,                          # Reserved
            1,                          # Color planes
            32,                         # Bits per pixel
            len(png_bytes),             # Size of image data
            current_offset              # Offset to image data
        )
        current_offset += len(png_bytes)

    # Append all image data
    for size, png_bytes in image_data:
        ico_bytes += png_bytes

    # Write to file
    print(f"  Saving to {ico_path}...")
    with open(ico_path, 'wb') as f:
        f.write(ico_bytes)

    size_kb = len(ico_bytes) / 1024
    print(f"[OK] Created {ico_path.name} ({size_kb:.1f} KB)")
    print(f"  Contains {len(sizes)} resolutions for crisp display at all sizes")


if __name__ == '__main__':
    assets_dir = Path(__file__).parent / 'assets'
    ico_path = assets_dir / 'icon.ico'
    sizes = [16, 32, 48, 256]

    create_ico_manual(ico_path, sizes)

    print("\nDone! The new icon.ico will be used:")
    print("  - In PyInstaller builds (via Supervertaler.spec)")
    print("  - In Start Menu shortcuts")
    print("  - In taskbar when app is running")
    print("\nRebuild the Windows EXE to see the new icon.")
