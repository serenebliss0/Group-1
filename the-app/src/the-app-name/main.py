import tkinter as tk
from backend import database, session
from backend.audio import GameAudio
from frontend.login import LoginScreen
from frontend.signup import SignupScreen
from frontend.splash import SplashScreen
from frontend.main_menu import MainMenu
from frontend.game_screen import GameScreen
from frontend.leaderboard import LeaderboardScreen
from frontend.settings import SettingsScreen
from frontend.ending_screen import EndingScreen
from frontend.act1 import ActOne
from frontend.scene2 import Scene2
from backend import login_handler, signup_handler, logic, input_manager
from frontend import login, signup, splash, main_menu, scene2
from frontend.login import LoginScreen
from frontend.signup import SignupScreen
from frontend.splash import SplashScreen
from frontend.main_menu import MainMenu


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("What Remains?")

        self.scale = 0.8
        self.width = int(self.winfo_screenwidth() * self.scale)
        self.height = int(self.winfo_screenheight() * self.scale)
        self.geometry(f"{self.width}x{self.height}")

        self.db = database.Database()
        self.current_user = None

        self.mixer = logic.Mixer()
        self.mixer.play_intro_sound()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #this ensures the login/signup frames only appear when no user is signed in
        self.current_user = session.load_session()

        self.accesible_screens = [SplashScreen, LoginScreen, SignupScreen, MainMenu, Scene2]
        
        for F in self.accesible_screens:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        if self.current_user is None:
            self.show_frame("SplashScreen")
        else:
            self.show_frame("MainMenu")
    def on_close(self):
        self.mixer.on_close()
        self.destroy()

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

    print(logic.wtf_value) ## Remove this later

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
    