import tkinter as tk

class Prelude5(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#eef1ec")

        self.controller = controller
        self.after_id = None

        tk.Label(
            self,
            text="TODAY FEELS LIKE ANY OTHER DAY.",
            font=("Times New Roman", 24),
            bg="#eef1ec",
            fg="#0b1c2c",
            justify="center"
        ).place(relx=0.5, rely=0.5, anchor="center")


    def on_show(self):
        self.after_id = self.after(
            3000,
            lambda: self.controller.show_frame("Scene2")
        )


    def on_hide(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None