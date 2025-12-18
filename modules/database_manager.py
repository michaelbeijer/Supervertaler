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
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from difflib import SequenceMatcher


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
                            context_after: str = None, notes: str = None) -> int:
        """
        Add translation unit to database
        
        Returns: ID of inserted/updated entry
        """
        # Generate hash for fast exact matching
        source_hash = hashlib.md5(source.encode('utf-8')).hexdigest()
        
        try:
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
        
        source_hash = hashlib.md5(source.encode('utf-8')).hexdigest()
        
        # Get base language codes for comparison
        src_base = get_base_lang_code(source_lang) if source_lang else None
        tgt_base = get_base_lang_code(target_lang) if target_lang else None
        
        query = """
            SELECT * FROM translation_units 
            WHERE source_hash = ? AND source_text = ?
        """
        params = [source_hash, source]
        
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
        Calculate similarity ratio between two texts using SequenceMatcher
        
        Returns: Similarity score from 0.0 to 1.0
        """
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def search_fuzzy_matches(self, source: str, tm_ids: List[str] = None,
                            threshold: float = 0.75, max_results: int = 5,
                            source_lang: str = None, target_lang: str = None,
                            bidirectional: bool = True) -> List[Dict]:
        """
        Search for fuzzy matches using FTS5 with proper similarity calculation
        
        Args:
            bidirectional: If True, search both directions (nl→en AND en→nl)
        
        Returns: List of matches with similarity scores
        """
        # For better FTS5 matching, tokenize the query and escape special chars
        # FTS5 special characters: " ( ) - : , . ! ? 
        import re
        from modules.tmx_generator import get_base_lang_code
        
        # Remove special FTS5 characters and split into words
        clean_text = re.sub(r'[^\w\s]', ' ', source)  # Replace special chars with spaces
        search_terms = [term for term in clean_text.strip().split() if len(term) > 1]
        
        print(f"[DEBUG] search_fuzzy_matches: source='{source[:50]}', search_terms={search_terms}")
        
        if not search_terms:
            # If no valid terms, return empty results
            print(f"[DEBUG] search_fuzzy_matches: No valid search terms, returning empty")
            return []
        
        # Quote each term to prevent FTS5 syntax errors
        fts_query = ' OR '.join(f'"{term}"' for term in search_terms)
        print(f"[DEBUG] search_fuzzy_matches: FTS query = {fts_query}")
        
        # Get base language codes for comparison
        src_base = get_base_lang_code(source_lang) if source_lang else None
        tgt_base = get_base_lang_code(target_lang) if target_lang else None
        
        # Use FTS5 for initial candidate retrieval (fast)
        query = """
            SELECT tu.*, 
                   bm25(translation_units_fts) as relevance
            FROM translation_units tu
            JOIN translation_units_fts ON tu.id = translation_units_fts.rowid
            WHERE translation_units_fts MATCH ?
        """
        params = [fts_query]
        
        if tm_ids:
            placeholders = ','.join('?' * len(tm_ids))
            query += f" AND tu.tm_id IN ({placeholders})"
            params.extend(tm_ids)
        
        # Use flexible language matching (matches 'nl', 'nl-NL', 'Dutch', etc.)
        from modules.tmx_generator import get_lang_match_variants
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
        
        # Get more candidates than needed for proper scoring
        query += f" ORDER BY relevance DESC LIMIT {max_results * 5}"
        
        print(f"[DEBUG] search_fuzzy_matches: Executing query...")
        try:
            self.cursor.execute(query, params)
            all_rows = self.cursor.fetchall()
            print(f"[DEBUG] search_fuzzy_matches: FTS query returned {len(all_rows)} candidates")
        except Exception as e:
            print(f"[DEBUG] search_fuzzy_matches: SQL ERROR: {e}")
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
        
        print(f"[DEBUG] search_fuzzy_matches: After threshold filter: {len(results)} matches")
        
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
            
            if tm_ids:
                placeholders = ','.join('?' * len(tm_ids))
                query += f" AND tu.tm_id IN ({placeholders})"
                params.extend(tm_ids)
            
            # Reversed language filters with flexible matching
            # For reverse: TM target_lang should match our source_lang, TM source_lang should match our target_lang
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
        
        # Sort by similarity (highest first) and limit results
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:max_results]
    
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
                            source_lang: str = None, target_lang: str = None) -> List[Dict]:
        """
        Search for text in source and/or target (concordance search)
        Uses FTS5 full-text search for fast matching on millions of segments.
        Falls back to LIKE queries if FTS5 fails.
        
        Args:
            query: Text to search for
            tm_ids: List of TM IDs to search (None = all)
            direction: 'source' = search source only, 'target' = search target only, 'both' = bidirectional
            source_lang: Filter by source language (None = any)
            target_lang: Filter by target language (None = any)
        """
        # Escape FTS5 special characters and wrap words for prefix matching
        # FTS5 special chars: " * ( ) : ^
        fts_query = query.replace('"', '""')
        # Wrap in quotes for phrase search
        fts_query = f'"{fts_query}"'
        
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
            
            # Add language filters
            if source_lang:
                fts_sql += " AND tu.source_lang = ?"
                params.append(source_lang)
            if target_lang:
                fts_sql += " AND tu.target_lang = ?"
                params.append(target_lang)
            
            fts_sql += " ORDER BY tu.modified_date DESC LIMIT 100"
            
            self.cursor.execute(fts_sql, params)
            return [dict(row) for row in self.cursor.fetchall()]
            
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
            
            if source_lang:
                sql += " AND source_lang = ?"
                params.append(source_lang)
            if target_lang:
                sql += " AND target_lang = ?"
                params.append(target_lang)
            
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
                        min_length: int = 0) -> List[Dict]:
        """
        Search termbases for matching source terms
        
        Args:
            search_term: Source term to search for
            source_lang: Filter by source language (optional)
            target_lang: Filter by target language (optional)
            project_id: Filter by project (optional)
            min_length: Minimum term length to return
            
        Returns:
            List of termbase hits, sorted by priority (lower = higher priority)
        """
        # Build query with filters - include termbase name and ranking via JOIN
        # Note: termbase_id is stored as TEXT in termbase_terms but INTEGER in termbases
        # Use CAST to ensure proper comparison
        # IMPORTANT: Join with termbase_activation to get the ACTUAL priority for this project
        query = """
            SELECT 
                t.id, t.source_term, t.target_term, t.termbase_id, t.priority, 
                t.forbidden, t.source_lang, t.target_lang, t.definition, t.domain,
                t.notes, t.project, t.client,
                tb.name as termbase_name,
                tb.source_lang as termbase_source_lang,
                tb.target_lang as termbase_target_lang,
                tb.is_project_termbase,
                COALESCE(ta.priority, tb.ranking) as ranking
            FROM termbase_terms t
            LEFT JOIN termbases tb ON CAST(t.termbase_id AS INTEGER) = tb.id
            LEFT JOIN termbase_activation ta ON ta.termbase_id = tb.id AND ta.project_id = ? AND ta.is_active = 1
            WHERE (
                LOWER(t.source_term) = LOWER(?) OR 
                LOWER(t.source_term) LIKE LOWER(?) OR 
                LOWER(t.source_term) LIKE LOWER(?) OR 
                LOWER(t.source_term) LIKE LOWER(?)
            )
            AND (ta.is_active = 1 OR tb.is_project_termbase = 1)
        """
        # Exact match, word at start, word at end, word in middle
        # Use LOWER() for case-insensitive matching (handles "Edelmetalen" = "edelmetalen")
        # IMPORTANT: project_id must be first param for the LEFT JOIN ta.project_id = ? above
        params = [
            project_id if project_id else 0,  # Use 0 if no project (won't match any activation records)
            search_term,
            f"{search_term} %",
            f"% {search_term}",
            f"% {search_term} %"
        ]
        
        # Language filters - if term has no language, use termbase language for filtering
        if source_lang:
            query += """ AND (
                t.source_lang = ? OR 
                (t.source_lang IS NULL AND tb.source_lang = ?) OR
                (t.source_lang IS NULL AND tb.source_lang IS NULL)
            )"""
            params.extend([source_lang, source_lang])
        
        if target_lang:
            query += """ AND (
                t.target_lang = ? OR 
                (t.target_lang IS NULL AND tb.target_lang = ?) OR
                (t.target_lang IS NULL AND tb.target_lang IS NULL)
            )"""
            params.extend([target_lang, target_lang])
        
        # Project filter: match project-specific terms OR global terms (project_id IS NULL)
        if project_id:
            query += " AND (t.project_id = ? OR t.project_id IS NULL)"
            params.append(project_id)
        
        if min_length > 0:
            query += f" AND LENGTH(t.source_term) >= {min_length}"
        
        # Sort by ranking (lower number = higher priority)
        # Project termbases (ranking IS NULL) appear first, then by ranking, then alphabetically
        # Use COALESCE to treat NULL as -1 (highest priority)
        query += " ORDER BY COALESCE(tb.ranking, -1) ASC, t.source_term ASC"
        
        self.cursor.execute(query, params)
        results = []
        for row in self.cursor.fetchall():
            result_dict = dict(row)
            # SQLite stores booleans as 0/1, explicitly convert to Python bool
            if 'is_project_termbase' in result_dict:
                result_dict['is_project_termbase'] = bool(result_dict['is_project_termbase'])
            
            # Fetch target synonyms for this term and include them in the result
            term_id = result_dict.get('id')
            if term_id:
                try:
                    self.cursor.execute("""
                        SELECT synonym_text, forbidden FROM termbase_synonyms
                        WHERE term_id = ? AND language = 'target'
                        ORDER BY display_order ASC
                    """, (term_id,))
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
