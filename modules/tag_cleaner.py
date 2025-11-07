"""
TagCleaner Module for Supervertaler
Removes CAT tool tags from translation text

Supports tags from:
- memoQ
- Trados Studio
- CafeTran
- Wordfast

Can be used standalone or integrated with other modules like AutoFingers.
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class TagPattern:
    """Definition of a tag pattern to clean"""
    name: str
    description: str
    pattern: str  # Regex pattern
    enabled: bool = True


class TagCleaner:
    """
    Removes CAT tool tags from translation text.

    Usage:
        cleaner = TagCleaner()
        cleaner.enable_memoq_index_tags()
        cleaned = cleaner.clean("Text with [1}tags{2] here")
    """

    def __init__(self):
        """Initialize TagCleaner with all available tag patterns."""
        self.enabled = False  # Master switch

        # memoQ tag patterns
        self.memoq_patterns: Dict[str, TagPattern] = {
            "index_tags": TagPattern(
                name="memoQ Index Tags",
                description="Index tags like [1} {2] [3} {4] etc.",
                pattern=r'(?:\[\d+\}|\{\d+\])',
                enabled=True
            ),
            # Add more memoQ tag types here as needed
        }

        # Trados Studio tag patterns (placeholders for future)
        self.trados_patterns: Dict[str, TagPattern] = {
            # TODO: Add Trados tag patterns
        }

        # CafeTran tag patterns (placeholders for future)
        self.cafetran_patterns: Dict[str, TagPattern] = {
            # TODO: Add CafeTran tag patterns
        }

        # Wordfast tag patterns (placeholders for future)
        self.wordfast_patterns: Dict[str, TagPattern] = {
            # TODO: Add Wordfast tag patterns
        }

    def enable(self) -> None:
        """Enable tag cleaning (master switch)."""
        self.enabled = True

    def disable(self) -> None:
        """Disable tag cleaning (master switch)."""
        self.enabled = False

    def is_enabled(self) -> bool:
        """Check if tag cleaning is enabled."""
        return self.enabled

    # memoQ tag control methods
    def enable_memoq_index_tags(self) -> None:
        """Enable cleaning of memoQ index tags ([1} {2] etc.)."""
        if "index_tags" in self.memoq_patterns:
            self.memoq_patterns["index_tags"].enabled = True

    def disable_memoq_index_tags(self) -> None:
        """Disable cleaning of memoQ index tags."""
        if "index_tags" in self.memoq_patterns:
            self.memoq_patterns["index_tags"].enabled = False

    def is_memoq_index_tags_enabled(self) -> bool:
        """Check if memoQ index tag cleaning is enabled."""
        return self.memoq_patterns.get("index_tags", TagPattern("", "", "", False)).enabled

    # Generic pattern management
    def add_custom_pattern(self, category: str, key: str, pattern: TagPattern) -> None:
        """
        Add a custom tag pattern.

        Args:
            category: Category name ("memoq", "trados", "cafetran", "wordfast")
            key: Unique identifier for this pattern
            pattern: TagPattern to add
        """
        category_map = {
            "memoq": self.memoq_patterns,
            "trados": self.trados_patterns,
            "cafetran": self.cafetran_patterns,
            "wordfast": self.wordfast_patterns,
        }

        if category.lower() in category_map:
            category_map[category.lower()][key] = pattern

    def remove_pattern(self, category: str, key: str) -> None:
        """Remove a tag pattern."""
        category_map = {
            "memoq": self.memoq_patterns,
            "trados": self.trados_patterns,
            "cafetran": self.cafetran_patterns,
            "wordfast": self.wordfast_patterns,
        }

        if category.lower() in category_map:
            category_map[category.lower()].pop(key, None)

    def get_all_patterns(self) -> List[TagPattern]:
        """Get all tag patterns from all categories."""
        all_patterns = []
        all_patterns.extend(self.memoq_patterns.values())
        all_patterns.extend(self.trados_patterns.values())
        all_patterns.extend(self.cafetran_patterns.values())
        all_patterns.extend(self.wordfast_patterns.values())
        return all_patterns

    def get_enabled_patterns(self) -> List[TagPattern]:
        """Get only enabled tag patterns."""
        return [p for p in self.get_all_patterns() if p.enabled]

    def clean(self, text: str) -> str:
        """
        Remove tags from text based on enabled patterns.

        Args:
            text: Text potentially containing CAT tool tags

        Returns:
            Text with enabled tags removed
        """
        if not self.enabled or not text:
            return text

        cleaned_text = text

        # Apply all enabled patterns
        for pattern in self.get_enabled_patterns():
            cleaned_text = re.sub(pattern.pattern, '', cleaned_text)

        return cleaned_text

    def preview_cleaning(self, text: str) -> Dict[str, str]:
        """
        Preview what text would look like with each pattern applied.

        Args:
            text: Text to preview cleaning on

        Returns:
            Dictionary mapping pattern names to cleaned text
        """
        previews = {}

        for pattern in self.get_all_patterns():
            if pattern.enabled:
                cleaned = re.sub(pattern.pattern, '', text)
                previews[pattern.name] = cleaned

        return previews

    def to_dict(self) -> Dict:
        """
        Export settings to dictionary (for JSON serialization).

        Returns:
            Dictionary with all tag cleaner settings
        """
        return {
            "enabled": self.enabled,
            "memoq": {
                key: {"enabled": pattern.enabled}
                for key, pattern in self.memoq_patterns.items()
            },
            "trados": {
                key: {"enabled": pattern.enabled}
                for key, pattern in self.trados_patterns.items()
            },
            "cafetran": {
                key: {"enabled": pattern.enabled}
                for key, pattern in self.cafetran_patterns.items()
            },
            "wordfast": {
                key: {"enabled": pattern.enabled}
                for key, pattern in self.wordfast_patterns.items()
            },
        }

    def from_dict(self, settings: Dict) -> None:
        """
        Import settings from dictionary.

        Args:
            settings: Dictionary with tag cleaner settings
        """
        self.enabled = settings.get("enabled", False)

        # Load memoQ pattern states
        memoq_settings = settings.get("memoq", {})
        for key, pattern_settings in memoq_settings.items():
            if key in self.memoq_patterns:
                self.memoq_patterns[key].enabled = pattern_settings.get("enabled", True)

        # Load Trados pattern states
        trados_settings = settings.get("trados", {})
        for key, pattern_settings in trados_settings.items():
            if key in self.trados_patterns:
                self.trados_patterns[key].enabled = pattern_settings.get("enabled", False)

        # Load CafeTran pattern states
        cafetran_settings = settings.get("cafetran", {})
        for key, pattern_settings in cafetran_settings.items():
            if key in self.cafetran_patterns:
                self.cafetran_patterns[key].enabled = pattern_settings.get("enabled", False)

        # Load Wordfast pattern states
        wordfast_settings = settings.get("wordfast", {})
        for key, pattern_settings in wordfast_settings.items():
            if key in self.wordfast_patterns:
                self.wordfast_patterns[key].enabled = pattern_settings.get("enabled", False)


# Standalone usage example
if __name__ == "__main__":
    # Create cleaner
    cleaner = TagCleaner()

    # Enable tag cleaning
    cleaner.enable()

    # Enable specific tag types
    cleaner.enable_memoq_index_tags()

    # Test text
    test_text = "Laat de tractor nooit draaien in een afgesloten ruimte, tenzij de uitlaat naar buiten wordt afgevoerd [7}lucht.{8]"

    # Clean tags
    cleaned = cleaner.clean(test_text)

    print(f"Original: {test_text}")
    print(f"Cleaned:  {cleaned}")
    print(f"\nExpected: Laat de tractor nooit draaien in een afgesloten ruimte, tenzij de uitlaat naar buiten wordt afgevoerd lucht.")
