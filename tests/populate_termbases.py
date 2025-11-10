#!/usr/bin/env python3
"""Populate test termbases with sample data"""

from modules.database_manager import DatabaseManager
from modules.termbase_manager import TermbaseManager

db = DatabaseManager()
db.connect()
tbmgr = TermbaseManager(db, print)

# Sample termbase data
termbases_data = [
    {
        "name": "Medical-NL-EN",
        "source_lang": "nl",
        "target_lang": "en",
        "description": "Medical and healthcare terminology (Dutch-English)",
        "terms": [
            ("patiënt", "patient"), ("dokter", "doctor"), ("ziekenhuis", "hospital"),
            ("diagnose", "diagnosis"), ("behandeling", "treatment"), ("chirurgie", "surgery"),
            ("medicijn", "medication"), ("bloed", "blood"), ("hartslag", "heartbeat"),
            ("ziekenhuisopname", "hospitalization"), ("genezing", "recovery"), ("operatie", "operation"),
            ("ziekte", "illness"), ("symptoom", "symptom"), ("vaccin", "vaccine"),
            ("therapie", "therapy"), ("fysiek", "physical"), ("psychisch", "mental"),
            ("rood", "red"), ("virus", "virus"), ("bacterie", "bacterium"),
            ("allergisch", "allergic"), ("gluten", "gluten"), ("lactose", "lactose"),
            ("artritis", "arthritis"), ("asthma", "asthma"), ("angst", "anxiety"),
            ("depressie", "depression"),
        ]
    },
    {
        "name": "Legal-NL-EN",
        "source_lang": "nl",
        "target_lang": "en",
        "description": "Legal and contract terminology (Dutch-English)",
        "terms": [
            ("contract", "contract"), ("handtekening", "signature"), ("clausule", "clause"),
            ("aansprakelijkheid", "liability"), ("vordering", "claim"), ("betaling", "payment"),
            ("verplicht", "mandatory"), ("verlenging", "extension"), ("herziening", "review"),
            ("beding", "provision"),
        ]
    },
    {
        "name": "Technical-NL-EN",
        "source_lang": "nl",
        "target_lang": "en",
        "description": "Technical and IT terminology (Dutch-English)",
        "terms": [
            ("software", "software"), ("hardware", "hardware"), ("netwerk", "network"),
            ("database", "database"), ("server", "server"), ("client", "client"),
            ("algoritme", "algorithm"), ("fout", "error"), ("bug", "bug"),
            ("patch", "patch"),
        ]
    }
]

print("Creating termbases and adding sample data...")
print("=" * 60)

for tb_data in termbases_data:
    # Create termbase
    tb_id = tbmgr.create_termbase(
        name=tb_data["name"],
        source_lang=tb_data["source_lang"],
        target_lang=tb_data["target_lang"],
        description=tb_data["description"],
        is_global=True
    )
    
    if tb_id:
        print(f"\n✓ Created: {tb_data['name']} (ID: {tb_id})")
        
        # Add terms
        for source, target in tb_data["terms"]:
            term_id = tbmgr.add_term(
                termbase_id=tb_id,
                source_term=source,
                target_term=target,
                source_lang=tb_data["source_lang"],
                target_lang=tb_data["target_lang"],
                priority=1
            )
            if not term_id:
                print(f"  ✗ Failed to add: {source} → {target}")
        
        # Verify
        terms = tbmgr.get_terms(tb_id)
        print(f"  Added {len(terms)} terms")
    else:
        print(f"✗ Failed to create: {tb_data['name']}")

print("\n" + "=" * 60)
print("Population complete!")

db.connection.close()
