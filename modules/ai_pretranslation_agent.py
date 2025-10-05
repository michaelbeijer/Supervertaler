"""
AI Pre-Translation Agent Module
Bridges Supervertaler's translation engines with CAT editor segments

This module provides "AI-Assisted Pre-Translation" functionality - the key innovation
that brings LLM-powered contextual translation to traditional CAT workflows.

Author: Supervertaler Project (Michael Beijer + Claude)
Date: October 5, 2025
Version: 2.5.0
"""

from typing import List, Optional, Dict, Any
import queue
from modules.segment_manager import Segment, SegmentManager


class AIPreTranslationAgent:
    """
    Bridge between Supervertaler's AI translation engines and CAT editor segments
    
    This agent takes a list of segments, sends them to the appropriate AI translation
    engine (Gemini, Claude, or OpenAI), and returns the segments with translations
    populated in the target field.
    
    Key innovation: Unlike traditional CAT tools that use basic MT (Google Translate),
    this provides full document context awareness, custom prompts, and multimodal support.
    """
    
    def __init__(self, log_queue: queue.Queue):
        """Initialize the pre-translation agent
        
        Args:
            log_queue: Queue for logging messages to the main app
        """
        self.log_queue = log_queue
        self.translation_agent = None  # Will be set when user selects AI provider
    
    def set_translation_agent(self, agent):
        """Set the active translation agent
        
        Args:
            agent: Instance of GeminiTranslationAgent, ClaudeTranslationAgent, 
                   or OpenAITranslationAgent
        """
        self.translation_agent = agent
        self.log("AI Translation engine configured")
    
    def pretranslate_segments(
        self,
        segments: List[Segment],
        source_lang: str,
        target_lang: str,
        custom_instructions: str = "",
        tm_matches: Optional[List[tuple]] = None,
        context: Optional[str] = None,
        progress_callback = None
    ) -> List[Segment]:
        """
        Pre-translate all segments using AI
        
        This is the main method that performs "AI-Assisted Pre-Translation".
        It sends segments to the AI engine and populates translations.
        
        Args:
            segments: List of Segment objects to translate
            source_lang: Source language (e.g., "English", "Dutch")
            target_lang: Target language (e.g., "French", "German")
            custom_instructions: Optional custom prompt/instructions for the AI
            tm_matches: Optional list of (source, target) TM matches for context
            context: Optional additional context (e.g., document type, domain)
            progress_callback: Optional function(current, total) for progress updates
            
        Returns:
            List of Segment objects with populated target translations
            
        Raises:
            ValueError: If no translation agent is configured
        """
        if not self.translation_agent:
            raise ValueError("No translation agent configured. Call set_translation_agent() first.")
        
        if not segments:
            self.log("No segments to translate")
            return segments
        
        self.log(f"Starting AI-assisted pre-translation of {len(segments)} segments...")
        self.log(f"Languages: {source_lang} → {target_lang}")
        
        # Extract source texts
        source_texts = [seg.source for seg in segments]
        
        # Build full context for AI
        full_context = self._build_translation_context(
            source_texts,
            source_lang,
            target_lang,
            custom_instructions,
            tm_matches,
            context
        )
        
        # Translate in batches (AI engines have token limits)
        batch_size = self._get_optimal_batch_size()
        total_segments = len(segments)
        
        for i in range(0, total_segments, batch_size):
            batch_segments = segments[i:i + batch_size]
            batch_texts = source_texts[i:i + batch_size]
            
            batch_num = (i // batch_size) + 1
            total_batches = (total_segments + batch_size - 1) // batch_size
            
            self.log(f"Translating batch {batch_num}/{total_batches} ({len(batch_texts)} segments)...")
            
            try:
                # Call the translation agent (this is where the magic happens!)
                translations = self._translate_batch(
                    batch_texts,
                    source_lang,
                    target_lang,
                    full_context
                )
                
                # Update segments with translations
                for seg, translation in zip(batch_segments, translations):
                    seg.update_target(translation, status="draft")
                
                # Update progress
                if progress_callback:
                    progress_callback(min(i + batch_size, total_segments), total_segments)
                
            except Exception as e:
                self.log(f"ERROR in batch {batch_num}: {str(e)}")
                # Mark failed segments
                for seg in batch_segments:
                    seg.update_target(f"[TRANSLATION ERROR: {str(e)}]", status="untranslated")
        
        translated_count = sum(1 for seg in segments if seg.status == "draft")
        self.log(f"✓ Pre-translation complete: {translated_count}/{total_segments} segments translated")
        
        return segments
    
    def pretranslate_untranslated_only(
        self,
        segments: List[Segment],
        source_lang: str,
        target_lang: str,
        custom_instructions: str = "",
        tm_matches: Optional[List[tuple]] = None,
        context: Optional[str] = None,
        progress_callback = None
    ) -> List[Segment]:
        """
        Pre-translate only segments with 'untranslated' status
        
        This is useful for re-running pre-translation without overwriting
        segments that have already been reviewed/edited by the user.
        
        Args: Same as pretranslate_segments()
        
        Returns:
            List of Segment objects (only untranslated ones are modified)
        """
        untranslated = [seg for seg in segments if seg.status == "untranslated"]
        
        if not untranslated:
            self.log("No untranslated segments to process")
            return segments
        
        self.log(f"Pre-translating {len(untranslated)} untranslated segments (skipping {len(segments) - len(untranslated)} already translated)...")
        
        # Translate only untranslated segments
        self.pretranslate_segments(
            untranslated,
            source_lang,
            target_lang,
            custom_instructions,
            tm_matches,
            context,
            progress_callback
        )
        
        return segments
    
    def _build_translation_context(
        self,
        source_texts: List[str],
        source_lang: str,
        target_lang: str,
        custom_instructions: str,
        tm_matches: Optional[List[tuple]],
        context: Optional[str]
    ) -> str:
        """Build rich context for AI translation
        
        Returns:
            Formatted context string to prepend to translation request
        """
        context_parts = []
        
        # Add document context if provided
        if context:
            context_parts.append(f"Document Context: {context}")
        
        # Add TM matches if provided
        if tm_matches:
            context_parts.append("Translation Memory Matches:")
            for src, tgt in tm_matches[:5]:  # Limit to top 5 matches
                context_parts.append(f"  • {src} → {tgt}")
        
        # Add custom instructions
        if custom_instructions:
            context_parts.append(f"Special Instructions: {custom_instructions}")
        
        # Full document awareness note
        context_parts.append(f"Note: You are translating part of a document with {len(source_texts)} total segments. Maintain consistency throughout.")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def _translate_batch(
        self,
        texts: List[str],
        source_lang: str,
        target_lang: str,
        context: str
    ) -> List[str]:
        """Translate a batch of texts using the configured AI agent
        
        Args:
            texts: List of source texts
            source_lang: Source language
            target_lang: Target language
            context: Contextual information for AI
            
        Returns:
            List of translated texts (same order as input)
        """
        # Prepare the input for Supervertaler's translation agents
        # They expect text with one segment per line
        combined_text = "\n".join(texts)
        
        # Add context as a prefix
        if context:
            full_input = f"{context}\n\n--- SEGMENTS TO TRANSLATE ---\n{combined_text}"
        else:
            full_input = combined_text
        
        # Call the translation agent's translate method
        # (Note: This interface may need adjustment based on actual agent implementation)
        translated_text = self.translation_agent.translate(
            full_input,
            source_lang,
            target_lang
        )
        
        # Split back into individual translations
        translations = translated_text.strip().split("\n")
        
        # Handle case where AI returns different number of lines
        if len(translations) != len(texts):
            self.log(f"WARNING: AI returned {len(translations)} translations for {len(texts)} segments")
            # Pad or truncate to match
            while len(translations) < len(texts):
                translations.append("[MISSING TRANSLATION]")
            translations = translations[:len(texts)]
        
        return translations
    
    def _get_optimal_batch_size(self) -> int:
        """Get optimal batch size based on AI provider
        
        Different AI providers have different token limits:
        - Gemini: ~30,000 tokens
        - Claude: ~200,000 tokens  
        - OpenAI: ~128,000 tokens (GPT-4)
        
        Returns:
            Recommended number of segments per batch
        """
        # Conservative default: process 50 segments at a time
        # This should work for all providers with typical segment lengths
        return 50
    
    def get_translation_statistics(self, segments: List[Segment]) -> Dict[str, Any]:
        """Get statistics about translation progress
        
        Args:
            segments: List of segments to analyze
            
        Returns:
            Dictionary with statistics
        """
        total = len(segments)
        if total == 0:
            return {
                'total': 0,
                'untranslated': 0,
                'draft': 0,
                'translated': 0,
                'approved': 0,
                'progress_percentage': 0
            }
        
        status_counts = {
            'untranslated': 0,
            'draft': 0,
            'translated': 0,
            'approved': 0
        }
        
        for seg in segments:
            status = seg.status.lower()
            if status in status_counts:
                status_counts[status] += 1
        
        # Calculate progress (draft, translated, and approved count as progress)
        completed = status_counts['draft'] + status_counts['translated'] + status_counts['approved']
        progress_pct = (completed / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            **status_counts,
            'progress_percentage': round(progress_pct, 1)
        }
    
    def log(self, message: str):
        """Log a message to the application log queue
        
        Args:
            message: Message to log
        """
        if self.log_queue:
            self.log_queue.put(message)
