#!/usr/bin/env python3
"""
Create navigation arrow icons for TM navigation (light and dark mode versions)

Requirements:
    pip install Pillow
"""

from pathlib import Path
from PIL import Image, ImageDraw


def create_arrow_icon(direction: str, color: str, size: int = 16) -> Image.Image:
    """
    Create a simple arrow icon

    Args:
        direction: 'left' or 'right'
        color: RGB tuple or hex string like '#FFFFFF'
        size: Icon size in pixels (square)
    """
    # Convert hex color to RGB if needed
    if isinstance(color, str) and color.startswith('#'):
        color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

    # Create transparent image
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw larger, more visible arrow triangle
    center = size // 2
    arrow_width = int(size * 0.5)   # Increased from 0.4
    arrow_height = int(size * 0.75)  # Increased from 0.6

    if direction == 'left':
        # Left-pointing triangle
        points = [
            (center + arrow_width//2, center - arrow_height//2),  # Top right
            (center + arrow_width//2, center + arrow_height//2),  # Bottom right
            (center - arrow_width//2, center),                     # Left point
        ]
    else:  # right
        # Right-pointing triangle
        points = [
            (center - arrow_width//2, center - arrow_height//2),  # Top left
            (center - arrow_width//2, center + arrow_height//2),  # Bottom left
            (center + arrow_width//2, center),                     # Right point
        ]

    draw.polygon(points, fill=color)

    return img


if __name__ == '__main__':
    assets_dir = Path(__file__).parent / 'assets'
    assets_dir.mkdir(exist_ok=True)

    print("Creating navigation arrow icons...")

    # Create light mode arrows (dark gray/black)
    print("  Creating light mode arrows (dark)...")
    create_arrow_icon('left', '#333333').save(assets_dir / 'arrow_left_light.png')
    create_arrow_icon('right', '#333333').save(assets_dir / 'arrow_right_light.png')

    # Create dark mode arrows (white)
    print("  Creating dark mode arrows (white)...")
    create_arrow_icon('left', '#FFFFFF').save(assets_dir / 'arrow_left_dark.png')
    create_arrow_icon('right', '#FFFFFF').save(assets_dir / 'arrow_right_dark.png')

    print("[OK] Arrow icons created in assets/ folder")
    print("  - arrow_left_light.png, arrow_right_light.png (for light mode)")
    print("  - arrow_left_dark.png, arrow_right_dark.png (for dark mode)")
