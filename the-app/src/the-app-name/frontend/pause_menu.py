"""Pause overlay for the game screen."""

import tkinter as tk

from backend.theme import BG, CREAM, DIM, EMBER, FOG, FONT_TITLE, FONT_UI


class PauseOverlay(tk.Frame):
    def __init__(self, parent, controller, on_resume, on_save=None):
        super().__init__(parent, bg="#0a0604")
        self.controller = controller
        self.on_resume = on_resume
        self.on_save = on_save

        blocker = tk.Frame(self, bg="#0a0604")
        blocker.place(relx=0, rely=0, relwidth=1, relheight=1)

        panel = tk.Frame(blocker, bg=BG, highlightbackground=DIM, highlightthickness=2)
        panel.place(relx=0.5, rely=0.5, anchor="center", width=320, height=380)

        tk.Label(panel, text="PAUSED", bg=BG, fg=CREAM, font=FONT_TITLE).pack(pady=(36, 24))

        for text, cmd in (
            ("RESUME", self._resume),
            ("SAVE GAME", self._save),
            ("SETTINGS", lambda: controller.show_frame("SettingsScreen")),
            ("MAIN MENU", self._main_menu),
            ("EXIT", self._exit),
        ):
            tk.Button(
                panel,
                text=text,
                bg=BG,
                fg=FOG,
                activebackground=EMBER,
                activeforeground=CREAM,
                font=FONT_UI,
                relief="flat",
                width=22,
                command=cmd,
            ).pack(pady=10, ipady=8)

    def _resume(self):
        if self.on_resume:
            self.on_resume()
        self.destroy()

    def _save(self):
        if self.on_save:
            self.on_save()
        tk.Label(self, text="Saved.", bg=BG, fg=EMBER, font=FONT_UI).place(relx=0.5, rely=0.9)

    def _main_menu(self):
        self.destroy()
        self.controller.show_frame("MainMenu")

    def _exit(self):
        self.controller.on_close()
