"""Helpers for platform-appropriate shortcut labels in UI text."""

import sys
import re


_MAC_SYMBOLS = {
    "Ctrl": "⌘",
    "Alt": "⌥",
    "Shift": "⇧",
    "Meta": "⌘",
}

_SHORTCUT_PATTERN = re.compile(
    r"\b(?:Ctrl|Alt|Shift|Meta)(?:\+[A-Za-z0-9,=+\- ]+)+"
)


def format_shortcut_for_display(shortcut: str) -> str:
    """Return a platform-native shortcut label suitable for UI text."""
    if not shortcut or sys.platform != "darwin":
        return shortcut

    parts = shortcut.split("+")
    converted = [_MAC_SYMBOLS.get(part, part) for part in parts]
    has_symbol = any(part in _MAC_SYMBOLS.values() for part in converted)
    return "".join(converted) if has_symbol else "+".join(converted)


def format_shortcuts_in_text(text: str) -> str:
    """Replace all shortcut-like tokens in text with platform-native display."""
    if not text or sys.platform != "darwin":
        return text
    return _SHORTCUT_PATTERN.sub(lambda m: format_shortcut_for_display(m.group(0)), text)
