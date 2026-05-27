import tkinter as tk

from backend import database, session, logger, logic
from backend.logger import get_logger
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
from frontend.prelude1 import Prelude1
from frontend.prelude2 import Prelude2
from frontend.prelude3 import Prelude3
from frontend.prelude4 import Prelude4
from frontend.prelude5 import Prelude5
from frontend.end_screen import EndScreen

logger = get_logger("Main")

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

        self.user_info = logic.username

        try:
            self.audio.play_intro_sound()
        except Exception as e:
            logger.error(f"Audio error: {e}")

        self.protocol("WM_DELETE_WINDOW", self.on_close)


        self.container = tk.Frame(self)

        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        try:
            splash = SplashScreen(
                parent=self.container,
                controller=self
            )

            self.frames["SplashScreen"] = splash

            splash.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

            splash.tkraise()

            self._current_frame = splash

        except Exception as e:
            logger.error(f"CRITICAL SPLASH ERROR: {e}")


        self.after(300, self.load_remaining_frames)


    def load_remaining_frames(self):
        screens = (
            LoginScreen,
            SignupScreen,
            MainMenu,
            ActOne,
            GameScreen,
            LeaderboardScreen,
            SettingsScreen,
            EndingScreen,
            Scene2,
            Prelude1,
            Prelude2,
            Prelude3,
            Prelude4,
            Prelude5,
            EndScreen
        )

        for cls in screens:

            name = cls.__name__

            try:
                frame = cls(
                    parent=self.container,
                    controller=self
                )

                self.frames[name] = frame

                frame.grid(
                    row=0,
                    column=0,
                    sticky="nsew"
                )

                logger.info(f"Loaded: {name}")

            except Exception as e:
                logger.error(f"Error loading {name}: {e}")


        if "SplashScreen" in self.frames:
            self.frames["SplashScreen"].tkraise()


    def show_frame(self, page_name):

        frame = self.frames.get(page_name)

        if not frame:
            logger.error(f"Frame '{page_name}' not found")
            return

        if self._current_frame and hasattr(self._current_frame, "on_hide"):
            self._current_frame.on_hide()

        self._current_frame = frame

        frame.tkraise()

        if hasattr(frame, "on_show"):
            frame.on_show()

        if page_name == "GameScreen" and hasattr(frame, "reset_game"):
            #pass
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