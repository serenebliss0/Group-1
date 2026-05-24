import tkinter as tk
import subprocess
import sys

def go_to_next(root):
    subprocess.Popen([sys.executable, "Prelude4.py"])
    root.destroy()

def main():
    root = tk.Tk()
    root.title("Prelude 3")
    root.geometry("800x600")
    root.configure(bg="#eef1ec")
    root.eval('tk::PlaceWindow . center')

    text = tk.Label(
        root, 
        text="YOUR NAME IS [USERNAME] PEOPLE KNOW YOU HERE. OR THEY THINK THEY DO.", 
        font=("Times New Roman", 24), 
        bg="#eef1ec", 
        fg="#0b1c2c",
        justify="center"
    )
    text.place(relx=0.5, rely=0.5, anchor="center")

    root.after(3000, lambda: go_to_next(root))
    root.mainloop()

if __name__ == "__main__":
    main()