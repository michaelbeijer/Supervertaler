"""
LLM Clients Module for Supervertaler
=====================================

Specialized independent module for interacting with various LLM providers.
Can be used standalone or imported by other applications.

Supported Providers:
- OpenAI (GPT-4, GPT-4o, GPT-5, o1, o3)
- Anthropic (Claude Sonnet 4.5, Haiku 4.5, Opus 4.1)
- Google (Gemini 2.5 Flash, 2.5 Pro, 3 Pro Preview)

Claude 4 Models (Released 2025):
- Sonnet 4.5: Best balance - flagship model for general translation ($3/$15 per MTok)
- Haiku 4.5: Fast & affordable - 2x speed, 1/3 cost of Sonnet ($1/$5 per MTok)
- Opus 4.1: Premium quality - complex legal/technical translation ($15/$75 per MTok)

Temperature Handling:
- Reasoning models (GPT-5, o1, o3): temperature parameter OMITTED (not supported)
- Standard models: temperature=0.3

Usage:
    from modules.llm_clients import LLMClient

    # Use default (Sonnet 4.5)
    client = LLMClient(api_key="your-key", provider="claude")

    # Or specify model
    client = LLMClient(api_key="your-key", provider="claude", model="claude-haiku-4-5-20251001")

    response = client.translate("Hello world", source_lang="en", target_lang="nl")
"""

import os
from typing import Dict, Optional, Literal, List
from dataclasses import dataclass


def load_api_keys() -> Dict[str, str]:
    """Load API keys from api_keys.txt file (supports both root and user_data_private locations)"""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Try user_data_private first (dev mode), then fallback to root
    possible_paths = [
        os.path.join(script_dir, "user_data_private", "api_keys.txt"),
        os.path.join(script_dir, "api_keys.txt")
    ]

    api_keys_file = None
    for path in possible_paths:
        if os.path.exists(path):
            api_keys_file = path
            break

    # If no file exists, create example file from template
    if api_keys_file is None:
        api_keys_file = possible_paths[1]  # Default to root
        example_file = os.path.join(script_dir, "api_keys.example.txt")

        # Create api_keys.txt from example if it exists
        if os.path.exists(example_file) and not os.path.exists(api_keys_file):
            try:
                import shutil
                shutil.copy(example_file, api_keys_file)
                print(f"Created {api_keys_file} from example template.")
                print("Please edit this file and add your API keys.")
            except Exception as e:
                print(f"Could not create api_keys.txt: {e}")

    api_keys = {
        "google": "",           # For Gemini (primary key name)
        "gemini": "",           # For Gemini (alias - synced with 'google')
        "google_translate": "", # For Google Cloud Translation API
        "claude": "",
        "openai": "",
        "deepl": "",
        "mymemory": "",
        "ollama_endpoint": "http://localhost:11434"  # Local LLM endpoint (no key needed)
    }

    if os.path.exists(api_keys_file):
        try:
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in api_keys:
                            api_keys[key] = value
                        # Also check for ollama_endpoint
                        elif key == 'ollama_endpoint' and value:
                            api_keys['ollama_endpoint'] = value
        except Exception as e:
            print(f"Error loading API keys: {e}")
    
    # Sync 'google' and 'gemini' keys (they're aliases for the same API)
    # If one is set and the other isn't, copy the value
    if api_keys.get('google') and not api_keys.get('gemini'):
        api_keys['gemini'] = api_keys['google']
    elif api_keys.get('gemini') and not api_keys.get('google'):
        api_keys['google'] = api_keys['gemini']
    
    # Set environment variable for Ollama endpoint if configured
    if api_keys.get('ollama_endpoint'):
        os.environ['OLLAMA_ENDPOINT'] = api_keys['ollama_endpoint']

    return api_keys


@dataclass
class LLMConfig:
    """Configuration for LLM client"""
    provider: Literal["openai", "claude", "gemini"]
    model: str
    api_key: str
    temperature: Optional[float] = None  # Auto-detected if None
    max_tokens: int = 16384  # Increased from 4096 for batch translation (100 segments needs ~16K tokens)


class LLMClient:
    """Universal LLM client for translation tasks"""

    # Default models for each provider
    DEFAULT_MODELS = {
        "openai": "gpt-4o",
        "claude": "claude-sonnet-4-5-20250929",  # Claude Sonnet 4.5 (Sept 2025)
        "gemini": "gemini-2.5-flash",  # Gemini 2.5 Flash (2025)
        "ollama": "qwen2.5:7b"  # Local LLM via Ollama - excellent multilingual quality
    }
    
    # Available Ollama models with descriptions (for UI display)
    OLLAMA_MODELS = {
        "qwen2.5:3b": {
            "name": "Qwen 2.5 3B",
            "description": "Fast & lightweight - good for simple translations",
            "size_gb": 2.0,
            "ram_required": 4,
            "quality_stars": 3,
            "strengths": ["Fast", "Low memory", "Multilingual"],
            "use_case": "Quick drafts, simple text, low-end hardware"
        },
        "qwen2.5:7b": {
            "name": "Qwen 2.5 7B",
            "description": "Recommended - excellent multilingual quality",
            "size_gb": 4.4,
            "ram_required": 8,
            "quality_stars": 4,
            "strengths": ["Excellent multilingual", "Good quality", "Balanced speed"],
            "use_case": "General translation, most European languages"
        },
        "llama3.2:3b": {
            "name": "Llama 3.2 3B",
            "description": "Meta's efficient model - good English",
            "size_gb": 2.0,
            "ram_required": 4,
            "quality_stars": 3,
            "strengths": ["Fast", "Good English", "Efficient"],
            "use_case": "English-centric translations, quick drafts"
        },
        "mistral:7b": {
            "name": "Mistral 7B",
            "description": "Strong European language support",
            "size_gb": 4.1,
            "ram_required": 8,
            "quality_stars": 4,
            "strengths": ["European languages", "French", "Fast inference"],
            "use_case": "French, German, Spanish translations"
        },
        "gemma2:9b": {
            "name": "Gemma 2 9B",
            "description": "Google's quality model - best for size",
            "size_gb": 5.5,
            "ram_required": 10,
            "quality_stars": 5,
            "strengths": ["High quality", "Good reasoning", "Multilingual"],
            "use_case": "Quality-focused translation, technical content"
        },
        "qwen2.5:14b": {
            "name": "Qwen 2.5 14B",
            "description": "Premium quality - needs 16GB+ RAM",
            "size_gb": 9.0,
            "ram_required": 16,
            "quality_stars": 5,
            "strengths": ["Excellent quality", "Complex text", "Nuanced translation"],
            "use_case": "Premium translations, complex documents, high-end hardware"
        },
        "llama3.1:8b": {
            "name": "Llama 3.1 8B",
            "description": "Meta's capable model - good all-rounder",
            "size_gb": 4.7,
            "ram_required": 8,
            "quality_stars": 4,
            "strengths": ["Versatile", "Good quality", "Well-tested"],
            "use_case": "General purpose translation"
        }
    }
    
    # Vision-capable models (support image inputs)
    VISION_MODELS = {
        "openai": [
            "gpt-4-vision-preview",
            "gpt-4-turbo",
            "gpt-4-turbo-2024-04-09",
            "gpt-4o",
            "gpt-4o-mini",
            "chatgpt-4o-latest"
        ],
        "claude": [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "claude-sonnet-4-5-20250929",
            "claude-haiku-4-5-20251001",
            "claude-opus-4-1-20250805"
        ],
        "gemini": [
            "gemini-pro-vision",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-2.0-flash",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-2.5-pro",
            "gemini-3-pro-preview"
        ]
    }

    # Available Claude 4 models with descriptions
    CLAUDE_MODELS = {
        "claude-sonnet-4-5-20250929": {
            "name": "Claude Sonnet 4.5",
            "description": "Best balance - Flagship model for general translation",
            "released": "2025-09-29",
            "strengths": ["General translation", "Multilingual", "Fast", "Cost-effective"],
            "pricing": {"input": 3, "output": 15},  # USD per million tokens
            "use_case": "Recommended for most translation tasks"
        },
        "claude-haiku-4-5-20251001": {
            "name": "Claude Haiku 4.5",
            "description": "Fast & affordable - 2x speed, 1/3 cost of Sonnet",
            "released": "2025-10-01",
            "strengths": ["High-volume translation", "Speed", "Budget-friendly", "Batch processing"],
            "pricing": {"input": 1, "output": 5},
            "use_case": "Best for large translation projects where speed and cost matter"
        },
        "claude-opus-4-1-20250805": {
            "name": "Claude Opus 4.1",
            "description": "Premium quality - Complex reasoning for nuanced translation",
            "released": "2025-08-05",
            "strengths": ["Legal translation", "Technical documents", "Complex reasoning", "Highest accuracy"],
            "pricing": {"input": 15, "output": 75},
            "use_case": "Best for specialized legal/technical translation requiring deep reasoning"
        }
    }

    # Reasoning models that don't support temperature parameter (must be omitted)
    REASONING_MODELS = ["gpt-5", "o1", "o3"]

    @classmethod
    def get_claude_model_info(cls, model_id: Optional[str] = None) -> Dict:
        """
        Get information about available Claude models

        Args:
            model_id: Specific model ID to get info for, or None for all models

        Returns:
            Dict with model information

        Example:
            # Get all models
            models = LLMClient.get_claude_model_info()
            for model_id, info in models.items():
                print(f"{info['name']}: {info['description']}")

            # Get specific model
            info = LLMClient.get_claude_model_info("claude-sonnet-4-5-20250929")
            print(info['use_case'])
        """
        if model_id:
            return cls.CLAUDE_MODELS.get(model_id, {})
        return cls.CLAUDE_MODELS
    
    @classmethod
    def get_ollama_model_info(cls, model_id: Optional[str] = None) -> Dict:
        """
        Get information about available Ollama models
        
        Args:
            model_id: Specific model ID to get info for, or None for all models
            
        Returns:
            Dict with model information
        """
        if model_id:
            return cls.OLLAMA_MODELS.get(model_id, {})
        return cls.OLLAMA_MODELS
    
    @classmethod
    def check_ollama_status(cls, endpoint: str = None) -> Dict:
        """
        Check if Ollama is running and get available models
        
        Args:
            endpoint: Ollama API endpoint (default: http://localhost:11434)
            
        Returns:
            Dict with:
                - running: bool - whether Ollama is running
                - models: list - available model names
                - error: str - error message if not running
        """
        import requests
        
        endpoint = endpoint or os.environ.get('OLLAMA_ENDPOINT', 'http://localhost:11434')
        
        try:
            # Check if Ollama is running
            response = requests.get(f"{endpoint}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [m['name'] for m in data.get('models', [])]
                return {
                    'running': True,
                    'models': models,
                    'endpoint': endpoint,
                    'error': None
                }
            else:
                return {
                    'running': False,
                    'models': [],
                    'endpoint': endpoint,
                    'error': f"Ollama returned status {response.status_code}"
                }
        except requests.exceptions.ConnectionError:
            return {
                'running': False,
                'models': [],
                'endpoint': endpoint,
                'error': "Cannot connect to Ollama. Please ensure Ollama is installed and running."
            }
        except Exception as e:
            return {
                'running': False,
                'models': [],
                'endpoint': endpoint,
                'error': str(e)
            }
    
    @classmethod
    def model_supports_vision(cls, provider: str, model_name: str) -> bool:
        """
        Check if a model supports vision (image) inputs
        
        Args:
            provider: Provider name ("openai", "claude", "gemini")
            model_name: Model identifier
            
        Returns:
            True if model supports vision, False otherwise
        """
        provider = provider.lower()
        vision_models = cls.VISION_MODELS.get(provider, [])
        return model_name in vision_models

    def __init__(self, api_key: str = None, provider: str = "openai", model: Optional[str] = None, max_tokens: int = 16384):
        """
        Initialize LLM client
        
        Args:
            api_key: API key for the provider (not required for 'ollama')
            provider: "openai", "claude", "gemini", or "ollama"
            model: Model name (uses default if None)
            max_tokens: Maximum tokens for responses (default: 16384)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model or self.DEFAULT_MODELS.get(self.provider)
        self.max_tokens = max_tokens
        
        if not self.model:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Validate API key for cloud providers (not needed for Ollama)
        if self.provider != "ollama" and not self.api_key:
            raise ValueError(f"API key required for provider: {provider}")
        
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
    
    def _get_temperature(self) -> Optional[float]:
        """Determine optimal temperature for model (None means omit parameter)"""
        model_lower = self.model.lower()
        
        # Reasoning models don't support temperature parameter - return None to omit it
        if any(reasoning in model_lower for reasoning in self.REASONING_MODELS):
            return None
        
        # Standard models use 0.3 for consistency
        return 0.3
    
    def translate(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "nl",
        context: Optional[str] = None,
        custom_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        images: Optional[List] = None
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
        
        # Log warning if images provided but model doesn't support vision
        if images and not self.model_supports_vision(self.provider, self.model):
            print(f"⚠️ Warning: Model {self.model} doesn't support vision. Images will be ignored.")
            images = None  # Don't pass to API
        
        # Call appropriate provider
        if self.provider == "openai":
            return self._call_openai(prompt, max_tokens=max_tokens, images=images)
        elif self.provider == "claude":
            return self._call_claude(prompt, max_tokens=max_tokens, images=images)
        elif self.provider == "gemini":
            return self._call_gemini(prompt, max_tokens=max_tokens, images=images)
        elif self.provider == "ollama":
            return self._call_ollama(prompt, max_tokens=max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _call_openai(self, prompt: str, max_tokens: Optional[int] = None, images: Optional[List] = None) -> str:
        """Call OpenAI API with GPT-5/o1/o3 reasoning model support and vision capability"""
        print(f"🔵 _call_openai START: model={self.model}, prompt_len={len(prompt)}, max_tokens={max_tokens}, images={len(images) if images else 0}")

        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI library not installed. Install with: pip install openai"
            )

        # Detect if this is a reasoning model (GPT-5, o1, o3)
        model_lower = self.model.lower()
        is_reasoning_model = any(x in model_lower for x in ["gpt-5", "o1", "o3"])

        # Reasoning models need MUCH longer timeout (they can take 5-10 minutes for large prompts)
        timeout_seconds = 600.0 if is_reasoning_model else 120.0  # 10 min vs 2 min
        client = OpenAI(api_key=self.api_key, timeout=timeout_seconds)
        print(f"🔵 OpenAI client created successfully (timeout: {timeout_seconds}s)")

        # Use provided max_tokens or default
        # IMPORTANT: Reasoning models need MUCH higher limits because they use tokens for:
        # 1. Internal reasoning/thinking (can be thousands of tokens)
        # 2. The actual response content
        # If limit is too low, all tokens get used for reasoning and response is empty!
        if max_tokens is not None:
            tokens_to_use = max_tokens
        elif is_reasoning_model:
            # For reasoning models, use 32K tokens (GPT-5 supports up to 65K)
            # This gives plenty of room for both reasoning and response
            tokens_to_use = 32768
        else:
            tokens_to_use = self.max_tokens

        print(f"🔵 Is reasoning model: {is_reasoning_model}, tokens_to_use: {tokens_to_use}")

        # Build message content (text + optional images)
        if images:
            # Vision API format: content as array with text and image_url objects
            content = [{"type": "text", "text": prompt}]
            for img_ref, img_base64 in images:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_base64}"}
                })
            print(f"🔵 Vision mode: {len(images)} images added to message")
        else:
            # Standard text-only format
            content = prompt

        # Build API call parameters
        api_params = {
            "model": self.model,
            "messages": [{"role": "user", "content": content}],
            "timeout": timeout_seconds
        }

        if is_reasoning_model:
            # Reasoning models (gpt-5, o1, o3-mini) require specific parameters
            # - Use max_completion_tokens instead of max_tokens
            # - DO NOT include temperature parameter (it's not supported)
            api_params["max_completion_tokens"] = tokens_to_use
            # Note: Temperature parameter is OMITTED for reasoning models (not supported)
            # Note: reasoning_effort is also OMITTED - without it, GPT-5 is much faster
            print(f"🔵 Reasoning model params: max_completion_tokens={tokens_to_use}, no reasoning_effort (faster)")
        else:
            # Standard models (gpt-4o, gpt-4-turbo, etc.)
            api_params["max_tokens"] = tokens_to_use
            api_params["temperature"] = self.temperature
            print(f"🔵 Standard model params: max_tokens={tokens_to_use}, temperature={self.temperature}")

        try:
            print(f"🔵 Calling OpenAI API...")
            response = client.chat.completions.create(**api_params)
            print(f"🔵 OpenAI API call completed")

            # Check if response has content
            if not response.choices or not response.choices[0].message.content:
                error_msg = f"OpenAI returned empty response for model {self.model}"
                print(f"❌ ERROR: {error_msg}")
                raise ValueError(error_msg)

            translation = response.choices[0].message.content.strip()

            # Check if translation is empty after stripping
            if not translation:
                error_msg = f"OpenAI returned empty translation after stripping for model {self.model}"
                print(f"❌ ERROR: {error_msg}")
                print(f"Raw response: {response.choices[0].message.content}")
                raise ValueError(error_msg)

            # Clean up translation: remove any prompt remnants
            translation = self._clean_translation_response(translation, prompt)

            return translation

        except Exception as e:
            # Log the actual error with context
            print(f"❌ OpenAI API Error (model: {self.model})")
            print(f"   Error type: {type(e).__name__}")
            print(f"   Error message: {str(e)}")
            print(f"   Prompt length: {len(prompt)} characters")
            if hasattr(e, 'response'):
                print(f"   Response: {e.response}")
            raise  # Re-raise to be caught by calling code
    
    def _call_claude(self, prompt: str, max_tokens: Optional[int] = None, images: Optional[List] = None) -> str:
        """Call Anthropic Claude API with vision support"""
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Anthropic library not installed. Install with: pip install anthropic"
            )
        
        # Use longer timeout for batch operations (detected by large prompts)
        # Opus 4.1 can take longer to process, especially with extended context
        prompt_length = len(prompt)
        if prompt_length > 50000:  # Large batch prompt
            timeout_seconds = 300.0  # 5 minutes for very large prompts
        elif prompt_length > 20000:  # Medium batch prompt
            timeout_seconds = 180.0  # 3 minutes
        else:
            timeout_seconds = 120.0  # 2 minutes for normal operations
        
        client = anthropic.Anthropic(api_key=self.api_key, timeout=timeout_seconds)
        
        # Use provided max_tokens or default (Claude uses 4096 as default)
        tokens_to_use = max_tokens if max_tokens is not None else self.max_tokens
        
        # Build message content (text + optional images)
        if images:
            # Claude vision format: content as array with text and image objects
            content = []
            for img_ref, img_base64 in images:
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_base64
                    }
                })
            # Add text after images
            content.append({"type": "text", "text": prompt})
            print(f"🟣 Claude vision mode: {len(images)} images added to message")
        else:
            # Standard text-only format
            content = prompt
        
        response = client.messages.create(
            model=self.model,
            max_tokens=tokens_to_use,
            messages=[{"role": "user", "content": content}],
            timeout=timeout_seconds  # Explicit timeout
        )
        
        translation = response.content[0].text.strip()
        
        # Clean up translation: remove any prompt remnants
        translation = self._clean_translation_response(translation, prompt)
        
        return translation
    
    def _call_gemini(self, prompt: str, max_tokens: Optional[int] = None, images: Optional[List] = None) -> str:
        """Call Google Gemini API with vision support"""
        try:
            import google.generativeai as genai
            from PIL import Image
        except ImportError:
            raise ImportError(
                "Google AI library not installed. Install with: pip install google-generativeai pillow"
            )
        
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)
        
        # Build content (text + optional images)
        if images:
            # Gemini format: list with prompt text followed by PIL Image objects
            content = [prompt]
            for img_ref, pil_image in images:
                content.append(pil_image)  # Gemini accepts PIL.Image directly
            print(f"🟢 Gemini vision mode: {len(images)} images added to message")
        else:
            # Standard text-only
            content = prompt
        
        response = model.generate_content(content)
        translation = response.text.strip()
        
        # Clean up translation: remove any prompt remnants
        translation = self._clean_translation_response(translation, prompt)
        
        return translation
    
    def _call_ollama(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Call local Ollama server for translation.
        
        Ollama provides a simple REST API compatible with local LLM inference.
        Models run entirely on the user's computer - no API keys, no internet required.
        
        Args:
            prompt: The full prompt to send
            max_tokens: Maximum tokens to generate (default: 4096)
            
        Returns:
            Translated text
            
        Raises:
            ConnectionError: If Ollama is not running
            ValueError: If model is not available
        """
        try:
            import requests
        except ImportError:
            raise ImportError(
                "Requests library not installed. Install with: pip install requests"
            )
        
        # Get Ollama endpoint from environment or use default
        endpoint = os.environ.get('OLLAMA_ENDPOINT', 'http://localhost:11434')
        
        # Use provided max_tokens or default
        tokens_to_use = max_tokens if max_tokens is not None else min(self.max_tokens, 8192)
        
        print(f"🟠 _call_ollama START: model={self.model}, prompt_len={len(prompt)}, max_tokens={tokens_to_use}")
        print(f"🟠 Ollama endpoint: {endpoint}")
        
        # Build request payload
        # Using /api/chat for chat-style interaction (better for translation prompts)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,  # Get complete response at once
            "options": {
                "temperature": 0.3,  # Low temperature for consistent translations
                "num_predict": tokens_to_use,
                "top_p": 0.9,
                "repeat_penalty": 1.1
            }
        }
        
        try:
            # Make API call with generous timeout (local models can be slow, especially first load)
            # First call loads model into memory which can take 30-60 seconds
            # Large models (14B+) on CPU can take 2-5 minutes per translation
            print(f"🟠 Calling Ollama API...")
            
            # Determine timeout based on model size
            model_lower = self.model.lower()
            if '14b' in model_lower or '13b' in model_lower or '20b' in model_lower:
                timeout_seconds = 600  # 10 minutes for large models on CPU
            elif '7b' in model_lower or '8b' in model_lower or '9b' in model_lower:
                timeout_seconds = 300  # 5 minutes for medium models
            else:
                timeout_seconds = 180  # 3 minutes for small models
            
            response = requests.post(
                f"{endpoint}/api/chat",
                json=payload,
                timeout=timeout_seconds
            )
            
            if response.status_code == 404:
                raise ValueError(
                    f"Model '{self.model}' not found in Ollama. "
                    f"Please download it first with: ollama pull {self.model}"
                )
            
            response.raise_for_status()
            
            result = response.json()
            print(f"🟠 Ollama API call completed")
            
            # Extract translation from response
            if 'message' in result and 'content' in result['message']:
                translation = result['message']['content'].strip()
            else:
                raise ValueError(f"Unexpected Ollama response format: {result}")
            
            # Log some stats if available
            if 'eval_count' in result:
                print(f"🟠 Ollama stats: {result.get('eval_count', 0)} tokens generated")
            
            # Clean up translation: remove any prompt remnants
            translation = self._clean_translation_response(translation, prompt)
            
            return translation
            
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {endpoint}. "
                "Please ensure Ollama is installed and running.\n\n"
                "To start Ollama:\n"
                "  1. Install from https://ollama.com\n"
                "  2. Run 'ollama serve' in a terminal\n"
                "  3. Try again"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(
                f"Ollama request timed out after {timeout_seconds} seconds.\n\n"
                "This usually means:\n"
                "  1. System is low on RAM (check Task Manager)\n"
                "  2. Model is too large for your hardware\n"
                "  3. First-time model loading takes longer\n\n"
                "Solutions:\n"
                "  • Close other applications to free RAM\n"
                "  • Use a smaller model: 'qwen2.5:7b' or 'qwen2.5:3b'\n"
                "  • Try again (subsequent runs are faster)"
            )
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama API error: {str(e)}")


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


# Wrapper functions for easy integration with Supervertaler
def get_openai_translation(text: str, source_lang: str, target_lang: str, context: str = "") -> Dict:
    """
    Get OpenAI translation with metadata
    
    Args:
        text: Text to translate
        source_lang: Source language name
        target_lang: Target language name
        context: Optional context for better translation
    
    Returns:
        Dict with translation, model, and metadata
    """
    try:
        print(f"🔍 [DEBUG] OpenAI: Starting translation for '{text[:30]}...'")
        
        # Load API key from config
        api_key = _load_api_key('openai')
        print(f"🔍 [DEBUG] OpenAI: API key loaded: {'Yes' if api_key else 'No'}")
        if not api_key:
            raise ValueError("OpenAI API key not found in api_keys.txt")
            
        # Create LLM client and get real translation
        print(f"🔍 [DEBUG] OpenAI: Creating LLMClient...")
        client = LLMClient(api_key=api_key, provider="openai")
        print(f"🔍 [DEBUG] OpenAI: Client created, calling translate...")
        
        translation = client.translate(
            text=text,
            source_lang=_convert_lang_name_to_code(source_lang),
            target_lang=_convert_lang_name_to_code(target_lang),
            context=context if context else None
        )
        
        print(f"🔍 [DEBUG] OpenAI: Translation received: '{translation[:30]}...'")
        return {
            'translation': translation,
            'model': client.model,
            'explanation': f"Translation provided with context: {context[:50]}..." if context else "Translation completed",
            'success': True
        }
    except Exception as e:
        print(f"🔍 [DEBUG] OpenAI: ERROR - {str(e)}")
        return {
            'translation': None,
            'error': str(e),
            'success': False
        }


def get_claude_translation(text: str, source_lang: str, target_lang: str, context: str = "") -> Dict:
    """
    Get Claude translation with metadata
    
    Args:
        text: Text to translate
        source_lang: Source language name
        target_lang: Target language name
        context: Optional context for better translation
    
    Returns:
        Dict with translation, model, and metadata
    """
    try:
        print(f"🔍 [DEBUG] Claude: Starting translation for '{text[:30]}...'")
        
        # Load API key from config
        api_key = _load_api_key('claude')
        print(f"🔍 [DEBUG] Claude: API key loaded: {'Yes' if api_key else 'No'}")
        if not api_key:
            raise ValueError("Claude API key not found in api_keys.txt")
            
        # Create LLM client and get real translation
        print(f"🔍 [DEBUG] Claude: Creating LLMClient...")
        client = LLMClient(api_key=api_key, provider="claude")
        print(f"🔍 [DEBUG] Claude: Client created, calling translate...")
        
        translation = client.translate(
            text=text,
            source_lang=_convert_lang_name_to_code(source_lang),
            target_lang=_convert_lang_name_to_code(target_lang),
            context=context if context else None
        )
        
        print(f"🔍 [DEBUG] Claude: Translation received: '{translation[:30]}...'")
        return {
            'translation': translation,
            'model': client.model,
            'reasoning': f"High-quality translation considering context: {context[:50]}..." if context else "Translation completed",
            'success': True
        }
    except Exception as e:
        print(f"🔍 [DEBUG] Claude: ERROR - {str(e)}")
        return {
            'translation': None,
            'error': str(e),
            'success': False
        }


def _load_api_key(provider: str) -> str:
    """Load API key from api_keys.txt file"""
    try:
        import os
        api_keys_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api_keys.txt')
        
        if not os.path.exists(api_keys_path):
            return None
            
        with open(api_keys_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key_name, key_value = line.split('=', 1)
                    if key_name.strip().lower() == provider.lower():
                        return key_value.strip()
        return None
    except Exception:
        return None

def _convert_lang_name_to_code(lang_name: str) -> str:
    """Convert language names to codes for LLM API"""
    lang_map = {
        'Dutch': 'nl',
        'English': 'en', 
        'German': 'de',
        'French': 'fr',
        'Spanish': 'es',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Chinese': 'zh',
        'Japanese': 'ja',
        'Korean': 'ko'
    }
    return lang_map.get(lang_name, lang_name.lower()[:2])

def get_google_translation(text: str, source_lang: str, target_lang: str) -> Dict:
    """
    Get Google Cloud Translation API translation with metadata
    
    Args:
        text: Text to translate
        source_lang: Source language code (e.g., 'en', 'nl', 'auto')
        target_lang: Target language code (e.g., 'en', 'nl')
    
    Returns:
        Dict with translation, confidence, and metadata
    """
    try:
        # Load API key from api_keys.txt
        api_keys = load_api_keys()
        # Try both 'google_translate' and 'google' for backward compatibility
        google_api_key = api_keys.get('google_translate') or api_keys.get('google')
        
        if not google_api_key:
            return {
                'translation': None,
                'error': 'Google Translate API key not found in api_keys.txt (looking for "google_translate" or "google")',
                'success': False
            }
        
        # Use Google Cloud Translation API (Basic/v2) via REST
        try:
            import requests
            
            # Use REST API directly with API key
            url = "https://translation.googleapis.com/language/translate/v2"
            
            # Handle 'auto' source language
            params = {
                'key': google_api_key,
                'q': text,
                'target': target_lang
            }
            
            if source_lang and source_lang != 'auto':
                params['source'] = source_lang
            
            # Make API request
            response = requests.post(url, params=params)
            
            if response.status_code == 200:
                result = response.json()
                if 'data' in result and 'translations' in result['data']:
                    translation_data = result['data']['translations'][0]
                    return {
                        'translation': translation_data['translatedText'],
                        'confidence': 'High',
                        'detected_source_language': translation_data.get('detectedSourceLanguage', source_lang),
                        'provider': 'Google Cloud Translation',
                        'success': True,
                        'metadata': {
                            'model': 'nmt',  # Neural Machine Translation
                            'input': text
                        }
                    }
                else:
                    return {
                        'translation': None,
                        'error': f'Unexpected Google API response format: {result}',
                        'success': False
                    }
            else:
                return {
                    'translation': None,
                    'error': f'Google API error: {response.status_code} - {response.text}',
                    'success': False
                }
                
        except ImportError:
            # Fallback if requests is not installed
            return {
                'translation': None,
                'error': 'Requests library not installed. Install: pip install requests',
                'success': False
            }
    except Exception as e:
        return {
            'translation': None,
            'error': f'Google Translate error: {str(e)}',
            'success': False
        }


if __name__ == "__main__":
    main()
