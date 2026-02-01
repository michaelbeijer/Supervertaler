"""
ExtractTM - Persistent TM extraction saved to .svtm files

This module implements TM extraction that saves relevant segments from existing TMs
to a .svtm file (SQLite database) next to the project file. Unlike the in-memory
ProjectTM, this persists across sessions.

File format: .svtm (Supervertaler TM) - SQLite database internally
Filename pattern: {ProjectName}_Extract.svtm
"""

import sqlite3
import threading
import os
from pathlib import Path
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Callable, Tuple
import re
import time


class ExtractTM:
    """
    Persistent TM extraction saved to disk as .svtm file.

    Extracts relevant segments from selected TMs and saves them to a SQLite
    database file next to the project. This persists across sessions, so
    extraction only needs to happen once per project.

    Usage:
        extract_tm = ExtractTM()

        # Extract and save
        extract_tm.extract_and_save(
            output_path="MyProject_Extract.svtm",
            db_manager=db_manager,
            project_segments=segments,
            tm_ids=['tm1', 'tm2'],
            threshold=0.80,
            progress_callback=lambda cur, total, msg: print(f"{cur}/{total} - {msg}")
        )

        # Load existing extraction
        extract_tm.load("MyProject_Extract.svtm")

        # Search
        matches = extract_tm.search("source text")
    """

    SCHEMA_VERSION = 1

    def __init__(self):
        """Initialize ExtractTM (not connected to any file yet)"""
        self.conn = None
        self.file_path = None
        self.lock = threading.Lock()
        self.is_loaded = False
        self.segment_count = 0
        self.metadata = {}

    def _create_schema(self):
        """Create the database schema"""
        with self.lock:
            cursor = self.conn.cursor()

            # Metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

            # Segments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS segments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text TEXT NOT NULL,
                    target_text TEXT NOT NULL,
                    source_lower TEXT NOT NULL,
                    tm_id TEXT,
                    tm_name TEXT,
                    similarity REAL,
                    original_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_source_lower ON segments(source_lower)")

            # FTS5 for fuzzy text search
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS segments_fts USING fts5(
                    source_text,
                    content=segments,
                    content_rowid=id
                )
            """)

            # Store schema version
            cursor.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('schema_version', ?)",
                          (str(self.SCHEMA_VERSION),))

            self.conn.commit()

    def _set_metadata(self, key: str, value: str):
        """Store metadata in the database"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)", (key, value))
            self.conn.commit()

    def _get_metadata(self, key: str, default: str = None) -> Optional[str]:
        """Retrieve metadata from the database"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT value FROM metadata WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else default

    def extract_and_save(
        self,
        output_path: str,
        db_manager,
        project_segments: List,
        tm_ids: List[str],
        tm_names: List[str] = None,
        source_lang: str = None,
        target_lang: str = None,
        threshold: float = 0.80,
        project_name: str = None,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Tuple[int, str]:
        """
        Extract segments from TMs and save to .svtm file.

        Args:
            output_path: Path for the .svtm file
            db_manager: The main database manager with TM data
            project_segments: List of project segments to find matches for
            tm_ids: List of TM IDs to extract from
            tm_names: List of TM names (for display/metadata)
            source_lang: Source language filter
            target_lang: Target language filter
            threshold: Minimum similarity threshold (0.0-1.0)
            project_name: Project name for metadata
            progress_callback: Optional callback(current, total, message)

        Returns:
            Tuple of (segments_extracted, output_path)
        """
        start_time = time.time()

        # Close any existing connection
        if self.conn:
            self.conn.close()
            self.conn = None

        # Remove existing file if present
        if os.path.exists(output_path):
            os.remove(output_path)

        # Create new database file
        self.file_path = output_path
        self.conn = sqlite3.connect(output_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        # Create schema
        self._create_schema()

        # Store metadata
        self._set_metadata('project_name', project_name or 'Unknown')
        self._set_metadata('source_lang', source_lang or '')
        self._set_metadata('target_lang', target_lang or '')
        self._set_metadata('threshold', str(threshold))
        self._set_metadata('tm_ids', ','.join(tm_ids) if tm_ids else '')
        self._set_metadata('tm_names', ','.join(tm_names) if tm_names else '')
        self._set_metadata('created_at', time.strftime('%Y-%m-%d %H:%M:%S'))

        if not project_segments or not db_manager or not tm_ids:
            self.is_loaded = True
            self.segment_count = 0
            return 0, output_path

        # Get unique source texts from project
        unique_sources = {}
        for seg in project_segments:
            # Try both 'source' and 'source_text' attributes (different segment types use different names)
            source = getattr(seg, 'source', None) or getattr(seg, 'source_text', None)
            if source and source.strip():
                key = source.strip().lower()
                if key not in unique_sources:
                    unique_sources[key] = source.strip()

        total = len(unique_sources)
        if total == 0:
            self.is_loaded = True
            self.segment_count = 0
            return 0, output_path

        extracted_count = 0
        seen_sources = set()
        cursor = self.conn.cursor()

        tm_names_str = ', '.join(tm_names) if tm_names else 'Selected TMs'

        for i, (key, source_text) in enumerate(unique_sources.items()):
            if progress_callback:
                progress_callback(i, total, f"Searching: {tm_names_str}")

            try:
                # Search TMs for fuzzy matches
                matches = db_manager.search_fuzzy_matches(
                    source_text,
                    tm_ids=tm_ids,
                    threshold=threshold,
                    max_results=10,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    bidirectional=True
                )

                for match in matches:
                    match_source = match.get('source_text', '')
                    match_target = match.get('target_text', '')

                    if not match_source or not match_target:
                        continue

                    # Deduplicate
                    source_key = match_source.strip().lower()
                    if source_key in seen_sources:
                        continue
                    seen_sources.add(source_key)

                    cursor.execute("""
                        INSERT INTO segments (source_text, target_text, source_lower,
                                            tm_id, tm_name, similarity, original_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        match_source,
                        match_target,
                        source_key,
                        match.get('tm_id'),
                        match.get('tm_name', 'Unknown'),
                        match.get('similarity', 0),
                        match.get('id')
                    ))
                    extracted_count += 1

            except Exception as e:
                pass  # Continue on errors

        # Commit and rebuild FTS
        self.conn.commit()

        try:
            cursor.execute("INSERT INTO segments_fts(segments_fts) VALUES('rebuild')")
            self.conn.commit()
        except Exception:
            pass

        # Update metadata with final count
        elapsed = time.time() - start_time
        self._set_metadata('segment_count', str(extracted_count))
        self._set_metadata('extraction_time', f"{elapsed:.1f}s")

        if progress_callback:
            progress_callback(total, total, f"Complete: {extracted_count} segments")

        self.is_loaded = True
        self.segment_count = extracted_count

        return extracted_count, output_path

    def load(self, file_path: str) -> bool:
        """
        Load an existing .svtm file.

        Args:
            file_path: Path to the .svtm file

        Returns:
            True if loaded successfully, False otherwise
        """
        if not os.path.exists(file_path):
            return False

        try:
            # Close existing connection
            if self.conn:
                self.conn.close()

            self.file_path = file_path
            self.conn = sqlite3.connect(file_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row

            # Load metadata
            self.metadata = {
                'project_name': self._get_metadata('project_name', 'Unknown'),
                'source_lang': self._get_metadata('source_lang', ''),
                'target_lang': self._get_metadata('target_lang', ''),
                'threshold': self._get_metadata('threshold', '0.80'),
                'tm_ids': self._get_metadata('tm_ids', ''),
                'tm_names': self._get_metadata('tm_names', ''),
                'created_at': self._get_metadata('created_at', ''),
                'segment_count': self._get_metadata('segment_count', '0'),
                'extraction_time': self._get_metadata('extraction_time', ''),
            }

            # Get actual segment count
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM segments")
            self.segment_count = cursor.fetchone()[0]

            self.is_loaded = True
            return True

        except Exception as e:
            self.is_loaded = False
            return False

    def search(self, source_text: str, max_results: int = 5) -> List[Dict]:
        """
        Search ExtractTM for matches.

        Args:
            source_text: Source text to search for
            max_results: Maximum results to return

        Returns:
            List of match dictionaries
        """
        if not self.is_loaded or not source_text or not self.conn:
            return []

        source_lower = source_text.strip().lower()
        results = []

        with self.lock:
            cursor = self.conn.cursor()

            # 1. Exact match
            cursor.execute("SELECT * FROM segments WHERE source_lower = ? LIMIT 1", (source_lower,))
            exact = cursor.fetchone()

            if exact:
                results.append({
                    'source_text': exact['source_text'],
                    'target_text': exact['target_text'],
                    'tm_id': exact['tm_id'],
                    'tm_name': exact['tm_name'] + ' (Extract)',
                    'similarity': 1.0,
                    'match_pct': 100,
                    'id': exact['original_id']
                })
                return results

            # 2. FTS5 fuzzy search
            try:
                clean_text = re.sub(r'[^\w\s]', ' ', source_text)
                search_terms = [t for t in clean_text.split() if len(t) > 2]

                if search_terms:
                    fts_query = ' OR '.join(f'"{term}"' for term in search_terms[:10])

                    cursor.execute("""
                        SELECT s.*, bm25(segments_fts) as rank
                        FROM segments s
                        JOIN segments_fts ON s.id = segments_fts.rowid
                        WHERE segments_fts MATCH ?
                        ORDER BY rank
                        LIMIT ?
                    """, (fts_query, max_results * 3))

                    candidates = cursor.fetchall()

                    for row in candidates:
                        similarity = self._calculate_similarity(source_text, row['source_text'])
                        if similarity >= 0.5:
                            results.append({
                                'source_text': row['source_text'],
                                'target_text': row['target_text'],
                                'tm_id': row['tm_id'],
                                'tm_name': row['tm_name'] + ' (Extract)',
                                'similarity': similarity,
                                'match_pct': int(similarity * 100),
                                'id': row['original_id']
                            })

                    results.sort(key=lambda x: x['similarity'], reverse=True)
                    results = results[:max_results]

            except Exception:
                pass

        return results

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        clean1 = re.sub(r'<[^>]+>', '', text1).lower()
        clean2 = re.sub(r'<[^>]+>', '', text2).lower()
        return SequenceMatcher(None, clean1, clean2).ratio()

    def export_to_tmx(self, output_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> int:
        """
        Export the ExtractTM to a TMX file.

        Args:
            output_path: Path for the TMX file
            progress_callback: Optional callback(current, total)

        Returns:
            Number of segments exported
        """
        if not self.is_loaded or not self.conn:
            return 0

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM segments")
            rows = cursor.fetchall()

        if not rows:
            return 0

        source_lang = self.metadata.get('source_lang', 'en')
        target_lang = self.metadata.get('target_lang', 'nl')

        # Build TMX content
        tmx_header = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE tmx SYSTEM "tmx14.dtd">
<tmx version="1.4">
  <header creationtool="Supervertaler" creationtoolversion="1.0"
          datatype="plaintext" segtype="sentence"
          adminlang="en" srclang="{source_lang}" o-tmf="Supervertaler">
  </header>
  <body>
'''
        tmx_footer = '''  </body>
</tmx>
'''

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(tmx_header)

            for i, row in enumerate(rows):
                if progress_callback and i % 100 == 0:
                    progress_callback(i, len(rows))

                source = self._escape_xml(row['source_text'])
                target = self._escape_xml(row['target_text'])

                tu = f'''    <tu>
      <tuv xml:lang="{source_lang}">
        <seg>{source}</seg>
      </tuv>
      <tuv xml:lang="{target_lang}">
        <seg>{target}</seg>
      </tuv>
    </tu>
'''
                f.write(tu)

            f.write(tmx_footer)

        if progress_callback:
            progress_callback(len(rows), len(rows))

        return len(rows)

    def _escape_xml(self, text: str) -> str:
        """Escape XML special characters"""
        if not text:
            return ''
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))

    def get_info(self) -> Dict:
        """Get information about the loaded ExtractTM"""
        return {
            'file_path': self.file_path,
            'is_loaded': self.is_loaded,
            'segment_count': self.segment_count,
            **self.metadata
        }

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
        self.is_loaded = False


def get_extract_path(project_path: str) -> str:
    """
    Get the expected Extract TM path for a project.

    Args:
        project_path: Path to the project file (.sproj)

    Returns:
        Path to the Extract TM file (.svtm)
    """
    project_dir = os.path.dirname(project_path)
    project_name = os.path.splitext(os.path.basename(project_path))[0]
    return os.path.join(project_dir, f"{project_name}_Extract.svtm")


def extract_exists(project_path: str) -> bool:
    """Check if an Extract TM exists for a project"""
    return os.path.exists(get_extract_path(project_path))
