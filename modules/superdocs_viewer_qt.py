"""
Deprecated Superdocs viewer module.

The in-app Superdocs viewer was removed in favor of the online GitBook documentation.
This file is kept as a small shim to prevent import-time crashes in older packaged builds.
"""

def __getattr__(name):
    raise ImportError(
        "The 'modules.superdocs_viewer_qt' module has been removed. Visit https://supervertaler.gitbook.io/superdocs/ for documentation."
    )
        self.open_external_btn.clicked.connect(self.open_in_external_editor)
        self.open_external_btn.setEnabled(False)
        title_bar_layout.addWidget(self.open_external_btn)

        viewer_layout.addLayout(title_bar_layout)

        # Markdown viewer
        self.doc_viewer = QTextBrowser()
        self.doc_viewer.setOpenExternalLinks(False)
        self.doc_viewer.anchorClicked.connect(self.on_link_clicked)
        viewer_layout.addWidget(self.doc_viewer)  # This gets all the stretch

        splitter.addWidget(viewer_widget)

        # Set splitter proportions (25% tree, 75% viewer for more reading space)
        splitter.setSizes([250, 750])

        main_layout.addWidget(splitter, 1)  # 1 = stretch to fill available space

    def load_documentation_tree(self):
        """Load documentation structure into tree view"""
        self.doc_tree.clear()

        if not self.docs_dir.exists():
            self.status_label.setText("⚠ Documentation not generated yet. Click 'Generate Documentation' to create it.")
            self.stats_label.setText("No documentation files found")
            return

        # Add root-level documents
        root_files = ["index.md", "architecture.md", "dependencies.md"]
        file_count = 0

        for filename in root_files:
            file_path = self.docs_dir / filename
            if file_path.exists():
                icon = "📄"
                if filename == "index.md":
                    icon = "🏠"
                elif filename == "architecture.md":
                    icon = "🏗"
                elif filename == "dependencies.md":
                    icon = "🔗"

                item = QTreeWidgetItem([f"{icon} {filename[:-3].title()}"])
                item.setData(0, Qt.ItemDataRole.UserRole, str(file_path))
                self.doc_tree.addTopLevelItem(item)
                file_count += 1

        # Add modules folder
        modules_dir = self.docs_dir / "modules"
        if modules_dir.exists():
            modules_item = QTreeWidgetItem(["📁 Modules"])
            self.doc_tree.addTopLevelItem(modules_item)

            # Add all module documentation files
            module_files = sorted(modules_dir.glob("*.md"))
            for module_file in module_files:
                item = QTreeWidgetItem([f"📄 {module_file.stem}"])
                item.setData(0, Qt.ItemDataRole.UserRole, str(module_file))
                modules_item.addChild(item)
                file_count += 1

            modules_item.setExpanded(True)

        # Update stats
        self.stats_label.setText(f"📊 {file_count} documentation files")
        self.status_label.setText(f"Documentation loaded - Last generated: {self.get_last_generation_time()}")

        # Auto-select index if available
        if self.doc_tree.topLevelItemCount() > 0:
            first_item = self.doc_tree.topLevelItem(0)
            self.doc_tree.setCurrentItem(first_item)
            self.on_tree_item_clicked(first_item, 0)

    def get_last_generation_time(self):
        """Get timestamp of last documentation generation"""
        index_file = self.docs_dir / "index.md"
        if index_file.exists():
            timestamp = datetime.fromtimestamp(index_file.stat().st_mtime)
            return timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return "Unknown"

    def on_tree_item_clicked(self, item, column):
        """Handle tree item click - load and display document"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)

        if not file_path:
            return

        self.current_file = Path(file_path)
        self.load_document(self.current_file)

    def load_document(self, file_path):
        """Load and display markdown document"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            # Convert markdown to HTML
            html_content = markdown.markdown(
                markdown_content,
                extensions=['extra', 'codehilite', 'tables', 'fenced_code']
            )

            # Add CSS styling for better readability
            styled_html = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                        line-height: 1.6;
                        padding: 20px;
                        color: #333;
                    }}
                    h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                    h2 {{ color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; margin-top: 30px; }}
                    h3 {{ color: #555; margin-top: 20px; }}
                    code {{
                        background-color: #f4f4f4;
                        padding: 2px 6px;
                        border-radius: 3px;
                        font-family: "Courier New", monospace;
                    }}
                    pre {{
                        background-color: #f8f8f8;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        padding: 15px;
                        overflow-x: auto;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 20px 0;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 12px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #3498db;
                        color: white;
                    }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    a {{ color: #3498db; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                    blockquote {{
                        border-left: 4px solid #3498db;
                        padding-left: 15px;
                        color: #666;
                        font-style: italic;
                    }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """

            self.doc_viewer.setHtml(styled_html)
            self.doc_title_label.setText(f"📄 {file_path.stem}")
            self.open_external_btn.setEnabled(True)

            # Update word count
            word_count = len(markdown_content.split())
            self.word_count_label.setText(f"📝 {word_count:,} words")

        except Exception as e:
            self.doc_viewer.setPlainText(f"Error loading document: {e}")
            self.doc_title_label.setText("Error")
            self.open_external_btn.setEnabled(False)

    def on_link_clicked(self, url):
        """Handle clicks on internal documentation links"""
        url_str = url.toString()

        # Handle relative links to other documentation files
        if url_str.endswith('.md'):
            target_file = self.docs_dir / url_str
            if target_file.exists():
                self.load_document(target_file)
                # Update tree selection
                self.select_tree_item_by_path(target_file)
        else:
            # External links - open in browser
            import webbrowser
            webbrowser.open(url_str)

    def select_tree_item_by_path(self, file_path):
        """Select tree item by file path"""
        iterator = QTreeWidgetItem(self.doc_tree.invisibleRootItem())
        for i in range(self.doc_tree.topLevelItemCount()):
            item = self.doc_tree.topLevelItem(i)
            if self._check_item_path(item, file_path):
                return

    def _check_item_path(self, item, target_path):
        """Recursively check item and children for matching path"""
        item_path = item.data(0, Qt.ItemDataRole.UserRole)
        if item_path and Path(item_path) == target_path:
            self.doc_tree.setCurrentItem(item)
            return True

        for i in range(item.childCount()):
            if self._check_item_path(item.child(i), target_path):
                return True

        return False

    def open_in_external_editor(self):
        """Open current document in external editor"""
        if not self.current_file or not self.current_file.exists():
            return

        import subprocess
        import sys

        try:
            if sys.platform == 'win32':
                subprocess.run(['start', '', str(self.current_file)], shell=True)
            elif sys.platform == 'darwin':
                subprocess.run(['open', str(self.current_file)])
            else:
                subprocess.run(['xdg-open', str(self.current_file)])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open file in external editor: {e}")

    def generate_documentation(self):
        """Generate documentation in background thread"""
        if self.generator_thread and self.generator_thread.isRunning():
            QMessageBox.information(self, "In Progress", "Documentation generation is already running.")
            return

        # Confirm action
        reply = QMessageBox.question(
            self,
            "Generate Documentation",
            "This will scan the entire codebase and regenerate all documentation files.\n\n"
            "This may take a few moments. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Disable buttons during generation
        self.generate_btn.setEnabled(False)
        self.refresh_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress

        # Start generation thread
        self.generator_thread = SuperdocsGeneratorThread()
        self.generator_thread.progress.connect(self.on_generation_progress)
        self.generator_thread.finished.connect(self.on_generation_finished)
        self.generator_thread.start()

    def on_generation_progress(self, message):
        """Update progress status"""
        self.status_label.setText(f"⏳ {message}")
        self.progress_bar.setFormat(message)

    def on_generation_finished(self, success, message):
        """Handle generation completion"""
        # Re-enable buttons
        self.generate_btn.setEnabled(True)
        self.refresh_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            self.status_label.setText(f"✅ {message}")
            QMessageBox.information(self, "Success", message)
            # Reload documentation tree
            self.load_documentation_tree()
        else:
            self.status_label.setText(f"❌ {message}")
            QMessageBox.critical(self, "Error", message)

        self.generator_thread = None


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
