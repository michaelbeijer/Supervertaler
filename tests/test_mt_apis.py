"""Test Google Cloud Translation API"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_google_cloud_translate():
    """Test Google Cloud Translation API with sample text"""
    try:
        from google.cloud import translate_v2 as translate
        
        # Mock API key (user needs to add real one)
        api_key = "YOUR_GOOGLE_TRANSLATE_API_KEY_HERE"
        
        print("Google Cloud Translation API Test")
        print("=" * 60)
        print("✓ google-cloud-translate library installed")
        print(f"✗ API key not configured (add to api_keys.txt)")
        print("\nTo configure:")
        print("  1. Get API key from: https://console.cloud.google.com/apis/credentials")
        print("  2. Enable Cloud Translation API in your Google Cloud project")
        print("  3. Add to api_keys.txt:")
        print("     google_translate = YOUR_API_KEY_HERE")
        print("\nExample usage:")
        print("  client = translate.Client(api_key=api_key)")
        print("  result = client.translate('Hello', target_language='de')")
        print("  print(result['translatedText'])  # 'Hallo'")
        
    except ImportError as e:
        print(f"✗ google-cloud-translate not installed: {e}")
        print("  Install with: pip install google-cloud-translate")


def test_deepl():
    """Test DeepL API"""
    try:
        import deepl
        
        # Load API keys
        script_dir = os.path.dirname(os.path.abspath(__file__))
        api_keys_file = os.path.join(script_dir, "user data_private", "api_keys.txt")
        
        deepl_key = None
        if os.path.exists(api_keys_file):
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        if key.strip().lower() == "deepl":
                            deepl_key = value.strip()
                            break
        
        print("\n\nDeepL API Test")
        print("=" * 60)
        print("✓ deepl library installed")
        
        if deepl_key:
            print(f"✓ API key found: {deepl_key[:10]}...{deepl_key[-5:]}")
            
            # Test translation
            translator = deepl.Translator(deepl_key)
            result = translator.translate_text("Hello, world!", target_lang="DE")
            translated = str(result)  # Convert to string
            print(f"\nTest translation:")
            print(f"  EN: Hello, world!")
            print(f"  DE: {translated}")
            print("\n✓ DeepL API is working!")
        else:
            print("✗ API key not found in api_keys.txt")
        
    except ImportError:
        print("✗ deepl library not installed")
        print("  Install with: pip install deepl")
    except Exception as e:
        print(f"✗ DeepL test failed: {e}")


if __name__ == "__main__":
    test_google_cloud_translate()
    test_deepl()
