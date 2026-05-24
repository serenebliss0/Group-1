import tkinter as tk

from backend import (
    database,
    login_handler,
    signup_handler,
    logic,
    notification,
    input_manager,
    session
)

from frontend.login import LoginScreen
from frontend.signup import SignupScreen
from frontend.splash import SplashScreen
from frontend.main_menu import MainMenu
from frontend.scene2 import Scene2


class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("The Ruin and the Green")

        self.scale = 0.8
        self.width = int(self.winfo_screenwidth() * self.scale)
        self.height = int(self.winfo_screenheight() * self.scale)
        self.geometry(f"{self.width}x{self.height}")

        self.db = database.Database()
        self.current_user = session.load_session()

        try:
            self.mixer = logic.Mixer()
            self.mixer.play_intro_sound()
        except Exception as e:
            print("Mixer error:", e)
            self.mixer = None

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.accessible_screens = (
            SplashScreen,
            LoginScreen,
            SignupScreen,
            MainMenu,
            Scene2
        )

        for F in self.accessible_screens:
            page_name = F.__name__

            try:
                frame = F(parent=self.container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            except Exception as e:
                print(f"Error loading {page_name}: {e}")

        self.after(200, self.startup_routing)

    def startup_routing(self):
        self.update_idletasks()
        self.show_frame("SplashScreen")

    def show_frame(self, page_name):

        frame = self.frames.get(page_name)

        if frame:
            frame.tkraise()

            # 🔥 RESET GAME WHEN ENTERING SCENE
            if page_name == "Scene2":
                frame.reset_game()

        else:
            print(f"Frame '{page_name}' not found")

    def on_close(self):

        try:
            if self.mixer:
                self.mixer.on_close()
        except:
            pass

        self.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()