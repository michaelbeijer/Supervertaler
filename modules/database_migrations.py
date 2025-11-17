"""
Database Migration Functions

Handles schema updates and data migrations for the Supervertaler database.
"""

import sqlite3
from typing import Optional


def migrate_termbase_fields(db_manager) -> bool:
    """
    Migrate termbase_terms table to add new fields:
    - project (TEXT)
    - client (TEXT)
    - term_uuid (TEXT UNIQUE) - for tracking terms across import/export
    
    Note: 'notes' field already exists in schema, 'definition' is legacy (no longer used)
    
    Args:
        db_manager: DatabaseManager instance
        
    Returns:
        True if migration successful
    """
    try:
        cursor = db_manager.cursor
        
        # Check which columns exist
        cursor.execute("PRAGMA table_info(termbase_terms)")
        columns = {row[1] for row in cursor.fetchall()}
        
        migrations_needed = []
        
        # Add 'project' column if it doesn't exist
        if 'project' not in columns:
            migrations_needed.append(("project", "ALTER TABLE termbase_terms ADD COLUMN project TEXT"))
        
        # Add 'client' column if it doesn't exist
        if 'client' not in columns:
            migrations_needed.append(("client", "ALTER TABLE termbase_terms ADD COLUMN client TEXT"))
        
        # Add 'term_uuid' column if it doesn't exist
        # Note: SQLite doesn't allow adding UNIQUE constraint via ALTER TABLE,
        # so we add column first, then create unique index separately
        if 'term_uuid' not in columns:
            migrations_needed.append(("term_uuid", "ALTER TABLE termbase_terms ADD COLUMN term_uuid TEXT"))
        
        # Execute migrations
        for column_name, sql in migrations_needed:
            print(f"📊 Adding column '{column_name}' to termbase_terms...")
            cursor.execute(sql)
            print(f"  ✓ Column '{column_name}' added successfully")
        
        # Create UNIQUE index for term_uuid if column was added
        if 'term_uuid' in [name for name, _ in migrations_needed]:
            print("📊 Creating UNIQUE index for term_uuid...")
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_termbase_term_uuid 
                ON termbase_terms(term_uuid)
            """)
            print("  ✓ UNIQUE index created successfully")
        
        db_manager.connection.commit()
        
        if migrations_needed:
            print(f"✅ Database migration completed: {len(migrations_needed)} column(s) added")
        else:
            print("✅ Database schema is up to date")
        
        return True
        
    except Exception as e:
        print(f"❌ Database migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_synonyms_table(db_manager) -> bool:
    """
    Create termbase_synonyms table for storing term synonyms.
    
    Schema:
    - id: Primary key
    - term_id: Foreign key to termbase_terms
    - synonym_text: The synonym text
    - language: 'source' or 'target'
    - created_date: Timestamp
    
    Args:
        db_manager: DatabaseManager instance
        
    Returns:
        True if successful
    """
    try:
        cursor = db_manager.cursor
        
        # Check if table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='termbase_synonyms'
        """)
        
        if cursor.fetchone():
            print("✅ termbase_synonyms table already exists")
            return True
        
        print("📊 Creating termbase_synonyms table...")
        
        cursor.execute("""
            CREATE TABLE termbase_synonyms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term_id INTEGER NOT NULL,
                synonym_text TEXT NOT NULL,
                language TEXT NOT NULL CHECK(language IN ('source', 'target')),
                created_date TEXT DEFAULT (datetime('now')),
                modified_date TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (term_id) REFERENCES termbase_terms(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for fast lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_synonyms_term_id 
            ON termbase_synonyms(term_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_synonyms_text 
            ON termbase_synonyms(synonym_text)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_synonyms_language 
            ON termbase_synonyms(language)
        """)
        
        db_manager.connection.commit()
        print("✅ termbase_synonyms table created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create termbase_synonyms table: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_migrations(db_manager) -> bool:
    """
    Run all pending database migrations.
    
    Args:
        db_manager: DatabaseManager instance
        
    Returns:
        True if all migrations successful
    """
    print("\n" + "="*60)
    print("DATABASE MIGRATIONS")
    print("="*60)
    
    success = True
    
    # Migration 1: Add new termbase fields
    if not migrate_termbase_fields(db_manager):
        success = False
    
    # Migration 2: Create synonyms table
    if not create_synonyms_table(db_manager):
        success = False
    
    print("="*60)
    
    return success


def check_and_migrate(db_manager) -> bool:
    """
    Check if migrations are needed and run them if so.
    This is safe to call on every app startup.
    
    Args:
        db_manager: DatabaseManager instance
        
    Returns:
        True if migrations successful or not needed
    """
    try:
        print("🔍 Checking database schema for migrations...")
        cursor = db_manager.cursor
        
        # Quick check: do we need migrations?
        cursor.execute("PRAGMA table_info(termbase_terms)")
        columns = {row[1] for row in cursor.fetchall()}
        print(f"🔍 Found termbase_terms columns: {sorted(columns)}")
        
        needs_migration = (
            'project' not in columns or 
            'client' not in columns or
            'term_uuid' not in columns
        )
        
        # Check if synonyms table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='termbase_synonyms'
        """)
        needs_synonyms_table = cursor.fetchone() is None
        
        if needs_migration:
            print(f"⚠️ Migration needed - missing columns: {', '.join([c for c in ['project', 'client', 'term_uuid'] if c not in columns])}")
        
        if needs_synonyms_table:
            print("⚠️ Migration needed - termbase_synonyms table missing")
        
        if needs_migration or needs_synonyms_table:
            success = run_all_migrations(db_manager)
            if success:
                # Generate UUIDs for terms that don't have them
                generate_missing_uuids(db_manager)
            return success
        
        # Even if no schema migration needed, check for missing UUIDs
        print("✅ Database schema is current - checking UUIDs...")
        generate_missing_uuids(db_manager)
        
        return True
        
    except Exception as e:
        print(f"❌ Migration check failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_missing_uuids(db_manager) -> bool:
    """
    Generate UUIDs for any termbase terms that don't have them.
    This ensures all existing terms get UUIDs after the term_uuid column is added.
    
    Args:
        db_manager: DatabaseManager instance
        
    Returns:
        True if successful
    """
    try:
        import uuid
        cursor = db_manager.cursor
        
        # Find terms without UUIDs
        cursor.execute("""
            SELECT id FROM termbase_terms 
            WHERE term_uuid IS NULL OR term_uuid = ''
        """)
        terms_without_uuid = cursor.fetchall()
        
        if not terms_without_uuid:
            return True  # Nothing to do
        
        print(f"📊 Generating UUIDs for {len(terms_without_uuid)} existing terms...")
        
        # Generate and assign UUIDs
        for (term_id,) in terms_without_uuid:
            term_uuid = str(uuid.uuid4())
            cursor.execute("""
                UPDATE termbase_terms 
                SET term_uuid = ? 
                WHERE id = ?
            """, (term_uuid, term_id))
        
        db_manager.connection.commit()
        print(f"  ✓ Generated {len(terms_without_uuid)} UUIDs successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ UUID generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
