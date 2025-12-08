# supermemory

**File:** `modules/supermemory.py`
**Lines:** 2,301
**Classes:** 9
**Functions:** 1

---

## Module Description

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

---

## Classes

### `MemoryEntry`

**Line:** 60

Single translation memory entry

---

### `IndexedTM`

**Line:** 75

Metadata about an indexed translation memory

---

### `SearchResult`

**Line:** 91

Search result with semantic similarity

---

### `Domain`

**Line:** 100

Translation domain category

---

### `SupermemoryEngine`

**Line:** 144

Core engine for vector-indexed translation memory.
Handles indexing, searching, and LLM context generation.

#### Methods

##### `check_dependencies()`

Check if required dependencies are available

##### `get_missing_dependencies()`

Get list of missing dependencies with install commands

##### `initialize()`

Initialize the embedding model and ChromaDB.

Args:
    model_name: Embedding model to use (default: multilingual MiniLM)
    
Returns:
    True if initialization successful

##### `is_initialized()`

Check if engine is ready for use

##### `index_tmx()`

Index a TMX file into the vector database.

Args:
    tmx_path: Path to TMX file
    progress_callback: Optional callback(current, total, message)
    domain: Domain category for this TM (e.g., "Patents", "Medical")
    
Returns:
    IndexedTM metadata or None if failed

##### `get_indexed_tm()`

Get metadata for an indexed TM

##### `get_all_indexed_tms()`

Get all indexed TMs

##### `set_tm_active()`

Set the active state of a TM

##### `get_active_tm_ids()`

Get list of TM IDs that are marked as active

##### `remove_indexed_tm()`

Remove an indexed TM completely

##### `search()`

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

##### `search_by_active_domains()`

Search using currently active domains only.

Args:
    query: Text to search for
    n_results: Maximum results
    source_lang: Source language filter
    target_lang: Target language filter
    
Returns:
    List of SearchResult filtered by active domains

##### `get_context_for_llm()`

Get relevant TM examples formatted for LLM context injection.

Args:
    source_text: The segment being translated
    n_examples: Number of examples to include
    source_lang: Source language code
    target_lang: Target language code
    use_active_domains: If True, filter by active domains
    
Returns:
    Formatted string with TM examples for prompt injection

##### `get_all_domains()`

Get all defined domains

##### `get_active_domains()`

Get only active domains

##### `add_domain()`

Add a new domain

##### `update_domain()`

Update an existing domain

##### `delete_domain()`

Delete a domain (does not affect indexed TMs)

##### `set_domain_active()`

Set a domain's active status

##### `get_domains_for_filter()`

Get list of domain names that are currently active

##### `get_unique_language_pairs()`

Get all unique language pairs from indexed TMs

##### `get_tms_by_domain()`

Get all indexed TMs for a specific domain

##### `update_tm_domain()`

Update the domain for an indexed TM

##### `get_stats()`

Get statistics about indexed content

##### `get_storage_info()`

Get detailed storage information

##### `export_to_tmx()`

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

##### `export_to_csv()`

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


---

### `IndexingThread`

**Line:** 1258

Background thread for TMX indexing

#### Methods

##### `run()`

No docstring


---

### `DomainManagerDialog`

**Line:** 1282

Dialog for managing translation domains

#### Methods


---

### `SupermemoryWidget`

**Line:** 1418

Main Supermemory UI widget for the Tools tab.
Provides TMX indexing and semantic search interface.

#### Methods


---

### `CheckmarkCheckBox`

**Line:** 2224

Custom checkbox with green background and white checkmark when checked

#### Methods

##### `paintEvent()`

Override paint event to draw white checkmark when checked


---

## Functions

### `get_install_instructions()`

**Line:** 2206

Get instructions for installing Supermemory dependencies

---

