"""
Database Manager Module

SQLite database backend for Translation Memories, Glossaries, and related resources.
Replaces in-memory JSON-based storage with efficient database storage.

Schema includes:
- Translation units (TM entries)
- Glossary terms
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
            # Will be set by application - defaults to user data folder
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
            
            self.log(f"✓ Database connected: {os.path.basename(self.db_path)}")
            return True
            
        except Exception as e:
            self.log(f"✗ Database connection failed: {e}")
            return False
    
    def _create_tables(self):
        """Create database schema"""
        
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
        # GLOSSARY TABLES
        # ============================================
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS glossary_terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_term TEXT NOT NULL,
                target_term TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                glossary_id TEXT NOT NULL,
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
                
                FOREIGN KEY (tm_source_id) REFERENCES translation_units(id) ON DELETE SET NULL
            )
        """)
        
        # Indexes for glossary_terms
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gt_source_term 
            ON glossary_terms(source_term)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gt_glossary_id 
            ON glossary_terms(glossary_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gt_project_id 
            ON glossary_terms(project_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gt_domain 
            ON glossary_terms(domain)
        """)
        
        # Full-text search for glossary
        self.cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS glossary_terms_fts 
            USING fts5(
                source_term,
                target_term,
                definition,
                content=glossary_terms,
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
                active_glossary_ids TEXT,
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
        self.connection.commit()
    
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
                       source_lang: str = None, target_lang: str = None) -> Optional[Dict]:
        """
        Get exact match from TM
        
        Args:
            source: Source text to match
            tm_ids: List of TM IDs to search (None = all)
            source_lang: Filter by source language
            target_lang: Filter by target language
        
        Returns: Dictionary with match data or None
        """
        source_hash = hashlib.md5(source.encode('utf-8')).hexdigest()
        
        query = """
            SELECT * FROM translation_units 
            WHERE source_hash = ? AND source_text = ?
        """
        params = [source_hash, source]
        
        if tm_ids:
            placeholders = ','.join('?' * len(tm_ids))
            query += f" AND tm_id IN ({placeholders})"
            params.extend(tm_ids)
        
        if source_lang:
            query += " AND source_lang = ?"
            params.append(source_lang)
        
        if target_lang:
            query += " AND target_lang = ?"
            params.append(target_lang)
        
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
        
        return None
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity ratio between two texts using SequenceMatcher
        
        Returns: Similarity score from 0.0 to 1.0
        """
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def search_fuzzy_matches(self, source: str, tm_ids: List[str] = None,
                            threshold: float = 0.75, max_results: int = 5,
                            source_lang: str = None, target_lang: str = None) -> List[Dict]:
        """
        Search for fuzzy matches using FTS5 with proper similarity calculation
        
        Returns: List of matches with similarity scores
        """
        # For better FTS5 matching, tokenize the query and escape special chars
        # FTS5 special characters: " ( ) - : , . ! ? 
        import re
        # Remove special FTS5 characters and split into words
        clean_text = re.sub(r'[^\w\s]', ' ', source)  # Replace special chars with spaces
        search_terms = [term for term in clean_text.strip().split() if len(term) > 1]
        
        if not search_terms:
            # If no valid terms, return empty results
            return []
        
        # Quote each term to prevent FTS5 syntax errors
        fts_query = ' OR '.join(f'"{term}"' for term in search_terms)
        
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
        
        if source_lang:
            query += " AND tu.source_lang = ?"
            params.append(source_lang)
        
        if target_lang:
            query += " AND tu.target_lang = ?"
            params.append(target_lang)
        
        # Get more candidates than needed for proper scoring
        query += f" ORDER BY relevance DESC LIMIT {max_results * 5}"
        
        self.cursor.execute(query, params)
        results = []
        
        for row in self.cursor.fetchall():
            match_dict = dict(row)
            # Calculate actual similarity using SequenceMatcher
            similarity = self.calculate_similarity(source, match_dict['source_text'])
            
            # Only include matches above threshold
            if similarity >= threshold:
                match_dict['similarity'] = similarity
                match_dict['match_pct'] = int(similarity * 100)
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
    
    def concordance_search(self, query: str, tm_ids: List[str] = None) -> List[Dict]:
        """
        Search for text in both source and target (concordance search)
        """
        search_query = f"%{query}%"
        
        sql = """
            SELECT * FROM translation_units 
            WHERE (source_text LIKE ? OR target_text LIKE ?)
        """
        params = [search_query, search_query]
        
        if tm_ids:
            placeholders = ','.join('?' * len(tm_ids))
            sql += f" AND tm_id IN ({placeholders})"
            params.extend(tm_ids)
        
        sql += " ORDER BY modified_date DESC LIMIT 100"
        
        self.cursor.execute(sql, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ============================================
    # GLOSSARY METHODS (Placeholder for Phase 3)
    # ============================================
    
    def add_glossary_term(self, source_term: str, target_term: str,
                         source_lang: str, target_lang: str,
                         glossary_id: str = 'main', **kwargs) -> int:
        """Add term to glossary (Phase 3)"""
        # TODO: Implement in Phase 3
        pass
    
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
