"""
Model Version Checker for Supervertaler
========================================

Automatically checks for new LLM models from OpenAI, Anthropic, and Google.
Notifies users when new models are available and provides easy addition interface.

Features:
- Once-per-day automatic checking (configurable)
- Manual check button
- Popup dialog showing new models
- Easy click-to-add interface
- Caches results to avoid unnecessary API calls

Usage:
    from modules.model_version_checker import ModelVersionChecker

    checker = ModelVersionChecker(cache_path="user_data/model_cache.json")
    new_models = checker.check_for_new_models(
        openai_key="...",
        anthropic_key="...",
        google_key="..."
    )
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class ModelVersionChecker:
    """Check for new models from LLM providers"""

    def __init__(self, cache_path: str = None):
        """
        Initialize the model version checker

        Args:
            cache_path: Path to JSON cache file for storing last check time and known models
        """
        self.cache_path = cache_path or "model_version_cache.json"
        self.cache = self._load_cache()

        # Current known models (from llm_clients.py)
        self.known_models = {
            "openai": [
                "gpt-4o",
                "gpt-4o-mini",
                "chatgpt-4o-latest",
                "o1-preview",
                "o1-mini",
                "o3-mini",
                "gpt-4-turbo",
                "gpt-4"
            ],
            "claude": [
                "claude-sonnet-4-5-20250929",
                "claude-haiku-4-5-20251001",
                "claude-opus-4-1-20250805",
                "claude-3-5-sonnet-20241022",
                "claude-3-5-sonnet-20240620",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ],
            "gemini": [
                "gemini-3-pro-preview",
                "gemini-2.5-pro",
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-2.0-flash",
                "gemini-1.5-pro",
                "gemini-1.5-flash"
            ]
        }

    def _load_cache(self) -> dict:
        """Load cache from JSON file"""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            "last_check": None,
            "discovered_models": {
                "openai": [],
                "claude": [],
                "gemini": []
            }
        }

    def _save_cache(self):
        """Save cache to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save model cache: {e}")

    def should_check(self) -> bool:
        """
        Check if we should run the version check

        Returns:
            True if more than 24 hours since last check, or never checked
        """
        if not self.cache.get("last_check"):
            return True

        last_check = datetime.fromisoformat(self.cache["last_check"])
        return datetime.now() - last_check > timedelta(hours=24)

    def check_openai_models(self, api_key: str) -> Tuple[List[str], Optional[str]]:
        """
        Check for new OpenAI models

        Args:
            api_key: OpenAI API key

        Returns:
            (list of new model IDs, error message if any)
        """
        if not api_key:
            return [], "No API key provided"

        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            # List all models
            models = client.models.list()

            # Filter for GPT models (gpt-4*, gpt-5*, o1*, o3*)
            available_models = []
            for model in models.data:
                model_id = model.id
                if any(prefix in model_id.lower() for prefix in ['gpt-4', 'gpt-5', 'o1', 'o3']):
                    available_models.append(model_id)

            # Find new models not in our known list
            new_models = [m for m in available_models if m not in self.known_models["openai"]]

            return new_models, None

        except ImportError:
            return [], "OpenAI library not installed (pip install openai)"
        except Exception as e:
            return [], f"Error checking OpenAI models: {str(e)}"

    def check_claude_models(self, api_key: str) -> Tuple[List[str], Optional[str]]:
        """
        Check for new Claude models

        Note: Anthropic doesn't provide a models.list() endpoint, so we try
        to call the API with common model naming patterns and see what works.

        Args:
            api_key: Anthropic API key

        Returns:
            (list of new model IDs, error message if any)
        """
        if not api_key:
            return [], "No API key provided"

        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)

            # Anthropic doesn't have a list endpoint, so we'll try common patterns
            # This is a limitation - we can only detect models we explicitly test for
            test_patterns = [
                # Claude 5 potential patterns
                "claude-sonnet-5",
                "claude-haiku-5",
                "claude-opus-5",
                # Claude 4 with newer dates
                "claude-sonnet-4-5-20260101",
                "claude-haiku-4-5-20260101",
                "claude-opus-4-5-20260101",
            ]

            new_models = []

            # Test each pattern with a minimal API call
            for pattern in test_patterns:
                if pattern in self.known_models["claude"]:
                    continue

                try:
                    # Try a minimal API call
                    response = client.messages.create(
                        model=pattern,
                        max_tokens=1,
                        messages=[{"role": "user", "content": "test"}]
                    )
                    # If we got here, the model exists
                    new_models.append(pattern)
                except Exception as model_error:
                    # Model doesn't exist or other error - skip it
                    if "model" not in str(model_error).lower():
                        # Not a model error, might be real issue
                        pass

            return new_models, None

        except ImportError:
            return [], "Anthropic library not installed (pip install anthropic)"
        except Exception as e:
            return [], f"Error checking Claude models: {str(e)}"

    def check_gemini_models(self, api_key: str) -> Tuple[List[str], Optional[str]]:
        """
        Check for new Gemini models

        Args:
            api_key: Google AI API key

        Returns:
            (list of new model IDs, error message if any)
        """
        if not api_key:
            return [], "No API key provided"

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            # List all available models
            models = genai.list_models()

            # Filter for generative models only
            available_models = []
            for model in models:
                # Model name format: "models/gemini-xxx"
                if hasattr(model, 'name'):
                    model_id = model.name.replace('models/', '')
                    # Only include models that start with 'gemini'
                    if model_id.startswith('gemini'):
                        # Check if it supports generateContent
                        if hasattr(model, 'supported_generation_methods'):
                            if 'generateContent' in model.supported_generation_methods:
                                available_models.append(model_id)

            # Find new models not in our known list
            new_models = [m for m in available_models if m not in self.known_models["gemini"]]

            return new_models, None

        except ImportError:
            return [], "Google AI library not installed (pip install google-generativeai)"
        except Exception as e:
            return [], f"Error checking Gemini models: {str(e)}"

    def check_all_providers(
        self,
        openai_key: str = None,
        anthropic_key: str = None,
        google_key: str = None,
        force: bool = False
    ) -> Dict[str, Dict]:
        """
        Check all providers for new models

        Args:
            openai_key: OpenAI API key
            anthropic_key: Anthropic API key
            google_key: Google AI API key
            force: Force check even if checked recently

        Returns:
            Dictionary with results per provider:
            {
                "openai": {"new_models": [...], "error": None},
                "claude": {"new_models": [...], "error": None},
                "gemini": {"new_models": [...], "error": None},
                "checked": True
            }
        """
        # Check if we should run the check
        if not force and not self.should_check():
            return {
                "openai": {"new_models": [], "error": None},
                "claude": {"new_models": [], "error": None},
                "gemini": {"new_models": [], "error": None},
                "checked": False,
                "message": "Already checked in the last 24 hours"
            }

        results = {}

        # Check OpenAI
        if openai_key:
            new_models, error = self.check_openai_models(openai_key)
            results["openai"] = {"new_models": new_models, "error": error}
        else:
            results["openai"] = {"new_models": [], "error": "No API key"}

        # Check Claude
        if anthropic_key:
            new_models, error = self.check_claude_models(anthropic_key)
            results["claude"] = {"new_models": new_models, "error": error}
        else:
            results["claude"] = {"new_models": [], "error": "No API key"}

        # Check Gemini
        if google_key:
            new_models, error = self.check_gemini_models(google_key)
            results["gemini"] = {"new_models": new_models, "error": error}
        else:
            results["gemini"] = {"new_models": [], "error": "No API key"}

        # Update cache
        self.cache["last_check"] = datetime.now().isoformat()
        for provider, result in results.items():
            if result["new_models"] and not result["error"]:
                # Add newly discovered models to cache
                existing = set(self.cache["discovered_models"].get(provider, []))
                existing.update(result["new_models"])
                self.cache["discovered_models"][provider] = list(existing)

        self._save_cache()

        results["checked"] = True
        return results

    def has_new_models(self, results: Dict) -> bool:
        """
        Check if any new models were found

        Args:
            results: Results from check_all_providers()

        Returns:
            True if any new models found
        """
        if not results.get("checked"):
            return False

        for provider in ["openai", "claude", "gemini"]:
            if results.get(provider, {}).get("new_models"):
                return True

        return False

    def get_cache_info(self) -> Dict:
        """Get information about the cache"""
        return {
            "last_check": self.cache.get("last_check"),
            "discovered_models": self.cache.get("discovered_models", {})
        }


# Standalone test
if __name__ == "__main__":
    checker = ModelVersionChecker()

    # Test with dummy keys (will fail but shows structure)
    results = checker.check_all_providers(
        openai_key="dummy",
        anthropic_key="dummy",
        google_key="dummy",
        force=True
    )

    print("Check results:")
    print(json.dumps(results, indent=2))
