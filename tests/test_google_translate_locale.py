"""Test Google Translate with en-US → nl-NL conversion"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_lang_code(language: str) -> str:
    """Convert language name or locale code to 2-letter code for MT APIs"""
    # Handle locale codes like "en-US", "nl-NL", etc.
    if '-' in language or '_' in language:
        # Extract just the language part (before - or _)
        return language.split('-')[0].split('_')[0].lower()
    
    # Handle full language names
    lang_map = {
        "english": "en", "dutch": "nl", "german": "de", "french": "fr",
        "spanish": "es", "italian": "it", "portuguese": "pt", "russian": "ru",
        "chinese": "zh", "japanese": "ja", "korean": "ko", "arabic": "ar"
    }
    return lang_map.get(language.lower(), language.lower()[:2])


def test_google_translate_with_locales():
    """Test Google Translate with locale codes"""
    try:
        import requests
        
        # Load API key
        script_dir = os.path.dirname(os.path.abspath(__file__))
        api_keys_file = os.path.join(script_dir, "user_data_private", "api_keys.txt")
        
        google_translate_key = None
        if os.path.exists(api_keys_file):
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        if key.strip().lower() == "google_translate":
                            google_translate_key = value.strip()
                            break
        
        if not google_translate_key:
            print("✗ No API key found")
            return
        
        print("Google Translate Test with Locale Codes")
        print("=" * 60)
        
        # Simulate your project settings
        source_language = "en-US"
        target_language = "nl-NL"
        
        src_lang = get_lang_code(source_language)
        tgt_lang = get_lang_code(target_language)
        
        print(f"Project settings:")
        print(f"  Source: {source_language} → API code: {src_lang}")
        print(f"  Target: {target_language} → API code: {tgt_lang}")
        
        # Test translation
        text = "Hello, world!"
        print(f"\nTranslating: '{text}'")
        
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            'key': google_translate_key,
            'q': text,
            'source': src_lang,
            'target': tgt_lang,
            'format': 'text'
        }
        
        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result['data']['translations'][0]['translatedText']
            print(f"Result: '{translated_text}'")
            print("\n✓ Translation successful!")
        else:
            print(f"\n✗ Error {response.status_code}: {response.text}")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_google_translate_with_locales()
