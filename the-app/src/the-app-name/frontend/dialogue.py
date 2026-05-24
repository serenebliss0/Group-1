"""Cinematic dialogue overlay with typewriter effect."""

import tkinter as tk

from backend.game_state import load_settings
from backend.theme import BG, CREAM, DIM, EMBER, FOG, FONT_DIALOGUE, FONT_UI


class DialogueOverlay(tk.Frame):
    """Bottom dialogue panel; pauses movement via callback."""

    def __init__(self, parent, scenario_data, on_close, on_choice=None, audio=None):
        super().__init__(parent, bg="")
        self.scenario = scenario_data
        self.on_close_cb = on_close
        self.on_choice_cb = on_choice
        self.audio = audio
        self._typing = False
        self._char_index = 0
        self._type_job = None
        settings = load_settings()
        self.text_speed = settings.get("text_speed", 35)

        # Dim full screen
        self.dim = tk.Frame(self, bg="#000000")
        self.dim.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.dim.configure(bg="#0a0604")
        try:
            self.dim.configure(bg="#0a0604")
        except tk.TclError:
            pass

        # Semi-transparent effect via dark frame
        overlay = tk.Frame(self, bg="#120a06", highlightbackground=EMBER, highlightthickness=1)
        overlay.place(relx=0.5, rely=1.0, anchor="s", relwidth=0.92, height=200)

        name = scenario_data.get("name", "...")
        tk.Label(
            overlay, text=name.upper(), bg="#120a06", fg=EMBER, font=FONT_UI, anchor="w"
        ).pack(fill="x", padx=24, pady=(14, 4))

        self.text_label = tk.Label(
            overlay,
            text="",
            bg="#120a06",
            fg=CREAM,
            font=FONT_DIALOGUE,
            wraplength=700,
            justify="left",
            anchor="nw",
        )
        self.text_label.pack(fill="both", expand=True, padx=24, pady=(0, 8))

        self.full_text = scenario_data.get("text", "")
        btn_row = tk.Frame(overlay, bg="#120a06")
        btn_row.pack(fill="x", padx=20, pady=(0, 14))

        tk.Button(
            btn_row,
            text="SKIP",
            bg=BG,
            fg=FOG,
            activebackground=EMBER,
            activeforeground=CREAM,
            font=FONT_UI,
            relief="flat",
            command=self._skip_text,
        ).pack(side="left", padx=4)

        self.continue_btn = tk.Button(
            btn_row,
            text="CONTINUE ▶",
            bg=BG,
            fg=CREAM,
            activebackground=EMBER,
            activeforeground=CREAM,
            font=FONT_UI,
            relief="flat",
            state="disabled",
            command=self._show_choices,
        )
        self.continue_btn.pack(side="right", padx=4)

        self.choice_frame = tk.Frame(overlay, bg="#120a06")
        self._start_typewriter()

    def _start_typewriter(self):
        self._typing = True
        self._char_index = 0
        self._type_next()

    def _type_next(self):
        if self._char_index <= len(self.full_text):
            self.text_label.config(text=self.full_text[: self._char_index])
            ch = self.full_text[self._char_index - 1] if self._char_index else ""
            delay = self.text_speed
            if ch in ".!?":
                delay += 120
            elif ch in ",;:":
                delay += 60
            self._char_index += 1
            self._type_job = self.after(delay, self._type_next)
        else:
            self._typing = False
            self.continue_btn.config(state="normal")

    def _skip_text(self):
        if self._type_job:
            self.after_cancel(self._type_job)
        self._typing = False
        self.text_label.config(text=self.full_text)
        self.continue_btn.config(state="normal")

    def _show_choices(self):
        self.continue_btn.pack_forget()
        self.choice_frame.pack(fill="x", padx=12, pady=(0, 8))
        for idx, key in enumerate(("choice_a", "choice_b", "choice_c")):
            label = self.scenario.get(key, "").strip()
            if not label:
                continue
            tk.Button(
                self.choice_frame,
                text=label.upper(),
                bg=BG,
                fg=FOG,
                activebackground=EMBER,
                activeforeground=CREAM,
                font=FONT_UI,
                relief="flat",
                wraplength=200,
                command=lambda i=idx: self._pick(i),
            ).pack(side="left", expand=True, fill="x", padx=4, ipady=6)

        if not self.choice_frame.winfo_children():
            tk.Button(
                self.choice_frame,
                text="LEAVE",
                bg=BG,
                fg=CREAM,
                font=FONT_UI,
                relief="flat",
                command=self._finish,
            ).pack()

    def _pick(self, choice_index):
        if self.audio:
            self.audio.play_sfx("click")
        if self.on_choice_cb:
            self.on_choice_cb(choice_index, self.scenario)
        self._finish()

    def _finish(self):
        if self.on_close_cb:
            self.on_close_cb()
        self.destroy()
