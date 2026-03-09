"""
Context-sensitive help system for Supervertaler.

Opens the relevant GitBook documentation page when the user presses F1
or uses the Help > Context Help menu action.

Usage:
    from modules.help_system import Topics, install, set_topic, open_help

    # Install the event filter on the main window (call once at startup):
    install(main_window)

    # Tag any widget with a help topic:
    set_topic(my_widget, Topics.GLOSSARY_TERMLENS)

    # Open help for a specific topic programmatically:
    open_help(Topics.AI_BATCH)
"""

from PyQt6.QtCore import QObject, QEvent, QUrl, Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QApplication


DOCS_BASE_URL = "https://supervertaler.gitbook.io/help"

# Property key stored on widgets to identify their help topic
_HELP_TOPIC_PROPERTY = "_help_topic"


class Topics:
    """Help topic identifiers mapping to GitBook page paths."""

    # Home
    HOME                = ""

    # Get Started
    INSTALLATION        = "get-started/installation"
    QUICK_START         = "get-started/quick-start"
    API_KEYS            = "get-started/api-keys"
    FIRST_PROJECT       = "get-started/first-project"

    # Supervertaler for Trados (cross-reference)
    TRADOS_PLUGIN       = "supervertaler-for-trados"

    # Editor & Translation
    TRANSLATION_GRID    = "editor-and-translation/translation-grid"
    NAVIGATION          = "editor-and-translation/navigation"
    EDITING             = "editor-and-translation/editing-confirming"
    SEGMENT_STATUSES    = "editor-and-translation/segment-statuses"
    KEYBOARD_SHORTCUTS  = "editor-and-translation/keyboard-shortcuts"
    FIND_REPLACE        = "editor-and-translation/find-replace"
    FILTERING           = "editor-and-translation/filtering"
    PAGINATION          = "editor-and-translation/pagination"

    # AI Translation
    AI_OVERVIEW         = "ai-translation/overview"
    AI_PROVIDERS        = "ai-translation/providers"
    AI_SINGLE_SEGMENT   = "ai-translation/single-segment"
    AI_BATCH            = "ai-translation/batch-translation"
    AI_PROMPTS          = "ai-translation/prompts"
    AI_PROMPT_MANAGER   = "ai-translation/prompt-library"
    AI_QUICKLAUNCHER    = "ai-translation/quicklauncher"
    AI_OLLAMA           = "ai-translation/ollama"

    # CAT Tool Integration
    CAT_OVERVIEW        = "cat-tool-integration/overview"
    CAT_TRADOS          = "cat-tool-integration/trados"
    CAT_MEMOQ           = "cat-tool-integration/memoq"
    CAT_PHRASE          = "cat-tool-integration/phrase"
    CAT_CAFETRAN        = "cat-tool-integration/cafetran"

    # Translation Memory
    TM_BASICS           = "translation-memory/basics"
    TM_MANAGING         = "translation-memory/managing-tms"
    TM_IMPORTING        = "translation-memory/importing-tmx"
    TM_FUZZY            = "translation-memory/fuzzy-matching"
    TM_SUPERMEMORY      = "translation-memory/supermemory"

    # Glossaries
    GLOSSARY_BASICS     = "glossaries-termbases/basics"
    GLOSSARY_CREATING   = "glossaries-termbases/creating"
    GLOSSARY_IMPORTING  = "glossaries-termbases/importing"
    GLOSSARY_HIGHLIGHT  = "glossaries-termbases/highlighting"
    GLOSSARY_TERMLENS   = "glossaries-termbases/termlens"
    GLOSSARY_EXTRACTION = "glossaries-termbases/extraction"

    # Import & Export
    IMPORT_FORMATS      = "import-and-export/formats"
    IMPORT_DOCX         = "import-and-export/docx-import"
    IMPORT_TXT          = "import-and-export/txt-import"
    IMPORT_MULTI        = "import-and-export/multi-file"
    EXPORT              = "import-and-export/exporting"
    BILINGUAL_TABLES    = "import-and-export/bilingual-tables"

    # Superlookup
    SUPERLOOKUP         = "superlookup/overview"
    SUPERLOOKUP_TM      = "superlookup/tm-search"
    SUPERLOOKUP_GLOSS   = "superlookup/glossary-search"
    SUPERLOOKUP_MT      = "superlookup/mt"
    SUPERLOOKUP_WEB     = "superlookup/web-resources"

    # Quality Assurance
    QA_SPELLCHECK       = "quality-assurance/spellcheck"
    QA_TAGS             = "quality-assurance/tag-validation"
    QA_NT               = "quality-assurance/non-translatables"

    # Tools
    TOOL_PDF_RESCUE     = "tools/pdf-rescue"
    TOOL_TMX_EDITOR     = "tools/tmx-editor"
    TOOL_AUTOFINGERS    = "tools/autofingers"
    TOOL_VOICE          = "tools/voice-commands"
    TOOL_IMAGE_EXTRACT  = "tools/image-extractor"

    # Settings
    SETTINGS_GENERAL    = "settings-and-customization/general"
    SETTINGS_VIEW       = "settings-and-customization/view"
    SETTINGS_SHORTCUTS  = "settings-and-customization/shortcuts"
    SETTINGS_THEME      = "settings-and-customization/theme"
    SETTINGS_FONTS      = "settings-and-customization/fonts"

    # Troubleshooting
    TROUBLESHOOTING     = "troubleshooting/common-issues"


class _HelpEventFilter(QObject):
    """
    Application-level event filter that intercepts F1 key presses
    and opens the relevant GitBook documentation page.

    Walks up the widget tree from the focused widget, looking for
    a widget tagged with a help topic via set_topic(). If found,
    opens that page; otherwise opens the docs home.
    """

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_F1:
            topic = self._resolve_topic(QApplication.focusWidget())
            open_help(topic)
            return True  # consumed
        return False

    @staticmethod
    def _resolve_topic(widget):
        """Walk up the widget tree to find the nearest help topic."""
        w = widget
        while w is not None:
            topic = w.property(_HELP_TOPIC_PROPERTY)
            if topic:
                return topic
            w = w.parent()
        return None  # falls back to docs home


# Module-level singleton
_event_filter = None


def install(main_window):
    """Install the help event filter on the application. Call once at startup."""
    global _event_filter
    if _event_filter is None:
        _event_filter = _HelpEventFilter()
        QApplication.instance().installEventFilter(_event_filter)


def set_topic(widget, topic: str):
    """Tag a widget with a help topic path (relative to DOCS_BASE_URL)."""
    widget.setProperty(_HELP_TOPIC_PROPERTY, topic)


def open_help(topic: str = None):
    """Open the GitBook documentation page for the given topic."""
    if topic:
        url = f"{DOCS_BASE_URL}/{topic.strip('/')}"
    else:
        url = DOCS_BASE_URL
    QDesktopServices.openUrl(QUrl(url))
