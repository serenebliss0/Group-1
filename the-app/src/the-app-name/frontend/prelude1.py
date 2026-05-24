import tkinter as tk
import subprocess
import sys

def go_to_next(root):
    subprocess.Popen([sys.executable, "Prelude2.py"])
    root.destroy()

def main():
    root = tk.Tk()
    root.title("Prelude 1")
    root.geometry("800x600")
    root.configure(bg="#eef1ec") 
    
    # Center the window on the screen
    root.eval('tk::PlaceWindow . center')

    text = tk.Label(
        root, 
        text="THE CITY WAKES UP SLOWLY. IT ALWAYS DOES.", 
        font=("Times New Roman", 24), 
        bg="#eef1ec", 
        fg="#0b1c2c",
        justify="center"
    )
    text.place(relx=0.5, rely=0.5, anchor="center")

    # Wait 3000ms (3 seconds) then trigger go_to_next
    root.after(3000, lambda: go_to_next(root))
    root.mainloop()

if __name__ == "__main__":
    main()
