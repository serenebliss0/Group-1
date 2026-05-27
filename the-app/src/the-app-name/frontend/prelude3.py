import tkinter as tk

class Prelude3(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#eef1ec")

        self.controller = controller
        self.after_id = None

        self.label = tk.Label(
            self,
            text="",
            font=("Times New Roman", 24),
            bg="#eef1ec",
            fg="#0b1c2c",
            justify="center",
            wraplength=700
        )

        self.label.place(relx=0.5, rely=0.5, anchor="center")


    def on_show(self):

        username = getattr(self.controller, "user_info", "UNKNOWN")

        self.label.config(
            text=f"YOUR NAME IS {username}. PEOPLE KNOW YOU HERE. OR THEY THINK THEY DO."
        )

        self.after_id = self.after(
            3000,
            lambda: self.controller.show_frame("Prelude4")
        )


    def on_hide(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None