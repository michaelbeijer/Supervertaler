"""
ProjectTM - In-memory TM for instant grid lookups (Total Recall architecture)

This module implements a lightweight in-memory Translation Memory that extracts
relevant segments from the full TM database on project load. This makes grid
navigation instant while keeping the full TM for concordance searches.

Inspired by CafeTran's "Total Recall" feature.
"""

import sqlite3
import threading
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Callable
import re


class ProjectTM:
    """
    Lightweight in-memory TM extracted from the main TM database.

    On project load, extracts segments that are relevant to the current project
    (fuzzy matches above threshold) into an in-memory SQLite database for
    instant lookups during grid navigation.

    Usage:
        project_tm = ProjectTM()
        project_tm.extract_from_database(
            db_manager,
            project_segments,
            tm_ids=['tm1', 'tm2'],
            threshold=0.75,
            progress_callback=lambda cur, total: print(f"{cur}/{total}")
        )

        # Fast lookup during grid navigation
        matches = project_tm.search("source text to translate")
    """

    def __init__(self):
        """Initialize in-memory SQLite database for ProjectTM"""
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        self.is_built = False
        self.segment_count = 0

        # Create the schema
        self._create_schema()

    def _create_schema(self):
        """Create the in-memory database schema"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS segments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text TEXT NOT NULL,
                    target_text TEXT NOT NULL,
                    source_lower TEXT NOT NULL,
                    tm_id TEXT,
                    tm_name TEXT,
                    similarity REAL,
                    original_id INTEGER
                )
            """)
            # Index for fast exact match lookups
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_source_lower ON segments(source_lower)")
            # FTS5 for fuzzy text search
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS segments_fts USING fts5(
                    source_text,
                    content=segments,
                    content_rowid=id
                )
            """)
            self.conn.commit()

    def clear(self):
        """Clear all segments from the ProjectTM"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM segments")
            cursor.execute("DELETE FROM segments_fts")
            self.conn.commit()
            self.is_built = False
            self.segment_count = 0

    def extract_from_database(
        self,
        db_manager,
        project_segments: List,
        tm_ids: List[str] = None,
        source_lang: str = None,
        target_lang: str = None,
        threshold: float = 0.75,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        log_callback: Optional[Callable[[str], None]] = None
    ) -> int:
        """
        Extract relevant segments from the main TM database into ProjectTM.

        For each unique source text in the project, searches the TM for fuzzy
        matches above the threshold and stores them in memory.

        Args:
            db_manager: The main database manager with TM data
            project_segments: List of project segments to find matches for
            tm_ids: List of TM IDs to search (None = all active TMs)
            source_lang: Source language filter
            target_lang: Target language filter
            threshold: Minimum similarity threshold (0.0-1.0)
            progress_callback: Optional callback(current, total) for progress
            log_callback: Optional callback(message) for logging

        Returns:
            Number of TM segments extracted
        """
        def log(msg):
            if log_callback:
                log_callback(msg)
            else:
                print(msg)

        self.clear()

        if not project_segments or not db_manager:
            log(f"[ProjectTM] Early exit: segments={bool(project_segments)}, db={bool(db_manager)}")
            return 0

        # Get unique source texts from project
        unique_sources = {}
        for seg in project_segments:
            # Try both 'source' and 'source_text' attributes (different segment types use different names)
            source = getattr(seg, 'source', None) or getattr(seg, 'source_text', None)
            if source and source.strip():
                # Normalize: strip and lowercase for deduplication
                key = source.strip().lower()
                if key not in unique_sources:
                    unique_sources[key] = source.strip()

        total = len(unique_sources)
        log(f"[ProjectTM] Found {total} unique source texts from {len(project_segments)} segments")
        if total == 0:
            return 0

        extracted_count = 0
        seen_sources = set()  # Deduplicate TM entries

        cursor = self.conn.cursor()

        log(f"[ProjectTM] Searching TMs: {tm_ids}, threshold={threshold}, langs={source_lang}->{target_lang}")

        for i, (key, source_text) in enumerate(unique_sources.items()):
            if progress_callback and i % 10 == 0:
                progress_callback(i, total)

            try:
                # Search main TM database for fuzzy matches
                matches = db_manager.search_fuzzy_matches(
                    source_text,
                    tm_ids=tm_ids,
                    threshold=threshold,
                    max_results=10,  # Keep top 10 matches per source
                    source_lang=source_lang,
                    target_lang=target_lang,
                    bidirectional=True
                )

                # Debug: log first search
                if i == 0:
                    log(f"[ProjectTM] First search '{source_text[:50]}...' returned {len(matches)} matches")

                for match in matches:
                    match_source = match.get('source_text', '')
                    match_target = match.get('target_text', '')

                    if not match_source or not match_target:
                        continue

                    # Deduplicate by source text
                    source_key = match_source.strip().lower()
                    if source_key in seen_sources:
                        continue
                    seen_sources.add(source_key)

                    # Insert into ProjectTM
                    cursor.execute("""
                        INSERT INTO segments (source_text, target_text, source_lower,
                                            tm_id, tm_name, similarity, original_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        match_source,
                        match_target,
                        source_key,
                        match.get('tm_id'),
                        match.get('tm_name', 'Unknown TM'),
                        match.get('similarity', 0),
                        match.get('id')
                    ))
                    extracted_count += 1

            except Exception as e:
                # Log but continue - don't fail extraction for one bad segment
                pass

        # Commit all inserts
        self.conn.commit()

        # Rebuild FTS5 index
        try:
            cursor.execute("INSERT INTO segments_fts(segments_fts) VALUES('rebuild')")
            self.conn.commit()
        except Exception:
            pass  # FTS rebuild may fail if no data, that's OK

        if progress_callback:
            progress_callback(total, total)

        self.is_built = True
        self.segment_count = extracted_count

        return extracted_count

    def search(self, source_text: str, max_results: int = 5) -> List[Dict]:
        """
        Search ProjectTM for matches (instant lookup).

        First checks for exact matches, then falls back to fuzzy search.

        Args:
            source_text: Source text to search for
            max_results: Maximum number of results to return

        Returns:
            List of match dictionaries with source_text, target_text, similarity, etc.
        """
        if not self.is_built or not source_text:
            return []

        source_lower = source_text.strip().lower()
        results = []

        with self.lock:
            cursor = self.conn.cursor()

            # 1. Check for exact match first (fastest)
            cursor.execute("""
                SELECT * FROM segments WHERE source_lower = ? LIMIT 1
            """, (source_lower,))
            exact = cursor.fetchone()

            if exact:
                results.append({
                    'source_text': exact['source_text'],
                    'target_text': exact['target_text'],
                    'tm_id': exact['tm_id'],
                    'tm_name': exact['tm_name'],
                    'similarity': 1.0,  # Exact match
                    'match_pct': 100,
                    'id': exact['original_id']
                })
                return results  # Exact match - no need to search further

            # 2. FTS5 fuzzy search
            try:
                # Tokenize query for FTS5
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
                    """, (fts_query, max_results * 3))  # Get more candidates for re-ranking

                    candidates = cursor.fetchall()

                    # Re-rank by actual similarity
                    for row in candidates:
                        similarity = self._calculate_similarity(source_text, row['source_text'])
                        if similarity >= 0.5:  # Lower threshold for ProjectTM (pre-filtered)
                            results.append({
                                'source_text': row['source_text'],
                                'target_text': row['target_text'],
                                'tm_id': row['tm_id'],
                                'tm_name': row['tm_name'],
                                'similarity': similarity,
                                'match_pct': int(similarity * 100),
                                'id': row['original_id']
                            })

                    # Sort by similarity and limit
                    results.sort(key=lambda x: x['similarity'], reverse=True)
                    results = results[:max_results]

            except Exception:
                pass  # FTS search may fail, return what we have

        return results

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity ratio between two texts"""
        # Strip HTML/XML tags for comparison
        clean1 = re.sub(r'<[^>]+>', '', text1).lower()
        clean2 = re.sub(r'<[^>]+>', '', text2).lower()
        return SequenceMatcher(None, clean1, clean2).ratio()

    def get_stats(self) -> Dict:
        """Get statistics about the ProjectTM"""
        return {
            'is_built': self.is_built,
            'segment_count': self.segment_count
        }
