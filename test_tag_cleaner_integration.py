"""
Test TagCleaner integration with AutoFingers
"""

from modules.tag_cleaner import TagCleaner
from modules.autofingers_engine import AutoFingersEngine

def test_tag_cleaner_standalone():
    """Test TagCleaner as standalone module"""
    print("=" * 60)
    print("TEST 1: Standalone TagCleaner")
    print("=" * 60)

    cleaner = TagCleaner()
    cleaner.enable()
    cleaner.enable_memoq_index_tags()

    test_texts = [
        "Laat de tractor nooit draaien in een afgesloten ruimte, tenzij de uitlaat naar buiten wordt afgevoerd [7}lucht.{8]",
        "This has [1}multiple{2] tags [3}in{4] it.",
        "No tags here!",
        "[15}Start{16] and [99}end{100] tags",
    ]

    for text in test_texts:
        cleaned = cleaner.clean(text)
        print(f"\nOriginal: {text}")
        print(f"Cleaned:  {cleaned}")

    print("\n[PASS] Standalone test complete\n")


def test_autofingers_integration():
    """Test TagCleaner integration with AutoFingers"""
    print("=" * 60)
    print("TEST 2: AutoFingers Integration")
    print("=" * 60)

    # Create AutoFingers engine (dummy TMX)
    engine = AutoFingersEngine(
        tmx_file="user_data_private/autofingers_tm.tmx",
        source_lang="en",
        target_lang="nl"
    )

    # Test tag cleaner is available
    assert hasattr(engine, 'tag_cleaner'), "AutoFingers should have tag_cleaner attribute"
    print("[OK] AutoFingers has tag_cleaner attribute")

    # Test enabling tag cleaning
    engine.tag_cleaner.enable()
    engine.tag_cleaner.enable_memoq_index_tags()
    print("[OK] Tag cleaning enabled")

    # Test cleaning via engine
    test_text = "Text with [1}tags{2] inside"
    cleaned = engine.tag_cleaner.clean(test_text)
    expected = "Text with tags inside"

    print(f"\nOriginal: {test_text}")
    print(f"Cleaned:  {cleaned}")
    print(f"Expected: {expected}")

    assert cleaned == expected, f"Expected '{expected}', got '{cleaned}'"
    print("[OK] Tag cleaning works correctly via AutoFingers engine")

    # Test disabling
    engine.tag_cleaner.disable()
    not_cleaned = engine.tag_cleaner.clean(test_text)
    assert not_cleaned == test_text, "Disabled cleaner should return original text"
    print("[OK] Disabling tag cleaning works")

    print("\n[OK] Integration test complete\n")


def test_settings_export():
    """Test settings export/import"""
    print("=" * 60)
    print("TEST 3: Settings Export/Import")
    print("=" * 60)

    cleaner = TagCleaner()
    cleaner.enable()
    cleaner.enable_memoq_index_tags()

    # Export settings
    settings = cleaner.to_dict()
    print(f"\nExported settings:")
    import json
    print(json.dumps(settings, indent=2))

    # Create new cleaner and import
    cleaner2 = TagCleaner()
    cleaner2.from_dict(settings)

    assert cleaner2.is_enabled(), "Imported cleaner should be enabled"
    assert cleaner2.is_memoq_index_tags_enabled(), "memoQ index tags should be enabled"
    print("\n[OK] Settings export/import works")

    print("\n[OK] Settings test complete\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TagCleaner Module Test Suite")
    print("=" * 60 + "\n")

    test_tag_cleaner_standalone()
    test_autofingers_integration()
    test_settings_export()

    print("=" * 60)
    print("ALL TESTS PASSED [OK]")
    print("=" * 60)
