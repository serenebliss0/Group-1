"""First-run controls tutorial."""

import tkinter as tk

from backend.game_state import load_settings, save_settings
from backend.theme import BG, CREAM, EMBER, FOG, FONT_SUB, FONT_TITLE, FONT_UI


def should_show_tutorial():
    return not load_settings().get("tutorial_seen", False)


def mark_tutorial_seen():
    s = load_settings()
    s["tutorial_seen"] = True
    save_settings(s)


class TutorialOverlay(tk.Frame):
    def __init__(self, parent, on_dismiss):
        super().__init__(parent, bg="#0a0604")
        self.on_dismiss = on_dismiss

        panel = tk.Frame(self, bg=BG, highlightbackground=EMBER, highlightthickness=1)
        panel.place(relx=0.5, rely=0.5, anchor="center", width=520, height=420)

        tk.Label(panel, text="How to Explore", bg=BG, fg=EMBER, font=FONT_TITLE).pack(
            pady=(28, 16)
        )

        lines = (
            "W A S D  or  Arrow keys — move through the ruins",
            "E — interact when you see [E] Interact",
            "ESC — pause menu",
            "",
            "Walk toward glowing zones on the map.",
            "Make choices that restore — or abandon — the city.",
            "After several discoveries, return to the center (?).",
        )
        for line in lines:
            tk.Label(
                panel, text=line, bg=BG, fg=CREAM if line else BG,
                font=FONT_SUB, wraplength=460, justify="left",
            ).pack(anchor="w", padx=32, pady=2)

        tk.Label(
            panel,
            text="Click the map or press ENTER to begin.",
            bg=BG,
            fg=FOG,
            font=FONT_UI,
        ).pack(pady=(20, 8))

        tk.Button(
            panel,
            text="BEGIN",
            bg=EMBER,
            fg=CREAM,
            activebackground="#a04010",
            font=FONT_UI,
            relief="flat",
            command=self.dismiss,
        ).pack(pady=12, ipadx=16, ipady=6)

        self.bind("<Return>", lambda e: self.dismiss())
        self.bind("<Escape>", lambda e: self.dismiss())

    def dismiss(self):
        mark_tutorial_seen()
        if self.on_dismiss:
            self.on_dismiss()
        self.destroy()
