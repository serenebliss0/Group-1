from pathlib import Path
from tkinter import Canvas, Frame, Label, PhotoImage

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


# ---------------- PATH (STABLE) ---------------- #
BASE_DIR = Path(__file__).resolve().parent.parent
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


# ---------------- BUTTON CLASS ---------------- #
class ImageButton(Label):
    def __init__(self, master=None, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self._command = command

        self.configure(cursor="hand2")

        self.bind("<Button-1>", self._invoke)

    def _invoke(self, event):
        if self._command:
            self._command()


# ---------------- MAIN MENU ---------------- #
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
            highlightthickness=0
        )

        canvas.place(x=0, y=0)

        # ---------------- TEXT ---------------- #

        canvas.create_text(
            64,
            98,
            anchor="nw",
            text="COS 102 · GROUP 1 · PAN-ATLANTIC UNIVERSITY · 2026",
            fill="#4A3820",
            font=("DM Mono", -9)
        )

        canvas.create_text(
            64,
            159,
            anchor="nw",
            text="What",
            fill="#E8DCC8",
            font=("Playfair Display", -79, "bold")
        )

        canvas.create_text(
            64,
            231,
            anchor="nw",
            text="Remains?",
            fill="#B5420E",
            font=("Playfair Display", -79, "bold", "italic")
        )

        canvas.create_text(
            64,
            317,
            anchor="nw",
            text="A narrative game",
            fill="#E8DCC8",
            font=("Playfair Display", -35)
        )

        canvas.create_text(
            64,
            415,
            anchor="nw",
            text=(
                "You are a citizen of a dying city making impossible decisions.\n\n"
                "Until you realise you are not a citizen at all."
            ),
            fill="#9A8872",
            font=("DM Mono", -12, "italic")
        )

        canvas.create_text(
            1017,
            48,
            anchor="nw",
            text="?",
            fill="#2A1E10",
            font=("Playfair Display", -120, "bold")
        )

        canvas.create_text(
            982,
            718,
            anchor="nw",
            text="\"It's ugly, isn't it?\"\n\nKeep looking.",
            fill="#4A3820",
            font=("Playfair Display", -11, "italic")
        )

        # ---------------- DEBUG ---------------- #

        print("BASE_DIR:", BASE_DIR)
        print("ASSETS_PATH:", ASSETS_PATH)
        print("ASSETS EXISTS:", ASSETS_PATH.exists())

        # ---------------- IMAGES ---------------- #

        try:
            self._img1 = load_photo_image(
                relative_to_assets("image_1.png")
            )

            canvas.create_image(
                88,
                382,
                image=self._img1
            )

        except Exception as e:
            print("FAILED image_1.png:", e)

        try:
            self._img2 = load_photo_image(
                relative_to_assets("player.png")
            )

            canvas.create_image(
                847,
                404,
                image=self._img2
            )

        except Exception as e:
            print("FAILED player.png:", e)

        # ---------------- BUTTONS ---------------- #

        # Scene Button
        try:
            self._btn1_img = load_photo_image(
                relative_to_assets("button_1.png")
            )

            ImageButton(
                self,
                image=self._btn1_img,
                command=lambda: self.controller.show_frame("Scene2")
            ).place(
                x=64,
                y=559,
                width=220,
                height=48
            )

        except Exception as e:
            print("FAILED button_1.png:", e)

        # Leaderboard Button
        try:
            self._btn2_img = load_photo_image(
                relative_to_assets("main-leaderboard.png")
            )

            ImageButton(
                self,
                image=self._btn2_img,
                command=lambda: self.controller.show_frame("LeaderboardScreen")
            ).place(
                x=64,
                y=620,
                width=220,
                height=47
            )

        except Exception as e:
            print("FAILED main-leaderboard.png:", e)

        # ---------------- SETTINGS BUTTON ---------------- #

        try:
            self._btn3_img = load_photo_image(
                relative_to_assets("main-settings.png")
            )

            ImageButton(
                self,
                image=self._btn3_img,
                command=lambda: self.controller.show_frame("SettingsScreen")
            ).place(
                x=64,
                y=679,
                width=220,
                height=47
            )

        except Exception as e:
            print("FAILED main-settings.png:", e)