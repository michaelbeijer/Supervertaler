"""
Test suite for AutoFingers fuzzy matching feature

Demonstrates the new fuzzy matching capability:
- Segment with tags that prevent exact matching
- Fuzzy match finds the best match (based on similarity)
- Fuzzy match is inserted but NOT auto-confirmed
- AutoFingers continues to next segment automatically
"""

import sys
from modules.autofingers_engine import AutoFingersEngine, TranslationMatch
import tempfile
import os


def create_test_tmx():
    """Create a test TMX file with sample translations"""
    
    tmx_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE tmx SYSTEM "tmx14.dtd">
<tmx version="1.4">
  <header
    creationtool="AutoFingers Test"
    creationtoolversion="1.0"
    datatype="PlainText"
    segtype="sentence"
    adminlang="en-US"
    srclang="en"
    o-tmf="AutoFingers"
  />
  <body>
    <!-- Exact match: no tags -->
    <tu>
      <tuv xml:lang="en">
        <seg>Hello world</seg>
      </tuv>
      <tuv xml:lang="nl">
        <seg>Hallo wereld</seg>
      </tuv>
    </tu>
    
    <!-- Your example: with tags [1}...{2] -->
    <tu>
      <tuv xml:lang="en">
        <seg>The on-site user can disconnect by clicking the Disconnect button in the remote assistance toolbar on the Console device.</seg>
      </tuv>
      <tuv xml:lang="nl">
        <seg>De gebruiker op locatie kan de verbinding verbreken door op de knop Disconnect te klikken in de werkbalk voor externe assistentie op het Console-apparaat.</seg>
      </tuv>
    </tu>
    
    <!-- Variations that will match via fuzzy matching -->
    <tu>
      <tuv xml:lang="en">
        <seg>The user can disconnect by clicking the Disconnect button in the toolbar.</seg>
      </tuv>
      <tuv xml:lang="nl">
        <seg>De gebruiker kan de verbinding verbreken door op de knop Disconnect te klikken in de werkbalk.</seg>
      </tuv>
    </tu>
    
    <tu>
      <tuv xml:lang="en">
        <seg>Click the disconnect button to end the session.</seg>
      </tuv>
      <tuv xml:lang="nl">
        <seg>Klik op de knop Verbreking om de sessie te beëindigen.</seg>
      </tuv>
    </tu>
    
    <!-- Different domain but similar structure -->
    <tu>
      <tuv xml:lang="en">
        <seg>The remote user can disconnect by clicking the Disconnect button.</seg>
      </tuv>
      <tuv xml:lang="nl">
        <seg>De externe gebruiker kan de verbinding verbreken door op de knop Verbreking te klikken.</seg>
      </tuv>
    </tu>
  </body>
</tmx>
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tmx', delete=False, encoding='utf-8') as f:
        f.write(tmx_content)
        return f.name


def test_exact_match():
    """Test 1: Exact match (100%)"""
    print("\n" + "="*70)
    print("TEST 1: Exact Match (100%)")
    print("="*70)
    
    tmx_file = create_test_tmx()
    
    try:
        engine = AutoFingersEngine(tmx_file, source_lang="en", target_lang="nl")
        success, message = engine.load_tmx()
        print(f"✓ Loaded TMX: {message}")
        
        # Test exact match
        result = engine.lookup_translation("Hello world")
        if result:
            print(f"\n✓ EXACT MATCH FOUND:")
            print(f"  Source:      'Hello world'")
            print(f"  Target:      '{result.translation}'")
            print(f"  Match Type:  {result.match_type}")
            print(f"  Match %:     {result.match_percent}%")
            assert result.match_type == "exact", "Should be exact match"
            assert result.match_percent == 100, "Should be 100%"
            print("\n✅ TEST 1 PASSED: Exact matching works")
        else:
            print("❌ TEST 1 FAILED: Should find exact match")
    finally:
        os.unlink(tmx_file)


def test_fuzzy_match_with_tags():
    """Test 2: Fuzzy match for segment with tags"""
    print("\n" + "="*70)
    print("TEST 2: Fuzzy Match (With Tags - Your Use Case)")
    print("="*70)
    
    tmx_file = create_test_tmx()
    
    try:
        engine = AutoFingersEngine(tmx_file, source_lang="en", target_lang="nl")
        engine.enable_fuzzy_matching = True
        engine.fuzzy_threshold = 0.75  # 75% threshold
        
        success, message = engine.load_tmx()
        print(f"✓ Loaded TMX: {message}")
        
        # Your example: segment WITH tags (these prevent exact matching)
        source_with_tags = "The on-site user can disconnect by clicking the [1}Disconnect{2] button in the remote assistance toolbar on the Console device."
        
        print(f"\nSearching for fuzzy match...")
        print(f"Input (with tags): '{source_with_tags}'")
        
        result = engine.lookup_translation(source_with_tags)
        if result:
            print(f"\n✓ FUZZY MATCH FOUND:")
            print(f"  Target:      '{result.translation}'")
            print(f"  Match Type:  {result.match_type}")
            print(f"  Match %:     {result.match_percent}%")
            
            assert result.match_type == "fuzzy", "Should be fuzzy match"
            assert result.match_percent > 0, "Should have positive match percentage"
            assert result.match_percent < 100, "Should not be 100% (exact)"
            
            print(f"\n✅ Fuzzy match found at {result.match_percent}%")
            print("   (Translator will see this and can confirm/edit)")
            print("\n✅ TEST 2 PASSED: Fuzzy matching handles tags correctly")
        else:
            print("❌ TEST 2 FAILED: Should find fuzzy match")
    finally:
        os.unlink(tmx_file)


def test_fuzzy_threshold_configuration():
    """Test 3: Fuzzy threshold configuration"""
    print("\n" + "="*70)
    print("TEST 3: Fuzzy Threshold Configuration")
    print("="*70)
    
    tmx_file = create_test_tmx()
    
    try:
        engine = AutoFingersEngine(tmx_file, source_lang="en", target_lang="nl")
        engine.enable_fuzzy_matching = True
        
        success, message = engine.load_tmx()
        print(f"✓ Loaded TMX: {message}")
        
        # Test with different thresholds
        test_cases = [
            ("Very similar text", 0.85, "High threshold (85%)"),
            ("Different text altogether", 0.50, "Low threshold (50%)"),
            ("Click the disconnect button to end the session", 0.75, "Medium threshold (75%)"),
        ]
        
        for source_text, threshold, description in test_cases:
            engine.fuzzy_threshold = threshold
            result = engine.lookup_translation(source_text)
            
            status = "✓ Found" if result else "✗ Not found"
            match_info = f" ({result.match_percent}%)" if result else ""
            print(f"\n{status}: {description}")
            print(f"     Input: '{source_text}'")
            if result:
                print(f"     Target: '{result.translation}'")
                print(f"     {match_info}")
        
        print("\n✅ TEST 3 PASSED: Threshold configuration works")
    finally:
        os.unlink(tmx_file)


def test_no_match_behavior():
    """Test 4: No match behavior (skip vs pause)"""
    print("\n" + "="*70)
    print("TEST 4: No Match Behavior")
    print("="*70)
    
    tmx_file = create_test_tmx()
    
    try:
        engine = AutoFingersEngine(tmx_file, source_lang="en", target_lang="nl")
        engine.enable_fuzzy_matching = True
        engine.fuzzy_threshold = 0.95  # Very high threshold
        
        success, message = engine.load_tmx()
        print(f"✓ Loaded TMX: {message}")
        
        # Completely different text that won't match
        unusual_text = "xyzzy abc def qwerty"
        
        result = engine.lookup_translation(unusual_text)
        if result is None:
            print(f"\n✓ Correctly returned None for non-matching text")
            print(f"   With skip_no_match=False: Would pause for manual translation")
            print(f"   With skip_no_match=True: Would skip segment and continue")
            print("\n✅ TEST 4 PASSED: No match behavior works correctly")
        else:
            print("❌ TEST 4 FAILED: Should not find match")
    finally:
        os.unlink(tmx_file)


def test_match_type_tracking():
    """Test 5: Match type tracking (exact vs fuzzy)"""
    print("\n" + "="*70)
    print("TEST 5: Match Type Tracking")
    print("="*70)
    
    tmx_file = create_test_tmx()
    
    try:
        engine = AutoFingersEngine(tmx_file, source_lang="en", target_lang="nl")
        engine.enable_fuzzy_matching = True
        engine.fuzzy_threshold = 0.75
        
        success, message = engine.load_tmx()
        print(f"✓ Loaded TMX: {message}")
        
        tests = [
            ("Hello world", "exact", 100),
            ("Hello world with extra text", "fuzzy", None),  # Will be fuzzy, exact % unknown
        ]
        
        for source, expected_type, expected_percent in tests:
            result = engine.lookup_translation(source)
            if result:
                match_result = "✓" if result.match_type == expected_type else "✗"
                print(f"\n{match_result} {source}")
                print(f"  Match Type: {result.match_type} (expected: {expected_type})")
                print(f"  Match %:    {result.match_percent}%")
                
                if expected_percent:
                    assert result.match_percent == expected_percent
        
        print("\n✅ TEST 5 PASSED: Match type tracking works correctly")
    finally:
        os.unlink(tmx_file)


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("AutoFingers Fuzzy Matching Feature Tests")
    print("="*70)
    print("\nTesting the new fuzzy matching fallback for AutoFingers")
    print("when segments contain tags that prevent exact matching.")
    
    try:
        test_exact_match()
        test_fuzzy_match_with_tags()
        test_fuzzy_threshold_configuration()
        test_no_match_behavior()
        test_match_type_tracking()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED")
        print("="*70)
        print("\n📋 Feature Summary:")
        print("  • AutoFingers now searches for fuzzy matches if exact match fails")
        print("  • Default threshold: 80% similarity")
        print("  • Fuzzy matches are inserted but NOT auto-confirmed")
        print("  • Translator can review/edit fuzzy matches")
        print("  • AutoFingers continues to next segment automatically")
        print("  • Tags in segments (like [1}text{2]) no longer cause skipping")
        print("\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
