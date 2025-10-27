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


# Quick test
if __name__ == "__main__":
    segmenter = SimpleSegmenter()
    
    test_text = """
    This is a test sentence. This is another sentence! 
    Dr. Smith works at Inc. Corp. The company has many employees.
    What about questions? They work too. And exclamations!
    """
    
    segments = segmenter.segment_text(test_text)
    
    print(f"Found {len(segments)} segments:")
    for i, seg in enumerate(segments, 1):
        print(f"{i}. {seg}")
