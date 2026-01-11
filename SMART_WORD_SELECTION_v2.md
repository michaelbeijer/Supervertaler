# Smart Word Selection - Code for PyQt6 CAT Tools

This feature automatically expands partial word selections to full words. When a translator selects part of a word (e.g., "ductiv" in "productivity"), it automatically expands to select the full word.

This trick was originally implemented in CafeTran Espresso and is one of the best ways to reduce the stressful feeling of selecting words on a computer.

**Now works across multiple lines!** If you select text spanning several lines, partial words at the START and END of your selection will be expanded to full words.

## Implementation

Add this method to your `QTextEdit` subclass (or any text editor widget):

```python
def mouseReleaseEvent(self, event):
    """Smart word selection - expand partial selections to full words
    
    Works across multiple lines - if you select text spanning several lines,
    partial words at the START and END of your selection will be expanded.
    """
    super().mouseReleaseEvent(event)

    # Optional: Check if feature is enabled via a setting
    # if not self.enable_smart_word_selection:
    #     return

    # Get the current cursor
    cursor = self.textCursor()

    # Only expand if there's a selection
    if cursor.hasSelection():
        # Get selection boundaries
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # Get the full text
        text = self.toPlainText()

        # Helper function to check if character is part of a word
        # Includes alphanumeric, underscore, hyphen, and apostrophe
        def is_word_char(char):
            return char.isalnum() or char in "_-'"

        # Track if we need to update the selection
        selection_changed = False

        # Expand START boundary if we're in the middle of a word
        # (i.e., the character before the selection is a word character)
        if start > 0 and is_word_char(text[start - 1]):
            # Also check that the first selected character is a word char
            # (to avoid expanding when selecting from whitespace)
            if start < len(text) and is_word_char(text[start]):
                while start > 0 and is_word_char(text[start - 1]):
                    start -= 1
                selection_changed = True

        # Expand END boundary if we're in the middle of a word
        # (i.e., the character after the selection is a word character)
        if end < len(text) and is_word_char(text[end]):
            # Also check that the last selected character is a word char
            # (to avoid expanding when selecting to whitespace)
            if end > 0 and is_word_char(text[end - 1]):
                while end < len(text) and is_word_char(text[end]):
                    end += 1
                selection_changed = True

        # Set the new selection if boundaries changed
        if selection_changed:
            cursor.setPosition(start)
            cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
            self.setTextCursor(cursor)
```

## Required Import

```python
from PyQt6.QtWidgets import QTextEdit
# Or if using PySide6:
# from PySide6.QtWidgets import QTextEdit
```

## Usage Example

```python
class SmartTextEdit(QTextEdit):
    """Text editor with smart word selection"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.enable_smart_word_selection = True  # Can be toggled via settings
    
    def mouseReleaseEvent(self, event):
        """Smart word selection - expand partial selections to full words"""
        super().mouseReleaseEvent(event)

        if not self.enable_smart_word_selection:
            return

        cursor = self.textCursor()

        if cursor.hasSelection():
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            text = self.toPlainText()

            def is_word_char(char):
                return char.isalnum() or char in "_-'"

            at_start_boundary = start == 0 or not is_word_char(text[start - 1])
            at_end_boundary = end == len(text) or not is_word_char(text[end])

            selection_length = end - start
            if (not at_start_boundary or not at_end_boundary) and selection_length < 50:
                while start > 0 and is_word_char(text[start - 1]):
                    start -= 1
                while end < len(text) and is_word_char(text[end]):
                    end += 1

                cursor.setPosition(start)
                cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
                self.setTextCursor(cursor)
```

## How It Works

1. **Triggers on mouse release** - After the user finishes a selection drag
2. **Checks for partial selection** - If selection doesn't start/end at word boundaries
3. **Expands both directions** - Moves start backward and end forward to word boundaries
4. **Word characters** - Alphanumeric + underscore + hyphen + apostrophe (covers most languages and compound words like "state-of-the-art")
5. **Length limit** - Only expands selections under 50 characters (prevents breaking intentional multi-word selections)

## Optional: Settings Integration

```python
# In your settings/preferences dialog:
smart_selection_checkbox = QCheckBox("Enable smart word selection")
smart_selection_checkbox.setToolTip(
    "When enabled, selecting part of a word automatically expands to the full word.\n\n"
    "Example: Selecting 'ductiv' in 'productivity' will automatically select 'productivity'.\n\n"
    "This makes word selection faster during translation."
)
```

## Notes

- Feel free to adapt the `is_word_char()` function if you need to include additional characters for specific languages or use cases
- This feature was inspired by CafeTran Espresso's implementation
- Code from Supervertaler (https://supervertaler.com) - MIT License
