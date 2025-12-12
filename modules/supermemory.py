"""
Supermemory - Vector-Indexed Translation Memory
================================================
Semantic search across translation memories using embeddings.
Provides AI-enhanced TM matching that understands meaning, not just text similarity.

Features:
- Import TMX files into vector database
- Semantic search (find by meaning, not fuzzy match)
- Cross-TM search (search all indexed TMs at once)
- LLM context injection (provide relevant examples to Ollama/Claude)
- Terminology mining (find how terms were translated historically)

Technical:
- Uses ChromaDB for vector storage (local, no cloud)
- Sentence-transformers for embeddings (local)
- SQLite for metadata

Author: Supervertaler
"""

import os
import json
import hashlib
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
import re
import threading

# Optional imports - will be checked at runtime
CHROMADB_AVAILABLE = False
SENTENCE_TRANSFORMERS_AVAILABLE = None  # None = not yet checked, False = failed, True = available
SENTENCE_TRANSFORMERS_ERROR = None  # Store error message if import fails
SentenceTransformer = None  # Will be set on first use

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    pass

# NOTE: sentence_transformers is imported lazily in _lazy_load_sentence_transformers()
# to avoid DLL crashes at module load time on Windows


def _lazy_load_sentence_transformers():
    """Lazily load sentence_transformers to avoid DLL crashes at startup."""
    global SENTENCE_TRANSFORMERS_AVAILABLE, SENTENCE_TRANSFORMERS_ERROR, SentenceTransformer
    
    if SENTENCE_TRANSFORMERS_AVAILABLE is not None:
        return SENTENCE_TRANSFORMERS_AVAILABLE
    
    try:
        from sentence_transformers import SentenceTransformer as ST
        SentenceTransformer = ST
        SENTENCE_TRANSFORMERS_AVAILABLE = True
        return True
    except (ImportError, OSError, Exception) as e:
        # Catch DLL loading errors on Windows (common with PyTorch)
        SENTENCE_TRANSFORMERS_AVAILABLE = False
        SENTENCE_TRANSFORMERS_ERROR = str(e)
        return False


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class MemoryEntry:
    """Single translation memory entry"""
    source: str
    target: str
    source_lang: str
    target_lang: str
    tm_name: str
    tm_id: str
    entry_id: str
    metadata: Dict = field(default_factory=dict)
    similarity: float = 0.0  # For search results
    domain: str = ""  # Domain category (e.g., "patents", "medical", "legal")


@dataclass 
class IndexedTM:
    """Metadata about an indexed translation memory"""
    tm_id: str
    name: str
    file_path: str
    source_lang: str
    target_lang: str
    entry_count: int
    indexed_date: str
    file_hash: str
    status: str = "ready"  # ready, indexing, error
    domain: str = ""  # Domain category for this TM
    active: bool = True  # Whether this TM is active for searching


@dataclass
class SearchResult:
    """Search result with semantic similarity"""
    entry: MemoryEntry
    similarity: float
    rank: int
    domain: str = ""  # Domain of the source TM


@dataclass
class Domain:
    """Translation domain category"""
    name: str
    description: str = ""
    color: str = "#4A90D9"  # UI color for visual distinction
    active: bool = True  # Whether this domain is active for current project


# =============================================================================
# EMBEDDING MODELS
# =============================================================================

# Recommended models for translation (multilingual, efficient)
EMBEDDING_MODELS = {
    "paraphrase-multilingual-MiniLM-L12-v2": {
        "name": "Multilingual MiniLM",
        "description": "Fast, good quality, 50+ languages",
        "dimensions": 384,
        "size_mb": 420,
        "recommended": True
    },
    "paraphrase-multilingual-mpnet-base-v2": {
        "name": "Multilingual MPNet",
        "description": "Better quality, slower, 50+ languages", 
        "dimensions": 768,
        "size_mb": 970,
        "recommended": False
    },
    "distiluse-base-multilingual-cased-v2": {
        "name": "DistilUSE Multilingual",
        "description": "Good balance of speed/quality",
        "dimensions": 512,
        "size_mb": 480,
        "recommended": False
    }
}

DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


# =============================================================================
# SUPERMEMORY ENGINE
# =============================================================================

class SupermemoryEngine:
    """
    Core engine for vector-indexed translation memory.
    Handles indexing, searching, and LLM context generation.
    """
    
    def __init__(self, data_dir: Path, log_callback: Callable = None):
        """
        Initialize the Supermemory engine.
        
        Args:
            data_dir: Directory for storing database and indexes
            log_callback: Optional logging function
        """
        self.data_dir = Path(data_dir)
        self.supermemory_dir = self.data_dir / "supermemory"
        self.supermemory_dir.mkdir(parents=True, exist_ok=True)
        
        self.log = log_callback or print
        
        # Database paths
        self.metadata_db_path = self.supermemory_dir / "metadata.db"
        self.chroma_path = self.supermemory_dir / "chroma_db"
        
        # State
        self.embedding_model = None
        self.embedding_model_name = None
        self.chroma_client = None
        self.collection = None
        
        # Initialize metadata database
        self._init_metadata_db()
        
    def _init_metadata_db(self):
        """Initialize SQLite database for TM metadata"""
        conn = sqlite3.connect(str(self.metadata_db_path))
        cursor = conn.cursor()
        
        # Table for indexed TMs (with domain support)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS indexed_tms (
                tm_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                file_path TEXT,
                source_lang TEXT,
                target_lang TEXT,
                entry_count INTEGER DEFAULT 0,
                indexed_date TEXT,
                file_hash TEXT,
                status TEXT DEFAULT 'ready',
                domain TEXT DEFAULT ''
            )
        """)
        
        # Table for domains
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS domains (
                name TEXT PRIMARY KEY,
                description TEXT DEFAULT '',
                color TEXT DEFAULT '#4A90D9',
                active INTEGER DEFAULT 1
            )
        """)
        
        # Table for settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        # Run migrations for existing databases
        self._migrate_database(cursor)
        
        conn.commit()
        conn.close()
    
    def _migrate_database(self, cursor):
        """Apply database migrations for existing installations"""
        # Check if domain column exists in indexed_tms
        cursor.execute("PRAGMA table_info(indexed_tms)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'domain' not in columns:
            cursor.execute("ALTER TABLE indexed_tms ADD COLUMN domain TEXT DEFAULT ''")
        
        if 'active' not in columns:
            cursor.execute("ALTER TABLE indexed_tms ADD COLUMN active INTEGER DEFAULT 1")
        
        # Insert default domains if table is empty
        cursor.execute("SELECT COUNT(*) FROM domains")
        if cursor.fetchone()[0] == 0:
            default_domains = [
                ("General", "General purpose translations", "#808080", 1),
                ("Patents", "Patent and intellectual property documents", "#4A90D9", 1),
                ("Medical", "Medical and pharmaceutical content", "#D94A4A", 1),
                ("Legal", "Legal contracts and documents", "#8B4513", 1),
                ("Technical", "Technical manuals and documentation", "#4AD94A", 1),
                ("Marketing", "Marketing and advertising content", "#D9D94A", 1),
                ("Financial", "Financial and banking documents", "#9B59B6", 1),
                ("Software", "Software UI and documentation", "#3498DB", 1),
            ]
            cursor.executemany(
                "INSERT OR IGNORE INTO domains (name, description, color, active) VALUES (?, ?, ?, ?)",
                default_domains
            )
        
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if required dependencies are available"""
        # Lazy load sentence_transformers to avoid DLL crashes at startup
        st_available = _lazy_load_sentence_transformers()
        return {
            "chromadb": CHROMADB_AVAILABLE,
            "sentence_transformers": st_available,
            "ready": CHROMADB_AVAILABLE and st_available
        }
    
    def get_missing_dependencies(self) -> List[str]:
        """Get list of missing dependencies with install commands"""
        # Lazy load sentence_transformers to avoid DLL crashes at startup
        st_available = _lazy_load_sentence_transformers()
        missing = []
        if not CHROMADB_AVAILABLE:
            missing.append("chromadb")
        if not st_available:
            missing.append("sentence-transformers")
        return missing
    
    def initialize(self, model_name: str = None) -> bool:
        """
        Initialize the embedding model and ChromaDB.
        
        Args:
            model_name: Embedding model to use (default: multilingual MiniLM)
            
        Returns:
            True if initialization successful
        """
        deps = self.check_dependencies()
        if not deps["ready"]:
            self.log(f"[Supermemory] Missing dependencies: {self.get_missing_dependencies()}")
            return False
        
        try:
            model_name = model_name or DEFAULT_MODEL
            
            # Load embedding model
            self.log(f"[Supermemory] Loading embedding model: {model_name}")
            self.embedding_model = SentenceTransformer(model_name)
            self.embedding_model_name = model_name
            self.log(f"[Supermemory] Model loaded successfully")
            
            # Initialize ChromaDB
            self.log(f"[Supermemory] Initializing ChromaDB at {self.chroma_path}")
            self.chroma_client = chromadb.PersistentClient(
                path=str(self.chroma_path),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="translation_memory",
                metadata={"description": "Supervertaler Translation Memory Vectors"}
            )
            
            # Note: Avoid calling collection.count() immediately after creation
            # ChromaDB 1.3.x Rust backend can have race conditions
            self.log(f"[Supermemory] Collection initialized successfully")
            return True

        except Exception as e:
            error_msg = str(e)
            self.log(f"[Supermemory] Initialization error: {error_msg}")

            # Provide helpful instructions for common Windows DLL errors
            if "DLL" in error_msg or "c10.dll" in error_msg or "torch" in error_msg.lower():
                self.log("[Supermemory] 💡 PyTorch DLL loading failed. Try these fixes:")
                self.log("[Supermemory]   1. Install Visual C++ Redistributables:")
                self.log("[Supermemory]      https://aka.ms/vs/17/release/vc_redist.x64.exe")
                self.log("[Supermemory]   2. Reinstall PyTorch:")
                self.log("[Supermemory]      pip uninstall torch sentence-transformers")
                self.log("[Supermemory]      pip install torch sentence-transformers")
                self.log("[Supermemory]   3. Or disable Supermemory auto-init in Settings → AI Settings")

            return False
    
    def is_initialized(self) -> bool:
        """Check if engine is ready for use"""
        return (self.embedding_model is not None and 
                self.chroma_client is not None and 
                self.collection is not None)
    
    # =========================================================================
    # TMX PARSING
    # =========================================================================
    
    def _parse_tmx(self, tmx_path: Path, progress_callback: Callable = None) -> List[MemoryEntry]:
        """
        Parse a TMX file and extract translation units.
        
        Args:
            tmx_path: Path to TMX file
            progress_callback: Optional callback(current, total, message)
            
        Returns:
            List of MemoryEntry objects
        """
        entries = []
        
        try:
            # Parse XML
            tree = ET.parse(str(tmx_path))
            root = tree.getroot()
            
            # Get header info
            header = root.find('.//header')
            source_lang = header.get('srclang', 'en') if header is not None else 'en'
            
            # Find all translation units
            tus = root.findall('.//tu')
            total = len(tus)
            
            tm_name = tmx_path.stem
            tm_id = self._generate_tm_id(tmx_path)
            
            for i, tu in enumerate(tus):
                if progress_callback and i % 100 == 0:
                    progress_callback(i, total, f"Parsing {tm_name}...")
                
                tuvs = tu.findall('.//tuv')
                if len(tuvs) < 2:
                    continue
                
                # Extract source and target
                source_text = None
                target_text = None
                target_lang = None
                
                for tuv in tuvs:
                    lang = tuv.get('{http://www.w3.org/XML/1998/namespace}lang', '') or tuv.get('lang', '')
                    seg = tuv.find('.//seg')
                    
                    if seg is not None and seg.text:
                        text = self._clean_segment_text(seg)
                        
                        # First tuv is usually source
                        if source_text is None:
                            source_text = text
                            if lang:
                                source_lang = lang
                        else:
                            target_text = text
                            target_lang = lang
                
                if source_text and target_text:
                    entry_id = f"{tm_id}_{i}"
                    entries.append(MemoryEntry(
                        source=source_text,
                        target=target_text,
                        source_lang=source_lang[:2].lower() if source_lang else 'en',
                        target_lang=target_lang[:2].lower() if target_lang else 'xx',
                        tm_name=tm_name,
                        tm_id=tm_id,
                        entry_id=entry_id
                    ))
            
            if progress_callback:
                progress_callback(total, total, f"Parsed {len(entries)} entries")
                
        except Exception as e:
            self.log(f"[Supermemory] Error parsing TMX {tmx_path}: {e}")
            
        return entries
    
    def _clean_segment_text(self, seg_element) -> str:
        """Extract and clean text from a seg element, handling inline tags"""
        # Get all text including tail of child elements
        texts = []
        
        if seg_element.text:
            texts.append(seg_element.text)
            
        for child in seg_element:
            # Include child's tail (text after the tag)
            if child.tail:
                texts.append(child.tail)
        
        text = ''.join(texts)
        # Clean up whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    def _generate_tm_id(self, file_path: Path) -> str:
        """Generate unique ID for a TM based on file path"""
        return hashlib.md5(str(file_path).encode()).hexdigest()[:12]
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate hash of file for change detection"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    # =========================================================================
    # INDEXING
    # =========================================================================
    
    def index_tmx(self, tmx_path: Path, progress_callback: Callable = None, 
                  domain: str = "") -> Optional[IndexedTM]:
        """
        Index a TMX file into the vector database.
        
        Args:
            tmx_path: Path to TMX file
            progress_callback: Optional callback(current, total, message)
            domain: Domain category for this TM (e.g., "Patents", "Medical")
            
        Returns:
            IndexedTM metadata or None if failed
        """
        if not self.is_initialized():
            self.log("[Supermemory] Engine not initialized")
            return None
        
        tmx_path = Path(tmx_path)
        if not tmx_path.exists():
            self.log(f"[Supermemory] File not found: {tmx_path}")
            return None
        
        tm_id = self._generate_tm_id(tmx_path)
        file_hash = self._calculate_file_hash(tmx_path)
        
        # Check if already indexed with same hash
        existing = self.get_indexed_tm(tm_id)
        if existing and existing.file_hash == file_hash:
            # If domain changed, update it
            if domain and existing.domain != domain:
                self.update_tm_domain(tm_id, domain)
                existing.domain = domain
            self.log(f"[Supermemory] TM already indexed: {tmx_path.name}")
            return existing
        
        # If exists but hash changed, remove old entries
        if existing:
            self.log(f"[Supermemory] TM changed, re-indexing: {tmx_path.name}")
            self._remove_tm_entries(tm_id)
        
        try:
            # Parse TMX
            if progress_callback:
                progress_callback(0, 100, f"Parsing {tmx_path.name}...")
            
            entries = self._parse_tmx(tmx_path, progress_callback)
            
            if not entries:
                self.log(f"[Supermemory] No entries found in {tmx_path.name}")
                return None
            
            # Generate embeddings and add to ChromaDB
            total = len(entries)
            batch_size = 100
            
            for batch_start in range(0, total, batch_size):
                batch_end = min(batch_start + batch_size, total)
                batch = entries[batch_start:batch_end]
                
                if progress_callback:
                    progress_callback(batch_start, total, f"Indexing {tmx_path.name}...")
                
                # Prepare batch data
                ids = [e.entry_id for e in batch]
                documents = [e.source for e in batch]  # Embed source text
                metadatas = [
                    {
                        "source": e.source,
                        "target": e.target,
                        "source_lang": e.source_lang,
                        "target_lang": e.target_lang,
                        "tm_name": e.tm_name,
                        "tm_id": e.tm_id,
                        "domain": domain  # Include domain in metadata
                    }
                    for e in batch
                ]
                
                # Generate embeddings
                embeddings = self.embedding_model.encode(documents).tolist()
                
                # Add to ChromaDB
                self.collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas
                )
            
            # Save metadata
            indexed_tm = IndexedTM(
                tm_id=tm_id,
                name=tmx_path.stem,
                file_path=str(tmx_path),
                source_lang=entries[0].source_lang if entries else 'en',
                target_lang=entries[0].target_lang if entries else 'xx',
                entry_count=len(entries),
                indexed_date=datetime.now().isoformat(),
                file_hash=file_hash,
                status="ready",
                domain=domain
            )
            
            self._save_indexed_tm(indexed_tm)
            
            if progress_callback:
                progress_callback(total, total, f"Indexed {total} entries")
            
            self.log(f"[Supermemory] Indexed {len(entries)} entries from {tmx_path.name}")
            return indexed_tm
            
        except Exception as e:
            self.log(f"[Supermemory] Error indexing {tmx_path}: {e}")
            return None
    
    def _remove_tm_entries(self, tm_id: str):
        """Remove all entries for a TM from the collection"""
        try:
            # ChromaDB allows filtering by metadata
            self.collection.delete(
                where={"tm_id": tm_id}
            )
        except Exception as e:
            self.log(f"[Supermemory] Error removing entries: {e}")
    
    def _save_indexed_tm(self, tm: IndexedTM):
        """Save TM metadata to database"""
        conn = sqlite3.connect(str(self.metadata_db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO indexed_tms 
            (tm_id, name, file_path, source_lang, target_lang, entry_count, indexed_date, file_hash, status, domain)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tm.tm_id, tm.name, tm.file_path, tm.source_lang, tm.target_lang,
            tm.entry_count, tm.indexed_date, tm.file_hash, tm.status, tm.domain
        ))
        
        conn.commit()
        conn.close()
    
    def get_indexed_tm(self, tm_id: str) -> Optional[IndexedTM]:
        """Get metadata for an indexed TM"""
        conn = sqlite3.connect(str(self.metadata_db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM indexed_tms WHERE tm_id = ?", (tm_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return IndexedTM(
                tm_id=row[0], name=row[1], file_path=row[2],
                source_lang=row[3], target_lang=row[4], entry_count=row[5],
                indexed_date=row[6], file_hash=row[7], status=row[8],
                domain=row[9] if len(row) > 9 else ""
            )
        return None
    
    def get_all_indexed_tms(self) -> List[IndexedTM]:
        """Get all indexed TMs"""
        conn = sqlite3.connect(str(self.metadata_db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM indexed_tms ORDER BY indexed_date DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            IndexedTM(
                tm_id=row[0], name=row[1], file_path=row[2],
                source_lang=row[3], target_lang=row[4], entry_count=row[5],
                indexed_date=row[6], file_hash=row[7], status=row[8],
                domain=row[9] if len(row) > 9 else "",
                active=bool(row[10]) if len(row) > 10 else True
            )
            for row in rows
        ]
    
    def set_tm_active(self, tm_id: str, active: bool) -> bool:
        """Set the active state of a TM"""
        try:
            conn = sqlite3.connect(str(self.metadata_db_path))
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE indexed_tms SET active = ? WHERE tm_id = ?",
                (1 if active else 0, tm_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.log(f"[Supermemory] Error setting TM active state: {e}")
            return False
    
    def get_active_tm_ids(self) -> List[str]:
        """Get list of TM IDs that are marked as active"""
        conn = sqlite3.connect(str(self.metadata_db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT tm_id FROM indexed_tms WHERE active = 1")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
    
    def remove_indexed_tm(self, tm_id: str) -> bool:
        """Remove an indexed TM completely"""
        try:
            # Remove from ChromaDB
            self._remove_tm_entries(tm_id)
            
            # Remove from metadata
            conn = sqlite3.connect(str(self.metadata_db_path))
            cursor = conn.cursor()
            cursor.execute("DELETE FROM indexed_tms WHERE tm_id = ?", (tm_id,))
            conn.commit()
            conn.close()
            
            self.log(f"[Supermemory] Removed TM: {tm_id}")
            return True
            
        except Exception as e:
            self.log(f"[Supermemory] Error removing TM: {e}")
            return False
    
    # =========================================================================
    # SEARCHING
    # =========================================================================
    
    def search(self, query: str, n_results: int = 10, 
               source_lang: str = None, target_lang: str = None,
               tm_ids: List[str] = None, domains: List[str] = None) -> List[SearchResult]:
        """
        Semantic search across indexed TMs.
        
        Args:
            query: Text to search for
            n_results: Maximum results to return
            source_lang: Filter by source language (optional)
            target_lang: Filter by target language (optional)
            tm_ids: Filter by specific TMs (optional)
            domains: Filter by specific domains (optional)
            
        Returns:
            List of SearchResult objects sorted by similarity
        """
        if not self.is_initialized():
            return []
        
        if not query or not query.strip():
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Build filter - ChromaDB requires $and for multiple conditions
            where_conditions = []
            if source_lang:
                where_conditions.append({"source_lang": source_lang.lower()[:2]})
            if target_lang:
                where_conditions.append({"target_lang": target_lang.lower()[:2]})
            if tm_ids:
                where_conditions.append({"tm_id": {"$in": tm_ids}})
            if domains:
                where_conditions.append({"domain": {"$in": domains}})
            
            # Construct proper where filter
            if len(where_conditions) == 0:
                where_filter = None
            elif len(where_conditions) == 1:
                where_filter = where_conditions[0]
            else:
                where_filter = {"$and": where_conditions}
            
            # Search ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )
            
            # Convert to SearchResult objects
            search_results = []
            
            if results and results['ids'] and results['ids'][0]:
                for i, entry_id in enumerate(results['ids'][0]):
                    metadata = results['metadatas'][0][i]
                    distance = results['distances'][0][i]
                    
                    # Convert distance to similarity (ChromaDB uses L2 distance)
                    # Lower distance = more similar
                    similarity = max(0, 1 - (distance / 2))  # Normalize roughly
                    
                    domain = metadata.get('domain', '')
                    
                    entry = MemoryEntry(
                        source=metadata['source'],
                        target=metadata['target'],
                        source_lang=metadata['source_lang'],
                        target_lang=metadata['target_lang'],
                        tm_name=metadata['tm_name'],
                        tm_id=metadata['tm_id'],
                        entry_id=entry_id,
                        similarity=similarity,
                        domain=domain
                    )
                    
                    search_results.append(SearchResult(
                        entry=entry,
                        similarity=similarity,
                        rank=i + 1,
                        domain=domain
                    ))
            
            return search_results
            
        except Exception as e:
            self.log(f"[Supermemory] Search error: {e}")
            return []
    
    def search_by_active_domains(self, query: str, n_results: int = 10,
                                  source_lang: str = None, target_lang: str = None) -> List[SearchResult]:
        """
        Search using currently active domains only.
        
        Args:
            query: Text to search for
            n_results: Maximum results
            source_lang: Source language filter
            target_lang: Target language filter
            
        Returns:
            List of SearchResult filtered by active domains
        """
        active_domains = self.get_domains_for_filter()
        if not active_domains:
            # No domains active = search all
            return self.search(query, n_results, source_lang, target_lang)
        
        return self.search(query, n_results, source_lang, target_lang, domains=active_domains)
    
    def get_context_for_llm(self, source_text: str, n_examples: int = 3,
                           source_lang: str = None, target_lang: str = None,
                           use_active_domains: bool = True) -> str:
        """
        Get relevant TM examples formatted for LLM context injection.
        
        Args:
            source_text: The segment being translated
            n_examples: Number of examples to include
            source_lang: Source language code
            target_lang: Target language code
            use_active_domains: If True, filter by active domains
            
        Returns:
            Formatted string with TM examples for prompt injection
        """
        if use_active_domains:
            results = self.search_by_active_domains(
                source_text, 
                n_results=n_examples,
                source_lang=source_lang,
                target_lang=target_lang
            )
        else:
            results = self.search(
                source_text, 
                n_results=n_examples,
                source_lang=source_lang,
                target_lang=target_lang
            )
        
        if not results:
            return ""
        
        lines = ["Reference translations from translation memory:"]
        
        for r in results:
            similarity_pct = int(r.similarity * 100)
            lines.append(f"• Source: {r.entry.source}")
            lines.append(f"  Target: {r.entry.target}")
            if r.domain:
                lines.append(f"  (Similarity: {similarity_pct}%, Domain: {r.domain})")
            else:
                lines.append(f"  (Similarity: {similarity_pct}%)")
            lines.append("")
        
        return "\n".join(lines)
    
    # =========================================================================
    # DOMAIN MANAGEMENT
    # =========================================================================
    
    def get_all_domains(self) -> List[Domain]:
        """Get all defined domains"""
        conn = sqlite3.connect(str(self.metadata_db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, description, color, active FROM domains ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Domain(name=row[0], description=row[1], color=row[2], active=bool(row[3]))
            for row in rows
        ]
    
    def get_active_domains(self) -> List[Domain]:
        """Get only active domains"""
        return [d for d in self.get_all_domains() if d.active]
    
    def add_domain(self, domain: Domain) -> bool:
        """Add a new domain"""
        try:
            conn = sqlite3.connect(str(self.metadata_db_path))
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO domains (name, description, color, active) VALUES (?, ?, ?, ?)",
                (domain.name, domain.description, domain.color, 1 if domain.active else 0)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.log(f"[Supermemory] Error adding domain: {e}")
            return False
    
    def update_domain(self, name: str, domain: Domain) -> bool:
        """Update an existing domain"""
        try:
            conn = sqlite3.connect(str(self.metadata_db_path))
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE domains SET name=?, description=?, color=?, active=? WHERE name=?",
                (domain.name, domain.description, domain.color, 1 if domain.active else 0, name)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.log(f"[Supermemory] Error updating domain: {e}")
            return False
    
    def delete_domain(self, name: str) -> bool:
        """Delete a domain (does not affect indexed TMs)"""
        try:
            conn = sqlite3.connect(str(self.metadata_db_path))
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM domains WHERE name=?", (name,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.log(f"[Supermemory] Error deleting domain: {e}")
            return False
    
    def set_domain_active(self, name: str, active: bool) -> bool:
        """Set a domain's active status"""
        try:
            conn = sqlite3.connect(str(self.metadata_db_path))
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE domains SET active=? WHERE name=?",
                (1 if active else 0, name)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.log(f"[Supermemory] Error setting domain active status: {e}")
            return False
    
    def get_domains_for_filter(self) -> List[str]:
        """Get list of domain names that are currently active"""
        active = self.get_active_domains()
        return [d.name for d in active]
    
    def get_unique_language_pairs(self) -> List[tuple]:
        """Get all unique language pairs from indexed TMs"""
        conn = sqlite3.connect(str(self.metadata_db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT source_lang, target_lang 
            FROM indexed_tms 
            ORDER BY source_lang, target_lang
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [(row[0], row[1]) for row in rows]
    
    def get_tms_by_domain(self, domain: str) -> List[IndexedTM]:
        """Get all indexed TMs for a specific domain"""
        conn = sqlite3.connect(str(self.metadata_db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM indexed_tms WHERE domain = ? ORDER BY name", (domain,))
        rows = cursor.fetchall()
        conn.close()
        
        return [
            IndexedTM(
                tm_id=row[0], name=row[1], file_path=row[2],
                source_lang=row[3], target_lang=row[4], entry_count=row[5],
                indexed_date=row[6], file_hash=row[7], status=row[8],
                domain=row[9] if len(row) > 9 else ""
            )
            for row in rows
        ]
    
    def update_tm_domain(self, tm_id: str, domain: str) -> bool:
        """Update the domain for an indexed TM"""
        try:
            conn = sqlite3.connect(str(self.metadata_db_path))
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE indexed_tms SET domain=? WHERE tm_id=?",
                (domain, tm_id)
            )
            
            conn.commit()
            conn.close()
            
            # Also update ChromaDB metadata for all entries of this TM
            # Note: ChromaDB doesn't support bulk metadata updates easily,
            # so we skip this for now - domain filtering will use tm_id lookup
            
            return True
        except Exception as e:
            self.log(f"[Supermemory] Error updating TM domain: {e}")
            return False
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_stats(self) -> Dict:
        """Get statistics about indexed content"""
        tms = self.get_all_indexed_tms()
        
        total_entries = sum(tm.entry_count for tm in tms)
        
        # Get language pairs
        lang_pairs = {}
        for tm in tms:
            pair = f"{tm.source_lang}-{tm.target_lang}"
            lang_pairs[pair] = lang_pairs.get(pair, 0) + tm.entry_count
        
        # Note: We use total_entries from metadata instead of collection.count()
        # because ChromaDB 1.3.x Rust backend can crash on count() calls
        
        return {
            "total_tms": len(tms),
            "total_entries": total_entries,
            "language_pairs": lang_pairs,
            "collection_count": total_entries,  # Use metadata count, not collection.count()
            "model": self.embedding_model_name or "Not loaded"
        }
    
    def get_storage_info(self) -> Dict:
        """Get detailed storage information"""
        def get_folder_size(path: Path) -> int:
            """Calculate total size of a folder in bytes"""
            total = 0
            if path.exists():
                for item in path.rglob('*'):
                    if item.is_file():
                        try:
                            total += item.stat().st_size
                        except:
                            pass
            return total
        
        def format_size(bytes_size: int) -> str:
            """Format bytes to human readable"""
            for unit in ['B', 'KB', 'MB', 'GB']:
                if bytes_size < 1024:
                    return f"{bytes_size:.1f} {unit}"
                bytes_size /= 1024
            return f"{bytes_size:.1f} TB"
        
        # Calculate sizes
        metadata_size = self.metadata_db_path.stat().st_size if self.metadata_db_path.exists() else 0
        chroma_size = get_folder_size(self.chroma_path)
        total_size = metadata_size + chroma_size
        
        # Get file counts
        chroma_files = len(list(self.chroma_path.rglob('*'))) if self.chroma_path.exists() else 0
        
        return {
            "storage_path": str(self.supermemory_dir),
            "metadata_db_path": str(self.metadata_db_path),
            "chroma_db_path": str(self.chroma_path),
            "metadata_size": metadata_size,
            "metadata_size_formatted": format_size(metadata_size),
            "chroma_size": chroma_size,
            "chroma_size_formatted": format_size(chroma_size),
            "total_size": total_size,
            "total_size_formatted": format_size(total_size),
            "chroma_files": chroma_files
        }
    
    # =========================================================================
    # EXPORT
    # =========================================================================
    
    def export_to_tmx(self, output_path: Path, tm_ids: List[str] = None, 
                      domains: List[str] = None, source_lang: str = None,
                      target_lang: str = None, progress_callback: Callable = None) -> int:
        """
        Export indexed entries to TMX format.
        
        Args:
            output_path: Path for output TMX file
            tm_ids: Filter by specific TM IDs (optional)
            domains: Filter by domains (optional)
            source_lang: Filter by source language (optional)
            target_lang: Filter by target language (optional)
            progress_callback: Optional callback(current, total, message)
            
        Returns:
            Number of entries exported
        """
        if not self.is_initialized():
            return 0
        
        # Build query to get all matching entries
        # We need to search with a very generic query and high n_results
        # ChromaDB doesn't have a "get all" so we use a workaround
        
        # Get matching TMs based on filters
        tms = self.get_all_indexed_tms()
        if tm_ids:
            tms = [tm for tm in tms if tm.tm_id in tm_ids]
        if domains:
            tms = [tm for tm in tms if tm.domain in domains]
        if source_lang:
            tms = [tm for tm in tms if tm.source_lang.lower().startswith(source_lang.lower()[:2])]
        if target_lang:
            tms = [tm for tm in tms if tm.target_lang.lower().startswith(target_lang.lower()[:2])]
        
        if not tms:
            return 0
        
        # Determine language pair from first TM
        src = tms[0].source_lang if tms else 'en'
        tgt = tms[0].target_lang if tms else 'xx'
        
        # Build TMX
        root = ET.Element('tmx', version='1.4')
        header = ET.SubElement(root, 'header', {
            'creationtool': 'Supervertaler Supermemory',
            'creationtoolversion': '1.0',
            'segtype': 'sentence',
            'adminlang': 'en',
            'srclang': src,
            'datatype': 'plaintext'
        })
        body = ET.SubElement(root, 'body')
        
        total_entries = 0
        tm_ids_to_export = [tm.tm_id for tm in tms]
        
        # Get entries from ChromaDB for each TM
        for tm in tms:
            try:
                # Query all entries for this TM
                results = self.collection.get(
                    where={"tm_id": tm.tm_id},
                    include=["metadatas"]
                )
                
                if results and results['ids']:
                    for i, entry_id in enumerate(results['ids']):
                        metadata = results['metadatas'][i]
                        
                        if progress_callback and i % 100 == 0:
                            progress_callback(total_entries, -1, f"Exporting {tm.name}...")
                        
                        # Create TU element
                        tu = ET.SubElement(body, 'tu')
                        
                        # Source TUV
                        src_tuv = ET.SubElement(tu, 'tuv', {
                            '{http://www.w3.org/XML/1998/namespace}lang': metadata.get('source_lang', src)
                        })
                        src_seg = ET.SubElement(src_tuv, 'seg')
                        src_seg.text = metadata.get('source', '')
                        
                        # Target TUV
                        tgt_tuv = ET.SubElement(tu, 'tuv', {
                            '{http://www.w3.org/XML/1998/namespace}lang': metadata.get('target_lang', tgt)
                        })
                        tgt_seg = ET.SubElement(tgt_tuv, 'seg')
                        tgt_seg.text = metadata.get('target', '')
                        
                        total_entries += 1
                        
            except Exception as e:
                self.log(f"[Supermemory] Error exporting TM {tm.name}: {e}")
        
        # Write TMX file
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(str(output_path), encoding='utf-8', xml_declaration=True)
        
        if progress_callback:
            progress_callback(total_entries, total_entries, f"Exported {total_entries} entries")
        
        return total_entries
    
    def export_to_csv(self, output_path: Path, tm_ids: List[str] = None,
                      domains: List[str] = None, source_lang: str = None,
                      target_lang: str = None, progress_callback: Callable = None) -> int:
        """
        Export indexed entries to CSV format.
        
        Args:
            output_path: Path for output CSV file
            tm_ids: Filter by specific TM IDs (optional)
            domains: Filter by domains (optional)
            source_lang: Filter by source language (optional)
            target_lang: Filter by target language (optional)
            progress_callback: Optional callback(current, total, message)
            
        Returns:
            Number of entries exported
        """
        import csv
        
        if not self.is_initialized():
            return 0
        
        # Get matching TMs based on filters
        tms = self.get_all_indexed_tms()
        if tm_ids:
            tms = [tm for tm in tms if tm.tm_id in tm_ids]
        if domains:
            tms = [tm for tm in tms if tm.domain in domains]
        if source_lang:
            tms = [tm for tm in tms if tm.source_lang.lower().startswith(source_lang.lower()[:2])]
        if target_lang:
            tms = [tm for tm in tms if tm.target_lang.lower().startswith(target_lang.lower()[:2])]
        
        if not tms:
            return 0
        
        total_entries = 0
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Source', 'Target', 'Source Lang', 'Target Lang', 'TM Name', 'Domain'])
            
            for tm in tms:
                try:
                    results = self.collection.get(
                        where={"tm_id": tm.tm_id},
                        include=["metadatas"]
                    )
                    
                    if results and results['ids']:
                        for i, entry_id in enumerate(results['ids']):
                            metadata = results['metadatas'][i]
                            
                            if progress_callback and i % 100 == 0:
                                progress_callback(total_entries, -1, f"Exporting {tm.name}...")
                            
                            writer.writerow([
                                metadata.get('source', ''),
                                metadata.get('target', ''),
                                metadata.get('source_lang', ''),
                                metadata.get('target_lang', ''),
                                metadata.get('tm_name', tm.name),
                                metadata.get('domain', tm.domain)
                            ])
                            
                            total_entries += 1
                            
                except Exception as e:
                    self.log(f"[Supermemory] Error exporting TM {tm.name}: {e}")
        
        if progress_callback:
            progress_callback(total_entries, total_entries, f"Exported {total_entries} entries")
        
        return total_entries


# =============================================================================
# UI WIDGET
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QLineEdit, QTextEdit,
    QProgressBar, QFileDialog, QMessageBox, QGroupBox,
    QSplitter, QHeaderView, QComboBox, QSpinBox, QFrame,
    QDialog, QCheckBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor


class IndexingThread(QThread):
    """Background thread for TMX indexing"""
    progress = pyqtSignal(int, int, str)  # current, total, message
    finished = pyqtSignal(object)  # IndexedTM or None
    error = pyqtSignal(str)
    
    def __init__(self, engine: SupermemoryEngine, tmx_path: Path, domain: str = ""):
        super().__init__()
        self.engine = engine
        self.tmx_path = tmx_path
        self.domain = domain
    
    def run(self):
        try:
            result = self.engine.index_tmx(
                self.tmx_path,
                progress_callback=lambda c, t, m: self.progress.emit(c, t, m),
                domain=self.domain
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class DomainManagerDialog(QDialog):
    """Dialog for managing translation domains"""
    
    def __init__(self, engine: SupermemoryEngine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("Domain Manager")
        self.setMinimumSize(500, 400)
        self._setup_ui()
        self._load_domains()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Info label
        info = QLabel("Manage translation domains for organizing your TMs. "
                     "Active domains are used when filtering search results.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(info)
        
        # Domain table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Active", "Name", "Description", "Color"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemChanged.connect(self._on_item_changed)
        layout.addWidget(self.table)
        
        # Buttons row
        btn_row = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add Domain")
        add_btn.clicked.connect(self._add_domain)
        btn_row.addWidget(add_btn)
        
        delete_btn = QPushButton("🗑️ Delete Selected")
        delete_btn.clicked.connect(self._delete_domain)
        btn_row.addWidget(delete_btn)
        
        btn_row.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        
        layout.addLayout(btn_row)
    
    def _load_domains(self):
        self.table.blockSignals(True)
        domains = self.engine.get_all_domains()
        self.table.setRowCount(len(domains))
        
        for i, domain in enumerate(domains):
            # Active checkbox
            active_item = QTableWidgetItem()
            active_item.setCheckState(Qt.CheckState.Checked if domain.active else Qt.CheckState.Unchecked)
            active_item.setData(Qt.ItemDataRole.UserRole, domain.name)  # Store original name
            self.table.setItem(i, 0, active_item)
            
            # Name
            name_item = QTableWidgetItem(domain.name)
            self.table.setItem(i, 1, name_item)
            
            # Description
            desc_item = QTableWidgetItem(domain.description)
            self.table.setItem(i, 2, desc_item)
            
            # Color
            color_item = QTableWidgetItem(domain.color)
            color_item.setBackground(QColor(domain.color))
            self.table.setItem(i, 3, color_item)
        
        self.table.blockSignals(False)
    
    def _on_item_changed(self, item):
        """Handle cell edits"""
        row = item.row()
        col = item.column()
        
        original_name = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        if col == 0:  # Active checkbox
            active = item.checkState() == Qt.CheckState.Checked
            self.engine.set_domain_active(original_name, active)
        else:
            # Get current values
            name = self.table.item(row, 1).text()
            desc = self.table.item(row, 2).text()
            color = self.table.item(row, 3).text()
            active = self.table.item(row, 0).checkState() == Qt.CheckState.Checked
            
            domain = Domain(name=name, description=desc, color=color, active=active)
            
            if self.engine.update_domain(original_name, domain):
                # Update stored name if it changed
                if col == 1:
                    self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, name)
                # Update color background
                if col == 3:
                    self.table.item(row, 3).setBackground(QColor(color))
    
    def _add_domain(self):
        """Add a new domain"""
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, "Add Domain", "Domain name:")
        if ok and name.strip():
            domain = Domain(name=name.strip())
            if self.engine.add_domain(domain):
                self._load_domains()
            else:
                QMessageBox.warning(self, "Error", "Could not add domain. It may already exist.")
    
    def _delete_domain(self):
        """Delete selected domain"""
        selected = self.table.selectedItems()
        if not selected:
            return
        
        row = selected[0].row()
        name = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "Delete Domain",
            f"Delete domain '{name}'?\n\nThis will not delete any indexed TMs.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.engine.delete_domain(name):
                self._load_domains()


class SupermemoryWidget(QWidget):
    """
    Main Supermemory UI widget for the Tools tab.
    Provides TMX indexing and semantic search interface.
    """
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.engine = None
        self.indexing_thread = None
        
        self._setup_ui()
        self._initialize_engine()
    
    def _setup_ui(self):
        """Build the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        # Header
        header = self._create_header()
        layout.addWidget(header)
        
        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Top: Indexed TMs list
        tms_group = self._create_tms_panel()
        splitter.addWidget(tms_group)
        
        # Bottom: Search panel
        search_group = self._create_search_panel()
        splitter.addWidget(search_group)
        
        splitter.setSizes([300, 400])
        layout.addWidget(splitter, stretch=1)
        
        # Status bar
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.status_label)
    
    def _create_header(self) -> QWidget:
        """Create header with title and controls"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("🧠 Supermemory")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Vector-Indexed Translation Memory")
        subtitle.setStyleSheet("color: #666; margin-left: 10px;")
        layout.addWidget(subtitle)
        
        layout.addStretch()
        
        # Export button
        self.export_btn = QPushButton("📤 Export...")
        self.export_btn.clicked.connect(self._show_export_dialog)
        self.export_btn.setToolTip("Export indexed entries to TMX or CSV")
        layout.addWidget(self.export_btn)
        
        # Storage info button
        self.storage_btn = QPushButton("📁 Storage Info")
        self.storage_btn.clicked.connect(self._show_storage_info)
        self.storage_btn.setToolTip("Show where Supermemory data is stored")
        layout.addWidget(self.storage_btn)
        
        # Stats label
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("color: #666;")
        layout.addWidget(self.stats_label)
        
        return header
    
    def _create_tms_panel(self) -> QGroupBox:
        """Create panel for managing indexed TMs"""
        group = QGroupBox("Indexed Translation Memories")
        layout = QVBoxLayout(group)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.add_tmx_btn = QPushButton("📂 Add TMX...")
        self.add_tmx_btn.clicked.connect(self._add_tmx)
        toolbar.addWidget(self.add_tmx_btn)
        
        self.remove_btn = QPushButton("🗑️ Remove Selected")
        self.remove_btn.clicked.connect(self._remove_selected)
        self.remove_btn.setEnabled(False)
        toolbar.addWidget(self.remove_btn)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self._refresh_tm_list)
        toolbar.addWidget(self.refresh_btn)
        
        # Domain manager button
        self.domain_btn = QPushButton("🏷️ Domains...")
        self.domain_btn.clicked.connect(self._show_domain_manager)
        self.domain_btn.setToolTip("Manage translation domains")
        toolbar.addWidget(self.domain_btn)
        
        toolbar.addStretch()
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumWidth(200)
        toolbar.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        toolbar.addWidget(self.progress_label)
        
        layout.addLayout(toolbar)
        
        # TM table with domain column and active checkbox
        self.tm_table = QTableWidget()
        self.tm_table.setColumnCount(7)
        self.tm_table.setHorizontalHeaderLabels(["Active", "Name", "Domain", "Languages", "Entries", "Indexed", "Status"])
        self.tm_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Name column stretches
        self.tm_table.setColumnWidth(0, 50)  # Active column is narrow
        self.tm_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tm_table.setAlternatingRowColors(True)
        self.tm_table.itemSelectionChanged.connect(self._on_selection_changed)
        self.tm_table.cellChanged.connect(self._on_cell_changed)
        layout.addWidget(self.tm_table)
        
        return group
    
    def _create_search_panel(self) -> QGroupBox:
        """Create semantic search panel with filters"""
        group = QGroupBox("Semantic Search")
        layout = QVBoxLayout(group)
        
        # Filter row
        filter_row = QHBoxLayout()
        
        filter_row.addWidget(QLabel("Language:"))
        self.lang_filter = QComboBox()
        self.lang_filter.addItem("All Languages", None)
        self.lang_filter.setMinimumWidth(120)
        filter_row.addWidget(self.lang_filter)
        
        filter_row.addWidget(QLabel("Domains:"))
        self.domain_filter_btn = QPushButton("All Domains ▼")
        self.domain_filter_btn.clicked.connect(self._show_domain_filter)
        self.domain_filter_btn.setMinimumWidth(120)
        filter_row.addWidget(self.domain_filter_btn)
        
        self.use_active_domains_cb = CheckmarkCheckBox("Use active domains only")
        self.use_active_domains_cb.setChecked(True)
        self.use_active_domains_cb.setToolTip("Filter results by domains marked as active in Domain Manager")
        filter_row.addWidget(self.use_active_domains_cb)
        
        filter_row.addStretch()
        layout.addLayout(filter_row)
        
        # Search input row
        search_row = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter text to search for semantically similar translations...")
        self.search_input.returnPressed.connect(self._do_search)
        search_row.addWidget(self.search_input, stretch=1)
        
        self.results_spin = QSpinBox()
        self.results_spin.setRange(1, 50)
        self.results_spin.setValue(10)
        self.results_spin.setPrefix("Results: ")
        search_row.addWidget(self.results_spin)
        
        self.search_btn = QPushButton("🔍 Search")
        self.search_btn.clicked.connect(self._do_search)
        search_row.addWidget(self.search_btn)
        
        layout.addLayout(search_row)
        
        # Results table with domain column
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Similarity", "Source", "Target", "Domain", "TM"])
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.results_table)
        
        return group
    
    def _initialize_engine(self):
        """Initialize the Supermemory engine"""
        try:
            data_dir = self.main_window.user_data_path if hasattr(self.main_window, 'user_data_path') else Path.home() / ".supervertaler"
            self.engine = SupermemoryEngine(data_dir, self.main_window.log if hasattr(self.main_window, 'log') else print)
            
            # Check dependencies
            deps = self.engine.check_dependencies()

            if not deps["ready"]:
                missing = self.engine.get_missing_dependencies()
                error_msg = f"⚠️ Missing: {', '.join(missing)}. Install with: pip install {' '.join(missing)}"

                # If sentence-transformers import failed with an error, show the actual error
                if 'sentence-transformers' in missing and SENTENCE_TRANSFORMERS_ERROR:
                    error_msg = f"⚠️ Error loading sentence-transformers: {SENTENCE_TRANSFORMERS_ERROR}"
                    # Log detailed error to console
                    if hasattr(self.main_window, 'log'):
                        self.main_window.log(f"Supermemory initialization failed:")
                        self.main_window.log(f"  {SENTENCE_TRANSFORMERS_ERROR}")

                self.status_label.setText(error_msg)
                self.add_tmx_btn.setEnabled(False)
                self.search_btn.setEnabled(False)
                return
            
            # Initialize in background
            if self.engine.initialize():
                self._refresh_tm_list()
                self._update_stats()
                self.status_label.setText("✅ Ready")
            else:
                self.status_label.setText("❌ Initialization failed")
                
        except Exception as e:
            self.status_label.setText(f"❌ Error: {e}")
    
    def _update_stats(self):
        """Update statistics display"""
        if self.engine and self.engine.is_initialized():
            stats = self.engine.get_stats()
            self.stats_label.setText(
                f"📊 {stats['total_tms']} TMs | {stats['total_entries']:,} entries | Model: {stats['model']}"
            )
    
    def _refresh_tm_list(self):
        """Refresh the list of indexed TMs"""
        if not self.engine:
            return
        
        tms = self.engine.get_all_indexed_tms()
        
        # Block signals while updating to avoid triggering cellChanged
        self.tm_table.blockSignals(True)
        self.tm_table.setRowCount(len(tms))
        
        for i, tm in enumerate(tms):
            # Active checkbox column (column 0)
            active_item = QTableWidgetItem()
            active_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            active_item.setCheckState(Qt.CheckState.Checked if tm.active else Qt.CheckState.Unchecked)
            active_item.setData(Qt.ItemDataRole.UserRole, tm.tm_id)  # Store tm_id here
            self.tm_table.setItem(i, 0, active_item)
            
            # Name column (column 1)
            name_item = QTableWidgetItem(tm.name)
            self.tm_table.setItem(i, 1, name_item)
            
            # Domain column (column 2)
            domain_item = QTableWidgetItem(tm.domain or "—")
            if tm.domain:
                # Try to get domain color
                domains = self.engine.get_all_domains()
                domain_obj = next((d for d in domains if d.name == tm.domain), None)
                if domain_obj:
                    domain_item.setBackground(QColor(domain_obj.color).lighter(170))
            self.tm_table.setItem(i, 2, domain_item)
            
            # Languages (column 3)
            self.tm_table.setItem(i, 3, QTableWidgetItem(f"{tm.source_lang} → {tm.target_lang}"))
            
            # Entry count (column 4)
            self.tm_table.setItem(i, 4, QTableWidgetItem(f"{tm.entry_count:,}"))
            
            # Format date nicely (column 5)
            try:
                dt = datetime.fromisoformat(tm.indexed_date)
                date_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = tm.indexed_date[:16] if tm.indexed_date else ""
            self.tm_table.setItem(i, 5, QTableWidgetItem(date_str))
            
            # Status (column 6)
            status_item = QTableWidgetItem(tm.status)
            if tm.status == "ready":
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            self.tm_table.setItem(i, 6, status_item)
        
        # Re-enable signals
        self.tm_table.blockSignals(False)
        
        self._update_stats()
        self._update_filters()
    
    def _on_cell_changed(self, row: int, column: int):
        """Handle cell changes (for checkbox clicks)"""
        if column == 0:  # Active checkbox column
            item = self.tm_table.item(row, column)
            if item:
                tm_id = item.data(Qt.ItemDataRole.UserRole)
                is_active = item.checkState() == Qt.CheckState.Checked
                if tm_id and self.engine:
                    self.engine.set_tm_active(tm_id, is_active)
        
        self._update_stats()
        self._update_filters()
    
    def _on_selection_changed(self):
        """Handle TM table selection change"""
        self.remove_btn.setEnabled(len(self.tm_table.selectedItems()) > 0)
    
    def _add_tmx(self):
        """Add and index a TMX file with domain selection"""
        if not self.engine or not self.engine.is_initialized():
            QMessageBox.warning(self, "Not Ready", "Supermemory engine is not initialized.")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select TMX File", "", "TMX Files (*.tmx);;All Files (*)"
        )
        
        if not file_path:
            return
        
        # Show domain selection dialog
        domain = self._select_domain_for_import(Path(file_path).stem)
        if domain is None:  # User cancelled
            return
        
        # Start indexing in background
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setVisible(True)
        self.add_tmx_btn.setEnabled(False)
        
        self.indexing_thread = IndexingThread(self.engine, Path(file_path), domain=domain)
        self.indexing_thread.progress.connect(self._on_indexing_progress)
        self.indexing_thread.finished.connect(self._on_indexing_finished)
        self.indexing_thread.error.connect(self._on_indexing_error)
        self.indexing_thread.start()
    
    def _select_domain_for_import(self, file_name: str) -> str:
        """Show dialog to select domain for TMX import"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Domain")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        info = QLabel(f"Select domain for:\n<b>{file_name}</b>")
        info.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(info)
        
        # Domain combo
        combo = QComboBox()
        domains = self.engine.get_all_domains()
        for d in domains:
            combo.addItem(d.name, d.name)
        combo.setCurrentText("General")
        layout.addWidget(combo)
        
        # Buttons
        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        btn_row.addWidget(cancel_btn)
        
        ok_btn = QPushButton("Import")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(dialog.accept)
        btn_row.addWidget(ok_btn)
        
        layout.addLayout(btn_row)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return combo.currentData()
        return None
    
    def _on_indexing_progress(self, current: int, total: int, message: str):
        """Handle indexing progress updates"""
        if total > 0:
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
        self.progress_label.setText(message)
    
    def _on_indexing_finished(self, result):
        """Handle indexing completion"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.add_tmx_btn.setEnabled(True)
        
        if result:
            self._refresh_tm_list()
            self.status_label.setText(f"✅ Indexed: {result.name} ({result.entry_count:,} entries)")
        else:
            self.status_label.setText("⚠️ Indexing completed with no entries")
    
    def _on_indexing_error(self, error: str):
        """Handle indexing error"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.add_tmx_btn.setEnabled(True)
        self.status_label.setText(f"❌ Error: {error}")
        QMessageBox.critical(self, "Indexing Error", f"Failed to index TMX:\n{error}")
    
    def _remove_selected(self):
        """Remove selected TM from index"""
        selected = self.tm_table.selectedItems()
        if not selected:
            return
        
        row = selected[0].row()
        tm_name = self.tm_table.item(row, 1).text()  # Name is now column 1
        tm_id = self.tm_table.item(row, 0).data(Qt.ItemDataRole.UserRole)  # tm_id stored in checkbox column
        
        reply = QMessageBox.question(
            self, "Remove TM",
            f"Remove '{tm_name}' from Supermemory index?\n\nThis will not delete the original TMX file.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.engine.remove_indexed_tm(tm_id):
                self._refresh_tm_list()
                self.status_label.setText(f"✅ Removed: {tm_name}")
            else:
                self.status_label.setText(f"❌ Failed to remove: {tm_name}")
    
    def _show_domain_manager(self):
        """Open the domain manager dialog"""
        if not self.engine:
            return
        dialog = DomainManagerDialog(self.engine, self)
        dialog.exec()
        self._refresh_tm_list()  # Refresh in case domains changed
    
    def _show_domain_filter(self):
        """Show multi-select dialog for domain filtering"""
        if not self.engine:
            return
        
        domains = self.engine.get_all_domains()
        if not domains:
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Filter by Domains")
        dialog.setMinimumWidth(250)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("Select domains to include in search:"))
        
        list_widget = QListWidget()
        for d in domains:
            item = QListWidgetItem(d.name)
            item.setCheckState(Qt.CheckState.Checked if d.active else Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, d.name)
            list_widget.addItem(item)
        layout.addWidget(list_widget)
        
        # Buttons
        btn_row = QHBoxLayout()
        
        select_all = QPushButton("Select All")
        select_all.clicked.connect(lambda: self._set_all_items(list_widget, True))
        btn_row.addWidget(select_all)
        
        select_none = QPushButton("Select None")
        select_none.clicked.connect(lambda: self._set_all_items(list_widget, False))
        btn_row.addWidget(select_none)
        
        btn_row.addStretch()
        
        ok_btn = QPushButton("Apply")
        ok_btn.clicked.connect(dialog.accept)
        btn_row.addWidget(ok_btn)
        
        layout.addLayout(btn_row)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update active status for all domains
            for i in range(list_widget.count()):
                item = list_widget.item(i)
                name = item.data(Qt.ItemDataRole.UserRole)
                active = item.checkState() == Qt.CheckState.Checked
                self.engine.set_domain_active(name, active)
            
            self._update_domain_filter_button()
    
    def _set_all_items(self, list_widget: QListWidget, checked: bool):
        """Helper to select/deselect all items in a list widget"""
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        for i in range(list_widget.count()):
            list_widget.item(i).setCheckState(state)
    
    def _update_filters(self):
        """Update filter dropdowns based on indexed TMs"""
        if not self.engine:
            return
        
        # Update language filter
        current_lang = self.lang_filter.currentData()
        self.lang_filter.clear()
        self.lang_filter.addItem("All Languages", None)
        
        lang_pairs = self.engine.get_unique_language_pairs()
        seen = set()
        for src, tgt in lang_pairs:
            pair = f"{src} → {tgt}"
            if pair not in seen:
                self.lang_filter.addItem(pair, (src, tgt))
                seen.add(pair)
        
        # Restore selection if possible
        if current_lang:
            idx = self.lang_filter.findData(current_lang)
            if idx >= 0:
                self.lang_filter.setCurrentIndex(idx)
        
        self._update_domain_filter_button()
    
    def _update_domain_filter_button(self):
        """Update domain filter button text"""
        if not self.engine:
            return
        
        active = self.engine.get_active_domains()
        total = len(self.engine.get_all_domains())
        
        if len(active) == total:
            self.domain_filter_btn.setText("All Domains ▼")
        elif len(active) == 0:
            self.domain_filter_btn.setText("No Domains ▼")
        else:
            self.domain_filter_btn.setText(f"{len(active)}/{total} Domains ▼")
    
    def _do_search(self):
        """Perform semantic search with filters"""
        if not self.engine or not self.engine.is_initialized():
            return
        
        query = self.search_input.text().strip()
        if not query:
            return
        
        n_results = self.results_spin.value()
        
        # Get language filter
        lang_data = self.lang_filter.currentData()
        source_lang = lang_data[0] if lang_data else None
        target_lang = lang_data[1] if lang_data else None
        
        # Get domain filter
        use_active_domains = self.use_active_domains_cb.isChecked()
        
        self.status_label.setText("Searching...")
        self.search_btn.setEnabled(False)
        
        try:
            if use_active_domains:
                results = self.engine.search_by_active_domains(
                    query, n_results=n_results,
                    source_lang=source_lang, target_lang=target_lang
                )
            else:
                results = self.engine.search(
                    query, n_results=n_results,
                    source_lang=source_lang, target_lang=target_lang
                )
            
            # Update column headers with actual language names if available
            if results and len(results) > 0:
                src = results[0].entry.source_lang.upper()
                tgt = results[0].entry.target_lang.upper()
                self.results_table.setHorizontalHeaderLabels([
                    "Similarity", f"Source ({src})", f"Target ({tgt})", "Domain", "TM"
                ])
            else:
                # Reset to default if no results
                self.results_table.setHorizontalHeaderLabels([
                    "Similarity", "Source", "Target", "Domain", "TM"
                ])
            
            self.results_table.setRowCount(len(results))
            
            for i, r in enumerate(results):
                sim_pct = f"{int(r.similarity * 100)}%"
                self.results_table.setItem(i, 0, QTableWidgetItem(sim_pct))
                self.results_table.setItem(i, 1, QTableWidgetItem(r.entry.source))
                self.results_table.setItem(i, 2, QTableWidgetItem(r.entry.target))
                self.results_table.setItem(i, 3, QTableWidgetItem(r.domain or "—"))
                self.results_table.setItem(i, 4, QTableWidgetItem(r.entry.tm_name))
            
            self.status_label.setText(f"✅ Found {len(results)} results")
            
        except Exception as e:
            self.status_label.setText(f"❌ Search error: {e}")
        
        finally:
            self.search_btn.setEnabled(True)
    
    def _show_export_dialog(self):
        """Show export dialog for TMX/CSV export"""
        if not self.engine or not self.engine.is_initialized():
            QMessageBox.warning(self, "Not Ready", "Supermemory engine is not initialized.")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Export Supermemory")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Info
        info = QLabel("Export indexed translation memory entries to TMX or CSV format.")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Format selection
        format_row = QHBoxLayout()
        format_row.addWidget(QLabel("Format:"))
        format_combo = QComboBox()
        format_combo.addItems(["TMX (Translation Memory Exchange)", "CSV (Comma Separated Values)"])
        format_row.addWidget(format_combo, stretch=1)
        layout.addLayout(format_row)
        
        # Domain filter
        domain_row = QHBoxLayout()
        domain_row.addWidget(QLabel("Domains:"))
        domain_combo = QComboBox()
        domain_combo.addItem("All Domains", None)
        for d in self.engine.get_all_domains():
            domain_combo.addItem(d.name, d.name)
        domain_row.addWidget(domain_combo, stretch=1)
        layout.addLayout(domain_row)
        
        # TM filter
        tm_row = QHBoxLayout()
        tm_row.addWidget(QLabel("TM:"))
        tm_combo = QComboBox()
        tm_combo.addItem("All TMs", None)
        for tm in self.engine.get_all_indexed_tms():
            tm_combo.addItem(f"{tm.name} ({tm.entry_count:,} entries)", tm.tm_id)
        tm_row.addWidget(tm_combo, stretch=1)
        layout.addLayout(tm_row)
        
        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        btn_row.addWidget(cancel_btn)
        
        export_btn = QPushButton("📤 Export...")
        export_btn.setDefault(True)
        btn_row.addWidget(export_btn)
        
        layout.addLayout(btn_row)
        
        def do_export():
            # Get filter values
            domain = domain_combo.currentData()
            domains = [domain] if domain else None
            
            tm_id = tm_combo.currentData()
            tm_ids = [tm_id] if tm_id else None
            
            # Determine format
            is_tmx = "TMX" in format_combo.currentText()
            ext = "tmx" if is_tmx else "csv"
            filter_str = f"{'TMX' if is_tmx else 'CSV'} Files (*.{ext})"
            
            # Get save path
            file_path, _ = QFileDialog.getSaveFileName(
                dialog, "Export Supermemory", f"supermemory_export.{ext}", filter_str
            )
            
            if not file_path:
                return
            
            dialog.accept()
            
            # Show progress
            self.status_label.setText("Exporting...")
            QApplication.processEvents()
            
            try:
                if is_tmx:
                    count = self.engine.export_to_tmx(
                        Path(file_path), tm_ids=tm_ids, domains=domains
                    )
                else:
                    count = self.engine.export_to_csv(
                        Path(file_path), tm_ids=tm_ids, domains=domains
                    )
                
                self.status_label.setText(f"✅ Exported {count:,} entries to {Path(file_path).name}")
                
                QMessageBox.information(
                    self, "Export Complete",
                    f"Successfully exported {count:,} entries to:\n{file_path}"
                )
                
            except Exception as e:
                self.status_label.setText(f"❌ Export error: {e}")
                QMessageBox.critical(self, "Export Error", f"Failed to export:\n{e}")
        
        export_btn.clicked.connect(do_export)
        dialog.exec()
    
    def _show_storage_info(self):
        """Show storage location and size information"""
        if not self.engine:
            QMessageBox.information(self, "Storage Info", "Supermemory engine not initialized.")
            return
        
        try:
            info = self.engine.get_storage_info()
            stats = self.engine.get_stats()
            
            message = f"""<h3>🧠 Supermemory Storage</h3>
            
<p><b>Storage Location:</b><br/>
<code style="background: #f0f0f0; padding: 2px 6px;">{info['storage_path']}</code></p>

<p><b>Database Files:</b></p>
<ul>
<li><b>Metadata DB:</b> {info['metadata_size_formatted']}<br/>
<code style="font-size: 10px;">{info['metadata_db_path']}</code></li>
<li><b>Vector DB (ChromaDB):</b> {info['chroma_size_formatted']} ({info['chroma_files']} files)<br/>
<code style="font-size: 10px;">{info['chroma_db_path']}</code></li>
</ul>

<p><b>Total Storage Used:</b> {info['total_size_formatted']}</p>

<hr/>

<p><b>Content Summary:</b></p>
<ul>
<li>Indexed TMs: {stats['total_tms']}</li>
<li>Total Entries: {stats['total_entries']:,}</li>
<li>Embedding Model: {stats['model']}</li>
</ul>

<p><i>All data is stored locally on your computer.<br/>
No cloud services are used.</i></p>
"""
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Supermemory Storage Info")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(message)
            msg.setIcon(QMessageBox.Icon.Information)
            
            # Add "Open Folder" button
            open_btn = msg.addButton("📂 Open Folder", QMessageBox.ButtonRole.ActionRole)
            msg.addButton(QMessageBox.StandardButton.Ok)
            
            msg.exec()
            
            if msg.clickedButton() == open_btn:
                # Open the storage folder in file explorer
                import subprocess
                import sys

                if sys.platform == 'win32':
                    subprocess.Popen(['explorer', info['storage_path']])
                elif sys.platform == 'darwin':
                    subprocess.Popen(['open', info['storage_path']])
                else:
                    subprocess.Popen(['xdg-open', info['storage_path']])
                    
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not get storage info:\n{e}")


# =============================================================================
# INSTALLATION HELPER
# =============================================================================

def get_install_instructions() -> str:
    """Get instructions for installing Supermemory dependencies"""
    return """
Supermemory requires additional Python packages for vector search:

    pip install chromadb sentence-transformers

This will install:
• ChromaDB - Local vector database (no cloud, fully private)
• Sentence-Transformers - Multilingual text embeddings

First run will download the embedding model (~420MB).
After that, everything runs locally and offline.

Recommended: Use a Python virtual environment.
"""


class CheckmarkCheckBox(QCheckBox):
    """Custom checkbox with green background and white checkmark when checked"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setEnabled(True)
        self.setStyleSheet("""
            QCheckBox {
                font-size: 9pt;
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #999;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
            }
            QCheckBox::indicator:hover {
                border-color: #666;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #45a049;
                border-color: #45a049;
            }
        """)

    def paintEvent(self, event):
        """Override paint event to draw white checkmark when checked"""
        super().paintEvent(event)

        if self.isChecked():
            from PyQt6.QtWidgets import QStyleOptionButton
            from PyQt6.QtGui import QPainter, QPen, QColor
            from PyQt6.QtCore import QPointF, Qt

            opt = QStyleOptionButton()
            self.initStyleOption(opt)
            indicator_rect = self.style().subElementRect(
                self.style().SubElement.SE_CheckBoxIndicator,
                opt,
                self
            )

            if indicator_rect.isValid():
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                pen_width = max(2.0, min(indicator_rect.width(), indicator_rect.height()) * 0.12)
                painter.setPen(QPen(QColor(255, 255, 255), pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
                painter.setBrush(QColor(255, 255, 255))

                x = indicator_rect.x()
                y = indicator_rect.y()
                w = indicator_rect.width()
                h = indicator_rect.height()

                padding = min(w, h) * 0.15
                x += padding
                y += padding
                w -= padding * 2
                h -= padding * 2

                check_x1 = x + w * 0.10
                check_y1 = y + h * 0.50
                check_x2 = x + w * 0.35
                check_y2 = y + h * 0.70
                check_x3 = x + w * 0.90
                check_y3 = y + h * 0.25

                painter.drawLine(QPointF(check_x2, check_y2), QPointF(check_x3, check_y3))
                painter.drawLine(QPointF(check_x1, check_y1), QPointF(check_x2, check_y2))

                painter.end()
