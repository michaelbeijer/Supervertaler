"""
Termbase Manager Module

Handles termbase/termbase management for Supervertaler:
- Create/delete glossaries
- Add/edit/delete terms
- Activate/deactivate for projects
- Import/export glossaries
- Search across termbases

Unified management for both global and project-specific termbases.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TermbaseInfo:
    """Information about a termbase/termbase"""
    id: int
    name: str
    description: str
    source_lang: Optional[str]
    target_lang: Optional[str]
    project_id: Optional[int]  # None = global, set = project-specific
    created_date: str
    modified_date: str
    entry_count: int
    is_active_for_project: bool = False


@dataclass
class TermbaseEntry:
    """A single term entry in a termbase"""
    id: int
    termbase_id: int
    source_term: str
    target_term: str
    priority: int  # 1-99, lower = higher priority
    domain: str
    definition: str
    forbidden: bool
    non_translatable: bool
    created_date: str
    modified_date: str


class TermbaseManager:
    """Manages glossaries and termbases"""

    def __init__(self, db_manager, log_callback=None):
        """
        Initialize termbase manager
        
        Args:
            db_manager: DatabaseManager instance
            log_callback: Optional logging function
        """
        self.db = db_manager
        self.log = log_callback if log_callback else print

    def create_termbase(
        self,
        name: str,
        description: str = "",
        source_lang: Optional[str] = None,
        target_lang: Optional[str] = None,
        project_id: Optional[int] = None
    ) -> int:
        """
        Create a new termbase
        
        Args:
            name: termbase name
            description: Optional description
            source_lang: Source language code (e.g., 'NL', 'EN')
            target_lang: Target language code
            project_id: Optional project ID (None = global termbase)
        
        Returns:
            termbase ID
        """
        try:
            cursor = self.db.cursor
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO glossaries (name, description, source_lang, target_lang, project_id, created_date, modified_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, description, source_lang, target_lang, project_id, now, now))
            
            self.db.connection.commit()
            termbase_id = cursor.lastrowid
            self.log(f"Created termbase '{name}' (ID: {termbase_id})")
            return termbase_id
        except Exception as e:
            self.log(f"Error creating termbase: {e}")
            raise

    def get_all_termbases(self) -> List[GlossaryInfo]:
        """Get all glossaries (global and project-specific)"""
        try:
            cursor = self.db.cursor
            cursor.execute("""
                SELECT 
                    g.id, g.name, g.description, g.source_lang, g.target_lang,
                    g.project_id, g.created_date, g.modified_date,
                    COUNT(gt.id) as entry_count
                FROM glossaries g
                LEFT JOIN termbase_terms gt ON g.id = gt.termbase_id
                GROUP BY g.id
                ORDER BY g.name
            """)
            
            results = cursor.fetchall()
            glossaries = []
            for row in results:
                glossaries.append(GlossaryInfo(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    source_lang=row[3],
                    target_lang=row[4],
                    project_id=row[5],
                    created_date=row[6],
                    modified_date=row[7],
                    entry_count=row[8] or 0
                ))
            return glossaries
        except Exception as e:
            self.log(f"Error fetching glossaries: {e}")
            return []

    def get_termbase_terms(self, termbase_id: int) -> List[TermEntry]:
        """Get all terms in a termbase"""
        try:
            cursor = self.db.cursor
            cursor.execute("""
                SELECT id, termbase_id, source_term, target_term, priority, 
                       domain, definition, forbidden, non_translatable, created_date, modified_date
                FROM termbase_terms
                WHERE termbase_id = ?
                ORDER BY priority ASC, source_term ASC
            """, (termbase_id,))
            
            results = cursor.fetchall()
            terms = []
            for row in results:
                terms.append(TermEntry(
                    id=row[0],
                    termbase_id=row[1],
                    source_term=row[2],
                    target_term=row[3],
                    priority=row[4],
                    domain=row[5],
                    definition=row[6],
                    forbidden=bool(row[7]),
                    non_translatable=bool(row[8]),
                    created_date=row[9],
                    modified_date=row[10]
                ))
            return terms
        except Exception as e:
            self.log(f"Error fetching terms for termbase {termbase_id}: {e}")
            return []

    def add_term(
        self,
        termbase_id: int,
        source_term: str,
        target_term: str,
        priority: int = 50,
        domain: str = "",
        definition: str = "",
        forbidden: bool = False,
        non_translatable: bool = False
    ) -> int:
        """
        Add a term to a termbase
        
        Args:
            termbase_id: Target termbase ID
            source_term: Source language term
            target_term: Target language term
            priority: Priority ranking (1-99, lower = higher)
            domain: Domain/subject area
            definition: Definition or note
            forbidden: Whether term is forbidden for translation
            non_translatable: Whether term should not be translated
        
        Returns:
            Term ID
        """
        try:
            cursor = self.db.cursor
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO termbase_terms 
                (termbase_id, source_term, target_term, priority, domain, definition, 
                 forbidden, non_translatable, source_lang, target_lang, created_date, modified_date)
                SELECT ?, ?, ?, ?, ?, ?, ?, ?, source_lang, target_lang, ?, ?
                FROM glossaries
                WHERE id = ?
            """, (termbase_id, source_term, target_term, priority, domain, definition,
                  forbidden, non_translatable, now, now, termbase_id))
            
            self.db.connection.commit()
            term_id = cursor.lastrowid
            self.log(f"Added term '{source_term}' to termbase {termbase_id}")
            return term_id
        except Exception as e:
            self.log(f"Error adding term: {e}")
            raise

    def update_term(
        self,
        term_id: int,
        source_term: str = None,
        target_term: str = None,
        priority: int = None,
        domain: str = None,
        definition: str = None,
        forbidden: bool = None,
        non_translatable: bool = None
    ) -> bool:
        """Update a term in a termbase"""
        try:
            cursor = self.db.cursor
            now = datetime.now().isoformat()
            
            # Build dynamic update query
            updates = ["modified_date = ?"]
            params = [now]
            
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
            if non_translatable is not None:
                updates.append("non_translatable = ?")
                params.append(non_translatable)
            
            params.append(term_id)
            query = f"UPDATE termbase_terms SET {', '.join(updates)} WHERE id = ?"
            
            cursor.execute(query, params)
            self.db.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.log(f"Error updating term {term_id}: {e}")
            return False

    def delete_term(self, term_id: int) -> bool:
        """Delete a term from a termbase"""
        try:
            cursor = self.db.cursor
            cursor.execute("DELETE FROM termbase_terms WHERE id = ?", (term_id,))
            self.db.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.log(f"Error deleting term {term_id}: {e}")
            return False

    def delete_termbase(self, termbase_id: int) -> bool:
        """Delete a termbase and all its terms"""
        try:
            cursor = self.db.cursor
            # Delete terms first
            cursor.execute("DELETE FROM termbase_terms WHERE termbase_id = ?", (termbase_id,))
            # Delete termbase
            cursor.execute("DELETE FROM glossaries WHERE id = ?", (termbase_id,))
            self.db.connection.commit()
            self.log(f"Deleted termbase {termbase_id}")
            return cursor.rowcount > 0
        except Exception as e:
            self.log(f"Error deleting termbase {termbase_id}: {e}")
            return False

    def activate_for_project(self, termbase_id: int, project_id: int) -> bool:
        """Mark a termbase as active for a specific project"""
        try:
            cursor = self.db.cursor
            cursor.execute("""
                INSERT OR REPLACE INTO termbase_project_activation (termbase_id, project_id, activated_date)
                VALUES (?, ?, datetime('now'))
            """, (termbase_id, project_id))
            self.db.connection.commit()
            return True
        except Exception as e:
            self.log(f"Error activating termbase: {e}")
            return False

    def deactivate_for_project(self, termbase_id: int, project_id: int) -> bool:
        """Mark a termbase as inactive for a specific project"""
        try:
            cursor = self.db.cursor
            cursor.execute("""
                DELETE FROM termbase_project_activation
                WHERE termbase_id = ? AND project_id = ?
            """, (termbase_id, project_id))
            self.db.connection.commit()
            return True
        except Exception as e:
            self.log(f"Error deactivating termbase: {e}")
            return False

    def is_active_for_project(self, termbase_id: int, project_id: int) -> bool:
        """Check if termbase is active for a project"""
        try:
            cursor = self.db.cursor
            cursor.execute("""
                SELECT 1 FROM termbase_project_activation
                WHERE termbase_id = ? AND project_id = ?
            """, (termbase_id, project_id))
            return cursor.fetchone() is not None
        except Exception as e:
            self.log(f"Error checking activation status: {e}")
            return False

    def get_active_glossaries_for_project(self, project_id: int) -> List[GlossaryInfo]:
        """Get all glossaries active for a specific project (global + project-specific)"""
        try:
            cursor = self.db.cursor
            # Get global glossaries (project_id IS NULL) that are activated
            # Plus project-specific glossaries (project_id = target_project)
            cursor.execute("""
                SELECT DISTINCT
                    g.id, g.name, g.description, g.source_lang, g.target_lang,
                    g.project_id, g.created_date, g.modified_date,
                    COUNT(gt.id) as entry_count
                FROM glossaries g
                LEFT JOIN termbase_terms gt ON g.id = gt.termbase_id
                WHERE (g.project_id = ? OR 
                       (g.project_id IS NULL AND g.id IN 
                        (SELECT termbase_id FROM termbase_project_activation WHERE project_id = ?)))
                GROUP BY g.id
                ORDER BY g.name
            """, (project_id, project_id))
            
            results = cursor.fetchall()
            glossaries = []
            for row in results:
                glossaries.append(GlossaryInfo(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    source_lang=row[3],
                    target_lang=row[4],
                    project_id=row[5],
                    created_date=row[6],
                    modified_date=row[7],
                    entry_count=row[8] or 0,
                    is_active_for_project=True
                ))
            return glossaries
        except Exception as e:
            self.log(f"Error fetching active glossaries: {e}")
            return []

    def export_glossary_to_csv(self, termbase_id: int, filepath: str) -> bool:
        """Export termbase to CSV format"""
        try:
            import csv
            terms = self.get_termbase_terms(termbase_id)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Source Term', 'Target Term', 'Domain', 'Definition', 'Priority', 'Forbidden', 'Non-Translatable'])
                
                for term in terms:
                    writer.writerow([
                        term.source_term,
                        term.target_term,
                        term.domain,
                        term.definition,
                        term.priority,
                        'Yes' if term.forbidden else 'No',
                        'Yes' if term.non_translatable else 'No'
                    ])
            
            self.log(f"Exported termbase {termbase_id} to {filepath}")
            return True
        except Exception as e:
            self.log(f"Error exporting termbase: {e}")
            return False

    def import_glossary_from_csv(self, termbase_id: int, filepath: str) -> int:
        """Import terms into termbase from CSV file"""
        try:
            import csv
            count = 0
            
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    priority = int(row.get('Priority', 50))
                    forbidden = row.get('Forbidden', 'No').lower() == 'yes'
                    non_translatable = row.get('Non-Translatable', 'No').lower() == 'yes'
                    
                    self.add_term(
                        termbase_id,
                        row['Source Term'],
                        row['Target Term'],
                        priority=priority,
                        domain=row.get('Domain', ''),
                        definition=row.get('Definition', ''),
                        forbidden=forbidden,
                        non_translatable=non_translatable
                    )
                    count += 1
            
            self.log(f"Imported {count} terms into termbase {termbase_id}")
            return count
        except Exception as e:
            self.log(f"Error importing termbase: {e}")
            return 0
