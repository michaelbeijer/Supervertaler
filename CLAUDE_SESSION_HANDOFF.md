# Claude Session Handoff - Grid Performance & Build System

> **Created:** January 30, 2026
> **Purpose:** Summary of discussion from Claude Code for Desktop session, to continue in VS Code
> **Branch:** `claude/optimize-cat-grid-performance-qoMxy`

---

## Issue 1: Grid Responsiveness / Cache System Upgrade

### Problem Statement

The CAT grid needs to feel instant when clicking between segments. Currently, TM matches and glossary/termbase matches can feel sluggish, making translators wait.

### Current Architecture

Supervertaler has two approaches (toggle via `disable_all_caches` setting):

#### A. Multi-Cache System (older, complex)
- **termbase_cache**: Maps `segment_id → {term: match_dict}`
- **translation_matches_cache**: Maps `segment_id → {"TM": [...], "Termbases": [...], "MT": [...], "LLM": [...]}`
- **Prefetch worker**: Background thread pre-populates cache for next 5-20 segments
- **Batch worker**: On project load, pre-populates termbase cache for ALL segments
- **Idle prefetch**: After 1.5s typing pause, prefetches upcoming segments

#### B. Cache Kill Switch (newer, simpler)
- `disable_all_caches = True` (default since v1.9.170)
- Every segment selection triggers fresh database lookups
- Simpler code path, but slower for rapid navigation

### Key Files

| Component | File | Key Lines |
|-----------|------|-----------|
| Cache init | `Supervertaler.py` | ~6220-6244 |
| Cell selection | `Supervertaler.py` | ~31293-31820 |
| TM search | `modules/database_manager.py` | ~887-1147 |
| Termbase search | `Supervertaler.py` | ~22322-22500 |
| Prefetch worker | `Supervertaler.py` | ~22567-22694 |
| TermView widget | `modules/termview_widget.py` | full file |

### Identified Bottlenecks

| Area | Issue | Impact |
|------|-------|--------|
| **TM Search** | FTS5 fetches 500 candidates per TM, then calculates SequenceMatcher similarity for each | ~50-200ms per TM |
| **Termbase Search** | Per-word LIKE queries with UNION for bidirectional matching | ~20-100ms depending on word count |
| **Empty Results Not Cached** | Line ~22652: `if total_matches > 0` means segments with no matches are re-searched every time | Wasted DB queries |
| **Debounce Delays** | 150ms (arrow nav) + 300ms (TM/MT/LLM) = 450ms minimum before results appear | Perceived lag |
| **TermView Rendering** | `clear_terms()` + recreate all widgets from scratch | UI thread blocking |

---

## Proposed Solution: "Total Recall" Architecture (CafeTran-style)

### Concept

Instead of querying giant TMs on every segment click, extract relevant segments into a lightweight "Project TM" on project load.

```
┌─────────────────────────────────────────────────────────────────┐
│                      TOTAL RECALL (Archive)                      │
│                    Giant SQLite DB (millions)                    │
│                                                                  │
│  Used for: Concordance searches (user expects delay)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Project Load: Extract relevant segments
                              │ (one-time cost, can show progress bar)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT TM (Working Set)                      │
│               In-memory SQLite or Python dict                    │
│                                                                  │
│  Only segments that match project source text:                  │
│  • Exact matches (100%)                                         │
│  • Fuzzy matches (≥75%)                                         │
│  • Typically 1-5% of Total Recall size                          │
│                                                                  │
│  Used for: Grid lookups (instant)                               │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation Plan

#### Step 1: In-Memory Termbase Index (Quick Win)
Load all termbase terms into a Python `dict` on project load for O(1) lookups:

```python
# On project load: build in-memory index
self.termbase_index = {}  # {lowercase_term: [match_info, ...]}
for term in all_terms:
    key = term['source_term'].lower()
    self.termbase_index.setdefault(key, []).append(term)

# On segment selection: instant lookup
def find_terms(source_text):
    words = source_text.lower().split()
    matches = {}
    for word in words:
        if word in self.termbase_index:
            matches.update(self.termbase_index[word])
    return matches
```

#### Step 2: Project TM Class
Create a new `ProjectTM` class with in-memory SQLite:

```python
class ProjectTM:
    """Lightweight in-memory TM extracted from Total Recall"""

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("""
            CREATE TABLE segments (
                id INTEGER PRIMARY KEY,
                source TEXT,
                target TEXT,
                source_lower TEXT,
                tm_name TEXT,
                match_pct INTEGER
            )
        """)
        self.conn.execute("CREATE INDEX idx_source ON segments(source_lower)")

    def extract_from_total_recall(self, project_segments, total_recall_db,
                                   threshold=75, progress_callback=None):
        """Extract relevant segments on project load"""
        unique_sources = set(seg.source for seg in project_segments)
        for i, source in enumerate(unique_sources):
            if progress_callback:
                progress_callback(i, len(unique_sources))
            matches = total_recall_db.search_fuzzy(source, threshold=threshold)
            for match in matches:
                self.conn.execute(
                    "INSERT INTO segments VALUES (NULL, ?, ?, ?, ?, ?)",
                    (match['source'], match['target'], match['source'].lower(),
                     match['tm_name'], match['match_pct'])
                )
        self.conn.commit()

    def search(self, source_text, max_results=10):
        """Instant lookup - called on every segment click"""
        # Fast exact match
        cursor = self.conn.execute(
            "SELECT * FROM segments WHERE source_lower = ? LIMIT 1",
            (source_text.lower(),)
        )
        exact = cursor.fetchone()
        if exact:
            return [dict(exact)]

        # Return pre-computed fuzzy matches
        cursor = self.conn.execute(
            "SELECT * FROM segments WHERE source_lower LIKE ? ORDER BY match_pct DESC LIMIT ?",
            (f"%{source_text.lower()[:20]}%", max_results)
        )
        return [dict(row) for row in cursor.fetchall()]
```

#### Step 3: Wire Into Project Load

```python
def load_project(self, project):
    # 1. Load project immediately
    self._load_project_segments(project)

    # 2. Load termbase into memory (instant lookups)
    self._build_termbase_index()

    # 3. Start background Project TM extraction
    self.project_tm = ProjectTM()
    self.extraction_thread = threading.Thread(
        target=self._extract_project_tm,
        args=(project.segments,),
        daemon=True
    )
    self.extraction_thread.start()

    # Grid is usable immediately - TM matches appear as extraction progresses
```

### Quick Wins (Can Implement First)

1. **Cache empty results** - Fix line ~22652 to cache segments with no matches
2. **Reduce TM candidate limit** - Change from 500 to 100 in `database_manager.py:1019`
3. **Reduce debounce delays** - 150ms → 50ms, 300ms → 100ms

### Expected Results

| Metric | Current | After Implementation |
|--------|---------|---------------------|
| Termbase lookup | 20-100ms | <1ms |
| TM lookup (grid) | 50-200ms | <5ms |
| Project load | Fast | Slightly slower (extraction) |
| Concordance search | Same | Same (uses archive) |

---

## Issue 2: Unified Build System

### Current State

- **Single spec file exists:** `Supervertaler.spec` (unified)
- **Old CORE/FULL specs:** Deleted (no longer exist)
- **PowerShell script:** `build_windows_release.ps1` is **OUTDATED** - still references non-existent CORE/FULL specs

### What Needs to Be Done

Update or replace the build system to use the single unified spec:

#### Option A: Update PowerShell Script
Simplify `build_windows_release.ps1` to just:
```powershell
pyinstaller Supervertaler.spec --clean
# Copy user_data
# Create ZIP
```

#### Option B: Create Python Build Script (Cross-Platform)
Create `build_release.py` that works on both Windows and Linux:
```python
# Usage:
# python build_release.py
# python build_release.py --clean
```

### Current Build Command (Manual)
Until the script is updated, you can build manually:
```powershell
pyinstaller Supervertaler.spec --clean
```

---

## Recommended Implementation Order

1. **Quick wins** - Cache empty results, reduce delays (30 min)
2. **In-memory termbase index** - Biggest speed improvement (1 hour)
3. **ProjectTM class** - Total Recall architecture (2-3 hours)
4. **Update build script** - Fix the outdated PowerShell script (30 min)

---

## Questions to Resolve

1. Should Project TM extraction block project load, or run in background with progress indicator?
2. Should we keep the `disable_all_caches` toggle, or remove it once new system is proven?
3. For the build script: Python (cross-platform) or stick with PowerShell (Windows-only)?

---

## References

- CafeTran's "Total Recall" feature - inspiration for this architecture
- Key insight: Translators spend 95% of time navigating grid, 5% doing concordance searches
