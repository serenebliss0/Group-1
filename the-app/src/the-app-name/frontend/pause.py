import tkinter as tk

# Match MainMenu palette
BG = "#0C0904"
TEXT = "#E8DCC8"
ACCENT = "#B5420E"
DIM = "#4A3820"


class PauseMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        self.place(relx=0.5, rely=0.5, anchor="center", width=420, height=520)

        # Title
        tk.Label(
            self,
            text="PAUSED",
            bg=BG,
            fg=TEXT,
            font=("Playfair Display", 30, "bold")
        ).pack(pady=(50, 20))

        # Subtitle
        tk.Label(
            self,
            text="Everything waits here.",
            bg=BG,
            fg=DIM,
            font=("DM Mono", 10, "italic")
        ).pack(pady=(0, 40))

        btn_style = {
            "bg": BG,
            "fg": TEXT,
            "activebackground": ACCENT,
            "activeforeground": TEXT,
            "relief": "flat",
            "font": ("DM Mono", 12),
            "width": 20
        }

        tk.Button(self, text="RESUME", **btn_style, command=self.destroy).pack(pady=10)
        tk.Button(self, text="SETTINGS", **btn_style).pack(pady=10)
        tk.Button(self, text="SAVE GAME", **btn_style).pack(pady=10)

        # ONLY WORKING ACTION
        tk.Button(
            self,
            text="QUIT TO MAIN MENU",
            bg=ACCENT,
            fg=TEXT,
            activebackground=DIM,
            activeforeground=TEXT,
            font=("DM Mono", 12, "bold"),
            relief="flat",
            width=20,
            command=self._quit_to_menu
        ).pack(pady=(40, 10))

    def _quit_to_menu(self):
        self.destroy()
        self.controller.show_frame("MainMenu")