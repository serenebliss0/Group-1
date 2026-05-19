import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets" / "images"


BG = "#0d0800"

class SplashScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Initialize as a standard frame
        super().__init__(parent, bg=BG)
        self.controller = controller
        
        # Convert BG hex code to an RGB tuple for Pillow canvas blending
        self._bg_rgb = self._hex_to_rgb(BG)
        
        # Load the single combined image using Path
        # Convert to RGBA so we can manipulate the transparency channel
        self.original_img = Image.open(ASSETS / "splash.png").convert("RGBA")
        
        # 4. Create a single blank label to display the image frames
        self.image_label = tk.Label(self, bg=BG)
        self.image_label.pack(fill="both", expand=True)
        
        # 5. Run the animation sequence
        self.alpha = 0.0
        self.fade_in()

    def _hex_to_rgb(self, hex_str):
        """Converts #RRGGBB strings to an (R, G, B) integer tuple."""
        hex_str = hex_str.lstrip('#')
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

    def update_image_alpha(self, alpha_value):
        """Blends the single splash image over your custom BG color matrix."""
        # Create a blank background matching the custom hex color canvas
        bg_canvas = Image.new("RGBA", self.original_img.size, self._bg_rgb + (255,))
        
        # Mathematically interpolate the image over the background color
        blended = Image.blend(bg_canvas, self.original_img, alpha_value)
        
        # Keep a reference and push it to the label frame
        self.tk_img = ImageTk.PhotoImage(blended)
        self.image_label.configure(image=self.tk_img)

    def fade_in(self):
        if self.alpha < 1.0:
            self.alpha += 0.04  # Speed of the fade loop
            if self.alpha > 1.0: self.alpha = 1.0
            self.update_image_alpha(self.alpha)
            self.after(25, self.fade_in)  # ~40 FPS animation loop
        else:
            # Fully visible. Hold still for 2.5 seconds, then fade out
            self.after(2500, self.fade_out)

    def fade_out(self):
        if self.alpha > 0.0:
            self.alpha -= 0.04
            if self.alpha < 0.0: self.alpha = 0.0
            self.update_image_alpha(self.alpha)
            self.after(25, self.fade_out)
        else:
            # Animation finished! Tell the main app container to flip to the login
            self.controller.show_frame("LoginScreen")