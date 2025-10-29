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
    
    def __init__(self, api_key: str, provider: str = "openai", model: Optional[str] = None):
        """
        Initialize LLM client
        
        Args:
            api_key: API key for the provider
            provider: "openai", "claude", or "gemini"
            model: Model name (uses default if None)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model or self.DEFAULT_MODELS.get(self.provider)
        
        if not self.model:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Auto-detect temperature based on model
        self.temperature = self._get_temperature()
    
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
        context: Optional[str] = None
    ) -> str:
        """
        Translate text using configured LLM
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            context: Optional context for translation
        
        Returns:
            Translated text
        """
        # Build prompt
        prompt = f"Translate the following text from {source_lang} to {target_lang}:\n\n{text}"
        
        if context:
            prompt = f"Context: {context}\n\n{prompt}"
        
        # Call appropriate provider
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "claude":
            return self._call_claude(prompt)
        elif self.provider == "gemini":
            return self._call_gemini(prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI library not installed. Install with: pip install openai"
            )
        
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature
        )
        
        return response.choices[0].message.content.strip()
    
    def _call_claude(self, prompt: str) -> str:
        """Call Anthropic Claude API"""
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Anthropic library not installed. Install with: pip install anthropic"
            )
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text.strip()
    
    def _call_gemini(self, prompt: str) -> str:
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
        return response.text.strip()


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
