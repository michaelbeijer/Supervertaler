#!/usr/bin/env python3
"""
Create multi-resolution Windows .ico file from SVG

This script converts an SVG icon to a high-quality .ico file with multiple
resolutions (16x16, 32x32, 48x48, 256x256) for crisp display at all sizes.

Requirements:
    pip install Pillow cairosvg
"""

from pathlib import Path
try:
    from PIL import Image
    import cairosvg
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("\nPlease install required packages:")
    print("  pip install Pillow cairosvg")
    exit(1)


def create_multisize_ico(svg_path: Path, ico_path: Path, sizes: list[int] = None):
    """
    Convert SVG to multi-resolution .ico file

    Args:
        svg_path: Path to source SVG file
        ico_path: Path to output .ico file
        sizes: List of icon sizes to include (default: [16, 32, 48, 256])
    """
    if sizes is None:
        sizes = [16, 32, 48, 256]  # Standard Windows icon sizes

    print(f"Converting {svg_path.name} to multi-resolution .ico...")
    print(f"Generating sizes: {', '.join(str(s) for s in sizes)}px")

    # Convert SVG to PNG at each size
    images = []
    for size in sizes:
        print(f"  Rendering {size}x{size}...")

        # Convert SVG to PNG bytes at specific size
        png_bytes = cairosvg.svg2png(
            url=str(svg_path),
            output_width=size,
            output_height=size,
        )

        # Load PNG into PIL Image
        from io import BytesIO
        img = Image.open(BytesIO(png_bytes))
        images.append(img)

    # Save all sizes to .ico file
    print(f"  Saving to {ico_path}...")
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:],
    )

    # Show file size
    size_kb = ico_path.stat().st_size / 1024
    print(f"✓ Created {ico_path.name} ({size_kb:.1f} KB)")
    print(f"  Contains {len(images)} resolutions for crisp display at all sizes")


if __name__ == '__main__':
    # Paths
    assets_dir = Path(__file__).parent / 'assets'
    svg_path = assets_dir / 'icon_sv_simple.svg'  # Or use icon_sv_modern.svg
    ico_path = assets_dir / 'icon.ico'

    # Check if SVG exists
    if not svg_path.exists():
        print(f"Error: SVG file not found: {svg_path}")
        print("\nAvailable SVG files:")
        for svg in assets_dir.glob('*.svg'):
            print(f"  - {svg.name}")
        exit(1)

    # Create multi-resolution icon
    create_multisize_ico(svg_path, ico_path)

    print("\nDone! The new icon.ico will be used:")
    print("  - In PyInstaller builds (via Supervertaler.spec)")
    print("  - In Start Menu shortcuts")
    print("  - In taskbar when app is running")
    print("\nRebuild the Windows EXE to see the new icon.")
