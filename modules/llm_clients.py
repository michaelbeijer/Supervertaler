"""
LLM Clients Module for Supervertaler
=====================================

Specialized independent module for interacting with various LLM providers.
Can be used standalone or imported by other applications.

Supported Providers:
- OpenAI (GPT-4, GPT-4o, GPT-5, o1, o3)
- Anthropic (Claude 3.5 Sonnet, etc.)
- Google (Gemini 2.0 Flash, Pro)

Temperature Handling:
- Reasoning models (GPT-5, o1, o3): temperature=1.0
- Standard models: temperature=0.3

Usage:
    from modules.llm_clients import LLMClient
    
    client = LLMClient(api_key="your-key", provider="openai")
    response = client.translate("Hello world", source_lang="en", target_lang="nl")
"""

from typing import Dict, Optional, Literal
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Configuration for LLM client"""
    provider: Literal["openai", "claude", "gemini"]
    model: str
    api_key: str
    temperature: Optional[float] = None  # Auto-detected if None
    max_tokens: int = 4096


class LLMClient:
    """Universal LLM client for translation tasks"""
    
    # Default models for each provider
    DEFAULT_MODELS = {
        "openai": "gpt-4o",
        "claude": "claude-3-5-sonnet-20241022",
        "gemini": "gemini-2.0-flash-exp"
    }
    
    # Reasoning models that require temperature=1.0
    REASONING_MODELS = ["gpt-5", "o1", "o3"]
    
    def __init__(self, api_key: str, provider: str = "openai", model: Optional[str] = None, max_tokens: int = 4096):
        """
        Initialize LLM client
        
        Args:
            api_key: API key for the provider
            provider: "openai", "claude", or "gemini"
            model: Model name (uses default if None)
            max_tokens: Maximum tokens for responses (default: 4096)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model or self.DEFAULT_MODELS.get(self.provider)
        self.max_tokens = max_tokens
        
        if not self.model:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Auto-detect temperature based on model
        self.temperature = self._get_temperature()
    
    def _clean_translation_response(self, translation: str, prompt: str) -> str:
        """
        Clean translation response to remove any prompt remnants.
        
        Sometimes LLMs translate the entire prompt instead of just the source text.
        This method attempts to extract only the actual translation.
        
        Args:
            translation: Raw translation response from LLM
            prompt: Original prompt sent to LLM
        
        Returns:
            Cleaned translation text
        """
        if not translation:
            return translation
        
        # First, try to find the delimiter we added ("**YOUR TRANSLATION**")
        # Everything after this delimiter should be the actual translation
        delimiter_markers = [
            "**YOUR TRANSLATION (provide ONLY the translated text, no numbering or labels):**",
            "**YOUR TRANSLATION**",
            "**YOUR TRANSLATION (provide ONLY",
            "**JOUW VERTALING**",
            "**TRANSLATION**",
            "**VERTALING**",
            "Translation:",
            "Vertaling:",
            "YOUR TRANSLATION",
            "JOUW VERTALING",
        ]
        
        # Try to split on delimiter first (most reliable)
        import re
        for marker in delimiter_markers:
            # Use word boundary or newline before marker for better matching
            pattern = re.escape(marker)
            # Try with newline before it
            pattern_with_newline = r'\n\s*' + pattern
            match = re.search(pattern_with_newline, translation, re.IGNORECASE | re.MULTILINE)
            if not match:
                # Try without newline requirement
                match = re.search(pattern, translation, re.IGNORECASE)
            
            if match:
                result = translation[match.end():].strip()
                # Clean up any leading/trailing newlines, colons, or whitespace
                result = re.sub(r'^[::\s\n\r]+', '', result)
                result = result.strip()
                if result:
                    # Additional cleanup: remove any remaining prompt patterns
                    result = self._remove_prompt_patterns(result)
                    if result and len(result) < len(translation) * 0.9:  # Must be significantly shorter
                        return result
        
        # Common patterns that indicate the prompt was translated
        # These are translations of common prompt phrases
        prompt_patterns = [
            # Dutch translations of prompt instructions
            "Als een professionele",
            "Als professionele",
            "U bent een expert",
            "Uw taak is om",
            "Tijdens het vertaalproces",
            "De output moet uitsluitend bestaan",
            "Waarschuwingsinformatie:",
            "⚠️ PROFESSIONELE VERTAALCONTEXT:",
            "vertaler",
            "handleidingen",
            "regelgeving",
            "naleving",
            "medische apparaten",
            "professionele doeleinden",
            "medisch advies",
            "volledige documentcontext",
            "tekstsegmenten",
            "CAT-tool tags",
            "memoQ-tags",
            "Trados Studio-tags",
            "CafeTran-tags",
            # English patterns (in case language is mixed)
            "As a professional",
            "You are an expert",
            "Your task is to",
            "During the translation process",
            "The output must consist exclusively",
            "⚠️ PROFESSIONAL TRANSLATION CONTEXT:",
            "professional translation",
            "technical manuals",
            "regulatory compliance",
            "medical devices",
            "professional purposes",
            "medical advice",
            "full document context",
            "text segments",
            "CAT tool tags",
            "memoQ tags",
            "Trados Studio tags",
            "CafeTran tags",
        ]
        
        # Check if translation contains prompt patterns - if so, it's likely a translated prompt
        translation_lower = translation.lower()
        prompt_pattern_count = sum(1 for pattern in prompt_patterns if pattern.lower() in translation_lower)
        
        # If translation is suspiciously long and contains many prompt patterns, it's likely a translated prompt
        if len(translation) > 300 and prompt_pattern_count >= 3:
            # Try to find where actual translation starts
            # Look for the end of the last prompt-like sentence
            lines = translation.split('\n')
            cleaned_lines = []
            found_actual_translation = False
            
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                if not line_stripped:
                    if found_actual_translation:
                        cleaned_lines.append(line)
                    continue
                
                # Check if this line looks like prompt instruction
                is_prompt = any(pattern.lower() in line_stripped.lower() for pattern in prompt_patterns)
                
                # Also check if it's a very long line (likely prompt instructions)
                if len(line_stripped) > 200:
                    prompt_phrases = sum(1 for pattern in prompt_patterns if pattern.lower() in line_stripped.lower())
                    if prompt_phrases >= 2:
                        is_prompt = True
                
                if is_prompt:
                    # Skip prompt lines
                    continue
                else:
                    # This might be actual translation
                    found_actual_translation = True
                    cleaned_lines.append(line)
            
            result = '\n'.join(cleaned_lines).strip()
            if result and len(result) < len(translation) * 0.7:  # Significantly shorter = likely cleaned correctly
                return self._remove_prompt_patterns(result)
        
        # Final cleanup: remove any remaining prompt patterns
        cleaned = self._remove_prompt_patterns(translation)
        
        # If cleaned version is much shorter, it was likely cleaned correctly
        if cleaned != translation and len(cleaned) < len(translation) * 0.8:
            return cleaned
        
        return translation
    
    def _remove_prompt_patterns(self, text: str) -> str:
        """Remove prompt-like patterns from text"""
        prompt_patterns = [
            "Als een professionele", "Als professionele", "U bent een expert",
            "Uw taak is om", "Tijdens het vertaalproces", "De output moet",
            "Waarschuwingsinformatie:", "⚠️ PROFESSIONELE", "vertaler",
            "handleidingen", "regelgeving", "naleving", "medische apparaten",
            "professionele doeleinden", "medisch advies", "volledige documentcontext",
            "tekstsegmenten", "CAT-tool tags", "memoQ-tags", "Trados Studio-tags",
            "CafeTran-tags", "As a professional", "You are an expert",
            "Your task is to", "During the translation process",
            "The output must consist exclusively", "⚠️ PROFESSIONAL",
            "professional translation", "technical manuals", "regulatory compliance",
            "medical devices", "professional purposes", "medical advice",
            "full document context", "text segments", "CAT tool tags",
            "memoQ tags", "Trados Studio tags", "CafeTran tags",
        ]
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line_lower = line.lower()
            # Skip lines that contain prompt patterns
            has_prompt = any(pattern.lower() in line_lower for pattern in prompt_patterns)
            # Also skip very long lines that might be prompt instructions
            if not has_prompt and (len(line.strip()) < 300 or len(line.strip().split()) < 50):
                cleaned_lines.append(line)
        
        result = '\n'.join(cleaned_lines).strip()
        return result if result else text
    
    def _get_temperature(self) -> float:
        """Determine optimal temperature for model"""
        model_lower = self.model.lower()
        
        # Reasoning models require temperature=1.0
        if any(reasoning in model_lower for reasoning in self.REASONING_MODELS):
            return 1.0
        
        # Standard models use 0.3 for consistency
        return 0.3
    
    def translate(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "nl",
        context: Optional[str] = None,
        custom_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Translate text using configured LLM
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            context: Optional context for translation
            custom_prompt: Optional custom prompt (overrides default simple prompt)
        
        Returns:
            Translated text
        """
        # Use custom prompt if provided, otherwise build simple prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            # Build prompt
            prompt = f"Translate the following text from {source_lang} to {target_lang}:\n\n{text}"
            
            if context:
                prompt = f"Context: {context}\n\n{prompt}"
        
        # Call appropriate provider
        if self.provider == "openai":
            return self._call_openai(prompt, max_tokens=max_tokens)
        elif self.provider == "claude":
            return self._call_claude(prompt, max_tokens=max_tokens)
        elif self.provider == "gemini":
            return self._call_gemini(prompt, max_tokens=max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _call_openai(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Call OpenAI API"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI library not installed. Install with: pip install openai"
            )
        
        client = OpenAI(api_key=self.api_key, timeout=120.0)  # 2 minute timeout
        
        # Use provided max_tokens or default
        tokens_to_use = max_tokens if max_tokens is not None else self.max_tokens
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=tokens_to_use,
            timeout=120.0  # Explicit timeout
        )
        
        translation = response.choices[0].message.content.strip()
        
        # Clean up translation: remove any prompt remnants
        translation = self._clean_translation_response(translation, prompt)
        
        return translation
    
    def _call_claude(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Call Anthropic Claude API"""
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Anthropic library not installed. Install with: pip install anthropic"
            )
        
        client = anthropic.Anthropic(api_key=self.api_key, timeout=120.0)  # 2 minute timeout
        
        # Use provided max_tokens or default (Claude uses 4096 as default)
        tokens_to_use = max_tokens if max_tokens is not None else self.max_tokens
        
        response = client.messages.create(
            model=self.model,
            max_tokens=tokens_to_use,
            messages=[{"role": "user", "content": prompt}],
            timeout=120.0  # Explicit timeout
        )
        
        translation = response.content[0].text.strip()
        
        # Clean up translation: remove any prompt remnants
        translation = self._clean_translation_response(translation, prompt)
        
        return translation
    
    def _call_gemini(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Call Google Gemini API"""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError(
                "Google AI library not installed. Install with: pip install google-generativeai"
            )
        
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)
        
        response = model.generate_content(prompt)
        translation = response.text.strip()
        
        # Clean up translation: remove any prompt remnants
        translation = self._clean_translation_response(translation, prompt)
        
        return translation


# ============================================================================
# STANDALONE USAGE
# ============================================================================

def main():
    """Example standalone usage of LLM client"""
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python llm_clients.py <provider> <api_key> <text_to_translate>")
        print("Example: python llm_clients.py openai sk-... 'Hello world'")
        sys.exit(1)
    
    provider = sys.argv[1]
    api_key = sys.argv[2]
    text = sys.argv[3]
    
    # Create client
    client = LLMClient(api_key=api_key, provider=provider)
    
    # Translate
    print(f"Translating with {provider} ({client.model})...")
    result = client.translate(text, source_lang="en", target_lang="nl")
    
    print(f"\nOriginal: {text}")
    print(f"Translation: {result}")


if __name__ == "__main__":
    main()
