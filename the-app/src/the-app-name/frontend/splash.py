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

        # Main display label
        self.image_label = tk.Label(self, bg=BG, bd=0)
        self.image_label.pack(fill="both", expand=True)

        # Load image safely
        image_path = ASSETS / "splash.png"

        try:
            self.original_img = Image.open(image_path).convert("RGBA")

            # Resize image to fit window nicely
            self.original_img = self.original_img.resize(
                (800, 500)
            )

        except Exception as e:
            print("IMAGE LOAD ERROR:", e)

            # fallback text so splash still works
            tk.Label(
                self,
                text="SPLASH IMAGE NOT FOUND",
                fg="white",
                bg=BG,
                font=("Arial", 24)
            ).pack(expand=True)

            self.after(2000, self.go_next)
            return

        # Animation state
        self.alpha = 0.0

        # Start after Tk fully renders
        self.after(100, self.fade_in)

    def draw_image(self):
        # Create background canvas
        bg = Image.new(
            "RGBA",
            self.original_img.size,
            (13, 8, 0, 255)
        )

        # Blend image with alpha
        blended = Image.blend(
            bg,
            self.original_img,
            self.alpha
        )

        self.tk_img = ImageTk.PhotoImage(blended)

        self.image_label.configure(image=self.tk_img)
        self.image_label.image = self.tk_img

    def fade_in(self):
        if self.alpha < 1.0:
            self.alpha += 0.05

            if self.alpha > 1.0:
                self.alpha = 1.0

            self.draw_image()

            self.after(30, self.fade_in)

        else:
            self.after(2000, self.fade_out)

    def fade_out(self):
        if self.alpha > 0.0:
            self.alpha -= 0.05

            if self.alpha < 0.0:
                self.alpha = 0.0

            self.draw_image()

            self.after(30, self.fade_out)

        else:
            # Tell the main app container to flip to the login
            self.controller.show_frame("LoginScreen")