#!/usr/bin/env python3
"""
Build Script for Supervertaler v2.4.1
Creates a distributable executable package using PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

class SupervertalerBuilder:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        self.package_name = "Supervertaler_v2.4.1"
        self.exe_name = "Supervertaler.exe"
        
    def print_header(self, text):
        """Print a formatted header"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70 + "\n")
    
    def print_step(self, step_num, total_steps, text):
        """Print a step indicator"""
        print(f"\n[{step_num}/{total_steps}] {text}")
        print("-" * 70)
    
    def check_dependencies(self):
        """Check if all required tools are installed"""
        self.print_step(1, 6, "Checking dependencies")
        
        # Check Python version
        python_version = sys.version_info
        print(f"OK - Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check for required packages
        required_packages = [
            ('PyInstaller', 'PyInstaller'),
            ('PIL', 'Pillow'),
            ('anthropic', 'anthropic'),
            ('google.generativeai', 'google-generativeai'),
            ('openai', 'openai'),
            ('docx', 'python-docx'),
        ]
        
        missing_packages = []
        
        for import_name, package_name in required_packages:
            try:
                __import__(import_name)
                print(f"OK - {package_name}")
            except ImportError:
                print(f"ERROR - {package_name} - NOT INSTALLED")
                missing_packages.append(package_name)
        
        if missing_packages:
            print("\nWARNING - Missing packages detected!")
            print("\nInstall them with:")
            print(f"  pip install {' '.join(missing_packages)}")
            return False
        
        print("\nOK - All dependencies installed!")
        return True
    
    def create_icon(self):
        """Create icon from image if it doesn't exist"""
        self.print_step(2, 6, "Creating application icon")
        
        icon_path = self.project_dir / "Supervertaler.ico"
        
        if icon_path.exists():
            print(f"OK - Icon already exists: {icon_path}")
            return True
        
        print("Icon not found. Running icon creator...")
        
        try:
            result = subprocess.run(
                [sys.executable, "create_icon.py"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                input="\n\n",  # Use defaults
                timeout=30
            )
            
            if result.returncode == 0 and icon_path.exists():
                print("OK - Icon created successfully!")
                return True
            else:
                print("WARNING - Icon creation failed, continuing without icon")
                print(result.stdout)
                print(result.stderr)
                return True  # Continue anyway
                
        except Exception as e:
            print(f"WARNING - Error creating icon: {e}")
            print("Continuing without icon...")
            return True  # Continue anyway
    
    def clean_previous_builds(self):
        """Remove previous build artifacts"""
        self.print_step(3, 6, "Cleaning previous builds")
        
        dirs_to_clean = [self.build_dir, self.dist_dir]
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                print(f"Removing {dir_path}...")
                shutil.rmtree(dir_path)
                print(f"OK - Cleaned {dir_path}")
            else:
                print(f"OK - {dir_path} doesn't exist (nothing to clean)")
    
    def build_executable(self):
        """Run PyInstaller to build the executable"""
        self.print_step(4, 6, "Building executable with PyInstaller")
        
        spec_file = self.project_dir / "Supervertaler.spec"
        
        if not spec_file.exists():
            print(f"ERROR - Spec file not found: {spec_file}")
            return False
        
        print(f"Using spec file: {spec_file}")
        print("This may take a few minutes...\n")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "PyInstaller", str(spec_file), "--clean"],
                cwd=self.project_dir,
                check=True
            )
            
            print("\nOK - Build completed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\nERROR - Build failed with error code {e.returncode}")
            return False
    
    def create_user_folders(self):
        """Create folders for user data in the distribution"""
        self.print_step(5, 6, "Setting up user folders")
        
        package_dir = self.dist_dir / self.package_name
        
        if not package_dir.exists():
            print(f"ERROR - Package directory not found: {package_dir}")
            return False
        
        # Create user data folders
        folders_to_create = [
            "api_keys.txt",  # Create empty file
            "custom_prompts_private",
            "projects",
            "projects_private",
        ]
        
        # Copy essential files to package root
        files_to_copy = [
            ("api_keys.example.txt", "api_keys.example.txt"),
            ("README.md", "README.md"),
            ("CHANGELOG.md", "CHANGELOG.md"),
        ]
        
        for src_file, dst_file in files_to_copy:
            src_path = self.project_dir / src_file
            dst_path = package_dir / dst_file
            if src_path.exists():
                shutil.copy(src_path, dst_path)
                print(f"OK - Copied {src_file}")
        
        # Copy folders from _internal to root for user convenience
        internal_dir = package_dir / "_internal"
        folders_to_copy = ["custom_prompts", "docs"]
        
        for folder in folders_to_copy:
            src_folder = internal_dir / folder
            dst_folder = package_dir / folder
            if src_folder.exists() and not dst_folder.exists():
                shutil.copytree(src_folder, dst_folder)
                print(f"OK - Copied {folder}/ to package root")
        
        # Create api_keys.txt as a copy of example
        api_keys_src = package_dir / "api_keys.example.txt"
        api_keys_dst = package_dir / "api_keys.txt"
        
        if api_keys_src.exists() and not api_keys_dst.exists():
            shutil.copy(api_keys_src, api_keys_dst)
            print(f"OK - Created api_keys.txt from example")
        
        # Create folders
        for folder in ["custom_prompts_private", "projects", "projects_private"]:
            folder_path = package_dir / folder
            folder_path.mkdir(exist_ok=True)
            
            # Create README in each folder
            readme_path = folder_path / "README.txt"
            with open(readme_path, 'w') as f:
                if 'private' in folder:
                    f.write(f"This folder is for your private {folder.replace('_private', '').replace('_', ' ')}.\n")
                    f.write("Files in this folder will not be synced to GitHub.\n")
                else:
                    f.write(f"This folder is for your {folder.replace('_', ' ')}.\n")
            
            print(f"OK - Created {folder}/")
        
        return True
    
    def create_distribution_package(self):
        """Create final distribution package"""
        self.print_step(6, 6, "Creating distribution package")
        
        package_dir = self.dist_dir / self.package_name
        
        if not package_dir.exists():
            print(f"ERROR - Package directory not found: {package_dir}")
            return False
        
        # Create installation guide
        install_guide = package_dir / "INSTALLATION_GUIDE.txt"
        
        with open(install_guide, 'w', encoding='utf-8') as f:
            f.write("""
═══════════════════════════════════════════════════════════════════════
                    SUPERVERTALER v2.4.1
                    Installation Guide
═══════════════════════════════════════════════════════════════════════

QUICK START:

1. Extract this entire folder to your desired location
   (e.g., C:\\Program Files\\Supervertaler\\ or your Documents folder)

2. Edit api_keys.txt and add your API keys:
   - Open api_keys.txt in Notepad
   - Add your OpenAI, Anthropic, and/or Google API keys
   - Save the file

3. Double-click Supervertaler.exe to launch the application!

═══════════════════════════════════════════════════════════════════════

FOLDER STRUCTURE:

Supervertaler.exe           - Main application (double-click to run)
api_keys.txt                - Your API keys (REQUIRED - edit this file)
api_keys.example.txt        - Example of how to format API keys
custom_prompts/             - Pre-made prompt templates
custom_prompts_private/     - Your private custom prompts
projects/                   - Your translation projects
projects_private/           - Your private projects
docs/                       - User guides and documentation
README.md                   - Full documentation
CHANGELOG.md                - Version history

═══════════════════════════════════════════════════════════════════════

IMPORTANT NOTES:

WARNING - API KEYS REQUIRED: You must add at least one API key to api_keys.txt
   before using Supervertaler. Get API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Google: https://makersuite.google.com/app/apikey

WARNING - KEEP THIS FOLDER INTACT: Do not move Supervertaler.exe out of this
   folder. It needs the other files and folders to work properly.

WARNING - WINDOWS SECURITY: If Windows SmartScreen blocks the app, click
   "More info" then "Run anyway". This is normal for new applications.

═══════════════════════════════════════════════════════════════════════

GETTING STARTED:

1. Read the User Guide: docs/user_guides/Supervertaler User Guide (v2.4.0).md
2. Set up API keys: docs/user_guides/API_KEYS_SETUP_GUIDE.md
3. Try the bilingual workflow: docs/user_guides/BILINGUAL_WORKFLOW_QUICK_START.md

═══════════════════════════════════════════════════════════════════════

SUPPORT:

- GitHub: https://github.com/michaelbeijer/Supervertaler
- Email: info@michaelbeijer.co.uk
- Website: https://michaelbeijer.co.uk

═══════════════════════════════════════════════════════════════════════
""")
        
        print(f"OK - Created INSTALLATION_GUIDE.txt")
        
        # Show package info
        print("\n" + "=" * 70)
        print("BUILD SUMMARY")
        print("=" * 70)
        
        exe_path = package_dir / self.exe_name
        if exe_path.exists():
            exe_size = exe_path.stat().st_size / (1024 * 1024)
            print(f"OK - Executable: {self.exe_name} ({exe_size:.1f} MB)")
        
        total_size = sum(f.stat().st_size for f in package_dir.rglob('*') if f.is_file())
        total_size_mb = total_size / (1024 * 1024)
        
        print(f"OK - Package size: {total_size_mb:.1f} MB")
        print(f"OK - Location: {package_dir}")
        
        return True
    
    def run(self):
        """Run the complete build process"""
        self.print_header("Supervertaler v2.4.1 - Build Script")
        
        print("This script will create a distributable executable package.")
        print("The process will take several minutes.\n")
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            print("\nERROR - Build aborted: Missing dependencies")
            return False
        
        # Step 2: Create icon
        if not self.create_icon():
            print("\nERROR - Build aborted: Icon creation failed")
            return False
        
        # Step 3: Clean previous builds
        self.clean_previous_builds()
        
        # Step 4: Build executable
        if not self.build_executable():
            print("\nERROR - Build aborted: Executable build failed")
            return False
        
        # Step 5: Create user folders
        if not self.create_user_folders():
            print("\nERROR - Build aborted: User folder creation failed")
            return False
        
        # Step 6: Create distribution package
        if not self.create_distribution_package():
            print("\nERROR - Build aborted: Distribution package creation failed")
            return False
        
        # Success!
        self.print_header("BUILD COMPLETED SUCCESSFULLY!")
        
        print("OK - Supervertaler is ready for distribution!\n")
        print(f"Distribution package location:")
        print(f"  {self.dist_dir / self.package_name}\n")
        print("Next steps:")
        print("  1. Test the executable by running Supervertaler.exe")
        print("  2. Zip the entire folder for distribution")
        print("  3. Upload to GitHub releases or your distribution platform")
        print()
        
        return True


if __name__ == "__main__":
    builder = SupervertalerBuilder()
    success = builder.run()
    sys.exit(0 if success else 1)