"""
Term Extractor Module

Extracts potential terminology from source text for project termbases.
Can be used as a standalone tool or integrated into Supervertaler.

Author: Michael Beijer
License: MIT
"""

import re
from typing import List, Dict, Set, Optional, Tuple
from collections import Counter
import string


class TermExtractor:
    """Extract terminology from source text using various algorithms"""
    
    def __init__(self, source_lang: str = "en", min_frequency: int = 2, 
                 min_word_length: int = 3, max_ngram: int = 3):
        """
        Initialize term extractor
        
        Args:
            source_lang: Source language code (e.g., 'en', 'nl', 'de')
            min_frequency: Minimum number of occurrences to consider as term
            min_word_length: Minimum character length for single words
            max_ngram: Maximum n-gram size (1=single words, 2=bigrams, 3=trigrams)
        """
        self.source_lang = source_lang.lower()
        self.min_frequency = min_frequency
        self.min_word_length = min_word_length
        self.max_ngram = max_ngram
        
        # Common stop words by language
        self.stop_words = self._get_stop_words(source_lang)
    
    def _get_stop_words(self, lang: str) -> Set[str]:
        """Get stop words for a language"""
        # Basic stop words - can be expanded
        stop_words = {
            'en': {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                   'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                   'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                   'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
                   'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'},
            'nl': {'de', 'het', 'een', 'en', 'of', 'maar', 'in', 'op', 'aan', 'te', 'voor',
                   'van', 'met', 'bij', 'uit', 'als', 'is', 'was', 'zijn', 'waren', 'wordt',
                   'worden', 'werd', 'werden', 'hebben', 'heeft', 'had', 'hadden', 'zal',
                   'zou', 'kunnen', 'kan', 'moet', 'mag', 'dit', 'dat', 'deze', 'die',
                   'ik', 'je', 'jij', 'hij', 'zij', 'het', 'wij', 'ze'},
            'de': {'der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einer', 'einem',
                   'einen', 'eines', 'und', 'oder', 'aber', 'in', 'an', 'auf', 'zu', 'für',
                   'von', 'mit', 'bei', 'aus', 'als', 'ist', 'war', 'sind', 'waren', 'wird',
                   'werden', 'wurde', 'wurden', 'haben', 'hat', 'hatte', 'hatten', 'ich',
                   'du', 'er', 'sie', 'es', 'wir', 'ihr'},
            'fr': {'le', 'la', 'les', 'un', 'une', 'des', 'et', 'ou', 'mais', 'dans', 'sur',
                   'à', 'de', 'pour', 'avec', 'par', 'comme', 'est', 'était', 'sont', 'étaient',
                   'être', 'avoir', 'a', 'avait', 'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils'},
            'es': {'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o', 'pero',
                   'en', 'a', 'de', 'para', 'con', 'por', 'como', 'es', 'era', 'son', 'eran',
                   'ser', 'estar', 'haber', 'he', 'ha', 'yo', 'tú', 'él', 'ella', 'nosotros'},
        }
        return stop_words.get(lang, set())
    
    def extract_terms(self, text: str, use_frequency: bool = True,
                     use_capitalization: bool = True,
                     use_special_chars: bool = True) -> List[Dict[str, any]]:
        """
        Extract potential terms from text
        
        Args:
            text: Source text to analyze
            use_frequency: Consider term frequency in ranking
            use_capitalization: Give higher weight to capitalized terms
            use_special_chars: Consider terms with hyphens, underscores, etc.
            
        Returns:
            List of term dictionaries with fields: term, frequency, score, type
        """
        if not text:
            return []
        
        # Collect all candidate terms
        candidates = {}
        
        # Extract n-grams (1 to max_ngram)
        for n in range(1, self.max_ngram + 1):
            ngrams = self._extract_ngrams(text, n)
            for ngram, freq in ngrams.items():
                if ngram not in candidates:
                    candidates[ngram] = {
                        'term': ngram,
                        'frequency': freq,
                        'ngram_size': n,
                        'is_capitalized': ngram[0].isupper() if ngram else False,
                        'has_special_chars': bool(re.search(r'[-_./]', ngram))
                    }
        
        # Score and rank terms
        scored_terms = []
        for term_info in candidates.values():
            score = self._calculate_score(
                term_info,
                use_frequency=use_frequency,
                use_capitalization=use_capitalization,
                use_special_chars=use_special_chars
            )
            
            if score > 0:  # Only include terms with positive score
                scored_terms.append({
                    'term': term_info['term'],
                    'frequency': term_info['frequency'],
                    'score': score,
                    'type': self._classify_term(term_info)
                })
        
        # Sort by score (highest first)
        scored_terms.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_terms
    
    def _extract_ngrams(self, text: str, n: int) -> Dict[str, int]:
        """Extract n-grams from text"""
        # Tokenize text into words
        words = re.findall(r'\b[\w-]+\b', text.lower())
        
        # Generate n-grams
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram_words = words[i:i+n]
            
            # Skip if contains stop words (except for longer n-grams where they might be acceptable)
            if n == 1 and ngram_words[0] in self.stop_words:
                continue
            
            # Skip if too short
            if n == 1 and len(ngram_words[0]) < self.min_word_length:
                continue
            
            # Create n-gram string
            ngram = ' '.join(ngram_words)
            ngrams.append(ngram)
        
        # Count frequencies
        return dict(Counter(ngrams))
    
    def _calculate_score(self, term_info: Dict, use_frequency: bool,
                        use_capitalization: bool, use_special_chars: bool) -> float:
        """Calculate term score based on various factors"""
        score = 0.0
        
        # Base score from frequency
        if use_frequency and term_info['frequency'] >= self.min_frequency:
            # Logarithmic scale for frequency (diminishing returns)
            import math
            score += math.log(term_info['frequency'] + 1) * 2
        elif term_info['frequency'] < self.min_frequency:
            return 0.0  # Below minimum threshold
        
        # Bonus for capitalization (likely proper nouns or technical terms)
        if use_capitalization and term_info['is_capitalized']:
            score += 3.0
        
        # Bonus for special characters (technical terms, compound words)
        if use_special_chars and term_info['has_special_chars']:
            score += 2.0
        
        # Bonus for longer n-grams (multi-word terms often more valuable)
        if term_info['ngram_size'] > 1:
            score += term_info['ngram_size'] * 1.5
        
        return score
    
    def _classify_term(self, term_info: Dict) -> str:
        """Classify term type"""
        if term_info['is_capitalized']:
            return 'proper_noun'
        elif term_info['has_special_chars']:
            return 'technical'
        elif term_info['ngram_size'] > 1:
            return 'phrase'
        else:
            return 'word'
    
    def extract_from_segments(self, segments: List[str]) -> List[Dict[str, any]]:
        """
        Extract terms from a list of segments (e.g., translation project)
        
        Args:
            segments: List of source text segments
            
        Returns:
            List of extracted term dictionaries
        """
        # Combine all segments into one text
        combined_text = '\n'.join(segments)
        return self.extract_terms(combined_text)
    
    def filter_by_frequency(self, terms: List[Dict], min_freq: int = None,
                           max_freq: int = None) -> List[Dict]:
        """Filter terms by frequency range"""
        if min_freq is None:
            min_freq = self.min_frequency
        
        filtered = [t for t in terms if t['frequency'] >= min_freq]
        
        if max_freq:
            filtered = [t for t in filtered if t['frequency'] <= max_freq]
        
        return filtered
    
    def filter_by_type(self, terms: List[Dict], term_types: List[str]) -> List[Dict]:
        """Filter terms by type"""
        return [t for t in terms if t['type'] in term_types]
    
    def filter_by_score(self, terms: List[Dict], min_score: float) -> List[Dict]:
        """Filter terms by minimum score"""
        return [t for t in terms if t['score'] >= min_score]
    
    def deduplicate_terms(self, terms: List[Dict]) -> List[Dict]:
        """Remove duplicate terms (case-insensitive)"""
        seen = set()
        unique = []
        
        for term in terms:
            term_lower = term['term'].lower()
            if term_lower not in seen:
                seen.add(term_lower)
                unique.append(term)
        
        return unique


# Convenience function for quick extraction
def extract_terms_from_text(text: str, source_lang: str = "en",
                           min_frequency: int = 2, max_terms: int = 100) -> List[str]:
    """
    Quick term extraction - returns just the term strings
    
    Args:
        text: Source text
        source_lang: Language code
        min_frequency: Minimum occurrences
        max_terms: Maximum number of terms to return
        
    Returns:
        List of term strings
    """
    extractor = TermExtractor(source_lang=source_lang, min_frequency=min_frequency)
    terms = extractor.extract_terms(text)
    return [t['term'] for t in terms[:max_terms]]


# Example usage
if __name__ == "__main__":
    sample_text = """
    The system architecture includes a database manager, termbase manager, and 
    translation memory. The database manager handles all database operations.
    The termbase manager provides terminology management functionality.
    Translation memory stores previously translated segments for reuse.
    """
    
    extractor = TermExtractor(source_lang="en", min_frequency=2)
    terms = extractor.extract_terms(sample_text)
    
    print("Extracted Terms:")
    for term in terms[:10]:
        print(f"  {term['term']:<30} freq={term['frequency']:<3} score={term['score']:.2f} type={term['type']}")
