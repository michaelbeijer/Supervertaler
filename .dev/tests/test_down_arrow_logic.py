"""
Test the new use_down_arrow feature in AutoFingers

Note: Despite the variable name 'use_down_arrow', we actually use Alt+N 
because pyautogui has issues with arrow keys in memoQ. Alt+N is memoQ's 
native "Go to Next Segment" command.
"""

# Quick verification that the logic is correct
print("Testing AutoFingers use_down_arrow logic")
print("=" * 60)

# Simulate different scenarios
scenarios = [
    # (is_exact, auto_confirm, auto_confirm_fuzzy, use_down_arrow, expected_behavior)
    (True, True, False, False, "Ctrl+Enter (exact match, auto-confirm ON, down arrow OFF)"),
    (True, True, False, True, "Alt+N (exact match, auto-confirm ON, down arrow ON)"),
    (True, False, False, False, "Alt+N (exact match, auto-confirm OFF, down arrow OFF)"),
    (True, False, False, True, "Alt+N (exact match, auto-confirm OFF, down arrow ON)"),
    (False, True, True, False, "Ctrl+Enter (fuzzy match, auto-confirm fuzzy ON, down arrow OFF)"),
    (False, True, True, True, "Alt+N (fuzzy match, auto-confirm fuzzy ON, down arrow ON)"),
    (False, True, False, False, "Alt+N (fuzzy match, auto-confirm fuzzy OFF, down arrow OFF)"),
    (False, True, False, True, "Alt+N (fuzzy match, auto-confirm fuzzy OFF, down arrow ON)"),
]

for is_exact, auto_confirm, auto_confirm_fuzzy, use_down_arrow, expected in scenarios:
    is_fuzzy = not is_exact
    should_auto_confirm = (is_exact and auto_confirm) or (is_fuzzy and auto_confirm_fuzzy)
    
    if should_auto_confirm and not use_down_arrow:
        action = "Ctrl+Enter"
    else:
        # Always use Alt+N when:
        # - use_down_arrow is enabled (leave unconfirmed)
        # - OR when not auto-confirming (leave unconfirmed)
        action = "Alt+N"
    
    match_type = "Exact" if is_exact else "Fuzzy"
    status = "✓" if action in expected else "✗"
    
    print(f"{status} {match_type:6} | auto_confirm={auto_confirm} fuzzy={auto_confirm_fuzzy} down={use_down_arrow} → {action:12} (expected: {expected})")

print("\n" + "=" * 60)
print("Logic verification complete!")
print("\nKey behaviors:")
print("1. When use_down_arrow=True: ALWAYS uses Alt+N (leaves unconfirmed)")
print("2. When use_down_arrow=False: Uses Ctrl+Enter for auto-confirm, Alt+N otherwise")
print("3. This gives translator full control over confirmation workflow")
print("\nNote: We use Alt+N instead of Down Arrow because pyautogui has issues")
print("with arrow keys in memoQ. Alt+N is memoQ's native 'Go to Next' command.")

