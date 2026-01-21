# Quick test for data path functions
import sys
from pathlib import Path

# Simulate what's in Supervertaler.py
def get_user_data_path():
    """Get path to user data directory (writable)."""
    if getattr(sys, 'frozen', False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).parent if '__file__' in dir() else Path.cwd()
    return base / 'user_data'

def get_bundled_data_path():
    """Get path to bundled data (read-only defaults)."""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / 'user_data'
    else:
        return get_user_data_path()

print("=== Data Path Test ===")
print(f"Frozen: {getattr(sys, 'frozen', False)}")
print(f"User data path: {get_user_data_path()}")
print(f"Bundled data path: {get_bundled_data_path()}")

user_path = get_user_data_path()
bundled_path = get_bundled_data_path()

# Check dictionaries
dict_path = user_path / 'dictionaries'
if dict_path.exists():
    langs = [d.name for d in dict_path.iterdir() if d.is_dir()]
    print(f"Dictionaries: {langs}")
else:
    print(f"No dictionaries at {dict_path}")

# Check prompts
prompts_path = user_path / 'Prompt_Library'
if prompts_path.exists():
    prompts = list(prompts_path.rglob('*.svprompt'))
    print(f"Prompts: {len(prompts)} found")
else:
    print(f"No prompts at {prompts_path}")

print("=== Test Complete ===")
