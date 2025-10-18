"""
Document Analyzer Module

Analyzes loaded document segments to provide context-aware insights and suggestions.
Part of Phase 2 AI Assistant implementation.

Features:
- Domain detection (medical, legal, technical, etc.)
- Terminology extraction and analysis
- Tone and formality assessment
- Document structure analysis
- Prompt optimization suggestions
"""

import re
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple


class DocumentAnalyzer:
    """Analyzes document content to provide AI-powered insights"""
    
    # Domain keywords for detection
    DOMAIN_KEYWORDS = {
        'medical': {
            'keywords': ['patient', 'diagnosis', 'treatment', 'medication', 'clinical', 'medical', 
                        'hospital', 'doctor', 'surgery', 'therapeutic', 'pharmaceutical', 'disease',
                        'symptom', 'therapy', 'prescription', 'dosage', 'adverse', 'pathology'],
            'patterns': [r'\d+\s*mg', r'\d+\s*ml', r'ICD-\d+', r'[A-Z]{3,}\s+\d+']
        },
        'legal': {
            'keywords': ['contract', 'agreement', 'party', 'clause', 'hereby', 'whereas', 'pursuant',
                        'liability', 'jurisdiction', 'arbitration', 'plaintiff', 'defendant', 'court',
                        'law', 'regulation', 'statute', 'breach', 'damages', 'legal', 'attorney'],
            'patterns': [r'§\s*\d+', r'Article\s+\d+', r'\(\d+\)', r'Section\s+\d+\.\d+']
        },
        'technical': {
            'keywords': ['system', 'configuration', 'parameter', 'interface', 'protocol', 'function',
                        'module', 'component', 'specification', 'operation', 'procedure', 'mechanism',
                        'algorithm', 'implementation', 'hardware', 'software', 'network', 'database'],
            'patterns': [r'\d+\.\d+\.\d+', r'[A-Z]{2,}\d+', r'\w+\(\)', r'[A-Z_]{3,}']
        },
        'patent': {
            'keywords': ['invention', 'claim', 'embodiment', 'apparatus', 'method', 'comprising',
                        'wherein', 'patent', 'prior art', 'novelty', 'utility', 'figure', 'drawing',
                        'applicant', 'inventor', 'chemical', 'compound', 'formula'],
            'patterns': [r'Figure\s+\d+', r'claim\s+\d+', r'Fig\.\s*\d+', r'\([IVX]+\)']
        },
        'marketing': {
            'keywords': ['brand', 'customer', 'product', 'service', 'campaign', 'audience', 'market',
                        'engagement', 'strategy', 'creative', 'promotion', 'sales', 'consumer',
                        'advertising', 'content', 'message', 'value', 'experience'],
            'patterns': [r'®', r'™', r'©', r'\d+%\s+(?:more|less|increase|decrease)']
        },
        'financial': {
            'keywords': ['investment', 'revenue', 'profit', 'asset', 'liability', 'equity', 'financial',
                        'fiscal', 'budget', 'expense', 'income', 'balance', 'statement', 'accounting',
                        'audit', 'dividend', 'portfolio', 'securities', 'capital'],
            'patterns': [r'\$[\d,]+', r'€[\d,]+', r'£[\d,]+', r'\d+\.\d+%', r'Q[1-4]\s+\d{4}']
        }
    }
    
    def __init__(self):
        """Initialize the document analyzer"""
        self.segments = []
        self.analysis_cache = {}
    
    def analyze_segments(self, segments: List) -> Dict:
        """
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
        """
        self.segments = segments
        
        if not segments:
            return {
                'success': False,
                'error': 'No segments to analyze'
            }
        
        # Extract all source text
        source_texts = [seg.source for seg in segments if hasattr(seg, 'source') and seg.source]
        
        if not source_texts:
            return {
                'success': False,
                'error': 'No source text found in segments'
            }
        
        combined_text = ' '.join(source_texts)
        
        # Perform analysis
        analysis = {
            'success': True,
            'segment_count': len(segments),
            'domain': self._detect_domain(source_texts, combined_text),
            'terminology': self._extract_terminology(source_texts),
            'tone': self._assess_tone(combined_text),
            'structure': self._analyze_structure(segments, source_texts),
            'statistics': self._calculate_statistics(source_texts),
            'special_elements': self._detect_special_elements(combined_text),
            'suggestions': []
        }
        
        # Generate suggestions based on analysis
        analysis['suggestions'] = self._generate_suggestions(analysis)
        
        return analysis
    
    def _detect_domain(self, texts: List[str], combined_text: str) -> Dict:
        """Detect the primary domain(s) of the document"""
        domain_scores = defaultdict(int)
        
        combined_lower = combined_text.lower()
        
        for domain, data in self.DOMAIN_KEYWORDS.items():
            # Score based on keyword matches
            for keyword in data['keywords']:
                count = combined_lower.count(keyword)
                domain_scores[domain] += count * 2  # Keywords worth more
            
            # Score based on pattern matches
            for pattern in data['patterns']:
                matches = re.findall(pattern, combined_text)
                domain_scores[domain] += len(matches)
        
        # Normalize scores
        total_words = len(combined_text.split())
        if total_words > 0:
            domain_scores = {k: (v / total_words) * 1000 for k, v in domain_scores.items()}
        
        # Get top domains
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        
        primary = sorted_domains[0] if sorted_domains and sorted_domains[0][1] > 1 else None
        secondary = sorted_domains[1] if len(sorted_domains) > 1 and sorted_domains[1][1] > 0.5 else None
        
        return {
            'primary': primary[0] if primary else 'general',
            'primary_confidence': round(primary[1], 2) if primary else 0,
            'secondary': secondary[0] if secondary else None,
            'secondary_confidence': round(secondary[1], 2) if secondary else 0,
            'all_scores': dict(sorted_domains[:5])
        }
    
    def _extract_terminology(self, texts: List[str]) -> Dict:
        """Extract and analyze key terminology"""
        # Combine all text
        combined = ' '.join(texts)
        
        # Extract potential terms (capitalized words, technical terms, etc.)
        # Capitalized words (potential proper nouns or technical terms)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', combined)
        
        # Acronyms (but filter out Roman numerals and single letters)
        acronyms_raw = re.findall(r'\b[A-Z]{2,}\b', combined)
        acronyms = [a for a in acronyms_raw if not re.match(r'^[IVXLCDM]+$', a)]  # Filter Roman numerals
        
        # Technical terms with numbers (but must have letters too)
        # Pattern: word containing both letters and numbers, or camelCase, or underscore
        technical_raw = re.findall(r'\b(?:[a-zA-Z]+\d+[a-zA-Z\d]*|\d+[a-zA-Z]+[a-zA-Z\d]*|[a-z]+[A-Z][a-zA-Z]*|[a-z]+_[a-z]+)\b', combined)
        
        # Filter out: pure numbers, very short terms (< 3 chars), common words
        technical = [t for t in technical_raw 
                    if len(t) >= 3 
                    and not t.isdigit()  # Not pure numbers
                    and not t.lower() in ['the', 'and', 'for', 'are', 'van', 'het', 'een', 'een']]  # Common words
        
        # Count frequencies
        cap_counter = Counter(capitalized)
        acro_counter = Counter(acronyms)
        tech_counter = Counter(technical)
        
        return {
            'capitalized_terms': dict(cap_counter.most_common(15)),  # Increased from 10 to 15
            'acronyms': dict(acro_counter.most_common(15)),
            'technical_terms': dict(tech_counter.most_common(15)),
            'total_unique_terms': len(set(capitalized + acronyms + technical))
        }
    
    def _assess_tone(self, text: str) -> Dict:
        """Assess the tone and formality of the text"""
        text_lower = text.lower()
        
        # Formal/Legal indicators (stronger weight for patents/legal)
        formal_indicators = ['hereby', 'pursuant', 'whereas', 'thereof', 'aforementioned',
                            'notwithstanding', 'shall', 'must', 'required', 'specified',
                            'comprising', 'wherein', 'embodiment', 'invention', 'claim']
        formal_count = sum(text_lower.count(ind) for ind in formal_indicators)
        
        # Informal indicators
        informal_indicators = ["don't", "can't", "won't", "it's", "you'll", "we're",
                              'really', 'just', 'pretty', 'quite', 'maybe', 'probably']
        informal_count = sum(text_lower.count(ind) for ind in informal_indicators)
        
        # Technical indicators
        technical_indicators = ['algorithm', 'parameter', 'configuration', 'implementation',
                               'interface', 'protocol', 'specification', 'mechanism',
                               'apparatus', 'method', 'device', 'system', 'process']
        technical_count = sum(text_lower.count(ind) for ind in technical_indicators)
        
        # Conversational indicators (but filter out common words in formal contexts)
        # Only count these if they appear in clearly conversational patterns
        conversational_patterns = [r'\byou can\b', r'\byour \w+\b', r'\bwe recommend\b', 
                                  r'\blet\'s\b', r'\bwant to\b', r'\bneed to\b']
        conversational_count = sum(len(re.findall(pattern, text_lower)) for pattern in conversational_patterns)
        
        # Determine primary tone
        total_words = len(text.split())
        if total_words == 0:
            return {'tone': 'unknown', 'formality': 'unknown'}
        
        formal_ratio = (formal_count / total_words) * 1000
        informal_ratio = (informal_count / total_words) * 1000
        technical_ratio = (technical_count / total_words) * 1000
        conversational_ratio = (conversational_count / total_words) * 1000
        
        # Determine formality
        if formal_ratio > 5:
            formality = 'very formal'
        elif formal_ratio > 2 or technical_ratio > 3:
            formality = 'formal'
        elif informal_ratio > 3 or conversational_ratio > 10:
            formality = 'informal'
        else:
            formality = 'neutral'
        
        # Determine tone
        if technical_ratio > 2:
            tone = 'technical'
        elif conversational_ratio > 8:
            tone = 'conversational'
        elif formal_ratio > 3:
            tone = 'professional'
        else:
            tone = 'neutral'
        
        return {
            'tone': tone,
            'formality': formality,
            'formal_score': round(formal_ratio, 2),
            'informal_score': round(informal_ratio, 2),
            'technical_score': round(technical_ratio, 2),
            'conversational_score': round(conversational_ratio, 2)
        }
    
    def _analyze_structure(self, segments: List, texts: List[str]) -> Dict:
        """Analyze document structure"""
        # Detect lists
        list_items = sum(1 for text in texts if re.match(r'^\s*[-•*\d+\.]\s', text))
        
        # Detect headings (short segments, possibly all caps or title case)
        potential_headings = sum(1 for text in texts 
                                if len(text.split()) <= 10 and (text.isupper() or text.istitle()))
        
        # Detect references to figures/tables
        figure_refs = sum(len(re.findall(r'Figure\s+\d+|Fig\.\s*\d+|Table\s+\d+', text)) 
                         for text in texts)
        
        # Average segment length
        avg_length = sum(len(text.split()) for text in texts) / len(texts) if texts else 0
        
        return {
            'list_items': list_items,
            'potential_headings': potential_headings,
            'figure_references': figure_refs,
            'average_segment_length': round(avg_length, 1),
            'has_visual_elements': figure_refs > 0
        }
    
    def _calculate_statistics(self, texts: List[str]) -> Dict:
        """Calculate basic statistics"""
        combined = ' '.join(texts)
        words = combined.split()
        
        return {
            'total_words': len(words),
            'total_characters': len(combined),
            'average_words_per_segment': round(len(words) / len(texts), 1) if texts else 0,
            'unique_words': len(set(word.lower() for word in words))
        }
    
    def _detect_special_elements(self, text: str) -> Dict:
        """Detect special elements in the text"""
        return {
            'urls': len(re.findall(r'https?://\S+', text)),
            'emails': len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
            'dates': len(re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)),
            'numbers': len(re.findall(r'\b\d+(?:\.\d+)?\b', text)),
            'percentages': len(re.findall(r'\d+(?:\.\d+)?%', text)),
            'currencies': len(re.findall(r'[$€£¥]\s*\d+', text)),
            'measurements': len(re.findall(r'\d+\s*(?:mm|cm|m|km|mg|g|kg|ml|l|°C|°F)', text))
        }
    
    def _generate_suggestions(self, analysis: Dict) -> List[Dict]:
        """Generate prompt optimization suggestions based on analysis"""
        suggestions = []
        
        domain = analysis.get('domain', {})
        tone = analysis.get('tone', {})
        structure = analysis.get('structure', {})
        special = analysis.get('special_elements', {})
        
        # Domain-specific suggestions
        primary_domain = domain.get('primary', 'general')
        if primary_domain != 'general' and domain.get('primary_confidence', 0) > 2:
            suggestions.append({
                'type': 'domain',
                'priority': 'high',
                'title': f'Optimize for {primary_domain.title()} Domain',
                'description': f'Your document appears to be {primary_domain}-related. '
                             f'Consider using a specialized {primary_domain} translation prompt.',
                'action': f'switch_prompt_{primary_domain}'
            })
        
        # Tone suggestions
        if tone.get('formality') == 'very formal':
            suggestions.append({
                'type': 'tone',
                'priority': 'medium',
                'title': 'Very Formal Language Detected',
                'description': 'This document uses highly formal language. Ensure your prompt '
                             'emphasizes maintaining professional tone and formal register.',
                'action': 'add_formality_instruction'
            })
        
        # Visual elements
        if structure.get('figure_references', 0) > 0:
            suggestions.append({
                'type': 'visual',
                'priority': 'high',
                'title': 'Figure References Detected',
                'description': f'Found {structure["figure_references"]} references to figures. '
                             'Consider loading visual context in the Images tab.',
                'action': 'load_figure_context'
            })
        
        # Special elements
        if special.get('measurements', 0) > 5:
            suggestions.append({
                'type': 'formatting',
                'priority': 'medium',
                'title': 'Preserve Measurement Units',
                'description': 'Document contains many measurements. Add instruction to '
                             'preserve units exactly as written.',
                'action': 'add_measurement_rule'
            })
        
        if special.get('currencies', 0) > 3:
            suggestions.append({
                'type': 'formatting',
                'priority': 'medium',
                'title': 'Currency Values Present',
                'description': 'Document contains currency values. Ensure prompt specifies '
                             'how to handle currency symbols and amounts.',
                'action': 'add_currency_rule'
            })
        
        # Terminology
        terminology = analysis.get('terminology', {})
        unique_terms = terminology.get('total_unique_terms', 0)
        if unique_terms > 20:
            suggestions.append({
                'type': 'terminology',
                'priority': 'medium',
                'title': 'Rich Terminology Detected',
                'description': f'Found {unique_terms} unique technical/specialized terms. '
                             'Consider using a glossary for consistent translation.',
                'action': 'enable_glossary'
            })
        
        return suggestions
    
    def get_summary_text(self, analysis: Dict) -> str:
        """Generate human-readable summary of analysis"""
        if not analysis.get('success'):
            return "❌ Unable to analyze document: " + analysis.get('error', 'Unknown error')
        
        domain = analysis.get('domain', {})
        tone = analysis.get('tone', {})
        stats = analysis.get('statistics', {})
        structure = analysis.get('structure', {})
        
        summary = f"""📊 Document Analysis Results

📝 **Overview:**
- {analysis['segment_count']} segments
- {stats.get('total_words', 0):,} words total
- {stats.get('average_words_per_segment', 0)} words per segment on average

🎯 **Domain:** {domain.get('primary', 'General').title()}"""
        
        if domain.get('primary_confidence', 0) > 2:
            summary += f" (confidence: {domain['primary_confidence']:.1f})"
        
        if domain.get('secondary'):
            summary += f"\n   Secondary: {domain['secondary'].title()}"
        
        summary += f"""

✍️ **Tone & Style:**
- Formality: {tone.get('formality', 'unknown').title()}
- Style: {tone.get('tone', 'unknown').title()}

📋 **Structure:**
- List items: {structure.get('list_items', 0)}
- Potential headings: {structure.get('potential_headings', 0)}
- Figure references: {structure.get('figure_references', 0)}
"""
        
        # Add suggestions summary
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            summary += f"\n💡 **Recommendations:** {len(suggestions)} suggestion(s) available"
        
        return summary
