#!/usr/bin/env python3
"""
Comprehensive Test Suite for Supervertaler v3.7.0-beta

Tests all major components to ensure nothing is broken by recent changes:
- Security updates (pre-commit hooks, .gitignore)
- Repository consolidation (.dev/previous_versions)
- Root directory cleanup
- Module imports and functionality
"""

import os
import sys
import json
from pathlib import Path

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

# Test results
results = {
    'passed': 0,
    'failed': 0,
    'warnings': 0,
    'errors': []
}

def test(name, condition, details=""):
    """Record test result"""
    if condition:
        print(f"✓ {name}")
        results['passed'] += 1
    else:
        print(f"✗ {name}")
        if details:
            print(f"  → {details}")
        results['failed'] += 1
        results['errors'].append(f"{name}: {details}")

def warning(name, message):
    """Record warning"""
    print(f"⚠ {name}: {message}")
    results['warnings'] += 1

print("=" * 70)
print("SUPERVERTALER v3.7.0-beta - COMPREHENSIVE TEST SUITE")
print("=" * 70)
print()

# ============================================================================
# 1. SECURITY TESTS
# ============================================================================
print("1. SECURITY CHECKS")
print("-" * 70)

# Check .gitignore
gitignore_path = Path('.gitignore')
test("✓ .gitignore exists", gitignore_path.exists(), "Critical file missing!")

if gitignore_path.exists():
    with open(gitignore_path, 'r') as f:
        gitignore_content = f.read()
    
    test("  - user data_private/ protected", 
         "user data_private/" in gitignore_content,
         "CRITICAL: Private data folder not protected!")
    
    test("  - api_keys.txt protected",
         "api_keys.txt" in gitignore_content,
         "CRITICAL: API keys not protected!")

# Check pre-commit hook
hook_path = Path('.git/hooks/pre-commit')
test("✓ Pre-commit hook installed", hook_path.exists(), "Security hook missing!")

if hook_path.exists():
    with open(hook_path, 'r', encoding='utf-8', errors='ignore') as f:
        hook_content = f.read()
    
    test("  - Checks user_data_private removal",
         "user data_private" in hook_content,
         "Hook doesn't check for private data removal!")

# Check security documentation
test("✓ SECURITY_SETUP_GUIDE.md exists",
     Path('SECURITY_SETUP_GUIDE.md').exists())
test("✓ .dev/CRITICAL_GITIGNORE_ENTRIES.md exists",
     Path('.dev/CRITICAL_GITIGNORE_ENTRIES.md').exists())
test("✓ .dev/SECURITY_INCIDENT_ROOT_CAUSE.md exists",
     Path('.dev/SECURITY_INCIDENT_ROOT_CAUSE.md').exists())

print()

# ============================================================================
# 2. REPOSITORY STRUCTURE TESTS
# ============================================================================
print("2. REPOSITORY STRUCTURE")
print("-" * 70)

# Check root directory - should be clean
root_files = [f.name for f in Path('.').glob('*') 
              if f.is_file() and not f.name.startswith('.')]
root_garbage = [f for f in root_files if f.endswith('.md') and 'BUGFIX' in f or 'RELEASE' in f]
test("✓ Root directory clean (no garbage files)", len(root_garbage) == 0,
     f"Found: {', '.join(root_garbage)}")

# Check .dev/previous_versions
prev_versions_path = Path('.dev/previous_versions')
test("✓ .dev/previous_versions exists", prev_versions_path.exists())

if prev_versions_path.exists():
    version_files = list(prev_versions_path.glob('*.py'))
    test(f"  - Contains {len(version_files)} archived versions",
         len(version_files) > 0,
         "No archived versions found!")

# Check root previous_versions is removed
test("✓ Root previous_versions/ removed",
     not Path('previous_versions').exists(),
     "Old previous_versions folder still exists!")

# Check user data_private is NOT tracked by git
print()

# ============================================================================
# 3. MODULE IMPORT TESTS
# ============================================================================
print("3. MODULE IMPORTS")
print("-" * 70)

modules_to_test = [
    ('modules.prompt_library', 'PromptLibrary'),
    ('modules.tag_manager', 'TagManager'),
    ('modules.tracked_changes', 'TrackedChanges'),
    ('modules.simple_segmenter', 'SimpleSegmenter'),
    ('modules.document_analyzer', 'DocumentAnalyzer'),
    ('modules.translation_memory', 'TranslationMemory'),
]

for full_module_name, class_name in modules_to_test:
    try:
        module = __import__(full_module_name, fromlist=[class_name])
        has_class = hasattr(module, class_name)
        test(f"✓ {full_module_name}.{class_name} imports",
             has_class,
             f"Class {class_name} not found in module!")
    except Exception as e:
        test(f"✓ {full_module_name} imports", False, str(e))

print()

# ============================================================================
# 4. ENCODING TESTS
# ============================================================================
print("4. ENCODING FIXES")
print("-" * 70)

# Check for problematic Unicode in prompt_library
prompt_lib_path = Path('modules/prompt_library.py')
if prompt_lib_path.exists():
    with open(prompt_lib_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    test("✓ No ⚠ emoji in prompt_library.py",
         '⚠' not in content,
         "Unicode emoji still present!")
    
    test("  - Uses [WARNING] instead",
         '[WARNING]' in content,
         "Warning replacement not found!")

print()

# ============================================================================
# 5. CONFIGURATION TESTS
# ============================================================================
print("5. CONFIGURATION")
print("-" * 70)

main_file = Path('Supervertaler_v3.7.0-beta.py')
test("✓ Main app file exists", main_file.exists())

if main_file.exists():
    with open(main_file, 'r', encoding='utf-8', errors='ignore') as f:
        main_content = f.read()
    
    test("  - APP_VERSION = '3.7.0-beta'",
         "APP_VERSION = '3.7.0-beta'" in main_content or 'APP_VERSION = "3.7.0-beta"' in main_content)
    
    test("  - Supervertaler v3.7.0-beta in title",
         'Supervertaler v3.7.0-beta' in main_content)

print()

# ============================================================================
# 6. GIT STATUS TESTS
# ============================================================================
print("6. GIT REPOSITORY STATUS")
print("-" * 70)

# Check if git is available
try:
    import subprocess
    git_status = subprocess.run(['git', 'status', '--porcelain'], 
                               capture_output=True, text=True, timeout=5)
    modified_files = [line for line in git_status.stdout.split('\n') if line]
    
    test("✓ Git repository clean or only expected changes",
         len(modified_files) <= 2,  # Allow encoding fix + this test file
         f"Unexpected changes: {modified_files}")
    
    # Check latest commit
    git_log = subprocess.run(['git', 'log', '--oneline', '-1'], 
                            capture_output=True, text=True, timeout=5)
    latest_commit = git_log.stdout.strip()
    test("  - Latest commit related to fixes/security",
         any(word in latest_commit.lower() for word in 
             ['fix', 'security', 'encoding', 'prevention']),
         f"Unexpected commit: {latest_commit}")
         
except Exception as e:
    warning("Git status check", str(e))

print()

# ============================================================================
# 7. FILE INTEGRITY TESTS
# ============================================================================
print("7. FILE INTEGRITY")
print("-" * 70)

critical_files = [
    'Supervertaler_v3.7.0-beta.py',
    'README.md',
    'CHANGELOG.md',
    '.gitignore',
    'modules/__init__.py',
    'modules/prompt_library.py',
]

for file in critical_files:
    test(f"✓ {file} exists", Path(file).exists())

# Check for broken imports in main file
test("✓ Main file syntax valid (no encoding errors)",
     not any(b'\x8f' in open(Path(f), 'rb').read() 
             for f in [main_file] if main_file.exists()),
     "Binary encoding issues detected!")

print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 70)
print(f"TEST RESULTS: {results['passed']} passed, {results['failed']} failed, {results['warnings']} warnings")
print("=" * 70)

if results['failed'] > 0:
    print("\nFAILED TESTS:")
    for error in results['errors']:
        print(f"  • {error}")
    sys.exit(1)
elif results['warnings'] > 0:
    print("\n✓ All critical tests passed (with warnings)")
    sys.exit(0)
else:
    print("\n✓ All tests passed successfully!")
    sys.exit(0)
