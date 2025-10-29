1"""
Standalone test script for AutoFingers Python engine
Tests the translation automation without GUI integration
"""

import sys
import time
from modules.autofingers_engine import AutoFingersEngine


def test_tmx_loading():
    """Test TMX file loading."""
    print("=" * 60)
    print("TEST 1: TMX Loading")
    print("=" * 60)
    
    # Use the existing TMX file from your AutoFingers setup
    tmx_file = r"c:\Dev\Supervertaler\user data_private\Private tools\autofingers_tm.tmx"
    
    engine = AutoFingersEngine(
        tmx_file=tmx_file,
        source_lang="en",
        target_lang="nl"
    )
    
    success, message = engine.load_tmx()
    print(f"Result: {message}")
    
    if success:
        print(f"\nLoaded {engine.tm_count} translation units")
        print("\nSample translations:")
        for i, (source, target) in enumerate(list(engine.tm_database.items())[:5]):
            print(f"  {i+1}. '{source}' → '{target}'")
    
    return engine if success else None


def test_lookup():
    """Test translation lookup."""
    print("\n" + "=" * 60)
    print("TEST 2: Translation Lookup")
    print("=" * 60)
    
    engine = test_tmx_loading()
    if not engine:
        print("Cannot test lookup - TMX loading failed")
        return None
    
    # Test with first few entries
    print("\nTesting lookups:")
    test_sources = list(engine.tm_database.keys())[:3]
    
    for source in test_sources:
        translation = engine.lookup_translation(source)
        print(f"  '{source}' → '{translation}'")
    
    # Test with non-existent text
    translation = engine.lookup_translation("This text does not exist")
    print(f"  'This text does not exist' → {translation}")
    
    return engine


def test_single_segment():
    """Test single segment processing in memoQ."""
    print("\n" + "=" * 60)
    print("TEST 3: Single Segment Processing")
    print("=" * 60)
    
    engine = test_tmx_loading()
    if not engine:
        print("Cannot test segment processing - TMX loading failed")
        return
    
    print("\nThis will automate memoQ in 5 seconds...")
    print("Make sure memoQ is open with a segment ready!")
    print("The segment should contain text that matches your TMX.")
    print("\nCountdown:")
    
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\nProcessing segment NOW!")
    success, message = engine.process_single_segment()
    print(f"Result: {message}")
    
    if success:
        print("✓ Single segment processing works!")
    else:
        print("✗ Single segment processing failed")


def test_loop_mode():
    """Test loop mode processing."""
    print("\n" + "=" * 60)
    print("TEST 4: Loop Mode (3 segments)")
    print("=" * 60)
    
    engine = test_tmx_loading()
    if not engine:
        print("Cannot test loop mode - TMX loading failed")
        return
    
    print("\nThis will process 3 segments automatically in 5 seconds...")
    print("Make sure memoQ is open with multiple segments ready!")
    print("\nCountdown:")
    
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\nProcessing 3 segments NOW!")
    
    # Callback to show progress
    def progress_callback(success, message):
        print(f"  Segment {engine.segments_processed}: {message}")
    
    count, final_message = engine.process_multiple_segments(
        max_segments=3,
        callback=progress_callback
    )
    
    print(f"\nFinal result: {final_message}")
    print(f"✓ Processed {count} segments")


def main():
    """Main test menu."""
    print("\n" + "=" * 60)
    print("AutoFingers Python Engine - Test Suite")
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 60)
        print("Select test:")
        print("  1. Test TMX loading")
        print("  2. Test translation lookup")
        print("  3. Test single segment (memoQ automation)")
        print("  4. Test loop mode - 3 segments (memoQ automation)")
        print("  5. Run all tests")
        print("  0. Exit")
        print("-" * 60)
        
        choice = input("\nEnter choice (0-5): ").strip()
        
        if choice == "0":
            print("Exiting...")
            break
        elif choice == "1":
            test_tmx_loading()
        elif choice == "2":
            test_lookup()
        elif choice == "3":
            test_single_segment()
        elif choice == "4":
            test_loop_mode()
        elif choice == "5":
            test_tmx_loading()
            test_lookup()
            
            proceed = input("\nProceed with memoQ automation tests? (y/n): ").lower()
            if proceed == 'y':
                test_single_segment()
                
                proceed = input("\nProceed with loop mode test? (y/n): ").lower()
                if proceed == 'y':
                    test_loop_mode()
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    print("\nIMPORTANT: Before running memoQ tests, make sure:")
    print("  1. pyautogui and pyperclip are installed (pip install pyautogui pyperclip)")
    print("  2. memoQ is open with a project loaded")
    print("  3. You have segments that match your TMX file")
    print("  4. You're ready to let the script control your keyboard!\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
