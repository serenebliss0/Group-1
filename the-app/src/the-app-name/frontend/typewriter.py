import tkinter as tk

class TypewriterLabel(tk.Label):
    def __init__(self, parent, text="", speed=40, **kwargs):
        super().__init__(parent, text="", **kwargs)

        self.full_text = text
        self.speed = speed
        self.current_index = 0

    def start(self):
        self.config(text="")
        self.current_index = 0
        self.type_next()

    def type_next(self):
        if self.current_index <= len(self.full_text):
            self.config(text=self.full_text[:self.current_index])
            self.current_index += 1

            self.after(self.speed, self.type_next)