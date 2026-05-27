"""Local SQLite leaderboard display."""

import tkinter as tk

from backend.theme import BG, CREAM, DIM, EMBER, FOG, FONT_SUB, FONT_TITLE, FONT_UI


class LeaderboardScreen2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        tk.Label(self, text="Leaderboard", bg=BG, fg=EMBER, font=FONT_TITLE).pack(
            pady=(40, 8)
        )
        tk.Label(
            self,
            text="Environmental restoration across runs",
            bg=BG,
            fg=FOG,
            font=FONT_SUB,
        ).pack(pady=(0, 20))

        self.list_frame = tk.Frame(self, bg=BG)
        self.list_frame.pack(fill="both", expand=True, padx=40, pady=10)

        tk.Button(
            self,
            text="BACK",
            bg=BG,
            fg=CREAM,
            activebackground=EMBER,
            font=FONT_UI,
            relief="flat",
            command=self._back,
        ).pack(pady=24, ipady=8)

    def _back(self):
        if getattr(self.controller, "current_user", None):
            self.controller.show_frame("MainMenu")
        else:
            self.controller.show_frame("SplashScreen")

    def on_show(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        rows = []
        if self.controller.db:
            rows = self.controller.db.get_local_top_scores(15) or []

        if not rows:
            tk.Label(
                self.list_frame,
                text="No runs recorded yet. Explore the ruins.",
                bg=BG,
                fg=FOG,
                font=FONT_SUB,
            ).pack(pady=40)
            return

        header = tk.Frame(self.list_frame, bg=BG)
        header.pack(fill="x", pady=(0, 8))
        for text, w in (("PLAYER", 18), ("SCORE", 8), ("ENDING", 12), ("TIME", 8)):
            tk.Label(header, text=text, bg=BG, fg=DIM, font=FONT_UI, width=w, anchor="w").pack(
                side="left", padx=4
            )

        for i, row in enumerate(rows):
            bg_row = "#1f140c" if i % 2 == 0 else BG
            fr = tk.Frame(self.list_frame, bg=bg_row)
            fr.pack(fill="x", pady=2, ipady=4)
            tk.Label(
                fr, text=row.get("player_name", "?")[:16], bg=bg_row, fg=CREAM, font=FONT_UI, width=18, anchor="w"
            ).pack(side="left", padx=4)
            tk.Label(
                fr, text=str(row.get("score", 0)), bg=bg_row, fg=EMBER, font=FONT_UI, width=8, anchor="w"
            ).pack(side="left", padx=4)
            tk.Label(
                fr, text=str(row.get("ending", "—")), bg=bg_row, fg=FOG, font=FONT_UI, width=12, anchor="w"
            ).pack(side="left", padx=4)
            tk.Label(
                fr, text=f"{row.get('time_played', 0)}s", bg=bg_row, fg=FOG, font=FONT_UI, width=8, anchor="w"
            ).pack(side="left", padx=4)
