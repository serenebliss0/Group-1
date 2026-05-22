import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets" / "images"

# Design System Colors
BG = "#1a0a00"      # Ruin Dark background color [cite: 182, 191]
EMBER = "#C8541A"   # Accent line highlight [cite: 182]

class GameMapScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        
        # Track map state sizing
        self.map_width = 3840
        self.map_height = 2160
        
        self._build_viewport()
        
    def _build_viewport(self):
        # 1. Create the Master Viewing Portal (Fills the available application UI space)
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # 2. Load the High-Resolution Concept Map Image using Pillow
        try:
            # Sourced textured background reflecting oxidised metal or internal circuitry [cite: 48, 180]
            raw_img = Image.open(ASSETS / "game_map.png")
            
            # Double-check safety constraints if you ever need runtime scaling adjustments
            if raw_img.size != (self.map_width, self.map_height):
                raw_img = raw_img.resize((self.map_width, self.map_height), Image.LANCZOS)
                
            self.map_image = ImageTk.PhotoImage(raw_img)
            
            # Render image inside virtual space (Anchored top-left at 0, 0)
            self.canvas.create_image(0, 0, image=self.map_image, anchor="nw")
            
            # Set scroll boundary zone boundaries to match image dimensions
            self.canvas.configure(scrollregion=(0, 0, self.map_width, self.map_height))
            
        except Exception as e:
            # Graceful developer logic tracking errors to logger.txt if file asset is missing [cite: 272, 309]
            self.canvas.create_text(
                600, 400, 
                text=f"MAP ASSET ERROR: Ensure game_map.png is {self.map_width}x{self.map_height}\nDetail: {e}",
                fill="#4a3728", font=("Courier", 12, "bold") # Ash subdued color fallback [cite: 182, 189]
            )

        # 3. Bind Controls for Interactive Map Traversal (Click & Drag)
        self.canvas.bind("<ButtonPress-1>", self._scroll_start)
        self.canvas.bind("<B1-Motion>", self._scroll_move)
        
        # Optional: Render an asset placeholder indicator showing the player's initial orientation position
        # Representing an alert bull navigating the dark city environment matrix [cite: 55, 115]
        self.player_marker = self.canvas.create_oval(
            1920-15, 1080-15, 1920+15, 1080+15, 
            fill=EMBER, outline="#f5ead8", width=2 # Cream highlight details [cite: 182]
        )

    def _scroll_start(self, event):
        """Remembers coordinate origins when the click-drag interaction triggers."""
        self.canvas.scan_mark(event.x, event.y)

    def _scroll_move(self, event):
        """Computes shifts on drag updates, scrolling the viewport dynamically."""
        # Adjusting values changes camera panning resistance
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def move_player_to(self, target_x, target_y):
        """Moves the player marker across the map and centres the camera viewport."""
        # Update marker coordinates on virtual coordinates grid map
        self.canvas.coords(
            self.player_marker, 
            target_x-15, target_y-15, target_x+15, target_y+15
        )
        
        # Center camera view bounding boxes onto new coordinates location
        win_w = self.canvas.winfo_width()
        win_h = self.canvas.winfo_height()
        
        # Convert absolute target pixel locations to percentage scroll float requirements
        scroll_x = (target_x - (win_w / 2)) / self.map_width
        scroll_y = (target_y - (win_h / 2)) / self.map_height
        
        self.canvas.xview_moveto(scroll_x)
        self.canvas.yview_moveto(scroll_y)


if __name__ == '__main__':
        root = tk.Tk()
        root.geometry("900x600")
        root.configure(bg="#0d0800")
        #app = LoginScreen(root, controller=None)
        #app.pack(fill="both", expand=True)
        root.mainloop()