import tkinter as tk

BG = "#0C0904"
TEXT = "#E8DCC8"
ACCENT = "#B5420E"
DIM = "#4A3820"


class GameOverScreen(tk.Frame):
    def __init__(self, parent, controller, missed_nodes):
        super().__init__(parent, bg=BG)

        self.controller = controller

        self.place(relx=0.5, rely=0.5, anchor="center", width=500, height=550)

        # ---------------- TITLE ---------------- #
        tk.Label(
            self,
            text="GAME OVER",
            bg=BG,
            fg=TEXT,
            font=("Playfair Display", 28, "bold")
        ).pack(pady=(40, 10))

        tk.Label(
            self,
            text="The land couldn't be saved in time...",
            bg=BG,
            fg=DIM,
            font=("DM Mono", 10, "italic")
        ).pack(pady=(0, 20))

        # ---------------- MISSED SUMMARY ---------------- #
        summary_text = "You missed:\n\n"

        if not missed_nodes:
            summary_text += "Nothing (???)"
        else:
            for node in missed_nodes:
                summary_text += f"• {node['name']}\n"

        tk.Label(
            self,
            text=summary_text,
            bg=BG,
            fg=TEXT,
            font=("DM Mono", 11),
            justify="left"
        ).pack(pady=20)

        # ---------------- BUTTON ---------------- #
        tk.Button(
            self,
            text="QUIT TO MAIN MENU",
            bg=ACCENT,
            fg=TEXT,
            activebackground=DIM,
            font=("DM Mono", 12, "bold"),
            relief="flat",
            width=22,
            command=self._quit
        ).pack(pady=30)

    def _quit(self):
        self.destroy()
        self.controller.show_frame("MainMenu")