#!/usr/bin/env python3
"""
Simplified icon creator - generates individual PNG files that can be converted online

This creates PNG files at multiple resolutions that you can upload to an online
ICO converter like: https://convertio.co/png-ico/ or https://www.icoconverter.com/

Requirements:
    pip install Pillow
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_sv_icon(size: int) -> Image.Image:
    """Create Supervertaler icon at specified size"""
    # Create image with transparency
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Calculate dimensions
    center = size // 2
    radius = int(size * 0.44)

    # Draw blue circle
    circle_color = (33, 142, 227)  # #218EE3
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill=circle_color
    )

    # Draw "Sv" text
    s_size = int(size * 0.52)
    v_size = int(size * 0.44)

    try:
        font_s = ImageFont.truetype("arialbd.ttf", s_size)
        font_v = ImageFont.truetype("arialbd.ttf", v_size)
    except:
        font_s = ImageFont.load_default()
        font_v = ImageFont.load_default()

    # Draw "S"
    s_bbox = draw.textbbox((0, 0), "S", font=font_s)
    s_width = s_bbox[2] - s_bbox[0]

    # Draw "v"
    v_bbox = draw.textbbox((0, 0), "v", font=font_v)
    v_width = v_bbox[2] - v_bbox[0]

    # Calculate total width for centering
    total_width = s_width + v_width

    # Position text
    text_y = int(size * 0.55)

    # Draw "S"
    s_x = center - total_width // 2
    draw.text((s_x, text_y), "S", font=font_s, fill='white', anchor="lt")

    # Draw "v"
    v_x = s_x + s_width
    v_y_offset = int(size * 0.008)
    draw.text((v_x, text_y + v_y_offset), "v", font=font_v, fill='white', anchor="lt")

    return img


if __name__ == '__main__':
    assets_dir = Path(__file__).parent / 'assets'
    sizes = [16, 32, 48, 256]

    print("Creating PNG files at multiple resolutions...")
    print("These can be uploaded to an online ICO converter.\n")

    for size in sizes:
        output_path = assets_dir / f'icon_{size}x{size}.png'
        print(f"  Creating {size}x{size}...")
        img = create_sv_icon(size)
        img.save(output_path, 'PNG')
        print(f"    Saved: {output_path.name}")

    print("\n[OK] PNG files created!")
    print("\nNext steps:")
    print("1. Go to: https://www.icoconverter.com/")
    print("2. Upload the 256x256 PNG file")
    print("3. Download the generated .ico file")
    print("4. Replace assets/icon.ico with the downloaded file")
    print("\nOr upload all PNGs to: https://convertio.co/png-ico/")
