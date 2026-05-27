"""Settings — volume, text speed, accessibility."""

import tkinter as tk

from backend.game_state import load_settings, save_settings
from backend.theme import BG, CREAM, EMBER, FOG, FONT_SUB, FONT_TITLE, FONT_UI


class SettingsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.settings = load_settings()

        tk.Label(self, text="Settings", bg=BG, fg=EMBER, font=FONT_TITLE).pack(pady=(50, 30))

        self._slider_row("Music volume", "music_volume", 0, 1, self._music_changed)
        self._slider_row("Sound effects", "sfx_volume", 0, 1, self._sfx_changed)
        self._slider_row("Text speed (lower = faster)", "text_speed", 15, 80, self._text_changed)

        self.motion_var = tk.BooleanVar(value=self.settings.get("reduced_motion", False))
        tk.Checkbutton(
            self,
            text="Reduced motion",
            variable=self.motion_var,
            bg=BG,
            fg=FOG,
            selectcolor=BG,
            activebackground=BG,
            font=FONT_UI,
            command=self._save,
        ).pack(pady=12)

        tk.Button(
            self,
            text="SHOW TUTORIAL AGAIN",
            bg=BG,
            fg=FOG,
            activebackground=EMBER,
            font=FONT_UI,
            relief="flat",
            command=self._reset_tutorial,
        ).pack(pady=8, ipady=6)

        tk.Button(
            self,
            text="BACK",
            bg=BG,
            fg=CREAM,
            activebackground=EMBER,
            font=FONT_UI,
            relief="flat",
            command=self._back,
        ).pack(pady=20, ipady=8)

    def _reset_tutorial(self):
        s = load_settings()
        s["tutorial_seen"] = False
        save_settings(s)

    def _slider_row(self, label, key, lo, hi, callback):
        tk.Label(self, text=label, bg=BG, fg=FOG, font=FONT_SUB).pack(pady=(12, 4))
        val = self.settings.get(key, (lo + hi) / 2)
        scale = tk.Scale(
            self,
            from_=lo,
            to=hi,
            resolution=0.05 if isinstance(val, float) else 1,
            orient="horizontal",
            bg=BG,
            fg=CREAM,
            highlightthickness=0,
            troughcolor="#2a1e10",
            activebackground=EMBER,
            command=lambda v, k=key, cb=callback: cb(k, float(v)),
        )
        scale.set(val)
        scale.pack(fill="x", padx=80)
        setattr(self, f"_scale_{key}", scale)

    def _music_changed(self, key, val):
        self.settings[key] = val
        audio = getattr(self.controller, "audio", None)
        if audio:
            audio.set_music_volume(val)
        self._save()

    def _sfx_changed(self, key, val):
        self.settings[key] = val
        audio = getattr(self.controller, "audio", None)
        if audio:
            audio.set_sfx_volume(val)
        self._save()

    def _text_changed(self, key, val):
        self.settings[key] = int(val)
        self._save()

    def _save(self):
        self.settings["reduced_motion"] = self.motion_var.get()
        save_settings(self.settings)

    def _back(self):
        if getattr(self.controller, "current_user", None):
            self.controller.show_frame("MainMenu")
        else:
            self.controller.show_frame("MainMenu")

    def on_show(self):
        self.settings = load_settings()
        audio = getattr(self.controller, "audio", None)
        if audio:
            audio.settings = self.settings
