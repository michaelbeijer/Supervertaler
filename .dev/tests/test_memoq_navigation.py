. """
Test if ANY keys work in memoQ from pyautogui.
"""

import pyautogui
import time

print("memoQ Keyboard Test")
print("=" * 50)
print("Make sure memoQ is open with a segment active!")
print("This will test if keys reach memoQ at all.")
print("You have 5 seconds to switch to memoQ...")
print()

time.sleep(5)

tests = [
    ("Type 'TEST'", lambda: pyautogui.typewrite('TEST', interval=0.2)),
    ("Ctrl+A (select all)", lambda: pyautogui.hotkey('ctrl', 'a')),
    ("Backspace", lambda: pyautogui.press('backspace')),
    ("Ctrl+Shift+S (copy source)", lambda: pyautogui.hotkey('ctrl', 'shift', 's')),
    ("Down arrow", lambda: pyautogui.press('down')),
    ("Ctrl+Enter", lambda: pyautogui.hotkey('ctrl', 'enter')),
]

print("Starting keyboard tests...")
print("Watch memoQ closely!")
print()

try:
    for name, key_func in tests:
        print(f"Testing: {name}")
        key_func()
        time.sleep(2)
        
    print("\n✓ Test complete!")
    print("Which keys worked in memoQ?")
    
except KeyboardInterrupt:
    print("\n✗ Test stopped by user")

