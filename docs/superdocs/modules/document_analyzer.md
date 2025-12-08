# document_analyzer

**File:** `modules/document_analyzer.py`
**Lines:** 427
**Classes:** 1
**Functions:** 0

---

## Module Description

Document Analyzer Module

Analyzes loaded document segments to provide context-aware insights and suggestions.
Part of Phase 2 AI Assistant implementation.

Features:
- Domain detection (medical, legal, technical, etc.)
- Terminology extraction and analysis
- Tone and formality assessment
- Document structure analysis
- Prompt optimization suggestions

---

## Classes

### `DocumentAnalyzer`

**Line:** 20

Analyzes document content to provide AI-powered insights

#### Methods

##### `analyze_segments()`

Comprehensive analysis of loaded document segments.

Args:
    segments: List of Segment objects from the translation grid

Returns:
    Dictionary containing analysis results:
    - domain: Detected domain(s)
    - terminology: Key terms and phrases
    - tone: Formality level and style
    - structure: Document organization
    - statistics: Word counts, segment counts, etc.
    - suggestions: Recommended prompt adjustments

##### `get_summary_text()`

Generate human-readable summary of analysis


---

