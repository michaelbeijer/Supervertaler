"""
Prompt Manager Module - Qt Edition
4-Layer Prompt Architecture for maximum translation/proofreading/copywriting precision

Layers:
1. System Prompts (hardcoded - always included: memoQ tags, formatting rules)
2. Domain Prompts (domain-specific translation prompts)
3. Project Prompts (project-specific rules)
4. Style Guides (language-specific formatting guidelines)
5. Prompt Assistant (AI-powered prompt refinement)

This module can be embedded in the main Supervertaler Qt application as a tab.
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem,
    QComboBox, QTextEdit, QPlainTextEdit, QSplitter, QTabWidget, QGroupBox,
    QMessageBox, QFileDialog, QInputDialog, QLineEdit, QListWidget, QListWidgetItem,
    QFrame, QDialog, QDialogButtonBox, QApplication
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QFont, QColor

from modules.prompt_library import PromptLibrary
from modules.style_guide_manager import StyleGuideLibrary


class PromptManagerQt:
    """
    Prompt Manager feature - manage System Prompts, Domain Prompts, Project Prompts, and Style Guides
    Can be embedded in any PyQt6 application as a tab or panel
    """
    
    def __init__(self, parent_app, standalone=False):
        """
        Initialize Prompt Manager module
        
        Args:
            parent_app: Reference to the main application (needs .user_data_path, .log() method)
            standalone: If True, running as standalone app. If False, embedded in Supervertaler
        """
        self.parent_app = parent_app
        self.standalone = standalone
        
        # Get user data path from parent app
        if hasattr(parent_app, 'user_data_path'):
            self.user_data_path = Path(parent_app.user_data_path)
        else:
            # Fallback
            self.user_data_path = Path("user data")
        
        # Initialize logging
        self.log = parent_app.log if hasattr(parent_app, 'log') else print
        
        # Helper for QMessageBox (PyQt6 uses instances, not static methods)
        self._msg_box = None
        
        # Initialize prompt library
        # Note: Directory names kept for backward compatibility, but content maps to new terminology:
        # - System_prompts folder → contains Layer 2: Domain Prompts
        # - Custom_instructions folder → contains Layer 3: Project Prompts
        system_prompts_dir = self.user_data_path / "Prompt_Library" / "System_prompts"
        custom_instructions_dir = self.user_data_path / "Prompt_Library" / "Custom_instructions"
        
        self.prompt_library = PromptLibrary(
            system_prompts_dir=str(system_prompts_dir),
            custom_instructions_dir=str(custom_instructions_dir),
            log_callback=self.log
        )
        
        # Initialize style guide library
        style_guides_dir = self.user_data_path / "Prompt_Library" / "Style_Guides"
        self.style_guide_library = StyleGuideLibrary(
            style_guides_dir=str(style_guides_dir),
            log_callback=self.log
        )
        
        # Load prompts and guides
        self.prompt_library.load_all_prompts()
        self.style_guide_library.load_all_guides()
        
        # Active prompts state
        self.active_translate_prompt = None
        self.active_translate_prompt_name = None
        self.active_proofread_prompt = None
        self.active_proofread_prompt_name = None
        self.active_project_prompt = None  # Layer 3: Project Prompts (was active_custom_instruction)
        self.active_project_prompt_name = None  # Layer 3: Project Prompts name
        self.active_style_guide = None
        self.active_style_guide_name = None
        self.active_style_guide_language = None
        
        # UI references (will be set in create_tab)
        self.active_trans_label = None
        self.active_proof_label = None
        self.active_project_label = None  # Layer 3: Project Prompts (was active_custom_label)
        self.active_style_label = None
        
        # Current selection
        self.current_filename = None
        
        # System prompts storage (Layer 1 - loaded from file, with defaults)
        self.system_prompts = {}  # Layer 1: System Prompts
        self.system_prompts_file = self.user_data_path / "Prompt_Library" / "system_prompts_layer1.json"
        
        # Settings for tab memory
        self.settings = QSettings("Supervertaler", "PromptManager")
    
    def log_message(self, message: str):
        """Log a message to the parent app's log if available"""
        if hasattr(self.parent_app, 'log'):
            self.parent_app.log(f"[Prompt Manager] {message}")
        else:
            print(f"[Prompt Manager] {message}")
    
    def _show_message(self, icon, title, text):
        """Helper method for showing QMessageBox"""
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec()
        return msg
    
    def create_tab(self, parent: QWidget):
        """
        Create the Prompt Manager tab UI
        
        Args:
            parent: The QWidget container for the tab
        """
        # Main layout
        main_layout = QVBoxLayout(parent)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # ===== HEADER: Standard Template (matches PDF Rescue / TMX Editor / AutoFingers) =====
        header = QLabel("💡 Prompt Manager")
        header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
        main_layout.addWidget(header, 0)  # 0 = no stretch, stays compact
        
        # Description box (matches Universal Lookup / PDF Rescue / TMX Editor style)
        description = QLabel(
            "4-Layer Prompt Architecture for maximum translation/proofreading/copywriting precision.\n"
            "Manage System Prompts, Domain Prompts, Project Prompts, Style Guides, and AI-powered prompt refinement."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
        main_layout.addWidget(description, 0)  # 0 = no stretch, stays compact
        
        # ===== ACTIVE PROMPTS DISPLAY =====
        active_bar = QFrame()
        active_bar.setStyleSheet("background-color: #FFF3E0; border: 1px solid #FFE0B2; border-radius: 3px;")
        active_bar_layout = QVBoxLayout(active_bar)
        active_bar_layout.setContentsMargins(10, 8, 10, 8)
        active_bar_layout.setSpacing(5)
        
        # Active prompts grid
        active_grid = QHBoxLayout()
        active_grid.setSpacing(15)
        
        # Translation prompt row
        trans_label = QLabel("Translation:")
        trans_label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        trans_label.setMinimumWidth(80)
        active_grid.addWidget(trans_label)
        
        self.active_trans_label = QLabel("Default")
        self.active_trans_label.setStyleSheet("color: #2196F3;")
        active_grid.addWidget(self.active_trans_label, 1)
        
        # Proofreading prompt row
        proof_label = QLabel("Proofreading:")
        proof_label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        proof_label.setMinimumWidth(80)
        active_grid.addWidget(proof_label)
        
        self.active_proof_label = QLabel("Default")
        self.active_proof_label.setStyleSheet("color: #2196F3;")
        active_grid.addWidget(self.active_proof_label, 1)
        
        # Project Prompts row (Layer 3)
        project_label = QLabel("Project Prompts:")
        project_label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        project_label.setMinimumWidth(80)
        active_grid.addWidget(project_label)
        
        self.active_project_label = QLabel("None")
        self.active_project_label.setStyleSheet("color: #4CAF50;")
        active_grid.addWidget(self.active_project_label, 1)
        
        # Style guide row
        style_label = QLabel("Style guide:")
        style_label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        style_label.setMinimumWidth(80)
        active_grid.addWidget(style_label)
        
        self.active_style_label = QLabel("None")
        self.active_style_label.setStyleSheet("color: #FF9800;")
        active_grid.addWidget(self.active_style_label, 1)
        
        active_bar_layout.addLayout(active_grid)
        main_layout.addWidget(active_bar, 0)  # 0 = no stretch, stays compact
        
        # ===== MAIN LAYOUT: Split (Lists | Editor) =====
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # ===== LEFT PANEL: Tab Widget with Lists =====
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab widget for different sections
        self.list_tabs = QTabWidget()
        self.list_tabs.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        
        # System Prompts tab (Layer 1 - first tab since it's the base layer)
        system_prompts_tab = self._create_system_prompts_tab()
        self.list_tabs.addTab(system_prompts_tab, "⚙️ System Prompts")
        
        # Domain Prompts tab (Layer 2)
        domain_tab = self._create_domain_expertise_tab()
        self.list_tabs.addTab(domain_tab, "🎯 Domain Prompts")
        
        # Project Prompts tab (Layer 3)
        project_tab = self._create_project_guidelines_tab()
        self.list_tabs.addTab(project_tab, "📋 Project Prompts")
        
        # Style Guides tab
        style_tab = self._create_style_guides_tab()
        self.list_tabs.addTab(style_tab, "🎨 Style Guides")
        
        # Prompt Assistant tab
        assistant_tab = self._create_prompt_assistant_tab()
        self.list_tabs.addTab(assistant_tab, "🤖 Prompt Assistant")
        
        # Restore saved tab selection
        saved_tab = self.settings.value("selected_tab", 0, type=int)
        if saved_tab < self.list_tabs.count():
            self.list_tabs.setCurrentIndex(saved_tab)
        
        # Connect tab change to save selection
        self.list_tabs.currentChanged.connect(self._on_tab_changed)
        
        left_layout.addWidget(self.list_tabs)
        main_splitter.addWidget(left_panel)
        
        # ===== RIGHT PANEL: Editor =====
        self.editor_panel = self._create_editor_panel()
        main_splitter.addWidget(self.editor_panel)
        
        # Set splitter proportions (40% left, 60% right)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)
        main_splitter.setSizes([400, 600])
        
        main_layout.addWidget(main_splitter, 1)
        
        # Load initial data
        self._load_system_prompts()
        self._load_domain_expertise()
        self._load_project_guidelines()
        self._load_style_guides()
        
        # Update active prompts display
        self._update_active_display()
    
    def _on_tab_changed(self, index):
        """Save tab selection and hide/show editor as needed"""
        self.settings.setValue("selected_tab", index)
        
        # Hide editor on Prompt Assistant, Style Guides, and System Prompts tabs
        tab_text = self.list_tabs.tabText(index)
        if "Prompt Assistant" in tab_text:
            self.editor_panel.setVisible(False)
        elif "Style Guides" in tab_text:
            # Style Guides has its own editor
            self.editor_panel.setVisible(False)
        elif "System Prompts" in tab_text:
            # System Prompts has its own editor
            self.editor_panel.setVisible(False)
        else:
            self.editor_panel.setVisible(True)
    
    def _create_system_prompts_tab(self) -> QWidget:
        """Create System Prompts (Layer 1) tab for viewing/editing base prompts"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Info bar
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #FFE0B2; border: 1px solid #FFCCBC; border-radius: 3px;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(8, 5, 8, 5)
        
        info_title = QLabel("⚙️ Layer 1: System Prompts")
        info_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        info_layout.addWidget(info_title)
        
        info_desc = QLabel(
            "These System Prompts are ALWAYS included in every translation (Layer 1). "
            "They contain critical instructions for CAT tool tag preservation, formatting rules, and language conventions. "
            "⚠️ Edit with caution - incorrect changes may break tag preservation."
        )
        info_desc.setWordWrap(True)
        info_desc.setStyleSheet("color: #666;")
        info_layout.addWidget(info_desc)
        
        layout.addWidget(info_frame)
        
        # Mode selector
        mode_frame = QHBoxLayout()
        mode_label = QLabel("Translation Mode:")
        mode_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        mode_frame.addWidget(mode_label)
        
        self.system_prompts_mode = QComboBox()
        self.system_prompts_mode.addItems(["Single Segment", "Batch DOCX", "Batch Bilingual"])
        self.system_prompts_mode.currentTextChanged.connect(self._on_system_prompts_mode_change)
        mode_frame.addWidget(self.system_prompts_mode, 1)
        mode_frame.addStretch()
        layout.addLayout(mode_frame)
        
        # Editor
        self.system_prompts_editor = QPlainTextEdit()
        self.system_prompts_editor.setFont(QFont("Consolas", 9))
        layout.addWidget(self.system_prompts_editor, 1)
        
        # Buttons
        btn_frame = QFrame()
        btn_frame.setStyleSheet("background-color: #FFE0B2; border: 1px solid #FFCCBC; border-radius: 3px;")
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(8, 5, 8, 5)
        
        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self._save_system_prompt)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 4px 8px;")
        btn_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("↩️ Reset to Default")
        reset_btn.clicked.connect(self._reset_system_prompt)
        reset_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 4px 8px;")
        btn_layout.addWidget(reset_btn)
        
        export_btn = QPushButton("📤 Export")
        export_btn.clicked.connect(self._export_system_prompt)
        export_btn.setToolTip("Export System Prompt to file")
        btn_layout.addWidget(export_btn)
        
        import_btn = QPushButton("📥 Import")
        import_btn.clicked.connect(self._import_system_prompt)
        import_btn.setToolTip("Import System Prompt from file")
        btn_layout.addWidget(import_btn)
        
        btn_layout.addStretch()
        layout.addWidget(btn_frame)
        
        return tab
    
    def _create_domain_expertise_tab(self) -> QWidget:
        """Create Domain Prompts tab (Layer 2)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Filter bar
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: #BBDEFB; border: 1px solid #90CAF9; border-radius: 3px;")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(8, 5, 8, 5)
        
        filter_label = QLabel("Task:")
        filter_layout.addWidget(filter_label)
        
        self.domain_task_filter = QComboBox()
        self.domain_task_filter.addItems([
            "All Tasks", "Translation", "Localization", "Transcreation",
            "Proofreading", "QA", "Copyediting", "Post-editing", "Terminology Extraction"
        ])
        self.domain_task_filter.currentTextChanged.connect(self._load_domain_expertise)
        filter_layout.addWidget(self.domain_task_filter)
        filter_layout.addStretch()
        
        layout.addWidget(filter_frame)
        
        # Prompt list tree
        self.domain_tree = QTreeWidget()
        self.domain_tree.setHeaderLabels(["Prompt Name", "Task", "Domain", "Ver"])
        self.domain_tree.setColumnWidth(0, 250)
        self.domain_tree.setColumnWidth(1, 120)
        self.domain_tree.setColumnWidth(2, 150)
        self.domain_tree.setColumnWidth(3, 50)
        self.domain_tree.itemSelectionChanged.connect(self._on_domain_select)
        layout.addWidget(self.domain_tree, 1)
        
        # Buttons
        btn_frame = QFrame()
        btn_frame.setStyleSheet("background-color: #FFF3E0; border: 1px solid #FFE0B2; border-radius: 3px;")
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(8, 5, 8, 5)
        
        new_btn = QPushButton("➕ New")
        new_btn.clicked.connect(self._create_new_domain_expertise)
        new_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 4px 8px;")
        btn_layout.addWidget(new_btn)
        
        btn_layout.addSpacing(10)
        
        activate_label = QLabel("⚡ Activate:")
        activate_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        btn_layout.addWidget(activate_label)
        
        trans_btn = QPushButton("⚡ Translation")
        trans_btn.clicked.connect(lambda: self._activate_domain_expertise('translate'))
        trans_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 4px 8px;")
        btn_layout.addWidget(trans_btn)
        
        proof_btn = QPushButton("⚡ Proofreading")
        proof_btn.clicked.connect(lambda: self._activate_domain_expertise('proofread'))
        proof_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 4px 8px;")
        btn_layout.addWidget(proof_btn)
        
        btn_layout.addStretch()
        layout.addWidget(btn_frame)
        
        return tab
    
    def _create_project_guidelines_tab(self) -> QWidget:
        """Create Project Prompts tab (Layer 3)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Info bar
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #C8E6C9; border: 1px solid #A5D6A7; border-radius: 3px;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(8, 5, 8, 5)
        
        info_label = QLabel("📝 Project-specific rules (Layer 3) added to Domain Prompts (Layer 2)")
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_frame)
        
        # Guidelines list tree
        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabels(["Project Prompt Name", "Domain", "Ver"])
        self.project_tree.setColumnWidth(0, 300)
        self.project_tree.setColumnWidth(1, 200)
        self.project_tree.setColumnWidth(2, 50)
        self.project_tree.itemSelectionChanged.connect(self._on_project_select)
        layout.addWidget(self.project_tree, 1)
        
        # Buttons
        btn_frame = QFrame()
        btn_frame.setStyleSheet("background-color: #C8E6C9; border: 1px solid #A5D6A7; border-radius: 3px;")
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(8, 5, 8, 5)
        
        new_btn = QPushButton("➕ New")
        new_btn.clicked.connect(self._create_new_project_guideline)
        new_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 4px 8px;")
        btn_layout.addWidget(new_btn)
        
        btn_layout.addSpacing(10)
        
        activate_label = QLabel("✅ Activate:")
        activate_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        btn_layout.addWidget(activate_label)
        
        activate_btn = QPushButton("✅ Use in Current Project")
        activate_btn.clicked.connect(self._activate_project_guideline)
        activate_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 4px 8px;")
        btn_layout.addWidget(activate_btn)
        
        clear_btn = QPushButton("✖ Clear")
        clear_btn.clicked.connect(self._clear_project_guideline)
        clear_btn.setStyleSheet("background-color: #f44336; color: white; padding: 4px 8px;")
        btn_layout.addWidget(clear_btn)
        
        btn_layout.addStretch()
        layout.addWidget(btn_frame)
        
        return tab
    
    def _create_style_guides_tab(self) -> QWidget:
        """Create Style Guides tab with 3-panel layout"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Info section
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #E3F2FD; border: 1px solid #BBDEFB; border-radius: 3px;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(8, 5, 8, 5)
        
        info_title = QLabel("📖 Professional Style Guides")
        info_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        info_layout.addWidget(info_title)
        
        info_desc = QLabel("Manage formatting rules and style guidelines for multiple languages (Layer 4 in prompt hierarchy)")
        info_desc.setWordWrap(True)
        info_desc.setStyleSheet("color: #666;")
        info_layout.addWidget(info_desc)
        
        layout.addWidget(info_frame)
        
        # 3-panel splitter
        style_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # LEFT: Language List
        lang_panel = QWidget()
        lang_layout = QVBoxLayout(lang_panel)
        lang_layout.setContentsMargins(5, 5, 5, 5)
        
        lang_label = QLabel("📚 Languages")
        lang_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        lang_layout.addWidget(lang_label)
        
        self.style_languages_list = QListWidget()
        self.style_languages_list.itemSelectionChanged.connect(self._on_style_language_select)
        lang_layout.addWidget(self.style_languages_list, 1)
        
        # Language buttons
        lang_btn_layout = QVBoxLayout()
        
        new_lang_btn = QPushButton("➕ New")
        new_lang_btn.clicked.connect(self._create_new_style_guide)
        lang_btn_layout.addWidget(new_lang_btn)
        
        activate_lang_btn = QPushButton("✅ Activate")
        activate_lang_btn.clicked.connect(self._activate_style_guide)
        lang_btn_layout.addWidget(activate_lang_btn)
        
        clear_lang_btn = QPushButton("✖ Clear")
        clear_lang_btn.clicked.connect(self._clear_style_guide)
        lang_btn_layout.addWidget(clear_lang_btn)
        
        reload_lang_btn = QPushButton("Reload All")
        reload_lang_btn.clicked.connect(self._load_style_guides)
        lang_btn_layout.addWidget(reload_lang_btn)
        
        lang_layout.addLayout(lang_btn_layout)
        style_splitter.addWidget(lang_panel)
        
        # CENTER: Editor
        editor_panel = QWidget()
        editor_layout = QVBoxLayout(editor_panel)
        editor_layout.setContentsMargins(5, 5, 5, 5)
        
        editor_label = QLabel("📝 Edit Guide")
        editor_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        editor_layout.addWidget(editor_label)
        
        # View mode toggle
        view_mode_frame = QHBoxLayout()
        view_mode_label = QLabel("View Mode:")
        view_mode_frame.addWidget(view_mode_label)
        
        self.style_view_mode = QComboBox()
        self.style_view_mode.addItems(["Formatted", "Raw Markdown"])
        self.style_view_mode.currentTextChanged.connect(self._on_style_view_mode_change)
        view_mode_frame.addWidget(self.style_view_mode)
        view_mode_frame.addStretch()
        editor_layout.addLayout(view_mode_frame)
        
        # Editor
        self.style_editor = QPlainTextEdit()
        self.style_editor.setFont(QFont("Consolas", 9))
        editor_layout.addWidget(self.style_editor, 1)
        
        # Editor buttons
        editor_btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self._save_style_guide)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 4px 8px;")
        editor_btn_layout.addWidget(save_btn)
        
        import_btn = QPushButton("📥 Import")
        import_btn.clicked.connect(self._import_style_guide)
        editor_btn_layout.addWidget(import_btn)
        
        export_btn = QPushButton("📤 Export")
        export_btn.clicked.connect(self._export_style_guide)
        editor_btn_layout.addWidget(export_btn)
        
        editor_btn_layout.addStretch()
        editor_layout.addLayout(editor_btn_layout)
        
        style_splitter.addWidget(editor_panel)
        style_splitter.setStretchFactor(0, 1)
        style_splitter.setStretchFactor(1, 3)
        style_splitter.setSizes([200, 600])
        
        layout.addWidget(style_splitter, 1)
        
        # Tip at bottom
        tip_frame = QFrame()
        tip_frame.setStyleSheet("background-color: #E3F2FD; border: 1px solid #BBDEFB; border-radius: 3px;")
        tip_layout = QVBoxLayout(tip_frame)
        tip_layout.setContentsMargins(8, 5, 8, 5)
        
        tip_label = QLabel("💡 Tip: Use the Prompt Assistant tab to get AI help with editing style guides")
        tip_label.setStyleSheet("color: #666; font-style: italic;")
        tip_layout.addWidget(tip_label)
        
        layout.addWidget(tip_frame)
        
        return tab
    
    def _create_prompt_assistant_tab(self) -> QWidget:
        """Create Prompt Assistant tab with chat interface"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Header
        header_label = QLabel("🤖 Prompt Assistant")
        header_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(header_label)
        
        # Info
        info_label = QLabel("AI-powered prompt refinement through natural language conversation")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; padding: 5px; background-color: #E8F5E9; border-radius: 3px;")
        layout.addWidget(info_label)
        
        # Chat history area
        self.assistant_chat = QPlainTextEdit()
        self.assistant_chat.setReadOnly(True)
        self.assistant_chat.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.assistant_chat, 1)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.assistant_input = QLineEdit()
        self.assistant_input.setPlaceholderText("Describe how you want to improve your prompt...")
        self.assistant_input.returnPressed.connect(self._send_assistant_message)
        input_layout.addWidget(self.assistant_input, 1)
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self._send_assistant_message)
        send_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 4px 12px;")
        input_layout.addWidget(send_btn)
        
        layout.addLayout(input_layout)
        
        # Add welcome message
        self.assistant_chat.setPlainText(
            "Welcome to Prompt Assistant!\n\n"
            "I can help you improve your translation prompts using natural language.\n\n"
            "First, select a prompt from Domain Prompts or Project Prompts tabs, "
            "then come back here to refine it.\n\n"
            "Try asking:\n"
            "- 'Make it more formal'\n"
            "- 'Add emphasis on terminology consistency'\n"
            "- 'Simplify the language'\n"
        )
        
        return tab
    
    def _create_editor_panel(self) -> QWidget:
        """Create the right-side editor panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Title
        title = QLabel("Prompt Editor")
        title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Metadata grid
        meta_group = QGroupBox("Metadata")
        meta_layout = QVBoxLayout(meta_group)
        
        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        name_label.setMinimumWidth(80)
        name_layout.addWidget(name_label)
        self.editor_name = QLineEdit()
        name_layout.addWidget(self.editor_name, 1)
        meta_layout.addLayout(name_layout)
        
        # Domain and Task Type row
        domain_row = QHBoxLayout()
        
        domain_label = QLabel("Domain:")
        domain_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        domain_label.setMinimumWidth(80)
        domain_row.addWidget(domain_label)
        self.editor_domain = QLineEdit()
        domain_row.addWidget(self.editor_domain, 1)
        
        task_label = QLabel("Task Type:")
        task_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        task_label.setMinimumWidth(80)
        domain_row.addWidget(task_label)
        self.editor_task_type = QComboBox()
        self.editor_task_type.addItems([
            "Translation", "Localization", "Transcreation", "Proofreading",
            "QA", "Copyediting", "Post-editing", "Terminology Extraction"
        ])
        domain_row.addWidget(self.editor_task_type, 1)
        meta_layout.addLayout(domain_row)
        
        # Version
        version_layout = QHBoxLayout()
        version_label = QLabel("Version:")
        version_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        version_label.setMinimumWidth(80)
        version_layout.addWidget(version_label)
        self.editor_version = QLineEdit()
        self.editor_version.setMaximumWidth(100)
        version_layout.addWidget(self.editor_version)
        version_layout.addStretch()
        meta_layout.addLayout(version_layout)
        
        layout.addWidget(meta_group)
        
        # Description
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(desc_label)
        
        self.editor_description = QPlainTextEdit()
        self.editor_description.setMaximumHeight(60)
        layout.addWidget(self.editor_description)
        
        # Content
        content_label = QLabel("Prompt Content:")
        content_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(content_label)
        
        self.editor_content = QPlainTextEdit()
        self.editor_content.setFont(QFont("Consolas", 9))
        layout.addWidget(self.editor_content, 1)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save Changes")
        save_btn.clicked.connect(self._save_prompt)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 4px 8px;")
        btn_layout.addWidget(save_btn)
        
        revert_btn = QPushButton("↩️ Revert")
        revert_btn.clicked.connect(self._revert_prompt)
        revert_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 4px 8px;")
        btn_layout.addWidget(revert_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(self._delete_prompt)
        delete_btn.setStyleSheet("background-color: #F44336; color: white; padding: 4px 8px;")
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        return panel
    
    # ===== Data Loading Methods =====
    
    def _load_domain_expertise(self):
        """Load Domain Prompts (Layer 2) into the tree"""
        self.domain_tree.clear()
        
        # Force reload
        self.prompt_library.load_all_prompts()
        
        # Get filter
        filter_task = self.domain_task_filter.currentText()
        
        # Load from PromptLibrary
        prompts = self.prompt_library.get_prompt_list()
        
        for prompt_info in prompts:
            # Only show Domain Prompts (Layer 2)
            # Note: stored in System_prompts folder but are Layer 2 Domain Prompts
            if prompt_info.get('_type', 'system_prompt') != 'system_prompt':
                continue
            
            # Skip if in Custom_instructions folder (those are Layer 3 Project Prompts)
            if 'Custom_instructions' in prompt_info.get('filename', ''):
                continue
            
            # Filter by task type
            task = prompt_info.get('task_type', '')
            if filter_task != "All Tasks" and task != filter_task:
                continue
            
            name = prompt_info.get('name', 'Unnamed')
            domain = prompt_info.get('domain', '')
            version = str(prompt_info.get('version', '1.0'))  # Convert to string
            
            # Check if active
            is_active = (name == self.active_translate_prompt_name or
                        name == self.active_proofread_prompt_name)
            
            # Create item
            item = QTreeWidgetItem([name, task, domain, version])
            item.setData(0, Qt.ItemDataRole.UserRole, prompt_info.get('filename'))
            
            # Bold if active
            if is_active:
                font = item.font(0)
                font.setBold(True)
                item.setFont(0, font)
            
            self.domain_tree.addTopLevelItem(item)
    
    def _load_project_guidelines(self):
        """Load Project Prompts (Layer 3) into the tree"""
        self.project_tree.clear()
        
        # Force reload
        self.prompt_library.load_all_prompts()
        
        # Load from PromptLibrary
        prompts = self.prompt_library.get_prompt_list()
        
        for prompt_info in prompts:
            # Only show Project Prompts (Layer 3)
            filename = prompt_info.get('filename', '')
            is_system = prompt_info.get('_type', 'system_prompt') == 'system_prompt'
            is_in_custom_folder = 'Custom_instructions' in filename
            
            # Show if explicitly Project Prompts OR in Custom_instructions folder
            if is_system and not is_in_custom_folder:
                continue
            
            name = prompt_info.get('name', 'Unnamed')
            domain = prompt_info.get('domain', '')
            version = str(prompt_info.get('version', '1.0'))  # Convert to string
            
            # Check if active
            is_active = (name == self.active_project_prompt_name)
            
            # Create item
            item = QTreeWidgetItem([name, domain, version])
            item.setData(0, Qt.ItemDataRole.UserRole, filename)
            
            # Bold if active
            if is_active:
                font = item.font(0)
                font.setBold(True)
                item.setFont(0, font)
            
            self.project_tree.addTopLevelItem(item)
    
    def _load_style_guides(self):
        """Load style guides into the languages list"""
        self.style_languages_list.clear()
        
        # Force reload
        self.style_guide_library.load_all_guides()
        
        # Get all languages
        languages = self.style_guide_library.get_all_languages()
        
        # Get active language
        active_language = self.active_style_guide_language
        
        for language in languages:
            # Add visual indicator for active item
            display_text = f"✓ {language}" if language == active_language else f"  {language}"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, language)
            self.style_languages_list.addItem(item)
    
    # ===== Selection Handlers =====
    
    def _on_domain_select(self):
        """Handle Domain Prompt (Layer 2) selection"""
        try:
            items = self.domain_tree.selectedItems()
            if not items:
                return
            
            item = items[0]
            if not item:
                return
            
            filename = item.data(0, Qt.ItemDataRole.UserRole)
            if not filename:
                return
            
            # Load prompt
            prompt_data = self.prompt_library.get_prompt(filename)
            if not prompt_data:
                self.log_message(f"Prompt data not found for: {filename}")
                return
            
            self.current_filename = filename
            self._populate_editor(prompt_data)
        except Exception as e:
            self.log_message(f"Error selecting Domain Prompt: {str(e)}")
            import traceback
            self.log_message(traceback.format_exc())
    
    def _on_project_select(self):
        """Handle Project Prompt (Layer 3) selection"""
        try:
            items = self.project_tree.selectedItems()
            if not items:
                return
            
            item = items[0]
            if not item:
                return
            
            filename = item.data(0, Qt.ItemDataRole.UserRole)
            if not filename:
                return
            
            # Load prompt
            prompt_data = self.prompt_library.get_prompt(filename)
            if not prompt_data:
                self.log_message(f"Prompt data not found for: {filename}")
                return
            
            self.current_filename = filename
            self._populate_editor(prompt_data)
        except Exception as e:
            self.log_message(f"Error selecting Project Prompt: {str(e)}")
            import traceback
            self.log_message(traceback.format_exc())
    
    def _on_style_language_select(self):
        """Handle style guide language selection"""
        items = self.style_languages_list.selectedItems()
        if not items:
            return
        
        item = items[0]
        language = item.data(Qt.ItemDataRole.UserRole)
        if not language:
            return
        
        # Load guide
        guide = self.style_guide_library.get_guide(language)
        if not guide:
            return
        
        # Store raw content for toggling
        self.current_style_language = language
        self.current_style_raw_content = guide.get('content', '')
        
        # Display in editor
        self.style_editor.setPlainText(self.current_style_raw_content)
    
    def _populate_editor(self, prompt_data):
        """Populate editor with prompt data"""
        try:
            # Ensure all values are strings or safe defaults
            name = str(prompt_data.get('name', '')) if prompt_data.get('name') else ''
            domain = str(prompt_data.get('domain', '')) if prompt_data.get('domain') else ''
            version = str(prompt_data.get('version', '1.0'))  # Convert to string (may be float)
            description = str(prompt_data.get('description', '')) if prompt_data.get('description') else ''
            
            self.editor_name.setText(name)
            self.editor_domain.setText(domain)
            
            task_type = prompt_data.get('task_type', 'Translation')
            if task_type:
                task_type = str(task_type)
                index = self.editor_task_type.findText(task_type)
                if index >= 0:
                    self.editor_task_type.setCurrentIndex(index)
                else:
                    self.editor_task_type.setCurrentIndex(0)
            else:
                self.editor_task_type.setCurrentIndex(0)
            
            self.editor_version.setText(version)
            self.editor_description.setPlainText(description)
            
            # Content - use translate_prompt field
            content = prompt_data.get('translate_prompt', '') or prompt_data.get('content', '')
            if content:
                content = str(content)
            else:
                content = ''
            self.editor_content.setPlainText(content)
        except Exception as e:
            self.log_message(f"Error populating editor: {str(e)}")
            # Clear editor on error
            self.editor_name.clear()
            self.editor_domain.clear()
            self.editor_task_type.setCurrentIndex(0)
            self.editor_version.clear()
            self.editor_description.clear()
            self.editor_content.clear()
    
    # ===== Activation Methods =====
    
    def _activate_domain_expertise(self, slot):
        """Activate selected Domain Prompt (Layer 2) for translation or proofreading"""
        items = self.domain_tree.selectedItems()
        if not items:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("No Selection")
            msg.setText("Please select a Domain Prompt to activate.")
            msg.exec()
            return
        
        item = items[0]
        filename = item.data(0, Qt.ItemDataRole.UserRole)
        if not filename:
            return
        
        # Load and apply
        prompt_data = self.prompt_library.get_prompt(filename)
        if not prompt_data:
            return
        
        if slot == 'translate':
            self.active_translate_prompt = prompt_data.get('translate_prompt', '')
            self.active_translate_prompt_name = prompt_data.get('name', 'Unnamed')
            self.log_message(f"Activated for Translation: {self.active_translate_prompt_name}")
        elif slot == 'proofread':
            self.active_proofread_prompt = prompt_data.get('proofread_prompt', '') or prompt_data.get('translate_prompt', '')
            self.active_proofread_prompt_name = prompt_data.get('name', 'Unnamed')
            self.log_message(f"Activated for Proofreading: {self.active_proofread_prompt_name}")
        
        self._update_active_display()
        self._load_domain_expertise()  # Refresh to show bold
    
    def _activate_project_guideline(self):
        """Activate selected Project Prompt (Layer 3)"""
        items = self.project_tree.selectedItems()
        if not items:
            self._show_message(QMessageBox.Icon.Warning, "No Selection", "Please select a Project Prompt to activate.")
            return
        
        item = items[0]
        filename = item.data(0, Qt.ItemDataRole.UserRole)
        if not filename:
            return
        
        # Load
        prompt_data = self.prompt_library.get_prompt(filename)
        if not prompt_data:
            return
        
        content = prompt_data.get('translate_prompt', '') or prompt_data.get('content', '')
        name = prompt_data.get('name', 'Unnamed')
        
        # Activate
        self.active_project_prompt = content
        self.active_project_prompt_name = name
        
        self._update_active_display()
        self._load_project_guidelines()  # Refresh
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Activated")
        msg.setText(f"Project Prompt '{name}' is now active for this project.\n\n"
                   f"It will be appended to your Domain Prompts during translation.")
        msg.exec()
    
    def _clear_project_guideline(self):
        """Clear active project prompt"""
        if not self.active_project_prompt:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("No Active Prompt")
            msg.setText("No Project Prompt is currently active.")
            msg.exec()
            return
        
        self.active_project_prompt = None
        self.active_project_prompt_name = None
        
        self._update_active_display()
        self._load_project_guidelines()
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Cleared")
        msg.setText("Project Prompt has been cleared.")
        msg.exec()
    
    def _activate_style_guide(self):
        """Activate selected style guide"""
        items = self.style_languages_list.selectedItems()
        if not items:
            self._show_message(QMessageBox.Icon.Warning, "No Selection", "Please select a Style Guide to activate.")
            return
        
        item = items[0]
        language = item.data(Qt.ItemDataRole.UserRole)
        if not language:
            return
        
        # Load
        guide = self.style_guide_library.get_guide(language)
        if not guide:
            self._show_message(QMessageBox.Icon.Critical, "Error", f"Could not load style guide: {language}")
            return
        
        content = guide.get('content', '')
        name = guide.get('language', language)
        
        # Activate
        self.active_style_guide = content
        self.active_style_guide_name = name
        self.active_style_guide_language = language
        
        self._update_active_display()
        self._load_style_guides()
        
        self._show_message(
            QMessageBox.Icon.Information, "Activated",
            f"Style Guide '{name}' is now active for this project.\n\n"
            f"It will be appended to your prompts during translation (Layer 4 in hierarchy)."
        )
    
    def _clear_style_guide(self):
        """Clear active style guide"""
        if not self.active_style_guide:
            self._show_message(QMessageBox.Icon.Information, "No Active Style Guide", "No Style Guide is currently active.")
            return
        
        self.active_style_guide = None
        self.active_style_guide_name = None
        self.active_style_guide_language = None
        
        self._update_active_display()
        self._load_style_guides()
        
        self._show_message(QMessageBox.Icon.Information, "Cleared", "Style Guide has been cleared.")
    
    def _update_active_display(self):
        """Update the active prompts display at top"""
        if self.active_trans_label:
            trans_name = self.active_translate_prompt_name or "Default"
            self.active_trans_label.setText(trans_name)
        
        if self.active_proof_label:
            proof_name = self.active_proofread_prompt_name or "Default"
            self.active_proof_label.setText(proof_name)
        
        if self.active_project_label:
            project_name = self.active_project_prompt_name or "None"
            self.active_project_label.setText(project_name)
        
        if self.active_style_label:
            style_name = self.active_style_guide_name or "None"
            self.active_style_label.setText(style_name)
    
    # ===== Creation Methods =====
    
    def _create_new_domain_expertise(self):
        """Create a new Domain Prompt (Layer 2)"""
        name, ok = QInputDialog.getText(
            None, "New Domain Prompt",
            "Enter a name for the new Domain Prompt:"
        )
        if not ok or not name:
            return
        
        # Create sanitized filename
        base_filename = name.lower().replace(' ', '_').replace('-', '_')
        base_filename = ''.join(c for c in base_filename if c.isalnum() or c == '_')
        filename = f"{base_filename} (system prompt).md"
        
        # Check if exists
        system_prompts_dir = self.user_data_path / "Prompt_Library" / "System_prompts"
        filepath = system_prompts_dir / filename
        
        if filepath.exists():
            self._show_message(
                QMessageBox.Icon.Critical, "File Exists",
                f"A Domain Prompt named '{name}' already exists.\n"
                f"Please choose a different name."
            )
            return
        
        # Create template
        from datetime import datetime
        template = f"""---
name: "{name}"
description: "New Domain Prompt (Layer 2)"
domain: "General"
version: "1.0"
task_type: "Translation"
created: "{datetime.now().strftime('%Y-%m-%d')}"
translate_prompt: |
  You are a professional translator.
  
  Your task is to translate text accurately and naturally.
  
  Key requirements:
  - Maintain the original meaning and tone
  - Use natural, idiomatic language
  - Preserve formatting and structure
  - Be consistent with terminology
---

# {name}

This is a new Domain Prompt (Layer 2). Edit this content to define the domain-specific translation guidelines and behavior.

## Guidelines

Add your translation guidelines here...
"""
        
        try:
            system_prompts_dir.mkdir(parents=True, exist_ok=True)
            filepath.write_text(template, encoding='utf-8')
            
            # Reload and select
            self._load_domain_expertise()
            
            # Find and select the new item
            for i in range(self.domain_tree.topLevelItemCount()):
                item = self.domain_tree.topLevelItem(i)
                if item and item.text(0) == name:
                    self.domain_tree.setCurrentItem(item)
                    self.domain_tree.scrollToItem(item)
                    break
            
            self.log_message(f"Created new Domain Prompt: {name}")
            self._show_message(
                QMessageBox.Icon.Information, "Success",
                f"Domain Prompt '{name}' created successfully!\n\n"
                f"File: {filename}"
            )
        except Exception as e:
            self._show_message(QMessageBox.Icon.Critical, "Error", f"Failed to create Domain Prompt:\n{str(e)}")
    
    def _create_new_project_guideline(self):
        """Create a new Project Prompt (Layer 3)"""
        name, ok = QInputDialog.getText(
            None, "New Project Prompt",
            "Enter a name for the new Project Prompt:"
        )
        if not ok or not name:
            return
        
        # Create sanitized filename
        base_filename = name.lower().replace(' ', '_').replace('-', '_')
        base_filename = ''.join(c for c in base_filename if c.isalnum() or c == '_')
        filename = f"{base_filename} (project_prompt).md"
        
        # Check if exists
        custom_dir = self.user_data_path / "Prompt_Library" / "Custom_instructions"
        filepath = custom_dir / filename
        
        if filepath.exists():
            self._show_message(
                QMessageBox.Icon.Critical, "File Exists",
                f"A Project Prompt named '{name}' already exists.\n"
                f"Please choose a different name."
            )
            return
        
        # Create template
        from datetime import datetime
        template = f"""---
name: "{name}"
description: "New Project Prompt (Layer 3)"
domain: "Project-specific"
version: "1.0"
task_type: "Translation"
created: "{datetime.now().strftime('%Y-%m-%d')}"
translate_prompt: |
  # {name}
  
  Add your project-specific instructions here...
---

# {name}

This Project Prompt (Layer 3) will be appended to your Domain Prompts (Layer 2) during translation.

## Custom Rules

Add your custom rules and guidelines here...

### Examples:
- Use specific terminology
- Follow client preferences
- Handle special formatting
"""
        
        try:
            custom_dir.mkdir(parents=True, exist_ok=True)
            filepath.write_text(template, encoding='utf-8')
            
            # Reload and select
            self._load_project_guidelines()
            
            # Find and select the new item
            for i in range(self.project_tree.topLevelItemCount()):
                item = self.project_tree.topLevelItem(i)
                if item and item.text(0) == name:
                    self.project_tree.setCurrentItem(item)
                    self.project_tree.scrollToItem(item)
                    break
            
            self.log_message(f"Created new Project Prompt: {name}")
            self._show_message(
                QMessageBox.Icon.Information, "Success",
                f"Project Prompt '{name}' created successfully!\n\n"
                f"File: {filename}"
            )
        except Exception as e:
            self._show_message(QMessageBox.Icon.Critical, "Error", f"Failed to create Project Prompt:\n{str(e)}")
    
    def _create_new_style_guide(self):
        """Create a new style guide"""
        language, ok = QInputDialog.getText(
            None, "New Style Guide",
            "Enter the language for the new style guide:\n(e.g., 'German', 'French', 'Spanish')"
        )
        if not ok or not language:
            return
        
        # Capitalize properly
        language = language.strip().title()
        
        # Check if exists
        existing = self.style_guide_library.get_guide(language)
        if existing:
            self._show_message(
                QMessageBox.Icon.Critical, "Style Guide Exists",
                f"A style guide for '{language}' already exists.\n"
                f"Please edit the existing one or choose a different language."
            )
            return
        
        # Create template
        template = f"""# {language} Style Guide

## Document Purpose
Professional style guidelines for translating into {language}.

## Formatting Rules

### Numbers
- Use appropriate thousands separator
- Follow local conventions for decimals

### Dates and Times
- Follow {language} date format conventions
- Use 24-hour or 12-hour format as appropriate

### Currency
- Use local currency symbols correctly
- Place currency symbols according to {language} conventions

## Typography

### Quotation Marks
- Use appropriate quotation marks for {language}

### Punctuation
- Follow {language} punctuation rules
- Pay attention to spacing around punctuation

## Terminology Guidelines

### Consistency
- Use consistent terminology throughout
- Refer to project termbase when available

### Formality
- Maintain appropriate level of formality
- Use polite forms where culturally expected

## Special Considerations

### Cultural Adaptation
- Adapt idioms and expressions appropriately
- Consider cultural context

### Legal/Regulatory
- Follow any legal requirements for {language} documents
- Use standard legal terminology where applicable

---

*This style guide should be customized based on client requirements and industry standards.*
"""
        
        try:
            # Use StyleGuideLibrary's create_guide method
            if self.style_guide_library.create_guide(language, template):
                # Reload
                self.style_guide_library.load_all_guides()
                self._load_style_guides()
            
            # Select the new guide
            for i in range(self.style_languages_list.count()):
                item = self.style_languages_list.item(i)
                if item and item.data(Qt.ItemDataRole.UserRole) == language:
                    self.style_languages_list.setCurrentItem(item)
                    self._on_style_language_select()
                    break
            
                self.log_message(f"Created new style guide: {language}")
                self._show_message(
                    QMessageBox.Icon.Information, "Success",
                    f"Style guide for '{language}' created successfully!"
                )
            else:
                self._show_message(
                    QMessageBox.Icon.Critical, "Error",
                    f"Failed to create style guide for '{language}'."
                )
        except Exception as e:
            self._show_message(QMessageBox.Icon.Critical, "Error", f"Failed to create style guide:\n{str(e)}")
    
    # ===== Editor Methods =====
    
    def _save_prompt(self):
        """Save changes to current prompt"""
        if not self.current_filename:
            self._show_message(QMessageBox.Icon.Warning, "No Prompt", "No prompt selected to save.")
            return
        
        # Gather data
        name = self.editor_name.text()
        domain = self.editor_domain.text()
        task_type = self.editor_task_type.currentText()
        version = self.editor_version.text()
        description = self.editor_description.toPlainText()
        translate_prompt = self.editor_content.toPlainText()
        
        # Save via PromptLibrary
        if self.prompt_library.update_prompt(
            self.current_filename, name, description, domain,
            translate_prompt, proofread_prompt="", version=version, task_type=task_type
        ):
            self.log_message(f"Saved: {name}")
            self._show_message(QMessageBox.Icon.Information, "Saved", f"Prompt '{name}' saved successfully.")
            # Reload lists
            self._load_domain_expertise()
            self._load_project_guidelines()
        else:
            self._show_message(QMessageBox.Icon.Critical, "Error", "Failed to save prompt.")
    
    def _revert_prompt(self):
        """Revert changes by reloading from file"""
        if not self.current_filename:
            return
        
        # Reload from disk
        prompt_data = self.prompt_library.get_prompt(self.current_filename)
        if not prompt_data:
            return
        
        self._populate_editor(prompt_data)
        self.log_message("Reverted changes")
    
    def _delete_prompt(self):
        """Delete current prompt"""
        if not self.current_filename:
            self._show_message(QMessageBox.Icon.Warning, "No Prompt", "No prompt selected to delete.")
            return
        
        # Confirm
        name = self.editor_name.text()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm Delete")
        msg.setText(f"Are you sure you want to delete '{name}'?\n\nThis cannot be undone.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg.exec()
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Delete via PromptLibrary
        if self.prompt_library.delete_prompt(self.current_filename):
            self.log_message(f"Deleted: {name}")
            # Clear editor
            self.current_filename = None
            self.editor_name.clear()
            self.editor_domain.clear()
            self.editor_task_type.setCurrentIndex(0)
            self.editor_version.clear()
            self.editor_description.clear()
            self.editor_content.clear()
            # Reload lists
            self._load_domain_expertise()
            self._load_project_guidelines()
            self._show_message(QMessageBox.Icon.Information, "Deleted", f"Prompt '{name}' deleted successfully.")
        else:
            self._show_message(QMessageBox.Icon.Critical, "Error", "Failed to delete prompt.")
    
    # ===== Style Guide Methods =====
    
    def _save_style_guide(self):
        """Save current style guide"""
        if not hasattr(self, 'current_style_language') or not self.current_style_language:
            self._show_message(QMessageBox.Icon.Warning, "No Selection", "Please select a style guide to save.")
            return
        
        content = self.style_editor.toPlainText()
        
        try:
            # Save via StyleGuideLibrary
            if self.style_guide_library.update_guide(self.current_style_language, content):
                self.log_message(f"Saved style guide: {self.current_style_language}")
                self._show_message(QMessageBox.Icon.Information, "Saved", "Style guide saved successfully.")
                self._load_style_guides()
            else:
                self._show_message(QMessageBox.Icon.Critical, "Error", "Failed to save style guide.")
        except Exception as e:
            self._show_message(QMessageBox.Icon.Critical, "Error", f"Failed to save style guide:\n{str(e)}")
    
    def _import_style_guide(self):
        """Import style guide from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Import Style Guide", "",
            "Markdown Files (*.md);;Text Files (*.txt);;All Files (*.*)"
        )
        if not file_path:
            return
        
        try:
            content = Path(file_path).read_text(encoding='utf-8')
            self.style_editor.setPlainText(content)
            self.log_message(f"Imported style guide from: {Path(file_path).name}")
        except Exception as e:
            self._show_message(QMessageBox.Icon.Critical, "Error", f"Failed to import style guide:\n{str(e)}")
    
    def _export_style_guide(self):
        """Export current style guide to file"""
        if not self.style_editor.toPlainText():
            self._show_message(QMessageBox.Icon.Warning, "No Content", "No style guide content to export.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Export Style Guide", "",
            "Markdown Files (*.md);;Text Files (*.txt);;All Files (*.*)"
        )
        if not file_path:
            return
        
        try:
            Path(file_path).write_text(self.style_editor.toPlainText(), encoding='utf-8')
            self.log_message(f"Exported style guide to: {Path(file_path).name}")
            self._show_message(QMessageBox.Icon.Information, "Exported", "Style guide exported successfully.")
        except Exception as e:
            self._show_message(QMessageBox.Icon.Critical, "Error", f"Failed to export style guide:\n{str(e)}")
    
    def _on_style_view_mode_change(self, mode_text):
        """Handle style guide view mode change"""
        # For now, just show raw markdown
        # Could add markdown rendering later
        pass
    
    # ===== Prompt Assistant Methods =====
    
    def _send_assistant_message(self):
        """Send message to prompt assistant"""
        message = self.assistant_input.text().strip()
        if not message:
            return
        
        # Add to chat
        self.assistant_chat.appendPlainText(f"\nYou: {message}\n")
        self.assistant_input.clear()
        
        # TODO: Integrate with modules.prompt_assistant.PromptAssistant
        # For now, just show a placeholder
        self.assistant_chat.appendPlainText(
            "Assistant: Prompt Assistant integration coming soon.\n"
            "This will help you refine your prompts using AI.\n"
        )
    
    # ===== System Prompt Methods (Layer 1) =====
    
    def _load_system_prompts(self):
        """Load System Prompts (Layer 1) from file, or use defaults"""
        import json
        
        # Default prompts
        default_prompts = {
            "single": self._get_default_system_prompt("single"),
            "batch_docx": self._get_default_system_prompt("single"),  # Same for now
            "batch_bilingual": self._get_default_system_prompt("single")  # Same for now
        }
        
        # Try to load from file
        if self.system_prompts_file.exists():
            try:
                with open(self.system_prompts_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults (in case new modes are added)
                    self.system_prompts = {**default_prompts, **loaded}
                self.log_message("Loaded System Prompts from file")
            except Exception as e:
                self.log_message(f"Error loading System Prompts: {e}, using defaults")
                self.system_prompts = default_prompts
        else:
            # Use defaults and save them
            self.system_prompts = default_prompts
            self._save_system_prompts_file()
        
        # Update editor if it exists
        if hasattr(self, 'system_prompts_editor'):
            self._on_system_prompts_mode_change()
    
    def _save_system_prompts_file(self):
        """Save System Prompts (Layer 1) to file"""
        import json
        
        try:
            self.system_prompts_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.system_prompts_file, 'w', encoding='utf-8') as f:
                json.dump(self.system_prompts, f, indent=2, ensure_ascii=False)
            self.log_message("Saved System Prompts to file")
        except Exception as e:
            self.log_message(f"Error saving System Prompts: {e}")
    
    def _get_default_system_prompt(self, mode="single"):
        """Get default System Prompt (Layer 1 - hardcoded fallback)"""
        if mode == "single":
            return """# SYSTEM PROMPT

⚠️ PROFESSIONAL TRANSLATION CONTEXT:
You are performing professional technical/medical translation as a licensed service for a commercial translation company. This is legitimate professional work. All medical, technical, or specialized terminology is for professional translation purposes only.
THIS IS NOT A REQUEST FOR MEDICAL ADVICE - it is professional document translation for regulatory compliance.

You are an expert {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}} translator with deep understanding of context and nuance.

**CONTEXT**: Full document context is provided for reference below.

**YOUR TASK**: Translate ONLY the text in the 'TEXT TO TRANSLATE' section.

**IMPORTANT INSTRUCTIONS**:
- Provide ONLY the translated text
- Do NOT include numbering, labels, or commentary
- Do NOT repeat the source text
- Maintain accuracy and natural fluency

**CRITICAL: CAT TOOL TAG PRESERVATION**:
- Source may contain CAT tool formatting tags in various formats:
  • memoQ: [1}, {2], [3}, {4] (asymmetric bracket-brace pairs)
  • Trados Studio: <410>text</410>, <434>text</434> (XML-style opening/closing tags)
  • CafeTran: |formatted text| (pipe symbols mark formatted text - bold, italic, underline, etc.)
  • Other CAT tools: various bracketed or special character sequences
- These are placeholder tags representing formatting (bold, italic, links, etc.)
- PRESERVE ALL tags - if source has N tags, target must have exactly N tags
- Keep tags with their content and adjust position for natural target language word order
- Never translate, omit, or modify the tags themselves - only reposition them
- Examples:
  • memoQ: '[1}De uitvoer{2]' → '[1}The exports{2]'
  • Trados: '<410>De uitvoer van machines</410>' → '<410>Exports of machinery</410>'
  • CafeTran: 'He debuted against |Juventus FC| in 2001' → 'Hij debuteerde tegen |Juventus FC| in 2001'
  • Multiple: '[1}De uitvoer{2] [3}stelt niets voor{4]' → '[1}Exports{2] [3}mean nothing{4]'

**SPECIAL RULE FOR UICONTROL TAGS** (memoQ bilingual DOCX):
- Text wrapped in [uicontrol...{uicontrol] tags must be translated with the original text followed by translation in parentheses
- Structure: [uicontrol id="GUID"}Original English Text{uicontrol]: Description
- Translation format: [uicontrol id="GUID"}Original English Text (Translation){uicontrol]: Translated Description
- Example:
  • Source: [uicontrol id="GUID-D82B8555-1166-4740-AFD1-78FCA44BF83A"}Turn on the positioning mode{uicontrol]: Enabling the function of camera-aided positioning.
  • Target: [uicontrol id="GUID-D82B8555-1166-4740-AFD1-78FCA44BF83A"}Turn on the positioning mode (Schakel de positioneringsmodus in){uicontrol]: Het inschakelen van de functie voor camera-ondersteunde positionering.
- CRITICAL: Keep the original English text unchanged, add translation in parentheses after it

**LANGUAGE-SPECIFIC NUMBER FORMATTING**:
- If the target language is **Dutch**, **French**, **German**, **Italian**, **Spanish**, or another **continental European language**, use a **comma** as the decimal separator and a **space or non-breaking space** between the number and unit (e.g., 17,1 cm).
- If the target language is **English** or **Irish**, use a **full stop (period)** as the decimal separator and **no space** before the unit (e.g., 17.1 cm).
- Always follow the **number formatting conventions** of the target language.

If the text refers to figures (e.g., 'Figure 1A'), relevant images may be provided for visual context.

{{SOURCE_LANGUAGE}} text:
{{SOURCE_TEXT}}"""
        
        # For other modes, return same as single for now
        return self._get_default_system_prompt("single")
    
    def _on_system_prompts_mode_change(self):
        """Handle System Prompt mode selection change"""
        if not hasattr(self, 'system_prompts_editor'):
            return
        
        mode_text = self.system_prompts_mode.currentText()
        mode_key = "single"
        if mode_text == "Batch DOCX":
            mode_key = "batch_docx"
        elif mode_text == "Batch Bilingual":
            mode_key = "batch_bilingual"
        
        # Get current prompt for this mode
        prompt = self.system_prompts.get(mode_key, self._get_default_system_prompt(mode_key))
        self.system_prompts_editor.setPlainText(prompt)
    
    def _save_system_prompt(self):
        """Save current System Prompt (Layer 1)"""
        if not hasattr(self, 'system_prompts_editor'):
            return
        
        mode_text = self.system_prompts_mode.currentText()
        mode_key = "single"
        if mode_text == "Batch DOCX":
            mode_key = "batch_docx"
        elif mode_text == "Batch Bilingual":
            mode_key = "batch_bilingual"
        
        content = self.system_prompts_editor.toPlainText()
        self.system_prompts[mode_key] = content
        self._save_system_prompts_file()
        
        self.log_message(f"Saved System Prompt for {mode_text}")
        self._show_message(QMessageBox.Icon.Information, "Saved", f"System Prompt for '{mode_text}' saved successfully.")
    
    def _reset_system_prompt(self):
        """Reset current System Prompt (Layer 1) to default"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Reset to Default")
        msg.setText("Are you sure you want to reset this System Prompt to the default?\n\nThis will discard any customizations.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg.exec()
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        mode_text = self.system_prompts_mode.currentText()
        mode_key = "single"
        if mode_text == "Batch DOCX":
            mode_key = "batch_docx"
        elif mode_text == "Batch Bilingual":
            mode_key = "batch_bilingual"
        
        # Reset to default
        default = self._get_default_system_prompt(mode_key)
        self.system_prompts[mode_key] = default
        self.system_prompts_editor.setPlainText(default)
        self._save_system_prompts_file()
        
        self.log_message(f"Reset System Prompt for {mode_text} to default")
        self._show_message(QMessageBox.Icon.Information, "Reset", f"System Prompt for '{mode_text}' reset to default.")
    
    def _export_system_prompt(self):
        """Export current System Prompt (Layer 1) to file"""
        if not hasattr(self, 'system_prompts_editor'):
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Export System Prompt", "",
            "Text Files (*.txt);;Markdown Files (*.md);;All Files (*.*)"
        )
        if not file_path:
            return
        
        try:
            Path(file_path).write_text(self.system_prompts_editor.toPlainText(), encoding='utf-8')
            self.log_message(f"Exported System Prompt to: {Path(file_path).name}")
            self._show_message(QMessageBox.Icon.Information, "Exported", "System Prompt exported successfully.")
        except Exception as e:
            self._show_message(QMessageBox.Icon.Critical, "Error", f"Failed to export System Prompt:\n{str(e)}")
    
    def _import_system_prompt(self):
        """Import System Prompt (Layer 1) from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Import System Prompt", "",
            "Text Files (*.txt);;Markdown Files (*.md);;All Files (*.*)"
        )
        if not file_path:
            return
        
        try:
            content = Path(file_path).read_text(encoding='utf-8')
            self.system_prompts_editor.setPlainText(content)
            self.log_message(f"Imported System Prompt from: {Path(file_path).name}")
        except Exception as e:
            self._show_message(QMessageBox.Icon.Critical, "Error", f"Failed to import System Prompt:\n{str(e)}")
    
    def get_system_prompt(self, mode="single"):
        """
        Get the System Prompt (Layer 1 - always included)
        Contains memoQ tags, formatting rules, etc.
        
        Args:
            mode: "single", "batch_docx", or "batch_bilingual"
        
        Returns:
            System Prompt string (Layer 1)
        """
        # Load if not already loaded
        if not self.system_prompts:
            self._load_system_prompts()
        
        # Get prompt for mode (defaults to "single" if not found)
        prompt = self.system_prompts.get(mode, self.system_prompts.get("single", self._get_default_system_prompt(mode)))
        
        return prompt
    
    def build_final_prompt(self, source_text, source_lang, target_lang, mode="single"):
        """
        Build final prompt using 4-layer architecture
        
        Args:
            source_text: Text to translate
            source_lang: Source language name
            target_lang: Target language name
            mode: Translation mode ("single", "batch_docx", "batch_bilingual")
        
        Returns:
            Complete prompt string ready to send to LLM
        """
        # Layer 1: System Prompts (always included)
        system_prompt = self.get_system_prompt(mode)
        
        # Replace placeholders in System Prompt
        system_prompt = system_prompt.replace("{{SOURCE_LANGUAGE}}", source_lang)
        system_prompt = system_prompt.replace("{{TARGET_LANGUAGE}}", target_lang)
        system_prompt = system_prompt.replace("{{SOURCE_TEXT}}", source_text)
        
        # Layer 2: Domain Prompts (optional)
        domain_prompt = ""
        if self.active_translate_prompt:
            domain_prompt = self.active_translate_prompt
            # Replace placeholders
            domain_prompt = domain_prompt.replace("{source_lang}", source_lang)
            domain_prompt = domain_prompt.replace("{target_lang}", target_lang)
            domain_prompt = domain_prompt.replace("{{SOURCE_LANGUAGE}}", source_lang)
            domain_prompt = domain_prompt.replace("{{TARGET_LANGUAGE}}", target_lang)
        else:
            domain_prompt = f"You are an expert {source_lang} to {target_lang} translator."
        
        # Layer 3: Project Prompts (optional)
        project_prompt = ""
        if self.active_project_prompt:
            project_prompt = "\n\n# PROJECT-SPECIFIC INSTRUCTIONS\n\n" + self.active_project_prompt
        
        # Layer 4: Style Guide (optional)
        style_guide = ""
        if self.active_style_guide:
            language_label = f" ({self.active_style_guide_language})" if self.active_style_guide_language else ""
            style_guide = "\n\n# STYLE GUIDE & FORMATTING RULES" + language_label + "\n\n" + self.active_style_guide
        
        # Combine all layers
        final_prompt = system_prompt + "\n\n" + domain_prompt + project_prompt + style_guide
        
        return final_prompt

