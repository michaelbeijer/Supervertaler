#!/usr/bin/env python3
"""
Update Website Version Script
==============================

Automatically updates version references in the website to match
the version defined in Supervertaler_v3.7.6.py

⚠️  IMPORTANT: This script is intentionally conservative:
    - Updates: Website HTML (docs/index.html), download links
    - Preserves: CHANGELOG.md, RELEASE notes (historical records)
    
    Reason: CHANGELOG and release notes must NOT be updated to preserve
    the history of what features were in each past version.

Usage:
    python update_website_version.py

This script:
1. Reads APP_VERSION from Supervertaler_v3.7.6.py
2. Updates HTML files in docs/ (version badges, hero text)
3. Updates README.md download instructions ONLY
4. Preserves historical records (CHANGELOG, past release notes)
5. Reports changes made

This ensures the website stays in sync with the application version
without erasing historical release information.
"""

import os
import re
import sys
from pathlib import Path


def extract_version_from_python():
    """Extract APP_VERSION from Supervertaler_v3.7.2.py"""
    try:
        python_file = Path(__file__).parent / "Supervertaler_v3.7.2.py"
        with open(python_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('APP_VERSION'):
                    # Extract version string: APP_VERSION = "3.7.1"
                    match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', line)
                    if match:
                        return match.group(1)
    except Exception as e:
        print(f"❌ Error reading Python file: {e}")
        return None
    
    print("❌ Could not find APP_VERSION in Supervertaler_v3.7.1.py")
    return None


def update_html_files(version):
    """Update all version references in HTML files"""
    docs_dir = Path(__file__).parent / "docs"
    html_files = list(docs_dir.glob("*.html"))
    
    if not html_files:
        print(f"⚠️  No HTML files found in {docs_dir}")
        return 0
    
    total_replacements = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern 1: v3.x.x (any version number)
            # This will match v3.6.8, v3.7.0, v3.7.1, etc.
            content = re.sub(
                r'v\d+\.\d+\.\d+',
                f'v{version}',
                content
            )
            
            # Pattern 2: Supervertaler v3.x.x (in text)
            # This will match "Supervertaler v3.6.8" etc.
            content = re.sub(
                r'Supervertaler v\d+\.\d+\.\d+',
                f'Supervertaler v{version}',
                content
            )
            
            # Pattern 3: version": "3.x.x (in JSON/config strings)
            # This will match 3.6.8, 3.7.0, 3.7.1 etc.
            content = re.sub(
                r'version":\s*"?\d+\.\d+\.\d+',
                f'version": "{version}',
                content
            )
            
            # Count replacements
            if content != original_content:
                replacements = len(re.findall(r'v\d+\.\d+\.\d+', original_content))
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {html_file.name}: Updated version references")
                total_replacements += replacements
        
        except Exception as e:
            print(f"❌ Error processing {html_file.name}: {e}")
    
    return total_replacements


def update_markdown_files(version):
    """
    Update version references in Markdown files.
    
    NOTE: This function only updates README.md installation instructions.
    CHANGELOG.md and RELEASE notes are HISTORICAL RECORDS and should NOT be updated
    to preserve the history of what features were in each version.
    """
    root_dir = Path(__file__).parent
    md_file = root_dir / "README.md"
    
    if not md_file.exists():
        return 0
    
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # ONLY update these specific patterns in README:
        # Pattern 1: Download instruction filenames (Supervertaler-v3.x.x.zip)
        # Match: Supervertaler-v3.7.0.zip and replace with Supervertaler-v3.7.1.zip
        content = re.sub(
            r'Supervertaler-v\d+\.\d+\.\d+\.zip',
            f'Supervertaler-v{version}.zip',
            content
        )
        
        # Pattern 2: Installation section header "Supervertaler vX.X.X is available"
        # Match: "Supervertaler v3.7.0 is available" and replace with current version
        content = re.sub(
            r'Supervertaler v\d+\.\d+\.\d+ is available',
            f'Supervertaler v{version} is available',
            content
        )
        
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {md_file.name}: Updated download instructions")
            return 1
        else:
            print(f"ℹ️  {md_file.name}: No updates needed")
            return 0
    
    except Exception as e:
        print(f"❌ Error processing {md_file.name}: {e}")
        return 0


def main():
    """Main entry point"""
    print("=" * 60)
    print("🔄 Website Version Update Script")
    print("=" * 60)
    
    # Extract current version
    version = extract_version_from_python()
    if not version:
        print("\n❌ Failed to extract version. Aborting.")
        sys.exit(1)
    
    print(f"\n📌 Current version: v{version}")
    print(f"📍 Source file: Supervertaler_v3.7.1.py")
    
    # Update HTML files
    print(f"\n🔍 Scanning HTML files in docs/...")
    html_updates = update_html_files(version)
    
    # Update Markdown files
    print(f"\n🔍 Scanning Markdown files...")
    md_updates = update_markdown_files(version)
    
    # Summary
    total_updates = html_updates + md_updates
    print("\n" + "=" * 60)
    if total_updates > 0:
        print(f"✅ Success! Updated {total_updates} version references to v{version}")
    else:
        print(f"ℹ️  No version references found to update")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Review the changes: git diff")
    print("   2. Commit changes: git add .; git commit -m 'Update website version to v{}'".format(version))
    print("   3. Push to GitHub: git push origin main")
    print()


if __name__ == "__main__":
    main()
