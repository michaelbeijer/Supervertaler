"""Test API keys loading"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_api_keys():
    """Load API keys from api_keys.txt file (supports both root and user data_private locations)"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try user data_private first (dev mode), then fallback to root
    possible_paths = [
        os.path.join(script_dir, "user data_private", "api_keys.txt"),
        os.path.join(script_dir, "api_keys.txt")
    ]
    
    api_keys_file = None
    for path in possible_paths:
        if os.path.exists(path):
            api_keys_file = path
            break
    
    # If no file exists, use root location
    if api_keys_file is None:
        api_keys_file = possible_paths[1]  # Default to root
    
    api_keys = {
        "google": "",           # For Gemini
        "google_translate": "", # For Google Cloud Translation API
        "claude": "",
        "openai": "",
        "deepl": ""
    }
    
    if os.path.exists(api_keys_file):
        try:
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        if key in ["google", "google_api_key", "gemini"]:
                            api_keys["google"] = value
                        elif key in ["google_translate", "google_translate_api_key"]:
                            api_keys["google_translate"] = value
                        elif key in ["claude", "claude_api_key", "anthropic"]:
                            api_keys["claude"] = value
                        elif key in ["openai", "openai_api_key", "chatgpt"]:
                            api_keys["openai"] = value
                        elif key in ["deepl", "deepl_api_key"]:
                            api_keys["deepl"] = value
            print(f"✓ API keys loaded from: {api_keys_file}")
        except Exception as e:
            print(f"Error reading api_keys.txt: {e}")
    else:
        print(f"No API keys file found at: {api_keys_file}")
    
    return api_keys


if __name__ == "__main__":
    print("Testing API keys loading...\n")
    
    api_keys = load_api_keys()
    
    print("\nAPI Keys Status:")
    print("=" * 60)
    for key, value in api_keys.items():
        if value:
            masked = value[:10] + "..." + value[-5:] if len(value) > 15 else value
            print(f"  {key:20s}: {masked}")
        else:
            print(f"  {key:20s}: [NOT SET]")
    
    print("\n" + "=" * 60)
    print(f"✓ Found {sum(1 for v in api_keys.values() if v)} / {len(api_keys)} API keys")
