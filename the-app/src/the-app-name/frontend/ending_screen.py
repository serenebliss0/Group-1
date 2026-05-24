"""Three endings based on environmental restoration score."""

import tkinter as tk

from backend.theme import BG, CREAM, DIM, EMBER, FOG, FONT_SUB, FONT_TITLE, MUTED_GREEN

ENDINGS = {
    "good": {
        "title": "The City Remembered How to Breathe",
        "body": (
            "Water clears. Roots split concrete. Lights blink on one by one.\n\n"
            "You were never only a citizen. You were what remained — "
            "and what remained chose to stay."
        ),
        "accent": MUTED_GREEN,
    },
    "neutral": {
        "title": "A Pause, Not a Peace",
        "body": (
            "The damage slows. Some streets hold. Some rivers still choke.\n\n"
            "The future is uncertain — but uncertainty is not the same as surrender."
        ),
        "accent": FOG,
    },
    "bad": {
        "title": "Nothing Remained",
        "body": (
            "Skies darken. The last green folds into rust.\n\n"
            "You disappear into the ruins — another silence "
            "in a city that forgot how to listen."
        ),
        "accent": DIM,
    },
}


class EndingScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.title_lbl = tk.Label(self, bg=BG, fg=EMBER, font=FONT_TITLE, wraplength=700)
        self.title_lbl.pack(pady=(80, 20))
        self.body_lbl = tk.Label(self, bg=BG, fg=CREAM, font=FONT_SUB, wraplength=620, justify="center")
        self.body_lbl.pack(pady=20, padx=40)
        self.score_lbl = tk.Label(self, bg=BG, fg=FOG, font=FONT_SUB)
        self.score_lbl.pack(pady=10)

        tk.Button(
            self,
            text="MAIN MENU",
            bg=BG,
            fg=CREAM,
            activebackground=EMBER,
            font=FONT_SUB,
            relief="flat",
            command=lambda: controller.show_frame("MainMenu"),
        ).pack(pady=12, ipady=8)
        tk.Button(
            self,
            text="LEADERBOARD",
            bg=BG,
            fg=FOG,
            activebackground=EMBER,
            font=FONT_SUB,
            relief="flat",
            command=lambda: controller.show_frame("LeaderboardScreen"),
        ).pack(pady=6, ipady=6)

    def on_show(self):
        key = getattr(self.controller, "pending_ending", "neutral")
        data = ENDINGS.get(key, ENDINGS["neutral"])
        from backend.game_state import GameState

        score = GameState().restoration_percent()
        self.configure(bg=BG)
        self.title_lbl.config(text=data["title"], fg=data["accent"])
        self.body_lbl.config(text=data["body"])
        self.score_lbl.config(text=f"Environmental restoration: {score}%")
