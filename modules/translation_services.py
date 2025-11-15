"""
Translation Services Module
Handles Machine Translation (MT) and Large Language Model (LLM) integration
Keeps main application file clean and manageable

Author: Michael Beijer
License: MIT
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging


@dataclass
class TranslationRequest:
    """Request object for translation services"""
    source_text: str
    source_lang: str
    target_lang: str
    context: Optional[str] = None
    source_lang_code: Optional[str] = None
    target_lang_code: Optional[str] = None


@dataclass
class TranslationResult:
    """Result object from translation services"""
    source: str
    target: str
    relevance: int
    metadata: Dict[str, Any]
    match_type: str  # 'MT' or 'LLM'
    provider_code: str
    success: bool = True
    error: Optional[str] = None


class TranslationServices:
    """
    Main class for handling all translation services (MT and LLM)
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize translation services
        
        Args:
            config: Configuration dictionary with service settings
        """
        self.config = config or {}
        
        # Service availability flags
        self.google_translate_enabled = self.config.get('google_translate_enabled', True)
        self.deepl_enabled = self.config.get('deepl_enabled', False)
        self.openai_enabled = self.config.get('openai_enabled', True)
        self.claude_enabled = self.config.get('claude_enabled', True)
        
        # Enable/disable flags
        self.enable_mt_matching = self.config.get('enable_mt_matching', True)
        self.enable_llm_matching = self.config.get('enable_llm_matching', True)
        
        self.logger = logging.getLogger(__name__)
    
    def get_all_translations(self, request: TranslationRequest) -> List[TranslationResult]:
        """
        Get translations from all available services
        
        Args:
            request: TranslationRequest object
            
        Returns:
            List of TranslationResult objects
        """
        results = []
        
        # Get MT translations
        if self.enable_mt_matching:
            mt_results = self.get_mt_translations(request)
            results.extend(mt_results)
        
        # Get LLM translations
        if self.enable_llm_matching:
            llm_results = self.get_llm_translations(request)
            results.extend(llm_results)
        
        return results
    
    def get_mt_translations(self, request: TranslationRequest) -> List[TranslationResult]:
        """
        Get Machine Translation results
        
        Args:
            request: TranslationRequest object
            
        Returns:
            List of TranslationResult objects from MT services
        """
        results = []
        
        self.logger.info(f"🤖 DIRECT MT SEARCH: Getting machine translation for '{request.source_text[:50]}...'")
        
        # Google Translate
        if self.google_translate_enabled:
            try:
                from modules.llm_clients import get_google_translation
                mt_result = get_google_translation(
                    request.source_text,
                    request.source_lang_code or 'auto',
                    request.target_lang_code or 'en'
                )
                
                if mt_result and mt_result.get('translation'):
                    result = TranslationResult(
                        source=request.source_text,
                        target=mt_result['translation'],
                        relevance=85,  # Good relevance for MT
                        metadata={
                            'provider': 'Google Translate',
                            'confidence': mt_result.get('confidence', 'N/A'),
                            'detected_lang': mt_result.get('detected_source_language', request.source_lang_code)
                        },
                        match_type='MT',
                        provider_code='GT'
                    )
                    results.append(result)
                    self.logger.info(f"🤖 DIRECT MT SEARCH: Added Google Translate result")
                    
            except Exception as e:
                self.logger.error(f"Error in Google Translate: {e}")
        
        # DeepL (placeholder for future implementation)
        if self.deepl_enabled:
            try:
                # DeepL integration would go here
                pass
            except Exception as e:
                self.logger.error(f"Error in DeepL: {e}")
        
        return results
    
    def get_llm_translations(self, request: TranslationRequest) -> List[TranslationResult]:
        """
        Get Large Language Model translation results
        
        Args:
            request: TranslationRequest object
            
        Returns:
            List of TranslationResult objects from LLM services
        """
        results = []
        
        self.logger.info(f"🧠 DIRECT LLM SEARCH: Getting AI translation for '{request.source_text[:50]}...'")
        
        # OpenAI/ChatGPT
        if self.openai_enabled:
            try:
                from modules.llm_clients import get_openai_translation
                llm_result = get_openai_translation(
                    request.source_text,
                    request.source_lang or 'Dutch',
                    request.target_lang or 'English',
                    context=request.context or "Technical documentation translation"
                )
                
                if llm_result and llm_result.get('translation'):
                    # Clean the translation to remove provider prefix
                    clean_translation = self._clean_provider_prefix(
                        llm_result['translation'], 
                        ['[OpenAI]', '[openai]', 'OpenAI:', 'openai:']
                    )
                    
                    result = TranslationResult(
                        source=request.source_text,
                        target=clean_translation,
                        relevance=90,  # High relevance for LLM with context
                        metadata={
                            'provider': 'OpenAI GPT',
                            'model': llm_result.get('model', 'gpt-3.5-turbo'),
                            'context_aware': True,
                            'explanation': llm_result.get('explanation', '')
                        },
                        match_type='LLM',
                        provider_code='AI'
                    )
                    results.append(result)
                    self.logger.info(f"🧠 DIRECT LLM SEARCH: Added OpenAI result")
                    
            except Exception as e:
                self.logger.error(f"Error in OpenAI translation: {e}")
        
        # Claude
        if self.claude_enabled:
            try:
                from modules.llm_clients import get_claude_translation
                claude_result = get_claude_translation(
                    request.source_text,
                    request.source_lang or 'Dutch',
                    request.target_lang or 'English',
                    context=request.context or "Technical documentation translation"
                )
                
                if claude_result and claude_result.get('translation'):
                    # Clean the translation to remove provider prefix
                    clean_translation = self._clean_provider_prefix(
                        claude_result['translation'], 
                        ['[Claude]', '[claude]', 'Claude:', 'claude:']
                    )
                    
                    result = TranslationResult(
                        source=request.source_text,
                        target=clean_translation,
                        relevance=92,  # Very high relevance for Claude
                        metadata={
                            'provider': 'Anthropic Claude',
                            'model': claude_result.get('model', 'claude-3'),
                            'context_aware': True,
                            'reasoning': claude_result.get('reasoning', '')
                        },
                        match_type='LLM',
                        provider_code='CL'
                    )
                    results.append(result)
                    self.logger.info(f"🧠 DIRECT LLM SEARCH: Added Claude result")
                    
            except Exception as e:
                self.logger.error(f"Error in Claude translation: {e}")
        
        return results
    
    def _clean_provider_prefix(self, translation: str, prefixes: List[str]) -> str:
        """
        Remove provider prefixes from translation text
        
        Args:
            translation: Original translation text
            prefixes: List of prefixes to remove
            
        Returns:
            Cleaned translation text
        """
        if not translation:
            return translation
        
        cleaned = translation.strip()
        
        for prefix in prefixes:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
                break
        
        # Remove any remaining leading/trailing parentheses or brackets
        cleaned = cleaned.strip('()[]')
        
        # Remove common trailing patterns
        trailing_patterns = [
            f' (translated to {self.config.get("target_lang", "English")})',
            ' (translated)',
            ' - Translation',
            ' - translated'
        ]
        
        for pattern in trailing_patterns:
            if cleaned.lower().endswith(pattern.lower()):
                cleaned = cleaned[:-len(pattern)]
                break
        
        return cleaned.strip()


def create_translation_service(config: Dict[str, Any] = None) -> TranslationServices:
    """
    Factory function to create a TranslationServices instance
    
    Args:
        config: Configuration dictionary
        
    Returns:
        TranslationServices instance
    """
    return TranslationServices(config)