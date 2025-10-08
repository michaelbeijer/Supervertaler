#!/usr/bin/env python3
"""
Icon Creator for Supervertaler
Converts an image to .ico format for use with PyInstaller
"""

from PIL import Image
import os

def create_icon(input_image, output_icon="Supervertaler.ico"):
    """
    Convert an image to .ico format with multiple sizes
    
    Args:
        input_image: Path to source image (JPG, PNG, etc.)
        output_icon: Path to output .ico file
    """
    try:
        # Open the image
        img = Image.open(input_image)
        print(f"✓ Loaded image: {input_image}")
        print(f"  Original size: {img.size}")
        
        # Convert to RGBA if necessary
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            print(f"  Converted to RGBA mode")
        
        # Define icon sizes (Windows standard sizes)
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Create a list to store resized images
        icon_images = []
        
        for size in icon_sizes:
            # Create a copy and resize
            resized = img.copy()
            resized.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Create a new image with the exact size (in case thumbnail didn't match)
            icon_img = Image.new('RGBA', size, (0, 0, 0, 0))
            
            # Center the resized image
            offset = ((size[0] - resized.size[0]) // 2, (size[1] - resized.size[1]) // 2)
            icon_img.paste(resized, offset)
            
            icon_images.append(icon_img)
            print(f"  ✓ Created {size[0]}x{size[1]} icon")
        
        # Save as .ico with multiple sizes
        icon_images[0].save(
            output_icon,
            format='ICO',
            sizes=icon_sizes,
            append_images=icon_images[1:]
        )
        
        print(f"\n✓ Icon created successfully: {output_icon}")
        print(f"  File size: {os.path.getsize(output_icon):,} bytes")
        print(f"  Contains {len(icon_sizes)} sizes: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")
        
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: Image file not found: {input_image}")
        return False
    except Exception as e:
        print(f"✗ Error creating icon: {e}")
        return False


if __name__ == "__main__":
    # Default: use Supervertaler_character.JPG from Screenshots folder
    input_image = "Screenshots/Supervertaler_character.JPG"
    output_icon = "Supervertaler.ico"
    
    print("=" * 60)
    print("Supervertaler Icon Creator")
    print("=" * 60)
    print()
    
    # Check if PIL is installed
    print("Checking dependencies...")
    try:
        from PIL import Image
        print("✓ Pillow (PIL) is installed")
    except ImportError:
        print("✗ Pillow is not installed!")
        print("\nPlease install it with:")
        print("  pip install Pillow")
        exit(1)
    
    print()
    
    # Allow custom input
    custom_input = input(f"Image to convert (press Enter for '{input_image}'): ").strip()
    if custom_input:
        input_image = custom_input
    
    custom_output = input(f"Output icon name (press Enter for '{output_icon}'): ").strip()
    if custom_output:
        output_icon = custom_output
    
    print()
    print("-" * 60)
    
    # Create the icon
    success = create_icon(input_image, output_icon)
    
    print("-" * 60)
    
    if success:
        print("\n✓ Icon is ready to use with PyInstaller!")
        print(f"\nUse it in your build with:")
        print(f"  pyinstaller --icon={output_icon} Supervertaler_v2.4.1.py")
    else:
        print("\n✗ Icon creation failed. Please check the error messages above.")
    
    print()
