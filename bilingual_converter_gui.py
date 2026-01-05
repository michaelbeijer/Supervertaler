"""
Bilingual → [SEGMENT] NL/EN converter (Windows GUI)

Fixes:
- Handles real tabs AND tab-like pasted whitespace (NBSP, thin spaces) AND 2+ spaces.
- Tolerates stray standalone line numbers ("1", "2", "3", ...)
- Tolerates header lines.
- Looks for a UUID to identify real data rows.
- Extracts NL and EN from the two columns after the UUID.

Run:
  python bilingual_converter_gui.py

No external dependencies (standard library only).
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox


# UUID (exact)
UUID_FULL_RE = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)

# UUID (search inside a line)
UUID_SEARCH_RE = re.compile(
    r"[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}"
)

# Split on:
# - real tabs
# - 2+ spaces
# - 2+ non-breaking spaces (U+00A0)
# - 2+ common "wide spaces" (en space, em space, thin space)
COL_SPLIT_RE = re.compile(r"\t+| {2,}|\u00A0{2,}|[\u2002\u2003\u2009]{2,}")


def split_cols(line: str):
    """Split a row into columns using robust separators."""
    return [p for p in COL_SPLIT_RE.split(line.strip()) if p != ""]


def parse_segments(raw: str):
    """
    Parse pasted bilingual rows into [(nl, en), ...].

    Accepts rows like:
      <rownum?> <uuid> <NL> <EN>

    Returns:
      segments: list[(nl, en)]
      skipped: list[(lineno, line, reason)]
    """
    segments = []
    skipped = []

    for lineno, line in enumerate(raw.splitlines(), start=1):
        s = line.strip()
        if not s:
            continue

        lower = s.lower()

        # Skip header-ish lines
        if "dutch" in lower and "english" in lower:
            continue
        if lower.startswith("id") and ("dutch" in lower or "english" in lower):
            continue

        # Skip standalone index lines ("1", "2", ...)
        if s.isdigit():
            continue

        # Require a UUID somewhere to treat as a data row
        m = UUID_SEARCH_RE.search(s)
        if not m:
            skipped.append((lineno, line, "No UUID found"))
            continue

        parts = split_cols(s)

        # Find the UUID column (near the front)
        uuid_idx = None
        for idx, p in enumerate(parts[:6]):
            if UUID_FULL_RE.match(p.strip()):
                uuid_idx = idx
                break

        if uuid_idx is None:
            # Fallback: UUID exists in the raw line, but split didn't isolate it cleanly.
            # Use the regex match span and split the tail into NL/EN.
            tail = s[m.end():].strip()
            tail_parts = split_cols(tail)
            if len(tail_parts) >= 2:
                nl = tail_parts[0].strip()
                en = tail_parts[1].strip()
                if nl and en:
                    segments.append((nl, en))
                    continue
            skipped.append((lineno, line, "UUID found but could not split NL/EN"))
            continue

        # NL/EN expected directly after UUID
        if uuid_idx + 2 >= len(parts):
            skipped.append((lineno, line, "Missing NL/EN columns after UUID"))
            continue

        nl = parts[uuid_idx + 1].strip()
        en = parts[uuid_idx + 2].strip()

        if not nl or not en:
            skipped.append((lineno, line, "Empty NL or EN cell"))
            continue

        segments.append((nl, en))

    return segments, skipped


def format_segments(segments, start_at=1, pad=4):
    """Format as [SEGMENT 0001] NL: ... EN: ..."""
    out_lines = []
    n = start_at
    for nl, en in segments:
        out_lines.append(f"[SEGMENT {n:0{pad}d}]")
        out_lines.append(f"NL: {nl}")
        out_lines.append(f"EN: {en}")
        out_lines.append("")  # blank line between segments
        n += 1
    return "\n".join(out_lines).rstrip() + ("\n" if segments else "")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bilingual → [SEGMENT] NL/EN converter")
        self.geometry("1150x720")
        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)

        # Options
        opts = ttk.Frame(main)
        opts.pack(fill="x")

        ttk.Label(opts, text="Start segment number:").pack(side="left")
        self.start_var = tk.StringVar(value="1")
        ttk.Entry(opts, width=8, textvariable=self.start_var).pack(side="left", padx=(6, 18))

        ttk.Label(opts, text="Zero padding:").pack(side="left")
        self.pad_var = tk.StringVar(value="4")
        ttk.Entry(opts, width=6, textvariable=self.pad_var).pack(side="left", padx=(6, 18))

        ttk.Button(opts, text="Convert", command=self.on_convert).pack(side="left", padx=(0, 8))
        ttk.Button(opts, text="Copy output", command=self.on_copy).pack(side="left", padx=(0, 8))
        ttk.Button(opts, text="Clear", command=self.on_clear).pack(side="left")

        # Paned areas
        panes = ttk.Panedwindow(main, orient="horizontal")
        panes.pack(fill="both", expand=True, pady=(10, 0))

        left = ttk.Frame(panes, padding=5)
        right = ttk.Frame(panes, padding=5)
        panes.add(left, weight=1)
        panes.add(right, weight=1)

        ttk.Label(left, text="Input (paste bilingual export here)").pack(anchor="w")
        self.in_text = tk.Text(left, wrap="none", undo=True)
        self.in_text.pack(fill="both", expand=True)

        ttk.Label(right, text="Output ([SEGMENT] format)").pack(anchor="w")
        self.out_text = tk.Text(right, wrap="none", undo=True)
        self.out_text.pack(fill="both", expand=True)

        # Status
        self.status = tk.StringVar(value="Ready.")
        ttk.Label(main, textvariable=self.status).pack(anchor="w", pady=(8, 0))

    def on_convert(self):
        raw = self.in_text.get("1.0", "end").strip("\n")
        if not raw.strip():
            messagebox.showinfo("Nothing to convert", "Paste some input text first.")
            return

        try:
            start_at = int(self.start_var.get().strip())
            pad = int(self.pad_var.get().strip())
            if pad < 1 or pad > 8:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid options", "Start must be an integer. Padding must be 1–8.")
            return

        segments, skipped = parse_segments(raw)
        output = format_segments(segments, start_at=start_at, pad=pad)

        self.out_text.delete("1.0", "end")
        self.out_text.insert("1.0", output)

        msg = f"Converted {len(segments)} segment(s)."
        if skipped:
            msg += f" Skipped {len(skipped)} line(s)."
        self.status.set(msg)

        # If everything skipped, show top reasons
        if len(segments) == 0 and skipped:
            reasons = {}
            for _, _, r in skipped:
                reasons[r] = reasons.get(r, 0) + 1
            top = sorted(reasons.items(), key=lambda x: x[1], reverse=True)[:6]
            preview = "\n".join([f"{r}: {c}" for r, c in top])
            messagebox.showwarning(
                "No segments found",
                "No valid rows were parsed.\n\nTop reasons:\n" + preview
            )

    def on_copy(self):
        out = self.out_text.get("1.0", "end").strip("\n")
        if not out.strip():
            messagebox.showinfo("Nothing to copy", "Convert something first.")
            return
        self.clipboard_clear()
        self.clipboard_append(out)
        self.status.set("Output copied to clipboard.")

    def on_clear(self):
        self.in_text.delete("1.0", "end")
        self.out_text.delete("1.0", "end")
        self.status.set("Cleared.")


if __name__ == "__main__":
    # Better scaling on Windows (optional)
    try:
        from ctypes import windll  # type: ignore
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = App()
    app.mainloop()
