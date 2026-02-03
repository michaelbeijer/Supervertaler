"""
QuickTrans - Instant translation popup (GT4T-style)

A popup window that shows translations from all enabled MT engines and LLMs.
Part of the Supervertaler tool suite. Triggered by Ctrl+M (in-app) or Ctrl+Alt+M (global).

Features:
- Shows source text at the top
- Displays numbered list of translations from MT engines and LLMs
- Press number key (1-9) or click to insert translation
- Escape to dismiss
- Translations fetched in parallel for speed
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QWidget, QPushButton, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSettings
from PyQt6.QtGui import QKeySequence, QShortcut, QCursor, QFont
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class MTSuggestion:
    """A single MT suggestion from a provider"""
    provider_name: str  # Full name: "Google Translate", "DeepL", etc.
    provider_code: str  # Short code: "GT", "DL", etc.
    translation: str
    is_error: bool = False


class MTFetchWorker(QThread):
    """Background worker to fetch MT translations in parallel"""

    result_ready = pyqtSignal(str, str, str, bool)  # provider_name, provider_code, translation, is_error
    all_complete = pyqtSignal()

    def __init__(self, source_text: str, source_lang: str, target_lang: str,
                 providers: List[Tuple[str, str, callable]], parent=None):
        super().__init__(parent)
        self.source_text = source_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.providers = providers  # List of (name, code, call_function)

    def run(self):
        """Fetch translations from all providers in parallel"""
        def fetch_single(provider_info):
            name, code, call_func = provider_info
            try:
                result = call_func(self.source_text, self.source_lang, self.target_lang)
                is_error = result.startswith('[') and 'error' in result.lower()
                return (name, code, result, is_error)
            except Exception as e:
                return (name, code, f"[Error: {str(e)}]", True)

        # Use ThreadPoolExecutor for parallel execution
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(fetch_single, p): p for p in self.providers}
            for future in as_completed(futures):
                try:
                    name, code, translation, is_error = future.result()
                    self.result_ready.emit(name, code, translation, is_error)
                except Exception as e:
                    provider = futures[future]
                    self.result_ready.emit(provider[0], provider[1], f"[Error: {str(e)}]", True)

        self.all_complete.emit()


class MTSuggestionItem(QFrame):
    """A single MT suggestion row in the popup"""

    clicked = pyqtSignal(str)  # Emits the translation text when clicked

    def __init__(self, number: int, suggestion: MTSuggestion, parent=None):
        super().__init__(parent)
        self.suggestion = suggestion
        self.number = number
        self.is_selected = False

        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(10)

        # Number badge
        num_label = QLabel(str(number))
        num_label.setFixedSize(24, 24)
        num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        num_label.setStyleSheet("""
            QLabel {
                background-color: #ff9800;
                color: #333;
                font-weight: bold;
                font-size: 11px;
                border-radius: 4px;
            }
        """)
        layout.addWidget(num_label)

        # Provider icon/code badge
        provider_label = QLabel(suggestion.provider_code)
        provider_label.setFixedWidth(36)
        provider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        provider_label.setToolTip(suggestion.provider_name)

        # Color-code by provider
        provider_colors = {
            "GT": "#4285F4",   # Google blue
            "DL": "#042B48",   # DeepL dark blue
            "MS": "#00A4EF",   # Microsoft blue
            "AT": "#FF9900",   # Amazon orange
            "MMT": "#6B4EE6",  # ModernMT purple
            "MM": "#2ECC71",   # MyMemory green
            # LLM providers
            "CL": "#D97706",   # Claude orange/amber
            "GPT": "#10A37F",  # OpenAI green
            "GEM": "#4285F4",  # Gemini blue (Google)
        }
        bg_color = provider_colors.get(suggestion.provider_code, "#666")
        provider_label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: white;
                font-weight: bold;
                font-size: 9px;
                border-radius: 3px;
                padding: 2px 4px;
            }}
        """)
        layout.addWidget(provider_label)

        # Translation text
        text_label = QLabel(suggestion.translation)
        text_label.setWordWrap(True)
        text_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        if suggestion.is_error:
            text_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")
        else:
            text_label.setStyleSheet("color: #333; font-size: 11px;")

        layout.addWidget(text_label, 1)

        self._update_style()

    def _update_style(self):
        """Update visual style based on selection state"""
        if self.is_selected:
            self.setStyleSheet("""
                MTSuggestionItem {
                    background-color: #e3f2fd;
                    border: 1px solid #2196F3;
                    border-radius: 4px;
                }
            """)
        else:
            self.setStyleSheet("""
                MTSuggestionItem {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                }
                MTSuggestionItem:hover {
                    background-color: #f5f5f5;
                    border: 1px solid #bdbdbd;
                }
            """)

    def select(self):
        """Select this item"""
        self.is_selected = True
        self._update_style()

    def deselect(self):
        """Deselect this item"""
        self.is_selected = False
        self._update_style()

    def mousePressEvent(self, event):
        """Handle click to select this translation"""
        if event.button() == Qt.MouseButton.LeftButton and not self.suggestion.is_error:
            self.clicked.emit(self.suggestion.translation)
        super().mousePressEvent(event)


class MTQuickPopup(QDialog):
    """
    GT4T-style popup showing MT suggestions from all enabled providers

    Usage:
        popup = MTQuickPopup(parent_app, source_text, source_lang, target_lang)
        popup.translation_selected.connect(on_translation_selected)
        popup.show()
    """

    translation_selected = pyqtSignal(str)  # Emitted when user selects a translation

    def __init__(self, parent_app, source_text: str, source_lang: str = None,
                 target_lang: str = None, parent=None):
        super().__init__(parent)
        self.parent_app = parent_app
        self.source_text = source_text
        self.source_lang = source_lang or getattr(parent_app, 'source_language', 'en')
        self.target_lang = target_lang or getattr(parent_app, 'target_language', 'nl')

        self.suggestions: List[MTSuggestion] = []
        self.suggestion_items: List[MTSuggestionItem] = []
        self.selected_index = -1
        self.worker = None

        self.setup_ui()
        self.setup_shortcuts()
        self.start_fetching()

    def setup_ui(self):
        """Setup the popup UI"""
        self.setWindowTitle("⚡ Supervertaler QuickTrans")
        # Use standard dialog with title bar for resize/move support
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.WindowCloseButtonHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        # Set size - allow resizing
        self.setMinimumWidth(450)
        self.setMinimumHeight(200)

        # Restore saved size and position or use defaults
        settings = QSettings("Supervertaler", "MTQuickPopup")
        saved_width = settings.value("width", 650, type=int)
        saved_height = settings.value("height", 400, type=int)
        self.resize(saved_width, saved_height)

        # Check if we have a saved position
        self._has_saved_position = settings.contains("x") and settings.contains("y")
        if self._has_saved_position:
            saved_x = settings.value("x", 0, type=int)
            saved_y = settings.value("y", 0, type=int)
            self.move(saved_x, saved_y)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)

        # Container with styling
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(8)

        # Header with title and settings button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 4)

        title_label = QLabel("⚡ Supervertaler QuickTrans")
        title_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #333;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Settings button
        settings_btn = QPushButton("⚙️")
        settings_btn.setFixedSize(24, 24)
        settings_btn.setToolTip("Configure QuickTrans providers")
        settings_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-radius: 4px;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        settings_btn.clicked.connect(self._open_settings)
        header_layout.addWidget(settings_btn)

        container_layout.addLayout(header_layout)

        # Source text display
        source_frame = QFrame()
        source_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
        """)
        source_layout = QVBoxLayout(source_frame)
        source_layout.setContentsMargins(8, 6, 8, 6)

        source_header = QLabel("Source:")
        source_header.setStyleSheet("font-size: 9px; color: #666; font-weight: bold;")
        source_layout.addWidget(source_header)

        source_text_label = QLabel(self.source_text)
        source_text_label.setWordWrap(True)
        source_text_label.setStyleSheet("font-size: 11px; color: #333;")
        source_text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        source_layout.addWidget(source_text_label)

        container_layout.addWidget(source_frame)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #e0e0e0;")
        sep.setFixedHeight(1)
        container_layout.addWidget(sep)

        # Suggestions scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.suggestions_container = QWidget()
        self.suggestions_layout = QVBoxLayout(self.suggestions_container)
        self.suggestions_layout.setContentsMargins(0, 0, 0, 0)
        self.suggestions_layout.setSpacing(4)

        # Loading indicator
        self.loading_label = QLabel("⏳ Fetching translations...")
        self.loading_label.setStyleSheet("color: #666; font-size: 11px; padding: 20px;")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.suggestions_layout.addWidget(self.loading_label)

        self.suggestions_layout.addStretch()

        scroll.setWidget(self.suggestions_container)
        container_layout.addWidget(scroll, 1)

        # Footer with hint
        hint = QLabel("Press 1-9 to insert • ↑↓ to navigate • Enter to insert selected • Esc to close")
        hint.setStyleSheet("font-size: 9px; color: #999; padding-top: 4px;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(hint)

        main_layout.addWidget(container)

        # Position popup near cursor
        self._position_near_cursor()

    def _position_near_cursor(self):
        """Position the popup near the cursor (only if no saved position)"""
        # Skip if we restored a saved position
        if getattr(self, '_has_saved_position', False):
            # Verify saved position is still on a valid screen
            screen = QApplication.screenAt(self.pos())
            if screen:
                return  # Saved position is valid, use it

        # Position near cursor
        cursor_pos = QCursor.pos()
        screen = QApplication.screenAt(cursor_pos)
        if screen:
            screen_geo = screen.availableGeometry()

            # Try to position popup below and to the right of cursor
            x = cursor_pos.x() + 10
            y = cursor_pos.y() + 10

            # Ensure popup stays on screen
            if x + self.width() > screen_geo.right():
                x = cursor_pos.x() - self.width() - 10
            if y + self.height() > screen_geo.bottom():
                y = cursor_pos.y() - self.height() - 10

            # Clamp to screen bounds
            x = max(screen_geo.left(), min(x, screen_geo.right() - self.width()))
            y = max(screen_geo.top(), min(y, screen_geo.bottom() - self.height()))

            self.move(x, y)

    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Number keys 1-9 for quick selection
        for i in range(1, 10):
            shortcut = QShortcut(QKeySequence(str(i)), self)
            shortcut.activated.connect(lambda idx=i: self._select_by_number(idx))

        # Navigation
        QShortcut(QKeySequence(Qt.Key.Key_Up), self).activated.connect(self._navigate_up)
        QShortcut(QKeySequence(Qt.Key.Key_Down), self).activated.connect(self._navigate_down)
        QShortcut(QKeySequence(Qt.Key.Key_Return), self).activated.connect(self._insert_selected)
        QShortcut(QKeySequence(Qt.Key.Key_Enter), self).activated.connect(self._insert_selected)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self).activated.connect(self.close)

    def start_fetching(self):
        """Start fetching translations from all enabled providers"""
        providers = self._get_enabled_providers()

        if not providers:
            self.loading_label.setText("⚠️ No MT providers configured. Check Settings → MT Settings.")
            return

        self.worker = MTFetchWorker(
            self.source_text,
            self.source_lang,
            self.target_lang,
            providers,
            self
        )
        self.worker.result_ready.connect(self._on_result_ready)
        self.worker.all_complete.connect(self._on_all_complete)
        self.worker.start()

    def _get_enabled_providers(self) -> List[Tuple[str, str, callable]]:
        """Get list of enabled MT providers with their call functions"""
        providers = []

        if not self.parent_app:
            return providers

        api_keys = {}
        enabled_providers = {}

        if hasattr(self.parent_app, 'load_api_keys'):
            api_keys = self.parent_app.load_api_keys()
        if hasattr(self.parent_app, 'load_provider_enabled_states'):
            enabled_providers = self.parent_app.load_provider_enabled_states()

        # Load MT Quick Lookup specific settings
        mt_quick_settings = self._load_mt_quick_settings()

        # Define MT providers: (display_name, code, enabled_key, api_key_name, call_method_name)
        mt_provider_defs = [
            ("Google Translate", "GT", "mt_google_translate", "google_translate", "call_google_translate"),
            ("DeepL", "DL", "mt_deepl", "deepl", "call_deepl"),
            ("Microsoft Translator", "MS", "mt_microsoft", "microsoft_translate", "call_microsoft_translate"),
            ("Amazon Translate", "AT", "mt_amazon", "amazon_translate", "call_amazon_translate"),
            ("ModernMT", "MMT", "mt_modernmt", "modernmt", "call_modernmt"),
            ("MyMemory", "MM", "mt_mymemory", None, "call_mymemory"),  # MyMemory works without key
        ]

        for name, code, enabled_key, api_key_name, method_name in mt_provider_defs:
            # Check if provider is enabled in MT Quick Lookup settings (default: use MT Settings state)
            quick_lookup_key = f"mtql_{code.lower()}"
            if not mt_quick_settings.get(quick_lookup_key, enabled_providers.get(enabled_key, True)):
                continue

            # Check if API key is available (MyMemory doesn't require one)
            if api_key_name and not api_keys.get(api_key_name):
                continue

            # Get the call method
            if hasattr(self.parent_app, method_name):
                call_method = getattr(self.parent_app, method_name)

                # Create a wrapper that handles the API key
                api_key = api_keys.get(api_key_name) if api_key_name else None

                def make_caller(m, k):
                    return lambda text, src, tgt: m(text, src, tgt, k)

                providers.append((name, code, make_caller(call_method, api_key)))

        # Add LLM providers if enabled
        self._add_llm_providers(providers, api_keys, mt_quick_settings)

        return providers

    def _load_mt_quick_settings(self) -> Dict[str, Any]:
        """Load MT Quick Lookup specific settings"""
        if hasattr(self.parent_app, 'load_general_settings'):
            settings = self.parent_app.load_general_settings()
            return settings.get('mt_quick_lookup', {})
        return {}

    def _add_llm_providers(self, providers: List, api_keys: Dict, mt_quick_settings: Dict):
        """Add LLM providers (Claude, OpenAI, Gemini) to the providers list"""
        # LLM provider definitions: (name, code, api_key_name, settings_key)
        llm_defs = [
            ("Claude", "CL", "claude", "mtql_claude"),
            ("OpenAI", "GPT", "openai", "mtql_openai"),
            ("Gemini", "GEM", "gemini", "mtql_gemini"),
        ]

        for name, code, api_key_name, settings_key in llm_defs:
            # Check if LLM is enabled in MT Quick Lookup settings (default: disabled)
            if not mt_quick_settings.get(settings_key, False):
                continue

            # Check if API key is available
            if not api_keys.get(api_key_name):
                continue

            # Get model from settings or use default
            model_key = f"{settings_key}_model"
            model = mt_quick_settings.get(model_key, None)

            # Create LLM translation caller
            def make_llm_caller(provider_name, provider_key, provider_model):
                def call_llm(text, src_lang, tgt_lang):
                    return self._call_llm_translation(provider_key, text, src_lang, tgt_lang, provider_model)
                return call_llm

            providers.append((name, code, make_llm_caller(name, api_key_name, model)))

    def _call_llm_translation(self, provider: str, text: str, source_lang: str, target_lang: str, model: str = None) -> str:
        """Call LLM for translation"""
        try:
            from modules.llm_clients import LLMClient, load_api_keys

            api_keys = load_api_keys()
            api_key = api_keys.get(provider)

            if not api_key:
                return f"[Error: No API key for {provider}]"

            client = LLMClient(
                api_key=api_key,
                provider=provider,
                model=model
            )

            # Use the translate method
            result = client.translate(
                text=text,
                source_lang=source_lang,
                target_lang=target_lang
            )

            # Clean up result - remove quotes if present
            if result:
                result = result.strip()
                if (result.startswith('"') and result.endswith('"')) or (result.startswith("'") and result.endswith("'")):
                    result = result[1:-1]

            return result or "[No translation returned]"

        except Exception as e:
            return f"[Error: {str(e)}]"

    def _open_settings(self):
        """Open MT Quick Lookup settings tab"""
        if self.parent_app and hasattr(self.parent_app, 'open_mt_quick_lookup_settings'):
            self.close()  # Close popup first
            self.parent_app.open_mt_quick_lookup_settings()

    def _on_result_ready(self, provider_name: str, provider_code: str, translation: str, is_error: bool):
        """Handle a single MT result"""
        # Hide loading label on first result
        if self.loading_label.isVisible():
            self.loading_label.hide()

        # Create suggestion
        suggestion = MTSuggestion(
            provider_name=provider_name,
            provider_code=provider_code,
            translation=translation,
            is_error=is_error
        )
        self.suggestions.append(suggestion)

        # Create and add item widget
        item = MTSuggestionItem(len(self.suggestions), suggestion)
        item.clicked.connect(self._on_item_clicked)
        self.suggestion_items.append(item)

        # Insert before the stretch
        self.suggestions_layout.insertWidget(self.suggestions_layout.count() - 1, item)

        # Auto-select first non-error result
        if self.selected_index == -1 and not is_error:
            self._select_index(len(self.suggestion_items) - 1)

    def _on_all_complete(self):
        """Handle completion of all MT fetches"""
        if not self.suggestions:
            self.loading_label.setText("⚠️ No translations available.")
            self.loading_label.show()
        # Don't call adjustSize() - it shrinks the window and loses user's preferred size

    def _on_item_clicked(self, translation: str):
        """Handle click on a suggestion item"""
        self.translation_selected.emit(translation)
        self.close()

    def _select_by_number(self, number: int):
        """Select suggestion by number (1-based)"""
        idx = number - 1
        if 0 <= idx < len(self.suggestion_items):
            suggestion = self.suggestions[idx]
            if not suggestion.is_error:
                self.translation_selected.emit(suggestion.translation)
                self.close()

    def _select_index(self, index: int):
        """Select suggestion by index"""
        # Deselect previous
        if 0 <= self.selected_index < len(self.suggestion_items):
            self.suggestion_items[self.selected_index].deselect()

        # Select new (skip errors)
        if 0 <= index < len(self.suggestion_items):
            self.selected_index = index
            self.suggestion_items[index].select()
            # Ensure visible
            self.suggestion_items[index].setFocus()

    def _navigate_up(self):
        """Navigate to previous suggestion"""
        if not self.suggestion_items:
            return

        new_idx = self.selected_index - 1
        while new_idx >= 0:
            if not self.suggestions[new_idx].is_error:
                self._select_index(new_idx)
                return
            new_idx -= 1

    def _navigate_down(self):
        """Navigate to next suggestion"""
        if not self.suggestion_items:
            return

        new_idx = self.selected_index + 1
        while new_idx < len(self.suggestions):
            if not self.suggestions[new_idx].is_error:
                self._select_index(new_idx)
                return
            new_idx += 1

    def _insert_selected(self):
        """Insert the currently selected suggestion"""
        if 0 <= self.selected_index < len(self.suggestions):
            suggestion = self.suggestions[self.selected_index]
            if not suggestion.is_error:
                self.translation_selected.emit(suggestion.translation)
                self.close()

    def closeEvent(self, event):
        """Clean up worker on close and save window size and position"""
        # Save window size and position for next time
        settings = QSettings("Supervertaler", "MTQuickPopup")
        settings.setValue("width", self.width())
        settings.setValue("height", self.height())
        settings.setValue("x", self.x())
        settings.setValue("y", self.y())

        # Clean up worker
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait(1000)
        super().closeEvent(event)
