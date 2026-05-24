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
        self.current_user = session.load_session()
        self.audio = GameAudio()
        self.audio.play_intro_sound()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for cls in (
            SplashScreen,
            LoginScreen,
            SignupScreen,
            MainMenu,
            ActOne,
            GameScreen,
            LeaderboardScreen,
            SettingsScreen,
            EndingScreen,
            Scene2
        ):
            name = cls.__name__
            try:
                frame = cls(parent=self.container, controller=self)
                self.frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            except Exception as e:
                print(f"Error loading {name}: {e}")

        self.after(200, self._startup)

    def _startup(self):
        self.update_idletasks()
        if self.current_user:
            self.show_frame("MainMenu")
        else:
            self.show_frame("SplashScreen")

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if not frame:
            print(f"Frame '{page_name}' not found")
            return
        if self._current_frame and hasattr(self._current_frame, "on_hide"):
            self._current_frame.on_hide()
        self._current_frame = frame
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
        if page_name == "GameScreen" and hasattr(frame, "reset_game"):
            frame.reset_game()

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


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()