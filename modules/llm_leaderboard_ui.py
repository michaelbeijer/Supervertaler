"""
LLM Leaderboard - Qt UI Components
===================================

PyQt6 user interface for LLM translation benchmarking.

Features:
- Test dataset selection
- Model selection (checkboxes)
- Benchmark execution with progress
- Results table with comparison
- Summary statistics panel
- Export functionality

Author: Michael Beijer
License: MIT
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QPushButton, QComboBox, QCheckBox, QTableWidget, QTableWidgetItem,
    QProgressBar, QTextEdit, QSplitter, QHeaderView, QMessageBox,
    QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from typing import List, Optional, Dict
import json
from pathlib import Path

try:
    from modules.llm_leaderboard import (
        LLMLeaderboard, TestDataset, ModelConfig, BenchmarkResult,
        create_sample_datasets, CHRF_AVAILABLE
    )
except ImportError:
    from llm_leaderboard import (
        LLMLeaderboard, TestDataset, ModelConfig, BenchmarkResult,
        create_sample_datasets, CHRF_AVAILABLE
    )


class BenchmarkThread(QThread):
    """Background thread for running benchmarks without blocking UI"""

    progress_update = pyqtSignal(int, int, str)  # current, total, message
    finished = pyqtSignal(list)  # results
    error = pyqtSignal(str)  # error message

    def __init__(self, leaderboard: LLMLeaderboard, dataset: TestDataset, models: List[ModelConfig]):
        super().__init__()
        self.leaderboard = leaderboard
        self.dataset = dataset
        self.models = models

    def run(self):
        """Run benchmark in background thread"""
        try:
            results = self.leaderboard.run_benchmark(
                self.dataset,
                self.models,
                progress_callback=self._on_progress
            )
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

    def _on_progress(self, current: int, total: int, message: str):
        """Forward progress updates to main thread"""
        self.progress_update.emit(current, total, message)


class LLMLeaderboardUI(QWidget):
    """Main UI widget for LLM Leaderboard"""

    def __init__(self, parent=None, llm_client_factory=None):
        super().__init__(parent)
        self.parent_app = parent
        self.llm_client_factory = llm_client_factory
        self.leaderboard = None
        self.benchmark_thread = None
        self.current_results = []

        # Load sample datasets
        self.datasets = create_sample_datasets()
        self.current_dataset = self.datasets[0] if self.datasets else None

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Top section: Dataset and Model selection
        top_widget = self._create_top_section()
        layout.addWidget(top_widget)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; font-size: 9pt;")
        layout.addWidget(self.status_label)

        # Splitter for results and log
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Results table
        self.results_table = self._create_results_table()
        splitter.addWidget(self.results_table)

        # Summary panel
        self.summary_panel = self._create_summary_panel()
        splitter.addWidget(self.summary_panel)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(150)
        self.log_output.setPlaceholderText("Benchmark log will appear here...")
        splitter.addWidget(self.log_output)

        splitter.setStretchFactor(0, 3)  # Results table gets most space
        splitter.setStretchFactor(1, 1)  # Summary panel medium space
        splitter.setStretchFactor(2, 1)  # Log output smallest

        layout.addWidget(splitter)

        self.setLayout(layout)

    def _create_top_section(self) -> QWidget:
        """Create dataset selection and model selection section"""
        widget = QWidget()
        layout = QHBoxLayout()

        # Left: Dataset selection
        dataset_group = QGroupBox("Test Dataset")
        dataset_layout = QVBoxLayout()

        self.dataset_combo = QComboBox()
        for ds in self.datasets:
            self.dataset_combo.addItem(f"{ds.name} ({len(ds.segments)} segments)", ds)
        self.dataset_combo.currentIndexChanged.connect(self._on_dataset_changed)
        dataset_layout.addWidget(self.dataset_combo)

        dataset_info_label = QLabel("Select a test set to compare models")
        dataset_info_label.setStyleSheet("color: #666; font-size: 9pt;")
        dataset_layout.addWidget(dataset_info_label)

        # TODO: Add Import CSV and Create Custom buttons
        # import_btn = QPushButton("Import CSV...")
        # dataset_layout.addWidget(import_btn)

        dataset_layout.addStretch()
        dataset_group.setLayout(dataset_layout)
        layout.addWidget(dataset_group)

        # Right: Model selection
        model_group = QGroupBox("Model Selection")
        model_layout = QVBoxLayout()

        model_layout.addWidget(QLabel("Select models to test:"))

        # OpenAI models
        self.openai_checkbox = QCheckBox("OpenAI (GPT-4o)")
        self.openai_checkbox.setChecked(True)
        model_layout.addWidget(self.openai_checkbox)

        self.openai_model_combo = QComboBox()
        self.openai_model_combo.addItems([
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-5"
        ])
        self.openai_model_combo.setEnabled(True)
        model_layout.addWidget(self.openai_model_combo)

        # Claude models
        self.claude_checkbox = QCheckBox("Claude (Sonnet 4.5)")
        self.claude_checkbox.setChecked(True)
        model_layout.addWidget(self.claude_checkbox)

        self.claude_model_combo = QComboBox()
        self.claude_model_combo.addItems([
            "claude-sonnet-4-5-20250929",
            "claude-haiku-4-5-20251001",
            "claude-opus-4-1-20250805"
        ])
        self.claude_model_combo.setEnabled(True)
        model_layout.addWidget(self.claude_model_combo)

        # Gemini models
        self.gemini_checkbox = QCheckBox("Gemini (2.5 Flash)")
        self.gemini_checkbox.setChecked(True)
        model_layout.addWidget(self.gemini_checkbox)

        self.gemini_model_combo = QComboBox()
        self.gemini_model_combo.addItems([
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-2.5-pro"
        ])
        self.gemini_model_combo.setEnabled(True)
        model_layout.addWidget(self.gemini_model_combo)

        model_layout.addStretch()

        # Run button
        self.run_button = QPushButton("🚀 Run Benchmark")
        self.run_button.setStyleSheet("font-weight: bold; padding: 8px;")
        self.run_button.clicked.connect(self._on_run_benchmark)
        model_layout.addWidget(self.run_button)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self._on_cancel_benchmark)
        model_layout.addWidget(self.cancel_button)

        # Export button
        self.export_button = QPushButton("📊 Export Results...")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self._on_export_results)
        model_layout.addWidget(self.export_button)

        model_group.setLayout(model_layout)
        layout.addWidget(model_group)

        widget.setLayout(layout)
        return widget

    def _create_results_table(self) -> QTableWidget:
        """Create results comparison table"""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Segment", "Source Text", "Model", "Translation", "Speed (ms)", "Quality"
        ])

        # Set column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        return table

    def _create_summary_panel(self) -> QWidget:
        """Create summary statistics panel"""
        widget = QGroupBox("Summary Statistics")
        layout = QVBoxLayout()

        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(5)
        self.summary_table.setHorizontalHeaderLabels([
            "Model", "Avg Speed (ms)", "Avg Quality", "Success", "Errors"
        ])

        header = self.summary_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.summary_table.setMaximumHeight(200)
        self.summary_table.setAlternatingRowColors(True)
        self.summary_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.summary_table)
        widget.setLayout(layout)

        return widget

    def _on_dataset_changed(self, index: int):
        """Handle dataset selection change"""
        self.current_dataset = self.dataset_combo.itemData(index)
        self.log(f"Selected dataset: {self.current_dataset.name}")

    def _on_run_benchmark(self):
        """Start benchmark execution"""
        if not self.llm_client_factory:
            QMessageBox.warning(self, "Error", "LLM client factory not available")
            return

        if not self.current_dataset:
            QMessageBox.warning(self, "Error", "No dataset selected")
            return

        # Get selected models
        models = self._get_selected_models()
        if not models:
            QMessageBox.warning(self, "Error", "Please select at least one model to test")
            return

        # Confirm if sacrebleu not available
        if not CHRF_AVAILABLE:
            reply = QMessageBox.question(
                self,
                "Quality Scoring Unavailable",
                "sacrebleu library is not installed. Quality scores will not be calculated.\n\n"
                "Continue anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        # Clear previous results
        self.results_table.setRowCount(0)
        self.summary_table.setRowCount(0)
        self.log_output.clear()
        self.current_results = []

        # Update UI state
        self.run_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.export_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Running benchmark...")

        # Create leaderboard instance
        self.leaderboard = LLMLeaderboard(self.llm_client_factory, self.log)

        # Start benchmark in background thread
        self.benchmark_thread = BenchmarkThread(self.leaderboard, self.current_dataset, models)
        self.benchmark_thread.progress_update.connect(self._on_progress_update)
        self.benchmark_thread.finished.connect(self._on_benchmark_finished)
        self.benchmark_thread.error.connect(self._on_benchmark_error)
        self.benchmark_thread.start()

    def _on_cancel_benchmark(self):
        """Cancel running benchmark"""
        if self.leaderboard:
            self.leaderboard.cancel_benchmark()
            self.log("⚠️ Cancelling benchmark...")

    def _on_progress_update(self, current: int, total: int, message: str):
        """Update progress bar and status"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_label.setText(f"{message} ({current}/{total})")

    def _on_benchmark_finished(self, results: List[BenchmarkResult]):
        """Handle benchmark completion"""
        self.current_results = results

        # Update UI state
        self.run_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.export_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"✅ Benchmark complete: {len(results)} results")

        # Populate results table
        self._populate_results_table(results)

        # Populate summary table
        self._populate_summary_table()

        self.log("✅ Benchmark finished successfully")

    def _on_benchmark_error(self, error_msg: str):
        """Handle benchmark error"""
        self.run_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("❌ Benchmark failed")

        QMessageBox.critical(self, "Benchmark Error", f"An error occurred:\n\n{error_msg}")
        self.log(f"❌ Error: {error_msg}")

    def _populate_results_table(self, results: List[BenchmarkResult]):
        """Populate results table with benchmark data"""
        # Group results by segment
        segments_dict = {}
        for result in results:
            if result.segment_id not in segments_dict:
                segments_dict[result.segment_id] = []
            segments_dict[result.segment_id].append(result)

        # Populate table
        row = 0
        for segment_id in sorted(segments_dict.keys()):
            segment_results = segments_dict[segment_id]

            # Get source text from dataset
            source_text = ""
            for seg in self.current_dataset.segments:
                if seg.id == segment_id:
                    source_text = seg.source
                    break

            # Truncate source text for display
            if len(source_text) > 80:
                source_text = source_text[:77] + "..."

            for result in segment_results:
                self.results_table.insertRow(row)

                # Segment ID
                self.results_table.setItem(row, 0, QTableWidgetItem(str(segment_id)))

                # Source text
                self.results_table.setItem(row, 1, QTableWidgetItem(source_text))

                # Model name
                self.results_table.setItem(row, 2, QTableWidgetItem(result.model_name))

                # Translation output
                output_text = result.output if result.output else f"ERROR: {result.error}"
                if len(output_text) > 100:
                    output_text = output_text[:97] + "..."
                item = QTableWidgetItem(output_text)
                if result.error:
                    item.setForeground(QColor("red"))
                self.results_table.setItem(row, 3, item)

                # Speed
                speed_item = QTableWidgetItem(f"{result.latency_ms:.0f}")
                self.results_table.setItem(row, 4, speed_item)

                # Quality
                if result.quality_score is not None:
                    quality_item = QTableWidgetItem(f"{result.quality_score:.1f}")
                    self.results_table.setItem(row, 5, quality_item)
                else:
                    self.results_table.setItem(row, 5, QTableWidgetItem("—"))

                row += 1

    def _populate_summary_table(self):
        """Populate summary statistics table"""
        if not self.leaderboard:
            return

        summary = self.leaderboard.get_summary_stats()

        self.summary_table.setRowCount(len(summary))
        row = 0

        for model_name, stats in summary.items():
            # Model name
            self.summary_table.setItem(row, 0, QTableWidgetItem(model_name))

            # Avg speed
            avg_speed = stats["avg_latency_ms"]
            speed_item = QTableWidgetItem(f"{avg_speed:.0f}")
            self.summary_table.setItem(row, 1, speed_item)

            # Avg quality
            avg_quality = stats["avg_quality_score"]
            if avg_quality is not None:
                quality_item = QTableWidgetItem(f"{avg_quality:.1f}")
                self.summary_table.setItem(row, 2, quality_item)
            else:
                self.summary_table.setItem(row, 2, QTableWidgetItem("—"))

            # Success count
            self.summary_table.setItem(row, 3, QTableWidgetItem(str(stats["success_count"])))

            # Error count
            error_item = QTableWidgetItem(str(stats["error_count"]))
            if stats["error_count"] > 0:
                error_item.setForeground(QColor("red"))
            self.summary_table.setItem(row, 4, error_item)

            row += 1

    def _on_export_results(self):
        """Export results to file"""
        if not self.current_results:
            QMessageBox.warning(self, "No Results", "No benchmark results to export")
            return

        # Ask user for file path
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Export Benchmark Results",
            "llm_leaderboard_results.json",
            "JSON Files (*.json);;All Files (*)"
        )

        if not filepath:
            return

        try:
            # Export to JSON
            export_data = self.leaderboard.export_to_dict()
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            QMessageBox.information(self, "Export Complete", f"Results exported to:\n{filepath}")
            self.log(f"✅ Results exported to {filepath}")

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export results:\n{str(e)}")
            self.log(f"❌ Export error: {e}")

    def _get_selected_models(self) -> List[ModelConfig]:
        """Get list of selected models from UI"""
        models = []

        if self.openai_checkbox.isChecked():
            models.append(ModelConfig(
                name="GPT-4o",
                provider="openai",
                model_id=self.openai_model_combo.currentText()
            ))

        if self.claude_checkbox.isChecked():
            models.append(ModelConfig(
                name="Claude Sonnet 4.5",
                provider="claude",
                model_id=self.claude_model_combo.currentText()
            ))

        if self.gemini_checkbox.isChecked():
            models.append(ModelConfig(
                name="Gemini 2.5 Flash",
                provider="gemini",
                model_id=self.gemini_model_combo.currentText()
            ))

        return models

    def log(self, message: str):
        """Append message to log output"""
        self.log_output.append(message)


# For standalone testing
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Mock LLM client factory for testing UI
    def mock_llm_factory(provider, model):
        print(f"Mock: Creating {provider} client with model {model}")
        return None

    window = LLMLeaderboardUI(llm_client_factory=mock_llm_factory)
    window.setWindowTitle("LLM Leaderboard")
    window.resize(1200, 800)
    window.show()

    sys.exit(app.exec())
