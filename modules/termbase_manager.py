"""
Termbase Manager Module

Handles all termbase operations: creation, activation, term management, searching.
Uses 'termbase' terminology throughout (never 'glossary').

Termbases can be:
- Global (available to all projects)
- Project-specific (linked to particular project)

Activation system: termbases can be activated/deactivated per project.
"""

import sqlite3
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class TermbaseManager:
    """Manages termbase operations and term storage"""
    
    def __init__(self, db_manager, log_callback=None):
        """
        Initialize termbase manager
        
        Args:
            db_manager: DatabaseManager instance
            log_callback: Optional logging function
        """
        self.db_manager = db_manager
        self.log = log_callback if log_callback else print
    
    # ========================================================================
    # TERMBASE MANAGEMENT
    # ========================================================================
    
    def create_termbase(self, name: str, source_lang: Optional[str] = None, 
                       target_lang: Optional[str] = None, project_id: Optional[int] = None,
                       description: str = "", is_global: bool = True) -> Optional[int]:
        """
        Create a new termbase
        
        Args:
            name: Termbase name
            source_lang: Source language code (e.g., 'en', 'nl')
            target_lang: Target language code
            project_id: If set, termbase is project-specific; if None, it's global
            description: Optional description
            is_global: Whether this is a global termbase (available to all projects)
            
        Returns:
            Termbase ID or None if failed
        """
        try:
            cursor = self.db_manager.cursor
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO termbases (name, source_lang, target_lang, project_id, 
                                      description, is_global, created_date, modified_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, source_lang, target_lang, project_id, description, is_global, now, now))
            
            self.db_manager.connection.commit()
            termbase_id = cursor.lastrowid
            self.log(f"✓ Created termbase: {name} (ID: {termbase_id})")
            return termbase_id
        except Exception as e:
            self.log(f"✗ Error creating termbase: {e}")
            return None
    
    def get_all_termbases(self) -> List[Dict]:
        """
        Get all termbases (global and project-specific)
        
        Returns:
            List of termbase dictionaries with fields: id, name, source_lang, target_lang, 
            project_id, description, is_global, is_active, term_count, created_date, modified_date
        """
        try:
            cursor = self.db_manager.cursor
            
            cursor.execute("""
                SELECT 
                    t.id, t.name, t.source_lang, t.target_lang, t.project_id,
                    t.description, t.is_global, t.created_date, t.modified_date,
                    COUNT(gt.id) as term_count
                FROM termbases t
                LEFT JOIN termbase_terms gt ON t.id = gt.termbase_id
                GROUP BY t.id
                ORDER BY t.is_global DESC, t.name ASC
            """)
            
            termbases = []
            for row in cursor.fetchall():
                termbases.append({
                    'id': row[0],
                    'name': row[1],
                    'source_lang': row[2],
                    'target_lang': row[3],
                    'project_id': row[4],
                    'description': row[5],
                    'is_global': row[6],
                    'created_date': row[7],
                    'modified_date': row[8],
                    'term_count': row[9] or 0
                })
            
            return termbases
        except Exception as e:
            self.log(f"✗ Error fetching termbases: {e}")
            return []
    
    def get_termbase(self, termbase_id: int) -> Optional[Dict]:
        """Get single termbase by ID"""
        try:
            cursor = self.db_manager.cursor
            
            cursor.execute("""
                SELECT 
                    t.id, t.name, t.source_lang, t.target_lang, t.project_id,
                    t.description, t.is_global, t.created_date, t.modified_date,
                    COUNT(gt.id) as term_count
                FROM termbases t
                LEFT JOIN termbase_terms gt ON t.id = gt.termbase_id
                WHERE t.id = ?
                GROUP BY t.id
            """, (termbase_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'source_lang': row[2],
                    'target_lang': row[3],
                    'project_id': row[4],
                    'description': row[5],
                    'is_global': row[6],
                    'created_date': row[7],
                    'modified_date': row[8],
                    'term_count': row[9] or 0
                }
            return None
        except Exception as e:
            self.log(f"✗ Error fetching termbase: {e}")
            return None
    
    def delete_termbase(self, termbase_id: int) -> bool:
        """
        Delete termbase and all its terms
        
        Args:
            termbase_id: Termbase ID
            
        Returns:
            True if successful
        """
        try:
            cursor = self.db_manager.cursor
            
            # Delete terms first
            cursor.execute("DELETE FROM termbase_terms WHERE termbase_id = ?", (termbase_id,))
            
            # Delete termbase
            cursor.execute("DELETE FROM termbases WHERE id = ?", (termbase_id,))
            
            self.db_manager.connection.commit()
            self.log(f"✓ Deleted termbase ID: {termbase_id}")
            return True
        except Exception as e:
            self.log(f"✗ Error deleting termbase: {e}")
            return False
    
    def get_active_termbases_for_project(self, project_id: int) -> List[Dict]:
        """
        Get all active termbases for a specific project
        
        Args:
            project_id: Project ID
            
        Returns:
            List of active termbase dictionaries
        """
        try:
            cursor = self.db_manager.cursor
            
            cursor.execute("""
                SELECT 
                    t.id, t.name, t.source_lang, t.target_lang, t.project_id,
                    t.description, t.is_global, t.created_date, t.modified_date,
                    COUNT(gt.id) as term_count
                FROM termbases t
                LEFT JOIN termbase_terms gt ON t.id = gt.termbase_id
                LEFT JOIN termbase_activation ta ON t.id = ta.termbase_id AND ta.project_id = ?
                WHERE (t.is_global = 1 OR t.project_id = ?)
                AND (ta.is_active = 1 OR ta.is_active IS NULL)
                GROUP BY t.id
                ORDER BY t.name ASC
            """, (project_id, project_id))
            
            termbases = []
            for row in cursor.fetchall():
                termbases.append({
                    'id': row[0],
                    'name': row[1],
                    'source_lang': row[2],
                    'target_lang': row[3],
                    'project_id': row[4],
                    'description': row[5],
                    'is_global': row[6],
                    'created_date': row[7],
                    'modified_date': row[8],
                    'term_count': row[9] or 0
                })
            
            return termbases
        except Exception as e:
            self.log(f"✗ Error fetching active termbases: {e}")
            return []
    
    # ========================================================================
    # TERMBASE ACTIVATION
    # ========================================================================
    
    def is_termbase_active(self, termbase_id: int, project_id: int) -> bool:
        """Check if termbase is active for a project"""
        try:
            cursor = self.db_manager.cursor
            
            cursor.execute("""
                SELECT is_active FROM termbase_activation 
                WHERE termbase_id = ? AND project_id = ?
            """, (termbase_id, project_id))
            
            result = cursor.fetchone()
            if result:
                return result[0] == 1
            
            # If no record exists, termbases are active by default
            return True
        except Exception as e:
            self.log(f"✗ Error checking termbase activation: {e}")
            return True
    
    def activate_termbase(self, termbase_id: int, project_id: int) -> bool:
        """Activate termbase for project"""
        try:
            cursor = self.db_manager.cursor
            
            cursor.execute("""
                INSERT OR REPLACE INTO termbase_activation (termbase_id, project_id, is_active)
                VALUES (?, ?, 1)
            """, (termbase_id, project_id))
            
            self.db_manager.connection.commit()
            self.log(f"✓ Activated termbase {termbase_id} for project {project_id}")
            return True
        except Exception as e:
            self.log(f"✗ Error activating termbase: {e}")
            return False
    
    def deactivate_termbase(self, termbase_id: int, project_id: int) -> bool:
        """Deactivate termbase for project"""
        try:
            cursor = self.db_manager.cursor
            
            cursor.execute("""
                INSERT OR REPLACE INTO termbase_activation (termbase_id, project_id, is_active)
                VALUES (?, ?, 0)
            """, (termbase_id, project_id))
            
            self.db_manager.connection.commit()
            self.log(f"✓ Deactivated termbase {termbase_id} for project {project_id}")
            return True
        except Exception as e:
            self.log(f"✗ Error deactivating termbase: {e}")
            return False
    
    # ========================================================================
    # TERM MANAGEMENT
    # ========================================================================
    
    def add_term(self, termbase_id: int, source_term: str, target_term: str,
                 priority: int = 99, domain: str = "", definition: str = "",
                 forbidden: bool = False, source_lang: Optional[str] = None,
                 target_lang: Optional[str] = None) -> Optional[int]:
        """
        Add a term to termbase
        
        Args:
            termbase_id: Termbase ID
            source_term: Source language term
            target_term: Target language term
            priority: Priority (1=highest, 99=default)
            domain: Domain/category
            definition: Optional definition
            forbidden: Whether this is a forbidden term
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Term ID or None if failed
        """
        try:
            cursor = self.db_manager.cursor
            
            cursor.execute("""
                INSERT INTO termbase_terms 
                (termbase_id, source_term, target_term, priority, domain, definition, 
                 forbidden, source_lang, target_lang)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (termbase_id, source_term, target_term, priority, domain, definition,
                  forbidden, source_lang, target_lang))
            
            self.db_manager.connection.commit()
            term_id = cursor.lastrowid
            self.log(f"✓ Added term to termbase {termbase_id}: {source_term} → {target_term}")
            return term_id
        except Exception as e:
            self.log(f"✗ Error adding term: {e}")
            return None
    
    def get_terms(self, termbase_id: int) -> List[Dict]:
        """Get all terms in a termbase"""
        try:
            cursor = self.db_manager.cursor
            
            cursor.execute("""
                SELECT id, source_term, target_term, priority, domain, definition, forbidden
                FROM termbase_terms
                WHERE termbase_id = ?
                ORDER BY priority ASC, source_term ASC
            """, (termbase_id,))
            
            terms = []
            for row in cursor.fetchall():
                terms.append({
                    'id': row[0],
                    'source_term': row[1],
                    'target_term': row[2],
                    'priority': row[3],
                    'domain': row[4],
                    'definition': row[5],
                    'forbidden': row[6]
                })
            
            return terms
        except Exception as e:
            self.log(f"✗ Error fetching terms: {e}")
            return []
    
    def update_term(self, term_id: int, source_term: Optional[str] = None,
                   target_term: Optional[str] = None, priority: Optional[int] = None,
                   domain: Optional[str] = None, definition: Optional[str] = None,
                   forbidden: Optional[bool] = None) -> bool:
        """Update a term"""
        try:
            cursor = self.db_manager.cursor
            updates = []
            params = []
            
            if source_term is not None:
                updates.append("source_term = ?")
                params.append(source_term)
            if target_term is not None:
                updates.append("target_term = ?")
                params.append(target_term)
            if priority is not None:
                updates.append("priority = ?")
                params.append(priority)
            if domain is not None:
                updates.append("domain = ?")
                params.append(domain)
            if definition is not None:
                updates.append("definition = ?")
                params.append(definition)
            if forbidden is not None:
                updates.append("forbidden = ?")
                params.append(forbidden)
            
            if not updates:
                return False
            
            params.append(term_id)
            sql = f"UPDATE termbase_terms SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql, params)
            self.db_manager.connection.commit()
            
            self.log(f"✓ Updated term {term_id}")
            return True
        except Exception as e:
            self.log(f"✗ Error updating term: {e}")
            return False
    
    def delete_term(self, term_id: int) -> bool:
        """Delete a term"""
        try:
            cursor = self.db_manager.cursor
            cursor.execute("DELETE FROM termbase_terms WHERE id = ?", (term_id,))
            self.db_manager.connection.commit()
            self.log(f"✓ Deleted term {term_id}")
            return True
        except Exception as e:
            self.log(f"✗ Error deleting term: {e}")
            return False
    
    # ========================================================================
    # SEARCH
    # ========================================================================
    
    def search_termbase(self, termbase_id: int, search_term: str, 
                       search_source: bool = True, search_target: bool = True) -> List[Dict]:
        """
        Search within a termbase
        
        Args:
            termbase_id: Termbase ID to search in
            search_term: Term to search for
            search_source: Search in source terms
            search_target: Search in target terms
            
        Returns:
            List of matching terms
        """
        try:
            cursor = self.db_manager.cursor
            
            conditions = ["termbase_id = ?"]
            params = [termbase_id]
            
            # Build search condition
            search_conds = []
            if search_source:
                search_conds.append("source_term LIKE ?")
                params.append(f"%{search_term}%")
            if search_target:
                search_conds.append("target_term LIKE ?")
                params.append(f"%{search_term}%")
            
            if search_conds:
                conditions.append(f"({' OR '.join(search_conds)})")
            
            sql = f"""
                SELECT id, source_term, target_term, priority, domain, definition, forbidden
                FROM termbase_terms
                WHERE {' AND '.join(conditions)}
                ORDER BY priority ASC, source_term ASC
            """
            
            cursor.execute(sql, params)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'source_term': row[1],
                    'target_term': row[2],
                    'priority': row[3],
                    'domain': row[4],
                    'definition': row[5],
                    'forbidden': row[6]
                })
            
            return results
        except Exception as e:
            self.log(f"✗ Error searching termbase: {e}")
            return []
