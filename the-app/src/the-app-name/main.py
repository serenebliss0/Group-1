import tkinter as tk

from backend import database, session, logger, logic
from backend.logger import get_logger
from backend.audio import GameAudio
from frontend.login import LoginScreen
from frontend.signup import SignupScreen
from frontend.splash import SplashScreen
from frontend.main_menu import MainMenu
from frontend.scene2 import SceneScreen

class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("What Remains?")

        self.pending_ending = "neutral"
        self.start_new_game = False
        self._current_frame = None

        self.scale = 0.85

        self.width = int(self.winfo_screenwidth() * self.scale)
        self.height = int(self.winfo_screenheight() * self.scale)

        self.geometry(f"{self.width}x{self.height}")

        self.minsize(960, 640)

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

        self.accesible_screens = [SplashScreen, LoginScreen, SignupScreen, MainMenu, SceneScreen]
        
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

        try:
            self.audio.on_close()
        except Exception:
            pass

        try:
            if self.db:
                self.db.close()
        except Exception:
            pass

        self.destroy()

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

    print(logic.wtf_value) ## Remove this later

if __name__ == "__main__":

    app = MainApp()
    app.mainloop()
    
