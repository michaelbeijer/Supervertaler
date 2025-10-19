#!/usr/bin/env python3
"""
Simple JSON Prompt Viewer
Displays Supervertaler prompt files in human-readable format
"""

import json
import sys
import os

def view_prompt(json_file):
    """Display JSON prompt in human-readable format with proper line breaks"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {json_file}")
        print(f"   {str(e)}")
        sys.exit(1)
    
    # Header
    print()
    print("=" * 80)
    print(f"📄 {data.get('name', 'Unnamed Prompt')}")
    print("=" * 80)
    print()
    
    # Metadata section
    print("📋 METADATA")
    print("-" * 80)
    
    metadata_fields = [
        ('Description', 'description'),
        ('Domain', 'domain'),
        ('Version', 'version'),
        ('Task Type', 'task_type'),
        ('Created', 'created'),
        ('Modified', 'modified'),
        ('Source Language', 'source_language'),
        ('Target Language', 'target_language')
    ]
    
    for label, key in metadata_fields:
        value = data.get(key, '')
        if value:
            print(f"{label:20}: {value}")
    
    print()
    
    # Main translation prompt
    if 'translate_prompt' in data:
        print("📝 TRANSLATION PROMPT")
        print("-" * 80)
        print(data['translate_prompt'])
        print()
    
    # Proofreading prompt (if exists)
    if data.get('proofread_prompt'):
        print("✏️ PROOFREADING PROMPT")
        print("-" * 80)
        print(data['proofread_prompt'])
        print()
    
    # Footer
    print("=" * 80)
    print()

def list_prompts(directory):
    """List all JSON prompt files in a directory"""
    if not os.path.exists(directory):
        print(f"❌ Error: Directory not found: {directory}")
        sys.exit(1)
    
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    if not json_files:
        print(f"No JSON prompt files found in: {directory}")
        return
    
    print()
    print(f"📁 Prompt files in: {directory}")
    print("-" * 80)
    
    for i, filename in enumerate(sorted(json_files), 1):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            name = data.get('name', filename)
            domain = data.get('domain', 'N/A')
            print(f"{i:3}. {name:40} [{domain}]")
        except:
            print(f"{i:3}. {filename:40} [Error reading file]")
    
    print()

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print()
        print("=" * 80)
        print("📖 Supervertaler JSON Prompt Viewer")
        print("=" * 80)
        print()
        print("Usage:")
        print("  python view_prompt.py <prompt.json>              # View a specific prompt")
        print("  python view_prompt.py --list <directory>         # List all prompts in folder")
        print()
        print("Examples:")
        print('  python view_prompt.py "Patent Translation Specialist.json"')
        print('  python view_prompt.py --list "C:/Dev/Supervertaler/user data_private/System_prompts"')
        print()
        sys.exit(0)
    
    # List mode
    if sys.argv[1] == '--list' and len(sys.argv) > 2:
        list_prompts(sys.argv[2])
        sys.exit(0)
    
    # View mode
    view_prompt(sys.argv[1])

if __name__ == "__main__":
    main()
