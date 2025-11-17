"""
TM Editor Dialog - Edit a specific Translation Memory

This dialog provides comprehensive editing for a single TM:
- Browse entries
- Concordance search
- Statistics
- Import/Export (scoped to this TM)
- Maintenance

Similar to TMManagerDialog but scoped to a specific tm_id.
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTabWidget, QWidget, QPushButton)
from PyQt6.QtCore import Qt

# Import the existing TM Manager tabs
from modules.tm_manager_qt import TMManagerDialog


class TMEditorDialog(QDialog):
    """TM Editor for a specific translation memory"""
    
    def __init__(self, parent, db_manager, log_callback, tm_id: str, tm_name: str):
        """
        Initialize TM Editor
        
        Args:
            parent: Parent widget
            db_manager: DatabaseManager instance
            log_callback: Logging function
            tm_id: The tm_id to edit
            tm_name: Display name of the TM
        """
        super().__init__(parent)
        self.db_manager = db_manager
        self.log = log_callback
        self.tm_id = tm_id
        self.tm_name = tm_name
        
        self.setWindowTitle(f"TM Editor - {tm_name}")
        self.setMinimumSize(1000, 700)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI - tabs for editing a specific TM"""
        layout = QVBoxLayout(self)
        
        # Header showing which TM is being edited
        header = QLabel(f"📝 Editing: {self.tm_name}")
        header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            background-color: #e3f2fd;
            border-radius: 4px;
            margin-bottom: 10px;
        """)
        layout.addWidget(header)
        
        # Info about TM
        from modules.tm_metadata_manager import TMMetadataManager
        tm_metadata_mgr = TMMetadataManager(self.db_manager, self.log)
        tm_info = tm_metadata_mgr.get_tm_by_tm_id(self.tm_id)
        
        if tm_info:
            info_text = f"TM ID: {self.tm_id} | Languages: {tm_info['source_lang'] or '?'} → {tm_info['target_lang'] or '?'} | Entries: {tm_info['entry_count']}"
            info_label = QLabel(info_text)
            info_label.setStyleSheet("color: #666; font-size: 11px; padding: 5px; margin-bottom: 10px;")
            layout.addWidget(info_label)
        
        # Create nested TM Manager for this specific TM
        tm_manager = TMManagerDialog(self, self.db_manager, self.log, tm_ids=[self.tm_id])
        
        # Create tab widget with only relevant tabs for editing a specific TM
        tabs = QTabWidget()
        
        # Tab 1: Browse (this TM only)
        tabs.addTab(tm_manager.browser_tab, "📖 Browse Entries")
        
        # Tab 2: Import/Export (this TM only)
        tabs.addTab(tm_manager.import_export_tab, "📥 Import/Export")
        
        # Tab 3: Statistics (this TM only)
        tabs.addTab(tm_manager.stats_tab, "📊 Statistics")
        
        # Tab 4: Maintenance (this TM only)
        tabs.addTab(tm_manager.maintenance_tab, "🧹 Maintenance")
        
        # Store reference to prevent garbage collection
        self._tm_manager = tm_manager
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
