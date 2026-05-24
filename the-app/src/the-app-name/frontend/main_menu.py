from pathlib import Path
import sys
import tkinter as tk
from tkinter import Canvas, Label
from PIL import Image, ImageTk

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_PATH = BASE_DIR / "assets" / "images"
IMAGE_REFS = []

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_photo_image(path: str):
    try:
        image = tk.PhotoImage(file=str(path))
    except Exception:
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
        if self._command is not None:
            self._command()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#000000")
        self.controller = controller
        self._build()

    def _build(self):
        canvas = Canvas(
            self,
            bg="#000000",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        button_image_1 = load_photo_image(relative_to_assets("begin_button.png"))
        ImageButton(
            self,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("GameScreen"),
            relief="flat",
            bg="#000000"
        ).place(x=75.0, y=353.0, width=350.0, height=64.0)

        button_image_2 = load_photo_image(relative_to_assets("mainleaderboard.png"))
        ImageButton(
            self,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("LeaderboardScreen"),
            relief="flat",
            bg="#000000"
        ).place(x=75.0, y=478.0, width=350.0, height=64.0)

        button_image_3 = load_photo_image(relative_to_assets("settings_button.png"))
        ImageButton(
            self,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("SettingsScreen"),
            relief="flat",
            bg="#000000"
        ).place(x=75.0, y=603.0, width=350.0, height=64.0)

        canvas.create_text(
            487.0, 667.0, anchor="nw",
            text="+COS 102 · GROUP 1 · PAN-ATLANTIC UNIVERSITY · 2026",
            fill="#4A3820",
            font=("DM Mono", 15 * -1, "normal", "roman")
        )

        image_image_1 = load_photo_image(relative_to_assets("image_1.png"))
        canvas.create_image(1275.0, 361.0, image=image_image_1)

        canvas.create_text(
            181.0, 103.0, anchor="nw",
            text="What",
            fill="#E8DCC8",
            font=("Playfair Display", 128 * -1, "bold", "roman")
        )

        canvas.create_text(
            545.0, 103.0, anchor="nw",
            text="Remains?",
            fill="#B5420E",
            font=("Playfair Display", 128 * -1, "bold", "italic")
        )

        image_image_2 = load_photo_image(relative_to_assets("bull_outline.png"))
        canvas.create_image(1219.0, 494.0, image=image_image_2)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    root.configure(bg="#000000")
    root.resizable(False, False)
    root.show_frame = lambda name: print(f"navigate to → {name}")
    app = MainMenu(root, controller=root)
    app.place(relwidth=1, relheight=1)
    root.mainloop()