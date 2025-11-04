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
    QFrame, QDialog, QDialogButtonBox, QApplication, QCheckBox
)
from PyQt6.QtCore import Qt, QSettings, QTimer
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
        self.current_system_prompt_mode = "single"  # Track current System Prompt mode
        
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
        
        # Preview combined prompt button (like tkinter)
        preview_combined_btn = QPushButton("🧪 Preview Combined Prompt")
        preview_combined_btn.setToolTip("Preview the exact combined prompt (all layers) that will be sent to AI with current segment")
        preview_combined_btn.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; padding: 6px 12px;")
        preview_combined_btn.clicked.connect(self._preview_combined_prompt)
        active_bar_layout.addWidget(preview_combined_btn)
        
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
        
        # Prompt Assistant tab (moved to first position)
        assistant_tab = self._create_prompt_assistant_tab()
        self.list_tabs.addTab(assistant_tab, "🤖 Prompt Assistant")
        
        # System Prompts tab (Layer 1)
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
        
        # Hide editor on Prompt Assistant and Style Guides tabs
        tab_text = self.list_tabs.tabText(index)
        if "Prompt Assistant" in tab_text:
            self.editor_panel.setVisible(False)
        elif "Style Guides" in tab_text:
            # Style Guides has its own editor
            self.editor_panel.setVisible(False)
        elif "System Prompts" in tab_text:
            # System Prompts uses shared editor but hide metadata fields
            self.editor_panel.setVisible(True)
            self._configure_editor_for_system_prompts()
        else:
            self.editor_panel.setVisible(True)
            self._configure_editor_for_normal_prompts()
    
    def _create_system_prompts_tab(self) -> QWidget:
        """Create System Prompts (Layer 1) tab for viewing/editing base prompts"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # System Prompts list (similar to Domain Prompts tree)
        self.system_prompts_tree = QTreeWidget()
        self.system_prompts_tree.setHeaderLabels(["System Prompt", "Mode", "Status"])
        self.system_prompts_tree.setColumnWidth(0, 250)
        self.system_prompts_tree.setColumnWidth(1, 150)
        self.system_prompts_tree.setColumnWidth(2, 100)
        self.system_prompts_tree.itemSelectionChanged.connect(self._on_system_prompt_select)
        layout.addWidget(self.system_prompts_tree, 1)
        
        # Buttons (similar to Domain Prompts)
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
        
        # Load system prompts list
        self._load_system_prompts_list()
        
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
        
        btn_layout.addSpacing(10)
        
        deactivate_label = QLabel("✖ Deactivate:")
        deactivate_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        btn_layout.addWidget(deactivate_label)
        
        deactivate_trans_btn = QPushButton("✖ Translation")
        deactivate_trans_btn.clicked.connect(lambda: self._deactivate_domain_expertise('translate'))
        deactivate_trans_btn.setStyleSheet("background-color: #f44336; color: white; padding: 4px 8px;")
        btn_layout.addWidget(deactivate_trans_btn)
        
        deactivate_proof_btn = QPushButton("✖ Proofreading")
        deactivate_proof_btn.clicked.connect(lambda: self._deactivate_domain_expertise('proofread'))
        deactivate_proof_btn.setStyleSheet("background-color: #f44336; color: white; padding: 4px 8px;")
        btn_layout.addWidget(deactivate_proof_btn)
        
        btn_layout.addSpacing(10)
        
        preview_btn = QPushButton("🧪 Preview Prompt")
        preview_btn.clicked.connect(self._preview_domain_prompt)
        preview_btn.setStyleSheet("background-color: #9C27B0; color: white; padding: 4px 8px;")
        btn_layout.addWidget(preview_btn)
        
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
        
        clear_btn = QPushButton("✖ Deactivate")
        clear_btn.clicked.connect(self._clear_project_guideline)
        clear_btn.setStyleSheet("background-color: #f44336; color: white; padding: 4px 8px;")
        btn_layout.addWidget(clear_btn)
        
        btn_layout.addSpacing(10)
        
        preview_btn = QPushButton("🧪 Preview Prompt")
        preview_btn.clicked.connect(self._preview_project_prompt)
        preview_btn.setStyleSheet("background-color: #9C27B0; color: white; padding: 4px 8px;")
        btn_layout.addWidget(preview_btn)
        
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
        """Create Prompt Assistant tab with document analysis and chat interface"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Header
        header_label = QLabel("🤖 Prompt Assistant")
        header_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(header_label)
        
        # Info
        info_label = QLabel("AI-powered document analysis and prompt generation")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; padding: 5px; background-color: #E8F5E9; border-radius: 3px;")
        layout.addWidget(info_label)
        
        # Document Analysis Section
        analysis_group = QGroupBox("📊 Document Analysis")
        analysis_layout = QVBoxLayout(analysis_group)
        
        self.doc_analysis_status = QLabel("No analysis performed yet")
        self.doc_analysis_status.setStyleSheet("color: #999; padding: 5px;")
        analysis_layout.addWidget(self.doc_analysis_status)
        
        analysis_btn_layout = QHBoxLayout()
        
        analyze_btn = QPushButton("🔍 Analyze Document")
        analyze_btn.clicked.connect(self._analyze_current_document)
        analyze_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 6px 12px;")
        analysis_btn_layout.addWidget(analyze_btn)
        
        generate_btn = QPushButton("🎯 Generate Prompts")
        generate_btn.clicked.connect(self._generate_translation_prompts)
        generate_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 6px 12px;")
        analysis_btn_layout.addWidget(generate_btn)
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self._clear_analysis)
        clear_btn.setStyleSheet("background-color: #757575; color: white; padding: 4px 8px;")
        analysis_btn_layout.addWidget(clear_btn)
        
        analysis_btn_layout.addStretch()
        analysis_layout.addLayout(analysis_btn_layout)
        
        layout.addWidget(analysis_group)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: #ddd;")
        layout.addWidget(separator)
        
        # Chat history area
        chat_label = QLabel("💬 AI Assistant Chat")
        chat_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(chat_label)
        
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
            "I can help you understand your document and optimize your translation settings.\n\n"
            "📊 Document Analysis: Click 'Analyze Document' to get AI-powered analysis of your loaded document.\n"
            "🎯 Generate Prompts: After analysis, click 'Generate Prompts' to create optimized System Prompt and Project Prompt.\n\n"
            "Or ask me questions about your prompts!\n"
            "Try asking:\n"
            "- 'Make it more formal'\n"
            "- 'Add emphasis on terminology consistency'\n"
            "- 'Simplify the language'\n"
        )
        
        # Initialize state
        self.doc_analysis_result = None
        
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
        
        # Store references to editor components for System Prompts mode switching
        self.editor_meta_group = meta_group
        self.editor_desc_label = desc_label
        self.editor_description_widget = self.editor_description
        
        return panel
    
    def _configure_editor_for_system_prompts(self):
        """Configure editor panel for System Prompts mode"""
        # Hide metadata fields and description
        if hasattr(self, 'editor_meta_group'):
            self.editor_meta_group.setVisible(False)
        if hasattr(self, 'editor_desc_label'):
            self.editor_desc_label.setVisible(False)
        if hasattr(self, 'editor_description_widget'):
            self.editor_description_widget.setVisible(False)
        
        # Update title
        if hasattr(self, 'editor_panel'):
            layout = self.editor_panel.layout()
            if layout:
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and hasattr(item, 'widget') and item.widget():
                        widget = item.widget()
                        if isinstance(widget, QLabel) and widget.text() == "Prompt Editor":
                            widget.setText("System Prompt Editor")
                            break
    
    def _configure_editor_for_normal_prompts(self):
        """Configure editor panel for normal prompts (Domain/Project)"""
        # Show metadata fields and description
        if hasattr(self, 'editor_meta_group'):
            self.editor_meta_group.setVisible(True)
        if hasattr(self, 'editor_desc_label'):
            self.editor_desc_label.setVisible(True)
        if hasattr(self, 'editor_description_widget'):
            self.editor_description_widget.setVisible(True)
        
        # Update title
        if hasattr(self, 'editor_panel'):
            layout = self.editor_panel.layout()
            if layout:
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and hasattr(item, 'widget') and item.widget():
                        widget = item.widget()
                        if isinstance(widget, QLabel) and "System Prompt" in widget.text():
                            widget.setText("Prompt Editor")
                            break
    
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
    
    def _deactivate_domain_expertise(self, slot):
        """Deactivate Domain Prompt for translation or proofreading"""
        if slot == 'translate':
            if not self.active_translate_prompt:
                self._show_message(QMessageBox.Icon.Information, "No Active Prompt", "No Domain Prompt is currently active for Translation.")
                return
            self.active_translate_prompt = None
            self.active_translate_prompt_name = None
            self.log_message("Deactivated Domain Prompt for Translation")
        elif slot == 'proofread':
            if not self.active_proofread_prompt:
                self._show_message(QMessageBox.Icon.Information, "No Active Prompt", "No Domain Prompt is currently active for Proofreading.")
                return
            self.active_proofread_prompt = None
            self.active_proofread_prompt_name = None
            self.log_message("Deactivated Domain Prompt for Proofreading")
        
        self._update_active_display()
        self._load_domain_expertise()  # Refresh to remove bold
    
    def _preview_domain_prompt(self):
        """Preview the exact prompt that will be sent to AI for Domain Prompts"""
        items = self.domain_tree.selectedItems()
        if not items:
            self._show_message(QMessageBox.Icon.Warning, "No Selection", "Please select a Domain Prompt to preview.")
            return
        
        item = items[0]
        filename = item.data(0, Qt.ItemDataRole.UserRole)
        if not filename:
            return
        
        prompt_data = self.prompt_library.get_prompt(filename)
        if not prompt_data:
            return
        
        # Get the prompt content
        prompt_text = prompt_data.get('translate_prompt', '')
        if not prompt_text:
            self._show_message(QMessageBox.Icon.Warning, "No Prompt", "Selected prompt has no content.")
            return
        
        # Build the full prompt that would be sent (without actual source text)
        source_lang = "English"  # Default
        target_lang = "Dutch"  # Default
        
        # Try to get from parent app if available
        if hasattr(self.parent_app, 'current_project'):
            if self.parent_app.current_project:
                source_lang = getattr(self.parent_app.current_project, 'source_lang', source_lang)
                target_lang = getattr(self.parent_app.current_project, 'target_lang', target_lang)
        
        # Build final prompt
        full_prompt = self.build_final_prompt(
            source_text="[Source text will appear here]",
            source_lang=source_lang,
            target_lang=target_lang,
            mode="single"
        )
        
        # Show preview dialog
        self._show_prompt_preview_dialog(full_prompt, f"Domain Prompt: {prompt_data.get('name', 'Unnamed')}", source_lang, target_lang)
    
    def _preview_project_prompt(self):
        """Preview the exact prompt that will be sent to AI for Project Prompts"""
        items = self.project_tree.selectedItems()
        if not items:
            self._show_message(QMessageBox.Icon.Warning, "No Selection", "Please select a Project Prompt to preview.")
            return
        
        item = items[0]
        filename = item.data(0, Qt.ItemDataRole.UserRole)
        if not filename:
            return
        
        prompt_data = self.prompt_library.get_prompt(filename)
        if not prompt_data:
            return
        
        # Get the prompt content
        prompt_text = prompt_data.get('translate_prompt', '') or prompt_data.get('content', '')
        if not prompt_text:
            self._show_message(QMessageBox.Icon.Warning, "No Prompt", "Selected prompt has no content.")
            return
        
        # Build the full prompt that would be sent (without actual source text)
        source_lang = "English"  # Default
        target_lang = "Dutch"  # Default
        
        # Try to get from parent app if available
        if hasattr(self.parent_app, 'current_project'):
            if self.parent_app.current_project:
                source_lang = getattr(self.parent_app.current_project, 'source_lang', source_lang)
                target_lang = getattr(self.parent_app.current_project, 'target_lang', target_lang)
        
        # Temporarily activate this prompt to build the full prompt
        old_active = self.active_project_prompt
        self.active_project_prompt = prompt_text
        
        try:
            full_prompt = self.build_final_prompt(
                source_text="[Source text will appear here]",
                source_lang=source_lang,
                target_lang=target_lang,
                mode="single"
            )
        finally:
            self.active_project_prompt = old_active
        
        # Show preview dialog
        self._show_prompt_preview_dialog(full_prompt, f"Project Prompt: {prompt_data.get('name', 'Unnamed')}", source_lang, target_lang)
    
    def _show_prompt_preview_dialog(self, prompt_text, title, source_lang, target_lang):
        """Show a dialog with the exact prompt that will be sent to AI"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QDialogButtonBox, QApplication
        from PyQt6.QtGui import QFont
        
        dialog = QDialog()
        dialog.setWindowTitle("🧪 Prompt Preview - What AI Will Receive")
        dialog.resize(900, 700)
        
        layout = QVBoxLayout(dialog)
        
        # Header
        header_label = QLabel(f"<h3>{title}</h3>")
        header_label.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 3px;")
        layout.addWidget(header_label)
        
        # Info
        info_label = QLabel(f"<b>Languages:</b> {source_lang} → {target_lang}<br><b>This is the EXACT prompt that will be sent to the AI</b>")
        info_label.setStyleSheet("background-color: #E3F2FD; padding: 8px; border-radius: 3px; margin: 5px 0;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Prompt text
        prompt_text_edit = QTextEdit()
        prompt_text_edit.setPlainText(prompt_text)
        prompt_text_edit.setReadOnly(True)
        prompt_text_edit.setFont(QFont("Consolas", 9))
        prompt_text_edit.setStyleSheet("background-color: #f5f5f5; border: 1px solid #ccc; padding: 5px;")
        layout.addWidget(prompt_text_edit, 1)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Copy)
        copy_btn = button_box.button(QDialogButtonBox.StandardButton.Copy)
        copy_btn.setText("📋 Copy to Clipboard")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(prompt_text))
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.exec()
    
    def _preview_combined_prompt(self):
        """Preview the complete combined prompt (all layers) with current segment - like tkinter"""
        # Check if project is loaded and has segments
        if not hasattr(self.parent_app, 'current_project') or not self.parent_app.current_project:
            self._show_message(
                QMessageBox.Icon.Warning,
                "No Project",
                "Please load a project with segments first.\n\nThe preview shows the exact prompt that will be sent to the AI for the currently selected segment."
            )
            return
        
        # Get current segment from grid
        current_segment = None
        if hasattr(self.parent_app, 'table') and self.parent_app.table:
            current_row = self.parent_app.table.currentRow()
            if current_row >= 0:
                # Map display row to actual segment index (handles pagination)
                if hasattr(self.parent_app, 'grid_row_to_segment_index') and current_row in self.parent_app.grid_row_to_segment_index:
                    actual_index = self.parent_app.grid_row_to_segment_index[current_row]
                    if actual_index < len(self.parent_app.current_project.segments):
                        current_segment = self.parent_app.current_project.segments[actual_index]
        
        if not current_segment:
            self._show_message(
                QMessageBox.Icon.Information,
                "No Segment Selected",
                "Please select a segment in the grid to preview the prompt.\n\nThe preview will show how all prompt layers (System, Domain, Project, Style Guide) are combined for that segment."
            )
            return
        
        # Get languages
        source_lang = getattr(self.parent_app.current_project, 'source_lang', 'English')
        target_lang = getattr(self.parent_app.current_project, 'target_lang', 'Dutch')
        
        # Build the FULL combined prompt using build_final_prompt
        full_prompt = self.build_final_prompt(
            source_text=current_segment.source,
            source_lang=source_lang,
            target_lang=target_lang,
            mode="single"
        )
        
        # Build composition breakdown
        composition_parts = []
        composition_parts.append(f"• System Prompt (Layer 1): {len(self.get_system_prompt('single'))} characters")
        
        if self.active_translate_prompt:
            composition_parts.append(f"• Domain Prompt (Layer 2 - {self.active_translate_prompt_name}): {len(self.active_translate_prompt)} characters")
        else:
            composition_parts.append("• Domain Prompt (Layer 2): Default")
        
        if self.active_project_prompt:
            composition_parts.append(f"• Project Prompt (Layer 3 - {self.active_project_prompt_name}): {len(self.active_project_prompt)} characters")
        else:
            composition_parts.append("• Project Prompt (Layer 3): None")
        
        if self.active_style_guide:
            style_name = self.active_style_guide_name or "Active"
            composition_parts.append(f"• Style Guide (Layer 4 - {style_name}): {len(self.active_style_guide)} characters")
        else:
            composition_parts.append("• Style Guide (Layer 4): None")
        
        composition_parts.append(f"• Total prompt length: {len(full_prompt)} characters")
        composition_text = "\n".join(composition_parts)
        
        # Show preview dialog with full combined prompt
        self._show_combined_prompt_preview_dialog(
            full_prompt,
            f"{source_lang} → {target_lang} | Segment #{current_segment.id}",
            composition_text,
            current_segment.source
        )
    
    def _show_combined_prompt_preview_dialog(self, prompt_text, header_text, composition_text, source_text):
        """Show dialog with combined prompt preview - matches tkinter style"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QDialogButtonBox, QApplication
        from PyQt6.QtGui import QFont, QTextCharFormat, QTextCursor
        from PyQt6.QtCore import Qt
        
        dialog = QDialog()
        dialog.setWindowTitle("🧪 Complete Prompt Preview - What AI Will Receive")
        dialog.resize(900, 700)
        
        layout = QVBoxLayout(dialog)
        
        # Header (blue background like tkinter)
        header_label = QLabel(f"<h3>🧪 Complete Prompt Preview</h3><p>{header_text}</p>")
        header_label.setStyleSheet("background-color: #2196F3; color: white; padding: 15px; border-radius: 3px;")
        header_label.setWordWrap(True)
        layout.addWidget(header_label)
        
        # Info panel (light blue like tkinter)
        info_label = QLabel(f"💡 <b>This is the EXACT prompt that will be sent to the AI</b><br><br>📋 <b>Composition:</b><br>{composition_text.replace(chr(10), '<br>')}")
        info_label.setStyleSheet("background-color: #E3F2FD; padding: 10px; border-radius: 3px; margin: 5px 0;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Prompt text area
        prompt_text_edit = QTextEdit()
        prompt_text_edit.setPlainText(prompt_text)
        prompt_text_edit.setReadOnly(True)
        prompt_text_edit.setFont(QFont("Consolas", 9))
        prompt_text_edit.setStyleSheet("background-color: #f5f5f5; border: 1px solid #ccc; padding: 5px;")
        
        # Highlight source text (like tkinter)
        if source_text and source_text in prompt_text:
            cursor = prompt_text_edit.textCursor()
            format = QTextCharFormat()
            format.setBackground(Qt.GlobalColor.yellow)
            format.setFontWeight(QFont.Weight.Bold)
            
            # Find and highlight source text
            text = prompt_text_edit.toPlainText()
            start_pos = text.find(source_text)
            if start_pos >= 0:
                cursor.setPosition(start_pos)
                cursor.setPosition(start_pos + len(source_text), QTextCursor.MoveMode.KeepAnchor)
                cursor.setCharFormat(format)
                prompt_text_edit.setTextCursor(cursor)
        
        layout.addWidget(prompt_text_edit, 1)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Copy)
        copy_btn = button_box.button(QDialogButtonBox.StandardButton.Copy)
        copy_btn.setText("📋 Copy to Clipboard")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(prompt_text))
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.exec()
    
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
        # Check if we're in System Prompts mode
        tab_text = self.list_tabs.tabText(self.list_tabs.currentIndex()) if hasattr(self, 'list_tabs') else ""
        if "System Prompts" in tab_text:
            self._save_system_prompt()
            return
        
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
        # Check if we're in System Prompts mode
        tab_text = self.list_tabs.tabText(self.list_tabs.currentIndex()) if hasattr(self, 'list_tabs') else ""
        if "System Prompts" in tab_text:
            self._reset_system_prompt()
            return
        
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
        # System Prompts cannot be deleted, only reset
        tab_text = self.list_tabs.tabText(self.list_tabs.currentIndex()) if hasattr(self, 'list_tabs') else ""
        if "System Prompts" in tab_text:
            self._show_message(QMessageBox.Icon.Information, "Cannot Delete", "System Prompts cannot be deleted. Use 'Reset to Default' to restore default values.")
            return
        
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
    
    def _analyze_current_document(self):
        """Analyze the currently loaded document"""
        # Check if project is loaded
        if not hasattr(self.parent_app, 'current_project') or not self.parent_app.current_project:
            QMessageBox.warning(
                self.parent_app if self.parent_app else None,
                "No Document",
                "Please load a document or create a project first"
            )
            return
        
        # Check if LLM is configured
        if not hasattr(self.parent_app, 'load_api_keys'):
            QMessageBox.critical(
                self.parent_app if self.parent_app else None,
                "Configuration Error",
                "Cannot access API keys. Please check application configuration."
            )
            return
        
        api_keys = self.parent_app.load_api_keys()
        
        # Get LLM settings
        if not hasattr(self.parent_app, 'load_llm_settings'):
            QMessageBox.critical(
                self.parent_app if self.parent_app else None,
                "Configuration Error",
                "Cannot access LLM settings. Please check application configuration."
            )
            return
        
        settings = self.parent_app.load_llm_settings()
        provider = settings.get('provider', 'openai')
        
        # Map provider to API key name
        api_key_map = {
            'openai': 'openai',
            'claude': 'claude',
            'gemini': 'google'
        }
        api_key_name = api_key_map.get(provider)
        
        if not api_keys.get(api_key_name):
            QMessageBox.warning(
                self.parent_app if self.parent_app else None,
                "API Key Missing",
                f"Please configure {provider.upper()} API key in Settings → LLM Settings first."
            )
            return
        
        # Update status
        self.doc_analysis_status.setText("⏳ Analyzing document with AI...")
        self.doc_analysis_status.setStyleSheet("color: #FF9800; padding: 5px;")
        
        # Get segments
        project = self.parent_app.current_project
        source_texts = [seg.source for seg in project.segments if seg.source]
        
        if not source_texts:
            QMessageBox.warning(
                self.parent_app if self.parent_app else None,
                "No Content",
                "No source text found in the document."
            )
            self.doc_analysis_status.setText("❌ No content to analyze")
            self.doc_analysis_status.setStyleSheet("color: #D32F2F; padding: 5px;")
            return
        
        full_text = "\n".join(source_texts)
        
        # Truncate if too long (roughly 10000 tokens = 7500 words)
        words = full_text.split()
        if len(words) > 8000:
            full_text = " ".join(words[:8000]) + "\n\n[...document continues...]"
        
        # Get languages
        source_lang = project.source_lang or "English"
        target_lang = project.target_lang or "Dutch"
        
        # Show message in chat
        self._add_chat_message("system", f"🤔 Analyzing {len(words)} words with {provider.upper()}...")
        
        # Import threading to run async
        import threading
        
        def perform_analysis():
            try:
                # Build intelligent analysis prompt (fully domain-agnostic, works for ALL document types)
                system_prompt = f"""You are a professional translator working between {source_lang} and {target_lang}.

The user is translating a document and needs your help with terminology and translation questions.

Your analysis should be comprehensive and practical for professional translation work. Adapt your approach based on the document type you identify."""

                user_prompt = f"""Please analyze this document carefully, examining its content, structure, and terminology. Provide me with a detailed high-level summary and a comprehensive bilingual termbase of key terms. I will use your response to help configure an AI-powered translation tool for sentence-by-sentence translation.

**Document text ({source_lang}):**

{full_text}

**Please provide:**

1. **High-level summary** (2-4 paragraphs):
   - What is the main subject/topic?
   - What problems does it address or what is its purpose?
   - What are the key features, components, concepts, or methods described?
   - What is the overall significance or application?

2. **Document type and technical domain**: First identify the document type, then specify the domain:
   - Document types: patent, medical report, legal contract, technical manual, user guide, marketing material, scientific paper, regulatory document, etc.
   - Technical domains: civil engineering, medical devices, pharmaceuticals, software, mechanical engineering, legal/regulatory, finance, etc.

3. **Bilingual termbase of key technical terms** in markdown table format:

| {source_lang} term | {target_lang} equivalent | Notes / context |
|-------------------|------------------------|------------------|

**CRITICAL termbase INSTRUCTIONS:**
- Extract 25-40 of the most important domain-specific terms (not exhaustive, focus on quality)
- IGNORE common words: articles (de, het, een), pronouns (deze, dit), prepositions (van, in, op)
- IGNORE section headers like "DESCRIPTION", "FIGURES", "INTRODUCTION" unless they're technical terms
- Focus on: specialized terminology, key concepts, technical components, processes, legal/medical/technical jargon
- For patents: emphasize claimed elements, structural components, technical features, materials, methods
- For medical: focus on anatomical terms, procedures, medications, conditions, measurements
- For legal: emphasize legal terms, clauses, obligations, definitions, regulatory references
- For technical manuals: focus on components, operations, specifications, safety terms
- Include compound terms and multi-word technical expressions
- Provide helpful context notes for each term (usage, synonyms, technical meaning, register)
- When multiple translations exist, list them separated by / (e.g., "joint plate / expansion joint plate")

Your response will help configure an AI translation tool for professional-quality sentence-by-sentence translation."""
                
                # Call LLM using parent app's LLM client
                from modules.llm_clients import LLMClient
                
                client = LLMClient(
                    api_key=api_keys[api_key_name],
                    provider=provider,
                    model=settings.get(f'{provider}_model', 'gpt-4o')
                )
                
                # Build custom prompt with system and user parts
                full_custom_prompt = f"{system_prompt}\n\n{user_prompt}"
                
                # Call LLM - pass custom prompt
                # Use a placeholder text since translate() expects text parameter
                # The actual analysis request is in the custom_prompt
                analysis_text = client.translate(
                    text="Analyze this document.",  # Placeholder - actual request is in custom_prompt
                    source_lang=source_lang,
                    target_lang=target_lang,
                    custom_prompt=full_custom_prompt
                )
                
                # Clean the response to remove any prompt remnants
                analysis_text = client._clean_translation_response(analysis_text, full_custom_prompt)
                
                # Store result
                analysis_result['result'] = {
                    'success': True,
                    'analysis': analysis_text,
                    'segment_count': len(project.segments),
                    'word_count': len(words),
                    'source_lang': source_lang,
                    'target_lang': target_lang
                }
                analysis_result['completed'] = True
                
                # Update status (thread-safe UI update)
                QTimer.singleShot(0, lambda: self.doc_analysis_status.setText(
                    f"✓ Analysis complete: {len(project.segments)} segments analyzed with AI"
                ))
                QTimer.singleShot(0, lambda: self.doc_analysis_status.setStyleSheet("color: #388E3C; padding: 5px;"))
                
                # Add to chat (thread-safe UI update)
                QTimer.singleShot(0, lambda: self._add_chat_message("assistant", f"**Document Analysis Complete**\n\n{analysis_text}"))
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                analysis_result['error'] = str(e)
                analysis_result['completed'] = True
                # Update status (thread-safe UI update)
                QTimer.singleShot(0, lambda: self.doc_analysis_status.setText(f"❌ Error: {str(e)}"))
                QTimer.singleShot(0, lambda: self.doc_analysis_status.setStyleSheet("color: #D32F2F; padding: 5px;"))
                QTimer.singleShot(0, lambda: self._add_chat_message("error", f"Error during analysis: {str(e)}"))
        
        # Run in background thread to avoid blocking UI
        analysis_thread = threading.Thread(target=perform_analysis, daemon=True)
        analysis_thread.start()
        
        # Set up timeout mechanism (120 seconds = 2 minutes)
        def check_timeout():
            import time
            start_time = time.time()
            timeout_seconds = 120
            
            while not analysis_result['completed']:
                import time
                if time.time() - start_time > timeout_seconds:
                    # Timeout occurred
                    analysis_result['completed'] = True
                    analysis_result['error'] = f"Analysis timed out after {timeout_seconds} seconds. The document may be too large or the API is slow."
                    QTimer.singleShot(0, lambda: self.doc_analysis_status.setText(f"❌ Timeout: Analysis took longer than {timeout_seconds} seconds"))
                    QTimer.singleShot(0, lambda: self.doc_analysis_status.setStyleSheet("color: #D32F2F; padding: 5px;"))
                    QTimer.singleShot(0, lambda: self._add_chat_message("error", f"Document analysis timed out after {timeout_seconds} seconds. Try with a smaller document or check your API connection."))
                    break
                import time
                time.sleep(1)  # Check every second
        
        # Start timeout checker in separate thread
        threading.Thread(target=check_timeout, daemon=True).start()
    
    def _generate_translation_prompts(self):
        """Generate ready-to-use System Prompt and Custom Instructions based on document analysis"""
        if not self.doc_analysis_result:
            QMessageBox.information(
                self.parent_app if self.parent_app else None,
                "Analyze First",
                "Please analyze the document first by clicking 'Analyze Document'"
            )
            return
        
        # Check if LLM is configured
        api_keys = self.parent_app.load_api_keys()
        settings = self.parent_app.load_llm_settings()
        provider = settings.get('provider', 'openai')
        
        api_key_map = {
            'openai': 'openai',
            'claude': 'claude',
            'gemini': 'google'
        }
        api_key_name = api_key_map.get(provider)
        
        if not api_keys.get(api_key_name):
            QMessageBox.warning(
                self.parent_app if self.parent_app else None,
                "API Key Missing",
                f"Please configure {provider.upper()} API key in Settings → LLM Settings first."
            )
            return
        
        # Show thinking indicator
        self._add_chat_message("system", "🤔 Generating optimized prompts based on your document analysis...")
        
        # Get the previous analysis
        analysis_text = self.doc_analysis_result.get('analysis', '')
        source_lang = self.doc_analysis_result.get('source_lang', 'English')
        target_lang = self.doc_analysis_result.get('target_lang', 'Dutch')
        segment_count = self.doc_analysis_result.get('segment_count', 0)
        
        # Build prompt to generate actionable System Prompt + Custom Instructions
        system_prompt = f"""You are an expert translation workflow consultant helping configure a CAT tool.

The user has just analyzed their document and received the following analysis:

{analysis_text}

Your task is to generate TWO separate, ready-to-use prompts for the translator:

1. **SYSTEM PROMPT** (Global translation strategy - goes in "System Prompts" section)
   - This should be a COMPLETE, ready-to-use prompt that defines HOW to translate
   - Include the translation direction using PLACEHOLDERS: {{SOURCE_LANGUAGE}} → {{TARGET_LANGUAGE}}
   - Specify the domain, tone, register, terminology handling GENERALLY (not document-specific)
   - Include specific translation strategies for this document type
   - Make it GENERIC and REUSABLE for similar documents in this domain
   - Should be 3-5 paragraphs, comprehensive but focused
   - Do NOT include specific termbase terms - keep it general
   - Use {{SOURCE_LANGUAGE}} and {{TARGET_LANGUAGE}} placeholders, NOT specific language names
   
   **CRITICAL REQUIREMENTS - You MUST include ALL of these in your System Prompt:**
   
   **LANGUAGE AGNOSTIC RULE**: All examples and instructions must use {{SOURCE_LANGUAGE}} and {{TARGET_LANGUAGE}} placeholders. NEVER hardcode specific language pairs (like English→Dutch). The prompt must work for ANY translation direction.
   
   a) **Professional Context**: Explain this is professional translation work for regulatory compliance, medical/technical terminology for legitimate professional purposes, NOT medical advice
   
   b) **Translation Role**: Define yourself as an expert {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}} translator with deep understanding of context and nuance
   
   c) **Context Availability**: Mention that full document context may be provided for reference
   
   d) **Task Definition**: Clearly specify the translation task (translate ONLY specified text, not full document)
   
   e) **Output Format**: 
     - Provide ONLY the translated text
     - Do NOT include numbering, labels, or commentary
     - Do NOT repeat the source text
     - Maintain accuracy and natural fluency
   
   f) **CAT TOOL TAG PRESERVATION** (CRITICAL - preserve ALL of these):
     - memoQ tags: [1}}, {{2}}, [3}}, {{4}} (asymmetric bracket-brace pairs)
     - Trados Studio tags: <410>text</410>, <434>text</434> (XML-style opening/closing tags)
     - CafeTran tags: |formatted text| (pipe symbols mark formatted text - bold, italic, underline, etc.)
     - Other CAT tools: various bracketed or special character sequences
     - These are placeholder tags representing formatting (bold, italic, links, etc.)
     - PRESERVE ALL tags - if source has N tags, target must have exactly N tags
     - Keep tags with their content, adjust position for natural target language word order
     - Never translate, omit, or modify the tags themselves - only reposition them
     - Include MULTIPLE examples but use GENERIC examples that work for ANY language pair
     - Examples should show structure/format, NOT specific language pairs (e.g., '[1}}Source Text{{2}}' → '[1}}Target Text{{2}}')
   
   g) **SPECIAL RULE FOR UICONTROL TAGS** (memoQ bilingual DOCX - CRITICAL):
     - Text in [uicontrol id="GUID"}}Original Text{{uicontrol] tags must keep original + add translation in parentheses
     - Structure: [uicontrol id="GUID"}}Original {{SOURCE_LANGUAGE}} Text{{uicontrol]: Description
     - Format: [uicontrol id="GUID"}}Original {{SOURCE_LANGUAGE}} Text ({{TARGET_LANGUAGE}} Translation){{uicontrol]: {{TARGET_LANGUAGE}} Description
     - Keep original {{SOURCE_LANGUAGE}} text unchanged, add {{TARGET_LANGUAGE}} translation in parentheses
     - Include GENERIC example using placeholders or structure only (e.g., [uicontrol id="GUID-X"}}Original Text{{uicontrol]: Description → [uicontrol id="GUID-X"}}Original Text (Translation){{uicontrol]: Translated Description)
     - DO NOT hardcode specific language pairs (e.g., English→Dutch) - must work for ANY direction
   
   h) **LANGUAGE-SPECIFIC NUMBER FORMATTING**:
     - For Dutch/French/German/Italian/Spanish (continental European): use comma as decimal separator, space or non-breaking space before unit (e.g., 17,1 cm)
     - For English/Irish: use period as decimal separator, no space before unit (e.g., 17.1 cm)
     - Always follow the number formatting conventions of the target language
   
   i) **Optional: Figure References**: If applicable, mention figures (e.g., 'Figure 1A') may have relevant images provided for visual context

2. **CUSTOM INSTRUCTIONS** (Project-specific guidance - goes in "Custom Instructions" tab)
   - Start with 2-3 paragraphs of SPECIFIC guidance for THIS document
   - Then include the KEY TERMINOLOGY section
   
   **CRITICAL: termbase TABLE REQUIREMENTS**
   - You MUST copy the ENTIRE bilingual termbase table from the analysis above
   - Copy it VERBATIM - every single row, word-for-word
   - The table header must be: | {source_lang} term | {target_lang} equivalent | Notes / context |
   - Include the separator line: |------------|--------------------|-----------------| 
   - Then copy EVERY SINGLE ROW from the analysis termbase
   - If there are 33 terms in the analysis, there must be 33 rows in your output
   - DO NOT STOP until you've copied the LAST row of the termbase
   - After the complete table, add 2-3 paragraphs with specific examples
   
   Reference specific key terms with translation examples
   Mention specific challenges identified in the analysis
   Include domain-specific requirements (e.g., for patents: maintain claim structure, legal accuracy)
   List terminology consistency rules with concrete examples from the termbase
   Highlight any special handling needed (measurements, figures, technical processes)

Format your response EXACTLY like this:

---SYSTEM PROMPT---
[Full system prompt text here, ready to copy-paste]

---CUSTOM INSTRUCTIONS---
[Full custom instructions text here, ready to copy-paste]

---

Be specific, practical, and actionable. The translator should be able to copy these directly into Supervertaler."""

        user_prompt = f"""Based on the document analysis above, generate optimized translation prompts.

Document context:
- Source: {source_lang}
- Target: {target_lang}
- {segment_count} segments to translate

Provide the two prompts in the specified format."""
        
        # Import threading to run async
        import threading
        
        def perform_generation():
            try:
                # Call LLM
                from modules.llm_clients import LLMClient
                
                client = LLMClient(
                    api_key=api_keys[api_key_name],
                    provider=provider,
                    model=settings.get(f'{provider}_model', 'gpt-4o')
                )
                
                # Build custom prompt
                full_custom_prompt = f"{system_prompt}\n\n{user_prompt}"
                
                # Call LLM - pass custom prompt (use empty text, analysis is in prompt)
                ai_response = client.translate(
                    text="",  # Empty text, generation is in the prompt itself
                    source_lang=source_lang,
                    target_lang=target_lang,
                    custom_prompt=full_custom_prompt
                )
                
                # Show generated prompts dialog (thread-safe UI update)
                QTimer.singleShot(0, lambda: self._show_generated_prompts_dialog(ai_response, source_lang, target_lang))
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                QTimer.singleShot(0, lambda: self._add_chat_message("error", f"Error generating prompts: {str(e)}"))
                QTimer.singleShot(0, lambda: QMessageBox.critical(
                    self.parent_app if self.parent_app else None,
                    "Generation Error",
                    f"Failed to generate prompts:\n\n{str(e)}"
                ))
        
        # Run in background thread
        threading.Thread(target=perform_generation, daemon=True).start()
    
    def _clear_analysis(self):
        """Clear analysis results and chat history"""
        self.doc_analysis_result = None
        self.doc_analysis_status.setText("No analysis performed yet")
        self.doc_analysis_status.setStyleSheet("color: #999; padding: 5px;")
        self.assistant_chat.setPlainText(
            "Welcome to Prompt Assistant!\n\n"
            "I can help you understand your document and optimize your translation settings.\n\n"
            "📊 Document Analysis: Click 'Analyze Document' to get AI-powered analysis of your loaded document.\n"
            "🎯 Generate Prompts: After analysis, click 'Generate Prompts' to create optimized System Prompt and Project Prompt.\n\n"
            "Or ask me questions about your prompts!\n"
            "Try asking:\n"
            "- 'Make it more formal'\n"
            "- 'Add emphasis on terminology consistency'\n"
            "- 'Simplify the language'\n"
        )
        self.log_message("Analysis results and chat history cleared")
    
    def _add_chat_message(self, role: str, message: str):
        """Add a message to the chat display"""
        prefix = {
            'system': '🤖 System',
            'assistant': '🤖 Assistant',
            'error': '❌ Error',
            'warning': '⚠️ Warning'
        }.get(role, '💬')
        
        self.assistant_chat.appendPlainText(f"\n{prefix}: {message}\n")
    
    def _show_generated_prompts_dialog(self, ai_response, source_lang, target_lang):
        """Display generated prompts in an interactive dialog with copy/apply actions"""
        # Parse the AI response to extract System Prompt and Custom Instructions
        try:
            # Split by the main delimiters
            if "---SYSTEM PROMPT---" in ai_response and "---CUSTOM INSTRUCTIONS---" in ai_response:
                parts = ai_response.split("---SYSTEM PROMPT---")
                remainder = parts[1].split("---CUSTOM INSTRUCTIONS---")
                system_prompt_text = remainder[0].strip()
                # DON'T split on --- again - take everything after ---CUSTOM INSTRUCTIONS---
                custom_instructions_text = remainder[1].strip()
                # Only remove trailing --- if it exists at the very end
                if custom_instructions_text.endswith("---"):
                    custom_instructions_text = custom_instructions_text[:-3].strip()
            else:
                # Fallback: try to parse without delimiters
                system_prompt_text = ai_response[:len(ai_response)//2]
                custom_instructions_text = ai_response[len(ai_response)//2:]
        except Exception as e:
            self.log_message(f"⚠️ Error parsing AI response: {str(e)}")
            system_prompt_text = ai_response
            custom_instructions_text = "See System Prompt above for complete guidance."
        
        # Store generated prompts in project for later retrieval
        from datetime import datetime
        self.generated_prompts = {
            'system_prompt': system_prompt_text,
            'custom_instructions': custom_instructions_text,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'generated_at': datetime.now().isoformat()
        }
        self.log_message("💾 Generated prompts stored")
        
        # Create dialog
        dialog = QDialog(self.parent_app if self.parent_app else None)
        dialog.setWindowTitle(f"Generated Translation Prompts - {source_lang} → {target_lang}")
        dialog.setMinimumSize(950, 800)
        
        layout = QVBoxLayout(dialog)
        
        # Header
        header_label = QLabel("🎯 Ready-to-Use Translation Prompts")
        header_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #2E7D32; padding: 10px; background-color: #E8F5E9; border-radius: 3px;")
        layout.addWidget(header_label)
        
        info_label = QLabel(
            "Generated based on your document analysis. Copy or apply directly to your translation setup."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(info_label)
        
        # Tab widget
        tabs = QTabWidget()
        
        # System Prompt Tab
        sys_tab = QWidget()
        sys_layout = QVBoxLayout(sys_tab)
        
        sys_info = QLabel(
            "This prompt will be saved as a Domain Prompt in your Prompt Library"
        )
        sys_info.setWordWrap(True)
        sys_info.setStyleSheet("color: #1976D2; padding: 5px; background-color: #E3F2FD; border-radius: 3px;")
        sys_layout.addWidget(sys_info)
        
        sys_text = QTextEdit()
        sys_text.setPlainText(system_prompt_text)
        sys_text.setReadOnly(True)
        sys_layout.addWidget(sys_text, 1)
        
        sys_btn_layout = QHBoxLayout()
        
        auto_activate_sys = QCheckBox("✓ Automatically activate for this project")
        auto_activate_sys.setChecked(True)
        sys_btn_layout.addWidget(auto_activate_sys)
        sys_btn_layout.addStretch()
        
        def save_system_prompt():
            """Save System Prompt as Domain Prompt"""
            # Ask for filename
            doc_type = "Custom"
            if "patent" in system_prompt_text.lower():
                doc_type = "Patent"
            elif "medical" in system_prompt_text.lower():
                doc_type = "Medical"
            elif "legal" in system_prompt_text.lower():
                doc_type = "Legal"
            elif "technical" in system_prompt_text.lower():
                doc_type = "Technical"
            
            name, ok = QInputDialog.getText(
                dialog,
                "Save System Prompt",
                f"Enter a name for this System Prompt:\n(will be saved as Domain Prompt):",
                text=f"{doc_type}_{source_lang}_to_{target_lang}"
            )
            
            if not ok or not name:
                return
            
            # Determine domain
            domain_map = {
                "Patent": "Intellectual Property",
                "Medical": "Medical/Healthcare",
                "Legal": "Legal/Regulatory",
                "Technical": "Technical/Engineering"
            }
            domain = domain_map.get(doc_type, "General")
            
            # Replace language names with placeholders
            prompt_with_placeholders = system_prompt_text.replace(source_lang, "{source_lang}").replace(target_lang, "{target_lang}")
            
            # Create prompt data
            prompt_data = {
                "name": name,
                "description": f"AI-generated system prompt for translation in {doc_type.lower()} domain",
                "domain": domain,
                "version": "1.0",
                "task_type": "Translation",
                "created": datetime.now().strftime("%Y-%m-%d"),
                "modified": datetime.now().strftime("%Y-%m-%d"),
                "translate_prompt": prompt_with_placeholders,
                "proofread_prompt": ""
            }
            
            # Save file as Markdown
            try:
                # Use prompt library's dict_to_markdown
                system_prompts_dir = self.user_data_path / "Prompt_Library" / "System_prompts"
                filename = f"{name} (system prompt).md"
                filepath = system_prompts_dir / filename
                
                self.prompt_library.dict_to_markdown(prompt_data, str(filepath))
                
                self.log_message(f"✓ Saved System Prompt to: {filepath}")
                
                # Reload prompt library
                self.prompt_library.load_all_prompts()
                self._load_domain_expertise()  # Refresh Domain Prompts list
                
                # Auto-activate if checked
                if auto_activate_sys.isChecked():
                    # Find the prompt in the domain tree and activate it
                    # We need to select it in the tree first
                    for i in range(self.domain_tree.topLevelItemCount()):
                        item = self.domain_tree.topLevelItem(i)
                        if item and item.data(0, Qt.ItemDataRole.UserRole) == filename:
                            self.domain_tree.setCurrentItem(item)
                            self._activate_domain_expertise('translate')
                            self.log_message("✅ System Prompt automatically activated")
                            break
                
                QMessageBox.information(
                    self.parent_app if self.parent_app else None,
                    "Saved!",
                    f"System Prompt saved as:\n{filename}\n\n"
                    f"Location: {system_prompts_dir}\n\n"
                    f"It will now appear in your Prompt Manager → Domain Prompts section."
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self.parent_app if self.parent_app else None,
                    "Error",
                    f"Failed to save:\n{str(e)}"
                )
        
        def copy_system_prompt():
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(system_prompt_text)
            QMessageBox.information(
                self.parent_app if self.parent_app else None,
                "Copied!",
                "System Prompt copied to clipboard!"
            )
        
        save_sys_btn = QPushButton("💾 Save as Domain Prompt")
        save_sys_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 6px 12px;")
        save_sys_btn.clicked.connect(save_system_prompt)
        sys_btn_layout.addWidget(save_sys_btn)
        
        copy_sys_btn = QPushButton("📋 Copy to Clipboard")
        copy_sys_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 6px 12px;")
        copy_sys_btn.clicked.connect(copy_system_prompt)
        sys_btn_layout.addWidget(copy_sys_btn)
        
        sys_layout.addLayout(sys_btn_layout)
        tabs.addTab(sys_tab, "📋 System Prompt (Global Strategy)")
        
        # Custom Instructions Tab
        custom_tab = QWidget()
        custom_layout = QVBoxLayout(custom_tab)
        
        custom_info = QLabel(
            "These custom instructions will be saved as a Project Prompt in your Prompt Library"
        )
        custom_info.setWordWrap(True)
        custom_info.setStyleSheet("color: #F57C00; padding: 5px; background-color: #FFF3E0; border-radius: 3px;")
        custom_layout.addWidget(custom_info)
        
        custom_text = QTextEdit()
        custom_text.setPlainText(custom_instructions_text)
        custom_text.setReadOnly(True)
        custom_layout.addWidget(custom_text, 1)
        
        custom_btn_layout = QHBoxLayout()
        
        auto_activate_custom = QCheckBox("✓ Automatically activate for this project")
        auto_activate_custom.setChecked(True)
        custom_btn_layout.addWidget(auto_activate_custom)
        custom_btn_layout.addStretch()
        
        def save_custom_instructions():
            """Save custom instructions as Project Prompt"""
            # Ask for name
            name, ok = QInputDialog.getText(
                dialog,
                "Save Custom Instructions",
                "Enter a name for these custom instructions:",
                text=f"{source_lang} to {target_lang} - Custom Instructions"
            )
            
            if not ok or not name:
                return
            
            # Extract domain from analysis if available
            domain = "General"
            if self.doc_analysis_result:
                analysis_text = self.doc_analysis_result.get('analysis', '').lower()
                if 'patent' in analysis_text:
                    domain = "Legal/Patents"
                elif 'medical' in analysis_text or 'clinical' in analysis_text:
                    domain = "Medical"
                elif 'technical' in analysis_text or 'engineering' in analysis_text:
                    domain = "Technical"
                elif 'legal' in analysis_text:
                    domain = "Legal"
                elif 'marketing' in analysis_text:
                    domain = "Marketing"
            
            # Create prompt data
            custom_data = {
                "name": name,
                "description": "AI-generated custom instructions",
                "domain": domain,
                "version": "1.0",
                "created": datetime.now().strftime("%Y-%m-%d"),
                "translate_prompt": custom_instructions_text,
                "proofread_prompt": custom_instructions_text
            }
            
            # Save to Custom Instructions folder
            custom_instructions_dir = self.user_data_path / "Prompt_Library" / "Custom_instructions"
            custom_instructions_dir.mkdir(parents=True, exist_ok=True)
            
            # Sanitize filename and add descriptor
            safe_filename = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f"{safe_filename} (custom instructions).md"
            filepath = custom_instructions_dir / filename
            
            try:
                # Save as Markdown
                self.prompt_library.dict_to_markdown(custom_data, str(filepath))
                
                self.log_message(f"✅ Custom Instructions saved: {filename}")
                
                # Reload prompt library
                self.prompt_library.load_all_prompts()
                self._load_project_guidelines()  # Refresh Project Prompts list
                
                # Auto-activate if checked
                if auto_activate_custom.isChecked():
                    self.active_project_prompt = custom_instructions_text
                    self.active_project_prompt_name = name
                    self._update_active_display()
                    self.log_message("✅ Custom Instructions automatically activated")
                
                QMessageBox.information(
                    self.parent_app if self.parent_app else None,
                    "Saved!",
                    f"Custom Instructions saved as:\n\n{filename}\n\n"
                    f"Location: {custom_instructions_dir}"
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self.parent_app if self.parent_app else None,
                    "Error",
                    f"Failed to save custom instructions:\n\n{str(e)}"
                )
        
        def copy_custom_instructions():
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(custom_instructions_text)
            QMessageBox.information(
                self.parent_app if self.parent_app else None,
                "Copied!",
                "Custom Instructions copied to clipboard!"
            )
        
        save_custom_btn = QPushButton("💾 Save as Project Prompt")
        save_custom_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 6px 12px;")
        save_custom_btn.clicked.connect(save_custom_instructions)
        custom_btn_layout.addWidget(save_custom_btn)
        
        copy_custom_btn = QPushButton("📋 Copy to Clipboard")
        copy_custom_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 6px 12px;")
        copy_custom_btn.clicked.connect(copy_custom_instructions)
        custom_btn_layout.addWidget(copy_custom_btn)
        
        custom_layout.addLayout(custom_btn_layout)
        tabs.addTab(custom_tab, "📝 Custom Instructions (Project-Specific)")
        
        layout.addWidget(tabs, 1)
        
        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(dialog.accept)
        layout.addWidget(button_box)
        
        # Show dialog
        dialog.exec()
        
        # Add to chat for reference
        self._add_chat_message(
            'assistant',
            f"✅ **Generated Translation Prompts**\n\n"
            f"I've created optimized System Prompt and Custom Instructions based on your document analysis.\n\n"
            f"**Next steps:**\n"
            f"1. Review the prompts in the dialog window\n"
            f"2. Save System Prompt → Add to Domain Prompts library\n"
            f"3. Save/Apply Custom Instructions → Add to Project Prompts\n"
            f"4. Start translating with optimized settings!"
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
        
        # List will be loaded when tab is created
    
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
    
    def _load_system_prompts_list(self):
        """Load System Prompts (Layer 1) into the tree list"""
        if not hasattr(self, 'system_prompts_tree'):
            return
        
        # Preserve current selection if available
        current_mode_key = self.current_system_prompt_mode
        
        self.system_prompts_tree.clear()
        
        # Ensure system prompts are loaded
        if not self.system_prompts:
            self._load_system_prompts()
        
        # Define the modes
        modes = [
            ("Single Segment", "single", "⚙️ System Prompt - Single Segment"),
            ("Batch DOCX", "batch_docx", "⚙️ System Prompt - Batch DOCX"),
            ("Batch Bilingual", "batch_bilingual", "⚙️ System Prompt - Batch Bilingual")
        ]
        
        selected_item = None
        for mode_text, mode_key, display_name in modes:
            # Check if prompt exists and is customized
            prompt = self.system_prompts.get(mode_key, None)
            default_prompt = self._get_default_system_prompt(mode_key)
            
            # Determine status
            if prompt is None:
                status = "Not Loaded"
            elif prompt == default_prompt:
                status = "Default"
            else:
                status = "Customized"
            
            # Create item
            item = QTreeWidgetItem([display_name, mode_text, status])
            item.setData(0, Qt.ItemDataRole.UserRole, mode_key)  # Store mode key for selection
            
            # Bold if customized
            if status == "Customized":
                font = item.font(0)
                font.setBold(True)
                item.setFont(0, font)
            
            self.system_prompts_tree.addTopLevelItem(item)
            
            # Remember if this is the currently selected item
            if mode_key == current_mode_key:
                selected_item = item
        
        # Select preserved item or first item by default
        if selected_item:
            self.system_prompts_tree.setCurrentItem(selected_item)
            # Don't call _on_system_prompt_select() to avoid changing the editor unnecessarily
        elif self.system_prompts_tree.topLevelItemCount() > 0:
            first_item = self.system_prompts_tree.topLevelItem(0)
            self.system_prompts_tree.setCurrentItem(first_item)
            if current_mode_key is None:  # Only auto-select on initial load
                self._on_system_prompt_select()
    
    def _on_system_prompt_select(self):
        """Handle System Prompt selection from list"""
        if not hasattr(self, 'system_prompts_tree'):
            return
        
        items = self.system_prompts_tree.selectedItems()
        if not items:
            return
        
        item = items[0]
        if not item:
            return
        
        mode_key = item.data(0, Qt.ItemDataRole.UserRole)
        if not mode_key:
            return
        
        # Store current mode
        self.current_system_prompt_mode = mode_key
        
        # Load the prompt for this mode
        prompt = self.system_prompts.get(mode_key, self._get_default_system_prompt(mode_key))
        if hasattr(self, 'editor_content'):
            self.editor_content.setPlainText(prompt)
    
    def _on_system_prompts_mode_change(self):
        """Handle System Prompt mode selection change - this method is no longer used but kept for compatibility"""
        # Mode selection is now handled by clicking items in the list
        pass
    
    def _save_system_prompt(self):
        """Save current System Prompt (Layer 1)"""
        if not hasattr(self, 'editor_content'):
            self._show_message(QMessageBox.Icon.Warning, "Error", "Editor not available.")
            return
        
        mode_key = self.current_system_prompt_mode
        mode_map = {
            "single": "Single Segment",
            "batch_docx": "Batch DOCX",
            "batch_bilingual": "Batch Bilingual"
        }
        mode_text = mode_map.get(mode_key, "Single Segment")
        
        content = self.editor_content.toPlainText()
        self.system_prompts[mode_key] = content
        self._save_system_prompts_file()
        
        # Refresh the list to update status
        self._load_system_prompts_list()
        
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
        
        mode_key = self.current_system_prompt_mode
        mode_map = {
            "single": "Single Segment",
            "batch_docx": "Batch DOCX",
            "batch_bilingual": "Batch Bilingual"
        }
        mode_text = mode_map.get(mode_key, "Single Segment")
        
        # Reset to default
        default = self._get_default_system_prompt(mode_key)
        self.system_prompts[mode_key] = default
        if hasattr(self, 'editor_content'):
            self.editor_content.setPlainText(default)
        self._save_system_prompts_file()
        
        # Refresh the list to update status
        self._load_system_prompts_list()
        
        self.log_message(f"Reset System Prompt for {mode_text} to default")
        self._show_message(QMessageBox.Icon.Information, "Reset", f"System Prompt for '{mode_text}' reset to default.")
    
    def _export_system_prompt(self):
        """Export current System Prompt (Layer 1) to file"""
        if not hasattr(self, 'editor_content'):
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Export System Prompt", "",
            "Text Files (*.txt);;Markdown Files (*.md);;All Files (*.*)"
        )
        if not file_path:
            return
        
        try:
            Path(file_path).write_text(self.editor_content.toPlainText(), encoding='utf-8')
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
            if hasattr(self, 'editor_content'):
                self.editor_content.setPlainText(content)
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
        
        # Add clear delimiter to mark where translation should start
        # This prevents the LLM from translating the prompt itself
        final_prompt += "\n\n**YOUR TRANSLATION (provide ONLY the translated text, no numbering or labels):**\n"
        
        return final_prompt

