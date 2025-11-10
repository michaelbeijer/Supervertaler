#!/usr/bin/env python3
"""Test adding terms to termbases"""

from modules.database_manager import DatabaseManager
from modules.termbase_manager import TermbaseManager

db = DatabaseManager()
db.connect()  # Must call connect first!
tbmgr = TermbaseManager(db, print)

# Check existing termbases
termbases = tbmgr.get_all_termbases()
print(f'Found {len(termbases)} termbases')

if len(termbases) > 0:
    # Add a term to the first termbase to test
    tb = termbases[0]
    print(f'Adding test term to {tb["name"]}')
    
    term_id = tbmgr.add_term(
        termbase_id=tb['id'],
        source_term='test',
        target_term='prueba',
        source_lang='en',
        target_lang='es'
    )
    
    if term_id:
        print(f'✓ Term added with ID {term_id}')
        
        # Verify it was added
        terms = tbmgr.get_terms(tb['id'])
        print(f'Termbase now has {len(terms)} terms')
        
        if terms:
            print(f'  - {terms[0]["source_term"]} → {terms[0]["target_term"]}')
    else:
        print('✗ Failed to add term')
else:
    print('No termbases found')

db.connection.close()
