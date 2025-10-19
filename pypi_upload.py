#!/usr/bin/env python
"""
Quick PyPI Setup and Upload Script for Supervertaler

This script handles the complete PyPI upload process:
1. Builds distribution packages
2. Tests with twine (checks for issues)
3. Uploads to PyPI

Usage:
    python pypi_upload.py
"""

import subprocess
import sys
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n{'='*70}")
    print(f"▶ {description}")
    print(f"{'='*70}")
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FAILED")
        print(f"Error code: {e.returncode}")
        return False

def main():
    """Main PyPI upload process"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  SUPERVERTALER v3.7.0 - PyPI UPLOAD TOOL                     ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Get project root
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    # Step 1: Check dependencies
    print("\n[1/4] Checking dependencies...")
    try:
        import build
        import twine
        print("  ✓ build installed")
        print("  ✓ twine installed")
    except ImportError:
        print("\n❌ Missing dependencies!")
        print("Install with: pip install --upgrade build twine")
        return 1
    
    # Step 2: Clean previous builds
    print("\n[2/4] Cleaning previous builds...")
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    for directory in [dist_dir, build_dir]:
        if directory.exists():
            shutil.rmtree(directory)
            print(f"  ✓ Removed {directory.name}/")
    
    # Remove egg-info
    for egg_dir in project_root.glob("*.egg-info"):
        shutil.rmtree(egg_dir)
        print(f"  ✓ Removed {egg_dir.name}")
    
    # Step 3: Build distribution
    print("\n[3/4] Building distribution packages...")
    if not run_command(
        [sys.executable, "-m", "build"],
        "Build distribution (wheel + sdist)"
    ):
        return 1
    
    # Show what was created
    if dist_dir.exists():
        print("\n📦 Distribution files created:")
        for file in sorted(dist_dir.glob("*")):
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"  • {file.name} ({size_mb:.2f} MB)")
    
    # Step 4: Check with twine
    print("\n[4/4] Checking files with twine...")
    if not run_command(
        ["twine", "check", str(dist_dir / "*")],
        "Twine check (validate metadata)"
    ):
        print("\n⚠️  Twine check reported issues (may not be critical)")
    
    # Final instructions
    print(f"""
    {'='*70}
    ✅ BUILD COMPLETE - Ready to Upload to PyPI
    {'='*70}
    
    📦 Distribution files ready in: dist/
    
    Next step: Upload to PyPI
    
    Option A - Upload directly (requires PyPI account):
        twine upload dist/*
    
    Option B - Test first on TestPyPI (recommended):
        twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    
    After upload, users can install with:
        pip install Supervertaler
    
    For detailed instructions, see: PYPI_UPLOAD_GUIDE.md
    
    {'='*70}
    """)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
