import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import difflib
import re

# ==========================================
# 1. BACKEND LOGIC (Same as before)
# ==========================================

TM_FILE = 'translation_memory.json'

class TranslationMemory:
    def __init__(self):
        self.tm = self.load_tm()

    def load_tm(self):
        if not os.path.exists(TM_FILE):
            return {}
        try:
            with open(TM_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def save_tm(self):
        with open(TM_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tm, f, ensure_ascii=False, indent=4)

    def segment_text(self, text):
        # Split by sentence endings
        segments = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in segments if s.strip()]

    def find_match(self, source_segment):
        # 1. Exact Match
        if source_segment in self.tm:
            return self.tm[source_segment], 100

        # 2. Fuzzy Match
        best_match = None
        highest_ratio = 0.0
        
        for stored_source, stored_target in self.tm.items():
            ratio = difflib.SequenceMatcher(None, source_segment, stored_source).ratio()
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match = stored_target
        
        return best_match, int(highest_ratio * 100)

    def update_entry(self, source, target):
        self.tm[source] = target

# ==========================================
# 2. FRONTEND (GUI)
# ==========================================

class CatToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python CAT Tool MVP")
        self.root.geometry("900x600")
        
        self.backend = TranslationMemory()
        self.row_widgets = [] # To keep track of generated input fields

        self._setup_ui()

    def _setup_ui(self):
        # --- Top Frame: Input ---
        top_frame = tk.Frame(self.root, pady=10, padx=10)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="1. Paste Source Text:").pack(anchor="w")
        self.input_text = tk.Text(top_frame, height=4, width=100)
        self.input_text.pack(fill="x", pady=5)

        btn_analyze = tk.Button(top_frame, text="2. Segment & Translate", command=self.analyze_text, bg="#dddddd")
        btn_analyze.pack(anchor="w")

        # --- Middle Frame: The Grid (Scrollable) ---
        # Creating a scrollable canvas for the grid
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame)
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # --- Bottom Frame: Actions ---
        bottom_frame = tk.Frame(self.root, pady=10)
        bottom_frame.pack(fill="x")
        
        btn_save = tk.Button(bottom_frame, text="3. Save to TM & Export", command=self.save_work, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_save.pack()

    def analyze_text(self):
        # Clear previous grid
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.row_widgets = []

        raw_text = self.input_text.get("1.0", tk.END)
        segments = self.backend.segment_text(raw_text)

        # HEADERS
        tk.Label(self.scrollable_frame, text="Source Segment", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(self.scrollable_frame, text="Target Translation", font=("Arial", 10, "bold")).grid(row=0, column=1, sticky="w", padx=5)
        tk.Label(self.scrollable_frame, text="Match", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w", padx=5)

        # GENERATE ROWS
        for i, seg in enumerate(segments):
            row_idx = i + 1
            
            # 1. Source Label
            lbl_source = tk.Label(self.scrollable_frame, text=seg, wraplength=350, justify="left", anchor="w", bg="#f0f0f0", relief="sunken")
            lbl_source.grid(row=row_idx, column=0, sticky="nsew", padx=5, pady=2)

            # 2. Target Entry
            ent_target = tk.Entry(self.scrollable_frame, width=50)
            ent_target.grid(row=row_idx, column=1, sticky="nsew", padx=5, pady=2)

            # 3. Match Logic
            match_text, score = self.backend.find_match(seg)
            status_color = "white"
            status_text = "New"

            if score == 100:
                status_text = "100%"
                status_color = "#90EE90" # Light Green
                ent_target.insert(0, match_text) # Auto-fill
            elif score > 60:
                status_text = f"Fuzzy {score}%"
                status_color = "#FFFACD" # Lemon Chiffon
                ent_target.insert(0, match_text) # Auto-fill suggestion
            
            # 4. Status Label
            lbl_status = tk.Label(self.scrollable_frame, text=status_text, bg=status_color, width=10)
            lbl_status.grid(row=row_idx, column=2, padx=5, pady=2)

            # Store reference to widgets to retrieve data later
            self.row_widgets.append({
                "source": seg,
                "entry": ent_target
            })

    def save_work(self):
        if not self.row_widgets:
            return

        full_translation = []
        
        for row in self.row_widgets:
            source = row["source"]
            target = row["entry"].get()
            
            if target.strip():
                # Update Memory
                self.backend.update_entry(source, target)
                full_translation.append(target)
            else:
                full_translation.append(source) # Fallback if empty

        self.backend.save_tm()
        
        # Show Result
        result_window = tk.Toplevel(self.root)
        result_window.title("Export Result")
        txt = tk.Text(result_window, height=10, width=60)
        txt.pack(padx=10, pady=10)
        txt.insert("1.0", " ".join(full_translation))
        
        messagebox.showinfo("Success", "Translation Memory Updated!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CatToolApp(root)
    root.mainloop()