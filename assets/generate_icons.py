"""
Generate icon files from SVG for all platforms
Requires: pip install cairosvg pillow
"""

import os
from pathlib import Path

try:
    import cairosvg
    from PIL import Image
    import io
except ImportError:
    print("Missing dependencies. Please install:")
    print("pip install cairosvg pillow")
    exit(1)

# Base directory
assets_dir = Path(__file__).parent
source_svg = assets_dir / "icon_sv_modern.svg"
output_dir = assets_dir

# Define sizes needed
SIZES = {
    'windows': [16, 24, 32, 48, 64, 128, 256],  # For .ico
    'web': [16, 32, 48, 180],  # Favicon and Apple touch icon
    'macos': [16, 32, 64, 128, 256, 512, 1024],  # For .icns
}

def svg_to_png(svg_path, output_path, size):
    """Convert SVG to PNG at specified size"""
    print(f"Generating {size}x{size} PNG...")

    # Convert SVG to PNG bytes
    png_data = cairosvg.svg2png(
        url=str(svg_path),
        output_width=size,
        output_height=size
    )

    # Save PNG
    with open(output_path, 'wb') as f:
        f.write(png_data)

    return output_path

def create_ico(png_paths, output_path):
    """Create Windows .ico file from multiple PNGs"""
    print(f"\nCreating {output_path}...")

    images = []
    for png_path in png_paths:
        img = Image.open(png_path)
        images.append(img)

    # Save as ICO with all sizes
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images]
    )

    print(f"✓ Created {output_path}")

def main():
    if not source_svg.exists():
        print(f"Error: {source_svg} not found!")
        return

    print("=" * 60)
    print("Supervertaler Icon Generator")
    print("=" * 60)
    print(f"Source: {source_svg}")
    print()

    # Generate all PNG sizes
    all_sizes = set()
    for platform_sizes in SIZES.values():
        all_sizes.update(platform_sizes)

    png_files = {}
    for size in sorted(all_sizes):
        output_png = output_dir / f"icon_{size}x{size}.png"
        svg_to_png(source_svg, output_png, size)
        png_files[size] = output_png

    print("\n" + "=" * 60)
    print("Creating platform-specific icon files...")
    print("=" * 60)

    # Create Windows .ico
    ico_pngs = [png_files[size] for size in SIZES['windows']]
    create_ico(ico_pngs, output_dir / "icon.ico")

    # Create favicon (16, 32, 48 in one .ico)
    favicon_pngs = [png_files[16], png_files[32], png_files[48]]
    create_ico(favicon_pngs, output_dir / "favicon.ico")

    # Copy specific sizes for web
    print(f"\n✓ Created icon_180x180.png (Apple Touch Icon)")

    # Create macOS .icns (requires iconutil on macOS, so just note it)
    print("\n" + "=" * 60)
    print("macOS .icns creation:")
    print("=" * 60)
    print("For macOS, use these PNG files with iconutil:")
    print("1. Create icon.iconset folder")
    print("2. Copy/rename PNGs following macOS naming:")
    for size in SIZES['macos']:
        if size <= 512:
            print(f"   - icon_{size}x{size}.png → icon_{size}x{size}.png")
            if size * 2 in SIZES['macos']:
                print(f"   - icon_{size*2}x{size*2}.png → icon_{size}x{size}@2x.png")
    print("3. Run: iconutil -c icns icon.iconset")

    print("\n" + "=" * 60)
    print("✓ Icon generation complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print(f"  - icon.ico (Windows app icon)")
    print(f"  - favicon.ico (Website favicon)")
    print(f"  - icon_*x*.png (Various sizes)")
    print("\nNext steps:")
    print("  1. Integrate icon.ico into PyQt6 application")
    print("  2. Copy favicon.ico to website docs/")
    print("  3. Update website to use icon SVG in header")

if __name__ == "__main__":
    main()
