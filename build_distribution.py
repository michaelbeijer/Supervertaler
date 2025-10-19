#!/usr/bin/env python
"""
Build script for Supervertaler - Creates standalone distribution package

This script creates a complete distribution folder with:
- Supervertaler executable
- All support folders (assets, modules, docs)
- Template files (api_keys.example.txt, README, etc.)

This allows users to extract and run the application without Python installed.

Usage:
    python build_distribution.py

Requirements:
    pip install pyinstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    """Build Supervertaler distribution package"""
    
    print("=" * 70)
    print("Supervertaler v3.7.0 - Building Distribution Package")
    print("=" * 70)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("✗ PyInstaller not found!")
        print("\nInstall with: pip install pyinstaller")
        sys.exit(1)
    
    # Get project root
    project_root = Path(__file__).parent
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    dist_package_dir = dist_dir / "Supervertaler"
    
    print(f"\nProject root: {project_root}")
    
    # Clean previous builds
    print("\n[1/4] Cleaning previous builds...")
    for dir_to_remove in [dist_dir, build_dir]:
        if dir_to_remove.exists():
            print(f"  - Removing {dir_to_remove.name}/")
            shutil.rmtree(dir_to_remove)
    
    # Create distribution directory structure
    print("\n[2/4] Creating distribution package structure...")
    dist_package_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Created {dist_package_dir.name}/")
    
    # Build executable with PyInstaller (one-file mode)
    print("\n[3/4] Building executable with PyInstaller...")
    print("  This may take a few minutes (3-5 minutes typical)...")
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",  # Single executable file
        "--windowed",
        "--name=Supervertaler",
        f"--distpath={dist_package_dir}",
        "--workpath=.\\build",
        "--exclude-module=PyQt6",
        "Supervertaler_v3.7.0.py",
    ]
    
    # Add icon if available
    icon_path = project_root / "assets" / "icon.ico"
    if icon_path.exists():
        cmd.insert(9, f"--icon={icon_path}")
        print(f"  ✓ Icon found: {icon_path}")
    
    try:
        result = subprocess.run(cmd, cwd=project_root, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code {e.returncode}")
        sys.exit(1)
    
    # Verify and copy supporting files
    print("\n[4/4] Verifying and copying supporting files...")
    exe_path = dist_package_dir / "Supervertaler.exe"
    
    if exe_path.exists():
        file_size = exe_path.stat().st_size
        size_mb = file_size / (1024 * 1024)
        print(f"  ✓ Executable: Supervertaler.exe ({size_mb:.1f} MB)")
        
        # Copy support folders and files to dist root
        files_to_copy = [
            ("docs", True),                    # folders (True = directory)
            ("user data", True),
            ("assets", True),
            ("modules", True),
            ("api_keys.example.txt", False),
            ("README.md", False),
            ("CHANGELOG.md", False),
            ("FAQ.md", False),
        ]
        
        print(f"\n  Copying support files to distribution root...")
        for item_name, is_dir in files_to_copy:
            source = project_root / item_name
            dest = dist_package_dir / item_name
            
            if source.exists():
                if is_dir:
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(source, dest)
                    file_count = len(list(dest.rglob("*")))
                    print(f"    ✓ Copied {item_name}/ ({file_count} files)")
                else:
                    shutil.copy2(source, dest)
                    size_kb = dest.stat().st_size / 1024
                    print(f"    ✓ Copied {item_name} ({size_kb:.0f} KB)")
            else:
                if item_name != "user data":  # user data is optional
                    print(f"    ⚠ Not found: {item_name}")
        
        # List what users will see
        print(f"\n  📦 Distribution root contents:")
        items_list = sorted([item.name for item in dist_package_dir.iterdir()])
        for item in items_list:
            full_path = dist_package_dir / item
            if full_path.is_dir():
                file_count = len(list(full_path.rglob("*")))
                print(f"    📁 {item}/ ({file_count} files)")
            else:
                size_kb = full_path.stat().st_size / 1024
                if size_kb > 1000:
                    size_str = f"{size_kb/1024:.1f} MB"
                else:
                    size_str = f"{size_kb:.0f} KB"
                print(f"    📄 {item} ({size_str})")
        
        # Calculate total package size
        total_size = sum(f.stat().st_size for f in dist_package_dir.rglob("*") if f.is_file())
        total_mb = total_size / (1024 * 1024)
        
        print("\n" + "=" * 70)
        print("✓ BUILD SUCCESSFUL!")
        print("=" * 70)
        print(f"\nDistribution Package Ready: dist/Supervertaler/")
        print(f"Total Size: {total_mb:.1f} MB")
        print(f"\nWhat users see when they extract:")
        print(f"  Supervertaler.exe (standalone executable)")
        print(f"  docs/ (documentation)")
        print(f"  user data/ (profiles, templates, settings)")
        print(f"  assets/ (icons, images)")
        print(f"  modules/ (application modules)")
        print(f"  api_keys.example.txt (API configuration template)")
        print(f"  README.md, CHANGELOG.md, FAQ.md (guides)")
        print(f"\nNext steps:")
        print(f"  1. Test: dist/Supervertaler/Supervertaler.exe")
        print(f"  2. Compress: zip -r Supervertaler-v3.7.0.zip dist/Supervertaler")
        print(f"  3. Upload to GitHub release")
        print("\n" + "=" * 70)
        
        return 0
    else:
        print(f"\n✗ Build verification failed!")
        print(f"  Expected: {exe_path}")
        print(f"  Not found!")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
