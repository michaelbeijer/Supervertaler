"""
Simple Segmenter
Basic sentence segmentation using regex patterns
"""

import re
from typing import List

class SimpleSegmenter:
    """Simple sentence segmenter using regex patterns"""
    
    def __init__(self):
        # Common abbreviations that shouldn't trigger sentence breaks
        self.abbreviations = {
            'mr', 'mrs', 'ms', 'dr', 'prof', 'sr', 'jr',
            'inc', 'ltd', 'co', 'corp', 'fig', 'figs',
            'etc', 'vs', 'e.g', 'i.e', 'cf', 'approx', 'ca',
            'no', 'nos', 'vol', 'p', 'pp', 'art', 'op'
        }
    
    def segment_text(self, text: str) -> List[str]:
        """
        Segment text into sentences
        
        Returns: List of sentences
        """
        if not text or not text.strip():
            return []
        
        # Replace newlines with spaces (preserve paragraph structure elsewhere)
        text = text.replace('\n', ' ').replace('\r', '')
        
        # Find potential sentence boundaries
        # Pattern: sentence-ending punctuation followed by space and capital letter or quote
        pattern = r'([.!?]+)\s+(?=[A-Z"\'])'
        
        # Split but keep the punctuation
        parts = re.split(pattern, text)
        
        # Reconstruct sentences
        sentences = []
        i = 0
        while i < len(parts):
            if i + 1 < len(parts) and parts[i+1] in ['.', '!', '?', '...', '.)', '."']:
                # Combine text with its ending punctuation
                sentence = (parts[i] + parts[i+1]).strip()
                i += 2
            else:
                sentence = parts[i].strip()
                i += 1
            
            if sentence and not self._is_abbreviation_only(sentence):
                sentences.append(sentence)
        
        # Post-process: merge sentences that were incorrectly split at abbreviations
        sentences = self._merge_abbreviation_splits(sentences)
        
        return sentences
    
    def _is_abbreviation_only(self, text: str) -> bool:
        """Check if text is just an abbreviation"""
        cleaned = text.lower().rstrip('.')
        return cleaned in self.abbreviations
    
    def _merge_abbreviation_splits(self, sentences: List[str]) -> List[str]:
        """Merge sentences that were incorrectly split at abbreviations"""
        if not sentences:
            return []
        
        merged = []
        current = sentences[0]
        
        for i in range(1, len(sentences)):
            # Check if previous sentence ends with common abbreviation
            prev_words = current.split()
            if prev_words:
                last_word = prev_words[-1].lower().rstrip('.')
                
                # If it's an abbreviation and next sentence starts with lowercase
                # or is very short, merge them
                if (last_word in self.abbreviations and 
                    (sentences[i][0].islower() or len(sentences[i]) < 10)):
                    current += ' ' + sentences[i]
                    continue
            
            # Otherwise, save current and start new
            merged.append(current)
            current = sentences[i]
        
        # Don't forget the last one
        merged.append(current)
        
        return merged
    
    def segment_paragraphs(self, paragraphs: List[str]) -> List[tuple]:
        """
        Segment a list of paragraphs, tracking which paragraph each segment belongs to
        
        Returns: List of (paragraph_index, segment_text) tuples
        """
        all_segments = []
        
        for para_idx, paragraph in enumerate(paragraphs):
            if not paragraph.strip():
                continue
                
            segments = self.segment_text(paragraph)
            for segment in segments:
                all_segments.append((para_idx, segment))
        
        return all_segments


class MarkdownSegmenter(SimpleSegmenter):
    """Markdown-aware sentence segmenter.

    Protects markdown constructs (links, images, inline code, code spans,
    reference-style links, HTML tags) from being incorrectly split by the
    sentence boundary detector, then restores them after splitting.
    """

    # Patterns ordered from most specific to least specific to avoid
    # partial matches.  Each pattern is compiled once at class level.
    _MD_PATTERNS = [
        # Fenced code blocks (``` ... ```) — should not appear mid-line but
        # protect just in case (non-greedy across backticks)
        re.compile(r'```.*?```', re.DOTALL),
        # Inline code spans with double backticks (`` ... ``)
        re.compile(r'``[^`]+``'),
        # Inline code spans with single backticks (` ... `)
        re.compile(r'`[^`]+`'),
        # Images: ![alt](url "optional title")
        re.compile(r'!\[[^\]]*\]\([^)]+\)'),
        # Inline links: [text](url "optional title")
        re.compile(r'\[[^\]]*\]\([^)]+\)'),
        # Reference-style links/images: [text][ref] or ![alt][ref]
        re.compile(r'!?\[[^\]]*\]\[[^\]]*\]'),
        # Autolinks: <https://...> or <user@example.com>
        re.compile(r'<(?:https?://[^>]+|[^>]+@[^>]+)>'),
        # Bare URLs (http/https) — common in markdown even without angle brackets
        re.compile(r'https?://\S+'),
        # HTML tags: <tag attr="val"> or </tag> or <br/> etc.
        re.compile(r'</?[a-zA-Z][a-zA-Z0-9]*(?:\s+[^>]*)?>'),
    ]

    def segment_text(self, text: str) -> list:
        """Segment text into sentences, protecting markdown constructs."""
        if not text or not text.strip():
            return []

        # Phase 1: Replace markdown constructs with placeholders
        placeholders = {}
        protected = text

        def _make_placeholder(match):
            idx = len(placeholders)
            key = f'\x00MD{idx}\x00'
            placeholders[key] = match.group(0)
            return key

        for pattern in self._MD_PATTERNS:
            protected = pattern.sub(_make_placeholder, protected)

        # Phase 2: Run normal sentence segmentation on protected text
        sentences = super().segment_text(protected)

        # Phase 3: Restore placeholders in each sentence
        restored = []
        for sentence in sentences:
            for key, original in placeholders.items():
                sentence = sentence.replace(key, original)
            restored.append(sentence)

        return restored


# Quick test
if __name__ == "__main__":
    print("=== SimpleSegmenter ===")
    segmenter = SimpleSegmenter()

    test_text = """
    This is a test sentence. This is another sentence!
    Dr. Smith works at Inc. Corp. The company has many employees.
    What about questions? They work too. And exclamations!
    """

    segments = segmenter.segment_text(test_text)
    print(f"Found {len(segments)} segments:")
    for i, seg in enumerate(segments, 1):
        print(f"  {i}. {seg}")

    print("\n=== MarkdownSegmenter ===")
    md_segmenter = MarkdownSegmenter()

    md_tests = [
        "See [the docs](https://example.com/page.html) for details. This is the next sentence.",
        "Use `str.split()` to tokenize. Then call `re.match()` to validate. Finally return the result.",
        "Check the ![logo](img/logo.png) image. It should render correctly.",
        "Visit https://example.com/path.html for more info. The site has good docs.",
        "Read the <a href=\"https://example.com\">documentation</a> first. Then try the examples.",
    ]

    for test in md_tests:
        print(f"\n  Input: {test}")
        segments = md_segmenter.segment_text(test)
        for i, seg in enumerate(segments, 1):
            print(f"    {i}. {seg}")
