"""Test Google Cloud Translation API with correct initialization"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_google_cloud_translate_with_env():
    """Test Google Cloud Translation API using environment variable"""
    try:
        from google.cloud import translate_v2 as translate
        
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
        
        print("Google Cloud Translation API Test")
        print("=" * 60)
        print("✓ google-cloud-translate library installed")
        
        if google_translate_key:
            print(f"✓ API key found: {google_translate_key[:15]}...{google_translate_key[-5:]}")
            
            # Set environment variable
            original_key = os.environ.get('GOOGLE_API_KEY')
            os.environ['GOOGLE_API_KEY'] = google_translate_key
            
            try:
                # Initialize client
                client = translate.Client()
                
                # Test translation
                print("\nTesting translation...")
                result = client.translate(
                    "Hello, world!",
                    source_language="en",
                    target_language="de"
                )
                
                print(f"  EN: Hello, world!")
                print(f"  DE: {result['translatedText']}")
                print("\n✓ Google Cloud Translation API is working!")
                
            except Exception as e:
                print(f"\n✗ Translation failed: {e}")
                print(f"\nError type: {type(e).__name__}")
                import traceback
                traceback.print_exc()
            finally:
                # Restore original environment variable
                if original_key is None:
                    os.environ.pop('GOOGLE_API_KEY', None)
                else:
                    os.environ['GOOGLE_API_KEY'] = original_key
        else:
            print("✗ API key not found in api_keys.txt")
            print("\nAdd to user data_private/api_keys.txt:")
            print("  google_translate = YOUR_API_KEY_HERE")
        
    except ImportError as e:
        print(f"✗ google-cloud-translate not installed: {e}")
        print("  Install with: pip install google-cloud-translate")


if __name__ == "__main__":
    test_google_cloud_translate_with_env()
