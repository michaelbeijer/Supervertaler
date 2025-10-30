"""
Sample Termbase Data - Medical Dutch-English

Populates the database with a sample termbase to demonstrate functionality.
Run this to test the termbase system.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.database_manager import DatabaseManager
from modules.termbase_manager import TermbaseManager


def create_sample_termbases():
    """Create sample termbases with test data"""
    
    # Initialize database
    db_path = "user_data/supervertaler.db"
    db_manager = DatabaseManager(db_path)
    db_manager.connect()
    
    termbase_mgr = TermbaseManager(db_manager)
    
    print("\n" + "="*60)
    print("CREATING SAMPLE TERMBASES")
    print("="*60)
    
    # ========================================================================
    # SAMPLE 1: Medical Terminology (Dutch-English)
    # ========================================================================
    
    print("\n[1] Creating Medical Termbase (NL → EN)...")
    
    medical_tb_id = termbase_mgr.create_termbase(
        name="Medical-NL-EN",
        source_lang="nl",
        target_lang="en",
        description="Medical and healthcare terminology (Dutch-English)",
        is_global=True
    )
    
    if medical_tb_id:
        medical_terms = [
            # High priority terms (1-10)
            ("totale lichaamscan", "total body scan", 1, "Diagnostic Imaging", "Complete body radiological examination"),
            ("hele lichaamscan", "whole body scan", 1, "Diagnostic Imaging", "Comprehensive body imaging"),
            ("ECG-poort scan", "ECG-gated scan", 2, "Diagnostic Imaging", "Scan synchronized with cardiac rhythm"),
            ("myocardinfarct", "myocardial infarction", 1, "Cardiology", "Heart attack"),
            ("dynamische scan", "dynamic scan", 2, "Diagnostic Imaging", "Real-time imaging"),
            
            # Medium priority terms (20-50)
            ("scanmodus", "scan mode", 25, "Diagnostic Imaging", "Scanning technique setting"),
            ("scanbesturings software", "scan control software", 30, "Equipment", "Software for scan operation"),
            ("virusscaninstellingen", "virus scanning settings", 35, "Equipment", "Configuration for infection detection"),
            ("contrastversterkde scan", "contrast-enhanced scan", 20, "Diagnostic Imaging", "Imaging with contrast agent"),
            ("scannerruimte", "scanning room", 40, "Facilities", "Area where scanning occurs"),
            ("abdominale scan", "abdominal scan", 25, "Diagnostic Imaging", "Imaging of abdominal region"),
            
            # Additional medical terms
            ("patiënttabel", "patient table", 30, "Equipment", "Table where patient lies during scan"),
            ("scanneropening", "scanner aperture", 35, "Equipment", "Opening of scanning device"),
            ("stralingsdosis", "radiation dose", 20, "Safety", "Amount of radiation exposure"),
            ("CT-getal", "Hounsfield unit", 40, "Diagnostic Imaging", "Measurement of X-ray density"),
            ("axiale afbeelding", "axial image", 25, "Diagnostic Imaging", "Horizontal cross-section image"),
            ("sagittale afbeelding", "sagittal image", 25, "Diagnostic Imaging", "Side-to-side cross-section"),
            ("coronale afbeelding", "coronal image", 25, "Diagnostic Imaging", "Front-to-back cross-section"),
            ("reconstructie", "reconstruction", 30, "Image Processing", "Building 3D image from slices"),
            ("artefact", "artifact", 35, "Image Quality", "Unwanted distortion in image"),
            ("ruis", "noise", 35, "Image Quality", "Background interference in image"),
            ("spatiale resolutie", "spatial resolution", 30, "Image Quality", "Level of detail in image"),
            ("contrastresolutie", "contrast resolution", 30, "Image Quality", "Ability to distinguish different tissues"),
            ("temporale resolutie", "temporal resolution", 30, "Image Quality", "Time-based detail capability"),
            ("windowing", "windowing", 40, "Image Processing", "Adjusting image contrast and brightness"),
            ("level", "level", 40, "Image Processing", "Center point of image brightness adjustment"),
            ("breedte", "width", 40, "Image Processing", "Range of image brightness adjustment"),
        ]
        
        for source, target, priority, domain, definition in medical_terms:
            termbase_mgr.add_term(
                termbase_id=medical_tb_id,
                source_term=source,
                target_term=target,
                priority=priority,
                domain=domain,
                definition=definition,
                source_lang="nl",
                target_lang="en"
            )
        
        print(f"✓ Created Medical termbase with {len(medical_terms)} terms")
    
    # ========================================================================
    # SAMPLE 2: Legal Terminology (Dutch-English)
    # ========================================================================
    
    print("\n[2] Creating Legal Termbase (NL → EN)...")
    
    legal_tb_id = termbase_mgr.create_termbase(
        name="Legal-NL-EN",
        source_lang="nl",
        target_lang="en",
        description="Legal and contract terminology (Dutch-English)",
        is_global=True
    )
    
    if legal_tb_id:
        legal_terms = [
            ("geldende overeenkomst", "binding agreement", 1, "Contract", "Agreement that has legal force"),
            ("partijen", "parties", 2, "Legal", "Entities involved in contract"),
            ("voorwaarden", "terms and conditions", 1, "Contract", "Rules in agreement"),
            ("artikel", "clause", 2, "Legal", "Section of legal document"),
            ("bijlage", "appendix", 30, "Document", "Attached additional information"),
            ("handtekening", "signature", 1, "Contract", "Authorized mark of agreement"),
            ("getekende verklaring", "signed statement", 25, "Legal", "Formal declaration with signature"),
            ("aanvang datum", "commencement date", 20, "Contract", "Start date of agreement"),
            ("vervaldatum", "expiration date", 20, "Contract", "End date of agreement"),
            ("verlenging", "renewal", 25, "Contract", "Extension of agreement period"),
        ]
        
        for source, target, priority, domain, definition in legal_terms:
            termbase_mgr.add_term(
                termbase_id=legal_tb_id,
                source_term=source,
                target_term=target,
                priority=priority,
                domain=domain,
                definition=definition,
                source_lang="nl",
                target_lang="en"
            )
        
        print(f"✓ Created Legal termbase with {len(legal_terms)} terms")
    
    # ========================================================================
    # SAMPLE 3: Technical Terminology (Dutch-English)
    # ========================================================================
    
    print("\n[3] Creating Technical Termbase (NL → EN)...")
    
    tech_tb_id = termbase_mgr.create_termbase(
        name="Technical-NL-EN",
        source_lang="nl",
        target_lang="en",
        description="Technical and IT terminology (Dutch-English)",
        is_global=True
    )
    
    if tech_tb_id:
        tech_terms = [
            ("software", "software", 1, "IT", "Computer programs"),
            ("hardware", "hardware", 1, "IT", "Physical computer parts"),
            ("netwerk", "network", 2, "IT", "Connected computers"),
            ("server", "server", 2, "IT", "Central computer"),
            ("cliënt", "client", 2, "IT", "User computer"),
            ("database", "database", 2, "IT", "Organized data storage"),
            ("backup", "backup", 3, "IT", "Data copy for recovery"),
            ("firewall", "firewall", 3, "Security", "Network security system"),
            ("encryptie", "encryption", 3, "Security", "Converting data to code"),
            ("gebruiker", "user", 1, "IT", "Person operating system"),
        ]
        
        for source, target, priority, domain, definition in tech_terms:
            termbase_mgr.add_term(
                termbase_id=tech_tb_id,
                source_term=source,
                target_term=target,
                priority=priority,
                domain=domain,
                definition=definition,
                source_lang="nl",
                target_lang="en"
            )
        
        print(f"✓ Created Technical termbase with {len(tech_terms)} terms")
    
    print("\n" + "="*60)
    print("SAMPLE TERMBASES CREATED SUCCESSFULLY!")
    print("="*60)
    print("\nYou can now:")
    print("1. Open the 'Termbases' tab in Supervertaler")
    print("2. See the three sample termbases listed")
    print("3. Activate them for your current project")
    print("4. When translating, termbases will appear in the Assistance Panel")
    print("5. Use Ctrl+1-9 to insert termbase matches into your translation")
    print("\n")


if __name__ == "__main__":
    create_sample_termbases()
