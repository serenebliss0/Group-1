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


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("What Remains?")
        self.pending_ending = "neutral"
        self.start_new_game = False

        self.scale = 0.85
        self.width = int(self.winfo_screenwidth() * self.scale)
        self.height = int(self.winfo_screenheight() * self.scale)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(960, 640)

        self.db = database.Database()
        self.current_user = session.load_session()
        self.audio = GameAudio()
        self.audio.play_intro_sound()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        screen_classes = [
            SplashScreen,
            LoginScreen,
            SignupScreen,
            MainMenu,
            GameScreen,
            LeaderboardScreen,
            SettingsScreen,
            EndingScreen,
        ]

        self.frames = {}
        for cls in screen_classes:
            name = cls.__name__
            frame = cls(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self._current_frame = None
        if self.current_user:
            self.show_frame("MainMenu")
        else:
            self.show_frame("SplashScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if self._current_frame and hasattr(self._current_frame, "on_hide"):
            self._current_frame.on_hide()
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
        self._current_frame = frame

    def on_close(self):
        self.audio.on_close()
        if self.db:
            self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
