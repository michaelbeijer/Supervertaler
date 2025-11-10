"""
Test script to display available Claude 4 models
"""

import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from modules.llm_clients import LLMClient

def display_claude_models():
    """Display all available Claude 4 models with their information"""
    print("=" * 80)
    print("AVAILABLE CLAUDE 4 MODELS FOR TRANSLATION")
    print("=" * 80)
    print()

    models = LLMClient.get_claude_model_info()

    for model_id, info in models.items():
        print(f"📘 {info['name']}")
        print(f"   Model ID: {model_id}")
        print(f"   Released: {info['released']}")
        print(f"   Description: {info['description']}")
        print(f"   Pricing: ${info['pricing']['input']}/MTok input, ${info['pricing']['output']}/MTok output")
        print(f"   Strengths: {', '.join(info['strengths'])}")
        print(f"   Use Case: {info['use_case']}")
        print()

    print("=" * 80)
    print(f"DEFAULT MODEL: {LLMClient.DEFAULT_MODELS['claude']}")
    print("=" * 80)

if __name__ == "__main__":
    display_claude_models()
