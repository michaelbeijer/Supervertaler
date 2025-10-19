#!/usr/bin/env python
"""
Build script for Supervertaler .exe standalone executable

This script builds a Windows .exe using PyInstaller that works without Python installed.

Usage:
    python build_exe.py

Requirements:
    pip install pyinstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    """Build Supervertaler .exe executable"""
    
    print("=" * 70)
    print("Supervertaler v3.7.0 - Building Windows .exe Executable")
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
    
    print(f"\nProject root: {project_root}")
    
    # Clean previous builds
    print("\n[1/3] Cleaning previous builds...")
    for dir_to_remove in [dist_dir, build_dir]:
        if dir_to_remove.exists():
            print(f"  - Removing {dir_to_remove.name}/")
            shutil.rmtree(dir_to_remove)
    
    # Remove spec build artifacts
    spec_files = list(project_root.glob("*.spec"))
    if spec_files:
        for spec_file in spec_files:
            if spec_file.name != "Supervertaler.spec":
                spec_file.unlink()
    
    # Build executable with PyInstaller
    print("\n[2/3] Building executable with PyInstaller...")
    print("  This may take a few minutes (2-5 minutes typical)...")
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=Supervertaler",
        f"--distpath={dist_dir}",
        "--workpath=.\\build",
        "--exclude-module=PyQt6",
        "--add-data=assets;assets",
        "--add-data=modules;modules",
        "--add-data=docs;docs",
        "--add-data=README.md;.",
        "--add-data=CHANGELOG.md;.",
        "--add-data=FAQ.md;.",
        "--add-data=api_keys.example.txt;.",
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
    
    # Verify build
    print("\n[3/3] Verifying build...")
    exe_path = dist_dir / "Supervertaler.exe"
    
    if exe_path.exists():
        file_size = exe_path.stat().st_size
        size_mb = file_size / (1024 * 1024)
        print(f"  ✓ Executable created: {exe_path}")
        print(f"  ✓ File size: {size_mb:.1f} MB")
        
        print("\n" + "=" * 70)
        print("✓ BUILD SUCCESSFUL!")
        print("=" * 70)
        print(f"\nExecutable: {exe_path}")
        print(f"Ready to distribute: dist/Supervertaler.exe")
        print("\nNext steps:")
        print("  1. Test the .exe locally")
        print("  2. Upload to GitHub release")
        print("  3. Users can download and run without Python!")
        print("\n" + "=" * 70)
        
        return 0
    else:
        print(f"\n✗ Build verification failed!")
        print(f"  Expected: {exe_path}")
        print(f"  Not found!")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
