"""
Translation Memory Manager for Supervertaler Qt
Provides comprehensive TM management features:
- Browse all TM entries
- Concordance search
- Import/Export TMX files
- Delete entries
- View statistics
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                              QTableWidget, QTableWidgetItem, QLineEdit, QPushButton,
                              QLabel, QMessageBox, QFileDialog, QHeaderView,
                              QGroupBox, QTextEdit, QComboBox, QSpinBox, QCheckBox,
                              QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QFont
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Callable


class TMXImportThread(QThread):
    """Background thread for importing TMX files"""
    progress = pyqtSignal(int, str)  # progress percentage, status message
    finished = pyqtSignal(bool, str, int)  # success, message, entries_imported
    
    def __init__(self, tmx_path: str, db_manager, source_lang: str, target_lang: str, tm_id: str = 'imported'):
        super().__init__()
        self.tmx_path = tmx_path
        self.db_manager = db_manager
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.tm_id = tm_id
    
    def run(self):
        """Import TMX file in background"""
        try:
            tree = ET.parse(self.tmx_path)
            root = tree.getroot()
            
            # Find body element
            body = root.find('.//body')
            if body is None:
                self.finished.emit(False, "Invalid TMX file: no body element found", 0)
                return
            
            # Get all translation units
            tus = body.findall('tu')
            total = len(tus)
            imported = 0
            
            for idx, tu in enumerate(tus):
                # Extract source and target
                tuvs = tu.findall('tuv')
                if len(tuvs) < 2:
                    continue
                
                source_text = None
                target_text = None
                
                for tuv in tuvs:
                    lang = tuv.get('{http://www.w3.org/XML/1998/namespace}lang', 
                                  tuv.get('lang', ''))
                    seg = tuv.find('seg')
                    if seg is None or seg.text is None:
                        continue
                    
                    # Simple language matching (could be improved)
                    if not source_text:
                        source_text = seg.text
                    else:
                        target_text = seg.text
                
                # Add to TM if both source and target found
                if source_text and target_text:
                    self.db_manager.add_translation_unit(
                        source=source_text,
                        target=target_text,
                        source_lang=self.source_lang,
                        target_lang=self.target_lang,
                        tm_id=self.tm_id,
                        save_mode='all'  # Always use 'all' mode for imports
                    )
                    imported += 1
                
                # Update progress every 10 entries
                if idx % 10 == 0:
                    progress_pct = int((idx / total) * 100)
                    self.progress.emit(progress_pct, f"Importing... {idx}/{total}")
            
            self.finished.emit(True, f"Successfully imported {imported} entries", imported)
            
        except Exception as e:
            self.finished.emit(False, f"Import failed: {str(e)}", 0)


class TMManagerDialog(QDialog):
    """Translation Memory Manager dialog"""
    
    def __init__(self, parent, db_manager, log_callback: Optional[Callable] = None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.log = log_callback if log_callback else lambda x: None
        self.parent_app = parent
        
        self.setWindowTitle("Translation Memory Manager")
        self.resize(1000, 700)
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        """Setup the UI with tabs"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("📚 Translation Memory Manager")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.browser_tab = self.create_browser_tab()
        self.search_tab = self.create_search_tab()
        self.import_export_tab = self.create_import_export_tab()
        self.stats_tab = self.create_stats_tab()
        
        self.tabs.addTab(self.browser_tab, "📋 Browse")
        self.tabs.addTab(self.search_tab, "🔍 Concordance")
        self.tabs.addTab(self.import_export_tab, "📥 Import/Export")
        self.tabs.addTab(self.stats_tab, "📊 Statistics")
        
        layout.addWidget(self.tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def create_browser_tab(self):
        """Create TM browser tab"""
        widget = QGroupBox()
        layout = QVBoxLayout()
        
        # Filter controls
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter:"))
        self.browser_filter = QLineEdit()
        self.browser_filter.setPlaceholderText("Type to filter entries...")
        self.browser_filter.textChanged.connect(self.filter_browser_entries)
        filter_layout.addWidget(self.browser_filter)
        
        self.browser_limit = QSpinBox()
        self.browser_limit.setRange(100, 10000)
        self.browser_limit.setValue(500)
        self.browser_limit.setSingleStep(100)
        self.browser_limit.setPrefix("Show: ")
        self.browser_limit.setSuffix(" entries")
        filter_layout.addWidget(self.browser_limit)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_browser)
        filter_layout.addWidget(refresh_btn)
        
        layout.addLayout(filter_layout)
        
        # Table
        self.browser_table = QTableWidget()
        self.browser_table.setColumnCount(6)
        self.browser_table.setHorizontalHeaderLabels([
            "ID", "Source", "Target", "TM", "Usage", "Modified"
        ])
        self.browser_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.browser_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.browser_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.browser_table.setAlternatingRowColors(True)
        layout.addWidget(self.browser_table)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        delete_btn = QPushButton("🗑️ Delete Selected")
        delete_btn.clicked.connect(self.delete_selected_entry)
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()
        
        self.browser_status = QLabel("Ready")
        btn_layout.addWidget(self.browser_status)
        
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_search_tab(self):
        """Create concordance search tab"""
        widget = QGroupBox()
        layout = QVBoxLayout()
        
        # Search controls
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter text to search in source and target...")
        self.search_input.returnPressed.connect(self.do_concordance_search)
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("🔍 Search")
        search_btn.clicked.connect(self.do_concordance_search)
        search_layout.addWidget(search_btn)
        
        layout.addLayout(search_layout)
        
        # Results display
        self.search_results = QTextEdit()
        self.search_results.setReadOnly(True)
        self.search_results.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.search_results)
        
        # Status
        self.search_status = QLabel("Enter a search term and press Search")
        layout.addWidget(self.search_status)
        
        widget.setLayout(layout)
        return widget
    
    def create_import_export_tab(self):
        """Create import/export tab"""
        widget = QGroupBox()
        layout = QVBoxLayout()
        
        # Import section
        import_group = QGroupBox("Import TMX")
        import_layout = QVBoxLayout()
        
        import_info = QLabel(
            "Import translation units from a TMX file into your database.\n"
            "All entries will be added to a new TM or merged with an existing one."
        )
        import_info.setWordWrap(True)
        import_layout.addWidget(import_info)
        
        import_controls = QHBoxLayout()
        import_controls.addWidget(QLabel("TM ID:"))
        self.import_tm_id = QLineEdit("imported")
        self.import_tm_id.setPlaceholderText("Enter TM identifier")
        import_controls.addWidget(self.import_tm_id)
        
        import_btn = QPushButton("📂 Select and Import TMX...")
        import_btn.clicked.connect(self.import_tmx)
        import_controls.addWidget(import_btn)
        import_layout.addLayout(import_controls)
        
        self.import_progress = QProgressBar()
        self.import_progress.setVisible(False)
        import_layout.addWidget(self.import_progress)
        
        self.import_status = QLabel("")
        import_layout.addWidget(self.import_status)
        
        import_group.setLayout(import_layout)
        layout.addWidget(import_group)
        
        # Export section
        export_group = QGroupBox("Export TMX")
        export_layout = QVBoxLayout()
        
        export_info = QLabel(
            "Export your translation memory to a standard TMX file.\n"
            "The TMX file can be used in other CAT tools or shared with colleagues."
        )
        export_info.setWordWrap(True)
        export_layout.addWidget(export_info)
        
        export_controls = QHBoxLayout()
        export_controls.addWidget(QLabel("TM to export:"))
        self.export_tm_selector = QComboBox()
        self.export_tm_selector.addItem("All TMs", "all")
        self.export_tm_selector.addItem("Project TM only", "project")
        export_controls.addWidget(self.export_tm_selector)
        
        export_btn = QPushButton("💾 Export to TMX...")
        export_btn.clicked.connect(self.export_tmx)
        export_controls.addWidget(export_btn)
        export_layout.addLayout(export_controls)
        
        self.export_status = QLabel("")
        export_layout.addWidget(self.export_status)
        
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_stats_tab(self):
        """Create statistics tab"""
        widget = QGroupBox()
        layout = QVBoxLayout()
        
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        self.stats_display.setFont(QFont("Courier New", 10))
        layout.addWidget(self.stats_display)
        
        refresh_btn = QPushButton("🔄 Refresh Statistics")
        refresh_btn.clicked.connect(self.refresh_stats)
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)
        return widget
    
    def load_initial_data(self):
        """Load initial data for all tabs"""
        self.refresh_browser()
        self.refresh_stats()
    
    def refresh_browser(self):
        """Refresh the TM browser table"""
        try:
            limit = self.browser_limit.value()
            filter_text = self.browser_filter.text().strip()
            
            # Get entries from database
            if filter_text:
                entries = self.db_manager.concordance_search(filter_text)
            else:
                # Get recent entries
                self.db_manager.cursor.execute(f"""
                    SELECT * FROM translation_units 
                    ORDER BY modified_date DESC 
                    LIMIT {limit}
                """)
                entries = [dict(row) for row in self.db_manager.cursor.fetchall()]
            
            # Populate table
            self.browser_table.setRowCount(len(entries))
            for row, entry in enumerate(entries):
                self.browser_table.setItem(row, 0, QTableWidgetItem(str(entry['id'])))
                self.browser_table.setItem(row, 1, QTableWidgetItem(entry['source_text'][:100]))
                self.browser_table.setItem(row, 2, QTableWidgetItem(entry['target_text'][:100]))
                self.browser_table.setItem(row, 3, QTableWidgetItem(entry['tm_id']))
                self.browser_table.setItem(row, 4, QTableWidgetItem(str(entry.get('usage_count', 0))))
                self.browser_table.setItem(row, 5, QTableWidgetItem(entry.get('modified_date', '')[:16]))
            
            self.browser_status.setText(f"Showing {len(entries)} entries")
            self.log(f"TM Browser: Loaded {len(entries)} entries")
            
        except Exception as e:
            self.browser_status.setText(f"Error: {str(e)}")
            self.log(f"Error refreshing TM browser: {e}")
    
    def filter_browser_entries(self):
        """Filter browser entries as user types"""
        # Auto-refresh on filter change (with debouncing in real implementation)
        pass
    
    def delete_selected_entry(self):
        """Delete the selected TM entry"""
        selected_rows = self.browser_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select an entry to delete")
            return
        
        row = self.browser_table.currentRow()
        entry_id = int(self.browser_table.item(row, 0).text())
        source = self.browser_table.item(row, 1).text()
        target = self.browser_table.item(row, 2).text()
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Delete this TM entry?\n\nSource: {source}\nTarget: {target}\n\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_manager.cursor.execute("DELETE FROM translation_units WHERE id = ?", (entry_id,))
                self.db_manager.connection.commit()
                self.log(f"Deleted TM entry {entry_id}")
                self.refresh_browser()
                QMessageBox.information(self, "Success", "Entry deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete entry: {str(e)}")
    
    def do_concordance_search(self):
        """Perform concordance search"""
        query = self.search_input.text().strip()
        if not query:
            self.search_status.setText("Please enter a search term")
            return
        
        try:
            results = self.db_manager.concordance_search(query)
            
            # Display results
            self.search_results.clear()
            html = f"<h3>Found {len(results)} matches for '{query}'</h3>"
            
            for idx, match in enumerate(results, 1):
                source_highlighted = match['source_text'].replace(
                    query, f"<span style='background-color: yellow;'>{query}</span>"
                )
                target_highlighted = match['target_text'].replace(
                    query, f"<span style='background-color: yellow;'>{query}</span>"
                )
                
                html += f"""
                <div style='border: 1px solid #ccc; padding: 10px; margin: 10px 0;'>
                    <p><strong>#{idx}</strong> - TM: {match['tm_id']} - Used: {match.get('usage_count', 0)} times</p>
                    <p><strong>Source:</strong> {source_highlighted}</p>
                    <p><strong>Target:</strong> {target_highlighted}</p>
                    <p style='color: #888; font-size: 9pt;'>Modified: {match.get('modified_date', 'N/A')}</p>
                </div>
                """
            
            self.search_results.setHtml(html)
            self.search_status.setText(f"Found {len(results)} matches")
            self.log(f"Concordance search: {len(results)} matches for '{query}'")
            
        except Exception as e:
            self.search_status.setText(f"Error: {str(e)}")
            self.log(f"Error in concordance search: {e}")
    
    def import_tmx(self):
        """Import a TMX file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select TMX File", "",
            "TMX Files (*.tmx);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        tm_id = self.import_tm_id.text().strip() or "imported"
        
        # Get source and target languages from parent app
        if hasattr(self.parent_app, 'current_project'):
            source_lang = self.parent_app.current_project.source_lang
            target_lang = self.parent_app.current_project.target_lang
        else:
            source_lang = "en"
            target_lang = "de"
        
        # Show progress bar
        self.import_progress.setValue(0)
        self.import_progress.setVisible(True)
        self.import_status.setText("Importing...")
        
        # Start import thread
        self.import_thread = TMXImportThread(file_path, self.db_manager, source_lang, target_lang, tm_id)
        self.import_thread.progress.connect(self.on_import_progress)
        self.import_thread.finished.connect(self.on_import_finished)
        self.import_thread.start()
    
    def on_import_progress(self, percent, message):
        """Update import progress"""
        self.import_progress.setValue(percent)
        self.import_status.setText(message)
    
    def on_import_finished(self, success, message, count):
        """Import finished"""
        self.import_progress.setVisible(False)
        self.import_status.setText(message)
        
        if success:
            QMessageBox.information(self, "Import Complete", f"{message}\n\nTotal entries: {count}")
            self.refresh_browser()
            self.refresh_stats()
        else:
            QMessageBox.critical(self, "Import Failed", message)
    
    def export_tmx(self):
        """Export TM to TMX file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save TMX File", "",
            "TMX Files (*.tmx);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            tm_filter = self.export_tm_selector.currentData()
            
            # Get entries to export
            if tm_filter == "all":
                self.db_manager.cursor.execute("SELECT * FROM translation_units")
            else:
                self.db_manager.cursor.execute("SELECT * FROM translation_units WHERE tm_id = ?", (tm_filter,))
            
            entries = [dict(row) for row in self.db_manager.cursor.fetchall()]
            
            if not entries:
                QMessageBox.warning(self, "No Entries", "No translation units to export")
                return
            
            # Create TMX
            tmx = ET.Element('tmx')
            tmx.set('version', '1.4')
            
            header = ET.SubElement(tmx, 'header')
            header.set('creationdate', datetime.now().strftime('%Y%m%dT%H%M%SZ'))
            header.set('srclang', 'en')
            header.set('adminlang', 'en')
            header.set('segtype', 'sentence')
            header.set('creationtool', 'Supervertaler')
            header.set('creationtoolversion', '4.0')
            header.set('datatype', 'plaintext')
            
            body = ET.SubElement(tmx, 'body')
            
            for entry in entries:
                tu = ET.SubElement(body, 'tu')
                
                # Source
                tuv_src = ET.SubElement(tu, 'tuv')
                tuv_src.set('xml:lang', entry.get('source_lang', 'en'))
                seg_src = ET.SubElement(tuv_src, 'seg')
                seg_src.text = entry['source_text']
                
                # Target
                tuv_tgt = ET.SubElement(tu, 'tuv')
                tuv_tgt.set('xml:lang', entry.get('target_lang', 'de'))
                seg_tgt = ET.SubElement(tuv_tgt, 'seg')
                seg_tgt.text = entry['target_text']
            
            # Write to file
            tree = ET.ElementTree(tmx)
            ET.indent(tree, space="  ")
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            
            self.export_status.setText(f"Exported {len(entries)} entries to {Path(file_path).name}")
            QMessageBox.information(self, "Export Complete", 
                                   f"Successfully exported {len(entries)} translation units")
            self.log(f"Exported {len(entries)} entries to {file_path}")
            
        except Exception as e:
            self.export_status.setText(f"Error: {str(e)}")
            QMessageBox.critical(self, "Export Failed", f"Failed to export TMX:\n{str(e)}")
            self.log(f"Error exporting TMX: {e}")
    
    def refresh_stats(self):
        """Refresh TM statistics"""
        try:
            # Get various statistics
            self.db_manager.cursor.execute("SELECT COUNT(*) FROM translation_units")
            total_entries = self.db_manager.cursor.fetchone()[0]
            
            self.db_manager.cursor.execute("SELECT COUNT(DISTINCT tm_id) FROM translation_units")
            tm_count = self.db_manager.cursor.fetchone()[0]
            
            self.db_manager.cursor.execute("""
                SELECT tm_id, COUNT(*) as count 
                FROM translation_units 
                GROUP BY tm_id 
                ORDER BY count DESC
            """)
            tm_breakdown = self.db_manager.cursor.fetchall()
            
            self.db_manager.cursor.execute("""
                SELECT AVG(LENGTH(source_text)), AVG(LENGTH(target_text))
                FROM translation_units
            """)
            avg_lengths = self.db_manager.cursor.fetchone()
            
            # Format statistics
            stats_text = f"""
═══════════════════════════════════════════════
  TRANSLATION MEMORY STATISTICS
═══════════════════════════════════════════════

Total Translation Units: {total_entries:,}
Number of TMs: {tm_count}

Average Source Length: {avg_lengths[0]:.1f} characters
Average Target Length: {avg_lengths[1]:.1f} characters

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BREAKDOWN BY TM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
            for tm_id, count in tm_breakdown:
                pct = (count / total_entries * 100) if total_entries > 0 else 0
                stats_text += f"{tm_id:20s} {count:8,} entries ({pct:5.1f}%)\n"
            
            self.stats_display.setPlainText(stats_text)
            self.log("TM statistics refreshed")
            
        except Exception as e:
            self.stats_display.setPlainText(f"Error loading statistics:\n{str(e)}")
            self.log(f"Error refreshing stats: {e}")
