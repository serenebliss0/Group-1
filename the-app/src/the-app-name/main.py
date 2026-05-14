import tkinter as tk
from backend import database, login_handler, signup_handler, logic
from frontend import login, signup
from frontend.login import LoginScreen
from frontend.signup import SignupScreen

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Ruin and the Green")

        scale = 0.8
        self.width = int(self.winfo_screenwidth() * scale)
        self.height = int(self.winfo_screenheight() * scale)
        self.geometry(f"{self.width}x{self.height}")

        self.db = database.Database()
        self.current_user = None

        #init audio ONCE here
        self.mixer = logic.Mixer()
        self.mixer.play_intro_sound()

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # build screens ONLY
        for F in (LoginScreen, SignupScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # show ONCE after setup
        self.show_frame("LoginScreen")
    
    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()