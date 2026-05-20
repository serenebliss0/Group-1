from pathlib import Path
import ctypes
import sys
from tkinter import (
    Canvas, Frame, Label, PhotoImage, Tk
)

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_PATH = BASE_DIR / "assets" / "images"
IMAGE_REFS = []

def relative_to_assets(path: str):
    return ASSETS_PATH / path

def load_photo_image(path: str):
    try:
        image = PhotoImage(file=path)
    except Exception:
        if Image is None or ImageTk is None:
            raise
        image = ImageTk.PhotoImage(Image.open(path))
    IMAGE_REFS.append(image)
    return image

class ImageButton(Label):
    def __init__(self, master=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self._command = command
        self.configure(cursor="hand2")
        self.bind("<Button-1>", self._invoke)

    def _invoke(self, event):
        if self._command:
            self._command()

    def configure(self, cnf=None, **kwargs):
        if cnf and "command" in cnf:
            cnf = dict(cnf)
            self._command = cnf.pop("command")
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        return super().configure(cnf, **kwargs)

    config = configure


class MainMenu(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0C0904")
        self.controller = controller
        self._build()

    def _build(self):
        canvas = Canvas(
            self,
            bg="#0C0904",
            height=826,
            width=1130,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        canvas.create_text(
            64.0, 98.71,
            anchor="nw",
            text="COS 102 · GROUP 1 · PAN-ATLANTIC UNIVERSITY · 2026",
            fill="#4A3820",
            font=("DM Mono", -9, "normal", "roman")
        )
        canvas.create_text(
            64.0, 159.81,
            anchor="nw",
            text="What",
            fill="#E8DCC8",
            font=("Playfair Display", -79, "bold", "roman")
        )
        canvas.create_text(
            64.0, 231.02,
            anchor="nw",
            text="Remains?",
            fill="#B5420E",
            font=("Playfair Display", -79, "bold", "italic")
        )
        canvas.create_text(
            64.0, 317.84,
            anchor="nw",
            text="A narrative game",
            fill="#E8DCC8",
            font=("Playfair Display", -35, "normal", "roman")
        )
        canvas.create_text(
            64.0, 415.89,
            anchor="nw",
            text="You are a citizen of a dying city making impossible decisions.\n\nUntil you realise you are not a citizen at all.",
            fill="#9A8872",
            font=("DM Mono", -12, "normal", "italic")
        )
        canvas.create_text(
            1017.6, 48.0,
            anchor="nw",
            text="?",
            fill="#2A1E10",
            font=("Playfair Display", -120, "bold", "roman")
        )
        canvas.create_text(
            982.58, 718.6,
            anchor="nw",
            text="\"It's ugly, isn't it?\"\n\nKeep looking.",
            fill="#4A3820",
            font=("Playfair Display", -11, "normal", "italic")
        )

        # ── Images ──
        try:
            self._img1 = load_photo_image(relative_to_assets("image_1.png"))
            canvas.create_image(88.0, 382.89, image=self._img1)
        except Exception:
            pass

        try:
            self._img2 = load_photo_image(relative_to_assets("main-bull.png"))
            canvas.create_image(847.79, 404.89, image=self._img2)
        except Exception:
            pass

        # ── Buttons ──
        try:
            self._btn1_img = load_photo_image(relative_to_assets("button_1.png"))
            ImageButton(
                self,
                image=self._btn1_img,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.controller.show_frame("LoginScreen"),
                relief="flat"
            ).place(x=64.0, y=559.89, width=220.0, height=48.6)
        except Exception:
            pass

        try:
            self._btn2_img = load_photo_image(relative_to_assets("main-leaderboard.png"))
            ImageButton(
                self,
                image=self._btn2_img,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.controller.show_frame("LeaderboardScreen"),
                relief="flat"
            ).place(x=64.0, y=620.49, width=220.0, height=47.1)
        except Exception:
            pass

        try:
            self._btn3_img = load_photo_image(relative_to_assets("main-settings.png"))
            ImageButton(
                self,
                image=self._btn3_img,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.controller.show_frame("SettingsScreen"),
                relief="flat"
            ).place(x=64.0, y=679.59, width=220.0, height=47.1)
        except Exception:
            pass