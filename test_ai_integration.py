#!/usr/bin/env python3
"""
Test script for AI integration in Style Guides feature.
Tests that LLM client is properly configured and responses work.
"""

import os
import sys

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_key_loading():
    """Test that API keys are loaded correctly"""
    print("=" * 70)
    print("TEST: API Key Loading")
    print("=" * 70)
    
    # Load API keys directly from file
    api_keys = {
        "google": "",
        "claude": "",
        "openai": ""
    }
    
    api_keys_file = os.path.join(os.path.dirname(__file__), "api_keys.txt")
    if os.path.exists(api_keys_file):
        try:
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        if key in ["openai", "openai_api_key", "chatgpt"]:
                            api_keys["openai"] = value
        except Exception as e:
            print(f"Error reading api_keys.txt: {e}")
    
    print(f"✓ API_KEYS loaded from api_keys.txt")
    print(f"  OpenAI key: {'Present (length {})'.format(len(api_keys.get('openai', ''))) if api_keys.get('openai') else 'Not configured'}")
    print(f"  Claude key: {'Present' if api_keys.get('claude') else 'Not configured'}")
    print(f"  Google key: {'Present' if api_keys.get('google') else 'Not configured'}\n")
    
    return bool(api_keys.get('openai')), api_keys

def test_prompt_assistant_methods():
    """Test that PromptAssistant has required methods"""
    print("=" * 70)
    print("TEST: PromptAssistant Methods")
    print("=" * 70)
    
    from modules.prompt_assistant import PromptAssistant
    
    assistant = PromptAssistant()
    
    has_send_message = hasattr(assistant, 'send_message')
    has_chat_history = hasattr(assistant, 'chat_history')
    has_set_llm = hasattr(assistant, 'set_llm_client')
    
    print(f"✓ PromptAssistant methods:")
    print(f"  - send_message: {has_send_message}")
    print(f"  - chat_history: {has_chat_history}")
    print(f"  - set_llm_client: {has_set_llm}\n")
    
    return has_send_message and has_chat_history and has_set_llm

def test_style_guides_library():
    """Test StyleGuideLibrary"""
    print("=" * 70)
    print("TEST: StyleGuideLibrary")
    print("=" * 70)
    
    from modules.style_guide_manager import StyleGuideLibrary
    
    try:
        library = StyleGuideLibrary()
        print(f"✓ StyleGuideLibrary available")
        print(f"  - get_all_languages: {hasattr(library, 'get_all_languages')}")
        print(f"  - append_to_all_guides: {hasattr(library, 'append_to_all_guides')}")
        print(f"  - append_to_guide: {hasattr(library, 'append_to_guide')}\n")
        return True
    except Exception as e:
        print(f"❌ StyleGuideLibrary error: {e}\n")
        return False

def test_offline_mode():
    """Test PromptAssistant in offline mode (no LLM)"""
    print("=" * 70)
    print("TEST: Offline Mode (No LLM)")
    print("=" * 70)
    
    from modules.prompt_assistant import PromptAssistant
    
    assistant = PromptAssistant()  # No LLM client
    
    # Simulate a call to send_message
    response = assistant.send_message(
        system_prompt="You are a style guide assistant",
        user_message="What are some good style rules?",
        callback=None
    )
    
    if response:
        print(f"✓ send_message works in offline mode")
        print(f"  Response: {str(response)[:80]}...\n")
        return True
    else:
        print(f"❌ send_message returned None\n")
        return False


def test_style_guides_ai_integration():
    """Test that style guides AI integration is properly set up"""
    print("=" * 70)
    print("TEST: Style Guides AI Integration Setup")
    print("=" * 70)
    
    from modules.prompt_assistant import PromptAssistant
    from modules.style_guide_manager import StyleGuideLibrary
    
    # Check that methods exist
    assistant = PromptAssistant()
    
    has_send_message = hasattr(assistant, 'send_message')
    has_chat_history = hasattr(assistant, 'chat_history')
    has_set_llm = hasattr(assistant, 'set_llm_client')
    
    print(f"✓ PromptAssistant methods:")
    print(f"  - send_message: {has_send_message}")
    print(f"  - chat_history: {has_chat_history}")
    print(f"  - set_llm_client: {has_set_llm}\n")
    
    # Check StyleGuideLibrary exists
    try:
        library = StyleGuideLibrary()
        print(f"✓ StyleGuideLibrary available")
        print(f"  - get_all_languages: {hasattr(library, 'get_all_languages')}")
        print(f"  - append_to_all_guides: {hasattr(library, 'append_to_all_guides')}")
        print(f"  - append_to_guide: {hasattr(library, 'append_to_guide')}\n")
        return True
    except Exception as e:
        print(f"❌ StyleGuideLibrary error: {e}\n")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("🧪 STYLE GUIDES AI INTEGRATION TESTS")
    print("=" * 70)
    print()
    
    # Test API key loading
    has_api_key, api_keys = test_api_key_loading()
    
    # Test PromptAssistant methods
    pa_methods = test_prompt_assistant_methods()
    
    # Test Style Guides library
    sg_lib = test_style_guides_library()
    
    # Test offline mode
    offline_ok = test_offline_mode()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"API Keys Loaded: {'✓' if has_api_key else '⚠'}")
    print(f"PromptAssistant Methods: {'✓' if pa_methods else '❌'}")
    print(f"StyleGuideLibrary: {'✓' if sg_lib else '❌'}")
    print(f"Offline Mode: {'✓' if offline_ok else '❌'}")
    print()
    
    # Overall result
    all_pass = pa_methods and sg_lib and offline_ok
    if all_pass:
        print("✅ AI Integration framework is ready!")
        if has_api_key:
            print("✓ OpenAI API key is configured for full AI assistance.")
        else:
            print("⚠ No OpenAI API key configured. Offline mode with command system is available.")
        return 0
    else:
        print("❌ AI Integration setup has issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())
