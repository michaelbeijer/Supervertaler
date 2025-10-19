#!/usr/bin/env python3
"""
Conversion script to migrate prompts from JSON to Markdown format.
This script converts all JSON files to Markdown with YAML frontmatter.
"""

import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from prompt_library import PromptLibrary

def get_user_data_path(subfolder="", use_private=False):
    """Get user data path"""
    base = "user data_private" if use_private else "user data"
    if subfolder:
        return os.path.join(os.path.dirname(__file__), base, subfolder)
    return os.path.join(os.path.dirname(__file__), base)

def main():
    """Convert all prompts from JSON to Markdown"""
    
    print("=" * 60)
    print("Supervertaler Prompt Format Converter (JSON -> Markdown)")
    print("=" * 60)
    
    # Initialize library with both public and private directories
    system_prompts_public = get_user_data_path("System_prompts", use_private=False)
    system_prompts_private = get_user_data_path("System_prompts", use_private=True)
    custom_instructions_public = get_user_data_path("Custom_instructions", use_private=False)
    custom_instructions_private = get_user_data_path("Custom_instructions", use_private=True)
    
    def log_msg(msg):
        print(msg)
    
    # Process public System Prompts
    print("\n1. Converting PUBLIC System Prompts...")
    if os.path.exists(system_prompts_public):
        lib = PromptLibrary(system_prompts_dir=system_prompts_public, log_callback=log_msg)
        converted, failed = lib.convert_json_to_markdown(system_prompts_public, "system_prompt")
        print(f"   Result: {converted} converted, {failed} failed")
    else:
        print(f"   (Directory not found: {system_prompts_public})")
    
    # Process private System Prompts
    print("\n2. Converting PRIVATE System Prompts...")
    if os.path.exists(system_prompts_private):
        lib = PromptLibrary(system_prompts_dir=system_prompts_private, log_callback=log_msg)
        converted, failed = lib.convert_json_to_markdown(system_prompts_private, "system_prompt")
        print(f"   Result: {converted} converted, {failed} failed")
    else:
        print(f"   (Directory not found: {system_prompts_private})")
    
    # Process public Custom Instructions
    print("\n3. Converting PUBLIC Custom Instructions...")
    if os.path.exists(custom_instructions_public):
        lib = PromptLibrary(custom_instructions_dir=custom_instructions_public, log_callback=log_msg)
        converted, failed = lib.convert_json_to_markdown(custom_instructions_public, "custom_instruction")
        print(f"   Result: {converted} converted, {failed} failed")
    else:
        print(f"   (Directory not found: {custom_instructions_public})")
    
    # Process private Custom Instructions
    print("\n4. Converting PRIVATE Custom Instructions...")
    if os.path.exists(custom_instructions_private):
        lib = PromptLibrary(custom_instructions_dir=custom_instructions_private, log_callback=log_msg)
        converted, failed = lib.convert_json_to_markdown(custom_instructions_private, "custom_instruction")
        print(f"   Result: {converted} converted, {failed} failed")
    else:
        print(f"   (Directory not found: {custom_instructions_private})")
    
    print("\n" + "=" * 60)
    print("Conversion complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
