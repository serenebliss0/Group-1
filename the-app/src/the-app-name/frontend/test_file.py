import tkinter as tk
from tkinter import ttk

# --- Main App ---
class EcoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Eco Snap 🌱")
        self.geometry("500x400")
        self.configure(bg="#1e1e1e")  # dark background

        # container for screens
        container = tk.Frame(self, bg="#1e1e1e")
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (StartScreen, GameScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartScreen)

    def show_frame(self, screen):
        frame = self.frames[screen]
        frame.tkraise()


# --- Start Screen ---
class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e1e")

        style = ttk.Style()
        style.theme_use("default")

        style.configure("TButton",
                        font=("Arial", 12),
                        padding=10)

        title = tk.Label(self,
                         text="🌱 Eco Snap",
                         font=("Arial", 24, "bold"),
                         bg="#1e1e1e",
                         fg="white")
        title.pack(pady=40)

        start_btn = ttk.Button(self,
                               text="Start Game",
                               command=lambda: controller.show_frame(GameScreen))
        start_btn.pack(pady=10)


# --- Game Screen ---
class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e1e")

        self.score = 0

        title = tk.Label(self,
                         text="Clean the Environment!",
                         font=("Arial", 16),
                         bg="#1e1e1e",
                         fg="white")
        title.pack(pady=20)

        self.score_label = tk.Label(self,
                                   text="Score: 0",
                                   font=("Arial", 12),
                                   bg="#1e1e1e",
                                   fg="lightgreen")
        self.score_label.pack(pady=10)

        clean_btn = ttk.Button(self,
                               text="Pick Trash 🗑️",
                               command=self.increase_score)
        clean_btn.pack(pady=10)

        back_btn = ttk.Button(self,
                              text="Back",
                              command=lambda: controller.show_frame(StartScreen))
        back_btn.pack(pady=10)

    def increase_score(self):
        self.score += 10
        self.score_label.config(text=f"Score: {self.score}")


# --- Run App ---
if __name__ == "__main__":
    app = EcoApp()
    app.mainloop()