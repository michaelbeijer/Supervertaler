"""Test Google Cloud Translation API using REST API"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_google_translate_rest():
    """Test Google Cloud Translation API using direct REST calls"""
    try:
        import requests
        
        # Load API key from file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        api_keys_file = os.path.join(script_dir, "user data_private", "api_keys.txt")
        
        google_translate_key = None
        if os.path.exists(api_keys_file):
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        if key.strip().lower() == "google_translate":
                            google_translate_key = value.strip()
                            break
        
        print("Google Cloud Translation API Test (REST)")
        print("=" * 60)
        print("✓ requests library available")
        
        if google_translate_key:
            print(f"✓ API key found: {google_translate_key[:15]}...{google_translate_key[-5:]}")
            
            # Test translation using REST API
            print("\nTesting translation...")
            url = "https://translation.googleapis.com/language/translate/v2"
            params = {
                'key': google_translate_key,
                'q': 'Hello, world!',
                'source': 'en',
                'target': 'de',
                'format': 'text'
            }
            
            response = requests.post(url, params=params)
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result['data']['translations'][0]['translatedText']
                print(f"  EN: Hello, world!")
                print(f"  DE: {translated_text}")
                print("\n✓ Google Cloud Translation API is working!")
            else:
                print(f"\n✗ Translation failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
                # Try to parse error message
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        print(f"\nError details:")
                        print(f"  Code: {error_data['error'].get('code', 'N/A')}")
                        print(f"  Message: {error_data['error'].get('message', 'N/A')}")
                except:
                    pass
        else:
            print("✗ API key not found in api_keys.txt")
            print("\nAdd to user data_private/api_keys.txt:")
            print("  google_translate = YOUR_API_KEY_HERE")
        
    except ImportError as e:
        print(f"✗ requests library not installed: {e}")
        print("  Install with: pip install requests")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_google_translate_rest()
