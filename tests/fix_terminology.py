#!/usr/bin/env python3
"""Fix terminology: replace glossary with termbase throughout codebase"""

import os
import re

# Files to process
files_to_fix = [
    'Supervertaler_Qt.py',
    'modules/database_manager.py',
    'modules/glossary_manager.py',
    'Supervertaler_tkinter.py'
]

replacements = [
    # Database table/column names
    ('glossary_terms', 'termbase_terms'),
    ('glossary_id', 'termbase_id'),
    ('glossary_project_activation', 'termbase_project_activation'),
    
    # Class and method names (case-sensitive patterns)
    (r'class GlossaryInfo', 'class TermbaseInfo'),
    (r'class GlossaryManager', 'class TermbaseManager'),
    (r'class TermEntry', 'class TermbaseEntry'),
    
    # Method names
    (r'def get_glossaries\b', 'def get_termbases'),
    (r'def get_all_glossaries\b', 'def get_all_termbases'),
    (r'def get_glossary_terms\b', 'def get_termbase_terms'),
    (r'def add_glossary_term\b', 'def add_termbase_term'),
    (r'def delete_glossary\b', 'def delete_termbase'),
    (r'def create_glossary\b', 'def create_termbase'),
    (r'def create_glossary_results_tab\b', 'def create_termbase_results_tab'),
    (r'def display_glossary_results\b', 'def display_termbase_results'),
    (r'def create_glossary_tab\b', 'def create_termbase_tab'),
    (r'def search_glossary\b', 'def search_termbase'),
    
    # Variable names (more carefully)
    (r'glossary_tab\b', 'termbase_tab'),
    (r'glossary_mgr\b', 'termbase_mgr'),
    (r'glossary_manager', 'termbase_manager'),
    (r'glossary_combo', 'termbase_combo'),
    (r'glossary_tree', 'termbase_tree'),
    (r'glossary_results_table', 'termbase_results_table'),
    (r'glossary_source_var', 'termbase_source_var'),
    
    # UI strings
    ('Glossary Manager', 'Termbase Manager'),
    ('Glossary Results', 'Termbase Results'),
    ('Glossary:', 'Termbase:'),
    ('Search Glossary', 'Search Termbase'),
    ('Glossary terms', 'Termbase terms'),
    ('Glossary/Termbase', 'Termbase'),
    ('Project Glossary', 'Project Termbase'),
    ('Main Termbase', 'Main Termbase'),
    ('Domain Glossary', 'Domain Termbase'),
    ('All Glossaries', 'All Termbases'),
    
    # Comments
    ('# Glossary', '# Termbase'),
    ('Glossary Management', 'Termbase Management'),
    ('Initialize glossary', 'Initialize termbase'),
    ('Create a new glossary', 'Create a new termbase'),
    ('Add a term to a glossary', 'Add a term to a termbase'),
    ('Delete a glossary', 'Delete a termbase'),
    
    # Remaining glossary references
    (r'\bglossary\b', 'termbase'),
]

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        print(f'Skipping {filepath} - not found')
        continue
    
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    original_content = content
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE if pattern.islower() else 0)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {filepath}')
    else:
        print(f'No changes in {filepath}')

print('Terminology standardization complete!')
