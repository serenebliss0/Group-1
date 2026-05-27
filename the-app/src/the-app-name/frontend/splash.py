import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets" / "images"

BG = "#0d0800"


class SplashScreen(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        self.controller = controller


        self.image_label = tk.Label(
            self,
            bg=BG,
            bd=0
        )

        self.image_label.pack(
            fill="both",
            expand=True
        )


        image_path = ASSETS / "splash.png"

        try:
            self.original_img = Image.open(image_path).convert("RGBA")

        except Exception as e:

            print("IMAGE LOAD ERROR:", e)

            tk.Label(
                self,
                text="SPLASH IMAGE NOT FOUND",
                fg="white",
                bg=BG,
                font=("Arial", 24)
            ).pack(expand=True)

            self.after(
                1500,
                lambda: self.controller.show_frame("LoginScreen")
            )

            return


        self.after(50, self.prepare_splash)


    def prepare_splash(self):

        self.controller.update_idletasks()

        win_w = self.controller.winfo_width()
        win_h = self.controller.winfo_height()

        img = self.original_img.copy()

        img.thumbnail((win_w - 100, win_h - 100))

        self.display_img = img

        self.alpha = 0.0

        self.draw_image()

        self.after(100, self.fade_in)


    def draw_image(self):

        bg = Image.new(
            "RGBA",
            self.display_img.size,
            (13, 8, 0, 255)
        )

        blended = Image.blend(
            bg,
            self.display_img,
            self.alpha
        )

        self.tk_img = ImageTk.PhotoImage(blended)

        self.image_label.configure(image=self.tk_img)

        self.image_label.image = self.tk_img

    def fade_in(self):

        self.alpha += 0.06

        if self.alpha > 1:
            self.alpha = 1

        self.draw_image()

        if self.alpha < 1:

            self.after(30, self.fade_in)

        else:

            # SHORTER DISPLAY TIME
            self.after(1800, self.fade_out)


    def fade_out(self):

        self.alpha -= 0.06

        if self.alpha < 0:
            self.alpha = 0

        self.draw_image()

        if self.alpha > 0:

            self.after(30, self.fade_out)

        else:
            self.controller.show_frame("MainMenu")