import tkinter as tk
from backend import database, login_handler, signup_handler, logic, notification, input_manager
from frontend import login, signup, splash
from frontend.login import LoginScreen
from frontend.signup import SignupScreen
from frontend.splash import SplashScreen

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

        self.mixer = logic.Mixer()
        self.mixer.play_intro_sound()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.accesible_screens = [SplashScreen, LoginScreen, SignupScreen]
        
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
        self.frames[page_name].tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
