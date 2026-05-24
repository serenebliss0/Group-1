from datetime import datetime
from pathlib import Path
import tkinter as tk

from backend import game_state, session
from backend.theme import BG_DARK, CREAM, EMBER, FOG, FONT_SUB, FONT_TITLE, FONT_UI

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_PATH = BASE_DIR / "assets" / "images"
IMAGE_REFS = []


def relative_to_assets(path: str):
    return ASSETS_PATH / path


def load_photo_image(path):
    try:
        image = tk.PhotoImage(file=str(path))
    except Exception:
        if Image is None or ImageTk is None:
            raise
        image = ImageTk.PhotoImage(Image.open(path))
    IMAGE_REFS.append(image)
    return image


class ImageButton(tk.Label):
    def __init__(self, master=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self._command = command
        self.configure(cursor="hand2")
        self.bind("<Button-1>", self._invoke)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _invoke(self, event):
        if self._command:
            self._command()

    def _on_enter(self, event):
        audio = getattr(self.master.winfo_toplevel(), "audio", None)
        if hasattr(self.master, "controller"):
            audio = getattr(self.master.controller, "audio", None)
        if audio:
            audio.play_sfx("click")

    def _on_leave(self, event):
        pass

    def configure(self, cnf=None, **kwargs):
        if cnf and "command" in cnf:
            cnf = dict(cnf)
            self._command = cnf.pop("command")
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        return super().configure(cnf, **kwargs)

    config = configure


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0C0904")
        self.controller = controller
        self._build()

    def _build(self):
        self.canvas = tk.Canvas(
            self, bg="#0C0904", height=826, width=1130,
            bd=0, highlightthickness=0, relief="ridge",
        )
        self.canvas.place(x=0, y=0)
        canvas = self.canvas

        canvas.create_text(
            64.0, 98.71, anchor="nw",
            text="COS 102 · GROUP 1 · PAN-ATLANTIC UNIVERSITY · 2026",
            fill="#4A3820", font=("DM Mono", 9),
        )
        canvas.create_text(64.0, 159.81, anchor="nw", text="What", fill="#E8DCC8",
                            font=("Playfair Display", 48, "bold"))
        canvas.create_text(64.0, 210.0, anchor="nw", text="Remains?", fill="#B5420E",
                            font=("Playfair Display", 48, "bold", "italic"))
        canvas.create_text(64.0, 280.0, anchor="nw", text="A narrative game",
                            fill="#E8DCC8", font=("Playfair Display", 22))

        self.profile_text = canvas.create_text(
            64.0, 330.0, anchor="nw", text="", fill="#9A8872", font=("DM Mono", 10), width=500,
        )

        canvas.create_text(
            982.58, 718.6, anchor="nw",
            text='"It\'s ugly, isn\'t it?"\n\nKeep looking.',
            fill="#4A3820", font=("Playfair Display", 11, "italic"),
        )

        try:
            self._img2 = load_photo_image(relative_to_assets("main-bull.png"))
            canvas.create_image(847.79, 404.89, image=self._img2)
        except Exception:
            pass

        btn_y = 480
        self._text_btn("NEW JOURNEY", 64, btn_y, self._new_game)
        self._text_btn("CONTINUE", 64, btn_y + 52, self._continue_game)
        self._text_btn("LEADERBOARD", 64, btn_y + 104, lambda: self.controller.show_frame("LeaderboardScreen"))
        self._text_btn("SETTINGS", 64, btn_y + 156, lambda: self.controller.show_frame("SettingsScreen"))
        self._text_btn("CREDITS", 64, btn_y + 208, self._credits)
        self._text_btn("SIGN OUT", 64, btn_y + 260, self._sign_out)

        try:
            self._btn1_img = load_photo_image(relative_to_assets("button_1.png"))
            ImageButton(
                self, image=self._btn1_img, borderwidth=0, highlightthickness=0,
                command=self._new_game, relief="flat",
            ).place(x=64.0, y=559.89, width=220.0, height=48.6)
        except Exception:
            pass

    def _text_btn(self, text, x, y, cmd):
        b = tk.Button(
            self, text=text, bg="#0C0904", fg=FOG, activebackground=EMBER,
            activeforeground=CREAM, font=FONT_UI, relief="flat", anchor="w",
            command=cmd, width=24,
        )
        b.place(x=x, y=y)
        b.bind("<Enter>", lambda e: e.widget.config(fg=CREAM))
        b.bind("<Leave>", lambda e: e.widget.config(fg=FOG))

    def on_show(self):
        user = getattr(self.controller, "current_user", None) or session.load_session()
        if user:
            self.controller.current_user = user
        gs = game_state.GameState()
        pct = gs.restoration_percent()
        save_line = "No save yet"
        if user and game_state.has_save(user):
            data = game_state.load_game(user) or {}
            saved = data.get("saved_at", "")
            if saved:
                try:
                    dt = datetime.fromisoformat(saved)
                    save_line = f"Last save: {dt.strftime('%d %b %Y, %H:%M')}"
                except ValueError:
                    save_line = f"Last save: {saved[:16]}"
            pct = data.get("env_score", pct)
        name = user or "Traveler"
        profile = (
            f"Signed in as {name}\n"
            f"Restoration: {pct}%  ·  Memories: {gs.memory_fragments}\n"
            f"{save_line}"
        )
        self.canvas.itemconfig(self.profile_text, text=profile)

    def _new_game(self):
        self.controller.start_new_game = True
        self.controller.show_frame("GameScreen")

    def _continue_game(self):
        user = getattr(self.controller, "current_user", None)
        if user and game_state.has_save(user):
            self.controller.show_frame("GameScreen")
        else:
            self._new_game()

    def _credits(self):
        tk.messagebox = __import__("tkinter").messagebox
        tk.messagebox.showinfo(
            "Credits",
            "What Remains? — Group 1, COS 102\n"
            "Pan-Atlantic University · 2026\n\n"
            "Inspired by the scrap-metal bull at Yemisi Shyllon Museum of Art.",
        )

    def _sign_out(self):
        session.clear_session()
        self.controller.current_user = None
        self.controller.show_frame("SplashScreen")
