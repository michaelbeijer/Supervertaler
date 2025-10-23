"""Test language code conversion with locale codes"""

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


# Test cases
test_cases = [
    ("en-US", "en"),
    ("nl-NL", "nl"),
    ("de-DE", "de"),
    ("fr-FR", "fr"),
    ("en_US", "en"),
    ("English", "en"),
    ("Dutch", "nl"),
    ("German", "de"),
    ("ENGLISH", "en"),
]

print("Language Code Conversion Tests")
print("=" * 50)
for input_lang, expected in test_cases:
    result = get_lang_code(input_lang)
    status = "✓" if result == expected else "✗"
    print(f"{status} {input_lang:15s} → {result:5s} (expected: {expected})")

print("\nYour project:")
print(f"  Source: en-US → {get_lang_code('en-US')}")
print(f"  Target: nl-NL → {get_lang_code('nl-NL')}")
