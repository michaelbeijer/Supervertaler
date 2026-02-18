"""
Find & Replace Module for Supervertaler (PyQt6)

This module provides enhanced Find & Replace functionality including:
- History dropdowns for recent search/replace terms
- Saveable F&R Sets for batch operations
- Import/Export of .svfr files

Classes:
    - FindReplaceHistory: Manages and persists recent search/replace terms
    - FindReplaceOperation: Single F&R operation with all settings
    - FindReplaceSet: Collection of F&R operations
    - FindReplaceSetsManager: UI widget for managing F&R sets
    - HistoryComboBox: Editable combo box with history dropdown

Author: Michael Beijer
License: MIT
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Callable
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QComboBox, QLineEdit, QHeaderView, QAbstractItemView,
    QMessageBox, QFileDialog, QInputDialog, QSplitter, QLabel, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor


class FindReplaceHistory:
    """Manages and persists recent find/replace terms."""
    
    MAX_HISTORY = 20
    
    def __init__(self, user_data_path: str):
        self.user_data_path = Path(user_data_path)
        self.history_file = self.user_data_path / "settings" / "find_replace_history.json"
        self.find_history: List[str] = []
        self.replace_history: List[str] = []
        self._load()
    
    def _load(self):
        """Load history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.find_history = data.get('find', [])[:self.MAX_HISTORY]
                    self.replace_history = data.get('replace', [])[:self.MAX_HISTORY]
            except Exception:
                pass
    
    def _save(self):
        """Save history to file."""
        try:
            self.user_data_path.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'find': self.find_history[:self.MAX_HISTORY],
                    'replace': self.replace_history[:self.MAX_HISTORY]
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def add_find(self, text: str):
        """Add a find term to history."""
        if not text or not text.strip():
            return
        text = text.strip()
        # Remove if exists, add to front
        if text in self.find_history:
            self.find_history.remove(text)
        self.find_history.insert(0, text)
        self.find_history = self.find_history[:self.MAX_HISTORY]
        self._save()
    
    def add_replace(self, text: str):
        """Add a replace term to history."""
        if text is None:
            return
        text = text.strip() if text else ""
        # Remove if exists, add to front
        if text in self.replace_history:
            self.replace_history.remove(text)
        self.replace_history.insert(0, text)
        self.replace_history = self.replace_history[:self.MAX_HISTORY]
        self._save()
    
    def add_operation(self, find_text: str, replace_text: str):
        """Add both find and replace terms."""
        self.add_find(find_text)
        self.add_replace(replace_text)


@dataclass
class FindReplaceOperation:
    """Single find/replace operation with all settings."""
    find_text: str
    replace_text: str = ""
    search_in: str = "target"  # "source", "target", "both"
    match_mode: int = 0  # 0=anything, 1=whole words, 2=entire segment
    case_sensitive: bool = False
    enabled: bool = True
    auto_case: bool = False  # Auto-adjust replacement to match case pattern of matched text

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'FindReplaceOperation':
        # Accept old saved sets that lack newer fields (forward-compatible defaults)
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered)


@dataclass
class FindReplaceSet:
    """Collection of F&R operations that can be saved/loaded."""
    name: str
    operations: List[FindReplaceOperation] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'operations': [op.to_dict() for op in self.operations]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FindReplaceSet':
        ops = [FindReplaceOperation.from_dict(op) for op in data.get('operations', [])]
        return cls(name=data.get('name', 'Unnamed Set'), operations=ops)
    
    def add_operation(self, op: FindReplaceOperation):
        self.operations.append(op)
    
    def remove_operation(self, index: int):
        if 0 <= index < len(self.operations):
            del self.operations[index]


class HistoryComboBox(QComboBox):
    """Editable combo box with history dropdown."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setCompleter(None)  # Disable auto-complete (fixes #163: uppercase history overwriting lowercase input)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.setMaxVisibleItems(15)
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.setMinimumWidth(200)
    
    def set_history(self, history: List[str]):
        """Update the dropdown items with history."""
        current_text = self.currentText()
        self.clear()
        self.addItems(history)
        self.setCurrentText(current_text)
    
    def text(self) -> str:
        """Get current text (convenience method)."""
        return self.currentText()
    
    def setText(self, text: str):
        """Set current text (convenience method)."""
        self.setCurrentText(text)


class FindReplaceSetsManager(QWidget):
    """UI widget for managing F&R sets."""
    
    # Signals
    operation_selected = pyqtSignal(object)  # Emits FindReplaceOperation
    run_set_requested = pyqtSignal(object)   # Emits FindReplaceSet
    set_selected = pyqtSignal(object)        # Emits FindReplaceSet for batch run
    
    def __init__(self, user_data_path: str, parent=None):
        super().__init__(parent)
        self.user_data_path = Path(user_data_path)
        self.sets_dir = self.user_data_path / "find_replace_sets"
        self.sets_dir.mkdir(parents=True, exist_ok=True)
        
        self.sets: List[FindReplaceSet] = []
        self.current_set: Optional[FindReplaceSet] = None
        
        self._setup_ui()
        self._load_sets()
        self._refresh_sets_table()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 0)
        
        # Horizontal splitter for sets list and operations
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Saved F&R Sets
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 5, 0)
        
        left_layout.addWidget(QLabel("<b>📁 Saved F&R Sets</b>"))
        
        self.sets_table = QTableWidget()
        self.sets_table.setColumnCount(2)
        self.sets_table.setHorizontalHeaderLabels(["Name", "Operations"])
        self.sets_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.sets_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.sets_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.sets_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.sets_table.itemSelectionChanged.connect(self._on_set_selected)
        left_layout.addWidget(self.sets_table)
        
        # Sets buttons
        sets_btn_layout = QHBoxLayout()
        
        new_set_btn = QPushButton("+ New Set")
        new_set_btn.clicked.connect(self._create_new_set)
        sets_btn_layout.addWidget(new_set_btn)
        
        import_btn = QPushButton("📥 Import")
        import_btn.clicked.connect(self._import_set)
        sets_btn_layout.addWidget(import_btn)
        
        left_layout.addLayout(sets_btn_layout)
        
        splitter.addWidget(left_widget)
        
        # Right side: Operations in selected set
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 0, 0, 0)
        
        self.ops_label = QLabel("<b>📋 Operations in: (none selected)</b>")
        right_layout.addWidget(self.ops_label)
        
        self.ops_table = QTableWidget()
        self.ops_table.setColumnCount(5)
        self.ops_table.setHorizontalHeaderLabels(["✓", "Find", "Replace", "Search in", "Match"])
        self.ops_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.ops_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.ops_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.ops_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.ops_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.ops_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ops_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ops_table.cellDoubleClicked.connect(self._on_op_double_clicked)
        self.ops_table.cellChanged.connect(self._on_op_cell_changed)
        right_layout.addWidget(self.ops_table)
        
        # Operations buttons
        ops_btn_layout = QHBoxLayout()
        
        add_op_btn = QPushButton("+ Add Operation")
        add_op_btn.clicked.connect(self._add_empty_operation)
        ops_btn_layout.addWidget(add_op_btn)
        
        ops_btn_layout.addStretch()
        
        run_all_btn = QPushButton("▶ Run All")
        run_all_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        run_all_btn.clicked.connect(self._run_all_operations)
        ops_btn_layout.addWidget(run_all_btn)
        
        right_layout.addLayout(ops_btn_layout)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 500])
        
        layout.addWidget(splitter)
    
    def _load_sets(self):
        """Load all F&R sets from the sets directory."""
        self.sets = []
        for file_path in self.sets_dir.glob("*.svfr"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    fr_set = FindReplaceSet.from_dict(data)
                    self.sets.append(fr_set)
            except Exception:
                pass
        
        # If no sets exist, create a default one
        if not self.sets:
            default_set = FindReplaceSet(name="F&R Set 1")
            self.sets.append(default_set)
            self._save_set(default_set)
    
    def _save_set(self, fr_set: FindReplaceSet):
        """Save a F&R set to file."""
        safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in fr_set.name)
        file_path = self.sets_dir / f"{safe_name}.svfr"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(fr_set.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving F&R set: {e}")
    
    def _refresh_sets_table(self):
        """Refresh the sets table."""
        self.sets_table.setRowCount(len(self.sets))
        for i, fr_set in enumerate(self.sets):
            name_item = QTableWidgetItem(fr_set.name)
            name_item.setForeground(QColor("#1976D2"))  # Blue color for names
            self.sets_table.setItem(i, 0, name_item)
            
            count_item = QTableWidgetItem(str(len(fr_set.operations)))
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.sets_table.setItem(i, 1, count_item)
        
        # Select first set if none selected
        if self.sets and not self.current_set:
            self.sets_table.selectRow(0)
    
    def _refresh_ops_table(self):
        """Refresh the operations table for the current set."""
        self.ops_table.blockSignals(True)
        
        if not self.current_set:
            self.ops_table.setRowCount(0)
            self.ops_label.setText("<b>📋 Operations in: (none selected)</b>")
            self.ops_table.blockSignals(False)
            return
        
        self.ops_label.setText(f"<b>📋 Operations in: {self.current_set.name}</b>")
        self.ops_table.setRowCount(len(self.current_set.operations))
        
        for i, op in enumerate(self.current_set.operations):
            # Enabled checkbox
            enabled_item = QTableWidgetItem("✓" if op.enabled else "")
            enabled_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            enabled_item.setFlags(enabled_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            enabled_item.setCheckState(Qt.CheckState.Checked if op.enabled else Qt.CheckState.Unchecked)
            self.ops_table.setItem(i, 0, enabled_item)
            
            # Find text
            find_item = QTableWidgetItem(op.find_text)
            self.ops_table.setItem(i, 1, find_item)
            
            # Replace text
            replace_item = QTableWidgetItem(op.replace_text)
            self.ops_table.setItem(i, 2, replace_item)
            
            # Search in - full text
            search_in_map = {"source": "Source", "target": "Target", "both": "Both"}
            search_item = QTableWidgetItem(search_in_map.get(op.search_in, "Target"))
            self.ops_table.setItem(i, 3, search_item)
            
            # Match mode - full text
            match_map = {0: "Anything", 1: "Whole words", 2: "Entire segment"}
            match_item = QTableWidgetItem(match_map.get(op.match_mode, "Anything"))
            self.ops_table.setItem(i, 4, match_item)
        
        self.ops_table.blockSignals(False)
    
    def _on_set_selected(self):
        """Handle set selection in the sets table."""
        selected_rows = self.sets_table.selectionModel().selectedRows()
        if selected_rows:
            index = selected_rows[0].row()
            if 0 <= index < len(self.sets):
                self.current_set = self.sets[index]
                self._refresh_ops_table()
    
    def _on_op_double_clicked(self, row: int, col: int):
        """Handle double-click on an operation to load it into the dialog."""
        if self.current_set and 0 <= row < len(self.current_set.operations):
            op = self.current_set.operations[row]
            self.operation_selected.emit(op)
    
    def _on_op_cell_changed(self, row: int, col: int):
        """Handle cell changes in the operations table."""
        if not self.current_set or row >= len(self.current_set.operations):
            return
        
        op = self.current_set.operations[row]
        item = self.ops_table.item(row, col)
        
        if col == 0:  # Enabled checkbox
            op.enabled = item.checkState() == Qt.CheckState.Checked
        elif col == 1:  # Find text
            op.find_text = item.text()
        elif col == 2:  # Replace text
            op.replace_text = item.text()
        
        self._save_set(self.current_set)
    
    def _create_new_set(self):
        """Create a new F&R set."""
        name, ok = QInputDialog.getText(self, "New F&R Set", "Enter set name:")
        if ok and name.strip():
            new_set = FindReplaceSet(name=name.strip())
            self.sets.append(new_set)
            self._save_set(new_set)
            self._refresh_sets_table()
            # Select the new set
            self.sets_table.selectRow(len(self.sets) - 1)
    
    def _import_set(self):
        """Import a F&R set from a .svfr file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import F&R Set", "", "Supervertaler F&R Sets (*.svfr);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    fr_set = FindReplaceSet.from_dict(data)
                    self.sets.append(fr_set)
                    self._save_set(fr_set)
                    self._refresh_sets_table()
                    QMessageBox.information(self, "Import", f"Imported '{fr_set.name}' with {len(fr_set.operations)} operations.")
            except Exception as e:
                QMessageBox.warning(self, "Import Error", f"Failed to import: {e}")
    
    def _add_empty_operation(self):
        """Add an empty operation to the current set."""
        if not self.current_set:
            QMessageBox.information(self, "No Set", "Please select or create a F&R set first.")
            return
        
        op = FindReplaceOperation(find_text="", replace_text="")
        self.current_set.add_operation(op)
        self._save_set(self.current_set)
        self._refresh_ops_table()
        self._refresh_sets_table()  # Update operation count
    
    def _run_all_operations(self):
        """Request to run all enabled operations in the current set."""
        if not self.current_set:
            return
        
        enabled_ops = [op for op in self.current_set.operations if op.enabled and op.find_text]
        if not enabled_ops:
            QMessageBox.information(self, "Run All", "No enabled operations with find text.")
            return
        
        self.set_selected.emit(self.current_set)
    
    def add_current_operation_to_set(self, op: FindReplaceOperation):
        """Add an operation to the current set (called from main dialog)."""
        if not self.current_set:
            # Create a default set if none exists
            if not self.sets:
                self._create_new_set()
            if self.sets:
                self.current_set = self.sets[0]
                self.sets_table.selectRow(0)
        
        if self.current_set:
            self.current_set.add_operation(op)
            self._save_set(self.current_set)
            self._refresh_ops_table()
            self._refresh_sets_table()  # Update operation count
