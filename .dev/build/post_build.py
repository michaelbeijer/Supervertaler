"""
Post-build script for Supervertaler
Copies user-facing files from _internal to root folder for better accessibility
"""

import os
import shutil
from pathlib import Path

def copy_to_root():
    """Copy user-facing files and folders from _internal to distribution root"""
    
    # Define paths
    dist_folder = Path("dist/Supervertaler_v2.4.1")
    internal_folder = dist_folder / "_internal"
    
    # Check if dist folder exists
    if not dist_folder.exists():
        print(f"❌ ERROR: Distribution folder not found: {dist_folder}")
        return False
    
    # Files to copy to root
    files_to_copy = [
        "api_keys.example.txt",
        "README.md",
        "CHANGELOG.md",
        "INSTALLATION_GUIDE.txt",
    ]
    
    # Folders to copy to root
    folders_to_copy = [
        "custom_prompts",
        "docs",
        "projects",
        "projects_private",
    ]
    
    print("=" * 60)
    print("POST-BUILD: Copying user-facing files to root folder")
    print("=" * 60)
    
    # Copy files
    for filename in files_to_copy:
        src = internal_folder / filename
        dst = dist_folder / filename
        
        if src.exists():
            try:
                shutil.copy2(src, dst)
                print(f"✅ Copied file: {filename}")
            except Exception as e:
                print(f"❌ Failed to copy {filename}: {e}")
        else:
            print(f"⚠️  File not found in _internal: {filename}")
    
    # Copy folders
    for foldername in folders_to_copy:
        src = internal_folder / foldername
        dst = dist_folder / foldername
        
        if src.exists():
            try:
                # Remove destination if it exists
                if dst.exists():
                    shutil.rmtree(dst)
                # Copy entire folder tree
                shutil.copytree(src, dst)
                # Count files in folder
                file_count = len(list(dst.rglob('*')))
                print(f"✅ Copied folder: {foldername}/ ({file_count} items)")
            except Exception as e:
                print(f"❌ Failed to copy {foldername}/: {e}")
        else:
            print(f"⚠️  Folder not found in _internal: {foldername}/")
    
    print("=" * 60)
    print("POST-BUILD: Complete!")
    print("=" * 60)
    
    # Verify final structure
    print("\nFinal ROOT folder contents:")
    root_items = sorted([item.name for item in dist_folder.iterdir()])
    for item in root_items:
        item_path = dist_folder / item
        if item_path.is_dir():
            print(f"  📁 {item}/")
        else:
            size_mb = item_path.stat().st_size / (1024 * 1024)
            print(f"  📄 {item} ({size_mb:.2f} MB)")
    
    return True

if __name__ == "__main__":
    success = copy_to_root()
    exit(0 if success else 1)
