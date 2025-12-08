"""
Model Update Dialog for Supervertaler
======================================

Dialog window that displays new LLM models detected by the version checker.
Allows users to easily add new models to their configuration.

Features:
- Shows new models grouped by provider
- Click to select models to add
- One-click "Add Selected" button
- Shows model details when available
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QGroupBox, QScrollArea, QWidget, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Dict, List


class ModelUpdateDialog(QDialog):
    """Dialog for showing and adding new models"""

    models_selected = pyqtSignal(dict)  # Emits selected models by provider

    def __init__(self, results: Dict, parent=None):
        """
        Initialize the dialog

        Args:
            results: Results from ModelVersionChecker.check_all_providers()
            parent: Parent widget
        """
        super().__init__(parent)
        self.results = results
        self.selected_models = {
            "openai": [],
            "claude": [],
            "gemini": []
        }

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🆕 New LLM Models Available")
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)

        layout = QVBoxLayout()

        # Header
        header_label = QLabel("New models have been detected from LLM providers!")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)

        info_label = QLabel(
            "Select the models you want to add to your Supervertaler configuration.\n"
            "These models will be added to the respective dropdowns in Settings."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Scroll area for model groups
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Track if we have any new models
        has_new_models = False

        # OpenAI models
        if self.results.get("openai", {}).get("new_models"):
            has_new_models = True
            openai_group = self._create_provider_group(
                "OpenAI",
                self.results["openai"]["new_models"],
                "openai"
            )
            scroll_layout.addWidget(openai_group)

        # Claude models
        if self.results.get("claude", {}).get("new_models"):
            has_new_models = True
            claude_group = self._create_provider_group(
                "Anthropic Claude",
                self.results["claude"]["new_models"],
                "claude"
            )
            scroll_layout.addWidget(claude_group)

        # Gemini models
        if self.results.get("gemini", {}).get("new_models"):
            has_new_models = True
            gemini_group = self._create_provider_group(
                "Google Gemini",
                self.results["gemini"]["new_models"],
                "gemini"
            )
            scroll_layout.addWidget(gemini_group)

        # Show errors if any
        error_text = []
        for provider in ["openai", "claude", "gemini"]:
            error = self.results.get(provider, {}).get("error")
            if error and "No API key" not in error:
                error_text.append(f"❌ {provider.capitalize()}: {error}")

        if error_text:
            error_box = QGroupBox("⚠️ Errors")
            error_layout = QVBoxLayout()
            error_label = QLabel("\n".join(error_text))
            error_label.setWordWrap(True)
            error_label.setStyleSheet("color: #d32f2f;")
            error_layout.addWidget(error_label)
            error_box.setLayout(error_layout)
            scroll_layout.addWidget(error_box)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # Buttons
        button_layout = QHBoxLayout()

        if has_new_models:
            select_all_btn = QPushButton("Select All")
            select_all_btn.clicked.connect(self._select_all)
            button_layout.addWidget(select_all_btn)

            deselect_all_btn = QPushButton("Deselect All")
            deselect_all_btn.clicked.connect(self._deselect_all)
            button_layout.addWidget(deselect_all_btn)

        button_layout.addStretch()

        if has_new_models:
            add_btn = QPushButton("Add Selected Models")
            add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            add_btn.clicked.connect(self._add_selected)
            button_layout.addWidget(add_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _create_provider_group(self, provider_name: str, models: List[str], provider_key: str) -> QGroupBox:
        """
        Create a group box for a provider's models

        Args:
            provider_name: Display name (e.g., "OpenAI")
            models: List of model IDs
            provider_key: Key for tracking selections ("openai", "claude", "gemini")

        Returns:
            QGroupBox with checkboxes for each model
        """
        group = QGroupBox(f"🤖 {provider_name} ({len(models)} new model{'s' if len(models) != 1 else ''})")
        layout = QVBoxLayout()

        # Create checkbox for each model
        for model in models:
            checkbox = CheckmarkCheckBox(model)
            checkbox.setChecked(True)  # Pre-select all by default
            checkbox.stateChanged.connect(
                lambda state, m=model, p=provider_key: self._on_model_toggled(p, m, state)
            )
            layout.addWidget(checkbox)

            # Add model to selected by default
            if model not in self.selected_models[provider_key]:
                self.selected_models[provider_key].append(model)

        group.setLayout(layout)
        return group

    def _on_model_toggled(self, provider: str, model: str, state: int):
        """Handle checkbox toggle"""
        if state == Qt.CheckState.Checked.value:
            if model not in self.selected_models[provider]:
                self.selected_models[provider].append(model)
        else:
            if model in self.selected_models[provider]:
                self.selected_models[provider].remove(model)

    def _select_all(self):
        """Select all checkboxes"""
        for checkbox in self.findChildren(QCheckBox):
            checkbox.setChecked(True)

    def _deselect_all(self):
        """Deselect all checkboxes"""
        for checkbox in self.findChildren(QCheckBox):
            checkbox.setChecked(False)

    def _add_selected(self):
        """Emit signal with selected models and close dialog"""
        # Only include providers with selected models
        selected = {
            provider: models
            for provider, models in self.selected_models.items()
            if models
        }

        if selected:
            self.models_selected.emit(selected)
            self.accept()
        else:
            # No models selected
            self.reject()

    def get_selected_models(self) -> Dict[str, List[str]]:
        """Get the selected models"""
        return {
            provider: models
            for provider, models in self.selected_models.items()
            if models
        }


class NoNewModelsDialog(QDialog):
    """Simple dialog shown when no new models are found"""

    def __init__(self, last_check: str = None, parent=None):
        """
        Initialize dialog

        Args:
            last_check: ISO format timestamp of last check
            parent: Parent widget
        """
        super().__init__(parent)
        self.last_check = last_check
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("✅ No New Models")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Icon and message
        label = QLabel("✅ No new LLM models detected")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        label.setFont(font)
        layout.addWidget(label)

        info_label = QLabel(
            "Your Supervertaler is up to date with the latest models from:\n"
            "• OpenAI (GPT-4, GPT-5, o1, o3)\n"
            "• Anthropic (Claude Sonnet, Haiku, Opus)\n"
            "• Google (Gemini 2.5, Gemini 3)"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        if self.last_check:
            from datetime import datetime

class CheckmarkCheckBox(QCheckBox):
    """Custom checkbox with green background and white checkmark when checked"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setEnabled(True)
        self.setStyleSheet("""
            QCheckBox {
                font-size: 9pt;
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #999;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
            }
            QCheckBox::indicator:hover {
                border-color: #666;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #45a049;
                border-color: #45a049;
            }
        """)

    def paintEvent(self, event):
        """Override paint event to draw white checkmark when checked"""
        super().paintEvent(event)

        if self.isChecked():
            from PyQt6.QtWidgets import QStyleOptionButton
            from PyQt6.QtGui import QPainter, QPen, QColor
            from PyQt6.QtCore import QPointF, Qt

            opt = QStyleOptionButton()
            self.initStyleOption(opt)
            indicator_rect = self.style().subElementRect(
                self.style().SubElement.SE_CheckBoxIndicator,
                opt,
                self
            )

            if indicator_rect.isValid():
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                pen_width = max(2.0, min(indicator_rect.width(), indicator_rect.height()) * 0.12)
                painter.setPen(QPen(QColor(255, 255, 255), pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
                painter.setBrush(QColor(255, 255, 255))

                x = indicator_rect.x()
                y = indicator_rect.y()
                w = indicator_rect.width()
                h = indicator_rect.height()

                padding = min(w, h) * 0.15
                x += padding
                y += padding
                w -= padding * 2
                h -= padding * 2

                check_x1 = x + w * 0.10
                check_y1 = y + h * 0.50
                check_x2 = x + w * 0.35
                check_y2 = y + h * 0.70
                check_x3 = x + w * 0.90
                check_y3 = y + h * 0.25

                painter.drawLine(QPointF(check_x2, check_y2), QPointF(check_x3, check_y3))
                painter.drawLine(QPointF(check_x1, check_y1), QPointF(check_x2, check_y2))

                painter.end()

            try:
                check_time = datetime.fromisoformat(self.last_check)
                time_str = check_time.strftime("%Y-%m-%d %H:%M")
                last_check_label = QLabel(f"Last checked: {time_str}")
                last_check_label.setStyleSheet("color: #666; font-style: italic;")
                layout.addWidget(last_check_label)
            except:
                pass

        layout.addStretch()

        # Close button
        close_btn = QPushButton("OK")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)
