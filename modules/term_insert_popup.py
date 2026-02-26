"""
term_insert_popup.py

memoQ-style floating popup for inserting glossary terms and non-translatables.
Triggered by a single keyboard shortcut (default: Ctrl+K).

Shows a numbered list (1-9) of all glossary matches + NT matches for the
current segment, with NTs distinguished by a yellow background.

Usage:
    popup = TermInsertPopup(glossary_matches, nt_matches, parent=main_window)
    popup.term_inserted.connect(handler)
    popup.show()
    popup.setFocus()
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent, QCursor


# ─────────────────────────────────────────────────────────────────────────────
# Individual row widget
# ─────────────────────────────────────────────────────────────────────────────

class _TermRow(QFrame):
    """A single selectable row in the TermInsertPopup."""

    clicked = pyqtSignal()

    _STYLE_NORMAL_TERM = """
        _TermRow { background: #F2F2F2; border-bottom: 1px solid #D8D8D8; }
        _TermRow:hover { background: #E2EDF8; }
    """
    _STYLE_SELECTED_TERM = """
        _TermRow {
            background: #D9ECFC;
            border-bottom: 1px solid #90CAF9;
            border-left: 3px solid #1976D2;
        }
    """
    _STYLE_NORMAL_NT = """
        _TermRow { background: #FBF5D6; border-bottom: 1px solid #DDD09A; }
        _TermRow:hover { background: #F7EFA8; }
    """
    _STYLE_SELECTED_NT = """
        _TermRow {
            background: #F5E97A;
            border-bottom: 1px solid #CFBA50;
            border-left: 3px solid #F9A825;
        }
    """

    def __init__(self, number: int, source: str, target: str, meta: str,
                 is_nt: bool, parent=None):
        super().__init__(parent)
        self.number = number
        self.insert_text = target
        self.is_nt = is_nt
        self._selected = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._build_ui(number, source, target, meta, is_nt)
        self._apply_style(False)

    def _build_ui(self, number, source, target, meta, is_nt):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 5, 8, 5)
        layout.setSpacing(6)

        # ── number badge ──────────────────────────────────────────────────
        num_lbl = QLabel(str(number))
        num_lbl.setFixedSize(18, 18)
        num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_color = "#F9A825" if is_nt else "#1976D2"
        num_lbl.setStyleSheet(f"""
            background: {badge_color}; color: white;
            border-radius: 9px; font-size: 8pt; font-weight: bold;
        """)
        layout.addWidget(num_lbl)

        if is_nt:
            # ── NT row ────────────────────────────────────────────────────
            icon_lbl = QLabel("🚫")
            icon_lbl.setStyleSheet("font-size: 10pt; background: transparent;")
            layout.addWidget(icon_lbl)

            text_lbl = QLabel(source)
            text_lbl.setStyleSheet("font-size: 9pt; font-weight: bold; background: transparent;")
            layout.addWidget(text_lbl)

            layout.addStretch()

            meta_lbl = QLabel(meta)
            meta_lbl.setStyleSheet("font-size: 8pt; color: #888; font-style: italic; background: transparent;")
            layout.addWidget(meta_lbl)
        else:
            # ── Glossary term row ─────────────────────────────────────────
            src_lbl = QLabel(source)
            src_lbl.setStyleSheet("font-size: 9pt; color: #555; background: transparent;")
            layout.addWidget(src_lbl)

            arrow_lbl = QLabel("→")
            arrow_lbl.setStyleSheet("font-size: 9pt; color: #AAAAAA; background: transparent;")
            layout.addWidget(arrow_lbl)

            tgt_lbl = QLabel(target)
            tgt_lbl.setStyleSheet("font-size: 9pt; font-weight: bold; color: #1A237E; background: transparent;")
            layout.addWidget(tgt_lbl)

            layout.addStretch()

            meta_lbl = QLabel(meta)
            meta_lbl.setStyleSheet(
                "font-size: 8pt; color: #999; font-style: italic; padding-left: 4px; background: transparent;")
            layout.addWidget(meta_lbl)

    def _apply_style(self, selected: bool):
        self._selected = selected
        if self.is_nt:
            self.setStyleSheet(self._STYLE_SELECTED_NT if selected else self._STYLE_NORMAL_NT)
        else:
            self.setStyleSheet(self._STYLE_SELECTED_TERM if selected else self._STYLE_NORMAL_TERM)

    def set_selected(self, selected: bool):
        self._apply_style(selected)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
# Main popup
# ─────────────────────────────────────────────────────────────────────────────

class TermInsertPopup(QFrame):
    """
    memoQ-style floating popup listing glossary matches + NTs for the current
    segment, numbered 1–9 for instant keyboard insertion.

    Signals:
        term_inserted(str): emitted with the text to insert when the user
                            selects an item.
    """

    term_inserted = pyqtSignal(str)

    MAX_ITEMS = 9

    def __init__(self, glossary_matches: list, nt_matches: list, parent=None):
        super().__init__(parent, Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self._items: list[dict] = []   # raw item data
        self._rows: list[_TermRow] = []  # row widgets
        self._selected_idx = 0

        self._build_items(glossary_matches, nt_matches)
        self._init_ui()
        self._position_near_cursor()

    # ── data ──────────────────────────────────────────────────────────────

    def _build_items(self, glossary_matches: list, nt_matches: list):
        for m in glossary_matches:
            if len(self._items) >= self.MAX_ITEMS:
                break
            self._items.append({
                "insert": m.get("target_term", ""),
                "source": m.get("source_term", ""),
                "target": m.get("target_term", ""),
                "meta":   m.get("termbase_name", ""),
                "is_nt":  False,
            })
        for nt in nt_matches:
            if len(self._items) >= self.MAX_ITEMS:
                break
            text = nt.get("text", "")
            self._items.append({
                "insert": text,
                "source": text,
                "target": text,
                "meta":   nt.get("list_name", "NT"),
                "is_nt":  True,
            })

    # ── UI ────────────────────────────────────────────────────────────────

    def _init_ui(self):
        self.setStyleSheet("""
            TermInsertPopup {
                background: #F2F2F2;
                border: 1px solid #BDBDBD;
                border-radius: 6px;
            }
        """)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # header
        header = QLabel("  Insert term or non-translatable")
        header.setStyleSheet("""
            background: #1565C0; color: white;
            font-size: 8pt; font-weight: bold;
            padding: 5px 8px;
            border-top-left-radius: 5px; border-top-right-radius: 5px;
        """)
        outer.addWidget(header)

        if not self._items:
            empty = QLabel("No terms or NTs found for this segment")
            empty.setStyleSheet("padding: 14px; color: #888; font-size: 9pt;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            outer.addWidget(empty)
        else:
            for i, item in enumerate(self._items):
                row = _TermRow(
                    number=i + 1,
                    source=item["source"],
                    target=item["target"],
                    meta=item["meta"],
                    is_nt=item["is_nt"],
                    parent=self,
                )
                idx = i  # capture for closure
                row.clicked.connect(lambda checked=False, x=idx: self._insert(x))
                outer.addWidget(row)
                self._rows.append(row)

            # highlight first row
            if self._rows:
                self._rows[0].set_selected(True)

        # footer
        footer = QLabel("  1–9 insert  ·  ↑↓ navigate  ·  Enter confirm  ·  Esc close")
        footer.setStyleSheet("""
            background: #E6E6E6; color: #999999;
            font-size: 7pt; padding: 3px 8px;
            border-top: 1px solid #D0D0D0;
            border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;
        """)
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(footer)

        self.adjustSize()
        self.setMinimumWidth(380)

    def _position_near_cursor(self):
        cursor_pos = QCursor.pos()
        screen = QApplication.screenAt(cursor_pos) or QApplication.primaryScreen()
        sg = screen.availableGeometry()

        w = self.sizeHint().width()
        h = self.sizeHint().height()
        x = cursor_pos.x() + 16
        y = cursor_pos.y() + 16

        if x + w > sg.right():
            x = cursor_pos.x() - w - 10
        if y + h > sg.bottom():
            y = cursor_pos.y() - h - 10

        self.move(max(sg.left(), x), max(sg.top(), y))

    # ── logic ─────────────────────────────────────────────────────────────

    def _insert(self, index: int):
        if 0 <= index < len(self._items):
            self.term_inserted.emit(self._items[index]["insert"])
            self.close()

    def _move_selection(self, delta: int):
        if not self._rows:
            return
        self._rows[self._selected_idx].set_selected(False)
        self._selected_idx = max(0, min(self._selected_idx + delta, len(self._rows) - 1))
        self._rows[self._selected_idx].set_selected(True)

    # ── keyboard ──────────────────────────────────────────────────────────

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        # 1–9: direct insert
        if Qt.Key.Key_1 <= key <= Qt.Key.Key_9:
            self._insert(key - Qt.Key.Key_1)
            event.accept()
            return

        if key == Qt.Key.Key_Down:
            self._move_selection(+1)
            event.accept()
            return

        if key == Qt.Key.Key_Up:
            self._move_selection(-1)
            event.accept()
            return

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._insert(self._selected_idx)
            event.accept()
            return

        if key == Qt.Key.Key_Escape:
            self.close()
            event.accept()
            return

        super().keyPressEvent(event)
