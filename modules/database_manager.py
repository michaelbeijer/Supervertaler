"""
Database Manager Module

SQLite database backend for Translation Memories, Glossaries, and related resources.
Replaces in-memory JSON-based storage with efficient database storage.

Schema includes:
- Translation units (TM entries)
- Termbase terms
- Non-translatables
- Segmentation rules
- Project metadata
- Resource file references
"""

import sqlite3
import os
import json
import hashlib
import unicodedata
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from difflib import SequenceMatcher


def _normalize_for_matching(text: str) -> str:
    """Normalize text for exact matching.

    Handles invisible differences that would cause exact match to fail:
    - Unicode normalization (NFC)
    - Multiple whitespace -> single space
    - Leading/trailing whitespace
    - Non-breaking spaces -> regular spaces
    """
    if not text:
        return ""
    # Unicode normalize (NFC form)
    text = unicodedata.normalize('NFC', text)
    # Convert non-breaking spaces and other whitespace to regular space
    text = text.replace('\u00a0', ' ')  # NBSP
    text = text.replace('\u2007', ' ')  # Figure space
    text = text.replace('\u202f', ' ')  # Narrow NBSP
    # Collapse multiple whitespace to single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


class DatabaseManager:
    """Manages SQLite database for translation resources"""
    
    def __init__(self, db_path: str = None, log_callback=None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file (default: user_data/supervertaler.db)
            log_callback: Optional logging function
        """
        self.log = log_callback if log_callback else print
        
        # Set default database path if not provided
        if db_path is None:
            # Will be set by application - defaults to user_data folder
            self.db_path = "supervertaler.db"
        else:
            self.db_path = db_path
        
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to database and create tables if needed"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else ".", exist_ok=True)
            
            # Connect to database
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Access columns by name
            self.cursor = self.connection.cursor()
            
            # Enable foreign keys
            self.cursor.execute("PRAGMA foreign_keys = ON")
            
            # Create tables
            self._create_tables()
            
            # Run database migrations (adds new columns/tables as needed)
            try:
                from modules.database_migrations import check_and_migrate
                migration_success = check_and_migrate(self)
                if not migration_success:
                    self.log("[WARNING] Database migration reported failure")
            except Exception as e:
                self.log(f"[WARNING] Database migration check failed: {e}")
                import traceback
                traceback.print_exc()
            
            # Auto-sync FTS5 index if out of sync
            try:
                fts_status = self.check_fts_index()
                if not fts_status.get('in_sync', True):
                    self.log(f"[TM] FTS5 index out of sync ({fts_status.get('fts_count', 0)} vs {fts_status.get('main_count', 0)}), rebuilding...")
                    self.rebuild_fts_index()
            except Exception as e:
                self.log(f"[WARNING] FTS5 index check failed: {e}")
            
            self.log(f"[OK] Database connected: {os.path.basename(self.db_path)}")
            return True
            
        except Exception as e:
            self.log(f"[ERROR] Database connection failed: {e}")
            return False
    
    def _create_tables(self):
        """Create database schema"""
        print("📊 Creating database tables...")
        
        # ============================================
        # TRANSLATION MEMORY TABLES
        # ============================================
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS translation_units (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT NOT NULL,
                target_text TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                tm_id TEXT NOT NULL,
                project_id TEXT,
                
                -- Context for better matching
                context_before TEXT,
                context_after TEXT,
                
                -- Fast exact matching
                source_hash TEXT NOT NULL,
                
                -- Metadata
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usage_count INTEGER DEFAULT 0,
                created_by TEXT,
                notes TEXT,
                
                -- Indexes
                UNIQUE(source_hash, target_text, tm_id)
            )
        """)
        
        # Indexes for translation_units
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tu_source_hash 
            ON translation_units(source_hash)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tu_tm_id 
            ON translation_units(tm_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tu_project_id 
            ON translation_units(project_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tu_langs 
            ON translation_units(source_lang, target_lang)
        """)
        
        # Full-text search for fuzzy matching
        self.cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS translation_units_fts 
            USING fts5(
                source_text, 
                target_text,
                content=translation_units,
                content_rowid=id
            )
        """)
        
        # Triggers to keep FTS index in sync
        self.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS tu_fts_insert AFTER INSERT ON translation_units BEGIN
                INSERT INTO translation_units_fts(rowid, source_text, target_text)
                VALUES (new.id, new.source_text, new.target_text);
            END
        """)
        
        self.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS tu_fts_delete AFTER DELETE ON translation_units BEGIN
                DELETE FROM translation_units_fts WHERE rowid = old.id;
            END
        """)
        
        self.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS tu_fts_update AFTER UPDATE ON translation_units BEGIN
                DELETE FROM translation_units_fts WHERE rowid = old.id;
                INSERT INTO translation_units_fts(rowid, source_text, target_text)
                VALUES (new.id, new.source_text, new.target_text);
            END
        """)
        
        # ============================================
        # TRANSLATION MEMORY METADATA
        # ============================================
        
        # Translation Memories table - tracks individual TM names/metadata
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS translation_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                source_lang TEXT,
                target_lang TEXT,
                tm_id TEXT NOT NULL UNIQUE,  -- The tm_id used in translation_units table
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                entry_count INTEGER DEFAULT 0,  -- Cached count, updated on changes
                last_used TIMESTAMP,
                is_project_tm BOOLEAN DEFAULT 0,  -- Whether this is the special project TM
                read_only BOOLEAN DEFAULT 1,  -- Whether this TM should not be updated (default: read-only, Write unchecked)
                project_id INTEGER  -- Which project this TM belongs to (NULL = global)
            )
        """)
        
        # TM activation (tracks which TMs are active for which projects)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tm_activation (
                tm_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                activated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (tm_id, project_id),
                FOREIGN KEY (tm_id) REFERENCES translation_memories(id) ON DELETE CASCADE
            )
        """)
        
        # Index for fast tm_id lookups
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tm_tm_id 
            ON translation_memories(tm_id)
        """)
        
        # Migration: Add is_project_tm, read_only, and project_id columns if they don't exist
        try:
            self.cursor.execute("PRAGMA table_info(translation_memories)")
            columns = [row[1] for row in self.cursor.fetchall()]
            
            if 'is_project_tm' not in columns:
                self.cursor.execute("ALTER TABLE translation_memories ADD COLUMN is_project_tm BOOLEAN DEFAULT 0")
                print("✓ Added is_project_tm column to translation_memories")
            
            if 'read_only' not in columns:
                self.cursor.execute("ALTER TABLE translation_memories ADD COLUMN read_only BOOLEAN DEFAULT 1")
                print("✓ Added read_only column to translation_memories (default: read-only)")
            
            if 'project_id' not in columns:
                self.cursor.execute("ALTER TABLE translation_memories ADD COLUMN project_id INTEGER")
                print("✓ Added project_id column to translation_memories")
            
            self.connection.commit()
        except Exception as e:
            print(f"Migration info: {e}")
        
        # ============================================
        # TERMBASE TABLES
        # ============================================
        
        # Termbases container table (terminology, never "termbase")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS termbases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                source_lang TEXT,
                target_lang TEXT,
                project_id INTEGER,  -- NULL = global, set = project-specific
                is_global BOOLEAN DEFAULT 1,
                is_project_termbase BOOLEAN DEFAULT 0,  -- True if this is a project-specific termbase
                priority INTEGER DEFAULT 50,  -- DEPRECATED: Use ranking instead
                ranking INTEGER,  -- Termbase activation ranking: 1 = highest priority, 2 = second highest, etc. Only for activated termbases.
                read_only BOOLEAN DEFAULT 1,  -- Whether this termbase should not be updated (default: read-only, Write unchecked)
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Migration: Add priority column if it doesn't exist (for existing databases)
        try:
            self.cursor.execute("ALTER TABLE termbases ADD COLUMN priority INTEGER DEFAULT 50")
            self.connection.commit()
        except Exception:
            # Column already exists, ignore
            pass
        
        # Migration: Add is_project_termbase column if it doesn't exist
        try:
            self.cursor.execute("ALTER TABLE termbases ADD COLUMN is_project_termbase BOOLEAN DEFAULT 0")
            self.connection.commit()
        except Exception:
            # Column already exists, ignore
            pass
        
        # Migration: Add ranking column if it doesn't exist
        try:
            self.cursor.execute("ALTER TABLE termbases ADD COLUMN ranking INTEGER")
            self.connection.commit()
        except Exception:
            # Column already exists, ignore
            pass
        
        # Migration: Add read_only column if it doesn't exist
        try:
            self.cursor.execute("ALTER TABLE termbases ADD COLUMN read_only BOOLEAN DEFAULT 1")
            self.connection.commit()
        except Exception:
            # Column already exists, ignore
            pass

        # Data Migration: Set is_project_termbase=1 for termbases with non-NULL project_id
        # This ensures existing project termbases are correctly flagged
        try:
            self.cursor.execute("""
                UPDATE termbases
                SET is_project_termbase = 1
                WHERE project_id IS NOT NULL
                AND (is_project_termbase IS NULL OR is_project_termbase = 0)
            """)
            updated_count = self.cursor.rowcount
            if updated_count > 0:
                self.log(f"✅ Data migration: Updated {updated_count} project termbase(s) with is_project_termbase=1")
            self.connection.commit()
        except Exception as e:
            self.log(f"⚠️ Data migration warning (is_project_termbase): {e}")
            pass

        # Legacy support: create glossaries as alias for termbases
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS glossaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                source_lang TEXT,
                target_lang TEXT,
                project_id INTEGER,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Termbase activation (tracks which termbases are active for which projects)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS termbase_activation (
                termbase_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                activated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                priority INTEGER,  -- Manual priority (1=highest, 2=second, etc.). Multiple termbases can share same priority.
                PRIMARY KEY (termbase_id, project_id),
                FOREIGN KEY (termbase_id) REFERENCES termbases(id) ON DELETE CASCADE
            )
        """)
        
        # Migration: Add priority column to termbase_activation if it doesn't exist
        try:
            self.cursor.execute("ALTER TABLE termbase_activation ADD COLUMN priority INTEGER")
            self.connection.commit()
        except Exception:
            # Column already exists, ignore
            pass
        
        # Legacy support: termbase_project_activation as alias
        # Note: Foreign key now references termbases for consistency with Qt version
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS termbase_project_activation (
                termbase_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                activated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (termbase_id, project_id),
                FOREIGN KEY (termbase_id) REFERENCES termbases(id) ON DELETE CASCADE
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS termbase_terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_term TEXT NOT NULL,
                target_term TEXT NOT NULL,
                source_lang TEXT DEFAULT 'unknown',
                target_lang TEXT DEFAULT 'unknown',
                termbase_id TEXT NOT NULL,
                priority INTEGER DEFAULT 99,
                project_id TEXT,
                
                -- Terminology-specific fields
                synonyms TEXT,
                forbidden_terms TEXT,
                definition TEXT,
                context TEXT,
                part_of_speech TEXT,
                domain TEXT,
                case_sensitive BOOLEAN DEFAULT 0,
                forbidden BOOLEAN DEFAULT 0,
                
                -- Link to TM entry (optional)
                tm_source_id INTEGER,
                
                -- Metadata
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usage_count INTEGER DEFAULT 0,
                notes TEXT,
                note TEXT,
                project TEXT,
                client TEXT,
                term_uuid TEXT,
                
                FOREIGN KEY (tm_source_id) REFERENCES translation_units(id) ON DELETE SET NULL
            )
        """)
        
        # Indexes for termbase_terms
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gt_source_term 
            ON termbase_terms(source_term)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gt_termbase_id 
            ON termbase_terms(termbase_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gt_project_id 
            ON termbase_terms(project_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gt_domain 
            ON termbase_terms(domain)
        """)
        
        # Full-text search for termbase
        self.cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS termbase_terms_fts 
            USING fts5(
                source_term,
                target_term,
                definition,
                content=termbase_terms,
                content_rowid=id
            )
        """)
        
        # ============================================
        # NON-TRANSLATABLES
        # ============================================
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS non_translatables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT NOT NULL UNIQUE,
                pattern_type TEXT DEFAULT 'regex',
                description TEXT,
                project_id TEXT,
                enabled BOOLEAN DEFAULT 1,
                example_text TEXT,
                category TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_nt_project_id 
            ON non_translatables(project_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_nt_category 
            ON non_translatables(category)
        """)
        
        # ============================================
        # SEGMENTATION RULES
        # ============================================
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS segmentation_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_name TEXT NOT NULL,
                source_lang TEXT,
                rule_type TEXT NOT NULL,
                pattern TEXT NOT NULL,
                description TEXT,
                priority INTEGER DEFAULT 100,
                enabled BOOLEAN DEFAULT 1,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sr_source_lang 
            ON segmentation_rules(source_lang)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sr_priority 
            ON segmentation_rules(priority)
        """)
        
        # ============================================
        # PROJECT METADATA
        # ============================================
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                source_lang TEXT,
                target_lang TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_opened TIMESTAMP,
                
                -- Linked resources (JSON arrays)
                active_tm_ids TEXT,
                active_termbase_ids TEXT,
                active_prompt_file TEXT,
                active_style_guide TEXT,
                
                -- Statistics
                segment_count INTEGER DEFAULT 0,
                translated_count INTEGER DEFAULT 0,
                
                -- Settings (JSON blob)
                settings TEXT
            )
        """)
        
        # ============================================
        # FILE METADATA (for prompts and style guides)
        # ============================================
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,
                file_type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                last_used TIMESTAMP,
                use_count INTEGER DEFAULT 0
            )
        """)
        
        # ============================================
        # TMX EDITOR TABLES (for database-backed TMX files)
        # ============================================
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tmx_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,
                file_name TEXT NOT NULL,
                original_file_path TEXT,  -- Original file path when imported
                load_mode TEXT NOT NULL,  -- 'ram' or 'database'
                file_size INTEGER,  -- File size in bytes
                
                -- Header metadata (JSON)
                header_data TEXT NOT NULL,
                
                -- Statistics
                tu_count INTEGER DEFAULT 0,
                languages TEXT,  -- JSON array of language codes
                
                -- Timestamps
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tmx_translation_units (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tmx_file_id INTEGER NOT NULL,
                tu_id INTEGER NOT NULL,  -- Original TU ID from TMX file
                
                -- System attributes
                creation_date TEXT,
                creation_id TEXT,
                change_date TEXT,
                change_id TEXT,
                srclang TEXT,
                
                -- Custom attributes (JSON)
                custom_attributes TEXT,
                
                -- Comments (JSON array)
                comments TEXT,
                
                FOREIGN KEY (tmx_file_id) REFERENCES tmx_files(id) ON DELETE CASCADE,
                UNIQUE(tmx_file_id, tu_id)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tmx_segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tu_id INTEGER NOT NULL,  -- References tmx_translation_units.id
                lang TEXT NOT NULL,
                text TEXT NOT NULL,
                
                -- Language-specific attributes
                creation_date TEXT,
                creation_id TEXT,
                change_date TEXT,
                change_id TEXT,
                
                FOREIGN KEY (tu_id) REFERENCES tmx_translation_units(id) ON DELETE CASCADE,
                UNIQUE(tu_id, lang)
            )
        """)
        
        # Indexes for TMX tables
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tmx_tu_file_id 
            ON tmx_translation_units(tmx_file_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tmx_tu_tu_id 
            ON tmx_translation_units(tu_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tmx_seg_tu_id 
            ON tmx_segments(tu_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tmx_seg_lang 
            ON tmx_segments(lang)
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS style_guide_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,
                language TEXT NOT NULL,
                last_used TIMESTAMP,
                use_count INTEGER DEFAULT 0
            )
        """)
        
        # Commit schema
        try:
            self.connection.commit()
            print("✅ Database tables created and committed successfully")
        except Exception as e:
            print(f"❌ Error committing database schema: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    # ============================================
    # TRANSLATION MEMORY METHODS
    # ============================================
    
    def add_translation_unit(self, source: str, target: str, source_lang: str,
                            target_lang: str, tm_id: str = 'project',
                            project_id: str = None, context_before: str = None,
                            context_after: str = None, notes: str = None,
                            overwrite: bool = False) -> int:
        """
        Add translation unit to database

        Args:
            source: Source text
            target: Target text
            source_lang: Source language code
            target_lang: Target language code
            tm_id: TM identifier
            project_id: Optional project ID
            context_before: Optional context before
            context_after: Optional context after
            notes: Optional notes
            overwrite: If True, delete existing entries with same source before inserting
                      (implements "Save only latest translation" mode)

        Returns: ID of inserted/updated entry
        """
        # Generate hash from NORMALIZED source for consistent exact matching
        # This handles invisible differences like Unicode normalization, whitespace variations
        normalized_source = _normalize_for_matching(source)
        source_hash = hashlib.md5(normalized_source.encode('utf-8')).hexdigest()

        try:
            # If overwrite mode, delete ALL existing entries with same source_hash and tm_id
            # This ensures only the latest translation is kept
            if overwrite:
                self.cursor.execute("""
                    DELETE FROM translation_units
                    WHERE source_hash = ? AND tm_id = ?
                """, (source_hash, tm_id))

            self.cursor.execute("""
                INSERT INTO translation_units
                (source_text, target_text, source_lang, target_lang, tm_id,
                 project_id, context_before, context_after, source_hash, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_hash, target_text, tm_id) DO UPDATE SET
                    usage_count = usage_count + 1,
                    modified_date = CURRENT_TIMESTAMP
            """, (source, target, source_lang, target_lang, tm_id,
                  project_id, context_before, context_after, source_hash, notes))

            self.connection.commit()
            return self.cursor.lastrowid

        except Exception as e:
            self.log(f"Error adding translation unit: {e}")
            return None
    
    def get_exact_match(self, source: str, tm_ids: List[str] = None,
                       source_lang: str = None, target_lang: str = None,
                       bidirectional: bool = True) -> Optional[Dict]:
        """
        Get exact match from TM

        Args:
            source: Source text to match
            tm_ids: List of TM IDs to search (None = all)
            source_lang: Filter by source language (base code matching: 'en' matches 'en-US', 'en-GB', etc.)
            target_lang: Filter by target language (base code matching)
            bidirectional: If True, search both directions (nl→en AND en→nl)

        Returns: Dictionary with match data or None
        """
        from modules.tmx_generator import get_base_lang_code

        # Try both normalized and non-normalized hashes for backward compatibility
        # This handles invisible differences like Unicode normalization, whitespace variations
        source_hash = hashlib.md5(source.encode('utf-8')).hexdigest()
        normalized_source = _normalize_for_matching(source)
        normalized_hash = hashlib.md5(normalized_source.encode('utf-8')).hexdigest()

        # Get base language codes for comparison
        src_base = get_base_lang_code(source_lang) if source_lang else None
        tgt_base = get_base_lang_code(target_lang) if target_lang else None

        # Search using both original hash and normalized hash
        query = """
            SELECT * FROM translation_units
            WHERE (source_hash = ? OR source_hash = ?)
        """
        params = [source_hash, normalized_hash]
        
        if tm_ids:
            placeholders = ','.join('?' * len(tm_ids))
            query += f" AND tm_id IN ({placeholders})"
            params.extend(tm_ids)
        
        # Use flexible language matching (matches 'nl', 'nl-NL', 'Dutch', etc.)
        from modules.tmx_generator import get_lang_match_variants
        if src_base:
            src_variants = get_lang_match_variants(source_lang)
            src_conditions = []
            for variant in src_variants:
                src_conditions.append("source_lang = ?")
                params.append(variant)
                src_conditions.append("source_lang LIKE ?")
                params.append(f"{variant}-%")
            query += f" AND ({' OR '.join(src_conditions)})"
        
        if tgt_base:
            tgt_variants = get_lang_match_variants(target_lang)
            tgt_conditions = []
            for variant in tgt_variants:
                tgt_conditions.append("target_lang = ?")
                params.append(variant)
                tgt_conditions.append("target_lang LIKE ?")
                params.append(f"{variant}-%")
            query += f" AND ({' OR '.join(tgt_conditions)})"
        
        query += " ORDER BY usage_count DESC, modified_date DESC LIMIT 1"
        
        self.cursor.execute(query, params)
        row = self.cursor.fetchone()
        
        if row:
            # Update usage count
            self.cursor.execute("""
                UPDATE translation_units 
                SET usage_count = usage_count + 1 
                WHERE id = ?
            """, (row['id'],))
            self.connection.commit()
            
            return dict(row)
        
        # If bidirectional and no forward match, try reverse direction
        if bidirectional and src_base and tgt_base:
            # Search where our source text is in the target field (reverse direction)
            query = """
                SELECT * FROM translation_units 
                WHERE target_text = ?
            """
            params = [source]
            
            if tm_ids:
                placeholders = ','.join('?' * len(tm_ids))
                query += f" AND tm_id IN ({placeholders})"
                params.extend(tm_ids)
            
            # Reversed: search where TM source_lang matches our target_lang (flexible matching)
            # Note: for reverse, we swap - TM source_lang should match our target_lang
            tgt_variants = get_lang_match_variants(target_lang)
            src_variants = get_lang_match_variants(source_lang)
            
            src_conditions = []
            for variant in tgt_variants:  # TM source_lang = our target_lang
                src_conditions.append("source_lang = ?")
                params.append(variant)
                src_conditions.append("source_lang LIKE ?")
                params.append(f"{variant}-%")
            
            tgt_conditions = []
            for variant in src_variants:  # TM target_lang = our source_lang
                tgt_conditions.append("target_lang = ?")
                params.append(variant)
                tgt_conditions.append("target_lang LIKE ?")
                params.append(f"{variant}-%")
            
            query += f" AND ({' OR '.join(src_conditions)}) AND ({' OR '.join(tgt_conditions)})"
            
            query += " ORDER BY usage_count DESC, modified_date DESC LIMIT 1"
            
            self.cursor.execute(query, params)
            row = self.cursor.fetchone()
            
            if row:
                # Update usage count
                self.cursor.execute("""
                    UPDATE translation_units 
                    SET usage_count = usage_count + 1 
                    WHERE id = ?
                """, (row['id'],))
                self.connection.commit()
                
                # Swap source/target since this is a reverse match
                result = dict(row)
                result['source_text'], result['target_text'] = result['target_text'], result['source_text']
                result['source_lang'], result['target_lang'] = result['target_lang'], result['source_lang']
                result['reverse_match'] = True
                return result
        
        return None
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity ratio between two texts using SequenceMatcher.
        Tags are stripped before comparison for better matching accuracy.
        
        Returns: Similarity score from 0.0 to 1.0
        """
        import re
        # Strip HTML/XML tags for comparison
        clean1 = re.sub(r'<[^>]+>', '', text1).lower()
        clean2 = re.sub(r'<[^>]+>', '', text2).lower()
        return SequenceMatcher(None, clean1, clean2).ratio()
    
    def search_fuzzy_matches(self, source: str, tm_ids: List[str] = None,
                            threshold: float = 0.75, max_results: int = 5,
                            source_lang: str = None, target_lang: str = None,
                            bidirectional: bool = True) -> List[Dict]:
        """
        Search for fuzzy matches using FTS5 with proper similarity calculation
        
        Args:
            bidirectional: If True, search both directions (nl→en AND en→nl)
        
        Returns: List of matches with similarity scores
        
        Note: When multiple TMs are provided, searches each TM separately to ensure
        good matches from smaller TMs aren't pushed out by BM25 keyword ranking
        from larger TMs. Results are merged and sorted by actual similarity.
        """
        # For better FTS5 matching, tokenize the query and escape special chars
        # FTS5 special characters: " ( ) - : , . ! ? 
        import re
        from modules.tmx_generator import get_base_lang_code, get_lang_match_variants
        
        # Strip HTML/XML tags from source for clean text search
        text_without_tags = re.sub(r'<[^>]+>', '', source)
        
        # Remove special FTS5 characters and split into words (from tag-stripped text)
        clean_text = re.sub(r'[^\w\s]', ' ', text_without_tags)  # Replace special chars with spaces
        search_terms_clean = [term for term in clean_text.strip().split() if len(term) > 2]  # Min 3 chars
        
        # Also get search terms from original source (in case TM was indexed with tags)
        clean_text_with_tags = re.sub(r'[^\w\s]', ' ', source)
        search_terms_with_tags = [term for term in clean_text_with_tags.strip().split() if len(term) > 2]
        
        # Combine both sets of search terms (deduplicated)
        all_search_terms = list(dict.fromkeys(search_terms_clean + search_terms_with_tags))
        
        # For long segments, prioritize longer/rarer words to get better FTS5 candidates
        # Sort by length (longer words are usually more discriminating)
        all_search_terms.sort(key=len, reverse=True)
        
        # Limit search terms to avoid overly complex queries (top 20 longest words)
        # This helps find similar long segments more reliably
        search_terms_for_query = all_search_terms[:20]
        
        if not search_terms_for_query:
            # If no valid terms, return empty results
            return []
        
        # Quote each term to prevent FTS5 syntax errors
        fts_query = ' OR '.join(f'"{term}"' for term in search_terms_for_query)
        
        # Get base language codes for comparison
        src_base = get_base_lang_code(source_lang) if source_lang else None
        tgt_base = get_base_lang_code(target_lang) if target_lang else None
        
        # MULTI-TM FIX: Search each TM separately to avoid BM25 ranking issues
        # When a large TM is combined with a small TM, the large TM's many keyword matches
        # push down genuinely similar sentences from the small TM
        tms_to_search = tm_ids if tm_ids else [None]  # None means search all TMs together
        
        all_results = []
        
        for tm_id in tms_to_search:
            # Search this specific TM (or all if tm_id is None)
            tm_results = self._search_single_tm_fuzzy(
                source, fts_query, [tm_id] if tm_id else None,
                threshold, max_results, src_base, tgt_base, 
                source_lang, target_lang, bidirectional
            )
            all_results.extend(tm_results)
        
        # Deduplicate by source_text (keep highest similarity for each unique source)
        seen = {}
        for result in all_results:
            key = result['source_text']
            if key not in seen or result['similarity'] > seen[key]['similarity']:
                seen[key] = result
        
        deduped_results = list(seen.values())
        
        # Sort ALL results by similarity (highest first) - this ensures the 76% match
        # appears before 40% matches regardless of which TM they came from
        deduped_results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return deduped_results[:max_results]
    
    def _search_single_tm_fuzzy(self, source: str, fts_query: str, tm_ids: List[str],
                                 threshold: float, max_results: int,
                                 src_base: str, tgt_base: str,
                                 source_lang: str, target_lang: str,
                                 bidirectional: bool) -> List[Dict]:
        """Search a single TM (or all TMs if tm_ids is None) for fuzzy matches"""
        from modules.tmx_generator import get_lang_match_variants
        
        # Build query for this TM
        query = """
            SELECT tu.*, 
                   bm25(translation_units_fts) as relevance
            FROM translation_units tu
            JOIN translation_units_fts ON tu.id = translation_units_fts.rowid
            WHERE translation_units_fts MATCH ?
        """
        params = [fts_query]
        
        if tm_ids and tm_ids[0] is not None:
            placeholders = ','.join('?' * len(tm_ids))
            query += f" AND tu.tm_id IN ({placeholders})"
            params.extend(tm_ids)
        
        # Use flexible language matching (matches 'nl', 'nl-NL', 'Dutch', etc.)
        if src_base:
            src_variants = get_lang_match_variants(source_lang)
            src_conditions = []
            for variant in src_variants:
                src_conditions.append("tu.source_lang = ?")
                params.append(variant)
                src_conditions.append("tu.source_lang LIKE ?")
                params.append(f"{variant}-%")
            query += f" AND ({' OR '.join(src_conditions)})"
        
        if tgt_base:
            tgt_variants = get_lang_match_variants(target_lang)
            tgt_conditions = []
            for variant in tgt_variants:
                tgt_conditions.append("tu.target_lang = ?")
                params.append(variant)
                tgt_conditions.append("tu.target_lang LIKE ?")
                params.append(f"{variant}-%")
            query += f" AND ({' OR '.join(tgt_conditions)})"
        
        # Per-TM candidate limit - INCREASED to catch more potential fuzzy matches
        # When multiple TMs are searched, BM25 ranking can push genuinely similar
        # entries far down the list due to common word matches in other entries
        candidate_limit = max(500, max_results * 50)
        query += f" ORDER BY relevance DESC LIMIT {candidate_limit}"
        
        try:
            self.cursor.execute(query, params)
            all_rows = self.cursor.fetchall()
        except Exception as e:
            return []
        
        results = []
        
        for row in all_rows:
            match_dict = dict(row)
            # Calculate actual similarity using SequenceMatcher
            similarity = self.calculate_similarity(source, match_dict['source_text'])
            
            # Only include matches above threshold
            if similarity >= threshold:
                match_dict['similarity'] = similarity
                match_dict['match_pct'] = int(similarity * 100)
                results.append(match_dict)
        
        # If bidirectional, also search reverse direction
        if bidirectional and src_base and tgt_base:
            query = """
                SELECT tu.*, 
                       bm25(translation_units_fts) as relevance
                FROM translation_units tu
                JOIN translation_units_fts ON tu.id = translation_units_fts.rowid
                WHERE translation_units_fts MATCH ?
            """
            params = [fts_query]
            
            if tm_ids and tm_ids[0] is not None:
                placeholders = ','.join('?' * len(tm_ids))
                query += f" AND tu.tm_id IN ({placeholders})"
                params.extend(tm_ids)
            
            # Reversed language filters with flexible matching
            src_variants = get_lang_match_variants(source_lang)
            tgt_variants = get_lang_match_variants(target_lang)
            
            # TM target_lang = our source_lang
            tgt_conditions = []
            for variant in src_variants:
                tgt_conditions.append("tu.target_lang = ?")
                params.append(variant)
                tgt_conditions.append("tu.target_lang LIKE ?")
                params.append(f"{variant}-%")
            query += f" AND ({' OR '.join(tgt_conditions)})"
            
            # TM source_lang = our target_lang  
            src_conditions = []
            for variant in tgt_variants:
                src_conditions.append("tu.source_lang = ?")
                params.append(variant)
                src_conditions.append("tu.source_lang LIKE ?")
                params.append(f"{variant}-%")
            query += f" AND ({' OR '.join(src_conditions)})"
            
            query += f" ORDER BY relevance DESC LIMIT {max_results * 5}"
            
            try:
                self.cursor.execute(query, params)
                
                for row in self.cursor.fetchall():
                    match_dict = dict(row)
                    # Calculate similarity against target_text (since we're reversing)
                    similarity = self.calculate_similarity(source, match_dict['target_text'])
                    
                    # Only include matches above threshold
                    if similarity >= threshold:
                        # Swap source/target for reverse match
                        match_dict['source_text'], match_dict['target_text'] = match_dict['target_text'], match_dict['source_text']
                        match_dict['source_lang'], match_dict['target_lang'] = match_dict['target_lang'], match_dict['source_lang']
                        match_dict['similarity'] = similarity
                        match_dict['match_pct'] = int(similarity * 100)
                        match_dict['reverse_match'] = True
                        results.append(match_dict)
            except Exception as e:
                print(f"[DEBUG] _search_single_tm_fuzzy (reverse): SQL ERROR: {e}")
        
        return results
    
    def search_all(self, source: str, tm_ids: List[str] = None, enabled_only: bool = True,
                   threshold: float = 0.75, max_results: int = 10) -> List[Dict]:
        """
        Search for matches across TMs (both exact and fuzzy)
        
        Args:
            source: Source text to search for
            tm_ids: List of TM IDs to search (None = all)
            enabled_only: Currently ignored (all TMs enabled)
            threshold: Minimum similarity threshold (0.0-1.0)
            max_results: Maximum number of results
            
        Returns:
            List of matches with source, target, match_pct, tm_name
        """
        # First try exact match
        exact = self.get_exact_match(source, tm_ids=tm_ids)
        if exact:
            return [{
                'source': exact['source_text'],
                'target': exact['target_text'],
                'match_pct': 100,
                'tm_name': exact['tm_id'].replace('_', ' ').title(),
                'tm_id': exact['tm_id']
            }]
        
        # No exact match, try fuzzy
        fuzzy_matches = self.search_fuzzy_matches(
            source, 
            tm_ids=tm_ids,
            threshold=threshold,
            max_results=max_results
        )
        
        results = []
        for match in fuzzy_matches:
            results.append({
                'source': match['source_text'],
                'target': match['target_text'],
                'match_pct': match['match_pct'],
                'tm_name': match['tm_id'].replace('_', ' ').title(),
                'tm_id': match['tm_id']
            })
        
        return results
    
    def get_tm_entries(self, tm_id: str, limit: int = None) -> List[Dict]:
        """Get all entries from a specific TM"""
        query = "SELECT * FROM translation_units WHERE tm_id = ? ORDER BY id"
        params = [tm_id]
        
        if limit:
            query += f" LIMIT {limit}"
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_tm_count(self, tm_id: str = None) -> int:
        """Get entry count for TM(s)"""
        if tm_id:
            self.cursor.execute("""
                SELECT COUNT(*) FROM translation_units WHERE tm_id = ?
            """, (tm_id,))
        else:
            self.cursor.execute("SELECT COUNT(*) FROM translation_units")
        
        return self.cursor.fetchone()[0]
    
    def clear_tm(self, tm_id: str):
        """Clear all entries from a TM"""
        self.cursor.execute("""
            DELETE FROM translation_units WHERE tm_id = ?
        """, (tm_id,))
        self.connection.commit()
    
    def delete_entry(self, tm_id: str, source: str, target: str):
        """Delete a specific entry from a TM"""
        # Get the ID first
        self.cursor.execute("""
            SELECT id FROM translation_units 
            WHERE tm_id = ? AND source_text = ? AND target_text = ?
        """, (tm_id, source, target))
        
        result = self.cursor.fetchone()
        if not result:
            return  # Entry not found
        
        entry_id = result['id']
        
        # Delete from FTS5 index first
        try:
            self.cursor.execute("""
                DELETE FROM tm_fts WHERE rowid = ?
            """, (entry_id,))
        except Exception:
            pass  # FTS5 table might not exist
        
        # Delete from main table
        self.cursor.execute("""
            DELETE FROM translation_units 
            WHERE id = ?
        """, (entry_id,))
        
        self.connection.commit()
    
    def concordance_search(self, query: str, tm_ids: List[str] = None, direction: str = 'both',
                            source_lang = None, target_lang = None) -> List[Dict]:
        """
        Search for text in source and/or target (concordance search)
        Uses FTS5 full-text search for fast matching on millions of segments.
        Falls back to LIKE queries if FTS5 fails.
        
        Language filters define what you're searching FOR and what translation you want:
        - "From: Dutch, To: English" = Search for Dutch text, show English translations
        - Searches ALL TMs (regardless of their stored language pair direction)
        - Automatically swaps columns when needed (e.g., finds Dutch in target column of EN→NL TM)
        - This is MORE intuitive than traditional CAT tools that only search specific TM directions
        
        Args:
            query: Text to search for
            tm_ids: List of TM IDs to search (None = all)
            direction: 'source' = search source only, 'target' = search target only, 'both' = bidirectional
            source_lang: Filter by source language - can be a string OR a list of language variants (None = any)
            target_lang: Filter by target language - can be a string OR a list of language variants (None = any)
        """
        # Normalize language filters to lists for consistent handling
        source_langs = source_lang if isinstance(source_lang, list) else ([source_lang] if source_lang else None)
        target_langs = target_lang if isinstance(target_lang, list) else ([target_lang] if target_lang else None)
        
        # Escape FTS5 special characters and wrap words for prefix matching
        # FTS5 special chars: " * ( ) : ^
        fts_query = query.replace('"', '""')
        # Wrap in quotes for phrase search
        fts_query = f'"{fts_query}"'
        
        # When language filters specified, we need to search intelligently:
        # - Don't filter by TM language pair (search ALL TMs)
        # - Search in BOTH columns to find text
        # - Swap columns if needed to show correct language order
        use_smart_search = (source_langs or target_langs)
        
        try:
            # Use FTS5 for fast full-text search
            if direction == 'source':
                fts_sql = """
                    SELECT tu.* FROM translation_units tu
                    JOIN translation_units_fts fts ON tu.id = fts.rowid
                    WHERE fts.source_text MATCH ?
                """
                params = [fts_query]
            elif direction == 'target':
                fts_sql = """
                    SELECT tu.* FROM translation_units tu
                    JOIN translation_units_fts fts ON tu.id = fts.rowid
                    WHERE fts.target_text MATCH ?
                """
                params = [fts_query]
            else:
                # Both directions - search in combined FTS index
                fts_sql = """
                    SELECT tu.* FROM translation_units tu
                    JOIN translation_units_fts fts ON tu.id = fts.rowid
                    WHERE translation_units_fts MATCH ?
                """
                params = [fts_query]
            
            if tm_ids:
                placeholders = ','.join('?' * len(tm_ids))
                fts_sql += f" AND tu.tm_id IN ({placeholders})"
                params.extend(tm_ids)
            
            # DON'T filter by language when smart search active
            # (we need to search all TMs and figure out which column has our language)
            if not use_smart_search:
                # Traditional filtering when no language filters
                if source_langs:
                    placeholders = ','.join('?' * len(source_langs))
                    fts_sql += f" AND tu.source_lang IN ({placeholders})"
                    params.extend(source_langs)
                if target_langs:
                    placeholders = ','.join('?' * len(target_langs))
                    fts_sql += f" AND tu.target_lang IN ({placeholders})"
                    params.extend(target_langs)
            
            fts_sql += " ORDER BY tu.modified_date DESC LIMIT 100"
            
            self.cursor.execute(fts_sql, params)
            raw_results = [dict(row) for row in self.cursor.fetchall()]
            
            # Smart search: Filter and swap based on language metadata
            if use_smart_search:
                processed_results = []
                for row in raw_results:
                    row_src_lang = row.get('source_lang', '')
                    row_tgt_lang = row.get('target_lang', '')
                    
                    # Check if this row matches our language requirements
                    # If "From: Dutch, To: English":
                    # - Accept if source=nl and target=en (normal)
                    # - Accept if source=en and target=nl (swap needed)
                    
                    matches = False
                    needs_swap = False
                    
                    if source_langs and target_langs:
                        # Both filters specified
                        if row_src_lang in source_langs and row_tgt_lang in target_langs:
                            # Perfect match - no swap
                            matches = True
                            needs_swap = False
                        elif row_src_lang in target_langs and row_tgt_lang in source_langs:
                            # Reversed - needs swap
                            matches = True
                            needs_swap = True
                    elif source_langs:
                        # Only "From" specified - just check if Dutch is in EITHER column
                        if row_src_lang in source_langs:
                            matches = True
                            needs_swap = False
                        elif row_tgt_lang in source_langs:
                            matches = True
                            needs_swap = True
                    elif target_langs:
                        # Only "To" specified - just check if English is in EITHER column
                        if row_tgt_lang in target_langs:
                            matches = True
                            needs_swap = False
                        elif row_src_lang in target_langs:
                            matches = True
                            needs_swap = True
                    
                    if matches:
                        # CRITICAL CHECK: Verify the search text is actually in the correct column
                        # If user searches for Dutch with "From: Dutch", the text must be in the source column (after any swap)
                        # This prevents finding Dutch text when user asks to search FOR English
                        
                        if needs_swap:
                            # After swap, check if query is in the NEW source column (was target)
                            text_to_check = row['target_text'].lower()
                        else:
                            # No swap, check if query is in source column
                            text_to_check = row['source_text'].lower()
                        
                        # Only include if query text is actually in the source column
                        if query.lower() in text_to_check:
                            if needs_swap:
                                # Swap columns to show correct language order
                                swapped_row = row.copy()
                                swapped_row['source'] = row['target_text']
                                swapped_row['target'] = row['source_text']
                                swapped_row['source_lang'] = row['target_lang']
                                swapped_row['target_lang'] = row['source_lang']
                                processed_results.append(swapped_row)
                            else:
                                # No swap needed - just rename columns
                                processed_row = row.copy()
                                processed_row['source'] = row['source_text']
                                processed_row['target'] = row['target_text']
                                processed_results.append(processed_row)
                
                return processed_results
            else:
                # No language filters - just rename columns
                processed_results = []
                for row in raw_results:
                    processed_row = row.copy()
                    processed_row['source'] = row['source_text']
                    processed_row['target'] = row['target_text']
                    processed_results.append(processed_row)
                return processed_results
            
        except Exception as e:
            # Fallback to LIKE query if FTS5 fails (e.g., index not built)
            print(f"[TM] FTS5 search failed, falling back to LIKE: {e}")
            search_query = f"%{query}%"
            
            if direction == 'source':
                sql = """
                    SELECT * FROM translation_units 
                    WHERE source_text LIKE ?
                """
                params = [search_query]
            elif direction == 'target':
                sql = """
                    SELECT * FROM translation_units 
                    WHERE target_text LIKE ?
                """
                params = [search_query]
            else:
                sql = """
                    SELECT * FROM translation_units 
                    WHERE (source_text LIKE ? OR target_text LIKE ?)
                """
                params = [search_query, search_query]
            
            if tm_ids:
                placeholders = ','.join('?' * len(tm_ids))
                sql += f" AND tm_id IN ({placeholders})"
                params.extend(tm_ids)
            
            # Add language filters (support for list of variants)
            if source_langs:
                placeholders = ','.join('?' * len(source_langs))
                sql += f" AND source_lang IN ({placeholders})"
                params.extend(source_langs)
            if target_langs:
                placeholders = ','.join('?' * len(target_langs))
                sql += f" AND target_lang IN ({placeholders})"
                params.extend(target_langs)
            
            sql += " ORDER BY modified_date DESC LIMIT 100"
            
            self.cursor.execute(sql, params)
            return [dict(row) for row in self.cursor.fetchall()]
    
    def rebuild_fts_index(self) -> int:
        """
        Rebuild the FTS5 full-text search index from scratch.
        Use this after importing TMs or if FTS search isn't returning results.
        
        Returns:
            Number of entries indexed
        """
        try:
            # Clear existing FTS data
            self.cursor.execute("DELETE FROM translation_units_fts")
            
            # Repopulate from translation_units table
            self.cursor.execute("""
                INSERT INTO translation_units_fts(rowid, source_text, target_text)
                SELECT id, source_text, target_text FROM translation_units
            """)
            
            self.conn.commit()
            
            # Get count
            self.cursor.execute("SELECT COUNT(*) FROM translation_units_fts")
            count = self.cursor.fetchone()[0]
            print(f"[TM] FTS5 index rebuilt with {count:,} entries")
            return count
        except Exception as e:
            print(f"[TM] Error rebuilding FTS index: {e}")
            return 0
    
    def check_fts_index(self) -> Dict:
        """
        Check if FTS5 index is in sync with main table.
        
        Returns:
            Dict with 'main_count', 'fts_count', 'in_sync' keys
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM translation_units")
            main_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM translation_units_fts")
            fts_count = self.cursor.fetchone()[0]
            
            return {
                'main_count': main_count,
                'fts_count': fts_count,
                'in_sync': main_count == fts_count
            }
        except Exception as e:
            return {'main_count': 0, 'fts_count': 0, 'in_sync': False, 'error': str(e)}

    # ============================================
    # termbase METHODS (Placeholder for Phase 3)
    # ============================================
    
    def add_termbase_term(self, source_term: str, target_term: str,
                         source_lang: str, target_lang: str,
                         termbase_id: str = 'main', **kwargs) -> int:
        """Add term to termbase (Phase 3)"""
        # TODO: Implement in Phase 3
        pass
    
    def search_termbases(self, search_term: str, source_lang: str = None,
                        target_lang: str = None, project_id: str = None,
                        min_length: int = 0, bidirectional: bool = True) -> List[Dict]:
        """
        Search termbases for matching terms (bidirectional by default)

        Args:
            search_term: Term to search for
            source_lang: Filter by source language (optional)
            target_lang: Filter by target language (optional)
            project_id: Filter by project (optional)
            min_length: Minimum term length to return
            bidirectional: If True, also search target_term and swap results (default True)

        Returns:
            List of termbase hits, sorted by priority (lower = higher priority)
            Each result includes 'match_direction' ('source' or 'target') indicating
            which column matched. For 'target' matches, source_term and target_term
            are swapped so results are always oriented correctly for the current project.
        """
        # Build query with filters - include termbase name and ranking via JOIN
        # Note: termbase_id is stored as TEXT in termbase_terms but INTEGER in termbases
        # Use CAST to ensure proper comparison
        # IMPORTANT: Join with termbase_activation to get the ACTUAL priority for this project
        # CRITICAL FIX: Also match when search_term starts with the glossary term
        # This handles cases like searching for "ca." when glossary has "ca."
        # AND searching for "ca" when glossary has "ca."
        # We also strip trailing punctuation from glossary terms for comparison

        # Build matching conditions for a given column
        def build_match_conditions(column: str) -> str:
            return f"""(
                LOWER(t.{column}) = LOWER(?) OR
                LOWER(t.{column}) LIKE LOWER(?) OR
                LOWER(t.{column}) LIKE LOWER(?) OR
                LOWER(t.{column}) LIKE LOWER(?) OR
                LOWER(RTRIM(t.{column}, '.!?,;:')) = LOWER(?) OR
                LOWER(?) LIKE LOWER(t.{column}) || '%' OR
                LOWER(?) = LOWER(RTRIM(t.{column}, '.!?,;:'))
            )"""

        # Build match params for one direction
        def build_match_params() -> list:
            return [
                search_term,
                f"{search_term} %",
                f"% {search_term}",
                f"% {search_term} %",
                search_term,  # For RTRIM comparison
                search_term,  # For reverse LIKE
                search_term   # For reverse RTRIM comparison
            ]

        # Matching patterns:
        # 1. Exact match: column = search_term
        # 2. Glossary term starts with search: column LIKE "search_term %"
        # 3. Glossary term ends with search: column LIKE "% search_term"
        # 4. Glossary term contains search: column LIKE "% search_term %"
        # 5. Glossary term (stripped) = search_term: RTRIM(column) = search_term (handles "ca." = "ca")
        # 6. Search starts with glossary term: search_term LIKE column || '%'
        # 7. Search = glossary term stripped: search_term = RTRIM(column)

        # Base SELECT for forward matches (source_term matches)
        base_select_forward = """
            SELECT
                t.id, t.source_term, t.target_term, t.termbase_id, t.priority,
                t.forbidden, t.source_lang, t.target_lang, t.definition, t.domain,
                t.notes, t.project, t.client,
                tb.name as termbase_name,
                tb.source_lang as termbase_source_lang,
                tb.target_lang as termbase_target_lang,
                tb.is_project_termbase,
                COALESCE(ta.priority, tb.ranking) as ranking,
                'source' as match_direction
            FROM termbase_terms t
            LEFT JOIN termbases tb ON CAST(t.termbase_id AS INTEGER) = tb.id
            LEFT JOIN termbase_activation ta ON ta.termbase_id = tb.id AND ta.project_id = ? AND ta.is_active = 1
            WHERE {match_conditions}
            AND (ta.is_active = 1 OR tb.is_project_termbase = 1)
        """.format(match_conditions=build_match_conditions('source_term'))

        # Base SELECT for reverse matches (target_term matches) - swap source/target in output
        base_select_reverse = """
            SELECT
                t.id, t.target_term as source_term, t.source_term as target_term,
                t.termbase_id, t.priority,
                t.forbidden, t.target_lang as source_lang, t.source_lang as target_lang,
                t.definition, t.domain,
                t.notes, t.project, t.client,
                tb.name as termbase_name,
                tb.target_lang as termbase_source_lang,
                tb.source_lang as termbase_target_lang,
                tb.is_project_termbase,
                COALESCE(ta.priority, tb.ranking) as ranking,
                'target' as match_direction
            FROM termbase_terms t
            LEFT JOIN termbases tb ON CAST(t.termbase_id AS INTEGER) = tb.id
            LEFT JOIN termbase_activation ta ON ta.termbase_id = tb.id AND ta.project_id = ? AND ta.is_active = 1
            WHERE {match_conditions}
            AND (ta.is_active = 1 OR tb.is_project_termbase = 1)
        """.format(match_conditions=build_match_conditions('target_term'))

        # Build params
        project_param = project_id if project_id else 0
        forward_params = [project_param] + build_match_params()
        reverse_params = [project_param] + build_match_params()

        # Build language filter conditions
        lang_conditions_forward = ""
        lang_conditions_reverse = ""
        lang_params_forward = []
        lang_params_reverse = []

        if source_lang:
            # For forward: filter on source_lang
            lang_conditions_forward += """ AND (
                t.source_lang = ? OR
                (t.source_lang IS NULL AND tb.source_lang = ?) OR
                (t.source_lang IS NULL AND tb.source_lang IS NULL)
            )"""
            lang_params_forward.extend([source_lang, source_lang])
            # For reverse: source_lang becomes target_lang (swapped)
            lang_conditions_reverse += """ AND (
                t.target_lang = ? OR
                (t.target_lang IS NULL AND tb.target_lang = ?) OR
                (t.target_lang IS NULL AND tb.target_lang IS NULL)
            )"""
            lang_params_reverse.extend([source_lang, source_lang])

        if target_lang:
            # For forward: filter on target_lang
            lang_conditions_forward += """ AND (
                t.target_lang = ? OR
                (t.target_lang IS NULL AND tb.target_lang = ?) OR
                (t.target_lang IS NULL AND tb.target_lang IS NULL)
            )"""
            lang_params_forward.extend([target_lang, target_lang])
            # For reverse: target_lang becomes source_lang (swapped)
            lang_conditions_reverse += """ AND (
                t.source_lang = ? OR
                (t.source_lang IS NULL AND tb.source_lang = ?) OR
                (t.source_lang IS NULL AND tb.source_lang IS NULL)
            )"""
            lang_params_reverse.extend([target_lang, target_lang])

        # Project filter conditions
        project_conditions = ""
        project_params = []
        if project_id:
            project_conditions = " AND (t.project_id = ? OR t.project_id IS NULL)"
            project_params = [project_id]

        # Min length conditions
        min_len_forward = ""
        min_len_reverse = ""
        if min_length > 0:
            min_len_forward = f" AND LENGTH(t.source_term) >= {min_length}"
            min_len_reverse = f" AND LENGTH(t.target_term) >= {min_length}"

        # Build forward query
        forward_query = base_select_forward + lang_conditions_forward + project_conditions + min_len_forward
        forward_params.extend(lang_params_forward)
        forward_params.extend(project_params)

        if bidirectional:
            # Build reverse query
            reverse_query = base_select_reverse + lang_conditions_reverse + project_conditions + min_len_reverse
            reverse_params.extend(lang_params_reverse)
            reverse_params.extend(project_params)

            # Combine with UNION and sort
            query = f"""
                SELECT * FROM (
                    {forward_query}
                    UNION ALL
                    {reverse_query}
                ) combined
                ORDER BY COALESCE(ranking, -1) ASC, source_term ASC
            """
            params = forward_params + reverse_params
        else:
            # Original forward-only behavior
            query = forward_query + " ORDER BY COALESCE(ranking, -1) ASC, source_term ASC"
            params = forward_params

        self.cursor.execute(query, params)
        results = []
        seen_combinations = set()  # Track (source_term, target_term, termbase_id) to avoid duplicates

        for row in self.cursor.fetchall():
            result_dict = dict(row)

            # Deduplicate: same term pair from same termbase should only appear once
            # Prefer 'source' match over 'target' match
            combo_key = (
                result_dict.get('source_term', '').lower(),
                result_dict.get('target_term', '').lower(),
                result_dict.get('termbase_id')
            )
            if combo_key in seen_combinations:
                continue
            seen_combinations.add(combo_key)

            # SQLite stores booleans as 0/1, explicitly convert to Python bool
            if 'is_project_termbase' in result_dict:
                result_dict['is_project_termbase'] = bool(result_dict['is_project_termbase'])

            # Fetch target synonyms for this term and include them in the result
            term_id = result_dict.get('id')
            match_direction = result_dict.get('match_direction', 'source')
            if term_id:
                try:
                    # For reverse matches, fetch 'source' synonyms since they become targets
                    synonym_lang = 'source' if match_direction == 'target' else 'target'
                    self.cursor.execute("""
                        SELECT synonym_text, forbidden FROM termbase_synonyms
                        WHERE term_id = ? AND language = ?
                        ORDER BY display_order ASC
                    """, (term_id, synonym_lang))
                    synonyms = []
                    for syn_row in self.cursor.fetchall():
                        syn_text = syn_row[0]
                        syn_forbidden = bool(syn_row[1])
                        if not syn_forbidden:  # Only include non-forbidden synonyms
                            synonyms.append(syn_text)
                    result_dict['target_synonyms'] = synonyms
                except Exception:
                    result_dict['target_synonyms'] = []

            results.append(result_dict)
        return results
    
    # ============================================
    # UTILITY METHODS
    # ============================================
    
    def get_all_tms(self, enabled_only: bool = True) -> List[Dict]:
        """
        Get list of all translation memories
        
        Args:
            enabled_only: If True, only return enabled TMs
            
        Returns:
            List of TM info dictionaries with tm_id, name, entry_count, enabled
        """
        # Get distinct TM IDs from translation_units
        query = "SELECT DISTINCT tm_id FROM translation_units ORDER BY tm_id"
        self.cursor.execute(query)
        tm_ids = [row[0] for row in self.cursor.fetchall()]
        
        tm_list = []
        for tm_id in tm_ids:
            entry_count = self.get_tm_count(tm_id)
            tm_info = {
                'tm_id': tm_id,
                'name': tm_id.replace('_', ' ').title(),
                'entry_count': entry_count,
                'enabled': True,  # For now, all TMs are enabled
                'read_only': False
            }
            tm_list.append(tm_info)
        
        return tm_list
    
    def get_tm_list(self, enabled_only: bool = True) -> List[Dict]:
        """Alias for get_all_tms for backward compatibility"""
        return self.get_all_tms(enabled_only=enabled_only)
    
    def get_entry_count(self, enabled_only: bool = True) -> int:
        """
        Get total number of translation entries
        
        Args:
            enabled_only: Currently ignored (all TMs enabled)
            
        Returns:
            Total number of translation units
        """
        return self.get_tm_count()
    
    def vacuum(self):
        """Optimize database (VACUUM)"""
        self.cursor.execute("VACUUM")
        self.connection.commit()
    
    # ============================================
    # TMX EDITOR METHODS (database-backed TMX files)
    # ============================================
    
    def tmx_store_file(self, file_path: str, file_name: str, original_file_path: str,
                       load_mode: str, file_size: int, header_data: dict,
                       tu_count: int, languages: List[str]) -> int:
        """
        Store TMX file metadata in database
        
        Returns:
            tmx_file_id (int)
        """
        languages_json = json.dumps(languages)
        header_json = json.dumps(header_data)
        
        # Check if file already exists
        self.cursor.execute("SELECT id FROM tmx_files WHERE file_path = ?", (file_path,))
        existing = self.cursor.fetchone()
        
        if existing:
            # Update existing
            self.cursor.execute("""
                UPDATE tmx_files 
                SET file_name = ?, original_file_path = ?, load_mode = ?, file_size = ?,
                    header_data = ?, tu_count = ?, languages = ?, last_accessed = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (file_name, original_file_path, load_mode, file_size, header_json,
                  tu_count, languages_json, existing['id']))
            self.connection.commit()
            return existing['id']
        else:
            # Insert new
            self.cursor.execute("""
                INSERT INTO tmx_files 
                (file_path, file_name, original_file_path, load_mode, file_size,
                 header_data, tu_count, languages)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (file_path, file_name, original_file_path, load_mode, file_size,
                  header_json, tu_count, languages_json))
            self.connection.commit()
            return self.cursor.lastrowid
    
    def tmx_store_translation_unit(self, tmx_file_id: int, tu_id: int,
                                   creation_date: str = None, creation_id: str = None,
                                   change_date: str = None, change_id: str = None,
                                   srclang: str = None, custom_attributes: dict = None,
                                   comments: List[str] = None, commit: bool = True) -> int:
        """
        Store a translation unit in database
        
        Args:
            commit: If False, don't commit (for batch operations)
        
        Returns:
            Internal TU ID (for referencing segments)
        """
        custom_attrs_json = json.dumps(custom_attributes) if custom_attributes else None
        comments_json = json.dumps(comments) if comments else None
        
        self.cursor.execute("""
            INSERT OR REPLACE INTO tmx_translation_units
            (tmx_file_id, tu_id, creation_date, creation_id, change_date, change_id,
             srclang, custom_attributes, comments)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tmx_file_id, tu_id, creation_date, creation_id, change_date, change_id,
              srclang, custom_attrs_json, comments_json))
        if commit:
            self.connection.commit()
        return self.cursor.lastrowid
    
    def tmx_store_segment(self, tu_db_id: int, lang: str, text: str,
                         creation_date: str = None, creation_id: str = None,
                         change_date: str = None, change_id: str = None,
                         commit: bool = True):
        """
        Store a segment (language variant) for a translation unit
        
        Args:
            commit: If False, don't commit (for batch operations)
        """
        self.cursor.execute("""
            INSERT OR REPLACE INTO tmx_segments
            (tu_id, lang, text, creation_date, creation_id, change_date, change_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tu_db_id, lang, text, creation_date, creation_id, change_date, change_id))
        if commit:
            self.connection.commit()
    
    def tmx_get_file_id(self, file_path: str) -> Optional[int]:
        """Get TMX file ID by file path"""
        self.cursor.execute("SELECT id FROM tmx_files WHERE file_path = ?", (file_path,))
        row = self.cursor.fetchone()
        return row['id'] if row else None
    
    def tmx_get_translation_units(self, tmx_file_id: int, offset: int = 0,
                                  limit: int = 50, src_lang: str = None,
                                  tgt_lang: str = None, src_filter: str = None,
                                  tgt_filter: str = None, ignore_case: bool = True) -> List[Dict]:
        """
        Get translation units with pagination and filtering
        
        Returns:
            List of dicts with TU data including segments
        """
        # Build base query
        query = """
            SELECT tu.id as tu_db_id, tu.tu_id, tu.creation_date, tu.creation_id,
                   tu.change_date, tu.change_id, tu.srclang, tu.custom_attributes, tu.comments
            FROM tmx_translation_units tu
            WHERE tu.tmx_file_id = ?
        """
        params = [tmx_file_id]
        
        # Add filters
        if src_filter or tgt_filter:
            query += """
                AND EXISTS (
                    SELECT 1 FROM tmx_segments seg1
                    WHERE seg1.tu_id = tu.id
            """
            if src_lang:
                query += " AND seg1.lang = ?"
                params.append(src_lang)
            if src_filter:
                if ignore_case:
                    query += " AND LOWER(seg1.text) LIKE LOWER(?)"
                    params.append(f"%{src_filter}%")
                else:
                    query += " AND seg1.text LIKE ?"
                    params.append(f"%{src_filter}%")
            
            if tgt_filter:
                query += """
                    AND EXISTS (
                        SELECT 1 FROM tmx_segments seg2
                        WHERE seg2.tu_id = tu.id
                """
                if tgt_lang:
                    query += " AND seg2.lang = ?"
                    params.append(tgt_lang)
                if ignore_case:
                    query += " AND LOWER(seg2.text) LIKE LOWER(?)"
                    params.append(f"%{tgt_filter}%")
                else:
                    query += " AND seg2.text LIKE ?"
                    params.append(f"%{tgt_filter}%")
                query += ")"
            
            query += ")"
        
        query += " ORDER BY tu.tu_id LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        
        # Fetch segments for each TU
        result = []
        for row in rows:
            tu_data = dict(row)
            # Get segments
            self.cursor.execute("""
                SELECT lang, text, creation_date, creation_id, change_date, change_id
                FROM tmx_segments
                WHERE tu_id = ?
            """, (tu_data['tu_db_id'],))
            segments = {}
            for seg_row in self.cursor.fetchall():
                seg_dict = dict(seg_row)
                segments[seg_dict['lang']] = seg_dict
            
            tu_data['segments'] = segments
            if tu_data['custom_attributes']:
                tu_data['custom_attributes'] = json.loads(tu_data['custom_attributes'])
            if tu_data['comments']:
                tu_data['comments'] = json.loads(tu_data['comments'])
            
            result.append(tu_data)
        
        return result
    
    def tmx_count_translation_units(self, tmx_file_id: int, src_lang: str = None,
                                    tgt_lang: str = None, src_filter: str = None,
                                    tgt_filter: str = None, ignore_case: bool = True) -> int:
        """Count translation units matching filters"""
        query = """
            SELECT COUNT(DISTINCT tu.id)
            FROM tmx_translation_units tu
            WHERE tu.tmx_file_id = ?
        """
        params = [tmx_file_id]
        
        # Add same filters as tmx_get_translation_units
        if src_filter or tgt_filter:
            query += """
                AND EXISTS (
                    SELECT 1 FROM tmx_segments seg1
                    WHERE seg1.tu_id = tu.id
            """
            if src_lang:
                query += " AND seg1.lang = ?"
                params.append(src_lang)
            if src_filter:
                if ignore_case:
                    query += " AND LOWER(seg1.text) LIKE LOWER(?)"
                    params.append(f"%{src_filter}%")
                else:
                    query += " AND seg1.text LIKE ?"
                    params.append(f"%{src_filter}%")
            
            if tgt_filter:
                query += """
                    AND EXISTS (
                        SELECT 1 FROM tmx_segments seg2
                        WHERE seg2.tu_id = tu.id
                """
                if tgt_lang:
                    query += " AND seg2.lang = ?"
                    params.append(tgt_lang)
                if ignore_case:
                    query += " AND LOWER(seg2.text) LIKE LOWER(?)"
                    params.append(f"%{tgt_filter}%")
                else:
                    query += " AND seg2.text LIKE ?"
                    params.append(f"%{tgt_filter}%")
                query += ")"
            
            query += ")"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchone()[0]
    
    def tmx_update_segment(self, tmx_file_id: int, tu_id: int, lang: str, text: str):
        """Update a segment text"""
        # Get internal TU ID
        self.cursor.execute("""
            SELECT tu.id FROM tmx_translation_units tu
            WHERE tu.tmx_file_id = ? AND tu.tu_id = ?
        """, (tmx_file_id, tu_id))
        tu_row = self.cursor.fetchone()
        if not tu_row:
            return False
        
        tu_db_id = tu_row['id']
        change_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        
        # Update segment
        self.cursor.execute("""
            UPDATE tmx_segments
            SET text = ?, change_date = ?
            WHERE tu_id = ? AND lang = ?
        """, (text, change_date, tu_db_id, lang))
        
        # Update TU change date
        self.cursor.execute("""
            UPDATE tmx_translation_units
            SET change_date = ?
            WHERE id = ?
        """, (change_date, tu_db_id))
        
        # Update file last_modified
        self.cursor.execute("""
            UPDATE tmx_files
            SET last_modified = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (tmx_file_id,))
        
        self.connection.commit()
        return True
    
    def tmx_delete_file(self, tmx_file_id: int):
        """Delete TMX file and all its data (CASCADE will handle TUs and segments)"""
        self.cursor.execute("DELETE FROM tmx_files WHERE id = ?", (tmx_file_id,))
        self.connection.commit()
    
    def tmx_get_file_info(self, tmx_file_id: int) -> Optional[Dict]:
        """Get TMX file metadata"""
        self.cursor.execute("""
            SELECT id, file_path, file_name, original_file_path, load_mode,
                   file_size, header_data, tu_count, languages,
                   created_date, last_accessed, last_modified
            FROM tmx_files
            WHERE id = ?
        """, (tmx_file_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        
        info = dict(row)
        info['header_data'] = json.loads(info['header_data'])
        info['languages'] = json.loads(info['languages'])
        return info
    
    def get_database_info(self) -> Dict:
        """Get database statistics"""
        info = {
            'path': self.db_path,
            'size_bytes': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0,
            'tm_entries': self.get_tm_count(),
        }
        
        # Get size in MB
        info['size_mb'] = round(info['size_bytes'] / (1024 * 1024), 2)
        
        return info
