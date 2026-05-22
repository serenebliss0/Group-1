import tkinter as tk
from backend import database, login_handler, signup_handler, logic, notification, input_manager
from frontend import login, signup, splash
from frontend.login import LoginScreen
from frontend.signup import SignupScreen
from frontend.splash import SplashScreen
from app import HomeScreen, MapScreen, GameScreen, InventoryScreen, CustomizeScreen

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Ruin and the Green")

        self.scale = 0.8
        self.width = int(self.winfo_screenwidth() * self.scale)
        self.height = int(self.winfo_screenheight() * self.scale)
        self.geometry(f"{self.width}x{self.height}")

        self.db = database.Database()
        self.current_user = None

        # Game State
        self.player_health = 100
        self.player_energy = 100
        self.inventory = []
        self.current_level = None
        self.completed_levels = []
        self.tutorial_done = False
        
        self.armour_parts = {
            "head": "Rust Helmet",
            "torso": "Scrap Chest",
            "arms": "Wire Arms",
            "legs": "Metal Legs"
        }

        self.mixer = logic.Mixer()
        self.mixer.play_intro_sound()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.accesible_screens = [SplashScreen, LoginScreen, SignupScreen, HomeScreen, MapScreen, GameScreen, InventoryScreen, CustomizeScreen]
        
        for F in self.accesible_screens:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SplashScreen")

    def on_close(self):
        self.mixer.on_close()
        self.destroy()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "update_ui"):
            frame.update_ui()
        frame.tkraise()
        if page_name == "GameScreen":
            frame.focus_set()
            frame.start_level()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
