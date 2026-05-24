import tkinter as tk
from pathlib import Path

from backend import game_state, session
from backend.theme import BG_DARK, CREAM, EMBER, FOG, FONT_SUB, FONT_TITLE

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets" / "images"


class SplashScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        self._bg_rgb = (13, 8, 0)
        self.alpha = 0.0
        self._buttons_visible = False

        self.image_label = tk.Label(self, bg=BG_DARK)
        self.image_label.pack(fill="both", expand=True)

        self.overlay = tk.Frame(self, bg=BG_DARK)
        self.overlay.place(relx=0.5, rely=0.5, anchor="center")

        overlay = self.overlay
        tk.Label(
            overlay,
            text="What",
            bg=BG_DARK,
            fg=CREAM,
            font=("Playfair Display", 42, "bold"),
        ).pack()
        tk.Label(
            overlay,
            text="Remains?",
            bg=BG_DARK,
            fg=EMBER,
            font=("Playfair Display", 42, "bold", "italic"),
        ).pack()
        tk.Label(
            overlay,
            text="A narrative exploration game",
            bg=BG_DARK,
            fg=FOG,
            font=FONT_SUB,
        ).pack(pady=(8, 28))

        self.btn_frame = tk.Frame(overlay, bg=BG_DARK)
        self.btn_frame.pack()
        for label, cmd in (
            ("START GAME", self._start),
            ("CONTINUE", self._continue),
            ("LEADERBOARD", lambda: controller.show_frame("LeaderboardScreen")),
            ("SETTINGS", lambda: controller.show_frame("SettingsScreen")),
            ("EXIT", controller.on_close),
        ):
            b = tk.Button(
                self.btn_frame,
                text=label,
                bg=BG_DARK,
                fg=FOG,
                activebackground=EMBER,
                activeforeground=CREAM,
                font=FONT_SUB,
                relief="flat",
                width=22,
                command=cmd,
            )
            b.pack(pady=6, ipady=6)
            b.bind("<Enter>", lambda e, btn=b: btn.config(fg=CREAM))
            b.bind("<Leave>", lambda e, btn=b: btn.config(fg=FOG))

        self.overlay.place_forget()
        self._load_splash_image()
        self.fade_in()

    def _load_splash_image(self):
        path = ASSETS / "splash.png"
        if Image and path.exists():
            self.original_img = Image.open(path).convert("RGBA")
        else:
            self.original_img = None

    def _start(self):
        user = session.load_session()
        if user:
            self.controller.current_user = user
            self.controller.show_frame("MainMenu")
        else:
            self.controller.show_frame("LoginScreen")

    def _continue(self):
        user = session.load_session() or getattr(self.controller, "current_user", None)
        if not user:
            self.controller.show_frame("LoginScreen")
            return
        self.controller.current_user = user
        if game_state.has_save(user):
            self.controller.show_frame("GameScreen")
        else:
            self.controller.show_frame("MainMenu")

    def update_image_alpha(self, alpha_value):
        if not self.original_img or not Image:
            return
        bg_canvas = Image.new("RGBA", self.original_img.size, self._bg_rgb + (255,))
        blended = Image.blend(bg_canvas, self.original_img, alpha_value)
        self.tk_img = ImageTk.PhotoImage(blended)
        self.image_label.configure(image=self.tk_img)

    def fade_in(self):
        if self.original_img and Image:
            if self.alpha < 1.0:
                self.alpha = min(1.0, self.alpha + 0.04)
                self.update_image_alpha(self.alpha)
                self.after(25, self.fade_in)
            else:
                self.after(800, self._show_buttons)
        else:
            self._show_buttons()

    def _show_buttons(self):
        self.overlay.place(relx=0.5, rely=0.5, anchor="center")

    def on_show(self):
        self.alpha = 0.0
        self.overlay.place_forget()
        if self.original_img:
            self.fade_in()
        else:
            self._show_buttons()
