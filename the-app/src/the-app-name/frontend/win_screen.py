import tkinter as tk

BG = "#0C0904"
TEXT = "#E8DCC8"
ACCENT = "#2E8B57"   # green vibe for victory
DIM = "#4A3820"


class WinScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        self.controller = controller

        self.place(relx=0.5, rely=0.5, anchor="center", width=500, height=500)

        # ---------------- TITLE ---------------- #
        tk.Label(
            self,
            text="YOU WON",
            bg=BG,
            fg=ACCENT,
            font=("Playfair Display", 30, "bold")
        ).pack(pady=(50, 10))

        # ---------------- SUBTEXT ---------------- #
        tk.Label(
            self,
            text="Every problem was fixed in time.\nThe land breathes again.",
            bg=BG,
            fg=TEXT,
            font=("DM Mono", 11),
            justify="center"
        ).pack(pady=20)

        # ---------------- BUTTON ---------------- #
        tk.Button(
            self,
            text="BACK TO MAIN MENU",
            bg=ACCENT,
            fg=TEXT,
            activebackground=DIM,
            font=("DM Mono", 12, "bold"),
            relief="flat",
            width=22,
            command=self._quit
        ).pack(pady=40)

    def _quit(self):
        self.destroy()
        self.controller.show_frame("MainMenu")